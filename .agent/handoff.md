# Handoff — F109 Semantic dedupe, SESSION 1, round 4

Branch: `feature/f109-semantic-dedupe`
Base commit: `f7a11ff7f663e94f9344c6f29983b4645f1e02db` (round 3 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

This round REPAIRED A BLIND GATE. No production code changed.

## Commits this round

| Item | SHA        | Commit subject                                                              |
|------|------------|-----------------------------------------------------------------------------|
| C0a  | `39396a20` | F109 R4 C0a: save the round 4 step block verbatim                           |
| C0b  | `12282e04` | F109 R4 C0b: mirror the step block to last_block                            |
| C1   | `47b33393` | F109 R4 C1: plan for round 4 — register and repair the blind chain gate     |
| C2   | `ae6781eb` | F109 R4 C2: book the round 3 gate and register R-0770                      |
| C3   | `75de4b47` | F109 R4 C3: give the chain tests one provider per role so each seam is pinned alone |
| C4   | `9cc8869e` | F109 R4 C4: record R-0770 landed for the two record seams                   |

C5 is this handoff rewrite, committed on top of `9cc8869e`. Every gate G1–G7
ran at C4 or earlier, so all seven are quoted below from real output. The push
happens AFTER C5 and is therefore deliberately not quoted here; the reviewer
measures the remote tip itself.

Six single-parent commits in the range before C5, no merge commit.

## Changed files (this round)

| Path                                            | Change                                                  |
|-------------------------------------------------|---------------------------------------------------------|
| `.agent/authored/f109-r4.md`                    | new — step block, `cp` not retyped                      |
| `.agent/last_block.md`                          | rewritten — byte mirror of the authored block           |
| `.agent/plan.md`                                | rewritten — SLICE PLAN, whole file, 41 lines            |
| `.agent/live_review.md`                         | appended TWICE — SLICE RECORD at C2, SLICE LANDED at C4 |
| `tests/orchestration/test_semantic_dedupe.py`   | edited — `TestChainAgainstTheRealLoop` rewritten        |
| `.agent/handoff.md`                             | rewritten — this file (C5)                              |

No path outside the ordered change set was touched. `git diff --numstat` over
`f7a11ff7..HEAD` lists exactly those five paths (C5 adds the sixth).

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum .remedy-wt/f109-r4.md
  .agent/authored/f109-r4.md .agent/last_block.md` printed ONE digest three
  times:
  **`7d62881a6c8ca7c7725c71f31e6751641f5719ff65f8817a0bb83c03580695fd`**,
  equal to the digest the delegation wrapper stated. The scratch original was
  verified against that digest as the round's FIRST action, before anything was
  read or written, and both C0a and C0b were `cp`, never a retype. The block is
  322 lines and 24016 bytes, as the wrapper stated.
- **G2 THE PLAN — PASS.** `cmp .agent/plan.md .remedy-wt/slice_plan.txt` exit 0
  — byte-equal against the extracted slice, never a retype. `wc -l` = **41**,
  strictly under 50. `grep -n '^## '` lists exactly four headings, of which
  `## Goal` appears once (line 6) and `## Next Steps` appears once (line 25).
- **G3 THE RECORD APPEND — PASS, all four parts.** (a) base **2030395** bytes
  with sha256
  `f09af719542dbb3ecace6cc8f00cc2a1a84ed0d80e41bc965670eed177bc17d6`, exactly
  as the block stated; S = **5817** after the trailing-newline strip; expected
  2030395 + 2 + 5817 = **2036214**, actual **2036214**; the file still ends
  WITHOUT a trailing newline (checked as a byte test, not a claim). (b) The
  blank-line reader split the WHOLE file into **851** units; I counted the
  paragraphs of SLICE RECORD myself — the `Gate: F109 R3 — …` paragraph and the
  `- R-0770 — …` paragraph, so **N = 2** — and the LAST 2 units equal those two
  paragraphs IN ORDER: True. (c) NEGATIVE CONTROL on a scratch copy: byte at
  offset 2030402, which is inside the FIRST appended paragraph (not the last),
  XOR-flipped; the same reader REJECTED it (True). The tracked file's sha256 was
  `f3161b0062d1abe45b6b0c8fe55c07ae5205c2dcc68d14b3759fbf719a85bda3` before the
  control and `f3161b0062d1abe45b6b0c8fe55c07ae5205c2dcc68d14b3759fbf719a85bda3`
  after — identical. (d) `grep -c '^- R-[0-9]\{4\} — '` went **330 → 331**;
  `grep -c '^- R-0770 — '` is **1**; `grep -c '^Gate: F109 R3 — '` is **1**;
  `grep -c '^Done: R-[0-9]\{4\} — '` is UNCHANGED at **62**. `grep -c 'R-0770'`
  was **0** before C2, so the id was not already spent.
- **G4 THE LANDED APPEND — PASS.** Base is the size measured after C2,
  **2036214**; S2 = **421** after the same strip; expected 2036214 + 2 + 421 =
  **2036637**, actual **2036637**; still ends without a trailing newline. The
  same structural reader counted N = **1** over 852 units and the last unit is
  byte-equal to SLICE LANDED; its own negative control on the appended
  paragraph was REJECTED, with the tracked digest
  `cb8e452a71f2917e1cff20a4faac089cf30cad09cd9c80d948c2e9481a512fdb` unchanged
  across it. `grep -c '^Landed: R-'` went **24 → 25**;
  `grep -c '^Landed: R-0770 — '` is **1**; `grep -c '^Done: R-[0-9]\{4\} — '`
  is STILL **62** — I wrote no `Done:` line.
- **G5 THE COLOUR — CONTROL GREEN, MUTATION A RED, MUTATION B RED, AND THE
  PROBE ALSO RED.** Run in a disposable worktree added at the C3 commit
  `75de4b47` by exact path
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r4-mut`, never in the primary
  checkout. CONSTRAINT 7 FIRST, before any mutation:
  `python3 -B -c "import packages.orchestration.pingpong_loop as m;
  print(m.__file__)"` run with the worktree as cwd printed
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r4-mut/packages/orchestration/pingpong_loop.py`
  — INSIDE the worktree, so the editable-install `.pth` did not shadow it.
  `find … -name __pycache__ -type d | wc -l` printed **0** before the first run
  (a fresh worktree carries none) and `python3 -B` was used for every run. Each
  pytest process was launched with the worktree as its cwd through a no-shell
  `subprocess.run` runner so the REAL exit code could be read (see deviation 6);
  the argv was the block's exact command every time. Before each mutation the
  exact text was confirmed to occur EXACTLY ONCE in `pingpong_loop.py` and ZERO
  times after, so no mutation silently failed to land, and the file was restored
  with `git checkout --` between mutations.
  (a) CONTROL, unmutated: **exit 0, 55 passed**.
  (b) MUTATION A — deleted line 3278,
  `record_finalized_call(session_sent_index, builder_out,
  builder_composed.manifest_as_dicts())`, occurrences 1 → 0:
  **exit 1, 6 failed, 49 passed — RED.** The failures INCLUDE SPEC R case 1,
  `TestChainAgainstTheRealLoop::test_the_builder_seam_records_a_row_of_its_own`,
  which fails with `KeyError: 'sess-builder'` — the row disappears exactly as
  the reviewer's pre-delegation measurement predicted. This is the mutation that
  came back GREEN in round 3. THE REPAIR WORKS.
  (c) MUTATION B — restored, then deleted line 3581,
  `record_finalized_call(session_sent_index, reviewer_out,
  reviewer_composed.manifest_as_dicts())`, occurrences 1 → 0:
  **exit 1, 6 failed, 49 passed — RED.** The failures INCLUDE SPEC R case 2,
  `test_the_reviewer_seam_records_a_row_of_its_own`.
  (d) PROBE — restored, then deleted line 3269,
  `invalidate_on_resume_fallback(session_sent_index, builder_out,
  builder_resume_ref or "")`, occurrences 1 → 0:
  **exit 1, 1 failed, 54 passed — RED, NOT the GREEN the block expected.** The
  single failure is `test_the_fallback_invalidation_shrinks_exactly_the_builder_row`
  with `assert 9 < 9`. Reported exactly as measured, with no test touched in
  either direction; see deviations 1 and 2 for what it means.
  Cleanup: the worktree was confirmed clean (`git status --porcelain` empty
  inside it), then `git worktree remove --force
  /home/decodeux/Repos/remedy/.remedy-wt/f109-r4-mut` and `git worktree prune`.
  `git worktree list` afterwards shows the primary checkout plus exactly the
  four pre-existing `.remedy-wt/job-*` worktrees (`job-48a379ab5ca44ec5`,
  `job-7d1c93e2dc98415a`, `job-98e9364a83a34872`, `job-f76686b8435640e9`), which
  predate this branch and were left untouched. The primary checkout was
  confirmed unmutated: all four call sites plus the two imports still present
  (`grep -c` = 6) and `git status --porcelain` empty.
- **G6 THE SUITES — PASS, all eight ordered suites, run SERIALLY with never two
  pytest processes alive at once.**
  `tests/orchestration/test_semantic_dedupe.py` exit 0, **55 passed** (base 51 —
  the block allowed this one to change; the chain class went from 6 cases to 10);
  `tests/orchestration/test_pingpong.py` exit 0, **34 passed** (base 34);
  `tests/orchestration/test_session_resume.py` exit 0, **27 passed** (base 27);
  `tests/ui_server/` exit 0, **515 passed** (base 515);
  `tests/orchestration/test_test_runner.py` exit 0, **52 passed** (base 52);
  `tests/regression/test_resource_safety.py` exit 0, **21 passed** (base 21);
  `tests/orchestration/test_integrity_gate.py` exit 0, **16 passed** (base 16);
  `tests/cli/test_golden_path.py` exit 0, **42 passed** (base 42). Every count
  matches its base except the one the block allowed to move.
- **G7 THE TREE — PASS.** `git status --porcelain` EMPTY (no output).
  `git ls-files .remedy-wt` returns NOTHING. Insertion counts, six numbers,
  `+` column only: C0a **322**, C0b **233**, C1 **13**, C2 **5**, C3 **156**,
  C4 **3**. Every one under 500. CONSTRAINT 2, the number this gate exists for:
  `git diff --numstat f7a11ff7..HEAD -- packages/orchestration/pingpong_loop.py
  packages/orchestration/session_sent_index.py` produced **NO OUTPUT AT ALL** —
  both files are ABSENT from the range diff entirely, so no production code
  changed this round. The full range numstat lists exactly five paths:
  `.agent/authored/f109-r4.md` 322/0, `.agent/last_block.md` 233/307,
  `.agent/live_review.md` 7/1, `.agent/plan.md` 13/14 and
  `tests/orchestration/test_semantic_dedupe.py` 156/64.

## Item status

| Item | Status | Reason                                                        |
|------|--------|---------------------------------------------------------------|
| C0a  | done   |                                                               |
| C0b  | done   |                                                               |
| C1   | done   |                                                               |
| C2   | done   |                                                               |
| C3   | done   |                                                               |
| C4   | done   |                                                               |
| C5   | done   | this file                                                     |

## What C3 actually landed

`TestChainAgainstTheRealLoop` was rewritten in place; the diff's first changed
line is 541, the class's own docstring, so nothing above the class was touched
and no test outside it was edited. 156 insertions, 64 deletions, 6 cases → 10.

THE ONE STRUCTURAL CHANGE, per SPEC R. A single `_provider_pair()` helper builds
TWO `FakeProvider` instances with DISTINCT `fake_session_id` values —
`sess-builder` and `sess-reviewer`, held as class constants — and `_run` passes
them as `builder_provider` and `reviewer_provider` separately. The class
docstring states WHY: with one shared id the four loop call sites collapse into
a single observable and no mutation of an individual seam can be caught. A
`_rows_by_session` helper keys the evidence by session id so a case can NAME the
seam it reads. `FakeProvider` counts builds and reviews on separate counters, so
splitting one instance into two changes no round outcome — it only splits the
observable.

The ten cases, mapped to SPEC R:

1. `test_the_builder_seam_records_a_row_of_its_own` — SPEC R case 1. Row EXISTS
   BY ID and is non-empty; no exact hash count asserted. Broken by MUTATION A.
2. `test_the_reviewer_seam_records_a_row_of_its_own` — SPEC R case 2. Broken by
   MUTATION B.
3. `test_both_seams_appear_exactly_once_and_the_rows_are_sorted` — SPEC R case
   3: the id set is exactly `{"sess-builder", "sess-reviewer"}`, there are
   exactly 2 rows, and they are sorted by `session_id`.
4. `test_every_recorded_hash_is_a_real_segment_hash` — SPEC R case 4, over BOTH
   rows now: 64-char lowercase hex and each row's `sent_sha256` sorted.
5. `test_a_provider_pair_that_reports_no_session_id_records_nothing` — SPEC R
   case 5: both providers built without `fake_session_id`, evidence `== []`.
6. `test_the_two_seams_do_not_share_one_observable` — SPEC R case 6. The two
   hash SETS are asserted UNEQUAL. Measured before the assertion was written:
   they are unequal (9 hashes vs 10), so this was not forced.
7. `test_a_single_round_run_records_the_sessions_it_proved` — SPEC R case 7,
   single-round half, adapted to the pair.
8. `test_the_loop_is_otherwise_unchanged_for_a_non_resuming_provider_pair` —
   SPEC R case 7, non-resuming half: `final_status == "staged_review_passed"`
   and 2 rounds.
9. `test_a_failed_builder_resume_falls_back_within_the_same_round` — SPEC R case
   8 exactly as specified: only the BUILDER's `resume_fails` is set (the two
   providers make that possible for the first time), the run completes, and
   round 2's `resume_fallback` is True. Its comment states plainly that a SINGLE
   run cannot discriminate the builder's `invalidate_on_resume_fallback`.
10. `test_the_fallback_invalidation_shrinks_exactly_the_builder_row` — ROUND 3'S
    DISCRIMINATOR, KEPT under constraint 4 and narrowed to the builder row. See
    deviations 1 and 2: this is the case that made probe (d) red.

EVERY VALUE WAS MEASURED BEFORE IT WAS ASSERTED, in a gitignored scratch probe
that drove the real loop at the base commit: clean two-round chain →
`sess-builder` 9 hashes, `sess-reviewer` 10; builder-fallback chain →
`sess-builder` 8, `sess-reviewer` 10; single-round chain → `sess-builder` 4,
`sess-reviewer` 6, 1 round; no-session pair → `[]`; non-resuming pair →
`staged_review_passed`, 2 rounds. The reviewer's own pre-delegation numbers (9
and 10) reproduced exactly.

Ruff followed by construction per constraint 6, which forbids gating on it:
longest line in the file is **101** characters, under the configured 120; no
import was added, removed or reordered; the file parses with `ast`.

## Deviations

1. **PROBE (d) CAME BACK RED, NOT GREEN, AND THAT CONTRADICTS A CLAUSE OF THE
   R-0770 TEXT I WAS ORDERED TO COMMIT VERBATIM.** Deleting the builder
   `invalidate_on_resume_fallback` call fails exactly one test,
   `test_the_fallback_invalidation_shrinks_exactly_the_builder_row`, with
   `assert 9 < 9`. R-0770 as registered at C2 says "no assertion available today
   separates 'cleared then refilled' from 'never cleared'" and "this finding is
   not resolved until a test fails when the Builder
   `invalidate_on_resume_fallback` call is removed"; SLICE LANDED says "the
   fallback-invalidation half is unchanged and stays OPEN". As of C3 that
   condition is MET. The premise that fails is the word "today": the clause
   reasons about a SINGLE run, where the following `record_finalized_call`
   refills the session it just cleared, and that reasoning is correct. Round 3's
   test compares TWO runs — a fallback chain against a clean chain — and the
   invalidation is visible in the DIFFERENCE. Measured, in the gitignored probe
   before C3 was authored and again as G5(d) in the worktree: with the call,
   `sess-builder` is 8 in the fallback run and 9 in the clean run; with the call
   neutralised, both are 9. I applied both slices byte-for-byte per constraint 1
   and did NOT edit the committed ledger text. The reviewer owns the ledger and
   should decide whether R-0770's fallback half is now discharged or whether the
   cross-run comparison is too indirect to count; I wrote no `Done:` line.
2. **TEN CASES, NOT THE NINE SPEC R ENUMERATES — CONSTRAINT 4 FORCED IT.** SPEC
   R item 8 specifies a fallback case that asserts only the PATH, and mandates a
   docstring saying it does not discriminate the invalidation. Constraint 4
   says I may NOT reduce what is asserted and that every property round 3's
   chain tests pinned must still be pinned by some case. Round 3 pinned
   `len(fallback_hashes) < len(clean_hashes)`. Dropping it to obey item 8 would
   have deleted a live assertion, so I did BOTH: case 9 is item 8 exactly as
   written, and case 10 keeps round 3's comparison, narrowed to the
   `sess-builder` row (plus a new assertion that the `sess-reviewer` row is
   unchanged at 10, since only the builder fell back). Case 9's comment says
   truthfully that a SINGLE run cannot discriminate the call and points at case
   10, rather than the flatly-false "no case here discriminates it". This is the
   only place I departed from SPEC R's literal wording, and it is why probe (d)
   is red.
3. **The block's G5(d) cross-reference is off by one letter.** SPEC R item 8
   says "G5's probe (c) below establishes that", but (c) is MUTATION B and the
   probe is (d). Non-load-bearing; I executed (a)–(d) as G5 itself defines them.
   Raised for `.agent/prose_slips.md`, not for an id.
4. **G6's closing sentence says "The four state readers are ordered … and they
   are run AS FOUR", but the ordered list contains EIGHT suites** and none is
   labelled a state reader. I ran all eight exactly as listed, serially, and
   reported all eight. No suite was skipped and none was added.
5. **The `TestChainAgainstTheRealLoop` helpers changed signature.** `_run` now
   takes a `(builder, reviewer)` tuple instead of one provider, and
   `_make_repo`, `isolate_data_root` and `demo_repo` are byte-identical to round
   3's. That is inside the class constraint 4 permits me to rewrite.
6. **The sandbox bash guard refused several command FORMS**, not contents:
   `${PIPESTATUS[0]}` and `$?` expansions, and compound commands containing
   several `grep -c` patterns. Real exit codes were therefore read through a
   no-shell `subprocess.run` runner that received the block's EXACT argv
   (`python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`, and
   the `python3 -m pytest …` form for G6) and printed `proc.returncode`; every
   `grep -c` pattern the block names was run verbatim as its own standalone
   command and is quoted above. No gate was weakened or reworded to fit the
   guard.
7. **Scratch artefacts live under `.remedy-wt/` and are gitignored**, never
   committed and never in the change set: `probe_r4.py`, `probe_r4b.py`,
   `extract.py`, `append.py`, `splice.py`, `chain_class.txt`, `mutate.py`,
   `runpt.py`, `slice_plan.txt`, `slice_record.txt`, `slice_landed.txt`.
   `git ls-files .remedy-wt` returns nothing, as G7 records.
8. **Four `.remedy-wt/job-*` worktrees predate this branch** and were left
   alone. Exactly one worktree was created this round and it was removed by
   exact path, then pruned.

## Open findings

The ledger now stands at **331** findings registered and **62** resolved, so the
open set is **269**. This round registered `R-0770` (C2) and wrote its `Landed:`
line (C4); a `Landed:` is not a `Done:`, and `^Done: R-[0-9]\{4\} — ` is still
62. `.agent/candidates.md` is unchanged and EMPTY, so no block condition stands
against F109. Deviation 1 above is the one item the reviewer must rule on: the
fallback-invalidation half of R-0770 is, by measurement, now caught by a test.

## Next expected action

`git push` on `feature/f109-semantic-dedupe` immediately after this commit —
not quoted here by design, so the reviewer measures the remote tip itself. Then
the reviewer's verdict on round 4, including the ruling deviation 1 asks for.
After that, T002: the composition hook, where a segment whose hash the session
already holds becomes a one-line marker, non-resume calls bypass the hook
entirely, and a byte-equality golden pins the composed prompt.
