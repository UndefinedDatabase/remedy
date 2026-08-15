── STEP R23/23 — F082 Self-benchmark — CLOSURE ────────────────────────────────

Goal:
  Close F082 per docs/roadmap/STATUS_closure_protocol.md. Record the R22 PASS,
  register the two defects R22 exposed — both the reviewer's own — repair the
  round-map sentence that now contradicts itself on disk, then run the closure
  algorithm: the evidence job, a FRESH review zip, the STATUS line, the README
  count and Tier-2 row, the candidates carrier, and the PR. It changes no code
  and no test.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f082-r23.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R22 + R-0446 + R-0447, appended at EOF in
       ONE commit. Findings persist FIRST (planner_reviewer_prompt §4.4).
  C2   `.agent/context.md` (both pairs) and `.agent/plan.md` (PLAN, whole file),
       ONE commit. This is the LAST CONTENT COMMIT — its HEAD is the ACCEPTED
       HEAD the zip and the STATUS line both record.
  ——  the evidence job and the review zip run HERE, against the C2 head, from a
       clean tree. Neither is committed.
  C3   the CLOSURE COMMIT, and the last commit on this branch (Rule A4):
       `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md` and
       `.agent/handoff.md`. Exactly those four paths (R-0154) — nothing else.
  ——  then `gh pr create`. The PR is NOT merged this session (protocol step 6).

BASE: 9cc80e33. Re-derive `git rev-parse HEAD` before the first commit and
report whether it equals 9cc80e33 (R-0428). If it does NOT, stop and hand off.

TRANSPORT: the reviewer's scratchpad original of THIS block is on disk at
`.remedy-wt/.cache/r23/f082-r23.md`, which `.gitignore` drops (line 235,
`.remedy-wt/`). C0a is a byte COPY of that file — do not retype it, do not
reflow it, do not strip anything.

SLICE CONVENTION (R-0437): every FROM and TO body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The block's authored units are, listed: one EOF
append (GATE-R22-BLOCK); five REWRITE pairs with FROM and TO disjoint (CTX-D12
and CTXSTEPS-R23 in `.agent/context.md`, STATUSLINE in
`docs/roadmap/STATUS.md`, READMECOUNT and READMETIER in `README.md`); and two
whole-file replacements (PLAN, CANDIDATES). No numeral is stated for that list —
the list IS the statement (R-0402, R-0441).

THE STATUS LINE IS THE ONE SLICE THAT CANNOT BE FULLY AUTHORED. It carries three
values that do not exist when this block is written — the zip filename, its
SHA-256, and the accepted HEAD — and ordering a value that cannot yet exist is
exactly R-0371. So STATUSLINE-TO below carries three literal placeholder tokens,
`<<ZIP>>`, `<<SHA256>>` and `<<HEAD40>>`, and the worker substitutes ONLY those
three, each exactly once, with the measured value. Everything else in that line
is byte-verbatim and gate 9 proves it. Substituting anything else, or leaving a
`<<` token behind, is a failure of the round.

Constraints:
  1. Change set: `.agent/authored/f082-r23.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/context.md`, `.agent/plan.md`,
     `.agent/candidates.md`, `.agent/handoff.md`, `docs/roadmap/STATUS.md`,
     `README.md`. Nothing else. `packages/`, `apps/`, `scripts/` and `tests/`
     stay EMPTY in the range diff; `docs/` contains EXACTLY ONE file,
     `docs/roadmap/STATUS.md`. Gate 12 measures both as restrictions.
  2. Apply every slice BYTE-VERBATIM, except the three placeholder tokens named
     above. A defect in my text is a declared deviation, never a silent repair.
  3. C1 lands BEFORE C2. C3 is the LAST commit. No commit follows C3 — if
     something needs correcting afterwards, it goes in the handoff's deviations
     and into `.agent/candidates.md`, not into a trailing commit, because the
     STATUS edit must be the branch's final commit (Rule A4).
  4. This round adds NO worktree. `git worktree list` is one line throughout.
  5. The evidence directory is NEVER committed. Write it to
     `remedy-job-evidence-f082-closure/` at the repo root, which `.gitignore`
     drops (line 226, `remedy-job-evidence-*/`). A committed evidence dir puts
     evidence files into the base..HEAD review subject and the package builds
     BLOCKED_EVIDENCE — the F147 attempt-2 lesson.
  6. The zip is built from a CLEAN tree after C2 and BEFORE C3. A package built
     from a dirty tree is invalid.
  7. A failing zip build is a closure BLOCKER, not a deviation: do not close
     over it. Record the raw error in the handoff, do NOT make C3, do NOT create
     the PR, and end. R24 then repairs it. This is the one place where ending
     without closing is the correct outcome (G8).

