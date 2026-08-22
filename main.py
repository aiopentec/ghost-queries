import requests
import json
import os
import re
import datetime
from google import genai

GEMINI_KEY = os.environ.get('GEMINI_KEY')
INDEXNOW_KEY = os.environ.get('INDEXNOW_KEY')
AFFILIATE_LINK = os.environ.get('AFFILIATE_LINK')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')  # set this as a repo secret too
REPO_NAME = "ghost-queries"
STATE_FILE = "processed_questions.json"

client = genai.Client(api_key=GEMINI_KEY)


def load_processed_ids():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return set(json.load(f))
    return set()


def save_processed_ids(ids):
    with open(STATE_FILE, 'w') as f:
        json.dump(sorted(ids), f)


def get_unanswered_question(processed_ids):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody",
        "answers": 0,
        "pagesize": 30,
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Stack Exchange API error: {e}")
        return None

    for q in data.get('items', []):
        if q['score'] > 2 and q['question_id'] not in processed_ids:
            return q
    return None


def generate_solution(question):
    prompt = f"""You are an expert developer. A user asked this question and never got an answer:
Title: {question['title']}
Body: {question['body'][:2000]}

Write a clear, step-by-step technical solution in Markdown format. Do not include
any affiliate links, disclosures, or sign-offs — those will be added separately."""
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


def slugify(title):
    safe = re.sub(r'[^a-z0-9\s-]', '', title.lower())
    safe = re.sub(r'\s+', '-', safe).strip('-')
    return safe[:60]


def save_to_website(question, solution):
    slug = slugify(question['title'])
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f"_posts/{date_str}-{slug}.md"
    so_link = question.get('link', f"https://stackoverflow.com/q/{question['question_id']}")

    disclosure = (
        "\n\n---\n*This post contains an affiliate link. "
        "If you buy through it, I may earn a small commission at no extra cost to you.*\n"
    )
    affiliate_block = (
        f"\n## Level Up Your Skills\n"
        f"If you want to master solving problems like this, I recommend "
        f"[this book]({AFFILIATE_LINK})."
    )
    attribution = f"\n\n*Originally asked on [Stack Overflow]({so_link}).*"

    content = (
        f"---\nlayout: post\ntitle: \"{question['title']}\"\n---\n"
        f"{solution}{affiliate_block}{attribution}{disclosure}"
    )

    os.makedirs("_posts", exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)

    base_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"
    post_url = f"{base_url}{date_str.replace('-', '/')}/{slug}/"
    ping_url = "https://api.indexnow.org/IndexNow"
    payload = {
        "host": f"{GITHUB_USERNAME}.github.io",
        "key": INDEXNOW_KEY,
        "keyLocation": f"{base_url}{INDEXNOW_KEY}.txt",
        "urlList": [post_url],
    }
    try:
        requests.post(ping_url, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"IndexNow ping failed (non-fatal): {e}")

    return question['question_id']


if __name__ == "__main__":
    processed = load_processed_ids()
    q = get_unanswered_question(processed)
    if q:
        print(f"Found orphaned question: {q['title']}")
        solution = generate_solution(q)
        if solution:
            qid = save_to_website(q, solution)
            processed.add(qid)
            save_processed_ids(processed)
            print("Successfully generated and saved solution!")
        else:
            print("Generation failed — skipping this run.")
    else:
        print("No new suitable questions found today.")
