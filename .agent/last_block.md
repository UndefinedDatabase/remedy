STEP amend0905-throughput — Part 2 (2a session length, 2b soft-limit default, 2c ledger rotation) — single operator-amendment branch
BRANCH feature/amend0905-throughput, cut from `main` after F262's closure PR merged

Goal
  Land the operator's 2026-09-05 Part 2 amendment: two rule paragraphs in
  docs/agents/self_drive_protocol.md (2a, 2b), the ledger-rotation script
  with its tests and its two rule paragraphs (2c), the FIRST rotation of
  .agent/live_review.md on this branch, and a DECISION entry; then push and
  open the pull request. Do NOT merge — the reviewer reads the checks and
  merges under the operator's authorization.

Bundle, in this order (one commit each)
  C0a save this block verbatim to .agent/authored/amend0905-1.md
  C0b mirror it to .agent/last_block.md
  C1  docs/agents/self_drive_protocol.md: apply the SESSION pair (2a), the
      SOFT pair (2b) and the SDP_ROT pair (2c); docs/roadmap/STATUS_closure_protocol.md:
      apply the SCP_ROT pair (2c). One commit — the four paragraphs describe
      one amendment.
  C2  scripts/rotate_live_review.py (new) written to SPEC, plus
      tests/orchestration/test_live_review_rotation.py (new) written to SPEC.
  C3  THE FIRST ROTATION: `python3 scripts/rotate_live_review.py --dry-run`
      first (report its output), then the real run; commit exactly
      .agent/live_review.md and .agent/live_review_archive.md (new).
  C4  append DECISION (below) to .agent/decisions.md; replace .agent/plan.md
      with PLANP2 (below).
  then push, run G3/G4 (must be green), `gh pr create` (constraint 9)
  C5  rewrite .agent/handoff.md (below: what it must carry); push.

Change set - EXACTLY these paths and nothing else
  .agent/authored/amend0905-1.md, .agent/last_block.md (C0a/C0b) -
  docs/agents/self_drive_protocol.md, docs/roadmap/STATUS_closure_protocol.md
  (C1) - scripts/rotate_live_review.py, tests/orchestration/test_live_review_rotation.py
  (C2) - .agent/live_review.md, .agent/live_review_archive.md (C3) -
  .agent/decisions.md, .agent/plan.md (C4) - .agent/handoff.md (C5)

Constraints
  1. Every authored slice (the four docs pairs, DECISION, PLANP2) is applied
     BYTE FOR BYTE from the COMMITTED .agent/authored/amend0905-1.md by
     marker extraction in Python, never retyped. Pairs via
     str.replace(FROM, TO, 1) after confirming FROM occurs EXACTLY ONCE.
     All four pairs are APPEND-shaped: `TO contains FROM: true` for SESSION,
     SOFT, SDP_ROT and SCP_ROT (the TO is the FROM plus the new paragraph),
     so the obligation is FROM exactly 1x afterwards and the new paragraph
     present exactly 1x — re-check and report each reading.
  2. Read .agent/STOP before C0a, before C3 and before the PR step; if
     present, finish the commit in hand, write the handback, stop, create
     no PR.
  3. The script and the test are PRODUCTION CODE written by you to the
     SPEC — no slice is shipped. Keep them ruff-clean (`ruff check
     scripts/rotate_live_review.py tests/orchestration/test_live_review_rotation.py`
     must print "All checks passed!"; report the exact output or refusal).
  4. C3 rotates the REAL ledger. Before the real run, record
     `wc -c .agent/live_review.md` and the open-findings count; after it,
     both again plus `wc -c .agent/live_review_archive.md`. The script's
     own printed lines go into the handback verbatim. If the script refuses,
     STOP: commit nothing for C3, report the refusal text, continue with C4
     (DECISION still lands, stating the refusal) and C5.
  5. NEWLINE CONVENTIONS: DECISION appends to .agent/decisions.md as EXACTLY
     ONE newline byte then the slice, no trailing newline (this file's
     consecutive-`##` convention). PLANP2 replaces .agent/plan.md whole, no
     trailing newline.
  6. Sandbox forms this session refuses are re-expressed in Python and each
     re-expression reported; never `cd`; `remedy` is denied (nothing here
     needs it).
  7. Commit subjects `amend0905: <what>`, no leading-slash token, no
     absolute path; trailers as instructed in the prompt.
  8. `.agent/decisions.md` is NOT rotated. Measure `wc -c .agent/decisions.md`
     before C4 and put it, with a one-paragraph follow-up proposal of your
     own words (what a decisions rotation would move — closed features'
     `## DECISION F<id> D<n>` entries — and what it must preserve), in the
     handoff's Next section.
  9. THE PULL REQUEST, after C4 is pushed and G3/G4 are green, BEFORE C5 so
     the handoff carries its number: write the PRBODY slice to a scratch
     file and run
       gh pr create --title "amend0905-throughput: session length, split-and-close default, ledger rotation" --base main --head feature/amend0905-throughput --body-file <file>
     Report the PR number and URL. Never `gh pr merge`.

