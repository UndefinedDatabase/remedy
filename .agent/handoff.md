# Handoff — F262 List commands v2 (dates, sort, filter), round 9 (T002 batch 7, patch.list gains created_at end to end)

## Session

SESSION 4 of feature F262 · round 9 · rounds so far 9.

Round 9 books round 8's PASS verdict (GATE8) into the ledger first,
then ships T002 batch 7: `created_at` is added to every patch-intent
explanation, stamped once at intent-derivation time in both creation
flows (`do_run.py`, `apps/cli/commands/job.py`), surfaced through
`list_patch_intents()` and a new CREATED column in
`format_intent_list()` ahead of DECIDED. `patch.list --json` needed no
separate change — it prints `list_patch_intents()`'s own dicts
verbatim, so the key flows through automatically. DECISION F262 D1
records why the value is sourced from the stored explanation dict
rather than the run-event log, and corrects a stale R8 plan.md claim
(job.py:623 DOES emit `patch_intent_created`; only do_run.py's own
`do_run_patch_intent_created` is dead — neither is what
`list_patch_intents()` reads). Three production files, three test
files, one commit.

## Range

Review of `74cfbd2863da1a50ac44d2a48a936bae720aaa95..8bbed794`. That
is C0a through C4 (six content commits before this handback — C0a,
C0b, C1, C2, C3, C4). This handback (C5) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `74cfbd2863da1a50ac44d2a48a936bae720aaa95`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r9.md` saved verbatim (Write tool, reconstructed from the received prompt), 440 lines, sha256 `76bc49e7643f81d00fd5c3e46f732a75e48bfd79ee80eaccb552e3bbb442f784` |
| C0b | done | mirrored to `.agent/last_block.md` via `cp`, sha256 identical to C0a's file |
| C1 | done | GATE8 appended to `.agent/live_review.md` byte-exact (base 2441251 + `\n` + GATE8 2457 bytes = 2443709, confirmed by direct read after write) |
| C2 | done | PAIR P1-P6 (rewrites) + TEST T1-T4 (appends) applied to six files, one commit, 176 insertions total |
| C3 | done | DECISION F262 D1 appended to `.agent/decisions.md` byte-exact (base 792132 + `\n` + 5397 bytes = 797530, confirmed) |
| C4 | done | PLAN10 applied to `.agent/plan.md`, whole-file replace |
| C5 (this handback) | done | |
| py_compile (6 files) | done | exit 0 |
| pytest combined (4 files) | done | 223 passed |
| canary: tests/ui_server/ | done | 515 passed, unmoved from GATE8 baseline |
| canary: test_test_runner.py | done | 52 passed, unmoved |
| canary: test_resource_safety.py | done | 21 passed, unmoved |
| canary: test_integrity_gate.py | done | 16 passed, unmoved |
| canary: test_golden_path.py | done | 42 passed, unmoved |

## Commits

### e15da6a8 F262 R9 C0a: save block verbatim to .agent/authored/f262-r9.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r9.md` | +440/-0 | transport artifact — verbatim copy of the round's step block, new file |

### 23733b15 F262 R9 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +382/-280 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 7d6df1bd F262 R9 C1: append GATE8 to live_review.md - books round 8's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE8, `\n` + GATE8's own bytes appended to the base file |

