# Handback — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 22 · The closure sequence's first half: Built State, the one checklist pass, the self-use item and the feature's one full suite

## Session

SESSION 5 of feature F283 · round 22 · rounds so far 22

This round booked round 21's PASS and resolved R-1033 on the record, wrote
`docs/roadmap/features/T2_F283.md`'s `## Built State` section, folded this
feature's one prose lesson into checklist item 34 of
`docs/agents/planner_reviewer_prompt.md`, generated and ran the closure's
self-use item (SU-026, "Address ledger finding R-0950") to the approval gate
under the `self_use` role's real configured provider, and ran the feature's
ONE full suite in the primary checkout: **18503 passed, 20 skipped, 1
warning**, exit 0, zero bad node ids. Every gate ran clean; no deviation from
the block's ordered commit sequence was needed.

Context self-assessment: a comfortable majority of the working budget
remained at the point this handoff was written, after the two slow steps
(the real self-use job, ~513s, and the full suite, ~249s) both ran once and
to completion.

## Range

Review of `0838fc12`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 199 | 199 | True |
| sha256 | `540c3caaaf2f637bd7ac24facf3a1b6b76a6559114d0103736b4117a9ba8399f` | `540c3caaaf2f637bd7ac24facf3a1b6b76a6559114d0103736b4117a9ba8399f` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `0838fc12`, matching the delegation message.
- `git branch --list 'remedy/job-*' | wc -l`, before C1: **37**.
- `git worktree list`, before C1: the primary checkout alone.

## Commits

### 4c9abbef F283 R22 C1: copy round 22 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r22-block.md | +199/-0 | byte-for-byte copy of this round's step block (`shutil.copyfile`) |
| .agent/authored/f283-r22-checklist_from.txt | +2/-0 | byte-for-byte copy of checklist_from.txt |
| .agent/authored/f283-r22-checklist_to.txt | +14/-0 | byte-for-byte copy of checklist_to.txt |
| .agent/authored/f283-r22-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r22-plan.md | +34/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **253** (199+2+14+4+34).

### 068a04f9 F283 R22 C2: book round 21's PASS and resolve R-1033
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append ledger.md payload: round 21's `Gate:` entry and R-1033's `Done:` paragraph |
| .agent/plan.md | +13/-14 | rewrite to plan.md payload, byte-identical |

Measured insertions: **17** (4+13); 14 deletions from the plan.md rewrite.

### 50876cc0 F283 R22 C3: write the feature file's Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F283.md | +74/-0 | NEW `## Built State` section: what meets each of the 5 Acceptance lines and where (the sweep + per-module tests for the envelope, the ratchet test for the empty read-only set, the exit-code taxonomy's module/guide/test), R-1019 (resolved F283 R8) and R-1020 (resolved F283 R4) with their landing commits, DECISIONS F283 D1 to D13 as one clause each, and the two new files this feature added (`apps/cli/exit_codes.py`, `tests/cli/test_json_contract.py`) |

Measured insertions: **74**.

### 09441a92 F283 R22 C4: fold F283's prose lesson into checklist item 34
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +12/-0 | applied the checklist_from/checklist_to payload pair verbatim (an APPEND, since TO contains FROM): item 34 gains one further KIND of target — a GENERATED LIST a new file JOINS (`tests/orchestration/import_reachability_allowlist.txt`), naming F283's own round 20 as the instance |

Measured insertions: **12**.

