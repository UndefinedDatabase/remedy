── STEP T003/8 — F008 SSE event stream — ROUND 35 · CLOSURE EVIDENCE ─────────
Round base — the SHA every range gate in this block measures from: 2bacba10
 (R34's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R34 verdict — PASS, the integration gate GREEN and re-run by the
 reviewer — write this feature's Built State into its roadmap file, and produce
 the two artefacts closure cannot happen without: the evidence bundle and a
 FRESH review zip. This round builds and reports them; the NEXT round authors
 the STATUS line from the values only this round can produce.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r35.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R35, applied whole
 C2   `.agent/live_review.md` <- LEDGER35, appended
 C3   `docs/roadmap/features/T5_F008.md` <- BUILTSTATE, appended
 then, with NO commit between them: push, the evidence job, the integrity
 check, the review zip — all at C3, the accepted HEAD they describe
 C4   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r35.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `docs/roadmap/features/T5_F008.md`,
 `.agent/handoff.md`.
 The evidence bundle and the review zip are NOT committed and are NOT in that
 set: `docs/roadmap/STATUS_closure_protocol.md` forbids committing the evidence
 dir, because a pre-committed bundle lands inside the base..HEAD review subject
 and packages BLOCKED_EVIDENCE.

Transport:
 This block is on disk at `.remedy-wt/f008-r35.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r35.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, none
 begins with a blank line, and every count this block orders over a slice is
 taken over those newline-INCLUDED bytes.

Pair shape (§3 item 15): this block contains NO FROM/TO pair, so no containment
reading is owed for anything in it. PLANF008R35 is a whole-file write, LEDGER35
and BUILTSTATE are appends, and EVIDENCESCRIPT is a new file written to the
gitignored `.remedy-wt/` and never committed as itself — its bytes reach the
record inside the C0a blob, like every other slice.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit. C1
    is the first substantive commit (§3 item 23). C3 is the LAST commit before
    the artefacts, and the push, the evidence job, the integrity check and the
    zip all run at C3 with a clean tree, in that order — the zip records C3 as
    the accepted HEAD, and a zip built from a dirty tree is invalid.
 3. Nothing outside the change set is touched. NO source file under
    `packages/`, `apps/` or `tests/` is edited this round: the code is final at
    `2bacba10` and this round produces artefacts about it.
 4. NO FINDING ID IS MINTED and none is resolved: R-0630 stays free, and
    R-0368, R-0429, R-0553, R-0593, R-0622, R-0628 and R-0629 all stay OPEN.
    Write no `Done:` and no `Landed:` line. If this round SURFACES a defect,
    it is a closure CANDIDATE and not a finding — record it in the handback's
    deviations section and spend no id on it, per
    docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings".
 5. END EVERY COMMIT MESSAGE of this round with the trailer line
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, preceded by a
    blank line. G13 measures the result. Never repair a missing trailer by
    amending — protocol G2 forbids it.
 6. The post-C4 porcelain and any push output after C4 belong to the ROUND
    REPORT, not to `.agent/handoff.md` (R-0371). The push at C3 and every
    artefact value DO belong in the handback: the next round's STATUS line is
    authored from them and they exist nowhere else.
 7. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH, DO NOT
    EDIT `docs/roadmap/STATUS.md` and DO NOT EDIT `README.md`. Those are the
    NEXT round's closure commit, which must be the last commit on the branch
    (Rule A4). `gh pr list --state open` returned `[]` at the reviewer's Phase
    0 probe; run no `gh` command at all this round.
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there; commit nothing
    from it. Never `cd` into a worktree and leave the shell there (R-0463).
 9. THE HANDBACK QUANTIFIES NOTHING IT DID NOT COUNT (R-0553). Any handback
    sentence stating "every", "no", "all" or "none" over commits, files, ids,
    runs or bundle entries names the command that produced the number.
 10. THE HANDBACK'S `## Next` SECTION states, in this order: that the next
    session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and
    its SECOND the Open PR Gate (Phase 1 rule 2); that R35 is PENDING REVIEW
    and its verdict is owed by the next round's ledger commit; that the next
    free finding id is R-0630; that R-0368, R-0429, R-0553, R-0593, R-0622,
    R-0628 and R-0629 are OPEN; and that R36 is the CLOSURE COMMIT round —
    the authored STATUS `[x]` line, the README capability sync and the
    `.agent/candidates.md` carrier in ONE commit (R-0154), then the pull
    request — carrying the package name, the SHA-256, the evidence job id and
    the accepted HEAD this round reports.

The reviewer's OWN readings, each produced by RUNNING the tool at the round base
`2bacba10`, serially, in the PRIMARY checkout, not recalled (R-0625):
`python3 -m pytest -n auto -q` EXITS 0 at `17412 passed, 20 skipped` in 151.4 s
with 0 lines beginning FAILED — the reviewer's own re-run of the integration
gate's branch side, which is precondition 2 of the closure protocol. Per suite,
`--collect-only -q` id counts against a `-q` run: test_sse_stream.py 65 ids /
65 passed, test_event_seq.py 7 / 7, test_server_concurrency.py 1 / 1,
test_brain_stream_hook.py 9 / 9, test_live_status_pill.py 7 / 7,
test_remedy_shell_stream.py 8 / 8 — every one EXIT 0 with 0 skipped, no id
containing whitespace, and 97 tests in total, which is exactly the branch run's
17412 minus the base run's 17315.
The reviewer ALSO DRY-RAN EVIDENCESCRIPT verbatim (item 12), with its
`EVIDENCE_DIR` diverted by a one-string patch to
`.remedy-wt/r35_dry_evidence/` and nothing else changed: EXIT 0, all six runs
reporting `len(node_ids) == selected`, a 27-entry bundle, and `output_hash`
equal to the sha256 of `stdout_summary` for all six. That dry bundle is scratch
and is NOT the one G10 orders — the path G10 names has never existed, which is
what its pre-existence reading is for.
The reviewer has NOT run the integrity check or the zip, and does not predict
their outcome: G11 and G12 order READINGS, and a failing zip is a closure
BLOCKER the round reports rather than retries.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2 and C3, and again immediately before the zip.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r35.md`
     as received, of `.agent/authored/f008-r35.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r35.md` with `git show`, by their marker lines, take
     the COUNT from that listing and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, that none carries trailing whitespace on any line, and that
     none begins with a blank line.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R35. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists.
 G5  The append at C2, against the round base, two ways that must agree. Read
     the base bytes with `git show 2bacba10:.agent/live_review.md` into scratch
     — never over the tracked file (item 29). (a) the base blob is a byte-exact
     PREFIX of the C2 blob and the remainder equals a newline plus LEDGER35 —
     report its sha256 prefix, bytes and lines; (b) an INDEPENDENT blank-line
     split of the WHOLE C2 file, its terminating newline normalised first, has
     LEDGER35's paragraph as its LAST unit. NEGATIVE CONTROL: flip one
     PRINTABLE ASCII byte of the remainder to another printable one; BOTH
     readings must reject it and both accept the unflipped.
 G6  The sets in `.agent/live_review.md`, line-anchored, reported at the round
     base AND at C2: `^- R-\d+ — ` reads 201 at both — this round mints no id —
     `^- R-0630 — ` 0 at both, `^- R-0593 — `, `^- R-0629 — `, `^- R-0429 — `,
     `^- R-0553 — `, `^- R-0628 — ` and `^- R-0368 — ` 1 each at both,
     `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at both, and `^Gate: R\d+ — `
     34 at the base and 35 at C2, over that many DISTINCT keys. HEADER SWEEP at
     C2 (item 26): report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of each non-match to its first period,
     and that the R35 pair occurs EXACTLY ONCE.
 G7  The Built State append at C3. Report that the base blob of
     `docs/roadmap/features/T5_F008.md` is a byte-exact PREFIX of the C3 blob
     and that the remainder equals a newline plus BUILTSTATE, with its sha256
     prefix, bytes and lines; that the lines that commit's diff ADDS are
     exactly the remainder's lines IN ORDER; and the count of `^## Built State`
     in that file at the base (expected 0) and at C3 (expected 1).
 G8  The docs gate and the canary, at C3, in the PRIMARY checkout, SERIALLY,
     never two test processes alive at once. This round's change set includes a
     `docs/roadmap/**` path, which gates with the docs suite in addition to the
     canary (planner_reviewer_prompt.md §3, verification tier 5):
     `python3 -m pytest tests/docs/ -q -rf` and
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report each
     command's EXIT CODE and its passed and skipped numbers SEPARATELY as well
     as their sum. If either fails, report the real values and STOP — a red
     docs gate means the Built State text broke a ledger pin, and that is a
     repair, not a closure.
 G9  Clean tree, pushed, AT C3. `git status --porcelain` EMPTY, then
     `git push -u origin feature/f008-sse-event-stream`; report its exit code
     and output. Report `git rev-parse HEAD` and use that value as C3's SHA
     everywhere below — the artefacts describe THAT commit.
 G10 THE EVIDENCE JOB, closure protocol Algorithm step 1. Write EVIDENCESCRIPT
     byte for byte to `.remedy-wt/r35_evidence.py` and run it with `python3`
     from the repository root. It builds the bundle at
     `.remedy-wt/f008_closure_evidence/remedy-job-evidence-f008-closure`
     through `create_manual_completion_bundle`, which is the canonical producer
     — `write_runtime_integration_gate` alone is NOT a bundle and packages as
     BLOCKED_EVIDENCE. Report: the exit code, that the directory did not
     pre-exist, the number of entries in it, and the producer's own printed
     summary. The script asserts, and you report, the four producer pitfalls
     the protocol names: per run `len(node_ids) == selected` with ids taken
     from `--collect-only -q` and never by regexing a `-v` log (finding
     R-0611), `test_files` entries all FILES and SORTED, every `run_id`
     matching `^vr-\d{4,}$`, and the full 40-character `base_commit`. Then read
     the WRITTEN bundle back and report, per verification run, whether
     `output_hash` equals the sha256 of `stdout_summary` EXACTLY — the pitfall
     that blocked the F083 closure and is not in that document's list. The
     bundle is NOT committed and lives under the gitignored `.remedy-wt/`, so
     it stays outside the base..HEAD review subject.
 G11 THE INTEGRITY CHECK, closure precondition 3. The `remedy` CLI is DENIED by
     this session's command guard, so call the same code directly:
     `from packages.orchestration.integrity_gate import run_integrity_checks`,
     then `run_integrity_checks()`. Report `passed`, the fail count, and EVERY
     check's name with its own status — do not summarise them. This is the
     precedent F255 R20 set, and it reads the same five checks the CLI reads.
     If any check fails, report it verbatim and STOP: a failed integrity check
     is a closure precondition failure, not a detail.
 G12 THE REVIEW ZIP, closure protocol Algorithm step 2 — MANDATORY, fresh,
     never skipped. From the repository root with the tree still clean:
     `bash scripts/make_review_zip.sh --evidence-dir <the G10 bundle path>`.
     Report the exit code, the package FILENAME, its SHA-256 as the script
     printed it AND as you recompute it from the file on disk with sha256sum,
     `PACKAGE_STATUS`, the member count, `EVIDENCE_AUTHORITATIVE`, the review
     subject alignment, and the manifest's `committed_review_subject` base and
     head — the head MUST equal C3's SHA from G9 and the base MUST be
     7c03adfa58519d484df685d38b950c49afaf70a8. A FAILING ZIP BUILD IS A CLOSURE
     BLOCKER: report the raw error and STOP rather than retrying blind. The
     package will contain `.remedy-wt/` scratch as context; that is the
     already-registered R-0403 and not a new condition of this closure.
 G13 The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only 2bacba10..C3` and that it
     equals the Change set MINUS `.agent/handoff.md` exactly, with none on
     either side alone. Walk `git rev-list --reverse 2bacba10..C3` and report
     ONE reading per commit: that it has exactly ONE parent, and BOTH numstat
     cells per path from `git show --numstat`, cross-checked against
     `git diff --numstat`, every insertion under 500 and every cell equal to
     the `+/-` column of your `## Commits` table, cell by cell (item 28). C4's
     own numbers cannot exist while C4 is being written, so they belong to the
     round report (item 14). Count LINES BEGINNING with `<<<SLICE ` or
     `<<<END ` in the plan at C1, the ledger at C2, the feature file at C3 and
     the handback at C4 — each is 0; `.agent/last_block.md` is NOT in that
     list, being the block's own mirror. Measure constraint 5 with
     `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 2bacba10..HEAD`
     before C4 and report how many commits it lists and how many return a
     NON-EMPTY value — state it as that measurement and never as a universal.
     Report this round's own reflog entries classified by the OPERATION before
     the first `:` in `%gs`: how many you classified, and `amend`, `rebase` and
     `cherry` at 0. Assert no total over the whole reflog (R-0601).
 G14 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 10
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C2, C3 and C4 — "exactly one row" scoping to that
     TABLE. It ALSO carries, in its own section, the four values the next
     round's STATUS line is authored from and which exist nowhere else: the
     evidence job id, the package filename, its SHA-256 and the accepted HEAD.
     Measure the file's line count with `wc -l` BEFORE committing it; this
     round's commit count is six, so the cap is 100, and an overage carries a
     DECISION D15 stated-cause line naming the real count and the mandated
     content that caused it. One line per gate here; raw transcripts go in the
     ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 ~100 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrations-Gate PASSED — Evidence-Job und Review-Zip in dieser Runde; nur STATUS-Zeile, README-Sync und der Pull Request bleiben) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R35
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint streaming the event ledger from a cursor — the ledger's
own monotonic seq carried and never renumbered, a 15 s heartbeat, Last-Event-ID
resume replaying exactly the missed span — plus a client hook with reconnect
backoff, gap detection and an honest polling fallback that labels itself
delayed. DONE when a fake job streams into a test client with zero gaps across
forced disconnects, the transcript byte-equals the ledger's envelope sequence,
the heartbeat holds cadence, and the fallback engages on a disabled EventSource
and recovers to live.

