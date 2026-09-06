# Handoff — F260 One world · round 23 · CLOSURE PART 2 REDONE · PACKAGE READY_FOR_REVIEW

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE
(the banner announces the REPORT, not a stop — amend0905-throughput)

Round 22's package built `BLOCKED_EVIDENCE` because the block ordered the wrong
`base_commit`. This round booked that verdict, registered the docs gap as `R-0817`,
repaired the gap in `docs/roadmap/STATUS_closure_protocol.md`, and rebuilt the
evidence bundle and the review zip from the branch's FORK POINT. **The package is
`READY_FOR_REVIEW` with `validation_errors: null`.** No base, no evidence field and
no source file was adjusted to get there — the base proof was measured BEFORE the
producer was called and it passed on its own.

## Session

SESSION 8 of feature F260 · round 23 · rounds so far 23

`.agent/STOP` was read from disk with `os.path.exists` before C0a (**False**),
before C3 (**False**) and before this handback (**False**).

Context self-assessment (amend0905-throughput): context is comfortable — this round
is five small commits plus two tool runs, and nothing about it pressed the margin.

F260 IS PAST ITS 7-SESSION SOFT LIMIT. **DECISION F260 D8** (2026-09-06, round 17)
is the standing authority for closing this feature at the scope it built, with F272
carrying the remainder; that decision is unchanged by this round.

`~99 % (T001 komplett, T002 Run-Haelfte, Integration Gate gruen, Evidence + Zip neu gebaut, nur noch STATUS/README/PR) — Schaetzung`

## THE CLOSURE ROUND'S INPUTS — the measured values the next round needs

Named here so a later reader finds them BY NAME. The closure round authors the
STATUS line from exactly these.

| Name | Value |
|---|---|
| EVIDENCE JOB ID | `017d918464634206` |
| PACKAGE FILENAME | `remedy-review-20260906-133417-READY_FOR_REVIEW.zip` |
| PACKAGE SHA-256 (as the script printed it) | `0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804` |
| PACKAGE SHA-256 (recomputed from the file on disk) | `0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804` — **equal** |
| PACKAGE ABSOLUTE DIRECTORY | `/home/decodeux/Repos/remedy-history/zips` |
| ACCEPTED HEAD | `1eb980675b2c553f4aa8b949265eb3b6f30d6964` (full sha of C3; the head the manifest recorded) |
| PACKAGE_STATUS | `READY_FOR_REVIEW` |
| REVIEW BASE | `b5cd6c20782283923f0e276d9479751e475b9359` — the branch's fork point |

The two SHA-256 readings are byte-equal, so the package on disk is the package the
script reported. The package is 23 950 222 bytes and carries 4015 members. The
manifest `.review_zip_manifest.json` records `committed_review_subject` base
`b5cd6c20782283923f0e276d9479751e475b9359` and head
`1eb980675b2c553f4aa8b949265eb3b6f30d6964`, `base_is_ancestor` **true**,
`commit_count` **166**, `file_count` **111**, `tombstones` **[]**, and
`validation_errors` **null**. The evidence directory was FRESH and gitignored:
`.remedy-wt/f260-r23-evidence-017d918464634206`, not the directory round 22 used.

THE LEDGER ROTATION ALREADY RAN IN ROUND 22, AT `6cebdce6`, AND IS **NOT** REPEATED
HERE. `.agent/live_review_archive.md` is untouched by this round.

## Commits

Range `18787ffa`..`HEAD`. Every commit single-parent. The insertion and deletion
cells below are the numbers `git diff --numstat <parent> <commit>` printed in G8,
compared cell by cell against that tool rather than re-derived by eye.

