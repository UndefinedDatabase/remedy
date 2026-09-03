# Handoff — F109 Semantic dedupe, SESSION 3, round 11

## Session

`SESSION 3 of feature F109 · round 11 · rounds so far 11`

Soft limit is 25 rounds / 7 sessions (self-drive protocol G7, amend0827 rule 6).
At 11 rounds and 3 sessions the limit is NOT reached, so no scope report is due.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

## Range

Review of `c22818f59e6f52ea79b10cb0f36390c5070322c7`..`d70d9b6a` (plus the
handoff commit that carries this file).

## THE ROUND ENDS RED — READ THIS FIRST

**G5(a) CONTROL and G6 are RED, and I stopped rather than routing around them.**
C4 is correct and does exactly what `R-0774` ordered, but it falsifies the
SELECTORS of two tests that had silently assumed "exactly one builder trace per
role per round". The block's constraint 6 forbids editing any existing line of
`tests/orchestration/test_semantic_dedupe.py`, and `tests/orchestration/test_prompt_trace.py`
is not in the change set at all, so neither test could be repaired inside this
round's authority. Per the standing order — "if a gate goes red, do not route
around it: stop, write the handback with the real result, and end" — C4 and C5
are committed and pushed as they stand, the branch is red, and the repair is
round 12's to authorize.

