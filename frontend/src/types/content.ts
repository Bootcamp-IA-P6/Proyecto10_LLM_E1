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

export interface ScienceRequest {
    topic: string
    audience: string
    tone?: string
    language?: Language
    max_papers?: number
}

export interface ScienceResponse {
    content: string 
    model_used: string
}

export interface NewsRequest {
    topic: string
    audience: string
    tone?: string
    language?: Language
    platform?: Platform
}

export interface NewsResponse {
    content: string 
    model_used: string
}

export interface NewsHeadline {
    title: string
    description: string
    url: string
}

export interface GenerationRecord {
    id: number
    platform: string
    topic: string
    audience: string
    tone: string | null
    language: string | null
    model_used: string
    content: string
    image_url: string | null
    gen_type: "general" | "science" | "news"
    created_at: string
}