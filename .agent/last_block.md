── STEP T002b interlude — F085 — R35 ─────────────────────────────────────────

Goal: record the R34 PASS, and register AND resolve R-0525 — a resolution that
located landed text in `.agent/handoff.md`, a path this workflow rewrites every
round — by naming those paths in checklist item 20 so a slice locating landed text
in one of them carries the SHA that holds it.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 narrow
checklist item 20 · C2 record R34 and register and resolve R-0525 · C3 plan ·
C4 handback.

## Why this round exists — read before C1

R34 PASSED. The reviewer re-ran G1-G7 over 7480d880..6ca30b16 and every one
reproduces the handback's reading, transport proved against the reviewer's own
scratch original rather than a digest. R34's worker did the thing this round exists
to reward: it found a sentence of the reviewer's own slice that its own C4 falsified,
declared it in the handback, and did NOT edit the slice it was told to apply
byte-verbatim.

The sentence is R-0523's resolution, which says the false R33 proof "stays in
`.agent/handoff.md` where it landed". C4 of R34 rewrote that file, so at 6ca30b16 the
path does not hold the sentence; commit 7480d880's version of it does. The referent
is recoverable, because the registration two paragraphs above names 7480d880 — which
is why this is Low and not a block condition.

What it exposes is a gap in R-0524's own carve-out, one round old. That carve-out lets
a slice name an ordering constraint instead of a SHA when it describes THIS round's
change. This sentence does something else: it locates a PRIOR round's text by path
alone. For most paths that is fine. For the handful this workflow rewrites at every
single round it is never fine, because the rewrite is scheduled rather than possible —
`.agent/handoff.md` is rewritten by the last commit of every round by construction, so
a bare path reference to it is stale before the round it was written in has ended.
Naming those paths is the whole counter-measure; no new obligation reaches any other
file.

This round changes no production code, so it orders no red proof and no ruff run.

## Change

C1 — `docs/agents/planner_reviewer_prompt.md`, one commit, the I20F→I20T pair, which
extends checklist item 20 in place. No item is added, removed or renumbered.

C2 — `.agent/live_review.md`, one commit, RECORD3 appended and nothing else. RECORD3
carries the R34 gate entry, then the R-0525 registration, then its resolution, as one
slice.

C3 — `.agent/plan.md`, one commit, the PLANF3→PLANT3 pair over the Current Step block
alone. Next Steps is untouched; the migration order did not change.

Change set, named rather than counted: `docs/agents/planner_reviewer_prompt.md`,
`.agent/authored/f085-r35.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md` and `.agent/handoff.md`. Nothing else is touched.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r35.md` by its marker pair. Never retype a slice,
   never apply one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test and recorded as
   the test's OUTPUT, one reading per pair — the form checklist item 15 has required
   since 6ca30b16:
   I20F→I20T — TO contains FROM: true — APPEND.
   PLANF3→PLANT3 — TO contains FROM: false — REWRITE.
   For the APPEND pair the "FROM 0x after" count is unattainable by construction and
   is NOT ordered; §4.9's append obligation is ordered instead. Do not report a
   FROM-zero reading for it under any wording.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This
   round orders no destructive check, so it creates no worktree; `git worktree list`
   is one line throughout.
5. C2 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD3. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round registers and
   resolves R-0525 and touches no other id, so the open count must come out
   unchanged.
7. If any gate comes out red, or a FROM does not match at exactly one place in the
   file it is applied to, STOP: write the handback naming the exact command, its exit
   code and its output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no
   sentence this round put on disk was falsified by a later commit of the same round,
   and that no slice quotes another file's current wording as a claim. Name what was
   re-read. RECORD3 states facts about `docs/agents/planner_reviewer_prompt.md` and
   `.agent/live_review.md`, both of which this block edits. Every reading RECORD3
   asserts about a state BEFORE this round names the SHA 6ca30b16 or an earlier one;
   every claim about a state this round CREATES names constraint 9. RECORD3 refers to
   `.agent/handoff.md` only with the SHA that holds the text it means — that is the
   rule this round lands, applied to itself.
9. The commit order C1 before C2 is load-bearing: it is what makes RECORD3's claim
   about the extended item 20 true when it is written, and what licenses RECORD3 to
   use the item-20 carve-out. Do not reorder.
10. Do not "repair" any landed text. `.agent/handoff.md` is rewritten by C4 in the
    normal way; R-0523's imprecise sentence is corrected by RECORD3's registration,
    not by editing `.agent/live_review.md` — the R-0521 principle.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r35.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report the sha256, the
byte count, the line count, the number of marker lines, and region digests over the
line ranges 1-100, 101-200 and 201-end, each digest taken over those lines with their
trailing newlines included. Do not compute any of those numbers by hand; measure
them.

G3 APPEND SHAPE for C2. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank line
plus RECORD3; RECORD3 is an exact suffix of the post-commit file; RECORD3's first
line occurs once among the lines that commit's diff ADDS; 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker LINES, never the substring,
because the quoted regex already appears in that file's prose. Report
`git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base 6ca30b16 and at HEAD, taking registered from
`^- R-\d{4} — `, done from `^Done: R-\d{4} — ` and landed from `^Landed: R-\d{4}`.
The reviewer's base reading is 139 registered / 21 done / 0 landed, 118 open, max
registered R-0524 and max resolved R-0524; at HEAD it must be 140 / 22 / 0 with 118
open again and both maxima R-0525. Report the registered symmetric difference and the
done symmetric difference (each must hold exactly R-0525), the landed symmetric
difference (empty), the count of duplicate ids, the count of resolutions naming an
unregistered id, the maximum id, and the next free id, which moves from R-0525 to
R-0526.

