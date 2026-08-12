── STEP T004 part 2b-ii / F107 R11 — the fixture task runs on the compiled context ──
Goal:        A fixture task is solved by the fake provider on the COMPILED
             context instead of the whole-file context pack, its context
             measurably smaller, with the omissions and size records written
             where the caller points — the feature's DONE condition.
Bundle:      C1 save this block · C2 mirror it · C3 apply the four authored
             live_review pairs · C4 the opt-in wiring in run_pingpong ·
             C5 the end-to-end test module · C6 the R-0281 one-line fix ·
             C7 plan · C8 handoff.
Change:      exactly these nine paths, nothing else:
             .agent/authored/f107-r11-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, the four pairs below ONLY)
             packages/orchestration/pingpong_loop.py (C4)
             tests/orchestration/test_context_compiler_e2e.py (new, C5)
             tests/orchestration/test_context_compiler.py (C6, ONE line)
             .agent/plan.md (C7, full replacement by slice PLAN11)
             .agent/handoff.md (C8)

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit, one
   logical step per commit, push after the last one, clean tree at handback.
   Never work on main, never force-push, never amend, rebase or revert.
 - Do-not-touch (docs/roadmap/features/T2_F107.md): prompt composition,
   retrieval/embedding approaches, repo-map features. Reject any TS parser
   dependency. Do NOT edit `docs/roadmap/ROADMAP.md`.
 - `packages/orchestration/context_compiler.py` is FROZEN this round: R11
   CONSUMES it and adds nothing to it. `apps/cli/commands/job_context_cmd.py`
   and `docs/` are equally out of scope.
 - THE DEFAULT PATH MUST NOT MOVE. With the new parameters unset, every byte
   `run_pingpong` produces stays what it is today, which is why gate f re-runs
   the module's own suites as a regression gate and not as a formality.
 - `packages/` NEVER imports from `apps/`. The candidate listing is passed IN,
   the same way `compile_task_context` deliberately never walks a tree.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line or field that does not exist, STOP that item, do the
   safe thing, and DECLARE the correction in the handback — that is wanted
   behaviour. Findings R-0274, R-0277, R-0278 and R-0280 all record reviewer
   block errors that a worker was right to report rather than route around.

Detail for C4 — packages/orchestration/pingpong_loop.py:
 The assembly point is already located; do not go looking for another one.
 `build_repo_context` (pingpong_loop.py:694) returns `(context_text,
 categories)`, `run_pingpong` calls it at pingpong_loop.py:2653, and that
 `context` string becomes the `builder_context` segment at rank JOB_CONTEXT in
 `compose_builder_prompt` (pingpong_loop.py:878). F107 replaces that SELECTION,
 never the formatting.
 - Add THREE keyword-only parameters to `run_pingpong`
   (pingpong_loop.py:2418), each defaulting to today's behaviour:
     `compiled_context_paths: list[str] | None = None`   — the task's fenced
        scope, i.e. its `files_hint`;
     `compiled_context_candidates: list[str] | None = None` — the repo listing;
     `context_record_dir: str | Path | None = None`      — where the two
        records go, or None to write nothing.
 - At the context-build site (the `try` block at pingpong_loop.py:2651-2665):
   when BOTH `compiled_context_paths` and `compiled_context_candidates` are
   non-empty, compile with `compile_task_context(repo_path, paths, candidates)`
   and use `render_compiled_context_text(repo_path, compiled)` as `context`,
   with `categories = ["compiled_context"]`. In EVERY other case call
   `build_repo_context` exactly as today — including when only one of the two
   lists is given, which is a caller mistake and must not silently half-compile.
 - Import the compiler INSIDE that branch, the way this module already imports
   `build_scope_contract_for_builder` locally at pingpong_loop.py:2694, so the
   default path's import cost does not change.
 - Records: only when the compiled branch ran AND `context_record_dir` is set,
   write `write_omitted_context_json` to `<dir>/OMITTED_CONTEXT_FILENAME` and
   `write_context_size_comparison_json` of
   `compare_context_size(repo_path, candidates, compiled)` to
   `<dir>/CONTEXT_SIZE_FILENAME`. Use the two name constants, never a literal
   filename. Writing nowhere is the default and writing outside that directory
   is never correct.
 - One WHY line above the branch, and one deliberate-absence sentence a searcher
   will find: `run_pingpong` does NOT list the repo itself and does NOT read a
   task's `files_hint` — both are the caller's, which is what keeps this
   opt-in and keeps `packages/` free of a second tree walk.
 - Keep `result.context_categories` and `result.context_chars` doing exactly
   what they do now (pingpong_loop.py:2664-2665); they are the measurement the
   end-to-end test reads.

