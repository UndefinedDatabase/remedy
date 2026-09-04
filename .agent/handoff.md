# Handoff — F262 List commands v2 (dates, sort, filter), round 10 (T002 batch 8, loop.list gains --json end to end)

## Session

SESSION 4 of feature F262 · round 10 · rounds so far 10.

Round 10 books round 9's PASS verdict (GATE9) into the ledger first,
plus one `.agent/prose_slips.md` line for a byte-fidelity gap the
round 9 reviewer found in round 9's own C4, then ships T002 batch 8:
`loop.list` gains a `--json` output matching the pattern already
shipped for job.list/queue.list/patch.list — the catalog entry gains
`_JSON_OPT` and `supports_json=True`, `_cmd_loop_list` gains a
`json_output` kwarg and a JSON branch, and the dispatch lambda passes
`args.json` through. The JSON path carries each loop's
`last_run_created_at`/`last_run_state` sourced from the exact same
`last_run_for_loop()` call the existing text "last run:" label
already uses — no new timestamp invented. `loop.list` already had
T001's `--sort/--since/--until/--limit` flags via
`_with_list_options()`'s auto-injection, so `--json` and its JSON
date fields were the only real gap. Three production files, one test
file, one commit.

## Range

Review of `9adfbc5360befe2c7e77c76454bfb31f2c5b9198..ada5cafa04b6ed24eb27425a50c79c1b7a8ea3b7`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `9adfbc5360befe2c7e77c76454bfb31f2c5b9198`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r10.md` saved verbatim (Write tool, reconstructed from the received prompt), 297 lines, sha256 `bfdaf95dbb4abdc8c6adcc94917a62ddf503eb54cdaef734e0adb09b47b9a46a` |
| C0b | done | mirrored to `.agent/last_block.md` via `cp`, sha256 identical to C0a's file |
| C1 | done | GATE9 appended to `.agent/live_review.md` byte-exact (base 2443709 + `\n` + GATE9 3112 bytes = 2446822, confirmed by direct read after write); PROSE_SLIP appended to `.agent/prose_slips.md` byte-exact (base 72104 + `\n` + slip 893 bytes = 72998, confirmed) |
| C2 | done | PAIR P1-P4 (loop_cmd.py, command_catalog.py rewrites) + PAIR P5 (test import) + TEST T1-T2 (appends) applied to four files, one commit; three PRE-EXISTING tests in the same file needed a follow-up fix — see Deviations |
| C3 | done | PLAN11 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (1928 == 1928) |
| C4 (this handback) | done | |
| py_compile (3 files) | done | exit 0 |
| pytest combined (2 files) | done | 41 passed |
| canary: tests/ui_server/ | done | 515 passed, unmoved from GATE9 baseline |
| canary: test_test_runner.py | done | 52 passed, unmoved |
| canary: test_resource_safety.py | done | 21 passed, unmoved |
| canary: test_integrity_gate.py | done | 16 passed, unmoved |
| canary: test_golden_path.py | done | 42 passed, unmoved |

## Commits

### 1302b67da6f28105843b3ecb8b165a371ea45870 F262 R10 C0a: save block verbatim to .agent/authored/f262-r10.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r10.md` | +297/-0 | transport artifact — verbatim copy of the round's step block, new file |

### f7d7dac47dc3018198e72963acb3eb20386fed89 F262 R10 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +180/-323 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### b5c152d14275ccebd7775f8eb0109e89c86bd4f0 F262 R10 C1: append GATE9 to live_review.md and one line to prose_slips.md - books round 9's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE9, `\n` + GATE9's own bytes appended to the base file |
| `.agent/prose_slips.md` | +2/-1 | byte-exact append of the round 9 byte-fidelity prose slip, `\n` + the line's own bytes appended to the base file |

### 9aaaedcb79a2d776a88825857679b61f82505c84 F262 R10 C2: loop.list gains --json end to end (T002 batch 8)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +2/-0 | PAIR P3 (rewrite: `loop.list` CommandEntry gains `args=(_JSON_OPT,)` and `supports_json=True`) |
| `apps/cli/commands/loop_cmd.py` | +26/-2 | PAIR P1 (rewrite: `json` import), PAIR P2 (rewrite: `_cmd_loop_list` gains `json_output` kwarg and JSON branch), PAIR P4 (rewrite: dispatch lambda passes `args.json`) |
| `tests/cli/test_loop_cmd.py` | +29/-3 | PAIR P5 (rewrite: `json` import), TEST T1 (append: `test_json_output_carries_last_run_created_at_and_state`), TEST T2 (append: `test_json_output_last_run_is_null_when_never_ran`), plus a follow-up fix to 3 pre-existing tests' dispatch calls — see Deviations |

