#!/usr/bin/env python3
"""01·06 라이브 차트 확인 — 레이아웃 판 r2026-10-C(01·06 모바일 가로 막대)의 "보이는 숫자 누락 0" 을 진짜 Chart.js 로 잰다.

사용법: "$PY" tests/chart_check.py <index.html> <compute.json> [--base <직전 배포본 html>] [--out <캡처 폴더>] [--widths 390,1280]

자리(사용자 결정 2026-10-06 — 8): **precheck 밖** — 구현·검증 회차 리허설 · 첫 적용 "보류" 회차(운영 세션) · 정기점검에서 돌린다.
playwright chromium 새 임시 프로필(수집 프로필 `~/saero-fetch` 아님) · 밖 요청은 cdnjs Chart.js·datalabels 2건만 보내고(allow-list)
그 밖은 막고 센다 — 막힌 요청이 1건이라도 있으면 URL 과 함께 FAIL(새 CDN·파일 0 원칙). file:// 는 그대로.
기다림: networkidle + 1.8초(Chart.js 애니메이션 1초). 기준값(분기 경계·인쇄 높이 상한·행 높이)은 config report_layout.mobile 에서 읽는다.

판정(하나라도 어긋나면 exit 1 · Chart.js 가 안 읽히면 `[FAIL] chart_check: Chart.js CDN 미로드 — 라이브 차트 확인 불가` exit 2 = 통과 아님):
- 모바일 폭(≤ config mobile.max_px, 기본 390 — dpr 2·모바일 UA): 01 indexAxis 'y' · tick = compute nlabels · 보이는 datalabels = 2n/2n ·
  캔버스 밖 0 · 글자 겹침 0(padding 을 뺀 글자 상자 교차) · padding 상자 겹침 ≤ --base 를 같은 폭에서 같은 도구로 잰 값(--base 없으면 1) ·
  제목 띠 침범 0(라벨 상자 y < chartArea.top) · 컨테이너 높이 = n×row_px+pad_px · 스크롤 박스 scrollWidth = clientWidth(뱃지 없음) · 맨 위 tick = 최신 날짜 /
  06 같은 꼴(라벨 n/n · padding·글자 겹침 0) / 문서 scrollWidth = 폭 / 문서의 캔버스 전부(8) Chart.getChart 있음 / pageerror 0.
- PC 폭(기본 1280): 01·06 indexAxis 'x' · tick n · 보이는 datalabels(01 2n · 06 0) · chartArea·첫 화면 일수·섹션 1·6 높이·뱃지 = --base 측정값 ·
  S(스크롤 시작 최신 쪽): 01·06 박스 scrollLeft = scrollWidth − clientWidth · 래퍼 .at-end 있음·.at-start 없음 · 첫 화면 끝 날짜 = 최신.
- 회전(모바일 폭 → 가로 844 → 모바일): 844 에서 01 'x'·tick n·scrollWidth = compute minwidth·뱃지·scrollLeft 끝 · 06 'x'·tick n /
  복귀에서 'y'·높이 n×row+pad·라벨 2n(로드와 같음) · .scroll-fade 래퍼가 남아 있으면 at-start·at-end 둘 다(페이드 0) · 뱃지 0 · pageerror 0.
- 인쇄 = page.pdf 실물(A4 · 여백 0.4in): 모바일 컨텍스트에서 `__ev` 훅(add_init_script — DOMContentLoaded 에 걸어 페이지 리스너 뒤에 돈다)으로
  beforeprint 때 01·06 컨테이너 높이 ≤ print_max_height_px · indexAxis 'y' 유지 · afterprint 뒤 높이·indexAxis 복구, pypdf 로 01·06 이 PDF 에 한 쪽 안·누락 0 —
  둘 중 하나: **벡터**(beforeprint 에 다시 그린 캔버스는 그리기 명령 그대로 실려 글자가 PDF 텍스트 — layout 추출 한 줄이 '날짜 노출 비용원'·'날짜 순위' 인 행이
  한 쪽에만 n 개 전부, 위에서 아래로 최신 → 오래된) 또는 **비트맵**(beforeprint 때 캔버스 비트맵 크기와 같은 이미지가 정확히 한 번·쪽 안·클립 없이·그려진 픽셀 > 0) /
  PC 컨텍스트 PDF 는 --base 와 같은 이미지 구성(큰 이미지 크기·배치 수·보이는 비율 같음 — 폭 3,280 캔버스가 종이 폭에 잘린 일수 그대로. 어느 날짜 구간이 찍히는지는
  대조하지 않는다 — 판 C 는 화면 스크롤 자리(S, 최신 쪽)를 따른다).
- --out 이 있으면 모바일·PC 폭의 섹션 1·6 PNG(로드 상태 — 전후 비교 재료)와 PDF 를 저장한다.

검사로 못 지키는 것 — **사용자 시크릿 창(실기기) 몫**: 실기기 폰트 폭(iOS Safari·삼성 인터넷 — 라벨 겹침이 달라질 수 있음) · 회전 체감·첫 페인트 깜빡임 ·
iOS 공유→PDF·실제 인쇄 대화상자(beforeprint 가 오는지) · PWA 설치본의 service-worker 캐시(network-first — 온라인이면 첫 열기에 새 판).
"""
import argparse
import json
import os
import shutil
import sys
import tempfile

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
from reportlib import load_config  # noqa: E402

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — 다른 시험과 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

