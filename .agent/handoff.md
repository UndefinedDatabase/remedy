# Handback — amend0820-gate-autonomy · session of 2026-08-20 (Open PR Gate, CLEAR)

Branch `main` at 86555049. This session was an ORDINARY interactive session, not the self-drive
command, and it executed the operator amendment amend0820-gate-autonomy end to end: it unblocked
F085's merge, merged it, and then made the block that stopped three previous sessions unable to
recur. No open PR remains.

Fortschritt: F085 ist gemerged (PR #204), die Gate-Autonomie ist gemerged (PR #205), und der
Arbeitsstand steht wieder bei "nächstes Feature nach Rule A5 beanspruchen". Der rote CI-Check
hatte EINE Ursache, kein Stufen-Budget: die Sandbox-Posture des Guards sperrte den eigenen
Testserver aus. Die Sitzungen können ab jetzt `gh run`, `gh api` und `gh pr checks` lesen, und
ein roter Lauf ist laut AGENTS.md ausdrücklich Arbeitsauftrag statt Abbruchgrund.

## Phase 0 — probe, run this session

- `git status --porcelain` EMPTY; branch was `feature/f085-sandbox-hardening`; `.agent/STOP` absent.
- `gh pr list --state open`: exactly ONE — #204, `feature/f085-sandbox-hardening` → `main`.
- `gh pr checks 204` → `ci` FAILURE, 42m51s, run 32301614177. This session COULD read it: the
  operator granted `gh run` in the prompt itself.

## What the red actually was

Run 32301614177 failed 62 tests across `fast` and `standard`, every one of them `[Errno 111]
Connection refused` against a server whose own log line said `ready`. `DENIED_NETWORK_ENV` set
`NO_PROXY=""`, so a guarded `test`-class child's HTTP request to a server IT HAD JUST STARTED went
to the closed discard-port proxy. That is how the runtime, smoke and CLI suites judge readiness.
No stage tripped its budget — `fast` 887.5 s, `standard` 1617.5 s — so the standing budget-kill
hypothesis from the previous handback is REFUTED, not merely unconfirmed.

A 63rd failure surfaced once the 62 were gone: the deny test's own CONTROL child. It is spawned
with plain `subprocess.run`, which inherits the pytest process's environment — and in CI that
process is itself a guarded child, so the "unguarded" control was guarded. It had been failing for
that reason all along, hidden behind the louder 62.

## Verification

| Gate | Result |
|------|--------|
| CI run 32338830449 (F085 branch) | SUCCESS — fast, standard, ui, smoke, budgets all passed |
| CI run 32340783256 (amendment branch) | SUCCESS |
| `tests/docs/` | 295 passed |
| `tests/cli/test_golden_path.py` | 42 passed |
| `tests/orchestration/test_exec_guard.py` under `run_guarded_test_command` | 45 passed |
| previously-red runtime/CLI/smoke suites, under the guard | 129 + 197 passed |
| `ruff check .` | 26 findings, identical to the base — no Python added by the amendment branch |

Both fixes are red-controlled: restore the empty `NO_PROXY` and the new exemption test fails;
drop the control's env argument and the deny test fails with the exact CI message.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Read and classify the red CI run | done | class (a), the guard's own posture |
| Repair on the F085 branch | done | f882c727, 4e926506 |
| Merge #204 | done | 68155931, branch deleted |
| Permissions for gh run / gh api / gh pr checks | done | tracked `.claude/settings.json` |
| AGENTS.md Open PR Gate exception | done | PR #205, merged at 86555049 |
| State files refreshed | done | this file and `.agent/plan.md` |

Open findings: 152, next free id R-0570 — carried from the R74 record, NOT re-measured here.
`.agent/candidates.md` holds TWO entries and stays non-empty.

## Deviations, declared

The three `gh` grants went into the TRACKED `.claude/settings.json`, not into
`.claude/settings.local.json` where the existing `gh pr` grants live. That file is gitignored
(`.gitignore:216`) AND read-denied by the repo's own settings, so it could neither be read nor
reach a fresh checkout. Allow-rules union across settings files, and nothing was removed. This
session ran in bypass-permissions mode, so it could NOT observe the grants taking effect; the
first session that is not in that mode is the real test.

## Next

1. Phase 1 rule 1 FIRST: re-read `.agent/STOP` from disk.
2. The Open PR Gate is CLEAR — zero open PRs. Claim the next feature by Rule A5, whose FIRST
   reviewed round registers or resolves BOTH `.agent/candidates.md` entries and empties that file.
