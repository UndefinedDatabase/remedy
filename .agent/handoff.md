# Handback — F033 · SESSION 7 · round 25

> Written by the WORKER at the close of the round-25 delegation. The reviewer
> holds the pre-emission original of the step block and runs the other half of
> the transport comparison itself.

## Session

SESSION 7 of feature F033 · round 25 · rounds so far 25.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

BOTH triggers of the amend0827 rule 6 soft limit are now reached at once: this
is the SEVENTH session and this is the TWENTY-FIFTH round. The scope report the
rule obliges was written one round early by the session-6 reviewer, is carried
forward verbatim in substance below, and is unchanged by this round — this round
produced no feature work, so nothing in it moves the report's arithmetic.

### Scope report — required by operator amendment amend0827 rule 6

WHAT IS FINISHED. The feature's Goal & Done is met on every clause the feature
file states. Stable content-hash ids with their stability property (T001). The
command, its validation, all-or-nothing subset apply, the hunk ledger and the
write door (T002). Partial-state truth on all three surfaces — viewer, task node
and report line (T003, R-0738). And the rejection-to-repair loop, complete end to
end as of round 24: an operator's rejection is recorded on the job, selected back
out by task, rebuilt into a ledger, rendered as repair findings with the reason
held byte for byte, and composed into the next builder prompt. THE FEATURE'S
FUNCTIONAL SCOPE CLOSED AT ROUND 24 and this round did not touch it: round 25
altered one docstring paragraph and no executable statement, proved by AST.

WHAT IS MISSING, and none of it is feature work:
  1. `docs/` owes an operator-facing description of `remedy patch approve-hunks`.
     No round has been allowed a `docs/` path in this whole feature, so this is
     a first — one round, carrying the `tests/docs/` gate the docs-round rule
     adds.
  2. The integration-gate round, per docs/agents/integration_gate.md.
  3. The closure sequence and its pull request, which by precedent on this
     branch is two rounds.
  4. R-0745 (Low, OPEN) — the write door's import guard reads DIRECT imports
     only, and the door's transitive closure now reaches `subprocess` through
     `evidence_index`.

THE PROPOSAL, unchanged and still a proposal only: split R-0745 onto its own
STATUS line and let F033 close on the Acceptance it has met, carrying R-0745 as
the documented Low risk the closure protocol's precondition 1 admits. The
alternative — keep R-0745 inside F033 and expect an eighth session — is recorded
because rule 6 asks for one. NEITHER IS EXECUTED ON A WORKER'S OR REVIEWER'S OWN
AUTHORITY. `.agent/plan.md` as rewritten this round takes the recommended
reading and states it as a Risk, so a reversal costs one plan rewrite.

## Range

`d81acca5`..`9e84514a` on branch `feature/f033-hunk-approval-v2`, pushed.
Six commits, C0a through C5.

## Commits

### ea71aeb4 docs(f033): save the round 25 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r25.md | +301/-0 | C0a — the block saved verbatim, copied with `shutil.copyfile`, never retyped |

### 2956aede docs(f033): mirror the round 25 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +266/-282 | C0b — the same bytes mirrored, copied from the saved file |

### 620a0343 docs(f033): rewrite the plan for round 25
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +20/-19 | C1 — full rewrite from slice PLAN25 |

### 8c5ecfdb docs(f033): book the round 24 verdict, resolve R-0748 and register R-0749
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6/-0 | C2 — slice RECORD25 appended: the R24 `Gate:`, the `Done: R-0748` and the R-0749 registration |

### 18428f07 docs(f033): record the round 24 untracked artifact sweep slip
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +2/-0 | C3 — slice SLIPS25 appended |

### 9e84514a fix(f033): state the wired job level hop in the compose_builder_prompt docstring
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_loop.py | +9/-10 | C4 — SPEC A, pair PAIR-ROUTE applied to the `compose_builder_prompt` docstring; no executable statement touched |
| .agent/live_review.md | +2/-0 | C4 — the single `Landed: R-0749` line, in the SAME commit as the repair |

