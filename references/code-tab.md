# Code 탭 실행 규약 — 수집부터 배포·등록·기록까지 한 세션 (정본)

데스크톱 앱 Code 탭(Claude Code, 이 PC 로컬 셸) 세션 하나가 ① 보고서 수집(`fetch_reports.py`) → ② 보관·합본·갱신·배포(SKILL.md 1~8단계)
→ ③ 제외 검색어 등록(5-0단계)을 **같은 작업 폴더에서** 잇는 방법이다. SKILL.md는 무엇을 하는지, 이 문서는 이 PC에서 어떻게 치는지를 적는다 —
둘이 어긋나면 둘 다 고친다. 근거: `audit/last-audit.md` "기능 추가 탐색 기준선(Code 탭 전 단계 실행, 2026-09-28)" 0~7절.
채팅(웹·Cowork)은 쓰지 않는다 — 네이버 API가 403이고(exclusion-ui.md 3절), SKILL.md 맨 위 채팅 가드가 멈춘다.

## 0. 진입

- Code 탭은 **`D:\saero` 폴더로 연다**(저장소 폴더로 열지 않는다 — 메모리 D--saero·wrapup이 안 붙는다). 첫 말은 **`/saero-run`**.
  진입 스킬 `D:\saero\.claude\skills\saero-run\SKILL.md`와 `D:\saero\CLAUDE.md`의 정본 사본은 저장소 `local/`에 있다(설치·갱신은 사용자가, 마감 때 md5 대조).
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
| 회차 작업물 | 저장소 `work/`(gitignore): `work/combined/` · `work/prev.html` · `work/index.html` · `work/compute.json` · `work/exclusions_proposal_<창시작>_<창끝>.md`·`_candidates.txt`·`_industry.txt`(propose — 창이 다르면 다른 파일) · `work/approved_<날짜>_<시분초>.txt`(push 참조 선택 모드 — 실제 push만, 덮어쓰기 없음) · `work/exclusions_proposal_<창시작>_<창끝>.md5`(propose 출처 기록) · `work/precheck_ok.md5`(precheck 통과 도장) · `work/exclusions_pull_<날짜>.json` |
| 줄바꿈 | `.gitattributes`: `*.csv -text`(바이트 그대로) · `*.sh text eol=lf`. 작업 폴더가 커밋과 다르게 풀려 있으면 8절 "작업 폴더 줄바꿈" |

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
| 5-0a | 후보 | (권장) `"$PY" scripts/exclusions.py pull --key-file ~/naver-api.keys.json`(읽기 — registry `verified_at`이 바뀐다, 커밋은 5-0c, 5-0c가 없는 회차는 8단계에서 함께) → `"$PY" scripts/exclusions.py propose work/combined --since YYYY-MM-DD` — propose `--since` = 직전 배포 masthead 끝 + 1일(ISO). 직전 회차 기록이 "등록 미룸"이면 그 회차 propose 창 시작(lo) — 미룬 이름과 새 이름을 한 묶음으로 올린다(first_seen 필터 때문에 끝 + 1일로는 미룬 이름이 다시 안 오른다). 기본 창은 마지막 하루뿐이라 쓰지 않는다. 산출물은 `work/exclusions_proposal_<창시작>_<창끝>.md`·`_candidates.txt`·`_industry.txt`·`.md5`(출처 기록 — push가 대조), 빈 창이면 `[주의] 빈 창` | ⓑ registry 없음 |
| ⓐ | **승인 묶음 한 번** | (1) 새 경쟁사 · (2) 애매 후보 · (3) 제외 그룹 · (4) 제외 검색어(propose 승인 문구 원문) 중 **해당하는 것만** 한 메시지. (1)~(4)가 모두 0일 때만 묻지 않는다 | 답을 기다린다 |
| 5-0b | 답 반영 | config(`competitors`·`excluded_groups`)가 바뀌면 → config 커밋(push는 5-0c와 함께) → compute 재실행(경쟁사가 바뀌면 propose도) | — |
| 5-0c | 등록·확인·기록 | 참조 선택 모드(6절) `exclusions.py push --from-candidates … [--drop …] [--industry … --industry-lines …] [--extra-csv work/combined/검색어.csv --extra-rows …] --expect N --dry-run`(호출 0 · 파일 쓰기 0 · `[FAIL]` 0 · "승인 N개" = 답의 N · `[주의]` 쌍둥이는 사용자에게 보인다) → 같은 명령에서 `--dry-run` 대신 `--key-file ~/naver-api.keys.json`(pull → POST → verify, 승인 목록은 실제 push가 `work/approved_<날짜>_<시분초>.txt`에 쓴다) → `exclusions.py report` → registry(+config) 커밋 → `git fetch` → `git push origin main` → HEAD == origin/main | ⓑ `[FAIL] 승인 목록…`(쓰기 0) · exit 1(부분 실패·verified:false) → 재시도는 ⓐ |
| 5 | 교체 | compute.json 값으로 01~12(12번 먼저, 11번 마지막). 07 각주·11·12번에 **등록 n · verified n · 실패 n**을 사실 그대로 | — |
| 6 | 검증 | `scripts/precheck.sh work/index.html work/combined work/prev.html` — 전부 통과하면 `work/precheck_ok.md5`(작업본 md5 도장) | ⓑ 세션이 고치고 재실행 |
| 7 | 배포 | `"$PY" scripts/deploy.py push --file work/index.html --base work/prev.html --message "리포트 갱신: <기간>" --dry-run`(precheck 도장 · base 대조 · 자격 증명 · 쓰기 권한 참) → 같은 명령(dry-run 없이 — `--base` 필수, 도장 = 작업본 md5일 때만 PUT) → `"$PY" scripts/deploy.py verify --file work/index.html` | ⓑ `[FAIL] precheck 통과본이 아님`·`[FAIL] 배포본이 4단계 fetch 뒤 바뀜`(PUT 0)·권한 거짓·PUT 409·403·404·verify 불일치(재PUT은 사용자) |
| 8 | 기록 | last-audit 갱신 회차 절(Edit — SKILL.md 8단계 양식, **propose 창 lo~hi · 등록 미룸(사용자) 여부** 포함) → 1절 신원으로 커밋(pull로 바뀐 registry가 아직 커밋 안 됐으면 함께 — 경로 지정 add) → `git fetch` → `git push origin main` → 스크래치 `git clone -c core.autocrlf=false`로 행수·md5 → 사용자 시크릿 창 확인 요청 | ⓑ push 실패 |

