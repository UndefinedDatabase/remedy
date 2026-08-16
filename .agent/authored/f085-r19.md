# F085 R19 — record the R18 PASS and sweep the stale self-count item 16 forbids

Feature T2_F085 Sandbox hardening (stage 1) · Round R19 · Branch feature/f085-sandbox-hardening
Base of this round: the R18 handback commit, `git rev-parse HEAD` at start = 646092ce.
Fortschritt: ~70 % (T001 gebaut · R13-R18 PASS · T002a: Builder-Site und CLI-Half fertig ·
`stream_evidence.py`, T002b-d, T003 offen) — Schätzung.

## Goal

R18 passed and its verdict is written by C1, which also registers R-0511 — a defect of the
reviewer's own R18 block, found by that round's worker and correctly reported rather than repaired.
The paragraph that introduces the pre-emission checklist says "Run all twelve checks" over a list
that held FOURTEEN before R18 and holds SEVENTEEN after it. That is exactly the shape checklist item
16 forbids, sitting in the paragraph that introduces the checklist item 16 belongs to, and R18's
promotion widened the gap it did not create. C2 removes the numeral, C3 resolves the finding.

The reviewer swept the WHOLE document for this class rather than the reported instance, which is
what item 16's last clause orders: a number-word standing next to `checks`, `items`, `paths`,
`commits`, `rules`, `points`, `steps` or `sub-points` matches at four lines, and the other three are
prose inside item bodies that count something real — "four different places, four checks" in item 7,
and the quoted examples inside items 16 and 17 themselves. Line 174 is the only heading that counts
the contents beneath it. The word `twelve` occurs nowhere else in the file.

## Bundle — in this order, none added, dropped or reordered

- C0a `docs(f085): save the R19 step block verbatim` — `.agent/authored/f085-r19.md`
- C0b `docs(f085): mirror the R19 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R18 PASS and register R-0511` — `.agent/live_review.md`
- C2 `docs(agents): drop the stale check count from the checklist heading` —
  `docs/agents/planner_reviewer_prompt.md`
- C3 `docs(review): resolve R-0511 now that the heading carries no count` — `.agent/live_review.md`
- C4 `docs(f085): advance the plan to the stream-evidence round` — `.agent/plan.md`
- C5 `docs(f085): rewrite the handback for R19` — `.agent/handoff.md`

C1 carries the registration as well as the record, because a finding persists in the FIRST content
commit of the repair round (planner_reviewer_prompt.md §4.4a) and nothing is lost if the session
dies. C3 stays separate for the same reason it did in R17 and R18: a resolution must not claim on
disk a fix no commit has landed.

## Change set — exactly these paths, nothing else

`.agent/authored/f085-r19.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`, `docs/agents/planner_reviewer_prompt.md`. Nothing under `packages/`, `tests/`,
`apps/` or `scripts/`; no file under `docs/` other than the one named. `.agent/context.md` and
`.agent/decisions.md` are NOT touched, and neither is `docs/README.md`.

## Constraints

1. `cp` and the `remedy` CLI are denied here: copy with `shutil.copyfile` or a byte write and prove
   the BYTE property, never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, reformatted or reworded.
3. Apply each FROM/TO pair by locating the FROM exactly once and replacing it with the TO; if it
   does not occur exactly once, STOP and report. Pair shapes, classified MECHANICALLY by containment
   at build time and printed here rather than judged by eye: HEADF→HEADT REWRITE, PLANF→PLANT
   REWRITE. Both TOs were tested for containment of their FROM and neither contains it.
4. This round orders NO destructive check and no mutation red-proof. No gate below needs a
   disposable tree, and no worktree is added, removed or pruned.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.
6. If the single `python3` heredoc that writes the C0a bytes is rejected for length, split it into
   sequential appends to the same path — that is what R18 did and G2 proved the result byte-exact.
   The method is fixed (programmatic write, never retyping); the number of calls is not.