### 838e0009 F262 R9 C2: patch.list/do_run/job.py gain created_at end to end (T002 batch 7)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | +3/-1 | PAIR P1 (rewrite: `datetime`/`timezone` import) and PAIR P2 (rewrite: `pi_created_at` stamped once, added to every explanation dict) |
| `packages/orchestration/approval_queue.py` | +5/-2 | PAIR P4 (rewrite: `created_at` in `list_patch_intents()`'s returned dict), PAIR P5 (rewrite: docstring line), PAIR P6 (rewrite: `format_intent_list()` gains CREATED column ahead of DECIDED) |
| `packages/orchestration/do_run.py` | +1/-0 | PAIR P3 (rewrite: `created_at` added to the fixture explanation dict; `datetime`/`timezone` already imported at line 22, no second import added) |
| `tests/orchestration/test_do_run.py` | +11/-0 | TEST T1 (append: `test_patch_intent_created_has_created_at` inserted after `test_patch_intent_created`, before `test_artifact_created`) |
| `tests/test_patch_intent_approval.py` | +31/-0 | TEST T2 (append: `test_format_intent_list_shows_created_when_set` in `TestFormatHelpers`, local `from packages.core.models import Artifact` import chosen over a module-level import to keep the diff smaller) and TEST T3 (append: `test_json_output_has_created_at_key` in `TestCmdListPatchIntents`) |
| `tests/test_run_log_cli.py` | +125/-0 | TEST T4 (append: `test_patch_intent_created_writes_created_at_on_explanation` in `TestRunNextTaskPatchIntentCreated`, after the class's only existing method) |

### 59bf9fe9 F262 R9 C3: append DECISION F262 D1 to decisions.md - CREATED date source
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14/-1 | byte-exact append of DECISION F262 D1 |

### 8bbed794 F262 R9 C4: replace plan.md with PLAN10
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21/-25 | whole-file replace with PLAN10 |

### (this handback commit, C5)
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
74cfbd2863da1a50ac44d2a48a936bae720aaa95
$ git branch --show-current
feature/f262-list-commands-v2
$ git status --porcelain
(empty)
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
All four confirmed.

**TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r9.md .agent/last_block.md
76bc49e7643f81d00fd5c3e46f732a75e48bfd79ee80eaccb552e3bbb442f784  .agent/authored/f262-r9.md
76bc49e7643f81d00fd5c3e46f732a75e48bfd79ee80eaccb552e3bbb442f784  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE8**:
```
base size immediately before C1: 2441251 bytes, no trailing newline (last byte '.')
GATE8 own byte length: 2457
GATE8 internal newline count: 0
base + 1 + GATE8_length = 2443709
post-C1 file real byte length = 2443709
match: True
```

**LEDGER APPEND, DECISION F262 D1**:
```
base size immediately before C3: 792132 bytes, no trailing newline
DECISION own byte length: 5397
base + 1 + DECISION_length = 797530
post-C3 file real byte length = 797530
match: True
```

**PRODUCTION PAIRS, READ AND COUNTED (P1-P6)**:
```
PAIR P1 (job.py, datetime import): FROM count before 1
PAIR P2 (job.py, explanation dict comprehension): FROM count before 1
PAIR P3 (do_run.py, fixture dict): FROM count before 1
PAIR P4 (approval_queue.py, list_patch_intents dict): FROM count before 1
PAIR P5 (approval_queue.py, docstring): FROM count before 1
PAIR P6 (approval_queue.py, format_intent_list): FROM count before 1
```
All six confirmed at exactly 1 occurrence in their target file before
being applied (constraint 1's re-confirmation, using each file's
CURRENT on-disk content, not the block's cited line numbers).

Full diff, `74cfbd28..838e0009`, all three production files:
```diff
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -6,6 +6,7 @@ import re
 import sys
 import time
 from collections.abc import Callable
+from datetime import datetime, timezone
 from typing import TYPE_CHECKING, Any
 
 from packages.core.models import Job, RunState, Task
@@ -609,9 +610,10 @@ def _cmd_run_next_task_local(job_id_str: str) -> None:
                         pis, pi_artifact.content or "", pi_task_type, pi_repo_root,
                     )
                     if dry_run_results:
+                        pi_created_at = datetime.now(timezone.utc).isoformat()
                         pi_artifact.metadata["patch_intent_explanations"] = [
                             {"file": r.target_path, "action": r.action, "risk": r.risk_level,
-                             "reason": r.reason, "summary": r.summary}
+                             "reason": r.reason, "summary": r.summary, "created_at": pi_created_at}
                             for r in dry_run_results
                         ]
                         pi_artifact.metadata["patch_intent_risks"] = [r.risk_level for r in dry_run_results]
diff --git a/packages/orchestration/approval_queue.py b/packages/orchestration/approval_queue.py
--- a/packages/orchestration/approval_queue.py
+++ b/packages/orchestration/approval_queue.py
@@ -146,6 +146,7 @@ def list_patch_intents(job: Job) -> list[dict]:
       risk             — validated risk level (RISK_LEVELS; RISK_UNKNOWN if bad)
       reason           — human-readable derivation reason
       summary          — truncated intent text
+      created_at       — ISO datetime string or None (set once, at intent-derivation time)
       state            — APPROVAL_PENDING | APPROVAL_APPROVED | APPROVAL_REJECTED
       decided_at       — ISO datetime string or None
       decided_by       — who recorded the decision, or None
@@ -174,6 +175,7 @@ def list_patch_intents(job: Job) -> list[dict]:
                     "risk": risk,
                     "reason": exp.get("reason", ""),
                     "summary": exp.get("summary", ""),
+                    "created_at": exp.get("created_at"),
                     "state": approval.get("state", APPROVAL_PENDING),
                     "decided_at": approval.get("decided_at"),
                     "decided_by": approval.get("decided_by"),
@@ -272,14 +274,15 @@ def format_intent_list(intents: list[dict]) -> str:
     if not intents:
         return "No patch intents found for this job."
 
-    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  {'DECIDED':<20}  TARGET PATH"]
-    lines.append("-" * 72)
+    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  {'CREATED':<20}  {'DECIDED':<20}  TARGET PATH"]
+    lines.append("-" * 92)
     for item in intents:
         lines.append(
             f"{item['intent_id']:<14}  "
             f"{item['state']:<8}  "
             f"{item['risk']:<8}  "
             f"{item['action']:<12}  "
+            f"{(item['created_at'] or '-'):<20}  "
             f"{(item['decided_at'] or '-'):<20}  "
             f"{item['target_path']}"
         )
diff --git a/packages/orchestration/do_run.py b/packages/orchestration/do_run.py
--- a/packages/orchestration/do_run.py
+++ b/packages/orchestration/do_run.py
@@ -517,6 +517,7 @@ def _run_patch_intent_phase(job: Any, artifact: Any, data_dir: Path) -> str:
             "action": "create",
             "risk": "low",
             "summary": "Safe documentation change",
+            "created_at": datetime.now(timezone.utc).isoformat(),
         }
     ]
     artifact.metadata["patch_intent_approvals"] = {}
```
Confirmed by reading the full diff: exactly PAIR P1/P2 in job.py, PAIR
P3 in do_run.py, PAIR P4/P5/P6 in approval_queue.py. Nothing else
touched in any of the three files.

```
$ python3 -m py_compile apps/cli/commands/job.py packages/orchestration/do_run.py packages/orchestration/approval_queue.py tests/orchestration/test_do_run.py tests/test_patch_intent_approval.py tests/test_run_log_cli.py
(exit 0, no output)
```
Exit 0 confirmed for all six touched files, one combined invocation.

Ruff attempted per constraint 3, refused:
```
$ ruff check <files>
This command requires approval
```
Denied this session, same shape of refusal seen in prior rounds (R8's
own handback recorded the identical text) — expected, not a blocker.

**PYTEST, C2's COMBINED RUN**:
```
$ python3 -m pytest tests/orchestration/test_do_run.py tests/test_patch_intent_approval.py tests/test_run_log_cli.py tests/test_command_catalog.py -q
223 passed in 1.02s
```

**THE STATE READERS AND THE CANARY, run individually**:
```
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.58s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.58s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.51s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.30s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.99s
```
515/52/21/16/42 — identical to GATE8's stated baseline. Not moved, as
expected: this round's change set names no path any of these five
suites should be sensitive to.

**THE PLAN**:
```
$ wc -l .agent/plan.md
45 .agent/plan.md
$ git diff --stat -- .agent/plan.md   (against pre-C4 HEAD)
21 insertions, 25 deletions
```
Whole-file replace applied via the Write tool with PLAN10's exact
content; `## Goal` and `## Next Steps` each appear once.

**THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C5 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C5, nothing under `.remedy-wt/` tracked (scratch
files `.remedy-wt/gate8_line.txt` and `.remedy-wt/decision_f262_d1.txt`
were written during this round to build byte-exact appends, remain
there, gitignored, untracked).

Per-commit numstat cross-check against this handback's own Commits
table:
```
$ git show --numstat e15da6a8
440  0    .agent/authored/f262-r9.md
$ git show --numstat 23733b15
382  280  .agent/last_block.md
$ git show --numstat 7d6df1bd
2    1    .agent/live_review.md
$ git show --numstat 838e0009
3    1    apps/cli/commands/job.py
5    2    packages/orchestration/approval_queue.py
1    0    packages/orchestration/do_run.py
11   0    tests/orchestration/test_do_run.py
31   0    tests/test_patch_intent_approval.py
125  0    tests/test_run_log_cli.py
$ git show --numstat 59bf9fe9
14   1    .agent/decisions.md
$ git show --numstat 8bbed794
21   25   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly. Note: at C0b commit time, `git commit`'s own printed
summary read "440 insertions(+), 338 deletions(-)" (a rename/rewrite
percentage-based estimate), while `--numstat` gives the real
line-level diff (382/280) used throughout this handback's Commits
table — the same tooling substitution R8's ledger entry already
documented; no committed byte is affected either way.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r9.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE8's
  content describes round 8's own verified facts.
- `apps/cli/commands/job.py` — NOT stale. Matches PAIR P1/P2 exactly;
  full diff read and confirmed.
- `packages/orchestration/do_run.py` — NOT stale. Matches PAIR P3
  exactly; no second `datetime` import added.
- `packages/orchestration/approval_queue.py` — NOT stale. Matches PAIR
  P4/P5/P6 exactly.
- `tests/orchestration/test_do_run.py`, `tests/test_patch_intent_approval.py`,
  `tests/test_run_log_cli.py` — NOT stale. TEST T1-T4 inserted exactly
  where specified; py_compile and pytest both green.
- `.agent/decisions.md` — NOT stale. DECISION F262 D1 is a fresh,
  dated entry describing this round's own reasoning.
- `.agent/plan.md` — NOT stale. Freshly written PLAN10 content
  accurately describes round 9's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from R8's own note.

## Deviations & assumptions

1. **No FROM mismatch occurred.** All six PAIR FROM strings (P1-P6)
   were re-read from each file's current on-disk content before
   applying, per constraint 1, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
2. **TEST T2's import placement** — the block offered a choice between
   a local `from packages.core.models import Artifact` inside the new
   test method or a module-level addition. Chose the local import (as
   the very first line of the method body) since `_add_patch_artifact`
   in the same file already uses that pattern, and it keeps the diff
   to exactly the new lines with no change to the shared module-level
   import list other tests also rely on.
3. **`git commit`'s printed stat for C0b** differed from `--numstat`
   (rename/rewrite percentage estimate vs. real line diff) — same
   substitution already declared in R8's own ledger; `--numstat`
   values are used throughout this handback's Commits table.
4. **Ruff denied**, as anticipated by constraint 3; noted, not treated
   as a blocker.
5. **`/tmp` writes were denied by the sandbox**; scratch files for
   building the byte-exact GATE8 and DECISION appends were written
   under the gitignored `.remedy-wt/` directory instead (consistent
   with this project's established scratch-location convention).

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, before C5, and once more before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r9.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/job.py`, `packages/orchestration/do_run.py`,
`packages/orchestration/approval_queue.py`,
`tests/orchestration/test_do_run.py`,
`tests/test_patch_intent_approval.py`, `tests/test_run_log_cli.py`,
`.agent/decisions.md`, `.agent/plan.md` and this handback were
committed. The bundle's commit order (C0a, C0b, C1, C2, C3, C4 — this
handback C5) was followed exactly, with C2 as one commit covering all
six files per constraint 5.

## Next

**NEXT EXPECTED ACTION: further date-coverage design, not T003 yet.**
PLAN10's Next Steps still lists two open date-coverage questions
(loop.list's CREATED substitute, change.list's event-log CREATED date)
before T003 (sort/filter/limit) should start, since T003 needs a
reasonably complete set of date fields to sort by across commands;
starting sort/filter work while two list commands still lack any
CREATED value risks building the sort flag against an incomplete
target shape. The execution.* trio's pre-existing `--json`-ignored
quirk stays excused per the Risks section.

**THIS IS SESSION 4, ROUND 9** — the operator may continue directly to
round 10 in this same session or start a fresh session per the
self-drive protocol's own judgment; no session/round-limit threshold
has been reached.
