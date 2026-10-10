# Handback — F301 round 4: book round 3, DECISION F301 D3, T003's setting and its rules

## Session

SESSION 1 of feature F301 · round 4 · rounds so far 4

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~55 % (claim, T001, T002, the structural steps and T003's rules · T003's command line, T004 and T005 open) — Schätzung

## Range

Review of `1cc583417`..HEAD (five commits on `feature/f301-mission-upkeep` — C1, C2, C3, C4, and
this handback, C5).

## Commits

### `207747119` F301 R4 C1: save the round 4 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f301-r4.md` | 150/0 | NEW FILE — byte copy of `block.md`; sha256 `78fa195539564423ba34b268323976c5fbffd670e514dcc997165080bc7e552a`, 150 lines, equal to `block.md`'s own |

### `cae3775de` F301 R4 C2: book round 3, DECISION F301 D3, the plan, a prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 10/0 | base blob at `1cc583417` + `append-decisions.txt`'s bytes: DECISION F301 D3, booked |
| `.agent/live_review.md` | 2/0 | base blob at `1cc583417` + `append-live_review.txt`'s bytes: round 3's Gate entry, VERDICT PASS, booked |
| `.agent/plan.md` | 8/9 | replaced with `dry-plan.md`: round 4's current step, T003's setting and rules |
| `.agent/prose_slips.md` | 1/0 | base blob at `1cc583417` + `append-prose_slips.txt`'s bytes: one prose-slip line appended |

### `fe1db1554` F301 R4 C3: the setting mission.upkeep_every (T003, DECISION F301 D1)

| Path | +/- | Reason |
|---|---|---|
| `docs/guides/environment.md` | 1/0 | one row added for `REMEDY_MISSION_UPKEEP_EVERY`, in sorted order, by `write_environment_guide()`; nothing else changed |
| `packages/orchestration/config_keys_mission.py` | 12/0 | `MISSION_KEY_SPECS` gains the `mission.upkeep_every` spec at its end: env var `REMEDY_MISSION_UPKEEP_EVERY`, a whole number, default 5 |

### `89c4f14b3` F301 R4 C4: the cadence, the plan, the compiled step, the upkeep job and the skip (T003, DECISIONs F301 D1 and D3)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mission_upkeep.py` | 240/0 | T003: `upkeep_every_setting`, `UpkeepCadence`/`upkeep_cadence`, `plan_upkeep` (and its structure-item and replaced-pairs helpers), `upkeep_has_work`, `compile_upkeep_step`, `UpkeepOutcome`/`make_upkeep_job_if_due`, `record_upkeep_skip`, by DECISIONs F301 D1 (6)-(8) and D3 |
| `tests/orchestration/test_mission_upkeep.py` | 257/1 | tests for every function above: the setting's registration/default/refusal/env var, the cadence's counting and slot-ending lines, the plan's findings/structure/replaced pairs and the compiled step's order, the upkeep job's due/not-due/made/not-needed paths, and the skip's reason and due-ness refusals |

### This commit — F301 R4 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None yet. The block's one push happens AFTER this commit (the "THEN" step), reported in the
worker's final reply after this commit. No pull request is opened this round.

## Verification

**Gate 1** (after C0, before C1): `python3 /home/decodeux/Repos/remedy/.remedy-wt/f301-r4-worker/01_gate1_digests.py`
— sha256 and newline-count check of every file `digests.txt` names in `.remedy-wt/f301-r4/`. All
13 files' hash and count checks `True`; `ALL_TRUE: True`; exit 0.

**Gate 2** (after C4): `git -C /home/decodeux/Repos/remedy status --porcelain` read empty. Re-ran
the C2 step 2 proofs (3 append-proofs against the `1cc583417` blobs + 4 copy-equal checks, 7 of 7
`True`), the C3 step 3 proofs (2 of 2 `True`), and the C4 step 3 proofs (2 of 2 `True`), all at
this commit's own HEAD (no later commit touched any of C2's, C3's or C4's paths again). 11 of 11
`True`; exit 0 each.

**Gate 3** (the round's one test selection, run once):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f301-r4/selection.txt
```
Exit code 0. Summary line: `6528 passed, 4 skipped in 246.79s (0:04:06)`. No `FAILED` or `ERROR`
line anywhere. SKIPPED lines, verbatim:
```
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

**Gate 4**:
```
python3 -m ruff check packages/orchestration/mission_upkeep.py packages/orchestration/config_keys_mission.py tests/orchestration/test_mission_upkeep.py
```
Exit 0. Output: `All checks passed!`

**Gate 5**:
```
python3 -m apps.cli.main integrity check --json
```
Exit 0. `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}` — all six
checks `status: pass` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`).
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit 0. Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1233']
```
Matches the block's ordered list exactly.

**THEN (the push)**: after this commit, reported in the worker's final reply.

## Authored-text proofs

`.agent/authored/f301-r4.md` (C1) equals `block.md` byte for byte: sha256
`78fa195539564423ba34b268323976c5fbffd670e514dcc997165080bc7e552a`, 150 lines, checked at write
time (C1) and not among gate 2's re-run proofs (the block names only C2 step 2, C3 step 3 and C4
step 3 for the re-run).

## Deviations & assumptions

- One compound command during the C0 precondition check: `test -e
  /home/decodeux/Repos/remedy/.agent/STOP && echo PRESENT || echo ABSENT`, run as a single tool
  call combining two commands with `&&` and `||`. The block forbids these even where the sandbox
  would let one through. The read itself was correct (`.agent/STOP` absent) and was immediately
  re-done correctly with a plain `ls` call (exit code 2, "No such file or directory") before any
  commit; no commit, proof or gate used the compound command's output.
