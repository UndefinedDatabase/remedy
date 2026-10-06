# Handoff — F295 session 1, round 2: book round 1, land T001 (the order file)

## Session

SESSION 1 of feature F295 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~25 % (T001 landed, its review pending · T002 to T004 open) — Schätzung.

## Range

Review of `2e37c7aec`..`54b23b790`.

## Commits

### ed5210e8b F295 R2 C1: book round 1, DECISION F295 D2, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r2.md` | 178/0 (new) | byte copy of the round 2 block |
| `.agent/decisions.md` | 10/0 | append `DECISION F295 D2` — the order-file rule, header format, the constraints clause, precedence over the flags, the five refusals and the module split |
| `.agent/live_review.md` | 2/0 | append the F295 R1 gate entry (VERDICT PASS) |
| `.agent/plan.md` | 10/9 | rewrite to round 2's current step: land T001 as DECISION F295 D2 rules it |

### d209c2ac8 F295 R2 C2: remedy do reads an order file (T001, DECISION F295 D2)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | 1/1 | `do.run`'s `goal` ArgDef help becomes "What you ask, as text, or one path ending in .md to an order file" (carries the vocabulary page's `order file` and `what you ask` fragments for the word "Order") |
| `apps/cli/commands/do_cmd.py` | 28/0 | `_cmd_do`'s first statement block: an argument naming a `.md` file is read with `read_order_file`; an `OrderFileError` exits 2; a file and no `--max-cost-usd` carrying no `max-cost-usd` header exits 2 as `order_file_no_cost_cap`; otherwise `goal`, `project`, `contract` and `max_cost_usd` are merged from the file, each only where the parameter was `None` |
| `packages/orchestration/order_file.py` | 175/0 (new) | the order-file module: `order_argument_names_file`, `parse_order_file_text`, `read_order_file`, `OrderFile`, `OrderFileError` — the file-vs-text rule, the header/order split, every refusal |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | add `packages.orchestration.order_file`, in sorted position between `orchestrator_move_schema` and `ownership` |

### 54b23b790 F295 R2 C3: tests for the order file (T001)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_do_order_file.py` | 243/0 (new) | the eleven CLI scenarios through `apps.cli.grouped.main`, the `test_do_flags.py` fixture shape |
| `tests/orchestration/test_order_file.py` | 180/0 (new) | pure unit tests of the module: the file/text rule, every header key, the repeated-constraint text build, each `order_file_invalid_header` cause with its line number, `order_file_empty`, the byte-order mark, and the `read_order_file` I/O refusals |

### F295 R2 C4: handback (self-reference exception — committed by this same write)

| Path | Reason |
|---|---|
| `.agent/handoff.md` | this file, rewritten in full per `AGENTS.md` and `docs/agents/handback_template.md`, as round 2's handback |

## External actions

None. No `gh` command, PR action or worktree operation was needed this round; the branch already
tracked `origin` at the round's base commit and the Open PR Gate was last satisfied in round 1
(pull request 310 merged, confirmed `[]`). The push after this C4 commit is reported in the
worker's final reply, not here (write-once rule; this file is written before that push).

## Verification — the five gates, run once each, after C3's commit and before C4's commit

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty, exit 0. Then a script compared
   the four C1 files (`.agent/authored/f295-r2.md`, `.agent/live_review.md`,
   `.agent/decisions.md`, `.agent/plan.md`) against their matching prepared file (`block.md` for
   the block copy, the matching `dry-*` file otherwise) with `filecmp.cmp(..., shallow=False)` —
   all four `True`; printed `ALL EQUAL: True`.

2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r2/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check packages/orchestration/order_file.py apps/cli/commands/do_cmd.py
   apps/cli/command_catalog.py tests/orchestration/test_order_file.py tests/cli/test_do_order_file.py`
   → `exit 0`; `All checks passed!`.

3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r2/run_selection.py /home/decodeux/Repos/remedy`
   → `exit 0`. No `FAILED` or `ERROR` line, no `process(es) behind` line. Three `SKIPPED` lines
   printed, the same three round 1 read:
   - `tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.`
   - `tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access`
   - `tests/test_repair_context_reviewer_memory.py:257: UI source not found`
   Summary line: `5868 passed, 3 skipped in 104.68s (0:01:44)`. (This selection also walks every
   `tests/test_*.py` file at the tree root plus `tests/cli/`, `tests/docs/` and the six named
   `tests/orchestration/` files named in `selection.txt`, so its count is larger than round 1's
   narrower selection.)

