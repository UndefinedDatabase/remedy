# Handback — F264 Steering channel · Round 1 · CLAIM F264 AND LAND T001's FIRST HALF: the sealed steering record and `remedy chat`

## Session

SESSION 1 of feature F264 · round 1 · rounds so far 1

This round cut `feature/f264-steering-channel` from `ef4cb503`, claimed
F264 in `.agent/live_review.md` and `docs/roadmap/STATUS.md`, recorded
DECISION F264 D1 (the steering record's shape and route), and landed
T001's first half: `packages/orchestration/steering.py` (accept, seal,
certify a steering message) and `remedy chat <job_id> "<message>"`,
its first caller, with the tests and red proofs. Well over 90% of this
session's working-context budget remained at handback.

## Range

Review of `ef4cb503`..`HEAD`.

## Commits

### 62b35ae4 F264 R1 C1a: copy round 1 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r1-block.md | +265/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f264-r1-status.diff | +13/-0 | Payload copy |
| .agent/authored/f264-r1-rehead.diff | +62/-0 | Payload copy |
| .agent/authored/f264-r1-plan.md | +33/-0 | Payload copy |
| .agent/authored/f264-r1-context.md | +50/-0 | Payload copy |
| .agent/authored/f264-r1-decisions.diff | +43/-0 | Payload copy |

Measured insertions by `git show --numstat`: 466 (265+201), matching the
block's stated formula "this block's line count plus 201" exactly
(265+201=466). Under the 500 cap.

### 1ab6f838 F264 R1 C1b: copy round 1 product diff and mutation tool into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r1-product.diff | +213/-0 | Payload copy |
| .agent/authored/f264-r1-mutations.py | +85/-0 | Payload copy (G5 red-proof tool) |

Measured insertions: 298, matching the block's expected number exactly.
Under the 500 cap.

### f812a63f F264 R1 C1c: copy round 1 product modules into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r1-steering.py | +186/-0 | Payload copy |
| .agent/authored/f264-r1-chat_cmd.py | +68/-0 | Payload copy |

Measured insertions: 254, matching the block's expected number exactly.
Under the 500 cap.

### e09f557f F264 R1 C1d: copy round 1 test payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f264-r1-test_steering.py | +133/-0 | Payload copy |
| .agent/authored/f264-r1-test_chat_cmd.py | +78/-0 | Payload copy |

Measured insertions: 211, matching the block's expected number exactly.
Under the 500 cap.

### 9df4b960 F264 R1 C2: claim F264 and re-head the live review record

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +26/-23 | `rehead.diff` applied |
| docs/roadmap/STATUS.md | +1/-1 | `status.diff` applied: F264's line flipped to `[~]` (claimed) |
| .agent/plan.md | +20/-14 | Rewritten to round 1's `plan.md` payload (via `shutil.copyfile`) |
| .agent/context.md | +25/-19 | Rewritten to round 1's `context.md` payload (via `shutil.copyfile`) |

Measured insertions by `git show --numstat`: 25 context.md, 26
live_review.md, 20 plan.md, 1 STATUS.md — matching the block's expected
numbers exactly. Under the 500 cap.

### ea455af1 F264 R1 C3: record DECISION F264 D1, the steering record's shape and route

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +35/-0 | `decisions.diff` applied |

Measured insertions: 35, matching the block's expected number exactly.
Under the 500 cap.

### 17fe02d0 F264 R1 C4: accept, seal and certify a steering message, and add remedy chat

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/steering.py | +186/-0 | New module (copy) |
| apps/cli/commands/chat_cmd.py | +68/-0 | New module (copy) |
| apps/cli/command_catalog.py | +24/-3 | `product.diff` applied |
| apps/cli/commands/__init__.py | +2/-1 | `product.diff` applied |
| apps/cli/grouped.py | +2/-1 | `product.diff` applied |
| apps/ui/src/api/humanizeCatalog.ts | +1/-0 | `product.diff` applied |
| docs/guides/exit-codes.md | +1/-0 | `product.diff` applied |
| packages/orchestration/event_names.py | +1/-0 | `product.diff` applied |
| tests/cli/test_cli_ux.py | +5/-4 | `product.diff` applied |
| tests/cli/test_golden_path.py | +1/-1 | `product.diff` applied |
| tests/orchestration/import_reachability_allowlist.txt | +2/-0 | `product.diff` applied |
| tests/test_command_catalog.py | +2/-2 | `product.diff` applied |

Measured insertions by `git diff --cached --numstat` before commit: 186
steering.py, 68 chat_cmd.py, 24 command_catalog.py, 2 __init__.py, 2
grouped.py, 1 humanizeCatalog.ts, 1 exit-codes.md, 1 event_names.py, 5
test_cli_ux.py, 1 test_golden_path.py, 2 import_reachability_allowlist.txt,
2 test_command_catalog.py — matching the block's expected numbers exactly.
Total 295 insertions. Under the 500 cap.

