# Handoff — F290 Findings paydown v6, round 1

## Session

SESSION 1 of feature F290 · round 1

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~15 % (T001 and T002 landed · T003 to T007 open) — Schätzung

## Range

Review of `31542dbfd`..`HEAD`: two commits on `feature/f290-findings-paydown-v6` and this handback
commit: `8d4606a9c`, `c03e2c374`, and this commit.

## Commits

### `8d4606a9c` F290 R1 C1: claim F290, book F200 R14, re-head the ledger, DECISION F290 D1 and the slice list

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f290-r1.md` | +148/-0 | NEW FILE at `.agent/authored/f290-r1.md`; byte-for-byte copy of this round's step block, verified against `.remedy-wt/f290-r1/block.md` before commit (`wc -l` 148, sha256 `9134bee3df0b75b6f9cc7beebe681a411623bc8ff28f1724e88f22b568b559ee`) |
| `docs/roadmap/STATUS.md` | +1/-1 | F290 claimed, `[ ]` to `[~]`; whole-file copy from `.remedy-wt/f290-r1/dry-STATUS.md`; byte comparison `True` |
| `.agent/live_review.md` | +21/-20 | re-headed from F200 to F290 (heading, paragraph, Steps section), plus the appended F200 R14 Gate entry (VERDICT PASS); whole-file copy from `.remedy-wt/f290-r1/dry-live_review.md`; append-byte-equality proof (pre-commit blob at `31542dbfd` plus `append-live_review.txt`'s bytes equals the post-append file from its `## Findings` heading) read `True True` |
| `.agent/decisions.md` | +12/-0 | bytes of `.remedy-wt/f290-r1/append-decisions.txt` appended without retyping (records DECISION F290 D1); pre-commit blob (`git show 31542dbfd:.agent/decisions.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/plan.md` | +18/-15 | whole-file copy from `.remedy-wt/f290-r1/dry-plan.md` for F290; byte comparison `True` |
| `.agent/context.md` | +10/-12 | whole-file copy from `.remedy-wt/f290-r1/dry-context.md` for F290; byte comparison `True` |
| `docs/roadmap/features/T2_F290.md` | +36/-0 | whole-file copy from `.remedy-wt/f290-r1/dry-T2_F290.md`; writes the "Task slicing" section (T001–T007) and one Acceptance line per id; byte comparison `True` |

`git diff --cached --numstat` before the commit read `148 0 .agent/authored/f290-r1.md`,
`10 12 .agent/context.md`, `12 0 .agent/decisions.md`, `21 20 .agent/live_review.md`,
`18 15 .agent/plan.md`, `1 1 docs/roadmap/STATUS.md`, `36 0 docs/roadmap/features/T2_F290.md` —
matching the block's stated numbers exactly. `git show --numstat 8d4606a9c` after the commit read
the same seven lines.

### `c03e2c374` F290 R1 C2: the preview test's nonce always passes the door, and the data-root allocator is read by its audit events (R-1128, R-1127)

| Path | +/- | Reason |
|---|---|---|
| `tests/ui_server/test_preview_end_to_end.py` | +1/-1 | R-1128: the command nonce now draws with `secrets.token_hex(8)` instead of `secrets.token_urlsafe(8)`; whole-file copy from `.remedy-wt/f290-r1/dry-test_preview_end_to_end.py`; byte comparison `True` |
| `tests/test_data_root_isolation.py` | +27/-0 | R-1127: adds the `_AUDIT` dict, the `_record_audit_event` hook and the new test `test_allocating_a_root_raises_no_audit_event_but_one_mkdir`, inserted directly above `test_a_cli_subprocess_inherits_the_isolated_root`; whole-file copy from `.remedy-wt/f290-r1/dry-test_data_root_isolation.py`; byte comparison `True` |

`git diff --cached --numstat` before the commit read `27 0 tests/test_data_root_isolation.py`,
`1 1 tests/ui_server/test_preview_end_to_end.py` — matching the block's stated numbers exactly.
`git diff --cached` showed only the one nonce-function-name line in the preview test, and in the
isolation test only the `_AUDIT` dictionary, the `_record_audit_event` hook and the new test —
nothing else moved; read as this round's self-review per the block's C2 instruction.

### this commit — F290 R1 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file, per `docs/agents/handback_template.md`; this commit |

## External actions

`git push -u origin feature/f290-findings-paydown-v6` runs after this commit; that outcome is
reported in the session's own reply, because it occurs after this file is written and committed.
No PR is opened this round (the block orders none). No worktree was added or removed by this
session's own commands; `git worktree list` read 12 lines (primary checkout plus
`.remedy-wt/f290-r1-dry`, the reviewer's own pre-existing dry tree at `31542dbfd`, plus ten
pre-existing `.remedy-wt/job-*` worktrees from earlier, unrelated jobs) — none of them touched by
this round's commands.

