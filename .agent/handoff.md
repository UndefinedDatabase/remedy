# Handoff — F290 Findings paydown v6, round 8 landed clean

## Session

SESSION 4 of feature F290 · round 8 · rounds so far 8

Context self-assessment: context is comfortable; round 8 ran its full ordered sequence — C1, C2
(landing the closure's self-use item `SU-044` exactly as the job wrote it, before the closure's one
full suite), all five gates and C3 — with every gate green, so this handback carries the block's
success-path content in full rather than a stop.

Fortschritt: ~88 % (all seven findings resolved and hardened; the self-use item run and landed; the
suite, the evidence and the pull request open) — Schätzung

## Range

Review of `3a5aba4e9`..`HEAD`: two commits on `feature/f290-findings-paydown-v6`, `500eebd93` and
`004f97870`, and this handback commit.

## Commits

### `500eebd93` F290 R8 C1: book round 7, record DECISION F290 D4

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f290-r8.md` | +107/-0 | NEW FILE; byte-for-byte copy of this round's step block `.remedy-wt/f290-s8/block.md` (`wc -l` 107, sha256 `b0ad4e33868986685b10fbf77e76dd06b1798d06aad6bd13f61e6635a28276e8`); byte comparison against the source read equal |
| `.agent/decisions.md` | +12/-0 | appended DECISION F290 D4 ("the closure's self-use item SU-044 lands"); whole-file copy from `.remedy-wt/f290-s8/dry-decisions.md`; append-byte-equality proof (`git show 3a5aba4e9:.agent/decisions.md` bytes + `append-decisions.txt` bytes == new file, compared with Python `==` over bytes) read `True` |
| `.agent/live_review.md` | +2/-0 | appended the F290 R7 Gate entry (VERDICT PASS, the closure's self-use item run to its approval gate, never applied); whole-file copy from `.remedy-wt/f290-s8/dry-live_review.md`; append-byte-equality proof read `True` |
| `.agent/plan.md` | +7/-9 | whole-file copy from `.remedy-wt/f290-s8/dry-plan.md`, advancing Current Step/Next Steps to round 8 (land `SU-044` as the job wrote it, before the closure's one full suite) |

`git diff --cached --numstat` before the commit read `107 0` for the new block file, `12 0` for
`.agent/decisions.md`, `2 0` for `.agent/live_review.md` and `7 9` for `.agent/plan.md` — matching
the block's stated numbers exactly. `git show --numstat 500eebd93` after the commit read the same
four lines.

### `004f97870` F290 R8 C2: the live-UI probe of dev status catches the two errors it can meet (SU-044)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/dev.py` | +1/-1 | narrows the live-UI probe's excused handler at line 140 from `(ImportError, Exception)` (with its `# noqa: BLE001` mark) to `(ImportError, AttributeError)`; the job's own change (`.agent/selfuse_f290/job_diff.txt`), copied from `dry-dev.py` |
| `tests/regression/test_named_bugs.py` | +64/-0 | two new tests in `TestDevStatusCommandSchema` pinning `remedy dev status --json` through the two errors the narrowed handler can meet, and confirming an unrelated error (`RuntimeError`) is no longer swallowed; copied from `dry-test_named_bugs.py` |
| `tests/test_ble001_ratchet.py` | +1/-1 | `MAX_EXCUSED` lowered from 286 to 285; the job's own change, copied from `dry-test_ble001_ratchet.py` |