### 4fe1fae6 F264 R1 C5: test the steering record and remedy chat

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_steering.py | +133/-0 | New test file (copy) |
| tests/cli/test_chat_cmd.py | +78/-0 | New test file (copy) |

Measured insertions: 133 test_steering.py, 78 test_chat_cmd.py — matching
the block's expected numbers exactly. Under the 500 cap.

### (uncommitted at handback time) F264 R1 C6: rewrite handoff for round 1

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git checkout -b feature/f264-steering-channel` from `main` at
  `ef4cb503` — real exit 0 (Open PR Gate had already run; `main` carried
  the merge commit, so no pull was needed).
- `git worktree add --detach .remedy-wt/f264-r1-mut 4fe1fae6` for G5 —
  real exit 0; removed afterward with `git worktree remove --force
  .remedy-wt/f264-r1-mut` — real exit 0 — and `git worktree prune`.
  `git worktree list` afterward: primary checkout plus the reviewer's
  `.remedy-wt/f264-r1-dry`, `.remedy-wt/f264-r1-sim`, and the four
  pre-existing `.remedy-wt/job-*` worktrees — nothing else, matching
  constraint 6.
- No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
  branch was cut, no branch deletion, no force-push, no `git stash` in
  any form.
- `git push -u origin feature/f264-steering-channel` — ordered after C6;
  its real outcome is reported in the worker's final reply, not in this
  committed file (it has not run yet when this file is written and
  committed as part of C6).

## Verification

**G1 — transport**: each of the eleven payloads' lines/bytes/sha256
measured against the block's PAYLOADS table — all eleven rows matched
exactly. The block itself: 265 lines (newline count), 18587 bytes,
sha256 `d51c1d2028ec8f214db0fbb8a057636ef099ff21e2c5be4272c592f65b4e7fcf`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f264-r1-*` blob read with `git show
<commit>:<path>` compared byte-for-byte against its
`.remedy-wt/f264-r1-payloads/` (or block) source: all twelve pairs
byte-identical = True.

**G2 — the bookkeeping**: at C2 (`9df4b960`), `.agent/live_review.md`
309547 bytes, sha256
`b0b29bde1e5e4ce93b8a7cbf1031d900a1e00ea1cac25cdba388cfc6bb1aa8aa`;
`docs/roadmap/STATUS.md` 48679 bytes, sha256
`b078c6d9c695e6593c9d8d867776892788f6e9588e88f8b27ed5e86a13b28a48`;
`.agent/plan.md` 1186 bytes, sha256
`5f1928decf859545d33bc454751f62ad6da8c57ed44ba5950c6ee1d7a0886600`;
`.agent/context.md` 2468 bytes, sha256
`63f5b98a9124bf0d105e8bb492ef752e5ef6d63aa61ad7518532bc8ede5dd9cc` — all
four equal to the block's table exactly. At C3 (`ea455af1`),
`.agent/decisions.md` 1939657 bytes, sha256
`234f0931e7cca34f3ebfb3ca9c32102f7f33794a6d932f0abf926b678cef2ca4` — equal
to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 3 at
`ef4cb503` (`R-0499`, `R-0950`, `R-1008`), 3 at C2 (`9df4b960`), same
three ids; both set differences (`base - head`, `head - base`) empty —
matching the block's reading exactly. F264's STATUS line at C2 read back
in full: `- [~] F264 — Steering channel (remedy chat)`, matching the
block's required reading exactly. `git diff --name-only e09f557f
9df4b960`: exactly `.agent/context.md`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/roadmap/STATUS.md`, matching C2's path list.
`git diff --name-only 9df4b960 ea455af1`: exactly `.agent/decisions.md`,
matching C3's path list.

