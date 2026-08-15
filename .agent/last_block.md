── STEP R1/8 — F083 CI self-check — CLAIM ─────────────────────────────────────

Goal:
  Claim F083 and open its record. Cut the branch, reset `.agent/live_review.md`
  for F083 carrying F082's open set forward, register the three closure-review
  candidates F082's R23 review produced as R-0448, R-0449 and R-0450, refresh
  the candidates carrier, and claim `[ ]`→`[~]` in the ledger. It changes no
  code and no test. The T001 marker inventory is R2, not this round.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r1.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — the WHOLE FILE, rebuilt as LIVEREVIEW-HEAD plus
       the carried open set. Findings persist FIRST (planner_reviewer_prompt §4.4).
  C2   `.agent/context.md` (CTX, whole file), `.agent/plan.md` (PLAN, whole file),
       `.agent/candidates.md` (CANDIDATES, whole file) and
       `docs/roadmap/STATUS.md` (STATUSLINE pair), ONE commit — the claim.
  C3   `.agent/handoff.md`, the handback, alone.

BRANCH: `git checkout -b feature/f083-ci-self-check` from `main` at
f3fd96d729c3be85604a2d37aee42c59fe39868a BEFORE C0a. The F082 closure PR #201 is
already merged by the reviewer at the Open PR Gate; do not merge anything.

BASE: f3fd96d729c3be85604a2d37aee42c59fe39868a. Re-derive `git rev-parse HEAD`
after the checkout and before the first commit, and report whether it equals that
value (R-0428). If it does NOT, stop and hand off.

TRANSPORT: the reviewer's scratchpad original of THIS block is on disk at
`.remedy-wt/.cache/f083-r1/f083-r1.md`, which `.gitignore` drops (line 235,
`.remedy-wt/`). C0a is a byte COPY of that file — do not retype it, do not
reflow it, do not strip anything.

SLICE CONVENTION (R-0437): every FROM and TO body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The block's authored units are, listed: one
whole-file HEAD fragment that a mechanical carry completes (LIVEREVIEW-HEAD);
three whole-file replacements (CTX, PLAN, CANDIDATES); and one REWRITE pair with
FROM and TO disjoint (STATUSLINE in `docs/roadmap/STATUS.md`). No numeral is
stated for that list — the list IS the statement (R-0402, R-0441).

THE CARRY IS MECHANICAL, NOT AUTHORED. `.agent/live_review.md` at BASE holds
every `^- R-\d+ — ` paragraph on ONE line each; the reviewer measured 77 such
paragraphs and 2 `^Done: R-\d+ — ` lines there. C1 builds the new file, as BYTES,
as exactly:

```
expected = HEAD + b"\n" + b"\n\n".join(carried) + b"\n"
```

`HEAD` is the LIVEREVIEW-HEAD slice body under the slice convention, so it ends
with R-0450's line and that line's newline. `carried` is, in BASE file order,
every `^- R-\d+ — ` LINE whose id appears in NO `^Done: R-\d+ — ` line, each as
one line with no newline of its own — the join supplies the blank line between
paragraphs and the final `b"\n"` terminates the last one. Extract them out of the
BASE file with Python; never retype a finding. `Gate:`, `Done:` and `Landed:`
lines are NOT carried, and the head slice says so in prose, so nothing is
silently dropped. This formula is not invented here: the reviewer applied it to
`.agent/live_review.md` at commit e978262b, the F082 reset, and it reproduced
that file byte-for-byte over its 33 paragraphs.