**재개·완료 판정은 대상의 현재 상태로 한다**(세션이 끊겼다 다시 시작할 때): 보관본 = `git fetch` 뒤 HEAD = origin/main(`ingest.sh`가 확인)이고 `git status --short -- data`가 빔 ·
등록 = `exclusions.py verify --key-file …`(registry note·기억으로 "등록 끝"이라 판정하지 않는다 — note는 verify 뒤에도 "확인 전"이 남는다) ·
배포 = `deploy.py verify --file work/index.html`. state 파일·대화 기억은 근거가 아니다.

**2-1 같음**: 2-1 기간이 같으면 승인 묶음 ⓐ와 별개의 앞 질문 하나만 하고 답을 기다린다 — 답 "다시 계산" → 3 → 5-0a → ⓐ(해당만) → 5-0b(해당 시) → 5-0c → 5 → 6 → 7 → 8 /
"CSV 다시" → ① / "미룬 등록만"(직전 회차 기록이 "등록 미룸"일 때만) → 3 건너뜀 → 5-0a(`--since` = 미룬 회차 창 시작) → ⓐ → 5-0c → 5(07·11·12 문구만) →
6(`--pending` 없이, 3번째 인자 = 이번 4단계 fetch) → 7 → 8.
(2-1 질문은 ⓐ 묶음에 넣지 않는다 — "다시 계산"·"미룬 등록만"이면 그 뒤에 ⓐ 묶음을 해당하는 것만 한 번 묻는다.)

