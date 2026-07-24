---
title: "Home"
layout: home
nav_order: 1
permalink: /
---

{% assign dated_pages = site.pages | where_exp: "item", "item.date != nil" | sort: "date" | reverse %}
{% assign recent_pages = dated_pages | slice: 0, 4 %}
{% assign latest_page = recent_pages | first %}

<div class="series-hero">
  <div class="series-eyebrow"><span>AI Agent Diary</span><span>최근 업데이트 {{ latest_page.date | date: "%Y.%m.%d" }} · 글 {{ dated_pages.size }}편</span></div>
  <h1 class="series-hero-title"><img src="{{ '/assets/images/brand/wordmark.svg' | relative_url }}" alt="SJ archive" width="380" height="150"></h1>
  <p>AI Agent, SDD, 개발 방법론, 그리고 AI 시대에 대한 이야기를 기록하는 개인 기술 블로그입니다.</p>
</div>

<section class="series-section home-latest">
  <div class="series-section-heading">
    <h2>최근 글</h2>
    <span>최신순</span>
  </div>
  <div class="series-index series-index--flat">
    {% for article in recent_pages %}
    <a class="series-row" href="{{ article.url | relative_url }}">
      <span class="series-body">
        <span class="series-row-meta">
          {% if forloop.first %}<span class="latest-badge">NEW</span>{% endif %}
          <span class="series-row-category">{% if article.parent == "Standalone" %}단독 글{% else %}{{ article.parent }}{% endif %}</span>
        </span>
        <span class="series-row-head"><span class="series-row-title">{{ article.title }}</span><span class="series-date">{{ article.date | date: "%Y.%m.%d" }}</span></span>
        {% if article.description %}<span class="series-row-desc">{{ article.description }}</span>{% endif %}
      </span>
    </a>
    {% endfor %}
  </div>
</section>

<section class="series-section">
  <h2>시리즈</h2>
  <div class="series-cards">
    <a class="series-card" href="./series/agent-sdd/">
      <span class="series-card-kicker">Series · 8편</span>
      <h3>Agent SDD 실무 개발</h3>
      <p>AI Agent를 실무 개발에 안정적으로 붙이기 위한 작업 등급화, 명세 기반 구현, 백로그를 이용한 세션 연속성, 도메인 문서로 탐색 줄이기, skill의 지시-예시 충돌, PR에서 business 문서를 안전하게 갱신하는 절차와 Skill Eval 검증까지.</p>
      <span class="series-card-more">시리즈 열기 →</span>
    </a>
    <a class="series-card" href="./series/ai-future-dialogue/">
      <span class="series-card-kicker">Series · 프롤로그 + 7편</span>
      <h3>AI에게 물어본 인간의 미래</h3>
      <p>노동과 분배, 통치, 결핍, 종교, 기술 발전의 목적, 그리고 한국 산업의 미래까지 질문을 확장하는 대화 연재.</p>
      <span class="series-card-more">시리즈 열기 →</span>
    </a>
  </div>
</section>

<section class="series-section">
  <h2>단독 글</h2>
  <div class="series-index series-index--flat">
    <a class="series-row" href="./standalone/2026-07-24-ai-engineer-worlds-fair-2026-agentic-engineering/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">AI Engineer World's Fair 2026, Agentic Engineering 세션에서 나온 이야기들</span><span class="series-date">2026.07.24</span></span>
        <span class="series-row-desc">여덟 개 세션을 통해 Harness, Skill, Agentic SDLC, Eval, Sandbox의 흐름을 짚는다.</span>
      </span>
    </a>
    <a class="series-row" href="./standalone/2026-07-21-human-ai-judgment/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">이해하지 못하는 결정을 승인한다는 것</span><span class="series-date">2026.07.21</span></span>
        <span class="series-row-desc">AI가 판단하고 인간이 승인할 때, 검증 능력과 책임은 누구에게 남는지 묻다.</span>
      </span>
    </a>
    <a class="series-row" href="./standalone/2026-05-07-controlling-ai-coding-agents/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">AI 코딩 에이전트를 제대로 통제하는 방법</span><span class="series-date">2026.05.07</span></span>
        <span class="series-row-desc">신뢰하되 통제하는 실무 원칙 — 에이전트를 안전하게 다루는 지침.</span>
      </span>
    </a>
    <a class="series-row" href="./standalone/2026-04-28-latency-numbers-every-programmer-should-know/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">Latency Numbers Every Programmer Should Know 정리</span><span class="series-date">2026.04.28</span></span>
        <span class="series-row-desc">Jeff Dean의 지연 숫자를 한국어로 정리하고 최신 감각으로 되짚은 참고 자료.</span>
      </span>
    </a>
    <a class="series-row" href="./standalone/2026-04-28-ai-slop-copy-paste-risk/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">AI-slop은 새로운 문제가 아니다. 더 위험해진 복붙 문제다</span><span class="series-date">2026.04.28</span></span>
        <span class="series-row-desc">더 빠르고 그럴듯하게 확장된 복붙 문제, 그 위험과 대응.</span>
      </span>
    </a>
  </div>
</section>

<section class="series-section">
  <h2>원본</h2>
  <p class="series-origin">Velog · <a href="https://velog.io/@hiha12ha/posts">@hiha12ha/posts</a><br>RSS · <a href="https://v2.velog.io/rss/@hiha12ha">v2.velog.io/rss/@hiha12ha</a></p>
</section>
