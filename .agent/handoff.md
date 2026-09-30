# Handoff — F293 Test load diet, round 3

## Session

SESSION 1 of feature F293 · round 3 · rounds so far 3

This session continues from round 2's own session (context remained comfortable through round 2;
no `.agent/prose_slips.md` line was written there). Round 3 was reviewer-authored in full (the
finding text, the fix design, the exact payload shape) and delegated as one worker round; it
required one substantive deviation from the authored block (below) discovered by reading the
production provider code directly rather than trusting the block's own proposed payload shape.
Self-assessment: three rounds of this feature have now each required deep reading of adjacent
production modules beyond what the round's own bundle named up front (round 2's cache module,
round 3's reviewer structured-output schema) — this is the kind of accumulating investigative load
self_drive_protocol.md's G7 names as a legitimate reason to end a session even short of the 6-8
round target. This handoff ends the session here rather than continuing into a 4th round.

## Range

Review of `1d0c46984`..`HEAD` — three commits on `feature/f293-test-load-diet`: `c953b9b8a`,
`0f6804827`, and this handback commit (not yet made at the time this line was drafted).

## Commits

### `c953b9b8a` F293 R3 C1: register and resolve R-1119 (real paid claude-cli calls in two tests)

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | R-1119 finding (registration paragraph + `Done:` paragraph) appended verbatim, one blank line after the prior last line (`Gate: F044 R15`), per the round's exact authored text |
| `.agent/plan.md` | +14/-14 | Current Step rewritten for round 3's result (full rewrite of the section per plan.md's own "rewrite, do not append" rule) |

`git show --numstat c953b9b8a`: `4 0 .agent/live_review.md`, `14 14 .agent/plan.md` — **18
insertions total**, well under the 500-line cap.

### `0f6804827` F293 R3 C2: mock the claude-cli subprocess seam in two provider-override tests

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_task_runner.py` | +53/-2 | new module-level helper `_install_fake_claude_cli(monkeypatch)` (after `_make_args`, line ~1234); both target tests gained a `monkeypatch` fixture parameter and a call to the helper as their first body line |

`git show --numstat 0f6804827`: `53 2 tests/orchestration/test_job_task_runner.py` — **53
insertions total**. `git diff` confirmed only the new helper function and the two tests' own
signature/first-line changed; no assertion in either test was touched.

### This handback commit — F293 R3 C3: verify the fix and handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | full rewrite | Current Step gains the round's measured verification result (timing, ps-proof) |
| `.agent/handoff.md` | full rewrite | this file |

## External actions

No `git worktree` used this round (no production code changed, so no mutation red-proof was
owed — AGENTS.md reserves those for production code, and this round's own Constraints said so
explicitly). `git worktree list` read 11 entries before and after this round, untouched (primary
checkout + 10 pre-existing `.remedy-wt/job-*` worktrees belonging to other running sessions on this
shared machine). One scratch file was written and removed within commit 3's own verification step:
`.remedy-wt/ps_proof_r1119.py` (the ps-polling script, item 2 below) — written, run, then deleted
before this handback commit; `git status --porcelain` was empty both before writing it and after
deleting it, and it was never staged. `git push origin feature/f293-test-load-diet` — run after
this handback commit; outcome reported in the session's own reply, not in this file. No PR created
this round — the worker does not create PRs. No `gh pr` commands.

## Verification

**Open PR Gate / state probe, before any work:**
```
$ git branch --show-current
feature/f293-test-load-diet
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
$ git status --short
(empty)
```

**`git grep` confirming the finding's own literal claim (before commit 1):**
```
$ git grep -n 'builder_provider="claude-cli"\|reviewer_provider="claude-cli"' tests/
```
Confirmed: exactly `tests/orchestration/test_job_task_runner.py:2187-2188` and `:2538-2539` among
all hits carry this pattern with no adjacent fake/mock in the same test (every other hit, in
`test_provider_evidence_integration.py` and `test_stream_evidence_integration.py`, is backed by a
fake `claude` binary on PATH or is a bare string passed to a dataclass constructor).

**Ruff, test file (commit 2, re-checked at commit 3):**
```
$ python3 -m ruff check tests/orchestration/test_job_task_runner.py
All checks passed!
```

**Both fixed tests, new timing:**
```
$ python3 -m pytest "tests/orchestration/test_job_task_runner.py::TestProviderOverrideToFake::test_cli_handler_provider_override" "tests/orchestration/test_job_task_runner.py::TestCommandPathExplicitOverrides::test_provider_override_to_fake" -v --durations=0
tests/orchestration/test_job_task_runner.py::TestProviderOverrideToFake::test_cli_handler_provider_override PASSED [ 50%]
tests/orchestration/test_job_task_runner.py::TestCommandPathExplicitOverrides::test_provider_override_to_fake PASSED [100%]
0.56s call     tests/orchestration/test_job_task_runner.py::TestProviderOverrideToFake::test_cli_handler_provider_override
0.52s call     tests/orchestration/test_job_task_runner.py::TestCommandPathExplicitOverrides::test_provider_override_to_fake
2 passed in 1.51s
```
Down from T001's 19.66s and 12.77s — both now under 0.6s.

**ps-proof, same method the reviewer used to find the defect (background subprocess, `ps -ef`
polled across the whole run):**
```
before claude -p pids: {'1203804'}
new claude -p pids seen during run: set()
test exit code: 0
. [100%]
1 passed in 0.75s
```
Pid `1203804` pre-existed (another session's real `claude -p` call on this shared machine, running
before this test even started) and is exactly the kind of unrelated hit the round's own
instructions said not to count. Zero NEW `claude -p` pids appeared during the test's run, polled at
0.1s/0.3s/0.5s/0.8s/1.2s intervals across the whole 0.75s duration.

**Whole file:**
```
$ grep -c 'def test_' tests/orchestration/test_job_task_runner.py
214
$ python3 -m pytest tests/orchestration/test_job_task_runner.py -q --durations=0
214 passed in 37.05s
```
214 passed matches the file's own `def test_` count exactly (same count the reviewer already
verified at round-3 authoring time). T001's own reading for this file was **89.92s**, but that
figure is the SUM of individual duration-lines under `-n auto` parallelism (a CPU-share
approximation, per `.agent/plan.md`'s own Risks note), not a serial wall-clock run; this round's
**37.05s** is a serial, non-parallel wall-clock run of the same file, so the two numbers are not on
the same basis and are not directly subtracted. What IS directly comparable and real: the two
target tests alone dropped from a summed 32.43s (19.66+12.77, T001's own duration-lines) to a
summed 1.08s (0.56+0.52) just now, in the same serial mode — a same-basis **~97% drop** for the
two tests this round targeted.

**Ruff clean (re-checked):**
```
$ python3 -m ruff check tests/orchestration/test_job_task_runner.py
All checks passed!
```

**Integrity check:**
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"message": "handlers=171", "name": "handler_import", "status": "pass"},
  {"message": "last Gate verdict PASS_WITH_RISKS", "name": "live_review_verdict", "status": "pass"},
  {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
  {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
  {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"},
  {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}
], "fail_count": 0, "ok": true, "passed": true}
```

