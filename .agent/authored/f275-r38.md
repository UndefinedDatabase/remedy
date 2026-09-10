── STEP T003 (3 of n) — F275 ─────────────────────────────────
Goal:        Repair the last surviving instance of R-0870's class, which this
             reviewer's own round 37 pair missed four lines below its own span,
             and enumerate the CLASSIC STORE SEAM — the half of the flip
             DECISION F275 D17 gave no site list.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 37
             verdict, new evidence on R-0870 and three prose slips · C3 the
             migration-path repair · C4 the seam enumeration · C5 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r38.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`,
             `docs/system/development-artifact-boundary-v0.md`,
             `.agent/f275_t003_flip_seam.md` (NEW),
             plus `.agent/handoff.md` at C5.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end of frame; the single pure rule line below is exactly 62 `─` characters
──────────────────────────────────────────────────────────────

## Base

This round's base is `4921e117`. THE REPAIR WAS APPLIED AND GATED and the SEAM
ENUMERATOR WAS WRITTEN AND RUN by the reviewer in a disposable worktree at that
base before this block was authored. Every numeral below is that run's.

## What this round is

TWO THINGS, AND THEY ARE UNRELATED TO EACH OTHER BY SUBJECT BUT BOTH BELONG TO
T003. The first closes R-0870's class. The second opens the measurement the flip
needs before it can be committed.

THE REPAIR, AND WHOSE MISTAKE IT IS. Round 37's PAIR D repaired the paragraph of
`docs/system/development-artifact-boundary-v0.md` that said a deleted handler
"reads" a file, and left the "Planned migration path" list four lines below it
naming the deleted `approval` GROUP and the deleted `progress` COMMAND in the
present tense. The block that ordered that pair quoted R-0870's widened fix clause
— "a pair that narrows or removes a definition, an assertion or a sentence is
authored against the WHOLE enclosing unit" — and then broke it. THE WORKER FOUND
IT AND DECLARED IT; it is repaired here rather than left, because the class this
finding is about is a claim that survives the thing it describes.

WHY THE MODULE-STEM SWEEP COULD NOT SEE IT, which is the part worth keeping. That
sweep looks for deleted MODULE STEMS. These two sentences name a COMMAND GROUP and
a COMMAND, and no module stem appears in either. The reviewer therefore ran a
SECOND sweep at the base, over the fifteen groups DECISION F260 D3 records as
deleted whole, in the two shapes a page uses them — backticked, and as
`remedy <group>` — across the 569 tracked files under `docs/`, `packages/` and
`apps/` outside `docs/roadmap/` and `docs/archive/`. It returned 28 hits, of which
these two are the only ones that treat a dead group as live: the rest are the
English words `provider` and `builder` used as a field name and a role name, the
cockpit's `overnight` SECTION key, whose reader `build_overnight_readiness`
survives in `packages/orchestration/mission_readiness.py` by DECISION F275 D1, and
pages that name a group and say in the same sentence that it is gone.

THE SEAM. DECISION F275 D17 measured the flip over `Job.id` and `Job.name` and
stated in its own terms that the union is "a FLOOR on the flip's size and not a
ceiling", giving the remainder no numeral because none was measured. Round 36
enumerated that floor: 1753 sites over 184 files. The reviewer has now measured
part of the remainder, and it is not small — the four classic-store functions are
called at 821 sites in 152 files, and 44 of those files hold NO enumerated `.id`
or `.name` site at all, so the round 36 list cannot see them. C4 enumerates them.

WHAT THIS ROUND STILL DOES NOT DO. It does not flip anything, it does not rule the
route, and it does not resolve R-0870 — the reviewer authors that resolution at
the next gate, once it has re-run both sweeps itself against the committed tree.
The third part of the remainder, the sites that treat a job id as a UUID rather
than as a 16-hex string, is NOT enumerated here: the reviewer measured it as a
BOUND at the base and could not make it a precise site set, and a bound is
recorded as a bound. That is the next round's work, with the DECISION that rules
the route on the complete figure.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Extract each by its delimiter lines from the
   committed `.agent/authored/f275-r38.md` and apply with `shutil.copyfile`
   semantics — never by retyping, never reflowed. If anything does not fit,
   DECLARE it in the handback and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, exactly — seven commits, no
   extra, none dropped, no reordering. C1 is the first substantive commit and
   makes `.agent/plan.md` current before any other change, per §3 item 23.
3. THE APPEND BASELINES, read by the reviewer at the base: `.agent/live_review.md`
   is 831847 bytes and `.agent/prose_slips.md` is 228778 bytes, each ending in a
   newline. An append is pre-blob, then ONE newline, then the slice as extracted.
   C2 makes THREE appends and C3 makes one, so each re-baselines on the state the
   append before it left.
4. C3 IS THE ONLY COMMIT THAT TOUCHES ANYTHING OUTSIDE `.agent/`. No path under
   `packages/`, `apps/`, `tests/` or `scripts/` moves in this round at all.
5. THE SEAM ENUMERATION IS GENERATED, NEVER RETYPED. SEAMTOOL is written to the
   gitignored `.remedy-wt/` scratch — NEVER to the repository root, where
   `ruff check .` would collect it — run from the repository root, and its output
   is what C4 commits. Its source is EMBEDDED in the committed file, which is the
   convention `.agent/f275_t002_flip_inventory.md` set, so the measurement is
   reproducible from the artefact alone.
6. IDS REGISTERED THIS ROUND: none. IDS RESOLVED THIS ROUND: none. The open set
   is 87 by distinct id at the base and must read 87 at C4.
7. THE ROUND GATE IS TIER 1 plus the docs tier: the scoped command in G6 and the
   canary. The full suite is NOT run this round.
8. PAIR F IS A REWRITE AND NOT AN APPEND, and the containment test was RUN before
   emission rather than judged by eye: `TO contains FROM: false`. Its FROM spans
   the WHOLE numbered list rather than the two items it changes, because removing
   an item renumbers the ones below it — §3 item 17. Order no "FROM 0x"
   whole-file count; the obligation is FROM exactly 1x before the edit and 0x
   after, which G5 states.

## SLICE PLAN38 → whole-file replacement of `.agent/plan.md`

<<<PLAN38
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

ROUND 38 does two things. It repairs the last surviving instance of R-0870's class, a
"Planned migration path" list that still names the deleted `approval` group and the deleted
`progress` command in the present tense, which the round 37 pair missed four lines below its
own span. And it enumerates the CLASSIC STORE SEAM — 821 calls of `save_job`, `load_job`,
`load_job_safe` and `resolve_job_id` across 152 files, 44 of them holding no enumerated
`.id` or `.name` site — which is the half of the flip DECISION F275 D17 gave no site list.
R-0870 STAYS OPEN until the reviewer's `Done:` text lands.

## Next Steps

1. Measure the last part of the flip remainder — the sites that treat a job id as a UUID
   rather than as a 16-hex string — and then a dated DECISION ruling the route on the
   complete figure, as T002's DECISION F275 D17 ruled it on the partial one.
2. The flip itself, applied from the round 36 enumeration and the round 38 seam list, as
   the one declared-oversize commit AGENTS.md permits per feature, with the inseparability
   reason stated in the handback BEFORE review.
3. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 2 is the largest single commit this repository will take and it spends the one
  declared-oversize allowance AGENTS.md rations per feature. Steps 1 and the round 38
  enumeration exist because that allowance can be spent once and the size it must cover
  was measured only in part.
- The open set is 87 by distinct id at this round's base `4921e117`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
PLAN38

## SLICE RECORD38 → append to `.agent/live_review.md`, in C2

<<<RECORD38
Gate: F275 R37 — the F275 round 37 entry. VERDICT PASS, written by the planner and reviewer of session 17 after reading the committed range `f4fc3459`..`4921e117` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits C0a `6d352722`, C0b `12bdd968`, C1 `9d42ef0d`, C2 `98634e58`, C3 `751aaf21`, C4 `ae516313` and C5 `4921e117`, per-commit insertions 393, 306, 20, 6, 6 and 66 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's delegation source was written AND HASHED BEFORE delegation at `4ddc7169076679ae4315bf5d0f899bb74fc455835ff5a76ef650f1db86bce666`, and both committed copies are 30519 bytes at that digest as ONE shared git blob; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN37 at 2669 bytes, 47 lines against the cap of 50, both mandated headings exactly once. G3 OVER ALL FOUR APPENDS, each re-derived by the reviewer: `.agent/live_review.md` 825867 to 830928 for RECORD37 and 830928 to 831847 for LANDED37, `.agent/prose_slips.md` 227412 to 228778, and `.agent/decisions.md` 1039256 to 1044462; every post-blob equal to its pre-blob then ONE newline then the slice as extracted, every joining byte READ BACK at offset len(pre) reading a newline, N COUNTED FROM EACH SLICE as 1, 2, 1 and 7 with the last N blank-line units matching IN ORDER, and all four negative controls flipped INSIDE THE FIRST appended paragraph rejected by BOTH readers. `^Gate: F275 R36 ` exactly 1 and `^## DECISION F275 D20 ` exactly 1, with no id collision. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base, at C4 `ae516313` and at C5 `4921e117`, over 103 registrations against 16 resolutions; `R-0870` is in it, carries ZERO `Done:` lines and now carries THREE `Landed:` lines, one per repaired batch. G5: all three repair pairs reconstruct exactly — FROM 1x before and 0x after in each target, TO 1x after, and the committed post-blob equal to the pre-blob with the FROM span replaced and nothing else; `ruff check tests/conftest.py` printed `All checks passed!`; and every entry of `SUBPROCESS_FILES` now names a file that exists, 21 entries over 20 distinct names, the duplicate `test_test_runner.py` being pre-existing and deliberately untouched. G6: `tests/docs/` with `tests/cli/test_product_spine.py` reads `371 passed` at exit 0, re-run by the reviewer, and collection reads `18366 tests collected` — identical to the base, which is the direct evidence that removing a `SUBPROCESS_FILES` entry changed no test's collection. G8: the change set is an EXACT set match over ten paths with MISSING and EXTRA both empty, porcelain EMPTY, ONE worktree, `.agent/STOP` absent, canary `42 passed`. THE THREE DEVIATIONS THE WORKER DECLARED ARE ALL THE REVIEWER'S OWN AND ALL ARE SUSTAINED. FIRST, G4 of that block ordered the base reading at `965ea50d`, which is the PREVIOUS round's base, while the block's own Base section names `f4fc3459`; the worker read all three revisions rather than choosing one, and every one gives 87, so no numeral moved. SECOND, G7's exclusion clause dropped stems shorter than five characters and the two English-generic stems `provider` and `progress` by name, and NO STEM WAS DROPPED, because the real stems are `provider_trust` and `progress_cmd` — an inert clause that protected nothing and forbade nothing. THIRD, and this is the one that found a defect rather than a wording slip, G7's predicted hit list was incomplete by six files and eight hits; the worker opened and read every one, found all of them in the correct "names it AND says it is gone" pattern, repaired none, and reported the corpus reconciliation that explains the difference. AND THE ROUND FOUND A DEFECT IN THE BLOCK THAT ORDERED IT, which is recorded here because it is the reason the next round exists: PAIR D repaired the paragraph of `docs/system/development-artifact-boundary-v0.md` naming `progress_cmd.py` and left the "Planned migration path" list four lines below it naming the deleted `approval` GROUP and the deleted `progress` COMMAND in the present tense — outside the pair's span and outside the module-stem sweep's reach, in a block that quoted R-0870's whole-enclosing-unit clause while breaking it. NO FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.
RECORD38

