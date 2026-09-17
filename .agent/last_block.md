# F281 Round 2 — step block

## Goal

Book round 1's PASS, record DECISION F281 D2 (the scope boundary for the F259
enforced-vocabulary flip), and land a verified first slice of the catalog
description rewrite: the full Contract/Roadmap/Plan/Worker meaning-violation
buckets (13 descriptions, 19 total violations once each description's OTHER
binding words were checked too) plus the 4 of 6 retired-"loop"-synonym
offenders that are pure prose (not a persisted or tested CLI literal).

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r2.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD1 + DECISION2 + PLAN2 — one commit.
C2: CODE — the 18 catalog text edits in `apps/cli/command_catalog.py`.
C3: HANDBACK.

## C1 — RECORD1 + DECISION2 + PLAN2

### RECORD1 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F281 R1 — the F281 round 1 entry. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `c617dd74`..`01fb61d1` (commits `f427225c`, `b53154aa`, `62d65f9c`, `6352b176`, `dd56b151`, `01fb61d1`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r1.md` and `.agent/last_block.md` are byte-identical to the reviewer's own authored block, sha256 `cfed923da9ec02aaced12bfbf2b4fd6845bf9fcc0207538702368e5cbfb116d7`, 20608 bytes, reproduced directly by `cmp` and `sha256sum`. THE STATE: over `.agent/live_review.md` after C1's append, `^Gate: ` reads 25, distinct `^- R-\d+ — ` ids read 137 (the base's 136 plus exactly R-0954), distinct `^Done: R-\d+ — ` ids read 5 unchanged, the open set by distinct id reads 132 — all reproduced directly. THE CANDIDATE: `.agent/candidates.md`'s CANDIDATE paragraph is replaced with "EMPTY — no candidate is open." plus a discharge note naming R-0954, reproduced directly; the F275/F109/F108 historical notes below it are untouched. THE CLAIM: `docs/roadmap/STATUS.md`'s F281 line reads `[~]`, the sole byte changed on that line, reproduced directly. THE DECISION: DECISION F281 D1 is present verbatim in `.agent/decisions.md`, naming the 3 production rename sites and the 7 untouched ones. THE CODE: `apps/cli/commands/do_cmd.py:618,621` and `packages/orchestration/pingpong_evidence.py:230,232` read `Builder:`/`Builder write mode:`, and `tests/cli/test_cli_ux.py:592,665` read `assert "Builder:" in out` — reproduced directly by `git show` on `dd56b151`. THE GATES, reproduced directly by the reviewer at HEAD: `python3 -m pytest tests/cli/test_cli_ux.py tests/orchestration/test_evidence_bundle.py tests/orchestration/test_job_evidence.py -q` reads `227 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `grep -rn "Worker:" apps/ packages/ tests/ --include=*.py --include=*.tsx` reads exactly the 7 untouched sites DECISION F281 D1 names (`worker.py:67,227`, `brain_viewer.py:559,975`, `brain_detail.py:1175`, `project_brain.py:630`, `RightLivePanel.tsx:41`) plus 2 unrelated comment lines in `test_vocabulary.py` and one unrelated class name, and zero remaining in `do_cmd.py`/`pingpong_evidence.py`/`test_cli_ux.py`; `python3 -m ruff check apps/cli/commands/do_cmd.py packages/orchestration/pingpong_evidence.py tests/cli/test_cli_ux.py` reads `All checks passed!`. THE RED-PROOF, independently re-run by the reviewer in a disposable worktree at HEAD (`git worktree add --detach .remedy-wt/f281-review`, removed after, confirmed by `git worktree list`): reverting `do_cmd.py:618` alone from `Builder:` back to `Worker:` reddened `tests/cli/test_cli_ux.py::TestTextReportTokenProof::test_text_report_shows_provider_evidence` (`AssertionError: assert 'Builder:' in out`) against a green control of the same node; reverted, green again. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `01fb61d1` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every file this round touched is exactly the path set its own commits declare, every byte independently reproduces, and the mutation red-proof confirms the rename is load-bearing rather than cosmetic.
```

### DECISION2 — append to `.agent/decisions.md`, after its current last line
(after DECISION F281 D1), verbatim (with today's date):

```

