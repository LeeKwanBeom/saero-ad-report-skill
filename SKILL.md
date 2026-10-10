---
name: saero-ad-report
description: 새로필라테스 네이버 검색광고 주간리포트(GitHub Pages)를 CSV 4개로 갱신하고 배포한다. "광고 리포트 업데이트", "네이버광고 주간리포트", "광고 CSV 넣어줘", "주간리포트 배포", "saero report", "필라테스 광고 리포트" 같은 말이 나오거나, 네이버 검색광고 보고서 CSV(키워드/검색어/상세지역/시간대별)가 업로드되면 반드시 이 스킬을 사용할 것. 광고 성과 숫자를 리포트에 반영하거나 leekwanbeom.github.io/saero-pilates-report 를 갱신하는 모든 작업에 적용된다.
---

# 새로필라테스 네이버 광고 주간리포트 업데이트

매주 네이버 검색광고 보고서 CSV 4개를 받아, GitHub Pages에 배포된 리포트의
숫자와 문구를 갱신하고 다시 배포하는 스킬.

## 먼저 — 실행 환경(채팅 가드)

**`/home/claude`나 `/mnt/user-data`가 있는 환경(채팅 — 웹·Cowork 컨테이너)이면 아무것도 하지 말고 "PC 데스크톱 앱 Code 탭(`D:\saero` 폴더)에서 `/saero-run`으로 실행해 주세요"라고 안내하고 멈춘다.**
이 스킬은 PC Code 탭 세션 하나에서 수집부터 배포·제외 검색어 등록·기록까지 돈다(사용자 결정 2026-09-28 — 채팅은 네이버 API가 403이라 수집·등록을 못 한다).
이 PC에서 치는 방법(작업 폴더·`$PY`·사전 점검 S0·순서·멈춤·금지)은 **`references/code-tab.md`가 정본**이다. 아래 명령의 `$PY`는 저장소 밖 venv 파이썬
(`python3` 금지 — 이 PC에선 Store 스텁), 상대 경로는 작업 폴더(저장소 루트) 기준이다.

## 가장 중요한 원칙

**리포트 HTML을 새로 만들지 말 것.** 반드시 GitHub에 배포된 현재 index.html을
그대로 받아와서 "숫자와 문구만" 교체한다. 레이아웃·CSS·섹션 순서·디자인 요소를
임의로 재해석하면 매주 결과물이 조금씩 달라지고, 사장형이 익숙해진 형식이 깨진다.

이 스킬의 설명만 보고 처음부터 코딩하면 여백·문구·세부 스타일이 반드시 달라진다.
**배포본이 유일한 원본이고, 이 문서는 그 원본을 어떻게 다루는지에 대한 설명서다.**
**레이아웃 판(접기·표 순서 같은 모양)은 설계 회차·사용자 결정으로만 바꾼다** — 지금 판은 `r2026-10-F`(사용자 결정 2026-10-06·07·08·09 — 판 B 접기형 + 01·06 모바일 가로 막대(판 C) + 모바일 01·06 처음 최근 14일·펼치기 버튼(판 D) + 01 모바일 터치 날짜(판 E) + KPI 카드 넷 아래 광고비 잔액 카드(판 F), references/report-structure.md "레이아웃 판"), 배포본 `<meta name="report-layout">` = config `report_layout.layout_id` 여야 validate·deploy 가 통과한다.

## 배포 정보

- 저장소: `LeeKwanBeom/saero-pilates-report`
- 공개 링크: https://leekwanbeom.github.io/saero-pilates-report/
- 갱신 대상 파일: `index.html` (이 파일 하나가 웹페이지 전체)
- 자격 증명: **이 PC의 git 자격 증명 하나**(GCM — `credential.helper=manager`). 토큰은 대화창에서 받지 않고
  스킬·저장소에 두지 않는다(2026-09-28 Code 탭 회차에서 대화창 입력 폐지). `deploy.py --token-file`은 git 자격 증명을 못 쓸 때의
  사용자 선택(저장소 밖 한 줄 토큰 파일)일 뿐 기본 흐름에는 없다.

**쓰기 대상은 두 저장소다.**

| 쓰기 | 저장소 | 이 PC에서 |
|---|---|---|
| 리포트 배포(7단계) | `LeeKwanBeom/saero-pilates-report` | `deploy.py push` — deploy.py가 `git credential fill`로 얻은 값을 변수에만 둔다(출력·파일 0) |
| 스킬 문서·기준선·registry·**원본 보관(data/)** push | `LeeKwanBeom/saero-ad-report-skill` | `git push origin main`(ingest.sh 포함) |

채팅 운영 때의 "토큰은 용도에 따라 두 종류이고 서로 통하지 않는다"(저장소 한정 fine-grained PAT)는 **이 PC에서는 성립하지 않는다** —
git 자격 증명은 계정 로그인 하나라 두 저장소 쓰기가 같은 자격 증명으로 간다(스킬 저장소 push는 2026-09-28 실측, 배포 PUT은 첫 실사용이 첫 실측).
그래서 저장소를 가르는 관문은 자격 증명이 아니라 승인 자리와 쓰기 전 확인이다(S0의 `git push --dry-run`은 원격 인증까지,
`deploy.py push --dry-run`은 자격 증명 값을 얻은 뒤 인증 GET(읽기)으로 배포 저장소 쓰기 권한 `permissions.push`까지 — 참/거짓만 찍고 거짓이면 `[FAIL]`.
계정 역할 기준이라 토큰 범위는 PUT이 최종 확인한다).
읽기는 두 저장소 모두 공개라 자격 증명 없이 된다 — `deploy.py`는 GET을 무인증으로 먼저 보내고 403·429(무인증 rate limit,
2026-09-11·09-21·09-26 실측)일 때만 자격 증명으로 1회 다시 보낸다. push·PUT이 403이면 어느 저장소 쓰기인지 적어 사용자에게 자격 증명 확인을 요청한다.

## 설정값은 config/report-config.json 하나에서 읽는다

개업일·제외 그룹·경쟁사 목록·타겟 지역·CTR 강조 기준·차트 폭 규칙은 전부
`config/report-config.json`에 있다. 읽는 코드: `scripts/validate.py`·`compute.py`·`archive.py`·`deploy.py`·`exclusions.py`(`exclusions` 블록: 대상 그룹·금지 패턴·registry 경로)·`fetch_reports.py`(`report_fetch` 블록: 목록 URL·보고서 이름·기간 규칙·컬럼 원문·허용/금지 동작)·`leads.py`(`leads` 블록: 장부 경로·질문 문구·칸·상한·공개 범위·판정 규칙·라벨)·`place.py`(`place_checklist` 블록: 체크리스트 경로·항목 P1~P9·12번 자리 수·창·띠·상태 낱말). **값을 정의하는 자리(판정 목록·계산 기준)는
이 문서나 references에 값을 적지 않고 설정 파일의 키를 가리킨다.** validate.py도
값을 하드코딩하지 않고 그 파일을 읽는다. 값이 바뀌면 그 파일만 고친다.

설명을 위해 이름이 나와야 하는 자리(예: 왜 그 그룹이 제외됐는지, 개업일이 왜
중요한지)에는 이름을 두되 어느 키를 보라는 한 줄을 붙인다. 그런 이름은 예시이며,
실제 판단은 항상 설정 파일 값을 읽어서 한다. 둘이 다르면 설정 파일이 맞다.

작업 폴더는 PC의 저장소 clone 하나(`D:\saero\saero-ad-report-skill`, main)이고 회차 작업물은 저장소 `work/`(gitignore)에 둔다
(`work/combined/`·`work/prev.html`·`work/index.html`·`work/compute.json` — `references/code-tab.md` 1절). 입력 CSV는 수집 성공 폴더
(`fetch_reports.py` 출력 `[PASS] … → <폴더>` — config `report_fetch.download_dir` 아래 날짜 폴더)의 4개다. 경로를 하드코딩하지 말고 출력의 실제 경로를 쓴다.
**수집 CSV를 바로 계산에 쓰지 않는다** — 1단계대로 `data/`에 보관하고 합본을 만들어
2단계 이후 모든 계산·검증은 합본 4개로 한다.

## 원본 보관 — data/ (2026-09-26 도입)

보고서는 광고주센터의 `이번달`·`지난달` 프리셋으로 받는다(31일 달도 한 파일로 받아지고 두 달 전 데이터도 조회된다 —
2026-09-28 실측. "최근 30일까지만"은 직접 입력한 기간이 30일로 잘리는 것을 잘못 일반화한 옛 전제). 2026-09-26에 `최근 30일`
프리셋으로 받던 창 밖으로 개업일(8/26)이 밀려나 누적이 깨질 뻔했다. 그래서 원본을 이 저장소에 월별로 쌓고 매 회차
합쳐서 쓴다(사용자 결정 2026-09-26).

- 구조: `data/YYYY-MM/키워드.csv · 검색어.csv · 상세지역.csv · 시간대별.csv`
  (네이버 원본 그대로, 첫 줄 기간 헤더 포함. 수집 파일명은 `<이름> 보고서,2580077.csv` — 키워드 보고서는 `필라테스 보고서,2580077.csv`,
  손으로 받으면 `필라테스_보고서_2580077.csv`. 보관 이름은 종류명이고 종류는 컬럼으로 판별한다)
- **지난달**: 확정본으로 고정. 다시 받을 필요 없다.
- **이번 달**: 같은 Code 탭 세션이 `scripts/fetch_reports.py`로 매일 **이번 달 1일~어제**(매월 1일은 `지난달` 1일~말일)를 받아
  수집 성공 폴더의 4개를 그대로 1단계 `ingest.sh`에 넘긴다 — 업로드 없음(절차 `references/code-tab.md` 3절, 값 정의 `references/report-fetch.md`;
  수동 폴백 `code-tab.md` 8절: 보고서 형식에 `이번달`이 저장돼 있어 열기 → 다운로드). 같은 달 파일을 덮어쓴다.
- 달끼리 기간이 겹치지 않으므로, 날짜 컬럼이 없는 시간대별 보고서도 달별로 그냥 더하면
  누적이 된다. 이게 월별로 나누는 이유다 — "최근 30일"로 받은 파일끼리는 겹치는 날을
  시간대별에서 뺄 방법이 없다.
- **`store --chunk`(조각 추가)는 폴백**: `지난달` 프리셋은 31일 달도 한 파일로 준다(8/1~8/31, 2026-09-28 실측).
  프리셋 대신 기간을 직접 입력해 30일로 잘릴 때만, 1일~30일 파일은 그대로 두고 **말일 하루치 4개**를 따로 받아
  `store --chunk`로 조각을 더한다. combine이 조각 경계를 4종 모두 대조한다.
