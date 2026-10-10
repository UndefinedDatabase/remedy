# Handback — F205 round 3: book round 2, and the structural steps `remedy do` needs before it walks several projects

## Session

SESSION 1 of feature F205 · round 3 · rounds so far 3

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~30 % (claim, the record over several projects and the steps remedy do needs · the walk over several projects, the loop, the digest and API, the upkeep and the fixture mission open) — Schätzung

## Range

Review of `7f7b07914`..`8dd25dc0e` (5 commits on `feature/f205-multi-repo-missions` — C1
`b0eb913fb`, C2 `a4caa2c71`, C3 `6b9dd3786`, C4 `d1739e267`, C5 `8dd25dc0e` — plus this handback,
C6).

## Commits

### `b0eb913fb` F205 R3 C1: book round 2, a prose slip, DECISION F205 D3, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f205-r3.md` | 151/0 | NEW FILE — byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | appended `src/append-decisions.txt` — DECISION F205 D3 |
| `.agent/live_review.md` | 2/0 | appended `src/ledger-append.txt` — books F205 R2 PASS |
| `.agent/plan.md` | 14/13 | rewritten with `prep/c1/.agent/plan.md` — round 3's goal, current step and next steps |
| `.agent/prose_slips.md` | 1/0 | appended `src/prose-append.txt` — one round 2 prose slip |

### `a4caa2c71` F205 R3 C2: the walk's context and targets leave do_sequence.py (structure rule 2, DECISION F205 D3)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 6/1 | `do_sequence.py` boundary gains step (1); row 1477→1263 |
| `packages/orchestration/do_context.py` | 168/0 | NEW FILE — the shapes, step statuses, `DoStepResult`, `DoContext`, `_job_run_role_flags`, `do_stopped_walk_note`, moved unchanged |
| `packages/orchestration/do_sequence.py` | 42/256 | loses the moved names, imports both modules back by name |
| `packages/orchestration/do_targets.py` | 128/0 | NEW FILE — `_step_init`, `mission_plan_outlines`, `do_shape_of_plan`, `resolve_do_shape`, `_shape_job_orders`, moved unchanged |
| `tests/cli/test_client_interface.py` | 2/1 | reads `DoStepResult.to_json` from `do_context.py` |
| `tests/orchestration/import_reachability_allowlist.txt` | 2/0 | gains both new modules |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` 77604→77390 |

### `6b9dd3786` F205 R3 C3: the walk's cockpit and summaries leave do_sequence.py (structure rule 2, DECISION F205 D3)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 3/1 | boundary gains step (2); row 1263→1079 |
| `packages/orchestration/do_cockpit.py` | 115/0 | NEW FILE — the cockpit and `_step_ui`, moved unchanged |
| `packages/orchestration/do_sequence.py` | 42/226 | loses the moved names, imports both modules back by name |
| `packages/orchestration/do_summary.py` | 141/0 | NEW FILE — the contract and cost summaries, moved unchanged |
| `tests/cli/test_client_interface.py` | 2/1 | reads the cost tree from `do_summary.py` |
| `tests/orchestration/import_reachability_allowlist.txt` | 2/0 | gains both new modules |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` 77390→77206 |

### `d1739e267` F205 R3 C4: the walk's apply and push leave do_sequence.py (structure rule 2, DECISION F205 D3)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 2/1 | boundary gains step (3), "the file left the table"; row removed |
| `packages/orchestration/do_apply.py` | 188/0 | NEW FILE — the apply step, the waiting jobs' Next lines, the mission's one push, moved unchanged |
| `packages/orchestration/do_sequence.py` | 16/167 | loses the moved names, imports the module back by name; falls to 928 lines, below the 1,000-line limit |
| `tests/cli/test_client_interface.py` | 4/3 | reads the `landed` and `push` trees from `do_apply.py` |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | gains the new module |
| `tests/test_structure_ratchet.py` | 2/2 | `MAX_FILE_ROWS` 38→37, `MAX_FILE_LINES` 77206→76127 |

