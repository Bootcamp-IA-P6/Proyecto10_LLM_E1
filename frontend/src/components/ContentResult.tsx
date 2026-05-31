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
            <div className="w-full flex flex-col gap-3 animate-pulse">
                <div className="h-4 bg-white/10 rounded w-1/3" />
                <div className="h-4 bg-white/10 rounded w-full" />
                <div className="h-4 bg-white/10 rounded w-full" />
                <div className="h-4 bg-white/10 rounded w-5/6" />
                <div className="h-4 bg-white/10 rounded w-full" />
                <div className="h-4 bg-white/10 rounded w-4/6" />
            </div>
        )
    }

    // Estado: sin resultado
    if (!result) {
        return (
            <div className="w-full flex items-center justify-center h-40 border-2 border-dashed border-white/10 rounded-xl">
                <p className="text-sm text-white/30">
                    El contenido generado aparecerá aquí
                </p>
            </div>
        )
    }

    // Estado: con resultado
    return (
        <div className="w-full flex flex-col gap-3">

            {/* Cabecera con metadatos */}
            <div className="flex items-center justify-between">
                <span className="text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-2 py-1 rounded-full">
                    {PLATFORM_LABELS[result.platform] ?? result.platform}
                </span>
                <span className="text-xs text-white/30">
                    Modelo: {result.model_used}
                </span>
            </div>

            {/* Contenido generado */}
            <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-sm text-emerald-50 whitespace-pre-wrap leading-relaxed">
                {result.content}
            </div>

            {/* Botón copiar */}
            <button
                onClick={() => navigator.clipboard.writeText(result.content)}
                className="self-end text-xs text-white/40 hover:text-emerald-400 transition-colors"
            >
                Copiar al portapapeles
            </button>

        </div>
    )
}