Done when - the gates. Real exit codes, real output.
  G1 TRANSPORT. `sha256sum .agent/authored/amend0905-1.md .agent/last_block.md`
     - one digest, twice.
  G2 THE DOCS PAIRS. Per pair: FROM count before (1), `TO contains FROM`
     (true), after C1 `grep -c "amend0905-throughput" docs/agents/self_drive_protocol.md`
     reads 3 and the same grep over docs/roadmap/STATUS_closure_protocol.md
     reads 1; `grep -c "Reverse by deleting this paragraph."` over each file
     grew by exactly 3 and 1 respectively (report before/after).
  G3 THE SCRIPT AND ITS TESTS. `python3 -m pytest tests/orchestration/test_live_review_rotation.py -q`
     green (report the count); ruff per constraint 3; `python3 scripts/rotate_live_review.py --help`
     exit 0.
  G4 THE SUITES that read these files, serially:
       python3 -m pytest tests/docs/ -q                                (expect 295)
       python3 -m pytest tests/test_agent_tooling.py -q                (report)
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q (expect 16)
       python3 -m pytest tests/orchestration/test_self_use_generator.py -q (report)
       python3 -m pytest tests/ui_server/ -q                           (expect 515)
       python3 -m pytest tests/orchestration/test_test_runner.py -q    (expect 52)
       python3 -m pytest tests/regression/test_resource_safety.py -q   (expect 21)
       python3 -m pytest tests/cli/test_golden_path.py -q              (expect 42)
     plus `python3 -m apps.cli.grouped integrity check --json` AFTER C3
     (expect passed true, fail_count 0).
  G5 THE ROTATION (constraint 4): dry-run output; real-run output; old and
     new `wc -c` of the ledger; archive size; open-findings count before and
     after (identical); `grep -c '^Gate: ' .agent/live_review.md` after
     (report) and the same over the archive; `git show --numstat <C3>`
     names exactly the two files.
  G6 RED-PROOF of the test, in a disposable `git worktree` (never the
     primary checkout; address files by absolute path, run pytest via
     `subprocess.run(cwd=<worktree>)`): (a) control — the test file passes
     unmutated in the worktree; (b) mutate the worktree's script so the
     archive writer drops the LAST byte of every appended record — the
     verification test(s) must FAIL; (c) mutate the worktree's script so
     the pre-write sha256 check is skipped — at least one test must FAIL;
     (d) restore, control passes again; remove the worktree and its tmp
     branch, prove with `git worktree list`. Report each colour with the
     failing test ids.
  G7 STRUCTURE. `git status --porcelain` empty before C5 is staged;
     `git ls-files .remedy-wt | wc -l` 0; per-commit numstat for C0a..C4
     against the handback's Commits table; each commit single-parent and
     under 500 insertions EXCEPT C3, which is the verbatim rotation of a
     single `.agent/**` state file pair — declare its numbers as the
     AGENTS.md DECISION F104 D1 exemption; the PR number/URL, not a draft,
     not merged; the push result.

SPEC — scripts/rotate_live_review.py (production code: written by the worker to this
spec, reviewed by the reviewer; no slice is shipped for it)

