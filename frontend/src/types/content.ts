export type Platform = "blog" | "twitter" | "linkedin" | "instagram"
export type Model = "groq" | "ollama"
export type Language = "es" | "en" | "fr" | "it"

export interface GenerateRequest {
    platform: Platform
    topic: string
    audience: string
    tone?: string
    language?: Language
    model?: Model
    company_profile?: string
}

export interface GenerateResponse {
    content: string
    platform: Platform
    model_used: string
    image_url?: string
}

export interface CompanyProfile {
    name: string
    sector: string
    tone: string
    description?: string
}