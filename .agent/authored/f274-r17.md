STEP — F274 ROUND 17 — execute the split: register F275 in one atomic ledger commit, and give F274 its Built State

Goal: DECISION F274 D8 landed in round 16 and ruled the split; this round EXECUTES it. It books
round 16's PASS verdict, registers feature F275 for the remaining scope in ONE atomic ledger commit,
and appends the Built State section F274's file has never had and that operator order
amend0906-split-placement requires to name which slices moved. NO LINE UNDER `packages/`, `apps/`
OR `scripts/` MOVES, and gate G7 proves it.

Base commit for every reading in this block: `7bd19462`.

WHY THE REGISTRATION IS ONE COMMIT AND MAY NOT BE SPLIT. `tests/docs/test_docs_consistency.py`
pins the feature ledger from four directions at once: the count of feature detail files and the
count of STATUS entries must both equal `TOTAL_FEATURES`, the ids must be contiguous from 1 to
`TOTAL_FEATURES` in BOTH, each file's `T<n>_` prefix must match its STATUS line's enclosing tier
heading, and the README's "N of M registered items accepted." line must carry M equal to
`TOTAL_FEATURES`. Landing the STATUS line, the feature file, the pin and the README counters in
separate commits therefore leaves an intermediate commit at which `tests/docs/` is RED, whatever
the order. They go together, with the six `Depends on` edits, as C3.

THE NEW FEATURE FILE DOES NOT TRAVEL INSIDE THIS BLOCK. It is 136 lines, which would push the
block over its 490-line budget, so it travels as its own digest-stamped scratch artefact and is
COPIED rather than retyped or extracted:

  path:   /home/decodeux/Repos/remedy/.remedy-wt/f274-r17-F275FILE.txt
  sha256: ba5445586c11c28909aab801be1e560e06f0a4bceb31a756eadba298f1f6568d
  bytes:  9701

Copy it with `shutil.copyfile(src, dst)` and NOT with `shutil.copy2` or any archive helper: the
property that must survive is BYTE EQUALITY of the file contents and nothing else, `copyfile`
copies contents alone, and G4 gates that property by digest rather than trusting the call. The
destination is `docs/roadmap/features/T2_F275.md`, which does not exist at the base.

WHAT THE REVIEWER RAN BEFORE AUTHORING. Every pair below, the file copy and both appends were
applied to a disposable worktree at the base commit above, and every numeral the gates order was
read out of that applied tree: the per-pair base and post counts, the copied file's digest, both
append arithmetics with their negative controls, and the four gate suites. The suite figures are
reference values a correct round reproduces, not predictions. The reviewer also confirmed in that
tree that the FIRST unchecked STATUS line becomes F275's, which is the property
amend0906-split-placement exists to produce.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines, its leading
newline included, and marker lines never reach any file. No line of this block's FRAME — every
line outside a BEGIN/END pair — is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r17.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN17 slice.
C2   Append the RECORD17 slice to `.agent/live_review.md` — books round 16's PASS verdict.
C3   THE ATOMIC REGISTRATION: copy the F275 feature file into place and apply every pair of
     PAIRS17. ONE commit, ten paths.
C4   Append the BUILTSTATE slice to `docs/roadmap/features/T2_F274.md`.
C5   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must
be current before every commit (§3 item 23). C2 precedes C3 because verdicts persist first
(§4 item 4). C4 follows C3 because the Built State names F275, which C3 creates.


## Change set — these paths and nothing else

  .agent/authored/f274-r17.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/handoff.md
  docs/roadmap/STATUS.md
  docs/roadmap/features/T2_F275.md
  docs/roadmap/features/T2_F274.md
  docs/roadmap/features/T2_F261.md
  docs/roadmap/features/T2_F263.md
  docs/roadmap/features/T2_F268.md
  docs/roadmap/features/T2_F269.md
  docs/roadmap/features/T2_F270.md
  docs/roadmap/features/T2_F271.md
  README.md
  tests/docs/test_docs_consistency.py


