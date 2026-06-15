export default function BackgroundOrbs() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-emerald-500 rounded-full opacity-10 blur-3xl" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-teal-400 rounded-full opacity-10 blur-3xl" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-green-400 rounded-full opacity-5 blur-3xl" />
    </div>
  );
}