**예외 "등록은 나중에"**(사용자가 그렇게 말할 때만): 07·11·12번에 "제안함 — 등록은 사용자 결정으로 다음에"처럼 사실형 문구로 배포하고
`--pending`은 쓰지 않는다. 8단계 기록에 `propose 창 lo~hi · 등록 미룸(사용자): 예`를 남긴다. 미룬 이름은 **다음 회차**(새 데이터)의 propose를
`--since lo`(미룬 회차 창 시작)로 돌려 새 이름과 한 묶음으로 올리고, 같은 데이터로 미룬 등록만 하려면 위 2-1 답 "미룬 등록만"으로 간다
(4단계는 이미 그 회차 배포본을 새로 받았고, precheck 3번째 인자는 그 파일 — `--pending` 없이 통과한 뒤 재배포).

## 4. 멈춤 표

**ⓐ 사람 승인(남긴다)**: SKILL.md "승인이 필요한 지점" (1)~(4) · 2-1 같음 질문(ⓐ 묶음과 별개의 앞 질문 — 답 셋: 다시 계산 / CSV 다시 / 미룬 등록만) · 3단계 새 제외 그룹 ·
등록 실패 재시도·keep·한도 초과 재승인 · delete/test-roundtrip `--confirm`(사용자 입회) · 12번 N주 미반영 질문.

**ⓑ 자동 검사 FAIL(멈추고 → 다음 행동)**

| FAIL | 다음 행동(세션) | 사람 |
|---|---|---|
| S0 줄 | 원인 한 줄 보고, 다음 단계 안 감 | 설치·창 닫기·자격 증명 로그인 |
| fetch exit 2 부분 실패 | `partial/<날짜>/summary.json`을 **재실행 전에** 읽고(재실행이 partial을 지운다) 보고서별 원인 보고 | 다시 받을지 |
| fetch exit 1 금지 차단·허용 밖 | summary.json은 없다(`--debug`여도 — SystemExit가 summary 작성 전에 끝남). 메시지의 동작·요소 문구를 보고 · 재실행 전에 `partial/<날짜>/`를 읽는다(재실행이 지운다) · `--debug` 없이 `debug/`가 있으면 앞 보고서 실패 컷(차단 화면 아님, 차단 순간 컷은 없다) → 원인 불명으로 보고 | `--debug` 재실행 여부 |
| fetch exit 1 로그인 | `--login` 백그라운드 → 끝나면 본 실행 | 창에서 로그인·2단계 인증 |
| store 거부·combine FAIL | 메시지 원문 보고. `--force`·`--chunk` 자동 금지. 월초를 놓쳐 지난달 끝이 비면 평일 fetch로는 못 채운다 → 8절 폴백 | 다시 받기·폴백 |
| store 부분 적용 | `git status data/`로 바뀐 파일 보고(커밋 안 함) — 새 달 폴더의 추적 안 된 파일(`??`)은 되돌리기가 지우지 않는다(`git clean -n -- data`로 목록만) | 되돌리기(`git restore --source=HEAD --staged --worktree -- data` — M·A·D 전부 HEAD로, 스테이징된 새 파일은 작업 폴더에서도 지운다. 입력은 data/ 밖이라 잃지 않는다)·`??` 파일 지우기 |
| ingest `[FAIL] HEAD ≠ origin/main`·브랜치(시작 검사면 쓰기 0) | 상태(`git status -sb`) 보고 | push·pull 결정 |
| ingest `[FAIL] data/가 HEAD와 다름`(시작 검사, 쓰기 0) | 함께 찍힌 `git status --short data` 보고 — 누가 바꿨는지(ingest 커밋 실패로 `A`가 남은 것일 수도) | 되돌리기(`git restore --source=HEAD --staged --worktree -- data`) |
| ingest `[FAIL] data/에 추적 안 된 파일이 있음`(시작 검사, 쓰기 0) | 찍힌 파일 목록 보고(store 부분 적용·손으로 둔 파일) | 지울지(`git clean -n -- data`로 확인 뒤) |
| ingest `[FAIL] data/ CSV 줄바꿈이 커밋과 다름`(시작 검사, 쓰기 0) | 이름 댄 CSV 보고 → 8절 "작업 폴더 줄바꿈" | 정리 승인 |
| push 403·거부(ingest `[FAIL] push 실패`) | 어느 저장소인지·커밋이 로컬에만 있는지 적어 보고 | 자격 증명 확인·재시도 |
| registry 없음 | `git status`·경로 점검 | — |
| exclusions `[FAIL] 승인 목록…`(쓰기 0) | 출력의 출처 목록·`[FAIL]`·`[주의]` 쌍둥이를 그대로 보이고 줄·행 번호를 사용자 답과 다시 맞춘다(이름을 쓰지 않는다). `후보 파일이 propose 산출물이 아님·propose 뒤 바뀜`이면 **재시도 = 같은 `--since`로 propose 다시 → 새 `_candidates.txt` → `--from-candidates … --expect <재승인 N>`** | 답 확인·재승인 |
| exclusions exit 1 | 성공/실패를 그룹×이름으로 나눠 보고 | 재시도·keep |
| precheck FAIL | 전체 출력 보고 → 원인 고쳐 재실행(배포 금지) | — |
| deploy `[FAIL] 배포본이 4단계 fetch 뒤 바뀜`(PUT 0) | 지금 배포본 sha·md5를 보고 — 다른 배포가 있었다 | 4단계부터 다시 할지 |
| deploy `[FAIL] precheck 통과본이 아님`(PUT 0) | precheck가 끝난 뒤 작업본이 바뀌었다 — 6단계부터 다시 | — |
| deploy PUT 409(`배포본이 GET 뒤 바뀜`)·403(쓰기 권한 없음)·404(저장소·경로) | 출력 줄 그대로 보고, 자동 재시도 금지 | 4단계부터 다시 할지·권한 확인 |
| deploy 권한 거짓·권한 조회 실패 | 출력 줄 그대로 보고(값 없음) | 계정·권한 확인 |
| deploy verify 불일치 | 멈춤. 출력의 재수령본 sha·md5를 보고(verify를 한 번 더 — 읽기만 — 해 같은지 덧붙인다) | 재PUT 여부 |

