#!/usr/bin/env python3
"""
validate.py · archive.py 검사 생존 확인(파괴 실험).

사용법:
    "$PY" tests/mutation_test.py <배포본 index.html> <키워드CSV> <검색어CSV> <시간대별CSV> <상세지역CSV> [<잔액 기록 balance.json>]
    (판 F — 6번째 인자가 없으면 index.html 옆 balance.json. 사본으로만 validate 에 --balance 로 넘긴다)

동작:
  1. 스킬 저장소의 scripts/·config/·data/ 와 인자로 받은 index.html·CSV 4개를 임시 디렉토리에
     **복사**한다. 이후 모든 변조는 사본에만 한다. 원본 경로에는 쓰기 자체를 하지 않는다
     (원본은 읽기 전용으로 열고, 시작·종료 시 원본 md5(html·CSV 4·data/ 전부)를 대조해 변하지 않았음을 증명한다).
  2. 사본으로 validate.py를 돌려 기준 PASS를 만들고, 출력의 [PASS]/[FAIL] 줄을 세어
     **검사 목록을 실행 시점에 알아낸다**(개수를 이 파일에 적지 않는다).
  3. 검사마다 대응하는 변조(사본 한 곳만 바꾸기)를 적용해 그 검사가 FAIL로 바뀌는지 본다.
  4. 마크업이 바뀌어 검사 대상이 0건이 되는 경우를 흉내 내 0건 가드가 FAIL을 내는지 본다.
  5. config 사본의 값을 바꿔 검사가 설정을 실제로 읽는지 본다.
  6. 기준 목록의 검사 중 어떤 변조도 겨냥하지 않은 것이 있으면 UNCOVERED로 보고한다
     — 검사가 늘었는데 이 스크립트가 따라가지 못했다는 뜻이다.
  7. (2026-09-26) archive.py: data/ 사본에서 store 거부 2종·combine 검사 5종을 깨뜨려 [FAIL]로 멈추는지 본다.
  (2026-10-06 회차 2) "레이아웃 판": 변조 2(meta 값 변경 · 03 접기 하나 풀기) + 0건 가드 2(meta 제거 · 접기 전부 풀기 — 옛 모양 복원 흉내)
     + config 실험(report_layout.layout_id 를 바꾸면 기준 사본이 "레이아웃 판" FAIL — config 를 실제로 읽는지).
  (2026-10-06 판 C) "레이아웃 판": 변조 +1(분기 표지 주석 06 제거) + 0건 가드 +1(분기 도우미 M 줄 이름 변조 var M → var MX)
     + config 실험(report_layout.mobile.max_px 를 1 올리면 기준 사본이 "레이아웃 판" FAIL — M 줄·CSS 경계를 config 와 대조하는지).
  (2026-10-08 판 E) "레이아웃 판": 0건 가드 +1(01 모바일 터치 축 axis:'y' 지우기 — 판 D 꼴로 되돌림).
  (2026-10-09 판 F) "광고비 잔액 카드": 변조 4(카드 값 +1원 · 기준 시각 +1분 · 며칠분 +1 — 실패 기록이면 보조 줄 끝 글자 · 잔액 기록 읽은 시각을 집계 마지막 날로(지난 회차 기록))
     + 0건 가드 2(카드 표지 data-balance 지우기 → "광고비 잔액 카드" · "레이아웃 판" 각각).
  (2026-10-10 매출 작업 A·C) "01·10·11 서술에 장부 라벨+숫자 0"(판 I — 판 H 까지 01·11·12): 변조 1(10 첫 항목에 '장부 등록 1명') + 0건 가드 1(Section 1·10·11 주석 변조)
     + config 실험(leads.publish 를 counts 로 → 기준 사본 FAIL) / "11번 장부·플레이스 행": 변조 2(판정 낱말 config 밖 · 'M/D까지' 하루 앞) + 0건 가드 1(판정 문구 변조).
     기준 사본은 11번 장부 행이 있는 배포본(첫 적용 뒤)이어야 한다 — 첫 적용 전 배포본은 기준 실행에서 "11번 장부·플레이스 행" FAIL 로 멈춘다(기대값).
  (2026-10-23 판 I 콘텐츠 지면 빼기) 기준 사본은 판 I 배포본(구역 11 · 지면 구역 없음)이어야 한다 — 판 H 배포본은 기준 실행에서 "레이아웃 판"·"섹션 주석"·
     "화면 글 구역 번호" FAIL 로 멈춘다(기대값). 11·12번 변조는 10·11번으로 · "섹션 주석": 변조 +1(Section 12 주석 덧붙임 — 그 밖 번호) ·
     "레이아웃 판": 변조 +3(placementChart 캔버스 덧붙임 · 11 번호 배지 → 12 · ① 칸 머리 검색·콘텐츠 되살림) · "화면 글 구역 번호": 변조 3(다음 액션 표지 글에 '12번 행 없음' ·
     12-basis 를 'KPI·01~07·10번' 으로 되돌림 · 요약 표지에 '콘텐츠 지면 47일 연속 0') + 0건 가드 1(서술 표지 이름 꼴 변조 → 표지 0개).
  (2026-10-12 판 G 보고서 더 받기 A + B) index.html 옆 extra/(precheck 와 같은 work/extra — 추가 합본·원장 사본)를 사본으로 옮겨 validate 에 --extra 로 넘긴다
     (없으면 빈 폴더 — 카드가 '확인 못 함' 이어야 기준 PASS). "추가 카드·표": 변조 4(성별·연령대 표 첫 노출 +1 · 변경 기록 기간 끝 하루 뒤 · 스킬 등록 회수 +1 ·
     배포본에 아이디 꼴 `:naver` 주석) — 카드가 '확인 못 함' 이면 앞 셋은 SKIP + 0건 가드 2(변경 기록 블록 표지 지우기 → "추가 카드·표" · "레이아웃 판" 각각).
  (2026-10-23 판 J 불필요 항목 빼기) 기준 사본은 판 J 작업본(서술까지 판 J 꼴)이어야 한다 — 판 I 배포본은 기준 실행에서 "레이아웃 판"·"판 J 뺀 글 0"·"10번 항목 수·판정 줄" FAIL(기대값).
     "추가 카드·표": '스킬 등록 회수 +1' → '스킬 줄 되살림'(판 J 에서 뺀 줄) · "06번 카드 그룹"(새 검사): 변조 2(오래된 그룹 카드 되살림 · 04 이름 칸에 '(M/D 신규)' 되살림) ·
     "판 J 뺀 글 0"(새 검사): 변조 3(01 머리 줄 누적 CTR A → B · 10 변화 없음 줄에 숫자 · 11 note 정렬 줄) + 0건 가드 1(Section 3 주석 변조 → 구역 0자) ·
     "레이아웃 판": 변조 +2(KPI '업종 평균 수준' 되살림 · 09-call 표지 매회차로) · "07번 클릭률": 변조 +1('적음' 칸을 숫자로) · "10번 항목 수·판정 줄": 변조 +1(판정 줄 M/D 하루 앞) ·
     "05번 mediaChart": 변조 +1(콘텐츠 매체 MLB파크 5위 막대 되살림) · config 실험 +2(group_cards.promotion_groups 비움 → "06번 카드 그룹" FAIL · ctr_few_07.min_imps +1 → "레이아웃 판" FAIL).
  (2026-10-26 판 K 01 요일 카드) 기준 사본은 판 K 작업본(precheck 를 통과한 work/index.html — 옆에 compute.json)이어야 한다 — 판 J 배포본은 기준 실행에서 "레이아웃 판" FAIL(기대값).
     "레이아웃 판": 변조 +3(요일 캔버스 이름 변조 · 카드를 ① 박스 뒤로 · 차트 블록을 분기 도우미 앞으로) ·
     **compare 실험**(새 — 6b): index.html 옆 compute.json(precheck 의 재계산) 사본으로 기준 compare DIFF 0 → 변조 5(막대 노출 첫 칸 +1 · 클릭 첫 칸 +0.1 · 보조 줄 끝날 하루 앞 ·
     보조 줄 일수 +1 · compute 쪽 노출 첫 칸 +1)마다 겨냥한 "01 요일 카드 …" 항목만 DIFF · exit 1. 카드·compute.json 이 없으면 [MISS](통과 아님).
  (2026-10-27 판 L 하루예산 카드) 기준 사본은 판 L 작업본(precheck 를 통과한 work/index.html — 옆에 compute.json · balance.json(budget 포함) · extra/)이어야 한다.
     "하루예산 카드"(새 검사 24b): 변조 7(플레이스 값 +1원 · 최근 7일 +1 · 파워링크 캠페인 값 +1원 · summary 일수 +1 · 목록 첫 줄 시각 +1분(줄이 없으면 줄 하나 덧붙임) ·
     예산 기록 읽은 시각 = 집계 마지막 날 · 예산 기록의 플레이스 그룹 하루예산 +1,000원) + 0건 가드 2(data-budget 표지 지우기 → "하루예산 카드" · "레이아웃 판") ·
     "레이아웃 판": 변조 +2(하루예산 카드를 잔액 카드 앞으로 · 카드 뒤에 다른 카드) ·
     **compare 실험 6c**(index.html 옆 compute.json 사본): 변조 6(값 한도 +1 · 최근 7일 +1 · 보조 줄 멈춘 수 +1 · summary 일수 +1 · 목록 첫 줄 시각 · compute 쪽 플레이스 횟수 +1)마다
     겨냥한 "하루예산 카드 …" 항목만 DIFF · exit 1. 카드·compute.json 이 없으면 [MISS](통과 아님).

종료 코드: 0 = 전부 살아 있음(변조마다 겨냥한 검사가 FAIL, 미커버 검사 없음, archive 7종 FAIL, 원본 md5 동일), 1 = 아니면.
"""

