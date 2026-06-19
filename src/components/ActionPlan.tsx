type Props = {
  items: string[];
};

export default function ActionPlan({ items }: Props) {
  return (
    <section>
      <h2 className="text-sm font-bold text-sub mb-2 px-1">오늘 액션 플랜</h2>
      <div className="bg-cardHi text-ink rounded-2xl shadow-card px-5 py-4 border border-up/40">
        <ul className="space-y-2">
          {items.map((it, i) => (
            <li key={i} className="flex gap-3 text-sm leading-relaxed">
              <span className="flex-none w-5 h-5 rounded-full bg-up/20 text-up flex items-center justify-center text-[11px] font-bold">
                {i + 1}
              </span>
              <span>{it}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
