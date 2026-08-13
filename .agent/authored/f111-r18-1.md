── STEP T003-c / F111 — Round 18 (SESSION CLOSING) ───────────
Goal:
  Record the R17 verdict, then close T003 with the MEASUREMENT the feature's
  DONE line asks for: a repair round records what the diff path actually sent
  against what the full-file path would have sent, and a fixture test proves
  the diff path costs a fraction of it. Per DECISION F111 D9 these are
  CHARACTER counts and are named as such — this repository has no tokenizer,
  so a field named `tokens` would carry a fabricated number.

Bundle (ordered; one commit each, push after EVERY commit per R-0289):
  C1  save this block verbatim to .agent/authored/f111-r18-1.md
  C2  mirror the same bytes into .agent/last_block.md
  C3  .agent/live_review.md, TEXT-A appended, one commit
  C4  the denominator, in packages/orchestration/builder_bridge.py
  C5  tests, in tests/orchestration/test_builder_repair_loop.py
  C6  replace .agent/plan.md with TEXT-B, then rewrite .agent/handoff.md

Scope — EXACTLY these seven paths, no others:
  1 .agent/authored/f111-r18-1.md   2 .agent/last_block.md
  3 .agent/live_review.md           4 packages/orchestration/builder_bridge.py
  5 tests/orchestration/test_builder_repair_loop.py
  6 .agent/plan.md                  7 .agent/handoff.md

Change — C4, packages/orchestration/builder_bridge.py. Two edits, no others.

  EDIT 1 — one new module-level private helper, directly above
  `_attach_diff_repair_hunks`, with the one-line WHY comment above the def:

    def _repair_payload_chars(repo_root: Path, paths: list[str]) -> int:
        """Characters the FULL-FILE path would have sent for these paths.

        Unreadable and missing paths contribute nothing rather than raising:
        this number exists to be compared, and a measurement that can crash
        the repair loop is worse than one that undercounts a file it cannot
        read.
        """

  It sums `len((repo_root / rel).read_text(encoding="utf-8"))` over `paths`,
  catching `OSError` and `UnicodeDecodeError` per path and continuing.

  EDIT 2 — in `_attach_diff_repair_hunks`, on the DIFF branch only, add ONE
  key to the returned metadata dict, beside the existing `total_chars`:

    "full_file_chars": _repair_payload_chars(repo_path, sorted(ranges)),

  Add a one-line comment naming the pair: `total_chars` is what the diff path
  SENT, `full_file_chars` is what the full-file path WOULD have sent, and
  Remedy deliberately does not record a derived `chars_saved` field — a
  derived number can disagree with its own inputs, and the reader subtracts.
  Per DECISION F111 D9 both are CHARACTERS, never tokens.

  Change NOTHING else: not the full_file branches, not the loop, not the diff
  channel from R17, and nothing outside this file.

Change — C5, tests/orchestration/test_builder_repair_loop.py:
  Add ONE new fixture builder and TWO tests. Do not modify the twelve tests
  already in the file.

  The fixture builder lays down a calc.py LARGE enough for the saving to be
  real — the existing 7-line `_DIFF_CALC_SOURCE` is smaller than one
  margin-expanded hunk, so it cannot demonstrate a fraction of anything. Build
  a calc.py of at least 60 lines where the function under repair sits in the
  MIDDLE, so a margin-3 hunk carries roughly 7 lines out of 60. State that
  reasoning in the builder's docstring: the file size is the point of the
  fixture, not incidental.

  1. `test_the_diff_payload_is_a_fraction_of_the_full_file_payload`
     Drive the loop over the large fixture so cycle 1 applies a diff patch and
     fails, producing a diff-mode repair context. Read the
     `repair_mode_selected` event and assert its metadata carries BOTH
     `total_chars` and `full_file_chars`; that `full_file_chars` is greater
     than zero; and that `total_chars * 4 < full_file_chars` — a real fraction,
     not merely "less than". Put the two measured values into the assertion
     message so a failure PRINTS the numbers rather than hiding them. This is
     the feature file's "measured, recorded" DONE line; the comment above the
     assertion says so and cites DECISION F111 D9 for why they are chars.
  2. `test_the_full_file_denominator_is_the_bytes_actually_on_disk`
     Same drive. Assert `full_file_chars` equals the real character length of
     calc.py as it stands when the repair context is built — read the file and
     compare. This pins the denominator to something measured rather than
     estimated, which is the only thing that makes the ratio above meaningful.

  Read events with `packages.orchestration.timeline.load_run_events`.

