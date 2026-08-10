── STEP R37 — F105 ───────────────────────────
Goal:        Record the R36 reviewer gate, resolve R-0259 and R-0260 with
             reviewer-authored `Done:` text, and register plus fix R-0261 —
             the character distance both guard comments attach to the wrong
             anchor.
Bundle:      C1 save this block · C2 every `.agent/live_review.md` edit, the
             findings-first commit · C3 the two comment corrections ·
             C4 plan and handoff.
Change:      `.agent/authored/f105-r37-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
             `tests/orchestration/test_mission_compiler.py`,
             `tests/orchestration/test_orchestrator_loop.py`. Nothing else.
             No production code: the two test edits change COMMENT and
             DOCSTRING TEXT only — no executable line moves, no constant
             changes.
Constraints: Do not touch `packages/`, `apps/`, `docs/` or `tests/` beyond the
             two named test files. Do not change the number 200, the
             `source.index(...)` anchors, or any `assert` in either test.
             Do not reflow any line you were not given a pair for. Do not
             touch the `Landed:`/`Done:` pair on the R-0257 block: it is
             historical, its `Done:` sits directly beneath it, and editing it
             is outside this change set.
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp /home/decodeux/Repos/remedy/.remedy-wt/f105-r37-1.block.md`
      `.agent/authored/f105-r37-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  `sha256sum` all three plus `cmp`; digest in the handback.

C2 — every `.agent/live_review.md` edit, ONE commit, findings first
  Apply PAIR_V, PAIR_W, PAIR_X, PAIR_Y and PAIR_Z to `.agent/live_review.md`.
  Declared shapes, to be MEASURED not assumed:
    PAIR_V REWRITE — the header's next-free-ID line.
    PAIR_W REWRITE — R-0259's `Landed:` line becomes the reviewer's `Done:`
      text. §4.4 of docs/agents/planner_reviewer_prompt.md says the `Done:`
      text REPLACES the `Landed:` line, so the line does not survive.
    PAIR_X REWRITE — the same for R-0260.
    PAIR_Y CONTAINS-FROM — registers R-0261 at the END of `## Findings`.
    PAIR_Z CONTAINS-FROM — the R36 step line and the R36 gate record at the
      END of the file, under `## Steps`.
  All five share ONE path in ONE commit, so reconcile them TOGETHER against
  `git show --numstat` for that commit: every added line comes from a TO, and
  every removed line is a FROM.

C3 — the two comment corrections, ONE commit, comment text only
  Apply PAIR_F2 to `tests/orchestration/test_mission_compiler.py` and PAIR_G2
  to `tests/orchestration/test_orchestrator_loop.py`. Both REWRITEs.
  Every added and removed line in this commit is a `#` comment line or a line
  of docstring prose. If any line you are about to write is not, STOP and
  declare it instead of applying it.

C4 — plan and handoff, ONE commit
  Apply PAIR_P to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md` in your own words per AGENTS.md.

<<<PAIR_V_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0261.
<<<END_PAIR_V_FROM>>>

<<<PAIR_V_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0262.
<<<END_PAIR_V_TO>>>

<<<PAIR_W_FROM>>>
  Landed: R-0259 — the R-0257 block moved to the end of Findings, C2 of R36.
<<<END_PAIR_W_FROM>>>

<<<PAIR_W_TO>>>
  Done: R-0259 (2026-08-10) — RESOLVED at F105 R36, commit 78891cd7. The
  27-line R-0257 block now sits at the END of `## Findings`, so the R30 gate
  record closes with its own ``LAST_REVIEWED_SHA` advances 0c8932e3 ->
  0ba30611.` line and no reader can attribute that advance to R-0257's
  resolution text. Proved a MOVE and not a retype by the strongest measure
  available, re-run by this reviewer rather than read from the handback: the
  SORTED file digest is
  `9412ed6e2ad347f614e0024a29dc15d9123a6494ce0b1446ca669765060ab920`
  both before and after the commit, so the line multiset is
  identical and nothing was added, dropped or reflowed — only reordered. The
  block occurs exactly 1x before and 1x after, and the commit's numstat is
  `27 27`, one file.
<<<END_PAIR_W_TO>>>

<<<PAIR_X_FROM>>>
  Landed: R-0260 — both guard comments now describe the real window, C4 of R36.
