### STEP T001a — F257 Self-use track, round 1 (THE CLAIM)

Goal: merge the F256 closure PR at the Open PR Gate, claim F257, retarget the
`.agent/` state onto it, and record the two rulings this feature's shape
depends on — that F257 is claimable at all, and what the queue format and the
consumption point ARE.

This round deliberately writes NO production code. The feature file's
Orchestrator brief rules that the queue format and the consumption point are
settled before anything that runs is written; this round settles them, and the
next round builds the queue file, its loader and its tests against DECISION
F257 D2.

Base: the tip of `main` AFTER constraint 0's merge. That SHA is not knowable
when this block is written, so nothing here states it; constraint 0 orders you
to REPORT it, and every gate below names it as BASE.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r1.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 retarget `.agent/plan.md` and `.agent/context.md`, and append DECISIONS
  F257 D1 and F257 D2 to `.agent/decisions.md`
- C2 the STATUS claim
- C3 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r1.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/context.md`
- `.agent/decisions.md`
- `docs/roadmap/STATUS.md`
- `.agent/handoff.md`

`.agent/live_review.md` is NOT edited. F256 R10 was the last round of its
branch, and docs/agents/planner_reviewer_prompt.md §4 item 13 rules that such a
round has no on-disk gate entry, so nothing is owed to the ledger this round.
The F256 R10 verdict is PASS; it lives in the reviewer's report and in pull
request #220.

### Constraints

0. THE OPEN PR GATE, BEFORE ANYTHING ELSE. Run
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
   report its output verbatim. It must hold EXACTLY ONE entry: number 220, head
   `feature/f256-diff-viewer-completion`, base `main`, `isDraft` false. If it
   holds anything else, STOP and hand back without committing. The reviewer
   confirmed the `ci` check GREEN on that PR before this block was written.
   Merge with `gh pr merge 220 --merge --delete-branch`, then `git checkout
   main` and `git pull --ff-only`. Report `git rev-parse HEAD`; that value is
   BASE and every gate below names it. Then create and switch to
   `feature/f257-self-use-track`; every commit lands there. Never force-push,
   never rewrite history, and delete no branch beyond the gate's own
   `--delete-branch`.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r1.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, and every form of
   environment-variable assignment (`VAR=x cmd`, `env VAR=x cmd`,
   `export VAR=x; cmd`) are rejected by FORM; route such work through
   `python3 - <<'PY'`, set variables in-process with `os.environ[...]`, and copy
   with `shutil.copyfile`. Capture real exit codes as
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess` in Python — the
   tool does not surface a non-zero exit on its own. Report every re-expression
   in the handback.
7. NO PRODUCTION CODE AND NO NEW FILE OUTSIDE THE CHANGE SET. Nothing under
   `packages/`, `apps/`, `tests/` or `scripts/` is created or edited this round.
   The queue file `scripts/self_use_queue.json`, its loader
   `packages/orchestration/self_use_queue.py` and its tests belong to the NEXT
   round, which builds them against DECISION F257 D2.

### The authored slices

<<<SLICE PLANF257R1
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
| claim F257 and retarget the state | done | this round |
| rule the queue format and the consumption point | done | DECISIONS F257 D1 and D2 |
| the queue file and its read-only loader | open | next round, against D2 |
| render a queue item into a job file and plan it | open | needs the loader first |
| consume exactly one item per feature close | open | the closure-protocol edit |
| document the format where a reader looks | open | acceptance item 1 |

## Next Steps
1. Build `scripts/self_use_queue.json` and its read-only loader
   `packages/orchestration/self_use_queue.py`, with tests, against DECISION
   F257 D2.
2. Render a pending queue item into a job file and plan it through
   `plan_job_from_file`, so the queue reaches the real job path.
3. Wire the consumption point into the closure sequence, so exactly one item is
   consumed per feature close and the track cannot rot.

## Risks
- A job must never mark its own queue item consumed; the loader will ship no
  writer and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
