── STEP CLOSURE-TWO — F009 ──
Goal:        Close F009. The R33 verdict is recorded, then ONE commit carries
             the authored STATUS `[x]` line, the README capability sync and the
             closure candidate, and the pull request is created from it. That
             commit is the LAST on this branch (AGENTS.md Rule A4) and the PR is
             NOT merged in this session — it merges at the next feature's start
             via the Open PR Gate, which is the operator's manual-review window.

Fortschritt: ~100 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN · Evidenz-Bundle und Review-Zip gebaut
             und verifiziert; diese Runde schreibt die STATUS-Zeile, den
             README-Sync und den Pull Request) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R33 verdict
             · C3 the closure commit · then push and create the pull request.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r34.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md` and
             `.agent/handoff.md` (ALL FOUR in C3, one commit). NOTHING under
             `packages/`, `apps/` or `tests/` is touched.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger commit because the plan must be current before it (checklist item
    23). C3 is the LAST commit on this branch: nothing may be committed after
    the STATUS edit (AGENTS.md Rule A4), which is why the handback is written
    INSIDE C3 rather than after it — docs/roadmap/STATUS_closure_protocol.md
    step 5 puts STATUS, README and the final `.agent/` state in that one
    commit, and R-0154 requires README and STATUS never to disagree in any
    committed state.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. The next free id is R-0648
    when the round ends. The one defect this round records is written to
    `.agent/candidates.md` as a CANDIDATE without an id, which is what the
    closure protocol's "Closure-candidate findings" section requires of a
    finding raised during a closure review.
 4. ONE APPEND, TWO WHOLE-FILE REPLACEMENTS AND FOUR FROM/TO PAIRS.
    PLANF009R34 replaces `.agent/plan.md` at C1 in full. LEDGER34 appends to
    `.agent/live_review.md` at C2 based on the ROUND BASE. CANDIDATES34
    replaces `.agent/candidates.md` at C3 in full. The four pairs all apply at
    C3. Their containment readings, each PRINTED BY THE REVIEWER'S OWN SCRIPT
    against the files at the round base and recorded here one per pair
    (checklist item 15): STATUS `TO contains FROM: false`, so REWRITE;
    READMEA `TO contains FROM: false`, so REWRITE; READMEB
    `TO contains FROM: false`, so REWRITE; READMEC `TO contains FROM: true`,
    so APPEND. Order the FROM-zero count ONLY for the three rewrites; for
    READMEC that count is unattainable by construction and the obligation is
    instead FROM exactly 1x plus each TO-only line exactly 1x among the lines
    C3's diff ADDS (§4.9).
 5. Each pair's FROM occurs EXACTLY ONCE in its target at the round base — the
    reviewer's script printed 1 for all four. Apply the pairs with a script,
    each with `count=1`, and report the occurrence count you measured BEFORE
    each replacement.
 6. The reviewer measured the targets at the round base
    `06aeb7494ff47dae77764303dbbb3d4aace48158`: `.agent/live_review.md` is
    589646 bytes over 1146 lines and ends in exactly ONE newline;
    `.agent/candidates.md` is 736 bytes over 13 lines; `.agent/plan.md` is 2091
    bytes over 37 lines. So the append is one newline followed by its slice.
 7. EVERY reading at a revision other than the one your shell is on is taken
    with `git show <sha>:<path>`. NEVER write a base blob over a tracked file
    and restore it (finding R-0594, guardrail G5).
 8. Count LEDGER34's paragraphs with your script rather than from any sentence
    in this block.
 9. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
10. SIZE, measured at emission by reading it back out of the assembled bytes
    and computing PROSE as TOTAL minus the slices' CONTENT lines, with marker
    lines counted as prose per DECISION F085 D5: this block is 327 lines TOTAL
    against DECISION F085 D6's 490 cap, 240 of them PROSE against D5's 400.
    Re-measure both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C3: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2 and C3. Report the round base SHA you
     read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r34.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for all three. C0b is written FROM the committed
     C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 10's two numbers from that same blob — TOTAL, and PROSE as
     TOTAL minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R34 and
     `.agent/candidates.md` at C3 is BYTE-EQUAL to CANDIDATES34 — report `cmp`
     exit and both sha256 for EACH, each with a negative control against
     another file exiting non-zero. Report `wc -l` for the plan against the
     50-line cap of AGENTS.md; line-anchored, `^## Goal$` and `^## Next Steps$`
     each read 1. Over `.agent/candidates.md`, line-anchored: a leading `- `
     reads 0 at the round base and 1 at C3, `^EMPTY\.` reads 1 at the base and
     0 at C3, and `^NON-EMPTY\.` reads 0 at the base and 1 at C3 — six numbers,
     every one anchored, because the UNANCHORED substring `EMPTY.` reads 1 at
     both points and discriminates nothing (R-0646).
 G5  THE APPEND, under TWO independent readers, with a negative control on the
     FIRST appended paragraph (finding R-0631). LEDGER34 at C2 based on the
     round base. (a) the base blob is a byte-exact PREFIX and the remainder
     equals a newline plus that slice — report its sha256, bytes and lines;
     (b) N is counted BY YOUR SCRIPT and the last N blank-line-separated units
     equal the slice's N paragraphs IN ORDER. Then flip one printable byte in
     the FIRST appended paragraph, at equal length, and report that BOTH
     readers REJECT the flip while both ACCEPT the true file.
 G6  THE FOUR PAIRS at C3. For each, report the FROM occurrence count you
     measured in the target BEFORE replacing. AFTER C3: for the three REWRITES
     (STATUS, READMEA, READMEB) report FROM 0x and TO 1x in the target. For the
     APPEND (READMEC) report FROM exactly 1x, and report that every line the
     TO adds which the FROM does not contain occurs exactly 1x among the lines
     `git show --numstat`/`git diff` show C3 ADDING to `README.md` — never a
     whole-file count, which a legitimate repeat makes unsatisfiable (§4.9,
     R-0253). Report `git show --numstat` for `README.md` and
     `docs/roadmap/STATUS.md` at C3.
 G7  Line-anchored at line START over `.agent/live_review.md` at the round base
     AND at C2: a leading `- R-` id with every captured id DISTINCT at each; a
     leading `Done: R-` id; a leading `Landed: `; a leading `Gate: R` key over
     that many DISTINCT keys; and the `Gate: R34` key. Report EVERY one of
     those five readings at BOTH points (R-0494). The reviewer's base readings,
     which yours must reproduce: entries 213 all DISTINCT, `Done:` 3,
     `Landed: ` 0, `Gate: R` keys 33 over 33 DISTINCT, `Gate: R34` 0.
     Constraint 3 fixes that entries read 213 all DISTINCT at C2 too, and that
     `Gate: R34` reads 1 at C2.
 G8  Report the max REGISTERED id, read line-anchored, and the open count by
     DECISION F009 D10's rule at the round base and at C2. This fixes the next
     round's id ceiling and is NOT an anchoring control. The reviewer's base
     readings: max R-0647, open 210, both UNCHANGED at C2 by constraint 3.
 G9  THE STATUS LEDGER AT C3, all read line-anchored over
     `docs/roadmap/STATUS.md`: `^- \[x\] ` reads 54 at the round base and 55 at
     C3; `^- \[~\] ` reads 1 at the base and 0 at C3; `^- \[x\] F009 — ` reads
     0 at the base and 1 at C3; `^- \[~\] F009 — ` reads 1 at the base and 0 at
     C3. Report all eight. Then report that the C3 F009 line contains, as
     literal substrings, the evidence job `f009-closure`, the package
     `remedy-review-20260822-085607-READY_FOR_REVIEW.zip`, the SHA-256
     `ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f` and the
     accepted HEAD `97d028980b5781cbf22a0f651f7e879eea1a0485`, and that the
     last of those EQUALS the `head_commit` recorded in
     `.review_zip_manifest.json` inside that package on disk — read it out of
     the zip, do not retype it. Report the package's own sha256 recomputed from
     the file on disk against the value in the STATUS line.
 G10 DOCS GATE, owed because this round's change set holds `docs/roadmap/**`
     (planner_reviewer_prompt.md §3 verification tier 5): at C3, in the PRIMARY
     checkout, serially, with no other pytest alive,
     `python3 -m pytest tests/docs/ -q -rf`. Report its REAL exit code and the
     count IT printed. The reviewer ran this gate at the round base — 295
     passed, exit 0 — and then ran it AGAIN in a disposable worktree with these
     exact closure edits applied: 295 passed, exit 0. It was also proved able
     to FAIL: with the README accepted-count set to a wrong value the same
     command exits 1 with
     `tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_accepted_count_equals_the_status_count`
     as the single failure at 1 failed, 294 passed, and restoring the authored
     value returns it to 295. So a red here is real (R-0364).
 G11 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the
     PRIMARY checkout, serially, after the docs gate has finished. Report its
     REAL exit code and the count IT printed. The reviewer ran it at the round
     base: exit 0 at 42 passed.
 G12 RANGE: the range from the round base to C3 lists EXACTLY the seven
     declared paths, the set difference EMPTY in both directions, and 0 paths
     beginning `packages/`, `apps/` or `tests/`. Each commit has ONE parent;
     `git show --numstat` and `git diff --numstat` AGREE on every cell —
     invoke `git show` WITHOUT a `--` before the SHA; every cell equals the
     `+/-` column of the handback's `## Commits` table (checklist item 28),
     compared cell by cell. Report each commit's insertions against the 500
     cap. Leading `<<<SLICE ` and `<<<END ` read 0 LINES in every file a slice
     lands in, which are `.agent/plan.md`, `.agent/live_review.md`,
     `.agent/candidates.md`, `docs/roadmap/STATUS.md` and `README.md` — read
     that count LINE-ANCHORED, not as a substring. `git ls-files .remedy-wt`
     reads 0. Classify THIS ROUND's reflog rows by the operation before the
     first `:` and report `amend`, `rebase` and `cherry` each 0; assert no
     total over the whole reflog (R-0601).
 G13 THE PULL REQUEST, created AFTER C3 is pushed and NEVER merged. Report the
     `gh pr create` exit code and the PR number and URL it printed, and report
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
     showing exactly one open PR from `feature/f009-single-write-channel` into
     `main`, not a draft. Run NO `gh pr merge`. The description carries: what
     changed and why; the key decisions; how to review and test; a
     changed-files table for the branch; the latest verdict PASS_WITH_RISKS;
     the open-findings count 210 with the note that the two unresolved High
     findings R-0495 and R-0574 are inherited from the closed features F085 and
     F086 and are not F009 defects; and the runtime actuals — 34 rounds, the
     four closure values, and `not-measured` for tokens, cost and total wall
     clock, which is the honest reading rather than a guess (closure protocol
     step 3). The PR title names F009 and its T-slices and contains NO
     leading-slash token and NO absolute path (AGENTS.md commit discipline).
 G14 The handback, written INSIDE C3, carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, one line per gate, and this block's
     `Fortschritt:` line VERBATIM across all four of its lines. Where a gate
     ordered a reading at SEVERAL points, every point's value appears in the
     file (R-0494). Its `## Next` section states that F009 is CLOSED, that the
     PR is open and unmerged, and that the next session's Open PR Gate merges
     it before any new feature is claimed. The PR number and the C3 SHA cannot
     exist when C3's own content is written, so name them by role and put the
     values in the round report (R-0371). Report its `wc -l`; the cap is 60 for
     a five-commit round, and if the mandated content does not fit, carry a
     DECISION D15 "Deviations, declared" line naming the actual count and the
     content that caused the overage — never drop a section.

