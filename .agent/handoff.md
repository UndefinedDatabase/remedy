# Handback — F008 SSE event stream, R5

Branch `feature/f008-sse-event-stream`. Open findings: 185, unchanged — constraint 5 ordered no registration and none was made.

## Range

Review of `9cb131c1`..HEAD, HEAD being the C4 commit that writes this file.

## Commits

### f0d6d2d6 chore(state): save the F008 R5 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f008-r5.md | +349/-0 | C0a — the step block saved verbatim |

### f2532d00 chore(state): mirror the F008 R5 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +260/-291 | C0b — mirror, byte-equal to C0a |

### 627ab499 chore(plan): advance the plan to F008 R5
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-22 | C1 — PLANF008R5, the first substantive commit |

### f00360c0 docs(review): record the R4 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — one `Gate:` paragraph, no finding |

### 0b1abd81 feat(ui-server): expose the ledger position as seq on events-since
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +5/-1 | C3 — SEQFROM rewritten to SEQTO |
| tests/ui_server/test_event_seq.py | +92/-0 | C3 — TESTFILE, new, pins `seq` |

### C4 docs(state): write the F008 R5 handback
`.agent/handoff.md`, rewritten. A handoff cannot table the commit that writes it (R-0149), so its `+/-` is reported in the round report.

## External actions

- `git worktree add .remedy-wt/redctl-r5 0b1abd81 --detach` — created.
- `git worktree remove .remedy-wt/redctl-r5 --force` — removed; at this handback `git worktree list` names the primary checkout alone.
- `git push -u origin feature/f008-sse-event-stream` — ORDERED by Push Discipline, run after this commit; its outcome is reported in the round report rather than asserted here.
- No PR created, none merged, no `gh` command run.

## Verification

- G1 `.agent/STOP` absent, read immediately before C0a; branch `feature/f008-sse-event-stream`; `git status --porcelain` empty after every commit and at this handback; `git worktree list` names the primary checkout alone.
- G2 block on disk, authored@C0a and last_block@C0b are ALL EQUAL — sha256 `67489603142f567411b9c370351d8e3595cb9f9bcb951de067faa7c6a3e7b23b`, 23217 bytes, 349 lines.
- G3 5 slices by ordered extraction from the committed file: PLANF008R5 `3c30da07` 2374B/43L · RECORDR4 `36227d97` 4465B/1L · SEQFROM `d8e35c29` 93B/3L · SEQTO `b74eaa8a` 377B/7L · TESTFILE `0b9c7605` 3518B/92L.
- G4 plan@C1 `3c30da07` 2374B/43L, byte-equal to PLANF008R5; 43 < 50; `## Goal` 1, `## Next Steps` 1, `F008` 3; C1 is the first commit after C0a and C0b.
- G5 (a) the C1 blob is a byte-exact prefix of the C2 blob and the remainder `42658972` 4466B/2L equals `\n`+RECORDR4; (b) an INDEPENDENT blank-line split yields 194 units whose LAST equals RECORDR4. Negative control: one flipped byte is REJECTED by both readings while the unflipped value is ACCEPTED by both.
- G6 C1→C2: `^- R-\d+ — ` 185→185 · `^Done: R-\d+ — ` 0→0 · `^Landed: ` 0→0 · `^Gate: R\d+ — ` 4→5 with keys R1 R2 R3 R4 R5 DISTINCT · `^- R-0614 — ` 0 at both.
- G7 in ui_server.py SEQFROM reads 1 then 0 and SEQTO reads 0 then 1 between `9cb131c1` and C3; the containment test printed `TO contains FROM: false`, a rewrite; `git show --numstat 0b1abd81 -- packages/orchestration/ui_server.py` reads `5	1`.
- G8 test file@C3 `0b9c7605` 3518B/92L, byte-equal to TESTFILE; `git ls-tree 9cb131c1 -- tests/ui_server/test_event_seq.py` printed nothing.
- G9 RED PROOF, in the disposable worktree and never in the primary checkout: with SEQTO replaced by SEQFROM and the new tests left in place, `python3 -m pytest tests/ui_server/test_event_seq.py -q -rf` EXITS 1 at `6 failed, 1 passed in 0.21s`, and both `KeyError` and `seq` appear — the decisive line is `E   KeyError: 'seq'`. Restored, the file is byte-identical to C3's blob (sha256 `e2feda53…`) and the same command EXITS 0 at `7 passed in 0.21s`. The one test that passes reverted is `test_a_cursor_past_the_end_returns_nothing_and_invents_no_seq`, which asserts an EMPTY event list and so never reads a `seq` key; the other six all die on the missing field.
- G10 `python3 -m pytest tests/ui_server/test_event_seq.py -q -rf` in the primary checkout: exit 0, passed 7 + skipped 0 = 7.
- G11 serially in the primary checkout, never alongside G10: the combined four exit 0 at passed 358 + skipped 0 = 358; `tests/cli/test_golden_path.py` exits 0 at passed 42 + skipped 0 = 42. No skip fired on these runs; per constraint 10 the sums, not bare passed counts, are the readings.
- G12 `git show <sha>:<path>` piped to `python3 -m ruff check --stdin-filename <path> -`, writing to no tracked file: ui_server@`9cb131c1` exit 0 multiset {} · ui_server@C3 exit 0 {} · test file@C3 exit 0 {} — the two ui_server multisets are EQUAL and the new file's is empty. An UNORDERED red control through the same path returned exit 1 with {I001:1, F811:1, F401:1}, proving the extractor can report a non-empty multiset rather than reading empty always.
- G13 `git diff --name-only 9cb131c1..C4` equals the Change set with no path on either side alone; every commit in the range has exactly one parent; insertions 349 / 260 / 21 / 2 / 97 are all under 500 and agree cell by cell with the `+/-` column above.
- G14 lines beginning `<<<SLICE ` or `<<<END `: plan@C1 0 · live_review@C2 0 · ui_server@C3 0 · test file@C3 0 · this file@C4 0.
- G15 over this round's OWN reflog entries the only OPERATION — the text before the first `:` in `git reflog --format=%gs` — is `commit`; the count whose operation is `amend`, `rebase` or `cherry` is 0. Counted by operation, never by substring (R-0613).
- G16 this file carries every section `docs/agents/handback_template.md` mandates plus the item table below; its line count is reported in the round report; the cap for this round is 100.

## Authored-text proofs

Every slice was extracted from the COMMITTED `.agent/authored/f008-r5.md` by its marker lines and applied without retyping, rewrapping or reflowing. Disk-to-disk: `.agent/plan.md`@C1 is byte-equal to PLANF008R5, `tests/ui_server/test_event_seq.py`@C3 to TESTFILE, and the C2 remainder to `\n`+RECORDR4 (G4, G8, G5); the pair landed as SEQFROM 1→0 and SEQTO 0→1 (G7). No slice objection is raised.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## Deviations & assumptions

None. The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed exactly — no extra commit, none dropped, none reordered.

## Next

Reviewer review of `9cb131c1`..HEAD, then R6: the stream endpoint `GET /api/jobs/<jid>/events/stream` with SSE framing, `seq` as the event id, a 15 s heartbeat and 404 for an unknown job. At the next session's start, Phase 1 rule 1 (`.agent/STOP`) precedes rule 2 (the Open PR Gate).

Fortschritt: 18 % (F008 beansprucht · fünf Urteile im Ledger ·
DECISION F008 D1 vollständig umgesetzt: Server nebenläufig und
die Ledger-Position als `seq` sichtbar · der Stream-Endpunkt
selbst beginnt in R6) — Schätzung
