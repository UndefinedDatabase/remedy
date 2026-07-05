# Remedy Design Reference — Canonical Package (v1.0 · 2026-07-04)

**The screenshot is law.** `docs/ui/design_reference/ux_design.png` (2174×1206 px,
measured from the checked-in file; it equals the 1678×926 design frame of
`docs/ui/RICHTIG_PIXEL_LOCK_SPEC.md` at ≈1.295× scale) is the authoritative visual target for the Remedy cockpit.
This package translates it into implementation-ready specifications, grounded in
the actual codebase (audited 2026-07-04, review bundle `remedy-review-20260704-191403`).

## A. Executive summary

The cockpit shows the **Growing Brain**: a luminous, organic neural graph at
center — the job core as a glowing `</>` sphere, tasks and runs as small glossy
nodes on soft dendritic branches — surrounded by calm glass surfaces: a brand
rail left, metrics + command bar top, a live panel right (now-card, chat/activity,
task checklist), and a phase timeline bottom. Feeling: **calm, premium,
futuristic, intelligent, glassy, soft, alive, trustworthy, technically serious.**

Codebase verdict in one paragraph: the repo is **much closer to the screenshot
than a rebuild suggests**. React 19 + Vite + CSS Modules with a `--remedy-*`
token file already tuned to this reference; the shell layout (rail / stage /
right panel / timeline) exists and matches the pixel-lock region table; state
colors match the legend. The gaps are concentrated in the **center stage**: the
active graph renderer (`BrainGraphCanvas`, SVG) is a placeholder layout, while a
better canvas renderer (`ForceBrainGraph`, react-force-graph-2d) exists but is
not mounted; the organic glow/particle/branch language of the screenshot is not
yet achieved by either. Secondary gaps: command bar styling, chat input in the
right panel, filter chip styling, timeline sub-glyph legend, and token coverage
(spacing/z/motion tokens missing). The plan therefore **preserves the shell and
tokens, replaces the center**, and hardens fidelity last.

## Authority chain (binding for every visual decision)
`ux_design.png` → `assets_spec.md` + `tokens.css` → `graph_spec.md` /
`ux_spec.md` / `component_spec.md` / `motion_spec.md` → feature-file prose.
Feature prose can never override the design reference on visual matters;
deviations require an assumption_log entry with a technical reason — silent
redesign is a review finding.

## Package contents

| File | Deliverable |
|---|---|
| `codebase_audit.md` | B — codebase design audit |
| `ux_spec.md` | C — canonical design spec (incl. layout grid, states, responsive) |
| `tokens.css` + `tokens_rules.md` | D — design tokens + usage rules |
| `component_spec.md` | E — component breakdown |
| `graph_spec.md` | F — Growing Brain graph specification |
| `graph_tech_recommendation.md` | G — renderer analysis & recommendation |
| `motion_spec.md` | motion system (referenced by C/E/F) |
| `implementation_plan.md` | H — staged plan for coding agents |
| `feature_reference_block.md` | I — roadmap/feature-file integration |
| `acceptance_criteria.md` | J — pixel-faithful acceptance criteria |
| `assets_spec.md` | Asset authority: fonts, icons, graph glyphs, logo |

## K. Assumptions and open questions

1. **Mock-frame text.** "CONCEPT 01 OF 10 / GROWING BRAIN OVERVIEW / An AI agent
   shipping a CLI tool…" in the left rail is concept-sheet framing. Mapped to a
   real **JobHeader** slot: kicker = project name, title = job title, body =
   job description. The visual treatment (sizes, colors, spacing) is law; the
   literal words are not. (Assumption — flagged, low risk.)
2. **Avatar in chat.** The user message shows a photographic avatar. Real app
   uses an initial-letter disc in the same size/position (no stock photos).
   (Assumption; keeps privacy + asset discipline.)
3. **Token namespace.** Code uses `--remedy-*` (40+ consumers); the roadmap
   CONVENTIONS registry documents `--rm-*`. This package canonizes
   **`--remedy-*`** and ships a patch note for CONVENTIONS (see
   `feature_reference_block.md`). Decision made here to avoid a 40-file rename
   with zero user value; needs a one-line ADR when applied.
4. **Numbers in the reference.** Metrics (34/18/56/68%), task names and chat
   lines are sample data; bindings are specified in `component_spec.md`.
5. **Exact blur radii, particle counts, glow alphas** are estimated from the
   screenshot and labeled `(estimated)` throughout; the acceptance process
   (J §2) settles them by side-by-side review, not by guesswork wars.
6. **Open question for the operator:** should the right-panel chat input send
   steering messages before the steering feature exists? Spec ships it
   **rendered but disabled with an honest tooltip** (matches roadmap F021/F030
   sequencing). Flip to live is one prop.
