STEP T001 — F037 Rendered diff viewer — ROUND 14

Goal: close the remaining half of `R-0721`. Both parser ceilings bound what
F037 BUILDS; neither bounds what it READS.
`packages/orchestration/diff_view_source.py` still calls
`artifact.read_text(encoding="utf-8")` on `workspace.diff` before the parser is
ever entered, so the whole artifact is in memory whatever its size — and a diff
of one enormous line reaches neither ceiling and still costs the read. This
round bounds the read, folds that truncation into the envelope's existing
`truncated` flag, and proves the cut never hands the parser a partial line or a
split character.

Base: the round starts from `922f3223` on branch
`feature/f037-rendered-diff-viewer`. Nothing else is in flight.

Bundle, one commit each, in this order:
- C0a save this block verbatim to `.agent/authored/f037-r14.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 apply PLANF037R14 to `.agent/plan.md`
- C2 append GATER13 to `.agent/live_review.md`
- C3 append DECISION7 to `.agent/decisions.md` and write SPEC S1 through S4 into
  `packages/orchestration/diff_view_source.py`
- C4 write SPEC S5 through S11 into
  `tests/orchestration/test_diff_view_source.py`
- C5 append DONE0721B to `.agent/live_review.md`
- C6 rewrite `.agent/handoff.md` as the handback

Change set, and nothing outside it: `.agent/authored/f037-r14.md`,
`.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/handoff.md`,
`packages/orchestration/diff_view_source.py`,
`tests/orchestration/test_diff_view_source.py`. Push the branch after C6.
Create no PR, merge nothing.

Constraints:
1. A slice between the markers is applied BYTE FOR BYTE. Never edit a slice,
   never reflow it, never fix a typo in it. If a slice looks wrong, apply it and
   say so in the handback's Deviations.
2. Production code and test code are DESCRIBED by the SPEC below, not sliced.
   Write them yourself, in this repository's idiom — this test module annotates
   its tests `(tmp_path: Path) -> None` and builds every tree under `tmp_path` —
   and report every place your reading of the SPEC differed from what you wrote.
3. `packages/orchestration/diff_parser.py` and
   `tests/orchestration/test_diff_parser.py` are NOT touched. The two ceilings
   DECISION F037 D5 and D6 set stay exactly as they are at `922f3223`; this
   round bounds a different resource in a different module, and keeping them
   apart is what lets the red-proofs say which bound they proved.
4. `packages/orchestration/ui_server.py` is NOT touched. It already copies the
   envelope's `truncated` through, so the endpoint needs no change; say so in
   the handback rather than editing it.
5. Nothing under `apps/` or `docs/` is touched.
6. Every existing test in `tests/orchestration/test_diff_view_source.py` as it
   stands at `922f3223` is left byte-identical. This round only appends.
7. Ruff runs under this repository's own configuration — line length 120, rules
   `E`, `F`, `W`, `I`, `UP`. Never `--isolated`.
8. Every destructive check runs inside a disposable `git worktree` under
   `.remedy-wt/`, never in the primary checkout, which reads
   `git status --porcelain` empty after every commit.
9. C5 runs after C3 and C4. DONE0721B states what this round landed, so the
   commit order is what makes it true.
10. The value in SPEC S1 and the figures quoted with it are the reviewer's
    measurements. Do not re-derive them; if a measurement of yours disagrees,
    report the disagreement and apply the SPEC.

SPEC — `packages/orchestration/diff_view_source.py`

S1. A module-level constant `DIFF_VIEW_MAX_ARTIFACT_BYTES = 8_000_000`, placed
    with the other module constants, above `SAFE_TASK_RUN_ID_RE`. Its comment
    block states: it is the ceiling on BYTES read from a diff artifact; DECISION
    F037 D7 fixes it; and WHY this bound is not made redundant by the parser's
    two ceilings — those bound the view that is BUILT, and a diff of one
    enormous line with no newline reaches NEITHER of them while still costing
    the whole read. Record the reviewer's measurement beside it: a diff that
    saturates BOTH parser ceilings at once is 1,423,907 bytes of input —
    397,907 for `DIFF_VIEW_MAX_BODY_LINES` body lines in one file and 1,026,000
    for `DIFF_VIEW_MAX_FILES` one-pair files at paths of sixty characters and
    more — so this ceiling is over five times the input any diff needs before
    the parser's own bounds take over.

S2. The read in `build_diff_view` becomes bounded. Keep the existing
    `if artifact.is_file():` guard, the existing `except (OSError,
    UnicodeDecodeError): diff_text = None` handler and the existing
    `if diff_text is None:` absence branch exactly as they are — a file that
    cannot be read or decoded still arrives as `DIFF_REASON_ARTIFACT_MISSING`
    and nothing about that path changes. Inside the `try`, replace
    `artifact.read_text(encoding="utf-8")` with: open the artifact in BINARY
    mode and read `DIFF_VIEW_MAX_ARTIFACT_BYTES + 1` bytes; if what came back is
    LONGER than `DIFF_VIEW_MAX_ARTIFACT_BYTES`, set a local `read_truncated`
    True, cut the bytes to `DIFF_VIEW_MAX_ARTIFACT_BYTES`, and then cut them
    again to end at the LAST newline they contain — `raw[: raw.rfind(b"\n") + 1]`
    is the expression, and it yields the empty bytes when there is no newline at
    all. Then decode as UTF-8. `read_truncated` starts False.

S3. The WHY comment above that cut carries three facts. FIRST, reading one byte
    MORE than the ceiling is how "larger than the ceiling" is distinguished from
    "exactly the ceiling" in one read, and exactly the ceiling is NOT truncated —
    the same inclusive boundary the parser's two ceilings have. SECOND, the cut
    back to the last newline is what keeps the parser from being handed a
    partial line, and it is also what keeps a multi-byte character from being
    split across the boundary, since a newline is never inside one — without it
    a cut mid-character raises `UnicodeDecodeError` and a readable artifact
    would be reported as missing. THIRD, an artifact whose first
    `DIFF_VIEW_MAX_ARTIFACT_BYTES` bytes hold no newline yields the empty text,
    which parses to the empty-files shape and is reported as available and
    truncated: that is the one enormous line, and saying so in the data is this
    module's whole design.

S4. The envelope's `truncated` becomes `parsed["truncated"] or read_truncated`,
    so a truncation from EITHER source reaches the caller. `build_diff_view`'s
    docstring gains one sentence naming the read ceiling and saying that
    `truncated` is True when the read cut the artifact, when the parser hit one
    of its own two ceilings, or when the artifact carried an upstream truncation
    sentinel.

SPEC — `tests/orchestration/test_diff_view_source.py`

S5. A helper that writes a job-scope evidence tree whose `workspace.diff` is
    given text, returning the evidence directory — the existing
    `_write_evidence_tree` builds a fixed pair and is not what these tests need.
    Do not modify it; add the new helper beside it.

S6. `test_an_artifact_above_the_read_ceiling_is_cut_and_the_envelope_says_so`,
    at the REAL constant and monkeypatching nothing. Write a `workspace.diff`
    of a single file whose body lines carry more than
    `DIFF_VIEW_MAX_ARTIFACT_BYTES` bytes in total, parse it, and assert
    `available` True, `truncated` True, and that at least one file came back —
    a bound that returned nothing would satisfy a truncation assertion alone.
    Its docstring records what this test costs and why it is worth it: it is the
    only test here that exercises the real ceiling, and the parser stops at its
    own body-line ceiling early in that text, so the cost is the read and the
    split rather than a full parse of eight megabytes.

S7. The remaining shape tests run against a SMALL ceiling, set with
    `monkeypatch.setattr` on the module attribute
    `DIFF_VIEW_MAX_ARTIFACT_BYTES`, because a boundary is a property of the
    comparison and not of the value, and a fixture per test at the real value
    would cost tens of megabytes of writes to prove the same thing. State that
    in a comment where the small ceiling is introduced.

S8. `test_the_read_ceiling_boundary_holds_on_both_of_its_sides`. Under a small
    ceiling: an artifact of EXACTLY the ceiling's bytes is available and NOT
    truncated, and one of exactly one byte more IS truncated. Both halves in one
    test, for the reason the parser's two boundary tests already state — each
    half alone is satisfiable by a bound one off in either direction.

S9. `test_the_cut_never_hands_the_parser_a_partial_line`. Under a small ceiling,
    an artifact whose cut would land in the MIDDLE of a body line. Assert that
    every `content` the view carries equals the corresponding whole generated
    line, so no half line reached the contract. Assert `truncated` True beside
    it, so the test cannot pass by the cut never having happened.

S10. `test_the_cut_never_splits_a_multi_byte_character`. Under a small ceiling,
    an artifact whose body lines carry multi-byte UTF-8 characters and whose cut
    point falls INSIDE one of them — choose the ceiling so that it does, and
    assert in the test that the byte at the ceiling is a UTF-8 continuation
    byte, so the fixture cannot silently stop exercising the case. Assert
    `available` True and `reason` None: without the newline cut this artifact
    raises `UnicodeDecodeError` and comes back as
    `DIFF_REASON_ARTIFACT_MISSING`, which is a readable diff reported as absent.

S11. `test_one_enormous_line_is_bounded_though_it_reaches_neither_parser_ceiling`
    and `test_the_parsers_own_truncation_still_reaches_the_envelope`. The first,
    under a small ceiling, writes an artifact that is one single line with no
    newline anywhere and asserts `available` True, `truncated` True and `files`
    empty — the shape that motivates this bound, since it appends nothing to
    either parser counter. The second writes an artifact SMALLER than the
    ceiling that carries the upstream `[DIFF TRUNCATED]` sentinel, and asserts
    `truncated` True with the read having done nothing: it is the discriminator
    that the envelope's flag is an OR over both sources rather than a
    replacement of one by the other.

Slice convention: each authored text sits between a line beginning `<<<SLICE `
and a line beginning `<<<END `, both carrying the slice's name. The marker lines
are NEVER written into any target file. The slices are PLANF037R14, GATER13,
DECISION7 and DONE0721B.

<<<SLICE PLANF037R14
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D7.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R14 closes the remaining half of `R-0721`. DECISION F037 D5 and D6 bound what
the parser BUILDS; neither bounds what `diff_view_source.py` READS, and a diff
of one enormous line with no newline reaches neither ceiling while still costing
the whole read. The read is bounded at `DIFF_VIEW_MAX_ARTIFACT_BYTES`, cut back
to the last newline so no partial line and no split character reaches the
parser, and the envelope's `truncated` becomes an OR over both sources.
DECISION F037 D7 records the value and how to reverse it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R13 verdict | ordered | record first |
| C3 DECISION F037 D7 and the read bound | ordered | the choice beside what it governs |
| C4 the read-bound tests | ordered | both sides, and the two cut hazards |
| C5 the resolution | ordered | written after the repair is proved |
| C6 the handback | ordered | |

## Next Steps
1. T002 is NOT blocked by the refused runner and the round after this one says
   so in a DECISION and starts the rendering core. `apps/ui/vitest.config.ts`
   collects `src/**/*.test.ts` in a node environment,
   `tests/orchestration/test_test_runner.py` runs `npx vitest run` from pytest
   and is exit 0 here at `922f3223`, and `tests/ui_contracts/` pins the markup
   vitest never renders. Logic goes in `apps/ui/src/api/`, where vitest reaches
   it; markup is pinned from pytest.
2. T003 — sidebar, virtual scrolling, lazy language bundles, the L3 tab —
   follows the rendering core and is the feature's last slice.

## Risks
- The feature is at round 14 against a soft limit of 25, with T002 and T003 both
  still to build. If the rendering core does not start within two rounds, the
  next handback carries a scope report rather than another step.
- The binding CSS defines no intraline treatment while Acceptance requires it,
  so that stays a question for the round that renders spans.
<<<END PLANF037R14

<<<SLICE GATER13
Gate: F037 R13 — the round that closed `R-0722`, the second dimension of the parser's bound. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all of the load-bearing ones itself at `922f3223`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING, which is the strongest link this workflow can offer: the block was written to the gitignored scratch `.remedy-wt/f037-r13-block.md` before the worker existed and measured there at sha256 `39a60cc6aa9423c9b7bfa3ed76e4e00b9597706efed9a0ccd8e6e79aac161260` over 34679 bytes and 439 lines, and the committed `.agent/authored/f037-r13.md` is byte-identical to that original, with the saved copy and `.agent/last_block.md` ONE git blob `2f9c30ae910007b4e7301b72d361ca347a3202b3`. EXTRACTION REPRODUCES THE ARITHMETIC: slices at 49, 1, 1, 9, 79 and 1 content lines, CONTENT 140 against TOTAL 439, PROSE 299, both caps holding. THE PLAN IS BYTE-EQUAL to PLANF037R13 with the trailing-newline negative control False, at 49 lines with one `## Goal` and one `## Next Steps` — under the AGENTS.md fifty-line rule by one line, which is where the reviewer's own last trim put it. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED, recomputed mechanically: `^- R-\d+ — ` 282 to 283 with every id distinct, `^Done: R-\d+ — ` 30 to 31, `^Landed: R-` unmoved at 1, `^Gate: F\d+ R\d+ — ` 82 to 83, and the OPEN SET UNMOVED at 252 because `R-0722` was registered and resolved in the same round, which is the shape §4 item 4 prescribes rather than an anomaly. Each of the three append-only files is a byte PREFIX of its result — `.agent/live_review.md` 1200063 to 1209025, `.agent/decisions.md` 663863 to 668900, `.agent/prose_slips.md` 10681 to 11331 — so nothing landed was rewritten. `.agent/decisions.md` carries 172 `## DECISION ` headings and `F037 D6` exactly once. THE CODE MATCHES THE SPEC AND THE REVIEWER READ THE CODE RATHER THAN THE SUMMARY: the cut sits directly after `_collapse_doubled_header_regions`, uses `>` so exactly the ceiling parses in full, and the reviewer checked the one thing that could have made the file-ceiling tests measure nothing — `_region_is_redundant_header_echo` returns False when either header is None, so the mode-change fixtures, which carry no header pair at all, are never folded and the entry counts those tests assert are real. THE SUITES AND THE LINT ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER: `python3 -m pytest tests/orchestration/test_diff_parser.py -q` exit 0 at `43 passed in 2.32s` against the base `37 passed in 2.14s`; `python3 -m pytest tests/orchestration/test_diff_view_source.py tests/ui_server/test_diff_endpoint.py tests/cli/test_golden_path.py -q` exit 0 at `57 passed`, which holds the canary's 42 and the base's 15 unmoved; and `python3 -m ruff check` over both changed files exit 0 at `All checks passed!`. ALL FIVE RED-PROOFS REPRODUCE EXACTLY, run by the reviewer in a disposable worktree at `922f3223` with `python3 -B`, each replaced string counted at exactly 1 before its edit and the module restored and re-hashed to `b66d3164b74a23c3d5fe1b7fdef8496f079fd0002a2c2c5d68a435fd56b56027` after every run: unmutated control exit 0 at `43 passed`; deleting the cut exit 1 at `5 failed, 38 passed`; `>` to `>=` exit 1 at `1 failed, 42 passed` killing exactly the boundary test; the cut moved ABOVE the collapse exit 1 at `1 failed, 42 passed` killing exactly the doubled-header test, which is the discriminator for its placement; raising `DIFF_VIEW_MAX_FILES` tenfold exit 1 at `2 failed, 41 passed`. THE FIFTH IS THE ONE THIS ROUND EXISTED FOR AND IT TURNED OVER: raising `DIFF_VIEW_MAX_BODY_LINES` tenfold was exit 0 at `43 passed` in the reviewer's own measurement at `327c1333`, and at `922f3223` it is exit 1 at `3 failed, 40 passed` with the payload-budget test among the failures. THE STRUCTURE IS CLEAN: the path residue is empty in both directions, `docs/` and `apps/` are untouched, `packages/` holds only `diff_parser.py`, every commit is single-parent and under 500 insertions, and the marker sweep is 0 in all four targets against 6 in the block blob as its control. THE ELEVEN DECLARED DEVIATIONS ARE ALL HONEST and two are worth recording: the worker measured the file-dimension payload at 1.233 MB where the SPEC states 1.269 MB, because its long-path template is shorter than the reviewer's, and it applied the SPEC value and reported the disagreement rather than quietly correcting either; and it added an assertion of its own that the re-based fixture's file count is strictly below `DIFF_VIEW_MAX_FILES`, which is the discriminator the block described in prose and did not order. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER13

