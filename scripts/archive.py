#!/usr/bin/env python3
"""
네이버 광고 보고서 CSV 월별 보관(store)과 합본 만들기(combine).

네이버 광고시스템은 보고서를 최근 30일까지만 내려준다. 그래서 개업일부터 누적하려면
원본을 저장소에 쌓아 두고 매 회차 합쳐서 써야 한다.

보관 구조:
    data/YYYY-MM/키워드.csv · 검색어.csv · 상세지역.csv · 시간대별.csv
    (네이버가 준 원본 그대로 — 첫 줄 기간 헤더 포함)

사용법:
    python3 archive.py store <업로드CSV> [<업로드CSV> ...] [--chunk] [--force]
        업로드 파일을 컬럼으로 종류를 판별하고, 첫 줄 기간 헤더의 달 폴더에 저장한다.
        같은 달·같은 종류 파일은 덮어쓴다(이번 달은 매일 1일~어제로 다시 받으므로).
        --chunk  : 덮어쓰지 않고 조각으로 추가(<종류>_2.csv …). 31일로 끝나는 달의
                   마지막 날처럼 한 달치를 한 번에 못 받을 때만 쓴다.
        --force  : 새 파일 기간이 기존보다 짧아도 덮어쓴다(기본은 거부 — 옛 다운로드를
                   잘못 올려 데이터가 줄어드는 것을 막는다).

    python3 archive.py combine <출력폴더>
        data/ 아래 전부를 합쳐 <출력폴더>/키워드.csv 등 4개를 만든다. 첫 줄에 합본 기간
        헤더를 넣으므로 validate.py 등 기존 코드는 read_csv(skiprows=1) 그대로 쓴다.

combine 검사(하나라도 실패하면 exit 1, 합본을 쓰지 말 것):
  - 종류별 조각 기간이 빈틈·겹침 없이 이어지는지(헤더 기간 기준)
  - 4종의 조각 경계가 똑같은지(시간대별은 날짜 컬럼이 없어 기간을 헤더로만 알 수 있다)
  - 조각마다 시간대별·상세지역 노출 합계 = 키워드 노출 합계(같은 기간을 받았는지)
  - 날짜 있는 3종의 일별 최솟값 = config open_date, 각 조각 일별이 헤더 기간 안
  - 계정 번호가 전부 같은지
"""

import glob
import json
import os
import re
import shutil
import sys
from datetime import date, timedelta

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
with open(os.path.join(ROOT, "config", "report-config.json"), encoding="utf-8") as f:
    CFG = json.load(f)
OPEN_DATE = CFG["open_date"]  # "2026.08.26."

TYPES = ["키워드", "검색어", "상세지역", "시간대별"]
DATED = ["키워드", "검색어", "상세지역"]
HEAD_RE = re.compile(r"\((\d{4})\.(\d{2})\.(\d{2})\.~(\d{4})\.(\d{2})\.(\d{2})\.\)\s*\"?,\s*(\d+)")


def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)


def read_head(path):
    with open(path, encoding="utf-8-sig") as f:
        line = f.readline().strip()
    m = HEAD_RE.search(line)
    if not m:
        fail(f"{path}: 첫 줄 기간 헤더를 읽을 수 없음 — {line!r}")
    g = [int(x) for x in m.groups()]
    return date(g[0], g[1], g[2]), date(g[3], g[4], g[5]), m.group(7)


def kind_of(path):
    cols = set(pd.read_csv(path, skiprows=1, nrows=0).columns)
    if {"광고그룹", "키워드"} <= cols:
        return "키워드"
    for k in ("검색어", "상세지역", "시간대별"):
        if k in cols:
            return k
    fail(f"{path}: 컬럼으로 보고서 종류를 판별할 수 없음 — {sorted(cols)}")


def store(paths, chunk=False, force=False):
    for p in paths:
        k = kind_of(p)
        s, e, acct = read_head(p)
        if (s.year, s.month) != (e.year, e.month):
            fail(f"{os.path.basename(p)}: 기간 {s}~{e}가 두 달에 걸침 — 달별로 나눠 받아야 함")
        folder = os.path.join(DATA, f"{s.year:04d}-{s.month:02d}")
        os.makedirs(folder, exist_ok=True)
        existing = sorted(glob.glob(os.path.join(folder, f"{k}*.csv")))
        if chunk:
            dest = os.path.join(folder, f"{k}_{len(existing) + 1}.csv" if existing else f"{k}.csv")
        else:
            for old in existing:
                _, oe, _ = read_head(old)
                if e < oe and not force:
                    fail(f"{os.path.basename(p)}: 기간 끝 {e}가 보관본 {os.path.basename(old)}의 끝 {oe}보다 앞섬 "
                         f"— 옛 다운로드로 보임. 맞으면 --force")
            for old in existing:
                os.remove(old)
            dest = os.path.join(folder, f"{k}.csv")
        shutil.copyfile(p, dest)
        print(f"[저장] {os.path.basename(p)} → {os.path.relpath(dest, ROOT)} ({k}, {s}~{e}, 계정 {acct})")


def chunks_of(kind):
    out = []
    for p in glob.glob(os.path.join(DATA, "*", f"{kind}*.csv")):
        s, e, acct = read_head(p)
        out.append((s, e, acct, p))
    return sorted(out)


