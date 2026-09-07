STEP — F274 ROUND 7 — the repair round for round 6's G6 FAIL: fix the broken smoke section, then close the blindness that let it through

Goal: repair `scripts/remedy_smoke.sh` section 12ai, which round 6 left importing two symbols it
had just deleted, and then widen the cluster deletion map's walker so that a consumer embedding
first-party python in a NON-PYTHON file under a consumer root can no longer hide from it. Recording
the edge that widened walk newly sees returns `packages.orchestration.context_optimizer` to ONE
consumer, so it is NOT deletable and round 6's zero-edge reading is corrected on disk by the guard
itself. NO CLUSTER MODULE IS DELETED THIS ROUND.

Base commit for every reading in this block: `450365a7214b3d6c04c394a645a5fee65cc00867`.

ROUND 6 FAILED ON G6 AND THE FAULT WAS THE REVIEWER'S, NOT THE WORKER'S. The round 6 block ordered
five deleted symbols to total zero across four roots; the worker measured FIVE, reported the real
number, located them all in `scripts/remedy_smoke.sh`, refused to widen its change set and declared
it. That is exactly right. The reviewer's pre-emission dry run had swept with a file filter of
`.py`, `.ts`, `.tsx` and `.txt`, so a `.sh` file could not appear in it. This round repairs both the
breakage and the blindness.

