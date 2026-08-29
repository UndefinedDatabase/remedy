# F033 — Hunk-level diff approval · ROUND 13 · THE SHARED EVIDENCE-DIRECTORY RESOLVER

SESSION 4 of feature F033. Round 13, rounds so far 13.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R13`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline. Every APPEND
   slice is joined to its file as: the base blob, then one newline, then the
   slice, and the result ends in exactly one newline. Take a slice as the bytes
   from the end of its `<<<SLICE` marker line up to and INCLUDING the newline
   that ends its last content line.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON IS A SPEC, NOT A SLICE. You write the code and the tests from the
   description. Names, signatures and the behaviours the SPEC fixes are binding;
   structure, comment wording and test names are yours. If the SPEC is
   impossible, STOP and say so rather than inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>`. NEVER write a base
   blob over a tracked file.
9. Purge `__pycache__` or use `python3 -B` whenever a mutation must reach a test.
10. Byte OFFSETS and byte SPANS are measured on BYTES, never on a decoded string.
11. IF A GATE AND A SPEC PARAGRAPH DISAGREE, the GATE is load-bearing: satisfy it,
    satisfy the SPEC's INTENT around it, and declare the disagreement.

## Base

BASE is `d526dfb5bb89bf83c5a23ed506f3843b1278e496`, the commit that closed session
3, on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 12 PASSED. The reviewer of session 3 re-executed all eight of that round's
gates at `c4ad00c4`, reproduced every ordered reading, ran all four ordered
mutations plus one of its own in its own disposable worktree, and wrote the
verdict into `.agent/handoff.md`, which is committed and pushed at BASE. Under
operator amendment amend0827-process-diet rule 1 that file is a durable carrier,
so C2 books that verdict into `.agent/live_review.md` and C3 appends the two
reviewer prose slips it carries. Neither buys a round of its own, and this round
is not a bookkeeping round: it ships production code.

THE PLAN SAID THE CLI COMMAND WAS NEXT. It still is — but reading the ground for
it surfaced one seam that must be fixed first, and this round is that seam.

WHAT THE CLI COMMAND WILL NEED. `packages/orchestration/hunk_decision_record.py`'s
`record_hunk_decision_from_view` takes the viewer's ENVELOPE, and the thing that
produces that envelope is `packages/orchestration/diff_view_source.py`'s
`build_diff_view(evidence_dir, task_id)`. Its first argument is a DIRECTORY, and
somebody has to decide WHICH directory a given job's diff lives in.

WHO DECIDES IT TODAY, measured at BASE. `packages/orchestration/ui_server.py`
holds a module-level private function `_resolve_evidence_dir(job_id)` — 18 lines,
four call sites in that file, two of them the very `build_diff_view` calls the
F037 viewer serves its diffs from. It reads
`<data root>/job_evidence_index/<job_id>.json` BY NAME, takes `evidence_dir_local`
from it when that names a real directory, and otherwise falls back to a
repo-relative `remedy-job-evidence-<job_id>` directory, and otherwise answers
None.

WHY A SECOND COPY WOULD BE A DEFECT AND NOT A DUPLICATION. The F033 write door
records an operator's decision over the hunks THE OPERATOR WAS SHOWN. The viewer
showed them out of whatever directory `_resolve_evidence_dir` picked. If the CLI
picks by a second rule, the two can disagree, and the operator's recorded consent
then names hunks from a diff nobody rendered — which is exactly the class of harm
`HUNK_RECORD_REFUSAL_NO_DIFF` was minted for in round 12, arriving through the
resolution instead of through the artifact. There is no honest way to write the
CLI handler without answering this, so it is answered here, once, before the
command exists.

