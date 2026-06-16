import type { ReactNode } from "react";

interface PageHeaderProps {
  eyebrow?: string;
  title: ReactNode;
  description?: string;
}

export default function PageHeader({ eyebrow, title, description }: PageHeaderProps) {
  return (
    <div className="flex flex-col items-center gap-3 text-center">
      {eyebrow && (
        <div className="flex items-center gap-2 bg-emerald-500/20 border border-emerald-400/30 rounded-full px-4 py-1">
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
          <span className="text-emerald-300 text-xs font-medium tracking-wide uppercase">
            {eyebrow}
          </span>
        </div>
      )}
      <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white">{title}</h1>
      {description && (
        <p className="text-sm text-emerald-100/60 max-w-xl leading-relaxed">{description}</p>
      )}
    </div>
  );
}
