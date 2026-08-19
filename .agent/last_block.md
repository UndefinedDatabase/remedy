── STEP R67 record — a false clause in the ledger — F085 — R68 ───────────────

Goal: record the R67 FAIL, resolve the two findings R67 really did repair, register the false clause
R67's own record shipped, and correct that clause by APPEND. R67's worker declared the defect
instead of editing the reviewer text it came in — which is exactly what its constraint 8 asked for —
so the failure is the REVIEWER's for the second round running, and the finding is registered against
the reviewer's authored text. No source file and no document is touched this round.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R67 FAIL, resolve R-0561 and R-0562, register R-0563 and append its correction ·
C3 handback. The record and the correction share one commit because the correction IS ledger text:
docs/agents/planner_reviewer_prompt.md §3 checklist item 20 forbids rewriting landed text, so the
repair for this defect can only ever be an appended paragraph in the same file the finding registers
against, and splitting them would put a retraction in a different commit from the finding it retracts.

CONVENTION, binding on every count here, carried verbatim in force from the R67 block. A line count is
the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIR IS PLAN22. THE END-OF-FILE
APPEND IN THIS BLOCK, WHICH HAS NO FROM AT ALL, IS RECORD36 — listed rather than counted, per §3
checklist item 11. The append slice CARRIES ITS OWN LEADING BLANK LINES, so the separation its
target's convention requires is a property of bytes that were measured and never of a join shape that
was reasoned about.

## Change

C1 applies PLAN22F→PLAN22T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep a stale
label. C2 appends RECORD36 to the END of `.agent/live_review.md`.

Change set, named rather than counted: `.agent/authored/f085-r68.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`. Nothing else. Every path in it is
under `.agent/`, so NO `docs/**` path is edited and the docs-consistency suite is not ordered, NO
`.py` path is edited and no lint gate is ordered, and NO `docs/roadmap/**` path is edited so Rule A4
is untouched. Each tracked path named in a gate below was resolved on disk at a8ba453d with
`git ls-tree`, one call per path, before emission, per checklist item 24, and all of them exist;
`.agent/authored/f085-r68.md` is the one path no gate reads at the base, because C0a creates it.

WHY R67 FAILED, read by the reviewer rather than taken from its handback. Every gate the R67 block
ordered — G1 through G9 — was re-executed over 261dce53..a8ba453d and each reproduces the handback's
reading exactly, including the truth gate G8 on all six of its readings. The worker deviated in
nothing. What failed is a clause NO gate read: RECORD35, committed at 60057260 and now permanent in
`.agent/live_review.md`, closes R-0562 by asserting that the `spawn unsupervised` sweep leaves two
further hits standing elsewhere in the repository, one a constant in `packages/runtimes/dev_server.py`
and one in `docs/agents/planner_reviewer_prompt.md`, and the R67 block's own "THE SWEEP BEHIND THIS
ROUND" paragraph says the same. Measured at 261dce53 and again at a8ba453d, `git grep -n "spawn
unsupervised"` over `packages/`, `apps/`, `docs/` and `tests/` returns EXACTLY two hits at each SHA —
the two live claims themselves — so no further hit exists under those four trees; the `dev_server.py`
lines carry the bare word `unsupervised` and never the phrase, and
`docs/agents/planner_reviewer_prompt.md` carries 0 occurrences of `unsupervised` in any case at either
SHA. The phrase DOES recur under `.agent/`, in this workflow's own block mirrors and records, which is
why every sweep clause in this block names the trees it swept. R67's G8 ordered the sweep's TOTAL, got two,
and passed, while the prose beside it said four: the gate counted hits and the sentence described
them, and nothing in the block compared the two. That is the defect this round registers.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r68.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C3; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPE. The reviewer ran the containment test at emission against the target's blob at
   a8ba453d and prints its own output here per checklist item 15: PLAN22F→PLAN22T
   `TO contains FROM: false`. It is therefore a REWRITE and owes the FROM 0x / TO 1x reading over its
   post-commit file. PLAN22F occurs EXACTLY 1x in `.agent/plan.md` at a8ba453d — the reviewer
   measured it.
4. RECORD36 HAS NO FROM. It is appended at the END of `.agent/live_review.md`. Its obligation is
   ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of the
   post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are
   exactly the slice's lines IN ORDER. Do not invent a FROM for it and do not report a FROM count.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record. Only C0a and C0b may precede it. This
   round writes to the finding ledger, so §3 checklist item 23 binds it.
