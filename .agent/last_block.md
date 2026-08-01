OUTCOME: executed — F062 claimed [~]; T001 delivered (product_smoke block
registered into the F061 seam, app_starts runner with bounded retry and
teardown-always, not-applicable non-gating, two real fixture apps). All three
ordered gates green; broken-start red→green proven by mutation in a throwaway
worktree (removed + pruned). No push, no PR. See .agent/handoff.md.

You are the Remedy worker (Window 2) for feature F062, round R1. Rules, in
  priority order: AGENTS.md, then docs/agents/worker_conventions.md, then this
  block. Read docs/roadmap/STATUS.md and docs/roadmap/features/T1_F062.md so
  you know the plan; implement ONLY this block. Full worker bootstrap
  contract: docs/agents/split_workflow.md (last_block.md first action,
  authored-text fidelity, handback per docs/agents/handback_template.md —
  note its new rule: PR create entries include the resulting PR number).

  ── STEP T001/1 — F062 ────────────────────────────────────────
  Goal:        Claim F062 and build T001: the product-smoke standard DoD
               block registration + app_starts + the not-applicable path +
               both fixture apps.
  Bundle:
   1. Open PR Gate (AGENTS.md): run
        gh pr list --state open --json number,headRefName,baseRefName,isDraft
      Expected: NO open PRs (#172 and #173 merged at this boundary). If
      exactly one eligible feature/*→main non-draft PR appears anyway, merge
      it per the gate; otherwise STOP per AGENTS.md and record raw output.
   2. Read .agent/candidates.md: it must contain no entries ("No open
      candidates."). A non-empty entry list = block condition — STOP and
      record it in the handback.
   3. Branch: git checkout main && git pull && git checkout -b
      feature/f062-product-smoke
   4. FIRST actions: write .agent/last_block.md (OUTCOME: pending + this
      block verbatim). Save the two AUTHORED TEXTS below to
      .agent/authored/f062-r1-1.md and .agent/authored/f062-r1-2.md (bytes
      between BEGIN/END markers, exclusive, incl. final newline). Verify
      each with sha256sum against its BEGIN-marker hash BEFORE committing —
      mismatch = STOP, report raw output, commit nothing. Commit 1
      (bookkeeping: authored/ + last_block).
   5. Apply f062-r1-1 → .agent/live_review.md by full-file copy (cmp → 0).
      Apply f062-r1-2 → docs/roadmap/STATUS.md (FROM line → TO line, occurs
      once). Rewrite .agent/plan.md and .agent/context.md for F062
      (context.md must satisfy ALL its test readers: a "Steps" section,
      "## Active Branch" with the feature/ slug, a roadmap F-id, and a
      pytest/resource-safety line — R-0162). Commit 2 with grep/cmp proofs
      in the handback.
   6. T001 (inspect FIRST, then build): locate the DoD compiler's
      standard-block seam (packages/orchestration/dod_schema.py /
      dod_compiler.py — F061 left the seam for F062 to register into) and
      the runtime-harness verbs for start/probe/log-capture/stop (F007
      harness). THEN implement: the product-smoke standard block that
      compiles into ordered blocking checks (this round only app_starts);
      app_starts = harness start + readiness probe within the configured
      window, teardown ALWAYS runs (assert no zombie process on every
      outcome); one retry after short backoff recorded as "passed on
      retry"; port-conflict reported as start failure with the harness's
      reason. Not-applicable path: no configured/detected runtime → block
      reports "smoke: not applicable (no runtime configured)" and does NOT
      gate — never silently green. Fixtures: two REAL mini-apps in the
      test tree (not harness mocks): one that starts clean, one with green
      unit tests but broken startup — its job must be HELD OPEN with a
      concrete reason ("start failed: <probe reason>").
  Change:      packages/orchestration/** (smoke block + registration),
               tests/orchestration/test_product_smoke.py + fixture apps
               under tests/, docs/roadmap/STATUS.md (claim line only),
               .agent/** state. Nothing beyond.
  Constraints: NO browser dependency (reject at self-review). Do not touch
               the harness's process semantics — orchestrate its existing
               verbs. Feature file's Do-not-touch applies. Commits small
               (<500-line diffs), Commit Gate before each.
  Done when:   python3 -m pytest tests/orchestration/test_product_smoke.py -q
               → exit 0 (include the broken-start red→green evidence);
               python3 -m pytest tests/docs/ -q → exit 0 (STATUS.md touched);
               python3 -m pytest tests/cli/test_golden_path.py -q → exit 0.
               Raw transcripts of all three in the handback.
  Handback:    completion report + rewrite .agent/handoff.md per
               docs/agents/handback_template.md, ending with
               "Handing back to Window 1 for review of <main-merge-base>..HEAD."
  ──────────────────────────────────────────────────────────────

  --- BEGIN f062-r1-1 sha256=49e41f96837a79b35f8e92a241a9162ce645949239c6a0cba76d7eef8de59af0 ---
  # Live Review — F062 Product smoke as the closing gate (Tier 1)

  Branch: feature/f062-product-smoke
  Scope: a standard DoD block proving a runnable app STARTS, its core
  paths RESPOND, and the console stream is clean, before a job may end
  green; not-applicable (no runtime) reported honestly, never silently
  green; fixtures are real mini-apps in the test tree. v1 is
  HTTP-level — no browser dependency (reject any diff adding one).

  ## Steps
  - R1 (SPLIT): claim + T001 — standard-block registration +
    app_starts + not-applicable path + fixture apps (green-tests/
    broken-start job held open with a concrete probe reason).
  - R2: T002 core_paths_respond + path extraction hand-off from the
    DoD compiler + fixtures (ok, wrong status, missing marker).
  - R3: T003 clean_console + documented pattern list +
    teardown-always (no zombie processes even on red); then the
    integration gate per docs/agents/integration_gate.md.
  - R4: closure per docs/roadmap/STATUS_closure_protocol.md.

  ## Findings
  - Next free ID: R-0166.

  ## Verdicts
  - (none yet — R1 pending)
  --- END f062-r1-1 ---

  --- BEGIN f062-r1-2 sha256=549239c5291ecdd628b5723c18776550cb17056b58423212fcdc9ef1eed38e55 ---
  FROM (exact line, occurs once in docs/roadmap/STATUS.md, replace once):
  - [ ] F062 — Product smoke as the closing gate
  TO:
  - [~] F062 — Product smoke as the closing gate
  --- END f062-r1-2 ---