4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r2/run.py /home/decodeux/Repos/remedy 3 python3 -m apps.cli.main integrity check --json`
   → `exit 0`; JSON tail:
   `{"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}`

5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r2/run.py /home/decodeux/Repos/remedy 3 python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   → `exit 0`; `['R-1138', 'R-1139']`.

## Authored-text proofs

- `.remedy-wt/f295-r2/block.md` → `.agent/authored/f295-r2.md`: `wc -l` 178/178, sha256
  `61fb8e1fa9d44d6bf05f74f0582a7d58e4b090693245c6425b6cd8ac7adfab7f`/same, byte comparison equal
  (`cmp` prints nothing / `filecmp.cmp` `True`).
- Each `dry-*` file copied verbatim over its path (`dry-live_review.md` → `.agent/live_review.md`,
  `dry-decisions.md` → `.agent/decisions.md`, `dry-plan.md` → `.agent/plan.md`): every pair's byte
  comparison read `True`.
- Proof (a): `.agent/live_review.md` equals `git show 2e37c7aec:.agent/live_review.md` followed by
  the bytes of `append-live_review.txt` — Python equality printed `True`.
- Proof (b): `.agent/decisions.md` equals `git show 2e37c7aec:.agent/decisions.md` followed by the
  bytes of `append-decisions.txt` — Python equality printed `True`.
- `git diff --cached --numstat` before the C1 commit read exactly the four lines the block named
  (`178 0`, `10 0`, `2 0`, `10 9`, matched by path above under Commits), confirming the base had
  not moved.
- All five prepared-file hashes in the block (`dry-live_review.md`, `dry-decisions.md`,
  `dry-plan.md`, `append-live_review.txt`, `append-decisions.txt`) were verified against the
  block's stated sha256 digests before use — all five `OK`.

## Deviations & assumptions

None against the block's ordered sequence (C1 with its four steps, the five gates, C2, C3, C4) or
its constraints. The two new test files were run standalone while writing them (23 and 11 passed
respectively), exactly as the block's constraints section permits; the five gates above are the
one recorded run of everything else.

## State

- Branch: `feature/f295-machine-client-contract-v1`, base `2e37c7aec` (confirmed equal to
  `origin`'s tip and to `HEAD` before any write).
- Head after C3: `54b23b790`.
- Head after C4: this handback's own commit, built on `54b23b790`; a commit cannot state its own
  hash inside its own content, so the exact SHA is left to the worker's final reply.
- Fortschritt: ~25 % (T001 landed, its review pending · T002 to T004 open) — Schätzung.

## For the operator, in plain sentences

Remedy can now take its work order from a file, the way Luna will hand it over; the file must say
how much money the work may cost at most, or Remedy refuses it before doing anything; a missing,
empty or broken file is refused the same way; ordinary typed orders behave exactly as before.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if present, write the handoff and stop; nothing here creates
   that file.
2. Otherwise Phase 1 rule 2 — the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 2's verdict in the next round's first commit.
5. T002: the digest in `remedy status --json`.

Operator questions open: 0.
Open findings: 2 (R-1138 and R-1139, both Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 step 1 (block copy + proofs) | done | `wc -l` 178/178, sha256 equal, cmp equal |
| C1 step 2 (dry-* copies) | done | all 3 pairs cmp equal |
| C1 step 3 (two byte-equality proofs) | done | proof (a) `True`, proof (b) `True` |
| C1 step 4 (numstat check + self-review) | done | `git diff --cached --numstat` matched the block exactly; diff read clean |
| C1 commit | done | `ed5210e8b` |
| C2: `packages/orchestration/order_file.py` | done | `order_argument_names_file`, `parse_order_file_text`, `read_order_file`, `OrderFile`, `OrderFileError`, all per DECISION F295 D2 |
| C2: `_cmd_do` order-file block | done | reads the file first, refuses before any step, merges into the existing flow |
| C2: `command_catalog.py` help text | done | carries the vocabulary page's Order meaning fragments |
| C2: import-reachability allowlist | done | `packages.orchestration.order_file` inserted in sorted position |
| C2 commit | done | `d209c2ac8` |
| C3: `tests/orchestration/test_order_file.py` | done | 23 tests, all passed standalone |
| C3: `tests/cli/test_do_order_file.py` | done | 11 tests, all passed standalone |
| C3 commit | done | `54b23b790` |
| Gate 1 (status + cmp proofs) | done | porcelain empty, all 4 files equal |
| Gate 2 (ruff) | done | `All checks passed!`, exit 0 |
| Gate 3 (selection suite) | done | `5868 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | `fail_count: 0`, exit 0 |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139']`, exit 0 |
| C4 handback commit | done | this file |
| Push after C4 | pending | runs immediately after this commit, reported in the worker's final reply |