| Item | SHA | Subject | Path | Ins | Del |
|---|---|---|---|---|---|
| C0a | `b857e96f` | f260: save the round 23 step block as the authored original | `.agent/authored/f260-r23.md` | 356 | 0 |
| C0b | `39171b42` | f260: mirror the round 23 step block into the last block state file | `.agent/last_block.md` | 237 | 171 |
| C1 | `8aaa7e10` | f260: point the plan at the round 23 repair and package rebuild | `.agent/plan.md` | 22 | 19 |
| C2 | `876b4d4f` | f260: book the round 22 verdict and register the closure base gap | `.agent/live_review.md` | 4 | 0 |
| C2 | `876b4d4f` | (same commit) | `.agent/prose_slips.md` | 2 | 0 |
| C3 | `1eb98067` | f260: state in the closure protocol that the evidence base is the fork point | `docs/roadmap/STATUS_closure_protocol.md` | 20 | 0 |
| C4 | this commit | f260: hand back the round 23 package rebuild | `.agent/handoff.md` | not reported | not reported |

C4's own insertion count and byte length are reported NOWHERE, as the block orders:
under self-drive there is no round report and the reviewer measures those at the
next gate. Every insertion cell above is far under the AGENTS.md DECISION F104 D1
cap of 500, which counts INSERTIONS ONLY, so no oversize declaration is needed.

## Item status

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## Gates — one line each, real exit codes and real readings

**G1 TRANSPORT — PASS.** One digest three times: `.remedy-wt/f260-r23-block.md`,
`.agent/authored/f260-r23.md` and `.agent/last_block.md` are each **32879** bytes and
each hash to `cf645cb40892a5a37c661098c3b7e382f28b891c2998f5a292c88839ef45169f`, which
is the digest the delegation named and which was verified against the source file
before anything else in the block was executed; `filecmp.cmp(shallow=False)` is
**True** for source-vs-saved and **True** for source-vs-mirror; both measured before
C0a was staged, and both saves are `shutil.copyfile` of the same source, never
retyped.

**G2 THE RECORD — PASS.** `.agent/live_review.md`, at C2 `876b4d4f`:
(a) BYTE — post equals pre + newline + GATE_R22 + blank line + FIND0817 + newline
**True**; pre is a byte-exact PREFIX of post **True**; **939023** → **948369** bytes,
delta **9346**; ends in exactly one newline **True**.
(b) STRUCTURAL, computed independently by splitting the whole image on `\n{2,}`,
dropping units empty after stripping and stripping each survivor of leading and
trailing newlines — unit count **433** before, **435** after; N = **2**, counted by
the script from the slices' own paragraphs and not taken from the block; unit[-2] is
GATE_R22 (equal **True**), unit[-1] is FIND0817 (equal **True**), and the last 2
units equal those paragraphs IN ORDER **True**.
(c) NEGATIVE CONTROL, in memory on a `bytes` object and never on disk — offset
**939224** was first ASSERTED to lie inside the FIRST appended paragraph (GATE_R22
occupies bytes 939024..945360, and that byte range was asserted equal to the GATE_R22
slice); the byte `'b'` XOR 0x20 became `'B'`; reader (a) REJECTS **True** and reader
(b) REJECTS **True**; after restoring, reader (a) ACCEPTS **True**, reader (b)
ACCEPTS **True**, and the restored image equals the disk image **True**.
`.agent/prose_slips.md`: pre is a byte-exact prefix **True**, the remainder equals
newline + SLIP27 + newline **True**, **126730** → **127541** bytes (delta **811**),
ends in exactly one newline **True**, unit count **157** → **158**, last unit equals
the SLIP27 paragraph **True**.
LEDGER COUNTS before → after: `^Gate: ` **21 → 22**; `^Gate: R22 — ` **0 → 1**;
`^- R-0817 — ` **0 → 1** — the last two each 0 to exactly 1.
OPEN SET BY DISTINCT ID before → after: distinct `^- R-\d{4} — ` ids **300 → 301**
minus distinct `^Done: R-\d{4} — ` ids **2 → 2**, so the open set is **298 → 299** —
it ROSE BY EXACTLY ONE. Lines matching `^Done:` in the appended region: **0**; lines
matching `^Landed:`: **0**. (See deviation 2 for the one bare `Done:` substring.)

