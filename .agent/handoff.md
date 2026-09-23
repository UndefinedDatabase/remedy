# Handback — F263 Human-change absorption (absorb) · Round 4 · Book round 3's PASS, record DECISION F263 D4, land T002 `remedy absorb` — PASS

## Session

SESSION 1 of feature F263 · round 4 · rounds so far 4

This round booked round 3's PASS into the ledger with DECISION F263 D4
(C2), then landed T002 in one bundle: `packages/orchestration/human_change.py`'s
new `absorb_job`/`JobAbsorbOutcome`, `packages/orchestration/worktrees.py`'s
new `lock_is_held`, the new `apps/cli/commands/absorb_cmd.py` handler, its
catalog entry, visible help slot (`VISIBLE_GROUP_ORDER`, group count 32)
and bare form, plus the three pinned tests that move with it (C3). G1
through G5 all ran and every reading matched the block's stated
expectation, including the pytest count divergence the block itself
anticipated (my run, unlike the reviewer's disposable-worktree dry run,
included `tests/cli/test_golden_path.py` as the block's own G4 command
orders). Context self-assessment: nearly all of the session's working
context budget remained at handback.

## Range

Review of `d5fe145f`..`HEAD`.

## Commits

### 46131302 F263 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r4-block.md | +211/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f263-r4-ledger.md | +2/-0 | Payload copy |
| .agent/authored/f263-r4-decisions.md | +41/-0 | Payload copy |
| .agent/authored/f263-r4-plan.md | +30/-0 | Payload copy |

Measured insertions by `git show --numstat 46131302`: 284 (211+41+2+30),
matching the block's stated formula "this block's line count plus 73"
(211 + 73 = 284) exactly. Under the 500 cap.

### 09e59026 F263 R4 C1b: copy round 4 product payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r4-product.diff | +185/-0 | Payload copy |
| .agent/authored/f263-r4-absorb_cmd.py | +98/-0 | Payload copy |
| .agent/authored/f263-r4-pins.diff | +65/-0 | Payload copy |

Measured insertions by `git show --numstat 09e59026`: 348 (185+98+65),
matching the block's expected 348 exactly.

### aa15014e F263 R4 C1c: copy round 4 test payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r4-test_absorb_cmd.py | +167/-0 | Payload copy |
| .agent/authored/f263-r4-mutations.py | +81/-0 | Payload copy (G5 tool) |

Measured insertions by `git show --numstat aa15014e`: 248 (167+81),
matching the block's expected 248 exactly.

