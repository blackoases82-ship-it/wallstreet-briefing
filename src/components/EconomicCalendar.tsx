import type { EconomicCalendar as EconomicCalendarType, CalendarEvent } from "@/types/briefing";

type Props = {
  calendar?: EconomicCalendarType;
};

function catTone(cat: CalendarEvent["category"]): string {
  switch (cat) {
    case "FOMC":
      return "bg-red-500/15 text-red-300 border-red-500/40";
    case "지표":
      return "bg-sky-500/15 text-sky-300 border-sky-500/40";
    case "실적":
      return "bg-emerald-500/15 text-emerald-300 border-emerald-500/40";
    case "정책":
      return "bg-amber-500/15 text-amber-300 border-amber-500/40";
    default:
      return "bg-white/10 text-sub border-line";
  }
}

function regionLabel(r: CalendarEvent["region"]): string {
  return r === "US" ? "🇺🇸" : r === "KR" ? "🇰🇷" : "🌐";
}

export default function EconomicCalendar({ calendar }: Props) {
  if (!calendar || calendar.months.length === 0) return null;

  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">
        🗓️ 세계 증시 주요 일정
      </h2>
      <div className="bg-card rounded-2xl shadow-card border border-line overflow-hidden">
        <div className="scroll-x no-scrollbar">
          <div className="flex gap-3 p-3 min-w-full">
            {calendar.months.map((m) => (
              <div key={m.month} className="min-w-[260px] flex-1">
                <p className="text-sm font-extrabold mb-2 text-ink">{m.month}</p>
                <div className="space-y-3">
                  {m.weeks.map((w) => (
                    <div key={w.week}>
                      <p className="text-[11px] font-semibold text-sub mb-1">
                        {w.week}
                      </p>
                      <ul className="space-y-1.5">
                        {w.events.map((e, i) => (
                          <li
                            key={i}
                            className={`rounded-lg border px-2.5 py-1.5 ${catTone(
                              e.category
                            )} ${
                              e.importance === "high" ? "font-semibold" : ""
                            }`}
                          >
                            <div className="flex items-start justify-between gap-2">
                              <span className="text-xs leading-snug">
                                {regionLabel(e.region)} {e.title}
                              </span>
                              {e.importance === "high" && (
                                <span className="text-[10px] flex-none mt-0.5">
                                  🔴
                                </span>
                              )}
                            </div>
                            <span className="text-[10px] opacity-80">
                              {e.dateLabel} · {e.category}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      {calendar.note && (
        <p className="text-[11px] text-sub mt-1 px-1">{calendar.note}</p>
      )}
    </section>
  );
}