Constraints:
  1. Change set: `.agent/authored/f083-r1.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/context.md`, `.agent/plan.md`,
     `.agent/candidates.md`, `.agent/handoff.md`, `docs/roadmap/STATUS.md`.
     Nothing else. `packages/`, `apps/`, `scripts/` and `tests/` stay EMPTY in
     the range diff; `docs/` contains EXACTLY ONE file, `docs/roadmap/STATUS.md`.
     Gate 10 measures both as restrictions.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared
     deviation in the handback, never a silent repair. No slice below contains an
     instruction to the worker; the instructions are in this block only (R-0450).
  3. C1 lands BEFORE C2. Push after C3.
  4. NO PULL REQUEST this round. F083's PR is created at closure, not before —
     the F082 precedent and STATUS_closure_protocol step 5. `gh pr create` is
     out of scope; the AGENTS.md "create a PR if reviewable" rule is satisfied by
     the closure round, and this constraint is the deviation record for it.
  5. This round adds NO worktree. `git worktree list` is one line throughout.
  6. `docs/roadmap/ROADMAP.md` is NOT edited (AGENTS.md documentation boundary);
     only the one STATUS.md line changes.

--- BEGIN SLICE LIVEREVIEW-HEAD --- (HEAD of the rebuilt .agent/live_review.md, C1; the carry defined above follows it)
# Live Review — F083 CI self-check

> Round-by-round review record for the F083 branch, reset at the feature claim.
> The F082 record closed with PR #201, merged 2026-08-15; that branch's closing
> verdict lives in its handoff and in the PR, per
> docs/agents/planner_reviewer_prompt.md §4 item 13. Finding ids continue the
> monotonic R-XXXX series across the reset. Next free id: R-0451.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The seventy-five findings
> open when the F082 record closed are reproduced verbatim at the end of this
> file, extracted by id out of the previous record and never retyped. The
> pre-reset record also held four `Landed:` lines, for R-0431, R-0432, R-0433 and
> R-0434, recording repairs that landed without a formal resolution; those lines
> are NOT carried, and that repair status is read out of git history rather than
> out of this file.

## Steps
R1 merge the F082 closure PR at the Open PR Gate, claim F083, reset this record
carrying the F082 open set forward, and register the three F082 closure-review
candidates as R-0448, R-0449 and R-0450 → R2 the T001 marker inventory: the
collected count and the wall time per marker, which markers already exist, and
which stage each belongs to, every answer carrying a file-and-symbol citation →
R3 T001 the stage runner, the marker selections and the summary table → R4 T002
the determinism and budget stages plus the guard-test wiring → R5 T002 the
seeded-failure test per stage → R6 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R7 the integration gate → R8
closure. Each round marks the PREVIOUS one done and never itself; the map is
stated here ONLY, and no other file restates it (R-0447).

## Findings

- R-0448 — Medium, A CLOSURE BLOCK ORDERED AN EVIDENCE FIELD IN AN ORDER THE PACKAGING VALIDATOR REJECTS, SO THE FIRST PACKAGE BUILT BLOCKED_EVIDENCE. Raised by the reviewer during F082's R23 closure review and registered here as a closure candidate, per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings". The R23 block ordered `verification_runs[0].test_files` as "the eight FILES above", and that authored list was not sorted — `tests/cli/test_stats_bench.py` was written last and sorts first. `scripts/build_review_manifest.py::_vt_safe_files` rejects a list for which `tf != sorted(tf)`, which invalidates the whole VerificationTests document and leaves `vt_passed` unconfirmable, so packaging attempt 1 returned PACKAGE_STATUS=BLOCKED_EVIDENCE with two blocking reasons, of which `validate_evidence_candidate` named the sorting one as the single root error. The worker repaired it inside the round — the same eight files sorted, the suite re-run in that order so `command` and `node_ids` still describe a real execution, the evidence directory rebuilt from scratch, and `validate_evidence_candidate` checked BEFORE the second build — and attempt 2 packaged READY_FOR_REVIEW. The reviewer re-verified the delivered package independently rather than accepting the handback: sha256 3e8e33eb4bb724ce775ea5987e0fee0de5341d1a3bfe902c6e5f4f6f2deb84b2 recomputed from disk, `zipfile.testzip()` None, 6060 members, `ready_gate_matrix.ok` True with `blocking_reasons` `[]`, and `committed_review_subject.head_commit` equal to the accepted head 4b9bc7bc1dabdde5fca68de6ae20f86b11d21eb0. Nothing false was closed over. Medium, not Low, because this is a NEW member of a family the closure protocol already documents and therefore already knows how to prevent: the producer pitfalls listed at STATUS_closure_protocol.md Algorithm step 1 are (a) node ids with `len(node_ids) == selected`, (b) test_files that are files and never directories, (c) the `^vr-\d{4,}$` run_id regex and (d) never a full-suite node-id list — and the sorted-`test_files` rule is a fifth, (e), which that document does not carry, so every future closure block can lose a build to it exactly as this one did. The fix is one bullet in `docs/roadmap/STATUS_closure_protocol.md`; that is a process doc F083 does not own and AGENTS.md forbids mixing an unrelated fix into a feature branch, so it routes to a paydown branch exactly as R-0403, R-0444 and R-0445 were routed. OPEN.

