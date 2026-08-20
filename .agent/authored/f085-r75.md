── STEP VERDICT RECORD — F085 · R75 ────────────────────────────────
Goal:        Land the reviewer's closing verdict for R74 — the last round of this branch, whose
             verdict lives in `.agent/handoff.md`, the round report and the PR and never in
             `.agent/live_review.md` (docs/agents/planner_reviewer_prompt.md §4 item 13) — and carry
             the one candidate this gate raised into `.agent/candidates.md`.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 append CAND2 to the
candidate carrier · C2 append VERDICT to the handoff · THE PUSH · THE PR COMMENT.

Change:      exactly these paths and nothing else —
             `.agent/authored/f085-r75.md` (new, C0a — a byte COPY of this block)
             `.agent/last_block.md` (C0b, verbatim rewrite, AGENTS.md DECISION F104 D1 exempt)
             `.agent/candidates.md` (C1, CAND2 appended at EOF)
             `.agent/handoff.md` (C2, VERDICT appended at EOF)
             `.agent/plan.md` is deliberately NOT touched and this block says so rather than leaving
                 you to discover it: its Current Step already names R74 as the closure round and both
                 its Next Steps stay true after this round, so AGENTS.md's Commit Gate item 1 is met
                 without an edit. Nothing here registers, resolves or renumbers a finding, so
                 docs/agents/planner_reviewer_prompt.md §3 checklist item 23 does not bind.
             `docs/roadmap/STATUS.md`, `README.md` and `.agent/live_review.md` are NOT touched. F085
                 is already `[x]`, and item 13 forbids a live_review gate entry for this round.

CONVENTION, binding on every count and proof here, carried verbatim in force from the R74 block. A
line count is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES
STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT
LINE: extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so `pre + slice` is already newline-terminated and NO joiner and
NO terminator byte is ever added. THIS BLOCK HAS NO FROM/TO PAIR. ITS APPENDS AT END OF FILE ARE
CAND2 AND VERDICT. PRCOMMENT IS APPLIED TO NO FILE — it is the body of a PR comment.

TRANSPORT, the in-session shape (docs/agents/self_drive_protocol.md Phase 2 item 1): there is no
paste relay in this session, so this block already exists on disk at `.remedy-wt/r75/block.md`, which
is gitignored reviewer scratch and never enters the repository tree. C0a is a byte COPY of that file
— never a retype — and the hash-stamp ritual is replaced by the disk-to-disk equality G2 orders.

Constraints:
 1. Apply every slice BYTE-VERBATIM, extracted programmatically from the committed
    `.agent/authored/f085-r75.md` by marker pair under the CONVENTION. Edit no slice. No slice
    carries a substitution slot and no substitution is permitted anywhere.
 2. Re-read `.agent/STOP` from disk immediately before C0a and again immediately before C2. If it
    exists at either point, finish only the commit in flight, report, and stop.
 3. Commit in exactly the order C0a, C0b, C1, C2. C2 is the LAST commit on the branch.
 4. `git status --porcelain` is EMPTY after every commit. Any destructive check runs only in a
    disposable worktree under `.remedy-wt/`, removed and pruned before you report.
 5. Never force-push. NEVER MERGE PR #204 and never close it. It merges at the next feature's Open
    PR Gate, which is the operator's manual-review window.
 6. This round's handback IS the VERDICT slice plus the ROUND REPORT you return in your reply. Do
    NOT rewrite `.agent/handoff.md`: a rewrite would delete the reviewer text this whole round exists
    to land, and the appended VERDICT section carries the mandated handback fields itself. This is
    the §4 item 13 terminator, and the deviation is authorised here in writing rather than left for
    you to discover.
 7. Author no `Done:` and no `Gate:` text of your own. Those are reviewer-authored strings.
 8. REPORT DISAGREEMENT, DO NOT FIX IT. If any number, path, quotation or claim here contradicts what
    you measure, record BOTH readings in the round report and change no slice.

## THE PUSH — after C2

    git status --porcelain          # must be EMPTY
    git push

## THE PR COMMENT — after the push, last action of the round

Post the PRCOMMENT slice verbatim as a comment on PR #204:

    gh pr comment 204 --body-file <a file under .remedy-wt/ holding the PRCOMMENT slice>

