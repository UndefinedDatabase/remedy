STEP T001 (carry-over 1, batch 1) — F275 One world completion, part three — ROUND 1

Goal:
  Claim F275, cut its branch, re-point the state files, re-head the review record, book F274's
  branch-terminating round 23 verdict, rule DECISION F275 D1, and land the FIRST staged batch of
  the carried readiness module UNWIRED.

Read first (you are not required to trust anything below that you can read yourself):
  AGENTS.md · docs/agents/self_drive_protocol.md · docs/roadmap/features/T2_F275.md ·
  DECISION F274 D1 and D2 in `.agent/decisions.md` · `tests/orchestration/cluster_deletion_map.txt`

ENVIRONMENT, so you do not rediscover it (each item cost an earlier session a round):
  - `VAR=x cmd`, `env VAR=x cmd` and `export VAR=x; cmd` are ALL DENIED. Set env in-process.
  - `cp` is DENIED. Copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`.
  - Bare `ruff` is DENIED. Use `python3 -m ruff check <path>`.
  - The Bash tool does not surface non-zero exits. Wrap a gate as
    `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and NEVER pipe into `tail` when you need the exit
    code — the pipe reports tail's status. Redirect to a file instead.
  - Shell loops, `$(...)` inside a compound, and `$?` in a compound are refused by FORM. Use
    `python3 -` heredocs for counting, hashing and line-ending work.
  - Commit subjects carry no leading-slash token, no absolute path and no secret-like string.

Bundle, in this exact commit order. There is no commit after C6.
  C0a  Cut the branch `feature/f275-one-world-completion-part-three` from `main` at
       `a5bf894946ab6de053a4232109d6341a63533768`, then save THIS ENTIRE BLOCK verbatim as
       `.agent/authored/f275-r1.md`, copied with `shutil.copyfile` from the file the delegating
       message names. Never retype it.
  C0b  Mirror the same bytes into `.agent/last_block.md` with `shutil.copyfile`.
  C1   Replace `.agent/plan.md` with the PLAN1 slice, byte for byte.
  C2   The record, in ONE commit: replace everything in `.agent/live_review.md` BEFORE the
       findings heading with the HEAD1 slice, append the RECORD1 slice at end of file, and
       append the DEC1 slice at end of `.agent/decisions.md`.
  C3   Apply pair P1 to `docs/roadmap/STATUS.md` and replace `.agent/context.md` with CTX1.
  C4   Create `packages/orchestration/mission_readiness.py` per the SPEC below. UNWIRED.
  C5   Run every gate G1 to G8 and record its REAL exit code and REAL output.
  C6   Rewrite `.agent/handoff.md` as the handback. It quotes all eight gates, which is why they
       run at C5, strictly before this commit.

Change set — exactly these paths, and nothing else:
  .agent/authored/f275-r1.md · .agent/last_block.md · .agent/plan.md · .agent/live_review.md ·
  .agent/decisions.md · .agent/context.md · docs/roadmap/STATUS.md ·
  packages/orchestration/mission_readiness.py · .agent/handoff.md

