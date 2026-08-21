# Handback — F008 R4 · cockpit server serves concurrent requests

## Range
Branch `feature/f008-sse-event-stream`, no PR open this round. Review of
`c1e4e3ac`..HEAD, HEAD being C5 — the commit that writes this file, whose SHA
cannot exist when this line is written and is in the round report.

## Commits
### 2896fe2d chore(state): save the F008 R4 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f008-r4.md | +380/-0 | C0a — block saved; every slice extracted from this blob |

### 5112a5d2 chore(state): mirror the F008 R4 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +300/-254 | C0b — mirror, byte-equal to the C0a blob |

### 9b183953 chore(plan): advance the plan to F008 R4
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-20 | C1 — PLANF008R4, 44 lines, first commit after the two saves |

### 6292fd51 docs(review): register finding R-0613
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — FIND0613 appended, before the verdict per §4.4 |

### 6fb06928 docs(review): record the R3 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3 — RECORDR3 appended |

### e5b93f23 fix(ui-server): serve concurrent requests with a threading server
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +2/-2 | C4 — import and instantiation, `HTTPServer` to `ThreadingHTTPServer` |
| tests/ui_server/test_server_concurrency.py | +110/-0 | C4 — TESTFILE, a `threading.Barrier(2)` both requests must reach |

### C5 docs(state): write the F008 R4 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | C5 — a handoff cannot table the commit that writes it (R-0149) |

## External actions
- `git worktree add .remedy-wt/redctl-r4 e5b93f23 --detach` — created, detached at C4; `git worktree remove .remedy-wt/redctl-r4 --force` — removed, `git worktree list` then naming the primary checkout alone.
- Push: ORDERED by AGENTS.md Push Discipline and executed after C5; a push that follows this commit cannot be asserted by a line inside it, so its real outcome is in the round report.
- No PR created, edited or merged. No `gh` command run.

## Verification
- G1 `.agent/STOP` absent before C0a; branch `feature/f008-sse-event-stream`; `git status --porcelain` empty after all 7 commits and at the handback; `git worktree list` = primary alone.
- G2 block, `.agent/authored/f008-r4.md`@C0a and `.agent/last_block.md`@C0b: sha256 `da369700…`, 26853 B, 380 lines — all three EQUAL.
- G3 8 slices, count taken from the extraction listing over the C0a blob: PLANF008R4 `76033137…`/2456/44 · FIND0613 `2b93656f…`/2815/1 · RECORDR3 `b307ebcb…`/4668/1 · IMPORTFROM `aad96037…`/59/1 · IMPORTTO `0e5aadf1…`/68/1 · SERVERFROM `dadae59d…`/53/1 · SERVERTO `12ed4c15…`/62/1 · TESTFILE `9a1d28fb…`/3681/110.
- G4 `.agent/plan.md`@C1 sha256 `76033137…`, 2456 B, 44 lines — byte-equal to PLANF008R4, under 50; `^## Goal$` 1, `^## Next Steps$` 1, `F008` 4; first commit after C0a/C0b.
- G5 C1→C2 prefix true, remainder `ee3e98ce…`/2816 B/2 lines = newline+FIND0613; blank-line split 192 units, last unit equals the slice; both agree. C2→C3 prefix true, remainder `e466f9c0…`/4669 B/2 lines = newline+RECORDR3; 193 units, last unit equals the slice; both agree. Negative control on C1→C2: one flipped byte REJECTED by both readings, unflipped accepted by both.
- G6 `^- R-\d+ — ` 184/185/185 · `^Done: R-\d+ — ` 0/0/0 · `^Landed: ` 0/0/0 · `^Gate: R\d+ — ` 3/3/4, the four keys at C3 being R1 R2 R3 R4, distinct · `^- R-0613 — ` 0/1/1.
- G7 IMPORTFROM 1→0, IMPORTTO 0→1, SERVERFROM 1→0, SERVERTO 0→1 as exact whole lines, base to C4; containment printed `TO contains FROM: False` for both pairs — both REWRITEs, neither owes an append reading. `git show --numstat` on that path reads `2	2`.
- G8 `tests/ui_server/test_server_concurrency.py`@C4 sha256 `9a1d28fb…`, 3681 B, 110 lines — byte-equal to TESTFILE; `git ls-tree c1e4e3ac -- <path>` printed nothing.
- G9 primary checkout, serial: new test alone exit 0, `1 passed`; `tests/ui_server/` exit 0, `262 passed` — the 261 measured at base plus this round's one.
- G10 RED PROOF in `.remedy-wt/redctl-r4` only. (1) Both lines reverted, test file left in place: exit 1, last line `1 failed in 12.49s`, the failure being `threading.BrokenBarrierError` raised inside `gated` — the single-threaded server never gets the second request into the handler. (2) Both lines restored: file sha256 `ad95be28…` byte-identical to C4's blob, worktree `git status --porcelain` empty. (3) Same command: exit 0, `1 passed in 0.58s`.
- G11 primary checkout, serial, never alongside G9: state-reader four exit 0 `160 passed`; `tests/cli/test_golden_path.py` exit 0 `42 passed`. No resource-safety regression from `daemon_threads`.
- G12 `git show <sha>:<path>` piped to `ruff check --stdin-filename`, no tracked file written: ui_server.py at `c1e4e3ac` exit 0 multiset `{}`, at C4 exit 0 multiset `{}` — EQUAL; the new test file at C4 exit 0, multiset `{}` (empty), literal form printing `All checks passed!`. Red control through the same stdin path: a two-line file yields `{I001:1, F401:1}` exit 1, so the green is not vacuous.
- G13 measured after C5 exists, since the range ends at C5; the reading and the cell-by-cell agreement with the table above are in the round report. C0a..C4 insertions 380, 300, 21, 2, 2, 112 — all under 500; every commit has one parent.
- G14 marker lines beginning `<<<SLICE ` or `<<<END `: plan.md@C1 0 · live_review.md@C3 0 · ui_server.py@C4 0 · the new test@C4 0 · handoff.md@C5 measured after C5, in the round report.
- G15 over this round's own reflog entries, counting by OPERATION — the text before the first `:` in `git reflog --format=%gs` — entries whose operation is `amend`, `rebase` or `cherry`: 0. No entry total is stated.
- G16 this file carries the mandated sections and the item-status table below; its line count is in the round report.

## Authored-text proofs
Every slice was extracted from the COMMITTED `.agent/authored/f008-r4.md` by its
marker lines and applied byte for byte; none was retyped, rewrapped or edited.
Disk-to-disk equality is the G4/G5/G7/G8 readings above: plan.md byte-equal to
PLANF008R4, both ledger remainders equal to newline+slice under two independent
extractors, the new test byte-equal to TESTFILE, the four production lines
counted as exact whole lines 1→0 and 0→1.

## Deviations & assumptions
None. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly —
no extra commit, none dropped, none reordered; no slice altered; no path outside
the block's Change list touched; no oversize commit needed.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

Fortschritt: 14 % (F008 beansprucht · vier Urteile im Ledger ·
Findings-Order gemessen, DECISION F008 D1 verankert · der
Cockpit-Server bedient jetzt nebenläufige Requests, mit
Barrier-Beweis statt Stoppuhr · T001 beginnt in R5) —
Schätzung

## Next
Review `c1e4e3ac`..C5, then author R5 — T001 proper: the per-job SSE endpoint,
its 15 s heartbeat, 404 and 429, with seq read from the ledger position.
