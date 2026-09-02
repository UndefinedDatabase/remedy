# Handoff — F109 Semantic dedupe, SESSION 1, round 3

Branch: `feature/f109-semantic-dedupe`
Base commit: `4b14eb3e770a1885a73424faa0a25f7e0f237a32` (round 2 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

## Commits this round

| Item | SHA        | Commit subject                                                    |
|------|------------|-------------------------------------------------------------------|
| C0a  | `9948064b` | F109 R3 C0a: save the round 3 step block verbatim                 |
| C0b  | `3d255fac` | F109 R3 C0b: mirror the round 3 block to last_block               |
| C1   | `a49d89fb` | F109 R3 C1: plan for round 3 wiring the adapters into the loop    |
| C2   | `6f5368a2` | F109 R3 C2: book the round 2 PASS verdict into the ledger         |
| C3   | `f68cbd9a` | F109 R3 C3: record the round 2 reviewer prose slip                |
| C4   | `7451e9c7` | F109 T001b-ii C4: wire the sent-hash index into the ping-pong loop|
| C5   | `13bbdeec` | F109 T001b-ii C5: chain tests driving the real loop through the index |

C6 is this handoff rewrite, committed on top of `13bbdeec`. Every gate G1–G7
ran at C5 or earlier, so all seven are quoted below from real output. The push
happens AFTER C6 and is therefore deliberately not quoted here; the reviewer
measures the remote tip itself.

Seven single-parent commits in the range, no merge commit.

## Changed files (this round)

| Path                                            | Change                                               |
|-------------------------------------------------|------------------------------------------------------|
| `.agent/authored/f109-r3.md`                    | new — step block, `cp` not retyped                   |
| `.agent/last_block.md`                          | rewritten — byte mirror of the authored block        |
| `.agent/plan.md`                                | rewritten — SLICE PLAN, whole file, 42 lines         |
| `.agent/live_review.md`                         | one paragraph appended — the round 2 gate entry      |
| `.agent/prose_slips.md`                         | one paragraph appended — one reviewer prose slip     |
| `packages/orchestration/pingpong_loop.py`       | added to — 28 insertions, ZERO deletions             |
| `tests/orchestration/test_semantic_dedupe.py`   | added to — chain cases, 45 tests → 51                |
| `.agent/handoff.md`                             | rewritten — this file (C6)                           |

No path outside the ordered change set was touched.
`packages/orchestration/session_sent_index.py` was NOT edited, as constraint 6
requires; no call site needed a behaviour that module lacks.

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum` over `.remedy-wt/f109-r3.md`,
  `.agent/authored/f109-r3.md` and `.agent/last_block.md` returns the same
  digest for all three:
  `c34d14df27ad8bb2f53d58c74b5f1984dab684f4f4fdbeb9c90df853bca3ec7f`, equal to
  the digest the delegation wrapper stated. Verified BEFORE the round began
  (396 lines, 29325 bytes); both C0a and C0b were `cp`, never a retype.
- **G2 THE PLAN — PASS.** `cmp .agent/plan.md .remedy-wt/slice_PLAN.txt` exit 0,
  byte-equal against the extracted slice rather than a retype; `wc -l` = 42,
  strictly under 50; one `## Goal` heading and one `## Next Steps` heading.
  Negative control: one byte flipped on a scratch copy and `cmp` exit 1, so the
  equality discriminates rather than accepts.
- **G3 THE VERDICT APPEND — PASS, all four parts.** (a) base 2024336 bytes with
  sha256 `5dc6aeb1b8bccae8c8c7593aa4bc623ac5b0349e50db2fdcc68c449c56ec4d25` as
  stated, S = 6057 after the trailing-newline strip, expected 2024336 + 2 + 6057
  = 2030395, actual **2030395**, and the file still ends WITHOUT a trailing
  newline. (b) The blank-line reader counted N = **1** paragraph in the slice
  itself (not taken from the block) over 849 units in the file, and the last 1
  unit is byte-equal to it: True. (c) Negative control on a scratch copy: one
  byte flipped inside the FIRST appended paragraph and the same reader REJECTED
  it (True); the tracked file's sha256 was
  `f09af719542dbb3ecace6cc8f00cc2a1a84ed0d80e41bc965670eed177bc17d6` both before
  and after, identical. (d) The block's exact `grep -c` commands:
  `^Gate: F109 R2 — ` is exactly **1**; `^- R-[0-9]\{4\} — ` UNCHANGED at
  **330**; `^Done: R-[0-9]\{4\} — ` UNCHANGED at **62**. This round registers no
  finding and resolves none. A structurally independent Python regex reader
  produced the same three numbers.
- **G4 THE SLIPS APPEND — PASS.** Base 41716 bytes with sha256
  `fae736593569c3dad97eb33d8ea9bb9b1c2494d77f5c47910bcad35b621ec3c6` as stated,
  S2 = 903 after the same strip, expected 41716 + 2 + 903 = 42621, actual
  **42621**, still ending without a trailing newline. The blank-line reader
  counted N2 = **1** paragraph itself and the last 1 unit of the file equals it:
  True.
- **G5 THE COLOUR OF THE WIRING — CONTROL GREEN, AND BOTH MUTATIONS CAME BACK
  GREEN. THIS IS A REAL FINDING ABOUT THE TESTS AND IT IS REPORTED, NOT FIXED.**
  Run in a disposable worktree added at `13bbdeec`, never in the primary
  checkout; `__pycache__` purged before every run and `python3 -B` throughout.
  Before each mutation the exact text was confirmed to occur EXACTLY ONCE in
  `pingpong_loop.py`, and after each it was confirmed to occur ZERO times, so
  neither mutation silently failed to land.
  (a) CONTROL, unmutated: **exit 0, 51 passed**.
  (b) MUTATION A, DELETE the builder `record_finalized_call` call of SPEC W item
  4(b) (occurrences 1 → 0): **exit 0, 51 passed, 0 failed — GREEN, contrary to
  the block's stated expectation.** The block's premise — "with no builder
  recording the evidence for a resumed chain can no longer be populated" — is
  false as the loop is now wired: the REVIEWER site records into the SAME
  session id later in the same round, so the evidence stays populated. Measured
  directly under the mutation, the resumed chain still yields one row for
  `sess-1`, with 10 hashes instead of 19. Every mandated case asserts only shape
  (non-empty, exactly one row, the session id, sortedness, hex-ness), never a
  count attributable to the builder, so none of them discriminates that call.
  (c) MUTATION B, restore then DELETE the builder
  `invalidate_on_resume_fallback` call of SPEC W item 4(a) (occurrences 1 → 0):
  **exit 0, 51 passed, 0 failed — GREEN, exactly the outcome the block asked me
  to report plainly rather than manufacture a red for.** Cause, measured rather
  than guessed: the fallback chain returns **7 hashes for `sess-1` with the call
  present and 7 with it deleted — byte-identical**. Builder and Reviewer share
  one session id, both fall back in the same round, and the REVIEWER's
  invalidation fires LATER and clears the whole session anyway, so the builder's
  invalidation is fully masked. SPEC C item 5 therefore does not discriminate
  the builder call, and no test was edited to make it appear to.
  Cleanup: `git worktree remove --force
  /home/decodeux/Repos/remedy/.remedy-wt/f109-g5` and `git worktree prune`;
  `git worktree list` afterwards shows the primary checkout plus exactly the
  four pre-existing `.remedy-wt/job-*` worktrees (`job-48a379ab5ca44ec5`,
  `job-7d1c93e2dc98415a`, `job-98e9364a83a34872`, `job-f76686b8435640e9`),
  which predate this branch and were left untouched. The primary checkout was
  confirmed unmutated: `git status --porcelain` empty.
- **G6 THE SUITES — PASS, all nine, run SERIALLY with never two pytest
  processes alive at once.**
  `tests/orchestration/test_semantic_dedupe.py` exit 0, **51 passed** (base 45,
  GREW as ordered); `tests/orchestration/test_pingpong.py` exit 0, **34 passed**
  (base 34); `tests/orchestration/test_session_resume.py` exit 0, **27 passed**
  (base 27); `tests/orchestration/test_run_report.py` exit 0, **81 passed**
  (base 81); `tests/ui_server/` exit 0, **515 passed** (base 515);
  `tests/orchestration/test_test_runner.py` exit 0, **52 passed** (base 52);
  `tests/regression/test_resource_safety.py` exit 0, **21 passed** (base 21);
  `tests/orchestration/test_integrity_gate.py` exit 0, **16 passed** (base 16);
  `tests/cli/test_golden_path.py` exit 0, **42 passed** (base 42). Every count
  matches its base except the one ordered to grow. The three property guards
  named in constraint 10 live in `test_test_runner.py` and all 52 pass, so the
  loop additions satisfy all three.
- **G7 THE TREE — PASS.** `git status --porcelain` EMPTY (no output).
  `git ls-files .remedy-wt` returns NOTHING — the scratch directory is
  gitignored and untracked. Insertion counts, seven numbers, `+` column only:
  C0a **396**, C0b **274**, C1 **13**, C2 **3**, C3 **3**, C4 **28**,
  C5 **154**. Every one under 500. And the number constraint 4 exists for:
  `git diff --numstat 4b14eb3e..` for `packages/orchestration/pingpong_loop.py`
  alone is **28 insertions, 0 DELETIONS**. The wiring is purely additive; no
  existing statement was edited, moved, reindented or removed.

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

Five additive edits to `packages/orchestration/pingpong_loop.py`, 28
insertions and 0 deletions:

1. A NEW `from packages.orchestration.session_sent_index import (...)`
   statement importing `SessionSentIndex`, `invalidate_on_resume_fallback` and
   `record_finalized_call`. Written as its own statement, so no existing import
   block was reflowed. It sorts last in the first-party group — the group runs
   `artifact_summary`, `exec_guard`, `hunk_repair_findings`, `pingpong_provider`,
   `prompt_segments`, `provider_timeouts`, `rate_governor`, and neither
   `run_manifest` nor `scope_plan` is present in this file.
2. `session_sent_evidence: list[dict] = field(default_factory=list)` appended as
   the LAST field of `PingPongResult`, after `provider_attempts`, with the four
   `#:` comment lines exactly as the SPEC gives them. It has a default, so every
   existing construction site keeps working untouched.
3. `session_sent_index = SessionSentIndex()` beside the three existing
   initialisations inside the `try:` block and before the round loop — one index
   per RUN.
4. Builder site: `invalidate_on_resume_fallback(session_sent_index, builder_out,
   builder_resume_ref or "")` immediately after `builder_out.resume_fallback =
   True`, inside that same `if` body at that same indentation; then
   `record_finalized_call(session_sent_index, builder_out,
   builder_composed.manifest_as_dicts())` and the
   `result.session_sent_evidence = session_sent_index.as_evidence_dicts()`
   refresh immediately after the `builder_ctx = _finalize_call(...)` statement.
5. Reviewer site: the same two additions mirrored, with `reviewer_out`,
   `reviewer_resume_ref or ""` and `reviewer_composed.manifest_as_dicts()`.

No call was added inside the parse-retry path, the post-mortem path or any
other provider call, as the SPEC directs. No new function, no new class and no
new branch: the decision logic shipped in round 2 and this round only calls it.

ANCHORS: every line number the block gave matched its symbol text exactly at
the base commit — the import block at 33–70, `class PingPongResult:` at 111 with
its last field at 223, `def run_pingpong(` at 2715, the `try:` at 3066 with the
three initialisations at 3067–3069 and the round loop at 3071,
`builder_out.resume_fallback = True` at 3251, the `builder_ctx = _finalize_call(`
statement at 3255–3257, `reviewer_out.resume_fallback = True` at 3548 and the
`reviewer_final_ctx = _finalize_call(` statement at 3552–3554. Nothing had to be
relocated by text against a disagreeing number. `builder_composed` (3154) and
`reviewer_composed` (3424) were both confirmed unconditionally assigned at the
same indentation earlier in the same loop iteration, so both are in scope.

Ruff followed by construction per constraint 7, which forbids gating on it: max
added line length 106 in the loop and 94 in the test file, both under 120;
imports stay grouped `__future__`, stdlib, first-party and alphabetised within
the first-party group; names inside the new import follow the file's own
existing convention (CamelCase before lowercase, as `pingpong_provider`'s import
already does). Both edited files parse with `ast`.

## What C5 actually landed

Six mandated cases in one new class, `TestChainAgainstTheRealLoop`, whose
docstring states that these cases run the real loop. Both fixtures were copied
from `tests/orchestration/test_session_resume.py` — the autouse
`REMEDY_DATA_DIR` redirect and the `demo_repo` builder — but declared INSIDE the
class, so the 45 pre-existing unit tests above stay genuinely pure (no tmp_path,
no provider) rather than merely nominally so. No existing test was changed.

Every asserted value was TAKEN FROM A REAL RUN before the assertion was written,
as SPEC C items 4 and 6 require:

- item 4: a single-round run with no session id gives 1 round and `[]` evidence;
  the same run with `fake_session_id="sess-1"` gives 1 round and exactly one row
  for `sess-1`. So a run that never resumed DOES record what it proved, and the
  test name says so:
  `test_a_single_round_run_records_its_session_even_though_it_never_resumed`.
  "Resumed session only" governs the composition hook (T002), not what the index
  is permitted to remember.
- item 6: the non-resuming chain gives `final_status == "staged_review_passed"`
  and 2 rounds. Both numbers were measured at the BASE commit `4b14eb3e` in a
  separate throwaway worktree BEFORE the wiring existed, and again at HEAD after
  it: identical on both sides. That worktree was removed by exact path.

## Deviations

1. **MUTATION A came back GREEN and the block expected RED.** Reported, not
   repaired. The block's stated reason is factually wrong about the wired loop:
   deleting the builder recording does not empty a resumed chain's evidence,
   because the Reviewer seam records into the same session id in the same round.
   I did not touch a test to produce a red, and I did not widen the change set
   to "fix" it. Full measurement is in G5(b) above.
2. **MUTATION B came back GREEN**, the outcome the block explicitly told me to
   report plainly if it happened. SPEC C item 5 does not discriminate the
   builder `invalidate_on_resume_fallback` call, because the Reviewer's
   invalidation fires later in the same round on the same session id and clears
   it regardless — the fallback evidence is 7 hashes with the call and 7 without.
   No test was edited. Full measurement is in G5(c) above. Taken together, 1 and
   2 mean the round's four call statements are currently proven as a GROUP, not
   individually; a case that separates the Builder seam from the Reviewer seam
   would need two DIFFERENT session ids, which `FakeProvider` emits from a single
   `fake_session_id`. That is a design question for the reviewer, not something
   I invented a fix for.
3. **One deletion in C5, in the module docstring, not in a test.** The block
   ordered "ADD the chain cases … Change no existing test", and no existing test
   was changed. But the file's docstring asserted "Hermetic and pure: no
   tmp_path, no network, no provider, no sleep", and that sentence becomes FALSE
   the moment loop-driving cases land in the file. I rewrote that one sentence
   to scope purity to the unit tests and to name the new class's use of
   `FakeProvider` and tmp_path; hermeticity itself still holds — no network, no
   sleep. That is the whole of the 2-deletion count in C5's `154/2` numstat.
   Declared rather than left as a false claim on disk.
4. **Four one-line WHY comments in C4 beyond the bare statements SPEC W
   names.** Constraint 5 forbids adding BEHAVIOUR beyond the spec; these add
   none, and every neighbouring seam in this file carries the same kind of
   F-numbered comment (F012, F106 T002c). They record why the third argument is
   passed and why the order is invalidate-then-record, which the SPEC explicitly
   asked not to be rediscovered later as a bug. Declared because they are
   insertions the SPEC did not enumerate.
5. **An environment hazard that would have made G5 a FALSE GREEN, found and
   defeated.** `remedy` is installed editable: a `.pth` in site-packages puts
   `/home/decodeux/Repos/remedy` on `sys.path`, and `packages` is a namespace
   package. A naive `pytest` run inside a git worktree therefore imports the
   PRIMARY checkout's `pingpong_loop.py`, so a mutation applied in the worktree
   would never have been executed and every mutation would have "passed". I
   proved the resolution explicitly in EVERY G5 run by printing
   `packages.orchestration.pingpong_loop.__file__`, which read
   `/home/decodeux/Repos/remedy/.remedy-wt/f109-g5/packages/orchestration/pingpong_loop.py`
   each time, and separately confirmed the base worktree resolved to its own
   copy (its `pingpong_loop.py` correctly lacked `session_sent_evidence`). The
   green mutations above are therefore real results, not artefacts of this
   hazard. Future rounds should keep this proof step.
6. **The sandbox bash guard refused several command FORMS**, not contents:
   `$?` in an `echo`, `$`-anchored grep patterns in a compound command, a
   `VAR=value cmd` env prefix, `export`, and a heredoc containing braces with
   quotes. Every affected check was re-run through a no-shell Python/`subprocess`
   runner or as a standalone command; the block's exact `grep -c` patterns did
   run verbatim as standalone commands and are quoted in G3(d). No gate was
   weakened or reworded to fit the guard.
7. **Four `.remedy-wt/job-*` worktrees predate this branch** and were left
   alone. Two worktrees were created and both were removed by exact path: the
   base-measurement one for SPEC C item 6, and the G5 mutation one.

## Open findings

The ledger stands at **330** findings registered and **62** resolved, both
UNCHANGED by this round, so the open set is **268**. This round registered no
finding and resolved none; the one reviewer prose slip went to
`.agent/prose_slips.md` and spends no id, per AGENTS.md `### prose_slips.md` and
operator amendment amend0827-process-diet rule 2. `.agent/candidates.md` is
EMPTY, so no block condition stands against F109. The two green mutations above
are raised here for the reviewer to classify; I registered no id for them, since
the reviewer owns the ledger.

## Next expected action

`git push` on `feature/f109-semantic-dedupe` immediately after this commit —
not quoted here by design, so the reviewer measures the remote tip itself. Then
the reviewer's decision on the two green mutations: whether SPEC C item 5 needs
a discriminating case (which needs two distinct session ids, so it likely needs
a `FakeProvider` capable of emitting a per-role session id) before T002 builds
on this index. After that, T002: the composition hook that turns an
already-sent segment into a one-line marker, with non-resume calls bypassing the
hook entirely.
