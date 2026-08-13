── STEP T-DOC/1 — F111 Diff-only repair · Round 20 ───────────────────
Goal:        Ship the feature's ist-doc, register it in the docs index, and
             clear finding R-0318 — the last content work before the
             integration gate.
Bundle:      C1 save this block · C2 create the ist-doc · C3 register it in
             docs/README.md · C4 fix R-0318 in builder_bridge.py ·
             C5 record the R19 gate in live_review · C6 plan + handoff
Change:      EXACTLY these paths, nothing else:
               .agent/authored/f111-r20-1.md   (new, C1)
               .agent/last_block.md            (rewrite, C1)
               docs/system/diff-only-repair-v1.md (new, C2)
               docs/README.md                  (two added rows, C3)
               packages/orchestration/builder_bridge.py (comment only, C4)
               .agent/live_review.md           (append only, C5)
               .agent/plan.md                  (full rewrite, C6)
               .agent/handoff.md               (full rewrite, C6)
Constraints:
  - TEXT-A, TEXT-B, TEXT-C, TEXT-D and TEXT-E are AUTHORED text. Apply them
    byte for byte. Do not reword, rewrap, re-punctuate, or "improve" them.
    If an authored text looks wrong, apply it anyway and report it as a
    declared deviation in the handback — do not silently fix it.
  - C4 changes a COMMENT only. No behaviour, no identifier, no signature, no
    test may change. If you find yourself editing anything else in
    builder_bridge.py, stop and report.
  - Do NOT write a `Done:` paragraph in .agent/live_review.md. `Done:` is
    reserved for reviewer-authored text
    (docs/agents/planner_reviewer_prompt.md §4.4). For C4 you write exactly
    ONE line, at column 0, in the shape
    `Landed: R-0318 — <one line: what changed, which commit>`
    appended after TEXT-D, and nothing else of your own in that file.
  - No line in any file you create may carry trailing whitespace.
  - Do not touch docs/roadmap/**, tests/, or any other package.
  - Six commits, one per C-item. Each stays far below the 500-insertion cap.
Done when: every command below has been RUN for real and its true output
           recorded in the handback. A guessed or expected value is a finding.
  a. `cmp .agent/authored/f111-r20-1.md .agent/last_block.md` exits 0.
     Record `sha256sum` of both, and `wc -lc` of the authored file.
  b. Extraction proof for the doc — run exactly this and record the word it
     prints:
       python3 - <<'PY'
       from pathlib import Path
       src = Path('.agent/authored/f111-r20-1.md').read_text(encoding='utf-8').split('\n')
       b = src.index('<<<BEGIN TEXT-A docs/system/diff-only-repair-v1.md>>>')
       e = src.index('<<<END TEXT-A>>>')
       extracted = '\n'.join(src[b+1:e]) + '\n'
       target = Path('docs/system/diff-only-repair-v1.md').read_text(encoding='utf-8')
       print('MATCH' if extracted == target else 'MISMATCH')
       PY
     It must print MATCH. MISMATCH means the doc is not what was authored:
     fix the doc, never the proof.
  c. `grep -c 'diff-only-repair-v1.md' docs/README.md` prints exactly 2
     (one quick-find row, one system-list row; it was 0 before this round).
  d. `grep -cF '(\`hunk_count\`, \`total_chars\`, \`omitted\`)' packages/orchestration/builder_bridge.py`
     prints 0, and
     `grep -cF '(\`hunk_count\`, \`total_chars\`, \`full_file_chars\`, \`omitted\`)' packages/orchestration/builder_bridge.py`
     prints 1.
  e. `git diff ed7eaeef..HEAD -- packages/orchestration/builder_bridge.py`
     shows ONLY comment lines changed. Paste that diff in the handback in
     full — it is short.
  f. In `.agent/live_review.md`: `grep -c '^Done:'` prints 11 (unchanged),
     `grep -c '^Landed:'` prints 1, `grep -c '^### R19 — PASS'` prints 1,
     `grep -c '^- R-0'` prints 43 (unchanged — this round registers nothing).
  g. `wc -l .agent/plan.md` prints 44.
  h. `python3 -m pytest tests/docs/ -q` — record the tail and exit code.
  i. `python3 -m pytest tests/orchestration/test_builder_repair_loop.py -q` —
     record the count and exit code (it was 14 passed at the R18 gate).
  j. `python3 -m pytest tests/cli/test_golden_path.py -q` — the canary; it was
     42 passed at R19.
  k. `python3 -m ruff check packages/orchestration/builder_bridge.py` — record
     the real output and exit code. If ruff is not installed, say so; do not
     substitute another tool silently.
  l. `git status --porcelain` is empty, `git diff --name-only ed7eaeef..HEAD`
     lists exactly the eight paths above, and
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     prints 0 and 0 after the final push.
Handback:  a completion report + rewrite `.agent/handoff.md`
           (docs/agents/handback_template.md). It carries the item-status
           table (C1-C6, every item exactly once), the commit table with real
           SHAs and insertion counts, the changed-files table, and every
           result a-l as a REAL value. It repeats the Fortschritt line
           verbatim. If it exceeds 60 lines, carry a "Deviations, declared"
           line naming the count and the mandated content that caused it
           (AGENTS.md DECISION D15).
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1 — commit `chore(f111): save the R20 step block verbatim`
  Save the block bytes to `.agent/authored/f111-r20-1.md`, then copy that file
  to `.agent/last_block.md` (a copy, so the bytes cannot drift). Run gate (a).

C2 — commit `docs(f111): document the diff-only repair path`
  Create `docs/system/diff-only-repair-v1.md` from TEXT-A: every line strictly
  between the `<<<BEGIN TEXT-A …>>>` and `<<<END TEXT-A>>>` marker lines, with
  a single trailing newline at end of file and no other change. The marker
  lines themselves are transport only and never appear in the doc. Run gate (b).

C3 — commit `docs(f111): register the diff-only repair doc in the index`
  Apply the two TEXT-B pairs to `docs/README.md`. Both are APPEND-shaped: each
  TO contains its FROM verbatim as its first line, followed by one new row.
  Insert nothing anywhere else; the surrounding rows keep their order. Run
  gate (c).

C4 — commit `fix(f111): complete the metadata enumeration in the diff comment`
  Apply the TEXT-C pair to `packages/orchestration/builder_bridge.py`. It is a
  REWRITE: the two FROM lines are replaced by the three TO lines. Nothing else
  in the file changes. Run gates (d), (e), (i), (k).

C5 — commit `chore(f111): record the R19 gate in the live review`
  Append TEXT-D to the END of `.agent/live_review.md`, then append your own
  single `Landed: R-0318 — …` line after it as the Constraints describe. Run
  gate (f).

C6 — commit `chore(f111): refresh the plan and write the R20 handoff`
  Replace `.agent/plan.md` with TEXT-E in full. Rewrite `.agent/handoff.md`
  yourself per the Handback line. Run gates (g), (h), (j), (l), then push.

<<<BEGIN TEXT-A docs/system/diff-only-repair-v1.md>>>
# Diff-Only Repair v1

> Built state of F111 (`docs/roadmap/features/T2_F111.md`, Tier 2). A repair
> round in the BOUNDED repair loop sends only the failure-relevant hunks and
> accepts a unified diff back, falling back to the full-file round on any doubt.

## Where this applies — and where it deliberately does not

The path is `run_builder_bridge_loop` in
`packages/orchestration/builder_bridge.py`: the bounded
build → bridge → test → repair-context → rebuild cycle, whose bridge already
applies a `StructuredPatch` through the fenced applicator in
`packages/orchestration/source_apply.py`.

`packages/orchestration/pingpong_loop.py` is NOT on this path (DECISION F111
D1). Its builder is an agentic CLI that edits the staging tree itself, its
`BuilderOutput` carries no patch, and no applicator is invoked there — so there
is no seam for a diff channel to attach to. Remedy deliberately does not route
ping-pong repairs through the diff channel in v1.

## Knobs

| Parameter of `run_builder_bridge_loop` | Default | Effect |
|---|---|---|
| `diff_mode` | `True` | `False` ⇒ every repair round is full-file, reason `diff_mode_off` |
| `diff_margin_lines` | `3` | context lines added on each side of every selected range |

## Prompt side — what a repair round carries

`packages/orchestration/diff_repair.py` selects the source a repair prompt
sends:

    select_repair_hunks(repo_root, changed_line_ranges, *,
                        margin_lines=3, max_total_chars=20000)

The line ranges come from the PATCH THAT WAS APPLIED, through
`changed_line_ranges_from_patch` → `review_scope.parse_diff_line_ranges` — not
from the `source_patch_applied` timeline event, whose metadata carries file
lists and no line numbers at all (DECISION F111 D3).

Selected hunks reach the repair context as `diff_hunks`; every path that
carried none reaches it as `diff_hunks_omitted` with a reason — `missing`,
`binary`, `no_ranges`, `out_of_bounds` or `budget`. `out_of_bounds` is the
load-bearing one: lines WERE requested but none of them exist in the file,
which is how a stale diff becomes visible instead of being swallowed.

The prompt-side choice is recorded as `repair_mode`: `diff`, or `full_file`
with a reason (`no_patch`, `no_ranges`, `no_hunks_selected`, `diff_mode_off`).

## Response side

`packages/orchestration/diff_repair_response.py` accepts one versioned record:

    {"format": "unified_diff", "diff": "<unified diff>", "files": ["<path>"]}

`validate_diff_repair_response` rejects a diff touching any file outside the
declared `files` list, and `precheck_diff_repair_fences` asks the job's fences
BEFORE any file is opened — so a diff aimed at a fence-denied path never
reaches the applicator by construction, rather than by an exception raised
mid-apply. `diff_repair_response_to_patch` then converts the accepted answer
into the `StructuredPatch` the existing applicator already takes.

## Apply side — all-or-nothing, or full fallback

`apply_diff_repair` (`packages/orchestration/diff_repair_apply.py`) reports a
mode as data, never as an exception:

| Mode | Meaning |
|---|---|
| `diff` | the unified diff landed; the full-file round was skipped |
| `full_fallback` | nothing landed; `fallback_reason` names why |

`fallback_reason` is prefixed by the stage that refused: `validation:`,
`fence_denied:` or `apply_failed:`. Context matching is STRICT — no fuzz, no
offset search, and nothing shells out to `patch` or `git apply`.

All-or-nothing is `source_apply`'s durable snapshot, created and verified
before any mutation; this path adds no rollback and no second reading of
unified-diff syntax of its own. When the applicator's own restore fails it says
so — `rollback_incomplete (N file(s)): …` — and the result then carries
`rollback_incomplete=True` plus the real `files_modified` count instead of a
reassuring zero.

New-file creation and deletion both stay on the full-file path in v1 (DECISION
F111 D6): the applicator requires the target file to exist, so a creation diff
fails the apply and the round falls back, and the full-file round creates the
file under the same durable snapshot.

## Evidence

Timeline events on this path: `repair_mode_selected` (the prompt-side choice
plus the size pair below), `diff_repair_not_used` (the answer was not a valid
diff record), `diff_repair_applied` (mode, `fallback_reason`, `files_modified`,
`rollback_incomplete`) and `repair_round_fell_back_to_full_file`. The bridge
stop reason for a discarded attempt is `diff_repair_fell_back`.

`repair_mode_selected` carries the pair the saving is read from: `total_chars`,
what the diff path SENT, and `full_file_chars`, what the full-file path WOULD
have sent for the same paths. Both are CHARACTERS, never tokens (DECISION F111
D9) — calling them tokens turns a real measurement into a fabricated one.
Remedy deliberately does not record a derived `chars_saved` field: a derived
number can disagree with its own inputs, and the reader can subtract.

## Related

- [repair-loop-v1.md](repair-loop-v1.md) — the approval-gated repair PROPOSAL
  path. A different loop: it never applies code and never calls a provider.
- `docs/roadmap/features/T2_F111.md` — the target spec and its decisions.
<<<END TEXT-A>>>

TEXT-B — two APPEND pairs for docs/README.md

  PAIR B1 (quick-find table)
  FROM (1 line, occurs exactly once):
| context | [context-inspector.md](system/context-inspector.md) | system |
  TO (2 lines):
| context | [context-inspector.md](system/context-inspector.md) | system |
| diff-only repair | [diff-only-repair-v1.md](system/diff-only-repair-v1.md) | system |

  PAIR B2 (system file list)
  FROM (1 line, occurs exactly once):
| [development-artifact-boundary-v0.md](system/development-artifact-boundary-v0.md) | Boundaries between dev artifacts and production |
  TO (2 lines):
| [development-artifact-boundary-v0.md](system/development-artifact-boundary-v0.md) | Boundaries between dev artifacts and production |
| [diff-only-repair-v1.md](system/diff-only-repair-v1.md) | Diff-only repair: hunk selection, unified-diff response, strict apply, full-file fallback |

TEXT-C — one REWRITE pair for packages/orchestration/builder_bridge.py

  FROM (2 lines, occurs exactly once, four leading spaces on each):
    # (`hunk_count`, `total_chars`, `omitted`) — because `build_repair_context`'s
    # contract is that its dict is safe to log; source text belongs in the prompt.
  TO (3 lines, four leading spaces on each):
    # (`hunk_count`, `total_chars`, `full_file_chars`, `omitted`) — because
    # `build_repair_context`'s contract is that its dict is safe to log; source
    # text belongs in the prompt.

TEXT-D — append verbatim to the END of .agent/live_review.md

### R19 — PASS (2026-08-13)

Reviewed by the main session over 916b997e..ed7eaeef. This gate was recorded one
round late, and deliberately: R19 was the last round of its session, so by
docs/agents/planner_reviewer_prompt.md §4.13 its verdict lived only in
`.agent/handoff.md` until a later round could carry it. R20 is that round. The
absence was the terminator, not a missing gate, and nothing was reopened to
produce this entry.

Every value below was re-run by the reviewer on this machine at the start of
the R20 session; none was read off the handback. Transport:
`.agent/authored/f111-r19-1.md` and `.agent/last_block.md` are byte-identical
under `cmp`, 11951 bytes, 198 lines, sha256
48441002284c61d6ab0a28ed94b6253091bf0d59a30d4bd1f6f49cb608084acb, and no line
in the authored file carries trailing whitespace. Markers at the R19 gate:
eleven resolution paragraphs, 43 registered findings, one R18 gate heading, zero
unreviewed-fix markers, and `R-0318` twice — its registration and the
back-reference to it. `.agent/plan.md` is 45 lines, under the AGENTS.md cap.
Scope: exactly the five `.agent` paths the block ordered, with per-commit
insertions 198, 153 and 70 plus the handoff commit, each far under 500. The
canary re-ran at 42 passed, exit 0, and `git status --porcelain` is empty.

R19 wrote no production code, and the defect it registered was still present at
review time: the reviewer read
`packages/orchestration/builder_bridge.py` and confirmed the comment enumerated
three keys while the dict beneath it returned four. That is R-0318 exactly as
registered, and R20 fixes it.

TEXT-E — the complete new .agent/plan.md (44 lines)

# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: ed7eaeef (R19 PASS).
Next free finding ID: R-0319. Open findings: 32 — 43 registered minus
11 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T001, T002 and T003 are complete and gated. R20 shipped the feature's
ist-doc `docs/system/diff-only-repair-v1.md`, registered it in
docs/README.md, cleared R-0318 and recorded the R19 gate. What remains
is proving the build against the whole repository and closing it.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md: full suite
   with `-n auto`, base against branch, every branch-only failure
   attributed rather than assumed (R-0286: five known base failures).
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job,
   FRESH review zip, the authored STATUS line committed last, the PR
   created and NOT merged in that session.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- The saving is measured in CHARACTERS, not tokens (DECISION F111
  D9). Any doc, STATUS line or PR body calling them tokens turns an
  honest measurement into a fabricated one.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.
- 32 findings stay open at closure, none above Medium, each carried
  as an accepted risk exactly as F107 carried its own.

Fortschritt: ~95 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate offen · Closure offen) — Schätzung
