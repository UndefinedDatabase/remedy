# STEP — F037 Rendered diff viewer, round 25 — THE INTEGRATION GATE

## Who you are and what binds you

You are the WORKER of a self-drive round (docs/agents/self_drive_protocol.md).
AGENTS.md is the highest authority and nothing here weakens it: the self-review
loop before every commit, the Commit Gate, small commits, push discipline, and
the `.agent/plan.md` currency rule all apply in full. You are the only actor in
this round that writes anything. The reviewer is read-only and will re-run every
gate below itself before issuing a verdict, so a number you report and a number
that is true must be the same number.

BASE. This round starts from commit `38966bf3`, which is the tip of branch
`feature/f037-rendered-diff-viewer`. Read `.agent/STOP` from disk before your
first commit; if it exists, write the handback and end without doing anything
else.

SESSION. This is SESSION 8 of feature F037 and round 25. The rounds planned for
this session are R25 (this one), R26 and R27; R27 is the round that ends the
session and the feature's closure sequence. Carry "SESSION 8 of feature F037 ·
round 25 · rounds so far 25" in the handback's Session section.

WHY THIS ROUND IS PERMITTED PAST THE SOFT LIMIT. Operator amendment
amend0827-process-diet rule 6 makes a SCOPE REPORT the obligation at the soft
limit, and R24 discharged that obligation: DECISION F037 D11 and feature-file
amendment A6 are on disk and the report is in `.agent/handoff.md` at `38966bf3`.
Rule 1 of the same amendment names a feature's CLOSURE SEQUENCE as the one
exception to the ban on bookkeeping-only rounds. This round is the first of the
three that sequence needs.

## Goal

Run F037's integration gate — the full suite on this branch and again at the
merge base, compared and attributed — and book the two record entries the
closure needs, so that F037 enters its evidence round with no open finding of
its own and with closure precondition 2 satisfied by a real run.

## Bundle, in this commit order

- C0a — save the block verbatim to `.agent/authored/f037-r25.md`.
- C0b — mirror the same bytes into `.agent/last_block.md`.
- C1 — rewrite `.agent/plan.md` from the PLANF037R25 slice.
- C2 — append GATER24 then DONE719 to `.agent/live_review.md`, in that order.
- C3 — write the integration-gate evidence under `.agent/gate_f037_r25/`.
- C4 — rewrite `.agent/handoff.md` as the handback, then push.

## Change set — these paths and nothing else

- `.agent/authored/f037-r25.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/gate_f037_r25/` (the evidence files named under C3 below)
- `.agent/handoff.md`

Nothing under `apps/`, `packages/`, `tests/` or `docs/` is touched by this
round. No test is edited, added, deleted or skipped, and no assertion is
weakened. If the gate finds a real regression, you STOP and hand back: the
repair is its own reviewer-gated round, never a fix folded into this one.

## Slice convention

The authored texts below are delimited by lines beginning `<<<SLICE ` and
`<<<END `, each naming its own label. The delimiter lines are transport markers
and never reach a target file. Apply each slice BYTE FOR BYTE, including its
trailing newline and excluding the delimiter lines. Do not reflow, reword,
retitle, correct or shorten a slice, even where you believe it is wrong — if a
slice is wrong, apply it as written and declare the problem in the handback's
deviations. The labels used below are PLANF037R25, GATER24 and DONE719.

<<<SLICE PLANF037R25
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D11.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse and
virtual scrolling. `docs/roadmap/features/T5_F037.md` holds Goal & Done, the task
slicing, the binding CSS and the design amendments A1 through A6, the last of
which records what this feature deliberately no longer ships.

## Current Step
R25 is the INTEGRATION-GATE round, the first of F037's closure sequence. It books
the R24 verdict, resolves `R-0719` — whose counter-measure landed as amendment A4
at `c60a7318`, two commits after the entry that registered it, and was never
written up — and then runs the full suite twice: once on this branch and once in
a throwaway worktree at the merge base `9dde5495`, comparing the two failure sets
and attributing every branch-only id. The raw evidence lands under
`.agent/gate_f037_r25/`. Nothing under `apps/`, `packages/`, `tests/` or `docs/`
is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R24 verdict and one resolution | ordered | record first |
| C3 the integration-gate evidence | ordered | the round's substance |
| C4 the handback | ordered | |