`git diff --cached --numstat` before the commit read `1 1` for `apps/cli/commands/dev.py`, `64 0`
for `tests/regression/test_named_bugs.py` and `1 1` for `tests/test_ble001_ratchet.py` — matching
the block's stated numbers exactly. `git show --numstat 004f97870` after the commit read the same
three lines. The change to `apps/cli/commands/dev.py` and `tests/test_ble001_ratchet.py` was
confirmed as the job's own: a Python byte equality of `git diff --cached -- apps/cli/commands/dev.py
tests/test_ble001_ratchet.py` against everything after the first line of
`.agent/selfuse_f290/job_diff.txt` read `True`.

### this commit — F290 R8 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; documents round 8 landing clean through C1, C2 (landing `SU-044`) and all five gates |

## External actions

- This commit is pushed with `git push origin feature/f290-findings-paydown-v6` immediately after
  it is made.
- No worktree add/remove issued this round; the reviewer's prepared files were read from the
  existing `.remedy-wt/f290-s8/` directory. Scratch helper files were written under
  `.remedy-wt/f290-r8-worker/` (gitignored, newly created this round).
- No pull request was checked, opened, or merged this round: the block names no such step and
  forbids opening one.

## Verification

Gates run once each, after C2 and before C3, in the block's order.

Gate 1 — `git status --porcelain`, then a byte comparison of the seven committed files against
their prepared files:

    $ git status --porcelain
    (no output)

    $ python3 gate1_cmp.py
    .agent/authored/f290-r8.md vs block.md : SILENT(equal)
    .agent/live_review.md vs dry-live_review.md : SILENT(equal)
    .agent/decisions.md vs dry-decisions.md : SILENT(equal)
    .agent/plan.md vs dry-plan.md : SILENT(equal)
    apps/cli/commands/dev.py vs dry-dev.py : SILENT(equal)
    tests/regression/test_named_bugs.py vs dry-test_named_bugs.py : SILENT(equal)
    tests/test_ble001_ratchet.py vs dry-test_ble001_ratchet.py : SILENT(equal)
    ALL_OK: True

Gate 1: GREEN.

Gate 2 — `python3 /home/decodeux/Repos/remedy/.remedy-wt/f290-s8/run_selection.py
/home/decodeux/Repos/remedy`:

    exit 0
    SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). ...
    SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
    SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
    SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): ... (same reason)
    SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): ... (same reason)
    SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): ... (same reason)
    SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): ... (same reason)
    SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): ... (same reason)
    SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
    4358 passed, 9 skipped in 50.70s

Gate 2: GREEN — no FAILED or ERROR line, no "process(es) behind" line; `4358 passed, 9 skipped`
matches the reviewer's dry-tree reading exactly. Run once, not re-run.

Gate 3 — `python3 /home/decodeux/Repos/remedy/.remedy-wt/f290-s4/run.py /home/decodeux/Repos/remedy 3
python3 -m ruff check apps/cli/commands/dev.py tests/regression/test_named_bugs.py
tests/test_ble001_ratchet.py`:

    All checks passed!
    exit 0

Gate 3: GREEN.

Gate 4 — `python3 -m apps.cli.main integrity check --json`, from the primary checkout:

    exit 0
    {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}

Gate 4: GREEN — `fail_count` 0.

Gate 5 — `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:

    exit 0
    ['R-1138']

Gate 5: GREEN — matches the required `['R-1138']` exactly.

## Authored-text proofs

- `.agent/authored/f290-r8.md` vs `.remedy-wt/f290-s8/block.md`: byte comparison equal; `wc -l` 107,
  sha256 `b0ad4e33868986685b10fbf77e76dd06b1798d06aad6bd13f61e6635a28276e8` on both readings (the
  prompt-delivered digest and the post-copy re-measurement).
- `.agent/live_review.md` vs `dry-live_review.md`: byte comparison equal; sha256
  `9bdb700d807a6d8a873f6032d6ea6a8f73ae6ef67a86f7a8c2d9e3c005ae07de`. Append-byte-equality proof
  (base bytes at `3a5aba4e9` plus `append-live_review.txt` bytes equals the new file, compared with
  Python `==` over bytes) read `True`.
- `.agent/decisions.md` vs `dry-decisions.md`: byte comparison equal; sha256
  `b4df17b11fb5b573f96057f78e431466ceb58f7a5a0bf99329953cafc904b5aa`. Append-byte-equality proof
  (base bytes at `3a5aba4e9` plus `append-decisions.txt` bytes equals the new file) read `True`.
- `.agent/plan.md` vs `dry-plan.md`: byte comparison equal; sha256
  `b597bba9b18c549721eeebdc0dcdcfff395ca573c409c6e1a4b5a709f612f5ea` (whole-file copy, no append
  proof applicable).
- `apps/cli/commands/dev.py` vs `dry-dev.py`: byte comparison equal; sha256
  `f70070fa74f867dbab467642efae1e5ab1bc5ac130e8724c208460ed5716fe51`; confirmed as the job's own
  change jointly with `tests/test_ble001_ratchet.py` below by the byte-equality proof against
  `.agent/selfuse_f290/job_diff.txt` (everything after its first line equals `git diff --cached` of
  the two files, read `True`).
