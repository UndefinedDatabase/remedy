── STEP integration-gate — F105 R49 ──────────────────────────
Goal:        Close the one durable gap R48's probe exposed, then run the
             feature's integration gate: full suite on the branch, full suite
             at the merge base with restored parity, and an attribution for
             every differing id.
Bundle:      C1 save block · C2 mirror · C3 register R-0269 and the R48 gate ·
             C4 fix R-0269 in the note · C5 the integration gate · C6 plan,
             handoff, push.
Change:      .agent/authored/f105-r49-1.md (new), .agent/last_block.md,
             .agent/live_review.md,
             docs/system/cache-optimal-prompt-ordering-v1.md,
             .agent/gate_f105_r49/ (new evidence dir), .agent/plan.md,
             .agent/handoff.md. NOTHING else. No production code, no tests.
Constraints: No production code under packages/ or apps/ and no test module is
             edited this round — a gate that repairs what it measures is not a
             gate. No PR, no merge, no `main`, no force-push. The base worktree
             is removed and pruned before handback.
Done when:   R-0269 is registered and its fix has landed, the gate evidence dir
             carries the full comparison, every differing id is attributed, and
             every gate below carries a real exit code.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────

C1 — write this ENTIRE block to `.agent/authored/f105-r49-1.md` byte for byte,
  commit it ALONE.
C2 — `cp` it over `.agent/last_block.md`, commit alone, `cmp` silent.

C3 — .agent/live_review.md. PAIR_ID is a REWRITE; PAIR_LR is CONTAINS-FROM.

<<<PAIR_ID_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0269.
<<<END_PAIR_ID_FROM>>>

<<<PAIR_ID_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0270.
<<<END_PAIR_ID_TO>>>

<<<PAIR_LR_FROM>>>
  read and any number there would be invented.
<<<END_PAIR_LR_FROM>>>

<<<PAIR_LR_TO>>>
  read and any number there would be invented.
- R-0269 (Low, F105 R48, registered at R49): the note
  `docs/system/cache-optimal-prompt-ordering-v1.md` states correctly that the
  measurement module's only numeric assertion is the directional
  `after_prefix >= before_prefix`, but it does not state what that guard cannot
  catch — and the reviewer's R48 probe measured exactly that. With every
  segment forced to a single rank, five of the six roles do not move at all,
  because their registration order already equals rank order, and `plan`
  collapses from 1463 to 227, which is precisely its own `before_prefix`, so
  the assertion still passes on a prompt whose ordering advantage has been
  destroyed. The module is NOT vacuous: reversing the sort key fails five of
  six roles, `orchestrator` at `after_prefix 37 < before_prefix 3872`. The
  point is narrower and worth durable words — the module is a REGRESSION guard
  on the ordering's VALUE, not a proof that the registry SORTS, and what proves
  the sort is the T003 goldens' rank assertions. That distinction currently
  lives only in `.agent/handoff.md`, which is rewritten every round, while the
  note is the durable home for it. OPEN.