FRAME CONVENTION. No line of this block is a run of a single repeated character. Every slice is
delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>` and a line reading `END <NAME>`,
and the slice is the bytes BETWEEN those two lines, the leading newline of an appended slice
included. Every FROM/TO pair is delimited by lines reading `FROM <id>`, `TO <id>` and `ENDPAIR <id>`
on their own; the pair's text is the bytes between those markers, and the marker lines are never
written to any file. Each pair's containment reading was MEASURED mechanically before emission and
is printed beside it.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r7.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN7 slice.
C2   Append the RECORD7 slice to `.agent/live_review.md` — books round 6's FAIL verdict and
     registers R-0833 and R-0834.
C3   Append the SLIPS7 slice to `.agent/prose_slips.md`.
C4   THE REPAIR: pairs P1 through P4 against `scripts/remedy_smoke.sh`.
C5   THE GUARD: pairs P5 through P7 against `tests/orchestration/test_cluster_deletion_map.py`, and
     pair P8 against `tests/orchestration/cluster_deletion_map.txt`. ONE commit — the walker and the
     edge it newly sees land together, because the map test reds if either lands alone.
C6   Append the LANDED7 slice to `.agent/live_review.md`.
C7   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must
be current before every commit.


## Change set — these paths and nothing else

  .agent/authored/f274-r7.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  scripts/remedy_smoke.sh
  tests/orchestration/test_cluster_deletion_map.py
  tests/orchestration/cluster_deletion_map.txt


## C4 — the repair, four pairs against `scripts/remedy_smoke.sh`

Each FROM occurs EXACTLY ONCE in that file at the base commit; the reviewer measured each count.
The `decision_queue` half of section 12ai SURVIVES in every one of these pairs, including the
assertion pinning its ordering weight — only the `context_budget` half goes.

P1  TO contains FROM: false  -> REWRITE
FROM P1
    # 12ai. Brain nodes: decision_queue + context_budget (Steps 69, 71)
TO P1
    # 12ai. Brain nodes: decision_queue (Step 69)
ENDPAIR P1

P2  TO contains FROM: false  -> REWRITE
FROM P2
    echo "--- 12ai. Brain decision_queue + context_budget nodes"
TO P2
    echo "--- 12ai. Brain decision_queue node"
ENDPAIR P2

P3  TO contains FROM: false  -> REWRITE
FROM P3
    NT_DECISION_QUEUE, NT_CONTEXT_BUDGET,
    ET_HAS_DECISION_QUEUE, ET_HAS_CONTEXT_BUDGET,
TO P3
    NT_DECISION_QUEUE,
    ET_HAS_DECISION_QUEUE,
ENDPAIR P3

P4  TO contains FROM: false  -> REWRITE
FROM P4
dq = [n for n in graph.nodes if n.type == NT_DECISION_QUEUE]
cb = [n for n in graph.nodes if n.type == NT_CONTEXT_BUDGET]
chk(len(dq) == 1, 'missing decision_queue node')
chk(len(cb) == 1, 'missing context_budget node')
chk(dq[0].id == 'decision_queue', 'bad dq id')
chk(cb[0].id == 'context_budget', 'bad cb id')

dq_edges = [e for e in graph.edges if e.type == ET_HAS_DECISION_QUEUE]
cb_edges = [e for e in graph.edges if e.type == ET_HAS_CONTEXT_BUDGET]
chk(len(dq_edges) == 1, 'missing decision_queue edge')
chk(len(cb_edges) == 1, 'missing context_budget edge')

chk(NT_DECISION_QUEUE in _NODE_TYPE_ORDER, 'missing dq in order')
chk(NT_CONTEXT_BUDGET in _NODE_TYPE_ORDER, 'missing cb in order')

print('    brain nodes: OK (decision_queue + context_budget)')
TO P4
dq = [n for n in graph.nodes if n.type == NT_DECISION_QUEUE]
chk(len(dq) == 1, 'missing decision_queue node')
chk(dq[0].id == 'decision_queue', 'bad dq id')

dq_edges = [e for e in graph.edges if e.type == ET_HAS_DECISION_QUEUE]
chk(len(dq_edges) == 1, 'missing decision_queue edge')

chk(NT_DECISION_QUEUE in _NODE_TYPE_ORDER, 'missing dq in order')

print('    brain nodes: OK (decision_queue)')
ENDPAIR P4


## C5 — the guard, three pairs against the map test and one against the map data

P5 is a REWRITE and not the append it resembles: inserting `import re` between two lines breaks the
FROM's contiguity, so the TO does not contain the FROM verbatim. The reviewer measured that rather
than reading it.

P5  TO contains FROM: false  -> REWRITE
FROM P5
from __future__ import annotations

from pathlib import Path
TO P5
from __future__ import annotations

import re
from pathlib import Path
ENDPAIR P5

P6  TO contains FROM: true  -> APPEND
FROM P6
# Production trees a surviving consumer can live in. `tests/` is deliberately
# excluded: a test of a deleted module is deleted with it and blocks nothing.
CONSUMER_ROOTS = ("packages", "apps", "scripts")
TO P6
# Production trees a surviving consumer can live in. `tests/` is deliberately
# excluded: a test of a deleted module is deleted with it and blocks nothing.
CONSUMER_ROOTS = ("packages", "apps", "scripts")

# A python import statement naming a first-party module, matched as TEXT rather
# than parsed. Finding R-0834: `scripts/remedy_smoke.sh` embeds its checks in
# `python3 -c "..."` heredocs, so the module it imports is real, executed and
# breaks on deletion exactly like an import in a `.py` file — but `ast` cannot
# reach it, because the file it lives in is not python. The walker below is
# therefore deliberately a REGEX over non-python files and deliberately matches
# only the two IMPORT FORMS: a bare mention of a dotted name is not an edge, and
# `cluster_deletion_map.txt` is itself full of bare mentions.
_EMBEDDED_IMPORT = re.compile(
    r"^[ \t]*(?:from|import)[ \t]+(packages\.[A-Za-z0-9_.]+)", re.MULTILINE
)


def embedded_first_party_imports(path: Path) -> set[str]:
    """First-party modules imported by python EMBEDDED in a non-python file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()
    return set(_EMBEDDED_IMPORT.findall(text))
ENDPAIR P6

P7  TO contains FROM: false  -> REWRITE
FROM P7
        for path in sorted((REPO_ROOT / root).rglob("*.py")):
            if path.resolve() in excluded:
                continue
            for dotted in first_party_imports(path):
TO P7
        for path in sorted((REPO_ROOT / root).rglob("*")):
            if not path.is_file() or path.resolve() in excluded:
                continue
            if path.suffix == ".py":
                dotted_names = first_party_imports(path)
            else:
                dotted_names = embedded_first_party_imports(path)
            for dotted in dotted_names:
ENDPAIR P7

P8  TO contains FROM: false  -> REWRITE
FROM P8
packages.orchestration.candidate_quality <- packages/orchestration/ui_server.py
packages.orchestration.dogfood_run <- apps/cli/commands/worker_facade_cmd.py
TO P8
packages.orchestration.candidate_quality <- packages/orchestration/ui_server.py
packages.orchestration.context_optimizer <- scripts/remedy_smoke.sh
packages.orchestration.dogfood_run <- apps/cli/commands/worker_facade_cmd.py
ENDPAIR P8

The map data file is SORTED and the new line is placed by that sort, which is why P8 spans its two
neighbours rather than appending at the end — and why P8 is a REWRITE for the same reason P5 is:
the TO inserts a line BETWEEN the FROM's two lines, so the FROM does not survive contiguously.


## Constraints

1. Apply every slice and every pair BYTE FOR BYTE. Do not reflow, retype, re-indent or "fix" one.
   If something looks wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD7, LANDED7 and SLIPS7 are APPENDS: the target's existing bytes are a byte-exact PREFIX of
   the result and the slice is an exact SUFFIX. Each carries its OWN leading newline, which supplies
   the blank-line separation — ADD NO SEPARATOR of your own. PLAN7 replaces `.agent/plan.md`
   entirely. `.agent/live_review.md` is appended to TWICE this round, at C2 and again at C6; C6's
   base is C2's result.
3. The path set of C0a through C6 is exactly the paths listed under "Change set" other than
   `.agent/handoff.md`, which C7 writes. Nothing outside that list is created, edited or deleted.
4. Every destructive check runs ONLY inside a disposable `git worktree`, never in the primary
   checkout, which satisfies `git status --porcelain` == empty at every commit boundary. Remove and
   prune each worktree you create.
5. Do not write a `Done:` paragraph. The LANDED7 slice's `Landed:` lines are reviewer-authored text
   you apply verbatim; only the reviewer writes `Done:`, at the next gate.
6. Every gate below runs at a commit STRICTLY EARLIER than C7, so the handback can quote each
   result.
7. C4 must not touch the map test and C5 must not touch the smoke script: the two halves are
   separately revertible on purpose, because one is a repair and the other is a new guard.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r7.md` equals `sha256` of
    the committed `.agent/last_block.md`, and both equal the digest the delegation message states.
    Report the digest you measured.

