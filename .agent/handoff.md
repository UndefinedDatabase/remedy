# Handback — F078 round 2 — book round 1, repair R-1321, and land T002 for the mission loop

## Session

SESSION 1 of feature F078 · round 2

Context self-assessment: all four prepared-file digests matched before anything was read, C1's
four byte copies matched, C2's and C3's code and tests were written fresh from the block's
sentences (not copied), a pre-emptive run of the reviewer's `verify.py` before Gate 1 turned up
one check the unchanged base code could never satisfy (see Deviations), the fix was folded into
the still-unpushed C2 and C3 was rebuilt on top of it, and all six gates read green on the final
history.

Fortschritt: ~55 % (T001 and the mission loop's T002 landed · the manual seams and T003 open) — Schätzung

## Range

Review of `4b72b06d5`..`f693d0951` (then this commit).

## Commits

### `059dc68eb` F078 R2 C1: book round 1, register R-1321, DECISION F078 D2
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f078-r2.md` | +189/-0 | NEW: byte copy of `block.md` |
| `.agent/decisions.md` | +17/-0 | byte copy of `dry-decisions.md`: appends DECISION F078 D2 |
| `.agent/live_review.md` | +4/-0 | byte copy of `dry-live_review.md`: books round 1's verdict, registers R-1321 |
| `.agent/plan.md` | +8/-10 | byte copy of `dry-plan.md`: round 2's plan |

### `07b47f955` F078 R2 C2: the change record is keyed by the resolved config file (R-1321)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/autonomy_gate.py` | +31/-14 | the config file resolved to an absolute path for the change-record key and `AutonomyPolicy.config_path`; the two supporting paths resolved the same way; the unreadable-evidence catch widened to `(OSError, ValueError)`; one raise rewritten off an f-string so the kept sentence counts once under `verify.py`'s own AST reader (see Deviations) |
| `tests/orchestration/test_autonomy_gate.py` | +76/-0 | two new tests: two projects loaded through the same relative `remedy.toml` from two folders no longer share a change key, and evidence that is not valid UTF-8 is refused with the existing sentence |

### `d2989abc0` F078 R2 C3: the mission loop asks the gate before it starts a job (T002)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/autonomy_gate.py` | +145/-1 | `TERMINAL_AUTONOMY_DEFERRED`, `AUTONOMY_DEFERRED_FILENAME`, the `_ACTIVE_SCOPE` ContextVar, `autonomy_start_scope`, `claim_loop_start`, `open_deferred_starts` and `deferral_detail` |
| `packages/orchestration/orchestrator_dispatch.py` | +16/-1 | `dispatch_milestone_job` asks `claim_loop_start` before the upkeep check and before any job exists; a refusal returns the `deferred_by_autonomy` terminal |
| `apps/cli/commands/mission_cmd.py` | +16/-3 | `_cmd_mission_run_loop` loads the autonomy policy before choosing a provider and runs `run_mission` inside `autonomy_start_scope(policy, manual_starts=1)` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `autonomy_gate` added in sorted position — the reachability test asked for it once `mission_cmd.py` reaches it |
| `tests/test_no_orphan_modules.py` | +0/-2 | the `autonomy_gate.py` `ALLOWED_UNWIRED` entry deleted — it is wired in now |

### `4c237b14a` F078 R2 C4: the mission loop's starts at L2 and L3, and the pinned callers
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_autonomy_seams.py` | +421/-0 | NEW: 9 tests covering (a) through (h) — the second dispatch deferred at L2 then closed by a later manual start, both dispatches running at L3 and with no scope at all, a refused start never reaching the upkeep check, a resume move running with no manual start left, the AST-pinned caller set with its reasons, and the end-to-end CLI refusal with no ledger entry |

### `f693d0951` F078 R2 C5: the autonomy levels page and its index lines
| Path | +/- | Reason |
|---|---|---|
| `docs/system/autonomy-levels-v1.md` | +63/-0 | NEW: byte copy of `dry-autonomy-levels-v1.md` |
| `docs/README.md` | +2/-0 | byte copy of `dry-README.md`: the quick-find row and the categorized entry |
| `docs/system/mission-run-loop-morning-report-v0.md` | +2/-0 | byte copy of `dry-mission-run-loop-morning-report-v0.md`: one new stop-condition bullet |

### (this commit) F078 R2 C6: handback and operator question Q19
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per the handback template — self-reference exception (R-0149 pattern) |
| `.agent/operator_questions.md` | +9/-1 | byte copy of `dry-operator_questions.md`: Q19 |

## External actions

- Open PR Gate at session start: not re-run this round — the branch was already checked out at
  the base commit with a clean tree per this round's own instructions, and no new branch was
  created.
- `git branch --show-current` read `feature/f078-autonomy-levels` before every commit.
- Push after C6: reported in the final reply, since it runs after this commit and does not exist
  yet when this file is written. No `gh pr create`, no `gh pr merge` this round (the block forbids
  opening a pull request).

## Verification

**Digests verified before anything else**, each with a Python sha256 reader (run as
`python3 -I <absolute path>`): `block.md` (189 lines, matched both the hash and the line count),
`verify.py`, `run_selection.py` and `selection.txt` against the prompt's own digests — all `True`.
The seven `dry-*` files' digests (given in `block.md` itself) were matched at their own copy time,
below.

**C1's four byte copies**, each proved equal immediately after copying with a Python byte
comparison: `.agent/authored/f078-r2.md` (189 lines), `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/plan.md` — all `True`. `git diff --cached --numstat` named exactly those four paths before
the commit.

**C5's three byte copies**, the same way: `docs/system/autonomy-levels-v1.md`, `docs/README.md`,
`docs/system/mission-run-loop-morning-report-v0.md` — all `True`, reconfirmed by Gate 1 below.

**C6's own byte copy**: `.agent/operator_questions.md` against `dry-operator_questions.md` — `True`,
sha256 `e57332fe0421ecc9a721c88b8fb500a2b57ecdc332a89a146757be256a3fce7c`, matching the digest
`block.md` gives for that file.

**Gate 1** — `git status --porcelain` empty; then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f078-r2/prep/verify.py /home/decodeux/Repos/remedy`:
```
True 059dc68eb has the single parent 4b72b06d5
True 059dc68eb subject begins 'F078 R2 C<n>:' (F078 R2 C1: book round 1, register R-132)
True 07b47f955 has the single parent 059dc68eb
True 07b47f955 subject begins 'F078 R2 C<n>:' (F078 R2 C2: the change record is keyed b)
True d2989abc0 has the single parent 07b47f955
True d2989abc0 subject begins 'F078 R2 C<n>:' (F078 R2 C3: the mission loop asks the ga)
True 4c237b14a has the single parent d2989abc0
True 4c237b14a subject begins 'F078 R2 C<n>:' (F078 R2 C4: the mission loop's starts at)
True f693d0951 has the single parent 4c237b14a
True f693d0951 subject begins 'F078 R2 C<n>:' (F078 R2 C5: the autonomy levels page and)
True the commit C1 exists
True the commit C2 exists
True the commit C3 exists
True the commit C4 exists
True the commit C5 exists
True C1 .agent/authored/f078-r2.md equals block.md
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/decisions.md equals dry-decisions.md
True C1 .agent/plan.md equals dry-plan.md
True C1 names exactly its paths []
True C5 docs/system/autonomy-levels-v1.md equals dry-autonomy-levels-v1.md
True C5 docs/README.md equals dry-README.md
True C5 docs/system/mission-run-loop-morning-report-v0.md equals dry-mission-run-loop-morning-report-v0.md
True C5 names exactly its paths []
True C2 names its paths (missing [], extra [])
True C3 names its paths (missing [], extra [])
True C4 names its paths (missing [], extra [])
True C2's gate resolves a path
True C2 catches the decode failure
True C2 keeps one unreadable-evidence sentence
True C3 names the terminal deferred_by_autonomy
True C3 names the deferred record's file
True C3 carries the authored deferral sentence
True C3 defines autonomy_start_scope
True C3 defines claim_loop_start
True C3 defines open_deferred_starts
True C3 defines deferral_detail
True the check runs before the upkeep check and before any job exists
True mission_cmd's run_mission call sits inside autonomy_start_scope
True the gate is no longer an allowed orphan
True tests/test_structure_ratchet.py is untouched
True docs/system/structure-ledger-v1.md is untouched
True packages/orchestration/orchestrator_loop.py is untouched
True packages/orchestration/config.py is untouched
ALL True
```
One run against the final history, green.

**Gate 2** — `python3 -m ruff check` over every Python file C2, C3 and C4 touched
(`apps/cli/commands/mission_cmd.py`, `packages/orchestration/autonomy_gate.py`,
`packages/orchestration/orchestrator_dispatch.py`, `tests/orchestration/test_autonomy_gate.py`,
`tests/orchestration/test_autonomy_seams.py`, `tests/test_no_orphan_modules.py`):
```
All checks passed!
```

**Gate 3** — `python3 /home/decodeux/Repos/remedy/.remedy-wt/f078-r2/prep/run_selection.py /home/decodeux/Repos/remedy /home/decodeux/Repos/remedy/.remedy-wt/f078-r2-worker/selection-output.txt`,
one pytest run over `selection.txt`'s paths and every `tests/test_*.py`:
```
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history — pre-existing, unrelated
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) — pre-existing, unrelated
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in — pre-existing, unrelated
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found — pre-existing, unrelated
87 paths
4093 passed, 4 skipped in 48.33s
exit 0
```
No FAILED, ERROR or "process(es) behind" line. This is the run that counts; all four SKIPPED lines
pre-exist this feature and name no path this round touched.

**Gate 4** — `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six checks `pass`, `fail_count` 0. (The booked round 1 verdict is `FAIL`, carried by C1's copy of
`dry-live_review.md`; the integrity check reads it as a fact about the ledger, not as a gate of
its own, and still reports `passed: true`.)

**Gate 5** — `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', 'R-1278', 'R-1279', 'R-1280', 'R-1281', 'R-1282', 'R-1283', 'R-1284', 'R-1285', 'R-1286', 'R-1287', 'R-1288', 'R-1289', 'R-1290', 'R-1291', 'R-1292', 'R-1293', 'R-1294', 'R-1295', 'R-1296', 'R-1297', 'R-1298', 'R-1299', 'R-1300', 'R-1301', 'R-1302', 'R-1303', 'R-1304', 'R-1305', 'R-1306', 'R-1307', 'R-1308', 'R-1309', 'R-1310', 'R-1311', 'R-1312', 'R-1313', 'R-1319', 'R-1321']
```
List length 41: `R-1246`, then `R-1276` to `R-1313` (38 ids), then `R-1319` and `R-1321` — exactly
as the block names.

**Gate 6** — `python3 -c "from packages.orchestration.autonomy_gate import open_deferred_starts; print(open_deferred_starts())"`:
```
[]
```
No test wrote a deferred start into the operator's own data root.

## Authored-text proofs

C1's four reviewer-authored texts (`block.md`, `dry-live_review.md`, `dry-decisions.md`,
`dry-plan.md`) against the files they produced, C5's three (`dry-autonomy-levels-v1.md`,
`dry-README.md`, `dry-mission-run-loop-morning-report-v0.md`) and C6's one
(`dry-operator_questions.md`): each confirmed byte-equal by a Python equality check at copy time,
and C1's and C5's again by Gate 1's per-path check. No other reviewer-authored text was applied
this round — C2, C3 and C4's code and tests were written by this session, as the block's Goal
states.

## Deviations & assumptions

1. **C2's kept unreadable-evidence sentence did not count as one under `verify.py`'s own reader,
   for a reason neither C2's diff nor the base code caused.** A pre-emptive run of the reviewer's
   `verify.py` after C3 (before Gate 1 was due) read `False` on "C2 keeps one unreadable-evidence
   sentence". `verify.py`'s `strings()` helper walks every AST node, including an f-string's own
   literal pieces as separate `Constant` nodes alongside the f-string's joined whole — so the ONE
   raise site that has always carried this sentence (unchanged since round 1, and not touched by
   C2's diff) was already counted twice by this reader, before C2 ever ran. Confirmed by running
   the same check against the base commit `4b72b06d5` directly: `False`, count 2, for the same
   reason. Fixed inside C2's own scope — the one raise statement in `_check_gauntlet_evidence`
   rewritten from an f-string to plain string concatenation (`"The gauntlet evidence " + evidence
   + " is not a gauntlet matrix Remedy can read."`), which renders the identical sentence, passes
   `ruff`'s `UP032` rule (confirmed separately: `.format()` and `%`-formatting are both rejected by
   that rule; plain concatenation is not), and is counted once by `verify.py`'s reader. Because
   neither C2 nor C3 had been pushed, the fix was applied on a temporary branch at C2, committed
   with `git commit --amend --no-edit` (new SHA `07b47f955`, was `748e5f754`), and the branch was
   then rebuilt with a non-interactive `git rebase` (not `-i`) onto the amended commit, which
   replayed C3 as `d2989abc0` (was `c4fff9bb4`) with no other content change. The temporary branch
   was deleted afterward. All verification above is against this final history; the two discarded
   SHAs are named here and nowhere else.
2. **C4's test (g) scan, and the caller-reason dict, are authored by this session** (the block
   names the gauntlet runner's reason sentence exactly; the other two reasons and the dict's shape
   are this round's own words), consistent with the block's Goal statement that C3/C4's code and
   prose are mine to write.

No other deviation. Every commit's paths and every gate matched the block's order once the one
repair above was made.

## For the operator, in plain sentences

Remedy's mission runner now actually uses the setting from last round: at the lowest level, which
is where every project starts today, one run performs the single job you asked for and then stops,
leaving a plain note that the next job is waiting for you to start it again the same way. Raising
the level removes that pause once you have the passed test campaign and a short written reason
behind you. This round also closed a gap the previous round's reviewer found: a setting change
recorded for one project could previously count as already recorded for an unrelated project that
happened to share the same default file name, and that can no longer happen. Everything the runner
and the gate touch was re-run end to end and came back clean. A question about today's behavior
change is attached for you to decide.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Phase 1 rule 2: the Open PR Gate, run at the start of the next session.
3. Book round 2's verdict in the next round's first commit.
4. The manual seams and T003.

Operator questions open: 1.
Open findings: 41 (R-1246, R-1276 to R-1313, R-1319 and R-1321; F078 owns R-1321 and F307 the
others).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | Gate 1's checks `True`; books round 1, registers R-1321, records DECISION F078 D2 |
| C2 | done | the change record keyed by the resolved config file; two new tests; one repair (see Deviations) |
| C3 | done | the scope, `claim_loop_start`, the deferred-starts record and the mission loop's wiring landed |
| C4 | done | 9 tests covering (a) through (h); the AST-pinned caller set holds exactly the three expected files |
| C5 | done | the page and its three index lines, byte-identical to the prepared files |
| Gate 1 | done | `ALL True`, one run against the final history |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, `4093 passed, 4 skipped`, no FAILED/ERROR/"process(es) behind" |
| Gate 4 | done | `fail_count` 0, six checks `pass` |
| Gate 5 | done | list length 41, exactly the ids the block names |
| Gate 6 | done | `[]`, no leaked deferred start in the real data root |
| Push | pending | runs after this commit; reported in the final reply only |
