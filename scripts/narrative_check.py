#!/usr/bin/env python3
"""서술 미교체 검사(6단계 precheck) — 매 회차 다시 써야 하는 서술 블록이 직전 배포본과 바이트까지 같으면 멈춘다.

사용법: "$PY" scripts/narrative_check.py <작업본 index.html> <직전 배포본 index.html>

서술 표지(references/report-structure.md "서술 표지"): `<!-- n:<자리>:<매회차|고정> -->…<!-- /n -->`
- 매회차 = 마지막 날짜(M/D)·일차·회차 수가 들어 있어 값이 같아도 문구가 바뀌어야 하는 블록. 고정 = 표 설명·규칙(대조 안 함).
- 판정 순서:
  1. 작업본 표지 0개 → [FAIL](0건 가드 — 표지를 통째로 잃은 작업본) · 표지 짝·이름이 어긋나면(여는 표지 수 ≠ 짝 수, 이름 중복) [FAIL]
  2. 두 파일의 `집계 기간<b>…</b>` 이 같으면 → `[주의] 같은 기간 — 대조 생략` exit 0(2-1 같음 경로: "다시 계산"·"미룬 등록만"·첫 적용 경로 C)
  3. 직전 배포본에 표지가 없으면 → `[주의] 직전 배포본에 표지 없음 — 대조 생략` exit 0(첫 적용)
  4. 그 밖엔 작업본의 매회차 블록마다 직전 배포본의 같은 이름 블록과 바이트가 같으면 `[FAIL] 서술 미교체 <자리>` exit 1
- compare.py 가 숫자를 읽지 않는 서술(01 해석·07 각주·12 등)이 지난 회차 그대로 배포되는 것(2026-10-06 01 머리글·07 ✓ 사례)을 막는다.
종료 코드: 0 = 통과(또는 [주의]로 생략), 1 = 실패.
"""
import re
import sys

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — 다른 스크립트와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

OPEN = re.compile(r"<!-- n:")
BLOCK = re.compile(r"<!-- n:([^\s:]+):(매회차|고정) -->(.*?)<!-- /n -->", re.S)
PERIOD = re.compile(r"집계 기간<b>([^<]+)</b>")


def blocks(html):
    """[(자리, 종류, 안쪽 문자열)] — 문서 순서."""
    return BLOCK.findall(html)


def check(work_html, prev_html):
    """(종료 코드, 출력 줄 목록)."""
    out = []
    bw = blocks(work_html)
    if not bw:
        return 1, ["[FAIL] 작업본에 서술 표지 0개 — 표지(<!-- n:<자리>:<매회차|고정> -->…<!-- /n -->)를 잃었거나 옛 글 그대로임"]
    names = [n for n, _, _ in bw]
    dup = sorted({n for n in names if names.count(n) > 1})
    n_open = len(OPEN.findall(work_html))
    if dup or n_open != len(bw) or work_html.count("<!-- /n -->") != len(bw):
        return 1, [f"[FAIL] 서술 표지 짝·이름 어긋남 — 여는 표지 {n_open} · 닫는 표지 {work_html.count('<!-- /n -->')} · 짝 {len(bw)}"
                   + (f" · 중복 이름 {dup}" if dup else "")]
    pw, pp = PERIOD.search(work_html), PERIOD.search(prev_html)
    if not pw or not pp:
        return 1, [f"[FAIL] 집계 기간을 못 찾음 — 작업본 {'있음' if pw else '없음'} · 직전 배포본 {'있음' if pp else '없음'}"]
    every = [n for n, k, _ in bw if k == "매회차"]
    if pw.group(1).strip() == pp.group(1).strip():
        return 0, [f"[주의] 같은 기간 — 대조 생략({pw.group(1).strip()} · 표지 {len(bw)}개 중 매회차 {len(every)}개)"]
    bp = {n: body for n, _, body in blocks(prev_html)}
    if not bp:
        return 0, [f"[주의] 직전 배포본에 표지 없음 — 대조 생략(첫 적용 · 작업본 표지 {len(bw)}개 중 매회차 {len(every)}개)"]
    stale = [n for n, k, body in bw if k == "매회차" and n in bp and bp[n] == body]
    new = [n for n in every if n not in bp]
    gone = [n for n in bp if n not in names]
    if new:
        out.append(f"[주의] 직전 배포본에 없던 매회차 표지 {len(new)}개(대조 없음): {', '.join(new)}")
    if gone:
        out.append(f"[주의] 직전 배포본에만 있는 표지 {len(gone)}개: {', '.join(gone)}")
    if stale:
        out += [f"[FAIL] 서술 미교체 {n} — 직전 배포본과 바이트가 같음(이번 회차 문장으로 다시 쓸 것)" for n in stale]
        out.append(f"서술 미교체 {len(stale)}개 / 매회차 {len(every)}개")
        return 1, out
    out.append(f"[PASS] 서술 표지 {len(bw)}개 · 매회차 {len(every)}개 전부 직전 배포본과 다름({pp.group(1).strip()} → {pw.group(1).strip()})")
    return 0, out


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        work_html = f.read()
    with open(sys.argv[2], encoding="utf-8") as f:
        prev_html = f.read()
    rc, lines = check(work_html, prev_html)
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
