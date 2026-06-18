import type { StockItem } from "@/types/briefing";
import {
  calculateSafetyMargin,
  getRecommendationLabel,
} from "@/lib/calculations";
import {
  changeColorClass,
  formatAfterHours,
  formatPercent,
  formatPrice,
} from "@/lib/formatters";
import { ratingBadgeClass } from "./StockRow";

type Props = {
  stocks: StockItem[];
};

export default function KoreanMarketFocus({ stocks }: Props) {
  const krStocks = stocks.filter((s) => s.market === "KR");
  if (krStocks.length === 0) return null;

  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">
        오늘 국내장 관심/추천
      </h2>
      <p className="text-[11px] text-sub mb-2 px-1">
        한국장 개장 전 · 미국장 흐름 반영
      </p>

      <div className="space-y-3">
        {krStocks.map((s) => {
          const margin = calculateSafetyMargin(
            s.closePrice,
            s.targetAverage ?? null
          );
          const rating = getRecommendationLabel(margin, s.ticker);

          return (
            <div
              key={s.ticker}
              className="bg-white rounded-2xl shadow-card px-4 py-3"
            >
              <div className="flex items-center justify-between gap-2">
                <p className="font-bold text-[15px]">{s.nameKo}</p>
                <span
                  className={`text-[11px] font-bold rounded-full px-2 py-1 ${ratingBadgeClass(
                    rating
                  )}`}
                >
                  {rating}
                </span>
              </div>

              {/* 종가 / 시간외 / 안전마진 — 한 줄에 붙여서 */}
              <p className="mt-1 text-sm">
                <span
                  className={`font-bold ${changeColorClass(s.changePercent)}`}
                >
                  종가 {formatPrice(s.closePrice, "KRW")}
                </span>
                <span className="text-sub">
                  {" "}
                  / 시간외 {formatAfterHours(s.afterHoursPrice, "KRW")}
                </span>
                {margin != null && (
                  <span className="ml-2 inline-block bg-marginBadge text-red-700 font-bold rounded-lg px-2 py-0.5 text-xs">
                    안전마진 {margin.toFixed(1)}%
                  </span>
                )}
              </p>

              {/* 목표가 저/평/고 */}
              <p className="mt-1 text-xs text-gray-700">
                목표가 저/평/고 {formatPrice(s.targetLow ?? null, "KRW")} /{" "}
                <span className="font-semibold">
                  {formatPrice(s.targetAverage ?? null, "KRW")}
                </span>{" "}
                / {formatPrice(s.targetHigh ?? null, "KRW")}
              </p>

              <p className="mt-1 text-xs text-sub">오늘 체크: {s.keyNews}</p>
              {s.riskNote && (
                <p className="mt-1 text-[11px] text-red-600 font-semibold">
                  ⚠ {s.riskNote}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
