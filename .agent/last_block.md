── STEP T003 CLOSURE — F085 · R74 ──────────────────────────────────
Goal:        Close F085 per docs/roadmap/STATUS_closure_protocol.md: record R73's PASS, build the
             evidence job and a FRESH review zip from a clean tree at that record's commit, then land
             the reviewer-authored STATUS line, the README capability sync and the candidate carrier
             in one final commit, and open the PR the operator merges at the next Open PR Gate.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R73 PASS · THE EVIDENCE JOB · THE REVIEW ZIP · C3 the closure commit · THE PR.

Change:      exactly these paths and nothing else —
             `.agent/authored/f085-r74.md` (new, C0a)
             `.agent/last_block.md` (C0b, verbatim rewrite, AGENTS.md DECISION F104 D1 exempt)
             `.agent/plan.md` (C1, PLAN28F→PLAN28T — this is ALSO the plan's final state, so C3 does
                 not touch it again; the protocol's "final `.agent/` state" is satisfied by C1 for
                 this file and the block says so here rather than leaving you to discover it)
             `.agent/live_review.md` (C2, RECORD43 appended at EOF)
             `docs/roadmap/STATUS.md` (C3, STATUSF→STATUST)
             `README.md` (C3, READMECOUNTF→READMECOUNTT, READMETIERF→READMETIERT, READMEDOCF→READMEDOCT)
             `.agent/candidates.md` (C3, CANDIDATES — whole-file replacement)
             `.agent/handoff.md` (C3)
             The evidence directory is NEVER committed and never enters the review subject.
             `.agent/context.md` and `.agent/decisions.md` are deliberately untouched.

CONVENTION, binding on every count and proof here, carried verbatim in force from the R73 block. A
line count is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES
STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT
LINE: extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so `pre + slice` is already newline-terminated and NO joiner and
NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN28, STATUS, READMECOUNT,
READMETIER AND READMEDOC. ITS END-OF-FILE APPEND, WHICH HAS NO FROM, IS RECORD43. ITS WHOLE-FILE
REPLACEMENT IS CANDIDATES. PRBODY IS NOT APPLIED TO ANY FILE — it is the PR description.

PAIR SHAPES, one containment reading per pair, each produced mechanically by the reviewer before
emission and reported here as the test's own output:
  PLAN28       `TO contains FROM: false`  → REWRITE. Order FROM 1x pre / 0x post, TO 1x post.
  STATUS       `TO contains FROM: false`  → REWRITE. Same three readings.
  READMECOUNT  `TO contains FROM: false`  → REWRITE. Same three readings.
  READMETIER   `TO contains FROM: false`  → REWRITE. Same three readings.
  READMEDOC    `TO contains FROM: true`   → APPEND-shaped. Take NO FROM-zero count: it is
               unattainable by construction. The obligation is FROM exactly 1x in the post-commit
               file plus each TO-ONLY line exactly 1x AMONG THE LINES C3's DIFF ADDS to `README.md`.
Each FROM string occurs exactly ONCE in its target at ed34119b — the reviewer counted all five.

Constraints:
 1. Apply every slice BYTE-VERBATIM, extracted programmatically from the committed
    `.agent/authored/f085-r74.md` by marker pair under the CONVENTION. Edit no slice. The ONLY
    substitutions permitted anywhere are the three slots `<<ZIP>>`, `<<SHA256>>` and `<<HEAD40>>` in
    STATUST, one occurrence each, filled from the measured values named under THE REVIEW ZIP below.
 2. Re-read `.agent/STOP` from disk immediately before C0a and again immediately before C3. If it
    exists at either point, finish only the commit in flight, write the handback, and stop.
 3. Commit in exactly the order C0a, C0b, C1, C2, C3. C1 advances the plan before the ledger commit
    (docs/agents/planner_reviewer_prompt.md §3 checklist item 23). C3 is the LAST commit on the
    branch (Rule A4) and carries the STATUS edit.
 4. `git status --porcelain` is EMPTY after every commit AND immediately before the zip build — a
    package built from a dirty tree is invalid. Any destructive check runs only in a disposable
    worktree under `.remedy-wt/`, removed and pruned before the handback.
 5. Never force-push. Never merge. CREATE the PR, do not merge it: it merges at the next feature's
    Open PR Gate, which is the operator's manual-review window.
 6. Run every suite command in the PRIMARY checkout and SERIALLY, one pytest process at a time.
 7. If the evidence job or the zip build FAILS, that is a closure BLOCKER: record the full raw
    stdout+stderr in `.agent/handoff.md`, do NOT commit C3, do NOT create the PR, and hand back. A
    closure without a package does not happen.
 8. REPORT DISAGREEMENT, DO NOT FIX IT. If any number, path, quotation or claim here contradicts what
    you measure, record BOTH readings in the handback and change no slice.
 9. Author no `Done:` and no `Gate:` text of your own. Those are reviewer-authored strings.