- R-0449 — Low, A BLOCK ORDERED A VALUE INTO AN ARTIFACT THAT IS WRITTEN BEFORE THE VALUE CAN EXIST. Raised by the reviewer during F082's R23 closure review. The R23 block ordered three things that cannot all hold at once: the PR number appears in `.agent/handoff.md`, `gh pr create` runs AFTER C3, and no commit follows C3 because the STATUS edit must be the branch's last commit (Rule A4). The handoff is written inside C3, so the number does not exist when the file is authored and no later commit may add it. The worker declared the contradiction before the reviewer read the diff, wrote the handoff without inventing a number, named the recovery command, and reported the number in its final message; the reviewer recovered PR #201 with exactly that command and merged it at this round's Open PR Gate. This is R-0371 — never order a value that cannot exist when the text is written — recurring in the reviewer's own block one feature after R-0371 was registered for the same class, and it is the second such recurrence in R23 alongside R-0450. Low, because nothing false was written, the worker's declaration was correct, and the recovery is a single read-only command. Standing rule from here, binding the reviewer: before ordering any value INTO an artifact, name the commit that writes the artifact and the step that produces the value; if the producer is not strictly earlier than the writer, the block orders the value reported in the round's final message and orders the artifact to say so. OPEN.

- R-0450 — Low, A CARRIER FILE WHOSE OWN TEXT ORDERS AN APPEND THAT THE SAME BLOCK FORBIDS, SO THE CARRIER CANNOT CARRY. Raised by the reviewer during F082's R23 closure review. The CANDIDATES slice — authored by the reviewer and applied byte-verbatim into `.agent/candidates.md` — says "Every defect the closure round's worker declares in its handback is appended below, one line each", while the same block's Constraint 2 orders every slice applied BYTE-VERBATIM and its Constraint 3 forbids any commit after C3, which is the commit the file lands in. The worker declared two defects in its handback and appended neither, correctly giving the byte-verbatim constraint precedence and recording both as declared deviations instead. The result on disk is a carrier reading "no candidate was carried out of F082's closure review" at a head where two declared defects existed — which is the exact loss the F056-candidate operator ruling of 2026-08-01 created the carrier to prevent, arriving through the carrier's own text. Nothing was actually lost: the closure brief is the vehicle STATUS_closure_protocol.md prescribes, the file is only its disk backup for a session boundary this single-session run did not have, and the three findings registered in this round ARE those candidates. Low for that reason. Standing rule from here, binding the reviewer: a slice ordered byte-verbatim may not contain an instruction addressed to the worker about the file it lands in — instructions live in the block, never in the applied bytes — and a carrier file's text describes only what the file holds. OPEN.
--- END SLICE LIVEREVIEW-HEAD ---

--- BEGIN SLICE CTX --- (WHOLE FILE replacement of .agent/context.md, C2)
# Context — F083 CI self-check

