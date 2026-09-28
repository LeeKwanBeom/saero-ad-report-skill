# 보고서 자동 수집 — UI 실물·흐름·검사·PC 절차 (정본)

`scripts/fetch_reports.py`(설계안 C: 사용자 PC의 크롬을 Playwright로 움직여 다차원 보고서 4개를 내려받고 검사)의 값 정의다.
**문서 = 코드**: 여기 적힌 규칙과 코드·config `report_fetch`가 어긋나면 셋 다 고친다.
탐색 근거는 `audit/last-audit.md` "기능 추가 탐색 기준선(보고서 자동 수집, 2026-09-28)" 1절(UI CSV 형식)·6-5(UI 실물)·6-6(설계안 C)·6-7(금지 후보).
표기: [실측] 실물에서 확인 · [문서] 공식 문서 · [추론] 확인 안 됨 · [시험] 저장소 `tests/fixtures` 가짜 화면으로 확인.

## 1. PC 설치 (한 번)

PowerShell, 저장소 루트(`git pull` 뒤):
```
pip install playwright
python -m playwright install chromium          # 설치된 크롬을 쓰므로 크롬이 있으면 건너뛰어도 된다(번들 크로미움은 크롬이 없을 때의 대체)
python scripts\fetch_reports.py --dry-run      # 브라우저 0 — 할 일 표가 나오면 설치 끝
```
- 필요한 것: Python 3.9 이상 · `playwright` 패키지 · 크롬(설치돼 있으면 `browser_channel: "chrome"`로 그것을 쓴다) — pandas 불필요(표준 라이브러리만).
- **Python 3.14에서 `pip install playwright`가 실패하면**(휠 없음·`greenlet` 빌드 오류 등): ① `pip install --upgrade pip` 뒤 재시도 ② 그래도 안 되면 python.org에서 3.12 또는 3.13을 **추가 설치**(기존 3.14는 두고, 설치 중 "Add python.exe to PATH" 체크 불필요)하고 이후 모든 명령의 `python`을 `py -3.12`로 바꾼다:
  `py -0`(설치된 버전 목록) → `py -3.12 -m pip install playwright` → `py -3.12 -m playwright install chromium` → `py -3.12 scripts\fetch_reports.py --dry-run`.
