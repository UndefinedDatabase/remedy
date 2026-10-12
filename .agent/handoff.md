# Handback — F058 round 3: book round 2 (PASS), repair R-1259 and R-1260, two structural steps,
and the rest of T002 — the disclosure in the run's record and the line in the run report

## Session

SESSION 2 of feature F058 · round 3 · rounds so far 3

Context self-assessment: this round verified the block's digest and line count, every prep
file's digest and the gate-3 helpers' digests before any write; byte-copied the five `dry-*`/block
targets for C1; repaired both round-2 findings (two tests, one docstring sentence); completed both
structural moves with the ledger rows and `MAX_FILE_LINES` re-measured the same way the block
names; landed the disclosure key, the report line and the three test files for T002's rest; hit
one red gate 3 after a real mistake (an incomplete re-export dropped at C4) and repaired it in one
commit without growing the structure ledger.

Fortschritt: ~60 % (T001 and T002 landed · T003, the documentation page and the closure open) —
Schätzung

## Range

Review of `356c05709`..HEAD.

## Commits

### 1d466f067 F058 R3 C1: book round 2 (PASS, R-1259 and R-1260; R-1257 and R-1258 resolved), DECISION F058 D3

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f058-r3.md` | +225/-0 | NEW FILE, byte copy of `block.md` (225 lines, sha256 `212f05e4113bdcb16630c923f356919a513ae8be21e3a97ec220aafbfa701c30`, matching both the delivering prompt and `wc -l`/`sha256sum`) |
| `.agent/decisions.md` | +12/-0 | DECISION F058 D3 appended, byte copy of `dry-decisions.md` |
| `.agent/live_review.md` | +10/-0 | round 2's `Gate: F058 R2` entry, R-1259, R-1260 and the two `Done:` resolutions appended, byte copy of `dry-live_review.md` |
| `.agent/plan.md` | +12/-13 | rewritten for round 3, byte copy of `dry-plan.md` |
| `.agent/prose_slips.md` | +1/-0 | one prose-slip line appended, byte copy of `dry-prose_slips.md` |

### e98522615 F058 R3 C2: repair R-1259 and R-1260 (the walk's two missing tests, the factory's docstring)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/role_provider_factory.py` | +5/-2 | `create_role_provider`'s docstring sentence about `make_provider` rewritten to name the shim `_create_provider_with_cwd` and why it passes `create_provider` |
| `tests/orchestration/test_model_failover.py` | +17/-0 | `TestIsFailoverTrigger` gains two False-case tests (an HTTP 504 timeout, an exit-1-with-connection-refused), both reading as unavailable too; `TestFailoverProviderWalk` gains a `supports_resume is False` test over a primary that answers `False` |

### 4c1772656 F058 R3 C3: a call's own fields in the run record move to pingpong_call_record.py (structural, DECISION F058 D3)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_call_record.py` | +36/-0 | NEW FILE: `_add_exit_detail` and `_session_fields` moved byte-unchanged out of `pingpong_loop.py` |
| `packages/orchestration/pingpong_loop.py` | +1/-27 | both functions removed; import added in sorted place; file shrinks 5272 → 5246 (−26) |
| `docs/system/structure-ledger-v1.md` | +3/-2 | `pingpong_loop.py` boundary bullet gains Step (2); file row `5272` → `5246` |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` `74625` → `74599` (falls by 26) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.pingpong_call_record` added in sorted place |