Write that body file under the gitignored `.remedy-wt/` and never into the repository tree. Report
the comment URL. Do not merge, do not close, and do not edit the PR body or its title.

Done when — run each gate, record its REAL exit code and real output, never a colour you did not see:

 G1 STATE. `.agent/STOP` absent at the two points constraint 2 names. `git status --porcelain` empty
    after every commit. `git worktree list` one line at the start and one at the end.
 G2 TRANSPORT. After C0b, sha256 over all four of `.remedy-wt/r75/block.md`, the committed
    `.agent/authored/f085-r75.md`, the committed `.agent/last_block.md` and the working
    `.agent/last_block.md` — all four MUST be equal. Report the digest, byte size and line count.
    Report the count of lines beginning `BEGIN-` or `END-`, and report each slice's measured line
    count and sha256. Budget: TOTAL is the line count and must be ≤ 490 (DECISION F085 D6); PROSE is
    TOTAL minus the sum of the slices' line counts and must be ≤ 400 (DECISION F085 D5).
 G3 SHAPES, one reading per unit, each against that commit's OWN pre-commit blob. Both units are
    appends at end of file with no FROM, so take NO FROM count and NO "TO 1x" count for either — the
    obligation is ORDERED EQUALITY. For CAND2 at C1 over `.agent/candidates.md` and for VERDICT at C2
    over `.agent/handoff.md` report: the pre-commit blob is a byte-exact PREFIX of the post-commit
    file, the slice is an exact SUFFIX of it, `pre + slice == post` is True, and that commit's ADDED
    lines equal the slice's lines IN ORDER. Report `git show --numstat` for C1 and C2. Report the
    count of lines beginning `BEGIN-` or `END-` in `.agent/candidates.md` and in `.agent/handoff.md`
    at C2 — each must be 0.
 G4 STATE READERS after C2, in the PRIMARY checkout, serially:
    `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    The reviewer ran this at e950e8af and measured exit 0, `160 passed`.
 G5 DOCS GATES after C2, serially: `python3 -m pytest tests/docs/ -q -rf` and
    `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`. This round edits no `docs/`
    path, so these two are a REGRESSION check that the `.agent/` appends changed nothing they read.
    The reviewer measured `295 passed` and `30 passed` at e950e8af.
 G6 CANARY, serially: `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer saw exit 0,
    `42 passed` at e950e8af.
 G7 INTEGRITY. The `remedy` CLI entry point is DENIED in this sandbox, so call the SAME functions
    `apps/cli/commands/integrity_cmd.py` invokes — `run_integrity_checks()` and
    `summarize_integrity()` from `packages.orchestration.integrity_gate` — and report the full
    summary. State that the module path was used, so the substitution is visible rather than hidden.
    The reviewer ran it at e950e8af and saw `Status: PASS (0 failures)` over five checks. It MUST
    pass.
 G8 ARITHMETIC under DECISION F085 D7, OPEN = REGISTERED − DONE, a `Landed:` line never subtracted.
    This round writes nothing into `.agent/live_review.md`, so report both operands and OPEN at
    e950e8af and at C2 and confirm they are UNCHANGED. The reviewer measured 184 registered, 32 done,
    OPEN 152 at e950e8af, with max registered R-0569, max resolved R-0564 and next free id R-0570.
 G9 HYGIENE. Report `git diff --name-only e950e8af..C2` in full — every path must be one this
    block's Change set names, none may end `.log`, and no evidence directory and no zip may appear.
    Report the insertion count of C0a, C0b and C1; C2's own count belongs in the round report and not
    in a gate, because it cannot exist while C2's text is being written. Confirm every commit is
    single-parent.
G10 PR UNTOUCHED. After the comment is posted, report
    `gh pr view 204 --json number,state,isDraft,baseRefName,headRefName` — state must still be OPEN,
    isDraft false, base `main`, head `feature/f085-sandbox-hardening`. Report the comment URL.

Round report, in your reply and NOT committed: the four commit SHAs with their changed-files tables,
C2's own insertion count, the real results of G1 through G10, the item-status table covering C0a,
C0b, C1 and C2 exactly once each, the push result, the PR comment URL, and any deviation with its
reason.

Next expected action: none in this session. The reviewer confirms the landed text and ends. The
operator merges PR #204 at the next feature's Open PR Gate.
────────────────────────────────────────────────────────────────────

