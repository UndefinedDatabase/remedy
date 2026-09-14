── STEP T003 — F275 — ROUND 82 ──
Goal: Fix the flip's input set on disk and make it reproducible — the corrected set minus
the two sites DECISION F275 D55 names, re-keyed onto the tree the flip will run on, and
re-checked by the shipped owner check — and measure what the re-key's refusal does NOT
catch.

Base commit: `d7cf5d58`. Every gate below runs at a commit this block names.

THE FRAME RULE, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3, stated as the
property that was MEASURED over the final bytes: NO LINE of this block is a run of a single
repeated character, and every box-drawing rule inside the STEP and SLICE header lines is
exactly two characters long. Nothing appliable travels in the frame; the appliable bytes
are the slices below, each proved against its own target.

## Bundle — the ordered commit sequence

C0a  `.agent/authored/f275-r82.md`            the block, saved verbatim
C0b  `.agent/last_block.md`                   mirrored FROM THE COMMITTED C0a BLOB
C1   `.agent/plan.md`                         slice PLAN82, a full replacement
C2   `.agent/live_review.md`                  slice RECORD82 appended
C3   `.agent/prose_slips.md`                  slice SLIPS82 appended
C4   `.agent/authored/f275-r82-input.py.md`   the generator, written to the SPEC below
C5   `.agent/f275_t003_flip_input_r82.md`     the artefact, produced BY the C4 blob
C6   `.agent/decisions.md`                    slice DEC82 appended
C7   `.agent/handoff.md`                      the handback

C1 is the FIRST SUBSTANTIVE COMMIT because this round touches the finding ledger, per item
23 of §3. Only C0a and C0b may precede it.

## Change — exactly these paths and no others

The paths listed in the Bundle are the whole change set. NOTHING under `packages/`, `apps/`,
`tests/`, `docs/` or `scripts/` is touched by this round. No suite beyond the canary is
run. The flip itself is NOT performed here.

## Why the generator is SPECIFIED and not shipped as a slice

Under `docs/agents/self_drive_protocol.md` a block travels inside the worker's prompt and
the worker retypes it, so an authored source slice is the one link no gate in this
repository can prove — item 37 again. A generator is different from prose: its correctness
is decidable by what it COMPUTES. So this block describes what the generator must measure
and pins the reviewer's own independently measured figures beside it, and the gate is that
the worker's run reproduces them. Two implementations agreeing on a set-theoretic reading
is a stronger proof than a byte copy of one of them, and the committed generator still
makes the artefact reproducible for the flip round.

## The trees this round needs

Build all four under `.remedy-wt/`, never as a registered `git worktree`, and leave the
primary checkout untouched:

 BASE   `git archive ef75e213` extracted, then `git init -q` and `git add -A -f .` inside
        it. The index is required: the owner stage enumerates with `git ls-files`.
 TIP    the same recipe at `d7cf5d58`, this round's base.
 SHIFT  a copy of TIP with THREE BLANK LINES inserted after line 1 of
        `packages/orchestration/brain_detail.py`, so every ruled site in that file moves by
        three. Line 1 of that file is the opening `"""` of its module docstring, so the
        insertion lands inside the docstring and the file still parses.
 DELETE a copy of TIP with the single line `    job_id_str = str(job.id)` removed from
        `packages/orchestration/brain_detail.py`. THE REVERT TARGET IS NAMED BY PATH AND IS
        UNIQUE INSIDE IT, per item 25 of §3: those bytes occur EXACTLY ONCE in that file,
        measured at `d7cf5d58`. They also occur once in each of seven other modules under
        `packages/orchestration/`, which is why the path is named and the count is taken in
        the named file. SHIFT and DELETE each need their own index too.

Copy TIP with `shutil.copytree(..., symlinks=True)`. The argument is named rather than
assumed, per item 18 of §3: `copytree` defaults to `symlinks=False` and dereferences.

## The committed instruments, extracted not retyped

