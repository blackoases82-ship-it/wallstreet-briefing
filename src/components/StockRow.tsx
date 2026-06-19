import type { StockItem } from "@/types/briefing";
import {
  calculateSafetyMargin,
  calculateUpside,
  getRecommendationLabel,
  getRecommendationTone,
} from "@/lib/calculations";
import {
  changeColorClass,
  formatAfterHours,
  formatPercent,
  formatPrice,
} from "@/lib/formatters";

export function ratingBadgeClass(label: string): string {
  const tone = getRecommendationTone(label);
  switch (tone) {
    case "buy":
      return "bg-red-100 text-red-700";
    case "split":
      return "bg-orange-100 text-orange-700";
    case "watch":
      return "bg-yellow-100 text-yellow-800";
    case "hold":
      return "bg-blue-100 text-blue-700";
    case "avoid":
      return "bg-gray-200 text-gray-600";
    default:
      return "bg-gray-100 text-gray-500";
  }
}

export default function StockRow({ stock }: { stock: StockItem }) {
  const margin = calculateSafetyMargin(stock.closePrice, stock.targetAverage ?? null);
  const upside = calculateUpside(stock.closePrice, stock.targetAverage ?? null);
  const rating = getRecommendationLabel(margin, stock.ticker);

  const cur = stock.currency;

  return (
    <tr className="border-b border-line last:border-0 align-top">
      {/* 종목 (이름 + 티커) — 항상 먼저 보이게 sticky */}
      <td className="sticky left-0 bg-card px-3 py-3 min-w-[120px]">
        <p className="font-bold text-sm leading-tight">{stock.nameKo}</p>
        <p className="text-[11px] text-sub">{stock.ticker}</p>
        <p className="text-[11px] text-sub">{stock.sector}</p>
      </td>

      {/* 종가/시간외 — 안전마진 바로 옆 */}
      <td className="px-3 py-3 whitespace-nowrap">
        <p
          className={`font-bold text-sm ${changeColorClass(
            stock.changePercent
          )}`}
        >
          {formatPrice(stock.closePrice, cur)}
        </p>
        <p className="text-[11px] text-sub">
          시간외 {formatAfterHours(stock.afterHoursPrice, cur)}
        </p>
        {stock.changePercent != null && (
          <p className={`text-[11px] ${changeColorClass(stock.changePercent)}`}>
            {formatPercent(stock.changePercent)}
          </p>
        )}
      </td>

      {/* 안전마진 — 가격 바로 옆 (핵심 규칙) */}
      <td className="px-3 py-3 whitespace-nowrap">
        {margin == null ? (
          <span className="text-xs text-sub">계산 제외</span>
        ) : (
          <span className="inline-block bg-marginBadge text-red-300 font-bold text-sm rounded-lg px-2 py-1">
            {margin.toFixed(1)}%
          </span>
        )}
      </td>

      {/* 목표가 저/평/고 */}
      <td className="px-3 py-3 whitespace-nowrap text-xs">
        <span className="text-sub">저</span>{" "}
        {formatPrice(stock.targetLow ?? null, cur)}
        <br />
        <span className="text-sub">평</span>{" "}
        <span className="font-semibold">
          {formatPrice(stock.targetAverage ?? null, cur)}
        </span>
        <br />
        <span className="text-sub">고</span>{" "}
        {formatPrice(stock.targetHigh ?? null, cur)}
      </td>

      {/* 상승여력 */}
      <td className="px-3 py-3 whitespace-nowrap">
        <span
          className={`text-sm font-semibold ${
            upside == null
              ? "text-sub"
              : upside >= 0
              ? "text-up"
              : "text-down"
          }`}
        >
          {upside == null ? "-" : formatPercent(upside)}
        </span>
      </td>

      {/* 등급 */}
      <td className="px-3 py-3 whitespace-nowrap">
        <span
          className={`inline-block text-[11px] font-bold rounded-full px-2 py-1 ${ratingBadgeClass(
            rating
          )}`}
        >
          {rating}
        </span>
      </td>

      {/* 핵심 뉴스 */}
      <td className="px-3 py-3 text-xs text-gray-300 min-w-[200px]">
        {stock.keyNews}
        {stock.riskNote && (
          <span className="block mt-1 text-[11px] text-red-600 font-semibold">
            ⚠ {stock.riskNote}
          </span>
        )}
        {stock.dataTime && (
          <span className="block mt-1 text-[10px] text-sub">
            기준 {stock.dataTime}
          </span>
        )}
      </td>
    </tr>
  );
}
