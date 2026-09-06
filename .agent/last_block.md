── STEP T001 (move two, test half and the deletion) — F272 ─
Goal:        Move the 132 test-side callers onto `run_dir` and `runs_dir`, then
             DELETE `pingpong_runs_dir` and `pingpong_run_dir` from
             `data_paths.py` in the round's last code commit. T001's move two
             is finished when this round ends.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 5
             gate entry and the prose slip · C3 the seventeen unshadowed test
             files · C4 `test_pingpong_promote.py` · C5 the seven remaining
             shadowed-scope files · C6 `tests/test_data_paths.py`, including
             the deletion of the alias test · C7 delete the two functions ·
             C8 the handback.
Change:      EXACTLY the paths listed under "The change set" below and nothing
             else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line carries one run of 2. Both readings were measured, not recalled.

## Where this round stands

Round 5 moved all 41 PRODUCTION callers off the two ping-pong spellings and
proved it: at `78457a98` making `pingpong_run_dir` raise reddened 330 tests that
never name it, and at `61c4bd2e` the same mutation over the same 88-file
selection is EXIT 0 at 3562 passed. Nothing under `packages/` or `apps/` reaches
either name any more.

What is left is the test side — 132 occurrences in 26 files, measured by the
reviewer at `61c4bd2e` over every tracked `.py` file — and then the deletion
itself. DECISION F272 D3 rules the two call shapes; they bind here unchanged and
are NOT restated in full. Read the decision in
`docs/roadmap/features/T2_F272.md`.

## The shape rule, and the correction round 5 earned

D3's Shape B applies wherever the calling SCOPE binds a local named `run_dir` or
`runs_dir` — not merely where the line being edited is the assignment. Round 5's
worker established that distinction by AST and it is the single most important
thing to carry into this round: in `pingpong_loop.run_pingpong` three call sites
sat in a scope shadowed by an assignment far below them, and a token swap there
would have raised `UnboundLocalError` BEFORE reaching the assignment. An
assignment-line regex cannot see those. USE THE SCOPE TEST.

MEASURED BY THE REVIEWER AT `61c4bd2e`, with `ast`: 34 call sites sit inside a
shadowed scope, spread over 8 files. Those 34 take SHAPE B — import
`from packages.orchestration import data_paths` and call `data_paths.run_dir(...)`
or `data_paths.runs_dir(...)`, leaving the local's name alone. The other 98 take
SHAPE A, the plain token swap.

    file                                                  sites  shadowed
    tests/orchestration/test_pingpong_promote.py             46        23
    tests/orchestration/test_failure_wiring.py                9         1
    tests/orchestration/test_job_evidence.py                  8         4
    tests/orchestration/test_evidence_bundle.py               3         2
    tests/orchestration/test_manual_completion_bundle.py      2         1
    tests/orchestration/test_repair_loop.py                   2         1
    tests/orchestration/test_worktree_lifecycle.py            2         1
    tests/orchestration/test_worktree_resume_cli.py           2         1

Compute the scope set YOURSELF with `ast` before editing anything, and report
your own numbers against these. Where yours differ, yours are the measurement
and the difference is a declared deviation.

## The change set

C3, the seventeen files with NO shadowed scope — 45 sites, SHAPE A throughout:
`tests/cli/test_task_input.py`, `tests/orchestration/test_pingpong_cli.py`,
`tests/orchestration/test_worktree_safety.py`,
`tests/orchestration/test_job_stop_integration.py`,
`tests/orchestration/test_job_worktree_integration.py`,
`tests/orchestration/test_worktree_isolation.py`,
`tests/orchestration/test_failure_postmortem.py`,
`tests/orchestration/test_job_worktree_handoff.py`,
`tests/orchestration/test_job_worktree_integrity.py`,
`tests/orchestration/test_persisted_call_episode_membership.py`,
`tests/orchestration/test_persisted_call_ownership.py`,
`tests/orchestration/test_persisted_run_call_schema.py`,
`tests/orchestration/test_run_manifest_ledger_semantics.py`,
`tests/orchestration/test_run_manifest_task_lifecycle_binding.py`,
`tests/orchestration/test_run_manifest_zero_call_expectations.py`,
`tests/orchestration/test_stream_export_e2e.py`,
`tests/orchestration/test_worktree_persistence.py`.