## Next Steps
1. The evidence-and-zip round: the feature file's Built State section, the
   `create_manual_completion_bundle` evidence job, and a FRESH review zip whose
   failure is a closure blocker.
2. The STATUS round: the `[x]` line, the README capability sync in the SAME
   commit, and the closure PR, which this session does not merge.

## Risks
- A6 narrows what F037 ships. Reversing it is one paragraph in each of
  `.agent/decisions.md` and the feature file, both named in D11.
- The base worktree lacks `apps/ui/node_modules` and `apps/ui/dist`. Both are
  restored with symlinks PRESERVED, or the base-only set fills with environment
  failures that mask the real ones.
<<<END PLANF037R25

<<<SLICE GATER24
Gate: F037 R24 — the SCOPE-REPORT round that F037's seven-session soft limit made the obligation. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `38966bf3` rather than reading the handback's numbers. TRANSPORT IS REPORTED FOR EXACTLY WHAT IT COVERS, per the pre-emission checklist's item on transport claims: no reviewer scratch original of the R24 block survives into this session, so the chain walked here runs from the committed C0a blob to its C0b mirror and no further — the committed `.agent/authored/f037-r24.md` blob is 26106 bytes, 341 lines, sha256 `fe2e3a1afdc6479472ec744f9afb7f34b86f640d353ebe21a0010f890b674cda`, and at `a01d9036` that path and `.agent/last_block.md` are ONE blob `dce091538cc0d1e695cc0f92d0cd616bf1c308b1`. That proves the worker was SELF-CONSISTENT and says nothing about the emitted bytes, which this workflow cannot measure and which this verdict therefore does not claim.

EVERY SLICE WAS RE-EXTRACTED FROM THE COMMITTED BLOB AND RE-APPLIED BY THE REVIEWER. `.agent/plan.md` at `e6e8851f` is byte equal to PLANF037R24 including its trailing newline, the negative control that drops that newline is False, and the file is 43 lines carrying exactly one `## Goal` and one `## Next Steps`. The two-slice append to `.agent/live_review.md` at `f4181491` satisfies reader (a) byte for byte with a control flipped inside the FIRST appended paragraph rejected, and the pre-round blob is a byte PREFIX at 1308970 bytes growing to 1316230; reader (b) measured 5 blank-line units against the slices' 5 paragraphs, matching IN ORDER. DECISIOND11 at `421a4004` and AMENDMENTA6 at `24a28760` are proved the same way, prefix and equality True with each negative control False, 684609 growing to 687668 and 10885 growing to 12982; over the C3 blob `^## DECISION ` rose from 176 to 177 with `F037 D11` occurring exactly once, and over the C4 blob the lines starting `**A6` and `**A5 ` are exactly one each. SCOPEREPORT is present verbatim in `.agent/handoff.md` at `38966bf3`, carrying the unmissable SITZUNGS-LIMIT line that amendment mandates.

THE RECORD MOVED EXACTLY AS THE BLOCK PREDICTED BEFORE THE ROUND RAN, every figure re-measured by the reviewer at `82d3d584` and at `f4181491`: registrations UNMOVED at 292 and all 292 DISTINCT, `^Done: R-\d+ — ` 41 to 42, `^Landed: R-` UNMOVED at 11, `^Gate: F\d+ R\d+ — ` 93 to 94, and the OPEN SET computed AS A SET fell from 253 to 252, which is `R-0731` resolved and no id registered. `Gate: F037 R23` occurs exactly once in the `f4181491` blob.