Constraints:
  1. Apply every slice BYTE FOR BYTE. Extract each one programmatically as the bytes strictly
     between its `BEGIN <NAME>` line and its `END <NAME>` line, verify the extracted bytes
     against that BEGIN line's own sha256 and byte count BEFORE applying, and never let a
     marker line reach any file. Do not edit a slice, even to fix something you believe wrong;
     if a slice is wrong, apply it as given and say so in the handback's deviations.
  2. THE LIVE-REVIEW HEAD SWAP ANCHORS ON A LINE, NOT ON A SUBSTRING. The literal text
     `## Findings` ALSO occurs inside the header's own blockquote, at byte offset 491, so a
     plain `.index("## Findings")` finds the WRONG anchor and would destroy the record. Split on
     the LINE-ANCHORED regular expression `^## Findings$` in multi-line mode, which matches
     EXACTLY ONCE in the file. Everything from that line to end of file is carried forward
     BYTE-IDENTICAL; only the prefix before it is replaced.
  3. Append convention: `.agent/live_review.md` and `.agent/decisions.md` each already end with
     exactly one newline, so an append writes one newline, then the slice's bytes. Each slice
     already ends with its own newline. Add nothing else.
  4. P1 is a REWRITE, not an append: the containment test printed `TO contains FROM: false`, and
     the FROM occurs EXACTLY ONCE in `docs/roadmap/STATUS.md`. Replace that one occurrence, then
     re-measure FROM at 0 and TO at 1. Do not run a FROM-zero count on any other pair; there is
     no other pair in this round.
  5. C4 IS BUILT FROM THE SPEC BELOW BY YOUR OWN SCRIPT, not copied from any file under
     `.remedy-wt/`. No consumer is edited, no import of the new module is added anywhere, and
     `packages/orchestration/overnight_readiness.py` IS NOT TOUCHED — its sha256 at C4 equals
     its sha256 at the base.
  6. Run the suites SERIALLY, one command per call.
  7. Nothing destructive runs in the primary checkout. If you need a mutation, use a disposable
     `git worktree` under `.remedy-wt/`, remove it by EXACT PATH, and prove
     `git status --porcelain` empty afterwards.
  8. Never force-push. Never merge anything. Push the branch with
     `git push -u origin feature/f275-one-world-completion-part-three`. Do NOT create a pull
     request this round.

SPEC for C4 — `packages/orchestration/mission_readiness.py`, staged batch 1 of 2, UNWIRED.
  WHAT IT IS. DECISION F275 D1, which the DEC1 slice of this block lands, rules the first
  carry-over's destination, its partition and its staging. This commit performs batch 1 only.
  HOW TO BUILD IT. Parse `packages/orchestration/overnight_readiness.py` with `ast` at the base
  commit and copy, BYTE-IDENTICALLY, the source span of each of these SEVENTEEN top-level
  definitions, in this order, which is their source order:
      OvernightStopReason, _CAP_AVAILABLE, _CAP_BLOCKED, _CAP_NOT_SUPPORTED,
      BoundedOvernightPolicy, default_overnight_policy, OvernightCapability,
      OvernightChecklistItem, OvernightRisk, OvernightNextAction, OvernightReadinessReport,
      _now, _Inputs, _gather_inputs, _build_budget_summary, _build_evidence_summary,
      _build_capabilities
  A definition's span STARTS AT ITS FIRST DECORATOR where it has one — several of these are
  `@dataclass` classes, and an `ast` node's own `lineno` points at the `class` line, so a span
  taken from `lineno` silently drops the decorator.
  DELIBERATELY EXCLUDED, and this is not an oversight: `OvernightEvidenceStatus` and
  `_CAP_UNKNOWN` are reachable from nothing in the module and have no user anywhere outside it,
  and `OvernightRunPlan`, `build_overnight_plan` and `export_plan_json` are the plan path, which
  dies with the cluster. DECISION F275 D1 records the measurement behind both exclusions.
  THE FILE'S SHAPE. A module docstring saying what it is and that batch 1 is unwired; then the
  import block copied from the source's own — `from __future__ import annotations`, a blank
  line, then the `dataclasses`, `datetime`, `pathlib`, `typing` and `uuid` imports; then TWO
  blank lines; then the seventeen definitions separated by two blank lines each. The two-blank-
  line gap after the import block is not cosmetic: with one blank line `python3 -m ruff check`
  fails `I001`, which the reviewer confirmed by running it.
  RENAME NOTHING. The carried symbols keep their `overnight_` names, per DECISION F275 D1's
  second ruling; F261 owns renames.

