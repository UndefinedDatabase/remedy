── STEP closure-precondition-6/2 — F258 ────────────────────────
Goal: Book round 7's PASS verdict into the ledger, then execute
STATUS_closure_protocol.md precondition 6's REAL plan+run half (no
finding registration yet — that is the reviewer's own next-round act).

Bundle:
1. Book `Gate: F258 R7` (RECORD8) into `.agent/live_review.md`.
2. Rewrite `.agent/plan.md` from PLAN8.
3. Run `packages.orchestration.self_use_runner.run_next_self_use_item`
   FOR REAL against the shipped queue (`scripts/self_use_queue.json`,
   no `queue_path` override), in an isolated `REMEDY_DATA_DIR`, and
   record the raw outcome under `.agent/gate_f258_closure/`.

Change set (exactly these paths, plus the handback commit):
- `.agent/authored/f258-r8.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/gate_f258_closure/self_use_run.txt`
- `.agent/gate_f258_closure/self_use_defects.txt`
- `.agent/handoff.md`
No file under `packages/`, `apps/`, `tests/` or `docs/` changes this round.
`scripts/self_use_queue.json` is READ, never written, this round —
`consumed_by` is set only in F258's final closure commit
(STATUS_closure_protocol.md Algorithm step 5), never here.

Constraints:
1. Never retype an authored slice — copy the bytes
   (`shutil.copyfile`), never hand-retype.
2. `.agent/plan.md` is a full rewrite from PLAN8 below, byte for byte.
3. `.agent/live_review.md` gets ONE append this round: RECORD8 below,
   as `base + b"\n" + RECORD8` where `base` is the file's own current
   bytes immediately before this commit. RECORD8 is a single paragraph
   (one line, one trailing `\n`) — no internal blank line.
4. Order: C0a (save block) → C0b (mirror) → C1 (plan.md, the FIRST
   substantive commit, per checklist item 23, since this round also
   touches the finding ledger) → C2 (append RECORD8) → C3 (the real
   self-use run + its two evidence files) → handback commit.
5. For C3, isolate `REMEDY_DATA_DIR` IN-PROCESS (never a shell `VAR=x`
   prefix — denied in this sandbox) to
   `<repo_root>/.remedy-wt/f258-r8-selfuse/data`, and use
   `<repo_root>/.remedy-wt/f258-r8-selfuse/jobs` as `dest_dir`. Pass NO
   `builder_provider`/`reviewer_provider`/`builder_name`/`reviewer_name`
   override — let the call resolve the real product default exactly as
   `packages/orchestration/self_use_runner.py`'s own docstring commits
   to ("the same product default any other unflagged job resolves").
   Do NOT delete `<repo_root>/.remedy-wt/f258-r8-selfuse/` afterward —
   the reviewer re-loads the persisted `JobPlan` from it at review time.
6. Wrap the C3 call so EVERY outcome is recorded honestly: a completed
   or blocked `JobPlan`, a `SelfUseRunError`/`SelfUseJobError` raised by
   planning, or any other exception — whichever happens is written to
   `self_use_run.txt` verbatim, never hidden, never retried into a
   different-looking outcome. An environment-caused failure (e.g. the
   resolved provider being unreachable in this sandbox) is an HONEST,
   ACCEPTABLE outcome for this round — it still discharges "run to the
   approval gate", and it mints NO finding, because amend0827
   rule 2 spends an R-id only on a defect with PRODUCT effect, and an
   unreachable local provider in this sandbox is not one.
7. `self_use_defects.txt` carries the VERBATIM output of
   `packages.orchestration.self_use_findings.describe_self_use_run_defects`
   called on the SAME `result` — one string per line — or the literal
   line `EMPTY TUPLE — nothing to register` when the tuple is empty, or
   `N/A — ...` when planning itself raised before any `result` existed.
   Do NOT write an `- R-XXXX` line into `.agent/live_review.md` for any
   of this — that stays the reviewer's own next-round act, per
   `packages/orchestration/self_use_findings.py`'s own docstring and
   checklist item 30 (grep the open set before minting).
8. Confirm and report `scripts/self_use_queue.json`'s sha256 before and
   after C3 in `self_use_run.txt` — they must be equal.
9. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` after
   the round's own commits, REAL exit 0, matching the standing baseline
   (42 passed) — report it in the handback, not asserted about itself
   in `.agent/live_review.md`.
10. Handback per `docs/agents/handback_template.md`: changed-files
    table, every gate's REAL result, deviations section (if any),
    `git status --porcelain` empty, `git worktree list` showing only
    the primary checkout, `git branch --list 'tmp/*'` empty, push
    confirmed. Session header: `SESSION 3 of feature F258 · round 8`.

Done when (exact verification commands, run by the WORKER before
handback and independently RE-RUN by the reviewer):
- G1 transport: `.agent/authored/f258-r8.md`, `.agent/last_block.md`
  and this file's own bytes are sha256-equal (digest stated below).
- G2 the plan: `.agent/plan.md` sha256-equals PLAN8 (digest below),
  1978 bytes, 41 lines, carries `## Goal` and `## Next Steps`, ends
  with exactly one `\n`.
