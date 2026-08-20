── STEP R18 — F086 Release capability (record R17; resolve R-0584; rule D4) ──

Goal:
Close the record R17 opened and rule the one design question standing between this
feature and its last piece of work. R17 registered R-0584 and repaired it; the
reviewer has since re-executed every gate over `4750383c..f0b27118` and the repair
holds, so this round replaces the worker's `Landed:` line with the reviewer's
`Done:` text, records R17's verdict, and writes DECISION F086 D4 — where the
install smoke executes, and why no round of this workflow can execute it.

THIS ROUND WRITES NO PRODUCTION CODE AND NO TEST. Its change set is state files
only. The install smoke itself is R19's work, and D4 is what R19 implements.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r18.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN18 slice, whole file
  C2  replace the `Landed: R-0584` line in `.agent/live_review.md` with DONE0584
  C3  append RECORD16 to `.agent/live_review.md`
  C4  append DECISION4 to `.agent/decisions.md`
  C5  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C6  append the VERDICT slice to `.agent/handoff.md`

C1 precedes every ledger commit because §3 item 23 requires the plan to advance
first. C2 and C3 are separate commits although both write one file: C2 is a
REPLACEMENT and C3 an APPEND, and a commit holding both would make the append's
prefix proof unmeasurable.

Base:
This round starts from `f0b27118`, the tip of `feature/f086-release-capability`
and the R17 handback commit. Every range gate names that SHA. Stay on the branch:
do NOT create one, merge, or open a PR — F086's PR belongs to its closure round.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. PLAN18 is a
COMPLETE file including its single trailing newline. RECORD16, DECISION4 and
VERDICT are EOF-APPENDS: pure concatenation, each slice's own leading blank line
INSIDE the slice, nothing prepended, nothing stripped. LANDEDFROM and DONE0584 are
a single-line replacement pair, each carrying its own trailing newline and no
leading blank line — the blank line above that line is already in the file and is
not part of either slice.

PAIR SHAPE, from the containment test run on these exact bytes at emission:
  LANDEDFROM → DONE0584   TO contains FROM: false → REWRITE → FROM 0x and TO 1x
  are orderable at HEAD.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `f0b27118`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r18.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r18.md`; copy that file rather than retyping it. Commit alone.
   C0b then copies the COMMITTED `.agent/authored/f086-r18.md` over
   `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN18 slice, byte-verbatim, whole file. Alone.

3. C2 — in `.agent/live_review.md`, replace the single line LANDEDFROM with
   DONE0584. LANDEDFROM occurs exactly 1x in that file at `f0b27118`; count it
   before replacing it. Nothing else in the file changes — not the blank line
   above it, not the trailing newline after it. Commit alone.
   This is §4 item 4 being honoured rather than described: the worker's `Landed:`
   line said a fix had landed, and only reviewer-authored text may say it is
   resolved.

4. C3 — append RECORD16 to `.agent/live_review.md` under the append convention.
   Commit alone. It is the reviewer's R17 verdict and begins `Gate:`.

5. C4 — append DECISION4 to `.agent/decisions.md` under the append convention.
   Commit alone. That file is an append-only ledger: do not reflow, re-indent or
   renumber anything already in it.

6. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of f0b27118..<HEAD>`; write the literal token `HEAD`, this
   branch's convention from R10 onward, because a handoff cannot name the SHA of
   the commit that writes it.
   THE VERIFICATION SECTION IS A SUMMARY, NOT A TRANSCRIPT — one line per gate:
   its number, what it measured in a clause, and its real colour or value (the
   R-0582 repair; G12 measures it). The FULL transcript goes in your ROUND REPORT,
   which no cap binds.
   THE BUDGET IS ARITHMETIC: the VERDICT slice C6 appends is 42 lines, measured by
   the reviewer, so 58 of the 100 remain for your text. Measure it yourself from
   the COMMITTED C0a file before writing C5, and state the FINAL line count of
   `.agent/handoff.md` in your Deviations section. Do NOT trim after C6.
   `Next` names, in order, the next session's first three actions: re-read
   `.agent/STOP` from disk (Phase 1 rule 1), run the Open PR Gate (rule 2), then
   review `f0b27118..HEAD` and record R18's verdict (rule 4).

7. C6 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C5 must be a byte-exact PREFIX of the file at HEAD.

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r18.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `.agent/decisions.md`, and `.agent/handoff.md` at C5
   and C6. NOT `tests/orchestration/test_release_workflow.py`, not
   `.github/workflows/release.yml`, not `scripts/release_gate_check.py`, not
   `packages/orchestration/ci_stages.py`, not `pyproject.toml`, and nothing under
   `apps/`, `packages/`, `tests/` or `docs/`. All five named files exist at
   `f0b27118`, so the prohibition forbids something real (R-0559).
3. DONE0584, RECORD16, DECISION4 and VERDICT are the reviewer's text. Do not
   summarise or reformat them, and do not write a verdict of your own anywhere —
   in the handoff, in a commit message, or in your report. Reporting what a gate
   MEASURED is your job; ruling on a round is not. This round grants no
   exception: unlike R17, there is no worker-authored line in it.
4. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback, and `git worktree list` reads one line throughout. This round
   orders NO mutation and NO disposable worktree: it writes no code, so there is
   nothing to red-prove, and inventing a mutation to look thorough would prove
   nothing about a state file.
5. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
6. SIZE, measured at emission on the final bytes: this block is 379 lines TOTAL —
   232 prose and 147 slice including its 12 marker lines — against DECISION F085
   D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED C0a file
   and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`;
    `git worktree list` one line.

G2  TRANSPORT. `.remedy-wt/f086-r18.md`, the committed
    `.agent/authored/f086-r18.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN18 slice extracted
    from the COMMITTED `.agent/authored/f086-r18.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  THE RESOLUTION REPLACED THE LANDED LINE. In `.agent/live_review.md`:
    LANDEDFROM occurs exactly 1x at `f0b27118` and exactly 0x at HEAD, and
    DONE0584 occurs 0x at `f0b27118` and exactly 1x at HEAD — four counts,
    reported one by one. The ORDERED-EQUALITY reading: the file as C2 committed it
    is byte-equal to the `f0b27118` blob with that one occurrence replaced and
    nothing else changed, and `git show --numstat <C2> -- .agent/live_review.md`,
    with C2's real SHA in place of `<C2>`, reads 1 insertion and 1 deletion.
    Report C2's blob sha256.

G5  THE LEDGER APPEND. The blob C2 committed is a byte-exact PREFIX of the blob C3
    committed and the remainder is byte-equal to RECORD16. Report the remainder's
    own full sha256 and its line count.

