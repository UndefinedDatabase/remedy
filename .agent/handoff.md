# Handoff — F262 List commands v2 (dates, sort, filter), round 11 (T002 batch 9, review.list gains a CREATED date end to end)

## Session

SESSION 5 of feature F262 · round 11 · rounds so far 11.

Round 11 books round 10's PASS verdict (GATE10) into the ledger first,
then ships T002 batch 9: `review.list` gains a `created_at` field end
to end, the same shape as R9's patch.list and R10's loop.list batches.
`ReviewerRecommendation` gains a `created_at` field, stamped once in
`run_reviewer()` at construction time (`datetime.now(timezone.utc)`),
carried through `store_recommendations()`'s persisted dict, and
rendered as a `(created=...)` suffix in `_cmd_review_list`'s text
branch — its `--json` branch needed no code change, since it already
prints `list_recommendations()`'s own dicts verbatim and will now
include `created_at` automatically. A new `tests/cli/test_review_cmd.py`
(the first dedicated CLI test file for `review_cmd.py`) covers both
branches; `tests/orchestration/test_approval_queue.py` gains one more
round-trip test for the new field. Two production files, two test
files (one new), one commit.

## Range

Review of `c37fd16679cd1b65dd6f2b31a0a9a525479cb311..26a451401c00f83a3fa6b9f940027e85893d0e8a`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `c37fd16679cd1b65dd6f2b31a0a9a525479cb311`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r11.md` saved verbatim (Write tool, reconstructed from the received prompt), 285 lines, sha256 `22243901b501929043ad99dd8aa873620c89f476fe82753f6e4c4d4e30622d13` |
| C0b | done | mirrored to `.agent/last_block.md` via `cp`, sha256 identical to C0a's file |
| C1 | done | GATE10 appended to `.agent/live_review.md` byte-exact (base 2446822 + `\n` + GATE10 2871 bytes = 2449694, confirmed by direct read after write) |
| C2 | done | PAIR P1-P4 (reviewer.py rewrites) + PAIR P5 (review_cmd.py rewrite) + TEST T1 (test_approval_queue.py append) + TEST T2 (new file tests/cli/test_review_cmd.py) applied to four files, one commit; no follow-up fixes needed |
| C3 | done | PLAN12 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2144 == 2144) |
| C4 (this handback) | done | |
| py_compile (4 files) | done | exit 0, no output |
| pytest combined (2 files, C2) | done | 28 passed |
| canary: combined 5-suite invocation | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |

## Commits

### def4a3c5875110e9400aff0a1db5ef5b0db36327 F262 R11 C0a: save block verbatim to .agent/authored/f262-r11.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r11.md` | +285/-0 | transport artifact — verbatim copy of the round's step block, new file |

### 36f08d2e701bbfb14698bece45c0c8903dc9f7ba F262 R11 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +169/-181 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### f794abda7770261a8a35316a4f1c6b19d9d2936b F262 R11 C1: append GATE10 to live_review.md - books round 10's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE10, `\n` + GATE10's own bytes appended to the base file |