## THE EVIDENCE JOB — after C2, from a clean tree

Build the bundle through the CANONICAL producer; `write_runtime_integration_gate` alone is NOT a
bundle and packages as BLOCKED_EVIDENCE:

    from packages.orchestration.job_evidence import create_manual_completion_bundle

Its arguments are keyword-only after the first. Call it with
`evidence_dir="remedy-job-evidence-f085-closure"`, `repo_root` the absolute repository path,
`base_commit="a5a706214d20101dd54564c23d0a3c22efcc705d"` in full 40-character form,
`job_id="f085-closure"`, `job_title="F085 Sandbox hardening stage 1 closure"`,
`step_range="T001-T003"`, `prior_job_ids=[]`, `head_commit` the C2 commit SHA in full 40-character
form, `review_feature_id="f085"`, and `timestamp`/`generated_at` as ISO-8601 Z strings. Inspect the
real signature first and report any parameter this block names that it does not accept.

`verification_runs` is what has blocked several previous closures, so BUILD IT FROM A REAL RUN rather
than typing values. The record covers F085's OWN two new test files — the full-suite proof rides in
the committed `.agent/gate_f085_r72/` evidence and in the reviewer's own re-runs, never here, because
`len(node_ids) == selected` forbids filtering and a full-suite id list is rejected by the packaging
metadata scan. The `test_files` list is these two paths and it MUST be sorted, and they are FILES and
never a directory — an unsorted list packages as BLOCKED_EVIDENCE:

    tests/orchestration/test_claude_cli_exec_guard.py
    tests/orchestration/test_exec_guard.py

Take the ids from `python3 -m pytest <those two files> --collect-only -q` and the counts from running
the same two files. The reviewer ran both at ed34119b and measured 57 collected node ids and
`57 passed`, exit 0. Write ONE record with `run_id="vr-0001"` — the regex is `^vr-\d{4,}$`, and a
rejected VerificationTests document yields `vt_passed = None`, which fails the final-verifier
confirmation. Carry the exact `command`, the real `exit_code`, `passed`, `failed`, `skipped`,
`selected`, `node_ids` with `len(node_ids) == selected`, `test_files` as the two files above,
`head_sha` the C2 head, a `stdout_summary`, and `output_hash` as the sha256 hex of that
`stdout_summary` string EXACTLY — a digest of anything else packages as BLOCKED_EVIDENCE.

Record `Evidence job f085-closure` and the bundle's own status in the handback.

## THE REVIEW ZIP — still after C2, still from a clean tree, MANDATORY

    git status --porcelain          # must be EMPTY
    git push
    bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f085-closure

Record the printed filename and its SHA-256, and confirm the manifest's `committed_review_subject`
head_commit equals the C2 commit. Those three values fill STATUST's slots: `<<ZIP>>` is the package
filename, `<<SHA256>>` is the printed SHA-256, and `<<HEAD40>>` is that head_commit in full
40-character form. A failing build is constraint 7. Expect a large archive: the gitignored
`.remedy-wt/` scratch is packaged too, which is registered finding R-0403 and routed to a paydown
branch — it is not a defect of this round.

## THE PR — after C3, last action of the round

    git push
    gh pr create --base main --head feature/f085-sandbox-hardening --title "F085 — Sandbox hardening (stage 1)" --body-file <a file holding the PRBODY slice with its slots filled>

Fill PRBODY's `<<ZIP>>`, `<<SHA256>>` and `<<HEAD40>>` from the same measured values as STATUST, and
its `<<COMMITS>>` slot with the count of commits in `main..HEAD`. Write the body file under the
gitignored `.remedy-wt/` and never into the repository tree. Report the PR number and URL. Do not
merge it.