G2  THE TWO RECORD APPENDS, re-derived from the COMMITTED blobs.
    (a) AT C2: `.agent/live_review.md` 543921 -> 554047; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the 10126-byte RECORD7 slice with no separator added. Structural reader
        over the WHOLE appended region: a unit is a maximal run of consecutive non-empty lines;
        COUNT N from the slice itself (do not take it from this block); the file's last N units
        equal the slice's units IN ORDER and everything before them is unchanged. Units 217 -> 220.
        NEGATIVE CONTROL: flip the byte at ZERO-INDEXED BYTE offset 543922 of the post-image — the
        `G` opening the first appended paragraph — and confirm BOTH readers reject it.
    (b) AT C6: 554047 -> 554669; same prefix, suffix and ordered-unit readings against the
        622-byte LANDED7 slice; units 220 -> 222; NEGATIVE CONTROL at zero-indexed byte offset
        554048, the `L` opening the first appended `Landed:` paragraph.
    (c) COUNTS at C6: registrations 66 -> 68, resolutions 3 -> 3, OPEN SET 63 -> 65 BY DISTINCT ID,
        `^Gate: ` 37 -> 38, `^Gate: F274 R6` 0 -> 1, `^- R-0833 — ` exactly 1, `^- R-0834 — `
        exactly 1, `^Landed: ` 31 -> 33.
    Do every flip in memory or in a disposable worktree; the primary checkout stays clean.

G3  THE STATE PROSE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN7 slice, is 43 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md`
    at C3 goes 158733 -> 159553 with the pre-image a byte-exact prefix and each appended line
    occurring once.

G4  THE REPAIR PROVES ITSELF BY RUNNING, at C4. Extract section 12ai's embedded python FROM THE
    COMMITTED `scripts/remedy_smoke.sh` — do not retype it — and EXECUTE it. It must be EXIT 0 and
    print `brain nodes: OK (decision_queue)`. Report the exit code. Then confirm the sweep round 6
    could not pass: over `packages/`, `apps/`, `tests/` and `scripts/`, ALL FILE TYPES and not only
    python, the tokens `NT_CONTEXT_BUDGET`, `ET_HAS_CONTEXT_BUDGET`, `_build_context_budget_node`,
    `_detail_context_budget` and `has_context_budget` now total ZERO. Report the total.

G5  THE EXTENDED GUARD IS LOAD-BEARING, BOTH WAYS, in a disposable worktree at C5. Report the exit
    code of every run, and the UNMUTATED control both before and after the mutations.
    (a) CONTROL: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` EXIT 0.
    (b) RED ONE — the new walker is what produces the new edge: replace the single line
        `    return set(_EMBEDDED_IMPORT.findall(text))` in
        `tests/orchestration/test_cluster_deletion_map.py` with `    return set()`. That exact line
        occurs once in that file at C5. The command must be EXIT 1 reporting `DISAPPEARED (1)` and
        naming `context_optimizer <- scripts/remedy_smoke.sh`. Restore BY EXACT PATH, byte-identical.
    (c) RED TWO — the new walker sees a NEW embedded consumer: append the single line
        `from packages.orchestration.review_bundle import build_review_bundle` to
        `scripts/remedy_smoke.sh`. The command must be EXIT 1 reporting `APPEARED (1)` and naming
        `review_bundle <- scripts/remedy_smoke.sh`. Restore BY EXACT PATH, byte-identical.
    (d) The control returns to EXIT 0 after both restorations.

