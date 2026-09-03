== STEP closure / F109 — ROUND 21, THE LAST ROUND OF THIS BRANCH ==

SESSION 4 of feature F109. Round 21. Rounds so far: 20 done, this is the 21st.
Soft limit is 25 rounds / 7 sessions (docs/agents/self_drive_protocol.md G7,
amend0827 rule 6); at 21 rounds and 4 sessions it is NOT reached. No line of this
block is a run of a repeated character, so there is no run length to recover
(§3 checklist item 37).

Scope rule, verbatim as every F109 order must carry it:
RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## Goal

CLOSE F109. Closure-protocol algorithm steps 4 and 5: the authored STATUS line
with the README capability sync in the SAME commit, `consumed_by` set to `F109`
on the self-use item this close consumes, the final `.agent/` state, and then the
PR. The package is already READY and its facts are fixed; this round spends them.

## Bundle, in commit order

- C0a  save this block verbatim to `.agent/authored/f109-r21.md`
- C0b  mirror it to `.agent/last_block.md`
- C1   apply PLAN21 to `.agent/plan.md`            (FIRST substantive commit)
- C2   append RECORD21 to `.agent/live_review.md`  (the round 20 verdict)
- C3   THE CLOSURE COMMIT — all five pairs, plus the final `.agent/plan.md` and
       the `.agent/handoff.md` rewrite, in ONE commit. It is the LAST commit on
       this branch (Rule A4).
- then, with NO further commit, create the PR.

## Change set — these paths and nothing else

    .agent/authored/f109-r21.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/roadmap/STATUS.md
    README.md
    scripts/self_use_queue.json
    .agent/handoff.md

## Constraints

1. EVERY slice is applied BYTE FOR BYTE. If a slice looks wrong, apply it
   unchanged and DECLARE it. The closure handback additionally carries GREP PROOF
   that each applied reviewer-authored text is byte-identical to this block's
   slice, which the closure protocol requires by name.
2. RULE A4: the C3 closure commit is the LAST commit on this branch. Nothing
   follows it — no handback commit, no fixup. The `.agent/handoff.md` rewrite is
   INSIDE C3, which is why C3's path set includes it. The ONE permitted successor
   is a commit whose path set is exactly `.agent/candidates.md`, and only if the
   closure gate raises a candidate; you raise none, so do not create one.
3. C3 touches EXACTLY: `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json`, `.agent/plan.md`, `.agent/handoff.md`. README
   and STATUS may never disagree in any committed state, which is why the
   capability sync and the `[x]` flip are ONE commit and not two (R-0154).
4. `.agent/live_review.md` ends WITHOUT a trailing newline: append exactly the two
   bytes `\n\n` then RECORD21, which itself ends without one.
5. `scripts/self_use_queue.json` is edited as TEXT, by the single PAIR Q
   replacement — NOT by a `json.load`/`json.dumps` round trip. Finding `R-0785`
   records that a round trip through `json.dumps` rewrites every non-ASCII byte in
   the file; a text replacement of one unique string touches nothing else.
6. THE PR IS CREATED AND NOT MERGED. It merges at the next feature's start via the
   Open PR Gate — that gap is the operator's manual-review window. Creating it is
   ordered; merging it this session is forbidden.
7. Nothing outside the change set is edited. If the sweep finds something else,
   DECLARE it; do not repair it.