G5 THE NARROWING LANDED, measured at HEAD after C1, and the APPEND obligation. In
`docs/agents/planner_reviewer_prompt.md`:
- the I20F text still occurs exactly once, because the pair is APPEND-shaped and its
  FROM survives by construction;
- the item-15 opener
  `  15. **Pair shapes are classified by a containment test, never by eye.** Finding`
  and the item-20 opener
  `  20. **A slice states a fact about a file the same block edits only with the commit`
  and the closing paragraph opener
  `  Why this is on disk and not a habit: item 2 has recurred six times across`
  each still occur exactly once, because this commit extends one item rather than
  adding, removing or renumbering any;
- every line I20T adds that I20F does not contain occurs exactly once AMONG THE LINES
  C1's DIFF ADDS — that is the §4.9 append obligation, ordered INSTEAD of a FROM-zero
  count;
- 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached the file.
Report `git show --numstat` for C1.

G6 STATE READERS AND DOCS. This round changes no production code, so it orders no
ruff run and no red proof. Because it rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`159 passed`. RUN IT IN THE PRIMARY CHECKOUT AND NEVER IN A WORKTREE: R-0518 records
why, and a red naming `TestVitestFrontendTestFoundation::test_vitest_passes` with
`apps/ui/node_modules` absent IS that finding rather than a regression. Any other red
is a STOP under constraint 7. Because a file under `docs/` changes:
`python3 -m pytest tests/docs/ -q` exits 0, base reading `295 passed`. Do NOT read
that green as evidence about C1: the reviewer ran the red control in a disposable
worktree at 7480d880 and, with `docs/agents/planner_reviewer_prompt.md` replaced by
the single line `# broken`, the suite still returned `295 passed`. No test under
`tests/docs/` reads that file, so this gate covers the README index and roadmap
consistency and is BLIND to C1 by construction. G5 is the only check on C1's content.
CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`.

G7 COMMIT HYGIENE. `git diff --name-only 6ca30b16..HEAD` measured BEFORE C4 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which C4
writes, and nothing else. Report per-commit insertions for every commit BEFORE C4 —
C4 cannot measure itself, so report its own insertions in the round report instead —
and confirm none exceeds 500. Confirm every commit has exactly one parent and that
`git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA 6ca30b16, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G7 with
exit codes, the open-findings count, and the next expected action. In the
`## Authored-text proofs` section, report each pair under the shape constraint 2
assigns it and NEVER report a FROM-zero count for an APPEND pair. Repeat this
Fortschritt line verbatim:
Fortschritt: ~70 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34
PASS · T002a KOMPLETT · T002b 9 von 12 Sites auf dem Seam, 3 offen · T002c-d, T003
offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open
PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). It
MUST also state that R35's own verdict is NOT a §4.13 terminator because this branch
continues, and that the next reviewed round records R35's gate entry in
`.agent/live_review.md`.

