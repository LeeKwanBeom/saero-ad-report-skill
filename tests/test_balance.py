#!/usr/bin/env python3
"""광고비 잔액 카드(레이아웃 판 r2026-10-F, 2026-10-09) · 하루예산 읽기(판 L, 2026-10-27) 시험 — scripts/balance.py · compute.py --balance · validate.py "광고비 잔액 카드".

가짜 API(sender 바꿔 끼우기 — 네트워크 0)·가짜 키 파일(임시 폴더)·합성 CSV 만 쓴다. 실제 키 파일·계정·배포본에 닿지 않는다.
- balance.py: 성공(원 단위 버림 · 정수 그대로) · customerId 같음(문자열/숫자) → ok / 401·403 · 5xx · 그 밖 코드 · 429 두 번 · 네트워크 · 프록시 · 응답 도중 끊김 ·
  응답 꼴 다름(dict 아님 · bizmoney 없음 · 문자열 · bool · NaN · 무한 · 음수 · customerId 다름) · 예상 못 한 오류 · 키 파일 없음·JSON 아님·칸 없음 → fail 기록(exit 0) ·
  옛 ok 기록은 실행 시작에 지워져 실패 기록으로 바뀐다(옛 값이 남지 않음) · 기록을 못 쓰면 exit 1·파일 없음 · 잔액 호출은 GET /billing/bizmoney 하나뿐(429 재시도만 둘) ·
  서버가 키를 되돌려 줘도 화면·json 에 키 0.
- balance.py 하루예산(판 L — Route 가짜 서버가 주소마다 답): GET /ncc/campaigns 1 + 캠페인마다 GET /ncc/adgroups?nccCampaignId= 1(10/27 꼴 캠페인 2 → 합 4회 · 전부 GET · 본문 없음) ·
  기록 "budget"(이름·유형·useDailyBudget·dailyBudget 원 버림·userLock·status · 그룹 목록) · 잔액과 따로: 예산 실패(5xx · 401/403 · 네트워크 · 응답 꼴 다름 9가지)에도 잔액 ok·exit 0 /
  잔액 실패에도 예산 ok · 키 파일 문제면 둘 다 fail · 호출 0 · 서버가 키를 되돌려 줘도 0 · balance.py 원문의 request 메서드는 GET 뿐(쓰기 호출 0).
- compute.py --balance: 창 = 키워드 `일별` 달력 7일(빈 날 0원 · 제외 그룹 뺌) · 일분 = ⌊원 × 창일수 ÷ 창합계⌋ · 합계 0 이면 일분 null · 실패 기록 → 상태 fail ·
  읽은 날 ≤ 집계 마지막 날(지난 회차 기록) → [FAIL] exit 1 · 파일 없음·꼴 다름 → [FAIL] exit 1.
- validate.py "광고비 잔액 카드": 합성 카드 HTML + 합성 키워드 표 — ok·일분 생략·fail 꼴 PASS / 값·시각·며칠분·꼴 하나라도 다르면 FAIL · 지난 회차 기록 FAIL ·
  기록 없음·카드 0건 FAIL.
실행: "$PY" tests/test_balance.py
"""
import contextlib
import datetime as dt
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import balance as B  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass

KEY, SECRET, CID = "FAKE-API-KEY-0123456789", "FAKE+SECRET/abcdefghij==", 4480035
COMPUTE = os.path.join(ROOT, "scripts", "compute.py")


class Fake:
    """sender 자리 — 받은 요청을 적고, 정해 둔 응답(또는 예외)을 차례로 돌려준다."""

    def __init__(self, *answers):
        self.answers, self.seen = list(answers), []

    def __call__(self, method, url, headers, data):
        self.seen.append((method, url, dict(headers), data))
        a = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        if isinstance(a, BaseException):
            raise a
        return a(headers) if callable(a) else a


