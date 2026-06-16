import axios from "axios";
import type {
  GenerateRequest,
  GenerateResponse,
  CompanyProfile,
  ScienceRequest,
  ScienceResponse,
  NewsRequest,
  NewsResponse,
  NewsHeadline,
  GenerationRecord,
} from "@/types/content";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

export async function generateContent(req: GenerateRequest): Promise<GenerateResponse> {
  try {
    const res = await apiClient.post<GenerateResponse>("/api/generate", req);
    return res.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || "Error al conectar con el servidor");
    }
    throw new Error("Error inesperado");
  }
}

export async function saveProfile(profile: CompanyProfile): Promise<void> {
  try {
    await apiClient.post("/api/profile", profile);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || "Error al guardar el perfil");
    }
    throw new Error("Error inesperado al guardar el perfil");
  }
}

export async function getProfile(): Promise<CompanyProfile | null> {
  try {
    const res = await apiClient.get<CompanyProfile | null>("/api/profile");
    return res.data;
  } catch {
    return null;
  }
}

export async function generateScience(req: ScienceRequest): Promise<ScienceResponse> {
  try {
    const res = await apiClient.post<ScienceResponse>("/api/generate/science", req, {
      timeout: 180000,
    });
    return res.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || "Error al generar contenido científico");
    }
    throw new Error("Error inesperado en generación científica");
  }
}

export async function generateNews(req: NewsRequest): Promise<NewsResponse> {
  try {
    const res = await apiClient.post<NewsResponse>("/api/generate/news", req);
    return res.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || "Error al generar contenido financiero");
    }
    throw new Error("Error inesperado en generación financiera");
  }
}

export async function getFinancialNews(topic?: string): Promise<NewsHeadline[]> {
  try {
    const params = topic ? { topic } : {};
    const res = await apiClient.get<{ topic: string; count: number; news: NewsHeadline[] }>(
      "/api/news/financial",
      { params },
    );
    return res.data.news;
  } catch {
    return [];
  }
}

export async function getHistory(limit = 20, skip = 0): Promise<GenerationRecord[]> {
  try {
    const res = await apiClient.get<GenerationRecord[]>("/api/history", {
      params: { limit, skip },
    });
    return res.data;
  } catch {
    return [];
  }
}

export async function deleteGeneration(id: number): Promise<boolean> {
  try {
    await apiClient.delete(`/api/history/${id}`);
    return true;
  } catch {
    return false;
  }
}
