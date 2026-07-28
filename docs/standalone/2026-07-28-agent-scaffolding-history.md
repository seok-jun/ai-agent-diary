---
title: "흡수된 것들과 흡수되지 않은 하나 — 에이전트 도구사 3년"
parent: Standalone
nav_order: 1
permalink: /standalone/2026-07-28-agent-scaffolding-history/
date: 2026-07-28
description: "에이전트 도구사 3년을 돌아보며 모델의 약점을 보정하던 구조물이 어떻게 흡수되고 걷혔는지, 끝까지 남는 검증층은 무엇인지 정리한 글."
---

# 흡수된 것들과 흡수되지 않은 하나 — 에이전트 도구사 3년
{: .no_toc }

_2026.07.28 게시_

## 에이전트 도구사 3년을 하나의 규칙으로 압축하면

{: .no_toc }

<details open markdown="block">
  <summary>목차</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## 들어가며: 연표는 많은데 규칙이 없다

"2026 AI 에이전트 트렌드" 같은 글은 이제 검색하면 수십 개가 나온다. 대부분 같은 구조다. ReAct가 있었고, AutoGPT가 있었고, LangChain이 있었고, MCP가 나왔고, 지금은 harness engineering이다. 나열은 정확한데, 나열만으로는 아무것도 결정할 수 없다.

내가 알고 싶은 건 다른 거다. **지금 내가 만들고 있는 것 중에 뭐가 6개월 뒤에 걷어내야 할 짐이 되는가.**

이 질문으로 3년치를 다시 훑어보면 연표가 아니라 규칙이 하나 보인다. 에이전트 도구사는 새로운 개념이 차례로 발명된 역사가 아니다. **모델의 특정 약점을 보정하려고 만든 구조물이 생겼다가, 그 기능이 모델에 흡수되면서 걷혀 나간 역사**다. 그리고 3년 동안 딱 한 층만 흡수되지 않았다.

용어를 두 개만 정해두고 시작한다. **흡수**는 바깥에 코드로 만들어뒀던 기능이 모델이나 런타임 안으로 들어가는 것을 뜻한다. **걷어내기**는 흡수가 끝나 쓸모없어진 바깥 구조물을 제거하는 것이다. 둘은 짝이지만 성격이 다르다. 흡수는 우리가 가만히 있어도 모델 릴리스가 알아서 해준다. 걷어내기는 아무도 대신 해주지 않는다. 이 글 후반부가 문제 삼는 게 정확히 그 비대칭이다.

이 글은 그 규칙과, 흡수되지 않은 한 층에 대한 정리다.

---

## 1부. 만들어졌다 걷힌 것들

각 항목을 "무엇을 보정하려 했나 / 어디로 갔나"로 본다.

### 1-1. 자율 루프 스캐폴딩 (2023년 봄)

AutoGPT, BabyAGI 계열. 태스크 큐, 목표 분해기, 자기 프롬프트 재주입 루프를 **모델 바깥에** 코드로 구현했다.

- **보정 대상**: 모델이 스스로 계획을 세우고 하위 작업으로 쪼개지 못하는 것
- **흡수된 곳**: 모델과 런타임. 계획·분해·재시도의 상당 부분이 네이티브 에이전트 루프로 옮겨갔다. 범용 에이전트에 별도의 태스크 큐와 분해 규칙을 강제하면 네이티브 계획과 충돌하는 이중 관리가 된다

당시 실패 원인으로 지목된 건 무한 루프, 자기검증 부재, 컨텍스트 오버플로였는데, 셋 중 앞의 둘은 모델 개선으로 상당 부분 해소됐다. 세 번째는 해소되지 않고 다음 단계의 주제가 됐다.

<svg viewBox="0 0 700 214" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" role="img" aria-label="2023년에는 목표 분해기와 태스크 큐가 모델 바깥 코드에 있었고, 2026년에는 같은 기능이 모델 안으로 흡수되어 외부 harness가 얇아졌다">
  <defs><marker id="a11" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="none" stroke="currentColor" stroke-width="1.4"/></marker></defs>
  <g font-size="12" fill="currentColor" text-anchor="middle" opacity="0.7">
  <text x="165" y="28">2023</text><text x="535" y="28">2026</text>
  </g>
  <rect x="20" y="40" width="290" height="132" rx="5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.8"/>
  <text x="30" y="56" font-size="11" fill="currentColor" opacity="0.65">외부 스캐폴딩 (코드)</text>
  <g font-size="11" fill="currentColor" text-anchor="middle">
  <rect x="32" y="64" width="84" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="74" y="80">목표 분해기</text>
  <rect x="124" y="64" width="84" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="166" y="80">태스크 큐</text>
  <rect x="216" y="64" width="84" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="258" y="80">재주입 루프</text>
  </g>
  <rect x="32" y="100" width="268" height="58" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <text x="166" y="124" font-size="13" fill="currentColor" text-anchor="middle" font-weight="600">모델</text>
  <text x="166" y="143" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.7">한 스텝 추론 + 툴 호출</text>
  <line x1="322" y1="106" x2="376" y2="106" stroke="currentColor" stroke-width="1.4" marker-end="url(#a11)" opacity="0.8"/>
  <rect x="390" y="40" width="290" height="132" rx="5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.45"/>
  <text x="400" y="56" font-size="11" fill="currentColor" opacity="0.45">harness (얇아짐)</text>
  <rect x="402" y="62" width="266" height="98" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <text x="535" y="84" font-size="13" fill="currentColor" text-anchor="middle" font-weight="600">모델</text>
  <g font-size="11" fill="currentColor" text-anchor="middle">
  <rect x="414" y="96" width="76" height="22" rx="3" fill="currentColor" opacity="0.14"/><text x="452" y="111">계획</text>
  <rect x="498" y="96" width="76" height="22" rx="3" fill="currentColor" opacity="0.14"/><text x="536" y="111">분해</text>
  <rect x="582" y="96" width="74" height="22" rx="3" fill="currentColor" opacity="0.14"/><text x="619" y="111">재시도</text>
  <rect x="456" y="126" width="158" height="22" rx="3" fill="currentColor" opacity="0.14"/><text x="535" y="141">추론 + 툴 호출</text>
  </g>
  <text x="350" y="200" font-size="11.5" fill="currentColor" text-anchor="middle" opacity="0.7">계획·분해가 모델과 런타임으로 옮겨가면서, 외부 큐는 이중 관리가 됐다</text>