Both already exist on this branch and neither is edited. Extract each one's ONLY
```python fence — the bytes between the first fence opener and its closing fence — into
`.remedy-wt/`, and check the digest before use:

 `.agent/authored/f275-r59-rekey.py.md`        ->   5186 bytes
   sha256 `f56394e9ac2582d5655a64a135fbf95b2930c24d14e791a23a2eb2630742a721`
 `.agent/authored/f275-r73-owner-stage.py.md`  ->  24253 bytes
   sha256 `7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8`

The second digest is the one `.agent/f275_t003_owner_fallback_r81.md` pins for the same
file, so the extraction rule is the one round 81 already used.

## The pinned data inputs

Neither is regenerated and neither is committed — they are round 77's, and this round
consumes them exactly as rounds 79, 80 and 81 did:

 `.remedy-wt/r77_corrected.json`         120753 bytes
   sha256 `765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512`
 `.remedy-wt/r77_corrected_owners.json`  121095 bytes
   sha256 `670c6e952667b7c52b6c5a9ffd832dcc9f096aedfba114b83bc28ca061591b44`

If either digest fails to match, STOP and report; do not regenerate.

## SPEC — what `.agent/authored/f275-r82-input.py.md` must do

A `.md` carrying one ```python fence, because a `.py` anywhere `ruff check .` scans is
counted by `tests/orchestration/test_ci_budgets.py`. It takes BASE, TIP, SHIFT, DELETE, the
two pinned JSON paths, the two extracted instrument paths and a scratch directory AS
ARGUMENTS — no path and no commit is embedded in it. It prints, in this order, and its
stdout IS the artefact's body:

 S0  Each pinned input's byte count and sha256.
 S1  THE SUBTRACTION. The corrected set's site count and its distinct-tuple count; the
     owners map's key count; the ruled sites the owners map does NOT name, listed; for each
     of the two sites DECISION F275 D55 drops, its number of occurrences in the set and its
     owner in the owners map; the site and owner-key counts after the subtraction; a
     CROSS-CHECK that exactly two sites and exactly two owner keys went and that no
     dropped site survives; and the sha256 of the surviving set in a canonical form the
     generator states (sorted, `json.dumps` with `separators=(",", ":")`), with that
     payload's byte length beside it.
 S2  THE RE-KEY AND ITS TWO CONTROLS. The re-key stage run BASE to TIP, its whole stdout
     and its REAL exit code, and a CROSS-CHECK that its output is equal to the subtracted
     set both as a set and in order. Then the same stage run BASE to SHIFT, and BASE to
     DELETE, each with its whole stdout and REAL exit code. For DELETE, compare the set it
     emits against the TIP set and PARTITION the ruled sites of the mutated file into those
     whose STATEMENT TEXT is unchanged and those re-bound to a different statement,
     printing for each re-bound one its old and new coordinates, the old and new source
     lines, and the owner the owners map carries across.
 S3  THE SHIPPED OWNER CHECK, run over the set at TIP and again over the set at DELETE,
     each with its whole stdout and REAL exit code.
 S4  THE SET BY FILE. The distinct-file count, the site total, the counts by attribute, and
     then one line per file reading the count and the path, SORTED BY PATH.

A LISTING OVER A SET SORTS BEFORE IT IS EMITTED, and the generator is run three times with
its output compared byte for byte across the three before C5 is made. Report the number of
distinct digests; it must be 1.

THE GENERATOR PRINTS NO WALL-CLOCK VALUE of any kind — no duration, no timestamp — because
the artefact is compared byte for byte against a later re-run.

## The figures the reviewer measured, which the run must reproduce

Measured by the reviewer at `d7cf5d58` over the same four trees and the same two
instruments, and stated here so a disagreement SHOWS rather than being reconciled away:

 the corrected set                                         2185 sites, 2185 distinct
 its owners map                                            2184 keys
 ruled sites the owners map does not name                  1
   and it is `tests/orchestration/test_repair_loop_v1.py|56|28|id`
 `tests/cli/test_repair_runtime.py` 68:32 `id`             1 occurrence, owner `Job`
 `packages/orchestration/brain_detail.py` 345:54 `id`      1 occurrence, owner `Task`
 after the subtraction                                     2183 sites, 2182 owner keys
 canonical sha256 of the surviving set
   `b347365ec9f7f17462c69a5c11c89d01fd3418fda350661fc2fa6e3545edbda4` over 111904 bytes
 re-key BASE to TIP        2183 recovered, line-key control 2183, unresolved 0, exit 0
   and its output equal to the subtracted set as a set AND in order
 re-key BASE to SHIFT      2183 recovered, line-key control 2174, unresolved 0, exit 0
 re-key BASE to DELETE     2183 recovered, line-key control 2174, unresolved 0, exit 0
 ruled sites in the mutated file                           9
 of them merely re-located                                 8
 of them RE-BOUND to a different statement                 1
   from 142:21 to 144:16, `    job_id_str = str(job.id)` to
   `    node_map = {n.id: n for n in graph.nodes}`, with the owner `Job` carried across
 owner check at TIP        2183 sites, 71 record classes, 1908 confirmed,
                           106 + 103 + 66 refused, CONTRADICTED 0, exit 0
 owner check at DELETE     1907 confirmed, 107 + 103 + 66 refused, CONTRADICTED 0, exit 0
 the set by file           191 files, 2183 sites, `id` 2100, `name` 44, `description` 39

