STEP T001 read-endpoint part one — F037 R6

Goal: the diff artifacts become readable as contract-v1 JSON without a server.
One new module resolves an evidence directory, and optionally one task run, to
the right unified-diff artifact and returns the F037 envelope, naming every
absence instead of raising. R7 wires the routes onto it.

Base: `9deb942eda94ec82ba00badbeece4cde05138bed`.
Branch: `feature/f037-rendered-diff-viewer`. SESSION 2 of feature F037, round 6,
rounds so far 5.

Bundle, one commit each, in this order:
C0a  save this block verbatim to `.agent/authored/f037-r6.md`
C0b  mirror the C0a blob into `.agent/last_block.md`
C1   `.agent/plan.md` from slice PLANF037R6
C2   `.agent/live_review.md` from pairs DONE717 and DONE718, then append GATER5;
     `.agent/prose_slips.md` append SLIPR6
C3   `packages/orchestration/diff_view_source.py` and
     `tests/orchestration/test_diff_view_source.py`, written by you from the SPEC
C4   `.agent/handoff.md`, the handback

Change set — these paths and no others:
  .agent/authored/f037-r6.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  packages/orchestration/diff_view_source.py
  tests/orchestration/test_diff_view_source.py
  .agent/handoff.md
Run `git push origin feature/f037-rendered-diff-viewer` AFTER C4. Create no pull
request and merge nothing: the Open PR Gate returned `[]` when this block was
authored, so there is nothing to merge.

Slice convention: the authored texts in this block are PLANF037R6, DONE717,
DONE718, GATER5 and SLIPR6. Each is delimited by a line `<<<SLICE <NAME>` and a
line `<<<END <NAME>`; the marker lines are never part of the text.

Constraints:
1. Apply every slice byte for byte, extracted from the COMMITTED C0a blob by its
   marker LINES in Python. Never retype a slice, never edit a slice.
2. `.agent/plan.md` is a WHOLE-FILE replacement by PLANF037R6.
3. DONE717 and DONE718 are FROM/TO pairs. The containment test was run before
   emission, one reading per pair: DONE717 `TO contains FROM: false`, DONE718
   `TO contains FROM: false`. Both are REWRITES, so each orders its FROM at 0x
   and its TO at 1x in the file after C2, and neither orders an append reading.
   The FROM of each pair is the whole existing `Landed:` line for that finding.
4. GATER5 is appended at EOF of `.agent/live_review.md` AFTER both pairs are
   applied, in the same commit. SLIPR6 is appended at EOF of
   `.agent/prose_slips.md`. The append convention is the file's existing one: a
   single separator newline, then the slice bytes.
5. No finding id is minted this round. R5 PASSED and produced no defect with
   product effect; the reviewer-prose slips it exposed go to SLIPR6 with no id,
   per AGENTS.md `### prose_slips.md` and operator amendment amend0827 rule 2.
6. Do NOT touch the `Landed: R-0711` line. It belongs to F032, whose branch
   ended before a reviewer could author its `Done:` text — the
   docs/agents/planner_reviewer_prompt.md §4 item 13 terminator, not a gap for
   this round to close. Its survival is why `^Landed: R-` reads 1 and not 0
   after C2.
7. Production code is written by YOU from the SPEC. It is described, not sliced,
   so no gate compares it to authored bytes. Match the surrounding module's
   idiom: module docstring, a one-line WHY above each definition, type hints,
   the same import style `packages/orchestration/diff_parser.py` uses.
8. `packages/orchestration/ui_server.py` is NOT touched. No route, no handler
   dict key, no test under `tests/ui_server/`. R7 does the wiring and needs the
   route-walk guard measured first.
9. `packages/orchestration/diff_parser.py` is NOT touched. R6 consumes it.
10. `tests/test_no_interactive_guard.py` sweeps every file under
    `packages/orchestration` for interactive constructs against an EMPTY
    allowlist (read at the base). The new module contains no `input(`, no
    `getpass`, no interactive prompt of any kind.
