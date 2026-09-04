# Handoff — F262 List commands v2 (dates, sort, filter), round 7 (T002 batch 5, job.list/queue.list --json)

## Session

SESSION 2 of feature F262 · round 7 · rounds so far 7.

Round 7 ships T002 batch 5: `job.list` and `queue.list` gain `--json`
end to end (catalog `args` + `supports_json=True`, handler
`json_output` kwarg + json branch, dispatch lambda) — the same shape
round 6 proved once for `project.list`. `job.list`'s json output
carries `created_at` (its TEXT output already printed an ISO date —
only `--json` was missing). `queue.list`'s json output carries the RAW
`created_at` string plus `goal` (its TEXT output prints an AGE,
`_age(entry.created_at)`, a pre-existing derived display this round
does NOT change — out of scope, not a gap). Neither `Job` nor the
queue entry model has a second/updated timestamp, so neither json
gains an `updated_at` key — same precedent as rounds 5 and 6. Three
production files (`command_catalog.py` touched twice), two test files.
No model or store change.

## Range

Review of `7c25e9363ee43c6b91d26659e7d538ce9b9650f2..23cd7e21`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `7c25e9363ee43c6b91d26659e7d538ce9b9650f2`, branch matched, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r7.md` saved verbatim, 490 lines |
| C0b | done | mirrored to `.agent/last_block.md`, sha256 identical |
| C1 | done | GATE6 appended to `.agent/live_review.md` byte-exact |
| C2 | done | PAIR J1 (rewrite) + PAIR Q1 (rewrite) applied to `command_catalog.py`; PAIR J2 (rewrite) + PAIR J3 (rewrite) applied to `job.py`; PAIR Q2 (rewrite) + PAIR Q3 (rewrite) applied to `queue_cmd.py`; four new tests added across two test files; one commit, five files |
| C3 | done | PLAN8 applied to `.agent/plan.md`, whole-file replace |
| C4 (this handback) | done | |
| G1 TRANSPORT | done | PASS — one digest, twice |
| G2 THE LEDGER APPEND | done | PASS — arithmetic matched, tail equal, negative control rejected |
| G3 THE SIX PAIRS | done | PASS — J1/Q1/J2/J3/Q2/Q3 FROM 1→0, TO 0→1 (all rewrites); both `command_catalog.py` edits confirmed to have landed independently; all three production diffs read in full, nothing else touched; py_compile exit 0 x5 |
| G4 THE TESTS, BEFORE AND AFTER | done | PASS — `test_grouped_cli.py` 516→518 (base+2), `test_queue_cmd.py` 24→26 (base+2), fully green both times |
| G5 STATE READERS + CANARY | done | PASS — 515/52/21/16/42, unmoved from session baseline |
| G6 THE PLAN | done | PASS — byte comparison equal, 41 lines, both header counts 1 |
| G7 THE TREE, COMMITS, SWEEP | done | PASS — tree clean, `.remedy-wt` untracked, numstats compared cell-for-cell, staleness declared |

## Commits

### 1af43b59 F262 R7 C0a: save round 7 step block to .agent/authored/f262-r7.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r7.md` | +490/-0 | transport proof — verbatim copy (`shutil.copyfile`) of the reviewer's step block (`.remedy-wt/f262-r7-block.txt`), new file |

### 3a19d064 F262 R7 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +365/-202 | mirror of the round's authored block via `shutil.copyfile` (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 99325866 F262 R7 C1: append GATE6 to live_review.md - books round 6's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE6 (extracted from committed authored file by marker index), `\n` + GATE6's own bytes appended to the base file |

