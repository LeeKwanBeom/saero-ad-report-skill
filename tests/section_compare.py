#!/usr/bin/env python3
"""섹션 전후 비교 페이지 — 옛 배포본과 작업본의 같은 섹션을 폭마다 캡처해 나란히 놓은 한 파일(compare.html, 그림 base64 내장)을 쓴다.

사용법: "$PY" tests/section_compare.py <작업본 index.html> <직전 배포본 index.html> --out <폴더> [--sections 12] [--widths 1280,390]

자리(2026-10-10 매출 작업 A·C): **precheck 밖** — 리포트 글·행을 바꾸는 기능의 첫 적용 "보류" 회차(운영 세션)에서 도장 뒤 사용자에게 보이는 재료
(판 C·D·F 의 chart_check compare.html 은 상단 카드·01·06 만 — 12번처럼 레이아웃 판을 바꾸지 않는 서술 행 추가는 이 도구로).
- 섹션 = `<!-- Section N: … -->` 주석 바로 뒤 요소(.section). 그 요소만 element screenshot(폭마다 옛·새) — 화면 크기·글꼴은 chart_check 와 같은 조건
  (모바일 폭 ≤ config report_layout.mobile.max_px 는 dpr 2·모바일 UA·터치, 그 밖 dpr 1).
- 밖 요청은 배포본 head 의 cdnjs 두 건(Chart.js·datalabels)만 보내고 나머지는 막고 센다(새 CDN·파일 0 원칙 — 막힌 요청 수를 출력). file:// 그대로.
- 파일 쓰기는 --out 폴더 안(PNG·compare.html)뿐 — 두 HTML 은 읽기만.
종료 코드: 0 = 모든 폭·섹션 캡처 · 1 = 섹션을 못 찾음·캡처 실패 · 2 = 인자.
"""
import argparse
import base64
import html as H
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
from reportlib import load_config  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

CDN_ALLOW = (
    "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js",
)
MARK = """(n) => {
  const it = document.createNodeIterator(document.body, NodeFilter.SHOW_COMMENT);
  let c;
  while ((c = it.nextNode())) {
    if (c.nodeValue.trim().startsWith('Section ' + n + ':')) {
      let e = c.nextSibling;
      while (e && e.nodeType !== 1) e = e.nextSibling;
      if (!e) return null;
      e.setAttribute('data-cmp', 'sec' + n);
      const r = e.getBoundingClientRect();
      return {h: Math.round(r.height), w: Math.round(r.width)};
    }
  }
  return null;
}"""


def capture(pw, path, width, sections, out, tag, max_px):
    mobile = width <= max_px
    browser = pw.chromium.launch()
    try:
        ctx = browser.new_context(viewport={"width": width, "height": 900}, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile)
        blocked = []

        def route(r):
            u = r.request.url
            if u.startswith("file:") or u in CDN_ALLOW:
                return r.continue_()
            blocked.append(u)
            return r.abort()
        ctx.route("**/*", route)
        page = ctx.new_page()
        page.goto("file:///" + os.path.abspath(path).replace("\\", "/"), wait_until="networkidle")
        page.wait_for_timeout(1800)
        res = {}
        for n in sections:
            box = page.evaluate(MARK, n)
            if not box:
                print(f"[FAIL] {tag} {width}px: Section {n} 주석 뒤 요소를 못 찾음 — {path}")
                return None, blocked
            png = os.path.join(out, f"{tag}_{width}_sec{n}.png")
            page.locator(f"[data-cmp=sec{n}]").screenshot(path=png)
            res[n] = (png, box)
        return res, blocked
    finally:
        browser.close()


def img(p):
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("new")
    ap.add_argument("old")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sections", default="12")
    ap.add_argument("--widths", default="1280,390")
    a = ap.parse_args()
    try:
        sections = [int(x) for x in a.sections.split(",")]
        widths = [int(x) for x in a.widths.split(",")]
    except ValueError:
        print("[FAIL] --sections·--widths 는 쉼표로 이은 숫자")
        return 2
    for p in (a.new, a.old):
        if not os.path.isfile(p):
            print(f"[FAIL] 파일 없음: {p}")
            return 2
    os.makedirs(a.out, exist_ok=True)
    max_px = int(load_config()["report_layout"]["mobile"]["max_px"])
    shots, nblock = {}, 0
    with sync_playwright() as pw:
        for w in widths:
            for tag, p in (("old", a.old), ("new", a.new)):
                r, blocked = capture(pw, p, w, sections, a.out, tag, max_px)
                nblock += len(blocked)
                if r is None:
                    return 1
                shots[(tag, w)] = r
    rows = []
    for n in sections:
        rows.append(f"<h2>{n}번 섹션</h2>")
        for w in widths:
            (po, bo), (pn, bn) = shots[("old", w)][n], shots[("new", w)][n]
            rows.append(f"<h3>{w}px — 높이 {bo['h']} → {bn['h']}px</h3><div class='pair'>"
                        f"<figure><figcaption>옛(직전 배포본)</figcaption><img src='data:image/png;base64,{img(po)}' style='width:{min(w, 640)}px'></figure>"
                        f"<figure><figcaption>새(작업본)</figcaption><img src='data:image/png;base64,{img(pn)}' style='width:{min(w, 640)}px'></figure></div>")
            print(f"[캡처] {n}번 {w}px 옛 {bo['w']}×{bo['h']} · 새 {bn['w']}×{bn['h']}")
    doc = ("<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>전후 비교 — {','.join(str(n) for n in sections)}번</title><style>body{{font-family:sans-serif;margin:16px;background:#faf8f3;color:#1c2b2a}}"
           ".pair{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}figure{margin:0}figcaption{font-weight:700;margin:4px 0}"
           "img{border:1px solid #ccc;background:#fff;max-width:100%}</style></head><body>"
           f"<h1>전후 비교 — {','.join(str(n) for n in sections)}번 섹션</h1><p>옛 = {H.escape(os.path.basename(a.old))} · 새 = {H.escape(os.path.basename(a.new))}"
           f" · 폭 {', '.join(str(w) for w in widths)}px · 밖 요청 막음 {nblock}건</p>" + "".join(rows) + "</body></html>")
    out = os.path.join(a.out, "compare.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"[PASS] 전후 비교 {out} · 섹션 {sections} · 폭 {widths} · 밖 요청 막음 {nblock}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
