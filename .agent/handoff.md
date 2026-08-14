# Handback — F082 Self-benchmark, R10 (T003a, the stats bench read view)

## Range
Review of d08250ed..HEAD (8 commits; HEAD is the C6 commit that writes this file).

## Commits

### b9ef3b1e chore(f082): save the R10 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f082-r10.md | +377/-0 | C0a — the R10 block copied byte-for-byte from the reviewer scratchpad |

### 587b93b0 chore(f082): mirror the R10 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +328/-203 | C0b — mirrored from the COMMITTED authored file via `git show`, never from the scratchpad |

### b1b93185 docs(f082): record the R9 verdict and DECISION F082 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +31/-0 | C1 — GATE-R9 then DECISION-D5, appended, verdicts persisted FIRST |

### 96bf3762 docs(f082): retire the stale steps map in the review record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-3 | C2 — LRSTEPS REWRITE pair; the branch's largest stale sentence |

### 529570ce feat(f082): add the stats bench read view over the bench history
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/bench_cmd.py | +401/-0 | C3 — the NEW read-only module (worker-authored code) |
| apps/cli/command_catalog.py | +22/-0 | C3 — CATALOG append-shaped pair: the `stats.bench` entry |
| apps/cli/commands/__init__.py | +2/-1 | C3 — INIT1 + INIT2 rewrite pairs: import and registration |

### 9b929697 test(f082): pin the stats bench read view over a real history
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_stats_bench.py | +372/-0 | C4 — 25 tests over a real history under `tmp_path`, no test-only flag |

### d68750ed docs(f082): re-sync the plan and the step map for T003a
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-13 | C5 — whole-file replacement with the PLAN slice |
| .agent/context.md | +3/-2 | C5 — CTXSTEPS rewrite pair |

### (this commit) chore(f082): handback R10
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6 — this file; a handoff cannot table the commit that writes it (R-0149) |

## External actions
- `git push` after every commit: d08250ed→b9ef3b1e→587b93b0→b1b93185→96bf3762→
  529570ce→9b929697→d68750ed, all OK; C6 pushed after this file is committed.
- `git worktree add .remedy-wt/f082-r10-redproof HEAD --detach` (gate 18), then
  `git worktree remove --force` + `git worktree prune`. `git worktree list` is back to
  one line.
- `gh pr list --state open --json number,headRefName` → `[]`. NO PR created; F082 is
  mid-feature and its PR is created at closure.
- No merge, no force-push, no rebase, no branch deletion.

## Verification — all twenty ordered gates, real measured values

