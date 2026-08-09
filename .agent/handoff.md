# Handoff — F105 Cache-optimal prompt ordering, R2 (T001 segment registry)

Feature F105, round **R2**, branch `feature/f105-cache-optimal-prompt-ordering`.
Review range **6b74d7c4..HEAD** (6b74d7c4 = the R1 handback). This is a SPLIT
round: it writes production code, so it is not self-certified. Nothing merged,
no PR created or edited, no force-push, no branch switch. Change set held
exactly to the six files the block named.

## Commits

### c136e8b6 chore(f105): save the R2 T001 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r2-1.md | +110 | the R2 block, verbatim (new) |
| .agent/last_block.md | +101/-244 | same bytes; replaces the R1 block |

211 insertions. Both files sha256
`48dde40ffb7464ac841e31382ec7e141f49ca78889a74ac358e97d6e76c44ab0`.

### 0a0d9454 feat(f105): add the prompt segment registry, compose and manifest
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/prompt_segments.py | +201 | the mechanism (new) |
| tests/orchestration/test_prompt_segments.py | +284 | 22 pinning tests (new) |

485 insertions — under the 500 cap, no exemption used. Nothing else under
`packages/orchestration` was opened for edit; no builder, no prompt content.

### (this commit) chore(f105): hand back R2
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14/-13 | Current Step → R2 done; Next Steps → R3 T002; 44 lines |
| .agent/handoff.md | rewrite | this file (template self-reference exception) |

## Exported public names (grep targets)
From `packages/orchestration/prompt_segments.py`:
`SegmentStabilityRank` (IntEnum: SYSTEM=0, CONVENTIONS=1, DOSSIER=2,
JOB_CONTEXT=3, TASK=4, STEERING=5) · `PromptSegment` · `PromptSegmentManifestEntry`
· `ComposedPrompt` (`.text`, `.manifest`, `.manifest_as_dicts()`) ·
`PromptSegmentRegistry` (`.register(name, rank, text, *, token_cap=None)`,
`.registered_segments()`) · `PromptSegmentError` · `PROMPT_SEGMENT_DELIMITER`
(`"\n\n"`) · `CONVENTIONS_TOKEN_CAP` (`800`) · `compose_prompt_segments(segments)`.
One private helper: `_manifest_entry_for_segment`. Every public name grepped to
its own definition only before the commit — no prior use of any of them existed.

## Verification
Run by me from the repo root after 0a0d9454, real exit codes, real tails:

| Gate | Command | Exit | Result |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r2-1.md .agent/last_block.md` | **0** | no output — byte-identical |
| B | `pytest tests/orchestration/test_prompt_segments.py -q` | **0** | 22 passed in 0.07s |
| C | `pytest tests/orchestration/test_token_economy.py -q` | **0** | 37 passed in 0.19s |
| D | `pytest tests/cli/test_golden_path.py -q` (canary) | **0** | 42 passed in 19.33s |
| E | `pytest tests/docs/ -q` | **0** | 294 passed in 0.25s |
| F | `remedy integrity check --json` via `apps.cli.grouped:main` | **0** | `"passed": true` (line 3), `"fail_count": 0`, 5 checks |
| G | `git status --porcelain` | **0** | EMPTY (before this commit; re-checked after) |
| H | `ruff check` on both new files | **0** | All checks passed |

**Red-proof (not ordered by the block, run anyway).** Ten mutations of
`prompt_segments.py` — rank order dropped, tie-break reversed, delimiter given a
marker, sha256 over the name, `chars` over the name, cap never enforced,
duplicates accepted, rank scale renumbered, manifest in registration order,
empty composition made an error — each run against the suite and each reverted.
**10 killed, 0 survivors.** It ran only inside a disposable worktree at
`.remedy-wt/f105-r2-redproof` (G5), which was removed; `git worktree list` shows
the primary checkout alone and the tree stayed clean throughout.

## Deviations & assumptions — declared
- **D1.** `.agent/plan.md` was updated in the handback commit, not before C1/C2:
  the block orders C1 to carry its two files alone and C2 to carry module plus
  tests together. Same shape as the accepted F105 R1 D3 and F104 04889d8d. The
  plan already named R2 as its next step, so no commit ran against a stale plan.
- **D2.** `registered_segments()` is not named in the block. The block requires
  the registry to preserve registration order but names no way to read it out,
  and `compose_prompt_segments()` takes a sequence; the accessor is the seam
  between them. Flagged so the reviewer can reject it rather than discover it.
- **D3.** Rank validation lives in `register()`, not in a `PromptSegment`
  `__post_init__`: the block says name must be non-empty and unique "within a
  registry", which only the registry can know, so both checks sit together.
- **D4.** `remedy` is not invocable on PATH here; gate F ran through the
  `python3 -c "… from apps.cli.grouped import main …"` form the block spells out.
- **Deviations, declared: this handoff is 106 lines** (AGENTS.md D15 stated
  cause): three per-commit changed-files tables, the exported-names block the
  block explicitly ordered, the eight-row gate table plus the red-proof result,
  the item-status table and four declared deviations. No section dropped.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 save the block (both files, cmp) | done | c136e8b6; cmp exit 0, two files only |
| C2 module + tests together | done | 0a0d9454; 485 insertions, 22 tests green |
| C3 plan + handoff + push | done | this commit; push result in the completion report |

## Open findings
**1** — R-0221 (Low, carried from F103 R5 through F104 and F105 R1; F252
flake-debt class, not this feature's code). No new findings raised by this
round. Next free finding ID **R-0229**. Closure candidates: **0 open**.

## Next
Reviewer confirms `6b74d7c4..HEAD`, re-runs gates A-G itself, and gates R2. On
PASS, `LAST_REVIEWED_SHA` advances to this commit and the next authored step is
**R3 — T002**: the role loaders for `docs/agents/worker_conventions.md` and
`docs/agents/reviewer_conventions.md` (both present on disk, 2023 and 2068 bytes
— comfortably under `CONVENTIONS_TOKEN_CAP`) plus their content-equality
goldens. R3 is also a SPLIT round.