G6  THE EDGE TRUTH, at C5. Measured edges equal recorded edges at 38. The measured consumers of
    `packages.orchestration.context_optimizer` are EXACTLY `['scripts/remedy_smoke.sh']`, so that
    module is NOT deletable and round 6's zero-edge reading is corrected. The modules with no edge
    are exactly `context_pack`, `review_bundle` and `self_repair_proposal`. The non-`.py` consumers
    the widened walk finds are exactly `['scripts/remedy_smoke.sh']`. Report all four readings.

G7  THE SUITES AND THE CEILING, run serially in the primary checkout at C6.
    `tests/orchestration/test_cluster_deletion_map.py` 3, `tests/orchestration/test_import_reachability.py` 3,
    `tests/test_remedy_smoke_script.py` 191, `tests/orchestration/test_project_brain.py` 82, and the
    canary `tests/cli/test_golden_path.py` 42 — each EXIT 0, and report each NUMBER. Then
    `python3 -m ruff check .` is 26 errors in a disposable worktree checked out at
    `450365a7214b3d6c04c394a645a5fee65cc00867` and RUN FROM THAT WORKTREE'S OWN ROOT, and 26 in the
    primary checkout at C6; `tests/orchestration/test_ci_budgets.py` EXIT 0 at 10.

G8  THE TREE, at C6. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY;
    `git worktree list` the same count as before your first worktree and after your last prune;
    `git diff --name-only 450365a7214b3d6c04c394a645a5fee65cc00867..<C6>` naming exactly the paths
    of constraint 3 and nothing else; every commit C0a through C6 single-parent. Report the
    INSERTION count of each commit C0a through C6 — the `+` column only, per AGENTS.md DECISION
    F104 D1. Do not report C7's own numbers; the reviewer measures them at the next gate.


## Handback — rewrite `.agent/handoff.md` at C7, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits
table with its `+/-` column taken from `git diff --numstat` and compared cell by cell against the
insertion counts G8 reports, the changed-files table, ONE LINE PER GATE G1 through G8 with its real
result, the deviations, the open-findings count, and the next expected action. No length cap. Name
the SESSION NUMBER as SESSION 4 of feature F274 and the round as 7. State the open-findings count
as the number G2(c) MEASURED. Add the one sentence of context self-assessment
amend0905-throughput requires.

DECLARE, do not silently repair: if any gate goes red, or any pair or slice does not apply as
described, report the real command, the real exit code and the real output and say what you did.
Round 6's G6 red is in this record precisely because its worker did that.


BEGIN PLAN7 sha256=ab2fd8b46fcdcf1e6efddf66142eee5be02edb133073f7557a88cdf97d4b5576 bytes=2512
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 7, the repair round for round 6's FAIL on gate G6. Cut the `context_budget` half of
`scripts/remedy_smoke.sh` section 12ai, which round 6 left importing two deleted symbols, and then
widen the deletion map's walker so a consumer that embeds first-party python in a non-python file
under a consumer root can no longer hide from it. Recording the edge that walk newly sees returns
`context_optimizer` to ONE consumer, so it is NOT deletable and round 6's zero-edge reading is
corrected on disk. Book round 6's FAIL verdict, register R-0833 and R-0834, and mark both Landed.

## Next Steps

1. Cut section 12ah of `scripts/remedy_smoke.sh`, the last recorded consumer of
   `context_optimizer`, in the round that takes that module to zero for real.
