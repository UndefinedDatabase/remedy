── STEP CLOSE / F111 — Round 19 (SESSION CLOSING, .agent only) ───
Goal:
  Persist what this session learned before it ends: register R-0318, record the
  R18 gate with its two upheld deviations, and rewrite the handoff so the next
  session resumes from disk and not from anyone's memory. No production code,
  no tests, no docs — the integration gate and closure belong to the next
  session.

Bundle (ordered; one commit each, push after EVERY commit per R-0289):
  C1  save this block verbatim to .agent/authored/f111-r19-1.md
  C2  mirror the same bytes into .agent/last_block.md
  C3  .agent/live_review.md, both appends in ONE commit, in this order:
      TEXT-A, then TEXT-B
  C4  replace .agent/plan.md with TEXT-C, then rewrite .agent/handoff.md

Scope — EXACTLY these five paths, no others:
  1 .agent/authored/f111-r19-1.md   2 .agent/last_block.md
  3 .agent/live_review.md           4 .agent/plan.md
  5 .agent/handoff.md

Constraints:
  - You are the worker; you make every commit. Self-review loop before every
    commit, clean tree, push after each commit.
  - Never work on main, never force-push, never merge. No PR this round.
  - Do NOT write a `Done:` paragraph of your own (planner_reviewer_prompt.md
    §4.4). TEXT-A registers a finding as OPEN; it resolves nothing.
  - Apply TEXT-A, TEXT-B and TEXT-C BYTE FOR BYTE. If a text violates a rule,
    do not repair it — apply it and declare the deviation.
  - Do NOT touch packages/, tests/, docs/, docs/roadmap/ or STATUS.md.

