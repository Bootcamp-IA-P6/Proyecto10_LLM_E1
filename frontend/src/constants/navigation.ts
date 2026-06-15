export interface NavItem {
  to: string;
  label: string;
  icon: string;
}

export const NAV_ITEMS: NavItem[] = [
  { to: "/generate", label: "General", icon: "✍️" },
  { to: "/science", label: "Científico", icon: "🔬" },
  { to: "/news", label: "Noticias", icon: "📰" },
  { to: "/history", label: "Historial", icon: "🕓" },
  { to: "/profile", label: "Perfil", icon: "🏢" },
];
