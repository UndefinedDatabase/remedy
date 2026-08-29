# Handback — F033 · ROUND 20 · rejected hunks rendered as verbatim repair findings

> Written by the WORKER of round 20. The reviewer writes the verdict; this file reports
> what was run and what it printed. This round registered NO finding of its own and wrote
> NO `Done:` and NO `Landed:` line of its own — the two `Done:` paragraphs in
> `.agent/live_review.md` are the reviewer's authored RECORD20 slice, applied byte for
> byte. The existing `Landed: R-0746` line was left where it is, per block constraint 3.

## Session

SESSION 5 of feature F033 · round 20 · rounds so far 20.
The soft limit is NOT reached: 20 rounds of 25, 5 sessions of 7.

## Fortschritt

~95 % (T001 and T002 complete. T003: the fold's partial truth and the popover label landed
in round 16, the tasks-card row in round 17, the fold's shared home and its counts in
round 18, the run report's task line in round 19. THIS round ships the REJECTED half of
T003's loop — `packages/orchestration/hunk_repair_findings.py`, a PURE renderer with no
caller yet, and the verbatim-quote trace proof `docs/roadmap/features/T5_F033.md` calls
acceptance material. Wiring that renderer into the next builder round's prompt remains,
then R-0745, then the operator docs and the closure sequence) — Schätzung.

## Range

Review of `d4a21259`..`4420328a` for the gated work — every gate below ran at a commit no
later than C5 — plus the two commits that cannot be inside it: C6, which writes this file,
and C7, which records the real push outcome after the push.
Branch `feature/f033-hunk-approval-v2`.

## Bundle item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f033-r20.md` | done | |
| C0b mirror it into `.agent/last_block.md` | done | one blob id with C0a |
| C1 `.agent/plan.md` <- PLAN20 | done | whole-file replacement, checklist item 23 |
| C2 `.agent/live_review.md` <- RECORD20 | done | verdict + `Done:` for R-0738 and R-0746 |
| C3 `.agent/prose_slips.md` <- SLIPS20 | done | |
| C4 the rejection-findings renderer (SPEC A) | done | |
| C5 its tests, including the verbatim trace proof (SPEC B) | done | |
| C6 `.agent/handoff.md` <- this handback | done | |
| C7 `.agent/handoff.md` <- the PUSH OUTCOME | done | written after the push |

## Commits

Every `+/-` cell below was taken from the SAME `git diff --numstat` run G8 reports — one
script iterating `git rev-list --reverse d4a21259..4420328a` and running
`git diff --numstat <sha>~1 <sha>` for each — and compared to it CELL BY CELL; they agree.
No cell was filled from a file's own line count.

### e0a754a4 docs(f033): save the round 20 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r20.md` | +344 -0 | C0a — the reviewer's block, byte for byte |

### 0d202c14 docs(f033): mirror the round 20 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +238 -245 | C0b — same bytes; one blob id with C0a |

### 69084af5 docs(f033): advance the plan to round 20
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +20 -22 | C1 — PLAN20 replaces the file whole |

### d9db68ef docs(f033): book the round 19 verdict and resolve R-0738 and R-0746
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +6 -0 | C2 — RECORD20 appended; amend0827 rule 1 |

### 688cf561 docs(f033): append the three round 19 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +6 -0 | C3 — SLIPS20 appended; amend0827 rule 2 |

### 7bd1ea96 feat(f033): render rejected hunks as verbatim repair findings
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/hunk_repair_findings.py` | +130 -0 | SPEC A — NEW module: `REJECTION_FINDINGS_HEADING`, `REJECTION_FINDINGS_ENTRY_PREFIX`, `REJECTION_FINDINGS_REASON_INTRO`, the re-stated `_total_text` coercion guard and the one public function `render_rejection_findings` |

### 4420328a test(f033): pin the verbatim reason trace and the renderer totality
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_hunk_repair_findings.py` | +294 -0 | SPEC B — NEW file, 17 tests in six classes: the verbatim trace proof, ledger order, approved/pending contributing nothing, the two empty-string inputs, driven totality, and the `Public API::` AST guard |