## C3 — the pairs

PAIRS17 carries them. `--- S<n> FILE <path>` opens a pair against ONE file and
`--- S<n> FILES <path> <path> …` opens a pair applied SEPARATELY to EACH of the listed files;
`--- S<n> FROM` opens its FROM block and `--- S<n> TO` opens its TO block; a block is every
following line up to the next marker line, and `--- S5 END` closes the last one. Replace each FROM
block with its TO block ONCE per file, keeping line endings. Marker lines reach no file.

PAIR SHAPES, MEASURED MECHANICALLY AND RECORDED AS THE TEST'S OWN OUTPUT RATHER THAN AS A LABEL
(§3 item 15). The reviewer ran the containment test on every pair at the base commit:
  S1  TO contains FROM: true   -> APPEND
  S2  TO contains FROM: false  -> REWRITE
  S3  TO contains FROM: false  -> REWRITE
  S4  TO contains FROM: false  -> REWRITE
  S5  TO contains FROM: true   -> APPEND
At that same commit each FROM block occurs EXACTLY ONCE in each file the pair names — one
occurrence in `STATUS.md`, one and one in `README.md` for S2 and S3, one in the pin file, and one
in each of S5's six feature files.

THE TWO APPEND-SHAPED PAIRS CARRY NO "FROM 0x" OBLIGATION and G4 does not order one, because that
count is unattainable by construction when the TO contains the FROM (§4 item 9). For S1 and S5 the
ordered reading is FROM exactly 1 and TO exactly 1 after the edit; for the three REWRITEs it is
FROM 0 and TO 1.

WHAT EACH PAIR DOES. S1 inserts F275's STATUS line DIRECTLY after F274's, inside the same
`## Tier 2` heading, which is what makes the file's `T2_` prefix agree with its STATUS tier and
what puts F275 ahead of every other unchecked feature under Rule A5. S2 and S3 move the README's
two registered-item counters, the prose line's M and the Tier 2 row's Total; the Done column is
pinned to accepted `[x]` lines only and a registration never moves it. S4 moves the
`TOTAL_FEATURES` pin and extends the dated comment that explains every registration above it. S5
adds F275 beside F274 in the `Depends on` line of every OPEN feature that names F274 — the six
files it lists, which are all of them; `T2_F272.md` also names F274 and is deliberately excluded,
because it is `[x]` and a closed feature's dependency line is history.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks
   wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD17 and BUILTSTATE are APPENDS: the target's existing bytes are a byte-exact PREFIX of the
   result and the slice is an exact SUFFIX of it. Each carries its OWN leading newline — ADD NO
   SEPARATOR of your own, and do not strip one. PLAN17 REPLACES `.agent/plan.md` entirely and has
   no leading newline. PAIRS17 and FORTSCHRITT are appended to no file.
3. Extract each slice from the COMMITTED `.agent/authored/f274-r17.md` by its BEGIN and END marker
   lines and apply it with a script. Do not retype a slice by hand into a target.
4. The path set of C0a through C4 is exactly the "Change set" paths other than
   `.agent/handoff.md`, which is C5's. C3's own path set is exactly ten paths.
5. NO DESTRUCTIVE CHECK RUNS IN THE PRIMARY CHECKOUT. Any mutation or red control runs only inside
   a disposable `git worktree`, which is removed and pruned; `git status --porcelain` is empty at
   every commit boundary. There are 14 worktrees registered before you start.
6. Run every suite of G5 and G7 IN THE PRIMARY CHECKOUT, serially, one suite per invocation.
7. Every gate below runs at a commit STRICTLY EARLIER than C5, so the handback can quote each
   one's real result (§3 item 31). Take G2, G3, G4 and G6 at C1, C2, C3 and C4 respectively; take
   G5 at C3; take G1, G7 and G8 at C4.
8. Do not write a `Done:` paragraph or a finding registration of your own. This round registers no
   finding and resolves none; the open set is 63 by distinct id at both ends of it.