### `8dd25dc0e` F205 R3 C5: what remedy do reads before any step leaves do_cmd.py (structure rule 2, DECISION F205 D3)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | 13/88 | `_order_repo` and the order-file block (now `read_do_order`) leave; imports both back by name; falls to 1173 lines |
| `apps/cli/commands/do_order_input.py` | 131/0 | NEW FILE — `DoOrderInput`, `read_do_order` (the order-file block, unchanged apart from indentation) and `_order_repo`, moved unchanged |
| `docs/system/structure-ledger-v1.md` | 6/2 | gains the `do_cmd.py` bullet with step (1); file row 1248→1173, `_cmd_do` row 139→110 |
| `tests/cli/test_client_interface.py` | 2/2 | the order-file refusal site now named `apps.cli.commands.do_order_input:read_do_order` |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | gains the new module |
| `tests/test_structure_ratchet.py` | 2/2 | `MAX_FUNCTION_LINES` 31102→31073, `MAX_FILE_LINES` 76127→76052 |

### This commit — F205 R3 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f205-multi-repo-missions` — pending,
  reported in the worker's final reply only (runs after this commit, per the block's `THEN`).
- No `gh pr create`, no `gh pr list` run this round (the block's C0 did not order it; round 2 left
  no PR open and the Open PR Gate is deferred to the next round's `## Next`). No `claude` process
  started. No merge, no branch creation/move/deletion, no force-push, no stash entry touched, no
  worktree added or removed.

## Verification

**Opening verification** (one Python sha256/line-count reader, run as `python3 -I <path>`, before
the block was read whole): `block.md` sha256
`1e8e0421ea308f8cb885affb508832a10dafc63db939a65988c485ee8b23eaef`, 151 lines — both equal the
order's stated values.

**Gate 1** (`gate1_digests.py`, after C0 and before C1): every line of `digests.txt` (34 entries)
checked against the file it names — `ALL_TRUE`, all 34 `True`.

**C0 preconditions**: `git rev-parse HEAD` read `7f7b079147b5c9926d0cb22b9d86dabfda2b1986`, equal to
`origin/feature/f205-multi-repo-missions`; `git status --porcelain` empty; `.agent/STOP` absent.
No pull. `git branch --show-current` re-checked before every commit and read
`feature/f205-multi-repo-missions` each time.

**C1** (`c1_apply.py`, ran once; `c1_proof.py`, read-only): copied `block.md` to
`.agent/authored/f205-r3.md`, and the four `prep/c1/.agent/` files over their paths. Proofs: each
of the five copies byte-equal to its prepared file, `True` (5 of 5); and `live_review.md`,
`prose_slips.md`, `decisions.md` each equal `git show 7f7b07914:<path>` followed by its slice
(`ledger-append.txt`, `prose-append.txt`, `append-decisions.txt`), `True` (3 of 3) — 8 of 8 in all.
Self-review: the whole `git diff --cached` (239 lines) written to
`.remedy-wt/f205-r3-worker/c1_diff_cached.txt` and read whole — exactly the five ordered paths, one
new file, no unrelated edit. `git diff --cached --numstat` matched the table above. Committed as
`b0eb913fb`; `git show --numstat` matched.

**C2** (`c2_apply.py`, ran once; `c2_proof.py`, read-only): copied the seven prepared files over
their paths. Checked against the block's C2 section before committing: `do_context.py` holds the
shapes, the step statuses, `DoStepResult`, `DoContext`, `_job_run_role_flags` and
`do_stopped_walk_note` unchanged; `do_targets.py` holds `_step_init` with `mission_plan_outlines`,
`do_shape_of_plan`, `resolve_do_shape` and `_shape_job_orders` unchanged; `do_sequence.py` imports
every name back by name; the structure page gains the `do_sequence.py` bullet with step (1) and the
row falls 1477→1263; the reachability list gains both modules; `test_client_interface.py` reads
`DoStepResult.to_json` from `do_context.py`. All held and nothing more was found changed. Proofs:
all seven copied files byte-equal to their prepared file, `True` (7 of 7). `git diff --cached` (732
lines) written to `.remedy-wt/f205-r3-worker/c2_diff_cached.txt` and read whole — exactly the seven
ordered paths, two new files, no unrelated edit; 349 insertions, under the 500-line cap. Committed
as `a4caa2c71`; `git show --numstat` matched.

**C3** (`c3_apply.py`, ran once; `c3_proof.py`, read-only): copied the seven prepared files over
their paths. Checked: the cockpit with `_step_ui` and the contract/cost summaries move unchanged
and are imported back; the bullet gains step (2); the row falls again, 1263→1079;
`test_client_interface.py` reads the cost tree from `do_summary.py`. All held. Proofs: 7 of 7
`True`. `git diff --cached` (657 lines) written to `.remedy-wt/f205-r3-worker/c3_diff_cached.txt`
and read whole — exactly the seven ordered paths, two new files, no unrelated edit; 306 insertions.
Committed as `6b9dd3786`; `git show --numstat` matched.

**C4** (`c4_apply.py`, ran once; `c4_proof.py`, read-only): copied the six prepared files over
their paths. Checked: the apply step, the waiting jobs' Next lines and the mission's one push move
unchanged and are imported back; the bullet gains step (3); `do_sequence.py` falls to 928 lines and
its "Files above 1,000 lines" row is gone; `test_client_interface.py` reads the `landed` and `push`
trees from `do_apply.py`. All held. Proofs: 6 of 6 `True`. `git diff --cached` (471 lines) written
to `.remedy-wt/f205-r3-worker/c4_diff_cached.txt` and read whole — exactly the six ordered paths,
one new file, no unrelated edit; 213 insertions. Committed as `d1739e267`; `git show --numstat`
matched.

**C5** (`c5_apply.py`, ran once; `c5_proof.py`, read-only): copied the six prepared files over
their paths. Checked: `_order_repo` moves unchanged; the order-file block of `_cmd_do` becomes
`read_do_order`, body unchanged apart from indentation, answering a `DoOrderInput`; `_cmd_do` calls
it and keeps every later line; the page gains the `do_cmd.py` bullet and lowers the file's row
(1248→1173) and `_cmd_do`'s (139→110); `test_client_interface.py`'s order-file refusal site names
`apps.cli.commands.do_order_input:read_do_order`. All held. Proofs: 6 of 6 `True`. `git diff
--cached` (362 lines) written to `.remedy-wt/f205-r3-worker/c5_diff_cached.txt` and read whole —
exactly the six ordered paths, one new file, no unrelated edit; 155 insertions. Committed as
`8dd25dc0e`; `git show --numstat` matched.

**Gate 2** (after C5, `gate2.py`): `git status --porcelain` empty. The byte proofs of C1 to C5
re-run at this commit against `git show <commit>:<path>` for each commit's own paths, compared
against the prepared file each commit's own paths came from (so a path two later commits also
touched, e.g. `do_sequence.py`, is proven from the commit's own historical snapshot rather than the
now-further-edited working tree): 31 of 31 comparisons `True`.