## SLICE NOTE38 → append to `.agent/live_review.md`, in C2

<<<NOTE38
Note: F275 R38 — new evidence for the OPEN finding R-0870, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, because the defect is R-0870's own subject and the open set was searched for it before this paragraph was written. R-0870 records a claim falsified by a deletion in a place no gate can see. THIS IS THE NINTH INSTANCE AND IT IS THE FIRST THAT NAMES NO MODULE AT ALL, which is the widening. THE MEASUREMENT, taken by the reviewer at `4921e117`. `docs/system/development-artifact-boundary-v0.md` carries a "Planned migration path" list whose item 1 reads "Core operator commands (`worker`, `mission`, `approval`) already use structured state" and whose item 2 reads "The development command `progress` may continue reading `.agent/` files". Importing the shipped catalog at that commit gives 44 groups: `worker` and `mission` are among them, `approval` and `progress` are NOT — both are on DECISION F260 D3's list of groups deleted whole. So item 1 names a dead group beside two live ones and item 2 offers an operator a command that does not exist. WHY NO SWEEP THIS FEATURE HAS RUN COULD SEE IT: every one of them, including the round 37 resolution sweep, searches for deleted MODULE STEMS, and neither sentence contains one — they name a COMMAND GROUP and a COMMAND. The reviewer therefore built a second instrument at this base, over the fifteen groups D3 records as deleted whole, in the two shapes a page uses them — backticked, and as `remedy <group>` — across the 569 tracked files under `docs/`, `packages/` and `apps/` outside `docs/roadmap/` and `docs/archive/`; it returns 28 hits of which these two are the only ones treating a dead group as live. WHY THIS IS EVIDENCE RATHER THAN A SECOND ID: R-0870 is OPEN, its subject is exactly a surviving claim a deletion falsified, and a second id would be a second thing to resolve for one defect. WIDENED FIX CLAUSE, binding on every remaining round of this feature and replacing the reach of the `Note: F275 R24` wording rather than repeating it: a sweep that supports a claim about surviving prose runs over the deleted COMMAND SURFACE — group names and command ids — as well as over deleted module stems, because a page can advertise a dead capability without naming a single deleted symbol.
NOTE38

