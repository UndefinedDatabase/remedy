── STEP session-stop — F105 R47 (STOP-triggered close) ───────
Goal:        Record, durably, that `.agent/STOP` appeared and that this session
             ended on it — plus the one finding that observation is worth.
Bundle:      C1a save block · C1b mirror · C2 register R-0268 and advance the
             ID · C3 plan and handoff.
Change:      .agent/authored/f105-r47-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md. NOTHING
             else. No production code, no tests, no docs, no catalog.
Constraints: `.agent/STOP` is NOT touched, NOT staged, NOT deleted. No PR, no
             merge, no `main`, no force-push, no new worktree.
Done when:   the diff touches exactly the five paths above and every gate below
             carries a real exit code.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────

C1a — write this ENTIRE block to `.agent/authored/f105-r47-1.md` byte for
  byte, commit it ALONE.
C1b — `cp` it over `.agent/last_block.md`, commit alone, `cmp` silent.

C2 — .agent/live_review.md. PAIR_ID is a REWRITE; PAIR_LR is CONTAINS-FROM.

<<<PAIR_ID_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0268.
<<<END_PAIR_ID_FROM>>>

<<<PAIR_ID_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0269.
<<<END_PAIR_ID_TO>>>

<<<PAIR_LR_FROM>>>
  session; the branch continues.
<<<END_PAIR_LR_FROM>>>

<<<PAIR_LR_TO>>>
  session; the branch continues.
- R-0268 (Low, F105 R46, registered NOT fixed): a `.agent/STOP` file appeared
  during R46 and this session could not establish who created it. The file is
  empty and untracked, with an mtime of 17:50:27 — 59 seconds AFTER the R46
  handoff was written (17:49:28) and about three minutes after `.agent/plan.md`
  (17:47:54). The R46 handback states that `.agent/STOP` is absent and was not
  created, and that statement was true when it was written; the file appeared
  afterwards. Two readings fit the evidence equally — the operator dropped the
  file asynchronously, which is exactly the mechanism G6 exists to serve, or
  the worker created it after writing its report. Nothing on disk separates
  them, and this entry deliberately does NOT accuse: it records the gap. What
  IS certain is that the timestamps are the only evidence a later session will
  have, which is the finding — a stop signal carries no author, no timestamp of
  intent and no reason, so the one control input allowed to interrupt a build
  is also the least auditable thing in the repository. Worth fixing where the
  signal is defined, not here: a STOP file that carried one line of provenance
  would have made this entry unnecessary. Registered against F105 because that
  is where it surfaced; it belongs to the self-drive protocol, not to prompt
  composition. OPEN.
- Reviewer gate on R46 (2026-08-10): PASS. Range `c7510403..aad00eee` = seven
  commits, exactly the eight paths the block named. Insertions per commit 298,
  230, 40, 49, 2, 20 and 131, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r46-1.block.md`, the
  committed `.agent/authored/f105-r46-1.md` and `.agent/last_block.md` all
  three hash to
  `b1c6eff1420194b5c02efc623cf7cb0084c2cab6891340a1e87a23b93649a165`
  at 298 lines; both `cmp` runs silent.
  Stray reconcile over all four authored commits: 40/0, 49/0, 2/0 and 20/0
  added/stray — zero strays anywhere.
  Gates re-run by THIS reviewer, none taken from the handback:
  `tests/cli/test_stats_cost.py` `41 passed in 0.39s`; the catalog and spine
  suites `113 passed in 0.57s`; the canary `42 passed in 19.95s`; `py_compile`
  exit 0 on both production files; `.agent/plan.md` 45 lines with both mandated
  headings; one `## Steps` heading; the ID line read R-0268; `^<<<` 0 in all
  six touched files.
  The payload was not accepted on its tests' word: the reviewer called
  `_cache_payload` directly on a synthetic three-bucket report. `builder` came
  back `0.06015` with `share_basis` `measured`, `reviewer` came back `null`
  with `unmeasured`, and `empty` came back `null` with `undefined`. The two
  absences stay distinguishable in the JSON exactly as they are in the table,
  and neither is ever a 0.
  The worker's THREE declared pair-shape deviations are ACCEPTED, and all three
  are the REVIEWER's authoring errors, verified against the files rather than
  taken from the declaration. PAIR_H and PAIR_ARG each insert a line INSIDE
  their FROM, so the TO cannot contain the FROM contiguously — both were
  REWRITEs mislabelled CONTAINS-FROM, the §3 checklist item 4 failure.
  PAIR_FLAG's TO triple already existed 1x on the `stats.verify-ledger` entry
  (measured 1x before, 2x after), so the ordered "TO 0x before" proof was
  unmeetable by construction — checklist item 6. Every FROM was unique, so all
  three edits landed once and in the right place; the cost was three deviation
  declarations on a round that executed correctly.
  `LAST_REVIEWED_SHA` advances c7510403 -> aad00eee.
