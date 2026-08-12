── STEP T004-note/1 — F105 R48 (before/after comparison note) ─
Goal:        Close T004's remaining half: measure the cacheable-prefix change
             per role from the goldens' own frozen pre-migration forms, and
             document it honestly — including that the provider-side
             cache-read share is UNMEASURED because no ledger exists on disk.
Bundle:      C1 save block · C2 mirror · C3 record the R47 gate · C4 the
             measurement module · C5 the ist-doc + index row · C6 the feature
             file's Built State · C7 plan, handoff, push.
Change:      .agent/authored/f105-r48-1.md (new), .agent/last_block.md,
             .agent/live_review.md,
             tests/orchestration/test_prompt_cache_prefix.py (new),
             docs/system/cache-optimal-prompt-ordering-v1.md (new),
             docs/README.md, docs/roadmap/features/T2_F105.md,
             .agent/plan.md, .agent/handoff.md. NOTHING else.
Constraints: No production code under packages/ or apps/ is edited — this
             round only MEASURES what T001-T003 already built. No frozen
             golden template constant is edited for any reason. No PR, no
             merge, no `main`, no force-push. Any destructive probe runs ONLY
             in a disposable git worktree removed before handback.
Done when:   the diff touches exactly the nine paths above, the note carries
             REAL measured numbers, and every gate below carries a real exit
             code.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────

C1 — write this ENTIRE block to `.agent/authored/f105-r48-1.md` byte for
  byte, commit it ALONE.
C2 — `cp` it over `.agent/last_block.md`, commit alone, `cmp` silent.

C3 — .agent/live_review.md. PAIR_LR is CONTAINS-FROM (the TO contains the
  FROM verbatim as its first line, then appends). No ID advance this round:
  no new finding is registered, so the next free ID stays R-0269.

<<<PAIR_LR_FROM>>>
  point of the file.
<<<END_PAIR_LR_FROM>>>

<<<PAIR_LR_TO>>>
  point of the file.
- Reviewer gate on R47 (2026-08-12): PASS. Range `aad00eee..5e55669d` = five
  commits, exactly the five paths the block named. Insertions per commit 140,
  126, 58, 102 and 12, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r47-1.block.md`, the
  committed `.agent/authored/f105-r47-1.md` and `.agent/last_block.md` all
  three hash to
  `318a9c5d57188d45ea659ba8c25c0e54df99971070eaca5051c63531baa39fec`
  at 140 lines; both `cmp` runs silent.
  Stray reconcile over C2: 58 added, 1 removed, 0 stray — the single removal
  is the PAIR_ID FROM line its own REWRITE replaces.
  Pair shapes MEASURED, both exactly as declared: PAIR_ID a rewrite, the ID
  line now reading R-0269 1x and R-0268 0x; PAIR_LR contains-from, appended at
  its unique tail anchor.
  Gates re-run by THIS reviewer, none taken from the handback:
  `python3 -m pytest tests/docs/ -q` `294 passed in 0.26s`;
  `tests/ui_server/test_dashboard_contract.py` `70 passed in 4.44s`; the canary
  `42 passed in 19.58s`; `.agent/plan.md` 47 lines carrying both mandated
  headings; exactly one `^## Steps` heading in this file; `^<<<` 0 in all three
  written state files; `git worktree list` shows the primary ALONE.
  `.agent/STOP` is GONE at review time. The operator removed it between the
  sessions — which is precisely the mechanism G6 exists to serve, and the
  reason work resumes here. `git status --porcelain` is empty.
  The handoff's ONE declared structural deviation, C3b, is ACCEPTED: a gate row
  reporting insertions per commit cannot carry its own commit's count until
  that commit exists, so filling it in afterwards beats leaving a placeholder
  in an evidence table. It touches only a path the block already named.
  The R-0268 placement note is ACCEPTED as honest disclosure, and the placement
  is the REVIEWER's doing, not the worker's: PAIR_LR's only anchor was the tail
  step line, so the finding landed inside `## Steps` rather than under
  `## Findings`. The worker executed the authored bytes exactly. It costs
  nothing but this sentence.
  `LAST_REVIEWED_SHA` advances aad00eee -> 5e55669d.
- R48: SPLIT round — T004's remaining half. The cacheable prefix per role is
  measured before and after the migration, from the goldens' own frozen
  pre-migration forms, and the honest note lands in a new ist-doc. The
  provider-side cache-read share stays UNMEASURED and the note says so: no
  `ledger.sqlite` exists anywhere in this checkout, so there are no actuals to
  read and any number there would be invented.
<<<END_PAIR_LR_TO>>>

C4 — `tests/orchestration/test_prompt_cache_prefix.py` (new). This module
  MEASURES; it does not re-pin prompt content.

  The six migrated roles, each with the golden that already freezes its
  PRE-migration form:
    intake        tests/orchestration/test_intake_prompt_golden.py
    plan          tests/orchestration/test_plan_prompt_golden.py
    mission       tests/orchestration/test_mission_prompt_golden.py
    builder       tests/orchestration/test_builder_prompt_golden.py
    reviewer      tests/orchestration/test_reviewer_prompt_golden.py
    orchestrator  tests/orchestration/test_orchestrator_prompt_golden.py
  READ each golden FIRST and reuse its existing frozen form and its existing
  builder-invocation shape. Never retype a frozen template: import it, or
  slice it exactly as that golden already does.

  For each role, build TWO renders that differ ONLY in volatile input — the
  per-task/per-round content that ranks last (task, steering) — and are
  otherwise identical. Measure, in characters:
    before_prefix   longest common prefix of the two PRE-migration renders
    after_prefix    longest common prefix of the two COMPOSED renders
    before_total    length of the first PRE-migration render
    after_total     length of the first composed render
  Assert, per role, `after_prefix >= before_prefix`. That is the feature's
  DIRECTIONAL acceptance and the ONLY assertion this module makes about the
  numbers. Do NOT assert exact byte counts: a legitimate later prompt change
  would then break a test that is not about content.
  Expose the table through one module-level function `measure_cacheable_prefixes()`
  returning a mapping of role -> the four numbers, so the doc's figures and the
  test's figures cannot drift. Find an invocation that actually WORKS from the
  repo root, verify it, and record that exact command plus its raw output in
  the handback; the doc cites the same command.
  If a role genuinely cannot be measured this way, SKIP it with a reason naming
  what is missing, and record the skip in the doc. An honest gap beats an
  invented number.

