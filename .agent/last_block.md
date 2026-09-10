── STEP T003 (2 of n) — F275 ─────────────────────────────────
Goal:        Discharge R-0870's widened fix clause over the WHOLE surviving tree
             by repairing every remaining instance the resolution sweep found,
             and extend DECISION F260 D3's mapping to the nineteen deleted CLI
             handler modules it does not name.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 36
             verdict and two prose slips · C3 the three R-0870 repairs · C4 the
             D3 handler amendment · C5 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r37.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `.agent/decisions.md`,
             `docs/system/test-lanes-v0.md`,
             `docs/system/development-artifact-boundary-v0.md`,
             `tests/conftest.py`,
             plus `.agent/handoff.md` at C5.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end of frame; the single pure rule line below is exactly 62 `─` characters
──────────────────────────────────────────────────────────────

## Base

This round's base is `f4fc3459`. EVERY REPAIR BELOW WAS APPLIED AND RUN by the
reviewer in a disposable worktree at that base before this block was authored,
and the handler mapping in SPEC-D3 was DERIVED FROM GIT rather than inferred from
the handler names. Every numeral is that run's.

## What this round is, and what it is NOT

R-0870 records prose falsified by a deletion in a file the deleting round's change
set did not name, and the `Note: F275 R24` entry WIDENED its fix clause to bind
"every remaining round of this feature". Four instances are on the record and all
four are repaired — two at round 23, two at round 36. THE RESOLUTION SWEEP THE
REVIEWER RAN AT THE BASE FOUND MORE, which is why this round exists rather than a
`Done:` paragraph: over 90 deleted module stems and 2255 tracked files outside
`.agent/`, `docs/roadmap/` and `docs/archive/`, three surviving files still make a
claim a deletion falsified. C3 repairs them.

THIS ROUND STILL DOES NOT RESOLVE R-0870 and the worker writes no `Done:`
paragraph. The reviewer authors the resolution at the next gate, once it has
re-run the sweep itself against the committed tree; the worker marks the fix
`Landed:` per planner_reviewer_prompt.md §4 item 4.

WHAT THE SWEEP DELIBERATELY DID NOT TREAT AS AN INSTANCE, stated so the next
sweep does not re-open them. `docs/system/vocabulary.md` names the
`overnight_mission` module inside a landed DECISION paragraph that says in its own
words that the module "is superseded by this and deleted"; that sentence is TRUE
and §3 item 20 forbids rewriting landed decision text. `packages/orchestration/mission_readiness.py`
names `packages/orchestration/overnight_readiness.py` twice and then states "F275
round 19 deleted that module with its cluster group", which is the correct
pattern and the one C3 of round 36 established. `docs/system/quality-baseline-v0.md`
names two deleted handlers and annotates each "(deleted by F275)". And
`packages/orchestration/proposed_tasks.py` defines a FUNCTION called
`overnight_readiness`, which is a name collision with a deleted module stem and
not a reference to it.

THE LANE COUNTS ARE NOT TOUCHED. `docs/system/test-lanes-v0.md` gives each lane an
approximate test count written `~535`, `~57`, `~6860+` and `~300+`. Removing two
suite rows makes the first of those smaller by an unmeasured amount. Those figures
were approximations before this deletion and re-deriving all four lanes is a
measurement this round does not take; PAIR C changes rows and no numeral.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Extract each by its delimiter lines from the
   committed `.agent/authored/f275-r37.md` and apply with `shutil.copyfile`
   semantics — never by retyping, never reflowed. If anything does not fit,
   DECLARE it in the handback and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, exactly — seven commits, no
   extra, none dropped, no reordering. C1 is the first substantive commit and
   makes `.agent/plan.md` current before any other change, per §3 item 23.
3. THE APPEND BASELINES, read by the reviewer at the base: `.agent/live_review.md`
   is 825867 bytes, `.agent/prose_slips.md` is 227412 bytes and
   `.agent/decisions.md` is 1039256 bytes, each ending in a newline. An append is
   pre-blob, then ONE newline, then the slice as extracted.
