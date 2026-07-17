# Live Review — Steps 10361-10560 — F012 hardening round 14

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (4 external trust-chain findings + 2 contract items), awaiting
re-review (NOT accepted)

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened; no manifest field added.

External review of `remedy-review-20260717-095618-READY_FOR_REVIEW.zip` (formally clean, verdict
FINDINGS) reported four remaining trust-chain problems. All fixed as one block; each reproduced
against the production seam first (table in `.agent/plan.md`).

- **F1 — a complete terminal ledger is FINAL.** Round 13 froze the entry PREFIX, so a later
  episode could extend a run that had already published `complete=true, terminal_state=completed`
  and restate its outcome. The whole ledger object is now frozen; a later episode repeats it
  byte-for-byte or not at all. Later work uses a new run id — which is what production already
  does (`PingPongResult.run_id` is a fresh `uuid4` per execution), proven on a real stop/resume.
- **F2/F5 — the ledger set is exactly the expectation set.** A `GHOST` ledger belonging to no
  JobInput task, no expectation and no call was accepted everywhere. `validate_ledger_set()` is one
  shared set-level contract: exact set equality, exactly-once JobInput membership, no duplicate
  key, no duplicate ref, refs recomputable from identity.
- **F3 — ledger refs are collision-free.** `{task}-{run}.json` was ambiguous (`("a-b","c")` and
  `("a","b-c")` both → `a-b-c.json`) and the anchored reader silently overwrote one declaration.
  The ref is now `sha256(canonical identity)`: deterministic, recomputable, fixed-width, far below
  NAME_MAX. Duplicates are refused before any dict is keyed by them.
- **F4 — a closed canonical call-ref grammar.** `safe_call_ref()` accepted `calls//builder`,
  `calls/./builder`, `calls/builder/` and `home/alice`. Every production call-id source was
  inspected and run first; the grammar is closed to the two real shapes and the ref must AGREE
  with the CallIdentity it encodes. One validator serves identity and ledger alike.
- **F6 — the contract is corrected.** The extension model is documented as superseded; F140 serves
  stream N WITHIN one frozen Run Ledger.

## Local commits this round (user-authorized; NOT an acceptance signal)

| SHA | Subject |
|---|---|
| `8d186b4` | chore(f012): checkpoint round 13 reviewed state |
| `0f0f171` | fix(f012): make published run ledgers terminal and exact |
| `f850e44` | fix(f012): make ledger and call refs canonical |
| `7a3e616` | test(f012): prove closed ledger trust chain |
| `65332a0` | docs(f012): document final ledger semantics |

## Verification (authoritative pytest summaries — each recorded as its own Evidence command)

- New round-14 suites (terminal_ledger_finality, exact_ledger_set, ledger_ref_uniqueness,
  call_ref_grammar) → **119 passed**.
- Every F012 suite → **1148 passed**.
- F010/F011/Evidence integration → **499 passed**.
- CLI regressions (`tests/cli`, excluding the two suites under PRE-EXISTING) → **848 passed**.
- Docs consistency → **100 passed**.
- compileall (`packages apps scripts tests`) exit 0; `bash -n scripts/make_review_zip.sh` clean;
  `git diff --check` clean; `remedy integrity check` **all checks pass** (including
  `relevant_untracked`, now that the branch is committed rather than dirty).

## Pre-existing failures OUTSIDE this block (not introduced, not fixed)

`tests/cli/test_do_cmd_summary.py` and `tests/cli/test_product_spine.py` fail 18 tests **at base
`b0ba27a` itself**, proven on a pristine detached worktree of the base: they require
`docs/core-product-spine-v0.md` and sibling flat docs an earlier restructure moved. Round 14
touches none of those paths. The recorded CLI command excludes exactly those two files and the
debt is reported here rather than hidden by a green number.

## Known gap (unchanged, recorded honestly)

The preferred filesystem-tree identity for genuinely non-Git workspaces is still not implemented:
such a workspace records an explicit `unavailable` identity and therefore INCOMPLETE input
coverage, which is the finding's own stated fallback. It never yields `same_inputs=true`.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch committed locally,
**unpushed, unmerged**.
