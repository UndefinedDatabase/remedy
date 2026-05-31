export function NetworkLogoIcon({ className }: { className?: string }) {
  const dots = [[16,10],[32,10],[10,24],[24,24],[38,24],[16,38],[32,38]];
  return (
    <svg className={className} viewBox="0 0 48 48" role="img" aria-label="Remedy network logo">
      <g fill="none" stroke="rgba(76,131,255,0.72)" strokeWidth="2">
        <path d="M16 10 L24 24 L32 10" />
        <path d="M10 24 L24 24 L38 24" />
        <path d="M16 38 L24 24 L32 38" />
      </g>
      {dots.map(([cx,cy], i) => <circle key={i} cx={cx} cy={cy} r="4.2" fill="#4c83ff" opacity={i === 3 ? 1 : .76} />)}
    </svg>
  );
}