MEASURED, SO THAT THE MOVE IS A MOVE. `packages/orchestration/evidence_index.py`
already owns this index — it is the module whose own docstring says it reads and
writes `<REMEDY_DATA_DIR>/job_evidence_index/`, it already imports
`job_evidence_index_dir` from `data_paths`, and it already carries the reader
`find_record`. It is where a reader searching for "which evidence directory" will
land. But `find_record` is NOT this rule: it loads EVERY record through
`load_index_records` and matches on the `job_id` KEY INSIDE each file, while
`_resolve_evidence_dir` opens `<job_id>.json` BY NAME and never reads that key.
A record file written without a `job_id` key resolves under the second rule and
would stop resolving under the first. So this round MOVES the existing rule and
does not re-express it on top of `find_record`; the SPEC says so and G6 measures
it.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 12 verdict into `.agent/live_review.md`
- C3 the two dated prose slips into `.agent/prose_slips.md`
- C4 `resolve_job_evidence_dir` in `packages/orchestration/evidence_index.py`,
  and `packages/orchestration/ui_server.py` delegating to it — ONE commit,
  because a delegation whose target does not yet exist is a broken tree
- C5 its tests in `tests/orchestration/test_evidence_index.py`
- C6 the handback

You write NO `Done:` paragraph — `Done:` is the reviewer's word. This round
registers no finding and resolves none, so there is no `Landed:` line and no
`Landed:` commit.

## Change set — these paths and nothing else

    .agent/authored/f033-r13.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/evidence_index.py
    packages/orchestration/ui_server.py
    tests/orchestration/test_evidence_index.py
    .agent/handoff.md

NEW FILES, named rather than counted: `.agent/authored/f033-r13.md`. This round
does NOT touch `packages/orchestration/hunk_decision_record.py`,
`packages/orchestration/hunk_ledger.py`,
`packages/orchestration/hunk_apply.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/diff_view_source.py`,
`packages/orchestration/diff_parser.py`, `apps/cli/command_catalog.py`,
`apps/cli/commands/patch.py`, `apps/cli/grouped.py`,
`tests/ui_server/test_command_channel.py`, `tests/test_command_catalog.py` or
`docs/roadmap/STATUS.md`. THE DOOR, THE CATALOG AND THE WHOLE HUNK LAYER ARE
PROVABLY UNCHANGED and G8 measures it. `.agent/context.md` is deliberately NOT
touched.

## SPEC — `packages/orchestration/evidence_index.py`

An EDIT that ADDS ONE public function. Every name that exists today keeps its
name, its signature and its behaviour.

    def resolve_job_evidence_dir(job_id: str, index_dir: Path | None = None) -> Path | None:

Place it beside `find_record`, in the same module-level style as its neighbours.

ITS BODY IS THE MOVED RULE, and the move is behaviour-preserving in both
directions. In order:

1. Compute the index file as `(index_dir or job_evidence_index_dir()) / f"{job_id}.json"`.
   Everything from here to the end of step 2 sits inside ONE `try`.
2. If that file exists, parse it with `json.loads(...read_text())`, take
   `record.get("evidence_dir_local", "")`, and when that value is truthy AND
   `Path(value).is_dir()`, RETURN `Path(value)`.
3. The `except` clause catches EXACTLY `(ImportError, OSError, ValueError, KeyError)`
   and does nothing but fall through. DO NOT widen it and DO NOT narrow it. A
   behaviour-preserving move preserves the behaviour it found, including the
   inputs it does not handle: a record file holding a JSON list raises
   `AttributeError` out of this function TODAY, and it must still do so, because
   changing that is a different change and is not this round's. `ImportError` is
   retained from the moved original and is now unreachable, since
   `job_evidence_index_dir` is imported at module level here rather than inside
   the `try`; say that in a comment rather than dropping the name.
4. Then `Path(f"remedy-job-evidence-{job_id}")`, returned when it `is_dir()`.
   This path is RELATIVE and resolves against the current working directory,
   exactly as it does today. Say so in a comment — it is the half of this rule a
   reader is most likely to misread as absolute.
5. Otherwise `None`.

`index_dir` is NEW and defaults to None, matching `load_index_records` and
`find_record` in this same module so a test can point it at a `tmp_path` without
setting an environment variable. With the default, the computed path is
byte-identical to what `resolve_data_root() / "job_evidence_index" / f"{job_id}.json"`
produces today, because `job_evidence_index_dir()` is defined as exactly that.