--- BEGIN SLICE GATE-R22-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R22 — PASS. Verification tier: the docs-round gate plus the canary, both re-run by the reviewer; no full-suite claim is made here, because F082's full-suite claim belongs to R21 and is not restated. All fifteen ordered gates reproduce against the committed tree. TRANSPORT held for the second consecutive round in its new shape: scratchpad, authored and last_block are all sha256 1c1ad2c8d14a1db569cee8e1899906048db04aefc8e4a21a0b70eea9851ff159, 28609 bytes, 324 lines, byte-equal, footer 324 equal to measured 324. C1's prefix property is True with a `35 0` numstat. C2 is the round's structurally interesting proof: two rewrite pairs AND an append into the SAME file were settled by ONE equality, `pre.replace(F1,T1).replace(F2,T2) + b"\n" + BUILTSTATE == post`, measured True — a shape worth reusing, because it cannot be satisfied by applying two of the three edits correctly. C3's context pair and composite are True. All five live_review line-anchored counts and all three feature-file counts hit their ordered values, including the zero-gate `a later round owes a test` 0x. `.agent/plan.md` byte-equals the PLAN slice at sha256 947d27ab0cccd9b935fee794f5115a4ea40b484be1cefa59dfa5c4fdce559438, 46 lines. `tests/docs/` collected 295 and passed 295, exit 0, and the canary 42 and 42, exit 0 — both re-run by the reviewer at HEAD, and both equal to the counts the block declared at emission, which is R-0438's rule holding for a second round. The OPEN SET recomputed at HEAD is 75 registered, 2 resolved, 73 open, max R-0445, next free R-0446, 4 `Landed:` lines, no duplicate id. The integrity gate passes all five checks with `fail_count` 0. The change set restricted to `packages/`, `apps/`, `scripts/` and `tests/` is EMPTY and `docs/` holds exactly the one feature file; `docs/roadmap/STATUS.md` and `README.md` are untouched, as ordered. Insertions 324 · 249 · 35 · 61 · 28 · 172 · 7, none over 500. ONE unordered commit exists — 9cc80e33, a seven-insertion correction to `.agent/handoff.md` recording the push and the re-measured D15 line count that the handoff could not state from inside itself. It is within the round's declared path set, it is honestly declared, and it is the R-0371 self-reference limit showing up as bookkeeping rather than as a false claim; it is accepted, not a finding, and C3 of the closure round is ordered as the branch's last commit so the pattern does not repeat where Rule A4 forbids it. TWO findings are registered below and both are defects of the reviewer's own block text; the worker declared both before the reviewer read the diff, which is the sixth consecutive round.