**Gate 3** (`gate3.py`, run once, from the primary checkout):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f205-r3/selection.txt
```
exit 0; `5696 passed, 3 skipped in 536.47s (0:08:56)`, no FAILED or ERROR line. The three SKIPPED
lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252, pre-existing),
`tests/test_install_smoke.py:175` (install smoke is opt-in),
`tests/test_repair_context_reviewer_memory.py:257` (UI source not found).

**Gate 4** (`gate4.py`):
```
python3 -m ruff check packages/orchestration/do_sequence.py packages/orchestration/do_context.py packages/orchestration/do_targets.py packages/orchestration/do_cockpit.py packages/orchestration/do_summary.py packages/orchestration/do_apply.py apps/cli/commands/do_cmd.py apps/cli/commands/do_order_input.py tests/cli/test_client_interface.py tests/test_structure_ratchet.py
```
exit 0: `All checks passed!`.

**Gate 5** (`gate5.py`):
```
python3 -m apps.cli.main integrity check --json
```
exit 0: six checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`), `"fail_count": 0`, `"ok": true`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
exit 0: `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172',
'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235']` — matches the block's ordered
list exactly.

**No new line in this round's commits (`7f7b07914`..`8dd25dc0e`) carries `promot`** except the one
line inside `.agent/authored/f205-r3.md` quoting that very constraint — `.agent/` is outside
`tests/docs/test_retired_promote_word.py`'s scanned scope (`apps`, `packages`, `scripts`, `tests`,
`docs`, `README.md`), the same situation round 1 and round 2's saved block carried without a
finding.

