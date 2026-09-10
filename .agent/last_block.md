── STEP T003 (4 of n) — F275 ─────────────────────────────────
Goal:        Land the SECOND MEASUREMENT finding R-0832 asks for — an event-name
             coupling ratchet beside the retired import map — so the coupling
             the map cannot see becomes visible and stays visible.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 34
             verdict and two prose slips · C3 the guard · C4 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r35.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`,
             `tests/orchestration/test_event_name_coupling.py` (NEW),
             plus `.agent/handoff.md` at C4.
Constraints: the numbered list below.
Done when:   gates G1 to G7 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

## Base

This round's base is `df5d527f`. THE GUARD BELOW WAS WRITTEN, RUN AND
RED-PROVED by the reviewer in a disposable worktree at that base before this
block was authored; every numeral below is that run's.

## What this round is, and what it is NOT

R-0832 records that the cluster deletion map measured IMPORT edges only, so a
consumer coupled to a deleted module by EVENT NAME is invisible to it and
survives as dead code. Its fix clause has TWO halves and this round lands the
FIRST: "extend the map, or add a second measurement beside it, that records
EVENT-NAME couplings from the cluster's emitters to their non-cluster readers"
— and then "name the event-coupled consumers in D3 so the deletion round removes
them in the same commit as their emitter".

THIS ROUND DOES NOT RESOLVE R-0832 and does not write a `Done:` paragraph for
it. The second half belongs to the round that drafts DECISION F260 D3, which is
where the DISPOSAL of each coupling is ruled. The reason the disposal is not
taken here is measured rather than preferred: the one dead coupling that exists,
`context_budget_optimized`, survives as a run-log SCHEMA entry and a UI
action-class entry, and DECISION F275 D18 ruled four rounds ago that a schema
for an event historical run logs still carry is KEPT rather than deleted. Which
of those two readings governs is a ruling, and D3 is where it belongs.

## Constraints

1. APPLY THE SLICE BYTE FOR BYTE. GUARD35 is a WHOLE NEW FILE: write it with
   `shutil.copyfile` semantics from the extracted slice, never by retyping, and
   never reflow it. If anything does not fit, DECLARE it and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, exactly. C1 is the first
   substantive commit, per §3 item 23.
3. THE CHANGE SET IS THE PATH LIST IN THE HEADER'S `Change:` LINE, together with
   `.agent/handoff.md` at C4. Stage by naming paths, never `git add -A`.
4. EVERY APPEND IS `pre + ONE newline + slice`. At the base
   `.agent/live_review.md` is 814121 bytes and `.agent/prose_slips.md` is 223959,
   each ending in a single `\n`. `.agent/decisions.md` is NOT touched.
5. NO PRODUCTION LINE MOVES AT ALL THIS ROUND. The only non-`.agent/` path is a
   NEW test file. Nothing under `packages/`, `apps/`, `docs/` or `scripts/` is
   edited, added or deleted, and G7 gates that.
6. DESTRUCTIVE VERIFICATION IS ISOLATED, inside a disposable `git worktree`
   under `.remedy-wt/`, never in the primary checkout. Remove and prune it
   before the handback.
7. THE FULL SUITE IS NOT ORDERED THIS ROUND. The change set holds one new test
   file and no production line, so the round gate is the scoped set G6 names
   plus the canary — verification tier 1 of
   docs/agents/planner_reviewer_prompt.md §3. The reviewer nevertheless ran the
   full serial suite over this exact change and read `18336 passed, 29 skipped`
   with ONE failure, `TestVitestFrontendTestFoundation::test_vitest_passes`,
   which is the known fresh-worktree artifact: `apps/ui/node_modules` did not
   exist on that first pass, and the same class re-ran GREEN at 4 passed once it
   did. Collection goes 18362 to 18366, the four tests this file adds.
8. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. The open set is 87 by
   distinct id at the base and must read 87 at C3. R-0832 STAYS OPEN by design,
   for the reason stated above. The next free id is R-0875 and this round does
   not spend it.
9. THE GUARD IS A RATCHET AND NOT A ZERO-GATE, deliberately. Its allowlist
   `KNOWN_DEAD_EVENT_COUPLINGS` holds exactly one entry today and its ceiling
   `_COUPLING_CEILING` is the LITERAL 1, not a length. A ceiling derived from
   the thing it bounds cannot fail — that is the defect F275 round 27 found in
   this reviewer's own advertisement guard, and this file does not repeat it.

## SLICE PLAN35 → whole-file replacement of `.agent/plan.md`

<<<PLAN35
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

ROUND 35 lands the SECOND MEASUREMENT finding R-0832 asks for: a ratchet that records
EVENT-NAME couplings from deleted modules to surviving readers, which the retired import map
could not see. It measures 43 deleted modules, two event names they emitted and exactly one
dead coupling, `context_budget_optimized`. R-0832 STAYS OPEN: its second half — ruling how
each coupling is disposed of — belongs to the round that drafts DECISION F260 D3.

## Next Steps

1. DECISION F260 D3: name all 43 deleted modules and the feature that inherited each one,
   rule the disposal of every dead event coupling the round 35 ratchet reports, and delete
   what that ruling condemns. This discharges the second half of R-0832 and is the last
   thing T001 owes.
2. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base with the DECISION F272 D7
   descriptor probe rather than inheriting round 31's figures.
3. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 2 is the largest single commit this repository will take and it spends the one
  declared-oversize allowance AGENTS.md rations per feature. It needs its own session.
- The open set is 87 by distinct id at this round's base `df5d527f`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
PLAN35

## SLICE RECORD35 → append to `.agent/live_review.md`

<<<RECORD35
Gate: F275 R34 — the F275 round 34 entry. VERDICT PASS, written by the planner and reviewer of session 16 after reading the committed range `bc77c7ac`..`df5d527f` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits C0a `30ccdd26`, C0b `4dcdd0b0`, C1 `e86466fa`, C2 `b92f6de7`, C3 `bd452b61`, C4 `0523aa36` and C5 `df5d527f`, per-commit insertions 388, 326, 18, 8, 16 and 70 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's scratch original at `.remedy-wt/f275-r34-block.md` was written AND HASHED BEFORE delegation at `82714e2ea0dca36a5ea051e2332e4648e16ef47d825a461d810af074c9faa07c`, and both committed copies are 34579 bytes at that digest as ONE shared git blob; the chain covers those three artefacts and nothing emitted into a prompt, per §3 item 37. G2: `.agent/plan.md` byte-identical to PLAN34 at 2261 bytes, 41 lines against the cap of 50, both mandated headings exactly once. G3 over all three append targets — `.agent/live_review.md` 808624, `.agent/prose_slips.md` 221335 and `.agent/decisions.md` 1033519 bytes before — each post-blob equal to its pre-blob then ONE newline then the slice as extracted, the joining byte READ BACK at offset len(pre) reading a newline in all three, the structural reader counting N from each slice and matching the last N blank-line units IN ORDER, and every negative control flipped INSIDE THE FIRST appended paragraph and REJECTED by BOTH readers. `^Gate: F275 R33 ` and `^## DECISION F275 D19 ` each exactly 1. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base and 87 at C4; this round registered none and resolved none, which is what DECISION F275 D19 makes correct — under D18's superseded reading two findings would have been owed here. G5 THE INHERITANCE LANDED AND THE REVIEWER RE-READ IT BY IMPORTING THE SHIPPED CATALOG: 220 commands in 44 groups with ZERO dangling `related=` references, the `is_expensive` set exactly `['job.resume']`, and `job.resume` carrying `job_id`, `--checkpoint`, `--dry-run`, `--cycles`, `--unattended`, `--yes` and `--json` in that order; `job.run` is ABSENT at C4 and was PRESENT at the base, where the catalog read 221 commands and the expensive set was `['job.run']` — the absence taken beside its presence, because neither reading means anything alone. G6 THE HANDLER SURVIVED, WHICH IS THE PROPERTY THE WHOLE T003 SEQUENCE TURNS ON: parsing `apps/cli/commands/job.py` with `ast` at C4 shows `_cmd_job_run_cycles` still defined with `_cmd_job_resume` as its SOLE referrer, so the one surviving door still reaches the bounded-cycles run and, under the shipped one-cycle default, the single pass beneath it. The two ordered mutations bite with named assertions: deleting the `yes=getattr(args, "yes", False),` passthrough from the dispatch lambda fires the exact-kwargs equality at `test_resume_cli.py:516`, and flipping the catalog entry's `is_expensive` to False fires both `test_command_catalog.py:105` and `:110` — which is the proof that F114's cost-preview contract genuinely MOVED to the inheriting command rather than being re-pointed at an assertion that would have passed either way. G7 IS THE GATE CONSTRAINT 8 EXISTED FOR AND IT HELD: the token-safe sweep took `job.run` from 26 lines in 7 files to ZERO and the spaced advertisement from 17 lines in 11 files to ZERO, while the ATTRIBUTE population `job.run_*` reads 34 lines BEFORE and 34 lines AFTER — untouched, which is the direct evidence that no attribute access was corrupted. The reviewer re-measured all four populations itself against the committed blobs rather than accepting the worker's reading. The full serial suite at C4 reads `18339 passed, 23 skipped` at exit 0, identical to the base, and the reviewer re-ran the canary, the catalog guards, the resume and escalation suites and the lint-ceiling test itself at 181 passed. G8: porcelain EMPTY, ONE worktree, `.agent/STOP` absent, `bc77c7ac..0523aa36` an EXACT set match over 21 paths with MISSING and EXTRA both empty and NO `node_modules` among them, and `ruff check .` at 26 against the frozen ceiling its own test pins. BOTH DECLARED DEVIATIONS ARE THE REVIEWER'S AND BOTH ARE SUSTAINED. FIRST, G7 ordered a `git diff` filtered to `job.resume_` to be EMPTY, and over the whole range it returns four matches — every one of them the block's OWN text, saved verbatim into `.agent/authored/f275-r34.md` and `.agent/last_block.md` by C0a and C0b. That is a gate quoting its own wording, and the worker did the right thing: it scoped the filter to C4, where the result is EMPTY, and reported both readings. SECOND, the SLIPS34 slice states the token-safe sweep would change "22 in 5" where the worker measured 20 in 5, because the reviewer's arithmetic subtracted the four catalog and dispatch lines but not the two lines pair E1 consumes in `tests/test_command_catalog.py`. It is non-load-bearing by the block's own construction — SPEC-INHERIT (3) states no expected sweep count and makes the ZERO readings binding — and the worker applied the slice byte for byte and declared it rather than reconciling, which is exactly right. NO FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.
RECORD35