8. `python3 -m pytest` is the pytest route. Env-var assignment and `cp` are
   DENIED: copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`. A
   `bash -c` wrapper around a Python heredoc, and a heredoc with braces adjacent
   to quotes, have both been observed DENIED — write such logic to a scratch `.py`
   under `.remedy-wt/` and run it with `python3 -B`.
9. Never force-push, never work on main.

## SLICE FORTSCHRITT — one line, applied verbatim into the handback's state block

BEGIN FORTSCHRITT
| **Fortschritt** | 100 % (T001-T003 ✅ · Integration Gate ✅ · Self-Use ✅ · Evidence+Zip ✅ · Closure) — Schätzung |
END FORTSCHRITT

## SLICE PLAN21 — the whole of `.agent/plan.md`, applied at C1

BEGIN PLAN21
# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 21, session 4 — THE CLOSURE ROUND, and the last on this branch.
The authored STATUS line flips F109 to accepted with the README
capability sync in the SAME commit, `consumed_by` is set to `F109` on
`SU-005`, and the PR is created but NOT merged: it merges at the next
feature's start through the Open PR Gate, and that gap is the operator's
manual-review window.

## Next Steps

- The operator merges the PR, or the next feature's first session merges
  it at the Open PR Gate.
- Nothing else is owed by this branch.

## Risks

- Three findings from the self-use run are carried as documented Low
  risks, not repaired: `R-0784`, `R-0785` and `R-0786`. Two of them are
  F258's generator and one is F257's queue file, so none is F109's code.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this as its first limit.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
END PLAN21

## SLICE RECORD21 — appended to `.agent/live_review.md` at C2, one paragraph

BEGIN RECORD21
Gate: F109 R20 — the round 20 entry. VERDICT PASS, over the range `a06a6e69..6336513e`. THE PACKAGE IS READY AND THE REVIEWER VERIFIED IT INDEPENDENTLY, not from the handback: `remedy-review-20260903-073602-READY_FOR_REVIEW.zip` exists at `/home/decodeux/Repos/remedy-history/zips`, 20811647 bytes, and its sha256 recomputed by the reviewer is `92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538`, matching the packager's own `final_sha256` exactly. Reading `.review_zip_manifest.json` OUT OF the archive rather than trusting stdout: `package_status` is `READY_FOR_REVIEW`, `committed_review_subject.base_commit` is `5e18a8536afa086b591b5a2e13009d68d6227432` and its `head_commit` is `00084eef9de84b01e207a621d05d9b55378a2abc`, which is C2 — the last CONTENT commit, exactly as the closure protocol's "the zip is built from a clean tree after all CONTENT commits" prescribes — over 3699 members. THE EVIDENCE BUNDLE reached the canonical producer: six verification runs at 130, 54, 27, 20, 13 and 14, each with `len(node_ids) == selected`, zero strings rejected by the packaging scanner with its red control firing on an absolute path, and all six `output_hash` values re-derived as `sha256(stdout_summary)` and matching. Its final verdict is `PASS_WITH_RISKS`, which is what the STATUS line will carry. CLOSURE PRECONDITION 3 IS MET: `run_integrity_checks()` answers `.passed True` with `.fail_count 0` over 5 checks — read through the module because the `remedy` binary is denied in this sandbox, and reported as the attribute it is rather than through a `.get` that would raise. THE THREE SELF-USE FINDINGS ARE REGISTERED AND NONE IS RESOLVED, which is correct and deliberate: `R-0784` is the blocked run precondition 6 required be recorded, `R-0785` is the generator's `ensure_ascii` byte damage and `R-0786` the queue description that denies Remedy appends items, and the latter two are F258's and F257's code respectively, so repairing them from this branch is the scope drift AGENTS.md forbids. They close as DOCUMENTED LOW RISKS. THE OPEN SET IS 279 by set difference over 347 distinct registered ids and 68 distinct resolved. ONE READING THE ROUND HAD TO PIN, and it belongs in this record because a later session will otherwise re-derive it differently: three defensible ways of counting a resolved id over this ledger give 49, 76 and 68, and the reading every figure in this feature has used — and the only one that reproduces them — is the FIRST R-id named by each `^Done: ` line, which is 68. THE ZIP DID NOT LAND WHERE THE BLOCK EXPECTED: the reviewer's own text said it would sit in the repo root under `.gitignore`, and the packager moved it to `/home/decodeux/Repos/remedy-history/zips` itself, outside the repository. The tree stayed clean either way and the ARCHIVED PATH is a real directory rather than `NOT ARCHIVED`, which is what DECISION amend0827 D1 exists to capture; the reviewer's expectation was simply wrong and is corrected here.
END RECORD21

## PAIR S — the STATUS line, in `docs/roadmap/STATUS.md`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE. FROM counted at `6336513e`: exactly 1x. The grammar is copied from the
accepted F106 line directly above it, including the EN DASH in `T001–T003`.

BEGIN PAIRS_FROM
- [~] F109 — Semantic dedupe
END PAIRS_FROM

BEGIN PAIRS_TO
- [x] F109 — Semantic dedupe (T001–T003 complete; accepted 2026-09-03 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f109-closure · package remedy-review-20260903-073602-READY_FOR_REVIEW.zip · SHA-256 92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 00084eef9de84b01e207a621d05d9b55378a2abc)
END PAIRS_TO

## PAIR R1 — the accepted count, in `README.md`

TO contains FROM: false. REWRITE. FROM counted at `6336513e`: exactly 1x.

BEGIN PAIRR1_FROM
67 of 266 registered items accepted.
END PAIRR1_FROM

BEGIN PAIRR1_TO
68 of 266 registered items accepted.
END PAIRR1_TO

## PAIR R2 — the tier table's Done column, in `README.md`

TO contains FROM: false. REWRITE. FROM counted at `6336513e`: exactly 1x.

BEGIN PAIRR2_FROM
| 3 | Full Token Economy & Autonomy | 2 | 26 |
END PAIRR2_FROM

BEGIN PAIRR2_TO
| 3 | Full Token Economy & Autonomy | 3 | 26 |
END PAIRR2_TO

## PAIR R3 — the Tier 3 capability paragraph, in `README.md`

Containment test, run mechanically before emission: TO contains FROM: false. The
new paragraph is inserted BETWEEN the FROM's two parts, so the TO does not contain
the FROM contiguously and this is a REWRITE, not an append — FROM 0x and TO 1x
after C3 is therefore attainable and IS the proof. FROM counted at `6336513e`:
exactly 1x.

BEGIN PAIRR3_FROM
truncated view rather than blocking the run).

Accepted in Tier 5 so far:
END PAIRR3_FROM

BEGIN PAIRR3_TO
truncated view rather than blocking the run).

F109 semantic dedupe (inside a RESUMED provider session, a prompt segment whose
exact content already provably reached that session is replaced by a one-line
"[unchanged: ...]" marker instead of being sent again; the sent-hash index
records only proven sends, a resume fallback forgets the session entirely, a
config kill switch disables the path completely, and a run's own prompt traces
measure what it withheld — 556 characters avoided against 97 spent on markers on
the fixture chain. No concrete adapter resumes in production yet, so the
mechanism is exercised by the suite and inert on real runs today).

Accepted in Tier 5 so far:
END PAIRR3_TO

## PAIR Q — the self-use consumption, in `scripts/self_use_queue.json`

TO contains FROM: false. REWRITE. FROM counted at `6336513e`: exactly 1x — the
four earlier items all carry a non-empty `consumed_by`, so the empty one is
`SU-005` and only `SU-005`. Apply as TEXT, per constraint 5.

BEGIN PAIRQ_FROM
"consumed_by": "",
END PAIRQ_FROM

BEGIN PAIRQ_TO
"consumed_by": "F109",
END PAIRQ_TO

## Done when — the eight gates. RUN each one and record its REAL exit code.

G1 TRANSPORT. `cmp .remedy-wt/f109-r21.md .agent/authored/f109-r21.md`, report the
   exit code; that scratch file is the REVIEWER'S OWN original. Then
   `sha256sum .agent/authored/f109-r21.md .agent/last_block.md` — one digest twice.

G2 THE PLAN AND THE RECORD. `cmp` the delimiter-extracted PLAN21 against
   `.agent/plan.md` after C1: exit 0; `wc -l` under 50; `^## Goal` and
   `^## Next Steps` each 1. Then for RECORD21: base size and sha256 of
   `.agent/live_review.md` at `6336513e`, appended length S, new size, and whether
   base + S equals it; the file still ends WITHOUT a trailing newline; and a
   SECOND READER that splits the whole file on blank-line boundaries and shows the
   LAST N units equal RECORD21's N paragraphs in order, N counted by YOUR script
   from the slice. Report `grep -c '^Gate: F109 R20 — '` = 1.