class Route:
    """sender 자리(판 L) — 주소(쿼리 뗀 경로)마다 정해 둔 답(목록이면 차례로 · 마지막은 되풀이 · 함수면 (headers, url) 을 받아 답). 받은 요청을 적는다."""

    def __init__(self, **answers):
        self.answers, self.seen = {k: (list(v) if isinstance(v, list) else [v]) for k, v in answers.items()}, []

    def __call__(self, method, url, headers, data):
        self.seen.append((method, url, dict(headers), data))
        path = url.split("api.searchad.naver.com", 1)[1].split("?")[0]
        q = self.answers[{"/billing/bizmoney": "biz", "/ncc/campaigns": "camps", "/ncc/adgroups": "groups"}[path]]
        a = q.pop(0) if len(q) > 1 else q[0]
        if isinstance(a, BaseException):
            raise a
        return a(headers, url) if callable(a) else a


CAMPS = [{"nccCampaignId": "cmp-1", "name": "가짜 파워링크", "campaignTp": "WEB_SITE", "useDailyBudget": True, "dailyBudget": 30000, "status": "ELIGIBLE", "userLock": False},
         {"nccCampaignId": "cmp-2", "name": "가짜플레이스#1", "campaignTp": "PLACE", "useDailyBudget": True, "dailyBudget": 30000.9, "status": "ELIGIBLE", "userLock": False}]
GROUPS = {"cmp-1": [{"nccAdgroupId": "grp-1", "nccCampaignId": "cmp-1", "name": "가짜그룹A", "adgroupType": "WEB_SITE", "useDailyBudget": True, "dailyBudget": 15000,
                     "status": "ELIGIBLE", "userLock": False},
                    {"nccAdgroupId": "grp-2", "nccCampaignId": "cmp-1", "name": "가짜그룹B", "adgroupType": "WEB_SITE", "useDailyBudget": False, "dailyBudget": 0,
                     "status": "PAUSED", "userLock": True}],
          "cmp-2": [{"nccAdgroupId": "grp-3", "nccCampaignId": "cmp-2", "name": "가짜플레이스그룹", "adgroupType": "LOCAL_AD", "useDailyBudget": True, "dailyBudget": 20000,
                     "status": "ELIGIBLE", "userLock": False}]}


def groups_by_query(h, url):
    return 200, GROUPS[url.split("nccCampaignId=")[1]]


