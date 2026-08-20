── STEP R17 — F086 Release capability (record R16; repair R-0584) ──

Goal:
Record R16's verdict and repair the defect its review found. R16 gave the release
gate its manual trigger and seven text guards, and the reviewer's own controls
show that three of those guards assert a positive existence over text that
INCLUDES the workflow's comments — two of them satisfiably so. Delete the shell
fallback that keeps an absent CI answer from reading green, or comment out the
only trigger the workflow has, and the suite stays at 7 passed either way. This
round registers that as R-0584, moves the three positive checks onto the file's
executable lines, and proves both mutations red afterwards against a base control
that is green.

THE WORKFLOW ITSELF IS CORRECT AND IS NOT TOUCHED. `.github/workflows/release.yml`
is not in this round's change set: the defect is in the guards over it, and a
round that edited both would be unable to say which half its red proof measured.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r17.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN17 slice, whole file
  C2  append FIND0584 then RECORD15 to `.agent/live_review.md`
  C3  apply the three FROM/TO pairs to
      `tests/orchestration/test_release_workflow.py`
  C4  append ONE `Landed: R-0584 — …` line to `.agent/live_review.md`
  C5  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C6  append the VERDICT slice to `.agent/handoff.md`

C1 precedes C2 because §3 item 23 requires the plan to advance before any commit
touching the finding ledger. C2 precedes C3 because §4 item 4 requires findings to
persist BEFORE their repair, so a session that dies mid-round leaves the defect on
disk rather than a silent fix. C4 follows C3 because a `Landed:` line asserts that
the fix is committed, and it may not be written before the commit it names exists.

Base:
This round starts from `4750383c`, the tip of `feature/f086-release-capability`
and the R16 handback commit. Every range gate names that SHA. Stay on the branch:
do NOT create one, merge, or open a PR — F086's PR belongs to its closure round.

Slice convention:
Each authored unit sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each programmatically by its markers and
apply it byte-verbatim; no marker line ever reaches a target file. PLAN17 is a
COMPLETE file including its single trailing newline. FIND0584, RECORD15 and
VERDICT are EOF-APPENDS: pure concatenation, each slice's own leading blank line
INSIDE the slice, nothing prepended, nothing stripped. PAIR1FROM/PAIR1TO,
PAIR2FROM/PAIR2TO and PAIR3FROM/PAIR3TO are single-line replacement pairs, each
line carrying its own four-space indentation and its trailing newline.

PAIR SHAPES, from the containment test run on these exact bytes at emission, one
reading per pair, never one reading generalised (§3 item 15):
  PAIR1  TO contains FROM: false  → REWRITE → FROM 0x and TO 1x are orderable
  PAIR2  TO contains FROM: false  → REWRITE → FROM 0x and TO 1x are orderable
  PAIR3  TO contains FROM: false  → REWRITE → FROM 0x and TO 1x are orderable

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `4750383c`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r17.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r17.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone. C0b then copies the COMMITTED `.agent/authored/f086-r17.md`
   over `.agent/last_block.md`, whole file, also alone.

2. C1 — `.agent/plan.md` := the PLAN17 slice, byte-verbatim, whole file. Alone.

3. C2 — append FIND0584 and then RECORD15 to `.agent/live_review.md`, in that
   order, under the append convention. Commit alone. FIND0584 registers the
   finding; RECORD15 is the reviewer's R16 verdict and begins `Gate:`.

4. C3 — apply the three pairs to
   `tests/orchestration/test_release_workflow.py`, all three in ONE commit: they
   are one repair of one class, and splitting them would leave the file in a state
   where the round's own finding is half true. Each FROM occurs exactly 1x in that
   file at `4750383c`; replace each with its TO. Change NOTHING else — not the
   docstrings, not `executable_lines()`, not the two guards that already read it,
   and not `.github/workflows/release.yml`.

5. C4 — append to `.agent/live_review.md` a blank line followed by exactly ONE
   line of YOUR OWN text, of the form
   `Landed: R-0584 — <one line: what changed, which commit>`, naming C3's real
   SHA. That line is the only text in this round you author into a tracked file.
   Do NOT write a `Done:` paragraph: §4 item 4 reserves `Done:` for
   reviewer-authored text, and the resolution is authored at the next gate once
   the reviewer has verified C3. Commit alone.

6. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 4750383c..<HEAD>`; write the literal token `HEAD`, this
   branch's convention from R10 onward, because a handoff cannot name the SHA of
   the commit that writes it.
   THE VERIFICATION SECTION IS A SUMMARY, NOT A TRANSCRIPT — one line per gate:
   its number, what it measured in a clause, and its real colour or value. This is
   the R-0582 repair, which has held at R14, R15 and R16; G14 measures it. The
   FULL transcript goes in your ROUND REPORT, which no cap binds.
   THE BUDGET IS ARITHMETIC: the VERDICT slice C6 appends is 44 lines, measured by
   the reviewer, so 56 of the 100 remain for your text. Measure it yourself from
   the COMMITTED C0a file before writing C5, and state the FINAL line count of
   `.agent/handoff.md` — your lines plus the slice's — in your Deviations section.
   Do NOT trim after C6.
   `Next` names, in order, the next session's first three actions: re-read
   `.agent/STOP` from disk (Phase 1 rule 1), run the Open PR Gate (rule 2), then
   review `4750383c..HEAD` and record R17's verdict (rule 4).

7. C6 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C5 must be a byte-exact PREFIX of the file at HEAD.

──────────────────────────────────────────────────────────────

Constraints:

1. Do not edit a slice. Every slice is applied byte-verbatim or the round stops.
2. The change set is EXACTLY these paths and nothing else:
   `.agent/authored/f086-r17.md`, `.agent/last_block.md`, `.agent/plan.md`,
   `.agent/live_review.md`, `tests/orchestration/test_release_workflow.py`, and
   `.agent/handoff.md` at C5 and C6. NOT `.github/workflows/release.yml`, not
   `scripts/release_gate_check.py`, not `packages/orchestration/release_gate.py`,
   not `pyproject.toml`, not `hatch_build.py`, not `.github/workflows/ci.yml`,
   not `CHANGELOG.md`, and nothing under `apps/` or `docs/`. All ten named files
   exist at `4750383c`, so the clause forbids something real (R-0559).
3. FIND0584, RECORD15 and VERDICT are the reviewer's text. Do not summarise or
   reformat them, and do not write a verdict of your own anywhere — in the
   handoff, in a commit message, or in your report. Reporting what a gate
   MEASURED is your job; ruling on a round is not. The C4 `Landed:` line is the
   single exception this block grants, and its form is fixed in step 5.
4. `git status --porcelain` in the PRIMARY checkout is EMPTY at every commit and
   at the handback. This round adds exactly TWO disposable worktrees — one at the
   round's HEAD for G9's mutations and one at `4750383c` for G9's base controls;
   both are removed and pruned before the handback, where `git worktree list`
   reads one line. Every other gate command runs in the PRIMARY checkout, and
   suites run SERIALLY — the second starts only after the first has ENDED
   (R-0518).
5. Shell loops, `$( )`, `${arr[0]}`, brace-with-quote literals and env-prefix
   command forms are refused by this session's Bash guard. Route that work
   through `python3 - <<'PY'` heredocs or scripts under `.remedy-wt/`. The
   mutation strings in G9 legitimately contain such shell forms — they are bytes
   you WRITE into a YAML file, never a command you run.
6. SIZE, measured at emission on the final bytes: this block is 414 lines TOTAL —
   294 prose and 120 slice including its 20 marker lines — against DECISION F085
   D6's 490 total and D5's 400 prose. Re-measure both from the COMMITTED C0a file
   and report your readings.

──────────────────────────────────────────────────────────────

Done when:

G1  HYGIENE. `git status --porcelain` EMPTY in the primary checkout at every
    commit and at the handback; `.agent/STOP` absent, re-read from disk before
    C0a and again at the handback; branch `feature/f086-release-capability`.

G2  TRANSPORT. `.remedy-wt/f086-r17.md`, the committed
    `.agent/authored/f086-r17.md` and the committed `.agent/last_block.md` are all
    three byte-EQUAL. Report the sha256 IN FULL — all 64 hex characters, never
    elided (R-0581) — plus the byte count and the line count.

G3  PLAN. `.agent/plan.md` at HEAD is byte-equal to the PLAN17 slice extracted
    from the COMMITTED `.agent/authored/f086-r17.md`. Report its full sha256 and
    line count, confirm the count is under 50, and confirm it contains `## Goal`,
    `## Next Steps` and `F086`.