### a57aa2d47cef54b69fa91c3ed2826a0b5dd3c43f F262 R11 C2: review.list gains a CREATED date end to end (T002 batch 9)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/reviewer.py` | +4/-0 | PAIR P1 (rewrite: `datetime`/`timezone` import), PAIR P2 (append: `created_at` field on `ReviewerRecommendation`), PAIR P3 (rewrite: `run_reviewer()` stamps `created_at`), PAIR P4 (rewrite: `store_recommendations()` persists `created_at`) |
| `apps/cli/commands/review_cmd.py` | +2/-1 | PAIR P5 (rewrite: `_cmd_review_list`'s text branch gains a `created=` suffix) |
| `tests/orchestration/test_approval_queue.py` | +16/-0 | TEST T1 (append: `test_store_and_list_recommendations_carries_created_at`) |
| `tests/cli/test_review_cmd.py` | +46/-0 | TEST T2 (new file: `test_text_output_shows_created_date`, `test_json_output_carries_created_at`) |

### 26a451401c00f83a3fa6b9f940027e85893d0e8a F262 R11 C3: replace plan.md with PLAN12
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +25/-21 | whole-file replace with PLAN12, byte-for-byte verified |

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
c37fd16679cd1b65dd6f2b31a0a9a525479cb311
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
$ sha256sum .agent/authored/f262-r11.md .agent/last_block.md
22243901b501929043ad99dd8aa873620c89f476fe82753f6e4c4d4e30622d13  .agent/authored/f262-r11.md
22243901b501929043ad99dd8aa873620c89f476fe82753f6e4c4d4e30622d13  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE10**:
```
base size immediately before C1: 2446822 bytes
GATE10 own byte length: 2871
GATE10 internal newline count: 0
base + 1 + GATE10_length = 2449694
post-C1 file real byte length = 2449694
match: True
```
Confirmed by direct measurement (`wc -c` before and after, plus
`git diff --stat` reading `2 insertions(+), 1 deletion(-)`, consistent
with the prior line losing its "no newline at end of file" status and
one new line being appended).

**PRODUCTION PAIRS, READ AND COUNTED (P1-P5, T1)**:
```
PAIR P1 (reviewer.py, datetime/timezone import): FROM count before 1
PAIR P2 (reviewer.py, created_at field append): FROM count before 1
PAIR P3 (reviewer.py, run_reviewer stamps created_at): FROM count before 1
PAIR P4 (reviewer.py, store_recommendations persists created_at): FROM count before 1
PAIR P5 (review_cmd.py, text branch created= suffix): FROM count before 1
TEST T1 (test_approval_queue.py, insertion point): FROM count before 1
```
All six confirmed at exactly 1 occurrence in their target file before
being applied (constraint 1's re-confirmation, using each file's
CURRENT on-disk content, read via the Read tool, not the block's cited
line numbers). TEST T2 was a brand-new file (`tests/cli/test_review_cmd.py`
confirmed absent before creation).

Full diff, `def4a3c5..a57aa2d4`, both production files:
```diff
diff --git a/apps/cli/commands/review_cmd.py b/apps/cli/commands/review_cmd.py
--- a/apps/cli/commands/review_cmd.py
+++ b/apps/cli/commands/review_cmd.py
@@ -83,7 +83,8 @@ def _cmd_review_list(args: Any) -> None:
             status = r.get("status", "?")
             title = r.get("title", "?")
             rid = r.get("id", "?")
-            print(f"  [{status}] {rid}  {title}")
+            created = r.get("created_at", "?")
+            print(f"  [{status}] {rid}  {title}  (created={created})")
 
 
 def _cmd_review_accept(args: Any) -> None:
diff --git a/packages/orchestration/reviewer.py b/packages/orchestration/reviewer.py
--- a/packages/orchestration/reviewer.py
+++ b/packages/orchestration/reviewer.py
@@ -19,6 +19,7 @@ from __future__ import annotations
 
 from collections.abc import Callable
 from dataclasses import dataclass
+from datetime import datetime, timezone
 from typing import Any
 from uuid import uuid4
 
@@ -36,6 +37,7 @@ class ReviewerRecommendation:
     source: str = "reviewer"
     origin_task_id: str = ""
     status: str = "pending"  # pending, accepted, rejected
+    created_at: str = ""
 
 
 def _default_reviewer(context: dict[str, Any]) -> list[dict[str, Any]]:
@@ -105,6 +107,7 @@ def run_reviewer(
             priority=str(item.get("priority", "low")),
             source="reviewer",
             origin_task_id=after_task_id or "",
+            created_at=datetime.now(timezone.utc).isoformat(),
         )
         recs.append(rec)
 
@@ -160,6 +163,7 @@ def store_recommendations(job: Any, recs: list[ReviewerRecommendation]) -> None:
             "source": rec.source,
             "origin_task_id": rec.origin_task_id,
             "status": rec.status,
+            "created_at": rec.created_at,
         })
     _save_recommendations(job, existing)
```
Confirmed by reading the full diff: exactly PAIR P1/P2/P3/P4 in
reviewer.py, PAIR P5 in review_cmd.py. Nothing else touched in either
file. The JSON branch above `_cmd_review_list`'s text loop, and the
`if not recs:` early return, are confirmed untouched, per constraint 8.

```
$ python3 -m py_compile packages/orchestration/reviewer.py apps/cli/commands/review_cmd.py tests/orchestration/test_approval_queue.py tests/cli/test_review_cmd.py
(exit 0, no output)
```
Exit 0 confirmed for all four touched/added files, one combined
invocation.

Ruff attempted per constraint 3, refused:
```
$ ruff check packages/orchestration/reviewer.py apps/cli/commands/review_cmd.py
This command requires approval
```
Denied this session, same shape of refusal every prior round's
handback recorded — expected, not a blocker.

**PYTEST, C2's COMBINED RUN**:
```
$ python3 -m pytest tests/cli/test_review_cmd.py tests/orchestration/test_approval_queue.py -q
28 passed in 0.42s
```
Matches the block's expected count exactly (25 pre-existing in
test_approval_queue.py + 1 new there + 2 new in the new file = 28).
No follow-up fixes were needed this round — unlike R10's dispatch
breakage, `review_cmd.py`'s dispatch lambdas already pass `args`
through unconditionally for every review.* command, so no pre-existing
test's bare Namespace was newly exercised by this round's change.