11. Where a measurement disagrees with a value this block names, report the
    measured value and the disagreement under Deviations. Never bend a
    measurement to a gate, and never change code to suit a number.

SPEC — packages/orchestration/diff_view_source.py

S1. The module docstring states the WHY: `diff_parser.py` turns diff TEXT into
    the contract-v1 view and touches no filesystem; this module is the other
    half — it decides WHICH artifact to read for a scope and hands the text
    over. It performs no HTTP and imports nothing from `ui_server.py`, so the
    endpoint layer stays a thin caller and this half is testable with no server.

S2. The module's public names:
      DIFF_SCOPE_JOB = "job"
      DIFF_SCOPE_TASK_RUN = "task_run"
      DIFF_JOB_ARTIFACT_NAME = "workspace.diff"
      DIFF_TASK_RUN_ARTIFACT_NAME = "safe.diff"
      DIFF_TASK_RUNS_DIR_NAME = "task_runs"
      DIFF_REASON_NO_EVIDENCE_DIR = "evidence_dir_unavailable"
      DIFF_REASON_ARTIFACT_MISSING = "diff_artifact_missing"
      DIFF_REASON_UNKNOWN_TASK_RUN = "unknown_task_run"
      SAFE_TASK_RUN_ID_RE = re.compile(r"^T\d{3,}$")
      list_task_run_ids(evidence_dir) -> list[str]
      build_diff_view(evidence_dir, task_id=None) -> dict
    `DIFF_REASON_NO_EVIDENCE_DIR`'s VALUE repeats the string
    `packages/orchestration/ui_server.py` already uses for the same condition in
    its `_empty_prompt_trace("evidence_dir_unavailable")` call, read at the base
    commit named above — one spelling per concept, per AGENTS.md "Code
    Discoverability Conventions".

S3. `list_task_run_ids(evidence_dir)` returns the SORTED names of the
    subdirectories of `<evidence_dir>/task_runs` that `SAFE_TASK_RUN_ID_RE`
    fully matches. It returns `[]` when `evidence_dir` is None, is not a
    directory, or holds no `task_runs` directory. The pattern is the same shape
    `packages/orchestration/final_verifier.py` applies to that same directory in
    its own `_task_ids` reader, read at the base commit; it is re-declared here
    rather than imported because that name is private to that module.

S4. `build_diff_view(evidence_dir, task_id=None)` returns a dict with exactly
    these keys:
      version      — `diff_parser.DIFF_VIEW_VERSION`, IMPORTED. The module
                     declares no second version literal of its own.
      scope        — DIFF_SCOPE_TASK_RUN when `task_id` is not None, else
                     DIFF_SCOPE_JOB. It is what was ASKED FOR, so it is set
                     before anything can fail.
      task_id      — the argument unchanged, or None.
      source       — the artifact path RELATIVE to the evidence dir, or None.
      available    — True only when a diff artifact was actually read.
      reason       — None when available, else exactly one DIFF_REASON_* value.
      truncated    — the parser's value, or False.
      files        — the parser's list, or [].
      task_run_ids — `list_task_run_ids(evidence_dir)`, always present so a
                     caller that asked for the wrong run can see the real set.