**G3 THE PLAN — PASS.** `.agent/plan.md` equals the PLANF260R23 slice plus exactly one
trailing newline **True**, measured length **1847** bytes; **39** lines, under the
AGENTS.md cap of 50 **True**; exactly one `## Goal` and exactly one `## Next Steps`.

**G4 THE PITFALL PAIR — PASS.** Containment measured here, not taken from the block:
`TO contains FROM: true` — so the label derived from that output on this same line is
**APPEND**. FROM count BEFORE **1**; post equals pre with that ONE replacement applied
and nothing else **True**; **15727** → **17056** bytes (delta **1329**); still ends
with exactly one newline **True**. The APPEND obligation, not a FROM-zero count: of
the **20** TO-ONLY lines, every one occurs exactly ONCE among the added lines, and
`git show --numstat` reports `20 0 docs/roadmap/STATUS_closure_protocol.md` while
`git show` yields exactly **20** added lines — the added lines are exactly the TO-ONLY
lines, in order (**True**). FROM still occurs **1** time after the edit, which is what
an append-shaped pair requires and is NOT reported as a defect. In the producer-pitfall
region — lines **65..110**, from the `Producer pitfalls that block packaging` line up
to but excluding the `2. **Review zip` line — the literal `(e) ` occurs **exactly 1**
time and the labels `(a)`, `(b)`, `(c)` and `(d)` each occur **exactly 1** time.

**G5 THE EVIDENCE JOB — PASS.** THE BASE PROOF RAN FIRST, before the producer was
called: with base `b5cd6c20782283923f0e276d9479751e475b9359` and head
`1eb980675b2c553f4aa8b949265eb3b6f30d6964`, `git rev-list --ancestry-path <base>..<head>`
counts **166** (exit 0) and `git rev-list <base>..<head>` counts **166** (exit 0) —
THE TWO ARE EQUAL **True**, and the commit SETS are identical too. The base is an
ancestor of `main` **True** (exit 0), of `origin/main` **True** (exit 0) and of the
head **True** (exit 0). `git status --porcelain` was EMPTY immediately before the run
and EMPTY immediately after it. The verification run is REAL: `python3 -m pytest
tests/docs/ -q` exit **0**, `303 passed in 0.49s`, so passed 303, failed 0, skipped 0,
deselected 0, selected **303**; `--collect-only` of the SAME selection returned
**303** node ids, so `len(node_ids) == selected`; `test_files` is the sorted FILE list
`['tests/docs/test_docs_consistency.py', 'tests/docs/test_vocabulary.py']`, never a
directory; `run_id` `vr-1788694440` matches `vr-\d{4,}`; `stdout_summary` is **420**
characters, under 4000; `output_hash`
`54ee3d3888b1c4ccead127b3538b2fe188504221b685cfbd99bdd680e539a486` is the sha256 of
exactly that string. No full-suite node-id list is recorded anywhere in the bundle.
The returned summary dict in full:

    {"job_id": "017d918464634206",
     "head_commit": "1eb980675b2c553f4aa8b949265eb3b6f30d6964",
     "authority_count": 73,
     "partition": {"T001": 25, "T002": 25, "T003": 23},
     "commit_count": 166,
     "verdict": "PASS_WITH_RISKS",
     "manual_completion": true,
     "operator_attested_tasks": ["T001", "T002", "T003"],
     "total_passed": 303}

Job id `017d918464634206`; the final verdict it names is **PASS_WITH_RISKS**.