def combine(outdir):
    os.makedirs(outdir, exist_ok=True)
    per = {k: chunks_of(k) for k in TYPES}
    for k in TYPES:
        if not per[k]:
            fail(f"{k}: data/ 아래 보관본 없음")
    accts = {c[2] for k in TYPES for c in per[k]}
    if len(accts) != 1:
        fail(f"계정 번호가 섞여 있음: {sorted(accts)}")
    acct = accts.pop()

    bounds = {k: [(c[0], c[1]) for c in per[k]] for k in TYPES}
    for k in TYPES:
        b = bounds[k]
        for (s1, e1), (s2, e2) in zip(b, b[1:]):
            if s2 != e1 + timedelta(days=1):
                fail(f"{k}: 조각 {s1}~{e1} 다음이 {s2}~{e2} — 빈틈 또는 겹침")
    ref = bounds["키워드"]
    for k in TYPES[1:]:
        if bounds[k] != ref:
            fail(f"{k} 조각 경계 {bounds[k]} ≠ 키워드 {ref} — 같은 기간으로 받아야 함")

    frames = {k: [] for k in TYPES}
    for i, (s, e) in enumerate(ref):
        dfs = {k: pd.read_csv(per[k][i][3], skiprows=1) for k in TYPES}
        kw_imp = int(dfs["키워드"]["노출수"].sum())
        for k in ("시간대별", "상세지역"):
            v = int(dfs[k]["노출수"].sum())
            if v != kw_imp:
                fail(f"조각 {s}~{e}: {k} 노출 {v:,} ≠ 키워드 {kw_imp:,} — 기간이 다르게 받아졌을 수 있음")
        for k in DATED:
            d = dfs[k]["일별"]
            lo, hi = s.strftime("%Y.%m.%d."), e.strftime("%Y.%m.%d.")
            if len(d) and (d.min() < lo or d.max() > hi):
                fail(f"조각 {s}~{e}: {k} 일별 {d.min()}~{d.max()}가 헤더 기간 밖")
        for k in TYPES:
            frames[k].append(dfs[k])
        print(f"[조각] {s}~{e}  노출 {kw_imp:,} · 클릭 {int(dfs['키워드']['클릭수'].sum()):,} · "
              f"비용 {int(dfs['키워드']['총비용'].sum()):,}원")

    out = {}
    for k in DATED:
        out[k] = pd.concat(frames[k], ignore_index=True)
        mn = out[k]["일별"].min()
        if mn != OPEN_DATE:
            fail(f"{k}: 합본 일별 최솟값 {mn} ≠ 개업일 {OPEN_DATE} — 개업 달 보관본 확인")

    h = pd.concat(frames["시간대별"], ignore_index=True)
    order = list(dict.fromkeys(h["시간대별"]))
    ranked = h["평균노출순위"] > 0  # 순위 0 행은 가중평균에서 뺀다(SKILL.md 계산 규칙)
    h["_rank_w"] = (h["평균노출순위"] * h["노출수"]).where(ranked, 0)
    h["_rank_n"] = h["노출수"].where(ranked, 0)
    num = [c for c in h.columns if c != "시간대별"]
    g = h.groupby("시간대별", sort=False)[num].sum().reindex(order).reset_index()
    g["클릭률(%)"] = (g["클릭수"] / g["노출수"].where(g["노출수"] > 0) * 100).round(2).fillna(0)
    g["평균 CPC"] = (g["총비용"] / g["클릭수"].where(g["클릭수"] > 0)).round(0).fillna(0).astype(int)
    g["평균노출순위"] = (g["_rank_w"] / g["_rank_n"].where(g["_rank_n"] > 0)).round(1).fillna(0)
    if "총 전환율(%)" in g:
        g["총 전환율(%)"] = (g["총 전환수"] / g["클릭수"].where(g["클릭수"] > 0) * 100).round(2).fillna(0)
    out["시간대별"] = g[[c for c in frames["시간대별"][0].columns]]

    s0, e0 = ref[0][0], ref[-1][1]
    for k in TYPES:
        path = os.path.join(outdir, f"{k}.csv")
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            f.write(f"\"{k} 보고서 합본({s0:%Y.%m.%d.}~{e0:%Y.%m.%d.}),{acct}\"\n")
            out[k].to_csv(f, index=False)
    kw = out["키워드"]
    print(f"[합본] {outdir}  일별 {kw['일별'].min()}~{kw['일별'].max()} ({kw['일별'].nunique()}일) · "
          f"노출 {int(kw['노출수'].sum()):,} · 클릭 {int(kw['클릭수'].sum()):,} · 비용 {int(kw['총비용'].sum()):,}원")
    print("[PASS] 합본 검사 통과")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("store", "combine"):
        sys.exit(__doc__)
    if a[0] == "store":
        files = [x for x in a[1:] if not x.startswith("--")]
        if not files:
            sys.exit("저장할 CSV를 지정하세요")
        store(files, chunk="--chunk" in a, force="--force" in a)
    else:
        if len(a) != 2:
            sys.exit("사용법: archive.py combine <출력폴더>")
        combine(a[1])