- G3 the record append: measure `.agent/live_review.md`'s byte length
  immediately before C2 (`base`); `base + b"\n" + RECORD8 == committed`
  must hold, and the committed file's LAST `\n\n`-delimited unit must
  equal RECORD8 exactly. Negative control (a single byte flipped
  inside a COPY of RECORD8, in a disposable worktree, removed after):
  the flipped reconstruction must be REJECTED, the true one ACCEPTED.
- G4 the ledger, before C1/after C2: 317 distinct `^- R-\d+ — ` ids
  and 55 distinct `^Done: R-\d+` ids UNCHANGED; `DECISION F258` ids
  unchanged at `['D1','D2']`; `Gate: F258 R` lines go from
  `['F258 R1','F258 R2','F258 R3','F258 R4','F258 R5','F258 R6']` to
  the same six PLUS exactly `'F258 R7'`.
- G5 the self-use run: `self_use_run.txt` names a real `job_id`;
  independently re-loading that same job id via
  `packages.orchestration.pingpong_job.load_job_plan(job_id)` (with
  `REMEDY_DATA_DIR` pointed at the SAME
  `.remedy-wt/f258-r8-selfuse/data`) reproduces the SAME status, error
  and per-task fields the evidence file states — OR, if planning
  itself raised before any job existed, the same exception type and
  message is reproducible by calling
  `packages.orchestration.self_use_job.plan_next_self_use_item` again
  read-only (it is provably read-only; re-calling it is safe).
- G6 the defects: independently calling
  `describe_self_use_run_defects` on the SAME reloaded `JobPlan`
  reproduces `self_use_defects.txt` byte for byte.
