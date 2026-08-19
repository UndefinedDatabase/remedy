── STEP R66 repair — false class claims — F085 — R67 ─────────────────────────

Goal: repair two documented claims about which command classes run under the guard, both false at
261dce53, and record the R66 FAIL that found the first of them. R66's own worker declared the defect
instead of editing the slice it came in — which is exactly what its constraint 12 asked for — so the
failure is the REVIEWER's and the finding is registered against the reviewer's authored text.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R66 FAIL and register R-0561 and R-0562 · C3 repair the limitations document ·
C4 repair the `exec_guard` module docstring · C5 handback. Findings persist in their OWN commit BEFORE
either repair, which is the order docs/agents/self_drive_protocol.md Phase 2 step 4 requires of a FAIL.
That list runs past five commits, so the handback takes the ≤100-line cap AGENTS.md allows when a
per-commit table needs it.

CONVENTION, binding on every count here, carried verbatim in force from the R66 block. A line count is
the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN21, FIXDOC AND FIXMOD;
ITS ONE END-OF-FILE APPEND, WHICH HAS NO FROM AT ALL, IS RECORD35 — listed rather than counted, per §3
checklist item 11. The append slice CARRIES ITS OWN LEADING BLANK LINES, so the separation its
target's convention requires is a property of bytes that were measured and never of a join shape that
was reasoned about.

## Change

C1 applies PLAN21F→PLAN21T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep a stale
label. C2 appends RECORD35 to the END of `.agent/live_review.md`. C3 applies FIXDOCF→FIXDOCT to
`docs/system/exec-guard-limitations-v0.md`, replacing its one false section. C4 applies
FIXMODF→FIXMODT to `packages/orchestration/exec_guard.py`, replacing the stale clause of the module
docstring's PARTIAL COVERAGE bullet.