<<<END PLANF257R1

<<<SLICE CTXF257R1
# Context — F257 Self-use track

## Active Branch
feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220.

## Scope
Feature F257, `docs/roadmap/features/T5_F257.md` — the standing self-use track
operator order amend0828-daily-driver registered. The pieces: a curated queue
file, exactly one item consumed per feature close, the run taken to the normal
approval gate, and findings recorded as operator findings in the feature file
that owns the surface.

## Do not touch
STATUS semantics — a job must never check itself off. The approval gate: the
`--approve` barrier in `packages/orchestration/job_promote.py` is unchanged. The
scope-fence builtin deny list in `packages/orchestration/scope_fences.py`.
`docs/roadmap/ROADMAP.md` is not edited.

## Assumptions
- The queue will store job-file TEXT in the format
  `packages/orchestration/pingpong_job.py:parse_job_file` accepts, so it cannot
  drift into a second task format.
- Shipped curated data lives in `scripts/` with one named loader under
  `packages/orchestration/`, the convention `scripts/dead_models.json` and
  `packages/orchestration/dead_model_list.py` already set.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this feature's, and
deleting them with the rest of a rewrite is what cost an earlier round a red
CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path: the `REMEDY_DATA_DIR` single-reader invariant, the path-utils
  single-implementation invariant, the bare-`except: pass` ban, and the
  development-artifact boundary.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.
<<<END CTXF257R1

<<<SLICE DECF257D1
## DECISION F257 D1 (2026-08-28, F257 R1) — F257 IS claimable; the feature file's "NOT to build it" clause bounds the round that registered it, not every later round

CONTEXT. `docs/roadmap/features/T5_F257.md` opens with a provenance blockquote
reading "REGISTRATION ONLY — the order says to register it with a feature file
and NOT to build it. Nothing in this file has been implemented." No other
feature file carries such a clause, and no round has ever interpreted it:
measured at `c9c54d27`, the string `F257` appears nowhere in
`.agent/live_review.md`, `.agent/decisions.md` or `.agent/context.md`. Rule A5
nevertheless names F257 as the next feature, because it is the first `[ ]` line
after F256, and both `.agent/plan.md` and `.agent/handoff.md` at `c9c54d27` say
so in as many words.

CHOSEN. The clause is read as a scope fence on the ROUND THAT EXECUTED THE ORDER
— register the feature, do not also build it in the same breath — and not as a
standing prohibition. Three readings on disk carry that. The clause's own
grammatical subject is what THE ORDER SAID, and it sits inside the blockquote
whose purpose is registration provenance. The STATUS line is plain `[ ]` rather
than the `[!]` marker docs/agents/planner_reviewer_prompt.md §1 reserves for a
line a session must surface instead of claim. And the file carries a full
Acceptance section and an Orchestrator brief addressed to the planner, which is
text written for a round that builds it. Point 4 of the SAME operator order
registered F256 with no such clause and points 1 through 3 were built
immediately, so the order mixed both kinds and marked which was which.

ALTERNATIVES CONSIDERED. (a) Treat the clause as standing and advance Rule A5 to
F033. Rejected on evidence as well as cost: F033's branch already exists, nine
commits ahead of `main` and five behind, halted on a STOP sentinel at its round
2, so it is not the cheaper path; and reading a registration note as a permanent
gate would leave the first `[ ]` line unclaimable with nothing on disk ever
saying when that lifts. (b) Ask the operator. Forbidden — §2 of the reviewer
prompt bars questions and menus, and §4 item 7 requires exactly this instead: a
loud, persisted, reversible decision.

CONSEQUENCE. F257 is claimed and built in STATUS order. To keep the exposure
near zero if this reading is wrong, this round ships only rulings and state and
nothing that runs — which is also what the feature file's own Orchestrator brief
demands of a first round.