### 9e0bb0c41 F058 R3 C4: the run handlers move to run_report_cmd.py (structural, DECISION F058 D3)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/run_report_cmd.py` | +161/-0 | NEW FILE: `_cmd_run_show`, `_cmd_run_list`, `_print_text_report` moved byte-unchanged out of `do_cmd.py` |
| `apps/cli/commands/do_cmd.py` | +7/-154 | the three functions removed; `_cmd_run_list`/`_cmd_run_show` imported back by name (incomplete — see the fix commit below); module docstring's last sentence rewritten; file shrinks 1173 → 1026 (−147) |
| `docs/system/structure-ledger-v1.md` | +5/-4 | `do_cmd.py` boundary bullet reordered (`run` handlers before `job` handlers) and gains Step (2); file row `1173` → `1026` |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` `74599` → `74452` (falls by 147) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `apps.cli.commands.run_report_cmd` added in sorted place |

### d1bc82e43 F058 R3 C5: a failed-over call's disclosure in the run record and the line in run show (T002, DECISION F058 D3)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_call_record.py` | +10/-1 | `_session_fields` gains the `"failover"` key when `out.failover_disclosure` is a real `FailoverDisclosure`; docstring sentence added |
| `packages/orchestration/model_failover.py` | +46/-0 | `failover_report_line(run_record)` added, with its WHY comment and a Public API line |
| `apps/cli/commands/run_report_cmd.py` | +5/-0 | `_print_text_report` prints `failover_report_line(data)` directly after the Builder/Reviewer lines, when not `None` |

### 0d183dfd8 F058 R3 C6: the disclosure's, the report line's and the run fixtures' tests (T002)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_pingpong_call_record.py` | +44/-0 | NEW FILE: `_session_fields` without a disclosure, with a real one, and with a non-disclosure attribute |
| `tests/cli/test_run_report_cmd.py` | +125/-0 | NEW FILE: `_cmd_run_show` prints the failover line once after `Reviewer:` for a served and a ran-out run, prints no `Failover:` line for a no-chain run, and carries the round's `failover` entry in `json_output=True` for both the served and the ran-out run |
| `tests/orchestration/test_model_failover.py` | +135/-0 | `TestFailoverReportLine` (five named cases) and `TestFailoverThroughARealRun` (the three real-`run_pingpong` scenarios (a)/(b)/(c)) |

### 63cabe0ff F058 R3 fix: re-export _print_text_report from do_cmd (gate 3 red at C4)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | +1/-1 | `_print_text_report` added to the re-export line (with a `# noqa: F401`), beside `_cmd_run_list`/`_cmd_run_show` — `tests/cli/test_task_input.py` imports it directly from `do_cmd` and gate 3 found that red; line count is unchanged (1026), so no ledger update follows |

## External actions

No pull request opened this round (the block forbids it; `gh pr list --state open --json number`
read `[]` before C1 and no new PR was created). No `git worktree add`/`remove` performed. The
worker's scratch directory `.remedy-wt/f058-r3-worker/` (gitignored) holds every copy/digest/gate
script and output this round used; it is not pushed. The push that follows this commit is reported
in the final reply only, not here, because the handoff is written before that command runs.

## Verification

**Preconditions (before C1):** `git branch --show-current` read `feature/f058-model-failover-chain`;
`git rev-parse HEAD` read `356c05709...`; `git status --porcelain` empty; `gh pr list --state open
--json number,headRefName,baseRefName,isDraft` read `[]`.

**Block and prep digests (before any write):** `block.md` sha256
`212f05e4113bdcb16630c923f356919a513ae8be21e3a97ec220aafbfa701c30`, 225 lines — both equal to the
values given in the delivering prompt. `dry-live_review.md`, `dry-decisions.md`,
`dry-prose_slips.md`, `dry-plan.md`, `run_selection.py` and `selection.txt` all sha256-checked
against the digests the block and the prompt named; all matched. Each `dry-*` file's diff against
its live counterpart was also read in full and matched the Bundle's description of what it adds.

**C1:** the five `dry-*`/block targets were written; `filecmp.cmp(..., shallow=False)` read `True`
for all five pairs. `git diff --cached --numstat` read exactly the Bundle's five pairs (`225 0`,
`12 0`, `10 0`, `12 13`, `1 0`). Commit `1d466f067`.

