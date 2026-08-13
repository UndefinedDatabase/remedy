── STEP R1/n — F115 Prompt breakdown & cost report · Round 1 ─────────
Goal:        Merge the F111 closure PR at the Open PR Gate, claim F115, reset
             the round state, clear the closure-candidates file by carrying its
             single entry forward as finding R-0320, and INVENTORY the current
             shape of the token ledger and the prompt-segment registry. No
             production code this round: the feature file demands the shape be
             found before it is built.
Bundle:      C0 Open PR Gate + branch · C1a save this block · C1b mirror it ·
             C2 claim and state reset (STATUS, live_review, candidates, plan,
             context) · C3 the inventory + handback
Change:      EXACTLY these paths:
               .agent/authored/f115-r1-1.md    (new, C1a)
               .agent/last_block.md            (rewrite, C1b)
               docs/roadmap/STATUS.md          (C2: one line)
               .agent/live_review.md           (C2: full replace)
               .agent/candidates.md            (C2: full replace)
               .agent/plan.md                  (C2: full replace)
               .agent/context.md               (C2: full replace)
               .agent/f115_inventory.md        (new, C3)
               .agent/handoff.md               (C3: rewrite)
             NO source file, NO test file, NO docs/system file this round.
Constraints:
  - TEXT-A … TEXT-E are AUTHORED text. Apply them byte for byte. Do not reword,
    rewrap or re-punctuate. If one looks wrong, apply it anyway and report it as
    a declared deviation. There are NO placeholder slots in this block:
    substitute nothing, anywhere.
  - Do NOT write a `Done:` or `Landed:` paragraph of your own. R1 registers a
    finding; it resolves none.
  - The inventory (C3) is YOUR OWN writing, not authored text. It reports what
    the code ACTUALLY does today. Every claim in it cites `path:line`. A claim
    you did not read in the source is a fabrication and a block condition.
  - C1 is SPLIT into two commits on purpose (authored file, then last_block):
    combined they exceed the AGENTS.md 500-insertion cap.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a PR this round. The branch is not reviewable-complete; the
    PR is created at closure per STATUS_closure_protocol.md.
Done when: every command has been RUN for real and its TRUE output recorded. A
           guessed, expected or remembered value is a finding.
  a. C0 gate proof: `gh pr view 194 --json state,mergedAt` shows state MERGED
     with a real mergedAt; `git branch --show-current` prints
     `feature/f115-prompt-cost-report`; `git log --oneline -n 2 main` shows the
     merge commit; `git merge-base --is-ancestor main HEAD` exits 0. Record the
     40-char SHA of the main tip the branch was cut from.
  b. `cmp .agent/authored/f115-r1-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  c. After C2, in `docs/roadmap/STATUS.md`:
     `grep -c '^- \[~\] F115 — Prompt breakdown & cost report$'` prints 1,
     `grep -c '^- \[~\]'` prints 1 (F115 is the ONLY claimed feature),
     `grep -c '^- \[x\] F[0-9][0-9][0-9] — '` still prints 44, and
     `grep -c '^- \[ \] F115'` prints 0. Touch no other STATUS line.
  d. After C2, in `.agent/live_review.md`: `grep -c '^- R-0320'` prints 1,
     `grep -c '^- R-0'` prints 1, `grep -c '^## Steps'` prints 1,
     `grep -c '^Done:'` prints 0, `grep -c '^Landed:'` prints 0.
  e. After C2: `grep -c '^- ' .agent/candidates.md` prints 0 — the file carries
     no candidate entry. Record the real number.
  f. After C2: `wc -l .agent/plan.md` prints a number BELOW 50 — record the real
     number. Do not pad or trim the authored text to hit a count.
  g. The `.agent` state contract suite, which reads plan.md, context.md and
     live_review.md and is the class that has broken twice on authored resets
     (R-0162): `python3 -m pytest tests/ui_server/test_dashboard_contract.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_test_runner.py -q`. Record tail and exit code.
  h. The change set includes docs/roadmap/**, so the docs gate is mandatory:
     `python3 -m pytest tests/docs/ -q`. Record tail and exit code.
  i. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q`. Record tail
     and exit code.
  j. The inventory answers all SEVEN questions below, each with `path:line`
     citations, and states plainly where the answer is "this does not exist
     yet". An honest "not present" is the most valuable line in the file; a
     plausible guess is a block condition.
  k. `git status --porcelain` empty; `git diff --name-only <main-tip>..HEAD`
     lists ONLY the nine ordered paths;
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0 after the final push.
Handback:  completion report + rewrite `.agent/handoff.md`. Item-status table
           (C0, C1a, C1b, C2, C3 — each exactly once), commit table with real
           SHAs and insertions, changed-files table, every result a-k as a REAL
           value. Repeat the Fortschritt line verbatim. Over 60 lines ⇒ carry a
           "Deviations, declared" line naming the count and the mandated content
           that caused it (AGENTS.md DECISION D15).