Done when — EIGHT gates. Run every one at C5, after C4 and before the handback commit C6.
Record the REAL exit code and the REAL output of each; the word "green" is not a result.

  G1 TRANSPORT. sha256 of the committed blob `.agent/authored/f275-r1.md` equals the sha256 of
     the committed blob `.agent/last_block.md`, and both equal the digest of the scratch
     original the delegating message names. Report the three digests and the byte count. This
     proves the chain scratch-original to saved copy to mirror, and claims nothing about the
     emitted bytes.
  G2 THE PLAN. `.agent/plan.md` sha256 equals
     `ea6355ae797d77238f31c95f41130558d66618323b04c1334c2e838c7d2402ed`; its byte count is 2526;
     its line count is 43, under the AGENTS.md cap of 50; `^## Goal$` occurs once and
     `^## Next Steps$` occurs once.
  G3 THE RECORD, all six parts, over the committed C2.
     (a) BYTES. `.agent/live_review.md` is 506317 at the base and 510121 after;
         `.agent/decisions.md` is 919768 at the base and 927408 after, a gain of 7640 — the
         DEC1 slice's 7639 bytes plus the one newline the append convention writes. Report both
         numbers you measured.
     (b) THE CARRIED REGION IS UNTOUCHED. The bytes from the `^## Findings$` line to end of
         file, taken before the edit, have sha256
         `ac08353106bfe118095963282161da9db92051b5be4fe03a8a86b53da920169e`, and the same bytes
         at the same position after the edit have the SAME sha256. This is the whole point of
         the re-head, so measure it rather than assuming it.
     (c) EXACT EDGES. The new `.agent/live_review.md` STARTS with the HEAD1 bytes and ENDS with
         the RECORD1 bytes; the pre-commit `.agent/decisions.md` blob is a byte-exact PREFIX of
         the post-commit one, and DEC1 is a byte-exact SUFFIX of it.
     (d) ORDERED EQUALITY, by a reader independent of (c). Split the post-commit
         `.agent/decisions.md` on blank lines, COUNT the DEC1 slice's own paragraphs into N
         rather than taking N from this block, and compare the file's last N units against the
         slice's N paragraphs IN ORDER, reporting a per-unit sha256.
     (e) NEGATIVE CONTROL, on the FIRST appended paragraph of DEC1, in scratch only: flip one
         byte and confirm that BOTH the reader of (c) and the reader of (d) REJECT it. Re-read
         the tracked file afterwards and confirm it is unchanged. Never write the mutation to
         disk.
     (f) COUNTS over the post-commit `.agent/live_review.md`, each landing on its predicted
         pair: blank-line units 212 to 214 · `^Gate: ` 22 to 23 · `^Gate: F274 R23 ` 0 to 1 ·
         distinct `^- R-\d+ — ` ids 68 to 68 · distinct `^Done: R-\d+ — ` ids 3 to 3 ·
         OPEN SET BY DISTINCT ID 65 to 65. The open set does not move because this round
         registers no id and resolves none. Subtract DISTINCT resolved IDS, never `Done:`
         LINES, of which the record carries five.
  G4 THE CLAIM. In `docs/roadmap/STATUS.md` after C3: the P1 FROM occurs 0 times and the P1 TO
     occurs 1 time; `^- \[~\] F275 ` occurs exactly once; `^- \[~\] ` occurs exactly once in the
     whole file; and `^- \[x\] F\d{3} — ` still occurs 76 times, unchanged, because a claim
     accepts nothing. `.agent/context.md` sha256 equals
     `bfbc3bf1ae84942cef771ac4055ef671308f2be363a1112ec7777445d8d6a8ce`.
  G5 THE CARRIED CODE, over the committed C4. For EACH of the seventeen named definitions, its
     byte span in `packages/orchestration/mission_readiness.py` is IDENTICAL to that
     definition's byte span in `packages/orchestration/overnight_readiness.py` at
     `a5bf894946ab6de053a4232109d6341a63533768`; report how many of the seventeen matched. The
     new module PARSES under `ast.parse`. The command
     `bash -c 'python3 -m ruff check packages/orchestration/mission_readiness.py; echo "REAL_EXIT=$?"'`
     exits 0. `git show --numstat` for C4 on that path reports INSERTIONS UNDER 500 — report the
     number you measured rather than a number this block states.
  G6 UNWIRED, AND THE SOURCE UNTOUCHED. A repo-wide search over `packages/`, `apps/`, `tests/`,
     `scripts/` and `docs/` for the two DOTTED IMPORT FORMS of the new module —
     `orchestration\.mission_readiness` and `orchestration import mission_readiness` — returns
     ZERO matches, so nothing imports it. DO NOT gate on the BARE token `mission_readiness`:
     it already occurs at FOUR sites as an unrelated FUNCTION in the cluster module
     `packages/orchestration/overnight_mission.py` and its handler, which the reviewer measured
     at the base commit, so a bare-token zero-gate is unmeetable and would fail an honest
     worker. DECISION F275 D1 records that collision and rules it.
     `packages/orchestration/overnight_readiness.py` has
     the same sha256 at C4 as at the base commit. `tests/orchestration/cluster_deletion_map.txt`
     is byte-identical to its base version: this round cuts no edge and removes no line.
  G7 THE SUITES, each run ALONE and in this order, every one from the primary checkout:
     `python3 -m pytest tests/docs/ -q`, then
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`, then the FOUR state
     readers as FOUR separate runs — `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py` — and last the canary
     `python3 -m pytest tests/cli/test_golden_path.py -q`. Report each command's REAL exit code
     and its REAL passed count. The reviewer measured `tests/docs/` at 303 passed and the canary
     at 42 passed at the base commit; a different number is not automatically wrong, but report
     what you measured.
  G8 THE TREE. `.agent/STOP` does not exist. `git status --porcelain` is EMPTY. The branch is
     `feature/f275-one-world-completion-part-three`. `git worktree list` shows only the primary
     checkout. `git log --oneline` shows C0a through C6 as single-parent commits in that order.

Handback: rewrite `.agent/handoff.md`. It carries the mandated sections — the state block with
the SESSION NUMBER (this is SESSION 1 of F275) and the Fortschritt line repeated verbatim, the
per-commit changed-files table with real `git diff --numstat` columns, one line per gate with
its REAL exit code, the open-findings count, the item-status table covering every C and every G
exactly once, the deviations, and the next expected action. It has NO length cap. Do not write
a `Done:` paragraph anywhere: only the reviewer's authored text resolves a finding.

BEGIN PLAN1 sha256=ea6355ae797d77238f31c95f41130558d66618323b04c1334c2e838c7d2402ed bytes=2526
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. T001 runs FIRST, and its `git rm`
sequence is never started by a session that cannot finish it.

## Current Step

ROUND 1 claims F275 in the roadmap ledger, cuts the branch, re-points this file and
`.agent/context.md`, re-heads `.agent/live_review.md`, books F274's branch-terminating round
23 verdict into it, and records DECISION F275 D1 — which rules the first carry-over's
destination module, its measured definition partition and its staging. The round's code commit
lands the FIRST staged batch of `packages/orchestration/mission_readiness.py`, UNWIRED, so no
consumer moves and the tree is green at every commit boundary.

## Next Steps

1. The SECOND staged batch completes `mission_readiness.py`, still unwired, and lands the test
   file named after it.
2. The wiring round gives the CLI and the cockpit the carried readiness view, cuts the one
   surviving `packages/orchestration/ui_server.py` edge the deletion map records for
   `overnight_readiness`, and removes that line from the map in the SAME commit, which is what
   `tests/orchestration/test_cluster_deletion_map.py` requires of every cut.
3. DECISION F260 D3, the deletion paragraph, drafted with R-0832's fix clause binding it and
   R-0831 named among the ideas deleted rather than inherited.
4. The prototype-cluster deletion itself, bounded by the map's edges, one commit per module
   group, under the four measurements amend0906-triage-throughput names for a deletion round.

## Risks

- 65 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12. The integrity gate's
  `high_blockers_open` check is WRONG about them, which is R-0648 and itself open.
- The first carry-over moves 655 lines of definitions, which exceeds the DECISION F104 D1 cap
  of 500 insertions for one commit, so it is staged across commits and the new module stays
  unwired until the last of them. This feature's single declared-oversize allowance is
  reserved for T002's atomic flip, which cannot be staged at all.
END PLAN1

BEGIN CTX1 sha256=bfbc3bf1ae84942cef771ac4055ef671308f2be363a1112ec7777445d8d6a8ce bytes=3885
# Context — F275 One world completion, part three

## Active Branch
feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Scope
F275 (Tier 2; depends on F259's binding vocabulary page, on the record F260 closed at, on the
run re-key and unified record F272 closed at, and on the deletion map, the import-reachability
ratchet and the consumer-edge cuts F274 closed at; blocks F261, F266, F268, F269, F270, F271
and F263): the remainder DECISION F274 D8 split off F274 at the standing soft limit. Task
slicing per `docs/roadmap/features/T2_F275.md`: T001 the reachability-gated cluster deletion
with its two carry-overs and DECISION F260 D3, T002 measure the flip and rule the cap, T003
the classic runner.

## Do not touch
Everything `T2_F272.md`'s and `T2_F274.md`'s "Do not touch" sections name, unchanged: the
scope-fence builtin deny list (F017), the approval gate, STATUS semantics. No command is
RENAMED here — F261 owns renames. No module outside F260's Design lists is deleted, and a
module the reachability probe REACHES is reported with its import chain and deferred in
DECISION F260 D3, never deleted.

## Assumptions
- Cleanliness before compatibility: no migration shim, no compatibility reader, no alias. A
  helper accepting both records is what AGENTS.md Scope Control forbids by name.
- F272's and F274's rulings stay binding here and are NOT restated; both feature files keep
  their DECISION sections unedited for exactly that purpose. F272 D13, D14 parts 1 and 3, and
  D15 are starting conditions, as are F274 D1 through D7.
- NEVER SPLIT INSIDE T001's DELETION. DECISION F274 D1 rules that this prohibition binds the
  `git rm` sequence and NOT its prerequisites: the carry-overs and DECISION F260 D3 leave the
  tree consistent at every commit boundary and may land across sessions.

## Constraints
The bullets in this first group are STANDING project constraints, carried forward from the
context this file replaces.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in the primary
  checkout, which satisfies `git status --porcelain` empty at every verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>` is the spelling
  every gate of this feature orders.
