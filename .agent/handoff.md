# Handback — F275 ROUND 1 — F275 is claimed, the record is re-headed and carries F274's round 23 PASS, DECISION F275 D1 is ruled, and staged batch 1 of `mission_readiness.py` is on disk UNWIRED

This file supersedes the F274 round 23 handback. It is written by the delegated worker of F275
round 1 on the reviewer's authored text; the reviewer never edits a work-tree file. It carries NO
verdict of its own — verdicts live in `.agent/live_review.md`, and this round's C2 booked the
reviewer's authored F274 round 23 PASS there. No `Done:` paragraph was written anywhere: only the
reviewer's authored text resolves a finding.

THIS FILE IS WRITTEN INSIDE C6, THE LAST COMMIT OF THE ROUND. One value it would otherwise carry
CANNOT EXIST when it is written and is deliberately not guessed: **C6's own `git diff --numstat`
columns** (the R-0149 pattern — a handoff cannot table the commit that writes it). All eight gates
G1–G8 were run at C5, strictly before this commit, exactly as the block ordered, and their real
exit codes and real numbers are transcribed in full below. G8's `git log` clause is the single
reading that C5 cannot complete, because C6 did not exist yet; its C5 reading is given verbatim and
the post-C6 confirmation is reported in the round's completion message.

## Session

SESSION 1 of feature F275 · round 1 · feature rounds so far 1 of the soft limit of 25, sessions 1
of 7.

Context self-assessment (amend0905-throughput): context is comfortable — this was a single
delegated round with no repair loop and no red gate, and nothing about it constrains the session's
remaining round budget.

Fortschritt: ~5 % (T001 begonnen: Claim ✅ · Record ✅ · D1 ✅ · Carry-over Batch 1 von 2 ✅ ·
Batch 2 offen · Verdrahtung offen · F260 D3 offen · Löschung offen · T002 offen · T003 offen) —
Schätzung

## State

