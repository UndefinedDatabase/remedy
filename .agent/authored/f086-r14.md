── STEP R14 — F086 Release capability (record R13; close the session) ──

Goal:
Close this session on disk. Record the R13 verdict in the finding ledger and
write the reviewer's own session verdict into `.agent/handoff.md`, so that no
verdict this session issued exists only in a transcript — finding R-0571. This
is the LAST round of the session. No code, no test, no PR.

THIS ROUND ALSO APPLIES THE REPAIR R-0582 PROPOSES, and is the first test of it.
R-0582, registered at R13, is that the reviewer's blocks order more mandated
content into `.agent/handoff.md` than its 100-line cap admits, so DECISION D15's
declared-overage exception has become the rule: 113 lines at R10, 165 at R11,
223 at R12, 222 at R13. The cheaper of the two repairs it names — the one the
reviewer may make alone, without touching AGENTS.md — is to stop ordering the
full per-gate transcript into the handback and order it into the ROUND REPORT
instead, keeping the handback to the state the next session actually needs.
G8 below is that repair stated as a measurable obligation, and it can fail.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r14.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN14 slice, whole file
  C2  append RECORD12 to `.agent/live_review.md`
  C3  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C4  append the VERDICT slice to `.agent/handoff.md`

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger. This round registers NO finding —
R13 produced none — so the open set does not move and no FINDINGS slice exists.

WHY C4 EXISTS AND WHY IT APPENDS. A branch's last round has no on-disk gate entry
by construction (docs/agents/planner_reviewer_prompt.md §4 item 13), so a session
ending after its final verdict leaves that verdict nowhere. C4 APPENDS rather
than rewrites because a rewrite of `.agent/handoff.md` is exactly what destroys a
verdict already written into it.

Base:
This round starts from `a662abcc`, the tip of `feature/f086-release-capability`
and the R13 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. PLAN14 is a
COMPLETE file including its single trailing newline. RECORD12 and VERDICT are
EOF-APPENDS: pure concatenation, each slice's own leading blank line INSIDE the
slice, nothing prepended, nothing stripped. No FROM/TO pair exists in this block.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `a662abcc`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r14.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r14.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone. C0b then copies the COMMITTED `.agent/authored/f086-r14.md`
   over `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN14 slice, byte-verbatim, whole file. Commit
   alone.

3. C2 — append RECORD12 to `.agent/live_review.md` under the append convention.
   Commit alone. It is the reviewer's R13 verdict; it begins `Gate:` and
   registers no finding id, so it moves no ledger set.

4. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of a662abcc..<HEAD>`; write the literal token `HEAD`, which
   is this branch's convention from R10 onward, because a handoff cannot name the
   SHA of the commit that writes it.
   THE VERIFICATION SECTION IS A SUMMARY, NOT A TRANSCRIPT. Give one line per
   gate: its number, what it measured in a clause, and its real colour or value.
   Do NOT paste command output, do NOT reproduce full digests there, and do NOT
   write a per-gate paragraph. The FULL transcript — every command, its real exit
   code, its output and every digest at 64 characters — goes in your ROUND
   REPORT, which is where a reader who wants to re-derive a reading will look and
   which no cap binds. This is the R-0582 repair; G8 measures it.
   THE BUDGET IS ARITHMETIC, NOT A HOPE, and the reviewer measured it before
   ordering it: the VERDICT slice C4 appends is 43 lines, so 57 of the 100 remain
   for your text. A layout that fits with margin: title 2, Range 4, Commits 11 as
   ONE flat six-row table, External actions 4, Verification 17 as one line for
   each of the 14 gates, Authored-text proofs 4, Deviations 5, Next 4 — 51 in
   total. If you cannot fit, do not silently overrun: report which section would
   not compress and by how much.
   BEFORE writing C3, measure the VERDICT slice's own line count from the
   COMMITTED `.agent/authored/f086-r14.md`, because C4 appends exactly those
   lines. Your `Deviations & assumptions` section states the FINAL line count of
   `.agent/handoff.md` as it will stand after C4 — your own lines plus the
   slice's. Do NOT trim after C4. Report your own C3 insertion count and the
   post-C3 path set in the ROUND REPORT, not in the file (§3 item 14).
   The `Next` section names, in this order, the next session's first two actions:
   re-read `.agent/STOP` from disk (Phase 1 rule 1), then run the Open PR Gate
   (Phase 1 rule 2).

