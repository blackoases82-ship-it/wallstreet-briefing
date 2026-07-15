#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
나만의 월스트리트 - 일일 데이터 자동 생성기 (GitHub Actions용)

- yfinance로 관심종목/지수/거시/섹터ETF/시총을 받아 src/data/briefing.json 의
'숫자' 부분을 갱신한다.
- 뉴스(news) / 최종분석(finalAnalysis) / 경제캘린더(economicCalendar) / 제목(title) /
oneLineConclusion 은 기존 파일 값을 그대로 보존한다(LLM 없이 자동 생성 불가하므로).
=> 나중에 ANTHROPIC_API_KEY 를 붙이면 이 부분도 자동화 가능(확장 지점 표시).
- 값을 못 받은 항목은 기존 JSON 값을 유지(앱이 빈칸/깨짐 없이 항상 동작).

실행: python scripts/generate_briefing.py
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta

import yfinance as yf

KST = timezone(timedelta(hours=9))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "src", "data", "briefing.json")

# ---------------------------------------------------------------------------
# 관심종목 메타데이터 (티커 → 표시정보). 시세/목표가는 yfinance로 채운다.
# riskNote 가 있으면 고변동 라벨로 사용.
# ---------------------------------------------------------------------------
STOCKS = [
# ① 반도체
{"ticker": "삼성전자", "yf": "005930.KS", "nameKo": "삼성전자", "sector": "반도체", "market": "KR", "currency": "KRW"},
{"ticker": "SK하이닉스", "yf": "000660.KS", "nameKo": "SK하이닉스", "sector": "반도체", "market": "KR", "currency": "KRW"},
{"ticker": "NVDA", "yf": "NVDA", "nameKo": "엔비디아", "nameEn": "NVIDIA", "sector": "반도체", "market": "US", "currency": "USD"},
{"ticker": "AVGO", "yf": "AVGO", "nameKo": "브로드컴", "nameEn": "Broadcom", "sector": "반도체", "market": "US", "currency": "USD"},
{"ticker": "SNPS", "yf": "SNPS", "nameKo": "시놉시스", "nameEn": "Synopsys", "sector": "반도체", "market": "US", "currency": "USD"},
{"ticker": "TSM", "yf": "TSM", "nameKo": "TSMC", "nameEn": "Taiwan Semiconductor", "sector": "반도체", "market": "US", "currency": "USD"},
{"ticker": "INTC", "yf": "INTC", "nameKo": "인텔", "nameEn": "Intel", "sector": "반도체", "market": "US", "currency": "USD"},
{"ticker": "QCOM", "yf": "QCOM", "nameKo": "퀄컴", "nameEn": "Qualcomm", "sector": "반도체", "market": "US", "currency": "USD"},
{"ticker": "MRVL", "yf": "MRVL", "nameKo": "마벨테크놀로지", "nameEn": "Marvell", "sector": "반도체", "market": "US", "currency": "USD"},
{"ticker": "SNDK", "yf": "SNDK", "nameKo": "샌디스크", "nameEn": "Sandisk", "sector": "반도체", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
# ② 빅테크·플랫폼
{"ticker": "MSFT", "yf": "MSFT", "nameKo": "마이크로소프트", "nameEn": "Microsoft", "sector": "기술", "market": "US", "currency": "USD"},
{"ticker": "META", "yf": "META", "nameKo": "메타", "nameEn": "Meta Platforms", "sector": "커뮤니케이션", "market": "US", "currency": "USD"},
{"ticker": "AMZN", "yf": "AMZN", "nameKo": "아마존", "nameEn": "Amazon", "sector": "임의소비", "market": "US", "currency": "USD"},
{"ticker": "GOOGL", "yf": "GOOGL", "nameKo": "알파벳(구글)", "nameEn": "Alphabet", "sector": "커뮤니케이션", "market": "US", "currency": "USD"},
{"ticker": "AAPL", "yf": "AAPL", "nameKo": "애플", "nameEn": "Apple", "sector": "기술", "market": "US", "currency": "USD"},
{"ticker": "NAVER", "yf": "035420.KS", "nameKo": "네이버", "sector": "커뮤니케이션", "market": "KR", "currency": "KRW"},
# ③ AI SW·데이터
{"ticker": "PLTR", "yf": "PLTR", "nameKo": "팔란티어", "nameEn": "Palantir", "sector": "기술", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
{"ticker": "ORCL", "yf": "ORCL", "nameKo": "오라클", "nameEn": "Oracle", "sector": "기술", "market": "US", "currency": "USD"},
{"ticker": "IBM", "yf": "IBM", "nameKo": "아이비엠", "nameEn": "IBM", "sector": "기술", "market": "US", "currency": "USD"},
# ④ 양자컴퓨팅
{"ticker": "RGTI", "yf": "RGTI", "nameKo": "리게티컴퓨팅", "nameEn": "Rigetti Computing", "sector": "양자컴퓨팅", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
{"ticker": "IONQ", "yf": "IONQ", "nameKo": "아이온큐", "nameEn": "IonQ", "sector": "양자컴퓨팅", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
# ⑤ 우주·위성
{"ticker": "RKLB", "yf": "RKLB", "nameKo": "로켓랩", "nameEn": "Rocket Lab", "sector": "우주", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
{"ticker": "ASTS", "yf": "ASTS", "nameKo": "AST스페이스모바일", "nameEn": "AST SpaceMobile", "sector": "우주/통신", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
{"ticker": "SPCX", "yf": "SPCX", "nameKo": "스페이스X", "nameEn": "SpaceX", "sector": "우주", "market": "US", "currency": "USD", "riskNote": "상장 직후 · 컨센서스 형성 초기"},
# ⑥ 에너지·전력·원전
{"ticker": "두산에너빌리티", "yf": "034020.KS", "nameKo": "두산에너빌리티", "sector": "산업/원전", "market": "KR", "currency": "KRW"},
{"ticker": "CEG", "yf": "CEG", "nameKo": "컨스털레이션에너지", "nameEn": "Constellation Energy", "sector": "유틸리티/원전", "market": "US", "currency": "USD"},
{"ticker": "BE", "yf": "BE", "nameKo": "블룸에너지", "nameEn": "Bloom Energy", "sector": "에너지", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
{"ticker": "FLNC", "yf": "FLNC", "nameKo": "플루언스에너지", "nameEn": "Fluence Energy", "sector": "에너지", "market": "US", "currency": "USD", "riskNote": "초고위험 변동성 종목"},
# ⑦ 모빌리티·EV
{"ticker": "현대차", "yf": "005380.KS", "nameKo": "현대차", "sector": "임의소비", "market": "KR", "currency": "KRW"},
{"ticker": "TSLA", "yf": "TSLA", "nameKo": "테슬라", "nameEn": "Tesla", "sector": "임의소비", "market": "US", "currency": "USD", "riskNote": "변동성 큰 종목"},
# ⑧ 데이터센터·채굴
{"ticker": "IREN", "yf": "IREN", "nameKo": "아이렌", "nameEn": "IREN", "sector": "에너지/AI", "market": "US", "currency": "USD", "riskNote": "변동성 큰 종목"},
]

INDEXES = [
{"name": "다우존스", "yf": "^DJI"},
{"name": "S&P 500", "yf": "^GSPC"},
{"name": "나스닥", "yf": "^IXIC"},
{"name": "러셀 2000", "yf": "^RUT"},
]

SECTOR_ETFS = [
{"sector": "기술(XLK)", "yf": "XLK"},
{"sector": "경기소비재(XLY)", "yf": "XLY"},
{"sector": "산업재(XLI)", "yf": "XLI"},
{"sector": "유틸리티(XLU)", "yf": "XLU"},
{"sector": "커뮤니케이션(XLC)", "yf": "XLC"},
{"sector": "필수소비재(XLP)", "yf": "XLP"},
{"sector": "여스케어(XLV)", "yf": "XLV"},
{"sector": "금융(XLF)", "yf": "XLF"},
{"sector": "에너지(XLE)", "yf": "XLE"},
]

MARKETCAP = [
{"ticker": "NVDA", "nameKo": "엔비디아"},
{"ticker": "GOOGL", "nameKo": "알파벳(구글)"},
{"ticker": "AAPL", "nameKo": "애플"},
{"ticker": "MSFT", "nameKo": "마이크로소프트"},
{"ticker": "AMZN", "nameKo": "아마존"},
{"ticker": "TSM", "nameKo": "TSMC"},
{"ticker": "AVGO", "nameKo": "브로드컴"},
{"ticker": "TSLA", "nameKo": "테슬라"},
{"ticker": "META", "nameKo": "메타"},
{"ticker": "BRK-B", "nameKo": "버크셔해서웨이"},
]

def round_price(v, currency):
    if v is None:
        return None
    return int(round(v)) if currency == "KRW" else round(float(v), 2)

def quote(sym, retries=3):
    """(price, prevClose, changePct) — fast_info 우선, 실패 시 history."""
    last_err = None
    for _ in range(retries):
        try:
            t = yf.Ticker(sym)
            price = prev = None
            try:
                fi = t.fast_info
                price = fi.get("last_price") or fi.get("lastPrice")
                prev = fi.get("previous_close") or fi.get("previousClose")
            except Exception:
                pass
            if price is None or prev is None:
                h = t.history(period="5d")
                if len(h) >= 2:
                    price = float(h["Close"].iloc[-1])
                    prev = float(h["Close"].iloc[-2])
                elif len(h) == 1:
                    price = float(h["Close"].iloc[-1])
                    prev = float(h["Open"].iloc[-1])
            if price is not None and prev:
                chg = (price - prev) / prev * 100.0
                return float(price), float(prev), round(chg, 2)
            if price is not None:
                return float(price), None, None
        except Exception as e:  # noqa
            last_err = e
            time.sleep(1.5)
    print(f"  ! quote 실패 {sym}: {last_err}", file=sys.stderr)
    return None, None, None
def info_targets(sym, retries=2):
    for _ in range(retries):
        try:
            info = yf.Ticker(sym).info
            return (
                info.get("targetLowPrice"),
                info.get("targetMeanPrice"),
                info.get("targetHighPrice"),
                info.get("marketCap"),
                info.get("regularMarketChangePercent"),
            )
        except Exception:
            time.sleep(1.5)
    return None, None, None, None, None

def fmt_cap(v):
    if not v:
        return None
    t = v / 1e12
    if t >= 1:
        return f"${t:.2f}T"
    return f"${v/1e9:.0f}B"

# ---------------------------------------------------------------------------
# (선택) 뉴스/분석 자동화: ANTHROPIC_API_KEY 가 있으면
# 1) yfinance로 '실제 헤드라인'을 수집하고
# 2) 그 헤드라인 + 오늘 수치만 근거로 Anthropic API가 한국어 뉴스/분석을 생성한다.
# => 모델이 사실을 지어내지 않도록, 제공된 헤드라인/수치 밖의 구체사실 생성을 금지한다.
# 키가 없거나 실패하면 기존 news/finalAnalysis/oneLineConclusion 을 그대로 보존한다.
# ---------------------------------------------------------------------------
HEADLINE_TICKERS = [
    "NVDA", "INTC", "TSM", "AVGO", "MRVL", "QCOM", "MSFT", "META",
    "AMZN", "GOOGL", "AAPL", "PLTR", "TSLA", "SNDK", "005930.KS", "000660.KS",
]

def gather_headlines(symbols, per=5, limit=22):
    items, seen = [], set()
    for sym in symbols:
        try:
            news = yf.Ticker(sym).news or []
        except Exception:
            news = []
        for n in news[:per]:
            title = pub = date = None
            content = n.get("content") if isinstance(n, dict) else None
            if content:  # 신 스키마
                title = content.get("title")
                pub = (content.get("provider") or {}).get("displayName")
                date = content.get("pubDate") or content.get("displayTime")
            else:  # 구 스키마
                title = n.get("title")
                pub = n.get("publisher")
                ts = n.get("providerPublishTime")
                if ts:
                    try:
                        date = datetime.fromtimestamp(ts, KST).strftime("%Y-%m-%d")
                    except Exception:
                        date = None
            if title and title not in seen:
                seen.add(title)
                items.append({"ticker": sym, "title": title, "publisher": pub, "date": date})
    return items[:limit]

def llm_generate(data, headlines, weekday_ko="", kr_data_date="", us_data_date=""):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return False
    import requests
    model = os.environ.get("BRIEFING_MODEL", "claude-sonnet-4-6")

    idx = "; ".join(f"{i['name']} {i['value']} ({i.get('changePercent')}%)" for i in data.get("marketIndexes", []))
    movers = sorted(
        [s for s in data["stocks"] if isinstance(s.get("changePercent"), (int, float))],
        key=lambda s: s["changePercent"],
    )
    top_up = "; ".join(f"{s['ticker']} {s['changePercent']:+.1f}%" for s in movers[-6:][::-1])
    top_dn = "; ".join(f"{s['ticker']} {s['changePercent']:+.1f}%" for s in movers[:5])
    macro = "; ".join(f"{m['name']} {m['value']} ({m.get('note', '')})" for m in data.get("macroIndicators", []))
    strong = "; ".join(f"{x['sector']} {x['changePercent']:+.1f}%" for x in data["sectorRotation"]["strong"])
    weak = "; ".join(f"{x['sector']} {x['changePercent']:+.1f}%" for x in data["sectorRotation"]["weak"])
    kr_actual = "; ".join(
        f"{s['ticker']} {s['closePrice']:,}원 ({s.get('changePercent') or 0:+.1f}%)"
        for s in data.get("stocks", [])
        if s.get("market") == "KR" and s.get("closePrice") is not None
    )
    heads = "\n".join(
        f"- [{h['ticker']}] {h['title']} ({h.get('publisher') or ''}, {h.get('date') or ''})" for h in headlines
    ) or "(수집된 헤드라인 없음 — 이 경우 뉴스는 비우고 분석만 작성)"

    # 요일 컨텍스트
    weekday_line = f"({weekday_ko})" if weekday_ko else ""
    kr_date_line = kr_data_date or data.get("generatedAt", "")
    us_date_line = us_data_date or ""

    prompt = f"""당신은 한국어 투자 모닝 브리핑 에디터다. 아래 '오늘 데이터'와 '실제 헤드라인'에만 근거해 작성한다.
규칙: 제공되지 않은 구체 사실(수치/계약/발언/날짜)은 절대 지어내지 말 것. 불확실한 소문은 confidence를 "low"로 하고 source 끝에 "(미확정)"을 붙인다. 시적이되 간결하게, 단정은 피한다.
★★★ 요일 규칙(절대 최우선) ★★★: 이 브리핑을 읽는 독자의 요일은 반드시 {weekday_ko if weekday_ko else '(요일정보없음)'}이다. oneLineConclusion의 첫 단어는 반드시 "{weekday_ko if weekday_ko else '오늘'}"이어야 한다. 시장 이벤트가 전날 발생했어도 독자 기준 요일({weekday_ko if weekday_ko else '오늘'})로 시작한다. 올바른 예: "{weekday_ko if weekday_ko else '오늘'} 아침, 어제 시장은...". 절대 금지: "{weekday_ko if weekday_ko else '오늘'}"이 아닌 다른 요일 단어로 시작하는 것.

[한국시장 기준일] {kr_date_line} {weekday_line}
[미국시장 기준일] {us_date_line} (직전 미국 종가)
[지수] {idx}
[강세섹터] {strong}
[약세섹터] {weak}
[상승상위] {top_up}
[하락상위] {top_dn}
[거시] {macro}
[한국주요주가·실측치(이 수치만 기사에 사용, 날조 금지)]
{kr_actual}
[실제 헤드라인]
{heads}

아래 JSON만 출력한다(코드펜스/설명 금지). 모든 텍스트는 한국어.
{{
"oneLineConclusion": "한 줄 결론(반드시 {weekday_ko if weekday_ko else '오늘'}로 시작, 지수/등락 수치 1~2개 포함)",
"news": [{{"category":"official|analyst|overseas|chatter|rumor","title":"제목","summaryKo":"2~3문장 한국어 요약","relatedTickers":["TICKER"],"impact":"positive|negative|neutral|mixed","confidence":"high|medium|low","source":"매체명","publishedAt":"YYYY-MM-DD"}}],
"finalAnalysis": {{"marketDiagnosis":"3~4문장","sectorRotationAnalysis":"2~3문장","koreanMarketStrategy":"3~4문장","usPortfolioStrategy":"3~4문장","topOpportunities":["3개 항목"],"topRisks":["3개 항목"],"actionPlan":["5개 항목"]}}
}}
news는 위 헤드라인을 근거로 5~7개. 헤드라인이 없으면 news는 빈 배열 []."""

    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": model, "max_tokens": 3500, "messages": [{"role": "user", "content": prompt}]},
            timeout=120,
        )
        r.raise_for_status()
        txt = "".join(b.get("text", "") for b in r.json().get("content", []) if b.get("type") == "text")
        s, e = txt.find("{"), txt.rfind("}")
        obj = json.loads(txt[s:e + 1])
        if isinstance(obj.get("news"), list) and obj["news"]:
            data["news"] = obj["news"]
        if isinstance(obj.get("finalAnalysis"), dict) and obj["finalAnalysis"]:
            data["finalAnalysis"] = obj["finalAnalysis"]
        if obj.get("oneLineConclusion"):
            conclusion = obj["oneLineConclusion"]
            # 요일 강제 교정: LLM이 규칙을 무시해도 코드로 보정
            if weekday_ko and not conclusion.startswith(weekday_ko):
                _days = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]
                replaced = False
                for d in _days:
                    if conclusion.startswith(d):
                        conclusion = weekday_ko + conclusion[len(d):]
                        replaced = True
                        print(f" ⚠ 요일 교정: {d} → {weekday_ko}")
                        break
                if not replaced:
                    conclusion = f"{weekday_ko} 아침, " + conclusion
                    print(f" ⚠ 요일 접두 추가: {weekday_ko}")
            data["oneLineConclusion"] = conclusion
        print(f"  LLM 뉴스/분석 갱신 완료 (model={model}, news={len(obj.get('news', []))})")
        return True
    except Exception as ex:  # noqa
        print(f"  ! LLM 단계 실패 — 기존 뉴스/분석 보존: {ex}", file=sys.stderr)
        return False

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    prev_stocks = {s["ticker"]: s for s in data.get("stocks", [])}
    now = datetime.now(KST)
    stamp = now.strftime("%Y. %-m. %-d. ") + ("오전 " if now.hour < 12 else "오후 ") + now.strftime("%-I:%M KST")
    # 요일 및 날짜 변수 (LLM 프롬프트용)
    WEEKDAYS_KO = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    weekday_ko = WEEKDAYS_KO[now.weekday()]
    kr_data_date = now.strftime("%Y-%m-%d")
    # 미국 시장 직전 종가 날짜: 월요일이면 지난 금요일, 일요일이면 지난 금요일, 그 외는 전일
    us_day = now.date()
    if now.weekday() == 0:  # 월요일 → 금요일
        us_day -= timedelta(days=3)
    elif now.weekday() == 6:  # 일요일 → 금요일
        us_day -= timedelta(days=2)
    else:
        us_day -= timedelta(days=1)
    us_data_date = us_day.strftime("%Y-%m-%d")

    # --- 종목 ---
    new_stocks = []
    for meta in STOCKS:
        sym = meta["yf"]
        print(f"[stock] {meta['ticker']} ({sym})")
        # SPCX(SpaceX): 비상장 — yfinance 호출 금지, null 유지
        if meta.get("ticker") == "SPCX":
            old_item = prev_stocks.get("SPCX", {})
            new_stocks.append({
                "ticker": "SPCX", "nameKo": meta["nameKo"], "nameEn": meta.get("nameEn",""),
                "sector": meta["sector"], "market": meta["market"], "currency": meta.get("currency","USD"),
                "closePrice": None, "afterHoursPrice": None, "changePercent": None,
                "targetLow": None, "targetAverage": None, "targetHigh": None,
                "keyNews": old_item.get("keyNews",""), "dataTime": old_item.get("dataTime",""),
                "riskNote": meta.get("riskNote", old_item.get("riskNote")),
            })
            continue
        price, _, chg = quote(sym)
        tlow, tmean, thigh, _, info_chg = info_targets(sym)
        if chg is None:
            chg = round(info_chg, 2) if info_chg is not None else None
        old = prev_stocks.get(meta["ticker"], {})
        cur = meta.get("currency", "USD")
        item = {
            "ticker": meta["ticker"],
            "nameKo": meta["nameKo"],
            "sector": meta["sector"],
            "market": meta["market"],
            "currency": cur,
            "closePrice": round_price(price, cur) if price is not None else old.get("closePrice"),
            "afterHoursPrice": None,
            "changePercent": chg if chg is not None else old.get("changePercent"),
            "targetLow": round_price(tlow, cur) if tlow else old.get("targetLow"),
            "targetAverage": round_price(tmean, cur) if tmean else old.get("targetAverage"),
            "targetHigh": round_price(thigh, cur) if thigh else old.get("targetHigh"),
            # keyNews/분석성 문구는 기존 보존
            "keyNews": old.get("keyNews", ""),
            "dataTime": ("韓 직전 종가 (자동)" if meta["market"] == "KR" else "美 직전 종가 (자동)"),
        }
        if "nameEn" in meta:
            item["nameEn"] = meta["nameEn"]
        rn = meta.get("riskNote") or old.get("riskNote")
        if rn:
            item["riskNote"] = rn
        new_stocks.append(item)
    data["stocks"] = new_stocks

    # --- 지수 ---
    new_idx = []
    old_idx = {i["name"]: i for i in data.get("marketIndexes", [])}
    for meta in INDEXES:
        price, _, chg = quote(meta["yf"])
        o = old_idx.get(meta["name"], {})
        new_idx.append({
            "name": meta["name"],
            "value": f"{price:,.0f}" if price is not None else o.get("value", "-"),
            "changePercent": chg if chg is not None else o.get("changePercent"),
        })
    data["marketIndexes"] = new_idx

    # --- 거시 ---
    def macro_dir(chg):
        if chg is None:
            return "unknown"
        if chg > 0.05:
            return "up"
        if chg < -0.05:
            return "down"
        return "flat"

    macro = []
    krw_p, _, krw_c = quote("KRW=X")
    gold_p, _, gold_c = quote("GC=F")
    silver_p, _, silver_c = quote("SI=F")
    vix_p, _, vix_c = quote("^VIX")
    tnx_p, _, _ = quote("^TNX")
    dxy_p, _, dxy_c = quote("DX-Y.NYB")
    old_macro = {m["name"]: m for m in data.get("macroIndicators", [])}
    if krw_p:
        macro.append({"name": "원/달러", "value": f"{krw_p:,.0f}", "direction": macro_dir(krw_c), "note": f"전일比 {krw_c:+.1f}%" if krw_c is not None else ""})
    if gold_p:
        macro.append({"name": "금", "value": f"${gold_p:,.0f}", "direction": macro_dir(gold_c), "note": f"{gold_c:+.1f}%" if gold_c is not None else ""})
    if silver_p:
        macro.append({"name": "은", "value": f"${silver_p:,.0f}", "direction": macro_dir(silver_c), "note": f"{silver_c:+.1f}%" if silver_c is not None else ""})
    if vix_p:
        macro.append({"name": "VIX", "value": f"{vix_p:.1f}", "direction": macro_dir(vix_c), "note": f"{vix_c:+.1f}%" if vix_c is not None else ""})
    if tnx_p:
        macro.append({"name": "美10년물", "value": f"{tnx_p:.2f}%", "direction": "flat"})
    # 공포·탐욕 지수는 yfinance에 없음 → 기존 값 보존
    if "공포·탐욕" in old_macro:
        macro.append(old_macro["공포·탐욕"])
    if macro:
        data["macroIndicators"] = macro

    # --- 섹터 순환 ---
    moves = []
    for meta in SECTOR_ETFS:
        _, _, chg = quote(meta["yf"])
        if chg is not None:
            moves.append({"sector": meta["sector"], "changePercent": round(chg, 1)})
    if moves:
        moves.sort(key=lambda x: x["changePercent"], reverse=True)
        data["sectorRotation"] = {"strong": moves[:4], "weak": moves[-4:][::-1]}

    # --- 미국 시총 Top10 ---
    caps = []
    for i, meta in enumerate(MARKETCAP, 1):
        _, _, chg = quote(meta["ticker"])
        _, _, _, cap, _ = info_targets(meta["ticker"])
        caps.append({
            "rank": i, "ticker": meta["ticker"], "nameKo": meta["nameKo"],
            "marketCap": fmt_cap(cap) or "-",
            "changePercent": round(chg, 1) if chg is not None else None,
        })
    if any(c["marketCap"] != "-" for c in caps):
        data["usMarketCap"] = {"asOf": f"美 직전 종가 기준 (자동·{us_data_date})", "items": caps}

    # 뉴스/분석: ANTHROPIC_API_KEY 있으면 실제 헤드라인+수치 기반으로 LLM 자동 생성,
    # 없거나 실패하면 기존 news/finalAnalysis/oneLineConclusion 보존.
    # economicCalendar / title 은 항상 기존 보존.
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("[llm] 헤드라인 수집 + 뉴스/분석 자동 생성")
        try:
            heads = gather_headlines(HEADLINE_TICKERS)
            print(f"  헤드라인 {len(heads)}건 수집")
            llm_generate(data, heads, weekday_ko=weekday_ko, kr_data_date=kr_data_date, us_data_date=us_data_date)
        except Exception as ex:  # noqa
            print(f"  ! 뉴스/분석 자동화 건너뜀(기존 보존): {ex}", file=sys.stderr)

    # --- 메타 (LLM 호출 이후에 기록해 정확한 완료 시각 반영) ---
    data["generatedAt"] = stamp

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n완료: {JSON_PATH} ({len(new_stocks)} stocks, generatedAt={stamp})")

if __name__ == "__main__":
    main()
