#!/usr/bin/env bash
# 6단계 한 번에: validate(검산) → compute+compare(배포 전 차이 0) → overflow(3폭) → narrative(서술 미교체, 2026-10-06). 하나라도 실패하면 exit 1.
# 사용법: PY=<venv 파이썬> scripts/precheck.sh <작업중 index.html> <합본폴더> <직전 배포본 index.html> [--pending]
#   <직전 배포본>은 4단계 deploy.py fetch가 저장한 파일(work/prev.html) — 07 경쟁사표의 정본으로 compute에 넘긴다.
#   작업본을 넣으면 작업본의 표가 정본이 돼 검사가 무력화되므로(2026-09-27 검증 (c)) md5가 같으면 멈춘다.
#   --pending 은 validate에만 넘긴다(사용자 답 대기 배포 — 잔존 문구 검사 허용). 답을 반영한 재배포에는 금지.
#   compute.json은 작업본 옆(같은 폴더)에 쓴다. validate·compare는 통과면 끝 3줄, 실패면 전체 출력(종료 코드는 그대로).
#   (2026-10-09 판 F) 광고비 잔액 카드 — 작업본 옆 balance.json(5단계 balance.py 의 잔액 기록)을 validate·compute 에 --balance 로 넘긴다.
#   없거나 꼴이 다르거나 지난 회차 기록이면 validate "광고비 잔액 카드" FAIL(그 뒤 compute 도 [FAIL]) — 이 스크립트가 따로 검사하지는 않는다.
#   전부 통과하면 작업본 옆에 도장 precheck_ok.md5를 쓴다 — 1줄 `<작업본 md5>  <이름>` · 2줄 `<직전 배포본 md5>  <이름>` · 3줄 `mode full|pending`.
#   deploy.py 실제 push는 작업본 md5 = --file, 직전 배포본 md5 = --base일 때만 PUT(수정 회차 3 W11·4 X2 — pending이면 [주의]만).
#   인자 수가 맞으면 무엇보다 먼저 옛 도장을 지우고(파일 없음 FAIL에도 — 이번 실행이 끝까지 통과해야 다시 생긴다), 작업본 md5를 시작·끝 두 번 재 같을 때만 쓴다(도중에 바뀌면 [FAIL]).
#   작업본·직전 배포본 파일이 없으면 md5 가드 전에 [FAIL] exit 2.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; PENDING=(); ARGS=()
PY="${PY:-python3}"; export PYTHONUTF8=1
for a in "$@"; do if [ "$a" = "--pending" ]; then PENDING=(--pending); else ARGS+=("$a"); fi; done
if [ "${#ARGS[@]}" -ne 3 ]; then echo "사용법: PY=<venv 파이썬> scripts/precheck.sh <작업중 index.html> <합본폴더> <직전 배포본 index.html> [--pending]"; exit 2; fi
HTML="${ARGS[0]}"; C="${ARGS[1]}"; PREV="${ARGS[2]}"; J="$(dirname "$HTML")/compute.json"; STAMP="$(dirname "$HTML")/precheck_ok.md5"; BAL="$(dirname "$HTML")/balance.json"
rm -f "$STAMP"
for f in "$HTML" "$PREV"; do [ -f "$f" ] || { echo "[FAIL] 파일 없음: $f — 작업본(work/index.html)·직전 배포본(work/prev.html) 경로 확인"; exit 2; }; done
"$PY" -c 'import sys' 2>/dev/null || { echo "[FAIL] 파이썬을 실행할 수 없음: PY=$PY — Code 탭은 PY=<venv 파이썬>(references/code-tab.md 1절)"; exit 1; }
M0="$(md5sum < "$HTML" | cut -c1-32)"; P0="$(md5sum < "$PREV" | cut -c1-32)"   # 표준 입력으로 — 파일명의 \ 때문에 출력 앞에 \가 붙는 것 방지
MODE=full; [ "${#PENDING[@]}" -eq 0 ] || MODE=pending
if [ "$M0" = "$P0" ]; then
  echo "[FAIL] 직전 배포본이 작업본과 같다 — 3번째 인자에는 4단계 deploy.py fetch가 저장한 직전 배포본(work/prev.html)을 넣어라"; exit 1; fi
run() {  # 통과면 끝 3줄(종전과 같음), 실패면 전체 출력 뒤 같은 종료 코드로 멈춘다
  local out rc=0
  out="$("$@")" || rc=$?
  if [ "$rc" -eq 0 ]; then printf '%s\n' "$out" | tail -n 3; else printf '%s\n' "$out"; exit "$rc"; fi
}
echo "== validate ${PENDING[*]:-}"; run "$PY" "$ROOT/scripts/validate.py" "$HTML" "$C/키워드.csv" "$C/검색어.csv" "$C/시간대별.csv" "$C/상세지역.csv" --balance "$BAL" ${PENDING[@]+"${PENDING[@]}"}
echo "== compute(직전 배포본 $PREV 경쟁사표 기준) → compare"; "$PY" "$ROOT/scripts/compute.py" "$C" --competitors-html "$PREV" --balance "$BAL" -o "$J"
run "$PY" "$ROOT/scripts/compare.py" "$HTML" "$J"
echo "== overflow"; "$PY" "$ROOT/tests/overflow_check.py" "$HTML"
echo "== narrative(서술 미교체)"; run "$PY" "$ROOT/scripts/narrative_check.py" "$HTML" "$PREV"
M1="$(md5sum < "$HTML" | cut -c1-32)"
if [ "$M1" != "$M0" ]; then echo "[FAIL] 작업본이 precheck 도중 바뀜(시작 md5 ${M0:0:8} ≠ 끝 ${M1:0:8}) — 도장 안 씀, precheck를 다시"; exit 1; fi
printf '%s  %s\n%s  %s\nmode %s\n' "$M0" "$(basename "$HTML")" "$P0" "$(basename "$PREV")" "$MODE" > "$STAMP"
echo "== 6단계 전부 통과 — 도장 $STAMP(작업본 ${M0:0:8}… · 직전 배포본 ${P0:0:8}… · 모드 $MODE)"