## SLICE SLIPS35 → append to `.agent/prose_slips.md`

<<<SLIPS35
2026-09-10 · F275 R34 · The round 34 block's G7 ordered a `git diff` filtered to lines containing `job.resume_` to come back EMPTY, as the direct check that no attribute access had been corrupted by the id migration. Over the whole round the filter returns four matches, and every one of them is the block's OWN prose — the constraint and the gate that name the string — saved verbatim by C0a and C0b into `.agent/authored/` and `.agent/last_block.md`. The worker scoped the filter to the production commit, where it is genuinely empty, and reported both readings. A gate that greps for a token its own text contains is measuring the block before it measures the tree, and any such gate names the commit range that excludes the two block-save commits.

2026-09-10 · F275 R34 · The SLIPS34 slice predicted the token-safe sweep would change 22 lines in 5 files and the worker measured 20 in 5, because the reviewer subtracted the four catalog and dispatch lines consumed by earlier parts of the spec but forgot the two lines pair E1 consumes in `tests/test_command_catalog.py`. The block itself had already been corrected to state no expected sweep count at all, for exactly this ordering reason, so the stale figure survived only in the prose slip beside it — a numeral corrected in one clause and left standing in another, which is the R-0486 and R-0488 shape. When a block withdraws a numeral because it cannot be predicted, the withdrawal sweeps every slice the block ships, not only the clause that stated it.
SLIPS35

