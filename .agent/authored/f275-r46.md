── STEP T003 / round 46 — F275 ───────────────────────────────
Goal:        Book round 45's PASS verdict and R-0875's resolution, then record what a
             dry run of THE FLIP measured at this round's base: it does not converge as
             one mechanical commit, and the largest unruled class is the id SHAPE, which
             reaches three pydantic models no artefact of this feature enumerates.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r46.md`
             C0b  mirror it into `.agent/last_block.md` from the committed blob
             C1   slice PLAN46 — whole-file replacement of `.agent/plan.md`
             C2   slice RECORD46 — append two paragraphs to `.agent/live_review.md`
             C3   slice ARTEFACT46 — create `.agent/f275_t003_flip_residue.md`
             C4   slice DECIDE46 — append DECISION F275 D26 to `.agent/decisions.md`
             C5   the handback, rewriting `.agent/handoff.md`

Change:      EXACTLY the paths listed here and nothing else.
             `.agent/authored/f275-r46.md`          (new)
             `.agent/last_block.md`
             `.agent/plan.md`
             `.agent/live_review.md`
             `.agent/f275_t003_flip_residue.md`     (new)
             `.agent/decisions.md`
             `.agent/handoff.md`
             NO path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moves
             this round. This round lands no production line and no test line.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never edit, reflow, re-wrap or retype one. If a
    slice looks wrong, apply it as given and DECLARE it in the handback. Extract each
    slice mechanically from the COMMITTED block blob by its `BEGIN-`/`END-` marker
    lines; never retype a slice from the prompt.
 2. The commit order C0a, C0b, C1, C2, C3, C4, C5 is FIXED. None merged, none
    reordered, none added, none dropped.
 3. EVERY length in this round is `len(<bytes>)`, taken from `read_bytes()` or from a
    `git show` / `git cat-file` byte stream. Never `len()` over a decoded `str`: these
    files hold em dashes, and the two readings differ.
 4. The two appends are `old_bytes + slice_bytes` in Python, nothing inserted. Each
    append slice OWNS its leading blank line, which is the separator the target's record
    format uses between entries. Both pre-blobs end in a newline; add none.
 5. This round RESOLVES `R-0875` and REGISTERS nothing. The `Landed: R-0875` line is NOT
    edited, moved or removed — the record is append-only, and a `Landed:` line standing
    beside its `Done:` paragraph is the intended state, not a leftover.
 6. `.agent/f275_t003_flip_residue.md` is a NEW file. Write it with a whole-file write of
    the slice's bytes; do not append to anything and do not create any other file. In
    particular do NOT commit a `.py` file anywhere: no `.agent/**.py` is tracked today,
    and seven suites sweep `git ls-files '*.py'`. The instrument lives INSIDE the
    artefact as a fenced block, which is the convention the three sibling artefacts set.
 7. Any destructive or exploratory run happens ONLY in a disposable `git worktree` under
    the gitignored `.remedy-wt/`, removed and pruned before the handback. The primary
    checkout satisfies `git status --porcelain` == empty at every commit.
 8. Re-read `.agent/STOP` FROM DISK before the first commit and report what you found.

Done when:   the gates below, each run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
             one line per gate in the handback, EVERY reading taken at C4 or earlier —
             C5 writes the handback and cannot quote a number that does not yet exist.
             Report the number of gates YOU ran; this block states none.

 G1  TRANSPORT, at C0b. sha256 over the bytes of `.agent/authored/f275-r46.md` equals the
     digest in this block's BEGIN marker. `.agent/last_block.md` is written from
     `git cat-file blob <C0a-sha>:.agent/authored/f275-r46.md` and never retyped; report
     both byte counts and both digests. State the chain the proof walked — the saved
     copy, its mirror, the working copy — and claim nothing about the bytes emitted into
     your prompt, which nothing in this workflow can measure.

 G2  THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to slice PLAN46: report both byte
     counts and both sha256 digests. Report its line count against the AGENTS.md cap of
     50. `^## Goal$` occurs exactly 1x and `^## Next Steps$` exactly 1x.

 G3  THE RECORD, at C2, over COMMITTED blobs only. Read the pre blob at C1 and the post
     blob at C2 with `git show <sha>:.agent/live_review.md` into memory — never by writing
     a non-current revision over the tracked file, which guardrail G5 of
     docs/agents/self_drive_protocol.md forbids outright.
     (a) reader A: pre_bytes + slice_bytes == post_bytes, reported as `identical: True`.
     (b) reader B, independent and structural: N is the number of blank-line-separated
         paragraphs your script COUNTS IN THE SLICE — never a number this block asserts —
         and the LAST N blank-line units of the post blob equal the slice's N paragraphs
         IN ORDER, compared with boundary whitespace stripped.
     (c) negative control: flip ONE byte inside the FIRST appended paragraph OF THE
         IN-MEMORY COPY — no file on disk is touched by this reading, and the working tree
         is never the subject of it — and report that reader A rejects AND reader B
         rejects. A control on the last paragraph proves nothing about the first.

 G4  THE NEW ARTEFACT, at C3. `.agent/f275_t003_flip_residue.md` is BYTE-EQUAL to slice
     ARTEFACT46: report both byte counts and both sha256 digests, and its line count.
     Report that `git cat-file -e C2:.agent/f275_t003_flip_residue.md` FAILS — the path
     does not exist one commit earlier — so the file is a creation and not an overwrite.

 G5  THE DECISIONS, at C4. The same three readings as G3, over `.agent/decisions.md`,
     pre at C3 and post at C4, with the negative control again on the FIRST appended
     paragraph.

 G6  THE OPEN SET AND THE COUNT GATE, at C4, over `.agent/live_review.md`. Derive the open
     set BY DISTINCT ID and mechanically: distinct `^- R-\d+ — ` minus distinct
     `^Done: R-\d+ — `. At the base `978046fe` that is 104 − 17 = 87; at C4 it must be
     104 − 18 = 86. Report the ids REGISTERED this round, which is the empty list, and the
     ids RESOLVED, which is `['R-0875']`. Then four counts, each read at C1 and again at
     C4: `^Gate: F275 R45 ` 0 then exactly 1; `^Done: R-0875 ` 0 then exactly 1;
     `^Landed: R-0875 ` exactly 1 then exactly 1, UNCHANGED by any slice, which is
     constraint 5 measured rather than promised; and `R-0876` ABSENT at C4, so the next
     free id stays free.

 G7  THE PREMISES REPRODUCE, at C4. Extract the fenced python block that follows the line
     `<!-- INSTRUMENT -->` in the COMMITTED C3 blob of
     `.agent/f275_t003_flip_residue.md`, write it to the gitignored `.remedy-wt/` and run
     it from the repository ROOT of the primary checkout with `python3 -B`. It writes
     nothing. Report its WHOLE stdout and REAL_EXIT, and compare it LINE BY LINE against
     the recorded output in section 6 of the artefact — every line of the two must be
     byte-identical, and the readings that carry the decision are P1's four annotations,
     P2's `53` and `6` with its six model names, P3's `51 sites in 30 files, production
     files 0`, and P4's `397 sites in 154 files, production files 55`.
     The FIRST line is the one exception and the artefact says so. Its
     `tracked .py from git ls-files` count reads 993 in the artefact and must still read
     993 at C4, because constraint 6 commits NO `.py` file; its `instrument reads itself`
     half must read `False`, because you write the instrument to the gitignored
     `.remedy-wt/` where `git ls-files` cannot see it. Report both halves.
     If any reading differs, do NOT edit the slice: report both values and declare it.

 G8  NOTHING ELSE MOVED, at C4. `.agent/STOP` ABSENT from disk, re-read and not
     remembered. `git status --porcelain` EMPTY, reported as the literal string.
     `git worktree list` exactly ONE entry. The changed-path set over `978046fe`..C4
     equals the Change list EXACTLY: report MISSING and EXTRA as lists, both `[]`. ZERO
     paths under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`. Report each of
     C0a..C4's own insertion count against the F104 D1 cap of 500; C5's own number is
     not orderable here and belongs to the next round's ledger entry. Those insertion
     counts land TWICE — here, and in the `+/-` column of the handback's `## Commits`
     table that docs/agents/handback_template.md mandates. Derive them ONCE, from
     `git show --numstat <sha> -- <path>`, and fill both from that reading; a whole-file
     rewrite is exactly where a line-count-before-and-after diverges from what `numstat`
     reports, and the table is the half a later session reads.

 No pytest command is ordered this round and no canary is owed: the change set holds no
 production line, no test line and no import, so there is nothing for a suite to reach.
 That is stated rather than left out, because a missing canary is normally a finding.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 19 of F275,
             round 46, the item-status table with every ordered item exactly once, the
             deviations, and one sentence of context self-assessment.
──────────────────────────────────────────────────────────────

WHY THIS ROUND IS NOT THE FLIP, in one paragraph, because the handback you are replacing
says the next round IS the flip. It said so honestly: at the close of session 18 the flip's
target API existed, its record shapes were measured, its construction mapping was ruled and
the tree was green. Before authoring it, this reviewer did what the standing rule requires
and APPLIED it in a disposable worktree at `978046fe` and RAN it. It does not converge. The
tree it produces is parseable and collects 18394 tests with zero collection errors, and the
suite then reads 2714 failed and 106 errors. The artefact below records that run, its
classification and the two rules the transform still lacked; DECISION F275 D26 records what
follows from it. Nothing about F275's route changes: the flip is still F275's one declared
oversize commit. What changes is that it is not the NEXT commit, and the reason is measured
rather than felt.

────────── SLICES ──────────
The authored texts follow, in the order their commits apply them: PLAN46, RECORD46,
ARTEFACT46, DECIDE46. Each is delimited by its own `BEGIN-`/`END-` marker lines; the marker
lines are NOT part of any slice and never reach a target file. Extract each slice from the
COMMITTED blob of `.agent/authored/f275-r46.md` by those markers, matching a marker by its
`BEGIN-<name> ` or `END-<name> ` PREFIX. Every rule line in this block's frame is a run of
U+2500 BOX DRAWINGS LIGHT HORIZONTAL, and no rule LENGTH is load-bearing anywhere: markers
are matched by prefix, and the STEP frame carries no appliable bytes at all.

The pair shape of each slice, from the mechanical reading and not by eye. PLAN46 is a WHOLE
FILE REPLACEMENT and no containment question arises. RECORD46, DECIDE46: appends, applied as
`old_bytes + slice_bytes`, so no FROM string exists and no FROM-zero count is orderable.
ARTEFACT46 is a CREATION into a path that does not exist at C2, which G4 measures.

BEGIN-PLAN46 ─────────────────────────────────────────────────
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 46 books round 45's PASS verdict and the resolution of R-0875, and records what a DRY
RUN of the flip measured at `978046fe`. Applied as a mechanical `ast` transformation the flip
produces a parseable tree that collects 18394 tests with zero collection errors, and the suite
then reads 2714 failed, 15551 passed and 106 errors. The failures classify into six classes,
and the largest that no decision has ruled is the ID SHAPE: `Job.id` and `Task.id` are
`uuid.UUID` while the unified record spells both `str`, and that type reaches `Artifact`,
`TaskExecutionContext` and `PatchIntentSet` — three models no artefact of this feature
enumerates. DECISION F275 D26 records the finding and the route.

## Next Steps

1. THE ID-SHAPE MIGRATION, as its own commit or commits before the flip, on the pattern
   DECISION F275 D22 and D23 set: measure the sites, then widen. It is the prerequisite the
   flip's three enumerations each recorded as a bound and never sized.
2. THE FOUR TRANSFORM RULES the dry run added to DECISION F275 D25's two, all in
   `.agent/f275_t003_flip_residue.md` section 3: the seam's own imports move with the seam,
   a mixed import is SPLIT rather than moved, the type imports move their MODULE PATH, and a
   construction whose keywords arrive through a `**` splat is invisible to a keyword rewrite.
3. THE FLIP, once the classes above are gone from the dry run's residue, still as the one
   declared-oversize commit AGENTS.md permits per feature, declared with its inseparability
   reason before review.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store. Then the
   closure sequence: the integration gate, the evidence job, a fresh review zip, the ledger
   rotation, the STATUS line and the PR.

## Risks

- F275 stands at 46 rounds and 19 sessions against the operator's soft limit of 60 rounds and
  20 sessions. The NEXT session is the twentieth and owes a scope report under
  amend0908-f275-finish rule 1; that rule also forbids the split-and-close default here.
- The open set is 86 by distinct id once this round books `Done: R-0875`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN46 ───────────────────────────────────────────────────

BEGIN-RECORD46 ───────────────────────────────────────────────

Gate: F275 R45 — the F275 round 45 entry. VERDICT PASS, written by the planner and reviewer of session 18 after reading the committed range `123a0c3f`..`9310dc30` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Booked here by round 46's C2 from `.agent/handoff.md` as the durable carrier, per operator amendment amend0827-process-diet rule 1. THE BRANCH TIP IS GREEN AGAIN AND THE REVIEWER CONFIRMED IT FIRST: `tests/test_model_construction_keywords.py` reads `6 passed` at exit 0 in the primary checkout, against `1 failed, 4 passed` at exit 1 before that round. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback — the scratch original survived, was hashed BEFORE delegation at `e5b409f47c13ca3beba1ffd738428a2d887b7b58336cb5698d47bb2b267c3ecd`, and is byte-identical to both committed copies at 23302 bytes. G2: `.agent/plan.md` byte-identical to PLAN45 at 2642 bytes over 46 lines. G3: both appends reconstruct exactly — `.agent/live_review.md` 874338 to 878949 and `.agent/prose_slips.md` 236456 to 237582 — with reader B true at N counted from each slice and both negative controls rejected by BOTH readers with the flipped byte inside the FIRST appended paragraph; `^Gate: F275 R44 ` reads 1, `^Landed: R-0875 ` reads 1 UNCHANGED, and `^Done: R-0875 ` reads 0. G4: the open set is 87 BY DISTINCT ID at the base, at C3 and at the tip, over 104 registrations against 17 resolutions, with nothing registered and nothing resolved. G5 IS THE GATE THAT ROUND EXISTS FOR AND IT HOLDS AT THE STRENGTH THE PAIR DESERVES: the containment test's own output reads `TO contains FROM: False`, so PAIR45 is a REWRITE and the FROM-zero count applies — FROM reads exactly 1 in the committed BASE blob and 0 in the committed C3 blob, TO reads exactly 1, and the reviewer rebuilt the C3 blob from the BASE blob by applying the pair alone, byte-identical at 5498 bytes, 134 lines and sha256 `e0b29143eb63dba5723570a02cf694c40a242fe8dbad13d1351621db18ed0016`. G6's TWO red proofs were re-run by the reviewer in its own disposable worktree at C3 and they separate exactly as ordered: the control reads `6 passed` at exit 0, M1 putting a real offender back reddens `test_no_tracked_file_passes_an_undeclared_keyword`, M2 introducing the per-file exemption the repair rejected reddens `test_the_sweep_reads_this_file_too`, THE TWO NODE-ID SETS ARE DISJOINT, both reverts are byte-exact by sha256, the control is green again, and the PRIMARY checkout's porcelain read EMPTY in the same command sequence as every mutation. G7: an EXACT set match over six paths with MISSING and EXTRA both empty, nothing outside `.agent/` and `tests/`, and insertions 272, 186, 23, 4 and 21. THE REPAIR IS THE RIGHT SHAPE AND NOT MERELY A GREEN ONE: an exemption for the guard's own file was the obvious fix and was rejected on the record, because it would make the sweep PARTIAL and hand a later reader a hole to widen instead of an offender to fix. Passing the premise keywords as a `**{...}` splat keeps the sweep TOTAL, and it is not a dodge — the sweep's subject is the LITERAL keyword a reader sees and believes, a splat carries no `keyword.arg`, and M2 proves the new self-coverage test closes the exemption route the repair declined. NO FINDING IS REGISTERED BY THIS GATE AND ONE IS RESOLVED: `R-0875`, whose `Done:` paragraph this same commit appends.

Done: R-0875 — RESOLVED at F275 rounds 44 and 45, in two commits because the first was defective, and the resolution says so rather than reading as one clean landing. The DEFECT: forty keyword arguments passed to `Job(...)` and `Task(...)` named no field on either model, so pydantic's default `extra="ignore"` dropped every one, and forty call sites under `tests/` had never established the state their own keyword named — `Job(permissions=...)` at 6 sites, `Job(prompt=...)` at 5, `Task(task_type=...)` at 17, `Task(type=...)` at 8 and `Task(title=...)` at 4, with zero in production. THE FIX, at round 44's C3 `be83dc4c`: 35 keywords deleted and the 5 `prompt` keywords REPOINTED onto `user_prompt`, the field they plainly meant, which is a behaviour change ordered because it was measured green rather than because it read better. The reviewer re-ran the 24 cleaned files itself and read `1083 passed, 10 skipped` at exit 0, the figure the block stated, and confirmed by reading the BASE bytes through `ruff check --stdin-filename` that the two surviving `I001` findings both pre-date the round. THE GUARD, and why it took two commits: a runtime test cannot catch this class at all — the keyword is dropped silently, which is the whole defect — so the guard is a SOURCE sweep over every tracked `*.py` file, reading each model's declared field set by IMPORTING the shipped class rather than from a list of its own. As first landed that guard reported ITSELF, because its premise test wrote `Task(description="d", type="write_readme")` literally and the sweep reads the file it lives in; that is planner_reviewer_prompt.md §3 item 2, the reviewer's own defect, it left the branch tip RED for one round, and it is recorded as a dated line in `.agent/prose_slips.md` rather than a second id. Round 45's C3 `9310dc30` repaired it by passing those keywords as a `**{...}` splat — which the sweep skips for the right reason, its subject being the literal keyword a reader believes — and ADDED a test asserting the guard's own file is among the files the sweep reads, so the per-file exemption that was the tempting repair cannot arrive later by accident. Both halves are red-proved on the reviewer's own runs, over disjoint node ids: re-adding one deleted keyword reddens `test_no_tracked_file_passes_an_undeclared_keyword`, and introducing the exemption reddens `test_the_sweep_reads_this_file_too`. The guard reads `6 passed` at exit 0 at `9310dc30`.
END-RECORD46 ─────────────────────────────────────────────────

BEGIN-ARTEFACT46 ─────────────────────────────────────────────
# F275 T003 — the FLIP, APPLIED AND RUN: what its residue is

> Measured by the reviewer at `978046fe`, this round's base, in a disposable `git worktree`
> under the gitignored `.remedy-wt/`, removed and pruned before the block was authored.
> THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.

## 1. Why this reading was owed

`.agent/handoff.md` at `978046fe` names the flip as the next round's work and calls it "a
mechanical transformation with every prerequisite measured". Every clause of that sentence
was earned: DECISION F275 D23 widened in the store capabilities the flip's target lacked,
D24 proved the JOB record pair clean, and D25 ruled the construction mapping and recorded
two mechanical rules. What none of those rounds did is APPLY the flip and RUN the suite.
This file is that run — the fourth artefact of T003 and the first to execute rather than
enumerate.

## 2. The transform

Surgical text edits at `ast`-resolved `(line, column)` spans, right to left within each
line, so comments, blank lines and formatting survive. `ast.unparse` is not used: it
discards every comment, which would destroy this repository's WHY comments and redden the
guards that read source text. Edits are applied IN BYTES, because `ast` reports
`col_offset` as a UTF-8 byte offset — DECISION F275 D25's first mechanical rule. The six
rules already ruled by this chain:

    T1 type names `Job`->`JobPlan`, `Task`->`TaskEntry` · T2 job fields `.id`->`.job_id`,
    `.name`->`.job_title` (D24) · T3 task fields `.id`->`.task_id`,
    `.description`->`.title` (D25) · T4 ctor keywords `name=`, `description=`, `type=`,
    `task_type=`, `id=` · T5 the store seam (D23) · T6
    `<job>.created_at.isoformat()`->`<job>.created_at` (D24)

## 3. THE FOUR RULES THIS DRY RUN ADDED, each learned by failing

Recorded here rather than in DECISION F275 D26 because they are mechanics, not a choice.

**I1 — a type import moves its MODULE PATH, not only its name.** D25's second rule,
restated because implementing it exposed the three below. The unified record lives in
`packages.orchestration.pingpong_job`, so `from packages.core.models import Job` becomes
`from packages.orchestration.pingpong_job import JobPlan`.

**I2 — a MIXED import is SPLIT, never moved.** 358 `ImportFrom` nodes name `Job` or `Task`,
every one from `packages.core.models`, and 176 of those name a target BESIDE a non-target —
`RunState` at 103, `Artifact` and `ArtifactKind` at 29 more, and so on. Moving such a node's
module path wholesale takes the non-targets with it. The node becomes two statements: the
survivors keep the old module, the targets get the new one. Applied: 518 moved, 218 split.

**I3 — the SEAM'S OWN IMPORTS move with the seam.** Rewriting the CALL `save_job(...)` to
`save_job_plan(...)` while leaving `from packages.orchestration.storage import save_job`
standing leaves the new name unbound. The first dry run read exactly that, as `NameError:
name 'save_job_plan' is not defined`, and repairing it moved the suite from 2839 failed and
229 errors to 2714 failed and 106 errors — which is the honest size of this rule's effect
and the reason it is a rule rather than the cause.

**I4 — a construction whose keywords arrive through a `**` splat is INVISIBLE to a keyword
rewrite, and the transform does not yet see it.** `Job(**defaults)` where `defaults` is a
dict literal holding `"id"` keeps the classic key and the unified constructor refuses it. It
is the blindness a text sweep has to an argv-list invocation: the keyword is not a
`keyword.arg`, so no rewrite of `keyword.arg` reaches it. The sites are test helper
factories of the shape `def _make_job(**kw): defaults = {"name": ...}; defaults.update(kw);
return Job(**defaults)`, so the rule must reach the helper's dict literal AND its callers'
keywords — a call-graph pass, not a node rewrite. This class is the largest in the residue
at 867 failures and it is NOT what blocks the flip; see section 6.

## 4. What the applied transform did

| reading | measured |
|---|---:|
| files rewritten | 282 |
| files left unparsable by the edit | 0 |
| `git diff --shortstat` insertions | 5388 |
| `git diff --shortstat` deletions | 5230 |
| changed files under `packages/` or `apps/` | 110 |
| changed files under `tests/` | 172 |
| `pytest tests/ -q --co` collected | 18394 |
| collection errors | 0 |

Rewrites by rule, as the instrument counted them: import moved 518, import split 218, T1
type name 1236, T2 job field 1895, T3 task field 532, T4 `description` 247, T4 `id` 107, T4
`name` 539, T5 seam 779, T6 isoformat 6. Five paths are EXCLUDED because they define or
implement the classic record and its store rather than consume it —
`packages/core/models.py`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/storage.py` and `tests/test_storage.py`, of which four exist.

## 5. What the flipped tree then does

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly
    2714 failed, 15551 passed, 23 skipped, 1 warning, 106 errors in 1189.47s (0:19:49)
    REAL_EXIT=1

Classified by bucketing the run's own exception lines — the type, and the message with
quoted spans and digits normalised — over the 2563 lines the pattern matched:

| count | class |
|---:|---|
| 867 | `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` |
| 493 | `AttributeError: 'X' object has no attribute 'X'` |
| 271 | `TypeError: unsupported operand type(s) for /: 'X' and 'X'` |
| 256 | `ValueError: badly formed hexadecimal UUID string` |
| 241 | `pydantic ValidationError: N validation error for Artifact` |
| 128 | `pydantic ValidationError: N validation errors for TaskExecutionContext` |
| 14 | `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` |

## 6. THE PREMISES, and the instrument that re-measures them

The four readings DECISION F275 D26 rests on. P1 and P2 read the SHIPPED classes by
importing them, the convention DECISION F275 D22 and D24 set; P3 and P4 resolve a site by
`ast` over the files `git ls-files '*.py'` names, never by grep. Recorded output:

    tracked .py from git ls-files: 993 | instrument reads itself: False
    P1 Job.id <class 'uuid.UUID'> | JobPlan.job_id str
    P1 Task.id <class 'uuid.UUID'> | TaskEntry.task_id str
    P2 pydantic models under `packages.`: 53 | declaring a UUID-typed field: 6
       packages.core.models.Artifact ['id', 'task_id']
       packages.core.models.Job ['id']
       packages.core.models.Task ['id', 'output_artifact_ids']
       packages.orchestration.builder_models.TaskExecutionContext ['job_id', 'task_id']
       packages.orchestration.patch_intent.PatchIntentSet ['task_id', 'artifact_id']
       packages.orchestration.project_registry.RemyProject ['id']
    P3 splat constructions: 51 sites in 30 files, production files 0
    P4 seam imports: 397 sites in 154 files, production files 55

P1 AND P2 ARE WHY THE FLIP IS NOT THE NEXT COMMIT, and P3 is why the largest failure class
is not. A `**` splat is a transform rule: 51 sites, all under `tests/`, and every line they
touch is rewritten by the flip anyway, so nothing is owed to them ahead of it. THE ID SHAPE
IS NOT A RULE. `Job.id` is a `uuid.UUID` and `JobPlan.job_id` is a `str`, and three models
the flip never touches — `Artifact`, `TaskExecutionContext`, `PatchIntentSet` — declare that
type on a field the flip feeds. No rewrite of the classic record can satisfy them, and no
gate over a rename could see them, which is why this reading was owed before the commit and
not after it.

The instrument, so that this artefact is reproducible from itself. Run from the repository
root with `python3 -B`; it writes nothing.

<!-- INSTRUMENT -->
```python
"""F275 R46 — the four premises DECISION F275 D26 rests on, re-measured in one run.

P1 and P2 read the SHIPPED classes by importing them. P3 and P4 resolve a site by `ast`
over the files `git ls-files '*.py'` names, never by grep, so a name inside a comment or
a string is not a site. This probe WRITES NOTHING.
"""
import ast, collections, dataclasses, importlib, inspect, pkgutil, subprocess

CTOR = {"Job", "Task"}
SEAM = {"save_job", "load_job", "load_job_safe", "list_jobs", "list_jobs_safe",
        "resolve_job_id"}

paths = [p for p in subprocess.run(["git", "ls-files", "*.py"], capture_output=True,
                                   text=True).stdout.split() if p]
own = __file__.split("/")[-1]
print(f"tracked .py from git ls-files: {len(paths)} | instrument reads itself: "
      f"{any(p == own or p.endswith('/' + own) for p in paths)}")

from packages.core.models import Job, Task
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
jp = {f.name: str(f.type) for f in dataclasses.fields(JobPlan)}
te = {f.name: str(f.type) for f in dataclasses.fields(TaskEntry)}
print(f"P1 Job.id {Job.model_fields['id'].annotation} | JobPlan.job_id {jp.get('job_id')}")
print(f"P1 Task.id {Task.model_fields['id'].annotation} | "
      f"TaskEntry.task_id {te.get('task_id')}")

from pydantic import BaseModel
import packages
found = {}
for m in pkgutil.walk_packages(packages.__path__, "packages."):
    try:
        mod = importlib.import_module(m.name)
    except Exception:
        continue
    for obj in vars(mod).values():
        if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel:
            found[f"{obj.__module__}.{obj.__name__}"] = obj
hits = {}
for name, obj in found.items():
    u = [f for f, i in obj.model_fields.items() if "UUID" in str(i.annotation)]
    if u:
        hits[name] = u
print(f"P2 pydantic models under `packages.`: {len(found)} | "
      f"declaring a UUID-typed field: {len(hits)}")
for name in sorted(hits):
    print(f"   {name} {hits[name]}")

splats, seam_nodes = [], []
for rel in paths:
    try:
        tree = ast.parse(open(rel, "rb").read(), filename=rel)
    except (SyntaxError, OSError):
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            called = f.id if isinstance(f, ast.Name) else (
                f.attr if isinstance(f, ast.Attribute) else None)
            if called in CTOR and any(k.arg is None for k in n.keywords):
                splats.append(rel)
        elif isinstance(n, ast.ImportFrom):
            if {a.name for a in n.names} & SEAM:
                seam_nodes.append(rel)
for label, rows in (("P3 splat constructions", splats), ("P4 seam imports", seam_nodes)):
    files = set(rows)
    print(f"{label}: {len(rows)} sites in {len(files)} files, production files "
          f"{len([f for f in files if not f.startswith('tests/')])}")
```

## 7. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The classes above account for 2270 of the 2563
exception lines the classifier matched, and 2563 is itself smaller than 2714 failures plus
106 errors, because a failure whose traceback line the pattern did not match is not counted.
That remainder is given NO numeral beyond the two totals, because none was measured.

THE 493 `AttributeError` AND 271 `unsupported operand` CLASSES ARE NOT DIAGNOSED HERE. They
are consistent with the id shape and with a receiver the field rename should not have
touched, and neither reading was taken, so neither is stated. The round that migrates the id
shape re-runs this dry run and reads them against a tree where the shape is no longer a
cause.

THE EXCLUSION LIST IS A CHOICE THIS DRY RUN MADE, NOT A RULING. Excluding
`packages/core/models.py` and `packages/orchestration/storage.py` is what lets the classic
record and its store survive the flip commit, so that DECISION F260 D5's resolver collapse
can delete them in the commit range it names. A later round may rule differently.
END-ARTEFACT46 ───────────────────────────────────────────────

BEGIN-DECIDE46 ───────────────────────────────────────────────

## DECISION F275 D26 (2026-09-11, F275 round 46) — the flip is NOT the next commit: a dry run of it at `978046fe` leaves 2714 failing tests in six classes, and the largest unruled one is the ID SHAPE, which reaches three models outside the classic record

WHAT THIS AMENDS AND WHAT IT LEAVES ALONE. DECISION F275 D17 chose the flip's ROUTE — F275's ONE declared-oversize commit — and DECISION F275 D21 measured its floor. That route is UNCHANGED here and this decision does not reopen it. DECISION F275 D25 recorded two mechanical rules a dry run had learned by failing and closed with the flip's construction mapping ruled, and `.agent/handoff.md` at `978046fe` accordingly names the flip as the next round's work and calls it "a mechanical transformation with every prerequisite measured". That sentence is the one this decision corrects, and it is corrected by running the thing rather than by re-reading it. No landed text is rewritten, per planner_reviewer_prompt.md §3 item 20.

THE MEASUREMENT, taken by the reviewer at `978046fe` in a disposable worktree and recorded in full, with its instrument, in `.agent/f275_t003_flip_residue.md`. The flip was implemented as a surgical `ast`-span text transformation carrying DECISION F275 D25's two rules and four more the dry run itself required, and it CONVERGES AS AN EDIT: 282 files rewritten, 5388 insertions against 5230 deletions, ZERO files left unparsable, and `pytest --co` collects 18394 tests with ZERO collection errors. It does NOT converge as a CHANGE: the suite reads 2714 failed, 15551 passed, 23 skipped and 106 errors at exit 1 in 19 minutes 49 seconds. Six classes account for it, each measured by bucketing the run's own exception lines: 867 `JobPlan.__init__() got an unexpected keyword argument`, 493 `AttributeError: object has no attribute`, 271 `TypeError: unsupported operand type(s) for /`, 256 `ValueError: badly formed hexadecimal UUID string`, 241 `ValidationError for Artifact` and 128 `ValidationError for TaskExecutionContext`.

THE FINDING THIS DECISION EXISTS FOR, and it is the one no artefact of this feature enumerates. `Job.id` and `Task.id` are `uuid.UUID`; `JobPlan.job_id` and `TaskEntry.task_id` are `str`. A rename cannot carry a type change, and the type does not stop at the record: of 53 pydantic models reachable under `packages.`, SIX declare a UUID-typed field, and THREE of the six are neither `Job` nor `Task` — `Artifact` at `id` and `task_id`, `TaskExecutionContext` at `job_id` and `task_id`, and `PatchIntentSet` at `task_id` and `artifact_id`. That is what the 256 hexadecimal-UUID failures and the 369 model-validation failures are: the flip hands a 16-hex string to a field annotated `uuid.UUID` on a model the flip never touches. DECISION F275 D21 and both enumeration artefacts recorded this remainder in their own words as measured "only as a BOUND", and `.agent/f275_t003_flip_seam.md` says of it that "a bound is recorded as a bound". It is now sized on its consumers rather than on its sites, which is the reading that decides the route.

CHOSEN: THE ID SHAPE IS MIGRATED FIRST, IN ITS OWN COMMIT OR COMMITS, BEFORE THE FLIP — the same move DECISION F275 D22 made for the `Task` record and DECISION F275 D23 made for the unified store, for the same reason each gave. A capability the flip's target lacks is widened in first, green by construction, and the atomic commit shrinks by everything the widen carries. Landing it inside the flip would put a type migration across three models the flip does not otherwise touch inside the ONE commit in this feature that cannot be split to repair a mixture, which is exactly what AGENTS.md's Commit Discipline forbids and what D23 already rejected on the same arithmetic. The four transform rules the dry run added are recorded in the artefact rather than here, because they are mechanics and not a choice.

ALTERNATIVES CONSIDERED, each rejected on a measurement rather than a preference. (i) Author the flip now and repair the residue in follow-up rounds — rejected because the residue is 2714 tests and the commit carrying it cannot be split, so every repair would land on a tree that has never been green, and no reviewer could tell a migration that dropped a capability from one that never had it. (ii) Keep `uuid.UUID` on the three outer models and coerce at each boundary — rejected because it is the compatibility reader AGENTS.md's Scope Control forbids by name, and it leaves two spellings of one id alive after a feature whose whole purpose is that there is one. (iii) Treat the 867 splat failures as the first prerequisite instead — rejected on the reading rather than the count: a `**` splat is invisible to a keyword rewrite, which makes it a TRANSFORM RULE the artefact now states, not a capability the target record lacks, and fixing it changes no line that survives the flip. (iv) Declare the flip undeliverable and hard-stop with an operator question under amend0908-f275-finish rule 2 — rejected because that rule reserves the hard stop for a module group genuinely undeletable under T001's three rules, and nothing measured here is undeliverable; it is unsequenced.

HOW TO REVERSE: delete this decision. The flip then stands as the next round's work at the size D21 declares, and the round that authors it rediscovers the 2714 failures on a commit that cannot be split.
END-DECIDE46 ─────────────────────────────────────────────────