- 스크립트: `scripts/archive.py` (store / combine). 검사 내용은 그 파일 docstring.
- 이 저장소는 **공개**다. 원본 CSV(검색어·지역·비용 전부)가 누구나 볼 수 있는 상태로
  올라간다는 점을 도입 회차에 사용자에게 알렸다.
  **사용자 결정(2026-09-27): 공개 유지.** 비공개·절충안(data/ 분리, 계정번호 마스킹)은 채택하지 않음.

## 전체 절차

### 1단계. CSV 받기 → 보관 → 합본

받기: `"$PY" scripts/fetch_reports.py [--prev <직전 성공 폴더>]` — Code 탭은 백그라운드로(사용자 화면에 크롬 창, `references/code-tab.md` 3절).
보관·합본·push 한 번에: `scripts/ingest.sh "<수집 성공 폴더>"/*.csv`(환경 변수 `PY` = venv 파이썬) — 아래 1~3을 순서대로 실행하고
어느 단계든 실패하면 거기서 멈춘다(`set -e`). main 브랜치에서만 돌고(아니면 쓰기 전에 `[FAIL]`), store 전 **시작 검사**(쓰기 0으로 멈춤)로
HEAD = origin/main(`git fetch` 뒤) · data/ = HEAD(`git diff --quiet HEAD -- data` — 스테이징·미스테이징, 추적 안 된 파일도 0) · data/ CSV 줄바꿈 = 커밋(`ls-files --eol`)을 보고,
push 뒤와 "data/ 변경 없음" 두 분기 모두 origin/main = HEAD를 다시 읽어 확인한다. 단계를 따로 돌릴 때는 아래 명령을 쓴다.

1. 수집 파일을 보관한다(종류는 컬럼으로, 달은 첫 줄 기간 헤더로 판별):
   ```bash
   "$PY" scripts/archive.py store "<수집 성공 폴더>"/*.csv
   ```
   두 달에 걸친 파일(예: "최근 30일")과 기간 끝이 보관본보다 이른 파일(옛 다운로드)은 거부된다. 거부되면 멈추고 메시지를 보고한 뒤
   수집 재실행(평일 저장된 `이번달`, 매월 1일 `지난달` 프리셋)이나 수동 폴백(`code-tab.md` 8절)을 사용자와 정한다.
   `--force`·`--chunk`는 자동으로 붙이지 않는다. 수집 성공 폴더 밖(`partial/` 등)은 넘기지 않는다.
2. 합본을 만든다. **FAIL이면 멈추고** 메시지대로 사용자에게 확인한다:
   ```bash
   "$PY" scripts/archive.py combine work/combined
   ```
3. 합본이 PASS면 **계산 전에 보관본부터 push**한다(`git push origin main` — 이 PC git 자격 증명). 세션이 끊겨도
   원본이 남게 하기 위해서다. 커밋 메시지에 달·기간을 적는다.

이후 단계의 "키워드 CSV" 등은 전부 `work/combined/키워드.csv` 등 합본을 뜻한다.

받아야 할 파일과 용도:

| 보고서 | 담당 섹션 | 주요 컬럼 |
|---|---|---|
| 키워드 보고서 | KPI, 01~06, 10~12 | 캠페인/광고그룹/키워드/일별/매체이름/PC·모바일/검색·콘텐츠/노출수/클릭수/클릭률/평균CPC/총비용/평균노출순위 |
| 검색어 보고서 | 07 | 검색어/검색 유형/일별/노출수/클릭수/총비용 |
| 상세지역 보고서 | 08 | 상세지역/일별/노출수/클릭수/총비용 |
| 시간대별 보고서 | 09 | 시간대별/노출수/클릭수/클릭률/평균CPC/총비용 |

모든 CSV는 첫 줄이 기간 헤더이므로 `pandas.read_csv(path, skiprows=1)`로 읽는다.