Done when — run each gate, record its REAL exit code and real output, never a colour you did not see:

 G1 STATE. `.agent/STOP` absent at the two points constraint 2 names. `git status --porcelain` empty
    after every commit and immediately before the zip build. `git worktree list` one line at the start
    and at the end.
 G2 TRANSPORT. After C0b, sha256 over all four of the committed `.agent/authored/f085-r74.md`, the
    committed `.agent/last_block.md` and both working copies — all four MUST be equal. Report the
    digest, byte size, line count, and the count of lines beginning `BEGIN-` or `END-`, noting that
    the CONVENTION paragraph contains one prose line beginning `END-OF-FILE` which is not a marker.
    Budget: TOTAL is the line count and must be ≤ 490 (DECISION F085 D6); PROSE is TOTAL minus the sum
    of the slices' line counts and must be ≤ 400 (DECISION F085 D5). Report every slice's measured
    line count and sha256.
 G3 SHAPES, one reading per unit, each against that commit's OWN pre-commit blob, using the PAIR
    SHAPES table above and taking no reading that table forbids. For the four REWRITE pairs report
    FROM occurrences pre and post, TO occurrences post, and byte-exact reproduction of the post blob
    by re-applying FROM→TO. For READMEDOC report FROM 1x post plus each TO-ONLY line exactly 1x among
    C3's ADDED lines for `README.md`. For RECORD43 report ORDERED EQUALITY: pre is a byte-exact
    PREFIX, the slice an exact SUFFIX, `pre + slice == post`, and C2's ADDED lines equal the slice's
    lines IN ORDER. For CANDIDATES report that the post-commit file equals the slice byte for byte.
    Report `git show --numstat` for C1, C2 and C3. Report the count of lines beginning `BEGIN-` or
    `END-` in every edited target file at C3 — each must be 0.
 G4 FULL SUITE at the C2 commit, the closure re-confirmation precondition 2 requires, in the primary
    checkout: `python3 -m pytest -n auto -q`. Report exit code, wall time and the summary line. The
    reviewer ran this four times at d6d96e50 and saw `17132 passed, 19 skipped` three times and, once,
    a single red on
    `tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_every_outcome`, which
    passes serially and is registered as R-0569, the xdist-flake class
    docs/agents/integration_gate.md step 4 records rather than blocks. If YOUR run reds on that id,
    re-run that id serially, report both readings, and continue. Any OTHER red is constraint 7.
 G5 DOCS GATES after C3, serially: `python3 -m pytest tests/docs/ -q -rf` and
    `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`. This round edits
    `docs/roadmap/STATUS.md` and `README.md`, and both suites read those files — `tests/docs/` pins
    the README accepted-count and tier table against the ledger and link-checks the README, while the
    roadmap index parses the STATUS grammar. The reviewer measured `295 passed` and `30 passed` at
    ed34119b before ordering them.
 G6 STATE READERS after C2, serially, the four files `.agent/context.md` names:
    `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    The reviewer measured exit 0, `160 passed` at ed34119b.
 G7 INTEGRITY, precondition 3. The `remedy integrity check --json` entry point is DENIED in this
    sandbox, so call the SAME functions that CLI command calls — `run_integrity_checks()` and
    `summarize_integrity()` from `packages.orchestration.integrity_gate`, which
    `apps/cli/commands/integrity_cmd.py` invokes — and report the full summary. State in the handback
    that the module path was used because the CLI entry point is unavailable, so the substitution is
    visible in the record rather than hidden. The reviewer ran it at ed34119b and saw
    `Status: PASS (0 failures)` over five checks. It MUST pass; a failure is constraint 7.
 G8 PLAN CONTRACT at C1: `.agent/plan.md` line count ≤ 50, with `## Goal`, `## Next Steps` and a
    string matching `\bF\d{3}\b` present.
 G9 ARITHMETIC under DECISION F085 D7, OPEN = REGISTERED − DONE, a `Landed:` line never subtracted.
    Report both operands and OPEN at ed34119b and at C3, the symmetric differences, duplicate ids,
    resolutions naming an unregistered id, max registered and max resolved at each SHA, and the next
    free id. The reviewer measured the base itself: 184 registered, 32 done, OPEN 152.