4. C3 AND C4 ARE THE ONLY COMMITS THAT TOUCH ANYTHING OUTSIDE `.agent/`, and only
   C3 does — C4's single path is `.agent/decisions.md`. No path under `packages/`,
   `apps/` or `scripts/` moves in this round at all.
5. THE `Landed:` LINE HAS ITS OWN SLICE AND ITS OWN COMMIT SLOT. LANDED37 is
   appended to `.agent/live_review.md` IN C3, after the three repairs are staged,
   so that the marking and the fix it names are one commit. This is stated because
   the round 36 block ordered such a marking without giving it either, and the
   worker had to place it itself.
6. IDS REGISTERED THIS ROUND: none. IDS RESOLVED THIS ROUND: none. The open set
   is 87 by distinct id at the base and must read 87 at C4.
7. THE ROUND GATE IS TIER 1 plus the docs tier: the scoped commands in G6 and the
   canary. The full suite is NOT run this round.
8. EACH PAIR BELOW IS A REWRITE AND NOT AN APPEND, and the containment test was
   RUN before emission rather than judged by eye: for PAIR C `TO contains FROM:
   false`, for PAIR D `TO contains FROM: false`, for PAIR E `TO contains FROM:
   false`. Order no "FROM 0x" whole-file count for any of them; the obligation is
   FROM exactly 1x in its target before the edit and 0x after, which G5 states.

## SLICE PLAN37 → whole-file replacement of `.agent/plan.md`

<<<PLAN37
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

ROUND 37 discharges R-0870's widened fix clause across the whole surviving tree. The
reviewer's resolution sweep — 90 deleted module stems over 2255 tracked files outside
`.agent/`, `docs/roadmap/` and `docs/archive/` — found three surviving files still making a
claim a deletion falsified, and this round repairs all three. The same round extends
DECISION F260 D3's mapping to the nineteen deleted CLI handler modules, by a mapping
derived from git rather than from their names. R-0870 STAYS OPEN until the reviewer's
`Done:` text lands.

## Next Steps

1. Re-derive the REMAINDER of the flip that DECISION F275 D17 gave no numeral: the store
   seam and the sites that treat a job id as a UUID. The round 36 enumeration covers the
   `.id` and `.name` half only, and the reviewer measured that 124 further files are
   reached by the remainder alone. Then a dated DECISION ruling the route on the complete
   figure, as T002 did on the partial one.
2. The flip itself, applied from that complete enumeration, as the one declared-oversize
   commit AGENTS.md permits per feature, with the inseparability reason stated in the
   handback BEFORE review.
3. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 2 is the largest single commit this repository will take and it spends the one
  declared-oversize allowance AGENTS.md rations per feature. Step 1 exists because that
  allowance can be spent once and the size it must cover is not yet fully measured.
- The open set is 87 by distinct id at this round's base `f4fc3459`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
PLAN37

## SLICE RECORD37 → append to `.agent/live_review.md`, in C2