**G6 THE REVIEW ZIP — PASS, READY_FOR_REVIEW.** `git status --porcelain` EMPTY first
and the branch pushed (`HEAD` and `origin/feature/f260-one-world` both
`1eb980675b2c553f4aa8b949265eb3b6f30d6964`). `bash scripts/make_review_zip.sh
--evidence-dir /home/decodeux/Repos/remedy/.remedy-wt/f260-r23-evidence-017d918464634206`
exited **0**. Its closing report, verbatim:

    {"member_count": 4015, "authoritative_count": 73, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260906-133417-READY_FOR_REVIEW.zip", "final_sha256": "0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "03ad88562f4583b13e88b41257883141daba48b6bc1521d95f89fdeb48147e40"}

    ============================================
    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    PACKAGING_CWD=/home/decodeux/Repos/remedy
    EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/f260-r23-evidence-017d918464634206
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
    ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260906-133417-READY_FOR_REVIEW.zip
    ============================================

    ZIP CREATED AND READY FOR FINAL REVIEW

    23M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260906-133417-READY_FOR_REVIEW.zip
    Included files: 4015
    Branch: feature/f260-one-world
    Commit: 1eb980675b2c553f4aa8b949265eb3b6f30d6964
    Evidence: evidence/current/

PACKAGE FILENAME `remedy-review-20260906-133417-READY_FOR_REVIEW.zip`; SHA-256
`0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804` as the script
printed it AND as recomputed from the 23 950 222-byte file on disk, **equal**;
ABSOLUTE DIRECTORY `/home/decodeux/Repos/remedy-history/zips`; `PACKAGE_STATUS`
**READY_FOR_REVIEW**; the manifest's `committed_review_subject` spans base
`b5cd6c20782283923f0e276d9479751e475b9359` .. head
`1eb980675b2c553f4aa8b949265eb3b6f30d6964`, exactly the ordered range, with
`validation_errors` **null**. Constraint 11 was never reached — nothing was adjusted
to make the package go READY. See deviation 1 on the extent of the captured stdout.

**G7 THE PRECONDITIONS — PASS, run SERIALLY in the primary checkout.**
`python3 -m pytest tests/docs/ -q -p no:randomly` exit **0**, `303 passed in 0.49s` —
**303**, the same number the reviewer measured at `18787ffa`, so C3's edit to a file
that suite reads changed no count.
`python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly` exit **0**,
`42 passed in 21.39s` — the canary at the expected **42**.
`python3 -m apps.cli.grouped integrity check --json` exit **0**, `"passed": true`,
`"fail_count": 0`.
`git status --porcelain` exit 0 and EMPTY; with `--untracked-files=all` the untracked
list is **empty (0 paths)**, because every scratch artifact this round produced sits
under `.remedy-wt/`, which `git check-ignore -v` resolves to `.gitignore:235:.remedy-wt/`
for `.remedy-wt/`, `.remedy-wt/r23/`, `.remedy-wt/f260-r23-block.md` and
`.remedy-wt/f260-r23-evidence-017d918464634206/` alike — all four gitignored.

