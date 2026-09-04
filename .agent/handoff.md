# Handoff — F262 List commands v2 (dates, sort, filter), round 12 (test.list gains a real per-row text listing)

## Session

SESSION 5 of feature F262 · round 12 · rounds so far 12.

Round 12 books round 11's PASS verdict (GATE11) into the ledger first,
then closes the last named gap round 11's audit found: `test.list`'s
`--json` branch already carried `created_at` per row, but its TEXT
branch printed only a bare count (`"Test runs for {job}: {N}"`) with
no per-row listing at all. `_cmd_test_list`'s text branch now either
prints an honest `"No test runs for {job}."` empty-state message, or
loops over the same `out["runs"]` list the JSON branch already built
and prints one line per row (`test_run_id`, `status`, `exit_code`,
`created`) — the same shape already used by `review.list` and
`patch.list`. No new field was added anywhere; only the TEXT branch
was wired to data that already existed. One production file, one test
file (two new tests appended), one commit.

## Range

Review of `de9d412ef6a1aa6088d85ea7eb55bae143e1ae86..344eb42fe3e7259716f8942f4cb62a9edbaf54b6`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `de9d412ef6a1aa6088d85ea7eb55bae143e1ae86`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r12.md` saved verbatim (Write tool, reconstructed from the received prompt), 188 lines, sha256 `29ed10fe8418108ed320a1a3f7c37127d4835fb1c312b6bbd9a399e23f271210` |
| C0b | done | mirrored to `.agent/last_block.md` via `cp`, sha256 identical to C0a's file |
| C1 | done | GATE11 appended to `.agent/live_review.md` byte-exact (base 2449694 + `\n` + GATE11 2836 bytes = 2452539, confirmed by direct read after write) |
| C2 | done | PAIR P1 (real_test_execution_cmd.py rewrite) + TEST T1 (two new tests appended to test_real_test_execution_cli.py) applied to two files, one commit; no follow-up fixes needed |
| C3 | done | PLAN13 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2312 == 2312) |
| C4 (this handback) | done | |
| py_compile (2 files) | done | exit 0, no output |
| pytest, C2's file | done | 8 passed |
| canary: combined 5-suite invocation | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |

## Commits

### b30c545d6de7d666ea18c5093ed40796a1f0ecf6 F262 R12 C0a: save block verbatim to .agent/authored/f262-r12.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r12.md` | +188/-0 | transport artifact — verbatim copy of the round's step block, new file |

### f8ea265e7a9c5c409f12bce6978baefd96603678 F262 R12 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +93/-190 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### c8d48c23252d7f7b4b47042ee581cf6ab02b6411 F262 R12 C1: append GATE11 to live_review.md - books round 11's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE11, `\n` + GATE11's own bytes appended to the base file |

### 0bab90b987e094a72ec48e08d1374d2b3786c63b F262 R12 C2: test.list gains a real per-row text listing
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/real_test_execution_cmd.py` | +5/-1 | PAIR P1 (rewrite: `_cmd_test_list`'s text branch gains an empty-state message and a per-row loop over `out["runs"]`) |
| `tests/cli/test_real_test_execution_cli.py` | +27/-0 | TEST T1 (append: `test_test_list_empty_text_message`, `test_test_list_text_shows_per_row`) |

### 344eb42fe3e7259716f8942f4cb62a9edbaf54b6 F262 R12 C3: replace plan.md with PLAN13
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +27/-25 | whole-file replace with PLAN13, byte-for-byte verified |

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
de9d412ef6a1aa6088d85ea7eb55bae143e1ae86
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
$ sha256sum .agent/authored/f262-r12.md .agent/last_block.md
29ed10fe8418108ed320a1a3f7c37127d4835fb1c312b6bbd9a399e23f271210  .agent/authored/f262-r12.md
29ed10fe8418108ed320a1a3f7c37127d4835fb1c312b6bbd9a399e23f271210  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE11**:
```
base size immediately before C1: 2449694 bytes
GATE11 own byte length: 2836
GATE11 internal newline count: 0
base + 1 + GATE11_length = 2452539
post-C1 file real byte length = 2452539
match: True
```
Confirmed by direct measurement (Python byte read before and after,
plus `git diff --stat` reading `2 insertions(+), 1 deletion(-)`,
consistent with the prior line losing its "no newline at end of file"
status and one new line being appended).

**PRODUCTION PAIR, READ AND COUNTED (P1, T1)**:
```
PAIR P1 (real_test_execution_cmd.py, text branch rewrite): FROM count before 1
TEST T1 (test_real_test_execution_cli.py, insertion point): FROM count before 1
```
Both confirmed at exactly 1 occurrence in their target file before
being applied (constraint 1's re-confirmation, using each file's
CURRENT on-disk content, read via the Read/grep tools, not only the
block's cited line numbers).

Full diff, C2 (`0bab90b9`), both files:
```diff
diff --git a/apps/cli/commands/real_test_execution_cmd.py b/apps/cli/commands/real_test_execution_cmd.py
--- a/apps/cli/commands/real_test_execution_cmd.py
+++ b/apps/cli/commands/real_test_execution_cmd.py
@@ -38,7 +38,11 @@ def _cmd_test_list(args: Any) -> None:
     if getattr(args, "json", False):
         print(json.dumps(out, indent=2))
         return