THE ONE-LINE WHY SITS DIRECTLY ABOVE THE DEFINITION, per AGENTS.md's Code
Discoverability Conventions, and the docstring carries three things: that this is
what decides which directory the F037 viewer and the F033 decision doors read a
diff out of, so both get ONE answer; that it reads `<job_id>.json` BY NAME and
deliberately does NOT go through `find_record`, which matches on the `job_id` key
INSIDE the file and would therefore stop resolving a record written without that
key; and that `packages/orchestration/ui_server.py`'s `_resolve_evidence_dir` is
now a delegation to it and is kept only because callers import that name.

## SPEC — `packages/orchestration/ui_server.py`

An EDIT that REPLACES ONE FUNCTION BODY and nothing else.

`_resolve_evidence_dir` keeps its exact name, its exact signature
`(job_id: str) -> Path | None`, and its position in the file. Its body becomes a
docstring plus a local import of `resolve_job_evidence_dir` from
`packages.orchestration.evidence_index` plus a single `return` of that call with
`job_id` passed through and NOTHING else passed. The local-import idiom is the
file's own: `_build_diff_json` imports `build_diff_view` the same way.

The docstring says the implementation moved and names the module it moved to,
and says why the name survives here: callers import it, including
`tests/orchestration/test_final_audit_evidence.py`, which imports it from
`ui_server` directly.

Its four call sites in that file are UNCHANGED. No other line of
`packages/orchestration/ui_server.py` changes, and G6 measures that as a line
count on the commit's own diff.

## SPEC — `tests/orchestration/test_evidence_index.py`

An EDIT that ADDS. Every existing test stays untouched and must still pass —
that is half the proof the move moved nothing.

Add tests, each pinning ONE property, every one of them passing `index_dir`
explicitly and using `monkeypatch.chdir(tmp_path)` so the relative fallback of
step 4 can never resolve against this repository's own working tree:

- an index file naming an `evidence_dir_local` that EXISTS returns exactly that
  directory as a `Path`;
- an index file naming an `evidence_dir_local` that does NOT exist falls through
  and answers None — the discriminator that pins the `is_dir()` check;
- an index file carrying NO `job_id` key at all still resolves. THIS IS THE
  DISCRIMINATOR FOR THE WHOLE MOVE: it passes under the by-name read and fails
  under any re-expression through `find_record`, so say that in the test's own
  one-line docstring;
- a malformed index file — bytes that are not JSON — falls through to None
  rather than raising;
- the relative fallback: with the CWD at `tmp_path` and a real
  `remedy-job-evidence-<job_id>` directory created there, the function returns
  it; with no such directory it returns None;
- THE DELEGATION PROOF: `packages.orchestration.ui_server._resolve_evidence_dir`
  and `resolve_job_evidence_dir` answer the SAME value for the same job id, over
  a case that is NOT None. Reaching this one needs the default index dir, so
  point `resolve_data_root` at `tmp_path` by whatever mechanism the existing
  tests in this file already use for that, and do not invent a second one.

Extend the module docstring's property list with what you added, in the file's
existing style.

## The slices

<<<SLICE PLANF033R13
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 4 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | done | round 12 |
| one evidence-directory resolver for viewer and doors | open | this round |
| the CLI command and its handler | open | next |
| the write door's exposure and dispatch | open | after the CLI command |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. ONE evidence-directory resolver. `build_diff_view` takes a DIRECTORY, and
   `ui_server._resolve_evidence_dir` already decides which one the viewer reads.
   A second rule in `apps/cli/` could disagree with it, and a decision recorded
   over hunks nobody was shown is the harm `HUNK_RECORD_REFUSAL_NO_DIFF` exists
   to prevent. So the rule MOVES to `packages/orchestration/evidence_index.py`,
   which owns that index already, and `ui_server` delegates.
