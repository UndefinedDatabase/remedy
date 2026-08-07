# Handback — S1+S2 self-drive skill, R1 (worker)
Branch feature/selfdrive-skill, cut at df39c3fa. Open findings 0 · next free ID R-0207.

## Range
Review of df39c3fa..4a38253f (merge-base with main = df39c3fa).

## Commits
### 12e151df chore(selfdrive): sweep F080 candidate, open R1 state
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/selfdrive-r1-{1..11}.md | +457/-0 | 11 verified receipts |
| .agent/live_review.md | +54/-95 | R1 opened; D5/D6/D7; verdict PENDING |
| .agent/plan.md | +32/-41 | R1 goal, four-commit step, risks |
| .agent/context.md | +24/-28 | branch, scope, constraints |
| .agent/candidates.md | +3/-10 | F080 candidate swept (carrier empty) |
| docs/roadmap/STATUS_closure_protocol.md | +10/-0 | producer pitfall (d) |
### f681fb95 docs(selfdrive): add the one-session build protocol
| Path | +/- | Reason |
|---|---|---|
| docs/agents/self_drive_protocol.md | +124/-0 | new: roles, phases, G1-G8 |
| docs/README.md | +2/-0 | quick-find + Agent Conventions rows |
### 6976e7d7 feat(selfdrive): add build-remedy-self command and skill
| Path | +/- | Reason |
|---|---|---|
| .claude/skills/remedy-self-drive/SKILL.md | +60/-0 | new skill entry point |
| .claude/commands/build-remedy-self.md | +15/-0 | new slash command |
| .claude/README.md | +5/-1 | contents line + self-drive pointer |
### 4a38253f test(selfdrive): pin the protocol guardrails and registration
| Path | +/- | Reason |
|---|---|---|
| tests/test_agent_tooling.py | +37/-0 | 3 pins, append-only |

## External actions
- `gh pr list --state open ...` → exactly one: #184, feature/adr-0001-cycle-cap → main, isDraft false — gate shape matched; `gh pr merge 184 --merge --delete-branch` → merged; `git pull --ff-only` → 97bcefe0..df39c3fa (8 files); `git checkout -b feature/selfdrive-skill` at df39c3fa.
- `git push -u origin feature/selfdrive-skill` → `* [new branch]`, tracking set. No PR created (step block). No worktree, no force-push.

## Verification (raw; every command exit 0, none ran red)
- commit 1: `pytest tests/docs/ -q` 293 passed 0.19s · `tests/ui_server/test_dashboard_contract.py` 70 passed 3.02s · `tests/orchestration/test_test_runner.py` 51 passed 3.05s · `tests/regression/test_resource_safety.py` 21 passed 10.77s · `tests/cli/test_golden_path.py` 42 passed 15.26s
- commit 2: `pytest tests/docs/ -q` 293 passed 0.19s. commit 3: `pytest tests/test_agent_tooling.py -q` 7 passed, 1 skipped 0.03s.
- commit 4: `pytest tests/test_agent_tooling.py -q` 10 passed, 1 skipped 0.04s · `tests/cli/test_golden_path.py` 42 passed 15.31s. `git status --porcelain` after push → empty.

## Authored-text proofs
- `sha256sum selfdrive-r1-*.md`: all 11 digests equal their BEGIN-marker stamp on the FIRST save; no wrap recovery needed. Display-wrapped lines were rejoined before saving (r1-6 two table rows, r1-7 pair-2 rows, r1-8 `description:`); the matching hashes confirm each rejoin.
- `cmp` = 0 receipt vs applied file: r1-1→live_review.md, r1-2→plan.md, r1-3→context.md, r1-4→candidates.md, r1-6→docs/agents/self_drive_protocol.md, r1-8→SKILL.md, r1-9→build-remedy-self.md.
- r1-10 (.claude/README.md): FROM 0x, TO 1x — a true 0x/1x rewrite. r1-5 and r1-7 pairs 1+2: TO CONTAINS FROM verbatim (TO = FROM + appended row/paragraph), so FROM 0x is unattainable by construction and is NOT claimed; proof given instead is FROM 1x plus each TO-only addition exactly 1x — `A fourth, from the F080 R4 attempt` 1x, `| self-drive | …agents |` 1x, `| [self_drive_protocol.md](…) | One-session build discipline… |` 1x.
- r1-11: appended to tests/test_agent_tooling.py; `git diff --numstat` = `37 0`, no existing line touched; file ends with exactly one newline (hexdump-verified).

## Deviations & assumptions
- Only deviation: the 0x FROM proof for r1-5 / r1-7 (above) — nothing was reworded to reach a count. No PR created and no STATUS.md edit (D7). Nothing under packages/, apps/, scripts/ touched.

## Item status
| Item | Status | Reason |
|---|---|---|
| 0 Open PR Gate + branch | done | |
| 1 state + candidate sweep + pitfall (d) | done | 5 gates exit 0 |
| 2 protocol doc + docs index | done | gate exit 0 |
| 3 skill + command + .claude/README | done | gate exit 0 |
| 4 test pins | done | 2 gates exit 0 |
| 5 push + handoff | done | pushed; no PR by instruction |

## Next
Reviewer gates R1 against the committed diff df39c3fa..4a38253f.
