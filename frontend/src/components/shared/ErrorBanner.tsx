export default function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="w-full max-w-xl bg-red-500/10 border border-red-400/30 rounded-xl px-4 py-3 backdrop-blur-sm">
      <p className="text-sm text-red-300">{message}</p>
    </div>
  );
}
