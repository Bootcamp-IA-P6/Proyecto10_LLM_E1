"use client"

import { useState, useEffect, useRef } from "react"
import GenerateForm from "@/components/GenerateForm"
import ContentResult from "@/components/ContentResult"
import ProfileForm from "@/components/ProfileForm"
import ScienceForm from "@/components/ScienceForm"
import NewsSection from "@/components/NewsSection"
import HistoryPanel from "@/components/HistoryPanel"
import {
  generateContent,
  generateScience,
  generateNews,
  getProfile,
} from "@/services/api"
import {
  GenerateRequest,
  GenerateResponse,
  ScienceRequest,
  ScienceResponse,
  NewsRequest,
  NewsResponse,
  CompanyProfile,
} from "@/types/content"

type Tab    = "general" | "science" | "news"
type Result = GenerateResponse | ScienceResponse | NewsResponse | null

export default function Home() {
  const [activeTab, setActiveTab]         = useState<Tab>("general")
  const [isLoading, setIsLoading]         = useState(false)
  const [result, setResult]               = useState<Result>(null)
  const [error, setError]                 = useState<string | null>(null)
  const [showProfile, setShowProfile]     = useState(false)
  const [showHistory, setShowHistory]     = useState(false)
  const [activeProfile, setActiveProfile] = useState<CompanyProfile | null>(null)
  const [historyKey, setHistoryKey]       = useState(0)

  // Guardamos la última request para el botón regenerar
  const lastGeneralReq  = useRef<GenerateRequest | null>(null)
  const lastScienceReq  = useRef<ScienceRequest | null>(null)
  const lastNewsReq     = useRef<NewsRequest | null>(null)

  useEffect(() => {
    async function loadProfile() {
      const profile = await getProfile()
      if (profile) setActiveProfile(profile)
    }
    loadProfile()
  }, [])

  function handleTabChange(tab: Tab) {
    setActiveTab(tab)
    setResult(null)
    setError(null)
  }

  async function handleGenerate(req: GenerateRequest) {
    lastGeneralReq.current = req
    setIsLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await generateContent(req)
      setResult(data)
      setHistoryKey(prev => prev + 1)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado")
    } finally {
      setIsLoading(false)
    }
  }

  async function handleGenerateScience(req: ScienceRequest) {
    lastScienceReq.current = req
    setIsLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await generateScience(req)
      setResult(data)
      setHistoryKey(prev => prev + 1)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado")
    } finally {
      setIsLoading(false)
    }
  }

  async function handleGenerateNews(req: NewsRequest) {
    lastNewsReq.current = req
    setIsLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await generateNews(req)
      setResult(data)
      setHistoryKey(prev => prev + 1)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado")
    } finally {
      setIsLoading(false)
    }
  }

  async function handleRegenerate() {
    if (activeTab === "general" && lastGeneralReq.current) {
      await handleGenerate(lastGeneralReq.current)
    } else if (activeTab === "science" && lastScienceReq.current) {
      await handleGenerateScience(lastScienceReq.current)
    } else if (activeTab === "news" && lastNewsReq.current) {
      await handleGenerateNews(lastNewsReq.current)
    }
  }

  async function handleProfileSaved() {
    const profile = await getProfile()
    if (profile) {
      setActiveProfile(profile)
      setShowProfile(false)
    }
  }

  const TAB_LABELS: Record<Tab, string> = {
    general: "✍️ General",
    science: "🔬 Científico",
    news:    "📰 Noticias",
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-emerald-950 via-teal-900 to-green-900 flex flex-col items-center px-4 py-12 gap-10">

      {/* Orbes decorativos */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-emerald-500 rounded-full opacity-10 blur-3xl" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-teal-400 rounded-full opacity-10 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-green-400 rounded-full opacity-5 blur-3xl" />
      </div>

      {/* Cabecera */}
      <div className="relative flex flex-col items-center gap-3 text-center">
        <div className="flex items-center gap-2 bg-emerald-500/20 border border-emerald-400/30 rounded-full px-4 py-1">
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
          <span className="text-emerald-300 text-xs font-medium tracking-wide uppercase">
            IA Generativa · Groq + Ollama
          </span>
        </div>

        <h1 className="text-5xl font-extrabold tracking-tight">
          <span className="text-white">Digital</span>
          {" "}
          <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">
            Content AI
          </span>
        </h1>

        <p className="text-sm text-emerald-100/60 max-w-md leading-relaxed">
          Genera contenido listo para publicar en cualquier plataforma
          usando inteligencia artificial
        </p>
      </div>

      {/* Perfil de empresa */}
      <div className="relative w-full max-w-xl flex flex-col gap-3">
        <button
          onClick={() => setShowProfile(prev => !prev)}
          className="flex items-center justify-between w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-emerald-200 hover:bg-white/10 transition-all"
        >
          <div className="flex items-center gap-2">
            <span>🏢</span>
            <span className="font-medium">
              {activeProfile
                ? `Perfil activo: ${activeProfile.name}`
                : "Configurar perfil de empresa"
              }
            </span>
          </div>
          <span className="text-white/40 text-xs">
            {showProfile ? "▲ Cerrar" : "▼ Abrir"}
          </span>
        </button>

        {activeProfile && !showProfile && (
          <div className="flex gap-2 flex-wrap px-1">
            <span className="text-xs bg-emerald-500/10 border border-emerald-400/20 text-emerald-300 px-2 py-1 rounded-full">
              {activeProfile.sector}
            </span>
            <span className="text-xs bg-emerald-500/10 border border-emerald-400/20 text-emerald-300 px-2 py-1 rounded-full">
              Tono: {activeProfile.tone}
            </span>
          </div>
        )}

        {showProfile && (
          <div className="relative bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 shadow-xl">
            <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent" />
            <ProfileForm onSaved={handleProfileSaved} />
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="w-full max-w-xl flex gap-1 bg-white/5 border border-white/10 rounded-xl p-1">
        {(Object.keys(TAB_LABELS) as Tab[]).map(tab => (
          <button
            key={tab}
            onClick={() => handleTabChange(tab)}
            className={`flex-1 px-3 py-2 text-sm font-medium rounded-lg transition-all ${
              activeTab === tab
                ? "bg-emerald-500 text-white shadow-sm"
                : "text-white/40 hover:text-white/70"
            }`}
          >
            {TAB_LABELS[tab]}
          </button>
        ))}
      </div>

      {/* Tarjeta principal */}
      <div className="relative w-full max-w-xl bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl shadow-black/30">
        <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent" />

        {activeTab === "general" && (
          <GenerateForm onSubmit={handleGenerate} isLoading={isLoading} />
        )}
        {activeTab === "science" && (
          <ScienceForm onSubmit={handleGenerateScience} isLoading={isLoading} />
        )}
        {activeTab === "news" && (
          <NewsSection onSubmit={handleGenerateNews} isLoading={isLoading} />
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="w-full max-w-xl bg-red-500/10 border border-red-400/30 rounded-xl px-4 py-3 backdrop-blur-sm">
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      {/* Resultado */}
      <div className="w-full max-w-xl">
        <ContentResult
          result={result as GenerateResponse | null}
          isLoading={isLoading}
          onRegenerate={result ? handleRegenerate : undefined}
        />
      </div>

      {/* Historial */}
      <div className="relative w-full max-w-xl flex flex-col gap-3">
        <button
          onClick={() => setShowHistory(prev => !prev)}
          className="flex items-center justify-between w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-emerald-200 hover:bg-white/10 transition-all"
        >
          <div className="flex items-center gap-2">
            <span>🕓</span>
            <span className="font-medium">Historial de generaciones</span>
          </div>
          <span className="text-white/40 text-xs">
            {showHistory ? "▲ Cerrar" : "▼ Abrir"}
          </span>
        </button>

        {showHistory && (
          <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 shadow-xl">
            <HistoryPanel key={historyKey} />
          </div>
        )}
      </div>

    </main>
  )
}