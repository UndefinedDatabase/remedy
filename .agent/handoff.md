# Handback — F021 R6 (T001: the humanize module, its catalog and the contract test)

Branch: feature/f021-live-activity-feed · Round base: `82fcc7c0272d366e36ebda5020dbc1697d98e32b`
Open findings: 211 registered, maximum id R-0648, nothing minted and nothing resolved this round.

Fortschritt: ~30 % (T001 gebaut · T002 offen · T003 offen; R1-R5 Anspruch,
             Vermessung, Entscheidung, Verdikt und Korrektur — R6 ist die erste
             Runde, die Produktionscode liefert) — Schätzung

## Range

Review of `82fcc7c0`..HEAD — ten commits, C0a through C8.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | |
| C8 | done | |

## Commits

### 1fe225c0 docs(state): save the F021 R6 T001 block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r6.md | +357/-0 | the block, copied byte-for-byte |

### 757094ce docs(state): mirror the F021 R6 T001 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +284/-165 | written FROM the committed C0a blob |

### 7c3eb24d docs(state): point the F021 plan at the R6 build round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-15 | slice PLANF021R6, full replacement |

### 5d4e3bef docs(review): record the R5 verdict and widen the R-0449 and R-0494 evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | slice RECORD5, appended |

### 426ee2a1 docs(agents): add the pre-emission checklist item on gate ordering
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +24/-0 | pair CHECKFROM to CHECKTO, §3 item 31 |

### e9568263 feat(ui): add the humanize module and its honest generic line
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanize.ts | +29/-0 | slice HUMANIZE, new file |

### 9c782704 feat(ui): add the stream event humanization catalog
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanizeCatalog.ts | +92/-0 | 83 entries, keys = the G5 vocabulary |

### ef67e7b0 test(ui): cover the humanize module behaviour and its generic path
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanize.test.ts | +57/-0 | 8 vitest cases, catalog and generic path |

### 2750a726 test(ui): pin the catalog key set to the python run-log emitters
| Path | +/- | Reason |
|---|---|---|
| tests/ui_contracts/test_humanize_catalog.py | +231/-0 | 9 pytest cases, set equality |

### C8 docs(state): hand back F021 R6 — role: the handback commit, which writes this file and therefore cannot name its own SHA or its own numstat; G1 orders those readings NOWHERE and the reviewer takes them at the next gate (finding R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured at the next gate | this handback |

## External actions

- `git worktree add` + `git worktree remove --force` + `git worktree prune`, three times, all disposable and all removed: `.remedy-wt/g6-wt` at `5d4e3bef` (G6 mutant), `.remedy-wt/base-wt` at `82fcc7c0` with the primary `apps/ui/node_modules` symlinked in and unlinked before teardown (G10/G11 round-base readings), `.remedy-wt/g12-wt` at `2750a726` (G12 red control). `git worktree list` ends with the primary checkout alone.
- `gh pr list --state open --json number,headRefName` → `[]`. No `gh pr create`, no `gh pr merge`.
- `git push -u origin feature/f021-live-activity-feed` after C8.

## Verification

