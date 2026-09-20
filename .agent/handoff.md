# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 11

## Session

SESSION 6 of feature F277 · round 11 · rounds so far 11

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`.remedy-wt/f277-r11-block.md` and `docs/roadmap/features/T2_F277.md` in full, verified the
step block's own bytes before using it (R-0954: measured 214 lines, sha256
`910fde83ebae596d4f6a180697ff1b9fd0a2ac648366d685085631f783413d5e`, matching both of the
delegation message's readings exactly), found no `.agent/STOP` on disk, verified the branch
was already `feature/f277-machine-contracts` clean at `e90faf51`, then verified all four
PAYLOADS entries (line count + bytes + sha256) against the block's table before using any of
them — all four matched exactly. Executed the four-commit bundle (C1a, C1b, C2, C3) in order,
ran all six gates for real, and pushed. This is the session's LAST round.

## Range

Review of `e90faf51`..`HEAD`.

## Commits

### f0dfad5e F277 R11 C1a: copy round 11 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r11-block.md | +214/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r11-ledger.md | +2/-0 | byte-for-byte copy of ledger.md payload |
| .agent/authored/f277-r11-plan.md | +49/-0 | byte-for-byte copy of plan.md payload |
| .agent/authored/f277-r11-slips.md | +2/-0 | byte-for-byte copy of slips.md payload |

Measured insertions: 267 (214+2+49+2). Block's formula: block's own line count (214) plus 53
(2+49+2) = 267. Matches exactly.

### cf2dc62a F277 R11 C1b: book round 10's PASS and two slips, rewrite plan
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append round 10 PASS entry (ledger.md payload) |
| .agent/prose_slips.md | +2/-0 | append two prose-slip lines (slips.md payload) |
| .agent/plan.md | +18/-18 | rewrite to plan.md payload, byte-identical |

Measured insertions by `git show --numstat`: 22 (2+2+18). Matches the block's expected
reading exactly (2 + 2 + 18 = 22). `.agent/decisions.md` was not touched — there is no
decisions payload this round.

### e44f10b9 F277 R11 C2: migrate the memory group onto the shared fail helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/memory.py | +27/-19 | apply s1-memory.diff: migrate nine refusal sites onto `fail()`, drop the now-unused `import sys`, thread `json_output` into the five card-mutation handlers and their COMMAND_HANDLERS entries |
| tests/cli/test_memory_cmd.py | +116/-0 | apply s1-memory.diff: new file (created by the diff, explicitly `git add`ed since `git apply` leaves a created file untracked); the group's refusal-site coverage plus the catalog guard test |

Measured insertions: 143 (27+116). Matches expected exactly.

Self-reference exception (handback template): the following commit, which only writes this
handoff, and any trailing bookkeeping commit that only fills in its post-push readings, share
one grouped table with per-commit attribution in the Reason column — a handback cannot table
the commit that writes it (R-0149 pattern), following rounds 9 and 10's identical precedent.

### (this commit) F277 R11 C3: rewrite handoff for round 11
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, first write, with placeholder G6 push/status/worktree readings not yet knowable before the push |

### (trailing) F277 R11 C3-fix: record the actual push outcome in the handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this edit | fill in the real `git push`/`git status`/`git worktree list` output for G6, only knowable after C3 was pushed |

## External actions

- `git worktree add --detach .remedy-wt/f277-r11-g5 e44f10b9` — succeeded, for G5's mutation
  red-proofs.