BEGIN-CAND2

## Raised after the closure commit

One further candidate, raised by the reviewer's gate of R74 · source F085 · 2026-08-19, and written
here rather than only into the round report because this file is the carrier of record and a
brief-only candidate is exactly what the F056 closure lost. A branch's LAST round has no on-disk gate
entry by construction (docs/agents/planner_reviewer_prompt.md §4 item 13), so on disk a last round
whose verdict was issued and a last round whose verdict was never written are INDISTINGUISHABLE: both
show a handback with no `Gate:` paragraph naming it and no verdict anywhere. This session found
exactly that state at e950e8af — R74's handback present, `.agent/live_review.md` correctly silent
about R74, no verdict in `.agent/handoff.md`, and no comment on PR #204 when this gate began — and had
to re-run the entire round gate to establish which of the two states it was looking at. Item 13 tells
the reviewer to write the verdict into the handoff and the PR, but nothing on disk goes red when that
write does not happen, and the closure protocol's preconditions do not check for it either. Two
obvious counter-measures, for whoever takes this: have the closure round's own block order the verdict
slice as a named unit the way every other authored text is ordered, or give `.agent/handoff.md` a
terminator marker the integrity gate can look for. This is not F085's defect — it is a hole in the
terminator rule itself, which is why it needs a carrier rather than a repair inside this feature.
END-CAND2
BEGIN-VERDICT

## Reviewer verdict — R74: PASS

Issued by the planner and reviewer of the self-drive session of 2026-08-19 over the range
ed34119b..e950e8af. This is the LAST round of the branch, so its verdict lives here, in the round
report and on PR #204, and never in `.agent/live_review.md` — the terminator
docs/agents/planner_reviewer_prompt.md §4 item 13 describes, not a missing gate entry. Everything
below was RE-RUN by the reviewer rather than read from the handback above, except the absence of
`.agent/STOP` at the two points R74's constraint 2 names and `git status --porcelain` after each
intermediate commit, which are unobservable once a round has ended and are accepted on the worker's
report.

TRANSPORT HELD, disk-to-disk under the digest fallback of §4 item 9, and wider than the block
ordered: the committed `.agent/authored/f085-r74.md` and the committed `.agent/last_block.md` at
1181037b, both working copies, and both files again at e950e8af are all byte-EQUAL at sha256
d8a1225789c214549a90d61a21041f576e247036be4aa30cf941e3a394716e9b, 27361 B, 383 lines. TOTAL 383
against the 490 cap; the thirteen slices sum to 149 lines, so PROSE is 234 against 400. All thirteen
slice digests were recomputed by the reviewer and every one agrees with the handback. Of the 26 lines
beginning `BEGIN-` or `END-`, all 26 are real markers: the block predicted one prose line beginning
`END-OF-FILE`, and in the transported bytes that string is mid-line, so the worker's deviation 1 is
confirmed as measured and no slice was changed to suit the prediction.

THE SHAPES HELD, each against its own commit's pre-commit blob. PLAN28F→PLAN28T at 430a4a82 shows
FROM 1x pre and 0x post with TO exactly 1x post, and reproduces the post blob BYTE-EXACTLY.
STATUSF→STATUST at e950e8af, with only its three slots filled, shows the same three readings and the
same byte-exact reproduction. READMECOUNT and READMETIER at e950e8af each show FROM 1x pre, 0x post
and TO 1x post; their per-pair reproduction is False, and re-applying all three README pairs to the
617ef70a blob reproduces the e950e8af blob byte-exactly, which confirms the worker's deviation 2 as a
structural consequence of three pairs landing in one commit rather than as a defect. READMEDOC is
append-shaped — `TO contains FROM: true` — so no FROM-zero count was taken by anyone; its FROM occurs
1x in the post-commit file and its single TO-ONLY line occurs exactly 1x among the 3 lines C3's diff
adds to `README.md`. RECORD43 at 617ef70a satisfies ORDERED EQUALITY: the pre blob is a byte-exact
PREFIX, the slice an exact SUFFIX, `pre + slice == post` is True, and that commit's 36 added lines
equal the slice's 36 lines IN ORDER. `.agent/candidates.md` at e950e8af equals CANDIDATES byte for
byte at sha256 2343f4383e2465004f02a516276482d6587a0a5590d6cee008df4a76085431e6, 1915 B. Lines
beginning `BEGIN-` or `END-` number 0 in every TARGET file the round edited — `docs/roadmap/STATUS.md`,
`README.md`, `.agent/candidates.md`, `.agent/plan.md`, `.agent/live_review.md` and
`.agent/handoff.md`, each read at e950e8af — the two block mirrors excepted by construction.

