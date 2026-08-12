── STEP R26 (repair, SPLIT) — F105 ───────────────────────────
Goal:        Record the R25 gate, then fix the two findings R25 registered:
             R-0253 (§4.9 counts whole-file where it can only hold over the
             diff) and R-0254 (a shared helper reports a reviewer-side fault
             as a builder fault).
Bundle:      C1 save this block · C2 record the R25 gate · C3 fix R-0253 ·
             C4 fix R-0254 · C5 plan and handoff.
Change:      `.agent/authored/f105-r26-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`,
             `packages/orchestration/pingpong_loop.py`,
             `tests/orchestration/test_builder_prompt_golden.py`,
             `.agent/plan.md`, `.agent/handoff.md`. Nothing else.
Constraints: SPLIT round (docs/agents/planner_reviewer_prompt.md §3, "Round
             types"): C4 touches production code under `packages/`, so you
             execute and the reviewer gates. Never self-certify it.
             `_drop_one_newline_per_segment_boundary` keeps its name, its
             signature and all three of its branches. ONLY the message string
             changes. Do not rename the test file, do not touch the other five
             migration sites or their goldens, do not reflow any line you were
             not given a pair for.
             A landed fix gets one `Landed: R-XXXX` line and no `Done:` text
             (§4.4).
Done when:   every gate below is run and its REAL exit code recorded.

C1 — save this block verbatim, TWO commits
  C1a `cp` this block to `.agent/authored/f105-r26-1.md`. Commit it ALONE.
  C1b `cp` the same bytes to `.agent/last_block.md`. Commit separately.
  Both are `cp` of the file on disk — never a retype. `sha256sum` both plus
  `cmp`, and record the digest in the handback.

C2 — the R25 gate record (own commit)
  Apply PAIR_A to `.agent/live_review.md`. PAIR_A is APPEND-shaped: the TO
  contains the FROM verbatim as its prefix. Prove FROM exactly 1x, and count
  TO-only ADDED LINES IN THE DIFF (`git show --numstat` on this commit) with
  the stray count. Do NOT count whole-file occurrences — that is the very
  reading R-0253 exists to retire.

<<<PAIR_A_FROM>>>
  `LAST_REVIEWED_SHA` advances 554d9521 -> df32f595.
<<<END_PAIR_A_FROM>>>

<<<PAIR_A_TO>>>
  `LAST_REVIEWED_SHA` advances 554d9521 -> df32f595.
- Reviewer gate on R25 (2026-08-10, next session): PASS. A state-file-only
  round, exactly as declared: `git diff --stat df32f595..HEAD` touches five
  paths, all under `.agent/`, and no production file, no test file and nothing
  under `docs/` appears. Range df32f595..0341928d, FOUR commits, five path
  rows. Insertions per `git log --numstat`: 214, 167, 84, 69 — each under 500,
  and the 214-line authored save is under DECISION F105 D5's 400. C1b is the
  verbatim rewrite of ONE state file and is exempt from the churn reading by
  the AGENTS.md counting rule regardless.
  Transport: `.agent/authored/f105-r25-1.md` and `.agent/last_block.md` are
  byte-identical under `cmp` (exit 0) at sha256
  `a89edbcf2a2e9b5af1bd5befc90b4044f23d4861f32b83ab9ba34543abba0e9c`, 214 lines
  each — the digest the handback declared, recomputed by the reviewer.
  Application re-measured disk to disk against the COMMITTED authored file,
  never a retype: the reviewer re-sliced all four pairs from
  `.agent/authored/f105-r25-1.md` with its own reader, which rejects a marker
  line inside any body. PAIR_A is a REWRITE and measures FROM 0x after, TO 1x.
  PAIR_B and PAIR_C are APPEND-shaped and the prefix property holds literally —
  each TO begins with its own FROM — at FROM 1x each. PAIR_D and the applied
  `.agent/plan.md` are byte-equal, 40 lines against the cap of 50. Marker
  leakage: `PAIR_A_FROM`, `PAIR_D_PLAN`, `END_PAIR` and `<<<` all count 0 in
  both targets.
  The R-0253 reading was MEASURED, not accepted on the worker's word. The C2
  commit adds exactly 84 lines and removes exactly 1. The 84 decompose as 1
  (PAIR_A TO) + 31 (PAIR_B TO-only) + 52 (PAIR_C TO-only) = 84 with nothing
  left over: each of those 84 lines occurs exactly once among the diff's ADDED
  lines, and no ADDED line comes from outside a TO slice. Strays 0, extras 0.
  The one removed line is PAIR_A's FROM. So the diff-scoped reading is exact
  and achievable, which is the finding's own claim, now independently checked.
  Gates re-run by THIS reviewer: `tests/docs/` 294 passed, the dashboard
  contract 70 passed, the canary 42 passed. NO mutation red-proof was ordered
  or run, and that is correct: nothing executable changed, so there was no
  branch to mutate (DECISION F105 D10, checklist item 5). `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  Two corrections to the record, BOTH charged to the reviewer, NEITHER held
  against R25. First: R25 called itself the §4.13 TERMINATOR. §4.13 covers the
  last round of a BRANCH; R25 is the last round of a SESSION and the branch
  continues, so its gate was never owed to construction — it is recorded here.
  R25 was right to open no repair round for it under either reading. Second:
  R-0254's fix note says to update "the two message assertions" in
  `TestDropOneNewlinePerSegmentBoundary`. There is exactly ONE, at
  `tests/orchestration/test_builder_prompt_golden.py:280`, and it matches on
  `segment boundary carries no newline to drop between segments 0 and 1` — a
  substring that SURVIVES dropping the word "builder". The fix as written would
  therefore change production bytes that no test pins. R26 anchors that
  assertion to the whole message instead, which turns the wording into
  something a mutation can prove red.
  `LAST_REVIEWED_SHA` advances df32f595 -> 0341928d.
<<<END_PAIR_A_TO>>>

C3 — fix R-0253 (own commit)
  Apply PAIR_B and PAIR_C to `docs/agents/planner_reviewer_prompt.md`.
  PAIR_B is a REWRITE (FROM and TO are disjoint): prove FROM 0x after, TO 1x.
  PAIR_C is APPEND-shaped: prove FROM exactly 1x plus the TO-only added lines.
  Then append ONE line to `.agent/live_review.md`, immediately after the line
  `  desirable in this file, so the rule must bend, not the text. OPEN.`:
    `  Landed: R-0253 — §4.9 scoped to diff-added lines and D8 item 6 added, commit <sha>.`
  with `<sha>` the short SHA of this commit. No other text.

<<<PAIR_B_FROM>>>
   the obligation there is FROM exactly 1x plus each TO-ONLY
   addition exactly 1x. The reviewer states which shape each pair is
   at authoring time, in the receipt itself.
<<<END_PAIR_B_FROM>>>

<<<PAIR_B_TO>>>
   the obligation there is FROM exactly 1x plus each TO-ONLY
   addition exactly 1x AMONG THE LINES THAT COMMIT'S DIFF ADDS
   (R-0253, F105 R24). Whole-file counting is unsatisfiable whenever
   a TO legitimately repeats a sentence the file already carries, and
   prose that echoes an earlier gate's sentence is normal and
   desirable in this file — so the rule bends, never the text. The
   measurement is `git show --numstat <commit> -- <path>` for the
   total, plus a per-line count over that diff's ADDED lines for the
   strays. The reviewer states which shape each pair is at authoring
   time, in the receipt itself.
<<<END_PAIR_B_TO>>>

<<<PAIR_C_FROM>>>
     A worker who reports an ordered mutation as green is telling the truth
     about dead code, and it costs that round a declared deviation to prove a
     reviewer mistake (finding R-0252, DECISION F105 D10).
<<<END_PAIR_C_FROM>>>

<<<PAIR_C_TO>>>
     A worker who reports an ordered mutation as green is telling the truth
     about dead code, and it costs that round a declared deviation to prove a
     reviewer mistake (finding R-0252, DECISION F105 D10).
  6. **Zero-gates read the TARGET's existing content.** A "must be 0" or an
     "exactly 1x" gate is checked against what the target FILE already
     contains, not only against the block's own bytes. An append pair whose TO
     legitimately repeats a sentence already on disk can never satisfy a
     whole-file count, so scope such counts to the commit's ADDED lines (§4.9).
     Items 1-4 read the block, item 5 reads the code the block points at, and
     this one reads the file the block writes into — three different places, so
     three separate checks (finding R-0253).
<<<END_PAIR_C_TO>>>

C4 — fix R-0254 (own commit)
  Apply PAIR_D to `packages/orchestration/pingpong_loop.py` and PAIR_E to
  `tests/orchestration/test_builder_prompt_golden.py`. Both are REWRITES:
  prove FROM 0x after and TO 1x for each, each grep SCOPED to its own file.
  The helper serves BOTH prompt composers — `pingpong_loop.py:933` (builder)
  and `pingpong_loop.py:1382` (reviewer) — which is the whole finding; the new
  message is role-neutral. PAIR_E anchors the assertion with `^` and `$` so the
  message can no longer carry an extra leading word unnoticed.
  Then append ONE line to `.agent/live_review.md`, immediately after the line
  `  in the same commit. Production code, so it needs a SPLIT round. OPEN.`:
    `  Landed: R-0254 — message is role-neutral and the assertion now anchors it, commit <sha>.`
  with `<sha>` the short SHA of this commit. No other text.

<<<PAIR_D_FROM>>>
                "builder prompt segment boundary carries no newline to drop "
<<<END_PAIR_D_FROM>>>

<<<PAIR_D_TO>>>
                "prompt segment boundary carries no newline to drop "
<<<END_PAIR_D_TO>>>

<<<PAIR_E_FROM>>>
            match="segment boundary carries no newline to drop "
                  "between segments 0 and 1",
<<<END_PAIR_E_FROM>>>

<<<PAIR_E_TO>>>
            match="^prompt segment boundary carries no newline to drop "
                  "between segments 0 and 1$",
<<<END_PAIR_E_TO>>>

C5 — plan and handoff (own commit)
  Apply PAIR_F to `.agent/plan.md` as a FULL replacement, then rewrite
  `.agent/handoff.md`.

<<<PAIR_F_PLAN>>>
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step
T001 and T002 are DONE and gated. T003's MIGRATION ORDER
(`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings —
R-0241) is COMPLETE: all six sites are migrated, each under its own golden.
R25 is GATED; `LAST_REVIEWED_SHA` is 0341928d. R26 is a SPLIT repair round: it
records the R25 gate, then fixes R-0253 (§4.9 scoped to diff-added lines, plus
a sixth D8 checklist item) and R-0254 (the shared boundary helper's
builder-only error text, plus the one assertion that must pin it).
Open findings: R-0221, R-0239, R-0246, R-0247, R-0253, R-0254 — the last two
land in R26 and are Resolved by the reviewer at the R26 gate.
No PR; one is created at CLOSURE.