## Active Branch
feature/f083-ci-self-check, cut from main at f3fd96d7 after PR #201 merged. F083
is claimed `[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR
exists for this branch yet; one is created at closure, not before.

## Scope
In: Remedy's own CI as one entrypoint plus thin hosted wrappers. Nothing is built
yet — this round only opens the record. The feature file T2_F083.md sets the
shape: `remedy ci [--stage NAME] [--json]` over the stages fast, standard,
determinism, ui and budgets; stages are MARKER SELECTIONS over the existing test
tree, not a new test organization; hosted workflow files call the same
entrypoint so there is one source of truth for what CI means; live-provider
tests and the F082 benchmark are excluded by marker and said so in the output
with their manual commands. Plus `.agent/**` round state and the one claimed
STATUS line.

Out: test contents, marker semantics, the bench's cost profile and release
packaging — the feature file's Do-not-touch list. CI never auto-retries a suite;
a flaky test is quarantined only by an explicit marker change in a reviewed diff.
A change that needs a test's CONTENT edited is a finding, not a fix.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/, and a round rewriting `.agent/` state also gates
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py, which read that state live.
  Destructive and red-proof checks run only inside a disposable git worktree
  under .remedy-wt/, so resource safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a round gate (R-0364); ruff is gated scoped to the files F083 owns.
- The reviewer measures its block mechanically on the final bytes before
  emission and keeps it under 400 lines (DECISION F105 D5), with 240 the
  preferred target so the block-save commit stays inside the 500-insertion
  limit (R-0381).
- R-0205 rides with this feature by the feature file's Carried findings section:
  contract tests that assert against LIVE `.agent/` state flip red for reasons
  unrelated to the round that trips them. Detecting a red main is this feature's
  own job, so the fixture-versus-live design question is answered inside it and
  not routed away.

## Steps
The round map is stated ONCE, in the Steps section of `.agent/live_review.md`,
and is deliberately not restated here: a map quoted in two places is the
contradiction R-0447 records. This file tracks scope and constraints only.
--- END SLICE CTX ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C2)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0451. Open findings: seventy-eight — the
seventy-five carried out of the F082 record, plus R-0448, R-0449 and R-0450
registered at R1. `.agent/live_review.md` is the source of truth; this file
mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure in
each stage fails the right stage with a readable summary, and total runtime
stays within a documented budget.

## Current Step
R1 is the CLAIM: cut the branch, reset the live review record carrying F082's
open set forward, register the three F082 closure-review candidates as R-0448,
R-0449 and R-0450, refresh the candidates carrier, and move the ledger line from
`[ ]` to `[~]`. No code and no test changes.

## Next Steps
1. R2 is the T001 marker inventory, which the feature file's orchestrator brief
   names as T001's first deliverable: collected count and wall time per marker,
   which markers already exist, and which stage each belongs to.
2. The stage split follows that data. No stage runner is written before it.

## Risks
- The three findings registered this round are all defects in the reviewer's own
  block text, and two of them, R-0449 and R-0450, are recurrences of R-0371 in
  the round that registered it. The counter-measures are written as standing
  rules inside the findings; whether they hold is measurable only in later rounds.
- R-0448's repair edits `docs/roadmap/STATUS_closure_protocol.md`, a process doc
  F083 does not own, so it joins R-0403, R-0444 and R-0445 on the paydown queue.
  That queue has no owner yet and grows by one this round.
- R-0205 is carried into this feature by its own feature file: live-state
  contract tests can turn main red for reasons unrelated to the change under
  review. It is in scope here rather than deferred.
--- END SLICE PLAN ---

--- BEGIN SLICE CANDIDATES --- (WHOLE FILE replacement of .agent/candidates.md, C2)
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

The carrier is empty. The three candidates F082's closure review produced were
registered as R-0448, R-0449 and R-0450 in `.agent/live_review.md` at F083 R1,
which is what the closure protocol asks the next feature's first reviewed round
to do.
--- END SLICE CANDIDATES ---

--- BEGIN SLICE STATUSLINE --- (in docs/roadmap/STATUS.md, C2 — REWRITE pair, FROM and TO disjoint)
- [ ] F083 — CI self-check
--- BEGIN SLICE STATUSLINE-TO --- (C2)
- [~] F083 — CI self-check
--- END SLICE STATUSLINE-TO ---

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and after the last.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and again at handback (R-0347).
 2. BRANCH and BASE: report `git branch --show-current` and `git rev-parse HEAD`
    taken after the checkout and before C0a, and whether the head equals
    f3fd96d729c3be85604a2d37aee42c59fe39868a.
 3. TRANSPORT, bytes read in Python: report sha256, byte count and line count of
    `.remedy-wt/.cache/f083-r1/f083-r1.md`, `.agent/authored/f083-r1.md` and
    `.agent/last_block.md`, whether all three byte strings are EQUAL, and whether
    the measured line count equals this block's declared footer count.
 4. C1 REBUILD PROPERTY, proven by reconstruction, not by reading: in Python,
    read `.agent/live_review.md` at BASE, build `carried` by the rule stated
    above, build `expected` by the formula stated above, and report whether
    `expected` byte-equals `.agent/live_review.md` at the C1 head. Report the
    count of carried paragraphs and the sha256 of the committed file. Extract
    LIVEREVIEW-HEAD out of the COMMITTED `.agent/authored/f083-r1.md` by its
    markers — never retype it.
 5. C1 CONTENT COUNTS at the C1 head: `^- R-\d+ — ` count, `^Done: R-\d+ — `
    count, `^Landed: ` count, `^Gate: ` count, the max id, the next free id, and
    any duplicate id. Report what you MEASURE; if it differs from seventy-eight
    registered and zero resolved, say so rather than reconciling it.
 6. C2 WHOLE FILES: `.agent/context.md`, `.agent/plan.md` and
    `.agent/candidates.md` at the C2 head each byte-equal their slice — report
    sha256 and line count for each, `.agent/plan.md` under 50 lines with `## Goal`
    and `## Next Steps` both present.
 7. C2 STATUS PAIR: report the FROM count in `pre`, the FROM count in `post`, the
    TO count in `post`, `FROM in TO`, and `pre.replace(FROM,TO) == post`. Then at
    HEAD report `^- \[ \] F083` 0x, `^- \[~\] F083` 1x, the count of ALL
    `^- \[~\] ` lines, and the count of `^- \[x\] ` lines, which the reviewer
    measured at 49 before this round and which must not change.
 8. VERIFICATION, each command run separately with its exit code read from the
    process, never from a pipe (R-0438). Report collected count and real exit
    code for EACH: `python3 -m pytest tests/docs/ -q` — the reviewer measured 295
    collected, 295 passed, exit 0 at BASE; `python3 -m pytest
    tests/regression/test_resource_safety.py -q` — 21 passed, exit 0 at BASE;
    `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` — 15
    passed, exit 0 at BASE; and the canary `python3 -m pytest
    tests/cli/test_golden_path.py -q` — 42 collected, 42 passed, exit 0 at BASE.
    The three non-canary targets are this round's real check: they read
    `.agent/` state and the ledger live, which is exactly what this round rewrites.
 9. INTEGRITY GATE, in Python because the `remedy` CLI is denied in this session
    class (R-0408): `python3 -c "from packages.orchestration.integrity_gate
    import run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count` and every named check's status and
    message. The reviewer measured 5 checks, `fail_count` 0 at BASE.
10. CHANGE SET, measured BEFORE the handoff is written into C3:
    `git diff --name-only f3fd96d729c3be85604a2d37aee42c59fe39868a..HEAD`. Report
    the full list and its count. Restricted to `packages/`, `apps/`, `scripts/`
    and `tests/` it must be EMPTY; restricted to `docs/` it must be EXACTLY ONE
    file, `docs/roadmap/STATUS.md`. Report both restrictions as measured lists.
11. Insertions (`+` column only) per commit — report each; none over 500. C0b and
    C1 are verbatim single-`.agent/`-file rewrites and are exempt by the AGENTS.md
    counting rule; report their numbers anyway.
12. PUSH: `git push -u origin feature/f083-ci-self-check` and report its result.
    Create NO pull request (Constraint 4); report that `gh pr list --state open`
    is empty afterwards.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as
C3 — feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and the next expected action. C3 cannot table its own
SHA (R-0371, R-0149); say so rather than inventing one. Repeat this line verbatim
as the Fortschritt line:

Fortschritt: 0 % (F083 beansprucht · Record zurückgesetzt, 75 offene Funde übernommen · R-0448 bis R-0450 registriert · T001–T003 offen · noch kein Code) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 313 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