class BalanceScript(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp()
        self.keys = os.path.join(self.td, "keys.json")
        with open(self.keys, "w", encoding="utf-8") as f:
            json.dump({"api_key": KEY, "secret_key": SECRET, "customer_id": CID}, f)
        self.out = os.path.join(self.td, "work", "balance.json")

    def tearDown(self):
        shutil.rmtree(self.td, ignore_errors=True)

    def run_main(self, sender, keys=None, out=None):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = B.main(["--key-file", keys or self.keys, "--out", out or self.out], sender=sender)
        rec = None
        if os.path.exists(out or self.out):
            with open(out or self.out, encoding="utf-8") as f:
                raw = f.read()
            rec = json.loads(raw)
            self.assertNotIn(KEY, raw)
            self.assertNotIn(SECRET, raw)
        text = buf.getvalue()
        self.assertNotIn(KEY, text)
        self.assertNotIn(SECRET, text)
        return rc, rec, text

    def test_ok_floor_and_one_get(self):
        f = Fake((200, {"customerId": CID, "bizmoney": 217817.915506, "budgetLock": False, "refundLock": False}), (200, []))   # 둘째 답부터 = 캠페인 0개(판 L 예산 GET 1)
        rc, rec, text = self.run_main(f)
        self.assertEqual(rc, 0, text)
        self.assertEqual(rec["status"], "ok")
        self.assertEqual(rec["bizmoney"], 217817)                       # 원 단위 버림(반올림 아님)
        self.assertEqual(rec["bizmoney_raw"], 217817.915506)
        self.assertIs(rec["budgetLock"], False)
        t = dt.datetime.fromisoformat(rec["read_at"])
        self.assertEqual(t.utcoffset(), dt.timedelta(hours=9))          # KST
        self.assertLess(abs((dt.datetime.now(dt.timezone.utc) - t).total_seconds()), 60)
        self.assertEqual([(m, u.split("?")[0]) for m, u, _, _ in f.seen], [("GET", "https://api.searchad.naver.com/billing/bizmoney"),
                                                                          ("GET", "https://api.searchad.naver.com/ncc/campaigns")])   # 잔액 1 + 판 L 캠페인 1(0개 — 그룹 GET 0)
        self.assertIsNone(f.seen[0][3])                                  # 본문 없음(읽기)
        self.assertEqual(f.seen[0][2]["X-Customer"], str(CID))
        self.assertIn("[잔액] 217,817원 · ", text)
        self.assertIn("GET /billing/bizmoney 1회", text)
        self.assertEqual(rec["budget"]["status"], "ok")
        self.assertEqual(rec["budget"]["campaigns"], [])

    def test_ok_variants(self):
        for label, resp, want in (("정수", {"bizmoney": 5000}, 5000), (".999 버림", {"bizmoney": 9.999}, 9), ("0원", {"bizmoney": 0.0}, 0),
                                  ("customerId 문자열", {"customerId": str(CID), "bizmoney": 12.5}, 12), ("customerId 없음", {"bizmoney": 1}, 1)):
            with self.subTest(label=label):
                rc, rec, text = self.run_main(Fake((200, resp)))
                self.assertEqual((rc, rec["status"], rec["bizmoney"]), (0, "ok", want), text)

    def fail_case(self, sender, reason_part):
        rc, rec, text = self.run_main(sender)
        self.assertEqual(rc, 0, text)                                   # 조회 실패로 회차를 멈추지 않는다
        self.assertEqual(rec["status"], "fail", text)
        self.assertIn(reason_part, rec["reason"])
        self.assertEqual(set(rec), {"status", "read_at", "reason", "budget"})   # 숫자 칸 없음(판 L — 예산 기록은 따로)
        self.assertIn("[주의] 잔액 확인 못 함", text)
        return rec, text

    def test_http_failures(self):
        echo = lambda h: (401, {"code": 1, "message": f"invalid {h['X-API-KEY']} sig"})   # 서버가 키를 되돌려 줌 — 가려져야
        self.fail_case(Fake(echo), "인증·권한")
        self.fail_case(Fake((403, {"message": "forbidden"})), "인증·권한")
        self.fail_case(Fake(lambda h: (500, {"message": f"oops {h['X-API-KEY']}"})), "서버 오류(500)")
        self.fail_case(Fake((404, {"message": "no"})), "응답 코드 404")
        f = Fake((429, {"message": "slow"}))
        orig = B.X.time.sleep
        B.X.time.sleep = lambda s: None
        try:
            self.fail_case(f, "429")
        finally:
            B.X.time.sleep = orig
        self.assertEqual(len([u for _, u, _, _ in f.seen if u.endswith("/billing/bizmoney")]), 2)   # 429 는 NaverApi.request 가 1회 재시도(그 밖엔 1회)

    def test_transport_failures(self):
        self.fail_case(Fake(urllib.error.URLError("Tunnel connection failed: 403 Forbidden")), "프록시")
        self.fail_case(Fake(urllib.error.URLError(f"getaddrinfo failed {KEY}")), "네트워크 오류")
        self.fail_case(Fake(TimeoutError("timed out")), "요청 결과 모름")
        self.fail_case(Fake(ValueError("not json")), "요청 결과 모름")
        self.fail_case(Fake(RuntimeError(f"weird {SECRET}")), "알 수 없는 오류(RuntimeError)")

    def test_shape_failures(self):
        for label, resp in (("list", [1, 2]), ("None", None), ("bizmoney 없음", {"customerId": CID}), ("문자열", {"bizmoney": "217817"}),
                            ("bool", {"bizmoney": True}), ("NaN", {"bizmoney": math.nan}), ("무한", {"bizmoney": math.inf}),
                            ("음수", {"bizmoney": -1}), ("customerId 다름", {"customerId": 999, "bizmoney": 100}),
                            ("키 되돌림", {"echo": KEY})):
            with self.subTest(label=label):
                self.fail_case(Fake((200, resp)), "응답 꼴 다름")

    def test_key_file_problems(self):
        bad_json = os.path.join(self.td, "bad.json")
        with open(bad_json, "w", encoding="utf-8") as f:
            f.write("{not json")
        no_secret = os.path.join(self.td, "nosecret.json")
        with open(no_secret, "w", encoding="utf-8") as f:
            json.dump({"api_key": KEY}, f)
        as_list = os.path.join(self.td, "list.json")
        with open(as_list, "w", encoding="utf-8") as f:
            json.dump([KEY, SECRET], f)
        for label, path in (("없음", os.path.join(self.td, "없는.json")), ("JSON 아님", bad_json), ("칸 없음", no_secret), ("객체 아님(목록)", as_list)):
            with self.subTest(label=label):
                f = Fake((200, {"bizmoney": 1}))
                rc, rec, text = self.run_main(f, keys=path)
                self.assertEqual((rc, rec["status"], rec["reason"]), (0, "fail", "키 파일 문제"), text)
                self.assertEqual(f.seen, [])                              # 호출 0
                self.assertIn("GET /billing/bizmoney 0회", text)

    def test_old_ok_record_never_survives(self):
        os.makedirs(os.path.dirname(self.out))
        with open(self.out, "w", encoding="utf-8") as f:
            json.dump({"status": "ok", "read_at": "2026-10-08T14:00:00+09:00", "bizmoney": 999999}, f)
        rec, _ = self.fail_case(Fake(urllib.error.URLError("down")), "네트워크")
        self.assertNotIn("bizmoney", rec)
        os.remove(self.out)                                              # 쓰기 실패: 자리가 폴더라 못 씀 → exit 1 · 옛 기록 없음
        os.makedirs(self.out)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = B.main(["--key-file", self.keys, "--out", self.out], sender=Fake((200, {"bizmoney": 1})))
        self.assertEqual(rc, 1, buf.getvalue())
        self.assertIn("[FAIL]", buf.getvalue())
        self.assertTrue(os.path.isdir(self.out))

    # ── 판 L 하루예산(2026-10-27) ──
    def test_budget_ok_four_gets(self):
        r = Route(biz=(200, {"bizmoney": 483628.96}), camps=(200, CAMPS), groups=groups_by_query)
        rc, rec, text = self.run_main(r)
        self.assertEqual(rc, 0, text)
        self.assertEqual((rec["status"], rec["bizmoney"]), ("ok", 483628))
        self.assertEqual([(m, u.split("searchad.naver.com")[1]) for m, u, _, _ in r.seen],
                         [("GET", "/billing/bizmoney"), ("GET", "/ncc/campaigns"), ("GET", "/ncc/adgroups?nccCampaignId=cmp-1"), ("GET", "/ncc/adgroups?nccCampaignId=cmp-2")])
        self.assertTrue(all(m == "GET" and d is None for m, _, _, d in r.seen))       # 전부 GET · 본문 없음(쓰기 0)
        b = rec["budget"]
        self.assertEqual(b["status"], "ok")
        t = dt.datetime.fromisoformat(b["read_at"])
        self.assertEqual(t.utcoffset(), dt.timedelta(hours=9))
        self.assertEqual(b["campaigns"][1], {"id": "cmp-2", "name": "가짜플레이스#1", "type": "PLACE", "useDailyBudget": True, "dailyBudget": 30000, "userLock": False,
                                             "status": "ELIGIBLE", "groups": [{"id": "grp-3", "name": "가짜플레이스그룹", "type": "LOCAL_AD", "useDailyBudget": True,
                                                                               "dailyBudget": 20000, "userLock": False, "status": "ELIGIBLE"}]})   # 30000.9 → 30000(버림)
        self.assertEqual([(g["name"], g["userLock"], g["useDailyBudget"]) for g in b["campaigns"][0]["groups"]], [("가짜그룹A", False, True), ("가짜그룹B", True, False)])
        self.assertIn("[하루예산] 가짜 파워링크 30,000원(켜진 그룹 1 · 15,000원) · 가짜플레이스#1 30,000원(켜진 그룹 1 · 20,000원)", text)
        self.assertIn("GET /ncc/campaigns 1회 · /ncc/adgroups 2회 · 이 실행 호출 합 4회(전부 GET — 쓰기 0)", text)
        self.assertIn("GET /billing/bizmoney 1회", text)

    def test_budget_fail_keeps_balance(self):
        bad_shapes = (("목록 아님", (200, {"data": CAMPS})), ("dailyBudget 문자열", (200, [dict(CAMPS[0], dailyBudget="30000")])),
                      ("dailyBudget bool", (200, [dict(CAMPS[0], dailyBudget=True)])), ("dailyBudget NaN", (200, [dict(CAMPS[0], dailyBudget=math.nan)])),
                      ("dailyBudget 음수", (200, [dict(CAMPS[0], dailyBudget=-1)])), ("useDailyBudget 없음", (200, [{k: v for k, v in CAMPS[0].items() if k != "useDailyBudget"}])),
                      ("이름 없음", (200, [{k: v for k, v in CAMPS[0].items() if k != "name"}])), ("nccCampaignId 없음", (200, [{k: v for k, v in CAMPS[0].items() if k != "nccCampaignId"}])),
                      ("userLock 문자열", (200, [dict(CAMPS[0], userLock="false")])))
        for label, camps in bad_shapes:
            with self.subTest(label=label):
                rc, rec, text = self.run_main(Route(biz=(200, {"bizmoney": 1000}), camps=camps, groups=groups_by_query))
                self.assertEqual((rc, rec["status"], rec["bizmoney"]), (0, "ok", 1000), text)    # 잔액 그대로
                self.assertEqual((rec["budget"]["status"], rec["budget"]["reason"]), ("fail", "응답 꼴 다름"), text)
                self.assertEqual(set(rec["budget"]), {"status", "read_at", "reason"})           # 반쪽 목록 0
                self.assertIn("[주의] 하루예산 확인 못 함(응답 꼴 다름)", text)
                self.assertIn("[잔액] 1,000원", text)
        other = dict(GROUPS, **{"cmp-2": [dict(GROUPS["cmp-2"][0], nccCampaignId="cmp-9")]})
        for label, kw, why in (("캠페인 500", {"camps": lambda h, u: (500, {"message": f"oops {h['X-API-KEY']}"})}, "서버 오류(500)"),
                               ("그룹 403", {"camps": (200, CAMPS), "groups": (403, {"message": "forbidden"})}, "인증·권한"),
                               ("그룹 404", {"camps": (200, CAMPS), "groups": (404, {"message": "no"})}, "응답 코드 404"),
                               ("캠페인 네트워크", {"camps": urllib.error.URLError(f"getaddrinfo failed {KEY}")}, "네트워크 오류"),
                               ("캠페인 끊김", {"camps": TimeoutError("timed out")}, "요청 결과 모름"),
                               ("그룹 목록 아님", {"camps": (200, CAMPS), "groups": (200, {"x": 1})}, "응답 꼴 다름"),
                               ("그룹 캠페인 다름", {"camps": (200, CAMPS), "groups": lambda h, u: (200, other[u.split("=")[1]])}, "응답 꼴 다름"),
                               ("그룹 dailyBudget 없음", {"camps": (200, CAMPS), "groups": (200, [{k: v for k, v in GROUPS["cmp-1"][0].items() if k != "dailyBudget"}])}, "응답 꼴 다름")):
            with self.subTest(label=label):
                kw.setdefault("groups", groups_by_query)
                rc, rec, text = self.run_main(Route(biz=(200, {"bizmoney": 1000}), **kw))
                self.assertEqual((rc, rec["status"], rec["bizmoney"]), (0, "ok", 1000), text)
                self.assertEqual(rec["budget"]["status"], "fail", text)
                self.assertIn(why, rec["budget"]["reason"])
                self.assertIn("[주의] 하루예산 확인 못 함", text)

    def test_balance_fail_budget_ok(self):
        r = Route(biz=(500, {"message": "down"}), camps=(200, CAMPS), groups=groups_by_query)
        rc, rec, text = self.run_main(r)
        self.assertEqual((rc, rec["status"], rec["budget"]["status"]), (0, "fail", "ok"), text)   # 잔액 실패에도 예산은 따로
        self.assertIn("[주의] 잔액 확인 못 함(서버 오류(500))", text)
        self.assertIn("[하루예산] ", text)
        self.assertEqual(len(r.seen), 4)

    def test_key_file_problem_budget_fail_no_calls(self):
        r = Route(biz=(200, {"bizmoney": 1}), camps=(200, CAMPS), groups=groups_by_query)
        rc, rec, text = self.run_main(r, keys=os.path.join(self.td, "없는.json"))
        self.assertEqual((rc, rec["budget"]["status"], rec["budget"]["reason"], r.seen), (0, "fail", "키 파일 문제", []), text)
        self.assertIn("GET /ncc/campaigns 0회 · /ncc/adgroups 0회 · 이 실행 호출 합 0회", text)

    def test_source_has_get_only(self):
        with open(os.path.join(ROOT, "scripts", "balance.py"), encoding="utf-8") as f:
            src = f.read()
        methods = re.findall(r'\.request\(\s*"([A-Z]+)"', src)
        self.assertEqual(sorted(set(methods)), ["GET"])                                  # 쓰기 호출(POST·PUT·PATCH·DELETE) 0 — 판 L 은 GET 만 더한다
        self.assertEqual(len(methods), 3)                                                # 잔액 · 캠페인 · 그룹
        self.assertNotRegex(src, r"\.(add_restricted|delete_restricted)\(")

    def test_cli_usage(self):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "balance.py")], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 2)                                # --key-file 없음 = 인자 오류(호출 0)


