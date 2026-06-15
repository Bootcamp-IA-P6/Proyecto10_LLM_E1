import { createFileRoute } from "@tanstack/react-router";
import HistoryPanel from "@/components/history/HistoryPanel";
import PageHeader from "@/components/shared/PageHeader";

export const Route = createFileRoute("/history")({
  head: () => ({
    meta: [
      { title: "Historial · Digital Content AI" },
      { name: "description", content: "Historial de generaciones." },
    ],
  }),
  component: HistoryPage,
});

function HistoryPage() {
  return (
    <div className="flex flex-col items-center px-4 py-12 gap-8">
      <PageHeader
        eyebrow="Historial"
        title="Generaciones guardadas"
        description="Filtra, copia y borra contenido generado anteriormente."
      />
      <div className="w-full max-w-2xl bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 shadow-xl">
        <HistoryPanel />
      </div>
    </div>
  );
}
