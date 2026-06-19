import type { MarketCapItem } from "@/types/briefing";
import { changeColorClass, formatPercent } from "@/lib/formatters";

type Props = {
  data?: { asOf: string; items: MarketCapItem[] };
};

export default function UsMarketCapTop10({ data }: Props) {
  if (!data || data.items.length === 0) return null;

  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">
        🇺🇸 미국 시가총액 Top 10
      </h2>
      <div className="bg-card rounded-2xl shadow-card border border-line overflow-hidden">
        <ul>
          {data.items.map((it) => (
            <li
              key={it.rank}
              className="flex items-center gap-3 px-4 py-2.5 border-b border-line last:border-0"
            >
              <span className="w-5 text-center text-sm font-bold text-sub flex-none">
                {it.rank}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-bold leading-tight truncate">
                  {it.nameKo}{" "}
                  <span className="text-[11px] text-sub font-normal">
                    {it.ticker}
                  </span>
                </p>
              </div>
              <span className="text-sm font-semibold tabular-nums">
                {it.marketCap}
              </span>
              <span
                className={`w-16 text-right text-xs font-semibold tabular-nums ${changeColorClass(
                  it.changePercent
                )}`}
              >
                {it.changePercent == null ? "-" : formatPercent(it.changePercent)}
              </span>
            </li>
          ))}
        </ul>
      </div>
      <p className="text-[11px] text-sub mt-1 px-1">{data.asOf}</p>
    </section>
  );
}
