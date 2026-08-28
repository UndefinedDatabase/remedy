### STEP T002 — F257 Self-use track, round 6 (THE INTEGRATION GATE)

Goal: book the round 5 verdict and RUN THE INTEGRATION GATE — the full-suite
tier-3 run that must PASS before F257 may close. This round writes no production
code; its deliverable is the gate's real evidence, committed.

Base: `c3f8d5fe`, the tip of `feature/f257-self-use-track` and the handback this
round starts from. Merge base with `main`, measured by the reviewer at that tip:
`f17b1d0d03e4042df8452b2019b719cbe4704b21`. The suite collects 18206 tests
there; both runs below are LONG, and that is expected, not a fault.

THE CANONICAL PROCEDURE IS `docs/agents/integration_gate.md`. READ IT IN FULL
BEFORE STARTING. This block does not restate it; it binds you to it and adds only
the six adaptations below that this session's guard and this feature require.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r6.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R5 verdict into `.agent/live_review.md` and append two
  reviewer-prose slips to `.agent/prose_slips.md`
- C3 the gate evidence under `.agent/gate_f257_r6/`
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r6.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `.agent/gate_f257_r6/**`
- `.agent/handoff.md`

NO file under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/` is edited by
this round. If the gate finds a defect, you do NOT fix it here: you STOP and hand
back, because a fix is its own reviewer-gated round — `docs/agents/integration_gate.md`
step 4 says so in as many words.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `c3f8d5fe`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch except the throwaway base-gate
   branch constraint A2 requires. Create no pull request. Never force-push and
   never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r6.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through a scratch script under the
   gitignored `.remedy-wt/`, set variables in-process with `os.environ[...]`,
   and copy with `shutil.copyfile` / `shutil.copytree`. Capture real exit codes
   with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`. This Python
   is 3.10: an f-string expression may not contain a backslash, so hoist any
   regex into a named variable. Report every re-expression.
6. THE APPEND CONVENTION: an appended slice is separated from the text before it
   by exactly ONE BLANK LINE and the file ends with exactly one trailing
   newline. Concretely, for a target whose last byte is already a newline, write
   one newline then the slice, the slice carrying its own single terminator.
   This constraint is the authority on separators; if a gate formula below
   disagrees, follow this constraint and declare the disagreement.
7. THE OPEN SET IS COUNTED BY DISTINCT ID, as
   `len(set(registered ids) - set(resolved ids))`. It reads 254 at `c3f8d5fe`.
   This round registers NO id and resolves none, so it must read 254 at C2 too.

### The six adaptations to `docs/agents/integration_gate.md`

A1. RUN LOGS ARE WRITTEN OUTSIDE THE REPOSITORY, then copied in. The procedure's
step 2 forbids a log growing INSIDE the repo during a run — it changes the
worktree digest mid-run and produced four false manifest-identity failures at
R-0176. This session's guard rejects a bare `/tmp` shell write, so create the
scratch directory IN-PROCESS with `tempfile.mkdtemp()` and write both run logs
there. Copy them into `.agent/gate_f257_r6/` with `shutil.copyfile` only AFTER
the run has exited. Evidence files are named `.txt`, NEVER `.log`: `.gitignore`
drops `*.log` silently and the review-zip guard rejects any member matching
`\.log$` (R-0169).

A2. THE BASE WORKTREE IS CREATED ON A BRANCH, NOT DETACHED:
`git worktree add -b tmp/f257-base-gate .remedy-wt/f257-r6-base f17b1d0d`.
The self-dogfood branch guard refuses a detached HEAD BY DESIGN, so a detached
base worktree fails the guard-dependent ids and poisons the comparison
(DECISION D3, F053 R2). Afterwards remove the worktree, prune, DELETE the
throwaway branch, and prove all three with `git worktree list` and
`git branch --list 'tmp/*'`.

A3. RESTORE BUILD PARITY BEFORE THE BASE RUN, BY COPY AND NEVER BY SYMLINK. The
throwaway worktree has no build outputs, so copy the primary checkout's
`apps/ui/node_modules` (305 MB, measured by the reviewer — this takes minutes,
which is expected) and `apps/ui/dist` into it with `shutil.copytree`. NEVER
symlink them: the UI auto-build runs npm install and writes THROUGH a symlink
into the primary checkout (F053 R3 evidence). Set
`REMEDY_UI_NO_AUTO_BUILD=1` in-process for the base run, but do NOT trust it
alone — a spawned build path ignored it once (R-0169).

