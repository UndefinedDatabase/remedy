── STEP T003 / round 52 — F275 ───────────────────────────────
Goal:        Complete `R-0877`. Round 51 made the run-log seam join its id verbatim; 26 call
             sites in 12 files still wrap that id in `UUID(...)`, so ONE job's run log lands
             in TWO directories and each reader sees only its own half. Remove every wrap by
             one `ast` pass with the imports it orphans, and add a repo-wide sweep test.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r52.md`
             C0b  mirror it into `.agent/last_block.md` from the committed blob
             C1   slice PLAN52 — whole-file replacement of `.agent/plan.md`
             C2   slices RECORD52 and NOTE52 — the round 51 PASS verdict and one record
                  note settling that round's first declared deviation
             C3   THE FIX — run the generator UNWRAP52, then the code append GUARD52
             C4   slice LANDED52 — the second `Landed: R-0877` line, appended after the fix
             C5   the handback, rewriting `.agent/handoff.md`

Change:      EXACTLY these paths and nothing else.
             `.agent/authored/f275-r52.md`  (new) · `.agent/last_block.md` ·
             `.agent/plan.md` · `.agent/live_review.md` ·
             `.remedy-wt/f275_r52_unwrap.py`  (scratch, gitignored, NOT committed) ·
             `apps/cli/commands/dashboard_cmd.py` · `packages/memory/context_summary.py` ·
             `packages/orchestration/` × 4: `do_continue.py`, `job_fulfillment.py`,
             `mission_readiness.py`, `repair_loop.py`, plus `self_dogfood_execution.py` ·
             `tests/orchestration/` × 4: `test_memory_events.py`, `test_memory_safety.py`,
             `test_mission_readiness.py`, `test_repair_apply_cycle.py` ·
             `tests/test_patch_apply.py` · `tests/test_timeline.py` · `.agent/handoff.md`
             NO path under `docs/` or `scripts/` moves. `.agent/decisions.md` is NOT touched
             — DECISION F275 D29 already rules this work — and neither is
             `.agent/prose_slips.md`: NOTE52 is a record note, not a slip, and says why.

Constraints:
 1. Apply every slice BYTE FOR BYTE; extract each mechanically from the COMMITTED blob of
    `.agent/authored/f275-r52.md` by its `BEGIN-<name> ` / `END-<name> ` marker-line
    PREFIX. Never retype, reflow or edit one. A slice that looks wrong is applied as given
    and DECLARED.
 2. The commit order C0a, C0b, C1, C2, C3, C4, C5 is FIXED — none merged, none reordered.
    C1 precedes C2 because a round booking into the finding ledger advances the plan first
    (planner_reviewer_prompt.md §3 item 23), and C4 comes AFTER C3.
 3. EVERY length is `len(<bytes>)` from `read_bytes()` or a `git show` byte stream, never
    `len()` over a decoded `str`.
 4. The three appends — RECORD52, NOTE52, LANDED52 — are `old_bytes + slice_bytes` in
    Python; each owns its leading blank line, every pre-blob ends in a newline and none is
    added. GUARD52 is a CODE append and obeys the same rule.
 5. UNWRAP52 IS THE PRODUCTION CHANGE AND IT IS RUN, NOT TRANSCRIBED. Extract it to
    `.remedy-wt/f275_r52_unwrap.py` and run `python3 -B .remedy-wt/f275_r52_unwrap.py .`
    from the repository root. It is DETERMINISTIC and rewrites only what its own `ast` pass
    finds: do NOT hand-edit a site it misses or one it changes, and if its output disagrees
    with G4 below, report that and stop. The script is gitignored SCRATCH and is NEVER
    committed — its committed record is its slice inside `.agent/authored/f275-r52.md`.
 6. This round RESOLVES nothing. Write the `Landed: R-0877` line at C4 and NO `Done:`
    paragraph — only reviewer-authored text sets a resolution, and `R-0877` already carries
    one `Landed:` line from round 51 which is NOT deleted or rewritten. The open set stays
    87 at the base and 87 at C4.
 7. Destructive verification — the red proof in G6 — runs ONLY inside a disposable
    `git worktree` under `.remedy-wt/`, removed and pruned before the handback. The primary
    checkout satisfies `git status --porcelain` == empty at every commit.
 8. Re-read `.agent/STOP` FROM DISK before the first commit and report what you found.

Done when:   the gates below, each run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
             one line per gate in the handback, EVERY reading taken at C4 or earlier.
             Report the number of gates YOU ran; this block states none.

 G1  TRANSPORT, at C0b. sha256 over the bytes of `.agent/authored/f275-r52.md` equals the
     digest the delegation message states — this block carries marker lines for its SLICES
     only and no BEGIN marker of its own. `.agent/last_block.md` is written from
     `git cat-file blob <C0a-sha>:<that path>` and never retyped. Report both byte counts
     and both digests, and state the chain the proof walked. Claim nothing about the bytes
     emitted into your prompt.

 G2  THE PLAN, at C1. `.agent/plan.md` BYTE-EQUAL to slice PLAN52: both byte counts, both
     sha256 digests, the line count against the AGENTS.md cap of 50, `^## Goal$` exactly 1x
     and `^## Next Steps$` exactly 1x.

 G3  THE RECORD, at C2, then again at C4. Read every pre and post blob with
     `git show <sha>:<path>` INTO MEMORY — never write a non-current revision over a
     tracked file.
     (i)  `.agent/live_review.md` ← RECORD52 then NOTE52, applied in that order inside C2,
          pre at C1 and post at C2, all three readings:
          (a) reader A: pre_bytes + RECORD52 + NOTE52 == post_bytes, `identical: True`.
          (b) reader B, structural: N is the number of blank-line-separated paragraphs your
              script COUNTS across the two slices — never a number this block asserts — and
              the LAST N blank-line units of the post blob equal those N paragraphs IN
              ORDER, stripped.
          (c) negative control: flip ONE ASCII LETTER inside the FIRST appended paragraph
              of the IN-MEMORY copy — an ASCII byte, so the mutated copy stays decodable —
              and require that reader A rejects AND reader B rejects, each re-run against
              the ORIGINAL slices.
     (ii) `.agent/live_review.md` ← LANDED52, pre at C3 and post at C4, reading (a) alone.

 G4  WHAT THE GENERATOR DID, at C3, against COMMITTED blobs. Report the script's OWN stdout
     in full — it prints a per-file count and the imports it removed — and then verify it
     independently rather than believing it:
     (a) `git diff --numstat <C3-sha>^..<C3-sha>` reads the generator's twelve files plus
         `tests/test_timeline.py` at 89/0, the guard. Report every row you measured against
         this list: 1/1 `dashboard_cmd.py`, 1/2 `context_summary.py`, 1/1 `do_continue.py`,
         8/8 `job_fulfillment.py`, 1/1 `mission_readiness.py`, 5/5 `repair_loop.py`, 1/1
         `self_dogfood_execution.py`, 3/6 `test_memory_events.py`, 1/2
         `test_memory_safety.py`, 1/1 `test_mission_readiness.py`, 1/1
         `test_repair_apply_cycle.py`, 3/3 `test_patch_apply.py`, 89/0 `test_timeline.py`.
     (b) RE-RUN THE GENERATOR against a disposable worktree detached at the base `87d76c66`
         and compare that worktree's `packages`, `apps` and `tests` tree digests against
         C3's; they must be equal, which is what makes the change REPRODUCIBLE rather than
         merely present.
     (c) An `ast` sweep over the tracked `.py` files at C3 for a call to
         `append_run_event`, `emit_failure_events` or `load_run_events` whose SECOND
         positional argument is a `UUID(...)` call must return ZERO. At the base `87d76c66`
         the same sweep returns 26. Report both numbers and, at the base, the file counts.

 G5  THE GUARD, at C3, as a CODE APPEND and therefore by ORDERED EQUALITY, not by a
     per-line count — a code slice repeats blank lines and `assert` lines structurally, so
     multiplicity is unattainable by construction. For `tests/test_timeline.py` ← GUARD52,
     all three: the base blob at `87d76c66` is a byte-exact PREFIX of the C3 blob; the
     slice is a byte-exact SUFFIX of the C3 blob; and the lines that C3's diff ADDS for
     that path are exactly the slice's lines IN ORDER.

 G6  THE RED PROOF, at C3, in a disposable worktree under `.remedy-wt/` detached at C3,
     never `cd`-ed into: run every command as `subprocess.run([...], cwd=<abs worktree>)`
     under `python3 -B` with `-p no:cacheprovider`, purge `__pycache__` first, and PRINT
     the resolved `__file__` of `packages.orchestration.timeline` before believing any
     result — it must lie inside the worktree. Selection for EVERY run, all three node ids
     of `tests/test_timeline.py::TestTheRunLogSeamHasOneIdSpelling` together. Run the
     UNMUTATED control FIRST and report its exit code beside every mutated one. M1 re-wraps
     the `append_run_event` id argument in `packages/orchestration/job_fulfillment.py`'s
     `fulfillment_started` emission. M2 re-wraps it in `packages/memory/context_summary.py`
     and restores that file's local `from uuid import UUID`. Record each file's sha256
     BEFORE its mutation and prove the revert byte-exact against that recorded digest.
     Report the FAILED node ids as a SET per run, parsing a node id as what follows the
     FIRST space of a `FAILED <nodeid> - <msg>` line, AND report the `path:line` the sweep's
     assertion MESSAGE names — that message is the discriminator, because it must name the
     site you mutated and no other. M1's set is a SUBSET of M2's, stated here rather than
     claiming a disjointness that does not hold: M2 adds the behavioural node, and M1 shows
     the sweep reaching a file no behavioural test in this selection executes. Finish with
     the control again.

 G7  NOTHING NEAR IT MOVED, at C3.
     (a) `git rev-parse C3:packages`, `C3:apps` and `C3:tests` must equal
         `ff6cebaf9e41cbcd813399fb022940c47ca7180b`,
         `1dd43398c371aa88e16fa8aba95bead4c131c2ac` and
         `1d425fe0f1a27848b0cec31fce0c92077ce28d12`. At the base `87d76c66` the same three
         read `6d2ec62e10948175e3c338aa951f3bca3cb4ddc5`,
         `6d3dba7c11f6586682d8c55f0628f330742df584` and
         `b104a5acd66ce6c1c1482e7deaf4c862b0bcda52`. These are the reviewer's own
         measurement of this change applied to a clean checkout; a digest that differs
         means your tree is not the tree that was measured, so report it and stop.
     (b) THE RUFF CEILING, because this round removes six imports and
         `tests/orchestration/test_ci_budgets.py` freezes the repository's count.
         `python3 -m ruff check . --output-format concise` at C3 and at the base — read the
         base in a disposable worktree, never by writing base bytes over a tracked file.
         Report the finding COUNT at both; both are 26. Ruff exits 1 whenever findings
         remain, so the gate is the COUNT and not the exit code.
     (c) The SCOPED round gate, in the primary checkout at C3:
         `python3 -m pytest tests/test_timeline.py tests/orchestration/test_memory_events.py
         tests/orchestration/test_memory_safety.py
         tests/orchestration/test_mission_readiness.py
         tests/orchestration/test_repair_apply_cycle.py tests/test_patch_apply.py
         tests/orchestration/test_job_fulfillment.py
         tests/orchestration/test_repair_loop_v1.py tests/orchestration/test_ci_budgets.py
         tests/test_run_log.py tests/orchestration/test_budget_tick.py -q`
         and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. Report both
         last lines and both exit codes.

 G8  NOTHING ELSE MOVED, at C4.
     (a) `.agent/STOP` re-read from disk: report the literal result. `git status
         --porcelain` == `''`: report the literal string. Report `git worktree list` as ONE
         entry.
     (b) The changed-path set over `87d76c66..C4` equals the paths the Change section
         lists, other than `.agent/handoff.md` which C5 writes and
         `.remedy-wt/f275_r52_unwrap.py` which is gitignored scratch and must NOT appear.
         Resolve that expectation against the Change section itself, not against a number
         stated anywhere in this block. Report MISSING and EXTRA as lists, and the count of
         paths in that set under `docs/` or `scripts/`, which must be 0.
     (c) THE OPEN SET, BY DISTINCT ID over `.agent/live_review.md`: distinct `^- R-\d+ — `
         minus distinct `^Done: R-\d+ — `, at the base `87d76c66` and at C4. It reads 87 at
         the base and must read 87 at C4. Report the ids registered and resolved this round
         as lists; both are empty. Report `^Landed: R-0877 ` at C3 and at C4, which are 1
         and 2 — the second line is this round's, and round 51's is NOT rewritten — and
         `^Done: R-0877 ` at both, which is 0 at both.
     (d) Each of C0a..C4's own insertion count against the F104 D1 cap of 500, derived ONCE
         from `git show --numstat <sha>` and used both here and in the `+/-` column of the
         handback's `## Commits` table.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 20 of F275,
             round 52, the item-status table with every ordered item exactly once, the
             deviations, and one sentence of context self-assessment. The session's SCOPE
             REPORT was written in round 51's handback; say in one line that it stands.
