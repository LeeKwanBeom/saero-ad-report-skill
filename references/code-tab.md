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
| 셸 상태 | Bash 도구는 호출 사이에 env가 이어지지 않는다 → **매 호출 첫머리** `export PY=/d/saero/.venv/Scripts/python.exe PYTHONUTF8=1 GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never; unset GIT_ASKPASS SSH_ASKPASS` (자격 증명 창·프롬프트로 멈추지 않게 — push·fetch는 `git -c credential.interactive=false …`) |
| 인코딩 | 도구 파이프는 cp949 — 스크립트는 stdout·stderr를 utf-8로 바꾸지만 인라인 파이썬·heredoc까지 덮으려고 `PYTHONUTF8=1` |
| 시각 | KST = `TZ=KST-9 date` (이 PC Git Bash에는 zoneinfo가 없어 `TZ=Asia/Seoul`은 **UTC**를 낸다) |
| git 신원 | 이 PC에는 없다 → 커밋은 `git -c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com commit …`(`ingest.sh`는 없을 때 스스로 붙인다) |
| 자격 증명 | **이 PC git 자격 증명 하나**(GCM, `credential.helper=manager`) — 스킬 저장소 `git push`와 배포 PUT(`deploy.py`가 `git credential fill`로 얻어 변수에만 둔다) 둘 다. 토큰 파일·대화창 토큰 0. 세션은 `git credential fill`을 직접 치지 않는다 |
| 네이버 API 키 | 키 파일 `~/naver-api.keys.json`(저장소 밖) — `--key-file` 경로만 넘긴다. 세션은 열지도 출력하지도 않는다(`test -f`로 존재만) |
| 수집 폴더 | config `report_fetch.download_dir` `~/saero-fetch/downloads` · 전용 프로필 `profile_dir` `~/saero-fetch/chrome-profile`(`~` = 사용자 홈) |
| 회차 작업물 | 저장소 `work/`(gitignore): `work/combined/` · `work/prev.html` · `work/index.html` · `work/compute.json` · `work/exclusions_proposal_<창끝>.md`·`_candidates.txt` · `work/approved_<날짜>.txt` · `work/exclusions_pull_<날짜>.json` |
| 줄바꿈 | `.gitattributes`: `*.csv -text`(바이트 그대로) · `*.sh text eol=lf`. 작업 폴더가 커밋과 다르게 풀려 있으면 8절 "작업 폴더 줄바꿈" |

## 2. S0 사전 점검 — Bash 한 번, 쓰기 0

아래 블록을 그대로 한 번에 돌린다. 줄마다 `[FAIL]`이면 다음 단계로 가지 않는다(다음 행동은 4절 ⓑ). 외부 쓰기·파일 쓰기 0
(`git fetch`의 원격 ref 갱신만). 키 파일은 존재만 보고, 자격 증명은 값을 출력하지 않는다.

```bash
cd /d/saero/saero-ad-report-skill && export PY=/d/saero/.venv/Scripts/python.exe PYTHONUTF8=1 GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never && unset GIT_ASKPASS SSH_ASKPASS && F=0 && {
git -c credential.interactive=false fetch -q origin || { echo "[FAIL] git fetch"; F=1; }
b=$(git rev-parse --abbrev-ref HEAD); [ "$b" = main ] || { echo "[FAIL] 브랜치 $b — main이어야 함"; F=1; }
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || { echo "[FAIL] HEAD ≠ origin/main — git status -sb 확인(push·pull은 사용자와)"; F=1; }
[ -z "$(git status --porcelain)" ] || { echo "[FAIL] 작업 트리에 변경 있음 — git status"; F=1; }
x=$(git -c core.quotepath=false ls-files --eol -- '*.csv' '*.sh' | awk '{split($1,a,"/");split($2,b,"/"); if(a[2]!=b[2]) print $NF}'); [ -z "$x" ] || { echo "[FAIL] 줄바꿈이 커밋과 다름(8절): $x"; F=1; }
"$PY" -c "import pandas, playwright" 2>/dev/null || { echo "[FAIL] PY에 pandas·playwright 없음: $PY"; F=1; }
h=$(TZ=KST-9 date +%H%M); [ $((10#$h)) -ge 100 ] || { echo "[FAIL] KST $h — 01:00 이후에(어제 집계 완료 전)"; F=1; }
test -f ~/naver-api.keys.json || { echo "[FAIL] 네이버 API 키 파일 없음(존재만 봄) — ③ 불가"; F=1; }
"$PY" -c "import sys; sys.path.insert(0,'scripts'); import fetch_reports as R; sys.exit(3 if R.profile_in_use(R.fetch_config()['profile_dir']) else 0)"; r=$?; [ "$r" -eq 0 ] || { [ "$r" -eq 3 ] && echo "[FAIL] 수집 프로필을 쓰는 크롬이 떠 있음 — 그 창을 모두 닫고 다시" || echo "[FAIL] 프로필 검사 실행 오류(rc=$r — 위 출력 확인)"; F=1; }
timeout 90 git -c credential.interactive=false push --dry-run -q origin HEAD:main || { echo "[FAIL] 스킬 저장소 push --dry-run — 자격 증명, 또는 HEAD ≠ origin/main이면 non-fast-forward(권한 문제로 단정하지 말 것)"; F=1; }
"$PY" scripts/deploy.py push --dry-run | tail -2; [ "${PIPESTATUS[0]}" -eq 0 ] || { echo "[FAIL] 배포 저장소 자격 증명을 얻지 못함(deploy.py push --dry-run — 값 존재까지 확인, 쓰기 권한은 첫 PUT)"; F=1; }
echo "S0 $([ "$F" -eq 0 ] && echo PASS || echo FAIL)"; }
```