4개 중 하나라도 없으면 combine이 FAIL로 멈춘다(조각 경계 불일치, `archive.py` combine 검사) — 빠진
보고서를 받아 store한 뒤 다시 combine한다. **부분 갱신 경로는 없다**(2026-09-26 D-13: 옛 "직전 데이터로
두고 나머지만" 경로는 합본 방식과 양립하지 않아 삭제).

"지역 보고서"(시/도 단위)와 "요일별 보고서"는 받을 필요 없다.

### 2단계. 집계 기간 검증 — 여기서 멈추고 확인

1단계 combine이 이 검증을 한다: 날짜 있는 3종 합본의 `일별` 최솟값 = config
`open_date`, 달 조각이 빈틈·겹침 없이 이어짐, 조각마다 시간대별·상세지역 노출 합계 =
키워드 노출 합계(시간대별은 날짜 컬럼이 없어 기간을 이것으로 확인한다). 6단계
validate.py 검사 3(시간대별 클릭 합계 = 키워드 전체 클릭)도 그대로 돈다.
**헤더의 기간만 보고 판단하지 말 것** — 헤더가 넓어도 실제 데이터는 개업일부터인
경우가 있고(8월 파일 헤더는 08.01인데 데이터는 08.26부터) 그 반대도 있다.

combine이 FAIL이면 **작업을 멈추고** 메시지 원문을 보고한 뒤 다음 행동을 사용자와 정한다. 흔한 경우:

> 합본 검사가 멈췄습니다: <메시지 원문>. 이번 달 파일의 기간이 기대(**이번 달 1일 ~ 어제**)와 다른 것 같습니다.
> 수집을 다시 돌릴까요(평일은 저장된 `이번달`, 매월 1일은 `지난달` 프리셋)? 아니면 손으로 받은 4개로 폴백할까요(`code-tab.md` 8절)?

월초 회차를 놓쳐 지난달 말일 구간이 비면 평일 수집(`이번달`)으로는 채울 수 없다 — 지난달 4개를 `지난달` 프리셋으로 받아 폴백으로 넣는다.

### 2-1단계. 배포본이 이미 최신인지 먼저 확인 — 재계산·교체 전에 멈춘다

**전 섹션을 재계산하기 전에** 배포본을 한 번 열어 기간부터 대조한다.
같은 CSV를 다시 올리는 일이 실제로 있었고, 그때 전부 계산한 뒤에야 알았다.
배포본은 4단계 fetch를 **이 단계 앞으로 당겨** 받고, 대조용으로 `compute.py`(계산만 — 쓰기 = `work/compute.json`)도 당겨 돌린다
(읽기·계산이라 부작용 없음 — 단계 번호는 그대로. 교체(5단계)·제외 그룹 판정·제외 검색어 후보는 이 대조 뒤에).

1. 배포본 `work/prev.html`의 masthead `집계 기간`을 읽는다 (`집계 기간<b>...</b>`)
2. 키워드 CSV `일별`의 min·max와 대조한다 — `compute.py`(계산만, 쓰기 = `work/compute.json`)의 `masthead` 문자열과 비교하면 형식까지 같다

기간이 **다르면** → 새 데이터다. 3단계로 진행한다.

기간이 **같으면** → 이미 반영된 데이터일 가능성이 높다. 3단계·5-0단계(pull·propose)로 가지 말고 이 질문 하나만 곧바로 묻는다:

> 배포본 집계 기간이 이번 CSV와 같습니다(2026.08.26 — 09.06). 이미 반영된
> 데이터로 보이는데, 그래도 다시 계산할까요? 아니면 새 기간으로 CSV를
> 다시 받으시겠어요?
> (직전 회차 기록이 "등록 미룸"일 때만 덧붙인다) 아니면 미뤄 둔 제외 검색어 등록만 할까요?

답을 받기 전에 5단계로 넘어가지 않는다.
2-1 기간이 같으면 승인 묶음 ⓐ와 별개의 앞 질문 하나만 하고 답을 기다린다 — 답 "다시 계산" → 3 → 5-0a → ⓐ(해당만) → 5-0b(해당 시) → 5-0c → 5 → 6 → 7 → 8 /
"CSV 다시" → ① / "미룬 등록만"(직전 회차 기록이 "등록 미룸"일 때만) → 3 건너뜀 → 5-0a(`--since` = 미룬 회차 창 시작) → ⓐ → 5-0c → 5(07·11·12 문구만) →
6(`--pending` 없이, 3번째 인자 = 이번 4단계 fetch) → 7 → 8. (단계 번호·ⓐ는 `references/code-tab.md` 3절 순서표.)

### 3단계. 제외 그룹 확인

집행이 멈춘 광고그룹은 KPI·01~07·10번 집계에서 제외한다. 상세 판정 규칙은
아래 "제외 그룹 판정"을 따른다. 새로운 후보가 감지되면 **멈추고 확인한다.**

### 4단계. 현재 배포본 가져오기

```
"$PY" scripts/deploy.py fetch --out work/prev.html   # 직전 배포본 — 손대지 않는다(2-1 앞으로 당겨 받는다)
cp work/prev.html work/index.html                    # 작업본은 이 사본
```
`prev.html`은 5단계 compute의 `--competitors-html`과 6단계 precheck.sh 3번째 인자로 그대로 쓴다(작업본을 넣으면
작업본의 경쟁사표가 정본이 돼 검사가 무력화된다 — 2026-09-27 검증 (c)).
(내부는 `GET https://api.github.com/repos/LeeKwanBeom/saero-pilates-report/contents/index.html`을 무인증으로 먼저 보내고,
403·429(무인증 rate limit — 2026-09-11·09-21·09-26 실측)면 이 PC git 자격 증명으로 1회 다시 보낸다. 응답의 `sha`를 출력하고
`content`를 base64 디코드해 저장한다.)

**GET이 자격 증명으로도 안 되면 `git clone -c core.autocrlf=false https://github.com/LeeKwanBeom/saero-pilates-report`로 받는다(진단·검증 회차도 같다 — 바이트 그대로).**

### 5-0단계. 제외 검색어 — 후보·승인·등록·확인·기록 (2026-09-27 도입, `scripts/exclusions.py`)

파워링크 3그룹 "확장 검색" 칸의 제외 검색어를 **묻지 않고 판정하고, 승인 뒤에만 등록하고, 등록 뒤 다시 읽어 확인하고, 기록**한다.
값 정의·API·UI 실물·registry 스키마·판정 규칙은 전부 `references/exclusion-ui.md`(문서 = 코드). 대상 그룹·금지 패턴·registry 경로는
config `exclusions`. 등록 상태의 기계 정본은 `audit/exclusions.csv`(registry) — **"이미 등록했었냐"를 사용자에게 묻지 않는다.**

```bash
"$PY" scripts/exclusions.py propose work/combined --since YYYY-MM-DD   # 후보·재노출 판정·승인 문구 — registry·계정 쓰기 0,
                                                    # work/exclusions_proposal_<창시작>_<창끝>.md·_candidates.txt·_industry.txt·.md5(출처 기록 — push가 대조)를 쓴다
"$PY" scripts/exclusions.py push --from-candidates work/exclusions_proposal_<창시작>_<창끝>_candidates.txt [--drop …] \
  [--industry …_industry.txt --industry-lines …] [--extra-csv work/combined/검색어.csv --extra-rows …] --expect N --dry-run
                                                    # 승인 뒤 할 일 목록만(호출 0) — 참조 선택 모드(references/code-tab.md 6절)
"$PY" scripts/exclusions.py report                  # registry 요약
```
propose `--since` = 직전 배포 masthead 끝 + 1일(ISO). 직전 회차 기록이 "등록 미룸"이면 그 회차 propose 창 시작(lo) — 미룬 이름과 새 이름을
한 묶음으로 올린다(first_seen 필터 때문에 끝 + 1일로는 미룬 이름이 다시 안 오른다). 창 안 검색어 행이 0이면(`--since`·`--day`가 데이터 끝 뒤 등) `[주의] 빈 창` — 재등록 후보만 쓴다.
1. **재노출 판정**(propose 출력 "재노출 판정"): 등록 이력이 있는 이름이 `확장` 행에 잡히면 registry로 판정해 셋 중 하나로 **보고만** 한다 —
   "등록돼 있는데도 노출"(등록일·노출일 명시, 원인은 "~일 수 있음") / "등록 누락 → 후보"·"일부 그룹 미등록 → 후보"(다음 승인 목록에 자동 포함) /
   "미확인" = registry 파일이 없거나 못 읽은 회차 — 이때 propose·push·verify는 `[FAIL] registry 없음 … (미확인)` exit 1로 **멈추고 아무 후보도 내지 않는다**
   (빈 registry로 판정하면 이력 있는 이름이 신규 후보로 올라오므로; 8단계 양식의 "미확인 c"는 그 회차 표시). 등록 당일은 판정하지 않고, 정확 일치·`확장` 행만 본다(현행 규칙 유지).
   어느 경우도 탭 목록 확인을 요청하지 않는다. 등록·확인에 **실패한 이름(`failed`)은 재노출이 없어도 다음 propose 재등록 후보에 실패 사유와 함께 다시 오른다** — 반복 실패(문자 제한 등)는 registry `status=keep`으로 사용자가 뺀다.
2. **후보 제시**: 신규 후보(클릭 0·첫 등장·금지 패턴·경쟁사·업종어 아님)는 무관/애매/키즈로 분류해 채팅에 제안(결정은 사용자), 재등록 후보(registry 미등록·일부 누락)는 그대로,
   "업종어 포함"(config `industry_terms`)과 "후보에서 뺀 것"(`never_exclude_patterns`·`competitors`)은 이유와 함께 보이기만 한다.
3. **승인 문구**는 propose 출력 마지막 절을 그대로 붙인다(전체 이름에 번호 — 번호 = `_candidates.txt` 줄, 제안서 업종어 절 번호 = `_industry.txt` 줄).
   답 예: "등록 승인 12개"(N은 숫자로 쓴다) · "3 빼고"(→ `--drop 3`) · "업종어 2 넣기"(→ `--industry …_industry.txt --industry-lines 2`) — 세션은 답의 번호를 그대로 옮긴다. **답이 오기 전에는 등록하지 않는다**(아래 "승인이 필요한 지점" (4)).
   N을 숫자로 쓰지 않았거나("등록 승인 N개" 글자 그대로) "위 2가지만"처럼 둘 이상으로 읽히면 세션은 글자에 가장 가까운 해석의 `push … --dry-run` 목록(`[승인 목록] N개`·이름)을 보이고
   다른 해석을 한 줄로 붙여 되묻는다 — 확인 답 전에는 실제 push 0(2026-09-29 실측, `references/code-tab.md` 6절).
4. **등록·확인**: `pull`·`push`·`verify`는 **PC 작업 폴더를 연 Code 탭 세션**이 같은 폴더에서 돌린다(API 호스트가 열린 PC 로컬 셸 — references/exclusion-ui.md 3절,
   2026-09-28 실측). 실제 등록은 **push 참조 선택 모드만** 된다 — push가 원천(`_candidates.txt`·`_industry.txt`·합본 `검색어.csv` `검색어` 칸)에서
   줄·행 번호로 이름을 직접 읽고(실제 push만 — pull 재검사를 통과한 뒤 첫 POST 전에 — `work/approved_<날짜>_<시분초>.txt`를 남긴다 — dry-run은 화면만), 세션은 번호와 N만 넘긴다
   (`--expect` = 답의 N — N이 없는 번호 답("3 빼고"·"업종어 2 넣기")이면 세션이 목록 수에서 계산하고(− 뺀 수 + 넣은 수), 실제 push 전에 dry-run의 `[승인 목록] N개`와 이름을 사용자에게 보인다)
   (이름을 쓰지 않는다 — 기호·마침표 원문 그대로). 후보·업종어 파일은 `work/` 밑·같은 propose 실행이어야 하고 propose가 쓴 출처 기록(`<창 이름>.md5` —
   파일·합본·registry md5)과 지금이 같아야 한다. 합계 ≠ N·범위 밖·빈 원천·중복·고른 이름 중 하나라도 이미 registered·keep·금지 패턴·경쟁사명은 쓰기 전 `[FAIL]`,
   실제 push는 pull 뒤 고른 이름 중 하나라도 대상 그룹 전부에 이미 있으면 POST 0 `[FAIL]`(승인 파일 안 씀), 기호만 다른 쌍둥이는 `[주의]`
   (`references/code-tab.md` 6절, 2026-09-28 "노원힐링장소." 사례). push의 `--approved <파일>`은 dry-run·시험 전용(verify의 `--approved`는 재개 판정용).
   키 파일은 `--key-file ~/naver-api.keys.json` 경로만 넘기고 열지 않는다. push는 pull → 그룹별로 없는 이름만 POST →
   verify(다시 읽어 3그룹 확인)까지 한 번에 하고, 확인 안 된 이름은 `failed`(성공이라고 쓰지 않는다). 부분 실패는 그룹×이름으로 보고, 재시도는 사용자 결정.
   요청 도중 끊기거나 응답을 못 읽으면(`요청 결과 모름` — 반영됐을 수 있다) 그 묶음은 `failed`로 두고 verify가 실제 상태를 다시 읽으며, 어떤 예외에도 registry는 저장된다
   (다시 읽은 목록에 전부 있으면 끝 줄 `… 전부 있음 — … 재시도 안 함` exit 1 — 등록은 됨) —
   재개·확인은 `verify --key-file … --approved <이번 회차 propose(.md5) 뒤에 생긴 가장 최근 work/approved_*.txt>`(없으면 이번 회차 push는 POST 전 · `--approved` 없는 verify의 "pending 0"은 판정이 아니다).
   push는 그룹별 `현재 N + 등록 예정 M`을 찍고 config `max_per_group`(950 추정) 초과 예상이면 `[주의]`만 낸다(차단 안 함 — 3716 오류는 항목별 `failed`로 남고 재승인 대상). `delete`도 `--confirm` 없이는 돌지 않는다.
5. **기록**: registry가 정본. `audit/last-audit.md` "등록 제외 검색어 대조 목록" 표에는 **회차별 요약 행만**(등록 n · verified n · 실패 n · description). 07번 각주·12번 1번에는 판정 결과 문구 그대로.
6. 시험 등록(`test-roundtrip`, 1건·사용자 입회·등록→확인→삭제)은 **구현 회차 끝**(과 API 키가 바뀐 뒤)에만 한다. 검증 회차는 그 기록(출력 원문·registry `deleted` 행)을
   대조하고 가짜 API 시험(`tests/test_exclusions.py`)을 돌린다 — 실제 계정에 다시 쓰지 않는다. 진단 회차는 propose·report·`--dry-run`만.

### 5단계. 전 섹션 재계산·교체

`references/report-structure.md`를 읽고 12개 섹션을 순서대로 갱신한다.
**숫자는 `scripts/compute.py` 출력값만 쓴다 — 즉석 계산 금지.**

```bash
"$PY" scripts/compute.py work/combined --competitors-html work/prev.html -o work/compute.json
```
(`--competitors-html`은 4단계의 직전 배포본 `prev.html` — 작업본 `index.html`을 넣지 말 것.)

키는 report-structure.md 절 번호("KPI","01"~"10")이고 자리마다 값이 있다. 계산 정의는
report-structure.md 각 절의 "정의(compute.py)" 줄과 1:1이다 — 둘이 어긋나면 둘 다 고친다.
`--competitors-html`의 07번 경쟁사표가 경쟁사 집합의 정본이고, 출력의 `신규변형후보`(config 이름을
포함하는데 직전 표에 없던 검색어)는 사람이 표기 변형 행으로 추가한다. 11·12번은 계산 대상이 아니다.
예외: **11번은 12번을 확정한 뒤 맨 마지막에 쓴다** — 12번에서 완료·철회로
결정된 항목을 11번이 "미반영"으로 서술하는 모순을 막기 위해서다(11번·12번
"작성 기준" 참고).

교체는 잔액 읽기 + 두 단계(2026-10-06 — E2 저장소화 · 서술 표지 · 레이아웃 판 / 2026-10-09 판 F 광고비 잔액 카드 — 앞 두 줄):
```bash
"$PY" scripts/balance.py --key-file ~/naver-api.keys.json                              # 광고비 잔액(비즈머니) GET 1회(읽기) → work/balance.json — 실패해도 exit 0(카드 "확인 못 함")
"$PY" scripts/compute.py work/combined --competitors-html work/prev.html --balance work/balance.json --leads "$("$PY" scripts/leads.py path)" --place "$("$PY" scripts/place.py path)" -o work/compute.json   # 잔액 카드 값("잔액")·성과장부·플레이스전후까지 — 잔액 기록이 없거나 지난 회차 것이면 [FAIL] exit 1
"$PY" scripts/apply.py --layout --html work/index.html --compute work/compute.json   # 기계 자리(KPI·잔액 카드·표·목록·차트·masthead·og·접기 summary) + 레이아웃 판 — 앵커가 하나가 아니면 [FAIL] exit 1, 작업본 그대로
"$PY" work/n<날짜>.py                                                                  # 서술 — 저장소 밖 스크래치, 표지마다 rep('<자리>', 새 문장)
```
**광고비 잔액 카드(판 F)**: `balance.py` 는 네이버 검색광고 API `GET /billing/bizmoney` 를 한 번 읽어(서명·키는 exclusions.py 의 NaverApi·load_keys 그대로 — 키 파일은 경로만)
`work/balance.json` 에 원 단위 버림 값과 읽은 시각(KST)을 쓴다. 시작하자마자 옛 기록을 지우고, 조회가 실패하면(키 파일·네트워크·401/403·5xx·응답 꼴 다름) 실패 기록을 쓰고 exit 0 —
카드는 `확인 못 함` · `M/D(요일) HH:MM 조회 실패`(옛 값을 새 시각으로 보이지 않는다, 회차는 멈추지 않는다 — 사용자 결정 2026-10-09). 성공이면 카드 값 `217,817원` · 보조 줄
`10/9(금) 14:34 기준 · 약 24일분`(며칠분 = 잔액 ÷ 집계 마지막 날까지 7일 평균 총비용, 버림 — 평균 0 이면 생략). compute 는 읽은 날(KST)이 집계 마지막 날 이하인 기록(지난 회차 것)을
`[FAIL]` 로 멈추고, apply 는 compute.json 에 "잔액" 이 없으면(5a 의 `--balance` 없는 compute 그대로) `[FAIL] apply: … "잔액" 없음` 으로 멈춘다 — 세 줄은 이 순서로 매 회차(2-1 같음 경로 포함).
세션은 `work/balance.json` 을 손으로 쓰거나 고치지 않는다(다시 읽으려면 balance.py 를 다시 — 그 뒤 compute·apply 도 다시).
**매출 작업 A·C(2026-10-10 — 주간 성과 장부 + 플레이스 화면 손보기, 새 외부 쓰기 0 · 네이버 호출 0)**: 3단계 뒤 `leads.py status`·`place.py status`(읽기)가 (5) 지난주 숫자 · (7) 지난주 플레이스에서 바꾼 것 ·
C 첫 회 9항목을 물을지 정하고(질문은 ⓐ 묶음 끝의 **정보 질문** — 답이 없으면 미입력/바꾼 것 없음으로 진행, `references/code-tab.md` 3절 3a·3b·4절), 답이 오면 `leads.py add|skip`·`place.py set|done`(dry-run → 실제, 줄 추가만)이
장부(config `leads.path` — 저장소 밖, 공개 안 함)·체크리스트(config `place_checklist.path` — 저장소, 공개)에 쓴다. compute 의 "성과장부"는 config `leads.publish` = verdict 라 **판정 낱말·'M/D까지'·입력 주 수만**(건수·매출은 없음),
"플레이스전후"는 12번 플레이스 행(✗ 항목 · 바꾼 항목의 효과 판정 — 플레이스 검색 지면만·달력 일수·띠 `band_pct` 밖일 때만 좋아짐/나빠짐)과 채팅 질문 신호·이월 줄. 12번 행 꼴은
`references/report-structure.md` 12번 작성 기준 6). 장부 숫자·(5) 답 원문·캡처 숫자는 리포트·last-audit·커밋 어디에도 쓰지 않는다(공개 저장소·공개 배포본 — validate "장부 라벨+숫자 0"·`leads.py guard`).
`--layout` 은 **매 회차 붙인다**(멱등): 작업본이 이미 레이아웃 판(meta = config `report_layout.layout_id`)이면 변환을 건너뛰고 값만(분기 도우미의 M 줄 포함),
meta 없는 옛 판이면 사슬(meta + 접기 5개 뼈대 = r2026-10-B → 01·06 모바일 분기 = r2026-10-C → 모바일 기간 접기 = r2026-10-D → 01 모바일 터치 날짜 = r2026-10-E → 광고비 잔액 카드 = r2026-10-F),
meta r2026-10-B·C·D·E 판이면 사슬을 따라 r2026-10-F 로 바꾼 뒤 값.
`--layout` 없이 옛 판이면 `[FAIL] apply: ApplyError: 레이아웃 판 meta 없음 — --layout …`, B·C·D·E 판이면 `… 레이아웃 판 meta r2026-10-E ≠ config r2026-10-F — --layout …`(B·C·D 도 같은 꼴),
meta 가 사슬 밖의 값이면 FAIL(판 변경은 설계 회차 몫). 03 은 합계 맨 위 + 최근 `recent_days`(7)일 최신 위,
나머지 날짜는 접힌 표에 최신 위. **접기 머리(summary)의 개수·날짜(03 "이전 N일(M/D~M/D)" · 07 "(N개 · 펼치기)" · 경쟁사 "표 N행" · 08 "(N개 지역·클릭 M건)")는 apply 가 compute.json 으로 매 회차 쓴다**
— 서술 스크립트는 summary·details 를 건드리지 않는다.
서술 자리 이름·종류(매회차/고정)·compare 가 읽는 문구는 `references/report-structure.md` "서술 표지" 표가 정본이고, 글 길이는 같은 문서 "서술 공통 규칙"과
각 절 "길이" 줄(숫자 한 줄 + 결론 한 줄 · 날짜 박힌 판정·등록 이력은 리포트에서 빼고 정본 표에). 매회차 표지를 빠뜨리면 6단계 narrative 가 `[FAIL] 서술 미교체`로 멈춘다.
직전 배포본에 표지가 없는 첫 적용 회차만 n<날짜>.py 가 표지를 먼저 넣는다(같은 표 아래 문단).

