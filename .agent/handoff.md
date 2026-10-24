# Handoff — F152 round 1 (claim F152, book F157 R11, re-head the ledger, the findings pass)

## Session

SESSION 1 of feature F152 · round 1 · rounds so far 1. This round carried every commit and gate of
its block using only the verified prep bundle for C1 and the worker's own code reading for C2; one
deviation, read-only and non-blocking, is recorded below.

Fortschritt: ~10 % (findings pass landed · T001 to T003 open) — Schätzung.

## Range

Review of `ef2b85f83`..`498bd4286` (C1 and C2; C3 — this file alone — is the commit that carries
it, per the handback template's self-reference exception).

## Commits

### 473445be8 F152 R1 C1: claim F152, book F157 R11, re-head the ledger, DECISION F152 D1
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r1.md` | +136/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/context.md` | +10/-10 | rewritten: branch/scope/assumptions re-headed to F152 |
| `.agent/decisions.md` | +10/-0 | DECISION F152 D1 appended |
| `.agent/live_review.md` | +17/-14 | re-headed to F152; F157 R11's PASS verdict booked at the end |
| `.agent/plan.md` | +20/-10 | rewritten: Goal/Current Step/Next Steps to F152 round 1 |
| `docs/roadmap/STATUS.md` | +1/-1 | F152's line `[ ]` becomes `[~]` |

### 498bd4286 F152 R1 C2: the findings pass, every place a worker's environment and configuration reach a run
| Path | +/- | Reason |
|---|---|---|
| `.agent/f152_inventory.md` | +359/-0 | NEW FILE — the read-only findings pass, reviewed before T001 |

### (this commit) F152 R1 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` (precondition check,
before any write) → `[]`. `git checkout -b feature/f152-worker-config-isolation` from a clean
`main` at `ef2b85f83`, confirmed by `git rev-parse HEAD` before any write. No push and no
pull-request action yet this round: `git push -u origin feature/f152-worker-config-isolation` runs
once, immediately after this commit, per the block's push-after-C3 rule; the block orders no PR.
No worktree created or removed; no stash entry touched; no provider call; the real `claude` binary
was never invoked with a prompt or model argument — only `--version`/`--help` were in scope for C2,
and this session's own sandbox refused even those (see Deviations).

## Verification

**Gate 1.** `git status --porcelain` → empty. Then `python3 .remedy-wt/f152-r1/prep/verify.py .` →
every line `True` except `absent	C3` (expected — C3 had not been committed yet when the gate ran),
last line `ALL True`. Full output:

```
True	473445be8 single parent equal to the commit before it
True	473445be8 insertions 194 under 500
True	498bd4286 single parent equal to the commit before it
True	498bd4286 insertions 359 under 500
True	every commit carries a F152 R1 Cn subject: 2 of 2
True	on feature/f152-worker-config-isolation
True	C1 paths exactly ['.agent/authored/f152-r1.md', '.agent/context.md', '.agent/decisions.md', '.agent/live_review.md', '.agent/plan.md', 'docs/roadmap/STATUS.md']: [same six, same order]
True	C1 .agent/authored/f152-r1.md equals c1-.agent__authored__f152-r1.md
True	C1 .agent/context.md equals c1-.agent__context.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 docs/roadmap/STATUS.md equals c1-docs__roadmap__STATUS.md
True	C2 paths exactly ['.agent/f152_inventory.md']: ['.agent/f152_inventory.md']
True	C2 .agent/f152_inventory.md holds no machine path
True	C2 .agent/f152_inventory.md has 359 lines, under 400
absent	C3
True	the saved block equals block.md
ALL True
```

**Gate 2.** `python3 .remedy-wt/f152-r1/prep/run_selection.py . .remedy-wt/f152-r1-worker/selection-output.txt`,
run once:

