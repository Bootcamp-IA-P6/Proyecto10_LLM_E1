import { SITE } from "@/constants/site";

export default function Footer() {
  return (
    <footer className="border-t border-white/10 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-white/40">
        <span>
          © {new Date().getFullYear()} {SITE.name}
        </span>
        <span>Groq · Ollama · arXiv · NewsAPI</span>
      </div>
    </footer>
  );
}
