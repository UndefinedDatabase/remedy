# Handoff — F158 round 3

## Session

SESSION 1 of feature F158 · round 3 · rounds so far 3. This session verified the prepared digest
and every manifest entry before touching a file, applied the three byte-copy commits exactly as
ordered, and found all five gates green on the first and only run of each.

Fortschritt: ~45 % (T001 and the catalog format landed · the ledger valuation and T003 open) —
Schätzung.

## Range

Review of `48213e23b`..`afb02742e` (C1 to C3; C4 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 51995a931 F158 R3 C1: book round 2, DECISION F158 D4, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-r3.md` | +88/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +10/-0 | DECISION F158 D4 (the price catalog format, its refusals and the empty claude-cli catalog) appended, byte-copied |
| `.agent/live_review.md` | +2/-0 | the F158 round 2 Gate entry booked at its end, byte-copied |
| `.agent/plan.md` | +14/-16 | rewritten: Current Step/Next Steps to round 3, T002 part 1 per DECISION F158 D4, byte-copied |

### fd7290f89 F158 R3 C2: amendment A1, the catalog's names follow the tree
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T8_F158.md` | +19/-0 | amendment A1 appended: the catalog basis word (`price_table`, not `catalog_computed`), its home beside its module, the advisory model/currency checks, the removed cockpit, and the tests' home in `tests/orchestration/`, byte-copied |

### afb02742e F158 R3 C3: the price catalog format, its refusals and the empty claude-cli catalog
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/price_catalog.py` | +184/-0 | NEW FILE — `PRICE_CATALOG_DIR`, the field tuples, `PriceCatalogError`, `ModelPrice`, `PriceCatalog`, `registered_adapter_refs`, `parse_price_catalog`, `load_price_catalog`, `load_price_catalogs`, `price_catalog_warnings`, byte-copied |
| `packages/orchestration/price_catalog_files/claude-cli.toml` | +24/-0 | NEW FILE — the shipped, empty claude-cli catalog with its comment explaining why, byte-copied |
| `tests/orchestration/test_price_catalog.py` | +188/-0 | NEW FILE — the format's refusals, the shipped empty catalog, the advisory warnings and `registered_adapter_refs`, byte-copied |
| `tests/test_no_orphan_modules.py` | +3/-0 | `ALLOWED_UNWIRED` gains `price_catalog.py`'s entry, with the reason the next round's ledger writer retires, byte-copied |

### (this commit) F158 R3 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh` command run this round — the block defers the Open PR Gate check to the next session. No
`git worktree` command run by me. No stash entry touched. No `claude` or `codex` binary invoked by
me; no provider call this round; no web fetch. `git push origin feature/f158-cost-normalization`
runs once, immediately after this commit, per the block's push instruction; its real outcome is
reported in the session reply, not in this file.

## Verification

**Gate 1.** `git -C <repo> status --porcelain` → empty (exit 0). Then
`python3 .remedy-wt/f158-r3/prep/verify.py .`, run from the primary checkout through a `cwd`-set
Python wrapper (no shell `cd`):
```
True	51995a931 single parent equal to the commit before it
True	51995a931 insertions 114 under 500 (or the handoff alone)
True	fd7290f89 single parent equal to the commit before it
True	fd7290f89 insertions 19 under 500 (or the handoff alone)
True	afb02742e single parent equal to the commit before it
True	afb02742e insertions 399 under 500 (or the handoff alone)
True	every commit carries a F158 R3 Cn subject: 3 of 3
True	on feature/f158-cost-normalization
True	C1 paths exactly [the four paths]: [the same four paths]
True	C1 .agent/authored/f158-r3.md equals c1-.agent__authored__f158-r3.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths exactly [the one path]: [the same one path]
True	C2 docs/roadmap/features/T8_F158.md equals c2-docs__roadmap__features__T8_F158.md
True	C3 paths exactly [the four paths]: [the same four paths]
True	C3 packages/orchestration/price_catalog.py equals c3-packages__orchestration__price_catalog.py
True	C3 packages/orchestration/price_catalog_files/claude-cli.toml equals c3-packages__orchestration__price_catalog_files__claude-cli.toml
True	C3 tests/orchestration/test_price_catalog.py equals c3-tests__orchestration__test_price_catalog.py
True	C3 tests/test_no_orphan_modules.py equals c3-tests__test_no_orphan_modules.py
absent	C4
True	the saved block equals block.md
ALL True
```
Exit 0. Every line `True` (C4 correctly `absent`, since C4 had not committed yet when this gate
ran); last line `ALL True`.

**Gate 2.** `python3 .remedy-wt/f158-r3/prep/run_selection.py . .remedy-wt/f158-r3-worker/selection-output.txt`,
run once from the primary checkout through the same kind of wrapper:
```
paths 82
exit 0
3618 passed, 2 skipped in 51.88s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
Exit 0, `3618 passed, 2 skipped`, no `FAILED`, `ERROR` or `process(es) behind` line. Both skips are
pre-existing and unrelated to this round (a deliberately quarantined test and an opt-in network
smoke test).

**Gate 3.** `python3 -m ruff check packages/orchestration/price_catalog.py tests/orchestration/test_price_catalog.py tests/test_no_orphan_modules.py`,
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
copying, before staging. The mandated proof, `.agent/authored/f158-r3.md` against `block.md`:
byte-identical (`block.md == authored/f158-r3.md: True`), `wc -l` 88, sha256
`39d9ce5575857e0196ed6b410756ed8512d5570cd0d57e23dca8e9dffd56ec2a` for both files — the exact
digest `digests.txt` stated for `block.md`. Gate 1's independent `verify.py` run re-confirmed every
`C1 ... equals c1-...`, `C2 ... equals c2-...` and `C3 ... equals c3-...` line `True`. `None
applied` beyond C1 — C2's and C3's files are prepared docs/code byte copies proved the same way,
not reviewer-authored findings or verdict prose under the fidelity protocol.

## Deviations & assumptions

1. The prepared folder also held `a1.md`, `build.py`, `d4.md`, `gate.md` and `plan.md`, none named
   in `digests.txt`; none of the three change-set commits or the five gates names them either, so
   they were left unread and unused — only the fourteen digested files that `digests.txt` and the
   block actually name were touched.

No other departure from the block's ordered commit sequence: no split, no correction commit, no
file touched outside the paths named per commit, no second test command beyond Gate 2's one scoped
pytest run, no `REMEDY_TEST_MAX_WORKERS`, no `-n` of my own beyond what `run_selection.py` itself
passes, no `claude` or `codex` binary invoked, no web fetch, no mutation red-proof, no full suite,
no worktree of my own, no agent/fork/helper of any kind started, and no `gh pr create/merge`,
`git checkout`/`git switch`, branch creation/move/deletion or force-push, and no `--no-verify`.

## For the operator, in plain sentences

This session continued teaching Remedy to compare money honestly across the different AI services
it calls. It first recorded last round's approved decision and plan update, then built the actual
pieces that decision described: a simple file format for listing what each AI service charges per
model, one file per service kept beside the code that reads it; a loader that reads such a file and
refuses the whole thing, naming why, if even one entry is malformed, missing its price, missing its
required source or using an unapproved currency; a test file proving every one of those refusals and
the honest handling of an unpriced model; and the starting price list for the Claude command line,
shipped empty on purpose because that service already states its own cost for every call, with a
comment explaining why no price is listed yet. A note was also added to the feature's planning
document recording four small ways the actual program's existing names differ from the original
plan's wording, so the plan now matches the code. Every file this session wrote was an exact copy of
text the reviewing session had already prepared and approved, checked byte for byte both before and
after copying. All required checks passed: a full test run, a style check, a health check of the
whole repository, and a count of how many known problems remain open, which held steady. Three
questions from earlier work still await your decision and are unchanged by this round. The next
piece of work is teaching the program to price each individual use of an AI service as it happens,
which needs one more approved decision before it can be built.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to prepared copies; DECISION F158 D4 and the plan booked |
| C2 | done | one file byte-equal; amendment A1 landed in the feature file |
| C3 | done | four files byte-equal; the shipped catalog and its tests landed, the allowed-unwired entry added |
| C4 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | every line `True`, last line `ALL True` (C4 correctly `absent`) |
| Gate 2 | done | exit 0, 3618 passed, 2 pre-existing skips, no FAILED/ERROR/process(es)-behind |
| Gate 3 | done | `All checks passed!` |
| Gate 4 | done | exit 0, `fail_count` 0, all six checks pass |
| Gate 5 | done | open ids count exactly 10, matching the block |
| Push | pending | runs immediately after this commit; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2 — the Open PR Gate: this round opens no pull request, so the next session checks
   for open pull requests before starting anything new.
3. Book round 3's verdict in the next round's first commit.
4. T002 part 2: each ledger call valued at record time, DECISION F158 D5.

Operator questions open: 3.
Open findings: 10 (unchanged this round; none owned by F158).