<<<SLICE RECORD1>>>
Gate: R18 — PASS, the round that put three standing rules on disk. All nine ordered gates were re-run
by the reviewer over 88dbcefa..646092ce and every one reproduces the handback's reading. TRANSPORT
is proven twice over. Disk-to-disk: the committed `.agent/authored/f085-r19.md` predecessor
`.agent/authored/f085-r18.md`, the committed `.agent/last_block.md` and both working copies are
byte-EQUAL at sha256 7187303bf16c3414278b5cbcf7efe2ddb082e3e4c4405e31fc65247ca9ccbac8, 20616 B, 281
lines, with 14 marker lines and 7 slice pairs intact. And by digest fallback against the reviewer's
OWN pre-emission measurements, which is what makes the worker's declared split write a non-event:
the block was measured in four regions before it was delegated, and the saved file's four
corresponding regions hash to 989020a1, 88eed983, 5fe3c39b and 4fe2a9ff exactly as measured, with
the fifth region at its measured 71 lines and the file at its measured 281. A block that reaches
disk byte-identical to the bytes the reviewer measured has not been damaged by the number of write
calls it took. BOTH APPEND COMMITS HOLD THEIR SHAPE: for C1 the pre-commit blob (291333 B) is a
byte-exact PREFIX of the post-commit file (295507 B) and the remainder is byte-equal to blank plus
RECORD1; for C3 the pre-commit blob (295507 B) is a prefix of (297276 B) and the remainder is blank
plus DONE1 plus blank plus DONE2. Each occurs exactly ONCE at HEAD, no marker line survives, HEAD
equals the C3 blob. THE ARITHMETIC: 125 / 6 / 0 at base and again after C1 — a record adds no id —
against 125 / 8 / 0 at HEAD, the open set moving 119 to 117, registered difference EMPTY, resolved
difference exactly R-0508 and R-0510, no duplicate and no resolution naming an unregistered id; next
free R-0511. THE PROMOTION LANDED AND ITS OWN RULE HOLDS ON IT: PROMF occurs exactly once at HEAD,
so the anchor survived its append; each of the three item titles occurs exactly once among C2's 34
added lines; and the checklist region parses to a contiguous 1 through 17 with no repeat and no gap,
which is item 17's arity rule holding on the very commit that writes item 17. THE PLAN PAIR: PLANF
0x and PLANT 1x, `.agent/plan.md` at sha256
65f9287c4ef71975c8b956a9df25793cd2e5584fb528cc816a374c39d5ca0253, 2344 B, 40 lines under its cap,
`## Goal` and `## Risks` byte-identical to base, `## Next Steps` parsing to 1, 2, 3. Doc readers are
305 passed 1 skipped, the state readers 157 passed and the canary 42 passed, all rc 0 and all re-run
by the reviewer rather than accepted from the report. The change set is exactly the declared paths
with 0 outside; insertions are 281, 198, 44, 34, 21 and 7 before the handback commit, which is
itself 30, none over 500; seven single-parent commits, twenty reflog entries all `commit:`-prefixed,
no amend, rebase, reset or force-push; the tree is clean and `git worktree list` is ONE line. The
handback measures 78 lines against its own declaration of 78, inside the template's 100-line
allowance for a table of this many commits, and its two declared deviations are both accurate. THE
WORKER'S REFUSAL WAS CORRECT AND IS RECORDED AS SUCH: it found the stale check count at line 174,
declined to fix it because the change set did not include it, and reported it instead of widening
scope. That is the behaviour this loop is built to produce, and the defect it surfaced belongs to
the reviewer's block, not to its execution — it is registered below as R-0511.
LAST_REVIEWED_SHA advances to 646092ce.
<<<END RECORD1>>>
<<<SLICE REG1>>>
- R-0511 — Low, A HEADING KEPT COUNTING ITS OWN CONTENTS IN THE PARAGRAPH THAT INTRODUCES THE RULE
AGAINST IT. Raised by the R18 worker in its handback and confirmed by the reviewer on disk.
`docs/agents/planner_reviewer_prompt.md`:174 reads "Run all twelve checks mechanically" over a list
that already held FOURTEEN items before R18 and holds SEVENTEEN after it. The count was therefore
stale by two BEFORE the promotion round and by five after it, so R18 widened a defect it did not
create — but it widened it while adding the very item, 16, that forbids a heading from counting the
contents beneath it, which is what makes this worth an id rather than a silent fix. The reviewer's
own pre-emission pass ran item 16 against the BLOCK's headings and never ran it against the TARGET
file's, which is the same class boundary items 2, 6 and 7 exist to keep separate: a rule that reads
the block, a rule that reads the file the block writes into, and a rule that reads the tests
guarding it are three different passes. Item 16 as written does not say which of those it belongs
to, and the answer is BOTH — the block's headings and the headings of any section the block edits.
No gate was contradicted and nothing was mis-executed; the R18 worker's refusal to widen its change
set was correct and is recorded in that round's gate. Counter-measure, applied by this block: C2
removes the numeral entirely rather than correcting it to seventeen, because a corrected count is
the same defect with a longer fuse — this is the R-0486 correction-carries-the-old-fact shape, and
the only stable fix for a self-count is to stop counting. The reviewer additionally swept the whole
file for the class rather than the reported line, and reports the sweep's predicate and its four
matches in this round's block. OPEN.
<<<END REG1>>>
<<<SLICE DONE1>>>
Done: R-0511 — the heading no longer counts anything. `docs/agents/planner_reviewer_prompt.md`:174
now reads "Run EVERY check below mechanically", so the sentence carries no numeral that a later
promotion can falsify, and the word `twelve` occurs nowhere in the file. The fix was made the way the
finding prescribed: the numeral was REMOVED rather than corrected to seventeen, because an accurate
count is the identical defect waiting for the next item — the distinction item 11 draws between a
measurement and a recollection, applied to the target file instead of to the block. The sweep the
finding also demanded was run and is reported in this round's block: the predicate is a number-word
standing next to a countable noun, it matches four lines in the file, and the three that are not
line 174 count something real inside an item's prose rather than announcing the size of a list.
Item 16 is amended by neither this fix nor this resolution; what changes is that the reviewer now
runs it against the headings of every section a block EDITS as well as against the block's own,
which is the reading the finding established and which this round is the first to perform.
<<<END DONE1>>>
<<<SLICE HEADF>>>
- **Pre-emission block checklist (DECISION F105 D8, finding R-0250).** Run all
  twelve checks mechanically, on the FINAL bytes, after the last edit, before any
