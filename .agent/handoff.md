# Handback — F151 round 10 (BLOCKED — gate 3 red, round stops before C3)

## Session

SESSION 2 of feature F151 · round 10 · rounds so far 10.

Context self-assessment: `digests.txt` was checked against the sha256 given in the prompt before
any file it lists was trusted, every file `digests.txt` and `manifest.tsv` list was checked against
its own digest before use, `block.md` was read in full before acting, and every number below (byte
sizes, numstats, gate readings, the rotation's whole output) was produced by running the thing, not
recalled. The session ends here because gate 3 came back red and the block forbids a second
invocation of its test selection to chase the cause further; the next session (or a continuation of
this one, once it is confirmed no other `remedy` process holds the shared data root) re-runs gate 3
exactly once and, on a clean result, finishes C3, the handoff, the push and the pull request exactly
as block.md already specifies — F151 is NOT closed and does not end in a fresh session yet.

Fortschritt: ~85 % (C1 and C2 done and pushed; C3's three files are written and byte-verified but
uncommitted; gates 1 and 2 passed; gate 3 is red; gates 4, 5, the handoff-proper, the push and the
pull request are not reached) — Schätzung.

## Item status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | `HEAD` read `5a10b48d6`, equalled `origin/feature/f151-worker-adapter-contract`, `git status --porcelain` was empty, `.agent/STOP` absent, `gh pr list` returned `[]` — all before any write |
| C1 | done | five prepared paths copied and proved byte-identical, staged numstat matched `manifest.tsv` exactly, committed as `363defdb5` |
| C2 | done | `scripts/rotate_live_review.py` run once via a `cwd`-scoped Python wrapper; exit code and every line but `written:` matched `sim-rotation.txt`; both ledger files proved byte-identical to their `c2-*` sources; committed as `8cba09943` |
| C3 step 1 (three files) | deviated | all three files copied into the working tree and proved byte-identical to their `c3-*` sources; **not committed**, because gate 3 (ordered before the handoff but after these files are in place) came back red |
| Gate 1 | done | `git status --porcelain` showed only the three C3 files modified; `verify.py` printed `True` on every line, `absent` for C3's committed check (as specified pre-commit), last line `ALL True` |
| Gate 2 | done | the prep folder's `status_line.txt` content (minus its trailing newline) occurs exactly once in `docs/roadmap/STATUS.md`, and no line of it begins `- [~]` |
| Gate 3 | **RED** | `python3 .remedy-wt/f151-r10/prep/gate3.py .` → `exit 1` (block requires `exit 0`); pytest line read `793 passed in 38.97s`, matching `sim-gate3.txt`'s passed count exactly, with no `FAILED`, `ERROR` or `SKIPPED` line; integrity sub-check read `integrity exit 0, "fail_count": 0`, matching the simulation |
| Gate 4 | skipped | not reached; gate 3 must pass first |
| Gate 5 | skipped | not reached; gate 3 must pass first |
| C3 step 3 (handoff bundled with the three files) | skipped | not reached; this document is a standalone blocked-handback instead, per the block's own red-gate rule |
| Push (C1/C2 only) | done | `git push origin feature/f151-worker-adapter-contract` succeeded on the first attempt after this handback's commit; no HTTP 500, no retry needed |
| Pull request | skipped | not created; the block forbids opening it when a gate is red |

## Why gate 3 read exit 1 with a matching passed count and no FAILED/ERROR/SKIPPED line

`tests/conftest.py`'s `pytest_sessionfinish` hook (`trylast=True`) can set
`session.exitstatus = pytest.ExitCode.TESTS_FAILED` in two cases that are each unrelated to any
test's own pass/fail state: a process left running inside this run's own temp folder (F293 T003,
`tests/load_governor.py`'s `leftover_processes`/`end_processes`), or an unexcused change to the
*configured data root* between the start and the end of the run (R-0803, `_data_root_fingerprint`/
`_data_root_guard_verdict`). Both notices are written through the terminal reporter (`red=True`),
never as a `FAILED`/`ERROR`/`SKIPPED`-prefixed line, which is exactly the set `gate3.py`'s own
filter greps for — so its three printed lines (`exit 1`, the passed-count line, and nothing from the
FAILED/ERROR/SKIPPED grep) are consistent with either guard tripping and do not by themselves say
which one, or say anything about F151's own code being at fault.

Circumstantial evidence pointed at the data-root guard rather than a leaked process: `ps aux` at the
time showed `remedy serve start` (pid 740108) running continuously since 2026-10-20 — a "foreign
supervisor" in `_foreign_supervisor_answers`'s own terms, since no test in this round's selection
starts one — and a separate, unrelated `python3 -m apps.cli.main do run --json --no-ui
--run-unattended -- order.md` process started the same afternoon as this round, plus several
`remedy-loop-runner` shell processes. `_data_root_guard_verdict` excuses a change only inside
`SUPERVISOR_OWN_CLASSES` (`api`, `serve`, `logs`, `projects`); a concurrent client doing real work
through that supervisor would write into `jobs`/`runs`, which is not excused, and would make this
run's data-root fingerprint differ at the end from the one taken at the start — without this run's
own tests having written anything.

This was not confirmed by re-running gate 3, because the block fixes it as "the round's one test
selection, run once." DECISION F151 D6 in `.agent/decisions.md` records the reasoning and the
instruction for the session that picks this back up.

## Range

Review of `5a10b48d6`..`HEAD` (`HEAD` is this handback's own commit).

## Commits

### `363defdb5` F151 R10 C1: book round 9, the Built State, save the round 10 block and the PR body

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r10.md` | +136/-0 (new) | byte copy of `block.md`, proved equal to it |
| `.agent/authored/f151-r10-pr_body.md` | +67/-0 (new) | byte copy of the prepared PR body |
| `.agent/live_review.md` | +2/-0 | round 9's `Gate: F151 R9` verdict booked |
| `.agent/plan.md` | +5/-4 | advanced to round 10, the closing round |
| `docs/roadmap/features/T8_F151.md` | +38/-0 | the Built State section added |

### `8cba09943` F151 R10 C2: rotate the finding ledger into its archive

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-42 | 7 gate records and 7 finding pairs (14 records) moved to the archive by `scripts/rotate_live_review.py` |
| `.agent/live_review_archive.md` | +42/-0 | the same 42 lines appended there |

### this commit — F151 R10 blocked handback (not C3; see Deviations)

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | rewritten | records the blocker and the exact next action |
| `.agent/decisions.md` | +1 entry (DECISION F151 D6) | records the red-gate reasoning and the reversal instruction |
| `.agent/handoff.md` | rewritten | this handback |

Not committed this round: `README.md`, `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json` —
written in the working tree and byte-verified against `c3-README.md`, `c3-docs__roadmap__STATUS.md`
and `c3-scripts__self_use_queue.json`, but held back because gate 3 (which the block orders before
the handoff) came back red. They remain modified, uncommitted, in the working tree exactly as
written; nothing needs to be re-copied to resume.

## External actions

- Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`,
  checked before any write.
- `git push origin feature/f151-worker-adapter-contract` → run once, after this handback's commit;
  outcome below.
- No worktree added or removed. No pull request created, none merged. No branch created, switched
  or deleted. No stash touched. No provider call.

## Verification

Interpreter: the repository's configured Python 3.

Gate 1 — `git status --porcelain` → `M README.md`, `M docs/roadmap/STATUS.md`,
`M scripts/self_use_queue.json` (exactly the three C3 files). `python3
.remedy-wt/f151-r10/prep/verify.py .` → 21 lines, every one `True` except the expected `absent\tC3
committed`, and the three `C3 working tree <path> equals c3-<name>` lines each `True`; last line
`ALL True`.

Gate 2 — `python3`-measured: the prep folder's `status_line.txt` content, minus its trailing
newline, occurs `1` time in `docs/roadmap/STATUS.md`; `begins with '- [~]': False`. `GATE2 PASS`.

Gate 3 — `python3 .remedy-wt/f151-r10/prep/gate3.py .` → `exit 1`; second line `793 passed in
38.97s`; no further FAILED/ERROR/SKIPPED line printed; `integrity exit 0 6 pass;
['{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}']`. `sim-gate3.txt`'s own
reading was `exit 0` / `793 passed in 72.61s (0:01:12)` / the same integrity line. The passed count
and the integrity line match; the exit code does not. **RED — run once, not repeated.**

Gate 4 — not reached (gate 3 must read `exit 0` first).

Gate 5 — not reached (gate 3 must read `exit 0` first).

## Authored-text proofs

C1's five paths and C2's two paths are reviewer-authored text applied this round. Each was copied
from its `c1-*`/`c2-*` file under `.remedy-wt/f151-r10/prep/` by a dedicated `python3` script under
`.remedy-wt/f151-r10-worker/` (`c1_copy.py`, `c2_rotate.py` for the rotation itself), each proved
byte-identical immediately before `git add` (`c1_verify_bytes.py`, `c2_verify_bytes.py`); all reads
`True`/`EQUAL`. C3's three paths were copied and proved byte-identical the same way
(`c3_copy.py`, `c3_verify_bytes.py`) but are not yet committed, so there is no committed
authored-text proof for them this round — only the working-tree one gate 1 already reports above.

## Deviations & assumptions

- **Gate 3 read red** (`exit 1` against the required `exit 0`), with the same passed count as the
  simulation and no FAILED/ERROR/SKIPPED line. Per the block's own rule ("If a gate goes red, STOP:
  commit and push what is verified, write an honest handoff, and hand back WITHOUT creating the pull
  request"), the round stops here. DECISION F151 D6 records the full reasoning, the circumstantial
  evidence pointing at a concurrent `remedy` process on this machine rather than a defect in F151's
  code, and why gate 3 was not re-run to confirm (the block's "run once" rule for that gate).
- C3's three files were written and byte-verified in the working tree (as block.md's C3 step 1
  orders) but are **not committed**, because the block orders the commit together with the handoff
  only after gates 1–5 all pass, and gate 3 did not.
- This handback is **not** the C3 commit block.md describes (it does not carry README.md,
  docs/roadmap/STATUS.md or scripts/self_use_queue.json), because those three files are not yet
  verified complete. It instead carries `.agent/plan.md`, `.agent/decisions.md` and
  `.agent/handoff.md` alone, which is the smallest honest commit that records the blocker.
- No pull request was created. No `gh pr merge`. No branch created, switched or deleted. No
  force-push. `git branch --show-current` was run as a standalone command before each commit and
  read `feature/f151-worker-adapter-contract` every time.
- No production or test file was edited. No provider call. No mutation, no worktree, no
  `REMEDY_TEST_MAX_WORKERS`, no `-n` flag — gate 3 ran exactly once, alone.

## For the operator, in plain sentences

The closing round booked the previous round's result, gave the feature file its finished-state
section, and moved the old finding records into the archive file — all three of those steps are
done, committed and pushed. The last step, accepting the feature in the project's status list and
opening the pull request, could not finish this round: one of the mandatory checks before that step
came back failed, and the reason looks like another program on this same computer was doing real
work at the same time rather than a problem with the feature itself, but that is not proven. Nothing
was lost: the files for the last step are already written and checked, waiting for the next attempt.
No pull request exists yet.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists (absent at the time of this handback).
2. Confirm no other `remedy` process (the `serve` daemon, a `do run`, a loop-runner) is actively
   using the shared data root, then run `python3 .remedy-wt/f151-r10/prep/gate3.py .` exactly once.
3. On a clean `exit 0` with `793 passed` and no FAILED/ERROR/SKIPPED line: run gates 4 and 5, then
   finish C3 — commit `README.md`, `docs/roadmap/STATUS.md` and `scripts/self_use_queue.json` with
   the handoff block.md's C3 step 3 describes, push, and open the pull request exactly as block.md's
   `THEN` clause orders. The Open PR Gate still merges it only in the session after that.
4. If gate 3 is genuinely red on a clean re-run, stop again and report it as a real defect; do not
   weaken or route around it.

Operator questions open: 0. Open findings (the set gate 3's own check reads): `R-1246`, `R-1281`,
`R-1326`, `R-1351`, `R-1353`, `R-1418`, `R-1421`, `R-1425`, `R-1426`, `R-1427`, `R-1428` (11), all
owned by F314.