## Verification

**Gate 1** (after C2, before this handoff):
```
$ git status --porcelain
(empty)
```
Byte comparisons (Python `filecmp.cmp`), all `True`: `.agent/authored/f290-r1.md`,
`docs/roadmap/STATUS.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
`.agent/context.md`, `docs/roadmap/features/T2_F290.md`, `tests/ui_server/test_preview_end_to_end.py`,
`tests/test_data_root_isolation.py`, each against its prepared file under `.remedy-wt/f290-r1/`.
Exit 0.

**Gate 2**:
```
$ python3 -m ruff check tests/test_data_root_isolation.py tests/ui_server/test_preview_end_to_end.py
All checks passed!
```
Exit 0.

**Gate 3**:
```
$ python3 .remedy-wt/f290-r1/run_selection.py /home/decodeux/Repos/remedy
exit 0
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
7267 passed, 15 skipped, 1 warning in 100.11s (0:01:40)
```
Exit 0; matches the reviewer's dry-tree reading (`7267 passed, 15 skipped`) exactly, 15 SKIPPED
lines reported as they are, no FAILED, no ERROR, no `process(es) behind` line.

**Gate 4**:
```
$ python3 -m apps.cli.main integrity check --json
fail_count 0; six checks: handler_import pass, live_review_verdict pass, plan_consistency pass,
relevant_untracked pass, repo_root_hygiene pass, high_blockers_open pass
```
Exit 0.

**Gate 5**:
```
$ python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
['R-1117', 'R-1125', 'R-1127', 'R-1128', 'R-1129', 'R-1133', 'R-1137']
```
Exit 0; matches exactly.

**Gate 6**:
```
$ python3 -c "print(open('docs/roadmap/STATUS.md', encoding='utf-8').read().count('- [~] F290 — Findings paydown v6'))"
1
```
Exit 0; matches exactly.

## Authored-text proofs

`.agent/authored/f290-r1.md` (commit `8d4606a9c`): byte-for-byte copy of the step block given to
this round; `wc -l` read 148 lines, `sha256sum` read
`9134bee3df0b75b6f9cc7beebe681a411623bc8ff28f1724e88f22b568b559ee`, matching both the delivering
prompt's stated digest/line count and `block.md`'s own digest; byte comparison against `block.md`
read `True`.

`.agent/live_review.md` (commit `8d4606a9c`): whole-file copy from `dry-live_review.md`, byte
comparison `True`; the append-byte-equality proof (pre-commit blob at `31542dbfd` plus
`append-live_review.txt`'s bytes equals the post-append file from its `## Findings` heading to the
appended tail) read `True True`.