- `remedy` (the built CLI) is DENIED to this session's reviewer, subagents included; a round
  needing it delegates the run to the worker and reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops, `$(...)`
  substitution, and `$?` inside a compound command — so checks of that shape are re-expressed
  in Python and the re-expression is reported. A pipe into `tail` also MASKS the real exit
  code, so a gate reporting one redirects to a file instead of piping.
- A fresh worktree has neither `apps/ui/node_modules` nor a built `apps/ui/dist`, so a full
  suite run there carries a known environment failure class that a control run must establish
  before any mutated run is read as evidence.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.
END CTX1

BEGIN HEAD1 sha256=57eff85e50db81418781f4a28ebe30598b0a33571746c5fe57051ae28ebf5072 bytes=3843
# Live Review — F275 One world completion, part three

> Round-by-round review record, re-headed at the F275 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named F274, which is
> accepted: its STATUS line went `[x]` at `c6003e5d2638efd783f45cb83f1108f906e5ef3b` and its
> pull request 246 merged at `a5bf894946ab6de053a4232109d6341a63533768`, at this session's
> Open PR Gate. Only the heading, this paragraph and the `## Steps` section below are
> rewritten. Every finding record below `## Findings` is carried forward BYTE-IDENTICAL — the
> block that ordered this re-head gates that region's sha256 equal before and after the edit,
> as its gate G3 — and finding ids continue the monotonic R-XXXX series across the re-head.
> Measured by the reviewer at `a5bf894946ab6de053a4232109d6341a63533768`, the branch point: 68
> DISTINCT ids matching `^- R-\d{4} — ` against 3 DISTINCT ids matching `^Done: R-\d{4} — `, so
> 65 findings are open BY DISTINCT ID. The subtraction is over DISTINCT resolved IDS and not
> over `Done:` LINES, of which the record carries five: two ids are resolved by two paragraphs
> each, and counting lines would report the open set two too low. THE NEXT ID THIS FEATURE
> MINTS IS R-0840.
> F274's LAST round has an entry here, which is the exception rather than the rule: under
> docs/agents/self_drive_protocol.md there is no second window, so the reviewer books a
> branch-terminating verdict into the FIRST commit of the next feature's first round rather
> than losing it with the session. Records belonging to features already marked `[x]` in
> docs/roadmap/STATUS.md are not here at all: `scripts/rotate_live_review.py` moves them
> byte-verbatim into the append-only `.agent/live_review_archive.md` in every closure
> sequence, under operator amendment amend0905-throughput, and that archive is read on demand
> by id, never at session start.

