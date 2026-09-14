── STEP T001 (documentary remainder) — F275 — ROUND 30 ──
(The rule line above and the one at the end are each exactly 56 characters, per §3 item 37.)

Goal: Rule R-0873's eighteen pages, repair the part of that finding that is
mechanically checkable, and leave a guard so the checkable part cannot come back.
R-0873 records that an advertisement sweep is blind to a page documenting a deleted
mechanism. Most of that class needs a human ruling, and this round records one.
But part of it does not: a page that names a MODULE PATH makes a claim that is true
or false on disk, and nothing in this repository was checking it. Four such claims
were false, in three pages, every one naming a file F275 itself deleted.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r30.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN30
  C2   the record: LEDGER30 into `.agent/live_review.md`, DECISION30 into
       `.agent/decisions.md`
  C3   the five path repairs, pairs W1 to W5
  C4   the new guard `tests/docs/test_named_source_paths.py`
  C5   the handback

Change set — exactly these paths, nothing else:
  .agent/authored/f275-r30.md                      (C0a, new file)
  .agent/last_block.md                             (C0b)
  .agent/plan.md                                   (C1)
  .agent/live_review.md                            (C2, append)
  .agent/decisions.md                              (C2, append)
  docs/system/vocabulary.md                        (C3)
  docs/system/development-artifact-boundary-v0.md  (C3)
  docs/system/quality-baseline-v0.md               (C3)
  docs/system/reviewer-safety.md                   (C3)
  tests/docs/test_named_source_paths.py            (C4, new file)
  .agent/handoff.md                                (C5)

`docs/README.md` is NOT in this change set and no index row is owed: the one new
file is a TEST, and AGENTS.md's Documentation Updates rule registers `docs/` pages,
not test modules.

Constraints:
 1. Every slice is applied BYTE FOR BYTE. If a slice looks wrong, apply it anyway
    and DECLARE the doubt in the handback. Never repair a reviewer slice.
 2. Marker lines never reach a target file. Extract slices from the COMMITTED C0a
    blob, never from a retype.
 3. PAIR SHAPES, from the reviewer's own containment test, one reading per pair —
    `TO contains FROM: false` for W1, W3, W4 and W5, which are REWRITES and each
    get the FROM 1x -> 0x and TO 0x -> 1x proof. W2 is a DELETION: its TO is empty,
    so its proof is FROM 1x -> 0x and NO TO count is ordered for it.
 4. `tests/docs/test_named_source_paths.py` is a WHOLE NEW FILE and is written with
    `shutil.copyfile` semantics — the slice's bytes are the file's bytes, including
    its terminating newline, and nothing is appended to or trimmed from it. Prove it
    by comparing the committed blob to the extracted slice for BYTE EQUALITY, not by
    a line count.
 5. `.agent/STOP` is re-read FROM DISK before the FIRST commit and again before C4.
 6. Destructive verification runs ONLY inside a disposable `git worktree` under the
    gitignored `.remedy-wt/`, never in the primary checkout. Remove and prune it
    before the handback.
 7. Commit subjects carry NO leading-slash token or absolute path. C3's and C4's
    subjects name R-0873.
 8. No file outside the change set is edited, and no test is deleted, skipped or
    weakened to make a gate green.
 9. Do not re-verify rounds 27, 28 or 29.
10. `.agent/prose_slips.md` is NOT in this change set. Round 29's worker declared
    one imprecision in the round 29 block — its bracketed rename counts were
    post-V1 readings and the block did not say so — and that is recorded in
    LEDGER30's gate entry where the measurement lives, not as a separate slip.

──────── WHAT THE REVIEWER ALREADY MEASURED, by APPLYING all of it ────────

Applied in a disposable worktree at `fa2279da` and RUN. These are the numbers the
gates re-derive, not predictions. All five pairs applied FROM 1 -> 0. The new guard
sweeps `docs/system` and `docs/guides` and reads 244 source paths named with ZERO
missing; before the repairs it read four missing, in three pages. `ruff check` is
clean on the new file. `tests/docs/ tests/cli/` is green at 1651 passed, which is
round 29's 1648 plus this file's THREE tests. The diff is 113 insertions against 6
deletions over five files.

