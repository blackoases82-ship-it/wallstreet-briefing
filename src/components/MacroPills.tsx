import type { MacroIndicator } from "@/types/briefing";

type Props = {
  indicators: MacroIndicator[];
};

function directionColor(dir?: string) {
  if (dir === "up") return "text-up";
  if (dir === "down") return "text-down";
  return "text-ink";
}

export default function MacroPills({ indicators }: Props) {
  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">거시 지표</h2>
      <div className="flex flex-wrap gap-2">
        {indicators.map((m) => (
          <div
            key={m.name}
            className="bg-card rounded-full shadow-card px-4 py-2 flex items-baseline gap-1.5 border border-line"
            title={m.note ?? undefined}
          >
            <span className="text-xs text-sub">{m.name}</span>
            <span className={`text-sm font-bold ${directionColor(m.direction)}`}>
              {m.value || "-"}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