2. Then the CLI command and its handler TOGETHER: `apps/cli/grouped.py` builds
   its parsers from the catalog, so a handlerless entry is reachable in help and
   answers `Error: no handler`. It lands in the `patch` group, whose size and
   exact subcommand set `TestCatalogLookups.test_get_commands_for_group` in
   `tests/test_command_catalog.py` pins — widened in the SAME commit.
3. Then the write door. `UI_EXPOSED_COMMANDS` is a SUBSET of the catalog pinned
   at exactly two ids by `TestUiExposedCommands`, so exposure needs step 2 first.
   `DOOR_METHODS` and `ALLOWED_IMPORTS` are EQUALITY guards widened in the same
   commit as the dispatch, and `packages.orchestration.hunk_apply` joins
   `FORBIDDEN_MODULES` so DECISION F033 D4's forbidden mistake cannot be made
   silently later.
4. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report line derived from the ledger, and partial state rendered truthfully in
   viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard: a new import reddens the branch
  tip unless it is ruled in the same commit. R-0738 is T003's to repair.
<<<END PLANF033R13

<<<SLICE RECORDF033R13
Gate: F033 R12 — THE RECORDER LEARNS THE VIEWER'S ENVELOPE. THE ROUND PASSED. This entry books, under operator amendment amend0827-process-diet rule 1, the verdict the session-3 reviewer reached and committed to `.agent/handoff.md` at `d526dfb5`; it is written into this record by the first commit of the next round rather than by a round of its own, and every reading below is that reviewer's, taken at `c4ad00c4`. All eight gates were re-executed from scripts of its own and every ordered reading reproduced. TRANSPORT: the C0a blob measured 30167 bytes at sha256 `e15f5523…5fecf`, byte-identical to the reviewer's own pre-emission original, with ONE blob id `3bcfa06b` at C0b — a chain that walks the saved copy, its mirror and the working copy, which is what this workflow can measure and is not a claim about the emitted bytes. THE RECORD APPEND at `62760bac` reconstructed 1506343 plus one newline plus 6482 to 1512826, the committed blob exactly, base a byte PREFIX, N COUNTED at 2, the last two blank-line units equal to the slice's paragraphs IN ORDER, and THREE negative controls placed inside the FIRST appended paragraph — whose byte span the reviewer computed independently as 1506344 to 1511396, agreeing with the worker's — at its start, its middle and two bytes from its end, all three rejected by BOTH readers. THE LEDGER: registered 303 UNMOVED, `Done:` 47 lines over 45 distinct to 48 over 46 with the ADDED resolved id exactly `R-0742`, `Landed:` 15 UNMOVED with the `Landed: R-0742` line still standing beside its new `Done:` paragraph as this append-only record requires, `Gate:` 128 to 129 with `^Gate: F033 R11 — ` exactly 1, `DECISION F033 D` 4 UNMOVED, and the open set 258 to 257. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to its slice at 2713 bytes over 49 lines, under the 50-line cap AGENTS.md sets; `.agent/prose_slips.md` reconstructed 22079 plus one newline plus 927 to 23007. THE CODE AGAINST THE SPEC: `ruff` exited 0; the AST import set is twelve names, every one standard library or from `diff_parser`, `hunk_approval` or `hunk_ledger`, with `hunk_apply`, `source_apply`, `storage`, `subprocess` and `shutil` ALL ABSENT and `open(` and `save_job` both 0, so DECISION F033 D4 survives that round MEASURED rather than assumed; the two pre-existing constants are unchanged and `HUNK_RECORD_REFUSAL_NO_DIFF` reads `no_diff_available`; `record_hunk_decision`'s signature is BYTE-IDENTICAL to its signature at that round's base; and its extracted body is its docstring plus one `return record_hunk_decision_from_view(...)` call, holding none of `build_hunk_ledger`, `decide_hunk_approval`, `export_hunk_ledger` or `setdefault` — so "one implementation, two doors" is a measurement and not a claim. THE MUTATIONS were reproduced in the reviewer's own disposable worktree at `c4ad00c4`, the import first proved to resolve inside it, each anchor asserted UNIQUE and the module restored byte-identically after each: the UNMUTATED CONTROL is a real exit 0 at 15 passed against 9 at that round's base; skipping the availability refusal is exit 1 at 2 failed; defaulting `available` to False is exit 1 at 11 failed; checking truncation before availability is exit 1 at 1 failed; and writing the record even when the availability refusal fires is exit 1 at 2 failed. THE REVIEWER ALSO RAN A MUTATION THE BLOCK NEVER ORDERED — making the text door hand the view door an envelope marked unavailable — and it went RED at 10 failed, so the delegation itself is pinned and not merely written. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the recorder 15, the ledger 29, approval and apply 41 together, `test_diff_view_source.py` 15, `tests/ui_server/test_command_channel.py` 106 and the canary 42. THE STRUCTURE: seven single-parent commits over that round's range ending at its C5, of 407, 256, 29, 4, 4, 94 and 153 insertions, every one under 500, with the handback a further 340; the path set EQUALS the declared change set in BOTH directions; residue 0 in all four targets against a 5 and 6 control; `git ls-files .remedy-wt` 0; and ALL TWELVE do-not-touch paths byte-identical by blob id, so the claim that the write door and the catalog were untouched is a measurement. THE WORKER'S FLAG ABOUT THE PUSH TRANSCRIPT WAS EXAMINED AND IS NOT A FINDING: `docs/agents/handback_template.md` at `c4ad00c4` requires "command + outcome" under `## External actions` and never a transcript, and scopes `## Verification` to the gates the round's block ordered, which a push is not; nothing under `docs/` is wrong, so no id is spent and the wording was the handback's own choice. THE TWO REVIEWER PROSE SLIPS that round carried — a Bundle line reading "one dated line" over a slice carrying two dated paragraphs, and an AST import count that read eleven at R11 and twelve at R12 because `Mapping` was added for an annotation — damaged nothing on disk and are recorded in `.agent/prose_slips.md` under amend0827 rule 2, with no id and no correction round.
<<<END RECORDF033R13

