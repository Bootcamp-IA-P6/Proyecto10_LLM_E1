"use client"

import { GenerateResponse } from "@/types/content"

interface ContentResultProps {
    result:    GenerateResponse | null
    isLoading: boolean
}

const PLATFORM_LABELS: Record<string, string> = {
    blog:      "Blog",
    twitter:   "Twitter / X",
    linkedin:  "LinkedIn",
    instagram: "Instagram",
}

export default function ContentResult({ result, isLoading }: ContentResultProps) {

  // Estado: cargando
    if (isLoading) {
        return (
        <div className="w-full max-w-xl flex flex-col gap-3 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/3" />
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-5/6" />
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-4/6" />
        </div>
        )
    }

    // Estado: sin resultado
    if (!result) {
        return (
        <div className="w-full max-w-xl flex items-center justify-center h-40 border-2 border-dashed border-gray-200 rounded-lg">
            <p className="text-sm text-gray-400">
            El contenido generado aparecerá aquí
            </p>
        </div>
        )
    }

  // Estado: con resultado
    return (
        <div className="w-full max-w-xl flex flex-col gap-3">

        {/* Cabecera con metadatos */}
        <div className="flex items-center justify-between">
            <span className="text-xs font-medium bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
            {PLATFORM_LABELS[result.platform] ?? result.platform}
            </span>
            <span className="text-xs text-gray-400">
            Modelo: {result.model_used}
            </span>
        </div>

        {/* Contenido generado */}
        <div className="border border-gray-200 rounded-lg p-4 bg-gray-50 text-sm text-gray-800 whitespace-pre-wrap leading-relaxed">
            {result.content}
        </div>

        {/* Botón copiar */}
        <button
            onClick={() => navigator.clipboard.writeText(result.content)}
            className="self-end text-xs text-gray-500 hover:text-blue-600 transition-colors"
        >
            Copiar al portapapeles
        </button>

        </div>
    )
}