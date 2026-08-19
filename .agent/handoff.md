# Handback — F085 sandbox hardening, R69 (T003's last acceptance line)

Branch: feature/f085-sandbox-hardening. Base SHA: 1df91b27.

## Range

Review of 1df91b27..HEAD

## Commits

### e575ab43 chore(f085): save the R69 step block under .agent/authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r69.md | +420/-0 | C0a — the block, copied byte-verbatim |

### 6a4df519 chore(f085): mirror the R69 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +349/-273 | C0b — mirror, byte-equal to the authored copy |

### cc563f6d docs(f085): advance the plan to the R69 acceptance round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8/-9 | C1 — PLAN23F→PLAN23T rewrite |

### 4651069b docs(f085): record the R68 PASS and resolve R-0563
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +40/-0 | C2 — RECORD37 appended at EOF |

### b735eb93 test(f085): measure the denied fetch against a really listening server
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +104/-0 | C3 — IMPORTSF→IMPORTST, THEN NETTEST appended |

### C4 (this commit) docs(f085): write the R69 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — a handoff cannot table the commit that writes it |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

`git worktree add --detach .remedy-wt/redctl-r69 HEAD` → created at b735eb93 for G8; removed with
`git worktree remove --force .remedy-wt/redctl-r69`; `git worktree list` one line again.
`git push -u origin feature/f085-sandbox-hardening` after this commit. No PR, no merge.

## Verification

G1 STATE, all readings as ordered: `.agent/STOP` absent before C0a and before C4; `git status
--porcelain` empty at round start and after every commit; `git worktree list` one line at start and
at end, and no worktree existed across any commit.
G2 TRANSPORT. Committed and working `.agent/authored/f085-r69.md` + `.agent/last_block.md`, all four
byte-EQUAL: sha256 3b506bf1f24540e5ed8fe84ac7487b67041b17da43b02b0d869d08305d893dc3, 27901 B, 420
lines, 12 marker lines. TOTAL 420 / cap 490 · PROSE 241 / 400 · RECORD37 40 / 140.
G3 SHAPES. cc563f6d: `TO contains FROM: false`, FROM 0x and TO 1x post-commit, re-apply reproduces
post BYTE-EXACTLY. 4651069b: PREFIX, SUFFIX, `pre + slice` == post byte for byte, ADDED 40 == slice
40 IN ORDER. b735eb93: IMPORTSF 1x pre / 0x post, IMPORTST 1x post, NETTEST an exact SUFFIX, and
`pre.replace(IMPORTSF, IMPORTST) + NETTEST` == post BYTE-EXACTLY. numstat 8/9 · 40/0 · 104/0. Marker
LINES 0 in all three edited files.
G4 SUITES, primary checkout, serial, each exit 0: `test_exec_guard.py -q -rf` → `44 passed` (base
42); `-k "really_listening or closed_proxy_port"` → `2 passed, 42 deselected`, 2 selected / 2 passed;
the four state readers → `160 passed` (base 160); CANARY `test_golden_path.py` → `42 passed` (base 42).
G5 PLAN CONTRACT. 39 lines / cap 50; `## Goal` true, `## Next Steps` true, `\bF\d{3}\b` true.
G6 ARITHMETIC. 1df91b27: 178 / 30 / 0, 148 open, max reg R-0563, max resolved R-0562. HEAD:
178 / 31 / 0, 147 open, max reg R-0563, max resolved R-0563. Symmetric differences — registered []
· done ['R-0563'] · landed []; 0 duplicate ids and 0 orphan resolutions at both SHAs; next id R-0564.
G7 LINT, both exit 0, both `All checks passed!`: `ruff check` and `ruff check --preview` over
`tests/orchestration/test_exec_guard.py`.
G8 RED CONTROL, in the disposable worktree only, after C3. Ordered byte string 1x in
`packages/orchestration/exec_guard.py`; bare `deny_network=True,` 2x, post-mutation 1 True
(dod-process, untouched) / 1 False. `pytest ... -k "really_listening or closed_proxy_port"` there:
EXIT 1, `2 failed, 42 deselected` — RED. FAILED
test_a_guarded_test_command_cannot_reach_a_server_that_is_really_listening (`assert 0 != 0`, guarded
child returncode=0, stdout `REMEDY_EXEC_GUARD_SERVED_BODY`); FAILED
test_the_refusal_a_denied_child_sees_names_the_closed_proxy_port (`assert b'Connection refused' in
b''`). Worktree removed, mutation committed nowhere, primary checkout clean.
G9 HYGIENE, before C4: exactly the 5 change-set paths minus `.agent/handoff.md`; 0 under
packages/apps/docs/scripts, 1 under tests/. Insertions 420 · 349 · 8 · 40 · 104, none over 500, all
five single-parent.

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r69.md` by its
marker pair under the block's CONVENTION; none retyped, none taken from the prompt. The disk-to-disk
comparison is G2's four-way byte equality plus G3's three byte-exact reconstructions.

## Deviations & assumptions

Ordered commit sequence C0a · C0b · C1 · C2 · C3 · C4 followed exactly — no extra, dropped or
reordered commit. Declared overage: this handback is 124 lines against the ≤100 cap, caused by
mandated content only — six per-commit tables, the item-status table, nine gate transcripts and the
verbatim Fortschritt block; no section was dropped. Constraint 8: I re-measured every mechanically
checkable RECORD37 claim — R68's transport digest/size/marker readings, TOTAL 344 / PROSE 230 /
RECORD36 88, 0 marker lines in both files R68 edited, plan.md 40 lines at 1df91b27, the
177/28/0-149-open → 178/30/0-148-open move with symmetric differences {R-0563} and {R-0561, R-0562},
the a8ba453d ledger a byte-exact PREFIX of the 1df91b27 ledger, `and an example sentence in` at 1x
per SHA, and five single-parent commits over the range. ALL AGREE; no disagreement to report.

## Next

ONE: R70 is the INTEGRATION GATE — the full suite per docs/agents/integration_gate.md, the first of
the two full-suite runs this feature owes; closure per docs/roadmap/STATUS_closure_protocol.md
follows it.
TWO: R69 carries no verdict of its own, because the round that records a verdict cannot record one on
itself (docs/agents/planner_reviewer_prompt.md §4 item 13); R70 carries it.
THREE: 147 findings open; next free id R-0564.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk.

Fortschritt: ~100 % der Bauarbeit (T001 gebaut · T002 KOMPLETT · T003 KOMPLETT: Netz-Posture
verdrahtet und gepinnt, Limitations-Dokument steht, verlinkt und inhaltlich korrekt, und die letzte
Akzeptanzzeile ist jetzt am echt lauschenden Server gemessen, mit Kontrolle · R66 und R67 FAIL, beide
Fehler des Reviewers, beide repariert) — offen bleiben nur noch Integration Gate und Closure.
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.