| # | Gate | Real measured value |
|---|---|---|
| 1 | clean tree / worktrees | `git status --porcelain` EMPTY at handback (no output); `git worktree list` = one line, `/home/decodeux/Repos/remedy  d68750ed [feature/f082-self-benchmark]` |
| 2 | transport as a PROPERTY | scratchpad, `.agent/authored/f082-r10.md` and `.agent/last_block.md` all sha256 `415841817bbb53313cdf57b2abb766c0d46416d7fb75057ddb7b5c39ea385431`, 27229 bytes, **377 lines** (≤ 400). `read_bytes()` equality TRUE for all three pairs; `cp`/`cmp` denied, python3 route (R-0408) |
| 3 | `.agent/STOP` | ABSENT at round start and ABSENT at handback (`ls: cannot access '.agent/STOP': No such file or directory`, exit 2 both times) |
| 4 | C1 append proof | `post == pre + add` TRUE byte-wise over COMMITTED `b1b93185^`→`b1b93185`, `add` = `"\n" + GATE-R9 + "\n" + DECISION-D5` = 5791 bytes; `post.startswith(pre)` TRUE; 138-line pre is an exact prefix of the 169-line post. numstat `31  0` — DELETION column **0** |
| 5 | record counts at HEAD | `^Gate: R9 — PASS` **1** · `^## DECISION F082 D5` **1** · `^Landed: ` **0** · `^Done: ` **0** |
| 6 | open set recomputed | 47 `^- R-\d+ — ` paragraphs minus 0 `^Done:` lines = **FORTY-SEVEN**; duplicates NONE; max **R-0417**; next free **R-0418**. R10 registers no finding |
| 7 | LRSTEPS pair (REWRITE) | `post == pre.replace(FROM, TO)` TRUE byte-wise over `96bf3762^`→`96bf3762`. FROM 1x before / **0x after**; TO 0x before / **1x after**; `FROM in TO` False |
| 8 | CATALOG + both INIT pairs | CATALOG (APPEND-SHAPED): property TRUE; `FROM in TO` **True**, so FROM 1x before / **1x after** as the block states; `stats.bench` in command_catalog.py **0 before / 1 after**. INIT1 and INIT2 (REWRITES) chained: `post == pre.replace(1).replace(2)` TRUE; each FROM 1x→0x, each TO 0x→1x |
| 9 | state slices + contract readers | (a) CTXSTEPS property TRUE over `d68750ed^`→`d68750ed`, FROM 1x→0x, TO 0x→1x. (b) `.agent/plan.md` BYTE-EQUALS the PLAN slice as a whole file, sha256 `697951df422842fd7a1504580da36615b56550ac929f1c13e386fcae95dd26ef`, **41 lines** (< 50). (c) `## Active Branch` present and followed by `feature/f082-self-benchmark`; `Steps` present; F-ids F077/F082/F105; `pytest` AND `resource` present; plan keeps `## Goal` and `## Next Steps`; `.agent/context.md` **61 lines** |
| 10 | STANDING STALENESS GATE (2nd run) | **59 sentences** re-read across the 9 touched files. **55 HOLD, 4 DO NOT** — enumerated below. Repaired: only what the ordered pairs cover (live_review's `## Steps`, context's step map); nothing widened |
| 11 | change set | `git diff --name-only d08250ed..HEAD` measured BEFORE C6 = **9 paths**: `.agent/authored/f082-r10.md`, `.agent/context.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/bench_cmd.py`, `tests/cli/test_stats_bench.py`. With C6 it becomes 10, adding `.agent/handoff.md`. Every one is inside the block's Change list. `… -- packages/` = **EMPTY** |
| 12 | eleven-file orchestration suite | exit 0 — **294 passed** in 1.52s. Exactly the reviewer's 294 at d08250ed; R10 adds no test there and removes none |
| 13 | canary + three contract readers | exit 0 — **184 passed** in 39.45s. `test_dashboard_contract.py` calls `collect_all_handlers()`, so the new registration is exercised |
| 14 | catalog / grouped-CLI guards | exit 0 — **634 passed** in 40.08s. All five guard files UNMODIFIED; none needed an edit |
| 15 | the new test file + the real parser | `pytest tests/cli/test_stats_bench.py -q` exit 0 — **25 passed** in 0.15s. `python3 -m apps.cli.main stats bench --help` exit 0, real output: `Usage: remedy stats bench [OPTIONS]` / the catalog description verbatim / Options `--series`, `--multiplier`, `--project`, `--json`, `--help` |
| 16 | scoped ruff (4 paths) | exit 0 — `All checks passed!` over bench_cmd.py, commands/__init__.py, command_catalog.py, test_stats_bench.py |
| 17 | integrity check | exit 0 — `"passed": true`, `"fail_count": 0`, `"check_count": 5`; `handler_import` message **`handlers=337`** (336 + exactly one key); `high_blockers_open`: `no open blocker/high findings` |
| 18 | RED-PROOF (disposable worktree) | In `.remedy-wt/f082-r10-redproof` only. `_render_bench_human`'s `elif warnings:` body replaced by `raise AssertionError("red-proof")`. Import proof (R-0337): `IMPORTED FROM .../f082-r10-redproof/apps/cli/commands/bench_cmd.py`. Result **6 failed, 19 passed**, exit 1 — `test_the_warnings_are_exactly_what_bench_regressions_produced` (the load-bearing one), plus `test_neither_output_mode_changes_one_byte_of_the_history`, `test_it_names_the_chosen_series_and_the_one_it_did_not_read`, `test_an_unmeasured_row_prints_the_word_in_every_column`, `test_no_repair_round_column_and_the_limit_is_stated_once`, `test_no_price_is_computed_anywhere`. Worktree removed and pruned |
| 19 | open PRs | `gh pr list --state open --json number,headRefName` → `[]` verbatim |
| 20 | insertions per commit | `git show --numstat`: b9ef3b1e **+377**, 587b93b0 **+328**, b1b93185 **+31**, 96bf3762 **+8**, 529570ce **+425**, 9b929697 **+372**, d68750ed **+16**. NONE over 500. C6 cannot state its own numstat (R-0371); it is the verbatim rewrite of ONE `.agent/**` state file, exempt per AGENTS.md DECISION F104 D1, and its real value is in the completion report |

