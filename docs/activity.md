---
title: "AI 개발 활동"
parent: null
nav_order: 4.5
permalink: /activity/
description: "Codex·Claude Code 토큰 사용량과 GitHub 개발 활동을 일별·월별로 기록합니다."
---

# AI 개발 활동

Codex·Claude Code와 함께 쌓은 사용 기록, 그리고 GitHub에 남긴 개발 활동입니다. 공개·비공개 저장소의 활동은 합산한 숫자로만 표시합니다.

<div id="activity-dashboard" class="activity-dashboard" data-source="{{ '/assets/activity/data.json' | relative_url }}">
  <p id="activity-status" role="status" aria-live="polite">활동 기록을 불러오는 중입니다.</p>
  <div id="activity-content" hidden>
    <div class="activity-heroes">
      <section class="activity-hero" aria-label="Codex 누적 사용량">
        <span class="activity-eyebrow">CODEX · PROFILE ACTIVITY</span>
        <h2 id="activity-total-heading">지금까지 사용한 토큰</h2>
        <strong id="activity-lifetime" class="activity-total">—</strong>
        <p id="activity-codex-date"></p>
      </section>
      <section class="activity-hero activity-hero--claude" aria-label="Claude Code 수집 사용량">
        <span class="activity-eyebrow">CLAUDE CODE · LOCAL HISTORY</span>
        <h2>수집한 토큰</h2>
        <strong id="activity-claude-total" class="activity-total">—</strong>
        <p id="activity-claude-date"></p>
      </section>
    </div>
    <div class="activity-records" id="activity-records"></div>
    <section aria-labelledby="activity-period-heading">
      <h2 id="activity-period-heading">기간별 기록</h2>
      <div class="activity-controls">
        <label>보기 <select id="activity-period"><option value="day">일별</option><option value="month" selected>월별</option><option value="all">누적</option></select></label>
        <label id="activity-day-label" hidden>날짜 <input id="activity-day" type="date"></label>
        <label id="activity-month-label">월 <input id="activity-month" type="month"></label>
        <label>비교 토큰 <select id="activity-source"><option value="codex" selected>Codex</option><option value="claude">Claude Code</option><option value="total">Codex + Claude Code</option></select></label>
      </div>
      <p id="activity-period-note" class="activity-muted"></p>
      <div id="activity-metrics" class="activity-metrics"></div>
    </section>
    <section aria-labelledby="activity-chart-heading">
      <h2 id="activity-chart-heading">토큰과 개발 활동 추이</h2>
      <p id="activity-chart-note" class="activity-muted"></p>
      <div id="activity-chart" class="activity-chart"></div>
    </section>
    <section aria-labelledby="activity-comparison-heading">
      <h2 id="activity-comparison-heading">토큰 사용량 대비 병합·완료</h2>
      <p id="activity-comparison-note" class="activity-muted"></p>
      <div id="activity-rates" class="activity-metrics"></div>
      <p class="activity-muted">건수와 비율은 작업 규모·품질이나 AI 기여도를 평가하지 않습니다. 토큰을 사용한 날과 PR 병합·이슈 완료일에는 시차가 있을 수 있습니다.</p>
    </section>
    <section aria-labelledby="activity-history-heading">
      <h2 id="activity-history-heading">활동 내역</h2>
      <div class="activity-table-wrap" tabindex="0" role="region" aria-label="활동 내역 표, 가로로 스크롤 가능">
        <table class="activity-table">
          <caption id="activity-table-caption">선택한 기간의 기록</caption>
          <thead><tr><th scope="col">기간</th><th scope="col">Codex 토큰</th><th scope="col">Claude 토큰</th><th scope="col">커밋</th><th scope="col">병합 PR</th><th scope="col">완료 이슈</th></tr></thead>
          <tbody id="activity-history"></tbody>
        </table>
      </div>
    </section>
  </div>
</div>

<noscript>이 대시보드는 JavaScript가 필요합니다. <a href="{{ '/assets/activity/data.json' | relative_url }}">공개 집계 JSON</a>에서도 숫자를 확인할 수 있습니다.</noscript>

## 기록을 읽는 방법

- 토큰은 비공식 `codex-usage-analyzer`가 보고한 **Codex 프로필 누적 사용량**입니다. 요금제 잔여 한도, 청구 금액, API 사용량 또는 생산성을 뜻하지 않습니다. 일별 경계는 도구가 제공한 날짜를 그대로 사용합니다.
- Claude 토큰은 이 PC의 **Claude Code 로컬 대화 기록**에 남은 응답별 사용량(입력·출력·캐시 생성·캐시 읽기)을 한국 시간 날짜로 합산한 값입니다. 같은 응답이 여러 기록에 반복되면 한 번만 셉니다. Claude Code는 오래된 기록을 지우므로, 첫 수집 전에 지워진 기록은 포함되지 않고 이미 공개한 날짜의 값은 줄이지 않습니다. claude.ai 채팅, 다른 PC, 청구 금액은 포함하지 않습니다.
- 연속 활동과 최장 작업은 마지막 수집 시점의 프로필 수치입니다. 페이지를 열었다고 자동으로 갱신되지 않습니다. 초기 기록은 사용자가 제공한 2026년 10월 16일 스냅샷입니다.
- GitHub 커밋은 집계용 키로 접근 가능한 저장소의 **기본 브랜치에 있는 본인 작성 커밋**을 커밋 반영 시각(committer date), 병합 PR은 본인 작성 PR을 병합 시각, 완료 이슈는 본인 작성 이슈 중 `completed` 상태를 종료 시각 기준으로 집계합니다. GitHub 날짜 경계는 한국 시간입니다.
- GitHub 누적은 **Codex 일별 기록의 시작일부터 수집한 구간 내 누적**입니다. 수집 전·구간 밖은 ‘미수집’이며 0건과 구분합니다. 일부만 포함된 월은 ‘일부 수집’으로 표시합니다. 집계용 키로 접근 가능한 저장소만 반영하므로 GitHub 전체 활동과 다를 수 있습니다. AI가 작성한 코드인지 판별하지 않습니다.
- 추이 비교와 100만 토큰당 건수는 ‘비교 토큰’에서 고른 Codex·Claude Code·합계 중 하나를 기준으로, 선택한 기간 중 **그 토큰 기록과 GitHub가 함께 수집된 날짜**만 사용합니다. 합계는 Codex·Claude Code·GitHub가 모두 수집된 날짜만 씁니다. 월별·누적 비율은 일별 비율의 평균이 아니라 공통 기간의 총건수를 총토큰으로 나눠 계산합니다. 사용 토큰이 0이면 비율을 표시하지 않습니다.
- 비공개 저장소 이름·경로·제목·커밋 메시지는 공개하지 않습니다. 방문자의 브라우저는 공개 JSON만 읽으며 비공개 API나 인증값을 사용하지 않습니다.

<script src="{{ '/assets/activity/dashboard.js' | relative_url }}" defer></script>