THE SCOPE REPORT IS TRUE WHERE IT IS CHECKABLE, which is the half of this verdict that matters most, because a report the operator acts on is worth no more than its measurements. Re-measured by the reviewer at `38966bf3` rather than at the base the report itself names: `loadDiffLanguageBundle` is referenced under `apps/` in exactly two files, its own module `apps/ui/src/api/diffViewModel.ts` and `apps/ui/src/api/diffViewModel.test.ts`, and the second of the two test files the report names is `tests/ui_contracts/test_diff_view_model.py` — so the claim that it has no caller outside its own module and its two test files holds at the round's tip and not only at its base, and amendment A6 rests on a measurement rather than on a recollection.

RE-RUN SUITES, primary checkout, ONE pytest process at a time, every one exit 0 and every figure equal to the handback's: `tests/ui_contracts/` 653 passed 4 skipped; `tests/ui_server/` 495 passed; `tests/orchestration/test_test_runner.py` with `tests/docs/` 347 passed; the canary `tests/cli/test_golden_path.py` 42 passed. THE STRUCTURE IS CLEAN: the path set over `82d3d584..38966bf3` is exactly the seven files the handback names, with the residue EMPTY in both directions; `git diff --stat` restricted to `apps/`, to `packages/` and to `tests/` prints NOTHING in all three cases, which is the change set's central constraint measured rather than asserted; the seven commits are each single-parent in the chain the handback states, and their insertions 341, 270, 25, 10, 46, 33 and 200 are each under 500 and each equal to the corresponding cell of the handback's `## Commits` table — the `.agent/plan.md` row reading `+25 / -29` against `git diff --numstat`'s `25` and `29`, which is the comparison the checklist's handback-template item exists to force. The marker sweep for both transport-delimiter prefixes is 0 in all five real targets against 6 and 6 in the C0a blob as its control, and `git ls-files .remedy-wt` is 0.
<<<END GATER24

<<<SLICE DONE719
Done: R-0719 — RESOLVED at F037 R8 by the amendment that round authored, and verified by the reviewer at `38966bf3`. The counter-measure this finding names is to amend the feature file rather than the design reference, with the amendment naming the three real authorities, and `docs/roadmap/features/T5_F037.md` carries exactly that as amendment A4 under its "Design amendments" section: the binding CSS block of the file's own Design section, `component_spec.md:113-116` for the entry-point contract, and `assets_spec.md:92-95` for the mono family with ligatures off. A4 closes by stating that the banner's `ux_spec.md` pointer is SUPERSEDED for the diff surface and for nothing else, which is the narrow repair the finding asked for rather than a wholesale rewrite of the banner, and DECISION F037 D3 records the choice and how to reverse it. The fix landed at `c60a7318`, two commits after `345235ca` registered the finding — inside the very round that raised it — and that is why it stayed OPEN for the rest of the feature: no later block re-read the open set for a finding whose repair was already on disk, which is the R-0694 class and the reason the pre-emission checklist now requires that read. It is resolved here, in the first round of the closure sequence, so F037 reaches its evidence round with no open finding of its own.
<<<END DONE719

## Constraints

1. Apply every slice byte for byte. A slice you believe is wrong is applied as
   written and the problem is declared in the handback's deviations. Never edit,
   reflow or repair a slice.
2. The change set above is exhaustive. `apps/`, `packages/`, `tests/` and
   `docs/` are untouched by every commit of this round.
3. `.agent/plan.md` is rewritten at C1, BEFORE the record commit, because this
   round moves the finding ledger and the AGENTS.md Commit Gate requires the plan
   to be current before every commit.
4. GATER24 and DONE719 are appended to `.agent/live_review.md` in that order, at
   C2, each preceded by exactly one newline separating it from what is already
   there. You author no `Done:`, `Gate:` or `Landed:` paragraph of your own: only
   the reviewer's text sets a resolution.
5. Nothing in this round is a repair. If the integration gate produces a
   reproducible branch-only failure coupled to feature code, you STOP after C3,
   record it in full, write the handback and end. Do not fix it, do not deselect
   it, do not re-run until it passes.
6. Never force-push, never rewrite history, never work on `main`, and create no
   pull request. Merges happen only at the Open PR Gate and not in this round.
