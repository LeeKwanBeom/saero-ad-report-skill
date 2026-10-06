# CSS · 레이아웃 · 재발 방지 기록

디자인이나 레이아웃을 건드려야 할 때 읽는다. 정기 데이터 갱신만 할 때는 필요 없다.

## 디자인 토큰 (브랜드 아이덴티티 고정)

```
메인 민트          #45ceb3
진한 민트          #2ea88f
연한 민트(배경)     #e8f9f5
잉크(진한 남색계열) #1c2b2a
배경지             #fbfaf7
폰트   Pretendard / Apple SD Gothic Neo / Noto Sans KR
차트   Chart.js 4.4.1 (cdnjs 경유) + chartjs-plugin-datalabels
```

**플레이스 광고 = 민트, 파워링크 광고 = 잉크.** 모든 차트에서 일관 유지.

브랜드 팔레트(민트 계열 + 잉크) 밖의 색(빨강·노랑 등)을 임의로 추가하지 않는다.

**같은 강조색을 서로 다른 의미로 쓰지 말 것.** 진한 민트(`.ctr-high`)는 이미
"클릭률 기준(config `ctr_high_threshold`, 현재 4%) 이상"에 배정돼 있으므로 다른 지표 강조에 재사용하지 않는다.
표 번호와 무관하게 뜻은 하나다 — 클릭률 기준 이상, 그 외 용도 금지.
현재 01번·07번 두 표에서 쓰고 있고, 다른 표에 클릭률 열이 생기면 같은 기준으로 적용한다.

### 적용되어 있는 시각 요소

- KPI 카드 4개: 각기 다른 강조색 + 왼쪽 4px 강조선 + 우상단 라인 아이콘(SVG stroke) +
  카드 우상단 원형 배경 장식
- 11번 핵심요약: 잉크→진한틸 그라데이션 배경, 민트색 불릿
- 푸터 상단에 얇은 그라데이션 라인(밝은민트→민트→진한틸)
- 모든 `.card`와 KPI 타일에 은은한 그림자
  `box-shadow: 0 1px 3px rgba(28,43,42,0.05), 0 8px 20px rgba(28,43,42,0.05)`

**제거된 것 — 다시 추가하지 말 것**: 제목 텍스트 그라데이션, 헤더 배경 블롭 장식.
시도했다가 "안 어울린다"고 판단해 제거했다.

## CSS 유틸리티 클래스

인라인 스타일을 반복 생성하지 말고 이 클래스들을 쓴다. (인라인이 130곳까지 늘어난
적이 있고, 조건부 강조를 인라인으로 관리하다 CTR 오강조 사고가 났다.)

```
.ctr-high     클릭률 기준(config ctr_high_threshold, 현재 4%) 이상 강조(진한민트+굵게). 표 무관, 클릭률 전용
.note         보조 설명 문단 (11.5px, ink-soft, line-height 1.55)
.note-mint    민트색 강조 해석 문단 (11.5px, mint-dark, 굵게, 1.55)
.sub-head     카드 안 소제목 (11.5px, 굵게, margin 12px 0 6px)
.stat-grid    숫자 그리드 (.k 라벨 / .v 값)
.scroll-x     가로 스크롤 wrapper (차트용)
.scroll-hint  스크롤 안내 뱃지 — 직접 마크업에 넣지 말 것 (스크립트가 자동 처리)
.scroll-fade  오른쪽(::after)·왼쪽(::before, 판 C) 끝 페이드용 래퍼 — 스크립트가 자동으로 감쌈
.wide-table   컬럼 많은 표 wrapper
.fold         접기 <details> (레이아웃 판 r2026-10-B — 아래 "접기 안내"). summary 에 cursor:pointer
.fold-more    접기 머리 중 새로 생긴 것(03 "이전 N일 펼치기" · 경쟁사 "표 N행 · 펼치기") — 12px 굵게 진한민트, 펼치면 아래 8px
```

### .wide-table 안의 표

```css
width: auto;          /* 셀을 내용 크기에 맞춤 */
min-width: 100%;      /* 내용이 좁으면 컨테이너를 채움 */
white-space: nowrap;  /* 줄바꿈으로 셀 찌그러지는 것 방지 */
```

