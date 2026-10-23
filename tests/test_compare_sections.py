#!/usr/bin/env python3
"""compare.py 구역별 try 시험 — 한 구역의 파싱 실패가 다른 구역 항목을 생략시키지 않는지(2026-10-06).

사용법: "$PY" tests/test_compare_sections.py <index.html> <compute.json>
  (index.html 은 그 compute.json 으로 compare DIFF 0 인 작업본 — 예: 리허설 work/R2/index.html + work/R2/compute.json)
동작: 사본만 만든다(원본 읽기 전용). 기준 실행(DIFF 0) 뒤 구역 하나의 서술 문단만 지운 사본 셋을 돌려
  ① DIFF 가 그 구역 항목뿐이고 ② 다른 구역의 기준 [OK] 항목이 전부 다시 [OK] 인지 본다.
  - 01 해석 문단(.note-mint) 삭제 · 07 ②③ 각주 블록 삭제(옛 '10 최근 7일·평균 문장 삭제'는 판 I 에서 지면 구역이 빠져 없앰)
  (2026-10-06 회차 2 — 레이아웃 판) 같은 방식으로 "그 구역 항목만 DIFF" 를 본다(파싱 실패가 아니라 값 DIFF):
  - 03 두 표의 날짜 행을 오름차순으로 되돌림(옛 배치 복귀) → "03 일별 표 전체 행" DIFF
  - (2026-10-15) 01 표 5행을 오름차순으로 되돌림(옛 배치 복귀) → "01 표 5일" DIFF
  - 07 summary 클릭 1건 개수 N → N+1(summary 만 옛 값) → "07 summary 클릭1건 개수" DIFF
  (2026-10-17 판 H — 07 정식표 접기, 작업본이 판 H 일 때만 — 아니면 [MISS])
  - 07 정식표 접힌 행 summary 의 클릭 합 M → M+1(summary 만 옛 값 — 시안 mut_c1_sum 유형) → "07 summary 정식표 나머지…" DIFF
  - 접힌 표 첫 행을 위 표 끝으로 옮김(이어 읽은 순서·값은 그대로) → "07 정식표 위 표 행수…" DIFF
  (2026-10-23 판 I — 콘텐츠 지면 빼기: 01 ③ 첫 문장 괄호)
  - 01 ③ 괄호의 콘텐츠 노출 합 N → N+1(글자만) → "01 ③ 괄호(…)" DIFF(괄호가 없는 작업본 — 콘텐츠 합 0 — 이면 [MISS])
  - 01 ③ 민트 줄 끝에 판 H 꼴 구절("콘텐츠 노출 N회는 9/6 이후 늘지 않음.")을 다시 붙임 → "01 ③ 옛 구절 0(…)" DIFF
  (2026-10-23 판 J — 불필요 항목 빼기: 새·고친 항목, 작업본이 판 J 일 때만 — 아니면 [MISS])
  - 07 정식표 '적음' 칸 하나를 클릭률 숫자로 되돌림 → "07 정식표 값(…)" DIFF
  - 04 회색 파워링크 비중 B → B+0.1(글자만) → "04 파워링크 비중"·"04 예산 비중 한 값(…)" DIFF
  - 04 민트 줄 격차 기준 플레이스 CPC +1(글자만) → "04 격차 기준(…)" DIFF
  - 08 note '비중 계산도 N 기준' N+1(고정 표지 숫자) → "08 각주 N회" DIFF
  - 09 콜아웃 2위 동률 시간 빼기(고정 표지 숫자) → "09 2위(동률 시간 포함)" DIFF(동률이 없는 작업본이면 [MISS])
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
    if head.startswith("10"):
        return "10·11"   # 판 I(2026-10-23) — 10 핵심 요약 · 10·11 금칙어
    if head == "11":
        return "11 장부·플레이스"
    return head.split("/")[0]


def section(html, n):
    s = html.find(f"<!-- Section {n}:")
    e = html.find(f"<!-- Section {n + 1}:")
    return s, (e if e != -1 else html.find("<script>", s))


def cut(html, n, pat):
    s, e = section(html, n)
    seg, k = re.subn(pat, "", html[s:e], count=1, flags=re.S)
    return html[:s] + seg + html[e:] if k == 1 else None


def reverse_rows(html, n):
    """n 구역의 날짜 행(합계 제외)을 DOM 전체 거꾸로 다시 늘어놓은 판(표 칸 수는 그대로 — 옛 apply 의 오름차순 복귀 흉내, 03 · 01)."""
    s, e = section(html, n)
    seg = html[s:e]
    trs = [m for m in re.finditer(r"<tr[^>]*>.*?</tr>", seg, re.S) if "<td" in m.group(0) and ">합계<" not in m.group(0)]
    if len(trs) < 2:
        return None
    new = [m.group(0) for m in trs][::-1]
    out, last = [], 0
    for m, t in zip(trs, new):
        out += [seg[last:m.start()], t]
        last = m.end()
    return html[:s] + "".join(out) + seg[last:] + html[e:]


def bump_mint_paren(html):
    """판 I 01 ③ 괄호의 콘텐츠 지면 노출 합 N → N+1(글자만 — compute 는 그대로). 괄호가 없으면(콘텐츠 노출 합 0 인 작업본) None."""
    s, e = section(html, 1)
    seg, k = re.subn(r"(콘텐츠 지면 노출 )([\d,]+)(회 포함)", lambda m: f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}", html[s:e], count=1)
    return html[:s] + seg + html[e:] if k == 1 else None


def restore_old_mint(html):
    """판 I 01 ③ 민트 줄 끝에 판 H 꼴 구절("콘텐츠 노출 N회는 9/6 이후 늘지 않음.")을 다시 붙인 판 — 복사된 옛 서술 흉내(첫 문장은 새 꼴 그대로 — DIFF 는 옛 구절 항목만)."""
    s, e = section(html, 1)
    seg, k = re.subn(r"(<!-- n:01-mint:매회차 -->.*?)(<!-- /n -->)", r"\1 콘텐츠 노출 1,746회는 9/6 이후 늘지 않음.\2", html[s:e], count=1, flags=re.S)
    return html[:s] + seg + html[e:] if k == 1 else None


def bump_click1_summary(html):
    s, e = section(html, 7)
    seg, k = re.subn(r"(클릭 1건 검색어 <span[^>]*>\()(\d+)(개 · 펼치기\))", lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", html[s:e], count=1)
    return html[:s] + seg + html[e:] if k == 1 else None


def bump_main07_summary(html):
    """판 H 07 정식표 접힌 행 summary "합 M건" → M+1(나머지가 0행이면 "나머지 0행" → "나머지 1행")."""
    s, e = section(html, 7)
    seg, k = re.subn(r"(<summary[^>]*>나머지 [\d,]+행\(클릭 [\d,~]+건 · 합 )([\d,]+)(건 · )", lambda m: f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}", html[s:e], count=1)
    if k == 0:
        seg, k = re.subn(r"(<summary[^>]*>나머지 )0(행 펼치기</summary>)", r"\g<1>1\g<2>", html[s:e], count=1)
    return html[:s] + seg + html[e:] if k == 1 else None


def move_first_fold_row_up(html):
    """판 H 접힌 표 첫 행을 위 표 끝으로 옮긴 판(이어 읽은 행 순서·값은 그대로 — 위 표 행 수만 K+1). 접힌 표가 비었으면 None."""
    s, e = section(html, 7)
    seg = html[s:e]
    i = seg.find('<summary class="fold-more">나머지 ')
    if i == -1:
        return None
    a = seg.index("<tbody>", i) + len("<tbody>")
    m = re.compile(r"\s*<tr[^>]*>.*?</tr>", re.S).match(seg, a)
    if not m:
        return None
    t1 = seg.index("</tbody>")   # 위 표 = 구역 첫 tbody
    row = m.group(0)
    seg = seg[:t1] + row.lstrip("\n") + "\n" + seg[t1:a] + seg[m.end():] if t1 < a else None
    return html[:s] + seg + html[e:] if seg else None


def sub_in(html, n, pat, rep, flags=0):
    """n 구역 안에서 pat 첫 일치를 rep 로(글자만) — 못 찾으면 None."""
    s, e = section(html, n)
    seg, k = re.subn(pat, rep, html[s:e], count=1, flags=flags)
    return html[:s] + seg + html[e:] if k == 1 else None


def unfew07(html):
    """판 J 07 정식표 '적음' 칸 하나 → '50.00%'(옛 꼴 — 노출 20회 미만 행에 클릭률 숫자)."""
    return sub_in(html, 7, r'<td class="num">적음</td>', '<td class="num">50.00%</td>')


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
                 ("01", "01 ③ 괄호 콘텐츠 노출 합 +1(글자만 — 판 I)", bump_mint_paren(H)),
                 ("01", "01 ③ 판 H 꼴 구절 끝에 다시 붙임(복사된 옛 서술 — 판 I)", restore_old_mint(H)),
                 ("03", "03 날짜 행 오름차순 복귀(옛 배치)", reverse_rows(H, 3)),
                 ("01", "01 표 5행 오름차순 복귀(옛 배치)", reverse_rows(H, 1)),
                 ("07", "07 summary 클릭 1건 개수 +1(summary 만 옛 값)", bump_click1_summary(H)),
                 ("07", "07 정식표 접힌 행 summary 클릭 합 +1(summary 만 옛 값 — 판 H)", bump_main07_summary(H)),
                 ("07", "07 접힌 표 첫 행을 위 표로 옮김(순서·값 그대로 — 판 H)", move_first_fold_row_up(H)),
                 ("07", "07 정식표 '적음' 칸을 클릭률 숫자로(판 J)", unfew07(H)),
                 ("04", "04 회색 파워링크 비중 +0.1(글자만 — 판 J)", sub_in(H, 4, r"(비중은 [\d.]+ → )([\d.]+)(%)", lambda m: f"{m.group(1)}{float(m.group(2)) + 0.1:.1f}{m.group(3)}")),
                 ("04", "04 민트 줄 격차 기준 플레이스 CPC +1(글자만 — 판 J)", sub_in(H, 4, r"(vs 플레이스 )([\d,]+)(원)", lambda m: f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}")),
                 ("08", "08 note '비중 계산도 N 기준' +1(고정 표지 숫자 — 판 J)", sub_in(H, 8, r"(비중 계산도 )([\d,]+)( 기준)", lambda m: f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}")),
                 ("09", "09 콜아웃 2위 동률 시간 빼기(고정 표지 숫자 — 판 J)", sub_in(H, 9, r"(2위는 \d+시 \d+건)으로 [\d시·]+와 같음", r"\1"))]
        want_diff = {"03 날짜 행 오름차순 복귀(옛 배치)": "03 일별 표 전체 행", "01 표 5행 오름차순 복귀(옛 배치)": "01 표 5일(5칸)", "07 summary 클릭 1건 개수 +1(summary 만 옛 값)": "07 summary 클릭1건 개수",
                     "07 정식표 접힌 행 summary 클릭 합 +1(summary 만 옛 값 — 판 H)": "07 summary 정식표 나머지(행·클릭 범위·합·비용) = compute 정식표[K:]",
                     "07 접힌 표 첫 행을 위 표로 옮김(순서·값 그대로 — 판 H)": "07 정식표 위 표 행수 = min(K, n)",
                     "01 ③ 괄호 콘텐츠 노출 합 +1(글자만 — 판 I)": "01 ③ 괄호(콘텐츠 기간·노출 합·검색 지면만 CTR — 합 0 이면 괄호 없음)",
                     "01 ③ 판 H 꼴 구절 끝에 다시 붙임(복사된 옛 서술 — 판 I)": "01 ③ 옛 구절 0(콘텐츠 지면 없는 날·검색 지면만 계산하면·콘텐츠 노출 N회는)",
                     "07 정식표 '적음' 칸을 클릭률 숫자로(판 J)": "07 정식표 값(뱃지 동률은 배포본 유지)",
                     "04 회색 파워링크 비중 +0.1(글자만 — 판 J)": "04 예산 비중 한 값(02 desc = 04 표 플레이스 행 · 04 회색 파워링크 = 100 − 그 값)",
                     "04 민트 줄 격차 기준 플레이스 CPC +1(글자만 — 판 J)": "04 격차 기준(파워링크 총비용 1위 그룹·CPC · 플레이스 CPC)",
                     "08 note '비중 계산도 N 기준' +1(고정 표지 숫자 — 판 J)": "08 각주 N회",
                     "09 콜아웃 2위 동률 시간 빼기(고정 표지 숫자 — 판 J)": "09 2위(동률 시간 포함)"}
        for sec, label, text in cases:
            if text is None:
                print(f"  [MISS] {label} — 지울 자리를 못 찾음(마크업이 바뀌었으면 이 시험을 고칠 것)")
                good = False
                continue
            rc, ok, diff = run(text, compute, work)
            wrong = [d for d in diff if section_of(d) != sec]
            lost = sorted(n for n in base_ok if section_of(n) != sec and n not in ok)
            other = sorted({section_of(n) for n in ok if section_of(n) != sec})
            res = rc == 1 and diff and not wrong and not lost and (label not in want_diff or want_diff[label] in diff)
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