6. NOTHING IN `.agent/live_review.md` THAT ALREADY EXISTS AT a8ba453d IS EDITED, MOVED OR DELETED.
   RECORD35's false clause STAYS on disk exactly where it was committed, and RECORD36 retracts it by
   appending. This is checklist item 20's ruling — "overwriting landed text is worse than a dated
   wrong sentence" — and DECISION F085 D6's own correction in `.agent/decisions.md` is the precedent
   this round follows. G3's PREFIX reading and G7's reading D both prove mechanically that you obeyed
   this; a repair that edits the old paragraph would satisfy neither.
7. Every sentence in RECORD36 that states a reading of a file names the SHA it was read at in the same
   clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to EVERY
   reading in the clause, not only the first. RECORD36 states readings of R67's range and of this
   round's base only, all of which are prior state, so every SHA it names already exists when it is
   written.
8. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD36 is reviewer text and carries the R67 gate
   entry, both resolutions, the one registration and the correction inside it. Do not add a `Landed:`
   line, do not add a `Done:` paragraph of your own, and do not edit RECORD36 to reconcile it with
   anything you measure. A disagreement between RECORD36 and your own reading is a finding to REPORT
   in the handback, never to fix — the same rule that caught R66 and R67, in the round that exists
   because it worked twice.
