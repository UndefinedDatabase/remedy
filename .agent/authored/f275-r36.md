── STEP T003 (1 of n) — F275 ─────────────────────────────────
Goal:        Re-derive the T002 flip site set AT T003's OWN BASE, as DECISION
             F275 D17 orders, and ENUMERATE it file by file so the flip commit
             is applied from a committed list; and repair the third and fourth
             instances of R-0870.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 35
             verdict and three prose slips · C3 the two R-0870 repairs · C4 the
             flip enumeration · C5 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r36.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`,
             `packages/common/public_text_redaction.py`,
             `tests/cli/test_mission_cmd.py`,
             `.agent/f275_t003_flip_sites.md` (NEW),
             plus `.agent/handoff.md` at C5.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end of frame; the single pure rule line below is exactly 62 `─` characters
──────────────────────────────────────────────────────────────

## Base

This round's base is `965ea50d`. EVERY NUMERAL BELOW WAS MEASURED BY THE
REVIEWER IN A DISPOSABLE WORKTREE AT THAT BASE BEFORE THIS BLOCK WAS AUTHORED:
the probe run, the static sweep, the union, the two repair pairs and the red
proof were all applied and run, and the readings are that run's, not a
prediction.

## What this round is, and what it is NOT

DECISION F275 D17 ruled the classic-to-unified flip ONE declared-oversize commit
inside T003, and its closing clause binds this round by name: "T003 re-derives
the set at its own base before it commits rather than inheriting these figures
— every count here names `0b009325`, and the tree moves between now and then."
The tree HAS moved: rounds 32 to 35 deleted `run_agent_loop`, `job.run-next` and
`job.run`, and the union has fallen from 1768 sites to 1753.

THIS ROUND MOVES NO PRODUCTION LINE OF THE FLIP. It produces the ENUMERATION the
flip round applies, which round 31's inventory deliberately did not carry — that
file SIZED the change and gave figures; this one NAMES every site. The reason for
the split is the commit cap: a per-site enumeration is 1753 lines and cannot be
one commit, while the per-FILE rendering below is 184 lines and can.

THIS ROUND DOES NOT RESOLVE R-0870 and the worker writes no `Done:` paragraph
for it. C3 repairs the third and fourth instances the `Note: F275 R24` entry
records; the reviewer authors the resolution at the next gate, and the worker
marks the fix `Landed:` per planner_reviewer_prompt.md §4 item 4.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Extract each by its delimiter lines from the
   committed `.agent/authored/f275-r36.md` and apply with `shutil.copyfile`
   semantics — never by retyping, never reflowed. If anything does not fit,
   DECLARE it in the handback and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, exactly — seven commits, no
   extra, none dropped, no reordering. C1 is the first substantive commit and
   makes `.agent/plan.md` current before any other change, per §3 item 23.
3. THE APPEND BASELINES, read by the reviewer at the base: `.agent/live_review.md`
   is 819410 bytes and `.agent/prose_slips.md` is 225483 bytes, each ending in a
   newline. An append is pre-blob, then ONE newline, then the slice as extracted.
4. C3 IS THE ONLY COMMIT THAT TOUCHES `packages/` OR `tests/`. C4 touches only
   `.agent/`. No path under `apps/`, `docs/` or `scripts/` moves in this round at
   all.
5. THE ENUMERATION IS GENERATED, NEVER RETYPED. `.agent/f275_t003_flip_sites.md`
   is written from the worker's OWN probe and sweep output by a script, and its
   numerals are the worker's own readings. The figures this block states are the
   reviewer's, carried so that a DIFFERENCE IS VISIBLE rather than reconciled
   away: report both, and never edit a measured number to match a stated one.
6. IDS REGISTERED THIS ROUND: none. IDS RESOLVED THIS ROUND: none. The open set
   is 87 by distinct id at the base and must read 87 at C4.
7. THE ROUND GATE IS TIER 1 — the scoped commands in G6 plus the canary. The full
   suite is NOT run outside the probe run G7 orders.
8. EACH PAIR BELOW IS A REWRITE AND NOT AN APPEND, and the containment test was
   RUN before emission rather than judged by eye: for PAIR A `TO contains FROM:
   false`, for PAIR B `TO contains FROM: false`. Order no "FROM 0x" whole-file
   count for either; the obligation is FROM exactly 1x in its target before the
   edit and 0x after, which G5 states.

## SLICE PLAN36 → whole-file replacement of `.agent/plan.md`

<<<PLAN36
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 36 re-derives the T002 flip site set AT T003's OWN BASE, which DECISION F275 D17 orders
by name, and ENUMERATES it file by file into `.agent/f275_t003_flip_sites.md` so the flip
commit is applied from a committed list rather than from a fresh measurement. The same round
repairs the third and fourth instances of R-0870 — a docstring sentence falsified by a later
deletion, and a test whose name and docstring outlived the assertion they described. R-0870
STAYS OPEN until the reviewer's `Done:` text lands.

## Next Steps

1. The flip DECISION F275 D17 sized, applied from the round 36 enumeration, as the one
   declared-oversize commit AGENTS.md permits per feature, with the inseparability reason
   stated in the handback BEFORE review.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. Amend DECISION F260 D3 by APPENDING a dated correction that names the nineteen deleted
   `apps/cli/commands/*_cmd.py` handler modules its mapping does not name, so the feature
   file's DONE condition "names every deleted module" is met on a reading rather than on an
   inference. D3's own landed text is NOT rewritten.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take and it spends the one
  declared-oversize allowance AGENTS.md rations per feature.
- The open set is 87 by distinct id at this round's base `965ea50d`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
PLAN36

## SLICE RECORD36 → append to `.agent/live_review.md`

<<<RECORD36
Gate: F275 R35 — the F275 round 35 entry. VERDICT PASS, ISSUED BY THE PLANNER AND REVIEWER OF SESSION 16 over the committed range `df5d527f`..`1e65661a`, and booked here by round 36 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, carried from the `.agent/handoff.md` that rule makes a durable carrier at `0626d133`. THIS PARAGRAPH IS A BOOKING AND NOT A SECOND GATE: the readings below are session 16's own, and the four re-measurements at the end are session 17's, taken at `965ea50d` and labelled as such, because a booking that quietly restates someone else's numbers as its own is the thing this record exists to prevent. WHAT SESSION 16 RE-DERIVED INDEPENDENTLY against the committed blobs, with the worker's report evidence for no line of it. Six single-parent commits C0a `36123491`, C0b `569b30d4`, C1 `02b90479`, C2 `c0de8e51`, C3 `1e65661a` and C4 `0626d133`, per-commit insertions 382, 323, 20, 6 and 145 for the five before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's scratch original was written AND HASHED BEFORE delegation at `e7fd8ff1efb71ded013ff68347b7b27a1e1e8ece9c673755b958539281e8729b`, and both committed copies are 26187 bytes at that digest as ONE shared git blob `f2293206c9256476487937970a031e4eae4092d7`; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN35 at 2417 bytes, 43 lines against the cap of 50, both mandated headings exactly once. G3 over both append targets — `.agent/live_review.md` 814121 to 819410 and `.agent/prose_slips.md` 223959 to 225483 — each post-blob equal to its pre-blob then ONE newline then the slice as extracted, the joining byte READ BACK at offset len(pre) reading a newline in both, the structural reader counting N from each SLICE as 1 and 2 and matching the last N blank-line units IN ORDER, and both negative controls flipped INSIDE THE FIRST appended paragraph per §3 item 36 and REJECTED by BOTH readers. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base and 87 at C3, over 103 registrations against 16 resolutions, with `R-0832` measured to be STILL IN that set rather than assumed to be. G5: the committed `tests/orchestration/test_event_name_coupling.py` and the GUARD35 slice are both 5951 bytes at `95997b5602ec6cc9576004f06dfbdfd75e350b2a2cefc1bf6e1068edade7f0b8` and compare BYTE-EQUAL; the path did not exist at the base, and `ruff` printed `All checks passed!`. G6 THE GUARD BITES, five mutations in a disposable worktree with `__pycache__` purged and every run under `python3 -B`, control 4 passed at exit 0: M1 emptying the allowlist fires `test_every_dead_coupling_is_declared`; M2 adding a stale entry fires BOTH the ceiling assertion and `test_no_declared_entry_is_stale`; M3 blinding `dead_event_couplings` to an empty mapping fires `test_no_declared_entry_is_stale`, which is the anti-blindness direction and the reading that matters most; M5, the real-world direction, inserts a schema entry for `context_pack_created` into `packages/orchestration/event_schemas.py` so a survivor begins reading an event only a deleted module ever emitted, and fires `test_every_dead_coupling_is_declared`. M4 IS GREEN AND WAS ORDERED KNOWING IT WOULD BE: weakening the anti-blindness floor `assert len(deleted_modules()) >= 40` to `>= 0` reddens nothing, because a test cannot detect the weakening of its own assertion, and the honest negative was reported rather than repaired. Every revert was verified byte-exact and the control is green again afterwards. G7: the change set is an EXACT set match over six paths with MISSING and EXTRA both empty, ZERO paths under `packages/`, `apps/`, `docs/` or `scripts/`, porcelain EMPTY, ONE worktree, `.agent/STOP` absent, and collection 18362 at the base to 18366 at C3 — exactly the four tests the new file adds. WHAT SESSION 17 RE-MEASURED AT `965ea50d` BEFORE WRITING THIS BOOKING, so that the entry rests on something this session ran: the open set recomputed mechanically from this file is 87 BY DISTINCT ID over 103 registrations against 16 resolutions, and `R-0832` and `R-0870` are both in it; importing `deleted_modules` and `dead_event_couplings` from the shipped guard reports 43 deleted modules and exactly ONE dead coupling, `context_budget_optimized`, with its two surviving readers `apps/ui/src/api/actionClass.ts` and `packages/orchestration/event_schemas.py`, which reproduces round 35's reading exactly; the guard's own four tests pass at exit 0; and `tests/orchestration/cluster_deletion_map.txt`, `test_cluster_deletion_map.py`, `test_cluster_deletion_order.py` and `.agent/f275_deletion_order.md` are all ABSENT from disk, which is DECISION F275 D15 landed. WHAT THIS GATE DOES NOT CLAIM: R-0832 is NOT resolved and no `Done:` line is written for it, and the reason is on the record rather than in a session — the `Note: F275 R24` entry on that finding rules that what resolves it is the residue's removal by a feature that owns the cockpit's event vocabulary, and DECISION F275 D14 (b) leaves the three surviving sites standing deliberately. NO FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.
RECORD36

## SLICE SLIPS36 → append to `.agent/prose_slips.md`

<<<SLIPS36
2026-09-10 · F275 R35 · The session 16 handback's "Next" section and `.agent/plan.md` Next Step 1 both order the next round to draft DECISION F260 D3, while D3 was recorded at round 23 and sits in `.agent/decisions.md` under its own heading, and DECISION F275 D14 (c) then declared the D3 SEQUENCE closed after round 25. Session 17 measured this at `965ea50d` before authoring. Nothing on disk was wrong — D3 exists and is correct — but the handoff is the file AGENTS.md's Session Resume tells the next session to read, so a work order it carries is executed before anything checks whether the work is already done. A handoff that names the next round's subject re-reads the decision record for that subject first.

2026-09-10 · F275 R35 · The same handback says the D3 round "discharges the second half of R-0832 and is the last thing T001 owes", while the `Note: F275 R24` entry on R-0832 already ruled that what resolves that finding is the residue's removal by a feature that owns the cockpit's event vocabulary, and that this feature is not that one. Both sentences are about the same id, one is in the append-only record and one is in a rewritten state file, and the rewritten one is the one a resuming session reads first. A claim about what resolves an OPEN finding is read out of the ledger paragraph that holds it, never out of the previous handback.

2026-09-10 · F275 R35 · `.agent/plan.md` at `965ea50d` states in its Current Step that "T001 and T002 are DONE" and in its Next Steps item 1 that the D3 round "is the last thing T001 owes", which cannot both be true of the same slice. This is the §3 item 35 shape inside a single authored file — the prose and the enumeration beside it were written in different rounds and never read against each other — and it is recorded here rather than as an id because `.agent/plan.md` is not one of the four trees amend0827-process-diet rule 2 spends an id on.
SLIPS36

## The R-0870 repairs — PAIR A and PAIR B

Both were APPLIED and RUN by the reviewer at the base before emission. Each FROM
occurs EXACTLY ONCE in its target, measured; each TO does NOT contain its FROM,
so both are REWRITES.

## PAIR A → `packages/common/public_text_redaction.py`

FROM is 523 bytes, sha256 `efe4162b287b2011…`; TO is 599 bytes, sha256
`79324162ccf96633…`; TO's longest line is 91 characters against the
`pyproject.toml` limit of 120.

<<<PAIRA_FROM
echo a secret value or an absolute path out of untrusted provider text). Seven modules that
have nothing to do with provider trust came to import them anyway, because masking a
public-facing string is a repository-wide obligation rather than a trust-gate one. F275
round 21 deletes the trust gate, so the helpers move here BYTE-IDENTICALLY — one
implementation, no copy, no shim — and the former host's importers repoint at this
module. DECISION F275 D10 records the move and why this file rather than an existing one.
PAIRA_FROM

<<<PAIRA_TO
echo a secret value or an absolute path out of untrusted provider text). Seven modules that
have nothing to do with provider trust came to import them anyway, because masking a
public-facing string is a repository-wide obligation rather than a trust-gate one. F275
round 21 MOVED the helpers here BYTE-IDENTICALLY — one implementation, no copy, no shim —
and repointed the former host's importers at this module; F275 round 22 then deleted that
host at `0242c0a3`, which is the deletion the sentence above names. DECISION F275 D10
records the move and why this file rather than an existing one.
PAIRA_TO

## PAIR B → `tests/cli/test_mission_cmd.py`

FROM is 421 bytes, sha256 `c551206edcaf8dce…`; TO is 789 bytes, sha256
`b912c91e5c6e9973…`; TO's longest line is 80 characters. The FROM spans the
WHOLE enclosing unit — the `def` line and the entire docstring — because that is
what the widened R-0870 fix clause in the `Note: F275 R24` entry requires, and
because the name, the docstring and the assertion are the three halves that
drifted apart. The assertion itself is NOT touched.

<<<PAIRB_FROM
    def test_the_cockpit_no_longer_imports_the_cluster_readiness_module(self):
        """The edge this round cut. The map ratchet proves the graph; this names the file.

        The token is the DOTTED MODULE PATH, never the bare word: the carried
        symbol `build_overnight_readiness` keeps its spelling by DECISION F275
        D1, so a substring check would red on the very names the move preserves.
        """
PAIRB_FROM

<<<PAIRB_TO
    def test_the_cockpit_source_names_the_carried_readiness_module(self):
        """The cockpit imports the CARRIED module, named by its dotted path.

        The token is the DOTTED MODULE PATH, never the bare word: the carried
        symbol `build_overnight_readiness` keeps its spelling by DECISION F275
        D1, so a substring check would red on the very names the move preserves.

        The negative half — that the deleted module is not imported here —
        carries no assertion and needs none: `overnight_readiness.py` has not
        existed on disk since `0f19c86a`, so an import of it raises instead of
        passing quietly. The map ratchet this test once cited was retired by
        DECISION F275 D15, so citing it would name a guard that is gone.
        """
PAIRB_TO

## SPEC-FLIP → the NEW file `.agent/f275_t003_flip_sites.md`, GENERATED at C4

This file is not sliced. The worker PRODUCES it from its own instrument runs, in
a disposable `git worktree` at C3, and every numeral in it is that run's.

THE INSTRUMENTS ARE ALREADY ON DISK AND ARE NOT REWRITTEN. At the base
`965ea50d` the file `.agent/f275_t002_flip_inventory.md` carries two fenced
```python blocks and no third, measured by the reviewer: the first is
`r31probe.py`, the second `r31_static.py`. Extract both by fenced-block
extraction and
write them at the WORKTREE ROOT under those two names — the probe computes its
own `ROOT` from its file location and refuses with a `RuntimeError` if the two
record modules resolve outside it, which is the editable-install guard.

THE RUNS, in this order, with `__pycache__` purged first and every run under
`python3 -B`:
  (a) `python3 -B -m pytest tests/ -q -p r31probe` — the full suite, SERIALLY.
  (b) `python3 -B r31_static.py` — the `ast` sweep over `git ls-files '*.py'`.

WHAT THE REVIEWER MEASURED AT THE BASE, so a difference is visible: run (a) read
`1 failed, 18336 passed, 29 skipped, 1 warning in 1289.85s (0:21:29)` at exit 1,
and the single failure is
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
which is the fresh-worktree `apps/ui/node_modules` artifact and NOT a probe
effect — the probe is behaviour-neutral and the golden-path canary reads 42
passed at exit 0 under it. REPORT the real summary line and exit code whatever
they are; do not make them match.

THE FILE'S SECTIONS, in this order.
  1. A banner naming the base SHA this was measured at, and stating that the file
     ENUMERATES the flip and that no line under `packages/`, `apps/`, `tests/`,
     `docs/` or `scripts/` moved in the round that wrote it.
  2. The two runs: command, real summary line, real exit code, and for (b) its
     whole stdout.
  3. A figures table with a `measured` column, a `reviewer` column carrying the
     numbers below, and a `verdict` column reading `same` or `differs (<n>)`.
  4. The provably-`Job`-but-never-executed list, BY PATH AND LINE IN FULL.
  5. THE ENUMERATION: one line per file, sorted by path, in the exact form
     `<path> | id: <comma-separated lines or -> | name: <comma-separated lines or ->`,
     where the lines are the sorted distinct line numbers of the UNION set for
     that file and that field.
  6. What the reading does not settle: the union is a FLOOR and not a ceiling,
     because a site both unexecuted and unprovable is invisible to both
     instruments, and that remainder is given NO numeral because none was
     measured.

THE REVIEWER'S FIGURES, measured at `965ea50d`. A site is one
`(path, line, field)` triple and a changed line one `(path, line)` pair.
  probe: sites 1745 · probe: distinct changed lines 1743
  static: provably `Job`, distinct triples 312
  UNION: sites 1753 · UNION: distinct changed lines 1751
  UNION: production lines 349 over 68 files
  UNION: test lines 1402 over 116 files
  provably `Job` but never executed 8
  tracked `.py` 991 · parsed 991 · unparsable 0
  `Job(...)` constructions 582 — production 12, test 570
  `Job` imports 345 — production 47, test 298
  `Job` annotations 368 — production 151, test 217
  the enumeration renders 184 file lines
The eight never-executed sites are `packages/orchestration/decision_queue.py:1017`,
`packages/orchestration/do_run.py` at 261, 285, 316 and 357,
`tests/orchestration/test_job_fulfillment.py:1087`,
`tests/orchestration/test_real_ollama_smoke.py:165` and
`tests/orchestration/test_token_economy_integration.py:28`, every one `.id`.

## Done when — GATES G1 to G8

Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code
and the real numbers. "Green" as a word is a finding. One line per gate in the
handback.

**G1 TRANSPORT (at C0b).** The committed `.agent/authored/f275-r36.md` and
`.agent/last_block.md` have the SAME sha256 as the reviewer's delegation source,
and resolve to ONE shared git blob. `.agent/last_block.md` is written from
`git cat-file blob HEAD:.agent/authored/f275-r36.md`, never retyped. State that
the chain covers those on-disk artefacts and claims nothing about emitted bytes.

**G2 THE PLAN (at C1).** `.agent/plan.md` is BYTE-EQUAL to the PLAN36 slice as
extracted — same length, same sha256. Report its line count against the
AGENTS.md cap of 50, and `^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2).** For `.agent/live_review.md` and
`.agent/prose_slips.md` separately: post-blob equals pre-blob then ONE newline
then the slice, with the pre-blob lengths of constraint 3; READ BACK the joining
byte at offset len(pre) and report it. Then an INDEPENDENT structural reader with
N COUNTED FROM THE SLICE and not from this block: the last N blank-line units of
the post-blob equal the slice's N paragraphs IN ORDER. Then one negative control
per append, flipping a byte INSIDE THE FIRST appended paragraph, which BOTH
readers must REJECT. `^Gate: F275 R35 ` exactly 1.

**G4 THE OPEN SET (at C4).** BY DISTINCT ID, every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id, at the base `965ea50d` and at C4. Report both. Ids
registered this round and ids resolved this round must both be `[]`. Report
SEPARATELY that `R-0870` IS STILL IN the open set at C4 and carries NO `Done:`
line — examined, not assumed.

**G5 THE TWO PAIRS ARE THE AUTHORED BYTES (at C3).** For each pair: the FROM
occurs EXACTLY 1x in its target before the edit and EXACTLY 0x after; the TO
occurs EXACTLY 1x after; and the applied file's post-blob equals its pre-blob
with the FROM span replaced by the TO span and nothing else, proved by
reconstructing the post-blob from the pre-blob and comparing sha256. Then
`python3 -m ruff check packages/common/public_text_redaction.py tests/cli/test_mission_cmd.py`
— the reviewer read `All checks passed!` at exit 0. Then the sweep the repair
exists for: `round 21 deletes the trust gate` and
`test_the_cockpit_no_longer_imports_the_cluster_readiness_module` each occur ZERO
times under `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` at C3. That
sweep DELIBERATELY EXCLUDES `.agent/`, where both strings survive inside the
frozen `.agent/authored/` blocks of earlier rounds and inside the `Note: F275 R24`
ledger entry that registered them; a zero-gate over `.agent/` would be unmeetable
by construction and this block does not order one.

**G6 THE REPAIRED TEST STILL BITES — RED PROOF (at C3).** In a DISPOSABLE
`git worktree` at C3, `__pycache__` purged, every run under `python3 -B`. The
reviewer's own readings at the base, to be reproduced: CONTROL unmutated
`python3 -B -m pytest tests/cli/test_mission_cmd.py -q` exit 0 at `108 passed`.
MUTATION, revert target `packages/orchestration/ui_server.py` and the anchor
counted 1 in THAT file before it is applied: replace the single line
`        from packages.orchestration.mission_readiness import (` with the same
line carrying TWO spaces before `import` — valid Python that still imports, so
what breaks is the asserted TEXT and nothing else. The reviewer read exit 1 at
`1 failed, 107 passed`, the failing node being
`tests/cli/test_mission_cmd.py::TestMissionReadinessIsWiredToTheCarriedModule::test_the_cockpit_source_names_the_carried_readiness_module`
— the RENAMED test, which is the point of the proof. Revert byte-exactly, verify
by sha256, and report the CONTROL AGAIN reading. Then the round's scoped gate in
the PRIMARY checkout: `python3 -B -m pytest tests/cli/test_mission_cmd.py
tests/orchestration/test_import_reachability.py -q`, which the reviewer read at
`111 passed`.

**G7 THE ENUMERATION (at C4).** Report run (a)'s real summary line and exit code
and run (b)'s whole stdout. Then the figures table of SPEC-FLIP, every row with
its measured value beside the reviewer's and a `same` or `differs (<n>)` verdict.
Then three properties of the committed file, measured on the file itself: its
section 5 holds exactly one line per distinct path in the union; the count of
line numbers across all its `id:` and `name:` fields equals the UNION site count
it reports; and every path it names resolves on disk at C4 with
`git ls-tree C4 -- <path>`. Report the file's own line count and byte length.

**G8 NOTHING ELSE MOVED (at C4).** `.agent/STOP` read FROM DISK: report present
or absent. `git status --porcelain`: EMPTY. `git worktree list`: exactly ONE
entry. `git diff --name-only 965ea50d..C4` is an EXACT SET MATCH against the
`Change:` list above minus `.agent/handoff.md` — report MISSING and EXTRA
explicitly. Per-commit insertions for C0a through C4, each under the DECISION
F104 D1 cap of 500; the handback commit's own numbers are NOT ordered here,
per §3 item 14. Canary `python3 -m pytest tests/cli/test_golden_path.py -q`.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
SESSION 17 of F275 and round 36, the per-commit table with `git diff --numstat`
values in the `+/-` column, one line per gate G1 to G8 with real exit codes, the
item-status table, the open-findings count by distinct id, and the deviations.
State explicitly that R-0870 is NOT resolved, that its fix is marked `Landed:`
and that the reviewer's `Done:` text is owed at the next gate. Add the one
sentence of context self-assessment amend0905-throughput requires. No PR is
created and nothing is merged: this round is not a closure sequence.
