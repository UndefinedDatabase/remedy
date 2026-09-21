# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 15

## Session

SESSION 7 of feature F277 · round 15 · rounds so far 15

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

**SCOPE REPORT (required by amend0827 rule 6 at the 7-session soft limit).** Unchanged in
substance since round 12. *Finished:* T001, the event vocabulary, and T002, the JSON envelope
with its dispatch error boundary. *Missing:* T003 is partly applied — `fail()` exists and nine
of the twenty-eight CLI modules call it. T004 is not started. *The proposal, already carried
out:* DECISION F277 D10 closes F277 on T001 and T002 complete and T003 in part; the remainder
is registered as F283, directly after F277. The operator question it owes is
`.agent/operator_questions.md` Q2. **New this round:** the integration gate's one red node is
REPAIRED and the re-run of the full suite is at **real exit code 0** with **zero** bad nodes.
The shrinking rule of amend0917 rule 2 is satisfied in the FIRST of the three repair rounds it
allows. Closure's suite precondition is now met on the evidence of this round.

Context self-assessment: before any edit I read `AGENTS.md`, `docs/agents/handback_template.md`
and `.remedy-wt/f277-r15-block.md` in full, then all four payloads, the current `.agent/plan.md`
and the whole of `apps/ui/src/api/humanizeCatalog.ts` before the patch touched it. I verified
the block's own bytes first (R-0954), found no `.agent/STOP` on disk, and confirmed the branch
clean at `4a7877ba`. I then verified all four PAYLOADS entries before using any of them, ran the
bundle in the block's order, and ran all six gates for real.

## Range

Review of `4a7877ba`..`HEAD`.

## Commits

### 7ce9d6c8 F277 R15 C1a: copy round 15 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r15-block.md | +235/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r15-catalog.diff | +11/-0 | byte-for-byte copy of the catalog.diff payload |
| .agent/authored/f277-r15-ledger.md | +2/-0 | byte-for-byte copy of the ledger.md payload |
| .agent/authored/f277-r15-plan.md | +45/-0 | byte-for-byte copy of the plan.md payload |
| .agent/authored/f277-r15-slips.md | +2/-0 | byte-for-byte copy of the slips.md payload |

Measured insertions (`git show --numstat`): **295**. Expected: 60 payload lines plus the
measured block line count of 235, which is 295. They **MATCH**. I ran the ordered cap
arithmetic BEFORE committing: `500 − 60 − 235 =` **205**, non-negative, so the commit was legal
and needed no oversize declaration. This feature's one permitted declaration stays spent where
round 12 spent it.

### b367e02b F277 R15 C1b: book round 14's PASS and two reviewer slips, rewrite plan
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append the ledger.md payload: the round 14 `Gate:` entry, VERDICT PASS |
| .agent/plan.md | +16/-17 | rewrite to the plan.md payload, byte-identical, 45 lines |
| .agent/prose_slips.md | +2/-0 | append the slips.md payload's two lines |

Measured insertions: **20** (2 + 16 + 2). The block expected **20**, and each per-file number
also matches the block's own breakdown, including the plan rewrite's diff insertions of 16.

### 8d82ceb4 F277 R15 C2: give the humanize catalog the command discovery entry
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/humanizeCatalog.ts | +1/-0 | `git apply catalog.diff`: the `"command_discovery_completed"` entry, in alphabetical position directly after `"command.accepted"` |

Measured insertions: **1**. The block expected **1**. They **MATCH**.

### C3 — NO COMMIT. The red-proofs wrote nothing in the primary checkout
The block's own words: "If you have no change to commit here, say so and fold the readings into
the handback rather than inventing a file to touch — an empty commit is not this block's
intent." I had no change to commit, so I made none. The readings are in G3 below and the
missing commit is declared as deviation 1.

### 2ca1bdc0 F277 R15 C4: re-run the closure suite against the repaired tree
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-closure-suite.txt | +7/-7 | the re-run's transcript, in the same eight-line shape, now certifying `8d82ceb4` at exit 0 with no bad nodes |

Measured insertions: **7**. The block did not state an expected number.