<<<RECORD37
Gate: F275 R36 — the F275 round 36 entry. VERDICT PASS, written by the planner and reviewer of session 17 after reading the committed range `965ea50d`..`f4fc3459` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits C0a `ae5fbc84`, C0b `5e0e09f2`, C1 `64bfe488`, C2 `a57bbdb0`, C3 `d68125d1`, C4 `7b7bb75f` and C5 `f4fc3459`, per-commit insertions 366, 321, 17, 8, 12 and 343 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's delegation source was written AND HASHED BEFORE delegation at `d25ff9154a448183f4a26b99381e4d982d49cb52dd027f2653b12fce4df1e418`, and both committed copies are 27786 bytes at that digest as ONE shared git blob; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN36 at 2476 bytes, 44 lines against the cap of 50, both mandated headings exactly once. G3 over both append targets — `.agent/live_review.md` 819410 to 824654 and `.agent/prose_slips.md` 225483 to 227412 — each post-blob equal to its pre-blob then ONE newline then the slice as extracted, the joining byte READ BACK at offset len(pre) reading a newline in both, the structural reader with N COUNTED FROM THE SLICE as 1 and 3 matching the last N blank-line units IN ORDER, and both negative controls flipped INSIDE THE FIRST appended paragraph rejected by BOTH readers when the reviewer ran them itself. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base, at C4 `7b7bb75f` and at C5 `f4fc3459`, over 103 registrations against 16 resolutions, with `R-0870` and `R-0832` both measured to be still in it and carrying no `Done:` line. G5: both repair pairs reconstruct exactly — the FROM occurs 1x before and 0x after in each target, the TO 1x after, and the committed post-blob equals the pre-blob with the FROM span replaced and nothing else; `ruff` printed `All checks passed!`; and the reviewer's own sweep over 1609 tracked files under `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` reads ZERO for both retired strings. G6 THE REPAIRED TEST STILL BITES, re-run by the reviewer in its own disposable worktree at C4: control exit 0 at `108 passed`, the mutation that puts two spaces before `import` in `packages/orchestration/ui_server.py` exit 1 at `1 failed, 107 passed` with the failing node being the RENAMED test `test_the_cockpit_source_names_the_carried_readiness_module`, the revert byte-exact by sha256, and the control green again. The scoped gate reads `111 passed` and the canary `42 passed`, both re-run by the reviewer. G7 THE ENUMERATION REPRODUCED EXACTLY AND THAT IS THE POINT OF THE ROUND: the committed `.agent/f275_t003_flip_sites.md` holds 184 rows over 184 distinct paths in sorted order, every path resolving at C4, and the reviewer's own reading of that file gives 1753 line numbers across its `id:` and `name:` fields over 1751 distinct changed lines, 349 production lines in 68 files and 1402 test lines in 116 files — every one of the 23 figure rows reading `same` against the figures the block carried, measured independently on both sides. The eight provably-`Job`-but-never-executed sites match the reviewer's list path for path. G8: the change set is an EXACT set match over nine paths with MISSING and EXTRA both empty, porcelain EMPTY, ONE worktree, `.agent/STOP` absent, and `ruff check .` at 26 against the ceiling its own test pins. THE WORKER'S FOUR SUBSTANTIVE DEVIATIONS ARE ALL SUSTAINED AND ONE OF THEM CORRECTS THIS REVIEWER. FIRST, the block ordered a `Landed: R-0870` marking without giving it a slice or a commit slot, and the worker placed it in C5 rather than silently dropping it or forcing it into a byte-gated append; the reviewer read that line at C5 and it is correct. SECOND, the block predicted the probe run would come back RED with a vitest failure caused by a fresh worktree lacking `apps/ui/node_modules`, and the worker measured the run GREEN at `18343 passed, 23 skipped` at exit 0 and measured the reviewer's stated CAUSE to be wrong as well — the worktree does carry `node_modules`, and the reviewer's own red came from vite resolving through the primary checkout. The block had ordered the real reading to be reported whatever it was, so the round lost nothing; the prediction was simply wrong and is recorded as a prose slip. THIRD, the enumeration file's section numbering runs one off from SPEC-FLIP because the banner was left unnumbered, with content order identical. FOURTH, the worker narrowed the file's no-movement banner because the wider wording SPEC-FLIP gave would have been false — C3 does move lines under `packages/` and `tests/` — and backed the narrowing with a measurement, that neither repaired file carries a single union site, so no enumerated line number shifted. That is the round catching a defect in the block rather than inheriting it. NO FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.
RECORD37

## SLICE SLIPS37 → append to `.agent/prose_slips.md`, in C2

