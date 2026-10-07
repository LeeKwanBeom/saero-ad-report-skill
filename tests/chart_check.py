#!/usr/bin/env python3
"""01·06 라이브 차트 확인 — 레이아웃 판 r2026-10-D(01·06 모바일 가로 막대 + 처음 최근 mobile.recent_days 일 · 펼치기 버튼)의 "보이는 숫자 누락 0" 을 진짜 Chart.js 로 잰다.

사용법: "$PY" tests/chart_check.py <index.html> <compute.json> [--base <직전 배포본 html>] [--out <캡처 폴더>] [--widths 390,1280]

자리(사용자 결정 2026-10-06 — 8): **precheck 밖** — 구현·검증 회차 리허설 · 첫 적용 "보류" 회차(운영 세션) · 정기점검에서 돌린다.
playwright chromium 새 임시 프로필(수집 프로필 `~/saero-fetch` 아님) · 밖 요청은 cdnjs Chart.js·datalabels 2건만 보내고(allow-list)
그 밖은 막고 센다 — 막힌 요청이 1건이라도 있으면 URL 과 함께 FAIL(새 CDN·파일 0 원칙). file:// 는 그대로.
기다림: networkidle + 1.8초(Chart.js 애니메이션 1초 — 버튼 누른 뒤·회전 복귀 뒤도 같은 1.8초). 기준값(분기 경계·인쇄 높이 상한·행 높이·최근 일수 K)은 config report_layout.mobile 에서 읽는다.

판정(하나라도 어긋나면 exit 1 · Chart.js 가 안 읽히면 `[FAIL] chart_check: Chart.js CDN 미로드 — 라이브 차트 확인 불가` exit 2 = 통과 아님):
- 모바일 폭(≤ config mobile.max_px, 기본 390 — dpr 2·모바일 UA), 판 D 접기(K = mobile.recent_days, 날짜 n > K 일 때):
  처음(접힘) 01 indexAxis 'y' · 그리는 날짜 = 최근 K(tick K · 맨 위 = 최신 · 맨 아래 = n−K 번째) · 보이는 datalabels = 2K/2K · 캔버스 밖 0 · 글자 겹침 0(padding 을 뺀
  글자 상자 교차) · padding 상자 겹침 ≤ --base 를 같은 폭에서 같은 도구로 잰 값(--base 없으면 1) · 제목 띠 침범 0(라벨 상자 y < chartArea.top) ·
  컨테이너 높이 = K×row_px+pad_px · 스크롤 박스 scrollWidth = clientWidth(뱃지 없음) · 카드 아래 버튼 하나 문구 "이전 n−K일(M/D~M/D) 펼치기"
  (labels 앞 n−K 개의 처음~끝, 요일 괄호 뺌) · aria-expanded false · 글꼴 크기·굵기·색·글꼴 = 03 접기 summary / 06 같은 꼴(라벨 K/K · padding·글자 겹침 0) /
  01 버튼 누름 → 01 전 기간(tick n · 라벨 2n/2n · 높이 n×row+pad · 맨 아래 = 첫 날짜 · 문구 그대로 · aria-expanded true) · 06 은 그대로(접힘) /
  01 다시 누름 → 처음과 같음 · 버튼 화면 위치 그대로(±1px) / 06 누름 → 06 전 기간 · 01 그대로 / 둘 다 펼침 /
  짧은 사본(apply 로 01·06 배열을 최근 K일·K+1일로 자른 판): K일이면 버튼 0·전부 · K+1일이면 "이전 1일(…)" 버튼 /
  문서 scrollWidth = 폭 / 문서의 캔버스 전부(8) Chart.getChart 있음 / pageerror 0. n ≤ K 면 처음부터 전 기간·버튼 없음을 기대한다.
- PC 폭(기본 1280): 01·06 indexAxis 'x' · tick n · 보이는 datalabels(01 2n · 06 0) · chartArea·첫 화면 일수·섹션 1·6 높이·뱃지 = --base 측정값
  (첫 화면은 새 판·기준 둘 다 01·06 박스를 맨 왼쪽으로 되돌려 잰다 — 판 C 이후 기준은 로드 때 최신 쪽이라) ·
  S(스크롤 시작 최신 쪽): 01·06 박스 scrollLeft = scrollWidth − clientWidth · 래퍼 .at-end 있음·.at-start 없음 · 첫 화면 끝 날짜 = 최신 · 펼치기 버튼 0.
- 회전(모바일 폭 → 01 펼침 → 가로 844 → 모바일): 844 에서 01 'x'·tick n·scrollWidth = compute minwidth·뱃지·scrollLeft 끝 · 06 'x'·tick n · 버튼 0 /
  복귀에서 처음(접힘)과 같음('y'·그리는 날짜 K·높이 K×row+pad·라벨 2K · 버튼 문구·aria-expanded false) · .scroll-fade 래퍼가 남아 있으면 at-start·at-end 둘 다(페이드 0) ·
  뱃지 0 · pageerror 0.
- 인쇄 = page.pdf 실물(A4 · 여백 0.4in): 모바일 컨텍스트(처음 = 접힘)에서 `__ev` 훅(add_init_script — DOMContentLoaded 에 걸어 페이지 리스너 뒤에 돈다)으로
  beforeprint 때 01·06 이 전 기간(날짜 n)·컨테이너 높이 = min(n×row+pad, print_max_height_px) · indexAxis 'y' 유지 · afterprint 뒤 접힘(날짜 K·높이 K×row+pad)·indexAxis 복구,
  pypdf 로 01·06 이 PDF 에 한 쪽 안·날짜 n 개 전부(누락 0) —
  둘 중 하나: **벡터**(beforeprint 에 다시 그린 캔버스는 그리기 명령 그대로 실려 글자가 PDF 텍스트 — layout 추출 한 줄이 '날짜 노출 비용원'·'날짜 순위' 인 행이
  한 쪽에만 n 개 전부, 위에서 아래로 최신 → 오래된) 또는 **비트맵**(beforeprint 때 캔버스 비트맵 크기와 같은 이미지가 정확히 한 번·쪽 안·클립 없이·그려진 픽셀 > 0) /
  PC 컨텍스트 PDF 는 --base 와 같은 이미지 구성(큰 이미지 크기·배치 수·보이는 비율 같음 — 폭 3,280 캔버스가 종이 폭에 잘린 일수 그대로. 어느 날짜 구간이 찍히는지는
  대조하지 않는다 — 판 C 는 화면 스크롤 자리(S, 최신 쪽)를 따른다).
- --out 이 있으면 모바일·PC 폭의 섹션 1·6 PNG(로드 상태 — 모바일은 접힘 `<폭>_sec1.png` + 둘 다 펼침 `<폭>_open_sec1.png`)와 PDF 를 저장하고,
  --base 도 있으면 기준 캡처 `base_<폭>_sec1.png` 와 전후 비교 페이지 `<out>/compare.html`(옛 판 · 새 판 처음 · 새 판 펼침 나란히, 그림 내장 한 파일 ·
  높이 표)을 쓴다 — 첫 적용 보류 회차에 사용자에게 보이는 비교 페이지(2026-10-07 — 이전 회차 생성기 mk_compare.py 는 작업 clone 과 함께 지워짐).

검사로 못 지키는 것 — **사용자 시크릿 창(실기기) 몫**: 실기기 폰트 폭(iOS Safari·삼성 인터넷 — 라벨 겹침이 달라질 수 있음) · 회전 체감·첫 페인트 깜빡임 ·
iOS 공유→PDF·실제 인쇄 대화상자(beforeprint 가 오는지) · PWA 설치본의 service-worker 캐시(network-first — 온라인이면 첫 열기에 새 판).
"""
import argparse
import json
import os
import re
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
  let topLabel = null, bottomLabel = null;
  if (horiz && cat.ticks.length) { let best = null, low = null; cat.ticks.forEach((t, i) => { const px = cat.getPixelForTick(i); if (best === null || px < best.px) best = {px, v: t.value};
    if (low === null || px > low.px) low = {px, v: t.value}; }); topLabel = c.data.labels[best.v]; bottomLabel = c.data.labels[low.v]; }
  const fs = (e) => { const s = getComputedStyle(e); return [s.fontSize, s.fontWeight, s.color, s.fontFamily]; };
  const card = canvas.closest('.card'), bts = card ? card.querySelectorAll('.chart-fold') : [];
  const btn = bts.length ? {count: bts.length, text: bts[0].textContent, expanded: bts[0].getAttribute('aria-expanded'), font: fs(bts[0]),
                            top: r1(bts[0].getBoundingClientRect().top), h: r1(bts[0].getBoundingClientRect().height)} : null;
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
  return {indexAxis: c.options.indexAxis || 'x', n, ticks: cat.ticks.length, topLabel, bottomLabel, lab0: c.data.labels[0], labN: c.data.labels[n - 1], btn, first,
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
  const s3 = document.querySelector('summary.fold-more'), st = s3 ? getComputedStyle(s3) : null;   // 문서 첫 접기 summary = 03 "이전 N일" — 펼치기 버튼 글꼴 기준
  return {canvases: cv.length, charts: cv.filter(c => Chart.getChart(c)).length, missing: cv.filter(c => !Chart.getChart(c)).map(c => c.id),
          docSW: document.documentElement.scrollWidth, docSH: document.documentElement.scrollHeight, secs, scrollY: window.scrollY,
          foldBtns: document.querySelectorAll('.chart-fold').length, sum3: st ? [st.fontSize, st.fontWeight, st.color, st.fontFamily] : null};
}"""

# 인쇄 훅 — DOMContentLoaded 에 걸어 페이지의 beforeprint/afterprint 리스너(차트 스크립트 끝 분기 도우미 · 안내 스크립트)보다 뒤에 돈다
EV_HOOK = """window.__ev = {beforeprint: [], afterprint: [], mq: []};
document.addEventListener('DOMContentLoaded', function(){
  function snap(k){ var o = {k: k, docW: document.documentElement.clientWidth};
    ['dailyChart', 'rankChart'].forEach(function(id){ var cv = document.getElementById(id); var c = (window.Chart && cv) ? Chart.getChart(cv) : null; var b = cv ? cv.parentElement : null;
      o[id] = {idx: c ? (c.options.indexAxis || 'x') : null, h: b ? Math.round(b.getBoundingClientRect().height * 10) / 10 : null, styleH: b ? b.style.height : null,
               bitmap: cv ? [cv.width, cv.height] : null, n: c ? c.data.labels.length : null}; });
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
    """섹션 1·6 캡처 — full_page 캡처는 쓰지 않는다: 같은 페이지에서 두 번째부터 창이 순간 4×4 로 바뀌는 resize 가 와서 Chart.js 가 다시 붙으며
    애니메이션 첫 프레임(막대 0)이 찍힌다(2026-10-07 실측 — 차트 인스턴스·판정 수치는 그대로). 대신 뷰포트 높이를 문서 높이로 잠시 늘려(폭 그대로 — 분기 경계 무관)
    맨 위에서 찍고 되돌린다."""
    if not out:
        return
    vp = pg.viewport_size
    sy = pg.evaluate("window.scrollY")
    pg.set_viewport_size({"width": vp["width"], "height": max(vp["height"], int(page_info["docSH"]))})
    pg.evaluate("window.scrollTo(0, 0)")
    pg.wait_for_timeout(300)
    try:
        for s in ("1", "6"):
            r = page_info["secs"].get(s)
            if r:
                pg.screenshot(path=os.path.join(out, f"{tag}_sec{s}.png"),
                              clip={"x": max(0, r["x"]), "y": max(0, r["y"]), "width": r["w"], "height": r["h"]})
    finally:
        pg.set_viewport_size(vp)
        pg.evaluate(f"window.scrollTo(0, {int(sy)})")
        pg.wait_for_timeout(300)


def write_compare(out, new_path, base_path, widths, maxpx, hts):
    """전후 비교 페이지(첫 적용 보류 회차에 사용자에게 보인다) — 섹션 1·6 캡처를 옛 판(--base) · 새 판(로드 상태 = 모바일 접힘) · 새 판 펼침(모바일)
    나란히, 그림은 base64 로 넣은 한 파일(<out>/compare.html). 높이 표는 이 실행의 측정값."""
    import base64
    import html as H

    def meta(p):
        with open(p, encoding="utf-8") as f:
            t = f.read()
        lid = re.search(r'<meta name="report-layout" content="([^"]*)">', t)
        per = re.search(r"집계 기간<b>([^<]+)</b>", t)
        return (lid.group(1) if lid else "meta 없음"), (per.group(1) if per else "?")

    def img(name, cap):
        p = os.path.join(out, name)
        if not os.path.exists(p):
            return f"<figure><figcaption>{H.escape(cap)}</figcaption><p class='k'>캡처 없음</p></figure>"
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"<figure><figcaption>{H.escape(cap)}</figcaption><img alt='{H.escape(name)}' src='data:image/png;base64,{b64}'></figure>"
    (lo, po), (ln, pn) = meta(base_path), meta(new_path)
    rows = "".join(f"<tr><td>{w}</td><td>{k}</td>" + "".join(f"<td class='n'>{v if v is not None else '—'}</td>" for v in hts[w].get(k, (None, None, None))) + "</tr>"
                   for w in widths for k in ("옛 판", "새 판(처음)", "새 판(펼침)") if k in hts.get(w, {}))
    secs = ""
    for s, name in (("1", "01 일별 추이"), ("6", "06 파워링크 키워드 노출순위 추이")):
        secs += f"<h2>{name}</h2>"
        for w in widths:
            mob = w <= maxpx
            figs = img(f"base_{w}_sec{s}.png", f"옛 판 {lo} · {w}px") + img(f"{w}_sec{s}.png", f"새 판 {ln} · {w}px" + (" · 처음(접힘)" if mob else ""))
            if mob:
                figs += img(f"{w}_open_sec{s}.png", f"새 판 {ln} · {w}px · 펼침(버튼 누른 뒤)")
            secs += f"<h3>{w}px 폭</h3><div class='pair{' w3' if mob else ''}'>{figs}</div>"
    page = ("<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>전후 비교</title><style>"
            ":root{--mint:#45ceb3;--mint-dark:#2ea88f;--ink:#1c2b2a;--ink-soft:#5b6b6a;--paper:#fbfaf7;--card:#fff;--line:#e7e2d8;}"
            "*{box-sizing:border-box} body{margin:0;background:var(--paper);color:var(--ink);font-family:'Pretendard','Apple SD Gothic Neo','Noto Sans KR',sans-serif;}"
            ".wrap{max-width:1400px;margin:0 auto;padding:24px 16px 60px} h1{font-size:22px;margin:0 0 6px} h2{font-size:17px;border-left:4px solid var(--mint);padding-left:8px;margin:28px 0 8px}"
            "h3{font-size:13px;color:var(--ink-soft);margin:14px 0 6px} .k,.meta{font-size:12.5px;color:var(--ink-soft);line-height:1.6}"
            "table{border-collapse:collapse;font-size:12.5px;background:var(--card)} th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;white-space:nowrap}"
            "th{color:var(--ink-soft);font-size:11.5px} .n{text-align:right;font-variant-numeric:tabular-nums} .tw{overflow-x:auto}"
            ".pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start} .pair.w3{grid-template-columns:repeat(3,minmax(0,420px))}"
            "figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px} figcaption{font-size:12px;font-weight:700;color:var(--mint-dark);margin-bottom:6px}"
            "img{width:100%;height:auto;display:block} @media (max-width:700px){.pair,.pair.w3{grid-template-columns:1fr}}"
            "</style></head><body><div class='wrap'><h1>전후 비교 — 01, 06번</h1>"
            f"<p class='meta'>옛 판 <b>{H.escape(base_path)}</b> (레이아웃 meta {lo} · 집계 기간 {H.escape(po)})<br>새 판 <b>{H.escape(new_path)}</b> (레이아웃 meta {ln} · 집계 기간 {H.escape(pn)})<br>"
            "캡처: tests/chart_check.py(Chart.js CDN 2건만 허용 · networkidle + 1.8초). 새 판 모바일은 처음(접힘)과 01·06 버튼을 누른 뒤(펼침) 두 가지.</p>"
            "<h2>높이(px)</h2><div class='tw'><table><thead><tr><th>폭</th><th>판</th><th class='n'>섹션 1</th><th class='n'>섹션 6</th><th class='n'>문서 전체</th></tr></thead>"
            f"<tbody>{rows}</tbody></table></div>{secs}</div></body></html>")
    p = os.path.join(out, "compare.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(page)
    return p


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


def btn_text(labels, k):
    """판 D 펼치기 버튼 문구 기대값 — 접는 앞쪽 n−K 일의 처음~끝(요일 괄호 뺀 M/D). 접을 날짜가 없으면 None(버튼 없음)."""
    n = len(labels)
    if k < 1 or n <= k:
        return None
    md = lambda s: s.split("(")[0]
    return f"이전 {n - k}일({md(labels[0])}~{md(labels[n - k - 1])}) 펼치기"


def view_ok(key, v, labels, k, open_, row, padpx, pad_max, sum3):
    """모바일 한 차트(01/06)의 기대 — open_ 이면 전 기간 n, 아니면 최근 min(n, K). (통과 여부, 설명)"""
    n = len(labels)
    m = n if open_ or n <= k else k
    dl = f"{2 * m}/{2 * m}" if key == "01" else f"{m}/{m}"
    want_h = m * row[key] + padpx[key]
    txt = btn_text(labels, k)
    b = v.get("btn")
    if txt is None:
        b_ok = b is None
    else:
        b_ok = bool(b) and b["count"] == 1 and b["text"] == txt and b["expanded"] == ("true" if open_ else "false") and b["font"] == sum3
    ok = (v["indexAxis"] == "y" and v["n"] == m and v["ticks"] == m and v["dl"] == dl and v["outside"] == 0 and v["glyphOverlap"] == 0
          and v["padOverlap"] <= pad_max and v["titleInvade"] == 0 and abs(v["contH"] - want_h) < 0.6 and v["box"] and v["box"]["sw"] == v["box"]["cw"]
          and not v["hint"] and v["topLabel"] == labels[-1] and v["bottomLabel"] == labels[n - m] and v["lab0"] == labels[n - m] and b_ok)
    det = (f"{'펼침' if open_ else '접힘'} indexAxis {v['indexAxis']} · 날짜 {v['n']}(기대 {m}/{n}) · ticks {v['ticks']} · 라벨 {v['dl']}(기대 {dl}) · 밖 {v['outside']} · "
           f"글자 겹침 {v['glyphOverlap']}{v['glyphPairs'] or ''} · padding 겹침 {v['padOverlap']}{v['padPairs'] or ''}(≤ {pad_max}) · 제목 띠 {v['titleInvade']} · "
           f"높이 {v['contH']} = {m}×{row[key]}+{padpx[key]}({want_h}) · 맨 위 {v['topLabel']} · 맨 아래 {v['bottomLabel']} · 뱃지 {v['hint']} · 캔버스 {v['w']}×{v['h']} · "
           f"버튼 {('없음' if not b else repr(b['text']) + ' aria-expanded ' + str(b['expanded']) + ' · 글꼴 ' + ('= 03 summary' if b['font'] == sum3 else str(b['font']) + ' ≠ 03 ' + str(sum3)))}"
           f"(기대 {txt!r})")
    return ok, det


KEYS = ("indexAxis", "n", "ticks", "dl", "glyphOverlap", "padOverlap", "outside", "contH", "contMinW", "topLabel", "bottomLabel", "w", "h")


def same_view(a, b):
    """두 측정(같은 차트)이 같은 모양인가 — 회전 복귀·다시 접힘 대조(버튼 문구·aria-expanded 포함, 화면 위치 제외)."""
    ba, bb = a.get("btn"), b.get("btn")
    return all(a[x] == b[x] for x in KEYS) and ((ba is None and bb is None) or (ba and bb and (ba["text"], ba["expanded"]) == (bb["text"], bb["expanded"])))


def main():
    ap = argparse.ArgumentParser(description="01·06 라이브 차트 확인(레이아웃 판 r2026-10-D — precheck 밖)")
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
    K = {k: int(v) for k, v in mob["recent_days"].items()}
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
          f"row {row} · pad {padpx} · recent {K} · 기준 {os.path.abspath(a.base) if a.base else '없음'}")
    kv = {k: (n if n <= K[k] else K[k]) for k in ("01", "06")}   # 모바일 처음(접힘) 그리는 날짜 수
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
                    mb = measure(pg)
                    shot(pg, mb["page"], out, f"base_{w}")   # 전후 비교 재료(로드 상태)
                    if not mobile:  # 기준도 같은 스크롤 자리(맨 왼쪽)에서 — 판 C 이후 기준은 로드 때 최신 쪽(S)이라
                        to_left(pg)
                        mb["start"] = measure(pg)
                    return mb
                finally:
                    ctx.close()

            def to_left(pg):
                pg.evaluate("() => ['dailyChart', 'rankChart'].forEach(id => { const b = document.getElementById(id).closest('.scroll-x'); "
                            "if (b) { b.scrollLeft = 0; b.dispatchEvent(new Event('scroll')); } })")
                pg.wait_for_timeout(300)

            def click(pg, cid):
                """판 D 펼치기 버튼(그 차트 카드 안 .chart-fold) 진짜 누르기 — (누르기 전 화면 y, 뒤 화면 y) · 버튼이 하나가 아니면 None."""
                loc = pg.locator(".card", has=pg.locator(f"#{cid}")).locator(".chart-fold")
                if loc.count() != 1:
                    return None
                loc.scroll_into_view_if_needed()
                t0 = loc.bounding_box()["y"]
                loc.click()
                pg.wait_for_timeout(SETTLE)
                bb = loc.bounding_box() if loc.count() == 1 else None
                return round(t0, 1), (round(bb["y"], 1) if bb else None)

            folds = {k: n > K[k] for k in ("01", "06")}
            hts = {}   # 전후 비교 높이 표 — {폭: {판: (섹션 1, 섹션 6, 문서)}}
            sec_h = lambda pi: (pi["secs"].get("1", {}).get("h"), pi["secs"].get("6", {}).get("h"), pi["docSH"])
            bpad = {"01": 1, "06": 0}   # 모바일 padding 겹침 상한(01 = --base 측정값, 아래 모바일 폭에서 채움)
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
                hts.setdefault(w, {})["새 판(처음)"] = sec_h(m["page"])
                m_start = None
                if not mobile:  # PC 모양 대조는 기준과 같은 스크롤 자리(맨 왼쪽)에서 — S 는 로드 상태(m)로 따로 본다
                    to_left(pg)
                    m_start = measure(pg)
                seq = {}
                if mobile and folds["01"] and folds["06"]:  # 판 D 버튼 — 01 펼침 → 01 다시 접힘(버튼 자리) → 06 펼침 → 01 도 펼침(둘 다)
                    for step, cid in (("open01", "dailyChart"), ("close01", "dailyChart"), ("open06", "rankChart"), ("both", "dailyChart")):
                        t = click(pg, cid)
                        if t is None:
                            break
                        seq[step] = measure(pg)
                        seq[step]["tops"] = t
                    if "both" in seq:
                        pg.mouse.move(0, 0)   # 캡처 전 마우스를 카드 밖(왼쪽 여백)으로 — 누른 자리에 남은 호버(툴팁·강조)가 비교 캡처에 찍히지 않게.
                        # 펼침 PNG 는 그래도 실행마다 하위 픽셀만 다를 수 있다(2026-10-07 실측 — 눈으로 같음 · 판정 수치는 같음). 로드 상태 PNG 는 바이트 같음
                        pg.wait_for_timeout(SETTLE)
                        shot(pg, seq["both"]["page"], out, f"{w}_open")
                        hts[w]["새 판(펼침)"] = sec_h(seq["both"]["page"])
                ctx.close()
                B = base_measure(w, h, mobile)
                if B:
                    hts[w]["옛 판"] = sec_h(B["page"])
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
                    bpad["01"] = B["01"]["padOverlap"] if B and "err" not in B["01"] else 1
                    sum3 = pgi["sum3"]
                    for k, v in (("01", d), ("06", r)):
                        ok, det = view_ok(k, v, labels, K[k], False, row, padpx, bpad[k], sum3)
                        run.check(f"{w} {k} 모바일 처음{'(최근 ' + str(K[k]) + '일 · 접힘)' if folds[k] else '(전부 — 날짜 ≤ K)'}", ok,
                                  det + ("" if k == "06" else f" · padding 기준 {bpad['01']}{'' if B else ' — --base 없음, 기본값'}"))
                    print(f"       {w} 섹션 높이 1 {pgi['secs'].get('1', {}).get('h')} · 6 {pgi['secs'].get('6', {}).get('h')} · 문서 높이 {pgi['docSH']}"
                          + (f"(기준 1 {B['page']['secs'].get('1', {}).get('h')} · 6 {B['page']['secs'].get('6', {}).get('h')} · 문서 {B['page']['docSH']})" if B else ""))
                    if folds["01"] != folds["06"]:
                        run.check(f"{w} 판 D 접기 시험 범위", False, f"01 접힘 {folds['01']} · 06 접힘 {folds['06']} — K 가 달라 한쪽만 접히는 경우는 이 도구가 버튼 순서를 다루지 않음")
                    elif folds["01"]:
                        sA, sB, sC, sD = (seq.get(x) for x in ("open01", "close01", "open06", "both"))
                        if not sA:
                            run.check(f"{w} 01 펼침(06 그대로)", False, "01 펼치기 버튼이 하나가 아님 — 누르지 못함")
                        else:
                            ok, det = view_ok("01", sA["01"], labels, K["01"], True, row, padpx, bpad["01"], sum3)
                            run.check(f"{w} 01 펼침(06 그대로)", ok and same_view(sA["06"], r), det + f" | 06 처음과 같음 {same_view(sA['06'], r)}")
                        if sB:
                            t0, t1 = sB["tops"]
                            ok = same_view(sB["01"], d) and same_view(sB["06"], r) and t1 is not None and abs(t1 - t0) <= 1
                            run.check(f"{w} 01 다시 접힘(처음과 같음 · 버튼 자리 그대로)", ok,
                                      f"01 처음과 같음 {same_view(sB['01'], d)} · 06 {same_view(sB['06'], r)} · 버튼 화면 y {t0} → {t1} · scrollY {sA['page']['scrollY'] if sA else '?'} → {sB['page']['scrollY']} · "
                                      f"날짜 {sB['01']['n']} · 높이 {sB['01']['contH']}")
                        else:
                            run.check(f"{w} 01 다시 접힘(처음과 같음 · 버튼 자리 그대로)", False, "누르지 못함")
                        if sC:
                            ok, det = view_ok("06", sC["06"], labels, K["06"], True, row, padpx, bpad["06"], sum3)
                            run.check(f"{w} 06 펼침(01 그대로)", ok and same_view(sC["01"], d), det + f" | 01 처음과 같음 {same_view(sC['01'], d)}")
                        else:
                            run.check(f"{w} 06 펼침(01 그대로)", False, "06 펼치기 버튼이 하나가 아님 — 누르지 못함")
                        if sD:
                            ok1, det1 = view_ok("01", sD["01"], labels, K["01"], True, row, padpx, bpad["01"], sum3)
                            ok6, det6 = view_ok("06", sD["06"], labels, K["06"], True, row, padpx, bpad["06"], sum3)
                            ok = ok1 and ok6 and sD["page"]["charts"] == sD["page"]["canvases"] == 8 and sD["page"]["docSW"] == w and not errs
                            run.check(f"{w} 01·06 둘 다 펼침", ok, f"01 {det1} | 06 {det6} | 캔버스 {sD['page']['charts']}/{sD['page']['canvases']} · 문서 폭 {sD['page']['docSW']} · pageerror {len(errs)}")
                            print(f"       {w} 펼침 섹션 높이 1 {sD['page']['secs'].get('1', {}).get('h')} · 6 {sD['page']['secs'].get('6', {}).get('h')} · 문서 높이 {sD['page']['docSH']}")
                        else:
                            run.check(f"{w} 01·06 둘 다 펼침", False, "누르지 못함")
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
                        if B and "err" not in B[k] and "err" not in B["start"][k]:
                            bv = B["start"][k]
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
                    run.check(f"{w} 펼치기 버튼 없음(PC)", pgi["foldBtns"] == 0, f"문서의 .chart-fold {pgi['foldBtns']}개")

            # ── 회전: 모바일 폭 → 가로(844) → 모바일 ──
            mws = [w for w in widths if w <= maxpx]
            if mws:
                w = mws[0]
                ctx, pg, errs = new_ctx(b, run, w, 844, True)
                load(pg, a.html)
                m0 = measure(pg)
                opened = click(pg, "dailyChart") if folds["01"] else None   # 판 D: 01 을 펼친 채로 회전 — 모바일로 돌아오면 접힘부터
                pg.set_viewport_size({"width": 844, "height": w})
                pg.wait_for_timeout(700)
                m1 = measure(pg)
                pg.set_viewport_size({"width": w, "height": 844})
                pg.wait_for_timeout(SETTLE)
                m2 = measure(pg)
                ctx.close()
                d1, r1_ = m1["01"], m1["06"]
                bx = d1.get("box") or {}
                ok = (d1.get("indexAxis") == "x" and d1.get("ticks") == n and bx.get("sw") == minwidth and d1.get("hint") and abs(bx.get("sl", -9) - (bx.get("sw", 0) - bx.get("cw", 0))) <= 1
                      and d1.get("atEnd") and not d1.get("atStart") and r1_.get("indexAxis") == "x" and r1_.get("ticks") == n and r1_.get("hint") and m1["page"]["foldBtns"] == 0)
                run.check(f"회전 {w}→844 PC 분기", ok,
                          f"01 indexAxis {d1.get('indexAxis')} · ticks {d1.get('ticks')} · 박스 {bx}(scrollWidth = minwidth {minwidth}) · 뱃지 {d1.get('hint')} · at-end {d1.get('atEnd')} · at-start {d1.get('atStart')} · "
                          f"06 indexAxis {r1_.get('indexAxis')} · ticks {r1_.get('ticks')} · 뱃지 {r1_.get('hint')} · 박스 {r1_.get('box')} · 펼치기 버튼 {m1['page']['foldBtns']}"
                          + (f" · 회전 전 01 펼침 {opened}" if folds["01"] else ""))
                same = all(same_view(m2[k], m0[k]) for k in ("01", "06"))
                fade_ok = all((not m2[k]["fade"]) or (m2[k]["atEnd"] and m2[k]["atStart"]) for k in ("01", "06"))
                ok = (same and fade_ok and not m2["01"]["hint"] and not m2["06"]["hint"] and m2["01"]["indexAxis"] == "y" and not errs
                      and m2["page"]["foldBtns"] == m0["page"]["foldBtns"] and (opened is not None or not folds["01"]))
                run.check(f"회전 844→{w} 복원(처음 = 접힘과 같음)", ok,
                          f"01 {[m2['01'][x] for x in KEYS]} 버튼 {(m2['01']['btn'] or {}).get('expanded')} · 처음 {[m0['01'][x] for x in KEYS]} 버튼 {(m0['01']['btn'] or {}).get('expanded')} · "
                          f"06 같음 {same_view(m2['06'], m0['06'])} · 펼치기 버튼 {m2['page']['foldBtns']}(처음 {m0['page']['foldBtns']}) · "
                          f"래퍼 01 {m2['01']['fade']}(at-end {m2['01']['atEnd']} · at-start {m2['01']['atStart']}) · 06 {m2['06']['fade']}(at-end {m2['06']['atEnd']} · at-start {m2['06']['atStart']}) · "
                          f"뱃지 {m2['01']['hint']}/{m2['06']['hint']} · pageerror {len(errs)}")

                # ── 짧은 사본(판 D 가장자리): apply 로 01·06 배열을 최근 K일·K+1일로 자른 판 — K일이면 버튼 없이 전부, K+1일이면 "이전 1일(…)" ──
                if n > max(K.values()):
                    import apply as A
                    with open(a.html, encoding="utf-8", newline="") as f:
                        H = f.read()
                    for nn in sorted({K["01"], K["01"] + 1, K["06"], K["06"] + 1}):
                        Rs = json.loads(json.dumps(R))
                        for s1, s2 in (("01", "labels"), ("01", "노출"), ("01", "총비용"), ("06", "rankChart")):
                            Rs[s1][s2] = Rs[s1][s2][-nn:]
                        ps = os.path.join(tmp, f"short_{nn}.html")
                        with open(ps, "w", encoding="utf-8", newline="") as f:
                            f.write(A.apply(H, Rs, cfg))
                        ctx, pg, errs = new_ctx(b, run, w, 844, True)
                        load(pg, ps)
                        ms = measure(pg)
                        ctx.close()
                        for k in ("01", "06"):
                            ok, det = view_ok(k, ms[k], labels[-nn:], K[k], False, row, padpx, bpad[k], ms["page"]["sum3"])
                            run.check(f"짧은 사본 {nn}일 {k}({'버튼 없음' if nn <= K[k] else '이전 ' + str(nn - K[k]) + '일 버튼'})", ok and not errs, det + f" · pageerror {len(errs)}")

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
                        full_h, fold_h = n * row[k] + padpx[k], kv[k] * row[k] + padpx[k]   # 인쇄 = 전 기간(높이 캡) · 뒤 = 처음(접힘)
                        b0, a0 = bp[cid], apv[cid]
                        ok = (b0["idx"] == "y" and b0["n"] == n and b0["h"] <= printmax + 0.5 and abs(b0["h"] - min(full_h, printmax)) < 0.6
                              and a0["idx"] == "y" and a0["n"] == kv[k] and abs(a0["h"] - fold_h) < 0.6
                              and N["m1"][k]["indexAxis"] == "y" and abs(N["m1"][k]["contH"] - fold_h) < 0.6 and same_view(N["m1"][k], N["m0"][k]))
                        det += (f" | {k}: beforeprint {b0['idx']} 날짜 {b0['n']}(= {n}) 높이 {b0['h']}(= min({full_h}, {printmax})) 비트맵 {b0['bitmap']} · "
                                f"afterprint {a0['idx']} 날짜 {a0['n']}(= {kv[k]}) 높이 {a0['h']}(= {fold_h}) · "
                                f"뒤 상태 {N['m1'][k]['indexAxis']} {N['m1'][k]['contH']} 라벨 {N['m1'][k]['dl']} · 처음과 같음 {same_view(N['m1'][k], N['m0'][k])}")
                    run.check(f"인쇄 {w} 이벤트(전 기간 · 높이 캡 · 뒤 접힘 복원)", ok and not N["errs"], det + f" · pageerror {len(N['errs'])}")
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
            if out and a.base:
                print(f"전후 비교: {write_compare(out, a.html, a.base, widths, maxpx, hts)}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)   # 짧은 사본·(--out 없을 때) PDF — --out 이 있으면 PDF 는 거기에 있다
    run.check("외부 요청", not run.blocked and len(run.allowed) == len(CDN_ALLOW),
              f"허용 {len(run.allowed)} · 차단 {len(run.blocked)}" + (f" {sorted(set(run.blocked))}" if run.blocked else ""))
    print(f"외부 요청 허용 {len(run.allowed)} · 차단 {len(run.blocked)}")
    if out:
        print(f"캡처·PDF: {os.path.abspath(out)}")
    print(f"chart_check: PASS {run.n_pass} / FAIL {len(run.fails)}" + (f" — 실패 {run.fails}" if run.fails else " — 전부 통과"))
    return 1 if run.fails else 0


if __name__ == "__main__":
    sys.exit(main())