## 3. 전 단계 순서

기준: SKILL.md 1 → 2 → 2-1 → 3 → 4 → 5-0 → 5 → 6 → 7 → 8. **승인·등록·확인은 배포 앞**(사용자 결정 2026-09-28). 모든 Bash 호출은 1절 `export` 줄로 시작한다.

| # | 단계 | 명령(작업 폴더) | 멈춤 |
|---|---|---|---|
| S0 | 사전 점검 | 2절 블록 | ⓑ FAIL 줄 |
| ① | 수집 | `"$PY" scripts/fetch_reports.py --prev <직전 성공 폴더 또는 data/YYYY-MM>` — **run_in_background**(사용자 화면에 크롬 창이 뜬다, 3~5분). 달의 첫날은 `--prev` 생략, 10/1처럼 `지난달` 첫 실측·화면 변경 의심 때는 `--debug` | exit 1 로그인 → `--login`을 백그라운드로 띄우고 **사용자가 창에서 로그인** → 본 실행 다시 / exit 1 차단·exit 2 → ⓑ |
| 1 | 보관·합본·push | `scripts/ingest.sh "<성공 폴더>"/*.csv` — 성공 폴더 = fetch 출력 `[PASS] … → <폴더>`·`다음:` 줄(`partial/` 금지) | ⓑ store 거부·combine FAIL·`[FAIL] HEAD ≠ origin/main` |
| 4 | 배포본 받기(2-1 전에 당겨서, 읽기) | `"$PY" scripts/deploy.py fetch --out work/prev.html && cp work/prev.html work/index.html` | ⓑ GET 실패 |
| 5a | 계산만(쓰기 = `work/compute.json`) | `"$PY" scripts/compute.py work/combined --competitors-html work/prev.html -o work/compute.json` — 2-1 대조를 형식까지 같게 하려고 당긴다(교체는 5단계) | ⓑ |
| 2-1 | 기간 대조 | `compute.json`의 `masthead` 문자열 ↔ `work/prev.html`의 `집계 기간<b>…</b>` | **같으면 3·5-0a를 건너뛰고 곧바로 ⓐ(이 질문 하나만 — 같은 데이터라 다른 후보가 의미 없다)**: "그래도 다시 계산할까요?" |
| 3 | 제외 그룹 | 합본 키워드로 SKILL.md "제외 그룹 판정" 규칙(세션 판정) | 신규 후보 → ⓐ 묶음 |
| 5-0a | 후보 | (권장) `"$PY" scripts/exclusions.py pull --key-file ~/naver-api.keys.json`(읽기 — registry `verified_at`이 바뀐다, 커밋은 5-0c, 5-0c가 없는 회차는 8단계에서 함께) → `"$PY" scripts/exclusions.py propose work/combined --since YYYY-MM-DD`(직전 배포 masthead 끝 날짜 + 1일을 ISO로. 기본 창은 마지막 하루뿐이라 건너뛴 날의 첫 등장 이름이 빠진다) | ⓑ registry 없음 |
| ⓐ | **승인 묶음 한 번** | (1) 새 경쟁사 · (2) 애매 후보 · (3) 제외 그룹 · (4) 제외 검색어(propose 승인 문구 원문) 중 **해당하는 것만** 한 메시지. (1)~(4)가 모두 0일 때만 묻지 않는다 | 답을 기다린다 |
| 5-0b | 답 반영 | config(`competitors`·`excluded_groups`)가 바뀌면 → config 커밋(push는 5-0c와 함께) → compute 재실행(경쟁사가 바뀌면 propose도) | — |
| 5-0c | 등록·확인·기록 | 승인 목록(6절 규칙) `work/approved_<날짜>.txt` → `exclusions.py push --approved … --dry-run`(호출 0, "승인 N개" = 답의 N) → `exclusions.py push --approved … --key-file ~/naver-api.keys.json`(pull → POST → verify) → `exclusions.py report` → registry(+config) 커밋 → `git fetch` → `git push origin main` → HEAD == origin/main | ⓑ exit 1(부분 실패·verified:false) → 재시도는 ⓐ |
| 5 | 교체 | compute.json 값으로 01~12(12번 먼저, 11번 마지막). 07 각주·11·12번에 **등록 n · verified n · 실패 n**을 사실 그대로 | — |
| 6 | 검증 | `scripts/precheck.sh work/index.html work/combined work/prev.html` | ⓑ 세션이 고치고 재실행 |
| 7 | 배포 | `"$PY" scripts/deploy.py push --file work/index.html --message "리포트 갱신: <기간>" --dry-run` → 같은 명령(dry-run 없이) → `"$PY" scripts/deploy.py verify --file work/index.html` | ⓑ PUT 실패·verify 불일치(재PUT은 사용자) |
| 8 | 기록 | last-audit 갱신 회차 절(Edit) → 1절 신원으로 커밋(pull로 바뀐 registry가 아직 커밋 안 됐으면 함께 — 경로 지정 add) → `git fetch` → `git push origin main` → 스크래치 `git clone -c core.autocrlf=false`로 행수·md5 → 사용자 시크릿 창 확인 요청 | ⓑ push 실패 |