## Steps

THE SLICE ORDER BELOW IS THE ONE DECISION amend0907-cluster-first D1 RULED ON 2026-09-07 and
DECISION F274 D8 CARRIED INTO THIS FEATURE: the deletion runs FIRST, because it was last in
three consecutive features and each of them closed by split-and-close before reaching it.
R1 claim F275 in the roadmap ledger, cut the branch, re-point `.agent/plan.md` and
`.agent/context.md`, re-head this record, book F274's round 23 verdict into it, rule DECISION
F275 D1 and land the first staged batch of the carried readiness module UNWIRED → the second
staged batch and the module's own test → the wiring round, which cuts the one surviving
`packages/orchestration/ui_server.py` edge and removes its line from the deletion map in the
same commit → DECISION F260 D3, the deletion paragraph, drafted → the prototype cluster
deletion itself, one commit per module group, which is NEVER SPLIT ACROSS SESSIONS → T002, the
`Job.id` flip measured with a recording property and its cap route ruled → T003, the classic
runner, `job.run --cycles`, `job.run-next`, their handlers and tests, and the resolver collapse
DECISION F260 D5 places in the same commit range → the integration gate → the closure sequence.

The two carry-overs F260's Design orders before the first `git rm` are NOT both owed as work.
The SECOND — every user-settable route-policy knob checked against F110's config keys — was
performed at F274 round 3 and registered as R-0831, which is OPEN and stays open until the
deletion round deletes those knobs with their modules and DECISION F260 D3 names route policy
among the ideas deleted rather than inherited. The reviewer re-measured it at
`a5bf894946ab6de053a4232109d6341a63533768` and confirms it unchanged: not one of the eight
knob names occurs in `packages/orchestration/role_config.py` or
`packages/orchestration/model_routing.py`. No second id is minted for it, per §3 item 30.
END HEAD1

