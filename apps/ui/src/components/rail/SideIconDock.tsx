import type { SVGProps } from "react";
import { SparkGlyph, TaskDoneGlyph, ChartGlyph, GearGlyph } from "../icons/RemedyGlyphs";
import styles from "./SideIconDock.module.css";

type G = SVGProps<SVGSVGElement>;

function FolderGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <path d="M2 5V4a1 1 0 011-1h3l2 2h5a1 1 0 011 1v6a1 1 0 01-1 1H3a1 1 0 01-1-1V5z" />
    </svg>
  );
}

function HistoryGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <circle cx="8" cy="8" r="5.5" />
      <polyline points="8 5 8 8 10.5 9.5" />
    </svg>
  );
}

function DocsGlyph(p: G) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <rect x="3" y="2" width="10" height="12" rx="1" />
      <line x1="6" y1="5" x2="10" y2="5" />
      <line x1="6" y1="7.5" x2="10" y2="7.5" />
      <line x1="6" y1="10" x2="8.5" y2="10" />
    </svg>
  );
}

const items: [string, typeof SparkGlyph][] = [
  ["Overview", SparkGlyph],
  ["Checks", TaskDoneGlyph],
  ["Activity", ChartGlyph],
  ["Files", FolderGlyph],
  ["History", HistoryGlyph],
  ["Docs", DocsGlyph],
  ["Settings", GearGlyph],
];

export function SideIconDock({ className }: { className?: string }) {
  return (
    <nav className={`${styles.dock} ${className || ""}`} aria-label="Remedy sections">
      {items.map(([label, Icon], i) => (
        <button key={label} className={i === 0 ? styles.active : styles.button} aria-label={label}>
          <Icon style={{ width: 18, height: 18 }} />
        </button>
      ))}
    </nav>
  );
}