## SPEC — what `.agent/f275_t003_flip_input_r82.md` must say

The generator's stdout, under a title and a short opening the worker writes, which states
that this round performs no flip, moves no production line and runs no suite beyond the
canary. Every indented line of the artefact is a line of that stdout, VERBATIM. The
artefact additionally states, in prose the worker writes from the run in front of it:

 1. THAT THE SUBTRACTION TOOK ONLY REFUSED SITES. The owner check's DECIDED count is
    unchanged at 1908 across the two sets while its REFUSED count falls by exactly two, so
    the two sites DECISION F275 D55 removed were both in the refused blind spot and no
    decided site left the input. Give that as the reading of the two runs, not as a claim.
 2. THAT THE RE-KEY ONTO THIS TIP IS AN IDENTITY, AND WHY THAT IS NOT A PASSING GATE ON ITS
    OWN. No path under `packages/`, `apps/` or `tests/` differs between `ef75e213` and
    `d7cf5d58`, so the line-key control recovers as much as the scope key and the stage's
    discriminating power is untested by this tree pair. The SHIFT control is what tests it:
    there the scope key holds all 2183 while the line key loses exactly the sites of the
    shifted file.
 3. THAT THE DELETE CONTROL IS THE ONE THAT FOUND SOMETHING. The stage did NOT refuse. Its
    key is an occurrence index within an enclosing scope, so removing a ruled statement
    makes the NEXT attribute of that name in that scope answer to the key, and the owners
    map carries the old verdict onto it. State the receiver by reading it: `graph.nodes` is
    annotated `tuple[BrainNode, ...]` at `packages/orchestration/project_brain.py`, so the
    re-bound site's receiver is a `BrainNode` while the owner carried across is `Job`.
 4. THAT THIS IS `R-0880`'s DEFECT REACHED BY A SECOND ROUTE AND NOT A NEW ONE. `R-0880`
    names `BrainNode` among the receivers the set already mis-owns, and its second
    obligation — the transform refuses a site whose owner verdict cannot be CONFIRMED —
    would stop this run too, because the owner check moves the re-bound site out of
    CONFIRMED and into the refused blind spot. Item 30 of §3 was applied before any id was
    considered and the search returned `R-0880` itself, so NO NEW ID IS MINTED.
 5. WHAT IS NOT CLAIMED. The two pinned JSON inputs are round 77's and live in gitignored
    scratch; this round makes the SUBTRACTION and the RE-KEY reproducible and does not make
    the corrected set itself reproducible from committed bytes, which needs the round 53
    probe run and is not this round's work. And the DELETE control is a synthetic mutation:
    no commit of this branch has yet removed a ruled statement.

## Constraints

1. NO SLICE IS EDITED. Apply PLAN82, RECORD82, SLIPS82 and DEC82 byte for byte. A
   discrepancy inside a slice is DECLARED in the handback, never repaired.
2. The generator and the artefact are the worker's OWN text, written from the SPECs above
   and from the run in front of it. They are the only two files of this round that are not
   slices.
3. READ `.agent/STOP` FROM DISK before C0a and again before C7, and record both readings
   with their real exit codes. If it appears, finish the commit in hand, write the handoff
   and end.
4. Every commit stages EXACTLY ONE path and every insertion count stays under 500.
5. No `.py` file is created anywhere inside the tracked tree. Every script this round
   writes lives under `.remedy-wt/` and stays uncommitted.