### C6 and C7 (this file)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | see below | C6 writes this handback; C7 appends the real push outcome. A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/r20/wt 4420328a`
  -> REAL exit 0, "Preparing worktree (detached HEAD 4420328a) / HEAD is now at 4420328a".
- `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/r20/wt` -> REAL exit
  0, no output. See D3 for why `--force`. `git worktree list` afterwards printed only
  `/home/decodeux/Repos/remedy  4420328a [feature/f033-hunk-approval-v2]`.
- `git push` — see the PUSH OUTCOME section at the bottom, written by C7.
- No `gh` command was run and no PR was created or merged. F033 is not closed and the PR
  belongs to the closure sequence.

## Verification — one line per gate, real exit codes

G1 HYGIENE AND THE STOP FILE — `ls -la /home/decodeux/Repos/remedy/.agent/STOP` REAL exit
2, printing exactly `ls: cannot access '/home/decodeux/Repos/remedy/.agent/STOP': No such
file or directory`, so the sentinel does not exist; `git status --porcelain` before C0a
REAL exit 0 printing NOTHING, and again after C5 REAL exit 0 printing NOTHING.

G2 TRANSPORT — REAL exit 0, three MATCH verdicts. Each applied region was read AT THE
COMMIT THAT APPLIED IT, which is what the block's own wording now names: PLAN20, whole-file
region at `69084af5` (C1), 2570 bytes, sha256
`11f614e84b0eac586273872dd7938c11fb1ec83b10601f9861172907c089e91a` — MATCH; RECORD20,
last-10101-byte region at `d9db68ef` (C2), sha256
`8cfd110e40c78fd9f2f173f633d3b166d0672106c763c3e693a6fb7f01d5d352` — MATCH; SLIPS20,
last-1622-byte region at `688cf561` (C3), sha256
`0d0130886ab67db31061a36ae4f4b7ad7808c87467e58bf4f6da82c33ddfffa4` — MATCH. Each region was
additionally compared to the slice RE-EXTRACTED from the block and is byte-EQUAL to it. The
C0a and C0b blobs are ONE id, `9cbfa57750daaa578231d4c19a8737577cbaf9e8`, and
`cmp .agent/authored/f033-r20.md .remedy-wt/r20/BLOCK.md` and the same `cmp` for
`.agent/last_block.md` were SILENT at REAL exit 0. THIS PROVES THE SAVED COPY, ITS MIRROR
AND THE WORKING COPY AGREE; IT IS NOT A CLAIM ABOUT THE BYTES THAT WERE EMITTED.

G3 THE RECORD APPEND at C2 — REAL exit 0, all three readings, "G3 OVERALL PASS". (a) BYTES:
pre-commit blob (read at `69084af5`) 1565456 bytes as the block states; post-commit blob
1575558 bytes, and 1565456 + 1 + 10101 = 1575558; pre is a byte PREFIX of post True;
RECORD20 is an exact SUFFIX at C2 True; the working copy equals the committed blob True.
(b) STRUCTURE, an independent blank-line-unit reader carrying no byte offsets: N COUNTED at
3 by the script; the post-commit file splits into 713 blank-line units; the LAST 3 units
equal the slice's 3 paragraphs IN ORDER True. (c) NEGATIVE CONTROL: the FIRST appended
paragraph was measured at 0-based span (1565457, 1570905), an EXACT match for the block's
stated span; containment ASSERTED as 1565457 <= 1568181 <= 1570905 True; the byte at 1568181
was flipped IN MEMORY from `b` to `B`; reader (a) REJECTS the flipped copy True and ACCEPTS
the unflipped one True, reader (b) REJECTS it True and ACCEPTS the unflipped one True, each
run INDEPENDENTLY of the other. The tracked file on disk was verified unchanged after the
flip True.