7. The primary checkout satisfies `git status --porcelain` == 0 at every commit
   boundary. Every destructive or exploratory step runs inside the throwaway
   worktree C3 creates, and that worktree is removed and pruned before C4.
8. This session's shell guard rejects some command FORMS — shell loops, command
   substitution, indexed expansions, and inline environment assignments. Where a
   form is rejected, re-express the same measurement through
   `python3 - <<'PY'` and pass `env=` to `subprocess.run`. A rejected form is
   never a reason to weaken, skip or substitute a gate; report the re-expression
   in the handback.

## C3 in detail — the integration gate

Follow docs/agents/integration_gate.md. Its steps are canonical; what follows
names the mechanisms this environment needs, and where the two differ the
mechanism named here wins because it is the one measured on this machine.

a. WARM DIST FIRST. Before the branch run, record whether
   `apps/ui/dist/index.html` exists and whether its mtime exceeds the mtime of
   every file under `apps/ui/src`. Report both readings. A cold or stale dist
   turns `pytest -n auto` red on a ui_server test for a reason that has nothing
   to do with this branch. The reviewer measured this warm at `38966bf3` and did
   not rebuild; you MEASURE it rather than taking that reading on trust. If it
   reads stale, stop and hand back — building the frontend is refused to
   delegated workers in this environment, so a stale dist is a handoff and not a
   task.

b. BRANCH RUN. `python3 -m pytest -n auto -q` from the repository root, output
   captured IN MEMORY and never into a file inside the worktree while the run is
   alive. Record the raw tail, the exit code and the wall time to
   `.agent/gate_f037_r25/branch_run.txt`, and the sorted list of lines beginning
   `FAILED` to `.agent/gate_f037_r25/branch_failed.txt`.

c. BASE WORKTREE. `git worktree add -b tmp/f037-r25-base
   .remedy-wt/f037-r25-base 9dde54956afbe5f432bfd429bf4ba0bb272f6d07` — that SHA
   is `git merge-base main HEAD` measured by the reviewer at `38966bf3`. It must
   be a BRANCH and never a detached head: the self-dogfood guard refuses a
   detached head by design.

d. PARITY. Copy `apps/ui/node_modules` and `apps/ui/dist` from the primary
   checkout into the base worktree with `shutil.copytree(src, dst,
   symlinks=True)`. `symlinks=True` is load-bearing and is ordered here as an
   ARGUMENT rather than left to the function's default: `copytree` defaults to
   `symlinks=False`, which dereferences npm's `.bin` shims and itself CAUSES
   base-only failures — the defect finding `R-0591` records. Never symlink either
   directory itself; the auto-build writes through such a symlink into the
   primary checkout.

e. NEUTRALISE THE STALENESS PREDICATE, then prove it. Raise the mtime of the
   base worktree's `apps/ui/dist/index.html` above every file under that
   worktree's `apps/ui/src`. Then IMPORT `_frontend_is_stale` from
   `packages/orchestration/ui_server.py` AS IT EXISTS IN THE BASE WORKTREE, call
   it with that worktree as the working directory, and record that it answers
   False. Write the reading to `.agent/gate_f037_r25/auto_build_neutralization.txt`.
   Calling the real predicate is the point: a copied timestamp that satisfies
   your arithmetic but not the function's is the failure this step exists to
   catch.

f. BASE RUN. The same command as (b), working directory the base worktree, with
   `REMEDY_UI_NO_AUTO_BUILD=1` passed through `env=` — not exported, not assumed
   sufficient. Record the mtime of every file under the base worktree's
   `apps/ui/dist` immediately before and immediately after the run, and report
   the run's time window beside them. ANY mtime falling inside that window VOIDS
   the parity claim; report the claim as VOID in that case rather than repairing
   it, and note that a void claim costs nothing when the base-only set is empty
   because no id is then owed an attribution. Write the run to
   `.agent/gate_f037_r25/base_run.txt`, the sorted `FAILED` lines to
   `base_failed.txt`, and the mtime window to `parity.txt`.