## DECISION F281 D2 (2026-09-17, F281 round 2) — two of the six retired-synonym offenders are structurally unreachable by this feature, and the F259 enforced flip is bounded by them

CONTEXT. T001 orders the F259 `VOCABULARY_MODE` flip to `enforced`
(`tests/docs/test_vocabulary.py`), gated by two mode-dependent checks:
`_synonym_offenders()` (6 hits measured at F281's claim) and
`_meaning_violations()` (294 hits). `_synonym_offenders()` scans, per DECISION
F259 D3's own scope, "every group's `id`, `label` and `description`, and every
command's `command_id`, `description`" — not prose alone. Two of the six hits
are not prose this feature may reword: `command:dev.agent-loop:command_id` is
the command's own id, and `docs/roadmap/features/T2_F281.md`'s Do-not-touch
clause states "the catalog's set of groups and commands is F280's; this
feature changes no command id." `arg:do.run:--fixture-builder:description`
names a real, load-bearing CLI value: `_VALID_FIXTURE_MODES` in
`apps/cli/commands/do_cmd.py:680` is the frozenset `{"true", "false",
"repair-loop"}`, and `"repair-loop"` by that exact spelling is asserted as a
literal parsed value in `tests/test_cli_execution_loop_closure.py`,
`tests/test_repair_context_reviewer_memory.py` and
`tests/cli/test_do_cmd_summary.py`, and named as a whole feature pair
(`docs/system/repair-loop-v0.md`, `repair-loop-v1.md`) that `docs/README.md`
indexes. Rewording the ArgDef's help text to avoid the word "loop" while still
naming the real accepted value truthfully is not possible; renaming the value
itself is a behaviour change to what the command accepts, which
`docs/roadmap/features/T2_F281.md`'s own scope statement forbids ("this
feature rewrites what help says, not what a command does").

CHOSEN. This round fixes the four synonym offenders that ARE pure prose —
`command:mission.run:description`, `group:mission:description`,
`arg:mission.run:run_id:description` (all three: "F070 orchestrator loop" →
"F070 orchestrator", no persisted or tested literal involved — confirmed by
grep, zero hits for the exact phrases before this round's edit) and
`command:dev.agent-loop:description` (its command_id is untouched; only the
description's own wording changes, since `_cmd_agent_loop` is in fact a
read-only inspector — it derives and prints a state summary, per
`apps/cli/commands/brain.py:489-513` — not an executor of a loop, so the
reword is also a correctness improvement, not only a synonym dodge). The
remaining two — `dev.agent-loop`'s command_id and `--fixture-builder`'s
`repair-loop` value — are LEFT NAMED AND UNFIXED, and this decision is the
record of why: the `enforced` flip's Acceptance line is met against a floor of
these two, not against zero, until a later DECISION either narrows
`_synonym_offenders()`'s own scanned fields (an amendment to DECISION F259
D3) or an operator ruling exempts these two named surfaces by id.

ALTERNATIVES CONSIDERED. Renaming `dev.agent-loop`'s command_id anyway (e.g.
to `dev.agent-status`) — rejected: it is a command-catalog rename, squarely
inside F280's remit and this feature's own Do-not-touch, and `dev` group
commands are debugging surfaces with no F281 mandate to touch. Renaming the
`repair-loop` VALUE to something synonym-clean (e.g. `repair-cycle`) —
rejected: it is a behaviour change (the CLI would stop accepting a value
operators and three test files already depend on), squarely the "not what a
command does" boundary this feature's own scope statement draws; if ever
wanted, it is a DECISION for whichever feature owns `do run`'s flag surface,
with a measured blast radius across the test and docs files named above.
Leaving all six offenders untouched this round — rejected: four of them cost
nothing but a reword and no test or doc depends on their current spelling.

