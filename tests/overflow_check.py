#!/usr/bin/env python3
"""모바일 폭에서 페이지 가로 넘침 검사 (css-and-layout.md 버그 기록 10).

사용법: python3 tests/overflow_check.py <index.html> [폭 ...]   (기본 360 390 430)
각 폭에서 document.documentElement.scrollWidth == 뷰포트 폭이면 PASS. 하나라도 넘치면 exit 1.
넘치는 텍스트는 요소 박스가 아니라 텍스트 노드라 getBoundingClientRect로는 안 잡힌다 — scrollWidth로 본다.
"""
import os
import sys

from playwright.sync_api import sync_playwright


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = os.path.abspath(sys.argv[1])
    widths = [int(w) for w in sys.argv[2:]] or [360, 390, 430]
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in widths:
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto("file://" + path)
            pg.wait_for_timeout(400)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            ok = sw <= w
            print(f"[{'PASS' if ok else 'FAIL'}] {w}px: scrollWidth {sw}")
            if not ok:
                bad.append(w)
            pg.close()
        b.close()
    if bad:
        print(f"가로 넘침 {bad} — 긴 숫자 나열엔 `·<wbr>`, 안전망 body{{overflow-wrap:anywhere}} 확인")
        return 1
    print("넘침 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
