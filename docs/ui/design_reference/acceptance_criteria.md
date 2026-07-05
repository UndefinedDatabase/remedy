# J — Acceptance Criteria for a Pixel-Faithful Implementation

## 1. Screenshot comparison approach
Deterministic fixture job (≈36 tasks, states matching the reference
distribution, seeded layout, frozen clock) rendered at 1678×926, DPR 2.
Compare against `ux_design.png` per REGION (pixel-lock table), not whole-frame:
rail, metrics, command bar, right panel, timeline get strict tolerance; the
graph region is judged by the §2 checklist + structural goldens (its layout is
seeded but organic — whole-frame SSIM alone would both over- and under-fail).

## 2. Human review checklist (graph rest state) — all must be "yes"
calm not busy · core reads as glowing glass sphere with `</>` · edges are
soft curved filaments (no straight spokes) · active branches glow, planned
stay quiet · node states readable without legend · starfield subtle (invisible
on first glance, felt on second) · no cartoon/neon/dark-mode drift · text
crisp at DPR 1 · nothing moves except pulse/breath/particles at rest ·
screenshot side-by-side: a designer cannot name an unintended difference in
10 seconds.

## 3. Token, structure & asset checks (CI)
stylelint: zero color literals outside tokens.css/palette bridge · zero
literal z-index/spacing off-scale (lint) · vitest snapshots per card
component · region geometry test vs. pixel-lock table · truth property:
rendered real ids == view-model ids; decor/stars have no hit area ·
asset gates (assets_spec.md §8): no hardcoded font-family, no foreign icon
imports (lucide-react + local canonical files only), no font binaries or
remote asset URLs in the repo, glyph SVG/canvas parity, goldens await
document.fonts.ready.

## 4. Motion, reduced motion, responsive, a11y
Motion: birth stagger ≤3, durations == motion_spec (exported constants
asserted) · particles only on data-active edges (fixture assert). Reduced
motion: fixture run with the media query — no particles/pulse frames, births
are fades (golden). Responsive: 1280 breakpoint (panel → sheet, dock-only
rail) renders and operates. A11y: axe pass (shell + popover), full keyboard
path chips→list→popover, canvas aria-hidden with list parity present,
aria-live throttled.

## 5. Performance budgets (CI-enforced)
First paint < 1.5s (built bundle, cold) · 60fps p95 at 200 nodes (Stage-1+)
and 500 nodes (Stage-6 gate) on the perf fixture trace · bundle: no new deps
beyond the recommendation; size-limit cap set at current build +10% ·
interaction latency: chip filter and node select < 100ms to first frame.

## 6. Browser targets
Chromium ≥ 120, Firefox ≥ 121, Safari ≥ 17 (backdrop-filter + canvas paths);
no-WebGL is irrelevant for v1 (Canvas2D) — the SVG fallback covers exotic
environments and remains keyboard-complete.

## 7. Do not pass if…
any status color is hardcoded · decor dots are clickable or counted · the
graph shows entities absent from the API · estimated costs/values render
without their honesty marker ("—"/tooltip) · reduced-motion still pulses ·
LIVE shows while polling is stale (>2 intervals) · the right panel shows debug
wording from the forbidden list (ux_spec §17) · the frame is stretched instead
of scaled · a deviation exists with no deviations.md entry · any font/icon/glyph outside assets_spec.md.