**THE STATE READERS AND THE CANARY, run as ONE combined invocation
per this round's block (a change from R10's per-suite style)**:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q
646 passed in 70.13s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching the sum of GATE10's stated
per-suite baseline exactly. Not moved, as expected: this round's
change set names no path any of these five suites should be sensitive
to.

**THE PLAN, BYTE-FOR-BYTE (constraint 7)**:
```
authored PLAN12 slice length: 2144 bytes
written .agent/plan.md length: 2144 bytes
EQUAL (bytes == bytes): True
```
Whole-file replace applied via the Write tool, then independently
re-verified with a `python3 -B` script that extracts the PLAN12 slice
from the committed `.agent/authored/f262-r11.md` by its own
BEGIN/END markers and compares it byte-for-byte against the written
`.agent/plan.md` — `plan12 == written` read `True`, no trailing-byte
gap this round (unlike R9's).

**THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked.

Per-commit numstat cross-check against this handback's own Commits
table:
```
$ git show --numstat def4a3c5
285  0    .agent/authored/f262-r11.md
$ git show --numstat 36f08d2e
169  181  .agent/last_block.md
$ git show --numstat f794abda
2    1    .agent/live_review.md
$ git show --numstat a57aa2d4
2    1    apps/cli/commands/review_cmd.py
4    0    packages/orchestration/reviewer.py
46   0    tests/cli/test_review_cmd.py
16   0    tests/orchestration/test_approval_queue.py
$ git show --numstat 26a45140
25   21   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly. Note: at C0b and C3 commit time, `git commit`'s own
printed summary used a rename/rewrite percentage-based estimate
(C0b printed "1 file changed, 285 insertions(+), 297 deletions(-),
rewrite .agent/last_block.md (73%)", differing from the 169/181
numstat truth; C3 printed "1 file changed, 47 insertions(+), 43
deletions(-), rewrite .agent/plan.md (68%)", differing from the 25/21
numstat truth) — the same tooling substitution prior rounds' ledger
entries already documented; `--numstat` values are used throughout
this handback's Commits table, no committed byte is affected either
way.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r11.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE10's
  content describes round 10's own verified facts.
- `packages/orchestration/reviewer.py` — NOT stale. Matches PAIR
  P1-P4 exactly; full diff read and confirmed.
- `apps/cli/commands/review_cmd.py` — NOT stale. Matches PAIR P5
  exactly; full diff read and confirmed.
- `tests/orchestration/test_approval_queue.py` — NOT stale. Matches
  TEST T1 exactly; py_compile and pytest both green.
- `tests/cli/test_review_cmd.py` — NOT stale in substance. New file;
  matches TEST T2's specified content except for one trailing newline
  byte the Write tool appended (see Deviations item 3) — every line of
  code, both test functions and `_recs()` are byte-identical to the
  block's literal text.
- `.agent/plan.md` — NOT stale. Freshly written PLAN12 content
  accurately describes round 11's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Deviations & assumptions

1. **No FROM mismatch occurred.** All six FROM strings (P1-P5, T1)
   were re-read from each file's current on-disk content before
   applying, per constraint 1, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
2. **No follow-up fix was needed in C2**, unlike R10's dispatch
   breakage. `review_cmd.py`'s five dispatch lambdas
   (`review.bundle`/`review.run`/`review.list`/`review.accept`/
   `review.reject`) already pass `args` through unconditionally to
   every handler (`lambda args: _cmd_review_list(args)`), so PAIR
   P5's change (adding a `created` local variable inside the existing
   text loop) did not change the handler's signature or touch any
   dispatch call site — no pre-existing bare-Namespace test was newly
   exercised.
3. **`tests/cli/test_review_cmd.py` (TEST T2, a whole new file) carries
   one trailing newline byte beyond the block's literal T2_NEWFILE
   content.** Verified with an independent `python3 -B` byte
   comparison: the T2_NEWFILE slice extracted from
   `.agent/authored/f262-r11.md` by its own BEGIN/END markers is 1448
   bytes; the written file is 1449 bytes; `t2 == written[:-1]` reads
   `True` — the only difference is the file's own trailing `\n`, added
   by the Write tool (standard POSIX text-file convention; every
   Python source file elsewhere in this repo also ends this way). No
   line of code differs. This is the same shape of gap R9's C4 gate
   found in `.agent/plan.md` and routed to `.agent/prose_slips.md`
   rather than an R-id (amend0827 rule 2) — but that routing rule is
   scoped to `.agent/` prose specifically; `tests/` is production
   surface, not `.agent/` state, so this round does not self-apply
   that same routing and instead reports it plainly here as an honest,
   no-product-effect deviation for the reviewer to route.
4. **The C3 plan.md gate used the Write tool plus a real
   `bytes == bytes` comparison** via an independent `python3 -B`
   script reading both the committed authored block and the written
   plan.md in binary mode — not `wc -l`/diffstat. Result: exact match,
   2144 authored bytes == 2144 written bytes (no trailing-byte gap for
   this file, unlike the new test file in item 3 above).
5. **`git commit`'s printed stat for C0b and C3** differed from
   `--numstat` (rename/rewrite percentage estimate vs. real line
   diff) — same substitution already declared in prior rounds'
   ledgers; `--numstat` values are used throughout this handback's
   Commits table.
6. **Ruff denied**, as anticipated by constraint 3; noted, not treated
   as a blocker.
7. **The Bash tool rejected several compound (`&&`-joined) commands
   this round** (e.g. the initial combined preconditions check, an
   initial `echo "EXIT:$?"` after py_compile); each was re-run as a
   single, standalone invocation, with no change to the underlying
   verification performed — consistent with prior rounds' documented
   sandbox behavior.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, after C2, and once more before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r11.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`packages/orchestration/reviewer.py`,
`apps/cli/commands/review_cmd.py`,
`tests/orchestration/test_approval_queue.py`,
`tests/cli/test_review_cmd.py`, `.agent/plan.md` and this handback
were committed. The bundle's commit order (C0a, C0b, C1, C2, C3 — this
handback C4) was followed exactly, with C2 as one commit covering all
four files per constraint 5.

## Next

**NEXT EXPECTED ACTION: start Round 11's own audit of all remaining
catalog list commands' date coverage against T002, then decide T003
readiness.** PLAN12's Next Steps names two concrete gaps this round's
own audit found while confirming review.list was the last unexcused,
undated list command: change.list's event-log CREATED date question
(open per DECISION F262 D1) and test.list's text branch, which prints
a bare count with no per-row listing at all (a gap wider than a
missing date — it has no rows to attach one to). Reasoning: with
review.list now dated, T002's per-command date work has run out of
unexcused targets except these two named gaps; round 12 should decide
whether to resolve or explicitly excuse each (most likely test.list's
missing per-row listing, since it is closer to a plain CLI defect than
a design question, while change.list's event-log join is a harder,
already-analyzed-and-parked problem) before T003 (sort/filter/limit)
begins, so that T003's design does not have to special-case commands
still missing a date to sort by.

**THIS IS SESSION 5, ROUND 11** — the operator may continue directly
to round 12 in this same session or start a fresh session per the
self-drive protocol's own judgment; no session/round-limit threshold
has been reached.
