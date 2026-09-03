# Handoff — F112 Prompt budget per task class, round 12 (DECISION F112 D5 + PLAN12 + T3_F112.md T003c amendment — decision/plan/feature-file only, no production code)

## Session

SESSION 4 of feature F112 · round 12 · rounds so far 12.

This round books round 11's already-independently-reviewed PASS verdict
into `.agent/live_review.md` (RECORD11, amend0827 rule 1 — a pending
verdict books in the FIRST COMMIT of the next round that is happening
anyway, i.e. round N's verdict books in round N+1's first commit),
appends DECISION F112 D5 (fresh investigation this round found
`run_pingpong`'s `use_compiled_context` gate requires BOTH
`compiled_context_paths` and `compiled_context_candidates` to be
non-empty, and job-dispatch `TaskEntry` has no fenced-scope source at
all — `fenced_paths=[]` is the only value available today, so
`bool([])` is `False` and the entire compiled/capped path can never
activate, not merely the `cannot_fit` branch DECISION F112 D4 found
unreachable), and amends `docs/roadmap/features/T3_F112.md`'s Task
slicing to add **T003c**: a job task markdown `"## Files"` section
parsed into a new `TaskEntry.files_hint: list[str]` field, the
prerequisite T003b2b2 needs before it can be built at all.

