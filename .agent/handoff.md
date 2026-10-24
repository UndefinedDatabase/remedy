# Handoff — F162 round 1

## Session

SESSION 1 of feature F162 · round 1 · rounds so far 1. This session claimed F162, re-headed the
review record, booked F152's round 10 verdict, recorded DECISION F162 D1, and landed the findings
pass as a reviewed inventory before any code was authored; context self-assessment: the two prior
enforcers (the exec guard and the tool sandbox) and F152's isolation declaration cover more of the
feature's named dimensions than the feature file's own design prose credits them for, which is now
on record for T001's DECISION F162 D2 to read.

Fortschritt: ~8 % (findings pass landed · T001 to T003 open) — Schätzung.

## Range

Review of `39beac4e1`..`e7ff11ad1` (C1 to C2; C3 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 389436af8 F162 R1 C1: claim F162, book F152 R10, re-head the ledger, DECISION F162 D1
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r1.md` | +142/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/context.md` | +9/-9 | rewritten: scope, do-not-touch and constraints re-stated for F162 |
| `.agent/decisions.md` | +10/-0 | DECISION F162 D1 appended: the round's order (inventory, then T001-T003) |
| `.agent/live_review.md` | +19/-16 | re-headed at the F162 claim; F152 round 10's PASS verdict booked as the closing Gate entry |
| `.agent/plan.md` | +22/-11 | rewritten: Goal/Current Step/Next Steps to F162's round 1 |
| `docs/roadmap/STATUS.md` | +1/-1 | F162's line becomes `[~]` |

### e7ff11ad1 F162 R1 C2: the findings pass, every place a worker process's limits are set or could be
| Path | +/- | Reason |
|---|---|---|
| `.agent/f162_inventory.md` | +348/-0 | NEW FILE — the read-only inventory of every dimension's current enforcer, platform reach, container tooling, evidence/doctor precedent and the T001 naming check, each sentence citing `path:line` at `39beac4e1` or a command this session ran |

### (this commit) F162 R1 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, checked before any
write (the Open PR Gate). No pull request open, so no merge was needed. `git checkout -b
feature/f162-sandbox-profiles` from `main` at `39beac4e1`, run once at the branch's creation. No
`gh pr create`, `gh pr merge`, `git worktree` command, or stash entry touched by this session. No
`claude` binary invoked; no model/provider call of any kind this round. `git push -u origin
feature/f162-sandbox-profiles` runs once, immediately after this commit, per the block's push
discipline; its real outcome is reported in the session reply, not in this file.

## Verification

**Gate 1.** After C2, `git status --porcelain` from the primary checkout: empty output, exit 0.
Then `python3 .remedy-wt/f162-r1/prep/verify.py .`:
```
True	389436af8 single parent equal to the commit before it
True	389436af8 insertions 203 under 500 (or the handoff alone)
True	e7ff11ad1 single parent equal to the commit before it
True	e7ff11ad1 insertions 348 under 500 (or the handoff alone)
True	every commit carries a F162 R1 Cn subject: 2 of 2
True	on feature/f162-sandbox-profiles
True	C1 paths exactly [...]: [...] (six paths, exact match)
True	C1 .agent/authored/f162-r1.md equals c1-.agent__authored__f162-r1.md
True	C1 .agent/context.md equals c1-.agent__context.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 docs/roadmap/STATUS.md equals c1-docs__roadmap__STATUS.md
True	C2 paths exactly ['.agent/f162_inventory.md']: ['.agent/f162_inventory.md']
True	C2 .agent/f162_inventory.md holds no machine path
True	C2 .agent/f162_inventory.md has 348 lines, under 400
absent	C3
True	the saved block equals block.md
ALL True
```
Every line `True` (C3 correctly `absent`, not yet committed when this gate ran); last line
`ALL True`.

**Gate 2.** `python3 .remedy-wt/f162-r1/prep/run_selection.py . .remedy-wt/f162-r1-worker/selection-output.txt`,
run once from the primary checkout:
```
paths 82
exit 0
3765 passed, 2 skipped in 29.02s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
`exit 0`, no `FAILED` or `ERROR` line, no line containing `process(es) behind`. Both `SKIPPED` lines
reported verbatim, as required.

**Gate 3.** `python3 -m apps.cli.main integrity check --json`, run once from the primary checkout:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass`.

**Gate 4.** `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`,
run once from the primary checkout: `9`. Exactly the block's named count; the ids themselves (read
separately, same function): `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448',
'R-1450', 'R-1464']`, every one owned by F316 per the re-headed ledger's own paragraph.

