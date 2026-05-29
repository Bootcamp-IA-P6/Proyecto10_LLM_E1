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
    <main className="min-h-screen bg-white flex flex-col items-center px-4 py-12 gap-10">

      {/* Cabecera */}
      <div className="flex flex-col items-center gap-2 text-center">
        <h1 className="text-3xl font-bold text-gray-900">
          Digital Content AI
        </h1>
        <p className="text-sm text-gray-500 max-w-md">
          Genera contenido listo para publicar en cualquier plataforma
          usando inteligencia artificial
        </p>
      </div>

      {/* Formulario */}
      <GenerateForm
        onSubmit={handleGenerate}
        isLoading={isLoading}
      />

      {/* Error */}
      {error && (
        <div className="w-full max-w-xl bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Resultado */}
      <ContentResult
        result={result}
        isLoading={isLoading}
      />

    </main>
  )
}