<<<SLIPS37
2026-09-10 · F275 R36 · The round 36 block's SPEC-FLIP predicted the probe run would read `1 failed, 18336 passed, 29 skipped` at exit 1 and attributed the failure to a fresh worktree lacking `apps/ui/node_modules`. The worker measured the run GREEN at `18343 passed, 23 skipped` at exit 0 and then measured the attribution wrong as well: the worktree does carry `node_modules`, and the reviewer's own red came from vite resolving `vitest` through the PRIMARY checkout's `.vite-temp`. Nothing was damaged, because the block ordered the real summary line and exit code to be reported whatever they were and forbade making them match. A predicted colour is worth stating only with the mechanism that would produce it, and a reviewer that cannot name the mechanism should order the reading without the prediction.

2026-09-10 · F275 R36 · The round 36 block ordered the fix marked `Landed: R-0870` in its prose and gave that line neither a slice nor a commit slot, while every other byte the round wrote was both sliced and gated. The worker placed it in the handback commit and declared the choice. An instruction that produces bytes in a file the block's own change set names is a slice like any other; ordering it in prose alone leaves the worker to invent the wording, the position and the commit, which is exactly what the slice discipline exists to prevent.
SLIPS37

## The R-0870 sweep repairs — PAIR C, PAIR D and PAIR E

Every FROM occurs EXACTLY ONCE in its target, measured at the base; no TO contains
its FROM, so all three are REWRITES. All three were applied and gated by the
reviewer before emission.

## PAIR C → `docs/system/test-lanes-v0.md`

The lane table advertises two suites this feature deleted. The FROM spans the two
surviving rows on either side of them, so the pair is anchored rather than a bare
deletion. FROM is 405 bytes, sha256 `2b5f303bcf0320eb…`; TO is 204 bytes, sha256
`d5a53ac9128d1d53…`. No test in the repository reads this page — the reviewer
grepped `tests/` and `scripts/` for its path and got one hit, in
`docs/README.md`, which is the index and names it without asserting anything.

<<<PAIRC_FROM
| `test_worker_facade_cmd.py` | unit | Worker add/doctor/disable, alias registry, catalog wiring |
| `test_dogfood_run.py` | unit | Mission run loop, morning report, 10 stop conditions, evidence |
| `test_self_repair_proposal.py` | unit | Proposal lifecycle: create/approve/deny/edit/worker-prompt |
| `test_development_artifact_boundary.py` | guard | Dev artifact vs product truth boundary enforcement |
PAIRC_FROM

<<<PAIRC_TO
| `test_worker_facade_cmd.py` | unit | Worker add/doctor/disable, alias registry, catalog wiring |
| `test_development_artifact_boundary.py` | guard | Dev artifact vs product truth boundary enforcement |
PAIRC_TO

## PAIR D → `docs/system/development-artifact-boundary-v0.md`

The page says in the present tense that a deleted handler reads a file. FROM is
142 bytes, sha256 `319d301921578b1b…`; TO is 309 bytes, sha256
`4d95064aaa6c3d46…`; TO's longest line is 82 characters.
`tests/cli/test_product_spine.py` reads this page and asserts exactly one thing
about it — that it contains the substring `NOT product runtime state` — which this
pair does not touch. That assertion was read at the base, not assumed.

<<<PAIRD_FROM
`progress_cmd.py` reads it for developer convenience display.
It is classified as a development command, not a core product operator command.
PAIRD_FROM

<<<PAIRD_TO
`progress_cmd.py` READ it for developer convenience display, and it was classified
as a development command rather than a core product operator command. F275 deleted
that handler with the whole `progress` command group, and nothing product-facing
replaced it, so no command reads this file for display today.
PAIRD_TO

## PAIR E → `tests/conftest.py`

`SUBPROCESS_FILES` is a set of test file NAMES, read at one site as
`if filename in SUBPROCESS_FILES:`. One entry names a file F275 deleted, so the
membership test can never fire for it — dead data rather than a wrong behaviour,
which is why it rides with the prose repairs. FROM is 106 bytes, sha256
`6c8d9df2ef11888a…`; TO is 70 bytes, sha256 `828f493e9bfdaa54…`. The FROM spans
the neighbouring entry on each side so the pair is anchored.