<<<END_PAIR_X_FROM>>>

<<<PAIR_X_TO>>>
  Done: R-0260 (2026-08-10) — RESOLVED at F105 R36, commit a9408174. Both
  comments now state the window the code actually takes: 200 characters from
  the call's start, which is the call plus 71 characters at the plan site and
  the call plus 27 at the run site. Re-measured by this reviewer against
  `apps/cli/commands/mission_cmd.py` at 25e6326a rather than taken from the
  handback: the plan call spans 129 characters from `outcome = plan_mission(`
  and the run call 173 from `result = run_mission(`, so 200 leaves exactly 71
  and 27 characters of overshoot, and each label still falls inside its own
  window. The constant 200 was deliberately not retuned, which was the right
  call: the guarded property was already proved by the R34 mutations, and this
  finding was about a comment that promised more than the code checked.
  The residual imprecision the repair itself introduced is registered
  separately as R-0261 and does not reopen this one.
<<<END_PAIR_X_TO>>>

<<<PAIR_Y_FROM>>>
  the regression cannot return silently the way it arrived.
<<<END_PAIR_Y_FROM>>>

<<<PAIR_Y_TO>>>
  the regression cannot return silently the way it arrived.

- R-0261 (Low, F105 R36, reviewer-authored defect): both repaired guard
  comments attach a real number to the wrong anchor. The compiler comment says
  "the run site's label sits 7335 characters away" and the loop docstring says
  "It stays 7335 characters clear of the plan call's label", but 7335 is the
  distance between the two CALL STARTS, not between a window and a label.
  Measured by the reviewer against `apps/cli/commands/mission_cmd.py` at
  25e6326a: `outcome = plan_mission(` starts at 6911 and `result = run_mission(`
  at 14246, a gap of exactly 7335; the run site's LABEL starts at 14396, which
  is 7485 characters from the plan call's start and 7285 past the end of its
  200-character window, while the run window starts 7229 characters after the
  plan label. R-0260's own text used 7335 correctly — "the call sites are 7335
  characters apart" — and the repair re-attributed it to labels. No test is
  wrong and every margin is over 7000 against a 200-character window, so the
  guarded property is untouched; this is a third consecutive round spent on the
  prose of the same two comments. Fix: DELETE the character figure from both
  comments rather than correct it. A cross-site distance is a fact about
  `mission_cmd.py` that no assertion pins, so it goes stale on the next edit to
  that file and buys nothing the phrase "far outside this window" does not
  already say. The per-site overshoots — 71 and 27 — stay: those describe each
  guard's OWN window against its OWN call, which is what R-0260 asked for and
  what a reader of that line needs. OPEN.
<<<END_PAIR_Y_TO>>>

<<<PAIR_Z_FROM>>>
  `LAST_REVIEWED_SHA` advances 28fe51c3 -> bcfb12e3.
<<<END_PAIR_Z_FROM>>>

<<<PAIR_Z_TO>>>
  `LAST_REVIEWED_SHA` advances 28fe51c3 -> bcfb12e3.
- R36: housekeeping round — MOVE the misfiled R-0257 block (R-0259), make both
  guard-window comments state the real window (R-0260), record the R35 gate.
  No production code.
