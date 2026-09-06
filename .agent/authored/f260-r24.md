STEP CLOSURE ROUND / F260 — One world: mission, job, run — round 24 of session 8
BRANCH feature/f260-one-world, head 790e6605 at the time this block was written.
THIS IS THE LAST ROUND OF THE BRANCH. Its own verdict lives in the handoff and in
the pull request, never in a ledger entry — §4 item 13, the branch terminator.

Goal
  Close F260. Book round 23's verdict and author the resolution of `R-0817`, then
  flip the STATUS line to `[x]`, sync the README, mark self-use item SU-011
  consumed and rewrite the handback — ALL FOUR IN ONE COMMIT, which is the last
  commit on this branch (Rule A4, R-0154). Then open the pull request and leave it
  UNMERGED as the operator's review window.

The closure inputs, all measured in round 23 and re-verified by the reviewer
  EVIDENCE JOB   017d918464634206
  PACKAGE        remedy-review-20260906-133417-READY_FOR_REVIEW.zip
  SHA-256        0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804
  PACKAGE PATH   /home/decodeux/Repos/remedy-history/zips
  ACCEPTED HEAD  1eb980675b2c553f4aa8b949265eb3b6f30d6964 (round 23's C3)
  The reviewer opened the zip itself: 23950222 bytes, 4015 members, sha256 equal
  to the value above, `package_status` READY_FOR_REVIEW and `validation_errors`
  null in `.review_zip_manifest.json`, spanning that base to that head over 166
  commits and 111 files.

What this round does NOT do
  THE LEDGER ROTATION IS NOT REPEATED. It ran in round 22 at `6cebdce6`, where the
  closure sequence places it — after the verdict bookings and before the STATUS
  flip. The `R-0817` pair this round resolves therefore stays in the live ledger
  and is archived by the NEXT feature's closure rotation, exactly as F259's closure
  left its own last pair. Do not run `scripts/rotate_live_review.py`. And NOTHING
  IS MERGED: the pull request is the operator's review window and it stays open.

Bundle, in this order (one commit each)
  C0a save this block file to .agent/authored/f260-r24.md (copy, never retype)
  C0b mirror it to .agent/last_block.md (same copy route, same source file)
  C1  .agent/plan.md <- PLANF260R24 (whole rewrite). FIRST substantive commit,
      per checklist item 23.
  C2  THE BOOKINGS (§4 item 4). `.agent/live_review.md`: append GATE_R23 then
      DONE0817, in that order, by the recipe below. ONE commit, ONE path.
  C3  THE CLOSURE COMMIT — ONE commit carrying exactly four paths, and the LAST
      commit on this branch:
        docs/roadmap/STATUS.md          the STATUS pair
        README.md                       the COUNT, TIER and LIST pairs
        scripts/self_use_queue.json     the QUEUE pair
        .agent/handoff.md               the rewritten handback
      README and STATUS may never disagree in any committed state, which is why
      they land together (R-0154). Every gate below runs BEFORE this commit is
      staged, so the handback can quote all of them.
  Then push, then create the pull request. NOTHING follows C3 on this branch.

Change set — EXACTLY these paths and nothing else
  .agent/authored/f260-r24.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md (C2) —
  docs/roadmap/STATUS.md, README.md, scripts/self_use_queue.json,
  .agent/handoff.md (C3)

Delivery
  This block is at `.remedy-wt/f260-r24-block.md`, gitignored scratch. C0a COPIES
  that file to .agent/authored/f260-r24.md with `shutil.copyfile`, C0b copies the
  SAME source file to .agent/last_block.md. Never retype either. Slices are
  extracted from the COMMITTED authored file after C0a, by matching lines EXACTLY
  equal to `<<<BEGIN name>>>` and `<<<END name>>>` by position, asserting exactly
  one of each, and joining the lines between them with a newline — so an extracted
  slice carries NO trailing newline of its own.

The C2 append
  `.agent/live_review.md` ends with exactly one newline; assert that from the
  file's OWN measured terminal byte BEFORE writing. Then append, in ONE write: the
  pre-image, a newline, GATE_R23, a blank line, DONE0817, a newline. Both are
  single-line paragraphs and contain no newline of their own.

The closure pairs (C3)
  Each is applied with `str.replace(FROM, TO, 1)` after asserting its FROM occurs
  EXACTLY ONCE in its own target file. The reviewer ran the containment test on
  every one of them before emission and each printed `TO contains FROM: false`, so
  EVERY closure pair is a REWRITE and the obligation for each is FROM 0x and TO 1x
  after the edit. Report the number of pairs you applied — measured by your own
  extraction, not taken from this sentence.
    STATUS_FROM -> STATUS_TO    docs/roadmap/STATUS.md
    COUNT_FROM  -> COUNT_TO     README.md   the accepted-count prose line
    TIER_FROM   -> TIER_TO      README.md   the Tier 2 row of the status table
    LIST_FROM   -> LIST_TO      README.md   the Accepted-in-Tier-2 list
    QUEUE_FROM  -> QUEUE_TO     scripts/self_use_queue.json
  The reviewer simulated them against the real files and confirmed every
  tests/docs pin they touch: README accepted ids stay a subset of the STATUS
  accepted set, the accepted count reads 74 of 272 against a STATUS count of 74,
  every tier row's Done cell equals the ledger-derived count, the ledger still
  holds 272 distinct feature lines, and the queue still parses as JSON with one
  item consumed by F260 and no empty `consumed_by` left.

Constraints
  1. Slices are applied BYTE FOR BYTE from the committed authored file by marker
     extraction in Python. If you believe a slice is wrong, apply it verbatim
     anyway and declare it in the handback.
  2. Read `.agent/STOP` from disk before C0a, before C3 and before the pull
     request. If it exists, finish any half-written commit, write the handback and
     end without creating the pull request.
  3. NEWLINE CONVENTIONS: PLANF260R24 replaces `.agent/plan.md` whole with the
     slice plus exactly one trailing newline; the C2 append is as described above;
     `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` each
     still end with exactly one newline after C3.
  4. NO ID IS MINTED. Exactly one `Done:` line is authored, `Done: R-0817`, and it
     is reviewer-authored text you apply rather than compose. The open set by
     DISTINCT id must go DOWN by exactly one.
  5. C3 IS ONE COMMIT AND IT IS THE LAST ON THE BRANCH. Do not split it, do not
     let any commit follow it, and do not add a fifth path to it.
  6. THE TREE IS CLEAN before C3 is staged and after it is committed. Do not
     rebuild the package, do not run the evidence job again, and do not run the
     ledger rotation.
  7. This session's shell guard refuses some command FORMS outright — shell loops,
     command substitution with parentheses, `$?` inside a compound command,
     `${PIPESTATUS[0]}`, a `$` anchor inside a `grep -c` pattern, an `=` that
     reads as an equals-expansion, and a newline followed by `#` inside a quoted
     argument. Write the Python to a file under `.remedy-wt/` and run that file
     rather than fighting the guard inline. Read every exit code from
     `subprocess.run(...).returncode`. The built `remedy` binary is denied; use
     `python3 -m apps.cli.grouped <...>`.
  8. Commit subjects are `f260: <what>`. No leading-slash token, no absolute path,
     no secret-like string. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
  9. AGENTS.md binds you in full. Never `--force`, never a history rewrite, NEVER
     `gh pr merge`, never a branch deletion, never a commit on `main`.
 10. Helper scripts go under the gitignored `.remedy-wt/` and are never `git
     add`ed. Create no git worktree; nothing this round is destructive.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. EVERY gate runs BEFORE C3 is staged. C3's own insertion count and the
handback's own length are reported NOWHERE — the commit does not exist while the
text inside it is being written (checklist items 14 and 31).

  G1 TRANSPORT. sha256 and byte length of `.remedy-wt/f260-r24-block.md`,
     `.agent/authored/f260-r24.md` and `.agent/last_block.md` — one digest, three
     times — plus `filecmp.cmp(shallow=False)` True for source-vs-saved and
     source-vs-mirror. Measured BEFORE C0a is staged. The delegation states the
     digest; verify against it BEFORE executing anything else in this block.
  G2 THE RECORD. Three readings over `.agent/live_review.md`.
     (a) BYTE: the post-image equals the pre-image followed by a newline, GATE_R23,
         a blank line, DONE0817 and a newline; and the pre-image is a byte-exact
         PREFIX of the post-image. Report both booleans, the byte lengths and the
         delta, and that the file ends in exactly one newline.
     (b) STRUCTURAL, independently of (a): split the WHOLE file image on the regex
         for two-or-more consecutive newlines, drop units empty after stripping,
         strip each surviving unit of leading and trailing newlines. Report the
         unit count before and after. N is COUNTED BY YOUR SCRIPT from the slices'
         own paragraphs; the last N units must equal those paragraphs IN ORDER and
         you report which unit is which.
     (c) NEGATIVE CONTROL, in memory on a `bytes` object and never on disk: pick a
         byte offset your script first ASSERTS lies inside the FIRST appended
         paragraph — GATE_R23, not DONE0817 — XOR it with 0x20, report that
         readers (a) and (b) both REJECT, then restore and report that both ACCEPT
         and the restored image equals the disk image.
     Then the counts before and after: `^Gate: `, `^Gate: R23 — ` and
     `^Done: R-0817 — `; the last two each go from 0 to exactly 1. Then the OPEN
     SET BY DISTINCT ID before and after — distinct ids matching `^- R-\d{4} — `
     minus distinct ids matching `^Done: R-\d{4} — ` — which must go DOWN by
     exactly one. Confirm no new registration line was added.
  G3 THE PLAN. `.agent/plan.md` equals the PLANF260R24 slice plus exactly one
     trailing newline — report the boolean and the byte length; its line count,
     under the AGENTS.md cap of 50; and that it carries `## Goal` and
     `## Next Steps`.
  G4 THE CLOSURE PAIRS, measured on the WORKING TREE after the edits and before
     C3 is staged. For EACH pair report, on one line: the containment reading in
     the words `TO contains FROM: false`, the REWRITE label derived from that
     output, and the FROM count BEFORE (1), AFTER (0) and the TO count AFTER (1).
     Then, per FILE, the boolean that the edited file equals the pre-edit file
     with ONLY that file's pairs applied and nothing else — reconstructed
     independently by your own script — plus its byte length before and after and
     that it still ends with exactly one newline. Report the number of pairs you
     extracted and applied.
  G5 THE DOCS PINS, run on the working tree BEFORE C3 is staged, because this is
     the gate that catches a broken ledger pin while it is still cheap.
     `python3 -m pytest tests/docs/ -q -p no:randomly` — report the count and exit
     code; the reviewer measured 303 at 790e6605 and expects 303 after the edits.
     Then compute and report DIRECTLY, not only through the suite: the count of
     `^- \[x\] F\d{3} — ` lines in `docs/roadmap/STATUS.md`; the two numbers in the
     README's `N of M registered items accepted.` line; the README Tier 2 row's
     Done cell; the boolean that `scripts/self_use_queue.json` parses as JSON with
     exactly one item whose `consumed_by` is `F260` and none left empty; and the
     F260 STATUS line in full as it stands on disk.
  G6 THE CANARY AND INTEGRITY, serially in the primary checkout.
     `python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly` — the
     reviewer measured 42. `python3 -m apps.cli.grouped integrity check --json` —
     report `passed` and `fail_count`. Report the untracked paths and whether each
     is gitignored.
  G7 STRUCTURE AND TREE. `git status --porcelain` EMPTY immediately before C3 is
     staged and again after it is committed; `git ls-files .remedy-wt` returns
     nothing. Every commit single-parent. `git diff --numstat <parent> <commit>`
     reported cell by cell for EACH of C0a, C0b, C1 and C2 — the insertions column
     only, which is the count AGENTS.md DECISION F104 D1 caps at 500, never
     insertions plus deletions. Report `git diff --name-only` over C3 as the
     four paths of the change set and nothing more, and confirm C3 is the branch
     tip with no commit after it. Report the number of marker lines beginning with
     the BEGIN or END prefix that reached any written file, which must be zero in
     each. Report the push result.
  G8 THE PULL REQUEST. Write the PR_BODY slice to a file under the gitignored
     `.remedy-wt/` and create the request with
     `gh pr create --base main --head feature/f260-one-world --title "f260: one world - mission, job, run" --body-file <that file>`.
     Report the PR number and URL; `gh pr view <n> --json state,isDraft,baseRefName,headRefName,mergeable`
     showing state OPEN, isDraft false, base `main`, head `feature/f260-one-world`;
     and the explicit statement that NOTHING was merged and no merge was attempted.
     If a pull request already exists for this branch, do NOT create a second one:
     report that fact and stop.

The handback — rewritten whole INSIDE C3
  No length cap (amend0827 rule 3). It carries: feature, round and SESSION NUMBER
  — SESSION 8 of F260, round 24, rounds so far 24; that this is the LAST round of
  the branch and that its own verdict lives here and in the pull request, never in
  a ledger entry (§4 item 13); the commit range; a `## Commits` table whose cells
  are the numbers G7 printed from `git diff --numstat`, compared cell by cell
  against that tool rather than re-derived by eye (checklist item 28) — C3's own
  row states its four paths and no numbers, because they cannot exist while this
  text is being written; the AGENTS.md item-status table with one row per bundle
  item C0a through C3; one line per gate G1 through G8 with its real reading; the
  closure inputs repeated verbatim from the section at the top of this block; the
  PR number; the deviations; ONE sentence of context self-assessment; and the
  open-findings count after C2. State plainly that the ledger rotation ran in
  round 22 at `6cebdce6` and was deliberately not repeated, and that DECISION F260
  D8 is the authority for closing at the built scope. Repeat this line verbatim in
  its state block:
  `100 % fuer den gebauten Umfang (T001 komplett, T002 Run-Haelfte; Rest per DECISION F260 D8 abgespalten) — Schaetzung`

<<<BEGIN PLANF260R24>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world. Rounds 1 to 23 are reviewed; round 1 FAILED and was
repaired, and 2 to 23 PASSED. DECISION F260 D8 closes this feature at the scope it
built; the follow-up feature registered directly after F260 carries the remainder.

## Goal

Close F260. This is the LAST round of the branch: the STATUS line goes to `[x]`,
the README is synced in the same commit, self-use item SU-011 is marked consumed,
and the pull request is opened and left UNMERGED as the operator's review window.

## Current Step

Round 24 books round 23's verdict and the resolution of `R-0817`, then lands the
STATUS flip, the README capability sync, the `consumed_by` edit and the handback in
ONE commit — the last on this branch (Rule A4) — and opens the pull request. The
ledger rotation ran in round 22 and is not repeated. The evidence job and the
review package were built in round 23 and are not rebuilt.

## Next Steps

1. The operator's review window: the pull request stays OPEN and UNMERGED. It is
   merged at the start of the next feature through the AGENTS.md Open PR Gate, or
   manually by the operator at any time before that.
2. The next feature is the follow-up registered directly after F260 in the ledger,
   which Rule A5 proposes first; it starts in a fresh session.

## Risks

- Nothing may follow the closure commit on this branch. A commit after it breaks
  Rule A4's rendering, which the ledger cross-check pins.
- README and STATUS may never disagree in any committed state, which is why both
  land in the same commit (R-0154).
<<<END PLANF260R24>>>
<<<BEGIN GATE_R23>>>
Gate: R23 — the F260 R23 entry, CLOSURE PART 2 REDONE. VERDICT PASS, AND THE PACKAGE IS READY_FOR_REVIEW. Range `18787ffa`..`790e6605`, six commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4 with nothing added, dropped or reordered; insertion counts 356, 237, 22, 6, 20 and 274, walked commit by commit with `git rev-list --reverse`, every one far under the 500 cap. `git diff --name-only` over the range lists exactly the seven paths of the change set, and `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` appear nowhere in it. THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT: the reviewer's own scratchpad original `.remedy-wt/f260-r23-block.md`, the committed `.agent/authored/f260-r23.md` at `b857e96f` and `.agent/last_block.md` at `39171b42` are all 32879 bytes and all hash to `cf645cb40892a5a37c661098c3b7e382f28b891c2998f5a292c88839ef45169f`, the digest the delegation named before the round began; per §3 item 37 that chain covers the scratch file, the saved copy and the mirror, and is not a claim about the bytes emitted into a prompt. THE RECORD, at `876b4d4f`: `.agent/live_review.md` 939023 to 948369 bytes, delta 9346, equal to its pre-image plus a newline plus GATE_R22 plus a blank line plus FIND0817 plus a newline exactly, with the pre-image a byte-exact prefix; blank-line units 433 to 435; the last two units are GATE_R22 then FIND0817 in that order; `^Gate: R22 — ` 0 to 1 and `^- R-0817 — ` 0 to 1; ZERO lines beginning `Done:` or `Landed:` in the appended region; and the OPEN SET 298 to 299 BY DISTINCT ID, up by exactly one, which is the arithmetic of minting one id and resolving none. `.agent/prose_slips.md` 126730 to 127541 bytes on the same recipe for SLIP27. `.agent/plan.md` at `8aaa7e10` equals its slice plus one newline at 1847 bytes and 39 lines, under the 50-line cap. THE REPAIR OF R-0817, at `1eb98067`: `docs/roadmap/STATUS_closure_protocol.md` 15727 to 17056 bytes under the single PITFALL pair, whose containment test reads `TO contains FROM: true`, making it APPEND-shaped, so the obligation is the §4 item 9 append reading and NOT a FROM-zero count. The reviewer reconstructed the file INDEPENDENTLY from its pre-edit bytes with only that one replacement applied and found it byte-equal to the committed result; the twenty lines that commit's diff ADDS are exactly the pair's TO-only lines IN ORDER, one of them the blank separator; and the producer-pitfall labels now read one each for `(a)`, `(b)`, `(c)`, `(d)` and `(e)`. THE BASE PROOF, WHICH IS THE WHOLE POINT OF THIS ROUND, re-measured by the reviewer over `b5cd6c20782283923f0e276d9479751e475b9359`..`1eb980675b2c553f4aa8b949265eb3b6f30d6964`: `rev-list --ancestry-path` returns 166 and plain `rev-list` returns 166, the two sets IDENTICAL and not merely equal in size; the base is an ancestor of both `main` and the round's own head; and against the product's own `_is_source_for_alignment` predicate the review subject's 111 files are covered by a commit union of 111, leaving ZERO unexplained. Round 22's package failed on exactly that reading at 41 against 158 with 58 unexplained, so this is the same measurement returning the other answer once the base names the fork point. THE PACKAGE, opened and verified by the reviewer from the archive rather than read out of the handback: `remedy-review-20260906-133417-READY_FOR_REVIEW.zip`, 23950222 bytes, 4015 members, sha256 `0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804` recomputed from the file on disk, archived at `/home/decodeux/Repos/remedy-history/zips`; its `.review_zip_manifest.json` reads `package_status` READY_FOR_REVIEW with `validation_errors` null, and its `committed_review_subject` spans that base to that head with `base_is_ancestor` true over 166 commits and 111 files. The evidence job is `017d918464634206`, verdict `PASS_WITH_RISKS`, authority count 73, total passed 303, its one verification run being `tests/docs/` at exit 0 with 303 node ids equal to 303 selected over the two sorted test files. SUITES re-run by the reviewer, serially, in the primary checkout: `tests/docs/` exit 0 at 303 passed, the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed, and `python3 -m apps.cli.grouped integrity check --json` exit 0 with `"passed": true` and `"fail_count": 0`. `git status --porcelain` EMPTY, `git ls-files .remedy-wt` EMPTY, and no pull request existed at `790e6605`. ONE CORRECTION BELONGS TO THE REVIEWER AND IS RECORDED HERE RATHER THAN CHARGED TO THE ROUND: the reviewer's first reading of the append obligation counted the pair's TO-only lines at 19 against the diff's 20 and read them unequal, because that reader dropped the blank separator line; the worker's 20 was right, the recount agrees line for line in order, and the decisive proof was in any case the independent one-replacement reconstruction, which is a total check and does not depend on line accounting at all. SIX ITEMS WERE DECLARED AND ALL SIX ARE UPHELD, including the worker's note that it did not re-measure the block's 41-versus-158 figure at `6cebdce6` — it measured its own range instead, which is the correct scope for a gate, and the reviewer had measured the other at authoring time.
<<<END GATE_R23>>>
<<<BEGIN DONE0817>>>
Done: R-0817 — RESOLVED at `1eb980675b2c553f4aa8b949265eb3b6f30d6964`. The resolution condition this finding carried was that `docs/roadmap/STATUS_closure_protocol.md` carry a producer-pitfall entry stating that `base_commit` is the branch's fork point rather than its merge base, giving the equality of `rev-list --ancestry-path <base>..<head>` and `rev-list <base>..<head>` as the mechanical check that distinguishes them. Entry `(e)` of Algorithm step 1 now states exactly that, names `packages/orchestration/review_subject.py` as the reason the distinction matters and `build_review_manifest.py` as where the failure surfaces, records the measured 41-against-158 with 58 unexplained paths beside the fork point's 160-against-160 with none, and closes on why a branch with no merges makes the two bases coincide — which is the trap that produced the defect, since the F259 precedent whose wording was carried forward had no merge in it. The reviewer verified the landed text by reconstructing the file independently from its pre-edit bytes with only that one pair applied and finding it byte-equal to the committed result, 15727 to 17056 bytes, with the pitfall labels reading one each for `(a)` through `(e)`. THE FIX WAS ALSO EXERCISED, not merely written: round 23 ordered the equality check as the FIRST reading of its evidence gate, before the producer was called, and it returned 166 against 166 with identical sets, after which the package built READY_FOR_REVIEW with `validation_errors` null — so the rule this entry adds is the same rule that turned the blocked closure green one round later. NO CODE CHANGED, and none was asked for: the packaging validator caught a real inconsistency and refused to certify it, which is a gate working rather than a gate to repair, and this finding was always about the protocol's own instructions to the reviewer who feeds that validator.
<<<END DONE0817>>>
<<<BEGIN STATUS_FROM>>>
- [~] F260 — One world: mission → job → run
<<<END STATUS_FROM>>>
<<<BEGIN STATUS_TO>>>
- [x] F260 — One world: mission → job → run (T001 complete and the run half of T002; accepted 2026-09-06 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 017d918464634206 · package remedy-review-20260906-133417-READY_FOR_REVIEW.zip · SHA-256 0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 1eb980675b2c553f4aa8b949265eb3b6f30d6964)
<<<END STATUS_TO>>>
<<<BEGIN COUNT_FROM>>>
73 of 272 registered items accepted.
<<<END COUNT_FROM>>>
<<<BEGIN COUNT_TO>>>
74 of 272 registered items accepted.
<<<END COUNT_TO>>>
<<<BEGIN TIER_FROM>>>
| 2 | Minimal Self-Build Runtime | 16 | 25 |
<<<END TIER_FROM>>>
<<<BEGIN TIER_TO>>>
| 2 | Minimal Self-Build Runtime | 17 | 25 |
<<<END TIER_TO>>>
<<<BEGIN LIST_FROM>>>
them, copied verbatim from the build record).
<<<END LIST_FROM>>>
<<<BEGIN LIST_TO>>>
them, copied verbatim from the build record),
F260 one world: mission, job, run (the ping-pong job record moved under the
one jobs root beside its own evidence; one 16-hex id shape, minted by one
function per kind, at its call sites; both job-id resolvers returning `str`;
the ping-pong run store and the job-keyed run-log store each given one
spelling in `data_paths`; and a run made an invocation rather than an event.
The run re-key, the eleven named consumers, the classic cycle runner and the
prototype-cluster deletion were split off at the seven-session soft limit and
belong to the follow-up feature the STATUS ledger registers directly after
it).
<<<END LIST_TO>>>
<<<BEGIN QUEUE_FROM>>>
"consumed_by": ""
<<<END QUEUE_FROM>>>
<<<BEGIN QUEUE_TO>>>
"consumed_by": "F260"
<<<END QUEUE_TO>>>
<<<BEGIN PR_BODY>>>
## What changed

