#!/usr/bin/env python3
"""시험용 변경 이력 엑셀(xlsx) 만들기 — 표준 라이브러리 zipfile 만(2026-10-12 추가 수집 B 시험 · 실제 계정·아이디 0).

광고주센터 `이력 목록 YYYYMMDD HHMM.xlsx` 꼴(탐색 전문 2-4 실측): 시트 `Sheet` · 공유 문자열 · 머리 `변경일자,변경 유형,변경자,캠페인,광고그룹,변경 내용` ·
**SYSTEM 줄은 캠페인·광고그룹 셀이 아예 없다(셀 4개 — `r` 속성 열 글자로만 맞음)** · 변경 내용은 `\\n` 여러 줄.
줄은 [값 | None] 목록 — None 이면 그 셀을 쓰지 않는다(빈 셀이 빠진 줄 재현).
"""
import zipfile
from xml.sax.saxutils import escape

HEADER = ["변경일자", "변경 유형", "변경자", "캠페인", "광고그룹", "변경 내용"]
FAKE = "tester01"   # 가짜 아이디(시험이 결과 파일·요약·로그에 이 글자가 0 인지 본다)

# 탐색 실측 갈래를 흉내 낸 가짜 줄(기간 2026.08.30.~2026.09.28. 안) — 사람 4 · 스킬 등록 2(같은 분 2줄 = 실행 1회) + 삭제 1 · SYSTEM 1(셀 4개) ·
# 같은 줄 두 번(같은 분 On/Off) · 앞뒤 공백 칸 · LF 칸
SAMPLE = [
    ["2026.09.28. 01:20", "타겟팅 변경", f"{FAKE}:naver(API)", "새로필라테스 파워링크", "상계동필라테스", "상계동필라테스\n등록된 내용\n확장 검색: 가짜검색어A, 가짜검색어B"],
    ["2026.09.28. 01:20", "타겟팅 변경", f"{FAKE}:naver(API)", "새로필라테스 파워링크", "노원역필라테스", "노원역필라테스\n등록된 내용\n확장 검색: 가짜검색어A, 가짜검색어B"],
    ["2026.09.27. 22:46", "광고그룹 하루예산 중단", "SYSTEM", None, None, "새로필라테스\n설정 값\n하루예산 사용여부: 사용함\n하루예산: 20,000원"],
    ["2026.09.27. 13:59", "타겟팅 변경", f"{FAKE}:naver(API)", "새로필라테스 파워링크", "상계동필라테스", "상계동필라테스\n삭제된 내용\n확장 검색: SAERO제외테스트"],
    ["2026.09.20. 15:30", "광고그룹 On/Off", f"{FAKE}:naver", "플레이스#1", "새로필라테스", "새로필라테스\n변경 전\nOn/Off: OFF\n변경 후\nOn/Off: ON"],
    ["2026.09.20. 15:30", "광고그룹 On/Off", f"{FAKE}:naver", "플레이스#1", "새로필라테스", "새로필라테스\n변경 전\nOn/Off: OFF\n변경 후\nOn/Off: ON"],
    ["2026.09.20. 15:30", "광고그룹 변경", f"{FAKE}:naver", "플레이스#1", "새로필라테스", "새로필라테스\n변경 전\n하루예산: 10,000원\n변경 후\n하루예산: 20,000원"],
    ["2026.09.17. 08:22", "타겟팅 변경", f"{FAKE}:naver", "플레이스#1", " 새로필라테스 ", "\n변경 전\n제외키워드: \n변경 후\n제외키워드: 가가, 나나, 다다"],
]


def _col(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def write_xlsx(path, rows, header=HEADER):
    """header + rows → xlsx(공유 문자열). rows 의 None 은 셀 자체를 쓰지 않는다."""
    strings, index = [], {}

    def sid(v):
        if v not in index:
            index[v] = len(strings)
            strings.append(v)
        return index[v]
    body = []
    for rn, row in enumerate([header] + list(rows), 1):
        cells = []
        for ci, v in enumerate(row):
            if v is None:
                continue
            cells.append(f'<c r="{_col(ci)}{rn}" t="s"><v>{sid(v)}</v></c>')
        body.append(f'<row r="{rn}">{"".join(cells)}</row>')
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    rns = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    sheet = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet {ns}><sheetData>{"".join(body)}</sheetData></worksheet>'
    sst = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sst {ns} count="{len(strings)}" uniqueCount="{len(strings)}">'
           + "".join(f'<si><t xml:space="preserve">{escape(s)}</t></si>' for s in strings) + "</sst>")
    wb = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook {ns} {rns}><sheets>'
          '<sheet name="Sheet" sheetId="1" r:id="rId1"/></sheets></workbook>')
    wbrels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
              '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
              '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
              "</Relationships>")
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>")
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
          '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wbrels)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
        z.writestr("xl/sharedStrings.xml", sst)
    return path