### 2087067b F283 R22 C5: generate and run the closure's self-use item, record its defects
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8/-0 | `generate_and_append_if_empty()` appended SU-026, "Address ledger finding R-0950", `consumed_by` empty (untouched — the closure round's own edit) |
| .agent/selfuse_f283/SU-026.md | +8/-0 | the rendered job markdown, copied from the planned job file |
| .agent/selfuse_f283/entry_and_job_file.txt | +5/-0 | entry id/title/provenance/consumed_by and the job file path |
| .agent/selfuse_f283/execution_config.txt | +39/-0 | the returned `JobPlan.execution_config`, serialized — proof of which provider ran |
| .agent/selfuse_f283/result_state.txt | +10/-0 | job state, stop fields, error, and each task's status/verdict/final_status |
| .agent/selfuse_f283/run_defects.txt | +4/-0 | `describe_self_use_run_defects(plan)`'s two strings, verbatim |
| .agent/selfuse_f283/timing.txt | +6/-0 | start/finish timestamps and elapsed seconds, plus the job's own created/first_running/stopped fields |
| .agent/selfuse_f283/full_transcript.txt | +13/-0 | job id, title, state, execution config and a per-task summary |

Measured insertions: **93** (8+5+39+10+4+6+13+8).

### C6 — THE INTEGRATION GATE AND THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-closure-suite.txt | new | the full suite's command, real exit code, summary line, and the (empty) bad-node-id list |
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the commit that writes it.

## External actions

- `python3 .remedy-wt/f283-r22-scratch/run_selfuse.py` — ran the real self-use
  job via `run_next_self_use_item`, `dest_dir=".remedy-wt/f283-r22-selfuse"`
  (untracked, under `.remedy-wt/`), no `builder_name`/`reviewer_name` passed.
  Left behind: branch `remedy/job-129b3ad7206d4f8d` and worktree
  `.remedy-wt/job-129b3ad7206d4f8d` — **not deleted**, per constraint 7 (a
  self-use run's leftovers are reported, never removed, and a branch is
  never deleted).
- `git push origin feature/f283-machine-contracts-part-two` after this
  commit — real outcome reported in the session reply, since it ships this
  very file.
- `gh pr list --state open ...` after the push — real outcome reported in
  the session reply.
- **NOTHING IS MERGED, NOTHING IS CLOSED.** No `gh pr merge`, no
  `gh pr create`, no checkout of `main`, no STATUS edit, no `consumed_by`
  edit, no review zip, no evidence job.
- `git stash` was **not** used at any point this round.

## Verification

### G1 — TRANSPORT: payloads, then the five authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 4/4 | 4583/4583 | True |
| plan.md | 34/34 | 1525/1525 | True |
| checklist_from.txt | 1/1 | 164/164 | True |
| checklist_to.txt | 13/13 | 1118/1118 | True |

**All four payload readings equal: True.**

Five `.agent/authored/f283-r22-*` blobs, each read back from the committed
tree with `git show 4c9abbef:<path>` and compared byte-for-byte with its
source (the block copy against `.remedy-wt/f283-r22-block.md`):

| copy | equal to source |
|---|---|
| f283-r22-block.md | True (14271 bytes both) |
| f283-r22-ledger.md | True (4583 bytes both) |
| f283-r22-plan.md | True (1525 bytes both) |
| f283-r22-checklist_from.txt | True (164 bytes both) |
| f283-r22-checklist_to.txt | True (1118 bytes both) |

**Copies compared: 5. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`0838fc12`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 555322 | 4583 | 559905 | True |

Matches the block's stated composition exactly (559905).

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R21 — ` = **1**,
`^Done: R-1033 — ` = **1**. Open set by distinct id, via `open_finding_ids`
from `scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `0838fc12` | **26** |
| C2 (`068a04f9`) | **25** |

Added: `[]`. Removed: `['R-1033']`. Matches the block's stated 26 → 25,
REMOVED `R-1033`, ADDED none, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload (`8f1606f409ab07a9920b784d632029cc4fc08ae236859e706fea0d6fa803659b`
both). Line count: **34**, under the AGENTS.md 50-line rule.

### G3 — THE DOCS

`checklist_from.txt`'s text occurs **exactly ONCE** in
`docs/agents/planner_reviewer_prompt.md` both before C4 and after (the pair
is an APPEND, since `TO contains FROM`): confirmed by direct substring count
(1 → 1). Every one of `checklist_to.txt`'s 12 lines beyond `checklist_from.txt`
appears exactly once among C4's diff-ADDED lines (`git diff` shows exactly
those 12 lines as `+`, nothing else).

The numbered items of the pre-emission checklist, read mechanically
(`re.findall(r"^  (\d+)\. \*\*", text, re.M)[:34]`):

| when | count | numbers |
|---|---|---|
| before C4 | 34 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37 |
| after C4 | 34 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37 |

Same numbers, same order — matches the block's stated reading exactly.

`python3 -m pytest tests/docs/ -q`:

| when | result | exit |
|---|---|---|
| after C3 | 315 passed in 84.96s | 0 |
| after C4 | 315 passed in 85.72s | 0 |