G4  THE TWO LEDGER APPENDS. The pre-C2 blob of `.agent/live_review.md` is a
    byte-exact PREFIX of the post-C2 blob and that remainder is byte-equal to
    FIND0584 followed by RECORD15; report the remainder's own full sha256 and its
    line count. Separately, the post-C2 blob is a byte-exact PREFIX of the post-C4
    blob and THAT remainder is a blank line plus exactly one line matching
    `^Landed: R-0584 — `; report the remainder verbatim.

G5  LEDGER SETS, BOTH EXTRACTIONS. Extract twice — once by PARAGRAPH (split on
    blank lines; a paragraph counts when it STARTS with `- R-\d+ — ` or
    `Done: R-\d+ — `) and once LINE-ANCHORED (`^- R-\d+ — ` and `^Done: R-\d+ — `).
    At HEAD report registered / resolved / duplicate ids / unregistered
    resolutions / anchored `Landed:` lines / open, for BOTH, and the two
    registered id SETS must be EQUAL. Expected at HEAD: 167 registered, 2
    resolved, 0 duplicates, 0 unregistered resolutions, 1 `Landed:` line, 165
    open. Report the symmetric difference of the HEAD registered set against the
    `4750383c` set AS THE SET; it must be exactly `['R-0584']`.
    CONTROL: the SAME extractor over `6f5a589a..efc021d9` must read `['R-0583']`,
    so a reading of `['R-0584']` above is a difference the extractor can see
    rather than an artefact of the range.

G6  NO MARKER LEAKED. `.agent/plan.md`, `.agent/live_review.md`,
    `.agent/handoff.md` and `tests/orchestration/test_release_workflow.py` at HEAD
    each contain 0 lines beginning `<<<SLICE ` or `<<<END `. Count marker LINES,
    not `<<<`.

G7  THE THREE PAIRS LANDED, AND NOTHING ELSE DID. In
    `tests/orchestration/test_release_workflow.py`: at `4750383c` each FROM occurs
    exactly 1x and each TO exactly 0x; at HEAD each FROM occurs exactly 0x and
    each TO exactly 1x — six counts before and six after, reported one by one.
    Then the ORDERED-EQUALITY reading that no count can give: the file at HEAD is
    byte-equal to the base blob with each FROM occurrence replaced by its TO and
    nothing else changed, and `git show --numstat 4750383c..HEAD --
    tests/orchestration/test_release_workflow.py` reads 3 insertions and 3
    deletions. Report the file's full sha256 and line count at HEAD; the line
    count must be unchanged at 70.

G8  THE RELEASE SUITES, in the PRIMARY checkout: `python3 -m pytest
    tests/orchestration/test_release_workflow.py
    tests/orchestration/test_release_gate_wiring.py
    tests/orchestration/test_release_gate.py -q -rf` → exit 0, 28 passed.