### c7c676e3 F262 R7 C2: job.list and queue.list gain --json end to end (T002 batch 5)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +4/-2 | PAIR J1 (rewrite: `job.list` CommandEntry gains `_JSON_OPT` in `args` and `supports_json=True`) and PAIR Q1 (rewrite: `queue.list` CommandEntry gains the same, `related=` unchanged and unmoved) |
| `apps/cli/commands/job.py` | +12/-0 | PAIR J2 (rewrite: `_cmd_list_jobs` gains `json_output` kwarg + json branch) and PAIR J3 (rewrite: dispatch lambda passes `json_output=args.json`) |
| `apps/cli/commands/queue_cmd.py` | +15/-1 | PAIR Q2 (rewrite: `_cmd_queue_list` gains `json_output` kwarg + json branch, RAW `created_at` string, `skipped_total`/stderr print left in place unmoved) and PAIR Q3 (rewrite: dispatch lambda passes `json_output=args.json`) |
| `tests/cli/test_queue_cmd.py` | +14/-0 | two new tests added by hand per the TEST SPEC: `test_list_has_json_flag` (in `TestCatalog`), `test_json_has_created_at_and_goal` (in `TestList`) |
| `tests/test_grouped_cli.py` | +22/-0 | new class `TestJobListCLI` added by hand per the TEST SPEC: `test_catalog_has_json_flag`, `test_list_json_has_created_at` |

### 23cd7e21 F262 R7 C3: replace plan.md with PLAN8
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12/-10 | whole-file replace with PLAN8 extracted from the committed authored file (per constraint 6) |

### (this handback commit, C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push origin feature/f262-list-commands-v2` — runs immediately
  after this commit, per the Bundle's C4 step; reported in the closing
  message, not here, since it happens after this file is committed. No
  `gh pr` command of any kind was run (forbidden this round: no PR, no
  merge, no Open PR Gate).

## Verification

Preconditions, checked before C0a:
```
$ git status --porcelain
(empty)
$ git rev-parse HEAD
7c25e9363ee43c6b91d26659e7d538ce9b9650f2
$ git branch --show-current
feature/f262-list-commands-v2
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
All four confirmed.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r7.md .agent/last_block.md
3ba94f24b91b38acc72ca8c09f90e9ed6d0007fa869247eb92ca19ca99667e6b  .agent/authored/f262-r7.md
3ba94f24b91b38acc72ca8c09f90e9ed6d0007fa869247eb92ca19ca99667e6b  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND, FULL FORENSICS**:
```
base size immediately before C1: 2433283 bytes, no trailing newline (last byte '.')
GATE6 own byte length: 4180
GATE6 internal newline count: 0
base + 1 + GATE6_length = 2437464
post-C1 file real byte length = 2437464
match: True
tail slice (last 4180 bytes of post-C1 file) vs GATE6: equal True
negative control: flipped first byte of a COPY of GATE6 vs the real tail: rejected True
```
All readings PASS — matches the block's own stated base (2433283,
no trailing newline, last byte `.`) exactly.

**G3 THE SIX PAIRS, READ AND COUNTED, PER CONSTRAINT 2's SHAPES**:
```
PAIR J1 (rewrite): FROM count before 1, FROM count after 0, TO count after 1
PAIR Q1 (rewrite): FROM count before 1, FROM count after 0, TO count after 1
PAIR J2 (rewrite): FROM count before 1, FROM count after 0, TO count after 1
PAIR J3 (rewrite): FROM count before 1, FROM count after 0, TO count after 1
PAIR Q2 (rewrite): FROM count before 1, FROM count after 0, TO count after 1
PAIR Q3 (rewrite): FROM count before 1, FROM count after 0, TO count after 1
```
All six PASS, matching Constraint 2's predicted shapes exactly
(extracted from the committed authored file via one `python3 -c`
script into a pickle of six FROM/TO pairs, applied via per-target
`python3 -c` scripts doing `content.replace(FROM, TO, 1)`, never
hand-retyped).

Constraint 7 pre-checks, done before writing any pair (all six FROM
strings counted against their target file in one script, reported
above under "count = 1" for each) — each exactly 1, as required —
proceeded to edit.

J1/Q1 both landed on `apps/cli/command_catalog.py`, confirmed
independently afterward:
```
$ grep -n 'command_id="job.list"' -A6 apps/cli/command_catalog.py
271:        command_id="job.list",
...
276-        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
277-        supports_json=True,
$ grep -n 'command_id="queue.list"' -A8 apps/cli/command_catalog.py
604:        command_id="queue.list",
...
609-        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
610-        supports_json=True,
611-        related=("queue.add",),
```
Both `command_id` lines appear exactly once each, each now followed by
`supports_json=True` within its own entry — both landed.

Full diff of `apps/cli/command_catalog.py`:
```diff
@@ -273,7 +273,8 @@ _BASE_CATALOG: tuple[CommandEntry, ...] = (
         subcommand="list",
         description="List jobs (scoped to current project by default).",
         action_class="read_only",
-        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG),
+        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
+        supports_json=True,
     ),
     CommandEntry(
         command_id="job.show",
@@ -605,7 +606,8 @@ _BASE_CATALOG: tuple[CommandEntry, ...] = (
         subcommand="list",
         description="List queue entries (scoped to the current project by default).",
         action_class="read_only",
-        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG),
+        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
+        supports_json=True,
         related=("queue.add",),
     ),
     CommandEntry(
```
Confirmed by reading the full diff: exactly the two named
insertions, one per entry. No other `CommandEntry` in the file was
touched.

Full diff of `apps/cli/commands/job.py`:
```diff
@@ -123,11 +123,22 @@ def _cmd_list_jobs(
     *,
     project: str | None = None,
     all_projects: bool = False,
+    json_output: bool = False,
 ) -> None:
     from packages.orchestration.project_scope import resolve_scope, scoped_jobs

     scope = resolve_scope(project_flag=project, all_projects=all_projects)
     jobs, degraded, skipped = scoped_jobs(scope)
+    if json_output:
+        import json as _json
+        print(_json.dumps({
+            "version": 1,
+            "job_count": len(jobs),
+            "jobs": [{"id": str(job.id), "state": job.state.value, "name": job.name,
+                     "created_at": job.created_at.isoformat(),
+                     "project_id": job.project_id or ""} for job in jobs],
+        }, sort_keys=True))
+        return
     if not jobs:
         print("No jobs found.")
         return
@@ -2433,6 +2444,7 @@ COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
     "job.list": lambda args: _cmd_list_jobs(
         project=getattr(args, "project", None),
         all_projects=getattr(args, "all_projects", False),
+        json_output=args.json,
     ),
     "job.show": lambda args: _cmd_show_job(args.job_id),
```
Confirmed by reading the full diff: exactly PAIR J2 (function body
rewrite) and PAIR J3 (dispatch line rewrite) changed. `degraded`
remains unused, as it was in the original — not a defect this round
introduces. Every other handler and dispatch line in the file is
byte-for-byte untouched.

Full diff of `apps/cli/commands/queue_cmd.py`:
```diff
@@ -126,7 +126,8 @@ def _project_ids_with_a_queue() -> list[str]:
     return sorted(p.name for p in root.iterdir() if p.is_dir())


-def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False) -> None:
+def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False,
+                    json_output: bool = False) -> None:
     from packages.orchestration.job_queue import list_entries_safe

     if all_projects:
@@ -141,6 +142,18 @@ def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False) -
         skipped_total += len(skipped)
         rows.extend((project_id, entry) for entry in entries)

+    if json_output:
+        import json as _json
+        print(_json.dumps({
+            "version": 1,
+            "entry_count": len(rows),
+            "entries": [{"id": entry.id, "status": entry.status, "priority": entry.priority,
+                        "created_at": entry.created_at, "claimed_by": entry.claimed_by or "",
+                        "goal": _goal_label(entry), "project_id": project_id}
+                       for project_id, entry in rows],
+        }, sort_keys=True))
+        return
+
     if not rows:
         print("No queue entries found.")
     for project_id, entry in rows:
@@ -234,6 +247,7 @@ COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
     "queue.list": lambda args: _cmd_queue_list(
         project=getattr(args, "project", None),
         all_projects=getattr(args, "all_projects", False),
+        json_output=args.json,
     ),
     "queue.rm": lambda args: _cmd_queue_rm(
         args.entry_id, project=getattr(args, "project", None)),
```
Confirmed by reading the full diff: exactly PAIR Q2 (function body
rewrite) and PAIR Q3 (dispatch line rewrite) changed. `entry.created_at`
is used raw (a plain ISO string), never `.isoformat()`'d, per the
block's own note. `skipped_total` and its trailing stderr print
(`if skipped_total: print(...)`) stayed in place after the new
`json_output` branch, unmoved — confirmed at `grep -n skipped_total
apps/cli/commands/queue_cmd.py` reading lines 139/142/164/165. Every
other handler and dispatch line is byte-for-byte untouched.

```
$ python3 -c "import py_compile; py_compile.compile('apps/cli/command_catalog.py', doraise=True)"
OK
$ python3 -c "import py_compile; py_compile.compile('apps/cli/commands/job.py', doraise=True)"
OK
$ python3 -c "import py_compile; py_compile.compile('apps/cli/commands/queue_cmd.py', doraise=True)"
OK
$ python3 -c "import py_compile; py_compile.compile('tests/test_grouped_cli.py', doraise=True)"
OK
$ python3 -c "import py_compile; py_compile.compile('tests/cli/test_queue_cmd.py', doraise=True)"
OK
$ python3 -m py_compile apps/cli/command_catalog.py apps/cli/commands/job.py apps/cli/commands/queue_cmd.py tests/test_grouped_cli.py tests/cli/test_queue_cmd.py
(exit 0, no output — succeeded on a later retry; several earlier
attempts at this exact command were rejected outright by the sandbox
before one ran clean — see Deviations)
```
Exit 0 confirmed for all five files, both individually (via
`py_compile.compile(..., doraise=True)`, equivalent to `python3 -m
py_compile` on a single file) and as one combined `-m py_compile`
invocation across all five — PASS.

Ruff attempted per constraint 4, exact refusal reproduced:
```
$ ruff check apps/cli/command_catalog.py apps/cli/commands/job.py apps/cli/commands/queue_cmd.py tests/test_grouped_cli.py tests/cli/test_queue_cmd.py
Permission to use Bash has been denied. IMPORTANT: You *may* attempt to
accomplish this action using other tools that might naturally be used
to accomplish this goal ... [sandbox denial text]
```
Ruff is denied this session, exactly as the block warned — same
wording as rounds 5 and 6's refusals.

**G4 THE TESTS, BEFORE AND AFTER**:
```
Before C2:
$ python3 -m pytest tests/test_grouped_cli.py -q
516 passed in 48.58s
$ python3 -m pytest tests/cli/test_queue_cmd.py -q
24 passed in 10.20s