- G7 the queue: `scripts/self_use_queue.json` is byte-identical before
  and after this round's entire commit range (`git diff --stat
  <base>..HEAD -- scripts/self_use_queue.json` is EMPTY), and its
  `consumed_by` fields are unchanged.
- G8 the tree and canary: `git status --porcelain` empty; `git
  worktree list` shows only the primary checkout; `git branch --list
  'tmp/*'` empty; every commit's insertions under 500 except a
  declared exception with its inseparability reason; canary REAL
  exit 0, 42 passed.

Handback: completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

--- BEGIN PLAN8 sha256=a9c4cec349ad58183a4ca956de12caded2509140c983a70049dfac818ceac73f bytes=1978 lines=41 ---
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 8.

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
| T001 self-replenishing queue | done | rounds 2-4 |
| T002 consumed means executed | done | round 5 |
| T003 findings flow back | done | round 6 |
| the dedicated integration-gate round | done | round 7 |
| precondition 6 — plan + run the queue's next item for real | open | this round |
| closure sequence (preconditions 1,3,4,5; evidence job; zip; STATUS+README; PR) | open | next round |

## Next Steps
1. This round books round 7's own verdict (`Gate: F258 R7`) into
   `.agent/live_review.md` first, per amend0827 rule 1.
2. Run `packages.orchestration.self_use_runner.run_next_self_use_item` for
   real against the shipped queue's next pending item, in an isolated
   `REMEDY_DATA_DIR`, recording the raw `JobPlan` and
   `packages.orchestration.self_use_findings.describe_self_use_run_defects`
   output under `.agent/gate_f258_closure/`. No finding is registered this
   round — the reviewer authors any `- R-XXXX` text next round from the
   real recorded output (STATUS_closure_protocol.md precondition 6;
   T5_F258.md T003).
3. `scripts/self_use_queue.json` stays byte-unchanged this round —
   `consumed_by` is set only in the final closure commit (Algorithm step 5).

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- No closure candidate is open; `.agent/candidates.md` stays empty.
--- END PLAN8 ---

--- BEGIN RECORD8 sha256=fa945cf77ca7380f7253a5f8d341d1f5af1e4ea19a6a30019b32dd34bc63ec5d bytes=4890 ---
Gate: F258 R7 — THE DEDICATED INTEGRATION-GATE ROUND (TIER 3): FULL SUITE RUN TWICE, BRANCH AND BASE, BOTH INDEPENDENTLY REPRODUCED BY THE REVIEWER FROM SCRATCH. VERDICT PASS. THE INTEGRATION GATE PASSES. The reviewer re-ran every gate independently against the real diff `be848035..176ec7fc`, not against the worker's own report, including re-executing BOTH the branch suite and the base suite from scratch in the reviewer's own disposable worktree, rather than trusting the worker's raw logs alone. G1 TRANSPORT: the block, its `.agent/authored/f258-r7.md` copy and `.agent/last_block.md` all sha256 `51fb13f461b633c737272859ca3ba5330a8957d0198310b5048a69ff49eb9bdd`, 10097 bytes, 175 lines — equal. G2 THE PLAN: `.agent/plan.md` sha256 `8bff7f63194c5c4d0701f8570f554e6a0d0d4985b3c91a3ac5b055584f0badb1`, 1702 bytes, 38 lines, `## Goal`/`## Next Steps` present, ends `\n`. G3 THE RECORD APPEND: base 1779093 bytes ending in one `\n`; `base + b"\n" + RECORD7 (3909 bytes) == committed (1783003 bytes)` True; the last `\n\n`-delimited unit equals RECORD7 exactly (RECORD7 is a single paragraph by construction, joining what the source verdict text originally carried as two paragraphs, to keep every ledger entry's own shape at N=1 — reworded, not merely reformatted, and reads cleanly). A negative control (byte-flip) was independently reproduced and correctly rejected. G4 THE LEDGER: `DECISION F258` unchanged at `['D1','D2']`; `Gate: F258 R` lines ADDED exactly `['F258 R6']`; 317 distinct `R-` ids and 55 distinct `Done:` ids unchanged. G5 THE BRANCH RUN: independently re-run by the reviewer at the current HEAD (`176ec7fc`) rather than at `846fdef8` — confirmed equivalent first, since `git diff --name-only be848035 176ec7fc -- packages/ apps/ tests/ docs/` is EMPTY across the round's ENTIRE range, not merely the four commits the worker's own deviation covered. REAL exit 0, `18677 passed, 20 skipped in 141.93s` — matching the worker's reading (18677/20/0, ~127s) exactly. THE WORKER'S DEVIATION (running at `846fdef8` instead of literally `be848035` to avoid detaching the primary checkout's HEAD, which would falsely fail every `self_dogfood_execution`-gated test) is accepted: sound reasoning, proven equivalent by an empty diff, not merely asserted. G6 THE BASE RUN: independently reproduced by the reviewer in a FRESH disposable worktree at the same merge-base (`18ae7129`), with the SAME parity fix (`shutil.copytree(..., symlinks=True)` then `os.utime` every `apps/ui/dist` file past the checkout time) applied proactively. The reviewer's own run gave REAL exit 0, `18642 passed, 20 skipped, 0 failed` — the ONE failure the worker's run showed (`tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`) did NOT reproduce in the reviewer's own run, which is itself corroborating evidence for the worker's own attribution: this id's `pgrep -f apps.cli.grouped.*--help` predicate is machine-wide and known flaky under `-n auto` parallel load (already on record twice, F032 R16/R17 and the F033 integration gate, both times serial-passing) — two independent runs disagreeing on this ONE id while agreeing on every other of 18677+ ids is exactly the signature of a load-dependent flake, not a regression. R-0736's proactive fix worked in BOTH the worker's run and the reviewer's own: zero `tests/ui_server/` stale-dist failures in either. G7 THE COMPARISON: branch-only 0 ids in both runs; base-only 1 id in the worker's run, 0 in the reviewer's — both outcomes are consistent with the flake attribution and neither shows a branch-vs-base regression coupled to F258's own code (`git diff --stat 18ae7129 176ec7fc -- tests/cli/test_review_bundle_runtime.py apps/cli/` independently re-confirmed EMPTY by the reviewer). No new finding is raised. G8 THE TREE: clean, single worktree, no `tmp/*` branch, per-commit insertions 175/137/14/2/593/(handoff) — the reviewer confirms C3's declared 593-insertion oversize exception is exact (1+104+0+305+92+91=593) and accepts it on the same grounds as the accepted F257 R6 precedent (`ddfc2dca`): the six evidence files are one indivisible measurement, and the reviewer independently verified their raw contents are genuine pytest output, not fabricated summaries. THE ROUND PASSES: the branch is pushed and matches `origin` exactly at `176ec7fc`, no throwaway worktree or branch survives, and the reviewer's own from-scratch re-execution of both suites corroborates every reading the worker reported. STATUS_closure_protocol.md precondition 2 ("Full relevant suite green... A dedicated integration-gate round... must have PASSed before closure") is now MET for F258. All three T-slices (T001, T002, T003) are built and independently verified (rounds 5, 6), and the integration gate is green (this round). The next round is the reviewer's own design of F258's closure sequence.
--- END RECORD8 ---