- `git worktree remove .remedy-wt/f277-r11-g5` — succeeded, as G5's last action.
- `git push -u origin feature/f277-machine-contracts` — reported under Verification/G6 below
  (the round's final act).

## Verification

### Pre-flight

- `ls .agent/STOP` → `No such file or directory`.
- `git status --porcelain` → empty.
- `git branch --show-current` → `feature/f277-machine-contracts`.
- `git rev-parse HEAD` → `e90faf517920b7f6650663648d8ce601ff2b0f12`. Matches the block's stated
  tip (`e90faf51`).
- Block self-verification (R-0954): measured 214 lines, sha256
  `910fde83ebae596d4f6a180697ff1b9fd0a2ac648366d685085631f783413d5e` for
  `.remedy-wt/f277-r11-block.md`. Both match the delegation message's two readings exactly.

### G1(a) — PAYLOADS transport, all four files

| file | lines measured | lines expected | bytes measured | bytes expected | sha256 match |
|---|---|---|---|---|---|
| ledger.md | 2 | 2 | 4388 | 4388 | True (`33f0e0a13bd36d5aa724cebb5d2c2047e71f549038aa8663bf21d1b8c2455811`) |
| plan.md | 49 | 49 | 2679 | 2679 | True (`922b9ab526eec009b77ea90d90faaabd78afcbfdc56225b0c31a7baa160d8ee1`) |
| slips.md | 2 | 2 | 1875 | 1875 | True (`40b4f76db324004721064d71770d009a2d9eec3be93b62907dc708f12a6afe3d`) |
| s1-memory.diff | 294 | 294 | 11857 | 11857 | True (`dc77324d5e107ed4ff8e20f7659fe48d903f7ccf7460501508c4d6a2f79aca1e`) |

All four equal. `git apply --check .remedy-wt/f277-r11-payloads/s1-memory.diff` exit code: 0,
run before the real `git apply` (also exit 0).

### G1(b) — the four `.agent/authored/f277-r11-*` copies vs. their sources

| copy | source | `cmp` result |
|---|---|---|
| f277-r11-block.md | .remedy-wt/f277-r11-block.md | True |
| f277-r11-ledger.md | .remedy-wt/f277-r11-payloads/ledger.md | True |
| f277-r11-plan.md | .remedy-wt/f277-r11-payloads/plan.md | True |
| f277-r11-slips.md | .remedy-wt/f277-r11-payloads/slips.md | True |

Four readings, all True.

### G1(c) — the two appends at C1b, pre/payload/post, plus the negative control

| file | pre (bytes at e90faf51) | payload (bytes) | post (bytes at C1b) | pre+payload=post |
|---|---|---|---|---|
| .agent/live_review.md | 435266 | 4388 | 439654 | True |
| .agent/prose_slips.md | 340325 | 1875 | 342200 | True |

Two readings, both True. Negative control, on `.agent/live_review.md` only: reconstructed
`pre + payload` in a scratch script, flipped one bit at offset `len(pre) + 5` inside the
appended region, and compared against the real post-append bytes — unflipped comparison:
True; flipped comparison: False, as required.

### G1(d) — `.agent/plan.md` at C1b vs. `plan.md` payload

Both sha256 `922b9ab526eec009b77ea90d90faaabd78afcbfdc56225b0c31a7baa160d8ee1`. Equal.
49 lines, under the 50-line rule.

### G1(e) — open set by distinct id in `.agent/live_review.md`

At `e90faf51`: 27 distinct ids matching `^- R-\d+ — ` minus 7 distinct ids matching
`^Done: R-\d+ — ` = 20.
At C1b (`cf2dc62a`): re-measured the same way = 27 distinct registered minus 7 distinct done =
20 (round 11's ledger append registers/resolves nothing under this pattern, so the two-line
append to `.agent/live_review.md` does not change the distinct-id open count).
Both readings: 20 and 20, as required — reported as measured, not merely claimed equal.

### G1(f) — `.agent/decisions.md` not touched

`git diff --name-only e90faf51 cf2dc62a` named exactly: `.agent/authored/f277-r11-block.md`,
`.agent/authored/f277-r11-ledger.md`, `.agent/authored/f277-r11-plan.md`,
`.agent/authored/f277-r11-slips.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/prose_slips.md`. `.agent/decisions.md` does not appear, as required.

### G2 — code transport, blob ids at C2 (e44f10b9)

| path | blob id measured | blob id expected | match |
|---|---|---|---|
| apps/cli/commands/memory.py | d973107be1cd64dfea3b9c4d0c5bcb6a93d45acf | same | True |
| tests/cli/test_memory_cmd.py | 67d4d3b4d9f50f1ac868485976091d7db93631f4 | same | True |

Both match. `git diff --name-only cf2dc62a e44f10b9` named exactly these two paths, length 2,
no third — `tests/cli/test_memory_cmd.py` is present, confirming the explicit `git add` for
the diff-created file was not omitted.

### G3 — targeted suite, in the primary checkout at C2

```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_memory_cmd.py \
  tests/test_data_paths.py tests/test_grouped_cli.py tests/test_command_catalog.py \
  tests/cli/test_command_catalog.py tests/orchestration/test_import_reachability.py \
  tests/test_no_orphan_modules.py tests/cli/test_golden_path.py tests/docs
806 passed in 156.21s (0:02:36)
```
Exit code: 0. Matches the reviewer's stated dry-run reading of `806 passed` exactly. Full
suite was NOT run, per amend0917 rule 1.

### G4 — lint over the two G2 paths

```
$ python3 -m ruff check apps/cli/commands/memory.py tests/cli/test_memory_cmd.py
All checks passed!
```
Exit code: 0.

### G5 — mutation red-proofs, disposable worktree

`git worktree add --detach .remedy-wt/f277-r11-g5 e44f10b9` → succeeded, detached HEAD at
`e44f10b9`.

Unmutated control: `13 passed in 0.23s`, exit 0. Matches the block's stated `13 passed`
reading.

| mutation | anchor count | expected | result | exit | failed node ids |
|---|---|---|---|---|---|
| (a) all five byte-identical `memory_card_not_found` refusals: `fail("memory_card_not_found", f"memory card not found: {memory_id}",` → `fail("card_missing", ...)` | 5 (matches the block's stated FIVE, not the usual one) | 5 failed, 8 passed | 5 failed, 8 passed | 1 | `test_under_json_it_is_an_envelope_on_stdout[_cmd_memory_card_show-get_memory_card-None]`, `test_under_json_it_is_an_envelope_on_stdout[_cmd_memory_card_approve-approve_memory_card-None]`, `test_under_json_it_is_an_envelope_on_stdout[_cmd_memory_card_reject-reject_memory_card-None]`, `test_under_json_it_is_an_envelope_on_stdout[_cmd_memory_card_stale-mark_stale-None]`, `test_contradict_threads_the_flag_through_its_two_ids` |
| (b) supersede's own wording: drop "old " from its message | 1 | 1 failed, 12 passed | 1 failed, 12 passed | 1 | `test_supersede_names_the_OLD_card_and_keeps_its_own_wording` |
| (c) `invalid_job_id` fail: `json_output=json_output` → `json_output=False` | 1 | 1 failed, 12 passed | 1 failed, 12 passed | 1 | `test_an_unknown_job_is_an_envelope_under_json` |
| (d) sever the flag above `approve_memory_card` import with `json_output = False` | 1 | 1 failed, 12 passed | 1 failed, 12 passed | 1 | `test_under_json_it_is_an_envelope_on_stdout[_cmd_memory_card_approve-approve_memory_card-None]` |
| (e) sever the flag above `contradict_memory_card` import with `json_output = False` | 1 | 1 failed, 12 passed | 1 failed, 12 passed | 1 | `test_contradict_threads_the_flag_through_its_two_ids` |

Every anchor count matched the block's stated count exactly, including mutation (a)'s FIVE.
Every reading matches the block's expected numbers and node ids exactly. Each mutation was
applied and reverted in one script run per mutation, with `M.read_bytes() == ORIG` confirmed
true after every single revert. No mutation stayed green.

Restored control (after all five reverts): `13 passed in 0.23s`, exit 0.
`git status --porcelain` in the mutation worktree, checked before removal: empty.

`git worktree remove .remedy-wt/f277-r11-g5` → succeeded. `git worktree list` after removal
shows the primary checkout and the two pre-existing `remedy/job-*` worktrees only (see G6).

### G6 — push and tree, after C3

- `git push -u origin feature/f277-machine-contracts` →
  `e90faf51..8bdf7d78 feature/f277-machine-contracts -> feature/f277-machine-contracts`.
  Succeeded.
- `git status --porcelain` after the push: empty.
- `git worktree list` after the push:
```
/home/decodeux/Repos/remedy                                  8bdf7d78 [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```
  Primary checkout plus the two pre-existing `remedy/job-*` worktrees, nothing else.

## Authored-text proofs

The four `.agent/authored/f277-r11-*` files copied at C1a were each compared byte-for-byte
(`cmp`) against their reviewer-authored source under `.remedy-wt/f277-r11-payloads/` (the
block copy against `.remedy-wt/f277-r11-block.md`). All four: True. See G1(b) above.

## Deviations & assumptions

1. **A trailing C3-fix commit, following rounds 9 and 10's identical precedent (C7/C7-fix,
   C4/C4-fix).** C3 writes this handoff with the G6 push outcome not yet knowable (the push
   is C3's own trailing action per the block's own instruction: "rewrite handoff, then
   push"); C3-fix fills in the real `git push`/`git status`/`git worktree list` readings for
   G6 once they exist. This is the handback template's explicit "trailing bookkeeping
   commits that only trim it" exception (R-0149 pattern).
2. No other deviation. The four-commit bundle (C1a, C1b, C2, C3) was executed in the block's
   exact order, none dropped, none added beyond the documented C3-fix, none reordered.

## Next

Phase 1 rule 1 first: read `.agent/STOP` from disk. Then the review of round 11 (this round's
C1a/C1b/C2/C3, all six gates). Then T003's remaining modules in the order `.agent/plan.md`
lists them: `job` (44 sites), `decision` (31), `project` (25), `brain` (24), `do` (19),
`patch` (18), `grouped` (8), `test_cmds` (7), then the tail; `runtime_cmd.py` is its own round
(27 sites, exit codes 2-5, `error_class` supervisor contract); T003 then closes with the
catalog half (33 read-only commands without `supports_json`). Then T004 (exit-code taxonomy +
sweep) and closure. Open findings count: 20. Operator-questions count: 1.
