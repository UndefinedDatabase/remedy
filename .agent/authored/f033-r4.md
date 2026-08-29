# F033 — Hunk-level diff approval · ROUND 4 · THE CLIENT SEAM

SESSION 1 of feature F033. Round 4, rounds so far 4.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R4`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE TYPESCRIPT IS A SPEC, NOT A SLICE. You write it from the description.
   Names and behaviours the SPEC fixes are binding; structure and wording are
   yours. If the SPEC is impossible, STOP and say so rather than inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Invoke `npx` through Python's
   `subprocess.run`, never through `npm run`. Python 3.10 forbids a backslash
   inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.

## Base

BASE is `51e04c89`, the round 3 handback commit, on branch
`feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD` before C0a and
STOP if it differs.

## Why this round exists

Round 3 made the server's hunk ids content-derived and bumped
`DIFF_VIEW_VERSION` to 2. The client did NOT go red, and that is the problem
rather than the reassurance: `apps/ui/src/api/diffViewModel.test.ts` builds its
own payloads, so its `version` and `id` expectations describe a FIXTURE and never
the server. The client is a v1-shaped consumer being handed v2 data with no test
covering the difference.

Underneath that sits a real defect. `apps/ui/src/api/diffViewModel.ts` reads

    id: rawId !== "" ? rawId : `${fileIndex}:${hunkIndex}`,

so when a payload carries no usable id the CLIENT INVENTS a positional one. Under
version 1 that was harmless, because positional was the real shape. Under version
2 it manufactures a string that sits in the same field as a content id, is
indistinguishable from one to every consumer downstream, and can never match
anything the server would recognise — so an approval keyed on it fails silently
rather than loudly. DECISION F033 D2, in the record slice below, rules it.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 3 verdict and DECISION F033 D2 into `.agent/live_review.md`
- C3 the client model and its tests, together
- C4 the handback

## Change set — these paths and nothing else

    .agent/authored/f033-r4.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    apps/ui/src/api/diffViewModel.ts
    apps/ui/src/api/diffViewModel.test.ts
    .agent/handoff.md

This round does NOT touch `packages/orchestration/diff_parser.py`,
`packages/orchestration/hunk_identity.py`,
`apps/ui/src/components/diff/DiffView.tsx`, or `docs/roadmap/STATUS.md`.

## SPEC — `apps/ui/src/api/diffViewModel.ts`

### 1. A reserved prefix, exported

Add an exported constant naming the prefix the client puts on an id it had to
invent. Name it `UNIDENTIFIED_HUNK_ID_PREFIX` and give it the value
`"unidentified:"`. A one-line WHY comment sits directly above it: a server hunk
id is sixteen lowercase hex characters, so a prefixed string cannot be mistaken
for one by any consumer, which is the whole point of the prefix.

### 2. The fallback stops manufacturing a plausible id

The expression that today reads
``id: rawId !== "" ? rawId : `${fileIndex}:${hunkIndex}` `` keeps its shape and
its purpose — every hunk still gets a DISTINCT non-empty id, because
`defaultCollapsedHunkIds` and `toggleHunkCollapse` key a `Set<string>` on it and
two hunks sharing an id would collapse and expand as one — but the invented value
now carries `UNIDENTIFIED_HUNK_ID_PREFIX` ahead of the position. The positional
part stays: it is what makes the invented ids distinct from each other.

A real id arriving from the server passes through UNTOUCHED. Do not validate it,
do not reformat it, do not check its length: the client is not the authority on
what a server id looks like, and a client that rejects ids it does not recognise
would break the next version bump for no gain.

### 3. What must NOT change

`readDiffEnvelope` NEVER throws, however broken the payload — the file's existing
test says so and it stays true. No other field of the envelope moves, no
signature changes, and nothing outside these two functions is edited.

## SPEC — `apps/ui/src/api/diffViewModel.test.ts`

- The test currently named `gives a hunk with no usable id the position the
  parser would have given it` asserts `"0:0"`. Its NAME states the contract this
  round replaces. Rewrite it to the new contract — an id-less hunk gets an id
  carrying `UNIDENTIFIED_HUNK_ID_PREFIX` — and rename it to say that.
- ADD: two id-less hunks in ONE file get DISTINCT ids, so the collapse set still
  treats them as two hunks. This is the property the positional suffix exists for
  and nothing currently pins it.
- ADD: a well-formed server id passes through UNCHANGED — use a realistic
  sixteen-character lowercase hex id and assert the envelope carries exactly it,
  with no prefix added.
- The fixture payload builders assert `version` 1 and a hunk id `"0:0"`. Those
  are v1 shapes. Move the fixtures to v2: `version` 2 and a sixteen-hex id.
  Report in the handback which fixture values you chose. Keep every other
  assertion in those tests exactly as it is — the snake/camel equivalence, the
  stats, the line counts, the `oldStart`, and the never-throws test.

## The slices

<<<SLICE PLANF033R4
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 1 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| restart, claim, register R-0738 | done | round 1, DECISION F033 D1 |
| the shared identity function and its tests | done | round 2, 10 tests |
| wire the parser, bump DIFF_VIEW_VERSION to 2 | done | round 3, 50 tests |
| rule the client's invented id | done | this round, DECISION F033 D2 |
| retire the diff-repair local hunk helper | open | next round, T001's last item |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Retire the local hunk helper in `packages/orchestration/diff_repair.py` onto
   `hunk_identity`, keeping `tests/orchestration/test_diff_repair.py` green.
   That closes T001.
2. Then T002: the `approve_hunks` command, its validation, and the
   all-or-nothing subset apply built on
   `packages/orchestration/source_apply.py`.
3. `packages/orchestration/repo_applicator.py` applies nothing by design, so the
   subset seam is new work rather than a parameter on something existing.

## Risks
- The diff endpoint added by F256 serves this envelope, so a shape change is
  consumer-visible. Version 2 is the declared seam and it has been taken.
- The client tests build their own payloads, so a server shape change cannot
  redden them. Keeping the fixtures realistic is the only guard against the
  client drifting a version behind the server.
- R-0738 stays open and is T003's to repair.
<<<END PLANF033R4

<<<SLICE RECORDF033R4
Gate: F033 R3 — THE PARSER SEAM. THE ROUND PASSED. Every gate was re-executed by the reviewer at `51e04c89` from a script of its own, and every reading reproduced. TRANSPORT EQUAL at 20035 bytes and sha256 `bb621ceb…a74b1` against the reviewer's own original, with ONE blob id at C0b. THE RECORD APPEND reconstructs 1435760 plus one newline plus 4340 to 1440101, the committed blob exactly, the base a byte PREFIX, N counted at 1, and the NEGATIVE CONTROL placed at offset 1435791 INSIDE the first appended paragraph rejected by BOTH readers. THE LEDGER is UNMOVED at 299 registered, `Done:` 44 over 42, `Landed:` 11 and the open set 257, with `Gate:` alone moving 119 to 120 and `^Gate: F033 R2 — ` reading 1. THE PARSER WAS READ AS A DIFF, LINE BY LINE, AND IT REMOVES NOTHING: `DIFF_VIEW_VERSION` is 2, the module imports `hunk_identity`, the stale claim `there is no endpoint yet` occurs ZERO times, `import os`, `import subprocess`, `import logging` and `open(` are all absent, and `ruff check` exits 0 at "All checks passed!". The id is computed from the file's resolved path, the hunk's `ctx` and `del` lines in order with `add` excluded, and an occurrence rank counted PER FILE and keyed on the normalised text rather than on the finished digest — and the round also corrected two neighbouring comments that still asserted the positional fact, which is the sweep R-0417's class asks for and which nothing gated. THE STABILITY PROPERTY WAS MEASURED BY THE REVIEWER AGAINST THE SHIPPED PARSER ON ITS OWN FIXTURES, not read out of the handback: with a two-hunk file, the second hunk's id survives an earlier hunk gaining an added line, survives a whole new hunk being inserted ahead of it, and survives its OWN added line changing — three perturbations, one unchanged id — while a newly inserted hunk takes a genuinely new id, two byte-identical old sides in one file take distinct ids, and every id is sixteen lowercase hex characters. THE THREE MUTATION RED-PROOFS WERE REPRODUCED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE with its own anchors, each asserted unique before replacement: the UNMUTATED CONTROL exits 0 at 50 passed, then admitting `add` lines into the old side reddens exactly `test_added_lines_do_not_enter_the_hunk_id`, pinning the occurrence to 0 reddens exactly `test_two_identical_hunks_in_one_file_get_distinct_ids_by_occurrence`, and reverting the version reddens exactly `test_diff_view_version_is_two_for_the_content_derived_hunk_ids`. THE SUITES were re-run SERIALLY in the primary checkout: `tests/orchestration/test_diff_parser.py` 50 passed against 43 at the base, `tests/orchestration/test_diff_view_source.py` 15, `tests/orchestration/test_hunk_identity.py` 10, `tests/docs/` 295, `tests/ui_server/` 497, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 and the canary `tests/cli/test_golden_path.py` 42, every REAL exit 0. THE STRUCTURE: six SINGLE-PARENT commits of 286, 221, 18, 2, 339 and 313 insertions, all under 500, the path set matching the change set in BOTH directions, and `git ls-files .remedy-wt` reading 0. THE WORKER CORRECTED THE REVIEWER ON A LOAD-BEARING POINT AND WAS RIGHT. The block's test 1 ordered a stability check in which an EARLIER hunk gains an added line, and asserted that positional ids would fail it. They would not: adding a line INSIDE a hunk moves no hunk's index, so `0:1` survives that perturbation and the test discriminates nothing. The worker shipped the ordered test anyway, as convention 1 requires, and added `test_a_hunk_keeps_its_id_when_a_whole_new_hunk_is_inserted_before_it`, which moves the observed hunk from index 1 to index 2 and is the shape that actually separates a content id from a positional one. The reviewer confirmed both readings on its own fixtures before accepting them. A stability claim is only worth the perturbation that would break the thing it replaces, and this block did not check that its perturbation would. It damaged nothing on disk, so under amend0827 rule 2 it spends no id and buys no correction round; it is a dated line in `.agent/prose_slips.md` at the next round that writes one.

DECISION F033 D2 — THE CLIENT MAY NOT INVENT AN ID THAT LOOKS LIKE A SERVER ID. THE SITUATION, read at `51e04c89`: `apps/ui/src/api/diffViewModel.ts` answers a hunk carrying no usable id with a synthesised positional one, ``id: rawId !== "" ? rawId : `${fileIndex}:${hunkIndex}` ``. Under version 1 that was harmless, because positional WAS the shape the server sent. Round 3 made server ids content-derived, so the invented value now occupies the same field as a real id, is indistinguishable from one to every consumer downstream, and can never match anything the server would recognise. CHOSEN: keep inventing an id — the client needs one, because `defaultCollapsedHunkIds` and `toggleHunkCollapse` key a `Set<string>` on it and two hunks sharing an id would collapse as one — but prefix it with the reserved `UNIDENTIFIED_HUNK_ID_PREFIX`, so a degraded payload is LEGIBLE as degraded rather than silently plausible, and T002's approval path can refuse such an id instead of sending it to a server that will never match it. ALTERNATIVE 1, drop the fallback and let the id stay empty, REJECTED: every id-less hunk would then share the empty string, and the collapse set would fold them into one, which trades a silent wrong id for a visible wrong behaviour. ALTERNATIVE 2, have the client validate that an id is sixteen hex characters and reject others, REJECTED: the client is not the authority on the server's id shape, and a consumer that rejects what it does not recognise breaks the next version bump for no gain — the version field exists precisely so consumers do not have to sniff. WHY THIS IS NOT MERELY COSMETIC: F033 exists to attribute an operator's consent to a specific piece of content, and an id that cannot be traced to content is the one thing that attribution cannot survive. HOW TO REVERSE: delete the constant and restore the bare positional template; the tests naming the prefix are the ones that would then fail, and they name it explicitly.
<<<END RECORDF033R4

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback.

- **G1 HYGIENE.** `.agent/STOP` read before C0a and before C4, absent both times.
  `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of `<C0a>:.agent/authored/f033-r4.md`
  and of `.remedy-wt/f033-r4-block.md` and whether they are EQUAL; no expected
  digest is stated here because a block cannot carry its own. Then
  `git rev-parse <C0b>:.agent/authored/f033-r4.md` and
  `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** Two readers. (a) the BASE blob, which must be
  1440101 bytes, plus one newline plus RECORDF033R4 equals the C2 blob byte for
  byte; BASE a byte PREFIX; result ending in exactly one newline. (b) let N be
  the paragraph count your script COUNTS in the slice — report it — and compare
  the LAST N blank-line units against the slice's paragraphs IN ORDER. NEGATIVE
  CONTROL at an offset your script PROVES lies inside the FIRST appended
  paragraph; BOTH readers must reject it.
- **G4 THE LEDGER at C2.** At BASE and C2 count `^- R-\d+ — ` with distinct ids,
  `^Done: R-\d+ — ` lines with distinct ids, `^Landed: R-`, and
  `^Gate: F\d+ R\d+ — `; report the open set at both. This round registers and
  resolves nothing: registered must stay 299, `Done:` 44 over 42, `Landed:` 11
  and the open set 257, all UNMOVED, with `Gate:` alone moving 120 to 121.
  `^Gate: F033 R3 — ` at C2 must read exactly 1.
- **G5 THE CLIENT AGAINST THE SPEC.** At C3, each as a measurement:
  `UNIDENTIFIED_HUNK_ID_PREFIX` is EXPORTED from
  `apps/ui/src/api/diffViewModel.ts` and its value is `unidentified:`; the bare
  template ``` `${fileIndex}:${hunkIndex}` ``` occurs ZERO times in that file
  — it occurs exactly ONCE at BASE, so this gate is not vacuous, and you should
  report the BASE count too; and `npx tsc --noEmit` in `apps/ui` exits 0. Invoke
  `npx` through Python, not `npm run`.
- **G6 VITEST.** In the PRIMARY checkout, from `apps/ui`, through Python:
  `npx vitest run --reporter=basic src/api/diffViewModel.test.ts` must exit 0.
  Report the test count; it was 93 at BASE and this round ADDS tests, so report
  both numbers. Then run the Python suites that read this seam, SERIALLY, one
  pytest process at a time, each exiting 0: `tests/ui_server/` (497 at BASE) and
  the canary `tests/cli/test_golden_path.py` (42 at BASE).
- **G7 THE VITEST RED-PROOF.** In a DISPOSABLE `git worktree` at C3, never in the
  primary checkout. A fresh worktree has NO `apps/ui/node_modules` — it is
  gitignored — so run the runner from the PRIMARY checkout and point it at the
  worktree's sources. The reviewer verified this exact route at `51e04c89`, with
  cwd `apps/ui` of the PRIMARY checkout:

      npx vitest run --reporter=basic \
        --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui \
        src/api/diffViewModel.test.ts

  FIRST the UNMUTATED control — it must exit 0; report the count. Then mutate the
  WORKTREE's `apps/ui/src/api/diffViewModel.ts` so the fallback returns the bare
  positional id again, without the prefix, assert the anchor is UNIQUE before
  replacing it, and report the REAL exit code, the failure count and the NAME of
  each failing test. It must go RED. Revert, remove the worktree BY EXACT PATH,
  then `git worktree prune`. If the mutation comes back GREEN, report that
  plainly and do NOT adjust anything to force a red.
- **G8 STRUCTURE.** Walk `git rev-list --reverse BASE..C3`: each commit exactly
  ONE parent, each under 500 INSERTIONS — the `+` column of `git diff --numstat`,
  never insertions plus deletions — and report the per-commit list. C4's own
  numbers are NOT ordered here; the reviewer measures C4 at the next gate. Report
  the range's path set against the change set in BOTH directions. Count
  `<<<SLICE ` and `<<<END ` in `.agent/plan.md` and both `apps/ui` files: each 0,
  against `.agent/authored/f033-r4.md` as a non-zero control whose count you
  report. `git ls-files .remedy-wt` must read 0.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 1,
round 4, BASE, the changed-files table with real `+/-` from `git diff --numstat`,
one line per gate with real numbers, the item-status table with every ordered
item exactly once, and your deviations. Quote the final fallback expression and
the fixture values you chose, and list the test names you added or renamed. No
length cap. Write no verdict on your own work.
