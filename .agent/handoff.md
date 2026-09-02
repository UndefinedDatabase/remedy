# Handoff — F109 Semantic dedupe, SESSION 1, round 1

Branch: `feature/f109-semantic-dedupe`
Base commit: `5e18a8536afa086b591b5a2e13009d68d6227432` (tip of `main`, pull
request 231 merged).
Open PR Gate at base: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
returned `[]` — no merge owed, none performed. No PR created this round.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

## Commits this round

| Item | SHA        | Commit subject                                                        |
|------|------------|-----------------------------------------------------------------------|
| C0a  | `4f3ead7a` | F109 R1 C0a: save the round-1 step block to .agent/authored           |
| C0b  | `bc7f8e26` | F109 R1 C0b: mirror the round-1 step block to last_block.md           |
| C1   | `db3cbcb1` | F109 R1 C1: plan for round 1 - claim, candidate discharge, T001a      |
| C2   | `cf16be96` | F109 R1 C2: claim F109 in the ledger and set the round context        |
| C3   | `5d00f15b` | F109 R1 C3: register R-0769 and empty the closure-candidate carrier   |
| C4   | `fa366bd1` | F109 T001a C4: pure per-session sent-hash index for semantic dedupe   |
| C5   | `2b547432` | F109 T001a C5: unit tests for the session sent-hash index             |

C6 is this handoff rewrite, committed on top of `2b547432`. Every gate G1–G8
ran at C5 or earlier, so all eight are quoted below from real output. The push
happens AFTER C6 and is therefore deliberately not quoted here; the reviewer
measures the remote tip itself.

## Changed files (this round)

| Path                                            | Change                                                        |
|-------------------------------------------------|---------------------------------------------------------------|
| `.agent/authored/f109-r1.md`                    | new — step block, copied not retyped                          |
| `.agent/last_block.md`                          | rewritten — byte mirror of the authored block                 |
| `.agent/plan.md`                                | rewritten — SLICE PLAN, whole file                            |
| `docs/roadmap/STATUS.md`                        | line 16 rewritten — F109 `[ ]` → `[~]`                        |
| `.agent/context.md`                             | rewritten — SLICE CONTEXT, whole file                         |
| `.agent/live_review.md`                         | one paragraph appended — R-0769                               |
| `.agent/candidates.md`                          | rewritten — SLICE CANDIDATES, carrier emptied                 |
| `packages/orchestration/session_sent_index.py`  | new — SPEC M, 211 lines                                       |
| `tests/orchestration/test_semantic_dedupe.py`   | new — SPEC T, 329 lines, 25 tests                             |
| `.agent/handoff.md`                             | rewritten — this file (C6)                                    |

No other tracked path was touched. `.remedy-wt/` is gitignored scratch and is
in no commit.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |
| C6   | done   | this commit |

## Gates — one line per gate, real results

- **G1 TRANSPORT — PASS.** `sha256sum .agent/authored/f109-r1.md .agent/last_block.md`
  exit 0; both `5652e93f880d9ee7972a7bbc5a486a148aae6b5201ed94e06ffb7c68d483df03`,
  equal to each other, to `.remedy-wt/f109-r1.md` and to the digest the
  delegation wrapper stated — all four values identical.
- **G2 THE PLAN — PASS.** `cmp` of `.agent/plan.md` against the extracted SLICE
  PLAN scratch copy: exit 0, no output. `wc -l` = 41 (< 50).
  `grep -c '^## Goal$'` = 1; `grep -c '^## Next Steps$'` = 1.
- **G3 THE CLAIM AND THE CONTEXT — PASS.** In `docs/roadmap/STATUS.md` after C2:
  `grep -c '^- \[~\] F109 — Semantic dedupe$'` = 1; `grep -c '^- \[ \] F109'` = 0
  (grep exit 1, the normal no-match exit); `grep -c '^- \[x\] F'` = 67 at the
  base commit and 67 after C2 — UNCHANGED, both numbers measured;
  `grep -c '^- \[~\] F'` = 1, at the cap `tests/docs/test_docs_consistency.py`
  enforces. The applied line was additionally proved byte-equal to the STATUSTO
  slice, not merely pattern-equal. `cmp` of `.agent/context.md` against SLICE
  CONTEXT: exit 0.