Handback:    completion report + the `.agent/handoff.md` rewrite INSIDE C3.
             Push, then create the PR. Do NOT merge it.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R34
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R34 is closure round two and the last round of this branch. It records the R33
verdict, then one commit carries the STATUS `[x]` line, the README capability
sync and the closure candidate, and the pull request is created from it.

## Next Steps
1. Nothing remains on this branch. The pull request is NOT merged in this
   session.
2. The next session's Open PR Gate merges it before any new feature is claimed,
   which is the operator's manual-review window.

## Risks
- The STATUS edit must be the LAST commit on the branch (Rule A4), so the
  handback is written inside that same commit rather than after it.
- README and STATUS may never disagree in any committed state (R-0154), which
  is why both land in one commit and the docs gate runs at it.
- Two open High findings, R-0495 from F085 and R-0574 from F086, are inherited
  from closed features and are documented risks, not F009 defects; the verdict
  is PASS_WITH_RISKS, exactly as F008 closed one feature ago.
<<<END PLANF009R34

<<<SLICE LEDGER34
Gate: R34 — the R33 entry. R33 PASSED, AND THE TWO CLOSURE ARTEFACTS ARE REAL — the reviewer re-executed all fourteen gates off disk and additionally verified each artefact against the file it claims, rather than against the handback. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r33.md` at `02eb5f8e`, `.agent/last_block.md` at `a97537ee` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r33.md`, are all sha256 0ee2aa94c7875f7912274654a5974c83c06444092fdf09b204ce5bb7f4bff9ca over 33170 bytes and 462 lines. The reviewer's own extraction out of the committed C0a blob prints 3 slices over 186 CONTENT lines, and constraint 10's numerals re-measure as 462 TOTAL and 276 PROSE, under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `f54fe49a` is BYTE-EQUAL to PLANF009R33 at 37 lines against the 50-line cap with `^## Goal$` and `^## Next Steps$` each 1; the negative control differs. THE APPEND HOLDS UNDER THE REVIEWER'S OWN TWO READERS: LEDGER33 at `97d02898` is based on the round base, the base blob a byte-exact PREFIX and the remainder exactly one newline plus the slice, 584339 to 589646 bytes and 1144 to 1146 lines, N counted at 1. THE SETS HELD line-anchored at line start at both points: at the round base entries 213 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys 32 over 32 DISTINCT, `Gate: R33` 0, max REGISTERED id R-0647, 210 open; at `97d02898` entries UNCHANGED at 213 all DISTINCT with max still R-0647 and 210 open, `Gate: R` 33 over 33 DISTINCT and `Gate: R33` at 1 — nothing was minted. THE ANCHORING CONTROL WAS ORDERED WITH ITS SCAN SHAPE NAMED, which is the R-0630 lesson the R32 round surfaced: at the base 213 anchored ids against 273 distinct unanchored strings of which 60 were never registered, 32 anchored `Gate: R` keys against 84 key-shaped and 131 literal occurrences; at C2 213, 273, 60, 33, 88 and 140. Both scans are reported and neither is called "the" count. THE EVIDENCE BUNDLE IS THE REVIEWER'S OWN READING OF THE FILES: `.remedy-wt/f009_closure_evidence/remedy-job-evidence-f009-closure` holds 27 entries and its `verification_tests.json` carries five runs whose `selected` equals `len(node_ids)` in every case — 99, 4, 27, 16 and 11 for 157 passed — whose `head_sha` is `97d02898` in every case, and whose `output_hash` the reviewer re-derived as sha256 over `stdout_summary` EXACTLY, matching for all five. Three tests are DESELECTED and the record says so rather than hiding it: the parametrization `[../escape]` occurs once each in the channel, nonce and audit suites and `scripts/build_review_manifest._unsafe_text` reads `../escape` as a local path, so those ids cannot be packaged; deselecting at run time keeps `len(node_ids) == selected` true where deleting an id from a list would have made it false. The reviewer re-ran that scanner over every packaged node id and command and it rejected 0, while an absolute-path control returned `a local absolute path`. This is the closure protocol's F080 R4 lesson (d) applied, and the three tests are green in this round's own suites and in the integration gate. THE ZIP IS READY AND WAS OPENED, NOT QUOTED: `remedy-review-20260822-085607-READY_FOR_REVIEW.zip` is 72237000 bytes on disk and its recomputed sha256 is ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f, equal to the value the build printed; `zipfile.namelist()` counts 12906 members, agreeing with the manifest; and `.review_zip_manifest.json` INSIDE the package reads `package_status` READY_FOR_REVIEW, `base_commit` the full ce49348b8f5b0374417f5b6c47d8c04966e7108e, `head_commit` 97d028980b5781cbf22a0f651f7e879eea1a0485 which is C2, `base_is_ancestor` true, `commit_count` 233, `file_count` 64, `packaged_evidence_job_id` f009-closure, `ready_gate_matrix.ok` true with an EMPTY `blocking_reasons`, and `review_subject_evidence_alignment` PASS with 0 issues and 0 hash mismatches. THAT GATE CAN FAIL, AND IT DID: before ordering it the reviewer built the same package from a throwaway bundle carrying the unfiltered node-id lists, and it returned PACKAGE_STATUS BLOCKED_EVIDENCE with EVIDENCE_AUTHORITATIVE false, naming three node ids as carrying a local absolute path plus the consequent missing VerificationTests total — at EXIT CODE 0, which is why exit code is not the reading here and the block said so. THE INTEGRITY CHECK passes 5 of 5 with `fail_count` 0, run through the module import because the `remedy` CLI is denied by this session's guard. THE RANGE HELD: base→`97d02898` lists exactly the four declared paths with the set difference EMPTY both ways, `docs/roadmap/STATUS.md` and `README.md` both ABSENT as this round's discipline requires, 0 paths beginning `packages/`, `apps/`, `docs/` or `tests/`; all five commits single-parent; `git show --numstat` and `git diff --numstat` agree on every cell and each equals the handback's own table at 462/0, 402/190, 13/14, 2/0 and 59/65, every insertion under the 500 cap; zero leading marker LINES in both slice targets; `git ls-files .remedy-wt` 0; five reflog rows all `commit` with `amend`, `rebase` and `cherry` each 0. THE CANARY IS THE REVIEWER'S OWN: exit 0 at 42 passed. THE HANDBACK IS 88 LINES against the 60-line cap a five-commit round allows, and the overage is DECLARED in its own line naming the count and the mandated closure content that caused it, with no section dropped — which is what DECISION D15 permits and what the block anticipated.
<<<END LEDGER34

