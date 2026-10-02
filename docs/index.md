---
title: "AI Agent Diary"
layout: home
nav_order: 1
permalink: /
---

{% assign dated_pages = site.pages | where_exp: "item", "item.date != nil" | where_exp: "item", "item.parent != 'AI에게 물어본 인간의 미래'" | sort: "date" | reverse %}
{% assign recent_pages = dated_pages | slice: 0, 4 %}
{% assign latest_page = recent_pages | first %}

<div class="series-hero">
  <div class="series-eyebrow"><span>seok jun의 개인 기술 블로그</span><span>최근 업데이트 {{ latest_page.date | date: "%Y.%m.%d" }} · 글 {{ dated_pages.size }}편</span></div>
  <h1 class="series-hero-title"><img src="{{ '/assets/images/brand/wordmark.svg' | relative_url }}" alt="AI Agent Diary" width="640" height="150"></h1>
  <p>AI 코딩 에이전트를 실무에 붙이면서 남긴 기록입니다. 개발 방법론, 검증, 문서화, 그리고 그 과정에서 마주친 판단들.</p>
  <p class="series-hero-about"><a href="./about/">글쓴이 소개 →</a></p>
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
          <span class="series-row-category">{{ article.parent }}</span>
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
    <div class="series-card series-card--grouped">
      <span class="series-card-kicker">Series · 14편</span>
      <h3><a href="./series/agent-sdd/">Agent SDD 실무 개발</a></h3>
      <p>AI Agent를 실무 개발에 붙이면서 겪은 일을 쓴 순서대로 정리한 연재입니다. 처음이라면 아래 세 묶음의 첫 글부터 읽으면 됩니다.</p>
      <ol class="series-groups">
        <li>
          <span class="series-group-head"><span class="series-group-range">1~4편</span><strong>기초</strong></span>
          <span class="series-group-desc">작업을 위험도로 나누고, 명세를 먼저 쓰고, 백로그로 세션을 잇고, 끝난 문서를 정리하는 기본 흐름.</span>
          <a class="series-group-link" href="./series/agent-sdd/001-ai-task-grading/">여기부터 →</a>
        </li>
        <li>
          <span class="series-group-head"><span class="series-group-range">5~8편</span><strong>문서와 Skill</strong></span>
          <span class="series-group-desc">도메인 문서와 Skill로 Agent가 헤매는 시간을 줄이고, PR에서 문서를 갱신하고, Eval로 Skill을 검증한 기록.</span>
          <a class="series-group-link" href="./series/agent-sdd/005-docs-cut-agent-wandering-not-tokens/">여기부터 →</a>
        </li>
        <li>
          <span class="series-group-head"><span class="series-group-range">9~14편</span><strong>방법론과 재검증</strong></span>
          <span class="series-group-desc">멀티 Agent 운영을 방법론으로 묶어 공유하고, 실무에 다시 적용하고, 모델이 좋아진 뒤 가드레일을 다시 재본 과정.</span>
          <a class="series-group-link" href="./series/agent-sdd/009-adaptive-agentic-sdd/">여기부터 →</a>
        </li>
      </ol>
      <a class="series-card-more" href="./series/agent-sdd/">시리즈 전체 보기 →</a>
    </div>
  </div>
</section>

<section class="series-section">
  <h2>단독 글</h2>
  <div class="series-index series-index--flat">
    <a class="series-row" href="./standalone/2026-10-02-why-ai-agents-need-evals/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">감으로는 고칠 수 없다 — AI 에이전트에 Eval이 필요한 이유</span><span class="series-date">2026.10.02</span></span>
        <span class="series-row-desc">Anthropic의 evals 가이드를 바탕으로, AI 에이전트에 왜 시험지가 필요한지를 비유와 도식, 표로 풀어 정리.</span>
      </span>
    </a>
    <a class="series-row" href="./standalone/2026-10-02-ai-native-sdlc-playbook/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">코드는 더 이상 병목이 아니다 — AI-Native SDLC 쉽게 읽기</span><span class="series-date">2026.10.02</span></span>
        <span class="series-row-desc">Anthropic의 AI-native SDLC 플레이북을 도식과 표로 풀어, 여섯 단계가 하나의 고리가 되는 방식을 정리.</span>
      </span>
    </a>
    <a class="series-row" href="./standalone/2026-07-28-agent-scaffolding-history/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">흡수된 것들과 흡수되지 않은 하나 — 에이전트 도구사 3년</span><span class="series-date">2026.07.28</span></span>
        <span class="series-row-desc">모델의 약점을 보정하던 구조물이 어떻게 흡수되고 걷혔는지, 끝까지 남는 검증층은 무엇인지.</span>
      </span>
    </a>
    <a class="series-row" href="./standalone/2026-07-24-agent-skill-getting-started/">
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">매번 붙여넣던 지시를 폴더 하나로 — Agent Skill 입문</span><span class="series-date">2026.07.24</span></span>
        <span class="series-row-desc">Skill이 무엇이고 왜 그렇게 생겼는지, 처음 하나 만들어보는 것까지.</span>
      </span>
    </a>
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
  <h2>Velog에도 게시</h2>
  <p class="series-origin">이 사이트가 정본이며, 같은 글을 Velog에도 게시합니다.<br>Velog · <a href="https://velog.io/@hiha12ha/posts">@hiha12ha/posts</a><br>RSS · <a href="https://v2.velog.io/rss/@hiha12ha">v2.velog.io/rss/@hiha12ha</a></p>
</section>