**폭을 고정 px로 지정하지 말 것.** 컬럼 수에 따라 560/660/720px을 부여했다가,
짧은 숫자만 든 표가 그 폭까지 억지로 늘어나면서 셀이 내용에 비해 과하게
뚱뚱해지는 문제가 생겼다(td.num이 30px 높이에 73px 폭). 컬럼별 실제 내용 길이를
사람이 예측해 px를 정하는 방식 자체가 무리였다.

12번 다음액션 표처럼 컬럼이 2개뿐이고 본문이 긴 표에는 `.wide-table`을 붙이지 않는다.

## 여백·밀도 기준

01번 인사이트 박스가 모바일에서 지나치게 길어 전체 밀도를 한 단계 조였다.
새 요소를 추가할 때도 이 값에 맞춘다. 다시 넉넉하게 벌리지 말 것.

```
.note / .note-mint 줄간격      1.55
.sub-head 여백                 12px 위 / 6px 아래
카드 안 결론 문단(구분선 포함)   margin-top 10px + padding-top 8px
숫자 카드 그리드                gap 6px, 라벨-값 간격 2px, 값 폰트 15px
표 행 padding (모바일 640px 이하) 6px
접기(.fold) 머리                 03 접기 위 10px(표와 사이) · .fold-more 펼쳤을 때 아래 8px ·
                                07 목록·08 머리는 옛 머리글 여백 그대로(margin-bottom 8px / sub-head 0 0 6px)
```

## 가로 스크롤 안내 자동화

페이지 하단 스크립트가 `.wide-table` / `.scroll-x` 요소를 훑어서
`scrollWidth > clientWidth`인 경우에만 처리한다:

1. **안내 뱃지** — `← 좌우로 밀어서 전체 보기` (연한민트 배경, 진한민트 굵은 글씨,
   알약 모양)를 앞에 자동 삽입. 넘치지 않으면 제거
2. **오른쪽 페이드** — 요소를 `.scroll-fade` 래퍼로 감싸고 `::after`로 흰색
   그라데이션. 끝까지 스크롤하면 `.at-end`가 붙어 사라짐
3. **왼쪽 페이드**(레이아웃 판 r2026-10-C, 2026-10-06) — 같은 래퍼의 `::before`(`linear-gradient(to left, …)`, 새 색 0).
   맨 왼쪽(scrollLeft ≤ 2)이면 `.at-start`가 붙어 사라진다 — `updateEnd`가 at-end 와 같이 맞춘다. 넘침이 없어진 박스(회전 뒤 모바일 가로 막대)는
   래퍼에 at-end·at-start 를 둘 다 붙여 페이드를 모두 숨긴다

창 크기 변경(resize)에도 다시 계산된다.

**시작 위치(S, 판 C)**: PC 의 01·06 차트(분기 도우미가 아는 `.scroll-x` 둘)는 로드 때 **오른쪽 끝(최신 날짜)** 에서 시작한다 — 안내 스크립트 끝의
`load` 리스너가 `setTimeout 0` 으로 `window.__saeroMobile.scrollEnd()` 를 부른다. `sync`의 래퍼 감싸기는 DOM 을 옮기며 그 박스의 scrollLeft 를 0 으로
되돌리므로 반드시 그 **뒤**여야 한다(2026-10-06 [실측]). 회전·창 크기로 PC 분기로 돌아올 때도 분기 도우미가 `sync` 뒤에 같은 일을 한다.
표(`.wide-table`)는 그대로 왼쪽에서 시작. 뱃지 문구 그대로. PC 인쇄는 화면의 scrollLeft 를 그대로 따른다 — 판 C 부터 PC PDF 의 01·06 은
최신 쪽 구간(1280 창·A4 여백 0.4in 에서 01 9/26 무렵~10/3·10/4, 06 9/28~10/5)이 찍히고, 일수는 판 B(8/26 부터)와 같은 ≈8일이다(2026-10-06 [실측] — 종이 폭에 잘리는 것은 그대로).
`window.__saeroSync` 는 안내 스크립트 IIFE 의 지역 함수 `sync` 를 노출한 것(복사본 아님) — 분기 도우미가 회전 뒤 뱃지·페이드를 resize 디바운스(200ms)를
기다리지 않고 바로 맞추려고 부른다. `scrollEnd` 는 `updateEnd` 를 직접 못 부르므로 박스에 `scroll` 이벤트를 보내 at-end·at-start 를 다시 계산하게 한다.