**G3 — the product**: at C5 (`4fe1fae6`), each of the fourteen files
read with `git show 4fe1fae6:<path>` equal to the reviewer's simulated
reading — all fourteen byte counts and sha256 digests matched exactly
(`packages/orchestration/steering.py`, `apps/cli/commands/chat_cmd.py`,
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`,
`apps/cli/grouped.py`, `apps/ui/src/api/humanizeCatalog.ts`,
`docs/guides/exit-codes.md`, `packages/orchestration/event_names.py`,
`tests/cli/test_cli_ux.py`, `tests/cli/test_golden_path.py`,
`tests/orchestration/import_reachability_allowlist.txt`,
`tests/test_command_catalog.py`, `tests/orchestration/test_steering.py`,
`tests/cli/test_chat_cmd.py`). `git diff --name-only ea455af1 17fe02d0`:
exactly the twelve paths C4 lists. `git diff --name-only 17fe02d0
4fe1fae6`: exactly the two paths C5 lists.

**G4 — the tests**: in the primary checkout at C5, the ordered pytest
selection: `1095 passed in 89.85s`, real exit 0. The reviewer's sim
(without golden path, inside a worktree lacking the UI toolchain) read
`1051 passed, 2 skipped`; the golden path alone there read `42 passed`
(1051+2+42=1095) — the two prior skips pass here because the primary
checkout carries the UI toolchain a worktree lacks, exactly as the block
anticipates. `python3 -m ruff check` over the eleven named files: `All
checks passed!`, real exit 0. `python3 -m apps.cli.main integrity check
--json`, real exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=149", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`handlers=149` matches the reviewer's sim reading exactly.

**G5 — the red proofs**: `python3 -B .remedy-wt/f264-r1-payloads/mutations.py
.remedy-wt/f264-r1-mut` against the detached worktree at C5, real exit 0
overall, matching the reviewer's readings on every mutation exactly:
control_before `28 passed` exit 0; m1 `4 failed` exit 1; m2 `2 failed`
exit 1; m3 `1 failed` exit 1; m4 `1 failed` exit 1; m5 `1 failed` exit 1;
m6 `1 failed` exit 1; m7 `1 failed` exit 1; m8 `1 failed` exit 1; m9 `4
failed` exit 1; control_after `28 passed` exit 0; every `restored
byte-identical` line True.

**G6**: reported in the worker's final reply only, per the block (not
in this committed handback).

## Authored-text proofs

- `.agent/authored/f264-r1-block.md` (C1a) ==
  `.remedy-wt/f264-r1-block.md`: byte-identical True (18587 bytes, 265
  lines, sha256
  `d51c1d2028ec8f214db0fbb8a057636ef099ff21e2c5be4272c592f65b4e7fcf`).
- `.agent/authored/f264-r1-status.diff`, `-rehead.diff`, `-plan.md`,
  `-context.md`, `-decisions.diff` (C1a) == their
  `.remedy-wt/f264-r1-payloads/` sources: byte-identical True, all five.
- `.agent/authored/f264-r1-product.diff`, `-mutations.py` (C1b) == their
  payload sources: byte-identical True, both.
- `.agent/authored/f264-r1-steering.py`, `-chat_cmd.py` (C1c) == their
  payload sources: byte-identical True, both.
- `.agent/authored/f264-r1-test_steering.py`, `-test_chat_cmd.py` (C1d)
  == their payload sources: byte-identical True, both.
- `rehead.diff` and `status.diff` were applied at C2 with `git apply
  --check` then `git apply` directly from the payloads' own bytes —
  never retyped, all real exit 0.
- `.agent/plan.md` and `.agent/context.md` at C2 == their payload
  sources verbatim (rewrite by `shutil.copyfile`): byte-identical True
  (confirmed by the G2 sha256 readings above and the payload table).
- `decisions.diff` was applied at C3 with `git apply --check` then `git
  apply` directly from the payload's own bytes — never retyped, both
  real exit 0.
- `steering.py` and `chat_cmd.py` were copied to their product paths at
  C4 with `shutil.copyfile`, then `product.diff` was applied with `git
  apply --check` then `git apply` directly from the payload's own
  bytes — never retyped, all real exit 0.
- `test_steering.py` and `test_chat_cmd.py` were copied to their test
  paths at C5 with `shutil.copyfile` — never retyped.
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and every diff was applied by `git apply` reading
  the payload file directly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 466 insertions, matches block formula (265+201) exactly |
| C1b | done | 298 insertions, matches block exactly |
| C1c | done | 254 insertions, matches block exactly |
| C1d | done | 211 insertions, matches block exactly |
| C2 | done | 25/26/20/1 insertions by `git show --numstat`, matches block exactly |
| C3 | done | 35 insertions, matches block exactly |
| C4 | done | 186/68/24/2/2/1/1/1/5/1/2/2 insertions, matches block exactly |
| C5 | done | 133/78 insertions, matches block exactly |
| C6 | done | this handback commits with it |
| Push | done | ordered after C6; real outcome in the final reply |
| G1 | done | all eleven payload readings match; all twelve authored copies byte-identical |
| G2 | done | all five sha256/byte readings match; open-set 3 at both ef4cb503 and C2, both differences empty; STATUS line reads exactly as required; both name-only diffs match |
| G3 | done | all fourteen C5 files byte/sha match; both name-only diffs (C3..C4, C4..C5) match |
| G4 | done | 1095 passed exit 0 (consistent with reviewer's 1051+2+42); ruff all checks passed exit 0; integrity check all six pass, fail_count 0, handlers=149 |
| G5 | done | all nine mutations plus both controls match the reviewer's readings exactly; every restore byte-identical |
| G6 | done | readings reported in the final reply only, per the block |

## Deviations & assumptions

None. Every measured number matched the block's stated expectation
exactly, and the commit sequence landed in the block's exact order
C1a-C1b-C1c-C1d-C2-C3-C4-C5-C6. No gate went red. No payload was edited
or retyped; every copy used `shutil.copyfile` and every diff was applied
via `git apply` reading the payload file directly. This round is SESSION
1 of F264, its first round. No pull request is opened this round
(constraint 5): the branch opens one at F264's closure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
1, then T001's second half — `chat.send` exposed on F009's write channel
as the cockpit's route. Open findings count: 3. Operator-questions
count: 0.
