import type { SVGProps } from "react";

type G = SVGProps<SVGSVGElement>;

export function RemedyMark(p: G) {
  return (
    <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" {...p}>
      <circle cx="16" cy="16" r="3" opacity=".9" />
      <circle cx="16" cy="6" r="2" opacity=".6" />
      <circle cx="25" cy="10" r="2" opacity=".5" />
      <circle cx="25" cy="22" r="2" opacity=".4" />
      <circle cx="16" cy="26" r="2" opacity=".6" />
      <circle cx="7" cy="22" r="2" opacity=".5" />
      <circle cx="7" cy="10" r="2" opacity=".4" />
      <line x1="16" y1="13" x2="16" y2="8" opacity=".3" />
      <line x1="18.5" y1="14" x2="23" y2="11" opacity=".3" />
      <line x1="18.5" y1="18" x2="23" y2="21" opacity=".3" />
      <line x1="16" y1="19" x2="16" y2="24" opacity=".3" />
      <line x1="13.5" y1="18" x2="9" y2="21" opacity=".3" />
      <line x1="13.5" y1="14" x2="9" y2="11" opacity=".3" />
    </svg>
  );
}

export function CodeOrbGlyph(p: G) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <polyline points="8 7 4 12 8 17" />
      <polyline points="16 7 20 12 16 17" />
      <line x1="13" y1="5" x2="11" y2="19" opacity=".6" />
    </svg>
  );
}

export function SparkGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" {...p}>
      <path d="M8 2v4M8 10v4M2 8h4M10 8h4M4 4l2.5 2.5M9.5 9.5L12 12M12 4L9.5 6.5M4 12l2.5-2.5" />
    </svg>
  );
}

export function TaskDoneGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <polyline points="4 8.5 7 11.5 12 5" />
    </svg>
  );
}

export function TaskPlannedGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" {...p}>
      <circle cx="8" cy="8" r="4" opacity=".5" />
    </svg>
  );
}

export function TaskCurrentGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" {...p}>
      <circle cx="8" cy="8" r="4" />
      <circle cx="8" cy="8" r="1.5" fill="currentColor" />
    </svg>
  );
}

export function PhaseGlyph({ phase, ...p }: G & { phase: string }) {
  const paths: Record<string, string> = {
    job: "M4 4h8v8H4z",
    planning: "M4 3v10h8V3 M6 6h4 M6 9h3",
    build: "M7 4L4 12h8L9 4",
    test: "M4 8l3 4 5-8",
    review: "M4 4h8v3H4z M6 10h4",
    finalized: "M8 3l2 4h-4z M6 9v3h4V9",
  };
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <path d={paths[phase] || paths.job} />
    </svg>
  );
}
