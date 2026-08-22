---
layout: default
title: ghost-queries
---

# Ghost Queries

Answers to abandoned Stack Overflow questions, generated daily.

<ul>
  {% for post in site.posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    — {{ post.date | date: "%B %-d, %Y" }}
  </li>
  {% endfor %}
</ul>