C4: `tests/orchestration/test_pingpong_promote.py` alone.

C5, the seven remaining shadowed-scope files:
`tests/orchestration/test_failure_wiring.py`,
`tests/orchestration/test_job_evidence.py`,
`tests/orchestration/test_evidence_bundle.py`,
`tests/orchestration/test_manual_completion_bundle.py`,
`tests/orchestration/test_repair_loop.py`,
`tests/orchestration/test_worktree_lifecycle.py`,
`tests/orchestration/test_worktree_resume_cli.py`.

C6: `tests/test_data_paths.py`. C7: `packages/orchestration/data_paths.py`.
C0a/C0b/C1/C2/C8: `.agent/authored/f272-r6.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`,
`.agent/handoff.md`.

That is 29 paths and no others. No file under `docs/` is touched: the stale
sentences in `T2_F272.md` sit inside landed DECISIONs D1 and D3, and §3 item 20
forbids rewriting landed decision text — a correction is appended, never
overwritten, and none is owed this round.

## C6 in detail, because it is the one file needing judgment

`tests/test_data_paths.py` holds 13 of the 132 sites and three distinct jobs.

**(a) Delete the test that exists only to pin the aliases.** It is
`test_the_pingpong_run_dir_is_the_run_id_under_the_pingpong_runs_dir`, currently
at lines 401 to 434, and it is deleted WHOLE — its decorator-free `def`, its
docstring and its body — because the functions it pins are being deleted. AGENTS.md
forbids deleting a test to make a check green; this is the other case, a test
whose subject is gone, and the round proves no coverage is lost rather than
asserting it. Every property it pinned is already pinned for the real names in
the SAME file, which the reviewer read at `61c4bd2e`:

    pingpong_runs_dir(arg_root) == arg_root / "runs"   ->  test_runs_dir_explicit_root (line 100)
    pingpong_runs_dir() default root                   ->  test_runs_dir_default (line 76)
    pingpong_run_dir(rid) == pingpong_runs_dir() / rid ->  test_a_run_hangs_under_runs_dir_and_never_under_jobs_dir (line 366)
    the root-argument-honoured guard                   ->  test_the_root_override_is_honoured_by_all_four (line 380)

**(b) Update two failure MESSAGES, not their assertions.** In
`test_pingpong_loop_has_no_runs_dir_helper_at_all` the strings
`"data_paths.pingpong_runs_dir / pingpong_run_dir"` and
`"data_paths.pingpong_run_dir replaced it"` name functions that will not exist.
Change those two message fragments to name `data_paths.runs_dir / run_dir` and
`data_paths.run_dir` respectively. DO NOT touch the assertions themselves: they
are about `pingpong_loop._pingpong_runs_dir`, a DIFFERENT symbol with a leading
underscore that F260 round 11 deleted, and that guard stays exactly as it is.

**(c) The remaining sites in that file** take SHAPE A or B by the scope test
like any other.

## C7, the deletion

From `packages/orchestration/data_paths.py`, delete:
- the two function definitions `pingpong_runs_dir` and `pingpong_run_dir`, with
  their docstrings;
- the comment block directly above them that begins "The ping-pong run store now
  IS the run store" and ends "do not add a new caller" — it exists only to
  explain why the two survived, so it goes with them;
- the two module-docstring lines near the top of the file that list
  `pingpong_runs_dir(...)` and `pingpong_run_dir(...)` in the path table.
Leave `runs_dir`, `run_dir`, `job_logs_dir` and `run_log_dir` untouched. Delete
no other line. Per AGENTS.md "Replacing is deleting" there is no alias, no
deprecation shim and no compatibility reader: git is the archive.

## Constraints

1. NO SLICE IS EDITED. Apply the authored texts byte for byte between their
   markers. If one looks wrong, apply it anyway and say so in the handback.