G3 THE FIVE PAIRS, every one of them a REWRITE by the containment test recorded
   beside it. For PAIR S, R1, R2, R3 and Q report each FROM's count in its target
   BEFORE C3 (each 1) and AFTER C3 (each 0), and each TO's count after C3 (each 1).

G4 THE LEDGER PINS, which are the reason README and STATUS share one commit.
   After C3 report: `grep -c '^- \[x\] F\d\{3\} — '` over `docs/roadmap/STATUS.md`
   = 68; `grep -c '^- \[~\] '` = 0; that `README.md` contains
   `68 of 266 registered items accepted` exactly 1x; and that its tier-3 row reads
   a Done column of 3. Then run `python3 -m pytest tests/docs/ -q` and report the
   collected count and REAL exit code — it was 295 at exit 0 at `6336513e`, and it
   is the suite that pins these counts against each other.

G5 RULE A4 — THE CLOSURE COMMIT IS LAST AND ITS PATH SET IS EXACT. Report
   `git log --oneline` for this round's range showing C3 as the branch tip with
   nothing after it, and `git show --numstat <C3>` naming EXACTLY these five paths
   and no others: `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json`, `.agent/plan.md`, `.agent/handoff.md`.

G6 THE SELF-USE CONSUMPTION, closure precondition 6's last clause. After C3
   report: the queue still holds 5 items; `SU-005`'s `consumed_by` reads exactly
   `F109`; the OTHER FOUR items' `consumed_by` values are unchanged from their
   pre-C3 values, named one by one; `schema_version` still reads 2; and the file
   still parses as JSON. Also report the count of the literal U+2014 character in
   that file before and after C3 — it must be UNCHANGED, which is what constraint
   5's text edit buys and what a `json.dumps` round trip would have destroyed
   (`R-0785`).