After C2:
$ python3 -m pytest tests/test_grouped_cli.py -q
518 passed in 48.61s
$ python3 -m pytest tests/cli/test_queue_cmd.py -q
26 passed in 10.62s
```
Both baselines matched the block's stated 516/24 exactly; after C2
both are base + 2, fully green — PASS. Nothing else in either file
touched (confirmed by the full diffs above and in G3).

**G5 THE STATE READERS AND THE CANARY**:
```
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.80s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.58s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.53s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.30s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 21.11s
```
515/52/21/16/42 — identical to this session's own prior readings. Not
moved, as expected: this round's change set names no path any of these
five suites should be sensitive to.

**G6 THE PLAN**:
```
$ (PLAN8 extracted from committed authored file into
   .remedy-wt/plan8_extracted.bin, compared byte-for-byte against
   .agent/plan.md via a python3 -c read-and-compare — `cmp` itself was
   denied by the sandbox on this round, see Deviations)
equal: True (1786 bytes both sides)
$ wc -l .agent/plan.md
41 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
Byte-identical (equivalent to `cmp` exit 0), 41 lines (under 50), both
header counts 1 — PASS.

**G7 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked.

Per-commit numstat cross-check (the '+' column) against this
handback's own Commits table:
```
$ git show --numstat 1af43b59
490  0    .agent/authored/f262-r7.md
$ git show --numstat 3a19d064
365  202  .agent/last_block.md
$ git show --numstat 99325866
2    1    .agent/live_review.md
$ git show --numstat c7c676e3
4    2    apps/cli/command_catalog.py
12   0    apps/cli/commands/job.py
15   1    apps/cli/commands/queue_cmd.py
14   0    tests/cli/test_queue_cmd.py
22   0    tests/test_grouped_cli.py
$ git show --numstat 23cd7e21
12   10   .agent/plan.md
```
Every path and every insertion count matches the Commits table exactly
(490, 365, 2, 4+12+15+14+22=67 total for C2, 12). `git commit`'s own
printed post-commit summary differed from these `--numstat` readings
for C0b (it printed 490/327 rather than 365/202) — the same tooling
substitution already declared in rounds 1, 5 and 6's ledger entries,
applying whole-file "rewrite %" accounting once a file's dissimilarity
crosses git's display threshold, whereas `--numstat` reports the real
line-level diff; this handback's table uses the `--numstat` reading
throughout per the block's own G7 instruction.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r7.md` — NOT stale. An immutable verbatim
  record of the round's own step block; nothing to go stale.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly, which is the file's whole purpose.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE6's
  content describes round 6's own verified facts and is not asserted
  to describe anything after it.