CONSEQUENCE. After this round, `_synonym_offenders()` reads 2
(`arg:do.run:--fixture-builder:description`, `command:dev.agent-loop:command_id`),
down from 6; `VOCABULARY_MODE` stays `"planned"` — flipping it now would
correctly assert `offenders == []` and fail on these two. HOW TO REVERSE:
revert round 2's C2 commit; delete this paragraph.
```

### PLAN2 — replace the entire content of `.agent/plan.md` with exactly:

```
# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request 253
(F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 once F280 has pruned and renamed the
command tree (`docs/roadmap/features/T2_F281.md`). DONE when T001 and the
Acceptance list hold.

## Current Step

ROUND 2. C1 books round 1's PASS, records DECISION F281 D2 (two of the six
retired-"loop"-synonym offenders — `dev.agent-loop`'s command_id and
`--fixture-builder`'s `repair-loop` value — are structurally unreachable by
this feature; the F259 enforced flip is bounded by them, not by zero), and
re-points `.agent/plan.md`. C2 rewrites 18 catalog text fields in
`apps/cli/command_catalog.py`: the full Contract/Roadmap/Plan/Worker
meaning-violation buckets (13 descriptions/help strings, 19 violations —
several descriptions carried more than one binding-word violation once
checked against every word, not only the one first measured) and the 4 of 6
"loop"-synonym offenders that are pure prose.

## Next Steps