Detail for C5 — tests/orchestration/test_context_compiler_e2e.py (new):
 A REAL tmp_path git-less fixture repo — a fenced file importing a neighbor, the
 neighbor, a distant module reached only through the neighbor, one unrelated
 module and a README — plus `FakeProvider`
 (packages/orchestration/pingpong_provider.py:156) as both builder and reviewer.
 Assert on REAL VALUES, never truthiness, and never recompute an expected number
 with the same expression the code uses. Cover at least:
 1. THE DONE CONDITION: one baseline run with the new parameters unset and one
    compiled run with them set, same fixture and same provider — the compiled
    run's `result.context_chars` is strictly LESS than the baseline's, both are
    greater than 0, and the compiled run reaches the SAME literal
    `final_status` string the baseline reaches, so the task is still solvable;
 2. the compiled run's `result.context_categories == ["compiled_context"]`,
    and the baseline run's is whatever `build_repo_context` returns today —
    assert the baseline list is unchanged rather than pinning it to a guess;
 3. with `context_record_dir` set, both records exist and carry real values:
    the size record's `compiled_tokens` equals the compiled context's
    `estimated_tokens`, its `saved_tokens` is greater than 0, and the omissions
    record names the unrelated module with reason `distance`;
 4. with `context_record_dir` unset, the compiled run writes NEITHER file;
 5. giving only ONE of the two lists leaves the default path in charge — the
    categories are the baseline's, not `["compiled_context"]`.

Detail for C6 — the one-line R-0281 fix:
 `tests/orchestration/test_context_compiler.py:801` calls
 `write_omitted_context_json` "The one writing function". Make that line true
 again; change nothing else in the file.

<<<BEGIN SLICE HDR2FROM sha256=9e0d720df7cbda0d59aa86945a0af066dba0d54226f23dfa52f9a9e15a94449f lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0280.
<<<END SLICE HDR2FROM>>>
<<<BEGIN SLICE HDR2TO sha256=f538e69d732216c02a2cbbe84f580095a5bb066fb2b1812babc020f96f1384f0 lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0282.
<<<END SLICE HDR2TO>>>
<<<BEGIN SLICE LRF7FROM sha256=bfec9b2ce4ab3e91d1511ebd78874ecb9afa92eb72e82377b08bbaf5b46b3028 lines=1>>>
  scope, which is exactly right. R10 C6 fixes it. OPEN.
<<<END SLICE LRF7FROM>>>
<<<BEGIN SLICE LRF7TO sha256=89279b5d1d82881bd4b20b006cd2d2ade69b90497fdf8cd1b0aab935096a8196 lines=19>>>
  scope, which is exactly right. R10 C6 fixes it. OPEN.
- R-0280 (Medium, F107 R10): the R10 block contradicted itself about which
  commit carries the two `docs/README.md` pairs — its Bundle line and Change
  list put that file in C6, while PROCEDURE step 3 and gate c put all six pairs
  in C3. Applied as step 3 read it, C3 would have added an index row pointing at
  a guide that only C6 creates, and
  `tests/docs/test_docs_consistency.py:276` (`TestPrimaryDocLinksResolve`)
  asserts every relative link in `docs/README.md` resolves — so C3, C4 and C5
  would each have been committed on a RED docs suite. The worker took the safe
  reading, put the rows in C6, and declared both readings. Same class as
  R-0274: a block that says two different things costs the round a deviation to
  prove the reviewer wrong. OPEN.
- R-0281 (Low, F107 R10): `tests/orchestration/test_context_compiler.py:801`
  still calls `write_omitted_context_json` "The one writing function", which
  stopped being true when C4 added `write_context_size_comparison_json`. C4
  corrected the same stale absolute claim in two module docstrings; the test's
  copy survived because C5's own constraint was append-only, so the worker
  flagged it instead of editing outside its instruction. The stale-claim class
  is worth one line: the next reader trusts it. Fixed in this round's C6. OPEN.
<<<END SLICE LRF7TO>>>
<<<BEGIN SLICE LR10FROM sha256=a837f435ff66071bcb993ff9b921dbcd5dde9270ed45e0a68d55cf537abfea9a lines=1>>>
  `LAST_REVIEWED_SHA` advances 7acb406d -> f86bda87.
<<<END SLICE LR10FROM>>>
<<<BEGIN SLICE LR10TO sha256=7a8aa26e00cdcd482b4d3fdf7328f63972a7be4a03bdf1f3949e634cb00b4fca lines=37>>>
  `LAST_REVIEWED_SHA` advances 7acb406d -> f86bda87.

