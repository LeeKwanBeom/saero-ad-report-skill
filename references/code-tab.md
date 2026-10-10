# Code 탭 실행 규약 — 수집부터 배포·등록·기록까지 한 세션 (정본)

데스크톱 앱 Code 탭(Claude Code, 이 PC 로컬 셸) 세션 하나가 ① 보고서 수집(`fetch_reports.py`) → ② 보관·합본·갱신·배포(SKILL.md 1~8단계)
→ ③ 제외 검색어 등록(5-0단계)을 **같은 작업 폴더에서** 잇는 방법이다. SKILL.md는 무엇을 하는지, 이 문서는 이 PC에서 어떻게 치는지를 적는다 —
둘이 어긋나면 둘 다 고친다. 근거: `audit/last-audit.md` "기능 추가 탐색 기준선(Code 탭 전 단계 실행, 2026-09-28)" 0~7절.
채팅(웹·Cowork)은 쓰지 않는다 — 네이버 API가 403이고(exclusion-ui.md 3절), SKILL.md 맨 위 채팅 가드가 멈춘다.

## 0. 진입

- Code 탭은 **`D:\saero` 폴더로 연다**(저장소 폴더로 열지 않는다 — 메모리 D--saero·wrapup이 안 붙는다). 첫 말은 **`/saero-run`**.
  진입 스킬 `D:\saero\.claude\skills\saero-run\SKILL.md`와 `D:\saero\CLAUDE.md`, 질문 다듬기 스킬 `D:\saero\.claude\skills\prompt-polish\`(세 파일)의 정본 사본은 저장소 `local/`에 있다(설치·갱신은 사용자가, 마감 때 md5 대조).
- 작업 폴더는 **`D:\saero\saero-ad-report-skill`(main) 하나**. 명령은 전부 여기서(Git Bash `cd /d/saero/saero-ad-report-skill`).
  Desktop 사본·검증용 clone·스크래치는 운영에 쓰지 않는다. 기능 브랜치 작업은 별도 clone에서 하고 작업 폴더는 main만.
- 설치본 부트스트랩(`anthropic-skills:saero-ad-report`)은 이 PC에서 **1절(컨테이너 작업 경로로 `cd` 뒤 `rm -rf`·`git clone`)을 돌리지 않는다.**
  Skill 도구로 부르지 않고, 그 컨테이너 경로(SKILL.md 채팅 가드 문장의 경로)를 이 PC에 만들지 않는다 — Git Bash에선 Git 설치 폴더 아래로 풀린다.
  CSV·리포트 말에 자동으로 걸려도 이 문서를 따른다.
- 마감은 wrapup(`마감`). 회차 기록 양식은 SKILL.md 8단계.

## 1. 환경

| 항목 | 값 |
|---|---|
| 파이썬 `PY` | 저장소 밖 venv `D:\saero\.venv\Scripts\python.exe`(Git Bash `/d/saero/.venv/Scripts/python.exe`) — `--system-site-packages`(시스템 playwright를 본다) + pandas 2.x. 만들기(사용자 승인 뒤 한 번): `python -m venv --system-site-packages D:\saero\.venv` → `D:\saero\.venv\Scripts\python.exe -m pip install "pandas>=2.2,<3"` |
| 금지 | `python3`(이 PC Git Bash에선 Microsoft Store 스텁, exit 49) · 시스템 `python`으로 ② 실행(pandas 없음) |
| 셸 상태 | Bash 도구는 호출 사이에 env가 이어지지 않는다 → **매 호출 첫머리** `export PY=/d/saero/.venv/Scripts/python.exe PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never; unset GIT_ASKPASS SSH_ASKPASS` (자격 증명 창·프롬프트로 멈추지 않게 — push·fetch는 `git -c credential.interactive=false …`. `PYTHONDONTWRITEBYTECODE`는 `__pycache__`를 만들지 않게) |
| 인코딩 | 도구 파이프는 cp949 — 스크립트는 stdout·stderr를 utf-8로 바꾸지만 인라인 파이썬·heredoc까지 덮으려고 `PYTHONUTF8=1` |
| 시각 | KST = `TZ=KST-9 date` (이 PC Git Bash에는 zoneinfo가 없어 `TZ=Asia/Seoul`은 **UTC**를 낸다) |
| git 신원 | 이 PC에는 없다 → 커밋은 `git -c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com commit …`(`ingest.sh`는 없을 때 스스로 붙인다) |
| 자격 증명 | **이 PC git 자격 증명 하나**(GCM, `credential.helper=manager`) — 스킬 저장소 `git push`와 배포 PUT(`deploy.py`가 `git credential fill`로 얻어 변수에만 둔다) 둘 다. 토큰 파일·대화창 토큰 0. 세션은 `git credential fill`을 직접 치지 않는다 |
| 네이버 API 키 | 키 파일 `~/naver-api.keys.json`(저장소 밖) — `--key-file` 경로만 넘긴다. 세션은 열지도 출력하지도 않는다(`test -f`로 존재만) |
| 수집 폴더 | config `report_fetch.download_dir` `~/saero-fetch/downloads` · 전용 프로필 `profile_dir` `~/saero-fetch/chrome-profile`(`~` = 사용자 홈) |
| 회차 작업물 | 저장소 `work/`(gitignore): `work/combined/` · `work/prev.html` · `work/index.html` · `work/compute.json` · `work/exclusions_proposal_<창시작>_<창끝>.md`·`_candidates.txt`·`_industry.txt`(propose — 창이 다르면 다른 파일) · `work/approved_<날짜>_<시분초>.txt`(push 참조 선택 모드 — 실제 push만, 덮어쓰기 없음) · `work/exclusions_proposal_<창시작>_<창끝>.md5`(propose 출처 기록) · `work/precheck_ok.md5`(precheck 통과 도장) · `work/exclusions_pull_<날짜>.json` · `work/balance.json`(5단계 광고비 잔액 기록 — balance.py 가 매 회차 지우고 다시 쓴다, 판 F) |
| 줄바꿈 | `.gitattributes`: `*.csv -text`(바이트 그대로) · `*.sh text eol=lf`. 작업 폴더가 커밋과 다르게 풀려 있으면 8절 "작업 폴더 줄바꿈" |
| 매출 작업 A·C(2026-10-10) | 주간 성과 장부 = config `leads.path`(저장소 **밖** `~/saero-leads/leads.csv` — 숫자 칸만, 공개 안 함, `leads.py` 만 쓴다) · 플레이스 체크리스트 = config `place_checklist.path`(저장소 `audit/place-checklist.csv` — 항목 id·상태·날짜만, 공개, `place.py` 만 쓴다 · 첫 실사용이 만든다). 둘 다 줄 추가만. 시험·리허설은 `--ledger`·`--checklist` 또는 환경 변수 `SAERO_LEADS`·`SAERO_PLACE` 로 스크래치(운영 회차는 쓰지 않는다 — 명령 첫 줄에 쓰는 경로가 찍힌다) |

## 2. S0 사전 점검 — Bash 한 번, 외부 쓰기·작업 트리 변경 0

아래 블록을 그대로 한 번에 돌린다. 줄마다 `[FAIL]`이면 다음 단계로 가지 않는다(다음 행동은 4절 ⓑ). 외부 쓰기·작업 트리 변경 0
(git이 `.git` 안 FETCH_HEAD·ref·commit-graph·index를, 파이썬이 gitignore된 `__pycache__`를 쓸 수 있다 — 블록의 `PYTHONDONTWRITEBYTECODE=1`이 뒤쪽을 막는다).
키 파일은 존재만 보고, 자격 증명은 값을 출력하지 않는다. 배포 저장소 줄은 인증 GET(읽기)으로 쓰기 권한(`permissions.push` — 계정 역할 기준, 토큰 범위는 PUT이 최종 확인)까지 본다.

```bash
cd /d/saero/saero-ad-report-skill && export PY=/d/saero/.venv/Scripts/python.exe PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never && unset GIT_ASKPASS SSH_ASKPASS && F=0 && {
git -c credential.interactive=false fetch -q origin || { echo "[FAIL] git fetch"; F=1; }
b=$(git rev-parse --abbrev-ref HEAD); [ "$b" = main ] || { echo "[FAIL] 브랜치 $b — main이어야 함"; F=1; }
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || { echo "[FAIL] HEAD ≠ origin/main — git status -sb 확인(push·pull은 사용자와)"; F=1; }
[ -z "$(git status --porcelain)" ] || { echo "[FAIL] 작업 트리에 변경 있음 — git status"; F=1; }
git diff --quiet HEAD -- data || { echo "[FAIL] data/가 HEAD와 다름(스테이징·미스테이징) — git status data/, 되돌리기는 4절"; F=1; }
x=$(git -c core.quotepath=false ls-files --eol -- '*.csv' '*.sh' | awk -F'\t' '{split($1,f," "); i=f[1]; w=f[2]; sub(/^i\//,"",i); sub(/^w\//,"",w); if(i!=w) print $2 (w=="" ? " (작업 폴더에 없음)" : "")}'); [ -z "$x" ] || { echo "[FAIL] 줄바꿈이 커밋과 다름(8절): $x"; F=1; }
"$PY" -c "import pandas, playwright" 2>/dev/null || { echo "[FAIL] PY에 pandas·playwright 없음: $PY"; F=1; }
h=$(TZ=KST-9 date +%H%M); [ $((10#$h)) -ge 100 ] || { echo "[FAIL] KST $h — 01:00 이후에(어제 집계 완료 전)"; F=1; }
test -f ~/naver-api.keys.json || { echo "[FAIL] 네이버 API 키 파일 없음(존재만 봄) — ③ 불가"; F=1; }
"$PY" -c "import sys; sys.path.insert(0,'scripts'); import fetch_reports as R; sys.exit(3 if R.profile_in_use(R.fetch_config()['profile_dir']) else 0)"; r=$?; [ "$r" -eq 0 ] || { [ "$r" -eq 3 ] && echo "[FAIL] 수집 프로필을 쓰는 크롬이 떠 있음 — 그 창을 모두 닫고 다시" || echo "[FAIL] 프로필 검사 실행 오류(rc=$r — 위 출력 확인)"; F=1; }
timeout 90 git -c credential.interactive=false push --dry-run -q origin HEAD:main || { echo "[FAIL] 스킬 저장소 push --dry-run — 자격 증명, 또는 HEAD ≠ origin/main이면 non-fast-forward(권한 문제로 단정하지 말 것)"; F=1; }
"$PY" scripts/deploy.py push --dry-run | tail -3; r=${PIPESTATUS[0]}; [ "$r" -eq 0 ] || { echo "[FAIL] 배포 저장소 점검 실패(deploy.py push --dry-run rc=$r) — 원인은 바로 위 줄(GET = 조회 / 자격 증명 / 권한 / 파이썬)"; F=1; }
echo "S0 $([ "$F" -eq 0 ] && echo PASS || echo FAIL)"; }
```

## 3. 전 단계 순서

기준: SKILL.md 1 → 2 → 2-1 → 3 → 4 → 5-0 → 5 → 6 → 7 → 8. **승인·등록·확인은 배포 앞**(사용자 결정 2026-09-28). 모든 Bash 호출은 1절 `export` 줄로 시작한다.

| # | 단계 | 명령(작업 폴더) | 멈춤 |
|---|---|---|---|
| S0 | 사전 점검 | 2절 블록 | ⓑ FAIL 줄 |
| ① | 수집 | `"$PY" scripts/fetch_reports.py --prev <직전 성공 폴더 또는 data/YYYY-MM>` — **run_in_background**(사용자 화면에 크롬 창이 뜬다, 3~5분). 달의 첫날은 `--prev` 생략, 10/1처럼 `지난달` 첫 실측·화면 변경 의심 때는 `--debug` | exit 1 로그인 → `--login`을 백그라운드로 띄우고 **사용자가 창에서 로그인** → 본 실행 다시 / exit 1 차단·exit 2 → ⓑ |
| 1 | 보관·합본·push | `scripts/ingest.sh "<성공 폴더>"/*.csv` — 성공 폴더 = fetch 출력 `[PASS] … → <폴더>`·`다음:` 줄(`partial/` 금지). 시작 검사(store 전): HEAD = origin/main · data/ = HEAD(`git diff --quiet HEAD -- data`) · data/에 추적 안 된 파일 0 · data/ CSV 줄바꿈 = 커밋 | ⓑ 시작 검사 FAIL(쓰기 0)·store 거부·combine FAIL·`[FAIL] HEAD ≠ origin/main` |
| 4 | 배포본 받기(2-1 전에 당겨서, 읽기) | `"$PY" scripts/deploy.py fetch --out work/prev.html && cp work/prev.html work/index.html` | ⓑ GET 실패 |
| 5a | 계산만(쓰기 = `work/compute.json`) | `"$PY" scripts/compute.py work/combined --competitors-html work/prev.html -o work/compute.json` — 2-1 대조를 형식까지 같게 하려고 당긴다(교체는 5단계) | ⓑ |
| 2-1 | 기간 대조 | `compute.json`의 `masthead` 문자열 ↔ `work/prev.html`의 `집계 기간<b>…</b>` | **같으면 ⓐ와 별개의 앞 질문 하나**(SKILL.md 2-1 문구) — 답에 따른 흐름은 표 아래 "2-1 같음" |
| 3 | 제외 그룹 | 합본 키워드로 SKILL.md "제외 그룹 판정" 규칙(세션 판정) | 신규 후보 → ⓐ 묶음 |
| 3a | 매출 작업 상태(읽기 — 쓰기 0) | `"$PY" scripts/leads.py status` → `STATUS ask5=yes\|no …`(지난주 = 합본 집계 끝 기준 다 찬 월~일 · 출력은 판정 낱말뿐 — `--numbers` 는 사용자가 물을 때만, 채팅에만) · `"$PY" scripts/place.py status` → `STATUS first=yes\|no ask7=<P 번호>\|none chat=N` | ask5=yes 면 ⓐ 에 (5) · 그 회차에 ask7 이 있으면 (7)도 · first=yes 면 C 첫 회 9항목은 **ⓐ 와 별도 메시지** · chat ≥ 1 이면 그 신호를 채팅으로 먼저(리포트에 또 적기 전 — 12번 작성 기준 5) |
| 5-0a | 후보 | (권장) `"$PY" scripts/exclusions.py pull --key-file ~/naver-api.keys.json`(읽기 — registry `verified_at`이 바뀐다, 커밋은 5-0c, 5-0c가 없는 회차는 8단계에서 함께) → `"$PY" scripts/exclusions.py propose work/combined --since YYYY-MM-DD` — propose `--since` = 직전 배포 masthead 끝 + 1일(ISO). 직전 회차 기록이 "등록 미룸"이면 그 회차 propose 창 시작(lo) — 미룬 이름과 새 이름을 한 묶음으로 올린다(first_seen 필터 때문에 끝 + 1일로는 미룬 이름이 다시 안 오른다). 기본 창은 마지막 하루뿐이라 쓰지 않는다. 산출물은 `work/exclusions_proposal_<창시작>_<창끝>.md`·`_candidates.txt`·`_industry.txt`·`.md5`(출처 기록 — push가 대조), 빈 창이면 `[주의] 빈 창` | ⓑ registry 없음 |
| ⓐ | **승인 묶음 한 번** | (1) 새 경쟁사 · (2) 애매 후보 · (3) 제외 그룹 · (4) 제외 검색어(propose 승인 문구 원문) 중 **해당하는 것만** 한 메시지. (1)~(4)·(5)·(7)이 모두 0일 때만 묻지 않는다((1)~(4)가 0 이고 (5)만 있으면 (5)·(7)만 한 메시지). 같은 메시지 끝에 **정보 질문**(승인 아님 — 4절): (5) 3a `leads.py status` 의 `(5) 질문:` 줄 그대로(ask5=yes 일 때만) · (7) `place.py status` 의 `(7) 질문` 줄(ask5=yes 이고 ask7 이 있을 때만) | (1)~(4)는 답을 기다린다 · (5)·(7)만 남은 질문이면 기다리지 않는다(4절) |
| 3b | 장부·체크리스트 쓰기(답이 왔을 때만) | (5) 숫자 답 → `leads.py add --inquiry N --trial N --signup N --naver N [--revenue N --place-visit N --call N --direction N --save N] --dry-run`(주는 넘기지 않는다 — status 와 같은 지난주) → 답 원문과 칸을 나란히 보이고(캡처에서 읽은 숫자는 "캡처에서 읽음" + 확인 답) → 같은 명령에서 `--dry-run` 만 뺌 / "건너뜀" → `leads.py skip` / "정정" → `add … --replace --week <월요일>`(옛 장부 `.bak-<시각>`) · (7) 답 → `place.py done P<n> --date YYYY-MM-DD --dry-run` → 실제 / C 첫 회 답 → `place.py set P1=done P2=todo … P6=later:YYYY-MM-DD --dry-run`(P1~P9 전부) → 실제 / 안 함·미룸·되돌림 → `place.py set P<n>=no\|later:<날짜>\|todo` | ⓑ add·skip·set·done `[FAIL]`(쓰기 0) |
| 5-0b | 답 반영 | config(`competitors`·`excluded_groups`)가 바뀌면 → config 커밋(push는 5-0c와 함께) → compute 재실행(경쟁사가 바뀌면 propose도 — **propose를 다시 돌리면 번호·출처 기록이 바뀌니 재승인**) | — |
| 5-0c | 등록·확인·기록 | 참조 선택 모드(6절) `exclusions.py push --from-candidates … [--drop …] [--industry … --industry-lines …] [--extra-csv work/combined/검색어.csv --extra-rows …] --expect N --dry-run`(답의 번호를 그대로 `--drop`·`--industry-lines`에 · 호출 0 · 파일 쓰기 0 · `[FAIL]` 0 · "승인 N개" = 답의 N · `[주의]` 쌍둥이는 사용자에게 보인다) → 같은 명령에서 `--dry-run` 대신 `--key-file ~/naver-api.keys.json`(pull → 고른 이름 중 하나라도 대상 그룹 전부에 이미 있으면 POST 0 FAIL(승인 파일 안 씀) → 승인 목록을 `work/approved_<날짜>_<시분초>.txt`에 쓰고 → POST → verify) → `exclusions.py report` → registry(+config) 커밋(커밋 전 `"$PY" scripts/leads.py guard --staged --message-file <메시지 파일>` → 통과면 `git commit -F <같은 파일>`) → `git fetch` → `git push origin main` → HEAD == origin/main | ⓑ `[FAIL] 승인 목록…`(쓰기 0) · exit 1(부분 실패·verified:false·요청 결과 모름·pull 뒤 이미 있음) → 재시도는 ⓐ |
| 5 | 교체 | (판 F — 앞 두 줄, 매 회차·2-1 같음 경로 포함) `"$PY" scripts/balance.py --key-file ~/naver-api.keys.json`(광고비 잔액 `GET /billing/bizmoney` 1회 — 읽기 · 시작에 옛 `work/balance.json` 을 지우고 새 기록을 쓴다 · 조회 실패면 `[주의] 잔액 확인 못 함(<사유>)` 과 실패 기록, exit 0 — 카드 "확인 못 함"으로 회차는 계속) → `"$PY" scripts/compute.py work/combined --competitors-html work/prev.html --balance work/balance.json --leads "$("$PY" scripts/leads.py path)" --place "$("$PY" scripts/place.py path)" -o work/compute.json`(5a 결과에 "잔액"·"성과장부"(판정 낱말만)·"플레이스전후" 를 더한 것 — 5a 는 `--balance`·`--leads`·`--place` 없이 그대로. 장부·체크리스트가 없으면 `[주의]` exit 0 — 판정 '확인 못 함' / 플레이스 행 0) → `"$PY" scripts/apply.py --layout --html work/index.html --compute work/compute.json`(기계 자리 + 잔액 카드 값·보조 줄 + 접기 summary 개수·날짜 + 레이아웃 판 — `--layout` 은 매 회차: 이미 그 판이면 변환 건너뜀(멱등), meta 없는 옛 판이면 변환. 앵커가 하나가 아니면 `[FAIL] apply:` exit 1, 작업본 그대로) → `"$PY" work/n<날짜>.py`(서술 — 저장소 밖 스크래치, 서술 표지마다 `rep('<자리>', 새 문장)` — 자리 이름은 `references/report-structure.md` "서술 표지" 표가 정본, 길이는 같은 문서 "서술 공통 규칙"). 12번 먼저, 11번 마지막. 07 각주 ②·11·12번에 **등록 n · 확인 a/b · 실패 n**(07 ② 형식 `제외 검색어: <M/D> 등록 N개 · 확인 a/b · 실패 n` — exclusion-ui.md 9절)을 사실 그대로. 12번 장부 행·플레이스 행은 서술 스크립트가 `leads.row_html(R)`·`place.rows_html(R)`(import — CLI `leads.py row`·`place.py row --compute work/compute.json` 은 보기용) 그대로 — 판정 낱말만, 장부 숫자 0(report-structure.md 12번 작성 기준 6)) | ⓑ `[FAIL] apply:` · compute `[FAIL] 잔액 기록…`·`[FAIL] 성과 장부` |
| 6 | 검증 | `scripts/precheck.sh work/index.html work/combined work/prev.html` — (작업본 옆 `work/balance.json` 을 validate·compute 에 `--balance` 로 · compute 에 `--leads`·`--place`(`leads.py path`·`place.py path` — 5단계와 같은 입력, compare "12 장부 기준 판정"·"12 플레이스 행"이 낡은 판정을 잡는다)) validate → compute+compare → overflow → **narrative**(매회차 서술 표지가 직전 배포본과 바이트 같으면 `[FAIL] 서술 미교체 <자리>`) — 전부 통과하면 `work/precheck_ok.md5` 도장(작업본 md5 · 직전 배포본 md5 · 모드 full\|pending, 작업본이 도중에 바뀌면 도장 없음). `tests/chart_check.py`(라이브 차트 — 판 C·D)는 precheck **밖**: 첫 적용 보류 회차에 운영 세션이 도장 뒤 돌린다(4절) | ⓑ 세션이 고치고 재실행 |
| 7 | 배포 | `"$PY" scripts/deploy.py push --file work/index.html --base work/prev.html --message "리포트 갱신: <기간>" --dry-run`(precheck 도장 · base 대조 · 자격 증명 · 쓰기 권한 참) → dry-run이 통과하고 남은 사람 질문이 없으면 **묻지 않고 바로**(자동 배포 — 4절) 같은 명령(dry-run 없이 — `--base` 필수, 도장의 작업본 md5 = `--file`·직전 배포본 md5 = `--base`일 때만 PUT) → `"$PY" scripts/deploy.py verify --file work/index.html --ref <push가 찍은 커밋>`(push 성공 줄 `배포 완료 커밋 <sha>`의 값 — ref 없는 GET은 PUT 직후 약 1분 옛 본문을 줄 수 있다, 2026-09-29 실측 2회). 레이아웃 판 게이트: `--file`·`--base` 의 `<meta name="report-layout">` 가 다르면 실제 push 는 `--layout-change` 없이 `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함`(dry-run 은 `[주의]`) — `--layout-change` 는 첫 적용 회차에 사용자 "배포" 답이 있을 때만(4절) | 자동 배포 — 남은 사람 질문이 있거나 사용자가 "보류"라고 했으면 PUT 없이 8 기록하고 끝냄 / ⓑ `[FAIL] precheck 통과본이 아님`·`[FAIL] 배포본이 4단계 fetch 뒤 바뀜`·`[FAIL] 레이아웃 판이 바뀜`(PUT 0)·권한 거짓·PUT 결과 모름(재PUT 금지 — verify 먼저)·409·403·404·verify 불일치(재PUT은 사용자) |
| 8 | 기록 | last-audit 갱신 회차 절(Edit — SKILL.md 8단계 양식, **propose 창 lo~hi · 등록 미룸(사용자) 여부** 포함 · (5)·(7)은 `입력됨(로컬)`·`건너뜀`·`미입력` / `P<n> M/D 바꿈`·`없음` 꼴만 — 답 원문·장부 숫자·캡처 숫자 0) → 1절 신원으로 커밋(경로 지정 add: `audit/last-audit.md` + 있으면 `audit/place-checklist.csv` · pull로 바뀐 registry가 아직 커밋 안 됐으면 `audit/exclusions.csv` · config) — **커밋 전 `"$PY" scripts/leads.py guard --staged --message-file <메시지 파일>`**(staged 추가 줄·커밋 메시지에 장부 라벨+숫자·장부 머리줄·최근 매출 값이 있으면 `[FAIL]` — 커밋 0, 그 줄을 고쳐 다시) → 통과면 `git commit -F <같은 파일>` · **마감(wrapup) 커밋 전에도 같은 guard** → `git fetch` → `git push origin main` → 스크래치 `git clone -c core.autocrlf=false`로 행수·md5 → 사용자 시크릿 창 확인 요청 | ⓑ push 실패 |

**3a·3b(매출 작업 A·C, 2026-10-10)는 매 회차**(2-1 같음 "다시 계산"·"미룬 등록만" 경로 포함 — 3 뒤에 3a, ⓐ 답 뒤에 3b). 3a 가 묻지 않으면 (5)·(7) 질문 0 · 3b 쓰기 0 이고 리포트 12번 장부·플레이스 행만 그 회차 compute 값으로 다시 쓴다.
재개 판정: 장부·체크리스트에 그 주·그 바꿈 줄이 있으면 쓴 것(`leads.py status` · `place.py status` 로 읽는다 — 기억으로 판정하지 않는다).

**재개·완료 판정은 대상의 현재 상태로 한다**(세션이 끊겼다 다시 시작할 때): 보관본 = `git fetch` 뒤 HEAD = origin/main(`ingest.sh`가 확인)이고 `git status --short -- data`가 빔 ·
등록 = `exclusions.py verify --key-file ~/naver-api.keys.json --approved <이번 회차 propose(.md5) 뒤에 생긴 가장 최근 work/approved_*.txt>`(그런 파일이 없으면 이번 회차 실제 push는 POST 전 — 승인 파일은 pull 재검사를 통과한 뒤 첫 POST 전에 생긴다.
registry note·기억으로 "등록 끝"이라 판정하지 않는다 —
note는 verify 뒤에도 "확인 전"이 남고, `--approved` 없는 verify의 "registry에 pending 0"은 판정이 아니다. 요청 도중 끊긴 push(`요청 결과 모름`)도 이것으로) ·
배포 = `deploy.py verify --file work/index.html --ref <커밋>`(push 성공 줄의 커밋 — 없으면 `git ls-remote https://github.com/LeeKwanBeom/saero-pilates-report HEAD` 값). state 파일·대화 기억은 근거가 아니다.

**2-1 같음**: 2-1 기간이 같으면 승인 묶음 ⓐ와 별개의 앞 질문 하나만 하고 답을 기다린다 — 답 "다시 계산" → 3 → 5-0a → ⓐ(해당만) → 5-0b(해당 시) → 5-0c → 5 → 6 → 7 → 8 /
"CSV 다시" → ① / "미룬 등록만"(직전 회차 기록이 "등록 미룸"일 때만) → 3 건너뜀 → 5-0a(`--since` = 미룬 회차 창 시작) → ⓐ → 5-0c → 5(07·11·12 문구만 — 잔액 세 줄(balance → compute `--balance` → apply)은 그대로 돌아 카드가 이번 회차 값) →
6(`--pending` 없이, 3번째 인자 = 이번 4단계 fetch) → 7 → 8.
(2-1 질문은 ⓐ 묶음에 넣지 않는다 — "다시 계산"·"미룬 등록만"이면 그 뒤에 ⓐ 묶음을 해당하는 것만 한 번 묻는다.)
2-1 같음 경로(기간이 같다)에서는 6단계 narrative 가 `[주의] 같은 기간 — 대조 생략` exit 0 으로 지나간다(같은 데이터라 서술이 같아도 정상) — 서술은 사람이 그 회차 사실로 다시 쓴다.

**예외 "등록은 나중에"**(사용자가 그렇게 말할 때만): 07·11·12번에 "제안함 — 등록은 사용자 결정으로 다음에"처럼 사실형 문구로 배포하고
`--pending`은 쓰지 않는다. 8단계 기록에 `propose 창 lo~hi · 등록 미룸(사용자): 예`를 남긴다. 미룬 이름은 **다음 회차**(새 데이터)의 propose를
`--since lo`(미룬 회차 창 시작)로 돌려 새 이름과 한 묶음으로 올리고, 같은 데이터로 미룬 등록만 하려면 위 2-1 답 "미룬 등록만"으로 간다
(4단계는 이미 그 회차 배포본을 새로 받았고, precheck 3번째 인자는 그 파일 — `--pending` 없이 통과한 뒤 재배포).

## 4. 멈춤 표

**ⓐ 사람 승인(남긴다)**: SKILL.md "승인이 필요한 지점" (1)~(4) · 2-1 같음 질문(ⓐ 묶음과 별개의 앞 질문 — 답 셋: 다시 계산 / CSV 다시 / 미룬 등록만) · 3단계 새 제외 그룹 ·
등록 실패 재시도·keep·한도 초과 재승인 · delete/test-roundtrip `--confirm`(사용자 입회) · 12번 N주 미반영 질문 ·
**(5)·(7)은 정보 질문(매출 작업 A·C, 2026-10-10 — 승인이 아니다)**: 답이 없거나 빠지면 그 주 장부 미입력 / 바꾼 것 없음으로 진행하고 쓰기 0(다음 회차 3a 가 다시 묻는다 — 장부 skip 줄은 사용자 "건너뜀" 답일 때만) — 자동 배포의 "남은 질문"에 세지 않는다. C 첫 회 9항목은 ⓐ 밖 별도 메시지이고 무응답이면 체크리스트 없음 그대로(12번 플레이스 행 0 · 다음 회차 다시) — 이것도 배포를 막지 않는다 ·
**배포는 묻지 않는다(자동 배포 — 사용자 결정 2026-09-30 "물어봐야 하는 거 다 물어보면 자동으로 배포까지")**: 위 ⓐ 질문에 모두 답을 받아 남은 것이 없고 6단계 precheck·7단계 dry-run이 통과하면 바로 실제 push → `verify --ref`.
남은 질문이 있으면(되묻기·등록 exit 1 재시도 등) 그 답 뒤로 미루고, 사용자가 그 회차에 "보류"·"오늘 배포 안 함"이라고 했으면 PUT 없이 기록하고 끝낸다(8단계 기록·마감이면 wrapup에 `배포: 보류(사용자 답 "<원문>")`).
검사 FAIL은 아래 ⓑ 그대로 — PUT 0으로 멈춘다. (옛 규칙 "배포할까요? — 배포 / 보류" 고정 질문(2026-09-29)은 이 결정으로 대체.)
**보류 뒤 같은 세션 재개 = 7단계부터**(2026-10-06): "보류"로 6단계 도장까지 하고 멈춘 뒤 같은 세션에서 사용자가 "배포"라고 하면 7단계(dry-run → push → verify)부터 —
작업본·직전 배포본이 그대로면 도장이 유효하다(deploy.py 가 도장 md5 = `--file`·`--base` 를 대조). 둘 중 하나라도 바뀌었으면 6단계부터.
리포트 글·모양을 바꾸는 기능의 **첫 적용 회차**(예: 글 줄이기 회차 1 — 경로 C "다시 계산", 직전 배포본에 서술 표지 없음)는 사용자가 첫 말에
"보류로 시작 — 6단계 도장까지만, 배포는 내가 말함"이라고 하고, 세션은 도장 뒤 작업본(`work/index.html`)을 사용자가 열어 보게 한 다음 "배포" 답에서 7단계로 간다.
**레이아웃 판을 바꾸는 첫 적용 회차**(회차 2 모양 — 직전 배포본에 `<meta name="report-layout">` 없음 · **판 C 첫 적용** — 직전 배포본 meta r2026-10-B · **판 D 첫 적용** — 직전 배포본 meta r2026-10-C · **판 E 첫 적용** — 직전 배포본 meta r2026-10-D · **판 F 첫 적용** — 직전 배포본 meta r2026-10-E)는 도장 뒤 작업본과 함께 전후 비교 페이지(구역 캡처 나란히)를 보이고,
(판 C·D·E) `"$PY" tests/chart_check.py work/index.html work/compute.json --base work/prev.html --out work/chart_<날짜>` 결과(전부 PASS · 390·1280 섹션 1·6 캡처 · PDF —
판 D 부터 같은 명령이 전후 비교 페이지 `work/chart_<날짜>/compare.html`(옛 판 · 새 판 모바일 접힘·펼침 · PC 나란히)도 쓴다 · 판 E 는 "01 모바일 터치 팝업(처음·펼침) = 누른 줄 날짜"
두 줄이 핵심 — 판 E 는 모양이 그대로라 비교 그림은 옛·새가 같다 · 판 F 는 compare.html 맨 앞 "상단 카드" 옛/새(1280·390)와 `상단 잔액 카드 한 줄 전체(판 F)` 두 줄 PASS 가 핵심 —
사용자에게 광고시스템 화면의 비즈머니 숫자와 카드 값(`[apply]` 출력 끝 `잔액 카드 …`)을 한 번 대조해 달라고 한다(쿠폰 포함 여부·끝자리 [미확인] — 2026-10-09 기준선))도 보이고,
사용자의 "배포" 답이 있을 때만 7단계 실제 push 에 `--layout-change` 를 붙인다(답 전에는 dry-run 의 `[주의] 레이아웃 판이 바뀜`만 — 세션이 스스로 붙이지 않는다).

**ⓑ 자동 검사 FAIL(멈추고 → 다음 행동)**

| FAIL | 다음 행동(세션) | 사람 |
|---|---|---|
| S0 줄 | 원인 한 줄 보고, 다음 단계 안 감 | 설치·창 닫기·자격 증명 로그인 |
| fetch exit 2 부분 실패 | `partial/<날짜>/summary.json`을 **재실행 전에** 읽고(재실행이 partial을 지운다) 보고서별 원인 보고 | 다시 받을지 |
| fetch exit 1 금지 차단·허용 밖 | summary.json은 없다(`--debug`여도 — SystemExit가 summary 작성 전에 끝남). 메시지의 동작·요소 문구를 보고 · 재실행 전에 `partial/<날짜>/`를 읽는다(재실행이 지운다) · `--debug` 없이 `debug/`가 있으면 앞 보고서 실패 컷(차단 화면 아님, 차단 순간 컷은 없다) → 원인 불명으로 보고 | `--debug` 재실행 여부 |
| fetch exit 1 로그인 | `--login` 백그라운드 → 끝나면 본 실행 | 창에서 로그인·2단계 인증 |
| store 거부·combine FAIL | 메시지 원문 보고. `--force`·`--chunk` 자동 금지. 월초를 놓쳐 지난달 끝이 비면 평일 fetch로는 못 채운다 → 8절 폴백. combine FAIL이면 store가 이미 바꾼 data/를 `git restore --source=HEAD --staged --worktree -- data`로 되돌리고(`??` 새 파일은 `git clean -n -- data`로 확인 뒤 정리) → 받을 폴더를 모두 모아 **한 번에** `ingest.sh` | 다시 받기·폴백 |
| store 부분 적용 | `git status data/`로 바뀐 파일 보고(커밋 안 함) — 새 달 폴더의 추적 안 된 파일(`??`)은 되돌리기가 지우지 않는다(`git clean -n -- data`로 목록만) | 되돌리기(`git restore --source=HEAD --staged --worktree -- data` — M·A·D 전부 HEAD로, 스테이징된 새 파일은 작업 폴더에서도 지운다. 입력은 data/ 밖이라 잃지 않는다)·`??` 파일 지우기 |
| ingest `[FAIL] HEAD ≠ origin/main`·브랜치(시작 검사면 쓰기 0) | 상태(`git status -sb`) 보고 | push·pull 결정 |
| ingest `[FAIL] data/가 HEAD와 다름`(시작 검사, 쓰기 0) | 함께 찍힌 `git status --short data` 보고 — 누가 바꿨는지(ingest 커밋 실패로 `A`가 남은 것일 수도) | 되돌리기(`git restore --source=HEAD --staged --worktree -- data`) |
| ingest `[FAIL] data/에 추적 안 된 파일이 있음`(시작 검사, 쓰기 0) | 찍힌 파일 목록 보고(store 부분 적용·손으로 둔 파일) | 지울지(`git clean -n -- data`로 확인 뒤) |
| ingest `[FAIL] data/ CSV 줄바꿈이 커밋과 다름`(시작 검사, 쓰기 0) | 이름 댄 CSV 보고 → 8절 "작업 폴더 줄바꿈" | 정리 승인 |
| push 403·거부(ingest `[FAIL] push 실패`) | 어느 저장소인지·커밋이 로컬에만 있는지 적어 보고 | 자격 증명 확인·재시도 |
| registry 없음 | `git status`·경로 점검 | — |
| exclusions `[FAIL] 승인 목록…`(쓰기 0) | 출력의 출처 목록·`[FAIL]`·`[주의]` 쌍둥이를 그대로 보이고 줄·행 번호를 사용자 답과 다시 맞춘다(이름을 쓰지 않는다). `후보 파일이 propose 산출물이 아님·propose 뒤 바뀜`·`propose 뒤 합본·registry가 바뀜`이면 **재시도 = 같은 `--since`로 propose 다시 → 새 `_candidates.txt`(`--industry`도 새 창 파일) → `--from-candidates … --expect <재승인 N>`**(번호가 바뀌니 새 승인 문구로 재승인) | 답 확인·재승인 |
| exclusions `[FAIL] 고른 이름 중 …개가 방금 읽은(pull) 대상 그룹 전부에 이미 있음`(실제 push, POST 0) | registry가 낡았다(pull 결과는 저장됨 · 승인 파일은 안 생김) — 같은 `--since`로 propose 다시 → 재승인 | 재승인 |
| exclusions `요청 결과 모름(<종류>)`(exit 1 — POST·GET 도중 끊김·응답을 못 읽음) | 재PUT·재등록 금지. `verify --key-file … --approved <그 승인 파일>`로 실제 상태를 읽어 보고(registry는 저장돼 있다). 첫 pull에서 났으면 `POST 전에 멈춤(POST 0 — 승인 파일 안 씀)` | 재시도 여부 |
| exclusions `[push] 완료: … — 요청 실패·결과 모름이 있었지만 다시 읽은 목록엔 전부 있음`(exit 1) | **재시도하지 않는다** — `verify --key-file … --approved <그 승인 파일>`로 확인해 보고(등록은 됨 — 11·12번에는 verified 수 그대로) | — |
| exclusions exit 1 | 성공/실패를 그룹×이름으로 나눠 보고 | 재시도·keep |
| 5단계 compute `[FAIL] 잔액 기록…`(못 읽음·꼴 다름·지난 회차 기록) · apply `[FAIL] apply: … "잔액" 없음` | 5단계 세 줄을 balance.py 부터 다시(작업본은 그대로 — apply 는 실패하면 쓰지 않는다). `work/balance.json` 을 손으로 고치지 않는다 | — |
| balance.py `[주의] 잔액 확인 못 함(<사유>)`(exit 0) | 멈추지 않는다 — 카드 "확인 못 함"으로 진행하고 끝 보고에 사유 한 줄(사용자 결정 2026-10-09 "조회 실패해도 배포는 멈추지 않는다"). 재시도는 사용자가 원할 때 balance.py 부터 | 키 파일·네트워크 확인 |
| precheck FAIL | 전체 출력 보고 → 원인 고쳐 재실행(배포 금지) | — |
| `leads.py add`·`skip` `[FAIL]`(입력 검사 — 숫자 아님·상한·모순 / 같은 주 / 장부 꼴 다름, 쓰기 0) | 그 줄과 사용자 답 원문을 나란히 보이고 되묻는다(같은 주면 "정정"인지). 꼴 다름이면 장부를 손으로 고치지 않고 보고 — 그 회차는 미입력으로 진행 | 숫자 다시·"정정"·"건너뜀" |
| `place.py set`·`done` `[FAIL]`(id·상태 밖 · 미래 날짜 · 첫 set 에 빠진 id · 같은 상태 · 꼴 다름, 쓰기 0) | 출력과 답을 나란히 보이고 되묻는다 | 번호·날짜 다시 |
| `leads.py guard` `[FAIL]`(staged 추가 줄·커밋 메시지에 장부 라벨+숫자·장부 머리줄·최근 매출 값, 커밋 0) | 커밋하지 않는다. 걸린 줄을 `(5) 장부 입력됨(로컬)` 같은 꼴로 고치고 다시 add → guard. 장부 숫자가 아닌 오탐(검색어 이름에 라벨 낱말이 들고 바로 뒤에 횟수가 붙은 것)이면 그 이름을 따옴표로 감싸 라벨과 숫자를 떼고 다시 guard — 장부 숫자를 다른 꼴로 바꿔 넣지 않는다 | — |
| compute `[주의] 장부 확인 못 함`·`[주의] 체크리스트 …`(exit 0) | 멈추지 않는다 — 12번 장부 행 `확인 못 함` / 플레이스 행 0 으로 진행하고 끝 보고에 한 줄(첫 입력 전이면 정상) | — |
| deploy `[FAIL] 배포본이 4단계 fetch 뒤 바뀜`(PUT 0) | 지금 배포본 sha·md5를 보고 — 다른 배포가 있었다 | 4단계부터 다시 할지 |
| deploy `[FAIL] precheck 통과본이 아님`(PUT 0) | precheck가 끝난 뒤 작업본이 바뀌었거나(6단계부터), 도장의 직전 배포본 ≠ `--base`(4단계를 다시 받았으면 5·6단계부터) | — |
| deploy `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함`(PUT 0 — 네트워크 전) | 레이아웃 판 첫 적용 회차면: 작업본·전후 비교 페이지를 보이고 사용자 "배포" 답을 기다린다(답이 있으면 같은 명령에 `--layout-change`). **데이터 회차에서 났으면**(병합 뒤 첫 적용 전에 데이터 회차가 먼저 돌아 5단계 `apply.py --layout` 이 모양을 바꾼 상태) PUT 0 으로 멈추고 사용자에게 묻는다 — `--layout-change` 를 스스로 붙이지 않는다 | 화면 확인 뒤 "배포"(→ `--layout-change`) 또는 보류 |
| deploy PUT 409(`배포본이 GET 뒤 바뀜`)·403(쓰기 권한 없음)·404(저장소·경로) | 출력 줄 그대로 보고, 자동 재시도 금지 | 4단계부터 다시 할지·권한 확인 |
| deploy `[FAIL] PUT 결과 모름`(요청 도중 끊김·5xx) | **재PUT 금지** — 먼저 `deploy.py verify --file work/index.html`(읽기)로 반영됐는지 보고(불일치면 캐시일 수 있다 — 아래 verify 불일치 행) | 재PUT 여부 |
| deploy `지금 배포본 = 작업본 — 앞 PUT이 이미 반영됨`(exit 0, PUT 0) | `deploy.py verify --file work/index.html`로 확인해 보고(결과 모름이던 앞 PUT이 반영된 것) | — |
| deploy 권한 거짓·권한 조회 실패 | 출력 줄 그대로 보고(값 없음) | 계정·권한 확인 |
| deploy verify 불일치 | 멈춤·**재PUT 금지**. ref 없이 돌렸으면(`[FAIL] 불일치 — PUT 직후라면 캐시일 수 있다`) `git ls-remote https://github.com/LeeKwanBeom/saero-pilates-report HEAD`(읽기)와 `verify --ref <push 성공 줄의 커밋 — 없으면 그 HEAD>`로 다시 verify — ref 없는 contents GET은 PUT 직후 약 1분 옛 본문을 준다(2026-09-29 실측 2회: HEAD = 새 커밋, `?ref=` 본문 = 로컬). `--ref`로도 불일치(`커밋 고정 조회라 캐시 아님`)면 출력의 재수령본 sha·md5를 보고 | 재PUT 여부 |

**사람만 하는 일**: 네이버 로그인·2단계 인증(`--login` 창) · 팝업·공지 닫기 · 라이브 시크릿 창 확인 · codegen 녹화 · 손 다운로드(8절).

## 5. exit 코드는 출력 줄로 가른다

| 명령 | 코드 | 출력으로 가르기 |
|---|---|---|
| `fetch_reports.py` | 1 | `목록 URL에 도달하지 못함`(로그인) / `허용 목록 밖 동작`·`금지 요소 클릭 시도 차단`(화면 변경) / `playwright가 없습니다`·설정(환경) |
| | 2 | `[FAIL] 4개 중 성공 …`(부분 실패, partial) / 첫 줄 `usage:`(인자 오류) |
| `exclusions.py` | 1 | `[FAIL] 승인 목록을 만들지 않았다`(그 위 `[FAIL]` 줄 — 합계 ≠ N · 범위 밖 · 원천 없음·빈 파일·읽을 수 없음 · `후보 파일이 propose 산출물이 아님·propose 뒤 바뀜`(work/ 밖 포함) · `같은 propose 실행이 아님` · `propose 뒤 합본·registry가 바뀜` · `이미 registered` · `registry에 keep` · 금지 패턴·경쟁사명 · K() 중복 · CSV 칸 줄바꿈 든 행) · `[FAIL] 고른 이름 중 …개가 방금 읽은(pull) 대상 그룹 전부에 이미 있음`(POST 0) · `요청 결과 모름(<종류>)`(첫 pull이면 `POST 전에 멈춤(POST 0 — 승인 파일 안 씀)`) · `[FAIL] --approved는 dry-run·시험 전용` · `[FAIL] 승인 목록 원천이 없음` · `[FAIL] --approved와 참조 선택 모드(…)를 함께 쓸 수 없음` · `[FAIL] 합본 CSV가 저장소 work/combined/검색어.csv가 아님`(전부 쓰기 전 — 쓰기 0) / `[push] 완료: … 실패/미확인 n`(부분 실패 — 끝이 `다시 읽은 목록엔 전부 있음 … 재시도 안 함`이면 등록은 됨, verify --approved로 확인) / `401`·ApiError(인증·API) / `[push] 등록할 이름이 없습니다`(전부 거부·후보 0) / `[FAIL] registry 없음` |
| | 2 | `[FAIL] 네트워크 차단(프록시)`(Code 탭에선 나지 않아야 함) / `usage:` |
| `ingest.sh` | 1 | `[FAIL] 현재 브랜치가 main이 아님` / `[FAIL] HEAD … ≠ origin/main — 시작 전`(쓰기 0) · `— push …`(push 뒤) / `[FAIL] data/가 HEAD와 다름`·`[FAIL] data/에 추적 안 된 파일이 있음`(쓰기 0) / `[FAIL] data/ CSV 줄바꿈이 커밋과 다름`(쓰기 0) / `[FAIL] push 실패`(커밋은 로컬에만) / `[FAIL] 파이썬을 실행할 수 없음` / archive `[FAIL] …` |
| | 128 | `fatal:`(git fetch 실패 — 네트워크·자격 증명, 또는 `== push data/` 뒤 커밋 실패 — `set -e`로 멈춤). `== push data/` 뒤에 났으면 `git fetch` 뒤 HEAD = origin/main **이고** `git status --short -- data`가 비어 있어야 보관본 완료 — `A`·`M`이 남았으면 커밋 실패(보관본 미완료) → 4절 되돌리기 뒤 ingest 다시 |
| | 그 밖 | 2 = 사용법(인자 없음) |
| `balance.py` | 0 | `[잔액] N원 · M/D(요일) HH:MM 기준(KST) · GET /billing/bizmoney 1회`(성공) / `[주의] 잔액 확인 못 함(<사유 — 키 파일 문제·네트워크 오류·네트워크 차단(프록시)·인증·권한 오류(401/403)·429 요청 한도·서버 오류(5xx)·응답 코드 N·요청 결과 모름·응답 꼴 다름·알 수 없는 오류>)`(실패 기록 — 카드 "확인 못 함") |
| | 1 | `[FAIL] 잔액 기록을 쓰지 못함` · `[FAIL] 옛 잔액 기록을 지우지 못함`(기록 없음 → compute `--balance` 가 FAIL) |
| | 2 | `usage:`(`--key-file` 없음) |
| `leads.py` | 0 | status·row·path(장부 없음·꼴 다름은 `[주의]` — 판정 '확인 못 함') / add·skip `[추가]`·`[정정]`·`[dry-run] … 파일 쓰기 0` / guard `[PASS] guard` |
| | 1 | add·skip `[FAIL]`(입력 검사 · 같은 주 · 정정할 주 없음·월요일 아님·다 찬 주 아님 · 장부 꼴 다름 · 장부 쓰기 — 쓰기 0) / guard `[FAIL] 공개 저장소에 장부 숫자 N곳`(커밋 0) / row `[FAIL] compute.json 에 "성과장부" 없음` |
| | 2 | `usage:` · `[FAIL] --week 는 --replace(정정)와 함께만` · `[FAIL] guard 는 --staged 로` · `[FAIL] git diff --cached 를 못 읽음` |
| `place.py` | 0 | status·row·path / set·done `[추가]`·`[dry-run] 파일 쓰기 0` |
| | 1 | set·done `[FAIL]`(쓰기 0 — 첫 set 빠진 id · id·상태 밖 · 미래·과거 날짜 · 같은 상태 · 꼴 다름 · 체크리스트가 아직 없음(done)) / status `[FAIL] 합본을 못 읽음` |
| | 2 | `usage:` · `[FAIL] 'P…' — P<n>=done\|todo\|no\|later[:YYYY-MM-DD]` · 날짜 꼴 |
| `precheck.sh` | 1 | md5 가드 `[FAIL] 직전 배포본이 작업본과 같다` / `[FAIL] 파이썬을 실행할 수 없음` / `[FAIL] 작업본이 precheck 도중 바뀜`(도장 없음) / validate·compare 실패(전체 출력). compute·overflow가 예외로 끝나면 `[FAIL]` 줄 없이 Traceback — **마지막 `==` 줄이 멈춘 단계** |
| | 2 | 사용법(인자 수) · `[FAIL] 파일 없음`(작업본·직전 배포본). 그 밖의 코드는 validate·compare가 낸 코드 그대로 |
| `deploy.py` | 1 | `GET …` / `[FAIL] precheck 통과본이 아님`(PUT 0 — 네트워크 전) / `[FAIL] 레이아웃 판이 바뀜 — PUT 안 함`(PUT 0 — 네트워크 전, 4절 ⓑ) / `[FAIL] PUT 결과 모름`(재PUT 금지 — verify 먼저) / `[FAIL] 배포본이 4단계 fetch 뒤 바뀜` / `[FAIL] 배포본이 GET 뒤 바뀜(sha 불일치)`(PUT 409) · `[FAIL] PUT 403`·`PUT 404`·`[FAIL] PUT <코드>` / `불일치`(verify — ref 없이면 `캐시일 수 있다`: ls-remote HEAD·`--ref`로 다시, `--ref`면 `커밋 고정 조회라 캐시 아님`) · `[FAIL] ref …의 index.html을 찾지 못함`(verify `--ref` 404) / `[FAIL] 자격 증명을 얻지 못함` / 권한 `거짓`·`권한 조회 실패` |
| | 2 | 인자(전부 GET 전) — `[FAIL] push에는 --file이 필요`·`verify에는 --file이 필요`·`fetch에는 --out이 필요` · `[FAIL] 실제 push에는 --base` · `--base 파일을 읽을 수 없음` · `[FAIL] --file을 읽을 수 없음` · `[FAIL] --base는 --file과 함께만` · `[FAIL] --ref는 verify에만`·`[FAIL] --ref는 커밋 sha(16진 7~40자 …)만` |
| | 0 | `지금 배포본 = 작업본 — 앞 PUT이 이미 반영됨`(PUT 0 — verify로 확인) |

## 6. 승인 목록 — push 참조 선택 모드(세션은 이름을 쓰지 않는다)

실제 등록(`exclusions.py push` — dry-run이 아닌 것)은 **참조 선택 모드만** 된다. push가 원천 파일에서 이름을 직접 읽어 목록을 만들고,
세션은 **줄·행 번호와 답의 N만** 넘긴다(이름을 타이핑하지도, 승인 파일을 쓰지도 않는다 — 2026-09-28 수정 회차 2).
```bash
"$PY" scripts/exclusions.py push --from-candidates work/exclusions_proposal_<창시작>_<창끝>_candidates.txt [--drop <줄번호,…>] \
  [--industry work/exclusions_proposal_<창시작>_<창끝>_industry.txt --industry-lines <줄번호,…>] \
  [--extra-csv work/combined/검색어.csv --extra-rows <행번호,…>] --expect <N> --dry-run      # 먼저 dry-run(HTTP 0) — 확인 뒤 --dry-run 대신 --key-file ~/naver-api.keys.json
```
- **승인 문구에 번호가 붙는다**: 목록 번호 = `_candidates.txt` 줄, 제안서 업종어 절 번호 = `_industry.txt` 줄. 답 예 — **"등록 승인 12개"(N은 숫자로 쓴다)** /
  "3 빼고"(→ `--drop 3`) / "업종어 2 넣기"(→ `--industry …_industry.txt --industry-lines 2`). 세션은 답의 번호를 그대로 옮긴다.
  `--expect` = 답의 N — N이 없는 번호 답("3 빼고"·"업종어 2 넣기")이면 세션이 목록 수에서 계산하고(− 뺀 수 + 넣은 수), 실제 push 전에 dry-run의 `[승인 목록] N개`와 이름을 사용자에게 보인다.
- **답이 모호하면 되묻는다**: N을 숫자로 쓰지 않았거나(`"등록 승인 N개"` 글자 그대로) "위 2가지만"처럼 둘 이상으로 읽히면, 세션은 글자에 가장 가까운 해석으로
  `push … --dry-run`만 돌려 `[승인 목록] N개`·이름을 보이고 다른 해석을 한 줄로 붙여 되묻는다 — 확인 답 전에는 실제 push 0
  (2026-09-29 실측: 답 "등록 승인 N개 / 업종어 1·3 / 위 2가지만 등록" → 2개 dry-run을 보이고 확인 → 사용자 "후보 10개 그대로 다 해줘 오타났다" → 12개 dry-run → 등록).
- 원천 셋: ① `_candidates.txt`(신규·재등록 후보 — 뺄 이름은 `--drop` 줄 번호) ② `_industry.txt`(업종어 포함 이름, 한 줄 하나 — 사용자가 고른 줄만
  `--industry-lines`) ③ 합본 `검색어.csv`의 `검색어` 칸(07번 표에서 고른 이름·재상정 — `--extra-rows`는 **파일 줄 번호**, 1행 기간 헤더·2행 컬럼 줄은 범위 밖.
  찾기: `grep -n '<이름 일부>' work/combined/검색어.csv`). 줄 번호는 `cat -n`·`grep -n`과 같은 1부터(push는 `\n`으로만 줄을 센다 — 칸 안 CR은 줄로 안 센다). 후보가 0줄이면 `--from-candidates`를 빼고
  `--industry`·`--extra-csv`만 쓴다(빈 원천 파일은 `[FAIL]`).
- push가 찍는 것: 고른 이름마다 **repr + 출처(파일:줄)**, `뺀 것:`(--drop 줄), `[승인 목록] N개 = --expect N`. **dry-run은 화면만**(파일 쓰기 0),
  실제 push만 — pull 재검사를 통과한 뒤 첫 POST 전에 — `work/approved_<날짜>_<시분초>.txt`(덮어쓰기 없음)를 쓴다. 세션은 이 출력을 그대로 사용자 답과 대조한다.
- **출처 검사**: `--from-candidates`는 `_candidates.txt`, `--industry`는 `_industry.txt`로 끝나고 저장소 `work/` 밑이어야 하며, 둘을 함께 주면 **같은 propose 실행**
  (같은 폴더·같은 `<창 이름>`)이어야 한다. propose가 같은 폴더에 쓴 `exclusions_proposal_<창시작>_<창끝>.md5`의 값과 지금 파일 md5가 같아야 하고,
  같은 기록의 `combined`(합본 검색어.csv)·`registry` md5도 지금 파일과 같아야 한다(propose 뒤 ingest·pull로 바뀌면 `propose 뒤 합본·registry가 바뀜`) — 손으로 쓴 파일·propose 뒤 바뀐 파일·두 파일을 바꿔 넣은 것은
  `[FAIL] 후보 파일이 propose 산출물이 아님·propose 뒤 바뀜(<옵션>)`. `--extra-csv`는 저장소 `work/combined/검색어.csv`(ingest가 만든 합본)만 받는다.
  다시 하려면 같은 `--since`로 propose를 다시 돌려 새 파일로 고른다(`--expect`는 재승인 N). `.md5`·도장은 우발 사고(손으로 쓴 파일·propose 뒤
  바뀐 파일) 가드다 — 보안 경계가 아니므로 **세션은 `*.md5`·`precheck_ok.md5`를 손으로 쓰거나 고치지 않는다**(다시 만들려면 propose·precheck.sh를 다시 돌린다).
- **쓰기 전 `[FAIL]`(dry-run도 같다 — 승인 파일·HTTP·registry 쓰기 0)**: 합계 ≠ `--expect N` · 원천 파일 없음·빈 파일·읽을 수 없음(UTF-8 아님) ·
  줄·행 번호 범위 밖(10진 숫자만) · 출처 검사 · `K()` 중복(같은 이름을 두 번 — 대소문자·앞뒤 공백만 다른 것 포함) · 합본 CSV 칸 안에 줄바꿈이 든 행을 고름
  (그 행만 — 칸 안 CR만 든 행 포함, 다른 행은 줄 번호 그대로 고를 수 있다. 따옴표 없는 칸의 CR은 파일 전체 `[FAIL]`) ·
  **고른 이름 중 하나라도 이미 registered**(후보·업종어·추가 전부 — 모든 대상 그룹 또는 propose와 같은 기준: `*` 기록·pending 포함 — 9/28 유형 신호) ·
  **registry keep**(사용자 결정 "노출 유지"를 덮지 않는다) ·
  **금지 패턴·경쟁사명**(참조 모드는 `[거부]`가 아니라 `[FAIL]` — propose가 후보로 내지 않는 이름이라 잘못 고른 신호).
- **실제 push의 pull 뒤 재검사**: 쓰기 전 읽기(pull) 결과 고른 이름 중 대상 그룹 전부에 이미 있는 이름이 있으면 POST 0으로 `[FAIL]`(registry가 낡아
  dry-run이 못 본 9/28 유형 — pull 결과는 registry에 저장, 승인 파일은 안 씀). 요청 도중 끊기거나 응답을 못 읽으면 `요청 결과 모름` — 그 묶음은 failed, verify가 실제 상태를 다시 읽고 registry는 저장된다.
- **`[주의]` 쌍둥이**: 고른 이름과 기호·공백·대소문자만 다른 이름이 후보·업종어 파일·합본 칸·registry에 있으면 둘을 나란히 찍는다
  (예: 고른 것 `'노원힐링장소.' ← 검색어.csv:1165` / 쌍둥이 `'노원힐링장소' ← 검색어.csv:1164·registry …행(registered 3)`). 멈추지는 않는다 —
  사용자 답의 원문과 같은 쪽을 골랐는지 세션이 확인해 보인다.
- push의 `--approved <파일>`은 dry-run·시험 전용이다(verify의 `--approved`는 재개 판정용) — 실제 push에 쓰면 `[FAIL] --approved는 dry-run·시험 전용` exit 1(쓰기 0).
- 사례(2026-09-28): 승인 6개 중 **"노원힐링장소."** — 채팅이 넘긴 목록엔 마침표가 있었는데 Code 탭에서 승인 파일을 다시 쓰며 빠졌다
  (등록 전 registry 사본으로 dry-run 재현: 마침표 없음 216 → 221, 있음 216 → 222 = 채팅 기록 값). 마침표 없는 이름은 registry에 이미
  3그룹 registered라 "건너뜀"으로 조용히 통과했고 원문은 미등록으로 남았다. 지금은 그 행(1164)을 고르면 "이미 registered" `[FAIL]`(실제 push에서 registry가 낡았어도 pull 뒤 재검사가 POST 0으로 멈춘다),
  맞는 행(1165)을 고르면 통과하면서 1164를 쌍둥이 `[주의]`로 보인다. 기호(`;`·`+`·`]`·`.`)도 API는 원문대로 등록한다(9/27 실측) — 원문을 바꿀 이유가 없다.

## 7. 금지

- `partial/`·검사 실패·summary 없는 폴더를 store에 넘기기 / `store --force`·`--chunk` 자동 부착
- 승인 이름을 세션이 다시 타이핑하거나 기호·마침표를 지우기 · 승인 파일을 손으로 써서 넘기기(실제 등록은 6절 참조 선택 모드만) / "등록 승인 N개" 전 `push`·`delete`·`test-roundtrip`
- `work/exclusions_proposal_*.md5`·`work/precheck_ok.md5`·`work/balance.json`을 손으로 쓰기·복사하기·고치기(propose·precheck.sh·balance.py만 쓴다) / 합본 밖 CSV를 `--extra-csv`로
- `deploy.py push`를 `--base work/prev.html` 없이 실제로 돌리기(코드가 exit 2로 막는다) · `[FAIL] 배포본이 4단계 fetch 뒤 바뀜` 뒤 `--base`만 새 배포본으로 바꿔 끼우기(4단계부터 다시 할지는 사용자가 정한다)
- 실제 이름·여러 건으로 시험 / 외부 쓰기(push·POST·PUT) 자동 재시도·자동 재PUT
- 헤드리스 실행 · 같은 프로필 동시 실행(백그라운드 fetch 중 fetch 재호출 포함) · 크래시 수정이 없는 판(Desktop 사본 `68028c8`)으로 실행
- 로그인 폼 입력 · 로그인 실패 산출물(`not_logged_in.*` png·aria·inventory) 열기
- 토큰·키 파일 열기·출력 · 토큰을 채팅에 요구 · **세션이 `git credential fill`을 직접 치기**(deploy.py만 쓴다)
- 세션이 registry(`audit/exclusions.csv`)를 손으로 고치기 / `git add -A`(`work/`·키·`.claude/`) — 경로를 지정해 add
- 이 PC에서 부트스트랩 1절 실행·컨테이너 작업 경로 생성 / `python3` 호출
- 답을 반영한 재배포에 `--pending` / precheck 3번째 인자에 작업본
- 01:00 KST 전 실행 / main 아닌 브랜치에서 `ingest.sh`
- 권한 허용 목록·env·settings 같은 사용자 설정 바꾸기
- (매출 작업 A·C) 장부(`~/saero-leads/leads.csv`)·체크리스트(`audit/place-checklist.csv`)를 손으로 쓰기·고치기·지우기(leads.py·place.py 만 — 줄 추가만) / `leads.py add` 에 `--week`(정정 `--replace` 밖) /
  (5) 답 원문·장부 숫자·캡처에서 읽은 숫자를 last-audit·커밋 메시지·리포트(01·11·12 포함 어디든)에 옮기기 — 숫자는 채팅·로컬 장부에만(config `leads.publish` = verdict) /
  `leads.py guard --staged` 없이 스킬 저장소 커밋(8단계·5-0c·config 커밋·마감 wrapup) / 운영 회차에 `SAERO_LEADS`·`SAERO_PLACE`·`--ledger`·`--checklist` 로 경로 바꾸기(시험·리허설 전용)

## 8. 수동 폴백과 작업 폴더 줄바꿈

**손 다운로드 4개**(fetch가 막혔을 때, 또는 월초를 놓쳐 `지난달` 끝이 비었을 때): 사용자가 광고주센터 다차원 보고서 목록에서 4개
(시간대별·상세지역·검색어·필라테스)를 열어 다운로드한다 — 평일은 저장된 `이번달`, 지난달을 채울 땐 `지난달` 프리셋.
파일은 `~/saero-fetch/downloads/manual-<YYYY-MM-DD>/`(data/ 밖)에 둔다. 세션은 4개 첫 줄 헤더(기간·계정 2580077)와
2행 컬럼을 확인한 뒤 `scripts/ingest.sh "<그 폴더>"/*.csv`. 이름은 `<보고서명>_보고서_2580077.csv`여도 된다(종류는 컬럼으로 판별).

**작업 폴더 줄바꿈**: 이 PC는 `core.autocrlf=true`라 `.gitattributes`가 들어오기 전에 풀린 CSV가 CRLF로 남아 있다.
그 상태에서 `git add --renormalize`나 `git add data`를 하면 **CRLF 바이트가 커밋된다 — 하지 않는다.** S0가 줄바꿈 FAIL을 내면
사용자와 함께 한 번: 작업 폴더에서 `git status`가 CSV 말고는 깨끗한지 보고 → S0가 이름을 댄 CSV 파일을 지운 뒤 `git checkout HEAD -- data`
(커밋 바이트로 다시 풀림) → `git ls-files --eol`로 i/·w/가 같은지 확인. 또는 작업 폴더를 `git clone -c core.autocrlf=false`로 새로 받아
바꿔 끼운다(`work/`의 파일은 옮겨 둔다).

## 9. 리허설 — 외부 쓰기 0으로 전 순서 확인

스크래치에 `git clone -c core.autocrlf=false`로 받은 저장소(또는 기능 브랜치)에서, origin을 **로컬 bare 저장소**로 바꿔 돌린다.
입력은 `data/YYYY-MM` 4개를 data 밖 폴더에 복사한 것(같은 경로를 store에 넘기면 archive.py가 원본을 지운 뒤 복사하다 잃는다).
순서: S0(스킬 저장소 push dry-run은 bare로) → `fetch_reports.py --dry-run`(오늘 · `--today 2026-10-01`, 수집·프로필 폴더는 스크래치) →
`ingest.sh`(bare로 push) → `deploy.py fetch`(무인증) → compute → 2-1 → `propose --since` → 6절 참조 선택 `push --dry-run`(틀린 행 FAIL · 맞는 행 통과 ·
쌍둥이 `[주의]`) → precheck(작업본 = 배포본 사본 + 주석 1줄 — md5 가드 통과용) → `deploy.py push --file work/index.html --base work/prev.html --dry-run`(precheck 도장 확인 포함) →
`verify`(같은 파일 일치 · 바꾼 사본 불일치 exit 1). 배포 저장소 권한 확인(인증 GET)은 이 PC 실제 자격 증명을 쓰므로 사용자에게 묻고 한다 —
S0를 그 전에 돌릴 때는 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=<도우미 없는 임시 설정>`으로 자격 증명 없이(배포 줄 FAIL이 정상).
판정: 작업 폴더·실제 원격의 data·config·registry md5, `git status`, 두 저장소 `git ls-remote` HEAD가 전후 같다. fetch 폴더 미생성.