**재개·완료 판정은 대상의 현재 상태로 한다**(세션이 끊겼다 다시 시작할 때): 보관본 = `git fetch` 뒤 HEAD = origin/main(`ingest.sh`가 확인) ·
등록 = `exclusions.py verify --key-file …`(registry note·기억으로 "등록 끝"이라 판정하지 않는다 — note는 verify 뒤에도 "확인 전"이 남는다) ·
배포 = `deploy.py verify --file work/index.html`. state 파일·대화 기억은 근거가 아니다.

**예외 "등록은 나중에"**(사용자가 그렇게 말할 때만): 07·11·12번에 "제안함 — 등록은 사용자 결정으로 다음에"처럼 사실형 문구로 배포하고
`--pending`은 쓰지 않는다. 뒤에 등록하면 4단계를 다시 fetch(새 prev.html)하고 `--pending` 없이 precheck를 통과한 뒤 재배포한다.

## 4. 멈춤 표

**ⓐ 사람 승인(남긴다)**: SKILL.md "승인이 필요한 지점" (1)~(4) · 2-1 "그래도 다시 계산할까요?" · 3단계 새 제외 그룹 ·
등록 실패 재시도·keep·한도 초과 재승인 · delete/test-roundtrip `--confirm`(사용자 입회) · 12번 N주 미반영 질문.

**ⓑ 자동 검사 FAIL(멈추고 → 다음 행동)**