<<<SLICE STATUSFROM
- [~] F009 — The single write channel
<<<END STATUSFROM

<<<SLICE STATUSTO
- [x] F009 — The single write channel (T001–T003 complete; accepted 2026-08-22 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f009-closure · package remedy-review-20260822-085607-READY_FOR_REVIEW.zip · SHA-256 ca7a77704beb2e9f29ef80f365e54665851a7655f2a0944cdb5d5744cf5dff9f · accepted HEAD 97d028980b5781cbf22a0f651f7e879eea1a0485)
<<<END STATUSTO

<<<SLICE READMEAFROM
54 of 255 registered items accepted. Next: F009 (The single write channel).
<<<END READMEAFROM

<<<SLICE READMEATO
55 of 255 registered items accepted. Next: F021 (Live activity feed + "agent is doing now").
<<<END READMEATO

<<<SLICE READMEBFROM
| 5 | Operator Cockpit | 2 | 29 |
<<<END READMEBFROM

<<<SLICE READMEBTO
| 5 | Operator Cockpit | 3 | 29 |
<<<END READMEBTO

<<<SLICE READMECFROM
F008 sse event stream (per-job SSE endpoint with heartbeat and Last-Event-ID
resume, a cockpit client with reconnect backoff and a polling fallback that
labels itself delayed instead of pretending to be live).
<<<END READMECFROM