# ── compute.py --balance · validate.py "광고비 잔액 카드" — 합성 합본(키워드 CSV 만 실제 꼴, 나머지 셋은 compute 가 읽는 최소 꼴) ──
KW_HEAD = "캠페인,광고그룹,키워드,일별,매체이름,PC/모바일 매체,검색/콘텐츠 매체,노출수,클릭수,클릭률(%),평균 CPC,총비용,평균노출순위"


def kw_csv(rows):
    """rows = [(일별 'YYYY.MM.DD.', 광고그룹, 총비용)] → 키워드 CSV 글(1행 기간 헤더 + 2행 컬럼)."""
    out = ["필라테스 보고서(2026.10.01.~2026.10.08.)", KW_HEAD]
    for d, g, cost in rows:
        out.append(f"파워링크#1,{g},가짜키워드,{d},네이버,모바일,검색,10,1,10.00,{cost},{cost},2.0")
    return "\n".join(out) + "\n"


def frame(rows):
    import pandas as pd
    return pd.read_csv(io.StringIO(kw_csv(rows)), skiprows=1)


def rec_ok(won_raw, read_at):
    return {"status": "ok", "read_at": read_at, "bizmoney": int(math.floor(won_raw)), "bizmoney_raw": won_raw, "budgetLock": False, "refundLock": False}