**C2:** two new tests added to `TestIsFailoverTrigger` (HTTP 504 and exit-1-with-connection-refused,
both already excluded by the existing timeout/exit branches — the repair is the test, not the
production code); one new test added to `TestFailoverProviderWalk` for `supports_resume is False`;
`role_provider_factory.py`'s docstring sentence rewritten. `ruff check` on both files: `All checks
passed!`. `python3 -I -c "import ast; ast.parse(...)"` on both: no error. Commit `e98522615`.

**C3:** `pingpong_call_record.py` written with `_add_exit_detail` and `_session_fields`, confirmed
byte-identical to the removed originals (diff showed only their removal and an import line added,
nothing inside either function body). `wc -l packages/orchestration/pingpong_loop.py`: `5246` (was
`5272`, −26). `python3 -m apps.cli.main integrity structure --json` confirmed the new file's size;
a script summed the ledger's "Files above 1,000 lines" table to `74599`, matching the new
`MAX_FILE_LINES` pin exactly. `ruff check` on the three touched production/test files: `All checks
passed!`. Commit `4c1772656`.

**C4:** `run_report_cmd.py` written with `_cmd_run_show`, `_cmd_run_list`, `_print_text_report`,
confirmed byte-identical to the removed originals via a script that sliced the exact source lines
before deleting them. `wc -l apps/cli/commands/do_cmd.py`: `1026` (was `1173`, −147). The ledger sum
script read `74452`, matching the new pin. Searched `tests/` for `_cmd_run_show`, `_cmd_run_list`,
`_print_text_report` and `"run.show"`/`"run.list"`: four files found
(`tests/test_command_catalog.py`, `tests/cli/test_job_refusal_envelope.py`,
`tests/cli/test_cli_ux.py`, `tests/cli/test_task_input.py`); none states a module path as a fact
in prose — all either import the names (which keep working through the re-export) or reference
`do_cmd.py` only as the file an AST-based refusal-site scanner reads (unaffected by the move) — so
none was edited at this commit. `python3 -m pytest tests/orchestration/test_import_reachability.py
-q` (the block's one permitted run after C4): `3 passed`. `ruff check` on the five touched files:
`All checks passed!`. Commit `9e0bb0c41`. **This commit's re-export was incomplete — see the fix
commit below, found by gate 3.**

**C5:** `_session_fields` gained the `"failover"` key (guarded by `isinstance(..., FailoverDisclosure)`);
`failover_report_line` added to `model_failover.py` with the exact sentence set the block specifies;
`_print_text_report` prints it after the Builder/Reviewer lines. `grep -il "promot"` on all three
touched files: no match. `ruff check` on all three: `All checks passed!`. Commit `d1bc82e43`.

**C6:** three test files written/extended per the block's exact named assertions. `ruff check` on
all three: `All checks passed!`. No test run performed between C5 and gate 3 (not one of the two
permitted runs). Commit `0d183dfd8`.

**Gates (after C6, before C7) — first pass:**

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. PASS.
2. `python3 -m ruff check packages/orchestration/model_failover.py
   packages/orchestration/role_provider_factory.py packages/orchestration/pingpong_call_record.py
   packages/orchestration/pingpong_loop.py apps/cli/commands/run_report_cmd.py
   apps/cli/commands/do_cmd.py tests/orchestration/test_model_failover.py
   tests/orchestration/test_pingpong_call_record.py tests/cli/test_run_report_cmd.py
   tests/test_structure_ratchet.py` → `All checks passed!`. PASS.
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f058-r3/prep/run_selection.py
   /home/decodeux/Repos/remedy` → **exit 1**. `1 failed, 4974 passed, 3 skipped in 41.28s`.
   `FAILED tests/cli/test_task_input.py::TestRunReportRendering::test_worker_self_report_separated`
   — it imports `_print_text_report` directly from `apps.cli.commands.do_cmd`, which C4 had
   stopped re-exporting. RED. Per the block's own clause: fixed with one new commit (below) and
   gate 3 re-run.
4. Not run this pass (gate 3 was red; the block's remaining gates were not evaluated until gate 3
   was green).
5. Not run this pass.
6. Not run this pass.