CDN_ALLOW = (  # 배포본 head 의 외부 스크립트 둘 — 이 밖의 밖 요청은 막고 센다
    "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js",
)
SETTLE = 1800
PDF_MARGIN = {"top": "0.4in", "right": "0.4in", "bottom": "0.4in", "left": "0.4in"}

# 차트 하나 — tick·datalabels(chartjs-plugin-datalabels 2.2.0 의 chart.$datalabels._labels: $layout._visible · _box._rect · _model.padding)·상자·스크롤 박스
INFO = """(id) => {
  const c = Chart.getChart(id); if (!c) return {err: 'Chart.getChart(' + id + ') 없음'};
  const canvas = c.canvas, cont = canvas.parentElement, box = canvas.closest('.scroll-x');
  const horiz = c.options.indexAxis === 'y';
  const cat = horiz ? c.scales.y : c.scales.x;
  const n = c.data.labels.length;
  const r1 = (v) => Math.round(v * 10) / 10;
  let topLabel = null;
  if (horiz && cat.ticks.length) { let best = null; cat.ticks.forEach((t, i) => { const px = cat.getPixelForTick(i); if (best === null || px < best.px) best = {px, v: t.value}; }); topLabel = c.data.labels[best.v]; }
  let first = null;
  if (!horiz && box) {
    const a = box.scrollLeft, b = a + box.clientWidth, idx = [];
    for (let i = 0; i < n; i++) { const p = cat.getPixelForValue(i); if (p >= a && p <= b) idx.push(i); }
    first = {days: idx.length, from: c.data.labels[idx[0]], to: c.data.labels[idx[idx.length - 1]]};
  }
  const L = (c.$datalabels && c.$datalabels._labels) || [];
  const V = L.filter(l => l.$layout && l.$layout._visible);
  const B = V.map(l => { const r = l.$layout._box._rect; const p = (l._model && l._model.padding) || {top: 0, right: 0, bottom: 0, left: 0}; const cx = l.$context;
    return {x: r.x, y: r.y, w: r.w, h: r.h, gx: r.x + p.left, gy: r.y + p.top, gw: r.w - p.left - p.right, gh: r.h - p.top - p.bottom,
            v: cx.dataset.data[cx.dataIndex], d: c.data.labels[cx.dataIndex], ds: cx.datasetIndex}; });
  const inter = (a, b, k) => { const ox = Math.min(a[k + 'x'] + a[k + 'w'], b[k + 'x'] + b[k + 'w']) - Math.max(a[k + 'x'], b[k + 'x']);
                               const oy = Math.min(a[k + 'y'] + a[k + 'h'], b[k + 'y'] + b[k + 'h']) - Math.max(a[k + 'y'], b[k + 'y']); return ox > 0 && oy > 0; };
  const pad = [], glyph = [];
  for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) {
    const a = B[i], b = B[j], tag = a.d + ' ' + a.v + ' × ' + b.d + ' ' + b.v;
    if (inter(a, b, '')) pad.push(tag); if (inter(a, b, 'g')) glyph.push(tag);
  }
  const ca = c.chartArea;
  const wrap = box && box.parentNode && box.parentNode.classList && box.parentNode.classList.contains('scroll-fade') ? box.parentNode : null;
  const prev = (wrap || box) ? (wrap || box).previousElementSibling : null;
  return {indexAxis: c.options.indexAxis || 'x', n, ticks: cat.ticks.length, topLabel, first,
          dl: V.length + '/' + L.length, dlVisible: V.length, padOverlap: pad.length, padPairs: pad.slice(0, 4), glyphOverlap: glyph.length, glyphPairs: glyph.slice(0, 4),
          outside: B.filter(b => b.x < 0 || b.y < 0 || b.x + b.w > c.width || b.y + b.h > c.height).length,
          titleInvade: B.filter(b => b.y < ca.top).length,
          chartArea: [r1(ca.left), r1(ca.top), r1(ca.right), r1(ca.bottom)], w: c.width, h: c.height, bitmap: [canvas.width, canvas.height],
          contH: r1(cont.getBoundingClientRect().height), contMinW: cont.style.minWidth,
          box: box ? {cw: box.clientWidth, sw: box.scrollWidth, sl: box.scrollLeft} : null,
          hint: !!(prev && prev.classList && prev.classList.contains('scroll-hint')), fade: !!wrap,
          atEnd: !!(wrap && wrap.classList.contains('at-end')), atStart: !!(wrap && wrap.classList.contains('at-start'))};
}"""