G10 CANARY, serially: `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer saw exit 0,
    `42 passed` at ed34119b.
G11 HYGIENE. Report `git diff --name-only ed34119b..C3` in full — every path must be one this block's
    Change set names, none may end `.log`, and no evidence directory or zip may appear. Report each
    commit's insertion count (C3's own belongs in the round report, not in a gate) and confirm every
    commit is single-parent.
G12 GREP PROOF, which the closure protocol item 5 requires: show that the applied STATUS line and the
    applied README lines are byte-identical to their authored slices apart from the three filled
    slots, and that the applied `.agent/candidates.md` is byte-identical to CANDIDATES.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md inside C3 — feature and
round, branch, base SHA ed34119b, per-commit changed-files tables, the item-status table covering
C0a, C0b, C1, C2 and C3 exactly once each, the real results of G1 through G12, the evidence job id and
the bundle status, the package filename and SHA-256 and the accepted HEAD, the PR number and URL, the
authored-text proofs, external actions, deviations, the open-findings count and the next expected
action. Every artifact-build attempt appears with its status, including any failure with its blocking
reason. Exceed the 60-line cap only for MANDATED content and then carry a "Deviations, declared" line
naming the actual count and the cause. Never drop a section.

The handback's state block repeats this Fortschritt line verbatim, label included:

Fortschritt: 100 % — F085 ist gebaut, gegengeprüft und wird in dieser Runde geschlossen. T001 bis
T003 stehen, das Integration Gate hält, der Reviewer hat die volle Suite selbst viermal gefahren, und
was nicht geliefert wurde — die `resource_limit`-Klasse in der F010-Taxonomie — steht als R-0568
offen im Protokoll statt in einer Behauptung. Offen bleibt nur der Merge, den der Operator am
nächsten Open PR Gate zieht. Schätzung, gemessen gegen die Klassentabelle aus Amendment F085 D1.

Next expected action for the reviewer: gate this round, issue the closing verdict into the handoff and
the PR — the last round of a branch records its verdict there and not in `.agent/live_review.md`, per
docs/agents/planner_reviewer_prompt.md §4 item 13 — and end the session.
────────────────────────────────────────────────────────────────────

BEGIN-PLAN28F
## Current Step
R73, this round: R72's verdict recorded, the findings its gate produced registered, and the feature
file's Built State written — so the closure round that follows touches only the paths
docs/roadmap/STATUS_closure_protocol.md item 5 allows. R72 PASSED: its transport, its slice shapes,
its arithmetic and its integration gate were re-taken by the reviewer rather than read, and the
branch-side full-suite failure the reviewer's own repeated runs produced passes serially, which
docs/agents/integration_gate.md step 4 classifies as the xdist-flake class to record and not to block.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line and the README capability sync authored by the reviewer, and the PR the operator merges at
   the next Open PR Gate.
2. R-0567, R-0568 and R-0569 close as documented risks in that closure under precondition 1 of that
   protocol, rather than by a repair round inside this feature.
END-PLAN28F
BEGIN-PLAN28T
## Current Step
R74, the closure round per docs/roadmap/STATUS_closure_protocol.md: R73's PASS recorded, then the
evidence job and a FRESH review zip built from a clean tree at that record's commit, then one closure
commit carrying the reviewer-authored STATUS line, the README capability sync and the candidate
carrier, then the PR. R73 PASSED — its transport, both slice shapes, the arithmetic and all four of
its gate suites were re-run by the reviewer rather than read from the handback.

## Next Steps
1. The operator merges the closure PR at the next feature's Open PR Gate; this session merges nothing.
2. The next session claims the next feature by Rule A5, and its FIRST reviewed round empties
   `.agent/candidates.md` by registering or resolving every entry that file holds.
END-PLAN28T
BEGIN-RECORD43

Gate: R74 — the R73 entry. R73 PASSED. Every gate its block ordered was re-taken by the reviewer over
d6d96e50..ed34119b rather than read from the handback, except the absence of `.agent/STOP` at the two
points R73's constraint 2 names and `git status --porcelain` after each intermediate commit, which are
unobservable once a round has ended and are accepted on the worker's report. TRANSPORT HELD,
disk-to-disk under the digest fallback of docs/agents/planner_reviewer_prompt.md §4 item 9: the
committed `.agent/authored/f085-r73.md`, the committed `.agent/last_block.md` and both working copies,
all read at ed34119b, are byte-EQUAL at sha256
5fd5b62c53488cd9386701ac8d3781aac6914d15ccbbf4b78a7f3fec34cc8b12, 24180 B, 293 lines. TOTAL 293
against the 490 cap; the four slices measure 11, 14, 93 and 32 lines, so PROSE is 143 against 400. Of
the nine lines beginning `BEGIN-` or `END-`, eight are the four slices' markers and the ninth is a
CONVENTION prose line beginning `END-OF-FILE`; the R73 worker reported both readings rather than
reconciling them, which is what constraint 8 asks for and the third round in this feature it has
produced a correct disclosure. THE SHAPES HELD: PLAN27F→PLAN27T over `.agent/plan.md` at 319060db
reads `TO contains FROM: false`, shows FROM 1x pre-commit and 0x post-commit with TO exactly 1x
post-commit, and reproduces its post-commit blob BYTE-EXACTLY on re-application. RECORD42 at 1961e5cc
and BUILTSTATE at e461e9c4 each satisfy ORDERED EQUALITY against their own pre-commit blob — PREFIX,
SUFFIX and `pre + slice` equal byte for byte. All four slice digests recomputed by the reviewer agree
with the handback. Marker LINES are 0 in all three edited files at e461e9c4. THE SUITES WERE RE-RUN,
NOT READ, in the primary checkout, serially, each exit 0 and each equal to the reading the reviewer
had taken at the base d6d96e50 before ordering it: `295 passed` for `tests/docs/`, `30 passed` for
`tests/orchestration/test_roadmap_index.py`, `160 passed` for the four state readers, and the canary
`42 passed`. The docs gate ran in BOTH halves because `tests/docs/` asserts nothing about a feature
file's BODY — finding R-0493 proved that by red control — so the roadmap-index half is what actually
reads the file C3 edited. The reviewer also pre-applied PLAN27T and BUILTSTATE inside a throwaway
worktree at d6d96e50 before emitting the block and measured `325 passed` for the two halves together,
so the ordered colour had been observed on the edited tree and not only on the base. THE ARITHMETIC
HELD under DECISION F085 D7: 181 registered / 32 done at d6d96e50 and 184 / 32 at e461e9c4, so OPEN
moves 149 to 152; the registered symmetric difference is exactly {R-0567, R-0568, R-0569}, the done
symmetric difference is empty, and there are 0 duplicate ids and 0 resolutions naming an unregistered
id at both SHAs. THE PLAN CONTRACT HELD at 319060db: 41 lines against the 50-line cap with `## Goal`,
`## Next Steps` and a roadmap F-id present. THE HYGIENE HELD: the range touches the six paths the
block named and no other, none under `packages/`, `apps/`, `scripts/` or `tests/` and none ending
`.log`, over six single-parent commits inserting 293, 279, 10, 93, 32 and 47 lines, none over 500.
THE BUILT STATE IS THEREFORE CURRENT, which is precondition 4 of
docs/roadmap/STATUS_closure_protocol.md and the reason this closure round can follow immediately.
END-RECORD43
BEGIN-STATUSF
- [~] F085 — Sandbox hardening (stage 1)
END-STATUSF
BEGIN-STATUST
- [x] F085 — Sandbox hardening (stage 1) (T001–T003 complete; accepted 2026-08-19 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f085-closure · package <<ZIP>> · SHA-256 <<SHA256>> · accepted HEAD <<HEAD40>>)
END-STATUST
BEGIN-READMECOUNTF
50 of 255 registered items accepted. Next: F085 (Sandbox hardening, stage 1).
END-READMECOUNTF
BEGIN-READMECOUNTT
51 of 255 registered items accepted. Next: F086 (Release capability).
END-READMECOUNTT
BEGIN-READMETIERF
| 2 | Minimal Self-Build Runtime | 12 | 14 |
END-READMETIERF
BEGIN-READMETIERT
| 2 | Minimal Self-Build Runtime | 13 | 14 |
END-READMETIERT
BEGIN-READMEDOCF
| Step history (archive) | [`docs/archive/remedy-step-history-v0.md`](docs/archive/remedy-step-history-v0.md) |
END-READMEDOCF
BEGIN-READMEDOCT
| Step history (archive) | [`docs/archive/remedy-step-history-v0.md`](docs/archive/remedy-step-history-v0.md) |
| Execution guard limits (F085) | [`docs/system/exec-guard-limitations-v0.md`](docs/system/exec-guard-limitations-v0.md) |
END-READMEDOCT
BEGIN-CANDIDATES
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