**The fix:** `apps/cli/commands/do_cmd.py`'s re-export line extended to also name
`_print_text_report`, with `# noqa: F401` since nothing inside `do_cmd.py` itself calls it. Written
first as a four-line parenthesized import (which grew `do_cmd.py` from 1026 to 1030 lines and
would have required a ledger/pin update that the ratchet rule frowns on for an upward move);
rewritten on one line instead, landing `do_cmd.py` back at exactly 1026 lines — the same row and
pin C4 already set, so no ledger change was needed. `ruff check apps/cli/commands/do_cmd.py`: `All
checks passed!`. Committed as `F058 R3 fix: re-export _print_text_report from do_cmd (gate 3 red at
C4)`, amended once in place (not yet pushed) to replace the four-line form with the one-line form
before the gates were re-run. Final SHA `63cabe0ff`.

**Gates (after the fix) — second pass, all six:**

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. PASS.
2. Same ruff command as above → `All checks passed!`. PASS.
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f058-r3/prep/run_selection.py
   /home/decodeux/Repos/remedy` → exit 0. Summary: `4975 passed, 3 skipped in 44.14s`. SKIPPED
   lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252); `tests/test_install_smoke.py:175`
   (opt-in, needs `REMEDY_INSTALL_SMOKE=1`); `tests/test_repair_context_reviewer_memory.py:257`
   ("UI source not found"). No FAILED, no ERROR, no `absent in tree:`, no `process(es) behind`
   line. PASS.
4. `python3 -m apps.cli.main integrity check --json` → `{"check_count": 6, "fail_count": 0, "ok":
   true, "passed": true, ...}`. PASS.
5. `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   → `['R-1235', 'R-1246', 'R-1251', 'R-1252', 'R-1259', 'R-1260']`, exact match. PASS.
6. `git -C /home/decodeux/Repos/remedy log --format=%s 356c05709..HEAD` → the C1-C6 subjects plus
   the fix commit's subject, newest first (the fix commit sits on top of C6 in the range, as the
   block's own red-gate clause anticipates). PASS.

## Authored-text proofs

1. `block.md` → `.agent/authored/f058-r3.md` (C1): byte-equal, `filecmp.cmp(shallow=False)` read
   `True`; sha256 `212f05e4113bdcb16630c923f356919a513ae8be21e3a97ec220aafbfa701c30` matches the
   delivering prompt.