- R-0446 — Low, A PARSE RULE ORDERED OVER TEXT IT DOES NOT FIT, SO THE GATE'S POPULATION DEPENDS ON WHICH READING YOU TAKE. Found by the WORKER while executing R22's gate 12(a). The gate ordered the open-set severity census read as "the word that follows `^- R-\d+ — ` up to the first comma". Across the 75 registered paragraphs the character immediately after the severity word is a space 47 times and a comma 28 times, because this ledger's finding titles are written as "Medium, A GATE THAT ..." in some rounds and "Medium A GATE THAT ..." in others. Under the strictest reading — severity word immediately followed by a comma — the rule classifies 26 of 73 open findings and silently drops 47 while still reporting a green census; under the looser reading it classifies all 73. The worker substituted "the first word after the em-dash", reported BOTH censuses, and the answer is identical either way: Blocker 0, High 0, Medium 23, Low 50. The reviewer independently recomputed both readings at HEAD and got Low 50 and Medium 23 under each. Low, because the closure precondition this census exists to test — no open Blocker or High — holds under every reading, and because the worker caught it before it mattered. It is registered because of the shape, which is now the fourth member of one family: R-0439 said a per-line count must name which lines it ranges over, R-0442 said a handback count must name the string it counted, and this one says a PARSE rule must be validated against the text it will parse. Standing rule from here, binding the reviewer: a gate that extracts a field by a textual rule is run against the actual corpus at emission and the block states how many items the rule successfully classifies out of how many exist. A rule that silently drops the items it cannot parse is the vacuous-gate class R-0438 named, wearing different clothes.

- R-0447 — Medium, A STATE FILE THAT NOW CONTRADICTS ITSELF, BECAUSE A DECISION MOVED A VALUE AN EARLIER AUTHORED SENTENCE HAD QUOTED. Found by the WORKER through the standing staleness gate, which is exactly what that gate exists for. `.agent/context.md` at the R22 head says in one place "the round map now runs to R21 the integration gate and R22 closure (DECISION F082 D11)" and in another, four dozen lines later, "→ R23 closure, per DECISION F082 D12". Both sentences are on disk in the same file at the same commit and they disagree about which round closes this feature. The reviewer confirmed it by literal count at HEAD: `DECISION F082 D11` 1x, `DECISION F082 D12` 1x, `R22 closure` 1x, `R23 closure` 1x. The cause is precise. The offending sentence was authored by the REVIEWER at R21 as the CTX-D10 pair's TO, to retire a stale D10 citation — and it retired that citation by quoting the round map, a value that moves. One round later the reviewer's own DECISION D12 moved it, and the R22 block that ruled D12 carried no pair to repair the sentence D12 falsified. Medium, not Low: `.agent/context.md` is read by thirteen test files and is the reviewer's context of record across sessions, so a reader resuming from disk gets two different answers to "which round closes F082" with nothing to break the tie. Not High because no test asserts the round map and the plan and the Steps chain both agree on R23. This is R-0440 recurring one round after R-0440 was written, in the reviewer's own text rather than in a `Done:` paragraph, which is precisely the generalisation R-0440 failed to make. Standing rule from here, binding the reviewer: a block that rules a DECISION changing any value carries, in the SAME block, a repair pair for every sentence on disk that states that value — found by grepping the value, not by recalling where it was written. The staleness gate is the backstop, not the mechanism; a contradiction it merely REPORTS has already shipped.
--- END SLICE GATE-R22-BLOCK ---

--- BEGIN SLICE CTX-D12 --- (in .agent/context.md, C2 — REWRITE pair, FROM and TO disjoint; this is R-0447's repair)
the Goal's three DONE conditions together. R20 recorded that PASS, and the round
map now runs to R21 the integration gate and R22 closure (DECISION F082 D11).
--- BEGIN SLICE CTX-D12-TO --- (C2)
the Goal's three DONE conditions together. R20 recorded that PASS. The round map
is stated once, in the Steps section below, and is not restated here — a map
quoted in two places is the contradiction R-0447 records.
--- END SLICE CTX-D12-TO ---

--- BEGIN SLICE CTXSTEPS-R23 --- (in .agent/context.md, C2 — REWRITE pair, FROM and TO disjoint)
verdict, register R-0438 and R-0439 and rule at D11 ✅ → R21 the integration
gate ✅ → R22 record R21, register R-0443 to R-0445 and bring Built State
current → R23 closure, per DECISION F082 D12.
--- BEGIN SLICE CTXSTEPS-R23-TO --- (C2)
verdict, register R-0438 and R-0439 and rule at D11 ✅ → R21 the integration
gate ✅ → R22 record R21, register R-0443 to R-0445 and bring Built State
current ✅ → R23 closure, per DECISION F082 D12.
--- END SLICE CTXSTEPS-R23-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C2)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. Next free finding id: R-0448. Open findings: seventy-five — the
thirty-two carried from F077, plus R-0403 to R-0447 registered on this branch,
less R-0435 and R-0436 resolved at R20. `.agent/live_review.md` is the source of
truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning. All three conditions are measured by the suite.