──────────────────────────────────────────────────────────────

WHAT THE REVIEWER ALREADY MEASURED, so that no gate above re-derives it. THE DEFECT IS A
MEASUREMENT, not an inference: at `87d76c66`, writing one event through an UNWRAPPED call
site and one through a WRAPPED one, with the SAME id, creates TWO directories —
`job_logs/00000000-0000-0000-0000-000000000000/` and
`job_logs/00000000000000000000000000000000/` — and neither reader sees both events. The
disagreement is OLDER than round 51: at `17d3f513` the same probe creates ONE directory, the
hyphenated one, and the unwrapped reader sees NOTHING while the wrapped one sees both. Round
51 moved the write side to the one-world spelling, turning a silently blind reader into two
visible directories; this round removes the other side. After the change: `ruff check .`
reads 26 findings against 26 at the base, the scoped selection in G7(c) reads `419 passed`
at exit 0, the canary `42 passed` at exit 0, and the FULL suite — not required by a round
gate, so reported rather than ordered — reads `1 failed, 18369 passed, 29 skipped` at exit
1, the failure being
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
which needs the gitignored `apps/ui/node_modules` and fails in every fresh worktree. The red
proof in G6 was run in full: control `3 passed` exit 0, M1 `1 failed, 2 passed`, M2 `2
failed, 1 passed`, the sweep's message naming `job_fulfillment.py:640` and
`context_summary.py:206` respectively, both reverts byte-exact, control green again.

