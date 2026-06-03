import axios from "axios"
import { GenerateRequest, GenerateResponse, CompanyProfile } from "@/types/content"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
})

export async function generateContent(
    req: GenerateRequest
    ): Promise<GenerateResponse> {
    try {
        const response = await apiClient.post<GenerateResponse>(
        "/api/generate",
        req
        )
        return response.data
    } catch (error) {
        if (axios.isAxiosError(error)) {
        throw new Error(
            error.response?.data?.detail || "Error al conectar con el servidor"
        )
        }
        throw new Error("Error inesperado")
    }
}

export async function saveProfile(profile: CompanyProfile): Promise<void> {
    try {
        await apiClient.post("/api/profile", profile)
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw new Error(
                error.response?.data?.detail || "Error al guardar el perfil"
            )
        }
        throw new Error("Error inesperado al guardar el perfil"
            )
    }
}

export async function getProfile(): Promise<CompanyProfile | null> {
    try {
        const response = await apiClient.get<CompanyProfile | null>("/api/profile")
        return response.data
    } catch (error) {
        return null
    }
}