Constraints:
  - SPLIT round. You are the worker; you make every commit. AGENTS.md is the
    highest authority: self-review loop before every commit, plan.md current,
    clean tree, push after each commit.
  - Never work on main, never force-push, never merge. No PR this round.
  - Destructive checks run ONLY inside a disposable `git worktree`, removed
    before the handback. `git status --porcelain` in the primary checkout is
    empty at every commit and at the handback. NOTE: `cd` may not take effect
    in some shells here — use absolute paths, verify with `pwd` before any
    mutation, and re-check `git status --porcelain` in the primary checkout
    immediately after.
  - Do NOT write a `Done:` paragraph of your own in `.agent/live_review.md`
    (planner_reviewer_prompt.md §4.4). If you land a fix this block did not
    order, mark it `Landed: R-XXXX — <one line>` instead.
  - Apply TEXT-A and TEXT-B BYTE FOR BYTE. If a text violates a rule, do not
    repair it — apply it and declare the deviation.
  - Do NOT touch docs/, docs/roadmap/, or STATUS.md this round. The feature's
    documentation and its STATUS line belong to the closure round, which the
    next session runs under docs/roadmap/STATUS_closure_protocol.md.
  - If any gate is red, or the block contradicts the code you find, stop at
    that point, commit what is clean, and say so in the handback. Do not widen
    scope to route around it.

Done when — every command run for real, exit code recorded, no value guessed:
  a. TRANSPORT: `sha256sum .agent/authored/f111-r18-1.md .agent/last_block.md`
     -> both digests identical, `cmp` exits 0. State the digest, the byte count
     and `wc -l`, which must be under 400.
  b. `.agent/live_review.md`: `grep -c '^Done:'` -> 11 (unchanged, no finding
     resolved this round); `grep -c '^- R-0'` -> 42 (unchanged);
     `grep -c '^### R17 — PASS'` -> 1; `grep -c '^Landed:'` -> prints 0.
  c. `grep -c '_repair_payload_chars' packages/orchestration/builder_bridge.py`
     -> 2 (the def and the one call site).
     `grep -c 'full_file_chars' …/builder_bridge.py` -> report the real number.
     `grep -c 'tokens' …/builder_bridge.py` -> MUST print 0. A token-named
     field would be a fabricated number (DECISION F111 D9).
  d. VALUE PROBE: print the `repair_mode_selected` metadata's `total_chars`,
     `full_file_chars`, and the ratio `full_file_chars / total_chars` rounded
     to one decimal. Paste the exact printed values. Also print the real
     character length of calc.py at that moment and confirm it equals
     `full_file_chars`.
  e. `python3 -m pytest tests/orchestration/test_builder_repair_loop.py -q`
     -> 14 passed (was 12).
  f. `python3 -m pytest tests/orchestration/test_diff_repair.py
     tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_diff_repair_apply.py -q` -> 71 passed, unmoved.
  g. IMPORT FALLOUT, the same nine files as R17: was 137 passed, 1 skipped.
     Report the real numbers; any drop is a finding, report it.
  h. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed.
  i. MUTATION PROBE, in a disposable worktree only: make
     `_repair_payload_chars` return a constant 1 and report WHICH tests fail
     and how many. Report the real result whatever it is; if nothing fails,
     say so, because that would mean the denominator is unpinned and is a
     finding, not your fault. Remove the worktree and show `git worktree list`.
  j. `git status --porcelain` -> empty. `git diff --name-only 6a93ee1c..HEAD`
     -> exactly the seven scoped paths. Per-commit insertions from
     `git log --numstat`, each under 500.
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> 0 and 0 after the final push.

Handback: completion report + rewrite .agent/handoff.md (item-status table for
C1-C6, changed-files table, the ten gate results a-j with their real values,
open-findings count, next expected action). Repeat the Fortschritt line from
TEXT-B verbatim. Do not write your own insertion count for C6 inside C6.

This is the SESSION-CLOSING round. The handoff must additionally carry a
NEXT SESSION block stating: the branch is UNMERGED with NO PR by design, so
Phase 0 must sweep `feature/*` branches to find it because a PR list will not
show it; the R18 verdict is gated by the next session's first block, exactly
as R15's was; and what remains is the integration gate
(docs/agents/integration_gate.md), the feature's documentation update, and
closure under docs/roadmap/STATUS_closure_protocol.md. Per
docs/agents/planner_reviewer_prompt.md §4.13 the next session must NOT open a
repair round merely to close R18.