</svg>

### 1-2. 체인·그래프 오케스트레이션 (2023 말 ~ 2024)

LangChain, LangGraph, CrewAI, AutoGen.

프레임워크가 나온 이유는 명확하고 정당했다. 2023년 초에는 모델을 문서에 연결하거나, 여러 LLM 호출을 체이닝하거나, 대화 메모리를 관리하거나, 외부 툴 접근을 주는 표준적인 방법이 아예 없었다. 모든 팀이 같은 배관 문제를 처음부터 풀고 있었다. 프레임워크가 떠맡은 것의 상당수는 **모델이 약해서** 생긴 것이다.

- **보정 대상**: 툴 선택의 불안정성, 상태 관리 부재, 재시도·분기 로직
- **흡수 중인 곳**: 모델과 런타임. 네이티브 tool calling, 병렬 툴 호출, 긴 컨텍스트 세션이 그쪽으로 넘어갔다

전부 걷힌 건 아니다. LangGraph의 체크포인팅, human-in-the-loop 일시정지·재개 같은 건 여전히 남는다. 흥미로운 건 남은 게 **"모델 능력 보정"이 아니라 "운영상의 요구"** 쪽이라는 점이다. 이 구분은 뒤에서 다시 쓴다.

<svg viewBox="0 0 700 236" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" role="img" aria-label="명시적 상태 그래프에서는 check 노드에서 통과와 실패로 갈라지는 분기를 사람이 노드로 명시해야 하지만, 단일 루프 방식에서는 모델이 런타임에 결정한다. 체크포인팅과 human-in-the-loop만 남는다">
  <defs><marker id="a12" markerWidth="10" markerHeight="10" refX="7.5" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0.5 L8,4 L0,7.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
  <g font-size="11.5" fill="currentColor" opacity="0.7">
  <text x="30" y="28">명시적 상태 그래프 (외부에서 제어)</text>
  <text x="380" y="28">단일 루프 + 네이티브 tool calling</text>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
  <rect x="30" y="56" width="62" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="61" y="73">plan</text>
  <rect x="112" y="56" width="62" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="143" y="73">tool</text>
  <rect x="194" y="56" width="62" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="225" y="73">check</text>
  <rect x="276" y="56" width="56" height="26" rx="3" fill="currentColor" opacity="0.14"/><text x="304" y="73" opacity="1">out</text>
  <rect x="112" y="118" width="62" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="143" y="135">retry</text>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" marker-end="url(#a12)" opacity="0.8">
  <line x1="92" y1="69" x2="106" y2="69"/>
  <line x1="174" y1="69" x2="188" y2="69"/>
  <line x1="256" y1="69" x2="270" y2="69"/>
  <path d="M225,82 L225,131 L180,131"/>
  <path d="M143,118 L143,88"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.6">
  <text x="263" y="60">pass</text>
  <text x="232" y="105">fail</text>
  </g>
  <text x="181" y="170" font-size="10.5" fill="currentColor" text-anchor="middle" opacity="0.6">분기·재시도를 <tspan font-weight="600">사람이 노드로 명시</tspan></text>
  <rect x="380" y="46" width="290" height="104" rx="6" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <text x="432" y="66" font-size="11.5" fill="currentColor" text-anchor="middle" font-weight="600">모델 루프</text>
  <path d="M445,80.4 A25,25 0 1 1 419,124.6" fill="none" stroke="currentColor" stroke-width="1.8" marker-end="url(#a12)" opacity="0.9"/>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
  <rect x="492" y="72" width="78" height="22" rx="3" fill="currentColor" opacity="0.14"/><text x="531" y="87" opacity="1">tool A</text>
  <rect x="578" y="72" width="78" height="22" rx="3" fill="currentColor" opacity="0.14"/><text x="617" y="87" opacity="1">tool B</text>
  <rect x="492" y="102" width="164" height="22" rx="3" fill="currentColor" opacity="0.14"/><text x="574" y="117" opacity="1">병렬 호출 · 자기교정</text>
  </g>
  <text x="525" y="170" font-size="10.5" fill="currentColor" text-anchor="middle" opacity="0.6">분기·재시도를 <tspan font-weight="600">모델이 런타임에 결정</tspan></text>
  <rect x="30" y="184" width="640" height="34" rx="4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 3"/>
  <text x="350" y="205" font-size="11.5" fill="currentColor" text-anchor="middle">남는 것: 체크포인팅 · 일시정지/재개 · HITL — <tspan font-weight="600">능력 보정이 아니라 운영 요구</tspan></text>
</svg>

### 1-3. 노코드 워크플로우 캔버스 (2024)

여기서 말하는 대상은 n8n 같은 워크플로우 도구 전체가 아니다. API 연동, 스케줄링, 승인 단계처럼 결정론적으로 굴러가는 부분은 멀쩡히 살아 있다. 문제는 **LLM의 판단을 여러 노드로 이어 붙여 추론 경로 자체를 고정하려던 캔버스형 구성**이다. 그 접근은 소멸이 가장 빠르게 진행된 사례에 가깝다.

캔버스 툴은 비엔지니어에게 "견고함의 환상"을 팔았지만, 실제로 제공한 건 **단계의 반복 가능성이지 결과의 품질이 아니었다.** 노드 하나에 LLM이 들어가는 순간 결정론적 프로세스가 결정론적 결과를 보장하지 않고, 노드 몇 개만 넘어가면 오차가 복리로 누적된다.

2026년 현재는 단일 long-horizon 에이전트가 그 캔버스들이 수십 개 노드로 조립하려던 걸 해낸다. 루프가 모델 바깥이 아니라 안에서 돌기 때문이다.

- **보정 대상**: 에이전트 실행 경로의 예측 불가능성
- **걷힌 이유**: 흡수가 아니라 전제가 무너졌다. 예측 가능성을 단계 수준에서 강제해봐야 결과 수준에서는 안 지켜진다는 게 드러났다

아래 그래프는 측정값이 아니라 설명용 모델이다. 각 노드의 성공 여부가 서로 독립이고 모든 노드가 성공해야 전체가 성공한다고 단순 가정했을 때 어떻게 되는지를 보여준다.

<svg viewBox="0 0 700 268" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" role="img" aria-label="노드별 성공률이 95퍼센트면 10개 노드를 지날 때 전체 성공률이 60퍼센트로, 90퍼센트면 35퍼센트로 떨어지는 복리 감쇠 곡선">
  <text x="30" y="26" font-size="11.5" fill="currentColor" opacity="0.7">전체 성공률 = (노드별 성공률)^노드 수 · 노드 독립 가정</text>
  <line x1="60" y1="40" x2="60" y2="212" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <line x1="60" y1="212" x2="660" y2="212" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <g font-size="10.5" fill="currentColor" opacity="0.55" text-anchor="end">
  <text x="53" y="44">100%</text><text x="53" y="129">50%</text><text x="53" y="215">0%</text>
  </g>
  <g stroke="currentColor" opacity="0.12" stroke-dasharray="3 4">
  <line x1="60" y1="125" x2="660" y2="125"/>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.55" text-anchor="middle">
  <text x="60" y="230">0</text><text x="184" y="230">2</text><text x="308" y="230">4</text><text x="432" y="230">6</text><text x="556" y="230">8</text><text x="618" y="230">9</text>
  <text x="360" y="250">노드 수</text>
  </g>
  <polyline points="60,48.5 122,56.6 184,64.2 246,71.5 308,78.5 370,85 432,91.3 494,97.2 556,102.9 618,108.2"
  fill="none" stroke="currentColor" stroke-width="2" opacity="0.85"/>
  <polyline points="60,57 122,72.3 184,86.1 246,98.5 308,109.6 370,119.7 432,128.7 494,136.8 556,144.1 618,150.7"
  fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4" opacity="0.85"/>
  <circle cx="618" cy="108.2" r="3.5" fill="currentColor"/>
  <circle cx="618" cy="150.7" r="3.5" fill="currentColor"/>
  <g font-size="11" fill="currentColor">
  <text x="632" y="105">60%</text>
  <text x="632" y="148">35%</text>
  <text x="300" y="66" opacity="0.8">노드별 95%</text>
  <text x="300" y="126" opacity="0.8">노드별 90%</text>
  </g>
  <text x="360" y="264" font-size="11.5" fill="currentColor" text-anchor="middle" opacity="0.7">단계의 반복 가능성은 보장됐지만, 결과의 품질은 노드 수만큼 복리로 깎였다</text>
</svg>

### 1-4. 프레임워크별 툴 어댑터 층 (2024년 11월, MCP)

MCP가 N×M 통합 문제를 끊었다. 툴이 프레임워크 종속에서 벗어난 시점이고, 이후 A2A·ACP가 같은 계열로 붙었다.

- **보정 대상**: 프레임워크마다 툴 통합을 다시 짜야 하는 것
- **걷힌 것**: 흡수가 아니라 표준으로 대체됐다. 프레임워크의 통합 카탈로그가 갖던 해자(moat)가 사라졌다. "배터리 포함"이 셀링 포인트이던 시절이 끝났다

<svg viewBox="0 0 700 244" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" role="img" aria-label="프레임워크 3개와 툴 4개를 직접 연결하면 12개의 어댑터가 필요하지만, MCP 허브를 두면 7개로 줄어든다">
  <g font-size="11.5" fill="currentColor" opacity="0.7">
  <text x="30" y="26">프레임워크별 어댑터</text>
  <text x="400" y="26">MCP</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35">
  <line x1="105" y1="70" x2="235" y2="58"/><line x1="105" y1="70" x2="235" y2="98"/><line x1="105" y1="70" x2="235" y2="138"/><line x1="105" y1="70" x2="235" y2="178"/>
  <line x1="105" y1="118" x2="235" y2="58"/><line x1="105" y1="118" x2="235" y2="98"/><line x1="105" y1="118" x2="235" y2="138"/><line x1="105" y1="118" x2="235" y2="178"/>
  <line x1="105" y1="166" x2="235" y2="58"/><line x1="105" y1="166" x2="235" y2="98"/><line x1="105" y1="166" x2="235" y2="138"/><line x1="105" y1="166" x2="235" y2="178"/>
  </g>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
  <rect x="35" y="58" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/><text x="70" y="74">FW A</text>
  <rect x="35" y="106" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/><text x="70" y="122">FW B</text>
  <rect x="35" y="154" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/><text x="70" y="170">FW C</text>
  <rect x="235" y="46" width="66" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="268" y="62" opacity="1">툴 1</text>
  <rect x="235" y="86" width="66" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="268" y="102" opacity="1">툴 2</text>
  <rect x="235" y="126" width="66" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="268" y="142" opacity="1">툴 3</text>
  <rect x="235" y="166" width="66" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="268" y="182" opacity="1">툴 4</text>
  </g>
  <text x="168" y="214" font-size="13" fill="currentColor" text-anchor="middle" font-weight="600">N × M = 12</text>
  <g stroke="currentColor" stroke-width="1.2" opacity="0.5">
  <line x1="475" y1="70" x2="512" y2="112"/><line x1="475" y1="118" x2="512" y2="118"/><line x1="475" y1="166" x2="512" y2="124"/>
  <line x1="588" y1="112" x2="625" y2="58"/><line x1="588" y1="116" x2="625" y2="98"/><line x1="588" y1="122" x2="625" y2="138"/><line x1="588" y1="126" x2="625" y2="178"/>
  </g>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
  <rect x="405" y="58" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/><text x="440" y="74">FW A</text>
  <rect x="405" y="106" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/><text x="440" y="122">FW B</text>
  <rect x="405" y="154" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.3"/><text x="440" y="170">FW C</text>
  <rect x="512" y="98" width="76" height="40" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><text x="550" y="123" font-size="12" font-weight="600">MCP</text>
  <rect x="625" y="46" width="60" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="655" y="62" opacity="1">툴 1</text>
  <rect x="625" y="86" width="60" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="655" y="102" opacity="1">툴 2</text>
  <rect x="625" y="126" width="60" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="655" y="142" opacity="1">툴 3</text>
  <rect x="625" y="166" width="60" height="24" rx="3" fill="currentColor" opacity="0.14"/><text x="655" y="182" opacity="1">툴 4</text>
  </g>
  <text x="545" y="214" font-size="13" fill="currentColor" text-anchor="middle" font-weight="600">N + M = 7</text>
  <text x="350" y="238" font-size="11.5" fill="currentColor" text-anchor="middle" opacity="0.7">프레임워크의 "배터리 포함" 통합 카탈로그가 해자를 잃은 지점</text>
</svg>

### 1-5. 그리고 MCP 자신의 일부도 걷혔다 (2025년 말)

이게 이 흐름에서 가장 재밌는 대목이다. **성공이 만든 역풍이다.**

MCP가 잘 되니까 에이전트 하나에 서버가 여러 개 붙고, 서버 하나에 툴이 수십 개씩 붙었다. 그러자 두 가지가 동시에 터졌다. 첫째, 툴 스키마 프리로드가 컨텍스트의 최대 낭비 요인이 됐다. 둘째, 툴 수와 스키마가 늘어날수록 컨텍스트 사용량뿐 아니라 툴 선택 정확도도 같이 떨어지기 시작했다.

2025년 하반기부터 나온 대응이 대체로 하나의 방향을 가리킨다. 아래 수치는 전부 1차 출처에서 직접 확인했다.

| 시점 | 이름 | 보고된 효과 |
|---|---|---|
| 2025.09.26 | Code Mode (Cloudflare) | 툴을 TypeScript API로 변환하면 더 많고 복잡한 툴을 다룰 수 있다. **정량 수치는 제시하지 않음** |
| 2025.11.04 | Code execution with MCP (Anthropic) | 150,000 → 2,000 토큰, 98.7% 절감 |
| 2025.11 | Tool Search Tool (Anthropic) | 약 77.2K → 8.7K 토큰, 85% 절감. 더불어 툴 선택 **정확도**가 Opus 4 기준 49% → 74% |
| 2025.10 | Agent Skills (Anthropic) | 스킬당 메타데이터 ~50토큰만 상주, 본문 ~500토큰, 레퍼런스 2,000+토큰은 필요할 때만 |

표를 만들면서 알게 된 것 두 가지를 적어둔다. 이게 이 절의 서사보다 중요할 수 있다.

**첫째, Code Mode는 이 흐름의 결론이 아니라 출발점이다.** Anthropic의 code execution 글이 Cloudflare를 "유사한 발견을 먼저 발표한 쪽"으로 인용하고 있다. 그리고 Code Mode 원문은 현재 구현이 TypeScript API **전체를 컨텍스트에 올린다**고 명시하면서, 동적 탐색은 향후 개선 과제로 남겨뒀다. 즉 Code Mode를 progressive disclosure 사례로 묶는 건 부정확하다. 같은 문제의식에서 출발했지만 해법의 축이 다르다 — Code Mode는 "툴 호출 대신 코드"이고, Tool Search와 Skills는 "선적재 대신 지연 적재"다.

덧붙여, 이 표를 만들며 참고한 집계 글 여러 곳이 Code Mode에 "입력 토큰 99.9% 감소"라는 수치를 붙여놨는데 원문에는 그런 숫자가 없다. 발행일도 2026년 2월로 적힌 곳이 있었지만 실제로는 2025년 9월이다. 이 분야 수치는 2차 출처를 거치며 부풀려지거나 뒤엉킨 게 꽤 있으니, 인용 전에 원문을 여는 편이 낫다.

**둘째, 이건 비용 절감 얘기만이 아니다.** Tool Search의 85%가 눈에 띄지만, 같은 발표에 정확도 수치가 함께 있다. Opus 4가 49%에서 74%로, Opus 4.5가 79.5%에서 88.1%로 올랐다. 컨텍스트에서 무관한 툴을 빼니까 선택이 정확해진 것이다. 토큰을 아끼려고 한 일이 성능을 올린 셈인데, 이 방향성이 이 글 전체의 논지와 맞물린다. 바깥에 쌓아둔 구조물을 걷어내는 게 손해가 아니었다.

뒤의 세 항목을 관통하는 게 **progressive disclosure**다. 에이전트가 필요로 하기 전까지 정의를 로드하지 않는다. 카탈로그는 크게 유지하고, 워킹셋만 작게 가져간다.


<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" role="img" aria-label="툴 스키마를 전량 프리로드하면 컨텍스트 창의 대부분을 스키마가 차지하지만, progressive disclosure는 메타데이터만 상주시키고 필요할 때 카탈로그에서 조회한다">
  <defs>
  <marker id="a15" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="none" stroke="currentColor" stroke-width="1.3"/></marker>
  <pattern id="sch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="7" stroke="currentColor" stroke-width="2.6" opacity="0.3"/>
  </pattern>
  </defs>
  <text x="30" y="26" font-size="11.5" fill="currentColor" opacity="0.7">전량 프리로드</text>
  <rect x="30" y="38" width="640" height="38" rx="4" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <rect x="31" y="39" width="600" height="36" fill="url(#sch)"/>
  <text x="330" y="62" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">툴 스키마 (전 서버 · 전 툴)</text>
  <text x="650" y="62" font-size="10.5" fill="currentColor" text-anchor="middle" opacity="0.8">작업</text>
  <text x="30" y="94" font-size="11" fill="currentColor" opacity="0.65">≈ 150,000 tokens · 툴이 늘수록 선택 정확도도 함께 떨어짐</text>
  <text x="30" y="130" font-size="11.5" fill="currentColor" opacity="0.7">progressive disclosure</text>
  <rect x="30" y="142" width="640" height="38" rx="4" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <rect x="31" y="143" width="26" height="36" fill="url(#sch)"/>
  <text x="360" y="166" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">작업에 쓸 수 있는 컨텍스트</text>
  <text x="30" y="198" font-size="11" fill="currentColor" opacity="0.65">≈ 2,000 tokens · 메타데이터(왼쪽 빗금)만 상주</text>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
  <rect x="330" y="212" width="90" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/><text x="375" y="228">툴 카탈로그</text>
  </g>
  <path d="M44,182 L44,224 L326,224" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.6" marker-end="url(#a15)"/>
  <path d="M424,224 L560,224 L560,184" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.6" marker-end="url(#a15)"/>
  <text x="200" y="219" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">필요 시 조회</text>
  <text x="500" y="219" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">그때만 적재</text>
</svg>

카탈로그는 크게 유지하고 워킹셋만 작게 가져간다. 프로토콜은 남고 **적재 전략만 뒤집혔다**는 게 이 사례의 핵심이다.

### 1-6. 한 장으로 보면

<svg viewBox="0 0 840 380" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" role="img" aria-label="2023년부터 2026년까지 다섯 개 스캐폴딩 층의 존속 기간과 소멸 시점, 그리고 끊기지 않고 이어지는 검증층">
  <defs>
  <pattern id="fade" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="8" stroke="currentColor" stroke-width="2" opacity="0.28"/>
  </pattern>
  </defs>
  <line x1="200" y1="330" x2="680" y2="330" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <g font-size="12" fill="currentColor" opacity="0.6" text-anchor="middle">
  <text x="270" y="350">2023</text>
  <text x="410" y="350">2024</text>
  <text x="550" y="350">2025</text>
  <text x="650" y="350">2026</text>
  </g>
  <g stroke="currentColor" opacity="0.18" stroke-dasharray="3 4">
  <line x1="340" y1="30" x2="340" y2="330"/>
  <line x1="480" y1="30" x2="480" y2="330"/>
  <line x1="620" y1="30" x2="620" y2="330"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="end">
  <text x="188" y="52">자율 루프 스캐폴딩</text>
  <text x="188" y="97">체인·그래프 오케스트레이션</text>
  <text x="188" y="142">노코드 캔버스</text>
  <text x="188" y="187">프레임워크별 툴 어댑터</text>
  <text x="188" y="232">MCP 툴 전량 프리로드</text>
  </g>
  <g>
  <rect x="228" y="38" width="77" height="20" rx="3" fill="currentColor" opacity="0.22"/>
  <rect x="305" y="38" width="63" height="20" rx="3" fill="url(#fade)"/>
  <rect x="284" y="83" width="196" height="20" rx="3" fill="currentColor" opacity="0.22"/>
  <rect x="480" y="83" width="200" height="20" rx="3" fill="url(#fade)"/>
  <rect x="340" y="128" width="196" height="20" rx="3" fill="currentColor" opacity="0.22"/>
  <rect x="536" y="128" width="70" height="20" rx="3" fill="url(#fade)"/>
  <rect x="256" y="173" width="210" height="20" rx="3" fill="currentColor" opacity="0.22"/>
  <rect x="466" y="173" width="42" height="20" rx="3" fill="url(#fade)"/>
  <rect x="466" y="218" width="133" height="20" rx="3" fill="currentColor" opacity="0.22"/>
  <rect x="599" y="218" width="42" height="20" rx="3" fill="url(#fade)"/>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.6" text-anchor="start">
  <text x="692" y="52">계획이 모델 안으로</text>
  <text x="692" y="97">네이티브 루프로 흡수</text>
  <text x="692" y="142">복리 오차로 붕괴</text>
  <text x="692" y="187">MCP로 표준화</text>
  <text x="692" y="232">progressive disclosure</text>
  </g>
  <rect x="200" y="272" width="480" height="30" rx="4" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="188" y="292" font-size="12" fill="currentColor" text-anchor="end" font-weight="600">검증층</text>
  <text x="440" y="292" font-size="11.5" fill="currentColor" text-anchor="middle" opacity="0.8">한 번도 끊기지 않음 — 이름만 eval → guardrail → sensor로 바뀜</text>
  <text x="692" y="292" font-size="11" fill="currentColor" opacity="0.6">흡수 불가</text>
</svg>

위쪽 다섯 줄은 전부 "모델이 아직 못하는 것"을 바깥에서 메우던 층이고, 빗금 구간에서 걷혔거나 걷히는 중이다. 맨 아래 한 줄만 3년 내내 끊기지 않았다.

---

## 2부. 규칙: Bitter Lesson의 한 층 위 버전

여기까지를 하나로 묶으면 이렇게 된다.

> **모델의 현재 약점을 보정하기 위해 만든 구조물은 그 약점의 수명만큼만 산다.**

Sutton의 Bitter Lesson이 "사람이 넣은 도메인 지식은 결국 계산량에 진다"였다면, 이건 그 한 층 위에서 같은 일이 반복되는 것이다. 사람이 넣은 **실행 구조**가 모델의 내재화에 진다.

harness를 탐색 공간으로 놓고 자동 최적화하는 outer-loop 기법에서 이 구분이 실제로 관찰된다. Meta-Harness(2026)는 두 종류의 결과를 함께 보고한다. 수학 추론용으로 발견한 **검색 정책**은 학습에 쓰지 않은 모델 5종과 처음 보는 분류 데이터셋 9종에서도 개선을 유지했다. 반면 코딩 벤치마크에서 발견한 harness에 대해서는 논문 스스로 **해당 벤치마크 환경에 특화됐다**고 적어뒀고, 그 핵심 구성요소는 "에이전트 루프 시작 전에 샌드박스 스냅샷을 떠서 초반 탐색 턴을 없애는" 환경 부트스트랩이었다.

갈리는 선이 이 글의 구분과 겹친다. 무엇을 가져올지 정하는 정보 라우팅은 옮겨 다녀도 살아남았고, 모델이 초반에 헤매는 걸 대신 메워주던 조각은 그 환경에 묶였다. 2026년 능력에 맞춰 2026년 태스크의 약점을 메운 구조물은, 정확히 다음 릴리스가 흡수해버리는 그 구조물이다.

한 가지는 정확히 해두자. 사라진 경로가 전부 흡수는 아니었다. 1-1, 1-2, 1-5는 모델·런타임이 기능을 가져간 흡수 사례지만, 1-3은 전제 자체가 틀렸음이 드러나 무너진 경우고, 1-4는 표준이 생겨 대체된 경우다. 규칙은 흡수 사례에서 가장 깨끗하게 작동하고, 나머지 둘에는 느슨하게 적용된다.

### 소모품과 자산을 가르는 기준

그래서 실무적으로 쓸 수 있는 판별 질문은 하나다.

**"이 구조물이 존재하는 이유가 '모델이 아직 못해서'인가, 아니면 '모델이 스스로는 도출할 수 없어서'인가?"**

| | 소모품 (흡수된다) | 자산 (흡수 불가) |
|---|---|---|
| 존재 이유 | 모델이 **아직 못한다** | 모델이 **스스로 도출할 수 없다** |
| 정보의 위치 | 모델 안에 언젠가 들어옴 | 조직/코드베이스/도메인 안에 있음 |
| 예시 | 외부 태스크 큐, 강제 분해기, 툴 선택 힌트, 프롬프트 우회 트릭, 노드 그래프 | CLAUDE.md·AGENTS.md의 도메인 규칙, 커스텀 린터, 구조 테스트, 모듈 경계 강제, 수용 기준 |
| 모델이 좋아지면 | 불필요해지거나 방해가 됨 | 그대로 필요하거나 오히려 더 필요해짐 |

두 번째 열이 그냥 "흡수되지 않는다"가 아니라 **"모델이 좋아질수록 더 필요해진다"**는 게 핵심이다. 그 이유가 3부다.

---

## 3부. 흡수되지 않은 하나: 검증

### 3-1. 왜 검증만 흡수되지 않는가

용어를 한 번 더 좁혀두자. 이 글에서 **검증**은 생성된 결과를 사후에 검사하는 좁은 뜻이 아니다. 모델 밖에 정답 기준을 두고, 생성 전에는 가이드로 방향을 잡고 생성 후에는 센서로 결과를 확인하는 **층 전체**를 뜻한다. 그래서 CLAUDE.md의 도메인 규칙(생성 전)과 커스텀 린터(생성 후)가 같은 층에 들어간다. 둘 다 "모델이 스스로 도출할 수 없는 기준"을 모델 밖에 두고 적용하는 장치라는 점에서 같다.

정답이 뭔지는 모델 안에 없다. 조직 밖, 코드베이스 밖, 도메인 안에 있다.

이건 능력 문제가 아니라 **정보 문제**다. 모델이 아무리 좋아져도 "이 커밋이 우리 결제 정책에 맞는가"는 모델이 일반 지식에서 추론으로 도달할 수 있는 명제가 아니다. 알려주면 알지만, 알려주지 않으면 영원히 모른다. 누군가 그 정책을 검증 가능한 형태로 바깥에 놓아야 한다. 이게 3년 내내 어떤 모델 릴리스도 흡수하지 못한 층이다.

그리고 생산량이 늘수록 이 층의 부하는 선형이 아니라 그 이상으로 늘어난다.

### 3-2. 숫자로 확인되는 것들

**delegation gap.** Anthropic의 2026 Agentic Coding Trends Report의 중심 수치. 개발자는 업무의 약 60%에 AI를 쓰지만, **완전히 위임 가능한 건 0~20%**다. 자사 엔지니어 자기보고 기반 수치라는 점은 감안해서 읽어야 한다. 리포트는 이걸 도입 실패가 아니라 발견으로 읽는다. 효과적인 AI 협업은 참여적이다 — 셋업, 프롬프팅, 감독, 검증, 판단은 마찰이 아니라 그게 일 자체다.

**복리 실패.** 체인의 각 에이전트가 70% 성공률이면 3-에이전트 체인은 전체 34%가 된다. 단일 턴 태스크에서 80~90%를 찍는 모델이 애플리케이션을 넘나드는 다단계 워크플로우에서는 크게 떨어진다는 벤치마크 보고도 있다. 데모를 파는 벤치마크와 프로덕션 동작을 예측하는 벤치마크는 다른 시험이다.

**신뢰성이 정확도를 못 따라간다.** ICML 2026에 실린 연구는 프론티어 모델 십수 종을 GAIA와 τ-bench에서 반복 실행하며 일관성·강건성·예측가능성·안전성으로 쪼개 측정했는데, **정확도는 꾸준히 올랐지만 전체 신뢰성 개선은 미미했다**고 보고한다. 능력 곡선과 신뢰성 곡선이 갈라져 있다는 게 이 흐름 전체의 요약에 가깝다. (이 논문은 arXiv 개정판마다 대상 모델 수와 기간 표기가 12~15종, 18개월/24개월로 달라진다. 그래서 여기서는 숫자를 인용하지 않았다.)

**실패 원인의 위치.** 프로덕션 실패의 상당수는 모델이 아니라 데이터 품질, 컨텍스트 공백, 거버넌스에서 온다. 모델은 배포 전 eval을 다 통과했다. 실패한 건 워크플로우다.

### 3-3. harness engineering = 검증층에 이름이 붙은 사건

2026년 초에 "harness engineering"이라는 용어가 주류에 진입했다. Birgitta Böckeler의 martinfowler.com 글이 기폭제였고, OpenAI와 Addy Osmani가 뒤이어 붙었다. 프레임은 **Agent = Model + Harness**다.

Böckeler의 뼈대는 두 가지 통제 장치다.

- **Guides (feedforward)** — 생성 *전에* 방향을 잡는다. 첫 시도에서 맞을 확률을 올린다. CLAUDE.md/AGENTS.md, 큐레이션된 문서, 아키텍처 제약
- **Sensors (feedback)** — 생성 *후에* 오류를 잡는다. 커스텀 린터, 구조 테스트, 모듈 경계 검사, 일관성 스캔

출발점이 중요하다. Böckeler의 문제의식은 "코딩 에이전트를 **덜 감독하면서** 쓰려면 결과에 대한 신뢰를 올릴 방법이 필요하다"였다. 즉 harness engineering은 새로운 능력을 추가하는 기술이 아니라, **검증 부담을 사람에서 시스템으로 옮기는 기술**이다.

여기서 이 글의 두 축이 만난다. 지난 3년간 걷힌 건 전부 "모델을 대신 똑똑하게 만들려던 구조물"이었고, 담론이 최종적으로 도착한 곳은 "모델의 출력을 확인하는 구조물"이다. 도구사가 다른 데를 헤매다 여기로 온 게 아니라, **다른 데가 전부 흡수돼서 여기만 남은 것**에 가깝다.

---

## 4부. 그래서 뭘 봐야 하나

지금 굴리고 있는 harness를 한 줄씩 놓고 이 순서로 물어보면 된다.

1. **이게 없으면 모델이 못하는가, 아니면 알려주지 않으면 모를 뿐인가?**
    - 못한다 → 소모품. 모델 업그레이드마다 필요 여부 재확인
    - 모른다 → 자산. 유지보수 대상으로 관리
2. **이게 모델 업그레이드 후에도 여전히 켜져 있는가?**
    - 흡수가 끝난 구조물을 안 걷어내면 그냥 방해물이다. 이중 계획 관리, 불필요한 프롬프트 우회, 안 쓰는 MCP 서버가 여기 해당
3. **검증 실패를 사람이 잡고 있는가, 센서가 잡고 있는가?**
    - 사람이 잡고 있으면 그건 스케일 안 되는 구간이다. 그 항목이 다음에 자동화할 것
4. **eval이 단일 태스크를 재고 있는가, 시퀀스를 재고 있는가?**
    - 대부분의 eval은 워크플로우에 박힌 에이전트가 아니라 격리된 에이전트를 잰다. 복리 실패는 여기서 안 보인다

---

## 5부. 이 주장에 대한 반론

이 글의 결론이 틀릴 수 있는 경로가 최소 세 개다.

**(1) 검증도 흡수될 수 있다.** self-verification, LLM-as-judge, agent-as-a-judge가 충분히 좋아지면 검증층도 모델 안으로 흡수된다는 반론이 가능하다. 현재로선 근거가 약하다 — 편향을 겨냥한 스트레스 테스트에서는 강한 모델도 절반 넘게 틀렸고, 후보 배치 순서나 반복 실행만으로 판단이 뒤집히는 문제가 보고돼 있다. 다만 이 수치는 일반적인 LLM-judge 전반이 아니라 편향을 노리고 설계한 평가에서 나온 것이라는 점은 짚어둬야 한다. 다만 "현재로선"이 언제까지일지는 나도 모른다. 이 글의 규칙을 이 글 자체에 적용하면, **검증층이 자산인 이유는 정보 문제라서지 난이도 문제라서가 아니어야** 한다. 만약 어떤 검증이 단순히 "모델이 아직 잘 못해서" 바깥에 있는 거라면 그것도 소모품이다.

**(2) "걷혔다"는 판정이 성급할 수 있다.** LangChain 생태계는 여전히 크고, 프레임워크가 죽었다는 주장은 매년 나오고 매년 틀렸다. 내가 걷혔다고 쓴 항목들 중 일부는 실제로는 "성장이 멈췄다" 정도일 수 있다.

**(3) 이 규칙 자체가 지금 모델 세대에 과적합일 수 있다.** 위에서 harness 자동 최적화가 태스크 분포에 과적합된다고 비판했는데, "약점 보정은 흡수되고 정보 인코딩은 남는다"는 규칙도 2023~2026 구간에서 뽑은 것이다. 표본이 3년이다.

---

## 닫으며

3년을 관통한 규칙은 한 줄이다. **모델을 대신 생각하게 만들려던 구조물은 흡수됐고, 모델 밖에 있는 기준을 넣고 확인하는 구조물만 남았다.**

그래서 새 harness 조각을 붙이기 전에 물어볼 것도 하나다. 이건 모델이 아직 못해서 필요한가, 아니면 모델이 스스로는 도출할 수 없는 기준을 전달하고 검증하기 위해 필요한가. 전자면 다음 릴리스가 가져간다. 후자면 다음 릴리스가 와도 내 몫으로 남는다.

서론의 질문 — 뭐가 6개월 뒤에 걷어내야 할 짐이 되는가 — 에 대한 답이 그거다. 짐이 될 것과 남을 것은 걷어낼 때가 아니라 만들 때 이미 갈린다.

---

## 참고

본문에서 단정하지 않은 것들을 먼저 적어둔다. Tool Search Tool과 Agent Skills의 발표일(2025.11 / 2025.10)은 수치와 달리 2차 출처에 의존해서 월 단위로만 썼다. LangChain 최초 릴리스 시점은 출처마다 2022년 말과 2023년 1월로 갈려 특정하지 않았다. 프로덕션 실패율 70~95%나 "2027년까지 40% 취소" 같은 수치는 컨설팅·벤더 리포트 계열이라 정의와 표본이 제각각이어서, 논지를 받치는 데 쓰지 않고 방향성 참고로만 언급했다.

- Anthropic, *Effective context engineering for AI agents* — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Anthropic, *Code execution with MCP: Building more efficient agents* (2025.11.04) — <https://www.anthropic.com/engineering/code-execution-with-mcp>
- Anthropic, *Introducing advanced tool use on the Claude Developer Platform* (Tool Search Tool / Programmatic Tool Calling) — <https://www.anthropic.com/engineering/advanced-tool-use>
- Anthropic, *Equipping agents for the real world with Agent Skills* — <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
- Anthropic, *Agent Skills* (Claude Platform Docs) — <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>
- Kenton Varda, Sunil Pai, *Code Mode: the better way to use MCP* (Cloudflare, 2025.09.26) — <https://blog.cloudflare.com/code-mode/>
- Anthropic, *2026 Agentic Coding Trends Report* — <https://resources.anthropic.com/2026-agentic-coding-trends-report>
- Birgitta Böckeler, *Harness engineering for coding agent users* (2026.04.02) — <https://martinfowler.com/articles/harness-engineering.html>
- Birgitta Böckeler, *Maintainability sensors for coding agents* (2026.05.27) — <https://martinfowler.com/articles/sensors-for-coding-agents.html>
- Addy Osmani, *Agent Harness Engineering* — <https://addyosmani.com/blog/agent-harness-engineering/>
- Han Chung Lee, *Hidden Technical Debt of AI Systems: Agent Harness* (2026.05.08) — <https://leehanchung.github.io/blogs/2026/05/08/hidden-technical-debt-agent-harness/>
- LangChain, *How and when to build multi-agent systems* — <https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems>
- *Towards a Science of AI Agent Reliability*, ICML 2026 — <https://arxiv.org/abs/2602.16666>
- Yoonho Lee et al., *Meta-Harness: End-to-End Optimization of Model Harnesses* (2026) — <https://arxiv.org/abs/2603.28052>