날짜·기간이 들어간 텍스트도 함께 갱신한다(아래 "매번 함께 바꿔야 할 텍스트").

### 6단계. 검증

한 번에: `scripts/precheck.sh work/index.html work/combined work/prev.html [--pending]`(환경 변수 `PY` = venv 파이썬)
— 아래 넷을 순서대로, 하나라도 실패하면 멈춘다. validate·compare는 통과면 끝 3줄(요약 `검사 N개: PASS … / FAIL 0` 포함), 실패면 전체 출력을 보인다.
compute.json은 작업본 옆(`work/compute.json`)에 쓴다(판 F — 작업본 옆 `work/balance.json` 을 validate·compute 에 `--balance` 로 넘긴다). 3번째 인자는 **4단계 fetch 파일(직전 배포본)** 이 필수이며 작업본과 md5가
같으면 "[FAIL] 직전 배포본이 작업본과 같다 — …"로 exit 1. `--pending`은 validate에만 넘어간다. 전부 통과하면 작업본 옆에
도장 `work/precheck_ok.md5`(1줄 작업본 md5 · 2줄 직전 배포본 md5 · 3줄 `mode full|pending`)를 쓴다 — 7단계 실제 push는 작업본 md5 = `--file`·
직전 배포본 md5 = `--base`일 때만 PUT한다(pending이면 `[주의]`만). 인자 수가 맞으면 무엇보다 먼저(파일 없음 FAIL에도) 옛 도장을 지우고, 작업본 md5를 시작·끝에 재 다르면
`[FAIL] 작업본이 precheck 도중 바뀜`(도장 없음). 작업본·직전 배포본 파일이 없으면 `[FAIL] 파일 없음` exit 2.
진단 회차의 재현 시험(작업본 = 현재 배포본)은 3번째 인자에 **그 배포본의 직전 배포**(예: ad48222 → 4c08ab3)를 넣는다.

1. `scripts/validate.py`(독립 검산 — 태그 짝·클릭수·CTR 강조·top5·카드·경쟁사·11·12번 등, 아래 "배포 전 검산")
   ```bash
   "$PY" scripts/validate.py <작업중인 index.html> <키워드CSV> <검색어CSV> <시간대별CSV> <상세지역CSV> [--pending] [--balance work/balance.json]
   ```
   `--pending`은 사용자 답을 기다리며 채팅 질문을 남긴 채 배포하는 회차에만 붙인다(07 각주·11·12번 잔존 문구 검사 21만 허용,
   건수는 그대로 출력). 답을 반영한 재배포에는 붙이지 않는다. 잔존 문구를 보는 자리는 이 검사 하나뿐이다(compare.py에 없음).
