── STEP T003 (repair + report provenance) — F045 ───────────────
Goal:        Persist finding R-0357, repair the citation that caused it, then
             make `loop_ref` visible in the run report — which lives inside the
             job's evidence area, so one change covers both halves of the
             feature file's Acceptance line.

Bundle:      C0a save this block · C0b point last_block at it · C1 persist
             R-0357 · C2 repair the inventory citation · C3 the report change ·
             C4 its tests · C5 plan.md and the handoff.

Change:      Exactly these files, nothing beyond them:
             - `.agent/authored/f045-r13.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1)
             - `.agent/f045_e2e_inventory.md` (C2)
             - `packages/orchestration/run_report.py` (C3)
             - `tests/orchestration/test_run_report.py` (C4)
             - `.agent/plan.md` and `.agent/handoff.md` (C5)
             Do NOT edit `packages/orchestration/loop_run.py`, `loop_spec.py`,
             `loop_cmd.py`, or any golden text inside
             `tests/orchestration/test_run_report.py`. If you believe a golden
             must change, STOP and report it — that is a reviewer decision.

Insertion budget, per commit, measured or reasoned (finding R-0350):
             C0a and C0b are each the verbatim rewrite of a SINGLE `.agent/**`
             state file, cap-EXEMPT by DECISION F104 D1.
             C1 adds 2 lines — one blank plus one authored line — measured from
             the authored text below.
             C2 is a FROM→TO rewrite of one paragraph; its net change is a
             handful of lines, so no cap question arises.
             C3 is three small edits in one module; no number is asserted here
             because the exact line count depends on how the module's existing
             formatting absorbs them.
             C4's size follows the tests it needs; if it alone exceeds 500
             insertions, split it and declare the split.
             C5 is two `.agent/**` files, far under the cap.

── C0a ────────────────────────────────────────────────────────
Write `.agent/authored/f045-r13.md`. Commit alone.
Subject: `chore(f045): save the R13 block verbatim`

── C0b ────────────────────────────────────────────────────────
Copy it to `.agent/last_block.md` so the two are byte-identical. Commit alone.
Subject: `chore(f045): point last_block at the R13 block`

── C1 — persist the finding FIRST ─────────────────────────────
APPEND to the very END of `.agent/live_review.md`: a blank line, then the
FINDING-357 text. It is ONE physical line — do not re-wrap it, do not insert
newlines, no trailing whitespace. Take the bytes from your saved copy.

This is REVIEWER-AUTHORED text. Do not edit it, shorten it, or write any
`Done:` paragraph of your own (planner_reviewer_prompt.md §4.4). If you think
it is wrong, STOP and report it rather than correcting it.

>>> FINDING-357 >>>
- R-0357 — Low — a survey's citation pointed at a module that cannot contain it, and contradicted its own neighbouring sentence. `.agent/f045_e2e_inventory.md` Q1 states that "Terminal transitions all funnel through `_apply_terminal` in the same module (line 911)". The sentence immediately before it greps `packages/orchestration/job_runner.py` and concludes "that module contains no executor at all", so "the same module" resolves to `job_runner.py` — a 94-line file whose only top-level definition is `plan_job`, which therefore has no line 911 and no `_apply_terminal`. `grep -rn "_apply_terminal" --include=*.py packages/ apps/` puts the symbol at `packages/orchestration/long_run_executor.py:911` with its one call site at line 1578, which is the module the section opened with three paragraphs earlier and the line number the citation already gives — so only the module attribution is wrong, and the quoted docstring "the ONE place a final run report is written (F053 T002)" is verbatim correct at that real location. Two rule families meet here. The citation does not resolve where it points, which is R-0349 and R-0353 and the whole reason for pre-emission checklist item 9 — closed on disk in the very round that then produced this. And the clause contradicts its own neighbour, which is the R-0331/R-0334 family: "contains no executor at all" and "terminal transitions funnel through the same module" cannot both be true of one 94-line file. Nothing landed wrong in code and no production file was touched, but `.agent/f045_e2e_inventory.md` exists precisely so the next round can trust it WITHOUT re-derivation, and a reader following it would grep a 94-line file, find nothing, and halt — the cost R-0349 and R-0353 each already charged this feature once. Counter-measure: a back-reference such as "the same module", "that file" or a bare "it" may not carry a `file:line` citation across an intervening paragraph that names a DIFFERENT module; whenever the previous sentence named another module, the intended module is named again in full. OPEN.
<<< FINDING-357 <<<

Commit C1 ALONE, before any fix. Subject: `docs(f045): register R-0357 on the inventory citation`

── C2 — repair the citation ───────────────────────────────────
In `.agent/f045_e2e_inventory.md`, replace the FROM paragraph with the TO
paragraph. This pair is a REWRITE (the TO does not contain the FROM), so the
proof is FROM 0x and TO 1x in the file after the edit.

>>> FROM-C2 >>>
Terminal transitions all funnel through `_apply_terminal` in the same module
(line 911), whose docstring says it is "the ONE place a final run report is
written (F053 T002)". It sets `job.metadata["cycle_terminal_status"]` and then
calls `write_final_report(job)`.
<<< FROM-C2 <<<

>>> TO-C2 >>>
Terminal transitions all funnel through `_apply_terminal`, which is NOT in
`job_runner.py` — that module really does contain no executor — but back in
`packages/orchestration/long_run_executor.py`. The command that places it:
`grep -rn "_apply_terminal" --include=*.py packages/ apps/` → its definition at
line 911 and its single call site at line 1578. Its docstring says it is "the
ONE place a final run report is written (F053 T002)". It sets
`job.metadata["cycle_terminal_status"]` and then calls `write_final_report(job)`.
<<< TO-C2 <<<

Commit C2 alone. Subject: `docs(f045): point the terminal citation at its real module`

── C3 — the report change ─────────────────────────────────────
`packages/orchestration/run_report.py` only. Three edits, in the exact shape
`stop_reason` already has. Read the whole module first (AGENTS.md file-editing
safety rules) and re-read it after.

  1. `ReportSources` (the frozen dataclass whose docstring says "Every field is
     optional and every absent field renders ``not recorded``") gains one field:
         loop_ref: str = ""
     Place it beside the other provenance fields, after `mission`. Default ""
     so an absent value renders nothing at all — see edit 3.
  2. `collect_report_sources(job)` already does
     `metadata = getattr(job, "metadata", None) or {}` and reads
     `cycle_terminal_status` and `cycle_stop_reason` by explicit name. Read the
     loop key beside them and pass it into the `ReportSources(...)` it builds.
     Do NOT retype the string "loop_ref": import the key so the writer and the
     reader cannot drift —
         from packages.orchestration.loop_run import LOOP_REF_METADATA_KEY
     as a LOCAL import inside the function, which is the style `report_path`
     already uses for `job_evidence_dir`. If that import turns out to be
     circular at runtime, STOP and report it; do not fall back to a literal.
  3. `_header_lines` emits ONE new line, conditional on the value being
     non-empty, immediately AFTER the `- Mission: …` line:
         if sources.loop_ref:
             lines.append(f"- Loop: {sources.loop_ref}")
     Conditional is load-bearing: the three goldens in
     `tests/orchestration/test_run_report.py` are full expected report texts for
     jobs that carry no loop, and they must stay byte-identical. That is a
     PROOF obligation in Done-when (e), not an assumption.

Add a one-line WHY comment directly above the new field and above the new
emit, per AGENTS.md "Code Discoverability Conventions".

Commit C3 alone. Subject: `feat(f045): carry the loop reference into the run report`

── C4 — the tests ─────────────────────────────────────────────
`tests/orchestration/test_run_report.py` only. Add tests; change no golden and
no existing test. Name them after what they pin. At minimum:

  1. A job whose `metadata` carries the loop key renders exactly one line
     `- Loop: <name>` in the report, and that line sits directly after the
     `- Mission: …` line. Assert on the RENDERED text, and drive it through the
     same public entry point the existing tests use.
  2. A job with NO loop key renders NO line beginning `- Loop:` anywhere in the
     report. This is the negative pin that keeps the goldens safe, so it must
     scan the whole rendered text, not a slice of it.
  3. The reader takes the key from `loop_run.LOOP_REF_METADATA_KEY` rather than
     the literal, so a rename of the constant cannot silently unhook the
     report from the writer.

Do NOT assert any line count, any numstat, or any total character count of a
report — assert the DATA (line present/absent, its text, its position relative
to the Mission line). A serialized golden's arithmetic is not a semantic gate.

Commit C4 alone. Subject: `test(f045): pin the loop line in the run report`

── C5 — plan and handoff ──────────────────────────────────────
Rewrite `.agent/plan.md`. It is YOURS to write this round, but it MUST:
  - stay under 50 lines (AGENTS.md), keep a `## Goal` and a `## Next Steps`
    heading (planner_reviewer_prompt.md §4.11);
  - state the open findings as exactly THREE — R-0350, R-0354 and R-0357 —
    RECOMPUTED from `.agent/live_review.md` by the gate (b) command, never
    carried forward from this block. If gate (b) disagrees with that list,
    gate (b) wins: write what the disk says and DECLARE the deviation.
  - name the next step as the end-to-end fixture loop driving `run_cycles`,
    then the integration gate, then closure;
  - end with the line: `Fortschritt: ~72 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung`

Then rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature
and round, branch, base SHA (785373ac), per-commit table, the gate table below
with REAL exit codes and REAL output, the item-status table (AGENTS.md), the
open-findings count, next expected action. Its last line repeats the plan's
Fortschritt line verbatim. Cap 60 lines; if MANDATED content genuinely does not
fit, exceed it and carry a "Deviations, declared" line naming the actual line
count and the specific mandated content that caused it. Never drop a section.

Commit C5 alone. Subject: `docs(f045): hand back R13 with the report provenance`

── Constraints ────────────────────────────────────────────────
- AGENTS.md governs. Self-review loop before EVERY commit. Push after each.
- Never work on main. Never force-push. Never merge. Never create a PR.
- Any mutation or red-proof runs ONLY inside a disposable `git worktree` under
  `.remedy-wt/`, never in the primary checkout, and is removed and pruned
  before you hand back. Writes to /tmp are denied in this environment.
- Authored texts (FINDING-357, FROM-C2, TO-C2) are applied byte for byte from
  your saved `.agent/authored/f045-r13.md`. No trailing whitespace anywhere.
- Never write a `Done:` paragraph. If a fix of yours lands that needs
  recording, write `Landed: R-XXXX — <one line>` instead.
- If a gate goes red, or you hit a contradiction, or something here is
  ambiguous: STOP, commit nothing further, and report it in full. Do not guess
  and do not widen scope to route around it. An honest halt is a success.

── Done when ──────────────────────────────────────────────────
Run every gate and record its REAL exit code and REAL output. Re-run (h), (i)
and (j) AFTER the final commit.

  (a) cmp .agent/authored/f045-r13.md .agent/last_block.md   → exit 0.
  (b) The open set, recomputed from the record after C1:
      python3 - <<'EOF'
      import re
      lines=open('.agent/live_review.md').read().splitlines()
      reg=[m.group(1) for l in lines if (m:=re.match(r'^- (R-\d+) — ',l))]
      done=[m.group(1) for l in lines if (m:=re.match(r'^Done: (R-\d+) — ',l))]
      print("OPEN",sorted(set(reg)-set(done)))
      EOF
      → must print exactly: OPEN ['R-0350', 'R-0354', 'R-0357']
  (c) FINDING-357 appears EXACTLY ONCE among the lines C1's diff ADDS, and C1's
      numstat for `.agent/live_review.md` is 2 insertions, 0 deletions.
  (d) The C2 pair, after the edit: FROM-C2 appears 0x in
      `.agent/f045_e2e_inventory.md` and TO-C2 appears exactly 1x. Also
      `grep -c "in the same module" .agent/f045_e2e_inventory.md` → 0.
  (e) THE GOLDENS ARE BYTE-IDENTICAL. Run
      `python3 -m pytest tests/orchestration/test_run_report.py -q` and report
      the real counts, AND confirm the three golden tests
      `test_green_terminal_matches_golden`,
      `test_blocked_with_decision_matches_golden` and
      `test_budget_terminal_matches_golden` each PASS by name
      (`-k` them and show the output). `git diff` on
      `tests/orchestration/test_run_report.py` must show NO deletion inside any
      golden text — report the deleted-line count for that file.
  (f) RED-PROOF, in a disposable worktree only. At HEAD, in a worktree under
      `.remedy-wt/`, first print `import packages.orchestration.run_report as m;
      print(m.__file__)` and confirm the path is INSIDE that worktree — a probe
      that imports the primary checkout proves nothing (finding R-0337). Then
      DELETE the two new emit lines in `_header_lines` and re-run the C4 tests.
      Report which tests fail and on WHICH assertion. Restore nothing — remove
      and prune the worktree instead.
  (g) python3 -m pytest tests/cli/test_loop_cmd.py tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
      → the F045 suite. Real counts.
  (h) python3 -m pytest tests/cli/test_golden_path.py -q   (the canary). Real counts.
  (i) git diff --name-only 785373ac..HEAD → exactly the eight paths in Change.
  (j) git status --porcelain → EMPTY.  git worktree list → exactly ONE line.
  (k) No trailing whitespace on any line of any file this round writes. If your
      environment denies `grep -rn ' $'`, run an equivalent Python scan
      (`l != l.rstrip()`) and say which command you actually ran.
  (l) gh pr list --state open --json number,headRefName → [].

Handback:    completion report plus the rewritten `.agent/handoff.md`. For each
             gate: the command, the exit code, the real output. "Green" as a
             word is not a result.
──────────────────────────────────────────────────────────────