2. `worker_recommend`'s three remaining edges, in `agent_loop.py`, `autonomy_loop.py` and
   `dashboard.py`. These are LIVE RUNTIME CALLS rather than read-only views, so a DECISION naming
   what inherits worker recommendation is authored before the cut.
3. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision DECISION
   F274 D2 rules.
4. The remaining edges, of which `packages/orchestration/ui_server.py` holds the most by far.
5. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`.
6. Draft DECISION F260 D3, the deletion paragraph. R-0832's and R-0834's fix clauses bind it.
7. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
8. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map is now proven blind twice: to event-name coupling (R-0832) and, until this round, to
  embedded python (R-0834). Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN7


BEGIN RECORD7 sha256=fc0342bea4038e7d8a26a3f87cfd0a945d9717308847373da2590e40a071078c bytes=10126

Gate: F274 R6 — the F274 round 6 entry. VERDICT FAIL, ON GATE G6 AND ON NOTHING ELSE, AND THE FAILURE IS THE REVIEWER'S AUTHORING ERROR RATHER THAN THE WORKER'S EXECUTION. Every gate was re-run by the reviewer itself, in the primary checkout and in a disposable worktree at `1755b6dbd387854b866fd6d1cf0a7647c1713044`, against the COMMITTED blobs rather than the working tree. Range `fcb77eab139faec83ffd88963bd5888d59dad677`..`450365a7214b3d6c04c394a645a5fee65cc00867`, seven commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, with the path set over `fcb77eab139faec83ffd88963bd5888d59dad677`..`1755b6dbd387854b866fd6d1cf0a7647c1713044` naming exactly the fourteen declared paths and nothing else. G1 TRANSPORT IS A REAL CHAIN AND FOR ONCE IT COVERS THE EMITTED BYTES: the block travelled as a FILE the worker copied rather than as text it retyped, so the reviewer's own scratch original `.remedy-wt/f274-r6-block.md`, written and hashed BEFORE delegation, is BYTE-IDENTICAL to the committed `.agent/authored/f274-r6.md` and `.agent/last_block.md`, all three 27569 bytes at `bd1d2cb8c10835c99c4ae7a0a2fcad4603febe145a30868f4ebe7af881f4b176`. G2 THE RECORD APPEND at `f6b6f7528f707101f163ec2672c470b0d98df5de`, re-derived from the committed blobs: 535659 to 543921 bytes, pre-image a byte-exact PREFIX, post-image equal to pre plus the 8262-byte RECORD6 slice with no separator added; units 215 to 217 under the maximal-run-of-non-empty-lines definition, N counted from the slice as 2, the last two units matching IN ORDER and everything before them unchanged, and the control flipped at zero-indexed BYTE offset 535660 — the `G` opening the first appended paragraph — rejected by BOTH readers; registrations 65 to 66, resolutions 3 to 3, OPEN SET 62 TO 63 BY DISTINCT ID, `^Gate: ` 36 to 37, `^Gate: F274 R5` 0 to 1, `^- R-0832 — ` exactly 1. G3: `.agent/plan.md` is byte-equal to its slice at 43 lines against the cap of 50 and carries both mandated headings; `.agent/prose_slips.md` 158178 to 158733 bytes with each appended line occurring once. G4 THE RATCHET HELD BOTH WAYS in the reviewer's own disposable worktree: control EXIT 0 at 6 passed, measured edges equal recorded edges at 37, the measured consumers of `packages.orchestration.context_optimizer` the EMPTY LIST, restoring the deleted map line EXIT 1 reporting `DISAPPEARED (1)` and naming that edge, appending an import to `packages/orchestration/ui_server.py` EXIT 1 reporting `APPEARED (1)`, each mutated file restored byte-identically by exact path and the control returning to EXIT 0. G5 THE ORDERED COUNTS ARE EXACT: `tests/orchestration/test_project_brain.py` 84 to 82, `tests/ui_server/test_brain_view_model.py` 39 to 38, `tests/ui_server/` 514 to 513, the four suites that match only a SURVIVING spelling unmoved together at 108, and the canary at 42. G7 THE LINT CEILING HELD at 26 errors at the base in a worktree run from its own root and 26 in the primary checkout, so DECISION F083 D5's frozen ceiling is untouched, and `test_ci_budgets.py` EXIT 0 at 10 passed. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 before and after. G6 IS THE ONE THAT FAILED, AND IT FAILED HONESTLY: it ordered the five deleted node symbols to total ZERO across `packages/`, `apps/`, `tests/` and `scripts/`, and the worker MEASURED FIVE, reported the real number, located every one of them in `scripts/remedy_smoke.sh`, declared it as a deviation and DID NOT REPAIR IT because that path was outside the change set the block bound it to. The reviewer independently re-measured the same reading: 30 occurrences across six files at `fcb77eab139faec83ffd88963bd5888d59dad677` and 5 at `1755b6dbd387854b866fd6d1cf0a7647c1713044`, all five in that one file, so all twenty-five in-scope occurrences went and only the out-of-scope file remains. THE CAUSE IS THE REVIEWER'S PRE-EMISSION DRY RUN: it swept for the five symbols with a file filter of `.py`, `.ts`, `.tsx` and `.txt`, so a `.sh` file could not appear in its result, and the block's change set was therefore authored one file short. The worker did exactly what this workflow asks of it — measure, report the real number, refuse to widen scope, declare. TWO FINDINGS ARE MINTED AND THEY ARE THE TWO PARAGRAPHS BELOW: R-0833 for the breakage on disk and R-0834 for the guard that could not see it. NO FINDING IS RESOLVED BY THIS GATE. The reviewer additionally sustains the worker's deviation D2 as a REVIEWER PROSE SLIP rather than an id, per amend0827 rule 2, because it left nothing wrong on disk: the block named `brain_viewer.py`'s two entries a "layer entry and weight entry" where the file calls those maps `_ZONE_MAP` and `_LAYER_MAP`, and named `ui_view_model.py`'s two integer maps "the two weight maps" where the file calls them `_RANK_MAP` and `_ZOOM_MAP`; the KEYS and the COUNTS the block gave were exact, so the site set was never ambiguous and the worker applied it as specified.

- R-0833 — Medium, THE BRANCH TIP SHIPS A SMOKE-SCRIPT SECTION THAT EXITS NON-ZERO ON AN IMPORT OF SYMBOLS ROUND 6 DELETED, AND NO SUITE CATCHES IT. Raised by the worker at the F274 round 6 handback as deviation D1, measured independently by the reviewer, and booked by round 7's first substantive commit. THE MEASUREMENT, taken at `450365a7214b3d6c04c394a645a5fee65cc00867`. `scripts/remedy_smoke.sh` section 12ai runs an embedded `python3 -c` whose first statement imports `NT_DECISION_QUEUE`, `NT_CONTEXT_BUDGET`, `ET_HAS_DECISION_QUEUE` and `ET_HAS_CONTEXT_BUDGET` from `packages.orchestration.project_brain`. Round 6 deleted the second and fourth of those, so that import is now `ImportError: cannot import name 'NT_CONTEXT_BUDGET' from 'packages.orchestration.project_brain'`, which the reviewer reproduced by executing the statement directly. The section's own body then reads the `context_budget` node and its edge and asserts each is present, so even a repaired import would fail on the node that no longer exists. `tests/test_remedy_smoke_script.py` is EXIT 0 at 191 passed at that same commit, so the suite does NOT reach this: it checks the script's structure and not its execution, which is why a green round shipped a red script. THE SEVERITY IS MEDIUM RATHER THAN HIGH because the product runtime is unaffected — the deleted node was a diagnostic view and no shipped code path imports these symbols — but the state on disk is genuinely wrong under `scripts/`, which is what amend0827 rule 2 spends an id on. FIX, discharged in F274 round 7 in the commit that this record's `Landed: R-0833` line names: cut the `context_budget` half of section 12ai and keep the `decision_queue` half, which is the half whose subject still exists — the import tuple loses two names, the node, edge and order assertions for `context_budget` go, and the section's comment, banner and success line stop naming it. The `decision_queue` assertions are UNCHANGED, including the one pinning the ordering weight 25.

- R-0834 — High, THE CLUSTER DELETION MAP WALKS `*.py` ONLY, SO A CONSUMER THAT EMBEDS FIRST-PARTY PYTHON IN A NON-PYTHON FILE UNDER A CONSUMER ROOT IS INVISIBLE TO IT — WHICH BOTH HID R-0833 AND MADE ROUND 6's ZERO-EDGE READING FALSE OF THE TREE. Raised by the reviewer at the F274 round 6 gate, from the worker's D1 measurement, and booked by round 7's first substantive commit. THE RULE. `tests/orchestration/test_cluster_deletion_map.py` declares `CONSUMER_ROOTS = ("packages", "apps", "scripts")` and then walks each root with `rglob("*.py")`, so `scripts` is named as a place a surviving consumer may live while every non-python file in it is skipped; DECISION F274 D2 rules the deletion bounded by the edges that walk produces. THE MEASUREMENT, taken at `450365a7214b3d6c04c394a645a5fee65cc00867`. `scripts/remedy_smoke.sh` section 12ah contains the statement `from packages.orchestration.context_optimizer import explain_context, optimize_context`, executed inside a `python3 -c` heredoc. That is a real, live, first-party import of a cluster module by a file under a CONSUMER_ROOT, and the map records NO edge for it. The consequence is not hypothetical and is not confined to R-0833: round 6's own goal, its plan slice and its `Gate: F274 R6` verdict all read `context_optimizer` as having ZERO consumer edges and therefore as the fourth module the deletion may take, and that reading is FALSE OF THE TREE — deleting `packages/orchestration/context_optimizer.py` on the map's authority would break section 12ah exactly as round 6 broke section 12ai. This is a gate over production code shown to be BLIND to a real coupling, and unlike R-0832's event-name shape it is blind to an ordinary `import` statement, which is the very thing the walker exists to find. THE REACH IS BOUNDED AND WAS MEASURED RATHER THAN ASSUMED: of the 240 tracked non-`.py` files under `packages/`, `apps/`, `scripts/` and `tests/`, exactly three name a cluster module at all, and two of those are the data files `tests/orchestration/cluster_deletion_map.txt` and `tests/orchestration/import_reachability_allowlist.txt`, which are bare dotted-name inventories under a root that is deliberately not a CONSUMER_ROOT. `scripts/remedy_smoke.sh` is the only real instance, and it is the one that broke. FIX, discharged in F274 round 7 in the commit that this record's `Landed: R-0834` line names: widen the walker to every file under a CONSUMER_ROOT, keep `ast` for `.py`, and read a non-python file with a regex that matches ONLY the two python IMPORT FORMS at line start, so that a bare mention of a dotted name is not an edge — `cluster_deletion_map.txt` is itself full of bare mentions and a substring sweep would turn the map into its own consumer. Record the newly visible edge in the map in the same commit, which returns `context_optimizer` to ONE consumer and the zero-edge set to `context_pack`, `review_bundle` and `self_repair_proposal`. This finding does not license widening the walker to non-import syntax: R-0832's event-name coupling is a different defect with a different fix, and the two are deliberately not merged.
END RECORD7


BEGIN LANDED7 sha256=935ddc6df4f195249384b2f7afd535f97cc639f11a4f6a949e7efa9191901a04 bytes=622

Landed: R-0833 — the `context_budget` half of `scripts/remedy_smoke.sh` section 12ai is cut and the `decision_queue` half is unchanged, in the commit this round's block names C4; the section's embedded python, extracted from the committed script and executed, is EXIT 0.

Landed: R-0834 — `measured_edges` in `tests/orchestration/test_cluster_deletion_map.py` now walks every file under a CONSUMER_ROOT, reading `.py` with `ast` and every other file with an import-form regex, and the edge that walk newly sees is recorded in `tests/orchestration/cluster_deletion_map.txt`, in the commit this round's block names C5.
END LANDED7


BEGIN SLIPS7 sha256=f1745333fb56148cfff1cf7506a7caafc6432a584f44dba91ce4914240fdceed bytes=820

2026-09-08 · F274 R6 · The round 6 block named `brain_viewer.py`'s two entries a "layer entry and weight entry" where the file calls those maps `_ZONE_MAP` and `_LAYER_MAP`, and named `ui_view_model.py`'s two integer maps "the two weight maps" where the file calls them `_RANK_MAP` and `_ZOOM_MAP`; the keys and the counts were exact, so the site set was never ambiguous and the worker applied it as specified.

2026-09-08 · F274 R6 · The reviewer's pre-emission dry run swept for the five deleted node symbols with a file filter of `.py`, `.ts`, `.tsx` and `.txt`, so `scripts/remedy_smoke.sh` could not appear in its result and the block's change set was authored one file short — the cause of round 6's G6 red, registered as R-0833 and R-0834 rather than left here, because both left real state wrong on disk.
END SLIPS7