REVERSE by ruling that F257 stays parked. Nothing this round builds runs on its
own or is reachable from any CLI command: flip the STATUS line back to `[ ]` and
Rule A5 advances to F033.
<<<END DECF257D1

<<<SLICE DECF257D2
## DECISION F257 D2 (2026-08-28, F257 R1) — the self-use queue is shipped curated JSON holding job-file TEXT, and only the closure round may mark an item consumed

CONTEXT. F257's Orchestrator brief rules that the queue format and the
consumption point are settled before anything that runs is written, because the
feature's risk sits in curation and in the "exactly one" rule rather than in
code. Measured at `c9c54d27`: no queue-like file that code reads exists in this
repository; `packages/orchestration/job_queue.py` is a per-project queue under
the DATA root rather than in the repo; and `plan_job_from_file` in
`packages/orchestration/pingpong_job.py` accepts a Markdown job file — a
`# Job:` H1 and `## Task N` headings, each task carrying an `Acceptance:` line.

CHOSEN, in three parts. FORMAT: `scripts/self_use_queue.json`, a
`schema_version`-stamped object read by one named loader,
`packages/orchestration/self_use_queue.py` — the convention
`scripts/dead_models.json` and `packages/orchestration/dead_model_list.py`
already set for shipped, operator-editable input. CONTENT: each item carries the
literal `job_markdown` the existing parser accepts, so the queue never grows a
second task format that has to be kept in step with the first, and a test
asserts every shipped item really parses. CONSUMPTION POINT: an item is marked
consumed by an edit the CLOSURE ROUND makes, and the loader ships no writer at
all.

ALTERNATIVES CONSIDERED. (a) A second, richer task schema in the queue, rendered
into a job file later. Rejected: two spellings of one concept is the synonym
drift AGENTS.md's discoverability conventions forbid, and the renderer becomes a
thing to keep in step forever. (b) Let the job itself mark its item consumed at
promotion. Rejected on this feature's own Do-not-touch: a job that can check
itself off is the failure `docs/roadmap/STATUS.md`'s place in
`scope_fences.BUILTIN_DENY` exists to prevent, and the queue is a ledger of the
same kind. (c) Put the queue under `docs/`. Rejected because
`tests/docs/test_docs_consistency.py` counts the files under
`docs/roadmap/features/` and pins the primary docs, and a data file that code
reads is not a doc.

CONSEQUENCE, stated plainly because it is a real dependency on a human step.
Consumption is a HUMAN-SEQUENCED edit, so the track rots if the closure sequence
never performs it. That is why a later round wires the consumption point into
the closure protocol rather than leaving it an intention — which is this
feature's Goal & Done clause in as many words.

REVERSE by deleting this decision; nothing depends on it until the next round
builds the queue file and its loader against it.
<<<END DECF257D2

<<<SLICE CLAIMFROM
- [ ] F257 — Self-use track (one curated maintenance job per feature close, run through job-plan/job-run against Remedy itself)
<<<END CLAIMFROM

<<<SLICE CLAIMTO
- [~] F257 — Self-use track (one curated maintenance job per feature close, run through job-plan/job-run against Remedy itself)
<<<END CLAIMTO

The CLAIM pair is a REWRITE — containment test, run mechanically before
emission: `TO contains FROM: false` — so its gate is a FROM-zero / TO-one count
and never an append obligation. `PLANF257R1` and `CTXF257R1` are WHOLE-FILE
replacements. `DECF257D1` and `DECF257D2` are APPENDS to `.agent/decisions.md`,
in that order, each separated from what precedes it by exactly one blank line.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C2; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's Open PR Gate
output, the merge result, BASE from `git rev-parse HEAD` on `main` after the
pull, `git branch --show-current`, and `git status --porcelain | wc -l` after
each of C0a, C0b, C1 and C2.