### C5 — the handback commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C5 — this file; a handoff cannot table the commit that writes it |

Per-commit insertions C0a..C4: 301, 266, 20, 6, 2, 11. Every one under 500.

## External actions

`git push` on `feature/f033-hunk-approval-v2` — succeeded. No PR created, no PR
edited, no merge, no worktree add or remove. This round ordered no disposable
worktree because it mutates no executable code (Constraint 8).

## Verification — G1 through G7, at C4 `9e84514a`

Every exit code below is a REAL one, taken from
`bash -c '<cmd>; echo "REAL_EXIT=$?"'` with no pipe.

### G1 TRANSPORT — REAL_EXIT=0

    .agent/authored/f033-r25.md  bytes 25113  sha256 88dd0980bf9486954e14eee00fbc64851b1e424e24f92a5086448cb8833323ab
    .agent/last_block.md         bytes 25113  sha256 88dd0980bf9486954e14eee00fbc64851b1e424e24f92a5086448cb8833323ab
    THE ONE DIGEST COMPARISON, authored == last_block: True

Both digests equal the sha256 the delegation declared for the pre-emission
original. The reviewer holds that original and runs the other half.

### G2 THE PROSE FILES — REAL_EXIT=0

    plan.md bytes 2329 | PLAN25 slice 2328 + trailing nl
    BYTE-EQUAL to PLAN25: True
    lines 43 | under 50: True
    holds '## Goal': True
    holds 'Steps': True

    prose_slips MEASURED base bytes: 31337     (measured at C1 620a0343, not taken from the block)
    one newline separator          : 1
    SLIPS25 append unit bytes      : 597       (slice 596 + nl)
    sum                            : 31935
    committed bytes                : 31935
    RECONSTRUCTS, base PREFIX, unit SUFFIX: True
    unchanged at C4: True

### G3 THE RECORD APPEND, at C2 — REAL_EXIT=0

    MEASURED base bytes      : 1602790        (measured at C1 620a0343)
    one newline separator    : 1
    RECORD25 append unit     : 8215
    sum                      : 1611006
    committed bytes          : 1611006
    ARITHMETIC RECONSTRUCTS  : True

    base is a byte PREFIX    : True
    unit is an exact SUFFIX  : True
    the joint is exactly one newline: True
    tail after base+1 == unit: True

    N COUNTED from the slice : 3
    unit 0 len 4333 == slice para 0 len 4333 : True | head: Gate: F033 R24 — THE JOB-LEVEL CALLER SUPP
    unit 1 len 1437 == slice para 1 len 1437 : True | head: Done: R-0748 — THE FALSE CLAUSE IS GONE FR
    unit 2 len 2440 == slice para 2 len 2440 : True | head: - R-0749 — Low, THE CLAIM R-0747 AND R-074
    ALL N UNITS EQUAL IN ORDER: True

    FIRST appended paragraph span: [ 1602791 , 1607124 )
    flip offset                  : 1604957
    offset lies INSIDE that span : True
    byte before flip / after flip: b' ' -> b'\x00'
    reader A accepts unflipped   : True
    reader B accepts unflipped   : True
    reader A REJECTS flipped     : True
    reader B REJECTS flipped     : True

Reader A is the arithmetic + prefix + exact-suffix reader; reader B compares the
file's last N blank-line units against the slice's paragraphs in order. They are
independent and both reject the flipped bytes.

### G4 THE LEDGER — REAL_EXIT=0

    base d81acca5 | registered lines 309 distinct 309 | Done lines 53 distinct 51 | Landed 20 | Landed R-0749 0 | Landed R-0748 1 | Gate F033 R24 0 | OPEN 258
    C2   8c5ecfdb | registered lines 310 distinct 310 | Done lines 54 distinct 52 | Landed 20 | Landed R-0749 0 | Landed R-0748 1 | Gate F033 R24 1 | OPEN 258
    C4   9e84514a | registered lines 310 distinct 310 | Done lines 54 distinct 52 | Landed 21 | Landed R-0749 1 | Landed R-0748 1 | Gate F033 R24 1 | OPEN 258

    ADDED registered id at C2 : ['R-0749']
    ADDED resolved id at C2   : ['R-0748']
    Landed R-0748 still standing: True

