--- STEP Closure C3 — F044 ---
ROUND 13. The closure sequence's third round: the integration gate
(docs/roadmap/STATUS_closure_protocol.md precondition 2; operator
amendment amend0917-throughput, docs/agents/self_drive_protocol.md).
Book round 12, then run the feature's ONE full suite pass.

Goal: produce the one, only, full-suite reading this feature is allowed
(amend0917-throughput rule 1: "THE FULL SUITE RUNS EXACTLY ONCE PER
FEATURE, in the closure sequence's integration-gate round, by the
WORKER, in the primary checkout"), committed as a real transcript the
reviewer reads rather than re-runs.

Bundle:
1. Book F044 round 12 into `.agent/live_review.md` (the `Gate: F044
   R12 —` paragraph) from the `records.diff` payload below, verbatim,
   no retyping; rewrite `.agent/plan.md` from the `plan.md` payload.
2. Run `python3 -m pytest -n auto -q` from the primary checkout, timing
   it yourself with a wrapper (`time.monotonic()` around the
   `subprocess.run`, or the shell's own `time`). Write
   `.agent/authored/f044-closure-suite.txt` in EXACTLY this shape (the
   format every prior closure's own file already uses — read
   `.agent/authored/f043-closure-suite.txt` first so you match it
   exactly):
   ```
   command: python3 -m pytest -n auto -q
   real exit code: <the process's own exit code>
   wall time: <your wrapper's reading>s (measured wrapper); pytest's own reported wall time <pytest's own "in Ns" reading>s (<pytest's own H:MM:SS if it printed one>)
   summary line: <pytest's own final summary line, verbatim>
   bad node ids (failed + errors): <NONE, or every failed/errored node id, one per line, indented two spaces, each prefixed "- ">
   tree it ran on: <your own HEAD's short sha> (<your own HEAD commit's subject line>)
   ```
   Commit this file ALONE, its own commit — nothing else in the same
   commit, so a later reader can find the transcript by commit message
   alone.

Change: exactly `.agent/live_review.md`, `.agent/plan.md` and
`.agent/authored/f044-closure-suite.txt` (plus the two payload copies
under `.agent/authored/f044-r13-*` Bundle item 1 already covers) —
nothing else. If the suite is RED, you STILL commit the transcript
exactly as read — do not retry, do not investigate, do not fix
anything this round; a repair, if one is needed, is the NEXT round's
own reviewer-authored block, built from what this transcript actually
says. Report the real reading either way.

Constraints:
- Never retype a payload. Copy the two below into
  `.agent/authored/f044-r13-<name>` with `shutil.copyfile`, verbatim,
  before using it; measure each saved copy's line count, byte count and
  sha256 and compare against the table below before applying it.
- `records.diff` is a unified diff: run `git apply --check
  <path-to-authored-copy>` from the repo root before the real `git
  apply` (it is the round's bookkeeping and AGENTS.md's Commit Gate
  item 1 requires `.agent/plan.md` current before every commit that
  follows it). `plan.md` is a REWRITE of `.agent/plan.md` (AGENTS.md:
  rewrite, never append) — copy the authored `plan.md` payload over
  `.agent/plan.md` with `shutil.copyfile` in the SAME commit as
  `records.diff`'s apply.
- The suite runs with NO markers, no `-k`, no path filter — the
  literal `python3 -m pytest -n auto -q` the closure protocol names.
  Do not add `--timeout`, do not add `-x`. Let it run to completion.
- No disposable worktree: the suite runs in the PRIMARY checkout, per
  amend0917-throughput rule 1 itself ("never a worktree, which lacks
  the UI dependencies").
- Commit subjects: no leading-slash tokens, no absolute paths.
- Self-review loop (AGENTS.md) before every commit: `git diff --stat`
  then `git diff`, read what changed, confirm it matches this step,
  only then commit.
- COMMIT TRAILER — every commit of this round ends with exactly this
  line, verbatim: `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report
   the reading.
2. Your shell must be in the primary checkout,
   `/home/decodeux/Repos/remedy`; report `pwd`. `git status --porcelain`
   must be empty, `git branch --show-current` must read
   `feature/f044-command-palette`, and `git log --oneline -1` must read
   `21123e307`. Report all three.
3. Report `git worktree list | wc -l` as found (expect 11 — unchanged
   by this round).

PAYLOADS — the reviewer-authored originals already exist on disk,
untouched by you, at `.remedy-wt/f044-r13-payloads/<file>` (this
session's in-session digest-fallback transport,
docs/agents/self_drive_protocol.md: "in-session there is no transport,
so the hash-stamp ritual is replaced by a cmp of the applied file
against the authored original"). Copy each with `shutil.copyfile` (never
open-and-retype, never an editor) to `.agent/authored/f044-r13-<file>`.
Verify every one's line count, byte count and sha256 BEFORE using it and
report every reading; never retype, never edit.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 10 | 7362 | b593607be78d84e9d44a9748539f075d771f4f141b40971a38182b5d9b78a7ed |
| plan.md | 35 | 1291 | 1c6d24a57538932f15927d38f393e54bc10f90a7d19a6b566b37b08d3b233b62 |

`records.diff` touches `.agent/live_review.md` only: the `Gate: F044
R12 —` paragraph, appended. `plan.md` is the full replacement text for
`.agent/plan.md` (35 lines, under the 50-line cap).

Suggested commit sequence (small, self-reviewed, each ends with the
trailer):
C1 — copy `block.md` (this text, saved by you as you received it) and
  `plan.md` into `.agent/authored/`.
C2 — copy `records.diff` into `.agent/authored/`.
C3 — `git apply` the authored `records.diff`; copy the authored
  `plan.md` over `.agent/plan.md`. First substantive commit of the round
  (AGENTS.md Commit Gate item 1; §3 pre-emission item 23).
C4 — run the full suite; write and commit
  `.agent/authored/f044-closure-suite.txt` alone.
C5 — handback: rewrite `.agent/handoff.md`, push.

Done when (run every command yourself; report the real exit code and the
literal output, never the word "green"):

G1 TRANSPORT — for each of the two payloads, report the line count,
byte count and sha256 you measured of the file you saved under
`.agent/authored/f044-r13-<name>`, beside the table above; both must
match exactly. Also report the line count, byte count and sha256 of
your own saved `.agent/authored/f044-r13-block.md` (the text of this
step, saved as you received it): the reviewer holds its own reading of
the same text and compares it at review time (R-0954).

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r13-
records.diff` then the real apply, both exit 0; `.agent/plan.md` read
back and compared byte-for-byte against `.agent/authored/f044-r13-
plan.md` (must be identical). Report `.agent/live_review.md`'s byte
length (`len(path.read_bytes())`) at your own C2 commit's tree (before
applying `records.diff`), and again after C3, and confirm the
post-apply length equals the pre-apply length plus the appended `Gate:
F044 R12 —` paragraph's own length from the table's `records.diff`
accounting — state both readings and the arithmetic explicitly.

G3 THE SUITE ITSELF — the real, complete output of `python3 -m pytest
-n auto -q`: its exit code, its own final summary line verbatim, and
the full list of any failed or errored node ids (or `NONE`). Report
`.agent/authored/f044-closure-suite.txt`'s own line count, byte count
and sha256 after you commit it, and confirm every field in it (exit
code, summary line, bad node ids, tree sha) matches what you actually
observed running the command — never a value copied from this block or
from any prior round's file.

G4 INTEGRITY — run in the primary checkout: `python3 -m apps.cli.main
integrity check --json` reads `"fail_count": 0` and `"ok": true`
REGARDLESS of the suite's own G3 outcome (integrity checks a different
set of things; a red G3 does not excuse a red G4, and a green G4 does
not excuse a red G3 — report both honestly, separately).

G5 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` passes
at exit 0 (AGENTS.md / §3 verification tiers, every handback) — this is
a SEPARATE, targeted run from G3's full suite, not a substitute for it
and not redundant with it (G3 already contains this file's own nodes,
but the canary is reported on its own per every prior round's own
convention).

Handback: completion report (changed-files table with +/- per commit,
verification results with real output, item-status table for Bundle
items 1-2, the full contents of `.agent/authored/f044-closure-suite.txt`
quoted verbatim) + rewrite `.agent/handoff.md` naming SESSION 4, round
13, the next step (the evidence bundle if G3 was green, or a repair
round naming every bad node id if it was not), and any deviation.
--- END STEP ---