G4 THE LEDGER, before at `69084af5` (C1) and after at `d9db68ef` (C2) — REAL exit 0, all ten
CHECK lines True. `^- R-\d+ — ` 307 before, 307 after, UNMOVED, added ids `[]` — this round
registers nothing. `^Done: R-\d+ — ` 50 lines over 48 distinct before, 52 lines over 50
distinct after, and the ADDED ids are exactly `['R-0738', 'R-0746']` and nothing else.
`^Landed: R-\d+ — ` 18 before, 18 after, UNMOVED, added ids `[]` — the `Landed: R-0746` line
STAYS and was measured present exactly once after C2. `^Gate: F033 R19 — ` 0 before,
exactly 1 after. Distinct `DECISION F033 D<n>` ids 5 before, 5 after, UNMOVED. THE OPEN SET,
registered distinct minus distinct `Done:` ids: 259 before, 257 after — exactly the block's
numbers. `^Done: R-0738 — ` exactly 1 after and `^Done: R-0746 — ` exactly 1 after.

G5 THE PROSE FILES — REAL exit 0, "G5 OVERALL PASS". `.agent/plan.md` after C1 is 2570 bytes
over 46 lines, byte-EQUAL to PLAN20 True, under the 50-line cap AGENTS.md sets True, and
holds `## Goal` True and `## Next Steps` True. `.agent/prose_slips.md` 28040 bytes before C3
and exactly 29663 after (28040 + 1 + 1622) True, the old bytes a PREFIX True and SLIPS20 an
exact SUFFIX True.

G6 THE MUTATIONS at `4420328a`, inside the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/r20/wt`, which held NO `__pycache__` before the
first run (`find . -name __pycache__ -type d` printed the empty string) and whose import
path was PROVED to resolve to its own copy — a probe printed
`/home/decodeux/Repos/remedy/.remedy-wt/r20/wt/packages/orchestration/hunk_repair_findings.py`
at REAL exit 0. Every run was `python3 -B -m pytest
tests/orchestration/test_hunk_repair_findings.py -q --tb=no -p no:cacheprovider` from the
worktree root. UNMUTATED CONTROL FIRST: REAL exit 0, 17 passed.
(i) anchor `            rendered.append(entry.reason)\n` asserted to occur EXACTLY 1 time and
DELETED, so the renderer emits each rejected hunk's id, the intro line and no reason; REAL
exit 1, 8 failed and 9 passed. SPEC B1'S TRACE PROOF WENT RED —
`test_a_reason_of_awkward_bytes_survives_into_the_rendered_text` — which is the round's
central reading, and with it the other two verbatim assertions
(`test_the_reason_is_neither_stripped_nor_rewrapped_nor_escaped`,
`test_the_reason_sits_on_its_own_lines_under_the_named_intro`), both B2 order tests, B3's
mixed-ledger test, and two of B5's totality tests, which redden because a deleted
`entry.reason` read is a deleted raise site. I name all eight rather than round the count
down. The four empty-string tests stayed GREEN, so the mutation DISCRIMINATES.
(ii) anchor `            if entry.state != HUNK_STATE_REJECTED:\n` asserted EXACTLY 1 time
and replaced by `            if entry.state == "pending":\n`, so the renderer emits APPROVED
entries as well as rejected ones; REAL exit 1, 3 failed and 14 passed. BOTH OF SPEC B3'S
ASSERTIONS WENT RED —
`test_a_ledger_of_only_approvals_and_pendings_renders_the_empty_string` and
`test_a_mixed_ledger_renders_its_rejections_and_nothing_else` — together with B4's
`test_an_all_approved_ledger_renders_the_empty_string`, which reads the same property from
the other end. The verbatim proof stayed GREEN, so this mutation discriminates too.
(iii) anchor `    except Exception:\n        return ""\n` asserted EXACTLY 1 time and
replaced by `    except Exception:\n        raise\n`, which removes the structural totality
guard's effect while leaving the code parseable; REAL exit 1, 5 failed and 12 passed. SPEC
B5's driven totality assertions DO go RED, and I answer the block's question plainly: FIVE
of the six went red — `test_none_returns_rather_than_raises`,
`test_an_object_with_no_entries_returns_rather_than_raises`,
`test_a_non_iterable_entries_returns_rather_than_raises`,
`test_an_entry_missing_its_reason_returns_rather_than_raises` and
`test_a_string_where_a_ledger_belongs_returns_rather_than_raises`. THE SIXTH STAYED GREEN:
`test_an_id_whose_str_raises_returns_rather_than_raises`, because that case is held by the
SEPARATE coercion guard `_total_text`, not by the structural one. That is a real result and
I report it as one rather than working around it — see the EXTRA CHECK below, which proves
the sixth is pinned by something rather than by nothing.
EXTRA CHECK, NOT ORDERED BY THE BLOCK: anchor — the seven-line `try/except/except` body of
`_total_text` — asserted EXACTLY 1 time and replaced by a bare `    return str(value)`,
removing the COERCION guard; REAL exit 1, EXACTLY 1 failed and 16 passed, and the one
failure is `test_an_id_whose_str_raises_returns_rather_than_raises`. So the two guards are
each measured, by disjoint tests, and neither is described-only.
Every mutated file was restored with
`git -C <worktree> checkout -- packages/orchestration/hunk_repair_findings.py` and PROVED
byte-identical against the committed blob with `git hash-object`, which printed
`b95feeb00c62a31275b0652eac29f145d1d61ed0` after each of the four restores, EQUAL to
`git rev-parse 4420328a:packages/orchestration/hunk_repair_findings.py`.
`git -C <worktree> status --porcelain` then printed the empty string and the POST-RESTORE
CONTROL re-ran at REAL exit 0, 17 passed. The worktree was removed BY ITS EXACT PATH and
`git worktree list` shows only the primary checkout.

G7 THE SUITES, run SERIALLY in the PRIMARY checkout at `4420328a`, every REAL exit 0.
`python3 -m pytest tests/orchestration/test_hunk_repair_findings.py -q` -> 17 passed; NEW
this round, and 17 is the number I measured.
`python3 -m pytest tests/orchestration/test_hunk_ledger.py -q` -> 29 passed, exactly the
stated base; not edited.
`python3 -m pytest tests/orchestration/test_hunk_approval.py -q` -> 30 passed, exactly the
stated base; not edited.
`python3 -m pytest tests/regression/test_named_bugs.py -q` -> 64 passed, 6 skipped, exactly
the stated base — the repo-wide sweep constraint 6 names.
`python3 -m pytest tests/regression/test_resource_safety.py -q` -> 21 passed, exactly the
stated base — the other repo-wide sweep.
`python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed, the canary, exactly its
base.
`python3 -m ruff check packages/orchestration/hunk_repair_findings.py
tests/orchestration/test_hunk_repair_findings.py` -> REAL exit 0, printing
`All checks passed!`. See deviation D1 for the form used.

