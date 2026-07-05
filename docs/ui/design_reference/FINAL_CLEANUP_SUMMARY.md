# Final Roadmap Metadata Cleanup — Summary (2026-07-05)

Scope: metadata-only pass over `docs/roadmap/` + `docs/ui/design_reference/`.
No feature IDs changed, no tiers renamed, no UI implemented, no images
generated, no font binaries added, no proprietary assets embedded.

## 1. Dependency metadata fixes (Task 1)
Rule enforced: `Depends on:` carries hard blockers only (earlier in STATUS.md
order); forward references moved to `Later integrates:` / `Enhanced by:` /
`Future UI integration:`. 25 feature headers now carry such soft-forward
clauses. Decisions on the flagged cases:
- **Softened (not hard):** F057→F049 (governor throttles parallelism later);
  F111→F106/F033 (v1 ships its own hunk lib; hard dep is F005 schema diffs);
  F108→F113 (cheap generation is an optimization); F065→F067 (library
  packaging); F067→F124; F068→F035 (decision-queue data suffices);
  F112/F114/F116→F074 (class-default bands, honestly labeled, until
  calibration); F084→F039/Tier 5 (CLI/report demo standalone); F119→F009/
  Tier-5 shell (CLI curation until the shell; UI is a parallel human track);
  F126→Tier-5 graph; F121→F138 (manual ADRs suffice); F122→F149 (manual
  fill); F163→F164 (F139 trailers suffice; F164 completes the standard);
  F189→F190 (F007 single-service runtime; compose enhances); F199→F202;
  F219→F249 (relationship inverted: F249 reuses F219's suite); F223→F226
  (--best-of stays manual until risk triggering); F036→F041; also hardened
  during checks: F011→F009, F017→F014, F018→F014 (config/CLI carry budgets
  until the Flight Plan), F051→F031 (backend queue already exists).
- **Solved by minimal reorder (truly hard):** F037 now precedes F033 in
  Tier 5 (hunk checkboxes live inside the diff viewer; A4 would otherwise be
  unsatisfiable) and F169 now precedes F168 in Tier 9 (the dossier's
  human-oversight chapter is core content, not garnish). STATUS.md and the
  ROADMAP Part F/tier prose were updated together.
Result: **zero forward references remain in `Depends on:`** (machine-checked)
— F080's parser can consume dependency metadata without false self-blocking.

## 2. Tier 0 order (Task 2)
Verified intact: F146 → F081 → F147 → F148. No further Tier-0 changes.

## 3. F147 wording (Task 3)
Now exactly: `Depends on: F146 · Later integrates: F014 completes full Flight
Plan rendering / plan-view behavior`. F147 is not blocked by F014.

## 4. Token migration map (Task 4)
The predicted global-replace bug was real: the map's LEFT sides had been
migrated too (`--remedy-card→--remedy-card`). Repaired in ROADMAP Part E —
left = legacy `--rm-*`, right = canonical `--remedy-*`, plus the explicit
rule "No active feature or spec may instruct builders to use `--rm-*`."

## 5. Font/icon/asset contradictions (Task 5)
Fresh scan: Manrope Variable and JetBrains Mono Variable are the only active
font rules; lucide-react + custom Remedy glyphs the only active icon/glyph
rules. Remaining mentions of Avenir Next, SF Mono, Material icons /
`@mui/icons-material` and `--rm-*` exist ONLY as audit history, OS-fallback
entries, or migration/deprecation notes — each verified line-by-line this
pass. No temporary/local paths; the design image path is uniformly
`docs/ui/design_reference/ux_design.png`.

## 6. Authority & graph consistency (Tasks 6–7)
Authority chain consistent everywhere (README, ROADMAP Part I, assets_spec
§10): ux_design.png → assets_spec + tokens.css → graph/ux/component/motion
specs → feature prose; deviations require an assumption_log entry with a
technical reason. Graph features defer to graph_spec/motion_spec/assets_spec/
tokens/acceptance; the earlier F020 hexagon conflict remains fixed; no
competing ontology, glyph, state-color or motion language found.

## 7. Summary files (Task 8)
Fragile exact counts replaced with robust wording; stale claims refreshed;
this file supersedes older per-pass check listings.

## 8. Machine-check results (Task 10, fresh)
250 feature files · missing F-numbers: none · duplicates: none · STATUS.md:
250 entries, zero tier mismatches with file names · forward hard deps in
"Depends on:": **none** · 25 headers carry soft-forward clauses · `--rm-*`
only in the Part E migration map + historical/audit notes · Avenir/SF Mono/
Material only historical/fallback/migration · temp paths: none · legacy hex
palettes: none · ux_design.png present, all references repo-pathed · binary
fonts: none · generated images: none · UI code files under docs/: none.

## 9. Unresolved assumptions
None blocking. Standing interpretive assumptions remain documented in
`README.md` §K (JobHeader slot, initials avatar, `--rm-warn` dual mapping).

## 10. Potential future follow-up (non-blocking note, not a feature)
Consider a vendor-neutral "Worker Instruction Packs / Prompt Constitution"
design later: abstracting authority hierarchy, task-class-specific
instruction packs, tool/capability routing, file-grounded claims, and
design-reference loading as reusable, worker-agnostic prompt infrastructure.
Do not copy or depend on any leaked or vendor-specific prompt text. This note
changes nothing in the roadmap.

## Verdict
**Commit-ready.** The package satisfies the full quality bar of this pass.