<<<END HEADF>>>
<<<SLICE HEADT>>>
- **Pre-emission block checklist (DECISION F105 D8, finding R-0250).** Run EVERY
  check below mechanically, on the FINAL bytes, after the last edit, before any
<<<END HEADT>>>
<<<SLICE PLANF>>>
## Current Step
R18, this round: record the R17 PASS, promote three standing rules into
docs/agents/planner_reviewer_prompt.md §3 as checklist items 15, 16 and 17, then
resolve R-0508 and R-0510 — the two findings that stayed open for exactly that
promotion. Reviewer habit binds nothing until it is on disk.
<<<END PLANF>>>
<<<SLICE PLANT>>>
## Current Step
R19, this round: record the R18 PASS, register R-0511 — the stale check count the R18
worker found in the checklist's own introduction — remove that numeral rather than
correct it, and resolve the finding. The next round leaves the review machinery and
returns to T002a's last spawn site.
<<<END PLANT>>>

## Application order

C1 appends RECORD1 then REG1 to `.agent/live_review.md`, each preceded by exactly one blank line,
appending only. C2 applies HEADF→HEADT to `docs/agents/planner_reviewer_prompt.md`. C3 appends DONE1
to `.agent/live_review.md`, preceded by exactly one blank line. C4 applies PLANF→PLANT to
`.agent/plan.md`.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

