# Handoff — F158 round 6

## Session

SESSION 1 of feature F158 · round 6 · rounds so far 6. This session verified the prepared digest
and every manifest entry before touching a file, applied the four byte-copy commits exactly as
ordered, and found all five gates green on the first and only run of each.

Fortschritt: ~85 % (T001 to T003 built · the closure open) — Schätzung.

## Range

Review of `2f620c763`..`d404415e6` (C1 to C4; C5 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 23c690330 F158 R6 C1: book round 5, DECISION F158 D7, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-r6.md` | +95/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +10/-0 | DECISION F158 D7 appended (the recompute, `remedy stats recompute-costs`, `remedy stats valuations`, the docs page, amendment A3), byte-copied |
| `.agent/live_review.md` | +2/-0 | the F158 round 5 Gate entry booked at its end, byte-copied |
| `.agent/plan.md` | +10/-11 | rewritten: Current Step/Next Steps moved to round 6 and the closure, Risks line adjusted, byte-copied |

### 9a64e8293 F158 R6 C2: the recompute of a ledger's valuations and the per-basis summary
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/call_valuation.py` | +70/-3 | `ledger_call_records`, `recompute_call_valuations` and `summarize_call_valuations` added; the unused `DEFAULT_CATALOG_STALE_DAYS` removed, byte-copied |
| `tests/orchestration/test_call_valuation.py` | +63/-0 | tests for the recompute and the per-basis summary added, byte-copied |

### 6a76b4732 F158 R6 C3: remedy stats valuations and remedy stats recompute-costs, with the end-to-end
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_stats.py` | +43/-0 | the two new `stats` entries (`recompute-costs`, `valuations`) added to the catalog, byte-copied |
| `apps/cli/commands/__init__.py` | +2/-1 | `stats_valuation_cmd` imported and registered in `collect_all_handlers`, byte-copied |
| `apps/cli/commands/stats_valuation_cmd.py` | +122/-0 | NEW FILE — the two handlers: `recompute-costs` (`write_metadata`) and `valuations` (`read_only`), byte-copied |
| `apps/cli/commands/worker_pricing_cmd.py` | +1/-1 | the success line now names `remedy stats recompute-costs`, byte-copied |
| `tests/cli/test_stats_valuation_cmd.py` | +196/-0 | NEW FILE — the end-to-end: two calls valued, a catalog shown then imported with `--yes`, revalue stability, the bases, the flagged call and the unchanged `calls` digest, byte-copied |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | the new handler module's reachability entry added, byte-copied |

### d404415e6 F158 R6 C4: the price catalog and valuations page, its index rows, and amendment A3
| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +2/-0 | index row for `price-catalog-v1.md` added to both tables, byte-copied |
| `docs/roadmap/features/T8_F158.md` | +10/-0 | amendment A3 recorded: the two command names, and that staleness is reported by `stats valuations`, not `worker doctor`, byte-copied |
| `docs/system/price-catalog-v1.md` | +55/-0 | NEW FILE — the catalog format, the shipped empty catalog and why, the update command, the valuation table, the deliberate absences and the two `stats` commands, byte-copied |

### (this commit) F158 R6 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh` command run this round. No `git worktree` command run by me. No stash entry touched. No
`claude` or `codex` binary invoked by me; no provider call this round; no web fetch.
`git push origin feature/f158-cost-normalization` runs once, immediately after this commit, per
the block's push instruction; its real outcome is reported in the session reply, not in this file.

## Verification

**Gate 1.** `git -C <repo> status --porcelain` → empty (exit 0). Then
`python3 .remedy-wt/f158-r6/prep/verify.py .`, run from the primary checkout through a `cwd`-set
Python wrapper (no shell `cd`):
```
True	23c690330 single parent equal to the commit before it
True	23c690330 insertions 117 under 500 (or the handoff alone)
True	9a64e8293 single parent equal to the commit before it
True	9a64e8293 insertions 133 under 500 (or the handoff alone)
True	6a76b4732 single parent equal to the commit before it
True	6a76b4732 insertions 365 under 500 (or the handoff alone)
True	d404415e6 single parent equal to the commit before it
True	d404415e6 insertions 67 under 500 (or the handoff alone)
True	every commit carries a F158 R6 Cn subject: 4 of 4
True	on feature/f158-cost-normalization
True	C1 paths exactly [the four paths]: [the same four paths]
True	C1 .agent/authored/f158-r6.md equals c1-.agent__authored__f158-r6.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths exactly [the two paths]: [the same two paths]
True	C2 packages/orchestration/call_valuation.py equals c2-packages__orchestration__call_valuation.py
True	C2 tests/orchestration/test_call_valuation.py equals c2-tests__orchestration__test_call_valuation.py
True	C3 paths exactly [the six paths]: [the same six paths]
True	C3 apps/cli/command_catalog_stats.py equals c3-apps__cli__command_catalog_stats.py
True	C3 apps/cli/commands/__init__.py equals c3-apps__cli__commands____init__.py
True	C3 apps/cli/commands/stats_valuation_cmd.py equals c3-apps__cli__commands__stats_valuation_cmd.py
True	C3 apps/cli/commands/worker_pricing_cmd.py equals c3-apps__cli__commands__worker_pricing_cmd.py
True	C3 tests/cli/test_stats_valuation_cmd.py equals c3-tests__cli__test_stats_valuation_cmd.py
True	C3 tests/orchestration/import_reachability_allowlist.txt equals c3-tests__orchestration__import_reachability_allowlist.txt
True	C4 paths exactly [the three paths]: [the same three paths]
True	C4 docs/README.md equals c4-docs__README.md
True	C4 docs/roadmap/features/T8_F158.md equals c4-docs__roadmap__features__T8_F158.md
True	C4 docs/system/price-catalog-v1.md equals c4-docs__system__price-catalog-v1.md
absent	C5
True	the saved block equals block.md
ALL True
```
Exit 0. Every line `True` (C5 correctly `absent`, since C5 had not committed yet when this gate
ran); last line `ALL True`.

**Gate 2.** `python3 .remedy-wt/f158-r6/prep/run_selection.py . .remedy-wt/f158-r6-worker/selection-output.txt`,
run once from the primary checkout through the same kind of wrapper:
```
paths 83
exit 0
6728 passed, 2 skipped in 136.70s (0:02:16)
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
Exit 0, `6728 passed, 2 skipped`, no `FAILED`, `ERROR` or `process(es) behind` line. Both skips are
pre-existing and unrelated to this round (a deliberately quarantined test and an opt-in network
smoke test).

**Gate 3.** `python3 -m ruff check packages/orchestration/call_valuation.py apps/cli/commands/stats_valuation_cmd.py apps/cli/command_catalog_stats.py apps/cli/commands/__init__.py apps/cli/commands/worker_pricing_cmd.py tests/orchestration/test_call_valuation.py tests/cli/test_stats_valuation_cmd.py`,
run once from the primary checkout:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`, run once from the primary checkout:
```
{"check_count": 6, "checks": [{"message": "handlers=204", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0, `fail_count` 0, all six checks `pass`.

**Gate 5.** `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`,
run once from the primary checkout:
```
10
```
Exit 0, matching the block's required `10` exactly.

## Authored-text proofs

C1's byte copy and its disk-to-disk proof read `True` for all four targets immediately after
copying, before staging. The mandated proof, `.agent/authored/f158-r6.md` against `block.md`:
byte-identical, `wc -l` 95, sha256
`daa7c26650e0d8b7f2f0954b2c7033a7238e877131666eabab7d447a11ff0e78` for both files — the exact
digest `digests.txt` stated for `block.md`. Gate 1's independent `verify.py` run re-confirmed every
`C1 ... equals c1-...`, `C2 ... equals c2-...`, `C3 ... equals c3-...` and `C4 ... equals c4-...`
line `True`. `None applied` beyond C1 — C2, C3 and C4's files are prepared docs/code byte copies
proved the same way, not reviewer-authored findings or verdict prose under the fidelity protocol.

## Deviations & assumptions

None. No split, no correction commit, no file touched outside the paths named per commit, no
second test command beyond Gate 2's one scoped pytest run, no `REMEDY_TEST_MAX_WORKERS`, no `-n`
of my own beyond what `run_selection.py` itself passes, no `claude` or `codex` binary invoked, no
web fetch, no mutation red-proof, no full suite, no worktree of my own, no agent/fork/helper of
any kind started, and no `gh pr create/merge`, `git checkout`/`git switch`, branch
creation/move/deletion or force-push, and no `--no-verify`.

## For the operator, in plain sentences

This session continued teaching the program to compare money honestly across the different AI
services it calls. It first booked last round's approved decision and plan update. Then it built
the piece that decision described: a way to revalue every call in a project's record again after a
price list changes, touching only the entries whose value actually moved, together with a summary
that totals what each kind of pricing evidence found, warns about calls flagged as suspicious or
prices going stale, and never blocks on either. A new command lets someone trigger that
revaluation on demand, and a second new command shows the summary and its warnings. The command
that imports an updated price list now points to the second of these by name in its own success
message. A documentation page was added describing the price list format, why the one shipped with
the program starts empty, the import command, the valuation summary, a few things the program
deliberately does not do, and both new commands, and that page joined the project's two
documentation indexes. A matching decision recorded why these two commands live where they do
rather than inside an existing one. A test file drives the whole new path end to end against a
real project record: two calls valued, a price list shown and then imported, the calls revalued,
the exact same revaluation run again to show nothing moves a second time, and the underlying raw
call records checked unchanged throughout. Every file this session wrote was an exact copy of text
the reviewing session had already prepared and approved, checked byte for byte both before and
after copying. All required checks passed: a full test run, a style check, a health check of the
whole repository, and a count of how many known problems remain open, which held steady. Three
questions from earlier work still await your decision and are unchanged by this round. With this
round, the first three pieces of this feature's plan are now built, and what remains is the
closing work: writing down the built state, a consolidation pass, a self-use run, and one full test
run, before the usual review and merge.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to prepared copies; DECISION F158 D7 and the plan booked |
| C2 | done | two files byte-equal; the recompute and the per-basis summary landed |
| C3 | done | six files byte-equal; `remedy stats recompute-costs`, `remedy stats valuations` and the end-to-end landed |
| C4 | done | three files byte-equal; `docs/system/price-catalog-v1.md`, its index rows and amendment A3 landed |
| C5 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | every line `True`, last line `ALL True` (C5 correctly `absent`) |
| Gate 2 | done | exit 0, 6728 passed, 2 pre-existing skips, no FAILED/ERROR/process(es)-behind |
| Gate 3 | done | `All checks passed!` |
| Gate 4 | done | exit 0, `fail_count` 0, all six checks pass |
| Gate 5 | done | open ids count exactly 10, matching the block |
| Push | pending | runs immediately after this commit; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2 — the Open PR Gate: this round opens no pull request, so the next session checks
   for open pull requests before starting anything new.
3. Book round 6's verdict in the next round's first commit.
4. The closure, per `docs/roadmap/STATUS_closure_protocol.md`: the Built State, the consolidation
   pass, the self-use run and the one full suite.

Operator questions open: 3.
Open findings: 10 (unchanged this round; none owned by F158).