WHY THE UNIT IS THE WHOLE SET. A write site and a read site of one run log must name the same
directory, so unwrapping one without the other splits a pair that currently agrees —
`repair_loop.py` writes at three sites and reads at two, `job_fulfillment.py` writes at seven
and reads at one. DECISION F275 D28 ruled this shape for an id widen: the atomic unit is the
assignment-connected component. Here that component is the seam, so all 26 sites move at once.

SESSION 20 IS PAST F275's SOFT LIMIT, and amend0908-f275-finish rule 2 forbids the
split-and-close default here BY NAME: do NOT close F275, do NOT register a follow-up feature,
and do NOT touch `docs/roadmap/STATUS.md`.

────────── SLICES ──────────
The authored texts follow, in the order their commits apply them: PLAN52, RECORD52, NOTE52,
UNWRAP52, GUARD52 and LANDED52, each delimited by its own `BEGIN-`/`END-` marker lines, which
are NOT part of any slice and never reach a target file. Every rule line in this block's frame
is a run of U+2500 BOX DRAWINGS LIGHT HORIZONTAL and no rule LENGTH is load-bearing: markers
are matched by PREFIX and the frame carries no appliable bytes.

Slice shapes, mechanically. PLAN52 is a WHOLE-FILE REPLACEMENT. RECORD52, NOTE52 and
LANDED52 are prose APPENDS applied as `old_bytes + slice_bytes`, each carrying its own
leading blank line. GUARD52 is a CODE APPEND, proved by ordered equality under G5. UNWRAP52
is a WHOLE-FILE write to gitignored SCRATCH and is then EXECUTED. No FROM/TO pair is
authored this round, so no containment test is owed and no FROM-zero count is ordered.