g. COMPARE. `comm -13 base_failed.txt branch_failed.txt` is the branch-only set;
   `comm -23` is the set the branch fixed. Report BOTH, in full and never
   truncated, to `.agent/gate_f037_r25/comm.txt`.

h. ATTRIBUTE, and attribute unconditionally. For EVERY branch-only id, re-run
   that exact node id SERIALLY, alone, and classify it: serial-pass is the xdist
   flake class and is recorded rather than blocking; serial-fail is reproduced at
   the merge base before the feature is blamed; a reproducible branch-only
   failure coupled to feature code is a BLOCKER and constraint 5 applies. For
   EVERY base-only id, name the missing artifact that explains it, by direct
   evidence and per id. This obligation does not depend on the parity claim's
   outcome and is not discharged by parity holding. Write it to
   `.agent/gate_f037_r25/attribution.txt`; if a set is empty, write that it is
   empty and say so explicitly rather than leaving the file absent.

i. CLEAN UP. Remove the worktree, prune, delete the `tmp/f037-r25-base` branch,
   and prove the result with `git worktree list`. Write a one-screen
   `.agent/gate_f037_r25/summary.txt` naming the two exit codes, the two wall
   times, the two failure counts, the two `comm` set sizes, the parity verdict
   and the canary result. Delete every scratch file you created OUTSIDE that
   directory by its exact path; never by a glob.

## Done when — the gates

Run every gate and record its real exit code and real output. "Green" as a word
is a finding. Gates G1 through G7 run at or before C3 and strictly before C4, so
the handback can quote them; C4's own insertion count belongs to the next
round's ledger entry and is not gated here.

G1 HYGIENE. `.agent/STOP` read from disk and reported ABSENT before C0a and
again before C4. `git rev-parse HEAD` before C0a equals the BASE `38966bf3`.
`git branch --show-current` is `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` is 0 after each of C0a, C0b, C1, C2 and C3.

G2 TRANSPORT. Report the sha256 of the committed `.agent/authored/f037-r25.md`
blob and the sha256 of the reviewer's own original at
`.remedy-wt/f037-r25-block.md`, and assert they are EQUAL. That file existed
before you did, so this reading covers the emission and not merely your own
self-consistency — state that in the handback, and state no digest you have not
computed. Then report that `git rev-parse` of `HEAD:.agent/authored/f037-r25.md`
and of `HEAD:.agent/last_block.md` at C0b name ONE blob, and give that blob id.

G3 THE PLAN AT C1. The PLANF037R25 slice, re-extracted from the COMMITTED C0a
blob with `git show <C0a>:.agent/authored/f037-r25.md`, is BYTE EQUAL to
`.agent/plan.md` at C1 including its trailing newline. Report the file's `wc -l`,
which must be strictly under 50, and the counts of lines exactly `## Goal` and
exactly `## Next Steps`, which must each be 1.

G4 THE RECORD AT C2, both readers. (a) The `38966bf3` blob of
`.agent/live_review.md`, plus a newline, plus GATER24, plus a newline, plus
DONE719, equals the C2 blob — with a NEGATIVE CONTROL that flips one byte inside
the FIRST appended paragraph and is REJECTED. (b) Split the C2 blob on blank
lines; let N be the number of paragraphs your own script COUNTS in the two
slices, and compare the LAST N units of the file against those paragraphs IN
ORDER. Report N as you measured it. Also report that the pre-round blob is a byte
PREFIX of the C2 blob and give both byte lengths. Read every non-current revision
with `git show <sha>:<path>` into memory; write over no tracked file.

G5 THE LEDGER. Over the C2 blob, and with the base figures RE-MEASURED at
`38966bf3` rather than inherited from this block: the count of `^- R-\d+ — `,
which the reviewer measured at 292 at the base and which this round must leave
UNMOVED, and whether all of them are DISTINCT; `^Done: R-\d+ — `, 42 at the base,
which must rise by exactly ONE; `^Landed: R-`, 11 at the base and UNMOVED;
`^Gate: F\d+ R\d+ — `, 94 at the base, which must rise by exactly ONE; and the
OPEN SET computed AS A SET — every registered id minus every `Done:` id — which
the reviewer measured at 252 at the base and which must FALL to 251. Report that
`Gate: F037 R24` occurs exactly once in the C2 blob and that `R-0719` now has a
`Done:` line.