──────────────────────────────────────────────────────────────────────

PROCEDURE

C0 (no commit) Open PR Gate, per AGENTS.md. PR #194 is the F111 closure PR:
    exactly one open PR, from `feature/f111-diff-only-repair` into `main`, not a
    draft, MERGEABLE/CLEAN. It was created in an EARLIER session and its round
    was gated PASS by the reviewer before this block was written, so it merges
    now:
      gh pr merge 194 --merge --delete-branch
      git checkout main
      git pull --ff-only
      git checkout -b feature/f115-prompt-cost-report
    If the merge is refused for ANY reason, STOP and hand back with the raw
    error. Do not retry with different flags, do not rebase, do not force.

C1a `chore(f115): save the R1 step block verbatim` — copy the reviewer's
    scratchpad original `.remedy-wt/f115-r1-1.md` to
    `.agent/authored/f115-r1-1.md`. Copy the FILE; do not retype it.
C1b `chore(f115): mirror the R1 block into last_block` — copy that same file to
    `.agent/last_block.md`. Run gate (b).

C2 `chore(f115): claim F115 and reset the round state`
    ONE commit touching exactly these five paths:
      - STATUS: apply the TEXT-A pair. Touch no other STATUS line.
      - `.agent/live_review.md` ← TEXT-B in full.
      - `.agent/candidates.md`  ← TEXT-C in full.
      - `.agent/plan.md`        ← TEXT-D in full.
      - `.agent/context.md`     ← TEXT-E in full.
    Run gates (c), (d), (e), (f), (g), (h), (i).

C3 `docs(f115): inventory the ledger and segment registry shape`
    Write `.agent/f115_inventory.md`, then rewrite `.agent/handoff.md`. Read the
    source before writing a word of it. Start here and follow what you find —
    this list is a starting point, not a boundary:
      packages/orchestration/token_ledger.py
      packages/orchestration/token_actuals.py
      packages/orchestration/prompt_segments.py
      packages/orchestration/token_cost_policy.py
      apps/cli/commands/stats_ledger_cmd.py
      apps/cli/command_catalog.py
    The SEVEN questions, each answered with `path:line` citations:
      Q1 Where is a token-ledger row WRITTEN? Name the function, its call
         sites, and the exact field/column set a row carries today.
      Q2 What is the ledger's storage shape — sqlite table, jsonl, something
         else? Quote the schema or the record construction verbatim.
      Q3 What does the prompt-segment MANIFEST contain (names, ranks, hashes,
         anything else) and where is it persisted into call evidence?
      Q4 Is there ALREADY any link between a ledger row and its segment
         manifest — a job id, call id, evidence path, anything joinable? If the
         answer is no, say NO in those words. This is the load-bearing
         question of the round: T001's size depends entirely on it.
      Q5 What does `remedy stats` expose today — every subcommand, its flags,
         and its output modes. Is there an existing markdown/json renderer
         pair to follow as a pattern?
      Q6 Where do cost and BASIS labels come from (token_cost_policy.py and
         whatever it reads), and what does an UNPRICED call look like on disk?
      Q7 What fixture-ledger and golden-file patterns already exist in the
         suite that T002 should follow rather than invent? Name the files.
    Then, in one short closing section, state which of the three T-slices the
    evidence says is LARGER or SMALLER than the feature file assumes, and why.
    That paragraph is what the next block is planned from.

TEXT-A — one REWRITE pair for docs/roadmap/STATUS.md
  FROM (1 line, occurs exactly once):
- [ ] F115 — Prompt breakdown & cost report
  TO (1 line):
- [~] F115 — Prompt breakdown & cost report

TEXT-B — the complete new .agent/live_review.md

# Live Review — F115 Prompt breakdown & cost report

> Round-by-round review record for F115, reset at the feature claim. The F111
> record is preserved in git history at its closure commit 98a49b5c. Finding
> IDs continue monotonically across features and are never renumbered.