6. Nothing under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` is edited, and the
   artefacts of rounds 79, 80 and 81 are not edited, deleted or staged.
7. No landed DECISION is rewritten. DEC82 is an APPEND and C6's deletion column is ZERO.
8. No `gh` and no `remedy` command. No pull request created, edited or merged; no branch
   created or deleted; no merge; NEVER a force-push; no history rewrite.
9. `git worktree add` is not used. The four trees are plain directories under
   `.remedy-wt/`, and `git worktree list` must still show the primary checkout alone.
10. THE BLOCK'S OWN SIZE, measured on its final bytes: 392 lines TOTAL and 317 lines of
    PROSE, against the caps of 490 and 400.
11. EVERY GATE RUNS AT C6, after every substantive commit and before the handback, and no
    gate is ordered after C7. This ends the split the last three rounds each had to make.
    C7's OWN insertion count and its OWN path go nowhere in this round: under item 31 of §3
    a handback cannot carry a reading taken after the commit that writes it, and under
    `docs/agents/self_drive_protocol.md` a value routed to a round report is written to a
    channel that ends with the session. The REVIEWER measures C7's numbers at the next gate
    and books them in the round's ledger entry. G7 and G8 are therefore both scoped to
    `d7cf5d58`..C6, and G7 compares against the Bundle's paths MINUS `.agent/handoff.md`.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r82.md` at C0a compared with `cmp`
against the block as received; `.agent/last_block.md` at C0b byte-identical to the COMMITTED
C0a blob. Extract each slice by its BEGIN and END markers, report the number of slices the
extraction FOUND, and check each one's bytes against the sha256 written on its own BEGIN
marker. Re-measure the block's TOTAL and PROSE line counts and compare against constraint
10. PROSE is TOTAL minus the lines of the slices.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN82 re-extracted from the
COMMITTED C0a blob. At most 50 lines. Exactly one `## Goal` and exactly one `## Next Steps`.

G3 THE RECORD, FULL FORENSICS, for `.agent/live_review.md` at C2 and `.agent/decisions.md`
at C6. READER A: the post-commit file equals the pre-commit blob followed by exactly the
slice, with the byte arithmetic printed — the pre-commit lengths are 1097205 and 1243551.
READER B, INDEPENDENT AND STRUCTURAL: the file's LAST N blank-line-separated units equal the
slice's N paragraphs IN ORDER, where N is COUNTED BY THE SCRIPT from the slice and is no
number this block states. For each append run a NEGATIVE CONTROL that flips one ASCII letter
inside the FIRST appended paragraph and require BOTH readers to REJECT it. Both deletion
columns must read 0. Separately: `.agent/prose_slips.md` at C3 equals its pre-commit blob of
288515 bytes followed by exactly SLIPS82 and nothing else, and C3's deletion column is 0.
Finally, DERIVE the ledger's entry-header pattern from the headers already in the file
rather than asserting one, report how many of them it matches, and report that RECORD82's
header matches it and duplicates none of them byte for byte.

