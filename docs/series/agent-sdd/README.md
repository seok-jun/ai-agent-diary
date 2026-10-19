---
title: "Agent SDD 개발 일지"
nav_order: 2
has_children: true
has_toc: false
permalink: /series/agent-sdd/
description: "AI 코딩 에이전트를 회사 일과 개인 프로젝트에 붙이면서, 모델 바깥의 절차·검사·규칙인 하네스를 직접 만들고 다시 재 본 연재."
last_modified_at: 2026-10-19
---

{%- assign series_posts = site.pages | where: "parent", page.title | sort: "nav_order" -%}
{%- assign last_post = series_posts | last -%}

<div class="series-hero">
  <div class="series-eyebrow"><span>Series · 연재</span><span>총 {{ series_posts.size }}편</span></div>
  <h1>Agent SDD 개발 일지</h1>
  <p>AI 코딩 에이전트를 회사 일과 개인 프로젝트에 붙이면서 남긴 기록입니다. 처음에는 절차를 하나씩 더해 가며 Agent를 붙잡았고, 모델이 좋아진 뒤에는 그 절차가 아직 필요한지 다시 재고 있습니다. 모델 바깥에서 Agent를 붙잡는 이런 절차와 검사, 규칙을 요즘은 하네스(harness)라고 부르는데, 이 연재는 그 하네스를 직접 만들고 다시 재 본 기록이기도 합니다. 처음이라면 <a href="./001-ai-task-grading/">1편</a>부터, 최근 이야기는 <a href="./012-outgrown-guardrails/">12편</a>부터 읽으면 됩니다. 글에 나오는 이름이 헷갈리면 아래 <a href="#glossary">자주 나오는 이름</a>을 먼저 보세요.</p>
  <p>시리즈에서 사용한 규칙과 Skill은 <a href="https://github.com/seok-jun/agent-sdd-kit">agent-sdd-kit</a>으로, 워크플로 전체는 <a href="https://github.com/seok-jun/adaptive-agentic-sdd">adaptive-agentic-sdd</a>로 공개했습니다.</p>
</div>

{% assign group_posts = series_posts | where_exp: "p", "p.nav_order >= 1 and p.nav_order <= 4" %}
<section class="series-group-section">
  <div class="series-section-heading">
    <h2>기초</h2>
    <span>1~4편</span>
  </div>
  <p class="series-group-intro">작업을 위험도로 나누고, 명세를 먼저 쓰고, 백로그로 세션을 잇고, 끝난 문서를 정리하는 기본 흐름.</p>
  <div class="series-index">
    {%- for post in group_posts %}
    {% include post-row.html post=post number=true %}
    {%- endfor %}
  </div>
</section>

{% assign group_posts = series_posts | where_exp: "p", "p.nav_order >= 5 and p.nav_order <= 8" %}
<section class="series-group-section">
  <div class="series-section-heading">
    <h2>문서와 Skill</h2>
    <span>5~8편</span>
  </div>
  <p class="series-group-intro">도메인 문서와 Skill로 Agent가 헤매는 시간을 줄이고, PR에서 문서를 갱신하고, Eval로 Skill을 검증한 기록.</p>
  <div class="series-index">
    {%- for post in group_posts %}
    {% include post-row.html post=post number=true %}
    {%- endfor %}
  </div>
</section>

{% assign group_posts = series_posts | where_exp: "p", "p.nav_order >= 9" %}
<section class="series-group-section">
  <div class="series-section-heading">
    <h2>방법론과 재검증</h2>
    <span>9~{{ last_post.nav_order }}편</span>
  </div>
  <p class="series-group-intro">멀티 Agent 운영을 방법론으로 묶어 공유하고, 실무에 다시 적용하고, 모델이 좋아진 뒤 하네스를 다시 재본 과정.</p>
  <div class="series-index">
    {%- for post in group_posts %}
    {% include post-row.html post=post number=true %}
    {%- endfor %}
  </div>
</section>

<section class="series-group-section" id="glossary">
  <div class="series-section-heading">
    <h2>자주 나오는 이름</h2>
    <span>12편부터 늘어난 이름들</span>
  </div>
  <div class="table-wrapper">
    <table>
      <thead>
        <tr><th>이름</th><th>뜻</th><th>처음 나온 곳</th></tr>
      </thead>
      <tbody>
        <tr><td>하네스(harness)</td><td>모델 바깥에서 Agent를 붙잡는 절차·검사·규칙 전체. 이 연재에서 만든 방법론이 여기에 해당합니다.</td><td><a href="./012-outgrown-guardrails/">12편</a></td></tr>
        <tr><td>하네스의 구성 요소</td><td>명세, 현행 분석, 변경 계획, 백로그, 독립 리뷰 같은 개별 절차. 통제와 보조 절차를 구분해 필요성을 판단합니다.</td><td><a href="./012-outgrown-guardrails/">12편</a></td></tr>
        <tr><td>통제 (헬멧)</td><td>권한, 수정 범위, 승인, 꼭 돌려야 하는 검증. 작업의 위험에 맞춰 거는 것이라 모델이 좋아져도 그대로 둡니다.</td><td><a href="./012-outgrown-guardrails/">12편</a></td></tr>
        <tr><td>보조 절차 (보조바퀴)</td><td>모델의 약점을 메우려고 넣은 절차. 지금도 필요한지 다시 재 보는 대상입니다.</td><td><a href="./013-removing-one-guardrail/">13편</a></td></tr>
        <tr><td>앱 저장소</td><td>실제로 만들고 있는 안드로이드 앱. 17편에서는 "실무 프로젝트"라고 불렀습니다.</td><td><a href="./018-connecting-methodology-from-outside/">18편</a></td></tr>
        <tr><td>연구 저장소</td><td>차세대 규칙을 설계하고 실험하는 비공개 저장소. 13~16편의 실험도 여기서 했습니다. 어떤 프로젝트도 직접 읽지 않습니다.</td><td><a href="./018-connecting-methodology-from-outside/">18편</a></td></tr>
        <tr><td>앱 전용 규칙 저장소</td><td>앱이 실제로 쓰는 Agent 작업 규칙을 앱 밖으로 떼어 따로 담은 저장소.</td><td><a href="./018-connecting-methodology-from-outside/">18편</a></td></tr>
        <tr><td>agent-sdd-kit</td><td>1~7편에서 쓴 작업 등급 규칙과 Skill 두 개를 공개용으로 정리한 저장소.</td><td><a href="./007-pr-business-docs-skill/">7편</a></td></tr>
        <tr><td>adaptive-agentic-sdd</td><td>멀티 Agent 운영 워크플로 전체를 방법론으로 묶어 공개한 저장소. 21편의 v1 preview도 여기에 냈습니다.</td><td><a href="./009-adaptive-agentic-sdd/">9편</a></td></tr>
      </tbody>
    </table>
  </div>
</section>
