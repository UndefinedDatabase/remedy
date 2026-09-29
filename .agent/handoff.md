# Handback — F291 round 4: book round 3, register R-1114, record D4, repair Tier 5 and the parametrize-id guard, and re-run the closure's one full suite

## Session

SESSION 1 of feature F291 · round 4 · rounds so far 4. Context self-assessment: roughly a third of
the session's context window remained when this handback was written, after all six commits, all
five gates and the one full suite run.

## Range

Review of `752164eb2`..HEAD (this round's final commit, C6 — the push's real outcome is reported in
the worker's reply, since this file is committed as part of C6 and cannot name its own commit's sha
or anything that follows it).

## Commits

### `eb18ece2a` F291 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r4-block.md | +211/-0 | this round's block, copied verbatim via `shutil.copyfile` |
| .agent/authored/f291-r4-plan.md | +28/-0 | payload copy |
| .agent/authored/f291-r4-records.diff | +50/-0 | payload copy |
| .agent/authored/f291-r4-tests.diff | +91/-0 | payload copy |

Total 380 insertions (block's 211 + 169), matching the block's stated formula exactly; measured
`git diff --cached --stat` before commit: `4 files changed, 380 insertions(+)`.

### `bd8017023` F291 R4 C2: book F291 R3, register R-1114, record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +30/-0 | DECISION F291 D4 appended (records.diff) |
| .agent/live_review.md | +4/-0 | Gate: F291 R3 entry and R-1114's registration appended (records.diff) |
| .agent/plan.md | +8/-7 | rewritten via `shutil.copyfile` from the plan.md payload |

Measured `git diff --numstat` before commit: 30/0, 4/0, 8/7 — equal to the block's expected numstat
table exactly, in the same order.

### `8eeeb23c4` F291 R4 C3: skip a test file that vanished while Tier 5 reads tests (R-1114)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/self_use_generator.py | +4/-0 | S1: `_bound_test_names` gains an `except FileNotFoundError: continue` clause before the existing `except (OSError, UnicodeDecodeError)` clause, under a 2-line comment naming R-1114 and DECISION F291 D4 |

Measured `git diff --numstat` before commit: 4/0 — equal to the block's stated reviewer's-own-version
reading exactly. No line contains `#` followed by `noqa: BLE001`, verified by an independent regex
scan. Tier 4's reader (`_public_top_level_names`) was not touched, verified by re-reading it after
the edit.

### `2327dea0e` F291 R4 C4: repair the parametrize-id guard's reader and add the vanished-file tests (R-1114)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_self_use_generator.py | +28/-1 | `git apply` of tests.diff: two new tests join `TestUntestedModuleTier` (`test_a_test_file_that_vanished_is_skipped`, `test_any_other_unreadable_test_file_still_raises`), and `TestUntestedModuleTierRealChain`'s second reader gains a `_source` helper that reads a vanished file as empty |
| tests/test_parametrize_ids_stable.py | +25/-1 | `git apply` of tests.diff: `fresh_value_parametrize_sites` skips a `FileNotFoundError` file, and one test (`test_a_test_file_that_vanished_is_skipped`) is added |

Measured `git diff --numstat` before commit: 28/1, 25/1 — equal to the block's expected numstat
table exactly.

### `22265f346` F291 R4 C5: add the round 4 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r4-mutations.py | +177/-0 | this round's mutation tool (G3): 3 labelled mutations (x1, x2, x3) against Tier 5's new clause, Tier 5's other read-error clause, and the parametrize-id guard's new clause; an unmutated control run first and last; a planted dangling-link run after the mutations |

Measured 177 insertions. `ruff check .agent/authored/f291-r4-mutations.py` (with the other three G2
files) → `All checks passed!`, exit 0, before this handback's writing.

### C6 (this commit) — F291 R4 C6: record the repaired tree's suite transcript and rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-closure-suite.txt | rewrite, 13/14 | this round's suite transcript: command, real exit code, wall time, summary line, bad node ids (NONE), the previous bad set and the shrink reading, and the tree SHA |
| .agent/handoff.md | this file | round 4 handback, written and committed together with the transcript per the block's C6 instruction |

## External actions

- `git worktree add --detach .remedy-wt/f291-r4-mut 22265f346` (G3): succeeded, `HEAD is now at
  22265f346`.
- `git worktree remove --force .remedy-wt/f291-r4-mut` then `git worktree prune` (G3, last action):
  both exit 0; `git worktree list | wc -l` read 13 afterward, equal to the BEFORE-ANYTHING-ELSE step
  4 reading.
- `git push -u origin feature/f291-self-use-sources-v2` after C6: real outcome reported in the
  worker's final reply, since this file cannot record a push that follows it.
- No PR was created (the block orders "No pull request" for this round). No `gh pr merge`, no
  checkout of `main`, no branch deletion, no force-push, no `git stash`, no evidence job, no zip, no
  self-use run and no job calling a provider.

## Verification

**BEFORE ANYTHING ELSE:** step 1 `ls .agent/STOP` — absent (`No such file or directory`). step 2
`pwd` `/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current`
`feature/f291-self-use-sources-v2`; `git log --oneline -1` `752164eb2` — all matched exactly. step 3
block measured 211 newlines, sha256
`72de4eab34a3ae3aef356e383bac7a3b2e7750a9855804e9528724fbecd5cbf6` — equal to the delegation
message's two readings exactly. step 4 `git worktree list | wc -l` 13.

**PAYLOADS:** all three measured exactly against the table — records.diff 50/11217/
`7416637ff513a0012da766e930248d54a78806352687a7bdaad6ba8e5daf1f6a`, tests.diff 91/4166/
`e8e64d83c65a8645c5102031ece6c9dc3e004a3e39e43284bec9e2205b97a819`, plan.md 28/927/
`2b5f7ad77784ba77c27afc640d55a3f3b489b0ffc012bde775b95636108d8462` — full readings match the block's
table digit for digit.

**G1 transport and records:** all four committed `.agent/authored/f291-r4-*` copies (block, plan,
records diff, tests diff) verified byte-identical to their sources with an independent
hash-comparison script (`git show <commit>:<path>` vs. source bytes) — all four equal, the block copy
against `.remedy-wt/f291-r4/block.md` included. The five-row G1 table (three files at C2, two at C4)
was read via `git show <commit>:<path>` with an independent script that computed each file's byte
count and full sha256 and compared both against the block's table; every row matched on both bytes
and the full 64-hex sha256, exactly as the block stated them (`.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md` at C2; `tests/orchestration/test_self_use_generator.py`,
`tests/test_parametrize_ids_stable.py` at C4 — no row printed MISMATCH). Also over the ledger text at
C2: `open_finding_ids` (imported from `scripts/rotate_live_review.py`) read `['R-1114']`,
`latest_gate_verdict` read `PASS` — both equal to the reviewer's reading.

**C2/C4 apply:** `git apply --check` then `git apply`, each exit 0, in order: records.diff,
tests.diff. Every `git diff --numstat` reading matched the block's expected table exactly before
each commit (see per-commit tables above).

**G2 the tests, serially, in the primary checkout at C5:**
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_parametrize_ids_stable.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/regression/test_resource_safety.py tests/test_ble001_ratchet.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
→ `625 passed, 1 skipped in 87.43s (0:01:27)`, `REAL_EXIT=0` — equal to the reviewer's simulated-tree
reading of `625 passed, 1 skipped` at exit 0 exactly. The `-rs` summary printed exactly one SKIPPED
line: `SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md
was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1,
docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog:
re-pin this contract on the split-workflow docs, or retire the test.` — the D12 quarantine, equal to
the reviewer's own reading. Then
```
python3 -m ruff check packages/orchestration/self_use_generator.py tests/test_parametrize_ids_stable.py tests/orchestration/test_self_use_generator.py .agent/authored/f291-r4-mutations.py
```
→ `All checks passed!`, exit 0. `git show --numstat` of `8eeeb23c4` (C3) read `4/0
packages/orchestration/self_use_generator.py`, matching. An independent regex scan of the generator
at C3 for `#\s*noqa:\s*BLE001\b` counted 0 matching lines (the pre-existing `EXCUSE_MARK_WORDS =
"noqa: BLE001"` constant has no `#` before it and does not match). Then
`python3 -m apps.cli.main integrity check --json` → all six checks `status: "pass"`
(`handler_import` handlers=171, `live_review_verdict` last Gate verdict PASS, `plan_consistency`
unchecked=0 context_complete=False, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene`
no reviewer scratch/evidence dir/archive at root, `high_blockers_open` no open blocker/high findings
— R-1114 is Low, so the open set does not block it), `fail_count: 0`, `ok: true`, `passed: true`,
real exit 0.

**G3 the red proofs:** `git worktree add --detach .remedy-wt/f291-r4-mut 22265f346` succeeded.
`python3 -B .agent/authored/f291-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f291-r4-mut`
printed, verbatim:
```
control (before) exit=0 failed=0
x1 (Tier 5's new clause catches ValueError in place of FileNotFoundError): exit=1 failed=1
restored byte-identical: True
x2 (Tier 5's reader skips every read error: the (OSError, UnicodeDecodeError) clause also continues): exit=1 failed=1
restored byte-identical: True
x3 (the guard's new clause catches ValueError in place of FileNotFoundError): exit=1 failed=1
restored byte-identical: True
control (after) exit=0 failed=0
planted dangling link run: exit=0 passed=2 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All three mutations turned red (exit 1, 1 failed each — equal to the reviewer's own probe reading of
1 failed each); both controls passed clean; every restore was byte-identical to the original, checked
by re-reading the mutated file's bytes after restore and comparing to the bytes read before mutation.
Each FROM text was independently verified to occur exactly once in its target file before the tool
was committed (x1 and x2 against `packages/orchestration/self_use_generator.py`, x3 against
`tests/test_parametrize_ids_stable.py`). The planted dangling-link run (a symlink at
`tests/regression/test_runtime_chain_zz_gone.py` pointing at a nonexistent file, filtered to
`-k "fresh_value_at_collection or real_tree_offers_a_module"`) read `2 passed` at exit 0, equal to the
reviewer's own reading, and the link was removed afterward. `git worktree remove --force
.remedy-wt/f291-r4-mut` and `git worktree prune` both exit 0; `git worktree list | wc -l` read 13
afterward — equal to the BEFORE-ANYTHING-ELSE step 4 reading.

**G4 the suite:**
(a) `apps/ui/node_modules/.bin/vite build` (cwd `apps/ui`, via a Python script with the binary's
absolute path): exit 0; last line `- Adjust chunk size limit for this warning via
build.chunkSizeWarningLimit.` (a chunk-size informational warning, not a failure — the build itself
reported `✓ built in 2.35s` and wrote `dist/index.html`, `dist/assets/*`). `git status --porcelain`
after the build: empty.
(b) `python3 -m pytest -n auto -q`: real exit code **0**; wall time measured **214 seconds**
(pytest's own reading: 207.03s, 0:03:27); summary line `20976 passed, 20 skipped, 1 warning in
207.03s (0:03:27)`; bad node ids: **NONE**. Round 3's bad set (from
`.agent/authored/f291-closure-suite.txt` at `752164eb2`) was the single node
`tests/test_parametrize_ids_stable.py::test_no_parametrize_argument_draws_a_fresh_value_at_collection`;
this round's empty set is strictly smaller and holds no newly bad node — the repair removed the only
bad node and introduced none. The full command, exit code, wall time, summary line, bad node reading
and tree SHA are recorded verbatim in `.agent/authored/f291-closure-suite.txt`, committed with this
handback (C6). `git status --porcelain` after the run: empty. `pgrep -af server.py` afterward: no
`server.py` process listed (only the `pgrep` invocation itself, which contains the search string in
its own command line, appears — no actual server process is running). The full suite ran exactly
once this round, in C6 (constraint 7).

**G5 sizes** (`git show --numstat --format= <commit>` for C1 to C5, beside the block's stated
expected insertions where one is given):
| Commit | Reading | Expected | Match |
|---|---|---|---|
| C1 `eb18ece2a` | 380 | 380 (211+169) | equal |
| C2 `bd8017023` | 30/0, 4/0, 8/7 | 30/0, 4/0, 8/7 | equal |
| C3 `8eeeb23c4` | 4/0 | 4/0 | equal |
| C4 `2327dea0e` | 28/1, 25/1 | 28/1, 25/1 | equal |
| C5 `22265f346` | 177/0 | (none stated) | — |

`git status --porcelain`, `git log --oneline -n 7`, plus the push's real outcome and the open-PR
check, are reported in the worker's reply, since C6 (this commit) cannot record itself or anything
that follows it.

**Round's whole tracked path set** (constraint 3), measured with `git diff --name-only 752164eb2`
after C5 (before C6 is committed): `.agent/authored/f291-r4-block.md`,
`.agent/authored/f291-r4-mutations.py`, `.agent/authored/f291-r4-plan.md`,
`.agent/authored/f291-r4-records.diff`, `.agent/authored/f291-r4-tests.diff`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/self_use_generator.py`,
`tests/orchestration/test_self_use_generator.py`, `tests/test_parametrize_ids_stable.py` — every path
is a member of the block's stated set (constraint 3's list, `.agent/authored/f291-closure-suite.txt`
and `.agent/handoff.md` itself added by C6). `tests/regression/test_resource_safety.py` was not
touched this round, confirmed in the same listing.

## Authored-text proofs

All four `.agent/authored/f291-r4-*` payload/block copies (block, plan, records diff, tests diff) are
byte-identical, source to committed copy, verified by an independent hash-comparison script comparing
`.remedy-wt/f291-r4/block.md` and each `.remedy-wt/f291-r4-payloads/*` file against
`git show <commit>:<path>` — all four equal (G1, above). The applied `records.diff` (→
`.agent/decisions.md`, `.agent/live_review.md`, and the rewritten `.agent/plan.md` via
`shutil.copyfile`) and `tests.diff` (→ `tests/orchestration/test_self_use_generator.py`,
`tests/test_parametrize_ids_stable.py`) both reproduced content matching the block's G1 sha256 table
exactly at C2 and C4 respectively — this confirms `git apply` and `shutil.copyfile` reproduced the
reviewer-authored text exactly, not only that the source payload itself was uncorrupted.

## Deviations & assumptions

None from the block's ordered commit sequence — every commit (C1 through C6) landed in order, with
no payload retyped or edited, and no existing test was edited to pass. Every gate the block ordered
(G1 through G5) ran and its real output is reported above and in
`.agent/authored/f291-closure-suite.txt`. The one deliberate implementation choice not dictated
verbatim by the block: mutation x2's edit changes the `raise SelfUseGenerationError(...) from exc`
statement to `continue` inside the `except (OSError, UnicodeDecodeError)` clause that immediately
follows Tier 5's new `except FileNotFoundError` clause — the FROM text spans both clauses (6 lines)
so it is unique to Tier 5's occurrence in `packages/orchestration/self_use_generator.py`, since
`_public_top_level_names` (Tier 4, untouched) has no preceding `FileNotFoundError` clause to make its
otherwise-identical `except (OSError, UnicodeDecodeError)` line ambiguous with Tier 5's. The tool
asserted the multi-line FROM text occurs exactly once before mutating, confirmed by an independent
pre-check script. The C6 full suite ended GREEN at exit 0 with no bad node id, the repair holding
against the reviewer's tests and against xdist. No file outside the round's tracked path set
(constraint 3) was touched (verified above). No `gh pr create` or `gh pr merge`, no checkout of
`main`, no branch deletion, no force-push, no `git stash`, no evidence job, no zip, no self-use run
and no job calling a provider.

## Next

Per the block's `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of
round 4 and of the suite transcript, then the evidence bundle and the review package (the suite is
green). Open findings: 1 (R-1114, whose resolution the reviewer books after this review). Operator
questions: 0.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 copy round 4 block and payloads into .agent/authored/ | done | 380 insertions, matching block's formula exactly |
| C2 book F291 R3, register R-1114, record D4 | done | numstat matched exactly (30/0, 4/0, 8/7); G1 hashes and ledger reading matched |
| C3 skip a test file that vanished while Tier 5 reads tests (R-1114) | done | numstat matched exactly (4/0); 0 BLE001-noqa lines; Tier 4 untouched |
| C4 repair the parametrize-id guard's reader and add the vanished-file tests | done | numstat matched exactly (28/1, 25/1); G1 hashes matched |
| C5 add the round 4 mutation tool | done | ruff clean; all three mutations caught, all controls clean, all restores byte-identical, planted run 2 passed at exit 0 |
| C6 record the repaired tree's suite transcript and rewrite handoff | done | this commit |
| G1 transport and records | done | all payload and authored-copy hashes verified equal; five-row table matched; open_finding_ids `['R-1114']`, latest_gate_verdict PASS |
| G2 the tests | done | 625 passed/1 skipped at exit 0, matching the reviewer's reading; ruff clean; integrity check 6/6 pass, fail_count 0 |
| G3 the red proofs | done | all three mutations caught (exit 1, 1 failed each); all controls clean; all restores byte-identical; planted run 2 passed at exit 0; `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`; worktree count restored to 13 |
| G4 the suite | done | UI build exit 0; full suite exit 0, NONE bad, strictly smaller than round 3's set; no lingering server processes |
| G5 sizes, tree and push | done for C1–C5 sizing; push/log/PR-list reported in the worker's reply |

Open findings: 1 (`R-1114`, per `open_finding_ids` at C2 — this round's repair; the reviewer books its
resolution). Operator questions open: 0.
