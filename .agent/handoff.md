# Handback — F082 Self-benchmark, R17/19 (worker)

Branch: feature/f082-self-benchmark. BASE re-derived at delegation: HEAD was
c044cb18, EQUAL to the block's declared BASE (R-0428). Review of c044cb18..HEAD.

## Commits

### dbe419b3 chore(f082): save the R17 step block as the round's authored original
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f082-r17.md | +399/-0 | C0a, byte-verbatim copy of the block |

### 0f70cad3 chore(f082): mirror the R17 block into the last-block state file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +327/-301 | C0b, byte-identical mirror of C0a |

### 983a897c docs(f082): record the R16 verdict and register R-0429 and R-0430
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C1, GATE-R16 + FINDINGS-R429-430 appended |

### 3e3bac91 feat(f082): add the on-demand bench run entry point
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/bench_run.py | +86/-0 | C2, NEW, authored from the contract |

### d86ef32f test(f082): pin the bench run end to end with no network and no clock
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_bench_run.py | +264/-0 | C3, NEW, six properties, nine seams doubled |

### d045ec35 test(f082): spend the D9 allowlist on the bench run entry point
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_bench_never_runs_implicitly.py | +6/-1 | C4, ALLOWLIST pair |

### b968671d docs(f082): repair the bench history additive claim for R-0427
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/bench_history.py | +5/-2 | C5, R0427FIX pair |

### a7eb19eb docs(f082): re-sync the plan and the context for R17
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-18 | C6, whole-file PLAN slice |
| .agent/context.md | +12/-4 | C6, three pairs as one composite |

### this commit docs(f082): hand back R17 (grouped, R-0149 self-reference)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C7; a handoff cannot table its own commit |

## External actions

`git push -u origin feature/f082-self-benchmark` after each of the nine commits
— all succeeded. `gh pr list --state open` → `[]`; no PR created.
`git worktree add .remedy-wt/redproof-r17 HEAD` → created at a7eb19eb;
`git worktree remove --force .remedy-wt/redproof-r17` → removed.

## Verification — the 22 ordered gates, real values

1. `git status --porcelain` → EMPTY. `git worktree list` → one line,
   `/home/decodeux/Repos/remedy  a7eb19eb [feature/f082-self-benchmark]`.
2. TRANSPORT: `read_bytes()` equality True; sha256
   `990fa83f927e9a575533bffc36ca0eac5ed7e5b40ebf76c0d1889b3632ed4ba5`; 33591
   bytes both. REAL line count 399 — MATCHES the declared 399.
3. `.agent/STOP` absent at round START, absent at handback.
4. C1 over `983a897c^..983a897c`: `post == pre + NL + GATE-R16 + NL +
   FINDINGS-R429-430` → True; `pre` a prefix of `post` → True; +8564 bytes;
   numstat `6	0	.agent/live_review.md`, deletion column 0.
5. Line-anchored at HEAD: `^Gate: R16 — PASS` 1 · `^- R-0429 — ` 1 ·
   `^- R-0430 — ` 1 · `^## DECISION F082 D9` 1 · `^Landed: ` 0 · `^Done: ` 0.
6. OPEN SET: 60 registered paragraphs, 0 `^Done:` → 60, no duplicate, max
   R-0430, next free R-0431.
7. C6 over `a7eb19eb^..a7eb19eb`: `pre` with ALL THREE replacements == `post`
   → True. Each pair FROM 1x in pre / 0x in post, TO 1x in post, `FROM in TO`
   False (CTXSCOPE-R17, CTXIMPLICIT-R17, CTXSTEPS-R17). `.agent/plan.md`
   byte-equals the PLAN slice → True, sha256
   `d5a5ffb8eac253fe310b8cc0abfbe5a804a6eecc75103017cea920c5d20dd141`,
   47 lines (under 50), `## Goal` and `## Next Steps` present. context.md 97 lines.
