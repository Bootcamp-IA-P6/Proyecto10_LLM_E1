"use client"

import { useState } from "react"
import { GenerateRequest, Platform, Language } from "@/types/content"

interface GenerateFormProps {
    onSubmit: (req: GenerateRequest) => void
    isLoading: boolean
}

export default function GenerateForm({ onSubmit, isLoading }: GenerateFormProps) {
    const [platform, setPlatform] = useState<Platform>("blog")
    const [topic, setTopic]       = useState("")
    const [audience, setAudience] = useState("")
    const [tone, setTone]         = useState("profesional")
    const [language, setLanguage] = useState<Language>("es")

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault()
        if (!topic.trim() || !audience.trim()) return
        onSubmit({ platform, topic, audience, tone, language })
    }

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-xl">

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

            {/* Tema */}
            <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-emerald-200">Tema</label>
                <input
                    type="text"
                    value={topic}
                    onChange={e => setTopic(e.target.value)}
                    placeholder="ej: inteligencia artificial en educación"
                    className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
                />
            </div>

            {/* Audiencia */}
            <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-emerald-200">Audiencia</label>
                <input
                    type="text"
                    value={audience}
                    onChange={e => setAudience(e.target.value)}
                    placeholder="ej: profesores de secundaria"
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
                    placeholder="ej: profesional, informal, divulgativo"
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
                disabled={isLoading || !topic.trim() || !audience.trim()}
                className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white rounded-lg px-4 py-2.5 text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-lg shadow-emerald-900/50"
            >
                {isLoading ? "Generando..." : "Generar contenido"}
            </button>

        </form>
    )
}