F260 gives Remedy ONE world for a job. Before it, a job existed in two shapes —
`<data_root>/jobs/<uuid>.json` and `<data_root>/task_jobs/<16-hex>/job.json` —
minting different id shapes, so `resolve_job_id` could never resolve a task-job id
and `remedy teach narrate <task-job-id>` answered "no job matches prefix" for a
job whose run log was on disk the whole time. Landed here:

- **T001, complete.** The inventory in `.agent/f260_inventory.md` measured both
  writers, the three id shapes actually minted, and the four kinds of thing the
  16-hex shape names. DECISION F260 D1 rules the record layout; D2 rules the
  16-hex id shape with ONE minting function per kind, at its call sites.
- **The run half of T002.** The ping-pong job record moved under the one jobs
  root beside its own evidence; both job-id resolvers return `str`; the ping-pong
  run store and the job-keyed run-log store each have ONE spelling in
  `data_paths` across the production side; and a run is an INVOCATION rather than
  an event (DECISION F260 D7, measured on disk by finding R-0816).

## Why it stops here

DECISION F260 D8 (2026-09-06) closes F260 at the scope it built. The feature
reached the SESSION half of the amend0905-throughput soft limit — seven sessions
— at round 17, so the constraint that ended it was wall clock, not scope creep:
every round from 2 to 23 passed, one failed and was repaired, and none was spent
reworking its own earlier work. The remainder — `Job.run_refs`, the re-key of the
run directory onto a RUN id, the unified record's administrative fields, the
Mission extension, the eleven named consumers, the classic cycle runner and the
prototype-cluster deletion — is registered as the follow-up feature placed
directly after F260 in the ledger, per operator order amend0906-split-placement,
so Rule A5 proposes it before any other unchecked feature. The Orchestrator brief
anticipated a split between T003 and T004; the limit arrived during T002, so the
split falls EARLIER than the brief allows and the brief is amended rather than
obeyed. Its prohibition on splitting inside T005 is untouched and binds the
follow-up, because a half-performed deletion is the one state this must never
leave behind.