**새 표·차트를 추가할 때 안내를 직접 써넣지 말 것.** wrapper에 `.wide-table`(표)
또는 `.scroll-x`(차트)만 붙이면 된다.

구현 주의:
- 페이드를 스크롤 컨테이너 자신에 `::after`로 주면 내용과 같이 스크롤돼 오른쪽
  끝에 고정되지 않는다. 그래서 스크립트가 래퍼를 한 겹 감싼다
- 페이드는 표와 차트 **양쪽 모두**에 적용한다. 처음엔 "차트는 잘린 게 눈에 보이니
  불필요"하다고 보고 표에만 넣었는데, 같은 리포트 안에서 한쪽만 페이드가 있어
  일관성이 깨진다는 피드백을 받고 통일했다
- 페이드 도착색이 `var(--card)`(흰색)이므로 스크롤 요소는 항상 `.card` 안에 둔다

## 접기 안내 (레이아웃 판 r2026-10-B, 2026-10-06)

긴 목록·표를 `<details class="fold">` 로 접는다(report-structure.md 맨 위 "레이아웃 판" — 03 이전 날짜 · 07 클릭 1건·클릭 0 목록 · 07 경쟁사표 · 08 TOP 10 밖, 5개).
기본 닫힘. 만드는 것은 `scripts/apply.py --layout`(옛 판을 이 판으로 바꿀 때 CSS·스크립트까지 한 번에 넣는다) — 손으로 넣지 않는다.

1. **CSS**: `.fold > summary{cursor:pointer;}` · `.fold-more{font-size:12px;font-weight:700;color:var(--mint-dark);}` · `.fold[open] > .fold-more{margin-bottom:8px;}`
   — 새 색 0(진한민트는 팔레트 안. `.ctr-high` 클래스는 쓰지 않는다). summary 의 마커(▶)는 브라우저 기본 그대로.
2. **toggle → 가로 안내 다시 맞추기**: 하단 가로 스크롤 안내 스크립트의 `resize` 줄 뒤에
   `document.querySelectorAll('details').forEach(d => d.addEventListener('toggle', sync))` — 닫힌 접기 안의 `.wide-table` 은 화면 폭이 0 이라
   load 때 뱃지·페이드 판단이 어긋날 수 있어 펼칠 때 다시 잰다(`toggle` 은 버블링하지 않으므로 details 마다 붙인다).
3. **인쇄**: `beforeprint` 에 닫힌 details 를 전부 열고 `afterprint` 에 그것만 다시 닫는다 — 닫힌 접기 안은 인쇄·PDF 에 찍히지 않기 때문.
   (iOS 공유 → PDF 처럼 이 이벤트가 오지 않는 경로는 [추론] — 확인 전)