import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔·Code 탭 파이프(cp949)에서 한글·기호(—) — 다른 시험·스크립트와 같은 방식
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
HEAD_RE = re.compile(r"\((\d{4})\.(\d{2})\.(\d{2})\.~(\d{4})\.(\d{2})\.(\d{2})\.\)")


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
    if e == -1:
        e = html.find("<script>", s)
    return html[s:e if e != -1 else len(html)] if s != -1 else ""


def replace_in_section(html, num, old, new):
    sec = section(html, num)
    if not sec or old not in sec:
        return None
    return html.replace(sec, sec.replace(old, new, 1), 1)


def csv_edit(text, row_idx, col_idx, delta=None, value=None):
    """기간 헤더(0행)·컬럼 헤더(1행) 다음 첫 데이터 행의 셀을 바꾼다(정수 delta 또는 값 교체)."""
    lines = text.split("\n")
    row = lines[row_idx].split(",")
    row[col_idx] = str(int(row[col_idx]) + delta) if delta is not None else value
    lines[row_idx] = ",".join(row)
    return "\n".join(lines)


def rewrite_head(text, start=None, end=None):
    """첫 줄 기간 헤더의 시작/끝 날짜를 바꾼다."""
    m = HEAD_RE.search(text.split("\n", 1)[0])
    s = start or date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    e = end or date(int(m.group(4)), int(m.group(5)), int(m.group(6)))
    return text.replace(m.group(0), f"({s:%Y.%m.%d.}~{e:%Y.%m.%d.})", 1)


