---
title: "단독 글"
nav_order: 3
has_children: true
has_toc: false
permalink: /standalone/
---

{%- assign standalone_posts = site.pages | where: "parent", page.title | sort: "nav_order" -%}

<div class="series-hero">
  <div class="series-eyebrow"><span>Standalone · 단독 글</span><span>총 {{ standalone_posts.size }}편</span></div>
  <h1>단독 글</h1>
  <p>특정 시리즈에 속하지 않는 개발 및 AI 활용 관련 단독 글을 모았습니다. 관심 있는 주제부터 자유롭게 읽으세요.</p>
</div>

<div class="series-index series-index--flat">
  {%- for post in standalone_posts %}
  {% include post-row.html post=post %}
  {%- endfor %}
</div>