<<<PAIRE_FROM
    "test_project_constitution.py",
    "test_agent_loop_execution.py",
    "test_autonomy_readiness.py",
PAIRE_FROM

<<<PAIRE_TO
    "test_project_constitution.py",
    "test_autonomy_readiness.py",
PAIRE_TO

## SLICE LANDED37 → append to `.agent/live_review.md`, in C3

<<<LANDED37
Landed: R-0870 — the three further falsified claims the reviewer's resolution sweep found at `f4fc3459` are repaired in C3 of F275 round 37, and the two `Landed:` lines above are left untouched because each names the instances it covers. `docs/system/test-lanes-v0.md` no longer advertises `test_dogfood_run.py` or `test_self_repair_proposal.py` as lane suites, both deleted with their module groups; `docs/system/development-artifact-boundary-v0.md` no longer says in the present tense that `progress_cmd.py` reads the review ledger for display, and names the deletion instead; and `tests/conftest.py` no longer carries `test_agent_loop_execution.py` in `SUBPROCESS_FILES`, an entry whose file died with the classic runner at round 32 and whose membership test could never fire again. NOT RESOLVED: the reviewer's `Done:` text is owed at the next gate, after it re-runs the sweep itself against the committed tree.
LANDED37

## SPEC-D3 → the DECISION F260 D3 amendment, appended to `.agent/decisions.md` in C4

This is a SLICE and is applied byte for byte like every other. It is stated as its
own section only because it is long.

<<<AMEND37
## DECISION F275 D20 (2026-09-10, F275 round 37) — amending DECISION F260 D3: the nineteen deleted CLI handler modules, and the feature that inherited each

WHAT IS BEING AMENDED, AND WHAT IS NOT. DECISION F260 D3, recorded at round 23, maps every
module F260's Design section lists to the feature that inherited its idea. Its own opening
clause states the obligation it answers, which `docs/roadmap/features/T2_F275.md` words as
D3 "exists and names every deleted module and the feature that inherited its idea". D3's
landed text is NOT rewritten, per planner_reviewer_prompt.md §3 item 20; this paragraph is
its dated extension.

THE GAP, MEASURED at `f4fc3459` rather than noticed. Walking `a5bf894946ab6de053a4232109d6341a63533768..f4fc3459`
with `git log --diff-filter=D` gives 42 deleted non-test `.py` modules: 23 under `packages/`
and 19 under `apps/cli/commands/`. D3's mapping names the 23, and a twenty-fourth,
`packages/orchestration/overnight_readiness.py`, which it records as CARRIED rather than
deleted in idea. It names NONE of the 19 handlers. Read strictly, the feature's DONE
condition was therefore met for 23 of 42 modules and left the rest to an inference.

THE MAPPING, DERIVED FROM GIT AND NOT FROM THE HANDLER NAMES. For each handler the reviewer
read its LAST content before the commit that deleted it — `git show <killer>~1:<path>` —
parsed it with `ast`, and recorded every first-party import of a module this feature also
deleted. Seventeen handlers serve exactly one such module and two serve two. The handler
inherits precisely what its module inherits, because operator RULE 1 in
`docs/roadmap/features/T2_F275.md` T001 defines a module group as one cluster module
together with everything that exists ONLY for it and names the handler first among those.