def archive_experiments(work):
    """archive.py store/combine 파괴 실험 — 전부 사본. (이름, 준비 함수, 명령, 기대 메시지 조각)"""
    arch = os.path.join(work, "arch")
    pristine = os.path.join(work, "arch_pristine")
    for d in (arch, pristine):
        os.makedirs(d, exist_ok=True)
        shutil.copytree(os.path.join(REPO, "scripts"), os.path.join(d, "scripts"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(REPO, "config"), os.path.join(d, "config"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(REPO, "data"), os.path.join(d, "data"), dirs_exist_ok=True)
    data = os.path.join(arch, "data")
    months = sorted(os.listdir(data))
    last, first = months[-1], months[0]

    def reset():
        shutil.rmtree(data)
        shutil.copytree(os.path.join(pristine, "data"), data)

    def run(*args):
        r = subprocess.run([sys.executable, os.path.join(arch, "scripts", "archive.py"), *args], capture_output=True, text=True, encoding="utf-8")
        return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else ""

    def write(path, text):
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            f.write(text)

    kw = os.path.join(data, last, "키워드.csv")
    sr = os.path.join(data, last, "검색어.csv")
    hr = os.path.join(data, last, "시간대별.csv")
    up = os.path.join(work, "upload.csv")
    exps = []

    def p_old():
        t = read_sig(kw); m = HEAD_RE.search(t); s = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        write(up, rewrite_head(t, end=s + timedelta(days=1)))
    exps.append(("store: 옛 다운로드(기간 끝이 보관본보다 이름)", p_old, ("store", up), "앞섬"))

    def p_span():
        t = read_sig(kw); m = HEAD_RE.search(t); s = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        write(up, rewrite_head(t, start=(s.replace(day=1) - timedelta(days=5))))
    exps.append(("store: 두 달에 걸친 기간 헤더", p_span, ("store", up), "두 달에 걸침"))

    def p_hourly():
        t = read_sig(hr); col = t.split("\n")[1].split(",").index("노출수"); write(hr, csv_edit(t, 2, col, delta=1))
    exps.append(("combine: 시간대별 노출 +1(조각 합계 불일치)", p_hourly, ("combine", os.path.join(work, "c_h")), "≠ 키워드"))

    exps.append(("combine: 개업 달 폴더 제거", lambda: shutil.rmtree(os.path.join(data, first)), ("combine", os.path.join(work, "c_f")), "개업일"))

    def p_gap():
        t = read_sig(sr); m = HEAD_RE.search(t); s = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        write(sr, rewrite_head(t, start=s + timedelta(days=1)))
    exps.append(("combine: 검색어 헤더 시작일 +1(빈틈)", p_gap, ("combine", os.path.join(work, "c_g")), "빈틈 또는 겹침"))

    def p_split():
        t = read_sig(sr); head, body = t.split("\n", 1); m = HEAD_RE.search(head)
        s, e = date(int(m.group(1)), int(m.group(2)), int(m.group(3))), date(int(m.group(4)), int(m.group(5)), int(m.group(6)))
        cut = e - timedelta(days=1); lines = body.split("\n"); cols = lines[0]
        a = [l for l in lines[1:] if l and l.split(",")[2] <= f"{cut:%Y.%m.%d.}"]
        b = [l for l in lines[1:] if l and l.split(",")[2] > f"{cut:%Y.%m.%d.}"]
        write(sr, rewrite_head(head, end=cut) + "\n" + "\n".join([cols] + a) + "\n")
        write(os.path.join(data, last, "검색어_2.csv"), rewrite_head(head, start=cut + timedelta(days=1)) + "\n" + "\n".join([cols] + b) + "\n")
    exps.append(("combine: 검색어만 조각 경계 다르게(끝 하루 분리)", p_split, ("combine", os.path.join(work, "c_s")), "조각 경계"))

    exps.append(("combine: 검색어 보관본 한 종류 누락", lambda: os.remove(sr), ("combine", os.path.join(work, "c_m")), "검색어"))

    print("\n== archive.py 파괴 실험 (사본 data/ — 기준 combine PASS 뒤 7종 전부 FAIL이어야 함)")
    rc, last_line = run("combine", os.path.join(work, "c_base"))
    if rc != 0:
        print(f"  [MISS] 기준 combine이 PASS가 아님: {last_line}")
        return False
    print(f"  기준 combine PASS: {last_line}")
    ok = True
    for name, prep, cmd, expect in exps:
        reset(); prep()
        rc, last_line = run(*cmd)
        if rc == 1 and last_line.startswith("[FAIL]") and expect in last_line:
            print(f"  [OK]   {name} → {last_line[:110]}")
        else:
            ok = False
            print(f"  [MISS] {name} → exit {rc}: {last_line[:150]}")
    return ok


def compare_experiments(work, H, comp_src, cfg_path, cfg_text):
    """판 K(2026-10-26 01 요일 카드) — 요일 값 변조가 compare DIFF 로 잡히는지(그 항목만 · exit 1). 재료 = 배포본(작업본) 사본 + index.html 옆 compute.json
    (precheck 가 쓴 재계산) 사본 — 원본은 읽기만. 기준 compare DIFF 0 이어야 시작. 변조 = 막대 노출 첫 칸 +1 · 막대 위 클릭 첫 칸 +0.1(null 이면 0.0) ·
    보조 줄 끝날 하루 앞 · 보조 줄 일수 +1 · compute 쪽 노출 첫 칸 +1(재계산이 배포본과 다르면)."""
    print("\n== compare 실험(판 K 01 요일 카드 — 겨냥한 항목만 DIFF · exit 1 이어야 함)")
    if 'data-weekday="card"' not in H:
        print("  [MISS] 요일 카드가 없는 배포본 — 판 K 작업본(precheck 를 통과한 work/index.html)으로 돌릴 것")
        return False
    if not os.path.exists(comp_src):
        print(f"  [MISS] compute.json 없음({comp_src}) — precheck 가 작업본 옆에 쓴 재계산이 재료")
        return False
    with open(cfg_path, "w", encoding="utf-8") as f:   # 위 config 실험이 남긴 덮어쓰기를 되돌린다(사본 config = 원본 글)
        f.write(cfg_text)
    compare = os.path.join(work, "scripts", "compare.py")
    hp, jp = os.path.join(work, "cmp.html"), os.path.join(work, "cmp.json")
    base_j = read(comp_src)

    def run(html, js):
        for p, t in ((hp, html), (jp, js)):
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(t)
        r = subprocess.run([sys.executable, compare, hp, jp], capture_output=True, text=True, encoding="utf-8")
        return r.returncode, [l.strip()[len("[DIFF] "):] for l in r.stdout.splitlines() if l.strip().startswith("[DIFF]")]

    rc, d = run(H, base_j)
    if rc != 0 or d:
        print(f"  [MISS] 기준 compare DIFF {len(d)}(exit {rc}) — {d[:3]} · 배포본과 compute.json 이 맞는 조합인지 먼저 확인할 것")
        return False
    print("  기준 compare DIFF 0")
    i = H.index("getElementById('weekdayChart')")
    blk = H[i:H.index("</script>", i)]
    in_blk = lambda old, new: H[:i] + blk.replace(old, new, 1) + H[i + len(blk):]
    m_imp = re.search(r"(label:\s*'하루 평균 노출'\s*,\s*data:\s*\[)(\d+)", blk)
    m_clk = re.search(r"(clicks:\s*\[)(null|[\d.]+)", blk)
    m_sub = re.search(r'(data-weekday="sub">검색 지면 · \d+/\d+~)(\d+)/(\d+)( · 요일마다 )(\d+)((?:~\d+)?일</div>)', H)
    R2 = json.loads(base_j)
    R2["01"]["요일"]["노출"][0] += 1
    sub = lambda f: H.replace(m_sub.group(0), f(m_sub), 1) if m_sub else None
    cases = [("요일 노출 첫 칸 +1", "01 요일 카드 노출 7칸", in_blk(m_imp.group(0), f"{m_imp.group(1)}{int(m_imp.group(2)) + 1}") if m_imp else None, base_j),
             ("요일 클릭 첫 칸 +0.1(null 이면 0.0)", "01 요일 카드 클릭 7칸",
              in_blk(m_clk.group(0), m_clk.group(1) + ("0.0" if m_clk.group(2) == "null" else f"{float(m_clk.group(2)) + 0.1:.1f}")) if m_clk else None, base_j),
             ("보조 줄 끝날 하루 앞", "01 요일 카드 보조 줄",
              sub(lambda m: f"{m.group(1)}{m.group(2)}/{int(m.group(3)) - 1 if int(m.group(3)) > 1 else 2}{m.group(4)}{m.group(5)}{m.group(6)}"), base_j),
             ("보조 줄 일수 +1", "01 요일 카드 보조 줄", sub(lambda m: f"{m.group(1)}{m.group(2)}/{m.group(3)}{m.group(4)}{int(m.group(5)) + 1}{m.group(6)}"), base_j),
             ("compute 쪽 요일 노출 첫 칸 +1(재계산이 다르면)", "01 요일 카드 노출 7칸", H, json.dumps(R2, ensure_ascii=False, indent=1))]
    ok = True
    for name, target, html, js in cases:
        if html is None:
            print(f"  [SKIP] {name} — 변조 위치를 못 찾음(마크업이 바뀌었으면 이 스크립트를 고칠 것)")
            ok = False
            continue
        rc, d = run(html, js)
        hit, others = [x for x in d if x.startswith(target)], [x for x in d if not x.startswith(target)]
        if rc == 1 and hit and not others:
            print(f"  [OK]   {name} → DIFF: {hit[0][:100]}")
        else:
            ok = False
            print(f"  [MISS] {name} → exit {rc} · 겨냥 '{target}' {len(hit)}건 · 다른 DIFF {others[:3]}")
    return ok


def budget_compare_experiments(work, H, comp_src, cfg_path, cfg_text):
    """판 L(2026-10-27 하루예산 카드) — 카드 값 변조가 compare DIFF 로 잡히는지(그 항목만 · exit 1). 재료 = 배포본(작업본) 사본 + index.html 옆 compute.json 사본(읽기만).
    기준 compare DIFF 0 이어야 시작. 변조 = 값 한도 +1원 · 최근 7일 +1 · 보조 줄 멈춘 수 +1 · summary 일수 +1 · 목록 첫 줄 시각 +1분(줄이 없으면 줄 하나 덧붙임) · compute 쪽 플레이스 횟수 +1."""
    print("\n== compare 실험(판 L 하루예산 카드 — 겨냥한 항목만 DIFF · exit 1 이어야 함)")
    if 'data-budget="card"' not in H:
        print("  [MISS] 하루예산 카드가 없는 배포본 — 판 L 작업본(precheck 를 통과한 work/index.html)으로 돌릴 것")
        return False
    if not os.path.exists(comp_src):
        print(f"  [MISS] compute.json 없음({comp_src}) — precheck 가 작업본 옆에 쓴 재계산이 재료")
        return False
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(cfg_text)
    compare = os.path.join(work, "scripts", "compare.py")
    hp, jp = os.path.join(work, "cmpb.html"), os.path.join(work, "cmpb.json")
    base_j = read(comp_src)

    def run(html, js):
        for p_, t in ((hp, html), (jp, js)):
            with open(p_, "w", encoding="utf-8", newline="") as f:
                f.write(t)
        r = subprocess.run([sys.executable, compare, hp, jp], capture_output=True, text=True, encoding="utf-8")
        return r.returncode, [l.strip()[len("[DIFF] "):] for l in r.stdout.splitlines() if l.strip().startswith("[DIFF]")]

    rc, d = run(H, base_j)
    if rc != 0 or d:
        print(f"  [MISS] 기준 compare DIFF {len(d)}(exit {rc}) — {d[:3]} · 배포본과 compute.json 이 맞는 조합인지 먼저 확인할 것")
        return False
    R = json.loads(base_j)
    if R.get("예산", {}).get("상태") != "ok" or R["예산"]["멈춤"]["상태"] != "ok" or not R["예산"]["멈춤"].get("플레이스"):
        print("  [MISS] compute 예산·멈춤이 ok 가 아님 — 값 변조 실험은 예산·원장 사본이 있는 작업본으로")
        return False
    print("  기준 compare DIFF 0")
    sub1 = lambda pat, f: (lambda m: H.replace(m.group(0), f(m), 1) if m else None)(re.search(pat, H))
    R2 = json.loads(base_j)
    R2["예산"]["멈춤"]["플레이스"]["횟수"] += 1
    row = re.search(r'(data-budget="list">\n)(\s*<div><span>)(\d+/\d+\([^)]\) \d{2}):(\d{2})', H)
    cases = [("값 한도 +1원", "하루예산 카드 값", sub1(r'(data-budget="value">플레이스 )([\d,]+)(<span)', lambda m: f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}"), base_j),
             ("최근 7일 +1", "하루예산 카드 값", sub1(r"(최근 7일 )(\d+)(번 멈춤)", lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}"), base_j),
             ("보조 줄 멈춘 수 +1", "하루예산 카드 보조 줄", sub1(r'(data-budget="sub">[^<]* · 멈춤 )(\d+)(번</div>)', lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}"), base_j),
             ("summary 일수 +1", "하루예산 카드 summary", sub1(r'(data-budget="summary">[^<]*? 뒤 )(\d+)(일 중)', lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}"), base_j),
             ("목록 첫 줄 시각 +1분(줄이 없으면 줄 하나 덧붙임)", "하루예산 카드 목록",
              H.replace(row.group(0), f"{row.group(1)}{row.group(2)}{row.group(3)}:{(int(row.group(4)) + 1) % 60:02d}", 1) if row else
              H.replace('data-budget="list">\n', 'data-budget="list">\n          <div><span>1/1(목) 00:00</span><span>하루예산 1원</span></div>\n', 1)
              if 'data-budget="list">\n' in H else None, base_j),
             ("compute 쪽 플레이스 횟수 +1(재계산이 다르면)", "하루예산 카드 summary", H, json.dumps(R2, ensure_ascii=False, indent=1))]
    ok = True
    for name, target, html, js in cases:
        if html is None:
            print(f"  [SKIP] {name} — 변조 위치를 못 찾음(마크업이 바뀌었으면 이 스크립트를 고칠 것)")
            ok = False
            continue
        rc, d = run(html, js)
        hit, others = [x for x in d if x.startswith(target)], [x for x in d if not x.startswith(target)]
        if rc == 1 and hit and not others:
            print(f"  [OK]   {name} → DIFF: {hit[0][:100]}")
        else:
            ok = False
            print(f"  [MISS] {name} → exit {rc} · 겨냥 '{target}' {len(hit)}건 · 다른 DIFF {others[:3]}")
    return ok


def main():
    if len(sys.argv) not in (6, 7):
        sys.exit(__doc__)
    orig = dict(zip(["html", "kw", "sr", "hr", "rg"], sys.argv[1:6]))
    bal_src = sys.argv[6] if len(sys.argv) == 7 else os.path.join(os.path.dirname(os.path.abspath(orig["html"])), "balance.json")
    bal_base = read(bal_src) if os.path.exists(bal_src) else None
    comp_src = os.path.join(os.path.dirname(os.path.abspath(orig["html"])), "compute.json")   # 판 K compare 실험 재료(precheck 가 작업본 옆에 쓴 재계산 — 읽기만)
    extra_src = os.path.join(os.path.dirname(os.path.abspath(orig["html"])), "extra")   # 판 G 추가 합본(precheck 와 같은 자리 — 없으면 빈 폴더)   # 판 F 잔액 기록(없으면 기준 실행이 "광고비 잔액 카드" FAIL — 아래에서 멈춘다)
    data_files = sorted(glob.glob(os.path.join(REPO, "data", "*", "*.csv")))
    orig_md5 = {k: md5(v) for k, v in orig.items()}
    data_md5 = {p: md5(p) for p in data_files}

    work = tempfile.mkdtemp(prefix="saero-mut-")
    try:
        # --- 1. 전부 사본으로 ---
        shutil.copytree(os.path.join(REPO, "scripts"), os.path.join(work, "scripts"))
        shutil.copytree(os.path.join(REPO, "config"), os.path.join(work, "config"))
        validate = os.path.join(work, "scripts", "validate.py")
        extra_w = os.path.join(work, "extra")
        if os.path.isdir(extra_src):
            shutil.copytree(extra_src, extra_w)
        else:
            os.makedirs(extra_w)
        cfg_path = os.path.join(work, "config", "report-config.json")
        cfg_text = read(cfg_path)
        cfg = json.loads(cfg_text)
        base = {k: read_sig(v) if k != "html" else read(v) for k, v in orig.items()}
        print(f"작업 디렉토리 {work} (원본에는 쓰지 않음)")

        def run(html=None, csv=None, cfg_override=None, bal=None):
            paths = {}
            bal_p = os.path.join(work, "balance.json")
            if bal is not None or bal_base is not None:
                with open(bal_p, "w", encoding="utf-8") as f:
                    f.write(bal if bal is not None else bal_base)
            elif os.path.exists(bal_p):
                os.remove(bal_p)
            for k in orig:
                p = os.path.join(work, f"{k}.{'html' if k == 'html' else 'csv'}")
                src = (html if (k == "html" and html is not None) else (csv or {}).get(k, base[k]))
                with open(p, "w", encoding="utf-8" if k == "html" else "utf-8-sig") as f:
                    f.write(src)
                paths[k] = p
            with open(cfg_path, "w", encoding="utf-8") as f:
                f.write(cfg_override if cfg_override else cfg_text)
            r = subprocess.run([sys.executable, validate, paths["html"], paths["kw"], paths["sr"], paths["hr"], paths["rg"], "--balance", bal_p, "--extra", extra_w],
                               capture_output=True, text=True, encoding="utf-8")
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
        s7, s1, s6, s11 = section(H, 7), section(H, 1), section(H, 6), section(H, 10)   # s11 = 핵심 요약(판 I 10번 — 판 H 까지 11번, 변수 이름 그대로)
        date_secs = [int(n) for n in cfg["chart_min_width"]["date_based_sections"]]
        sr_cols = base["sr"].split("\n")[1].split(",")

        # --- 3. 변조 목록: (이름, 겨냥하는 검사명 조각, 변조 결과) ---
        muts = []
        muts.append(("태그 짝: 첫 </div> 제거", "태그 짝", {"html": H.replace("</div>", "", 1)}))

        m = re.search(r'(<td class="num">[\d,]+</td>\s*<td class="num">)(\d+)(</td>\s*<td class="num[^"]*">[\d.]+%</td>)', s7)
        muts.append(("07 정식표 첫 행 클릭 −1", "07번 클릭수 합계",
                     {"html": replace_in_section(H, 7, m.group(0), f"{m.group(1)}{int(m.group(2)) - 1}{m.group(3)}") if m else None}))

        hr_lines = base["hr"].split("\n")
        clk_col = hr_lines[1].split(",").index("클릭수")
        muts.append(("시간대별 CSV 첫 행 클릭 −1", "09번 시간대별 클릭 합계", {"csv": {"hr": csv_edit(base["hr"], 2, clk_col, -1)}}))

        muts.append(("07 첫 .ctr-high 제거", "07번 클릭률", {"html": replace_in_section(H, 7, 'class="num ctr-high"', 'class="num"')}))
        muts.append(("01 첫 .ctr-high 제거", "01번 클릭률", {"html": replace_in_section(H, 1, 'class="num ctr-high"', 'class="num"')}))

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
                     {"html": H.replace(m.group(0), m.group(0).replace(m.group(1) + ",", "", 1).replace(m.group(1) + " ,", "", 1), 1) if m else None}))

        muts.append(("Section 5 주석 변조", "섹션 주석", {"html": H.replace("<!-- Section 5:", "<!-- Sect 5:", 1)}))

        m = re.search(r"(와 )(\d+)(회 차이)", H)
        muts.append(("08 각주 N회 +1", "08·09번 각주", {"html": H.replace(m.group(0), f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", 1) if m else None}))

        rg_lines = base["rg"].split("\n")
        imp_col = rg_lines[1].split(",").index("노출수")
        muts.append(("상세지역 CSV 첫 행 노출 +1", "상세지역 CSV 노출 합계", {"csv": {"rg": csv_edit(base["rg"], 2, imp_col, 1)}}))

        # (2026-09-26 추가) 05 top5 · 06 카드 · 경쟁사 2종 · 검색어 클릭합 · 10번(판 H 까지 11번) 2종
        i = H.find("getElementById('mediaChart')")
        m = re.search(r"(data:\s*\[)(\d+)(,)", H[i:]) if i != -1 else None
        muts.append(("05 mediaChart 첫 값 +1", "05번 mediaChart",
                     {"html": H[:i] + H[i:].replace(m.group(0), f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", 1) if m else None}))

        m = re.search(r'(font-weight:800;color:var\(--mint-dark\);">)([\d.]+)(위)', s6)
        muts.append(("06 첫 카드 큰 숫자 +0.01", "06번 카드",
                     {"html": replace_in_section(H, 6, m.group(0), f"{m.group(1)}{float(m.group(2)) + 0.01:.2f}{m.group(3)}") if m else None}))

        muts.append(("검색어 CSV 첫 행 검색어를 config 경쟁사명 포함으로", "경쟁사표 밖",
                     {"csv": {"sr": csv_edit(base["sr"], 2, sr_cols.index("검색어"), value=f"{cfg['competitors'][0]}변조")}}))

        i = s7.find("경쟁사 브랜드명")
        m = re.search(r'(<td class="num">)(\d+)(</td>)', s7[i:]) if i != -1 else None
        muts.append(("07 경쟁사표 첫 행 노출 +1", "경쟁사표 노출·클릭",
                     {"html": H.replace(s7, s7[:i] + s7[i:].replace(m.group(0), f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", 1), 1) if m else None}))

        muts.append(("검색어 CSV 첫 행 클릭 −1", "검색어 CSV 클릭 합계", {"csv": {"sr": csv_edit(base["sr"], 2, sr_cols.index("클릭수"), -1)}}))

        m = re.search(r"(항목 판정: 유지 )(\d+)", s11)
        muts.append(("10 판정 줄 유지 +1", "10번 항목 수",
                     {"html": replace_in_section(H, 10, m.group(0), f"{m.group(1)}{int(m.group(2)) + 1}") if m else None}))
        muts.append(("10 첫 항목에 금칙어 삽입", "10·11번 금칙어", {"html": replace_in_section(H, 10, "<li><b>", "<li><b>필요 ")}))
        muts.append(("11 첫 항목에 잔존 문구 삽입", "잔존 문구", {"html": replace_in_section(H, 11, "<td><span class=\"tag tag-mint\">", "<td>확인 요청 <span class=\"tag tag-mint\">")}))
        # (2026-10-23 판 I 콘텐츠 지면 빼기) 섹션 주석 그 밖 번호 · 레이아웃 판(지면 흔적 · 배지 · ① 칸 머리) · 화면 글 구역 번호(옛 12번 · 지면 10번 · 옛 지면 글)
        muts.append(("Section 12 주석 덧붙임(그 밖 번호)", "섹션 주석", {"html": H.replace("\n<script>", "\n<!-- Section 12: x -->\n<script>", 1) if "\n<script>" in H else None}))
        muts.append(("placementChart 캔버스 덧붙임", "레이아웃 판", {"html": H.replace('<canvas id="hourlyChart"></canvas>', '<canvas id="hourlyChart"></canvas><canvas id="placementChart"></canvas>', 1) if '<canvas id="hourlyChart"></canvas>' in H else None}))
        muts.append(("11 번호 배지 → 12", "레이아웃 판", {"html": H.replace('<span class="section-num">11</span>', '<span class="section-num">12</span>', 1) if '<span class="section-num">11</span>' in H else None}))
        muts.append(("01 ① 칸 머리 검색·콘텐츠 되살림", "레이아웃 판",
                     {"html": replace_in_section(H, 1, '<th class="num">노출</th>\n', '<th class="num">노출</th>\n            <th class="num">검색</th>\n            <th class="num">콘텐츠</th>\n')}))
        m = re.search(r"(<!-- n:12-note:매회차 -->)", H)
        muts.append(("다음 액션 표지 글에 '(12번 행 없음)'", "화면 글 구역 번호", {"html": H.replace(m.group(1), m.group(1) + "(12번 행 없음) ", 1) if m else None}))
        muts.append(("12-basis 를 'KPI·01~07·10번' 으로 되돌림", "화면 글 구역 번호", {"html": H.replace("KPI·01~07번에서 제외", "KPI·01~07·10번에서 제외", 1) if "KPI·01~07번에서 제외" in H else None}))
        m = re.search(r"(<!-- n:11-list:매회차 --><ul>\s*<li>)", H)
        muts.append(("요약 표지에 '콘텐츠 지면 47일 연속 0'", "화면 글 구역 번호", {"html": H.replace(m.group(1), m.group(1) + "콘텐츠 지면 47일 연속 0 · ", 1) if m else None}))
        # (2026-10-06 추가) 07 각주 세 자리 — 변조 1 + 아래 0건 가드 2
        muts.append(("07 각주 ② 문구 변조(제외 검색어: → 제외검색어:)", "07 각주 세 자리", {"html": replace_in_section(H, 7, "제외 검색어:", "제외검색어:")}))
        # (2026-10-06 회차 2) 레이아웃 판 — 변조 2 + 아래 0건 가드 2 + config 실험
        lid = cfg["report_layout"]["layout_id"]
        meta = f'<meta name="report-layout" content="{lid}">'
        muts.append(("레이아웃 판 meta 값 변경", "레이아웃 판", {"html": H.replace(meta, meta.replace(lid, lid + "-변조"), 1) if meta in H else None}))

        def unfold(text):  # details/summary → 머리글 div(글자·속성 그대로) + 짝 </details> 제거 — 안 내용·앵커 문구는 그대로(옛 모양으로 "복원" 흉내)
            return re.sub(r"</details>", "", re.sub(r"<details(?:\s[^>]*)?>\s*<summary((?:\s[^>]*)?)>(.*?)</summary>", r"<div\1>\2</div>", text, flags=re.S))
        s3 = section(H, 3)
        muts.append(("03 접기 하나 풀기(details → 펼친 표)", "레이아웃 판", {"html": H.replace(s3, unfold(s3), 1) if "<details" in s3 else None}))
        # (2026-10-06 판 C) 분기 표지 주석 06 제거 → 분기 표지 1 ≠ config 2
        br06 = "/* saero:mobile-branch 06 */"
        muts.append(("판 C 분기 표지 06 주석 제거", "레이아웃 판", {"html": H.replace(br06, "", 1) if H.count(br06) == 1 else None}))

        # (2026-10-09 판 F) 광고비 잔액 카드 — 값 +1원 · 기준 시각 +1분 · 며칠분 +1(실패 기록이면 보조 줄 글자) · 잔액 기록을 지난 회차 것으로(읽은 날 = 집계 마지막 날)
        m = re.search(r'(<div class="value" data-balance="value">)([\d,]+)(<span class="unit">)', H)
        fail_v = 'data-balance="value">확인 못 함<'   # 실패 기록 회차의 카드 — 옛 값이 들어간 꼴로 변조
        muts.append(("잔액 카드 값 +1원(실패 기록이면 '확인 못 함' → 0원)", "광고비 잔액 카드",
                     {"html": H.replace(m.group(0), f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}", 1) if m else
                      (H.replace(fail_v, 'data-balance="value">0<span class="unit">원</span><', 1) if fail_v in H else None)}))
        m = re.search(r'(<div class="sub" data-balance="sub">[^<]*? )(\d{2}):(\d{2})( [^<]*</div>)', H)
        muts.append(("잔액 카드 기준 시각 +1분", "광고비 잔액 카드",
                     {"html": H.replace(m.group(0), f"{m.group(1)}{m.group(2)}:{(int(m.group(3)) + 1) % 60:02d}{m.group(4)}", 1) if m else None}))
        m = re.search(r'(<div class="sub" data-balance="sub">[^<]*약 )([\d,]+)(일분</div>)', H) or re.search(r'(<div class="sub" data-balance="sub">[^<]*)()(</div>)', H)
        muts.append(("잔액 카드 며칠분 +1(없으면 보조 줄 끝 글자)", "광고비 잔액 카드",
                     {"html": H.replace(m.group(0), f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1 if m.group(2) else '!'}{m.group(3)}", 1) if m else None}))
        stale = None
        if bal_base:
            from datetime import datetime as _dt
            _rec = json.loads(bal_base)
            _last = max(re.findall(r"(\d{4}\.\d{2}\.\d{2})\.", base["kw"].split("\n", 2)[2]))   # 키워드 CSV 일별 최댓값 = 집계 마지막 날
            _rec["read_at"] = _dt.strptime(_last, "%Y.%m.%d").strftime("%Y-%m-%dT23:59:00+09:00")
            stale = json.dumps(_rec, ensure_ascii=False)
        muts.append(("잔액 기록 읽은 시각 = 집계 마지막 날(지난 회차 기록)", "광고비 잔액 카드", {"html": H if stale else None, "bal": stale}))
        # (2026-10-10 매출 작업 A·C) 장부 라벨+숫자 삽입(01·10·11) · 11번 장부 판정 낱말 밖 · 장부 행 'M/D까지' 하루 앞
        muts.append(("10 첫 항목에 장부 숫자 삽입(등록 1명)", "장부 라벨+숫자", {"html": replace_in_section(H, 10, "<li><b>", "<li><b>장부 등록 1명 · ")}))
        m = re.search(r"(장부 기준 판정 = )([^<]+)(</b>)", H)
        muts.append(("11 장부 판정 낱말을 config 밖으로(좋아질 듯)", "11번 장부·플레이스 행", {"html": H.replace(m.group(0), f"{m.group(1)}좋아질 듯{m.group(3)}", 1) if m else None}))
        m = re.search(r"(\d+)/(\d+)(까지 장부 기준 판정 = )", H)
        muts.append(("11 장부 행 'M/D까지' 하루 앞(지난 회차 날짜)", "11번 장부·플레이스 행",
                     {"html": H.replace(m.group(0), f"{m.group(1)}/{int(m.group(2)) - 1 or 1}{m.group(3)}", 1) if m and int(m.group(2)) > 1 else None}))

        # (2026-10-12 판 G) 추가 카드·표 — 성별·연령대 첫 노출 +1 · 변경 기록 기간 끝 하루 뒤 · 스킬 등록 회수 +1 · 아이디 꼴 주석
        ga = H[H.find("<!-- saero:extra gender-age -->"):H.find("<!-- /saero:extra gender-age -->")]
        m = re.search(r'(<td class="name-cell">[^<]+</td>\s*<td class="num">)([\d,]+)(</td>)', ga)
        muts.append(("성별·연령대 표 첫 노출 +1", "추가 카드·표", {"html": H.replace(ga, ga.replace(m.group(0), f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}", 1), 1) if m else None}))
        m = re.search(r"(\((?:\d+/\d+)~)(\d+)/(\d+)( 기록)", H)
        muts.append(("변경 기록 기간 끝 하루 뒤", "추가 카드·표", {"html": H.replace(m.group(0), f"{m.group(1)}{m.group(2)}/{int(m.group(3)) + 1}{m.group(4)}", 1) if m else None}))
        muts.append(("스킬 줄 되살림(판 J 에서 뺀 줄)", "추가 카드·표",
                     {"html": H.replace("<!-- /saero:extra history -->", '<div class="note">스킬 제외 검색어 등록 28회(실행 수) · 삭제 3건</div>\n    <!-- /saero:extra history -->', 1)
                      if "<!-- /saero:extra history -->" in H and "확인 못 함 —" not in H[H.find("<!-- saero:extra history -->"):H.find("<!-- /saero:extra history -->")] else None}))
        muts.append(("배포본에 아이디 꼴 주석(:naver)", "추가 카드·표", {"html": H.replace("</body>", "<!-- x:naver --></body>", 1) if "saero:extra" in H else None}))

        # (2026-10-23 판 J) 06 카드 규칙 · 뺀 글 0 · 레이아웃 판 J 고정 글 · 07 '적음' · 판정 줄 M/D · 05 검색 지면 막대
        m = re.search(r'(\n    <div class="card" style="margin-top:12px;">\n.*?\n    </div>\n)', s6, re.S)
        muts.append(("06 오래된 그룹 카드 되살림(카드 규칙 밖)", "06번 카드 그룹",
                     {"html": H.replace(s6, s6.replace(m.group(1), m.group(1) + re.sub(r'">(\S+) <span style="color:var\(--mint-dark\)', '">노원산전필라테스 <span style="color:var(--mint-dark)', m.group(1)[1:], count=1), 1), 1) if m else None}))
        m = re.search(r'(<td class="name-cell">)(노원산전필라테스|[^<]+?)(</td>)', section(H, 4))
        muts.append(("04 이름 칸에 '(M/D 신규)' 되살림(등록 뒤 10일 넘은 그룹)", "06번 카드 그룹",
                     {"html": replace_in_section(H, 4, m.group(0), f'{m.group(1)}{m.group(2)} <span style="font-weight:400;color:var(--mint-dark);font-size:11px;">(9/2 신규)</span>{m.group(3)}') if m and "플레이스" not in m.group(2) else None}))
        m = re.search(r"(<!-- n:01-desc:매회차 -->[^<]*?)(<!-- /n -->)", H)
        muts.append(("01 머리 줄에 '누적 CTR A → B' 되살림", "판 J 뺀 글", {"html": H.replace(m.group(0), m.group(1) + ", 누적 CTR 3.34 → 3.34%" + m.group(2), 1) if m else None}))
        m = re.search(r"(변화 없음</b> — )", s11)
        muts.append(("10 변화 없음 줄에 숫자", "판 J 뺀 글", {"html": replace_in_section(H, 10, m.group(1), m.group(1) + "모바일 비중 79.6% · ") if m else None}))
        m = re.search(r"(<!-- n:12-note:매회차 -->)", H)
        muts.append(("11 note 에 정렬 줄 되살림", "판 J 뺀 글", {"html": H.replace(m.group(1), m.group(1) + "· <b>정렬</b>: 1번은 맨 위<br>", 1) if m else None}))
        m = re.search(r'(<div class="label">평균 클릭률</div>\s*<div class="value">[^\n]*</div>\n)', H)
        muts.append(("KPI '업종 평균 수준' 되살림", "레이아웃 판", {"html": H.replace(m.group(1), m.group(1) + '      <div class="sub">업종 평균 수준</div>\n', 1) if m else None}))
        muts.append(("09-call 표지 매회차로", "레이아웃 판", {"html": H.replace("<!-- n:09-call:고정 -->", "<!-- n:09-call:매회차 -->", 1) if "<!-- n:09-call:고정 -->" in H else None}))
        muts.append(("07 '적음' 칸을 클릭률 숫자로", "07번 클릭률", {"html": replace_in_section(H, 7, '<td class="num">적음</td>', '<td class="num">50.00%</td>')}))
        m = re.search(r"(\d+)/(\d+)(까지 지난 회차 10번)", s11)
        muts.append(("10 판정 줄 'M/D까지' 하루 앞", "10번 항목 수", {"html": replace_in_section(H, 10, m.group(0), f"{m.group(1)}/{int(m.group(2)) - 1 or 1}{m.group(3)}") if m and int(m.group(2)) > 1 else None}))
        i = H.find("getElementById('mediaChart')")
        blk5 = H[i:H.find("new Chart", i + 10)] if i != -1 else ""
        mm = re.search(r"(labels:\s*\[)(.*?)(\],\n)", blk5, re.S)
        md5_ = re.search(r"(label:\s*'노출수'[^\n]*\n\s*data:\s*\[)([^\]]*)(\])", blk5)
        mc = re.search(r"(backgroundColor:\s*\[)([^\]]*)(\])", blk5)
        b5 = (blk5.replace(mm.group(0), f"{mm.group(1)}{mm.group(2)},['MLB파크','모바일']{mm.group(3)}", 1).replace(md5_.group(0), f"{md5_.group(1)}{md5_.group(2)}, 828{md5_.group(3)}", 1)
              .replace(mc.group(0), f"{mc.group(1)}{mc.group(2)}, mint{mc.group(3)}", 1)) if mm and md5_ and mc else None
        muts.append(("05 콘텐츠 매체 MLB파크 5위 막대 되살림", "05번 mediaChart", {"html": H.replace(blk5, b5, 1) if b5 else None}))
        # (2026-10-26 판 K) 01 요일 카드 — 캔버스 이름 변조(표지 수) · 카드를 ① 박스 뒤로 · 차트 블록을 분기 도우미 앞으로 → "레이아웃 판"(값은 아래 compare 실험)
        wcard = re.search(r'\n    <div class="card" data-weekday="card".*?\n    </div>\n', H, re.S)
        wblk = re.search(r"\n// 8\. Weekday average.*?\n\}\)\(\);\n", H, re.S)
        muts.append(("요일 카드 캔버스 이름 변조(weekdayChart → weekdayChartX)", "레이아웃 판",
                     {"html": H.replace('<canvas id="weekdayChart">', '<canvas id="weekdayChartX">', 1) if '<canvas id="weekdayChart">' in H else None}))
        muts.append(("요일 카드를 ① 박스 뒤로(01 구역 끝)", "레이아웃 판",
                     {"html": H.replace(wcard.group(0), "\n", 1).replace("  <!-- Section 2:", wcard.group(0)[1:] + "  <!-- Section 2:", 1) if wcard else None}))
        muts.append(("요일 차트 블록을 분기 도우미 앞으로", "레이아웃 판",
                     {"html": H.replace(wblk.group(0), "\n", 1).replace("/* saero:mobile-helper", wblk.group(0)[1:] + "/* saero:mobile-helper", 1) if wblk else None}))
        # (2026-10-27 판 L) 하루예산 카드 — 화면 값 변조 5 · 예산 기록 변조 2 → "하루예산 카드"(독립 재셈) · 자리 변조 2 → "레이아웃 판"
        bcard = re.search(r'    <div class="kpi kpi-wide" data-budget="card".*?\n    </div>\n', H, re.S)
        bal_c = re.search(r'    <div class="kpi kpi-wide" style="--accent:#1c2b2a;">\n[^\n]*\n      <div class="label">광고비 잔액</div>.*?\n    </div>\n', H, re.S)
        def hsub(pat, f):
            m = re.search(pat, H)
            return H.replace(m.group(0), f(m), 1) if m else None
        muts.append(("하루예산 카드 플레이스 값 +1원", "하루예산 카드 =",
                     {"html": hsub(r'(data-budget="value">플레이스 )([\d,]+)(<span)', lambda m: f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}")}))
        muts.append(("하루예산 카드 최근 7일 멈춘 수 +1", "하루예산 카드 =", {"html": hsub(r"(최근 7일 )(\d+)(번 멈춤)", lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}")}))
        muts.append(("하루예산 카드 파워링크 캠페인 값 +1원", "하루예산 카드 =",
                     {"html": hsub(r'(data-budget="sub">파워링크 )([\d,]+)(원)', lambda m: f"{m.group(1)}{int(m.group(2).replace(',', '')) + 1:,}{m.group(3)}")}))
        muts.append(("하루예산 카드 summary 일수 +1", "하루예산 카드 =", {"html": hsub(r'(data-budget="summary">[^<]*? 뒤 )(\d+)(일 중)', lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}")}))
        brow = re.search(r'(data-budget="list">\n\s*<div><span>\d+/\d+\([^)]\) \d{2}):(\d{2})', H)
        muts.append(("하루예산 카드 목록 첫 줄 시각 +1분(줄이 없으면 줄 하나 덧붙임)", "하루예산 카드 =",
                     {"html": H.replace(brow.group(0), f"{brow.group(1)}:{(int(brow.group(2)) + 1) % 60:02d}", 1) if brow else
                      (H.replace('data-budget="list">\n', 'data-budget="list">\n          <div><span>1/1(목) 00:00</span><span>하루예산 1원</span></div>\n', 1) if 'data-budget="list">\n' in H else None)}))
        bstale = bmore = None
        if bal_base and '"budget"' in bal_base:
            from datetime import datetime as _dt
            _rec = json.loads(bal_base)
            if isinstance(_rec.get("budget"), dict):
                _last = max(re.findall(r"(\d{4}\.\d{2}\.\d{2})\.", base["kw"].split("\n", 2)[2]))
                _s = json.loads(bal_base)
                _s["budget"]["read_at"] = _dt.strptime(_last, "%Y.%m.%d").strftime("%Y-%m-%dT23:59:00+09:00")
                bstale = json.dumps(_s, ensure_ascii=False)
                _m = json.loads(bal_base)
                for _c in (_m["budget"].get("campaigns") or []):
                    if _c.get("type") == "PLACE":
                        for _g in _c["groups"]:
                            _g["dailyBudget"] = int(_g["dailyBudget"]) + 1000
                bmore = json.dumps(_m, ensure_ascii=False) if _m != _rec else None
        muts.append(("예산 기록 읽은 시각 = 집계 마지막 날(지난 회차 기록)", "하루예산 카드 =", {"html": H if bstale else None, "bal": bstale}))
        muts.append(("예산 기록의 플레이스 그룹 하루예산 +1,000원(카드는 그대로)", "하루예산 카드 =", {"html": H if bmore else None, "bal": bmore}))
        muts.append(("하루예산 카드를 잔액 카드 앞으로", "레이아웃 판",
                     {"html": H.replace(bal_c.group(0) + bcard.group(0), bcard.group(0) + bal_c.group(0), 1) if bcard and bal_c and (bal_c.group(0) + bcard.group(0)) in H else None}))
        muts.append(("하루예산 카드 뒤에 다른 카드", "레이아웃 판", {"html": H.replace(bcard.group(0), bcard.group(0) + '    <div class="kpi">x</div>\n', 1) if bcard else None}))

        # --- 4. 0건 가드 ---
        guards = [
            ("0건: masthead 문구 변조", "masthead 집계 기간", {"html": H.replace("집계 기간<b>", "집계기간<b>", 1)}),
            ("0건: KPI label 클래스 변조", "KPI 타일", {"html": H.replace('<div class="label">', '<div class="lbl">')}),
            ("0건: 04 td.num 전부 변조", "04번 예산 비중", {"html": H.replace(section(H, 4), section(H, 4).replace('<td class="num', '<td class="nm'), 1)}),
            ("0건: 각주 문구 변조", "08·09번 각주", {"html": H.replace("회로 상단 KPI(", "회로 상단 kpi(")}),
            ("0건: 07 name-cell 변조", "07번 클릭률", {"html": section(H, 7) and H.replace(s7, s7.replace('class="name-cell"', 'class="namecell"'), 1)}),
            ("0건: 날짜형 라벨 형식 변조", "날짜축 x축 라벨", {"html": re.sub(r"'(\d+/\d+\(.\))'", r"'\1_'", H)}),
            ("0건: mediaChart id 변조", "05번 mediaChart", {"html": H.replace("getElementById('mediaChart')", "getElementById('mediaChartX')", 1)}),
            ("0건: 06 카드 등록 문구 변조", "06번 카드", {"html": H.replace(s6, s6.replace(" 등록, ", " 등록· "), 1) if s6 else None}),
            ("0건: 경쟁사표 name-cell 변조", "경쟁사표", {"html": H.replace(s7, s7[:s7.find("경쟁사 브랜드명")] + s7[s7.find("경쟁사 브랜드명"):].replace('class="name-cell"', 'class="namecell"'), 1)}),
            ("0건: 10 판정 줄 문구 변조", "10번 항목 수", {"html": H.replace("항목 판정: 유지", "항목 판정 - 유지", 1)}),
            ("0건: Section 10·11 주석 변조(본문 0자)", "10·11번 금칙어", {"html": H.replace("<!-- Section 10:", "<!-- Sect 10:", 1).replace("<!-- Section 11:", "<!-- Sect 11:", 1)}),
            ("0건: Section 10·11 주석 변조(잔존 문구 검사)", "잔존 문구", {"html": H.replace("<!-- Section 10:", "<!-- Sect 10:", 1).replace("<!-- Section 11:", "<!-- Sect 11:", 1)}),
        ]
        for n in date_secs:
            m = re.search(r"\s*min-width:\s*\d+px;?", section(H, n))
            guards.append((f"0건: {n:02d}번 min-width 제거", f"{n:02d}번 차트 min-width",
                           {"html": replace_in_section(H, n, m.group(0), "") if m else None}))
        # (2026-10-06 추가) 07 ②③ 각주 블록 통째 제거 · ① 경쟁사 판정 줄 제거 → "07 각주 세 자리" FAIL
        m = re.search(r'<div class="note"[^>]*>(?:(?!</div>).)*?제외 검색어:.*?</div>', s7, re.S)
        guards.append(("0건: 07 ②③ 각주 블록 제거", "07 각주 세 자리", {"html": H.replace(s7, s7.replace(m.group(0), "", 1), 1) if m else None}))
        m = re.search(r"① 경쟁사 판정\(.*?<br>\s*", s7, re.S)
        guards.append(("0건: 07 ① 경쟁사 판정 줄 제거", "07 각주 세 자리", {"html": H.replace(s7, s7.replace(m.group(0), "", 1), 1) if m else None}))
        # (2026-10-06 회차 2) 레이아웃 판 meta 제거 · 접기 전부 풀기 → "레이아웃 판" FAIL
        guards.append(("0건: 레이아웃 판 meta 제거", "레이아웃 판", {"html": H.replace(meta + "\n", "", 1).replace(meta, "", 1) if meta in H else None}))
        guards.append(("0건: 접기 전부 풀기(옛 모양 복원 흉내)", "레이아웃 판", {"html": unfold(H) if "<details" in H else None}))
        # (2026-10-06 판 C) 분기 도우미 M 줄 이름 변조 → M 줄 0건
        guards.append(("0건: 판 C M 줄 변조(var M = { → var MX = {)", "레이아웃 판", {"html": H.replace("var M = {", "var MX = {", 1) if H.count("var M = {") == 1 else None}))
        # (2026-10-08 판 E) 01 모바일 터치 축 axis:'y' 지우기(판 D 꼴로 되돌림) → 터치 축 0건
        ty = "interaction: {mode:'index', intersect:false, axis:'y'}"
        guards.append(("0건: 판 E 01 모바일 터치 축 axis:'y' 지우기", "레이아웃 판",
                       {"html": H.replace(ty, "interaction: {mode:'index', intersect:false}", 1) if H.count(ty) == 1 else None}))
        # (2026-10-09 판 F) 잔액 카드 표지 지우기 → 카드 값·보조 줄 0건(잔액 검사) · 카드 표지 0(레이아웃 판)
        nob = H.replace(' data-balance="value"', "", 1).replace(' data-balance="sub"', "", 1) if 'data-balance="value"' in H else None
        guards.append(("0건: 판 F 잔액 카드 표지(data-balance) 지우기 → 잔액 검사", "광고비 잔액 카드", {"html": nob}))
        guards.append(("0건: 판 F 잔액 카드 표지(data-balance) 지우기 → 레이아웃 판", "레이아웃 판", {"html": nob}))
        # (2026-10-27 판 L) 하루예산 카드 표지 지우기 → 카드 값·보조 줄·summary 0건(하루예산 검사) · 카드 표지 0(레이아웃 판)
        nobd = re.sub(r' data-budget="[a-z]+"', "", H) if 'data-budget="card"' in H else None
        guards.append(("0건: 판 L 하루예산 카드 표지(data-budget) 지우기 → 하루예산 카드", "하루예산 카드 =", {"html": nobd}))
        guards.append(("0건: 판 L 하루예산 카드 표지(data-budget) 지우기 → 레이아웃 판", "레이아웃 판", {"html": nobd}))
        # (2026-10-10 매출 작업 A·C) 11번 장부 판정 문구 변조 → 장부 행 0 · Section 1·10·11 주석 변조 → 01·10·11 본문 0자
        noh = H.replace("<!-- saero:extra history -->", "", 1).replace("<!-- /saero:extra history -->", "", 1) if "<!-- saero:extra history -->" in H else None
        guards.append(("0건: 판 G 변경 기록 블록 표지 지우기 → 추가 카드·표", "추가 카드·표", {"html": noh}))
        guards.append(("0건: 판 G 변경 기록 블록 표지 지우기 → 레이아웃 판", "레이아웃 판", {"html": noh}))
        guards.append(("0건: 11 장부 판정 문구 변조(장부 기준 판정 = → 장부 판정:)", "11번 장부·플레이스 행",
                       {"html": H.replace("장부 기준 판정 = ", "장부 판정: ") if "장부 기준 판정 = " in H else None}))
        guards.append(("0건: Section 1·10·11 주석 변조(장부 라벨 검사 본문 0자)", "장부 라벨+숫자",
                       {"html": H.replace("<!-- Section 1:", "<!-- Sect 1:", 1).replace("<!-- Section 10:", "<!-- Sect 10:", 1).replace("<!-- Section 11:", "<!-- Sect 11:", 1)}))
        # (2026-10-23 판 I) 서술 표지 이름 꼴 변조 → 표지 0개 → "화면 글 구역 번호" 0건 가드
        guards.append(("0건: 서술 표지 이름 꼴 변조(<!-- n: → <!-- m:)", "화면 글 구역 번호", {"html": H.replace("<!-- n:", "<!-- m:") if "<!-- n:" in H else None}))
        # (2026-10-23 판 J) Section 3 주석 변조 → 03 구역 0자 → "판 J 뺀 글 0" 0건 가드
        guards.append(("0건: Section 3 주석 변조(판 J 뺀 글 검사 구역 0자)", "판 J 뺀 글", {"html": H.replace("<!-- Section 3:", "<!-- Sect 3:", 1)}))

        # --- 5. config 실험 ---
        c1 = json.loads(cfg_text); c1["ctr_high_threshold"] = float(cfg["ctr_high_threshold"]) + 1.0
        c2 = json.loads(cfg_text); c2["chart_min_width"]["date_based_sections"] = date_secs[:1]
        c3 = json.loads(cfg_text); c3["report_layout"]["layout_id"] = lid + "-config변조"
        c4 = json.loads(cfg_text); c4["report_layout"]["mobile"]["max_px"] = int(cfg["report_layout"]["mobile"]["max_px"]) + 1
        c5 = json.loads(cfg_text); c5["leads"]["publish"] = "counts"   # (2026-10-10) 공개 범위를 넓히면 기준 사본이 "장부 라벨+숫자" FAIL — config 를 읽는지
        c6 = json.loads(cfg_text); c6["group_cards"]["promotion_groups"] = []   # (2026-10-23 판 J) 승격 그룹을 비우면 기준 사본의 카드가 규칙 밖 → "06번 카드 그룹" FAIL
        c7 = json.loads(cfg_text); c7["ctr_few_07"]["min_imps"] = int(cfg["ctr_few_07"]["min_imps"]) + 1   # 07 범례·집계 기준 글의 N 과 config 가 어긋남 → "레이아웃 판" FAIL

        # --- 실행 ---
        ok = True
        print("\n== 검사별 변조 (겨냥한 검사가 FAIL로 바뀌어야 함)")
        covered = set()
        for name, target, spec in muts + guards:
            if spec.get("html") is None and "csv" not in spec and spec.get("bal") is None:
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
        rc, passed, failed, err = run(cfg_override=json.dumps(c3, ensure_ascii=False))
        hit3 = [f for f in failed if "레이아웃 판" in f and c3["report_layout"]["layout_id"] in f]
        print(f"  report_layout.layout_id {lid}→{c3['report_layout']['layout_id']}: 기준 사본 '레이아웃 판' FAIL {len(hit3)}건" + ("" if hit3 else "  ← MISS"))
        ok &= bool(hit3)
        rc, passed, failed, err = run(cfg_override=json.dumps(c4, ensure_ascii=False))
        mx = c4["report_layout"]["mobile"]["max_px"]
        hit4 = [f for f in failed if "레이아웃 판" in f and str(mx) in f]
        print(f"  report_layout.mobile.max_px {cfg['report_layout']['mobile']['max_px']}→{mx}: 기준 사본 '레이아웃 판' FAIL {len(hit4)}건" + ("" if hit4 else "  ← MISS"))
        ok &= bool(hit4)
        rc, passed, failed, err = run(cfg_override=json.dumps(c5, ensure_ascii=False))
        hit5 = [f for f in failed if "장부 라벨+숫자" in f and "counts" in f]
        print(f"  leads.publish verdict→counts: 기준 사본 '장부 라벨+숫자' FAIL {len(hit5)}건" + ("" if hit5 else "  ← MISS"))
        ok &= bool(hit5)
        rc, passed, failed, err = run(cfg_override=json.dumps(c6, ensure_ascii=False))
        hit6 = [f for f in failed if "06번 카드 그룹" in f]
        print(f"  group_cards.promotion_groups {cfg['group_cards']['promotion_groups']}→[]: 기준 사본 '06번 카드 그룹' FAIL {len(hit6)}건" + ("" if hit6 else "  ← MISS"))
        ok &= bool(hit6)
        rc, passed, failed, err = run(cfg_override=json.dumps(c7, ensure_ascii=False))
        hit7 = [f for f in failed if "레이아웃 판" in f and "ctr_few_07" in f]
        print(f"  ctr_few_07.min_imps {cfg['ctr_few_07']['min_imps']}→{c7['ctr_few_07']['min_imps']}: 기준 사본 '레이아웃 판' FAIL {len(hit7)}건" + ("" if hit7 else "  ← MISS"))
        ok &= bool(hit7)

        uncovered = [c for c in checks if c not in covered]
        print(f"\n== 커버리지: 기준 검사 {len(checks)}개 중 변조로 FAIL 확인 {len(covered)}개")
        for c in uncovered:
            print(f"  [UNCOVERED] {c} — 이 검사를 깨뜨리는 변조가 없다. 스크립트에 추가할 것")
        ok &= not uncovered

        # --- 6b. compare 실험(2026-10-26 판 K — 요일 값 변조 → compare DIFF, 그 항목만) ---
        ok &= compare_experiments(work, H, comp_src, cfg_path, cfg_text)
        # --- 6c. compare 실험(2026-10-27 판 L — 하루예산 카드 값 변조 → compare DIFF, 그 항목만) ---
        ok &= budget_compare_experiments(work, H, comp_src, cfg_path, cfg_text)

        # --- 7. archive.py ---
        ok &= archive_experiments(work)

        # --- 원본 무결성 ---
        changed = [k for k, v in orig.items() if md5(v) != orig_md5[k]] + [p for p in data_files if md5(p) != data_md5[p]]
        print(f"\n원본 md5 대조(html·CSV 4·data/ {len(data_files)}개): {'전부 동일' if not changed else '변경됨 ' + str(changed)}")
        ok &= not changed
        print("\n" + "=" * 50)
        print("전부 살아 있음." if ok else "문제 있음 — 위 [MISS]/[UNCOVERED]/[SKIP] 확인.")
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
