# Handoff — F152 round 2 (book round 1, DECISION F152 D2 and Q26, the claude-cli isolation record)

## Session

SESSION 1 of feature F152 · round 2 · rounds so far 2. This round carried every commit and gate of
its block using the verified prep bundle for C1 and the worker's own research, read from local
evidence only, for C2; no deviation this round.

Fortschritt: ~20 % (findings pass and isolation record landed · T001 to T003 open) — Schätzung.

## Range

Review of `a85f2007a`..`3e14f201e` (C1 and C2; C3 — this file alone — is the commit that carries
it, per the handback template's self-reference exception).

## Commits

### 3ead918aa F152 R2 C1: book round 1, DECISION F152 D2 and operator question Q26
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r2.md` | +115/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | DECISION F152 D2 appended |
| `.agent/live_review.md` | +2/-0 | F152 round 1's PASS verdict booked at the end |
| `.agent/operator_questions.md` | +10/-0 | Q26 appended, recommendation executed |
| `.agent/plan.md` | +11/-11 | rewritten: Current Step/Next Steps/Risks to round 2 |

### 3e14f201e F152 R2 C2: the claude-cli worker isolation record and its index rows
| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +8/-1 | quick-find row, folder paragraph and table row for the new record |
| `docs/adr/0002-claude-cli-worker-isolation.md` | +167/-0 | NEW FILE — the claude-cli isolation research record, written from local evidence |

### (this commit) F152 R2 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh` command this round: the Open PR Gate is not ordered until the next round's start (Next, below). No worktree created or removed; no stash entry touched; no provider call; the real `claude` binary was never invoked — the block forbids running it or fetching the web this round, and the record is written entirely from `.agent/f302_claude_help.txt` (captured earlier), the inventory and the installed code's own text. No push yet: `git push origin feature/f152-worker-config-isolation` runs once, immediately after this commit, per the block's push-after-C3 rule. The block orders no pull request.

## Verification

**Gate 1.** `git status --porcelain` → empty. Then
`python3 .remedy-wt/f152-r2/prep/verify.py .` → every line `True` except `absent	C3` (expected — C3
had not been committed yet when the gate ran), last line `ALL True`. Full output:

```
True	3ead918aa single parent equal to the commit before it
True	3ead918aa insertions 148 under 500
True	3e14f201e single parent equal to the commit before it
True	3e14f201e insertions 175 under 500
True	every commit carries a F152 R2 Cn subject: 2 of 2
True	on feature/f152-worker-config-isolation
True	C1 paths exactly ['.agent/authored/f152-r2.md', '.agent/decisions.md', '.agent/live_review.md', '.agent/operator_questions.md', '.agent/plan.md']: [same five, same order]
True	C1 .agent/authored/f152-r2.md equals c1-.agent__authored__f152-r2.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/operator_questions.md equals c1-.agent__operator_questions.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths exactly ['docs/README.md', 'docs/adr/0002-claude-cli-worker-isolation.md']: [same two, same order]
True	C2 docs/README.md equals c2-docs__README.md
True	C2 docs/adr/0002-claude-cli-worker-isolation.md holds no machine path
True	C2 docs/adr/0002-claude-cli-worker-isolation.md has 167 lines, under 250
True	C2 the record carries the ordered status line
True	C2 the record marks VERIFIED and UNVERIFIED
absent	C3
True	the saved block equals block.md
ALL True
```

**Gate 2.** `python3 .remedy-wt/f152-r2/prep/run_selection.py . .remedy-wt/f152-r2-worker/selection-output.txt`,
run once:

```
paths 82
exit 0
3765 passed, 2 skipped in 28.62s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Exit 0; no `FAILED`, no `ERROR`, no "process(es) behind" line; both `SKIPPED` lines are
pre-existing, documented skips unrelated to this round (identical counts to round 1's reading,
since this round changed only `docs/` and `.agent/` paths).

**Gate 3.** `python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass`, `"ok": true`.

**Gate 4.** `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
`8`, exit 0 — exactly the count the block names.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r2-worker/copy_c1.py`) read `EQUAL` for all five targets
immediately after copying: `.agent/authored/f152-r2.md`, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/operator_questions.md`, `.agent/plan.md`.
`.agent/authored/f152-r2.md`'s own newline count and sha256 — `115` lines,
`87a45eb80f5424897057fd1b162262fc025ea14f851441c3f53493971aeb1ff4` — were independently confirmed
equal to `block.md`'s own count and digest by a direct byte comparison. Gate 1's `verify.py` run
independently re-confirmed every `C1 ... equals c1-...` line `True` and the saved block equals
`block.md`.

C2's `docs/README.md` copy (the same script's successor step) read `EQUAL` against
`c2-docs__README.md` immediately after copying. `docs/adr/0002-claude-cli-worker-isolation.md` is
the worker's own authored text (the isolation research record itself), not a reviewer-prepared
snapshot, so there is no `c2-...` file to compare it against. `verify.py`'s C2 checks instead
confirmed the committed text holds no machine path, stays under the 250-line cap (167 lines),
carries the ordered status line and marks both VERIFIED and UNVERIFIED claims — all read `True` at
gate 1.

## Deviations & assumptions

None. C0 (none ordered this round — the branch was already current), C1 and C2 ran exactly as the
block ordered: C1's five byte copies, C2's `docs/README.md` byte copy plus the worker-authored
record under 250 lines in the ordered section sequence. Both gate groups ran once each, under the
constraints (no mutation red-proofs, no full suite, no `REMEDY_TEST_MAX_WORKERS`, no two test
commands at once, no `claude` binary invoked, no web fetch, no credential file read or quoted). No
commit was reordered, added or dropped relative to the block.

## For the operator, in plain sentences

This round wrote down, in one place, exactly what is known and not known about how the coding tool
Remedy uses for a worker keeps its own personal settings out of a run, using only a saved copy of
that tool's help text and this project's own source code, because this session's permission
settings still refuse to run that tool directly. The write-up marks every single claim as either
confirmed from a specific line of that saved text, or as still unconfirmed, and it lists exactly
which unconfirmed points need a real run of the tool to settle, and which can already be checked
today without one. It also found and wrote down a real tension worth the operator knowing about
before the next round builds anything: making the tool forget the operator's personal settings by
giving it a fresh, empty home directory would, under this project's own existing safety rules, also
strip out the one way the tool's login could be carried along as a plain setting, so a naive
version of that idea would leave the tool unable to prove who it is at all. The write-up proposes a
way around that tension, but it is a proposal for the next round to accept or change, not a
decision already acted on. The earlier open question about letting a session run the real tool
once, for one small paid proof, is still open and unchanged. Every existing test still passes, and
the one check this project runs on its own health and findings stayed green. Nothing is pushed yet;
that happens right after this note is saved.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to the prepared snapshots |
| C2 | done | `docs/README.md` byte-equal to the prepared copy; the isolation record authored, 167 lines, no machine path, VERIFIED/UNVERIFIED marked throughout |
| Gate 1 | done | `verify.py` `ALL True` (C3 `absent` at gate time, expected) |
| Gate 2 | done | exit 0, 3765 passed, 2 pre-existing skips, no FAILED/ERROR/leftover process |
| Gate 3 | done | `fail_count` 0, all six checks pass |
| Gate 4 | done | open-id count 8, matches the block exactly |
| C3 | done | this handback |
| Push | pending | runs once immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 2's verdict in the next round's first commit.
4. T001: the declaration, the evidence field and the throwaway home, DECISION F152 D3.

Operator questions open: 3.
Open findings: 8 (owned by F316).
