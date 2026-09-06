STEP T002/5 — F260 · ROUND 10 · THE RESOLVER RETURNS A STRING
(§3 item 37: every rule line below is exactly sixty-two U+2500 characters, and
no other line of this block's frame is a run of a repeated character.)

Goal:
  Make `data_paths.resolve_job_id` return `str` instead of `UUID`, and make the
  classic loader accept either. This is the one prerequisite DECISION F260 D4
  named for the ONE resolver: "a `str`-returning resolver cannot replace it
  until that loader reads the unified record". After this round the two
  resolvers have the SAME return type, and collapsing them is a small change
  instead of a forty-call-site sweep.

Base: `ce08cfd0da8da2f2ad12237d385d26ea85698f0f` (`ce08cfd0`). Every reading
quoted in this block was taken by the reviewer at that commit.

Bundle:
  C0a  Save this block verbatim as `.agent/authored/f260-r10.md`.
  C0b  Mirror it into `.agent/last_block.md`.
  C1   `.agent/plan.md` ← the PLAN slice, whole-file replacement.
  C2   `.agent/live_review.md` ← append DONE0814, then GATE_R9, in that order.
  C3   `.agent/prose_slips.md` ← append the three SLIP lines.
  C4   THE SIGNATURE CHANGE — see the SPEC below.
  C5   Handback: rewrite `.agent/handoff.md`.

Change set — nothing outside these paths:
  .agent/authored/f260-r10.md           (new)
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  packages/orchestration/data_paths.py
  packages/orchestration/storage.py
  apps/cli/commands/job_stop_cmd.py
  apps/cli/commands/project.py
  tests/test_data_paths.py
  tests/cli/test_patch_cmd.py

──────────────────────────────────────────────────────────────
THE BLAST RADIUS IS MEASURED, NOT ESTIMATED — do not re-derive it

The reviewer applied exactly this change in a disposable worktree at `ce08cfd0`
and ran the suite. Readings, all reproducible:

  - FULL SUITE, `pytest tests/ -q -n auto`: 20 failed, 19666 passed. FIFTEEN of
    those twenty are a PARALLELISM artifact, not this change: the same
    `tests/ui_server/test_command_channel.py`, `tests/ui_server/test_live_state.py`
    and `tests/orchestration/test_test_runner.py` selections run SERIALLY are
    262 passed / 0 failed BOTH at the unpatched base AND with the patch applied.
    They are therefore attributed by demonstration and not by assumption.
  - THE CHANGE'S REAL COST IS FIVE TESTS, every one of them asserting the RETURN
    TYPE that is being changed, and ZERO production call sites:
      tests/test_data_paths.py::TestResolveJobId::test_full_uuid_returns_uuid
      tests/test_data_paths.py::TestResolveJobId::test_short_prefix_resolves
      tests/test_data_paths.py::TestResolveJobId::test_full_uuid_works_without_job_file
      tests/cli/test_patch_cmd.py::TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId::test_a_short_hex_prefix_records_exactly_as_the_full_id_does
      tests/cli/test_patch_cmd.py::TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId::test_an_uppercase_uuid_records_exactly_as_the_lowercase_one_does
  - WHY forty call sites cost nothing: `storage.load_job` builds its path as
    `f"{job_id}.json"`, which formats a `str` and a `UUID` identically, and the
    call sites pass the resolved value straight into it.
  - CASE NORMALISATION SURVIVES, which is the property the uppercase test above
    exists for: with the patch, `resolve_job_id('0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D')`
    returns `'0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d'`. Keep `str(UUID(raw))` on
    the parse path — `raw` alone would drop the normalisation and redden that
    test for a real reason.

──────────────────────────────────────────────────────────────
SPEC FOR C4 — described, not sliced; you write the code

(1) `packages/orchestration/data_paths.py`
    - `resolve_job_id`: annotate `-> str`. On the parse path return
      `str(UUID(raw))`, NOT `raw` — see the case-normalisation reading above. On
      the unique-prefix path return `matches[0]` rather than `UUID(matches[0])`.
      The exit codes and messages do not change.
    - Its docstring says the return type "says so: a task-job id is sixteen hex
      characters and `UUID()` rejects it". That reasoning is now carried by the
      SEARCH rather than by the type, since a `str` could hold either shape.
      Rewrite it to say the function still searches the CLASSIC store only, that
      the return is the canonical lowercase id as a string, and that F260 T004
      is where the two resolvers become one.
    - Update the `Public API::` block at the top: `resolve_job_id(raw) -> str`.
    - If `UUID` becomes unused as an import after your edit, check before
      removing it — `resolve_any_job_id` still parses with it.

(2) `packages/orchestration/storage.py` — `load_job` and `load_job_safe` take
    `job_id: UUID | str`. Both spellings must stay accepted, and this is not a
    hedge: `Job.id` is a `UUID` model field and many callers pass `job.id`
    directly, so narrowing to `str` here would break real callers that never
    touch a resolver. Say that in a one-line WHY comment above `load_job`, per
    the AGENTS.md discoverability convention. Change no behaviour: the path
    build and both exception paths already format the id.

(3) The two call sites that now wrap a string in `str()`:
    `apps/cli/commands/job_stop_cmd.py:119` reads
    `job_id = str(resolve_job_id(job_id))` and
    `apps/cli/commands/project.py:449` reads
    `resolved_id = str(resolve_job_id(job_id_str))`. Drop the redundant `str(`
    call at both. Re-grep both line numbers before editing — they were read at
    `ce08cfd0` and this round's own commits do not move them, but §3 item 9 asks
    for the check rather than the assumption.

(4) The five tests named above. Each asserts the resolver's result equals a
    `UUID`; make each compare against the STRING form. In
    `tests/test_data_paths.py` that is `str(uid)` and in
    `tests/cli/test_patch_cmd.py` it is `str(job.id)`.
    RENAME `test_full_uuid_returns_uuid` — it now returns a string, so the name
    states the opposite of what it asserts. Name it for the property it really
    pins: a full UUID resolves to its own canonical string form.
    Do NOT weaken the uppercase test. Its point is that the RESOLVED id is
    canonical lowercase, and that property survives this change; asserting
    against `shouted` instead of `str(job.id)` would delete the test's reason to
    exist.

──────────────────────────────────────────────────────────────
CONSTRAINTS

 1. Apply every authored slice BYTE FOR BYTE. If a slice or a gate looks wrong,
    apply it as given and DECLARE the defect in the handback. Never repair a
    slice. Two of this block's predecessors carried gate defects the worker
    caught; that is the most valuable thing a handback contains.
 2. Change-set discipline: no path outside the list above. The list bounds
    WRITES; it does not bound the reads, probes or worktrees you need.
 3. `.agent/plan.md` stays under 50 lines (AGENTS.md); the PLAN slice was
    measured against that cap before emission.
 4. Both appends are to files ending with exactly ONE newline at `ce08cfd0`,
    measured: `.agent/live_review.md` at 904283 bytes and
    `.agent/prose_slips.md` at 101682 bytes. Derive each append recipe from its
    own target's terminal byte; never copy one recipe to the other.
 5. Slice shapes, classified before emission: DONE0814, GATE_R9 and the three
    SLIPs are all APPENDS with no FROM; PLAN is a whole-file REWRITE with no
    FROM. No pair in this block has a FROM, so no containment test applies and
    no FROM-zero count is ordered anywhere.
 6. THE `Landed: R-0814` LINE AT `.agent/live_review.md` IS NOT TOUCHED. The
    record is append-only (§3 item 20), and the DONE0814 paragraph is appended
    at the END of the file like every other paragraph. Do not splice, do not
    delete, do not rewrite that line.
 7. C2 appends DONE0814 FIRST and GATE_R9 SECOND. That order is the one §4 item
    4 fixes — findings and their resolutions before verdicts — and the round-3
    entry of this same ledger records it being applied.
 8. `git status --porcelain` is EMPTY at the handback. Every destructive check
    runs in a disposable `git worktree`, never in the primary checkout
    (self-drive protocol G5).
 9. AGENTS.md throughout: self-review loop before every commit, 500-insertion
    cap counting INSERTIONS only, push after committing, no force push, no work
    on `main`, no merge, no pull request.

──────────────────────────────────────────────────────────────
DONE WHEN — eight gates, each RUN and its real exit code recorded

G1 TRANSPORT — one digest. `sha256sum .agent/authored/f260-r10.md` equals the
   digest named in the delegation that carried this block, and the same digest
   over `.agent/last_block.md`. One reading, not a chain. Per §3 item 37 this
   covers the saved copy and its mirror and is not a claim about emitted bytes.

G2 THE RECORD — full byte forensics on the two-paragraph append.
   (a) EXACT IMAGE, not a length check: the post-image at C2 EQUALS
       `pre + b"\n" + DONE0814 + b"\n\n" + GATE_R9 + b"\n"` byte for byte, where
       `pre` is the file at `ce08cfd0`. State the measured length beside it.
       This gate is worded as an equality ON PURPOSE: round 9's version asked
       for a length plus a prefix, and neither of those can reject a same-length
       byte substitution, so its negative control could not pass in any round.
   (b) STRUCTURAL, independent of (a): split the post-image on `"\n\n"`; the
       last TWO units, with the file's terminating newline stripped from the
       final one, equal DONE0814 and GATE_R9 IN THAT ORDER. Units run 428 → 430.
   (c) NEGATIVE CONTROL on the FIRST appended paragraph (§3 item 36): flip ONE
       byte inside DONE0814 as it sits in the post-image and confirm readings
       (a) and (b) BOTH reject it. Restore and confirm both accept again.
   (d) POPULATIONS after C2: `^Gate: ` headers 19, all distinct;
       `^- R-\d{4} — ` registrations 299 over 299 distinct ids;
       `^Done: R-\d{4} — ` lines 5 over THREE distinct ids;
       `^Landed: R-0814 — ` still exactly 1, byte-identical to `ce08cfd0`.

G3 THE SLIPS. The post-image EQUALS
   `pre + b"\n" + SLIP4 + b"\n\n" + SLIP5 + b"\n\n" + SLIP6 + b"\n"` byte for
   byte; blank-line units run 134 → 137, a rise of exactly THREE, one per slip.

G4 THE PLAN. `.agent/plan.md` equals the PLAN slice plus exactly one trailing
   newline, byte for byte, and its line count is under 50.

G5 THE RESOLVER CONTRACT, read from the SHIPPED function with
   `REMEDY_DATA_DIR` at a scratch directory.
   (a) TYPE: `resolve_job_id` returns an instance of `str` and never of `UUID`,
       for BOTH the full-id form and the unique-prefix form. Assert on
       `isinstance`, not on the annotation — an annotation is not a behaviour.
   (b) CASE: an UPPERCASE full uuid resolves to the canonical LOWERCASE string.
       This is the property the uppercase test exists for and the one a naive
       `return raw` silently destroys.
   (c) EXIT CODES UNCHANGED: an ambiguous prefix still exits 2, an unmatched
       prefix and an invalid string still exit 1.
   (d) THE LOADER TAKES BOTH: with a classic job on disk, `storage.load_job`
       returns the same `Job` for `job.id` (a `UUID`) and for `str(job.id)`.
       NON-VACUITY: assert the two returned records are equal AND that the id
       really was passed in two different types, so a loader that ignored its
       argument could not pass.

G6 THE SUITES, run SERIALLY, each exit code recorded separately. Every one of
   these was GREEN at `ce08cfd0` when the reviewer ran it, so any red is this
   round's:
     `pytest tests/test_data_paths.py tests/cli/test_patch_cmd.py -q -p no:randomly`
     `pytest tests/cli/ -q -p no:randomly`
     `pytest tests/ui_server/test_command_channel.py
      tests/ui_server/test_live_state.py tests/orchestration/test_test_runner.py
      -q -p no:randomly`                                    (262 passed at base)
   The second group carries the canary `tests/cli/test_golden_path.py`. The
   third group is here BECAUSE the reviewer's parallel probe reddened it: run
   serially it is green, and this round must show that it stays green. Also run
   `python3 -m apps.cli.grouped integrity check --json` and record `passed`,
   `fail_count` and the check count.

G7 THE MUTATION RED-PROOF, in a disposable `git worktree` at the C4 commit,
   `__pycache__` purged, `python3 -B`, and the module confirmed to resolve from
   THAT worktree before any colour is trusted.
   (i)   UNMUTATED CONTROL FIRST in that worktree, over
         `tests/test_data_paths.py tests/cli/test_patch_cmd.py`: record exit
         code AND passed count. A colour with no baseline is not evidence.
   (ii)  Change the parse path to `return raw` (dropping the normalisation).
         The uppercase test must FAIL. Name the failing node id.
   (iii) Change `resolve_job_id`'s prefix path back to `return UUID(matches[0])`.
         At least one type assertion of G5(a) must FAIL. Name the node id.
   (iv)  Restore after EACH mutation and confirm the control is green again, and
         confirm `git diff` in that worktree is empty after the last restore.
   Name each revert target by PATH and verify the bytes you replace occur
   EXACTLY ONCE in that file before editing (§3 item 25).

G8 LINT AND CLEAN TREE. `ruff check` over exactly the six change-set paths under
   `packages/`, `apps/` and `tests/` exits 0 — the reviewer measured that
   file-scoped reading green at the base, while `ruff check packages/` is RED
   there with pre-existing errors that are not this feature's, which is why the
   gate is file-scoped. Then `git status --porcelain` and
   `git ls-files .remedy-wt` are both EMPTY.

──────────────────────────────────────────────────────────────
HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, `SESSION 3 of feature F260`, branch, commit SHAs, the changed-files table
with its `+/-` column read from `git diff --numstat` and never re-derived by eye
(§3 item 28), ONE LINE PER GATE with its real exit code, the open-findings count
BY DISTINCT ID, and the next expected action. No length cap applies. Declare
every deviation, including any place this block is wrong.

──────────────────────────────────────────────────────────────
AUTHORED SLICES

A slice is the bytes of the lines strictly BETWEEN its BEGIN and END marker
lines, joined by `"\n"`, carrying NO trailing newline. The marker lines are
never part of any slice and never reach any file.

<<<BEGIN DONE0814>>>
Done: R-0814 — RESOLVED at F260 R9, and the reviewer verified all three of the fix conditions this finding carries rather than reading them from the handback. FIRST, no module-local `_jobs_dir` in `packages/orchestration/pingpong_job.py`: `hasattr(pingpong_job, "_jobs_dir")` is False and the AST reading finds zero references, landed at R8 in `b92d096f`. SECOND, every evidence path is built from the same directory function as the record path: at `01c8c692` both `data_paths.job_record_path` and `data_paths.job_evidence_dir` are built on `data_paths.job_dir`, and `pingpong_job._persist_job` writes through the first while `pingpong_job.job_evidence_dir` returns the second, so the split root that produced this finding no longer has two roots to disagree about. THIRD, a test asserts that a job's record and its evidence resolve under one root: `test_a_persisted_pingpong_job_writes_its_record_under_its_own_job_dir` in `tests/test_data_paths.py` runs the SHIPPED writer, reads the bytes it left, and asserts `written == data_paths.job_record_path(job.job_id)` and `pingpong_job.job_evidence_dir(job.job_id).parent == data_paths.job_dir(job.job_id)` — a reading of the writer rather than a comparison of two accessors, which is what the accessor-only tests of R6 and R7 could not give. THE REVIEWER'S OWN MUTATION PROOF, run in a disposable worktree at `01c8c692` with the module confirmed to resolve from that worktree: the unmutated control is exit 0 at 46 passed; pointing `data_paths._task_job_id_matches` back at a literal `task_jobs` directory reddens `test_a_pingpong_record_in_the_jobs_dir_is_still_resolvable_beside_a_classic_one` with the exact stderr `Error: no job matches prefix '0123456789abcdef'`, which is the `remedy teach narrate` regression of 2026-08-25 reproduced on demand and the reason the writer and its reader had to move in ONE commit; making `_persist_job` write to `jobs_dir() / job.job_id / "record.json"` reddens the one-root test AND, unpredicted by the round-9 block, `test_no_module_that_owns_job_evidence_spells_the_path_itself[packages.orchestration.pingpong_job]`, because that mutation injects a `jobs_dir` reference into a module the round-7 guard forbids to hold one — which is that guard demonstrating from the other side that it is live and that the R9 change genuinely does not trip it. The control was green again after each restore. NOT CLAIMED HERE: the classic store `<data_root>/jobs/<uuid>.json` still exists beside the moved record, and `<data_root>/jobs/` now holds both `<uuid>.json` FILES and `<16hex>/` DIRECTORIES; the two are told apart by `_classic_job_id_matches` globbing `*.json` and `_task_job_id_matches` requiring a directory holding a `job.json`, proved by a test that plants both shapes plus a `job.json`-less directory in one directory and resolves each to exactly one match. Deleting the classic store is F260 T004's work and is not part of this resolution.
<<<END DONE0814>>>

<<<BEGIN GATE_R9>>>
Gate: R9 — the F260 R9 entry. R9 MOVED THE PING-PONG RECORD UNDER THE ONE JOBS ROOT AND RESOLVED R-0814. VERDICT PASS. Range 1523fde1..ce08cfd0, eight commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; largest insertion count 400, a single `.agent/**` state write, and largest code commit 76, both under the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback's numbers, and reproduced every number the worker reported. TRANSPORT: one digest `746c9953166920d3a6304bb115e47334ab07fb1db3916a0c9f658b83272c71c7` across the reviewer's scratch original, the saved copy at `.agent/authored/f260-r9.md` and the mirror at `.agent/last_block.md`, with `cmp` silent for both pairs; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into the prompt. THE RECORD: 898817 bytes to 902842 at C2, a growth of 4025 equal to a newline plus the 4023-byte slice plus a newline, with the post-image EQUAL to the pre-image plus that exact append and the last blank-line unit equal to the slice byte for byte; then to 904283 at C5, a growth of 1441 for the 1439-byte `Landed:` line the worker measured and reported. Blank-line units ran 426 to 427 to 428. Registrations 299 over 299 DISTINCT ids, `Done:` lines 4 over only TWO distinct ids, eighteen `Gate:` headers, and `Landed: R-0814` exactly once. THE SLIPS: 97989 to 101682 bytes, an image EQUAL to the pre-image plus the three slices with two-newline separators, units 131 to 134 — a rise of exactly THREE, one per slip. THE MOVE IS COMPLETE. By AST over 1030 tracked Python files under `packages/`, `apps/` and `tests/`, references resolving to exactly `task_jobs_dir`, `task_job_dir` or `task_job_record_path` number ZERO, against a non-vacuity control of 76 for `job_dir`; `hasattr(data_paths, n)` is False for all three deleted names and True for the five survivors; and with a scratch root, `job_dir`, `job_record_path`, `job_evidence_dir` and `run_dir` all honour a `root` argument set to a different directory from the environment root. THE SUITES, re-run serially by the reviewer, all exit 0 at 93, 165 and 186 — 444 tests — with the canary among them, and `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks. The count of 93 is unchanged from the base because C4 deleted the two task-layout tests whose functions no longer exist and C5 added two, leaving `tests/test_data_paths.py` at 42 test functions before and after. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY, in the reviewer's own disposable worktree at `01c8c692` with both modules confirmed to resolve from it: control exit 0 at 46 passed; the matcher pointed back at `task_jobs` reddens exactly the resolvability test with `Error: no job matches prefix`; the writer moved off `job_record_path` reddens the one-root test and also the evidence-owning guard; and `git diff` was empty after each restore with the control green again. RUFF over exactly the fourteen changed paths exits 0, scoped to files because `ruff check packages/` and `ruff check tests/orchestration/` are red at the base with pre-existing errors that are not this feature's. TWO GATE CLAUSES WENT RED AND BOTH ARE THE REVIEWER'S DEFECTS, NOT THE WORKER'S, and the reviewer reproduced both. G2(c) demanded that a byte flip be rejected by reading (a) as well as by reading (b), but (a) was worded as a length equality plus a prefix test and a same-length substitution changes neither, so no run could satisfy it; the protection was intact throughout because (b) rejects the flip, and the round-10 block rewords (a) as an exact-image equality. G5(c) required the literal `task_jobs` to occur zero times under `packages/`, `apps/` and `tests/`, while the SAME block's SPEC ordered a test asserting the record is not filed under a `task_jobs` component — an assertion that must contain the literal. All three surviving occurrences are inside that ordered test in `tests/test_data_paths.py` and there are ZERO anywhere else, so the move itself is complete and only the gate was unmeetable; it is §3 item 2, the self-counting gate, written by the checklist's own author. THE WORKER DECLARED EIGHT DEVIATIONS AND EVERY ONE IS UPHELD; three are worth the record. It applied the SPEC and refused to reword the test to shrink the count a reviewer gate demanded, which is the correct precedence and the reason the defect is visible at all. It found two stale sites the block's own list missed, both inside files the block already named — a comment calling four names "FOUR DIFFERENT names" where the deletion leaves three, and a docstring naming the deleted `task_job_dir` — and corrected the numeral with the list, which is §3 item 16 applied by the worker to the reviewer's omission. And its G7(iii) run reddened a second, unpredicted test, which it recognised as the evidence-owning guard proving itself live rather than as a failure of its own change.
<<<END GATE_R9>>>

<<<BEGIN SLIP4>>>
2026-09-06 · F260 R9 (reviewer) · Gate G2(c) of the round-9 block ordered a negative control no run could satisfy: it required a byte flipped inside the appended paragraph to be rejected by reading (a) AS WELL AS reading (b), while reading (a) was worded as "length equals pre plus the slice plus two newlines, and the pre-image is a byte-exact PREFIX". A same-length byte substitution inside the appended region changes neither the length nor the prefix, so (a) accepts it by construction. The reviewer reproduced this independently at offset 898918 of the C2 post-image: (a) accepts, (b) rejects, and both accept again after the restore — so the record was protected the whole time by the structural reading alone. THE LESSON: a byte-level reading of an append must be an EXACT IMAGE equality against `pre + separator + slice + terminator`, never a length plus a prefix, because the two properties a prefix test fixes are the two a substitution leaves alone. This is the gate-that-cannot-pass face of §3 item 33's "the gate that cannot fail and the gate that cannot pass are the same defect wearing two faces", and the round-10 block rewords the clause as an equality. Reviewer-authored unsatisfiable gate clause; the property it guarded was measured intact, and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP4>>>

<<<BEGIN SLIP5>>>
2026-09-06 · F260 R9 (reviewer) · Gate G5(c) of the round-9 block required the literal `task_jobs` to occur ZERO times under `packages/`, `apps/` and `tests/`, while the SAME block's SPEC for C5(A) ordered a test asserting "the record is NOT under any path containing a `task_jobs` component" — an assertion that cannot be written without the literal it forbids. The worker applied the SPEC, declared the contradiction, and did NOT reword the test to make the gate green, which is the correct precedence and the only reason the defect is visible. Measured at `ce08cfd0`: all three surviving occurrences sit in `tests/test_data_paths.py` at lines 396, 414 and 415, inside that ordered test and its docstring, and there are ZERO anywhere else under the three roots, so the record move itself is complete and only the gate was unmeetable. THE LESSON is §3 item 2 verbatim — a "must be 0" done-when may not count a string that the same block writes into that same file — and it was broken by the author of the checklist that carries it, over a SPEC rather than over a slice, which is the form item 2 does not name. Scope such a count to the files the block does not write, or assert the absence over the module under change rather than over a directory the block's own test lives in. Reviewer-authored self-counting gate; the load-bearing property holds and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP5>>>

<<<BEGIN SLIP6>>>
2026-09-06 · F260 R9 (reviewer) · Gate G1 of the round-9 block ordered the saved copy's digest compared against "the digest in this block's BEGIN marker", and the block carried no such marker: its only BEGIN markers delimit the five authored slices and none of them states a digest. The worker declared it and used the digest the delegation itself carried, which is the value the reviewer actually supplied and computed over the same bytes, so the transport proof is sound and one reading short of nothing. THE CAUSE is a phrase carried forward from the two-window relay of docs/agents/planner_reviewer_prompt.md §4 item 9, where the reviewer emits a hash-stamped BEGIN marker into a paste block; under docs/agents/self_drive_protocol.md there is no paste block and the digest travels in the delegation instead, which §3 item 37 already says in as many words. A block that names the artefact carrying its own digest must name the one this workflow actually produces. Reviewer-authored stale pointer in a gate; the gate ran against the correct value and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP6>>>

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 9 are reviewed and 2 to 9 PASSED. T001 is
CLOSED. T002 is open: the record has MOVED and finding R-0814 is resolved; what
remains of T002 is the one resolver over it.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

THE RESOLVER RETURNS A STRING. `data_paths.resolve_job_id` is annotated and
returns `str` instead of `UUID`, and `storage.load_job` / `load_job_safe` accept
either. DECISION F260 D4 named this the one thing standing between the two
resolvers and a collapse into one. Measured in a worktree before the round: the
change costs FIVE tests, every one asserting the return type, and ZERO
production call sites, because `load_job` formats its path from the id.

## Next Steps

- COLLAPSE the two resolvers into one, now that they share a return type: one
  `str`-returning function over both stores, the loser deleted in the same
  commit. Finding R-0809 — four wordings for "unknown id", and a real id of the
  other store rejected — belongs here.
- Then `runs/<run_id>/` keyed by run id, replacing `pingpong_runs/`.
- Then T003 consumer by consumer, T004 the classic runner and the classic
  store, T005 the reachability test and the cluster deletion.

## Risks

- Widening what `resolve_job_id` accepts changes an ERROR path: an id of the
  other store today exits 1 with "no job matches prefix" and would instead
  reach `load_job` and raise. That is R-0809's territory and needs its own test.
- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer.
- `<data_root>/jobs/` holds both `<uuid>.json` files and `<16hex>/` directories.
  Any new reader of that directory must make the same file/directory
  distinction the two matchers make.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLAN>>>

──────────────────────────────────────────────────────────────
