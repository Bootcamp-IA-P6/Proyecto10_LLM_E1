import { createFileRoute } from "@tanstack/react-router";
import NewsSection from "@/components/news/NewsSection";
import ContentResult from "@/components/shared/ContentResult";
import PageHeader from "@/components/shared/PageHeader";
import ProfileBadge from "@/components/shared/ProfileBadge";
import ErrorBanner from "@/components/shared/ErrorBanner";
import { useGeneration } from "@/hooks/useGeneration";
import type { NewsRequest } from "@/types/content";

export const Route = createFileRoute("/news")({
  head: () => ({
    meta: [
      { title: "Contenido financiero · Digital Content AI" },
      {
        name: "description",
        content: "Genera contenido a partir de titulares financieros actuales.",
      },
    ],
  }),
  component: NewsPage,
});

function NewsPage() {
  const { result, isLoading, error, submit, regenerate } = useGeneration({ kind: "news" });

  return (
    <div className="flex flex-col items-center px-4 py-12 gap-8">
      <PageHeader
        eyebrow="Modo noticias · Finanzas"
        title="Contenido financiero"
        description="A partir de titulares de mercado actualizados."
      />
      <ProfileBadge />
      <div className="relative w-full max-w-xl bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl shadow-black/30">
        <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent" />
        <NewsSection onSubmit={(r: NewsRequest) => submit(r)} isLoading={isLoading} />
      </div>
      {error && <ErrorBanner message={error} />}
      <div className="w-full max-w-xl">
        <ContentResult result={result} isLoading={isLoading} onRegenerate={regenerate} />
      </div>
    </div>
  );
}