G9  RED PROOFS WITH BASE CONTROLS — THE REPAIR CHANGED SOMETHING, AND EACH GUARD
    FAILS FOR ITS OWN REASON. Two disposable worktrees: MUT at the round's HEAD
    (repaired guards) and BASE at `4750383c` (the guards as R16 left them). In
    EACH worktree apply the mutations below to `.github/workflows/release.yml` one
    at a time, reverting fully between them, and after each run `python3 -m pytest
    <that worktree>/tests/orchestration/test_release_workflow.py -q -rf` →
      (a) in the single line
          `          echo "conclusion=${found:-missing}" >> "$GITHUB_OUTPUT"`,
          counted 1x in that file first, write
          `          echo "conclusion=$found" >> "$GITHUB_OUTPUT"` instead.
          MUT → exit 1, 1 failed / 6 passed, naming ONLY
          `test_release_workflow_refuses_when_no_ci_run_is_found`.
          BASE → exit 0, 7 passed. That green IS the finding.
      (b) replace the single line `  workflow_dispatch:`, counted 1x in that file
          first, with `  # workflow_dispatch:`.
          MUT → exit 1, 1 failed / 6 passed, naming ONLY
          `test_release_workflow_is_triggered_by_hand_only`.
          BASE → exit 0, 7 passed. That green is the second instance.
      (c) in the single line
          `          python3 scripts/release_gate_check.py --tag "$TAG" \`,
          counted 1x in that file first, write
          `          python3 scripts/release_gate_check.py --tag '${{ inputs.tag }}' \`
          instead. MUT → exit 1, 1 failed / 6 passed, naming ONLY
          `test_release_workflow_passes_the_tag_through_the_environment`. BASE →
          exit 1 as well: that guard was already sound and the repair did not
          weaken it, which is why (c) has no green control to report.
    After the last revert in each worktree, re-run and report 7 passed at exit 0
    with that worktree's `git status --porcelain` EMPTY. Report the six exit codes
    and the names you actually saw, never the names ordered here.

G10 RUFF, BY MULTISET RATHER THAN BY EXIT CODE. `python3 -m ruff check
    tests/orchestration/test_release_workflow.py` at `4750383c` and at HEAD; the
    rule-code MULTISETS must be equal. Read the base one in a disposable worktree
    or from `git show`, never in a checkout standing at HEAD (R-0532), and report
    both multisets even when both are empty. That file is the round's only
    Python path.

G11 CANARY AND THE STATE READERS, in the PRIMARY checkout, serially: `python3 -m
    pytest tests/orchestration/test_test_runner.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, 160 passed; then
    `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42 passed.
    State that they did not overlap.

G12 HISTORY AND COMMIT SIZE. Every commit in `4750383c..HEAD` has exactly one
    parent, the chain is linear, and `git reflog` over this round shows only
    `commit:` entries — no amend, rebase, reset, force-push. Report the chain, and
    with it the INSERTION count — the `+` column of `git show --numstat` — for
    every commit BEFORE C5, one each; none over 500. C5's and C6's own go in the
    round report (§3 item 14).

G13 CHANGE SET. `git diff --name-only 4750383c..HEAD` before C5 is exactly the
    five paths of constraint 2 other than `.agent/handoff.md`. Confirm with `git
    ls-tree 4750383c -- <path>` that every path constraint 2 FORBIDS exists at the
    base, so the prohibition forbids something real.

G14 THE HANDBACK. `.agent/handoff.md` at HEAD is AT MOST 100 lines and carries all
    seven mandated headings of docs/agents/handback_template.md in the template's
    order. Report the `wc -l` reading and the heading list. If it exceeds 100,
    declare the DECISION D15 overage with its cause rather than dropping a
    section.

G15 THE VERDICT APPEND. The `.agent/handoff.md` blob committed by C5 is a
    byte-exact PREFIX of the file at HEAD and the remainder is byte-equal to the
    VERDICT slice. Report the remainder's full sha256 and line count.

G16 OPEN PR GATE, re-read at the handback: `gh pr list --state open --json
    number,headRefName,baseRefName,isDraft`. Report its output. Create nothing,
    merge nothing.

Handback: your completion report with the FULL transcript, plus C5's rewrite of
`.agent/handoff.md` and C6's append, exactly as steps 6 and 7 specify.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN17>>>
# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs to
its closure round. `.agent/live_review.md` is the source of truth for the open set,
for the next free finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R17, this round: record R16's verdict, register finding R-0584 and repair it.
Three of the release workflow's seven text guards assert a positive existence over
text that includes the file's COMMENTS, and two of them are satisfied by a comment
alone — the `${found:-missing}` fallback can be deleted, and the only trigger the
workflow has can be commented out, with the suite green either way. All three
positive checks move onto the file's executable lines.

## Next Steps
1. The install smoke T2_F086 T001 still owes: a fresh virtualenv, the wheel
   installed into it, `remedy` on PATH, and the golden path and the UI serve
   probed from it. The round that writes it must rule, as a DECISION, WHERE that
   smoke executes — an opt-in marker, a `ci.yml` stage, or a step of
   `release.yml` — because no self-drive session can run it here.
2. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN. It is gated as TEXT, the way
   `tests/orchestration/test_ci_workflow.py` gates `ci.yml`. No round can
   dispatch it; its first real run is a human action, and its guards check what
   they say and nothing more.

## Risks
- The install smoke creates a fresh virtualenv and runs the wheel's console
  script. MEASURED at R17 rather than assumed: this session's permission layer
  refuses to execute an interpreter under `.remedy-wt/`, so a self-drive round can
  write that smoke but cannot run it, and the round that writes it says so.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
<<<END PLAN17>>>

<<<SLICE FIND0584>>>

- R-0584 — Medium — THREE OF THE RELEASE-WORKFLOW GUARDS ASSERT A POSITIVE EXISTENCE OVER TEXT THAT INCLUDES THE FILE'S COMMENTS, AND TWO OF THE THREE ARE SATISFIED BY A COMMENT ALONE. `tests/orchestration/test_release_workflow.py` at `4750383c` reads the workflow two ways: `executable_lines()` drops comment lines and is used by the guards that FORBID a token, while `workflow_text()` keeps them and is used by the three that REQUIRE one — `assert "missing" in workflow_text()`, `assert "workflow_dispatch:" in text` and `assert '--tag "$TAG"' in workflow_text()`. MEASURED by the reviewer in disposable worktrees at `4750383c`, one mutation at a time with a full revert between each: deleting the fallback in the single line `          echo "conclusion=${found:-missing}" >> "$GITHUB_OUTPUT"` — counted 1x in `.github/workflows/release.yml` first — leaves the suite at exit 0, 7 passed, because the word `missing` survives in the comment above it; and replacing the single line `  workflow_dispatch:`, also counted 1x there, with `  # workflow_dispatch:` ALSO leaves exit 0, 7 passed, because the commented-out line still contains the substring the guard looks for. WHY THIS IS A FINDING AND NOT A STYLE NOTE: `test_release_workflow_refuses_when_no_ci_run_is_found` exists to hold the property that an absent CI answer must not read as a green one, and that property lives entirely in a shell fallback whose deletion the guard cannot see; `test_release_workflow_is_triggered_by_hand_only` exists to hold the property that no event may fire the job, and it passes a workflow that has no trigger at all. Each names a property in its own docstring that it cannot fail on, which is the vacuous-gate class of R-0438 arriving through a comment rather than through a missing path. The third, the tag guard, is sound: the interpolation mutation R16 ran goes red at `4750383c` as well, and the fix does not weaken it. THE DEFECT IS THE REVIEWER'S — the GUARDS slice was reviewer-authored and applied byte-verbatim, so no worker deviation is implied. COUNTER-MEASURE, applied by this round's C3: each of the three asserts becomes `any(<needle> in line for line in executable_lines())`, after which both mutations above go red naming only their own test while the base stays green, which G9 measures at both commits rather than asserting.
<<<END FIND0584>>>