- `tests/regression/test_named_bugs.py` vs `dry-test_named_bugs.py`: byte comparison equal; sha256
  `4ffc015936d03cf733a771d4c82b0f45de35139f630e339eee016ca65b250d99`.
- `tests/test_ble001_ratchet.py` vs `dry-test_ble001_ratchet.py`: byte comparison equal; sha256
  `2c651e2e889f2aba430d7382d23a93abda1555633563586bd16c9a7f0df549c7`; confirmed as the job's own
  change jointly with `apps/cli/commands/dev.py` above.
- Gate 1's seven-way re-check (above) confirms all seven committed files still match their prepared
  files bit-for-bit after both commits.

## Deviations & assumptions

1. This session's auto-attached working directory was again a separate location (a disposable
   reviewer worktree under `.remedy-wt/`), unrelated to this round's work. It was never read from or
   written to: every command in this round ran against `/home/decodeux/Repos/remedy` directly, by
   absolute path or `git -C`. Recorded as an operating assumption, consistent with prior rounds.
2. For every git command this round the shell's working directory was first moved to the primary
   checkout with `cd` and the git command was then issued with an explicit `git -C
   /home/decodeux/Repos/remedy` argument naming the same path (e.g. `cd /home/decodeux/Repos/remedy
   && git -C /home/decodeux/Repos/remedy commit ...`) — a `cd`+`&&`+`git -C` compound. The block
   warns the sandbox "refuses some shell shapes" including "cd before a git command" and "compound
   commands"; this shape nonetheless executed without rejection every time it was used (`status`,
   `add`, `commit`, `show --numstat`). No git command was ever run relying on a bare `cd` alone, so
   the path each git command actually operated on was always pinned explicitly via `-C`. Recorded
   here because it is the kind of reading a later auditor should be able to find, not because it
   changed any result.
3. The round's first helper script (`verify_block.py`, for the initial sha256/line-count check) was
   first attempted via a shell heredoc (`cat > ... <<'EOF' ... EOF`); the sandbox silently swallowed
   it — no file was created, and the following `python3` invocation reported a parser error —
   rather than visibly rejecting the shape. Recovered by writing the same script with the Write tool
   instead, consistent with the block's own anticipation that "the sandbox refuses many shell
   shapes." Every scratch script after that point was written with the Write tool, never a heredoc.
4. The non-git gates (the pytest selection, the ruff check via `run.py`, the integrity check and the
   `rotate_live_review` import) were run either via their own `python3` script with the repo path
   passed as an argument, or with a plain `cd` to the primary checkout, since the block's
   shell-shape warning concerns commands immediately preceding a `git` invocation, not these.
5. The Session line above states `SESSION 4 of feature F290 · round 8 · rounds so far 8`, in full
   per the mandatory format `docs/agents/handback_template.md` and `AGENTS.md` prescribe (operator
   amendment amend0827-process-diet, rule 6), continuing round 7's handback's reading of 7 "rounds
   so far"; the block's own prose names only `SESSION 4 of feature F290 · round 8`, which this
   reading treats as the block naming the session/round content rather than overriding the
   mandatory trailing field.
6. No other deviation from the block's ordered commit sequence (C1, C2, five gates, C3) or from its
   stated paths, numbers, or gate commands. Exactly three commits landed, matching "one records
   commit, one code commit, one handback commit" (SLOW MODE).

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate).
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 8's verdict in the next round's first commit.
5. The integration gate: the one full suite and its CPU reading.

Operator questions open: 1.
Open findings: 1 (R-1138 Low, owned by the next paydown).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 7, record DECISION F290 D4 | done | commit `500eebd93`; numstat matched the block's stated numbers exactly |
| C2: the live-UI probe of dev status catches the two errors it can meet (SU-044) | done | commit `004f97870`; numstat matched exactly; job_diff byte-equality proof read `True` |
| Gate 1 (status + seven-way byte comparison) | done, GREEN | all seven comparisons silent/equal |
| Gate 2 (pytest selection) | done, GREEN | `4358 passed, 9 skipped`, matching the reviewer's dry-tree reading |
| Gate 3 (ruff check) | done, GREEN | `All checks passed!` |
| Gate 4 (integrity check) | done, GREEN | `fail_count` 0 |
| Gate 5 (`open_finding_ids`) | done, GREEN | `['R-1138']` |
| C3: handback | done | this commit |
| Push | pending | `git push origin feature/f290-findings-paydown-v6` runs immediately after this commit |