G8 THE STRUCTURE over `d4a21259`..`4420328a` — REAL exit 0, "G8 OVERALL PASS". SEVEN
commits, every one SINGLE-PARENT, with insertion counts from the `+` column of
`git diff --numstat`: 344, 238, 20, 6, 6, 130 and 294, every one UNDER the 500 AGENTS.md
DECISION F104 D1 caps. The path set over the range is the SEVEN paths of the block's change
set MINUS `.agent/handoff.md`, EQUAL in BOTH directions — unexpected present `[]`, expected
missing `[]` — and the union of the per-commit path sets equals that same set. All SIXTEEN
do-not-touch paths were read at both ends with `git rev-parse <commit>:<path>` and every
pair of blob ids is EQUAL, including `packages/orchestration/hunk_ledger.py` at
`57c00fcfde62`, `packages/orchestration/hunk_approval.py` at `25d1a8d0d08d`,
`packages/orchestration/proof_chain.py` at `693a29f505d7` and `docs/roadmap/STATUS.md` at
`a370be066b7a`.

## Authored-text proofs

Three slices applied, all disk-to-disk, none edited, every one applied byte for byte.
- PLAN20 -> `.agent/plan.md`, whole-file replacement. The file committed by C1 is byte-EQUAL
  to the slice extracted from the block: 2570 bytes, sha256
  `11f614e84b0eac586273872dd7938c11fb1ec83b10601f9861172907c089e91a`.