### d0890e7f F263 R4 C2: book round 3's PASS and DECISION F263 D4

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +41/-0 | Append of decisions.md payload (DECISION F263 D4) |
| .agent/live_review.md | +2/-0 | Append of ledger.md payload (round 3's PASS entry) |
| .agent/plan.md | +8/-9 | Rewritten to the round-4 `plan.md` payload |

Measured insertions by `git show --numstat d0890e7f`: `41 0
.agent/decisions.md`, `2 0 .agent/live_review.md`, `8 9 .agent/plan.md`
— matching the block's expected 41, 2, 8 exactly.

### ec4ee4bc F263 R4 C3: add remedy absorb over the one absorb path

| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +20/-2 | `git apply` of product.diff — `absorb` group, `VISIBLE_GROUP_ORDER` entry, `absorb.run` catalog entry |
| apps/cli/commands/__init__.py | +2/-1 | `git apply` of product.diff — registers `absorb_cmd` in `collect_all_handlers` |
| apps/cli/grouped.py | +3/-2 | `git apply` of product.diff — `absorb` in `_DEFAULT_COMMAND` and `_ALWAYS_INJECT` (bare form) |
| packages/orchestration/human_change.py | +39/-0 | `git apply` of product.diff — `JobAbsorbOutcome`, `absorb_job` |
| packages/orchestration/worktrees.py | +22/-0 | `git apply` of product.diff — `lock_is_held` |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `git apply` of product.diff — `apps.cli.commands.absorb_cmd` allowlisted |
| tests/test_command_catalog.py | +3/-1 | `git apply` of pins.diff — visible-group-order pin, group count 32 |
| tests/cli/test_cli_ux.py | +6/-4 | `git apply` of pins.diff — `_USER_FACING_GROUPS`, D4 partition count 32 |
| tests/cli/test_golden_path.py | +2/-1 | `git apply` of pins.diff — help-pinning docstring |
| apps/cli/commands/absorb_cmd.py | +98/-0 | New file, copied whole from absorb_cmd.py payload |
| tests/cli/test_absorb_cmd.py | +167/-0 | New file, copied whole from test_absorb_cmd.py payload |

Measured insertions by `git show --numstat ec4ee4bc`: 20, 2, 98, 3, 39,
22, 167, 6, 2, 1, 3 — matching the block's expected 20/2/98/3/39/22/167/6/2/1/3
exactly (363 total insertions, 11 deletions). `git apply --check` then
`git apply` for product.diff: real exit 0, 0. `git apply --check` then
`git apply` for pins.diff: real exit 0, 0. Both new files `git add`ed
before commit — `relevant_untracked` reads 0 at G4.

### (this commit) F263 R4 C4: rewrite handoff for round 4

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f263-r4-mut ec4ee4bc` (at C3) for
  G5: real exit 0.
- `git worktree remove --force .remedy-wt/f263-r4-mut`: real exit 0.
  `git worktree prune`: real exit 0.
- No `gh pr create`, no merge, no branch deletion — none ordered, none
  taken.
- `git push origin feature/f263-human-change-absorption` after C4 — real
  outcome reported in the worker's final reply (G6 readings cannot live
  in this committed file per the block).

## Verification

**G1 — transport**: every payload's lines/bytes/sha256 measured against
the block's PAYLOADS table: all eight rows matched exactly (ledger.md
2/2244, decisions.md 41/3115, plan.md 30/1163, product.diff 185/9570,
absorb_cmd.py 98/4118, pins.diff 65/3094, test_absorb_cmd.py 167/6800,
mutations.py 81/2936 — sha256 digests all equal to the table). Every
committed `.agent/authored/f263-r4-*` blob read with `git show
<commit>:<path>` compared byte-for-byte against its `.remedy-wt/` source:
all nine pairs (the block plus the eight payloads) byte-identical = True.

**G2 — the booking**: pre-C2 `.agent/live_review.md` (377686 bytes) +
ledger.md payload (2244 bytes) = 379930 bytes, matching `git show
d0890e7f:.agent/live_review.md` sha256
`1a669d064f7c6b410289bb7d7ea9ff0f3b5759c5631b150d72b4340f35c8108c`
exactly. Pre-C2 `.agent/decisions.md` (1882987 bytes) + decisions.md
payload (3115 bytes) = 1886102 bytes, matching sha256
`d2f6f01249ee5cf5a398c827a6aec7ab12678f025b15fdc5a482d69e80e50fd6`
exactly. `.agent/plan.md` at C2 equals plan.md payload: 1163 bytes, sha256
`11b32fa937b036ca348b8bd0472ea49a37cc522aac7ce3b832881750f9a4df7d` — all
three match the block's reviewer-simulated table exactly. Open finding
ids via `scripts/rotate_live_review.py`'s `open_finding_ids(text)` read
against `.agent/live_review.md`: at base `d5fe145f`, count 28; at C2
`d0890e7f`, count 28; both set differences empty — matching the block's
reading of 28, 28, both empty exactly.

**G3 — the product bytes**: at C3 (`ec4ee4bc`), `git show ec4ee4bc:<path>`
for all eleven paths in the block's table — bytes and sha256 both
matched exactly:

| path | bytes | sha256 | match |
|---|---|---|---|
| packages/orchestration/human_change.py | 13476 | a8d2e52ad1f901981c79bbf35b4b65ac63f0bca4862b26d2a44c9a4050edb6f2 | True |
| packages/orchestration/worktrees.py | 32486 | f60edc5e59e7544dce3faff9b91d835677587e51270d61880c90da61359141db | True |
| apps/cli/command_catalog.py | 111748 | ab3cb70b386def9d8ed6ab4a0ebe9d84c397095f9ec4c5fd437a2d22d46f82fa | True |
| apps/cli/grouped.py | 28934 | b6bcf7dde1158b31783af3c33e8ba693eb4a132380493875141d408a68dac329 | True |
| apps/cli/commands/__init__.py | 2065 | ac8cfcb63b70b50850bcbcf2256078caa6d757c487b9637295c4db330ded8c5a | True |
| tests/orchestration/import_reachability_allowlist.txt | 9932 | fcb6cdc1dc8c3b9c0ce2548aaa1ba2349ef6eaa8caa70c28129f6c05439266e3 | True |
| tests/test_command_catalog.py | 22526 | 1f03949b66afe54dfc2a31a2a62f2333e68030e8a5acf8a759e04fffa4047e30 | True |
| tests/cli/test_cli_ux.py | 39149 | a74a39b3fdd97e8841ed86c459cfd9b505f87fd096938d8097965628f8eb82fe | True |
| tests/cli/test_golden_path.py | 34675 | 633a0384d1fa63d56960870de63e8f3d1657c17b2425db58576906fc9733673d | True |
| apps/cli/commands/absorb_cmd.py | 4118 | a96e0f27501a0abe0a76537f07069dfb9f4b4bb28a8b5a7e3f12cbc5bf367bd1 | True |
| tests/cli/test_absorb_cmd.py | 6800 | 8ba2357b44e83fc8f122185300ad36dc576c08a7ade495ffc8039714dceab3b0 | True |

All eleven pairs equal the block's table.

**G4 — the tests and the lint, ALL PASSING**: in the primary checkout at
C3, SERIALLY: `python3 -m pytest -q -p no:cacheprovider` over the block's
exact 22-path selection (including `tests/cli/test_golden_path.py`, which
the block's own command orders here, unlike the reviewer's disposable-
worktree dry run which excluded it) → `1738 passed in 340.75s`, real exit
0 (`PIPESTATUS[0]`). The reviewer's own run (without the golden path, in
a disposable worktree) read `1694 passed, 2 skipped` at exit 0; my run
read 0 skipped and 44 more passing tests — the golden path's own tests
plus this primary checkout's environment (no external-binary probe
skipped here that the reviewer's disposable worktree skipped) account for
the delta; no failures either way, so this is reported as read, not
treated as a red gate (the block orders "report what you read", as it did
at round 3 for the identical pattern). Then `python3 -m ruff check .`
over the WHOLE repository from its root: `All checks passed!`, real exit
0. `python3 -m apps.cli.main integrity check --json`: all five checks
(`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) `pass`, `fail_count: 0`,
`ok: true`, `passed: true`, real exit 0.