## Next Steps
- ONE round wires `on_call` for the three sites lacking call evidence:
  `mission_cmd.py:362` (orchestrator), `mission_cmd.py:187` +
  `gauntlet_runner.py:505` (mission), `do_cmd.py:253` + `:2860` (plan).
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks
- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- The reviewer prompt was the worst-ordered of the six sites and 1824 of 2048
  measured renders reorder, so T004's before/after number should quote its
  cacheable-prefix gain specifically.
<<<END_PAIR_F_PLAN>>>

GATES — run every one, record the REAL exit code and the REAL output
  A transport: `sha256sum` on `.agent/authored/f105-r26-1.md` and
    `.agent/last_block.md`; `cmp` them. Digest in the handback.
  B size: `wc -l .agent/authored/f105-r26-1.md`.
  C application, each grep SCOPED to the named file:
    PAIR_A in `.agent/live_review.md`: FROM 1x (append shape).
    PAIR_B in `docs/agents/planner_reviewer_prompt.md`: FROM 0x, TO 1x.
    PAIR_C in `docs/agents/planner_reviewer_prompt.md`: FROM 1x (append shape).
    PAIR_D in `packages/orchestration/pingpong_loop.py`: FROM 0x, TO 1x.
    PAIR_E in `tests/orchestration/test_builder_prompt_golden.py`: FROM 0x,
      TO 1x.
    PAIR_F: `cmp` the applied `.agent/plan.md` against the sliced PAIR_F;
      `wc -l .agent/plan.md` must be under 50.
    For the two APPEND pairs, the TO-only ADDED-LINE count from
    `git show --numstat <commit> -- <path>` plus the stray count.
  D marker leakage: grep `PAIR_A_FROM`, `PAIR_F_PLAN`, `END_PAIR` and `<<<` in
    `.agent/live_review.md`, `.agent/plan.md`,
    `docs/agents/planner_reviewer_prompt.md`,
    `packages/orchestration/pingpong_loop.py` and
    `tests/orchestration/test_builder_prompt_golden.py` — each count must be 0.
  E the fixed suite: `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q`.
  F red-proof M1, in a DISPOSABLE `git worktree` at HEAD and nowhere else:
    put the word `builder ` back into the message (restore PAIR_D's FROM) and
    run `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q`.
    It MUST go RED. Report the exit code and the failing test NAME. Then remove
    and prune the worktree. If it comes out GREEN, do NOT edit anything to
    force a red — report the green as a declared deviation, because a green
    there means the assertion does not pin the message and the reviewer needs
    to know that, not a repaired number.
  G module regression: `python3 -m pytest tests/orchestration/ -q`.
  H contract tests: `python3 -m pytest tests/docs/ -q` and
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`. Both are
    state-file readers and this round rewrites two state files, and one of them
    reads `docs/`.
  I canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
  J hygiene: `git status --porcelain` empty; `git worktree list` the primary
    alone; `git log --numstat 0341928d..HEAD` with the `+` column per commit.
Handback:    completion report + rewrite `.agent/handoff.md` (changed-files
             table one row per path, item-status table over C1a/C1b/C2/C3/C4/C5,
             the gate table with REAL exit codes and REAL output, transport and
             pair proofs, the red-proof result, open-findings count, next
             action). Keep it under 60 lines, or carry a DECISION D15
             "Deviations, declared" line naming the real count and the mandated
             content that caused the overage. Then push. Do NOT create a PR.
──────────────────────────────────────────────────────────────