### G4 — THE SELF-USE ITEM

**(a) Generation.** `generate_and_append_if_empty(queue_path=..., ledger_path=...)`
answered `SU-026`, title "Address ledger finding R-0950", provenance
`generated (self-use-generator tier 1, ledger scan, R-0950)` — the same item
the reviewer's dry run at `0838fc12` predicted. `next_self_use_item(queue)`
afterward answered the same entry, `SU-026`.

**(b) The run.** `run_next_self_use_item(Path(".remedy-wt/f283-r22-selfuse"), repo_path=".", queue_path=QUEUE)`,
no `builder_name`/`reviewer_name` passed. Returned:

- entry: `SU-026`, "Address ledger finding R-0950"
- job file path: `.remedy-wt/f283-r22-selfuse/SU-026.md` (copied verbatim
  into `.agent/selfuse_f283/SU-026.md`)
- job id: `129b3ad7206d4f8d`
- job state: **blocked**
- error: `task_T001_gate_failed: final_status=provider_unavailable;
  missing_reviewer_output`
- elapsed: 513.4 seconds

`execution_config` (the proof of which provider actually ran):
`builder="claude-cli"` (source `cli`), `builder_model="claude-sonnet-4-6"`
(source `cli`), `builder_effort="medium"` (source `cli`),
`reviewer="claude-cli"` (source `cli`), `reviewer_model="claude-sonnet-4-6"`
(source `cli`), `reviewer_effort="medium"` (source `cli`) —
the `self_use` role's own configured frontier provider, never the raw
`"fake"` fallback (DECISION amend0920-selfuse-real D2). The run was **never
applied** — it stopped at the normal approval gate, `JOB_BLOCKED`.

**(c) `describe_self_use_run_defects(plan)`** answered a 2-tuple, both
strings written verbatim to `run_defects.txt`:

1. `job 129b3ad7206d4f8d (blocked): task_T001_gate_failed: final_status=provider_unavailable; missing_reviewer_output`
2. `T001 (blocked): completion_gate_failed: final_status=provider_unavailable; missing_reviewer_output`

**No finding was registered from these strings** — that is the reviewer's
act at the next round, per the block's own instruction.

**(d)** `python3 -m pytest tests/docs/ -q` after the queue write: **315
passed**, exit 0 — matches the reviewer's dry-run reading exactly, so
`tests/docs/test_retired_promote_word.py`'s `KEPT_BY_SENSE` guard did NOT go
red on SU-026's text, and no repair to that file was needed or made.

**`remedy/job-*` branch count and worktree list:**

| when | branch count | worktree list |
|---|---|---|
| before C1 | 37 | primary checkout alone |
| after C5 | 38 | primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` |

The one new branch and worktree are the self-use run's own leftover
(constraint 7): reported here, **not deleted**.

### G5 — THE INTEGRATION GATE

`python3 -m pytest -n auto -q` in the primary checkout, after C5:

```
18503 passed, 20 skipped, 1 warning in 248.77s (0:04:08)
```

Real exit code: **0**. Bad node ids (FAILED/ERROR): **NONE** — searched
mechanically (`grep -c "^FAILED\|^ERROR"` on the raw log) and found zero.
`tests/orchestration/test_import_reachability.py` and
`tests/test_no_orphan_modules.py`: **neither is among the bad nodes**,
because the bad-node set is empty (closure precondition 7 holds).

`python3 -m apps.cli.main integrity check --json`: all five checks
(`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) read `"status": "pass"`,
`"fail_count": 0`, `"passed": true`, exit 0.

`git status --porcelain` (before this commit): only
`.agent/authored/f283-closure-suite.txt` untracked — no other relevant
untracked file (closure precondition 3 holds once this commit lands).

## Authored-text proofs

- The five copies at C1, compared with the block's originals under
  `.remedy-wt/f283-r22-payloads/` and `.remedy-wt/f283-r22-block.md`: **five
  readings, all True** (G1).
- The one APPEND payload against its committed file: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md,
  555322+4583=559905, G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- The one checklist APPEND pair against its committed file: `checklist_from.txt`
  stays at exactly one occurrence, and every one of `checklist_to.txt`'s
  new lines appears exactly once among C4's diff-added lines (G3).