- Reviewer gate on R36 (2026-08-10): PASS, by the reviewer of the FOLLOWING
  session — the third session of this branch. R36 was the last round of a
  SESSION, not of the branch, so §4.13's terminator clause does not apply and
  it does get an on-disk entry; its handoff correctly named this gate as the
  next action instead of claiming a verdict on itself.
  Range `bcfb12e3..25e6326a` = six commits, seven paths. `git diff --stat`
  lists exactly the seven the block named — five under `.agent/` and the two
  named test files — nothing under `packages/`, `apps/`, `docs/` or the rest
  of `tests/`. Insertions per commit 263, 210, 27, 40, 11 and 58, each far
  under 500; the 210/189 one is the single-state-file verbatim rewrite
  AGENTS.md exempts from the churn reading anyway.
  Transport by the §4.9 DIGEST FALLBACK, stated as such because the primary
  proof was unavailable: the R36 session's scratchpad original
  `.remedy-wt/f105-r36-1.block.md` no longer exists on disk, so no
  cmp-against-original was possible at this gate. Both COMMITTED copies —
  `.agent/authored/f105-r36-1.md` and `.agent/last_block.md` — were re-hashed
  by this reviewer at
  `21faa61ece190293dcacc2509581b5f9bd4cace5e382c4a699e5aab183f5f3c8`,
  `cmp` silent between them, 263 lines against DECISION F105 D5's
  cap of 400, and that digest equals the one the R36 handback recorded.
  All four pairs re-sliced from the COMMITTED authored file by this reviewer's
  own whole-line marker reader, never retyped: declared shape equals measured
  shape for every one. PAIR_S is CONTAINS-FROM at FROM 1x / TO 1x; PAIR_F and
  PAIR_G are REWRITEs at FROM 0x / TO 1x; PAIR_P is byte-equal to the applied
  `.agent/plan.md` at 41 lines against the cap of 50. C2's order-only claim is
  proved independently by the sorted-file digest, recorded in R-0259's `Done:`
  text above.
  Gates re-run by THIS reviewer with real exit codes, none taken from the
  handback: `tests/docs/` `294 passed in 0.30s`; the dashboard contract
  `70 passed in 4.31s`; the scoped pair `tests/orchestration/
  test_mission_compiler.py` plus `test_orchestrator_loop.py` `317 passed in
  1.43s`; the canary `42 passed in 19.47s`; zero `^<<<` marker lines in all
  five written targets; `git status --porcelain` empty and `git worktree list`
  the primary alone at this verdict.
  No red-proof was ordered or run, and that is correct rather than an omission:
  every added and removed line of a9408174 is a `#` comment or docstring prose,
  checked line by line over `git show -U0`, so the round changed nothing
  executable and there is no branch to mutate (D8 checklist item 5, DECISION
  F105 D10).
  The arithmetic the two comments now assert was re-derived independently, not
  accepted: the plan call spans 129 characters and the run call 173, so a
  200-character window overshoots by 71 and 27 respectively, and both labels
  fall inside their own windows. Those figures are right. The cross-site figure
  is not, and is registered as R-0261 — a Low prose defect that changes no
  assertion, so it does not turn this verdict.
  Noted so a later round does not re-derive it: the R-0257 block carries BOTH a
  `Landed:` and a `Done:` line. That is historical, the `Done:` sits directly
  beneath it, and it is deliberately NOT a finding — from R-0259 and R-0260
  onward the `Done:` text replaces the `Landed:` line as §4.4 prescribes.
  `LAST_REVIEWED_SHA` advances bcfb12e3 -> 25e6326a.
<<<END_PAIR_Z_TO>>>

<<<PAIR_F2_FROM>>>
        # exactly (R-0260). That is enough for the job the guard has: the run
        # site's label sits 7335 characters away, far outside this window, so a
        # label that drifts to that call no longer satisfies this one.
<<<END_PAIR_F2_FROM>>>

<<<PAIR_F2_TO>>>
        # exactly (R-0260). That is enough for the job the guard has: the run
        # site's label lies far outside this window, so a label that drifts to
        # that call no longer satisfies this one. No character distance is
        # quoted here on purpose (R-0261): the gap between the two call sites
        # is a fact about mission_cmd.py that no assertion pins, so a number
        # here would go stale on the next edit to that file.
<<<END_PAIR_F2_TO>>>

<<<PAIR_G2_FROM>>>
        exactly (R-0260). It stays 7335 characters clear of the plan call's
        label, which is the property this guard exists to hold.
<<<END_PAIR_G2_FROM>>>

<<<PAIR_G2_TO>>>
        exactly (R-0260). It stays clear of the plan call's label by thousands
        of characters, which is the property this guard exists to hold. The
        exact gap is deliberately not quoted (R-0261): no assertion pins it,
        so a number here would go stale on the next edit to mission_cmd.py.
<<<END_PAIR_G2_TO>>>