- 설치는 config를 바꾸지 않는다. 저장 폴더·프로필 폴더는 config `download_dir`·`profile_dir`(기본 `~/saero-fetch/…` = `C:\Users\<사용자>\saero-fetch\`, **저장소 밖**)이고, 첫 실행 때 만들어진다(`--dry-run`은 만들지 않는다).

## 2. 첫 로그인 (한 번, 세션이 끝날 때마다)

```
python scripts\fetch_reports.py --login
```
전용 크롬 프로필(`profile_dir`)로 창이 뜨고 목록 URL로 간다. **사용자가 창에서 직접** 네이버 로그인을 하고 `로그인 상태 유지`를 체크한다(2단계 인증도 사용자가). 스크립트는 폼에 아무것도 입력하지 않으며, 목록 화면(`…/ad-accounts/2580077/sa/reports`)에 도달하면 `[OK] 목록 URL 도달 · 보고서 이름 4/4개 보임`을 찍고 창을 닫는다(닫아야 로그인 상태가 프로필에 저장된다). 최대 대기 `timeout_sec.login`(600초).
`[FAIL] 시간 안에 목록 화면에 도달하지 못함`이면 다시 `--login`. 이 프로필은 이 스크립트 전용이다 — 평소 쓰는 크롬 프로필을 넣지 않는다.

## 3. 매일 실행

```
python scripts\fetch_reports.py --prev C:\Users\<사용자>\saero-fetch\downloads\<직전 날짜> [--debug]
```
- 시각: **01:00 KST 이후**(어제 집계 완료 — API `cycleBaseTm` 01:00·UI 띠 00:20 실측 09-28). 그 전에 돌리면 어제 행이 비거나 헤더가 그제까지로 나와 "기간 = 기대" FAIL이 난다.
- `--prev`: 직전 성공 폴더(또는 저장소 `data/YYYY-MM`)를 주면 겹치는 날짜의 일별 노출·클릭·비용을 비교해 다르면 `[WARN]`(재집계 가능성)만 낸다 — **막지 않는다**. 첫 실행·달이 바뀐 날은 생략해도 된다.
- `--debug`: 단계마다 스크린샷을 저장 폴더 `debug/`에 남긴다. 첫 실사용·왕복 확인 때 켠다. 실패한 보고서의 스크린샷 1장은 `--debug` 없이도 남는다.
  스크린샷마다 같은 이름의 **`.aria.txt`**(접근성 트리 — 역할·이름·값)와 **`.inventory.json`**(날짜가 든 요소·input·button·link의 태그/역할/이름/클래스/문구)도 함께 저장된다 — 화면 문구만 담기고 자격 증명·쿠키는 없다. 다음 왕복에서 로케이터를 확정하는 근거(스크린샷만으로는 DOM을 알 수 없다 — 왕복 1).
- `--today YYYY-MM-DD`: 기대 기간 계산 기준일을 바꾼다(시험용). 평소에는 쓰지 않는다.

흐름(코드 `cmd_fetch`·`fetch_one`) — 목록 URL → (로그인 세션이 없으면 `[FAIL] … --login` exit 1) → 보고서마다:
① 목록에서 이름 링크 클릭(`report_names` 키, 링크·버튼 역할 우선) → `돌아가기` 버튼이 보이면 보고서 화면 ② 기간 읽기(`read_period`: 기간 텍스트 `YYYY.MM.DD. → YYYY.MM.DD.` → 없으면 날짜 값을 가진 보이는 input 2개(RangePicker형) → 없으면 본문 한 줄의 날짜 2개; 표시가 늦게 그려질 수 있어 `timeout_sec.page`까지 기다린다 — 왕복 1) ③ 기대 기간과 다르면 기간 표시(텍스트, 없으면 날짜 textbox, config `period_opener`가 있으면 그 이름) 클릭 → 프리셋(`이번달`/`지난달`) 클릭 → `확인` → **다시 읽어 기대와 같은지 확인**(다르면 그 보고서 실패, 조회·다운로드 안 함) ④ `조회하기` ⑤ `다운로드`(download 이벤트를 기다림) → 원본 파일명 그대로 저장 ⑥ `돌아가기`. 한 보고서의 실패는 그 보고서만 실패로 두고, **성공·실패 어느 쪽이든 목록으로 돌아간 뒤**(`back_to_list`: `돌아가기` 클릭 → 목록 URL·보고서 링크 2개 이상 확인, 안 되면 목록 URL로 이동) 다음 보고서로 간다.

기대 기간(`expected_period`) [실측 09-28]: 평일 = `이번달` = 이번 달 1일~어제 · **매월 1일** = `지난달` = 지난달 1일~말일(31일 달도 한 파일, 8/1~8/31 실측 ⑤). 보고서 4개의 형식에 `이번달`이 저장돼 있어 평일에는 열면 이미 기대 기간이다(①) — 그래서 평일은 프리셋 클릭 없이 ④로 간다.

## 4. 결과 확인

- 성공(exit 0): `download_dir\YYYY-MM-DD\`에 `시간대별_보고서_2580077.csv`·`상세지역_보고서_2580077.csv`·`검색어_보고서_2580077.csv`·`필라테스_보고서_2580077.csv`(원본 이름, 09-28 실측 ③) + `summary.json`(+ `debug/`). 콘솔에 보고서별 표(행·노출·클릭·비용). **이 4개를 세션에 올리면** 1단계(`archive.py store` → `combine`)가 이어진다 — store·push는 지금처럼 세션이 한다(2회차에 PC로 옮길지 결정).
- 부분 실패(exit 2): 받은 파일은 `download_dir\partial\YYYY-MM-DD\`에만 있고 정상 폴더에는 이번 실행 파일이 없다. 콘솔 표의 "비고"와 `summary.json`의 `reports[].error`·`check.checks`로 원인을 본다. **partial의 파일은 store 하지 않는다** — 원인을 고치고 다시 실행한다(같은 날 재실행은 partial을 비우고 시작한다).
- 검사 항목(`check_file`·`cross_check`, 파일마다): 첫 줄이 `archive.py` HEAD_RE에 맞음 · 첫 줄 이름 = 보고서 이름 · **기간 = 기대**(매월 1일은 1일~말일이 아니면 FAIL) · 계정 = `account_no` / 2행 컬럼 = config `columns`의 종류별 원문 / 데이터 행 ≥ 1 / 일별 값이 헤더 기간 안. 4개 뒤: **키워드·시간대별·상세지역 노출합 동일**(combine 정합과 같은 식; 검색어는 콘텐츠 지면이 빠져 비교하지 않는다 — [의도된 동작] 5).
- `summary.json`: `expected`(프리셋·기간) · `reports[]`(이름·종류·상태·파일·`steps`·`period_read`(읽은 기간과 읽은 방법 `range-text`/`inputs`)·`preset_clicked`·`check`(검사 결과·행수·노출/클릭/비용 합)) · `cross` · `prev_compare`·`warnings` · `browser`·`playwright` 버전 · `log`. 자격 증명·쿠키는 없다.

## 5. 오류 대처

| 증상 | 조치 |
|---|---|
| `[FAIL] 목록 URL에 도달하지 못함 … --login` (exit 1) | 로그인 세션 만료 → `python scripts\fetch_reports.py --login` 다시(사용자가 창에서 로그인) → 본 실행 |
| `[FAIL] 허용 목록 밖 동작` / `금지 요소 클릭 시도 차단` (exit 1) | 코드가 클릭 직전에 멈춘 것(설정 변경 방지). 화면이 바뀐 신호 — 아래 "화면 변경" |
| `목록에 보고서 링크 '…' 없음` | 목록의 보고서 이름과 config `report_names` 키가 다른지(스크린샷 `*_no_link.png`) |
| `보고서 화면(돌아가기 버튼)이 뜨지 않음` · `기간을 읽지 못함` · `프리셋 … 없음` · `확인/조회하기/다운로드 버튼을 찾지 못함` · `다운로드가 시작되지 않음` | **화면 변경**: `--debug`로 다시 돌려 `debug/` 전부(png·`.aria.txt`·`.inventory.json`) + `summary.json`을 세션에 첨부 → 세션이 문구·순서를 고친다(config `period_opener`·`download_menu_item`·`allowed_actions` 값으로 고칠 수 있는 범위면 config만) |
| 위로도 셀렉터가 안 잡히면(왕복 3회) | 로그인된 전용 프로필로 **녹화**해 파일을 첨부한다(녹화 중 **로그인·비밀번호 입력 금지**, 이미 로그인된 프로필이라 필요 없다): |

```
python -m playwright codegen --channel chrome --user-data-dir "C:\Users\<사용자>\saero-fetch\chrome-profile" --target python -o "C:\Users\<사용자>\saero-fetch\codegen_<날짜>.py" "https://ads.naver.com/manage/ad-accounts/2580077/sa/reports"
```
창에서 보고서 하나만 **열기 → 기간 클릭 → 프리셋 → 확인 → 조회하기 → 다운로드 → 돌아가기**를 한 번 하고 창을 닫는다. `codegen_<날짜>.py`에 Playwright가 기록한 로케이터(`get_by_role`·`get_by_text` …)가 남고, 세션은 그것으로 `locate()`의 문구·역할을 확정한다. 녹화 파일에 아이디·비밀번호가 없는지 보고 첨부한다.

| `[WARN] … 일별 합계가 다름(재집계 가능성)` | 막지 않는다. store 뒤 combine·validate가 실제 값으로 다시 검사한다. 자주 나면 재집계 기록으로 last-audit에 남긴다 |
|---|---|
| `[WARN] 파일명 … ≠ 기대` | 다운로드 파일명 규칙이 바뀐 것 — 내용 검사가 통과했으면 그대로 쓰고, 세션에 알린다 |
| `playwright가 없습니다` | 1절 설치. Python 3.14 대처법도 1절 |
| `channel=chrome 실행 실패 → 번들 크로미움으로 재시도` | 크롬이 없거나 실행 중 프로필 잠김. 크로미움으로 계속되면 그대로 두어도 된다(같은 프로필 폴더를 두 브라우저가 번갈아 쓰면 프로필이 깨질 수 있으니 한쪽으로 고정: `browser_channel`) |
| 창이 뜬 채 멈춤 | 네이버 쪽 팝업·공지가 떠 있으면 사용자가 닫는다(코드는 허용 요소만 클릭하므로 스스로 닫지 않는다). 시간 초과(`timeout_sec.page` 40초·`download` 90초)면 그 보고서 실패로 넘어간다 |

## 6. 금지 사항 (config `forbidden_actions` + 코드 규칙, checklist "되돌리면 안 되는 것")

- 코드는 `allowed_actions`(보고서 열기·기간·프리셋·확인·조회하기·다운로드·돌아가기) 밖의 요소를 **절대 클릭하지 않는다**. `+ 새 보고서`·`보고서 형식 저장`·항목 ×/끌어놓기·`삭제`·로그인 폼·계정/충전/결제 메뉴 문구가 든 요소는 클릭 직전에 막고 멈춘다(`click_allowed`). 클릭 호출은 코드에 한 곳뿐이다.
- 좌표 클릭·키 입력(`mouse`·`fill`·`type`·`press`)·드래그 0. 로케이터는 role·text만.
- 자격 증명·API 키·쿠키를 코드·config·저장소·채팅·summary·스크린샷 파일명 어디에도 두지 않는다. 로그인은 사용자가 창에서.
- 검사 통과 전·부분 실패에는 `archive.py store`를 하지 않는다. partial 폴더의 파일은 쓰지 않는다.
- 두 달에 걸친 기간을 만들지 않는다(프리셋 2개만 쓰고, 사용자 지정 기간 입력 코드가 없다). `store --force`·`--chunk`를 자동으로 붙이지 않는다.
- 헤드리스로 돌리지 않는다(사용자가 보는 창). 같은 프로필로 두 실행을 동시에 돌리지 않는다.
- 진단·검증 회차는 `--dry-run`과 `tests/test_fetch_reports.py`(가짜 화면)만 — 실제 광고주센터 실행은 사용자 PC·사용자 승인 뒤.

## 7. UI 실물 [실측: 사용자 스크린샷 3장, 2026-09-28 탐색 기준선 6-5] — 코드가 기대하는 문구

- 목록 `…/ad-accounts/2580077/sa/reports`: 제목 `다차원 보고서`, 주황 띠 `최근 집계 완료 시간 : YYYY.MM.DD. HH:MM`, 버튼 `+ 새 보고서 ∨`(금지), 표 `보고서 이름 | 통계기간 | 생성일 | 최근 열람일 | 생성자` — 행 4개 `시간대별 보고서`·`상세지역 보고서`·`검색어 보고서`·`필라테스 보고서`(= `report_names` 키, 링크 텍스트), 통계기간 열 전부 `이번달`(사용자가 09-28 저장 ①).
- 보고서 화면: `← 돌아가기` · `보고서 형식 저장 ∨`(금지) · `다운로드` · 기간 `YYYY.MM.DD. → YYYY.MM.DD.` + 달력 아이콘 + `<` `>` · `조회하기`(조회 전 회색). 기간 팝업: 프리셋 `어제·이번주·지난주·전 영업주·최근 7일 (오늘 제외)·이번달·지난달·이번 분기·지난 분기·최근 30일 (오늘 제외)·최근 90일 (오늘 제외)·최근 365일 (오늘 제외)` · 시작/끝 입력칸 · `취소`·`확인`.
- 다운로드 파일: `<보고서명>_보고서_2580077.csv`, 첫 줄 `"<이름> 보고서(YYYY.MM.DD.~YYYY.MM.DD.),2580077"`, utf-8-sig·LF, 2행 컬럼 = config `columns`(1절 실물) [실측 ③].
- [추론] 아직 실물로 못 본 것 → 첫 PC 왕복이 확정: 기간 텍스트를 클릭하면 팝업이 열리는지(아니면 달력 아이콘 → config `period_opener`에 그 접근성 이름) · `돌아가기`가 button인지 link인지(둘 다 찾는다) · `다운로드`가 바로 받는지 메뉴가 뜨는지(`download_menu_item`) · `확인` 뒤 기간 텍스트가 즉시 바뀌는지 · 조회 완료를 기다릴 시간(`settle_sec`).

## 8. 시험 (검증·진단 회차용, 네트워크 0)

`python3 tests/test_fetch_reports.py` — 실 CSV 4개로 검사 함수, 가짜 `playwright` 패키지로 `--dry-run` 브라우저 0·폴더 0, `click_allowed` 금지 차단·소스의 클릭 호출 1곳, `tests/fixtures/report-ui-fixture.html`(광고주센터 문구·흐름을 흉내 낸 로컬 화면, `login.html`은 `?auto=1`이면 1.5초 뒤 "사용자가 로그인한 것"으로 처리)에서 헤드리스로 `--login` 도달 → 4개 다운로드 성공(저장된 `이번달`이라 프리셋 클릭 0) → 매월 1일(`--today 2026-10-01`) `지난달` 프리셋 경로 → `--prev` WARN(막지 않음) → 보고서 이름 하나 틀리면 exit 2·정상 폴더 없음·partial 3개 → 로그인 안 됐으면 exit 1. 끝에 실제 `data/2026-09`·config md5 전/후 출력.
가짜 화면은 실제 사이트와 무관하다 — 실제 DOM의 문구·구조는 첫 PC 왕복(`--debug`)으로만 확정된다.

## 9. PC 왕복 절차 (구현 회차, 최대 3회)

세션이 브랜치를 push → 사용자 PC에서 `git pull`(브랜치 `feat-report-fetch` checkout) → 1절 설치 → `--dry-run` → `--login` → 본 실행 `--debug` → 콘솔 출력 전문·`debug/` 전부(png·`.aria.txt`·`.inventory.json`)·`summary.json`·(성공 시) 4개 CSV를 세션에 첨부 → 세션이 문구·config를 고쳐 다시 push. 3회 안에 셀렉터가 안 잡히면 5절 codegen 녹화. 왕복마다 결과를 `audit/last-audit.md` 구현 기준선 "PC 왕복 기록"에 남긴다.

왕복 1(2026-09-28, PC Python 3.12·pip 25.0.1·Playwright 1.63.0·크로미움 v1243·설치된 크롬 channel) [실측: 사용자 콘솔 화면 2장]: 설치·`--dry-run`·`--login`(`[OK] 목록 URL 도달 · 4/4개`) 통과. 본 실행은 `시간대별 보고서` 링크 클릭 → `돌아가기` 확인(보고서 열림)까지 되고 **기간 텍스트를 못 읽어** 실패, 그 뒤 목록 복귀가 없어 나머지 3개가 `링크 없음`(코드 결함 → `back_to_list` 신설). 실제 기간 표시 DOM은 아직 [미실측] → 왕복 2는 `read_period` 3단계 폴백 + `.aria.txt`·`.inventory.json`으로 확정한다.