Change set, named rather than counted: `.agent/authored/f085-r67.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `docs/system/exec-guard-limitations-v0.md`,
`packages/orchestration/exec_guard.py`, `.agent/handoff.md`. Nothing else. NO `docs/roadmap/**` path
is in that set, so no roadmap file is edited and Rule A4 is untouched; a `docs/**` path IS in it, so
the docs-consistency suite is ordered in G4. ONE `.py` path is in it, so a lint gate IS ordered — but
NO red control is, and G8 proves rather than asserts why: C4 changes bytes INSIDE the module docstring
only, so no statement changes, no behaviour changes, and there is no revert that could redden a test.
Every tracked path named here was resolved on disk at 261dce53 with `git ls-tree`, one call per path,
before emission, per checklist item 24, and all of them exist.

WHAT IS ACTUALLY TRUE, read from `docs/roadmap/features/T2_F085.md` at 261dce53, since both repairs
depend on it. Amendment F085 D1's table carries NINE class rows. SIX are marked `Stage 1 = yes`:
`builder` (5 sites), `test` (12), `dod-process` (1), `dod-app` (1), `runtime-server` (3) and
`runtime-build` (2). THREE are marked `no`: `git` (24), `packaging` (11) and `other` (8 real). The
network column is a SEPARATE column from stage-1 membership: `default-deny` for `builder`, `test` and
`dod-process`, `allowed` for the other three guarded rows, and that file gives the reason — the server
classes are judged by an HTTP readiness probe and `runtime-build` fetches from a package registry.
That file also rules that git, packaging and other are out of stage 1 because their argv is authored
by Remedy itself rather than by a project, states that this is a SCOPE ruling and NOT a safety claim,
notes that several of those sites pass no `timeout` and can hang, and assigns saying so explicitly to
the T003 limitations document — which FIXDOCT is therefore the first version of that document to do.
The runtime class is migrated WHOLE at 261dce53: its three server sites call
`runtime_server_exec_policy` from `packages/runtimes/dev_server.py`,
`packages/runtimes/runtime_supervisor.py` and `apps/cli/commands/runtime_cmd.py`, and its two build
sites call `run_guarded_runtime_build_command` from `packages/orchestration/ui_server.py`.

THE SWEEP BEHIND THIS ROUND, so no third copy of the claim survives. `grep -rn "spawn unsupervised"`
over `packages/`, `apps/`, `docs/` and `tests/` at 261dce53 returns exactly two live claims — the two
this round repairs. The other two hits are not this claim: `OWNER_UNSUPERVISED` in
`packages/runtimes/dev_server.py` is an unrelated constant naming a probe with no supervisor recorded,
and the line in `docs/agents/planner_reviewer_prompt.md` is an EXAMPLE sentence inside the rule about
naming a commit. G8 re-runs that sweep and reports its result, because a repair that fixes two of
three copies is the recurrence this feature has already paid for once (R-0417).

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r67.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   261dce53 and prints its own output here per checklist item 15, one reading per pair:
   PLAN21F→PLAN21T `TO contains FROM: false`; FIXDOCF→FIXDOCT `TO contains FROM: false`;
   FIXMODF→FIXMODT `TO contains FROM: false`. All three are therefore REWRITES and each owes the
   FROM 0x / TO 1x reading over its own post-commit file. Each FROM occurs EXACTLY 1x in its target at
   261dce53 — the reviewer measured all three.
4. RECORD35 HAS NO FROM. It is appended at the END of `.agent/live_review.md`. Its obligation is
   ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of the
   post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are
   exactly the slice's lines IN ORDER. Do not invent a FROM for it and do not report a FROM count.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of both repairs. Only C0a and
   C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. C2 LANDS BEFORE C3 AND C4. A FAIL persists its findings in their own commit FIRST and repairs
   afterwards; a repair that arrives before the record leaves the ledger describing a defect that the
   same commit range has already removed, with no commit to point at.
7. Every sentence in RECORD35 that states a reading of a file names the SHA it was read at in the same
   clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to EVERY
   reading in the clause, not only the first. RECORD35 states readings of R66's range and of this
   round's base only, all of which are prior state, so every SHA it names already exists when it is
   written.
8. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD35 is reviewer text and carries both
   registrations inside it. Do not add a `Landed:` line, do not add a `Done:` paragraph of your own,
   and do not edit RECORD35 to reconcile it with anything you measure. A disagreement between RECORD35
   and your own reading is a finding to REPORT in the handback, never to fix.
9. THIS ROUND REGISTERS EXACTLY TWO FINDINGS AND RESOLVES NOTHING. Registered moves 175 → 177, done
   stays 28, landed stays 0, open moves 147 → 149, and the next free id moves R-0561 → R-0563. The two
   repairs land in this round but are marked resolved by the NEXT round's record, which is where a
   reviewer who has re-read the repaired files writes `Done:` — never by the round that makes them.
   RECORD35 therefore carries exactly two `- R-` registration lines and no `Done:` line; G6 proves it.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r67.md`; a mismatch is a finding against this block, not the worker.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, and never widen the
   change set to route around a red.
12. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. These suites spawn real supervisors that bind a port and leave escapees when a readiness
   assertion fails, so two concurrent runs redden each other on tests neither touched.
13. BOTH REPAIRED TEXTS STATE ONLY WHAT IS BUILT AT HEAD. If you believe a sentence in FIXDOCT or
   FIXMODT is false at 261dce53, that is a finding to REPORT in the handback, never to edit — the same
   rule R66's constraint 12 gave, which is the rule that caught this defect.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. This round orders NO destructive check, so no `git worktree` is
created at all and `git worktree list` is one line at round start and one line at the end.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r67.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD35 line counts read
from that committed file, against constraint 10's 490 / 400 / 140.

G3 SHAPES, measured SEPARATELY per pair and per path. PLAN21F→PLAN21T is a REWRITE over
`.agent/plan.md` at C1, FIXDOCF→FIXDOCT a REWRITE over `docs/system/exec-guard-limitations-v0.md` at
C3, FIXMODF→FIXMODT a REWRITE over `packages/orchestration/exec_guard.py` at C4. For each report its
FROM 0x and its TO exactly 1x over the post-commit blob, and re-applying the extracted FROM→TO to the
pre-commit blob must reproduce the post-commit blob BYTE-EXACTLY. For RECORD35 at C2 report the
ordered-equality readings constraint 4 names: pre-commit blob is a byte-exact PREFIX, the slice is an
exact SUFFIX, `pre + slice` equals the post-commit blob byte for byte, and that commit's ADDED lines
are exactly the slice's lines IN ORDER. Plus `git show --numstat` for each path and commit, plus the
count of lines matching `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker
LINES, never the substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0, and serially per
constraint 12. Report each run's passed count; the counts are reported, never predicted, and only the
exit code is ordered. The reviewer took every base reading below itself, in the primary checkout, at
261dce53.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py tests/orchestration/test_test_runner.py
   tests/test_test_runner.py tests/orchestration/test_ci_run.py
   tests/orchestration/test_managed_builder_execution.py tests/orchestration/test_dod_runners.py
   -q -rf` — base `331 passed`, no skips: the readers of the file C4 edits.
 - `python3 -m pytest tests/docs/test_docs_consistency.py -q` — base `295 passed`; C3 changes
   `docs/**`.
 - `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
   tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
   base `160 passed`; two of them assert on `.agent/plan.md`, which C1 rewrites.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected by
grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 40 lines by applying the pair to that blob at 261dce53.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
261dce53 and at HEAD, from the line-start patterns for a registration, a resolution and a landed line.
The reviewer's base reading is 175 / 28 / 0, 147 open, max registered R-0560, max resolved R-0558. At
HEAD the reading must be 177 / 28 / 0, 149 open, max registered R-0562 and max resolved still R-0558,
because constraint 9 rules this round registers exactly two findings and resolves nothing. The
symmetric difference of the registered sets must be EXACTLY `{R-0561, R-0562}` and the done and landed
symmetric differences must both be EMPTY. Next free id R-0563. Report all three symmetric differences,
the duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs.

G7 LINT, over the one `.py` path this round edits, run from the repository root with the repository's
OWN configuration — no `--isolated`, per §3 checklist item 12. BOTH halves are green at the base, so
both are ordered GREEN rather than compared as multisets; the reviewer executed both at 261dce53
itself, per R-0364, and both printed `All checks passed!`.
 - `python3 -m ruff check packages/orchestration/exec_guard.py` — exit 0.
 - `python3 -m ruff check --preview packages/orchestration/exec_guard.py` — exit 0. The preview half
   is ordered separately because ruff is preview-blind to the E301-E306 class (R-0500, R-0558).

G8 TRUTH AND INERTNESS, the gate this round exists for. Report all six readings.
 - INERTNESS, which is why no red control is ordered: parse the pre-commit and post-commit blobs of
   `packages/orchestration/exec_guard.py` at C4 with `ast.parse`, set each module's docstring to None
   in the tree, and report that `ast.dump` of the two trees is IDENTICAL. That proves C4 changed a
   docstring and nothing executable, which no red control could show and which a red control would
   only pretend to.
 - The two FALSE SENTENCES are gone, while the phrase they shared survives with a corrected subject,
   which is the reading to take rather than a count of the phrase: the sentence
   `the runtime, git and packaging classes still spawn unsupervised` occurs 0 times in
   `packages/orchestration/exec_guard.py` at HEAD, and the sentence `The git, packaging, runtime and
   other call sites still spawn unsupervised` occurs 0 times in
   `docs/system/exec-guard-limitations-v0.md` at HEAD.
 - `grep -rn "spawn unsupervised"` over `packages/`, `apps/`, `docs/` and `tests/` at HEAD returns
   EXACTLY two hits, one in each of the two repaired files, and NEITHER names `runtime` among its
   subjects. The claim survives about `git`, `packaging` and `other`, which is where it is true.
 - `docs/system/exec-guard-limitations-v0.md` at HEAD contains all six stage-1 class names
   `builder`, `test`, `dod-process`, `dod-app`, `runtime-server` and `runtime-build`, each at least
   once. Report one boolean per name.
 - That same file at HEAD contains the string `SCOPE ruling` and the string `can hang`, which is the
   content `docs/roadmap/features/T2_F085.md` assigns to it and which its first version omitted.
 - The old heading `## Only three command classes run under the guard at all` occurs 0 times in that
   file at HEAD.

G9 HYGIENE. `git diff --name-only 261dce53..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular holds none of
`packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`,
`apps/cli/commands/runtime_cmd.py` and `packages/orchestration/ui_server.py`, the four files this
round READS to establish that the runtime class is migrated but must not touch. Those four were each
resolved at 261dce53 with `git ls-tree 261dce53 -- <path>`, one call per path, and all four exist;
re-run those four calls and report each result, per §3 checklist item 24. Report per-commit insertions
for every commit BEFORE C5 — C5 cannot measure itself, so its own go in the round report — and confirm
none exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a second
oversize commit is a STOP under constraint 11, never a declaration. Confirm every commit is
single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
261dce53, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3, C4
and C5, the real G1-G9 results with exit codes, the open-findings count and the next expected action.
The Bundle above holds more than five commits, so the ≤100-line cap applies; if the mandated content
genuinely does not fit even there, name the DECISION D15 stated cause and the specific mandated
content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~99 % (T001 gebaut · R13-R65 PASS · R66 FAIL, Fehler des Reviewers, in dieser Runde
repariert · T002 KOMPLETT · T003 fast fertig: Netz-Posture verdrahtet und gepinnt, Limitations-
Dokument steht, verlinkt und jetzt inhaltlich korrekt; offen bleibt allein die Akzeptanzmessung am
echt lauschenden Server) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R68 measures
T2_F085's remaining acceptance line — a network access from a guarded test command fails under deny —
against a loopback server that is really listening, with the red control that line needs; the
integration gate and closure follow it. TWO: R67 carries no verdict of its own, because the round that
records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R68
carries it, and R68's record is also where R-0561 and R-0562 are marked `Done:` if the reviewer's
re-reading of both repaired files agrees. THREE: a standalone closing line stating the open findings
count and the next free id. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the
self-drive protocol requires every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN21F
## Current Step
R66, this round: T003's document. `docs/system/exec-guard-limitations-v0.md` states what stage 1
does NOT prevent — a proxy posture is not containment, three classes of five run under the guard
at all, an allowlist does not bound what a child's own runtime adds, and an app log written to a
file takes no cap — and `docs/README.md` links it from both tables. The R65 PASS is recorded in
the same round.

## Next Steps
1. The remaining acceptance measurement: a guarded test command is refused against a loopback
   server that is really listening, where the same child without the posture is served.
2. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.
END-PLAN21F

BEGIN-PLAN21T
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
END-PLAN21T

BEGIN-FIXDOCF
## Only three command classes run under the guard at all

Amendment F085 D1's table wires `builder`, `test` and `dod-process`. The `dod-app` class
deliberately takes no wall timeout and no deny — its harness must keep serving on its own
port. The git, packaging, runtime and other call sites still spawn unsupervised, so a limit
proved for a test command says nothing about a `git` invocation.
END-FIXDOCF

BEGIN-FIXDOCT
## Six classes run under the guard, and only three of them deny the network

Amendment F085 D1's table marks SIX classes stage-1 guarded: `builder`, `test`, `dod-process`,
`dod-app`, `runtime-server` and `runtime-build`. Being guarded and denying the network are
SEPARATE columns of that table. Only `builder`, `test` and `dod-process` default-deny. The
other three are guarded but keep network access, because the server classes are judged by an
HTTP readiness probe and `runtime-build` fetches from a package registry — so a guarded
command is not necessarily a command that cannot reach the network.

The `git` (24 sites), `packaging` (11) and `other` (8) classes are NOT stage-1 classes and
still spawn unsupervised, so a limit proved for a test command says nothing about a `git`
invocation. Their exclusion is a SCOPE ruling and NOT a safety claim: their argv is authored by
Remedy itself rather than supplied by a project, which is the problem this feature names. It
follows that several of those sites pass no timeout at all and can hang, and stage 1 does not
fix that.
END-FIXDOCT

BEGIN-FIXMODF
  whole — its bounded checks through `run_guarded_dod_process_command`, and its
  application harness through the CHILD half of `dod_app_exec_policy` — while
  the runtime, git and packaging classes still spawn unsupervised. No count is
END-FIXMODF

BEGIN-FIXMODT
  whole — its bounded checks through `run_guarded_dod_process_command`, and its
  application harness through the CHILD half of `dod_app_exec_policy`; and since
  T002d the runtime class is migrated whole too, its three servers through
  `runtime_server_exec_policy` and its two builds through
  `run_guarded_runtime_build_command` — while the git, packaging and other
  classes still spawn unsupervised. No count is
END-FIXMODT

BEGIN-RECORD35

Gate: R67 — the R66 entry. R66 FAILED, and the failure is the REVIEWER's, not the worker's. Every
ordered gate G1-G8 was re-executed by the reviewer over 97caa9e1..261dce53, not read, and each
reproduces the handback's reading exactly; the worker deviated in nothing, applied every slice
unedited, and declared the defect this entry registers instead of repairing it — which is what that
block's constraint 12 asked for and the reason the defect was caught inside one round rather than at
closure. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD, disk-to-disk with no digest fallback:
the committed `.agent/authored/f085-r66.md` and the committed `.agent/last_block.md` at 261dce53,
both working copies at 261dce53, and the received `.remedy-wt/f085-r66.md` are all five byte-EQUAL at
sha256 9a356739fc567d675cfb1a075b48b7916ad6c13fd4ad9eb587c8d216142000e6, 26720 B, 379 lines, 16 marker
lines. THE SHAPES HELD: PLAN20 over `.agent/plan.md` at 9cc64066 and INDEX1 over `docs/README.md` at
5cc11db0 are REWRITES, each reading `TO contains FROM: false`, each FROM 1x pre-commit and 0x with TO
exactly 1x post-commit; INDEX2 over that same file at that same commit is APPEND-shaped, reading FROM
1x AND TO 1x post-commit with no FROM-zero reading taken; both `docs/README.md` pairs re-applied IN
ORDER reproduce the post-commit blob BYTE-EXACTLY, as does the PLAN20 pair on its own file. RECORD34
over `.agent/live_review.md` at 70f09162 satisfies ORDERED EQUALITY on every clause — PREFIX, SUFFIX,
`pre + slice` equal byte for byte, ADDED lines equal to the slice's lines IN ORDER, 51 and 51. DOCLIM
at 69addbbf satisfies WHOLE-FILE equality: `git ls-tree 97caa9e1` for that path is EMPTY and the
post-commit blob equals the DOCLIM bytes exactly. Marker LINES at 261dce53 are 0 in each of the four
edited files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout, serially, each exit 0:
`295 passed` for the docs-consistency suite, `160 passed` for the four state readers and the canary
`42 passed`, each equal to its base. THE PLAN CONTRACT HELD at 261dce53: 40 lines against the 50-line
cap with `## Goal`, `## Next Steps` and a roadmap F-id all present, 40 being that block's own
projection. THE ARITHMETIC DID NOT MOVE, as that block's constraint 8 required: 175 registered / 28
done / 0 landed and 147 open at both 97caa9e1 and 261dce53, max registered R-0560 and max resolved
R-0558 at both, all three symmetric differences EMPTY, and 0 duplicate ids and 0 orphan resolutions at
both SHAs. THE LINK GATE HELD at 261dce53: `system/exec-guard-limitations-v0.md` occurs exactly twice
in `docs/README.md`, the path resolves, and the file it resolves to is byte-identical to the DOCLIM
slice. WHAT FAILED IS THE CONTENT THOSE GATES NEVER READ. Not one of the eight gates asked whether the
document's sentences are TRUE, so a shape-perfect round published a false claim, and the only reason
it did not survive is that a human-facing constraint asked the worker to report disbelief.

- R-0561 — Medium — the T003 limitations document published a false statement of which command
classes run under the execution guard, and the reviewer authored it. The DOCLIM slice, applied
byte-verbatim at 69addbbf, carried the heading "Only three command classes run under the guard at all"
and the sentences "Amendment F085 D1's table wires `builder`, `test` and `dod-process`" and "The git,
packaging, runtime and other call sites still spawn unsupervised". Read at 261dce53,
`docs/roadmap/features/T2_F085.md` marks SIX rows `Stage 1 = yes` — `builder`, `test`, `dod-process`,
`dod-app`, `runtime-server` and `runtime-build` — and only three of those six carry `default-deny` in
the SEPARATE network column. The document therefore reported the DENY set as if it were the GUARDED
set, and named `runtime` among the unsupervised when its three server sites call
`runtime_server_exec_policy` at 261dce53 from `packages/runtimes/dev_server.py`,
`packages/runtimes/runtime_supervisor.py` and `apps/cli/commands/runtime_cmd.py` and its two build
sites call `run_guarded_runtime_build_command` from `packages/orchestration/ui_server.py`. The same
conflation reached `.agent/plan.md` at 9cc64066 as "three classes of five". Medium, not High, because
the error UNDERSTATES coverage — it credits the guard with less than it does, so no reader is misled
into trusting an unguarded path — and not Low, because this document exists precisely to be the
truthful account of what stage 1 does and does not do, and a limitations document that misdescribes
its own scope cannot serve that purpose. It also omitted content `docs/roadmap/features/T2_F085.md`
explicitly assigns to it: that the git, packaging and other exclusion is a SCOPE ruling and not a
safety claim, and that several of those sites pass no timeout and can hang. C3 of this round replaces
the section and adds the omitted content. COUNTER-MEASURE: a block that authors PROSE ASSERTING A FACT
ABOUT THIS REPOSITORY orders a gate that reads that fact back from its source — the class names from
the D1 table, the call sites from a grep — exactly as it already orders shape and arithmetic gates.
R66 ordered eight gates and not one of them could have failed on a false sentence; G8 of the R67 block
is the first of this kind and is the shape the rule takes. OPEN.

- R-0562 — Low — the `exec_guard` module docstring still called the runtime class unsupervised two
rounds after this branch migrated it. The PARTIAL COVERAGE bullet read "the runtime, git and packaging
classes still spawn unsupervised" at 261dce53, while R61 and R63 migrated all three `runtime-server`
sites and `packages/orchestration/ui_server.py` has called `run_guarded_runtime_build_command` for
both `runtime-build` sites since T002d. This is the R-0506 class — a documented absence claim
falsified by the migration that the same branch performed, and not retired in the round that
falsified it — arriving in the module whose docstring is the first thing a reader of this seam sees.
Low, because the claim is an inventory note rather than a safety property, and the bullet's own
sentence already declines to write a count "because it changes with every migration round", which is
the same instinct applied one clause too narrowly. C4 of this round repairs it. The sweep that bounds
both findings is reported in the R67 block and re-run by its G8: `spawn unsupervised` has exactly two
live occurrences at 261dce53, this one and R-0561's, and the two remaining hits in the repository are
an unrelated constant in `packages/runtimes/dev_server.py` and an example sentence in
`docs/agents/planner_reviewer_prompt.md`. OPEN.
END-RECORD35