### ada5cafa04b6ed24eb27425a50c79c1b7a8ea3b7 F262 R10 C3: replace plan.md with PLAN11
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +14/-16 | whole-file replace with PLAN11, byte-for-byte verified |

### (this handback commit, C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once) — numbers not tabled here; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f262-list-commands-v2` — runs
  immediately after this commit; result reported in the closing
  message, not here, since it happens after this file is committed. No
  `gh pr` command of any kind was run (forbidden this round: no PR, no
  merge, no Open PR Gate, no `main` touched).

## Verification

Preconditions, checked before C0a:
```
$ git rev-parse HEAD
9adfbc5360befe2c7e77c76454bfb31f2c5b9198
$ git branch --show-current
feature/f262-list-commands-v2
$ git status --porcelain
(empty)
$ test -f .agent/STOP
ABSENT
```
All four confirmed.

**TRANSPORT** (after C0b, re-confirmed at the end of the round):
```
$ sha256sum .agent/authored/f262-r10.md .agent/last_block.md
bfdaf95dbb4abdc8c6adcc94917a62ddf503eb54cdaef734e0adb09b47b9a46a  .agent/authored/f262-r10.md
bfdaf95dbb4abdc8c6adcc94917a62ddf503eb54cdaef734e0adb09b47b9a46a  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE9**:
```
base size immediately before C1: 2443709 bytes
GATE9 own byte length: 3112
GATE9 internal newline count: 0
base + 1 + GATE9_length = 2446822
post-C1 file real byte length = 2446822
match: True
tail matches gate9: True
preceding newline: True
```

**LEDGER APPEND, PROSE_SLIP**:
```
base size immediately before C1: 72104 bytes
slip own byte length: 893
slip internal newline count: 0
base + 1 + slip_length = 72998
post-C1 file real byte length = 72998
match: True
tail matches slip: True
preceding newline: True
```

**PRODUCTION PAIRS, READ AND COUNTED (P1-P5)**:
```
PAIR P1 (loop_cmd.py, json import): FROM count before 1
PAIR P2 (loop_cmd.py, _cmd_loop_list whole body): FROM count before 1
PAIR P3 (command_catalog.py, loop.list CommandEntry): FROM count before 1
PAIR P4 (loop_cmd.py, dispatch lambda): FROM count before 1
PAIR P5 (test_loop_cmd.py, json import): FROM count before 1
```
All five confirmed at exactly 1 occurrence in their target file before
being applied (constraint 1's re-confirmation, using each file's
CURRENT on-disk content, not the block's cited line numbers).

Full diff, `9adfbc53..9aaaedcb`, both production files:
```diff
diff --git a/apps/cli/command_catalog.py b/apps/cli/command_catalog.py
--- a/apps/cli/command_catalog.py
+++ b/apps/cli/command_catalog.py
@@ -642,6 +642,8 @@ _BASE_CATALOG: tuple[CommandEntry, ...] = (
         subcommand="list",
         description="List the loops in remedy.toml: name, trigger, action and last run.",
         action_class="read_only",
+        args=(_JSON_OPT,),
+        supports_json=True,
         related=("loop.validate", "loop.run"),
     ),
     CommandEntry(
diff --git a/apps/cli/commands/loop_cmd.py b/apps/cli/commands/loop_cmd.py
--- a/apps/cli/commands/loop_cmd.py
+++ b/apps/cli/commands/loop_cmd.py
@@ -23,6 +23,7 @@ wants: the feature requires all errors and a nonzero exit, not the first error.
 """
 from __future__ import annotations
 
+import json
 import sys
 from collections.abc import Callable
 from typing import TYPE_CHECKING, Any
@@ -77,7 +78,7 @@ def _trigger_label(spec: Any) -> str:
     return str(spec.trigger.kind)
 
 
-def _cmd_loop_list() -> None:
+def _cmd_loop_list(*, json_output: bool = False) -> None:
     """List every loop: name, trigger, action, last run. Reads, never writes."""
     from packages.orchestration.loop_spec import LoopSpecError, load_loop_specs
 
@@ -87,6 +88,29 @@ def _cmd_loop_list() -> None:
         print(f"Error: {exc}", file=sys.stderr)
         sys.exit(EXIT_ERROR)
 
+    if json_output:
+        from packages.orchestration.loop_run import last_run_for_loop
+        loops = []
+        for spec in specs:
+            job = last_run_for_loop(spec.name)
+            last_run_created_at = None
+            last_run_state = None
+            if job is not None:
+                last_run_created_at = getattr(
+                    job.created_at, "isoformat", lambda: str(job.created_at)
+                )()
+                last_run_state = getattr(job.state, "value", job.state)
+            loops.append({
+                "name": spec.name,
+                "trigger": spec.trigger.kind,
+                "is_inert": spec.is_inert,
+                "action": spec.action.kind,
+                "last_run_created_at": last_run_created_at,
+                "last_run_state": last_run_state,
+            })
+        print(json.dumps({"version": 1, "loops": loops}, sort_keys=True))
+        return
+
     if not specs:
         print("No loops defined. Add a [[loop]] table to remedy.toml.")
         return
@@ -207,7 +231,7 @@ def _cmd_loop_run(name: str, *, project: str | None = None, yes: bool = False) -
 
 
 COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
-    "loop.list": lambda args: _cmd_loop_list(),
+    "loop.list": lambda args: _cmd_loop_list(json_output=args.json),
     "loop.validate": lambda args: _cmd_loop_validate(),
     "loop.run": lambda args: _cmd_loop_run(
         args.name,
```
Confirmed by reading the full diff: exactly PAIR P1/P2/P4 in
loop_cmd.py, PAIR P3 in command_catalog.py. Nothing else touched in
either file.

```
$ python3 -m py_compile apps/cli/commands/loop_cmd.py apps/cli/command_catalog.py tests/cli/test_loop_cmd.py
(exit 0, no output)
```
Exit 0 confirmed for all three touched files, one combined invocation.

Ruff attempted per constraint 3, refused:
```
$ ruff check <files>
This command requires approval
```
Denied this session, same shape of refusal every prior round's
handback recorded — expected, not a blocker.

**PYTEST, C2's COMBINED RUN**:
```
$ python3 -m pytest tests/cli/test_loop_cmd.py tests/test_command_catalog.py -q
41 passed in 0.34s
```
(This run followed the Deviations-section fix below; the first
attempt, before that fix, read `3 failed, 38 passed in 0.43s`.)

**THE STATE READERS AND THE CANARY, run individually**:
```
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.49s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.59s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.51s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.28s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.97s
```
515/52/21/16/42 — identical to GATE9's stated baseline. Not moved, as
expected: this round's change set names no path any of these five
suites should be sensitive to.

**THE PLAN, BYTE-FOR-BYTE (constraint 7)**:
```
authored PLAN11 slice length: 1928 bytes
written .agent/plan.md length: 1928 bytes
EQUAL (bytes == bytes): True
```
Whole-file replace applied via a direct binary write of the extracted
PLAN11 slice (not the Write tool's text path), specifically to avoid
repeating R9's trailing-newline gap; the byte comparison above is the
gate itself, not a proxy (`wc -l`/diffstat were not used to establish
correctness this time, per the lesson booked in C1).

**THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked (scratch
files `.remedy-wt/gate9_line.txt` and `.remedy-wt/prose_slip_line.txt`
were written during this round to build the byte-exact ledger appends,
remain there, gitignored, untracked).

Per-commit numstat cross-check against this handback's own Commits
table:
```
$ git show --numstat 1302b67d
297  0    .agent/authored/f262-r10.md
$ git show --numstat f7d7dac4
180  323  .agent/last_block.md
$ git show --numstat b5c152d1
2    1    .agent/live_review.md
2    1    .agent/prose_slips.md
$ git show --numstat 9aaaedcb
2    0    apps/cli/command_catalog.py
26   2    apps/cli/commands/loop_cmd.py
29   3    tests/cli/test_loop_cmd.py
$ git show --numstat ada5cafa
14   16   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly. Note: at C0b commit time, `git commit`'s own printed
summary read "1 file changed, 297 insertions(+), 440 deletions(-)" (a
rename/rewrite percentage-based estimate), while `--numstat` gives the
real line-level diff (180/323) used throughout this handback's Commits
table — the same tooling substitution prior rounds' ledger entries
already documented; no committed byte is affected either way.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r10.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE9's
  content describes round 9's own verified facts.
- `.agent/prose_slips.md` — NOT stale. Append-only log; the new line
  describes round 9's own C4 byte-fidelity gap, already fixed in this
  round's own C3.
- `apps/cli/command_catalog.py` — NOT stale. Matches PAIR P3 exactly;
  full diff read and confirmed.
- `apps/cli/commands/loop_cmd.py` — NOT stale. Matches PAIR P1/P2/P4
  exactly; full diff read and confirmed.
- `tests/cli/test_loop_cmd.py` — NOT stale. Matches PAIR P5 and TEST
  T1/T2 exactly, plus the 3-test dispatch fix described in Deviations;
  py_compile and pytest both green.
- `.agent/plan.md` — NOT stale. Freshly written PLAN11 content
  accurately describes round 10's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Deviations & assumptions

1. **A follow-up fix was required in `tests/cli/test_loop_cmd.py`,
   beyond P1-P5/T1-T2 as literally specified.** PAIR P4's exact TO
   text (`"loop.list": lambda args: _cmd_loop_list(json_output=args.json)`)
   makes the dispatch lambda access `args.json` unconditionally. Three
   PRE-EXISTING tests in this same file
   (`test_a_manual_loop_lists_its_name_trigger_action_and_never`,
   `test_a_schedule_trigger_loop_is_listed_and_marked_inert`,
   `test_after_one_real_firing_the_row_shows_that_run`) call the
   file's own `_dispatch(command_id)` helper, which builds a bare
   `argparse.Namespace()` with NO attributes at all — this predates
   the round and was not flagged in the block's BACKGROUND FACTS.
   Before this round, `_cmd_loop_list()` took no arguments at all, so
   the old lambda (`lambda args: _cmd_loop_list()`) never touched
   `args`; PAIR P4 made it touch `args.json` for the first time,
   breaking those 3 tests with `AttributeError: 'Namespace' object has
   no attribute 'json'`. First pytest run (before the fix) read `3
   failed, 38 passed in 0.43s`. Fixed by changing those 3 call sites
   from `_dispatch("loop.list")` to `_dispatch_with("loop.list",
   json=False)` — using the file's own existing helper built exactly
   for this, staying inside the already-named test file, and not
   altering the P1-P5/T1-T2 pairs themselves in any way. Second run:
   `41 passed in 0.34s`. Reported here rather than silently folded in,
   per constraint 6's spirit (report the real numbers, not a
   "green"-only claim).
2. **No FROM mismatch occurred.** All five PAIR FROM strings (P1-P5)
   were re-read from each file's current on-disk content before
   applying, per constraint 1, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
3. **The C3 plan.md gate used a direct binary write plus a real
   `bytes == bytes` comparison**, not the Write tool's normal text
   path, specifically to avoid reproducing R9's own trailing-newline
   gap (the lesson just booked in this round's own C1). Result: exact
   match, 1928 authored bytes == 1928 written bytes.
4. **`git commit`'s printed stat for C0b** differed from `--numstat`
   (rename/rewrite percentage estimate vs. real line diff) — same
   substitution already declared in prior rounds' ledgers;
   `--numstat` values are used throughout this handback's Commits
   table.
5. **Ruff denied**, as anticipated by constraint 3; noted, not treated
   as a blocker.
6. **`/tmp` writes were denied by the sandbox**; scratch files for
   building the byte-exact GATE9 and PROSE_SLIP appends were written
   under the gitignored `.remedy-wt/` directory instead (consistent
   with this project's established scratch-location convention).

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, after C2, and once more before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r10.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`.agent/prose_slips.md`, `apps/cli/command_catalog.py`,
`apps/cli/commands/loop_cmd.py`, `tests/cli/test_loop_cmd.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering all four files per constraint 5.

## Next

**NEXT EXPECTED ACTION: audit remaining list commands' date coverage
before starting T003.** PLAN11's Next Steps names two open items:
change.list's event-log CREATED date question (unrelated to D1 — see
D1's Alternative section) and a broader audit of whether any other
list command still lacks a date field now that patch.list and
loop.list both have one. Reasoning: T003 (sort/filter/limit) needs a
reasonably complete set of date fields to sort by across commands, and
change.list is only ONE instance of that open question — starting the
audit first (rather than jumping straight to change.list's harder
event-log-join problem) gives round 11 a clean read on exactly how
many commands still block T003 before committing to a design for any
one of them. The execution.* trio's pre-existing `--json`-ignored
quirk stays excused per the Risks section.

**THIS IS SESSION 4, ROUND 10** — the operator may continue directly
to round 11 in this same session or start a fresh session per the
self-drive protocol's own judgment; no session/round-limit threshold
has been reached.