2. The 29 paths above are the whole change set. Nothing under `docs/`, nothing
   under `packages/` or `apps/` except `data_paths.py` at C7.
3. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, nothing reordered.
   C1 is the first substantive commit (§3 item 23).
4. APPEND CONVENTION for `.agent/live_review.md` and `.agent/prose_slips.md`:
   `post == pre + b"\n" + slice`, the slice being the lines between the markers
   each carrying its own terminating newline, and the post-image ending in
   exactly one `\n`.
5. PLAN CONVENTION: `.agent/plan.md` is REPLACED by exactly the PLANF272R6 slice
   bytes and nothing else.
6. THE DELETION IS THE LAST CODE COMMIT. C7 comes after every caller has moved,
   so that a missed caller surfaces as a hard `ImportError` at C7 rather than as
   a silent equivalence. Do not reorder it earlier for convenience.
7. Behaviour changes: NONE, other than the two functions ceasing to exist. Every
   other edit is a rename or a re-route of the same call to the same body.
8. Mint NO finding id and write NO `Done:` paragraph of your own.
9. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never in the primary checkout (protocol G5).
   Remove and prune it before the handback.
10. Read `.agent/STOP` with `os.path.exists` three times — before C0a, before C7
    and before C8 — and table all three. If it appears, finish only the
    half-written commit, then hand off (protocol G6).
11. `python3 -B` for every run; purge `__pycache__` in any worktree before a run.
12. Report each gate's REAL exit code. "Green" as a word is a finding (G4).

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r6.md` and `.agent/last_block.md`; both equal each other
and the BLOCK_SHA and length the delegation named. Per §3 item 37 this covers
the saved copy and its mirror, not the bytes emitted into your prompt; say so.

**G2 THE RECORD, at C2.** Four readers over `.agent/live_review.md`, readers (a)
and (b) over `.agent/prose_slips.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`, with N COUNTED BY YOUR SCRIPT from the slice's own paragraphs and never
taken from this block: units before, after, delta; the last N units equal the
slice's paragraphs IN ORDER; the units before an unchanged prefix.
(c) NEGATIVE CONTROL in memory on a `bytes` object, never on disk: flip a byte
inside the FIRST appended paragraph, asserting the offset lies inside it before
flipping; readers (a) and (b) must BOTH reject; restore and require both to
accept and the restored image to equal the disk image.
(d) COUNTS before → after C2: distinct `^- R-\d{4} — ` ids 302 → 302; distinct
`^Done: R-\d{4} — ` ids 247 → 247; open set BY DISTINCT ID 55 → 55; `^Gate: `
27 → 28; `^Gate: F272 R5 ` 0 → 1.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLANF272R6 slice bytes
exactly; report the equality and both byte lengths. Line count under the
AGENTS.md cap of 50. `## Goal` and `## Next Steps` both present.

**G4 THE COLLAPSE IS TOTAL, at C7. No exemption this time.**
(i) Enumerate every tracked `.py` file from `git ls-files` IN PYTHON — never a
shell glob, because `tests/**/*.py` does not match `tests/test_data_paths.py`.
`\bpingpong_runs?_dir\b` must occur ZERO times across all of them, INCLUDING
`data_paths.py`. Print any file with a surviving occurrence and its lines.
(ii) From the SHIPPED module rather than from its source text: import
`packages.orchestration.data_paths` and report
`hasattr(m, "pingpong_run_dir")` and `hasattr(m, "pingpong_runs_dir")`, both of
which must be FALSE. NON-VACUITY CONTROL, required beside them:
`hasattr(m, "run_dir")` and `hasattr(m, "runs_dir")` must both be TRUE, or the
two absences are measuring an import failure rather than a deletion.
(iii) NO SHADOW SURVIVES, measured BY AST over SCOPES and never by a regex over
assignment lines: zero function scopes that BOTH bind a local named `run_dir` or
`runs_dir` AND contain a call whose callee is a bare `Name` of that same
identifier. Report the count over every tracked `.py` file, which must be 0.
(iv) Report, per changed test file, how many sites you moved under each shape,
and the totals against the reviewer's 132 sites / 34 shadowed.

