import React from "react";
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

// Metrics glyphs
export function ClipboardGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <rect x="3" y="4" width="10" height="10" rx="1.5" />
      <path d="M6 4V3a2 2 0 014 0v1" />
      <line x1="6" y1="7.5" x2="10" y2="7.5" />
      <line x1="6" y1="10" x2="9" y2="10" />
    </svg>
  );
}

export function CalendarGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <rect x="2" y="3" width="12" height="11" rx="1.5" />
      <line x1="2" y1="6.5" x2="14" y2="6.5" />
      <line x1="5" y1="2" x2="5" y2="4" />
      <line x1="11" y1="2" x2="11" y2="4" />
    </svg>
  );
}

export function ChartGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <polyline points="2 12 6 7 9 9 14 4" />
    </svg>
  );
}

export function TokenGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" {...p}>
      <circle cx="8" cy="8" r="5.5" />
      <path d="M6 6.5a2 2 0 014 0c0 1.2-2 1.8-2 3" />
      <circle cx="8" cy="11.5" r=".5" fill="currentColor" />
    </svg>
  );
}

export function FlaskGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <path d="M6.5 2v4L3.5 12a1 1 0 00.9 1.5h7.2a1 1 0 00.9-1.5L9.5 6V2" />
      <line x1="5.5" y1="2" x2="10.5" y2="2" />
      <line x1="5" y1="9.5" x2="11" y2="9.5" opacity=".6" />
    </svg>
  );
}

export function ShieldCheckGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <path d="M8 2l5 2v4c0 3-2.2 5-5 6-2.8-1-5-3-5-6V4z" />
      <polyline points="6 8 7.5 9.5 10.5 6" />
    </svg>
  );
}

/** The budget/cost mark `assets_spec.md` line 179 already specifies — a coin,
 *  circle plus an inner cent-bar — so the COST metric conforms to the asset
 *  authority rather than minting a new glyph. */
export function CoinGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" {...p}>
      <circle cx="8" cy="8" r="5.5" />
      <line x1="8" y1="3.8" x2="8" y2="12.2" />
      <path d="M9.8 5.9a2.8 2.8 0 100 4.2" />
    </svg>
  );
}

// Activity glyphs
export function BuilderGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <polyline points="5 5 3 8 5 11" />
      <polyline points="11 5 13 8 11 11" />
      <line x1="9" y1="4" x2="7" y2="12" opacity=".6" />
    </svg>
  );
}

export function ReviewerGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <circle cx="8" cy="8" r="4" />
      <path d="M11 11l2.5 2.5" />
    </svg>
  );
}

export function PersonGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <circle cx="8" cy="5" r="2.5" />
      <path d="M3 14c0-3 2.5-5 5-5s5 2 5 5" />
    </svg>
  );
}

export function GearGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <circle cx="8" cy="8" r="2" />
      <path d="M7 2h2l.3 1.5a4.5 4.5 0 011.5.9L12.3 4l1 1.7-1.2.9a4.5 4.5 0 010 1.8l1.2.9-1 1.7-1.5-.5a4.5 4.5 0 01-1.5.9L9 14H7l-.3-1.5a4.5 4.5 0 01-1.5-.9L3.7 12l-1-1.7 1.2-.9a4.5 4.5 0 010-1.8L2.7 6.7l1-1.7 1.5.5a4.5 4.5 0 011.5-.9z" />
    </svg>
  );
}

export function ArrowSendGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <line x1="3" y1="8" x2="13" y2="8" />
      <polyline points="9 4 13 8 9 12" />
    </svg>
  );
}

export function CopyGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <rect x="5" y="5" width="8" height="8" rx="1" />
      <path d="M3 11V4a1 1 0 011-1h7" />
    </svg>
  );
}

export function PhaseGlyph({ phase, ...p }: G & { phase: string }) {
  const phaseContent: Record<string, React.ReactNode> = {
    job: <path d="M3 5h10v7H3z M5 5V3h6v2" />,
    planning: <path d="M4 3v10h8V3 M6 6h4 M6 9h3" />,
    build: <><polyline points="5 4 2 8 5 12" /><polyline points="11 4 14 8 11 12" /><line x1="9" y1="3" x2="7" y2="13" /></>,
    test: <><path d="M4 4h8v2H4z" /><path d="M5 6v6h6V6" /><polyline points="6 9 7.5 10.5 10 8" /></>,
    review: <><circle cx="8" cy="5.5" r="2.5" /><path d="M3 14c0-2.8 2.2-4.5 5-4.5s5 1.7 5 4.5" /></>,
    finalized: <><path d="M4 3v10l4-2.5L12 13V3" /></>,
  };
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.45" strokeLinecap="round" strokeLinejoin="round" {...p}>
      {phaseContent[phase] || phaseContent.job}
    </svg>
  );
}
