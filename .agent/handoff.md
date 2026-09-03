# Handback — F110 Model routing by task class, round 1 — THE CLAIM, THE CANDIDATE DISCHARGE AND T001a

## Session

SESSION 1 of feature F110 · round 1 · rounds so far 1

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 1 round and 1 session it is nowhere near, so no scope report is due.
`.agent/STOP` was read from disk three times — before the first commit, before
C4, and again before C5 — and does not exist at any of those points.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103 — done) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **BASE** | `6f2230cea29af36a75fea253afc10f4dfe5a79f0` — the merge commit of pull request 232 |
| **Runde** | 1 (Session 1) — claim + candidate discharge + T001a |
| **Fortschritt** | ~10 % (T001a ✅ inventory on disk · T001b, T002, T003 open) — Schätzung |
| **Gates** | G1-G8 alle ausgeführt, echte Exit-Codes und echte Ausgaben unten. ALLE GRÜN. |
| **Offene Findings** | 279 (Mengendifferenz über 347 registrierte und 68 aufgelöste ids; unverändert durch diese Runde — keine id vergeben, keine aufgelöst) |

## Range

Review of `6f2230cea29af36a75fea253afc10f4dfe5a79f0..HEAD` (HEAD is the commit
this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| A0 Open PR Gate | done | exactly one open PR read, number 232, head `feature/f109-semantic-dedupe`, base `main`, `isDraft: false`; merged with `gh pr merge 232 --merge --delete-branch`; `main` pulled ff-only to BASE; `git diff --stat edb16a46 BASE` produced NO output; branch cut |
| C0a `aade00be` | done | block written verbatim to `.agent/authored/f110-r1.md`, 398 insertions |
| C0b `d9bc084f` | done | mirrored with `shutil.copyfile`; one sha256 for both copies (G1) |
| C1 `a7e4b099` | done | PLAN1 extracted by delimiter index from the COMMITTED authored copy and applied whole; `cmp` exit 0, 43 lines |
| C2 `d6bd1db4` | done | PAIR S applied with `str.replace(FROM, TO, 1)`; CONTEXT1 applied whole; both proved (G3, G4) |
| C3 `be8d5946` | done | DEC1 appended (1 separator byte), SLIPS1 appended (2 separator bytes), CAND1 applied whole; candidates file now EMPTY |
| C4 `94150e14` | done | `.agent/f110_inventory.md` written from measurement; all three recorded commands re-run and line counts matched (G6) |
| C5 (this commit) | done | handback rewritten per `docs/agents/handback_template.md` |

Every ordered item appears exactly once. No item was skipped and none deviated
from its ordered position.

## Commits

### aade00be F110 R1 C0a: save the round 1 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r1.md` | +398 / -0 | the reviewer's block saved verbatim; the first link of the transport chain |

### d9bc084f F110 R1 C0b: mirror the round 1 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +385 / -283 | F109 round 21's block replaced by this one; byte-identical copy of the authored file |

### a7e4b099 F110 R1 C1: the plan turns to F110 round 1
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +30 / -26 | PLAN1 applied whole; 43 lines, under the AGENTS.md 50-line rule. FIRST substantive commit of the round |

### d6bd1db4 F110 R1 C2: claim F110 in the ledger and turn the context to it
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/context.md` | +33 / -27 | CONTEXT1 applied whole |
| `docs/roadmap/STATUS.md` | +1 / -1 | PAIR S — F110's `[ ]` line rewritten as `[~]`; exactly one line touched |

### be8d5946 F110 R1 C3: discharge the four F109 closure candidates without an R-id
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/candidates.md` | +14 / -61 | CAND1 applied whole; the file now reads EMPTY, lifting the block condition |
| `.agent/decisions.md` | +37 / -0 | DECISION F110 D1 appended — candidate 1 resolved inline as a §4.7 DECISION |
| `.agent/prose_slips.md` | +17 / -1 | the eight lessons candidates 2-4 named, appended as dated lines; no id spent (amend0827 rule 2) |

### 94150e14 F110 R1 C4: T001a call-site and role inventory, measured at BASE
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/f110_inventory.md` | +321 / -0 | T001a's deliverable; sections A-G, three re-runnable commands, measured at BASE |

### C5 (this commit) F110 R1 C5: the round 1 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern). Its own numbers go to neither a round report nor this file, per the block: under self-drive there is no round-report channel, and the reviewer measures them at the next gate |

The `+` column above is the INSERTION count from `git show --numstat`
(AGENTS.md DECISION F104 D1). The cell-by-cell comparison is in G8.

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | one PR: number 232, head `feature/f109-semantic-dedupe`, base `main`, `isDraft: false` — the gate's exact expected reading |
| `gh pr merge 232 --merge --delete-branch` | MERGED. `gh pr view 232` afterwards reports `state: MERGED`, `mergedAt: 2026-09-03T06:30:55Z`, `mergeCommit.oid: 6f2230cea29af36a75fea253afc10f4dfe5a79f0`. The command also switched the local checkout to `main`, fast-forwarded it `5e18a853..6f2230ce` and deleted the local F109 branch |
| `git pull --ff-only` | `Already up to date.` |
| `git rev-parse main` | `6f2230cea29af36a75fea253afc10f4dfe5a79f0` — recorded as BASE |
| `git diff --stat edb16a46 6f2230cea29af36a75fea253afc10f4dfe5a79f0` | NO OUTPUT — the load-bearing empty diff. Every byte and count the block measured at `edb16a46` is therefore true of BASE |
| `git checkout -b feature/f110-model-routing-by-task-class` | `Switched to a new branch` |
| `git push -u origin feature/f110-model-routing-by-task-class` | run after this commit; the real result is in the completion report |

No pull request was created this round, as the block orders. No worktree was
added or removed — this round runs no destructive verification, so none was
needed. Nothing was force-pushed and no history was rewritten. No commit was
made on `main`.

## Verification

One line per gate first, then the transcripts.

| Gate | Reading |
|---|---|
| G1 TRANSPORT | GREEN — one sha256 twice, `3d24b696…e3126`. Worker-self-consistency only, which is what the reviewer stated it proves |
| G2 THE PLAN | GREEN — `cmp` exit 0, 43 lines (< 50), `^## Goal` 1, `^## Next Steps` 1 |
| G3 THE STATUS PAIR | GREEN — FROM 1 before / 0 after, TO 0 before / 1 after, `TO contains FROM: false` |
| G4 THE CONTEXT AND THE CARRIER | GREEN — both `cmp` exit 0; every ordered reading reported as a number; all eight forbidden tokens counted 0 |
| G5 THE TWO APPENDS | GREEN — decisions arithmetic exact, second reader accepts in order, negative control REJECTS; prose_slips final bytes byte-equal to the slice. See D2 on the slice's trailing newline |
| G6 THE INVENTORY | GREEN on every clause — tracked, BASE present 8×, 19 path tokens checked and 0 unresolved, all three re-runs equal their table row counts, eight `## ` headings |
| G7 THE SUITES | GREEN — 295, 30, 515, 52, 21, 16, 42, each its own invocation, run serially, every one exit 0. No count moved |
| G8 THE TREE, THE COMMITS AND THE SWEEP | GREEN — tree EMPTY before C5 was staged, `git ls-files .remedy-wt` no output, all six insertion counts agree cell by cell with the Commits table |

### G1 TRANSPORT — GREEN

    $ sha256sum .agent/authored/f110-r1.md .agent/last_block.md
    3d24b6967e29b302e001d5bf9ce067d98b744c6defecf609d4a98224f39e3126  .agent/authored/f110-r1.md
    3d24b6967e29b302e001d5bf9ce067d98b744c6defecf609d4a98224f39e3126  .agent/last_block.md
    REAL_EXIT=0

One digest, twice. The reviewer stated up front that it holds no scratch
original this round, so this is WORKER-SELF-CONSISTENCY ONLY: it proves the
mirror equals the saved copy and nothing about what the reviewer typed. That is
the §3 item 37 shape and it is declared here rather than overclaimed. Every
APPLIED slice below was extracted by delimiter index from the COMMITTED
`.agent/authored/f110-r1.md` and written by script; nothing was retyped.

Slice extraction, by delimiter index, marker lines EXCLUDED:

    PLAN1        begin line 158  end line 202   43 lines  1967 bytes
    CONTEXT1     begin line 204  end line 266   61 lines  3147 bytes
    PAIR S FROM  begin line 268  end line 270    1 line     43 bytes
    PAIR S TO    begin line 272  end line 274    1 line     43 bytes
    DEC1         begin line 276  end line 313   36 lines  2162 bytes
    SLIPS1       begin line 315  end line 331   15 lines  3383 bytes
    CAND1        begin line 333  end line 365   31 lines  1903 bytes

Each marker string occurs exactly once in the file, asserted by the extractor
before any write.

### G2 THE PLAN — GREEN

    $ cmp .remedy-wt/f110r1/PLAN1.extracted .agent/plan.md
    (no output)
    REAL_EXIT=0
    $ wc -l .agent/plan.md
    43 .agent/plan.md            (must be under 50 — it is)
    REAL_EXIT=0
    $ grep -c '^## Goal' .agent/plan.md
    1
    REAL_EXIT=0
    $ grep -c '^## Next Steps' .agent/plan.md
    1
    REAL_EXIT=0

The extracted file was re-extracted from the COMMITTED authored blob
(`git show HEAD:.agent/authored/f110-r1.md`), not from the working copy, so the
comparison runs against what landed.

### G3 THE STATUS PAIR — GREEN, and a REWRITE

FROM was counted in the real target BEFORE anything was written, and the write
was refused unless it read exactly 1:

    FROM  '- [ ] F110 — Model routing by task class'
    TO    '- [~] F110 — Model routing by task class'

    FROM count in docs/roadmap/STATUS.md BEFORE C2:  1
    TO   count in docs/roadmap/STATUS.md BEFORE C2:  0
    FROM count AFTER C2:                             0
    TO   count AFTER C2:                             1
    TO contains FROM: false

The edit is `str.replace(FROM, TO, 1)` on the file's text, per constraint 4 — no
JSON or YAML round trip, no reformatting, no reflowing. `TO contains FROM: false`
is the containment test's own output, and it is what makes the FROM-zero count a
real discriminator: an append would leave FROM at 1.

### G4 THE CONTEXT AND THE CARRIER — GREEN

    $ cmp .remedy-wt/f110r1/CONTEXT1.extracted .agent/context.md
    (no output)
    REAL_EXIT=0
    $ cmp .remedy-wt/f110r1/CAND1.extracted .agent/candidates.md
    (no output)
    REAL_EXIT=0

On the written `.agent/context.md`, each reading as a NUMBER, not as a word:

    grep -c '^## Active Branch'                       ->  1   (exit 0)
    grep -c '^## Steps'                               ->  1   (exit 0)
    count of 'feature/'                               ->  1
    first regex match of F followed by three digits   ->  F110
    'pytest' in the lowercased text                   ->  True

And each of the eight forbidden tokens, counted:

    'steps-74_1-79'                  ->  0
    'steps-91-100'                   ->  0
    'feature/steps-74'               ->  0
    'PR #33'                         ->  0
    'Steps 91-100'                   ->  0
    'allow repo_test_run'            ->  0
    'synthetic_count: 4'             ->  0
    'job=None source_apply bypass'   ->  0

### G5 THE TWO APPENDS — GREEN

(a) `.agent/decisions.md`, the RECORD — the full arithmetic amend0827 rule 5
reserves for it.

    base size at edb16a46             723474      (measured, not taken from the block:
                                                   git show edb16a46:.agent/decisions.md
                                                   is 723474 bytes and ends WITH a newline)
    separator bytes                        1
    DEC1 slice length                   2162
    base + 1 + slice                  725637
    new size                          725637
    equal                             True
    new ends with a newline           True        (the file's convention preserved)

A SECOND READER THAT COUNTS NO BYTE. The WHOLE file was split on blank-line
boundaries. N was counted BY THE SCRIPT from the slice, never taken from the
block: N = 7. The file holds 1722 such units and the LAST 7 equal DEC1's 7
paragraphs, in order:

    unit[-7] equals DEC1 paragraph 1: True (len 122 vs 122)
    unit[-6] equals DEC1 paragraph 2: True (len 652 vs 652)
    unit[-5] equals DEC1 paragraph 3: True (len 453 vs 453)
    unit[-4] equals DEC1 paragraph 4: True (len 380 vs 380)
    unit[-3] equals DEC1 paragraph 5: True (len 173 vs 173)
    unit[-2] equals DEC1 paragraph 6: True (len 221 vs 221)
    unit[-1] equals DEC1 paragraph 7: True (len 139 vs 139)
    last N file units == DEC1 paragraphs IN ORDER: True

NEGATIVE CONTROL, on a SCRATCH COPY under `.remedy-wt/` — the tracked file was
never mutated:

    first appended paragraph found at byte offset 723475
    flipped byte at offset 723495 (was '(') with XOR 0x01
    second reader accepts the mutated copy: False
    second reader REJECTS it:               True

So the second reader distinguishes the two candidates rather than accepting both.

(b) `.agent/prose_slips.md` — a BYTE-EQUALITY CHECK ONLY, which is all amend0827
rule 5 allows a `.agent/` prose file.

    file size                                            48513
    file ends with a newline                             False   (convention preserved;
                                                                  base was 45129 bytes and
                                                                  also ended without one)
    extracted SLIPS1, target newline convention           3382 bytes
    file's final 3382 bytes equal the extracted slice:   True
    the two bytes immediately before the slice:          '\n\n'  (the ordered separator)

    extracted SLIPS1, natural form with trailing newline  3383 bytes
    file's final 3383 bytes equal that form:             False

Both readings are reported because the block's own two clauses pull in opposite
directions here; see deviation D2.

### G6 THE INVENTORY — GREEN on every clause

    $ git ls-files .agent/f110_inventory.md
    .agent/f110_inventory.md
    REAL_EXIT=0

    count of the literal word BASE in the file:                    8   (at least 1)
    count of the BASE sha 6f2230cea29af36a75fea253afc10f4dfe5a79f0: 2

Every backtick-quoted PATH token resolved. The file states its own criterion —
a backtick-quoted token containing a path separator or a file extension is a
repository path, everything else in backticks is a Python symbol — so the set is
defined rather than guessed:

    backtick-quoted path tokens checked:  19
    did NOT resolve:                       0   ([])

THE DISCRIMINATOR. Each of the three recorded commands was extracted back out of
the committed file, written to `.remedy-wt/f110r1/rerun_<section>.py`, and RUN
from the repository root:

    section A   re-run exit 0   line count 5   table row count 5   EQUAL: True
        packages/orchestration/artifact_summary.py:355 summary_call_fn
        packages/orchestration/self_use_runner.py:137 run_next_self_use_item
        packages/orchestration/teacher_model.py:182 resolve_teacher_transport
        packages/orchestration/teacher_model.py:228 ask_teacher
        apps/cli/commands/do_cmd.py:155 _resolve_cli_role_configs

    section B   re-run exit 0   line count 8   table row count 8   EQUAL: True
        packages/orchestration/artifact_summary.py:356 summary_call_fn
        packages/orchestration/gauntlet_runner.py:216 _default_plan_call_fn
        packages/orchestration/gauntlet_runner.py:225 _default_move_call_fn
        packages/orchestration/intake.py:331 make_provider_call_fn
        apps/cli/commands/do_cmd.py:2955 _cmd_do_replan
        apps/cli/commands/do_cmd.py:246 _cmd_do_mission
        apps/cli/commands/mission_cmd.py:385 _orchestrator_call_fn
        apps/cli/commands/mission_cmd.py:227 _cmd_mission_plan

    section C   re-run exit 0   line count 1   table row count 1   EQUAL: True
        packages/orchestration/pingpong_loop.py:4164 _create_provider_with_cwd

The row counts were derived from the file itself by matching `^\|\s*A\d+\s*\|`,
`^\|\s*B\d+\s*\|` and `^\|\s*C\d+\s*\|`, not typed in.

Headings beginning `## ` the file actually holds, all eight:

    ## Method
    ## A — production call sites of resolve_role_config
    ## B — production call sites of make_structured_call_fn
    ## C — production call sites of create_provider
    ## D — every role in KNOWN_ROLES against sections A, B and C
    ## E — the verdict: model selection is SCATTERED, not consolidated
    ## F — the overlap with the open finding set
    ## G — the routing layers this repository already has

THE SUBSTANCE T001a PRODUCED, since a gate that only counts rows says nothing
about what was found: model selection is SCATTERED across FOUR independent
mechanisms and there is no single seam. `resolve_role_config` has five
production call sites, of which exactly ONE forwards the resolved MODEL
(`packages/orchestration/artifact_summary.py:355-356`, the `summary` role) and
one forwards only the resolved PROVIDER. `apps/cli/commands/do_cmd.py:1409`
calls the resolver and BINDS NOTHING; `:2603` binds it and writes it into
job_flow.json and nowhere else — so the raw flag, not the resolved config,
is what reaches `run_job`. `packages/orchestration/pingpong_job.py:1740-1774`
runs a SECOND precedence chain whose default is the literal `"fake"` rather than
`role_config.DEFAULT_PROVIDER`, and that module does not import role_config at
all. The `orchestrator` role is routed by a raw `orchestrator.model` config read
at two sites. And `make_structured_call_fn` hard-wires `OllamaPlanner`, so six
of its eight call sites pass no model and none of the eight picks a provider.
Four of the nine `KNOWN_ROLES` — `repair` in effect, plus `design_worker`,
`test_worker` and `final_verifier` outright — reach no provider construction
through their own name at all. That absence is recorded as a result.

### G7 THE SUITES — GREEN, EACH AS ITS OWN INVOCATION, RUN SERIALLY

Never two pytest processes alive at once. Exit codes come from
`subprocess.run(...).returncode`, never from a pipe (R-0438).

    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.53s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
    30 passed in 0.35s
    REAL_EXIT=0

    $ python3 -m pytest tests/ui_server/ -q
    515 passed in 32.71s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_test_runner.py -q
    52 passed in 5.58s
    REAL_EXIT=0

    $ python3 -m pytest tests/regression/test_resource_safety.py -q
    21 passed in 11.50s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
    16 passed in 0.30s
    REAL_EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.62s
    REAL_EXIT=0

295, 30, 515, 52, 21, 16, 42 — exactly the seven counts the reviewer measured at
`edb16a46`, none moved. THE FOUR STATE READERS WERE RUN AS FOUR, NOT AS THREE:
`tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
`tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`. The last invocation is the canary
every handback owes. This round edits no test and no production code, so a moved
count would itself have been the finding; none moved.

### G8 THE TREE, THE COMMITS AND THE SWEEP — GREEN

Read immediately before C5 was staged:

    $ git status --porcelain
    (no output — the tree is EMPTY)
    $ git ls-files .remedy-wt
    (no output)

`git ls-files .remedy-wt` returns NOTHING, so every scratch script, extracted
slice and re-run file this round wrote is untracked and cannot enter the review
subject.

Insertion counts, the `+` column ONLY (AGENTS.md DECISION F104 D1), from
`git show --numstat`, compared CELL BY CELL against the Commits table above:

    commit     path                          numstat +   table +   agree
    aade00be   .agent/authored/f110-r1.md          398       398    yes
    d9bc084f   .agent/last_block.md                385       385    yes
    a7e4b099   .agent/plan.md                       30        30    yes
    d6bd1db4   .agent/context.md                    33        33    yes
    d6bd1db4   docs/roadmap/STATUS.md                1         1    yes
    be8d5946   .agent/candidates.md                 14        14    yes
    be8d5946   .agent/decisions.md                  37        37    yes
    be8d5946   .agent/prose_slips.md                17        17    yes
    94150e14   .agent/f110_inventory.md            321       321    yes

Per-commit totals: C0a 398, C0b 385, C1 30, C2 34, C3 68, C4 321. Every one is
far under the 500-insertion cap, and C0b and C1 would in any case be exempt as
the verbatim rewrite of a single `.agent/**` state file. C5's own numbers go to
NEITHER a round report NOR this file: under self-drive there is no round-report
channel, and the reviewer measures them at the next gate.

A number that looks wrong and is not: `git commit` printed "398 insertions,
296 deletions" for C0b and "43 insertions, 39 deletions" for C1 under rewrite
detection, while `git show --numstat` — the command this gate names — reports
385/283 and 30/26. The gate's own command is the one reported above. Run with
`--no-renames` the numstat readings are identical, so rename detection is not
what moved them.

**THE STALENESS SWEEP over every file this round touched, one entry per file.**

1. `.agent/authored/f110-r1.md` — NOT stale by construction. A verbatim copy of
   the reviewer's block; nothing in it is edited regardless of what a later
   measurement shows.
2. `.agent/last_block.md` — NOT stale, same reason, same bytes.
3. `.agent/plan.md` — NOT stale. Its `## Current Step` describes exactly what
   this round did. Its first Risk bullet — "`resolve_role_config` has production
   callers in several modules while `make_structured_call_fn` is called at sites
   that pass no resolved model at all" — was written by the reviewer BEFORE the
   inventory ran, and the inventory INDEPENDENTLY CONFIRMS both halves: five
   resolver call sites across four modules, and six of eight
   `make_structured_call_fn` sites passing no model. Its second bullet says
   `R-0768` is OPEN over this seam, which G6's own reading of
   `.agent/live_review.md` confirms.
4. `docs/roadmap/STATUS.md` — NOT stale. The line reads `[~]`, F110 is in
   progress, and it is the only line touched. STATUS carries no accepted-count
   figure that a `[~]` flip could invalidate, checked at BASE; `README.md`'s
   "68 of 266 registered items accepted" is unaffected because F110 is not `[x]`,
   and `tests/docs/` (295 passed) is the suite that pins the two against each
   other.
5. `.agent/context.md` — NOT stale in every clause the worker can measure. Two
   clauses it cannot: see D3 (the ruff claim) and D4 (the `F103 — done` claim).
6. `.agent/decisions.md` — NOT stale. DECISION F110 D1's one MEASURED claim was
   independently re-run this round:
   `git log --oneline 5e18a853..edb16a46 -- docs/agents/planner_reviewer_prompt.md`
   returns NO commit, exactly as the DECISION states. The DECISION deliberately
   does not restate amend0827 rule 4's item count, so it carries no numeral that
   can go stale.
7. `.agent/prose_slips.md` — NOT stale. Eight dated historical records of
   reviewer-prose slips from F109 rounds 17-21; each is a statement about a
   past round and is true of it. Append-only, never renumbered.
8. `.agent/candidates.md` — NOT stale. It reads EMPTY and the file IS empty of
   candidates; the two paragraphs that remain point at where the F108 and F106
   entries were registered (`R-0769`, `R-0762`), both of which are still on
   `.agent/live_review.md` as stated.
9. `.agent/f110_inventory.md` — NOT stale, and it is the file most at risk, so
   it says so itself: every present-tense sentence in it is stamped
   `MEASURED AT BASE = 6f2230ce…` in its first paragraph, per §3 item 20. Every
   line number in it was resolved by AST at BASE this round, not recalled.
10. `.agent/handoff.md` — this file; written once, per the write-once rule.

NOTHING OUTSIDE THE CHANGE SET WAS EDITED. Two sentences outside it are affected
and are DECLARED, NOT REPAIRED, per constraint 7 — see D5 and D6.

## Authored-text proofs

Every applied reviewer-authored text was extracted by delimiter index from the
COMMITTED `.agent/authored/f110-r1.md` (read with
`git show HEAD:.agent/authored/f110-r1.md`, not from the working copy) and
written to its target BY SCRIPT. Nothing was retyped.

| Authored text | Proof | Expected | Read | Exit |
|---|---|---|---|---|
| the whole block | `sha256sum` of `.agent/authored/f110-r1.md` and `.agent/last_block.md` | one digest twice | `3d24b696…e3126` twice | 0 |
| PLAN1 (43 lines, 1967 bytes) | `cmp .remedy-wt/f110r1/PLAN1.extracted .agent/plan.md` | identical | identical | 0 |
| CONTEXT1 (61 lines, 3147 bytes) | `cmp .remedy-wt/f110r1/CONTEXT1.extracted .agent/context.md` | identical | identical | 0 |
| CAND1 (31 lines, 1903 bytes) | `cmp .remedy-wt/f110r1/CAND1.extracted .agent/candidates.md` | identical | identical | 0 |
| PAIR S FROM (1 line, 43 bytes) | count in `docs/roadmap/STATUS.md` before / after | 1 / 0 | 1 / 0 | — |
| PAIR S TO (1 line, 43 bytes) | count in `docs/roadmap/STATUS.md` before / after | 0 / 1 | 0 / 1 | — |
| DEC1 (36 lines, 2162 bytes) | append arithmetic + paragraph-order second reader + negative control | exact / in order / rejected | exact / in order / rejected | — |
| SLIPS1 (15 lines, 3382 bytes applied) | final-bytes byte-equality against the extracted slice | True | True | — |

## Deviations & assumptions

**D1 — NONE OF THE BLOCK'S ORDERED COMMIT SEQUENCE WAS DEPARTED FROM.** A0, C0a,
C0b, C1, C2, C3, C4, C5 ran in exactly that order, with exactly the ten paths
the change set names and nothing else. No commit was added, dropped or
reordered. This entry exists because the handback template asks for the
departure to be named HERE even when there is none.

**D2 — THE BLOCK'S TWO CLAUSES ABOUT THE SLIPS1 TRAILING NEWLINE CANNOT BOTH BE
SATISFIED BY ONE DEFINITION OF "THE SLICE", AND HERE IS THE ONE I CHOSE AND WHY.**
Constraint 3 says `.agent/prose_slips.md` "ends WITHOUT one (45129 bytes, last
byte not a newline) and still ends without one after C3" — I re-measured both
halves and both are true of the base. Constraint 5 says SLIPS1 is appended as
"two newline bytes followed by the slice". G5(b) says to report whether "the
file's final bytes equal the extracted SLIPS1 slice exactly". If "the slice" is
the marker-excluded region INCLUDING the newline that terminates its last line
(3383 bytes), then appending it makes the file end WITH a newline and constraint
3 is broken. If it is the same region in the TARGET's own newline convention
(3382 bytes), constraint 3 holds and G5(b) reads True.

I took the second reading, for three reasons: constraint 3 is the only clause
that states an outcome for the file AFTER C3 and is therefore the more specific
order; the same convention is what F109 round 21 applied to its RECORD21 append
into a file that also ends without a newline; and the same file's own last
pre-existing entry ends without one, so the appended block is now formatted
exactly like its neighbours. BOTH readings are reported in G5(b) so the reviewer
can overrule me knowingly. The whole-file slices (PLAN1, CONTEXT1, CAND1) were
applied in the OTHER direction — WITH the trailing newline — because constraint
3 states those three files end with one, and G2/G4's `cmp` clauses confirm the
choice at exit 0.

**D3 — I CANNOT VERIFY CONTEXT1'S RUFF CLAIM FROM THIS SESSION, AND APPLIED IT
VERBATIM ANYWAY.** The CONTEXT1 slice asserts "This session's reviewer CAN
execute `ruff`, measured at the F110 claim as version 0.15.17". It is a claim
about the REVIEWER's capability, not about disk. I tried to corroborate it and
`ruff --version` was REFUSED by this session's permission layer, so the worker
has no reading either way. Applied byte for byte as ordered, declared here so
the constraint is not mistaken for something the worker measured. Practical
consequence for a later round: a block that gates on ruff must be run by the
reviewer, because on this evidence the worker cannot.

**D4 — CONTEXT1'S "DEPENDS ON F103 — DONE" IS THE REVIEWER'S READING AND I DID
NOT RE-MEASURE IT.** `docs/roadmap/features/T3_F110.md` line 2 does say
"Depends on: F103", so the dependency is right; whether F103 is `[x]` in the
ledger was not part of any ordered gate and I did not check it. Named so the
reviewer can close the loop cheaply.

**D5 — A STALE OBLIGATION OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED:
THE F109 VERDICT IS NOT BOOKED INTO THE LEDGER BY THIS ROUND.** Operator
amendment amend0827-process-diet rule 1 (AGENTS.md `### handoff.md`, and
`docs/agents/self_drive_protocol.md` Phase 2) says a verdict carried in a
pushed `.agent/handoff.md` "is booked into `.agent/live_review.md` in the FIRST
COMMIT of the next round that is happening anyway". This IS that next round, and
`.agent/live_review.md` is NOT in the block's change set — the change set says
"EXACTLY these paths and nothing else". Measured: `grep -c '^Gate: F109 R21'` on
`.agent/live_review.md` returns 0, and F109's own round 21 handback declared in
its D5 that its verdict would have no on-disk gate entry. So the F109 closure
round's verdict still lives only in git history and the PR, not in the ledger.
Declared, not repaired: writing to a file outside the change set is the one
thing constraint 7 and the change set jointly forbid. If the reviewer wants it
booked, it needs a path in a later block's change set.

**D6 — A SECOND STALE SENTENCE OUTSIDE THE CHANGE SET.**
`docs/agents/planner_reviewer_prompt.md` §3 is FROZEN while a feature is open
(amend0827 rule 4) and is not in the change set. DECISION F110 D1, landed at C3,
now places a consolidation obligation on F110's closure sequence covering BOTH
features' lessons — and that file carries no record of it. This is correct as
the rules are written (the DECISION is the carrier, the checklist is frozen), but
a reader of the checklist alone will not learn that two features' lessons are due
at the next consolidation. Declared, not repaired.

**D7 — THE INVENTORY IS A MEASUREMENT, AND ITS SECTION E VERDICT AND SECTION E
CONSOLIDATION ORDER ARE THE WORKER'S OWN JUDGEMENT ON TOP OF IT.** Sections A,
B, C and D are mechanical: every row is produced by a recorded command and G6
re-runs all three. Sections E, F and G are the worker READING that measurement,
and the block asks for exactly that ("THE VERDICT T001a EXISTS TO PRODUCE").
The judgement is separable from the data on purpose — if the reviewer disagrees
with the consolidation order E.a-E.d, sections A-D stand unchanged underneath it.
Section F deliberately leaves `R-0767` and `R-0768` REGISTERED and unrepaired and
says in the file itself that F110 may not absorb R-0768 silently, because
E.a and R-0768's own expected fix are the same edit.

**D8 — THE RETAINED JOB WORKTREES ARE STILL IN `.remedy-wt`, AND SO IS THIS
ROUND'S SCRATCH.** Earlier F109 rounds retained job worktrees there; this round
created none and removed none. This round added its own scratch under
`.remedy-wt/f110r1/` — the extracted slices, the three re-run scripts and the
negative-control copy of `.agent/decisions.md`. All of it is gitignored,
`git ls-files .remedy-wt` returns nothing, and nothing was deleted by glob
(the never-delete-by-glob rule). It is left in place deliberately so the reviewer
can re-run every gate from the same inputs.

**Assumptions.** (i) `.remedy-wt/` is gitignored session scratch that PERSISTS,
which is what makes D8's decision to leave it the right one. (ii) The block's
statement that the reviewer holds no scratch original is taken at face value, so
G1 is reported as self-consistency and not as transport — the weaker claim, on
purpose. (iii) "PRODUCTION" in SPEC INVENTORY is read as the roots `packages`,
`apps` and `scripts`, which excludes `tests/` as the block requires and includes
`scripts/` because a shipped script is production; sections A-C report the same
answer with or without `scripts/`, since no call site was found there.

## Next

REVIEW ROUND 1 AND ISSUE A VERDICT, then author round 2 as T001b — the single
resolver seam, whose consolidation order is written out in section E of
`.agent/f110_inventory.md`. The next session's first action is Phase 1 rule 1 —
read `.agent/STOP` from disk — before Phase 1 rule 2, the Open PR Gate, which
this round already satisfied: no pull request is open, because none was created.
The two declared-and-unrepaired items D5 and D6 need a path in a later block's
change set if the reviewer wants either acted on.