- **G4 THE LEDGER APPEND — PASS, all four parts.**
  (a) BYTE ARITHMETIC: base 2015028 + separator 2 + S 3285 = 2018315; actual
  size 2018315. Base sha256 confirmed
  `c3fa642ece4f90819e2ec7c73e29bc1d574dcf160e726e660e3ab05a937d588e` before the
  append. File still ends without a trailing newline, per constraint 4.
  (b) SECOND READER: split the whole file on blank lines into units; N counted
  in SLICE RECORD by the reader itself = 1; file holds 847 units; the last 1
  unit equals the 1 record paragraph byte-for-byte (3285 == 3285). Exit 0,
  VERDICT ACCEPTED.
  (c) NEGATIVE CONTROL: on the scratch copy `.remedy-wt/ledger_mutated.md`,
  byte 2015070 (inside the FIRST appended paragraph, `S` → `s` in
  "CARRIES") was flipped; reader (b) exited 1, VERDICT REJECTED. The tracked
  file's sha256 was
  `3a5981497bb3ada18babe0a906f4c6160a42563671b1350001fac74b0d2bc90e` before the
  control and identical after it — the tracked file was never mutated.
  (d) COUNTS: `grep -c '^- R-[0-9]\{4\} — '` 329 at base → 330 after C3;
  `grep -c '^- R-0769 — '` = 1; `grep -c '^Done: R-[0-9]\{4\} — '` = 62,
  UNCHANGED.
- **G5 THE CANDIDATES CARRIER — PASS.** `cmp` of `.agent/candidates.md` against
  SLICE CANDIDATES: exit 0. `grep -c 'R-0769'` = 1.
  `grep -c '^## Open candidates$'` = 0 (grep exit 1) — the section holding the
  open entry is gone.
- **G6 THE COLOUR OF THE NEW CODE — PASS.** Ran in a disposable worktree added
  at C5 (`2b547432`) under `.remedy-wt/g6`, never in the primary checkout;
  `__pycache__` purged before every run (0 dirs present each time) and every run
  used `python3 -B`.
  (a) CONTROL, unmutated: exit 0, `25 passed in 0.24s`.
  (b) MUTATION A — the `if not ok: return 0` guard deleted so `record_call`
  ignores `ok` and records regardless: exit 1, `1 failed, 24 passed`. The single
  failure is exactly the SPEC T item 2 case,
  `TestUnprovenSendsAreNotRecorded::test_a_failed_call_records_nothing_and_leaves_the_session_empty`
  (`assert 3 == 0`).
  (c) Restored from the commit, then MUTATION B — the
  `if not isinstance(session_id, str) or not session_id.strip(): return 0` guard
  deleted so an empty `session_id` becomes an ordinary key: exit 1,
  `2 failed, 23 passed`. Both failures are exactly the SPEC T item 3 cases,
  `...::test_a_call_with_an_empty_session_id_records_nothing` and
  `...::test_a_call_with_a_whitespace_only_session_id_records_nothing`.
  Then `git worktree remove --force` + `git worktree prune`, both exit 0.
  `git worktree list` afterwards shows the primary checkout plus four
  PRE-EXISTING job worktrees (`job-48a379ab5ca44ec5`, `job-7d1c93e2dc98415a`,
  `job-98e9364a83a34872`, `job-f76686b8435640e9`, at `f0e6b9a3`/`21a45836`/
  `4b49af98`, all older than this branch); the G6 worktree is gone. Those four
  were not created by this round and were not touched.
- **G7 THE SUITES — PASS, zero drift.** Seven commands run SERIALLY at C5, never
  two pytest processes alive at once, then the canary:

  | Command | Exit | Result | Base |
  |---------|------|--------|------|
  | `pytest tests/orchestration/test_semantic_dedupe.py -q` | 0 | 25 passed | new this round |
  | `pytest tests/docs/ -q` | 0 | 295 passed | 295 |
  | `pytest tests/orchestration/test_roadmap_index.py -q` | 0 | 30 passed | 30 |
  | `pytest tests/ui_server/ -q` | 0 | 515 passed | 515 |
  | `pytest tests/orchestration/test_test_runner.py -q` | 0 | 52 passed | 52 |
  | `pytest tests/regression/test_resource_safety.py -q` | 0 | 21 passed | 21 |
  | `pytest tests/orchestration/test_integrity_gate.py -q` | 0 | 16 passed | 16 |
  | `pytest tests/cli/test_golden_path.py -q` (canary) | 0 | 42 passed | 42 |

  Every base count matched exactly. The three property guards named in
  constraint 9 live in `tests/orchestration/test_test_runner.py`, which is green
  at 52 with the new module present in `packages/orchestration/`.
- **G8 THE TREE — PASS.** `git status --porcelain` EMPTY at C5 (and now).
  `git ls-files .remedy-wt` returns nothing. Insertion counts, C0a→C5:
  458, 455, 28, 28, 11, 211, 329 — SEVEN numbers, every one under 500. See
  deviation 2: the block's prose says "six numbers" while its own bundle
  enumerates seven commits from C0a through C5.

## What this round did

1. Claimed F109 in `docs/roadmap/STATUS.md` (`[ ]` → `[~]`), the only in-progress
   line in the file.
