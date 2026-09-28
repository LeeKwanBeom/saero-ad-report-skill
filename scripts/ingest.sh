#!/usr/bin/env bash
# 1단계 한 번에: store → combine → 보관본 push. 어느 단계든 실패하면 거기서 멈춘다(set -e).
# 사용법: PY=<venv 파이썬> scripts/ingest.sh <CSV> [<CSV> ...]   (합본은 저장소 work/combined — references/code-tab.md)
#   push는 이 PC의 git 자격 증명으로 `git push origin HEAD:main`(토큰 인자 없음). main 브랜치에서만 돈다(쓰기 전에 확인).
#   시작 검사(store 전, 쓰기 0으로 멈춤): 원격 main을 읽어(git fetch → FETCH_HEAD) HEAD와 같은지 · data/가 HEAD와 같은지
#   (`git diff --quiet HEAD -- data` — 스테이징·미스테이징 모두, 수정 회차 3 W2 · 추적 안 된 파일 0) · data/*.csv 줄바꿈이 커밋과 같은지
#   (ls-files --eol i/ = w/ — stat만 깨끗한 CRLF 작업 파일까지. `git add data`가 CRLF 바이트를 커밋하지 않게, 2026-09-28 수정 회차 2 N3).
#   push 뒤와 "data/ 변경 없음" 두 분기도 원격 main을 다시 읽어 HEAD와 같아야 통과한다 —
#   커밋만 되고 push 안 된 상태가 "변경 없음"으로 숨지 않게(2026-09-28 탐색 기준선 6절 공통 보정).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-python3}"; export PYTHONUTF8=1
export GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never; unset GIT_ASKPASS SSH_ASKPASS   # 자격 증명 창·프롬프트로 멈추지 않는다
OUT="$ROOT/work/combined"
if [ "$#" -lt 1 ]; then echo "사용법: PY=<venv 파이썬> scripts/ingest.sh <CSV> [<CSV> ...]"; exit 2; fi
"$PY" -c 'import sys' 2>/dev/null || { echo "[FAIL] 파이썬을 실행할 수 없음: PY=$PY — Code 탭은 PY=<venv 파이썬>(references/code-tab.md 1절)"; exit 1; }
BR="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
if [ "$BR" != "main" ]; then echo "[FAIL] 현재 브랜치가 main이 아님($BR) — 보관본은 main에만 올린다. 아무것도 쓰지 않고 멈춤"; exit 1; fi
GITID=()   # 이 PC처럼 git 신원이 없을 때만 저장소 기록 신원(checklist [마무리])을 붙인다
git -C "$ROOT" config user.name >/dev/null || GITID+=(-c user.name=LeeKwanBeom)
git -C "$ROOT" config user.email >/dev/null || GITID+=(-c user.email=322668067+LeeKwanBeom@users.noreply.github.com)
synced() {  # 원격 main을 다시 읽어(FETCH_HEAD — single-branch clone에서도 방금 받은 값) HEAD와 같은지. fetch 실패는 set -e로 멈춤(rc 128 `fatal:`)
  git -C "$ROOT" -c credential.interactive=false fetch -q origin main
  local h o; h="$(git -C "$ROOT" rev-parse HEAD)"; o="$(git -C "$ROOT" rev-parse FETCH_HEAD)"
  if [ "$h" != "$o" ]; then echo "[FAIL] HEAD ${h:0:7} ≠ origin/main ${o:0:7} — $1"; exit 1; fi
  echo "origin/main = HEAD ${h:0:7} 확인"
}
echo "== 시작 검사(store 전 — 실패하면 쓰기 0으로 멈춤)"
synced "시작 전 — store 전에 멈춤(쓰기 0). push 안 된 커밋이 있거나 원격이 앞서 있음(git status -sb로 확인 — push·pull은 사용자와 정한다)"
if ! git -C "$ROOT" diff --quiet HEAD -- data; then
  echo "[FAIL] data/가 HEAD와 다름(스테이징·미스테이징) — store 전에 멈춤(쓰기 0). git status data/로 보고, 되돌리기는 사용자와(references/code-tab.md 4절 git restore --source=HEAD --staged --worktree -- data — 스테이징된 새 파일까지)"
  git -C "$ROOT" -c core.quotepath=false status --short -- data; exit 1; fi
UNTR="$(git -C "$ROOT" -c core.quotepath=false ls-files --others --exclude-standard -- data)"   # diff는 추적 안 된 파일을 못 본다 — `git add data`가 그것까지 커밋하지 않게
if [ -n "$UNTR" ]; then echo "[FAIL] data/에 추적 안 된 파일이 있음 — store 전에 멈춤(쓰기 0). store 부분 적용·손으로 둔 파일일 수 있다(지우기는 사용자와 — git clean -n -- data로 목록만):"; echo "$UNTR" | sed 's/^/  /'; exit 1; fi
EOL="$(git -C "$ROOT" -c core.quotepath=false ls-files --eol -- 'data/*.csv' | awk -F'\t' '{split($1,f," "); i=f[1]; w=f[2]; sub(/^i\//,"",i); sub(/^w\//,"",w); if(i!=w) print $2 (w=="" ? " (작업 폴더에 없음)" : "")}')"
if [ -n "$EOL" ]; then echo "[FAIL] data/ CSV 줄바꿈이 커밋과 다름(ls-files --eol i/ ≠ w/) — store 전에 멈춤(쓰기 0). references/code-tab.md 8절 '작업 폴더 줄바꿈':"; echo "$EOL" | sed 's/^/  /'; exit 1; fi
echo "data/ CSV 줄바꿈 = 커밋 확인"
echo "== store"; "$PY" "$ROOT/scripts/archive.py" store "$@"
echo "== combine"; "$PY" "$ROOT/scripts/archive.py" combine "$OUT"
echo "== push data/"
cd "$ROOT"
git add data
if git diff --cached --quiet -- data; then
  echo "data/ 변경 없음 — 새 커밋 없음"
  synced "push 안 된 커밋이 있거나 원격이 앞서 있음(git status -sb로 확인 — push·pull은 사용자와 정한다)"
else
  MSG="data: $("$PY" - "$OUT" <<'PY'
import sys, pandas as pd; kw=pd.read_csv(sys.argv[1]+'/키워드.csv', skiprows=1); print(f"보관본 갱신 (합본 {kw['일별'].min()}~{kw['일별'].max()} {kw['일별'].nunique()}일)")
PY
)"
  git ${GITID[@]+"${GITID[@]}"} commit -q -m "$MSG" -- data   # data/만 커밋(다른 스테이징은 섞지 않는다)
  git -c credential.interactive=false push -q origin HEAD:main || {
    echo "[FAIL] push 실패 — 커밋 $(git rev-parse --short HEAD)는 로컬에만 있다(자격 증명·원격 상태를 사용자와 확인, 재시도는 사용자 결정)"; exit 1; }
  synced "push가 원격에 반영되지 않음"
  echo "push 완료: $MSG"
fi
echo "== 1단계 완료. 합본: $OUT"