## SLICE GUARD35 → the WHOLE NEW FILE `tests/orchestration/test_event_name_coupling.py`

<<<GUARD35
"""The EVENT-NAME coupling ratchet — the second measurement finding R-0832 asks for.

WHAT THIS GUARDS. `tests/orchestration/test_cluster_deletion_map.py` built its
edge set from `import` statements parsed with `ast`, and DECISION F274 D2 ruled
the prototype-cluster deletion bounded by those edges. Finding R-0832 records
what that shape cannot see: a consumer coupled to a deleted module by EVENT NAME
holds no import of it, so the map correctly records no edge and the consumer
survives the deletion as dead code. R-0832's fix clause asks for a SECOND
measurement beside the map rather than a wider import walker, because a run-log
event name is a string literal and not an import.

WHAT IT MEASURES. For every `.py` module this branch deleted, the last living
blob is recovered from git and parsed for the event names it EMITTED — a string
literal in first-positional-argument position of a run-log emit call. Each such
name is then looked for in the SURVIVING tree, both as an emitter and as a
reader. A name with a surviving READER and no surviving EMITTER is a DEAD
COUPLING: a consumer kept alive by a producer that no longer exists.

WHY AN ALLOWLIST AND NOT A ZERO. The dead couplings that exist today are real
and their disposal is a ruling DECISION F260 D3 owes, not a repair a test may
make. So this is a RATCHET against a declared set, in the shape this repository
already uses for dead advertisements: the set may SHRINK and never grow, and an
entry that stops being a dead coupling must be removed from the list in the same
commit, or assertion (c) reds. Remedy deliberately does not delete a schema for
an event that historical run logs still carry; what it refuses is an INVISIBLE
coupling.
"""
from __future__ import annotations