S5. The order of decisions, which is load-bearing:
    (a) `evidence_dir` is None or is not a directory: available False, reason
        DIFF_REASON_NO_EVIDENCE_DIR, source None, files [], task_run_ids [].
    (b) `task_id` is not None and is NOT a member of
        `list_task_run_ids(evidence_dir)`: available False, reason
        DIFF_REASON_UNKNOWN_TASK_RUN, source None, files [].
        MEMBERSHIP IN THE REAL LISTING is the check, never a pattern match over
        the argument alone. A name that is not already a directory there cannot
        be reached, so `..`, an absolute path and any traversal are refused by
        construction rather than by pattern; the regex filters the LISTING,
        which is a different job. Write the one-line WHY above the check, and
        state there that `path_utils.sanitize_path_component` is deliberately
        NOT used: sanitizing rewrites an unsafe id into a DIFFERENT valid one
        and would serve the wrong task run's diff, where refusing serves none.
    (c) otherwise the artifact is
        `<task_runs>/<task_id>/<DIFF_TASK_RUN_ARTIFACT_NAME>` for a task run and
        `<DIFF_JOB_ARTIFACT_NAME>` for a job. `source` is set to that relative
        path at this point, so an absence still tells the caller what was
        looked for.
    (d) the artifact does not exist, is not a file, or cannot be read as UTF-8
        (`OSError`, `UnicodeDecodeError`): available False, reason
        DIFF_REASON_ARTIFACT_MISSING, files [], truncated False, `source` kept.
    (e) otherwise parse the text with `parse_unified_diff_to_view` and take its
        `files`, `truncated` and `version`; available True, reason None. An
        EMPTY artifact is AVAILABLE with zero files: "nothing changed" and "no
        diff was written" are different answers and this module must not merge
        them. Say that in the WHY comment.

S6. `build_diff_view` never raises. Every failure is one of the three reasons.

SPEC — tests/orchestration/test_diff_view_source.py

S7. Build every evidence tree under pytest's `tmp_path`, never under the
    repository. One helper writes an evidence dir carrying `workspace.diff` and
    `task_runs/T001/safe.diff` from real unified-diff text.
S8. Job scope, happy path: scope is DIFF_SCOPE_JOB, source is
    `workspace.diff`, available True, reason None, and `files` carries the path
    the job fixture's diff names.
S9. Task-run scope, happy path: scope DIFF_SCOPE_TASK_RUN, task_id `T001`,
    source `task_runs/T001/safe.diff`, available True. Assert on a file path
    that ONLY the task diff contains, so the test fails if the two artifacts
    were ever swapped.
S10. Assert `version` equals `diff_parser.DIFF_VIEW_VERSION` by IMPORT, never a
     transcribed integer.
S11. One test per absence reason: `evidence_dir=None`; an evidence dir with no
     `workspace.diff`; `task_id="T404"` against a tree holding `T001`. Each
     asserts the exact reason constant, `available is False` and `files == []`;
     the unknown run additionally asserts `source is None` and that
     `task_run_ids` holds `T001`, and the missing artifact additionally asserts
     that `source` still names the path that was looked for.
S12. The refusal test, which must not be weakened: for each of
     `"../../../etc"`, `"T001/../../.."`, `"/etc"`, `"."` and `""`, assert
     reason DIFF_REASON_UNKNOWN_TASK_RUN and `source is None`. Before the calls,
     write a file OUTSIDE the evidence dir but under `tmp_path` holding a
     recognisable marker string, and assert that marker appears nowhere in
     `repr()` of any returned dict — so the test proves nothing was READ, not
     merely that a field was set.
S13. `list_task_run_ids` sorts and filters: build `T001`, `T010`, `T002`, a
     directory named `nope` and a FILE named `T999`, then assert the result is
     exactly `["T001", "T002", "T010"]`.
S14. An EMPTY `workspace.diff` is available with `files == []`, pinning the
     S5(e) distinction so a later simplification cannot fold it into
     DIFF_REASON_ARTIFACT_MISSING.

Done when — eight gates. Run every one, record its REAL exit code and its
verbatim summary line, and put one line per gate in the handback.

G1 hygiene. Read `.agent/STOP` from disk before C0a and again before C4; report
   ABSENT or PRESENT at both points, and if PRESENT stop after the current
   commit and hand off. Report `git rev-parse HEAD` before C0a — it must equal
   the base SHA above — and `git branch --show-current`. Report the
   `git status --porcelain` LINE COUNT after each of C0a, C0b, C1, C2 and C3;
   each must be 0.

