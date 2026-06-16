import { createFileRoute, Link } from "@tanstack/react-router";
import { SITE } from "@/constants/site";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: `${SITE.name} — ${SITE.tagline}` },
      { name: "description", content: SITE.description },
      { property: "og:title", content: SITE.name },
      { property: "og:description", content: SITE.description },
    ],
  }),
  component: LandingPage,
});

const FEATURES = [
  {
    icon: "✍️",
    title: "Generación general",
    description: "Blog, Twitter, LinkedIn e Instagram con tono y audiencia personalizables.",
    to: "/generate" as const,
  },
  {
    icon: "🔬",
    title: "Científico con RAG",
    description: "Contenido basado en papers reales de arXiv usando Ollama + RAG.",
    to: "/science" as const,
  },
  {
    icon: "📰",
    title: "Noticias financieras",
    description: "Genera contenido a partir de titulares de mercados actualizados.",
    to: "/news" as const,
  },
];

const STEPS = [
  { n: "01", title: "Configura tu perfil", text: "Define empresa, sector y tono de marca." },
  { n: "02", title: "Elige el modo", text: "General, científico o noticias." },
  { n: "03", title: "Genera y publica", text: "Copia, regenera o consulta el historial." },
];

function LandingPage() {
  return (
    <div className="flex flex-col items-center px-4 py-16 gap-24">
      {/* Hero */}
      <section className="flex flex-col items-center gap-6 text-center max-w-3xl">
        <div className="flex items-center gap-2 bg-emerald-500/20 border border-emerald-400/30 rounded-full px-4 py-1">
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
          <span className="text-emerald-300 text-xs font-medium tracking-wide uppercase">
            IA Generativa · Groq + Ollama
          </span>
        </div>
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight">
          <span className="text-white">Digital</span>{" "}
          <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">
            Content AI
          </span>
        </h1>
        <p className="text-lg text-emerald-100/70 max-w-xl leading-relaxed">{SITE.tagline}</p>
        <div className="flex flex-wrap gap-3 justify-center">
          <Link
            to="/generate"
            className="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white rounded-lg px-5 py-2.5 text-sm font-semibold shadow-lg shadow-emerald-900/50 transition-all"
          >
            Empezar a generar
          </Link>
          <Link
            to="/profile"
            className="border border-white/20 hover:bg-white/5 text-white rounded-lg px-5 py-2.5 text-sm font-semibold transition-all"
          >
            Configurar perfil
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="w-full max-w-5xl grid md:grid-cols-3 gap-4">
        {FEATURES.map((f) => (
          <Link
            key={f.title}
            to={f.to}
            className="group relative bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all"
          >
            <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent" />
            <div className="text-3xl mb-3">{f.icon}</div>
            <h3 className="text-lg font-semibold text-white mb-2">{f.title}</h3>
            <p className="text-sm text-white/60 leading-relaxed">{f.description}</p>
            <span className="mt-4 inline-block text-xs text-emerald-300 group-hover:text-emerald-200">
              Abrir →
            </span>
          </Link>
        ))}
      </section>

      {/* How it works */}
      <section className="w-full max-w-5xl flex flex-col gap-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white">Cómo funciona</h2>
          <p className="text-sm text-white/50 mt-2">Tres pasos para publicar más rápido.</p>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          {STEPS.map((s) => (
            <div
              key={s.n}
              className="bg-white/5 border border-white/10 rounded-2xl p-6 flex flex-col gap-2"
            >
              <span className="text-emerald-300 text-xs font-mono">{s.n}</span>
              <h4 className="text-white font-semibold">{s.title}</h4>
              <p className="text-sm text-white/50">{s.text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="w-full max-w-3xl text-center bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border border-emerald-400/20 rounded-3xl p-10">
        <h2 className="text-3xl font-bold text-white">¿Listo para crear contenido?</h2>
        <p className="text-sm text-white/60 mt-2 mb-6">
          Elige un modo y empieza en segundos. Sin configuración compleja.
        </p>
        <Link
          to="/generate"
          className="inline-block bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white rounded-lg px-6 py-3 text-sm font-semibold shadow-lg shadow-emerald-900/50"
        >
          Generar mi primer contenido
        </Link>
      </section>
    </div>
  );
}