9. Report each gate's REAL result, including a failure. A gate that fails is a handback that says
   so; it is never a gate quietly re-scoped until it passes.


## The slices

BEGIN PLAN17 sha256=e5a2bcd757ebbc30b685b3b15f89985ad7ff74e2b7196d5140932454bdd85113 bytes=2142
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8 — the split-and-close default operator
amendment amend0905-throughput makes standing at the soft limit, which this feature reached at
session seven of seven.

## Current Step

The registration round: book round 16's PASS verdict, then register F275 in ONE atomic ledger
commit — the STATUS line directly after F274's inside the same Tier 2 heading, the feature file,
the `TOTAL_FEATURES` pin and the README counters, plus the `Depends on` edit in every open
feature naming F274 — and give F274's own file a Built State section naming which slices moved.

## Next Steps

1. The integration-gate round: the full suite per docs/agents/integration_gate.md, whose verdict
   closure precondition 2 re-confirms.
2. The self-use item closure precondition 6 requires. Every queue item is consumed, so
   `generate_and_append_if_empty` runs FIRST; whatever it yields is planned and run to the normal
   approval gate, and every defect its findings reader returns is registered before the close.
3. The closure sequence itself: the remaining verdict bookings, the ledger rotation by
   `scripts/rotate_live_review.py` as its own commit, the evidence job, the fresh review zip, the
   STATUS `[x]` flip with the README sync in one commit, and the pull request.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
- The registration's four ledger pins must land in ONE commit; splitting them leaves an
  intermediate state in which `tests/docs/` is red.
END PLAN17

BEGIN RECORD17 sha256=075b2f2184a041f3ed723d89a787ef4df5624357f844754277c835eba6c72b26 bytes=6020

