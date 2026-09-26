#!/usr/bin/env bash
# 6단계 한 번에: validate(검산) → compute+compare(배포 전 차이 0) → overflow(3폭). 하나라도 실패하면 exit 1.
# 사용법: scripts/precheck.sh <작업중 index.html> <합본폴더> <직전 배포본 index.html> [--pending]
#   <직전 배포본>은 4단계 deploy.py fetch가 저장한 파일(/home/claude/work/prev.html) — 07 경쟁사표의 정본으로 compute에 넘긴다.
#   작업본을 넣으면 작업본의 표가 정본이 돼 검사가 무력화되므로(2026-09-27 검증 (c)) md5가 같으면 멈춘다.
#   --pending 은 validate에만 넘긴다(사용자 답 대기 배포 — 잔존 문구 검사 허용). 답을 반영한 재배포에는 금지.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; PENDING=(); ARGS=()
for a in "$@"; do if [ "$a" = "--pending" ]; then PENDING=(--pending); else ARGS+=("$a"); fi; done
if [ "${#ARGS[@]}" -ne 3 ]; then echo "사용법: scripts/precheck.sh <작업중 index.html> <합본폴더> <직전 배포본 index.html> [--pending]"; exit 2; fi
HTML="${ARGS[0]}"; C="${ARGS[1]}"; PREV="${ARGS[2]}"; J=/home/claude/work/compute.json
if [ "$(md5sum "$HTML" | cut -c1-32)" = "$(md5sum "$PREV" | cut -c1-32)" ]; then
  echo "[FAIL] 직전 배포본이 작업본과 같다 — 4단계 fetch 파일(/home/claude/work/prev.html)을 넣어라"; exit 1; fi
echo "== validate ${PENDING[*]:-}"; python3 "$ROOT/scripts/validate.py" "$HTML" "$C/키워드.csv" "$C/검색어.csv" "$C/시간대별.csv" "$C/상세지역.csv" "${PENDING[@]}" | tail -n 3
echo "== compute(직전 배포본 $PREV 경쟁사표 기준) → compare"; python3 "$ROOT/scripts/compute.py" "$C" --competitors-html "$PREV" -o "$J" && python3 "$ROOT/scripts/compare.py" "$HTML" "$J" | tail -n 3
echo "== overflow"; python3 "$ROOT/tests/overflow_check.py" "$HTML"
echo "== 6단계 전부 통과"
