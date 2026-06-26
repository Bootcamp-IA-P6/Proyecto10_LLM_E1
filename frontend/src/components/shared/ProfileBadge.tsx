import { Link } from "@tanstack/react-router";
import { useActiveProfile } from "@/hooks/useActiveProfile";

export default function ProfileBadge() {
  const { data: profile } = useActiveProfile();
  return (
    <Link
      to="/profile"
      className="flex items-center justify-between w-full max-w-xl bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-emerald-200 hover:bg-white/10 transition-all"
    >
      <div className="flex items-center gap-2">
        <span>🏢</span>
        <span className="font-medium">
          {profile ? `Perfil activo: ${profile.name}` : "Configurar perfil de empresa"}
        </span>
      </div>
      {profile && (
        <div className="hidden sm:flex gap-2">
          <span className="text-xs bg-emerald-500/10 border border-emerald-400/20 text-emerald-300 px-2 py-0.5 rounded-full">
            {profile.sector}
          </span>
        </div>
      )}
    </Link>
  );
}