A4. VERIFY THE NEUTRALISATION BY MEASURING THE EVENT, NOT THE OUTCOME (R-0444,
recurring at F009 R29). Record the mtime of EVERY file under the base
worktree's `apps/ui/dist` immediately before the base run and again immediately
after, together with the run's own start and end timestamps. Report the window.
ANY mtime falling inside the run window VOIDS the parity claim and forces
per-id attribution instead. A content hash may accompany that reading but never
stands alone: equal content is consistent both with no rebuild and with a
byte-identical one, which is the case F009 R29 actually hit.

A5. THE COMPARISON IS A SET DIFFERENCE, AND YOU ORDER THE PROPERTY, NOT THE
TOOL. The procedure names `comm -13` / `comm -23`; this session's guard rejects
the pipelines that feed them. Compute the same two sets in Python from the two
`FAILED` id lists — branch-only = `set(branch) - set(base)`, base-only =
`set(base) - set(branch)` — and say in the handback that you computed the set
difference rather than running `comm`. Sort both lists before writing them to
`branch_failed.txt` and `base_failed.txt`.

A6. TESTS THAT DO NOT EXIST AT BASE ARE NOT BASE FAILURES. `f17b1d0d` predates
this feature, so `tests/orchestration/test_self_use_job.py` and
`tests/orchestration/test_self_use_queue.py` are ABSENT there. Their ids can
therefore appear as branch-only, and they are NEW TESTS, not regressions —
report them as their own class, separately from any genuine branch-only failure,
and state for each that the file does not exist at the base revision (prove it
with `git cat-file -e f17b1d0d:<path>` and its non-zero exit).

### The known flake you are likely to meet

R-0734, registered at `c3f8d5fe`, is a server-start race in
`tests/ui_server/test_command_channel.py`: its `_start_server` helper polls
`Path(info_file).exists()` and then parses the file inside that branch, so a poll
landing before the server finished writing reads zero bytes and raises
`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`, which
escapes the retry loop. It fired once during F257 R3 and was green on re-run,
green at base, and green on the reviewer's independent re-run. If it fires again:
CLASSIFY it per `docs/agents/integration_gate.md` step 4 — serial re-run of the
exact node id — record it as the already-registered R-0734, and do NOT repair it.
Repairing it here would edit `tests/ui_server/`, which this round's change set
forbids. It is not a blocker; an UNCLASSIFIED failure would be.

### The authored slices

<<<SLICE PLANF257R6
# Plan — F257 Self-use track

Branch: feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220. F257 was claimed by Rule A5 as the first unchecked line in
`docs/roadmap/STATUS.md` after F256.

## Goal
Remedy is used on Remedy on a schedule that cannot be skipped: a curated queue
of small maintenance jobs, exactly one consumed per feature close, run through
`do job-plan` and `do job-run` against this repository and taken to the normal
approval gate.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the queue file and its read-only loader | done | round 2, 18 tests |
| render a queue item and plan it on the real job path | done | round 3 |
| refuse a job file written outside its destination | done | round 4, R-0733 |
| consume exactly one item per feature close | done | round 4, precondition 6 |
| refuse an id that is not one file name | done | round 5, R-0735 |
| document the format where a reader looks | done | round 5 |
| the integration gate | in progress | this round |
| the closure package and the STATUS line | open | needs the gate to PASS first |

## Next Steps
1. Build the closure package once the reviewer passes the integration gate.
2. Close F257 through docs/roadmap/STATUS_closure_protocol.md, satisfying its
   new precondition 6 — this feature is the first that must consume a self-use
   item at its own close.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 is a registered ui_server flake that may fire in a full-suite run; it is
  classified, never repaired on this branch.
<<<END PLANF257R6

<<<SLICE GATEF257R5
Gate: F257 R5 — the DOCUMENTATION round, which closed R-0735, shipped the self-use track's reference page and registered it in the docs index. THE ROUND PASSED. The reviewer re-ran every gate G1 through G8 independently at `c3f8d5fe`: transport EQUAL at sha256 `9434d5f1…13aa944` over 29290 bytes with one blob id at C0b; the plan byte-equal at 1768 bytes and 37 lines; both record appends reconstructing to 1393448 bytes with the negative control failing as it must and the two prose-slip lines landing exactly; the ledger moving 295 → 296 registered and 253 → 254 open with `Done:` and `Landed:` unmoved and `Gate:` 109 → 110; both structural residues empty; six single-parent commits under 500 insertions; delimiters 0 in all seven targets against a 9/9 control.

