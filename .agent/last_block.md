── STEP closure-precondition-1,3,5/2 — F258 ────────────────────────
Goal: Register the finding round 8's real self-use run surfaced, book
round 8's own PASS verdict, then re-confirm closure preconditions 1,
3 and 5 after those edits.

Bundle:
1. Register R-0757 (Medium) into `.agent/live_review.md`.
2. Book `Gate: F258 R8` (a second, separate append to the same file)
   into `.agent/live_review.md`.
3. Rewrite `.agent/plan.md` from PLAN9.
4. Re-run `remedy integrity check --json` (fallback
   `python3 -m apps.cli.main integrity check --json` if the bare
   binary is denied) AFTER the above edits and record the raw JSON.
5. Confirm `git status --porcelain` empty and the branch still
   matches `origin` after a `git fetch`.

Change set (exactly these paths, plus the handback commit):
- `.agent/authored/f258-r9.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/handoff.md`
No file under `packages/`, `apps/`, `tests/` or `docs/` changes this
round.

Constraints:
1. Never retype an authored slice — copy the bytes
   (`shutil.copyfile`), never hand-retype.
2. `.agent/plan.md` is a full rewrite from PLAN9 below, byte for byte.
3. `.agent/live_review.md` gets TWO appends this round, in order:
   FIRST FINDING_R0757 below (`base + b"\n" + FINDING_R0757`), THEN
   GATE_R8 below, appended to THAT result
   (`mid + b"\n" + GATE_R8`). Findings persist FIRST, per
   `planner_reviewer_prompt.md` §4 item 4 — this is why the finding is
   C2 and the verdict quoting it is C3, never the reverse.
4. Order: C0a (save block) → C0b (mirror) → C1 (plan.md, the FIRST
   substantive commit, per checklist item 23) → C2 (append
   FINDING_R0757) → C3 (append GATE_R8) → C4 (re-run the integrity
   check and record its raw JSON output to
   `.agent/gate_f258_closure/precondition_check_r9.txt`, which is
   IN the already-fixed change set as part of `.agent/**`) →
   handback commit.
5. Do NOT resolve, repair or touch R-0570, R-0736 or R-0757's code
   this round — only register/book text. No file under `packages/`
   changes.

Done when (exact verification commands, run by the WORKER before
handback and independently RE-RUN by the reviewer):
- G1 transport: `.agent/authored/f258-r9.md`, `.agent/last_block.md`
  and this file's own bytes are sha256-equal (digest stated below).
- G2 the plan: `.agent/plan.md` sha256-equals PLAN9 (digest below),
  1960 bytes, 43 lines, carries `## Goal` and `## Next Steps`, ends
  with exactly one `\n`.
- G3 the two record appends: measure `.agent/live_review.md`'s byte
  length immediately before C2 (`base0`, expected 1787894);
  `base0 + b"\n" + FINDING_R0757 == mid` (expected 1791942) must
  hold; then `mid + b"\n" + GATE_R8 == committed` (expected 1795167)
  must hold. The committed file's last `\n\n`-delimited unit must
  equal GATE_R8 exactly, and that same split's second-to-last unit,
  with ONE `\n` appended back (the split consumes FINDING_R0757's own
  trailing newline as half of the delimiter separating it from
  GATE_R8), must equal FINDING_R0757 exactly. TWO negative controls (a single byte
  flipped inside a COPY of each of FINDING_R0757 and GATE_R8, each in
  a disposable worktree, removed after): each flipped reconstruction
  must be REJECTED, each true one ACCEPTED.
- G4 the ledger: before C1, 317 distinct `^- R-\d+ — ` ids, 55
  distinct `^Done: R-\d+` ids, `DECISION F258` ids `['D1','D2']`,
  `Gate: F258 R` lines ending at `'F258 R7'`. After C2: 318 distinct
  `^- R-\d+ — ` ids (added exactly `R-0757`), everything else
  unchanged. After C3: 318 R-ids, 55 Done-ids, `DECISION F258`
  unchanged, `Gate: F258 R` lines ADDED exactly `'F258 R8'`.
- G5 precondition 3: the integrity check's JSON, run AFTER C3, shows
  `"passed": true`, `"fail_count": 0`, and its `high_blockers_open`
  check status `"pass"` — R-0757 being Medium must not trip it.
- G6 precondition 5: `git status --porcelain` empty at C4 and at the
  handback; `git fetch` then `git rev-parse HEAD
  origin/feature/f258-self-use-v2` equal, both before this round's own
  push and (separately, in the handback) after it.
- G7 precondition 1 (closure-scoped): recompute the set of F258-scoped
  open findings by grepping `.agent/live_review.md` for `R-0570`,
  `R-0736` and `R-0757` and confirming each is still OPEN (no `Done:`
  line for it) and each is Medium or Low — never Blocker or High.