8. C4 `d045ec35`: `pre.replace(FROM,TO) == post` True, FROM 1x→0x, numstat
   `6	1	tests/orchestration/test_bench_never_runs_implicitly.py`. C5 `b968671d`:
   True, FROM 1x→0x, numstat `5	2	packages/orchestration/bench_history.py`.
9. Range under `packages/`: bench_history.py, bench_run.py. Under `tests/`:
   test_bench_never_runs_implicitly.py, test_bench_run.py. NEW files
   bench_run.py +86/-0 and test_bench_run.py +264/-0 (both deletion 0).
   `^def test_` 7. `wc -l bench_run.py` 86.
10. `pytest tests/orchestration/test_bench_run.py -q` → `7 passed`, exit 0.
11. `pytest …/test_bench_never_runs_implicitly.py -q` → `6 passed`, exit 0.
    Observed per-tree counts: apps 73, packages 257, scripts 29.
12. RED-PROOF in the disposable worktree (`pwd` and `git rev-parse
    --show-toplevel` both `…/.remedy-wt/redproof-r17`): with the one name
    removed and `bench_run.py` in place the pin's COLOUR is RED —
    `test_only_allowlisted_modules_call_the_bench_write_entry_points` fails on
    "The bench gained an implicit caller: packages/orchestration/bench_run.py
    calls append_bench_run; …". Worktree removed; `git worktree list` one line.
13. Gauntlet seven → `276 passed`, exit 0. Pre-existing bench five
    (capability_bench, bench_orders, bench_dry_run, bench_history,
    cli/test_stats_bench) → `61 passed`, exit 0. Both equal their BASE values.
14. `pytest …/test_bench_model_context.py -q` → `14 passed`, exit 0.
15. Canary + three contract readers → `184 passed`, exit 0.
16. Scoped `ruff check` over the four files → `All checks passed!`, exit 0.
17. `integrity check --json` → `passed: True`, `fail_count: 0`,
    `check_count: 5`, `handler_import` pass `handlers=337`.
18. Range restricted to the five gauntlet modules → EMPTY. Constraint 1 holds.
19. CHANGE SET, measured BEFORE C7: `.agent/authored/f082-r17.md`,
    `.agent/context.md`, `.agent/last_block.md`, `.agent/live_review.md`,
    `.agent/plan.md`, `packages/orchestration/bench_history.py`,
    `packages/orchestration/bench_run.py`,
    `tests/orchestration/test_bench_never_runs_implicitly.py`,
    `tests/orchestration/test_bench_run.py` — COUNT 9, all inside the ceiling.
    Restricted to `docs/` → EMPTY; to `apps/` → EMPTY.
20. `gh pr list --state open --json number,headRefName` → `[]`, exit 0.
21. Insertions per commit: 399, 327, 6, 86, 264, 6, 5, 29 — none over 500.
22. STALENESS GATE, ninth run: 24 claim-bearing sentences checked across the six
    touched files that are neither verbatim transport nor append-only record —
    context.md 6, plan.md 5, the pin 4, bench_history.py 2, bench_run.py 3,
    test_bench_run.py 4. 21 hold at HEAD. Three reported, none covered by an
    ordered slice, none repaired: (a) context.md "The allowlist is
    EMPTY today and gains exactly one name at R17, which spent it on …" — the
    "is EMPTY today" clause is stale, the ordered pair only extended the tail;
    (b) the pin's docstring "which is empty today and gains exactly one name at
    R17", stale for the same reason; (c) the pin's "apps 73, packages 256,
    scripts 29" is time-stamped "measured at R16" and true as history — HEAD
    measures packages 257, and the floors 40/150/15 are unaffected. Re-checked
    and NOT repaired as ordered: context.md still names 240 as the preferred
    block target — PRESENT, read off the line directly, because my own first
    normalised read of (c) reproduced R16's wrap artefact. C5 repairs R-0427.

## Authored-text proofs

All 14 slices applied DISK-TO-DISK out of the committed
`.agent/authored/f082-r17.md`. Marker lines reaching any target: 0.
Trailing-whitespace lines gained in any target: 0. Pair proofs at gates 4, 7, 8.
C2 and C3 were AUTHORED from their contracts, not transported.