## Gate 10 — the four sentences that no longer hold

| File | Sentence | Why it fails |
|---|---|---|
| .agent/context.md | Scope: "Still to come, both T003: the `stats bench` CLI surface and the model-context recording" | HALF-STALE as of C3: the CLI surface landed THIS round. Only the model-context recording is still to come. NOT repaired — the block ordered one context pair and forbade widening |
| .agent/live_review.md | header: "Next free id: R-0404." | Next free is R-0418. Already registered as R-0406 (OPEN); outside this round's ordered slices |
| .agent/live_review.md | header: "the thirty-two findings … are reproduced verbatim at the end of this file" | COUNT holds (29 `R-03xx` + R-0400/01/02 = 32); "at the end of this file" does not — 15 findings, 2 decisions and 9 gate entries now sit below them |
| .agent/live_review.md | DECISION F082 D4 heading: "T003 moves to R9" | Superseded by DECISION F082 D5 in the same file. A historical decision record; no repair owed |

The other 55 hold, and the load-bearing ones were re-measured rather than read: R9's own
GATE-R9 claims reproduce exactly (change set 7 paths; insertions 252, 166, 4, 7, 21, 142;
294 and 184), the gauntlet's seven test files are untouched, `related=("stats.cost",
"stats.report")` both resolve in the catalog, `--history` occurs 0x in bench_cmd.py, and
`repair` is absent from the rendered column set.

## Authored-text proofs

Every slice was extracted from the COMMITTED `.agent/authored/f082-r10.md` via
`git show HEAD:.agent/authored/f082-r10.md` and applied disk-to-disk in python3. No slice
was retyped and none was taken from the scratchpad or the prompt after C0a.

| Slice | sha256 | bytes | lines | Applied-region proof |
|---|---|---|---|---|
| GATE-R9 | f8214cb5b5b301ed0b59cfec368f1bcaf3213c749d986e5e836eb0636db962de | 4154 | 1 | part of `post == pre + add`, TRUE |
| DECISION-D5 | 1a27d44ed9c2647adfb4495f1d090906e3c192ffc9dc863183016144020c17b7 | 1635 | 28 | part of `post == pre + add`, TRUE |
| LRSTEPS-FROM | 581f3940af46414b47da7da6f161c61b676965581a8d4d8088beac0863bf19c7 | 280 | 4 | 1x before / 0x after |
| LRSTEPS-TO | 98d6e0f301ff38e0b6cf826904519fb8f1cbe38b3d2092538f6c0056659dc4cb | 643 | 9 | 0x before / 1x after |
| INIT1-FROM | 06d2b0029d6aeea5f1bb6db857fc5520f9b24b542c80de2a9b05511d41bba762 | 53 | 2 | 1x before / 0x after |
| INIT1-TO | 22167fcd7ac9497250cf0a9177ff9693312b45914cce9c80038a7a4d4b15f67e | 72 | 3 | 0x before / 1x after |
| INIT2-FROM | 28699e3437ac36d13149b88b807448d97f72779e0ec6ec786bd4ba2c4f394f52 | 24 | 1 | 1x before / 0x after |
| INIT2-TO | 057e9652671404bfbce41c0809ad9e0894f11212de0ee1fe5f69646db78d7a67 | 35 | 1 | 0x before / 1x after |
| CATALOG-FROM | 9f34ec2ec4c3c764d4f553e66ab19a5c5f28667ef910d18f0a108e3a67741865 | 150 | 1 | 1x before / **1x after** (append-shaped: `FROM in TO`) |
| CATALOG-TO | 67dc7aaba61813170477677369143f55986d2a2e087adc3bb10e354c61b475f2 | 1206 | 23 | 0x before / 1x after |
| CTXSTEPS-FROM | 2297054912543f316d88c88d71fe0486f22b93b472a8d32a19d2d43915170b65 | 208 | 3 | 1x before / 0x after |
| CTXSTEPS-TO | 0ac4baa6b9380a813711b131f1b5f216f07931d4595403c5e2e66be02f1bf427 | 316 | 4 | 0x before / 1x after |
| PLAN | 697951df422842fd7a1504580da36615b56550ac929f1c13e386fcae95dd26ef | 2269 | 41 | `.agent/plan.md` byte-equals the slice as a WHOLE FILE |

NO transport marker line from the block reached any target file — 0 occurrences of either
marker in all 7 non-block targets. Trailing-whitespace scan over all 9 files: **ZERO**.
Every touched file ends in exactly one newline. `apps/cli/commands/bench_cmd.py` and
`tests/cli/test_stats_bench.py` are WORKER-AUTHORED code: the block specified their
BEHAVIOUR through Constraints 1–13 and dictated no source text.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror to last_block | done | |
| C1 GATE-R9 + DECISION-D5 | done | persisted FIRST, before any code commit |
| C2 LRSTEPS pair | done | |
| C3 bench_cmd + INIT1/INIT2/CATALOG | done | |
| C4 tests/cli/test_stats_bench.py | done | 25 tests |
| C5 CTXSTEPS + PLAN | done | |
| C6 handback | done | this file |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Gate 6 | done | |
| Gate 7 | done | |
| Gate 8 | done | |
| Gate 9 | done | |
| Gate 10 | done | 4 stale sentences surfaced, none repaired outside the ordered pairs |
| Gate 11 | done | measured before C6, stated as such |
| Gate 12 | done | |
| Gate 13 | done | |
| Gate 14 | done | no guard file edited |
| Gate 15 | done | |
| Gate 16 | done | |
| Gate 17 | done | |
| Gate 18 | done | 6 failed / 19 passed; worktree removed and pruned |
| Gate 19 | done | |
| Gate 20 | done | C6's own value in the completion report |

## Deviations, declared

1. **No Fortschritt line exists to repeat.** The Handback paragraph orders "The handoff
   repeats the Fortschritt line verbatim", but the R10 block contains no `Fortschritt: …`
   line (`grep -n "^Fortschritt" .agent/authored/f082-r10.md` → no match; its single
   "Fortschritt" occurrence is that instruction). Neither R8's nor R9's block nor R9's
   handoff carries one. This is the R-0371 class — a value ordered that does not exist at
   the moment of writing — so none is invented here. NOT registered as a finding: R10
   registers none by construction, and only the reviewer authors findings.
2. **Handoff length.** 200 lines against the 60-line cap, under the DECISION D15
   stated-cause allowance. The cause is mandated content only: seven per-commit tables,
   the twenty-gate verification table, gate 10's stale-sentence table, the thirteen-slice
   authored-text proof table and the twenty-eight-row item-status table. No section is
   dropped and no prose padding is added.
3. **Denied-command routes (R-0408).** `cp`, `cmp`, `echo $?` and compound shell chains
   are denied to this session class. Byte equality, transport and every FROM/TO property
   were proven with python3 `read_bytes()` plus `sha256`; exit codes came from python3
   `subprocess`; the CLI through `python3 -m apps.cli.main`.
4. **Commit messages carry no trailer**, matching every prior commit on this branch.
5. **`.agent/plan.md` is current only from C5 on.** The block's bundle puts the plan
   re-sync at C5, after the C0–C4 commits, so AGENTS.md Commit Gate item 1 is met by the
   bundle rather than at every intermediate commit. R-0377's counter-measure does not
   bind here: R10 registers, resolves and renumbers no finding, so the ledger this round
   commits is the one the round starts with.

## Next

The FIRST action of the next session is `docs/agents/self_drive_protocol.md`
**Phase 1 rule 1** — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate.

F082 is MID-FEATURE. No PR exists for `feature/f082-self-benchmark` and none is created
until closure; gate 19 proves `gh pr list --state open` is `[]`.

T001, T002 and T003a are built and gated. The next round is **R11 — T003b**:
model-context recording per run plus a fake-provider bench run end to end. It BEGINS WITH
AN INSPECT-THE-SHAPE PASS over the gauntlet's `run.json` writer — the field no run carries
yet is the risk — not with a change set. R12 is the integration gate, R13 closure.

Open findings: 47. Next free id: R-0418.