**G5 — the red proofs, all matching**: `git worktree add --detach
.remedy-wt/f263-r4-mut ec4ee4bc` real exit 0; `python3 -B
.remedy-wt/f263-r4-payloads/mutations.py .remedy-wt/f263-r4-mut`, real
exit 0 overall: `control_before` `11 passed` exit 0; `m1_running_job_rewritten`
1 failed exit 1; `m2_lock_probe_never_sees_a_holder` 2 failed exit 1;
`m3_rebase_leaves_the_ref` 1 failed exit 1; `m4_rebase_not_persisted` 2
failed exit 1; `m5_every_repository_absorbed` 1 failed exit 1;
`m6_job_option_ignored` 1 failed exit 1; `m7_ended_jobs_absorbed` 1 failed
exit 1; `m8_bare_absorb_prints_help` 1 failed exit 1; `control_after` `11
passed` exit 0; every `restored byte-identical` line `True` (8 of 8) —
matching the block's table of 1/2/1/2/1/1/1/1 exactly. Then `git worktree
remove --force .remedy-wt/f263-r4-mut` (real exit 0), `git worktree
prune` (real exit 0); `git worktree list` after: primary checkout at
`ec4ee4bc` plus the three `.remedy-wt/job-*` worktrees only (`09441a92`,
`cc8696a3`, `03d435e5`) — no new worktree or branch left behind (R-0940).

## Authored-text proofs

- `.agent/authored/f263-r4-block.md` (C1a) == `.remedy-wt/f263-r4-block.md`: byte-identical True (15157 bytes, sha256 `f299d909e829501915e7d146540522cd878d3c1718df729f8441874beb678dee`).
- `.agent/authored/f263-r4-ledger.md` (C1a) == `.remedy-wt/f263-r4-payloads/ledger.md`: byte-identical True (2244 bytes).
- `.agent/authored/f263-r4-decisions.md` (C1a) == `.remedy-wt/f263-r4-payloads/decisions.md`: byte-identical True (3115 bytes).
- `.agent/authored/f263-r4-plan.md` (C1a) == `.remedy-wt/f263-r4-payloads/plan.md`: byte-identical True (1163 bytes).
- `.agent/authored/f263-r4-product.diff` (C1b) == `.remedy-wt/f263-r4-payloads/product.diff`: byte-identical True (9570 bytes).
- `.agent/authored/f263-r4-absorb_cmd.py` (C1b) == `.remedy-wt/f263-r4-payloads/absorb_cmd.py`: byte-identical True (4118 bytes).
- `.agent/authored/f263-r4-pins.diff` (C1b) == `.remedy-wt/f263-r4-payloads/pins.diff`: byte-identical True (3094 bytes).
- `.agent/authored/f263-r4-test_absorb_cmd.py` (C1c) == `.remedy-wt/f263-r4-payloads/test_absorb_cmd.py`: byte-identical True (6800 bytes).
- `.agent/authored/f263-r4-mutations.py` (C1c) == `.remedy-wt/f263-r4-payloads/mutations.py`: byte-identical True (2936 bytes).
- APPLIED text: `product.diff` and `pins.diff` were each `git apply
  --check`ed (exit 0) then `git apply`ed (exit 0) unedited, never
  retyped; G3's post-apply sha256 matches against the block's table are
  the disk-to-disk proof that the applied bytes equal the payload's
  bytes. `absorb_cmd.py` and `test_absorb_cmd.py` were copied whole via
  `shutil.copyfile` to their landing paths, then read back at C3 in G3 —
  both byte-identical to their payloads.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 284 insertions, matches block formula (211+73) |
| C1b | done | 348 insertions, matches block exactly |
| C1c | done | 248 insertions, matches block exactly |
| C2 | done | 41/2/8 insertions, matches block exactly; G2 fully passed |
| C3 | done | 20/2/98/3/39/22/167/6/2/1/3 insertions, matches block exactly; G3 fully passed |
| C4 | done | this handback |
| G1 | done | all readings match |
| G2 | done | all readings match; open-set 28 at base and at C2, both differences empty |
| G3 | done | all readings match |
| G4 | done | pytest 1738 passed, exit 0 (deviation from reviewer's 1694/2-skipped explained, not a red gate); ruff `All checks passed!` exit 0; integrity check all-pass exit 0 |
| G5 | done | mutations.py: 1/2/1/2/1/1/1/1 failures exit 1, controls 11 passed exit 0, all 8 restores byte-identical |
| T002 (`remedy absorb`) | done | command, catalog entry, help slot, bare form and pinned tests landed at C3; proved by G3 (bytes) and G5 (red proofs) |

## Deviations & assumptions

None from the block's ordered commit sequence: bytes verified before use,
the six-commit bundle landed in order C1a–C1b–C1c–C2–C3–C4, no payload
was edited or retyped, G1 through G5 all ran and every reading matched
the block's stated expectation. One reported-not-treated-as-deviation
note: G4's pytest count read `1738 passed` (0 skipped) against the
reviewer's disposable-worktree reading of `1694 passed, 2 skipped` —
expected, since the block's own G4 command includes
`tests/cli/test_golden_path.py` while the reviewer explicitly ran
"WITHOUT the golden path"; no failures in either reading, and the block
itself says "report what you read" rather than asserting the reviewer's
count would recur (the identical pattern occurred at round 3). No other
worktree, branch or stash was touched.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
4, then T003 — absorption at every safe point of a run and before every
apply, deleting the drift error it replaces. Open findings count: 28.
Operator-questions count: 0.
