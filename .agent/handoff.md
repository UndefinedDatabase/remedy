# Handoff — F152 round 4 (DECISION F152 D4: refuse an adapter without a declaration, the A/B proof utility)

## Session

SESSION 1 of feature F152 · round 4 · rounds so far 4. This round booked round 3's FAIL, repaired
all three findings it left open, and built T002's A/B proof utility against a stand-in `claude`;
every commit followed the block's ordered sequence with no split and no correction commit needed.

Fortschritt: ~60 % (T001 and the A/B utility landed · T003 open) — Schätzung.

## Range

Review of `aa41ca9ad`..`cd586bab8` (C1 through C3; C4 — this file alone — is the commit that
carries it, per the handback template's self-reference exception).

## Commits

### ccf4db707 F152 R4 C1: book round 3's FAIL with R-1455 to R-1457, DECISION F152 D4, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r4.md` | +136/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | DECISION F152 D4 appended |
| `.agent/live_review.md` | +8/-0 | F152 round 3's FAIL verdict booked, R-1455/R-1456/R-1457 appended |
| `.agent/plan.md` | +7/-10 | rewritten: Current Step/Next Steps/Risks to round 4 |
| `.agent/prose_slips.md` | +1/-0 | one prose-slip line |

### 7dcbfcd54 F152 R4 C2: refuse an adapter without a declaration, the capability-route test states its property, the record's consequences
| Path | +/- | Reason |
|---|---|---|
| `docs/adr/0002-claude-cli-worker-isolation.md` | +15/-11 | R-1457 — "Consequences" rewritten to DECISION F152 D3/D4 and the operator question holding the real-binary proof; every other section byte-identical |
| `packages/orchestration/worker_adapter_slot.py` | +11/-12 | R-1456/D4 (1) — `adapter_child_env`/`adapter_isolation_record` call `declared_isolation`, losing the `isinstance(adapter, WorkerAdapter)` branch |
| `packages/orchestration/worker_isolation.py` | +25/-7 | `declared_isolation(adapter)` added; `record_worker_isolation`'s `record` retyped `dict[str, Any]`, its falsy-record branch and docstring clause removed |
| `tests/orchestration/test_capability_routes.py` | +21/-3 | R-1455 — the renamed test asserts no `capability_decisions.jsonl` and exactly the isolation line; both reduced adapters gain `isolation()` |
| `tests/orchestration/test_worker_adapter_slot.py` | +10/-7 | the two `_NarrowAdapter` tests become one `TypeError` test per slot function |
| `tests/orchestration/test_worker_isolation.py` | +24/-6 | the falsy-record test removed; `TestDeclaredIsolation` added (own answer, and `TypeError` for an isolation answering `None`) |

### cd586bab8 F152 R4 C3: the A/B proof utility, its stand-in proof and its red controls
| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v2.md` | +11/-3 | the "no caller yet" sentence replaced by the A/B utility, its stand-in proof and the operator-permission wait |
| `packages/orchestration/worker_isolation.py` | +90/-6 | `ISOLATION_POISON_ENV`, `IsolationAbResult`, `run_isolation_ab` (D4 (2)); the module docstring's and `create_throwaway_home`'s WHY comments updated to name the utility as the throwaway home's first caller |
| `tests/orchestration/test_worker_isolation.py` | +174/-3 | the stand-in-`claude` and `poison_home` helpers; `TestRunIsolationAb` — the full-poison proof, one test per surface, two red controls, two refusals, two home-teardown cases |

### (this commit) F152 R4 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh` command this round: the Open PR Gate runs at the next round's start (Next, below). No
worktree created or removed; no stash entry touched; no provider call; the real `claude` binary was
never invoked — forbidden this round regardless, and the A/B proof's own tests run only against a
stand-in executable the tests themselves write. `git push origin feature/f152-worker-config-isolation`
runs once, immediately after this commit, per the block's push-after-C4 rule. The block orders no
pull request.

## Verification

**Gate 1.** `git status --porcelain` → empty. Then `python3 .remedy-wt/f152-r4/prep/verify.py .`:

```
True	ccf4db707 single parent equal to the commit before it
True	ccf4db707 subject carries a F152 R4 Cn tag: F152 R4 C1: book round 3's FAIL with R-1455 to R-1457, DECISION F152 D
True	ccf4db707 insertions 162 under 500
True	ccf4db707 adds no machine path
True	7dcbfcd54 single parent equal to the commit before it
True	7dcbfcd54 subject carries a F152 R4 Cn tag: F152 R4 C2: refuse an adapter without a declaration, the capability-ro
True	7dcbfcd54 insertions 106 under 500
True	7dcbfcd54 adds no machine path
True	cd586bab8 single parent equal to the commit before it
True	cd586bab8 subject carries a F152 R4 Cn tag: F152 R4 C3: the A/B proof utility, its stand-in proof and its red cont
True	cd586bab8 insertions 275 under 500
True	cd586bab8 adds no machine path
True	on feature/f152-worker-config-isolation
True	C1 at most one split or correction: 1 commit(s)
True	C1 paths ['.agent/authored/f152-r4.md', '.agent/decisions.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md']
True	C1 .agent/authored/f152-r4.md equals c1-.agent__authored__f152-r4.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 at most one split or correction: 1 commit(s)
True	C2 paths ['docs/adr/0002-claude-cli-worker-isolation.md', 'packages/orchestration/worker_adapter_slot.py', 'packages/orchestration/worker_isolation.py', 'tests/orchestration/test_capability_routes.py', 'tests/orchestration/test_worker_adapter_slot.py', 'tests/orchestration/test_worker_isolation.py']
True	C3 at most one split or correction: 1 commit(s)
True	C3 paths ['docs/system/worker-adapter-contract-v2.md', 'packages/orchestration/worker_isolation.py', 'tests/orchestration/test_worker_isolation.py']
absent	C4
True	the record changed only in its Consequences section
True	the rewritten Consequences names DECISION F152 D3
True	the saved block equals block.md
ALL True
```

Every line `True` (C4 correctly `absent` before this commit exists); the last line is `ALL True`.

**Gate 2.** `python3 .remedy-wt/f152-r4/prep/run_selection.py . .remedy-wt/f152-r4-worker/selection-output.txt`,
run once after C3:

```
paths 88
exit 0
3936 passed, 2 skipped in 35.93s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Exit 0, no `FAILED` or `ERROR` line, no "process(es) behind" line. Both `SKIPPED` lines are
pre-existing, documented skips unrelated to this round — identical to round 3's reading. The
pre-existing red this round inherited (`test_stream_evidence_false_writes_no_file`, flagged in round
3's own Deviations) is resolved by this round's R-1455 repair and no longer appears.

**Gate 3.** `python3 -m ruff check` over every Python file C2 and C3 touched (5 files:
`packages/orchestration/worker_isolation.py`, `packages/orchestration/worker_adapter_slot.py`,
`tests/orchestration/test_worker_isolation.py`, `tests/orchestration/test_worker_adapter_slot.py`,
`tests/orchestration/test_capability_routes.py`):

```
All checks passed!
```

Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass`, `"ok": true`. `live_review_verdict` reads "last Gate verdict
FAIL" because round 3's own FAIL is the most recent Gate entry this check can see at this point in
the branch's own history; that is the round this handback books the repair for, not a defect of this
one.

**Gate 5.** `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
`11`, exit 0 — exactly the count the block names (the eight F316-owned ids plus R-1455, R-1456 and
R-1457, each still OPEN in the ledger text itself even though this round's own code repairs them;
the ledger entries are closed by a `Done:` paragraph in a later round, per the workflow's own rule
that a landed paragraph is not rewritten).

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r4-worker/do_c1_copy.py`) read `True` for all five targets
immediately after copying: `.agent/authored/f152-r4.md`, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`. `.agent/authored/f152-r4.md`'s own
line count and sha256 — `136` lines, `f0cb01935c2cc15431f328575eed1866b504c81862beb2c775bd7cebc658ca55` —
were independently confirmed equal to `block.md`'s own count and digest by `wc -l` and `sha256sum`
run directly on both files. Gate 1's `verify.py` run independently re-confirmed every
`C1 ... equals c1-...` line `True` and the saved block equals `block.md`.

C2 and C3 carry no second reviewer-prepared text to compare against (no `c2-`/`c3-` files exist in
the prep bundle); their own content is this round's worker-authored code and tests, checked by the
gates above rather than a byte comparison.

## Deviations & assumptions

None. Every commit followed the block's ordered sequence exactly: no split (`C2a`/`C2b` or
`C3a`/`C3b`), no correction commit, no file touched outside the paths named per commit. No mutation
red-proofs, no full suite, no `REMEDY_TEST_MAX_WORKERS`, no two test commands run at once, no
`claude` binary invoked. The one judgment call worth stating explicitly rather than leaving
implicit: R-1455's repair (renaming and rewriting the test) and the two reduced adapters in
`tests/orchestration/test_capability_routes.py` gaining `isolation()` were both required together —
D4 (1)'s refusal makes a conforming `isolation()` mandatory for any adapter reaching
`create_role_provider`, so the two repairs are one coherent change rather than two independent
ones, exactly as the block's own C2 bullet groups them.

## For the operator, in plain sentences

This round closed out the three problems last round's check-up found and then built the second
half of the isolation work: a tool used to run a worker's call must now say, in a fixed and checked
way, how it keeps the operator's own personal settings out of that call; an installed tool that
skips this declaration entirely is now refused outright rather than quietly let through with no
protection and no record, which is a safety gap this round closes. On top of that, a reusable check
was built that can take any such tool's own declared command and prove, by running it twice against
a deliberately tainted practice copy of its personal settings, whether the declared protection
really works — once without the protection and once with it, comparing whether a planted marker
leaks through. That check currently runs only against a stand-in program the tests themselves
write, because running it against the real paid tool needs the operator's own permission, which is
still an open question from an earlier round. Every other test this project runs, and the project's
own health and findings checks, stayed green. Nothing is pushed yet; that happens right after this
note is saved.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to the prepared snapshots |
| C2 | done | `declared_isolation` refuses an adapter without a declaration; R-1455 and R-1456 repaired; R-1457 repaired |
| C3 | done | `ISOLATION_POISON_ENV`, `IsolationAbResult`, `run_isolation_ab`; stand-in proof, two red controls, two refusals, two home-teardown cases; the contract page updated |
| C4 | done | this handback |
| R-1455 | done | repaired in C2 |
| R-1456 | done | repaired in C2 |
| R-1457 | done | repaired in C2 |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | exit 0, `3936 passed, 2 skipped`, no FAILED/ERROR, no leftover process |
| Gate 3 | done | exit 0, all checks passed |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open-id count 11, matches the block exactly |
| Push | pending | runs once immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 4's verdict and resolve R-1455 to R-1457 in the next round's first commit.
4. T003: doctor, the kit requirement and the docs.

Operator questions open: 3.
Open findings: 11.