BEGIN RECORD1 sha256=1587c6f7126eb79180ee7fe46f25b3ea8dbfde42ae300601f2c7b64f7e48561e bytes=3356
Gate: F274 R23 — the F274 round 23 entry. VERDICT PASS, and it is booked here by F275's round 1 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1: round 23 was the LAST round of its branch, so docs/agents/planner_reviewer_prompt.md §4 item 13 gives it no gate entry on its own branch by construction, and the carrier was the round 23 handback committed at `c6003e5d2638efd783f45cb83f1108f906e5ef3b` and pushed. WHAT THIS ENTRY MEASURES, AND WHY IT MEASURES ANYTHING AT ALL. Round 23's own text routed gates G4 through G8 to "the completion message", because Rule A4 makes the closure commit the last commit on the branch and a handback cannot transcribe a gate over the commit that writes it. Under docs/agents/self_drive_protocol.md there is no second window, so that channel ended with the session and those five readings are NOT recoverable; §3 item 31's last clause rules that the reviewer measures such numbers at the NEXT gate and records them in that round's ledger entry, which is this paragraph. G1 through G3 were transcribed in full in the round 23 handback and are not re-derived here. THE RE-MEASUREMENT, taken by the reviewer of F275 round 1 at `a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246, over the merged tree rather than over any report: `docs/roadmap/STATUS.md` carries exactly ONE line matching `^- \[x\] F274 — ` and 76 lines matching `^- \[x\] F\d{3} — `; `README.md` states "76 of 275 registered items accepted." and its tier-2 row reads `| 2 | Minimal Self-Build Runtime | 19 | 28 |`, so the counter and the tier Done column both agree with the ledger rather than merely with each other; and `SU-013` in `scripts/self_use_queue.json` carries `consumed_by` exactly `F274`. Those are the four edits round 23's C3 claimed, and all four are on disk as claimed. The docs gate that C3's own STATUS and README edits must satisfy was re-run by this reviewer at the same commit: `python3 -m pytest tests/docs/ -q` exits 0 at 303 passed, and a red control in a disposable worktree — flipping the F275 line to `[x]` — takes it to exit 1 with 2 failed, so the gate is demonstrably able to fail and its pass is evidence. THE OPEN SET IS UNCHANGED at 65 by DISTINCT id, 68 distinct registrations against 3 distinct resolutions, and four of the 65 are High — R-0803, R-0804, R-0806 and R-0807 — every one of them F273's rather than F274's, per DECISION F272 D12, which is why F274's close is PASS_WITH_RISKS and not PASS. THE PULL REQUEST: 246 was open, non-draft, from `feature/f274-one-world-completion-part-two` into `main` and MERGEABLE, its CI run 34197259162 completed with conclusion `success` on the branch tip, and this session merged it at the Open PR Gate with `gh pr merge 246 --merge --delete-branch`, which is the first action Phase 1 rule 2 of docs/agents/self_drive_protocol.md orders and the action round 23's own handback named as owed. NOT CLAIMED BY THIS ENTRY: the byte-level forensics of C3 itself. This reviewer did not witness round 23's C3 numstat columns, its per-slice application proofs or its `git worktree list` reading, and reconstructing them from the merged tree would be a claim about a measurement nobody took — the honesty shape §4.9's digest fallback requires. What is claimed is exactly what was re-measured above.
END RECORD1

BEGIN DEC1 sha256=a457acb404353de501738ff81bd1f7d5a900d1227241f5cbd23c54e8a0ba085d bytes=7639
## DECISION F275 D1 — the first carry-over lands in a NEW `mission_readiness` module, as a BYTE-IDENTICAL move of a measured definition set, staged and unwired (2026-09-08)

CONTEXT. F260's Design section orders two carry-overs before the first `git rm`, and DECISION F274 D2 measured the first of them — the read-only overnight readiness and report views — as a move of "25 of the 29 top-level definitions" and "650 of its 894 lines" of `packages/orchestration/overnight_readiness.py` "into a surviving module". D2 did not NAME that module, did not fix which definitions move, and did not settle whether the moved symbols keep their names. Those three questions block the round that performs the move, and none of them is answered by any text on disk.

THE MEASUREMENT, taken by the reviewer at `a5bf894946ab6de053a4232109d6341a63533768` with an `ast` reference closure rather than by reading the prose. `packages/orchestration/overnight_readiness.py` is 894 lines and binds 34 names at module level, 29 of them `ClassDef` or `FunctionDef` and 5 of them module-level assignments. Taking the closure of the names reachable from the readiness and report entry points — `build_overnight_readiness`, `export_readiness_json`, `build_overnight_report`, `render_overnight_report_markdown` and `select_overnight_next_action` — gives 29 bindings totalling 655 definition lines, of which 25 are `ClassDef` or `FunctionDef`. The complement is exactly five bindings: `OvernightRunPlan`, `build_overnight_plan` and `export_plan_json`, which are the plan path and are reachable only from it, at 69 lines; and `OvernightEvidenceStatus` and `_CAP_UNKNOWN`, which are reachable from NOTHING in the module at all, at 7 lines. Counting only `ClassDef` and `FunctionDef`, which is the rule D2's own numerals use, that complement is FOUR and the move is 25 of 29 — so this measurement reproduces DECISION F274 D2 exactly at a commit twenty rounds later, and does not amend it. WHAT NOTHING OUTSIDE THE MODULE NEEDS: the plan path's three names are imported only by `apps/cli/commands/overnight_cmd.py`, the module's own cluster-bound handler, and by `tests/orchestration/test_overnight_readiness.py`, its own test, both of which die in the deletion; the `export_plan_json` occurrences in `packages/orchestration/self_dogfood.py` and `apps/cli/commands/self_cmd.py` are a DIFFERENT function of the same name and are not this module's, which is the kind of name collision a grep alone would have mis-read. `OvernightEvidenceStatus` has no user anywhere outside the module.

CHOSEN, FIRST: THE DESTINATION IS A NEW MODULE `packages/orchestration/mission_readiness.py`. It sits beside `mission_state.py`, `mission_dossier.py`, `mission_compiler.py` and `mission_plan_schema.py`, so the file name matches the command name F260's Design gives the carried view, and AGENTS.md's Code Discoverability convention that a test file is named after the source it covers gives its test `tests/orchestration/test_mission_readiness.py` without further choice. ALTERNATIVE: carry the definitions into an existing surviving module such as `mission_state.py`, rejected because that module owns the mission record and would acquire 655 lines of an unrelated concern, and because a module that gains a second reason to change is the shape this repository's naming rules exist to prevent.

THE NAME IS PARTLY OCCUPIED, AND THE COLLISION IS RULED RATHER THAN DISCOVERED LATER. Measured at `a5bf894946ab6de053a4232109d6341a63533768`: the bare token `mission_readiness` already occurs at four sites, as a FUNCTION `mission_readiness` defined at `packages/orchestration/overnight_mission.py` line 840, named in that module's docstring, and imported by `apps/cli/commands/overnight_mission_cmd.py`. `overnight_mission.py` is one of the twenty-four cluster modules F260's Design lists, so that holder is deletion-bound and the name frees itself inside this feature. THE RULING: the MODULE name is taken NOW rather than waiting, because unlike DECISION F274 D2's `mission report` case there is no collision to wait out — `packages.orchestration.mission_readiness` and `packages.orchestration.overnight_mission.mission_readiness` are distinct fully-qualified paths, nothing shadows anything, and no import resolves differently because both exist. What the overlap DOES cost is grep: for the few rounds until the deletion, a bare search for `mission_readiness` returns the old function as well as the new module, which is why the gate proving the new module unwired searches for the DOTTED module path and not for the bare token — a bare-token zero-gate is unmeetable today, and this reviewer's first draft of it was, which is how the collision was found. The wiring round must not import the old function by its bare name.

CHOSEN, SECOND: THE MOVE IS BYTE-IDENTICAL PER DEFINITION AND RENAMES NOTHING. Each carried definition's bytes in the new module equal that definition's bytes in `overnight_readiness.py` at `a5bf894946ab6de053a4232109d6341a63533768`, which makes the move mechanically provable by a gate rather than reviewable by eye. The symbols therefore keep the `overnight_` spelling inside a `mission_readiness` module, which IS a synonym drift against AGENTS.md's "one spelling per concept" and is accepted deliberately and temporarily: `docs/roadmap/features/T2_F275.md`'s "Do not touch" section rules that no command is RENAMED here because F261 owns renames, and a symbol rename folded into the move would make the one strong proof available to this round — byte equality — unavailable, for a cosmetic gain in the same feature that is about to delete the word `overnight` from the tree entirely. ALTERNATIVES: rename the symbols during the move, rejected for the reason just given; rename them in the wiring round, rejected as churn on code whose only consumer is being written in that same round. The question is routed to F261 with this paragraph as its pointer.

CHOSEN, THIRD: THE MOVE IS STAGED ACROSS TWO COMMITS IN DIFFERENT ROUNDS, AND THE NEW MODULE IS UNWIRED UNTIL THE WIRING ROUND. 655 insertions exceed the DECISION F104 D1 cap of 500 for a single commit, and this feature's ONE declared-oversize allowance under AGENTS.md's Commit Discipline is reserved for T002's atomic flip, which DECISION F272 D15 rules cannot be staged at all — so spending it here would leave the flip with no route. The batches are PREFIXES of the carried set in source order, which is safe in either order because the module opens with `from __future__ import annotations` and therefore evaluates no annotation at import time; the first batch runs from `OvernightStopReason` through `_build_capabilities`. Until the wiring round nothing imports the new module, so every intermediate commit is green by construction and `overnight_readiness.py` itself is not touched. CONSEQUENCE: the surviving `packages/orchestration/ui_server.py` edge that `tests/orchestration/cluster_deletion_map.txt` records for `overnight_readiness` is cut in the wiring round and its map line is removed in that SAME commit, which is what `tests/orchestration/test_cluster_deletion_map.py` requires of every cut; DECISION F274 D4 already HELD that cockpit section for exactly this carry-over. The name `mission report` stays occupied until the deletion round, per DECISION F274 D2's third ruling, so this round claims `mission readiness` only.

REVERSE by deleting this section: the destination module then has no ruled name, the partition returns to D2's prose numerals with no measurement behind them, and the staging returns to being undecided, which is the state this ruling replaced.
END DEC1

BEGIN P1-FROM (docs/roadmap/STATUS.md, occurs exactly once)
- [ ] F275 — One world completion, part three — the cluster deletion, the atomic record flip and the classic runner
END P1-FROM

BEGIN P1-TO
- [~] F275 — One world completion, part three — the cluster deletion, the atomic record flip and the classic runner
END P1-TO
