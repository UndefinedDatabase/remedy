# Handback — F302 round 1: claim, T001's inventory, DECISION F302 D1, and the claude CLI's command line's structural step

## Session

SESSION 1 of feature F302 · round 1 · rounds so far 1

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~15 % (claim, T001 and the command line's structural step · T002 to T004 open) — Schätzung

## Range

Review of `6689c581eea590da948c19026af35a937339575b`..`687342d7c5ad5647b034de7a74c7c447f3b24e8b`
(three commits on `feature/f302-claude-cli-tokens` — C1 `279c3cf7a`, C2 `f360fd4b2`, C3
`687342d7c` — plus this handback, C4).

## Commits

### `279c3cf7a` F302 R1 C1: save the round 1 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f302-r1.md` | 157/0 | NEW FILE — byte copy of `block.md` |

### `f360fd4b2` F302 R1 C2: claim F302, book F301 R11, T001's inventory, DECISION F302 D1, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/context.md` | 15/12 | replaced with `dry-context.md` |
| `.agent/decisions.md` | 10/0 | appended `append-decisions.txt` (DECISION F302 D1) |
| `.agent/f302_inventory.md` | 187/0 | NEW FILE — byte copy of `f302_inventory.md` (T001's inventory) |
| `.agent/live_review.md` | 18/17 | replaced with `dry-live_review.md` (re-heads at the F302 claim, books F301 R11 PASS) |
| `.agent/plan.md` | 17/12 | replaced with `dry-plan.md` |
| `docs/roadmap/STATUS.md` | 1/1 | replaced with `dry-STATUS.md` (F302's line becomes `[~]`) |
| `docs/roadmap/features/T3_F302.md` | 13/0 | replaced with `dry-T3_F302.md` (DECISION F302 D1 amendment) |

### `687342d7c` F302 R1 C3: the claude CLI's command line moves to claude_cli_command.py (structure rule 2, DECISION F302 D1)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 5/3 | replaced with `code-structure-ledger-v1.md` — boundary gains step (1), `MAX_FILE_LINES` pin falls |
| `packages/orchestration/claude_cli_command.py` | 73/0 | NEW FILE — replaced with `code-claude_cli_command.py`; holds `build_claude_cli_args` and its four constants, moved unchanged |
| `packages/orchestration/pingpong_provider.py` | 16/63 | replaced with `code-pingpong_provider.py` — loses the moved names and `import re`, gains the five-name import back |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | replaced with `code-import_reachability_allowlist.txt` — gains `packages.orchestration.claude_cli_command` |
| `tests/test_structure_ratchet.py` | 1/1 | replaced with `code-test_structure_ratchet.py` — `MAX_FILE_LINES` pin moves to 78945 |

### This commit — F302 R1 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push -u origin feature/f302-claude-cli-tokens` — runs once
  after this commit, per the block's THEN step; reported in the worker's final reply only.
- No other `gh` command ran this round beyond the C0 precondition check
  (`gh pr list --state open --json number`, read `[]` before any write). No merge, no branch
  creation beyond C0, no force-push, no stash touched. No pull request opened, per the block.

## Verification

**Pre-state** (before any write): `git rev-parse HEAD` read `6689c581eea590da948c19026af35a937339575b`;
`git status --porcelain` empty; `.agent/STOP` absent; `gh pr list --state open --json number` read
`[]`. Then `git -C /home/decodeux/Repos/remedy checkout -b feature/f302-claude-cli-tokens`, once.
`git branch --show-current` read `feature/f302-claude-cli-tokens` before every commit.

**Opening digest check** (block verification, before the block was read): `block.md` sha256
`f39d0d82154bfd0884326a32211525c4c4a474bbab790649c46f9bdab6d9fe97`, line count 157 — both equal the
harness's own stated values.

**Gate 1** (after C0, before C1 — every line of `digests.txt` against the file it names, one Python
script): 14 of 14 comparisons `True` — `block.md`, `f302_inventory.md`, `dry-STATUS.md`,
`dry-live_review.md`, `dry-T3_F302.md`, `dry-plan.md`, `dry-context.md`, `append-decisions.txt`,
`selection.txt`, `code-claude_cli_command.py`, `code-pingpong_provider.py`,
`code-structure-ledger-v1.md`, `code-test_structure_ratchet.py`,
`code-import_reachability_allowlist.txt`. `ALL_TRUE: True`.

**C1's byte proof** (before commit): `.agent/authored/f302-r1.md` read sha256
`f39d0d82154bfd0884326a32211525c4c4a474bbab790649c46f9bdab6d9fe97`, line count 157 — equal to
`block.md`'s own, `True`.

**C2's byte proofs** (before commit, one Python script): `.agent/decisions.md` equals
`git show 6689c581e:.agent/decisions.md` followed by the bytes of `append-decisions.txt`, `True`;
every one of the six copied files equals its prepared file, six of six `True`. The whole
`git diff --cached` (395 lines) was written to a worker file and read whole before commit; every
hunk matched the claim/booking/DECISION intent the block describes.

**C3's content checks** (read before commit, per the block's own list): `claude_cli_command.py`
holds the module docstring naming DECISION F302 D1, `import re`, then the four constants,
`_CLI_SESSION_REF_PATTERN`, `build_claude_cli_args` and the F005 comment, each confirmed byte-for-byte
identical to their text in `pingpong_provider.py` at `6689c581e` by a Python substring check (four
checks, `True`). `pingpong_provider.py` lost `import re` (confirmed absent) and those five names
(confirmed absent), and gained the two-line DECISION F302 D1 comment and the five-name import
immediately after the `call_identity` import (confirmed by direct read, lines 22-41). The structure
page's file row for `packages/orchestration/pingpong_provider.py` reads 1977 (confirmed:
`wc -l` on the file also reads 1977), and its boundary names the claude CLI's command line first
with "Step (1), done by F302". `MAX_FILE_LINES = 78945` in `tests/test_structure_ratchet.py`
(confirmed, was `78992` at `6689c581e`); `MAX_FUNCTION_ROWS`, `MAX_FUNCTION_LINES` and
`MAX_FILE_ROWS` unchanged (confirmed against the base file, all three identical). The reachability
list gains `packages.orchestration.claude_cli_command` directly after
`packages.orchestration.ci_stages` (confirmed, lines 114-115).

**C3's byte proofs** (before commit, one Python script): all five paths equal their prepared file,
five of five `True`.

**Gate 2** (after C3): `git -C /home/decodeux/Repos/remedy status --porcelain` empty, `True`. The
byte proofs of C2 step 2 and C3 step 3, re-run at this commit by a read-only Python script (twelve
comparisons: the C2 decisions-append proof, the six C2 copies, the five C3 copies): twelve of
twelve `True`. (One procedural slip during this gate is reported below under Deviations &
assumptions.)

**Gate 3** (the round's one test selection, run once):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f302-r1/selection.txt
```
Exit 0. `5226 passed, 3 skipped in 386.28s (0:06:26)`. No `FAILED` or `ERROR` line. The three
SKIPPED lines:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

**Gate 4** (one saved script, `subprocess.run`, printing the exit code):
```
python3 -m ruff check packages/orchestration/claude_cli_command.py packages/orchestration/pingpong_provider.py tests/test_structure_ratchet.py
```
Exit 0: `All checks passed!`

**Gate 5** (same approach, two `subprocess.run` calls):
```
python3 -m apps.cli.main integrity check --json
```
Exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=182", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
"no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
"pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
"pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six of six checks `pass`, `fail_count 0`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit 0:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176',
'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230']
```
Matches the block's ordered list exactly.

## Authored-text proofs

`.agent/authored/f302-r1.md` = `block.md` (sha256 and line count both equal). No other
reviewer-authored text (in the fidelity-protocol sense of a saved `src`/`code`/`dry` text applied
verbatim) carried a separate authored-text obligation beyond the byte proofs already run in C2 and
C3 above and reported there in full.

## Deviations & assumptions

- During Gate 2, the first script run to re-verify the C2 byte proofs was the same script that
  originally performed the C2 copy-and-append (`c2.py`), which re-appended the bytes of
  `append-decisions.txt` to `.agent/decisions.md` a second time, leaving the working tree with an
  uncommitted duplicate append (`git status --porcelain` showed ` M .agent/decisions.md`). This was
  caught immediately, before any commit or push; `.agent/decisions.md` was restored to its
  committed state with `git checkout HEAD -- .agent/decisions.md`, confirmed by `git status
  --porcelain` returning empty again, and Gate 2 was then re-run with a read-only proof script
  (`gate2_proofs.py`) that only reads and compares, performing no copy or append. No commit, push,
  or other file was affected by this slip; it cost one extra read-only pytest-free round-trip, no
  mutation of a committed file, and is recorded here per the block's instruction that any departure
  belongs in this section, however small.

Otherwise: None. C0 through C3 ran in the block's exact order, each exactly once; `git branch
--show-current` was checked before every commit and read `feature/f302-claude-cli-tokens` each
time; every copy, hash, run and proof ran inside a Python script under
`/home/decodeux/Repos/remedy/.remedy-wt/f302-r1-worker/`, each capturing its own command's exit
code in the same script; gate 3 was the round's only pytest invocation, run once, with no
`REMEDY_TEST_MAX_WORKERS` set and no `-n` passed; no provider call was made and `claude` was never
started; no mutation; no file under `.remedy-wt/f302-r1/` was modified; no file outside the round's
named path set was touched; no stash entry touched, no branch other than the one C0 created, nothing
merged, no force-push; `.agent/STOP` did not appear at any point; commit subjects carry no
leading-slash token and no absolute path; no shell call used `cd`, `&&`, `||`, `;`, a pipe,
`$(...)`, `${...}`, `$?`, a heredoc, `VAR=x cmd`, `export` or `cp` — every shell call was one plain
command, and every copy/hash/run/proof ran inside a Python script instead.

This section says nothing about this commit's own self-review, per the block; that is reported in
the worker's final reply only.

## Round verdicts

F301's round 11 PASS verdict is booked by C2 (carried forward into the re-headed
`.agent/live_review.md`). Round 1's verdict is the reviewer's, to be written after this handback.

## For the operator, in plain sentences

The previous feature, the mission's cleanup job, is merged into the main line after both of
GitHub's checks passed. The new feature makes the worker Remedy starts for each step spend fewer
tokens before it does any work. This round read every recorded call of that worker through
Remedy's own commands, 77 calls with all their figures, and found that a builder's first call
writes about 41,000 tokens into the cache and reads about 281,000 from it while the job reports
only about 1 in 100 of the tokens its calls move. It moved the part of the code that builds the
worker's command line into a file of its own without changing what it does, because the size rule
lets the old file only shrink. The next round measures, with at most twenty calls, which loaded
parts cost the most. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (Open PR Gate).
3. Book round 1's verdict in the next round's first commit.
4. T002: the attribution, one fixed task through Remedy's own provider path, at most twenty calls.

Operator questions open: 0.
Open findings: 15 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225 and R-1230, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions confirmed; `feature/f302-claude-cli-tokens` created from `6689c581e` |
| C1: save the round 1 block | done | byte proof `True`; committed `279c3cf7a` |
| C2: claim F302, book F301 R11, T001's inventory, DECISION F302 D1, the plan | done | byte proofs `True`, 7 of 7; committed `f360fd4b2` |
| C3: the claude CLI's command line moves to `claude_cli_command.py` | done | content checks and byte proofs `True`, 5 of 5; committed `687342d7c` |
| Gate 1 | passed | 14 of 14 digest comparisons `True` |
| Gate 2 | passed | status clean; 12 of 12 byte proofs `True` (one procedural slip during, corrected before any commit — see Deviations) |
| Gate 3 | passed | `5226 passed, 3 skipped`, exit 0; no FAILED/ERROR |
| Gate 4 | passed | ruff exit 0, all checks passed |
| Gate 5 | passed | six integrity checks `pass`, `fail_count 0`; open findings list matches exactly |
| Push | pending | reported in the worker's final reply |