Done when — every command run for real, exit code recorded, no value guessed:
  a. TRANSPORT: `sha256sum .agent/authored/f111-r19-1.md .agent/last_block.md`
     -> both digests identical, `cmp` exits 0. State the digest, the byte count
     and `wc -l`, which must be under 400.
  b. `.agent/live_review.md`: `grep -c '^Done:'` -> 11 (unchanged — this round
     resolves nothing); `grep -c '^- R-0'` -> 43 (was 42, R-0318 registered);
     `grep -c '^### R18 — PASS'` -> 1; `grep -c '^Landed:'` -> prints 0.
  c. `grep -c 'R-0318' .agent/live_review.md` -> report the real number.
  d. `wc -l .agent/plan.md` -> under 50.
  e. VERIFY THE UNFIXED DEFECT IS STILL THERE, so R-0318 is not registered
     against something already gone:
     `grep -n 'hunk_count., .total_chars., .omitted' packages/orchestration/builder_bridge.py`
     -> report the line number and the matched text. Do NOT fix it.
  f. `python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed. The
     canary runs even on an `.agent`-only round.
  g. `git status --porcelain` -> empty. `git diff --name-only 916b997e..HEAD`
     -> exactly the five scoped paths. Per-commit insertions from
     `git log --numstat`, each under 500.
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> 0 and 0 after the final push.

Handback: completion report + rewrite .agent/handoff.md. Because this is the
session's LAST round, the handoff is the only return channel and must carry:
feature and round; branch; the four commit SHAs with subjects and insertions;
a changed-files table; the seven gate results a-g with their real values; the
open-findings count and next free ID; the item-status table for C1-C4; the
Fortschritt line from TEXT-C verbatim; and a NEXT SESSION block stating:

  - The branch is UNMERGED with NO PR by design. Phase 0 must sweep `feature/*`
    branches to find `feature/f111-diff-only-repair`; a PR list will not show
    it, and the Open PR Gate will correctly find nothing to merge.
  - Per docs/agents/planner_reviewer_prompt.md §4.13 the LAST round of a branch
    has no on-disk gate entry by construction. The next session must NOT open a
    repair round to close R19: its verdict lives in this handoff.
  - The remaining work, in order: (1) resolve R-0318 in the next production
    touch of `builder_bridge.py`; (2) the integration gate per
    docs/agents/integration_gate.md, full suite with `-n auto`, base against
    branch, attributing the five known base failures (R-0286) rather than
    assuming them; (3) the feature's documentation update, registered in
    `docs/README.md` in the same PR; (4) closure under
    docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip
    (a zip failure is a closure blocker), the authored STATUS line committed
    last, then the PR, which is NOT merged in that session.
  - Any doc, STATUS line or PR body that describes the F111 saving MUST say
    CHARACTERS, not tokens (DECISION F111 D9). Calling these numbers tokens
    turns an honest measurement into a fabricated one.

──────────────────────── TEXT-A — append to .agent/live_review.md ───────────

- R-0318 (Low, F111 R18, a counts-only comment that no longer lists all the
  counts): the comment above the diff-branch return in
  `_attach_diff_repair_hunks` states that the emitted metadata is "counts only
  (`hunk_count`, `total_chars`, `omitted`)". R18 added a fourth key,
  `full_file_chars`, directly beneath it, and the enumeration was not extended.
  The claim the comment protects is still TRUE — no hunk text reaches the
  timeline, and `full_file_chars` is a count like the others — so nothing is
  mis-stated about behaviour. What is wrong is the reading: an auditor checking
  whether source text can leak into evidence reads that parenthesis as the
  whole contents of the dict, and it is now one key short of it. A comment that
  enumerates is a comment that must be maintained, which is exactly why the
  next reader should either complete the list or stop enumerating. The R18
  worker found this and declined to fix it because the block said "Change
  NOTHING else" — the correct call, and it is registered here rather than held
  in a session that is about to end. Fix direction: extend the enumeration in
  the next round that touches `builder_bridge.py` for another reason; do not
  open a round for it alone. OPEN.

──────────────────────── TEXT-B — append to .agent/live_review.md ───────────

### R18 — PASS (2026-08-13)
Reviewed by the main session over 6a93ee1c..916b997e. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport:
`.agent/authored/f111-r18-1.md` and `.agent/last_block.md` are byte-identical
under `cmp`, 15283 bytes, 261 lines, sha256
948da87e9dcde37d50aca36e15a7072ae1f1302dcea7becf7ef9cabe8264654c, no line
carrying trailing whitespace. `.agent/plan.md` matches the TEXT-B slice
extracted from the committed authored file at 45 lines, under the cap. Markers:
eleven resolution paragraphs, 42 registered findings at gate time, one R17 gate
heading, zero unreviewed-fix markers. Scope: exactly the seven ordered paths.
Per-commit insertions 261/176/54/24/151/98, each under 500. `git status
--porcelain` empty, one worktree, and 0 ahead and 0 behind the remote.

Tests re-run by the reviewer: 14 for the repair loop (was 12), 71 for the three
diff-repair files — unmoved — 137 passed and 1 skipped across the nine files
that import `builder_bridge`, and 42 for the golden-path canary.

The measurement was verified INDEPENDENTLY, on a fixture the block never named:
a 120-line file whose repaired function sits at line 40. The recorded pair is
`total_chars` 106 against `full_file_chars` 1824, a ratio of 17.2, and
`full_file_chars` equals the real character length of the file at the moment
the repair context was built. The worker's own fixture recorded 58 against 768,
a ratio of 13.2. Two different files, two different denominators, each equal to
its own file's real size — so the number is measured and not constant, which is
the property the ordered mutation probe also confirms: pinning
`_repair_payload_chars` to a constant 1 fails both new tests and nothing else
in 208 other passing tests. That is the feature's "measured, recorded" DONE
line satisfied by value, in characters per DECISION F111 D9.

Deviation 1 is UPHELD and the fault is the reviewer's, not the worker's. The
R18 block ordered a comment ending "Per DECISION F111 D9 both are CHARACTERS,
never tokens" and, in the same block, a gate requiring `grep -c 'tokens'` over
that same file to print 0. That is precisely the self-counting gate that
DECISION F105 D8 item 2 exists to prevent — a "must be 0" gate over a string
the block's own TO writes into the target file — and it is the seventh
recurrence of that class in this repository. The worker kept the ordered text,
reported the real count of 1, and said why: rewording a comment to make a
number come out right would have been the worse failure. The reviewer confirmed
by measurement that the word `tokens` occurs exactly once in
`builder_bridge.py`, that the occurrence is the ordered comment, and that no
field, key or identifier is named `tokens` — so the substance the gate protects
holds. No finding is registered for it: the countermeasure already exists on
disk as the §3 pre-emission checklist, and registering a finding would only
re-register a rule that is already written down and was not run.

Deviation 2 is upheld: one new fixture builder was added and cycle 1's output is
built inline from a module-level constant, which is what "ONE new fixture
builder" asks for. Deviation 3 is upheld and registered as R-0318 above — the
worker declined to fix an unordered defect and reported it instead, which is the
behaviour this workflow is built to produce. The handoff at 100 lines sits at
the DECISION D15 allowance with its cause named and no section dropped.

──────────────────── TEXT-C — full replacement of .agent/plan.md ────────────

# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 916b997e (R18 PASS).
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
T001, T002 and T003 are complete and gated. The build is done; what
remains is proving it against the whole repository and closing it.
R19 registered R-0318 and recorded the R18 gate so no finding lives
only in a session that has ended.

## Next Steps
1. Resolve R-0318 in the next round that touches builder_bridge.py
   for another reason. Do not open a round for it alone.
2. Integration gate per docs/agents/integration_gate.md: full suite
   with `-n auto`, base against branch, every branch-only failure
   attributed rather than assumed (R-0286: five known base failures).
3. The feature's documentation update, registered in docs/README.md
   in the same PR.
4. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job,
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

Fortschritt: ~93 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration Gate offen ·
Doku offen · Closure offen) — Schätzung
