OUTCOME: pending

You are the WORKER for F061 — Definition-of-Done compiler (Tier 1).
  Authority: AGENTS.md. Feature file: docs/roadmap/features/T1_F061.md — read
  it completely before coding. Save THIS ENTIRE block verbatim to
  .agent/last_block.md before doing anything else (append OUTCOME at handback).

  PHASE 0 — OPEN PR GATE (AGENTS.md)
  1. git status --porcelain  → must be empty. If not, STOP and report.
  2. gh pr list --state open --json number,headRefName,baseRefName,isDraft
     Expected: exactly one PR — #171, feature/f056-missions → main, not draft.
     If anything else, STOP and report per the gate rules.
  3. gh pr merge 171 --merge --delete-branch
  4. git checkout main && git pull

  PHASE 1 — BRANCH + CLAIM (first commit)
  1. git checkout -b feature/f061-dod-compiler
  2. Save the four AUTHORED TEXT payloads below: for each, copy EXACTLY the
     lines between its BEGIN and END markers (exclusive, including the final
     newline) to .agent/authored/f061-r1-<n>.md. Verify each:
     sha256sum .agent/authored/f061-r1-<n>.md  must equal the sha256 in its
     BEGIN marker. Any mismatch → STOP, report the raw sha256sum output, do
     not apply anything.
  3. Apply, by copy, never by retype:
     - f061-r1-1: in docs/roadmap/STATUS.md replace the FROM line with the TO
       line. Verify the FROM line occurred exactly once before, zero times
       after; the TO line exactly once after. No other line changes.
     - f061-r1-2 → .agent/live_review.md (full replacement, byte copy; then
       cmp .agent/authored/f061-r1-2.md .agent/live_review.md → 0)
     - f061-r1-3 → .agent/plan.md (full replacement, byte copy, cmp → 0)
     - f061-r1-4 → .agent/context.md (full replacement, byte copy, cmp → 0)
  4. Commit 1 (authored files + applied state + STATUS claim + last_block):
     chore(f061): claim F061 — STATUS [~] + state reset
  5. Gate for commit 1 (docs-round gate + canary):
     python3 -m pytest tests/docs/ -q
     python3 -m pytest tests/cli/test_golden_path.py -q
     Any red → STOP (AGENTS.md If-Blocked), record raw output in the handoff.

  ── STEP T001+T002/4 — F061 ────────────────────────────────────
  Goal:        Machine-checkable DoD: versioned schema + compiler with
               deterministic fallback (T001), then runners with per-check
               evidence (T002).
  Bundle:
    T001 — schema + compiler + fallback + fixtures + traceability
      - packages/orchestration/dod_schema.py (or join the existing pattern in
        packages/orchestration/schemas/ — inspect first, follow the F005
        structured-output conventions): versioned DoD schema; checks[], each
        {id, kind: pytest|lint|build|runtime_flow|custom_cmd, spec
        (kind-specific, declarative), blocking: bool,
        source: compiled|plan_acceptance|standard}.
      - packages/orchestration/dod_compiler.py: compile(intake, plan) → DoD
        via provider call with the same discipline as intake/plan
        (schema-enforced, parse-retried). Merges three sources: compiled
        checks from intent; one check per plan acceptance line; standard
        checks (registry seam — the product-smoke feature registers here
        later, keep it a simple extension point).
      - TRACEABILITY RULE (verbatim from the feature file, tested): every
        plan acceptance line maps to at least one check id.
      - Deterministic fallback: no provider → minimal DoD built from plan
        acceptance lines, labeled compiled=false/deterministic — never
        presented as compiled.
      - Compile-time validation rejects detectable nonsense specs
        (unrunnable kinds, empty selectors).
      - Three long-goal fixture missions with golden DoDs under
        tests/orchestration/fixtures/ (follow the existing fixture layout).
      - Tests: tests/orchestration/test_dod_compiler.py — schema round-trip,
        three golden fixtures, traceability rule (positive + violation),
        fallback labeling, nonsense-spec rejection.
      T001 GATE (run before starting T002; red → STOP):
        python3 -m pytest tests/orchestration/test_dod_compiler.py -q
        python3 -m pytest tests/cli/test_golden_path.py -q
    T002 — runners for pytest / lint / build / custom_cmd
      - packages/orchestration/dod_runners.py: execute a check through the
        EXISTING subprocess discipline (inspect how current runners/probes
        shell out; reuse, don't reinvent). Per-check evidence: command, exit
        code, output tail. Result: green/red per check.
      - Missing tool → red with reason tool_unavailable, never a silent pass.
      - custom_cmd runs inside the worktree under the fence rules (F017).
      - runtime_flow: schema kind EXISTS but has NO runner in this round —
        the runner registry fails loud on the unsupported kind (tested).
        The runner lands in T003.
      - Tests: tests/orchestration/test_dod_runners.py — each of the four
        kinds proven red AND green (use tiny fixture commands/repos, no
        network), tool_unavailable path, per-check evidence shape,
        runtime_flow loud failure.
      T002 GATE (red → STOP):
        python3 -m pytest tests/orchestration/test_dod_runners.py -q
        python3 -m pytest tests/cli/test_golden_path.py -q
  Change:      ONLY: the new modules above, their tests, fixtures,
               docs/roadmap/STATUS.md (claim line), .agent/ state. Nothing
               else — especially NO job-lifecycle/terminal-path change (that
               is T004, its own round).
  Constraints: Feature file Do-not-touch (visual regression, browser
               automation depth, Tier-11 depth). Commits <500-line diffs,
               multiple commits expected (schema / compiler / fixtures /
               runners are natural cuts). Mandatory self-review loop before
               every commit. No mutation red-proofs in the primary checkout —
               disposable git worktree only, removed + pruned afterwards.
  Done when:   Both slice gates green (transcripts recorded) plus final:
               python3 -m pytest tests/orchestration/test_dod_compiler.py \
                   tests/orchestration/test_dod_runners.py -q
               python3 -m pytest tests/cli/test_golden_path.py -q
               python3 -m pytest tests/docs/ -q
               git status --porcelain  → empty
  Handback:    Completion report + REWRITE .agent/handoff.md: per-commit
               changed-files table (path, +/-, reason), raw verification
               transcripts (command, exit code, real output — never the word
               "green"), authored-text proofs (sha256sum outputs, cmp
               results, STATUS-line occurrence counts), deviations &
               assumptions (A9) explicitly listed. STOP at the first red
               gate and hand back with the raw failure — do not continue
               into the next slice.
  ──────────────────────────────────────────────────────────────

  ----- BEGIN AUTHORED f061-r1-1 sha256=d362fe36dec188aaf5df2ec355272d69f4d723078a31df7f2692ee63989ede0f -----
  FROM (exact line, occurs once in docs/roadmap/STATUS.md, replace once):
  - [ ] F061 — Definition-of-Done compiler
  TO:
  - [~] F061 — Definition-of-Done compiler
  ----- END AUTHORED f061-r1-1 -----

  ----- BEGIN AUTHORED f061-r1-2 sha256=552f4d6643a097d35db839b284dd85fda657706de8874a9250b92220e1b0d9e8 -----
  # Live Review — F061 Definition-of-Done compiler (Tier 1)

  Branch: feature/f061-dod-compiler
  Scope: user intent + Flight Plan compile into a machine-checkable DoD
  (versioned schema; checks with blocking flags); runners execute checks
  with per-check evidence; the job-end gate (T004) holds a job open on a
  red blocking check. Compiler is an LLM step with intake/plan
  discipline: schema-enforced, parse-retried, honest deterministic
  fallback labeled compiled=false.

  ## Steps
  - R1 (LARGE): T001 schema + compiler + deterministic fallback + three
    fixture missions with golden DoDs + acceptance-traceability rule,
    then T002 runners (pytest/lint/build/custom_cmd) with per-check
    evidence, each kind proven red and green — awaiting handback.
  - Later: T003 runtime_flow runner on the harness; T004 job-end gate +
    report matrix; integration gate; closure.

  ## Findings
  - None yet. Next free ID: R-0164 (continues monotonically from F056).

  ## Verdicts
  - (none yet)
  ----- END AUTHORED f061-r1-2 -----

  ----- BEGIN AUTHORED f061-r1-3 sha256=d204ac1ed3ced002a8ee785e0ef27774da71ebf2ab6d57fcd79b55a3c5725992 -----
  # Plan — F061 Definition-of-Done compiler

  ## Goal
  "Done" stops being vibes: user intent plus the Flight Plan compile
  into a machine-checkable DoD — a versioned list of concrete checks
  (pytest, lint, build, runtime_flow, custom_cmd) with blocking flags —
  and a job only ends green when all blocking checks pass. Three fixture
  missions compile into sensible DoDs; every plan acceptance line is
  traceable to at least one check id; the fallback DoD (no provider) is
  deterministic and labeled compiled=false.

  ## Current Step
  R1 (LARGE bundle): T001 — DoD schema + dod_compiler.py +
  deterministic fallback + three long-goal fixtures with golden DoDs +
  the traceability rule tested; then T002 — runners for
  pytest/lint/build/custom_cmd through the existing subprocess
  discipline with per-check evidence (command, exit, output tail), each
  kind proven red and green; missing tool = red with reason
  tool_unavailable.

  ## Next Steps
  - R2: T003 runtime_flow runner on the runtime harness + fixture app
    flow; then T004 job-end gate + report matrix + end-to-end.
  - Integration gate round, then closure per STATUS_closure_protocol.md.

  ## Risks
  - runtime_flow is schema-valid in R1 but has no runner until T003 —
    the runner registry must fail loud (unsupported kind), never pass.
  - The job-end gate (T004) touches the terminal-green path — deferred
    to its own round; nothing in R1 changes job lifecycle behavior.
  - Compiled nonsense checks must fail validation at compile time where
    detectable; a missing linter must never silently pass.
  ----- END AUTHORED f061-r1-3 -----

  ----- BEGIN AUTHORED f061-r1-4 sha256=fb02aa8585cd73ee4cbed9e74d2015007d038ea2fbfde526897b557927dd9175 -----
  # Context — F061 Definition-of-Done compiler (Tier 1)

  ## Active Branch
  `feature/f061-dod-compiler`
  Base commit: main after PR #171 merge (F056)

  ## Steps (round map)
  R1 (LARGE): STATUS claim `[~]` + state reset → T001 DoD schema +
  compiler + deterministic fallback + three golden-DoD fixtures +
  traceability rule → T002 runners (pytest/lint/build/custom_cmd) with
  per-check evidence, red and green per kind.
  R2: T003 runtime_flow on the harness → T004 job-end gate + matrix.
  Then integration gate; closure is its own later round.

  ## Scope
  `packages/orchestration/dod_schema.py` and
  `packages/orchestration/dod_compiler.py` (new; join the existing
  schema/validation pattern), `packages/orchestration/dod_runners.py`
  (new), fixtures under tests/orchestration/fixtures/, plus
  `tests/orchestration/test_dod_compiler.py` and
  `tests/orchestration/test_dod_runners.py`. Also `docs/roadmap/STATUS.md`
  (claim line only) and `.agent/` state. Nothing beyond.

  ## Gates (round verification, pytest)
  python3 -m pytest tests/orchestration/test_dod_compiler.py -q   T001 gate
  python3 -m pytest tests/orchestration/test_dod_runners.py -q    T002 gate
  python3 -m pytest tests/cli/test_golden_path.py -q              canary
  python3 -m pytest tests/docs/ -q                                docs gate
  Resource safety: everything runs through these pytest wrappers; no
  unbounded subprocess fan-out from runner tooling.

  ## Constraints
  - Traceability rule verbatim: every plan acceptance line maps to at
    least one check id (tested).
  - Fallback DoD (no provider) is deterministic, built from plan
    acceptance lines, labeled compiled=false — never presented as
    compiled.
  - Missing tool = red with reason tool_unavailable; never a silent
    pass. custom_cmd runs inside the worktree under the fence rules.
  - runtime_flow: schema kind exists, NO runner in R1 — registry fails
    loud on unsupported kind.
  - No job-lifecycle change in R1 (gate is T004, its own round).
  - Reviewer-authored texts under .agent/authored/ are applied by copy
    and sha256-verified before use; never hand-edited.
  - Commits stay under 500-line diffs (AGENTS.md).
  - context.md satisfies its FULL test reader list: a "Steps" section,
    "## Active Branch" with a feature/ slug, a roadmap F-id, and this
    pytest/resource line (R-0162; reader rule in
    planner_reviewer_prompt.md §4 item 11).

  ## Do not touch
  Visual regression, deep browser automation (the smoke feature
  decides), Tier-11 verification depth, the job-end terminal path
  (T004). docs/roadmap/ROADMAP.md; STATUS entries other than the F061
  line.
  ----- END AUTHORED f061-r1-4 -----