<<<SLICE READMECTO
F008 sse event stream (per-job SSE endpoint with heartbeat and Last-Event-ID
resume, a cockpit client with reconnect backoff and a polling fallback that
labels itself delayed instead of pretending to be live).
F009 the single write channel (one authenticated, CSRF-guarded, rate-limited
and nonce-idempotent POST endpoint for UI-initiated commands, every other
mutating route answering 405 under a route-walking test).
<<<END READMECTO

<<<SLICE CANDIDATES34
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. One candidate, raised by the reviewer during the F009 closure review
and recorded here without an id because the closure protocol reserves ids for
the next session's first reviewed round.

- THE CLOSURE PRECONDITION THAT IS SUPPOSED TO BLOCK ON OPEN HIGH FINDINGS
  CANNOT SEE THIS REPOSITORY'S FINDING LEDGER, SO IT PASSES VACUOUSLY · F009
  R34 · 2026-08-22. `_check_high_blockers_open` in
  `packages/orchestration/integrity_gate.py` parses `.agent/live_review.md` for
  findings shaped `### R-XXXX:` with `- **Status**:` and `- **Severity**:`
  lines beneath them, and reports PASS with "no open blocker/high findings"
  when it matches none. Measured at `06aeb749`, that file contains 0 of those
  headings, 0 `- **Status**:` lines and 0 `- **Severity**:` lines against 213
  real entries in the form `- R-XXXX — <Severity> — <headline>`, and two of
  those entries — R-0495 and R-0574 — are High and carry no `Done:` line. So
  the check answers PASS for a ledger holding exactly what it exists to catch,
  and closure precondition 3 has been satisfied by a reading that cannot fail.
  This is the R-0438 vacuous-gate class in PRODUCTION code rather than in a
  reviewer block, which is why it is worth more than the two that preceded it:
  a reviewer block is read by a human every round, and this parser is not.
  Nothing about the F009 closure is unsound because of it — the reviewer read
  the severities directly, found both Highs inherited from the closed features
  F085 and F086, and the verdict is PASS_WITH_RISKS on that basis — but the
  automated guard contributed nothing to that finding. Candidate
  counter-measure for the round that registers this: teach the parser the
  `- R-XXXX — <Severity> —` form the ledger actually uses with `Done:` as the
  resolution marker, and give it a test whose fixture is a ledger in the REAL
  format holding one open High, so the check goes red where today it is blind.
<<<END CANDIDATES34