<<<SLICE RECORD15>>>

Gate: R17 — the R16 entry. R16 PASSED, with ONE finding — R-0584, registered by this round's own FIND0584 slice and repaired by its C3. Every gate its block ordered was re-executed by the reviewer over `efc021d9..4750383c` rather than read from the handback, and every reading reproduces. THE TRIGGER EXISTS AND IT IS MANUAL, read off the file itself rather than off the guards over it: `.github/workflows/release.yml` at `4750383c` fires on `workflow_dispatch` alone, carries the tag to the runner through the ENVIRONMENT instead of interpolating it into a shell line, calls `scripts/release_gate_check.py` exactly once, and holds no upload step and no index credential — which is what T2_F086's Do-not-touch requires of it. THE SUITES WERE RE-RUN, NOT READ, serially and non-overlapping in the PRIMARY checkout: 28 passed for the workflow guards, the wiring suite and the gate suite together, then 160 passed for the four state readers, then 42 passed for the canary, each exit 0, and `ruff check` over the round's one new Python path exits 0 with an EMPTY rule-code multiset. THE TRANSPORT HELD: the committed `.agent/authored/f086-r16.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 8a19f2caeb84fd375e47c74ada81837e644f2f80fb1ed33c6d2fe2a774b7b5b7, 29805 B over 490 lines, which is the size constraint 6 of that block declares of itself. EVERY SLICE LANDED BYTE-EXACT, each re-extracted from the committed block by its own markers with the reviewer's own extractor: `.agent/plan.md` equals PLAN16 at 54c7030cb5be1fec3d02c1d34f023aeba4b9efcfefae0a03cc76ab66979a3f64 over 43 lines; `.github/workflows/release.yml` equals WORKFLOW at 96119e7751c028c0f2b113d1bed3e8201ef8b946015ba5afffedb6ef9acd6547 over 72 lines and `tests/orchestration/test_release_workflow.py` equals GUARDS at 0ec4e46063124cc06524f36e24895b1c96e512812d910b347c313af0733d5875 over 70 lines, both ABSENT at `efc021d9` under `git ls-tree`, so both commits are creations; the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 2-line remainder equals RECORD14 at e135e5a583fd48d1ddb87bb83ae3ecdf8f897a3aedde51cf04accd275186b5db; and the C5 handoff blob is a byte-exact PREFIX of the file at `4750383c` whose 43-line remainder equals VERDICT at dd453f0ac247ddad42c7e5b56e4cc1c25c890534e530b6fe00b2553b33d0857f. NO MARKER LINE REACHED ANY TARGET: 0 lines beginning `<<<SLICE ` or `<<<END ` in any of the five written files. THE LEDGER DID NOT MOVE, WHICH IS WHAT THE ROUND CLAIMED: both extractions agree at each end at 166 registered / 2 resolved / 0 duplicate ids / 0 unregistered resolutions / 0 `Landed:` / 164 open with the two registered SETS equal, the symmetric difference across the range is empty, and the reviewer's control over `6f5a589a..efc021d9` reads exactly `['R-0583']`, so the extractor can see a difference. THE `Gate: ` PARAGRAPHS go from 13 to 14 and the added one names R15. THE HANDBACK STAYED UNDER ITS CAP for the third round running: 99 lines against 100, all seven mandated headings of docs/agents/handback_template.md present in the template's order, no DECISION D15 overage declared — the R-0582 repair is holding. THE HYGIENE HELD: seven paths over eight single-parent commits inserting 490, 362, 18, 2, 72, 70, 30 and 43 lines, none over 500 and no DECISION F104 D1 exemption invoked; `pyproject.toml`, `hatch_build.py`, `.github/workflows/ci.yml`, `scripts/release_gate_check.py` and `CHANGELOG.md` are absent from the range and all five exist at `efc021d9`. WHERE R16 FELL SHORT is in none of that, but in the GUARDS slice the reviewer itself authored: three of its seven guards assert a positive existence over text that includes the workflow's comments, and two of those three stay green when the property they name is deleted — which is R-0584, proved by the reviewer's own controls at this commit and repaired by this round.
<<<END RECORD15>>>