PAGE = """() => {
  const secs = {};
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_COMMENT); let cm;
  while ((cm = tw.nextNode())) { const m = cm.nodeValue.trim().match(/^Section (\\d+):/); if (!m) continue;
    let e = cm.nextSibling; while (e && e.nodeType !== 1) e = e.nextSibling; if (!e) continue;
    const r = e.getBoundingClientRect(); secs[m[1]] = {x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: Math.round(r.height)}; }
  const cv = [...document.querySelectorAll('canvas')];
  return {canvases: cv.length, charts: cv.filter(c => Chart.getChart(c)).length, missing: cv.filter(c => !Chart.getChart(c)).map(c => c.id),
          docSW: document.documentElement.scrollWidth, docSH: document.documentElement.scrollHeight, secs};
}"""

# 인쇄 훅 — DOMContentLoaded 에 걸어 페이지의 beforeprint/afterprint 리스너(차트 스크립트 끝 분기 도우미 · 안내 스크립트)보다 뒤에 돈다
EV_HOOK = """window.__ev = {beforeprint: [], afterprint: [], mq: []};
document.addEventListener('DOMContentLoaded', function(){
  function snap(k){ var o = {k: k, docW: document.documentElement.clientWidth};
    ['dailyChart', 'rankChart'].forEach(function(id){ var cv = document.getElementById(id); var c = (window.Chart && cv) ? Chart.getChart(cv) : null; var b = cv ? cv.parentElement : null;
      o[id] = {idx: c ? (c.options.indexAxis || 'x') : null, h: b ? Math.round(b.getBoundingClientRect().height * 10) / 10 : null, styleH: b ? b.style.height : null,
               bitmap: cv ? [cv.width, cv.height] : null}; });
    return o; }
  window.addEventListener('beforeprint', function(){ window.__ev.beforeprint.push(snap('beforeprint')); });
  window.addEventListener('afterprint', function(){ window.__ev.afterprint.push(snap('afterprint')); });
  if (window.matchMedia) { var mq = window.matchMedia('(max-width: @@MAX@@px)');
    var f = function(e){ var o = snap('mq'); o.matches = e.matches; window.__ev.mq.push(o); };
    if (mq.addEventListener) mq.addEventListener('change', f); else mq.addListener(f); }
});"""


class Run:
    def __init__(self):
        self.n_pass, self.fails, self.blocked, self.allowed, self.errors = 0, [], [], set(), []

    def check(self, name, ok, detail):
        print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")
        if ok:
            self.n_pass += 1
        else:
            self.fails.append(name)

    def route(self, route):
        u = route.request.url
        if u.startswith(("file:", "data:", "blob:", "about:")):
            route.continue_()
        elif u in CDN_ALLOW:
            self.allowed.add(u)
            route.continue_()
        else:
            self.blocked.append(u)
            route.abort()


def url_of(path):
    return "file:///" + os.path.abspath(path).replace("\\", "/")


def new_ctx(b, run, w, h, mobile, hook=None):
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile)
    ctx.route("**/*", run.route)
    if hook:
        ctx.add_init_script(hook)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    return ctx, pg, errs


def load(pg, path):
    pg.goto(url_of(path), wait_until="networkidle")
    pg.wait_for_timeout(SETTLE)
    return pg.evaluate("typeof Chart !== 'undefined' && typeof ChartDataLabels !== 'undefined'")


def measure(pg):
    return {"01": pg.evaluate(INFO, "dailyChart"), "06": pg.evaluate(INFO, "rankChart"), "page": pg.evaluate(PAGE)}


def shot(pg, page_info, out, tag):
    for s in ("1", "6"):
        r = page_info["secs"].get(s)
        if r and out:
            pg.screenshot(path=os.path.join(out, f"{tag}_sec{s}.png"), full_page=True,
                          clip={"x": max(0, r["x"]), "y": max(0, r["y"]), "width": r["w"], "height": r["h"]})


# ── PDF(pypdf): 큰 이미지가 어느 쪽 어디에 얼마나 보이게(클립) 그려졌는지 ──
def _mul(a, b):
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3], a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