`builder_routing_cmd.py` served `builder_routing` — F110, routing configuration (R-0848,
with R-0831 holding the knob-by-knob audit). `candidate_quality_cmd.py` served
`candidate_quality` — F082, evidence-based comparison of a candidate (R-0848).
`context_optimizer_cmd.py` served `context_optimizer` and `context_pack_cmd.py` served
`context_pack` — both F107, context compiler v2 (R-0842). `dogfood_cmd.py` served
`dogfood_run` — NONE, deliberately, because F260's Design deletes the prototype rather than
carrying it (R-0845). `external_builder_cmd.py` served `external_builder_sandbox` — F085,
external-worker ingress (R-0852), with the scoring step going to F082 (R-0849).
`local_advisor_cmd.py` served `local_model_advisor` — F110, local-model advisory critique
(R-0853). `local_candidate_cmd.py` served `local_candidate_generator` — NONE, deliberately
(R-0848). `main_builder_adapter_cmd.py` served `main_builder_adapter` and
`managed_builder_execution_cmd.py` served both `main_builder_adapter` and
`managed_builder_execution` — F085 for bounded subprocess execution and F017 for human
approval (R-0856, R-0860). `overnight_cmd.py` served `overnight_readiness`, which is the one
entry on this list whose idea was CARRIED rather than deleted: DECISION F275 D1 moved its
measured definition set byte-identically into `packages/orchestration/mission_readiness.py`
and it ships as `mission readiness`, the single command id this feature added.
`overnight_mission_cmd.py` served `overnight_mission` — F269, which
`docs/system/vocabulary.md` already records as the feature that builds the contract
(R-0845), with the morning report carried to `mission report` in its degraded form and the
run-keyed addressing deleted (R-0840). `progress_cmd.py` served `progress_ledger` —
`job show --full` and `job evidence`, the mapping F260's own stub fixes (R-0844).
`provider_cmd.py` served both `provider_trust` and `provider_trust_verification` — the Trust
Gate; NONE, deliberately, with R-0866 recording the residue. `repair_loop_v2_cmd.py` served
`repair_loop_v2` — F110, for the repair work item, its route recommendation and its policy
knobs (R-0845). `route_policy_cmd.py` served `worker_registry` — F110, model routing
(R-0865); the user-settable route-policy knobs themselves are among the ideas DELETED rather
than inherited, per R-0831. `self_repair_cmd.py` served `self_repair_proposal` — F017, the
approval gate (R-0845). `tournament_cmd.py` served `model_route_tournament` — F082 (R-0848).
`worker_recommend_cmd.py` served `worker_recommend` — NONE, by DECISION F274 D7, which rules
worker recommendation dies with the cluster; its token mode MOVED to
`packages/orchestration/token_policy.py` because it never belonged to the cluster.

WHAT THIS AMENDMENT DELIBERATELY DOES NOT DO. It provides no stub, no shim, no alias and no
compatibility reader, which AGENTS.md's Scope Control forbids by name and which T001 RULE 3
forbids again. It re-opens no finding: naming an inheritor is not resolving one. It mints no
feature; where the answer is NONE it says NONE. And it adds no module to D3's own list,
because D3's subject is F260's Design list and this amendment's subject is the handlers that
served it — two different sets, and merging them would make D3's own arithmetic unreadable.

HOW TO REVERSE: delete this decision. DECISION F260 D3 stands unedited either way.
AMEND37

## Done when — GATES G1 to G8

Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code
and the real numbers. "Green" as a word is a finding. One line per gate in the
handback.

**G1 TRANSPORT (at C0b).** The committed `.agent/authored/f275-r37.md` and
`.agent/last_block.md` have the SAME sha256 as the reviewer's delegation source,
and resolve to ONE shared git blob. `.agent/last_block.md` is written from
`git cat-file blob HEAD:.agent/authored/f275-r37.md`, never retyped. State that
the chain covers those on-disk artefacts and claims nothing about emitted bytes.

**G2 THE PLAN (at C1).** `.agent/plan.md` is BYTE-EQUAL to the PLAN37 slice as
extracted — same length, same sha256. Report its line count against the
AGENTS.md cap of 50, and `^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2, C3 and C4).** For each of the four appends — RECORD37 and
SLIPS37 at C2, LANDED37 at C3, AMEND37 at C4 — post-blob equals pre-blob then ONE
newline then the slice, with C2's pre-blob lengths given in constraint 3 and the
later two re-baselining on the commit before them; READ BACK the joining byte at
offset len(pre) and report it for each. Then an INDEPENDENT structural reader with
N COUNTED FROM EACH SLICE and not from this block: the last N blank-line units of
the post-blob equal that slice's N paragraphs IN ORDER. Then one negative control
per append, flipping a byte INSIDE THE FIRST appended paragraph, which BOTH readers
must REJECT. `^Gate: F275 R36 ` exactly 1 and
`^## DECISION F275 D20 ` exactly 1 at C4.

