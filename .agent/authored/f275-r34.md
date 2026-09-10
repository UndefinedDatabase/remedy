── STEP T003 (3 of n) — F275 ─────────────────────────────────
Goal:        Complete the inheritance DECISION F275 D18 opened — `job.resume`
             gains `--unattended`, `--yes` and `is_expensive` — and then retire
             the `job.run` command surface entirely.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 33
             verdict and two prose slips · C3 DECISION F275 D19 · C4 the
             inheritance and the retirement · C5 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r34.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `.agent/decisions.md`,
             `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
             `apps/cli/commands/decision.py`, `apps/cli/commands/loop_cmd.py`,
             `packages/orchestration/config.py`,
             `packages/orchestration/orchestrator_loop.py`,
             `docs/README.md`, `docs/guides/cost-preview-user-guide-v0.md`,
             `docs/system/remedy-toml-configuration-system-v0.md`,
             `tests/cli/test_cost_preview.py`, `tests/cli/test_loop_cmd.py`,
             `tests/orchestration/test_escalation.py`,
             `tests/orchestration/test_long_run_executor.py`,
             `tests/orchestration/test_resume_cli.py`,
             `tests/test_command_catalog.py`,
             plus `.agent/handoff.md` at C5.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

## Base

This round's base is `bc77c7ac`. THE WHOLE C4 CHANGE WAS APPLIED AND RUN by the
reviewer in a disposable worktree at that base before this block was written,
and the full serial suite over it read `18339 passed, 23 skipped` at exit 0 —
identical to the base. Every numeral below is that run's.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Never reflow, retype, trim or repair a
   slice. If a slice does not fit its target, DECLARE it and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, exactly. C1 is the first
   substantive commit, per §3 item 23.
3. THE CHANGE SET IS THE PATH LIST IN THE HEADER'S `Change:` LINE, together with
   `.agent/handoff.md`, which that line names separately as C5's own target.
4. EVERY APPEND IS `pre + ONE newline + slice`. At the base
   `.agent/live_review.md` is 808624 bytes, `.agent/prose_slips.md` is 221335
   and `.agent/decisions.md` is 1033519, each ending in a single `\n`.
5. NO PRODUCTION LINE MOVES BEFORE C4.
6. DESTRUCTIVE VERIFICATION IS ISOLATED, inside a disposable `git worktree`
   under `.remedy-wt/`, never in the primary checkout. Remove and prune it
   before the handback.
7. THE SUITE RUNS SERIALLY AND ONLY AFTER C4 IS COMMITTED, per the reason round
   32 measured and round 33 restated. Link `apps/ui/node_modules` into any fresh
   worktree first, and never `git add` that symlink — it is not in the change
   set. Stage by naming paths, never with `git add -A`.
8. NEVER REPLACE THE BARE SUBSTRING `job.run`. THIS IS THE MOST IMPORTANT
   CONSTRAINT IN THIS BLOCK AND THE REVIEWER LEARNED IT BY DOING IT. The catalog
   id `job.run` is a PREFIX of real attribute names on the `Job` object —
   `job.run_refs`, `job.run_id`, `job.run_manifest_path`,
   `job.run_manifest_error`, `job.run_manifest_episodes` and more. Measured at
   `bc77c7ac` over the trees SPEC-INHERIT (3) names: the BARE substring
   `job.run`, excluding only `job.run-`, matches 60 lines in 13 files, and 34
   of those lines in 6 files are ATTRIBUTE ACCESS that a blind replace would
   corrupt — in `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/self_use_runner.py`,
   `tests/cli/test_job_rerun_manifest.py`,
   `tests/orchestration/test_job_run_refs.py`,
   `tests/orchestration/test_legacy_manifest_presence.py` and
   `tests/orchestration/test_run_manifest_recovery.py`. The reviewer did exactly
   that in its own worktree and had to revert it. Use the TOKEN-SAFE regular
   expression instead:

       (?<![\w.])job\.run(?![\w-])

   The trailing `(?!...)` excludes `job.run-next` and every identifier
   continuation; the leading `(?<!...)` excludes an attribute access on any
   object. At `bc77c7ac` it matches 26 lines in 7 files, and NONE of them is an
   attribute access. Report the count your run produced.
9. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. The open set is 87 by
   distinct id at the base and must read 87 at C4. The next free id is R-0875
   and this round does not spend it. DECISION F275 D19 explains why no finding
   is owed for the two surfaces DECISION F275 D18 expected to lose.
10. PAIR SHAPES, from the containment test the reviewer ran at `bc77c7ac`:
    E1 `TO contains FROM: false` → REWRITE. E2 `TO contains FROM: false` →
    REWRITE. E3 `TO contains FROM: false` → REWRITE. Each carries the §4.9
    FROM-0x / TO-1x obligation.
11. THE `ruff` READING IS A CEILING, NOT A ZERO. The reviewer ordered "ruff
    clean" last round and it was RED at the base for reasons this feature did
    not cause: `tests/cli/test_plan_approval.py` and
    `tests/orchestration/test_long_run_executor.py` carry 8 pre-existing F401
    and I001 findings, and the repository as a whole sits at 26, which is
    exactly the frozen ceiling
    `tests/orchestration/test_ci_budgets.py::test_this_repository_really_is_at_or_below_the_lint_ceiling`
    pins. Do NOT fix them; that is an unrelated edit. The gate is the CEILING
    test, and G8 orders it by name. Report the repo-wide `ruff check .` count
    beside it.

## SLICE PLAN34 → whole-file replacement of `.agent/plan.md`

<<<PLAN34
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE.

## Current Step

ROUND 34 finishes the classic runner's COMMAND SURFACE. DECISION F275 D19 amends D18: the
`--unattended` and `--yes` flags are INHERITED by `job.resume` rather than lost, because
losing them would delete F114's cost-preview contract along with them. So `job.resume` gains
both flags and the `is_expensive` mark, and the `job.run` entry, its dispatch line and all
its advertisements are then retired. The handler `_cmd_job_run_cycles` survives as the
internal execution path behind the one remaining door.

## Next Steps

1. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — together with the
   classic store, which is the same commit range by that decision's own terms.
3. DECISION F260 D3, the deletion paragraph naming every deleted module and the feature that
   inherited its idea, which T001 still owes.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- A catalog id that is a PREFIX of a model attribute cannot be migrated by substring. Round
  34 proved this on `job.run` against `job.run_refs` and `job.run_manifest_*`; the token-safe
  regex is recorded in that round's block and in `.agent/prose_slips.md`.
- The open set is 87 by distinct id at this round's base `bc77c7ac`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
PLAN34

## SLICE RECORD34 → append to `.agent/live_review.md`

<<<RECORD34
Gate: F275 R33 — the F275 round 33 entry. VERDICT PASS, written by the planner and reviewer of session 16 after reading the committed range `7d14e89f`..`bc77c7ac` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits C0a `5d8d4170`, C0b `e2d52ffd`, C1 `7bd2da3f`, C2 `750eb7e8`, C3 `7e61da07`, C4 `45ed2c8c` and C5 `bc77c7ac`, per-commit insertions 313, 259, 18, 10, 7 and 34 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's scratch original at `.remedy-wt/f275-r33-block.md` was written AND HASHED BEFORE delegation at `a1f8eab17d2e94432732ebfac36a9a8666607035f81c8b2ea860be6d2ba66558`, and both committed copies are 28569 bytes at that digest as ONE shared git blob; the chain covers those three artefacts and claims nothing about bytes emitted into a prompt, per §3 item 37. G2: `.agent/plan.md` byte-identical to PLAN33 at 2270 bytes, 41 lines against the cap of 50, both mandated headings exactly once. G3 IS THE INTERESTING ONE THIS ROUND BECAUSE `.agent/live_review.md` TOOK TWO APPENDS IN TWO DIFFERENT COMMITS: RECORD33 at C2 took it 799726 to 806703 and DONE33 at C3 took it 806703 to 808624, while SLIPS33 took `.agent/prose_slips.md` 219069 to 221335; each post-blob equals its own pre-blob then ONE newline then the slice as extracted, the joining byte READ BACK at offset len(pre) reads a newline in all three, and the structural reader counted N from each slice — 2, 3 and 1 paragraphs — and matched the last N blank-line units IN ORDER, with every negative control flipped INSIDE THE FIRST appended paragraph and REJECTED by BOTH readers. `^Gate: F275 R32 `, `^- R-0874 — ` and `^Done: R-0874 — ` each exactly 1 at C3. G4: THE OPEN SET READS 87 AT THE BASE, 88 AT C2 AND 87 AT C3, which is the correct trace for a round that registers one finding and resolves it in the same round; the registered and resolved lists each hold exactly `R-0874`. G5: pairs A1 and A2 each FROM 1 to 0 and TO 0 to 1. The worker declared that the phrase `execution loop` rises from 3 to 4 in that section rather than falling, and the declaration is CORRECT AND THE RIGHT READING: the extra occurrences are the authored TO texts themselves, which name the loop only to record that it is gone, and the one occurrence that asserted a LIVE loop is the one that disappeared. A repair that documents a deletion will mention the deleted thing more often than the text it replaced, and a gate that counted the noun rather than the claim would have failed a correct fix. G6: over `apps/ packages/ tests/ scripts/` the token `remedy job run-next` falls 21 lines in 11 files to ZERO, the bare `job run-next` 29 lines in 15 files to ZERO, and the dotted `job.run-next` 5 lines in 3 files to ZERO — the BEFORE readings taken as well as the after, because an absence proves nothing without them. THE HANDLER SURVIVED, WHICH IS THE PROPERTY THIS ROUND EXISTED TO PRESERVE: parsing `apps/cli/commands/job.py` with `ast` at C4 shows `_cmd_run_next_task_local` still defined and its sole caller printed as `_cmd_job_run_cycles`, so `job.resume` still reaches the single pass under the shipped default, exactly as DECISION F275 D18 rules. The catalog, read by IMPORT rather than through the denied `remedy` binary, holds 221 commands in 44 groups with ZERO dangling `related=` references. G7 IS THE GATE THIS ROUND WAS BUILT AROUND AND IT CAUGHT WHAT NO TEXT SWEEP COULD: an `ast` sweep for the adjacent string pair `("job", "run-next")` read TWO sites at the base — `tests/cli/test_plan_approval.py` lines 372 and 716, both `subprocess.run([*_CLI, "job", "run-next", short_id])` — and EMPTY after C4, with the 65-pair total unchanged as a control. Neither site contains the substring `remedy job run-next` or even `job run-next`, so both were invisible to every text instrument this repository has used for a command deletion, and the reviewer found them only by APPLYING the change in a worktree and running the full suite, which went red at 2 failed. The migrated tests then passed UNEDITED in their assertions: `remedy job resume` reaches the same plan-approval gate and exits 3 with the same two stderr strings, which is the strongest evidence yet that DECISION F275 D18's inheritance ruling is behaviourally true and not merely nominal. The full serial suite at C4 reads `18339 passed, 23 skipped` at exit 0, identical to the base, and the reviewer re-ran the canary and the catalog guards itself at 73 passed. G8: porcelain EMPTY, ONE worktree, `.agent/STOP` absent, and `7d14e89f..45ed2c8c` an EXACT set match over the 25 change-set paths with MISSING and EXTRA both empty. THE ONE DEVIATION IS A REVIEWER ERROR AND IT IS SUSTAINED IN THE WORKER'S FAVOUR: G8 ordered `ruff check` over every `.py` path in the change set, and it exits 123 with 8 findings — but the reviewer re-measured the SAME two files at the base `7d14e89f` in a disposable worktree and read the SAME 8 findings, same codes, same lines, so this round introduced none. The block should have ordered the repository's own invariant instead, which is a CEILING and not a zero: `ruff check .` reads 26 repo-wide and `tests/orchestration/test_ci_budgets.py` passes at 10, so the lint contract is MET. The worker was right to refuse to "fix" pre-existing findings on lines this round has no business touching. NO FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.
RECORD34

## SLICE SLIPS34 → append to `.agent/prose_slips.md`

<<<SLIPS34
2026-09-10 · F275 R33 · The round 33 block's G8 ordered `ruff check` over every `.py` path in the change set and treated its output as a pass/fail gate, without running it at the base first. It was RED at the base for the same 8 pre-existing F401 and I001 findings, in the same two files and on the same lines, so the gate could not distinguish a round that introduced lint debt from one that did not. This repository does not hold `ruff` at zero: it holds it at a frozen CEILING of 26, pinned by `tests/orchestration/test_ci_budgets.py`, and that test is the gate. A gate over a tool the repository already runs must be ordered in the same shape the repository's own invariant uses, and it must be executed at the base before it is ordered, or it measures the debt rather than the round.

2026-09-10 · F275 R34 · A catalog id that is a PREFIX of a model attribute cannot be migrated by substring, and the reviewer proved this by doing it in its own dry run rather than by reasoning about it. Measured at `bc77c7ac`, the bare substring `job.run` matches 60 lines in 13 files, and 34 of those lines in 6 files are real attribute access — `job.run_refs`, `job.run_manifest_path`, `job.run_manifest_episodes` in `pingpong_job.py`, `self_use_runner.py` and four test modules — so a blind replace silently turns them into attributes that do not exist. The token-safe form `(?<![\w.])job\.run(?![\w-])` matches 26 lines in 7 files at that same commit and none of them is an attribute. Nothing caught the corruption except reading the diff, because every corrupted line still parsed and the suite had not yet run. A command-id migration states the boundary characters of the token it replaces, and a sweep whose replacement is anchored on neither side is a rewrite of every identifier that happens to start the same way.

2026-09-10 · F275 R34 · The reviewer's first count of that same token-safe sweep said 12 lines in 4 files, and it was wrong because the tree it was measured on had already had part of the migration applied and then reverted only partially — the quoted occurrences in `tests/` were still converted when the count was taken. The clean-base figure is 26 lines in 7 files, of which four are consumed by the catalog and dispatch edits that precede the sweep, leaving 22 in 5. The block's own pre-emission check caught it by re-running the measurement against the live base rather than trusting the dry run's console output. A numeral produced during a dry run belongs to the STATE that run had reached, not to the base, and any figure a block states is re-measured at the base after the dry run ends.
SLIPS34

## SLICE DECISION34 → append to `.agent/decisions.md`

<<<DECISION34
## DECISION F275 D19 (2026-09-10, F275 round 34) — amending DECISION F275 D18: the `--unattended` and `--yes` surfaces are INHERITED by `job.resume`, not lost, because losing them would delete F114's cost-preview contract with them

CONTEXT AND WHAT IS BEING AMENDED. DECISION F275 D18, recorded at round 32, ruled that `job.resume` inherits the classic runner's execution path, and listed two things as "genuinely lost and owing a finding when the surface dies": the `--unattended` flag and the `--yes` cost-preview skip at the `job.run` door, on the ground that `_cmd_job_resume` passes neither to the handler it calls. That reading was correct about the code and wrong about the consequence, and this decision amends it. The landed text of D18 is NOT rewritten, per planner_reviewer_prompt.md §3 item 20; this paragraph is its dated correction.

WHAT THE REVIEWER MEASURED AT `bc77c7ac` THAT D18 DID NOT. `tests/test_command_catalog.py` carries three tests that pin the F114 cost-preview contract to the catalog, and all three name `job.run` by id: `test_exactly_job_run_is_marked_expensive_so_far`, which asserts that the set of commands marked `is_expensive` is EXACTLY one entry; `test_job_run_is_expensive`; and `test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation`, which asserts that the expensive command declares exactly one `--yes` arg and that it is a flag rather than a valued option. Deleting `job.run` under D18's reading therefore does not lose two flags — it empties the `is_expensive` set, leaves F114's entire product surface with no command to attach to, and turns three contract tests into assertions about nothing. F114 is a SHIPPED, CLOSED feature; a later feature's deletion round is not the place its contract quietly ends.

THE SECOND MEASUREMENT, WHICH SETTLES THE DIRECTION. `--yes` is the only way to run the expensive command above the configured cost threshold without a terminal present: `_cmd_job_run_cycles` calls `confirm_cost_preview(..., yes=(yes or unattended), ...)`, and the user guide `docs/guides/cost-preview-user-guide-v0.md` documents the non-interactive failure explicitly — piping empty stdin produces "stdin is not a terminal, so there is nobody to confirm. Pass --yes to run ... without a prompt." Removing that flag while keeping the expensive path alive behind `job.resume` would leave every scripted or unattended run above the threshold with no way to proceed. That is an automation regression with no workaround, not a cosmetic loss of a convenience flag.

CHOSEN: `job.resume` INHERITS BOTH FLAGS AND THE `is_expensive` MARK, IN THE SAME COMMIT THAT RETIRES `job.run`. Concretely, and measured by applying it: the catalog entry for `job.resume` gains the `--unattended` and `--yes` `ArgDef`s verbatim from `job.run`'s, gains `is_expensive=True`, and drops `job.run` from its `related=` tuple; `_cmd_job_resume` gains `unattended` and `yes` keyword parameters and passes both through to `_cmd_job_run_cycles`; the `job.resume` dispatch lambda reads both off the namespace with `getattr` defaults, exactly as the `job.run` lambda did, so an argparse namespace from before the flags existed still works; and `_cmd_job_run_cycles`'s `command_name="job.run"` becomes `command_name="job.resume"`, which is the string the cost-preview prompt prints. The three F114 tests are re-pointed to `job.resume` rather than deleted, and the assertion in the first of them stays EXACT — the expensive set is still asserted to be exactly one entry, and that entry is now `job.resume`. After the change the shipped catalog reads 220 commands in 44 groups with ZERO dangling `related=` references, and `job.resume` carries `job_id`, `--checkpoint`, `--dry-run`, `--cycles`, `--unattended`, `--yes` and `--json`.

THEREFORE NO FINDING IS OWED, AND THIS IS THE PART THAT AMENDS D18 OPERATIONALLY. Operator amendment amend0908-f275-finish rule 4 requires a finding naming the inheriting feature for "any user-observable behaviour lost". Under this decision NO user-observable behaviour is lost: every flag, the cost preview, the expensive mark and the non-interactive escape hatch continue to exist, on one door instead of two. The round that retires `job.run` therefore registers nothing, and the open set stays at 87.

ALTERNATIVES CONSIDERED. (a) FOLLOW D18 AS WRITTEN — delete the flags and register two findings naming an inheriting feature — rejected on both measurements above: it ends F114's contract inside an unrelated feature's deletion round and removes the only non-interactive path above the cost threshold, and a finding is a record of a regression rather than a substitute for not causing one. (b) KEEP `job.run` ALIVE beside `job.resume` until a later feature re-homes the flags — rejected by AGENTS.md's Scope Control, which forbids leaving a replaced mechanism alive beside its replacement and names the compatibility alias as the thing not to build. (c) MOVE `is_expensive` TO `do.run`, which also spends money — rejected because `do.run` does not call `confirm_cost_preview` at all, so marking it expensive would make the catalog claim a preview the code does not perform, which is the gate-that-lies class this record exists to prevent. (d) GIVE THE FLAGS TO `job.resume` IN ONE ROUND AND DELETE `job.run` IN THE NEXT — rejected because it leaves two doors carrying the same flags across a session boundary, and because the whole change measured green in one commit.

HOW TO REVERSE. Delete this paragraph and the five above it; DECISION F275 D18's own text is unedited and still reads as originally recorded, so reverting this amendment restores its "genuinely lost" reading without any further edit. Reversing the CODE is `git revert` of this round's C4.
DECISION34

## PAIRS E1 to E3 → three prose sites the token sweep does not reach

<<<E1-FROM
        assert marked == ["job.run"], (
            f"F114 T003 has only marked job.run so far; found {marked}"
        )
E1-FROM

<<<E1-TO
        assert marked == ["job.resume"], (
            f"F114 T003 marks exactly the one expensive command; found {marked}"
        )
E1-TO

<<<E2-FROM
Only `remedy job run` carries a cost preview today; it is the command the
E2-FROM

<<<E2-TO
Only `remedy job resume` carries a cost preview today; it is the command the
E2-TO

<<<E3-FROM
    def test_exactly_job_run_is_marked_expensive_so_far(self) -> None:
E3-FROM

<<<E3-TO
    def test_exactly_one_command_is_marked_expensive_so_far(self) -> None:
E3-TO

## SPEC-INHERIT → the C4 production change

The worker writes this code. The reviewer applied ALL of it at `bc77c7ac` and
ran the full serial suite over it green, so every count below is measured.
Do part (1) before part (2): the catalog must carry the flags before the door
that had them is removed.

(1) THE INHERITANCE.
  (a) `apps/cli/command_catalog.py`, the `job.resume` entry: insert the
      `--unattended` and `--yes` `ArgDef`s AFTER its `--cycles` arg and BEFORE
      its `_JSON_OPT`, copied VERBATIM from the `job.run` entry's own two
      `ArgDef`s including their help text. Add `is_expensive=True`. Change its
      `related=("job.checkpoints", "job.run", "event.replay")` to
      `related=("job.checkpoints", "event.replay")`.
  (b) `apps/cli/commands/job.py`, `_cmd_job_resume`: add keyword-only
      `unattended: bool = False` and `yes: bool = False` to the signature, and
      pass both through on the single `_cmd_job_run_cycles(...)` call that ends
      that function. That call site occurs exactly ONCE.
  (c) `apps/cli/commands/job.py`, the `job.resume` dispatch entry: in the
      `else _cmd_job_resume(` branch, add
      `unattended=getattr(args, "unattended", False),` and
      `yes=getattr(args, "yes", False),`. Use `getattr` with a default, not
      attribute access, so an older argparse namespace still works — there is a
      test that asserts exactly that and it is named in (3)(b).
  (d) `apps/cli/commands/job.py`: `command_name="job.run",` becomes
      `command_name="job.resume",`. It occurs exactly once and it is the string
      the cost-preview prompt prints.

(2) THE RETIREMENT.
  (e) `apps/cli/command_catalog.py`: DELETE the whole `CommandEntry(` block
      whose `command_id="job.run"`. The reviewer measured that span at 27 lines.
  (f) `apps/cli/commands/job.py`: DELETE the seven-line `"job.run": lambda args:`
      dispatch entry. `_cmd_job_run_cycles` ITSELF SURVIVES and is not touched:
      it is now reached only from `_cmd_job_resume`, which is the whole point of
      DECISION F275 D18.

(3) THE PAIRS AND THE SWEEPS, STRICTLY IN THIS ORDER: E1, E2, E3 FIRST, THEN
    (a), THEN (b). The order is load-bearing and the reviewer measured why.
    E1's FROM contains both `["job.run"]` and the words `job.run so far`, which
    sweep (b) rewrites; E2's FROM contains `remedy job run`, which sweep (a)
    rewrites. Applied after their sweep, either FROM would occur ZERO times and
    the pair would be unappliable. Applied before, each TO already carries the
    migrated spelling, so neither sweep finds anything left to change in it.
    E3's FROM contains `job_run` with an UNDERSCORE and is touched by neither.
    BECAUSE THE PAIRS RUN FIRST, THE SWEEP COUNTS BELOW ARE THE BASE READINGS
    AND NOT WHAT YOUR SWEEP WILL CHANGE. Report what each step actually changed;
    the block states no expected number for the sweeps, and the binding gates
    are the ZERO readings afterwards and the empty `job.resume_` diff in G7.
  (a) THE SPACED ADVERTISEMENT. Over tracked files under `apps/`, `packages/`,
      `tests/`, `scripts/` and `docs/` but NOT `docs/roadmap/`, replace
      `remedy job run` with `remedy job resume` on every line that contains it
      and contains NEITHER `run-loop` NOR `run-next` — those two name commands
      deleted by earlier rounds and their sentences are history, not
      advertisements. At the base, before any pair is applied, that matches 17
      lines in 11 files.
  (b) THE DOTTED ID, TOKEN-SAFE ONLY, per constraint 8. Over the same trees,
      apply the regular expression in constraint 8 and replace with
      `job.resume`. At the base, before anything else in this round is applied,
      that regex matches 26 lines in 7 files, enumerated as
      `apps/cli/command_catalog.py` 2, `apps/cli/commands/job.py` 2,
      `docs/guides/cost-preview-user-guide-v0.md` 5,
      `tests/cli/test_cost_preview.py` 4,
      `tests/orchestration/test_escalation.py` 4,
      `tests/orchestration/test_long_run_executor.py` 3 and
      `tests/test_command_catalog.py` 6. By the time this sweep runs, parts (1),
      (2) and E1 have already consumed some of those lines and deleted others
      with the blocks holding them, so the number it changes is SMALLER and is
      yours to report rather than the block's to predict.

(4) THE SIX TESTS THAT MUST MOVE, which the reviewer found by running the suite
    and which no sweep reaches. Each is a contract that survives on the
    inheriting command; none is deleted and no assertion is weakened.
  (a) `tests/orchestration/test_resume_cli.py`, class `TestHandOff`, three
      tests: each asserts the EXACT kwargs dict handed to `_cmd_job_run_cycles`.
      Add `"unattended": False, "yes": False` to each expected dict. The
      assertions stay exact equalities; they simply describe the wider handoff.
  (b) `tests/orchestration/test_escalation.py`, class
      `TestUnattendedRunLoopCliFlag`, two tests: both monkeypatch
      `_cmd_job_run_cycles` and then dispatch through `COMMAND_HANDLERS`. With
      the door moved, that dispatch now calls `_cmd_job_resume` FIRST, whose
      preamble loads the job and exits 1 on the stub id before the patched
      function is ever reached. Monkeypatch `_cmd_job_resume` instead, in both.
      The property under test is unchanged — the CLI flag reaches the handler.
  (c) `tests/orchestration/test_long_run_executor.py`: the single assertion
      `assert entry.subcommand == "run"` becomes `== "resume"`.

## Done when — GATES G1 to G8

Run every gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Every gate is ordered
at a commit STRICTLY EARLIER than C5, per §3 item 31.

**G1 TRANSPORT (at C0b).** Report the sha256 and byte length of
`.remedy-wt/f275-r34-block.md`, and show the committed
`.agent/authored/f275-r34.md` and `.agent/last_block.md` BYTE-EQUAL to it.
`.agent/last_block.md` comes from `git cat-file blob` of the committed C0a blob.
State that the chain covers three on-disk artefacts and no prompt bytes.

**G2 THE PLAN (at C1).** Committed `.agent/plan.md` byte-equal to PLAN34; report
both lengths, the sha256, the line count against the cap of 50, and
`^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2 and C3).** For RECORD34 and SLIPS34 at C2 and DECISION34
at C3: report each pre-size, confirm it equals constraint 4's figure, show
post == pre + ONE newline + slice, and read the joining byte BACK at offset
len(pre). Then the independent structural reader: count N from each slice
yourself, never from this block, and match the last N blank-line units against
the slice's N paragraphs IN ORDER. One negative control per append, flipping a
byte INSIDE THE FIRST appended paragraph, REJECTED by BOTH readers. Then
`^Gate: F275 R33 ` and `^## DECISION F275 D19 ` each exactly 1.

**G4 THE OPEN SET (at C4).** BY DISTINCT ID from `.agent/live_review.md`:
every `^- R-\d+ — ` id minus every `^Done: R-\d+ — ` id. Report the count at the
base `bc77c7ac` and at C4; both must read 87. Report the ids registered and
resolved this round; both lists must be EMPTY.

**G5 THE INHERITANCE LANDED (at C4).** By IMPORTING `apps.cli.command_catalog`
in `python3` — never the `remedy` binary, which is denied here — report: the
command count and the group count; the number of dangling `related=` references
resolved on the DOTTED id; the full sorted list of commands with
`is_expensive` true; and `job.resume`'s full arg-name list in order. Expected
220, 44, ZERO, exactly `['job.resume']`, and
`['job_id', '--checkpoint', '--dry-run', '--cycles', '--unattended', '--yes', '--json']`.
Then confirm `job.run` is ABSENT from the id set, and report that it was PRESENT
at the base — the absence needs the presence beside it.

**G6 THE HANDLER SURVIVED AND THE FLAGS REACH IT (at C4) — RED PROOF.** First,
by parsing `apps/cli/commands/job.py` with `ast`, report that
`_cmd_job_run_cycles` is still defined and print the names of every function
that references it; `_cmd_job_resume` must be among them. Then, in a disposable
worktree at C4 with `__pycache__` purged, run
`python3 -B -m pytest tests/orchestration/test_resume_cli.py tests/orchestration/test_escalation.py tests/test_command_catalog.py -q`
UNMUTATED first and report the exit code and pass count as the control. Then TWO
mutations, each reverted byte-exactly and each reported with WHICH assertion
fired, not merely an exit code:
  M1 — in the `job.resume` dispatch lambda in `apps/cli/commands/job.py`, delete
       the line `            yes=getattr(args, "yes", False),`. That exact byte
       string occurs once in that file. Expect RED: the flag no longer reaches
       the handler.
  M2 — in `apps/cli/command_catalog.py`, change the `job.resume` entry's
       `is_expensive=True,` to `is_expensive=False,`. That byte string occurs
       once in that file after C4. Expect RED in `tests/test_command_catalog.py`,
       which proves the F114 contract really did move rather than merely being
       re-pointed at a passing assertion.

**G7 THE SWEEPS AND THE SUITE (at C4).** Report, over the trees named in
SPEC-INHERIT (3), the counts BEFORE and AFTER C4 for: `remedy job run` excluding
`run-loop` and `run-next` lines, and the token-safe regex of constraint 8. Both
must be ZERO after; report the before readings too, because an absence proves
nothing without them. Report the number of lines each sweep actually changed —
the block predicts neither, for the ordering reason SPEC-INHERIT (3) states, and
the ZERO afterwards is the binding half. THEN, and this
is the gate constraint 8 exists for, print `git diff` filtered to lines
containing `job.resume_` and confirm the result is EMPTY — that is the direct
check that no attribute access was corrupted. Then, SERIALLY in the primary
checkout and only after C4 is committed, `python3 -B -m pytest tests/ -q`: the
reviewer read `18339 passed, 23 skipped` at exit 0 over this exact change, which
is identical to the base. Report YOUR numbers. Then the canary
`python3 -m pytest tests/cli/test_golden_path.py -q` and
`python3 -m pytest tests/docs/ -q`, which this round owes for its `docs/` paths.

**G8 NOTHING ELSE MOVED (at C4).** `.agent/STOP` read from disk and ABSENT.
`git status --porcelain` EMPTY. `git worktree list` exactly ONE entry. Branch
`feature/f275-one-world-completion-part-three`.
`git diff --name-only bc77c7ac..<C4>` an EXACT SET MATCH against the path list
in the header's `Change:` line, which does not include `.agent/handoff.md`,
reported as MISSING and EXTRA, both empty — and note that
`apps/ui/node_modules` appearing there would mean constraint 7 was broken. Per-
commit insertions for every commit before the handback, each under the cap of
500. Finally the LINT CEILING, per constraint 11:
`python3 -m pytest tests/orchestration/test_ci_budgets.py -q` and the repo-wide
`ruff check .` count beside it, reported as a number rather than as a verdict.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
SESSION NUMBER 16 of feature F275, round 34, ONE LINE PER GATE with real exit
codes and real numbers, the changed-files table with the `+/-` column taken from
`git diff --numstat` (§3 item 28), the item-status table, the open-findings
count, and the one-sentence context self-assessment amend0905-throughput
requires. Declare every deviation.