- Before the C1 commit, `git branch --show-current` was not re-checked immediately beforehand; the
  branch had last been confirmed during the C0 precondition block, several read-only tool calls
  earlier (the sha256 digest gate, which touches no git state). The block requires the check
  "before EVERY commit." Before C2, C3 and C4 the check was run immediately before each commit's
  own work, and before this commit (C5) as well. A post-hoc check now, after all five commits,
  still reads `feature/f301-mission-upkeep`, so no commit landed on the wrong branch, but the C1
  check was late rather than immediately prior, and is declared here as the block's rule requires.
- The very first sha256 check of `block.md` against the hash stated in the operator's own
  instructions was run as an inline `python3 -c` command before `.remedy-wt/f301-r4-worker/`
  existed; the folder was then created and the SAME check re-run as a saved script
  (`00_sha256_check.py`) inside it, which is the run whose output this reply reports. Not a block
  violation (the block's "every copy, hash, proof and run" rule binds operations the block itself
  orders, C1 onward), noted for completeness.
- The C1 commit-message file was first written with the Write tool
  (`.remedy-wt/f301-r4-worker/commit_msg_c1.txt`), then immediately overwritten with the identical
  text by a Python script (`03_write_commit_msg_c1.py`) before `git commit -F` ever read it. The
  commit that actually landed was made from the Python-script-written file, so the letter of
  "every commit message is written to a file by a Python script" held for the commit itself; the
  detour is declared because the first draft of that file was not.
- `wc -l` was run directly via the Bash tool (a single command, no pipe) to preview line counts of
  three already-tracked files (`mission_upkeep.py`, `test_mission_upkeep.py`,
  `environment.md`) before copying the C4/C3 prepared files over them, rather than reading them
  with the Read tool. No proof, hash, copy or gate relied on this command's output — the actual
  byte-equality proofs used the dedicated scripts — but it is a read-only look that could have
  used the file-reading tool instead, flagged for completeness.

Otherwise: None. C0 through C4 ran exactly as the block ordered, each exactly once, in the block's
sequence; every copy, hash, proof and run the block itself orders was performed by a dedicated
Python script under `.remedy-wt/f301-r4-worker/`, run with an explicit working directory of
`/home/decodeux/Repos/remedy`; no file outside the round's named paths was touched; no
`REMEDY_TEST_MAX_WORKERS` was set and no `-n` was passed; no mutation, no full suite (one selection
run, once), no worktree created or removed, no stash entry touched, no branch created, nothing
merged, no force-push; `.agent/STOP` did not appear at any point; every commit message's final
version was written to a file by a Python script and committed with `git commit -F <file>`;
commit subjects carry no leading-slash token and no absolute path; this round introduced no line
anywhere that trips the retired-word guard the block's constraints name (confirmed by gate 3's full
pass of `tests/docs/`, which includes that guard).

## Round verdicts

F301 round 3's PASS verdict is booked by C2 — the `dry-decisions.md` and `dry-live_review.md`
bytes, proved equal to the base blob at `1cc583417` plus the two append files' bytes, now carry
DECISION F301 D3 and round 3's Gate entry forward in `.agent/decisions.md` and
`.agent/live_review.md`. Round 4's verdict is the reviewer's, to be booked in the next round's
first commit.

## For the operator, in plain sentences

Remedy now has a setting that says after how many finished jobs of a mission a cleanup job comes
next, and it is five unless the operator sets another whole number. When the cleanup job is due,
Remedy plans it by fixed rules from its records: the oldest problems earlier jobs left, at most
five of them, the longest function and the longest code file of the project, and every file that a
newer one replaced. When nothing is left to clean, it makes no job and writes that down. Skipping a
due cleanup job needs a reason, and the reason is written down. The next round lets the operator do
both from the command line. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate).
3. Book round 4's verdict in the next round's first commit.
4. T003 through the command line: `remedy mission continue` and `--skip-upkeep`.

Operator questions open: 0.
Open findings: 16 (R-1233, Low, owned by F301; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch preconditions | done | branch `feature/f301-mission-upkeep`, HEAD = origin = `1cc583417a78020e53fe32fca66201a1a67692aa`, `status --porcelain` empty, `.agent/STOP` absent |
| Gate 1 | passed | all 13 digests `True`, exit 0 |
| C1: save the round 4 block | done | sha256/line count equal to `block.md`; committed `207747119` |
| C2: book round 3, DECISION F301 D3, the plan, a prose slip | done | all 7 byte proofs `True`; committed `cae3775de` |
| C3: the setting mission.upkeep_every | done | self-review checks held (spec ends `MISSION_KEY_SPECS`, one guide row added); 13 insertions; both byte proofs `True`; committed `fe1db1554` |
| C4: the cadence, the plan, the compiled step, the upkeep job and the skip | done | self-review checks held (each function matches D1 (6)-(8) and D3 and nothing more); 497 insertions matches the block's measurement; both byte proofs `True`; committed `89c4f14b3` |
| Gate 2 | passed | status clean; 11 of 11 re-run byte proofs `True` |
| Gate 3 | passed | `6528 passed, 4 skipped in 246.79s`, exit 0, no FAILED/ERROR |
| Gate 4 | passed | ruff exit 0, `All checks passed!` |
| Gate 5 | passed | integrity six checks pass, fail_count 0; open findings match the block's list exactly |
| C5: handback | done | this commit |
| Push | pending | reported in the worker's final reply, after this commit |