**G4 THE OPEN SET (at C4).** BY DISTINCT ID, every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id, read at the base with
`git show 965ea50d:.agent/live_review.md` into memory — never by writing over the
tracked file — and again at C4. Report both. Ids registered this round and ids
resolved this round must both be `[]`. Report SEPARATELY that `R-0870` IS STILL IN
the open set at C4 and carries NO `Done:` line — examined, not assumed.

**G5 THE THREE PAIRS ARE THE AUTHORED BYTES (at C3).** For each pair: the FROM
occurs EXACTLY 1x in its target before the edit and EXACTLY 0x after; the TO occurs
EXACTLY 1x after; and the applied file's post-blob equals its pre-blob with the
FROM span replaced by the TO span and nothing else, proved by reconstructing the
post-blob from the pre-blob and comparing sha256. Then
`python3 -m ruff check tests/conftest.py` — the reviewer read `All checks passed!`
at exit 0. Then the property the conftest repair exists for, which is stronger than
the absence of one name: EVERY entry of `SUBPROCESS_FILES` names a file that exists
on disk at C3. The reviewer measured 21 entries over 20 distinct names, the
duplicate being `test_test_runner.py`, which occurs twice with different trailing
comments and is PRE-EXISTING, harmless in a set literal and deliberately NOT
touched by this round.

**G6 THE SCOPED GATE (at C3).** `python3 -B -m pytest tests/docs/ tests/cli/test_product_spine.py -q`,
which the reviewer read at `371 passed` at exit 0 with the repairs applied. Then
`python3 -B -m pytest tests/ -q --collect-only`, which the reviewer read at
`18366 tests collected` with the repairs applied — the same count as the base,
which is the direct evidence that removing a `SUBPROCESS_FILES` entry changed no
test's collection. Report both readings.

**G7 THE SWEEP THE ROUND EXISTS FOR (at C4).** Re-run the resolution sweep over
the surviving tree: for every module stem this feature deleted, whole-word, over
every tracked file outside `.agent/`, `docs/roadmap/`, `docs/archive/` and
`.data/`, report the FULL hit list — never truncated. The reviewer's reading at
the base, after excluding stems shorter than five characters and the two
English-generic stems `provider` and `progress` that DECISION F275 D16 excluded by
name, is that the surviving hits are exactly the four classes the section "What the
sweep deliberately did not treat as an instance" above names, plus the three PAIR
targets. State whether that holds at C4 and enumerate anything it does not cover.
This gate is NOT a zero-gate: the correct result is a NON-EMPTY list, because a
sentence that names a deleted module AND says it was deleted is the pattern this
repository wants.

**G8 NOTHING ELSE MOVED (at C4).** `.agent/STOP` read FROM DISK: report present
or absent. `git status --porcelain`: EMPTY. `git worktree list`: exactly ONE
entry. `git diff --name-only f4fc3459..C4` is an EXACT SET MATCH against the
`Change:` list above minus `.agent/handoff.md` — report MISSING and EXTRA
explicitly. Per-commit insertions for C0a through C4, each under the DECISION
F104 D1 cap of 500; the handback commit's own numbers are NOT ordered here,
per §3 item 14. Canary `python3 -m pytest tests/cli/test_golden_path.py -q`.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
SESSION 17 of F275 and round 37, the per-commit table with `git diff --numstat`
values in the `+/-` column, one line per gate G1 to G8 with real exit codes, the
item-status table, the open-findings count by distinct id, and the deviations.
State explicitly that R-0870 is NOT resolved, that its fix is marked `Landed:` in
C3 and that the reviewer's `Done:` text is owed at the next gate. Add the one
sentence of context self-assessment amend0905-throughput requires. No PR is
created and nothing is merged: this round is not a closure sequence.
