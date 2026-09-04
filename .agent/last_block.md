═══════════════════════════════════════════════════════════════
── STEP CLOSURE PRECONDITION 3 / ROUND 16 — F114 Cost preview per command ──

FEATURE F114 — Cost preview per command (Tier 3) — SESSION 4, ROUND 16

Goal
  Book round 15's PASS verdict into the ledger (RECORD15 — the
  session-ending handback itself, already independently reviewed and
  reproduced by the reviewer at this session's start), then run closure
  precondition 3 (`remedy integrity check --json`) for the first time
  this feature. No code changes this round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r16.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD15 to .agent/live_review.md (append) and PLAN16 to
      .agent/plan.md (whole-file replacement)
  C2  run closure precondition 3 (read-only, writes no file) and
      rewrite .agent/handoff.md — the handback, reporting the exact
      reading

Change set — EXACTLY these paths and nothing else
  .agent/authored/f114-r16.md (new, C0a) — .agent/last_block.md (C0b) —
  .agent/live_review.md (C1) — .agent/plan.md (C1) — .agent/handoff.md
  (C2)

Constraints
  1. Every authored slice (RECORD15, PLAN16) is applied BYTE FOR BYTE:
     extract it by delimiter index from the COMMITTED
     .agent/authored/f114-r16.md — marker lines EXCLUDED — and write it
     with a script, never by retyping. If a slice looks wrong, apply it
     as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD15 appends to .agent/live_review.md as EXACTLY ONE newline
     byte followed by the slice. PLAN16 REPLACES .agent/plan.md whole.
  4. NEWLINE CONVENTION: RECORD15 and PLAN16 both carry NO trailing
     newline of their own.
  5. Read .agent/STOP from disk before the first commit and again
     before C2. If it exists, finish the commit in hand, write the
     handback, and stop.
  6. Precondition 3: first try `remedy integrity check --json` directly.
     If the sandbox denies it (literal text "This command requires
     approval"), run `python3 -m apps.cli.grouped integrity check
     --json` instead — this is the EXACT module `pyproject.toml`'s
     `[project.scripts]` maps the `remedy` console script to
     (`remedy = "apps.cli.grouped:main"`), so it is the same code path,
     not an approximation. Report the refusal text (if any) and the
     literal JSON reading either way.
  7. Precondition 3 is CONFIRMED only if the JSON reads `"passed":
     true`, `"fail_count": 0`, and `high_blockers_open` reports no open
     Blocker/High finding. If it reads anything else, do NOT declare
     precondition 3 confirmed — report the exact JSON verbatim in the
     handback instead and stop there; do not attempt to fix or silence
     it yourself (that would be undeclared scope). This is a real
     branch: say plainly which case you hit.
  8. This round does not touch packages/, apps/, or tests/ — only
     .agent/** changes. It does not touch docs/roadmap/**, so it does
     NOT need to gate tests/docs/ or test_roadmap_index.py this time.
  9. Self-review loop before every commit (git diff --stat, git diff).
     Push after C2. No pull request, no merge this round.

Done when — the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r16.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND (RECORD15). Base size of .agent/live_review.md
     immediately BEFORE C1: report byte length and trailing-newline
     status (expect 2402882, no trailing newline). RECORD15 has ZERO
     internal newlines — report its own byte length (expect 2613).
     Report base + 1 + 2613 and whether it equals the post-C1 file's
     byte length (expect 2405496). Second reader: post-C1 file's bytes
     from `base` to end equal exactly "\n" + RECORD15. Negative control
     in a scratch copy ONLY: flip one byte inside RECORD15's own text,
     confirm the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN16 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0 (if `cmp`
         is denied by the sandbox, substitute a Python byte-equality
         read of both files and say so)
       wc -l .agent/plan.md                      -> report; expect 32
         (PLAN16 has 33 logical lines but no trailing newline), must be
         under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 PRECONDITION 3. Per constraints 6-7 above: report the exact command
     that ran (and the refusal text if the first attempt was denied),
     then the literal JSON output, then state plainly whether
     precondition 3 is CONFIRMED or NOT per constraint 7's test.
  G5 THE FOUR STATE READERS, EACH AS ITS OWN INVOCATION, RUN SERIALLY
     (this round rewrites .agent/ state, per the standing
     .agent/context.md constraint), PLUS THE CANARY:
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each count. Expect 515 / 52 / 21 / 16 / 42 respectively,
     matching every prior round's baseline this session — if any count
     differs, report the real number and do not paper over it.
  G6 THE TREE, THE COMMITS AND THE SWEEP.
       git status --porcelain            -> empty, checked immediately
         before C2 staged
       git diff --stat <this round's own starting HEAD>..HEAD --
         packages/ apps/ tests/  -> empty
     Per-commit numstat cross-check (`git show --numstat`) for C0a,
     C0b, and C1 (two paths) against this handback's own Commits table
     — report every cell and confirm it matches. Staleness sweep: one
     entry per file this round touched, plus a statement that no NEW
     stale sentence was found outside the change set this round.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
There are two: RECORD15 and PLAN16.

<<<BEGIN RECORD15>>>
Gate: F114 R15 — the round 15 entry, the SESSION-ENDING handback itself (books round 14's PASS verdict, closes SESSION 3), no code changes. VERDICT PASS, over the range `1d0627fa50c63062af56987bd2f369241ad25d80..90b2960dc4fe0e4a1920bf7519217f250b25e134` (commits C0a `f45af9cf5f99fb384ddae53599eaa2ada0cc2ea2`, C0b `ee0c1e4c3b957d3b87571e9387f56d3e7db5a5b7`, C1 `ef66e50246d7f9bb0a8f78ca8db7bff56a5ab5b2` — three real content commits — plus handback commit `90b2960dc4fe0e4a1920bf7519217f250b25e134`), independently re-verified by the reviewer at session start. TRANSPORT HELD: `sha256sum .agent/authored/f114-r15.md .agent/last_block.md` both print `dbb981bacbf69b70f2396efefaa092ff3e4c4c1767aa6b01b4f444bda27cfaa7`, reproduced directly. G2 THE LEDGER APPEND (RECORD14) HELD BYTE-EXACT: base 2398958 bytes (no trailing newline), RECORD14 measured 3923 bytes with zero internal newlines, base + 1 + 3923 = 2402882 exactly matching the post-C1 file; the appended tail equals `\n` + RECORD14 byte for byte, a one-byte-flipped negative control was correctly rejected. G3 THE PLAN HELD BYTE-EXACT: PLAN15 extracted from the committed authored file compares equal to `.agent/plan.md` (37 lines by `wc -l`; `## Goal`/`## Next Steps` each exactly once). G4 THE TREE AND THE SWEEP HELD: `git status --porcelain` and `git diff --stat 1d0627fa..90b2960d -- packages/ apps/ tests/` are both empty, reproduced independently; every commit's numstat cells match the handback's own Commits table cell for cell (C0a 141/0 `.agent/authored/f114-r15.md`, C0b 90/171 `.agent/last_block.md`, C1 2/1 `.agent/live_review.md` and 18/21 `.agent/plan.md`). ONE DEVIATION WAS DECLARED BY THE ROUND (`cmp` denied by the sandbox, a Python byte-equality read substituted to the same effect) — not a defect on disk. Open findings recount confirmed the round's own figure unchanged: 354 registered R-ids minus 76 `Done:` lines equals 278 open, matching the handback exactly. Closure precondition status is unchanged by this round and carried forward accurately: preconditions 4 (Built State, round 14) and 6 (self-use, round 13) SATISFIED; precondition 1 (every step PASS) and precondition 2 (integration gate clean, round 11) HOLD; precondition 5 (clean tree, pushed) HOLDS, `git fetch` plus `git rev-parse HEAD origin/feature/f114-cost-preview-per-command` both equal `90b2960dc4fe0e4a1920bf7519217f250b25e134`; precondition 3 (`remedy integrity check --json`) remains NOT YET RUN as of this record, the very next item this session takes up. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head.
<<<END RECORD15>>>

<<<BEGIN PLAN16>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 16 opens SESSION 4. It books round 15's PASS verdict (RECORD15 —
the session-ending handback itself, reviewed and reproduced
independently at session start) into the ledger, then runs closure
precondition 3 (`remedy integrity check --json`) for the first time
this feature. No code changes.

## Next Steps

- The closure commit itself: evidence job, fresh review zip, STATUS
  line, README sync, `scripts/self_use_queue.json`'s `consumed_by=F114`
  edit, the PR (STATUS_closure_protocol.md algorithm) — its own round
  or two, per F258's own precedent (rounds 9-11).
- Preconditions 1, 2, 4, 5 and 6 hold; precondition 3 is confirmed this
  round (see Done when).

## Risks

- None new this round. The closure commit remains the highest-stakes
  remaining work.
<<<END PLAN16>>>

──────────────────────────────────────────────────────────────
═══════════════════════════════════════════════════════════════