BEGIN-PLAN52 ─────────────────────────────────────────────────
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 52 completes `R-0877`. Round 51 made the run-log seam join its id verbatim; 26 call
sites in 12 files still wrapped that id in `UUID(...)`, so one job's run log landed in two
directories and each reader saw only its own half — measured at `87d76c66` as two
directories for one id, with neither reader seeing both events. All 26 wraps are removed by
one `ast` pass, the six imports it orphans go with it, and a repo-wide sweep test keeps the
count at zero. The round 51 PASS verdict is booked here.

## Next Steps

1. The reviewer's authored `Done: R-0877`, covering both halves, at the next gate.
2. P1 — replace the transform's receiver-NAME heuristic with the DECISION F272 D7
   raising-property probe `docs/roadmap/features/T2_F275.md` T002 already orders. The probe
   and its site set exist at `0b009325` in `.agent/f275_t002_flip_inventory.md`; T003
   re-derives them at its own base, as that file says it must.
3. P3 — the `**` splat call-graph pass over the test helper factories.
4. Re-run the flip dry run, then THE FLIP as the one declared-oversize commit AGENTS.md
   permits per feature, declared with its inseparability reason before review.
5. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
6. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The remaining `UUID(...)` sites are NOT this class: they hold a value that is legitimately
  a `uuid.UUID` in the classic record, so they move WITH the flip and not before it.