# 10/2~10/8 중 10/5 는 행 없음(빈 날 = 0원) · 10/1 은 창 밖 · 제외 그룹 행은 빠진다
DAYS = [("2026.10.01.", "가짜그룹", 99999), ("2026.10.02.", "가짜그룹", 9000), ("2026.10.03.", "가짜그룹", 8000), ("2026.10.04.", "가짜그룹", 7000),
        ("2026.10.06.", "가짜그룹", 6000), ("2026.10.07.", "가짜그룹", 5000), ("2026.10.08.", "가짜그룹", 4000), ("2026.10.08.", "노원필라테스(삭제)", 50000)]
WIN_SUM, WIN_N = 9000 + 8000 + 7000 + 6000 + 5000 + 4000, 7   # 39,000 / 7일(10/2~10/8)


class ComputeBalance(unittest.TestCase):
    def test_section(self):
        import compute as C
        from reportlib import exclude_groups, load_config
        cfg = load_config()
        kw = frame(DAYS)
        inc = exclude_groups(kw, cfg)
        r = C.balance_card(rec_ok(217817.915506, "2026-10-09T14:34:59+09:00"), kw, inc)
        self.assertEqual(r, {"상태": "ok", "원": 217817, "기준": "10/9(금) 14:34", "창": "10/2~10/8", "창일수": WIN_N, "창합계": WIN_SUM,
                             "일분": 217817 * WIN_N // WIN_SUM})                     # 39 — 평균을 반올림하지 않는 정수 나눗셈
        r = C.balance_card({"status": "fail", "read_at": "2026-10-09T08:00:00+09:00", "reason": "네트워크 오류"}, kw, inc)
        self.assertEqual(r, {"상태": "fail", "기준": "10/9(금) 08:00"})
        z = frame([(d, g, 0) for d, g, _ in DAYS])
        self.assertIsNone(C.balance_card(rec_ok(5000.0, "2026-10-09T14:34:00+09:00"), z, exclude_groups(z, cfg))["일분"])   # 평균 0 → 며칠분 생략
        short = frame([("2026.10.07.", "가짜그룹", 3000), ("2026.10.08.", "가짜그룹", 1000)])        # 첫날보다 앞은 자른다 — 2일 창
        r = C.balance_card(rec_ok(10000.0, "2026-10-09T01:10:00+09:00"), short, exclude_groups(short, cfg))
        self.assertEqual((r["창"], r["창일수"], r["창합계"], r["일분"]), ("10/7~10/8", 2, 4000, 5))
        r = C.balance_card(rec_ok(1.0, "2026-10-09T05:00:00Z"), kw, inc)                 # UTC 로 적힌 기록도 KST 로(05:00Z = 14:00 KST)
        self.assertEqual(r["기준"], "10/9(금) 14:00")

    def test_stale_or_bad_record_fails(self):
        import compute as C
        from reportlib import exclude_groups, load_config
        kw = frame(DAYS)
        inc = exclude_groups(kw, load_config())
        bad = (("지난 회차 기록(읽은 날 = 마지막 날)", rec_ok(1.0, "2026-10-08T23:59:00+09:00"), "집계 마지막 날"),
               ("UTC 로는 9일이지만 KST 8일", rec_ok(1.0, "2026-10-08T14:00:00Z"), "집계 마지막 날"),
               ("상태 없음", {"read_at": "2026-10-09T10:00:00+09:00"}, "꼴"),
               ("시간대 없음", rec_ok(1.0, "2026-10-09T10:00:00"), "꼴"),
               ("bizmoney ≠ ⌊raw⌋", dict(rec_ok(5.5, "2026-10-09T10:00:00+09:00"), bizmoney=6), "꼴"),
               ("bizmoney 문자열", dict(rec_ok(5.5, "2026-10-09T10:00:00+09:00"), bizmoney="5"), "꼴"),
               ("음수", rec_ok(-1.0, "2026-10-09T10:00:00+09:00"), "꼴"))
        for label, rec, frag in bad:
            with self.subTest(label=label):
                with self.assertRaisesRegex(C.BalanceError, frag):
                    C.balance_card(rec, kw, inc)

    def test_cli_missing_file_fails_before_output(self):
        td = tempfile.mkdtemp()
        try:
            o = os.path.join(td, "o.json")
            r = subprocess.run([sys.executable, COMPUTE, os.path.join(td, "없는합본"), "--balance", os.path.join(td, "없는.json"), "-o", o],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("[FAIL] 잔액 기록", r.stdout)
            self.assertFalse(os.path.exists(o))
        finally:
            shutil.rmtree(td, ignore_errors=True)


def card(value, sub):
    return ('<div class="kpi-row">\n    <div class="kpi kpi-wide" style="--accent:#1c2b2a;">\n      <div class="label">광고비 잔액</div>\n'
            f'      <div class="value" data-balance="value">{value}</div>\n      <div class="sub" data-balance="sub">{sub}</div>\n    </div>\n  </div>\n')


class ValidateBalance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            import validate as V
        cls.V = V
        cls.kw = frame(DAYS)
        cls.td = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.td, ignore_errors=True)

    def run_check(self, html, rec, kw=None):
        p = os.path.join(self.td, "b.json")
        if rec is None:
            if os.path.exists(p):
                os.remove(p)
        else:
            with open(p, "w", encoding="utf-8") as f:
                f.write(rec if isinstance(rec, str) else json.dumps(rec))
        self.V.results.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            self.V.check_balance_card(html, self.kw if kw is None else kw, p)
        (name, ok, detail), = self.V.results
        self.assertIn("광고비 잔액 카드", name)
        return ok, detail

    def test_pass_forms(self):
        days = 217817 * WIN_N // WIN_SUM
        ok, d = self.run_check(card('217,817<span class="unit">원</span>', f"10/9(금) 14:34 기준 · 약 {days}일분"), rec_ok(217817.915506, "2026-10-09T14:34:12+09:00"))
        self.assertTrue(ok, d)
        ok, d = self.run_check(card("확인 못 함", "10/9(금) 14:34 조회 실패"), {"status": "fail", "read_at": "2026-10-09T14:34:12+09:00", "reason": "네트워크 오류"})
        self.assertTrue(ok, d)
        z = frame([(d_, g, 0) for d_, g, _ in DAYS])
        ok, d = self.run_check(card('5,000<span class="unit">원</span>', "10/9(금) 14:34 기준"), rec_ok(5000.0, "2026-10-09T14:34:12+09:00"), kw=z)
        self.assertTrue(ok, d)                                                          # 평균 0 → 며칠분 생략 꼴

    def test_fail_forms(self):
        days = 217817 * WIN_N // WIN_SUM
        good_v, good_s = '217,817<span class="unit">원</span>', f"10/9(금) 14:34 기준 · 약 {days}일분"
        ok_rec = rec_ok(217817.915506, "2026-10-09T14:34:12+09:00")
        fail_rec = {"status": "fail", "read_at": "2026-10-09T14:34:12+09:00", "reason": "x"}
        cases = (("값 +1", card('217,818<span class="unit">원</span>', good_s), ok_rec, "값"),
                 ("반올림한 값", card('217,818<span class="unit">원</span>', good_s), ok_rec, "값"),
                 ("시각 +1분", card(good_v, good_s.replace("14:34", "14:35")), ok_rec, "보조 줄"),
                 ("며칠분 +1", card(good_v, good_s.replace(f"약 {days}일분", f"약 {days + 1}일분")), ok_rec, "보조 줄"),
                 ("며칠분 빠짐", card(good_v, "10/9(금) 14:34 기준"), ok_rec, "보조 줄"),
                 ("실패 기록인데 옛 값", card(good_v, "10/9(금) 14:34 조회 실패"), fail_rec, "값"),
                 ("성공 기록인데 확인 못 함", card("확인 못 함", "10/9(금) 14:34 조회 실패"), ok_rec, "값"),
                 ("지난 회차 기록", card(good_v, "10/8(목) 14:34 기준 · 약 1일분"), rec_ok(217817.915506, "2026-10-08T14:34:12+09:00"), "집계 마지막 날"),
                 ("기록 없음", card(good_v, good_s), None, "잔액 기록"),
                 ("기록 JSON 아님", card(good_v, good_s), "{not json", "잔액 기록"),
                 ("카드 0건", "<div class=\"kpi-row\"></div>", ok_rec, "카드"),
                 ("카드 둘", card(good_v, good_s) + card(good_v, good_s), ok_rec, "카드"))
        for label, html, rec, frag in cases:
            with self.subTest(label=label):
                ok, d = self.run_check(html, rec)
                self.assertFalse(ok, d)
                self.assertIn(frag, d)


if __name__ == "__main__":
    unittest.main(verbosity=1)
