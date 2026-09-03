# Handoff — F109 Semantic dedupe, SESSION 2, round 10

Branch: `feature/f109-semantic-dedupe`
Base commit: `d7fbff5b99d35e1601c6001086a508187eaed323` (round 9 close, already
pushed). No branch created, no branch switched, no PR created, nothing merged.

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

THIS IS THE LAST ROUND OF SESSION 2 — see the SESSION BOUNDARY section at the
end of this file, which is the part of this handback the next session reads
first.

WHAT LANDED. `run_pingpong` now carries `semantic_dedupe_enabled: bool = True`,
forwarded to BOTH PRIMARY compositions as `dedupe_enabled=semantic_dedupe_enabled`
and to nothing else. That is the whole implementation: the flag is tested in ONE
place — `should_dedupe_segment` consults `enabled` first and alone, and
`_dedupe_resumed_segments` returns the segments untouched on False — so an
operator can rule the feature out for a whole run without editing code, and
there is no second test of the flag to drift away from the first. The
`dedupe_sent_hashes=` expressions were NOT made conditional on it, per SPEC V.

WHAT DELIBERATELY DID NOT CHANGE. The two resume-fallback recompositions pass no
dedupe argument at all and still pass none, so they send full content at either
value of the flag — a fallback is not a resumed session (`R-0771`). Neither
`<role>_composed = compose_<role>_prompt(` statement text moved; only arguments
were added INSIDE the parentheses, and `tests/orchestration/test_prompt_trace.py`
— whose two rescoped guards count those statements and pin one of them to the
fallback branch — is exit 0 at 46 passed, unmoved from the base.

## Commits this round

| Item | SHA        | Commit subject                                                                                 |   +   |   -   |
|------|------------|------------------------------------------------------------------------------------------------|-------|-------|
| C0a  | `b5209fc4` | F109 R10 C0a: save the round 10 step block verbatim                                            |  300  |   0   |
| C0b  | `686fc1e5` | F109 R10 C0b: mirror the round 10 block to last_block                                          |  177  |  257  |
| C1   | `41567c08` | F109 R10 C1: plan for round 10 — book round 9, resolve R-0772, land the kill switch            |   10  |  14   |
| C2   | `de1e6668` | F109 R10 C2: book the round 9 gate and resolve R-0772 with its fix record                      |    5  |   1   |
| C3   | `b245e1c9` | F109 R10 C3: a run-wide kill switch for semantic dedupe, forwarded to both primary compositions |   23  |   0   |
| C4   | `0af67841` | F109 R10 C4: pin the kill switch through the real loop on both roles and the fallback          |  164  |   0   |

Every `+` and `-` cell above was read from `git show --numstat` for that exact
SHA and COMPARED CELL BY CELL against the numstat output quoted under G7 below —
I state plainly that I did that comparison, and the cells agree. The `+` column
only, per AGENTS.md DECISION F104 D1, never insertions plus deletions, and never
a before/after line count of a rewritten file. Every commit is under the 500
insertion cap; the largest is C0a at 300. All six are single-parent, verified
with `git log --format="%h parents=%p"`; there is no merge commit in the range.

C5 is this handoff rewrite, committed on top of `0af67841`. Every gate G1–G7 ran
at C4 or earlier, per constraint 9, so every reading quoted below already existed
when this file was written; C5's own insertion count is deliberately NOT quoted
anywhere here, because the reviewer measures that one. The push happens AFTER
C5, so the remote tip is not quoted either.

## Changed files (this round)

| Path                                          | Change                                                                  |
|-----------------------------------------------|-------------------------------------------------------------------------|
| `.agent/authored/f109-r10.md`                 | new — step block, `cp` from the scratch original, never retyped         |
| `.agent/last_block.md`                        | rewritten — byte mirror of the authored block, also by `cp`             |
| `.agent/plan.md`                              | rewritten — SLICE PLAN, whole file, 45 lines                            |
| `.agent/live_review.md`                       | appended ONCE at C2 — SLICE RECORD then SLICE DONE, two paragraphs      |
| `packages/orchestration/pingpong_loop.py`     | SPEC V — 1 parameter, 1 docstring paragraph, 2 keyword arguments        |
| `tests/orchestration/test_semantic_dedupe.py` | SPEC W — 1 new class appended at the END, no existing line changed      |
| `.agent/handoff.md`                           | rewritten — this file (C5)                                              |

