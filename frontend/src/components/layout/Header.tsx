import { Link } from "@tanstack/react-router";
import { NAV_ITEMS } from "@/constants/navigation";
import { SITE } from "@/constants/site";

export default function Header() {
  return (
    <header className="sticky top-0 z-30 backdrop-blur-xl bg-emerald-950/50 border-b border-white/10">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-white font-semibold tracking-tight">
          <span className="inline-block w-6 h-6 rounded bg-gradient-to-br from-emerald-400 to-teal-300" />
          <span>{SITE.name}</span>
        </Link>
        <nav className="hidden md:flex items-center gap-1">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className="px-3 py-1.5 text-sm text-white/60 hover:text-white rounded-md transition-colors"
              activeProps={{ className: "px-3 py-1.5 text-sm text-emerald-300 bg-white/5 rounded-md" }}
            >
              <span className="mr-1">{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </nav>
        <Link
          to="/generate"
          className="md:hidden text-xs text-emerald-300 border border-emerald-400/30 bg-emerald-500/10 rounded-md px-3 py-1.5"
        >
          Generar
        </Link>
      </div>
      <nav className="md:hidden flex items-center gap-1 overflow-x-auto px-4 pb-2 border-t border-white/5">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.to}
            to={item.to}
            className="shrink-0 px-3 py-1 text-xs text-white/60 hover:text-white rounded-md transition-colors"
            activeProps={{ className: "shrink-0 px-3 py-1 text-xs text-emerald-300 bg-white/5 rounded-md" }}
          >
            <span className="mr-1">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