9. THIS ROUND REGISTERS ONE FINDING AND RESOLVES TWO. Registered moves 177 → 178, done moves 28 → 30,
   landed stays 0, open moves 149 → 148, and the next free id moves R-0563 → R-0564. RECORD36
   therefore carries exactly one `- R-` registration line and exactly two `Done:` lines; G6 proves it.
   The two resolutions are honest because their repairs landed in a PRIOR round at 5f09088a and
   3440efe4 and the reviewer re-read both files itself before authoring them — a resolution written by
   the round that makes the repair is what constraint 9 of the R67 block forbade, and this is the next
   round it names.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as its correction section fixes the ruled figure:
   490 lines TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three on the final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r68.md`; a mismatch is a finding against this block, not the worker.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, and never widen the
   change set to route around a red.
12. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. These suites spawn real supervisors that bind a port and leave escapees when a readiness
   assertion fails, so two concurrent runs redden each other on tests neither touched.
13. THIS ROUND ORDERS NO MUTATION, NO REVERT AND NO RED CONTROL, and creates no worktree. Its change
   set holds no executable path, so there is no behaviour a colour could prove; G7 reads facts back
   from their sources instead, which is the counter-measure R-0563 registers.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. This round orders NO destructive check, so no `git worktree` is
created at all and `git worktree list` is one line at round start and one line at the end.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r68.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD36 line counts read
from that committed file, against constraint 10's 490 / 400 / 140, where PROSE is TOTAL minus the
slice lines.

G3 SHAPES, measured SEPARATELY per pair and per path. PLAN22F→PLAN22T is a REWRITE over
`.agent/plan.md` at C1: report its FROM 0x and its TO exactly 1x over the post-commit blob, and
re-applying the extracted FROM→TO to the pre-commit blob must reproduce the post-commit blob
BYTE-EXACTLY. For RECORD36 at C2 report the ordered-equality readings constraint 4 names: pre-commit
blob is a byte-exact PREFIX, the slice is an exact SUFFIX, `pre + slice` equals the post-commit blob
byte for byte, and that commit's ADDED lines are exactly the slice's lines IN ORDER. Plus
`git show --numstat` for each path and commit — the deletion column for `.agent/live_review.md` at C2
must be 0, which is constraint 6 read off the diff — plus the count of lines matching
`^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0. Count marker LINES, never the
substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0, and serially per
constraint 12. Report each run's passed count; the counts are reported, never predicted, and only the
exit code is ordered. The reviewer took both base readings below itself, in the primary checkout, at
a8ba453d.
 - `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
   tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
   base `160 passed`; these read `.agent/plan.md`, which C1 rewrites, and `.agent/live_review.md`,
   which C2 appends to.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected by
grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 40 lines by applying the pair to that blob at a8ba453d.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
a8ba453d and at HEAD, from the line-start patterns for a registration, a resolution and a landed line.
The reviewer's base reading is 177 / 28 / 0, 149 open, max registered R-0562, max resolved R-0558. At
HEAD the reading must be 178 / 30 / 0, 148 open, max registered R-0563 and max resolved R-0562,
because constraint 9 rules this round registers one finding and resolves two. The symmetric difference
of the registered sets must be EXACTLY `{R-0563}`, the symmetric difference of the done sets EXACTLY
`{R-0561, R-0562}`, and the landed symmetric difference EMPTY. Next free id R-0564. Report all three
symmetric differences, the duplicate-id count and the count of resolutions naming an unregistered id,
at both SHAs.

G7 TRUTH, the gate this round exists for, and the first written under R-0563's counter-measure: every
clause of the sentence a sweep licenses is read back from that sweep's own output, not only its total.
Report all four readings.
 - READING A, the sweep itself, run at a8ba453d and again at HEAD: `git grep -n "spawn unsupervised"`
   over `packages/`, `apps/`, `docs/` and `tests/` returns EXACTLY two hits at each SHA, and the files
   they land in are exactly `docs/system/exec-guard-limitations-v0.md` and
   `packages/orchestration/exec_guard.py`. Report the count AND the path of every hit, at both SHAs —
   the path list is the half R67's G8 never took.
 - READING B, the hit RECORD35 claimed and the repository does not have:
   `git grep -ic "unsupervised" <sha> -- docs/agents/planner_reviewer_prompt.md` at a8ba453d and at
   HEAD returns NO match at either. Report the command's EXIT CODE as well as its output, because a
   `git grep` with no match exits 1 and prints nothing, and an unreported exit code is how a zero
   reading and a failed command look alike.
 - READING C, the distinction RECORD35 lost, measured in the file it named:
   `git grep -ic "unsupervised" a8ba453d -- packages/runtimes/dev_server.py` is NON-ZERO while
   `git grep -ic "spawn unsupervised" a8ba453d -- packages/runtimes/dev_server.py` HAS NO MATCH and
   exits 1. Both halves are case-INSENSITIVE on purpose, because the constant that produces the first
   reading is upper-case and a case-sensitive probe would understate it. Report both numbers and both
   exit codes. The bare word occurs there; the phrase never does.
 - READING D, that the correction was APPENDED and the landed text preserved, which is constraint 6
   proved rather than promised: the string `and an example sentence in` occurs EXACTLY 1 time in
   `.agent/live_review.md` at a8ba453d and EXACTLY 1 time at HEAD. That string belongs to RECORD35's
   retracted clause and to nothing else in the file at a8ba453d, and no slice of this block writes it,
   so a count that stays 1 proves the old paragraph is untouched and a count of 0 would prove it was
   overwritten. Report both counts.

G8 HYGIENE. `git diff --name-only a8ba453d..HEAD` measured BEFORE C3 holds exactly the change set
above minus `.agent/handoff.md`, which C3 writes, and nothing else — and in particular holds NO path
under `packages/`, `apps/`, `docs/`, `tests/` or `scripts/`, because this round edits no source, no
test and no document. Report the list. Report per-commit insertions for every commit BEFORE C3 — C3
cannot measure itself, so its own go in the round report — and confirm none exceeds 500. This branch
spent the AGENTS.md declared-oversize allowance at d4473f85, so a second oversize commit is a STOP
under constraint 11, never a declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
a8ba453d, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2 and C3,
the real G1-G8 results with exit codes, the open-findings count and the next expected action. Keep it
under the AGENTS.md 60-line cap; if the mandated content genuinely does not fit, name the DECISION D15
stated cause and the specific mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~99 % (T001 gebaut · R13-R65 PASS · R66 und R67 FAIL, beide Fehler des Reviewers, beide
in der jeweils nächsten Runde repariert · T002 KOMPLETT · T003 fast fertig: Netz-Posture verdrahtet
und gepinnt, Limitations-Dokument steht, verlinkt und inhaltlich korrekt; offen bleibt allein die
Akzeptanzmessung am echt lauschenden Server) — Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R69 measures
T2_F085's remaining acceptance line — a network access from a guarded test command fails under deny —
against a loopback server that is really listening, with the red control that line needs; the
integration gate and closure follow it. TWO: R68 carries no verdict of its own, because the round that
records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4 item 13);
R69 carries it, and R69's record is also where R-0563 is marked `Done:` if the reviewer's re-reading
of the appended correction agrees. THREE: a standalone closing line stating the open findings count
and the next free id. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the
self-drive protocol requires every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN22F
## Current Step
R67, this round: repair. R66 FAILED — the reviewer's limitations document claimed three classes
run under the guard when amendment F085 D1 marks SIX stage-1 and only three default-deny, and the
`exec_guard` module docstring still called the runtime class unsupervised after R61 and R63
migrated it whole. Both claims are corrected, both registered as R-0561 and R-0562, and the
sweep behind them is reported rather than assumed.

## Next Steps
1. The remaining acceptance measurement: a guarded test command is refused against a loopback
   server that is really listening, where the same child without the posture is served.
2. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.
END-PLAN22F

BEGIN-PLAN22T
## Current Step
R68, this round: the ledger. R67's two repairs are correct and re-read, so R-0561 and R-0562 are
marked done — but R67 FAILED on its own record: RECORD35 closes R-0562 by naming further
repository hits for `spawn unsupervised` that do not exist. That claim is registered as R-0563
and retracted by an APPENDED correction, never by rewriting landed text. No source file, no test
and no document is touched.

## Next Steps
1. The remaining acceptance measurement: a guarded test command is refused against a loopback
   server that is really listening, where the same child without the posture is served.
2. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.
END-PLAN22T

BEGIN-RECORD36

Gate: R68 — the R67 entry. R67 FAILED, and the failure is the REVIEWER's for the second round
running, not the worker's. Every ordered gate G1-G9 was re-executed by the reviewer over
261dce53..a8ba453d, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing, applied every slice unedited, and declared the defect this entry registers instead of
repairing it — which is what that block's constraint 8 asked for, and the second consecutive round in
which a worker's declared disbelief is the only thing that caught the reviewer. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD, disk-to-disk with no digest fallback: the committed
`.agent/authored/f085-r67.md` and the committed `.agent/last_block.md` at a8ba453d, and both working
copies at a8ba453d, are all four byte-EQUAL at sha256
8f1d0218ad4e0796a9618d46cf2737b8fd0d60ecb022431e5d73ebae92a99db1, 29948 B, 386 lines, 14 marker
lines. THE SHAPES HELD: PLAN21 over `.agent/plan.md` at 7c0dca8b, FIXDOC over
`docs/system/exec-guard-limitations-v0.md` at 5f09088a and FIXMOD over
`packages/orchestration/exec_guard.py` at 3440efe4 are REWRITES, each reading
`TO contains FROM: false`, each FROM 1x pre-commit and 0x post-commit with its TO exactly 1x
post-commit, and each pair re-applied to its pre-commit blob reproduces its post-commit blob
BYTE-EXACTLY. RECORD35 over `.agent/live_review.md` at 60057260 satisfies ORDERED EQUALITY on every
clause — PREFIX, SUFFIX, `pre + slice` equal byte for byte, ADDED lines equal to the slice's lines IN
ORDER, 71 and 71. Marker LINES at a8ba453d are 0 in each of the four edited files. THE SUITES WERE
RE-RUN, NOT READ, in the primary checkout, serially, each exit 0: `331 passed` for the six readers of
the edited module, `295 passed` for the docs-consistency suite, `160 passed` for the four state
readers and the canary `42 passed`, each equal to its base. THE PLAN CONTRACT HELD at a8ba453d: 40
lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all present. THE
ARITHMETIC MOVED BY EXACTLY TWO REGISTRATIONS, as that block's constraint 9 required: 175 registered /
28 done / 0 landed and 147 open at 261dce53 against 177 / 28 / 0 and 149 open at a8ba453d, the
registered symmetric difference exactly {R-0561, R-0562}, the done and landed differences both EMPTY,
and 0 duplicate ids and 0 orphan resolutions at both SHAs. THE LINT HELD at a8ba453d, both the plain
and the preview half exit 0 on `All checks passed!`. THE TRUTH GATE HELD on all six of its readings,
which is why both repairs resolve below. WHAT FAILED IS THE ONE CLAUSE THAT GATE DID NOT READ.

Done: R-0561 — Resolved at R67, commit 5f09088a. Re-read by the reviewer in the file rather than in
the handback: `docs/system/exec-guard-limitations-v0.md` at a8ba453d carries the heading
`## Six classes run under the guard, and only three of them deny the network`, contains each of the
six stage-1 class names `builder`, `test`, `dod-process`, `dod-app`, `runtime-server` and
`runtime-build`, separates being guarded from denying the network in as many words, and carries the
two contents `docs/roadmap/features/T2_F085.md` assigns to it and the first version omitted — that the
exclusion is a `SCOPE ruling` and that untouched sites `can hang`. The old heading
`## Only three command classes run under the guard at all` occurs 0 times in that file at a8ba453d,
and the false sentence naming `runtime` among the unsupervised occurs 0 times there.