THE DOCS TRANSPORTED BYTE-FOR-BYTE, PROVED AGAINST AN INDEPENDENT APPLICATION. Before delegating, the reviewer applied both authored pairs to its own copy of `docs/README.md` and kept both that result and the DOCPAGE slice. The C4 blob of `docs/README.md` is BYTE-IDENTICAL to the independently applied text, and the C4 blob of `docs/system/self-use-track-v1.md` is BYTE-IDENTICAL to the authored slice. The new page did not exist at the base revision, its one relative link `../roadmap/STATUS_closure_protocol.md` resolves, and `system/self-use-track-v1.md` appears exactly twice in the index — the quick-find row and the system table row.

THE FIX WAS RUN, AND R-0735 IS GONE. At `c3f8d5fe` the reviewer called the shipped `write_self_use_job_file` with the id that leaked at `f594cf3b`: `x/../SU-001` now raises `SelfUseJobError` rather than `FileNotFoundError`, and so do `..`, `.`, `sub/dir`, `../../escaped`, an absolute `/tmp/abs` and `./SU-001` — every one owned by the module rather than by pathlib. A valid `SU-001` still plans end to end against the shipped queue at `job_title` `Document the Markdown job-file format`, and the queue file is byte-unchanged after two full runs.

THE GATE NOW DISCRIMINATES, WHICH WAS THE POINT. At `f594cf3b` a mutation swapping the resolved comparison for an unresolved one left the suite green; that hole is closed. In its own worktree at `26c953ce` the reviewer measured: control 18 passed at exit 0; deleting the new single-component check gave exit 1 at 4 failed — the R-0735 regression; deleting the containment check gave exit 1 at 1 failed, so the symlink backstop is pinned by exactly one test; breaking the verbatim-bytes rule gave exit 1 at 2 failed; and a fourth mutation of the reviewer's own, dropping only the explicit `..` arm, gave exit 1 at 1 failed. Four mutations, four reds, control green before and after. All eight ordered suites re-ran green in the primary, `tests/docs/test_docs_consistency.py` at 295 passed among them.

THE WORKER CORRECTED THE BLOCK AUTHOR AND WAS RIGHT TO. S2 asserted that `Path("..").name` is the empty string, so that a single name comparison would refuse `..` on its own. It is not: it is `".."`, which the worker measured and the reviewer confirmed independently. Implementing S2 literally left a test red, so the worker added the explicit `entry.id in (".", "..")` arm and declared the deviation rather than quietly widening or narrowing the check. It also added a symlink test beyond S4's list, on the correct ground that without one the containment mutation would have gone green — the discriminator argument, made unprompted for the second round running. Both are booked as reviewer-prose slips; nothing wrong reached disk.
<<<END GATEF257R5

<<<SLICE SLIPSF257R5
2026-08-29 · F257 R5 · The block's S2 asserted that `Path("..").name` is the empty string and that a single-component comparison would therefore refuse `..` unaided; it is `".."`, the worker measured it, and the explicit `entry.id in (".", "..")` arm it added is what makes the shipped check correct.
2026-08-29 · F257 R5 · Constraint 8's own summarising sentence — "one newline, then the slice, then one newline" — would leave every appended file ending in two newlines; the clauses around it are right, the worker followed those, and every append since round 3 has reconstructed byte-exactly.
<<<END SLIPSF257R5

`PLANF257R6` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R5` is an
APPEND to `.agent/live_review.md` and `SLIPSF257R5` an APPEND of TWO LINES to
`.agent/prose_slips.md`, each under constraint 6. This round mints no finding id
and resolves none.

### The evidence C3 commits, under `.agent/gate_f257_r6/`

- `branch_run.txt` — the branch run's raw tail, its full `FAILED` list, its REAL
  exit code and its wall time.
- `base_run.txt` — the same for the base run at `f17b1d0d`.
- `branch_failed.txt` — the sorted `FAILED` node ids from the branch run, one
  per line; empty file if there were none.
- `base_failed.txt` — the same for the base run.
- `comparison.txt` — the two set differences A5 defines, the new-test class A6
  defines, and one attribution paragraph per branch-only id.
- `parity.txt` — A4's mtime readings: every file under the base worktree's
  `apps/ui/dist` before and after, the run window, and the verdict on whether any
  mtime fell inside it.

Write real measured content into each; a placeholder is a finding.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three
readings and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2
and C3.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r6.md` and of the reviewer's
own original at `.remedy-wt/f257-r6-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r6.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R6 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE RECORD APPEND AT C2. Reconstruct the C2 blob of `.agent/live_review.md`
from the `c3f8d5fe` blob plus GATEF257R5 under constraint 6 and report `True` or
`False` with all three lengths. NEGATIVE CONTROL: flip one byte at an offset your
script confirms lies INSIDE the FIRST appended paragraph, recompute, and report
the equality is now `False`. Report that the pre-round blob is a byte PREFIX,
with both lengths, and that the C2 blob ends in exactly ONE newline. Report
separately that `.agent/prose_slips.md` at C2 reconstructs from its `c3f8d5fe`
blob plus SLIPSF257R5, and that SLIPSF257R5 contributed exactly TWO lines.

G5 THE LEDGER AT C2, counted under constraint 7. Report over
`.agent/live_review.md` at `c3f8d5fe` and again at C2: the count of lines
matching `^- R-\d+ — ` and whether all are DISTINCT; the count of
`^Done: R-\d+ — ` lines AND the count of DISTINCT ids among them, as two
separate numbers; the count of `^Landed: R-`; the count of
`^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered UNMOVED at 296,
`Done:` and `Landed:` UNMOVED, `Gate:` 110 → 111, and the open set UNMOVED at
254 on BOTH sides. Report the count of `^Gate: F257 R5 — ` at C2, which must
be 1.

