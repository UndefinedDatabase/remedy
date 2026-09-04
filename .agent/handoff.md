# Handoff — F262 List commands v2 (dates, sort, filter), round 13 (T003 batch 1: shared list-options helper + job.list wiring)

## Session

SESSION 5 of feature F262 · round 13 · rounds so far 13.

Round 13 books round 12's PASS verdict (GATE12) into the ledger and
one `.agent/prose_slips.md` line for round 12's own arithmetic slip
first, then starts T003 (sort/filter/limit behaviour, newest-first
default): a new shared helper, `packages/orchestration/list_options.py`
(`apply_list_options`, `parse_time_bound`, `ListOptionError`), filters
by `--since`/`--until`, orders by `--sort`/`--desc` (newest-first is
the DEFAULT with no flags), and caps by `--limit` — one implementation
instead of 18 hand-rolled ones. Wired into `job.list` end to end as the
first proof of the design: `_cmd_list_jobs` reassigns its own `jobs`
list once before either `--json` or text rendering, so both branches
see the same filtered/sorted/limited rows by construction. One new
production file, one production rewrite, two test files (one new, one
appended), one commit.

## Range

Review of `02f92f4c6a339b793b621d18a3a9d6c731b6ea83..60d8c3123ba3406dae1aa002fee078a1bb454a93`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `02f92f4c6a339b793b621d18a3a9d6c731b6ea83`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r13.md` saved verbatim (Write tool, reconstructed from the received prompt), 508 lines, sha256 `f791b61c5a52e5444eb6bf1173e19645df07cd6d077bc416fec0a9b5aa864a73` |
| C0b | done | mirrored to `.agent/last_block.md` via `cp`, sha256 identical to C0a's file |
| C1 | done | GATE12 appended to `.agent/live_review.md` byte-exact (base 2452539 + `\n` + GATE12 2486 bytes = 2455026, confirmed by direct read after write) AND one line appended to `.agent/prose_slips.md` byte-exact (base 72998 + `\n` + slip 584 bytes = 73583, confirmed the same way) |
| C2 | done | one new production file (`packages/orchestration/list_options.py`), one production rewrite (PAIR P1 + PAIR P2 in `apps/cli/commands/job.py`), one new test file (`tests/orchestration/test_list_options.py`), one test append (TEST T1 in `tests/test_grouped_cli.py`) — four files, one commit; no follow-up fixes needed |
| C3 | done | PLAN14 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2388 == 2388) |
| C4 (this handback) | done | |
| py_compile (4 files) | done | exit 0, no output |
| pytest, C2's combined run | done | 530 passed |
| canary: combined 5-suite invocation | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |

## Commits

### f6eeacc3884fbf6587c99c822fb6e37141e33e13 F262 R13 C0a: save block verbatim to .agent/authored/f262-r13.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r13.md` | +508/-0 | transport artifact — verbatim copy of the round's step block, new file |

### 812943d116dcbeb073e85607e75b8e234bfa5661 F262 R13 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +417/-97 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 87cd8050a1e07a283347c242c059cfce8a148197 F262 R13 C1: append GATE12 to live_review.md and one line to prose_slips.md - books round 12's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE12, `\n` + GATE12's own bytes appended to the base file |
| `.agent/prose_slips.md` | +2/-1 | byte-exact append of one prose-slip line, `\n` + the line's own bytes appended to the base file |

### 9e27a561b8c8aef6189c9595435cf2f53b568395 F262 R13 C2: T003 batch 1 - shared list-options helper + job.list wiring
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | +26/-0 | PAIR P1 (`_cmd_list_jobs` gains sort/since/until/limit wiring via the new shared helper) + PAIR P2 (`job.list` dispatch lambda passes the five new flags through) |
| `packages/orchestration/list_options.py` | +112/-0 | new shared helper: `apply_list_options`, `parse_time_bound`, `ListOptionError` — no dependency on `packages.core.models` or any store |
| `tests/orchestration/test_list_options.py` | +99/-0 | new file: 9 domain tests for the shared helper |
| `tests/test_grouped_cli.py` | +35/-0 | TEST T1 (append: `test_default_order_is_newest_first`, `test_limit_caps_returned_jobs`, `test_unknown_sort_field_exits_nonzero`) |

### 60d8c3123ba3406dae1aa002fee078a1bb454a93 F262 R13 C3: replace plan.md with PLAN14
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +23/-22 | whole-file replace with PLAN14, byte-for-byte verified |

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
02f92f4c6a339b793b621d18a3a9d6c731b6ea83
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
$ sha256sum .agent/authored/f262-r13.md .agent/last_block.md
f791b61c5a52e5444eb6bf1173e19645df07cd6d077bc416fec0a9b5aa864a73  .agent/authored/f262-r13.md
f791b61c5a52e5444eb6bf1173e19645df07cd6d077bc416fec0a9b5aa864a73  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPENDS, GATE12 and the prose_slips.md line**:
```
base size immediately before C1 (live_review.md): 2452539 bytes
GATE12 own byte length: 2486
GATE12 internal newline count: 0
base + 1 + GATE12_length = 2455026
post-C1 file real byte length = 2455026
match: True

base size immediately before C1 (prose_slips.md): 72998 bytes
slip line own byte length: 584
slip line internal newline count: 0
base + 1 + slip_length = 73583
post-C1 file real byte length = 73583
match: True
```
Confirmed by direct Python byte read before and after each file, plus
`git diff --stat` reading `2 insertions(+), 1 deletion(-)` for each
file, consistent with the prior line losing its "no newline at end of
file" status and one new line being appended.

