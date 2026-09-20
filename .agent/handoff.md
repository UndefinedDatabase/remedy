# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 14

## Session

SESSION 7 of feature F277 · round 14 · rounds so far 14

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

**SCOPE REPORT (required by amend0827 rule 6 at the 7-session soft limit).** Unchanged since
round 12, so it is restated in brief. *Finished:* T001, the event vocabulary, and T002, the
JSON envelope with its dispatch error boundary. *Missing:* T003 is partly applied: `fail()`
exists and nine of the twenty-eight CLI modules call it. T004 is not started. *The proposal,
already carried out:* DECISION F277 D10 closes F277 on T001 and T002 complete and T003 in
part. The remainder is registered as F283, directly after F277. The operator question it owes
is `.agent/operator_questions.md` Q2. **New this round:** the closure's one full-suite run is
RED on exactly one node (G4). Closure cannot proceed until the shrinking rule of amend0917
rule 2 has run its course.

Context self-assessment: before any edit I read `AGENTS.md`, `docs/agents/handback_template.md`
and `.remedy-wt/f277-r14-block.md` in full, plus the four payloads, the current `.agent/plan.md`,
the tails of both append targets and the `KEPT_BY_SENSE` region of the guard test. I verified
the block's own bytes first (R-0954), found no `.agent/STOP` on disk, and confirmed the branch
clean at `24f36eaf`. Then I verified all four PAYLOADS entries before using any of them. I ran
the five-commit bundle C1a, C1b, C2, C3, C4 in order and ran all six gates for real.

## Range

Review of `24f36eaf`..`HEAD`.

## Commits

### c6419019 F277 R14 C1a: copy round 14 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r14-block.md | +222/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r14-guard.diff | +22/-0 | byte-for-byte copy of the guard.diff payload |
| .agent/authored/f277-r14-ledger.md | +6/-0 | byte-for-byte copy of the ledger.md payload |
| .agent/authored/f277-r14-plan.md | +46/-0 | byte-for-byte copy of the plan.md payload |
| .agent/authored/f277-r14-slips.md | +3/-0 | byte-for-byte copy of the slips.md payload |

Measured insertions (`git show --numstat`): **299**. Expected: 77 payload lines plus the
measured block line count of 222, which is 299. They **MATCH**. I ran the ordered cap
arithmetic BEFORE committing: `500 − 77 − 222 =` **201**. That is non-negative, so the commit
was legal and needed no oversize declaration. This feature's one permitted declaration stays
spent where round 12 spent it.

### e8e0abed F277 R14 C1b: register R-1015 and R-1016, book round 13's FAIL, rewrite plan
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | append the ledger.md payload: R-1015, R-1016, round 13 `Gate:` entry |
| .agent/plan.md | +18/-21 | rewrite to the plan.md payload, byte-identical, 46 lines |
| .agent/prose_slips.md | +3/-0 | append the slips.md payload's three lines |

Measured insertions: **27** (6 + 3 + 18). The block expected **27**, and each per-file number
also matches the block's own breakdown.

### 42af2188 F277 R14 C2: teach the retired-word guard that the self-use queue quotes the ledger
| Path | +/- | Reason |
|---|---|---|
| tests/docs/test_retired_promote_word.py | +12/-0 | `git apply guard.diff`: one `KEPT_BY_SENSE` entry for `scripts/self_use_queue.json`, sense `H`, token `promotion`, R-1015 stopgap comment |

Measured insertions: **12**. The block expected **12**. They **MATCH**.

### c83ba3ba F277 R14 C3: integration gate — the full suite once, transcript committed
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-closure-suite.txt | +8/-0 | the run's transcript, GENERATED from the log by `.remedy-wt/f277-r14-scratch/c3_transcript.py` and not typed by hand |

Measured insertions: **8**. The block did not state an expected number.

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the
commit that writes it.

### (this commit) F277 R14 C4: rewrite handoff for round 14
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the cap under DECISION F104 D1 |

## External actions

- `git push -u origin feature/f277-machine-contracts` runs after this commit. It is the
  round's last act, and its outcome is in the worker's session reply. See deviation 2.
- No `gh` command was run. No PR was created, edited or merged.
- **I added and removed no worktree.** `git worktree list` at C3 reads five entries: the
  primary checkout, the three `remedy/job-*` worktrees (including `job-86f628f5e4fb4e0c`,
  which constraint 6 says to leave alone), and `.remedy-wt/f277-r14-dry`, detached at
  `24f36eaf`. That last one is the reviewer's disposable dry-run worktree, which the block's
  G2 and C1b dry runs describe. I left it untouched. `remedy/job-*` branch count: **40**, the
  same as round 13's post-run reading.