G6 THE INTEGRATION GATE, run per `docs/agents/integration_gate.md` as adapted by
A1 through A6. Report, as separate labelled readings:
(a) THE BRANCH RUN — the exact command, its REAL exit code, its wall time, its
raw tail, and its complete untruncated `FAILED` list.
(b) THE BASE RUN at `f17b1d0d` in the throwaway worktree on branch
`tmp/f257-base-gate` — the same four readings, plus proof that the worktree was
created ON A BRANCH and not detached.
(c) PARITY, per A4 — the before and after mtime readings over the base
worktree's `apps/ui/dist`, the run window, and whether ANY mtime fell inside it.
State plainly whether the parity claim holds or is void.
(d) THE COMPARISON, per A5 — branch-only ids and base-only ids as set
differences, each list complete and untruncated, and the sentence saying you
computed a set difference rather than running `comm`.
(e) THE NEW-TEST CLASS, per A6 — the ids whose FILE does not exist at
`f17b1d0d`, with the `git cat-file -e` proof per file.
(f) ATTRIBUTION — for EVERY remaining branch-only id, a serial re-run of the
exact node id with its REAL exit code, and its classification: serial-pass ⇒
xdist-flake, recorded not blocking; serial-fail ⇒ reproduce at the merge base
before blaming the feature; a reproducible branch-only failure coupled to
feature code ⇒ BLOCKER, at which point you STOP and hand back.
(g) THE BUDGET — total wall clock for both runs.
DO NOT ISSUE THE GATE VERDICT. `docs/agents/integration_gate.md` step 5 reserves
it to the reviewer. Report the readings and say explicitly that the verdict is
the reviewer's.

G7 STRUCTURE, over `c3f8d5fe..<C3>` — the range that ends BEFORE the handback
commit, because C4's own numbers cannot exist while C4 is being written. The
change set lists `.agent/handoff.md`, which C4 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that path and name the
path you excluded; the range-minus-changeset residue is computed against the
full change set and must be empty, treating `.agent/gate_f257_r6/**` as matching
any path under that directory. Report each commit's insertions from
`git diff --numstat`, and that each of C0a, C0b, C1, C2 and C3 is single-parent.
C3 may exceed 500 insertions if the raw logs are large: if it does, DECLARE it in
the handback with the inseparability reason per AGENTS.md's oversize-commit
exception, because a gate's evidence is one indivisible artifact. Report,
counted affirmatively over each file's C3 content, the number of lines beginning
`<<<SLICE ` and `<<<END ` in `.agent/plan.md`, `.agent/live_review.md` and
`.agent/prose_slips.md` — each expected 0 — beside the same counts over
`.agent/authored/f257-r6.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0. Report that NO path under
`packages/`, `apps/`, `tests/`, `scripts/` or `docs/` appears in the range —
list the range's paths in full to show it. Report that no committed evidence
file name matches `\.log$`. Finally report `git worktree list` and
`git branch --list 'tmp/*'`, both of which must show the base-gate worktree and
its throwaway branch GONE.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F257 · round 6`; the range `c3f8d5fe..HEAD`; a
per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat`; ONE LINE PER GATE G1 through G7 with its real result; the
deviations, including every guard re-expression constraint 5 required; the
item-status table with every C-item and every gate appearing exactly once; the
open-findings count, which must be 254; and the next expected action.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R5 is
reviewer-authored text you apply verbatim, and any OTHER such paragraph is a
finding however hedged. Do not issue the integration-gate verdict.

After C4: push with `git push origin feature/f257-self-use-track` and report the
outcome. Do NOT create a pull request and do NOT merge anything.