Gate: F274 R16 — the F274 round 16 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout. Range `2cc1211f`..`7bd19462`, six commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4. THIS WAS THE FIRST ROUND OF F274's CLOSURE SEQUENCE, which is the one place operator amendment amend0827-process-diet rule 1 permits a round whose change set is bookkeeping and rulings; every other round of this feature moved product state. G1 TRANSPORT covers the chain this workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37 and NOT the emitted bytes: the reviewer's scratch original `.remedy-wt/f274-r16-FINAL.md`, hashed BEFORE delegation and verified by the worker as its first action, and both committed copies are all 29748 bytes at `d111b6120029677be10d67a71c5edce05ec5106684d0de951f2b0d5a3d2b6c39`. G2 THE PLAN at `cf756da1`: `.agent/plan.md` byte-equal to its slice at 2086 bytes and 37 lines against the AGENTS.md cap of 50, carrying exactly one `## Goal` and one `## Next Steps`. G3 THE RECORD APPEND at `1b74f069`: 609858 to 616218 bytes, exact append, N counted as 2, the last two blank-line units equal to the slice's two paragraphs IN ORDER, and the control flipping one byte inside the FIRST appended paragraph at offset 609859 rejected by BOTH readers; a second control inside the LAST appended paragraph at offset 613992 is also rejected by the structural reader, so the second reading covers the WHOLE appended region as finding R-0631 requires rather than degenerating to one paragraph. Units 239 to 241, `^Gate: ` 46 to 47, `^Gate: F274 R15 ` 0 to 1, registrations 70 to 70, distinct resolutions 7 to 7, OPEN SET 63 TO 63 BY DISTINCT ID. G4 THE DECISION APPEND at `26e2a0c3`: 911446 to 919768 bytes, exact append, N counted as 10, the last ten units equal to the slice's paragraphs in order, controls at offsets 911447 and 919242 — the first and the last appended paragraphs — both rejected by the structural reader, units 2000 to 2010, `^## DECISION F274 D8 ` 0 to 1. G5 THE SUITES, each run ALONE by the reviewer in the primary checkout: `tests/ui_server/test_dashboard_contract.py` 74 passed and 0 SKIPPED, which is the PRIMARY figure the block ordered rather than the 73-and-1 any fresh worktree gives, the round 13 defect deliberately not repeated; the orchestration trio 59 passed; `tests/docs/` 303 passed; and the canary at 42 passed. G6 THE SCOPE GUARD: `git diff --name-only 2cc1211f..26e2a0c3` names exactly five paths and every one begins `.agent/` — the authored block, `decisions.md`, `last_block.md`, `live_review.md` and `plan.md` — with ZERO paths under `packages/`, `apps/`, `tests/`, `scripts/`, `docs/` or `README.md`, and `tests/orchestration/cluster_deletion_map.txt` is BYTE-IDENTICAL at the base and at C3, both `7fbf3909fd6d094e0ab3654e8842222a1adf6a51cd6c74bf119b1f7c256d5155`, read with `git show` and never by writing into the checkout. THE BASE-ANCHORED RANGE IS THE CORRECT ONE HERE and is the reading R-0819's fix clause permits, because the claim is about the WHOLE ROUND's change set rather than one commit's path set. G7 THE PER-COMMIT NUMBERS for C0a through C3 and NOT for the handback commit: insertions 340, 297, 16, 4 and 102, every one under the DECISION F104 D1 cap of 500; the `## Commits` table of the handback carries `340/0`, `297/298`, `16/21`, `4/0` and `102/0`, which the reviewer confirmed are the `git diff --numstat` columns CELL FOR CELL and not the files' line counts before and after — the two diverge for the full-file rewrites C0b and C1, which is the §3 item 28 defect this gate exists to catch. G8 THE TREE AND THE RECORD-SLICE SCAN: `git status --porcelain` EMPTY, `git ls-files .remedy-wt` EMPTY, worktrees 14 at both ends, and every one of the four slices in the committed authored blob matches its own BEGIN marker's digest and byte count; with backtick-quoted spans deleted, the unquoted `\bHEAD\b` count is ZERO in RECORD16 and ZERO in DECISION16, which is what finding R-0586's scan requires of text bound for an append-only record. FIVE DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL FIVE, AND NONE IS A DEFECT OF THE ROUND OR OF THE BLOCK. The first is procedural and identical to round 15's: the session's shell guard refuses `$?` BY FORM, so every exit code came through a Python runner invoking the identical command and printing the real return code, and no exit code was inferred. The second is STRICTER than the block, not looser: the worker created no disposable worktree because the round ordered no product mutation and both negative controls were computed in memory on a copy of the committed post-image, so nothing was mutated on disk at all. The third records that the round's scratch scripts live under the gitignored `.remedy-wt/`, which `git ls-files` confirms are untracked. The fourth observes that `.agent/plan.md` was one round stale at the C0a and C0b boundaries; that is the case §3 item 23 EXPLICITLY PERMITS — only the two block-save commits, which write nothing but the block itself, may precede the plan update — so the block was compliant and the worker was right to flag rather than reorder. The fifth is a measurement the block did not ask for and the reviewer sustains it: the worker independently reproduced every load-bearing numeral of DECISION F274 D8 at the base — twenty map edges, eleven distinct cluster modules as targets and therefore thirteen of twenty-four edge-free, `provider_trust` the target of seven, the by-consumer split of four, four, three, two, two, two, one, one and one across nine files, 130 commits from the fork point, 46 files at 1269 insertions and 1340 deletions, and R-0830 through R-0836 registered with R-0833 through R-0836 resolved — and all of them are exact against the reviewer's own readings. NO FINDING IS REGISTERED BY THIS GATE AND NO NEW ID IS MINTED, so the open set stands at 63 by distinct id and the next free id is R-0837.
END RECORD17

BEGIN PAIRS17 sha256=393fca353de45b80ae7cf6be6d55bb8f2b3fd33f5973f2dfe9ed3627294be4c4 bytes=1774