<<<PAIR_P_PLAN>>>
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003's six migration sites are all migrated.
R36 is GATED; `LAST_REVIEWED_SHA` is 25e6326a. Call evidence reaches four
prompts: both `do_cmd` flight-plan sites, `remedy mission plan`, and the
orchestrator loop, whose sink lives inside `run_mission` so both callers inherit
it (DECISION D11). `remedy mission run` names its provider; the gauntlet's stays
unlabelled on purpose (DECISION D13).
R37 is the state round: it records the R36 gate, resolves R-0259 and R-0260
with reviewer-authored `Done:` text, and registers plus fixes R-0261 — the
cross-site character distance both guard comments attach to the wrong anchor.
No production code.
Open findings: R-0221, R-0239, R-0247, R-0256 — plus R-0261, whose fix lands
this round and awaits the reviewer's `Done:`.
No PR; one is created at CLOSURE.

## Next Steps
- R-0256 (compose once, not twice) needs a signature change on `plan_job_llm`
  and `run_intake`, so it is its own round — R38, the next one.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_P_PLAN>>>

GATES — run every one, record the REAL exit code in the handback

A transport
  `sha256sum .remedy-wt/f105-r37-1.block.md .agent/authored/f105-r37-1.md
  .agent/last_block.md` — all three EQUAL; `cmp` the authored file against the
  scratch original and against `last_block.md`, both silent. This is the
  PRIMARY proof shape, not the digest fallback: the original exists.

B size
  `wc -l .agent/authored/f105-r37-1.md` — report it against the cap of 400
  (DECISION F105 D5).

C pair shapes, MEASURED not assumed
  Slice every pair from the COMMITTED `.agent/authored/f105-r37-1.md` with a
  whole-line marker reader. Never retype a slice. PAIR_Y's TO opens with its
  FROM line followed by a BLANK line; PAIR_Z's TO opens with its FROM line and
  continues directly. Both are therefore literally CONTAINS-FROM — write each
  TO exactly as sliced, blank line included, and add nothing.
  For each pair print declared vs measured and the counts:
    PAIR_V, PAIR_W, PAIR_X, PAIR_F2, PAIR_G2 REWRITE: FROM 0x and TO 1x in the
      target after the write.
    PAIR_Y and PAIR_Z CONTAINS-FROM: FROM exactly 1x after the write.
    PAIR_P: `cmp` the applied `.agent/plan.md` against the sliced text; `wc -l`
      against the cap of 50.
  A declared shape that does not equal the measured shape is a STOP: report it,
  do not apply it.

D added-line reconciliation for C2
  The five live_review pairs share one path in one commit. Take
  `git show -U0 <C2> -- .agent/live_review.md`: every ADDED line must appear in
  some TO, and every REMOVED line must be a FROM. Report the two stray counts;
  both must be 0.

E marker leakage
  In all five written targets — `.agent/live_review.md`, `.agent/plan.md`,
  `.agent/handoff.md` and the two test files — the count of lines beginning
  `<<<` must be 0. Report the number, not the word.

F state-file contracts
  `python3 -m pytest tests/docs/ -q` and
  `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.
  `.agent/plan.md` must keep `## Goal` and a `Steps` substring;
  `.agent/live_review.md` must keep its `## Steps` heading.

G scoped
  `python3 -m pytest tests/orchestration/test_mission_compiler.py
  tests/orchestration/test_orchestrator_loop.py -q` — both guard tests still
  pass, unchanged in behaviour.

H the number is gone
  `grep -c 7335 tests/orchestration/test_mission_compiler.py
  tests/orchestration/test_orchestrator_loop.py` — 0 in BOTH. Scoped to the two
  test files on purpose: `.agent/live_review.md` records the number in R-0261's
  own text and must keep it.

I comments only
  Over `git show -U0 <C3>`, every added and removed line is a `#` comment line
  or docstring prose. Print the added and removed lines that are NOT — the list
  must be EMPTY. No mutation red-proof is ordered for this round and none is to
  be run: nothing executable changes (D8 item 5, DECISION F105 D10).

J canary
  `python3 -m pytest tests/cli/test_golden_path.py -q`.

K hygiene
  `git status --porcelain` empty at handback; `git worktree list` shows the
  primary alone; per-commit insertions each under 500 via `git show --numstat`.

Handback: completion report + rewrite `.agent/handoff.md` (changed-files table,
item-status table for C1a/C1b/C2/C3/C4, the real gate table with exit codes,
the transport and pair proofs, open-findings count, next expected action).
Then `git push`. No PR — one is created at CLOSURE.
──────────────────────────────────────────────────────────────
