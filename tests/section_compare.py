#!/usr/bin/env python3
"""섹션 전후 비교 페이지 — 옛 배포본과 작업본의 같은 섹션을 폭마다 캡처해 나란히 놓은 한 파일(compare.html, 그림 base64 내장)을 쓴다.

사용법: "$PY" tests/section_compare.py <작업본 index.html> <직전 배포본 index.html> --out <폴더> [--sections 11] [--widths 1280,390] [--extra top,basis]

자리(2026-10-10 매출 작업 A·C): **precheck 밖** — 리포트 글·행을 바꾸는 기능의 첫 적용 "보류" 회차(운영 세션)에서 도장 뒤 사용자에게 보이는 재료
(판 C·D·F 의 chart_check compare.html 은 상단 카드·01·06 만 — 다음 액션(판 I 11번 · 판 H 까지 12번)처럼 레이아웃 판을 바꾸지 않는 서술 행 추가는 이 도구로 ·
기본 `--sections 11` = 옛 판 다음 액션(판 I 부터 — 직전 배포본이 판 H 면 12 를 준다)).
- 섹션 = `<!-- Section N: … -->` 주석 바로 뒤 요소(.section). 그 요소만 element screenshot(폭마다 옛·새) — 화면 크기·글꼴은 chart_check 와 같은 조건
  (모바일 폭 ≤ config report_layout.mobile.max_px 는 dpr 2·모바일 UA·터치, 그 밖 dpr 1).
- (2026-10-23 판 I 콘텐츠 지면 빼기) `--sections` 는 **옛(직전 배포본) 구역 번호**이고, 새(작업본) 짝은 같은 제목(`.section-title` 글)의 구역이다 —
  번호가 어긋나도(판 I 첫 적용: 옛 11 핵심 요약 → 새 10) 제목으로 짝짓는다. 새 판에 같은 제목이 없으면(옛 10 "검색 지면 vs 콘텐츠 지면") 옛 그림만 싣고
  "새 판에서 빠짐" 으로 적는다. 제목이 같으면 번호도 같던 판(판 H 까지)은 예전과 같은 결과. 판 I 첫 적용 = `--sections 1,10,11`.
- (2026-10-23 판 J 불필요 항목 빼기) `--extra` = 구역 주석 밖 자리도 같은 꼴로 옛/새 나란히 — `top` = 머리(.masthead) + KPI 줄(.kpi-row) 두 요소를 감싼 영역 ·
  `basis` = 집계 기준 카드(sub-head 글 "집계 기준" 인 .card 하나). 페이지 맨 앞(top) · 맨 끝(basis)에 싣는다. 판 J 첫 적용 = `--sections 1,2,3,4,5,6,7,8,9,10,11 --extra top,basis`.
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
TITLES = """() => {
  const it = document.createNodeIterator(document.body, NodeFilter.SHOW_COMMENT);
  const out = {};
  let c;
  while ((c = it.nextNode())) {
    const m = c.nodeValue.trim().match(/^Section (\\d+):/);
    if (!m) continue;
    let e = c.nextSibling;
    while (e && e.nodeType !== 1) e = e.nextSibling;
    const t = e ? e.querySelector('.section-title') : null;
    out[m[1]] = t ? t.textContent.trim() : '';
  }
  return out;
}"""


EXTRA = """(k) => {
  if (k === 'top') {
    const a = document.querySelector('.masthead'), b = document.querySelector('.kpi-row');
    if (!a || !b) return null;
    const r1 = a.getBoundingClientRect(), r2 = b.getBoundingClientRect();
    const x = Math.min(r1.left, r2.left), y = Math.min(r1.top, r2.top) + window.scrollY;
    return {x: Math.floor(x), y: Math.floor(y), w: Math.ceil(Math.max(r1.right, r2.right) - x), h: Math.ceil(Math.max(r1.bottom, r2.bottom) + window.scrollY - y)};
  }
  if (k === 'basis') {
    const hs = Array.prototype.filter.call(document.querySelectorAll('.sub-head'), function(e){ return e.textContent.trim() === '집계 기준'; });
    if (hs.length !== 1) return null;
    const c = hs[0].closest('.card');
    if (!c) return null;
    c.setAttribute('data-cmp', 'basis');
    const r = c.getBoundingClientRect();
    return {w: Math.round(r.width), h: Math.round(r.height)};
  }
  return null;
}"""
EXTRA_NAME = {"top": "머리 · KPI(구역 주석 밖)", "basis": "집계 기준(구역 주석 밖)"}


def new_page(pw, path, width, max_px):
    mobile = width <= max_px
    browser = pw.chromium.launch()
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
    return browser, page, blocked


def titles(pw, path, max_px):
    """{구역 번호: 제목} — 1280 폭 한 번(제목은 폭과 무관)."""
    browser, page, _ = new_page(pw, path, 1280, max_px)
    try:
        return {int(k): v for k, v in page.evaluate(TITLES).items()}
    finally:
        browser.close()


def capture(pw, path, width, sections, out, tag, max_px, extra=()):
    browser, page, blocked = new_page(pw, path, width, max_px)
    try:
        res = {}
        for k in extra:   # 판 J — 구역 주석 밖 자리(top = 머리·KPI 줄 · basis = 집계 기준 카드)
            box = page.evaluate(EXTRA, k)
            if not box:
                print(f"[FAIL] {tag} {width}px: {EXTRA_NAME[k]} 자리를 못 찾음 — {path}")
                return None, blocked
            png = os.path.join(out, f"{tag}_{width}_{k}.png")
            if k == "top":
                page.screenshot(path=png, full_page=True, clip={"x": box["x"], "y": box["y"], "width": box["w"], "height": box["h"]})
            else:
                page.locator("[data-cmp=basis]").screenshot(path=png)
            res[k] = (png, box)
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
    ap.add_argument("--sections", default="11", help="옛(직전 배포본) 구역 번호 — 새 짝은 같은 제목 구역(번호가 어긋나도 · 없으면 '새 판에서 빠짐')")
    ap.add_argument("--widths", default="1280,390")
    ap.add_argument("--extra", default="", help="구역 주석 밖 자리 — top(머리·KPI 줄) · basis(집계 기준 카드), 쉼표로(판 J)")
    a = ap.parse_args()
    try:
        sections = [int(x) for x in a.sections.split(",")]
        widths = [int(x) for x in a.widths.split(",")]
    except ValueError:
        print("[FAIL] --sections·--widths 는 쉼표로 이은 숫자")
        return 2
    extra = [x for x in a.extra.split(",") if x]
    if [x for x in extra if x not in EXTRA_NAME]:
        print(f"[FAIL] --extra 는 {sorted(EXTRA_NAME)} 중에서")
        return 2
    for p in (a.new, a.old):
        if not os.path.isfile(p):
            print(f"[FAIL] 파일 없음: {p}")
            return 2
    os.makedirs(a.out, exist_ok=True)
    max_px = int(load_config()["report_layout"]["mobile"]["max_px"])
    shots, nblock = {}, 0
    with sync_playwright() as pw:
        t_old, t_new = titles(pw, a.old, max_px), titles(pw, a.new, max_px)
        miss = [n for n in sections if n not in t_old]
        if miss:
            print(f"[FAIL] 옛 판에 Section {miss} 주석이 없음 — {a.old}")
            return 1
        by_title = {}
        for k, v in t_new.items():
            by_title.setdefault(v, []).append(k)
        pairs = []
        for n in sections:
            cand = by_title.get(t_old[n], []) if t_old[n] else ([n] if n in t_new else [])
            if len(cand) > 1:
                print(f"[FAIL] 새 판에 제목 {t_old[n]!r} 구역이 {cand} 둘 이상 — 짝을 정할 수 없음")
                return 1
            pairs.append((n, cand[0] if cand else None))
            print(f"[짝] 옛 {n}번 「{t_old[n]}」 → " + (f"새 {cand[0]}번" if cand else "새 판에서 빠짐(같은 제목 없음 — 옛 그림만)"))
        for w in widths:
            for tag, p, secs in (("old", a.old, [o for o, _ in pairs]), ("new", a.new, [x for _, x in pairs if x is not None])):
                r, blocked = capture(pw, p, w, secs, a.out, tag, max_px, extra)
                nblock += len(blocked)
                if r is None:
                    return 1
                shots[(tag, w)] = r
    rows = []

    def extra_rows(k):
        rows.append(f"<h2>{EXTRA_NAME[k]}</h2>")
        for w in widths:
            (po, bo), (pn, bn) = shots[("old", w)][k], shots[("new", w)][k]
            rows.append(f"<h3>{w}px — 높이 {bo['h']} → {bn['h']}px</h3><div class='pair'>"
                        f"<figure><figcaption>옛(직전 배포본)</figcaption><img src='data:image/png;base64,{img(po)}' style='width:{min(w, 640)}px'></figure>"
                        f"<figure><figcaption>새(작업본)</figcaption><img src='data:image/png;base64,{img(pn)}' style='width:{min(w, 640)}px'></figure></div>")
            print(f"[캡처] {EXTRA_NAME[k]} {w}px 옛 {bo['w']}×{bo['h']} · 새 {bn['w']}×{bn['h']}")
    if "top" in extra:
        extra_rows("top")
    for o, n in pairs:
        head = f"옛 {o}번 「{H.escape(t_old[o])}」" + (f" → 새 {n}번" if n is not None and n != o else "" if n is not None else " — 새 판에서 빠짐")
        rows.append(f"<h2>{head}</h2>")
        for w in widths:
            po, bo = shots[("old", w)][o]
            if n is None:
                rows.append(f"<h3>{w}px — 옛 높이 {bo['h']}px · 새 판 없음</h3><div class='pair'>"
                            f"<figure><figcaption>옛(직전 배포본) {o}번</figcaption><img src='data:image/png;base64,{img(po)}' style='width:{min(w, 640)}px'></figure>"
                            "<figure><figcaption>새(작업본)</figcaption><p>이 구역은 새 판에서 빠짐</p></figure></div>")
                print(f"[캡처] 옛 {o}번 {w}px {bo['w']}×{bo['h']} · 새 판 없음")
                continue
            pn, bn = shots[("new", w)][n]
            rows.append(f"<h3>{w}px — 높이 {bo['h']} → {bn['h']}px</h3><div class='pair'>"
                        f"<figure><figcaption>옛(직전 배포본) {o}번</figcaption><img src='data:image/png;base64,{img(po)}' style='width:{min(w, 640)}px'></figure>"
                        f"<figure><figcaption>새(작업본) {n}번</figcaption><img src='data:image/png;base64,{img(pn)}' style='width:{min(w, 640)}px'></figure></div>")
            print(f"[캡처] 옛 {o}번 → 새 {n}번 {w}px 옛 {bo['w']}×{bo['h']} · 새 {bn['w']}×{bn['h']}")
    if "basis" in extra:
        extra_rows("basis")
    label = ",".join(str(o) if n == o else f"{o}→{n if n is not None else '없음'}" for o, n in pairs) + ("" if not extra else " + " + "·".join(extra))
    doc = ("<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>전후 비교 — {label}번</title><style>body{{font-family:sans-serif;margin:16px;background:#faf8f3;color:#1c2b2a}}"
           ".pair{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}figure{margin:0}figcaption{font-weight:700;margin:4px 0}"
           "img{border:1px solid #ccc;background:#fff;max-width:100%}</style></head><body>"
           f"<h1>전후 비교 — {label}번 섹션(짝 = 같은 제목)</h1><p>옛 = {H.escape(os.path.basename(a.old))} · 새 = {H.escape(os.path.basename(a.new))}"
           f" · 폭 {', '.join(str(w) for w in widths)}px · 밖 요청 막음 {nblock}건</p>" + "".join(rows) + "</body></html>")
    out = os.path.join(a.out, "compare.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"[PASS] 전후 비교 {out} · 짝 {pairs} · 폭 {widths} · 밖 요청 막음 {nblock}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
