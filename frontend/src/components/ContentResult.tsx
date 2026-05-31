"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
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

type Tab = "raw" | "preview"

export default function ContentResult({ result, isLoading }: ContentResultProps) {
    const [activeTab, setActiveTab] = useState<Tab>("raw")

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

            {/* Pestañas */}
            <div className="flex gap-1 bg-white/5 border border-white/10 rounded-lg p-1 w-fit">
                <button
                    onClick={() => setActiveTab("raw")}
                    className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
                        activeTab === "raw"
                            ? "bg-emerald-500 text-white shadow-sm"
                            : "text-white/40 hover:text-white/70"
                    }`}
                >
                    Raw
                </button>
                <button
                    onClick={() => setActiveTab("preview")}
                    className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
                        activeTab === "preview"
                            ? "bg-emerald-500 text-white shadow-sm"
                            : "text-white/40 hover:text-white/70"
                    }`}
                >
                    Preview
                </button>
            </div>

            {/* Contenido — Raw */}
            {activeTab === "raw" && (
                <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-sm text-emerald-50 whitespace-pre-wrap leading-relaxed">
                    {result.content}
                </div>
            )}

            {/* Contenido — Preview Markdown */}
            {activeTab === "preview" && (
                <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-sm text-emerald-50 leading-relaxed prose prose-invert prose-emerald max-w-none
                    prose-headings:text-emerald-300
                    prose-headings:font-bold
                    prose-h1:text-xl
                    prose-h2:text-lg
                    prose-h3:text-base
                    prose-p:text-emerald-50
                    prose-p:leading-relaxed
                    prose-strong:text-emerald-300
                    prose-em:text-emerald-200
                    prose-li:text-emerald-50
                    prose-a:text-teal-400
                    prose-a:no-underline
                    prose-a:hover:text-teal-300
                    prose-code:text-emerald-300
                    prose-code:bg-white/10
                    prose-code:px-1
                    prose-code:rounded
                    prose-blockquote:border-emerald-500
                    prose-blockquote:text-emerald-200
                    prose-hr:border-white/10
                ">
                    <ReactMarkdown>
                        {result.content}
                    </ReactMarkdown>
                </div>
            )}

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