THE SUITES WERE RE-RUN, NOT READ, in the primary checkout, serially, each exit 0. The full suite read
`17132 passed, 19 skipped in 120.36s`, and the reviewer ran it at e950e8af where the block ordered it
at 617ef70a: e950e8af is that commit's content plus one closure commit touching only `.agent/`,
`README.md` and `docs/roadmap/STATUS.md`, so the reading covers the ordered commit and the doc edits
made after it, and it is reported as the superset it is rather than as the reading that was ordered.
R-0569's id did not fire, so no serial re-run was needed. `tests/docs/` read `295 passed`,
`tests/orchestration/test_roadmap_index.py` read `30 passed`, the four state readers
`.agent/context.md` names read `160 passed`, and the canary read `42 passed` — every one equal to the
value the R74 block recorded at its base. The integrity gate read `Status: PASS (0 failures)` over
five checks with `handler_import: handlers=338`, through the module path because the `remedy` CLI
entry point is denied in this sandbox, which is the same substitution the worker declared.

THE ARITHMETIC HELD under DECISION F085 D7: 184 registered, 32 done and OPEN 152 at ed34119b, and the
same three values at e950e8af, with both symmetric differences EMPTY, 0 duplicate registered ids, 0
duplicate done ids, 0 resolutions naming an unregistered id and 0 `^Landed:` lines at both SHAs. Max
registered R-0569, max resolved R-0564, next free id R-0570. THE PLAN CONTRACT HELD at 430a4a82: 38
lines against the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present, and 0
marker lines. THE HYGIENE HELD: the range touches only paths the R74 block's Change set names, every
path that set names is touched, none ends `.log`, and no evidence directory and no zip appear, over
five single-parent commits in one chain inserting 383, 353, 8, 36 and 185 lines, none over 500. The
worker's deviation 8 is confirmed correct: `git show --numstat` reads 353 insertions for C0b where
the block's own line count is 383.

THE ARTIFACTS HELD, re-verified by the reviewer on disk rather than read. `sha256sum` over
`remedy-review-20260819-203439-READY_FOR_REVIEW.zip` returns
951d05c41f7c9ab5ee4dc0428b8be17e981b09738c20587f5c6c31b020296ad6, byte-identical to the value the
STATUS line carries. Its `.review_zip_manifest.json` reads `package_status: READY_FOR_REVIEW`,
`evidence_authoritative: true`, `review_subject_evidence_alignment.verdict: PASS`,
`final_verifier_reproducibility: VERIFIED_EQUAL`, `token_truth_authority: VERIFIED_EQUAL`,
`ready_gate_matrix.ok: true` with `blocking_reasons` empty, `packaged_evidence_job_id: f085-closure`
over task ids T001, T002 and T003, and a `committed_review_subject` whose head_commit is
617ef70a3d566abed1ca68a034570636636edad5 — the accepted HEAD the STATUS line names — with base
a5a706214d20101dd54564c23d0a3c22efcc705d, `base_is_ancestor: true` and commit_count 463, across 7258
members. `commit_execution_gate: NEEDS_HUMAN_APPROVAL` is the human-merge gate this workflow requires
and is not a defect. Read while this gate ran, PR #204 is OPEN, not a draft, from
`feature/f085-sandbox-hardening` into `main` and MERGEABLE, and its body's package, SHA-256 and
accepted HEAD equal the STATUS line's while its `464 commits` equals the reviewer's own
`git rev-list --count main..HEAD`.

ALL FIVE CLOSURE PRECONDITIONS of docs/roadmap/STATUS_closure_protocol.md hold, checked one by one:
every step has a PASS round and the 152 open findings are documented Medium or Low risks, with the
integrity gate reporting no open blocker and no High finding; the full relevant suite is green by the
reviewer's own run; the integrity gate passes with `untracked=0, relevant=0`; the feature file's
Built State section is present and was gated at R73; and at e950e8af the tree was clean with
`git status --porcelain` empty, the branch pushed to the same SHA as the local HEAD, and
`git worktree list` showing only the primary checkout.