- `apps/cli/command_catalog.py` — NOT stale. Matches PAIR J1 and
  PAIR Q1 exactly; no other CommandEntry touched; full diff read and
  confirmed.
- `apps/cli/commands/job.py` — NOT stale. Matches PAIR J2 and PAIR J3
  exactly; no other handler or dispatch line touched; full diff read
  and confirmed.
- `apps/cli/commands/queue_cmd.py` — NOT stale. Matches PAIR Q2 and
  PAIR Q3 exactly; `skipped_total`/stderr print unmoved; no other
  handler or dispatch line touched; full diff read and confirmed.
- `tests/test_grouped_cli.py` — NOT stale. New `TestJobListCLI` class
  matches the TEST SPEC's names, placement (true end of file, after
  `TestProjectListCLI`) and assertions exactly.
- `tests/cli/test_queue_cmd.py` — NOT stale. Two new test methods
  match the TEST SPEC's names, placement (end of `TestCatalog`, end of
  `TestList`) and assertions exactly.
- `.agent/plan.md` — NOT stale. Freshly written PLAN8 content
  accurately describes round 7's actual state (T002 batch 5 shipped;
  next up per PLAN8's Next Steps: the loop.list/patch.list timestamp
  design decision, the remaining 28-command audit handlers, then T003).