- Reviewer gate on R10 (2026-08-12): PASS. Range f86bda87..c50080e0 = eight
  commits touching exactly the nine paths the R10 block named. Transport by the
  PRIMARY shape: the reviewer original `.remedy-wt/f107-r10-1.block.md` is 312
  lines, its first 311 lines are byte-identical to BOTH
  `.agent/authored/f107-r11-1.md`'s predecessor `.agent/authored/f107-r10-1.md`
  and `.agent/last_block.md`, and all three sha256 to
  d0117326ae081a8d… — the value the original's own trailer declares. All
  thirteen slice bodies recompute to their BEGIN-marker digests at their
  declared lengths, and `sha256sum .agent/plan.md` returns the PLAN10 digest
  fd7a81e4… over 28 lines. Pair shapes were proven, not asserted: `git show
  --numstat 58742979 -- .agent/live_review.md` reads `79  1` — the single
  deletion being HDRFROM, the only REWRITE targeting that file — while LRF6, LR9
  and LRD2 each keep their FROM exactly 1x and their 28, 37 and 13 TO-only lines
  each occur exactly 1x among the 79 added lines; the only lines that fail an
  exactly-1x count are BLANK lines, which is the R-0253 case where whole-file
  and whole-diff counting bends rather than the text. 0 added lines belong to no
  TO body, and the same holds for `docs/README.md`, whose two rows arrive in C6
  with numstat `2  0`. Every scoped gate was RE-RUN by this reviewer: 61 passed
  on the compiler suite (55 before, +6), 9 passed on the CLI view, 42 passed on
  the canary, 294 passed on `tests/docs/`, `ruff check` "All checks passed!",
  tree clean, primary worktree alone, HEAD == origin. GATE j WAS RE-RUN, not
  read: compiling the same five-file fixture repo and calling
  `write_context_size_comparison_json` reproduces the handoff's file byte for
  byte — `whole_file_tokens` 215, `compiled_tokens` 164, `saved_tokens` 51,
  `saved_ratio` 0.2372093023255814 — the compiled figure equals the 164 the
  shipped CLI view prints, and the writer created its missing parent. The
  reviewer also ran TWO mutation probes the block did not order, in a disposable
  worktree at c50080e0, removed and pruned before this verdict: fabricating a
  1.0 ratio for a zero baseline gives `2 failed, 59 passed`, and clamping a
  negative saving to 0 gives `2 failed, 59 passed` — the new tests genuinely
  bite. The deviation that matters is the block's own self-contradiction over
  where the `docs/README.md` rows land, registered above as R-0280; the worker's
  reading was correct and its declaration is exactly the wanted behaviour. The
  stale claim it flagged rather than silently fixed is R-0281.
  `LAST_REVIEWED_SHA` advances f86bda87 -> c50080e0.
<<<END SLICE LR10TO>>>
<<<BEGIN SLICE LRD3FROM sha256=36e9a076b51a40f21b4d8e60d0f5441e09bb083c588e02fdc38f3b42bea6e9f7 lines=1>>>
is correct again, and this round allocates past it. Open findings 14 -> 13.
<<<END SLICE LRD3FROM>>>
<<<BEGIN SLICE LRD3TO sha256=ff528af9f55948399f0bf14268c584d26389f45348714296a2ea01a38fcb63bf lines=24>>>
is correct again, and this round allocates past it. Open findings 14 -> 13.

Done: R-0277 — RESOLVED. The R10 block's procedure step 1 no longer says
"below": it names the trailer line of `.remedy-wt/f107-r10-1.block.md` as the
digest's home and says in the same sentence that the trailer sits one line PAST
the saved region. The worker met the gate against that artifact without a
correction of its own, and this reviewer re-derived it independently — the
original's first 311 lines hash to d0117326ae081a8d…, which is what its line 312
declares. Open findings 15 -> 14.

Done: R-0278 — RESOLVED. Every zero-gate in the R10 block was anchored to the
line it is about rather than to the whole file, and the gate that used to be
unmeetable now measures what it means: `grep -c '^> Branch:.*Next free ID:
R-0277'` is 0 and `'^> Branch:.*Next free ID: R-0280'` is 1, both re-run by this
reviewer, while `.agent/live_review.md` still legitimately contains the string
`R-0277` inside R-0277's own body. The self-counting-gate class has a written
counter-measure that a block now demonstrably follows. Open findings 14 -> 13.

Done: R-0279 — RESOLVED. `remedy job context` is documented:
`docs/guides/job-context-view-user-guide-v0.md` exists at 184 lines and the
`docs/README.md` index carries its two rows (quick-find and guides table),
landing in C6 with numstat `2  0`. `python3 -m pytest tests/docs/ -q` returns
294 passed under this reviewer's own re-run, including the link-resolution check
that made the ordering matter. Open findings 13 -> 12.
<<<END SLICE LRD3TO>>>
<<<BEGIN SLICE PLAN11 sha256=1b01d7c9fa76a0a97a6830756a8810dfd63df8996efd84d124b83e35ab814260 lines=27>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0282. R10 reviewed PASS at c50080e0.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R11 — T004 part 2b-ii, the feature's DONE condition: `run_pingpong` gains an
OPT-IN compiled-context path, default off and byte-identical when unused, so a
fixture task runs on the compiled selection instead of the whole-file context
pack; the end-to-end test proves the fake provider still solves it and that the
context measurably shrank, and both records are written where the caller points.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md — the full suite, twice
   per feature, this being the first of the two.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line, then the PR. The branch has no PR yet
   and it is never merged in the session that creates it.