**PRODUCTION PAIR, READ AND COUNTED (P1, P2, T1)**:
```
PAIR P1 (job.py, _cmd_list_jobs body): FROM count before 1
PAIR P2 (job.py, job.list dispatch lambda): FROM count before 1
TEST T1 (test_grouped_cli.py, insertion point): FROM count before 1
```
All three confirmed at exactly 1 occurrence in their target file
before being applied (constraint 1's re-confirmation, using each
file's CURRENT on-disk content, read via the Read/grep tools, not
only the block's cited line numbers). `tests/test_grouped_cli.py`'s
T1_FROM was also confirmed to be the file's true last line (nothing
followed it) via a direct binary tail read.

Full diff, C2 (`9e27a561`), `apps/cli/commands/job.py`:
```diff
@@ -125,11 +125,32 @@ def _cmd_list_jobs(
     project: str | None = None,
     all_projects: bool = False,
     json_output: bool = False,
+    sort: str | None = None,
+    desc: bool = False,
+    since: str | None = None,
+    until: str | None = None,
+    limit: str | None = None,
 ) -> None:
+    from packages.orchestration.list_options import ListOptionError, apply_list_options
     from packages.orchestration.project_scope import resolve_scope, scoped_jobs

     scope = resolve_scope(project_flag=project, all_projects=all_projects)
     jobs, degraded, skipped = scoped_jobs(scope)
+    try:
+        jobs = apply_list_options(
+            jobs,
+            sort=sort, desc=desc, since=since, until=until, limit=limit,
+            sort_fields={
+                "created_at": lambda j: j.created_at,
+                "name": lambda j: j.name,
+                "state": lambda j: j.state.value,
+            },
+            default_sort_field="created_at",
+            date_getter=lambda j: j.created_at.isoformat(),
+        )
+    except ListOptionError as exc:
+        print(f"Error: {exc}", file=sys.stderr)
+        sys.exit(1)
     if json_output:
         import json as _json
         print(_json.dumps({
@@ -2447,6 +2468,11 @@ COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
         project=getattr(args, "project", None),
         all_projects=getattr(args, "all_projects", False),
         json_output=args.json,
+        sort=getattr(args, "sort", None),
+        desc=getattr(args, "desc", False),
+        since=getattr(args, "since", None),
+        until=getattr(args, "until", None),
+        limit=getattr(args, "limit", None),
     ),
     "job.show": lambda args: _cmd_show_job(args.job_id),
```
Confirmed by reading the full diff: exactly PAIR P1 and PAIR P2 in
`job.py`. Nothing else in the file touched. `packages/orchestration/
list_options.py` and `tests/orchestration/test_list_options.py` are
whole new files matching the authored content exactly (confirmed by
Write-tool round-trip); `tests/test_grouped_cli.py`'s diff is exactly
TEST T1's three new methods appended after the file's prior last line,
confirmed by reading the full diff (not reproduced here for length;
`git show --numstat 9e27a561` reads `35 0 tests/test_grouped_cli.py`,
matching the three-method append with no deletions).

```
$ python3 -m py_compile packages/orchestration/list_options.py apps/cli/commands/job.py tests/test_grouped_cli.py tests/orchestration/test_list_options.py
(exit 0, no output)
```
Exit 0 confirmed for all four touched/new files, one combined
invocation.

Ruff attempted per constraint 3, refused:
```
$ ruff check packages/orchestration/list_options.py apps/cli/commands/job.py tests/test_grouped_cli.py tests/orchestration/test_list_options.py
This command requires approval
```
Denied this session, same shape of refusal every prior round's
handback recorded — expected, not a blocker.