RED PROOFS ALREADY TAKEN, and G6 re-takes them. Control 3 passed. Reinstating a
deleted module path in an operator-facing page goes RED; reversing the extension
alternation so `tsx` is read as `ts` goes RED, which is the false-MISS the guard
was written to avoid rather than a false pass; and emptying the corpus goes RED on
the anti-blindness floor. Control green again afterwards, both mutated files
byte-identical to their originals.

WHY THE CORPUS EXCLUDES FOUR TREES, measured rather than assumed. Over all 377
tracked `.md` under `docs/`, 1105 source paths are named and 195 do not resolve.
187 of those 195 are in `docs/roadmap/`, which AGENTS.md's Documentation Structure
section rules describes what SHALL BE, so a feature file naming the module its
feature will create is CORRECT. `docs/ui/design_reference/` is a target spec in the
same sense. `docs/archive/` records abandoned designs. And `docs/agents/` QUOTES
paths in order to say they are wrong — finding R-0559's own text in
`planner_reviewer_prompt.md` names three non-resolving paths on purpose, and a
guard that cannot tell a quotation from a claim is satisfied by the quotation,
which is the R-0584 class. The remaining corpus is `docs/system` plus
`docs/guides`: the same two trees the advertisement guard sweeps, for the same
reason, and no page in them is skipped.

──────── The five path repairs ────────

W1 is a DELETION RECORD, and that is why it keeps the module NAME while dropping
the path: the sentence exists to say the module was deleted, so naming it is
right and spelling a path that cannot resolve is not.

<<<BEGIN W1 FROM>>>
(`packages/orchestration/overnight_mission.py`, `overnight contract-create |
contract-show | contract-readiness`)
<<<END W1 FROM>>>

<<<BEGIN W1 TO>>>
(the `overnight_mission` module and its `overnight contract-create |
contract-show | contract-readiness` commands)
<<<END W1 TO>>>

W2, in `docs/system/development-artifact-boundary-v0.md`, is a DELETION: the table
row lists a development artifact that no longer exists, so the row goes. Remove
the whole line including its newline.

<<<BEGIN W2 FROM>>>
| Progress command display | `apps/cli/commands/progress_cmd.py` | development progress display |
<<<END W2 FROM>>>

W3 and W4, in `docs/system/quality-baseline-v0.md`, sit in a dated "Top 10 coverage
gaps" table. The MEASUREMENTS are kept exactly — a coverage snapshot is a record
and rewriting its numbers would falsify it — and only the paths stop being paths,
because those two files were deleted after the snapshot was taken.

<<<BEGIN W3 FROM>>>
| 6.7% | 147 | apps/cli/commands/dogfood_cmd.py |
<<<END W3 FROM>>>

<<<BEGIN W3 TO>>>
| 6.7% | 147 | dogfood_cmd.py (deleted by F275) |
<<<END W3 TO>>>

<<<BEGIN W4 FROM>>>
| 11.2% | 83 | apps/cli/commands/external_builder_cmd.py |
<<<END W4 FROM>>>

<<<BEGIN W4 TO>>>
| 11.2% | 83 | external_builder_cmd.py (deleted by F275) |
<<<END W4 TO>>>

W5, in `docs/system/reviewer-safety.md`, was never a real path: it is a PLACEHOLDER
inside an example command, and it becomes one that reads as a placeholder.

<<<BEGIN W5 FROM>>>
(`scripts/remedy_pytest.sh tests/specific_file.py -q`)
<<<END W5 FROM>>>

<<<BEGIN W5 TO>>>
(`scripts/remedy_pytest.sh <test_file> -q`)
<<<END W5 TO>>>

──────── GUARD30 — the whole of `tests/docs/test_named_source_paths.py` ────────

A new file. Write the slice's bytes and nothing else, per constraint 4.