<<<END SLICE PLAN11>>>

PROCEDURE — in this order, one commit per numbered step:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r11-1.md`. The expected
    digest is the BLOCK_SHA256 line that the reviewer original
    `.remedy-wt/f107-r11-1.block.md` carries as its LAST line; that trailer sits
    one line PAST the region you save and is not part of the saved bytes. Verify
    BEFORE anything else; on mismatch STOP and report, never repair bytes.
    Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two, exit 0 and
    silent. Commit C2.
 3. Apply the four pairs to `.agent/live_review.md` by exact-string replacement
    of the FROM body with the TO body, verifying each slice's sha256 BEFORE use.
    HDR2 is a REWRITE (FROM and TO are disjoint); LRF7, LR10 and LRD3 are
    APPENDS (each TO literally contains its FROM). Commit C3 alone — findings
    persist before any code moves.
 4. C4, C5, C6 in that order, each its own commit, self-review loop before each.
 5. Replace `.agent/plan.md` entirely with slice PLAN11; `cmp` and `sha256sum`
    against the marker. Commit C7.
 6. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` (≤60 lines, or a declared
    stated-cause overage per AGENTS.md D15) and commit C8. Push.
 7. Do NOT write a `Done:` line of your own. If something lands that a finding
    covers, write `Landed: R-XXXX — <one line>` and nothing else.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r11-1.md .agent/last_block.md` → exit 0, silent;
    `sha256sum` of both == the BLOCK_SHA256 trailer named in step 1.
 b. Each of the nine slice bodies recomputes to its BEGIN-marker digest at its
    declared line count.
 c. `git show --numstat <C3> -- .agent/live_review.md` → the deletion column is
    exactly 1, HDR2 being the only REWRITE. Then, LINE-ANCHORED so no finding
    body that quotes a string can pollute a count (finding R-0278):
    `grep -c '^> Branch:.*Next free ID: R-0282'` → 1;
    `grep -c '^> Branch:.*Next free ID: R-0280'` → 0; `grep -c '^- R-0280'` → 1;
    `grep -c '^- R-0281'` → 1; `grep -c '^Done:'` → 7; `grep -c '^Landed:'` → 0;
    `grep -c '^## Steps'` → 1; `grep -c '^<<<'` → 0 (also 0 in `.agent/plan.md`
    and `.agent/handoff.md`).
 d. `python3 -m pytest tests/orchestration/test_context_compiler_e2e.py -q` →
    exit 0, and report the passed count.
 e. `python3 -m pytest tests/orchestration/test_context_compiler.py -q` → exit
    0, 61 passed.
 f. THE REGRESSION GATE, because C4 edits the loop every job runs through:
    `python3 -m pytest tests/orchestration/test_pingpong.py
    tests/orchestration/test_pingpong_integration.py -q` → exit 0, 43 passed —
    the count measured on this branch at c50080e0 BEFORE C4. A different number
    is a finding, not a rounding.
 g. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42
    passed.
 h. `python3 -m ruff check packages/orchestration/pingpong_loop.py
    tests/orchestration/test_context_compiler_e2e.py
    tests/orchestration/test_context_compiler.py` → exit 0.
 i. PROBE, inside a disposable `git worktree` at HEAD and nowhere else: make the
    compiled branch fall through to `build_repo_context` as though
    `compiled_context_paths` were never passed, and report WHICH tests fail and
    how many, or report that none do. A green probe is a true answer about a gap
    in C5, not a failure — report it either way, then remove and prune the
    worktree.
 j. THE REAL RUN, and this one decides the round: from a scratch directory under
    the gitignored `.remedy-wt/`, run the fixture end to end TWICE — once
    baseline, once compiled with `context_record_dir` set — and paste into the
    handoff, verbatim: both runs' `final_status` and `context_chars`, the
    resulting `context_size.json`, and the omissions entry for the unrelated
    module. A passing test module is NOT this gate: the round exists to prove
    the fixture task is still solved on a context that measurably shrank.
 k. `git status --porcelain` → empty; `git worktree list` → primary checkout
    alone; HEAD == origin/feature/f107-context-compiler-v2; insertions per
    commit, each < 500.
 l. `git diff --name-only c50080e0..HEAD` → exactly the nine paths of the Change
    list, nothing else.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C8, and every gate above with its real exit code and counted
value. Declare any deviation; a declared deviation costs nothing, an undeclared
one costs the round.
──────────────────────────────────────────────────────────────