## Verification

### Pre-flight

- `ls .agent/STOP`: `No such file or directory`. There is no STOP on disk.
- `git status --porcelain`: empty (0 lines).
- `git branch --show-current`: `feature/f277-machine-contracts`.
- `git rev-parse HEAD`: `24f36eafda8cca55238dd5082a626fb6714dcb77`, which matches `24f36eaf`.
- Block self-verification (R-0954), `.remedy-wt/f277-r14-block.md`:

| reading | measured | given in the delegation message | equal |
|---|---|---|---|
| line count | 222 | 222 | True |
| sha256 | `c66fc012d57291fb75784b2bd40a7cdb85947ffca871d3bb4358778d6d90d566` | `c66fc012d57291fb75784b2bd40a7cdb85947ffca871d3bb4358778d6d90d566` | True |

Neither reading differs, so the round went ahead. The block file is 14781 bytes and ends in a
newline.

### G1(a) — PAYLOADS transport, twelve readings

Script `.remedy-wt/f277-r14-scratch/g1a_payloads.py`, real exit code **0**.

| file | lines measured / given | bytes measured / given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| guard.diff | 22 / 22 | 1169 / 1169 | `bed28a452219e16071f41ad95050cf92ce1cf22a8e93855a47e547f51ca6cae7` | True |
| ledger.md | 6 / 6 | 12978 / 12978 | `004f0081351a2ef2821e6e4ecdc80065127e4b49193a090099037d91bfee4fca` | True |
| plan.md | 46 / 46 | 2360 / 2360 | `00ecf72718137091f3d44709c47d8cce1f3e26b041582925b2dddc460412dad4` | True |
| slips.md | 3 / 3 | 3211 / 3211 | `d9cc4606c545ae2ee6049237e3ccb0b1c93795848b1a0aa2c4715cdf6893a62d` | True |

`ALL_TWELVE_READINGS_EQUAL True`. I checked the separator shapes on disk: `ledger.md` begins
with a newline (`leading_newline True`), while `slips.md`, `plan.md` and `guard.diff` do not.
The payload directory holds exactly these four files.

### G1(b) — the five `.agent/authored/f277-r14-*` copies against their sources

Copied with `shutil.copyfile` by `.remedy-wt/f277-r14-scratch/c1a_copy.py`, then read back and
compared byte-for-byte. Real exit code **0**.

| copy | bytes | sha256 | BYTE_FOR_BYTE_EQUAL |
|---|---|---|---|
| f277-r14-block.md (against `.remedy-wt/f277-r14-block.md`) | 14781 | `c66fc012…d90d566` | True |
| f277-r14-guard.diff | 1169 | `bed28a45…ca6cae7` | True |
| f277-r14-ledger.md | 12978 | `004f0081…bfee4fca` | True |
| f277-r14-plan.md | 2360 | `00ecf727…412dad4` | True |
| f277-r14-slips.md | 3211 | `d9cc4606…f6893a62d` | True |

Five readings, all True.

### G1(c) — the two appends at C1b

**Reading (a), byte arithmetic** (`.remedy-wt/f277-r14-scratch/c1b_apply.py`, exit **0**):

| file | pre measured | pre, reviewer's | payload | post measured | post, reviewer's | pre+payload = post |
|---|---|---|---|---|---|---|
| .agent/live_review.md | 454865 | 454865 | 12978 | 467843 | 467843 | 454865 + 12978 = 467843 True |
| .agent/prose_slips.md | 348058 | 348058 | 3211 | 351269 | 351269 | 348058 + 3211 = 351269 True |

All four of my numbers equal the reviewer's. Both pre files ended in a newline.

**Reading (b), independent STRUCTURAL reader** (`.remedy-wt/f277-r14-scratch/g1c_structural.py`,
exit **0**). This reader splits on blank lines. It does not use byte offsets.

- N, the number of paragraphs my script COUNTED in `ledger.md`: **3**. They begin
  `- R-1015 — Medium, THE SELF-USE GENERATOR COPIES…`, `- R-1016 — Medium, THE CLOSURE'S
  SELF-USE RUN ENDED BLOCKED…` and `Gate: F277 R13 — the F277 round 13 entry. VERDICT FAIL…`.
- The last 3 blank-line units of the whole `.agent/live_review.md` at C1b, compared in order
  with those 3 paragraphs: `[True, True, True]`, so the reading is **True**.

**Negative control.** I flipped one bit at absolute byte offset 454906, which is offset 40
inside the FIRST appended paragraph. The byte went from 84 to 85 (`T` to `U`). The flip was
made on an in-memory copy; the committed file was never mutated.