<<<BEGIN GUARD30>>>
"""F275 — a page that names a source file must name one that exists.

Finding R-0873 recorded a class the advertisement guard
(``tests/cli/test_advertised_commands.py``) is structurally blind to: a page can
document a mechanism that has been deleted without ever spelling one of its
commands. Most of that class needs a human ruling, but one part of it does not —
a page that names a MODULE PATH is making a claim that is true or false on disk,
and nothing was checking it. At F275 round 30 four such claims were false, in
three pages, every one of them a file this feature had deleted.

WHY THE CORPUS IS THE OPERATOR-FACING ONE AND NOT ALL OF ``docs/``. The same two
trees the advertisement guard sweeps, for the same reason: these are the pages an
operator reads as instructions. The trees deliberately left out are left out
because a path that does not resolve is CORRECT in them:

* ``docs/roadmap/`` describes what SHALL BE (AGENTS.md, Documentation Structure),
  so a feature file names the module its feature will create. 187 unresolved
  paths live there by design.
* ``docs/ui/design_reference/`` is a target spec in the same sense.
* ``docs/agents/`` quotes findings ABOUT paths that do not resolve — finding
  R-0559's own text in ``planner_reviewer_prompt.md`` names three such paths in
  order to say they are wrong, and a guard that cannot tell a quotation from a
  claim is satisfied by the quotation (the R-0584 class).
* ``docs/archive/`` records abandoned designs and is expected to name their
  modules.

That exclusion is a property of the corpus, not a way to make the sweep pass: no
page under ``docs/system/`` or ``docs/guides/`` is skipped.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: The same two trees ``tests/cli/test_advertised_commands.py`` sweeps.
_OPERATOR_FACING_ROOTS: tuple[str, ...] = ("docs/system", "docs/guides")

#: A source path as a page writes one. ``tsx`` precedes ``ts`` in the extension
#: alternation on purpose: with ``ts`` first, ``RemedyShell.tsx`` matches as
#: ``RemedyShell.ts`` and the guard reports a miss on a file that exists.
_SOURCE_PATH_RE = re.compile(
    r"(?:packages|apps|tests|scripts)/[\w./-]*\.(?:tsx|ts|py|sh|json|toml)"
)


def _tracked_files() -> set[str]:
    listing = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=True,
    ).stdout
    return set(listing.splitlines())


def collect_named_source_paths() -> tuple[int, list[str]]:
    """Return (paths named, sites naming a path that does not exist)."""
    tracked = _tracked_files()
    named = 0
    missing: list[str] = []
    for root in _OPERATOR_FACING_ROOTS:
        listing = subprocess.run(
            ["git", "ls-files", root], cwd=REPO_ROOT,
            capture_output=True, text=True, check=True,
        ).stdout
        for relative_path in listing.splitlines():
            if not relative_path.endswith(".md"):
                continue
            source = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for line_number, line in enumerate(source.splitlines(), 1):
                for match in _SOURCE_PATH_RE.finditer(line):
                    named += 1
                    if match.group(0) not in tracked:
                        missing.append(f"{relative_path}:{line_number}: {match.group(0)}")
    return named, missing


def test_every_source_path_an_operator_facing_page_names_exists() -> None:
    named, missing = collect_named_source_paths()

    # Anti-blindness: a sweep that matches nothing satisfies a zero-gate
    # perfectly. The real figure was 244 when this guard was written, so 100 is
    # a floor with room rather than a pin on today's count.
    assert named > 100, f"the source-path sweep went blind: only {named} paths matched"

    assert not missing, (
        "an operator-facing page names a source file that does not exist — "
        "delete or repair the reference in the same commit as the file:\n"
        + "\n".join(missing)
    )


def test_the_sweep_reports_a_path_that_does_not_exist() -> None:
    """The guard's own discriminator: it must be able to find a miss."""
    tracked = _tracked_files()

    assert "packages/orchestration/no_such_module.py" not in tracked
    assert _SOURCE_PATH_RE.findall(
        "see `packages/orchestration/no_such_module.py` for details"
    ) == ["packages/orchestration/no_such_module.py"]


def test_the_extension_alternation_does_not_truncate_tsx() -> None:
    """``.tsx`` must not be read as ``.ts`` — that reported a false miss."""
    assert _SOURCE_PATH_RE.findall("`apps/ui/src/RemedyApp.tsx` composes") == [
        "apps/ui/src/RemedyApp.tsx"
    ]
<<<END GUARD30>>>

──────── PLAN30 — the whole of `.agent/plan.md` ────────

<<<BEGIN PLAN30>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 30 closes R-0873. DECISION F275 D16 rules all eighteen pages the capability sweep
flagged — none has a deleted mechanism as its SUBJECT, so none is deleted; the archive pages
already carry banners and are left. The checkable half is repaired: four operator-facing
pages named module paths F275 had deleted, and a fifth spelled a placeholder as a path. A
new guard sweeps `docs/system` and `docs/guides` so a page can no longer name a source file
that does not exist.

## Next Steps

1. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route between one commit, a declared oversize commit, or an operator amendment. No
   production line moves in that slice, and it wants a fresh session.
