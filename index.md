---
layout: default
title: Ghost Queries — AI Answers to Abandoned Questions
---

<div class="ghost-queries-index">

  <p>Every post here answers a real question that sat unanswered on Stack Exchange.
  Sorted by topic below — newest first within each.</p>

  {%- comment -%}
    Known verticals, in the order they should display. Add a new
    "slug,Label" pair here the day you onboard a new SITE_CONFIG category
    in main.py — nothing else in this file needs to change.
  {%- endcomment -%}
  {% assign known_slugs = "code-fixes,sysadmin,superuser-tips" | split: "," %}
  {% assign known_labels = "Code Fixes,Sysadmin & Ops,Superuser Tips" | split: "," %}

  {%- comment -%} Jump nav, only shown once there's more than one group present {%- endcomment -%}
  {% assign present_slugs = site.posts | map: "category" | uniq %}
  {% if present_slugs.size > 1 %}
    <nav class="category-jumpnav">
      {% for slug in known_slugs %}
        {% assign idx = forloop.index0 %}
        {% if present_slugs contains slug %}
          <a href="#{{ slug }}">{{ known_labels[idx] }}</a>
        {% endif %}
      {% endfor %}
      {% for slug in present_slugs %}
        {% unless known_slugs contains slug %}
          <a href="#{{ slug }}">{{ slug | replace: '-', ' ' | capitalize }}</a>
        {% endunless %}
      {% endfor %}
    </nav>
  {% endif %}

  {%- comment -%} Known categories, in fixed order {%- endcomment -%}
  {% for slug in known_slugs %}
    {% assign idx = forloop.index0 %}
    {% assign posts_in_cat = site.posts | where: "category", slug %}
    {% if posts_in_cat.size > 0 %}
      <section class="category-group" id="{{ slug }}">
        <h2>{{ known_labels[idx] }}</h2>
        <ul>
          {% for post in posts_in_cat %}
            <li>
              <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
              <span class="post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
            </li>
          {% endfor %}
        </ul>
      </section>
    {% endif %}
  {% endfor %}

  {%- comment -%}
    Catch-all: any category that shows up in a post's front matter but
    isn't in known_slugs yet (e.g. you cloned main.py to a new vertical
    and forgot to add it above). Keeps new verticals from silently
    vanishing from the index instead of failing loudly.
  {%- endcomment -%}
  {% for slug in present_slugs %}
    {% unless known_slugs contains slug %}
      {% assign posts_in_cat = site.posts | where: "category", slug %}
      <section class="category-group" id="{{ slug }}">
        <h2>{{ slug | replace: '-', ' ' | capitalize }}</h2>
        <ul>
          {% for post in posts_in_cat %}
            <li>
              <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
              <span class="post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
            </li>
          {% endfor %}
        </ul>
      </section>
    {% endunless %}
  {% endfor %}

</div>
