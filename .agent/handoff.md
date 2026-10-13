# Handback — F306 round 3: book round 2 and R-1251's resolution, then T004 (`run_manifest.py`'s probes and workspace identity, split into their own module)

## Session

SESSION 1 of feature F306 · round 3 · rounds so far 3

Context self-assessment: C1 was mechanical bookkeeping (prepared-bytes copies, verified digest by
digest). C2 required working out, per the block's own stay/move rule, which of the eleven named
candidates could actually move: ten moved cleanly, but `_read_untracked_verified` had to stay on
`run_manifest.py` because its body raises the module's own `ManifestError` (used at ~187 other
sites), and the `GIT_*`/`UNAVAILABLE` vocabulary plus the `_READING_HELPER_ARGS` memo had to move
with their owning candidates and be imported back, since staying code reads them too; every gate
passed clean on the first run with no amendment needed.

Fortschritt: ~40 % (T001 to T004 landed · T005 to T008 open) — Schätzung

## Range

Review of `cf118420f`..`aac90077a`

## Commits

### 6276efb93 F306 R3 C1: book round 2 and R-1251's resolution, a prose slip, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r3.md` | +118/-0 | NEW FILE, byte copy of `block.md` (118 lines, sha256 `0f5544196c2132782d9e63bffb364fc253b8c1fdd88e04c377a1b080aedf8246`) |
| `.agent/live_review.md` | +4/-0 | round 2's PASS verdict and R-1251's RESOLVED entry appended, byte-identical to `append-live_review.txt` |
| `.agent/prose_slips.md` | +1/-0 | round 2's prose slip appended, byte-identical to `append-prose_slips.txt` |
| `.agent/plan.md` | +8/-6 | replaced by `dry-plan.md` |

### aac90077a F306 R3 C2: run_manifest's probes, workspace identity record and verified untracked read move to a module of their own (T004)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/workspace_identity.py` | +205/-0 | NEW FILE: `_run_probe`, `probe_provider_version`, `_remedy_repo_root`, `_is_sha`, `GIT_OK`/`GIT_UNAVAILABLE`/`GIT_INCOMPLETE`, `WorktreeIdentity`, `_HELPER_NEUTRALIZING_ARGS`/`_HELPER_CONFIG_PATTERN`, `_git_helper_env`, `_READING_HELPER_ARGS`, `_helper_neutralizing_args`, `UNAVAILABLE`, `_VERSION_PROBE_TIMEOUT_S`/`_VERSION_PROBE_MAX_CHARS`, and the four `_Untracked*` exception classes — every body byte-for-byte |
| `packages/orchestration/run_manifest.py` | +20/-180 | the moved bodies removed; one import block re-exports every moved name (`_run_probe as _run_probe` on its own statement, the only one ruff's unused-import rule needs the alias for); `_read_untracked_verified` stays (see Deviations) |
| `docs/system/structure-ledger-v1.md` | +5/-2 | `run_manifest.py` row 6558→6398; the ledger bullet gains its Step (1) sentence, reworded to say what actually stayed |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 74301→74141 (same 160-line fall) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.workspace_identity` added in its sorted place |

### (this commit) F306 R3 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- Push after C3: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8` — result in the session's final reply (with retry-on-500 up to three times per the block).
- No PR opened — the block does not ask for one.
- No worktree added or removed. No `gh pr merge` or `gh pr edit`. `gh pr list --state open ...` read `[]` before any branch work, so the Open PR Gate needed no action.

## Verification

Preconditions confirmed before C1: `git branch --show-current` read `feature/f306-findings-paydown-v8`; `git rev-parse HEAD` read `cf118420f7cb54dcd702fb348549e2d4c0020c91`; `git status --porcelain` was clean.

Every prepared-file digest matched before use (all seven, plus `block.md` itself): `block.md` (118 lines, `0f5544196c2132782d9e63bffb364fc253b8c1fdd88e04c377a1b080aedf8246`), `append-live_review.txt` (`873715465547b448a5364cca9d375ba3c56dc70a46c9d0d1904e70a2035f06fe`), `append-prose_slips.txt` (`e7aecb0af30f210deed42f8011e1017d1cdc80ab5d47d321fdcde6c76916b1a5`), `dry-plan.md` (`6cc4917c79f69a090d640c2fb7e779d2e0d4395f1265b40c05c7264b2a864741`), `verify.py` (`50ec84bc3af0f54eff36db55a4173295e913253308a13c96bb60df023febaf46`), `run_selection.py` (`cddebcc9b29665c95a90fb1b93184e421e0348d110823ea328a6ff2b003d712e`), `selection.txt` (`5e0e4e5597983805701cc3f3b50d059159e8f4635d504b8e57d54dc7ded3f141`), `check_reexport.py` (`977f78664e2d84f73d3350e6eb84e7d8a5e241237ff2927c07edfceac6bda8df`).

C1: before commit, `git diff --cached --numstat` read exactly `118 0 .agent/authored/f306-r3.md`, `4 0 .agent/live_review.md`, `8 6 .agent/plan.md`, `1 0 .agent/prose_slips.md` — matching the block's specification exactly. `cmp` of the authored copy against `block.md` printed nothing.

C2: before commit, `git diff --cached --numstat` read `5 2`, `20 180`, `205 0`, `1 0`, `1 1` across the five named paths — 232 insertions total (`git diff --cached --stat`: `5 files changed, 232 insertions(+), 183 deletions(-)`), under the 500-insertion cap. Self-review ran over `git diff --cached` before the commit: the `run_manifest.py` diff showed only the planned removals and the two import statements; the new module's diff showed only the moved bodies plus a docstring and the stdlib imports they need; no unrelated line moved. `python3 -m ruff check` on the three named files passed after one `--fix` round that reordered the new import block (isort's constant/class/function grouping) — no other change. `tests/test_structure_ratchet.py` and `tests/orchestration/test_import_reachability.py` run directly beforehand: 8 passed. `tests/orchestration/test_run_manifest.py`, `test_run_manifest_security.py`, `test_run_manifest_logical_identity.py` and `test_run_manifest_integrity.py` run directly beforehand: 99 passed. No leftover process after any run.