import ast
import subprocess
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

BRANCH_BASE = "a5bf894946ab6de053a4232109d6341a63533768"

EMIT_FUNCS = frozenset({"log", "_emit", "emit", "log_event", "write_event",
                        "record_event"})

READER_SUFFIXES = (".py", ".ts", ".tsx")

# The dead couplings that exist today, each with the ruling that owns it.
# THIS LIST ONLY EVER SHRINKS. DECISION F260 D3 disposes of every entry.
KNOWN_DEAD_EVENT_COUPLINGS: tuple[str, ...] = (
    "context_budget_optimized",
)

_COUPLING_CEILING = 1


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                          capture_output=True, text=True, check=False).stdout


def deleted_modules() -> list[str]:
    out = _git("log", "--diff-filter=D", "--name-only", "--pretty=format:",
               f"{BRANCH_BASE}..HEAD", "--", "packages", "apps")
    return sorted({p for p in out.split() if p.endswith(".py")})


def _emitted_names(source: str, path: str) -> set[str]:
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else (
            fn.id if isinstance(fn, ast.Name) else None)
        if name not in EMIT_FUNCS:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            found.add(first.value)
    return found


def events_emitted_by_deleted_modules() -> dict[str, set[str]]:
    """Event name -> the deleted modules that emitted it."""
    emitted: dict[str, set[str]] = defaultdict(set)
    for path in deleted_modules():
        rev = _git("rev-list", "-n", "1", "HEAD", "--", path).strip()
        if not rev:
            continue
        blob = _git("show", f"{rev}^:{path}")
        if not blob:
            continue
        for name in _emitted_names(blob, path):
            emitted[name].add(path)
    return dict(emitted)


def dead_event_couplings() -> dict[str, list[str]]:
    """Event name -> surviving readers, for names nothing surviving emits."""
    emitted = events_emitted_by_deleted_modules()
    if not emitted:
        return {}
    survivors = [p for p in _git("ls-files", "packages", "apps").split()
                 if p.endswith(READER_SUFFIXES)]
    still_emitted: set[str] = set()
    readers: dict[str, list[str]] = defaultdict(list)
    for rel in survivors:
        try:
            text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for name in emitted:
            if name in text:
                readers[name].append(rel)
        if rel.endswith(".py"):
            still_emitted |= (_emitted_names(text, rel) & set(emitted))
    return {name: sorted(rs) for name, rs in readers.items()
            if name not in still_emitted and rs}


class TestEventNameCouplingRatchet:
    """Finding R-0832: the coupling the import map cannot see."""

    def test_the_instrument_sees_the_deleted_modules_at_all(self) -> None:
        # Anti-blindness floor: a measurement over an empty corpus proves nothing.
        assert len(deleted_modules()) >= 40

    def test_every_dead_coupling_is_declared(self) -> None:
        found = dead_event_couplings()
        undeclared = sorted(set(found) - set(KNOWN_DEAD_EVENT_COUPLINGS))
        assert not undeclared, (
            "an event-name coupling to a deleted module is not declared: "
            f"{ {n: found[n] for n in undeclared} }"
        )

    def test_the_declared_set_only_ever_shrinks(self) -> None:
        assert len(KNOWN_DEAD_EVENT_COUPLINGS) <= _COUPLING_CEILING

    def test_no_declared_entry_is_stale(self) -> None:
        found = dead_event_couplings()
        stale = [n for n in KNOWN_DEAD_EVENT_COUPLINGS if n not in found]
        assert not stale, (
            f"these are no longer dead couplings and must leave the list: {stale}"
        )
GUARD35

## Done when — GATES G1 to G7

Run every gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit
code and the REAL numbers. Every gate is ordered at a commit STRICTLY EARLIER
than C4, which writes the handback, per §3 item 31.

**G1 TRANSPORT (at C0b).** Report the sha256 and byte length of
`.remedy-wt/f275-r35-block.md`, and show the committed
`.agent/authored/f275-r35.md` and `.agent/last_block.md` BYTE-EQUAL to it.
`.agent/last_block.md` comes from `git cat-file blob` of the committed C0a blob,
never a retype. State that the chain covers three on-disk artefacts and makes no
claim about bytes emitted into a prompt.

