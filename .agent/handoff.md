# Handback — F041, round 3: book round 2 and R-1105's resolution, record D3, land T002's core

## Session

SESSION 1 of feature F041 · round 3 · rounds so far 3. This session read the round 3 block whole,
verified its bytes and every payload, booked round 2's gate entry and R-1105's resolution and
recorded DECISION F041 D3 (C1a, C1b, C2), wrote S1 to S3 and applied the wiring diff (C3), applied
the reviewer's tests unedited (C4), wrote and red-proved the round's mutation tool in a real
worktree (C5), fixed a placeholder the round's own serial gate caught in production code (C3-fix),
and ran every gate for real before writing this handback (C6). Context self-assessment: a
comfortable amount of context remains; the round completed inside one session with no blocked
handback, one declared deviation (the C3-fix commit).

For the operator, in plain words: F041's round 3 is now COMPLETE. A job's preview now has a real
record and state machine (`preview.json`), backed by the harness's own `remedy runtime serve`,
`probe` and `stop` verbs run as a child process — never re-implemented — and `remedy job
preview-start` / `preview-stop` record a request and act on it in one call, answering the link only
after a probe passes. Round 2's gate entry and R-1105's resolution are booked, and DECISION F041 D3
is recorded.

## Range

Review of `8130599a1`..`3ba1568ab` (before this handback commit).

## Commits

### 79c02a85b F041 R3 C1a: copy round 3 block, plan, records and wiring into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r3-block.md | 259/0 | copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f041-r3-plan.md | 28/0 | copy of the reviewer's plan.md payload |
| .agent/authored/f041-r3-records.diff | 30/0 | copy of the reviewer's records.diff payload |
| .agent/authored/f041-r3-wiring.diff | 93/0 | copy of the reviewer's wiring.diff payload |

Insertions measured 410 (259+28+30+93); block expected "this block's line count plus 151" = 259+151
= 410. MATCH.

### 872564a15 F041 R3 C1b: copy round 3 tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r3-tests.diff | 423/0 | copy of the reviewer's tests.diff payload |

Insertions measured 423; block expected 423. MATCH.

### 9e10e93cf F041 R3 C2: book round 2 and R-1105's resolution, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 10/0 | `git apply` of records.diff: DECISION F041 D3 |
| .agent/live_review.md | 4/0 | `git apply` of records.diff: round 2 gate entry + R-1105 `Done:` |
| .agent/plan.md | 7/8 | rewrite := plan.md payload, by `shutil.copyfile` |

Numstat measured 10/0, 4/0, 7/8; block expected the same. MATCH.

### 6f900d1ff F041 R3 C3: record preview requests and run them through the harness's own verbs
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/preview_control.py | 306/0 | NEW — S1: the preview record and its state machine |
| packages/orchestration/preview_runner.py | 76/0 | NEW — S2: the runner of the harness's own verbs |
| apps/cli/commands/job_preview_cmd.py | 75/0 | NEW — S3: `job preview-start` / `preview-stop` |
| apps/cli/command_catalog.py | 28/0 | `git apply` wiring.diff: catalog entries |
| apps/cli/commands/__init__.py | 2/1 | `git apply` wiring.diff: register `job_preview_cmd` |
| docs/guides/exit-codes.md | 2/0 | `git apply` wiring.diff: exit-code rows |
| tests/orchestration/import_reachability_allowlist.txt | 3/0 | `git apply` wiring.diff: allowlist lines |

Total insertions 492, under the 500-line cap — no split needed (block's C3a/C3b clause not
triggered). Wiring numstat measured 28/0, 2/1, 2/0, 3/0; block expected the same. MATCH. No
expected insertion count is given for the three new modules themselves.

### 678ca1cfe F041 R3 C4: add the reviewer's preview state machine, runner and command tests
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_preview.py | 111/0 | NEW — `git apply` tests.diff |
| tests/orchestration/test_preview_control.py | 208/0 | NEW — `git apply` tests.diff |
| tests/orchestration/test_preview_runner.py | 86/0 | NEW — `git apply` tests.diff |

