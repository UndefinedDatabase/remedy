export function CodeOrbIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 72 72" role="img" aria-label="Code node">
      <defs>
        <radialGradient id="codeOrbGradient" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#fff" />
          <stop offset="55%" stopColor="#6da0ff" />
          <stop offset="100%" stopColor="#2459d6" />
        </radialGradient>
      </defs>
      <circle cx="36" cy="36" r="31" fill="url(#codeOrbGradient)" />
      <circle cx="36" cy="36" r="31" fill="none" stroke="rgba(255,255,255,.8)" strokeWidth="2" />
      <path d="M29 27 L20 36 L29 45 M43 27 L52 36 L43 45 M39 24 L33 48" fill="none" stroke="white" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