**Gate run (against C2, the only one — no amendment needed):**
- Gate 1: `git status --porcelain` empty; `verify.py` →
  ```
  found True F306 R3 C1: 6276efb93bc98ba6a4b7a182bc57afbd032fdf4e
  C1 parent is the base True
  equal at F306 R3 C1: True .agent/live_review.md
  equal at F306 R3 C1: True .agent/prose_slips.md
  equal at F306 R3 C1: True .agent/plan.md
  equal at F306 R3 C1: True .agent/authored/f306-r3.md
  F306 R3 C1: names exactly its paths True []
  ALL True
  ```
- Gate 2: `python3 -m ruff check packages/orchestration/run_manifest.py packages/orchestration/workspace_identity.py tests/test_structure_ratchet.py` → `All checks passed!`.
- Gate 3: `run_selection.py` → exit 0:
  ```
  SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
  SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
  SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
  130 paths
  4535 passed, 3 skipped in 74.66s (0:01:14)
  exit 0
  ```
  No FAILED/ERROR line, no "process(es) behind" line.
- Gate 4: `python3 -m apps.cli.main integrity check --json` → exit 0:
  ```
  {"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
  ```
- Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` → `['R-1235', 'R-1246', 'R-1252']`.
- Gate 6: `check_reexport.py` →
  ```
  defined in workspace_identity: 11 ['WorktreeIdentity', '_UntrackedMissing', '_UntrackedRace', '_UntrackedSpecial', '_UntrackedSymlink', '_git_helper_env', '_helper_neutralizing_args', '_is_sha', '_remedy_repo_root', '_run_probe', 'probe_provider_version']
  re-exported as the same object: True []
  workspace_identity imports run_manifest: False
  ALL True
  ```

## Authored-text proofs

- `.agent/authored/f306-r3.md` against `block.md`: byte-equal, 118 lines, sha256 `0f5544196c2132782d9e63bffb364fc253b8c1fdd88e04c377a1b080aedf8246` (`cmp` printed nothing; Gate 1's "equal at F306 R3 C1 True .agent/authored/f306-r3.md").
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (Gate 1).
- `.agent/prose_slips.md` against the base plus `append-prose_slips.txt`: byte-equal (Gate 1).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (Gate 1).

No other reviewer-authored text applied this round: C2 is this session's own code (a structural move the ledger's own text ordered), proved by the gates above and by the unchanged test suite rather than by digest comparison to a prepared file.

## Deviations & assumptions

- **The moved list is ten of eleven named candidates, not eleven.** The block named `_read_untracked_verified` among the candidates, but its own rule 2 — "a candidate STAYS when it calls, directly, a name that stays" — applies to it: its body raises `ManifestError` twice (`"unsafe untracked path"`, `"untracked file too large to hash"`) and passes `error_cls=ManifestError` to `secure_fs.open_verified_dir`, and `ManifestError` is `run_manifest.py`'s own general exception type at ~187 other sites, far outside this move's scope — not itself a candidate, and not something this step may relocate. So `_read_untracked_verified` stays on `run_manifest.py`, reworded into the ledger's bullet and the item-status table below. The four exception classes it raises still moved (none of them calls a staying name), and `run_manifest.py` imports them back so `_read_untracked_verified` and the staying `_read_worktree_identity` keep raising/catching them unchanged.
- **Shared constants moved with their owning candidates, not left behind.** `GIT_OK`/`GIT_UNAVAILABLE`/`GIT_INCOMPLETE` (read by the moving `WorktreeIdentity.from_json`) and `UNAVAILABLE` (read by the moving `_run_probe`/`probe_provider_version`) are also read by staying code (`_read_worktree_identity`, `inspect_contained_workspace_identity`, `_models_for_job`, and the validators past line 2500). Since the new module may never import `run_manifest` (gate 6), and the block's step 3 allows exactly this ("constants the moved code needs are imported... one definition each"), all four moved to `workspace_identity.py` and are imported back into `run_manifest.py` by name; every staying reference resolves unchanged. The same reasoning moved the `_READING_HELPER_ARGS` contextvar (read by the moving `_helper_neutralizing_args` and set/reset by the staying `worktree_identity`/`_read_worktree_identity`) and imported it back. `_VERSION_PROBE_TIMEOUT_S`, `_VERSION_PROBE_MAX_CHARS`, `_HELPER_NEUTRALIZING_ARGS` and `_HELPER_CONFIG_PATTERN` moved with no back-import, since nothing left on `run_manifest.py` reads them.
- **`.agent/decisions.md` not touched.** This reasoning is a meaningful implementation decision AGENTS.md would normally ask `.agent/decisions.md` to record, but the block's constraints say "No file outside the paths named per commit," and `decisions.md` is named for none of C1/C2/C3 this round. A draft entry was written, then reverted (`git checkout --`) before any commit, once the conflict was noticed; the reasoning is recorded here and in the item-status table instead, per the block's own step 2 ("report the final moved list and, for each candidate that stayed, the reason").
- **Commit trailer model name.** Every commit carries `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` — the model this session actually runs on — per the standing operator instruction, not a fixed name typed into the block.
- No extra commit beyond C1, C2, C3; no dropped one; no reordering.

## For the operator, in plain sentences

This round first recorded the previous round's acceptance and the resolution of one of the four
open problems. It then took the first of two steps a long-standing size rule owes on the file that
records what inputs a job's run actually used: the code that reads a provider's version, reads a
git worktree's exact content identity, and neutralizes a repository's own configured git helpers
before trusting a read of it, moved into a module of its own, with every existing caller and every
existing test still finding it under its old name. One of the originally-named pieces turned out to
depend on this file's own general error type closely enough that moving it would have broken the
rule that the new module may never import from the old one, so it was left in place instead, with
the reason written down; nothing it does changed. Every check this round ran — the structure-size
rule, the import-reachability guard, the full test selection, the health check and the re-export
guard — passed on the first attempt, with no repair round needed. Four more structural steps and
two findings remain open for later sessions. Nothing waits on the operator right now.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. The Open PR Gate (none expected — this feature stays on its own branch with no PR this round).
3. Book round 3's verdict in the next round's first commit.
4. T005: R-1252.

Operator questions open: 0.
Open findings: 3 (R-1235, R-1246 and R-1252), all owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `6276efb93` |
| C2 | done | `aac90077a` |
| C3 | done | this commit |
| Candidate: `_run_probe` | moved | no staying-name call; re-exported `as _run_probe` (otherwise unused on `run_manifest`) |
| Candidate: `probe_provider_version` | moved | no staying-name call; still called from `run_manifest.py`'s snapshot builder |
| Candidate: `_remedy_repo_root` | moved | no staying-name call; still called from the staying `remedy_worktree_identity` |
| Candidate: `_is_sha` | moved | no staying-name call; still called from several staying functions |
| Candidate: dataclass `WorktreeIdentity` | moved | its `GIT_UNAVAILABLE` default moved with it (see Deviations); still constructed from several staying functions |
| Candidate: `_git_helper_env` | moved | no staying-name call; still called from the staying `_git_bytes` |
| Candidate: `_helper_neutralizing_args` | moved | no staying-name call; its `_READING_HELPER_ARGS` memo moved with it (see Deviations); still called from the staying `_git_bytes` |
| Candidate: `_UntrackedRace` | moved | no staying-name call; still raised/caught by staying `_read_untracked_verified`/`_read_worktree_identity` |
| Candidate: `_UntrackedSymlink` | moved | no staying-name call; same as above |
| Candidate: `_UntrackedSpecial` | moved | no staying-name call; same as above |
| Candidate: `_UntrackedMissing` | moved | no staying-name call; same as above |
| Candidate: `_read_untracked_verified` | stayed | raises `run_manifest`'s own `ManifestError` directly (see Deviations) |
| Gate 1 | passed | `ALL True` |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | exit 0, `4535 passed, 3 skipped`, 130 paths, no FAILED/ERROR/"process(es) behind" |
| Gate 4 | passed | six checks pass, `fail_count` 0 |
| Gate 5 | passed | `['R-1235', 'R-1246', 'R-1252']` |
| Gate 6 | passed | `ALL True` |
| Push | pending at write time | runs after this commit; result in the session's final reply |