G2 TRANSPORT. One digest comparison, per the gate budget. Compute sha256 and the
byte length of the committed blob `git show <C0a>:.agent/authored/f257-r1.md`
and of the reviewer's own original at `.remedy-wt/f257-r1-block.md`, and report
both digests, both lengths and whether they are EQUAL. That original was written
before this worker existed and is not the worker's output, so the reading covers
more than self-consistency; say so in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r1.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE STATE SLICES AT C1. Byte equality only, per the gate budget:
`.agent/plan.md` at C1 equals PLANF257R1 including the trailing newline, and
`.agent/context.md` at C1 equals CTXF257R1 including it. Report both as `True`
or `False`, and report `wc -l` of `.agent/plan.md`, which must be under 50
(AGENTS.md). Report the count of lines exactly `## Goal` and exactly
`## Next Steps` in `.agent/plan.md`, and of lines exactly `## Active Branch` in
`.agent/context.md`.

G4 THE DECISIONS APPEND AT C1, two readers. (a) The BASE blob of
`.agent/decisions.md`, plus a newline, plus DECF257D1, plus a newline, plus
DECF257D2, equals the C1 blob — report `True` or `False`. NEGATIVE CONTROL: flip
one byte at an offset your script confirms lies INSIDE THE FIRST appended
paragraph, recompute, and report that the equality is now `False`. (b) Split the
C1 blob on blank lines; let N be the number of paragraphs the two slices hold
TOGETHER, COUNTED BY YOUR SCRIPT from the slices themselves and never taken from
this block; report N, and report that the LAST N units of the file match those
paragraphs IN ORDER, unit by unit. Report that the pre-round blob is a byte
PREFIX of the C1 blob, with both byte lengths.

G5 THE CLAIM AT C2. Report, over `docs/roadmap/STATUS.md` at C2: the count of
CLAIMFROM (must be 0) and of CLAIMTO (must be 1); that CLAIMTO's text is present
as a WHOLE LINE and how many times; and the count of lines matching
`^- \[~\] F\d{3} — `, which `tests/docs/test_docs_consistency.py` requires to be
at most 1. Report the count of lines matching `^- \[x\] F\d{3} — ` before and
after C2 — it must be UNMOVED at 61.

G6 THE SUITES AT C2. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its REAL exit code and its own passed/failed
line: `tests/docs/` and `tests/orchestration/test_roadmap_index.py`, which this
round's `docs/roadmap/**` path requires; the four state readers
`tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
`tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G7 STRUCTURE, over `BASE..<C2>` — the range that ends BEFORE the handback
commit, because C3's own numbers cannot exist while C3 is being written. Report
`git diff --name-only` and both residues against the change set above, printed
in both directions and both expected empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and report that each of C0a, C0b, C1 and
C2 is single-parent. Report, counted affirmatively over each file's C2 content
rather than inferred from a silent grep, the number of lines beginning
`<<<SLICE ` and `<<<END ` in `.agent/plan.md`, `.agent/context.md`,
`.agent/decisions.md` and `docs/roadmap/STATUS.md` — each expected 0 — beside
the same counts over `.agent/authored/f257-r1.md` as the non-zero control.
Report `git ls-files .remedy-wt | wc -l`, expected 0.

### Handback

Rewrite `.agent/handoff.md` in C3 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F257 · round 1`; the range `BASE..HEAD` with BASE
spelled as the real SHA constraint 0 reported; a per-commit changed-files table
whose `+/-` cells are taken from `git diff --numstat` and compared cell by cell
against the figures G7 reports; ONE LINE PER GATE G1 through G7 with its real
result; the deviations, including every guard re-expression constraint 6
required; the item-status table with every C-item and every gate appearing
exactly once; and the next expected action.

Do not write a `Done:` or `Gate:` paragraph anywhere — only reviewer-authored
text sets those, and a worker-authored one is a finding however hedged.

After C3: push with `git push -u origin feature/f257-self-use-track` and report
the outcome. Do NOT create a pull request and do NOT merge anything beyond
constraint 0's merge of pull request 220.