F085's rounds raised no candidate of their own: everything its reviews found was
registered as an R-id in `.agent/live_review.md` while the round that found it was
still open, which is where a finding belongs. The three the closure-prep round
registered — R-0567, R-0568 and R-0569 — are findings and not candidates, and they
close as documented risks under precondition 1 rather than riding here.

One candidate, raised by the reviewer's closure review of R74 · source F085 ·
2026-08-19. The root `README.md` names five accepted Tier 2 features in its
"Accepted in Tier 2 so far" list while its own tier table records thirteen, and
nothing catches the gap: `test_the_readme_reports_the_accepted_foundation_and_no_later_feature`
in `tests/docs/test_docs_consistency.py` checks only that every feature the README
LISTS is accepted in the ledger, never the converse, so an incomplete list passes.
The count pin and the tier-table pin are both one-directional in the same way. This
is not F085's defect — the same list was already incomplete when F082 and F083
closed, neither of which added itself — which is exactly why it needs a carrier
rather than a repair inside this feature.

If the reviewer's gate of this round raises a further candidate after this file is
committed, that candidate rides in the round report and in `.agent/handoff.md`, and
the next feature's first reviewed round registers it — the path F082's three
closure candidates took to become R-0448, R-0449 and R-0450 at F083 R1.
END-CANDIDATES
BEGIN-PRBODY
## What changed