- R47: STOP-triggered session close. `.agent/STOP` appeared, so guardrail G6
  ends the session here. State only: this gate, R-0268, the plan and the
  handoff. The branch is NOT closed and no PR exists; the next session reads
  the STOP file FIRST and, per Phase 1 rule 1, writes its handoff and ends
  without starting work until the operator removes it — which is the whole
  point of the file.
<<<END_PAIR_LR_TO>>>

C3 — plan and handoff
  Rewrite `.agent/plan.md` (UNDER 50 lines, keeping a `## Goal` heading and a
  `## Next Steps` heading). It must state: the session ENDED ON `.agent/STOP`
  at R47, not at its round cap; `LAST_REVIEWED_SHA` is aad00eee with R46 GATED
  PASS; T004's view half is DONE (`remedy stats cache`, table and `--json`);
  the open findings are R-0221, R-0239, R-0247, R-0262, R-0265, R-0266 and
  R-0268; and that NO work may start in the next session while `.agent/STOP`
  exists. Next Steps, in order, for after the operator clears the STOP: the
  T004 before/after comparison note with honest numbers whatever they are; the
  integration gate per docs/agents/integration_gate.md; closure per
  docs/roadmap/STATUS_closure_protocol.md; and PR #189, which the operator must
  resolve before F105's closure PR is cut.
  Then rewrite `.agent/handoff.md` (UNDER 60 lines, or over with a DECISION D15
  "Deviations, declared" line naming the count and its mandated causes). It
  carries: feature and round, branch, the commit SHAs of THIS round, a
  changed-files table, an item-status table, the gates below with real exit
  codes, the open-findings count, and the next expected action. It MUST state
  in its own section that `.agent/STOP` EXISTS, is empty and untracked, was NOT
  removed by this round, and that its presence — not a round cap and not a
  failure — is why the session ended. It must also state that
  `.agent/live_review.md` carries the R47 step line and no R47 gate record,
  deliberately, per the R-0264 distinction.
  Commit C3, push the branch, create NO pull request.

Gates — real exit codes, never the word "green"
  A  sha256sum + cmp across block file, authored file and last_block: equal,
     both cmp silent.  B  wc -l the authored file against the cap of 400.
  C  PAIR_ID measured FROM 1x before / 0x after, TO 1x after. PAIR_LR measured
     FROM 1x before and 1x after, TO 1x after.
  D  Stray reconcile for C2: every ADDED line appears in the authored file.
     Report added, removed and stray counts.
  E  grep -c '^<<<' over live_review.md, plan.md and handoff.md — all 0.
  F  python3 -m pytest tests/docs/ -q
  G  python3 -m pytest tests/ui_server/test_dashboard_contract.py -q
  H  Canary: python3 -m pytest tests/cli/test_golden_path.py -q
  I  `ls -la .agent/STOP` — it MUST still exist, empty, and MUST NOT appear in
     `git diff --cached` or in any commit. Prove it: `git log --stat` for this
     round names no STOP path, and `git status --porcelain` still shows it as
     untracked `?? .agent/STOP`.
  J  git worktree list shows the primary ALONE; insertions per commit under
     500; git diff --name-only aad00eee..HEAD is exactly the five paths named.

Note on gate I: `git status --porcelain` will NOT be empty this round, and that
is CORRECT rather than a violation — the untracked STOP file is a control
signal, not a work artifact, and committing it to make the tree look clean
would be the one thing this round must never do.
