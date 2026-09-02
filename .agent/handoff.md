# Handoff — F109 Semantic dedupe, SESSION 1, round 2

Branch: `feature/f109-semantic-dedupe`
Base commit: `bdd628508408970e3eb519eb25bef88483e5168a` (round 1 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

## Commits this round

| Item | SHA        | Commit subject                                                      |
|------|------------|---------------------------------------------------------------------|
| C0a  | `596f84aa` | F109 R2 C0a: save the round 2 step block verbatim                   |
| C0b  | `34dac91d` | F109 R2 C0b: mirror the step block to last_block                    |
| C1   | `1381de9f` | F109 R2 C1: plan for round 2 — the finalized-call adapter           |
| C2   | `43a1c05d` | F109 R2 C2: book the round 1 PASS verdict into the ledger           |
| C3   | `b20b87f8` | F109 R2 C3: record two reviewer prose slips from round 1            |
| C4   | `364e113d` | F109 T001b-i C4: finalized-call adapters for the sent-hash index    |
| C5   | `a3fcda6f` | F109 T001b-i C5: tests for the finalized-call adapters              |

C6 is this handoff rewrite, committed on top of `a3fcda6f`. Every gate G1–G7
ran at C5 or earlier, so all seven are quoted below from real output. The push
happens AFTER C6 and is therefore deliberately not quoted here; the reviewer
measures the remote tip itself.

Seven single-parent commits, no merge commit in the range.

## Changed files (this round)

| Path                                            | Change                                                |
|-------------------------------------------------|-------------------------------------------------------|
| `.agent/authored/f109-r2.md`                    | new — step block, copied not retyped                  |
| `.agent/last_block.md`                          | rewritten — byte mirror of the authored block         |
| `.agent/plan.md`                                | rewritten — SLICE PLAN, whole file, 42 lines          |
| `.agent/live_review.md`                         | one paragraph appended — the round 1 gate entry       |
| `.agent/prose_slips.md`                         | two paragraphs appended — two reviewer prose slips    |
| `packages/orchestration/session_sent_index.py`  | added to — three adapters; docstring bullet reworded  |
| `tests/orchestration/test_semantic_dedupe.py`   | added to — SPEC B cases, 25 tests → 45                |
| `.agent/handoff.md`                             | rewritten — this file (C6)                            |

`git diff --name-only bdd62850..HEAD` returns exactly the seven paths above
(this file lands in C6). No path outside the ordered change set was touched.

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum` over `.remedy-wt/f109-r2.md`,
  `.agent/authored/f109-r2.md` and `.agent/last_block.md` gives the same digest
  for all three: `ff5ef37aab57bcd49acb964921f8cdf07d740670a35260a94c9e323265d25907`,
  equal to the digest the delegation wrapper stated. Verified BEFORE the round
  began; both C0a and C0b were `cp`, never a retype.
- **G2 THE PLAN — PASS.** `cmp .remedy-wt/plan_new.md .agent/plan.md` exit 0
  (byte-equal against the extracted slice, never a retype); `wc -l` = 42,
  strictly under 50; `^## Goal$` count 1 and `^## Next Steps$` count 1.
- **G3 THE VERDICT APPEND — PASS, all four parts.** (a) base 2018315 bytes with
  sha256 `3a5981497bb3ada18babe0a906f4c6160a42563671b1350001fac74b0d2bc90e` as
  stated, S = 6019 after the trailing-newline strip, expected 2018315 + 2 + 6019
  = 2024336, actual 2024336, and the file still ends WITHOUT a trailing newline.
  (b) The blank-line reader counted N = 1 paragraph in the slice itself (not
  taken from the block) over 848 units in the file, and the last 1 unit is
  byte-equal to it: `LAST_N_UNITS_EQUAL_SLICE=True`, exit 0. (c) Negative
  control on a scratch copy: one byte flipped at offset 2021326 inside the FIRST
  appended paragraph (`' '` → `'A'`) and the same reader REJECTED it
  (`READER_REJECTS_MUTATED_COPY=True`); the tracked file's sha256 was
  `5dc6aeb1b8bccae8c8c7593aa4bc623ac5b0349e50db2fdcc68c449c56ec4d25` both before
  and after, identical. (d) `^Gate: F109 R1 — ` is exactly 1 (it was 0 at base);
  `^- R-[0-9]\{4\} — ` UNCHANGED at 330; `^Done: R-[0-9]\{4\} — ` UNCHANGED at
  62. This round registers no finding and resolves none.
- **G4 THE SLIPS APPEND — PASS.** Base 40351 bytes with sha256
  `b00c1f249fce5ea243ea5963eee4453ac08a73fad1198c4b103f7e355e90e97c` as stated,
  S2 = 1363 after the same strip, expected 40351 + 2 + 1363 = 41716, actual
  41716, still ending without a trailing newline. The blank-line reader counted
  N2 = 2 paragraphs itself and the last 2 units of the file equal them IN ORDER:
  `LAST_N_UNITS_EQUAL_SLICE=True`, exit 0.
- **G5 THE COLOUR OF THE NEW CODE — PASS.** In a disposable worktree added at
  `a3fcda6f`, never in the primary checkout; `__pycache__` purged before every
  run and `python3 -B` used throughout. (a) CONTROL, unmutated: **exit 0, 45
  passed**. (b) MUTATION A, `ok=not getattr(output, "error", "")` inverted to
  `ok=bool(...)`: **exit 1, 3 failed / 42 passed**, and the failures INCLUDE the
  SPEC B item 5 case
  `test_an_errored_call_records_nothing_and_leaves_the_session_empty` (with
  `test_a_proven_call_records_every_hash_and_returns_record_calls_count` and
  `test_record_then_fallback_then_record_again`). (c) MUTATION B, restore then
  make `invalidate_on_resume_fallback` read only
  `getattr(output, "resume_session_ref", "")` and ignore `resumed_ref`: **exit
  1, 3 failed / 42 passed**, and the failures INCLUDE the SPEC B item 9 case
  `test_the_loops_replaced_output_invalidates_when_resumed_ref_is_passed` (with
  `test_a_fallback_empties_exactly_the_resumed_session` and
  `test_record_then_fallback_then_record_again`) — the third argument is
  therefore load-bearing, not decorative. (d) MUTATION C, restore then let a
  non-mapping `usage_actuals` propagate its exception: **exit 1, 2 failed / 43
  passed**, failing on exactly the SPEC B item 3 case, both parametrizations,
  `test_a_non_mapping_usage_actuals_reads_as_no_session_and_never_raises[7]` and
  `[usage_actuals0]`. Each mutation's anchor was asserted present AND unique
  before it was applied, so no mutation silently failed to land. Afterwards
  `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f109-r2-mut`
  and `git worktree prune`; `git worktree list` now shows the primary checkout
  plus exactly the four pre-existing `.remedy-wt/job-*` worktrees
  (`job-48a379ab5ca44ec5`, `job-7d1c93e2dc98415a`, `job-98e9364a83a34872`,
  `job-f76686b8435640e9`), which predate this branch and were left untouched.
  The primary checkout was confirmed unmutated: `git status --porcelain` empty
  and line 253 still reads
  `ref = (resumed_ref or getattr(output, "resume_session_ref", "")).strip()`.
- **G6 THE SUITES — PASS, all six, run SERIALLY with never two pytest processes
  alive at once.**
  `tests/orchestration/test_semantic_dedupe.py` exit 0, **45 passed** (base 25,
  GREW as ordered); `tests/ui_server/` exit 0, **515 passed** (base 515);
  `tests/orchestration/test_test_runner.py` exit 0, **52 passed** (base 52);
  `tests/regression/test_resource_safety.py` exit 0, **21 passed** (base 21);
  `tests/orchestration/test_integrity_gate.py` exit 0, **16 passed** (base 16);
  `tests/cli/test_golden_path.py` exit 0, **42 passed** (base 42). Every count
  matches its base except the one ordered to grow. The three property guards
  named in constraint 10 live in `test_test_runner.py` and all 52 pass, so the
  adapters satisfy them.
- **G7 THE TREE — PASS.** `git status --porcelain` EMPTY (no output).
  `git ls-files .remedy-wt` returns NOTHING — the scratch directory is
  gitignored and untracked. Insertion counts, seven numbers, `+` column only:
  C0a **372**, C0b **306**, C1 **15**, C2 **3**, C3 **5**, C4 **90**,
  C5 **202**. Every one under 500. The C6 handback commit's own count is not
  owed and is not reported.

## Item status

| Item | Status | Reason                                                        |
|------|--------|---------------------------------------------------------------|
| C0a  | done   |                                                               |
| C0b  | done   |                                                               |
| C1   | done   |                                                               |
| C2   | done   |                                                               |
| C3   | done   |                                                               |
| C4   | done   |                                                               |
| C5   | done   |                                                               |
| C6   | done   | this file                                                     |

## What C4 actually landed

Three functions added to `packages/orchestration/session_sent_index.py`,
placed after `session_sent_index_from_evidence` and BEFORE
`_segment_hashes_from_manifest` and `_evidence_hashes`, so the module keeps its
public-then-private layout (verified by parsing the module with `ast`, not by
reading it: `top_level_order` is `SessionSentIndexError`, `SessionSentIndex`,
`session_sent_index_from_evidence`, the three new names, then the two private
helpers; `public_then_private=True`).

- `session_id_of_finalized_call(output) -> str` — reads `usage_actuals` with
  `getattr`, returns `""` for a missing, None or non-mapping value, otherwise
  `str(actuals.get("session_id") or "")`, reproducing `pingpong_loop.py`'s own
  reading exactly.
- `record_finalized_call(index, output, manifest_rows) -> int` — passes
  `ok=not getattr(output, "error", "")` and the resolved session id straight
  into `record_call`. Neither guard is re-implemented; a sessionless call
  records nothing by the rule already inside `record_call`.
- `invalidate_on_resume_fallback(index, output, resumed_ref="") -> bool` —
  no-op returning False unless `resume_fallback`; resolves the ref as
  `resumed_ref` first, else `getattr(output, "resume_session_ref", "")`, strips
  it, and returns False on an empty result rather than guessing.

Purity held, verified by parsing rather than by claim: the module's entire
import set is `__future__` and `collections.abc`. It imports nothing from
`packages.orchestration` and nothing from `pingpong_provider`, so the adapters
are duck-typed exactly as constraint 6 requires. No file, network, subprocess
or `Path` token appears anywhere in the module. Max line length 95 in the
module and 85 in the test file, both under the ruff limit of 120; imports stay
grouped `__future__`, stdlib, first-party. No round of F109 gated on `ruff`,
per constraint 7.

The SPEC's two factual claims about the code it reads were CHECKED against the
base commit rather than taken on trust, and both hold: `BuilderOutput`
(`pingpong_provider.py` lines 66–80) and `ReviewerOutput` (lines 107–135) both
carry `error`, `usage_actuals`, `resume_used`, `resume_session_ref` and
`resume_fallback`; and `pingpong_loop.py` line 3233ff does REPLACE the output
object on the fallback path — it re-calls the provider with `resume=None` and
only then sets `builder_out.resume_fallback = True` at line 3251, with the
failed session's id surviving only in `builder_resume_ref` (line 3096ff). The
reviewer's stated reason for the third argument is therefore correct as
written, and MUTATION B proves the test suite would catch its removal.

## Deviations

1. **The C4 docstring reword is an EDIT inside an "ADD to existing files"
   commit, and it was ordered.** Constraint 4 says nothing already in either
   file is edited, reordered or deleted, while SPEC A's final paragraph
   explicitly requires rewording the "deliberate absences" bullet and extending
   the `Public API` list. The Bundle's own C4 line orders both. I applied the
   block as written — the bullet reworded to say the DECISION logic lands here
   and only the CALL SITES in `pingpong_loop.py` remain, plus the three names
   appended to the Public API list — and changed nothing else in the docstring.
   The diff shows 90 insertions against 2 deletions, and those 2 deletions are
   exactly the old two-line bullet. Declared so a reviewer reading constraint 4
   literally does not read the deletions as scope drift.
2. **C5 extends the existing import statement rather than adding a second
   one.** Same constraint-4 tension: the three new names were added to the
   existing `from packages.orchestration.session_sent_index import (...)` block.
   Nothing already imported was removed or reordered; the alternative — a second
   `from` statement against the same module — would have been a genuine style
   defect. The C5 diff is 202 insertions and ZERO deletions.
3. **One test beyond the mandated eleven.**
   `test_the_output_ref_is_used_when_the_caller_holds_no_variable` covers the
   output-object fallback branch that SPEC A explicitly specifies ("the
   output-object fallback is kept for callers that have no such variable") but
   that no mandated case exercises — without it that branch ships untested.
   Constraint 5's "nothing beyond it may be added" binds the PRODUCTION code,
   which contains exactly the three specified functions and nothing more.
   Declared rather than assumed harmless.
4. **The sandbox bash guard again refused a literal dollar sign inside a quoted
   grep pattern**, exactly as round 1 declared as its deviation 3. Every
   anchored grep in G2 and G3(d) was therefore routed through a no-shell
   `subprocess` argv runner so grep received each pattern byte-for-byte; the
   runner prints the pattern it actually used with `repr` alongside each count,
   so the reviewer can see the pattern rather than trust it. No count was
   weakened or reworded to fit the guard.
5. **Four `.remedy-wt/job-*` worktrees predate this branch** and were left
   alone, as the block instructs. Only this round's own G5 worktree was created
   and removed.

## Open findings

The ledger stands at **330** findings registered and **62** resolved, both
UNCHANGED by this round, so the open set is **268**. This round registered no
finding and resolved none; the two reviewer prose slips went to
`.agent/prose_slips.md` and spend no id, per AGENTS.md `### prose_slips.md` and
operator amendment amend0827-process-diet rule 2. `.agent/candidates.md` is
EMPTY, so no block condition stands against F109.

## Next expected action

`git push` on `feature/f109-semantic-dedupe` immediately after this commit —
not quoted here by design, so the reviewer measures the remote tip itself.
Then round 3, T001b-ii: wire these adapters into
`packages/orchestration/pingpong_loop.py` at the builder and reviewer
finalized-call seams and at BOTH resume-fallback sites, passing
`builder_resume_ref` / `reviewer_resume_ref` as the third argument — which is
the whole reason that argument exists — and persist the index into the job's
evidence.