-    print(f"Test runs for {str(args.job_id)[:8]}: {len(runs)}")
+    if not out["runs"]:
+        print(f"No test runs for {str(args.job_id)[:8]}.")
+        return
+    for r in out["runs"]:
+        print(f"  {r['test_run_id']}  status={r['status']}  exit={r['exit_code']}  created={r['created_at']}")
 
 
 def _cmd_test_integrity(args: Any) -> None:
diff --git a/tests/cli/test_real_test_execution_cli.py b/tests/cli/test_real_test_execution_cli.py
--- a/tests/cli/test_real_test_execution_cli.py
+++ b/tests/cli/test_real_test_execution_cli.py
@@ -59,6 +59,33 @@ def test_test_list_empty(env):
     assert json.loads(r.stdout)["run_count"] == 0
 
 
+def test_test_list_empty_text_message(env):
+    jid = _job(env)
+    r = run_grouped_cli(["test", "list", jid], env)
+    assert r.returncode == 0, r.stderr
+    assert f"No test runs for {jid[:8]}." in r.stdout
+
+
+def test_test_list_text_shows_per_row(capsys):
+    from argparse import Namespace
+    from unittest.mock import patch
+
+    from apps.cli.commands.real_test_execution_cmd import _cmd_test_list
+
+    job_id = str(uuid4())
+    fake_runs = [{"test_run_id": "run-1", "status": "passed", "exit_code": 0,
+                  "created_at": "2026-09-04T00:00:00+00:00"}]
+    args = Namespace(job_id=job_id, json=False)
+    with patch("packages.orchestration.real_test_execution.list_test_runs", return_value=fake_runs):
+        _cmd_test_list(args)
+
+    out = capsys.readouterr().out
+    assert "run-1" in out
+    assert "status=passed" in out
+    assert "exit=0" in out
+    assert "created=2026-09-04T00:00:00+00:00" in out
+
+
 def test_test_integrity(env):
     jid = _job(env)
     run_grouped_cli(["snapshot", "create", jid, "--json"], env)