Constraint 8 check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` This was already declared false as of round 2 (T001
shipped) and remains outside the declared change set this round too;
T002 batch 5 shipping this round makes the sentence even further from
true, but it is still not repaired, per Constraint 8 and consistent
with rounds 2 through 6's own handling of the same sentence.

No documentation elsewhere was found to quote an exact CLI output line
for `job.list` or `queue.list` (`grep` across `docs/` for both command
names found only conceptual/scoping references, no literal printed-line
quotes), so no other staleness was introduced by this round's printer
changes.

## Authored-text proofs

- `.agent/authored/f262-r7.md` written verbatim via
  `shutil.copyfile` from `.remedy-wt/f262-r7-block.txt` (the
  reviewer's original) — the transport proof required before building
  anything on top of it (C0a).
- `.agent/last_block.md` mirrors it via a second `shutil.copyfile`,
  confirmed by matching sha256 (G1).
- GATE6 was extracted from the COMMITTED `.agent/authored/f262-r7.md`
  by a Python script reading the file in BINARY mode, locating the
  `<<<BEGIN GATE6>>>`/`<<<END GATE6>>>` marker pair by byte index, and
  taking the exact bytes strictly between them (marker lines excluded)
  — never by hand-retyping (constraint 1). GATE6: 4180 bytes, 0
  internal newlines, no trailing newline of its own. Applied to
  `.agent/live_review.md` by appending `\n` + GATE6's bytes to the base
  file — reproduced byte-identical (G2).
- PAIR J1, Q1, J2, J3, Q2 and Q3 were extracted the same way, by their
  own `<<<BEGIN PAIR_.._FROM/TO>>>` marker pairs, and applied with
  `str.replace(FROM, TO, 1)` via inline `python3 -c` scripts — never by
  hand-retyping (constraint 2). Verified per-pair in G3 above.
- PLAN8 was extracted the same way, by the `<<<BEGIN PLAN8>>>`/
  `<<<END PLAN8>>>` marker pair, 1786 bytes, last byte `.` (no
  trailing newline). `.agent/plan.md` reproduces it byte-identical
  (G6).
- The four new test functions (`test_catalog_has_json_flag` and
  `test_list_json_has_created_at` in `TestJobListCLI`;
  `test_list_has_json_flag` and `test_json_has_created_at_and_goal` in
  `test_queue_cmd.py`) were written by hand from the TEST SPEC, per
  constraint 3 — not a byte-transport slice. Verified against the spec
  field-by-field in G4 above.

## Deviations & assumptions

1. **`git commit`'s own printed rewrite-detected stat line disagreed
   with `git show --numstat` for C0b.** For a whole-file rewrite that
   crosses git's own display dissimilarity threshold, the plain
   post-commit summary showed "full old file deleted, full new file
   inserted" counts (490/327) rather than a real line-level diff.
   `--numstat` (used throughout this handback's Commits table, per the
   block's own G7 instruction) gives the real diff counts (365/202).
   Both are internally consistent and this substitution is the same
   one already declared in rounds 1, 5 and 6's own ledger entries — not
   a new finding, no committed byte affected.
2. **A commit-message typo in C1, self-corrected before push.** The C1
   commit was first written with the message
   `F262 R4 C1: append GATE6...` (a copy-paste slip from an earlier
   round's commit-message pattern seen in the session's git-status
   context) instead of `F262 R7 C1: ...`. Caught immediately, before
   any further commit or push depended on it, and corrected with
   `git commit --amend` — a message-only correction to the tip commit,
   made before any push, not a rewrite of shipped history. No file
   content was affected; the amended commit's tree and diff are
   identical to what would have been committed with the correct
   message the first time.
3. **Bash tool single-shot rejections, retried as single or
   alternate-form invocations.** Several individual Bash tool calls in
   this round (`git status --porcelain` on the very first precondition
   check, several `python3 -m py_compile` invocations, a `cmp`
   invocation, and one `ruff check` invocation before the round's own
   deliberate ruff attempt) were rejected outright by the sandbox with
   "Permission to use Bash has been denied" on the first attempt.
   `git status --porcelain` and most `python3 -m py_compile` calls
   succeeded on a bare retry with the identical command. `cmp` never
   succeeded across several retries in this round, so the byte
   comparison for G6 was done instead via a `python3 -c` script reading
   both files in binary mode and comparing them directly — an
   equivalent, exit-0-yielding substitution, not a weaker check. No
   change to intent or result in any case, only to invocation shape.
4. **Ruff's exact refusal text.** This round's `ruff check` attempt
   produced the same "Permission to use Bash has been denied..."
   sandbox denial as rounds 5 and 6's; no ruff output of any kind was
   produced.
5. **Constraint 8's stale sentence, re-declared not repaired.**
   `docs/roadmap/features/T2_F262.md` line 5 ("REGISTRATION ONLY —
   nothing in this file has been implemented") was already false as of
   round 2 and remains outside this round's declared change set, so it
   is left untouched again — see the Constraint 8 check under the
   staleness sweep above.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, before C4, and once more before writing this
handback, per constraint 9 of the block). No path outside the declared
change set was written under version control: only
`.agent/authored/f262-r7.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `apps/cli/command_catalog.py`,
`apps/cli/commands/job.py`, `apps/cli/commands/queue_cmd.py`,
`tests/test_grouped_cli.py`, `tests/cli/test_queue_cmd.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering all five files per constraint 5.

## Next

**NEXT EXPECTED ACTION: Round 8.** Per PLAN8's Next Steps:
`loop.list`/`patch.list` have no timestamp on their own model and need
a design decision before any date can appear (round 3's handback
carries the full 28-command audit). The remaining un-audited handlers
from that 28-command list (worker.list, worker.registry-list,
change.list, review.list, config.list, builder.adapter-list, the
execution.* trio) still need their own pass once T002's date coverage
stabilizes. T003 (sort/filter/limit behavior) starts once date
coverage is far enough along to sort by.

**THIS IS THE NATURAL END OF SESSION 2** (rounds 5, 6 and 7 this
session, plus round 4's review at session start). The operator's next
session should re-run Phase 0 of
`docs/agents/self_drive_protocol.md` before continuing to round 8,
rather than resuming directly from this handback.