No path outside the ordered change set was touched. `git diff --numstat` over
`d7fbff5b..0af67841` lists exactly six of those paths; C5 adds the seventh,
`.agent/handoff.md`. `packages/orchestration/prompt_segments.py`,
`packages/orchestration/prompt_trace.py` and
`packages/orchestration/token_ledger.py` were NOT touched, per constraint 5.

## Gates — one line per gate, real results

**G1 TRANSPORT — PASS.** `sha256sum .agent/authored/f109-r10.md .agent/last_block.md`
prints ONE digest twice:
`3a8ef357639196c7bc40e0c98dba54ac49f4224832dae0fd6ca843cb2f6011d5`, equal to the
`SHA256_OF_THIS_BLOCK` the delegation wrapper states. The scratch original
`.remedy-wt/f109-r10.md` was verified against that same digest as my first
action, before reading anything. The chain compares the saved copy against its
mirror and claims nothing about the emitted bytes.

**G2 THE PLAN — PASS.** `cmp .agent/plan.md .remedy-wt/f109_r10_plan.txt`
produced no output and exit 0, where the right-hand file is the SLICE PLAN
extracted MECHANICALLY from `.agent/authored/f109-r10.md` by
`.remedy-wt/f109_r10_extract.py` (index of `<<<SLICE PLAN`, index of the closing
`SLICE PLAN` line, everything between). `wc -l .agent/plan.md` is **45**,
strictly under 50. `grep -c '^## Goal'` is **1**; `grep -c '^## Next Steps'` is
**1**.

**G3(a) THE RECORD APPEND, ARITHMETIC — PASS.** Base `.agent/live_review.md`:
**2065277** bytes, sha256
`be21e849e22036041cfc3a352a7bfcbfd6d582be9dfe07524a157dc6c9314f35`. Appended
length S after stripping trailing newlines: **5383** = 3342 (SLICE RECORD) + 2037
(SLICE DONE) + 4 (the two `\n\n` paragraph separators). Expected new size
2065277 + 5383 = **2070660**; actual new size **2070660**; the arithmetic agrees.
New sha256 `041feb66b7c3c31f7d514ffed307d7eeecca0e1d3c2890e6398004cb81bac5b8`.
The file still ends WITHOUT a trailing newline (measured on the bytes, `True`).

**G3(b) A SECOND, STRUCTURALLY DIFFERENT READER — PASS.**
`.remedy-wt/f109_r10_reader.py` never counts a byte: it splits the WHOLE file on
blank-line boundaries (`re.split(r"\n\n+")`) into units, counts N from the
PAYLOAD itself rather than from the block — N came out **2** — and asserts the
LAST 2 units equal the appended paragraphs IN ORDER. It accepts the tracked file
(`True`). Unit 1 begins `Gate: F109 R9 — the round 9 entry. VERDICT PASS, AND
THE BRA…`, unit 2 begins `Done: R-0772 — RESOLVED. THE FIX is in
\`tests/orchestration/…`.

**G3(c) NEGATIVE CONTROL — PASS.** On a scratch copy at the exact path
`.remedy-wt/f109_r10_negative_control.md`, never on the tracked file: byte offset
**2065379**, which lies inside the FIRST appended paragraph, was XOR-flipped with
`0x20` (it held `'6'`). Reader (b) REJECTED the mutated copy (`False`, where it
returned `True` for the tracked file). The tracked file's sha256 was
`041feb66b7c3c31f7d514ffed307d7eeecca0e1d3c2890e6398004cb81bac5b8` before the
control and `041feb66b7c3c31f7d514ffed307d7eeecca0e1d3c2890e6398004cb81bac5b8`
after it — it did not move. The scratch copy was then deleted BY EXACT PATH and
its absence confirmed with `ls`.

**G3(d) COUNTS — PASS.** `grep -c '^Gate: F109 R9 — '` is **1** (base: 0).
`grep -c '^Done: R-0772 — '` is **1**. `grep -c '^Done: R-[0-9]\{4\} — '` is
**65** against **64** at `d7fbff5b`, so it rose by exactly 1.
`grep -c '^Landed: R-0772 — '` is STILL **1** — the landed line stands beside its
new `Done:` paragraph, as constraint 2 requires. `grep -c '^- R-[0-9]\{4\} — '`
is **333**, UNCHANGED from the base commit, because this round registers nothing.
The base counts were read from `git show d7fbff5b…:.agent/live_review.md`, never
by rewinding the tracked file.