## SLICE SLIPS38 → append to `.agent/prose_slips.md`, in C2

<<<SLIPS38
2026-09-10 · F275 R37 · The round 37 block's PAIR D repaired the one paragraph of `docs/system/development-artifact-boundary-v0.md` that named a deleted handler and left the numbered list four lines below it naming the deleted `approval` group and the deleted `progress` command in the present tense. The same block quoted R-0870's widened fix clause — "authored against the WHOLE enclosing unit" — in its own prose. The enclosing unit of a claim about what a command does is the SECTION, not the paragraph, and a reviewer who reads a file by grepping for the string it is repairing sees exactly the span it already knew about. Read the whole section around every prose pair, and sweep the surviving capability rather than the surviving symbol.

2026-09-10 · F275 R37 · The round 37 block's G4 ordered the open set read at `965ea50d` while the block's own Base section names `f4fc3459` — the previous round's base, carried forward when the gate text was adapted. The worker read all three revisions rather than choosing one and every reading gave 87, so nothing moved. A SHA in a gate is re-resolved against the block's own Base line after the last edit, exactly as §3 item 9 requires of a citation, because a stale base is the one kind of wrong anchor that still returns a plausible number.

2026-09-10 · F275 R37 · The round 37 block's G7 excluded stems shorter than five characters and the two English-generic stems `provider` and `progress` by name, and the worker measured that NO STEM WAS DROPPED: the real stems are `provider_trust` and `progress_cmd`, so the clause forbade nothing and protected nothing. It was copied from DECISION F275 D16, where the exclusion operated on a different reduction of the same corpus. An exclusion clause is checked against the list it actually filters before it is written down, or it is a gate that reads as careful and measures nothing.
SLIPS38