- No payload was edited or retyped. The block copy and four payload copies
  at C1 were made with `shutil.copyfile`; the one append by reading the
  payload's bytes and writing base+payload back to disk; the plan.md
  rewrite by `shutil.copyfile`, then verified sha256-equal; the checklist
  pair applied with a single `str.replace(FROM, TO)` over the file's own
  text, read from the payload files on disk, never retyped.
- C3's Built State prose is WORKER-authored to the block's SPEC (it names
  the reviewer, not the worker, as author of the RECORD payloads and the
  checklist pair; the Built State is explicitly the worker's to write) —
  there is no reviewer-authored diff to compare it against.

## Deviations & assumptions

None. The block's six commits landed in order with no extra, dropped or
reordered commit; every constraint held; every gate read clean at every
required point.

1. **Constraint 1** (no payload edited or retyped): held — `shutil.copyfile`
   for C1's five copies and the plan.md rewrite; byte-read-then-write for
   C2's one append; `str.replace` over disk-read payload bytes for C4's pair.
2. **Constraint 2** (every commit under 500 insertions by `git show
   --numstat`): held — 253, 17, 74, 12, 93; this handoff commit exempt as a
   single `.agent/**` state file (plus the small closure-suite.txt beside it).
3. **Constraint 3** (the round's tracked path set is at most the block's
   enumeration): held — the round's whole path set (16 distinct paths before
   this commit, listed below) is a SUBSET of the enumeration; the one
   discretionary allowance (`tests/docs/test_retired_promote_word.py` under
   C5(d)) was NOT needed, since `tests/docs/` stayed green at 315 passed
   throughout.
4. **Constraint 4** (a RED full suite is this feature's own work, not a
   stop reason): not invoked — the suite came back fully green (18503
   passed, 20 skipped, 0 failed/errored).
5. **Constraint 5** (STOP if a gate goes red outside constraint 3's editable
   scope): not invoked — no such red occurred anywhere in the round.
6. **Constraint 6** (nothing merged, nothing closed): held — no
   `gh pr merge`, no `gh pr create`, no checkout of `main`, no STATUS edit,
   no `consumed_by` edit, no review zip, no evidence job.
7. **Constraint 7** (the self-use run's leftovers are reported, not
   deleted, and no branch is ever deleted): held — `remedy/job-129b3ad7206d4f8d`
   and its worktree left exactly as the run created them (branch count
   37→38, worktree list primary-only→primary-plus-one).
8. `git stash` was never used this round.

One observation, not a deviation: the self-use job (SU-026, addressing
R-0950) ended `blocked` on `provider_unavailable; missing_reviewer_output` —
a real infrastructure hiccup on the reviewer side of the loop during this
particular call, not a curation defect (planning did not block it; it
blocked mid-run, which the runner's own docstring names as an ordinary,
expected outcome). This is exactly the kind of outcome `describe_self_use_run_defects`
exists to surface, and it is left for the reviewer to register, per the
block's own instruction not to register findings here.

A second observation: R-0950 (the finding SU-026 itself targets) describes
four closure-suite nodes that reproduced as bad under `-n auto` in an
earlier session but reproduced green on isolated re-runs, calling the
failure flaky/cross-test-pollution-shaped rather than tied to any F280
round. This round's own full-suite run came back with **zero** bad nodes at
all, consistent with R-0950's own description of an intermittent rather
than a deterministic failure.

### The round's whole tracked path set (before this commit)