Numstat measured 111/0, 208/0, 86/0; block expected the same. MATCH. All three files passed
unedited against the round's code at this commit (see Verification).

### d01502bea F041 R3 C5: add the round 3 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r3-mutations.py | 156/0 | NEW — G4's tool: p1 to p8, control-first/control-last, byte-identical restore |

No expected insertion count given for C5.

### 3ba1568ab F041 R3 C3-fix: name the runtime verbs by name in preview_runner's docstring
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/preview_runner.py | 2/1 | `run_runtime_verb`'s docstring said `` `remedy runtime <verb>` ``; `tests/cli/test_advertised_commands.py`'s group-only sweep refuses a `remedy <group>` line that reaches no command — exactly S2's own warning. Caught by G3's serial run, not by C4's tests (which do not read docstrings). Fixed to name all three verbs by name, as S2 requires; no other line in any of the three new modules matched the same scanner. |

See Deviations & assumptions.

## External actions

- `git worktree add --detach .remedy-wt/f041-r3-worker-scratch 678ca1cfe` (a preliminary,
  self-owned sanity check of the mutation tool BEFORE fixing the p3 bug below) — added; then
  `git worktree remove --force .remedy-wt/f041-r3-worker-scratch` and `git worktree prune` —
  removed. Worktree count returned to 66 (the step-4 baseline) before G4 proper began.
- `git worktree add --detach .remedy-wt/f041-r3-mut 3ba1568ab` (G4) — added; then
  `git worktree remove --force .remedy-wt/f041-r3-mut` and `git worktree prune` — removed.
  Worktree count 66 both before and after.
- `git push -u origin feature/f041-artifact-preview` — see Verification for the real outcome
  (run after this handback commit; reported in the reply, since C6 cannot contain it per the
  block).
- No PR create, no PR merge, no branch deletion, no force-push, no `git stash`, no reset of any
  commit.

## Verification

Payload transport (PAYLOADS table), each measured line count / byte count / sha256 against the
block's table, all MATCH:

    records.diff  30 lines  11142 bytes  e487b0f2ea688d789214bbf589411b5f4971eaa7831da8bed556d10663cbfadf
    wiring.diff    93 lines   4941 bytes  bcd1ee4f13db5fe44b6348de4454960d13fd4ae7643a0e82a424d6d4de34fd31
    tests.diff    423 lines  18221 bytes  0b2a8787906ee346c62950be97e500fad77c26c92be5a33a609bd1b6d89a05be
    plan.md        28 lines    901 bytes  e1c18716b36a70ca6eac6734da1208d1e3188e491426eed8645ffcb29254aadd

`git apply --check` then real `git apply`, each exit 0: records.diff, wiring.diff, tests.diff.

G1 TRANSPORT — every `.agent/authored/f041-r3-*` copy, read with `git show <commit>:<path>` from
the commit that added it, equals its source byte for byte (sha256 compared): block.md, plan.md,
records.diff, wiring.diff at `79c02a85b`; tests.diff at `872564a15`. All MATCH.

G2 THE RECORDS, THE WIRING AND THE TESTS — every path in the block's G2 table, read with
`git show <commit>:<path>` at the commit named, equals the reviewer's stated bytes and sha256.
All ten rows MATCH (`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` at C2;
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `docs/guides/exit-codes.md`,
`tests/orchestration/import_reachability_allowlist.txt` at C3; the three test files at C4).
`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`: at `8130599a1`
→ `['R-1105']`; at `9e10e93cf` (C2) → `[]`. Both equal the reviewer's stated readings.

G3 THE CODE AND THE TESTS —

    python3 -m ruff check packages/orchestration/preview_control.py \
      packages/orchestration/preview_runner.py apps/cli/commands/job_preview_cmd.py \
      apps/cli/commands/__init__.py apps/cli/command_catalog.py \
      tests/orchestration/test_preview_control.py tests/orchestration/test_preview_runner.py \
      tests/cli/test_job_preview.py .agent/authored/f041-r3-mutations.py
    → All checks passed! REAL_EXIT=0