The open set is 258 at all three revisions, which is what the block predicted:
the registration of R-0749 and the resolution of R-0748 both land in C2, so the
+1 and the -1 cancel inside one commit and the intermediate value at C2 is 258
rather than 259. Registered distinct 309 -> 310; `Done:` 53 lines over 51
distinct -> 54 over 52; `Landed:` 20 -> 21; `Gate: F033 R24 — ` 0 before C2 and
exactly 1 after.

### G5 THE REPAIR IS A DOCSTRING AND NOTHING ELSE, at C4

(a) `python3 -m ruff check packages/orchestration/pingpong_loop.py` — REAL_EXIT=0

    All checks passed!

(b) and (c) — REAL_EXIT=0

    PAIRROUTE-FROM occurrences: 0 (required 0)
    PAIRROUTE-TO   occurrences: 1 (required exactly 1)

    docstrings blanked, base: 82 | C4: 82
    ast.dump length base: 477810
    ast.dump length C4  : 477810
    DUMPS EQUAL         : True

    red control, literal renamed in 1 place(s)
    CONTROL dump equals base (must be False): False

The red control renames the `builder_directive` segment literal and the reading
flips to False, so the AST gate discriminates rather than passing on everything.

SPEC A1 containment, re-measured here: `TO contains FROM: False`, so it is a
REWRITE. FROM occurred exactly ONCE in the target before the edit (1259 slice
bytes, 1260 in the file with its terminating newline, 17 lines) and 0 times
after; TO occurs exactly 1 time after. Target 198871 -> 198786 bytes.

### G6 THE CLAIM IS GONE, SWEPT SEMANTICALLY, at C4