The `## Next` section MUST additionally carry this migration design verbatim, because
it was derived by the reviewer at 6ca30b16 and would otherwise be re-derived wrongly:

  The next MIGRATION round takes the default `runner` closure in
  `packages/orchestration/mission_state.py` — at 6ca30b16 it is the
  `subprocess.run(argv, cwd=..., capture_output=True, text=True, timeout=900)` call
  inside `if runner is None:`, and it is the capture-and-timeout shape already
  migrated at `pingpong_loop.py`, `test_runner.py`, `job_promote.py` and
  `integrity_gate.py`.
  The import MUST be added at MODULE level, not inside the closure. Every existing
  seam test intercepts the call with
  `monkeypatch.setattr(<module>, "run_guarded_test_command", _fake_guarded)`
  (`tests/orchestration/test_pingpong.py`, `test_integrity_gate.py`,
  `test_job_promote.py` at 6ca30b16), and that patch cannot reach a name bound by a
  function-local import — a local import would leave the site untestable by the
  established pattern while every gate stayed green.
  The reviewer checked the cycle at 6ca30b16: `packages/orchestration/exec_guard.py`
  contains no reference to `mission_state`, so a module-level import adds no cycle.
  The seam returns BYTES while this closure has always returned `str`, so the decode
  `(proc.stdout or b"").decode("utf-8", "replace") + (proc.stderr or b"").decode(
  "utf-8", "replace")` is part of the change, matching `pingpong_loop.py` at 6ca30b16.
  `builder_bridge.py` still comes LAST and stays BLOCKED until the seam can SET an
  environment value rather than only allowlist a key.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-I20F
      reaches a claim about the round's OWN commits and nothing else, and a reading of
      any PRIOR state still names its SHA.
END-I20F

BEGIN-I20T
      reaches a claim about the round's OWN commits and nothing else, and a reading of
      any PRIOR state still names its SHA.
      Finding R-0525 closes the other side of the same gap. A slice that merely LOCATES
      landed text names the SHA of the commit holding it whenever the path is one this
      workflow rewrites every round — `.agent/handoff.md`, `.agent/plan.md`,
      `.agent/last_block.md`, `.agent/context.md`. For those the rewrite is SCHEDULED
      rather than possible: the last commit of every round rewrites the handback by
      construction, so a bare path reference to one of them is stale before the round
      that wrote it has ended, and no ordering constraint can rescue it. Elsewhere a
      bare path is fine, and this clause deliberately reaches no further. R-0525 is the
      carve-out above being read too widely one round after it landed: it licenses an
      ordering constraint in place of a SHA for a claim about the round's OWN change,
      and a sentence locating a PRIOR round's text is not that claim.
END-I20T

BEGIN-RECORD3
Gate: R35 — the R34 entry. R34 PASSED: the repair round that registered and resolved
R-0522, R-0523 and R-0524 — a pair labelled REWRITE while its TO contained its FROM,
the false rewrite proof that label produced, and the slice class item 20's required
SHA cannot reach. Every ordered gate was re-run by the reviewer over
7480d880..6ca30b16 and each reproduces the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL, not only against a digest: the scratch file the
block was authored into, the committed `.agent/authored/f085-r34.md`, the committed
`.agent/last_block.md` and both working copies are all five byte-EQUAL at sha256
42bf5eeb4bd3725848d7f824912827a9bff4948a18dd2f6cf13bc6caec46835b, 24167 B, 373 lines,
14 marker lines, region digests 2764ed2a, 6fe4a6ca and 2b83c685 — and that digest is
the one the reviewer measured BEFORE emission, so the block the worker applied is the
block the reviewer wrote. THE APPEND COMMIT HELD ITS SHAPE: 2342ed97's pre-commit blob
373548 B is a byte-exact PREFIX of the 381289 B post-commit file, the remainder is
7741 B = one blank line plus RECORD2, RECORD2 is an exact suffix, its first line
occurs once among the 104 lines that commit adds, numstat 104/0, 0 lines match
`^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 9 times. THE ARITHMETIC
MOVED IN BOTH SETS BY THE SAME THREE IDS: 136 registered / 18 done / 0 landed at
7480d880 against 139 / 21 / 0 at 6ca30b16, 118 open at both ends, registered and done
symmetric differences each exactly R-0522, R-0523 and R-0524, landed symmetric
difference empty, no duplicate id, no resolution naming an unregistered id, and next
free R-0525. THE NARROWINGS LANDED AS APPENDS AND WERE PROVED AS APPENDS: at 6ca30b16
the I15 and I20 FROM texts each still occur exactly once, which is what an
append-shaped pair guarantees and what R33's handback wrongly denied of its own pair;
the item-15, item-16 and item-20 openers and the checklist's closing paragraph each
occur exactly once; every one of the 24 lines the two TOs add that their FROMs do not
contain occurs exactly once among the 24 lines c15798a8 adds; 0 marker lines reached
the file; numstat 24/0. THE SUITES WERE RE-RUN, NOT READ: the four state readers
`159 passed`, the docs suite `295 passed` and the canary `42 passed`, each as its
exact ordered command line in the primary checkout, each exit 0. THE DOCS GATE IS
BLIND TO THE CHECKLIST EDIT AND WAS NOT COUNTED AS EVIDENCE FOR IT: the reviewer ran
the red control in a disposable worktree at 7480d880 with
`docs/agents/planner_reviewer_prompt.md` cut down to the single line `# broken`, and
`tests/docs/` still returned `295 passed`, so no test under that directory reads the
file and G5's occurrence counts are the only check on C1's content. The worktree was
removed and pruned and the primary checkout is clean. COMMIT HYGIENE IS CLEAN: the
path set before C4 is the five declared paths, per-commit insertions are 373, 304, 24,
104, 3 and the handback's own 81, none over 500, all six commits are single-parent,
the reflog holds only `commit:` entries, and the ordered push landed — origin and
local agree at 6ca30b16. THE HANDBACK REPORTED THE PAIR SHAPES THE WAY R34 EXISTS TO
MAKE POSSIBLE: both APPEND pairs are reported as APPEND with no FROM-zero count
claimed, and the one REWRITE pair carries its FROM-0x/TO-1x reading. That is R-0523's
counter-measure working on the first round it applied.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R34's worker reported that
one sentence of the reviewer's own RECORD2 was falsified by its own C4, and declared
it in the handback rather than editing a slice it was told to apply byte-verbatim.
That is exactly the behaviour constraint 8 exists to produce, and the finding below is
the reviewer's, not the worker's.