| FAIL | 다음 행동(세션) | 사람 |
|---|---|---|
| S0 줄 | 원인 한 줄 보고, 다음 단계 안 감 | 설치·창 닫기·자격 증명 로그인 |
| fetch exit 2 부분 실패 | `partial/<날짜>/summary.json`을 **재실행 전에** 읽고(재실행이 partial을 지운다) 보고서별 원인 보고 | 다시 받을지 |
| fetch exit 1 금지 차단·허용 밖 | summary.json은 없다(`--debug`여도 — SystemExit가 summary 작성 전에 끝남). 스크린샷은 `--debug`일 때만 `partial/<날짜>/debug/`에 → 원인 불명으로 보고 | `--debug` 재실행 여부 |
| fetch exit 1 로그인 | `--login` 백그라운드 → 끝나면 본 실행 | 창에서 로그인·2단계 인증 |
| store 거부·combine FAIL | 메시지 원문 보고. `--force`·`--chunk` 자동 금지. 월초를 놓쳐 지난달 끝이 비면 평일 fetch로는 못 채운다 → 8절 폴백 | 다시 받기·폴백 |
| store 부분 적용 | `git status data/`로 바뀐 파일 보고(커밋 안 함) | 되돌리기(`git checkout -- data/`) |
| ingest `[FAIL] HEAD ≠ origin/main`·브랜치 | 상태(`git status -sb`) 보고 | push·pull 결정 |
| push 403·거부(ingest `[FAIL] push 실패`) | 어느 저장소인지·커밋이 로컬에만 있는지 적어 보고 | 자격 증명 확인·재시도 |
| registry 없음 | `git status`·경로 점검 | — |
| exclusions exit 1 | 성공/실패를 그룹×이름으로 나눠 보고 | 재시도·keep |
| precheck FAIL | 전체 출력 보고 → 원인 고쳐 재실행(배포 금지) | — |
| deploy verify 불일치 | 멈춤. 출력의 재수령본 sha·md5를 보고(verify를 한 번 더 — 읽기만 — 해 같은지 덧붙인다) | 재PUT 여부 |

**사람만 하는 일**: 네이버 로그인·2단계 인증(`--login` 창) · 팝업·공지 닫기 · 라이브 시크릿 창 확인 · codegen 녹화 · 손 다운로드(8절).

## 5. exit 코드는 출력 줄로 가른다

| 명령 | 코드 | 출력으로 가르기 |
|---|---|---|
| `fetch_reports.py` | 1 | `목록 URL에 도달하지 못함`(로그인) / `허용 목록 밖 동작`·`금지 요소 클릭 시도 차단`(화면 변경) / `playwright가 없습니다`·설정(환경) |
| | 2 | `[FAIL] 4개 중 성공 …`(부분 실패, partial) / 첫 줄 `usage:`(인자 오류) |
| `exclusions.py` | 1 | `[push] 완료: … 실패/미확인 n`(부분 실패) / `401`·ApiError(인증·API) / `[push] 등록할 이름이 없습니다`(전부 거부·후보 0) / `[FAIL] registry 없음` |
| | 2 | `[FAIL] 네트워크 차단(프록시)`(Code 탭에선 나지 않아야 함) / `usage:` |
| `ingest.sh` | 1 | `[FAIL] 현재 브랜치가 main이 아님` / `[FAIL] HEAD … ≠ origin/main` / `[FAIL] push 실패`(커밋은 로컬에만) / `[FAIL] 파이썬을 실행할 수 없음` / archive `[FAIL] …` |
| | 그 밖 | 2 = 사용법(인자 없음) |
| `precheck.sh` | 1 | md5 가드 `[FAIL] 직전 배포본이 작업본과 같다` / validate·compare·overflow(전체 출력) |
| `deploy.py` | 1 | `GET …` / `PUT …` / `불일치` / `[FAIL] 자격 증명을 얻지 못함` · 2 = 인자 |

## 6. 승인 목록 — 복사로만 만든다

- 원천은 셋뿐: ① `work/exclusions_proposal_<창끝>_candidates.txt`(신규·재등록 후보, propose가 씀) ② 제안서 md의 "업종어 포함" 절에서
  사용자가 고른 줄 ③ 합본 `work/combined/검색어.csv` `검색어` 칸 원문(사용자가 07번 표에서 고른 이름·"노원힐링장소." 같은 재상정).