- G1 EXECUTED: `.agent/STOP` absent before C0a and before C8; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a-C7; C8's own reading ordered nowhere.
- G2 EXECUTED: authored blob, `.agent/last_block.md`, the received bytes and the reviewer's `.remedy-wt/f021-r6.md` are all sha256 `08dbd76e98e0ace307889876d49ff897cf5b2e2531daf2a72f17a45156bbbd77`, 28636 bytes, 357 lines.
- G3 EXECUTED: 5 slices over 106 CONTENT lines from the committed C0a blob; TOTAL 357 against 490, PROSE 251 against 400.
- G4 EXECUTED: `cmp` exit 0 for plan-vs-PLANF021R6 and humanize-vs-HUMANIZE; negative controls exit 1 and 1; plan `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 44 against the 50 cap.
- G5 EXECUTED: 82 call sites, 60 distinct literals, 11 non-constant event arguments, 15 names inside the four defined sets; static stream vocabulary 83; literals-vs-trace-sets intersection empty. All four ordered readings reproduce.
- G6 EXECUTED: reader (a) prefix holds, remainder sha256 `3567c4a03d02248b04258ba786445ab4295860bfc7e6996ac233a61c89b9061c`, 5706 bytes, 2 lines; file 440340 bytes/1078 lines to 446046/1080; reader (b) units 220 + 1 = 221, every position equal; the byte-7 `R`→`X` mutant of the first paragraph is REJECTED by both readers and the true file ACCEPTED by both.
- G7 EXECUTED: CHECKFROM 1 at the round base and 1 at C3 (APPEND-shaped); all 24 TO-ONLY lines occur exactly 1x among C3's 24 added lines; file 920 to 944 lines; numstat `24 0`; `^  31\. \*\*` 0 then 1, `^  32\. \*\*` 0 at both.
- G8 EXECUTED, base then C2: `- R-` 211/211 both DISTINCT at both; `Done: R-` 0/0; `Landed: ` 0/0; `Gate: R` keys 5 then 6, all DISTINCT; `Gate: R6` 0 then 1; maximum id R-0648 at both; `- R-0449 —` 1/1; `- R-0494 —` 1/1.
- G9 EXECUTED at the C5 blob: 1 exported symbol; 83 extracted keys equal to the 83-name G5 vocabulary; ASCII-sorted; 0 duplicate keys; 83 values, 83 distinct, 0 empty, 0 not ending in a full stop, 0 equal to `<key> event`.
- G10 EXECUTED: `npx tsc --noEmit` in `apps/ui` — exit 0 at the round base and exit 0 at C7.
- G11 EXECUTED: `npx vitest run` in `apps/ui` — round base exit 0, 10 files, 152 tests, 0.7 s wall; C7 exit 0, 11 files, 160 tests, 0.7 s wall.
- G12 EXECUTED: `python3 -m pytest tests/ui_contracts/ -q -rf` exit 0, 426 passed + 4 skipped = 430 = 421 + the 9 tests C7 adds. RED CONTROL in a worktree: deleting the `worktree_retained` entry FAILS the equality test at exit 1 and names `['worktree_retained']`; deleting `verification_passed` fails it and names that key too.
- G13 EXECUTED: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py -q -rf` exit 0, 511 passed + 0 skipped = 511. No docs gate owed: the Change list holds one `docs/agents/` path and zero `docs/roadmap/**` paths.
- G14 EXECUTED after G13, serially: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed.
- G15 EXECUTED over `82fcc7c0`..C7 plus the one path C8 writes: 9 range paths, both set differences against the 10-path Change list EMPTY once `.agent/handoff.md` is counted; 9 commits all single-parent; insertions 357/284/17/2/24/29/92/57/231, every one under 500; leading `<<<SLICE ` and `<<<END ` 0 lines in all four files a slice landed in; `git ls-files .remedy-wt` 0; this round's 9 reflog rows all `commit:` — amend 0, rebase 0, cherry 0.
- G16 EXECUTED: `gh pr list --state open --json number,headRefName` → `[]`. Neither `gh pr create` nor `gh pr merge` was run.
- G17 EXECUTED: this file — every mandated section, an item-status row per C0a-C8, the round base SHA, one line per gate, the `Fortschritt:` line verbatim, and a `## Next` naming R7 and T002.

## Authored-text proofs

`.agent/authored/f021-r6.md` at `1fe225c0` is byte-identical to the emitted block. Every slice was extracted programmatically from that committed blob by its marker lines; no slice was retyped. `.agent/plan.md` at C1 and `apps/ui/src/api/humanize.ts` at C4 each `cmp` at exit 0 against their extracted slice, each with a negative control at exit 1 (G4).

## Deviations & assumptions

- The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8 was followed exactly: no extra commit, none dropped, none reordered.
- G17 calls this "a nine-commit bundle"; it is a TEN-commit bundle (C0a through C8). The 100-line allowance the sentence names is what this file is measured against, and the item-status table carries all ten rows.
- G15's range reading was taken at C7 over `82fcc7c0`..C7, plus the single path C8 writes, which is why `.agent/handoff.md` shows as the only Change-list path outside that range. C8's own numstat, insertion count and `git status --porcelain` reading are ordered NOWHERE by G1 and are not stated here.
- Assumption, declared: the round-base readings of G10 and G11 were taken in a disposable worktree at `82fcc7c0` with the primary checkout's `apps/ui/node_modules` symlinked in, because a fresh worktree has no `node_modules`; the symlink and the worktree were removed before this handback.
- DECISION D15, stated-cause overage: this file is 121 lines against the 100-line allowance. The cause is mandated content only — ten per-commit changed-files tables (40 lines), the ten-row item-status table, and one line for each of the seventeen gates G17 requires. No section was dropped and no transcript was copied in; the transcripts live in the round report.

## Next

R7 rules the frontend test environment and the single-subscription fan-out — the two infrastructure DECISIONS T002 needs before the feed, its rows and the NowCard can be written. The reviewer's first action is Phase 1 rule 1: re-read `.agent/STOP` from disk, then the Open PR Gate.
