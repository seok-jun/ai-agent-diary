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
  <p id="activity-status" class="ad-status" role="status" aria-live="polite">활동 기록을 불러오는 중입니다.</p>
  <div id="activity-content" hidden>
    <section class="ad-section" aria-labelledby="activity-overview-heading">
      <h2 id="activity-overview-heading" class="ad-heading">누적 사용량</h2>
      <div class="ad-sources">
        <article class="ad-source ad-source--codex" aria-labelledby="activity-codex-name">
          <header class="ad-source-head"><span class="ad-key ad-key--codex" aria-hidden="true"></span><h3 id="activity-codex-name">Codex</h3><span id="activity-codex-asof" class="ad-muted"></span></header>
          <strong id="activity-codex-total" class="ad-total">—</strong>
          <p class="ad-muted">프로필 전체 기록 · 캐시 토큰 포함</p>
          <dl id="activity-codex-facts" class="ad-facts"></dl>
        </article>
        <article class="ad-source ad-source--claude" aria-labelledby="activity-claude-name">
          <header class="ad-source-head"><span class="ad-key ad-key--claude" aria-hidden="true"></span><h3 id="activity-claude-name">Claude Code</h3><span id="activity-claude-asof" class="ad-muted"></span></header>
          <strong id="activity-claude-total" class="ad-total">—</strong>
          <p id="activity-claude-range" class="ad-muted">개인 개발용 기록 · 캐시 토큰 포함</p>
          <dl id="activity-claude-facts" class="ad-facts"></dl>
        </article>
      </div>
    </section>
    <div class="ad-toolbar" role="group" aria-label="기간 선택">
      <div class="ad-segmented" role="radiogroup" aria-label="보기">
        <label><input type="radio" name="activity-period" value="day"><span>일별</span></label>
        <label><input type="radio" name="activity-period" value="month" checked><span>월별</span></label>
        <label><input type="radio" name="activity-period" value="all"><span>전체</span></label>
      </div>
      <label id="activity-day-label" class="ad-field" hidden><span class="ad-visually-hidden">날짜</span><input id="activity-day" type="date"></label>
      <label id="activity-month-label" class="ad-field"><span class="ad-visually-hidden">월</span><input id="activity-month" type="month"></label>
      <p id="activity-period-note" class="ad-muted ad-toolbar-note"></p>
    </div>
    <section class="ad-section" aria-labelledby="activity-tokens-heading">
      <h2 id="activity-tokens-heading" class="ad-heading">AI 토큰</h2>
      <p class="ad-muted ad-section-note">두 도구 모두 캐시 토큰을 포함한 값입니다. 긴 대화에서 이전 맥락을 다시 읽는 캐시 토큰이 대부분을 차지합니다.</p>
      <div id="activity-token-kpis" class="ad-kpis"></div>
      <figure class="ad-chart-card">
        <figcaption class="ad-chart-head"><span id="activity-token-chart-title">일별 토큰</span><span class="ad-legend"><span><i class="ad-key ad-key--codex"></i>Codex</span><span><i class="ad-key ad-key--claude"></i>Claude Code</span></span></figcaption>
        <div id="activity-token-chart" class="ad-chart"></div>
      </figure>
    </section>
    <section class="ad-section" aria-labelledby="activity-github-heading">
      <h2 id="activity-github-heading" class="ad-heading">GitHub 개발 활동</h2>
      <div id="activity-github-kpis" class="ad-kpis"></div>
      <figure class="ad-chart-card">
        <figcaption class="ad-chart-head"><span id="activity-github-chart-title">일별 병합·완료</span><span class="ad-legend"><span><i class="ad-key ad-key--prs"></i>병합 PR</span><span><i class="ad-key ad-key--issues"></i>완료 이슈</span></span></figcaption>
        <div id="activity-github-chart" class="ad-chart"></div>
      </figure>
    </section>
    <section class="ad-section" aria-labelledby="activity-rates-heading">
      <h2 id="activity-rates-heading" class="ad-heading">토큰 100만 개당 병합·완료</h2>
      <div class="ad-table-wrap" tabindex="0" role="region" aria-label="토큰 100만 개당 병합·완료 표">
        <table class="ad-table ad-table--rates">
          <thead><tr><th scope="col">토큰 기준</th><th scope="col">병합 PR</th><th scope="col">완료 이슈</th><th scope="col">비교한 기간</th></tr></thead>
          <tbody id="activity-rates"></tbody>
        </table>
      </div>
      <p class="ad-muted">토큰 기록과 GitHub 기록이 함께 있는 날짜만 비교합니다. 작업 규모·품질이나 AI 기여도를 평가하지 않으며, 토큰을 쓴 날과 병합·완료일에는 시차가 있을 수 있습니다.</p>
    </section>
    <section class="ad-section" aria-labelledby="activity-history-heading">
      <h2 id="activity-history-heading" class="ad-heading">활동 내역</h2>
      <div class="ad-table-wrap ad-table-wrap--history" tabindex="0" role="region" aria-label="활동 내역 표, 가로로 스크롤 가능">
        <table class="ad-table">
          <caption id="activity-table-caption" class="ad-muted">선택한 기간의 기록</caption>
          <thead>
            <tr><th scope="col" rowspan="2">기간</th><th scope="colgroup" colspan="2" class="ad-group">AI 토큰</th><th scope="colgroup" colspan="3" class="ad-group">GitHub</th></tr>
            <tr><th scope="col">Codex</th><th scope="col">Claude Code</th><th scope="col">커밋</th><th scope="col">병합 PR</th><th scope="col">완료 이슈</th></tr>
          </thead>
          <tbody id="activity-history"></tbody>
        </table>
      </div>
    </section>
  </div>