| | |
|---|---|
| Feature | F275 — One world completion, part three (Tier 2) |
| Round | 1 (session 1) |
| Branch | `feature/f275-one-world-completion-part-three` |
| Cut from | `main` at `a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246 |
| Commits | `35b4d250` · `b7ee3eb3` · `74197329` · `46e5336d` · `c4cebfcb` · `352659da` · C6 (this commit) |
| Open findings | 65 by DISTINCT id (68 distinct registrations − 3 distinct resolutions), UNCHANGED — this round registered none and resolved none |
| High among them | 4 — R-0803, R-0804, R-0806, R-0807, all F273's per DECISION F272 D12 |
| Pull request | NONE. The block forbade creating one this round. |
| Artifact builds | NONE attempted this round (no evidence bundle, no review zip) |

## Commits and their real `git diff --numstat` columns

| Commit | Subject | File | + | − |
|---|---|---|---|---|
| `35b4d250` | F275 R1 C0a: save the round 1 step block verbatim as the authored record | `.agent/authored/f275-r1.md` | 379 | 0 |
| `b7ee3eb3` | F275 R1 C0b: mirror the round 1 step block into the last-block state file | `.agent/last_block.md` | 367 | 290 |
| `74197329` | F275 R1 C1: re-point the plan at F275 round 1 | `.agent/plan.md` | 30 | 30 |
| `46e5336d` | F275 R1 C2: re-head the review record, book F274 round 23 PASS and rule DECISION F275 D1 | `.agent/decisions.md` | 16 | 0 |
| `46e5336d` | " | `.agent/live_review.md` | 41 | 33 |
| `c4cebfcb` | F275 R1 C3: claim F275 in the roadmap ledger and re-point the context file | `.agent/context.md` | 25 | 21 |
| `c4cebfcb` | " | `docs/roadmap/STATUS.md` | 1 | 1 |
| `352659da` | F275 R1 C4: land staged batch 1 of the carried mission readiness module, unwired | `packages/orchestration/mission_readiness.py` | 369 | 0 |
| C6 | F275 R1 C6: rewrite the handback for round 1 | `.agent/handoff.md` | — | — |

C5 is a measurement step and writes no file, by the block's own bundle. No commit exceeds the
DECISION F104 D1 cap of 500 insertions: the largest production diff is C4 at 369, and C0a/C0b are
verbatim rewrites of a single `.agent/**` state file, which that decision exempts by name. NO
declared-oversize allowance was spent — this feature's single allowance remains reserved for
T002's atomic flip.

The change set is exactly the nine paths the block named, and nothing else.

## Gates — one line each, with the REAL exit code

| Gate | Command / reader | REAL exit | Key numbers |
|---|---|---|---|
| G1 TRANSPORT | `python3 .remedy-wt/f275_r1_g1.py` | 0 | all three digests EQUAL at 36124 bytes / `6c75575db624c8e932909fc02cb68e667dc4235f4ff14e27daaace496f886071` — committed `.agent/authored/f275-r1.md` = committed `.agent/last_block.md` = scratch `.remedy-wt/f275-r1-FINAL.md` |
| G2 THE PLAN | `python3 .remedy-wt/f275_r1_g2.py` | 0 | sha256 `ea6355ae…02ed` ✅ · 2526 bytes ✅ · 43 lines (< 50) ✅ · `^## Goal$` 1 · `^## Next Steps$` 1 |
| G3 THE RECORD | `python3 .remedy-wt/f275_r1_g3.py` | 0 | all six parts PASS — see the breakdown below |
| G4 THE CLAIM | `python3 .remedy-wt/f275_r1_g4.py` | 0 | FROM 0 · TO 1 · `^- \[~\] F275 ` 1 · `^- \[~\] ` 1 in the whole file · `^- \[x\] F\d{3} — ` 76 (unchanged) · `.agent/context.md` sha256 `bfbc3bf1…a8ce` ✅ |
| G5 THE CARRIED CODE | `python3 .remedy-wt/f275_r1_g5.py` | 0 | 17 of 17 definitions BYTE-IDENTICAL to their spans at the base commit · `ast.parse` OK · no extra top-level binding |
| G5 ruff | `python3 -m ruff check packages/orchestration/mission_readiness.py` | 0 | `All checks passed!` |
| G5 numstat | `git show --numstat --format= 352659da -- packages/orchestration/mission_readiness.py` | 0 | **369 insertions**, measured, under the 500 cap |
| G6 UNWIRED | `python3 .remedy-wt/f275_r1_g6.py` | 0 | 1722 tracked files searched under `packages/ apps/ tests/ scripts/ docs/`; `orchestration\.mission_readiness` **0**, `orchestration import mission_readiness` **0**; `overnight_readiness.py` and `cluster_deletion_map.txt` byte-identical base→C4 |
| G7 `tests/docs/` | `python3 -m pytest tests/docs/ -q` | 0 | **303 passed** in 0.49s |
| G7 roadmap index | `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` | 0 | **30 passed** in 0.38s |
| G7 state reader 1/4 | `python3 -m pytest tests/ui_server/ -q` | 0 | **506 passed** in 21.55s |
| G7 state reader 2/4 | `python3 -m pytest tests/orchestration/test_test_runner.py -q` | 0 | **51 passed** in 3.40s |
| G7 state reader 3/4 | `python3 -m pytest tests/regression/test_resource_safety.py -q` | 0 | **21 passed** in 11.54s |
| G7 state reader 4/4 | `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` | 0 | **16 passed** in 0.30s |
| G7 canary | `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | **42 passed** in 21.44s |
| G8 THE TREE | `python3 .remedy-wt/f275_r1_g8.py` | 0 | no `.agent/STOP` · `git status --porcelain` EMPTY · branch correct · `git worktree list` 1 entry (the primary checkout) · 6 commits C0a→C4, every one SINGLE-PARENT |

Every suite ran ALONE, one command per call, in the block's order, from the primary checkout. The
two numbers the reviewer pre-measured at the base commit both reproduce exactly: `tests/docs/` at
303 passed and the canary at 42 passed.

### G3 in full — the six parts

- **(a) BYTES.** `.agent/live_review.md` **506317 → 510121**; `.agent/decisions.md` **919768 →
  927408**, a gain of **7640** = the DEC1 slice's 7639 bytes + the one newline the append
  convention writes. Both measured over the committed C2 blob, both landing on the block's numbers.
- **(b) THE CARRIED REGION IS UNTOUCHED.** `^## Findings$` matches EXACTLY ONCE before (offset
  3397) and once after (offset 3844). The 502920 bytes from that line to end of file have sha256
  `ac08353106bfe118095963282161da9db92051b5be4fe03a8a86b53da920169e` BEFORE and the SAME sha256
  AFTER. The plain substring `## Findings` occurs at FOUR offsets — 491, 3397, 356923, 365947 — so
  the line-anchored split constraint 2 ordered was load-bearing and was used.
- **(c) EXACT EDGES.** live_review STARTS with the HEAD1 bytes ✅ and ENDS with the RECORD1 bytes ✅;
  the pre-commit `.agent/decisions.md` blob is a byte-exact PREFIX of the post-commit one ✅ and
  DEC1 is a byte-exact SUFFIX of it ✅.
- **(d) ORDERED EQUALITY**, by a reader independent of (c): N = **8** paragraphs, COUNTED from the
  DEC1 slice itself and not taken from the block. The file's last 8 blank-line units equal the
  slice's 8 paragraphs IN ORDER, per-unit sha256 reported, all 8 MATCH.
- **(e) NEGATIVE CONTROL**, in scratch only, on DEC1's FIRST appended paragraph (the
  `## DECISION F275 D1 …` heading): byte 5 flipped `'C'` → `'c'`. Reader (c) REJECTS it (the
  mutated slice is not a suffix) and reader (d) REJECTS it (first mismatching unit index 0). The
  mutation was never written to disk; `.agent/decisions.md` re-read from disk afterwards is
  UNCHANGED at 927408 bytes / `1625a89dfa69613beab73d5558e6f0a9d0bfb0366f5d19e5b30020b550821ae2`.
- **(f) COUNTS**, each landing on its predicted pair: blank-line units **212 → 214** · `^Gate: `
  **22 → 23** · `^Gate: F274 R23 ` **0 → 1** · distinct `^- R-\d+ — ` ids **68 → 68** · distinct
  `^Done: R-\d+ — ` ids **3 → 3** · OPEN SET BY DISTINCT ID **65 → 65**. The subtraction is over
  DISTINCT resolved IDS; the record carries **5** `Done:` LINES, measured, which is why subtracting
  lines would report the open set two too low.

### G5 — the seventeen carried definitions

All seventeen byte-identical, in source order (which was verified equal to the block's order rather
than assumed): `OvernightStopReason` 879B · `_CAP_AVAILABLE` 29B · `_CAP_BLOCKED` 25B ·
`_CAP_NOT_SUPPORTED` 37B · `BoundedOvernightPolicy` 1093B · `default_overnight_policy` 144B ·
`OvernightCapability` 320B · `OvernightChecklistItem` 260B · `OvernightRisk` 151B ·
`OvernightNextAction` 118B · `OvernightReadinessReport` 886B · `_now` 69B · `_Inputs` 464B ·
`_gather_inputs` 2967B · `_build_budget_summary` 1018B · `_build_evidence_summary` 703B ·
`_build_capabilities` 5016B.

SEVEN of them are `@dataclass`-decorated and their spans START AT THE DECORATOR, as the SPEC
required — `BoundedOvernightPolicy`, `OvernightCapability`, `OvernightChecklistItem`,
`OvernightRisk`, `OvernightNextAction`, `OvernightReadinessReport` and `_Inputs`. A span taken from
the `ast` node's own `lineno` would have silently dropped seven decorators.

The five DELIBERATELY EXCLUDED names were confirmed present in the source and ABSENT from the new
module: `OvernightEvidenceStatus`, `_CAP_UNKNOWN`, `OvernightRunPlan`, `build_overnight_plan`,
`export_plan_json`.

### G6 — the bare-token collision the block predicted

Measured, not assumed: the bare token `mission_readiness` occurs at exactly **FOUR** sites outside
the new module — `packages/orchestration/overnight_mission.py:35` (docstring) and `:840` (the
function definition), and `apps/cli/commands/overnight_mission_cmd.py:127` and `:128`. The block's
reason for gating on the DOTTED forms instead of the bare token reproduces exactly. Both dotted
forms return ZERO, so nothing imports the new module.

## Item-status table — every C and every G, exactly once

| Item | Status | Reason |
|---|---|---|
| C0a save the block as `.agent/authored/f275-r1.md` | done | branch cut from `main` at the named base; copied with `shutil.copyfile`, never retyped |
| C0b mirror into `.agent/last_block.md` | done | same bytes, same method |
| C1 replace `.agent/plan.md` with PLAN1 | done | byte-for-byte, digest verified before and after |
| C2 the record in ONE commit | done | head swap + RECORD1 append + DEC1 append, one commit |
| C3 pair P1 + CTX1 | done | FROM occurred exactly once and was rewritten; CTX1 applied byte-for-byte |
| C4 create `mission_readiness.py` | done | built from the SPEC by the worker's own `ast` script, not copied from `.remedy-wt/` |
| C5 run G1–G8 | done | every gate run, real exit codes recorded above |
| C6 rewrite `.agent/handoff.md` | done | this file |
| G1 TRANSPORT | done | exit 0 |
| G2 THE PLAN | done | exit 0 |
| G3 THE RECORD (a–f) | done | exit 0, all six parts |
| G4 THE CLAIM | done | exit 0 |
| G5 THE CARRIED CODE | done | exit 0, 17/17, ruff 0, 369 insertions |
| G6 UNWIRED | done | exit 0, both dotted forms at zero |
| G7 THE SUITES | done | exit 0 on all seven runs |
| G8 THE TREE | deviated | every clause measured and PASS at C5; its `git log` clause names C6, which did not exist at C5, so that one row is confirmed post-C6 in the completion message |

## Deviations

1. **The head-swap construction was under-specified by ONE BYTE, and the block's own gates
   resolved it.** C2's prose says "replace everything in `.agent/live_review.md` BEFORE the findings
   heading with the HEAD1 slice". The base prefix is 3397 bytes and ends with `\n\n` — a blank line
   separating the `## Steps` prose from the `## Findings` heading. HEAD1 is 3843 bytes and ends with
   a single `\n`. Substituting HEAD1 for the prefix literally yields **510120** bytes and **213**
   blank-line units; G3(a) predicts **510121** and G3(f) predicts **214**. Both variants were
   measured in scratch before anything was written. Writing HEAD1 followed by ONE separator newline
   — which preserves the blank line the base file has, and matches the newline convention the block
   states for appends in constraint 3 — yields **510121** bytes and **214** units, satisfying BOTH
   gate predictions and every stated constraint (the carried region is byte-identical, the file
   starts with the HEAD1 bytes and ends with the RECORD1 bytes). No third construction satisfies
   both: appending RECORD1 with two newlines instead also reaches 510121 bytes but leaves the unit
   count at 213 and contradicts constraint 3, which the `.agent/decisions.md` arithmetic
   (919768 + 1 + 7639 = 927408, confirmed) independently pins to ONE newline. The applied
   construction is therefore the unique one satisfying the block; the slice itself was NOT edited.
2. **The block's P1 regions carry no digest.** Constraint 1 and the delegating message both state
   that each `BEGIN <NAME>` line states that slice's own sha256 and byte count. Five do —
   PLAN1, CTX1, HEAD1, RECORD1, DEC1, all five verified before use. `BEGIN P1-FROM` and
   `BEGIN P1-TO` state neither. Both were extracted the same way and measured: FROM 120 bytes /
   `75bd943aebd4e1286b54e52b7e10e84630eb0bdf039ada69b685491d26055d61`, TO 120 bytes /
   `80a0803f833d25b2b21d357f20979a82fc517e85179934d6ae936cf6f283ee98`, and the containment reading
   the block quotes was re-run rather than trusted: `TO contains FROM: False`.
3. **The Fortschritt line was authored by the worker.** The block orders "the Fortschritt line
   repeated verbatim" but supplies no Fortschritt line to repeat — it is normally carried into the
   block from the reviewer's operator brief. The line in the Session section above is the worker's
   own honest estimate of F275's progress and is labelled Schätzung; the reviewer should replace it
   if the brief's line differs.
4. **G8's `git log` clause cannot close at C5.** Reported as `deviated` in the item-status table
   above for the stated structural reason, not as a failure: the clause requires C6, and the block
   requires the gates to run before C6.

Nothing else deviated. No gate went red. No instruction was worked around, no slice was edited, no
`Done:` paragraph was written, no pull request was created, nothing was merged, no force-push
happened, and no destructive verification touched the primary checkout — the G3(e) negative control
ran entirely in memory and the tracked file was re-read afterwards to prove it.

## Next expected action

1. The reviewer re-runs this round's gates itself and issues the verdict for round 1. A worker's
   summary is never evidence.
2. Before authoring round 2, re-read `.agent/STOP` from disk (Phase 1 rule 1 of
   docs/agents/self_drive_protocol.md), then the Open PR Gate — there is currently NO open pull
   request, so nothing is owed there.
3. ROUND 2 is the SECOND staged batch: it completes `packages/orchestration/mission_readiness.py`
   with the remaining carried definitions from the reachability closure DECISION F275 D1 measured,
   still UNWIRED, and lands `tests/orchestration/test_mission_readiness.py`, the test file AGENTS.md's
   Code Discoverability convention names after the source. `packages/orchestration/overnight_readiness.py`
   stays untouched until the deletion.
4. Then the wiring round, which cuts the one surviving `packages/orchestration/ui_server.py` edge
   the deletion map records for `overnight_readiness` and removes that map line in the SAME commit.
   Note DECISION F275 D1's closing warning for that round: it must not import the old bare-name
   `mission_readiness` function out of the deletion-bound `overnight_mission.py`.
5. The branch is pushed. It has no pull request and must not get one until the reviewer says so.