--- S1 FILE docs/roadmap/STATUS.md
--- S1 FROM
- [~] F274 — One world completion, part two — the atomic record flip and the cluster deletion
--- S1 TO
- [~] F274 — One world completion, part two — the atomic record flip and the cluster deletion
- [ ] F275 — One world completion, part three — the cluster deletion, the atomic record flip and the classic runner
--- S2 FILE README.md
--- S2 FROM
75 of 274 registered items accepted.
--- S2 TO
75 of 275 registered items accepted.
--- S3 FILE README.md
--- S3 FROM
| 2 | Minimal Self-Build Runtime | 18 | 27 |
--- S3 TO
| 2 | Minimal Self-Build Runtime | 18 | 28 |
--- S4 FILE tests/docs/test_docs_consistency.py
--- S4 FROM
#: directly after its parent per amend0906-split-placement; see T2_F274.md.
TOTAL_FEATURES = 274
--- S4 TO
#: directly after its parent per amend0906-split-placement; see T2_F274.md.
#: One more, F275 (one world completion part three: the cluster deletion, the
#: atomic record flip and the classic runner), was registered on 2026-09-08 by
#: DECISION F274 D8, which split it off F274 at the standing soft limit of 7
#: sessions and 25 rounds and placed it directly after its parent per
#: amend0906-split-placement; see T2_F275.md.
TOTAL_FEATURES = 275
--- S5 FILES docs/roadmap/features/T2_F261.md docs/roadmap/features/T2_F263.md docs/roadmap/features/T2_F268.md docs/roadmap/features/T2_F269.md docs/roadmap/features/T2_F270.md docs/roadmap/features/T2_F271.md
--- S5 FROM
F274 (one world completion part two — the atomic record flip and the cluster deletion)
--- S5 TO
F274 (one world completion part two — the atomic record flip and the cluster deletion), F275 (one world completion part three — the cluster deletion, the atomic record flip and the classic runner)
--- S5 END
END PAIRS17

BEGIN BUILTSTATE sha256=d2fd4e3f7072f275cbc40afd8586d5408bf33256cb65b2db120277d20ae07cc4 bytes=2672

## Built State (2026-09-08, at the close)
What F274 has on disk at its close, so a later reader need not reconstruct it from the
ledger. DECISION F274 D8 in `.agent/decisions.md` is the ruling that closed the feature here
and split the rest; this section is that ruling's on-disk index.

BUILT. The prototype-cluster deletion map, `tests/orchestration/cluster_deletion_map.txt`,
GENERATED from the live import graph rather than typed and held against it in BOTH
directions by `tests/orchestration/test_cluster_deletion_map.py`, so a re-inserted edge
reddens a test instead of passing unnoticed. The import-reachability ratchet,
`tests/orchestration/test_import_reachability.py` with its 326-line allowlist, ruled a
RATCHET rather than a one-shot gate by DECISION F274 D1. The cockpit and command-layer edge
cuts: `packages/orchestration/ui_server.py` lost 458 lines and gained none, the `feature`
command group was deleted whole at 101 lines, and `apps/cli/commands/context.py` and
`apps/cli/commands/worker.py` were cut into the per-command modules their surviving halves
needed. The retirement of `packages.orchestration.worker_recommend`, which holds no recorded
consumer edge and is deletable. Seven dated rulings, DECISION F274 D1 through D7. Seven
findings registered, R-0830 through R-0836, of which R-0833, R-0834, R-0835 and R-0836 are
resolved and R-0830, R-0831 and R-0832 stand open as documented risks.

WHICH SLICES MOVED TO F275, which operator order amend0906-split-placement requires this
section to state. ALL THREE MOVED, in substance, and none was started here. T003's deletion
moved whole and is F275's T001: nothing was deleted in this feature, only made SAFE to
delete, and at this close the map records twenty surviving consumer edges across eleven of
the twenty-four cluster modules, with `packages.orchestration.provider_trust` alone the
target of seven. The two carry-overs F260's Design section names — overnight readiness and
report becoming `mission readiness` and `mission report`, and the route-policy knobs checked
against F110's config keys — moved with that slice, unstarted, and DECISION F274 D4 holds
two `ui_server.py` cockpit sections hostage to them. T001, the flip measurement and the cap
ruling DECISION F272 D15 demands before any site moves, moved unstarted and is F275's T002.
T002, the classic runner and the resolver collapse, moved unstarted and is F275's T003.

