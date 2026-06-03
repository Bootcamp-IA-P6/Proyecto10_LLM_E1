"use client";

import { useState, useEffect } from "react";
import { CompanyProfile } from "@/types/content";
import { saveProfile, getProfile } from "@/services/api";

export default function ProfileForm() {
  const [name, setName] = useState("");
  const [sector, setSector] = useState("");
  const [tone, setTone] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Al montar el componente recuperar el perfil guardado
  useEffect(() => {
    async function loadProfile() {
      const profile = await getProfile();
      if (profile) {
        setName(profile.name);
        setSector(profile.sector);
        setTone(profile.tone);
        setDescription(profile.description ?? "");
      }
    }
    loadProfile();
  }, []);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !sector.trim() || !tone.trim()) return;

    setIsLoading(true);
    setSuccess(false);
    setError(null);

    try {
      const profile: CompanyProfile = {
        name,
        sector,
        tone,
        description: description.trim() || undefined,
      };
      await saveProfile(profile);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Error al guardar el perfil",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSave} className="flex flex-col gap-4 w-full">
      {/* Nombre empresa */}
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">
          Nombre de la empresa
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="ej: TechCorp Madrid"
          className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
        />
      </div>

      {/* Sector */}
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">Sector</label>
        <input
          type="text"
          value={sector}
          onChange={(e) => setSector(e.target.value)}
          placeholder="ej: tecnología, salud, educación"
          className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
        />
      </div>

      {/* Tono */}
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">
          Tono de comunicación
        </label>
        <input
          type="text"
          value={tone}
          onChange={(e) => setTone(e.target.value)}
          placeholder="ej: innovador, cercano, profesional"
          className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30"
        />
      </div>

      {/* Descripción */}
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-emerald-200">
          Descripción
          <span className="text-white/30 font-normal ml-1">(opcional)</span>
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="ej: empresa de desarrollo de software con foco en IA"
          rows={3}
          className="bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 placeholder-white/30 resize-none"
        />
      </div>

      {/* Feedback */}
      {success && (
        <p className="text-sm text-emerald-400">
          ✅ Perfil guardado correctamente
        </p>
      )}
      {error && <p className="text-sm text-red-400">{error}</p>}

      {/* Botón */}
      <button
        type="submit"
        disabled={isLoading || !name.trim() || !sector.trim() || !tone.trim()}
        className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white rounded-lg px-4 py-2.5 text-sm font-semibold disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-lg shadow-emerald-900/50"
      >
        {isLoading ? "Guardando..." : "Guardar perfil"}
      </button>
    </form>
  );
}