2. T003, the classic runner, which T002's ruling is the prerequisite for.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 88 by distinct id at this round's base `fa2279da`, computed mechanically
  from the record. This round registers none and resolves one, leaving 87. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- T001's documentary remainder is finished with this round. What is left of F275 is T002 and
  T003, both of which are production-code slices, and T002's ruling gates T003 entirely.
<<<END PLAN30>>>

──────── DECISION30 — appended to `.agent/decisions.md` ────────

<<<BEGIN DECISION30>>>
## DECISION F275 D16 (2026-09-10) — THE EIGHTEEN PAGES R-0873 FLAGGED ARE RULED PAGE BY PAGE, AND NONE IS DELETED

CONTEXT. R-0873 measured that eighteen tracked non-roadmap pages under `docs/` still name a concept belonging to a module F275 deleted, and its fix clause binds the round that finishes R-0872 to rule each one DELETE, DATE or LEAVE. R-0872 was finished at round 29; this is that ruling. The measurement it rules on was retaken at `fa2279da` by the reviewer, over the 89 production `.py` paths F275 deleted across `a5bf8949..HEAD`, reduced to 43 module stems of which 41 are distinctive and 2 (`provider`, `progress`) excluded as English-generic and reported as excluded.

CHOSEN. NO PAGE IS DELETED, because no page's SUBJECT is a deleted mechanism — which is the condition R-0873 itself set for deletion, and it was tested rather than assumed. The two pages that looked likeliest, `docs/system/self-dogfood-v0.md` and `docs/system/self-dogfood-execution-v0.md`, document `packages/orchestration/self_dogfood.py` and `packages/orchestration/self_dogfood_execution.py`, and BOTH modules are alive on disk at `fa2279da` and reachable through a live `self` command group of eight ids — `self.inspect`, `self.plan`, `self.propose`, `self.execute`, `self.status`, `self.reconcile`, `self.integrity` and `self.report`. What died was the `dogfood` command GROUP, not the mechanism; the pages name the mechanism, so they are accurate.

THE RULING, in three classes. LEAVE, six pages, all under `docs/archive/`: `external-builder-sandbox-future.md`, `model-route-tournament-future.md`, `expensive-builder-routing-future.md`, `expensive-builder-routing-v0-plan.md`, `self-dogfood-overnight-future.md` and `candidate-generator-adapter-future.md`. Every one of the six already carries a `> **Status` banner, which was measured and not assumed, and an archive of abandoned designs that stopped naming the designs it abandoned would be an archive of nothing. ALREADY DATED, three pages that carry a `> **Status` banner and need no further action: `docs/system/orchestrator-brain-v0.md`, `docs/system/mission-run-loop-morning-report-v0.md` and — from round 26 — the `Group-first CLI v0` section of `docs/system/architecture.md`. LEAVE AS INCIDENTAL, the remainder: `docs/README.md`, `docs/system/vocabulary.md`, `docs/system/core-product-spine-v0.md`, `docs/system/test-lanes-v0.md`, `docs/system/token-economy-context-budget-optimizer-v0.md`, `docs/system/development-artifact-boundary-v0.md`, `docs/system/quality-baseline-v0.md`, `docs/system/self-dogfood-v0.md`, `docs/system/self-dogfood-execution-v0.md` and `docs/guides/do-continue-v1.md`. Each names a deleted module's concept in passing rather than as its subject, and each is a live page about a live thing.

WHAT IS REPAIRED RATHER THAN RULED, and it is the part of R-0873 that never needed a judgement. A page that names a MODULE PATH makes a claim that is true or false on disk. Four such claims were false at `fa2279da`: `docs/system/vocabulary.md` named `packages/orchestration/overnight_mission.py`, `docs/system/development-artifact-boundary-v0.md` named `apps/cli/commands/progress_cmd.py`, and `docs/system/quality-baseline-v0.md` named `apps/cli/commands/dogfood_cmd.py` and `apps/cli/commands/external_builder_cmd.py`. A fifth site, `docs/system/reviewer-safety.md`, spelled a PLACEHOLDER as a path. All five are repaired in this round's C3, and `tests/docs/test_named_source_paths.py` makes the class impossible to reintroduce in the two operator-facing trees.