Done: R-0562 — Resolved at R67, commit 3440efe4. The `exec_guard` module docstring's PARTIAL COVERAGE
bullet at a8ba453d names the runtime class as migrated whole, through `runtime_server_exec_policy` for
its servers and `run_guarded_runtime_build_command` for its builds, and leaves the unsupervised claim
to `git`, `packaging` and `other`; the sentence `the runtime, git and packaging classes still spawn
unsupervised` occurs 0 times in `packages/orchestration/exec_guard.py` at a8ba453d. The repair is
INERT, which is the property no red control could have shown: the pre-commit and post-commit blobs of
that file at 3440efe4, parsed with `ast.parse` and each module docstring set to None, produce
IDENTICAL `ast.dump` output, so that commit changed docstring bytes and nothing executable.

- R-0563 — Medium — a sweep gate read a TOTAL while the sentence beside it characterised the
INDIVIDUAL hits, so a false clause reached the finding ledger through the very round that registered
the counter-measure against false claims. RECORD35's closing sentence, committed at 60057260, states
that the `spawn unsupervised` sweep leaves two further hits standing in this repository beyond the two
it repairs, locating one in `packages/runtimes/dev_server.py` and one in
`docs/agents/planner_reviewer_prompt.md`; the R67 block's own sweep paragraph says the same, and both
were authored by the reviewer. Measured with `git grep -n "spawn unsupervised"` over `packages/`,
`apps/`, `docs/` and `tests/`, that phrase returns EXACTLY two hits at 261dce53 and EXACTLY two at
a8ba453d — the two live claims themselves — so no further hit exists under those four trees at either
SHA. The `dev_server.py` lines carry the bare word `unsupervised` in the `OWNER_UNSUPERVISED` constant
and never the phrase, and `docs/agents/planner_reviewer_prompt.md` carries 0 occurrences of
`unsupervised` in any case at either SHA, so one half of the claim confuses a word with a phrase and
the other half names a file that never held either. Medium, not High, because no repair was
misdirected — the two findings the sweep bounds are both correct and both resolve above — and not Low,
because that sentence is the BOUNDING claim for both of them: a reader who trusts it believes two
further sites were deliberately left alone and will not look, which is the R-0417 staleness hazard
pointed the other way. The R67 worker measured this and declared it under that block's constraint 8
rather than editing reviewer text, which is why it is registered here rather than shipped.
COUNTER-MEASURE, narrowing R-0561's: when a block orders a gate over a SWEEP, EVERY clause of the
sentence that sweep licenses is read back from the sweep's own output — the total, the path each hit
lands in, and the characterisation of every hit NOT repaired — because a gate that counts hits cannot
fail on a sentence that describes them. R67's G8 ordered the count, got two, and passed while the
prose beside it said four; nothing in that block compared the two, and no gate it ordered could have.
G7 of the R68 block is the first written under this rule, and reading A of that gate — the path of
every hit, not only how many — is the clause R67's G8 was missing. OPEN.

CORRECTION TO RECORD35, appended and not applied, per docs/agents/planner_reviewer_prompt.md §3
checklist item 20: overwriting landed text is worse than a dated wrong sentence, so the clause
registered as R-0563 above stands untouched where it was committed at 60057260 and THIS paragraph is
its retraction, exactly as the correction section of DECISION F085 D6 retracts a ruled figure in
`.agent/decisions.md` without editing it. The true reading, taken by the reviewer at 261dce53 and
again at a8ba453d: the phrase `spawn unsupervised` occurs exactly twice under `packages/`, `apps/`,
`docs/` and `tests/` at each of those SHAs, both occurrences are the two claims R-0561 and R-0562
name, and no third or fourth occurrence of that phrase exists under those four trees at either SHA.
The phrase does recur under `.agent/` — in this workflow's own block mirrors, handbacks and records,
RECORD35 among them — and that is the only place it does, which is why this retraction names the
trees it swept instead of saying `the repository`. R-0561 and R-0562 are unaffected by the
retraction: the sweep that bounds them is COMPLETE at two rather than at four, which makes their
repairs more nearly exhaustive than the sentence claimed, not less.
END-RECORD36