## PAIR F → `docs/system/development-artifact-boundary-v0.md`

FROM is 326 bytes, sha256 `0b29b118df4dc3ad…`; TO is 433 bytes, sha256
`8171b7da8e43567c…`; TO's longest line is 84 characters. The FROM spans the whole
four-item list because removing an item renumbers the two below it.
`tests/cli/test_product_spine.py` reads this page and asserts exactly one thing
about it — that it contains the substring `NOT product runtime state` — which this
pair does not touch; that assertion was read at the base, not assumed.

<<<PAIRF_FROM
1. Core operator commands (`worker`, `mission`, `approval`) already use structured state
2. The development command `progress` may continue reading `.agent/` files
3. Future blocks may migrate remaining self-dogfood paths to structured event ledger
4. No urgent migration needed — boundary is enforced for new product paths
PAIRF_FROM

<<<PAIRF_TO
1. Core operator commands (`worker`, `mission`) already use structured state. The
   `approval` group this list named beside them, and the development command
   `progress` it gave the remaining `.agent/` reads to, were both deleted by F275
   with the prototype cluster
2. Future blocks may migrate remaining self-dogfood paths to structured event ledger
3. No urgent migration needed — boundary is enforced for new product paths
PAIRF_TO

## SLICE LANDED38 → append to `.agent/live_review.md`, in C3

<<<LANDED38
Landed: R-0870 — the ninth instance, the one the `Note: F275 R38` entry above measures, is repaired in C3 of F275 round 38, and the three `Landed:` lines above are left untouched because each names the batch it covers. `docs/system/development-artifact-boundary-v0.md` no longer offers an operator the deleted `progress` command or lists the deleted `approval` group among the operator commands that already use structured state; the list names both as deleted with the prototype cluster instead, which is the pattern this repository wants. NOT RESOLVED: the reviewer's `Done:` text is owed at the next gate, after it re-runs BOTH sweeps — the module-stem one and the command-surface one the note above adds — against the committed tree.
LANDED38

## SLICE SEAMTOOL → written to `.remedy-wt/r38_seam_enum.py`, run, and EMBEDDED in the file C4 commits