ALTERNATIVES CONSIDERED. (a) Date every one of the eighteen with a banner — rejected because a banner on a live page about a live mechanism is noise that teaches a reader to ignore banners, and because ten of the eighteen carry only a passing mention. (b) Widen the new guard to all of `docs/` — rejected on a measurement rather than a preference: 195 of the 1105 source paths named across `docs/` do not resolve, and 187 of those are in `docs/roadmap/`, where naming a module a feature has not built yet is exactly what a roadmap file is for. A guard there would forbid the roadmap from being a roadmap. (c) Delete the two self-dogfood pages on the strength of the word `dogfood` — rejected because the modules are alive, which the ruling measured; deleting them would have destroyed documentation of a shipping capability on the evidence of a renamed command group.

HOW TO REVERSE. Delete this paragraph and, if the guard is also unwanted, delete `tests/docs/test_named_source_paths.py`. The ruling binds no page that does not exist yet: a page written after this date is governed by the guard where the guard reaches, and by nothing else here.
<<<END DECISION30>>>

──────── LEDGER30 — appended to `.agent/live_review.md` ────────

Two paragraphs, blank-line separated.

<<<BEGIN LEDGER30>>>
Gate: F275 R29 — the F275 round 29 entry. VERDICT PASS, written by the planner and reviewer of session 14 after reading the committed range `99e677f0`..`fa2279da` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs, and booked here by round 30 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1. Seven single-parent commits C0a `4e9ed17d`, C0b `fd07d29a`, C1 `72b9994d`, C2 `b881f25b`, C3 `60c96b5c`, C4 `047972e5` and C5 `fa2279da`, per-commit insertions 317, 259, 17, 4, 39, 2 and 235, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: scratch original and both committed copies 26767 bytes at `11b8bb509713cd02bd9fa7d604b909805ad5bf0bd7a9d7ec769fe64d18652b3e`, BYTE-EQUAL. G2: `.agent/plan.md` byte-identical to PLAN29 at 2268 bytes, 42 lines against the cap of 50. G3: `.agent/live_review.md` 775926 to 783650, post equal to pre plus ONE newline plus the slice, the joining byte READ BACK as a newline, the structural reader counting N=2 from the slice and matching in order, and the negative control flipped inside the FIRST appended paragraph and REJECTED by BOTH readers. THE OPEN SET FELL 89 TO 88 BY DISTINCT ID over 102 registrations against 14 resolutions. G4: V1 and V2 each FROM 1 to 0 and TO 0 to 1, and all 22 rename mappings reached ZERO, with the reviewer measuring 38 occurrences before V1 where the block's brackets total 37 — the difference is V1 itself and it is the block's imprecision, not the worker's: the bracketed counts were POST-V1 readings and the block never said so, which the worker measured and declared rather than quietly reconciling. G5 IS THE READING THIS ROUND WAS BUILT AROUND: at C3, with the allowlist still present, the operator-facing sweep read ZERO unresolved and ALL TWENTY-TWO allowlist entries stale, so the guard suite was RED between C3 and C4 at 1 failed and 5 passed — the ratchet correctly demanding its own deletion, which is the behaviour round 27 designed and the first time it has been exercised at zero. G6: after C4 the module holds ZERO occurrences of `KNOWN_DEAD_DOC_ADVERTISEMENTS`, `_ALLOWLIST_CEILING` and `only_ever_shrinks`; `ruff check` reads `All checks passed!`, and it is the ONLY check that could have caught an incomplete removal, because the reviewer's own dry run left a reference behind inside a comprehension over an empty list and `pytest` reported green while the module named an undefined symbol; the guard runs 5 passed; and the RED PROOF in a disposable worktree gives control 5 passed, `remedy absorb` restored 1 failed, revert byte-identical. G7: `tests/docs/ tests/cli/` green at 1648 passed run SERIALLY, and the 1649-to-1648 delta was PROVED rather than asserted — the range touches exactly one `tests/` path whose `def test_` set goes 6 to 5 with the removed name printed and the added set empty. The catalog is unchanged at 222, 44 and ZERO dangling `related=` over 286, resolved on the DOTTED id after round 28's worker declared a reader that got that wrong. All 22 rename TO pairs resolve in the shipped `CATALOG`, which the reviewer re-checked itself. Porcelain EMPTY, ONE worktree, `.agent/STOP` absent, and `99e677f0..047972e5` an EXACT set match over seven paths. TWO WORKER DOUBTS ARE SUSTAINED AND CARRIED, neither repaired and both belonging to R-0873's neighbourhood rather than to this round: `architecture.md` lines 1901 and 1909 still call `remedy project show` a "backward-compat" alias, which describes a live catalogued command as legacy; and `UnresolvedAdvertisement.key` is now a READERLESS property whose docstring still describes "the allowlist key", both of its call sites having been deleted with the allowlist — the R-0855 pattern arriving one level below the deletion, and `ruff` does not flag it because a property is a definition and not an import. NO FINDING IS RESOLVED BY THIS GATE; R-0872 was resolved by round 29's own C2.