**사람만 하는 일**: 네이버 로그인·2단계 인증(`--login` 창) · 팝업·공지 닫기 · 라이브 시크릿 창 확인 · codegen 녹화 · 손 다운로드(8절).

## 5. exit 코드는 출력 줄로 가른다

| 명령 | 코드 | 출력으로 가르기 |
|---|---|---|
| `fetch_reports.py` | 1 | `목록 URL에 도달하지 못함`(로그인) / `허용 목록 밖 동작`·`금지 요소 클릭 시도 차단`(화면 변경) / `playwright가 없습니다`·설정(환경) |
| | 2 | `[FAIL] 4개 중 성공 …`(부분 실패, partial) / 첫 줄 `usage:`(인자 오류) |
| `exclusions.py` | 1 | `[FAIL] 승인 목록을 만들지 않았다`(그 위 `[FAIL]` 줄 — 합계 ≠ N · 범위 밖 · 원천 없음·빈 파일·읽을 수 없음 · `후보 파일이 propose 산출물이 아님·propose 뒤 바뀜` · `이미 registered` · 금지 패턴·경쟁사명 · K() 중복 · CSV 칸 줄바꿈) · `[FAIL] --approved는 dry-run·시험 전용` · `[FAIL] 승인 목록 원천이 없음` · `[FAIL] --approved와 참조 선택 모드(…)를 함께 쓸 수 없음` · `[FAIL] 합본 CSV가 저장소 work/combined/검색어.csv가 아님`(전부 쓰기 전 — 쓰기 0) / `[push] 완료: … 실패/미확인 n`(부분 실패) / `401`·ApiError(인증·API) / `[push] 등록할 이름이 없습니다`(전부 거부·후보 0) / `[FAIL] registry 없음` |
| | 2 | `[FAIL] 네트워크 차단(프록시)`(Code 탭에선 나지 않아야 함) / `usage:` |
| `ingest.sh` | 1 | `[FAIL] 현재 브랜치가 main이 아님` / `[FAIL] HEAD … ≠ origin/main — 시작 전`(쓰기 0) · `— push …`(push 뒤) / `[FAIL] data/가 HEAD와 다름`·`[FAIL] data/에 추적 안 된 파일이 있음`(쓰기 0) / `[FAIL] data/ CSV 줄바꿈이 커밋과 다름`(쓰기 0) / `[FAIL] push 실패`(커밋은 로컬에만) / `[FAIL] 파이썬을 실행할 수 없음` / archive `[FAIL] …` |
| | 128 | `fatal:`(git fetch 실패 — 네트워크·자격 증명, 또는 `== push data/` 뒤 커밋 실패 — `set -e`로 멈춤). `== push data/` 뒤에 났으면 `git fetch` 뒤 HEAD = origin/main **이고** `git status --short -- data`가 비어 있어야 보관본 완료 — `A`·`M`이 남았으면 커밋 실패(보관본 미완료) → 4절 되돌리기 뒤 ingest 다시 |
| | 그 밖 | 2 = 사용법(인자 없음) |
| `precheck.sh` | 1 | md5 가드 `[FAIL] 직전 배포본이 작업본과 같다` / `[FAIL] 파이썬을 실행할 수 없음` / validate·compare 실패(전체 출력). compute·overflow가 예외로 끝나면 `[FAIL]` 줄 없이 Traceback — **마지막 `==` 줄이 멈춘 단계** |
| | 2 | 사용법(인자 수). 그 밖의 코드는 validate·compare가 낸 코드 그대로 |
| `deploy.py` | 1 | `GET …` / `[FAIL] precheck 통과본이 아님`(PUT 0 — 네트워크 전) / `[FAIL] 배포본이 4단계 fetch 뒤 바뀜` / `[FAIL] 배포본이 GET 뒤 바뀜(sha 불일치)`(PUT 409) · `[FAIL] PUT 403`·`PUT 404`·`[FAIL] PUT <코드>` / `불일치`(verify) / `[FAIL] 자격 증명을 얻지 못함` / 권한 `거짓`·`권한 조회 실패` |
| | 2 | 인자 — `--file 이 필요` · `[FAIL] 실제 push에는 --base` · `--base 파일을 읽을 수 없음` · `[FAIL] --base는 --file과 함께만` |

