import { useState } from "react";
import ReactMarkdown from "react-markdown";
import type { AnyResult, GenerateResponse } from "@/types/content";

interface Props {
  result: AnyResult | null;
  isLoading: boolean;
  onRegenerate?: () => void;
}

const PLATFORM_LABELS: Record<string, string> = {
  blog: "Blog",
  twitter: "Twitter / X",
  linkedin: "LinkedIn",
  instagram: "Instagram",
};

type Tab = "raw" | "preview";

function QualityBadge({ score, feedback }: { score: number; feedback?: string }) {
  const config =
    score >= 0.8
      ? { label: "✅ Alta calidad", classes: "bg-emerald-500/20 text-emerald-300 border-emerald-400/30" }
      : score >= 0.6
        ? { label: "⚠️ Calidad aceptable", classes: "bg-yellow-500/20 text-yellow-300 border-yellow-400/30" }
        : { label: "❌ Revisar contenido", classes: "bg-red-500/20 text-red-300 border-red-400/30" };
  return (
    <div className="flex flex-col gap-1">
      <span className={`text-xs font-medium border px-2 py-1 rounded-full w-fit ${config.classes}`}>
        {config.label} · {(score * 10).toFixed(1)}/10
      </span>
      {feedback && <p className="text-xs text-white/40 pl-1">{feedback}</p>}
    </div>
  );
}

export default function ContentResult({ result, isLoading, onRegenerate }: Props) {
  const [activeTab, setActiveTab] = useState<Tab>("raw");
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!result) return;
    navigator.clipboard.writeText(result.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const imageUrl = (result as GenerateResponse)?.image_url;
  const platform = (result as GenerateResponse)?.platform;
  const qualityScore = (result as GenerateResponse)?.quality_score;
  const qualityFeedback = (result as GenerateResponse)?.quality_feedback;

  if (isLoading) {
    return (
      <div className="w-full flex flex-col gap-3">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div
            key={i}
            className="h-4 rounded bg-gradient-to-r from-white/5 via-white/10 to-white/5 bg-[length:200%_100%] animate-[shimmer_1.5s_infinite]"
            style={{ width: ["33%", "100%", "100%", "83%", "100%", "66%"][i - 1] }}
          />
        ))}
      </div>
    );
  }

  if (!result) {
    return (
      <div className="w-full flex items-center justify-center h-40 border-2 border-dashed border-white/10 rounded-xl">
        <p className="text-sm text-white/30">El contenido generado aparecerá aquí</p>
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-3 animate-[fadeIn_0.4s_ease-in-out]">
      {imageUrl && (
        <img
          src={imageUrl}
          alt={`Imagen para ${PLATFORM_LABELS[platform] ?? platform}`}
          className="w-full h-48 object-cover rounded-xl border border-white/10"
        />
      )}

      <div className="flex items-center justify-between">
        {platform ? (
          <span className="text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-2 py-1 rounded-full">
            {PLATFORM_LABELS[platform] ?? platform}
          </span>
        ) : (
          <span className="text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-2 py-1 rounded-full">
            {result.model_used}
          </span>
        )}
        <span className="text-xs text-white/30">Modelo: {result.model_used}</span>
      </div>

      {qualityScore !== undefined && <QualityBadge score={qualityScore} feedback={qualityFeedback} />}

      <div className="flex gap-1 bg-white/5 border border-white/10 rounded-lg p-1 w-fit">
        {(["raw", "preview"] as Tab[]).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
              activeTab === tab
                ? "bg-emerald-500 text-white shadow-sm"
                : "text-white/40 hover:text-white/70"
            }`}
          >
            {tab === "raw" ? "Raw" : "Preview"}
          </button>
        ))}
      </div>

      {activeTab === "raw" ? (
        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-sm text-emerald-50 whitespace-pre-wrap leading-relaxed">
          {result.content}
        </div>
      ) : (
        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-sm text-emerald-50 leading-relaxed prose prose-invert max-w-none prose-headings:text-emerald-300 prose-strong:text-emerald-300 prose-a:text-teal-400">
          <ReactMarkdown>{result.content}</ReactMarkdown>
        </div>
      )}

      <div className="flex items-center justify-between">
        <span className="text-xs text-white/30">
          {result.content.length} caracteres
          {platform === "twitter" && (
            <span className={result.content.length > 1400 ? "text-yellow-400 ml-1" : "ml-1"}>
              · ~{Math.ceil(result.content.length / 280)} tweets estimados
            </span>
          )}
        </span>
        <div className="flex gap-3">
          {onRegenerate && (
            <button
              onClick={onRegenerate}
              className="text-xs text-white/40 hover:text-emerald-400 transition-colors"
            >
              🔄 Regenerar
            </button>
          )}
          <button
            onClick={handleCopy}
            className="text-xs text-white/40 hover:text-emerald-400 transition-colors"
          >
            {copied ? "✅ Copiado" : "Copiar al portapapeles"}
          </button>
        </div>
      </div>
    </div>
  );
}