### (this commit) F277 R15 C5: rewrite handoff for round 15
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the
commit that writes it.

## External actions

- `git worktree add --detach .remedy-wt/f277-r15-g3 8d82ceb4` — outcome: `Preparing worktree
  (detached HEAD 8d82ceb4)`, exit **0**. Removed at the end of C3 with
  `git worktree remove .remedy-wt/f277-r15-g3`, exit **0**. `git worktree list` afterwards reads
  five entries: the primary checkout, `.remedy-wt/f277-r14-dry` at `24f36eaf`, and the three
  `remedy/job-*` worktrees including `job-86f628f5e4fb4e0c`, which constraint 5 says to leave
  alone. I left it, and `.remedy-wt/f277-r14-dry`, untouched.
- `npm run build` in `apps/ui` (C4, best-effort) — exit **0**, `✓ built in 1.48s`.
- `git push -u origin feature/f277-machine-contracts` runs after this commit. It is the round's
  last act; its readings are in the worker's session reply, which is this handback's delivery
  surface. See deviation 2.
- No `gh` command was run. No PR was created, edited or merged.

## Verification

### Pre-flight

- `ls .agent/STOP`: `No such file or directory`, exit **2**. There is no STOP on disk.
- `git status --porcelain`: empty (0 lines).
- `git branch --show-current`: `feature/f277-machine-contracts`.
- `git rev-parse HEAD`: `4a7877ba7690b52941502772103d825eae403d64`, matching `4a7877ba`.
- Block self-verification (R-0954), `.remedy-wt/f277-r15-block.md`:

| reading | measured | given in the delegation message | equal |
|---|---|---|---|
| line count | 235 | 235 | True |
| sha256 | `75047674374245ffe2fc115ee77cc69bf23cf7da357c31baa66f55157fc22acc` | `75047674374245ffe2fc115ee77cc69bf23cf7da357c31baa66f55157fc22acc` | True |

Neither reading differs, so the round went ahead. The block file is 15734 bytes and ends in a
newline (235 newline bytes for 235 `splitlines()` lines).

### G1(a) — PAYLOADS transport, twelve readings

Script `.remedy-wt/f277-r15-scratch/g1a_payloads.py`, real exit code **0**.

| file | lines measured / given | bytes measured / given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| catalog.diff | 11 / 11 | 710 / 710 | `a9b88a27aad50f28935acabe24e705809bf4feec5819b823ad31fe7ce3b97df0` | True |
| ledger.md | 2 / 2 | 5668 / 5668 | `001cbadd00f4b3d51aafc145959365845e398a575b6796415ef243b0a27e5d19` | True |
| plan.md | 45 / 45 | 2356 / 2356 | `2d48e7729bffdff91d43079f64fc5bcb3e144b48a1194844411c9e632d0fc368` | True |
| slips.md | 2 / 2 | 2344 / 2344 | `b5936db13f0cd255272c5c558282c49d5a006d59db8064a9bfd2858e007be2a3` | True |

`all twelve readings equal: True`. Total payload lines **60**. The payload directory holds
exactly these four files.

### G1(b) — the five `.agent/authored/f277-r15-*` copies against their sources

Copied with `shutil.copyfile` (`c1a_copy.py`, exit **0**), then compared twice: once on the
working tree before the commit, and once — the stronger reading — by pulling each blob back OUT
of commit `7ce9d6c8` with `git show` and comparing it with the reviewer's original on disk
(`g1b_committed.py`, exit **0**).

| copy | committed bytes | sha256 (head) | equal to original |
|---|---|---|---|
| f277-r15-block.md (against `.remedy-wt/f277-r15-block.md`) | 15734 | `75047674374245ff` | True |
| f277-r15-catalog.diff | 710 | `a9b88a27aad50f28` | True |
| f277-r15-ledger.md | 5668 | `001cbadd00f4b3d5` | True |
| f277-r15-plan.md | 2356 | `2d48e7729bffdff9` | True |
| f277-r15-slips.md | 2344 | `b5936db13f0cd255` | True |

**Copies compared: 5. All True.** The chain makes no claim about the bytes emitted into the
worker's prompt, which this workflow cannot measure.