G7 THE CANARY AND THE FEATURE'S OWN SUITES, run SERIALLY. Report the collected
   count and REAL exit code of each: `tests/cli/test_golden_path.py` (42),
   `tests/orchestration/test_semantic_dedupe.py` (130),
   `tests/orchestration/test_prompt_trace.py` (54). None may go red and no count
   may move — this round edits no test and no production code.

G8 THE TREE, THE PR AND THE SWEEP. `git status --porcelain` EMPTY and
   `git ls-files .remedy-wt` returning nothing. Push, then create the PR with
   `gh pr create` and report its NUMBER and URL — and do NOT merge it. Report each
   commit's insertion count from `git show --numstat`, the `+` column ONLY, for
   C0a, C0b, C1, C2 and C3, compared cell by cell against your own `## Commits`
   table. Then re-read each file this round touched and report every sentence now
   stale, with the reason.

## The PR

Create it after C3 is pushed. Title: `F109 — Semantic dedupe`. The description
carries, per AGENTS.md's PR workflow: WHAT changed and WHY; the KEY DECISIONS —
that dedupe fires only inside a resumed session, that the kill switch is
consulted first and alone, and that the savings function is a measurement library
with no production caller; HOW TO REVIEW — `docs/system/semantic-dedupe-v1.md`
first, then `tests/orchestration/test_semantic_dedupe.py`; a CHANGED-FILES table;
the LATEST VERDICT and the fact that the integration gate ran with 18937 branch
and 18799 base tests passing and ZERO branch-only failures; the OPEN-FINDINGS
count as a set difference; and the runtime actuals you can observe, with
`not-measured` wherever you cannot — a guess is worse than an admission.

## Handback — inside C3, not after it

`.agent/handoff.md` is rewritten as part of the C3 closure commit. No length cap.
Its STATE BLOCK carries the FORTSCHRITT slice VERBATIM. It must also carry: the
SESSION NUMBER (4) and round (21); the item-status table with C0a, C0b, C1, C2, C3
each appearing exactly once; a per-commit changed-files table; ONE LINE PER GATE
G1 through G8, EXCEPT the PR number: the PR is created AFTER C3 is pushed, so the handback
inside C3 cannot name it. Write "PR created immediately after this commit; number
in the round report" there and report the real number in your reply. Do NOT amend
C3 to insert it — amending a pushed commit is the history rewrite guardrail G2
forbids, and this is exactly the R-0449 shape the checklist warns about; the GREP
PROOF constraint 1 requires; the closure facts (Evidence job, package, SHA-256,
package path, accepted HEAD); the open-finding count as a SET DIFFERENCE; and your
deviations. THIS ROUND'S OWN VERDICT HAS NO ON-DISK GATE ENTRY by construction
(planner_reviewer_prompt.md §4 item 13) — the last round of a branch cannot record
a gate on itself, so its verdict lives in this handback and in the PR, and that
absence is the branch TERMINATOR rather than a missing gate.