(First run, before the C3-fix, found one finding — `UP035` on `preview_control.py`'s
`from typing import Any, Callable` — fixed in place before C3 was committed, so C3's own diff
already carries the fix; this is separate from the C3-fix commit above, which ruff did not catch
because it is a docstring-text rule, not a lint rule.)

Serial pytest, run in the primary checkout at the current tip (after the C3-fix, so the reading
covers the code that actually ships):

    bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_preview_control.py tests/orchestration/test_preview_runner.py tests/cli tests/docs tests/test_subprocess_timeouts.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/ui_server/test_command_channel.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'

    SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) — same skip the reviewer named.
    2754 passed, 1 skipped in 583.83s (0:09:43)
    REAL_EXIT=0

Matches the reviewer's stated reading (`2754 passed, 1 skipped`) exactly.

FIRST run of this same command (before the C3-fix) read `1 failed, 2753 passed, 1 skipped` at
`REAL_EXIT=1` — the one failure being
`tests/cli/test_advertised_commands.py::test_every_group_only_advertisement_reaches_a_command`,
flagging `packages/orchestration/preview_runner.py:39` (`remedy runtime <verb>` in the docstring).
Fixed by the C3-fix commit; the rerun above is the one that counts.

Node counts by `--collect-only -q`:

    tests/orchestration/test_preview_control.py → 16 tests collected
    tests/orchestration/test_preview_runner.py  → 9 tests collected
    tests/cli/test_job_preview.py               → 7 tests collected

Matches the reviewer's stated reading (16, 9, 7) exactly.

    python3 -m apps.cli.main integrity check --json
    → {"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}
    all six checks "pass". REAL_EXIT=0

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f041-r3-mut 3ba1568ab` (the current tip,
carrying the C3-fix — see Deviations), then
`python3 -B .agent/authored/f041-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r3-mut`:

    CONTROL (first): all three named test files, exit_code=0 failed_count=0 ok=True
    p1: exit_code=1 failed_count=4   restored byte-identical: True
    p2: exit_code=1 failed_count=1   restored byte-identical: True
    p3: exit_code=1 failed_count=1   restored byte-identical: True
    p4: exit_code=1 failed_count=1   restored byte-identical: True
    p5: exit_code=1 failed_count=1   restored byte-identical: True
    p6: exit_code=1 failed_count=1   restored byte-identical: True
    p7: exit_code=1 failed_count=2   restored byte-identical: True
    p8: exit_code=1 failed_count=2   restored byte-identical: True
    CONTROL (last): all three named test files, exit_code=0 failed_count=0 ok=True
    ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
    REAL_EXIT=0

Every mutation caught (non-zero exit), every restore byte-identical, both controls clean.
`git worktree remove --force .remedy-wt/f041-r3-mut`, `git worktree prune`;
`git worktree list | wc -l` → 66 (equals the step-4 baseline).

(A preliminary, self-owned sanity run of the same tool against a scratch worktree at `678ca1cfe`
caught a bug in the tool itself — mutation p3's replacement text carried a trailing `#` comment
that fell mid-line before `else STATE_FAILED)`, turning a real assertion failure into a
`SyntaxError`/collection error, exit_code=2, failed_count=0. Fixed in the tool before C5 was
committed, so C5's own diff already carries the fix; the scratch worktree was removed immediately
after, worktree count confirmed back to 66.)

## Authored-text proofs

Every `.agent/authored/f041-r3-*` copy, read back with `git show <commit>:<path>` from the commit
that added it, is byte-identical to its `.remedy-wt/f041-r3*` source (sha256 compared): block.md,
plan.md, records.diff, wiring.diff at `79c02a85b`; tests.diff at `872564a15`. All MATCH — see G1
above for the full table.

## Deviations & assumptions