- **세션은 이름을 타이핑하지 않는다.** 파이썬으로 원천 파일의 줄을 그대로 옮기고, 뺄 이름은 줄을 지운다(줄 번호로 지정).
  `_candidates.txt`는 Windows에서 CRLF로 써진다 — 줄 끝 CR은 떼고 옮긴다. 후보 파일에서 만드는 예(2026-09-28 리허설에서 쓴 것,
  인자 = 원천 · 출력 · 답의 N · 뺄 줄 번호…):
  ```bash
  "$PY" - work/exclusions_proposal_<창끝>_candidates.txt work/approved_<날짜>.txt <N> [뺄 줄 번호 …] <<'PY'
  import sys
  src, out, n, drop = sys.argv[1], sys.argv[2], int(sys.argv[3]), {int(x) for x in sys.argv[4:]}
  lines = [l.rstrip("\r\n") for l in open(src, encoding="utf-8-sig")]
  keep = [l for i, l in enumerate(lines, 1) if l.strip() and not l.startswith("#") and i not in drop]
  K = lambda s: s.strip().upper()                      # exclusions.py K()와 같은 대조 키
  assert len(keep) == n, f"줄 수 {len(keep)} != 답의 N {n} — 사용자에게 다시 확인"
  assert all(any(K(k) == K(l) and k == l for l in lines) for k in keep)
  open(out, "w", encoding="utf-8", newline="\n").write("".join(k + "\n" for k in keep))
  print(f"승인 목록 {out}: {len(keep)}줄 = N", *[repr(k) for k in keep])
  PY
  ```
  업종어·재상정 이름을 더할 때도 같은 방식으로 제안서 업종어 절·합본 `검색어.csv`의 해당 줄에서 이름 칸을 복사해 붙인다(줄 수 = N 확인은 끝에 한 번).
- 만든 뒤 확인: 줄 수 = 답의 N · 각 줄이 원천의 한 줄과 `K()`(앞뒤 공백 제거·대문자) 일치이면서 원문 바이트 그대로 · `push --dry-run`의
  "승인 N개" = N. 셋 중 하나라도 다르면 사용자에게 다시 확인한다.
- 사례(2026-09-28): 승인 6개 중 **"노원힐링장소."** — 채팅이 넘긴 목록엔 마침표가 있었는데 Code 탭에서 파일을 다시 쓰며 빠졌다
  (등록 전 registry 사본으로 dry-run 재현: 마침표 없음 216 → 221, 있음 216 → 222 = 채팅 기록 값). 원문은 미등록으로 남았다.
  기호(`;`·`+`·`]`·`.`)도 API는 원문대로 등록한다(9/27 실측) — 원문을 바꿀 이유가 없다.
- 회차 2에서 `exclusions.py push --candidates … --expect N` 코드 가드로 올린다(그 전까지는 이 절이 유일한 방어).

## 7. 금지

- `partial/`·검사 실패·summary 없는 폴더를 store에 넘기기 / `store --force`·`--chunk` 자동 부착
- 승인 이름을 세션이 다시 타이핑하거나 기호·마침표를 지우기 / "등록 승인 N개" 전 `push`·`delete`·`test-roundtrip`
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
사용자와 함께 한 번: 작업 폴더에서 `git status`가 CSV 말고는 깨끗한지 보고 → S0가 이름을 댄 CSV 파일을 지운 뒤 `git checkout -- data`
(커밋 바이트로 다시 풀림) → `git ls-files --eol`로 i/·w/가 같은지 확인. 또는 작업 폴더를 `git clone -c core.autocrlf=false`로 새로 받아
바꿔 끼운다(`work/`의 파일은 옮겨 둔다).

## 9. 리허설 — 외부 쓰기 0으로 전 순서 확인

스크래치에 `git clone -c core.autocrlf=false`로 받은 저장소(또는 기능 브랜치)에서, origin을 **로컬 bare 저장소**로 바꿔 돌린다.
입력은 `data/YYYY-MM` 4개를 data 밖 폴더에 복사한 것(같은 경로를 store에 넘기면 archive.py가 원본을 지운 뒤 복사하다 잃는다).
순서: S0(스킬 저장소 push dry-run은 bare로) → `fetch_reports.py --dry-run`(오늘 · `--today 2026-10-01`, 수집·프로필 폴더는 스크래치) →
`ingest.sh`(bare로 push) → `deploy.py fetch`(무인증) → `propose --since` → 6절 규칙으로 승인 목록 → `push --dry-run` → compute →
precheck(작업본 = 배포본 사본 + 주석 1줄 — md5 가드 통과용) → `deploy.py push --dry-run` → `verify`(같은 파일 일치 · 바꾼 사본 불일치 exit 1).
판정: 작업 폴더·실제 원격의 data·config·registry md5, `git status`, 두 저장소 `git ls-remote` HEAD가 전후 같다. fetch 폴더 미생성.