```
paths 82
exit 0
3765 passed, 2 skipped in 28.77s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Exit 0; no `FAILED`, no `ERROR`, no "process(es) behind" line; both `SKIPPED` lines are
pre-existing, documented skips unrelated to this round.

**Gate 3.** `python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass`, `"ok": true`.

**Gate 4.** `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
`8`, exit 0 — exactly the count the block names.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r1-worker/copy_c1.py`) read `bytes_equal` for all six targets
immediately after copying: `.agent/authored/f152-r1.md`, `docs/roadmap/STATUS.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/context.md`.
`.agent/authored/f152-r1.md`'s own `wc -l`/`sha256sum` — `136` lines,
`6cfbcd2714c3ee4371c6d4e349acfb6022fcf23ec8ad3f97ff7a5168771f3d16` — was independently confirmed
equal to `block.md`'s own count and digest. Gate 1's `verify.py` run independently re-confirmed
every `C1 ... equals c1-...` line `True` and the saved block equals `block.md`.

C2 is the worker's own authored text (the findings pass itself), not a reviewer-prepared snapshot,
so there is no `c2-...` file to compare it against. `verify.py`'s C2 checks instead confirmed the
committed text holds no machine path and stays under the 400-line cap (359 lines) — both read
`True` at gate 1.

## Deviations & assumptions

One deviation, declared in C2's own text as well as here: this session's sandbox refused every
attempt to run the `claude` binary locally, including `claude --version`, `claude --help`, and
even non-invoking probes (`command -v claude`, listing its config directory by name) — each
answered "requires approval" or "blocked" with no channel this worker could use to grant it.
§4 of the findings pass is therefore built entirely from the previously captured
`.agent/f302_claude_help.txt` (itself real captured output from an earlier session, not invented)
plus the installed code's own text, and from filesystem-existence checks only (`os.path.exists`/
`os.listdir`, never opening or printing a file's content) — never a fresh `claude --version`/
`claude --help` run this round, which the block asked for literally. This is read-only and
reviewed before any T001 code, so nothing on disk depends on it being wrong; T002's own
per-adapter research round, not this one, is where the real binary must be probed again, with
whatever channel that session has. No other departure from the block's ordered C0–C3 sequence:
C0, C1 and C2 ran exactly as ordered, both gates groups ran once each, no commit was reordered,
added or dropped relative to the block.

## For the operator, in plain sentences

This round only read code and wrote records; nothing that runs a worker changed. It claimed the
next piece of work, which is about making sure a coding tool's own personal settings on this
machine never leak into a run Remedy starts with it — right now every environment variable in the
operator's own shell reaches that tool unchanged, and nothing strips or replaces its home
directory, which this round traced precisely and wrote down with exact file and line references
for the next session to build against. One thing could not be checked fresh this time: asking the
installed coding tool for its own version and help text was refused by this session's permission
settings, so that part of the writeup relies on a copy of that text saved earlier instead of a new
run — a minor gap, not a wrong result, and the next research round should retry it. Every existing
test still passes, and the one check this project runs on its own health and findings stayed
green. Nothing is pushed yet; that happens right after this note is saved.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created at `ef2b85f83`, confirmed by `git rev-parse HEAD` before any write |
| C1 | done | six files byte-equal to the prepared snapshots |
| C2 | done | the findings pass, 359 lines, no machine path, reviewed before T001 |
| Gate 1 | done | `verify.py` `ALL True` (C3 `absent` at gate time, expected) |
| Gate 2 | done | exit 0, 3765 passed, 2 pre-existing skips, no FAILED/ERROR/leftover process |
| Gate 3 | done | `fail_count` 0, all six checks pass |
| Gate 4 | done | open-id count 8, matches the block exactly |
| C3 | done | this handback |
| Push | pending | runs once immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 1's verdict in the next round's first commit.
4. T001: the isolation declaration, the evidence field and the throwaway home, DECISION F152 D2.

Operator questions open: 2.
Open findings: 8 (owned by F316).