──────────────────────── TEXT-A — append to .agent/live_review.md ───────────

### R17 — PASS (2026-08-13)
Reviewed by the main session over c0ed5dd1..6a93ee1c. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport:
`.agent/authored/f111-r17-1.md` and `.agent/last_block.md` are byte-identical
under `cmp`, 20623 bytes, 366 lines, sha256
a21506ddee38218bba4c6fb0f051c6b175d1eeaadffe8c476af3096598a07332, no line
carrying trailing whitespace. `.agent/plan.md` was compared against the TEXT-B
slice extracted from the committed authored file and is identical at 44 lines,
under the 50-line cap. Markers counted: eleven resolution paragraphs, 42
registered findings, one R16 gate heading, zero unreviewed-fix markers. Greps:
`diff_repair_fell_back` 2, `diff_repair_applied` 1, `diff_response` 10. Scope:
exactly the seven ordered paths. Per-commit insertions 366/305/71/95/164/101,
each under 500. `git status --porcelain` empty, one worktree, and 0 ahead and
0 behind the remote.

Tests re-run by the reviewer: 12 for the repair loop (was 9), 71 for the three
diff-repair files — unmoved — 137 passed and 1 skipped across the nine files
that import `builder_bridge`, and 42 for the golden-path canary. The three new
module-level diff-repair imports introduced no cycle.

The reviewer ran an INDEPENDENT conflict probe using a different conflicting
diff than the test uses — a rewritten function-signature context line rather
than an added parameter — and it reproduces the ordered behaviour exactly:
mode `full_fallback`, `fallback_reason`
`apply_failed:calc.py: diff hunks did not apply cleanly`, `files_modified` 0,
`rollback_incomplete` False, the file's bytes IDENTICAL across the attempt, the
next repair context back on `full_file` carrying that reason, and the loop
still succeeding on the following cycle through the full-file path. The
`apply_failed:` prefix is the load-bearing detail: the diff reached the
applicator and was rejected there, so this is the strict-apply guarantee being
exercised and not a cheap short-circuit at the validation stage.

A second reviewer mutation, unordered, ran inside a disposable git worktree
removed before this verdict: deleting the `repair_ctx["repair_mode"] =
"full_file"` line after a discard fails
`test_a_conflicting_diff_is_discarded_whole_and_the_round_falls_back` with
`KeyError: 'repair_mode'`. So the return to the full-file path is pinned, not
merely written. The worker's own ordered mutation is confirmed as reported: a
rejected diff made to look applied fails exactly that one test, and the worker
correctly reported that no other suite catches it rather than implying broader
cover.

The declared C5 deviation is UPHELD and is the round's best work. The block
said to read calc.py "before the loop" and compare bytes; read literally that
would have measured cycle 1's own legitimate write, because a diff-mode repair
context cannot exist until a first patch has landed. The worker recorded the
file as each cycle FOUND it and compared the bytes the discarded attempt
started from against the bytes the next cycle found — the true pre- and
post-attempt state — while keeping the literal pre-loop comparison as an extra
assertion. That is the correct reading of a reviewer instruction that was
imprecise, implemented without weakening the property and declared rather than
quietly substituted. The handoff overage at 85 lines is inside the DECISION D15
allowance with its cause named, and no section was dropped.

──────────────────── TEXT-B — full replacement of .agent/plan.md ────────────

# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 6a93ee1c (R17 PASS).
Next free finding ID: R-0318. Open findings: 31 — 42 registered minus
11 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R18 closes T003 with the measurement the feature's DONE line asks
for. `_repair_payload_chars` computes what the full-file path WOULD
have sent for the same paths, the diff round records it beside the
`total_chars` it actually sent, and a large-file fixture test proves
the diff payload is a fraction of it. Per DECISION F111 D9 these are
CHARACTER counts, never tokens: this repository has no tokenizer.
T001, T002 and T003's prompt and apply halves are complete and gated.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md — the full
   suite, base against branch, with the five known base failures
   (R-0286) attributed rather than assumed.
2. The feature's documentation update, then closure under
   docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH
   review zip, the authored STATUS line, and the PR.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch and
  attributes every branch-only failure before any closure claim.
- The saving is measured in characters, not tokens. Any later doc or
  STATUS line that calls these numbers tokens turns an honest
  measurement into a fabricated one.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.

Fortschritt: ~92 % (T001 ✅ · T002 ✅ · T003 ✅ komplett · Integration Gate
offen · Closure offen) — Schätzung