<<<SLICE SLIPSF033R13
2026-08-29 · F033 R12 · The block's Bundle line for C3 read "one dated line into `.agent/prose_slips.md`" while its own SLIPSF033R12 slice carried TWO dated paragraphs and G5 ordered the count without fixing it; the worker applied both byte for byte under convention 1 and declared the disagreement, which is the required behaviour, and the R12 append reconstructs exactly.

2026-08-29 · F033 R12 · The round 11 verdict recorded the recorder's AST import set as eleven names and this round's is twelve, which reads as drift and is not: `Mapping` was added for the `attempt_view: Mapping[str, Any]` annotation, it is standard library, and the property the gate exists for — every entry stdlib or one of the three allowed modules, all five forbidden names absent — is unchanged.
<<<END SLIPSF033R13

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C5, so the handback at C6 can quote all of them; C6's own numbers are NOT
ordered here.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C6,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r13.md` and of `.remedy-wt/f033-r13-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r13.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1512826 bytes, plus one newline plus RECORDF033R13 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R13 — report
  it — and compare the LAST N blank-line units of the C2 blob against the
  slice's paragraphs IN ORDER. NEGATIVE CONTROL at a BYTE offset your script
  PROVES lies inside the FIRST appended paragraph, whose span you compute in
  BYTES per convention 10 and report; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and at C2 count `^- R-\d+ — ` with distinct
  ids, `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`,
  `^Gate: F\d+ R\d+ — ` and `^DECISION F033 D\d+ — `; report the open set at
  both. Ordered: registered 303 UNMOVED and `Done:` 48 lines over 46 distinct
  UNMOVED — this round registers nothing and resolves nothing; `Landed:` 15
  UNMOVED; `Gate:` 129 to 130 with `^Gate: F033 R12 — ` going 0 to exactly 1;
  `DECISION F033 D` 4 UNMOVED; and the open set 257 at BOTH.