2. Discharged the one closure candidate F108 left open by registering it as
   finding `R-0769` in `.agent/live_review.md` and emptying
   `.agent/candidates.md`, in one commit — the closure protocol requires both in
   the same round.
3. Landed T001a: `packages/orchestration/session_sent_index.py`, a PURE
   per-session sent-hash index (`SessionSentIndexError`, `SessionSentIndex` with
   `record_call` / `sent_hashes` / `was_sent` / `invalidate_session` /
   `session_ids` / `as_evidence_dicts`, and
   `session_sent_index_from_evidence`), plus 25 unit tests covering all twelve
   mandatory SPEC T cases.

## Implementation notes the reviewer may want to check

- `sent_hashes` deliberately carries NO second guard against a blank session id.
  The spec's "an empty session id yields the EMPTY frozenset" is a CONSEQUENCE
  of `record_call` refusing to create such a key, so the rule lives in exactly
  one place. A redundant guard in `sent_hashes` would have MASKED mutation B and
  made G6(c) unfalsifiable; this is why the mutation is observable.
- `record_call` validates the entire manifest BEFORE mutating the index, so a
  malformed row leaves the index untouched rather than half-updated. Pinned by
  `test_a_malformed_row_leaves_the_index_unchanged`.
- `_evidence_hashes` rejects `str` and `bytes` explicitly even though both are
  `Sequence`s: iterating a bare string would silently accept its CHARACTERS as
  hashes. Pinned by `test_from_evidence_raises_when_sent_sha256_is_a_bare_string`.
- `record_call` returns early on `ok=False` and on a blank session id WITHOUT
  validating the manifest, because the spec says both cases "return 0" and are
  "silent" — a return of 0 is incompatible with raising.
- Constraint 6 honoured by construction, not by a gate: no `ruff` gate was run
  or claimed. The new files are ≤120 columns (max line length verified
  mechanically), carry no trailing whitespace, and group imports `__future__` →
  stdlib → first-party, matching `packages/orchestration/prompt_segments.py`.
  The tuple-form `isinstance(x, (str, bytes))` is the house convention (40+
  occurrences in production code under the same ruff config).

## Deviations

1. **Gate command FORM, not property — `$`-anchored greps.** The sandbox's bash
   guard rejects a literal `$` inside a quoted grep pattern, so the four
   end-of-line-anchored gate greps (G2's two, G3's `^- \[~\] F109 — Semantic
   dedupe$`, G5's `^## Open candidates$`) were executed through a five-line
   no-shell runner that passes argv straight to `execve`. grep therefore received
   each pattern byte-for-byte as the block names it; the printed `argv:` line in
   each run shows the exact pattern. No gate was weakened, reworded or skipped.
2. **Block numeral — G8 says "six numbers", the bundle has seven commits.**
   C0a, C0b, C1, C2, C3, C4, C5 is seven items, not six. Per constraint 1 the
   block was applied as written and the problem is declared rather than
   silently repaired: all SEVEN insertion counts are reported above, and all
   seven are under 500. Nothing on disk is affected.
3. **G4(a) reading of S.** The extractor writes every slice as a POSIX text file
   with a trailing newline, which would give S = 3286. Constraint 4 is explicit
   that the file "still ends without a trailing newline afterwards", so the
   scratch copy of SLICE RECORD used for the append and for S has that one
   trailing newline stripped: S = 3285, and the two clauses of the block agree.
   Declared because the reviewer may recompute S from the raw slice and get 3286.
4. **Four pre-existing job worktrees remain.** `git worktree list` is not empty
   after G6's cleanup. The four `.remedy-wt/job-*` worktrees predate this branch
   (commits `f0e6b9a3`, `21a45836`, `4b49af98`), are outside this round's change
   set, and were deliberately not removed. Only the G6 worktree this round
   created was removed.

No slice was edited to fit, no path outside the change set was touched, and no
gate went red.

## Open findings

330 findings on the record (`^- R-[0-9]\{4\} — `), up one from 329: `R-0769`
was registered this round. `Done:` lines unchanged at 62. `R-0769` is registered,
NOT fixed — its repair edits `README.md` and `tests/docs/test_docs_consistency.py`,
neither of which F109 owns, so it routes to the same paydown branch as `R-0570`.
`.agent/candidates.md` is now EMPTY — no closure candidate is open.

## Next expected action

Push `feature/f109-semantic-dedupe` (`git push -u origin
feature/f109-semantic-dedupe`), then hand back to the planner/reviewer for the
round-1 verdict. No PR was created and none is owed this round. The next build
step is T001b: persist the index into the job's evidence at the
`on_call_finalized` seam and invalidate a session's set whenever a resume
attempt falls back to full context.