F085 IS THEREFORE CLOSED AND ACCEPTED. What was not delivered stays on the record rather than in a
claim: R-0568 — the guard's `resource_limit` classification not reaching the F010 postmortem taxonomy
— remains open and documented.

One further candidate was raised by this gate after `.agent/candidates.md` was committed at e950e8af,
and this round carries it into that file: see its "Raised after the closure commit" section.

## Verdict round — record

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | block saved verbatim |
| C0b  | done   | block mirrored into last_block |
| C1   | done   | candidate carrier appended |
| C2   | done   | this verdict appended |

The four SHAs, the per-commit changed-files tables, C2's own insertion count and the ten gate results
ride in the round report, because a commit can state neither its own SHA nor its own insertion count
while its text is being written. Open findings: 152 (184 registered − 32 done, DECISION F085 D7).
Next free id R-0570.

Next expected action: none in this session. The operator merges PR #204 at the next feature's Open PR
Gate; this session merged nothing and created no branch.
END-VERDICT
BEGIN-PRCOMMENT
## Reviewer verdict — R74: PASS · F085 closed and accepted

Issued by the planner and reviewer of the self-drive session of 2026-08-19 over `ed34119b..e950e8af`.
This is the last round of the branch, so its verdict lives in `.agent/handoff.md`, the round report
and this comment, and never in `.agent/live_review.md`
(`docs/agents/planner_reviewer_prompt.md` §4 item 13). Every gate below was re-run by the reviewer in
the primary checkout rather than read from the handback.

**Suites, serially, each exit 0.** Full suite `python3 -m pytest -n auto -q` → `17132 passed, 19
skipped in 120.36s`, run at `e950e8af` where the block ordered it at `617ef70a`; that is the ordered
commit's content plus one closure commit touching only `.agent/`, `README.md` and
`docs/roadmap/STATUS.md`, and it is reported as the superset it is. `tests/docs/` → `295 passed`.
`tests/orchestration/test_roadmap_index.py` → `30 passed`. The four state readers → `160 passed`.
Canary `tests/cli/test_golden_path.py` → `42 passed`. Integrity gate → `Status: PASS (0 failures)`
over five checks, via the module path because the `remedy` CLI entry point is denied in this sandbox.

**Transport and shapes.** The committed authored block and `.agent/last_block.md` are byte-equal at
`d8a1225789c214549a90d61a21041f576e247036be4aa30cf941e3a394716e9b`, 27361 B, 383 lines, at both
`1181037b` and `e950e8af`, and all thirteen slice digests were recomputed and agree. The four rewrite
pairs each read FROM 1x pre / 0x post and TO 1x post; `README.md` reproduces byte-exactly only when
all three of its pairs are applied together, which is a consequence of three pairs landing in one
commit and is what the handback declared. The append-shaped `READMEDOC` and the `RECORD43` append
satisfy their own ordered-equality obligations, and `.agent/candidates.md` equals its authored slice
byte for byte.

**Arithmetic and hygiene.** 184 registered − 32 done = 152 open at `ed34119b`, unchanged at
`e950e8af`, both symmetric differences empty, no duplicate ids and no resolution naming an
unregistered id. The range touches only paths the round's change set names, over five single-parent
commits inserting 383, 353, 8, 36 and 185 lines.

**Artifacts.** `sha256sum` over the package returns
`951d05c41f7c9ab5ee4dc0428b8be17e981b09738c20587f5c6c31b020296ad6`, identical to the STATUS line, and
the manifest reads `READY_FOR_REVIEW`, `evidence_authoritative: true`, alignment `PASS`, accepted HEAD
`617ef70a3d566abed1ca68a034570636636edad5`, base `a5a70621…`, commit_count 463, 7258 members.
`commit_execution_gate: NEEDS_HUMAN_APPROVAL` is the human-merge gate this workflow requires, not a
defect.

All five preconditions of `docs/roadmap/STATUS_closure_protocol.md` hold. Open findings 152, none
High and none blocking; R-0568 is documented rather than claimed fixed.

**Not merged by an agent.** This PR merges at the next feature's Open PR Gate — the operator's
manual-review window.
END-PRCOMMENT
