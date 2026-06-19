import type { MarketIndex } from "@/types/briefing";
import { changeColorClass, formatPercent } from "@/lib/formatters";

type Props = {
  indexes: MarketIndex[];
};

export default function MarketIndexGrid({ indexes }: Props) {
  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">시장 현황</h2>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {indexes.map((idx) => (
          <div
            key={idx.name}
            className="bg-card rounded-2xl shadow-card px-4 py-3 border border-line"
          >
            <p className="text-xs text-sub">{idx.name}</p>
            <p className="text-xl font-extrabold mt-1">
              {idx.value || "확인중"}
            </p>
            <p
              className={`text-sm font-semibold mt-0.5 ${changeColorClass(
                idx.changePercent
              )}`}
            >
              {idx.changePercent == null ? "-" : formatPercent(idx.changePercent)}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