## 6. 승인 목록 — push 참조 선택 모드(세션은 이름을 쓰지 않는다)

실제 등록(`exclusions.py push` — dry-run이 아닌 것)은 **참조 선택 모드만** 된다. push가 원천 파일에서 이름을 직접 읽어 목록을 만들고,
세션은 **줄·행 번호와 답의 N만** 넘긴다(이름을 타이핑하지도, 승인 파일을 쓰지도 않는다 — 2026-09-28 수정 회차 2).
```bash
"$PY" scripts/exclusions.py push --from-candidates work/exclusions_proposal_<창시작>_<창끝>_candidates.txt [--drop <줄번호,…>] \
  [--industry work/exclusions_proposal_<창시작>_<창끝>_industry.txt --industry-lines <줄번호,…>] \
  [--extra-csv work/combined/검색어.csv --extra-rows <행번호,…>] --expect <N> --dry-run      # 먼저 dry-run(HTTP 0) — 확인 뒤 --dry-run 대신 --key-file ~/naver-api.keys.json
```
- 원천 셋: ① `_candidates.txt`(신규·재등록 후보 — 뺄 이름은 `--drop` 줄 번호) ② `_industry.txt`(업종어 포함 이름, 한 줄 하나 — 사용자가 고른 줄만
  `--industry-lines`) ③ 합본 `검색어.csv`의 `검색어` 칸(07번 표에서 고른 이름·재상정 — `--extra-rows`는 **파일 줄 번호**, 1행 기간 헤더·2행 컬럼 줄은 범위 밖.
  찾기: `grep -n '<이름 일부>' work/combined/검색어.csv`). 줄 번호는 `cat -n`·`grep -n`과 같은 1부터. 후보가 0줄이면 `--from-candidates`를 빼고
  `--industry`·`--extra-csv`만 쓴다(빈 원천 파일은 `[FAIL]`).
- push가 찍는 것: 고른 이름마다 **repr + 출처(파일:줄)**, `뺀 것:`(--drop 줄), `[승인 목록] N개 = --expect N`. **dry-run은 화면만**(파일 쓰기 0),
  실제 push만 `work/approved_<날짜>_<시분초>.txt`(덮어쓰기 없음)를 쓴다. 세션은 이 출력을 그대로 사용자 답과 대조한다.