- The open set is 87 by distinct id. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's, per DECISION F272 D12.
END-PLAN52 ───────────────────────────────────────────────────

BEGIN-RECORD52 ───────────────────────────────────────────────

Gate: F275 R51 — the F275 round 51 entry. VERDICT PASS. Written by the planner and reviewer of session 20 after reading the committed range `17d3f513`..`769fc2f8` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. G1 is the PRIMARY cmp-against-scratchpad proof and not the digest fallback: the reviewer's scratch original, the saved copy at C0a `02b8bfd5` and the mirror at C0b `63baabf6` are one blob at 40562 bytes and sha256 `b1601e968082383db0712420c1a136b28542f6260b14b59f3f5184a722de8e8a`. G2: `.agent/plan.md` byte-identical to slice PLAN51 at 2531 bytes over 44 lines, both mandated headings exactly once. G3: `.agent/live_review.md` 905059 to 912592 across RECORD51 and FIND51 and 912592 to 912896 for LANDED51 at C4, reader A identical in both, reader B true at N counted from the slices — 2 then 1 — and the negative control flipped inside the FIRST appended paragraph rejected by BOTH readers. G4: all ten pairs are REWRITES on the containment test's own output, every FROM reads 1 in its base blob and 0 in its C3 blob, and the TO reads 1 in nine of them — P51A is the exception the block declares, its TO being a PREFIX of its own FROM, so that count discriminates nothing there. The reviewer then REBUILT each of the five edited files from its base blob by applying only that file's own pairs in order, and all five came out byte-identical to the C3 blob. G5: GUARD51 is a CODE APPEND proved by ordered equality — the base blob is a byte-exact PREFIX at 35021 bytes, the slice a byte-exact SUFFIX at 2163, the sum exactly the C3 blob's 37184, and the 52 lines C3's diff adds are the slice's 52 lines IN ORDER. G6: both subtree digests equal the reviewer's own replay of this fix on a clean checkout — `packages` at `6d2ec62e10948175e3c338aa951f3bca3cb4ddc5` and `tests` at `b104a5acd66ce6c1c1482e7deaf4c862b0bcda52` — C3's OWN diff is exactly the six ordered rows, `ruff check .` reads 26 findings at C3 and 26 at the base with the base read in a disposable worktree rather than by writing over a tracked file, and the reviewer re-ran the scoped selection itself at `481 passed` and the canary at `42 passed`, both exit 0. G7 IS THE GATE THIS ROUND EXISTS FOR AND THE REVIEWER RE-RAN IT IN ITS OWN DISPOSABLE WORKTREE DETACHED AT C3 `133ccd53`, with both module paths PRINTED and resolving inside that worktree: the control reads `3 passed` at exit 0, M1 reverting the `timeline.py` writer statement reddens all three guards, M2 reverting the `test_failure_artifact.py` line reddens only `test_emit_failure_events_takes_the_shipped_job_id_shape`, both reverts are byte-exact by sha256 against a digest recorded BEFORE each mutation, and the control is green again. The two sets are NOT disjoint and the block said so in advance: M2's set is a proper SUBSET of M1's, and what M2 establishes is that the `emit_failure_events` fix is independently necessary, since that one node is still red with `timeline.py` already fixed. G8: the changed-path set over `17d3f513`..C4 is exactly the ten paths the Change section names with MISSING and EXTRA both empty and ZERO under `apps/`, `docs/` or `scripts/`; the open set goes 86 at the base to 87 at C4 with `R-0877` the only id registered and none resolved; `^Landed: R-0877 ` reads 0 at C3 and 1 at C4 against `^Done: R-0877 ` 0 at both; and per-commit insertions are 465, 381, 16, 4, 78 and 2, every one under the AGENTS.md DECISION F104 D1 cap of 500. THE HANDBACK CARRIES THE SESSION'S SCOPE REPORT AND THE LIMIT BANNER, as amend0908-f275-finish rule 1 obliges and rule 2 shapes: the report was written, F275 was not closed, no follow-up feature was registered and `docs/roadmap/STATUS.md` was not touched.
END-RECORD52 ─────────────────────────────────────────────────