4. **기준점 보존**: 앵커 문구(`클릭 1건 검색어`·`노출은 있으나 클릭 0건인`·`TOP 10 외`)는 summary 안 리터럴 그대로, `line-height:1.9;` 는 목록 div 세 곳에만
   (summary·details·`.fold` 에 쓰지 않는다 — validate·compare·apply 가 "앵커 뒤 첫 `line-height:1.9;">`"를 목록으로 읽는다). 경쟁사표 머리글 div 리터럴
   "경쟁사 브랜드명 검색어" 는 접기 밖 그대로. CSS·JS 주석에 `<details`·`<summary` 를 꺾쇠로 쓰지 않는다(validate 태그 짝이 센다).
5. **검사**: validate "레이아웃 판"(meta = config · details 5 · 짝) · overflow_check 는 details 를 전부 열고 3폭을 잰다 · 높이(닫힘·열림)는 회차 기록의 관찰값.

## 반응형

- viewport meta 적용됨
- `@media (max-width: 900px) and (min-width: 641px)` 태블릿 분기 —
  `grid-2` / `grid-2-07`을 1단으로 스택
- `@media (max-width: 640px)` — KPI 4개→2개씩 줄바꿈, 2단 그래프→1단,
  표 폰트/패딩 축소
- (판 C, 2026-10-06) 01·06 차트 모양은 CSS 가 아니라 JS 분기 — 차트 스크립트 끝 분기 도우미의 `matchMedia('(max-width: ' + M.maxPx + 'px)')`,
  M.maxPx = config `report_layout.mobile.max_px`(640) = 위 모바일 CSS 경계. validate "레이아웃 판" 이 JS(M 줄·matchMedia 꼴)와 CSS `@media (max-width: 640px){` 를
  config 와 대조한다. 경계 값을 바꾸는 것은 설계 회차 몫 — config 만 바꾸면 apply 가 M 줄만 다시 쓰고 배포본 CSS 리터럴은 그대로라 validate 가 FAIL 로 멈춘다

## PWA 설정

스마트폰에서 "홈 화면에 추가" 시 앱처럼 열린다.

- `manifest.json` — 앱 이름·아이콘·standalone 모드
- `service-worker.js` — **network-first**. 인터넷이 되면 항상 최신을 받아오고,
  안 될 때만 캐시를 보여준다. 데이터가 매주 바뀌는 리포트라 강하게 캐싱하면
  지난주 데이터가 보일 위험이 있어 이 전략으로 결정했다.
  **특별한 이유 없이 이 전략을 바꾸지 말 것**. 판이 바뀐 첫 배포(예: 판 C) 뒤에도 온라인이면 첫 열기에 새 판을 받는다 —
  오프라인으로 연 홈 화면 앱은 캐시된 옛 판일 수 있다(실기기 확인은 사용자 몫)
- `icon-192.png`, `icon-512.png` — 홈 화면 아이콘
- `favicon.png` (정사각 로고) / `og-image.png` (1500×1200 풀버전 로고, 카톡 미리보기용)
  두 파일은 용도가 다르니 헷갈리지 말 것

카톡 미리보기가 안 바뀌면 카카오 공유 디버거
(https://developers.kakao.com/tool/debugger/sharing)에서 URL 캐시를 초기화한다.

---

# 재발 방지용 버그 기록

같은 실수를 반복하지 않기 위한 기록. 새 요소를 추가할 때 해당 패턴을 확인한다.

**1. Chart.js 다중 라벨**
문자열에 `"\n"`을 넣으면 캔버스에서 줄바꿈이 안 되고 깨진다.
배열로 쓸 것: `['플레이스 광고','(새로필라테스)']`

**2. 가로 막대 차트 높이 고정**
캔버스 높이를 고정할 땐 `maintainAspectRatio:false`를 반드시 같이 설정한다.
`barThickness`를 큰 고정값으로 주면 좁은 컨테이너에서 막대가 겹치므로
`maxBarThickness` + `categoryPercentage`/`barPercentage` 조합으로 자동 조절되게 한다.

**3. 표 스크롤에 display:block 금지**
`<table>`에 `display:block`을 주면 안쪽 grid가 깨져 컬럼이 어긋나거나 표가
오른쪽으로 무한정 밀린다. 표를 `<div style="overflow-x:auto;">`로 감싸고
표 자체는 기본 table 레이아웃을 유지한다.

**4. 복합 차트는 고정 높이 컨테이너**
데이터 라벨·범례·양쪽 축이 많은 콤보 차트는 비율 유지 방식만 쓰면 모바일에서
세로까지 줄어들어 라벨이 겹친다. `<div style="height:280px;">`로 감싸고
`maintainAspectRatio:false`를 설정한다. 8개 차트 전부 이 패턴으로 통일돼 있다.
(판 C) 모바일 분기(≤ config mobile.max_px)에서는 01·06 컨테이너 높이를 JS 가 `n × row_px + pad_px` 로 정하고 PC 복귀 때 280/240 을 복원한다 — HTML 의 inline 값은 PC 값 그대로.

**5. 카테고리 많은 차트는 가로 스크롤**
24개 시간대처럼 카테고리가 많으면 모바일에서 라벨이 겹친다. 라벨을 줄이거나
숨기는 것보다 `overflow-x:auto` + `min-width` + `autoSkip:false`로 스크롤시키는
쪽이 정보 손실이 없어 우선한다.
예외(2026-10-06): 두 줄 tick 처럼 라벨을 나누는 것·화면 방향 바꾸기(판 C 01·06 모바일 가로 막대 — 날짜 tick·숫자 전부 그대로)는 줄이거나 숨기는 것이 아니라 손실이 아니다.

**6. 콤보 차트 범례 위치**
마지막 날짜가 최고치를 찍으면 top-right 범례가 데이터 라벨과 겹친다.
어느 날이 최고치든 겹칠 수 있는 구조적 문제라 `bottom`으로 고정한다.

**7. grid 안의 넓은 표**
CSS Grid 칸에 컬럼 많은 표를 넣으면 칸이 표의 최소 너비만큼 강제로 넓어지면서
내부 스크롤이 무력화되고 페이지 전체가 가로로 밀린다.
`.grid-2-07 > *{min-width:0;}`처럼 자식에 `min-width:0`을 준다.

**8. 매주 늘어나는 차트의 폭**
01번은 날짜가 매주 늘어나 고정 폭으로 두면 막대·라벨이 점점 좁아지다 겹친다.
`min-width = max(날짜 수 × per_day_px, floor_px)`로 자동 확장되게 한다.
두 값은 `config/report-config.json`의 `chart_min_width`에 있다(기본 80px / 650px).
대상 섹션도 같은 파일 `date_based_sections`에 적혀 있다(현재 01·06번).
06번 `rankChart`도 x축이 날짜라 같은 규칙의 대상이다(N일 × per_day_px, 01번과 같은 값).
05번처럼 카테고리 수가 고정인 차트에는 필요 없다.
(판 C) 모바일 가로 막대에서는 폭이 아니라 **높이**가 날짜 수에 비례해 는다(`n × row_px + pad_px`, config `report_layout.mobile` — 90일이면 ≈2,430px).
행 높이 하한·모바일 기간 창 같은 n 규칙은 아직 없다(이월 — ≈90일 전 정기점검).

**9. 표 재정렬 시 조건부 스타일 어긋남**
07번 표를 클릭수 내림차순으로 재배열하면서, 다른 행의 셀을 복사해 값만 바꾸는
과정에 강조 스타일(`.ctr-high`)이 같이 복사돼 CTR 3.68%(4% 미만) 행에 남았다.

재발 방지:
- 행을 복사해 값만 교체하는 방식을 피하고, 스타일은 항상 새로 판단해서 넣는다
- 업데이트 후 `scripts/validate.py`로 조건과 실제 스타일을 전수 대조한다

**10. 줄바꿈 기회가 없는 긴 문자열이 카드 밖으로 넘침 (2026-09-23, 10번)**
`216·242·260·…·318회`처럼 숫자를 가운뎃점(`·`)으로 이어 붙인 나열은 브라우저가
`·` 앞뒤를 줄바꿈 지점으로 보지 않아 한 덩어리로 취급한다. 17개짜리 나열이 모바일
카드 폭(약 320px)을 넘어 **페이지 전체에 가로 스크롤**이 생겼다(390px 뷰포트에서
scrollWidth 418). 한글 나열(`노원역아기·아기랑노원구·…`)은 음절 사이에서 끊기므로
문제없고, 숫자·영문·기호만 이어진 나열이 대상이다.

재발 방지(둘 다 적용돼 있음):
- 안전망: `body{overflow-wrap:anywhere;}` — 넘칠 때만 문자열 안에서 강제로 끊는다.
  `white-space:nowrap`인 `.wide-table` 표에는 영향 없다. **지우지 말 것**
- 긴 숫자 나열을 쓸 때는 구분점마다 `·<wbr>`를 넣어 숫자 중간이 아니라 구분점에서
  끊기게 한다(안전망만 있으면 `2|98`처럼 숫자 가운데가 잘릴 수 있다). 12개 이상
  나열이면 넣는다고 보면 된다. validate.py 태그 짝 검사는 `<wbr>`을 세지 않는다
- 갱신 후 확인: playwright(컨테이너에 설치돼 있음)로 390px 뷰포트에서
  `document.documentElement.scrollWidth`가 390인지 본다. 넘치는 텍스트는 요소 박스가
  아니라 텍스트 노드라 `getBoundingClientRect`로는 잡히지 않는다

**11. 접기(details) 안은 검사·인쇄·찾기에서 빠지기 쉽다 (2026-10-06, 레이아웃 판 r2026-10-B)**
접힌 `<details>` 안의 표·목록은 화면에 그려지지 않아 (1) 가로 넘침 검사가 닫힌 채로 재면 안의 넘침을 못 보고
(2) 안의 `.wide-table` 은 load 때 폭이 0 이라 가로 안내 판단이 어긋날 수 있고 (3) 인쇄·PDF 에 찍히지 않으며
(4) 브라우저에 따라 페이지 내 검색에 안 잡힌다. 또 (5) 접기 머리(summary)의 개수·날짜는 어느 서술 스크립트도 안 고치면
다음 회차부터 조용히 묵는다(목록은 36개인데 머리는 35개).
재발 방지(전부 적용돼 있음):
- `tests/overflow_check.py` 는 details 를 전부 열고 잰다
- 안내 스크립트가 details `toggle` 때 `sync` 를 다시 부른다(headless Chromium 에서는 닫힌 채로도 뱃지가 붙어 재현이 안 됨 — 실기기 확인은 [추론])
- `beforeprint` 에 전부 열고 `afterprint` 에 되돌린다(headless Chromium `page.pdf()` 에서 beforeprint 순간 5개 전부 열림·afterprint 뒤 0 [실측 2026-10-06])
- summary 의 개수·날짜는 `scripts/apply.py` 가 compute.json 으로 매 회차 쓰고 compare.py 가 summary 4항목으로 대조한다
- 서술 표지·각주(07 ①②③·08 note)는 접기 밖에 둔다 — 안으로 옮기면 검사는 통과하고 조용히 숨는다

**12. 화면 폭에 따라 차트 모양을 바꿀 때 (2026-10-06, 레이아웃 판 r2026-10-C — 01·06 모바일 가로 막대) [실측]**
(1) load 때 한 번만 판정하면 회전(390→844 — 가로 막대 그대로)·창 축소(1280→600 — 세로 3,280 스크롤 그대로)에서 모양이 어긋난다 → `matchMedia` change 로
다시 판정한다(상태 비교 — 로드 직후·afterprint 뒤에도 change 가 한 번 더 온다 · 동기 · 구형 iOS `addListener` 폴백 · 기능 감지).
(2) Chromium `page.pdf()`(인쇄)는 레이아웃을 종이 폭(≈794px, 여백 0.4in 이면 ≈720px)으로 다시 짜고 `(max-width: 640px)` change 를 beforeprint **뒤**에 보낸다
(window `resize` 는 안 옴) — 인쇄 중에 다시 그리면 빈 캔버스가 찍힌다 → beforeprint~afterprint 동안 판정을 잠근다(`printing`).
(3) 세로로 긴 캔버스(01 모바일 1,156px)는 한 쪽(≈1,050px)을 넘으면 쪽 나눔에서 통째로 빠진다 → beforeprint 에 높이를 config `print_max_height_px`(1,000) 이하로
줄이고 동기 `chart.resize()`·`update('none')`, afterprint 에 되돌린다(F 규약). beforeprint 에 다시 그린 캔버스는 PDF 에 **벡터**(차트 글자 = PDF 텍스트)로 실리고,
미리 그려 둔 캔버스는 비트맵이다 — `tests/chart_check.py` 가 둘 다 본다(벡터면 날짜·숫자 행을 PDF 텍스트에서 센다).
(4) 컨테이너(`height:…; min-width:…` div)에 `data-*` 속성이나 여분 min-width 를 HTML 로 더하면 apply.py 의 min-width 앵커(정확히 2곳)가 깨진다 →
원래 값은 JS 가 런타임에 `dataset.minwidth` 로 보관했다가 복원한다.
(5) 가로 안내 스크립트의 래퍼 감싸기(DOM 이동)는 그 박스의 scrollLeft 를 0 으로 되돌린다 → 시작 위치는 sync 뒤(load → setTimeout 0).
(6) 차트 8개가 한 `script` 요소 안에서 직렬로 만들어진다 — 앞 블록이 아직 정의되지 않은 도우미를 부르면 TypeError 로 뒤 차트 5개가 전부 빈다 →
01·06 블록은 제자리에서 PC 모양으로 만들고 큐(`window.__saeroMobileQ`)에 넣기만, 도우미는 차트 스크립트 끝에서 큐를 비운다(생성마다 try/catch — 실패하면 PC 모양).
재발 방지: `tests/chart_check.py`(precheck 밖 — 390·1280·회전·page.pdf 실물·외부 요청 CDN 2건만) · validate "레이아웃 판"(분기 표지·M 줄·matchMedia·CSS 경계) ·
`tests/test_apply.py` ApplyLayoutC.