- **출처 검사**: `--from-candidates`는 `_candidates.txt`, `--industry`는 `_industry.txt`로 끝나야 하고, propose가 같은 폴더에 쓴
  `exclusions_proposal_<창시작>_<창끝>.md5`의 값과 지금 파일 md5가 같아야 한다 — 손으로 쓴 파일·propose 뒤 바뀐 파일·두 파일을 바꿔 넣은 것은
  `[FAIL] 후보 파일이 propose 산출물이 아님·propose 뒤 바뀜(<옵션>)`. `--extra-csv`는 저장소 `work/combined/검색어.csv`(ingest가 만든 합본)만 받는다.
  다시 하려면 같은 `--since`로 propose를 다시 돌려 새 파일로 고른다(`--expect`는 재승인 N). `.md5`·도장은 우발 사고(손으로 쓴 파일·propose 뒤
  바뀐 파일) 가드다 — 보안 경계가 아니므로 **세션은 `*.md5`·`precheck_ok.md5`를 손으로 쓰거나 고치지 않는다**(다시 만들려면 propose·precheck.sh를 다시 돌린다).
- **쓰기 전 `[FAIL]`(dry-run도 같다 — 승인 파일·HTTP·registry 쓰기 0)**: 합계 ≠ `--expect N` · 원천 파일 없음·빈 파일·읽을 수 없음(UTF-8 아님) ·
  줄·행 번호 범위 밖(10진 숫자만) · 출처 검사 · `K()` 중복(같은 이름을 두 번 — 대소문자·앞뒤 공백만 다른 것 포함) · 합본 CSV 칸 안 줄바꿈 ·
  **고른 이름(후보·업종어·추가 전부)이 이미 registered**(모든 대상 그룹 — 또는 propose와 같은 기준: `*` 기록·pending 포함 — 9/28 유형 신호) ·
  **금지 패턴·경쟁사명**(참조 모드는 `[거부]`가 아니라 `[FAIL]` — propose가 후보로 내지 않는 이름이라 잘못 고른 신호).
- **`[주의]` 쌍둥이**: 고른 이름과 기호·공백·대소문자만 다른 이름이 후보 파일·합본 칸·registry에 있으면 둘을 나란히 찍는다
  (예: 고른 것 `'노원힐링장소.' ← 검색어.csv:1165` / 쌍둥이 `'노원힐링장소' ← 검색어.csv:1164·registry …행(registered 3)`). 멈추지는 않는다 —
  사용자 답의 원문과 같은 쪽을 골랐는지 세션이 확인해 보인다.
- `--approved <파일>`은 dry-run·시험 전용이다 — 실제 push에 쓰면 `[FAIL] --approved는 dry-run·시험 전용` exit 1(쓰기 0).
- 사례(2026-09-28): 승인 6개 중 **"노원힐링장소."** — 채팅이 넘긴 목록엔 마침표가 있었는데 Code 탭에서 승인 파일을 다시 쓰며 빠졌다
  (등록 전 registry 사본으로 dry-run 재현: 마침표 없음 216 → 221, 있음 216 → 222 = 채팅 기록 값). 마침표 없는 이름은 registry에 이미
  3그룹 registered라 "건너뜀"으로 조용히 통과했고 원문은 미등록으로 남았다. 지금은 그 행(1164)을 고르면 "이미 registered" `[FAIL]`,
  맞는 행(1165)을 고르면 통과하면서 1164를 쌍둥이 `[주의]`로 보인다. 기호(`;`·`+`·`]`·`.`)도 API는 원문대로 등록한다(9/27 실측) — 원문을 바꿀 이유가 없다.

## 7. 금지

- `partial/`·검사 실패·summary 없는 폴더를 store에 넘기기 / `store --force`·`--chunk` 자동 부착
- 승인 이름을 세션이 다시 타이핑하거나 기호·마침표를 지우기 · 승인 파일을 손으로 써서 넘기기(실제 등록은 6절 참조 선택 모드만) / "등록 승인 N개" 전 `push`·`delete`·`test-roundtrip`
- `work/exclusions_proposal_*.md5`·`work/precheck_ok.md5`를 손으로 쓰기·복사하기·고치기(propose·precheck.sh만 쓴다) / 합본 밖 CSV를 `--extra-csv`로
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
