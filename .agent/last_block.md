STEP T002/5 — F260 · ROUND 11 · ONE SPELLING FOR THE RUN STORE
(§3 item 37: every rule line below is exactly sixty-two U+2500 characters, and
no other line of this block's frame is a run of a repeated character.)

Goal:
  Give the ping-pong RUN store one spelling in `data_paths`, exactly as rounds 6
  to 8 did for the job store, and DELETE the module-local
  `pingpong_loop._pingpong_runs_dir` that owns it today. The store does NOT move
  this round: only its spelling changes, so DECISION F260 D1's collapse of
  `pingpong_runs/<run_id>/` into `runs/<run_id>/` becomes a change to two
  function bodies instead of a sweep of every caller. Round 9 proves the
  ordering works: it turned a 134-site move into a 76-insertion commit.
  This round also records DECISION F260 D5, moving the resolver collapse from
  T002 to T004 — the reasoning is measured, and is in the slice itself.

Base: `2cedf98c9fbc85c90c85a3ed45cfd257164c7361` (`2cedf98c`). Every reading
quoted in this block was taken by the reviewer at that commit.

Bundle:
  C0a  Save this block verbatim as `.agent/authored/f260-r11.md`.
  C0b  Mirror it into `.agent/last_block.md`.
  C1   `.agent/plan.md` ← the PLAN slice, whole-file replacement.
  C2   `.agent/live_review.md` ← append GATE_R10.
  C3   `.agent/prose_slips.md` ← append the two SLIP lines.
  C4   `docs/roadmap/features/T2_F260.md` ← append the DECISION_D5 slice, and
       `.agent/decisions.md` ← append the same decision text.
  C5   THE PRODUCTION SWEEP — see SPEC (1) and (2).
  C6   THE TEST SWEEP — see SPEC (3).
  C7   Handback: rewrite `.agent/handoff.md`.

Change set — nothing outside these paths:
  .agent/authored/f260-r11.md           (new)
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/decisions.md
  .agent/handoff.md
  docs/roadmap/features/T2_F260.md
  packages/orchestration/data_paths.py
  packages/orchestration/pingpong_loop.py
  packages/orchestration/pingpong_evidence.py
  packages/orchestration/pingpong_promote.py
  packages/orchestration/worktree_resume.py
  packages/orchestration/job_evidence.py
  packages/orchestration/repair_attest.py
  apps/cli/commands/do_cmd.py
  tests/test_data_paths.py
  — plus EXACTLY the test files SPEC (3) names, and no other.

──────────────────────────────────────────────────────────────
MEASURED AT THE BASE — do not re-derive these

  - `pingpong_loop._pingpong_runs_dir` is defined at `pingpong_loop.py:4229` and
    returns `resolve_data_root() / "pingpong_runs"`. It is the ONLY definition.
  - THIRTY-NINE references live under `packages/` and `apps/`, in seven modules:
    `pingpong_loop.py` (12, including the definition), `job_evidence.py` (13),
    `pingpong_promote.py` (4), `worktree_resume.py` (4), `pingpong_evidence.py`
    (2), `repair_attest.py` (2) and `apps/cli/commands/do_cmd.py` (2).
  - NO TEST GUARDS IT. `grep` over `tests/` for the name paired with `assert`,
    `hasattr` or `def test` returns nothing, so no existing test pins it to
    `pingpong_loop` and none has to be rewritten to allow the move.
  - THE EVIDENCE-OWNING GUARD DOES NOT TRIP. `tests/test_data_paths.py`'s
    `test_no_module_that_owns_job_evidence_spells_the_path_itself` requires ZERO
    AST references to the name `jobs_dir` in `pingpong_job`, `job_evidence`,
    `repair_attest` and `do_cmd`. `pingpong_runs_dir` and `pingpong_run_dir` are
    DIFFERENT names under a reading that matches on the resolved name, so three
    of those four modules take the new import safely. Do not weaken that guard.
  - THREE LOCAL VARIABLES ARE NAMED `runs_dir` while holding the PING-PONG runs
    root: `worktree_resume.py:136`, `job_evidence.py:1498` and
    `pingpong_loop.py:4271`. `data_paths.runs_dir` is a real and different
    function, so those names are the misleading-local defect R-0814 was an
    instance of. SPEC (2) renames them.

──────────────────────────────────────────────────────────────
SPEC FOR C5 — described, not sliced; you write the code

(1) `packages/orchestration/data_paths.py` gains the pair, placed beside the
    other "where does this live" answers and built one on the other exactly as
    `job_dir` / `job_record_path` are:

      pingpong_runs_dir(root: Path | None = None) -> Path
          <root>/pingpong_runs — the run store AS IT IS TODAY.
      pingpong_run_dir(run_id: str, root: Path | None = None) -> Path
          pingpong_runs_dir(root) / run_id

    Both take `root` and honour it, like every other function in the module.
    Add them to the `Public API::` block at the top.
    Write the WHY comment above the pair, in the idiom the module already uses:
    these name the store as it is today, DECISION F260 D1 says a run belongs at
    `<data_root>/runs/<run_id>/`, and giving the live store one spelling is what
    makes that move two function bodies instead of a sweep. Say plainly that
    `run_dir` above is the TARGET spelling and this pair is the LIVE one, which
    is the same relationship `job_dir` and `task_job_dir` had before round 9
    collapsed them — and that the collapse here is F260 T002's remaining work.

(2) DELETE `pingpong_loop._pingpong_runs_dir` and move all thirty-nine
    references onto the new pair. Where a site builds `_pingpong_runs_dir() /
    <run id>` by hand, use `pingpong_run_dir(<run id>)` instead — that
    hand-built join is the same shape whose job-store twin was finding R-0814's
    root cause, and leaving it would keep the defect alive one directory over.
    Where a site legitimately wants the ROOT (an iteration, an existence check),
    use `pingpong_runs_dir()`.
    Check whether each module imports `data_paths` at module level or inside
    function bodies, and follow that file's existing convention.
    RENAME the three misleading locals named `runs_dir` to `pp_runs_root` at
    `worktree_resume.py:136`, `job_evidence.py:1498` and `pingpong_loop.py:4271`
    and at every use of each within its own function. Re-grep all three line
    numbers before editing: they were read at `2cedf98c` (§3 item 9).

(3) FOR C6 — the test sweep. Move every `_pingpong_runs_dir` reference under
    `tests/` onto the same pair, by the same rule. The reviewer measured the
    reference counts per file at `2cedf98c`; use them as a CHECKLIST and report
    any file where your own count differs:
      test_pingpong_promote.py 46 · test_job_evidence.py 8 · test_failure_wiring.py 4
      test_worktree_safety.py 4 · test_pingpong_cli.py 3 · test_worktree_isolation.py 3
      test_job_worktree_integration.py 3 · test_worktree_resume_cli.py 2
      test_stream_export_e2e.py 2 · test_run_manifest_ledger_semantics.py 2
      test_worktree_persistence.py 2 · test_worktree_lifecycle.py 2
      test_persisted_run_call_schema.py 2 · test_persisted_call_episode_membership.py 2
      test_job_worktree_integrity.py 2 · test_run_manifest_zero_call_expectations.py 2
      test_job_worktree_handoff.py 2 · test_run_manifest_task_lifecycle_binding.py 2
      test_repair_loop.py 2 · test_persisted_call_ownership.py 2
    All twenty are under `tests/orchestration/`. If C6 would exceed the
    AGENTS.md 500-insertion cap, SPLIT it by file into two commits and say so.

(4) ADD to `tests/test_data_paths.py`, inside `TestJobAndRunLayout`, two tests
    mirroring the ones round 9 added for the job store:
    (A) `test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir` —
        `pingpong_run_dir(rid) == pingpong_runs_dir() / rid`, and the `root`
        argument is honoured by BOTH against an env root pointing somewhere
        else, so a function that drops `root` cannot pass by coincidence.
    (B) `test_pingpong_loop_has_no_runs_dir_helper_at_all` — the deleted-name
        guard, in the two readings round 8 proved are different:
        `hasattr(pingpong_loop, "_pingpong_runs_dir")` is False, AND the
        `_names_of` helper already in this file (which covers `FunctionDef` as
        well as references, because a revived helper comes back as an uncalled
        `def` first) finds zero for that name in `pingpong_loop`. Include the
        non-vacuity assertion the round-8 test carries: `hasattr` must find some
        OTHER real attribute of `pingpong_loop`, or the absence above would be
        measuring an import failure rather than a deleted helper.

──────────────────────────────────────────────────────────────
CONSTRAINTS

 1. Apply every authored slice BYTE FOR BYTE. If a slice or a gate looks wrong,
    apply it as given and DECLARE the defect. Never repair a slice, and never
    reshape code to make a reviewer's gate go green. Both of the last two rounds
    contained reviewer gate defects that only a declared deviation exposed.
 2. Change-set discipline: no path outside the list above and the twenty test
    files SPEC (3) names. The list bounds WRITES, not reads or worktrees.
 3. `.agent/plan.md` stays under 50 lines; the PLAN slice was measured against
    that cap before emission.
 4. Both `.agent/` appends target files ending with exactly ONE newline at
    `2cedf98c`, measured: `.agent/live_review.md` at 912232 bytes and
    `.agent/prose_slips.md` at 105750 bytes. Derive each recipe from its own
    target's terminal byte.
 5. Slice shapes, classified before emission and stated per target, because
    DECISION_D5 has a DIFFERENT shape in each of its two targets:
      GATE_R10 — APPEND at end of `.agent/live_review.md`.
      SLIP7, SLIP8 — APPEND at end of `.agent/prose_slips.md`.
      DECISION_D5 — INSERTION into `docs/roadmap/features/T2_F260.md`, between
        the end of DECISION F260 D4 and the `## Design` heading; and an APPEND
        at end of `.agent/decisions.md`.
      PLAN — whole-file REWRITE of `.agent/plan.md`.
    No pair in this block has a FROM, so no containment test applies and no
    FROM-zero count is ordered anywhere. An INSERTION is not an append and its
    proof is whole-file identity, which G4(b) orders.
 6. The DECISION_D5 slice is appended to `docs/roadmap/features/T2_F260.md` so
    that it lands INSIDE the `## DECISIONs` section, after DECISION F260 D4 and
    BEFORE the `## Design` heading — a decision filed under Design would not be
    found by a reader following the file's own structure. Measure where that
    boundary is and say which line you inserted at. The same text is APPENDED at
    the end of `.agent/decisions.md`.
 7. `git status --porcelain` is EMPTY at the handback. Destructive checks run
    only in a disposable `git worktree` (self-drive protocol G5).
 8. AGENTS.md throughout: self-review loop before every commit, 500-insertion
    cap counting INSERTIONS only, push after committing, no force push, no work
    on `main`, no merge, no pull request.

──────────────────────────────────────────────────────────────
DONE WHEN — eight gates, each RUN and its real exit code recorded

G1 TRANSPORT — one digest. `sha256sum .agent/authored/f260-r11.md` equals the
   digest named in the delegation that carried this block, and the same digest
   over `.agent/last_block.md`. One reading, not a chain.

G2 THE RECORD. (a) EXACT IMAGE: the post-image at C2 EQUALS
   `pre + b"\n" + GATE_R10 + b"\n"` byte for byte; state the measured length.
   (b) STRUCTURAL: split on `"\n\n"`; the last unit with the terminating newline
   stripped equals GATE_R10; units run 430 → 431. (c) NEGATIVE CONTROL: flip one
   byte inside the appended paragraph and confirm (a) AND (b) both reject, then
   restore and confirm both accept. (d) After C2: `^Gate: ` headers 20, all
   distinct; registrations 299 over 299 distinct ids; `^Done: ` 5 lines over 3
   distinct ids; open set 296 by distinct id.

G3 THE SLIPS. The post-image EQUALS
   `pre + b"\n" + SLIP7 + b"\n\n" + SLIP8 + b"\n"` byte for byte; blank-line
   units run 137 → 139, a rise of exactly TWO, one per slip.

G4 THE PLAN AND THE DECISION.
   (a) `.agent/plan.md` equals the PLAN slice plus exactly one trailing newline
       and is under 50 lines.
   (b) `docs/roadmap/features/T2_F260.md`, proved as an INSERTION by WHOLE-FILE
       IDENTITY and not by a substring count: let `pre` be the file at
       `2cedf98c` and `off` the byte offset you inserted at; then the post-image
       EQUALS `pre[:off] + <the inserted bytes> + pre[off:]` exactly, so nothing
       outside the insertion point moved. Report `off` and the inserted length.
       Then, as the structural half: the DECISION_D5 text occurs EXACTLY ONCE;
       the file still ends with exactly one newline; `^### DECISION F260 D`
       matches SIX times with D0, D1, D2, D3, D4 and D5 each exactly once; and
       the byte offset of the D5 heading is GREATER than that of the D4 heading
       and LESS than that of the `## Design` heading — the placement constraint
       6 orders. Measured at the base for you: D4's heading is at offset 13104
       and `\n## Design` at 15565, so a correct `off` lies between them.
   (c) The same text occurs exactly once in `.agent/decisions.md`.

G5 THE SPELLING IS ONE, AND THE OLD NAME IS GONE.
   (a) `hasattr(pingpong_loop, "_pingpong_runs_dir")` is False, and
       `hasattr(data_paths, n)` is True for `pingpong_runs_dir` and
       `pingpong_run_dir`. The second half is the non-vacuity control.
   (b) By AST over every TRACKED `.py` file under `packages/`, `apps/` and
       `tests/`, references AND definitions resolving to exactly
       `_pingpong_runs_dir` number ZERO. Use a reading that covers `FunctionDef`
       as well as `Name`, `Attribute` and `alias` — round 8 measured that a
       revived helper is a `def` and is INVISIBLE to a reference-only reading.
       NON-VACUITY CONTROL: the same reading over `pingpong_run_dir` is
       NON-ZERO. Both halves were run at the base: at `2cedf98c`
       `_pingpong_runs_dir` is non-zero, so this gate can fail.
   (c) The literal `pingpong_runs` occurs under `packages/`, `apps/` and
       `tests/` ONLY inside `packages/orchestration/data_paths.py`. Report the
       count and the file list rather than asserting a total the block names —
       and note this gate is deliberately NOT "zero everywhere", because
       `data_paths` is where the string now lives and a zero-gate would be
       unmeetable by construction. Round 9's G5(c) was exactly that mistake.
   (d) VALUE, with `REMEDY_DATA_DIR` at a scratch directory:
       `pingpong_run_dir(r)` equals `pingpong_runs_dir() / r`, and both honour a
       `root` argument set to a DIFFERENT directory from the env root.

G6 THE SUITES, run SERIALLY, each exit code recorded separately, never piped:
     `pytest tests/test_data_paths.py -q -p no:randomly`
     `pytest tests/orchestration/ -q -p no:randomly`
     `pytest tests/cli/test_golden_path.py -q -p no:randomly`   (the canary)
     `pytest tests/docs/ -q -p no:randomly`   (this round writes docs/roadmap/**,
       which the §3 docs-round tier requires; run it AFTER C4)
   Report the passed count and exit code for each. Also run
   `python3 -m apps.cli.grouped integrity check --json` and record `passed`,
   `fail_count` and the check count.

G7 THE MUTATION RED-PROOF, in a disposable `git worktree` at the C6 commit,
   `__pycache__` purged, `python3 -B`, and the module confirmed to resolve from
   THAT worktree before any colour is trusted.
   (i)   UNMUTATED CONTROL FIRST over `tests/test_data_paths.py`: exit code AND
         passed count.
   (ii)  Make `pingpong_run_dir` ignore its `root` argument. Test (A) must FAIL.
   (iii) Re-add `_pingpong_runs_dir` to `pingpong_loop` as an uncalled `def`.
         Test (B) must FAIL — and note which of its two readings catches it: a
         `def` is invisible to a reference-only reading, which is the whole
         reason (B) carries both.
   (iv)  Restore after EACH mutation, confirm the control is green again, and
         confirm `git diff` in that worktree is empty after the last restore.
   Name each revert target by PATH and verify the bytes you replace occur EXACTLY
   ONCE in that file before editing (§3 item 25) — round 10's first two candidate
   targets were both non-unique, so expect the same here.

G8 LINT AND CLEAN TREE. `ruff check` over exactly the production and test paths
   this round edited exits 0 — file-scoped on purpose, because `ruff check
   packages/` and `ruff check tests/orchestration/` are RED at the base with
   pre-existing errors that are not this feature's. Then `git status
   --porcelain` and `git ls-files .remedy-wt` are both EMPTY.

──────────────────────────────────────────────────────────────
HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, `SESSION 3 of feature F260`, branch, commit SHAs, the changed-files table
with its `+/-` column from `git diff --numstat` and never re-derived by eye (§3
item 28), ONE LINE PER GATE with its real exit code, the open-findings count BY
DISTINCT ID, the item-status table, the next expected action, and every
deviation — including any place this block is wrong. No length cap.

──────────────────────────────────────────────────────────────
AUTHORED SLICES

A slice is the bytes of the lines strictly BETWEEN its BEGIN and END marker
lines, joined by `"\n"`, carrying NO trailing newline. The marker lines are
never part of any slice and never reach any file.

<<<BEGIN GATE_R10>>>
Gate: R10 — the F260 R10 entry. R10 MADE THE CLASSIC RESOLVER RETURN A STRING AND THE CLASSIC LOADER TAKE EITHER SPELLING. VERDICT PASS. Range ce08cfd0..2cedf98c, seven commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; largest insertion count 320, a single `.agent/**` state write, and largest code commit 37, both far under the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN EVERY GATE ITSELF and reproduced every number the worker reported. TRANSPORT: one digest `28a3d69386e087be9fb6c8bd723592cc8121e60c5417686eea53e02fe6545f87` across the reviewer's scratch original, the saved copy at `.agent/authored/f260-r10.md` and the mirror at `.agent/last_block.md`; per §3 item 37 that chain covers those three artefacts and is not a claim about bytes emitted into a prompt. THE RECORD: 904283 to 912232 bytes, and the post-image is EQUAL to the pre-image plus a newline plus the 2934-byte DONE0814 slice plus two newlines plus the 5011-byte GATE_R9 slice plus a newline — an exact-image equality rather than a length check, which is the repair SLIP4 called for. Blank-line units ran 428 to 430 and the last two units are DONE0814 FIRST and GATE_R9 second, the order §4 item 4 requires. The negative control now WORKS: a byte flipped inside the FIRST appended paragraph is rejected by BOTH readings and both accept again after the restore, where round 9's wording could be satisfied by no run at all. Registrations 299 over 299 DISTINCT ids, `Done:` 5 lines over THREE distinct ids, nineteen `Gate:` headers, open set 296 BY DISTINCT ID, and the `Landed: R-0814` line survives BYTE-IDENTICAL to its image at `ce08cfd0`, which constraint 6 required and the reviewer verified by comparing the two lines rather than by counting them. THE SLIPS: 101682 to 105750 bytes by the same exact-image reading, units 134 to 137, a rise of exactly THREE. THE RESOLVER CONTRACT, read by the reviewer from the SHIPPED function against a scratch data root with a real classic job on disk: `resolve_job_id` returns a `str` and NOT a `UUID` for the full-id form and for the unique-prefix form alike, measured by `isinstance` rather than from the annotation; an UPPERCASE full uuid resolves to the canonical LOWERCASE string, which is the property a naive `return raw` destroys silently; the exit codes are unchanged at 2 for an ambiguous prefix and 1 for both an unmatched prefix and an invalid string; and `storage.load_job` returns the SAME record for `job.id` and for `str(job.id)`, with the two argument types confirmed to differ so a loader ignoring its argument could not pass. THE SUITES, re-run serially by the reviewer, all exit 0 at 59, 1537 and 203 — the middle one carrying the canary — and `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY in the reviewer's own disposable worktree at `d2af8906`, with the module confirmed to resolve from it and the control at exit 0 and 59 passed: dropping the normalisation to `return raw` reddens exactly `test_an_uppercase_uuid_records_exactly_as_the_lowercase_one_does`, and restoring the prefix path to `return UUID(matches[0])` reddens both `test_short_prefix_resolves` and `test_a_short_hex_prefix_records_exactly_as_the_full_id_does`; `git diff` was empty after each restore and the control was green again. Neither revert target was unique in its file on the first reading — `return str(UUID(raw))` and `return matches[0]` each occur twice, once per resolver — so both were anchored on a longer span verified to occur exactly once, which is §3 item 25 doing its job rather than being recited. RUFF over exactly the six changed paths exits 0. THE WORKER DECLARED FIVE DEVIATIONS AND EVERY ONE IS UPHELD. The first is a reviewer numeral error the reviewer confirmed at the base: gate G6's third group named three files and carried the figure 262, which the reviewer had measured over a FIVE-file selection during its blast-radius probe and then attached to a three-file gate; the true base and post-change reading is 203, `git log` over those three paths across this range is empty, and the gate's real property — serially green before and after — holds. The second and third are corrections beyond the SPEC and both are right: `resolve_any_job_id`'s docstring still claimed `resolve_job_id` "returns a `UUID`, which a 16-hex task-job id can never be", a sentence this round makes false, and `JobNotFoundError.__init__` needed `UUID | str` because `load_job` now passes a `str` into it and the project configures mypy, so leaving it would have INTRODUCED a type error rather than avoided one. The fourth notes that G7(iii) demanded a pytest node id from a clause whose subject is a probe with no node id, and the worker satisfied both halves rather than picking one. THE BLAST RADIUS THIS ROUND RESTED ON WAS MEASURED, NOT ESTIMATED, and the measurement is worth recording because its first reading was misleading: patching the signature in a disposable worktree and running the full suite gave 20 failures, of which FIFTEEN were a `-n auto` PARALLELISM artifact — the same `tests/ui_server/` and `test_test_runner.py` selections are green run serially BOTH at the unpatched base and with the patch applied — leaving exactly five real failures, every one of them a test asserting the return type being changed, and ZERO production call sites, because `storage.load_job` builds its path by formatting the id and forty call sites pass the resolved value straight into it. Attributing those fifteen by demonstration rather than by assumption is what docs/agents/integration_gate.md step 3 asks for, and it is the difference between a round scoped at five tests and a round abandoned as too large.
<<<END GATE_R10>>>

<<<BEGIN SLIP7>>>
2026-09-06 · F260 R10 (reviewer) · Gate G6 of the round-10 block named a THREE-file group — `tests/ui_server/test_command_channel.py`, `tests/ui_server/test_live_state.py` and `tests/orchestration/test_test_runner.py` — and annotated it "(262 passed at base)". That figure came from a FIVE-file selection the reviewer had run during its blast-radius probe, which also carried `tests/test_data_paths.py` and `tests/cli/test_patch_cmd.py`, and the reviewer attached it to the three-file gate without re-running the smaller selection. The worker measured the real base at 203, and the reviewer confirmed 203 independently at `2cedf98c`; `git log` over those three paths across the round's range is empty, so no test was lost and only the numeral was wrong. THE LESSON is §3 item 16 as widened by finding R-0585 — resolve every count to the LIST IT NAMES, wherever that list lives — arriving through a reviewer's own scratch measurement rather than through a drifting body: a number measured over one selection may not be carried onto a different selection, and the cheap counter-measure is to re-run the exact command the gate orders, which §3 item 12 already requires and which was not done for this one clause. Reviewer-prose numeral error in a gate annotation; the gate's load-bearing property was measured and holds, and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP7>>>

<<<BEGIN SLIP8>>>
2026-09-06 · F260 R10 (reviewer) · The PLAN slice of the round-10 block wrote, of the resolver collapse, "Finding R-0809 — four wordings for 'unknown id', and a real id of the other store rejected — belongs here", and R-0809 does not belong to F260 at all. Read at `2cedf98c`, that finding's own registration records its routing: "Applied: acceptance line added to `docs/roadmap/features/T2_F261.md` ## Acceptance", and it is "resolved when the four-wordings-gone test is green" against F261's acceptance list, F261 being the feature that owns command naming and message shape. The reviewer named it from memory of the neighbouring subject matter — both concern what happens to an unresolvable id — instead of reading the finding's routing line, and the claim landed on disk in `.agent/plan.md`, the file AGENTS.md's Session Resume tells the next session to read SECOND. THE LESSON is §3 item 34's last clause, the one about the OPEN SET being a target that must be READ and not recalled: a finding cited in a plan or a block is opened and its routing read, because a finding that names another feature's acceptance list cannot be discharged by this feature's rounds and a plan promising otherwise sends a later session looking for work that is not there. The round-11 PLAN slice drops the claim. Reviewer-prose misattribution in a rewritten state file, never in the append-only record; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP8>>>

<<<BEGIN DECISION_D5>>>
### DECISION F260 D5 (2026-09-06, F260 round 11) — the resolver collapse lands in T004, with the store that makes it true
DECISION F260 D4 placed the ONE resolver "inside T002, in the same round group as
the unified record and its loader", and rounds 9 and 10 built both halves that
ruling named: the record now lives at `<data_root>/jobs/<16hex>/job.json` beside
its own evidence, and `resolve_job_id` returns a `str` exactly as
`resolve_any_job_id` does. The collapse itself is now measured as belonging one
task later, and this decision records why rather than leaving the discrepancy for
a later reader to find.

MEASURED at `2cedf98c`. `resolve_job_id` searches the CLASSIC store only;
`resolve_any_job_id` searches both. Collapsing them means the survivor searches
both, and forty call sites across nine `apps/cli/commands/` modules then accept a
16-hex ping-pong id they reject today. Every one of those call sites feeds
`storage.load_job`, which reads `<data_root>/jobs/<id>.json` — a FILE. A ping-pong
id names a DIRECTORY, so the resolver would succeed and the loader would then
raise `JobNotFoundError`, replacing today's clean `exit 1` with an exception on a
path forty commands share. The collapse is therefore not a rename; it is a
behaviour change to an error path, and it is only harmless once the classic store
is gone.

CHOSEN: the collapse happens in T004, in the same commit range that deletes the
classic store `<data_root>/jobs/<uuid>.json` and the classic runner. At that point
"one resolver over one store" is true rather than aspirational, the
`JobNotFoundError` case above cannot arise because there is no second shape left
to resolve into, and the feature file's existing T004 order — which already lists
`resolve_any_job_id` and every which-store branch as T004's deletions — is
satisfied by one change instead of two. T002's remaining work is what it always
was: the run directory, the unified record's fields and the Mission extension.

ALTERNATIVES CONSIDERED. Collapsing now and letting the loader raise — rejected:
it degrades a shared error path for forty commands for the length of a task, in a
feature whose own reason for existing is that unresolvable ids confuse the
operator. Collapsing now and teaching the loader to read both shapes — rejected:
that builds a compatibility reader, which AGENTS.md "Replacing is deleting" and
DECISION D-A forbid outright, and T004 would then delete code written two rounds
earlier. Leaving D4 unamended and letting a later session rediscover the
sequencing — rejected: D4 is quoted by the plan and by two round blocks, so an
unrecorded departure from it reads as drift rather than as a ruling.

NOT CHANGED BY THIS RULING: the deliverable, the scope, and D4's own reasoning
about why the resolver could not land in T001. Only the task the collapse sits in
moves, from T002 to T004.

REVERSE by deleting this paragraph, at which point D4's placement binds again and
the collapse returns to T002 with the error-path change unresolved.
<<<END DECISION_D5>>>

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 10 are reviewed and 2 to 10 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, and both
resolvers now return `str`.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE SPELLING FOR THE RUN STORE. `data_paths` gains `pingpong_runs_dir` and
`pingpong_run_dir`, and `pingpong_loop._pingpong_runs_dir` is DELETED with its
thirty-nine production references and its test references moved onto the pair.
The store does NOT move: only its spelling changes, so D1's collapse into
`<data_root>/runs/<run_id>/` becomes two function bodies. DECISION F260 D5 is
recorded in the same round, moving the resolver collapse to T004.

## Next Steps

- The run move itself: `pingpong_runs_dir` and `pingpong_run_dir` collapse into
  `runs_dir` and `run_dir`. The run LOG at `<data_root>/runs/<job_id>/` must
  move to the run id in the same commit, or `timeline.load_run_events` reads a
  directory keyed two ways — DECISION F260 D0 measured that collision.
- The unified record's own fields, and the Mission extension (order, contract,
  mission plan, job refs), which is the rest of T002.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- `<data_root>/runs/` is keyed by JOB id today and D1 keys it by RUN id. Every
  reader of the old shape moves in the same commit as its writer.
- `<data_root>/jobs/` holds both `<uuid>.json` files and `<16hex>/` directories.
  Any new reader of that directory must make the same file/directory
  distinction the two matchers make.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLAN>>>

──────────────────────────────────────────────────────────────
