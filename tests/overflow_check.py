#!/usr/bin/env python3
"""모바일 폭에서 페이지 가로 넘침 검사 (css-and-layout.md 버그 기록 10).

사용법: $PY tests/overflow_check.py <index.html> [폭 ...]   (기본 360 390 430)
각 폭에서 document.documentElement.scrollWidth == 뷰포트 폭이면 PASS. 하나라도 넘치면 exit 1.
넘치는 텍스트는 요소 박스가 아니라 텍스트 노드라 getBoundingClientRect로는 안 잡힌다 — scrollWidth로 본다.
file:// 밖 요청(cdnjs Chart.js 등)은 전부 막는다 — 어느 환경에서나 "Chart.js 미로드 상태"로 잰다(checklist [의도된 동작] 17).
(2026-10-06 회차 2) 재기 전에 접기(details)를 전부 연다 — 접힌 안의 표·목록이 넘치는지까지 본다. 가로 폭만 본다(닫힘·열림 높이는 이 도구 몫이 아님).
"""
import os
import sys

from playwright.sync_api import sync_playwright

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — fetch_reports.py·exclusions.py와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = os.path.abspath(sys.argv[1])
    widths = [int(w) for w in sys.argv[2:]] or [360, 390, 430]
    bad = []
    blocked = []

    def only_file(route):  # file:// 밖은 보내지 않는다(외부 요청 0)
        if route.request.url.startswith("file:"):
            route.continue_()
        else:
            blocked.append(route.request.url)
            route.abort()

    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in widths:
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.route("**/*", only_file)
            pg.goto("file://" + path)
            pg.wait_for_timeout(400)
            nd = pg.evaluate("(() => { const d = document.querySelectorAll('details'); d.forEach(x => x.open = true); return d.length; })()")
            pg.wait_for_timeout(100)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            ok = sw <= w
            print(f"[{'PASS' if ok else 'FAIL'}] {w}px: scrollWidth {sw} (details {nd}개 연 상태)")
            if not ok:
                bad.append(w)
            pg.close()
        b.close()
    print(f"외부 요청 차단 {len(blocked)}건(file:// 밖 — 보내지 않음)")
    if bad:
        print(f"가로 넘침 {bad} — 긴 숫자 나열엔 `·<wbr>`, 안전망 body{{overflow-wrap:anywhere}} 확인")
        return 1
    print("넘침 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
