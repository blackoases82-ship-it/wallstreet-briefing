type Props = {
  title: string;
  generatedAt: string;
};

export default function Header({ title, generatedAt }: Props) {
  return (
    <header className="bg-white rounded-2xl shadow-card px-5 py-4">
      <h1 className="text-2xl font-extrabold tracking-tight flex items-center gap-2">
        <span aria-hidden>🗽</span>
        <span>{title}</span>
      </h1>
      <p className="mt-1 text-sm text-sub">기준 {generatedAt}</p>

      <div className="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-xs text-sub">
        <span>
          색: <span className="text-up font-semibold">빨강=상승</span> /{" "}
          <span className="text-down font-semibold">파랑=하락</span>
        </span>
        <span>안전마진=평균 목표가 대비 할인율</span>
        <span>목표가 低·平·高=애널리스트 목표주가 저/평균/고</span>
      </div>
    </header>
  );
}