**G8 STRUCTURE AND TREE — PASS.** `git status --porcelain` EMPTY immediately before
C4 was staged; `git ls-files .remedy-wt` returns nothing. All five prior commits are
single-parent (parents=1 each), and the `git diff --numstat <parent> <commit>` cells
are the table above: C0a 356/0, C0b 237/171, C1 22/19, C2 4/0 and 2/0, C3 20/0 —
insertions column only, which is the count AGENTS.md DECISION F104 D1 caps at 500,
never insertions plus deletions, and every one of 356, 237, 22, 4, 2 and 20 is under
that cap. `git diff --name-only 18787ffa..HEAD` lists exactly the six change-set
paths; `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are
named NOWHERE in this round's diff (**False** for each). Push: `18787ffa..1eb98067
feature/f260-one-world -> feature/f260-one-world`, and `origin/feature/f260-one-world`
equals HEAD. NO pull request was created — `gh pr list --state open` returns `[]`.
Marker lines beginning with the BEGIN or END prefix that reached a written file:
`.agent/plan.md` **0**, `.agent/live_review.md` **0**, `.agent/prose_slips.md` **0**,
`docs/roadmap/STATUS_closure_protocol.md` **0**.

## Deviations

1. **G6's "report the full stdout" is reported as its closing section, not its whole
   transcript.** `scripts/make_review_zip.sh` was run once and its output was read
   through `tail -60`, so the earlier evidence-refresh progress lines were not
   retained. Every field G6 names by name — filename, both SHA-256 readings, absolute
   directory, `PACKAGE_STATUS`, and the manifest's base and head — is present above
   and was re-measured from the file on disk. The build was NOT repeated to recover
   the missing lines, because a second run would place a second READY package in the
   archive directory and leave the closure round ambiguous about which package it is
   closing against; a declared reporting gap is the smaller cost. Declared rather than
   quietly rounded off.
2. **One bare `Done:` substring exists in the appended ledger region and it is not a
   `Done:` line.** It sits inside GATE_R22's own prose, in the backticked pattern
   `` `^Done: R-dddd — ` `` (spelled with a literal `d`, not `\d`, by the reviewer),
   at offset 2490 of the appended region. Lines matching `^Done:` in that region:
   **0**. Lines matching `^Landed:`: **0**. No `Done:` or `Landed:` line was authored,
   as constraint 4 requires.
3. **Constraint 1 — no slice was believed wrong.** All six slices (PLANF260R23,
   GATE_R22, FIND0817, SLIP27, PITFALL_FROM, PITFALL_TO) were extracted from the
   COMMITTED `.agent/authored/f260-r23.md` by exact-position marker matching, with
   exactly one BEGIN and one END asserted for each, and applied byte for byte. Nothing
   was edited, reflowed or corrected.
4. **A note, not a change: the block's diagnosis reproduces at this head.** The block
   states that from `f957c4c6` the ancestry chain was 41 against a plain `rev-list` of
   158. At this round's head the fork-point base gives **166 against 166** — equal, as
   the block predicted the correct base would. The block's numbers were not re-checked
   at `6cebdce6`, since the base proof this round needed was the one over its own
   range and that one passed.
5. **`git check-ignore -v <path>` followed by `echo "exit=$?"` was refused by this
   session's shell guard**, verbatim: `Permission to use Bash has been denied.` — the
   `$?` inside a compound command, exactly as constraint 8 warned. Every exit code
   above was therefore read from `subprocess.run(...).returncode` in a Python file
   under `.remedy-wt/r23/`, never from a word. The scripts run were
   `g1_transport.py`, `c1_plan.py`, `c2_record.py`, `g2_done_check.py`,
   `c3_pitfall.py`, `g4_added_lines.py`, `g5_base_proof.py`, `g5_evidence.py`,
   `g6_verify.py`, `g6_manifest.py`, `g7_preconditions.py` and `g8_structure.py`; none
   was ever `git add`ed and `git ls-files .remedy-wt` is empty.
6. **No git worktree was created and nothing destructive ran**, per constraint 12.
   `.agent/live_review_archive.md` was not touched: the rotation ran in round 22 at
   `6cebdce6` and is not repeated.

## Next expected action

1. **THE REVIEWER'S GATE on round 23** — re-run G1 through G8 independently. Note
   that `.agent/live_review.md` now carries the `Gate: R22` record and the `R-0817`
   registration, and that NO `Done: R-0817` line was authored: only the reviewer sets
   Resolved, at the next gate.
2. **THEN THE CLOSURE ROUND.** Book round 23's verdict and author `Done: R-0817`;
   then, in ONE commit, the `docs/roadmap/STATUS.md` `[x]` flip for F260, the README
   capability sync and `consumed_by: F260` on SU-011 in `scripts/self_use_queue.json`
   (R-0154 requires the three together); then the handback; then the pull request,
   which is created but **NOT merged this session** — it is the operator's review
   window. The STATUS line is authored from the values in the inputs table above:
   evidence job `017d918464634206`, package
   `remedy-review-20260906-133417-READY_FOR_REVIEW.zip`, SHA-256
   `0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804`, archived at
   `/home/decodeux/Repos/remedy-history/zips`, accepted head
   `1eb980675b2c553f4aa8b949265eb3b6f30d6964`.
3. Phase 1 rule 1 before rule 2: re-read `.agent/STOP` from disk first; there is no
   open pull request (`gh pr list --state open` returned `[]`).