**G2 THE PLAN (at C1).** Committed `.agent/plan.md` byte-equal to PLAN35; report
both byte lengths, the sha256, the line count against the cap of 50, and
`^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2).** For RECORD35 into `.agent/live_review.md` and SLIPS35
into `.agent/prose_slips.md`: report each pre-size, confirm it equals constraint
4's figure, show post == pre + ONE newline + slice, and read the joining byte
BACK at offset len(pre). Then the independent structural reader: count N from
each slice yourself, never from this block, and match the last N blank-line units
against the slice's N paragraphs IN ORDER. One negative control per append,
flipping a byte INSIDE THE FIRST appended paragraph, REJECTED by BOTH readers.
Then `^Gate: F275 R34 ` exactly 1.

**G4 THE OPEN SET (at C3).** BY DISTINCT ID from `.agent/live_review.md`: every
`^- R-\d+ — ` id minus every `^Done: R-\d+ — ` id. Report the count at the base
`df5d527f` and at C3; both must read 87. Report the ids registered and resolved
this round; both lists must be EMPTY. Report separately that `R-0832` is in the
OPEN set at C3 — constraint 8 requires it to stay there and an unexamined
absence would look identical to a resolution.

**G5 THE GUARD IS THE AUTHORED BYTES (at C3).** The committed
`tests/orchestration/test_event_name_coupling.py` byte-equal to the GUARD35
slice: report both byte lengths and the sha256 of each, and that the file did
NOT exist at the base. Then `ruff check` that one path and report its exact
output line.

**G6 THE GUARD BITES — RED PROOF (at C3).** In a disposable worktree at C3 with
`__pycache__` purged, run
`python3 -B -m pytest tests/orchestration/test_event_name_coupling.py -q`
UNMUTATED first and report the exit code and pass count as the control. Then
FIVE mutations, each reverted byte-exactly before the next, each reported with
WHICH assertion fired rather than only an exit code. The revert target is named
per mutation and each anchor occurs exactly ONCE in it.
  M1 — in the guard, delete the line `    "context_budget_optimized",` from
       `KNOWN_DEAD_EVENT_COUPLINGS`. Expect RED: a real dead coupling becomes
       undeclared.
  M2 — in the guard, insert `    "no_such_event_name",` as the first entry of
       `KNOWN_DEAD_EVENT_COUPLINGS`. Expect RED on TWO assertions: the ceiling
       and the staleness check.
  M3 — in the guard, replace the two-line `return {name: sorted(rs) ...}`
       comprehension that ends `dead_event_couplings` with `    return {}`.
       Expect RED: blinding the instrument must not read as a clean tree. This
       is the anti-blindness direction and it is the most important of the five.
  M4 — in the guard, weaken the floor `assert len(deleted_modules()) >= 40` to
       `>= 0`. The reviewer measured this GREEN and ORDERS IT ANYWAY, so the
       handback records the honest negative: a test that weakens its own
       assertion cannot detect that, which is why the floor is a separate test
       rather than a clause inside another one. Report the green.
  M5 — THE REAL-WORLD DIRECTION, and its revert target is a DIFFERENT FILE. In
       `packages/orchestration/event_schemas.py`, insert the line
       `    "context_pack_created": frozenset({"chars"}),` immediately above the
       line `    "context_budget_optimized": frozenset({`, which occurs exactly
       once in that file. Expect RED: a survivor that starts reading an event
       only a deleted module ever emitted is a NEW dead coupling and must be
       caught. Revert and confirm the control is green again.

**G7 NOTHING ELSE MOVED (at C3).** `.agent/STOP` read from disk and ABSENT.
`git status --porcelain` EMPTY. `git worktree list` exactly ONE entry. Branch
`feature/f275-one-world-completion-part-three`.
`git diff --name-only df5d527f..<C3>` an EXACT SET MATCH against the path list in
the header's `Change:` line, which does not include `.agent/handoff.md`, reported
as MISSING and EXTRA, both empty. Report that ZERO paths under `packages/`,
`apps/`, `docs/` or `scripts/` appear in that diff — constraint 5. Per-commit
insertions for every commit before the handback, each under the DECISION F104 D1
cap of 500. Then the canary `python3 -m pytest tests/cli/test_golden_path.py -q`
and the scoped set `python3 -m pytest tests/orchestration/ -q`, both serially,
with their real summary lines. Finally the collection count
`python3 -B -m pytest tests/ -q --collect-only` at the base and at C3: the
reviewer read 18362 and 18366.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
SESSION NUMBER 16 of feature F275, round 35, ONE LINE PER GATE with real exit
codes and real numbers, the changed-files table with the `+/-` column taken from
`git diff --numstat` (§3 item 28), the item-status table, the open-findings
count, and the one-sentence context self-assessment amend0905-throughput
requires. Declare every deviation.