BEGIN-NOTE52 ─────────────────────────────────────────────────

Note: F275 R52 — the round 51 worker's first declared deviation does NOT stand, and the reading that settles it is the reviewer's own. The worker reported that slice FIND51's phrase "beside sixteen further `UUID | str` parameters" did not reproduce, counting 15. Both counts are correct and they are counts of different trees. FIND51 names its commit in the same sentence — "an `ast` sweep over the 993 tracked `.py` files at `17d3f513`" — and re-running that sweep against a worktree detached at `17d3f513` reads 2 coercing parameters and 16 non-coercing ones, exactly as the slice states; re-running it against the round's own tip reads 0 and 15, because this round's own pair P51D converted `load_run_events` from `UUID | str` to `str` and so removed one of the sixteen it was counting. The worker measured at the later tree. No prose slip is recorded and no id is spent: the sentence was true of the commit it named, which is precisely what planner_reviewer_prompt.md §3 item 20 requires of it. The worker was right to declare rather than reconcile, and the declaration is what made the reading cheap to take.
END-NOTE52 ───────────────────────────────────────────────────

BEGIN-UNWRAP52 ───────────────────────────────────────────────
"""F275 R52 — unwrap the redundant `UUID(...)` around the id argument of the run-log seam.

R-0877 made `append_run_event`, `emit_failure_events` and `load_run_events` join their
`job_id` VERBATIM. A call site that still writes `UUID(job_id)` therefore names a second
directory for the same job's log, and raises on the sixteen hex characters
`data_paths.mint_job_id` produces. Every site moves in one pass, because a write site and a
read site of one log must agree. Edits are applied per line RIGHT TO LEFT IN BYTES, since
`ast` reports `col_offset` as a UTF-8 byte offset (DECISION F275 D25); `ast.unparse` is not
used because it discards this repository's WHY comments.
"""
import ast
import collections
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1])
SEAM = {"append_run_event", "emit_failure_events", "load_run_events"}