- **G5 THE PROSE FILES.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R13 —
  report its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets. `.agent/prose_slips.md` at C3 is the BASE blob, which must be
  23007 bytes, plus one newline plus SLIPSF033R13, byte for byte, with BASE a
  byte PREFIX; report the count of lines matching
  `^2026-\d\d-\d\d · F033 R12 · ` at BASE, which must be 0, and at C3, and the
  count of lines beginning `- R-` in the whole file at C3, which must be 0.
- **G6 THE CODE AGAINST THE SPEC at C4.** (a) `ruff check` over
  `packages/orchestration/evidence_index.py`,
  `packages/orchestration/ui_server.py` and
  `tests/orchestration/test_evidence_index.py` exits 0 — report the summary line.
  (b) THE MOVE IS A MOVE: by AST extract `resolve_job_evidence_dir`'s body from
  the C4 blob of `evidence_index.py` and report it, and report the `except`
  clause's exception names, which must be exactly `ImportError`, `OSError`,
  `ValueError`, `KeyError` in that order; report that the text
  `remedy-job-evidence-` occurs in it, and that the names `find_record` and
  `load_index_records` do NOT. (c) THE DELEGATION: by AST extract
  `_resolve_evidence_dir`'s body from the C4 blob of `ui_server.py` and report
  it; it must contain a call to `resolve_job_evidence_dir` and must NOT contain
  the names `json`, `resolve_data_root`, `evidence_dir_local` or
  `remedy-job-evidence-`. Report its extracted signature, which must be
  byte-identical to its signature at BASE. (d) `git show --numstat C4 --
  packages/orchestration/ui_server.py` — report both columns; nothing outside
  that one function may move. (e) Run BOTH functions directly, not through the
  tests, in a `tempfile.TemporaryDirectory` with the CWD moved into it, over a
  hand-written index file naming a directory that exists, and report that the
  two return the SAME value and that it is not None.
- **G7 THE MUTATION RED-PROOFS at C5.** In a DISPOSABLE `git worktree` at C5,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy. FIRST the UNMUTATED CONTROL over
  `tests/orchestration/test_evidence_index.py` — REAL exit 0, report the count,
  which must exceed the 25 BASE gives. Then, one at a time, reverting fully
  between each, asserting the anchor is UNIQUE inside the named FILE before
  replacing it, and reporting the REAL exit code, the failure count and the NAME
  of each failing test:
  (i) in `packages/orchestration/evidence_index.py`, drop the `is_dir()` check on
      the index branch so a named-but-absent directory is returned anyway;
  (ii) in `packages/orchestration/evidence_index.py`, make the index branch
      additionally require the record's `job_id` key to equal `job_id` — the
      `find_record` re-expression this round refuses;
  (iii) in `packages/orchestration/ui_server.py`, make `_resolve_evidence_dir`
      return None unconditionally.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/orchestration/test_evidence_index.py`,
  `tests/orchestration/test_final_audit_evidence.py` (37 at BASE),
  `tests/ui_server/test_diff_endpoint.py` (8 at BASE),
  `tests/orchestration/test_hunk_decision_record.py` (15 at BASE),
  `tests/test_command_catalog.py` (18 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C5`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. Report the range's path set against
  the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/evidence_index.py`,
  `packages/orchestration/ui_server.py` and
  `tests/orchestration/test_evidence_index.py`: each 0, against
  `.agent/authored/f033-r13.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C5, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 4,
round 13, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Write external actions as command plus outcome. Quote
`resolve_job_evidence_dir`'s final signature and its extracted body from G6(b),
`_resolve_evidence_dir`'s extracted body from G6(c), and the test names you wrote
with the property each pins.

Carry SESSION 4 forward and name the next session's first actions in this order:
read `.agent/STOP` from disk, then run the Open PR Gate, then book this round's
verdict, then the plan's step 2. No length cap. Write no verdict on your own work.
