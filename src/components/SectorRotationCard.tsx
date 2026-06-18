import type { SectorMove } from "@/types/briefing";
import { formatPercent } from "@/lib/formatters";

type Props = {
  strong: SectorMove[];
  weak: SectorMove[];
};

function SectorList({
  title,
  items,
  tone,
}: {
  title: string;
  items: SectorMove[];
  tone: "up" | "down";
}) {
  const color = tone === "up" ? "text-up" : "text-down";
  return (
    <div className="bg-white rounded-2xl shadow-card px-4 py-3 flex-1">
      <p className={`text-sm font-bold mb-2 ${color}`}>{title}</p>
      <ul className="space-y-1.5">
        {items.map((s) => (
          <li
            key={s.sector}
            className="flex items-center justify-between text-sm"
          >
            <span>{s.sector}</span>
            <span className={`font-semibold ${color}`}>
              {formatPercent(s.changePercent)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function SectorRotationCard({ strong, weak }: Props) {
  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">섹터 순환</h2>
      <div className="flex gap-3">
        <SectorList title="강세 ▲" items={strong} tone="up" />
        <SectorList title="약세 ▼" items={weak} tone="down" />
      </div>
    </section>
  );
}