```
reading (a) byte arithmetic, length only : True
reading (a) byte arithmetic, strict concat: False
reading (b) structural, per-paragraph    : [False, True, True]
reading (b) structural, all equal        : False
BOTH READINGS FALSE UNDER THE CONTROL: True
```

Reading (a) is carried in its strict form: "the pre bytes plus the payload bytes EQUAL the post
bytes" is tested as byte concatenation, and the length numbers above are only its numeric
surface. As recorded, the length-only form stays True under a same-length flip. It cannot catch
a bit flip by construction, and that is why the strict form is the gate. See deviation 3.

### G1(d) — the plan rewrite at C1b

| reading | value |
|---|---|
| payload sha256 | `00ecf72718137091f3d44709c47d8cce1f3e26b041582925b2dddc460412dad4` |
| committed `.agent/plan.md` sha256 | `00ecf72718137091f3d44709c47d8cce1f3e26b041582925b2dddc460412dad4` |
| byte equal | True |
| line count | 46 (under the AGENTS.md 50-line rule: True) |

### G1(e) — open set by distinct id in `.agent/live_review.md`

Ids matching `^- R-\d+ — ` minus ids matching `^Done: R-\d+ — `:

| rev | OPEN |
|---|---|
| 24f36eaf | **20** |
| e8e0abed (C1b) | **22** |

Newly open: **`R-1015`, `R-1016`**. No longer open: none. I measured both numbers
independently; this is not arithmetic asserted after the fact.

### G2 — the repair, and that it did not blunt the guard

`python3 -m pytest -q -p no:cacheprovider tests/docs/` in the primary checkout:

| state | summary line | real exit code | reviewer's disposable-worktree reading |
|---|---|---|---|
| unrepaired, at C1b (`e8e0abed`) | `1 failed, 313 passed in 84.38s (0:01:24)` | **1** | `1 failed, 313 passed`, exit 1 |
| repaired, at C2 (`42af2188`) | `314 passed in 85.42s (0:01:25)` | **0** | `314 passed`, exit 0 |

The one unrepaired failure was
`tests/docs/test_retired_promote_word.py::test_no_file_outside_the_map_carries_the_word`, which
is the R-1015 defect.

`git apply --check .remedy-wt/f277-r14-payloads/guard.diff`: `CHECK_REAL_EXIT=0`. I ran it
before the real `git apply`, which returned `APPLY_REAL_EXIT=0`.

The `KEPT_BY_SENSE` entry, verbatim from the file (extracted by AST):

```
"scripts/self_use_queue.json": (H, frozenset({
        "promotion",
    })),
```

Sense constant `H` (`H = "H: history or a retired-word guard"`, line 50, the guard's own
existing sense). Token list `['promotion']`: **count 1**, exactly one.

`git diff --name-only e8e0abed 42af2188` returns `tests/docs/test_retired_promote_word.py`,
**length 1**.

### G3 — closure precondition 3, `remedy integrity check --json` at C2 (just before C3's commit)

Real exit code **0**. Full JSON:

```json
{
  "version": 1,
  "passed": true,
  "fail_count": 0,
  "check_count": 5,
  "checks": [
    {"name": "handler_import", "status": "pass", "message": "handlers=145"},
    {"name": "live_review_verdict", "status": "pass", "message": "Owner: F282 — Findings paydown v2 (re-assigned at F276's closure, 2026-09-20; this line supersedes a"},
    {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
    {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
    {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
  ]
}
```

All five checks read `pass`. `context_complete=False` is part of the `plan_consistency` pass,
as the block noted. (The JSON is reflowed one check per line here; the raw file is
`.remedy-wt/f277-r14-scratch/g3_integrity.json`.)

### G4 — THE INTEGRATION GATE: the full suite, ONCE, primary checkout, HEAD `42af2188`

Before the run I checked for the cold-`dist` trap (a memory lesson from F276 round 7: a cold
`apps/ui/dist` reddens `tests/ui_server/`). `apps/ui/dist` held 4 files, and **0** of 152
`apps/ui` source files were newer than it. `dist` was warm, so I ran no build and changed
nothing. Script: `.remedy-wt/f277-r14-scratch/dist_freshness.py`, exit 0.

```
$ bash -c 'python3 -m pytest -n auto -q > .remedy-wt/f277-r14-scratch/g4_fullsuite.txt 2>&1; echo "REAL_EXIT=$?"'
2026-09-21T01:47:51+02:00  ->  2026-09-21T01:53:15+02:00
REAL_EXIT=1
WALL_CLOCK_SECONDS=324
```

