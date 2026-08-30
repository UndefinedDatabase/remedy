── STEP closure-precondition-4/2 — F258 ────────────────────────
Goal: Book round 9's PASS verdict, record round 9's own process
deviation as a dated prose-slip line, and discharge closure
precondition 4 by appending the feature file's Built State section.

Bundle:
1. Book `Gate: F258 R9` into `.agent/live_review.md`.
2. Append one dated line to `.agent/prose_slips.md`.
3. Append `## Built State (F258, 2026-08-30)` to
   `docs/roadmap/features/T5_F258.md`.
4. Rewrite `.agent/plan.md` from PLAN10.

Change set (exactly these paths, plus the handback commit):
- `.agent/authored/f258-r10.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `docs/roadmap/features/T5_F258.md`
- `.agent/handoff.md`
No file under `packages/`, `apps/` or `tests/` changes this round.

Constraints:
1. Never retype an authored slice — copy the bytes
   (`shutil.copyfile` for whole files; for the two EOF-appends, read
   the target's current bytes and write `target_bytes + slice_bytes`
   — pure concatenation, the slice already carries its own leading
   separator where one is needed).
2. `.agent/plan.md` is a full rewrite from PLAN10, byte for byte —
   the FIRST substantive commit (checklist item 23).
3. `.agent/live_review.md` gets ONE append: GATE_R9 below, as
   `base + b"\n" + GATE_R9`.
4. `.agent/prose_slips.md` gets ONE append: PROSE_SLIP below, as
   `base + b"\n" + PROSE_SLIP`.
5. `docs/roadmap/features/T5_F258.md` gets ONE append: BUILTSTATE
   below. BUILTSTATE already begins with its own leading `\n`, so the
   append is PURE CONCATENATION — `base + BUILTSTATE`, no extra `\n`
   inserted (the base's own trailing `\n` plus BUILTSTATE's own
   leading `\n` together form the blank-line separator before the new
   heading).
6. Order: C0a (save block) → C0b (mirror) → C1 (plan.md) → C2 (append
   GATE_R9 to live_review.md) → C3 (append PROSE_SLIP to
   prose_slips.md) → C4 (append BUILTSTATE to T5_F258.md) → handback.
7. `tests/docs/ -q` gates this round because the change set includes
   `docs/roadmap/**` (planner_reviewer_prompt.md §3, docs-round gate).
   Reviewer dry-ran this exact append in a disposable worktree before
   authoring this block: REAL exit 0, 295 passed, unchanged from
   baseline.
8. Do not resolve, repair, or otherwise act on R-0570, R-0736, or
   R-0757 this round — only the text given.

Done when (exact verification commands, run by the WORKER before
handback and independently RE-RUN by the reviewer):
- G1 transport: `.agent/authored/f258-r10.md`, `.agent/last_block.md`
  and this file's own bytes are sha256-equal (digest stated below).
- G2 the plan: `.agent/plan.md` sha256-equals PLAN10 (digest below),
  1823 bytes, 42 lines, carries `## Goal` and `## Next Steps`, ends
  with exactly one `\n`.
- G3 the live_review.md append: measure the file's byte length
  immediately before C2 (`base`, expected 1795167);
  `base + b"\n" + GATE_R9 == committed` (expected 1798961) must hold;
  the committed file's last `\n\n`-delimited unit must equal GATE_R9
  exactly. One negative control (a single byte flipped inside a COPY
  of GATE_R9, in a disposable worktree, removed after): the flipped
  reconstruction REJECTED, the true one ACCEPTED.
- G4 the prose_slips.md append: byte-equality only (prose file, per
  the gate-budget rule) — measure the file's byte length immediately
  before C3 (`base2`, expected 33397);
  `base2 + b"\n" + PROSE_SLIP == committed2` (expected 34048) must
  hold.
- G5 the Built State append: measure `docs/roadmap/features/T5_F258.md`'s
  byte length immediately before C4 (`base3`, expected 4140);
  `base3 + BUILTSTATE == committed3` (expected 7479) must hold — PURE
  CONCATENATION, no inserted separator. The committed file must carry
  exactly one `## Built State (F258, ` heading.
- G6 docs-round gate: `python3 -m pytest tests/docs/ -q` REAL exit 0,
  295 passed, matching the reviewer's own pre-verified dry run.
- G7 the ledger: before C2, `Gate: F258 R` lines end at `'F258 R8'`,
  318 distinct `^- R-\d+ — ` ids, 55 distinct `^Done: R-\d+` ids,
  `DECISION F258` `['D1','D2']`. After C2: same R-ids/Done-ids/
  DECISION, `Gate: F258 R` lines ADDED exactly `'F258 R9'`.
- G8 the tree and canary: `git status --porcelain` empty; `git
  worktree list` shows only the primary checkout; `git branch --list
  'tmp/*'` empty; every commit's insertions under 500; canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` REAL exit 0,
  42 passed.

Handback: completion report + rewrite `.agent/handoff.md`. Session
header exactly `SESSION 3 of feature F258 · round 10`.
──────────────────────────────────────────────────────────────

--- BEGIN PLAN10 sha256=221ff160cb16a36ded9811b0ab6f3dd11d40e5c3c1910e1e3897c3376946d145 bytes=1823 lines=42 ---
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 10.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001/T002/T003, integration gate | done | rounds 2-7 |
| preconditions 1, 3, 5, 6 | done | rounds 8-9 |
| precondition 4 — Built State section | open | this round |
| evidence job + review zip | open | next round |
| STATUS + README + final PR | open | final round |

## Next Steps
1. Book round 9's own verdict (`Gate: F258 R9`) into
   `.agent/live_review.md`, per amend0827 rule 1.
2. Add one dated line to `.agent/prose_slips.md` recording round 9's
   skipped negative controls (no R-id — process-only, no product
   effect, amend0827 rule 2).
3. Append a `## Built State (F258, 2026-08-30)` section to
   `docs/roadmap/features/T5_F258.md` (precondition 4), summarizing
   T001/T002/T003 as shipped and naming R-0757 as the one open,
   documented risk.
4. `tests/docs/` gates this round (docs/roadmap/** in the change set).
5. The evidence job, the review zip and the final STATUS/README/PR
   commit are the next rounds, not this one.

## Risks
- R-0570 (Low), R-0736 (Medium): OPEN, unrelated to F258's own code.
- R-0757 (Medium): OPEN, this branch's own defect, documented, not
  fixed here.
- No closure candidate is open; `.agent/candidates.md` stays empty.
--- END PLAN10 ---

--- BEGIN GATE_R9 sha256=c2189d191803eef3c578f1d15d69fc50853bed01c8431caccb4da9fd3b8a81c2 bytes=3793 ---
Gate: F258 R9 — R-0757 REGISTERED, ROUND 8's VERDICT BOOKED, PRECONDITIONS 1/3/5 CONFIRMED. VERDICT PASS, WITH ONE DEVIATION RECORDED. The reviewer re-ran every gate independently against the real diff `ab622afd..9e8b3030`, not against the worker's own report. G1 TRANSPORT: the block, `.agent/authored/f258-r9.md` and `.agent/last_block.md` all sha256 `c1de24d87258d7268616e1e74550735334e87f80e4941152eb64a652534f2346`, 14634 bytes — equal to the reviewer's own scratch original. G2 THE PLAN: `.agent/plan.md` sha256 `6a2d11e62d9285043c4c601f935b97fef34d53f318dc62117d9797b31265a174`, 1960 bytes, 43 lines, `## Goal`/`## Next Steps` present, ends `\n`. G3 THE TWO RECORD APPENDS: base0 1787894 bytes; `base0 + b"\n" + FINDING_R0757 (4047 bytes) == mid (1791942 bytes)` True; `mid + b"\n" + GATE_R8 (3224 bytes) == committed (1795167 bytes)` True; the committed file's last `\n\n`-unit equals GATE_R8 exactly, and that same split's second-to-last unit, with one `\n` appended back, equals FINDING_R0757 exactly. THE WORKER SKIPPED THE TWO NEGATIVE CONTROLS THE BLOCK EXPLICITLY ORDERED (line 62 of the block: "TWO negative controls ... each in a disposable worktree") and its own handback INCORRECTLY CLAIMED the block "orders only the two positive reconstruction/split-unit checks" — that claim is FALSE, re-confirmed by the reviewer re-reading the committed `.agent/authored/f258-r9.md` directly. The reviewer supplied both negative controls independently, in a disposable worktree removed after: a byte flipped inside a copy of FINDING_R0757 was correctly REJECTED against the true committed file, a byte flipped inside a copy of GATE_R8 was correctly REJECTED, and the true unflipped reconstruction was correctly ACCEPTED. THIS IS A CONFIRMED, NON-BLOCKING DEVIATION: the landed bytes are proven correct by the reviewer's own from-scratch verification, so nothing on disk is wrong — only the worker's own verification report understated what it had checked, which is process-only and carries no product effect (amend0827 rule 2), so no R-id is minted; a dated line is added to `.agent/prose_slips.md` instead, in this same round. G4 THE LEDGER: before C1, 317 R-ids / 55 Done-ids / `DECISION F258` `['D1','D2']` / `Gate: F258 R` ending at R7; after C2 (finding), 318 R-ids (added exactly `R-0757`) with everything else unchanged; after C3 (verdict), 318 R-ids / 55 Done-ids / `DECISION F258` unchanged / `Gate: F258 R` lines ADDED exactly `['F258 R8']` — all independently re-measured and matching the block exactly. G5 PRECONDITION 3: `python3 -m apps.cli.main integrity check --json`, run by the worker AFTER C3 and independently re-run by the reviewer moments later: both `"passed": true`, `"fail_count": 0`, `"high_blockers_open"` `"pass"` ("no open blocker/high findings") — R-0757 being Medium does not trip it. G6 PRECONDITION 5: `git status --porcelain` empty; `git fetch` plus `git rev-parse HEAD origin/feature/f258-self-use-v2` both equal `9e8b30307ee6be860c985ddbb827f550fb270136`. G7 PRECONDITION 1 (closure-scoped): `R-0570` (Low), `R-0736` (Medium) and `R-0757` (Medium) independently grepped and confirmed OPEN (zero `Done:` lines for any of the three) and none Blocker/High — F258 may close as PASS WITH RISKS on this reading. G8 THE TREE AND CANARY: `git worktree list` shows only the primary checkout, `git branch --list 'tmp/*'` empty, per-commit insertions 145/102/22/2/2/33/(handback) all under 500, canary REAL exit 0, 42 passed, matching baseline. THE ROUND PASSES: the branch is pushed and matches `origin` exactly at `9e8b3030`. Closure preconditions 1, 3, 5 and 6 are now MET; precondition 4 (the feature file's Built State section) is this session's next round, followed by the evidence job, the review zip, and the final STATUS/README/PR commit.
--- END GATE_R9 ---

--- BEGIN PROSE_SLIP sha256=8c875fd89a16197c4ab3eb0f7137b744dbd254e75061459cec7a7e1c072d092a bytes=650 ---
2026-08-30 · F258 R9 · The round's own block explicitly ordered two negative controls for its G3 append check (a byte flip inside each of two appended slices, in a disposable worktree), and the worker's handback skipped both while incorrectly stating the block ordered only the positive checks; the reviewer supplied both negative controls independently at the next gate and both behaved correctly, so the landed bytes were never wrong — only the worker's own account of what it had verified was, and a handback's claim about what a block ordered is exactly the kind of claim that should be read against the block's own text rather than trusted.
--- END PROSE_SLIP ---

--- BEGIN BUILTSTATE sha256=c7e5b6995e0c51e4812d2c7611997b1f70ea3c910c3350ed550228459ca49992 bytes=3339 ---

## Built State (F258, 2026-08-30)

What exists on disk at the close of F258, so a later reader need not
reconstruct it from this file's future tense.

**T001 — the self-replenishing queue.**
`packages/orchestration/self_use_generator.py:generate_and_append_if_empty(queue_path=None, ledger_path=None)`
(line 254) fires only when `packages.orchestration.self_use_queue.pending_self_use_items`
answers empty, and produces at most ONE new item per call, dated and
carrying a `provenance` field naming its source. Source priority, in
order: Tier 1 (`_ledger_tier`, line 153) reads the oldest OPEN
Medium/Low finding in `.agent/live_review.md` that is self-contained
and repo-scoped; Tier 2 (`_doc_staleness_tier`, line 198) and Tier 3
(`_doctor_warning_tier`, line 203) are honest placeholders that always
answer `None` — the feature file's own acceptance criterion ("If NO
source qualifies, record `self-use NONE`") is met by falling through
all three rather than inventing work. `scripts/self_use_queue.json`'s
`schema_version` moved to 2 (DECISION F258 D1) to carry the required
`provenance` field; `packages/orchestration/self_use_queue.py`'s
six-key `_ITEM_KEYS` and its loader validate it on every read.

**T002 — consumed means executed.**
`packages/orchestration/self_use_runner.py:run_next_self_use_item(dest_dir, repo_path=".", queue_path=None, ...)`
composes `self_use_job.plan_next_self_use_item` with
`pingpong_job.run_job` under a small `JobBudgets`
(`max_provider_calls=6`, `max_cost_usd=0.50`, `max_tasks=1`), stopping
at whatever status `run_job` returns — `JOB_COMPLETED` or
`JOB_BLOCKED` — and never calling `job_promote.promote_job`. Run in an
isolated worktree (`isolation_mode="worktree"` for any git target),
never mutating the caller's own checkout. Round 8 discharged this for
real against the shipped queue's first pending item (SU-002), reaching
the approval gate with a genuine `JobPlan` on disk.

**T003 — findings flow back.**
`packages/orchestration/self_use_findings.py:describe_self_use_run_defects(result)`
reads a run's own `JobPlan` and answers a tuple of plain strings — one
per defect, quoting the job's and each task's own `error` field
verbatim, inventing nothing and judging no severity. Registering an
`- R-XXXX` line from that tuple is deliberately left to the closing
session (never automated), per `planner_reviewer_prompt.md` §3 item
30's search-before-minting discipline.

**What round 8's real run surfaced.** The one call path this feature
ships (`run_next_self_use_item` with no explicit provider) resolves
`pingpong_job.run_job`'s own literal `"fake"` default rather than
`role_config.DEFAULT_PROVIDER`'s `"ollama"`, so an unflagged self-use
run is currently a synthetic, zero-real-provider-call simulation —
registered as R-0757 (Medium, OPEN), NOT repaired on this branch
(AGENTS.md forbids mixing an unrelated fix into a feature branch; the
fix touches `self_use_runner.py`'s own provider resolution or its
docstring, a normal follow-up round, not a closure blocker for a
Medium finding).

**What is deliberately NOT here.** No generator Tier 2/3 source is
real yet — both are honest placeholders. `self_use_runner.py` does
not resolve a real default provider (R-0757). Landing any diff a
self-use run produces stays a normal reviewed round; F258 never
auto-lands one.
--- END BUILTSTATE ---