- G8 the tree and canary: `git worktree list` shows only the primary
  checkout; `git branch --list 'tmp/*'` empty; every commit's
  insertions under 500; canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` REAL exit 0,
  42 passed.

Handback: completion report + rewrite `.agent/handoff.md`. Session
header exactly `SESSION 3 of feature F258 · round 9`.
──────────────────────────────────────────────────────────────

--- BEGIN PLAN9 sha256=6a2d11e62d9285043c4c601f935b97fef34d53f318dc62117d9797b31265a174 bytes=1960 lines=43 ---
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 9.

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
| T001/T002/T003 | done | rounds 2-6 |
| integration-gate round | done | round 7 |
| precondition 6 — plan + run for real | done | round 8 |
| preconditions 1, 3, 5 | open | this round |
| precondition 4 — Built State section | open | next round |
| evidence job + review zip | open | next round |
| STATUS + README + final PR | open | final round |

## Next Steps
1. Register R-0757 (Medium — self-use runner silently resolves a fake
   provider by default) in `.agent/live_review.md`, own commit, before
   any verdict text — the finding round 8's real run surfaced.
2. Book round 8's own verdict (`Gate: F258 R8`) into the same file, per
   amend0827 rule 1.
3. Re-confirm preconditions 3 and 5 after this round's own edits
   (integrity check, tree/push state); precondition 1's closure-scoped
   reading: every F258-scoped open finding is Medium/Low (R-0570,
   R-0736, R-0757) — none Blocker/High.
4. Precondition 4, the evidence job, the review zip and the final
   STATUS/README/PR commit are the next rounds, not this one.

## Risks
- R-0570 (Low), R-0736 (Medium): OPEN, unrelated to F258's own code.
- R-0757 (Medium): OPEN, this branch's own defect, documented under
  this closure's PASS WITH RISKS reading, not fixed here.
- No closure candidate is open; `.agent/candidates.md` stays empty.
--- END PLAN9 ---

--- BEGIN FINDING_R0757 sha256=0f23574b5d676fb03e04a070906485c64b37a617947737da4c5b0434248cfb08 bytes=4047 ---
- R-0757 — Medium, THE SELF-USE RUNNER'S UNFLAGGED CALL SILENTLY RUNS UNDER A FAKE PROVIDER, NOT THE PRODUCT'S REAL DEFAULT, CONTRADICTING ITS OWN DOCSTRING'S PROMISE. THE MEASUREMENT, taken at `ab622afd` by running the shipped function for real (F258 round 8's own precondition-6 discharge): calling `packages.orchestration.self_use_runner.run_next_self_use_item` with no `builder_provider`/`reviewer_provider`/`builder_name`/`reviewer_name` override, exactly as `docs/roadmap/features/T5_F258.md` T002 and `STATUS_closure_protocol.md` precondition 6 both describe the mechanism, against the REAL shipped queue produced job `8c90a6d1ba5b4d6c` with `execution_config` recording `builder='fake' (source='default')`, `reviewer='fake' (source='default')`, and `budget_actuals.provider_call_count == 0` — zero real provider calls were made, verified in `.agent/gate_f258_closure/self_use_run.txt` and independently reproduced by the reviewer reloading the same job id. `packages/orchestration/pingpong_job.py:1740-1743` resolves `builder_name`/`reviewer_name` via `_resolve_cfg(explicit, persisted, "fake")` and `packages/orchestration/pingpong_loop.py:2569-2570`'s own `run_pingpong(..., builder_name: str = "fake", reviewer_name: str = "fake", ...)` confirms `"fake"` is the shipped default at this layer; `FakeProvider` (`packages/orchestration/pingpong_provider.py:159`) is documented as a "Deterministic fake provider for automated testing" that fabricates canned output (`files_changed=['docs/README.md']` by default) rather than doing real work. `packages/orchestration/role_config.py:32`'s `DEFAULT_PROVIDER = "ollama"` is wired into an unflagged job only via `apps/cli/commands/do_cmd.py` — grepped and confirmed absent from `self_use_runner.py`, `self_use_job.py` and `pingpong_job.py`'s own module scope — so `remedy do job-run` resolves a real local provider by default while `self_use_runner.run_next_self_use_item`'s direct call into `run_job()` does not: the two "unflagged" paths this repository ships do not resolve to the same default, contradicting `self_use_runner.py`'s own docstring claim that "a real self-use run resolves the same product default any other unflagged job resolves." WHY MEDIUM: no data is corrupted and no security boundary is crossed — the isolated worktree, the approval gate and the JobPlan bookkeeping all execute genuinely, so the defect is confined to WHICH provider fires, not whether the machinery around it works — but it is silent and load-bearing: `job.status == 'completed'` and every gate this round ran read as a clean pass, with nothing on disk or in the JobPlan flagging that no real attempt was made at the task, which is the same "false live indicator" shape this repository's own review culture treats seriously elsewhere. Every future automatic self-use consumption that does not explicitly thread a real provider through — which is every invocation the feature's own documentation describes — will silently repeat this: a synthetic, no-op "success" standing in for genuine maintenance work, defeating T5_F258's own stated purpose ("Remedy is used on Remedy... zero operator input") for the one call path this feature ships. THE FIX is to have `run_next_self_use_item` resolve real builder/reviewer configuration via `packages.orchestration.role_config.resolve_role_config` for the `builder`/`reviewer` roles — mirroring what `apps/cli/commands/do_cmd.py` already does — before calling `run_job`, so an unflagged self-use run genuinely resolves `role_config.DEFAULT_PROVIDER` (`"ollama"`) rather than `run_job`'s own raw `"fake"` fallback; or, if a synthetic default is intentional for self-use specifically (e.g. to avoid unattended cost), correct `self_use_runner.py`'s own docstring to state the TRUE default plainly rather than claim parity with "any other unflagged job." Resolved when `run_next_self_use_item`, called with no provider override, either resolves a real, non-`FakeProvider` builder/reviewer by default, or its docstring no longer claims that it does.
--- END FINDING_R0757 ---

--- BEGIN GATE_R8 sha256=1061a15af9c76ddf5ed02a53ccbe2b8bf8e36a694f20a87fba02f7dff6e4afda bytes=3224 ---
Gate: F258 R8 — STATUS_CLOSURE_PROTOCOL.MD PRECONDITION 6, DISCHARGED FOR REAL: SU-002 PLANNED AND RUN THROUGH THE ACTUAL JOB PATH, REACHING THE NORMAL APPROVAL GATE. VERDICT PASS. The reviewer re-ran every gate independently against the real diff `69bc74d0..ab622afd`, not against the worker's own report. G1 TRANSPORT: the block, `.agent/authored/f258-r8.md` and `.agent/last_block.md` all sha256 `bd79dc5af5107faea994a30adc25300dcf14902a358e6737ebecb0a6dbac9ce4`, 14450 bytes — equal to the reviewer's own pre-verified scratch original at `.remedy-wt/f258-r8/block.md`. G2 THE PLAN: `.agent/plan.md` sha256 `a9c4cec349ad58183a4ca956de12caded2509140c983a70049dfac818ceac73f`, 1978 bytes, 41 lines, `## Goal`/`## Next Steps` present, ends `\n`. G3 THE RECORD APPEND: base 1783003 bytes ending in one `\n`; `base + b"\n" + RECORD8 (4890 bytes) == committed (1787894 bytes)` True; the last `\n\n`-delimited unit equals RECORD8 exactly; a negative control (byte flip at index 100, in a disposable worktree, removed after) was correctly rejected while the true original was accepted. G4 THE LEDGER: `DECISION F258` unchanged at `['D1','D2']`; `Gate: F258 R` lines ADDED exactly `['F258 R7']`; 317 distinct `R-` ids and 55 distinct `Done:` ids unchanged before and after C2. G5/G6 THE SELF-USE RUN: the reviewer independently reloaded job `8c90a6d1ba5b4d6c` via `packages.orchestration.pingpong_job.load_job_plan` under the SAME isolated `REMEDY_DATA_DIR` (`.remedy-wt/f258-r8-selfuse/data`) and reproduced `status='completed'`, `error=''`, `isolation_mode='worktree'`, one task `T001` at `final_status='staged_review_passed'`, `reviewer_verdict='pass'`, matching `.agent/gate_f258_closure/self_use_run.txt` exactly; independently re-calling `describe_self_use_run_defects` on the same reloaded `JobPlan` reproduced the empty tuple `self_use_defects.txt` records. STATUS_closure_protocol.md precondition 6 is MET: SU-002 was planned via `self_use_job.plan_next_self_use_item` and RUN via `self_use_runner.run_next_self_use_item` to the normal approval gate, never promoted, and the empty defects tuple means nothing from `describe_self_use_run_defects` needed registering — but the reviewer's OWN reading of the real evidence surfaced a SEPARATE defect the module itself does not detect, registered as R-0757 (Medium) above this entry: the unflagged call silently resolved to `FakeProvider` rather than a real product default, zero real provider calls made. G7 THE QUEUE: `scripts/self_use_queue.json` byte-identical across the round's whole range (`git diff --stat 69bc74d0..ab622afd -- scripts/self_use_queue.json` empty); `consumed_by` fields untouched, correctly deferred to the final closure commit. G8 THE TREE AND CANARY: `git status --porcelain` empty, single worktree, no `tmp/*` branch, per-commit insertions 170/165/15/2/35/193 from `git show --numstat` against each commit's own parent, every one under 500; canary REAL exit 0, 42 passed, matching baseline. THE ROUND PASSES: the branch is pushed and matches `origin` exactly at `ab622afd`. R-0757 is Medium and does not block F258's closure verdict, which may proceed as PASS WITH RISKS once the remaining closure preconditions (1, 3, 4, 5) are also checked.
--- END GATE_R8 ---