2. `"$PY" scripts/compare.py <작업중인 index.html> <compute.json>` — 배포본 값이 compute.py 출력과 **차이 0**인지
   (2026-10-06 회차 2 기준 99항목: 표·차트 배열·각주·section-desc 숫자·11번 항목 수·금칙어 95 + 접기 summary 4(07 클릭 1건·클릭 0·경쟁사표 개수 = 목록 길이,
   03 "이전 N일(M/D~M/D)" = 접힌 표) · 2026-10-10 매출 작업 A·C **101항목**(+ 12번 `장부 기준 판정 = X` = 성과장부.판정 · 12번 플레이스 행 = 플레이스전후.12번).
   03 일별 표는 두 표를 이어 읽어 거꾸로 = 오름차순(최신 위가 정본 — 오름차순으로 되돌린 판은 DIFF).
   09-27 의 95 는 09-26의 99에서 잔존 문구 5항목을 validate 검사 21로 일원화하고 08 컴팩트를 집합+정렬 2항목으로 나눈 것. 경쟁사표 정본은 3번째 인자의 직전 배포본.
3. `"$PY" tests/overflow_check.py <작업중인 index.html>` — 360·390·430px 가로 넘침 0(css-and-layout.md 버그 기록 10). file:// 밖 요청은 막고 잰다(Chart.js 미로드 — checklist [의도된 동작] 17).
   재기 전에 접기(details)를 전부 연다(2026-10-06 — 접힌 안의 표·목록까지).
4. (2026-10-06) `"$PY" scripts/narrative_check.py <작업중인 index.html> <직전 배포본>` — 매회차 서술 표지 블록이 직전 배포본과 바이트가 같으면
   `[FAIL] 서술 미교체 <자리>`(compare 가 숫자를 읽지 않는 서술이 지난 회차 그대로 배포되는 것 — 10/6 01 머리글 유형). 같은 기간(2-1 같음)·직전 배포본에 표지 없음(첫 적용)은
   `[주의]`로 생략, 작업본 표지 0 은 FAIL(references/report-structure.md "서술 표지").

하나라도 실패하면 배포하지 말고 원인을 찾아 고친 뒤 다시 실행한다.

### 7단계. 배포

```bash
"$PY" scripts/deploy.py push --file work/index.html --base work/prev.html --message "리포트 갱신: <기간>" [--dry-run]
"$PY" scripts/deploy.py verify --file work/index.html --ref <push가 찍은 커밋>   # 그 커밋의 재수령본 md5 = 로컬
```

**자동 배포(사용자 결정 2026-09-30 — "물어봐야 하는 거 다 물어보면 자동으로 배포까지")**: 배포 질문은 따로 하지 않는다. 사람 질문(2-1 같음 · 승인 묶음 ⓐ · 모호한 답 되묻기 · 등록 실패 재시도 등 `references/code-tab.md` 4절 ⓐ)에 **모두 답을 받아 남은 질문이 없고**, 6단계 precheck 통과(도장)와 7단계 `--dry-run` 통과(도장·base 대조·자격 증명·쓰기 권한 참)면 같은 명령을 dry-run 없이 바로 돌려 PUT → `verify --ref`까지 간다.
검사가 하나라도 `[FAIL]`·exit ≠ 0이면 PUT 없이 멈추고 보고한다(자동 재시도 금지 그대로). 등록이 exit 1(부분 실패·요청 결과 모름)이면 재시도 질문이 남은 것이라 배포도 그 답 뒤로 미룬다.
사용자가 그 회차에 "보류"·"오늘 배포 안 함"이라고 했으면 PUT 없이 기록하고 끝낸다(8단계 기록·마감이면 wrapup, 배포 커밋 칸에 `보류(사용자 답 "<원문>")`). (옛 규칙 — 2026-09-29 "배포할까요? — 배포 / 보류" 고정 질문 — 은 이 결정으로 대체.)

**레이아웃 판 게이트(2026-10-06 회차 2)**: 실제 push 는 `--file`·`--base` 의 `<meta name="report-layout">` 가 다르면(한쪽 없음 포함) `--layout-change` 없이
`[FAIL] 레이아웃 판이 바뀜 — PUT 안 함` exit 1(네트워크 전 — GET·PUT 0), `--dry-run` 은 `[주의] 레이아웃 판이 바뀜 — 실제 push 에는 --layout-change`. 같으면 아무 문구 없이 지나간다
(데이터 회차엔 안 걸림 — 위 자동 배포 결정과 충돌 0). `--layout-change` 는 **레이아웃 판 첫 적용 회차에 사용자가 작업본(과 전후 비교 페이지)을 보고 "배포"라고 답했을 때만** 붙인다
(첫 적용은 "보류로 시작 — 6단계 도장까지만" → 사용자 확인 → "배포" → `push … --layout-change` → `verify --ref`). 데이터 회차에서 이 FAIL 이 나면(병합 뒤 첫 적용 전에
데이터 회차가 먼저 돈 경우) PUT 0 으로 멈추고 사용자에게 묻는다 — 세션이 스스로 `--layout-change` 를 붙이지 않는다.

**verify는 `--ref <push가 찍은 커밋>`으로** — push 성공 줄(`배포 완료 커밋 <sha> …`)과 다음 줄(`다음(읽기): deploy.py verify … --ref <sha>`)의 값.
ref 없는 contents GET은 PUT 직후 약 1분 옛 본문을 돌려줄 수 있다(2026-09-29 실측 2회 — 요청의 no-cache로도 안 막힘). `--ref`는 `?ref=`로 그 커밋의 본문을 받는다(16진 7~40자, verify 전용 — 아니면 GET 전에 exit 2).

`push`는 배포 직전에 `sha`를 **다시 조회**한 뒤 PUT한다(4단계 이후 값이 바뀌었을 수 있다). 그 조회 본문이 `--base`(4단계 fetch 파일)와
md5가 다르면 `[FAIL] 배포본이 4단계 fetch 뒤 바뀜` exit 1로 PUT하지 않는다 — 그 사이 다른 배포가 있었다(4단계부터 다시 할지는 사용자). 실제 push는
`--base` 필수(없으면 exit 2), 6단계 도장(`work/precheck_ok.md5`)의 작업본 md5 = `--file`·직전 배포본 md5 = `--base`일 때만 PUT(아니면
`[FAIL] precheck 통과본이 아님` exit 1 — precheck 뒤 작업본을 고쳤으면 6단계부터, 4단계를 다시 받았으면 5·6단계부터). PUT 409 = `[FAIL] 배포본이 GET 뒤 바뀜(sha 불일치)`,
403 = 쓰기 권한 없음, 404 = 저장소·경로, 요청 도중 끊김·5xx = `[FAIL] PUT 결과 모름(…) — 반영됐을 수 있다. 재PUT 금지, 먼저 deploy.py verify` — 자동 재시도 금지.
GET 본문이 `--base`와 다른데 작업본과 같으면 "앞 PUT이 이미 반영됨" exit 0(PUT 안 함 — verify로 확인). 인자 오류(`--file`·`--out` 없음)는 GET 전에 exit 2.
`--dry-run`은 도장(없으면 `[주의]`)·sha 조회·base 대조·자격 증명 확인(`자격 증명 확인됨(출처: git)`)·쓰기 권한 확인
(인증 GET으로 `permissions.push` 참/거짓, 거짓이면 `[FAIL]` — 계정 역할 기준, 토큰 범위는 PUT이 최종 확인)·본문 준비까지만 하고 PUT을 보내지도 파일을 쓰지도 않는다(2026-09-26 실측). 내부는
`PUT https://api.github.com/repos/LeeKwanBeom/saero-pilates-report/contents/index.html`
`body: { "message", "content": <base64>, "sha": <최신 sha> }`. PUT 자격 증명은 deploy.py가 이 PC git 자격 증명(`git credential fill`)에서 얻어
변수에만 둔다 — 출력·파일·로그 0, 세션이 직접 조회하지 않는다(`--token-file`을 주면 그 파일).

**verify가 불일치(exit 1)면 멈춘다** — 재PUT 금지. ref 없이 돌린 verify면(`[FAIL] 불일치 — PUT 직후라면 캐시일 수 있다`) `git ls-remote https://github.com/LeeKwanBeom/saero-pilates-report HEAD`와
`--ref <push가 찍은 커밋 — 없으면 그 HEAD>`로 다시 verify(읽기)한다. `--ref`로도 불일치(`커밋 고정 조회라 캐시 아님`)면 재수령본 sha·md5를 보고하고, 다시 PUT할지는 사용자가 정한다(자동 재PUT 금지).

반영까지 1~2분 걸린다는 점과 공개 링크를 함께 안내한다.

보관본(`data/`)은 1단계에서 이미 push했다. 배포 후 audit 기록 push 때 `git status`로
`data/`에 안 올라간 변경이 없는지 한 번 더 본다.

### 8단계. audit 기록 (갱신 회차 기록 양식 — 2026-09-26 개정안 8)

`audit/last-audit.md`의 갱신 회차 절에 아래를 적고 스킬 저장소에 push한다(같은 회차에 config가 바뀌었으면 함께, 5-0단계 pull로 바뀐 registry가 아직 커밋 안 됐으면 그것도 — 경로 지정 add).

```
## YYYY-MM-DD 갱신 회차 (진단 아님 — 리포트 배포 회차)
합본 `일별` ~ (N일) · 배포 커밋 <해시>(직전 <해시>, 파일 sha a → b) · 집계 기간 `…`
validate.py 검사 N개 전부 PASS(precheck가 보이는 요약 줄 `검사 N개: PASS N / FAIL 0`의 N — [PASS] 줄을 세려면 validate.py를 따로 돌린다) · compare.py 차이 0(항목 M, 직전 배포본 인자 <해시>) · overflow 360/390/430 넘침 0 · 재수령본 md5 일치
`--pending` 사용: 아니오/예 — 채팅 질문 N건(예이면 답을 반영한 재배포에서 `--pending` 없이 다시 PASS했는지도 적는다)
**효율: 벽시계 __분 · 도구 호출 __회 · 즉석 코드 __행**(compute/compare 밖에서 새로 쓴 코드 — 0이 목표)
2-1단계 선확인 / 제외 그룹 신규 후보 / 01·06 min-width·라벨 / 11번 판정(유지·뒤집힘·근거 소멸) / 12번 이월 판정 / 경쟁사·제외 검색어 대조 / 사용자에게 요청한 값 / 다음 회차 대조
제외 검색어(5-0단계): 재노출 판정 n건(등록돼 있는데도 노출 a · 등록 누락 b · 미확인 c) / 후보 n → 승인 n → 등록 n · verified n · 실패 n(description) / registry 행수
propose 창 lo~hi · 등록 미룸(사용자): 아니오/예(미룬 이름 n — 다음 회차 `--since` = lo)
매출 작업: (5) 장부 입력됨(로컬)/건너뜀/미입력 · 장부 판정 = <낱말> · (7) P<n> M/D 바꿈/없음 · 12번 플레이스 행 <P 번호> · 채팅 질문 신호 <n> — 답 원문·장부 숫자·캡처 숫자는 적지 않는다(공개 저장소)
```
스킬 저장소 커밋 전(이 8단계 · 5-0c registry · config 커밋 · **마감(wrapup) 커밋 전에도**) `"$PY" scripts/leads.py guard --staged --message-file <메시지 파일>` 을 돌려 통과(`[PASS] guard`)일 때만
`git commit -F <같은 파일>` — staged 추가 줄(audit/·config/·references/·local/·루트 *.md)·커밋 메시지에 장부 라벨+숫자·장부 머리줄·최근 매출 값이 있으면 `[FAIL]` 커밋 0(`references/code-tab.md` 4절 ⓑ).

효율 3항목은 매 회차 반드시 적는다 — 2026-09-26 진단 회차 기준선은 약 5분·17회·290행(재현 시험), 수정 회차 뒤 같은 재현은
**precheck.sh 1회·약 15초·0행**(재현 시험 — 계산·대조만, last-audit.md 효율표와 같은 값). 기록이 쌓여야 E3(도구 호출 묶기)를 실측할 수 있다.

## 승인이 필요한 지점 — 여기서는 반드시 멈춘다

아래 상황에서는 리포트에 반영하지 말고, **배포도 하지 말고**, 대화로 보고한 뒤
승인을 기다린다. 임의로 판단해서 넣으면 잘못된 정보가 조용히 배포된다.

**순서는 승인·등록·확인 → 배포다**(사용자 결정 2026-09-28). 해당하는 (1)~(4) 질문은 **한 메시지로 한 번에** 묻고(`references/code-tab.md` 3절 —
2-1 기간이 같으면 그 질문은 이 묶음과 별개의 앞 질문 하나다, 2-1단계),
제외 검색어 등록·verify 결과를 07 각주·11·12번에 쓴 뒤 배포한다. 예외 "등록은 나중에"는 사용자가 그렇게 말할 때만 —
07·11·12번에 사실형 문구("제안함 — 등록은 다음에")로 배포하고 `--pending`은 쓰지 않으며, 8단계 기록에 "등록 미룸(사용자): 예"와 propose 창 lo~hi를 남긴다.
미룬 이름은 다음 회차 propose를 `--since lo`로 돌려 새 이름과 한 묶음으로 올리고, 같은 데이터로 미룬 등록만 하려면 2-1 답 "미룬 등록만"으로 간다.

**(1) 새로운 경쟁사 브랜드명 검색어**

이미 확인된 경쟁사 목록은 `config/report-config.json`의 `competitors`다.
**여기에 이름을 적지 않는다** — 승인 때 config만 갱신하면 이 문서는 자동으로 맞다.

`competitors`에 없는 새 브랜드명 패턴(고유명사+필라테스, 지역명 조합이 아닌 것)이
검색어 보고서에 나타나면:

1. "이번 주 새로 발견된 경쟁사 후보: OOO(노출 N회·클릭 N회·비용 N원)" 형태로 보고
2. 웹 검색으로 소재지(구 단위) 확인을 시도하고 결과를 같이 알림. 특정 안 되면 "확인불가"
3. 승인받은 뒤에만 경쟁사 표에 추가

**판단 주의**: 기존 경쟁사의 표기 변형(예: "퍼스트필라테스" → "퍼스트필라테스아카데미노원")은
새 브랜드가 아니므로 이 절차 없이 기존 표에 행만 추가하면 된다.

**(1-1) 승인·제외 결과를 남기는 곳 — 반드시 세 곳 다**

승인을 받으면 "리포트에 반영"으로 끝내지 말 것. 기록을 남기지 않으면 다음 회차에
같은 후보를 처음 보는 것처럼 다시 묻게 된다. 실제로 그렇게 됐던 적이 있다.

| 무엇 | 어디에 | 형태 |
|---|---|---|
| 채택한 경쟁사 | `config/report-config.json`의 `competitors` | 이름 추가 |
| 채택·제외·종결 판정 전부 | `audit/last-audit.md`의 "경쟁사 판정 이력" 표 | 후보·판정·근거·일자 |
| 리포트 화면 | 07번 경쟁사표 각주 · 11번 `(참고)` 항목 · 12번 액션 표 | 세 곳 관행 유지 |

제외로 판정한 후보도 반드시 이력 표에 남긴다. 그래야 다시 후보로 올라오지 않는다.
이 문서에는 경쟁사 이름 목록이 없으므로 여기서 갱신할 곳은 없다 — 예전엔 이
문서에도 목록이 있어 승인 뒤 갱신이 빠졌고(노원M필라테스, 2026-09-06), 그래서 뺐다.
`config`와 `audit` 갱신은 리포트 배포와 **같은 회차에** 한다. 한쪽만 하면 어긋난다.

**(1-2) 자연 소멸 처리**

몇 주간 노출이 한 자릿수로 정체된 후보는 자연 소멸로 보고 더 언급하지 않는다.
이때도 이력 표에 "종결"로 한 줄 남긴다. 조용히 빼면 다음 회차에 신규로 잡힌다.

**(2) 애매한 후보**

지역 랜드마크+필라테스처럼 브랜드인지 지역 검색인지 불분명하거나, 노출·클릭이
너무 적어 판단 근거가 부족하거나, 검색해보니 다른 지역 프랜차이즈인데 이 동네
지점 여부가 불명확한 경우. 표에 넣지 말고 짧게 언급한 뒤 확인받는다.

몇 주간 노출이 한 자릿수로 정체되면 자연 소멸로 보고 더는 언급하지 않는다.

**(3) 새로운 제외 그룹 후보** — 아래 참고

**(4) 제외 검색어 등록** — 5-0단계의 승인 문구에 "등록 승인 N개"(또는 번호 — "3 빼고"·"업종어 2 넣기") 답이 오기 전에는 `push`·`delete`·`test-roundtrip`을 돌리지 않는다.
등록 여부 자체는 묻지 않는다(registry가 답한다). 금지 패턴(config `never_exclude_patterns`)·경쟁사 이름은 코드가 막는다(실제 등록 = 참조 선택 모드는 쓰기 전 `[FAIL]`, `--approved` dry-run은 `[거부]`).

(5)·(7)은 정보 질문 — 이 절의 멈춤·배포 보류에 들지 않음(`references/code-tab.md` 4절).

**배포(7단계 실제 PUT)** — 따로 묻지 않는다. 위 묶음(과 2-1·되묻기 등 사람 질문)의 답을 모두 받고 6단계 precheck·7단계 `--dry-run`이 통과하면 자동으로 PUT한다(사용자 결정 2026-09-30, 7단계 "자동 배포").
사용자가 "보류"라고 했거나 검사가 하나라도 실패하면 PUT하지 않는다.

일반 지역+필라테스 조합(예: "노원구필라테스", "노원역근처필라테스")은 경쟁사가
아니라 일반 검색어다. 이 절차 대상이 아니며 정식 표나 클릭1건 목록에 그대로 둔다.

## 제외 그룹 판정

**이미 확인된 제외 그룹은 자동으로 제외한다** (매주 반복해서 묻지 않는다).
목록은 `config/report-config.json`의 `excluded_groups`, 그 안에 잠들어 있는
키워드는 같은 파일의 `excluded_group_keywords`다. 여기에 값을 적지 않는다.

설명용으로 현재 유일한 제외 그룹만 언급하면: `노원필라테스(삭제)`는 CSV 표기가
"삭제"지만 실제로는 **OFF 상태**인 광고그룹이고, 키워드 10개가 등록된 채
집행만 멈춰 있다(어느 키워드인지는 `excluded_group_keywords` 참고).

**중요**: 키워드 보고서 CSV에는 노출이 0인 키워드는 행이 생기지 않는다. 그래서
OFF 그룹 키워드 중 노출이 잡힌 것(예: 8/26의 `노원필라테스`)만 보이고 나머지는
보이지 않는다. 보이지 않는다는 이유로, 검색어 보고서에 잡히는 검색어를 두고
**"미등록"이라고 단정하면 안 된다.**
실제로 "노원필라테스"를 2주 연속 "미등록인데 성과 좋음 → 재등록 필요"라고 잘못
써서 정정한 이력이 있다. 올바른 표현은 "OFF 그룹에만 등록돼 실제 집행되지 않는
상태 → 활성 그룹에 키워드 추가 또는 별도 그룹 신설"이다.

**새 후보 자동 감지**: `excluded_groups`에 없는 광고그룹 중 아래 조건에 해당하면 집행이
멈춘 것으로 의심하고 **멈춰서 확인한다**. 자동으로 제외하지 않는다.

- 전체 기간 클릭 0 **그리고** 노출 비중이 전체의 1% 미만
- 또는 최근 3일 연속 노출 0

그룹명 문자열(`(삭제)` 등)에만 의존하지 않는 이유: 네이버 표기가 바뀌거나 두 번째
OFF 그룹이 생기면 조용히 깨지는데, 깨져도 숫자가 그럴듯해서 알아채기 어렵다.

## 반드시 지켜야 할 계산 규칙

**집계 기준**
- 제외 그룹은 KPI·01~07·10번에서 제외
- 08·09번(상세지역·시간대별)은 원본 보고서에 광고그룹 구분 컬럼이 **없어서 제외
  불가** → 포함된 값을 쓰고, 각 섹션에 "KPI와 N회 차이" 각주를 매번 갱신
- 평균노출순위는 단순 평균이 아니라 **노출수 가중평균**
  `(순위 × 노출수).sum() / 노출수.sum()`, 순위가 0인 행은 제외
- 타겟 지역 = `config/report-config.json`의 `target_districts` (현재 5개 자치구)

**동률·경계·정의(2026-09-26 D-11 — 상세는 report-structure.md 각 절 "정의(compute.py)")**
- 07번은 **검색어 단위로 합산**(검색 유형이 갈린 행은 합치고 뱃지는 노출 많은 유형, 일치·확장 동률이면 직전 뱃지 유지).
  정식표 클릭 동률 → 노출 내림차순. 경쟁사표 노출 동률 → 클릭 내림차순, 그 안은 직전 순서. 클릭1건·클릭0·08번
  컴팩트 목록 동률 → 직전 순서 유지. **동률 원칙(2026-09-27)**: HTML의 동률 순서는 직전 순서 유지가 정본. compute.py 출력의 동률 순서(클릭1건 2차 키 총비용↓ 등)는 참고이며 compare.py는 집합+정렬 방향만 본다.
- 09번 심야 = 22·23·0~8시(**09시 배타**), 비중은 정수 반올림. 06번 rankChart = 노원역필라테스 **그룹 전체**(자동매칭 포함) 가중순위.
- 10번 표 A = `검색/콘텐츠 매체 == 검색` 이면서 `매체이름`이 `네이버`로 시작하는 매체 전부(검색탭·광고더보기 포함),
  B = 검색이면서 그 외(`기타 매체`의 검색분 포함), C·D = 콘텐츠의 같은 구분.
- 04번 예산 비중은 최대잔여법(소수 1자리, 합 100.0). 07번 "클릭 0 검색어 전체" 각주는 경쟁사 포함, "노출 5회 이상" 목록은 경쟁사 제외.

**누락 금지** — 이 리포트에서 가장 자주 났던 사고 유형이다
- 07번: 클릭 1건 이상인 검색어는 정식 표(클릭 2건 이상) 또는 클릭 1건 컴팩트 목록
  중 **반드시 어딘가에** 포함. "TOP N"으로 자르지 말 것
- 08번: TOP 10 표 밖에 클릭이 있는 지역은 컴팩트 목록으로 전부 표시

**서술 검증**
- 숫자만 바꾸고 끝내지 말고, 문장이 **여전히 사실인지** 매번 재확인한다.
  "비용은 9/3 최고치"가 다음 주엔 틀릴 수 있고, "노출이 계속 줄고 있다"가
  반등하면 거짓이 된다.
- 확실하지 않은 인과관계는 단정하지 말고 "~로 보임", "~일 수 있음"으로 여지를 둔다.
- 이전 주 결론이 뒤집히면 조용히 지우지 말고 "지난주 관찰이 이번 주엔 다르게
  보인다"고 솔직히 서술한다.

**톤**
- 사장형(비즈니스 오너)에게 유용한 정보를 준다는 관점 유지
- 심야·주말 광고 집행은 "카카오톡·네이버톡톡 상시 문의 대응" 전략과 맞물린
  의도된 운영이다. 경고나 비효율 뉘앙스로 쓰지 말 것

**신규 키워드**
- 데이터가 10일치 미만이면 요약 카드로 유지, 충분히 쌓이면 독립 라인 차트로 승격

## 매번 함께 바꿔야 할 텍스트

리포트가 데이터를 실시간으로 읽는 게 아니라 텍스트로 써넣는 방식이라 자동으로
안 바뀐다. 체크리스트처럼 확인한다.

1. masthead의 "집계 기간" (예: `2026.08.26 — 09.04 (10일)`)
2. `<meta property="og:description">` (카톡 공유 미리보기 문구)
3. 01번 x축 날짜 라벨 + 차트 컨테이너 `min-width` = 날짜 수 × `per_day_px`
   (최소 `floor_px`, 값은 config `chart_min_width`) — 라벨 배열·min-width 는 PC·HTML 그대로, 모바일 가로 막대(판 C)는
   같은 배열을 화면에서만 분기한다(높이는 JS — config `report_layout.mobile`, 판 D 는 처음에 최근 `mobile.recent_days` 일만 그리고 버튼으로 펼친다 — 배열은 그대로)
4. 06번 x축 날짜 라벨 + 차트 컨테이너 `min-width` (3번과 같은 규칙.
   대상 섹션은 config `date_based_sections`, 모바일은 3번과 같이 화면 분기)
5. 09번 심야(22시~09시) 노출·클릭·비용 콜아웃
6. 11번 핵심요약의 날짜 언급 문장
7. 01번 인사이트 박스 (① 표 · ② 순위 5칸과 각주 · ③ 해석 — 박스 머리글 줄은 두지 않는다, 2026-10-06)
8. 08·09번의 "KPI와 N회 차이" 각주
9. 04번 "예산 비중" 컬럼 (총비용 ÷ 전체 광고비, 합이 100%인지 검산)

## 배포 전 검산

`scripts/validate.py`가 자동으로 확인하는 항목(개수는 실행 출력의 [PASS]/[FAIL] 줄을 세어 확인 — 2026-10-06 회차 2 기준 24개 · 2026-10-09 판 F 기준 25개 · 2026-10-10 매출 작업 27개,
config `date_based_sections`에 따라 늘고 준다. 검사는 이름으로 부른다):

- HTML 태그 짝 (div/table/tr/td/th/span/script 등)
- KPI 총클릭수 = 07번 정식표 + 클릭1건 목록 + 경쟁사표 합계
- 09번 시간대별 클릭 합계 = 키워드 보고서 **제외 전 전체** 클릭 합계
  (시간대별 보고서는 광고그룹 구분이 없어 OFF 그룹이 포함된 값이므로 KPI가 아니라
  전체와 비교한다. 둘의 차이가 곧 08·09번 각주의 "KPI와 N회 차이"다)
- 07번 클릭률 기준 이상 행에만 `.ctr-high`가 적용됐는지 전수 대조
- 01번 일별 표의 클릭률 셀도 같은 규칙으로 전수 대조
- masthead 집계 기간 = CSV `일별` min~max·일수
- KPI 타일 4개(노출·클릭·클릭률·광고비) = CSV 계산값
- 04번 예산 비중 합계 = 100.0%
- 날짜축 차트 `min-width` = 날짜 수 × `per_day_px`(최소 `floor_px`) — 대상은
  config `date_based_sections`(현재 01·06번), 섹션마다 검사 1개
- 날짜축 차트의 x축 라벨 배열(`'M/D(요일)'` 형태) 길이 = 날짜 수
- 섹션 주석 `<!-- Section N: -->` 1~12 존재
- 08·09번 각주 "N회 차이" = 제외 전 전체 노출 − KPI 노출,
  그리고 상세지역 CSV 노출 합계 = 제외 전 전체 노출
- (2026-09-26 추가) 05번 mediaChart top5 = 키워드 CSV `매체이름` 노출 상위 5 — 라벨·값·순서·색
  (09-25 5위 누락 사고 유형. 역검증: feed999 배포본에서 FAIL)
- (2026-09-26 추가) 06번 신규 키워드 카드 큰 숫자 = 04번 같은 그룹의 평균순위 셀 (09-26 1.70/1.67 사고 유형. 역검증: 036080a에서 FAIL)
- (2026-09-26 추가) config `competitors` 이름을 포함하는 검색어가 07번 경쟁사표 **밖**에 없는지(순방향만 — 표 안 이름이
  config에 있는지는 어순 변형 때문에 검사하지 않는다) + 경쟁사표 각 행의 노출·클릭 = 검색어 CSV
- (2026-09-26 추가) 검색어 CSV 클릭 합계 = KPI 클릭 (종전 `참고` 출력 → FAIL)
- (2026-09-26 추가) 11번 항목 수 ≤ 8 + (참고) ≤ 2, 판정 줄 "유지+뒤집힘+근거 소멸 = 직전 항목 수"
- (2026-09-26 추가) 11·12번 본문 금칙어(`필요`·`시점`·`할 것`·`검토`·`주째`) 0건 / (09-27 범위 확장) 07번 각주(`class="note"`)·
  11·12번 본문 잔존 문구(`확인 요청`·`판단 요청`·`기다림`·`확인 중`·`대기`) 0건 — 후자는 `--pending`(사용자 답 대기 배포)일 때만 허용,
  잔존 문구를 보는 유일한 검사(compare.py에는 없음)
- (2026-10-06 추가) **"07 각주 세 자리(경쟁사 판정·제외 검색어·클릭 0 전체)"** — 07번 `class="note"` 전부를 이어 붙인 글에 ① `경쟁사 판정(` ·
  ② `제외 검색어: … 등록 N개 · 확인 a/b · 실패 n` · ③ `클릭 0인 검색어 전체는 N개·노출 N회` 셋 다 있고, ②의 b = 등록 수 × config `exclusions.targets` 수, a ≤ b,
  클릭 0 목록 항목 ≥ 1. 하나라도 없으면 FAIL(글을 줄인 뒤 각주 자리가 빠지거나 옛 형식으로 돌아가는 것). HTML 태그 짝 검사에 `details`·`summary` 포함(회차 2 선반영)
- (2026-10-06 회차 2 추가) **"레이아웃 판"** — `<meta name="report-layout" content="…">` 가 정확히 하나이고 값 = config `report_layout.layout_id`, `<details` 수 =
  `report_layout.markers.details`(5), details 마다 바로 안에 summary. meta 0건·details 0건이면 FAIL(옛 모양으로 조용히 되돌아가는 것 — 옛 사본 통째 교체·세션의 "복원").
  (판 C, 2026-10-06) 같은 검사가 분기 표지 주석 `/* saero:mobile-branch 01 */`·`06` 각 1(합 = `markers.mobile_branch` 2) · 분기 도우미 M 줄 = config `report_layout.mobile` ·
  `matchMedia('(max-width: ' + M.maxPx + 'px)')` 1곳 · CSS `@media (max-width: 640px){` 1곳 = `mobile.max_px`(JS 경계 = CSS 경계)도 본다(이름·검사 수 그대로).
  (판 D, 2026-10-07) M 줄에 `recent: {"01": 14, "06": 14}` = config `mobile.recent_days` 까지 대조.
  (판 E, 2026-10-08) 01 모바일 터치 축 `interaction: {mode:'index', intersect:false, axis:'y'}` 정확히 1건
  (판 F, 2026-10-09) 잔액 카드 표지(`data-balance` 값·보조 줄 각 `markers.balance_card` 1) · `.kpi-row` 안 넷째 카드 뒤 · `.kpi-wide` CSS 1 — PASS `r2026-10-F · details 5 · summary 짝 5 · 분기 2 · M 640/1000 · 최근 14/14 · CSS 640 · 01 터치 y · 잔액 카드 1`
- (2026-10-09 판 F 추가) **"광고비 잔액 카드 = 잔액 기록(balance.json)·며칠분"** — `--balance work/balance.json` 을 직접 읽어(compute 와 계산 공유 0) 카드 값 = ⌊bizmoney_raw⌋ 원 ·
  보조 줄 = 읽은 시각 KST + 며칠분(키워드 CSV 에서 제외 그룹 뺀 마지막 날까지 달력 7일 총비용 — 정수 나눗셈, 0 이면 생략) / 실패 기록이면 `확인 못 함` · `… 조회 실패` ·
  읽은 날 ≤ 집계 마지막 날(지난 회차 기록)·기록 없음·꼴 다름·카드 0건이면 FAIL. 이것으로 validate 검사는 **25개**
- (2026-10-10 매출 작업 A·C 추가) **"01·11·12 서술에 장부 라벨+숫자 0(공개 범위 verdict)"** — 01·11·12 본문에 config `leads.public_labels` 바로 뒤 숫자 0(제외 검색어 문구
  '등록 N개'·'→ 등록 N'·'· verified'·날짜는 안 셈 — `scripts/leads.py` label_hits, guard 와 같은 규칙), `leads.publish` ≠ verdict 면 FAIL /
  **"12번 장부·플레이스 행"** — `장부 기준 판정 = X` 행 정확히 1(X = config 판정 낱말 · `판정 전(N/8주)`) · 장부·플레이스 행의 `M/D까지` = 집계 마지막 날 ·
  플레이스 ✗ 행 ≤ `place_checklist.items_in_12` · ✓ 아닌 행 ≤ 7 · 12번 표 행 0 이면 FAIL. 이것으로 validate 검사는 **27개**(첫 적용 전 배포본 — 12번 장부 행 없음 — 은 이 검사가 FAIL 인 것이 기대값)

그 밖에 precheck 가 함께 돌리는 것(validate 검사 수에는 안 셈): compare.py(101항목 — 10번 나열은 2026-10-06부터 "최근 7일 + 9/6 이후 평균" 형식, 03 은 최신 위,
접기 summary 4항목, 2026-10-10 "12 장부·플레이스" 2항목, 구역별로 따로 파싱해 한 구역 실패가 다른 구역 대조를 생략시키지 않음) · overflow_check.py(접기 전부 열고) · narrative_check.py(서술 미교체).
compute.py 는 `--competitors-html` 경쟁사표가 0행이면 `[FAIL]` exit 1. deploy.py 는 레이아웃 판이 바뀌면 `--layout-change` 없이 PUT 하지 않는다(7단계).
precheck **밖**(판 C, 2026-10-06 · 판 D 2026-10-07 · 판 E 2026-10-08 · 판 F 2026-10-09): `"$PY" tests/chart_check.py <index.html> <compute.json> --base <직전 배포본> --out <폴더>` — 라이브 Chart.js(CDN 2건만 허용, 미로드면 exit 2)로
01·06 의 tick·datalabels·겹침(390 접힘·펼침·다시 접힘·짧은 사본 · 1280 · 회전 390→844→390)과 page.pdf 실물을 재고, 390 에서 01 줄마다 왼쪽·가운데·오른쪽을 진짜로 눌러 팝업 = 그 줄 날짜(판 E)를 본다. 판 F 는 폭마다 광고비 잔액 카드 = .kpi-row 마지막 자식 · 한 줄 전체 · 카드 넷 아래(1280 한 줄 / 390 2·2) · 글자 = compute "잔액". `--out`·`--base` 면 전후 비교 페이지 `<폴더>/compare.html`(맨 앞 상단 카드 옛/새) 도 쓴다. 리허설·검증·첫 적용 "보류" 회차·정기점검에서 돌린다(데이터 회차의 6단계에는 없음).

검사 대상이 0건이면 PASS가 아니라 **FAIL**이다. 마크업이 바뀌어 정규식이 안 맞는데
조용히 통과하는 것을 막기 위한 것이다.

위 목록 중 "매번 함께 바꿔야 할 텍스트" 1·3·4·8·9번은 validate.py 자동 검사 대상이고
(3·4번은 min-width와 라벨 개수까지), 2(og:description)·5(09번 심야 콜아웃 숫자)·7(01번 인사이트 표·순위 5칸·해석 숫자)과
3·4번의 라벨 문자열은 `scripts/compare.py`가 compute.py 출력과 대조한다. 남은 순수 수동 항목은
6(11번 날짜 문장)과 **문장이 여전히 사실인지**(서술 검증)뿐이다. 서술이 지난 회차 그대로 남았는지(교체 누락)는 2026-10-06부터
narrative_check.py 가 본다(매회차 표지 — 사실 여부는 여전히 사람). report-structure.md 11번 수동 검사 6개 중
4개(항목 수·판정 줄·금칙어·12번 모순의 잔존 문구)는 validate.py 검사가 됐다.

마지막 항목이 중요한 이유: 표를 클릭수 내림차순으로 재정렬할 때 조건부 스타일이
셀 값과 어긋나는 사고가 실제로 있었다(CTR 3.68%인데 4% 이상 강조가 남아있었음).
행을 복사해서 값만 바꾸는 방식을 피하고, 스타일은 항상 새로 판단해서 넣는다.

수동으로 추가 확인할 것(숫자는 compare.py가 대조하므로 **문장의 사실 여부**만):
- 08·09번 "OO% 차지" 콜아웃·section-desc "OO가 최고치"의 숫자는 compare.py 대조 항목이다 — 문장 방향(늘었다/줄었다·
  최고치 유지)이 여전히 사실인지는 사람이 본다
- 12번의 완료·철회·보류 항목과 11번 서술이 어긋나지 않는지(작성 기준 4)

## 참고 문서·스크립트

- `references/code-tab.md` — **Code 탭 실행 규약(정본)**: 진입(`D:\saero`·`/saero-run`)·환경(`$PY` venv·`PYTHONUTF8`·`TZ=KST-9`·git 신원·자격 증명)·
  S0 사전 점검 블록·전 단계 순서·멈춤 표·exit 코드 판정·승인 목록 참조 선택 모드·금지·수동 폴백·리허설. 회차를 시작할 때 먼저 읽는다.
  진입 스킬·로컬 CLAUDE.md·질문 다듬기 스킬(`local/prompt-polish/`)의 정본 사본은 저장소 `local/`(설치는 사용자).
- `references/report-structure.md` — 12개 섹션별 상세 구현 규칙 + 각 절 "정의(compute.py)". 5단계에서 읽는다.
- `references/css-and-layout.md` — CSS 유틸 클래스, 여백 기준, 재발 방지용 버그 기록.
  디자인·레이아웃을 건드려야 할 때 읽는다.
- `references/exclusion-ui.md` — 제외 검색어 자동화의 값 정의: API 끝점·서명·오류 코드, UI 실물(탭·대화상자·`이미등록`·금지 요소 `+ 전체추가`),
  registry 스키마·상태, 후보·재노출 판정 규칙, PC 실행 절차, 시험 등록. 5-0단계에서 읽는다.
- `scripts/exclusions.py`(5-0단계 `pull`/`import-ui`/`propose`/`push`(참조 선택 모드·`--dry-run`)/`verify`/`delete`/`test-roundtrip`/`report`) ·
  `audit/exclusions.csv`(등록 상태 registry, 기계 정본) · `tests/test_exclusions.py`(가짜 API로 서명·판정·부분 실패·verified:false(CLI 종료 코드 포함)·dry-run 무전송·
  승인 목록 쓰기 전 가드·pull 뒤 재검사·요청 결과 모름·키 가림·시험 순서 검사 — 정기 점검 때).
- `references/report-fetch.md` — 보고서 자동 수집(설계안 C, PC Playwright)의 값 정의: PC 설치·`--login`·매일 실행·검사·오류 대처·
  codegen 녹화·금지 사항·UI 실물. 1단계에서 읽는다.
- `scripts/fetch_reports.py`(1단계 PC 전용 `--dry-run`/`--login`/기본 실행/`--debug`/`--prev`, config `report_fetch`) ·
  `tests/test_fetch_reports.py`(가짜 화면 `tests/fixtures/`로 dry-run 브라우저 0·금지 차단·4개 다운로드·1일 프리셋·부분 실패 exit 2·
  미로그인 exit 1 검사 — 정기 점검 때).
- `scripts/reportlib.py` — 읽기·제외그룹 필터·일수·섹션 자르기 공통 헬퍼(값 계산은 두지 않는다).
- `scripts/archive.py`(1단계 store/combine) · `scripts/ingest.sh`(1단계 한 번에 — main에서만, 시작 검사(HEAD = origin/main·data/ = HEAD·추적 안 된 파일 0·data/ 줄바꿈 = 커밋) 뒤 store, push 뒤·변경 없음 둘 다 origin/main = HEAD 확인) ·
  `scripts/balance.py`(5단계 첫 명령 — 광고비 잔액 GET 1회 → work/balance.json, 판 F) · `scripts/compute.py`(5단계 값 — `--balance` 면 잔액 카드 값) · `scripts/apply.py`(5단계 기계 자리 교체 — 2026-10-06 저장소화, 멱등·앵커 하나 아니면 FAIL · `--layout` 레이아웃 판 변환·summary) ·
  `scripts/validate.py`(6단계 독립 검산) · `scripts/compare.py`(6단계 차이 0) · `scripts/narrative_check.py`(6단계 서술 미교체) · `scripts/precheck.sh`(6단계 한 번에) ·
  `scripts/deploy.py`(4·7단계 fetch/push/verify, `--dry-run`·`--base`·verify `--ref <커밋>`·push `--layout-change`(레이아웃 판 게이트) — GET 무인증 먼저, PUT은 이 PC git 자격 증명, dry-run은 쓰기 권한까지).
- `tests/mutation_test.py`(validate·archive 검사 생존 — 레이아웃 판 변조·0건 가드·config 실험 포함) · `tests/overflow_check.py`(360/390/430px 넘침, 접기 전부 열고, file:// 밖 요청 차단) ·
  `tests/test_balance.py`(판 F — balance.py 가짜 API 성공·실패 범주·키 비출력·옛 기록 지움 · compute 잔액 창·지난 기록 FAIL · validate 잔액 검사) ·
  `tests/test_apply.py`(+ `tests/fixtures/layout_old.html`·`layout_old.compute.json` — 가짜 값: 판 고르기·`--layout` 변환(옛 → B → C → D → E → F 사슬·E → F 범위·잔액 카드 값)·멱등·앵커·행 수·03 행 분배(10일)·summary·M 줄 다시 쓰기·시끄러운 실패·compute 경쟁사표 0행 FAIL) ·
  `tests/chart_check.py <index.html> <compute.json> [--base] [--out]`(판 F 라이브 차트 — precheck 밖, CDN 2건만 허용: 390 접힘·펼침 누락 0·01 터치 팝업 = 누른 줄 날짜·1280 = 기준·회전·page.pdf 실물 · 상단 잔액 카드 한 줄 전체 · 전후 비교 compare.html) ·
  `tests/test_narrative_check.py`(미교체 FAIL·전부 교체 PASS·표지 0 FAIL·[주의] 둘) · `tests/test_validate_07.py`(07 각주 세 자리·예외 회차 문구) ·
  `tests/test_compare_sections.py <index.html> <compute.json>`(한 구역 문단 삭제·03 오름차순 복귀·summary 옛 값 → 그 구역만 DIFF, 나머지 구역 전부 대조) ·
  `tests/test_ingest.py`(임시 저장소 + 로컬 bare origin: 정상 push·main 아닌 브랜치·push 안 된 커밋·CRLF 입력 바이트·시작 검사, precheck compute 실패) ·
  `scripts/leads.py`(매출 작업 A — 주간 성과 장부 status·add·skip·guard·row, 네트워크 0) · `scripts/place.py`(매출 작업 C — 플레이스 체크리스트 status·set·done·row, 네트워크 0) ·
  `tests/test_leads.py`(주 = 집계 끝 기준·월요일 경계 · 입력 검사 · 줄 추가만·같은 주 FAIL·정정 .bak · skip = 구멍 · 판정 규칙 · compute 건수 0 · guard · validate 25·26 · compare · 같은 주 이틀 narrative) ·
  `tests/test_place.py`(첫 set·쓰기 가드·in12_since · 검색 지면만·달력 일수·띠·겹침·측정 중 · 12번 목록·이월 줄·채팅 신호 · compare) · `tests/section_compare.py <작업본> <직전 배포본> --out <폴더> [--sections 12]`(precheck 밖 — 서술 행을 바꾸는 첫 적용 보류 회차의 전후 비교 페이지, 1280·390 캡처 나란히) ·
  `tests/test_deploy.py`(가짜 API + 가짜 자격 증명 도우미: 값 출력 0·dry-run PUT 0·base 불일치·권한 거짓·필드 없음·token 파일 인코딩·
  precheck 도장(직전 배포본·모드)·PUT 본문 = 도장 바이트·PUT 409/403·PUT 결과 모름·이미 반영 exit 0·`***` 가림·인자 오류 GET 0(exit 2)·토큰 모양·레이아웃 판 게이트 4건) — 정기 점검 때.
