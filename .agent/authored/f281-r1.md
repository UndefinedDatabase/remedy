# F281 Round 1 — step block

## Goal

Claim F281 (CLI help surface), book F280's last unbooked round (R26), register the
one open closure candidate F280 left on disk, and land the first slice of T001 named
by the orchestrator brief: the `Worker:` → `Builder:` role-label rename in the
pingpong report renderers.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r1.md`.
C0b: mirror this block verbatim to `.agent/last_block.md` (replacing its current
content).
C1: RECORD26 + FINDING954 + PLAN1 + DECISION1 — one commit (amend0917-throughput
rule 4).
C2: CLAIM — the STATUS line flip and the context re-point.
C3: CODE — the role-label rename, its tests, and the gates.
C4: HANDBACK.

## C1 — RECORD26 + FINDING954 + PLAN1 + DECISION1

### RECORD26 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F280 R26 — the F280 round 26 entry, POST-CLOSURE CI REPAIR. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `dd62df2d`..`6626c696` (commits `2196c22e`, `6a87e5b8`, `6626c696`) plus merge commit `c617dd74` of pull request 253, and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. It is booked here, in F281 round 1's own C1, per operator amendment amend0827-process-diet rule 1 — round 26 was F280's last round and no further F280 round existed to book it. THE TRANSPORT: `.agent/authored/f280-r26.md` and `.agent/last_block.md` at `2196c22e` are byte-identical, sha256 `646bbc4ebbdc0fa7bd0de338f01671be85624282b982b7096405825ac9b6ef6e`, 13126 bytes, reproduced directly. THE STATE: over `.agent/live_review.md` at HEAD (before this append), `^Gate: ` reads 24, distinct `^- R-\d+ — ` ids read 136, distinct `^Done: R-\d+ — ` ids read 5 (the base's 4 plus exactly R-0953), the file reads 648285 bytes — all matching the handback's own G2 claim exactly. THE FIX: `tests/orchestration/test_job_fulfillment.py::TestFulfilledDemoGuide::test_guide_mentions_propose` was rewritten at `6a87e5b8` to assert the doc's real post-D10 content; the reviewer ran `python3 -m pytest tests/orchestration/test_job_fulfillment.py -q` at HEAD and reproduced `96 passed`, and `python3 -m ruff check tests/orchestration/test_job_fulfillment.py` reads `All checks passed!`. THE CI: hosted CI run `35238707435` on pull request 253 reads `pass` (18m6s), and the PR is `MERGED` at `c617dd74df26b8e677161b265a88d5926f4d78ab`, `mergedAt` 2026-09-17T15:32:28Z — reproduced directly via `gh pr view 253 --json state,mergedAt,mergeCommit` and `gh pr checks 253`. WHY PASS: the transport, the ledger arithmetic, the specific test fix and the resulting green hosted CI all reproduce exactly; the round closed the CI-repair sequence honestly and pull request 253 merged clean. Branch `feature/f280-cli-vocabulary-v2-part-two` no longer exists (deleted at merge); `main` carries `c617dd74` at HEAD as of F281's claim.
```

### FINDING954 — append to `.agent/live_review.md`, immediately after RECORD26,
separated by exactly one blank line, verbatim:

```
- R-0954 — Low, ROUND 26'S OWN BLOCK-SAVE COMMIT DROPPED THE CLOSING SEPARATOR LINE OF THE SAVED BLOCK COPY. Raised as a closure candidate by the planner and reviewer of F280 round 26's own C1; recorded on disk in `.agent/candidates.md` at commit `82940b89`, since Rule A4 had already made round 26's own commits final and no F280 round remained to register it directly, per DECISION amend0827 D2. THE DEFECT, as declared by the discovering round and not independently re-derivable now (the reviewer's in-session scratch original no longer exists as a comparable artifact): `.agent/authored/f280-r26.md`, the copy of the round's own paste block that C1 saved, is 211 bytes shorter than the block the reviewer authored, missing only the block's final closing separator line (the `──...──` rule this repository's convention puts at the end of every paste block); `.agent/last_block.md` carries the same gap, being a copy of the same file. Every PAYLOAD the block ordered (RECORD26, FINDING953, PLAN26, DONE953, TEST26) was independently verified byte-for-byte correct against its own target, so the gap is confined to the closing decorative line of the saved block copy and carries no constraint, gate or payload text of its own. WHY LOW: nothing the round certified is wrong; the gap is in a decorative line of an already-applied, already-verified block copy. FIX: the next round that saves a block under `.agent/authored/` on any feature checks whether the worker's block-save step is silently dropping trailing content in general — a mechanical check comparing the saved file's own line count against the block text's line count, run before the commit that saves it — before that habit ever drops something load-bearing rather than decorative. Owner: F273.
```

