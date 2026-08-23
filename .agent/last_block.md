── STEP R5 — F031 Decision inbox ─────────────────────────────
Goal:        Record the R4 verdict, register the one finding R4's
             review produced, and RULE the three design questions the
             source inventory forced — each as a DECISION on disk and
             as an amendment appended to the feature file — so R6 can
             plan T001 against a spec that matches the source.

Fortschritt: ~4 % (F031 claimed; R1 through R4 landed and gated · the
             source inventory is on disk · R5 rules the three design
             questions · no T-slice started) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block ·
             C1 the plan · C2 the R4 gate entry and finding R-0678 ·
             C3 the three DECISIONs · C4 the feature-file amendment ·
             C5 the handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r5.md
             .agent/last_block.md
             .agent/plan.md
             .agent/live_review.md
             .agent/decisions.md
             docs/roadmap/features/T5_F031.md
             .agent/handoff.md
             This list bounds the round's WRITES, not its ACTIONS: the
             push named in gate G13 is ordered explicitly and is not a
             file (finding R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `f4311bf6e711c6a1cc6ff17c3e14a6bb53803222`, the R4
handback commit and the current tip of `feature/f031-decision-inbox`.
Every SHA-shaped token in this block was passed to `git cat-file -t`
before emission and every one resolves, with ONE deliberate exception:
the id FIND678 quotes as the defect it registers, which is that
finding's evidence and G11's positive control. That sweep is the
discipline R-0678 exists to enforce, applied to the block registering
it. Stay on that branch; create none, never commit to `main`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: `^- R-\d+ — ` 238 all DISTINCT, maximum
  `R-0677`; `^Done: R-\d+ — ` 2; `^Recurrence: R-` 14;
  `^Gate: R\d+ — ` 4, the keys `R19`, `R1`, `R2` and `R3`.
- The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus every
  `^Done: R-\d+ — ` line — is 238 − 2 = 236 at that commit.
- `.agent/plan.md` 49 lines. `.agent/decisions.md` 7320 lines.
  `docs/roadmap/features/T5_F031.md` 91 lines.
- `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q`
  exits 0 at 325 passed AT THIS BASE — the reviewer ran it there before
  ordering it (R-0364), so a red in G12 is this round's doing.

── Why this round exists ─────────────────────────────────────
R4 passed on every one of its ten gates under the reviewer's own
execution, reproducing every number cell for cell. C2 records that.

The review found ONE defect and it is the reviewer's own: the R4
block's Base section named a forty-character object id that does not
exist. `git cat-file -t` on it fails outright, its first twelve
characters match the real tip and the remaining twenty-eight do not.
The worker resolved the base by the branch tip — which the same
sentence named as the resolution rule — declared the divergence and
reconciled nothing, which is exactly right. The open set was searched
for the DEFECT before the id was minted (§3 item 30); FIND678 names the
three neighbouring entries and why none of them reaches it.

C3 rules the three design questions the R3 inventory forced. They are
ruled here rather than deferred because every T-slice estimate depends
on them and the feature file contradicts the source on the second.
C4 appends the amendment to the feature file rather than rewriting the
sentences it supersedes: the record stays append-only and a reader sees
what was planned and what was ruled, in that order.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" a slice. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback. A contradiction inside
   this block is the reviewer's defect, not yours: state it, reconcile
   nothing.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r5.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   a line equal to `<<<SLICE <NAME>` opens it, a line equal to
   `<<<END <NAME>` closes it. Marker lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5. No extra
   commit, none dropped, no reordering. If you must correct a landed
   commit, do NOT add a commit outside this sequence — declare it
   (R-0675). The push runs after C5.
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C5; if present,
   finish the commit in hand, write the handback and stop (G6).
6. The slices this block carries are the whole text PLANF031R5, the two
   ledger paragraphs GATE4 and FIND678, the decisions text DEC031 and
   the feature-file text FEATAMEND. This paragraph names them and
   states no count of them; G3 orders you to report the count YOUR
   extractor measured.
7. C2 appends GATE4 then FIND678 to `.agent/live_review.md` in that
   order; C3 appends DEC031 to `.agent/decisions.md`; C4 appends
   FEATAMEND to `docs/roadmap/features/T5_F031.md`. In every case the
   appended text is separated from the preceding text by exactly one
   blank line, consecutive appended paragraphs are separated from each
   other by exactly one blank line, and the file ends in exactly one
   newline. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment
   reading is owed and none is stated.
8. THIS ROUND MINTS EXACTLY ONE FINDING ID, `R-0678`, and changes no
   existing finding record. `^- R-\d+ — ` must be 238 before and 239
   after, and the maximum must move from `R-0677` to `R-0678`.
9. Do not touch any path under `packages/`, `apps/`, `tests/` or
   `README.md`, do not touch `docs/roadmap/ROADMAP.md` or
   `docs/roadmap/STATUS.md`, and do not touch `.agent/f031_inventory.md`
   — the inventory is landed evidence and is corrected by dating in a
   later round, never by editing (§3 item 20, findings R-0417, R-0525).
10. Destructive verification, if any, runs ONLY in a disposable
    `git worktree` under `.remedy-wt/`, removed BY ITS EXACT PATH
    (R-0662) and BEFORE the G12 suites — a worktree present makes
    `tests/orchestration/test_test_runner.py::`
    `TestVitestFrontendTestFoundation::test_vitest_passes` fail on a
    missing `node_modules` (the R-0518 shape), which is an artefact of
    the measurement and not a regression.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R5
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
source of truth for the record, the round map and the finding-id ceiling;
`.agent/f031_inventory.md` is the measured source inventory R3 landed, and
`.agent/decisions.md` now carries the three rulings R5 made over it.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R5 records the R4 verdict, registers finding R-0678, and rules the three design
questions the inventory forced as DECISION F031 D1, D2 and D3, appending the
matching amendment to the feature file.

## Next Steps
1. R6 records the R5 verdict and plans T001 against what D1, D2 and D3 ruled:
   the read endpoint over `list_decisions`, the blocked-size wiring from
   `blocked_downstream`, and a fixture per PRODUCING type.
2. T001 then lands that endpoint with its contract tests.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 236, measured at `f4311bf6`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533,
  R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677 and
  R-0678, of which R-0495 and R-0574 are the two Highs, inherited from F085 and
  F086.
- THE TWO BADGE COUNTERS F031 MUST REPLACE ARE A CONSTANT ZERO TODAY, and they
  are named by their FUNCTIONS because the bare symbol is ambiguous: the
  `decision_count` local of `_build_dashboard` and the `open_decisions` sum of
  `_build_live_state_json`, both in `packages/orchestration/ui_server.py`, each
  count the event kind `human_decision_requested`, which no producer emits. A
  THIRD `decision_count`, in `_build_orchestrator_section` of the same file, is
  fed by `orchestrator_brain.list_decisions` and is NOT always zero and NOT part
  of this feature. All three readings were taken at `f4311bf6`.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R5

<<<SLICE GATE4
Gate: R4 — the F031 R4 entry. R4 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM; every number the handback states reproduced cell for cell, and the round's only defect is the reviewer's own, registered below as R-0678. TRANSPORT HELD IN ITS STRONGEST FORM: the committed C0a blob at `3ff12773`, the committed C0b blob at `ef3653fe`, `.agent/last_block.md` off disk and `.agent/authored/f031-r4.md` off disk are ALL sha256 `e8481b51c7f1fb5a2cab4b26c6a238523d3916859ce820acfa6ac602e3736a96` over 24209 bytes and 291 lines, and C0a and C0b resolve to the SAME git blob `302388e9`. THE EXTRACTION printed 3 slices across 51 content lines against 291 total. `.agent/plan.md` at `1d91b6d9` is 2988 bytes and 49 lines, byte-equal to PLANF031R4 under the newline-INCLUDED convention with the trailing-newline-removed control FALSE, `^## Goal$` and `^## Next Steps$` once each, strictly under the cap of 50. THE TWO APPENDS HELD UNDER BOTH READERS AND A CONTROL: at `9808ecbd` the base blob is a byte-exact PREFIX, the file grew 532442 bytes to 539793 and the delta 7351 equals 1 plus GATE3's 4696 plus 1 plus RECUR601's 2653 with the two regions byte-equal at offsets 532443 and 537140, an independent blank-line split went 275 units to 277 with the LAST TWO equal to GATE3 then RECUR601 IN ORDER, and the reviewer flipped one byte inside the FIRST appended paragraph in memory and BOTH readers rejected the mutant while BOTH accepted the true file. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 238 to 238 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0677` UNCHANGED, `^Done: R-` 2 to 2, `^Recurrence: R-` 13 to 14 gaining exactly one `R-0601` line, and `^Gate: R\d+ — ` 3 to 4 gaining exactly the key `R3` with `R19`, `R1` and `R2` still present. MARKERS WERE LINE-ANCHORED 0 in `.agent/plan.md` at `1d91b6d9` and in `.agent/live_review.md` at `9808ecbd`, and the range named four paths, none under `packages/`, `apps/`, `tests/` or `docs/`, and not `.agent/f031_inventory.md`. STRUCTURE HELD: five commits from `f26c5da5` to `f4311bf6`, each single-parent, insertions 291, 166, 29, 4 and 92, each far under the 500 cap; over the full range the path set MINUS the change set and the change set MINUS the path set are BOTH EMPTY; `git ls-files .remedy-wt` 0, the zip glob 0, one worktree, `git status --porcelain` 0. THE REFLOG READING STATES ITS OWN SCOPE AND FIELD, as the R3 recurrence requires: over the 5 entries of this round's own range, read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, every prefix is `commit`, so amend 0, rebase 0 and cherry 0. THE FIVE SUITES ARE THE REVIEWER'S OWN, run SERIALLY with never two pytest processes alive, every one REAL exit code 0 at 470, 52, 21, 16 and 42 — cell for cell the readings the block predicted from R3's C4. THE PUSH DISCHARGED: local and remote tips are both `f4311bf6e711c6a1cc6ff17c3e14a6bb53803222`; no pull request, nothing merged. THE HANDBACK'S OWN ARITHMETIC IS CORRECT: it derives the tier 60 from the five commits constraint 3 fixes rather than quoting it, measures itself at 158 lines, claims a DECISION D15 stated-cause overage naming mandated content, claims NO token cap, and carries the block's three-line `Fortschritt` VERBATIM. ONE CLAUSE OF THE R3 ENTRY IS NARROWED HERE RATHER THAN EDITED, per §3 item 20: that entry says `decision_count` and the `open_decisions` sum are both always 0, which is TRUE of the two counters it means — the `decision_count` local of `_build_dashboard` and the `open_decisions` sum of `_build_live_state_json` — but `packages/orchestration/ui_server.py` at `f4311bf6` holds a THIRD `decision_count`, in `_build_orchestrator_section`, fed by `orchestrator_brain.list_decisions` and NOT always zero, so the symbol alone does not identify the defect and the function names do. THE VERDICT IS PASS.
<<<END GATE4

<<<SLICE FIND678
- R-0678 — Low, A BLOCK NAMED A FORTY-CHARACTER OBJECT ID THAT DOES NOT EXIST, AND ONLY TWELVE OF ITS CHARACTERS HAD EVER BEEN MEASURED. Raised by the reviewer at the F031 R4 gate against the reviewer's own R4 block. THE INSTANCE: that block's Base section reads "The round base is `f26c5da5e5b60e8b7a3b2ba1a4b1a0e5c0ff5a0d`'s branch". Measured at `f4311bf6`, `git cat-file -t` on that id exits 128 with "could not get object info", while the real R3 handback commit — which the same sentence names as the resolution rule, and which equalled the remote tip — is `f26c5da5e5b6563b1b4fd8e71946344e8c3f6fac`. The two agree for exactly twelve characters and diverge over the remaining twenty-eight, which is the signature of a short id that was really measured and then extended by invention rather than by `git rev-parse`. NOTHING FALSE LANDED, and that is the worker's doing rather than the gate's: it resolved the base by the branch tip as the sentence instructed, reproduced every base reading the block predicted there exactly, declared the divergence in its handback and reconciled nothing, exactly as constraint 1 requires. WHY LOW: the block carried its own resolution rule beside the bad id, so the round was recoverable without a repair commit, and no gate consumed the forty-character form. WHY IT IS A FINDING ANYWAY: a base id is the anchor every range gate of the round hangs from, and had the sentence named the id ALONE the round could not have started — the recovery depended on a clause the next block might not carry. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED (§3 item 30), and the three neighbouring entries each stop short of it: R-0368 governs WHICH commit a range gate takes as its base and R-0376 carries the grep for SHA-shaped tokens, but both test a token's ROLE and pass an id that is well-formed and fictional; R-0521 requires an identifier that already EXISTS when a slice is written, and was written against labels like `main` that re-resolve rather than against ids that resolve to nothing. THE FIX, binding on every block from here: before emission, every SHA-shaped token in the block's own bytes is passed to `git cat-file -t` and must exit 0, and any id the block states in full is the OUTPUT of `git rev-parse` on the short form rather than a transcription of it. This is one command over a token list the R-0376 grep already produces, so it is an extension of a check this repository has, not a new ritual. OPEN.
<<<END FIND678

<<<SLICE DEC031
## DECISION F031 D1 (2026-08-23) — what "the decision queue" IS: a derived read view, and where its durability actually lives

CHOSEN. The decision queue is a DERIVED READ VIEW, not a store.
`packages/orchestration/decision_queue.py` performs no I/O — measured at
`f4311bf6`, it imports only `dataclasses`, `typing` and `Job`, and the literals
open-paren-preceded `open` and `Path` occur 0 times in it — and `list_decisions`
re-derives every `HumanDecision` on each call from an already-loaded job plus
its event list. Durability lives UPSTREAM: `enqueue_task_decision` in
`packages/orchestration/escalation.py` stores task-decision records on the job,
and `save_job` in `packages/orchestration/storage.py` writes the job to disk.

The feature file's "the decision queue is and stays FILE-BASED (the established
store with its CLI)" is therefore TRUE OF THE JOB RECORD and false of the
module that bears the name. Both readings had a real referent, which is why the
contradiction survived into the feature file.

CONSEQUENCE FOR F031. T001 adds NO storage and NO second source of truth: the
read endpoint calls `list_decisions` over a loaded job and computes the extra
card fields on the way out. The feature file's "Do not touch — queue
storage/format" binds the escalation record shape and `save_job`, and it does
NOT freeze `decision_queue.py`, which is a view and may gain derived fields —
the blocked-subtree size of D-nothing-else being the first.

ALTERNATIVES CONSIDERED. Reading "FILE-BASED" as binding on the module and
adding a real store: rejected, because the module's own docstring calls itself
"a read-only aggregation" and "Not a second source of truth", and a store there
would duplicate the job record. Treating the contradiction as a feature-file
error to be deleted: rejected, because the sentence is true of the durable
record and deleting it invites the database the sentence exists to prevent.

REVERSE IT by deleting this DECISION and the D1 paragraph of the
`## Design amendments` section of `docs/roadmap/features/T5_F031.md`. No code
depends on it yet, because no T-slice has started.

## DECISION F031 D2 (2026-08-23) — the badge is fed by RE-DERIVATION on refetch, and F031 introduces no new event kind

CHOSEN. The inbox badge counts open decisions by RE-DERIVING them — the same
`list_decisions` derivation the read endpoint uses — refetched when the existing
SSE stream signals that the job changed. F031 emits NO `decision.requested` and
NO `decision.resolved` event, and adds no kind to
`packages/orchestration/event_schemas.py`.

THE MEASUREMENT THAT FORCES IT, taken at `f4311bf6`. The kinds the feature file
names do not exist: a repository-wide grep for `decision.requested`,
`decision_requested`, `decision.resolved` and `decision_resolved` finds those
strings only inside `docs/roadmap/features/T5_F031.md` itself. The differently
named `human_decision_requested` has 7 occurrences across 3 files and NOT ONE IS
AN EMITTER — they are a filter, three map keys, two counts and one test fixture
— and `human_decision_resolved` has 0 occurrences anywhere. Consequently the
`decision_count` local of `_build_dashboard` and the `open_decisions` sum of
`_build_live_state_json`, both in `packages/orchestration/ui_server.py`, are a
CONSTANT ZERO in production, and F031 must replace both rather than feed them.
A third `decision_count`, in `_build_orchestrator_section` of that same file, is
fed by `orchestrator_brain.list_decisions`, is not always zero, and is not part
of this feature.

WHY RE-DERIVATION AND NOT EMISSION. There is no producer to emit from. Every
decision is constructed inside `list_decisions` across the eight branches of
that one function, and each branch reads an upstream signal that ALREADY rides
the stream — `test_run_completed`, `git_status_read`, `job_stopped`, the
approval queue, the flight plan, the escalation records. Emitting a decision
kind would mean adding a writer at eight sites whose only job is to restate,
in a second vocabulary, something the stream already carries; the module
docstring's "Not a second source of truth" names precisely that hazard. Two of
the eight branches do have real upstream writers, so a partial emission design
is available and is worse: it would make the badge correct for two types and
silently wrong for six.

CONSEQUENCE FOR F031. The feature file's "live via decision.requested/resolved
events driving the badge" and its "(decision.requested/resolved kinds —
envelope coordination if not yet present)" are AMENDED by the appended
`## Design amendments` section rather than rewritten in place. The badge's
liveness is a refetch on the existing stream, and its correctness is pinned by a
test that derives the count from a fixture job rather than from an event kind.
The snapshot-refetch fallback the feature file already names becomes the primary
path rather than the fallback.

ALTERNATIVES CONSIDERED. Emitting the two kinds at all eight branches: rejected
above. Emitting only where a real writer exists: rejected as the partial design
that is wrong for six types. Polling on a timer: rejected because the stream
already delivers the signal and a timer would add latency and load for nothing.

REVERSE IT by deleting this DECISION and the D2 paragraph of the
`## Design amendments` section of `docs/roadmap/features/T5_F031.md`, which
restores the feature file's original event-driven wording as the live spec.

## DECISION F031 D3 (2026-08-23) — the acceptance loop covers PRODUCING types, and the two unproduced names stay declared

CHOSEN. `DECISION_TYPES` keeps all ten members. The acceptance criterion "every
producer type renders and answers correctly from fixtures" is read as the eight
types that a branch of `list_decisions` actually produces, and the fixture set
and its loop test are derived from THOSE BRANCHES rather than from the
frozenset. `worker_approval` and `revert_missing` get no fixture.

THE MEASUREMENT, taken at `f4311bf6`: a repository-wide grep over Python sources
for either name returns exactly one line, the `DECISION_TYPES` declaration
itself, so neither has a producer, a reader, or a test. The remaining eight each
have a producing branch, named per type in `.agent/f031_inventory.md` under Q3.

WHY THEY STAY DECLARED. Removing a member changes decision semantics, which the
feature file's "Do not touch" forbids outright, and the set is advisory in any
case — `HumanDecision.type` is annotated plain `str` and no production module
imports `DECISION_TYPES`, so the two names constrain nothing at runtime and cost
nothing by remaining. Deriving the fixture set from the frozenset instead would
make the loop test unsatisfiable by construction for two of its ten members.

WHY THIS COSTS NO COVERAGE. The renderer is generic over the decision's options
payload, so an unproduced type needs no per-type work; the extensibility test —
a novel fixture type with novel options rendering generically — is exactly the
case that covers a type nobody produces yet. When a producer for either name
lands, the loop test picks it up because it reads the branches.

ALTERNATIVES CONSIDERED. Deleting the two names from the frozenset: rejected as
a decision-semantics change the feature file forbids. Fixturing them anyway
against a hand-written decision no code can produce: rejected because a fixture
with no producer pins the fixture rather than the system, and the loop test's
whole point is that new producers must join the set.

REVERSE IT by deleting this DECISION and the D3 paragraph of the
`## Design amendments` section of `docs/roadmap/features/T5_F031.md`.
<<<END DEC031

<<<SLICE FEATAMEND
## Design amendments (F031 R5, 2026-08-23)

> These rulings SUPERSEDE the sentences they name above. The originals are
> deliberately left in place: this file records what was planned and then what
> was ruled, in that order. Full rationale, alternatives and reversal paths are
> in `.agent/decisions.md` under DECISION F031 D1, D2 and D3.

- **D1 — the queue is a derived read view.** "How it fits" says the queue "is
  and stays FILE-BASED (the established store with its CLI)". That is true of
  the JOB RECORD, which `escalation.py` writes and `storage.py` persists, and
  not of `packages/orchestration/decision_queue.py`, which performs no I/O and
  re-derives every decision from a loaded job. T001 adds no storage; "Do not
  touch — queue storage/format" binds the escalation record shape, not the
  derivation, which may gain derived fields such as the blocked-subtree size.

- **D2 — the badge re-derives; no new event kind ships.** "Goal & Done" says
  "live via decision.requested/resolved events driving the badge", and "How it
  fits" anticipates those kinds with "envelope coordination if not yet
  present". Those kinds do not exist and no producer emits anything equivalent,
  so the badge instead RE-DERIVES its count through the same `list_decisions`
  call the read endpoint uses, refetched on the existing SSE stream. The
  snapshot-refetch path the Design section lists as the fallback becomes the
  primary one. F031 adds no kind to `event_schemas.py`.

- **D3 — the acceptance loop covers PRODUCING types.** "Acceptance" says "every
  producer type renders and answers correctly from fixtures". That set is the
  eight types a branch of `list_decisions` produces, derived from the branches
  rather than from the `DECISION_TYPES` frozenset. `worker_approval` and
  `revert_missing` have no producer, stay declared, and get no fixture; the
  extensibility test already covers a type nobody produces.
<<<END FEATAMEND

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback with transcripts kept out of it
(finding R-0582). "Green" as a word is a finding. Every gate runs at a
commit STRICTLY EARLIER than C5, which writes the handback (§3 item 31).

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C5. Report
    `git status --porcelain` line count after each of C0a, C0b, C1, C2,
    C3 and C4; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r5.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R5 under
    your stated newline convention; report the slice length, the file
    length and the convention. NEGATIVE CONTROL: the file is NOT
    byte-equal to the same slice with its trailing newline REMOVED.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The ledger appends. For GATE4 and FIND678 separately, report that
    the corresponding region of `.agent/live_review.md` at C2 equals
    the extracted slice bytes, that the base blob is a byte-exact
    PREFIX, and the byte arithmetic. Report a SECOND, INDEPENDENT
    reading: split the C2 file on blank lines and confirm the LAST TWO
    units equal the two slices IN ORDER; report the unit count before
    and after. NEGATIVE CONTROL: flip ONE byte inside the FIRST
    appended paragraph in a disposable worktree and report that BOTH
    readers reject the mutant while BOTH accept the true file.

G6  The sets. In `.agent/live_review.md`, the round base versus C2:
    `^- R-\d+ — ` 238 → 239 all DISTINCT, ids ADDED exactly the one id
    `R-0678`, ids REMOVED the EMPTY SET, maximum `R-0677` → `R-0678`,
    `^Done: R-` 2 → 2, `^Recurrence: R-` 14 → 14 UNCHANGED.
    `^Gate: R\d+ — ` 4 → 5, gaining exactly the key `R4`, with `R19`,
    `R1`, `R2` and `R3` still present.

G7  The decisions append. `.agent/decisions.md` at C3: the base blob is
    a byte-exact PREFIX, the appended region equals DEC031's bytes, and
    the byte arithmetic is reported. Report the line-anchored count of
    `^## DECISION F031 D` as 0 at the base and 3 at C3, and report that
    `^## DECISION F031 D1 `, `^## DECISION F031 D2 ` and
    `^## DECISION F031 D3 ` each occur exactly 1x at C3 — the header
    comparison §3 item 26 requires against the file's existing
    `## DECISION <feature> D<n>` series.

G8  The feature-file append. `docs/roadmap/features/T5_F031.md` at C4:
    the base blob is a byte-exact PREFIX, the appended region equals
    FEATAMEND's bytes, and the byte arithmetic is reported. Report
    `^## Design amendments ` as 0 at the base and 1 at C4.

G9  Markers and untouched paths. Line-anchored `^<<<SLICE ` and
    `^<<<END ` both count 0 in `.agent/plan.md` at C1, in
    `.agent/live_review.md` at C2, in `.agent/decisions.md` at C3 and
    in `docs/roadmap/features/T5_F031.md` at C4. Report that
    `git diff --name-only <base>..C4` names NO path under `packages/`,
    `apps/`, `tests/` or `README.md`, names NEITHER
    `docs/roadmap/ROADMAP.md` NOR `docs/roadmap/STATUS.md`, and does
    NOT name `.agent/f031_inventory.md` (constraint 9).

G10 Structure and hygiene, over C0a..C4. Report per commit: that it is
    single-parent, and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Report the range path
    set MINUS the change set (must be EMPTY) and the change set MINUS
    the range (must be exactly `.agent/handoff.md`, which C5 writes).
    Report `git ls-files .remedy-wt` as 0, `git ls-files` over the
    pattern `*.zip` as 0, and `git worktree list` as 1 line. FOR THE
    REFLOG, state the SCOPE and the FIELD in the reading itself: over
    THIS ROUND'S reflog entries only, read by the OPERATION PREFIX
    before the first colon of `git reflog --format=%gs`, report
    `amend`, `rebase` and `cherry` each 0, and report how many entries
    you scoped the reading to.

G11 The block's own object ids, the R-0678 discipline applied to the
    block that registers it. Extract every SHA-shaped token from the
    COMMITTED C0a blob with the word-bounded pattern `[0-9a-f]{7,40}`,
    which by its boundaries does NOT match the 64-character sha256
    digests this block also carries, and pass each to
    `git cat-file -t`. THE SET OF TOKENS THAT FAIL MUST EQUAL THE ONE
    ID `f26c5da5e5b60e8b7a3b2ba1a4b1a0e5c0ff5a0d`, which FIND678 QUOTES
    as its evidence — a token a finding QUOTES is not a token the block
    USES (the R-0584 reading), so its failure is this gate's POSITIVE
    CONTROL and its absence from the failure set would mean the pattern
    matched nothing. Every other token must exit 0. Report the token
    count YOUR extractor measured, the failing set by value, and the
    type `git cat-file -t` printed for each token that resolved.

G12 Suites, run SERIALLY, never two pytest processes at once, in the
    PRIMARY checkout at the C4 tree, with `git worktree list` reported
    as 1 line immediately BEFORE the first pytest command. All must
    exit 0; report the real exit code and the counts:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
    The reviewer executed the first five at `f4311bf6` with no worktree
    present and measured, in the order listed: 470, 52, 21, 16 and 42,
    every one exit 0; and the last two TOGETHER at that same commit for
    325 passed, exit 0. Report yours against those and account for any
    difference. The last two are ordered because C4 writes a
    `docs/roadmap/**` path.

G13 The push. AFTER C5, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. This gate's outcome is REPORTED TO THE
    REVIEWER and is NOT a value of any file this round writes (finding
    R-0371's extended counter-measure).

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3, C4, C5
and the push, ONE LINE PER GATE with its real result, the finding
counts, and the next expected action. Carry the `Fortschritt:` block
above VERBATIM across the lines it occupies — count them yourself and
carry exactly those; this block states no numeral for them.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it
yourself from AGENTS.md under `### handoff.md` against the number of
commits constraint 3 fixes, and report BOTH the commit count you derived
and the tier that follows. If the MANDATED content genuinely does not
fit, exceed it and carry a DECISION D15 "Deviations, declared" line
naming your measured line count and the specific mandated content that
caused it. Never drop a mandated section to fit. Do NOT claim compliance
with any token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and the
COMMIT it was measured at, in the same sentence, per DECISION F009 D10.
A narrower set is named "the findings this feature must still act on"
and is never called "open" unqualified.

Your `## Next` section names, in order: Phase 1 rule 1 (re-read
`.agent/STOP` from disk), then that NO pull request exists for this
branch and none should be created yet, then that R6 records the R5
verdict — which by DECISION F085 D9 no artefact of this round can carry
— and plans T001 against DECISION F031 D1, D2 and D3.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