This session's Bash tool rejects `$?`, loops and command substitution BY FORM: read every exit code
as a real `subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before EVERY commit in the bundle; `.agent/STOP` re-read
from disk before the first and the last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r19.md` after C0a and `.agent/last_block.md` after C0b are
byte-EQUAL: report one sha256, byte length and line count for both, plus the marker-line count. C0b
copies the COMMITTED C0a blob, never the scratch file. Per docs/agents/self_drive_protocol.md §2.1
an in-session delegation has no transport hop, so the hash-stamp ritual is replaced by exactly this
byte-equality proof.

G3 APPEND SHAPE, twice. For C1 and again for C3: the pre-commit blob is a byte-exact PREFIX of the
post-commit file, HEAD equals it, and the remainder is byte-equal to blank + the ordered slices for
that commit — RECORD1 then REG1 for C1, and DONE1 for C3. Each occurs exactly ONCE in the whole file
at HEAD, and neither commit adds a marker line. Report both numstat pairs as READINGS.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 125 / 8 / 0, 117 open. After C1 expect 126 / 8 / 0, 118 open — this round
DOES register, so the count that stayed flat in R17 and R18 must move here, and a reading of 125
after C1 would mean REG1 never landed. At HEAD expect 126 / 9 / 0, 117 open. Report the reading
after C1 as well as at HEAD, both symmetric differences, duplicate-id counts, any resolution naming
an unregistered id, and the max and next-free id.

G5 THE SWEEP. HEADF occurs 0 times at HEAD and HEADT once. The word `twelve` occurs 0 times in the
WHOLE file — that count is safe to order over the whole file precisely because C2 removes the only
occurrence and no TO in this block writes the word into that file. Then, scoped to the region
between `**Pre-emission block checklist` and the line beginning `  Why this is on disk`, the numbers
matched by `^  (\d+)\. \*\*` still read 1 through 17 with no repeat and no gap: C2 must not disturb
the list it stops counting. Report the parsed sequence.

G6 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT once. Report `.agent/plan.md` sha256, bytes and
a line count under 50, with `## Goal`, `## Next Steps` and `## Risks` byte-IDENTICAL to base — this
pair rewrites the Current Step section ONLY, the list arity is unchanged, and a diff touching
`## Next Steps` would mean the FROM matched more than it should.

G7 DOC READERS. `python3 -m pytest tests/test_agent_tooling.py tests/docs/ -q` exits 0. No ruff gate
is ordered and none is skipped by oversight: the change set contains no `.py` file.

G8 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0.
CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with 42 passed. Report the
state-reader count as a READING rather than matching it against a number: that suite spawns wrapper
processes under flock and timeouts and is timing-sensitive. If a run comes out red, report the
failing test id, re-run `tests/regression/test_resource_safety.py` alone three times and report all
four readings. A failure that reproduces every time is a STOP; one that does not is recorded with
its tally and the round continues.

G9 COMMIT HYGIENE, three readings. `git diff --name-only 646092ce..HEAD` measured BEFORE C5 equals
the declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+` column of
`git show --numstat` for C0a, C0b, C1, C2, C3 and C4: none exceeds 500. C5's own count is ordered
nowhere, because a commit cannot measure itself; report it in the round report instead.
`git log --format=%h %p 646092ce..HEAD` shows ONE parent per commit and a linear chain; `git reflog`
shows every entry prefixed `commit:`, no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed, every gate has been RUN with its
exit code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C5. Run `gh pr list
--state open --json number,headRefName,baseRefName,isDraft` after the final push and report its
output; create NO pull request and merge nothing. Report what the commands PRINTED — a gate whose
result you did not read is a finding. If a gate contradicts this block, report the contradiction and
STOP: never repair text to make a number come out, never widen the change set. Declare every
deviation.