This round ships **no production code** — permitted under amend0827
rule 1 because the whole change set is a DECISION plus a feature-file
amendment (planning content, the §4 item 7 "wrong spec is a finding
routed to planning" shape), not a verdict/registration/correction. No
mutation red-proof was run (nothing under `packages/` or `tests/`
changed this round).

## Range

Review of `2ef8c4dd..HEAD` (commits C0a, C0b, C1, C2, C3, C4, plus this
handback commit C5 itself — six commits total this round, no C6; the
shorter shape reflects this round's decision/plan/feature-file-only
scope, not a departure from the block). **This range is UNREVIEWED by
construction** — round 12 has not yet been independently re-reviewed by
the reviewer; no verdict on this round's own work is claimed anywhere
in this file.

## Commits

### 7dcf71d7 F112 R12 C0a: save round 12 block to .agent/authored/f112-r12.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r12.md` | 83/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 55a46fb5 F112 R12 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 37/39 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption). Byte-equality confirmed before commit (see Verification Step 0 — `cmp` itself was denied by this session's sandbox, same as round 11; a `python3` byte-equality read substituted). |

### e85c6edc F112 R12 C1: append RECORD11 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD11 (round 11's verdict) via `content_bytes + b"\n" + RECORD11_bytes` — the ONE-newline formula. |

### 912781e1 F112 R12 C2: apply PLAN12 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 22/24 | Whole-file replacement with PLAN12, extracted programmatically from the committed authored file, not retyped. No trailing newline (per the block). |

### 7b26d4b0 F112 R12 C3: append DECISION F112 D5 to decisions.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 14/1 | Appended DECISION F112 D5 (the `use_compiled_context` both-lists-non-empty finding; T003c added as T003b2b2's prerequisite) via the same ONE-newline formula. |

### 17ed4d52 F112 R12 C4: add T003c to T3_F112.md Task slicing (DECISION F112 D5)
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T3_F112.md` | 8/0 | Applied the block's single REWRITE pair (FROM confirmed to occur exactly once before applying): appended a T003c bullet to Task slicing, between the existing T002 and T003 bullets, naming DECISION F112 D5 as its source and stating it is a prerequisite for T003b2b2, not an alternative to it. |

## External actions

`git push` → run immediately after this handback commit (C5); outcome
recorded in the completion report, not in this file (write-once rule).

No worktrees created or removed this round (no mutation red-proof —
no production code changed). `git worktree list` before this handback
showed only the primary checkout and the pre-existing, unrelated
`remedy/job-*` worktrees; no `f112-r12-mutation-*` entries were ever
created.

## Verification

**Step 0 TRANSPORT** — `cmp .agent/authored/f112-r12.md
.agent/last_block.md` was DENIED by this session's sandbox (a
bash-permission denial on the `cmp` invocation itself, unrelated to
file content — the same denial round 11 hit); substituted a `python3`
byte-equality read: `a == b` → **True**, both files **10485 bytes**.
Extracted-slice byte counts, measured programmatically against the
pinned figures in the block: RECORD11 **2195 bytes** (pinned 2195,
match), PLAN12 **2163 bytes** (pinned 2163, match), DECISION F112 D5
**5548 bytes** (pinned 5548, match). PASS.

**Step 1 LEDGER (RECORD11)** — `.agent/live_review.md` measured
**2267760 bytes** immediately before the append (matches round 11's own
post-append size exactly, per RECORD10's earlier append). Appended as
`content_bytes + b"\n" + RECORD11_bytes` (ONE newline). Post-size
measured at **2269956 bytes**, matching `2267760 + 1 + 2195` exactly.
Old-file-is-prefix check: **True**. Tail-equality check
(`post[len(old):] == b"\n" + RECORD11_bytes`): **True**. PASS.

**Step 2 PLAN** — PLAN12 extracted programmatically from the committed
`.agent/authored/f112-r12.md` (between its markers) to an in-memory
byte string, then Python byte-equality against `.agent/plan.md`:
**equal, 2163 bytes both sides**. `wc -l .agent/plan.md` → **46**
(the file has no trailing newline per the block's own instruction, so
literal `wc -l` undercounts by one against the content-line count — the
same pattern round 11's plan.md showed: `wc -l` read 48 there against a
stated 49 content lines). Content-line count (newline-count + 1) →
**47**, matching PLAN12 exactly. `grep -c '^## Goal' .agent/plan.md` →
**1**. `grep -c '^## Next Steps' .agent/plan.md` → **1**. PASS.

**Step 3 DECISION (D5)** — `.agent/decisions.md` measured **761111
bytes** immediately before the append (matches round 12's own
pre-append size, i.e. round 11's post-D4-append size). Appended as
`content_bytes + b"\n" + D5_bytes` (ONE newline). Post-size measured at
**766660 bytes**, matching `761111 + 1 + 5548` exactly. Old-file-is-prefix
check: **True**. Tail-equality check: **True**. PASS.

**Step 4 T3_F112.md AMENDMENT (C4)** — Grepped the file for the block's
FROM string before applying: **exactly 1** occurrence. Applied via
`Edit` (REWRITE). Diff reviewed (`git diff` before commit): exactly the
8-line T003c bullet inserted between the existing T002 and T003
bullets, no other change. `grep -c 'T003c' docs/roadmap/features/T3_F112.md`
→ **1**. `python3 -m pytest tests/docs/ -q` (docs-round gate, required
because `docs/roadmap/**` changed) → **295 passed**.
`python3 -m pytest tests/cli/test_golden_path.py -q` (canary) → **42
passed**. PASS.

`git status --porcelain` in the primary checkout read **empty**
immediately before this handback's own commit. PASS.

## Authored-text proofs

`.agent/authored/f112-r12.md` (committed at `7dcf71d7`) vs
`.agent/last_block.md` (committed at `55a46fb5`): byte-identical (Step
0 transport check above, `python3` byte-equality substitute for the
sandbox-denied `cmp`). RECORD11, PLAN12 and DECISION F112 D5 were all
extracted programmatically from this committed file (never retyped)
and applied via the stated append formulas or whole-file write; every
application was confirmed against pinned byte counts and before/after
equality checks above (Steps 1-3). The T3_F112.md REWRITE pair (C4) was
typed directly from the round's own prompt text (not carried inside the
authored block's markers, unlike the ledger/plan/decision texts) and
verified mechanically (occurrence count, post-edit `grep`, and a full
`git diff` read before commit) per Step 4 above.

## Deviations & assumptions

1. **`cmp` itself was denied by this session's Bash sandbox** (a
   permission denial on the bare `cmp <file1> <file2>` invocation, not
   a content or path issue) at the C0b self-check. Substituted a
   `python3` byte-equality read (`open(...).read() == open(...).read()`),
   which returned `True` — the two files are confirmed byte-identical by
   an equivalent method, not merely asserted. Same deviation round 11
   declared for the same reason.
2. **No search of the open-findings ledger (`.agent/live_review.md`'s
   open R-ids) was performed this round.** No new R-XXXX finding was
   minted or claimed resolved this round — only DECISION F112 D5 was
   authored (a scope/design decision, not a defect record). Item 30's
   "grep the DEFECT before minting an id" checklist obligation
   therefore does not apply this round; stated here for completeness
   rather than silently omitted.
3. **This round has six commits (C0a, C0b, C1, C2, C3, C4), ending at
   C5 as the handback commit itself** — no C4/C5 production-code split
   and no C6, unlike rounds 9-11's eight-commit shape. This is the
   block's own instructed sequence for a decision/plan/feature-file-only
   round (no production code), not a deviation from it; stated here to
   make the commit-count shift explicit for the reader, per item 30's
   "an extra commit, a dropped one, or a reordering is a deviation even
   when correct" instruction (this is a shorter sequence, the mirror
   case, and equally worth stating plainly).
4. **`git push` outcome is not recorded in this file** (write-once
   rule) — see the completion report for the real result.

## Next

**T003c** (per DECISION F112 D5 and the rewritten `.agent/plan.md` Next
Steps): parse `"## Files"` in job task markdown (mirrors the existing
`"Acceptance:"` inline-marker pattern) into a new
`TaskEntry.files_hint: list[str]` field, exported/imported like
`inputs`/`task_class`; update `task_entry_to_planned_task`'s mapping.
Its own dedicated round(s); T003b2b2 (the live call-site wiring) waits
until T003c lands, per DECISION F112 D5.

**RECORD12 (this round's own verdict) is NOT YET in the ledger** —
round 12 has not been independently re-reviewed by the reviewer yet, so
no verdict exists to book. Per amend0827-process-diet rule 1, it books
in the FIRST COMMIT of the next round that is happening anyway — that
is round 13's own C1. Before starting T003c: Phase 1 rule 1 — re-check
`.agent/STOP` from disk (not present as of this round).
