# Handback — F291 round 3: book round 2, record D3, land SU-037 with two reviewer tests, write the Built State's self-use paragraph, and run the closure's integration gate

## Session

SESSION 1 of feature F291 · round 3 · rounds so far 3. Context self-assessment: roughly half the
session's context window remained when this handback was written, after all seven commits, all five
gates and the one full suite run.

## Range

Review of `8cd5855d7`..HEAD (this round's final commit, C6 — the push's real outcome is reported in
the worker's reply, since this file is committed as part of C7 and cannot name its own commit's sha
or anything that follows it).

## Commits

### `85160411b` F291 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r3-block.md | +197/-0 | this round's block, copied verbatim via `shutil.copyfile` |
| .agent/authored/f291-r3-plan.md | +27/-0 | payload copy |
| .agent/authored/f291-r3-records.diff | +45/-0 | payload copy |
| .agent/authored/f291-r3-selfuse.diff | +26/-0 | payload copy |
| .agent/authored/f291-r3-tests.diff | +64/-0 | payload copy |
| .agent/authored/f291-r3-docs.diff | +16/-0 | payload copy |

Total 375 insertions (block's 197 + 178), matching the block's stated formula exactly; measured
`git diff --cached --stat` before commit: `6 files changed, 375 insertions(+)`.

### `c956c375b` F291 R3 C2: book F291 R2, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +27/-0 | DECISION F291 D3 appended (records.diff) |
| .agent/live_review.md | +2/-0 | Gate: F291 R2 entry appended (records.diff) |
| .agent/plan.md | +8/-9 | rewritten via `shutil.copyfile` from plan.md payload |

Measured `git diff --numstat` before commit: 27/0, 2/0, 8/9 — equal to the block's expected numstat
table exactly, in the same order.

### `1f8a7267e` F291 R3 C3: land SU-037, narrow the brain viewer's constitution handler to OSError
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/brain.py | +1/-1 | `except Exception:  # noqa: BLE001 ...` → `except OSError:` (selfuse.diff, the job's own diff) |
| tests/test_ble001_ratchet.py | +1/-1 | `MAX_EXCUSED` 290 → 289 (selfuse.diff) |

Measured `git diff --numstat` before commit: 1/1, 1/1 — equal to the block's expected numstat
exactly. `cmp` of `selfuse.diff` against a freshly regenerated `git diff
8cd5855d7...remedy/job-d6d60ea3d586425a` reported no difference (byte-identical).

### `d57e40bc0` F291 R3 C4: add the reviewer's tests for the narrowed constitution handler
| Path | +/- | Reason |
|---|---|---|
| tests/test_brain_viewer.py | +53/-0 | `git apply` of tests.diff: two new tests in `TestConstitutionGuard` — `test_an_unreadable_repo_warns_and_still_builds`, `test_a_defect_in_the_loader_is_not_swallowed` |

Measured `git diff --numstat` before commit: 53/0 — equal to the block's expected numstat exactly.

### `9de25ec67` F291 R3 C5: record the closure's self-use item in F291's Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F291.md | +8/-0 | "The closure's self-use item" paragraph appended (docs.diff) |

Measured `git diff --numstat` before commit: 8/0 — equal to the block's expected numstat exactly.

### `fd4d02e3c` F291 R3 C6: add the round 3 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r3-mutations.py | +113/-0 | this round's mutation tool (G3): 2 labelled mutations (m1, m2) against `apps/cli/commands/brain.py`'s narrowed handler, an unmutated control run first and last, byte-identical restore after each |

Measured 113 insertions. `ruff check .agent/authored/f291-r3-mutations.py` → `All checks passed!`,
exit 0, before commit.

### C7 (this commit) — F291 R3 C7: record the closure suite transcript and rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-closure-suite.txt | new file | the C7 integration gate's transcript: command, real exit code, wall time, summary line, bad node ids, tree SHA |
| .agent/handoff.md | this file | round 3 handback, written and committed together with the transcript per the block's C7 instruction |

## External actions

- `git worktree add --detach .remedy-wt/f291-r3-mut fd4d02e3c` (G3): succeeded, `HEAD is now at
  fd4d02e3c`.
- `git worktree remove --force .remedy-wt/f291-r3-mut` then `git worktree prune` (G3, last action):
  both exit 0; `git worktree list | wc -l` read 13 afterward, equal to the BEFORE-ANYTHING-ELSE step
  4 reading.
- `git push -u origin feature/f291-self-use-sources-v2` after C7: real outcome reported in the
  worker's final reply, since this file cannot record a push that follows it.
- No PR was created (the block orders "No pull request" for this round). No `gh pr merge`, no
  checkout of `main`, no branch deletion, no force-push, no `git stash`, no evidence job, no zip, no
  self-use run and no job calling a provider. `remedy/job-d6d60ea3d586425a` was not deleted.

## Verification

**BEFORE ANYTHING ELSE:** step 1 `ls .agent/STOP` — absent (`No such file or directory`). step 2
`pwd` `/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current`
`feature/f291-self-use-sources-v2`; `git log --oneline -1` `8cd5855d7` — all matched exactly. step 3
block measured 197 newlines, sha256
`9ff9c47bd12f921da26b24aebefdc434a3396ac849fee05b54cf0917cd8855f5` — equal to the delegation
message's two readings exactly. step 4 `git worktree list | wc -l` 13; `git branch --list
'remedy/*'` 17.

**PAYLOADS:** all five measured exactly against the table — records.diff 45/7822/
`83fb49cc0ccaab0d85bd4ae9f3c2b5c3434950e823a769fcb1ff3609ea2ae8c2`, selfuse.diff 26/1247/
`b10d93928ca92c32c00b210246c6904a0569080532904437b996387ba497a6bf`, tests.diff 64/2931/
`93a08777429844bdb47da5338b840aacfda47ad11113a33e611891ec51060d8f`, docs.diff 16/1241/
`05abe7079f3499c6458d2d8ab38a48d1b70f79e35cfd3fe5f851b30fcd9bbe8e`, plan.md 27/903/
`67a7ca7e49cf1defce5c7bfe91456297550808a232bb97bf402de3d11671c066` — full readings match the
block's table digit for digit.

**G1 transport and records:** all six committed `.agent/authored/f291-r3-*` copies (block, plan,
records diff, selfuse diff, tests diff, docs diff) verified byte-identical to their sources with an
independent hash-comparison script (`git show <commit>:<path>` vs. source bytes) — all six equal,
the block copy against `.remedy-wt/f291-r3/block.md` included. The seven-row G1 table (three files
at C2, two at C3, one at C4, one at C5) was read via `git show <commit>:<path>` with an independent
script that computed each file's byte count and full sha256 and compared both against the block's
table; every one of the seven rows matched on both bytes and the full 64-hex sha256, exactly as the
block stated them (`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` at C2;
`apps/cli/commands/brain.py`, `tests/test_ble001_ratchet.py` at C3; `tests/test_brain_viewer.py` at
C4; `docs/roadmap/features/T5_F291.md` at C5 — no row printed MISMATCH). Also over the ledger text
at C2: `open_finding_ids` (imported from `scripts/rotate_live_review.py`) read `[]`,
`latest_gate_verdict` read `PASS` — both equal to the reviewer's reading. `cmp` of `selfuse.diff`
against a freshly regenerated `git diff 8cd5855d7...remedy/job-d6d60ea3d586425a`, written under the
worker's own directory, reported no difference.

**C2/C3/C4/C5 apply:** `git apply --check` then `git apply`, each exit 0, in order: records.diff,
selfuse.diff, tests.diff, docs.diff. Every `git diff --numstat` reading matched the block's expected
table exactly before each commit (see per-commit tables above).

**G2 the tests, serially, in the primary checkout at C6:**
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_brain_viewer.py tests/test_ble001_ratchet.py tests/test_context_coverage.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
→ `801 passed, 1 skipped in 88.70s (0:01:28)`, `REAL_EXIT=0` — equal to the reviewer's simulated-tree
reading of `801 passed, 1 skipped` at exit 0 exactly. The `-rs` summary printed exactly one SKIPPED
line: `SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md
was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1,
docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog:
re-pin this contract on the split-workflow docs, or retire the test.` — the D12 quarantine, equal to
the reviewer's own reading. Then
```
python3 -m ruff check apps/cli/commands/brain.py tests/test_brain_viewer.py tests/test_ble001_ratchet.py .agent/authored/f291-r3-mutations.py
```
→ `All checks passed!`, exit 0. Then `python3 -m apps.cli.main integrity check --json` → all six
checks `status: "pass"` (`handler_import` handlers=171, `live_review_verdict` last Gate verdict
PASS, `plan_consistency` unchecked=0 context_complete=False, `relevant_untracked` untracked=0
relevant=0, `repo_root_hygiene` no reviewer scratch/evidence dir/archive at root, `high_blockers_open`
no open blocker/high findings), `fail_count: 0`, `ok: true`, `passed: true`, real exit 0.

**G3 the red proofs:** `git worktree add --detach .remedy-wt/f291-r3-mut fd4d02e3c` succeeded.
`python3 -B .agent/authored/f291-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f291-r3-mut`
printed, verbatim:
```
control (before) exit=0 failed=0
m1 (the handler goes back to catching Exception): exit=1 failed=1
restored byte-identical: True
m2 (the handler catches ValueError in place of OSError): exit=1 failed=1
restored byte-identical: True
control (after) exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Both mutations turned `tests/test_brain_viewer.py` red (exit 1, 1 failed each — equal to the
reviewer's own probe reading); both controls passed clean; every restore was byte-identical to the
original, checked by re-reading the mutated file's bytes after restore and comparing to the bytes
read before mutation. The FROM text (`        except OSError:`) was independently verified to occur
exactly once in `apps/cli/commands/brain.py` before the tool was committed. `git worktree remove
--force .remedy-wt/f291-r3-mut` and `git worktree prune` both exit 0; `git worktree list | wc -l`
read 13 afterward — equal to the BEFORE-ANYTHING-ELSE step 4 reading.

**G4 the integration gate:**
(a) `apps/ui/node_modules/.bin/vite build` (cwd `apps/ui`, via a Python script): exit 0; last line
`- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.` (a chunk-size
informational warning, not a failure — the build itself reported `✓ built in 2.26s` and wrote
`dist/index.html`, `dist/assets/*`). `git status --porcelain` after the build: empty.
(b) `python3 -m pytest -n auto -q`: real exit code **1**; wall time measured **193.93 seconds**;
summary line `1 failed, 20972 passed, 20 skipped, 1 warning in 193.14s (0:03:13)`; one bad node id:
`tests/test_parametrize_ids_stable.py::test_no_parametrize_argument_draws_a_fresh_value_at_collection`.
The failure is a `FileNotFoundError` on `tests/regression/test_runtime_chain_571577_0jkfclu8.py`, an
ephemeral file that does not exist in this tree's git history — some other test running concurrently
under `-n auto` wrote it into `tests/regression/` and removed it again, racing the parametrize-scan
test's `ast.parse` read of every tracked test file. This is a pre-existing full-suite node unrelated
to any file this round's payloads touch (`apps/cli/commands/brain.py`,
`tests/test_ble001_ratchet.py`, `tests/test_brain_viewer.py`); it was reported and left exactly as
measured — not edited, weakened, skipped or marked xfail, per constraint 4. The full command, exit
code, wall time, summary line, bad node id and tree SHA are recorded verbatim in
`.agent/authored/f291-closure-suite.txt`, committed with this handback (C7). `git status --porcelain`
after the run showed no leftover untracked files (the ephemeral regression file was already gone).
`pgrep -af server.py` afterward: no matches (exit 1, empty output) — no lingering server processes.
The full suite ran exactly once this round, in C7 (constraint 7).

**G5 sizes** (`git show --numstat --format= <commit>` for C1 to C6, beside the block's stated
expected insertions where one is given):
| Commit | Reading | Expected | Match |
|---|---|---|---|
| C1 `85160411b` | 375 | 375 (197+178) | equal |
| C2 `c956c375b` | 27/0, 2/0, 8/9 | 27/0, 2/0, 8/9 | equal |
| C3 `1f8a7267e` | 1/1, 1/1 | 1/1, 1/1 | equal |
| C4 `d57e40bc0` | 53/0 | 53/0 | equal |
| C5 `9de25ec67` | 8/0 | 8/0 | equal |
| C6 `fd4d02e3c` | 113/0 | (none stated) | — |

`git status --porcelain`, `git log --oneline -n 8`, plus the push's real outcome and the open-PR
check, are reported in the worker's reply, since C7 (this commit) cannot record itself or anything
that follows it.

**Round's whole tracked path set** (constraint 3), measured with `git diff --name-only 8cd5855d7`
after C6 (before C7 is committed): `.agent/authored/f291-r3-block.md`,
`.agent/authored/f291-r3-docs.diff`, `.agent/authored/f291-r3-mutations.py`,
`.agent/authored/f291-r3-plan.md`, `.agent/authored/f291-r3-records.diff`,
`.agent/authored/f291-r3-selfuse.diff`, `.agent/authored/f291-r3-tests.diff`,
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`, `apps/cli/commands/brain.py`,
`docs/roadmap/features/T5_F291.md`, `tests/test_ble001_ratchet.py`, `tests/test_brain_viewer.py` —
every path is a member of the block's stated set (constraint 3's list, `.agent/authored/
f291-closure-suite.txt` and `.agent/handoff.md` itself added by C7). `scripts/self_use_queue.json`
was not touched this round, confirmed in the same listing.

## Authored-text proofs

All six `.agent/authored/f291-r3-*` payload/block copies (block, plan, records diff, selfuse diff,
tests diff, docs diff) are byte-identical, source to committed copy, verified by an independent
hash-comparison script comparing `.remedy-wt/f291-r3/block.md` and each
`.remedy-wt/f291-r3-payloads/*` file against `git show <commit>:<path>` — all six equal (G1, above).
The applied `records.diff` (→ `.agent/decisions.md`, `.agent/live_review.md`, and the rewritten
`.agent/plan.md` via `shutil.copyfile`), `selfuse.diff` (→ `apps/cli/commands/brain.py`,
`tests/test_ble001_ratchet.py`), `tests.diff` (→ `tests/test_brain_viewer.py`) and `docs.diff` (→
`docs/roadmap/features/T5_F291.md`) all reproduced content matching the block's G1 sha256 table
exactly at C2, C3, C4 and C5 respectively — this confirms `git apply` and `shutil.copyfile`
reproduced the reviewer-authored text exactly, not only that the source payload itself was
uncorrupted. `selfuse.diff` was additionally verified byte-identical to a freshly regenerated
`git diff 8cd5855d7...remedy/job-d6d60ea3d586425a` via `cmp`, confirming it is still the job's own
diff, unedited.

## Deviations & assumptions

None from the block's ordered commit sequence — every commit (C1 through C7) landed in order, with
no payload retyped or edited, and no existing test was edited to pass. Every gate the block ordered
(G1 through G5) ran and its real output is reported above and in `.agent/authored/
f291-closure-suite.txt`. The one notable reading: the C7 full suite ended RED at exit 1 with one bad
node id, `tests/test_parametrize_ids_stable.py::test_no_parametrize_argument_draws_a_fresh_value_at_collection`,
caused by a `FileNotFoundError` on an ephemeral regression-test artifact that raced the scanning
test under `-n auto` — a pre-existing full-suite node this round's payloads never touch. Per
constraint 4, a RED full suite in C7 is this feature's work, not a stop: the transcript was committed
exactly as measured, the bad node id is reported here and in the transcript file, and nothing was
weakened, deleted, skipped or marked xfail to make it pass. No file outside the round's tracked path
set (constraint 3) was touched (verified above). No `gh pr create` or `gh pr merge`, no checkout of
`main`, no branch deletion, no force-push, no `git stash`, no evidence job, no zip, no self-use run
and no job calling a provider. `remedy/job-d6d60ea3d586425a` was not deleted.

## Next

Per the block's `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of
round 3 and of the suite transcript, then the first repair round for the one bad node id (the suite
is not green). Open findings: 0. Operator questions: 0.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 copy round 3 block and payloads into .agent/authored/ | done | 375 insertions, matching block's formula exactly |
| C2 book F291 R2, record D3 | done | numstat matched exactly (27/0, 2/0, 8/9); G1 hashes matched |
| C3 land SU-037, narrow the brain viewer's constitution handler to OSError | done | numstat matched exactly (1/1, 1/1); `cmp` against the job's own diff reported no difference |
| C4 add the reviewer's tests | done | 53/0 numstat matched; G1 hash matched |
| C5 record the closure's self-use item in the Built State | done | 8/0 numstat matched; G1 hash matched |
| C6 add the round 3 mutation tool | done | ruff clean; both mutations caught, both controls clean, both restores byte-identical |
| C7 record the closure suite transcript and rewrite handoff | done | this commit |
| G1 transport and records | done | all payload and authored-copy hashes verified equal; seven-row table matched; open_finding_ids `[]`, latest_gate_verdict PASS; selfuse.diff `cmp` clean |
| G2 the tests | done | 801 passed/1 skipped at exit 0, matching the reviewer's reading; ruff clean; integrity check 6/6 pass, fail_count 0 |
| G3 the red proofs | done | both mutations caught (exit 1, 1 failed each); both controls clean; both restores byte-identical; `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`; worktree count restored to 13 |
| G4 the integration gate | done (RED suite booked, not repaired) | UI build exit 0; full suite exit 1, 1 bad node id (pre-existing, unrelated flake), recorded verbatim in the transcript; no lingering server processes |
| G5 sizes, tree and push | done for C1–C6 sizing; push/log/PR-list reported in the worker's reply |

Open findings: 0 (per `open_finding_ids` at C2). Operator questions open: 0.
