# F083 R28 — CLOSURE

SPLIT round. It records the R27 verdict, then runs the closure algorithm of
`docs/roadmap/STATUS_closure_protocol.md`: the evidence job, a FRESH review zip,
the STATUS line, the README capability sync, the candidates carrier and the PR.
It changes no code and no test.

Base: `git rev-parse HEAD` MUST print 74063862 before the first commit. If it does
not, stop and report. The merge base, needed by the evidence job in FULL 40-char
form, is f3fd96d729c3be85604a2d37aee42c59fe39868a.

## Commit order, and where the uncommitted work sits

**C0a** copies `.remedy-wt/f083-r28.md` to `.agent/authored/f083-r28.md`. **C0b**
mirrors the COMMITTED copy over `.agent/last_block.md`.

**C1** applies RECORD-R27 as an EOF-append to `.agent/live_review.md`, the only
file in that commit.

**C2** applies PLAN. **C2 IS THE LAST CONTENT COMMIT — its head is the ACCEPTED
HEAD that the zip manifest and the STATUS line both record.**

— the evidence job and the review zip run HERE, against the C2 head, from a clean
tree. NEITHER IS COMMITTED. —

**C3** is the CLOSURE COMMIT and the LAST commit on this branch (Rule A4):
`docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md` and
`.agent/handoff.md`. Exactly those four paths (R-0154), nothing else.

— then `gh pr create`. The PR is NOT merged this session (protocol step 6). —

The ordered sequence is exactly C0a, C0b, C1, C2, C3 — five commits, no gaps and
no spare numbers.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The authored units carried
here are, listed: two EOF-or-whole-file writes named RECORD-R27 and PLAN, one
more whole-file write named CANDIDATES, and three REWRITE pairs whose FROM and TO
are disjoint, named STATUSLINE, READMECOUNT and READMETIER. No numeral is stated
for that list — the list IS the statement. Extract every slice programmatically
from the COMMITTED `.agent/authored/f083-r28.md` by its markers, never by
retyping.

The three REWRITE pairs carry a SECOND begin marker instead of a second end
marker, so read them by this rule and not by the general one above: a pair's FROM
body runs from the line AFTER `--- BEGIN SLICE <NAME> ---` to the line BEFORE
`--- BEGIN SLICE <NAME>-TO ---`, and its TO body from the line AFTER
`--- BEGIN SLICE <NAME>-TO ---` to the line BEFORE `--- END SLICE <NAME>-TO ---`.
Both bodies include the trailing newline of their last line. Each of the three
pairs is a single line of FROM and a single line of TO.

THE STATUS LINE IS THE ONE SLICE THAT CANNOT BE FULLY AUTHORED. It carries three
values that do not exist when this block is written — the zip filename, its
SHA-256 and the accepted HEAD — and ordering a value that cannot yet exist is
exactly R-0371. So STATUSLINE-TO carries three literal placeholder tokens,
`<<ZIP>>`, `<<SHA256>>` and `<<HEAD40>>`, and the worker substitutes ONLY those
three, each exactly once, with the measured value. Everything else in that line
is byte-verbatim, and gate 9 proves it by substituting the measured values back
out again. Leaving a `<<` token behind, or changing any other character, is a
failure of the round.

Shell note: this session rejects `$( )`, `${...}` and shell loops by form. Route
anything of that shape through `python3 - <<'PY'` and read every exit code from
the process object, never from `$?`.