G6 THE INTEGRATION GATE. All of C3 (a) through (i) executed and its evidence
files present under `.agent/gate_f037_r25/`. Report: the dist readings; both exit
codes; both wall times; the branch and base failure counts; both `comm` set sizes
IN FULL and never truncated; the parity verdict with its mtime window; the
per-id attribution for every branch-only and every base-only id; and
`git worktree list` after the cleanup, showing the primary checkout alone.

G7 THE CANARY AND THE STATE CONTRACTS, run after C3 and before C4, ONE pytest
process at a time in the primary checkout, each with its real exit code:
`python3 -m pytest tests/cli/test_golden_path.py -q` — the reviewer measured 42
passed at `38966bf3`; and `python3 -m pytest tests/ui_contracts/ -q` — 653 passed
and 4 skipped at `38966bf3` — which is the suite that reads the `.agent/plan.md`
this round rewrites. Record both to `.agent/gate_f037_r25/canary.txt`.

G8 STRUCTURE AND THE OPEN PR GATE, measured at C3. `git diff --name-only
38966bf3..<C3>` equals the change set above minus `.agent/handoff.md`, with the
RESIDUE reported EMPTY IN BOTH DIRECTIONS — measured-minus-changeset and
changeset-minus-measured, each printed. `git diff --stat 38966bf3..<C3>`
restricted to `apps/`, to `packages/`, to `tests/` and to `docs/` prints nothing
in all four cases. Every commit from C0a through C3 is single-parent; report each
one's insertion count from `git diff --numstat` and assert each is under 500, and
report those same numbers in the handback's `## Commits` table so the two
readings agree cell by cell. `git grep -c` for `^<<<SLICE ` and for `^<<<END ` is
0 in `.agent/plan.md` and in `.agent/live_review.md`, against the non-zero
control of `.agent/authored/f037-r25.md`. `git ls-files .remedy-wt | wc -l` is 0.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` is
reported with its real output. Finally, because this round's change set includes
an EVIDENCE path, run `git ls-files` over each build-output glob `.gitignore`
names — `*.zip`, `*.log`, `*.egg`, `*.egg-info`, `build`, `*/build/*`, `dist`,
`*/dist/*`, `node_modules`, `*/node_modules/*`, `sdist`, `packages.zip` and
`remedy-job-evidence-*` — require the total EMPTY, and record the reading. The
reviewer measured every one of those globs as 0 at `38966bf3`; you re-measure
rather than inherit. This is the fix clause finding `R-0677` binds on the next block whose
change set carries a packaging or evidence path.

## Handback

Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md and the
AGENTS.md `### handoff.md` section. It has NO length cap. It carries: the Session
section with the session number and roster above; the review range
`38966bf3..HEAD`; a per-commit `## Commits` table whose `+/-` cells are the
`git diff --numstat` readings of G8; the External actions; a Verification section
with ONE LINE PER GATE, G1 through G8, each carrying its real figures; the
Authored-text proofs; the Deviations and assumptions, including every re-expressed
command form; the item-status table covering every C and every G exactly once;
the open-findings count; and the Next section, which names the evidence-and-zip
round and tells the next session to apply Phase 1 rule 1 (`.agent/STOP`) before
rule 2 (the Open PR Gate). Then `git push -u origin
feature/f037-rendered-diff-viewer` and record its outcome. Create no PR.

ANY COMMIT BEYOND THE ORDERED SEQUENCE ABOVE receives its OWN `## Commits` row
and its OWN item-status row, and the Deviations section states its existence in
the same words rather than beside a clause denying it — a handback may not both
deny and disclose the same commit. Where the ordered sequence was followed
exactly, say that and nothing more. This is the fix clause finding `R-0675` binds
on the next block that orders a handback.
