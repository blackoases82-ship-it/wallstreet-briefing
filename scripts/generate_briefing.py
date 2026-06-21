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
    {"sector": "헬스케어(XLV)", "yf": "XLV"},
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


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    prev_stocks = {s["ticker"]: s for s in data.get("stocks", [])}
    now = datetime.now(KST)
    stamp = now.strftime("%Y. %-m. %-d. ") + ("오전 " if now.hour < 12 else "오후 ") + now.strftime("%-I:%M KST")

    # --- 종목 ---
    new_stocks = []
    for meta in STOCKS:
        sym = meta["yf"]
        print(f"[stock] {meta['ticker']} ({sym})")
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
        data["usMarketCap"] = {"asOf": f"美 직전 종가 기준 (자동·{now.strftime('%Y-%m-%d')})", "items": caps}

    # --- 메타 ---
    data["generatedAt"] = stamp
    # news / finalAnalysis / economicCalendar / title / oneLineConclusion : 기존 보존
    # (확장: ANTHROPIC_API_KEY 가 있으면 여기서 LLM 으로 재생성하도록 추가 가능)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n완료: {JSON_PATH} ({len(new_stocks)} stocks, generatedAt={stamp})")


if __name__ == "__main__":
    main()
