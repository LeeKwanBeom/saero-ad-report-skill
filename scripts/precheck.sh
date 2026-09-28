#!/usr/bin/env bash
# 6단계 한 번에: validate(검산) → compute+compare(배포 전 차이 0) → overflow(3폭). 하나라도 실패하면 exit 1.
# 사용법: PY=<venv 파이썬> scripts/precheck.sh <작업중 index.html> <합본폴더> <직전 배포본 index.html> [--pending]
#   <직전 배포본>은 4단계 deploy.py fetch가 저장한 파일(work/prev.html) — 07 경쟁사표의 정본으로 compute에 넘긴다.
#   작업본을 넣으면 작업본의 표가 정본이 돼 검사가 무력화되므로(2026-09-27 검증 (c)) md5가 같으면 멈춘다.
#   --pending 은 validate에만 넘긴다(사용자 답 대기 배포 — 잔존 문구 검사 허용). 답을 반영한 재배포에는 금지.
#   compute.json은 작업본 옆(같은 폴더)에 쓴다. validate·compare는 통과면 끝 3줄, 실패면 전체 출력(종료 코드는 그대로).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; PENDING=(); ARGS=()
PY="${PY:-python3}"; export PYTHONUTF8=1
for a in "$@"; do if [ "$a" = "--pending" ]; then PENDING=(--pending); else ARGS+=("$a"); fi; done
if [ "${#ARGS[@]}" -ne 3 ]; then echo "사용법: PY=<venv 파이썬> scripts/precheck.sh <작업중 index.html> <합본폴더> <직전 배포본 index.html> [--pending]"; exit 2; fi
HTML="${ARGS[0]}"; C="${ARGS[1]}"; PREV="${ARGS[2]}"; J="$(dirname "$HTML")/compute.json"
"$PY" -c 'import sys' 2>/dev/null || { echo "[FAIL] 파이썬을 실행할 수 없음: PY=$PY — Code 탭은 PY=<venv 파이썬>(references/code-tab.md 1절)"; exit 1; }
if [ "$(md5sum < "$HTML" | cut -c1-32)" = "$(md5sum < "$PREV" | cut -c1-32)" ]; then   # 표준 입력으로 — 파일명의 \ 때문에 출력 앞에 \가 붙는 것 방지
  echo "[FAIL] 직전 배포본이 작업본과 같다 — 3번째 인자에는 4단계 deploy.py fetch가 저장한 직전 배포본(work/prev.html)을 넣어라"; exit 1; fi
run() {  # 통과면 끝 3줄(종전과 같음), 실패면 전체 출력 뒤 같은 종료 코드로 멈춘다
  local out rc=0
  out="$("$@")" || rc=$?
  if [ "$rc" -eq 0 ]; then printf '%s\n' "$out" | tail -n 3; else printf '%s\n' "$out"; exit "$rc"; fi
}
echo "== validate ${PENDING[*]:-}"; run "$PY" "$ROOT/scripts/validate.py" "$HTML" "$C/키워드.csv" "$C/검색어.csv" "$C/시간대별.csv" "$C/상세지역.csv" ${PENDING[@]+"${PENDING[@]}"}
echo "== compute(직전 배포본 $PREV 경쟁사표 기준) → compare"; "$PY" "$ROOT/scripts/compute.py" "$C" --competitors-html "$PREV" -o "$J"
run "$PY" "$ROOT/scripts/compare.py" "$HTML" "$J"
echo "== overflow"; "$PY" "$ROOT/tests/overflow_check.py" "$HTML"
echo "== 6단계 전부 통과"
