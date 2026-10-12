---
name: q-saero-run
description: saero 광고 리포트 전 단계 실행(/q-saero-run, 광고 리포트 업데이트, 주간리포트 갱신, 보고서 받기, 제외 검색어 등록). 이 PC Code 탭(D:\saero)에서 수집 → 보관·합본 → 리포트 갱신 → 제외 검색어 승인·등록·확인 → 배포 → 기록을 한 세션으로 잇는다. 설치본 saero-ad-report(부트스트랩) 대신 이 스킬을 쓴다.
---
# saero 전 단계 실행 — 진입(정본은 저장소)

이 파일은 얇은 안내다. 절차·규칙·명령의 정본은 작업 폴더 저장소의 `references/code-tab.md`와 `SKILL.md`다 — 다르면 저장소를 따른다.
(이 파일의 정본 사본은 저장소 `local/q-saero-run/SKILL.md`. 고칠 때는 저장소를 고치고, 이 자리에 두는 것은 사용자가 한다.)

1. 작업 폴더로: `cd /d/saero/saero-ad-report-skill`(main 하나). Desktop 사본·검증 clone·기능 브랜치 clone은 쓰지 않는다.
2. `references/code-tab.md`를 처음부터 읽고, `SKILL.md`와 `audit/last-audit.md` 맨 위 절을 읽는다.
3. code-tab.md 2절 **S0 사전 점검 블록**을 그대로 한 번 돌린다. `[FAIL]` 줄이 있으면 거기서 멈추고 보고한다.
4. S0 PASS면 code-tab.md 3절 순서대로: ① 수집(백그라운드 — 4개 뒤 같은 실행이 추가 수집, 끝 줄 `· 추가:` 실패는 멈춤 아님) → 1 ingest → 1x `extras.py store "<성공 폴더>/extra"` → `extras.py combine --out work/extra`(`[주의]`는 멈춤 아님) → 4 fetch(→ `deploy.py public --file work/prev.html` 공개 대조 — `[주의]`면 그 `--seen`을 7 의 live 에) → compute(계산만) → 2-1
   → 3 → 5-0 propose → **승인 묶음 한 번** → (config가 바뀌면 5-0b) → 등록·확인·registry 기록 → 5 교체 → 6 precheck → 7 배포(`--base work/prev.html` · verify는 `--ref <push가 찍은 커밋>` → 그 일치 줄의 `다음(읽기): deploy.py live …`를 **run_in_background**) → 8 기록(머리·줄 = live 의 `기록 머리:`·`기록 줄:` 그대로 — "배포 완료"는 live exit 0 일 때만 · guard 가 `work/live_ok` 와 대조).
   세션이 끊겼다 다시 시작하면 "했었냐"는 대상 현재 상태(ingest의 origin/main 확인·`exclusions.py verify --key-file … --approved <이번 회차 propose(.md5) 뒤에 생긴 가장 최근 work/approved_*.txt>` — 없으면 이번 회차 push는 POST 전·`deploy.py verify --ref <push 커밋>` → 그 일치 줄이 찍은 live(`--commit` 은 deploy.py 가 고른다 — HEAD 메시지가 재배포 접두이고 부모 = push 커밋이면 HEAD, 아니면 push 커밋))로 판정한다.

지키는 것(전체 목록은 code-tab.md 7절):
- 매 Bash 호출 첫머리 `export PY=/d/saero/.venv/Scripts/python.exe PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never; unset GIT_ASKPASS SSH_ASKPASS`.
  `python3` 금지. KST는 `TZ=KST-9 date`.
- 설치본 `saero-ad-report`(부트스트랩)를 부르지 않는다. 그 1절의 컨테이너 경로를 이 PC에 만들지 않는다.
- 토큰·키 파일을 열거나 출력하지 않는다(경로만 인자로). `git credential fill`을 직접 치지 않는다.
- 승인 목록은 `exclusions.py push --from-candidates … --expect N`(참조 선택 모드, code-tab.md 6절) — 세션은 줄·행 번호와 N만 넘기고 이름을 쓰지 않는다.
- 사람 승인 (1)~(4)는 한 메시지로 묻고 답을 기다린다. 외부 쓰기(push·POST·PUT·PATCH)를 자동 재시도하지 않는다.
  승인 답의 N은 숫자(예 "등록 승인 12개") — N이 숫자가 아니거나 "위 2가지만"처럼 모호하면 dry-run 목록을 보이고 되묻는다.
- 배포는 따로 묻지 않는다(사용자 결정 2026-09-30): 사람 질문에 모두 답을 받고 6 precheck·7 dry-run이 통과하면 바로 PUT → verify `--ref` → live.
  검사 FAIL·남은 질문(되묻기·등록 재시도)·사용자 "보류"면 PUT 없음(자동 재시도 금지 그대로).
  **자동 배포 = 7단계 `deploy.py push`(답을 반영한 재배포 push 포함 — 2026-09-30 그대로) — `redeploy`(빈 커밋)는 그 밖, 사용자 답 '재배포' 원문 뒤에만(그 밖 답·무응답이면 쓰기 0 · 기록 재배포 0/1).**
  옛 낱말 '재배포' = 답을 반영한 push · 답 '재배포' = redeploy. live exit 1 `[멈춤]`이면 찍힌 `재배포 질문` 문구 그대로 한 번 묻고("멈춘 실행 #n — Actions 화면에서 'Cancel workflow' 가 보이면 먼저 눌러 보세요(사람). 그다음 '재배포' 라고 답하면 1번만 새 배포를 일으킵니다."),
  답 "재배포" → `redeploy`(dry-run) → 통과면 같은 명령 `--confirm` 1번 → 찍힌 live → exit 0 아니면 "GitHub 쪽 대기 — 기다림"으로 기록하고 멈춘다(두 번째 재배포 없음 · 배포 저장소 `git push` 금지). live exit 3(CDN)은 재배포를 묻지 않고 live 한 번 더.
- 2-1 기간이 같으면 승인 묶음 ⓐ와 별개의 앞 질문 하나만 하고 답을 기다린다 — 답 "다시 계산" → 3 → 5-0a → ⓐ(해당만) → 5-0b(해당 시) → 5-0c → 5 → 6 → 7 → 8 /
  "CSV 다시" → ① / "미룬 등록만"(직전 회차 기록이 "등록 미룸"일 때만) → 3 건너뜀 → 5-0a(`--since` = 미룬 회차 창 시작) → ⓐ → 5-0c → 5(07·11·12 문구만) →
  6(`--pending` 없이, 3번째 인자 = 이번 4단계 fetch) → 7 → 8.
- 커밋은 `git -c user.name=LeeKwanBeom -c user.email=322668067+LeeKwanBeom@users.noreply.github.com commit …`, add는 경로 지정(`git add -A` 금지).
- 사용자 설정(settings·env·권한 허용 목록)은 바꾸지 않는다. 끝나면 사용자의 "마감" → wrapup.