`.agent/decisions.md` (commit `8d4606a9c`): the append-byte-equality proof (pre-commit blob at
`31542dbfd` plus `append-decisions.txt`'s bytes equals the new file) read `True`.

`docs/roadmap/STATUS.md`, `.agent/plan.md`, `.agent/context.md`, `docs/roadmap/features/T2_F290.md`
(commit `8d4606a9c`): whole-file copies from `.remedy-wt/f290-r1/dry-STATUS.md`,
`dry-plan.md`, `dry-context.md` and `dry-T2_F290.md` respectively; byte comparisons all `True`.

`tests/ui_server/test_preview_end_to_end.py`, `tests/test_data_root_isolation.py` (commit
`c03e2c374`): whole-file copies from `.remedy-wt/f290-r1/dry-test_preview_end_to_end.py` and
`dry-test_data_root_isolation.py`; byte comparisons both `True`.

## Deviations & assumptions

None. Every gate ran exactly once, with its exit code captured inside the same `python3`/subprocess
call that ran it. The round's tracked path set is exactly the seven C1 paths plus the two C2 test
paths plus `.agent/handoff.md` — nothing else. No full suite ran this round (gate 3 was the round's
one test selection, the canary plus every `tests/test_*.py` file plus `tests/docs/` plus both
changed test files); no mutation red-proof ran; `REMEDY_TEST_MAX_WORKERS` was never set; no two test
commands ran at once; no `npm` command ran. No `Landed:`/`Done:` line was written anywhere — the
block reserves both resolutions for the reviewer to book in the next round. Nothing was merged, no
`main` checkout, no branch deletion, no force-push. `.agent/STOP` did not appear at any point in
this round. One sandbox-shape issue: an inline `python3 -c` script computing the ledger
append-equality proof was rejected by the shell sandbox (a newline followed by `#` inside a quoted
argument); per the block's own guidance this was moved into a `.py` file under
`.remedy-wt/f290-r1-worker/` and run from there — not a deviation from the block's content, only
from using an inline `-c` string for that one proof. This round's block names a specific commit
trailer, `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; both commits of this round
carry exactly that trailer, as ordered, rather than this session's own environment-default trailer.

## Next

1. Phase 1 rule 1 (`.agent/STOP`) — check first, in the next session.
2. Phase 1 rule 2, the Open PR Gate — no PR is open yet from this round (none was created, per the
   block); check for one before any new branch.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 1's verdict and the resolutions of R-1128 and R-1127 in the next round's first
   commit.
5. T003 and T004: the README's tier rows and the documentation index, each held by a test.

Operator questions open: 0.
Open findings: 7 (R-1117 Medium; R-1125, R-1127, R-1128, R-1129, R-1133, R-1137 Low; all owned by
F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Branch `feature/f290-findings-paydown-v6` from `main` at `31542dbfd` (C0) | done | HEAD confirmed `31542dbfd` before any write |
| NEW FILE `.agent/authored/f290-r1.md` (copy of `block.md`) | done | commit `8d4606a9c`; `wc -l` 148, sha256 matches, `cmp` silent |
| Claim F290 in `docs/roadmap/STATUS.md` (`[ ]` to `[~]`) | done | commit `8d4606a9c` |
| Re-head `.agent/live_review.md`, book F200 R14's Gate entry | done | commit `8d4606a9c`; append-byte-equality proof `True True` |
| DECISION F290 D1 in `.agent/decisions.md` | done | commit `8d4606a9c`; append-byte-equality proof `True` |
| Rewrite `.agent/plan.md` and `.agent/context.md` for F290 | done | commit `8d4606a9c` |
| Write the slice list and Acceptance lines in `docs/roadmap/features/T2_F290.md` | done | commit `8d4606a9c` |
| T001 (R-1128): preview test nonce via `secrets.token_hex(8)` | done | commit `c03e2c374` |
| T002 (R-1127): `test_allocating_a_root_raises_no_audit_event_but_one_mkdir` | done | commit `c03e2c374` |
| Gate 1 (status + 9 byte comparisons) | pass | all `True`, tree clean |
| Gate 2 (ruff) | pass | `All checks passed!` |
| Gate 3 (selection) | pass | `7267 passed, 15 skipped`, exit 0 |
| Gate 4 (integrity check) | pass | six checks pass, `fail_count` 0 |
| Gate 5 (open finding ids) | pass | matches exactly |
| Gate 6 (STATUS line count) | pass | `1` |
| Rewrite `.agent/handoff.md` | done | this file, this commit |
| Push after this commit | reported in reply | runs after this commit |
| PR create | skipped | block orders no PR this round |
