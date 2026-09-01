---
title: "Agent SDD 실무 개발"
nav_order: 2
has_children: true
has_toc: false
permalink: /series/agent-sdd/
---

<div class="series-hero">
  <div class="series-eyebrow"><span>Series · 연재</span><span>총 9편</span></div>
  <h1>Agent SDD 실무 개발</h1>
  <p>AI Agent를 실무 개발에 안정적으로 적용하기 위한 연재입니다. 작업의 위험도에 맞춰 절차를 조절하는 방법부터 명세 기반 구현 흐름, 백로그를 이용한 세션 연속성, 개발 완료 후 문서 정리, 도메인 문서로 Agent의 탐색을 줄이는 실험, SDD 문서 뼈대를 skill로 고정하려다 마주친 지시-예시 충돌, PR에서 business 문서를 안전하게 갱신하는 절차, Skill Eval을 이용한 검증, 멀티 Agent 작업 격리와 검증 Gate 운영까지 다룹니다.</p>
  <p>시리즈에서 사용한 규칙과 Skill은 <a href="https://github.com/seok-jun/agent-sdd-kit">agent-sdd-kit</a>으로 공개했습니다.</p>
</div>

<div class="series-index">
  <a class="series-row" href="./001-ai-task-grading/">
    <span class="series-num">01</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">AI한테 일을 시킬 때, 다 똑같이 다루면 안 되더라</span><span class="series-date">2026.06.25</span></span>
      <span class="series-row-desc">규모·리스크로 작업을 다섯 등급으로 나눠 프로세스의 무게를 조절하다.</span>
    </span>
  </a>
  <a class="series-row" href="./002-agent-sdd-stabilizing-ai-development/">
    <span class="series-num">02</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">Agent에게 바로 개발시키지 않기</span><span class="series-date">2026.06.25</span></span>
      <span class="series-row-desc">명세·영향분석·검증 기준을 단계별 산출물로 만든 뒤 구현해 개발을 안정화하다.</span>
    </span>
  </a>
  <a class="series-row" href="./003-agent-backlog-session-continuity/">
    <span class="series-num">03</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">죽은 Agent 세션, 백로그로 살리는 법</span><span class="series-date">2026.07.02</span></span>
      <span class="series-row-desc">끊긴 세션을 백로그의 보류 결정·후속 작업으로 되살려 연속성을 확보하다.</span>
    </span>
  </a>
  <a class="series-row" href="./004-sdd-artifacts-keep-or-delete/">
    <span class="series-num">04</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">개발이 끝난 SDD 문서, 지울 것과 도메인에 남길 것</span><span class="series-date">2026.07.05</span></span>
      <span class="series-row-desc">병합 후 작업 폴더에 남기지 않을 산출물과 도메인 옆 business 문서로 승격할 것을 가른다.</span>
    </span>
  </a>
  <a class="series-row" href="./005-docs-cut-agent-wandering-not-tokens/">
    <span class="series-num">05</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">문서는 토큰 청구서를 크게 줄이지 않는다 — 대신 Agent가 헤매는 시간을 줄인다</span><span class="series-date">2026.07.06</span></span>
      <span class="series-row-desc">코드에 경계가 없을 때 business 문서로 경계를 만들고, 설계 단계까지 Agent의 탐색 왕복이 줄어드는지 n=1로 측정한 기록.</span>
    </span>
  </a>
  <a class="series-row" href="./006-example-stronger-than-instruction/">
    <span class="series-num">06</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">예시가 지시보다 강할 때가 있다</span><span class="series-date">2026.07.09</span></span>
      <span class="series-row-desc">SDD 문서 뼈대를 skill로 고정하려다, skill 안의 지시 충돌과 그대로 복사되는 예시 값을 v1.x → v2 → v2-fix로 좁혀간 기록.</span>
    </span>
  </a>
  <a class="series-row" href="./007-pr-business-docs-skill/">
    <span class="series-num">07</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">business 문서를 PR에서 갱신해보기</span><span class="series-date">2026.07.14</span></span>
      <span class="series-row-desc">diff와 호출 관계로 갱신 대상을 찾고, 코드 근거 확인과 저장 전 검증으로 business 문서를 안전하게 최신화한 첫 실행 기록.</span>
    </span>
  </a>
  <a class="series-row" href="./008-skill-eval-validation/">
    <span class="series-num">08</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">Skill 검증을 위한 Eval, 직접 돌려보았다</span><span class="series-date">2026.07.22</span></span>
      <span class="series-row-desc">Trigger·Non-trigger·Procedure 케이스를 직접 실행하며 베이스라인, 검증 비용, 실행형 테스트의 부작용을 확인하다.</span>
    </span>
  </a>
  <a class="series-row" href="./009-adaptive-agentic-sdd/">
    <span class="series-num">09</span>
    <span class="series-body">
      <span class="series-row-head"><span class="series-row-title">멀티 Agent 개발을 실제로 운영해보고 정리한 것들</span><span class="series-date">2026.09.01</span></span>
      <span class="series-row-desc">멀티 Agent 병렬 개발과 작업 격리, 위험도별 검증 Gate를 실제 운영하며 바뀐 기준을 정리한 기록.</span>
    </span>
  </a>
</div>

<p class="series-note">1편에서 작업 등급을 정하고, 2편에서 Agent 작업 절차를 구성한 뒤, 3편에서 세션이 끊겨도 작업을 이어가는 방법으로, 4편에서 개발이 끝난 뒤 문서를 정리하는 방법으로, 5편에서 도메인 문서가 Agent의 탐색을 실제로 줄이는지 측정하고, 6편에서 그 문서 뼈대를 skill로 고정할 때 생기는 지시-예시 충돌을 살펴봅니다. 7편에서는 PR의 실제 구현을 기준으로 business 문서를 안전하게 갱신하는 절차까지 확장하고, 8편에서는 Skill의 트리거와 실행 절차를 Eval로 검증합니다. 9편에서는 멀티 Agent를 실제 운영하며 작업 격리, 제한된 탐색, 위험도별 검증 Gate로 확장합니다. 순서대로 읽기를 권합니다.</p>