C5 — `docs/system/cache-optimal-prompt-ordering-v1.md` (new) AND its
  `docs/README.md` index row, in the SAME commit — `tests/docs/` asserts that
  every relative link in `docs/README.md` resolves, so a row without its file
  is red. Register it in BOTH places the index uses: the quick-find table near
  the other `system` rows, and the system-category list.
  This doc is WORKER-AUTHORED from the REAL measurements: the reviewer does not
  supply its text because the reviewer does not know the numbers. It states:
  - what F105 changed about composition (registry, stability ranks, segment
    manifest) and that prompt CONTENT did not change, only its order;
  - the before/after cacheable-prefix table, per role, with the four measured
    numbers and the exact command that reproduces them;
  - plainly, that the provider-side cache-read share is NOT measured: no
    `ledger.sqlite` exists in this checkout, so `remedy stats cache` has no
    actuals to read and renders `unmeasured` rather than a 0. Give both words
    their meanings — `unmeasured` = nothing was reported, `undefined` = inputs
    were reported as zero — because that distinction is the whole point of the
    view;
  - the two known seams already inventoried in `.agent/t004_inventory.md` §1
    and §3: a provider that reports usage but no cache field leaves a
    measured-looking `0` the ledger cannot tell from a real zero, and the
    ledger's `role` is a hardcoded `builder` in production data, so a per-role
    breakdown from the ledger alone would be a single bucket. State them; do
    not work around them.
  Open the neighbouring `docs/system/*.md` files and match their existing
  status-banner shape rather than inventing one.

C6 — `docs/roadmap/features/T2_F105.md`: append a `## Built State` section in
  the shape `docs/roadmap/features/T2_F104.md:93` already uses — one italic
  "as built and reviewed on branch" line, then bullets covering T001-T004 that
  name the real modules (`packages/orchestration/prompt_segments.py`,
  `packages/orchestration/role_conventions.py`, the six migrated builders, and
  `remedy stats cache` with its `--json` mode), plus a pointer to the new
  ist-doc for the numbers. Do NOT restate the measured numbers here: one
  source, and the ist-doc is it.

C7 — plan and handoff.
  Rewrite `.agent/plan.md` (UNDER 50 lines, keeping a `## Goal` heading and a
  `## Next Steps` heading). It must state: `LAST_REVIEWED_SHA` is 5e55669d with
  R47 GATED PASS; T004 is now COMPLETE, view and note; the open findings are
  R-0221, R-0239, R-0247, R-0262, R-0265, R-0266 and R-0268, all seven still
  OPEN and none touched this round; and the next free finding ID stays R-0269.
  Next Steps, in order: the integration gate per docs/agents/integration_gate.md;
  closure per docs/roadmap/STATUS_closure_protocol.md; and PR #189, which the
  OPERATOR must resolve before F105's closure PR is cut.
  Then rewrite `.agent/handoff.md` (UNDER 60 lines, or over with a DECISION D15
  "Deviations, declared" line naming the real count and the mandated content
  that caused it). It carries: feature and round, branch, this round's commit
  SHAs, a changed-files table, an item-status table covering C1-C7, the gates
  below with real exit codes, the open-findings count, and the next expected
  action. It MUST also carry the measured before/after table and the exact
  command that produced it, and the gate-J probe outcome in words.
  Commit C7, push the branch, create NO pull request.

Gates — real exit codes, never the word "green"
  A  sha256sum + cmp across the scratch block file, `.agent/authored/f105-r48-1.md`
     and `.agent/last_block.md`: all three equal, both cmp silent.
  B  wc -l the authored file against the cap of 400.
  C  PAIR_LR is CONTAINS-FROM: measure FROM 1x before and 1x after, and each
     TO-ONLY added line exactly 1x AMONG THE LINES C3's OWN DIFF ADDS.
  D  Stray reconcile for C3: every ADDED line appears in the authored file.
     Report added, removed and stray counts.
  E  grep -c '^<<<' over live_review.md, plan.md, handoff.md, the new ist-doc,
     docs/README.md and T2_F105.md — all 0.
  F  python3 -m pytest tests/docs/ -q     (docs-round gate; roadmap is touched)
  G  python3 -m pytest tests/orchestration/test_prompt_cache_prefix.py -q
  H  python3 -m pytest tests/orchestration/ -q -k "prompt_golden or prompt_segments or role_conventions"
     — the goldens must still pass; this round must not have moved them.
  I  Canary: python3 -m pytest tests/cli/test_golden_path.py -q
  J  PROBE — non-vacuousness of C4, in a DISPOSABLE git worktree at HEAD ONLY:
     defeat the stability ordering there (e.g. give every registered segment
     the same rank) and report whether gate G goes RED. Report the REAL outcome
     whatever it is: a green result means the new test proves less than it
     appears to, and that is a finding worth having, not a failure to hide.
     Remove and prune the worktree before handback, so `git worktree list` then
     shows the primary ALONE and `git status --porcelain` is empty.
  K  insertions per commit under 500; `git diff --name-only 5e55669d..HEAD` is
     exactly the nine paths named above.