2. `dry-live_review.md` → `.agent/live_review.md` (C1): byte-equal.
3. `dry-decisions.md` → `.agent/decisions.md` (C1): byte-equal.
4. `dry-prose_slips.md` → `.agent/prose_slips.md` (C1): byte-equal.
5. `dry-plan.md` → `.agent/plan.md` (C1, before this handback's own later rewrite): byte-equal.

Nothing else this round is reviewer-authored text copied verbatim: C2-C6's code, tests, docstrings
and ledger prose are the worker's own, built from the block's prose and byte-level specification,
not copied from a prepared file.

## Deviations & assumptions

1. **Gate 3 red after C6, one fix commit.** C4's re-export of the moved `run` handlers back into
   `apps/cli/commands/do_cmd.py` named only `_cmd_run_list` and `_cmd_run_show` — `_print_text_report`
   was dropped because `ruff` flagged it as unused inside `do_cmd.py` itself. This was a real
   mistake: the block's own C4 text says all three are "imported back by name... so
   `COMMAND_HANDLERS` and every test that imports them from `do_cmd` keep working," and
   `tests/cli/test_task_input.py::TestRunReportRendering::test_worker_self_report_separated`
   imports `_print_text_report` directly from `do_cmd`. The first gate-3 run caught it (1 failed).
   Repaired with one new commit per the block's red-gate clause, re-exporting all three with a
   `# noqa: F401`; gate 3 was then re-run and read green (4975 passed, 3 skipped, exit 0). The fix
   commit was amended once, before any push, to replace an initial four-line parenthesized import
   (which would have grown `do_cmd.py` past its ledger row) with a one-line form that leaves
   `do_cmd.py` at exactly the row C4 already set — no ledger/pin follow-up was needed.
2. **The four test-guard files the C4 search found were all left unedited.** Searched `tests/` for
   `_cmd_run_show`, `_cmd_run_list`, `_print_text_report` and `"run.show"`/`"run.list"`:
   `tests/test_command_catalog.py` (command-name mapping, no module path), `tests/cli/test_job_refusal_envelope.py`
   (names `do_cmd.py` only as the file an AST refusal-site scanner reads — unaffected by the move,
   since the scanner's job is "no unmigrated print-then-exit pair remains in `do_cmd.py`", true
   regardless of where `_cmd_run_show` lives), `tests/cli/test_cli_ux.py` and
   `tests/cli/test_task_input.py` (both import the moved names from `do_cmd`, which keep working
   through the re-export). None states a module path as a documented fact that the move made
   false, so the block's "edit one only where it states the module path" clause did not apply to
   any of them — until the re-export gap above surfaced one of them as a real (not merely
   documentary) break, which the fix commit resolved in the production re-export, not the test.
3. `.agent/context.md` needs no update this round: scope, assumptions and constraints are
   unchanged from round 2 (failover is still opt-in; the transport/governor/routing boundaries are
   still out of scope; the structure ledger still may not grow — both structural steps this round
   made it fall, and the one upward wobble during the fix was rewritten away before landing).
4. `.agent/plan.md`'s Current Step, written forward-looking by C1 ("book round 2's verdict...
   and the rest of T002"), is rewritten by this handback to the past tense of what actually landed,
   since the Commit Gate requires the step be accurate and C1's own copy had become false by the
   time of this handback. Next Steps now opens with "the next round's first commit books round
   3's verdict," matching this handback's own Next section.
5. `shutil.which` was patched to answer `None` for `"claude"` specifically (falling back to the
   real `shutil.which` for any other name), matching the block's literal wording, rather than
   unconditionally `None` for every name.
6. No other departure from the block's ordered C1-C6 commit sequence.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): check first.
2. Phase 1 rule 2, the Open PR Gate: check for open pull requests before starting new work.
3. The next round's first commit books round 3's verdict.
4. T003, the trigger discipline, the sticky cooldown and the session guard.

Operator questions open: 0.
Open findings: 6 — R-1235, R-1246, R-1251 and R-1252, owned by F306; R-1259 and R-1260, owned by
F058, repaired this round and awaiting the reviewer's verdict.

## For the operator, in plain sentences

When a backup model answers a call, the record of the run now names the model Remedy meant to
use, the backup that answered and every backup it tried. The short report a person reads for a run
now says in one sentence how many calls a backup model served, or that no backup could be reached.
A run in which nothing switched reads exactly as before.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five paths byte-equal; numstat matched the Bundle's five pairs exactly |
| C2 | done | two tests added over existing exclusions; one docstring sentence rewritten; ruff clean |
| C3 | done | structural move only; ledger row, pin and boundary bullet all re-measured and agree |
| C4 | deviated | the move landed correctly, but its re-export was incomplete (`_print_text_report` missing); repaired by one fix commit (`63cabe0ff`), found by gate 3, rather than a second C4 |
| C5 | done | disclosure key, report line and its call site landed exactly as specified; no `promot` growth |
| C6 | done | three test files landed with the block's exact named assertions |
| C7 | done | this handback |
| Gate 1 | passed | `git status --porcelain` empty |
| Gate 2 | passed | `ruff` `All checks passed!` over the ten named files |
| Gate 3 | deviated | first pass red (1 failed, see C4 row); fixed with one commit; second pass `4975 passed, 3 skipped`, exit 0, no FAILED/ERROR/absent/behind line |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | open-id list matched exactly |
| Gate 6 | passed | C1-C6 subjects plus the fix commit's subject, newest first |
| R-1259 | repaired | two new tests over the trigger's existing timeout/exit exclusions, plus a `supports_resume is False` test |
| R-1260 | repaired | the docstring sentence rewritten to name the shim and why it passes `create_provider` |
| Push | pending | reported in the final reply only (see External actions) |
| Pull request | skipped | the block forbids opening one this round |
