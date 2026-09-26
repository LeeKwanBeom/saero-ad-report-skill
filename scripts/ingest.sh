#!/usr/bin/env bash
# 1단계 한 번에: store → combine → 보관본 push. 어느 단계든 실패하면 거기서 멈춘다(set -e).
# 사용법: scripts/ingest.sh <스킬저장소 토큰파일> <업로드CSV> [<업로드CSV> ...]   (합본은 /home/claude/work/combined)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; TOK="$1"; shift
OUT=/home/claude/work/combined
echo "== store"; python3 "$ROOT/scripts/archive.py" store "$@"
echo "== combine"; python3 "$ROOT/scripts/archive.py" combine "$OUT"
echo "== push data/"
cd "$ROOT" && git add data && (git diff --cached --quiet && echo "data/ 변경 없음 — push 생략" || {
  MSG="data: $(python3 - "$OUT" <<'PY'
import sys, pandas as pd; kw=pd.read_csv(sys.argv[1]+'/키워드.csv', skiprows=1); print(f"보관본 갱신 (합본 {kw['일별'].min()}~{kw['일별'].max()} {kw['일별'].nunique()}일)")
PY
)"; git commit -q -m "$MSG" && git push -q "https://x-access-token:$(cat "$TOK")@github.com/LeeKwanBeom/saero-ad-report-skill.git" HEAD:main && echo "push 완료: $MSG"; })
echo "== 1단계 완료. 합본: $OUT"