## Authored-text proofs

C1's six byte copies (`.remedy-wt/f162-r1-worker/c1_copy.py`) were each proved byte-equal to their
prepared `c1-` file immediately after copying, by `.remedy-wt/f162-r1-worker/c1_prove.py`, which
read `True` for all six targets and `True` for "authored equals block.md". The authored block's own
proof: `.agent/authored/f162-r1.md` is 142 lines (`wc -l`-equivalent line count) with sha256
`803c557120c3d3e9fe1af77030b3759a2588faa391644148a20f7171817826d4`, identical to `block.md`'s own
sha256 — the same digest `digests.txt` names for both prepared files. Gate 1's `verify.py` run
independently re-confirmed every `C1 ... equals c1-...` line `True`.

## Deviations & assumptions

1. This round's `.agent/f162_inventory.md` is new reviewer-facing content this session authored
   itself (not a reviewer-authored `c1-` file), so it carries no byte-identity proof against a
   prepared file; `verify.py`'s own checks for C2 are the no-machine-path and under-400-line checks
   instead, both `True` above.
2. Two commands this session ran joined `cd <repository root>` to a second command with `&&`
   (the C1 and C2 `git commit` invocations, and gate 3's `integrity check` call) — a shape the
   block's constraints ask to avoid in favour of `git -C`/absolute-path forms. Each ran from the
   session's own default working directory, which was already the repository root, so no relative
   path resolved differently than intended; all three completed with the exact expected output
   before anything else depended on them, and no further command used that joined form. No commit,
   decision or gate reading rests on an ambiguous path as a result.
3. Gate 4 was run twice: once through a `python3 -I -c` subprocess with `sys.path` set explicitly
   (to also print the nine ids themselves for this file's own record), then once more exactly as
   the block's literal command, from the session's default working directory. Both readings agree
   at `9`; the second, literal run is the one Gate 4 above reports as the compliant reading.

No other departure from the block's ordered commit sequence: no split, no correction commit, no
file touched outside the paths named per commit, no mutation red-proof, no full suite run, no
`REMEDY_TEST_MAX_WORKERS`, no two test commands run at once, no `claude` binary invoked, no
container image pulled or run, no worktree of my own, and no `gh pr merge`, `git checkout`/`git
switch` away from the feature branch, branch creation beyond C0, or force-push.

## For the operator, in plain sentences

This session claimed the next feature on the roadmap, which gives each kind of worker a declared,
testable limit on what it may touch — its files, its network reach and how much of the machine it
may use. Before writing any of that, the session first read the whole existing tree to find out
what already limits a worker today, because two separate mechanisms already exist and a new rule
that ignored them would either duplicate work or make a promise nothing actually keeps. That
reading is written down as a committed record for a human to check before any of the new code is
built. It found that one kind of worker already runs inside a strong, kernel-enforced boundary,
while the others only get a time limit and a cleaned set of settings, with no boundary around their
files or their network access at all. It also found that a planned safety feature for isolated,
offline deployments already assumes this feature will exist and behave a certain way, so the two
must be designed together. The previous feature's closing paperwork was also filed in this
session's first commit, as the process requires. No worker tool and no paid model call ran during
this session; every check that did run passed. The next session turns this reading into the actual
rule and its first tests.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch `feature/f162-sandbox-profiles` created from `main` at `39beac4e1`, confirmed before any write |
| C1 | done | six files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2 | done | `.agent/f162_inventory.md` committed, 348 lines, read-only investigation, no other file touched |
| C3 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | exit 0, `3765 passed, 2 skipped`, no FAILED/ERROR/`process(es) behind` |
| Gate 3 | done | `fail_count` 0, all six checks `pass` |
| Gate 4 | done | open id count `9`, matching the block exactly |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. The Open PR Gate, before any new branch.
3. Book round 1's verdict in the next round's first commit.
4. T001: the profile schema, the built-ins and the tighten-only comparator, DECISION F162 D2.

Operator questions open: 3.
Open findings: 9 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450 and R-1464, owned by
F316; F162 takes none of them).
