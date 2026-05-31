"use client"

import { useState } from "react"
import GenerateForm from "@/components/GenerateForm"
import ContentResult from "@/components/ContentResult"
import { generateContent } from "@/services/api"
import { GenerateRequest, GenerateResponse } from "@/types/content"

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult]       = useState<GenerateResponse | null>(null)
  const [error, setError]         = useState<string | null>(null)

  async function handleGenerate(req: GenerateRequest) {
    setIsLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await generateContent(req)
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-emerald-950 via-teal-900 to-green-900 flex flex-col items-center px-4 py-12 gap-10">

      {/* Orbes decorativos de fondo */}
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
            IA Generativa · Groq LLM
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

      {/* Tarjeta principal */}
      <div className="relative w-full max-w-xl bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl shadow-black/30">
        {/* Borde superior decorativo */}
        <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent" />

        <GenerateForm
          onSubmit={handleGenerate}
          isLoading={isLoading}
        />
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
          result={result}
          isLoading={isLoading}
        />
      </div>

    </main>
  )
}