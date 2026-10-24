# Handoff — F158 round 4

## Session

SESSION 1 of feature F158 · round 4 · rounds so far 4. This session verified the prepared digest
and every manifest entry before touching a file, applied the four byte-copy commits exactly as
ordered, and found all five gates green on the first and only run of each.

Fortschritt: ~60 % (T001 and T002 landed · T003 open) — Schätzung.

## Range

Review of `f992ec9fa`..`70067ff08` (C1 to C4; C5 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### b32d2f825 F158 R4 C1: book round 3, DECISION F158 D5, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-r4.md` | +96/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +10/-0 | DECISION F158 D5 (each mirrored ledger call valued beside its row, the basis rules, the threshold and the staleness check) appended, byte-copied |
| `.agent/live_review.md` | +2/-0 | the F158 round 3 Gate entry booked at its end, byte-copied |
| `.agent/plan.md` | +8/-8 | rewritten: Current Step/Next Steps to round 4, T002 part 2 per DECISION F158 D5, byte-copied |

### baeef55a0 F158 R4 C2: the cross-check threshold and catalog stale-window keys
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config_keys_budget.py` | +23/-0 | `cost.cross_check_threshold_percent` (default 5.0) and `cost.catalog_stale_days` (default 60) keys added, byte-copied |
| `docs/guides/environment.md` | +2/-0 | guide regenerated to list the two new keys, byte-copied |

### 260f7e7ff F158 R4 C3: each mirrored ledger call valued beside its row, and the staleness check
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/call_valuation.py` | +240/-0 | NEW FILE — the `call_valuations` table, `value_ledger_call`, `value_and_record_calls`, byte-copied |
| `packages/orchestration/price_catalog.py` | +6/-0 | `stale_model_prices` added, byte-copied |
| `packages/orchestration/pingpong_evidence.py` | +4/-0 | the evidence hook calls `value_and_record_calls` right after `record_task_run_calls`, inside the same guard, byte-copied |
| `tests/orchestration/import_reachability_allowlist.txt` | +2/-0 | `call_valuation.py`'s reachability entries added, byte-copied |
| `tests/test_no_orphan_modules.py` | +0/-3 | `price_catalog.py`'s `ALLOWED_UNWIRED` entry deleted — the hook now reaches it, byte-copied |

### 70067ff08 F158 R4 C4: the valuation goldens, the table, the hook and the staleness tests
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_call_valuation.py` | +261/-0 | NEW FILE — the mixed-basis goldens, the seeded deviation and the unpriced-model case, byte-copied |
| `tests/orchestration/test_price_catalog.py` | +11/-0 | `stale_model_prices` tests added, byte-copied |

### (this commit) F158 R4 C5: handback
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
`python3 .remedy-wt/f158-r4/prep/verify.py .`, run from the primary checkout through a `cwd`-set
Python wrapper (no shell `cd`):
```
True	b32d2f825 single parent equal to the commit before it
True	b32d2f825 insertions 116 under 500 (or the handoff alone)
True	baeef55a0 single parent equal to the commit before it
True	baeef55a0 insertions 25 under 500 (or the handoff alone)
True	260f7e7ff single parent equal to the commit before it
True	260f7e7ff insertions 252 under 500 (or the handoff alone)
True	70067ff08 single parent equal to the commit before it
True	70067ff08 insertions 272 under 500 (or the handoff alone)
True	every commit carries a F158 R4 Cn subject: 4 of 4
True	on feature/f158-cost-normalization
True	C1 paths exactly [the four paths]: [the same four paths]
True	C1 .agent/authored/f158-r4.md equals c1-.agent__authored__f158-r4.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths exactly [the two paths]: [the same two paths]
True	C2 docs/guides/environment.md equals c2-docs__guides__environment.md
True	C2 packages/orchestration/config_keys_budget.py equals c2-packages__orchestration__config_keys_budget.py
True	C3 paths exactly [the five paths]: [the same five paths]
True	C3 packages/orchestration/call_valuation.py equals c3-packages__orchestration__call_valuation.py
True	C3 packages/orchestration/pingpong_evidence.py equals c3-packages__orchestration__pingpong_evidence.py
True	C3 packages/orchestration/price_catalog.py equals c3-packages__orchestration__price_catalog.py
True	C3 tests/orchestration/import_reachability_allowlist.txt equals c3-tests__orchestration__import_reachability_allowlist.txt
True	C3 tests/test_no_orphan_modules.py equals c3-tests__test_no_orphan_modules.py
True	C4 paths exactly [the two paths]: [the same two paths]
True	C4 tests/orchestration/test_call_valuation.py equals c4-tests__orchestration__test_call_valuation.py
True	C4 tests/orchestration/test_price_catalog.py equals c4-tests__orchestration__test_price_catalog.py
absent	C5
True	the saved block equals block.md
ALL True
```
Exit 0. Every line `True` (C5 correctly `absent`, since C5 had not committed yet when this gate
ran); last line `ALL True`.

**Gate 1b (ordered within C4, per the block's own instruction).**
`python3 -c "from packages.orchestration.config import render_environment_guide; print(render_environment_guide() == open('docs/guides/environment.md').read())"`,
run from the repository root through the same kind of wrapper, immediately after C4:
```
exit 0
stdout: True
```

**Gate 2.** `python3 .remedy-wt/f158-r4/prep/run_selection.py . .remedy-wt/f158-r4-worker/selection-output.txt`,
run once from the primary checkout through the same kind of wrapper:
```
paths 87
exit 0
3907 passed, 2 skipped in 50.57s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
Exit 0, `3907 passed, 2 skipped`, no `FAILED`, `ERROR` or `process(es) behind` line. Both skips are
pre-existing and unrelated to this round (a deliberately quarantined test and an opt-in network
smoke test).

**Gate 3.** `python3 -m ruff check packages/orchestration/call_valuation.py packages/orchestration/price_catalog.py packages/orchestration/pingpong_evidence.py packages/orchestration/config_keys_budget.py tests/orchestration/test_call_valuation.py tests/orchestration/test_price_catalog.py tests/test_no_orphan_modules.py`,
run once from the primary checkout:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`, run once from the primary checkout:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
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
copying, before staging. The mandated proof, `.agent/authored/f158-r4.md` against `block.md`:
byte-identical, `wc -l` 96, sha256
`fbab85337f387192fb8f6faaf809ded5b6fe85a4023b16d9b201d288361bd71c` for both files — the exact
digest `digests.txt` stated for `block.md`. Gate 1's independent `verify.py` run re-confirmed every
`C1 ... equals c1-...`, `C2 ... equals c2-...`, `C3 ... equals c3-...` and `C4 ... equals c4-...`
line `True`. `None applied` beyond C1 — C2, C3 and C4's files are prepared docs/code byte copies
proved the same way, not reviewer-authored findings or verdict prose under the fidelity protocol.

## Deviations & assumptions

1. The prepared folder also held `build.py`, `d5.md`, `gate.md` and `plan.md`, none named in
   `digests.txt`; none of the four change-set commits or the five gates names them either, so they
   were left unread and unused — only the eighteen digested files that `digests.txt` and the block
   actually name were touched.

No other departure from the block's ordered commit sequence: no split, no correction commit, no
file touched outside the paths named per commit, no second test command beyond Gate 2's one scoped
pytest run, no `REMEDY_TEST_MAX_WORKERS`, no `-n` of my own beyond what `run_selection.py` itself
passes, no `claude` or `codex` binary invoked, no web fetch, no mutation red-proof, no full suite,
no worktree of my own, no agent/fork/helper of any kind started, and no `gh pr create/merge`,
`git checkout`/`git switch`, branch creation/move/deletion or force-push, and no `--no-verify`.

## For the operator, in plain sentences

This session continued teaching the program to compare money honestly across the different AI
services it calls. It first recorded last round's approved decision and plan update, then built
the actual pieces that decision described: two small settings controlling how far a catalog's own
estimate may differ from what a service itself reports before a warning fires, and how old a price
entry may get before it counts as stale; a new table that holds, for every recorded call, which
approach priced it, what that price came to, and why, kept entirely separate from the untouched
record of what actually happened, so that a later repricing can never rewrite history; the wiring
that makes every finished call actually get priced this way the moment it is recorded; and a check
for whether a price list has gone stale that reports the answer without stopping anything. A test
file was added proving all of this against a mixed set of priced and unpriced calls, a seeded
mismatch between the two pricing approaches, and an aged price list. Every file this session wrote
was an exact copy of text the reviewing session had already prepared and approved, checked byte
for byte both before and after copying. All required checks passed: a full test run, a style
check, a health check of the whole repository, and a count of how many known problems remain open,
which held steady. Three questions from earlier work still await your decision and are unchanged
by this round. The next piece of work needs one more approved decision before it can be built,
covering how prices get recomputed when a price list changes and how an operator pulls in a fresh
price list.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to prepared copies; DECISION F158 D5 and the plan booked |
| C2 | done | two files byte-equal; the two cost keys and the regenerated guide landed |
| C3 | done | five files byte-equal; the valuation module landed, the evidence hook wired, the allowed-unwired entry removed |
| C4 | done | two files byte-equal; the valuation and staleness goldens landed; the guide-render check printed `True` |
| C5 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | every line `True`, last line `ALL True` (C5 correctly `absent`) |
| Gate 2 | done | exit 0, 3907 passed, 2 pre-existing skips, no FAILED/ERROR/process(es)-behind |
| Gate 3 | done | `All checks passed!` |
| Gate 4 | done | exit 0, `fail_count` 0, all six checks pass |
| Gate 5 | done | open ids count exactly 10, matching the block |
| Push | pending | runs immediately after this commit; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2 — the Open PR Gate: this round opens no pull request, so the next session checks
   for open pull requests before starting anything new.
3. Book round 4's verdict in the next round's first commit.
4. T003 part 1: the recompute by pricing version and the pricing update command, DECISION F158 D6.

Operator questions open: 3.
Open findings: 10 (unchanged this round; none owned by F158).