Done: R-0873 — RESOLVED at F275 round 30, by the commit constraint ordering of that round's block, which fixes C2 as the commit carrying the ruling and C3 and C4 as the commits carrying the repair and the guard; the readings below are the reviewer's own, taken by APPLYING the change in a disposable worktree at `fa2279da` before the round was delegated. THE FIX CLAUSE ASKED FOR A PAGE-BY-PAGE RULING and it is recorded as DECISION F275 D16 in `.agent/decisions.md`: six `docs/archive/` pages LEFT, all six already carrying a `> **Status` banner which was measured rather than assumed; three pages already DATED; ten LEFT as incidental mentions; and NONE DELETED. The condition R-0873 set for deletion — that a page's SUBJECT be a deleted mechanism — is met by no page, and the two that looked likeliest were tested rather than guessed: `self-dogfood-v0.md` and `self-dogfood-execution-v0.md` document `self_dogfood.py` and `self_dogfood_execution.py`, both alive at `fa2279da` and reachable through a live `self` group of eight command ids. What died there was the `dogfood` command GROUP, not the mechanism. THE HALF THAT NEEDED NO JUDGEMENT IS REPAIRED AND THEN GUARDED, and this is what the finding is really worth. A page naming a MODULE PATH makes a claim that is true or false on disk, and four were false: `vocabulary.md` named `overnight_mission.py`, `development-artifact-boundary-v0.md` named `progress_cmd.py`, and `quality-baseline-v0.md` named `dogfood_cmd.py` and `external_builder_cmd.py` — every one a file F275 itself deleted, and not one visible to any advertisement sweep, because none of them is a command. A fifth site spelled a placeholder as a path. `tests/docs/test_named_source_paths.py` now sweeps `docs/system` and `docs/guides` and reads 244 paths named with ZERO missing, and it bites: reinstating a deleted path goes RED, emptying the corpus goes RED on an anti-blindness floor, and reversing the extension alternation so `.tsx` reads as `.ts` goes RED — that last one guarding a FALSE MISS the reviewer hit while writing the sweep, which reported three non-defects in `docs/ui/design_reference/` before the alternation was ordered. WHAT THIS RESOLUTION DOES NOT CLAIM, stated because the finding's own text is wider than its repair: the guard reaches PATHS, not SUBJECTS. A page that describes a deleted mechanism in prose, naming no module path and no command, is invisible to it exactly as it was invisible to the advertisement sweep, and DECISION F275 D16 is a dated ruling rather than a mechanism — it binds no page written after it. That residue is real and is left deliberately unguarded rather than covered by a gate that could not honestly hold it.
<<<END LEDGER30>>>

Done when — the gates below, G1 to G7, inside the amend0827 rule 5 budget of
eight. Each is run with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with real exit
codes and real numbers in the handback, ONE LINE PER GATE. G1 to G6 are ordered at
commits strictly before C5, per §3 item 31.

G1 TRANSPORT (at C0b). `sha256sum` of the scratch original at
   `.remedy-wt/f275-r30-block.md`, of the committed `.agent/authored/f275-r30.md`
   and of the committed `.agent/last_block.md` are ONE comparison and must be equal.

G2 THE PLAN (at C1). `.agent/plan.md` byte-identical to PLAN30; report
   `written == slice`. Line count under the AGENTS.md cap of 50. `^## Goal$` and
   `^## Next Steps$` each exactly 1.