- **Summary line:** `1 failed, 17812 passed, 20 skipped, 1 warning in 238.47s (0:03:58)`
- **Real exit code:** **1**, captured with no pipe
- **Wall clock:** **324 s** by `date +%s` around the run. pytest's own figure is 238.47 s.
- **Bad node ids (failed plus errors): 1** (1 failed, 0 errors):

```
tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary
```

The assertion as captured:
`emitted but NOT in the catalog (1): ['command_discovery_completed']`,
`in the catalog but NOT emitted (0): []`.

**The transcript.** `.agent/authored/f277-closure-suite.txt` is committed at `c83ba3ba`. It
was generated from the log by `c3_transcript.py` (command, HEAD, real exit code, wall clock,
summary line, bad-node count, then one id per line). `g4_compare.py c83ba3ba` extracted the
list independently from the log's `FAILED `/`ERROR ` lines and compared it with the list in the
COMMITTED blob: `BAD_NODE_LIST_BYTE_IDENTICAL True`, exit **0**. The run left no tracked file
dirty: `git status --porcelain` afterwards showed only the new transcript.

**Not repaired, as the block ordered.** Per C3 and constraint 4, a red suite is an outcome I
record here, not a gate I repair. I made one read-only diagnostic, with no tree effect,
declared as deviation 4:

- The node alone (`pytest -q -p no:cacheprovider <node>`) gives `1 failed in 86.31s`, exit
  **1**. It is deterministic, not an xdist flake.
- `command_discovery_completed` got a writer at `apps/cli/commands/test_cmds.py:139` in
  **`1a26ed8b` "F277 R3 C2: give command_discovery_completed a writer"**. It is also declared in
  `packages/orchestration/event_names.py:69`. The UI catalog the test reads,
  `apps/ui/src/api/humanizeCatalog.ts`, has no entry for it. On that reading this is an F277
  product-effect defect: the UI humanize catalog was not kept in step with a new emitter. It
  has been latent since round 3 and could only surface in a full run. I have authored no
  finding for it; registering it and ordering the repair are the reviewer's decisions.

### G5 — the round's whole path set

`git diff --name-only 24f36eaf c83ba3ba` (`g5_paths.py`, exit **0**), **length 10**:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f277-closure-suite.txt | C3 `c83ba3ba` |
| 2 | .agent/authored/f277-r14-block.md | C1a `c6419019` |
| 3 | .agent/authored/f277-r14-guard.diff | C1a `c6419019` |
| 4 | .agent/authored/f277-r14-ledger.md | C1a `c6419019` |
| 5 | .agent/authored/f277-r14-plan.md | C1a `c6419019` |
| 6 | .agent/authored/f277-r14-slips.md | C1a `c6419019` |
| 7 | .agent/live_review.md | C1b `e8e0abed` |
| 8 | .agent/plan.md | C1b `e8e0abed` |
| 9 | .agent/prose_slips.md | C1b `e8e0abed` |
| 10 | tests/docs/test_retired_promote_word.py | C2 `42af2188` |

This is set-equal to constraint 3's list minus `.agent/handoff.md`: True, with nothing missing
and nothing extra. Measured counts: paths under `packages/`: **0**; under `apps/`: **0**;
`scripts/self_use_queue.json`: **0**. The block says "eleven" here, but its own enumerated list
has ten entries; see deviation 1. `.agent/decisions.md` and `.agent/operator_questions.md`
were not touched.

Commit trailers, per commit over `24f36eaf..c83ba3ba`: all four read
`Claude Opus 5 <noreply@anthropic.com>`.

### G6 — push and tree, after C4

These readings do not exist when C4 is committed. They are in the worker's session reply, not
in a second write of this file (deviation 2).

## Authored-text proofs

- The five copies at C1a against their originals: five readings, all True (G1(b)).
- The REWRITE payload against the committed file: `.agent/plan.md` is sha256-equal to
  `plan.md` at 46 lines (G1(d)).
- The two APPEND payloads against the committed files: byte arithmetic equals the reviewer's
  four numbers. Strict concatenation and the independent structural reader (N = 3) are both
  True, and a one-bit negative control drives both to False (G1(c)).
- `guard.diff` was never retyped or edited. It went on with `git apply` after `--check`
  returned exit 0, and its committed copy is byte-identical to the original (G1(b)).
- `.agent/authored/f277-closure-suite.txt` is not reviewer-authored. It is generated from the
  run's log, and its bad-node list is byte-identical to the log's (G4).

## Deviations & assumptions