G4 THE GENERATOR AND THE ARTEFACT. The C4 blob holds exactly one ```python fence. The C5
blob is byte-identical to the file a fresh run of the COMMITTED C4 blob produces, and the
three-run digest count is 1. `git show d7cf5d58:.agent/f275_t003_flip_input_r82.md` and
`git show d7cf5d58:.agent/authored/f275-r82-input.py.md` both fail, which is how a NEW path
is proved new. Count the artefact's indented non-blank lines under the rule "its first
character is a space and it has a non-space character", match every one VERBATIM and at
STRICTLY INCREASING indices against the generator's saved stdout, and report the matched
count, the unmatchable count and the first and last matching indices. Report the artefact's
count of lines carrying a wall-clock duration and of three-backtick lines; both must be 0.
Both must be under 500 lines.

G5 THE MEASUREMENTS. Compare every figure of the run against the reviewer's list above,
one printed comparison per figure with its own MATCH or DIFFER, and report how many
comparisons were made and how many differ. A DIFFER is not repaired: it is reported.
Report also, from the run rather than from this block: the two owner-check runs' DECIDED
counts and REFUSED counts side by side, and the partition of the mutated file's ruled sites
into re-located and re-bound with its sum against the file's site count.

G6 TREE, COLOURS, PATH SET. `git status --porcelain` prints the EMPTY STRING at C6, shown
as `''`. `git worktree list` has exactly one row and the four scratch trees exist on disk
and none is registered — report both facts together. THE CANARY
`python3 -B -m pytest tests/cli/test_golden_path.py -q`, whose real exit code must be 0 at
42 passed, which is what the reviewer measured at `d7cf5d58`. `ruff check .` exits 1 BY ITS
OWN DESIGN at the frozen ceiling: count its location rows AND cross-check that count against
its own `Found <n> errors.` line, and the two must agree at 26. A filesystem
`rglob("*.py")` anywhere under `.agent/` must find 0 — that pattern does NOT match the
`.py.md` carrier C4 writes, which is the point of the carrier — and report how many files
the same sweep reached.

G7 THE OPEN SET AND THE PATH SET. Derive the open set mechanically at `d7cf5d58` and at C6 —
every `^- R-\d+ — ` registration minus every `^Done: R-\d+ — ` line, BY DISTINCT ID — and
report both counts, the membership difference each way, and whether `R-0880` is open and
`R-0879` resolved at each. The reviewer measured 87 open at the base with `R-0881` the
highest registered id. Report the ids registered, resolved and de-registered by this round;
all three sets must be EMPTY. Then the changed-path set of `d7cf5d58`..C6 against the
Bundle's paths MINUS `.agent/handoff.md`, reporting MISSING and EXTRA by name, and the count
of changed paths under `packages/`, `apps/`, `tests/` or `docs/`, which must be 0.

G8 THE INSERTION CAP. Per-commit insertion and deletion counts over `d7cf5d58`..C6, one row
per commit, each commit's staged path count, and the number of commits whose insertions
reach 500.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md` — the Session line
reading `SESSION 29 of feature F275 · round 82 · rounds so far 82`, the Commits table with
its `+/-` cells READ FROM `git show --numstat` and compared cell by cell against G8's own
numbers with the comparison printed — and C7's own row carries no numbers, per constraint
11 and item 31 of §3, saying so in the cell — the Verification table at one line per gate with its
REAL exit code, the External-actions table, the Authored-text proofs table, the Item-status
table, the Deviations section, and a `## Next` stating `Operator questions open: 0`. NO
SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED: amendment amend0911-f275-to-scope lifts
this feature's limit without a replacement number.

── SLICE PLAN82 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN82 sha256=e8657d4da419d2abcaee593de0ed263984a52f019a7e17d71698e7bcc4ea377a
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

ROUND 82 FIXES THE FLIP'S INPUT SET ON DISK AND MAKES IT REPRODUCIBLE. The corrected set
loses the two sites DECISION F275 D55 names, is re-keyed onto the tree the flip will run on
by the committed round 59 stage, and is re-checked by the committed round 73 owner check;
the generator that does all three is committed with the artefact it writes. Two controls sit
beside the re-key, and the second one found something: removing a ruled statement does not
make the stage refuse, it makes the next attribute of that name in that scope answer to the
key and carries the old owner verdict onto it. That is `R-0880`'s defect by a second route,
so no id is minted. The round 81 verdict and its prose slip are booked.

## Next Steps

1. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
2. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the
   input is re-derived by round 82's committed generator at the flip's own base, and any
   site fallen to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, which are
  gitignored. Rebuilding those needs the round 53 probe run, which no round has re-taken.
- THE RE-KEY CANNOT SEE A DELETED RULED SITE. Any round between here and the flip that
  removes a ruled read moves that site's verdict onto its neighbour with nothing said.
- The open set is 87 by distinct id at this round's base, with `R-0880` open. Four are High
  — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN82

── SLICE RECORD82 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD82 sha256=9613b788b92883a1af9494133246663fc4cf800f2e515d5d99628f4ec5f59687

Gate: F275 R81 — the F275 round 81 entry. VERDICT PASS. Written by the planner and reviewer of session 28 after reading the committed range `89d4772a`..`cba25b45` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 82, per operator amendment amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of §3. G1 was the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback, and the chain it walked is the reviewer's own scratch original, the committed `.agent/authored/` blob and the working copy — three artefacts that are all downstream of what the worker received, so it establishes self-consistency and not receipt. The block blob was byte-identical to the reviewer's original at 28740 bytes, `.agent/last_block.md` equalled the committed block blob, all four slices matched the sha256 on their own BEGIN markers, and the block re-measured at 343 lines TOTAL and 267 PROSE as its constraint 10 states.