**G4 THE EDIT SHAPE — PASS.** `.remedy-wt/f109_r10_g4.py` read the pre- and
post-commit blobs with `git show <sha>:<path>` — never by writing a revision over
the tracked file — and compared them as SEQUENCES OF LINES with
`difflib.SequenceMatcher(None, before, after, autojunk=False)`.
`packages/orchestration/pingpong_loop.py` at `b245e1c9` (5184 → 5207 lines):
FOUR non-equal opcodes, all `insert`, none `replace` or `delete` —
`before[2858:2858] → after[2858:2859]`, the one new parameter
`semantic_dedupe_enabled: bool = True,` (SPEC V, "ONE keyword-only parameter,
placed with the other behaviour flags"); `before[2903:2903] → after[2904:2913]`,
the nine-line docstring paragraph (SPEC V, "Document the parameter in
`run_pingpong`'s docstring"); `before[3308:3308] → after[3318:3327]`, the
eight-line comment plus `dedupe_enabled=semantic_dedupe_enabled,` at the BUILDER
primary compose call (SPEC V, "Add a short comment at the first of the two");
`before[3618:3618] → after[3637:3641]`, the three-line comment plus the same
keyword at the REVIEWER primary compose call (SPEC V, "the second may point at
the first"). TOTAL LINES DELETED: **0**.
`tests/orchestration/test_semantic_dedupe.py` at `0af67841` (1731 → 1895 lines):
ONE non-equal opcode, `insert`, `before[1731:1731] → after[1731:1895]` — the
whole addition at the END of the file (constraint 6). TOTAL LINES DELETED: **0**,
which constraint 6 requires.

**G5 THE COLOUR — PASS.** In a disposable worktree added BY EXACT PATH at
`/home/decodeux/Repos/remedy/.remedy-wt/f109-r10-wt`, checked out at the C4
commit `0af67841`, never in the primary checkout. THE IMPORT PROBE RAN FIRST:
`python3 -B -c "import packages.orchestration.pingpong_loop as m; print(m.__file__)"`
with the worktree as cwd resolved to
`/home/decodeux/Repos/remedy/.remedy-wt/f109-r10-wt/packages/orchestration/pingpong_loop.py`,
INSIDE the worktree, so no editable install shadowed it. `__pycache__` was purged
before every run (0 directories found each time; every process was `python3 -B`
with `-p no:cacheprovider`).
(a) CONTROL, unmutated: **exit 0, 122 passed**.
(b) MUTATION A — `semantic_dedupe_enabled: bool = True,` → `… = False,`. The
search string occurs EXACTLY **1** time in `packages/orchestration/pingpong_loop.py`
(counted and reported before the write). Result: **exit 1, 7 failed, 115 passed**.
The failure set INCLUDES the named half: narrowing the run to
`TestTheSemanticDedupeKillSwitch::test_the_switch_alone_decides_whether_a_resumed_chain_carries_a_marker`
shows it failing at `assert self._marked_traces(default) != []` — the half of
SPEC W case 1 that says the DEFAULT run still composes a marker. The other six
reddened cases are the pre-existing dedupe cases that also depend on the default
being True (`test_a_resumed_repair_chain_composes_a_marker_and_still_completes`,
`test_a_builder_resume_fallback_sends_full_content`,
`test_a_reviewer_resume_fallback_sends_full_content`,
`test_the_recorded_builder_row_describes_the_bytes_that_were_sent`,
`test_a_resumed_chain_that_never_falls_back_still_dedupes`,
`test_a_resumed_chain_reports_the_names_it_replaced`) — a wider red than ordered,
reported as the gate permits.
(c) MUTATION B — at the BUILDER primary compose call,
`dedupe_enabled=semantic_dedupe_enabled` → `dedupe_enabled=True`. The bare
expression occurs TWICE in the file, so per the gate I quoted a LONGER UNIQUE
string and say which one I took: the two lines
`"                # into it.\n                dedupe_enabled=semantic_dedupe_enabled,"`,
i.e. the argument immediately following the BUILDER comment's closing `# into
it.` line; that string occurs EXACTLY **1** time, counted and reported before the
write. Result: **exit 1, 3 failed, 119 passed**. The failure set INCLUDES the
named half: the same node, narrowed, fails at
`assert self._marked_traces(disabled) == []` — the half of SPEC W case 1 that
says the DISABLED run composes none. The two further reddened cases are
`test_a_disabled_run_reports_no_deduped_names_on_any_composition` and
`test_a_builder_resume_fallback_sends_full_content_at_either_flag_value[False]`,
both of which observe the same broken forwarding; again wider than ordered and
reported.
The file was restored from the C4 blob by exact path between the mutations and
after the last one; `git status --porcelain` inside the worktree was then EMPTY.
The worktree was removed with
`git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f109-r10-wt`,
followed by `git worktree prune`. `git worktree list` afterwards shows the
primary checkout plus the four PRE-EXISTING `remedy/job-*` worktrees that were
there before this round and are none of my making; `f109-r10-wt` is gone. My
shell's working directory was never inside the worktree — every command ran from
the repository root with the worktree addressed absolutely.

**G6 THE SUITES — PASS, all ten exit 0, run SERIALLY** by
`.remedy-wt/f109_r10_g6.py`, which starts one `python3 -B -m pytest` process,
waits for it, and only then starts the next. Base reading in parentheses; only
the first moved, and only upward:

| Suite | exit | passed | base |
|---|---|---|---|
| `tests/orchestration/test_semantic_dedupe.py` | 0 | 122 | (116) |
| `tests/orchestration/test_prompt_trace.py` | 0 | 46 | (46) |
| `tests/orchestration/test_prompt_segments.py` | 0 | 25 | (25) |
| `tests/orchestration/test_token_ledger.py` | 0 | 120 | (120) |
| `tests/orchestration/test_builder_prompt_golden.py` | 0 | 36 | (36) |
| `tests/orchestration/test_reviewer_prompt_golden.py` | 0 | 39 | (39) |
| `tests/orchestration/test_builder_prompt_quality.py` | 0 | 14 | (14) |
| `tests/orchestration/test_pingpong.py` | 0 | 34 | (34) |
| `tests/orchestration/test_session_resume.py` | 0 | 27 | (27) |
| `tests/cli/test_golden_path.py` | 0 | 42 | (42) |

`test_prompt_trace.py` is in that list because constraint 4(b) exists: it counts
the two `<role>_composed = compose_<role>_prompt(` statements this round added
arguments inside, and it is unmoved at 46. The dedupe suite rose by exactly 6 —
SPEC W's four cases, two of which are parametrized over the flag's two values
(1 + 1 + 2 + 2 = 6).

**G7 THE TREE — PASS.** `git status --porcelain` is EMPTY.
`git ls-files .remedy-wt` returns nothing. Insertions per commit BEFORE C5, taken
from `git show --numstat` and from nothing else — the `+` column only, per
AGENTS.md DECISION F104 D1 — and each is under 500: C0a **300**, C0b **177**,
C1 **10**, C2 **5**, C3 **23**, C4 **164**. I compared those six numbers cell by
cell against the `## Commits this round` table above and they agree; I state that
I ran that comparison. `git diff --numstat d7fbff5b99d35e1601c6001086a508187eaed323..0af67841`:

```
300	0	.agent/authored/f109-r10.md
177	257	.agent/last_block.md
5	1	.agent/live_review.md
10	14	.agent/plan.md
23	0	packages/orchestration/pingpong_loop.py
164	0	tests/orchestration/test_semantic_dedupe.py
```

That is exactly the ordered change set minus `.agent/handoff.md`, which C5 adds,
and nothing else.

## What C3 actually landed

Three edits and no fourth, all inside `run_pingpong`:

1. `semantic_dedupe_enabled: bool = True,` inserted after `keep_staging` — among
   the behaviour flags, not at the end of the signature, as SPEC V requires.
2. A nine-line docstring paragraph in the function's own `` `` ``-quoted style:
   `False` disables semantic dedupe for the WHOLE run whatever the session index
   holds; `True` is the default because dedupe is the feature's point and the
   switch exists so an operator can rule it out while diagnosing something else;
   it reaches the two primary compositions as `dedupe_enabled` and nowhere else.
3. `dedupe_enabled=semantic_dedupe_enabled,` at each PRIMARY compose call, beside
   the `dedupe_sent_hashes=` argument already there. The builder site carries the
   comment naming F109, what the flag is for, and — as SPEC V demands in the
   comment itself — that THE RESUME FALLBACK IS DELIBERATELY UNAFFECTED because
   the recomposition passes no dedupe argument at all. The reviewer site points
   at the builder comment rather than repeating it.

No second test of the flag was added anywhere, and the `dedupe_sent_hashes=`
expressions were not made conditional on it.

## What C4 actually landed

One class, `TestTheSemanticDedupeKillSwitch`, appended at the very END of
`tests/orchestration/test_semantic_dedupe.py`, driving the REAL loop through the
file's existing chain fixtures (`fallback_repo`,
`TestChainAgainstTheRealLoop._provider_pair` / `._run` / `._rows_by_session`,
`_capture_role_calls`, and SPEC T case 5's `_capture_compositions`). Nothing
already in the file was edited, reordered or deleted, and the import statements
did NOT need extending — every name the new cases use was already imported or
defined in the file, so constraint 6's one named exception went unused.

- **Case 1** (`test_the_switch_alone_decides_whether_a_resumed_chain_carries_a_marker`)
  is ONE case with both halves, as SPEC W prefers: the same `fallback_repo`, the
  same provider construction and the same repair budget are run twice, once with
  `semantic_dedupe_enabled=False` and once with the parameter not named at all,
  so the flag is the only argument that moves. The default run's traces carry at
  least one `[unchanged: ` marker, the disabled run's carry none, and BOTH reach
  `final_status == "staged_review_passed"`. The fixture did not force a split.
- **Case 2** (`test_a_disabled_run_reports_no_deduped_names_on_any_composition`)
  reads the composed objects the way round 9's case 5 does, through that class's
  own `_capture_compositions`, and asserts every composition reports
  `deduped_names == ()`. Non-vacuity is asserted rather than assumed: the chain
  really resumed (two rounds, and BOTH seams recorded proven sends), so round 2
  composed against a populated index and would have deduped had the flag not said
  otherwise.
- **Case 3** (`test_a_chain_that_never_resumes_composes_no_marker_at_either_flag_value`)
  is parametrized over `True` and `False`: a chain whose providers do not
  advertise resume composes no marker at either value and completes both times.
  This is the case that stops the flag from becoming the only thing standing
  between a fresh call and a marker.
- **Case 4** (`test_a_builder_resume_fallback_sends_full_content_at_either_flag_value`)
  reuses round 8's `fallback_repo` and `_capture_role_calls`, and is parametrized
  over both values: with the builder resume failing, the fallback really fires,
  the FRESH calls carry no marker at either value, and — the discriminator that
  stops the case passing because dedupe was simply off everywhere — the RESUMED
  calls carry a marker if and only if the flag is True.

Every absence claim in the class is bounded: `_marked_traces` asserts
`trace.prompt_text_truncated is False` on every trace before reading it, so the
absence is as wide as the recorded text and no wider.

## Item status

| Item | Status | Reason |
|------|--------|--------------------------------------------------------|
| C0a  | done   | `cp` from the scratch original, digest verified         |
| C0b  | done   | `cp` mirror, same digest                                |
| C1   | done   | SLICE PLAN applied byte for byte, `cmp` clean           |
| C2   | done   | SLICE RECORD + SLICE DONE appended, no trailing newline |
| C3   | done   | SPEC V, three edits, 0 lines deleted                    |
| C4   | done   | SPEC W, four cases (six tests), appended at the END     |
| C5   | done   | this handoff rewrite                                    |

No item was skipped and none deviated.

## Deviations

1. **THREE DOCSTRING PASSAGES ARE NOW STALE AND I DID NOT REPAIR THEM, because
   constraint 4 forbade it.** `packages/orchestration/pingpong_loop.py` still
   says, at line 922 in `_dedupe_resumed_segments` ("What remains absent is the
   config plumbing that supplies ``enabled``, which is T002c."), at line 1007 in
   `compose_builder_prompt` and at line 1542 in `compose_reviewer_prompt` ("the
   config plumbing that supplies it is T002c."), that the plumbing is still
   absent. As of C3 it exists. Constraint 4 says ONLY the edits SPEC V describes
   are permitted in that file and "nothing else in that file changes", so I
   applied the constraint as written and record the staleness here instead of
   widening the change set. The first of the three is a deliberate
   documented-absence note of exactly the kind AGENTS.md's discoverability
   section asks for, so it is the one most worth correcting in a later round.
2. **G5 mutation B needed a longer search string**, and the gate anticipated it:
   `dedupe_enabled=semantic_dedupe_enabled` occurs TWICE (both primary compose
   calls). I took the two-line string ending the builder comment's `# into it.`
   line plus the argument beneath it, which occurs exactly once, and named it
   above; the reviewer site was left alone, as the mutation orders.
3. **Both mutations reddened MORE than the named case**, which the gate permits
   and asks to be reported. Mutation A: 7 failed (the named node plus six
   pre-existing cases that depend on the default being True). Mutation B: 3
   failed (the named node plus two other new cases observing the same broken
   forwarding). Neither is a MISSING named case; the named half was pinned by
   narrowing the run to the single node and reading the failing source line.
4. **SPEC W cases 3 and 4 are `@pytest.mark.parametrize`d over the flag's two
   values** rather than written as two runs inside one function. The block asked
   for one case only in case 1 ("the two halves belong in one case"), and there
   the halves ARE in one case because the claim is a difference between two runs.
   Cases 3 and 4 each assert a property that must hold INDEPENDENTLY at each
   value, which a parametrize states more directly; this is why the dedupe suite
   rose by 6 rather than 4.
5. **No import statement was extended**, so constraint 6's one named exception
   was not used. Stated because the constraint anticipated it might be.

Nothing else deviated. Every gate was actually run; no gate result above is a
word rather than a measurement, and no test was edited to produce a colour.

## Open findings

The ledger stands at **333** findings registered and **65** resolved, so the open
set is **268** — registered UNCHANGED (this round registers nothing) and resolved
up by exactly 1 (`R-0772`), both measured by G3(d) against
`git show d7fbff5b…:.agent/live_review.md`. `R-0772`'s `Landed:` line still
stands beside its new `Done:` paragraph. **27** `Landed:` lines total, unchanged.
`R-0769` remains registered and unfixed; its repair edits `README.md` and a docs
test, neither of which F109 owns. `.agent/candidates.md` is unchanged and states
"EMPTY — no candidate is open.", so no block condition stands against F109.
`.agent/prose_slips.md` is untouched this round and holds **66** dated lines.
`.agent/STOP` was checked before the first action of the round and again before
this handback, and does not exist.

## Next expected action

`git push origin feature/f109-semantic-dedupe` immediately after this commit —
the remote tip is not quoted here by design, so the reviewer measures it. No PR
was created and nothing was merged.

Then the reviewer's round-10 verdict. See the SESSION BOUNDARY below for where
that verdict is booked, because this session does not book it.

## SESSION BOUNDARY — SESSION 2 ENDS HERE

**SESSION 2 OF F109 ENDS WITH THIS ROUND.** Round 10 is its last delegated round;
no further round is authored in this session.

**THE ROUND 10 VERDICT IS NOT IN THE LEDGER.** `.agent/live_review.md` currently
holds the round NINE gate entry (`Gate: F109 R9 — …`, booked at C2 of this round)
and nothing about round 10. Per operator amendment amend0827-process-diet rule 1,
this committed and pushed handback is the DURABLE CARRIER of round 10's result:
SESSION 3 books the round-10 verdict into `.agent/live_review.md` in the FIRST
COMMIT of its first round, the round that is happening anyway. A round whose
entire change set is that booking is forbidden.

**THE BRANCH TIP TO VERIFY BEFORE DOING ANYTHING.** Session 3's first act, after
`.agent/STOP` (Phase 1 rule 1 before rule 2) and the Phase 0 probe, is to confirm
that `feature/f109-semantic-dedupe` is at the C5 commit of this round — the
commit that carries this file — and that `git status --porcelain` is empty. C5's
own SHA cannot be quoted from inside itself; the tip to verify is the child of
**`0af67841`** (C4) on this branch, and it is the ONLY commit after `0af67841`.
The base this round started from was
`d7fbff5b99d35e1601c6001086a508187eaed323`.

**WHERE SESSION 3 RESUMES.** At the FIRST item in `.agent/plan.md`'s Next Steps:
surface the deduped names into the prompt TRACE, answering the `schema_v`
question on its own evidence. The standing constraint on that slice, repeated
here so it is not rediscovered the hard way: THE MANIFEST ROW KEYS STAY CLOSED —
`token_ledger.py`'s `call_segments` table mirrors them column for column, so
widening a row is a token-ledger change and not a prompt-trace change. After that
come the measurement fixture and the docs (T003), then the integration gate and
the closure sequence.

**SESSION COUNT.** This closes session 2 of F109 at round 10. The G7 soft limit
is 25 rounds OR 7 sessions per feature, whichever comes first; neither is
reached, so no scope report is owed and no limit line is emitted.
