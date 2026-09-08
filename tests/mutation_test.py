#!/usr/bin/env python3
"""
validate.py 검사 생존 확인(파괴 실험).

사용법:
    python3 tests/mutation_test.py <배포본 index.html> <키워드CSV> <검색어CSV> <시간대별CSV> <상세지역CSV>

동작:
  1. 스킬 저장소의 scripts/·config/ 와 인자로 받은 index.html·CSV 4개를 임시 디렉토리에
     **복사**한다. 이후 모든 변조는 사본에만 한다. 원본 경로에는 쓰기 자체를 하지 않는다
     (원본은 읽기 전용으로 열고, 시작·종료 시 원본 md5를 대조해 변하지 않았음을 증명한다).
  2. 사본으로 validate.py를 돌려 기준 PASS를 만들고, 출력의 [PASS]/[FAIL] 줄을 세어
     **검사 목록을 실행 시점에 알아낸다**(개수를 이 파일에 적지 않는다).
  3. 검사마다 대응하는 변조(사본 한 곳만 바꾸기)를 적용해 그 검사가 FAIL로 바뀌는지 본다.
  4. 마크업이 바뀌어 검사 대상이 0건이 되는 경우를 흉내 내 0건 가드가 FAIL을 내는지 본다.
  5. config 사본의 값을 바꿔 검사가 설정을 실제로 읽는지 본다.
  6. 기준 목록의 검사 중 어떤 변조도 겨냥하지 않은 것이 있으면 UNCOVERED로 보고한다
     — 검사가 늘었는데 이 스크립트가 따라가지 못했다는 뜻이다.

종료 코드: 0 = 전부 살아 있음(변조마다 겨냥한 검사가 FAIL, 미커버 검사 없음), 1 = 아니면.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_sig(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def section(html, num):
    s = html.find(f"<!-- Section {num}:")
    e = html.find(f"<!-- Section {num + 1}:")
    return html[s:e if e != -1 else len(html)] if s != -1 else ""


def replace_in_section(html, num, old, new):
    sec = section(html, num)
    if not sec or old not in sec:
        return None
    return html.replace(sec, sec.replace(old, new, 1), 1)


def csv_edit(text, row_idx, col_idx, delta):
    """기간 헤더(0행)·컬럼 헤더(1행) 다음 첫 데이터 행의 정수 셀을 delta만큼 바꾼다."""
    lines = text.split("\n")
    row = lines[row_idx].split(",")
    row[col_idx] = str(int(row[col_idx]) + delta)
    lines[row_idx] = ",".join(row)
    return "\n".join(lines)


def main():
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    orig = dict(zip(["html", "kw", "sr", "hr", "rg"], sys.argv[1:6]))
    orig_md5 = {k: md5(v) for k, v in orig.items()}

    work = tempfile.mkdtemp(prefix="saero-mut-")
    try:
        # --- 1. 전부 사본으로 ---
        shutil.copytree(os.path.join(REPO, "scripts"), os.path.join(work, "scripts"))
        shutil.copytree(os.path.join(REPO, "config"), os.path.join(work, "config"))
        validate = os.path.join(work, "scripts", "validate.py")
        cfg_path = os.path.join(work, "config", "report-config.json")
        cfg_text = read(cfg_path)
        cfg = json.loads(cfg_text)
        base = {k: read_sig(v) if k != "html" else read(v) for k, v in orig.items()}
        print(f"작업 디렉토리 {work} (원본에는 쓰지 않음)")

        def run(html=None, csv=None, cfg_override=None):
            paths = {}
            for k in orig:
                p = os.path.join(work, f"{k}.{'html' if k == 'html' else 'csv'}")
                src = (html if (k == "html" and html is not None)
                       else (csv or {}).get(k, base[k]))
                with open(p, "w", encoding="utf-8" if k == "html" else "utf-8-sig") as f:
                    f.write(src)
                paths[k] = p
            with open(cfg_path, "w", encoding="utf-8") as f:
                f.write(cfg_override if cfg_override else cfg_text)
            r = subprocess.run([sys.executable, validate, paths["html"], paths["kw"],
                                paths["sr"], paths["hr"], paths["rg"]],
                               capture_output=True, text=True)
            lines = r.stdout.splitlines()
            passed = [l[7:] for l in lines if l.startswith("[PASS] ")]
            failed = [l[7:] for l in lines if l.startswith("[FAIL] ")]
            return r.returncode, passed, failed, r.stderr

        # --- 2. 기준 PASS, 검사 목록 ---
        rc, passed, failed, err = run()
        checks = [p.split(" — ")[0] for p in passed] + [f.split(" — ")[0] for f in failed]
        print(f"\n기준 실행: 검사 {len(checks)}개, PASS {len(passed)} / FAIL {len(failed)}, exit {rc}")
        for c in checks:
            print(f"  · {c}")
        if failed or rc != 0:
            print("\n기준이 PASS가 아니다. 배포본과 CSV가 맞는 조합인지 먼저 확인할 것.")
            for f in failed:
                print("  [FAIL]", f)
            if err:
                print(err[-500:])
            return 1

        H = base["html"]
        s7, s1 = section(H, 7), section(H, 1)
        date_secs = [int(n) for n in cfg["chart_min_width"]["date_based_sections"]]

        # --- 3. 변조 목록: (이름, 겨냥하는 검사명 조각, 변조 결과) ---
        muts = []

        muts.append(("태그 짝: 첫 </div> 제거", "태그 짝", {"html": H.replace("</div>", "", 1)}))

        m = re.search(r'(<td class="num">[\d,]+</td>\s*<td class="num">)(\d+)(</td>\s*<td class="num[^"]*">[\d.]+%</td>)', s7)
        muts.append(("07 정식표 첫 행 클릭 −1", "07번 클릭수 합계",
                     {"html": replace_in_section(H, 7, m.group(0), f"{m.group(1)}{int(m.group(2)) - 1}{m.group(3)}") if m else None}))

        hr_lines = base["hr"].split("\n")
        clk_col = hr_lines[1].split(",").index("클릭수")
        muts.append(("시간대별 CSV 첫 행 클릭 −1", "09번 시간대별 클릭 합계",
                     {"csv": {"hr": csv_edit(base["hr"], 2, clk_col, -1)}}))

        muts.append(("07 첫 .ctr-high 제거", "07번 클릭률",
                     {"html": replace_in_section(H, 7, 'class="num ctr-high"', 'class="num"')}))
        muts.append(("01 첫 .ctr-high 제거", "01번 클릭률",
                     {"html": replace_in_section(H, 1, 'class="num ctr-high"', 'class="num"')}))

        m = re.search(r"집계 기간<b>([^<]*\()(\d+)(일\)[^<]*)</b>", H)
        muts.append(("masthead 일수 −1", "masthead 집계 기간",
                     {"html": H.replace(m.group(0), f"집계 기간<b>{m.group(1)}{int(m.group(2)) - 1}{m.group(3)}</b>", 1) if m else None}))

        m = re.search(r'(<div class="value">)([\d,]+)(<span class="unit">)', H)
        muts.append(("KPI 첫 타일 값 +1", "KPI 타일",
                     {"html": H.replace(m.group(0), f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}", 1) if m else None}))

        m = re.search(r'<td class="num[^"]*">(\d+\.\d)%</td>', section(H, 4))
        muts.append(("04 첫 예산 비중 −0.1", "04번 예산 비중",
                     {"html": replace_in_section(H, 4, f">{m.group(1)}%<", f">{float(m.group(1)) - 0.1:.1f}%<") if m else None}))

        for n in date_secs:
            m = re.search(r"min-width:\s*(\d+)px", section(H, n))
            muts.append((f"{n:02d}번 min-width −60px", f"{n:02d}번 차트 min-width",
                         {"html": replace_in_section(H, n, m.group(0), f"min-width:{int(m.group(1)) - 60}px") if m else None}))

        m = re.search(r"labels\s*:\s*\[\s*('\d+/\d+\(.\)')\s*,", H)
        muts.append(("날짜축 라벨 배열 첫 항목 제거", "날짜축 x축 라벨 개수",
                     {"html": H.replace(m.group(0), m.group(0).replace(m.group(1) + ",", "", 1)
                                        .replace(m.group(1) + " ,", "", 1), 1) if m else None}))

        muts.append(("Section 5 주석 변조", "섹션 주석",
                     {"html": H.replace("<!-- Section 5:", "<!-- Sect 5:", 1)}))

        m = re.search(r"(와 )(\d+)(회 차이)", H)
        muts.append(("08 각주 N회 +1", "08·09번 각주",
                     {"html": H.replace(m.group(0), f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", 1) if m else None}))

        rg_lines = base["rg"].split("\n")
        imp_col = rg_lines[1].split(",").index("노출수")
        muts.append(("상세지역 CSV 첫 행 노출 +1", "상세지역 CSV 노출 합계",
                     {"csv": {"rg": csv_edit(base["rg"], 2, imp_col, 1)}}))

        # --- 4. 0건 가드 ---
        guards = [
            ("0건: masthead 문구 변조", "masthead 집계 기간", {"html": H.replace("집계 기간<b>", "집계기간<b>", 1)}),
            ("0건: KPI label 클래스 변조", "KPI 타일", {"html": H.replace('<div class="label">', '<div class="lbl">')}),
            ("0건: 04 td.num 전부 변조", "04번 예산 비중", {"html": H.replace(section(H, 4), section(H, 4).replace('<td class="num', '<td class="nm'), 1)}),
            ("0건: 각주 문구 변조", "08·09번 각주", {"html": H.replace("회로 상단 KPI(", "회로 상단 kpi(")}),
            ("0건: 07 name-cell 변조", "07번 클릭률", {"html": section(H, 7) and H.replace(s7, s7.replace('class="name-cell"', 'class="namecell"'), 1)}),
            ("0건: 날짜형 라벨 형식 변조", "날짜축 x축 라벨", {"html": re.sub(r"'(\d+/\d+\(.\))'", r"'\1_'", H)}),
        ]
        for n in date_secs:
            m = re.search(r"\s*min-width:\s*\d+px;?", section(H, n))
            guards.append((f"0건: {n:02d}번 min-width 제거", f"{n:02d}번 차트 min-width",
                           {"html": replace_in_section(H, n, m.group(0), "") if m else None}))

        # --- 5. config 실험 ---
        c1 = json.loads(cfg_text); c1["ctr_high_threshold"] = float(cfg["ctr_high_threshold"]) + 1.0
        c2 = json.loads(cfg_text); c2["chart_min_width"]["date_based_sections"] = date_secs[:1]

        # --- 실행 ---
        ok = True
        print("\n== 검사별 변조 (겨냥한 검사가 FAIL로 바뀌어야 함)")
        covered = set()
        for name, target, spec in muts + guards:
            if spec.get("html") is None and "csv" not in spec:
                print(f"  [SKIP] {name} — 변조 위치를 못 찾음 (마크업이 바뀌었으면 이 스크립트를 고칠 것)")
                ok = False
                continue
            rc, passed, failed, err = run(**spec)
            hit = [f for f in failed if target in f]
            others = [f.split(" — ")[0] for f in failed if target not in f]
            if hit:
                covered.update(c for c in checks if target in c)
                print(f"  [OK]   {name} → FAIL: {hit[0][:90]}" + (f"  (+{others})" if others else ""))
            else:
                ok = False
                print(f"  [MISS] {name} → 겨냥한 '{target}'가 FAIL이 아님. exit {rc}, FAIL={others}" + (f" ERR={err[-200:]}" if err else ""))

        print("\n== config 실험 (설정을 실제로 읽는지)")
        rc, passed, failed, err = run(cfg_override=json.dumps(c1, ensure_ascii=False))
        thr = f"{c1['ctr_high_threshold']:g}%"
        lbl = [x for x in passed + failed if "ctr-high" in x and thr in x]
        print(f"  ctr_high_threshold {cfg['ctr_high_threshold']}→{c1['ctr_high_threshold']}: 라벨에 {thr} 반영 {len(lbl)}건" + ("" if lbl else "  ← MISS"))
        ok &= bool(lbl)
        rc, passed, failed, err = run(cfg_override=json.dumps(c2, ensure_ascii=False))
        n2 = len(passed) + len(failed)
        gone = [n for n in date_secs[1:] if not any(f"{n:02d}번 차트" in x for x in passed + failed)]
        print(f"  date_based_sections {date_secs}→{date_secs[:1]}: 검사 {len(checks)}→{n2}개, 사라진 섹션 검사 {gone}"
              + ("" if (n2 == len(checks) - (len(date_secs) - 1) and len(gone) == len(date_secs) - 1) else "  ← MISS"))
        ok &= n2 == len(checks) - (len(date_secs) - 1)

        uncovered = [c for c in checks if c not in covered]
        print(f"\n== 커버리지: 기준 검사 {len(checks)}개 중 변조로 FAIL 확인 {len(covered)}개")
        for c in uncovered:
            print(f"  [UNCOVERED] {c} — 이 검사를 깨뜨리는 변조가 없다. 스크립트에 추가할 것")
        ok &= not uncovered

        # --- 원본 무결성 ---
        changed = [k for k, v in orig.items() if md5(v) != orig_md5[k]]
        print(f"\n원본 md5 대조: {'전부 동일' if not changed else '변경됨 ' + str(changed)}")
        ok &= not changed
        print("\n" + "=" * 50)
        print("전부 살아 있음." if ok else "문제 있음 — 위 [MISS]/[UNCOVERED]/[SKIP] 확인.")
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
