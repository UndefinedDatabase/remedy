── STEP T003 (end-to-end fixture loop) — F045 ──────────────────
Goal:        Close R-0357, then prove the whole path once: a fixture loop
             materializes a job, that job runs through the STANDARD cycle loop
             with a fake provider, and the report on disk names the loop. This
             is T003's last item.

Bundle:      C0a save this block · C0b point last_block at it · C1 the authored
             `Done:` line for R-0357 · C2 the end-to-end fixture test ·
             C3 plan.md and the handoff.

Change:      Exactly these files, nothing beyond them:
             - `.agent/authored/f045-r14.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1)
             - `tests/orchestration/test_loop_run.py` (C2)
             - `.agent/plan.md` and `.agent/handoff.md` (C3)
             NO production code this round. If the test cannot pass without a
             production change, STOP and report exactly what is missing and
             why — do NOT make the change. That is the most valuable thing you
             can return, and it is a successful round.

Insertion budget, per commit, measured or reasoned (finding R-0350):
             C0a and C0b are each the verbatim rewrite of a SINGLE `.agent/**`
             state file, cap-EXEMPT by DECISION F104 D1.
             C1 adds 2 lines — one blank plus one authored line.
             C2's size follows the harness the test needs; no number is
             asserted here because the fixture's shape is what this round is
             discovering. If C2 alone exceeds 500 insertions, stop and split.
             C3 is two `.agent/**` files, far under the cap.

── C0a / C0b ──────────────────────────────────────────────────
Write `.agent/authored/f045-r14.md`; commit alone.
  Subject: `chore(f045): save the R14 block verbatim`
Copy it to `.agent/last_block.md` so the two are byte-identical; commit alone.
  Subject: `chore(f045): point last_block at the R14 block`

── C1 — close R-0357 ──────────────────────────────────────────
APPEND to the very END of `.agent/live_review.md`: a blank line, then the
DONE-357 text. It is ONE physical line — do not re-wrap it, do not insert
newlines, no trailing whitespace. Take the bytes from your saved copy.

REVIEWER-AUTHORED text. Do not edit it, do not shorten it, and do not write any
`Done:` paragraph of your own (planner_reviewer_prompt.md §4.4). If you believe
it is wrong, STOP and report it instead of correcting it.

>>> DONE-357 >>>
Done: R-0357 — RESOLVED at the R14 gate. Verified against the disk, not the report: `.agent/f045_e2e_inventory.md` Q1 now names the module in full — `_apply_terminal` "is NOT in `job_runner.py` ... but back in `packages/orchestration/long_run_executor.py`" — and carries the command that places it together with both its definition line and its single call site, so a reader no longer has to resolve a back-reference across an intervening paragraph that named a different module. `grep -c "in the same module" .agent/f045_e2e_inventory.md` returns 0, so the ambiguous phrase is GONE rather than merely qualified, and the self-contradiction the finding named went with it: the repaired text states outright that `job_runner.py` "really does contain no executor", which is consistent with the terminal path living elsewhere instead of contradicting it one sentence later. The reviewer re-grepped the citation itself rather than trusting the repair — `grep -rn "_apply_terminal" --include=*.py packages/ apps/` puts the definition at `packages/orchestration/long_run_executor.py:911` and its single call site at line 1578, exactly what the repaired paragraph claims. The counter-measure is worth keeping in the reader's eye rather than only in this record: a back-reference may not carry a citation across a paragraph that named a different module.
<<< DONE-357 <<<

Commit C1 ALONE. Subject: `docs(f045): close R-0357 at the R14 gate`

── C2 — the end-to-end fixture loop ───────────────────────────
Add to `tests/orchestration/test_loop_run.py`. Add tests only; change no
existing test in that file.

READ FIRST, before writing anything — these are the two harnesses you are
joining, and both were located by grep in this round's own commands:
  - `tests/orchestration/test_long_run_executor.py` — the cycle-loop harness.
    `isolate_data_root` (line 64) sets `REMEDY_DATA_DIR`; `make_job` (line 80)
    builds a PLANNED job; `class FakeProvider` (line 92) is the fake provider;
    `completing_step` (line 121) is the `task_step` seam; and
    `TestTerminalStatusMatrix::test_all_green` (line 172) is the existing test
    that drives a job all the way to a terminal state. Model the mechanics on
    it. Import or re-create its helpers as fits the repo's style — do not edit
    that file.
  - `run_cycles` in `packages/orchestration/long_run_executor.py` (line 1284),
    signature `run_cycles(job, limits, provider_call, *, task_step=None, …)`.

THE TEST — one end-to-end path, in this order:
  1. Build a loop from a TMP config the way the existing tests in this file
     already do (a `[[loop]]` table with a job action). Do not add a
     repo-level config file; nothing may depend on one existing.
  2. Call `run_loop` to materialize it. Assert the job carries
     `metadata[LOOP_REF_METADATA_KEY] == <the loop's name>`.
  3. Drive THAT SAME job through `run_cycles` with the fake provider and the
     `task_step` seam, to a terminal state.
  4. Read the report OFF DISK via `report_path(job.job_id)` from
     `packages.orchestration.run_report`. Assert the file exists, and that its
     text contains exactly one line equal to `- Loop: <the loop's name>`.
  5. Assert the PERSISTED job — loaded back through `storage.load_job`, never
     read out of an in-memory reference or a save callable — still carries the
     loop ref. A property decided by the fixture instead of by the code is the
     R-0344/R-0351 defect this feature has already paid for twice.

TERMINAL STATUS — order of the probe, not the colour (pre-emission checklist
item 5). I have NOT run this fixture and will not assert a value I did not
compute. Drive the job to a terminal state, then REPORT in your handback which
terminal status it actually reached and how many cycles it took. Pin in the
test only the value you OBSERVED, and say in the handback that you observed it
rather than that it was ordered. If it does not reach a terminal state at all,
that is a real result: report it and STOP rather than tuning the fixture until
a number appears.

ISOLATION — load-bearing, and this feature's most expensive recurring defect
(findings R-0351 and R-0352). `run_loop` writes to the REAL job store unless it
is isolated. Isolate through `REMEDY_DATA_DIR` (the `isolate_data_root` shape)
and/or an explicit `root`, and prove the isolation held: gate (f) below checks
the operator's real job store afterwards.

Do NOT assert any line count, any numstat, or any total character count of a
report — assert the DATA. A serialized artifact's arithmetic is not a semantic
gate.

Commit C2 alone. Subject: `test(f045): drive a fixture loop through the cycle loop end to end`

── C3 — plan and handoff ──────────────────────────────────────
Rewrite `.agent/plan.md`. It MUST: stay under 50 lines; keep `## Goal` and
`## Next Steps` headings; state the open findings RECOMPUTED by the gate (b)
command (if gate (b) disagrees with any number you expected, gate (b) wins —
write what the disk says and DECLARE the deviation); name the next steps as the
integration gate (docs/agents/integration_gate.md) then closure per
docs/roadmap/STATUS_closure_protocol.md; and say plainly whether T003 is now
complete based on what gate (e) actually showed. End with:
`Fortschritt: ~80 % (T001 ✅ · T002 ✅ · T003 ✅) — Schätzung`
— but ONLY if the end-to-end test actually passes. If it does not, write the
honest lower number and the honest T003 marker instead, and say why.

Then rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature
and round, branch, base SHA (0b2efeee), per-commit table, the gate table below
with REAL exit codes and REAL output, the item-status table (AGENTS.md), the
open-findings count, next expected action. Its last line repeats the plan's
Fortschritt line verbatim. Cap 60 lines; if MANDATED content genuinely does not
fit, exceed it and carry a "Deviations, declared" line naming the actual line
count and the specific mandated content that caused it. Never drop a section.

Commit C3 alone. Subject: `docs(f045): hand back R14 with the end-to-end loop`

── Constraints ────────────────────────────────────────────────
- AGENTS.md governs. Self-review loop before EVERY commit. Push after each.
- Never work on main. Never force-push. Never merge. Never create a PR.
- NO production code this round. A needed production change is a STOP and a
  report, not an edit.
- Any mutation or red-proof runs ONLY inside a disposable `git worktree` under
  `.remedy-wt/`, removed and pruned before handback. /tmp writes are denied here.
- Authored texts (DONE-357) applied byte for byte from your saved copy. No
  trailing whitespace anywhere.
- Never write a `Done:` paragraph of your own; use `Landed: R-XXXX — <one line>`.
- If a gate goes red, or you hit a contradiction, or something is ambiguous:
  STOP, commit nothing further, report it in full. Do not guess, do not widen
  scope to route around it. An honest halt is a success.

── Done when ──────────────────────────────────────────────────
Run every gate; record REAL exit codes and REAL output. Re-run (g), (h), (i)
AFTER the final commit.

  (a) cmp .agent/authored/f045-r14.md .agent/last_block.md   → exit 0.
  (b) The open set, recomputed from the record after C1:
      python3 - <<'EOF'
      import re
      lines=open('.agent/live_review.md').read().splitlines()
      reg=[m.group(1) for l in lines if (m:=re.match(r'^- (R-\d+) — ',l))]
      done=[m.group(1) for l in lines if (m:=re.match(r'^Done: (R-\d+) — ',l))]
      print("OPEN",sorted(set(reg)-set(done)))
      EOF
      → must print exactly: OPEN ['R-0350', 'R-0354']
  (c) DONE-357 appears EXACTLY ONCE among the lines C1's diff ADDS, and C1's
      numstat for `.agent/live_review.md` is 2 insertions, 0 deletions.
  (d) python3 -m pytest tests/orchestration/test_loop_run.py -q  → real counts,
      and name the new test(s) with `-k` and show that output too.
  (e) The end-to-end assertions, quoted from the real run: the terminal status
      observed, the report path, and the exact `- Loop: …` line found in it.
      If you cannot quote the real line from a real file, the item is NOT done.
  (f) ISOLATION PROOF. After the suite runs, check the OPERATOR'S REAL job
      store — the one `jobs_dir()` resolves to with no `REMEDY_DATA_DIR` set —
      and confirm it gained no job carrying a `loop_ref` from this round. Show
      the command and its real output. This is the R-0352 counter-measure.
  (g) python3 -m pytest tests/cli/test_loop_cmd.py tests/orchestration/test_loop_spec.py tests/orchestration/test_run_report.py tests/orchestration/test_long_run_executor.py -q
      → the neighbours this test joins. Real counts.
  (h) python3 -m pytest tests/cli/test_golden_path.py -q   (the canary). Real counts.
  (i) git diff --name-only 0b2efeee..HEAD → exactly the six paths in Change.
      git status --porcelain → EMPTY.  git worktree list → exactly ONE line.
  (j) ruff check on every Python file this round touches → real output.
  (k) No trailing whitespace on any line of any file this round writes. If your
      environment denies `grep -rn ' $'`, run an equivalent Python scan and say
      which command you actually ran.
  (l) gh pr list --state open --json number,headRefName → [].

Handback:    completion report plus the rewritten `.agent/handoff.md`. For each
             gate: the command, the exit code, the real output. "Green" as a
             word is not a result.
──────────────────────────────────────────────────────────────