## Current Step
R23 is CLOSURE: it records the R22 PASS, registers R-0446 and R-0447, repairs
the self-contradicting round map R-0447 reports, then runs the closure algorithm
— the evidence job, a fresh review zip, the STATUS line claiming `[x]`, the
README count and Tier-2 row, `.agent/candidates.md`, and the PR.

## Next Steps
1. Nothing on this branch. The PR is NOT merged this session; it merges at the
   next feature's start via the AGENTS.md Open PR Gate, which is the operator's
   manual-review window.
2. The next feature is F083 — CI self-check, per Rule A5. A fresh session claims
   it and its first reviewed round registers or resolves every entry in
   `.agent/candidates.md`.

## Risks
- Closure is PASS_WITH_RISKS, not PASS: seventy-five findings are open, all
  Medium or Low, none a Blocker or High under either parse reading (R-0446).
- Three carried defects are open against process docs rather than against F082
  code: R-0445 (integration_gate.md manufactures eight false base failures on
  every run), R-0444 (a content digest cannot see an identical rebuild) and
  R-0403 (the review zip packages `.remedy-wt/`). None is repaired here; a
  process-doc fix inside a feature branch is scope drift.
- Every acceptance measurement was taken under DOUBLES, never a live provider;
  the delivered order set is three, not five (R-0411); the freeze holds against
  a file-side edit only (R-0410); the builder's model stays unobservable. The
  feature file's Built State states all four absences.
--- END SLICE PLAN ---

--- BEGIN SLICE CANDIDATES --- (WHOLE FILE replacement of .agent/candidates.md, C3)
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

