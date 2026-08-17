# Handback — F085 Sandbox hardening (stage 1) — R28

Feature F085 · Round R28 · Branch `feature/f085-sandbox-hardening`
Base 07b1ba25 · pre-C4 HEAD e78c7027 · open findings 118 · next free id R-0519
Fortschritt: ~85 % (T001 gebaut · R13-R27 PASS · T002a KOMPLETT · T002b: Seam
gebaut, `test_runner` + `autorun` + `test_execution_service` migriert · T002b
Restprüfung, T002c-d, T003 offen) — Schätzung.

## Range

Review of 07b1ba25..HEAD — 6 commits: C0a C0b C1 C2 C3 C4.

## Commits

### ebf2c9b3 docs(f085): save the R28 step block — C0a
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r28.md | +398/-0 | R28 block verbatim; 26 marker lines, 13 pairs |

### b8ee66ec docs(f085): mirror the R28 block into last_block — C0b
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +334/-165 | written from the COMMITTED blob, not the worktree |

### d3e84dda docs(review): record the R27 PASS, resolve R-0517 and register R-0518 — C1
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +71/-0 | RECORD1 appended: R27 entry, R-0517 done, R-0518 new |

### 6186ec31 docs(f085): advance the plan to R28 — C2
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8/-7 | PLANF→PLANT over Current Step + Next Steps |

### e78c7027 feat(f085): spawn the isolated test process under the exec guard child plan — C3
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/test_execution_service.py | +15/-2 | S1 import, S2 `plan_child_spawn` |
| tests/orchestration/test_test_execution_service.py | +24/-0 | S3 `resource`, S4 `pytest`, S5 RLIMIT_CORE proof |

### C4 — this handback (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured in the round report | a handoff cannot measure the commit that writes it |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions

`git worktree add .remedy-wt/r28-g8 HEAD --detach` → created at e78c7027, G8 only; `git worktree
remove --force` + `git worktree prune` → `git worktree list` one line. `git push -u origin
feature/f085-sandbox-hardening` → after C4. No `gh` command, no PR, no merge.

## Verification

G1 `ls -la .agent/STOP` exit 2 `No such file or directory`, read before C0a and again before C4.
`git status --porcelain` empty at round start and after each of the five commits; `git worktree
list` one line.
G2 committed authored file, committed `last_block.md` and BOTH working copies byte-EQUAL: sha256
c73bac4c5553f82312b5d38669bb33de3586a897f2ec7198f39c0b1399b406d0, 21848 B, 398 lines, 26 marker
lines, region digests 3866a6a1 / d15e4f7e / 4b8d681f.
G3 pre-commit blob a byte-exact PREFIX: True; remainder exactly one blank line + RECORD1: True;
RECORD1's first line 1× among the 71 added lines; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while
the substring `END-` hits 7× (older prose). `git show --numstat`: `71 0`.
G4 base 07b1ba25: 132 registered / 14 done / 0 landed, 118 open, max R-0517. HEAD: 133 / 15 / 0,
118 open, max R-0518, next free R-0519. Registered symdiff `['R-0518']`, done symdiff `['R-0517']`,
landed symdiff `[]`; 0 duplicate ids; 0 resolutions naming an unregistered id.
G5 PLANF 0×, PLANT 1×; `## Goal` and `## Risks` byte-IDENTICAL to base; sha256
cb45b4b58e735e33e3ac8d3025f09f3850e1df79feafe4934d6d04357b52417f, 2393 B, 42 lines (<50);
`## Next Steps` parses to 1, 2, 3.
G6 S1F/S2F/S3F/S4F 0× each and S1T/S2T/S3T/S4T 1× each at HEAD. S5 append-shaped:
`    def test_child_half_of_the_exec_policy_reaches_the_child(self, tmp_path):` 1× among C3's 39
added lines; `    def test_no_shell_true(self):` still 1× in the whole file.
G7 exit 0, `98 passed in 24.72s` (base reading 97; this round adds one test, which ran — no skip).
G8 in worktree `.remedy-wt/r28-g8` at e78c7027 and nowhere else: `preexec_fn=plan.preexec_fn,`
deleted (1 occurrence) → node exit 1, last line `1 failed in 0.35s`; file restored byte-identical
→ same node exit 0, last line `1 passed in 0.27s`.
G9 exit 0, `All checks passed!`.
G10 exit 0, `158 passed in 19.95s`, run in the PRIMARY checkout, never in the G8 worktree (R-0518).
CANARY `tests/cli/test_golden_path.py` exit 0, `42 passed in 20.32s`.
G11 `git diff --name-only 07b1ba25..HEAD` before C4 holds exactly `.agent/authored/f085-r28.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`packages/orchestration/test_execution_service.py` and
`tests/orchestration/test_test_execution_service.py`, nothing else. Insertions 398, 334, 71, 8, 39
— none over 500. Every commit has one parent; `git reflog -12` holds only `commit:` entries.
STALENESS (constraint 8): both edited files re-read at HEAD after C3 — `_build_safe_env` is defined
in the same module the S2T comment names (line 265) and `_run_isolated_process` has exactly one
caller, unpacking the tuple positionally (line 806). No sentence this round wrote was falsified,
and no slice quotes another file's wording as a claim.

## Authored-text proofs

All thirteen slices were extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r28.md`
by their marker pairs and applied byte-verbatim; none was retyped or taken from the prompt. Every
FROM matched at exactly 1 place before its edit — pre-counted for all five code pairs before the
first write. 0 marker lines reached any target file. Disk-to-disk: the committed blob equals the
file copied in, sha256 as under G2.

## Deviations & assumptions

The ordered sequence C0a → C0b → C1 → C2 → C3 → C4 was followed exactly: no extra, dropped or
reordered commit, and no gate reading departed from what the block ordered.
Deviations, declared (DECISION D15): this file is 125 lines against the 100 its six per-commit
tables permit. The cause is mandated content — six per-commit changed-files tables, the six-row
item-status table, and real readings with exit codes for eleven gates plus the standing staleness
check. No section was dropped or shortened to meet the cap.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE
rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
R-0202 is NOT resolved by this round: `env` reaches the child exactly as the caller built it, so
`REMEDY_UI_NO_AUTO_BUILD` is dropped after this round by the same code as before it. R-0518 is
registered and NOT fixed here. R28's own verdict is NOT a §4.13 terminator, because this branch
continues, and the next reviewed round records R28's gate entry in `.agent/live_review.md`. Then
T002b Restprüfung.