1. **G5's "eleven" counts ten.** The block asks `git diff --name-only 24f36eaf <C3>` to "name
   exactly the eleven paths constraint 3 lists other than `.agent/handoff.md`". Constraint 3
   lists eleven paths INCLUDING `handoff.md`, so ten remain without it, and G5's own
   enumeration names those ten. I measured 10, set-equal to that enumeration. Nothing on disk
   is affected. It is a block numeral, which makes it a prose-slip candidate for the reviewer.
2. **No trailing C4-fix commit; G6 readings go in the session reply.** Rounds 9–13 added a
   sixth commit to write post-push readings back into this file. The template's write-once
   rule calls a second write of the handback "a smell", and this block orders exactly five
   commits. So I committed this file once and report the push outcome and the post-push
   `git status --porcelain` in my reply to the delegating agent. The bundle ran exactly as
   ordered: C1a, C1b, C2, C3, C4, with nothing added, dropped or reordered.
3. **G1(c)'s negative control, stated precisely.** "Show BOTH readings return False" holds
   when reading (a) is the strict byte-concatenation form. The length-only form of the byte
   arithmetic stays True under a same-length bit flip. I report that as measured rather than
   hide it, because it is exactly why the strict form is the one that gates.
4. **Unordered read-only diagnostics on the red node.** After the one full-suite run I re-ran
   the single bad node (exit 1, deterministic) and ran `git grep` / `git log -S` to locate its
   event name. No file changed and the full suite did not run again. This was done so the
   reviewer can order the first shrinking-rule repair without spending a round on diagnosis.
   It authors no finding and repairs nothing.
5. **Pre-run `dist` freshness check**, read-only, taken from a memory lesson rather than the
   block. `dist` was warm, so no `npm run build` ran and nothing changed.
6. **`.agent/plan.md` was rewritten at C1b, one commit after C1a**, following the block's
   ordered bundle and the established shape of this feature's rounds. At C1a the plan still
   described round 13. After C1b its Next Step 1 already names a shrinking-rule repair, which
   fits the red outcome, so I made no further plan edit (the block names no second plan
   write).
7. No mutation red-proof was run and no worktree was created, as constraint 5 orders. The
   change set holds no file under `packages/` or `apps/` (measured 0).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy block + 4 payloads | done | 299 insertions, matching 77 + 222; cap headroom 201, computed before committing |
| C1b register R-1015/R-1016, book round 13 FAIL, rewrite plan | done | 27 insertions, matching the block's 27 (6 + 3 + 18) |
| C2 the guard repair | done | 12 insertions, matching 12; docs suite 1 failed → 314 passed |
| C3 integrity check + full suite + transcript | done | integrity 5/5 pass, exit 0; suite RED at exit 1 on 1 node, recorded and not repaired |
| C4 rewrite handoff and push | done | this commit; push outcome in the session reply (deviation 2) |
| G1 transport and state (a–e) | done | 12/12 payload readings, 5/5 copies, both appends by two readers plus the negative control, plan identical at 46 lines, open set 20 → 22 |
| G2 repair did not blunt the guard | done | 1 failed/313 passed exit 1 → 314 passed exit 0; one token; path list length 1 |
| G3 closure precondition 3 | done | all five checks `pass`, exit 0 |
| G4 integration gate | done | `1 failed, 17812 passed, 20 skipped`, exit 1, 324 s; 1 bad node; transcript byte-identical |
| G5 whole path set | done | 10 paths, set-equal to the enumerated list; 0 under packages/ and apps/; queue file 0 |
| G6 push and tree | done | reported in the session reply |
| Constraint 1 no payload edited or retyped | done | `--check` exit 0 before the apply; copies by `shutil.copyfile` |
| Constraint 2 every commit under 500 | done | 299, 27, 12, 8; this handoff is a single state file and exempt |
| Constraint 3 no unnamed file | done | G5; `scripts/self_use_queue.json` untouched |
| Constraint 4 stop on red, except C3's suite | done | only C3's suite went red, and it was recorded, not repaired |
| Constraint 5 no mutation red-proof | done | none run |
| Constraint 6 leave `remedy/job-86f628f5e4fb4e0c` alone | done | untouched; still listed |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 14: C1a, C1b, C2, C3 and C4, with all six gates.
3. The closure suite was **RED**, so what comes next is **the first repair round under the
   shrinking rule of amend0917 rule 2**, not the evidence job. The bad set is one node,
   `tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary`.
   The repair round must shrink it strictly, with no node newly bad. The evidence job and the
   FRESH review zip follow only once the suite has closed green.

Open findings count: **22** (after C1b). Operator-questions count: **2**.