**G5 THE DELETION IS OBSERVABLE, AND NO COVERAGE IS LOST.**
THE CONTROL IS ALREADY MEASURED and you do not need to re-run it: in a
disposable worktree at `61c4bd2e` the reviewer deleted both function bodies with
the test callers UNMOVED and got EXIT 1 from all three of
`tests/test_data_paths.py` (1 failed, 50 passed),
`tests/orchestration/test_pingpong_promote.py` (23 failed, 48 passed) and
`tests/orchestration/test_job_evidence.py` (4 failed, 89 passed). A missed caller
is therefore a hard failure at C7 and not a silent equivalence, which is why
those same three suites going green at C7 is this round's red-proof. State that
reasoning in the handback rather than restating the control as your own reading.
COVERAGE: report `tests/test_data_paths.py`'s collected test count before C6 and
after C6 — the reviewer measured 51 at `61c4bd2e` and expects 50, the difference
being exactly the deleted alias test. Then obtain the FULL NODE IDS of the four
surviving pins by `--collect-only` — `test_runs_dir_default`,
`test_runs_dir_explicit_root`,
`test_a_run_hangs_under_runs_dir_and_never_under_jobs_dir` and
`test_the_root_override_is_honoured_by_all_four` — and run exactly those four:
EXIT 0 at 4 passed. Report the node ids you collected.

**G6 THE SUITES, at C7, run SERIALLY, each its own invocation.**
`python3 -B -m pytest tests/test_data_paths.py -q -p no:randomly`,
then `tests/orchestration/`, then `tests/cli/`, then the canary
`tests/cli/test_golden_path.py`. Every one EXIT 0. Report each exit code and
each summary line verbatim. The reviewer measured the canary at 42 passed and
`tests/cli/` at 1537 passed at `78457a98`; a lower count is a finding, not a
rounding.

