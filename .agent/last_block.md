OUTCOME: executed — R-0166 fixed (pushed FIRST), T002 core_paths_respond and
T003 clean_console + smoke config delivered, integration gate green on branch
(14969 passed) and base (14900 passed) with both comm directions EMPTY.
Worktree removed + pruned. Branch pushed. See .agent/handoff.md and
.agent/gate_f062_r2/.

You are the Remedy worker (Window 2) for feature F062, round R2 (LARGE).
  Rules in priority order: AGENTS.md, docs/agents/worker_conventions.md, this
  block. Full worker contract: docs/agents/split_workflow.md (last_block.md
  first action, authored-text fidelity, handback per
  docs/agents/handback_template.md). This is ONE autonomous multi-part block:
  exactly ONE handback, at the very end; intermediate parts end as checkpoint
  notes in the final completion report. STOP-ON-RED: if a slice's verification
  is red after your fix attempts within the slice, stop the block there and
  hand back honestly.

  PART 0 — persist findings + R-0166 fix (FIRST, own commit, then push)
   1. Write .agent/last_block.md (OUTCOME: pending + this block verbatim).
   2. Save the three AUTHORED TEXTS below to .agent/authored/f062-r2-{1,2,3}.md
      (bytes between BEGIN/END markers, exclusive, incl. final newline);
      verify each sha256sum against its BEGIN marker BEFORE committing —
      mismatch = STOP, report raw bytes, commit nothing.
   3. Apply all three to .agent/live_review.md (FROM block → TO block, each
      occurs exactly once; copy from the saved files, never retype).
      Commit 1: findings + verdict persisted + bookkeeping.
   4. git push -u origin feature/f062-product-smoke  ← the R-0166(a) fix.
      Then append under the R-0166 entry:  Done: R-0166 (pushed; this
      handback tables all commits).  Amend nothing else. Commit + push.

  PART 1 — T002 core_paths_respond (per-slice verify, then continue)
   - Extend the closed vocabulary: product_smoke.SMOKE_CHECKS and
     dod_schema.SMOKE_CHECK_NAMES gain "core_paths_respond"; stable check id
     (smoke-core-paths); spec keys extend by what the check needs (e.g.
     "paths") — keep the set closed and compile-time validated.
   - The block contributes it AFTER app_starts (ordered), blocking where a
     runtime resolves, same not-applicable discipline as T001.
   - Probe set: the configured health path PLUS paths the DoD compiler hands
     off from intent/plan (e.g. "/", the feature's route). Expectation =
     status ok and, where declared, a content marker. HTTP-level only.
   - Reuse _run_app_once (body = the path walk); teardown always.
   - Fixtures: ok / wrong status / missing marker — real mini-apps.
   - Verify NOW: python3 -m pytest tests/orchestration/test_product_smoke.py
     tests/orchestration/test_dod_runners.py tests/orchestration/test_dod_schema.py
     -q → exit 0 (adjust the schema-test path to the real file if it differs;
     record the real command). Red after fixes → STOP + handback.

  PART 2 — T003 clean_console + smoke config (per-slice verify)
   - clean_console: the harness-captured app output scanned for a SMALL
     DOCUMENTED pattern list (tracebacks, "ERROR", framework fatals),
     case-sensitive; any hit = red with the matched lines QUOTED. Runs as the
     third ordered check.
   - Smoke config table (project config): enabled (default true where a
     runtime exists), path-list override, error-pattern ADDITIONS, readiness
     window. Config extends patterns — code stays the documented base list.
   - Fixture logging an error → red with quoted lines; teardown-always test:
     no zombie processes even on red (assert real ports/processes).
   - Verify NOW: the scoped suites above + python3 -m pytest
     tests/cli/test_golden_path.py -q → exit 0. Red after fixes → STOP.

  PART 3 — integration gate (docs/agents/integration_gate.md, exactly)
   - Branch full suite AND base full suite (pytest -n auto), base in a
     throwaway worktree ON a throwaway branch, parity by COPYING
     apps/ui/node_modules + apps/ui/dist, REMEDY_UI_NO_AUTO_BUILD=1.
   - Raw outputs, comm attribution both directions, flake classes named.
     A branch-only regression = fix it (normal repair inside this slice),
     re-run; red after fixes → STOP + handback. Worktree removed + pruned
     before handback (git worktree list proof).

  Constraints: NO browser dependency (reject at self-review). Harness process
  semantics untouched. NO closure work in this block — closure is its own
  round. Commits small (<500-line diffs), Commit Gate each; docs-round gate
  (tests/docs/) only if any commit touches docs/roadmap/**. plan.md/context.md
  kept current (context keeps its full reader-pin set, R-0162).
  Done when:   every slice's verification exit 0 AND the integration gate is
               green on branch and base with attribution recorded.
  Handback:    push FIRST, then completion report + .agent/handoff.md per
               template — ALL commits tabled (grouped self-reference allowed),
               PR-create entries would carry the PR number (none expected),
               raw transcripts per slice, item-status table for
               R-0166/T002/T003/gate, ending with
               "Handing back to Window 1 for review of 30177869..HEAD."

  --- BEGIN f062-r2-1 sha256=b7d285c84623fa1863f9fd01fc1820431517083e3ed9183df9699dfbfa5c54ac ---
  FROM (exact block, occurs once in .agent/live_review.md):
  ## Findings
  - Next free ID: R-0166.
  TO:
  ## Findings
  - R-0166 (process, Low) 2026-08-01: handback form, two defects:
    (a) branch not pushed at handback (split_workflow.md single-writer
    rule: hand back only with a clean, committed, PUSHED branch;
    AGENTS.md Push Discipline); (b) the handoff commit (30177869) is
    absent from the handoff's Commits section and Range names HEAD
    1e3e58b0 while the branch head is the handoff commit — the R-0149
    exception allows a grouped self-reference table, not an omission.
    Fix: push as the FIRST action of R2; every later handback follows
    a push and tables ALL commits (grouped self-reference allowed).
  - Next free ID: R-0167.
  --- END f062-r2-1 ---

  --- BEGIN f062-r2-2 sha256=355cbe33d174285a2cc87e90244492a46b4e87a6f34ccb8feb5423dadff3d2bd ---
  FROM (exact block, occurs once in .agent/live_review.md):
  - R2: T002 core_paths_respond + path extraction hand-off from the
    DoD compiler + fixtures (ok, wrong status, missing marker).
  - R3: T003 clean_console + documented pattern list +
    teardown-always (no zombie processes even on red); then the
    integration gate per docs/agents/integration_gate.md.
  - R4: closure per docs/roadmap/STATUS_closure_protocol.md.
  TO:
  - R2 (LARGE, operator LARGE-mode 2026-08-01): T002
    core_paths_respond + path extraction hand-off + fixtures (ok,
    wrong status, missing marker); THEN T003 clean_console +
    documented pattern list + teardown-always (no zombie processes
    even on red) + the smoke config table; THEN the integration gate
    per docs/agents/integration_gate.md — per-slice verification,
    stop-on-red.
  - R3: closure per docs/roadmap/STATUS_closure_protocol.md.
  --- END f062-r2-2 ---

  --- BEGIN f062-r2-3 sha256=433fe1c29e43956e1a28b34b5ceae1e7bd80b22993488f68bdd19c0851f1bba0 ---
  FROM (exact block, occurs once in .agent/live_review.md):
  ## Verdicts
  - (none yet — R1 pending)
  TO:
  ## Verdicts
  - R1: PASS (SPLIT round, 2026-08-01). Range b836d364..1e3e58b0 plus
    handoff commit 30177869 (handoff+last_block only, verified).
    Reviewer re-ran: smoke 27, dod suites+schemas 200, docs 293,
    canary 42 — all exit 0, matching the handback transcripts.
    Transport cmp 0 disk-to-disk against scratchpad originals (both
    texts); STATUS claim FROM 1→0 / TO 0→1. Spot-checks: primary
    worktree only, no registration-by-import (fresh-process providers
    empty), no leaked runtime configs, 7 commits in range as tabled.
    Deviations 1–5 accepted: new check kind product_smoke; kind-set
    pin 5→6; additive StandardCheckContext.worktree_root;
    not-applicable = non-blocking red in reported_red (P6);
    _run_app_once extraction sharing the process discipline, harness
    semantics untouched. R-0166 registered (handback form, Low).
    LAST_REVIEWED_SHA = 30177869.
  --- END f062-r2-3 ---