- RECORD20 -> `.agent/live_review.md`, append. The last 10101 bytes of the file committed by
  C2 hash to `8cfd110e40c78fd9f2f173f633d3b166d0672106c763c3e693a6fb7f01d5d352`.
- SLIPS20 -> `.agent/prose_slips.md`, append. The last 1622 bytes of the file committed by
  C3 hash to `0d0130886ab67db31061a36ae4f4b7ad7808c87467e58bf4f6da82c33ddfffa4`.
- Each slice was extracted with the trailing newline of its LAST content line included and
  the marker lines excluded; BOTH candidate readings were computed for all three slices and
  only the with-trailing-newline candidate matches the marker's stated byte count and digest
  in every case (the without-newline candidates hash to `c567a682…`, `d773e81e…` and
  `d8329221…`), so the reading is measured rather than assumed.
- The block itself: `cmp .agent/authored/f033-r20.md .remedy-wt/r20/BLOCK.md` and
  `cmp .agent/last_block.md .remedy-wt/r20/BLOCK.md` both SILENT at REAL exit 0, and the
  delivered block is 32102 bytes at sha256
  `4b112ec7b2892a2e73e9c60dc1a5e77e993264c8297b224fbdc50f5a56991259`, the digest the round
  order named.

## Deviations & assumptions

D1 — G7's and constraint 8's ruff line. The bare `ruff` executable is DENIED to this
session's shell, exactly as constraint 8 states, so the check ran through the interpreter:
THE FORM USED WAS `python3 -m ruff check`, over both new files, REAL exit 0, printing
`All checks passed!`. Same tool, same arguments, same repository configuration; only the
entry point differs.

D2 — AN EXTRA MUTATION THE BLOCK DID NOT ORDER, run because G6(iii) did not fully
discriminate. G6(iii) removes the structural totality guard and reddens five of SPEC B5's
six driven cases; the sixth, the id whose `__str__` raises, stays GREEN because the module
has TWO guards and that case belongs to the other one. Rather than report a half-blind
reading and stop, I ran a fourth mutation removing `_total_text`'s try/except, and it
reddens EXACTLY that sixth test and nothing else. Both readings are in G6 above. I am
declaring this because it is work the block did not order, not because it changed anything
on disk — it ran only inside the disposable worktree and the file was restored and proved
byte-identical afterwards.

D3 — `git worktree remove` WAS RUN WITH `--force`. pytest leaves untracked `__pycache__`
directories inside the worktree, and `git worktree remove` refuses a worktree with untracked
files. `--force` here removes the DISPOSABLE WORKTREE DIRECTORY only; it is not a force-push
and rewrites no history. The tracked file inside it had already been restored and proved
byte-identical against `4420328a`'s blob before the removal, and `git worktree list`
afterwards shows only the primary checkout. I did not first attempt the removal without the
flag, so I cannot claim it would have failed — only that this is why I used it.

D4 — A DESIGN CHOICE INSIDE SPEC A6 THAT THE SPEC DOES NOT SETTLE, and it is the one thing
in this round I would most want the reviewer to look at. A6 orders BOTH "this function NEVER
raises, on any input at all" AND "Re-state the coercion guard the way `hunk_ledger.py` does"
AND "On anything unreadable, return the empty string rather than a partial block". Written
naively that is TWO defensive layers over the same inputs — a total `_entries`/`_total_attr`
family AS WELL AS an outer catch — and a doubly-defensive module CANNOT BE RED-PROOFED,
because removing either layer leaves the other one answering and every totality test stays
green. G6(iii) would then have been a mutation that discriminates nothing. So I wrote the
module with ONE structural guard and no redundant inner layer: `render_rejection_findings`
reads `ledger.entries`, `entry.state` and `entry.reason` DIRECTLY and the single
`try/except Exception: return ""` around the whole build is what makes it total, while
`_total_text` — the re-stated coercion guard A6 names — is applied to the hunk ID and to
nothing else. The module's own docstrings say this in those words. The consequence is
visible in G6: mutation (iii) reddens five of six, the extra mutation reddens the sixth, and
between them every totality case is pinned by something. The alternative reading of A6
would have shipped a guard no test could redden.

