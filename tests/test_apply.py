#!/usr/bin/env python3
"""scripts/apply.py 시험(E2 저장소화, 2026-10-06) + compute.py 직전 경쟁사표 0행 가드.

fixture = tests/fixtures/layout_old.html(배포본 앵커 마크업 발췌 — 숫자·검색어·경쟁사·그룹 이름 가짜, 서술 표지 없음) +
          tests/fixtures/layout_old.compute.json(같은 가짜 값의 compute 출력 꼴).
- 멱등: 같은 compute.json 으로 두 번 돌리면 바이트 같음(표지 없는 fixture · 서술 표지를 넣은 fixture 둘 다).
- 앵커·행 수: masthead·og·KPI·차트·01 표 5행·순위 5칸·03 행 수(날짜 + 합계)·04·06·07 정식표/목록/경쟁사표·08·10 이 compute 값과 같음.
  동률은 직전 순서(클릭 1건 목록) · 신규 변형 행 = config competitor_defaults.
- 시끄러운 실패: 앵커가 없거나 둘이면·새 04 그룹·직전/후보 밖 경쟁사 → `[FAIL] apply:` exit 1, 작업본 바이트 그대로.
- compute.py: --competitors-html 의 경쟁사표 0행(소제목만 바꾼 사본 — 탐색 프로브 r10 유형) → `[FAIL]` exit 1(합본을 읽기 전).
- 리허설 산출(work/R1/index.html + compute.json, 서술 표지 있음)이 있으면 그것도 멱등(없으면 건너뜀).
실행: "$PY" tests/test_apply.py
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import apply as A  # noqa: E402
from reportlib import load_config, section  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

FIX = os.path.join(HERE, "fixtures", "layout_old.html")
FIXJ = os.path.join(HERE, "fixtures", "layout_old.compute.json")
APPLY = os.path.join(ROOT, "scripts", "apply.py")
COMPUTE = os.path.join(ROOT, "scripts", "compute.py")


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def jread(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def md5(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def rows(s):
    return re.findall(r"<tr[^>]*>(.*?)</tr>", s, re.S)


def cells(tr):
    return [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]


def listtext(h, anchor):
    a = h.index('line-height:1.9;">', h.index(anchor)) + len('line-height:1.9;">')
    return [x.strip() for x in h[a:h.index("</div>", a)].strip().split(" · ")]


class ApplyFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.H, cls.R, cls.cfg = read(FIX), jread(FIXJ), load_config()
        cls.out = A.apply(cls.H, cls.R, cls.cfg)

    def test_idempotent_and_changed(self):
        self.assertNotEqual(self.out, self.H)                      # 빈 시험이 아님 — 값이 실제로 바뀐다
        self.assertEqual(A.apply(self.out, self.R, self.cfg), self.out)

    def test_idempotent_with_narrative_markers(self):
        """서술 표지가 있는 판(새 글) — 표지는 apply 가 건드리지 않고, 01 순위 5칸 끝 앵커(표지 무관)도 그대로 맞는다."""
        H2 = self.H.replace('<div class="note">닷새 동안 가짜 순위 서술.</div>',
                            '<div class="note"><!-- n:01-rank:매회차 -->닷새 가짜 순위 서술.<!-- /n --></div>', 1)
        H2 = H2.replace("        4일차. 가짜 카드 서술.", "        <!-- n:06-card-가짜그룹B:매회차 -->4일차. 가짜 카드 서술.<!-- /n -->", 1)
        self.assertEqual(H2.count("<!-- n:"), 2)
        o1 = A.apply(H2, self.R, self.cfg)
        self.assertEqual(A.apply(o1, self.R, self.cfg), o1)
        self.assertEqual(re.findall(r"<!-- n:[^>]+-->.*?<!-- /n -->", o1, re.S), re.findall(r"<!-- n:[^>]+-->.*?<!-- /n -->", H2, re.S))
        self.assertEqual(o1.count("위</div>"), self.out.count("위</div>"))  # 순위 5칸이 그대로 생성됨

    def test_values_and_row_counts(self):
        o, R = self.out, self.R
        self.assertIn(f"집계 기간<b>{R['masthead']}</b>", o)
        self.assertIn(f'og:description" content="{R["og"]}"', o)
        self.assertIn(f'<div class="value">{R["KPI"]["노출"]:,}<span class="unit">회', o)
        self.assertIn(f"일 평균 {R['KPI']['일평균노출']}회", o)
        self.assertIn(f"클릭당 평균 {R['KPI']['클릭당']:,}원", o)
        self.assertIn(f"광고비 비중 (총 {R['KPI']['광고비']:,}원)", o)
        self.assertEqual(len(re.findall(rf'min-width:{R["minwidth"]}px;">\s*<canvas id="(?:dailyChart|rankChart)"', o)), 2)
        self.assertIn("labels: [" + ",".join(f"'{x}'" for x in R["01"]["labels"]) + "]", o)
        self.assertIn("data: [" + ", ".join(map(str, R["01"]["노출"])) + "]", o)
        s1, s3, s4, s6, s7, s8, s10 = (section(o, n) for n in (1, 3, 4, 6, 7, 8, 10))
        self.assertEqual([cells(t)[0] for t in rows(s1)], [r["날짜"] for r in R["01"]["표5"]])
        self.assertEqual(re.findall(r'margin-bottom:2px;">([^<]+)</div>', s1), [g["날짜"] for g in R["01"]["플레이스순위5"]])
        self.assertEqual(len(re.findall(r'font-weight:800;color:var\(--mint-dark\);">[\d.]+위', s1)), 1)   # 민트 칸 하나
        r3 = [cells(t) for t in rows(s3) if "<td" in t]
        self.assertEqual(len(r3), len(R["03"]["rows"]) + 1)
        self.assertEqual([r[0] for r in r3], [r["날짜"] for r in R["03"]["rows"]] + ["합계"])           # 오름차순 + 합계(회차 1)
        self.assertEqual([cells(t)[1].split("(")[0].strip() for t in rows(s4)], [r["그룹"] for r in R["04"]["rows"]])
        self.assertIn("(1/2 신규)", s4)                                                                  # 이름 칸 메모는 직전 행 그대로
        self.assertIn("(1/2 등록, 6일차)", s6)
        self.assertIn('font-weight:800;color:var(--mint-dark);">1.55위', s6)
        main7 = [cells(t) for t in rows(s7[:s7.index("클릭 1건 검색어")])]
        self.assertEqual([r[0] for r in main7], [r["검색어"] for r in R["07"]["정식표"]])
        self.assertEqual(main7[1][1], "확장")                                                            # *동률 표시는 지움
        self.assertEqual(listtext(o, "클릭 1건 검색어"), ["가짜한건가(12회/700원)", "가짜한건나(10회/500원)", "가짜한건다(10회/900원)"])  # 동률 = 직전 순서
        self.assertEqual(listtext(o, "노출은 있으나 클릭 0건인"), [f"{x['검색어']}({x['노출']}회)" for x in R["07"]["클릭0목록"]])
        comp = [cells(t) for t in rows(s7[s7.index("경쟁사 브랜드명 검색어"):])]
        self.assertEqual([r[0] for r in comp], [r["검색어"] for r in R["07"]["경쟁사표"]])
        d = self.cfg["competitor_defaults"]
        self.assertEqual(comp[1][1:3], [d["district"], d["match"]])                                      # 신규 변형 = config 기본값
        self.assertEqual(comp[0][1:3], ["가짜구", "일치"])                                                 # 직전 행 그대로
        self.assertEqual(len([t for t in rows(s8) if "<td" in t]), 10)
        self.assertEqual(listtext(o, "TOP 10 외"), ["가짜동(노출6·클릭1)", "가짜읍(노출5·클릭1)"])
        self.assertIn(f"({R['08']['컴팩트수']}개 지역·클릭 {R['08']['컴팩트클릭']}건)", s8)
        self.assertEqual([[c.replace(",", "").replace("원", "") for c in cells(t)[2:5]] for t in rows(s10)],
                         [[str(v) for v in R["10"][k]] for k in "ABCD"])


class ApplyFailsLoudly(unittest.TestCase):
    def run_cli(self, html_text, R=None):
        td = tempfile.mkdtemp()
        try:
            h, j = os.path.join(td, "index.html"), os.path.join(td, "compute.json")
            with open(h, "w", encoding="utf-8", newline="") as f:
                f.write(html_text)
            if R is None:
                shutil.copy(FIXJ, j)
            else:
                with open(j, "w", encoding="utf-8") as f:
                    json.dump(R, f, ensure_ascii=False)
            before = md5(h)
            r = subprocess.run([sys.executable, APPLY, "--html", h, "--compute", j], capture_output=True, text=True, encoding="utf-8")
            return r.returncode, r.stdout + r.stderr, before == md5(h)
        finally:
            shutil.rmtree(td, ignore_errors=True)

    def test_cli_ok(self):
        rc, out, same = self.run_cli(read(FIX))
        self.assertEqual(rc, 0, out)
        self.assertFalse(same)
        self.assertIn("[apply]", out)

    def test_missing_or_duplicate_anchor(self):
        H = read(FIX)
        for label, text in (("TOP 10 외 없음", H.replace("TOP 10 외 지역", "TOP10 밖 지역", 1)),
                            ("클릭당 평균 둘", H.replace("</body>", "<p>클릭당 평균 1원</p></body>", 1)),
                            ("집계 기간 없음", H.replace("집계 기간<b>", "집계기간<b>", 1)),
                            ("경쟁사 머리글 소제목 변경", H.replace("경쟁사 브랜드명 검색어</div>", "경쟁사 검색어 (2개)</div>", 1)),
                            ("10 표 행 3개", H.replace('<td class="name-cell">추천·콘텐츠 지면 › 가짜 D</td>\n            <td>가짜 매체</td>\n            <td class="num">40</td>', '<td class="name-cell">D</td>', 1))):
            with self.subTest(label=label):
                rc, out, same = self.run_cli(text)
                self.assertEqual(rc, 1, out)
                self.assertIn("[FAIL] apply:", out)
                self.assertTrue(same, "실패했는데 작업본이 바뀜")

    def test_new_group_and_unknown_competitor(self):
        R = jread(FIXJ)
        R["04"]["rows"].append(dict(R["04"]["rows"][-1], 그룹="가짜새그룹"))
        rc, out, same = self.run_cli(read(FIX), R)
        self.assertEqual(rc, 1, out)
        self.assertIn("새 그룹", out)
        self.assertTrue(same)
        R = jread(FIXJ)
        R["07"]["신규변형후보"] = []                                   # 직전 표에도 후보에도 없는 이름 → 멈춤
        rc, out, same = self.run_cli(read(FIX), R)
        self.assertEqual(rc, 1, out)
        self.assertIn("신규 변형 후보도 아닌", out)
        self.assertTrue(same)


class ComputeCompetitorGuard(unittest.TestCase):
    def test_zero_rows_fail_before_reading_csv(self):
        import compute as C
        H = read(FIX)
        self.assertEqual(C.deployed_competitors(H), ["가짜경쟁A", "가짜경쟁B"])
        td = tempfile.mkdtemp()
        try:
            bad = os.path.join(td, "prev.html")
            with open(bad, "w", encoding="utf-8") as f:
                f.write(H.replace("경쟁사 브랜드명 검색어</div>", "경쟁사 검색어 (2개)</div>", 1))   # r10 유형 — 소제목만 바뀜
            r = subprocess.run([sys.executable, COMPUTE, os.path.join(td, "없는합본"), "--competitors-html", bad, "-o", os.path.join(td, "o.json")],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("[FAIL] 직전 배포본 경쟁사표 0행", r.stdout)
            self.assertFalse(os.path.exists(os.path.join(td, "o.json")))
        finally:
            shutil.rmtree(td, ignore_errors=True)


@unittest.skipUnless(os.path.exists(os.path.join(ROOT, "work", "R1", "index.html")) and os.path.exists(os.path.join(ROOT, "work", "R1", "compute.json")),
                     "리허설 산출 work/R1 없음(구현·검증 회차 리허설 뒤에만)")
class ApplyRehearsal(unittest.TestCase):
    def test_r1_output_idempotent(self):
        H = read(os.path.join(ROOT, "work", "R1", "index.html"))
        R = jread(os.path.join(ROOT, "work", "R1", "compute.json"))
        self.assertGreater(H.count("<!-- n:"), 20)
        self.assertEqual(A.apply(H, R, load_config()), H)


if __name__ == "__main__":
    unittest.main(verbosity=1)