<<<SLICE PAIR1FROM>>>
    assert "missing" in workflow_text()
<<<END PAIR1FROM>>>

<<<SLICE PAIR1TO>>>
    assert any("missing" in line for line in executable_lines())
<<<END PAIR1TO>>>

<<<SLICE PAIR2FROM>>>
    assert "workflow_dispatch:" in text
<<<END PAIR2FROM>>>

<<<SLICE PAIR2TO>>>
    assert any("workflow_dispatch:" in line for line in executable_lines())
<<<END PAIR2TO>>>

<<<SLICE PAIR3FROM>>>
    assert '--tag "$TAG"' in workflow_text()
<<<END PAIR3FROM>>>

<<<SLICE PAIR3TO>>>
    assert any('--tag "$TAG"' in line for line in executable_lines())
<<<END PAIR3TO>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, a NEW session resuming the branch at
`4750383c`. The reviewer wrote nothing in the work tree, one delegated worker made
every commit, and the verdict below rests on gates the reviewer re-executed over
the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R16 | efc021d9..4750383c | PASS — one finding, R-0584, against the reviewer |
| R17 | 4750383c..HEAD | verdict not yet on disk; see the last paragraph |

R16 was inherited ungated, so Phase 1 rule 4 reviewed it before any new work was
planned. Its trigger is real and it is manual: the workflow fires on
`workflow_dispatch` alone, carries the tag through the environment rather than
into a shell line, calls the gate runner once, and publishes nothing. Every
transport, ledger, hygiene and suite reading its block ordered reproduces under
the reviewer's own commands, and the handback held its 100-line cap for the third
round running.

Its one defect is in the guards the reviewer itself authored, and only a control
the block never ordered could find it: three of the seven assert a positive
existence over text that includes the workflow's COMMENTS. Delete the shell
fallback that keeps an absent CI answer from reading as a green one, and the suite
stays at 7 passed because the word survives in a comment. Comment out the only
trigger the workflow has, and the suite stays at 7 passed for the same reason.
That is R-0584, and this round moves all three positive checks onto the file's
executable lines, after which both mutations go red naming only their own test
while the same mutations at `4750383c` stay green.

WHAT THIS FEATURE STILL OWES, unchanged by this round: the install smoke, whose
fresh-virtualenv step this session's permission posture cannot execute — measured,
not assumed — then the integration gate and closure. The release workflow has
never been dispatched, and no round can dispatch it.

R17 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last
verdict to be recorded. THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then
rule 2, then rule 4: review `4750383c..HEAD` and record R17's verdict in
`.agent/live_review.md` as `Gate: R18 — the R17 entry`.
<<<END VERDICT>>>