**PYTEST, C2's COMBINED RUN**:
```
$ python3 -m pytest tests/test_grouped_cli.py tests/orchestration/test_list_options.py -q
530 passed in 49.09s
```
Matches the block's own prediction exactly: 518 pre-existing in
`test_grouped_cli.py` (confirmed by `--collect-only -q` before this
round's edits) + 3 new there + 9 new in the new file = 530.

**THE STATE READERS AND THE CANARY, run as ONE combined invocation
per this round's block**:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q
646 passed in 70.86s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching the sum of GATE12's stated
per-suite baseline exactly. Not moved, as expected: this round's
change set names no path any of these five suites should be sensitive
to.

**THE PLAN, BYTE-FOR-BYTE (constraint 7)**:
```
authored PLAN14 slice length: 2388 bytes
written .agent/plan.md length: 2388 bytes
EQUAL (bytes == bytes): True
```
Whole-file replace applied via the Write tool, then independently
re-verified with a `python3 -B` script that builds the PLAN14 text
directly from the same source used to author it and compares it
byte-for-byte, in binary mode, against the written `.agent/plan.md` —
`expected == written` read `True`, no trailing-byte gap this round.

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
$ git show --numstat f6eeacc3
508  0    .agent/authored/f262-r13.md
$ git show --numstat 812943d1
417  97   .agent/last_block.md
$ git show --numstat 87cd8050
2    1    .agent/live_review.md
2    1    .agent/prose_slips.md
$ git show --numstat 9e27a561
26   0    apps/cli/commands/job.py
112  0    packages/orchestration/list_options.py
99   0    tests/orchestration/test_list_options.py
35   0    tests/test_grouped_cli.py
$ git show --numstat 60d8c312
23   22   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly (`git commit`'s own printed summaries were consistent
with `--numstat` this round for every commit — no rename/rewrite
percentage substitution was observed, unlike some prior rounds).

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r13.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE12's
  content describes round 12's own verified facts.
- `.agent/prose_slips.md` — NOT stale. Append-only ledger; describes
  round 12's own reviewer-authored miscount.
- `apps/cli/commands/job.py` — NOT stale. Matches PAIR P1 and PAIR P2
  exactly; full diff read and confirmed.
- `packages/orchestration/list_options.py` — NOT stale. New file,
  matches authored content exactly.
- `tests/orchestration/test_list_options.py` — NOT stale. New file,
  matches authored content exactly; all 9 tests pass.
- `tests/test_grouped_cli.py` — NOT stale. Matches TEST T1 exactly;
  py_compile and pytest both green.
- `.agent/plan.md` — NOT stale. Freshly written PLAN14 content
  accurately describes round 13's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Deviations & assumptions

1. **No FROM mismatch occurred.** All three FROM strings (P1, P2, T1)
   were re-read from each file's current on-disk content before
   applying, per constraint 1, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
2. **Pre-existing test count in `tests/test_grouped_cli.py` before
   this round: 518**, confirmed with `python3 -m pytest
   tests/test_grouped_cli.py --collect-only -q` before any edit was
   applied — this matches the block's own claim of 518 exactly (no
   arithmetic slip to book this round, unlike round 12's own).
3. **The C3 plan.md gate used the Write tool plus a real
   `bytes == bytes` comparison** via an independent `python3 -B`
   script comparing the PLAN14 text (built from the same source used
   to author it) against the written plan.md in binary mode — not
   `wc -l`/diffstat. Result: exact match, 2388 authored bytes == 2388
   written bytes (no trailing-byte gap for this file).
4. **`git commit`'s printed stat matched `--numstat` for every commit
   this round** — no rename/rewrite percentage substitution was
   observed this time (differs from round 12's C0b/C3 experience,
   noted for completeness, not a concern).
5. **Ruff denied**, as anticipated by constraint 3; noted, not treated
   as a blocker.
6. **The Bash tool rejected a few compound/piped commands this round**
   (a combined preconditions check using `&&`, and `xxd`/piped `tail`
   used to inspect trailing bytes); each was re-run as a single,
   standalone invocation (mostly small `python3` scripts doing the
   same byte-level checks, or `tail -c N` alone), with no change to
   the underlying verification performed — consistent with prior
   rounds' documented sandbox behavior.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, after C2, and once more before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r13.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`.agent/prose_slips.md`, `apps/cli/commands/job.py`,
`packages/orchestration/list_options.py`,
`tests/orchestration/test_list_options.py`, `tests/test_grouped_cli.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering all four named files per constraint 5.
Only `job.list` was wired this round; no other list command's handler
was touched, per constraint 2.

## Next

**NEXT EXPECTED ACTION: T003 batch 2 — wire `apply_list_options` into
a few more list commands.** PLAN14's Next Steps names
patch.list/loop.list/queue.list/memory.list as the next candidates,
ordered by risk/simplicity (already-dated, well-tested, isolated
handlers) — patch.list, queue.list and memory.list look like the
lowest-risk next batch since their JSON and text branches already
share one row-building path the way `job.list`'s did, while loop.list
needs its own reconciliation step first (its JSON rows come from a
per-loop last-run lookup and its text rows come from iterating
`LoopSpec` objects — two different collections today) — so round 14's
reasonable focus is patch.list/queue.list/memory.list as a batch,
leaving loop.list for a dedicated batch once its two-collection shape
is reconciled.

**THIS IS SESSION 5, ROUND 13** — the operator may continue directly
to round 14 in this same session or start a fresh session per the
self-drive protocol's own judgment; no session/round-limit threshold
has been reached.