## Key decisions

- **F260 D1 / D2** — the record layout, and the 16-hex id shape with one minting
  function per kind. **F260 D7** — a run is an invocation, not an event.
- **F260 D8** — split-and-close at the soft limit, executed on the session's own
  authority under amend0905-throughput, reversible by the recipe it carries.
- **R-0817**, raised and resolved inside this closure: the closure protocol's
  producer-pitfall list never said WHICH commit `base_commit` must be, only that
  it must be full-length. On a branch that has merged `main` in, `git merge-base`
  names main's own tip rather than the fork point, and the packaged chain — built
  with `rev-list --ancestry-path` — then drops every commit made before that merge
  while the diff still carries their effect. The first package built
  BLOCKED_EVIDENCE for exactly that reason. Entry `(e)` of Algorithm step 1 now
  states the rule and gives the mechanical check.

## How to review — the package is the intended entry point

- Evidence job `017d918464634206`; package
  `remedy-review-20260906-133417-READY_FOR_REVIEW.zip` at
  `/home/decodeux/Repos/remedy-history/zips`, SHA-256
  `0f87ce8e9c4c506f82a6eb401deb6d85fb6ad1b3f7b066ad35808ca3df21c804`
- Accepted head `1eb980675b2c553f4aa8b949265eb3b6f30d6964`; review base
  `b5cd6c20782283923f0e276d9479751e475b9359` — the branch's fork point, over
  which `rev-list --ancestry-path` and plain `rev-list` both return 166 and the
  commit union covers all 111 subject files with none unexplained.