--- BEGIN SLICE RECORD-R27 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R27 — PASS. All sixteen ordered gates reproduce at the reviewer's own hand from the repository root at 74063862, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN original bytes and NOT by digest fallback (§4.9): `.remedy-wt/f083-r27.md`, the committed `.agent/authored/f083-r27.md` and the committed `.agent/last_block.md` are all byte-IDENTICAL at sha256 369d9a4e1773dea61dc7b13c414e2d1f5c524112b482b9eecb12ecc0db398c9c over 24166 bytes and 284 lines, under the 400-line cap. THE CHECKLIST PAIR WAS SETTLED BY ONE EQUALITY RATHER THAN BY COUNTS: `pre.replace(FROM, TO, 1) == post` measured True over `docs/agents/planner_reviewer_prompt.md`, which no partially-correct edit can satisfy; the FROM occurred 1x before and 1x after — inside the TO, the declared APPEND shape — the TO 0x before and 1x after, and the file holds 0 marker lines and 0 bare FROM:/TO: label lines. Both appends are pure: `docs/roadmap/features/T2_F083.md` goes 5064 B to 8757 B with the former a prefix of the latter and the 3693-byte tail byte-EQUAL to the BUILTSTATE slice at numstat `58 0`, `## Built State` 0x before and 1x after; `.agent/live_review.md` goes 308606 B to 315460 B with the same prefix property, its tail byte-EQUAL to the RECORD-R26 slice at numstat `5 0`, and its transport marker LINE count 0 at base and 0 at HEAD while the bare substring count is 4 at both. `.agent/plan.md` byte-EQUALS the PLAN slice at sha256 dc58b598b1eb72bc6944e7f59931a125dfd91a6925ce30866831a5e4621310e8, 41 lines under the 50-line cap, `## Goal` and `## Next Steps` present, 0 unchecked-box lines. THE BUILT STATE'S CLAIMS WERE CHECKED AGAINST THE CODE, NOT ACCEPTED AS PROSE: the reviewer imported the stage table and summed it, getting 3900 s against the workflow's 5400 s job cap so the "cap sits above the sum" sentence holds; the six stage names are exactly `fast`, `standard`, `ui`, `smoke`, `budgets` and `excluded`; and `LINT_ERROR_CEILING` is 26, the number the section calls a ratchet. The run gates reproduce: `tests/docs/` 295 passed at exit 0, the canary 42 passed at exit 0, the stage-table, workflow-guard and CLI-seam suites 22 passed at exit 0, and ruff `Found 26 errors.` with `[*] 25 fixable` at exit 1 — the ratchet held, and the only path C4 changed before HEAD is `.agent/handoff.md`, so the reading is invariant across the commit it was taken at. The restrictions hold as restrictions: the range over `packages/ apps/ scripts/ tests/ .github/` is EMPTY, the range over `docs/` is exactly `docs/agents/planner_reviewer_prompt.md` and `docs/roadmap/features/T2_F083.md`, and `docs/roadmap/STATUS.md` and `README.md` are each ABSENT from the whole range — which is what keeps the closure commit's own path set available. The open set recomputes to 117 registered, 13 resolved, 0 landed and 104 open, max R-0489 and next free R-0490, 0 duplicate ids and 0 resolutions naming an unregistered id, with R-0489 both registered and resolved and R-0482 and R-0487 still open. Per-commit insertions are 284, 212, 13, 58, 5, 16 and 99, none near 500; the range holds seven single-parent commits chained to ceb46a23; the reflog shows only `commit:` entries. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly, and C1 landed before C3 as ordered, so C3's claim that checklist item 14 is on disk was true at the moment it was committed. R-0489 IS RESOLVED AND THE FIX IS ALREADY WORKING. The finding was that a per-commit gate cannot reach the handback commit, so the R26 handoff reported five insertion counts beside a sentence calling a six-commit range "five single-parent commits". This round's handoff says "six commits in the range when read" and routes C5's own count to the round report, where it was measured at 99 — the same shape the R26 handoff got wrong, now right, one round after the rule was written down. That is the R-0460/R-0461 precedent honoured rather than cited: the block that asserted the promotion also performed it, in a commit that landed before the record claiming it. Three declared deviations, all honest, none a defect. The tooling substitution is correct in kind: `cp` is denied in this session, so C0a copied through `shutil.copyfile` and the worker measured the PROPERTY the gate names — byte equality of the committed blobs plus the shared sha256 — rather than reporting the tool. The stated-cause overage is honest under DECISION D15: the handoff is 136 lines against a cap that allows 100 for tables of more than five commits, the cause named is mandated content — seven per-commit tables and a sixteen-row item-status table — and the reviewer read the file and found no prose padding, no verbatim transcript and no restated procedure in it. It is over the cap and says so, which is the behaviour the rule asks for.
--- END SLICE RECORD-R27 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C2)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. `.agent/live_review.md` is the source of truth for the open set and for
the next free finding id; this file repeats neither.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R27 is closed PASS. R28 is the CLOSURE round per
docs/roadmap/STATUS_closure_protocol.md: it records that verdict, then runs the
evidence job and a fresh review zip against this commit, writes the STATUS `[x]`
line together with the README capability sync in one commit, and opens the PR.
T001, T002 and T003 are COMPLETE, the integration gate passed at R26 with 0
branch-only and 0 base-only failures, and the feature file's Built State landed
at R27.