## Current Step
R35 is the CLOSURE EVIDENCE round. It records the R34 verdict — PASS, the
integration gate green on both sides with 0 branch-only and 0 base-only
failures — writes this feature's Built State into
`docs/roadmap/features/T5_F008.md`, and then produces the two artefacts closure
cannot happen without: the evidence bundle from
`create_manual_completion_bundle` and a FRESH review zip, both at the commit
carrying the Built State.

## Next Steps
1. R36 is the CLOSURE COMMIT round per docs/roadmap/STATUS_closure_protocol.md:
   the authored STATUS `[x]` line, the README capability sync and the
   candidates carrier in ONE commit (R-0154), then the pull request, which is
   NOT merged in its own session.

## Risks
- A failing zip build is a closure BLOCKER, not a retry: the round stops and
  reports the raw error.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
<<<END PLANF008R35

<<<SLICE LEDGER35
Gate: R35 — the R34 entry. R34 PASSED, AND ITS INTEGRATION GATE IS GREEN ON BOTH SIDES. The round recorded the R33 verdict, amended R-0593 with the F008 R33 instance, retired the pill comment that denied its own caller, and ran the full suite once on this branch and once at the merge base — and EVERY BYTE PROOF WAS RE-RUN BY THE REVIEWER out of the committed blobs, with the branch-side suite re-run in the primary checkout, rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.agent/authored/f008-r34.md` at `78055070` and `.agent/last_block.md` at `6a9bde0c` are both sha256 b4e9edb5bba7649b6a1cc5bb5df4ee8b7ce1393664b581775ffa7345980e8532 over 32984 bytes and 379 lines, EQUAL to the digest the reviewer emitted and under the 490-line budget DECISION F085 D6 rules. SIX SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R35's predecessor PLANF008R34 17b7f5cd at 37 lines, PILLTO 9d7e18ba at 5, PILLFROM f8e95319 at 2, and single-line slices for R0593FROM d7dccc38, R0593TO a06b938c and LEDGER34 0b0f858d — none carrying trailing whitespace on any line, none beginning with a blank line, and each newline-terminated. THE PLAN LANDED FIRST at `340384ca`, byte-equal to PLANF008R34 at 37 lines under the 50-line cap. THE REWRITE at `dd1459d7` reads R0593FROM 1 at the base and 0 at C2 with R0593TO 0 and 1, the base blob with that one substitution is BYTE-EQUAL to the C2 blob, and the blank-line paragraph count is 244 on both sides with EXACTLY ONE paragraph differing, index 174, beginning `- R-0593 — `. THE LEDGER APPEND at `67dc5b6d` is proved twice over: the C2 blob is a byte-exact prefix of it with a 5616-byte remainder equal to a newline plus LEDGER34, and an INDEPENDENT split of the whole file gives 245 units whose LAST is LEDGER34's paragraph, with a one-byte printable flip REJECTED by BOTH readings and the unflipped value ACCEPTED by both. THE SETS HELD — 201 findings at the round base, at C2 and at C3 with NO id minted and R-0630 still 0, `- R-0368`, `- R-0429`, `- R-0553`, `- R-0593`, `- R-0628` and `- R-0629` 1 each and all OPEN, `Done:` 6, `Landed:` 0, `Gate: R` 33 at the base and at C2 and 34 at C3 over 34 DISTINCT keys, 33 of 34 headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match, and the R34 pair occurring exactly once. THE COMMENT RETIREMENT at `8ae77e92` is a REWRITE going PILLFROM 1 to 0 and PILLTO 0 to 1, the base blob with that one substitution BYTE-EQUAL to the C4 blob, 21 lines becoming 24 — and the reviewer measured the property the round's own constraint 3 claimed rather than trusting it: with block comments removed, the component's code at the base and at C4 is BYTE-IDENTICAL, so the edit really did touch nothing but prose. THE GATE IS THE REVIEWER'S OWN ON THE BRANCH SIDE: `python3 -m pytest -n auto -q` in the primary checkout at `2bacba10` EXITS 0 at `17412 passed, 20 skipped` in 151.4 s with 0 lines beginning FAILED — the same 17412 and 20 the worker's run at `8ae77e92` reported, reproduced at a later commit by a different actor. THE BASE SIDE IS THE WORKER'S, and its raw log survives on disk: `.remedy-wt/.cache/gate_r34/base_run.log` recomputes to the sha256 `full_log_provenance.txt` records, carries 0 lines beginning FAILED, and ends `17315 passed, 20 skipped` — its 97-test shortfall against the branch run being exactly the 97 ids the six F008 suites collect. BOTH `comm` SETS ARE 0, so no branch-only failure exists to attribute and no blocker is owed. THE PARITY CLAIM WENT VOID AND THE ROUND SAID SO, which is the honest outcome rather than the convenient one: the base worktree's `dist` digest and mtime both moved inside the run, the round chased the mover to ONE node id with a serial probe — `test_auto_build_runs_by_default`, which pops `REMEDY_UI_NO_AUTO_BUILD` itself and rebuilds into whichever checkout hosts it — and the primary checkout's digest, file count and mtime were unchanged across both runs. That probe also CORRECTS a reading this repository has carried since F255 R18: `auto-build (` appearing 0 times in a suite log means pytest captured it for a passing test, not that no build ran. SEVEN single-parent commits over `88c55f5d`..`3a648238`, insertions 379, 255, 13, 1, 2, 5 and 252 — every one under 500, 379 the maximum — with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `## Commits` column; the path set exactly the 14 the Change set names minus the handback's own; 0 marker lines in every committed target; 7 of 7 pre-C6 commits carrying `Co-Authored-By` and 8 of 8 after it; and a 93-line handback within the 100 eight commits allow. NO FINDING IS REGISTERED AGAINST THE WORKER, and the round earned more than a pass: it declared the parity void it could have buried, named the mover by direct probe, and corrected a false inference in the repository's own precedent — while every value it reported reproduced.
<<<END LEDGER35

<<<SLICE BUILTSTATE
## Built State — what F008 delivered

Read at `2bacba10`. A per-job SSE endpoint that streams the event ledger from a
cursor, and the cockpit client that consumes it — resume without renumbering,
an honest polling fallback, and a badge that says DELAYED rather than pretending
to be live.

- `packages/orchestration/ui_server.py` — the endpoint. It streams the ledger's
  OWN monotonic seq as the SSE event id and never assigns one, so a resume is a
  span of the ledger rather than a renumbering of it; a heartbeat holds the
  connection at cadence; `Last-Event-ID` replays exactly the missed span; and a
  connection cap answers over-subscription with 429 rather than with an
  unbounded thread count. The long-lived response required the server's
  threading shape to be settled first, which is what T001 measured before
  anything was built on it.
- `apps/ui/src/api/brainStream.ts`, `brainStreamDriver.ts`,
  `brainStreamRunner.ts`, `brainStreamHost.ts`, `brainStreamSession.ts` and
  `brainStreamDeps.ts` — the client, deliberately NOT React. Every rule the
  transport has lives in these modules, where the node-environment vitest can
  reach it: reconnect backoff, gap detection against the carried seq, the
  fallback that engages when EventSource is absent or fails, and the
  environment seam that reads its globals as an ARGUMENT — a contract test
  pins `globalThis` to zero occurrences in that module's COMMENT-STRIPPED
  source, which is what keeps the seam inside a node-environment vitest's
  reach. The two occurrences the word does have there are both in comments
  saying why the module does not read it.
- `apps/ui/src/api/useBrainStream.ts` — the only React in the feature: subscribe
  to a store, start it, close it on unmount. `makeDeps` is read through a ref
  rather than a dependency, because a caller that writes its deps inline hands a
  new function every render and a memo honouring that identity would tear down
  the stream and open a fresh EventSource on every parent render.
- `apps/ui/src/components/shell/RemedyShell.tsx` — where the two halves meet.
  The subscription sits in the shell rather than in `RemedyApp` (DECISION F008
  D3) because the shell renders only once a dashboard has loaded, so
  `dashboard.jobId` is always a real job, where `RemedyApp` would have to open a
  stream against an empty id on every URL that carries none.
- `apps/ui/src/components/panels/LiveStatusPill.tsx` and `RightLivePanel.tsx` —
  the acceptance surface. The TRANSPORT's status outranks the dashboard's
  liveness, because a client on the polling fallback is not live however active
  the job is; the dashboard arm is the fallback, not the rule.

Tests: `tests/ui_server/test_sse_stream.py`, `test_event_seq.py` and
`test_server_concurrency.py` on the server side; `tests/ui_contracts/
test_brain_stream_hook.py`, `test_live_status_pill.py` and
`test_remedy_shell_stream.py` on the client side, all reading COMMENT-STRIPPED
source because a guard that counted a token inside a comment would be satisfied
by the prose describing the code (R-0584); and the vitest suites beside each
client module, which is where the logic itself is exercised. This repository has
no DOM environment, which is the reason the React half is as thin as it is.
<<<END BUILTSTATE

<<<SLICE EVIDENCESCRIPT
"""F008 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f008_closure_evidence", "remedy-job-evidence-f008-closure"
)
BASE = "7c03adfa58519d484df685d38b950c49afaf70a8"
assert len(BASE) == 40, BASE

HEAD = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True
).stdout.strip()
assert len(HEAD) == 40, HEAD


def _tail(text):
    """The last 2000 chars on a WHOLE-LINE boundary, path-scrubbed TWICE.

    job_evidence._scrub_paths only relativises paths under REPO. A pytest header
    line can end in the interpreter's own absolute path, which
    build_review_manifest._unsafe_text correctly rejects as a local absolute
    path -> BLOCKED_EVIDENCE.
    """
    from packages.common.path_redaction import scrub_paths
    from packages.orchestration.job_evidence import _scrub_paths

    cut = text[-2000:]
    if len(text) > 2000 and "\n" in cut:
        cut = cut[cut.index("\n") + 1:]
    return scrub_paths(_scrub_paths(cut, REPO))


def mkrun(rid, path, expect):
    """One verification record. Node ids come from --collect-only, never from a
    -v log: a parametrized id can contain whitespace and a regex over -v output
    splits it (finding R-0611)."""
    assert re.match(r"^vr-\d{4,}$", rid), rid
    collect = subprocess.run(
        ["python3", "-m", "pytest", path, "--collect-only", "-q"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert collect.returncode == 0, (rid, collect.returncode)
    ids = [ln for ln in collect.stdout.split("\n") if ln.startswith("tests/")]
    run = subprocess.run(
        ["python3", "-m", "pytest", path, "-q"],
        cwd=REPO, capture_output=True, text=True,
    )
    text = run.stdout + run.stderr
    assert run.returncode == 0, (rid, run.returncode, text[-400:])
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    assert (passed, failed, skipped) == (expect, 0, 0), (rid, passed, failed, skipped)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = sorted({i.split("::")[0] for i in ids})
    assert files == sorted(files), rid
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": "python3 -m pytest " + path + " -q",
        "exit_code": 0, "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": 0, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": _tail(text),
    }


runs = [
    mkrun("vr-0001", "tests/ui_server/test_sse_stream.py", 65),
    mkrun("vr-0002", "tests/ui_server/test_event_seq.py", 7),
    mkrun("vr-0003", "tests/ui_server/test_server_concurrency.py", 1),
    mkrun("vr-0004", "tests/ui_contracts/test_brain_stream_hook.py", 9),
    mkrun("vr-0005", "tests/ui_contracts/test_live_status_pill.py", 7),
    mkrun("vr-0006", "tests/ui_contracts/test_remedy_shell_stream.py", 8),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "files", len(r["test_files"]), "dur", r["duration_seconds"])

now = datetime.now(timezone.utc)
from packages.orchestration.job_evidence import create_manual_completion_bundle  # noqa: E402

result = create_manual_completion_bundle(
    EVIDENCE_DIR,
    repo_root=REPO,
    base_commit=BASE,
    head_commit=HEAD,
    job_id="f008-closure",
    job_title="F008 SSE event stream - closure",
    step_range="T001-T003",
    prior_job_ids=["f255-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F008 closure",
    review_feature_id="f008",
)
print(json.dumps(result, indent=2, sort_keys=True))

# The output_hash preimage rule: sha256 over stdout_summary EXACTLY. This is the
# pitfall that blocked the F083 closure and it is not in the protocol's list.
vt = os.path.join(EVIDENCE_DIR, "verification_tests.json")
if os.path.isfile(vt):
    with open(vt, encoding="utf-8") as fh:
        doc = json.load(fh)
    for row in doc.get("runs", []):
        want = hashlib.sha256(row.get("stdout_summary", "").encode()).hexdigest()
        print("OUTPUT_HASH", row.get("run_id"), "matches sha256(stdout_summary):",
              row.get("output_hash") == want)
else:
    print("OUTPUT_HASH no verification_tests.json at", vt)
<<<END EVIDENCESCRIPT
