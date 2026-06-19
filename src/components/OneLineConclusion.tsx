type Props = {
  text: string;
};

export default function OneLineConclusion({ text }: Props) {
  return (
    <section className="bg-card rounded-2xl shadow-card px-5 py-4 border-l-4 border-up">
      <p className="text-xs font-semibold text-sub mb-1">오늘 한 줄</p>
      <p className="text-base leading-relaxed font-medium">{text}</p>
    </section>
  );
}