**Canary:**
```
$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 50.39s
```

**No full suite run this round** (amend0917-throughput: exactly one full suite per feature; T001
already spent it; this is a test-only fix, not the closure's integration-gate round).

## Authored-text proofs

The R-1119 finding text (commit 1) was applied by exact text append (`.agent/live_review.md` grew
by exactly the appended bytes, one blank line before the new paragraph, confirmed by reading the
tail before and after and by the file ending in exactly one trailing newline both times). The
helper function and the two test edits (commit 2) follow the block's own named shape and location
(after `_make_args`, both tests gaining `monkeypatch` and a first-line call) but the FAKE PAYLOAD
BODY itself was NOT applied verbatim from the block — see Deviations below, this is the round's one
declared departure.

## Deviations & assumptions

1. **The block's proposed reviewer payload shape does not match this codebase's default reviewer
   path, and was corrected before running anything, per the round's own Constraints** ("if the fake
   response shape does not satisfy `ClaudeCliProvider.build()`/`.review()`'s parsing... read the
   actual parsing code... to find the real expected shape, adjust the fake payload to match it
   honestly, and declare the adjustment"). MEASURED by reading `packages/orchestration/
   pingpong_provider.py` and `packages/orchestration/structured_outputs.py` directly:
   `reviewer_structured_enabled()` returns True unless the environment variable
   `REMEDY_REVIEWER_FREETEXT` is set, which no fixture or test in this file sets, so
   `ClaudeCliProvider.review()`'s default path is `_call_reviewer_structured`, which sends
   `--json-schema` and parses the top-level `structured_output` object from the raw envelope
   (`packages/orchestration/token_actuals.py::parse_cli_envelope`) — NOT the legacy free-text
   `result` field the block's own payload proposed (`json.dumps({"verdict": ...})` inside
   `"result"`). The schema behind `structured_output`, `ReviewVerdict`
   (`packages/orchestration/schemas/models.py`), forbids extra fields (`ConfigDict(extra="forbid")`)
   and requires exactly `schema_v: "rv1"`, `verdict`, `findings`, `confidence`, `summary`. The
   shipped fake therefore builds two different envelope shapes: the builder role keeps a `"result"`
   free-text field (builder's own call path, `_call`/`_build_impl`, never sends `--json-schema` and
   parses `result` unconditionally — confirmed by reading `build_claude_cli_args` and `_call`), and
   the reviewer role gets a top-level `"structured_output"` object as described. This was VERIFIED,
   not assumed: both fixed tests passed on the first run after this correction (see Verification
   above), and the `--version` probe and builder-role path both still use the fixture's originally
   proposed shape unchanged. No test assertion was touched to make this work — only the fake's own
   internals.

No other deviations. Constraints honoured: only the four named paths were touched
(`.agent/live_review.md`, `.agent/plan.md`, `tests/orchestration/test_job_task_runner.py`,
`.agent/handoff.md`); no production code under `packages/` or `apps/` touched; no assertion in
either fixed test was weakened, deleted, or had its expected value changed (`git diff` confirms —
every `assert` line in both tests is byte-identical to before); every commit stayed under the
500-insertion cap (18, 53 changed/inserted lines respectively); no `REMEDY_TEST_MAX_WORKERS` set,
no custom `-n` passed at any point; no PR opened; `.agent/STOP` did not appear at any point in this
round.

## Open findings

**MEASURED, not assumed, per this round's own instruction to state the mechanical count precisely**
("every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line"): running the repository's own
canonical function, `scripts.rotate_live_review.open_finding_ids`, against `.agent/live_review.md`
at this round's HEAD reads **2 open ids: `R-1117`, `R-1118`**. `R-1119` (this round's own finding)
nets to zero at every point after commit 1, since its registration and its `Done:` line landed in
the same commit.

**This does NOT match round 2's handback or this file's own re-head header** (both state 8 open
ids: `R-0413`, `R-0441`, `R-0471`, `R-0533`, `R-0632`, `R-0672`, `R-1117`, `R-1118`). Measured
cause: the six extra ids each appear in the CURRENT `.agent/live_review.md` only as a
`Recurrence: R-xxxx — ...` paragraph (their ORIGINAL `- R-xxxx — ` registration paragraphs were
already moved to `.agent/live_review_archive.md` when each was first resolved, confirmed by `grep`
— e.g. `Done: R-0413` at `.agent/live_review_archive.md:2552`), and the canonical function's own
regex, `^- (R-\d{4}) — `, does not match a line beginning `Recurrence:`. I ran the function fresh,
against the file as it stands right now, rather than trusting either the header's carried-forward
claim or round 2's restatement of it — this is a genuine discrepancy in how this repository's own
ledger arithmetic is carried across a re-head, and it is exactly the class of defect this same
ledger has registered against itself before (`R-0632`, `R-0441`, both visible a few lines above
R-1119 in the current file). I have NOT resolved it: it is outside this round's four-path scope and
outside this round's ordered work, so I am reporting the measurement plainly rather than picking
whichever number looked expected.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| R-1119 registered verbatim | done | commit 1, one blank line before, file ends in one trailing newline |
| `.agent/plan.md` Current Step advanced (commit 1) | done | rewritten, kept under 50 lines |
| R-1119 resolved (`Done:` paragraph, same round) | done | commit 1, same commit as registration |
| Fix implemented in both tests | done | commit 2; `_install_fake_claude_cli` helper + `monkeypatch` param + one call line in each test; no assertion touched |
| Ruff clean | done | `All checks passed!`, re-checked at commit 3 |
| Both tests pass with new timing | done | 0.56s / 0.52s, down from 19.66s / 12.77s |
| ps-proof of no real subprocess | done | zero new `claude -p` pids across the whole 0.75s run, polled 5 times |
| Whole-file green | done | 214 passed, matches `def test_` count exactly |
| Canary green | done | 42 passed |
| Integrity check green | done | `fail_count: 0` |
| `.agent/plan.md` updated (commit 3) | done | measured result (timing, ps-proof) added to Current Step |
| Deviation declared (payload shape) | done | see Deviations section; verified by both tests passing, not assumed |

## Next

T002 continued: more cuts from `.agent/f293_inventory.md` sections 2-3's remaining top entries
(`test_supervisor_portability.py`, `test_mission_cmd.py`, `test_do_sequence_cli.py`, and the rest of
the top-30 ranking), each with its own mutation red-proof where production code changes, until
either the ranking is exhausted of easy wins or a dated DECISION rules no more can be cut without
weakening a test. The 40%-of-1246.09 Acceptance check itself is read at the closure sequence's
integration-gate round, per DECISION F293 D1 — not inside any T002 round. The open-findings
discrepancy above (2 vs. 8) is unresolved and worth a session's first action to rule on — either by
DECISION explaining why `Recurrence:` paragraphs count as open despite the function's own regex, or
by correcting the header's carried claim — before the next round states an open count of its own.