WHAT DID NOT MOVE is everything in the BUILT paragraph above. F275 inherits a bounded,
machine-checked work list and seven dated rulings, not a fresh investigation — which is the
condition that made this close self-consistent rather than half-performed.
END BUILTSTATE

BEGIN FORTSCHRITT sha256=d474c5b479114768948e313ee9a2a577e063493444f8b41126c1851aa19046b9 bytes=239
Fortschritt: F274 schließt bei ~35 % des ursprünglichen Umfangs, der Rest ist als F275 registriert (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · Cluster-Löschung, Record-Flip und Classic-Runner → F275) — Schätzung
END FORTSCHRITT


## Done when

G1  TRANSPORT, two digest comparisons, at C4. First: `.agent/authored/f274-r17.md` and
    `.agent/last_block.md` are BYTE-IDENTICAL to each other and to the reviewer's scratch original
    at `/home/decodeux/Repos/remedy/.remedy-wt/f274-r17-FINAL.md`; report the sha256 and byte count
    of all three. Second: the committed `docs/roadmap/features/T2_F275.md` is byte-identical to the
    scratch source named above the Bundle; report its sha256 and byte count against the declared
    `ba54455…f6568d` and 9701. This proof covers the chain this workflow can walk — the reviewer's
    originals, the saved copy, its mirror, the committed file — and claims nothing about the bytes
    that reached you (§3 item 37).

G2  THE PLAN, at C1. `.agent/plan.md` is byte-identical to the PLAN17 slice; report its sha256,
    byte count and line count, and that it carries exactly one `## Goal` and one `## Next Steps`.
    Reference: 2142 bytes, 39 lines, both headings once, against the AGENTS.md cap of 50 lines.

G3  THE RECORD APPEND, at C2. Report from the file itself: byte count before and after; that the
    post-image equals the pre-image concatenated with the slice EXACTLY; N, the number of
    blank-line paragraphs in the slice, COUNTED by your script and not taken from this block; that
    the last N blank-line units of the whole file equal the slice's N paragraphs IN ORDER; and that
    a control flipping one byte inside the FIRST appended paragraph, at byte offset 616219, is
    REJECTED by both the byte reader and the ordered-unit reader. Then report before and after:
    blank-line units; `^Gate: `; `^Gate: F274 R16 `; distinct `^- R-\d+ — `; distinct
    `^Done: R-\d+ — `; and the open set as the first minus the second. Reference: 616218 to 622238
    bytes, N is 1, units 241 to 242, `^Gate: ` 47 to 48, `^Gate: F274 R16 ` 0 to 1, registrations
    70 to 70, distinct resolutions 7 to 7, OPEN SET 63 TO 63 BY DISTINCT ID.

G4  THE REGISTRATION, at C3. Report all four readings:
    (a) THE PATH SET OF THAT ONE COMMIT, read as `git show --name-only --format= <C3>` and NEVER
        as a range beginning at this round's base. A base-anchored range would also contain C0a,
        C0b, C1 and C2, so it answers a different question; ordering it here is exactly the defect
        the R-0819 recurrence booked in round 16 describes, and this gate is written not to repeat
        it. Report the list it returns. Reference: `README.md`, `docs/roadmap/STATUS.md`, the six
        `Depends on` feature files named in the Change set, `docs/roadmap/features/T2_F275.md` and
        `tests/docs/test_docs_consistency.py`.
    (b) PER PAIR AND PER FILE, the FROM and TO counts after the edit: FROM 0 and TO 1 for S2, S3
        and S4; FROM 1 and TO 1 for the append-shaped S1 and for S5 in each of its six files.
    (c) The new file's digest, as G1's second half orders it.
    (d) `TOTAL_FEATURES` reads 275, and the count of `^- \[[ ~x]\] F\d{3} — ` lines in
        `docs/roadmap/STATUS.md` is 275, and the count of files matching `T*_F*.md` under
        `docs/roadmap/features/` is 275 — the three numbers `tests/docs/` pins to each other.