<<<SEAMTOOL
"""F275 T003 — enumerate the CLASSIC STORE SEAM by `ast`, at this round's base.

DECISION F275 D17 sized the flip over `Job.id` and `Job.name` and gave the rest
of the atomic commit no site list. The round 36 enumeration covers that half. This
covers the half a rename cannot reach: every call of the four classic-store
functions, which change NAME and, at `resolve_job_id`, ID SHAPE.

A site is one `(path, line, function)` triple, resolved by `ast` over the tracked
`.py` files `git ls-files` names, never by grep.
"""
import ast
import collections
import subprocess
import sys

SEAM = ("save_job", "load_job", "load_job_safe", "resolve_job_id")


def tracked():
    return [p for p in subprocess.run(["git", "ls-files", "*.py"],
                                      capture_output=True, text=True).stdout.split() if p]


def called_name(node):
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def main():
    per_file = collections.defaultdict(lambda: collections.defaultdict(set))
    parsed = failed = 0
    for path in tracked():
        try:
            tree = ast.parse(open(path, "rb").read(), filename=path)
        except SyntaxError:
            failed += 1
            continue
        parsed += 1
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                name = called_name(n)
                if name in SEAM:
                    per_file[path][name].add(n.lineno)

    prod = {p for p in per_file if not p.startswith("tests/")}
    test = {p for p in per_file if p.startswith("tests/")}
    sites = sum(len(v) for f in per_file.values() for v in f.values())
    print(f"tracked .py parsed {parsed}, unparsable {failed}")
    print(f"seam sites (path, line, function): {sites}")
    print(f"files: {len(per_file)}  production {len(prod)}  test {len(test)}")
    for name in SEAM:
        p = sum(len(per_file[f][name]) for f in prod)
        t = sum(len(per_file[f][name]) for f in test)
        print(f"  {name:<18} total {p + t:>4}  production {p:>4}  test {t:>4}")

    if len(sys.argv) > 1 and sys.argv[1] == "--rows":
        print()
        for path in sorted(per_file):
            cells = []
            for name in SEAM:
                lines = sorted(per_file[path][name])
                cells.append(f"{name}: " + (",".join(map(str, lines)) if lines else "-"))
            print(f"{path} | " + " | ".join(cells))


if __name__ == "__main__":
    main()
SEAMTOOL

## SPEC-SEAM → the NEW file `.agent/f275_t003_flip_seam.md`, GENERATED at C4

Write SEAMTOOL to `.remedy-wt/r38_seam_enum.py`, run it from the repository root
with and without `--rows`, and build the file from its real output.

THE FILE'S SECTIONS, in this order.
  1. A banner naming the base SHA the measurement was taken at, stating that the
     file ENUMERATES the classic store seam and that no line under `packages/`,
     `apps/`, `tests/` or `scripts/` moved in the round that wrote it.
  2. The instrument: SEAMTOOL's source, embedded verbatim in one fenced python
     block, and the exact command lines used.
  3. A figures table with a `measured` column, a `reviewer` column carrying the
     numbers below, and a `verdict` column reading `same` or `differs (<n>)`.
  4. THE ENUMERATION: the `--rows` output, one line per file, sorted by path, in
     the exact form the tool emits.
  5. How this list relates to `.agent/f275_t003_flip_sites.md`: the two file sets,
     their overlap, and what each instrument is blind to.

THE REVIEWER'S FIGURES, measured at `4921e117`:
  tracked `.py` parsed 991 · unparsable 0
  seam sites 821 · files 152 — production 52, test 100
  `save_job` 513 — production 70, test 443
  `load_job` 262 — production 123, test 139
  `load_job_safe` 6 — production 6, test 0
  `resolve_job_id` 40 — production 32, test 8
  the enumeration renders 152 file lines
  round 36 enumeration files 184 · seam files 152 · union 228
  files the seam ADDS, holding no enumerated `.id` or `.name` site 44
  files both instruments name 108

WHAT SECTION 5 MUST SAY, because a measurement's limits are part of its result.
The round 36 list is blind to a file that touches the classic store without
reading `.id` or `.name` — 44 files. The seam list is blind to a file that reads
those fields off a job it did not load through these four functions — 76 files.
Neither sees a site that is both unexecuted and statically unprovable, and that
remainder is given NO numeral because none was measured.

## Done when — GATES G1 to G8

Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code
and the real numbers. "Green" as a word is a finding. One line per gate in the
handback.

**G1 TRANSPORT (at C0b).** The committed `.agent/authored/f275-r38.md` and
`.agent/last_block.md` have the SAME sha256 as the reviewer's delegation source,
and resolve to ONE shared git blob. `.agent/last_block.md` is written from
`git cat-file blob HEAD:.agent/authored/f275-r38.md`, never retyped. State that
the chain covers those on-disk artefacts and claims nothing about emitted bytes.