EVERY GATE HOLDS AND THE REVIEWER RE-RAN ALL EIGHT. `.agent/plan.md` was byte-identical to its slice at 46 lines. The two record appends were exact under reader A with reader B holding over the whole appended region at N counted from each slice as 4 and 9, every negative control on the FIRST appended paragraph was rejected by both readers, and every deletion column was ZERO. The round 79 and round 80 artefacts were byte-identical at the base and at the tip, so no landed reading was rewritten. The artefact's 155 indented lines all appeared verbatim in the instrument's output at strictly increasing indices with nothing unmatchable, and it carries no wall-clock duration. The canary read 42, `ruff check .` 26 rows against the frozen ceiling of 26, zero `.py` files under `.agent/`, one worktree, the changed-path set exactly the Change section with MISSING and EXTRA empty and zero paths under `packages/`, `apps/`, `tests/` or `docs/`, and the open set 87 by distinct id at both ends with identical membership and `R-0880` open at each.

THE ROUND'S SUBSTANCE, AND IT IS A DIAGNOSIS RATHER THAN A COUNT. Every ruled column the seventeen attributed frames blame is a column the SHIPPED owner check REFUSES rather than decides, and the reviewer re-derived all five verdicts independently: `job` and `t` CONFIRMED, `art`, `node` and `j` absent from the decided set. The transform renames them anyway on the fallback its P1 rule describes, so on a line carrying one owner verdict a refused column takes the verdict of the column beside it. The class that puts at risk re-derives exactly as the artefact reports it — 2185 ruled sites over 2080 distinct lines, 91 carrying more than one site, 58 of those agreeing on one verdict and 33 not, and 26 of the 58 spanning receivers with different names — and both lines behind sixteen of the seventeen frames are in the 26. DECISION F275 D55 takes two sites out of the flip's input BY NAME and leaves the third in with its stale test double routed to the flip's own commit, which is the right cut: refusal is not evidence of error, and dropping all 277 refusals would trade a measured defect for an unmeasured one. The limit of the reading is stated in the artefact and is worth repeating in the record: only what a test exercises produced a frame, so the fallback certainly reaches sites no reading in this chain can see, and 26 is an upper bound on the suspect set rather than a defect count. `R-0880` stays OPEN for exactly that reason.
END RECORD82

── SLICE SLIPS82 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS82 sha256=9c91a4ba4b505b129def68731af49c8aacdb4ebe5ae0f6c313c968ddb06f90a7

2026-09-12 · F275 R81 · Two rounds running, a freshly written gate script counted ruff rows with a pattern for an output format this ruff does not emit, read ZERO rows against a ceiling of 26, and reported a pass; both times the author caught it only because the block also ordered a cross-check against the tool's own `Found <n> errors.` tally. The recurrence is the finding: the second script was written after the first had failed the same way, by a different author, because nothing on disk records what this repository's ruff prints. THE RULE THAT FOLLOWS: where a gate parses a TOOL'S OUTPUT FORMAT, it never takes the count from the parse alone — it takes the tool's own stated total beside it and compares the two, because a parser that matches nothing is indistinguishable from a repository that is clean, and that is the failure direction nobody investigates.
END SLIPS82

── SLICE DEC82 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC82 sha256=8f14e60cd5627ce3ea2e10ee7c32dd8ad08e2c8ba7b83525db6a0d98c74c53fc

## DECISION F275 D56 (2026-09-12, F275 round 82) — the flip's input is the corrected set minus DECISION F275 D55's two sites, re-keyed onto the flip's own tree by a COMMITTED generator; and the re-key's refusal is measured blind to a deleted ruled site

CONTEXT. DECISION F275 D51 ruled the corrected set the flip's input at 2185 sites and DECISION F275 D55 named two of them to drop. Both rulings live in prose while the set itself lives in two gitignored JSON files round 77 wrote, and the flip is the one commit this feature cannot split. This round performs the subtraction, re-keys the result onto the tree the flip will run on, re-checks it with the shipped owner check of DECISION F275 D47, and lands the generator that does all three beside the artefact it writes.