- Reviewer gate on R48 (2026-08-12): PASS. Range `5e55669d..9c80cf59` = seven
  commits, exactly the nine paths the block named, and no production code under
  `packages/` or `apps/` among them. Insertions per commit 191, 172, 38, 322,
  177, 43 and 131, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r48-1.block.md`, the
  committed `.agent/authored/f105-r48-1.md` and `.agent/last_block.md` all
  three hash to
  `c6c7d4549d10470888aa7806f92790038060b735a60cff2ea48b97c00ecb4fae`
  at 191 lines; both `cmp` runs silent.
  Stray reconcile over C3: 38 added, 0 removed, 0 stray. PAIR_LR measured
  CONTAINS-FROM exactly as declared, FROM 1x before and 1x after; the ID line
  correctly did NOT move, because R48 registered nothing.
  Gates re-run by THIS reviewer, none taken from the handback:
  `python3 -m pytest tests/docs/ -q` `294 passed in 0.30s`;
  `test_prompt_cache_prefix.py` `16 passed in 0.20s`; the goldens, segments and
  conventions selection `109 passed, 10431 deselected in 2.53s`; the canary
  `42 passed in 21.57s`; one `^## Steps` heading; `^<<<` 0 in every written
  file; `git worktree list` primary ALONE and `git status --porcelain` empty.
  The numbers were not accepted on the module's word. The reviewer ran
  `python3 -m tests.orchestration.test_prompt_cache_prefix` and reproduced the
  note's six rows character for character, then checked the note's riskiest
  claims against the CODE rather than the report: the quoted `remedy stats
  cache` output is REAL (reproduced through `python3 -m apps.cli.grouped`,
  since `remedy` on PATH is sandbox-blocked here), `--json` really returns
  `"cache_read_share": null` with `"share_basis": "unmeasured"` and a
  `role_limit` line, `UNMEASURED` and `UNDEFINED_SHARE` both exist in
  `stats_ledger_cmd.py`, and `SegmentStabilityRank` really is the 0-5 scale the
  note documents. Nothing in the note is asserted that the code does not say.
  The measurement module earns its place: it reads every pre-migration form
  from the T003 goldens instead of retyping one, and carries three faithfulness
  guards plus a non-vacuity guard, which is what makes its numbers evidence
  rather than output.
  GATE J, re-run by the reviewer in a disposable worktree and then removed and
  pruned: the worker's report is TRUE and reproducible in both halves. The
  mutation this reviewer ORDERED — every segment forced to one rank — leaves
  the module at `16 passed`, for the measured reason recorded in R-0269. The
  worker's stronger second mutation, reversing the sort key, gives
  `5 failed, 11 passed`. Ordering the colour as a PROBE rather than as an
  expected result is exactly what §3 checklist item 5 exists for, and the probe
  did its job: it bought a true statement about what the guard proves instead
  of a false one. That the worker ran the second mutation unprompted, and
  reported the first as green rather than quietly reaching for a mutation that
  would look better, is why this round is trusted.
  One inaccuracy, noted and NOT a finding: the handoff justifies C7's size by
  DECISION F104 D1's single-file exemption, but C7 touches two `.agent/**`
  files, so that exemption does not apply. It does not need to — C7 inserts 131
  lines against a cap of 500.
  `LAST_REVIEWED_SHA` advances 5e55669d -> 9c80cf59.
- R49: SPLIT round — register R-0269 and fix it in the note, then run the
  feature's integration gate per docs/agents/integration_gate.md. R-0221 is
  known and will attribute phantom base-only failures through the UI auto-build
  mechanism; that is expected, not new.
<<<END_PAIR_LR_TO>>>

C4 — fix R-0269 in `docs/system/cache-optimal-prompt-ordering-v1.md`.
  Add ONE short paragraph to the measurement section, immediately after the
  existing paragraph that begins "The only numeric assertion the module makes".
  It says, in your own words and grounded in the numbers you measured at R48:
  what the directional guard DOES prove (composition never orders worse than
  the hand-written original), what it does NOT prove (that the registry sorts
  at all — with every segment forced to one rank, `plan` collapses to exactly
  its own `before_prefix` of 227 and the assertion still passes, while five of
  six roles do not move because their registration order already equals rank
  order), that reversing the sort key DOES fail five of six roles so the guard
  is not vacuous, and that the T003 goldens' rank assertions are what prove the
  sort. Keep it to one paragraph; do not restate the table.
  Then append to the END of `.agent/live_review.md` exactly one line:
    `  Landed: R-0269 — <one line: what changed, which commit>`
  and nothing else. Do NOT write a `Done:` paragraph; the reviewer authors that
  at the next gate.
  Commit C4 with the doc and that one line together.