G5  THE DOCS GATES, in the PRIMARY checkout, each in its own invocation, at C3. Report the exit
    code and the counts of each:
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
      python3 -m ruff check tests/docs/test_docs_consistency.py
    Reference: 303 passed; 30 passed; `All checks passed!`. Every one exits 0.

G6  THE BUILT STATE APPEND, at C4, against `docs/roadmap/features/T2_F274.md`. The same shape as
    G3: byte count before and after, exact concatenation, N counted by your script, the last N
    units equal to the slice's paragraphs in order, and the control at byte offset 9345 — inside
    the FIRST appended paragraph — rejected by both readers. Reference: 9344 to 12016 bytes, N is
    4. Also report that the file contains exactly one line beginning `## Built State`.

G7  THE SUITES AND THE SCOPE GUARD, at C4. In the PRIMARY checkout, serially:
      python3 -m pytest tests/cli/test_golden_path.py tests/orchestration/test_progress_ledger.py -q
    Reference: 73 passed, exit 0. Then the scope guard, for which the base-anchored range IS the
    correct reading because the claim is about the WHOLE round's change set:
    `git diff --name-only 7bd19462..<C4>` names NO path beginning `packages/`, `apps/` or
    `scripts/`. Report the full list it returns. Separately report that
    `tests/orchestration/cluster_deletion_map.txt` has the same sha256 at `7bd19462` and at C4,
    read with `git show <commit>:<path>` and never by writing into the checkout.

G8  THE TREE, THE PER-COMMIT NUMBERS AND THE RECORD-SLICE SCAN, at C4. `git status --porcelain` is
    EMPTY; `git ls-files .remedy-wt` is EMPTY; report `git worktree list` and confirm it is back to
    the 14 constraint 5 names. For C0a, C0b, C1, C2, C3 and C4 — and NOT for C5, whose own numbers
    cannot exist while its text is being written — report the insertion count from
    `git diff --numstat <parent>..<commit>` and confirm each is under the DECISION F104 D1 cap of
    500. The `## Commits` table of `.agent/handoff.md` carries these same values and its `+/-`
    cells are the numstat columns cell for cell, NOT a file's line counts before and after
    (§3 item 28); state that you compared the two. Finally, for the RECORD17 slice as committed in
    `.agent/authored/f274-r17.md`: delete every backtick-quoted span, then report the count of
    `\bHEAD\b` in what remains. Reference: ZERO, which is what finding R-0586's scan requires of
    text bound for an append-only record.


## Handback

Rewrite `.agent/handoff.md` per AGENTS.md and docs/agents/handback_template.md. It has no length
cap (amend0827 rule 3); it is valid when its mandated sections are present. It must carry:

- the state block, naming the feature, the round, THE SESSION NUMBER — session 7 of feature F274 —
  the branch, and the commit SHAs;
- the Fortschritt line, verbatim from the FORTSCHRITT slice above;
- the changed-files table and the `## Commits` table whose `+/-` cells G8 pins;
- ONE LINE PER GATE, G1 through G8, each carrying that gate's REAL measured result;
- the open-findings count, 63 by distinct id, with the arithmetic that produced it;
- every deviation, declared with its reason;
- the item-status table AGENTS.md requires, with every ordered item of this block appearing exactly
  once as done, skipped or deviated;
- the next expected action: the integration-gate round, per docs/agents/integration_gate.md, whose
  PASS closure precondition 2 re-confirms.

Then push the branch. Do not create a pull request; the closure sequence creates it in its own
round.
