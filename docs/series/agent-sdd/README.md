---
title: "Agent SDD 개발 일지"
nav_order: 2
has_children: true
has_toc: false
permalink: /series/agent-sdd/
last_modified_at: 2026-10-16
---

<div class="series-hero">
  <div class="series-eyebrow"><span>Series · 연재</span><span>총 19편</span></div>
  <h1>Agent SDD 개발 일지</h1>
  <p>AI 코딩 에이전트를 회사 일과 개인 프로젝트에 붙이면서 남긴 기록입니다. 처음에는 절차를 하나씩 더해 가며 Agent를 붙잡았고, 모델이 좋아진 뒤에는 그 절차가 아직 필요한지 다시 재고 있습니다. 처음이라면 <a href="./001-ai-task-grading/">1편</a>부터, 최근 이야기는 <a href="./012-outgrown-guardrails/">12편</a>부터 읽으면 됩니다.</p>
  <p>시리즈에서 사용한 규칙과 Skill은 <a href="https://github.com/seok-jun/agent-sdd-kit">agent-sdd-kit</a>으로, 워크플로 전체는 <a href="https://github.com/seok-jun/adaptive-agentic-sdd">adaptive-agentic-sdd</a>로 공개했습니다.</p>
</div>

<section class="series-group-section">
  <div class="series-section-heading">
    <h2>기초</h2>
    <span>1~4편</span>
  </div>
  <p class="series-group-intro">작업을 위험도로 나누고, 명세를 먼저 쓰고, 백로그로 세션을 잇고, 끝난 문서를 정리하는 기본 흐름.</p>
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
  </div>
</section>

<section class="series-group-section">
  <div class="series-section-heading">
    <h2>문서와 Skill</h2>
    <span>5~8편</span>
  </div>
  <p class="series-group-intro">도메인 문서와 Skill로 Agent가 헤매는 시간을 줄이고, PR에서 문서를 갱신하고, Eval로 Skill을 검증한 기록.</p>
  <div class="series-index">
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
  </div>
</section>

<section class="series-group-section">
  <div class="series-section-heading">
    <h2>방법론과 재검증</h2>
    <span>9~19편</span>
  </div>
  <p class="series-group-intro">멀티 Agent 운영을 방법론으로 묶어 공유하고, 실무에 다시 적용하고, 모델이 좋아진 뒤 가드레일을 다시 재본 과정.</p>
  <div class="series-index">
    <a class="series-row" href="./009-adaptive-agentic-sdd/">
      <span class="series-num">09</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">멀티 Agent 개발을 실제로 운영해보고 정리한 것들</span><span class="series-date">2026.09.01</span></span>
        <span class="series-row-desc">멀티 Agent 병렬 개발과 작업 격리, 위험도별 검증 Gate를 실제 운영하며 바뀐 기준을 정리한 기록.</span>
      </span>
    </a>
    <a class="series-row" href="./010-agentics-sharing-methodology/">
      <span class="series-num">10</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">방법론을 강요하지 않고 공유하는 방법</span><span class="series-date">2026.09.13</span></span>
        <span class="series-row-desc">모두가 지켜야 할 공통 규칙과 개발자가 선택하는 방법론을 가르고, .agentics로 연결 정보만 프로젝트에 남기는 구상.</span>
      </span>
    </a>
    <a class="series-row" href="./011-adaptive-sdd-work-project/">
      <span class="series-num">11</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">Adaptive SDD를 실무 프로젝트에 다시 적용하면서 손본 것들</span><span class="series-date">2026.09.21</span></span>
        <span class="series-row-desc">실무에 다시 적용하며 리뷰 요청과 반환 형식, 스냅샷 기준, 사람이 실행하는 검증 문서를 다듬은 기록.</span>
      </span>
    </a>
    <a class="series-row" href="./012-outgrown-guardrails/">
      <span class="series-num">12</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">모델은 좋아졌는데 가드레일은 그대로였다</span><span class="series-date">2026.10.02</span></span>
        <span class="series-row-desc">프론티어 모델을 쓰며 기존 가드레일이 걸림돌이 된 건 아닌지 의심하고, 걷어내기 전에 먼저 재보기로 한 이유.</span>
      </span>
    </a>
    <a class="series-row" href="./013-removing-one-guardrail/">
      <span class="series-num">13</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">가드레일 하나만 빼고 돌려봤다</span><span class="series-date">2026.10.02</span></span>
        <span class="series-row-desc">보조 절차 하나만 넣고 빼는 비교를 네 번 돌리고, 세 번 통과에도 판정을 보류한 기록.</span>
      </span>
    </a>
    <a class="series-row" href="./014-isolation-stopped-the-experiment/">
      <span class="series-num">14</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">실험을 멈춘 건 모델이 아니었다</span><span class="series-date">2026.10.02</span></span>
        <span class="series-row-desc">가드레일 비교 실험을 두 번 멈춘 것이 모델이 아니라 격리였던 이유와, 멈춘 뒤에 지킨 것.</span>
      </span>
    </a>
    <a class="series-row" href="./015-rebuilding-experiment-environment/">
      <span class="series-num">15</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">다시 실험하려고 실험장부터 만들었다</span><span class="series-date">2026.10.06</span></span>
        <span class="series-row-desc">실행마다 새 환경을 만들고 푸는 곳과 채점하는 곳을 나눈 실험장과, 끝까지 간 두 쌍에서 확인한 것.</span>
      </span>
    </a>
    <a class="series-row" href="./016-rechecking-the-verdict/">
      <span class="series-num">16</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">열세 번 돌리고, 판정을 다시 봤다</span><span class="series-date">2026.10.13</span></span>
        <span class="series-row-desc">아직 안 쓴 과제로 한 쌍을 더 돌려본 결과와, 15편 진단 과제의 판정을 검사별로 다시 본 이야기.</span>
      </span>
    </a>
    <a class="series-row" href="./017-counting-what-machines-can-check/">
      <span class="series-num">17</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">규칙을 기계에 넘기려고 세어 봤다</span><span class="series-date">2026.10.13</span></span>
        <span class="series-row-desc">규칙 370줄 중 온전히 판정 가능한 건 16줄이었고, 사고 기록에서 가장 많은 유형은 애초에 기계로 넘길 수 없는 것이었다.</span>
      </span>
    </a>
    <a class="series-row" href="./018-connecting-methodology-from-outside/">
      <span class="series-num">18</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">드디어 방법론 분리 진행</span><span class="series-date">2026.10.16</span></span>
        <span class="series-row-desc">버전만 적어 두는 연결을 만들었지만 앱은 그 길을 쓰지 않았다. 먼저 이어 본 시험 연결을 하나씩 끊어 내며 다시 분리한 과정.</span>
      </span>
    </a>
    <a class="series-row" href="./019-letting-agents-improve-the-method/">
      <span class="series-num">19</span>
      <span class="series-body">
        <span class="series-row-head"><span class="series-row-title">Agent 방법론 자기개선 과연 잘 될까?</span><span class="series-date">2026.10.16</span></span>
        <span class="series-row-desc">관측으로 방법론을 고치는 한 바퀴, 손으로 먼저 해 본 점검, 실제 15회 결과, 그리고 이틀 만에 뺀 서명 승인.</span>
      </span>
    </a>
  </div>
</section>