THE MEASUREMENT. The corrected set holds 2185 sites on 2185 distinct tuples against an owners map of 2184 keys, so ONE ruled site has no owner at all — `tests/orchestration/test_repair_loop_v1.py` line 56 column 28 — which no previous round recorded. Each of DECISION F275 D55's two sites occurs exactly once, with the owners `Job` and `Task`, and the subtraction leaves 2183 sites and 2182 owner keys. Re-keyed from `ef75e213` onto `d7cf5d58` by the committed round 59 stage, all 2183 resolve with none lost and the result is equal to its input both as a set and in order. The committed round 73 owner check reads 1908 CONFIRMED, 275 REFUSED and ZERO CONTRADICTED over it.

CHOSEN, FIRST: THE SUBTRACTION IS RULED TO HAVE TAKEN ONLY REFUSED SITES, AND THAT IS MEASURED RATHER THAN ASSUMED. The owner check's DECIDED count is 1908 both before and after, while its REFUSED count falls from 277 to 275, so neither removed site was one the check decided and the corrected set's zero-contradiction property is untouched. ALTERNATIVE: take the count on trust from DECISION F275 D55's reading of the same two columns, rejected because that reading was taken over three sites by hand and this one is taken over the whole set by the shipped instrument.

CHOSEN, SECOND: THE GENERATOR IS COMMITTED AND TAKES EVERY TREE AND FILE AS AN ARGUMENT. `.agent/authored/f275-r82-input.py.md` embeds no commit and no path, so the flip round re-derives the input at ITS OWN base rather than inheriting a set measured here. ALTERNATIVE: commit the 2183-site list itself, rejected because it is a 2183-line insertion against a 500-line cap whose one declared-oversize allowance this feature must keep for the flip commit; the artefact carries the per-file rendering and the canonical digest instead.

CHOSEN, THIRD: THE RE-KEY'S IDENTITY ON THIS TREE PAIR IS NOT ACCEPTED AS A PASSING GATE. No path under `packages/`, `apps/` or `tests/` differs between the two commits, so the line-key control recovers as much as the scope key and nothing about the stage is under test. A shift control supplies the discriminator: with three blank lines inserted in one module the scope key holds all 2183 while the line key falls to 2174, which is exactly that module's nine sites.

CHOSEN, FOURTH, AND IT IS WHAT THE ROUND FOUND: THE STAGE IS BLIND TO A DELETED RULED SITE, AND THE BLINDNESS IS RECORDED RATHER THAN REPAIRED HERE. Removing one ruled statement does not raise the stage's refusal. Its key is an occurrence index inside an enclosing scope, so the next attribute of that name in that scope answers to the key: the site at `packages/orchestration/brain_detail.py` 142:21, `job_id_str = str(job.id)`, re-binds to 144:16, `node_map = {n.id: n for n in graph.nodes}`, and the owners map carries `Job` onto a receiver the tree annotates `BrainNode`. Eight of that file's nine sites merely re-locate; this one does not.

CHOSEN, FIFTH: NO NEW FINDING ID IS MINTED FOR IT. Item 30 of `docs/agents/planner_reviewer_prompt.md` §3 requires the open set to be searched for the DEFECT before an id is spent, and the search returns `R-0880`, which already names `BrainNode` among the receivers this set mis-owns. Its second obligation — the transform refuses a site whose owner verdict cannot be CONFIRMED — would stop this run as well, because the owner check moves the re-bound site out of CONFIRMED and into the refused blind spot, which is measured here and not reasoned to. A fix for `R-0880` fixes this instance, so by the test that minted `R-0880` itself the two are not independent. ALTERNATIVE: mint an id against the round 59 stage, rejected under that test and under item 30.

CONSEQUENCE. The flip's input set is fixed at 2183 sites with a canonical digest and a committed producer, and the flip round re-derives it at its own base instead of inheriting it. `R-0880` stays OPEN and gains a second reachability path in evidence rather than a second id. The round 69 resolution of `R-0879` is NOT reopened and NOT rewritten: its claim about the stage is true of a vanished scope, which is what its own red control exercised, and this round adds the case that control did not reach. No production line moved, no suite beyond the canary was run, and no transform was executed.

HOW TO REVERSE. Delete this paragraph block, the artefact and the generator. The flip's input is then DECISION F275 D55's ruling in prose over round 77's two scratch JSON files, with no committed producer, no canonical digest, and the re-key's blindness to a deleted ruled site unmeasured.
END DEC82