G2 transport, ONE digest comparison. After C0a report the sha256, byte count and
   line count of `.agent/authored/f037-r6.md`. After C0b report
   `git rev-parse HEAD:.agent/authored/f037-r6.md` and
   `git rev-parse HEAD:.agent/last_block.md`; they must be the SAME blob hash.
   State plainly that this chain covers the saved copy, its mirror and the
   working copy, and claims nothing about the bytes of any prompt.

G3 extraction and caps. Extract all five slices from the COMMITTED C0a blob by
   their marker lines and print each slice's NAME and line count. Print TOTAL
   (the block's lines), CONTENT (the sum of the slice line counts) and
   PROSE = TOTAL − CONTENT. Report all three as measured. PROSE must be at most
   400 and TOTAL at most 490.

G4 the plan at C1. `.agent/plan.md` is byte-equal to PLANF037R6 under the
   newline-included convention: report True or False. Report the NEGATIVE
   CONTROL against the slice minus its trailing newline; it must be False.
   Report the line-anchored counts of `^## Goal$` and `^## Next Steps$`, each 1,
   and `wc -l`, which must be strictly under 50.

G5 the record at C2, full byte forensics — this is the append into the record,
   which the gate budget reserves it for.
   PAIRS: for each of R-0717 and R-0718 report the count of its FROM line before
   and after C2 (1 then 0) and of its TO line before and after (0 then 1).
   APPEND, live_review.md: measure the byte length AFTER the two pairs and
   BEFORE the append — call it L — then report that the post-append length
   equals L + 1 + the GATER5 byte length, and that the intermediate is a byte
   PREFIX of the final. Reader (b), independent and structural: have your script
   COUNT N, the number of blank-line units in GATER5, and compare the LAST N
   units of the final file against the slice's N units IN ORDER. NEGATIVE
   CONTROL: flip one byte inside the FIRST appended paragraph and report that
   reader (a) and reader (b) BOTH come back False.
   APPEND, prose_slips.md: the same two readers and the same control, with the
   control byte inside the FIRST appended bullet. The base length before C2 is
   6840 bytes; report the measured value beside it.
   COUNTS after C2, line-anchored, each reported as measured:
     `^- R-\d+ — ` 279, unchanged — no id is minted this round
     `^Done: R-\d+ — ` 27
     `^Landed: R-` 1
     `^Gate: F\d+ R\d+ — ` 76
     `^Gate: R\d+ — ` 19, unchanged
   Also report: the set of ids ADDED (must be empty), the set of ids newly
   RESOLVED (must be exactly R-0717 and R-0718), whether all ids are DISTINCT,
   the maximum id, and the size of the open set, which is every registered id
   minus every resolved id.

G6 the red-proofs for the new module, run ONLY inside a disposable
   `git worktree` at the C3 tree and never in the primary checkout. Purge
   `__pycache__` and use `python3 -B` before EVERY run, and restore the module
   between mutations. Report the UNMUTATED CONTROL first —
   `python3 -B -m pytest tests/orchestration/test_diff_view_source.py -q` — with
   its real exit code and verbatim summary; a colour with no baseline is not
   evidence. Then two mutations, each described BY PROPERTY because you wrote
   the code, and for each one quote the exact lines you changed FROM and TO, the
   real exit code, the verbatim summary and every failing node id in full:
     (a) defeat S5(b): make the task-run branch accept ANY `task_id` without
         testing membership in `list_task_run_ids`, so the path is built from
         the argument directly.
     (b) defeat S5(d): make the missing-artifact branch report `available` True
         with `reason` None.
   If either mutation comes back GREEN, report the green plainly and diagnose
   WHY the mutated branch is unreachable by the tests. Do NOT substitute a
   different mutation and do NOT add a test to make it red. Remove and prune the
   worktree afterwards and report `git worktree list` line count and
   `git status --porcelain` line count in the primary checkout.

G7 suite, lint and canary at C3, in the primary checkout, ONE pytest process at
   a time and never two in parallel.
   Run `python3 -m pytest tests/orchestration/test_diff_view_source.py
   tests/orchestration/test_diff_parser.py -q`; report the real exit code, the
   verbatim summary line and the count of lines matching `^FAILED`. Add the
   extractor-blindness control: run the SAME counter over a control string that
   contains `FAILED tests/orchestration/test_diff_view_source.py::test_control_string`
   and report that it returns 1, so a 0 above is a measurement and not a blind
   spot.
   Report the node-id inventory of the new file from
   `python3 -m pytest tests/orchestration/test_diff_view_source.py --collect-only -q`
   — the count and the ids. Never derive node ids by regexing `-v` output.
   Run `python3 -m ruff check packages/orchestration/diff_view_source.py
   tests/orchestration/test_diff_view_source.py` with the repository's own
   configuration and NO `--isolated`; report the real exit code and the verbatim
   output.
   Run the canary `python3 -m pytest tests/cli/test_golden_path.py -q`; report
   the real exit code and the verbatim summary.

G8 structure, artifacts and the Open PR Gate, measured at C3.
   Report `git diff --name-only <base>..<C3>` against the change set above minus
   `.agent/handoff.md`, and report BOTH residues — actual minus expected and
   expected minus actual — each of which must be empty.
   Report a restricted `git diff --stat`: `apps/` empty, `docs/` empty,
   `packages/` holding only `diff_view_source.py`, `tests/` holding only
   `test_diff_view_source.py`.
   Report the per-commit INSERTION count from `git diff --numstat` for C0a, C0b,
   C1, C2 and C3 — not for C4, whose own count cannot exist while its text is
   being written — and confirm each commit is single-parent and each insertion
   count is under 500.
   Report the line-anchored counts of `^<<<SLICE ` and `^<<<END ` in
   `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
   `.agent/prose_slips.md` at C2; all must be 0. Then run the SAME counter over
   the C0a blob and report the number it measures, which must be greater than
   zero, so the sweep is shown not to be blind.
   Report `git ls-files .remedy-wt` line count, which must be 0.
   Report the Open PR Gate verbatim:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
   The PUSH is ordered after C4 and is deliberately NOT part of any gate: C4
   writes the handback, so the handback cannot report a value that does not
   exist when it is written. Run the push, and do not name its result in
   `.agent/handoff.md`; the reviewer reads the remote tip itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the Session block naming SESSION 2 of feature F037 and round 6, the
range and base SHA, a per-commit changed-files table with a `+/-` column taken
from `git diff --numstat` itself and agreeing cell for cell with the per-commit
reading G8 orders, the external actions, one line per gate G1 through G8 with
its real result, the item-status table covering every C-item and every S-item
and every gate with `done`, `skipped` or `deviated` plus a reason, the
Deviations, and the Next section. It has NO length cap. State in the Next
section that the first action of the next round is to re-read `.agent/STOP`
from disk, then the Open PR Gate.

<<<SLICE PLANF037R6
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 and D2.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
R6 opens session 2 and builds the first half of what T001 still owes: a new
module `packages/orchestration/diff_view_source.py` resolving an evidence
directory, and optionally one task run, to the right diff artifact and returning
the contract-v1 envelope with every absence named rather than raised. It also
books the R5 verdict, replaces the `Landed:` lines of `R-0717` and `R-0718` with
reviewer-authored `Done:` text, and records four reviewer-prose slips. No route
is added: the server wiring is R7's and needs the route-walk guard measured
first.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R5 gate, both resolutions, the slips | ordered | record first |
| C3 the resolver module and its tests | ordered | refusal proved, not asserted |
| C4 the handback | ordered | |

## Next Steps
1. The two GET routes onto this module — the job scope as a handler-dict key and
   the task-run scope as a structural route — with the route walk in
   `tests/ui_server/test_command_channel.py` measured before the edit. That
   finishes T001.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low; it is a stale count in a test docstring and belongs
  to whoever next edits that file.
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- The parser still has no consumer. R6 gives it one that no HTTP layer can
  reach yet, so its corpus keeps carrying the weight until R7.
<<<END PLANF037R6

<<<SLICE DONE717
Done: R-0717 — RESOLVED at F037 R5, commit `763cc6a9`, and verified by the reviewer at `9deb942e`. `tests/orchestration/test_diff_parser.py` now carries `INTRALINE_PURE_DELETION_DIFF` and `INTRALINE_PURE_INSERTION_DIFF`, each producing the bare opcode the corpus never held, and each asserting the exact spans AND the sliced text on the marked side AND `[]` on the other — the discriminator the finding asked for, not merely a fixture. THE PIN IS PROVED AND NOT ASSERTED, and the reviewer reproduced both proofs itself in a disposable worktree at `9deb942e` with `__pycache__` purged before every run: against an unmutated control of exit 0 at `28 passed`, narrowing the old-side opcode tuple `("replace", "delete")` to `("replace",)` is exit 1 at `1 failed, 27 passed` failing exactly `test_intraline_spans_mark_a_pure_deletion_on_the_del_side_only`, and narrowing the new-side tuple `("replace", "insert")` to `("replace",)` is exit 1 at `1 failed, 27 passed` failing exactly `test_intraline_spans_mark_a_pure_insertion_on_the_add_side_only`. Each mutated string occurred exactly once in the module before its edit, counted rather than assumed. Both clauses were deletable at `c6c490cb` and neither is deletable now, which is the whole of the finding. ONE PART OF THE ORDER WAS WRONG AND THE ROUND CAUGHT IT: the block's stated discriminator for the deletion fixture named the `add`-side `[]` as the assertion that fails under the ordered mutation, and the assertion that actually fails is the `del`-side span equality, because dropping `delete` from the old tuple empties the old side. The fixture is correct either way and the test fails under the mutation as ordered; only the reviewer's explanation of which clause fires was wrong, and it is recorded in `.agent/prose_slips.md` with no id because nothing landed wrong on disk.
<<<END DONE717

<<<SLICE DONE718
Done: R-0718 — RESOLVED at F037 R5, commit `c984c161`, and verified by the reviewer at `9deb942e`. `packages/orchestration/diff_parser.py` now decides similarity in `_intraline_pair_is_similar`, which takes the `difflib` ratio over the SIGNIFICANT tokens — everything that is not pure whitespace — while `_intraline_spans_for_pair` keeps mapping spans over the FULL token stream so character offsets stay exact. That is precisely the counter-measure the finding named, and `DIFF_INTRALINE_MIN_RATIO` is unchanged at 0.3 because the constant was never the defect. THE REPAIR IS MEASURED IN BOTH DIRECTIONS BY THE REVIEWER AT `9deb942e`, not read: the FULL-STREAM ratio for `alpha beta gamma` against `zzz qqq www` is still 0.400, above the 0.3 threshold, so the old code could not have refused that pair and the finding's diagnosis is confirmed on the shipped module; the repaired module returns `[]` on BOTH sides for that pair, and a real one-word edit — `the fox jumps` against `the cat jumps` — is still marked at `[[4, 3]]` on both sides, so narrowing the ratio's stream did not narrow what it lets through. Widening the guard so it can never fire, `return ratio >= 0.0`, is exit 1 at `2 failed, 26 passed`: it kills the new multi-word test AND the pre-existing single-word threshold test together, which is the correct blast radius for that mutation rather than an over-broad one, since every test asserting the guard fired must die when the guard cannot fire. ONE PART OF THE ORDER WAS UNMEETABLE AND THE ROUND HANDLED IT WELL: the block ordered a report that a `the fox jumps` regression test still passes, and the corpus held no such test; the worker added it as `test_intraline_spans_still_mark_a_multi_word_pair_that_shares_its_other_words` with its ratio asserted rather than transcribed, instead of reporting a result it could not have measured. That authoring slip is recorded in `.agent/prose_slips.md` with no id.
<<<END DONE718

<<<SLICE GATER5
Gate: F037 R5 — the closing round of session 1, and the round that repaired both defects session 1's own red-proof discipline had exposed. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran the load-bearing ones itself at `9deb942e`: the scoped suite `python3 -m pytest tests/orchestration/test_diff_parser.py -q` is exit 0 at `28 passed`, `python3 -m ruff check` over the two touched paths with the repository's own configuration is exit 0 at `All checks passed!`, and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` is exit 0 at `42 passed`. ALL THREE MUTATION RED-PROOFS REPRODUCE EXACTLY AS REPORTED, run by the reviewer inside a disposable worktree with `__pycache__` purged before every run and the module restored between them, each mutated string counted at exactly one occurrence before its edit: unmutated control exit 0 at `28 passed`, the old-side opcode tuple narrowed exit 1 at `1 failed, 27 passed`, the new-side tuple narrowed exit 1 at `1 failed, 27 passed`, and the similarity guard widened to `return ratio >= 0.0` exit 1 at `2 failed, 26 passed`. `R-0717` AND `R-0718` ARE BOTH RESOLVED ABOVE, each with its own reviewer-authored text. THE RECORD IS AS THE ROUND LEFT IT: `^- R-\d+ — ` stands at 279 with every id distinct and a maximum of `R-0718`, and the open set stood at 254 before this entry's own commit. THE ROUND'S BEST WORK IS ITS DEVIATIONS, WHICH ARE ALL SOUND AND ALL REVIEWER-CAUSED. G8 ordered `^Landed: R-` to read 2 where 3 was the only reachable value, because the base's third such line belongs to `R-0711` and the same block's constraint 6 forbade deleting it — the worker declared the contradiction rather than bending either half, and it was right to. The block's stated discriminator for the pure-deletion fixture named the wrong failing assertion. Item S6's gloss on the both-empty case contradicted S6's own definition, and the worker implemented the DEFINITION, which is the operative clause and the one S5's diagnosis requires. Item S8 named a `the fox jumps` regression test the corpus did not hold, so the worker added it rather than transcribing a result. All four are reviewer-prose defects that left nothing wrong on disk, so under operator amendment amend0827 rule 2 they spend no id and are recorded in `.agent/prose_slips.md` instead. NO BLOCK CONDITION AROSE: nothing fabricated, no false live indicator, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER5

<<<SLICE SLIPR6
- 2026-08-28 · F037 R5 · G8 ordered `^Landed: R-` to read 2 after C4 while the
  same block's constraint 6 forbade deleting the third such line, which belongs
  to `R-0711`, so 3 was the only reachable value and the gate contradicted the
  block's own constraint; a count over a SHARED record file is derived from the
  base reading plus the lines the round's own constraints add, and pre-existing
  entries are counted rather than assumed away.

- 2026-08-28 · F037 R5 · SPEC S2 named the `add`-side `[]` as the assertion that
  fails when `delete` is dropped from the old-side opcode tuple, and the
  assertion that actually fails is the `del`-side span equality; a stated
  discriminator is RUN against the mutation it names before it is written down,
  because a fixture can be right while the sentence explaining it is wrong.

- 2026-08-28 · F037 R5 · SPEC S6 defined significant tokens as "the tokens that
  are not pure whitespace" and then glossed the both-empty case as lines made of
  "whitespace and punctuation", which that definition excludes; where a spec
  states a definition and a gloss beside it, the two are read against each other
  before emission and the gloss is deleted rather than left to be chosen between.

- 2026-08-28 · F037 R5 · SPEC S8 ordered a report that a `the fox jumps`
  replacement test still passes, and no such test existed in the corpus; a gate
  naming a test by its CONTENT is resolved against the file at the base commit,
  the same obligation `docs/agents/planner_reviewer_prompt.md` §3 item 24 places
  on a path a gate names.
<<<END SLIPR6