### G1(c) — the two appends at C1b

Byte arithmetic by strict CONCATENATION, not by length (`c1b_apply.py`, exit **0**):

| file | pre measured | pre, reviewer's | payload | post measured | post, reviewer's | pre+payload == post |
|---|---|---|---|---|---|---|
| .agent/live_review.md | 467843 | 467843 | 5668 | 473511 | 473511 | True |
| .agent/prose_slips.md | 351269 | 351269 | 2344 | 353613 | 353613 | True |

All four of my numbers equal the reviewer's four.

**Negative control**, on `.agent/live_review.md` only. I flipped one bit at absolute byte offset
467883 — offset 40 INSIDE the appended paragraph — on an in-memory copy; the committed file was
never mutated:

```
negative control (one bit flipped at offset 467883, inside the append):
  concat_equal=False   same_length=True
```

The strict reader returns **False** while the length stays identical, which is exactly the
round 14 finding that a length-only reader cannot catch a same-length flip. The gate is carried
in its strict form.

### G1(d) — the plan rewrite at C1b

| reading | value |
|---|---|
| payload sha256 | `2d48e7729bffdff91d43079f64fc5bcb3e144b48a1194844411c9e632d0fc368` |
| committed `.agent/plan.md` sha256 | `2d48e7729bffdff91d43079f64fc5bcb3e144b48a1194844411c9e632d0fc368` |
| byte equal | True |
| line count | 45 (under the AGENTS.md 50-line rule: True) |

### G1(e) — open set by distinct id in `.agent/live_review.md`

Ids matching `^- R-\d+ — ` minus ids matching `^Done: R-\d+ — `, each measured independently
(`g1e_openset.py`, exit **0**):

| rev | registered | done | OPEN |
|---|---|---|---|
| 4a7877ba | 29 | 7 | **22** |
| b367e02b (C1b) | 29 | 7 | **22** |

Ids added by round 15: **none**. Ids resolved by round 15: **none**. Round 15 registers and
resolves nothing, as the block states.

### G2 — the repair

`git apply --check .remedy-wt/f277-r15-payloads/catalog.diff` ran BEFORE the real apply:
exit **0**. The real `git apply`: exit **0**. Neither payload was edited nor retyped.

`python3 -m pytest -q -p no:cacheprovider tests/ui_contracts/test_humanize_catalog.py` in the
primary checkout at C2:

| state | summary line | real exit code |
|---|---|---|
| repaired, at C2 (`8d82ceb4`) | `12 passed in 88.99s (0:01:28)` | **0** |

The reviewer's disposable-worktree readings were `1 failed, 11 passed` at exit 1 unrepaired and
`12 passed` at exit 0 repaired. My repaired reading matches. I did not re-measure the
unrepaired state in the primary checkout — the full-suite transcript at `42af2188` and G3's two
mutations below already carry that direction.

`git diff --name-only b367e02b 8d82ceb4` returns exactly:

```
apps/ui/src/api/humanizeCatalog.ts
```

**Length 1.**

### G3 — THE RED-PROOFS, in the disposable worktree only

`git worktree add --detach .remedy-wt/f277-r15-g3 8d82ceb4`, exit **0**. This is production code
under `apps/`, so the proofs are mandatory. The contract test reads the TypeScript source as
text and needed no `node_modules`: it ran in the fresh worktree with no `--config` and no
install, so the R-0703 environment trap did not apply. **Every command below ran inside that
worktree; the primary checkout was not touched.**

| run | summary line | real exit code | FAILED node ids |
|---|---|---|---|
| unmutated CONTROL | `12 passed in 2.50s` | **0** | none |
| mutation (a) | `1 failed, 11 passed in 2.50s` | **1** | `tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary` |
| mutation (b) | `1 failed, 11 passed in 2.48s` | **1** | the same single node |
| restored CONTROL | `12 passed in 2.46s` | **0** | none |

**(a) an orphan catalog key.** I inserted `  "no_such_event_is_ever_emitted": "Nothing writes
this.",` directly above the new entry. The assertion names the direction:

```
E         emitted but NOT in the catalog (0): []
E         in the catalog but NOT emitted (1): ['no_such_event_is_ever_emitted']
```

Restore: `restored equal_to_original=True`, sha256
`20facd203d4013f12c9f167918934fa5bb324b27044e7bd96e27fc57346fd69c`, 6531 bytes — byte-identical
to the pre-mutation file, confirmed before the next mutation ran.

**(b) the key one character short.** I changed `"command_discovery_completed"` to
`"command_discovery_complete"`, which leaves the real emitter uncovered. The assertion names
BOTH directions, which is the sharper proof:

```
E         emitted but NOT in the catalog (1): ['command_discovery_completed']
E         in the catalog but NOT emitted (1): ['command_discovery_complete']
```

Restore: `restored equal_to_original=True`, same sha256 and byte count as above.

Neither mutation stayed green, so there is nothing to report under the block's "a mutation that
stays GREEN is a finding" clause. Mutation (a) reproduces the failure MODE of the original bad
node; mutation (b) reproduces the original bad node's exact message for
`command_discovery_completed`, which is the direct evidence that the C2 line — and not
something else in the tree — is what closed it.

`git status --porcelain` inside the mutation worktree after the restore: **empty (0 lines)**.
`git worktree remove .remedy-wt/f277-r15-g3`: exit **0**. `git worktree list` afterwards:

```
/home/decodeux/Repos/remedy                                  8d82ceb4 [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/f277-r14-dry          24f36eaf (detached HEAD)
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

The g3 worktree is gone; `job-86f628f5e4fb4e0c` is present and untouched.

### G4 — lint and canary

**Ruff was NOT run, and here is the measurement that says why.** The round's whole tracked path
set (`g4_pathset.py`, exit **0**) holds **11** paths and **0** of them end in `.py`:

```
python files in the path set: 0 []
```

So there is no Python file for `python3 -m ruff check` to read. This is the measured reason,
not a skipped gate: the only source file this round touches is TypeScript.

**The standing canary**, `python3 -m pytest tests/cli/test_golden_path.py -q`:

```
..........................................                               [100%]
42 passed in 130.27s (0:02:10)
```

Real exit code **0**.

### G5 — THE SUITE AND THE SHRINKING RULE

**`npm run build` in `apps/ui`** (C4, best-effort): it RAN and SUCCEEDED — neither a failure nor
a denial. Real exit code **0**, `vite v6.4.2`, `✓ 999 modules transformed`, `✓ built in 1.48s`,
emitting `dist/index.html`, `dist/assets/index-a38_yRwS.css`,
`dist/assets/diffHighlightGrammars-o9XqnLhb.js` and `dist/assets/index-DLlbqDm5.js`. Constraint
6 holds: `git status --porcelain` immediately after the build was **empty (0 lines)**, so it
left no TRACKED file dirty — everything it wrote is under the gitignored `apps/ui/dist`.

**The suite**, primary checkout, HEAD `8d82ceb4`, redirected to a file with NO pipe:

```
$ bash -c 'S=$(date +%s); python3 -m pytest -n auto -q > .remedy-wt/f277-r15-scratch/c4_suite.txt 2>&1; RC=$?; E=$(date +%s); echo "REAL_EXIT=$RC"; echo "WALL_SECONDS=$((E-S))"'
REAL_EXIT=0
WALL_SECONDS=326
```

- **Summary line:** `17813 passed, 20 skipped, 1 warning in 240.52s (0:04:00)`
- **Real exit code:** **0**, captured without a pipe
- **Wall clock:** **326 s** by `date +%s` around the run; pytest's own figure is 240.52 s
- **Bad node ids (failed plus errors): 0**, derived independently from the log's `FAILED `/
  `ERROR ` lines, of which there are **0**. The list is EMPTY.

**THE SHRINKING RULE, both readings, as sets I computed** (`g5_confirm.py`, exit **0**):

```
PREVIOUS bad set: ['tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary']
NEW bad set:      []
new is a STRICT SUBSET of previous: True
newly bad (new minus previous):     []
```

The new set is the empty set; the previous set had one element; the empty set is a strict subset
of a one-element set, and the difference `new − previous` is empty, so **no node is newly bad**.
The passed count moved 17812 → 17813 with skips unchanged at 20, which is the same one node
crossing from failed to passed and nothing else moving. I state these as computed sets; the
verdict on them is the reviewer's.

**The transcript.** `.agent/authored/f277-closure-suite.txt` is committed at `2ca1bdc0`, in the
same eight-line shape it already had. Its bad-node region reads `no bad nodes` under
`bad node ids (failed plus errors): 0`, and the comparison against the list extracted
independently from the log is `BAD_NODE_LIST_BYTE_IDENTICAL: True`, with the declared count
equal to the measured count.

**The round's whole tracked path set**, `git diff --name-only 4a7877ba 2ca1bdc0`, **length 10**,
plus `.agent/handoff.md` at C5 for **11** — set-equal to constraint 3's enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f277-closure-suite.txt | C4 `2ca1bdc0` |
| 2 | .agent/authored/f277-r15-block.md | C1a `7ce9d6c8` |
| 3 | .agent/authored/f277-r15-catalog.diff | C1a `7ce9d6c8` |
| 4 | .agent/authored/f277-r15-ledger.md | C1a `7ce9d6c8` |
| 5 | .agent/authored/f277-r15-plan.md | C1a `7ce9d6c8` |
| 6 | .agent/authored/f277-r15-slips.md | C1a `7ce9d6c8` |
| 7 | .agent/live_review.md | C1b `b367e02b` |
| 8 | .agent/plan.md | C1b `b367e02b` |
| 9 | .agent/prose_slips.md | C1b `b367e02b` |
| 10 | apps/ui/src/api/humanizeCatalog.ts | C2 `8d82ceb4` |
| 11 | .agent/handoff.md | C5, this commit |

Nothing missing, nothing extra. `scripts/self_use_queue.json` appears **0** times.
`.agent/decisions.md` and `.agent/operator_questions.md` were not touched.

Commit trailers over `4a7877ba..2ca1bdc0`, read per commit: all four end in exactly
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.

### G6 — push and tree, after C5

These readings do not exist when C5 is committed, and the block forbids a trailing commit for
them. They are reported after the push in the worker's session reply, which is this handback's
delivery surface and the same place round 14 put them (deviation 2).

## Authored-text proofs

- The five copies at C1a, read back OUT of commit `7ce9d6c8` and compared with the reviewer's
  originals on disk: **five readings, all True** (G1(b)).
- The REWRITE payload against the committed file: `.agent/plan.md` is sha256-equal to `plan.md`
  at 45 lines (G1(d)).
- The two APPEND payloads against the committed files: strict byte concatenation True for both,
  with all four byte numbers equal to the reviewer's, and a one-bit negative control inside the
  appended paragraph driving the strict reader to False at unchanged length (G1(c)).
- `catalog.diff` was never retyped or edited. It went on with `git apply` after `--check`
  returned exit 0, and its committed copy is byte-identical to the original (G1(b)).
- `.agent/authored/f277-closure-suite.txt` is not reviewer-authored. It is a rewrite in the
  file's existing shape from this round's own run, and its bad-node list is byte-identical to
  the list derived independently from the log (G5).

## Deviations & assumptions

1. **C3 is ABSENT from the commit sequence: the bundle ran C1a, C1b, C2, C4, C5 — five commits,
   not six.** The block ordered six but also ruled the case: C3 "writes NOTHING in the primary
   checkout" and "an empty commit is not this block's intent", so with no change to commit I made
   no commit. C3's readings are in G3 above, in full. Nothing else was added, dropped or
   reordered. Recorded here because a dropped commit is a deviation even when the block sanctions
   it (R-0485).
2. **No trailing commit for G6; its readings go in the session reply.** The block orders the
   readings "into the handback's own gate section AFTER pushing rather than adding a trailing
   commit". A file cannot carry the outcome of pushing itself without a second write, which the
   template's write-once rule and the block's own "no trailing commit" both refuse. Round 14
   resolved this the same way and the round 14 ledger entry describes that choice as putting the
   readings "in the handback itself", so the session reply is the surface the reviewer reads as
   the handback. I committed this file once and report the push outcome, the post-push
   `git status --porcelain` and `git worktree list` there.
3. **G2's unrepaired reading was not re-measured in the primary checkout.** The block reports the
   reviewer's own disposable-worktree pair; I measured only the repaired side there, because the
   unrepaired direction is already carried twice over — by the committed `42af2188` transcript and
   by G3's mutation (b), which reproduces the original assertion text exactly.
4. **`npm run build` ran even though it was best-effort.** It succeeded at exit 0 and left no
   tracked file dirty, so there is no failure or denial to report under C4's either-way clause.
5. **`.agent/plan.md` was rewritten at C1b, one commit after C1a**, per the block's ordered
   bundle. At C1a the plan still described round 14. After C1b it already names the green
   outcome's consequence in Next Step 1, so I made no further plan edit — the block names no
   second plan write and the outcome landed on the branch the plan predicted.
6. **Scratch and payload hygiene.** Every log, driver script and exit-code capture is under
   `.remedy-wt/f277-r15-scratch/`; I wrote nothing into `.remedy-wt/f277-r15-payloads/`. Both are
   gitignored, and `git status --porcelain` is empty at every commit boundary.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy block + 4 payloads | done | 295 insertions, matching 60 + 235; cap headroom 205, computed before committing |
| C1b book round 14 PASS + 2 slips, rewrite plan | done | 20 insertions, matching the block's 20 (2 + 16 + 2) |
| C2 the catalog repair | done | 1 insertion, matching 1; contract test `12 passed` at exit 0 |
| C3 the red-proofs | deviated | no commit: nothing changed in the primary checkout, per the block's own clause; readings in G3 (deviation 1) |
| C4 re-run the closure suite | done | 7 insertions; suite exit 0, `17813 passed, 20 skipped`, 0 bad nodes |
| C5 rewrite handoff and push | done | this commit; push readings in the session reply (deviation 2) |
| G1 transport and state (a–e) | done | 12/12 payload readings, 5/5 committed-blob copies, both appends by strict concatenation plus the negative control, plan identical at 45 lines, open set 22 → 22 |
| G2 the repair | done | `--check` exit 0; `12 passed` exit 0; path list length 1 |
| G3 the red-proofs | done | control 12 passed exit 0; (a) and (b) each `1 failed, 11 passed` exit 1 at the named node; both restores byte-identical; worktree removed |
| G4 lint and canary | done | ruff not run — 0 Python files in an 11-path set, measured; canary `42 passed` exit 0 |
| G5 suite and shrinking rule | done | build exit 0; suite exit 0, 326 s, 0 bad nodes; new set ⊊ previous set True; newly bad none; transcript list byte-identical |
| G6 push and tree | done | reported in the session reply after the push (deviation 2) |
| Constraint 1 no payload edited or retyped | done | `--check` exit 0 before the apply; copies by `shutil.copyfile` |
| Constraint 2 every commit under 500 | done | 295, 20, 1, 7; this handoff is a single state file and exempt |
| Constraint 3 no unnamed file touched | done | G5: 11 paths, set-equal to the enumeration |
| Constraint 4 stop on red | done | no gate went red; C4's suite came back at exit 0, so its stated exception was never needed |
| Constraint 5 leave `job-86f628f5e4fb4e0c` and the queue alone | done | untouched and still listed; `scripts/self_use_queue.json` appears 0 times in the path set |
| Constraint 6 build leaves no tracked file dirty | done | `git status --porcelain` empty immediately after the build |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 15: C1a, C1b, C2, C4 and C5, with all six gates and the absent C3
   (deviation 1).
3. The closure suite came back **GREEN at real exit code 0 with zero bad nodes**, and the
   shrinking rule is satisfied in the first of its three rounds, so what comes next is **the
   evidence job** (`create_manual_completion_bundle`, feature-scoped) and a **FRESH review zip**,
   whose `base_commit` is the branch's FORK POINT `f2494c02` — not a merge-base — with the two
   `rev-list` counts required to agree. The second repair round is NOT needed and should not be
   ordered.

Open findings count: **22**. Operator-questions count: **2**.