To re-derive the verdict rather than read it: `python3 -m pytest tests/docs/ -q`,
`python3 -m pytest tests/cli/test_golden_path.py -q`, and
`python3 -m apps.cli.grouped integrity check --json`. The full suite ran twice per
the verification tiers — the integration-gate round at R19 and the closure
confirmation — and the ledger entries `Gate: R1` through `Gate: R23` in
`.agent/live_review.md` carry each round's own readings.

## Changed files in this closure commit — one commit, last on the branch (Rule A4)

| Path | Why |
|---|---|
| `docs/roadmap/STATUS.md` | the `[x]` line with the evidence, package and accepted-head segments |
| `README.md` | the accepted count, the Tier 2 Done cell and the Tier 2 capability entry — same commit as STATUS, because the two may never disagree in any committed state (R-0154) |
| `scripts/self_use_queue.json` | `consumed_by` set to `F260` on SU-011, closure precondition 6 |
| `.agent/handoff.md` | the final handback |

## Verdict, open findings, runtime actuals

Latest live-review verdict: **PASS** on round 23, recorded as `Gate: R23` in
`.agent/live_review.md`. Rounds 2 through 23 passed; round 1 failed and was
repaired. Open findings after this closure: **298 by distinct id**, carried
forward and not hidden — `R-0817` was raised and resolved inside this closure,
and the self-use run's two defect strings were registered as a RECURRENCE of the
already-open `R-0784` rather than as a new id, because that finding already
describes the same defect and a second id would be a second thing to resolve.

Rounds 24, sessions 8. Wall clock, models, tokens and cost are `not-measured` —
the ledger does not carry them for this feature, and a guess is worse than the
absence. Self-use item consumed by this close: `SU-011`.

This request is NOT merged by the session that opened it. It is the operator's
manual-review window, and it merges at the start of the next feature through the
AGENTS.md Open PR Gate — or manually, at any time.
<<<END PR_BODY>>>