- R-0525 — Low, A RESOLUTION LOCATED LANDED TEXT IN A PATH THAT IS REWRITTEN EVERY
ROUND, WITHOUT THE SHA THAT HOLDS IT. R34's RECORD2, applied at commit 2342ed97,
closes its R-0523 resolution with the words "the false sentence stays in
`.agent/handoff.md` where it landed". Commit 6ca30b16 — C4 of the same round — rewrote
that path in full, so at 6ca30b16 it does not contain the sentence; the version of
that path in commit 7480d880 does. The referent is recoverable, because the R-0523
registration two paragraphs above names 7480d880 explicitly, which is why this is Low
and was not a block condition against R34. What makes it worth an id is that it is the
R-0520 family arriving through a door R-0524 had just left open. R-0524's carve-out
permits an ordering constraint in place of a SHA for a claim about the round's OWN
change; this sentence is not that claim. It locates a PRIOR round's text by path
alone, and for `.agent/handoff.md` a bare path can never be durable, because the last
commit of every round rewrites it by construction — the staleness is SCHEDULED, not
merely possible, and no ordering constraint reaches it. The same holds for
`.agent/plan.md`, `.agent/last_block.md` and `.agent/context.md`. Found by the
reviewer against the worker's declared observation, which is where a constraint-8
report is supposed to be read.

Done: R-0525 — Resolved at R35. Checklist item 20 of
`docs/agents/planner_reviewer_prompt.md` §3 now requires a slice that merely LOCATES
landed text to name the SHA of the commit holding it whenever the path is one this
workflow rewrites every round, and it names those paths — `.agent/handoff.md`,
`.agent/plan.md`, `.agent/last_block.md`, `.agent/context.md` — rather than leaving
the reader to judge which paths qualify. Elsewhere a bare path stays acceptable, and
the clause says so, because a rule that reaches every path would make ordinary
cross-references unwritable. Applied by the commit that constraint 9 of this round's
block fixes ahead of this one. This entry obeys the new clause: every reference it
makes to `.agent/handoff.md` names the SHA that holds the text it means.
END-RECORD3

BEGIN-PLANF3
## Current Step
R34, this round: record the R33 FAIL, and register and resolve R-0522, R-0523 and
R-0524 — a pair mislabelled REWRITE, the false rewrite proof that label produced, and
the slice class item 20's required SHA cannot reach. No production code changes.
END-PLANF3

BEGIN-PLANT3
## Current Step
R35, this round: record the R34 PASS, and register and resolve R-0525 by naming the
paths this workflow rewrites every round, so a slice locating landed text in one of
them carries the SHA that holds it. No production code changes.
END-PLANT3