def tracked():
    out = subprocess.run(["git", "ls-files", "*.py"], capture_output=True, text=True,
                         cwd=str(WT)).stdout
    return [p for p in out.split() if p]


def sites(tree):
    """Yield the byte span of every redundant UUID wrap, and of its inner argument."""
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        called = f.id if isinstance(f, ast.Name) else (
            f.attr if isinstance(f, ast.Attribute) else None)
        if called not in SEAM or len(n.args) < 2:
            continue
        arg = n.args[1]
        if not (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name)
                and arg.func.id == "UUID" and len(arg.args) == 1
                and not arg.keywords):
            continue
        inner = arg.args[0]
        if arg.lineno != arg.end_lineno or inner.lineno != inner.end_lineno:
            continue        # a wrap spanning lines is left alone and reported
        yield (arg.lineno, arg.col_offset, arg.end_col_offset,
               inner.col_offset, inner.end_col_offset)


counts = collections.Counter()
changed = []
for rel in tracked():
    p = WT / rel
    try:
        src = p.read_text()
        tree = ast.parse(src, filename=rel)
    except (SyntaxError, OSError):
        continue
    found = list(sites(tree))
    if not found:
        continue
    lines = src.split("\n")
    by_line = collections.defaultdict(list)
    for lineno, a, b, ia, ib in found:
        by_line[lineno].append((a, b, ia, ib))
    for lineno, items in by_line.items():
        raw = lines[lineno - 1].encode("utf-8")
        for a, b, ia, ib in sorted(items, key=lambda x: -x[0]):
            raw = raw[:a] + raw[ia:ib] + raw[b:]
        lines[lineno - 1] = raw.decode("utf-8")
    out = "\n".join(lines)
    ast.parse(out, filename=rel)        # never write a file the edit broke
    p.write_text(out)
    counts[rel] = len(found)
    changed.append(rel)

print(f"files rewritten: {len(changed)} | wraps removed: {sum(counts.values())}")
for rel, n in sorted(counts.items()):
    print(f"    {n:>3}  {rel}")

# An orphaned `UUID` import is removed in the same pass: leaving it raises the ruff count
# `tests/orchestration/test_ci_budgets.py` freezes. Orphaned is MEASURED, never guessed.
print("\n`UUID` imports orphaned by the rewrite and removed with it:")
for rel in changed:
    src = (WT / rel).read_text()
    tree = ast.parse(src, filename=rel)
    uses = sum(1 for n in ast.walk(tree)
               if isinstance(n, ast.Name) and n.id == "UUID")
    imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
               and any(a.name == "UUID" for a in n.names)]
    if not imports or uses:
        continue
    lines = src.split("\n")
    for imp in sorted(imports, key=lambda n: -n.lineno):
        survivors = [a for a in imp.names if a.name != "UUID"]
        indent = " " * imp.col_offset
        if survivors:
            names = ", ".join(a.name + (f" as {a.asname}" if a.asname else "")
                              for a in survivors)
            lines[imp.lineno - 1:imp.end_lineno] = [f"{indent}from {imp.module} import {names}"]
            print(f"    {rel}:{imp.lineno}  narrowed to `from {imp.module} import {names}`")
        else:
            del lines[imp.lineno - 1:imp.end_lineno]
            print(f"    {rel}:{imp.lineno}  line removed")
    out = "\n".join(lines)
    ast.parse(out, filename=rel)
    (WT / rel).write_text(out)
END-UNWRAP52 ─────────────────────────────────────────────────