## Steps
R1 claim, state reset and shape inventory → T001 manifest-alongside-actuals
persistence with backfill tolerance → T002 aggregation queries, the pure
renderer and its goldens → T003 CLI, period comparison and json schema →
integration gate → closure.

## Findings

- R-0320 — Low — carried forward from the F111 closure-candidates file under
  the disk-vehicle rule (docs/roadmap/STATUS_closure_protocol.md,
  "Closure-candidate findings"). A stop reason no code can ever emit:
  `STOP_REASONS` in `packages/orchestration/builder_bridge.py` declares
  `stale_diff_context`, and a repo-wide grep over every `.py` file finds that
  string in exactly one place — the frozenset itself. Nothing raises it,
  nothing tests it, nothing reads it. It predates the F111 branch (it is
  present at the merge base 4e0b762e), so it was not an F111 defect and was
  deliberately not fixed there. It is not fixed in F115 either: AGENTS.md bars
  mixing an unrelated fix into a feature branch, and F115 opens the token
  ledger and the report renderer, not the builder bridge. The remedy — wire it
  to the condition it names, or delete it — is a one-commit change that
  belongs to whichever feature next has a legitimate reason to open
  `builder_bridge.py`. Recording it here keeps it findable after
  `.agent/candidates.md` is emptied, which is the whole point of the
  carry-forward rule. OPEN.

TEXT-C — the complete new .agent/candidates.md

# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

(empty — the single F111 candidate was registered as finding R-0320 in
`.agent/live_review.md` at F115 R1, 2026-08-13.)

TEXT-D — the complete new .agent/plan.md

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main after PR #194
(F111 closure) merged at the Open PR Gate. Last reviewed SHA: none yet,
R1 is the first round. Next free finding ID: R-0321. Open findings: 1
(R-0320, Low, carried forward from F111 — not an F115 defect).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R1 — claim F115, reset the round state, and inventory the CURRENT shape
of the token ledger and the prompt-segment registry before any code is
written. The feature file demands that inspection first: F115 is
aggregation and presentation only, so the join it needs must be found
in what exists, not invented.

## Next Steps
1. T001 — persist the segment manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
2. T002 — aggregation queries plus the pure renderer, with goldens over
   a fixture ledger covering mixed roles, mixed task classes, missing
   manifests and unpriced calls.
3. T003 — the CLI, the prior-period comparison and the json schema; an
   empty prior period reads "no comparison data", not zeros.
4. Integration gate, then closure per STATUS_closure_protocol.md.

## Risks
- The join may not exist yet. If the ledger writer stores no manifest
  reference at all, T001 grows and the R1 inventory must say so plainly.
- Report generation must touch nothing (read-only, state snapshot equal);
  an aggregation path that writes is an acceptance failure, not a nit.

Fortschritt: 5 % (R1 Inventar läuft · T001 · T002 · T003 offen) — Schätzung

TEXT-E — the complete new .agent/context.md

# Context — F115 Prompt breakdown & cost report

## Active Branch
feature/f115-prompt-cost-report, cut from main after PR #194 (the F111
closure) was merged at the Open PR Gate. F115 is claimed `[~]` under Rule A5
as the first `[ ]` line of docs/roadmap/STATUS.md (Package 1 Self-Use,
Tier 2).

## Scope
In: joining what already exists. The prompt-segment registry records a
manifest (segment names, ranks, hashes) into call evidence and the token
ledger stores per-call actuals; F115 persists the manifest alongside the
ledger row additively, aggregates over it, and renders `remedy stats report`
as markdown and json. No new capture and no new numbers — aggregation and
presentation only.

Out, per the feature file's Do-not-touch: pricing tables, calibration, UI
rendering and scheduled reporting. The report is on demand; this feature adds
no scheduler and no background job. Report generation is read-only: the state
snapshot before and after a run must be equal.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/ and apps/, and
  production code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- A round pushes after EVERY commit, not once at its last step (R-0289).
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/ also runs
  tests/docs/. The full suite runs only at the integration gate, with
  `-n auto`. Destructive and mutation checks run only inside a disposable git
  worktree, so resource safety stays intact and no background pytest process is
  ever left running.
- Every number in the report is traceable to a ledger row. A period with
  missing data says so (P6); interpolation is a defect, not a fallback.

## Steps
R1 claim, state reset and shape inventory → T001 manifest-alongside-actuals
persistence → T002 aggregation queries, pure renderer and goldens → T003 CLI,
period comparison and json schema → integration gate → closure.