G3 THE RECORD (at C2), full byte forensics, BOTH append targets — `.agent/decisions.md`
   earns it as well as `.agent/live_review.md`, per the amend0827 rule 5 wording that
   names both. `.agent/live_review.md` is 783650 bytes before and `.agent/decisions.md`
   is 1012375. For each: post == pre + ONE newline + slice, with the joining byte READ
   BACK from the committed post-blob at offset len(pre) and shown to be a newline; plus
   an INDEPENDENT structural reader comparing the LAST N blank-line units against the
   slice's N paragraphs IN ORDER, N COUNTED BY THE SCRIPT from the slice and never taken
   from this block; plus a negative control flipping one byte inside the FIRST appended
   paragraph, which BOTH readers must REJECT while both accept the truth. Then
   `^Gate: F275 R29 ` == 1, `^Done: R-0873 — ` == 1 and `^## DECISION F275 D16 ` == 1.
   Then THE OPEN SET BY DISTINCT ID: it reads 88 at the base `fa2279da` over 102
   registrations against 14 resolutions; this commit registers none and resolves one, so
   it must read 87.

G4 THE PATH REPAIRS (at C3). W1, W3, W4 and W5 each FROM 1 -> 0 and TO 0 -> 1; W2
   FROM 1 -> 0 with NO TO count, per constraint 3. Then, over the four edited pages,
   report the total line count of each before and after.

G5 THE GUARD IS THE FILE THAT WAS AUTHORED (at C4). The committed blob of
   `tests/docs/test_named_source_paths.py` is BYTE-EQUAL to the GUARD30 slice as
   extracted from the committed C0a blob — report the two byte lengths and the two
   sha256 values and the equality, not a line count. Then `ruff check` on it, real
   message. Then, through the WORKER's OWN import of the new module,
   `collect_named_source_paths()` — report `named` and the FULL list of `missing`,
   which must be 244 and EMPTY. If `named` differs from 244, that is a deviation to
   DECLARE with the number you measured, not a reason to stop.

G6 THE RED PROOFS (after C4, inside a disposable worktree at the C4 commit, per
   constraint 6). Run the UNMUTATED control FIRST and report its exit code and count.
   Then THREE mutations, one at a time, each reverted byte-exactly before the next,
   each reported with its real exit code:
     M1 restore `apps/cli/commands/dogfood_cmd.py` into W3's repaired row in
        `docs/system/quality-baseline-v0.md` -> must go RED.
     M2 reverse the extension alternation in `_SOURCE_PATH_RE` so it reads
        `(?:ts|tsx|py|sh|json|toml)` -> must go RED, because `.tsx` then matches as
        `.ts` and the guard reports a miss on a file that exists. This mutation
        proves the guard against a FALSE MISS, which is the opposite direction from
        M1 and is why both are ordered.
     M3 set `_OPERATOR_FACING_ROOTS` to the empty tuple -> must go RED on the
        anti-blindness floor, not silently pass with zero findings.
   Then re-run the control and prove every mutated file byte-identical to bytes
   captured before the first mutation. A mutation that comes back GREEN is a finding.

G7 NOTHING ELSE MOVED (at C4, before C5).
   - `python3 -m pytest tests/docs/ tests/cli/ -q` run SERIALLY — report passed and
     failed. It must be GREEN at 1651, which is round 29's 1648 plus the THREE tests
     this round's new file adds; prove the delta is exactly those three by naming
     them, rather than reporting a bare number.
   - Through the shipped reader `apps.cli.command_catalog`: `len(_BASE_CATALOG)`,
     `len(GROUPS)` and dangling `related=` resolved on the DOTTED id — 222, 44 and 0
     at `fa2279da` and unchanged, because this round touches no command.
   - `tests/cli/test_advertised_commands.py` still reads ZERO unresolved on BOTH
     corpora, so this round's doc edits introduced no dead advertisement.
   - `.agent/STOP` absent (from disk), `git status --porcelain` EMPTY,
     `git worktree list` exactly ONE entry, branch correct.
   - `git diff --name-only fa2279da..<C4>` an EXACT SET MATCH against the change set
     minus `.agent/handoff.md`; report MISSING and EXTRA explicitly.
   - Per-commit insertions for every commit BEFORE the handback commit, against the
     DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — feature
and round, SESSION 14 of F275, branch, per-commit changed-files table with `+/-`
transcribed cell by cell from `git show --numstat` (§3 item 28), one line per gate
with real exit codes, the item-status table covering C0a..C5, W1..W5, GUARD30,
G1..G7 and R-0873, every deviation declared, the open-findings count, and the next
expected action. It has NO length cap. Push the branch. Create NO pull request.

────────────────────────────────────────────────────────
