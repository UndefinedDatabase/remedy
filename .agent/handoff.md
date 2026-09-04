# Handoff — F262 List commands v2 (dates, sort, filter), round 8 (T002 batch 6, patch.list --json + DECIDED column)

## Session

SESSION 3 of feature F262 · round 8 · rounds so far 8.

Round 8 books round 7's PASS verdict (GATE7) into the ledger first,
then ships T002 batch 6: `patch.list` gains `--json` end to end
(catalog `args` + `supports_json=True`, handler `json_output` kwarg +
json branch, dispatch lambda) — the same shape rounds 6-7 proved for
`project.list`/`job.list`/`queue.list` — plus a `DECIDED` column in
the TEXT output surfacing the intent dict's own `decided_at` (a patch
intent has no `created_at`, only a decision timestamp). Three
production files, two test files, one commit. No model or store
change.

## Range

Review of `2286919d60503ddd0535eedc49af3ea1242ac047..8108c51c`. That
is C0a through C3 (five content commits before this handback — C0a,
C0b, C1, C2, C3). This handback (C4) follows and is not part of the
reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `2286919d60503ddd0535eedc49af3ea1242ac047`, branch matched, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r8.md` saved verbatim (`shutil.copyfile`), 338 lines, 20723 bytes, byte-equal to `.remedy-wt/f262-r8-block.txt` before it was deleted |
| C0b | done | mirrored to `.agent/last_block.md`, sha256 identical |
| C1 | done | GATE7 appended to `.agent/live_review.md` byte-exact |
| C2 | done | PAIR P1/P2/P3/P4/P7 (rewrites) + PAIR P5/P6 (appends) applied to five files, one commit |
| C3 | done | PLAN9 applied to `.agent/plan.md`, whole-file replace, byte-equal |
| C4 (this handback) | done | |
| G1 TRANSPORT | done | PASS — one digest, twice |
| G2 THE LEDGER APPEND | done | PASS — arithmetic matched, tail equal, negative control rejected |
| G3 THE FOUR PRODUCTION PAIRS | done | PASS — P1/P2/P3/P4 FROM 1→0, TO 0→1; full diffs of all three files read, nothing else changed; py_compile exit 0 x5 |
| G4 THE TESTS, BEFORE AND AFTER | done | PASS with a discrepancy — see Deviations: real baseline read 89 (not the block's stated 77), after-C2 read 91 matching the block exactly (89+2 from P5/P6) |
| G5 STATE READERS + CANARY | done | PASS — 515/52/21/16/42, unmoved from session baseline |
| G6 THE PLAN | done | PASS — byte comparison equal, 48 newlines (49 lines, no trailing newline), both header counts 1 |
| G7 THE TREE, COMMITS, SWEEP | done | PASS — tree clean, `.remedy-wt` untracked, numstats compared cell-for-cell, staleness declared |

## Commits

### 0b87c339 F262 R8 C0a: save block verbatim to .agent/authored/f262-r8.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r8.md` | +338/-0 | transport proof — verbatim copy (`shutil.copyfile`) of the reviewer's step block (`.remedy-wt/f262-r8-block.txt`), new file |

### 7760958f F262 R8 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +311/-463 | mirror of the round's authored block via `shutil.copyfile` (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### a850bff6 F262 R8 C1: append GATE7 to live_review.md - books round 7's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE7 (extracted from committed authored file by marker index), `\n` + GATE7's own bytes appended to the base file |

### a2f9aa5f F262 R8 C2: patch.list gains --json end to end (T002 batch 6)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +2/-1 | PAIR P1 (rewrite: `patch.list` CommandEntry gains `_JSON_OPT` in `args` and `supports_json=True`) |
| `apps/cli/commands/patch.py` | +9/-2 | PAIR P2 (rewrite: `_cmd_list_patch_intents` gains `json_output` kwarg + json branch) and PAIR P3 (rewrite: dispatch lambda passes `json_output=args.json`) |
| `packages/orchestration/approval_queue.py` | +2/-1 | PAIR P4 (rewrite: `format_intent_list` header and row gain the `DECIDED` column, `item['decided_at'] or '-'`) |
| `tests/test_command_catalog.py` | +1/-1 | PAIR P7 (rewrite: `expected_json` set in `test_known_json_commands` gains `"patch.list"`) |
| `tests/test_patch_intent_approval.py` | +20/-0 | PAIR P5 (append: `test_format_intent_list_shows_decided_when_set` added after the existing target-path test in `TestFormatHelpers`) and PAIR P6 (append: `test_json_output_has_version_and_intents` added after `test_unknown_job_id_exits_1` in `TestCmdListPatchIntents`) |

