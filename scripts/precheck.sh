#!/usr/bin/env bash
# 6단계 한 번에: validate(검산) → compute+compare(배포 전 차이 0) → overflow(3폭). 하나라도 실패하면 exit 1.
# 사용법: scripts/precheck.sh <작업중 index.html> [합본폴더=/home/claude/work/combined]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; HTML="$1"; C="${2:-/home/claude/work/combined}"; J=/home/claude/work/compute.json
echo "== validate"; python3 "$ROOT/scripts/validate.py" "$HTML" "$C/키워드.csv" "$C/검색어.csv" "$C/시간대별.csv" "$C/상세지역.csv" | tail -n 3
echo "== compute → compare"; python3 "$ROOT/scripts/compute.py" "$C" --competitors-html "$HTML" -o "$J" && python3 "$ROOT/scripts/compare.py" "$HTML" "$J" | tail -n 3
echo "== overflow"; python3 "$ROOT/tests/overflow_check.py" "$HTML"
echo "== 6단계 전부 통과"