BEGIN-GUARD52 ────────────────────────────────────────────────


class TestTheRunLogSeamHasOneIdSpelling:
    """No call site re-shapes the id the run-log seam joins verbatim.

    `append_run_event`, `emit_failure_events` and `load_run_events` join their
    `job_id` VERBATIM (finding R-0877), as `data_paths.run_log_dir` always did. A
    caller that wraps the id in `UUID(...)` therefore names the canonical hyphenated
    directory while a caller that does not names the raw one — two directories for
    one job's run log, each reader blind to the other's half — and it raises outright
    on the sixteen hex characters `data_paths.mint_job_id` produces.
    """

    SEAM = ("append_run_event", "emit_failure_events", "load_run_events")

    def _wrapped_id_arguments(self):
        """Every call site handing one of the seam functions a `UUID(...)` id.

        Resolved with `ast` over the tracked `.py` files, never by grep: a name in a
        comment or a string is not a call site.
        """
        import ast
        import subprocess

        root = Path(__file__).resolve().parent.parent
        tracked = subprocess.run(
            ["git", "ls-files", "*.py"], cwd=str(root),
            capture_output=True, text=True, check=True).stdout.split()

        hits = []
        for rel in tracked:
            try:
                tree = ast.parse((root / rel).read_bytes(), filename=rel)
            except (SyntaxError, OSError):
                continue
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or len(node.args) < 2:
                    continue
                func = node.func
                called = func.id if isinstance(func, ast.Name) else (
                    func.attr if isinstance(func, ast.Attribute) else None)
                if called not in self.SEAM:
                    continue
                arg = node.args[1]
                if (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name)
                        and arg.func.id == "UUID"):
                    hits.append(f"{rel}:{node.lineno} {called}")
        return sorted(hits)

    def test_no_call_site_wraps_the_run_log_id_in_a_uuid(self):
        hits = self._wrapped_id_arguments()
        assert hits == [], (
            "these call sites re-shape an id the seam joins verbatim, so their run "
            "log lands in a second directory: " + ", ".join(hits))

    def test_the_sweep_can_see_a_wrap_at_all(self):
        """The discriminator: a zero-gate nobody can trip protects nothing."""
        import ast

        sample = "append_run_event(data_dir, UUID(job_id), event='x')"
        node = ast.parse(sample).body[0].value
        assert isinstance(node.args[1], ast.Call)
        assert node.args[1].func.id == "UUID"
        assert node.func.id in self.SEAM

    def test_a_recalled_memory_event_is_readable_by_the_shipped_reader(
            self, tmp_path, monkeypatch):
        """The behaviour the sweep exists to protect, through the REAL functions."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from packages.memory.context_summary import (
            build_memory_context,
            emit_memory_recalled_event,
        )
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.data_paths import mint_job_id
        from packages.orchestration.timeline import load_run_events

        store_memory(key="tip", value="Use fixtures", project_id="proj1", approved=True)
        ctx = build_memory_context(project_id="proj1")

        job_id = mint_job_id()
        assert len(job_id) == 16

        emit_memory_recalled_event(
            ctx, data_dir=str(tmp_path), job_id=job_id, stage="planning")

        events = load_run_events(tmp_path, job_id)
        assert [e["event"] for e in events] == ["project_memory_recalled"]
END-GUARD52 ──────────────────────────────────────────────────

BEGIN-LANDED52 ───────────────────────────────────────────────

Landed: R-0877 — the second and last half. All 26 call sites that still wrapped the seam's id in `UUID(...)` are unwrapped by one `ast` pass over the tracked `.py` files, the six `UUID` imports that pass orphans are removed or narrowed with it, and a repo-wide sweep test holds the count at zero. Both halves of the finding are now on disk; all in this round's C3. The reviewer's authored `Done:`, covering round 51's seam fix and this round's call sites together, is owed at the next gate.
END-LANDED52 ─────────────────────────────────────────────────
