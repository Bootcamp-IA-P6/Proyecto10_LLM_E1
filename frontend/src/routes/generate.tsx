import { createFileRoute } from "@tanstack/react-router";
import GenerateForm from "@/components/generate/GenerateForm";
import ContentResult from "@/components/shared/ContentResult";
import PageHeader from "@/components/shared/PageHeader";
import ProfileBadge from "@/components/shared/ProfileBadge";
import ErrorBanner from "@/components/shared/ErrorBanner";
import { useGeneration } from "@/hooks/useGeneration";
import type { GenerateRequest } from "@/types/content";

export const Route = createFileRoute("/generate")({
  head: () => ({
    meta: [
      { title: "Generar contenido · Digital Content AI" },
      {
        name: "description",
        content: "Genera contenido para blog, Twitter, LinkedIn e Instagram con IA.",
      },
    ],
  }),
  component: GeneratePage,
});

function GeneratePage() {
  const { result, isLoading, error, submit, regenerate } = useGeneration({ kind: "general" });

  return (
    <div className="flex flex-col items-center px-4 py-12 gap-8">
      <PageHeader
        eyebrow="Modo general"
        title="Generar contenido"
        description="Multi-plataforma, multi-idioma, multi-modelo."
      />
      <ProfileBadge />
      <div className="relative w-full max-w-xl bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl shadow-black/30">
        <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent" />
        <GenerateForm onSubmit={(r: GenerateRequest) => submit(r)} isLoading={isLoading} />
      </div>
      {error && <ErrorBanner message={error} />}
      <div className="w-full max-w-xl">
        <ContentResult result={result} isLoading={isLoading} onRegenerate={regenerate} />
      </div>
    </div>
  );
}
