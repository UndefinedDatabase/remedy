# Handback — F085 Sandbox hardening (stage 1) · Runde 38 (R37 record + DECISION F085 D3)

Branch: feature/f085-sandbox-hardening · Base SHA: c3201976 · HEAD: this commit (C3).
Fortschritt: ~74 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R37
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 durch
DECISION F085 D3 ab R39 entsperrt · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.
## Range
Review of c3201976..HEAD.

## Commits

### c8a379f1 docs(f085): save the R38 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r38.md | +284/-0 | C0a — block saved byte-for-byte |

### b9d5050b docs(f085): mirror the R38 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +249/-294 | C0b — full replacement with the same bytes |

### 3b915e3c docs(review): record the R37 PASS and register R-0528 and R-0529
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +65/-0 | C1 — RECORD6 appended: R37 gate entry, R-0528, R-0529 |

### 275a294e docs(f085): rule the extra_env overlay for the test-class seam
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +38/-0 | C2 — DEC6 appended as DECISION F085 D3 |
| .agent/plan.md | +11/-12 | C2 — PLANF6A->PLANT6A and PLANF6B->PLANT6B applied |

### C3 (this commit) docs(f085): rewrite the handback for R38
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | full rewrite | C3 — this handback; a handoff cannot table the commit that writes it (R-0149). Its own insertions are reported in the round report. |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions
No worktree was created — this round ordered no destructive check; `git worktree list` = 1 line throughout. `git push -u origin feature/f085-sandbox-hardening` — outcome in the round report (run after this commit). No PR, no merge, no gh command.

## Verification
G1 STATE — `.agent/STOP` re-read from disk before C0a and again before C3; absent both times (`ls` exit 2, "No such file or directory"). `git status --porcelain` = 0 lines at round start and after every commit. `git worktree list` = 1 line throughout: `/home/decodeux/Repos/remedy 275a294e [feature/f085-sandbox-hardening]`.
G2 TRANSPORT — the committed `.agent/authored/f085-r38.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's own `.remedy-wt/f085-r38.md` are all five byte-EQUAL, measured disk-to-disk after C0b, not by digest fallback. sha256 5fa4d096e45014a54d93d7f27efe176adc4c85a1f10ebdcf6a649c6620cb5090 · 18154 B · 284 lines · 12 marker lines. Region digests, trailing newlines included: 1-100 4568e657… (6223 B), 101-200 8bdbaafb… (7342 B), 201-300 7baf119c… (4589 B), 301-end EMPTY (0 B — the file ends at line 284). Every one measured; none computed by hand.
G3 APPEND SHAPE — C1 3b915e3c on `.agent/live_review.md`: pre-commit blob 397527 B is a byte-exact PREFIX of the 402603 B post-commit file; remainder 5076 B = exactly one blank line plus RECORD6; RECORD6 is an exact suffix; its first line occurs 1x among the 65 lines the diff ADDS; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 17x; `git show --numstat` = 65 0 .agent/live_review.md. C2 275a294e on `.agent/decisions.md`: pre-commit blob 356103 B is a byte-exact PREFIX of the 358646 B post-commit file; remainder 2543 B = exactly one blank line plus DEC6; DEC6 is an exact suffix; its first line occurs 1x among the 38 lines the diff ADDS; 0 marker lines, BEGIN substring 1x; `git show --numstat` = 38 0 .agent/decisions.md.
G4 ARITHMETIC — base c3201976: 142 registered / 24 done / 0 landed, 118 open, max registered R-0527, max resolved R-0527 — the block's base reading, reproduced. HEAD: 144 / 24 / 0, 120 open, max registered R-0529, max resolved R-0527. Registered symmetric difference {R-0528, R-0529}; done symmetric difference empty; landed symmetric difference empty; 0 duplicate ids; 0 resolutions naming an unregistered id; maximum id R-0529; next free id R-0530 (moved from R-0528).
G5 THE PLAN, measured at HEAD after C2 — PLANF6A 0x / PLANT6A 1x; PLANF6B 0x / PLANT6B 1x. `.agent/plan.md` is 45 lines against the 50-line AGENTS.md cap and still carries `## Goal` 1x and `## Next Steps` 1x. 0 lines match `^(BEGIN|END)-[A-Z0-9]+$`. `git show --numstat` for C2 = 38 0 .agent/decisions.md and 11 12 .agent/plan.md.
G6 SUITES — each run in the PRIMARY checkout /home/decodeux/Repos/remedy, never a worktree (R-0518). `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` exit 0, `159 passed in 20.99s` — no R-0518 red, `-rf` printed no failure section. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, `42 passed in 22.34s`. Both reproduce the block's base readings.
G7 HYGIENE — `git diff --name-only c3201976..HEAD` measured BEFORE C3 holds exactly `.agent/authored/f085-r38.md`, `.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and nothing else — the declared change set minus `.agent/handoff.md`, which C3 writes. Per-commit insertions before C3: 284, 249, 65, 49 — none exceeds 500. Every commit has exactly one parent (c8a379f1<-c3201976, b9d5050b<-c8a379f1, 3b915e3c<-b9d5050b, 275a294e<-3b915e3c). `git reflog -10` holds only `commit:` entries.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r38.md` by its BEGIN/END marker pair; none was retyped or taken from the prompt; each FROM was asserted to match exactly once before the replace; 0 marker lines reached any target file. Transport is disk-to-disk byte equality (G2), not a digest fallback.
- RECORD6 — append to `.agent/live_review.md`, no FROM; 5075 B, 64 lines; proved as an append by G3.
- DEC6 — append to `.agent/decisions.md`, no FROM; 2542 B, 37 lines; proved as an append by G3.
- PLANF6A->PLANT6A — containment test OUTPUT: `TO contains FROM: false` — REWRITE, so the pair is owed and given the FROM 0x / TO 1x reading. FROM occurred exactly 1x in `.agent/plan.md` at c3201976; at HEAD FROM 0x, TO 1x.
- PLANF6B->PLANT6B — containment test OUTPUT: `TO contains FROM: false` — REWRITE, same reading. FROM occurred exactly 1x in `.agent/plan.md` at c3201976; at HEAD FROM 0x, TO 1x.