F085 Sandbox hardening, stage 1: builder-, test-, DoD- and runtime-spawned subprocesses stop relying
on prompted discipline. A new `packages/orchestration/exec_guard.py` carries POSIX resource limits, a
wall timeout the guard supervises itself, output-size caps, a cwd pinned inside the worktree and an
environment allowlist, with a default-deny network posture for the classes that must not reach the
network. Twenty-four call sites across the four stage-1 classes were migrated to it, each behind
behaviour-equality tests. `docs/system/exec-guard-limitations-v0.md` says exactly what stage 1 does
NOT prevent and is linked from both the doc index and this repository's README.

## Why

Fences already stop the applicator from writing outside scope; nothing bounded what the commands
Remedy spawns could do. Stage 1 raises the bar with POSIX mechanisms and documents honestly that a
hostile binary can still ignore a proxy — container-grade isolation is a later feature and is never
claimed here.

## Key decisions

Amendment F085 D1 replaced the feature file's "small number of helpers" premise with the measured
seam shape: 67 real subprocess call sites, of which the four named classes hold 24. Amendments D7 and
D8 then split the `dod` and `runtime` rows, because neither class was policy-homogeneous — a bounded
child keeps its wall timeout even when its class serves a long-lived purpose. DECISION F085 D5 and D6
re-budgeted the step block so a round could carry code again, and D7 fixed the open-findings count as
REGISTERED minus DONE, with a `Landed:` line never subtracted.

## How to review

Start at `docs/roadmap/features/T2_F085.md` — the policy table and the Built State section. Then
`packages/orchestration/exec_guard.py` and its tests. The full review record is
`.agent/live_review.md`; the integration gate evidence is `.agent/gate_f085_r72/`.

## Verification

Full suite, `python3 -m pytest -n auto -q`, run by the reviewer four times: three clean at
`17132 passed, 19 skipped` and one with a single red on a fixed-port product-smoke assertion that
passes serially and is registered as R-0569. Integration gate: 0 branch-only failures, all five
base-only failures attributed per id to a stale `apps/ui/dist` in the throwaway base worktree.
Integrity gate PASS over five checks.

## State

Latest verdict PASS_WITH_RISKS. Open findings 152, none High or blocking; R-0568 — the guard's
`resource_limit` classification not reaching the F010 postmortem taxonomy — is the one that touches
this feature's own scope and is documented rather than claimed fixed. Evidence job f085-closure ·
package <<ZIP>> · SHA-256 <<SHA256>> · accepted HEAD <<HEAD40>> · <<COMMITS>> commits.

Not to be merged by an agent: this PR merges at the next feature's Open PR Gate, which is the
operator's manual-review window.
END-PRBODY