`git diff --name-only 0838fc12 HEAD` — **16** distinct paths; plus
`.agent/authored/f283-closure-suite.txt` and `.agent/handoff.md` from this
commit make **18** — a SUBSET of constraint 3's full enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r22-block.md | C1 `4c9abbef` |
| 2 | .agent/authored/f283-r22-checklist_from.txt | C1 `4c9abbef` |
| 3 | .agent/authored/f283-r22-checklist_to.txt | C1 `4c9abbef` |
| 4 | .agent/authored/f283-r22-ledger.md | C1 `4c9abbef` |
| 5 | .agent/authored/f283-r22-plan.md | C1 `4c9abbef` |
| 6 | .agent/live_review.md | C2 `068a04f9` |
| 7 | .agent/plan.md | C2 `068a04f9` |
| 8 | docs/roadmap/features/T2_F283.md | C3 `50876cc0` |
| 9 | docs/agents/planner_reviewer_prompt.md | C4 `09441a92` |
| 10 | scripts/self_use_queue.json | C5 `2087067b` |
| 11 | .agent/selfuse_f283/SU-026.md | C5 `2087067b` |
| 12 | .agent/selfuse_f283/entry_and_job_file.txt | C5 `2087067b` |
| 13 | .agent/selfuse_f283/execution_config.txt | C5 `2087067b` |
| 14 | .agent/selfuse_f283/result_state.txt | C5 `2087067b` |
| 15 | .agent/selfuse_f283/run_defects.txt | C5 `2087067b` |
| 16 | .agent/selfuse_f283/timing.txt | C5 `2087067b` |
| 17 | .agent/selfuse_f283/full_transcript.txt | C5 `2087067b` |
| 18 | .agent/authored/f283-closure-suite.txt | C6 (this commit) |
| 19 | .agent/handoff.md | C6 (this commit) |

No path outside constraint 3's enumeration was touched: nothing under
`packages/`, nothing under `apps/`, no `docs/roadmap/STATUS.md`, no root
`README.md`, no other file under `scripts/`, and none of
`.agent/candidates.md`, `.agent/context.md`, `.agent/operator_questions.md`,
`.agent/decisions.md`, `.agent/prose_slips.md` appear.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `0838fc12`; block 199 lines / matching sha256 |
| C1 copy block + 4 payloads | done | 253 insertions |
| C2 book round 21 PASS, resolve R-1033 | done | 17 insertions, 14 deletions; open set 26→25, removed R-1033, added none |
| C3 the feature file's Built State | done | 74 insertions; all 5 Acceptance lines addressed, R-1019/R-1020 rounds named, DECISIONS D1–D13 listed, 2 new files named |
| C4 fold the prose lesson into checklist item 34 | done | 12 insertions; FROM stays at 1 occurrence, 34 items before/after, same order |
| C5 the self-use item | done | SU-026 generated and run to the approval gate under claude-cli/claude-sonnet-4-6 (self_use role); JOB_BLOCKED on provider_unavailable; 2 defect strings recorded verbatim; tests/docs/ stayed green (315 passed) |
| C6 the integration gate + handback | done | this commit |
| G1 payload transport + authored copies | done | 4/4 payload readings equal; 5/5 authored copies byte-identical |
| G2(a) live_review.md append | done | 555322+4583=559905 |
| G2(b) line-anchored gate lines + open set by distinct id | done | 1 each of the 2 named lines; 26→25, removed R-1033, added none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 34 lines, under 50 |
| G3 the docs | done | FROM count 1→1; 12 TO-only lines each appear once in the diff; 34 items before/after, same order; tests/docs/ 315 passed twice |
| G4 the self-use item | done | generator/queue answers, execution_config, defects, tests/docs/ 315 passed, branch/worktree counts 37→38 |
| G5 the integration gate | done | 18503 passed, 20 skipped, 1 warning, exit 0, zero bad nodes; the two named closure-precondition tests are not among them (there are none); integrity all 5 pass; git status clean |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile` / bytes read+write / `str.replace` over disk-read payloads only |
| Constraint 2 every commit under 500 insertions | done | 253, 17, 74, 12, 93; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 16 paths before this commit (19 after), a SUBSET of the full enumeration; the one discretionary path not needed |
| Constraint 4 a red suite is work, not a stop reason | done (n/a) | suite came back fully green |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no such red occurred |
| Constraint 6 nothing is merged, nothing is closed | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no STATUS/consumed_by edit, no zip, no evidence job |
| Constraint 7 self-use leftovers reported, not deleted | done | `remedy/job-129b3ad7206d4f8d` + worktree, left alone, counts reported |
| `git stash` used | done (n/a) | never used this round |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk. While it exists, write nothing and end.
2. The review of round 22 — C1 through C6, all gates re-derived.
3. Then the closure sequence's second half: the registrations the self-use
   run's own defect strings ask for, the evidence job, a fresh review zip,
   the ledger rotation, the STATUS line with the README counters in the
   same commit, and the pull request (never merged in the session that
   opens it).

Open findings count: **25**. Operator-questions count: **0**.