Open findings: 120 (118 + R-0528 + R-0529 registered; nothing resolved this round).

## Deviations & assumptions
The commit sequence executed is exactly the block's Bundle in order: C0a, C0b, C1, C2, C3 — five commits, no extra, none dropped, no reordering. Every slice was applied byte-verbatim as written; none was edited.
DECLARED DEFECT IN THE BLOCK'S OWN TEXT, applied as written and not repaired (constraint 9): RECORD6's R-0528 paragraph asserts that `.agent/last_block.md` "hashes 208ad9d3 at 483975b3 and c8efc5c0 at 857ca31a and every commit after it". Measured by sha256 over `git show <sha>:.agent/last_block.md`: 208ad9d3 at 483975b3; c8efc5c0 at 857ca31a and at c3201976; 5fa4d096 at b9d5050b and at HEAD. The universal clause "every commit after it" is therefore FALSE from b9d5050b onward — b9d5050b is this round's own C0b, and C0b precedes C1, so the sentence was already false at the instant it landed. That is the same R-0417 staleness class R-0528 itself registers, recurring inside the paragraph that registers it; the fourth consecutive round in which the constraint-8 report produced the finding.
CONSTRAINT-8 SWEEP, naming what was re-read and reporting the measurement: all five files this round edited were re-read at HEAD after C2 — `.agent/authored/f085-r38.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`. Beyond the declaration above, RECORD6's remaining quotations each name the SHA they were measured at (the R37 constraint at e2b23b33 and 857ca31a, the `Done: R-0527` paragraph at 75feb987, both readings at c3201976), so neither C0b nor C1 falsifies them. DEC6's factual claims were re-measured at c3201976 and all hold: `ci_run.py` line 78 is `env = {**os.environ, PYTEST_TIMEOUT_ENV_VAR: str(timeout_sec)}`, line 79 is a `subprocess.run` with no capture (it streams), `builder_bridge.py` line 219 is `env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}`, and `exec_guard.py` offers `extra_env_keys` at lines 491/523 and no `extra_env`. DEC6's one claim about a file C2 itself rewrites names its SHA — "`.agent/plan.md` at c3201976 recorded this blocker for `builder_bridge.py` alone" — and was true there, so C2 does not falsify it.
LENGTH, measured with `wc -l` on the draft before writing the file: 87 lines against the 60-line cap that a 5-commit bundle carries, so a DECISION D15 stated-cause overage IS claimed. The mandated content that causes it: five per-commit tables plus the item-status table, seven gate entries G1-G7 carrying their real measurements, four authored-text pair proofs, the two texts the block orders repeated verbatim (the 4-line Fortschritt line and the 8-line R39/R40 note) and the two declarations above. No section was dropped and no transcript was padded.

## Next
The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). R38's own verdict is NOT a §4.13 terminator: this branch continues, so the next reviewed round records R38's gate entry in `.agent/live_review.md`.

Carried verbatim from the block:

  R39 implements DECISION F085 D3 in `packages/orchestration/exec_guard.py`: an
  `extra_env` mapping on `test_command_exec_policy` and `run_guarded_test_command`
  whose entries become the scrub SOURCE overlay and whose keys join the allowlist,
  with `scrub_child_env` keeping `FORBIDDEN_ENV_KEYS` as the floor, plus the tests
  that pin the set, the floor and the untouched allowlist. No call site is migrated
  in R39. R40 then migrates `packages/orchestration/ci_run.py`, which still owes its
  own DECISION on where the stage's output goes: at c3201976 the spawn at line 79
  streams straight to the console while the seam captures.