1. **C3-fix commit (undeclared until now).** `preview_runner.run_runtime_verb`'s docstring named
   the harness verb as `` `remedy runtime <verb>` ``, a placeholder — exactly the shape S2 warns
   against, because `tests/cli/test_advertised_commands.py` refuses a `remedy <group>` line that
   reaches no command. This was NOT caught by C4's tests (they exercise behaviour, not docstring
   text) and only surfaced when G3's serial run reached `tests/cli/test_advertised_commands.py`.
   By that point C3, C4 and C5 were already committed on top of the buggy line, and this repo's
   rules forbid an interactive rebase (no `-i` flag) and forbid amending anything but the current
   tip without one, so the fix could not be folded back into C3 without rewriting history. I added
   ONE new commit, `3ba1568ab`, fixing the docstring only (2 insertions, 1 deletion), between C5
   and C6. This is a departure from the block's named 7-commit bundle (C1a, C1b, C2, C3, C4, C5,
   C6) — an 8th commit exists. G5's `git log --oneline -n 8` below shows 9 entries for this reason
   (C6, C3-fix, C5, C4, C3, C2, C1b, C1a, `8130599a1`); the block's own G5 clause anticipates "one
   more if C3 was split", not this case, so I am naming the extra line explicitly here rather than
   letting it look like an unexplained deviation from the stated count.
2. **G4's worktree pinned to the tip, not to a bare "C5".** Because of deviation 1, the commit
   named "C5" in the block's G4 instruction (`git worktree add --detach .remedy-wt/f041-r3-mut
   <C5>`) would have been `d01502bea` — still carrying the docstring bug. Running the red proofs
   there would have validated code that no longer matches what ships. I ran G4 against the current
   tip, `3ba1568ab`, instead, so the red proofs cover the actual final state of the three modules.
   The mutation targets (FROM/TO text) are all outside the one line the C3-fix touched, so this
   substitution changes nothing about which behaviour each mutation exercises.
3. **A ruff finding fixed before C3 was committed, not after.** The first draft of
   `preview_control.py` imported `Callable` from `typing`; `ruff` (`UP035`) asked for
   `collections.abc.Callable`. Fixed before `git add`/commit, so C3's own diff (`6f900d1ff`) already
   carries the corrected import — no separate commit was needed for this one, unlike deviation 1.
4. **A bug in my own mutation tool, fixed before C5 was committed.** Mutation p3's original
   replacement text ended in a `#` comment that landed mid-line (before ` else STATE_FAILED)`),
   which is a `SyntaxError` in the mutated worktree copy rather than a real assertion failure —
   still "caught" by a non-zero exit code, but for the wrong reason, and every mutation is meant to
   be "a real behaviour change" a test's own assertions see. Found via a preliminary, self-owned
   sanity run against a scratch worktree at `678ca1cfe` (added and removed under my own
   `.remedy-wt/f041-r3-worker*` naming, never touching the reviewer's directories); fixed before
   `.agent/authored/f041-r3-mutations.py` was written to disk and committed, so C5's own diff
   already carries the fix.
5. **`run_pending`'s `data_root` type.** S1 does not spell every intermediate helper signature;
   `run_pending`'s `job` parameter is read only for `job.job_id` and `job.repo_path` (duck-typed),
   matching both the `SimpleNamespace` fixture in `test_preview_control.py` and the real `JobPlan`
   the command module hands it — no assumption beyond what the two call sites already require.
6. **A single shared `datetime.now(timezone.utc)` in `job_preview_cmd._cmd_job_preview`.** S3 reads
   "calls `request_preview` and `run_pending` ... and `datetime.now(timezone.utc)`" as one instant
   handed to both, not two separate reads; no test distinguishes the two readings, but the single
   read is the more literal one and avoids a hairline race between the two timestamps.

## Next

Next action: the review of round 3. `## Next Steps` in `.agent/plan.md` already reads (per the
block's own rewrite): (1) the door's preview commands, the server-side step acting on their
requests, revalidation of a live preview and the idle stop; (2) T003 — the panel, the lightbox and
the end-to-end run; (3) the closure sequence. Open findings: 0. Operator questions: 1 (unchanged
by this round; see `.agent/operator_questions.md`, not touched this round).