## Next Steps
1. The PR is NOT merged this session. It merges at the next feature's start via
   the AGENTS.md Open PR Gate; the gap is the operator's manual-review window.
2. A paydown branch for R-0482 and R-0487, which this feature deliberately did
   not fix.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the toolchain-dependent tests.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 (a live `NameError` on a guard's refusal path) and R-0487
  (`docs/README.md` is never link-checked) are both frozen here: each is a code-
  or test-content fix this feature may not make.
--- END SLICE PLAN ---
--- BEGIN SLICE CANDIDATES --- (WHOLE FILE, replaces .agent/candidates.md, C3)
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

The carrier is empty at the time F083's closure block was authored. F083 raised no
closure candidate of its own during its rounds: everything it found was registered
as an R-id in `.agent/live_review.md` while the round that found it was still open,
which is where a finding belongs.

Two open findings are deliberately deferred rather than carried here, because they
are registered findings and not candidates: R-0482, a live `NameError` on the
refusal path of `check_injections_supported`, and R-0487, `docs/README.md` never
being link-checked. Both are code- or test-content fixes that F083's scope
forbids, and both want a paydown branch of their own.

If the reviewer's closure review of this round raises a candidate after this file
is committed, that candidate rides in the round report and in `.agent/handoff.md`,
and the next feature's first reviewed round registers it — the same path F082's
three closure candidates took to become R-0448, R-0449 and R-0450 at F083 R1.
--- END SLICE CANDIDATES ---
--- BEGIN SLICE STATUSLINE --- (in docs/roadmap/STATUS.md, C3 — REWRITE pair, FROM and TO disjoint)
- [~] F083 — CI self-check
--- BEGIN SLICE STATUSLINE-TO --- (C3 — substitute ONLY <<ZIP>>, <<SHA256>> and <<HEAD40>>, one occurrence each)
- [x] F083 — CI self-check (T001–T003 complete; accepted 2026-08-16 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f083-closure · package <<ZIP>> · SHA-256 <<SHA256>> · accepted HEAD <<HEAD40>>)
--- END SLICE STATUSLINE-TO ---
--- BEGIN SLICE READMECOUNT --- (in README.md, C3 — REWRITE pair, FROM and TO disjoint)
49 of 255 registered items accepted. Next: F083 (CI self-check).
--- BEGIN SLICE READMECOUNT-TO --- (C3)
50 of 255 registered items accepted. Next: F085 (Sandbox hardening, stage 1).
--- END SLICE READMECOUNT-TO ---
--- BEGIN SLICE READMETIER --- (in README.md, C3 — REWRITE pair, FROM and TO disjoint)
| 2 | Minimal Self-Build Runtime | 11 | 14 |
--- BEGIN SLICE READMETIER-TO --- (C3)
| 2 | Minimal Self-Build Runtime | 12 | 14 |
--- END SLICE READMETIER-TO ---

## THE EVIDENCE JOB, between C2 and C3, from a clean tree

Build the bundle through the CANONICAL producer — `write_runtime_integration_gate`
alone is NOT a bundle and packages as BLOCKED_EVIDENCE:

```
from packages.orchestration.job_evidence import create_manual_completion_bundle
```

Its signature is keyword-only after the first argument; call it with
`evidence_dir="remedy-job-evidence-f083-closure"`, `repo_root` the absolute repo
path, `base_commit="f3fd96d729c3be85604a2d37aee42c59fe39868a"` in full 40-char
form, `job_id="f083-closure"`, `job_title="F083 CI self-check closure"`,
`step_range="T001-T003"`, `prior_job_ids=[]`, `head_commit` the C2 head,
`review_feature_id="f083"`, and `timestamp`/`generated_at` as ISO-8601 Z strings.

`verification_runs` is the part that has blocked several previous closures, so
BUILD IT FROM A REAL RUN rather than typing values. Use F083's own scoped suite,
which the reviewer ran at emission and measured at 121 passed, 121 collected,
exit 0. The `test_files` list is these SEVEN paths, and it must be SORTED — an
unsorted list packages as BLOCKED_EVIDENCE:

```
tests/cli/test_ci_cmd.py
tests/orchestration/test_ci_budgets.py
tests/orchestration/test_ci_run.py
tests/orchestration/test_ci_stage_selection.py
tests/orchestration/test_ci_stages.py
tests/orchestration/test_ci_workflow.py
tests/ui_server/test_dashboard_contract.py
```

Get the node ids from `python3 -m pytest <those seven files> --collect-only -q`
and the counts from running the same seven files. ONE record, with
`run_id="vr-0001"` — the regex is `^vr-\d{4,}$` and a rejected VerificationTests
document yields `vt_passed = None`, which fails the final-verifier confirmation —
the exact `command`, the real `exit_code`, `passed`, `failed`, `skipped`,
`selected`, `node_ids` with `len(node_ids) == selected`, `test_files` as the seven
FILES above and NEVER a directory, `output_hash` as a sha256 hex string,
`head_sha` the C2 head, and a `stdout_summary`. NEVER a full-suite node-id list:
`len(node_ids) == selected` forbids filtering, and the packaging metadata scan
rejects the redaction-torture parametrizations whose ids embed fake secrets and
absolute paths by design. F083's full-suite proof rides in the committed R26 gate
evidence and the reviewer's own re-run, not here.

## THE REVIEW ZIP, still between C2 and C3, still from a clean tree

```
git status --porcelain          # must be EMPTY
bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f083-closure
```

Record the printed filename and SHA-256, and confirm the manifest's
`committed_review_subject` head_commit equals the C2 head. If the build fails,
constraint 7 applies.

## Constraints

1. Change set over the whole range: `.agent/authored/f083-r28.md`,
   `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
   `.agent/candidates.md`, `.agent/handoff.md`, `docs/roadmap/STATUS.md` and
   `README.md`. Nothing else. `packages/`, `apps/`, `scripts/`, `tests/` and
   `.github/` stay EMPTY in the range diff, and `docs/` contains EXACTLY ONE
   file, `docs/roadmap/STATUS.md`. Gate 12 measures both as restrictions.
2. Apply every slice BYTE-VERBATIM, except the three placeholder tokens named
   above. A defect in the reviewer's text is a declared deviation, never a silent
   repair.
3. C1 lands BEFORE C2. C3 is the LAST commit on this branch. NO commit follows
   C3 — if something needs correcting afterwards it goes into the handoff's
   deviations and into the round report, not into a trailing commit, because the
   STATUS edit must be the branch's final commit (Rule A4).
4. This round adds NO worktree. `git worktree list` is one line throughout.
   Never force-push, never amend, never rebase, never reset. Never work on `main`.
5. The evidence directory is NEVER committed. Write it to
   `remedy-job-evidence-f083-closure/` at the repo root, which `.gitignore` drops
   at line 226 (`remedy-job-evidence-*/`). A committed evidence dir puts evidence
   files into the base..HEAD review subject and the package builds
   BLOCKED_EVIDENCE — the F147 attempt-2 lesson.
6. The zip is built from a CLEAN tree after C2 and BEFORE C3. A package built
   from a dirty tree is invalid.
7. A FAILING ZIP BUILD IS A CLOSURE BLOCKER, not a deviation: do not close over
   it. Record the raw error verbatim in the handoff, do NOT make C3, do NOT
   create the PR, and end the round. R29 then repairs it. This is the one place
   where ending without closing is the correct outcome.
8. The PR is created but NEVER merged this session. Run no `gh pr merge`.
9. Your handback's Deviations section states explicitly whether the ordered
   commit sequence was followed.

## Done when — every command its own unpiped process, each exit code read from
## that process, the working directory named for every one of them

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit,
   before the zip build, and after C3. `git worktree list` ONE line throughout.
   `.agent/STOP` ABSENT at round start and again at handback.
2. `git rev-parse HEAD` before the first commit; report the SHA it printed and
   whether that SHA equals 74063862.
3. TRANSPORT, bytes read in Python: report the sha256, byte count and line count
   of `.remedy-wt/f083-r28.md`, the committed `.agent/authored/f083-r28.md` and
   the committed `.agent/last_block.md`, and whether all three are byte-EQUAL.
4. C1: the pre content of `.agent/live_review.md` PREFIXES the post content, the
   tail byte-EQUALS the RECORD-R27 slice extracted from the committed authored
   file by its markers, and `git show --numstat` has deletion column 0. Report
   the file's transport BEGIN-marker LINE count at base and at HEAD; equal.
5. C2: `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   unchecked-box lines. Report the C2 head SHA in FULL 40-char form — this is the
   ACCEPTED HEAD, and gates 8 and 9 both refer back to it.
6. EVIDENCE JOB: report the producer call's returned summary, the evidence
   directory path, and that `git status --porcelain` is STILL EMPTY afterwards —
   the directory is gitignored and must not appear.
7. VERIFICATION RECORD, before packaging: report `selected`, `len(node_ids)` and
   whether they are equal; that `test_files` holds the seven paths and is sorted;
   that `run_id` matches `^vr-\d{4,}$`; and that `output_hash` is 64 hex chars.
8. REVIEW ZIP: report the exact command, its exit code, the package filename, the
   SHA-256, and the manifest's `committed_review_subject` head_commit with
   whether it equals the C2 head of gate 5. A failure here ends the round.
9. STATUS LINE, proven as a substitution and not as prose: report the final line
   from `docs/roadmap/STATUS.md` VERBATIM; report that the file contains `<<` 0
   times; and report that replacing the three measured values back with their
   tokens reproduces STATUSLINE-TO BYTE-FOR-BYTE. Report `^- \[~\] F083` 0x and
   `^- \[x\] F083` 1x in that file, and the count of `^- \[x\] F\d{3} — ` lines.
10. README: for READMECOUNT and READMETIER report the FROM count before, the FROM
    count after, the TO count after, and the composite
    `pre.replace(F1,T1).replace(F2,T2) == post` measured over the whole file.
11. VERIFICATION, each its own process with its own exit code read separately:
    `python3 -m pytest tests/docs/ -q` — the change set includes
    `docs/roadmap/**`, and this is the gate that pins the README count and the
    Tier-2 row to the ledger, so it is the real check on C3 rather than a
    formality. Then the canary `python3 -m pytest tests/cli/test_golden_path.py
    -q`. Report the passed count and the real exit code for EACH.
12. CHANGE SET over `74063862..HEAD`, measured after C3: report the full list and
    its count. Restricted to `packages/ apps/ scripts/ tests/ .github/` it must be
    EMPTY; restricted to `docs/` it must be EXACTLY `docs/roadmap/STATUS.md`.
    Report both restrictions as measured lists.
13. OPEN SET recomputed mechanically at HEAD from `.agent/live_review.md`:
    `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` lines and `^Landed: R-\d+ — `
    lines; report registered, resolved, landed, open, the max id, the next free
    id, and that no id repeats and no resolution names an unregistered id. Report
    the values measured; this block predicts none of them.
14. `remedy integrity check --json` — report `passed`, `fail_count` and the status
    of every named check. This is closure precondition 3.
15. Per-commit insertions from `git show --numstat` for C0a, C0b, C1 and C2 — the
    commits that exist before the handoff is written — none exceeding 500. C3's
    own insertion count goes in the ROUND REPORT, not the handoff, per checklist
    item 14. Report that the history is linear with no amend, rebase or reset,
    naming the number of commits the range holds at the time you read it.
16. PR: `gh pr create` with a description carrying what changed and why, the key
    decisions, how to review, the changed-files table, the latest verdict, the
    open-findings count and the runtime actuals. Report the PR number and URL.
    Run NO `gh pr merge`.

## Handback

Completion report plus a rewritten `.agent/handoff.md` per
`docs/agents/handback_template.md`, written INTO C3: feature and round, branch,
the commit table, the item-status table with every ordered item above appearing
exactly once, the real verification results, the open-findings count, the package
filename and SHA-256, the accepted HEAD, the PR number, and the next expected
action — which is that the PR merges at the NEXT feature's Open PR Gate and is
not merged now.

Fortschritt: 100 % der Bau-Arbeit, Closure läuft (F083 beansprucht · R1 bis R7, R9 bis R21, R23 bis R27 PASS, R8 und R22 FAIL — beide in der Folgerunde repariert · T001, T002 und T003 fertig · Integration Gate bei R26 grün in beide Richtungen, 0 branch-only und 0 base-only Failures, vom Reviewer selbst nachgefahren · Built State bei R27 gelandet · diese Runde macht Evidence-Job, frische Review-Zip, STATUS-Zeile, README-Sync und PR · der PR wird bewusst NICHT in dieser Session gemerged · R-0482 und R-0487 gehen auf einen eigenen Paydown-Branch · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
