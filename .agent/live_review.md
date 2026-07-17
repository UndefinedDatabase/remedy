# Live Review — Steps 10161-10360 — F012 hardening round 13

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (10 external findings), awaiting re-review (NOT accepted)

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened; no manifest field added.

External review of `remedy-review-20260716-232544-BLOCKED_EVIDENCE.zip` returned TEN findings.
All fixed as one block; each of the seven code findings was REPRODUCED against the production
seam first (the table is in `.agent/plan.md`).

- **F1** — a published reference's ledger must be `complete`; an incomplete one is refused, and a
  pre-publication candidate says so and reports incomplete Call coverage instead.
- **F2** — `terminal_state` is strictly decoded from the RUN's own `final_status` through a CLOSED
  map (unknown → recorded problem + incomplete ledger, never a `"stopped"` default). The stored
  task rule is narrow on purpose: production reaches `blocked`/`failed` with a SUCCESSFUL run.
- **F3** — the Manifest/Ledger bijection compares the exact named field set, `ok` included.
- **F4** — the recorded ORDER must be the manifest's order, and this episode's entries must be the
  ledger's suffix. F140 serves stream N for call N by that order.
- **F5** — cross-episode continuity: a later ledger is an exact extension; no prior entry may be
  invented, altered, reordered or dropped; every prior entry resolves to the episode that actually
  published it. Enforced in `_validate_episode_graph` — the one place the whole chain is in hand.
- **F6** — entry identities go through the established rules (`safe_call_ref` for the path-shaped
  call ref, component rule for the episode id) plus the same secret/path scanners; enums closed,
  numbers bounded.
- **F7** — containment is decided LEXICALLY before anything is opened; `open_verified_dir` refuses
  `..` on its own. No outside repo read, no outside helper run, no fd leak.
- **F8** — one closed ledger contract across typed validation, decoder, artifact read, full-chain,
  writer preflight/postcondition, recovery and export.
- **F9** — one operator-state policy: `.agent/*.md` excluded from the attested union using the
  SAME predicate every authoritative view already used; the diff is scoped by construction so
  `safe.diff` and `changed_files` are one account. Still shipped in the ZIP as context.
- **F10** — the BLOCKED package is a diagnostic artifact; the final ZIP is built only once the
  fresh Evidence is authoritative.

## Verification (authoritative pytest summaries — each recorded as its own Evidence command)

- New round-13 suites (ledger_semantics, ledger_chain_continuity, ledger_identity_safety,
  workspace_traversal, round13_evidence_alignment) → **133 passed**.
- Every F012 suite → **1021 passed**.
- F010/F011/Evidence integration → **499 passed**.
- CLI regressions (`tests/cli`, excluding the two suites listed under PRE-EXISTING) → **848
  passed**.
- Docs consistency → **84 passed**.
- compileall (`packages apps scripts tests`) exit 0; `bash -n scripts/make_review_zip.sh` clean;
  `git diff --check` clean.

## Pre-existing failures OUTSIDE this block (not introduced, not fixed)

`tests/cli/test_do_cmd_summary.py` and `tests/cli/test_product_spine.py` fail 18 tests **at base
`b0ba27a` itself**, proven on a pristine detached worktree of the base: they require
`docs/core-product-spine-v0.md` and sibling flat docs that an earlier restructure moved to
`system/`+`guides/`+`archive/`. Round 13 touches none of those paths. The recorded CLI command
excludes exactly those two files and the debt is reported here rather than hidden by a green
number.

## Known gap (unchanged from round 12, recorded honestly)

F9-round-12's preferred filesystem-tree identity for genuinely non-Git workspaces is still not
implemented: such a workspace records an explicit `unavailable` identity and therefore INCOMPLETE
input coverage, which is the finding's own stated fallback. It never yields `same_inputs=true`.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch uncommitted,
unpushed, unmerged.
