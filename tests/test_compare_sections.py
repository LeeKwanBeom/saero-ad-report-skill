#!/usr/bin/env python3
"""compare.py 구역별 try 시험 — 한 구역의 파싱 실패가 다른 구역 항목을 생략시키지 않는지(2026-10-06).

사용법: "$PY" tests/test_compare_sections.py <index.html> <compute.json>
  (index.html 은 그 compute.json 으로 compare DIFF 0 인 작업본 — 예: 리허설 work/R2/index.html + work/R2/compute.json)
동작: 사본만 만든다(원본 읽기 전용). 기준 실행(DIFF 0) 뒤 구역 하나의 서술 문단만 지운 사본 셋을 돌려
  ① DIFF 가 그 구역 항목뿐이고 ② 다른 구역의 기준 [OK] 항목이 전부 다시 [OK] 인지 본다.
  - 01 해석 문단(.note-mint) 삭제 · 07 ②③ 각주 블록 삭제 · 10 최근 7일·평균 문장 삭제
종료 코드: 0 = 전부 맞음, 1 = 아니면.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
COMPARE = os.path.join(os.path.dirname(HERE), "scripts", "compare.py")
LINE = re.compile(r"^  \[(OK|DIFF)\]\s+(.*?)(?::\s|$)")


def section_of(name):
    m = re.match(r"파싱 실패 \[([^\]]+)\]", name)
    if m:
        return m.group(1)
    head = name.split(" ")[0]
    if head in ("masthead", "og:description", "KPI"):
        return "masthead·KPI"
    if head.startswith("11"):
        return "11·12"
    return head.split("/")[0]


def section(html, n):
    s = html.find(f"<!-- Section {n}:")
    e = html.find(f"<!-- Section {n + 1}:")
    return s, (e if e != -1 else html.find("<script>", s))


def cut(html, n, pat):
    s, e = section(html, n)
    seg, k = re.subn(pat, "", html[s:e], count=1, flags=re.S)
    return html[:s] + seg + html[e:] if k == 1 else None


def run(html_text, compute, work):
    p = os.path.join(work, "index.html")
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(html_text)
    r = subprocess.run([sys.executable, COMPARE, p, compute], capture_output=True, text=True, encoding="utf-8")
    ok, diff = set(), []
    for line in r.stdout.splitlines():
        m = LINE.match(line)
        if m:
            (ok.add if m.group(1) == "OK" else diff.append)(m.group(2).strip())
    return r.returncode, ok, diff


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, compute = sys.argv[1], sys.argv[2]
    md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
    before = (md5(src), md5(compute))
    with open(src, encoding="utf-8", newline="") as f:
        H = f.read()
    work = tempfile.mkdtemp(prefix="saero-cmpsec-")
    good = True
    try:
        rc, base_ok, base_diff = run(H, compute, work)
        print(f"기준: exit {rc} · OK {len(base_ok)} · DIFF {len(base_diff)}")
        if rc != 0 or base_diff:
            print("  [MISS] 기준이 DIFF 0 이 아니다 — 작업본과 compute.json 짝 확인:", base_diff)
            return 1
        cases = [("01", "01 해석 문단(.note-mint) 삭제", cut(H, 1, r'<div class="note-mint"[^>]*>.*?</div>')),
                 ("07", "07 ②③ 각주 블록 삭제", cut(H, 7, r'<div class="note"[^>]*>(?:(?!</div>).)*?클릭 0인 검색어 전체는.*?</div>')),
                 ("10", "10 최근 7일·평균 문장 삭제", cut(H, 10, r"최근 7일 노출은 .*?일 평균 [\d.]+건\)\.?"))]
        for sec, label, text in cases:
            if text is None:
                print(f"  [MISS] {label} — 지울 자리를 못 찾음(마크업이 바뀌었으면 이 시험을 고칠 것)")
                good = False
                continue
            rc, ok, diff = run(text, compute, work)
            wrong = [d for d in diff if section_of(d) != sec]
            lost = sorted(n for n in base_ok if section_of(n) != sec and n not in ok)
            other = sorted({section_of(n) for n in ok if section_of(n) != sec})
            res = rc == 1 and diff and not wrong and not lost
            good &= bool(res)
            print(f"  [{'OK' if res else 'MISS'}]   {label} → exit {rc} · DIFF {len(diff)}개(전부 {sec} 구역: {not wrong}) · "
                  f"다른 구역 기준 OK {len(base_ok) - len([n for n in base_ok if section_of(n) == sec])}개 중 다시 OK {len([n for n in ok if section_of(n) != sec])}개 · "
                  f"대조된 다른 구역 {len(other)}개")
            for d in diff:
                print(f"         DIFF: {d}")
            if wrong:
                print(f"         다른 구역 DIFF: {wrong}")
            if lost:
                print(f"         생략된 다른 구역 항목: {lost}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    same = before == (md5(src), md5(compute))
    print(f"원본 md5 그대로: {same}")
    print("전부 맞음 — 한 구역의 파싱 실패가 다른 구역 대조를 생략시키지 않음." if good and same else "문제 있음 — 위 [MISS] 확인.")
    return 0 if good and same else 1


if __name__ == "__main__":
    sys.exit(main())
