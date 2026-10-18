---
title: "AI Agent Diary"
layout: home
nav_order: 1
permalink: /
---

{% assign dated_pages = site.pages | where_exp: "item", "item.date != nil" | where_exp: "item", "item.parent != 'AI에게 물어본 인간의 미래'" | sort: "date" | reverse %}
{% assign recent_pages = dated_pages | slice: 0, 4 %}
{% assign latest_page = recent_pages | first %}
{% assign series_posts = site.pages | where: "parent", "Agent SDD 개발 일지" | sort: "nav_order" %}
{% assign last_series_post = series_posts | last %}
{% assign standalone_posts = site.pages | where: "parent", "단독 글" | sort: "nav_order" %}

<div class="series-hero">
  <div class="series-eyebrow"><span>seok jun의 개인 기술 블로그</span><span>최근 업데이트 {{ latest_page.date | date: "%Y.%m.%d" }} · 글 {{ dated_pages.size }}편</span></div>
  <h1 class="series-hero-title"><img src="{{ '/assets/images/brand/wordmark.svg' | relative_url }}" alt="AI Agent Diary" width="640" height="150"></h1>
  <p>AI 코딩 에이전트를 회사 일과 개인 프로젝트에 붙이면서 남긴 기록입니다. 개발 방법론, 검증, 문서화, 그리고 그 과정에서 마주친 판단들.</p>
  <p id="home-activity" class="series-hero-stats" data-source="{{ '/assets/activity/data.json' | relative_url }}" hidden><span class="hs-label">최근 30일</span><span class="hs-values"><span>병합 PR <b data-ha="prs">—</b></span><span>완료 이슈 <b data-ha="issues">—</b></span><span>AI 토큰 <b data-ha="tokens">—</b> <small data-ha="tokens-note">캐시 포함</small></span><small data-ha="asof"></small></span></p>
  <p class="series-hero-about"><a href="./about/">글쓴이 소개 →</a> · <a href="./activity/">AI 개발 활동 →</a></p>
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

<script src="{{ '/assets/activity/home-summary.js' | relative_url }}" defer></script>

<section class="series-section">
  <h2>시리즈</h2>
  <div class="series-cards">
    <div class="series-card series-card--grouped">
      <span class="series-card-kicker">Series · {{ series_posts.size }}편</span>
      <h3><a href="./series/agent-sdd/">Agent SDD 개발 일지</a></h3>
      <p>AI Agent를 회사 일과 개인 프로젝트에 붙이면서 겪은 일을 쓴 순서대로 정리한 연재입니다. 처음이라면 아래 세 묶음의 첫 글부터 읽으면 됩니다.</p>
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
          <span class="series-group-head"><span class="series-group-range">9~{{ last_series_post.nav_order }}편</span><strong>방법론과 재검증</strong></span>
          <span class="series-group-desc">멀티 Agent 운영을 방법론으로 묶어 공유하고, 실무에 다시 적용하고, 모델이 좋아진 뒤 가드레일, 요즘 말로 하네스를 다시 재본 과정.</span>
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
    {%- for post in standalone_posts %}
    {% include post-row.html post=post %}
    {%- endfor %}
  </div>
</section>