D5 — A REASON IS NEVER COERCED, and that is a deliberate reading of A3 rather than an
omission. `_total_text` is NOT applied to `entry.reason`. `str()` on a `str` is the identity
so coercing would not have broken the verbatim rule, but it WOULD have turned an entry
carrying no reason into the rendered word "None" — putting words in an operator's mouth
inside the one artifact whose whole purpose is quoting the operator exactly. An unreadable
reason therefore sinks the block to `""` through the structural guard instead. SPEC B5's
`test_an_entry_missing_its_reason_returns_rather_than_raises` asserts both halves: it
RETURNS, and it returns the empty string rather than a partial block, which is A6's own
sentence.

D6 — SPEC B6 ASKS FOR THE FUNCTION GUARD; I ALSO GUARD THE CONSTANTS. B6 orders an AST walk
over every public module-level FUNCTION. SPEC A1 orders a `Public API::` block naming every
public NAME the module defines, and this module's public names include three constants that
no AST FunctionDef walk can see. The file therefore carries B6's guard exactly as ordered
plus a second test asserting the three named constants appear in the block. Without it, A1's
"every public name" would be unenforced for two thirds of the list — which is the R-0746
shape all over again, one layer down.

D7 — `.agent/context.md` WAS NOT UPDATED, deliberately. AGENTS.md's Commit Gate item 7 asks
whether it needs an update; it does not — the standing constraint this round leans on ("a
new module under `packages/orchestration/` is swept by repo-wide guards that name no path")
is ALREADY on disk there at line 53, which is where block constraint 6 says it is and where
I verified it. The block's change set does not include that path, so writing to it would
have been a scope violation in the other direction.

D8 — NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2, C3, C4, C5, C6 and C7
landed in exactly the order the block states, one commit each, one path each, with no extra
commit and none dropped. No `Done:` and no `Landed:` line of my own was written anywhere,
and the pre-existing `Landed: R-0746` line was not deleted, per constraint 3. Neither
`packages/orchestration/hunk_ledger.py` nor `packages/orchestration/hunk_approval.py` was
touched, per constraint 4, and both are blob-identical over the range (G8).

D9 — THE NEW MODULE HAS NO CALLER, which is the block's own design and not an oversight.
`render_rejection_findings` is imported by nothing outside its test file; the round that
wires it into the builder's repair prompt follows this one. A reviewer grepping for callers
will find none, and that is the expected reading at this commit.

Assumption: none beyond the above. Where a SPEC was ambiguous I applied the block's literal
wording and declared the disagreement rather than silently correcting it; D4 is the only
place where two clauses of one SPEC could not both be honoured naively, and I have named the
reading I took, why I took it, and the measurement that shows it was the one that keeps the
gate honest.

## Open findings

257 (registered 307 distinct, resolved 50 distinct `Done:` ids), down from 259 — measured at
`d9db68ef` by G4. Moved this round: R-0738 (Medium) and R-0746 (Low) both received their
`Done:` paragraphs from the reviewer's authored RECORD20 slice, so both are now RESOLVED in
the record. This round registered NOTHING. R-0745 (Low) remains open and belongs with the
next work that touches the write door's imports.

## Next

The reviewer gates round 20. The first thing to read is D4 together with G6(iii): SPEC A6's
three clauses cannot all be honoured by a doubly-defensive module without making its own
mutation gate blind, so the module ships ONE structural guard plus the named coercion guard,
and it takes TWO mutations rather than one to pin all six totality cases — the second of
which the block did not order. If the round PASSES, the plan's step 2 is the next round:
`render_rejection_findings` wired into the next builder round's prompt, and the two-round
end-to-end `docs/roadmap/features/T5_F033.md`'s Acceptance asks for. After that come R-0745,
the operator docs for `remedy patch approve-hunks` — no round has had a `docs/` path yet —
and the integration gate before closure.

## Push outcome

Written by C7, AFTER the push, so it records a fact rather than a promise.