```
Confirmed by reading the full diff: exactly PAIR P1 in
`real_test_execution_cmd.py`, exactly TEST T1's two new functions in
`test_real_test_execution_cli.py`. Nothing else touched in either
file. The JSON branch above `_cmd_test_list`'s text logic, the `out`
dict construction above that, and `list_test_runs`/`_cmd_test_result`/
`_cmd_test_integrity` are confirmed untouched, per constraint 2.

```
$ python3 -m py_compile apps/cli/commands/real_test_execution_cmd.py tests/cli/test_real_test_execution_cli.py
(exit 0, no output)
```
Exit 0 confirmed for both touched files, one combined invocation.

Ruff attempted per constraint 3, refused:
```
$ ruff check apps/cli/commands/real_test_execution_cmd.py tests/cli/test_real_test_execution_cli.py
This command requires approval
```
Denied this session, same shape of refusal every prior round's
handback recorded — expected, not a blocker.

**PYTEST, C2's FILE**:
```
$ python3 -m pytest tests/cli/test_real_test_execution_cli.py -q
8 passed in 3.05s
```
The block's own prose estimated "expected 7 (5 pre-existing + 2 new)"
— that estimate was wrong, not this round's work: the file actually
carried 6 pre-existing tests before this round
(`test_snapshot_create_show`, `test_rollback_proof_honest`,
`test_test_list_empty`, `test_test_integrity`, `test_invalid_ids`,
`test_json_purity`, confirmed by `git show de9d412e:tests/cli/test_real_test_execution_cli.py`
grepped for `^def test_`), so 6 pre-existing + 2 new = 8, matching the
real reading exactly. See Deviations.

**THE STATE READERS AND THE CANARY, run as ONE combined invocation
per this round's block**:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q
646 passed in 70.34s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching the sum of GATE11's stated
per-suite baseline exactly. Not moved, as expected: this round's
change set names no path any of these five suites should be sensitive
to.

**THE PLAN, BYTE-FOR-BYTE (constraint 7)**:
```
authored PLAN13 slice length: 2312 bytes
written .agent/plan.md length: 2312 bytes
EQUAL (bytes == bytes): True
```
Whole-file replace applied via the Write tool, then independently
re-verified with a `python3 -B` script that extracts the PLAN13 slice
from the committed `.agent/authored/f262-r12.md` by its own
BEGIN/END markers and compares it byte-for-byte against the written
`.agent/plan.md` — `plan13 == written` read `True`, no trailing-byte
gap this round.

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
$ git show --numstat b30c545d
188  0    .agent/authored/f262-r12.md
$ git show --numstat f8ea265e
93   190  .agent/last_block.md
$ git show --numstat c8d48c23
2    1    .agent/live_review.md
$ git show --numstat 0bab90b9
5    1    apps/cli/commands/real_test_execution_cmd.py
27   0    tests/cli/test_real_test_execution_cli.py
$ git show --numstat 344eb42f
27   25   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly. Note: at C0b and C3 commit time, `git commit`'s own
printed summary used a rename/rewrite percentage-based estimate
(C0b printed "1 file changed, 188 insertions(+), 285 deletions(-),
rewrite .agent/last_block.md (72%)", differing from the 93/190
numstat truth; C3 printed "1 file changed, 49 insertions(+), 47
deletions(-), rewrite .agent/plan.md (71%)", differing from the 27/25
numstat truth) — the same tooling substitution prior rounds' ledger
entries already documented; `--numstat` values are used throughout
this handback's Commits table, no committed byte is affected either
way.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r12.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE11's
  content describes round 11's own verified facts.
- `apps/cli/commands/real_test_execution_cmd.py` — NOT stale. Matches
  PAIR P1 exactly; full diff read and confirmed.
- `tests/cli/test_real_test_execution_cli.py` — NOT stale. Matches
  TEST T1 exactly; py_compile and pytest both green.
- `.agent/plan.md` — NOT stale. Freshly written PLAN13 content
  accurately describes round 12's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Deviations & assumptions

1. **No FROM mismatch occurred.** Both FROM strings (P1, T1) were
   re-read from each file's current on-disk content before applying,
   per constraint 1, and each occurred exactly once — nothing needed
   to stop or be reported as a mismatch.
2. **The block's own prose miscounted the pre-existing test total.**
   It said "expected 7 (5 pre-existing + 2 new)"; the file actually
   had 6 pre-existing tests, so the real, correct total after C2's two
   new tests is 8, which is exactly what `pytest` reported (8 passed).
   This is a one-off arithmetic slip in the authored block's prose,
   not a defect in the applied change — every FROM/TO pair matched
   exactly and no test failed.
3. **No follow-up fix was needed in C2.** `_cmd_test_list`'s only
   caller-visible signature is unchanged (still takes `args`), so no
   pre-existing test or dispatch call site needed adjustment, unlike
   R10's dispatch breakage.
4. **The C3 plan.md gate used the Write tool plus a real
   `bytes == bytes` comparison** via an independent `python3 -B`
   script reading both the committed authored block and the written
   plan.md in binary mode — not `wc -l`/diffstat. Result: exact match,
   2312 authored bytes == 2312 written bytes (no trailing-byte gap for
   this file).
5. **`git commit`'s printed stat for C0b and C3** differed from
   `--numstat` (rename/rewrite percentage estimate vs. real line
   diff) — same substitution already declared in prior rounds'
   ledgers; `--numstat` values are used throughout this handback's
   Commits table.
6. **Ruff denied**, as anticipated by constraint 3; noted, not treated
   as a blocker.
7. **The Bash tool rejected several compound commands this round**
   (e.g. a combined preconditions check with multiple `&&`-joined
   parts, `xxd`/`tail` piping to inspect trailing bytes, and a bare
   `echo` after py_compile to report `$?`); each was re-run as a
   single, standalone invocation (mostly small `python3` scripts doing
   the same byte-level checks), with no change to the underlying
   verification performed — consistent with prior rounds' documented
   sandbox behavior.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, after C2, and once more before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r12.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/real_test_execution_cmd.py`,
`tests/cli/test_real_test_execution_cli.py`, `.agent/plan.md` and this
handback were committed. The bundle's commit order (C0a, C0b, C1, C2,
C3 — this handback C4) was followed exactly, with C2 as one commit
covering both named files per constraint 5.

## Next

**NEXT EXPECTED ACTION: start T003's design (sort/filter/limit
behaviour).** PLAN13's Next Steps names change.list's event-log
CREATED date as the one remaining named, excused gap (parked behind
DECISION F262 D1, unrelated to this round), and every other list
command's date coverage is now either shipped or explicitly excused —
so T002's per-command date work has run out of unexcused targets and
round 13 should move on to designing where T003's shared sort/filter/
limit behaviour lives (most likely one shared helper each list
handler's text/json branches call, built on top of the existing
`_with_list_options()` catalog surface, rather than 18 hand-rolled
implementations), rather than opening a new dating sub-task.

**THIS IS SESSION 5, ROUND 12** — the operator may continue directly
to round 13 in this same session or start a fresh session per the
self-drive protocol's own judgment; no session/round-limit threshold
has been reached.