Nothing was reverted (a revert is outside the block's bundle and change set) and
no test was deleted, weakened or edited to produce a colour.

The two failing nodes:

| Suite | Node | Why C4 falsifies it |
|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | `TestAResumeFallbackSendsFullContent::test_the_recorded_builder_row_describes_the_bytes_that_were_sent` | builds `traces = {trace.round: ... for trace in result.prompt_traces if trace.role == "builder"}` — a dict keyed by round, so the LAST trace of a round wins. Round 2 now has two builder traces, so `traces[2]` is the full-content composition (which replaced nothing) instead of the abandoned one, and the positive control `assert replaced` sees `[]`. |
| `tests/orchestration/test_prompt_trace.py` | `TestSegmentManifest::test_the_reviewer_call_site_hands_its_composition_down` | a text-POSITIONAL wiring guard: `site = source.split("result.prompt_traces.append(build_trace_entry(")[2]` and its docstring "Index [2] is the reviewer's append; [1] is the builder's". C4 inserts a third append earlier in the file, so index [2] is now the builder fallback's. |

Neither is a defect in C4. Both are readers that encoded the very assumption
`R-0774` exists to break.

**THE MINIMAL REPAIR, MEASURED, NOT PROPOSED FROM READING.** I verified it in the
disposable worktree and threw it away — nothing below is committed:

1. `test_semantic_dedupe.py`: `for trace in result.prompt_traces` →
   `for trace in reversed(result.prompt_traces)`, so the FIRST (abandoned)
   builder trace of each round wins instead of the last. One line.
2. `test_prompt_trace.py`: split index `[2]` → `[3]`, and the docstring sentence
   updated to say `[3]` is the reviewer's and `[2]` the builder fallback's. One
   line plus its comment.

With both applied: `test_semantic_dedupe.py` **125 passed, exit 0** and
`test_prompt_trace.py` **46 passed, exit 0**. Neither edit weakens an assertion;
each repairs a selector. This is the `R-0749`/`R-0773` shape a third time — a
round makes prose and readers false without touching them.

## Commits

### 039af7a5 F109 R11 C0a: save the round 11 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f109-r11.md` | +365/-0 | the block, `cp`-ied from `.remedy-wt/f109-r11.md`, never retyped |

### a8e1fb7e F109 R11 C0b: mirror the round 11 block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +322/-257 | `cp` of the authored copy |

### bcd91216 F109 R11 C1: advance the plan to round 11
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12/-15 | SLICE PLAN applied byte for byte |

### 4721f5ec F109 R11 C2: book the round 10 gate and register R-0773 and R-0774
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +7/-1 | SLICE RECORD appended verbatim; no `Done:` paragraph and no verdict of my own (constraint 3) |

### 6c39b579 F109 R11 C3: state the landed dedupe config plumbing in all three docstrings
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_loop.py` | +15/-6 | SPEC X pairs X1 (1 site) and X2 (2 sites), docstring prose only |

### 498d98dc F109 R11 C4: trace the bytes a builder resume fallback actually sends
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_loop.py` | +41/-0 | SPEC Y, Builder half only (see deviation 2) + a deliberate-absence note on the Reviewer side |

### d70d9b6a F109 R11 C5: pin one prompt trace per actual provider invocation on both roles
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | +153/-0 | SPEC Z, one class appended at the very end, zero existing lines touched |

### C6 — the commit carrying this file
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | — | this handback; a handoff cannot table the commit that writes it (R-0149) |

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | deviated | SPEC Y's Builder append landed; its Reviewer append did NOT — the Reviewer already records the second trace and a third would double-count one call (deviation 2). One extra comment-only insertion on the Reviewer side (deviation 3). |
| C5 | done | all three SPEC Z cases land and pass; case 2's discriminator is the Reviewer's existing callback rather than a new append (deviation 2) |
| C6 | done | this file |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f109-r11-colour d70d9b6a` | ok, detached at C5 |
| `git worktree remove .remedy-wt/f109-r11-colour` | ok |
| `git worktree prune` | ok; list holds only the primary checkout and the four pre-existing `remedy/job-*` worktrees |
| `git push -u origin feature/f109-semantic-dedupe` | see the push line at the end |

No PR created, no PR merged, no branch created or switched, no force-push, no
history rewrite. Stayed on `feature/f109-semantic-dedupe` throughout.

## Verification — all eight gates, real exit codes

**G1 TRANSPORT — PASS, exit 0.** `sha256sum .remedy-wt/f109-r11.md
.agent/authored/f109-r11.md .agent/last_block.md` prints ONE digest three times:
`e0680ae71ed34a6646d070c82bb7737ee703f02b5a97202fe6bdd077575cafab`. This chain
compares the scratch original against the saved copy against its mirror and
claims nothing about any earlier bytes.

**G2 THE PLAN — PASS.** SLICE PLAN extracted mechanically from
`.agent/authored/f109-r11.md` by delimiter-line index; `cmp` against
`.agent/plan.md` gave no output, exit 0. `wc -l .agent/plan.md` = **42** (< 50).
`grep -c '^## Goal'` = **1**, `grep -c '^## Next Steps'` = **1**, both exit 0.
The extractor was validated against the round 10 precedent first: extracting R10's
SLICE PLAN the same way reproduces `.agent/plan.md` at `c22818f5` byte for byte
(True), which is what fixed the trailing-newline convention — the slice carries
the newline that terminates its own last content line.

**G3 THE RECORD APPEND — PASS, all four readings.**
- (a) ARITHMETIC. Base size **2070660**, base sha256
  `041feb66b7c3c31f7d514ffed307d7eeecca0e1d3c2890e6398004cb81bac5b8`. Appended
  length S after stripping trailing newlines = **9075**. New size **2079735**;
  base + S = 2079735; **arithmetic holds: True**. New sha256
  `6efe5b0613b4308224f94c397653ab2c5d6efa1f41f563133bd520fe83d56918`. The file
  still ends WITHOUT a trailing newline (True).
- (b) SECOND READER, counts no byte. Split the WHOLE file on blank-line
  boundaries into units; N derived from the payload itself = **3**; the LAST 3
  units equal the appended paragraphs IN ORDER (True), exit 0. First characters:
  `Gate: F109 R10 — the round 10 entry. VERDICT PASS, AND EVERY`,
  `- R-0773 — Low, \`packages/orchestration/pingpong_loop.py\` ST`,
  `- R-0774 — Medium, ON EVERY RESUME FALLBACK THE PROMPT TRACE`.
- (c) NEGATIVE CONTROL, on the scratch copy
  `.remedy-wt/negctl_r11_live_review.md` and never on the tracked file. Flipped
  ONE byte at offset 2070684, inside the FIRST appended paragraph (`' '` →
  `'\x00'`). Reader (b) **REJECTED** it, exit 1, naming the mismatch at unit 1,
  while it had ACCEPTED the tracked file at exit 0. Tracked sha256 before
  `6efe5b06…` and after `6efe5b06…` — identical, it did not move. Copy deleted by
  exact path; `ls .remedy-wt/negctl_r11_live_review.md` → "No such file or
  directory", exit 2.
- (d) COUNTS, every base read from `git show c22818f5…:.agent/live_review.md`
  and never by rewinding the tracked file. `^Gate: F109 R10 — ` = **1**.
  `^- R-0773 — ` = **1**. `^- R-0774 — ` = **1**. `^- R-[0-9]\{4\} — ` = **335**
  against **333** at base. `^Done: R-[0-9]\{4\} — ` = **65**, UNCHANGED at 65,
  because this round resolves nothing.

**G4 THE EDIT SHAPE — (b), (c), (d) PASS; (a) RED AS ORDERED, and the gate itself
is unmeetable. SPEC X was NOT misapplied — proven below.**
- (a) ACROSS C3, `ast.dump(tree, include_attributes=False)` before vs after:
  **NOT equal, exit 1.** The block says this "MUST BE EQUAL … a docstring is an
  expression" and that inequality means SPEC X was misapplied. That inference is
  false: `include_attributes=False` suppresses `lineno`/`col_offset` only, and
  still renders every `Constant` VALUE — and a docstring IS a `Constant`. **So no
  docstring-only edit can ever satisfy this gate.** CONTROL PROVING IT: a
  one-word docstring edit on a three-line module (`"""one"""` → `"""two"""`) also
  gives `ast.dump` equal = **False**. What DOES hold, and is the property the
  gate names ("SPEC X changes docstring prose and no executable statement"):
  node counts identical at **23625 == 23625** (nothing added or removed); exactly
  **3** differing `Constant` leaves, all `str`, and they are precisely SPEC X's
  three docstrings (`_dedupe_resumed_segments`, `compose_builder_prompt`,
  `compose_reviewer_prompt`) — the `Expr`/`FunctionDef`/`Module` entries in the
  differing-type list are only the ancestors containing them; and **`ast.dump`
  WITH EVERY DOCSTRING STRIPPED is EQUAL (True)**. I did not stop on this, because
  the block's stop clause is conditioned on SPEC X having been misapplied and that
  antecedent is measurably false. Declared as deviation 1.
- (b) ACROSS C4, `difflib.SequenceMatcher(None, before, after, autojunk=False)`
  over line sequences: opcodes `[('insert', 3416, 3416, 3416, 3446), ('insert',
  3751, 3751, 3781, 3792)]`. Every non-equal opcode is an `insert` (True); none is
  `replace` or `delete`. **TOTAL LINES DELETED: 0.** Exit 0.
- (c) ACROSS C5, same reading over the test file: **one** opcode,
  `[('insert', 1895, 1895, 1895, 2048)]`, at index 1895 == the before-file's line
  count, so it is AT THE END (True). **TOTAL LINES DELETED: 0.** Exit 0.
- (d) THE ZERO-GATE, scoped to `packages/orchestration/pingpong_loop.py` alone:
  `grep -c 'config plumbing that supplies'` = **0** after C3 (grep exit 1, which
  is what a zero count returns), against **2** at `c22818f59e6f52…`, exit 0.
  SPEC X's own obligations also held exactly: X1 FROM 1 → 0, TO 1; X2 FROM 2 → 0,
  TO 2.

**G5 THE COLOUR — IMPORT PROBE PASS; (a) CONTROL **RED**; (b) and (c) both
produce their ordered colour.** Worktree added by exact path
`.remedy-wt/f109-r11-colour`, detached at C5. `__pycache__` purged before every
run (0 dirs found each time); every process `python3 -B -m pytest … -p
no:cacheprovider`.
- IMPORT PROBE, run FIRST: `python3 -B -c "import
  packages.orchestration.pingpong_loop as m; print(m.__file__)"` with the
  worktree as cwd printed
  `/home/decodeux/Repos/remedy/.remedy-wt/f109-r11-colour/packages/orchestration/pingpong_loop.py`
  — INSIDE the worktree, exit 0. No editable install shadows it; the gate is not
  void.
- (a) CONTROL, unmutated: **exit 1 — 1 failed, 124 passed.** The failure is
  `TestAResumeFallbackSendsFullContent::test_the_recorded_builder_row_describes_the_bytes_that_were_sent`,
  the selector break described at the top of this file. BASELINE ESTABLISHING THE
  CAUSE: the same suite at **C3** (`6c39b579`, i.e. before C4) is **122 passed,
  exit 0** — exactly the block's own base reading — so C4 is definitively the
  cause and nothing was already broken.
- (b) MUTATION A, deleting the BUILDER's new `build_trace_entry` append from the
  fallback branch. Bytes counted before writing: occurrences of the target string
  in that file = **1**. Result **exit 1**, 1 failed / 124 passed, and the named
  node `TestATraceIsRecordedForEveryProviderInvocation::test_a_builder_resume_fallback_records_the_bytes_it_actually_sent`
  FAILS on `assert len(traces) == 2` with `AssertionError: [808]` — 808 being the
  abandoned resumed prompt, so the defect is restored exactly. Re-run alone:
  exit 1, 1 failed. ORDER THE COLOUR, NOT THE COUNT: the mutated totals (1 failed
  / 124 passed) coincide with the control's, but the failing SET differs — under
  mutation A the selector test passes again and SPEC Z case 1 fails, which is the
  same tension from the other side.
- (c) MUTATION B. The block orders "delete the REVIEWER's new append"; there is
  no such append (deviation 2), so I mutated the thing that actually makes SPEC Z
  case 2 hold on that role — the `on_call=_rev_trace(...)` argument on the
  Reviewer fallback's `_call_with_retry`. Bytes counted before writing:
  occurrences of the (longer, unique) target string = **1**. Result **exit 1**,
  2 failed / 123 passed, and the named node
  `…::test_a_reviewer_resume_fallback_records_the_bytes_it_actually_sent` FAILS on
  `assert len(traces) == 2` with `AssertionError: [1741]` — only the abandoned
  resumed trace survives. Re-run alone: exit 1, 1 failed.
- CLEANUP: `packages/orchestration/pingpong_loop.py` restored from the C5 blob by
  exact path after each mutation; `git status --porcelain` inside the worktree
  **EMPTY** before removal; worktree removed and pruned; `git worktree list` now
  holds only `/home/decodeux/Repos/remedy` and the four pre-existing
  `remedy/job-48a379ab5ca44ec5`, `remedy/job-7d1c93e2dc98415a`,
  `remedy/job-98e9364a83a34872`, `remedy/job-f76686b8435640e9`.

**G6 THE SUITES — RED: 13 of 15 exit 0, TWO exit 1.** Run SERIALLY, one process
started, finished, and only then the next. Base readings in parentheses.

| Suite | base | mine | exit |
|---|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | (122) | **1 failed, 124 passed** | **1** |
| `tests/orchestration/test_prompt_trace.py` | (46) | **1 failed, 45 passed** | **1** |
| `tests/orchestration/test_pingpong_cli.py` | (173) | 173 passed | 0 |
| `tests/orchestration/test_pingpong.py` | (34) | 34 passed | 0 |
| `tests/orchestration/test_session_resume.py` | (27) | 27 passed | 0 |
| `tests/orchestration/test_token_ledger.py` | (120) | 120 passed | 0 |
| `tests/orchestration/test_token_truth.py` | (37) | 37 passed | 0 |
| `tests/orchestration/test_token_truth_v1_contract.py` | (101) | 101 passed | 0 |
| `tests/orchestration/test_job_evidence.py` | (93) | 93 passed | 0 |
| `tests/orchestration/test_provider_evidence_integration.py` | (64) | 64 passed | 0 |
| `tests/orchestration/test_cost_report.py` | (22) | 22 passed | 0 |
| `tests/ui_server/test_prompt_trace_payload.py` | (20) | 20 passed | 0 |
| `tests/ui_server/test_prompt_trace_lens.py` | (13) | 13 passed | 0 |
| `tests/test_observability_index.py` | (14) | 14 passed | 0 |
| `tests/cli/test_golden_path.py` | (42) | 42 passed | 0 |

WHICH MOVED: `test_semantic_dedupe.py` 122 → 124 passed + 1 failed (+3 new SPEC Z
cases, −1 to the selector break). `test_prompt_trace.py` 46 → 45 passed + 1
failed, and it moved WITHOUT being touched by the change set. **The block's own
G6 design is what caught it** — the list names the suites the change set can
REACH, not only the ones expected to move, which is exactly the `R-0772`
counter-measure. Had the list named only the dedupe suite, the
`test_prompt_trace.py` break would have shipped invisibly. No other suite moved.

**G7 THE TREE — PASS.** `git status --porcelain` **EMPTY**, exit 0.
`git ls-files .remedy-wt` returns **nothing**, exit 0. Insertions, the `+` column
only per AGENTS.md DECISION F104 D1 — never insertions plus deletions, never a
before/after line count of a rewritten file:

| Item | sha | ins(+) | < 500 |
|---|---|---|---|
| C0a | `039af7a5` | 365 | yes |
| C0b | `a8e1fb7e` | 322 | yes |
| C1 | `bcd91216` | 12 | yes |
| C2 | `4721f5ec` | 7 | yes |
| C3 | `6c39b579` | 15 | yes |
| C4 | `498d98dc` | 41 | yes |
| C5 | `d70d9b6a` | 153 | yes |

Every commit single-parent, and the chain is unbroken back to base:
`d70d9b6a←498d98dc←6c39b579←4721f5ec←bcd91216←a8e1fb7e←039af7a5←c22818f5`.
**I RAN THE CELL-BY-CELL COMPARISON** of these seven sha/insertion/path rows
against the `## Commits` tables above and they agree in every cell. This
handback commit's own insertion count is quoted nowhere here; the reviewer
measures that one.

**G8 THE STALENESS SWEEP — RUN, and it FOUND THINGS.** (`R-0417`'s standing
counter-measure.) Every file this round touched, re-read end to end:

| File | Sentence stating a count / module list / round map / completion | Still holds? |
|---|---|---|
| `packages/orchestration/pingpong_loop.py` | l.3692 "F005 Finding 2: ONE prompt trace per ACTUAL provider call … so reviewer traces == reviewer attempts" | **YES**, and C4 makes it true of the Builder for the first time |
| `packages/orchestration/pingpong_loop.py` | l.3340 SAFE POINT 2 "no prompt trace of a call that did not happen" | YES — C4 appends only inside the fallback branch, after the recomposition |
| `packages/orchestration/pingpong_loop.py` | l.3213 "one index per RUN, not per round" | YES, untouched |
| `packages/orchestration/pingpong_loop.py` | the three passages C3 rewrote | YES — that was C3's whole purpose; `grep -c` = 0 (G4d) |
| `tests/orchestration/test_semantic_dedupe.py` | l.1494 "the round 2 Builder trace records the manifest of the composition the fallback ABANDONED" | **FALSIFIED BY IMPLICATION** — the definite article now names one of TWO; the FIRST still does. This is the sentence sitting on the failing selector. |
| `tests/orchestration/test_semantic_dedupe.py` | l.1870 "the round 2 Builder trace describes the composition the fallback ABANDONED, not the bytes that left the loop" | **FALSIFIED BY IMPLICATION**, same shape; the case itself still passes because it reads the CALLS, not the traces |
| `tests/orchestration/test_semantic_dedupe.py` | l.1748-1752 header "THE RESUME FALLBACK IS OUTSIDE THE SWITCH BY CONSTRUCTION" | YES — C4 changes what is RECORDED, not what is composed or sent |
| `tests/orchestration/test_semantic_dedupe.py` | l.2038 "one trace per role per round", new in C5 | YES, and it is asserted, not merely stated |
| `.agent/plan.md` | "the fix appends a second trace in each role's fallback branch" | **FALSE AS APPLIED** — the Builder's was appended, the Reviewer's was not and must not be (deviation 2). Byte-for-byte reviewer slice; NOT repaired. |
| `.agent/live_review.md` | `R-0774`: "The Reviewer side is the same shape: append at 3658, call at 3699, fallback recomposition at 3738" | **FALSE, MEASURED** (deviation 2). Append-only record; NOT repaired. |
| `.agent/live_review.md` | `R-0774` "Resolved when a Builder resume fallback and a Reviewer resume fallback each record TWO traces for that round…" | **YES, both halves now hold** — the Builder's by C4, the Reviewer's already at `c22818f5` |
| `.agent/authored/f109-r11.md`, `.agent/last_block.md` | verbatim copies of the block | n/a — carriers, not claims |

OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED, as G8 requires:
`tests/orchestration/test_prompt_trace.py` l.478 "Index [2] is the reviewer's
`build_trace_entry` append; [1] is the builder's" is **FALSIFIED** by C4 — there
are now three appends and the reviewer's is [3].

## Authored-text proofs

| Text | Proof |
|---|---|
| the block → `.agent/authored/f109-r11.md` → `.agent/last_block.md` | `cp` both times, never retyped; one sha256 three times (G1) |
| SLICE PLAN → `.agent/plan.md` | mechanical delimiter extraction, `cmp` no output exit 0 (G2); extractor first validated against the R10 precedent |
| SLICE RECORD → `.agent/live_review.md` | append arithmetic + independent unit reader + negative control (G3 a/b/c) |
| SPEC X → `pingpong_loop.py` | FROM/TO lifted mechanically out of the committed block, not retyped; X1 1→0/1, X2 2→0/2 (G4d) |

## Deviations & assumptions

**1 — G4(a) IS UNMEETABLE AS WRITTEN, AND I DID NOT STOP ON IT.** The block
orders `ast.dump(tree, include_attributes=False)` equality across a
docstring-only edit and says inequality proves SPEC X was misapplied.
`include_attributes=False` drops position attributes only, not `Constant`
values, and a docstring is a `Constant`, so the equality cannot hold for ANY
docstring edit — demonstrated with a three-line control module. I recorded the
real red exit code, proved SPEC X was applied exactly (23625 == 23625 nodes,
exactly the 3 intended docstring constants differ, AST equal with docstrings
stripped), and continued because the stop clause's antecedent is false. A
reviewer-prose defect, not a product defect — `.agent/prose_slips.md` material
under amend0827 rule 2, not an R-id.

**2 — SPEC Y'S REVIEWER APPEND WAS NOT ADDED, AND MUST NOT BE. THIS IS THE ROUND'S
BIGGEST DEPARTURE.** `R-0774` asserts "The Reviewer side is the same shape:
append at 3658, call at 3699, fallback recomposition at 3738". That is a STATIC
reading of line numbers and it is wrong: line 3658 is not an eager append, it is
inside the closure `_rev_trace`, which `_call_with_retry` invokes via `on_call`
ONCE PER ACTUAL PROVIDER INVOCATION, and which reads `reviewer_composed` at call
time — so it already picks up the fallback rebinding. MEASURED on the real loop
at `c22818f5`, before I changed anything, driving `fallback_repo` with
`reviewer_resume_fails=True, repair_rounds=2`: the Reviewer records **THREE**
traces, **TWO of them in the fallback round** — `chars=1741 marker=True` (the
abandoned resumed attempt) then `chars=1898 marker=False`, and 1898 is exactly
the length of the full-content prompt the fresh session actually received. The
Reviewer half of `R-0774`'s own "Resolved when" clause was therefore ALREADY
SATISFIED at base. Applying SPEC Y literally would have produced a THIRD entry
and double-counted one provider call in `prompt_trace.jsonl` and in
`token_ledger`'s `call_segments` — a new Medium defect of exactly the kind
`R-0774` exists to prevent, and it would have falsified SPEC Z case 2 ("there are
exactly TWO") in the same commit. AGENTS.md's self-review loop and Commit Gate
forbid committing a diff I have measured to be wrong, and AGENTS.md wins on
conflict, so I applied the Builder half only and declare the Reviewer half here
rather than silently. Consequences, all declared above: constraint 4's "SPEC Y
adds two appends" became one; G5(c)'s mutation target was retargeted to the
callback that actually carries the property.

**3 — ONE EXTRA COMMENT-ONLY INSERTION, NOT ORDERED BY THE BLOCK.** I added a
12-line deliberate-absence note in the Reviewer fallback branch saying DO NOT ADD
THE BUILDER'S SECOND APPEND HERE, with the measurement. Rationale: `R-0773`, the
finding this very round repairs, exists because a reader met a stale
deliberate-absence note and would have built an already-built thing a second
time; without this note the next reader of the Reviewer branch concludes
`R-0774` was half-fixed and adds the duplicate. It is a pure insert, so G4(b)
still reads all-inserts / 0 deleted, and it changes no executable statement.
AGENTS.md's discoverability section asks for exactly this ("Deliberate absences
are documented where a reader would search for them").

**4 — SPEC Z CASE 2 IS A REGRESSION PIN, NOT A NEW-BEHAVIOUR TEST.** It passes
before and after C4, because the behaviour it asserts already held on the
Reviewer. Its discriminator is real and I proved it (G5c): dropping the
Reviewer fallback's `on_call` turns it red. Its docstring names that
discriminator explicitly so a later reader does not mistake it for a case with no
subject.

**5 — THE ROUND ENDED RED AND NOTHING WAS REVERTED.** See the top section. C4/C5
are committed and pushed in their red state deliberately, per the standing "stop,
do not route around it" order. The measured one-line repair is written down
above so round 12 can land it immediately.

**6 — NO BLOCK ITEM WAS REORDERED, DROPPED OR ADDED.** C0a→C6 ran in the fixed
order. Constraint 8's STOP re-read was done before the first action and again
before this handback; `.agent/STOP` does not exist (exit 2, "No such file or
directory") both times.

## Open findings

`- R-[0-9]{4} — ` = **335** registered; `Done: R-[0-9]{4} — ` = **65** resolved;
**270 open**. This round resolved nothing by design (constraint 3): it registered
`R-0773` and `R-0774` and repaired `R-0773` in full and `R-0774`'s Builder half,
but the reviewer writes the `Done:` paragraphs in the NEXT round, and `R-0774`'s
resolution should not be booked while the suite it landed with is red.

## Next

**Round 12, and it is a repair round.** Land the two measured one-line selector
fixes above (`reversed(result.prompt_traces)` in `test_semantic_dedupe.py`;
split index `[2]` → `[3]` plus its docstring in `test_prompt_trace.py`), re-run
G6's fifteen suites to confirm 125 / 46 / all exit 0, and only then book
`R-0773` and `R-0774` as `Done:`. Decide deviation 2 first — whether the
Reviewer half of `R-0774` is accepted as already-satisfied (my measurement says
it is) or whether you want it re-verified — because `R-0774`'s "Resolved when"
wording depends on it. Phase 1 rule 1 (`.agent/STOP`) is checked before rule 2,
as always.