### CANDIDATES — edit `.agent/candidates.md`: replace the paragraph beginning
`CANDIDATE (2026-09-17, F280 round 26 C1)` (and ending `...load-bearing rather
than decorative.`) with exactly:

```
EMPTY — no candidate is open.

The entry F280 round 26's own C1 recorded on 2026-09-17 — the block-save transport
gap in `.agent/authored/f280-r26.md` — was registered in F281 round 1 as finding
`R-0954` in `.agent/live_review.md`; the measurement and the routing are on that
record.
```

Every other paragraph in `.agent/candidates.md` (the F275/F109/F108 historical
notes) is untouched.

### F273 ACCEPTANCE LINE — edit `docs/roadmap/features/T2_F273.md`: after the
existing bullet ending `...and the reviewer's standing \`git worktree list\`
check.` (the R-0940 bullet, immediately before the `## Do not touch` heading),
insert one new bullet:

```
- R-0954 carries a resolution line naming the commit that gives a worker's
  block-save step a line-count check of the saved file against its source block
  text, run before the commit that saves it.
```

### PLAN1 — replace the entire content of `.agent/plan.md` with exactly:

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

ROUND 1. C1 books F280 round 26's PASS (its last, unbooked round), registers
R-0954 (the block-save transport gap F280 round 26 raised as a closure
candidate) with Owner F273, empties `.agent/candidates.md`, and records DECISION
F281 D1 (the scope boundary for the `Worker:` → role-label rename — which of the
several "Worker" sites this feature's T001 touches and which it does not). C2
claims F281 on the STATUS line and re-points the context file. C3 lands the
first slice of T001, "role labels" (the orchestrator brief's own first item):
`Worker:` → `Builder:` at the three production report-renderer sites DECISION
F281 D1 names, with their two test assertions.

## Next Steps

1. The remaining slices of T001, in the orchestrator brief's order: descriptions
   (175 catalog strings; 294 measured `_meaning_violations()` plus 6
   `_synonym_offenders()` per `tests/docs/test_vocabulary.py`), help wrap, the
   `doctor core` dead-commands section (D11d, unbuilt), the D11a catalog
   group-reach test (unbuilt — `GroupDef` has no `feature`/`reach` field today),
   the visible-order data-pinned test (D4/amend0911-feedback D1's eighteen-slot
   order — no test pins it today), the F259 `VOCABULARY_MODE` flip to
   `enforced`, and the README quickstart's one surviving broken line (R-0895's
   `job create --plan plan.yaml`).
2. One open scope question the next round should read before touching
   descriptions: D11a's catalog test (per DECISION amend0905-vocab D11) and the
   F259 enforced-mode scan (per DECISION F259 D3) both read a command's
   `command_id`, and `dev.agent-loop`'s own command_id contains the retired
   word "loop" — but `docs/roadmap/features/T2_F281.md`'s Do-not-touch clause
   forbids this feature changing any command id. The `enforced` flip may not be
   reachable without either a DECISION narrowing the synonym scan's fields or a
   ruling that `dev.agent-loop` is out of scope for that check specifically.

## Risks

- The Worker→Builder rename does not change any gate's pass/fail on its own:
  DECISION F259 D3 scopes the vocabulary test's enforced-mode scan away from
  `Worker:` entirely (comment at `tests/docs/test_vocabulary.py:44-50`), so this
  slice is verified by its own targeted tests and mutation red-proof, not by
  that suite.
```

### DECISION1 — append to `.agent/decisions.md`, after its current last line,
verbatim (with today's date):

```

## DECISION F281 D1 (2026-09-17, F281 round 1) — the `Worker:` → role-label rename touches three production sites, not the twelve a bare grep finds

CONTEXT. DECISION F259 D3 named the role-label rename as the thing that "belongs
to F261" (now F281, by DECISION amend0917-throughput D4's carry-forward) and
explicitly excluded `Worker:` from the vocabulary test's own enforced-mode scan,
so no gate depends on this rename. A repo-wide search for the literal `Worker:`
finds twelve production sites, not one: `apps/cli/commands/do_cmd.py:618,621`;
`packages/orchestration/pingpong_evidence.py:230` (plus line 232's `Worker write
mode:`, the same reference without the bare colon); `apps/cli/commands/worker.py:
67,227`; `packages/orchestration/brain_viewer.py:559,975`;
`packages/orchestration/brain_detail.py:1175`;
`packages/orchestration/project_brain.py:630`; and
`apps/ui/src/components/panels/RightLivePanel.tsx:41`.

MEASURED. The `do_cmd.py`/`pingpong_evidence.py` sites are the pingpong run
report: each sits beside a sibling `Reviewer:` line built from
`reviewer_provider`, and each one's own value comes from `builder_provider` —
these are the retired BUILDER role label DECISION F259 D3 and D11a name. The
`worker.py`/`brain_viewer.py`/`brain_detail.py`/`project_brain.py`/
`RightLivePanel.tsx` sites all label a WORKER ADAPTER OR WORKER PROCESS record
(`match.display_name`, `status.worker_id`, `node.label`, `spec.display_name`,
`dashboard.workerStatus.lifecycle_state`) — the `worker` command group's own
subject and the cockpit/brain views of it, a live, still-correct vocabulary
sense per `docs/system/vocabulary.md`'s own Worker row (roles run ON a worker;
the worker itself keeps its name). Two test assertions pin the retired string on
the renamed side only: `tests/cli/test_cli_ux.py:592,665`, both against
`_cmd_run_show`'s text-mode output.

CHOSEN. Rename `Worker:` to `Builder:` (the pairing DECISION amend0905-vocab D1
gives the Builder/Reviewer roles, confirmed by the sibling `Reviewer:` line
already beside every one of these) at the five production line occurrences —
`do_cmd.py:618`, `do_cmd.py:621`, `pingpong_evidence.py:230`, and
`pingpong_evidence.py:232`'s `Worker write mode:` → `Builder write mode:` (the
same role reference; leaving it unrenamed beside a freshly renamed `Builder:`
line one line above would be the obvious residue a later reader trips on) —
plus the two test assertions that pin the old string. The seven
`worker`/`brain_*`/`project_brain.py`/`RightLivePanel.tsx` sites are UNTOUCHED:
none is the retired role label, and DECISION F259 D3's own vocabulary keeps
"worker" as the correct noun for the adapter/process entity.

ALTERNATIVES CONSIDERED. Renaming all twelve sites on the bare grep — rejected,
because it would rename the `worker` command group's own subject to `builder`,
which is wrong on its own terms and is exactly the over-reach a naive
grep-and-replace produces. Leaving `pingpong_evidence.py:232`'s "Worker write
mode" unrenamed because it lacks the literal substring `Worker:` — rejected as
the same class of miss in the other direction: leaving one role reference
un-renamed beside its own freshly renamed sibling.

CONSEQUENCE. `tests/cli/test_cli_ux.py`'s two assertions read `"Builder:" in
out`; the pingpong text report and its `summary.md` evidence file both print
`Builder:`/`Builder write mode:`; no other module's "Worker" reference changes.
HOW TO REVERSE: revert this round's C3 commit; delete this paragraph.
```

## Constraints

- Every edit above is applied byte-for-byte as given; no paraphrase.
- `.agent/plan.md` is REPLACED whole (not patched) with the PLAN1 text.
- The C1 commit's path set is exactly: `.agent/live_review.md`,
  `.agent/candidates.md`, `docs/roadmap/features/T2_F273.md`, `.agent/plan.md`,
  `.agent/decisions.md`. Nothing else.
- The C2 commit's path set is exactly: `docs/roadmap/STATUS.md` (the F281 line's
  `[ ]` → `[~]`, nothing else on that line changed), `.agent/context.md`
  (replaced whole, content below). Nothing else.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.
- Destructive/mutation verification runs only inside a disposable `git
  worktree` under `.remedy-wt/`, removed after, never inside the primary
  checkout.
- The branch is `feature/f281-cli-help-surface`, cut from `main` at
  `c617dd74df26b8e677161b265a88d5926f4d78ab` (current `main` tip). Confirm `git
  status --porcelain` is empty and `git branch --show-current` reads `main`
  before creating it.

### CONTEXT1 — replace the entire content of `.agent/context.md` with exactly:

```
# Context — F281 CLI help surface

## Active Branch
feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request 253
(F280's closure).

## Scope
F281 (Tier 2; depends on F280): T001 carries whole, verbatim, F280's own T002
(itself F261's old T004) — catalog descriptions, role labels, help wrapping, the
D11a catalog test, the D11d doctor check, the F259 enforced flip, the
D4/amend0911-feedback visible group order, and the README quickstart. Task
slicing per `docs/roadmap/features/T2_F281.md`'s Orchestrator brief: descriptions
and role labels first, then help wrap and `doctor core`, then the visible-order
test and the F259 enforced flip, the README quickstart last.

## Do not touch
The concept model (F259 owns the words), the job model (F260), STATUS
semantics, and behaviour behind a name: this feature rewrites what help says,
not what a command does. The catalog's set of groups and commands is F280's;
this feature changes NO COMMAND ID — see the open scope question in
`.agent/plan.md` about `dev.agent-loop`'s own command_id colliding with this
rule.

## Assumptions
- "Builder"/"Reviewer" is the role-label pairing DECISION amend0905-vocab D1
  names; every production "Worker:" print that means the BUILDER role (not the
  `worker` command group's own adapter/process noun) becomes "Builder:" — see
  DECISION F281 D1 for the full site-by-site boundary.
- Cleanliness before compatibility (DECISION D-A of
  `docs/roadmap/features/T2_F261.md`): no alias, no migration shim.

## Constraints
The bullets below are STANDING project constraints, carried forward from F280's
context file.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>`
  is the spelling every gate of this feature orders.
- `remedy` (the built CLI) may or may not be denied to this session's reviewer
  — try the binary once before falling back to `python3 -m apps.cli.main` or
  the disk-fallback route.
- The shell guard refuses shell loops, `$(...)` substitution and `$?` inside a
  compound command; such checks are written in Python.
- The editable install resolves `apps` and `packages` to the PRIMARY checkout,
  so a test run inside a worktree proves where its modules loaded from before
  its result is read.
- A fresh worktree has neither `apps/ui/node_modules` nor a built
  `apps/ui/dist`.
- Never call `run_job` or any runner from inside a checkout: a job run creates
  a `remedy/job-*` branch there.
- Per operator amendment amend0917-throughput (2026-09-17): the full suite runs
  exactly once per feature, in the closure sequence's integration-gate round;
  no round block may order it. A round's verification is targeted tests plus
  `tests/cli/test_golden_path.py`, `tests/docs/` when `docs/roadmap/**`
  changed, and `ruff check` on touched files. A round orders at most six
  gates; the plan slice, verdict booking, prose-slip lines and any DECISION
  land in ONE commit.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
```

## C3 — CODE (the role-label rename)

Edit `apps/cli/commands/do_cmd.py`. FROM (exact, two lines inside
`_print_text_report`):
```
        print(f"Worker: {b_label}")
        print(f"Reviewer: {r_label}")
    else:
        print(f"Worker: {data.get('builder_provider', 'unknown')}")
```
TO:
```
        print(f"Builder: {b_label}")
        print(f"Reviewer: {r_label}")
    else:
        print(f"Builder: {data.get('builder_provider', 'unknown')}")
```

Edit `packages/orchestration/pingpong_evidence.py`. FROM (exact, two lines
inside `_build_summary_md`):
```
    lines.append(f"- Worker: {run_data.get('builder_provider', 'unknown')} ({pe.get('builder_provider_kind', '')})")
    lines.append(f"- Reviewer: {run_data.get('reviewer_provider', 'unknown')} ({pe.get('reviewer_provider_kind', '')})")
    lines.append(f"- Worker write mode: {pe.get('builder_write_mode', 'none')}")
```
TO:
```
    lines.append(f"- Builder: {run_data.get('builder_provider', 'unknown')} ({pe.get('builder_provider_kind', '')})")
    lines.append(f"- Reviewer: {run_data.get('reviewer_provider', 'unknown')} ({pe.get('reviewer_provider_kind', '')})")
    lines.append(f"- Builder write mode: {pe.get('builder_write_mode', 'none')}")
```

Edit `tests/cli/test_cli_ux.py`. Both occurrences of the exact line
`        assert "Worker:" in out` (lines 592 and 665, inside
`test_text_report_shows_provider_evidence` and
`test_text_report_shows_token_accounting`) become
`        assert "Builder:" in out`.

## Gates (at most six; run and record real exit codes)

- G1 TARGETED: `python3 -m pytest tests/cli/test_cli_ux.py
  tests/orchestration/test_evidence_bundle.py
  tests/orchestration/test_job_evidence.py -q` — expect all pass, zero
  `Worker:`-related failures.
- G2 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect
  unchanged pass count from base.
- G3 SWEEP: `grep -rn '"Worker:' apps/ packages/ tests/ --include=*.py` reads
  exactly the seven untouched sites DECISION F281 D1 names (worker.py x2,
  brain_viewer.py x1 f-string + x1 html, brain_detail.py x1, project_brain.py
  x1) — zero remaining in `do_cmd.py`, `pingpong_evidence.py` or
  `test_cli_ux.py`.
- G4 RUFF: `python3 -m ruff check apps/cli/commands/do_cmd.py
  packages/orchestration/pingpong_evidence.py tests/cli/test_cli_ux.py` reads
  `All checks passed!`.
- G5 MUTATION RED-PROOF: in a disposable worktree under `.remedy-wt/`, revert
  `do_cmd.py:618`'s `Builder:` back to `Worker:` alone; re-run
  `tests/cli/test_cli_ux.py::TestTextReportTokenProof::
  test_text_report_shows_provider_evidence` and confirm it now REDS (the
  `assert "Builder:" in out` line fails) against a green control of the whole
  file; revert the mutation, confirm green again. Remove the worktree after.
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

## Done-when

C1, C2 and C3 are committed with the exact path sets named above; G1-G6 all
pass with real recorded output; the branch is pushed; `.agent/handoff.md` is
rewritten as C4 naming this round, its commits, its verification results, and
the next expected action (the remaining T001 slices named in PLAN1's "Next
Steps").