5. C4 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C3 must be a byte-exact PREFIX of the file at HEAD.

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r14.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, and `.agent/handoff.md` at C3 and C4. No path under
   `apps/`, `packages/`, `tests/`, `docs/` or `scripts/` is in it, and neither
   `pyproject.toml` nor `hatch_build.py` is: this round changes no behaviour and
   ships no code.
3. The VERDICT slice is the reviewer's text. Do not summarise it, do not reformat
   it, and do not write a verdict of your own anywhere — in the handoff, in a
   commit message, or in your report. Reporting what a gate MEASURED is your job;
   ruling on a round is not.
4. `git status --porcelain` in the primary checkout is EMPTY at every commit and
   at the handback, and `git worktree list` is exactly one line throughout. This
   round adds no worktree: it has nothing destructive to check.
5. Both suite commands run in the PRIMARY checkout, never in a worktree, and
   SERIALLY — the second starts only after the first has ENDED (R-0518).
6. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`.
7. SIZE, measured at emission: 330 lines TOTAL — 236 prose, 94 slice including
   6 marker lines — against DECISION F085 D6's 490 total and D5's 400 prose.
   Re-measure both from the COMMITTED C0a file and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `git worktree list` exactly 1 line; `.agent/STOP`
    absent, re-read from disk before C0a and again at the handback; branch
    `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r14.md`, the committed
    `.agent/authored/f086-r14.md` and the committed `.agent/last_block.md` are
    all three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters,
    never elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN14 slice extracted
    from the COMMITTED `.agent/authored/f086-r14.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
    PREFIX of the post-C2 blob and the remainder is byte-equal to RECORD12.
    Report the remainder's full sha256 and line count.