<<<SLICE DECISION7
## DECISION F037 D7 — the diff artifact is read under a byte ceiling, and `truncated` becomes an OR over every source of it

**Date:** 2026-08-28 · **Round:** F037 R14 · **Finding:** `R-0721`

**The choice.** `packages/orchestration/diff_view_source.py` gains a module
constant `DIFF_VIEW_MAX_ARTIFACT_BYTES = 8_000_000` and reads the diff artifact
in binary under that ceiling instead of calling
`artifact.read_text(encoding="utf-8")` on it whole. When the artifact is larger,
the bytes are cut to the ceiling and then cut back to the last newline they
contain, and the envelope's `truncated` becomes `parsed["truncated"] or
read_truncated`.

**Why a read bound is not made redundant by the two parser ceilings.** DECISION
F037 D5 bounds the body lines the view carries and D6 the file entries, and both
bound what is BUILT. The read happens first and is unbounded by either: a
`workspace.diff` of one enormous minified line appends nothing to the body
counter and adds one file entry, so it passes both ceilings untouched and still
costs the entire read. The layering is deliberate — this bound is on INPUT
BYTES, those are on OUTPUT OBJECTS, and neither can be expressed in the other's
unit.

**Why 8,000,000 bytes.** Measured by the reviewer at `922f3223`, a diff that
saturates BOTH parser ceilings at once is 1,423,907 bytes of input: 397,907 for
`DIFF_VIEW_MAX_BODY_LINES` body lines in a single file, and 1,026,000 for
`DIFF_VIEW_MAX_FILES` one-pair files at paths of sixty characters and more. The
ceiling is over five times that, so for any realistic line length the parser's
own bounds take over long before this one does, and this one is what stops the
pathological shapes those bounds cannot see. A diff whose body lines are
hundreds of characters wide can reach it first; that is a real cut, it is
reported in the data, and it is the point of having a byte bound at all.

**Why the cut goes back to the last newline.** Two hazards share one fix. A cut
at an arbitrary byte can land inside a multi-byte UTF-8 character, and the
decode then raises — which this module's existing handler would report as
`DIFF_REASON_ARTIFACT_MISSING`, turning a readable diff into an absent one. A
cut can also land in the middle of a body line, which would put half a line into
the contract as if it were whole. A newline is never inside a multi-byte
character and never inside a line, so cutting back to the last one answers both.
When the ceiling's worth of bytes holds no newline at all the result is the
empty text, which parses to the empty-files shape and is reported as available
and truncated: for one enormous line that is the honest answer, and it is the
same answer this module already gives for every other absence — name it in the
data rather than raise.

**Why the flag is an OR and not a replacement.** `truncated` now has three
sources: the upstream `[DIFF TRUNCATED]` sentinel some other producer wrote,
the parser's own two ceilings, and this read. They are independent and any of
them makes the view a prefix, so the envelope reports their disjunction. A test
whose artifact carries the sentinel while staying under the read ceiling is the
discriminator, because a replacement rather than an OR would drop it.

**What the endpoint needs.** Nothing. `packages/orchestration/ui_server.py`
builds its diff JSON by returning `build_diff_view`'s envelope, so the flag
reaches the client already; this decision changes what sets it, not what carries
it.

**Alternatives rejected.** (1) Check `artifact.stat().st_size` and refuse above
the ceiling — rejected because a refusal is exactly what this module's docstring
forbids: a viewer that shows the first part of a large job's diff is better than
one that shows nothing, and the contract already has the field for saying which
it did. (2) Cut at the ceiling with `errors="replace"` instead of at a newline —
rejected because it puts a replacement character into a line's content, which is
data the viewer would render as if the artifact contained it. (3) Stream the
artifact and parse incrementally — the honest long-term answer, rejected for
this round as a rewrite of a module that is total and pure by contract, and it
buys nothing the two ceilings and this bound do not already buy. (4) Derive the
byte ceiling from the two parser ceilings rather than stating it — rejected
because line length is not bounded by either of them, so no such derivation
exists.

**How to reverse.** Delete `DIFF_VIEW_MAX_ARTIFACT_BYTES` and restore the single
`artifact.read_text(encoding="utf-8")` call in `build_diff_view`, restore
`view["truncated"] = parsed["truncated"]`, and delete the tests F037 R14 added
in the final section of `tests/orchestration/test_diff_view_source.py`.
DECISION F037 D5 and D6 are untouched by this decision and survive its reversal.
<<<END DECISION7

<<<SLICE DONE0721B
Done: R-0721 — THE REMAINDER RESOLVED at F037 R14 by the round's C3 and C4, in the commit order constraint 9 of the R14 block fixes. This is the SECOND resolution paragraph for this id and it is deliberate: F037 R12 resolved the finding IN PART, and a partial resolution is invisible to the open-set arithmetic the pre-emission checklist runs — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — so the remaining half survived in prose only, which is recorded as a reviewer slip in `.agent/prose_slips.md` and is closed here rather than left to a reader to reconstruct. WHAT WAS STILL OPEN: `packages/orchestration/diff_view_source.py` read the artifact whole with `artifact.read_text(encoding="utf-8")` before `parse_unified_diff_to_view` was ever entered, so the two ceilings DECISION F037 D5 and D6 set bounded the view that was BUILT while the INPUT stayed unbounded — and a diff of one enormous line with no newline reaches neither of those ceilings and still costs the entire read. WHAT LANDED: the artifact is read in binary under `DIFF_VIEW_MAX_ARTIFACT_BYTES`, cut to that ceiling and then cut back to the last newline, and the envelope's `truncated` became an OR over the read, the parser's own ceilings and the upstream sentinel. DECISION F037 D7 records the value against the reviewer's measurement that a diff saturating both parser ceilings at once is 1,423,907 bytes of input, why the cut goes back to a newline rather than to an arbitrary byte, and how to reverse the whole thing. THE TWO CUT HAZARDS ARE PROVED RATHER THAN ARGUED, because they are the half of this repair that fails silently in opposite directions: a cut inside a multi-byte character would raise and be reported as `DIFF_REASON_ARTIFACT_MISSING`, turning a readable diff into an absent one, and a cut inside a body line would put half a line into the contract as if it were whole — each has a test whose fixture is built so the cut point lands exactly there. WHAT THIS RESOLUTION DOES NOT CLAIM: nothing here bounds the SERIALIZED response the endpoint writes, which is bounded only through the two parser ceilings and the payload budget F037 R13 recorded; and the read is bounded rather than streamed, so the ceiling's worth of bytes is still held in memory at once, which DECISION F037 D7 states as the alternative it rejected for this round.
<<<END DONE0721B

Done when — the gates below, every one executed with its REAL exit code
recorded, one line per gate in the handback. G1 through G8 run at the commits
named; none of them runs after C6, so the handback can quote every one of them.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again before C6 and
report both readings. Report `git rev-parse HEAD` before C0a and state whether
it equals `922f3223`, `git branch --show-current`, and the `git status
--porcelain` line count after each of C0a through C5.

G2 TRANSPORT, ONE DIGEST COMPARISON. Report sha256, byte count and line count of
the committed `.agent/authored/f037-r14.md` blob, and state whether they equal
the reviewer's scratch original at `.remedy-wt/f037-r14-block.md` — compare the
two files directly, disk to disk. Report `git rev-parse <C0b>:.agent/authored/f037-r14.md`
and `git rev-parse <C0b>:.agent/last_block.md` and whether they are the same
blob. State what the chain covers and what it does not.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob and never on the
prose. For each slice report its content line count; report TOTAL lines of the
blob, CONTENT as their sum, PROSE as TOTAL minus CONTENT, and whether TOTAL is
at most 490 and PROSE at most 400.

G4 THE PLAN AT C1. Report whether `.agent/plan.md` is byte-equal to the
PLANF037R14 slice extracted from the committed C0a blob, including the trailing
newline, plus the negative control against that slice minus its trailing
newline. Report the count of lines exactly `## Goal` and exactly `## Next
Steps`, and `wc -l` with whether it is strictly under 50.

G5 THE RECORD AT C2 AND C5. For each of the three appends — GATER13 into
`.agent/live_review.md`, DECISION7 into `.agent/decisions.md`, DONE0721B into
`.agent/live_review.md` — report reader (a), `result == before + b"\n" + slice`
re-read from disk; reader (b), which COUNTS the blank-line-separated units of
the slice and compares the LAST that many units of the file against them IN
ORDER, reporting the count it measured; and a negative control for both readers
that flips one byte inside the FIRST appended paragraph. Report whether each
file's pre-round blob is a byte PREFIX of the result, reading that blob with
`git show 922f3223:<path>` into memory and never over the tracked file. Then
report, line-anchored over `.agent/live_review.md` after C5 with the base figure
beside each: `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: F\d+ R\d+
— `, the open-set size, and whether every REGISTERED id is distinct. The
resolution lines are NOT expected to be distinct this round: report the number
of `^Done: R-\d+ — ` lines and the number of distinct ids among them, and name
the id that repeats — DONE0721B is a second resolution paragraph for `R-0721` by
design, and constraint 1 forbids repairing that by editing either paragraph.
Over `.agent/decisions.md`, report `^## DECISION ` and the count of `F037 D7`.

