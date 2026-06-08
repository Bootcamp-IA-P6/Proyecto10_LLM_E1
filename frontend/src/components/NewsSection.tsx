"use client"

import { useState, useEffect } from "react"
import { NewsRequest, NewsHeadline, Language, Platform } from "@/types/content"
import { getFinancialNews } from "@/services/api"

interface NewsSectionProps {
  onSubmit:  (req: NewsRequest) => void
  isLoading: boolean
}

export default function NewsSection({ onSubmit, isLoading }: NewsSectionProps) {
  const [topic, setTopic]             = useState("bolsa mercados finanzas")
  const [audience, setAudience]       = useState("")
  const [tone, setTone]               = useState("profesional")
  const [language, setLanguage]       = useState<Language>("es")
  const [platform, setPlatform]       = useState<Platform>("linkedin")
  const [headlines, setHeadlines]     = useState<NewsHeadline[]>([])
  const [loadingNews, setLoadingNews] = useState(false)

  useEffect(() => {
    fetchHeadlines()
  }, [])

  async function fetchHeadlines() {
    setLoadingNews(true)
    const news = await getFinancialNews(topic)
    setHeadlines(news)
    setLoadingNews(false)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!audience.trim()) return
    onSubmit({ topic, audience, tone, language, platform })
  }

  return (
    <div className="flex flex-col gap-4 w-full">

      {/* Titulares actuales */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-emerald-200">
            📰 Titulares actuales
          </p>
          <button
            onClick={fetchHeadlines}
            disabled={loadingNews}
            className="text-xs text-white/40 hover:text-emerald-400 transition-colors disabled:opacity-30"
          >
            {loadingNews ? "Actualizando..." : "↻ Actualizar"}
          </button>
        </div>

        {loadingNews ? (
          <div className="flex flex-col gap-2 animate-pulse">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-12 bg-white/5 rounded-lg" />
            ))}
          </div>
        ) : headlines.length > 0 ? (
          <div className="flex flex-col gap-2 max-h-48 overflow-y-auto pr-1">
            {headlines.map((headline, index) => (
              <div
                key={index}
                className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 flex flex-col gap-0.5"
              >
                <p className="text-xs font-medium text-emerald-100 leading-relaxed">
                  {headline.title}
                </p>
                {headline.description && (
                  <p className="text-xs text-white/30 line-clamp-1">
                    {headline.description}
                  </p>
                )}
                <a
                  href={headline.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-emerald-400 hover:text-emerald-300 transition-colors mt-1"
                >
                  Ver noticia →
                </a>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white/5 border border-white/10 rounded-lg px-3 py-4 text-center">
            <p className="text-xs text-white/30">
              No se encontraron titulares. Comprueba la NEWS_API_KEY.
            </p>
          </div>
        )}
      </div>

      <div className="h-px bg-white/10" />

      {/* Formulario de generación */}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">

        {/* Topic */}
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-emerald-200">
            Topic financiero
          </label>
          <input
            type="text"
            value={topic}
            onChange={e => setTopic(e.target.value)}
            placeholder="ej: bolsa española, criptomonedas, mercados"
            className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
          />
        </div>

        {/* Plataforma */}
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-emerald-200">Plataforma</label>
          <select
            value={platform}
            onChange={e => setPlatform(e.target.value as Platform)}
            className="bg-emerald-950 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 w-full"
          >
            <option className="bg-emerald-950 text-white" value="blog">Blog</option>
            <option className="bg-emerald-950 text-white" value="twitter">Twitter / X</option>
            <option className="bg-emerald-950 text-white" value="linkedin">LinkedIn</option>
            <option className="bg-emerald-950 text-white" value="instagram">Instagram</option>
          </select>
        </div>

        {/* Audiencia */}
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-emerald-200">Audiencia</label>
          <input
            type="text"
            value={audience}
            onChange={e => setAudience(e.target.value)}
            placeholder="ej: inversores, público general"
            className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
          />
        </div>

        {/* Tono */}
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-emerald-200">Tono</label>
          <input
            type="text"
            value={tone}
            onChange={e => setTone(e.target.value)}
            placeholder="ej: profesional, analítico, informativo"
            className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
          />
        </div>

        {/* Idioma */}
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-emerald-200">Idioma</label>
          <select
            value={language}
            onChange={e => setLanguage(e.target.value as Language)}
            className="bg-emerald-950 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 w-full"
          >
            <option className="bg-emerald-950 text-white" value="es">Español</option>
            <option className="bg-emerald-950 text-white" value="en">English</option>
            <option className="bg-emerald-950 text-white" value="fr">Français</option>
            <option className="bg-emerald-950 text-white" value="it">Italiano</option>
          </select>
        </div>

        {/* Botón */}
        <button
          type="submit"
          disabled={isLoading || !audience.trim()}
          className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white rounded-lg px-4 py-2.5 text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-lg shadow-emerald-900/50"
        >
          {isLoading ? "Generando..." : "Generar contenido financiero"}
        </button>

      </form>
    </div>
  )
}