C5 — the integration gate, per `docs/agents/integration_gate.md` EXACTLY. Read
  it and follow it; it is not restated here. Specifics for THIS run:
  - Merge base is `cfda4245b106aa17f2a7d846629dd1ab806766c7`.
  - Evidence dir `.agent/gate_f105_r49/`, matching the file set of the accepted
    precedent `.agent/gate_f104_r7/`: `branch_run.txt`, `branch_failed.txt`,
    `base_run.txt`, `base_failed.txt`, `comm_branch_only_failures.txt`,
    `comm_base_only_failures.txt`, `dist_hashes.txt`, `attribution.txt`,
    `worktree_cleanup.txt`. TRIMMED tails, never whole logs: that precedent is
    344 lines in total and this one stays in the same order of magnitude.
  - Full run logs are written OUTSIDE the repo, under `.remedy-wt/`, WHILE each
    suite runs; only trimmed copies are placed in the evidence dir afterwards.
    A log growing inside the repo during a run changes the worktree digest
    mid-run and fails the manifest-identity ids as FALSE positives (R-0176).
  - The base worktree is created ON A THROWAWAY BRANCH
    (`git worktree add -b tmp/base-gate <path> cfda4245b106aa17f2a7d846629dd1ab806766c7`),
    never detached — the self-dogfood branch guard refuses a detached HEAD by
    design (DECISION D3). Delete that branch and prune at the end, and prove it
    in `worktree_cleanup.txt` with `git worktree list` and `git branch --list 'tmp/*'`.
  - Restore base parity BEFORE the base run by COPYING the primary checkout's
    `apps/ui/node_modules` and `apps/ui/dist` into the base worktree — never
    symlink them: the UI auto-build runs npm install and writes THROUGH a
    symlink into the primary checkout. Set `REMEDY_UI_NO_AUTO_BUILD=1` for the
    base run but do NOT trust it alone: hash `apps/ui/dist` BEFORE and AFTER
    the base run into `dist_hashes.txt`. A changed hash voids the parity claim
    and forces per-id attribution instead.
  - R-0221 is a KNOWN open finding and will attribute phantom base-only
    failures through exactly this mechanism. Expected, not new: attribute them,
    do not report them as a discovery.
  - Attribute EVERY branch-only id per the procedure's step 4, by serial re-run
    of the exact node id, into `attribution.txt`. serial-pass is the xdist-flake
    class and is recorded, not a blocker. A reproducible branch-only failure
    coupled to F105 code is a BLOCKER: STOP, record it in full, and hand back
    WITHOUT attempting the fix.
  - Record wall clock for both runs. Over ~5 min is a note for a perf pass, not
    a failure.
  - If the flake class attributes MORE THAN 10 branch-only failures, say so
    plainly in the handoff: that is growing flake debt and the reviewer must
    surface it.

C6 — plan and handoff.
  Rewrite `.agent/plan.md` (UNDER 50 lines, keeping a `## Goal` heading and a
  `## Next Steps` heading). It must state: `LAST_REVIEWED_SHA` is 9c80cf59 with
  R48 GATED PASS; T001-T004 all DONE; the integration gate ran this round with
  its real result; the open findings and which of them are now Landed; and the
  next free ID after this round. Next Steps: closure per
  docs/roadmap/STATUS_closure_protocol.md, and PR #189, which the OPERATOR must
  resolve before F105's closure PR is cut.
  Then rewrite `.agent/handoff.md` (UNDER 60 lines, or over with a DECISION D15
  "Deviations, declared" line naming the real count and the mandated content
  that caused it). It carries: feature and round, branch, this round's commit
  SHAs, a changed-files table, an item-status table covering C1-C6, the gates
  below with real exit codes, the open-findings count, and the next expected
  action. It MUST carry the integration gate's real numbers: branch pass/fail
  counts, base pass/fail counts, the branch-only list, the base-only list, the
  attribution of every differing id, both wall clocks, and the dist-hash
  before/after parity proof.
  Commit C6, push the branch, create NO pull request.

Gates — real exit codes, never the word "green"
  A  sha256sum + cmp across the scratch block file, `.agent/authored/f105-r49-1.md`
     and `.agent/last_block.md`: all three equal, both cmp silent.
  B  wc -l the authored file against the cap of 400.
  C  PAIR_ID measured FROM 1x before / 0x after, TO 1x after. PAIR_LR measured
     FROM 1x before and 1x after, and each TO-ONLY added line exactly 1x AMONG
     THE LINES C3's OWN DIFF ADDS.
  D  Stray reconcile for C3: every ADDED line appears in the authored file.
     Report added, removed and stray counts.
  E  grep -c '^<<<' over live_review.md, plan.md, handoff.md and the note —
     all 0. (Scoped to these four on purpose: captured pytest output in the
     gate dir may legitimately contain such a sequence.)
  F  python3 -m pytest tests/docs/ -q
  G  The integration gate itself — branch run, base run, comm, attribution, all
     recorded in `.agent/gate_f105_r49/` with real exit codes and wall clocks.
  H  Canary: python3 -m pytest tests/cli/test_golden_path.py -q
  I  `git worktree list` shows the primary ALONE and `git branch --list 'tmp/*'`
     is empty; `git status --porcelain` is empty.
  J  insertions per commit under 500; `git diff --name-only 9c80cf59..HEAD` is
     exactly the paths named above.
