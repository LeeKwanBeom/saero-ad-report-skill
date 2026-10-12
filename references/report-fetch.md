# 보고서 자동 수집 — UI 실물·흐름·검사·PC 절차 (정본)

`scripts/fetch_reports.py`(설계안 C: 사용자 PC의 크롬을 Playwright로 움직여 다차원 보고서 4개를 내려받고 검사 — 2026-10-12 부터 4개 뒤 같은 실행에서 추가 수집, 4-1절)의 값 정의다.
**문서 = 코드**: 여기 적힌 규칙과 코드·config `report_fetch`가 어긋나면 셋 다 고친다.
탐색 근거는 `audit/archive/last-audit_~2026-10-05.md` "기능 추가 탐색 기준선(보고서 자동 수집, 2026-09-28)" 1절(UI CSV 형식)·6-5(UI 실물)·6-6(설계안 C)·6-7(금지 후보).
표기: [실측] 실물에서 확인 · [문서] 공식 문서 · [추론] 확인 안 됨 · [시험] 저장소 `tests/fixtures` 가짜 화면으로 확인.

## 1. PC 설치 (한 번)

**모든 명령은 작업 폴더(저장소 루트)에서** — Code 탭은 `D:\saero\saero-ad-report-skill`(main, `references/code-tab.md` 0절). 파이썬은 `$PY`(저장소 밖 venv,
`code-tab.md` 1절 — `--system-site-packages`라 시스템에 깐 playwright를 본다). 사용자 PowerShell에서 칠 때도 같은 폴더로 먼저 이동한다(새 창은 Downloads 등에서 열림, 왕복 3):
```
cd D:\saero\saero-ad-report-skill              # 작업 폴더(main) — Desktop 사본 등 다른 clone은 쓰지 않는다
python -m pip install playwright               # 시스템 파이썬에 한 번(venv가 이것을 본다)
python -m playwright install chromium          # 설치된 크롬을 쓰므로 크롬이 있으면 건너뛰어도 된다(번들 크로미움은 크롬이 없을 때의 대체)
D:\saero\.venv\Scripts\python.exe scripts\fetch_reports.py --dry-run      # 브라우저 0 — 할 일 표가 나오면 설치 끝
```
- 필요한 것: Python 3.9 이상 · `playwright` 패키지 · 크롬(설치돼 있으면 `browser_channel: "chrome"`로 그것을 쓴다) — pandas 불필요(표준 라이브러리만).
- **Python 3.14에서 `pip install playwright`가 실패하면**(휠 없음·`greenlet` 빌드 오류 등): ① `pip install --upgrade pip` 뒤 재시도 ② 그래도 안 되면 python.org에서 3.12 또는 3.13을 **추가 설치**(기존 3.14는 두고, 설치 중 "Add python.exe to PATH" 체크 불필요)하고
  playwright는 `py -3.12 -m pip install playwright`, venv도 `py -3.12 -m venv --system-site-packages D:\saero\.venv`로 만든다(`py -0` = 설치된 버전 목록).
  그 뒤 실행은 1절 그대로 `$PY`(venv 파이썬) — venv가 3.12 위에 서므로 명령마다 `py -3.12`로 바꿀 필요가 없다.