G5  LEDGER SETS, BOTH EXTRACTIONS, AND THEY MUST NOT MOVE. Extract twice — once
    by PARAGRAPH (split on blank lines; a paragraph counts when it STARTS with
    `- R-\d+ — ` or `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and
    `^Done: R-\d+ — `). At HEAD report registered / resolved / duplicate ids /
    unregistered resolutions / anchored `Landed:` lines / open, for BOTH, and the
    two registered id SETS must be EQUAL. Expected at HEAD: 165 registered, 2
    resolved, 0 duplicates, 0 unregistered resolutions, 0 `Landed:`, 163 open.
    Report the symmetric difference of the HEAD registered set against the
    `a662abcc` set as the SET itself; it must be EMPTY, this round registering
    nothing. CONTROL: report what the SAME extractor reads as added across
    `3351878d..a662abcc`; it must be `['R-0582']`, which is what proves the
    extractor can see a difference at all rather than being blind.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md` and
    `.agent/handoff.md` at HEAD each contain 0 lines beginning `<<<SLICE ` or
    `<<<END `. Count marker LINES, not `<<<` substrings.

G7  THE LEDGER CARRIES A VERDICT FOR EVERY REVIEWED ROUND OF THIS BRANCH. Count
    the paragraphs in `.agent/live_review.md` beginning `Gate: ` and report the
    count with the round each names. At `a662abcc` the reviewer measured 11,
    naming R3 through R13; C2 adds the twelfth, so HEAD must read 12 and the
    added one must name R14. R14's OWN entry is absent by construction and that
    absence is the terminator, not a gap — do NOT add one.

G8  THE R-0582 REPAIR HELD, AND THIS GATE CAN FAIL. Report the line count of
    `.agent/handoff.md` at HEAD — after C4, so including the appended VERDICT
    slice. It must be AT MOST 100, the AGENTS.md cap, with NO DECISION D15
    overage declared. Report alongside it the four measurements the finding
    names — 113 at R10, 165 at R11, 223 at R12, 222 at R13 — each re-derived by
    you from that file's blob at the commit concerned, not copied from this
    block. If HEAD exceeds 100, say so plainly and declare the overage as before:
    a repair that did not work is a finding, and hiding it would be worse than
    the overage it was meant to fix. Separately, confirm the file still holds all
    seven mandated headings of docs/agents/handback_template.md in order — the
    repair moves the transcript out, it does not drop a section.

G9  THE VERDICT LANDED AND NOTHING ELSE MOVED. `.agent/handoff.md` as committed
    by C3 is a byte-exact PREFIX of the file at HEAD, and the remainder is
    byte-equal to the VERDICT slice. Report the remainder's full sha256 and line
    count.

G10 ROUND GATE SUITE AND CANARY. `python3 -m pytest
    tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed;
    then `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42
    passed. Both in the PRIMARY checkout, the second started only after the first
    ENDED; state that they did not overlap.

G11 COMMIT SIZE. Report the INSERTION count — the `+` column of `git show
    --numstat` — for every commit in `a662abcc..HEAD` BEFORE C3, one line each;
    none may exceed 500. Report C3's own and C4's in the round report.

G12 HISTORY. Every commit in `a662abcc..HEAD` has exactly one parent, the chain
    is linear, and `git reflog` over this round shows only `commit:` entries — no
    amend, rebase, reset, force-push. Report the chain.

G13 PATH SET. `git diff --name-only a662abcc..HEAD`, measured before C3, is
    exactly `.agent/authored/f086-r14.md`, `.agent/last_block.md`,
    `.agent/live_review.md` and `.agent/plan.md`. Report the post-C3 set in the
    round report. Confirm `pyproject.toml`, `hatch_build.py` and every path under
    `apps/`, `packages/`, `tests/`, `docs/` and `scripts/` are ABSENT, and
    confirm with `git ls-tree a662abcc` that all seven EXIST at the base, so the
    clause forbids something real.

G14 OPEN PR GATE, READ-ONLY. `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft` → report it verbatim; merge nothing.

Handback:
A FULL completion report — every gate, its real command, its real exit code, its
output and every digest at 64 characters — plus a SHORT rewritten
`.agent/handoff.md` per C3. The report carries the transcript; the handoff
carries the state. Push after C2 and again after C4. "Green" as a word is a
finding. If a gate is red, say so plainly with the raw output and hand off.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN14>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs
to its closure round. `.agent/live_review.md` is the source of truth for the open
set, for the next free finding id and for the round map; this file repeats none
of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R14, this round: close the session. Record the R13 verdict, write the reviewer's
own session verdict to disk (finding R-0571), and apply the R-0582 repair by
keeping the handback under its cap with the transcript in the round report. No
code, no test, no PR.

## Next Steps
1. R15 — the DATA and the CALLER that R13 left out: a keep-a-changelog
   `CHANGELOG.md` with a section for the version `pyproject.toml` declares, a
   test that the real changelog covers the real version, and a manual-trigger
   release workflow calling `refuse_release` with the real tag, version,
   changelog and wheel size. UNTIL THAT LANDS THE GATE REFUSES NOTHING, because
   nothing calls it.
2. Then the install smoke, the integration gate, and closure. The packaging
   ist-doc is written at closure, when the built state stops moving.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches.
<<<END PLAN14>>>

<<<SLICE RECORD12>>>

Gate: R14 — the R13 entry. R13 PASSED, with NO finding. Every gate its block ordered was re-executed by the reviewer over `3351878d..a662abcc` rather than read from the handback, and every reading reproduces. THE GATE REFUSES FOR EACH REASON AND ACCEPTS OTHERWISE, measured by the reviewer outside pytest so the tuples themselves could be read rather than a count of them: from one accepting request, `refuse_release` returns `()` unchanged, `('CI is not green for this commit',)` with `ci_green=False`, `("tag 'v9.9.9' does not match distribution version '1.2.3'",)` on a tag mismatch, `("CHANGELOG.md has no section for version '1.2.3'",)` on a changelog with no such section, and `('wheel is 8388609 B, over the 8388608 B budget',)` one byte over the budget. Each seeded case trips the rule it was seeded for and no other, which a refusal COUNT could not have shown. THE PARSER CAN SAY NO: `changelog_section` returns None for a version absent from the text, without which the missing-section case would prove nothing. THE TESTS CAN FAIL: 12 passed at exit 0 in the primary checkout, and in a worktree at HEAD each of the two ordered mutations — the wheel-budget condition and the CI condition each turned to `if False:`, each line counted 1x in its file first — reads 2 failed / 10 passed, returning to 12 passed on revert with that worktree's `git status --porcelain` EMPTY. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original, the committed `.agent/authored/f086-r13.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 85312d57f16691d20c9d33b2186ea5ee6d251e15df3fa8a95a4d864d840c5f5b, 30339 B, 490 lines, and the block's own size sentence — 490 total, 246 prose, 244 slice — is what the reviewer re-measures from the committed file. EVERY SLICE LANDED BYTE-EXACT: `.agent/plan.md` equals PLAN13 at cd794e8cc754acb919f312450a0187e4d736118d9a12abe5608191b66d1a648e over 42 lines; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob with the 4-line remainder equal to FIND0582 followed by RECORD11 at 049b4b04e6103d2eb077af7551658387f8dd116df42985e6125332beb257ea28; `packages/orchestration/release_gate.py` equals GATE at e881d61d647e30ef622bbd85c73bfb365013d4474d1a710e9ef6dec77efc9384 over 82 lines and `tests/orchestration/test_release_gate.py` equals TESTS at e5150cd74f7a237d30ad85df144b3bb900a606f221961d690705cde2fc872454 over 106 lines, both ABSENT at `3351878d`. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the five written files. THE LEDGER MOVED BY EXACTLY ONE ID: both extractions AGREE at each end, 164 registered / 2 resolved / 162 open at `3351878d` and 165 / 2 / 163 at HEAD, with the symmetric difference of the registered sets exactly `['R-0582']` under both; the `Gate: ` paragraphs go from 10 to 11 and the added one names R13. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the primary checkout: 12 passed for the gate suite, 20 for the two CI-stage readers, 160 for the four state readers and 42 for the canary, each exit 0. RUFF IS CLEAN ON WHAT THE ROUND ADDS: exit 0 with an EMPTY rule-code multiset over both new files, measured in a worktree at HEAD; there is no base reading to compare against because both paths are new, which the block says rather than inventing one. THE HYGIENE HELD: seven paths over seven single-parent commits inserting 490, 305, 11, 4, 82, 106 and 176 lines, none over 500; `pyproject.toml`, `.github/workflows/ci.yml`, `hatch_build.py`, `apps/cli/version_report.py` and `packages/orchestration/ci_stages.py` are absent from the range and all five exist at the base, and `CHANGELOG.md` is absent from the range AND at the base, which the block ordered reported precisely so the clause would not forbid nothing (R-0559). WHAT THIS ROUND DELIBERATELY DID NOT DO, recorded so no reader mistakes a bounded round for a finished one: nothing calls this gate. The changelog it parses and the workflow that would supply a real tag, version and wheel size are R15's work, and until they land the gate refuses nothing.
<<<END RECORD12>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md. The reviewer wrote nothing in the work tree,
one delegated worker per round made every commit, and every verdict below rests
on gates the reviewer re-executed over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R11 | dea9dc2f..ee22186c | PASS — one finding, R-0581, against the reviewer |
| R12 | ee22186c..3351878d | PASS — no finding |
| R13 | 3351878d..a662abcc | PASS — no finding |
| R14 | a662abcc..HEAD | terminator; §4 item 13 gives it no ledger entry |

R11 was inherited unreviewed — the stranding DECISION F085 D9 warns about — so
reviewing it first was Phase 1 rule 4. Every ordered property held; its one
defect was in the evidence record, a transport digest reported ending
`f9ff257fc2` where the true one ends `f1fa257fc2`. That is R-0581 and not a
failure: "report the sha256" is a shape no wrong value violates, and the
convention wrote digests ELIDED. Every digest ordered since is in full.

R12 closed what T002 owed, proved on a real wheel built outside this repository:
417 members, one REVISION member at `<dist-info>/extra_metadata/REVISION` whose
bytes equal the probe worktree's own HEAD, against a base build that also exits
0 — so the control ran — and ships 416 with none. It also fixed a reader that
could never have worked, hatchling prefixing hook metadata with
`extra_metadata/`. R13 landed T003's decision half: `refuse_release` refuses on
red CI, a tag not matching the version, a missing or empty changelog section, and
a wheel over an 8 MiB budget, one seeded-failure test each.

WHAT THIS FEATURE STILL OWES: nothing calls the release gate. `CHANGELOG.md` does
not exist and no workflow supplies a real tag, version or wheel size — R15's
work, and until it lands the gate refuses nothing. Then the install smoke, whose
fresh-virtualenv step this session's permission posture cannot execute, then the
integration gate and closure.

All three findings this session registered are defects in the reviewer's own
instrumentation, not in the work under review, which passed every gate it was
given. G8 is the first gate this reviewer has written that can fail on the
reviewer's own habit.
<<<END VERDICT>>>
