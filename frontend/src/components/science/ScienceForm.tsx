import { useState } from "react";
import type { ScienceRequest, Language } from "@/types/content";

interface Props {
  onSubmit: (req: ScienceRequest) => void;
  isLoading: boolean;
}

export default function ScienceForm({ onSubmit, isLoading }: Props) {
  const [topic, setTopic] = useState("");
  const [audience, setAudience] = useState("");
  const [tone, setTone] = useState("divulgativo");
  const [language, setLanguage] = useState<Language>("es");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!topic.trim() || !audience.trim()) return;
    onSubmit({ topic, audience, tone, language, max_papers: 3 });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full">
      <div className="bg-emerald-500/10 border border-emerald-400/20 rounded-xl px-4 py-3 flex flex-col gap-1">
        <p className="text-xs text-emerald-300 font-medium">
          🔬 Contenido basado en papers reales de arXiv
        </p>
        <p className="text-xs text-white/40">
          Usa Ollama + RAG para generar contenido con fuentes científicas reales. Puede tardar 2-3
          minutos. Los topics en inglés dan mejores resultados.
        </p>
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">
          Topic científico
          <span className="text-white/30 font-normal ml-2 text-xs">(mejor en inglés)</span>
        </label>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="ej: artificial intelligence, quantum computing"
          className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">Audiencia</label>
        <input
          type="text"
          value={audience}
          onChange={(e) => setAudience(e.target.value)}
          placeholder="ej: público general, estudiantes de bachillerato"
          className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">Tono</label>
        <input
          type="text"
          value={tone}
          onChange={(e) => setTone(e.target.value)}
          placeholder="ej: divulgativo, educativo, accesible"
          className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">Idioma del contenido generado</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value as Language)}
          className="bg-emerald-950 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 w-full"
        >
          <option value="es">Español</option>
          <option value="en">English</option>
          <option value="fr">Français</option>
          <option value="it">Italiano</option>
        </select>
      </div>

      {isLoading && (
        <div className="bg-amber-500/10 border border-amber-400/20 rounded-xl px-4 py-3">
          <p className="text-xs text-amber-300 font-medium">
            ⏳ Consultando papers en arXiv y generando con Ollama...
          </p>
          <p className="text-xs text-white/40 mt-1">
            Esto puede tardar 2-3 minutos. Por favor no cierres la página.
          </p>
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading || !topic.trim() || !audience.trim()}
        className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white rounded-lg px-4 py-2.5 text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-lg shadow-emerald-900/50"
      >
        {isLoading ? "Generando con RAG..." : "Generar contenido científico"}
      </button>
    </form>
  );
}