- 설치는 config를 바꾸지 않는다. 저장 폴더·프로필 폴더는 config `download_dir`·`profile_dir`(기본 `~/saero-fetch/…` = `C:\Users\<사용자>\saero-fetch\`, **저장소 밖**)이고, 첫 실행 때 만들어진다(`--dry-run`은 만들지 않는다).

## 2. 첫 로그인 (한 번, 세션이 끝날 때마다)

```
"$PY" scripts/fetch_reports.py --login       # Code 탭 Git Bash(작업 폴더, code-tab.md 1절 export 뒤) — run_in_background(최대 600초 대기)
```
전용 크롬 프로필(`profile_dir`)로 창이 뜨고 목록 URL로 간다. **사용자가 창에서 직접** 네이버 로그인을 하고 `로그인 상태 유지`를 체크한다(2단계 인증도 사용자가). 스크립트는 폼에 아무것도 입력하지 않으며, 목록 화면(`…/ad-accounts/2580077/sa/reports`)에 도달하면 `[OK] 목록 URL 도달 · 보고서 이름 4/4개 보임`을 찍고 창을 닫는다(닫아야 로그인 상태가 프로필에 저장된다). 최대 대기 `timeout_sec.login`(600초).
`[FAIL] 시간 안에 목록 화면에 도달하지 못함`이면 다시 `--login`. 이 프로필은 이 스크립트 전용이다 — 평소 쓰는 크롬 프로필을 넣지 않는다.

## 3. 매일 실행

```
cd /d/saero/saero-ad-report-skill && export PY=/d/saero/.venv/Scripts/python.exe PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never; unset GIT_ASKPASS SSH_ASKPASS    # Code 탭 Git Bash(code-tab.md 1절) — S0 사전 점검 뒤
"$PY" scripts/fetch_reports.py --prev ~/saero-fetch/downloads/<직전 날짜> [--debug]                  # Code 탭은 run_in_background(3~5분, 사용자 화면에 창)
```
- 시각: **01:00 KST 이후**(어제 집계 완료 — API `cycleBaseTm` 01:00·UI 띠 00:20 실측 09-28). 그 전에 돌리면 어제 행이 비거나 헤더가 그제까지로 나와 "기간 = 기대" FAIL이 난다.
- `--prev`: 직전 성공 폴더(또는 저장소 `data/YYYY-MM`)를 주면 겹치는 날짜의 일별 노출·클릭·비용을 비교해 다르면 `[WARN]`(재집계 가능성)만 낸다 — **막지 않는다**. 첫 실행·달이 바뀐 날은 생략해도 된다.
- `--debug`: 단계마다 스크린샷을 저장 폴더 `debug/`에 남긴다. 첫 실사용·왕복 확인 때 켠다. 실패한 보고서의 스크린샷 1장은 `--debug` 없이도 남는다.
  스크린샷마다 같은 이름의 **`.aria.txt`**(접근성 트리 — 역할·이름·값)와 **`.inventory.json`**(날짜가 든 요소·input·button·link의 태그/역할/이름/클래스/문구)도 함께 저장된다 — 화면 문구만 담기고 자격 증명·쿠키는 없다. 다음 왕복에서 로케이터를 확정하는 근거(스크린샷만으로는 DOM을 알 수 없다 — 왕복 1).
  **광고주센터 모든 화면 위쪽에 로그인 아이디·비즈머니가 보인다**(2026-10-11 탐색 실측) — debug·실패 컷(png·`.aria.txt`·`.inventory.json`)·partial 은 저장소 밖(`download_dir`)에만 두고, 열어 본 아이디를 last-audit·커밋·채팅에 옮기지 않는다(`<ID>` 로 가림).
  추가 수집의 B(변경 이력)는 컷을 찍지 않는다(원인은 문구로만), `summary_extra.json` 의 실패 메시지에는 셀 원문이 없다(4-1절).
- `--today YYYY-MM-DD`: 기대 기간 계산 기준일을 바꾼다(시험용). 평소에는 쓰지 않는다.

흐름(코드 `cmd_fetch`·`fetch_one`) — 프로필 정리(`clean_download_history`, 브라우저를 띄우기 전 — 5절 "크래시") → 목록 URL → (로그인 세션이 없으면 `[FAIL] … --login` exit 1) → 보고서마다:
① 목록에서 이름 링크 클릭(`report_names` 키, 링크·버튼 역할 우선) → `돌아가기` 버튼이 보이면 보고서 화면 ② 기간 읽기(`read_period`: 기간 텍스트 `YYYY.MM.DD. → YYYY.MM.DD.` → 없으면 날짜 값을 가진 보이는 input 2개(RangePicker형) → 없으면 본문 한 줄의 날짜 2개; 표시가 늦게 그려질 수 있어 `timeout_sec.page`까지 기다린다 — 왕복 1) ③ 기대 기간과 다르면 기간 표시(텍스트, 없으면 날짜 textbox, config `period_opener`가 있으면 그 이름) 클릭 → 프리셋(`이번달`/`지난달`) 클릭 → `확인` → **다시 읽어 기대와 같은지 확인**(다르면 그 보고서 실패, 조회·다운로드 안 함) ④ `조회하기` — **활성일 때만** 클릭(저장된 형식으로 열면 결과가 자동 조회되고 버튼이 비활성(회색)이다 — 왕복 2 실측; 기간을 바꿔 `확인`하면 활성) ⑤ `다운로드`(download 이벤트를 기다림) → 원본 파일명 그대로 저장 ⑥ `돌아가기`. 한 보고서의 실패는 그 보고서만 실패로 두고, **성공·실패 어느 쪽이든 목록으로 돌아간 뒤**(`back_to_list`: `돌아가기` 클릭 → 목록 URL·보고서 링크 2개 이상 확인, 안 되면 목록 URL로 이동) 다음 보고서로 간다.

기대 기간(`expected_period`) [실측 09-28]: 평일 = `이번달` = 이번 달 1일~어제 · **매월 1일** = `지난달` = 지난달 1일~말일(31일 달도 한 파일, 8/1~8/31 실측 ⑤). 보고서 4개의 형식에 `이번달`이 저장돼 있어 평일에는 열면 이미 기대 기간이다(①) — 그래서 평일은 프리셋 클릭 없이 ④로 간다.

## 4. 결과 확인

- 성공(exit 0): `download_dir\YYYY-MM-DD\`(예 `C:\Users\<사용자>\saero-fetch\downloads\2026-09-28\`)에 **`시간대별 보고서,2580077.csv`·`상세지역 보고서,2580077.csv`·`검색어 보고서,2580077.csv`·`필라테스 보고서,2580077.csv`**(네이버가 보내는 원본 이름 그대로 — 왕복 3 실측; 손으로 받을 때 보이던 `<보고서명>_보고서_2580077.csv`도 정상 이름으로 본다) + `summary.json`(+ `debug/`). 콘솔에 보고서별 표(행·노출·클릭·비용)와 `다음:` 줄. **같은 Code 탭 세션이 이 폴더의 4개를 그대로** 1단계
`scripts/ingest.sh "<성공 폴더>"/*.csv`(store → combine → push)에 넘긴다 — 업로드 없음(2026-09-28 Code 탭 회차 = 예전 "2회차에 PC로 옮길지"의 그 회차, `code-tab.md` 3절).
- 부분 실패(exit 2): 받은 파일은 `download_dir\partial\YYYY-MM-DD\`에만 있고 정상 폴더에는 이번 실행 파일이 없다. 콘솔 표의 "비고"와 `summary.json`의 `reports[].error`·`check.checks`로 원인을 본다. **partial의 파일은 store 하지 않는다** — 원인을 고치고 다시 실행한다(같은 날 재실행은 partial을 비우고 시작한다).
- 검사 항목(`check_file`·`cross_check`, 파일마다): 첫 줄이 `archive.py` HEAD_RE에 맞음 · 첫 줄 이름 = 보고서 이름 · **기간 = 기대**(매월 1일은 1일~말일이 아니면 FAIL) · 계정 = `account_no` / 2행 컬럼 = config `columns`의 종류별 원문 / 데이터 행 ≥ 1 / 일별 값이 헤더 기간 안. 4개 뒤: **키워드·시간대별·상세지역 노출합 동일**(combine 정합과 같은 식; 검색어는 콘텐츠 지면이 빠져 비교하지 않는다 — [의도된 동작] 5).
- `summary.json`: `expected`(프리셋·기간) · `steps`(실행 단계 — 프로필 정리 결과 줄)·`profile_cleanup`(지운/유지 건수·DB 경로) · `reports[]`(이름·종류·상태·파일·`steps`·`period_read`(읽은 기간과 읽은 방법 `range-text`/`inputs`)·`preset_clicked`·`check`(검사 결과·행수·노출/클릭/비용 합)) · `cross` · `prev_compare`·`warnings` · `browser`·`playwright` 버전 · `log`. 자격 증명·쿠키는 없다.

## 4-1. 추가 수집 — 성별·연령대 보고서 · 변경 이력(2026-10-12, config `report_fetch.extras`)

사용자 결정 2026-10-12(보고서 더 받기 A + B, 원문 "추천대로 하자" — 매일 · 저장소 밖 · `성별 보고서`·`연령대 보고서` 두 개(한 보고서에 성별·연령대를 같이 못 고름 — 사용자 실측)).
기존 4개(`report_names`·`columns`·성공 폴더 `*.csv` 4개·ingest·data/·종료 코드)는 그대로다. 블록이 없으면 지금과 똑같은 출력.

- 흐름(코드 `cmd_fetch`·`finish_four`·`run_extras`·`fetch_history`): ① 4개(위 3절 그대로) → ② **브라우저를 닫기 전에** 4개 검사·교차 검사·성공 폴더 이동·summary·`[PASS] 4개 다운로드·검사 통과 → <폴더>`·표·`다음:` 줄(지금과 같은 줄) →
  ③ 4개 PASS 이고 `extras` 가 있으면 같은 브라우저로 — A `성별 보고서`·`연령대 보고서`(config `extras.reports` 키 = 목록 링크 텍스트 · 4개와 같은 `fetch_one` · 기대 기간도 4개와 같은 `이번달`/1일 `지난달`) →
  B 변경 이력 관리(config `history.url` 로 `page.goto` — 그 밖 이동 0 · 화면 기간 끝 = 오늘 확인 · `다운로드` 후보가 **정확히 1개**일 때만 `click_allowed('download')` · 엑셀을 표준 라이브러리(zipfile + xml)로 읽어
  머리줄 = config `history.columns` 확인 · 변경자 원문은 config `actor_rules`(끝 글자 → 사람/스킬/시스템, 안 맞으면 기타)로 **주체 낱말로 바꾸고 버린** 정리본 `변경이력.csv` 만 남기고 아이디가 든 엑셀은 지운다 ·
  B 단계 스크린샷·접근성 트리 0) → ④ 모든 길에서 `ctx.close()`(try/finally — 닫기 예외는 `[주의] 브라우저 닫기 예외(…) — 4개 결과·종료 코드는 그대로`).
- **종료 코드는 4개로만**(0 / 2 / 1 그대로). 추가의 실패·차단(금지 문구 SystemExit 포함)·예외·브라우저 꺼짐은 추가만 멈춘다(차단·예외면 나머지 건너뜀). 추가 단계 줄은 전부 `[추가]` 머리(SystemExit 원문의 `[FAIL]` 은 옮기지 않음).
  끝에 한 줄 다시 `[PASS] 4개 다운로드·검사 통과 → <폴더> · 추가: 성별 받음 · 연령대 받음 · 변경이력 받음`(실패면 `<종류> 실패(<원인>)` · 차단 `차단(<원인>) — 나머지 건너뜀` · 예외 `예외(<종류>) — 나머지 건너뜀`) +
  `다음:` 줄(`ingest.sh "<폴더>"/*.csv → 1x "$PY" scripts/extras.py store "<폴더>/extra" → "$PY" scripts/extras.py combine --out work/extra`). 4개가 실패(exit 2·1)면 추가 수집은 돌지 않는다.
- 파일 자리: 임시 `<download_dir>/partial/<날짜>-extra/`(4개 `partial/<날짜>/` 와 따로 — 4개 성공 뒤 `partial/<날짜>/` 를 되살리지 않는다) → 검사 통과분만 `<성공 폴더>/extra/`(ingest.sh `"<성공 폴더>"/*.csv` glob 밖) +
  `extra/summary_extra.json`(받음·실패·건너뜀 · 검사 · 차단 사유 · `[추가]` 로그 — 아이디 0). A `--debug`·실패 컷은 `<성공 폴더>/extra/debug/`(4개 `debug/` 와 섞지 않음). 검사 못 넘은 파일은 `partial/<날짜>-extra/` 에만.
  같은 날 다시 돌면 `<성공 폴더>/extra/` 를 새로 만든다(summary_extra 와 파일이 어긋나지 않게).
- A 검사(`check_extra`): 첫 줄 HEAD_RE · 첫 줄 이름 = 목록 이름 · 기간 = 기대 · 계정 / **2행 = config `extras.reports[이름].columns` 원문 정확 일치**(`kind_of`·`kind_by_columns` 안 씀 — 종류는 목록 이름으로 정한다) / 행 ≥ 1 / 일별 ⊂ 헤더.
  노출 합 ≠ 키워드(제외 전) 합은 WARN 만(첫 실측 기록 — 막지 않음). B 검사: 화면 기간 끝 = 오늘(주소에 기간이 붙었거나 화면이 바뀌면 실패) · 머리줄 = config(다르면 칸 수·다른 자리 수만 — 셀 원문 0) ·
  일자 꼴 `YYYY.MM.DD. HH:MM` · 빈 셀이 아예 빠진 줄(SYSTEM — 셀 4개)은 셀 `r` 속성의 열 글자로 놓는다.
- 설정(config `extras`): `subdir`(extra) · `archive_dir` · `reports`{이름: `kind` · `dim` · `columns`(다운로드 CSV 2행 원문 — 2026-10-12 구현 리허설 첫 `--debug` 실측 21칸: `캠페인유형`(붙여 씀) … `총비용` + 전환 12칸) · `every` daily · `dated`} · `gender_age`{`min_imps` · `show_unknown` · `unknown`} ·
  `history`{`kind` · `url`(쿼리 없음 · `list_url` 과 같은 출처) · `columns`(엑셀 머리줄 원문) · `actor_rules` · `ledger` · `show` · `show_system` · `max_rows`}. **설정 오류**(이름·종류가 4개와 겹침 · 종류끼리 접두 ·
  이름에 `forbidden_actions` 낱말 · columns·dim 없음 · URL 없음/쿼리/다른 출처 · 꼴)는 `fetch_config` 가 맨 위에 `[주의] extras 설정: <이유> — 추가 수집 끔(4개는 그대로)` 을 찍고 추가만 끈다 —
  SystemExit 0(S0 블록의 `fetch_config()` 도) · 끝 줄 `[PASS] … · 추가: 꺼짐(extras 설정 오류 — 맨 위 [주의] 줄)`.
- `--dry-run`: 할 일 표 뒤에 추가 표(`| A1 | 성별 보고서 | 성별 | 예(매일 · `이번달` 시작~끝) | <성공 폴더>/extra/ | 보관 끝 YYYY.MM.DD.·보관본 없음 |` · `| B | 변경 이력(<url>) | 변경이력 | 예(매일 · 화면 기본 30일 · 끝 = 오늘) | …/extra/변경이력.csv | 원장 N줄 · 마지막 날 · 기록 구간 끝 (경로) |`) —
  브라우저 0 · 폴더 0 · 보관·원장은 읽기만.
- 그 뒤(1x — `scripts/extras.py`, 저장소 밖): `store "<성공 폴더>/extra"`(summary_extra 의 받음만 — A → `<archive_dir>/YYYY-MM/<종류>.csv` 정확한 이름 하나 · 두 달 걸침·끝이 보관본보다 이른 파일·2행·이름 다름은 거부(`[주의]` — 보관본 그대로) ·
  임시 파일 → 이름 바꾸기 · 바뀌면 옛 것 `<종류>.csv.bak` / B → 원장 병합: 같은 줄(6칸 원문) 개수를 세어 새 쪽이 많은 만큼만 끝에 더함(같은 엑셀 두 번 = +0) · 기존 바이트 그대로 · 쓰기 전 `.bak-<시각>` ·
  기록 구간 `covered.csv` 에 [화면 시작, 받은 날 − 1] 추가(같은 구간이면 안 적음) · 구멍이면 `[주의] 원장 구멍 M/D~M/D`) → `combine --out work/extra`(종류마다 보관 조각을 **일 단위로** 이어 `work/extra/<종류>.csv`
  첫 줄 `"<종류> 합본(시작~끝),2580077"` — 빈틈·겹침이면 마지막 연속 구간만 + `[주의] <종류> 빈틈 M/D~M/D — M/D부터만`(겹침이면 `겹침`) · 원장·기록 구간 바이트 사본 `work/extra/변경이력.csv`·`변경이력_기록구간.csv` ·
  시작에 이 이름들만 지움 — 지난 회차 값이 남는 길 0) · `seed <엑셀> --start YYYY-MM-DD --end YYYY-MM-DD [--dry-run]`(처음 한 번 — 손으로 받은 엑셀 · 기록 구간 = [start, end − 1]).
  첫 줄에 쓰는 경로와 덮어쓰기 표시(`(config)` / `(환경 변수 SAERO_EXTRA_ARCHIVE 로 덮어씀 — 시험·리허설 전용)` / 인자 `--archive`·`--ledger`). 종료 코드 store·combine = 0(문제는 `[주의]`) · 2 = 사용법 · seed 는 시드 안 함이면 1.

## 5. 오류 대처

| 증상 | 조치 |
|---|---|
| `[FAIL] 목록 URL에 도달하지 못함 … --login` (exit 1) | 로그인 세션 만료 → `"$PY" scripts/fetch_reports.py --login` 다시(Code 탭은 백그라운드, 사용자가 창에서 로그인) → 본 실행 |
| `[FAIL] 허용 목록 밖 동작` / `금지 요소 클릭 시도 차단` (exit 1) | 코드가 클릭 직전에 멈춘 것(설정 변경 방지). 화면이 바뀐 신호 — 아래 "화면 변경". 이 경로엔 **summary.json이 없다**(`--debug`여도 — SystemExit가 summary 작성 전에 끝남). 메시지의 동작·요소 문구를 보고 · 재실행 전에 `partial/<날짜>/`를 읽는다(재실행이 지운다) · `--debug` 없이 `debug/`가 있으면 앞 보고서 실패 컷(차단 화면 아님 — 차단 순간 컷은 없다) → `--debug` 재실행은 사용자 결정 |
| `목록에 보고서 링크 '…' 없음` | 목록의 보고서 이름과 config `report_names` 키가 다른지(스크린샷 `*_no_link.png`) |
| `… 클릭 실패: TimeoutError: 요소 비활성(disabled)` / `다른 요소가 가림` / `보이지 않음` | 클릭은 `timeout_sec.click`(15초)만 기다리고 원인을 적는다. 비활성은 화면 상태(예: 결과가 아직 없음), 가림은 팝업·공지가 떠 있는 것 — 세션이 `summary.json`의 `error_detail`(Playwright 호출 로그)과 `debug/`를 직접 읽는다 |
| **크래시 = 프로필 다운로드 기록**: 같은 프로필 2회째 실행부터 `다운로드` 순간 크롬 창이 꺼짐(0xC0000005) → `TargetClosedError: … has been closed`, 나머지 보고서 `링크 없음` | 원인은 프로필 다운로드 기록에 남은 **이미 지워진 Playwright 임시 파일 경로**(검증 보고 2026-09-28 — 그 기록만 지우면 정상, 번들 헤드리스는 기록을 안 남김). 실행마다 브라우저를 띄우기 전에 `clean_download_history`가 `Default/History`(없으면 프로필 바로 밑 `History`)에서 **파일이 없는 기록만** 지우고 콘솔·`summary.json` `steps`에 `[profile] 다운로드 기록 정리: 파일 없는 기록 N건 삭제 …`를 남긴다(실제 파일이 있는 기록은 유지). `[WARN] 프로필 정리: … 브라우저가 떠 있음`/`잠김`이면 이 프로필로 뜬 크롬 창을 모두 닫고 다시 실행 |
| `보고서 화면(돌아가기 버튼)이 뜨지 않음` · `기간을 읽지 못함` · `프리셋 … 없음` · `확인/조회하기/다운로드 버튼을 찾지 못함` · `다운로드가 시작되지 않음` | **화면 변경**: 세션이 `partial/<날짜>/summary.json`을 **재실행 전에** 직접 읽고(재실행이 partial을 지운다) 원인을 보고 → 사용자가 정하면 `--debug`로 다시 돌려 세션이 `debug/`(png·`.aria.txt`·`.inventory.json`)를 직접 읽는다 → 문구·순서를 고친다(config `period_opener`·`download_menu_item`·`allowed_actions` 값으로 고칠 수 있는 범위면 config만). 로그인 실패 산출물(`not_logged_in.*`)은 열지 않는다(자동 채움 입력값이 담길 수 있음) · 변경 이력 화면 컷도 열지 않는다(B 는 컷을 찍지 않는다 — 있으면 코드가 바뀐 것, 변경자 아이디가 보인다) |
| `[추가] …` 줄 · 끝 줄 `· 추가: <종류> 실패(<원인>)`·`차단(<원인>) — 나머지 건너뜀`·`예외(<종류>) — 나머지 건너뜀`(2026-10-12 — exit 은 4개로, 0) | 멈추지 않는다(4개는 그대로 1단계로). 원인은 `<성공 폴더>/extra/summary_extra.json`(`reports[].error`·`history.error`·`blocked`)과 `[추가]` 줄로 본다. A 는 4개와 같은 대처(위 행들 — 컷은 `extra/debug/`), B 의 `` `다운로드` 후보 N개 — 1개여야 `` · `화면 기간 … 끝이 오늘 … 이 아님` · `엑셀 확인 실패: 엑셀 머리줄이 config history.columns 와 다름(…)` 은 화면·파일 꼴이 바뀐 신호 — config `extras` 값으로 고칠 범위면 config 만(설계 회차) |

| 위로도 셀렉터가 안 잡히면(왕복 3회) | 로그인된 전용 프로필로 **녹화**하고 세션이 그 파일을 읽는다(녹화 중 **로그인·비밀번호 입력 금지**, 이미 로그인된 프로필이라 필요 없다): |

```
python -m playwright codegen --channel chrome --user-data-dir "C:\Users\<사용자>\saero-fetch\chrome-profile" --target python -o "C:\Users\<사용자>\saero-fetch\codegen_<날짜>.py" "https://ads.naver.com/manage/ad-accounts/2580077/sa/reports"
```
창에서 보고서 하나만 **열기 → 기간 클릭 → 프리셋 → 확인 → 조회하기 → 다운로드 → 돌아가기**를 한 번 하고 창을 닫는다. `codegen_<날짜>.py`에 Playwright가 기록한 로케이터(`get_by_role`·`get_by_text` …)가 남고, 세션은 그것으로 `locate()`의 문구·역할을 확정한다. 세션은 녹화 파일에 아이디·비밀번호가 없는지 먼저 확인하고 읽는다.

| `[WARN] … 일별 합계가 다름(재집계 가능성)` | 막지 않는다. store 뒤 combine·validate가 실제 값으로 다시 검사한다. 자주 나면 재집계 기록으로 last-audit에 남긴다 |
|---|---|
| `[WARN] 파일명 … ≠ 기대` | 다운로드 파일명 규칙이 바뀐 것 — 내용 검사가 통과했으면 그대로 쓰고, 세션에 알린다 |
| `playwright가 없습니다` | 1절 설치. Python 3.14 대처법도 1절 |
| `channel=chrome 실행 실패 → 번들 크로미움으로 재시도` | 크롬이 없거나 실행 중 프로필 잠김. 크로미움으로 계속되면 그대로 두어도 된다(같은 프로필 폴더를 두 브라우저가 번갈아 쓰면 프로필이 깨질 수 있으니 한쪽으로 고정: `browser_channel`) |
| 창이 뜬 채 멈춤 | 네이버 쪽 팝업·공지가 떠 있으면 사용자가 닫는다(코드는 허용 요소만 클릭하므로 스스로 닫지 않는다). 시간 초과(`timeout_sec.page` 40초·`download` 90초)면 그 보고서 실패로 넘어간다 |

## 6. 금지 사항 (config `forbidden_actions` + 코드 규칙, checklist "되돌리면 안 되는 것")

- 코드는 `allowed_actions`(보고서 열기·기간·프리셋·확인·조회하기·다운로드·돌아가기) 밖의 요소를 **절대 클릭하지 않는다**. `+ 새 보고서`·`보고서 형식 저장`·항목 ×/끌어놓기·`삭제`·로그인 폼·계정/충전/결제 메뉴 문구가 든 요소는 클릭 직전에 막고 멈춘다(`click_allowed`). 클릭 호출은 코드에 한 곳뿐이다.
- (추가 수집, 2026-10-12) **변경 이력 화면의 클릭은 `다운로드` 하나**(보이는 후보가 정확히 1개일 때만 — 2개 이상·0개면 클릭하지 않고 실패) — `검색하기`·`열 맞춤 설정`·필터·기간 바꾸기 0. 이동은 config `history.url` 로의 `page.goto` 하나(쿼리 없는 경로).
  추가 단계의 금지 문구 차단은 추가만 멈춘다(4개 결과·exit 그대로 — 4-1절). 추가 보고서 이름에 `forbidden_actions` 낱말이 들면 설정 오류로 추가 수집을 끈다. 추가 보고서 형식을 저장·고치는 것은 사용자 몫(코드 0).
- 좌표 클릭·키 입력(`mouse`·`fill`·`type`·`press`)·드래그 0. 로케이터는 role·text만.
- 자격 증명·API 키·쿠키를 코드·config·저장소·채팅·summary·스크린샷 파일명 어디에도 두지 않는다. 로그인은 사용자가 창에서.
- 검사 통과 전·부분 실패에는 `archive.py store`를 하지 않는다. partial 폴더의 파일은 쓰지 않는다.
- 두 달에 걸친 기간을 만들지 않는다(프리셋 2개만 쓰고, 기간을 직접 입력하는 코드가 없다). `store --force`·`--chunk`를 자동으로 붙이지 않는다.
- 헤드리스로 돌리지 않는다(사용자가 보는 창). 같은 프로필로 두 실행을 동시에 돌리지 않는다.
- 진단·검증 회차는 `--dry-run`과 `tests/test_fetch_reports.py`(가짜 화면)만 — 실제 광고주센터 실행은 사용자 PC·사용자 승인 뒤.

## 7. UI 실물 [실측: 사용자 스크린샷 3장, 2026-09-28 탐색 기준선 6-5] — 코드가 기대하는 문구

- 목록 `…/ad-accounts/2580077/sa/reports`: 제목 `다차원 보고서`, 주황 띠 `최근 집계 완료 시간 : YYYY.MM.DD. HH:MM`, 버튼 `+ 새 보고서 ∨`(금지), 표 `보고서 이름 | 통계기간 | 생성일 | 최근 열람일 | 생성자` — 행 4개 `시간대별 보고서`·`상세지역 보고서`·`검색어 보고서`·`필라테스 보고서`(= `report_names` 키, 링크 텍스트), 통계기간 열 전부 `이번달`(사용자가 09-28 저장 ①).
- 보고서 화면: `← 돌아가기` · `보고서 형식 저장 ∨`(금지) · `다운로드` · 기간 `YYYY.MM.DD. → YYYY.MM.DD.` + 달력 아이콘 + `<` `>` · `조회하기`(조회 전 회색). 기간 팝업: 프리셋 `어제·이번주·지난주·전 영업주·최근 7일 (오늘 제외)·이번달·지난달·이번 분기·지난 분기·최근 30일 (오늘 제외)·최근 90일 (오늘 제외)·최근 365일 (오늘 제외)` · 시작/끝 입력칸 · `취소`·`확인`.
- 다운로드 파일: 스크립트가 받으면 **`<이름>,2580077.csv`**(예 `시간대별 보고서,2580077.csv`, Playwright `suggested_filename` — 왕복 3 실측), 손으로 받으면 `<보고서명>_보고서_2580077.csv`(탐색 ③). 내용은 같다: 첫 줄 `"<이름> 보고서(YYYY.MM.DD.~YYYY.MM.DD.),2580077"`, utf-8-sig·LF, 2행 컬럼 = config `columns`(1절 실물) [실측 ③·왕복 3].
- 왕복 1~3으로 확정된 것 [실측]: 목록 링크 텍스트 = `report_names` 키 · `돌아가기` 문구로 보고서 화면 판정 가능 · 기간은 **텍스트**(`range-text`)이고 보고서 정의 로드 뒤 늦게 그려진다 · 저장된 형식으로 열면 **자동 조회**되고 `조회하기`는 비활성 · `다운로드`는 버튼 하나(메뉴 없음, `download_menu_item` 불필요) · 비용 합계는 보고서마다 몇 원 다르다(314,902~314,910 — 행 단위 반올림, 검사 대상 아님).
- [미실측] 매월 1일 경로(기간 텍스트 클릭 → 팝업 → `지난달` → `확인` → `조회하기` 활성) — 10월 1일 첫 실행이 확정한다. 안 되면 `period_opener`(달력 아이콘 이름) 후보.
- (2026-10-12 추가 수집) 목록 6행 [실측: 사용자 캡처 10/12] — 맨 위 `연령대 보고서`·`성별 보고서`(사용자 저장 — 캠페인 + 일별 + 연령대 / 성별, 통계기간 `이번달`) + 기존 4개(이름·순서 그대로). 저장 창 "보고서 형식 저장하기"에 통계기간 `이번달`(상대)이 함께 저장된다.
  성별 보고서 기본 칸 = 캠페인 유형 · 캠페인 · 일별 · 성별 + 노출수 · 클릭수 · 클릭률 · 평균 CPC · 총비용(+ 전환 칸) · 성별 값에 `남성`·`알 수 없음` 보임 — 2행 원문은 config `extras.reports[…].columns`(2026-10-12 리허설 실측 — 화면 칸 이름은 `캠페인 유형`(띄어 씀)이지만 CSV 2행은 `캠페인유형`(붙여 씀) · 값 집합 [실측] 성별 `남성`·`여성`·`알 수 없음` / 연령대 `14세 ~ 18세`…`60세 ~ 99세` 10구간·`알 수 없음` · 캠페인유형 `플레이스`·`파워링크`).
- (2026-10-12 추가 수집) **변경 이력 관리**(도구 › 변경 이력 관리 — `…/ad-accounts/2580077/sa/tool/history`, config `extras.history.url` · 쿼리 없음) [실측: 사용자 캡처·표본 엑셀 85줄, 2026-10-11 탐색]: 기간 `YYYY.MM.DD. → YYYY.MM.DD.`(기본 = 오늘 포함 30일) ·
  필터(변경 유형 · 캠페인 · 광고그룹 · 대상 ID) · `검색하기` · 표 위 `⤓ 다운로드` · `열 맞춤 설정` — 받은 파일 `이력 목록 YYYYMMDD HHMM.xlsx`(형식 고르는 창 없이 바로). 엑셀: 시트 `Sheet` · 공유 문자열 ·
  머리 `변경일자,변경 유형,변경자,캠페인,광고그룹,변경 내용`(= config `history.columns`) · 일자 `2026.10.11. 07:59`(분 단위 — 같은 분에 여러 줄) · SYSTEM 줄은 캠페인·광고그룹 셀이 아예 없음(셀 4개) ·
  변경 내용은 여러 줄(둘째 줄 = `변경 전`·`설정 값`·`등록된 내용`·`삭제된 내용`) · 변경자 = `SYSTEM` / `<ID>:naver`(사람) / `<ID>:naver(API)`(스킬 — 제외 검색어 등록) — **아이디는 받는 즉시 주체 낱말로 바꾸고 버린다**(4-1절).

## 8. 시험 (검증·진단 회차용, 네트워크 0)

`"$PY" tests/test_fetch_reports.py` — 실 CSV 4개로 검사 함수(기대 기간은 `data/2026-09` 헤더에서 읽는다 — 이번 달 파일이 갱신돼도 안 깨짐), 가짜 `playwright` 패키지로 `--dry-run` 브라우저 0·폴더 0, `click_allowed` 금지 차단·소스의 클릭 호출 1곳, `tests/fixtures/report-ui-fixture.html`(광고주센터 문구·흐름을 흉내 낸 로컬 화면, `login.html`은 `?auto=1`이면 1.5초 뒤 "사용자가 로그인한 것"으로 처리)에서 헤드리스로 `--login` 도달 → 4개 다운로드 성공(저장된 `이번달`이라 프리셋 클릭 0) → 매월 1일(`--today 2026-10-01`) `지난달` 프리셋 경로 → `--prev` WARN(막지 않음) → 보고서 이름 하나 틀리면 exit 2·정상 폴더 없음·partial 3개 → 로그인 안 됐으면 exit 1 → 프로필 정리(가짜 History DB: 파일 없는 기록만 삭제·파일 있는 기록 유지·DB 없음/잠김 WARN) → `browser_channel` 그대로(null = 번들 크로미움 — 시험은 null이라 설치 크롬을 쓰지 않는다). 끝에 실제 `data/2026-09`·config md5 전/후 출력.
(2026-10-12 추가 수집) 같은 파일의 `ExtrasConfigTests`(실제 config 유효 · 설정 오류는 추가만 끔 · S0 줄 · 클릭·`goto` 자리 · dry-run 추가 표·쓰기 0)·`ExtrasBrowserTests`(목록 `?extra=1` · `tests/fixtures/history-fixture.html` · `tests/xlsxfix.py` 가짜 엑셀 —
성공 뒤 store·combine · 추가 실패 격리 · 금지 문구 차단 · 머리줄 다름 · 브라우저 꺼짐·닫기 예외에도 4개·exit·`partial/<날짜>/` 그대로)와 `tests/test_extras.py`(보관·원장·합본·엑셀 읽기).
가짜 화면은 실제 사이트와 무관하다 — 실제 DOM의 문구·구조는 첫 PC 왕복(`--debug`)으로만 확정된다.

## 9. PC 왕복 기록 (구현 회차 — 2026-09-28 main 병합 730aa45로 끝남)

구현 회차의 브랜치 왕복 절차는 병합으로 끝났다(지금은 Code 탭 세션이 작업 폴더에서 직접 돌리므로 브랜치를 받아 첨부하는 왕복이 없다). 아래는 당시 기록이다.

왕복 1(2026-09-28, PC Python 3.12·pip 25.0.1·Playwright 1.63.0·크로미움 v1243·설치된 크롬 channel) [실측: 사용자 콘솔 화면 2장]: 설치·`--dry-run`·`--login`(`[OK] 목록 URL 도달 · 4/4개`) 통과. 본 실행은 `시간대별 보고서` 링크 클릭 → `돌아가기` 확인(보고서 열림)까지 되고 **기간 텍스트를 못 읽어** 실패, 그 뒤 목록 복귀가 없어 나머지 3개가 `링크 없음`(코드 결함 → `back_to_list` 신설). 실제 기간 표시 DOM은 아직 [미실측] → 왕복 2는 `read_period` 3단계 폴백 + `.aria.txt`·`.inventory.json`으로 확정한다.

왕복 2(2026-09-28, 콘솔 전문) [실측]: 4개 모두 `보고서 열림` → `기간 읽음 2026.09.01.~2026.09.27. (range-text)` → `기간 = 기대(저장된 프리셋)`(기간 표시는 지연 대기로 해결, 실제 표기 = 기간 텍스트) → 목록 복귀도 정상. 실패는 `클릭 query: '조회하기'` → `TimeoutError: Locator.click: Timeout 30000ms exceeded.` 4/4 — 클릭 가능해지길 30초 기다린 것이므로 **저장된 형식으로 열면 자동 조회되고 `조회하기`가 비활성**이라고 판정(6-5 "회색 — 조회 전"·수동 흐름 "열기 → 다운로드"와 일치) [추론 → 왕복 3이 확정]. 수정: 활성일 때만 클릭, 클릭 대기 `timeout_sec.click` 15초, 실패 원인(비활성/가림/안 보임)을 출력·`error_detail`에 호출 로그.

왕복 3(2026-09-28, 콘솔 전문) [실측]: **성공** — 4개 모두 `조회하기 비활성(저장된 형식으로 이미 조회됨) → 건너뜀` → `다운로드` → 저장 → `돌아가기`, 검사 전부 PASS(시간대별 24행 · 상세지역 1,017행 · 검색어 1,532행 · 키워드 462행, 헤더 4개 `(2026.09.01.~2026.09.27.),2580077`, 노출합 7,628 = 7,628 = 7,628, 클릭 259, 검색어 노출 6,451), `downloads\2026-09-28\`로 이동. 남은 WARN은 파일명(`시간대별 보고서,2580077.csv` ≠ 옛 기대 `_보고서_`) 4건 → 실측 이름을 기대값으로 바꿔 해소.
