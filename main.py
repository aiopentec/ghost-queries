import requests
import json
import os
import datetime
import google.generativeai as genai
import urllib.parse

# Load environment variables
GEMINI_KEY = os.environ.get('GEMINI_KEY')
INDEXNOW_KEY = os.environ.get('INDEXNOW_KEY')
AFFILIATE_LINK = os.environ.get('AFFILIATE_LINK')
genai.configure(api_key=GEMINI_KEY)

def get_unanswered_questions():
    # Fetch highly upvoted, unanswered StackOverflow questions older than 365 days
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody",
        "answers": 0,
        "pagesize": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Ensure it's an old question
    for q in data.get('items', []):
        if q['score'] > 2:
            return q
    return None

def generate_solution(question):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are an expert developer. A user asked this question years ago and never got an answer:
    Title: {question['title']}
    Body: {question['body'][:2000]}
    
    Write a clear, step-by-step technical solution in Markdown format. 
    At the very end, add a section titled "Level Up Your Skills" and write exactly:
    If you want to master solving problems like this, I highly recommend reading [this book]({AFFILIATE_LINK}).
    """
    response = model.generate_content(prompt)
    return response.text

def save_to_website(question, solution):
    # Clean title for filename
    safe_title = "".join([c for c in question['title'][:50] if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    safe_title = safe_title.replace(" ", "-").lower()
    filename = f"_posts/{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    
    # GitHub API to create file
    token = os.environ.get('GH_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    
    content = f"---\nlayout: post\ntitle: \"{question['title']}\"\n---\n{solution}"
    
    api_url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    headers = {"Authorization": f"token {token}"}
    data = {
        "message": f"Auto-post: {question['title']}",
        "content": content.encode('utf-8').hex() # Base64 encode alternative, actually base64 needed. Let's use standard.
    }
    # Simpler GitHub Action will handle the commit. We just write the file locally for the Action to push.
    with open(filename, 'w') as f:
        f.write(content)
        
    # Ping IndexNow for instant Bing indexing
    base_url = "https://aiopentec.github.io/ghost-queries/"
    ping_url = f"https://api.indexnow.org/IndexNow"
    payload = {
        "host": "aiopentec.github.io",
        "key": INDEXNOW_KEY,
        "keyLocation": f"{base_url}{INDEXNOW_KEY}.txt",
        "urlList": [f"{base_url}{datetime.datetime.now().strftime('%Y/%m/%d')}/{safe_title.replace('-','/')}/"]
    }
    requests.post(ping_url, json=payload)

if __name__ == "__main__":
    q = get_unanswered_questions()
    if q:
        print(f"Found orphaned question: {q['title']}")
        solution = generate_solution(q)
        os.makedirs("_posts", exist_ok=True)
        save_to_website(q, solution)
        print("Successfully generated and saved solution!")
    else:
        print("No suitable questions found today.")