def _pt(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def _box(m, x0, y0, x1, y1):
    ps = [_pt(m, x0, y0), _pt(m, x1, y0), _pt(m, x0, y1), _pt(m, x1, y1)]
    return (min(p[0] for p in ps), min(p[1] for p in ps), max(p[0] for p in ps), max(p[1] for p in ps))


def _isect(a, b):
    if a is None:
        return b
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def pdf_images(path, min_h=100):
    """쪽마다 높이 min_h px 이상 이미지 XObject 의 배치: (쪽, 이미지 px 크기, 그려진 상자 pt, 보이는 비율 가로·세로(클립·쪽 경계 교집합), 그려진 픽셀)."""
    from pypdf import PdfReader
    from pypdf.generic import ContentStream
    r = PdfReader(path)
    out, drawn_cache = [], {}

    def drawn_px(o):
        key = id(o)
        if key not in drawn_cache:
            try:
                im = o.decode_as_image()
                im = im.convert("RGBA")
                drawn_cache[key] = sum(1 for p in (im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()) if p[3] > 0 and not (p[0] > 245 and p[1] > 245 and p[2] > 245))
            except Exception as e:  # pragma: no cover
                drawn_cache[key] = f"디코드 실패 {e}"
        return drawn_cache[key]

    def walk(pno, res, ops, ctm0, page_box, clip0):
        xo = (res.get("/XObject") or {}) if res else {}
        ctm, clip, stack, rects = ctm0, clip0, [], []
        for operands, op in ops:
            if op == b"q":
                stack.append((ctm, clip))
            elif op == b"Q":
                if stack:
                    ctm, clip = stack.pop()
            elif op == b"cm":
                ctm = _mul([float(x) for x in operands], ctm)
            elif op == b"re":
                x, y, w, h = [float(v) for v in operands]
                rects.append(_box(ctm, x, y, x + w, y + h))
            elif op in (b"n", b"f", b"F", b"S", b"B", b"f*", b"B*", b"b", b"b*", b"s"):
                rects = []
            elif op in (b"W", b"W*"):
                for rc in rects:
                    clip = _isect(clip, rc)
            elif op == b"Do":
                o = xo[operands[0]].get_object() if operands[0] in xo else None
                if o is None:
                    continue
                if o.get("/Subtype") == "/Image":
                    W, H = int(o["/Width"]), int(o["/Height"])
                    if H < min_h:
                        continue
                    ib = _box(ctm, 0, 0, 1, 1)
                    vis = _isect(_isect(clip, page_box), ib)
                    vw = max(0.0, vis[2] - vis[0]) / max(1e-9, ib[2] - ib[0])
                    vh = max(0.0, vis[3] - vis[1]) / max(1e-9, ib[3] - ib[1])
                    out.append({"page": pno, "size": [W, H], "pt": [round(v, 1) for v in ib], "vis_w": round(vw, 4), "vis_h": round(vh, 4),
                                "drawn": drawn_px(o)})
                elif o.get("/Subtype") == "/Form":
                    m = o.get("/Matrix")
                    walk(pno, o.get("/Resources"), ContentStream(o, r).operations, _mul([float(v) for v in m], ctm) if m else ctm, page_box, clip)

    for i, pg in enumerate(r.pages):
        mb = pg.mediabox
        page_box = (float(mb.left), float(mb.bottom), float(mb.right), float(mb.top))
        walk(i + 1, pg.get("/Resources"), ContentStream(pg.get_contents(), r).operations, [1, 0, 0, 1, 0, 0], page_box, None)
    return len(r.pages), out


def pdf_row_pages(path, rows):
    """캔버스가 벡터로 실린 PDF(Chromium 은 beforeprint 에 다시 그린 캔버스를 그리기 명령 그대로 — 글자가 PDF 텍스트로 남는다)에서
    차트 한 행(날짜 tick + 그 행의 datalabels)이 layout 추출 한 줄의 토큰과 정확히 같은 줄을 쪽마다 센다. → {쪽: [(줄 번호, 행 번호)]}
    (HTML 표의 숫자는 tabular 글꼴이라 다른 글자로 뽑혀 섞이지 않는다 — 2026-10-06 실측)"""
    from pypdf import PdfReader
    want = {tuple(sorted(t)): i for i, t in enumerate(rows)}
    hits = {}
    for p, pg in enumerate(PdfReader(path).pages):
        for li, line in enumerate(pg.extract_text(extraction_mode="layout").split("\n")):
            k = tuple(sorted(line.split()))
            if k in want:
                hits.setdefault(p + 1, []).append((li, want[k]))
    return hits


def print_rows_ok(hits, n):
    """한 쪽에만, n 행 전부 한 번씩, 위에서 아래로 최신 → 오래된(화면과 같은 순서)."""
    if len(hits) != 1:
        return False
    (_, h), = hits.items()
    order = [i for _, i in sorted(h)]
    return sorted(order) == list(range(n)) and order == list(range(n))[::-1]


def pdf_signature(imgs):
    """이미지 구성 비교용 — (크기, 배치 수, 보이는 비율) 정렬 목록."""
    by = {}
    for im in imgs:
        by.setdefault(tuple(im["size"]), []).append((im["vis_w"], im["vis_h"]))
    return sorted((k[0], k[1], len(v), tuple(sorted((round(a, 3), round(b, 3)) for a, b in v))) for k, v in by.items())


def main():
    ap = argparse.ArgumentParser(description="01·06 라이브 차트 확인(레이아웃 판 r2026-10-C — precheck 밖)")
    ap.add_argument("html")
    ap.add_argument("compute")
    ap.add_argument("--base", help="직전 배포본 html — PC 폭 측정값·padding 겹침 기준·PC 인쇄 이미지 구성의 기준")
    ap.add_argument("--out", help="캡처(섹션 1·6 PNG)·PDF 저장 폴더")
    ap.add_argument("--widths", default="390,1280")
    a = ap.parse_args()
    cfg = load_config()
    mob = cfg["report_layout"]["mobile"]
    maxpx, printmax = int(mob["max_px"]), int(mob["print_max_height_px"])
    row, padpx = {k: int(v) for k, v in mob["row_px"].items()}, {k: int(v) for k, v in mob["pad_px"].items()}
    with open(a.compute, encoding="utf-8") as f:
        R = json.load(f)
    n, minwidth, labels = int(R["nlabels"]), int(R["minwidth"]), R["01"]["labels"]
    widths = [int(x) for x in a.widths.split(",") if x.strip()]
    out = a.out
    if out:
        os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="saero-chart-")
    pdfdir = out or tmp
    run = Run()
    hook = EV_HOOK.replace("@@MAX@@", str(maxpx))
    print(f"chart_check: {os.path.abspath(a.html)} · compute nlabels {n} · minwidth {minwidth} · config mobile max_px {maxpx} · print_max_height_px {printmax} · "
          f"row {row} · pad {padpx} · 기준 {os.path.abspath(a.base) if a.base else '없음'}")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()

            def base_measure(w, h, mobile):
                if not a.base:
                    return None
                ctx, pg, errs = new_ctx(b, run, w, h, mobile)
                try:
                    if not load(pg, a.base):
                        return None
                    return measure(pg)
                finally:
                    ctx.close()

            for w in widths:
                mobile = w <= maxpx
                h = 844 if mobile else 900
                ctx, pg, errs = new_ctx(b, run, w, h, mobile)
                if not load(pg, a.html):
                    ctx.close()
                    b.close()
                    print("[FAIL] chart_check: Chart.js CDN 미로드 — 라이브 차트 확인 불가")
                    return 2
                m = measure(pg)
                shot(pg, m["page"], out, f"{w}")
                m_start = None
                if not mobile:  # PC 모양 대조는 기준과 같은 스크롤 자리(맨 왼쪽)에서 — S 는 로드 상태(m)로 따로 본다
                    pg.evaluate("() => ['dailyChart', 'rankChart'].forEach(id => { const b = document.getElementById(id).closest('.scroll-x'); "
                                "if (b) { b.scrollLeft = 0; b.dispatchEvent(new Event('scroll')); } })")
                    pg.wait_for_timeout(300)
                    m_start = measure(pg)
                ctx.close()
                B = base_measure(w, h, mobile)
                d, r, pgi = m["01"], m["06"], m["page"]
                for k, v in (("01", d), ("06", r)):
                    if "err" in v:
                        run.check(f"{w} {k}", False, v["err"])
                if "err" in d or "err" in r:
                    continue
                run.check(f"{w} 캔버스·pageerror", pgi["charts"] == pgi["canvases"] == 8 and not errs,
                          f"캔버스 {pgi['canvases']} · Chart.getChart {pgi['charts']}(없음 {pgi['missing']}) · pageerror {len(errs)}{(' ' + errs[0][:120]) if errs else ''}")
                run.check(f"{w} 문서 가로 넘침", pgi["docSW"] == w, f"scrollWidth {pgi['docSW']} / 폭 {w}")
                if mobile:
                    base_pad = B["01"]["padOverlap"] if B and "err" not in B["01"] else 1
                    want_h = n * row["01"] + padpx["01"]
                    ok = (d["indexAxis"] == "y" and d["ticks"] == n and d["dl"] == f"{2 * n}/{2 * n}" and d["outside"] == 0 and d["glyphOverlap"] == 0
                          and d["padOverlap"] <= base_pad and d["titleInvade"] == 0 and abs(d["contH"] - want_h) < 0.6 and d["box"] and d["box"]["sw"] == d["box"]["cw"]
                          and not d["hint"] and d["topLabel"] == labels[-1])
                    run.check(f"{w} 01 모바일 가로 막대", ok,
                              f"indexAxis {d['indexAxis']} · ticks {d['ticks']}/{n} · 라벨 {d['dl']} · 밖 {d['outside']} · 글자 겹침 {d['glyphOverlap']}{d['glyphPairs'] or ''} · "
                              f"padding 겹침 {d['padOverlap']}{d['padPairs'] or ''}(기준 {base_pad}{'' if B else ' — --base 없음, 기본값'}) · 제목 띠 {d['titleInvade']} · "
                              f"높이 {d['contH']} = {n}×{row['01']}+{padpx['01']}({want_h}) · 박스 {d['box']} · 뱃지 {d['hint']} · 맨 위 {d['topLabel']} · 캔버스 {d['w']}×{d['h']}")
                    want_h6 = n * row["06"] + padpx["06"]
                    ok = (r["indexAxis"] == "y" and r["ticks"] == n and r["dl"] == f"{n}/{n}" and r["outside"] == 0 and r["glyphOverlap"] == 0 and r["padOverlap"] == 0
                          and r["titleInvade"] == 0 and abs(r["contH"] - want_h6) < 0.6 and r["box"] and r["box"]["sw"] == r["box"]["cw"] and not r["hint"]
                          and r["topLabel"] == labels[-1])
                    run.check(f"{w} 06 모바일 가로", ok,
                              f"indexAxis {r['indexAxis']} · ticks {r['ticks']}/{n} · 라벨 {r['dl']} · 밖 {r['outside']} · 글자 겹침 {r['glyphOverlap']} · padding 겹침 {r['padOverlap']}{r['padPairs'] or ''} · "
                              f"제목 띠 {r['titleInvade']} · 높이 {r['contH']} = {n}×{row['06']}+{padpx['06']}({want_h6}) · 박스 {r['box']} · 뱃지 {r['hint']} · 맨 위 {r['topLabel']} · 캔버스 {r['w']}×{r['h']}")
                    print(f"       {w} 섹션 높이 1 {pgi['secs'].get('1', {}).get('h')} · 6 {pgi['secs'].get('6', {}).get('h')} · 문서 높이 {pgi['docSH']}"
                          + (f"(기준 1 {B['page']['secs'].get('1', {}).get('h')} · 6 {B['page']['secs'].get('6', {}).get('h')} · 문서 {B['page']['docSH']})" if B else ""))
                else:
                    for k, v, want_dl in (("01", d, 2 * n), ("06", r, 0)):
                        bx = v["box"] or {}
                        end_ok = bool(bx) and abs(bx["sl"] - (bx["sw"] - bx["cw"])) <= 1
                        ok = (v["indexAxis"] == "x" and v["ticks"] == n and v["dlVisible"] == want_dl and end_ok and v["atEnd"] and not v["atStart"]
                              and v["first"] and v["first"]["to"] == labels[-1] and v["hint"])
                        run.check(f"{w} {k} S 최신 쪽 시작", ok,
                                  f"indexAxis {v['indexAxis']} · ticks {v['ticks']}/{n} · 라벨 {v['dl']} · scrollLeft {bx.get('sl')} = {bx.get('sw')}−{bx.get('cw')} · "
                                  f"at-end {v['atEnd']} · at-start {v['atStart']} · 첫 화면 {v['first']} · 뱃지 {v['hint']}")
                        v0 = m_start[k]
                        ok = v0["atStart"] and not v0["atEnd"] and v0["chartArea"] == v["chartArea"]
                        det = (f"맨 왼쪽에서 at-start {v0['atStart']} · at-end {v0['atEnd']} · chartArea {v0['chartArea']} · 첫 화면 {v0['first']} · 라벨 {v0['dl']} · "
                               f"뱃지 {v0['hint']} · 캔버스 {v0['w']}×{v0['h']}")
                        if B and "err" not in B[k]:
                            bv = B[k]
                            ok = ok and (v0["chartArea"] == bv["chartArea"] and v0["first"] == bv["first"] and v0["hint"] == bv["hint"]
                                         and v0["dl"] == bv["dl"] and [v0["w"], v0["h"]] == [bv["w"], bv["h"]] and v0["ticks"] == bv["ticks"])
                            det += f" | 기준 chartArea {bv['chartArea']} · 첫 화면 {bv['first']} · 라벨 {bv['dl']} · 뱃지 {bv['hint']} · 캔버스 {bv['w']}×{bv['h']}"
                        else:
                            det += " | --base 없음 — 기준 대조 생략"
                        run.check(f"{w} {k} PC 모양 = 기준", ok, det)
                    if B:
                        s_new = [pgi["secs"].get(s, {}).get("h") for s in ("1", "6")]
                        s_old = [B["page"]["secs"].get(s, {}).get("h") for s in ("1", "6")]
                        run.check(f"{w} 섹션 1·6 높이 = 기준", s_new == s_old, f"새 {s_new} · 기준 {s_old}")

            # ── 회전: 모바일 폭 → 가로(844) → 모바일 ──
            mws = [w for w in widths if w <= maxpx]
            if mws:
                w = mws[0]
                ctx, pg, errs = new_ctx(b, run, w, 844, True)
                load(pg, a.html)
                m0 = measure(pg)
                pg.set_viewport_size({"width": 844, "height": w})
                pg.wait_for_timeout(700)
                m1 = measure(pg)
                pg.set_viewport_size({"width": w, "height": 844})
                pg.wait_for_timeout(700)
                m2 = measure(pg)
                ctx.close()
                d1, r1_ = m1["01"], m1["06"]
                bx = d1.get("box") or {}
                ok = (d1.get("indexAxis") == "x" and d1.get("ticks") == n and bx.get("sw") == minwidth and d1.get("hint") and abs(bx.get("sl", -9) - (bx.get("sw", 0) - bx.get("cw", 0))) <= 1
                      and d1.get("atEnd") and not d1.get("atStart") and r1_.get("indexAxis") == "x" and r1_.get("ticks") == n and r1_.get("hint"))
                run.check(f"회전 {w}→844 PC 분기", ok,
                          f"01 indexAxis {d1.get('indexAxis')} · ticks {d1.get('ticks')} · 박스 {bx}(scrollWidth = minwidth {minwidth}) · 뱃지 {d1.get('hint')} · at-end {d1.get('atEnd')} · at-start {d1.get('atStart')} · "
                          f"06 indexAxis {r1_.get('indexAxis')} · ticks {r1_.get('ticks')} · 뱃지 {r1_.get('hint')} · 박스 {r1_.get('box')}")
                keys = ("indexAxis", "ticks", "dl", "glyphOverlap", "padOverlap", "outside", "contH", "contMinW", "topLabel", "w", "h")
                same = all(m2[k][x] == m0[k][x] for k in ("01", "06") for x in keys)
                fade_ok = all((not m2[k]["fade"]) or (m2[k]["atEnd"] and m2[k]["atStart"]) for k in ("01", "06"))
                ok = same and fade_ok and not m2["01"]["hint"] and not m2["06"]["hint"] and m2["01"]["indexAxis"] == "y" and not errs
                run.check(f"회전 844→{w} 복원(로드와 같음)", ok,
                          f"01 {[m2['01'][x] for x in keys]} · 로드 {[m0['01'][x] for x in keys]} · 06 같음 {all(m2['06'][x] == m0['06'][x] for x in keys)} · "
                          f"래퍼 01 {m2['01']['fade']}(at-end {m2['01']['atEnd']} · at-start {m2['01']['atStart']}) · 06 {m2['06']['fade']}(at-end {m2['06']['atEnd']} · at-start {m2['06']['atStart']}) · "
                          f"뱃지 {m2['01']['hint']}/{m2['06']['hint']} · pageerror {len(errs)}")

            # ── 인쇄 = page.pdf 실물 ──
            for w in widths:
                mobile = w <= maxpx
                h = 844 if mobile else 900
                res = {}
                for tag, path in (("new", a.html), ("base", a.base)):
                    if tag == "base" and (mobile or not a.base):
                        continue
                    ctx, pg, errs = new_ctx(b, run, w, h, mobile, hook)
                    load(pg, path)
                    m0 = measure(pg)
                    pdf = os.path.join(pdfdir, f"{'' if tag == 'new' else 'base_'}{w}.pdf")
                    pg.pdf(path=pdf, format="A4", margin=PDF_MARGIN, print_background=True)
                    pg.wait_for_timeout(600)
                    ev = pg.evaluate("window.__ev")
                    m1 = measure(pg)
                    ctx.close()
                    pages, imgs = pdf_images(pdf)
                    res[tag] = {"m0": m0, "m1": m1, "ev": ev, "pages": pages, "imgs": imgs, "errs": errs, "pdf": pdf}
                N = res["new"]
                ev = N["ev"]
                if mobile:
                    bp = ev["beforeprint"][0] if ev["beforeprint"] else None
                    apv = ev["afterprint"][0] if ev["afterprint"] else None
                    ok = bool(bp and apv)
                    det = f"beforeprint {len(ev['beforeprint'])} · afterprint {len(ev['afterprint'])} · 인쇄 중 mq change {[(x['matches'], x['docW']) for x in ev['mq']]}"
                    for k, cid in (("01", "dailyChart"), ("06", "rankChart")):
                        if not ok:
                            break
                        want_h = n * row[k] + padpx[k]
                        b0, a0 = bp[cid], apv[cid]
                        ok = (b0["idx"] == "y" and b0["h"] <= printmax + 0.5 and abs(b0["h"] - min(want_h, printmax)) < 0.6 and a0["idx"] == "y" and abs(a0["h"] - want_h) < 0.6
                              and N["m1"][k]["indexAxis"] == "y" and abs(N["m1"][k]["contH"] - want_h) < 0.6 and N["m1"][k]["dl"] == N["m0"][k]["dl"])
                        det += (f" | {k}: beforeprint {b0['idx']} 높이 {b0['h']}(≤ {printmax}) 비트맵 {b0['bitmap']} · afterprint {a0['idx']} 높이 {a0['h']}(= {want_h}) · "
                                f"뒤 상태 {N['m1'][k]['indexAxis']} {N['m1'][k]['contH']} 라벨 {N['m1'][k]['dl']}")
                    run.check(f"인쇄 {w} 이벤트(F — 높이 캡·복구)", ok and not N["errs"], det + f" · pageerror {len(N['errs'])}")
                    rows = {"01": [(labels[i], f"{R['01']['노출'][i]:,}", f"{R['01']['총비용'][i]:,}원") for i in range(n)],
                            "06": [(labels[i], f"{R['06']['rankChart'][i]:.2f}") for i in range(n)]}
                    for k, cid in (("01", "dailyChart"), ("06", "rankChart")):
                        # 벡터(글자 = PDF 텍스트): 한 쪽에 n 행 전부·최신 위 / 비트맵: beforeprint 캔버스 비트맵과 같은 크기 이미지가 한 번·클립 없이·그려진 픽셀 > 0
                        vec = pdf_row_pages(N["pdf"], rows[k])
                        size = bp[cid]["bitmap"] if bp else None
                        imgs = [im for im in N["imgs"] if size and im["size"] == size]
                        vec_ok = print_rows_ok(vec, n)
                        img_ok = (len(imgs) == 1 and imgs[0]["vis_w"] >= 0.999 and imgs[0]["vis_h"] >= 0.999 and isinstance(imgs[0]["drawn"], int) and imgs[0]["drawn"] > 0)
                        ok = (vec_ok or img_ok) and not (vec and imgs)
                        run.check(f"인쇄 {w} {k} PDF 한 쪽 안·누락 0", ok,
                                  f"PDF {N['pages']}쪽 · 벡터 행 {({p: len(v) for p, v in vec.items()}) or 0}/{n}{'(최신 위 순서)' if vec_ok else ''} · "
                                  f"비트맵 {size} 이미지 {len(imgs)}"
                                  + (f"({imgs[0]['page']}쪽 · 보이는 비율 {imgs[0]['vis_w']}×{imgs[0]['vis_h']} · 그려진 픽셀 {imgs[0]['drawn']})" if imgs else "")
                                  + f" → {'벡터' if vec_ok else '비트맵' if img_ok else '못 찾음'}")
                else:
                    big = [im for im in N["imgs"] if im["size"][0] == minwidth]
                    det = f"PDF {N['pages']}쪽 · 폭 {minwidth} 캔버스 이미지 {[(x['size'], x['page'], x['vis_w'], x['vis_h']) for x in big]}"
                    ok = not N["errs"] and len(big) == 2
                    if "base" in res:
                        sig_new, sig_old = pdf_signature(N["imgs"]), pdf_signature(res["base"]["imgs"])
                        ok = ok and sig_new == sig_old
                        det += f" · 이미지 구성 기준과 {'같음' if sig_new == sig_old else '다름 새 ' + str(sig_new) + ' / 기준 ' + str(sig_old)}"
                    else:
                        det += " · --base 없음 — 기준 대조 생략"
                    run.check(f"인쇄 {w} PC PDF = 기준", ok, det + f" · pageerror {len(N['errs'])}")
            b.close()
    finally:
        if not out:
            shutil.rmtree(tmp, ignore_errors=True)
    run.check("외부 요청", not run.blocked and len(run.allowed) == len(CDN_ALLOW),
              f"허용 {len(run.allowed)} · 차단 {len(run.blocked)}" + (f" {sorted(set(run.blocked))}" if run.blocked else ""))
    print(f"외부 요청 허용 {len(run.allowed)} · 차단 {len(run.blocked)}")
    if out:
        print(f"캡처·PDF: {os.path.abspath(out)}")
    print(f"chart_check: PASS {run.n_pass} / FAIL {len(run.fails)}" + (f" — 실패 {run.fails}" if run.fails else " — 전부 통과"))
    return 1 if run.fails else 0


if __name__ == "__main__":
    sys.exit(main())