The command form, run once per string over TRACKED content:

    git grep -c -F "<string>" -- packages apps tests docs

    "no round has wired"            -> no match, REAL_EXIT=1, count 0
    "ONE HOP STILL MISSING"         -> no match, REAL_EXIT=1, count 0
    "this segment never registers"  -> no match, REAL_EXIT=1, count 0
    "persists no decision"          -> no match, REAL_EXIT=1, count 0   (R-0748's own predicate, re-measured at the commit that resolves it)

POSITIVE CONTROL, so the sweep is not vacuous — the same command at the base
commit finds all three of the retired strings, each once, in the repaired file:

    git grep -c -F "no round has wired" d81acca5 -- packages apps tests docs
      d81acca5:packages/orchestration/pingpong_loop.py:1        REAL_EXIT=0
    git grep -c -F "ONE HOP STILL MISSING" d81acca5 -- packages apps tests docs
      d81acca5:packages/orchestration/pingpong_loop.py:1
    git grep -c -F "this segment never registers" d81acca5 -- packages apps tests docs
      d81acca5:packages/orchestration/pingpong_loop.py:1        REAL_EXIT=0

THE READING HALF. `git grep -n -F "hunk_ledger" -- packages apps` (REAL_EXIT=0)
returns 63 hits across 7 files. Every hit that is a COMMENT or DOCSTRING rather
than code, read and reported, with whether it asserts the hop is unwired:

- `hunk_decision_record.py:28,31,36` — the module docstring's dependency and
  routing paragraphs; they name `hunk_ledger` as a MODULE a reader should go to
  for the record's shape. Does NOT assert the hop is unwired.
- `hunk_decision_record.py:45` — states that
  `load_latest_hunk_ledger_from_metadata` is the one TOTAL reader and answers an
  empty ledger for unreadable input. Does NOT assert the hop is unwired; it
  describes the reader that the now-wired job-level caller uses.
- `hunk_decision_record.py:68` — the Public API list line for that reader.
  Does NOT assert the hop is unwired.
- `hunk_decision_record.py:109,111` — the comment on `_LEDGER_ROWS_KEY`,
  explaining why the key name is re-stated rather than imported. Does NOT assert
  the hop is unwired.
- `hunk_decision_record.py:143` — `_known_hunk_ids`' docstring, on the order
  `build_hunk_ledger` walks. Does NOT assert the hop is unwired.
- `hunk_decision_record.py:275` — `_parsed_decision_stamp`'s docstring, on
  keeping the structural and parse guards separate. Does NOT assert it.
- `hunk_decision_record.py:308,318` — `load_latest_hunk_ledger_from_metadata`'s
  docstring, on the rebuild being `import_hunk_ledger`'s and on totality. Does
  NOT assert it.
- `hunk_ledger.py:58,59,60,95` — Public API list lines and the comment on the
  four exported keys. Do NOT assert it.
- `hunk_ledger.py:315,324,325,337` — `import_hunk_ledger`'s docstring, on the
  key rename, the round trip and the two separate guards. Does NOT assert it;
  it says the rebuild is "what makes a decision already recorded on a job usable
  by the renderer", which is now true end to end.
- `hunk_repair_findings.py:6` — the module docstring's WHY paragraph, pointing
  at where the verbatim rule comes from. Does NOT assert it.
- `hunk_repair_findings.py:22,24` — SEE THE FLAG BELOW. The DELIBERATE ABSENCE
  paragraph these two hits sit inside ends, at lines 25-26, with "and has NO
  CALLER YET — the round that wires its output into the next builder prompt
  follows this one." That IS an assertion that a hop is unwired, and it is FALSE
  at C4.
- `hunk_repair_findings.py:33` — the totality rule, cross-referencing siblings.
  Does NOT assert it.
- `hunk_repair_findings.py:55` — the naming convention comment. Does NOT.
- `hunk_repair_findings.py:70,72` — `_total_text`'s docstring, on re-stating a
  private guard. Does NOT.
- `hunk_repair_findings.py:122` — the VERBATIM LINE comment. Does NOT.
- `pingpong_loop.py:884,885` — `compose_builder_prompt`'s parameter paragraph,
  on what `hunk_ledger` is and why it is typed `Any`. Does NOT assert it.
- `pingpong_loop.py:897,904,908` — the REPAIRED paragraph. It now states the
  route as it is and names `d81acca5` as the commit its reading was taken at.
  Does NOT assert it; it asserts the opposite, correctly.
- `pingpong_loop.py:972-985` (the comment block above and below line 977) — why
  the render happens once and why the emptiness test is the one guard. Does NOT.
- `pingpong_loop.py:1029` — `build_builder_prompt`'s docstring, that
  `hunk_ledger` is forwarded unchanged. Does NOT.
- `pingpong_loop.py:2618` — `run_pingpong`'s docstring, that the loop forwards
  the value unchanged and "a caller holding the job is what turns a stored
  decision into this argument". Does NOT assert the hop is unwired — it names
  the caller's role without claiming the caller is absent.
- `pingpong_job.py:1603,1622` — `_recorded_hunk_ledger_for_task`'s docstring,
  which opens "THIS IS THE LAST HOP of F033's rejected-hunks route". Does NOT
  assert it; it is the wiring itself, documented.

NOTE, for completeness rather than as a defect: the R-0749 registration and the
`Done: R-0748` paragraph written this round QUOTE the three retired strings, but
they live in `.agent/live_review.md`, which is outside the four swept trees. The
sweep's scope and the record's append-only rule do not collide.

### G7 SUITES AND STRUCTURE, at C4

Serially, in the primary checkout:

    python3 -m pytest tests/orchestration/test_builder_prompt_hunk_rejections.py -q   16 passed   REAL_EXIT=0
    python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q            21 passed   REAL_EXIT=0
    python3 -m pytest tests/orchestration/test_pingpong.py -q                         34 passed   REAL_EXIT=0
    python3 -m pytest tests/cli/test_golden_path.py -q            (canary)            42 passed   REAL_EXIT=0

    git status --porcelain        -> EMPTY, REAL_EXIT=0

    per-commit insertions C0a..C4 -> 301, 266, 20, 6, 2, 11; every one under 500

    git diff --name-only d81acca5..9e84514a   REAL_EXIT=0
      .agent/authored/f033-r25.md
      .agent/last_block.md
      .agent/live_review.md
      .agent/plan.md
      .agent/prose_slips.md
      packages/orchestration/pingpong_loop.py

    Path set == change set minus `.agent/handoff.md`, in BOTH directions: 6 paths
    measured, 6 paths declared, no path in one and not the other.

## Authored-text proofs

Applied this round, all lifted from the COMMITTED `.agent/authored/f033-r25.md`
by marker extraction rather than retyped, so each is byte-identical to the block
by construction:

| Text | Bytes | sha256 | Result |
|------|-------|--------|--------|
| PLAN25 | 2328 | bb2145f08957f8388e51c9aad44fa7662ffd8dc569ca980e091dd21b93233f1a | `.agent/plan.md` == slice + one newline, True |
| RECORD25 | 8214 | 6f1071442c8c215faf73aa8866e180a13f06d71f1362efd708dbf792eee41354 | exact SUFFIX of `.agent/live_review.md` at C2, True |
| SLIPS25 | 596 | ae9d411373cf677e1f2e9944abf43682f10aeeaaceb6c5dba688e47e5158c460 | exact SUFFIX of `.agent/prose_slips.md` at C3, True |
| PAIRROUTE-FROM | 1259 | 8c49ef10555033cc241380b75f4784cb24445fcd09134fcc8c6f14ab1db1735c | 1 occurrence before C4, 0 after |
| PAIRROUTE-TO | 1174 | 52f79e69e2270876f77423a8deb880fd5d3454cf7923df91991c622664d81544 | 0 occurrences before C4, exactly 1 after |
| `Landed: R-0749` line | 162 | — | lifted from the block's indented code span, 4-space indent stripped; marker asserted unique |

Transport: `.agent/authored/f033-r25.md` and `.agent/last_block.md` both carry
sha256 `88dd0980…3323ab` at 25113 bytes, equal to each other and equal to the
digest the delegation declared. `.remedy-wt/f033-r25-block.md` was readable, so
nothing was retyped.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f033-r25.md` | done | `shutil.copyfile`; digest matches the declared original |
| C0b mirror the same bytes into `.agent/last_block.md` | done | copied from the saved file, not from the source |
| C1 rewrite `.agent/plan.md` from PLAN25 | done | byte-equal, 43 lines |
| C2 append RECORD25 to `.agent/live_review.md` | done | G3 green, N=3 |
| C3 append SLIPS25 to `.agent/prose_slips.md` | done | reconstructs 31337 + 1 + 597 = 31935 |
| C4 SPEC A repair + PAIR-ROUTE + the `Landed: R-0749` line | done | one commit, both paths |
| SPEC A1 apply PAIR-ROUTE, report both counts | done | FROM 0, TO 1 |
| SPEC A2 change nothing else in that file | done | AST dumps equal at 477810 bytes each |
| SPEC A3 the single `Landed:` line, no `Done:` paragraph | done | no `Done:` written by this worker |
| C5 rewrite `.agent/handoff.md` | done | this file |
| G1 TRANSPORT | done | REAL_EXIT=0 |
| G2 THE PROSE FILES | done | REAL_EXIT=0 |
| G3 THE RECORD APPEND | done | REAL_EXIT=0 |
| G4 THE LEDGER | done | REAL_EXIT=0 |
| G5 DOCSTRING AND NOTHING ELSE | done | REAL_EXIT=0 both halves |
| G6 THE CLAIM IS GONE | done | four counts 0; the READING half surfaced one stale claim, flagged below |
| G7 SUITES AND STRUCTURE | done | four suites REAL_EXIT=0, tree clean, path set equal |
| R-0749 | landed | the repair is in, its `Landed:` line is in |
| Push | done | branch pushed, no PR |

## Deviations & assumptions

1. NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. Six commits, C0a, C0b,
   C1, C2, C3, C4, C5 — exactly the Bundle, in order, with C4 carrying both of
   its ordered paths in one commit. No extra commit, none dropped, none
   reordered. No path outside the change set was written.

2. FLAG, NOT A REPAIR — A SECOND STALE "IT IS NOT WIRED YET" CLAIM, FOUND BY
   G6's READING HALF AND LEFT IN PLACE ON PURPOSE.
   `packages/orchestration/hunk_repair_findings.py`, lines 20-26, ends its
   DELIBERATE ABSENCE paragraph with: "and has NO CALLER YET — the round that
   wires its output into the next builder prompt follows this one." That is
   FALSE at C4 and has been false since round 21:
   `packages/orchestration/pingpong_loop.py:34` imports
   `render_rejection_findings` and line 977 calls it, measured with
   `git grep -n "hunk_repair_findings\|render_rejection_findings" -- packages apps`
   at REAL_EXIT=0.
   WHY IT WAS NOT FIXED: `hunk_repair_findings.py` is NOT in this round's change
   set, Constraint 5 forbids touching any path outside it, and the delegation
   forbids repairing on the worker's own initiative. It is reported instead.
   WHY IT MATTERS BEYOND ITSELF: it is the SAME defect class as R-0749 — a
   paragraph that was true when written and was falsified by a later round that
   never swept the prose naming the hop it completed. R-0749's resolution
   predicate is worded over "the job-level `hunk_ledger` hop", and this claim is
   about a DIFFERENT hop (the loop-level one, `hunk_repair_findings` into
   `compose_builder_prompt`), so on a literal reading the predicate still holds
   and this is a fourth instance rather than a miss. The reviewer owns that call;
   the worker's job was to read and report, which is what G6's reading half asked
   for. If it is to be a finding, the fix is one paragraph in one file.

3. `.agent/context.md` and `.agent/decisions.md` were NOT updated. Neither is in
   the change set, and this round changed no scope, no assumption, no constraint
   and made no technical decision — it applied a reviewer-authored docstring
   repair and three reviewer-authored prose slices. Declared here because the
   Commit Gate asks the question at every commit.

4. `docs/` was NOT touched, as Constraint 5 orders. This round changed no built
   behaviour — one docstring paragraph moved and the AST is byte-identical — so
   the AGENTS.md documentation triggers do not fire on it. The `docs/` guide for
   `remedy patch approve-hunks` remains the NEXT round's work.

5. The sandbox denials named in Constraint 6 held as described. Every proof was
   run as `python3 -B <path>` over a script under `.remedy-wt/`, and every REAL
   exit code came from `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with no pipe. One
   `Bash` call was refused outright by the harness before any of that — a
   compound `ls ... 2>&1; echo ...; ls ...; git log ...` line — and was replaced
   by separate simple calls. Nothing was worked around; the denial was respected.

6. Constraint 7 was applied throughout: every absence reading of this round was
   taken with `git grep` over TRACKED content, never with a plain recursive grep.
   That is the round-24 lesson recorded in SLIPS25, and it is also why the
   positive control at `d81acca5` was added — a tracked-content sweep that finds
   nothing proves nothing until it is shown to reach the file.

7. Constraint 2's warning was heeded: the bases for both appends were
   RE-MEASURED at the commit they were appended at (`.agent/live_review.md`
   1602790 and `.agent/prose_slips.md` 31337, both at C1 `620a0343`), not taken
   from the block. Both matched the block's numbers, so there is no discrepancy
   to declare — only the measurement.

## Next

The `docs/` round: write the operator-facing guide for
`remedy patch approve-hunks` under `docs/guides/`, register it in the
`docs/README.md` index in the SAME commit, and gate it with
`python3 -m pytest tests/docs/ -q` beside the canary. Before planning it, the
reviewer should settle deviation 2 above — whether the stale "NO CALLER YET"
paragraph in `packages/orchestration/hunk_repair_findings.py` earns an id or is
folded into the docs round as a one-paragraph repair.