</div>

<noscript>이 대시보드는 JavaScript가 필요합니다. <a href="{{ '/assets/activity/data.json' | relative_url }}">공개 집계 JSON</a>에서도 숫자를 확인할 수 있습니다.</noscript>

## 기록을 읽는 방법

**Codex**

- 비공식 `codex-usage-analyzer`가 보고한 **Codex 프로필 누적 사용량**입니다. 요금제 잔여 한도, 청구 금액, API 사용량 또는 생산성을 뜻하지 않습니다. **캐시 토큰을 포함**하며 Codex 계정 사용량은 캐시를 따로 구분해 제공하지 않습니다. 일별 경계는 도구가 제공한 날짜를 그대로 사용합니다.
- 연속 활동과 최장 작업은 마지막 수집 시점의 프로필 수치입니다. 페이지를 열었다고 자동으로 갱신되지 않습니다. 초기 기록은 사용자가 제공한 2026년 10월 16일 스냅샷입니다.

**Claude Code**

- **개인 개발용 Claude Code 대화 기록**에 남은 응답별 사용량(입력·출력·캐시 생성·캐시 읽기)을 한국 시간 날짜로 합산한 값으로, **캐시 토큰을 포함**합니다. 같은 응답이 여러 기록에 반복되면 한 번만 셉니다.
- Claude Code는 오래된 기록을 지우므로, 첫 수집 전에 지워진 기록은 포함되지 않고 이미 공개한 날짜의 값은 줄이지 않습니다. claude.ai 채팅, 개인 개발용 외 기록, 청구 금액은 포함하지 않습니다.

**GitHub**

- 커밋은 집계용 키로 접근 가능한 저장소의 **기본 브랜치에 있는 본인 작성 커밋**을 커밋 반영 시각(committer date), 병합 PR은 본인 작성 PR을 병합 시각, 완료 이슈는 본인 작성 이슈 중 `completed` 상태를 종료 시각 기준으로 집계합니다. 날짜 경계는 한국 시간입니다.
- 누적은 **Codex 일별 기록의 시작일부터 수집한 구간 내 누적**입니다. 집계용 키로 접근 가능한 저장소만 반영하므로 GitHub 전체 활동과 다를 수 있습니다. AI가 작성한 코드인지 판별하지 않습니다.

**공통**

- 수집 전·구간 밖은 ‘—’(미수집)로 표시하며 0과 구분합니다. 일부 날짜만 수집된 기간에는 ‘일부 수집’을 표시합니다.
- 100만 토큰당 건수는 고른 기간 중 **그 토큰 기록과 GitHub가 함께 수집된 날짜**만 사용합니다. 합계는 Codex·Claude Code·GitHub가 모두 수집된 날짜만 씁니다. 월별·전체 비율은 일별 비율의 평균이 아니라 그 기간의 총건수를 총토큰으로 나눠 계산합니다. 사용 토큰이 0이면 비율을 표시하지 않습니다.
- 비공개 저장소 이름·경로·제목·커밋 메시지는 공개하지 않습니다. 방문자의 브라우저는 공개 JSON만 읽으며 비공개 API나 인증값을 사용하지 않습니다.

<script src="{{ '/assets/activity/dashboard.js' | relative_url }}" defer></script>