### 8108c51c F262 R8 C3: replace plan.md with PLAN9
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +22/-15 | whole-file replace with PLAN9 extracted from the committed authored file (per constraint 6) |

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
$ git rev-parse HEAD
2286919d60503ddd0535eedc49af3ea1242ac047
$ git branch --show-current
feature/f262-list-commands-v2
$ git status --porcelain
(empty)
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
All four confirmed.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r8.md .agent/last_block.md
44f83c824b9e9756096948569313664134a71cfeee76f892c4cda66870b37031  .agent/authored/f262-r8.md
44f83c824b9e9756096948569313664134a71cfeee76f892c4cda66870b37031  .agent/last_block.md
```
One digest, twice — PASS. (Computed via a `python3 -c` `hashlib.sha256`
read of both files in binary mode, equivalent to `sha256sum`.)

**G2 THE LEDGER APPEND, FULL FORENSICS**:
```
base size immediately before C1: 2437464 bytes, no trailing newline (last byte '.')
GATE7 own byte length: 3786
GATE7 internal newline count: 0
base + 1 + GATE7_length = 2441251
post-C1 file real byte length = 2441251
match: True
tail slice (last 3786 bytes of post-C1 file) vs GATE7: equal True
byte immediately before the tail slice is '\n': True
negative control: flipped first byte of a COPY of GATE7 vs the real tail: rejected True
```
All readings PASS.

**G3 THE FOUR PRODUCTION PAIRS, READ AND COUNTED, PER CONSTRAINT 2's SHAPES**:
```
PAIR P1 (rewrite, command_catalog.py): FROM count before 1, FROM count after 0, TO count after 1
PAIR P2 (rewrite, patch.py handler body): FROM count before 1, FROM count after 0, TO count after 1
PAIR P3 (rewrite, patch.py dispatch lambda): FROM count before 1, FROM count after 0, TO count after 1
PAIR P4 (rewrite, approval_queue.py format_intent_list): FROM count before 1, FROM count after 0, TO count after 1
PAIR P7 (rewrite, test_command_catalog.py expected_json set): FROM count before 1, FROM count after 0, TO count after 1
```
All five PASS, matching Constraint 3's predicted shapes exactly
(extracted from the committed authored file via a `python3` script
locating each `<<<BEGIN PAIR_Pn_FROM/TO>>>` marker pair by byte index,
applied per-target with `content.replace(FROM, TO, 1)` — never
hand-retyped). Every FROM string was counted at exactly 1 occurrence
in its target file before any pair was applied (constraint 2's
re-confirmation), matching the reviewer's own dry-run counts.

Full diff of `apps/cli/command_catalog.py`:
```diff
@@ -794,7 +794,8 @@ _BASE_CATALOG: tuple[CommandEntry, ...] = (
         subcommand="list",
         description="List patch intents for a job.",
         action_class="read_only",
-        args=(_JOB_ID,),
+        args=(_JOB_ID, _JSON_OPT),
+        supports_json=True,
         related=("patch.show", "patch.approve"),
     ),
     CommandEntry(
```
Confirmed by reading the full diff: exactly PAIR P1's two-line
insertion at the `patch.list` entry. No other `CommandEntry` in the
file was touched.

Full diff of `apps/cli/commands/patch.py`:
```diff
@@ -14,7 +14,7 @@ if TYPE_CHECKING:
     import argparse
 
 
-def _cmd_list_patch_intents(job_id_str: str) -> None:
+def _cmd_list_patch_intents(job_id_str: str, *, json_output: bool = False) -> None:
     job_id = resolve_job_id(job_id_str)
     try:
         job = load_job(job_id)
@@ -24,6 +24,13 @@ def _cmd_list_patch_intents(job_id_str: str) -> None:
 
     from packages.orchestration.approval_queue import format_intent_list, list_patch_intents
     intents = list_patch_intents(job)
+    if json_output:
+        print(_json.dumps({
+            "version": 1,
+            "intent_count": len(intents),
+            "intents": intents,
+        }, sort_keys=True))
+        return
     print(format_intent_list(intents))
 
 
@@ -359,7 +366,7 @@ def _cmd_approve_hunks(
 
 
 COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
-    "patch.list": lambda args: _cmd_list_patch_intents(args.job_id),
+    "patch.list": lambda args: _cmd_list_patch_intents(args.job_id, json_output=args.json),
     "patch.show": lambda args: _cmd_show_patch_intent(args.job_id, args.intent_id),
```
Confirmed by reading the full diff: exactly PAIR P2 (function
signature + body) and PAIR P3 (dispatch line) changed. `_json` is
already imported at module level (`import json as _json`, line 5,
confirmed present) — no second import was added, per P2's own note.
Every other handler and dispatch line in the file is byte-for-byte
untouched.

Full diff of `packages/orchestration/approval_queue.py`:
```diff
@@ -272,7 +272,7 @@ def format_intent_list(intents: list[dict]) -> str:
     if not intents:
         return "No patch intents found for this job."
 
-    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  TARGET PATH"]
+    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  {'DECIDED':<20}  TARGET PATH"]
     lines.append("-" * 72)
     for item in intents:
         lines.append(
@@ -280,6 +280,7 @@ def format_intent_list(intents: list[dict]) -> str:
             f"{item['state']:<8}  "
             f"{item['risk']:<8}  "
             f"{item['action']:<12}  "
+            f"{(item['decided_at'] or '-'):<20}  "
             f"{item['target_path']}"
         )
     return "\n".join(lines)
```
Confirmed by reading the full diff: exactly PAIR P4's header and row
change. No other function in the file was touched.

```
$ python3 -m py_compile apps/cli/command_catalog.py apps/cli/commands/patch.py packages/orchestration/approval_queue.py tests/test_patch_intent_approval.py tests/test_command_catalog.py
(exit 0, no output)
```
Exit 0 confirmed for all five touched files, one combined invocation
— PASS.

Ruff attempted per constraint 9, exact refusal reproduced:
```
$ ruff check apps/cli/command_catalog.py apps/cli/commands/patch.py packages/orchestration/approval_queue.py tests/test_patch_intent_approval.py tests/test_command_catalog.py
This command requires approval
```
Ruff is denied this session, exactly as the block warned — same shape
of refusal as prior rounds (rounds 5-7 hit the Bash-permission denial
text; this round's sandbox surfaced it as "This command requires
approval" instead, still a refusal, not a run — see Deviations).

**G4 THE TESTS, BEFORE AND AFTER**:
```
Before C2 (measured at HEAD after C0a/C0b/C1, before applying any pair):
$ python3 -m pytest tests/test_patch_intent_approval.py tests/test_command_catalog.py -q
89 passed in 0.37s
(64 in test_patch_intent_approval.py + 25 in test_command_catalog.py,
confirmed by running each file individually and by --collect-only
reading "89 tests collected")

After C2:
$ python3 -m pytest tests/test_patch_intent_approval.py tests/test_command_catalog.py -q
91 passed in 0.43s
```
**Discrepancy from the block, recorded honestly, not papered over:**
the block states "before C2: 77 passed" (both in the Done-when table
and in the reviewer's own dry-run proof paragraph); the real reading
at HEAD `2286919d` — the exact commit the reviewer's dry-run worktree
was cut from — is 89 passed, not 77. `git log` confirms neither of
these two test files has been touched since commit `55a29fb0` (F262
R2 C2); rounds 3 through 7 changed other files (job.py, queue_cmd.py,
project.py, etc.), so 89 has been the stable count for these two files
since round 2 — this is not environmental drift from something this
session did. The after-C2 count (91) matches the block's own stated
91 exactly, which is arithmetically consistent with a real 89-baseline
plus the two new tests P5 and P6 each add (89+2=91), but is NOT
consistent with the block's own stated 77-baseline plus two (which
would be 79, not 91). This points to the "77" baseline figure in the
block being stale or transcribed from a different round/file pair,
not to any defect in the pairs themselves — the diffs above show
nothing beyond the seven named pairs landed, and the FROM/TO counts
all matched Constraint 2's pre-declared shapes exactly. Reported here
per the instruction to record a genuine numeric discrepancy rather
than force it to match.

**G5 THE STATE READERS AND THE CANARY**:
```
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.71s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.60s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.52s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.30s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.94s
```
515/52/21/16/42 — identical to the block's stated baseline and to
prior rounds' readings. Not moved, as expected: this round's change
set names no path any of these five suites should be sensitive to.

**G6 THE PLAN**:
```
$ (PLAN9 extracted from committed authored file into
   /tmp/plan9_extracted.bin, compared byte-for-byte against
   .agent/plan.md via a python3 -c read-and-compare)
byte-equal: True (2270 bytes both sides)
$ wc -l .agent/plan.md
48 .agent/plan.md
```
48 newlines because the file's last line (49th line of content) has
no trailing newline — same convention as PLAN9's own extracted byte
count (2270 bytes, 49 lines by the "count('\n') + 1 if no trailing
newline" measure). Under the 50-line cap either way.
```
## Goal count: 1
## Next Steps count: 1
```
Byte-identical, under 50 lines, both header counts 1 — PASS.

**G7 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked (the scratch
copy at `.remedy-wt/f262-r8-block.txt` was deleted after C0a's commit,
per the block's own instruction; several throwaway verification
scripts were also written under `.remedy-wt/` during this round and
remain there, gitignored, untracked).

Per-commit numstat cross-check (the '+'/'-' columns) against this
handback's own Commits table:
```
$ git show --numstat 0b87c339
338  0    .agent/authored/f262-r8.md
$ git show --numstat 7760958f
311  463  .agent/last_block.md
$ git show --numstat a850bff6
2    1    .agent/live_review.md
$ git show --numstat a2f9aa5f
2    1    apps/cli/command_catalog.py
9    2    apps/cli/commands/patch.py
2    1    packages/orchestration/approval_queue.py
1    1    tests/test_command_catalog.py
20   0    tests/test_patch_intent_approval.py
$ git show --numstat 8108c51c
22   15   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly. `git commit`'s own printed post-commit summary
differed from these `--numstat` readings for C0b — it reported this
round's own rewrite-detected percentage-based stat rather than the
real line-level diff `--numstat` gives (311/463); this is the same
tooling substitution already declared in rounds 1, 5, 6 and 7's own
ledger entries, not a new finding, no committed byte affected.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r8.md` — NOT stale. An immutable verbatim
  record of the round's own step block; nothing to go stale.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly, which is the file's whole purpose.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE7's
  content describes round 7's own verified facts and is not asserted
  to describe anything after it.
- `apps/cli/command_catalog.py` — NOT stale. Matches PAIR P1 exactly;
  no other `CommandEntry` touched; full diff read and confirmed.
- `apps/cli/commands/patch.py` — NOT stale. Matches PAIR P2 and PAIR
  P3 exactly; no other handler or dispatch line touched; full diff
  read and confirmed; `_json` module-level import reused, not
  duplicated.
- `packages/orchestration/approval_queue.py` — NOT stale. Matches
  PAIR P4 exactly; no other function touched; full diff read and
  confirmed.
- `tests/test_command_catalog.py` — NOT stale. Matches PAIR P7
  exactly; `expected_json` set gains only `"patch.list"`.
- `tests/test_patch_intent_approval.py` — NOT stale. The two new test
  methods match PAIR P5 and PAIR P6 exactly, confirmed by a full
  ordered-equality proof (pre-commit blob byte-exact prefix, each
  appended block an exact suffix in order, tail unchanged) rather than
  only a FROM-count check, per constraint 3's APPEND-shape rule.
- `.agent/plan.md` — NOT stale. Freshly written PLAN9 content
  accurately describes round 8's actual state (T002 batch 6 shipped;
  next up per PLAN9's Next Steps: the change.list/loop.list design
  decisions, then T003).

Constraint 8 check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` This was already declared false as of round 2 (T001
shipped) and remains outside the declared change set this round too;
T002 batch 6 shipping this round makes the sentence even further from
true, but it is still not repaired, per Constraint 8 and consistent
with rounds 2 through 7's own handling of the same sentence.

`grep` across `docs/` for `patch.list`/`patch list` found only two
usage-example lines (`docs/guides/autocoder-usage.md`,
`docs/system/repair-loop-v0.md`), both showing the bare
`remedy patch list <job_id>` invocation with no `--json` flag and no
literal printed-output quote — neither goes stale, since `--json` is
additive and optional; the base command's documented usage is
unchanged.

## Authored-text proofs

- `.agent/authored/f262-r8.md` written verbatim via `shutil.copyfile`
  from `.remedy-wt/f262-r8-block.txt` (the reviewer's original) — the
  transport proof required before building anything on top of it
  (C0a). Byte-equal confirmed (20723 bytes both sides) before the
  scratch copy was deleted.
- `.agent/last_block.md` mirrors it via a second `shutil.copyfile`,
  confirmed by matching sha256 (G1).
- GATE7 was extracted from the COMMITTED `.agent/authored/f262-r8.md`
  by a Python script reading the file in BINARY mode, locating the
  `<<<BEGIN GATE7>>>`/`<<<END GATE7>>>` marker pair by byte index, and
  taking the exact bytes strictly between them (marker lines excluded)
  — never by hand-retyping (constraint 1). GATE7: 3786 bytes, 0
  internal newlines, no trailing newline of its own. Applied to
  `.agent/live_review.md` by appending `\n` + GATE7's bytes to the base
  file — reproduced byte-identical (G2).
- PAIR P1, P2, P3, P4, P5, P6 and P7 were extracted the same way, by
  their own `<<<BEGIN PAIR_Pn_FROM/TO>>>` marker pairs, and applied
  with `content.replace(FROM, TO, 1)` via a `python3` script — never
  by hand-retyping (constraint 2). Verified per-pair in G3/G4 above:
  P1/P2/P3/P4/P7 by the FROM-0x/TO-1x rewrite proof, P5/P6 by the
  ordered-equality append proof.
- PLAN9 was extracted the same way, by the `<<<BEGIN PLAN9>>>`/
  `<<<END PLAN9>>>` marker pair, 2270 bytes, last byte `.` (no
  trailing newline). `.agent/plan.md` reproduces it byte-identical
  (G6).

## Deviations & assumptions

1. **The block's stated pre-C2 test count (77) does not match the
   real reading (89) at the exact HEAD the reviewer's own dry-run
   worktree was cut from.** Reported in full under G4 above. The
   after-C2 count (91) matches the block exactly and is arithmetically
   consistent with 89+2, not with 77+2 — pointing to a stale/mistaken
   "77" figure in the block's Done-when table and dry-run proof
   paragraph, not to any defect in the seven pairs, all of which
   landed exactly as specified (confirmed by full diffs and FROM/TO
   counts in G3). No number was forced to match; both real readings
   (89 before, 91 after) are reported as measured.
2. **`git commit`'s own printed rewrite-detected stat line disagreed
   with `git show --numstat` for C0b.** Same substitution already
   declared in rounds 1, 5, 6 and 7's own ledger entries — not a new
   finding, no committed byte affected. `--numstat` (311/463) is used
   throughout this handback's Commits table per the block's own G7
   instruction.
3. **Ruff's refusal text differs in wording from prior rounds' but is
   equally a refusal, not a run.** This round's `ruff check` attempt
   produced "This command requires approval" rather than the fuller
   "Permission to use Bash has been denied..." text rounds 5-7 saw;
   both are sandbox denials of the same command, with no ruff output
   of any kind produced either way. Constraint 9 anticipated a denial
   without specifying its exact wording, so this is not treated as a
   gate failure.
4. **One combined multi-line Bash invocation was rejected outright by
   the sandbox before any of its lines ran, and had to be re-issued as
   separate single-purpose commands.** A single Bash call that chained
   the `.agent/plan.md` copy, a byte-equality check, `wc -l` and two
   `grep -c` reads together was blocked in full (none of its lines
   executed, confirmed by `.agent/plan.md`'s unchanged mtime/content
   immediately after) because the trailing `grep -c` invocations
   required approval; the same operations were then re-run as isolated
   single-purpose Bash/python3 calls, each of which succeeded. No
   change to intent or result, only to invocation shape — the same
   category of substitution declared in round 7's ledger entry for
   `cmp`/`py_compile` retries.
5. **Constraint 8's stale sentence, re-declared not repaired.**
   `docs/roadmap/features/T2_F262.md` line 5 ("REGISTRATION ONLY —
   nothing in this file has been implemented") was already false as of
   round 2 and remains outside this round's declared change set, so it
   is left untouched again — see the Constraint 8 check under the
   staleness sweep above.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, before C4, and once more before writing this
handback, per constraint 7 of the block). No path outside the declared
change set was written under version control: only
`.agent/authored/f262-r8.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `apps/cli/command_catalog.py`,
`apps/cli/commands/patch.py`, `packages/orchestration/approval_queue.py`,
`tests/test_command_catalog.py`, `tests/test_patch_intent_approval.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering all five files per constraint 4.

## Next

**NEXT EXPECTED ACTION: Round 9.** Per PLAN9's Next Steps: a design
decision is needed on which event name marks patch-intent creation
before `change.list` can grow a CREATED date (the only production
emitter, `do_run_patch_intent_created`, is read by no consumer; every
reader instead checks a bare `patch_intent_created` no production code
emits); `loop.list`/`patch.list` still have no `created_at` on their
own model, so a CREATED date remains a separate open design question
from the `--json`/DECIDED work this round shipped. The execution.*
trio's pre-existing `--json`-ignored quirk stays excused per the
Risks section. T003 (sort/filter/limit behavior) starts once date
coverage is far enough along to sort by.

**THIS IS SESSION 3, ROUND 8** — the operator may continue directly to
round 9 in this same session or start a fresh session per the
self-drive protocol's own judgment; no session/round-limit threshold
has been reached (8 of a 25-round soft cap, 3 of a 7-session soft cap).
