"use client"

import { useState, useEffect } from "react"
import { GenerationRecord } from "@/types/content"
import { getHistory, deleteGeneration } from "@/services/api"

const GEN_TYPE_LABELS: Record<string, string> = {
  general: "✍️ General",
  science: "🔬 Científico",
  news:    "📰 Noticias",
}

const PLATFORM_LABELS: Record<string, string> = {
  blog:      "Blog",
  twitter:   "Twitter / X",
  linkedin:  "LinkedIn",
  instagram: "Instagram",
}

export default function HistoryPanel() {
  const [history, setHistory]     = useState<GenerationRecord[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [expanded, setExpanded]   = useState<number | null>(null)
  const [backendReady, setBackendReady] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [])

  async function loadHistory() {
    setIsLoading(true)
    const data = await getHistory()
    if (data.length === 0) {
      // Puede ser backend no listo o simplemente vacío
      // Lo distinguimos intentando la llamada
    }
    setHistory(data)
    setIsLoading(false)
  }

  async function handleDelete(id: number) {
    const success = await deleteGeneration(id)
    if (success) {
      setHistory(prev => prev.filter(g => g.id !== id))
      if (expanded === id) setExpanded(null)
    }
  }

  function formatDate(isoString: string) {
    const date = new Date(isoString)
    return date.toLocaleDateString("es-ES", {
      day:    "2-digit",
      month:  "short",
      hour:   "2-digit",
      minute: "2-digit",
    })
  }

  // Estado: cargando
  if (isLoading) {
    return (
      <div className="flex flex-col gap-3 animate-pulse">
        {[1, 2, 3].map(i => (
          <div key={i} className="h-16 bg-white/5 rounded-xl" />
        ))}
      </div>
    )
  }

  // Estado: sin historial
  if (history.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-40 border-2 border-dashed border-white/10 rounded-xl gap-2">
        <p className="text-sm text-white/30">
          Aún no hay generaciones guardadas
        </p>
        <p className="text-xs text-white/20">
          Genera contenido y aparecerá aquí
        </p>
      </div>
    )
  }

  // Estado: con historial
  return (
    <div className="flex flex-col gap-3">

      {/* Cabecera */}
      <div className="flex items-center justify-between">
        <p className="text-xs text-white/40">
          {history.length} generación{history.length !== 1 ? "es" : ""} guardada{history.length !== 1 ? "s" : ""}
        </p>
        <button
          onClick={loadHistory}
          className="text-xs text-white/40 hover:text-emerald-400 transition-colors"
        >
          ↻ Actualizar
        </button>
      </div>

      {/* Lista */}
      <div className="flex flex-col gap-2">
        {history.map(record => (
          <div
            key={record.id}
            className="bg-white/5 border border-white/10 rounded-xl overflow-hidden"
          >
            {/* Fila resumen */}
            <div
              className="flex items-center justify-between px-4 py-3 cursor-pointer hover:bg-white/5 transition-colors"
              onClick={() => setExpanded(expanded === record.id ? null : record.id)}
            >
              <div className="flex flex-col gap-0.5 flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-emerald-300 font-medium">
                    {GEN_TYPE_LABELS[record.gen_type] ?? record.gen_type}
                  </span>
                  <span className="text-xs text-white/20">·</span>
                  <span className="text-xs text-white/40">
                    {PLATFORM_LABELS[record.platform] ?? record.platform}
                  </span>
                </div>
                <p className="text-sm text-white/70 truncate">
                  {record.topic}
                </p>
              </div>

              <div className="flex items-center gap-3 ml-3 shrink-0">
                <span className="text-xs text-white/20">
                  {formatDate(record.created_at)}
                </span>
                <button
                  onClick={e => {
                    e.stopPropagation()
                    handleDelete(record.id)
                  }}
                  className="text-white/20 hover:text-red-400 transition-colors text-xs"
                >
                  ✕
                </button>
                <span className="text-white/20 text-xs">
                  {expanded === record.id ? "▲" : "▼"}
                </span>
              </div>
            </div>

            {/* Contenido expandido */}
            {expanded === record.id && (
              <div className="border-t border-white/10 px-4 py-3 flex flex-col gap-3">

                {/* Imagen si existe */}
                {record.image_url && (
                  <img
                    src={record.image_url}
                    alt={record.topic}
                    className="w-full h-32 object-cover rounded-lg"
                  />
                )}

                {/* Metadatos */}
                <div className="flex flex-wrap gap-2">
                  <span className="text-xs bg-white/5 border border-white/10 text-white/40 px-2 py-1 rounded-full">
                    {record.model_used}
                  </span>
                  {record.language && (
                    <span className="text-xs bg-white/5 border border-white/10 text-white/40 px-2 py-1 rounded-full">
                      {record.language.toUpperCase()}
                    </span>
                  )}
                  {record.audience && (
                    <span className="text-xs bg-white/5 border border-white/10 text-white/40 px-2 py-1 rounded-full">
                      {record.audience}
                    </span>
                  )}
                </div>

                {/* Contenido */}
                <div className="bg-black/20 rounded-lg p-3 text-xs text-emerald-50 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">
                  {record.content}
                </div>

                {/* Botón copiar */}
                <button
                  onClick={() => navigator.clipboard.writeText(record.content)}
                  className="self-end text-xs text-white/40 hover:text-emerald-400 transition-colors"
                >
                  Copiar al portapapeles
                </button>

              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}