**G7 LINT AND INTEGRITY, at C7.** `python3 -m ruff check` over exactly the
changed `.py` files in ONE invocation: EXIT 0. If it goes red, report the codes
and do NOT fix anything outside the change set. A repo-wide `ruff check .` is NOT
ordered: it is EXIT 1 at 26 errors on base and on `main` under OPEN finding
R-0468. `python3 -m apps.cli.grouped integrity check --json`: EXIT 0,
`"passed": true`, `"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C8 is staged.
`git ls-files .remedy-wt` EMPTY. `git worktree list` naming any worktree you
created and confirming its removal; the twelve pre-existing `remedy/job-*`
entries predate this round and stay. Per commit for C0a through C7 — NOT C8,
which cannot count its own insertions (§3 item 14) — the insertion count from
`git diff --numstat <parent> <commit>`, each under the DECISION F104 D1 cap of
500, each single-parent. Marker sweep: zero lines beginning `<<<BEGIN ` or
`<<<END ` in every written non-block file. The three `.agent/STOP` readings of
constraint 10, as a table.

## The slices

<<<BEGIN PLANF272R6>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3, 4 and 5 PASSED; round 2
FAILED on a premise DECISION F272 D2 has corrected. Round 6 finishes T001: the
test half of the name collapse and the deletion of the two ping-pong spellings.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 6 moves the 132 test-side callers onto `run_dir` and `runs_dir` by the two
shapes DECISION F272 D3 rules, choosing between them with an AST scope test
rather than an assignment regex, and then DELETES `pingpong_runs_dir` and
`pingpong_run_dir` in the round's last code commit. The test that exists only to
pin those two is deleted with them; its four properties are already pinned for
the real names in the same file. When this round ends, T001 is complete.

## Next Steps

1. T002, the rest of the unified record: the eleven administrative fields, eight
   of which have no counterpart in `JobPlan`, and the Mission extension — the
   order, the contract, the mission plan and the ordered job references.
2. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each with a test that proves it works on a job created
   through the ping-pong path.
3. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A missed caller is invisible until the deletion commit, where it becomes an
  `ImportError`. That is why the deletion is last and why the suites run after
  it rather than before.
- The shadowing hazard is a property of the enclosing SCOPE, not of the line
  being edited. Round 5 found three sites an assignment regex could not see.
<<<END PLANF272R6>>>

<<<BEGIN RECORDR6>>>
Gate: F272 R5 — the F272 round 5 entry. VERDICT PASS, AND THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY IN THE REVIEWER'S OWN WORKTREE. Range `78457a98`..`61c4bd2e`, nine commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7 with nothing added, dropped or reordered; insertion counts 384, 336, 21, 6, 70, 13, 14 and 14 for the eight before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. `git diff --numstat 78457a98..61c4bd2e` lists exactly the fourteen paths of the change set and nothing more. THE ROUND MOVED ALL 41 PRODUCTION CALLERS OF `pingpong_run_dir` AND `pingpong_runs_dir` ONTO `run_dir` AND `runs_dir`, AND THE REVIEWER READ EVERY ONE OF THE THREE CODE DIFFS LINE BY LINE rather than sampling them: 13 sites in `pingpong_loop.py` all under shape B, 14 in `job_evidence.py` split 10 shape A and 4 shape B, and 14 across the five remaining files split 12 and 2, which is 22 shape A and 19 shape B and reproduces the worker's own table exactly. Every shape-B site is one whose enclosing scope really does bind a local of that name, and every shape-A site is one whose scope does not. TRANSPORT: the reviewer's scratch original `.remedy-wt/f272-r5-block.md`, the committed `.agent/authored/f272-r5.md` and the committed `.agent/last_block.md` are all 30713 bytes and all hash to `eef4d9b30b7f1ab86b3119a053bec4cf8209f1f60b6e3d7ee6f0cc88cb38eb21`, the digest the delegation named before the round began; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. THE RED-PROOF IS THE ROUND'S LOAD-BEARING CLAIM AND THE REVIEWER RE-RAN IT RATHER THAN READING IT. In its own disposable worktree at `61c4bd2e`, with `data_paths` confirmed to resolve from INSIDE the worktree and every `__pycache__` purged, the reviewer replaced the single line `return pingpong_runs_dir(root) / run_id` — counted exactly 1x in that file before the edit — with a raise, confirmed by direct call that the raise was LIVE and that `run_dir` still returned `/tmp/z/runs/x`, recomputed the 88-file selection from the block's rule rather than copying the worker's list, and measured EXIT 0 at `3562 passed in 399.71s` with zero `FAILED` and zero `ERROR` lines. At `78457a98` the reviewer had measured the same mutation over the same selection at EXIT 1 with `330 failed, 3215 passed, 17 errors`, and the unmutated control there at EXIT 0 with 3562 passed. A run that passes 3562 tests while the function raises cannot be a broken environment reporting a false green — a broken worktree fails rather than passes — so the single mutated reading at the head is both the proof and its own control, and the before/after pair is a real discriminator rather than a gate that could not fail. THE STATIC GATES ALL REPRODUCE: over 1063 tracked `.py` files enumerated from `git ls-files` in Python, `\bpingpong_runs?_dir\b` occurs ZERO times under `packages/` and `apps/` outside `data_paths.py`, exactly 5 times inside it — the two defs, the two module-docstring lines and the one internal call — and still 132 times under `tests/`, which the round correctly left alone; `git diff --name-only` over the round lists no path beginning `tests/`; and zero lines in the seven changed files match the shadow pattern. THE RECORD, at C2: `.agent/live_review.md` 1073333 to 1081516 bytes and `.agent/prose_slips.md` 133530 to 134136, both with the pre-image a byte-exact prefix and `post == pre + NL + slice` TRUE under the convention round 5's constraint 4 states. Registrations 302 unchanged, resolutions 246 to 247 BY DISTINCT ID, open set 56 to 55, `Done: R-0818` 0 to 1 with the earlier `Landed: R-0818` line correctly LEFT IN PLACE because the record is append-only, `^Gate: ` 26 to 27 and `^Gate: F272 R4 ` 0 to 1. THE PLAN at C1 is 2173 bytes byte-equal to its slice, 45 lines against the cap of 50, carrying both required headings. THE FEATURE FILE at C3 is 14790 to 19325 bytes by the same append reader, with `### DECISION F272 D3`, `D2` and `D1` each exactly 1. `python3 -m ruff check` over all seven changed files in one invocation is EXIT 0 at `All checks passed!`, `python3 -m apps.cli.grouped integrity check --json` is EXIT 0 with `"passed": true` and `"fail_count": 0`, the canary with `tests/docs/` and `tests/orchestration/test_roadmap_index.py` is EXIT 0 at 375 passed, `git status --porcelain` is EMPTY and `git ls-files .remedy-wt` empty, and the `.agent/STOP` sentinel was absent at all three ordered readings. THE WORKER'S SECOND DEVIATION IS THE ROUND'S MOST VALUABLE OUTPUT AND IT IS UPHELD IN FULL. Determining the call shapes by `ast` rather than by regex, it reproduced the block's seven `run_dir = pingpong_run_dir(` assignments exactly and then found THREE FURTHER SITES, at former lines 3009, 3303 and 3649 of `pingpong_loop.py`, sitting inside `run_pingpong`, a scope shadowed by an assignment at former line 4076 far BELOW them. A token swap at those three would have raised `UnboundLocalError` EARLIER in the function than at the assignment itself, so they are more certainly fatal than the seven the block enumerated, and an assignment-line regex is blind to all three. They needed no special handling only because the block independently ruled shape B for all thirteen sites in that file. THE BLOCK'S RULE WAS CORRECT — it says to determine the shape by reading the enclosing scope and calls the enumeration a cross-check — while the enumeration standing beside it described a narrower thing than the rule, and a reader working from the list rather than the rule would have shipped three latent `UnboundLocalError`s. That gap is recorded as one dated line in `.agent/prose_slips.md` and spends no id, because nothing on disk was wrong: per operator amendment amend0827-process-diet rule 2 an id is spent on product effect, and here the worker's own measurement closed the gap before any byte landed. The counter-measure is on disk rather than in this paragraph: round 6's block orders the scope set computed by `ast` and its gate G4(iii) measures surviving shadows over SCOPES rather than over assignment lines. THE REMAINING DEVIATIONS ARE ACCEPTED. Collapsing the `pingpong_loop.py` from-import to one line and placing the new module import before `artifact_summary` is forced by ruff's `I001`, which gate G7 requires green, so it is a consequence of the ordered gate and not a choice. The behaviour argument is right and the reviewer re-derived it from the source rather than accepting it: `pingpong_runs_dir(root)` IS `runs_dir(root)` and `pingpong_run_dir(run_id, root)` IS `runs_dir(root) / run_id`, which is `run_dir`'s own body, so constraint 6 could not engage. Eleven scratch drivers were removed by exact path and never by glob, and the one stale `.remedy-wt/__pycache__` entry the worker found and declared — a round-3 artefact whose source no longer exists — is correctly reported as positive evidence that `python3 -B` held for every run of the round.
<<<END RECORDR6>>>

<<<BEGIN SLIPSR6>>>
2026-09-06 · F272 R5 block (reviewer) · The block's shape rule was scope-based and correct, but the enumeration beside it listed only the seven `run_dir = pingpong_run_dir(` ASSIGNMENTS, while the hazard is a property of the enclosing SCOPE: three further sites in `pingpong_loop.run_pingpong` sat above an assignment that shadowed them, where a token swap would have raised `UnboundLocalError` sooner than at the assignment itself. The worker determined the shapes by `ast`, found all three, and nothing wrong reached disk, so this spends no id. Round 6's block orders the scope set computed by `ast` and gates surviving shadows over scopes rather than over assignment lines.
<<<END SLIPSR6>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 2 of feature F272 · round 6`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-` from `git diff --numstat`, the item-status table covering
C0a through C8 with every item present exactly once, one line per gate G1 to G8
with its real exit code, the per-file site counts and shapes G4(iv) asks for,
the four collected node ids G5 asks for, the authored-text proof table,
deviations and assumptions, and the next expected action. There is no length cap.