1. `tests/docs/test_vocabulary.py` now measures 275 meaning-violations (was
   294) and 2 synonym-offenders (was 6, floor per DECISION F281 D2). The
   remaining 275 break down by binding word: Job 125 (or fewer — some Job
   violations may already have cleared as a side effect of a shared
   description; re-measure at the start of the next round rather than
   trusting this figure), Project ~65, Run, Mission, Order, Evidence, Task,
   Decision, Plan (any left outside this round's 4), Contract (any left
   outside this round's 1) — re-run `_meaning_violations()` grouped by word at
   the start of round 3 and take the next-smallest remaining bucket, the same
   pattern this round used (smallest buckets first, to build the rewrite
   pattern before the two large ones).
2. Help wrap, the `doctor core` dead-commands section (D11d), the D11a
   catalog group-reach test, the visible-order data-pinned test, the F259
   enforced flip itself (once the description buckets are clear and DECISION
   F281 D2's two-item floor is either accepted as the flip's final state or
   separately resolved), and the README quickstart's R-0895 line remain
   entirely undone.

## Risks

- Every catalog description edit is verified by re-running
  `tests/docs/test_vocabulary.py`'s own `_meaning_violations()` and
  `_synonym_offenders()` functions against the modified catalog BEFORE
  authoring, and by a full literal-string sweep for the two synonym floor
  items to confirm no round accidentally "fixes" them by editing text that
  isn't the command_id or the ArgDef value itself.
- A description rewrite that adds a binding word's own fragment can
  accidentally introduce a DIFFERENT binding word without ITS fragment (round
  2 caught this on `worker.list`/`worker.show`/`worker.doctor`/`group:worker`,
  where a first-draft rewrite added a bare "run" verb, tripping the `Run`
  check it hadn't tripped before); every rewrite in this feature is checked
  against the FULL violation diff (fixed vs. introduced), never just the one
  word it targeted.
```

## C2 — CODE (the 18 catalog text edits, all in `apps/cli/command_catalog.py`)

Apply each FROM → TO pair below EXACTLY. Every FROM string must appear
verbatim, once, at the cited line; if it does not match, STOP and report the
exact mismatch rather than adapting it.

1. Line 121 (GROUPS["worker"]). FROM:
```
    "worker": GroupDef("worker", "Worker", "Manage worker connections."),
```
TO:
```
    "worker": GroupDef("worker", "Worker", "Manage the workers that support a role: builder, reviewer, planner or teacher."),
```

2. Line 130 (GROUPS["mission"]). FROM:
```
    "mission": GroupDef("mission", "Mission", "Persistent goals above jobs, and the bounded run-loop facade (internal)."),
```
TO:
```
    "mission": GroupDef("mission", "Mission", "Persistent goals above jobs, and the bounded orchestrator facade (internal)."),
```

3. Line 141 (GROUPS["roadmap"]). FROM:
```
    "roadmap": GroupDef("roadmap", "Roadmap", "Read-only roadmap mirror — what is active, what is next. Proposes, never starts.", user_facing=False, hidden=True),
```
TO:
```
    "roadmap": GroupDef("roadmap", "Roadmap", "Read-only mirror of Remedy's own roadmap — what is active, what is next; proposes, never starts.", user_facing=False, hidden=True),
```

4. `test.run` CommandEntry (near line 583). FROM:
```
        description="Run discovered tests for a job (contract-gated, resource-safe).",
```
TO:
```
        description="Run the discovered tests for a job's tasks, gated by its contract (the job's acceptance criteria) and resource-safe.",
```

5. `worker.list` CommandEntry (near line 802). FROM:
```
        description="List known worker provider specs.",
```
TO:
```
        description="List the worker provider specs available for each role: builder, reviewer, planner or teacher.",
```

6. `worker.show` CommandEntry (near line 812). FROM:
```
        description="Show details of a single worker adapter.",
```
TO:
```
        description="Show the details of a single worker adapter: the model and the roles (builder, reviewer, planner, teacher) it supports.",
```

7. `worker.status` CommandEntry (near line 847). FROM:
```
        description="Show current worker status.",
```
TO:
```
        description="Show the current status of each worker: which role (builder, reviewer, planner or teacher) it is running, if any.",
```

8. `worker.doctor` CommandEntry (near line 857). FROM:
```
        description="Read-only: is each available worker provider's own tooling actually reachable?",
```
TO:
```
        description="Read-only: is each available worker provider's own tooling actually reachable for the roles (builder, reviewer, planner, teacher) it supports?",
```

9. The `mission` section comment (line 864). FROM:
```
    # ── mission (the F070 orchestrator loop, keyed on a mission id) ──────
```
TO:
```
    # ── mission (the F070 orchestrator, keyed on a mission id) ──────────
```

10. `mission.run` CommandEntry description (near line 869). FROM:
```
        description="Run the F070 orchestrator loop for one mission. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
```
TO:
```
        description="Run the F070 orchestrator for one mission. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
```

11. `mission.run`'s `run_id` ArgDef (near line 872). FROM:
```
            ArgDef("run_id", "Mission id (F070 loop)"),
```
TO:
```
            ArgDef("run_id", "Mission id (F070 orchestrator)"),
```

12. `job.resume` CommandEntry description (near line 1369). FROM:
```
        description=(
            "Resume a job. Without --checkpoint: continue from the newest valid "
            "cycle checkpoint (F047) — a pending stop request is consumed first, "
            "worktree drift refuses, the plan-approval gate still applies. With "
            "--checkpoint <id>: resume from that safe event-replay checkpoint."
        ),
```
TO:
```
        description=(
            "Resume a job. Without --checkpoint: continue from the newest valid "
            "cycle checkpoint (F047) — a pending stop request is consumed first, "
            "worktree drift refuses, the plan-approval gate (approving the job's "
            "tasks) still applies. With --checkpoint <id>: resume from that safe "
            "event-replay checkpoint."
        ),
```

13. `do.run`'s `--dry-run` ArgDef (line 1549 — the ONE inside the `do.run`
CommandEntry whose `related=("job.show", "change.proof")` line precedes it;
do not touch the other two `--dry-run` ArgDefs elsewhere in the file, which
belong to different commands and already carry no violation). FROM:
```
            ArgDef("--dry-run", "Show plan without executing", required=False, is_option=True, default="false"),
```
TO:
```
            ArgDef("--dry-run", "Show the plan's tasks without executing", required=False, is_option=True, default="false"),
```

14. `self.plan` CommandEntry description (near line 1899). FROM:
```
        description="Read-only: build a self-improvement plan (grouped items, top recommendations).",
```
TO:
```
        description="Read-only: build a self-improvement plan of grouped tasks and top recommendations.",
```

15. `self.plan`'s `--job-id` ArgDef (near line 1902 — the one inside the
`self.plan` CommandEntry; two OTHER `--job-id` ArgDefs exist for `self.inspect`
and `self.report` at lines 1889 and 1980 — do not touch those, they carry no
violation). FROM:
```
            ArgDef("--job-id", "Optional job to include in the plan", required=False, is_option=True),
```
TO:
```
            ArgDef("--job-id", "Optional job whose tasks are included in the plan", required=False, is_option=True),
```

16. `dev.agent-loop` CommandEntry description (near line 1993 — the
command_id itself, `"dev.agent-loop"`, is UNCHANGED per DECISION F281 D2).
FROM:
```
        description="Run the agent loop for a job (dev/testing).",
```
TO:
```
        description="Inspect the agent's cycle state for a job (dev/testing).",
```

17. `roadmap.status` CommandEntry description (near line 2023). FROM:
```
        description="Show the active roadmap feature, its blockers and its milestone.",
```
TO:
```
        description="Show the active feature in Remedy's own roadmap, its blockers and its milestone.",
```

18. `roadmap.next` CommandEntry description (near line 2036). FROM:
```
        description="Propose the next roadmap feature and its file path. Starts nothing.",
```
TO:
```
        description="Propose the next feature in Remedy's own roadmap and its file path; starts nothing.",
```

## Constraints

- Every FROM string is matched EXACTLY ONCE at its cited location before
  editing; several `--dry-run` and `--job-id` ArgDefs exist for OTHER
  commands elsewhere in the file and must NOT be touched — edit 13 and edit
  15 above name exactly which one and which two-to-avoid.
- `command:dev.agent-loop:command_id` (the string `"dev.agent-loop"` itself)
  and `arg:do.run:--fixture-builder:description` (the string containing
  `repair-loop`) are UNCHANGED this round — do not "fix" them, per DECISION
  F281 D2.
- The C2 commit's path set is exactly one file:
  `apps/cli/command_catalog.py`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.

## Gates (at most six; run and record real exit codes)

- G1 SYNONYM/MEANING DIFF: run the equivalent of this check (a Python one-liner
  or script is fine) and paste its real output: import
  `tests.docs.test_vocabulary` before and after the edit (or diff two
  invocations), and report the delta of `_synonym_offenders()` and
  `_meaning_violations()` — expect: synonym offenders 6 → 2 (fixed the 4
  DECISION F281 D2 names as pure prose, `dev.agent-loop`'s command_id and
  `--fixture-builder`'s value remain, as ordered); meaning violations 294 →
  275 (19 fixed, ZERO introduced — if any new violation appears anywhere in
  the catalog that wasn't there before this round's edit, STOP and report it
  rather than shipping it).
- G2 TARGETED: `python3 -m pytest tests/docs/test_vocabulary.py
  tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` —
  expect all pass (the two mode-dependent tests stay green in `"planned"`
  mode since offenders/violations are still non-empty after this round).
- G3 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect
  unchanged pass count (42).
- G4 SWEEP: `grep -n "F070 orchestrator loop\|repair-loop\|dev.agent-loop"
  apps/cli/command_catalog.py` — confirm the mission comment/description/
  arg-help no longer read "loop" after "orchestrator", `repair-loop` still
  appears exactly once (the untouched `--fixture-builder` ArgDef), and
  `dev.agent-loop` still appears as the command_id and subcommand strings
  (untouched) but its own `description=` field no longer contains "loop".
- G5 RUFF: `python3 -m ruff check apps/cli/command_catalog.py` reads `All
  checks passed!`.
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

No mutation red-proof is ordered this round: these are catalog description
strings read only by `tests/docs/test_vocabulary.py`'s own functions, and G1's
before/after diff against those exact functions IS the red/green proof — a
description that failed to change would show up as a missing "fixed" entry in
G1's own diff, which is a stronger, more precise proof than a hand-picked
single-node mutation would be for 18 independent text edits.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output, G1's delta matching exactly (6→2 synonym, 294→275
meaning, zero introduced); the branch is pushed; `.agent/handoff.md` is
rewritten as C3 naming this round, its commits, its verification results, and
the next expected action (round 3 re-measures the remaining 275 violations by
word and takes the next-smallest bucket, per PLAN2's "Next Steps").