## Deviations, declared

Stated-cause overage of the 60-line cap (AGENTS.md D15): this handoff is 205
lines. Cause: nine per-commit tables, twenty-two gate values and a 31-row
item-status table. No section dropped.
- **D1, mine.** `BenchRunResult.outcomes`/`.rows` are typed `tuple[Any, ...]`
  rather than `tuple[OrderOutcome, ...]`/`tuple[BenchRecord, ...]`: Constraint 1
  enumerates the five product symbols `bench_run.py` may import and both types
  are outside it. The concrete types are named in the field comments.
- **D2, REVIEWER SLICE DEFECT, applied verbatim as ordered (Constraint 8).**
  `CTXSCOPE-R17-TO`'s first line joins the existing sentence tail, giving a
  92-character line in a paragraph wrapped at ~79.
- **D3, REVIEWER SLICE DEFECT, applied verbatim as ordered.**
  `CTXIMPLICIT-R17-TO`'s second line, "deliberate act, not a repair.", carries
  no two-space continuation indent, so it dedents out of the `- ` bullet it
  belongs to in context.md's Constraints list.
- **D4, mine.** C3's property 5 is pinned by TWO test functions (missing
  `data_root`; missing `history_path`), so the file holds 7 `^def test_` for the
  six ordered properties. No seventh property was added.
- **D5.** Gate 11's observed `packages` count is 257, not R16's 256 — the block
  predicted "+1 file this round", and that file is `bench_run.py`.

Fortschritt: ~94 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · Q7-Kriterium gepinnt · Fake-Provider-Lauf gelandet · Integrationsgate + Closure offen) — Schätzung

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | deviated | D1 — payload typed `Any` to keep the import list at five |
| C3 | deviated | D4 — property 5 split across two test functions |
| C4 | done | |
| C5 | done | |
| C6 | deviated | D2, D3 — two reviewer slice defects applied verbatim |
| C7 | done | this handback |
| Gate 1 | done | clean tree, one worktree |
| Gate 2 | done | equal, 399 lines, matches |
| Gate 3 | done | absent, absent |
| Gate 4 | done | True, deletion column 0 |
| Gate 5 | done | 1·1·1·1·0·0 |
| Gate 6 | done | 60, max R-0430, next R-0431, no duplicate |
| Gate 7 | done | composite True, plan 47 lines |
| Gate 8 | done | both pairs True |
| Gate 9 | done | four paths, 0 deletions, 7 tests, 86 lines |
| Gate 10 | done | 7 passed, exit 0 |
| Gate 11 | deviated | D5 — packages 257, not 256 |
| Gate 12 | done | RED, worktree removed |
| Gate 13 | done | 276 passed, 61 passed |
| Gate 14 | done | 14 passed |
| Gate 15 | done | 184 passed |
| Gate 16 | done | All checks passed! |
| Gate 17 | done | passed True, handlers=337 |
| Gate 18 | done | EMPTY |
| Gate 19 | done | 9 paths, measured before C7 |
| Gate 20 | done | [] |
| Gate 21 | done | max 399 |
| Gate 22 | done | 24 sentences, 3 stale reported not repaired |

Open findings: 60 (max R-0430, next free R-0431). No block condition hit.

## Reviewer verdict — recorded after this handback was written

R17 is PASS. The reviewer re-executed all twenty-two gates against the disk and
every value reproduced; the verdict line and three findings, R-0431 to R-0433,
are appended to `.agent/live_review.md`. All three are the REVIEWER's own block
defects, two of them the deviations declared above. Open findings are now
SIXTY-THREE, max R-0433, next free R-0434.

## Next

R18 — the integration gate, which also repairs R-0431, R-0432 and R-0433 and is
the round that measures the Goal's three DONE conditions together. THE NEXT
SESSION'S FIRST ACTION is self_drive_protocol.md Phase 1 rule 1, re-read
`.agent/STOP` from disk, BEFORE rule 2's Open PR Gate. F082 is MID-FEATURE and
no PR exists.
