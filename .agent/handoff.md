# Handoff — F162 round 2

## Session

SESSION 1 of feature F162 · round 2 · rounds so far 2. This session booked round 1's verdict,
appended DECISION F162 D2 and the plan rewrite in its first commit, then built T001 — the
`sandbox_profiles` module, its three built-in profile files, the tighten-only preorder and its
refusal — with table tests pinning every rule of D2 (3) through (6); context self-assessment: the
module's own docstring and DECISION F162 D2 (7) already state plainly that nothing reads a profile
yet, so this round's whole surface is policy math, proved against itself rather than against any
spawn path.

Fortschritt: ~25 % (T001 landed · T002, T003 open) — Schätzung.

## Range

Review of `a564541c9`..`aa9fccfec` (C1 to C3; C4 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### be9762d37 F162 R2 C1: book round 1, DECISION F162 D2, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r2.md` | +147/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +17/-0 | DECISION F162 D2 appended: the sandbox profile schema, the built-ins, the order and the refusal |
| `.agent/live_review.md` | +2/-0 | round 1's gate/verdict entry booked |
| `.agent/plan.md` | +8/-11 | rewritten: Current Step moves to T001 under DECISION F162 D2 |
| `.agent/prose_slips.md` | +1/-0 | one reviewer-prose line appended, per the prepared file |

### f85e61882 F162 R2 C2a: the sandbox profile module and its three built-in profile files
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/sandbox_profile_files/net-local.toml` | +8/-0 | NEW FILE — the `net-local` built-in, `standard` plus a loopback/localhost allowlist |
| `packages/orchestration/sandbox_profile_files/standard.toml` | +8/-0 | NEW FILE — the `standard` built-in |
| `packages/orchestration/sandbox_profile_files/strict.toml` | +8/-0 | NEW FILE — the `strict` built-in |
| `packages/orchestration/sandbox_profiles.py` | +330/-0 | NEW FILE — the schema, the TOML parser and its refusals, the loader, and the tighten-only comparator (DECISION F162 D2 (2)-(6)) |
| `tests/test_no_orphan_modules.py` | +2/-0 | `ALLOWED_UNWIRED` entry for the new module, in path order after `hunk_apply.py` |

### 9641d1479 F162 R2 C2b: the sandbox profile module's parsing and built-in tests
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_sandbox_profiles.py` | +158/-0 | NEW FILE — this half pins the TOML form's 25 refusal rules, the built-ins' exact values, `get_sandbox_profile`, normalization, and the loader's two folder-shape refusals |

Deviation: C2 was split into C2a/C2b because the combined diff measured 514 insertions, over the
500-insertion cap; the block names this split as the expected response and asks that it be
declared (see Deviations & assumptions).

### aa9fccfec F162 R2 C3: the tighten-only order's table tests and the refusal
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_sandbox_profiles.py` | +177/-0 | per-dimension order tables (`fs_scope`, `net`, a ulimits key, `tmp_quota_mb`, `allowed_binaries`), the two built-in `profile_loosenings` results, the preorder's reflexivity/transitivity/non-antisymmetry, and `tighten_sandbox_profile`'s pass-through and refusal message |

### (this commit) F162 R2 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh pr list`, `gh pr create`, `gh pr merge`, or `git worktree` command this round: this is a
continuation round on the already-open feature branch, not a new branch start, so the Open PR Gate
does not apply here (it is the next round's first duty, named in `## Next`). No `claude` binary
invoked; no model/provider call of any kind. `git push origin feature/f162-sandbox-profiles` runs
once, immediately after this commit, per the block's push discipline; its real outcome is reported
in the session reply, not in this file.

## Verification

**Gate 1.** After C3, `git -C <repository root> status --porcelain`: empty output. Then
`python3 .remedy-wt/f162-r2/prep/verify.py .`:
```
True	be9762d37 single parent equal to the commit before it
True	be9762d37 subject carries a F162 R2 Cn tag
True	be9762d37 insertions 175 under 500
True	f85e61882 single parent equal to the commit before it
True	f85e61882 subject carries a F162 R2 Cn tag
True	f85e61882 insertions 356 under 500
True	9641d1479 single parent equal to the commit before it
True	9641d1479 subject carries a F162 R2 Cn tag
True	9641d1479 insertions 158 under 500
True	aa9fccfec single parent equal to the commit before it
True	aa9fccfec subject carries a F162 R2 Cn tag
True	aa9fccfec insertions 177 under 500
True	on feature/f162-sandbox-profiles
True	C1 paths exactly [...]: [...] (five paths, exact match)
True	C1 .agent/authored/f162-r2.md equals c1-.agent__authored__f162-r2.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 paths exactly [...]: [...] (six paths across C2a+C2b, exact match)
True	C2 <each path> adds no machine path (six lines)
True	C3 paths exactly ['tests/orchestration/test_sandbox_profiles.py']: [same]
True	C3 tests/orchestration/test_sandbox_profiles.py adds no machine path
absent	C4
True	C2 orphan entry present
True	C2 orphan entry in path order
True	C2 strict.toml holds 'net = "deny"' and ends with [ulimits]
True	C2 standard.toml holds 'allowed_binaries = "any"' and ends with [ulimits]
True	C2 net-local.toml holds 'allow = ["127.0.0.1", "::1", "localhost"]' and ends with [ulimits]
True	the saved block equals block.md
ALL True
```
Every line `True` (C4 correctly `absent`, not yet committed when this gate ran); last line
`ALL True`.

**Gate 2.** `python3 .remedy-wt/f162-r2/prep/run_selection.py . .remedy-wt/f162-r2-worker/selection-output.txt`,
run once, after C3:
```
paths 84
exit 0
3831 passed, 2 skipped in 34.42s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
`exit 0`, no `FAILED` or `ERROR` line, no line containing `process(es) behind`. Both `SKIPPED`
lines reported verbatim, as required. Not red, so no second run was needed.

**Gate 3.** `python3 -m ruff check packages/orchestration/sandbox_profiles.py tests/orchestration/test_sandbox_profiles.py tests/test_no_orphan_modules.py`:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
`9`. Exactly the block's named count.

## Authored-text proofs

C1's five byte copies (`.remedy-wt/f162-r2-worker/c1_copy.py`) were each proved byte-equal to their
prepared `c1-` file immediately after copying. The authored block's own proof:
`.agent/authored/f162-r2.md` is 147 lines (`wc -l`) with sha256
`2b653a56c3df6ccbac94d26c10757b41f7a7dac0dc9b8292ada08b265c6c5a80`, identical to `block.md`'s own
sha256 — the same digest `digests.txt` names for both prepared files. Gate 1's `verify.py` run
independently re-confirmed every `C1 ... equals c1-...` line `True`.

## Deviations & assumptions

1. C2 was split into C2a and C2b. The combined module, three TOML files, orphan entry and test
   file measured 514 insertions against the 500-insertion cap; the block itself names this split
   as the expected response ("If C2 would pass 500 insertions, split it once into C2a ... and C2b
   ..., and say so"), so this is a planned, declared split rather than an ad hoc one. C2a carries
   the module, the three built-in files and the orphan-list entry (356 insertions); C2b carries the
   test file (158 insertions). `verify.py`'s own by-tag grouping treats `C2a`/`C2b` as one logical
   `C2` for its path-set check, and that check reads `True` above.
2. Before the official gate runs, several single-file `pytest` invocations
   (`tests/orchestration/test_sandbox_profiles.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_import_reachability.py`, `tests/test_structure_ratchet.py`) and several
   `ruff check` runs were made during drafting, to self-review each commit's diff before it was
   staged. None ran concurrently with another test command, none was the full suite, and none was a
   mutation red-proof; gate 2 and gate 3 themselves each ran exactly once, after C3, as the block
   requires.
3. A throwaway sanity script and a digest-verification script were written under
   `.remedy-wt/f162-r2-worker/` (created fresh this round) to prove the module's comparator and
   refusal behaviour against DECISION F162 D2 before the test file was written; neither is committed
   and neither is a model or `claude`-binary call.

No other departure from the block's ordered commit sequence: no correction commit beyond the
declared split, no file touched outside the paths named per commit, no mutation red-proof, no full
suite run beyond gate 2's own selection, no `REMEDY_TEST_MAX_WORKERS`, no two test commands run at
once, no `claude` binary invoked, no container image pulled or run, no worktree of my own, and no
`gh pr merge`, `git checkout`/`git switch` away from the feature branch, branch creation, rebase,
amend, force-push, or `--no-verify`.

## For the operator, in plain sentences

This session turned last round's reviewed design into real code: a new module that describes what
a worker process may touch, in five separate categories, with three ready-made settings from
strict to permissive, and a rule that lets a project tighten its own limits but never loosen them
below what its adapter already requires. Every rule the design laid out — what a valid setting file
must contain, how the three ready-made settings compare to each other, and the exact wording of the
refusal when something tries to loosen a limit — now has a test proving it, including every way a
malformed setting file is rejected. None of this new code is wired into anything that actually runs
a worker yet; it is deliberately inert, policy math, by the design's own choice, so it can be
checked on its own before the next round plugs it into the two existing enforcement mechanisms.
Every check that ran this session passed, and nothing elsewhere in the repository was touched.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2a | deviated | split from the block's single C2, declared above; module, three built-ins and orphan entry, 356 insertions |
| C2b | deviated | split from the block's single C2, declared above; the parsing/built-in test half, 158 insertions |
| C3 | done | the tighten-only order's table tests and the refusal, 177 insertions, one path |
| C4 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | exit 0, `3831 passed, 2 skipped`, no FAILED/ERROR/`process(es) behind` |
| Gate 3 | done | `All checks passed!`, exit 0 |
| Gate 4 | done | `fail_count` 0; open id count `9`, matching the block exactly |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. The Open PR Gate, before any new branch.
3. Book round 2's verdict in the next round's first commit.
4. T002: enforcement per dimension through the exec guard and the tool sandbox, DECISION F162 D3.

Operator questions open: 3.
Open findings: 9 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450 and R-1464, owned by
F316; F162 takes none of them).