G6  LEDGER SETS, BOTH EXTRACTIONS. Extract twice — once by PARAGRAPH (split on
    blank lines; a paragraph counts when it STARTS with `- R-\d+ — ` or
    `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and `^Done: R-\d+ — `).
    At HEAD report registered / resolved / duplicate ids / unregistered
    resolutions / anchored `Landed:` lines / open, for BOTH, and the two
    registered id SETS must be EQUAL. Expected at HEAD: 167 registered, 3
    resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:` lines, 164
    open. Report the symmetric difference of the HEAD registered set against the
    `f0b27118` set AS THE SET; it must be EMPTY, this round registering nothing.
    Report the RESOLVED set at both ends; it must gain exactly `R-0584`.
    CONTROL: the SAME extractor over `4750383c..f0b27118` must read `['R-0584']`
    for the REGISTERED symmetric difference, so an empty reading above is a real
    absence of movement rather than a blind extractor.

G7  THE DECISIONS APPEND. The pre-C4 blob of `.agent/decisions.md` is a byte-exact
    PREFIX of the post-C4 blob and the remainder is byte-equal to DECISION4.
    Report the remainder's full sha256 and line count, and confirm that
    `grep -c '^## DECISION F086 D' .agent/decisions.md` goes from 3 to 4.

G8  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/decisions.md` and `.agent/handoff.md` at HEAD each contain 0 lines
    beginning `<<<SLICE ` or `<<<END `. Count marker LINES, not `<<<`.

G9  NOTHING THIS ROUND TOUCHED CHANGED BEHAVIOUR, and the suites say so. In the
    PRIMARY checkout, serially, the second starting only after the first has
    ENDED: `python3 -m pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed; then
    `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.
    These four readers are the suites that PARSE the files this round rewrites, so
    they are the gate that can actually fail on a bad state text, not a formality.

G10 CHANGE SET. `git diff --name-only f0b27118..HEAD` before C5 is exactly the
    four paths of constraint 2 other than `.agent/handoff.md`. Confirm with `git
    ls-tree f0b27118 -- <path>` that every path constraint 2 FORBIDS exists at the
    base. Report both lists.

G11 HISTORY AND COMMIT SIZE. Every commit in `f0b27118..HEAD` has exactly one
    parent, the chain is linear, and `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, force-push. Report the chain and
    the INSERTION count for every commit BEFORE C5, one each; none over 500. C5's
    and C6's own go in the round report (§3 item 14).

G12 THE HANDBACK. `.agent/handoff.md` at HEAD is AT MOST 100 lines and carries all
    seven mandated headings of docs/agents/handback_template.md in the template's
    order. Report the `wc -l` reading and the heading list. If it exceeds 100,
    declare the DECISION D15 overage with its cause rather than dropping a
    section.

G13 THE VERDICT APPEND. The `.agent/handoff.md` blob committed by C5 is a
    byte-exact PREFIX of the file at HEAD and the remainder is byte-equal to the
    VERDICT slice. Report the remainder's full sha256 and line count.

G14 OPEN PR GATE, re-read at the handback: `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft`. Report its output. Create nothing,
    merge nothing.

Handback: your completion report with the FULL transcript, plus C5's rewrite of
`.agent/handoff.md` and C6's append, exactly as steps 6 and 7 specify.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN18>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs to
its closure round. `.agent/live_review.md` is the source of truth for the open set,
for the next free finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R18, this round: state files only. R17's repair of R-0584 is verified, so the
worker's `Landed:` line becomes the reviewer's `Done:` text, R17's verdict enters
the ledger, and DECISION F086 D4 rules where the install smoke executes — the one
design question left open by the fact that no round of this workflow can run it.

## Next Steps
1. R19 writes the install smoke per DECISION F086 D4: one `smoke`-marked,
   `slow`-marked module that SELF-SKIPS unless `REMEDY_INSTALL_SMOKE` is set, so
   the default suite stays fast and the test is honest about never having run
   here. What R19 can gate is the skip path and the module's own logic; what it
   cannot gate is the install, and it says so.
2. Then the smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a 300 s budget
   that AGENTS.md forbids raising by hand.
3. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN. It is gated as TEXT, the way
   `tests/orchestration/test_ci_workflow.py` gates `ci.yml`. No round can
   dispatch it; its first real run is a human action.

## Risks
- The install smoke needs network, a venv interpreter and minutes. MEASURED at
  R17: this session's permission layer refuses to execute an interpreter under
  `.remedy-wt/`, so a self-drive round can write that smoke but cannot run it.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN18>>>

<<<SLICE LANDEDFROM>>>
Landed: R-0584 — the three positive release-workflow guards now assert over `executable_lines()` instead of `workflow_text()`, so a comment can no longer satisfy them; committed as 3bedad72.
<<<END LANDEDFROM>>>

<<<SLICE DONE0584>>>
Done: R-0584 — RESOLVED at `3bedad72`, and the resolution is measured rather than accepted. `tests/orchestration/test_release_workflow.py` at `f0b27118` is the base blob with exactly three lines replaced — each FROM 1x before and 0x after, each TO 0x before and 1x after, ordered equality holding across the whole file at 70 lines — and each of the three positive guards now reads `any(<needle> in line for line in executable_lines())`, the comment-blind form the file's own negative guards already used. THE REVIEWER RE-RAN THE CONTROL AT THE COMMITTED HEAD rather than reading the handback: deleting the fallback in the single line `          echo "conclusion=${found:-missing}" >> "$GITHUB_OUTPUT"` in `.github/workflows/release.yml`, inside a disposable worktree at `f0b27118`, now yields exit 1 with 1 failed / 6 passed naming ONLY `test_release_workflow_refuses_when_no_ci_run_is_found`, where the SAME mutation at `4750383c` yielded exit 0 and 7 passed. That pair of readings — red where it was green, one commit apart, same mutation — is what makes this a repair and not a rewording. The second instance behaves the same way: commenting out the single line `  workflow_dispatch:` was green at `4750383c` and is red at `f0b27118`, naming only its own guard. The third guard, the tag check, was sound before and stays sound: it is red at both commits, so the change did not weaken it. `.github/workflows/release.yml` was NOT edited by the repair — the round's change set holds no workflow path — so the red proofs measure the guards and nothing else.
<<<END DONE0584>>>

<<<SLICE RECORD16>>>

Gate: R18 — the R17 entry. R17 PASSED, with NO finding. Every gate its block ordered was re-executed by the reviewer over `4750383c..f0b27118` rather than read from the handback, and every reading reproduces. THE REPAIR IS REAL AND THE REVIEWER PROVED IT ITSELF, which is the round's whole point: in a disposable worktree at `f0b27118`, deleting the fallback in the single line `          echo "conclusion=${found:-missing}" >> "$GITHUB_OUTPUT"` — counted 1x in `.github/workflows/release.yml` first — yields exit 1, 1 failed / 6 passed, naming ONLY `test_release_workflow_refuses_when_no_ci_run_is_found`, and the same mutation at `4750383c` yielded exit 0 and 7 passed when the reviewer ran it there before authoring the round. Red where it was green, one commit apart, same bytes mutated. THE THREE PAIRS LANDED AND NOTHING ELSE DID: each FROM occurs 1x at the base and 0x at HEAD, each TO 0x and then 1x, the file at HEAD is byte-equal to the base blob with those three occurrences replaced, `git show --numstat` reads 3 insertions and 3 deletions for that path, and the line count is unchanged at 70 — sha256 72db2e02767e95b8813c684ee5be5d63de4c43aaea2fcaf28101b39377d0b3bf. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original `.remedy-wt/f086-r17.md`, the committed `.agent/authored/f086-r17.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 5edb6fb56580f0060a3506944ce49969060bcc000335180f5d26418364d6c620, 29930 B over 414 lines, which is the size constraint 6 of that block declares of itself — 414 total, 294 prose, 120 slice including 20 marker lines. EVERY SLICE LANDED BYTE-EXACT: `.agent/plan.md` equals PLAN17 at 610d15f861e2b47a83e8b53a6c30ffa7f037e05506c5b6fcaff386a7e9b25c85 over 46 lines; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals FIND0584 followed by RECORD15 at c7ac0e52078092e599cd225db6dde0b9544e5f6933206c1127c37fcf26e97bc1; the post-C2 blob is a byte-exact PREFIX of the post-C4 blob whose remainder is a blank line plus exactly one `Landed: R-0584 — ` line, the single piece of worker-authored text the block permitted; and the C5 handoff blob is a byte-exact PREFIX of the file at HEAD whose 44-line remainder equals VERDICT at 2a1bc108f15ed103fe69534ff591dc120f32c6e210e2cb226eed1d9fcd01244d. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the four written files. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end, 166 registered / 2 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 164 open at `4750383c` and 167 / 2 / 0 / 0 / 1 / 165 at HEAD with the two registered SETS equal, the symmetric difference is exactly `['R-0584']`, and the reviewer's control over `6f5a589a..efc021d9` reads `['R-0583']`. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the PRIMARY checkout: 28 passed for the three release suites, 160 for the four state readers, 42 for the canary, each exit 0, and `ruff check` over the one touched Python path exits 0 with an EMPTY rule-code multiset at both ends of the range, compared as multisets rather than as exit codes. THE HYGIENE HELD: five paths over eight single-parent commits inserting 414, 259, 13, 4, 3, 2, 27 and 44 lines, none over 500 and no DECISION F104 D1 exemption invoked; `.github/workflows/release.yml`, `scripts/release_gate_check.py`, `packages/orchestration/release_gate.py`, `pyproject.toml`, `hatch_build.py`, `.github/workflows/ci.yml` and `CHANGELOG.md` are absent from the range and all seven exist at the base. THE HANDBACK IS EXACTLY AT ITS CAP: 100 lines against 100, all seven mandated headings in the template's order, no DECISION D15 overage — the fourth round running that the R-0582 repair has held.
<<<END RECORD16>>>

<<<SLICE DECISION4>>>

## DECISION F086 D4 — the install smoke is written here and executed elsewhere (2026-08-20)

CHOSEN. The T2_F086 install smoke is ONE module, `tests/test_install_smoke.py`,
carrying the `smoke` and `slow` markers, which SELF-SKIPS unless the environment
variable `REMEDY_INSTALL_SMOKE` is set. Its execution host is a machine with
network access and permission to spawn an interpreter it just installed — a
GitHub runner or the operator's own shell — and never a self-drive round.

MEASURED, at R17, which is why this is a decision and not a preference: this
session's permission layer refuses to execute an interpreter under `.remedy-wt/`,
so `python3 -m venv .remedy-wt/probe-venv` succeeds and the resulting
`.remedy-wt/probe-venv/bin/python` cannot be run. A wheel install also needs the
network to resolve `pydantic>=2.0` and `psutil>=5.9`, which `pyproject.toml`
declares. Neither constraint is a property of one round; both hold for every
round of this workflow.

WHY OPT-IN RATHER THAN A NEW CI STAGE. `tests/orchestration/test_ci_stages.py`
pins the stage tuple to `("fast", "standard", "ui", "smoke", "budgets",
"excluded")`, so a new stage is a change to that pin as well; and the existing
`smoke` stage already selects `smoke`-marked tests. The opt-in variable mirrors
what `real_ollama` already does for tests the default suite must not run, which
is the pattern this repository has and the reason the marker exists.

WHAT THIS DECISION DELIBERATELY DOES NOT RULE. It does not name the CI stage that
sets the variable. That choice needs the smoke's real wall-clock, and the `smoke`
stage carries a 300 s `timeout_sec` which AGENTS.md forbids raising by hand — a
budget is re-derived by the rule `tests/orchestration/test_ci_stages.py` states,
from a re-measured maximum. Choosing the stage before measuring the duration
would be exactly the blind raise that rule exists to prevent, so it waits.

CONSEQUENCE, stated plainly so no later reader mistakes a written test for a
passing one: until that variable is set somewhere real, F086's DONE condition —
"a wheel built from a clean checkout installs into a fresh virtualenv where the
golden path and the UI serve work" — is UNPROVEN. The closure round names it as
unproven rather than counting a skipped test as coverage.

ALTERNATIVE CONSIDERED and rejected: put the smoke in the release workflow
instead, as a step of `release.yml`. Rejected because that workflow is manual and
rarely dispatched, so a packaging regression would surface at release time, which
is the latest and most expensive moment to learn about it.

Reverse this decision by deleting this section, which reopens the choice between
an opt-in marker, a new CI stage, and a release-workflow step.
<<<END DECISION4>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming the branch at `4750383c`. The
reviewer wrote nothing in the work tree, one delegated worker per round made every
commit, and every verdict below rests on gates the reviewer re-executed over the
committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R16 | efc021d9..4750383c | PASS — one finding, R-0584, against the reviewer |
| R17 | 4750383c..f0b27118 | PASS — no finding |
| R18 | f0b27118..HEAD | verdict not yet on disk; see the last paragraph |

R16 was inherited ungated, so Phase 1 rule 4 reviewed it first. Its trigger is
real and it is manual, and every transport, ledger and suite reading its block
ordered reproduces. Its one defect was invisible to every gate it ordered and only
a control the block never ordered could find it: three of its seven guards
asserted a positive existence over text that INCLUDED the workflow's comments, and
two of those were satisfied by a comment alone — delete the fallback that keeps an
absent CI answer from reading green, or comment out the only trigger the workflow
has, and the suite stayed at 7 passed either way.

R17 repaired exactly that, and the repair is measured from both sides: the same
mutation that was green at `4750383c` is red at `f0b27118`, naming only its own
test, while the guard that was already sound stays red at both commits. R18 then
resolved R-0584 in the ledger and ruled DECISION F086 D4.

WHAT THIS FEATURE STILL OWES: the install smoke module per D4, then its wall-clock
measured on a host that can run it, then the CI opt-in, then the integration gate
and closure. NOTHING IN THIS SESSION PROVED AN INSTALL: no round of this workflow
can, which D4 records with the measurement behind it. The release workflow has
likewise never been dispatched.

R18 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last
verdict to be recorded. THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then
rule 2, then rule 4: review `f0b27118..HEAD` and record R18's verdict in
`.agent/live_review.md` as `Gate: R19 — the R18 entry`.
<<<END VERDICT>>>