Purpose: move long-closed records out of `.agent/live_review.md` into the append-only
`.agent/live_review_archive.md`, byte-verbatim, with the script's own verification.

Record model (line-oriented; a "paragraph" model is WRONG for this file because
some features appended records with a single newline separator):
  - A RECORD starts at any line matching one of these start patterns, anchored at
    column 0: `Gate: `, `- R-\d{4} — `, `Done: R-\d{4} — `, `Landed: R-\d{4}`,
    `LANDED`, `Recurrence: R-\d{4}`, `RECURRENCE of R-\d{4}`, `RECOVERED`,
    `DECISION F\d{3} D\d+`, `#`, `>`, `R\d+ ` (the last three are the header,
    blockquote and Steps lines of the file's own preamble).
  - A record runs from its start line to the line before the next start line,
    with trailing blank lines stripped off the record (they are separators, not
    content). Indented `  FIX` paragraphs and wrapped continuation lines belong to
    the record above them.
  - A Gate record's feature id is parsed from its header by exactly two forms:
    `^Gate: F(\d{3}) R\d+` and `^Gate: R\d+ — the F(\d{3}) R\d+ entry`. Measured
    on 2026-09-05: 340 Gate records, both forms cover all 340, 0 unparsed. A Gate
    header matching neither form is NEVER moved (and is reported).
  - `[x]` feature ids come from `docs/roadmap/STATUS.md` lines matching
    `^- \[x\] F(\d{3}) — `.

What moves: (i) every Gate record whose feature id is `[x]`; (ii) every resolved
finding pair, DEFINED NARROWLY as an id with EXACTLY ONE `- R-xxxx — ` registration
record and EXACTLY ONE `Done: R-xxxx — ` record — both records move. Ids with two
`Done:` records (today `R-0721` and `R-0725`), `Landed:`, `Recurrence:`, `DECISION`
and every other record kind stay where they are. Nothing else is touched: the
preamble, `## Steps`, `## Findings`, open findings.

How it moves: (1) compute sha256 over each moving record's bytes; (2) rebuild the
ledger text by dropping each moving record's lines AND the blank separator lines
immediately preceding it, leaving every remaining byte in place; (3) append to the
archive — created if absent with a short header (`# Live Review Archive — rotated
records` plus one blockquote line saying records are moved here byte-verbatim by
this script and are read on demand by id, never at session start) — each moved
record in ledger order, separated by exactly one blank line (`\n\n`), never
touching any byte the archive already held; (4) VERIFY before writing anything:
every moved record's bytes occur verbatim in the new archive text and hash to the
digest computed in (1); the new archive bytes start with the old archive bytes
(append-only); the open-findings count — `^- R-\d{4} — ` lines minus
`^Done: R-\d{4} — ` lines — is identical before and after; the moved records are
exactly the ones absent from the new ledger; (5) only then write both files; on ANY
verification failure exit non-zero with the reason and write nothing.

CLI: `python3 scripts/rotate_live_review.py [--ledger PATH] [--status PATH]
[--archive PATH] [--dry-run]`; defaults are the repo files. It prints, on one line
each: records moved (gates and pairs separately), old ledger size, new ledger size,
old archive size, new archive size, open findings before and after. `--dry-run`
prints the same and writes nothing. A run with nothing to move exits 0 and changes
no byte. Stdlib only, `from __future__ import annotations`, ruff-clean under the
repository's `pyproject.toml`. Style: module docstring, small pure functions
(`split_records`, `classify_record`, `select_movable`, `rotate`), `main()` with
argparse, `if __name__ == "__main__": raise SystemExit(main())`.

SPEC — tests/orchestration/test_live_review_rotation.py (pytest, tmp_path fixtures,
synthetic ledger + STATUS files, imports `scripts.rotate_live_review`):
  1. moved records reappear byte-identical in the archive and are absent from the
     ledger (a Gate of an `[x]` feature in BOTH header forms; a resolved pair).
  2. a Gate of a non-`[x]` feature, an OPEN finding, a `Landed:` line, a
     `Recurrence:` paragraph and an id with two `Done:` records all stay.
  3. open-findings count identical before and after (line formula).
  4. the archive is append-only: a second run with a new `[x]` feature keeps the
     first archive bytes as an exact prefix.
  5. idempotence: a second run with nothing new moves 0 records and changes no byte
     of either file.
  6. refusal: monkeypatch the verification input (e.g. make the archive writer
     drop one byte of a record, or patch the digest function) and assert the
     script exits non-zero / raises and leaves both files unchanged.
  7. `--dry-run` prints the sizes and writes nothing.
  8. the F262-era single-newline separator shape (a Gate glued to the previous
     record with one `\n`) is handled: the record is moved and the remaining text
     carries no dangling separator.
Every test asserts on bytes read back from disk, never on the function's return
value alone. Red-proof is ordered in G6 below.

The authored slices. Each lies between its own one-line BEGIN and END
marker; the slice is the bytes between the BEGIN marker's newline and the
newline before the END marker, EXCLUDING that final newline.

<<<BEGIN SESSION_FROM>>>
  for it. The SOFT LIMIT is 25 rounds OR 7 sessions per feature, whichever
  comes first; on reaching it the obligation is a scope report, not more
  work — see "Ending a session". Reverse by deleting this paragraph.
<<<END SESSION_FROM>>>

<<<BEGIN SESSION_TO>>>
  for it. The SOFT LIMIT is 25 rounds OR 7 sessions per feature, whichever
  comes first; on reaching it the obligation is a scope report, not more
  work — see "Ending a session". Reverse by deleting this paragraph.
  Operator amendment amend0905-throughput (2026-09-05) — SESSIONS CONTINUE
  WHILE CONTEXT COMFORTABLY SUFFICES. The target is SIX TO EIGHT delegated
  rounds per session; four remains the floor. The honest early-end reasons
  above are unchanged — demonstrably exhausted context, or a round that
  explicitly needs a fresh session — and now explicitly include the
  reviewer noticing its own authoring errors accumulating (a run of
  `.agent/prose_slips.md` lines in one session is that signal). Every
  handoff adds ONE sentence of context self-assessment in its Session
  section. Rationale: each session boundary re-buys the full cold start —
  protocol, handoff, ledger, decisions — and F109's session 4 already ran
  eight PASS rounds, so the four-to-five default was spending boundaries
  the context did not need. Reverse by deleting this paragraph.
<<<END SESSION_TO>>>

<<<BEGIN SOFT_FROM>>>
Continuing quietly past the limit is a protocol violation. Reverse by deleting
this paragraph.
<<<END SOFT_FROM>>>

<<<BEGIN SOFT_TO>>>
Continuing quietly past the limit is a protocol violation. Reverse by deleting
this paragraph.

Operator amendment amend0905-throughput (2026-09-05) — THE STANDING DEFAULT AT
THE SOFT LIMIT IS SPLIT-AND-CLOSE, EXECUTED BY THE SESSION. On reaching the
soft limit the session still writes the scope report, and then EXECUTES the
default on its own authority: it registers the remaining scope as a new
follow-up feature (registration only, ledger atomicity respected — the
`TOTAL_FEATURES` pin, the README counters and the STATUS line in one commit
with the feature file), closes the current feature at a self-consistent
scope through the normal closure sequence, and records the whole move as a
dated DECISION in `.agent/decisions.md` that the operator may reverse
afterwards. The banner line stays but announces the REPORT, not a stop.
Only when no self-consistent close is possible does the old hard stop with
an operator question remain. This applies equally to a feature found
already past its limit with a pending scope report at session start.
Rationale: F262's round 23 wrote a correct scope report and then waited a
session for a ruling the default would have supplied. Reverse by deleting this paragraph.
<<<END SOFT_TO>>>

<<<BEGIN SDP_ROT_FROM>>>
Verification tiers, the canary, the integration gate and the closure
protocol are unchanged; this file adds no exception to any of them.
<<<END SDP_ROT_FROM>>>

<<<BEGIN SDP_ROT_TO>>>
Verification tiers, the canary, the integration gate and the closure
protocol are unchanged; this file adds no exception to any of them.

Operator amendment amend0905-throughput (2026-09-05) — LEDGER ROTATION.
`.agent/live_review.md` is rotated by `scripts/rotate_live_review.py` as its
own commit inside EVERY closure sequence, after the verdict bookings and
before the STATUS flip: every `Gate:` record whose feature id is `[x]` in
`docs/roadmap/STATUS.md`, and every resolved finding pair (the `- R-xxxx`
registration block with its one matching `Done: R-xxxx` block), moves
byte-verbatim into the append-only `.agent/live_review_archive.md`, which
the script verifies by per-record sha256 before and after and refuses on any
mismatch; the open-findings count is identical before and after. The byte-
append arithmetic of the next round's block re-baselines on the
post-rotation length. The archive is never read at session start — only on
demand, by id. Rationale: the ledger had grown to ~2.5 MB, most of it
per-round `Gate:` records of long-closed features, and every bootstrap paid
for it. Reverse by deleting this paragraph.
<<<END SDP_ROT_TO>>>

<<<BEGIN SCP_ROT_FROM>>>
   The closure handback includes grep proof that every piece of
   reviewer-authored applied text (STATUS line, resolution
   entries) is byte-identical to the authored paste block.
<<<END SCP_ROT_FROM>>>

<<<BEGIN SCP_ROT_TO>>>
   The closure handback includes grep proof that every piece of
   reviewer-authored applied text (STATUS line, resolution
   entries) is byte-identical to the authored paste block.
   Operator amendment amend0905-throughput (2026-09-05) — LEDGER ROTATION
   IS A STEP OF THIS SEQUENCE. After the verdict bookings and BEFORE the
   STATUS `[x]` flip, the worker runs `python3 scripts/rotate_live_review.py`
   as its OWN commit (paths: `.agent/live_review.md` and
   `.agent/live_review_archive.md` only). It moves, byte-verbatim, every
   `Gate:` record of a `[x]` feature and every resolved finding pair into
   the append-only archive, verifies each moved record's sha256 before and
   after and refuses on mismatch, keeps the open-findings count identical,
   and prints the old and new ledger sizes, which the handback records. The
   next block's byte-append arithmetic re-baselines on the post-rotation
   length; the archive is read only on demand, by id, never at session
   start. Reverse by deleting this paragraph.
<<<END SCP_ROT_TO>>>

<<<BEGIN DECISION>>>
## 2026-09-05: amend0905-throughput — session length, split-and-close default, ledger rotation

Operator instruction of 2026-09-05 (Part 2), executed on `feature/amend0905-throughput`
cut from `main` after F262's closure PR merged. Three rules, each a dated paragraph
labelled "Operator amendment amend0905-throughput" ending "Reverse by deleting this
paragraph": (2a) `docs/agents/self_drive_protocol.md` G7 — sessions continue while
context comfortably suffices, target six to eight delegated rounds, four the floor,
early-end reasons unchanged plus the reviewer's own accumulating authoring errors,
one sentence of context self-assessment per handoff; (2b) `docs/agents/self_drive_protocol.md`
"Ending a session" — the standing default at the soft limit is split-and-close
executed by the session (register the remainder as a follow-up feature with ledger
atomicity, close the current feature at a self-consistent scope, record it as a
dated DECISION), the banner announces the report, the hard stop remains only when
no self-consistent close exists; (2c) `scripts/rotate_live_review.py` with
`tests/orchestration/test_live_review_rotation.py`, rule paragraphs in
`docs/agents/self_drive_protocol.md` and `docs/roadmap/STATUS_closure_protocol.md`,
and the FIRST rotation executed on this branch, whose printed counts and old→new
sizes the branch's handoff carries verbatim. Ids with more than one `Done:` block
(`R-0721` and `R-0725` at the time of writing) are left in place so the canonical
line-count open-findings formula reads identically before and after. Not rotated:
`.agent/decisions.md` — its measured size and a one-paragraph follow-up proposal
travel in this branch's handoff. Reverse by deleting the three
rule paragraphs and this entry; the archive file stays, because moving records back
would rewrite the append-only ledger.
<<<END DECISION>>>

<<<BEGIN PLANP2>>>
# Plan — amend0905-throughput (operator amendment, Part 2)

Branch: feature/amend0905-throughput, cut from `main` after F262's
closure pull request merged.

## Goal

Land the operator's 2026-09-05 Part 2: sessions run six to eight rounds
while context suffices (2a); the soft-limit default is split-and-close
executed by the session (2b); `scripts/rotate_live_review.py` rotates
`[x]` Gate records and resolved finding pairs into the append-only
`.agent/live_review_archive.md` as a step of every closure sequence, and
the first rotation runs on this branch (2c).

## Current Step

The single amendment round: four rule paragraphs (C1), the script and its
tests (C2), the first rotation (C3), the DECISION entry and this plan
(C4), the handoff and the pull request (C5). No feature is in progress;
Rule A5 proposes the next feature once this merges.

## Next Steps

- The reviewer reads the PR's hosted checks and merges under the
  operator's 2026-09-05 authorization; end state 0 open PRs.
- Follow-up proposal (handoff): rotate `.agent/decisions.md`.

## Risks

- The rotation commit is large by construction (a verbatim move of one
  state-file pair) — declared under AGENTS.md DECISION F104 D1's exemption.
- Readers of `.agent/live_review.md` (integrity check, self-use generator,
  dashboard contract) must stay green after rotation — gated in G4.
<<<END PLANP2>>>

<<<BEGIN PRBODY>>>
## Summary
- Operator amendment amend0905-throughput (2026-09-05), three rules, each a
  dated paragraph ending "Reverse by deleting this paragraph":
  - 2a `docs/agents/self_drive_protocol.md` G7: sessions continue while
    context comfortably suffices — six to eight delegated rounds, four the
    floor; early-end reasons unchanged and now include the reviewer's own
    accumulating authoring errors; one sentence of context self-assessment
    per handoff.
  - 2b `docs/agents/self_drive_protocol.md` "Ending a session": at the soft
    limit the session writes the scope report and then EXECUTES the
    split-and-close default itself (register the remainder as a follow-up
    feature with ledger atomicity, close at a self-consistent scope, record a
    dated DECISION); the hard stop remains only when no self-consistent close
    exists.
  - 2c `scripts/rotate_live_review.py` + `tests/orchestration/test_live_review_rotation.py`
    + rule paragraphs in both protocol docs: every closure sequence rotates
    `[x]` features' `Gate:` records and resolved finding pairs byte-verbatim
    into the append-only `.agent/live_review_archive.md`, self-verified by
    per-record sha256, open-findings count identical. The first rotation is
    on this branch.

## How to review
- The four paragraphs are appends (`git diff` shows only additions in the
  two docs). The script is stdlib-only; its tests cover byte-identity,
  append-only archive, idempotence, refusal on mismatch, dry-run and the
  single-newline separator shape.
- `.agent/decisions.md` carries the dated entry; the handoff carries the
  old→new ledger sizes and the decisions-rotation follow-up proposal.

## Verification
- `tests/orchestration/test_live_review_rotation.py` green; red-proof in a
  disposable worktree (dropped byte → red, skipped digest check → red).
- `tests/docs/`, `tests/test_agent_tooling.py`, the four `.agent` state
  readers and the golden-path canary green after the rotation; integrity
  check `passed: true`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01LvvDEqLkieE84dZcwifEyU
<<<END PRBODY>>>

Handback: rewrite .agent/handoff.md per docs/agents/handback_template.md
and AGENTS.md — Session line `SESSION 1 of amendment amend0905-throughput ·
round 1 · rounds so far 1` with one sentence of context self-assessment,
Range `Review of <main merge sha>..<C4>`, one changed-files table per
commit, an item-status table over C0a..C5 and G1..G7, External actions
(worktree add/remove, the push, `gh pr create` with the PR number), raw
Verification per gate (the rotation's printed lines verbatim, old→new
sizes), Authored-text proofs, Deviations, and Next: the reviewer's merge
after green checks, plus the one-paragraph `.agent/decisions.md` rotation
proposal with its measured size (constraint 8).