**After the push** — reported in the worker's final reply only.

## Authored-text proofs

`.agent/authored/f205-r3.md` = `block.md`, sha256 and line count both equal, proven in C1 and
re-proven at the opening check. No other reviewer-authored free text was applied this round; every
C1 append and every C2–C5 path was applied by a plain byte copy or a bytes-append of a prepared
file and proven byte-equal against that file, not authored free text from the worker.

## Deviations & assumptions

None. C0 through C5 ran in the block's order, each copy script ran exactly once, every later proof
ran as a separate read-only script, every script ran as `python3 -I <absolute path>` with the
explicit working directory of `/home/decodeux/Repos/remedy`, no `cd`/`&&`/pipes/heredocs were used
in any shell call, gate 3 ran once as a saved script capturing pytest's own exit code with no extra
flags and no pipe, and gates 1, 2, 4 and 5 ran at the point and in the command the block orders.

## Round verdicts

Round 2's PASS is booked by C1 (appended into `.agent/live_review.md` as the "Gate: F205 R2" entry,
part of `src/ledger-append.txt`). Round 3's verdict is the reviewer's.

## For the operator, in plain sentences

This round changed no behaviour. It moved the parts of `remedy do` that the next round must change
into files of their own, because the size rule lets the two large files it came from only shrink.
The larger file is now below the size limit, and the other is smaller. Every test of `remedy do`
passes unchanged. The next round lets one order name several projects and run one job in each.
Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (the Open PR Gate).
3. Book round 3's verdict in the next round's first commit.
4. The order file names several projects; `remedy do` plans one job per repository and applies,
   commits and pushes each in its own repository.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions all confirmed; no pull; branch checked before every commit |
| Gate 1 | passed | 34 of 34 digest comparisons `True` |
| C1: book round 2, a prose slip, DECISION F205 D3, the plan, save the block | done | 8 of 8 byte proofs `True`; committed `b0eb913fb` |
| C2: the walk's context and targets leave do_sequence.py | done | 7 of 7 byte proofs `True`; properties re-checked against the block's C2 section; committed `a4caa2c71` |
| C3: the walk's cockpit and summaries leave do_sequence.py | done | 7 of 7 byte proofs `True`; properties re-checked against the block's C3 section; committed `6b9dd3786` |
| C4: the walk's apply and push leave do_sequence.py | done | 6 of 6 byte proofs `True`; `do_sequence.py` leaves the structure page; committed `d1739e267` |
| C5: what remedy do reads before any step leaves do_cmd.py | done | 6 of 6 byte proofs `True`; committed `8dd25dc0e` |
| Gate 2 | passed | status clean; 31 of 31 byte proofs re-run `True` |
| Gate 3 | passed | `5696 passed, 3 skipped` at exit 0, no FAILED/ERROR, run once as a saved script |
| Gate 4 | passed | ruff `All checks passed!`, exit 0 |
| Gate 5 | passed | integrity 6/6 `pass`, `fail_count 0`; open-findings list matches exactly |
| Push | pending | reported in the worker's final reply |