G6 THE RED-PROOFS OF THE READ BOUND. All runs inside a disposable worktree at
the C4 tree, never in the primary checkout, with `__pycache__` purged and
`python3 -B` for every run, the module restored between runs and each restore
verified byte-identical by sha256 against the unmutated C4 blob. Report the
UNMUTATED CONTROL's exit code and summary line first. Then, for each mutation,
report the occurrences of the replaced string BEFORE the edit — which must be
1 — the REAL exit code, the summary line, and the node ids that fail. The
ordered property is the COLOUR: report the names and counts you measure rather
than any this block predicts.
(a) Restore the unbounded read: replace the bounded read with
`artifact.read_text(encoding="utf-8")` and drop `read_truncated` from the flag.
Expect RED.
(b) Change the ceiling comparison so that exactly the ceiling counts as
truncated. Expect RED.
(c) Drop the cut back to the last newline, keeping the cut at the ceiling.
Expect RED.
(d) Replace `parsed["truncated"] or read_truncated` with `parsed["truncated"]`.
Expect RED.
(e) Replace it with `read_truncated` alone. Expect RED.

G7 SUITE, LINT AND CANARY AT C4. One pytest process at a time; never two at
once. Report the REAL exit code and the full summary line of each:
`python3 -m pytest tests/orchestration/test_diff_view_source.py -q`, whose base
figure at `922f3223` is `9 passed in 0.21s`;
`python3 -m pytest tests/orchestration/test_diff_parser.py
tests/ui_server/test_diff_endpoint.py -q`, whose base figure is `49 passed` and
which must be unmoved because constraints 3 and 4 forbid touching either side of
it; `python3 -m ruff check packages/orchestration/diff_view_source.py
tests/orchestration/test_diff_view_source.py` under this repository's own
configuration; and the canary `python3 -m pytest tests/cli/test_golden_path.py
-q`, whose base figure is `42 passed`. Report the view-source suite's `in <n>s`
figure and, since S6 writes an artifact of more than eight megabytes, name the
tests that account for the difference from the base rather than treating a rise
as a defect.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C5. Report `git diff
--name-only 922f3223..<C5>` and both residues against the change set above —
actual minus expected and expected minus actual, with `.agent/handoff.md`
expected to be the only member of the second because C6 writes it. Report
`git diff --stat` restricted to `docs/`, to `apps/`, and to `packages/`; the
third must hold `packages/orchestration/diff_view_source.py` and nothing else,
which is what proves constraints 3 and 4. Report each commit's insertion count
from `git show --numstat` for C0a through C5 and whether each is under 500, and
check those figures cell by cell against the `+/-` column of the handback's own
`## Commits` table. Report the count of lines matching `^<<<SLICE ` and
`^<<<END ` in `.agent/plan.md`, `.agent/live_review.md`,
`packages/orchestration/diff_view_source.py` and
`tests/orchestration/test_diff_view_source.py`, and the same counts over the C0a
blob as the control that the counter is not blind. Report
`git ls-files .remedy-wt` line count. Run `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` verbatim and report its exit code and
stdout.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER of this feature — session 4 — the round, the range
`922f3223..<C6>`, a per-commit changed-files table with the `+/-` column, one
line per gate G1 through G8 with its real result, the authored-text proofs, the
deviations, the item-status table covering C0a through C6 and G1 through G8 and
`R-0721`, and the next expected action. Derive any cap it must respect from
AGENTS.md yourself; this block states none. Then push the branch.
