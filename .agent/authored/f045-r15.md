── STEP T003→gate — F045 ───────────────────────────────────────
Goal:        Register finding R-0358, then run the INTEGRATION GATE for F045
             exactly as docs/agents/integration_gate.md prescribes. This is the
             last gate before closure.

Bundle:      C0a save this block · C0b point last_block at it · C1 register
             R-0358 · C2 the integration gate and its evidence · C3 plan.md and
             the handoff.

Change:      Exactly these files, nothing beyond them:
             - `.agent/authored/f045-r15.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1)
             - `.agent/gate_f045_r15/` (NEW directory, C2 — evidence only)
             - `.agent/plan.md` and `.agent/handoff.md` (C3)
             NO production code. NO test files. If the gate reveals a defect
             that needs a code change, that fix is its OWN reviewer-gated round
             — report it and STOP, do not fix it here.

Insertion budget (finding R-0350): C0a/C0b are single `.agent/**` state files,
cap-EXEMPT by DECISION F104 D1. C1 adds 2 lines. C2 is gate EVIDENCE whose size
is whatever the suite produces — no number is asserted, and evidence files are
exempt from the reviewability argument the cap exists for, but keep each file
to real captured output and nothing else. C3 is two `.agent/**` files.

── C0a / C0b ──────────────────────────────────────────────────
Write `.agent/authored/f045-r15.md`; commit alone.
  Subject: `chore(f045): save the R15 block verbatim`
Copy it to `.agent/last_block.md`, byte-identical; commit alone.
  Subject: `chore(f045): point last_block at the R15 block`

── C1 — register R-0358 ───────────────────────────────────────
APPEND to the very END of `.agent/live_review.md`: a blank line, then the
FINDING-358 text. ONE physical line — do not re-wrap, no trailing whitespace.
Take the bytes from your saved copy.

REVIEWER-AUTHORED. Do not edit or shorten it, and never write a `Done:`
paragraph of your own (planner_reviewer_prompt.md §4.4). If you think it is
wrong, STOP and report it.

>>> FINDING-358 >>>
- R-0358 — Low — a block ordered an attribute the type does not have. The R14 block's C2 step ordered the report read as `report_path(job.job_id)`, but `run_loop` returns a `packages.core.models.Job`, whose identifier field is `id` — the `id: UUID = Field(default_factory=uuid4)` line in the `Job` model — and `job_id` is not a field of that model at all; it belongs to `pingpong_job.JobPlan`, a different type the block never mentioned. `report_path` itself takes a plain string parameter, so the correct call is `report_path(str(job.id))`, which is what the R14 worker wrote after DECLARING the deviation rather than silently substituting it — the behaviour that keeps a block honest, and the fourth round of this feature in which a worker corrected the reviewer's own text. This is the R-0349/R-0353 family a third time: a reviewer naming a symbol whose shape it had not checked against the type in front of it. The existing counter-measures do not reach it — R-0349's covers a SYMBOL grepped to its own definition, R-0353's covers a `file:line` re-measured after this branch's edits, and pre-emission checklist item 9 covers pointers that do not resolve; none covers an ATTRIBUTE asserted on a value whose type the block itself named. Nothing landed wrong. Counter-measure: when a block names an attribute access on a value whose type it also names, that attribute is grepped on THAT type before emission and never inferred from the parameter name of the function the value is passed to — here `report_path`'s parameter is itself called `job_id`, which is precisely what made `job.job_id` look correct. OPEN.
<<< FINDING-358 <<<

Commit C1 ALONE, before the gate. Subject: `docs(f045): register R-0358 on the job id attribute`

── C2 — the integration gate ──────────────────────────────────
Read docs/agents/integration_gate.md and follow it EXACTLY. It is the canonical
procedure and this block deliberately does not restate it. The points below are
scope, not a replacement for that file.

  - Evidence directory: `.agent/gate_f045_r15/`. Evidence files use `.txt`
    names, NEVER `.log` (the review-zip guard rejects `\.log$`, R-0169).
  - Run logs are written OUTSIDE the repo worktree while a suite runs, and
    copied into the evidence dir only AFTER the run exits (R-0176 — a log
    growing inside the repo changes the worktree digest mid-run and fails the
    manifest-identity ids as false positives). `/tmp` writes are DENIED in this
    environment; use a scratch directory under `.remedy-wt/`, which is
    gitignored, and copy from there.
  - Merge base: compute it, do not assume it — `git merge-base main HEAD`.
    Record the SHA you got.
  - Base worktree goes on a THROWAWAY BRANCH (`git worktree add -b tmp/base-gate
    <path> <merge-base>`), never detached: the self-dogfood branch guard refuses
    a detached HEAD by design (DECISION D3). Remove and prune it, delete the tmp
    branch, and prove it with `git worktree list`.
  - Environment parity for the base run is a REAL obligation, not a footnote —
    follow the integration_gate.md paragraph on `apps/ui/node_modules` and
    `apps/ui/dist` (COPY, never symlink), verify the neutralization by hashing
    `apps/ui/dist` before and after the base run, and report both hashes. If
    you cannot restore parity, then attribute EVERY `comm -23` id to the
    environment class by direct per-id evidence. An unattributed `comm -23` id
    counts as a genuine base failure and BLOCKS the gate verdict.
  - Attribution for EVERY branch-only id per step 4 of that file: serial re-run
    of the exact node id, then classify (serial-pass ⇒ xdist-flake class,
    record not blocker; serial-fail ⇒ reproduce at the merge base before
    blaming the feature; reproducible branch-only failure coupled to F045 code
    ⇒ BLOCKER, STOP and hand back).
  - Record for BOTH runs: raw tail, the full FAILED list, exit code, wall time.
  - FLAKE DEBT: if more than 10 branch-only failures land in the pre-existing
    flake class, say so explicitly in the handback — it changes the reviewer's
    brief (planner_reviewer_prompt.md §2).

You do NOT issue the gate verdict. Only the reviewer does. Report the evidence.

Commit C2 alone. Subject: `chore(f045): record the integration gate evidence`

── C3 — plan and handoff ──────────────────────────────────────
Rewrite `.agent/plan.md`: under 50 lines; keep `## Goal` and `## Next Steps`;
state the open findings RECOMPUTED by gate (b) below (gate (b) wins over any
number you expected — write what the disk says and DECLARE any deviation);
state the integration gate's RESULT honestly (green, or the branch-only ids and
their classification); name the next step as closure per
docs/roadmap/STATUS_closure_protocol.md if and only if the gate is clean, and
otherwise name the repair the gate demands. End with a Fortschritt line that
reflects what actually happened — `~85 %` if the gate is clean, an honest lower
number if it is not.

Then rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature
and round, branch, base SHA (6451da42), per-commit table, the gate table with
REAL exit codes and REAL output, the item-status table, the open-findings
count, next expected action. Last line repeats the plan's Fortschritt verbatim.
Cap 60 lines; if MANDATED content genuinely does not fit, exceed it with a
"Deviations, declared" line naming the actual count and the mandated content
that caused it. Never drop a section.

IMPORTANT — this is the LAST round of the session. The handoff's "next expected
action" MUST name, in this order: (1) Phase 1 rule 1, read `.agent/STOP` from
disk, BEFORE anything else (finding R-0347 — a sentinel appearing mid-session
is invisible until something trips on it); (2) Phase 1 rule 2, the Open PR
Gate; (3) whatever F045 needs next.

Commit C3 alone. Subject: `docs(f045): close the session with the R15 handoff`

── Constraints ────────────────────────────────────────────────
- AGENTS.md governs. Self-review loop before EVERY commit. Push after each.
- Never work on main. Never force-push. Never merge. Never create a PR.
- NO production code, NO test files. A needed fix is a STOP and a report.
- The gate's base worktree and any scratch live under `.remedy-wt/`; all
  worktrees removed and pruned, tmp branch deleted, before handback.
- Authored text (FINDING-358) applied byte for byte from your saved copy. No
  trailing whitespace anywhere.
- Never write a `Done:` paragraph; use `Landed: R-XXXX — <one line>`.
- If a gate goes red in a way the procedure does not resolve, or you hit a
  contradiction, or something is ambiguous: STOP, commit what is validly
  complete, and report in full. Do not guess, do not widen scope. An honest
  halt is a success.

── Done when ──────────────────────────────────────────────────
Every gate run, REAL exit codes and REAL output. Re-run (f)/(g) AFTER the final
commit.

  (a) cmp .agent/authored/f045-r15.md .agent/last_block.md → exit 0.
  (b) Open set, recomputed from the record after C1:
      python3 - <<'EOF'
      import re
      lines=open('.agent/live_review.md').read().splitlines()
      reg=[m.group(1) for l in lines if (m:=re.match(r'^- (R-\d+) — ',l))]
      done=[m.group(1) for l in lines if (m:=re.match(r'^Done: (R-\d+) — ',l))]
      print("OPEN",sorted(set(reg)-set(done)))
      EOF
      → must print exactly: OPEN ['R-0350', 'R-0354', 'R-0358']
  (c) FINDING-358 appears EXACTLY ONCE among C1's ADDED lines; C1's numstat for
      `.agent/live_review.md` is 2 insertions, 0 deletions.
  (d) The integration gate's own records, per integration_gate.md: merge-base
      SHA · branch run exit code, wall time, raw tail, FAILED list ·
      base run the same · `comm -13` (branch-only) and `comm -23` (fixed at
      branch) · per-id attribution for every branch-only id · the
      `apps/ui/dist` hash before and after the base run.
  (e) python3 -m pytest tests/orchestration/test_loop_run.py tests/cli/test_loop_cmd.py tests/orchestration/test_loop_spec.py tests/orchestration/test_run_report.py -q
      → the F045 surface. Real counts.
  (f) git diff --name-only 6451da42..HEAD → the paths in Change and nothing
      else. git status --porcelain → EMPTY. git worktree list → exactly ONE
      line. `git branch --list 'tmp/*'` → empty.
  (g) No trailing whitespace on any non-evidence file this round writes. If
      `grep -rn ' $'` is denied here, run an equivalent Python scan and say
      which command you actually ran.
  (h) gh pr list --state open --json number,headRefName → [].

Handback:    completion report plus the rewritten `.agent/handoff.md`. For each
             gate: command, exit code, real output. "Green" as a word is not a
             result, and the gate verdict is the reviewer's, not yours.
──────────────────────────────────────────────────────────────