**G2 THE PLAN (at C1).** `.agent/plan.md` is BYTE-EQUAL to the PLAN38 slice as
extracted — same length, same sha256. Report its line count against the
AGENTS.md cap of 50, and `^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2 and C3).** For each of the four appends — RECORD38, NOTE38
and SLIPS38 at C2, LANDED38 at C3 — post-blob equals pre-blob then ONE newline
then the slice, with constraint 3's baselines and each later append re-baselining
on the one before it; READ BACK the joining byte at offset len(pre) and report it
for each. Then an INDEPENDENT structural reader with N COUNTED FROM EACH SLICE and
not from this block: the last N blank-line units of the post-blob equal that
slice's N paragraphs IN ORDER. Then one negative control per append, flipping a
byte INSIDE THE FIRST appended paragraph, which BOTH readers must REJECT.
`^Gate: F275 R37 ` exactly 1 and `^Note: F275 R38 ` exactly 1 at C3.

**G4 THE OPEN SET (at C4).** BY DISTINCT ID, every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id, read at THIS round's base `4921e117` with
`git show 4921e117:.agent/live_review.md` into memory — never by writing over the
tracked file — and again at C4. Report both. Ids registered this round and ids
resolved this round must both be `[]`. Report SEPARATELY that `R-0870` IS STILL IN
the open set at C4 and carries NO `Done:` line — examined, not assumed.

**G5 PAIR F IS THE AUTHORED BYTES (at C3).** The FROM occurs EXACTLY 1x in
`docs/system/development-artifact-boundary-v0.md` before the edit and EXACTLY 0x
after; the TO occurs EXACTLY 1x after; and the applied file's post-blob equals its
pre-blob with the FROM span replaced by the TO span and nothing else, proved by
reconstructing the post-blob from the pre-blob and comparing sha256. Then the
property the repair exists for, measured through the SHIPPED catalog rather than by
grep: import `apps.cli.command_catalog`, take `sorted(GROUPS)`, and report which of
`worker`, `mission`, `approval` and `progress` are in it. The reviewer read
`worker` and `mission` PRESENT and `approval` and `progress` ABSENT at the base.

**G6 THE SCOPED GATE (at C3).** `python3 -B -m pytest tests/docs/ tests/cli/test_product_spine.py -q`,
which the reviewer read at `371 passed` at exit 0 with the repair applied.

**G7 THE COMMAND-SURFACE SWEEP (at C4).** Re-run the sweep the `Note: F275 R38`
slice describes: the fifteen groups DECISION F260 D3 records as deleted whole, in
the two shapes `` `<group>` `` and `remedy <group>`, over every tracked file under
`docs/`, `packages/` and `apps/` outside `docs/roadmap/` and `docs/archive/`.
Report the FULL hit list, never truncated, and the file count the sweep covered —
the reviewer read 569 files and 28 hits at the base. This is NOT a zero-gate and
the correct result is a NON-EMPTY list: `provider` and `builder` occur as a field
name and a role name, `overnight` as the cockpit SECTION key whose reader survives,
and several pages name a group and say in the same sentence that it is gone. State
for every hit which of those classes it falls in, and enumerate anything that falls
in none.

**G8 NOTHING ELSE MOVED (at C4).** `.agent/STOP` read FROM DISK: report present
or absent. `git status --porcelain`: EMPTY. `git worktree list`: exactly ONE
entry. `git diff --name-only 4921e117..C4` is an EXACT SET MATCH against the
`Change:` list above minus `.agent/handoff.md` — report MISSING and EXTRA
explicitly. Per-commit insertions for C0a through C4, each under the DECISION
F104 D1 cap of 500; the handback commit's own numbers are NOT ordered here,
per §3 item 14. Canary `python3 -m pytest tests/cli/test_golden_path.py -q`, and
`python3 -m ruff check .`, which the reviewer read at 26 against the ceiling its
own test pins.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
SESSION 17 of F275 and round 38, the per-commit table with `git diff --numstat`
values in the `+/-` column, one line per gate G1 to G8 with real exit codes, the
item-status table, the open-findings count by distinct id, and the deviations.
State explicitly that R-0870 is NOT resolved, that its fix is marked `Landed:` in
C3 and that the reviewer's `Done:` text is owed at the next gate. Add the one
sentence of context self-assessment amend0905-throughput requires. No PR is
created and nothing is merged: this round is not a closure sequence.
