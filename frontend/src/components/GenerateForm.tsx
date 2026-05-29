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
                <label className="text-sm font-medium text-gray-700">Plataforma</label>
                <select
                value={platform}
                onChange={e => setPlatform(e.target.value as Platform)}
                className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                <option value="blog">Blog</option>
                <option value="twitter">Twitter / X</option>
                <option value="linkedin">LinkedIn</option>
                <option value="instagram">Instagram</option>
                </select>
            </div>

            {/* Tema */}
            <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Tema</label>
                <input
                type="text"
                value={topic}
                onChange={e => setTopic(e.target.value)}
                placeholder="ej: inteligencia artificial en educación"
                className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            {/* Audiencia */}
            <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Audiencia</label>
                <input
                type="text"
                value={audience}
                onChange={e => setAudience(e.target.value)}
                placeholder="ej: profesores de secundaria"
                className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            {/* Tono */}
            <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Tono</label>
                <input
                type="text"
                value={tone}
                onChange={e => setTone(e.target.value)}
                placeholder="ej: profesional, informal, divulgativo"
                className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            {/* Idioma */}
            <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">Idioma</label>
                <select
                value={language}
                onChange={e => setLanguage(e.target.value as Language)}
                className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                <option value="es">Español</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
                <option value="it">Italiano</option>
                </select>
            </div>

            {/* Botón */}
            <button
                type="submit"
                disabled={isLoading || !topic.trim() || !audience.trim()}
                className="bg-blue-600 text-white rounded-md px-4 py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
                {isLoading ? "Generando..." : "Generar contenido"}
            </button>

        </form>
    )
}