(no candidate was carried out of F082's closure review at the time this file was
written. Every defect the closure round's worker declares in its handback is
appended below, one line each, in the form
"- <description> · F082 · 2026-08-15"; if the worker declares none, this file
stays as it is and the next feature's first reviewed round empties nothing.)
--- END SLICE CANDIDATES ---

--- BEGIN SLICE STATUSLINE --- (in docs/roadmap/STATUS.md, C3 — REWRITE pair, FROM and TO disjoint)
- [~] F082 — Self-benchmark
--- BEGIN SLICE STATUSLINE-TO --- (C3 — substitute ONLY <<ZIP>>, <<SHA256>> and <<HEAD40>>, one occurrence each)
- [x] F082 — Self-benchmark (T001–T003 complete; accepted 2026-08-15 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f082-closure · package <<ZIP>> · SHA-256 <<SHA256>> · accepted HEAD <<HEAD40>>)
--- END SLICE STATUSLINE-TO ---

--- BEGIN SLICE READMECOUNT --- (in README.md, C3 — REWRITE pair, FROM and TO disjoint)
48 of 255 registered items accepted. Next: F082 (Self-benchmark).
--- BEGIN SLICE READMECOUNT-TO --- (C3)
49 of 255 registered items accepted. Next: F083 (CI self-check).
--- END SLICE READMECOUNT-TO ---

--- BEGIN SLICE READMETIER --- (in README.md, C3 — REWRITE pair, FROM and TO disjoint)
| 2 | Minimal Self-Build Runtime | 10 | 14 |
--- BEGIN SLICE READMETIER-TO --- (C3)
| 2 | Minimal Self-Build Runtime | 11 | 14 |
--- END SLICE READMETIER-TO ---

THE EVIDENCE JOB, between C2 and C3, from a clean tree:

Build the bundle through the canonical producer — `write_runtime_integration_gate`
alone is NOT a bundle and packages as BLOCKED_EVIDENCE:

```
from packages.orchestration.job_evidence import create_manual_completion_bundle
```

Call it with `evidence_dir="remedy-job-evidence-f082-closure"`,
`repo_root` the absolute repo path, `base_commit` the FULL 40-character merge
base `668d40f7ca691ba25e5293157651ddca853bbd4f`, `job_id="f082-closure"`,
`job_title="F082 Self-benchmark closure"`, `step_range="T001-T003"`,
`prior_job_ids=[]`, `head_commit` the C2 head, `review_feature_id="f082"`, and
`timestamp`/`generated_at` as ISO-8601 Z strings.

`verification_runs` is the part that has blocked four previous closures, so
BUILD IT FROM A REAL RUN rather than typing values. Use F082's own scoped
suite, which the reviewer ran at emission and measured at 90 passed, exit 0:

```
tests/orchestration/test_bench_dry_run.py
tests/orchestration/test_bench_history.py
tests/orchestration/test_bench_model_context.py
tests/orchestration/test_bench_never_runs_implicitly.py
tests/orchestration/test_bench_orders.py
tests/orchestration/test_bench_run.py
tests/orchestration/test_capability_bench.py
tests/cli/test_stats_bench.py
```

Get the node ids from `python3 -m pytest <those files> --collect-only -q` and
run the suite for the counts. ONE record, with `run_id="vr-0001"` (the regex is
`^vr-\d{4,}$`), the exact `command`, the real `exit_code`, `passed`, `failed`,
`skipped`, `selected`, `node_ids` (every id, `len(node_ids) == selected`),
`test_files` as the eight FILES above and never a directory, `head_sha` the C2
head, and a `stdout_summary`. Never a full-suite node-id list: the
`len(node_ids) == selected` rule forbids filtering, and the packaging metadata
scan rejects the redaction-torture parametrizations whose ids embed fake secrets
by design (the F080 R4 lesson, 94 rejected ids). F082's full-suite proof rides
in the committed R21 gate evidence and the reviewer's own re-run, not here.

THE REVIEW ZIP, still between C2 and C3, still from a clean tree:

```
git status --porcelain          # must be EMPTY
bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f082-closure
```

Record the printed filename and SHA-256, and confirm the manifest's
`committed_review_subject` head_commit equals the C2 head. If the build fails,
Constraint 7 applies: record the raw error, make no C3, create no PR, end.

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit, before the zip
    build, and after the last commit. `git worktree list` ONE line throughout.
    `.agent/STOP` ABSENT at round start and again at handback (R-0347).
 2. TRANSPORT, bytes read in Python: report sha256, byte count and line count of
    `.remedy-wt/.cache/r23/f082-r23.md`, `.agent/authored/f082-r23.md` and
    `.agent/last_block.md`, whether all three byte strings are EQUAL, and
    whether the measured line count equals this block's declared footer count.
 3. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 9cc80e33.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` is a prefix of `post`, and
    `post[len(pre):]` equals `b"\n" + GATE-R22-BLOCK` byte-for-byte. Report the
    numstat and confirm its deletion column is 0.
 5. C2: for CTX-D12 and CTXSTEPS-R23 report the FROM count in `pre`, the FROM
    count in `post`, the TO count in `post`, and `FROM in TO`; then the
    composite `pre.replace(F1,T1).replace(F2,T2) == post` over
    `.agent/context.md`. Separately, `.agent/plan.md` at the C2 head byte-equals
    the PLAN slice as a whole file — report sha256 and line count (under 50),
    and that `## Goal` and `## Next Steps` are both present.
 6. R-0447 IS REPAIRED, measured on `.agent/context.md` at HEAD as literals:
    `DECISION F082 D11` 0x, `R22 closure` 0x, `R23 closure` 1x,
    `DECISION F082 D12` 1x. Report all four.
 7. EVIDENCE JOB: report the producer call's returned summary dict, the
    evidence directory path, and that `git status --porcelain` is still EMPTY
    afterwards — the directory is gitignored and must not appear.
 8. REVIEW ZIP: report the exact command, its exit code, the package filename,
    the SHA-256, and the manifest's `committed_review_subject` head_commit with
    whether it equals the C2 head. A failure here ends the round (Constraint 7).
 9. STATUS LINE, proven as a substitution and not as prose: report the final
    line from `docs/roadmap/STATUS.md` verbatim; report that it contains `<<` 0
    times; and report that replacing the three measured values back with their
    tokens reproduces STATUSLINE-TO byte-for-byte. Report `^- \[~\] F082` 0x and
    `^- \[x\] F082` 1x in that file, and that the count of `^- \[x\] ` lines is
    49.
10. README: for READMECOUNT and READMETIER report the four pair numbers each,
    plus the composite `pre.replace(F1,T1).replace(F2,T2) == post`.
11. VERIFICATION. `python3 -m pytest tests/docs/ -q` — the change set includes
    `docs/roadmap/**`, and the reviewer measured this target at 295 collected at
    emission. Then the canary `python3 -m pytest tests/cli/test_golden_path.py
    -q`, 42 collected. Report the collected count and the real exit code for
    EACH, separately (R-0438). `tests/docs/` is the gate that pins the README
    count and the Tier-2 row to the ledger, so it is this round's real check on
    C3, not a formality.
12. CHANGE SET, measured BEFORE the handoff is written into C3:
    `git diff --name-only 9cc80e33..HEAD`. Report the full list and its count.
    Restricted to `packages/`, `apps/`, `scripts/` and `tests/` it must be
    EMPTY; restricted to `docs/` it must be EXACTLY ONE file,
    `docs/roadmap/STATUS.md`. Report both restrictions as measured lists.
13. OPEN SET recomputed mechanically at HEAD: count `^- R-\d+ — ` paragraphs,
    count `^Done: R-\d+ — ` lines, report both, their difference, the max id,
    the next free id, the count of remaining `^Landed: ` lines, and any
    duplicate id. Expected 77 registered and 2 resolved; report what you
    MEASURE, and if it differs say so rather than reconciling it.
14. CLOSURE PRECONDITIONS re-measured at the closure head, not carried from R22.
    (a) The severity census of the OPEN set by the rule R-0446 settled on — the
    first word after the em-dash — reporting how many of the open findings that
    rule successfully classifies out of how many exist, then the Blocker, High,
    Medium and Low counts. (b) The integrity gate, in Python because the
    `remedy` CLI is denied in this session class (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` —
    report `passed`, `fail_count` and every named check's status.
15. Insertions (`+` column only) per commit — report each; none over 500.
16. THE PR: `gh pr create` with a description carrying what changed and why, the
    key decisions (D1 to D12), how to review, a changed-files summary, the
    latest verdict, the open-findings count, and the runtime actuals you can
    observe. Report the PR number and URL. Do NOT merge it (protocol step 6).
    Then `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
    and report it — exactly one non-draft PR from this branch into `main`.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as
part of C3 — feature and round, branch, per-commit changed-files tables, every
gate value above, the item-status table covering every C-item and every gate,
open findings with max and next free id, the package name and SHA-256, the
evidence job id, the PR number, and the next expected action. Note that C3
cannot table its own SHA (R-0371, R-0149) and say so rather than inventing one;
do NOT add a trailing commit to correct it, because C3 must be the branch's last
commit (Constraint 3). Repeat this line verbatim as the Fortschritt line:

Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · alle drei DONE-Bedingungen gemessen · Integrationsgate ✅ PASS · Closure gelaufen · PR offen, Merge erst beim nächsten Feature) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 327 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
