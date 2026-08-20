── STEP R8 — F086 Release capability (repair the ledger separation; close the session) ──

Goal:
Repair the defect R7's G5 exposed: four findings landed as ONE paragraph block,
so the extractor that carries the open set forward at the next feature claim can
see only the first of them. Register the two defects, restore the separation
without altering one byte of any finding's text, record the R7 verdict, and close
this session with the reviewer's own session verdict written to disk. This is the
LAST round of the session. No code, no test, no PR.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r8.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN8 slice, whole file
  C2  append the FINDINGS2 slice to `.agent/live_review.md`
  C3  THE REPAIR — separate the R-0574…R-0577 paragraphs in `.agent/live_review.md`
  C4  append the RESOLUTION slice to `.agent/live_review.md`
  C5  append the RECORD6 slice to `.agent/live_review.md`
  C6  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C7  append the VERDICT slice to `.agent/handoff.md`

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger. C2 precedes C3 because
docs/agents/planner_reviewer_prompt.md §4 item 4 requires findings to persist in
their own commit BEFORE the fix, so nothing is lost if the session dies mid-round.
C4 marks R-0578 resolved and may only follow the commit that actually repairs it.

Why C7 exists and why it APPENDS. Finding R-0571, registered by this feature, is
that a verdict issued and never written to disk is indistinguishable from one
never issued: a branch's last round has no on-disk gate entry by construction
(docs/agents/planner_reviewer_prompt.md §4 item 13). It APPENDS rather than
rewrites because a rewrite of `.agent/handoff.md` is what destroys a verdict
already written into it.

Base:
This round starts from `b769ccd7`, the tip of `feature/f086-release-capability`
and the R7 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN8, FINDINGS2, RESOLUTION, RECORD6 and VERDICT. PLAN8 is the
COMPLETE file including its single trailing newline. FINDINGS2, RESOLUTION,
RECORD6 and VERDICT are EOF-APPENDS, defined as pure concatenation with each
slice's own leading blank line INSIDE the slice, so nothing is prepended and
nothing is stripped. No FROM/TO pair exists in this block; C3 is a specified
transformation, not a pair, and G6 measures it by its properties.

FINDINGS2 carries its two findings separated by a BLANK LINE, which is the very
property R-0578 exists to record. Apply it byte-verbatim and that separation
arrives with it; G5 measures that both new ids are visible to the paragraph
extractor and not only to a line-anchored one.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `b769ccd7`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r8.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r8.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r8.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN8 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the FINDINGS2 slice to `.agent/live_review.md` under the append
   convention. Commit alone. It registers R-0578 and R-0579, both defects in the
   REVIEWER's own R7 gates and neither a defect of your work.

5. C3 — THE REPAIR. In `.agent/live_review.md`, the lines beginning
   `- R-0575 — `, `- R-0576 — ` and `- R-0577 — ` each currently follow the
   previous finding with NO blank line between them. Insert exactly ONE blank
   line before each of those three lines. Change nothing else: no finding's text
   may gain, lose or alter a single byte, and no other line in the file may move
   except by that insertion. Do this PROGRAMMATICALLY — read the file, insert the
   three newlines, write it back — never by retyping a finding. Commit alone.
   G6 measures the result by properties, not by a predicted diff shape, so do not
   try to make any particular numstat appear.

6. C4 — append the RESOLUTION slice to `.agent/live_review.md` under the append
   convention. Commit alone. It is the reviewer's text marking R-0578 resolved;
   only reviewer-authored text sets a resolution.

7. C5 — append the RECORD6 slice to `.agent/live_review.md` under the append
   convention. Commit alone. The paragraph begins `Gate:` and registers no
   finding id, so it moves no ledger set.

8. C6 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of b769ccd7..<HEAD>`.
   BEFORE writing it, measure the VERDICT slice's own line count from the
   COMMITTED `.agent/authored/f086-r8.md`, because C7 appends exactly those lines
   to this file. Your `Deviations & assumptions` section states the FINAL line
   count of `.agent/handoff.md` as it will stand after C7 — your own lines plus
   the slice's — and, if that total exceeds the cap, declares the overage under
   AGENTS.md DECISION D15 naming its cause: this round carries the reviewer's
   authored session verdict, which is mandated content for the round that closes
   a session, and no section is dropped to meet the cap. Do NOT trim after C7.
   The `Next` section names, in this order, the next session's first two actions:
   re-read `.agent/STOP` from disk (Phase 1 rule 1), then run the Open PR Gate
   (Phase 1 rule 2).

9. C7 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C6 must be a byte-exact PREFIX of the file at HEAD, and G9 measures
   exactly that.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If one cannot be applied as-is, stop and
   declare it — never adjust the bytes to make a gate pass.
3. This round writes NO code and NO test. No path under `packages/`, `apps/`,
   `tests/`, `docs/` or `scripts/`, and not `pyproject.toml`, is touched. G11
   measures the change set exactly.
4. Never force-push, never rebase, never amend, never work on `main`, never delete
   a branch, and do not create one. Do NOT create a pull request.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write the
   handoff and end.
6. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, exit code and output, and hand back.
7. The VERDICT slice is the reviewer's text. Do not summarise it, do not reformat
   it, and do not write a verdict of your own anywhere: a worker-authored verdict
   is a finding however honestly it is hedged
   (docs/agents/planner_reviewer_prompt.md §4 item 4).

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is ONE
    line. `.agent/STOP` absent. Branch still `feature/f086-release-capability`.
G2  TRANSPORT: `.remedy-wt/f086-r8.md`, the committed `.agent/authored/f086-r8.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN8 slice extracted from the
    COMMITTED `.agent/authored/f086-r8.md`, contains `## Goal`, `## Next Steps`
    and a match of `\bF\d{3}\b`, and is under 50 lines. Report sha256 and lines.
G4  APPEND SHAPES. `.agent/live_review.md` is a byte-exact PREFIX of itself at each
    of the three append steps: at `b769ccd7` into the file after C2, after C3 into
    the file after C4, and after C4 into the file after C5; and the three
    remainders are exactly FINDINGS2, RESOLUTION and RECORD6, byte for byte.
    Report each prefix check as True or False and each remainder's sha256. C3 is
    NOT an append and is excluded from this gate; G6 covers it.
G5  LEDGER ARITHMETIC, BY BOTH READINGS, WHICH MUST AGREE. Two extractions over
    `.agent/live_review.md`. PARAGRAPH: split on runs of blank lines into blocks;
    a finding paragraph is any block whose FIRST line matches `^- R-\d+ — `, the
    whole block and never its first line. LINE-ANCHORED: every line matching
    `^- R-\d+ — `. A resolution is a line matching `^Done: R-\d+ — `; a `Landed:`
    line is one matching `^Landed: R-\d+`, ANCHORED at line start and never
    counted as a substring (finding R-0575). Report, at `b769ccd7` and at HEAD,
    under BOTH extractions: registered, resolved, duplicate ids, resolutions
    naming an unregistered id, anchored `Landed:` lines, and the OPEN set size.
    The reviewer measured at `b769ccd7`: PARAGRAPH 157 registered, LINE-ANCHORED
    160 registered — they DISAGREE, and that disagreement is finding R-0578.
    REQUIRED at HEAD: both extractions report 162 registered, 2 resolved, 0
    duplicates, 0 unregistered resolutions, 0 anchored `Landed:` lines and 160
    open, and the ids each adds over `b769ccd7`'s LINE-ANCHORED set are exactly
    R-0578 and R-0579 — report the set differences themselves, not just their
    sizes. The two readings agreeing at HEAD while disagreeing at `b769ccd7` is
    the property this round exists to restore, and `b769ccd7` is its control.
G6  THE REPAIR CHANGED SEPARATION AND NOTHING ELSE. Between `b769ccd7` and the C3
    commit, over `.agent/live_review.md`, report all four:
      (a) the multiset of lines matching `^- R-\d+ — ` is IDENTICAL — same lines,
          same count, byte for byte. Report the count and that the symmetric
          difference is empty.
      (b) the file with ALL blank lines removed is byte-IDENTICAL before and
          after. Report True or False and both sha256 digests.
      (c) the byte length increases by exactly 3.
      (d) `- R-0575 — `, `- R-0576 — ` and `- R-0577 — ` are each preceded by
          exactly one blank line at the C3 commit, and the count of finding lines
          NOT preceded by a blank line is 0 across the WHOLE file. The reviewer
          measured that count as 3 at `b769ccd7`, so this check can fail.
    Do NOT assert any `git show --numstat` value for C3: a separator insertion
    serialises as a rewritten hunk and predicting its shape is the defect class
    this repository already carries.
G7  RESOLUTION integrity: `Done: R-0578 — ` occurs exactly 1x at HEAD, R-0578 is
    among the registered ids under BOTH extractions, and no resolution names an id
    that is not registered.
G8  `.agent/live_review.md` contains `Steps`, and NO LINE of it begins `<<<SLICE `
    or `<<<END ` — no marker line leaked. The count is of marker LINES and not of
    the substring `<<<`, because prose in these files legitimately quotes the
    marker syntax when describing this very gate, and a whole-file substring count
    is unmeetable by construction (§3 pre-emission items 2 and 6). Report the
    marker-line count.
G9  `.agent/handoff.md`: the file as committed by C6 is a byte-exact PREFIX of the
    file at HEAD, and the appended remainder is exactly the VERDICT slice, byte
    for byte. Report the prefix check as True or False and the slice's sha256.
    Report the file's final line count, that NO LINE of it begins `<<<SLICE ` or
    `<<<END `, and that the seven mandated section headings of
    docs/agents/handback_template.md are present.
G10 CARRY STILL INTACT — the R2 repair must not regress. The carried set is the ids
    present BOTH in the HEAD ledger and in the blob at `76661dc1`. In that blob,
    "unresolved" means carrying no `^Done: R-\d+ — ` line anywhere in the file; the
    reviewer measured 184 finding paragraphs there and 32 such resolutions, leaving
    152, and verified that this equals the carried set. For every carried id, its
    paragraph at HEAD is byte-equal to its paragraph in the `76661dc1` blob. Report
    compared and equal; they must agree at 152. NEGATIVE CONTROL, read-only, no
    checkout: the SAME comparison against the blob at `25f7a5af` MUST report
    strictly fewer equal than compared — the reviewer measured 113 of 152. Fix the
    carried set ONCE from `76661dc1` ∩ HEAD and compare that SAME id set against
    both blobs; re-deriving the set separately per blob answers a different question
    and will not reproduce these numbers. If both halves agree the check cannot
    fail; report that and hand back.
G11 `git diff --name-only b769ccd7..HEAD` lists exactly `.agent/authored/f086-r8.md`,
    `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md` and
    `.agent/plan.md`. Report the real list and flag any difference rather than
    editing to match. `pyproject.toml` and every path under `packages/`, `apps/`,
    `tests/`, `docs/` and `scripts/` must be ABSENT; all five of those directories
    exist at `b769ccd7`, so the clause forbids something real.
G12 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. RUN IN THE PRIMARY CHECKOUT, not a worktree: the reviewer measured
    `160 passed`, exit 0, at `b769ccd7`, and the same command in a fresh worktree is
    red on `TestVitestFrontendTestFoundation::test_vitest_passes`, which spawns
    `npx vitest run` and cannot resolve `apps/ui/node_modules`, absent from every
    fresh worktree because it is gitignored. That red is the known R-0480
    mechanism, not a base red.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary. The
    reviewer measured `42 passed` at `b769ccd7`. `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` are NOT gated this round: no path
    under `docs/` changes.
G14 Per-commit insertions — the `+` column of `git show --numstat` — for C0a, C0b,
    C1, C2, C3, C4, C5 and C6. None may exceed 500 unless it is the verbatim
    rewrite of a SINGLE `.agent/**` state file, exempt under AGENTS.md DECISION
    F104 D1; if you invoke that exemption, name it and the file. C7's own count
    cannot exist while C6's text is being written, so report it in your FINAL
    MESSAGE.
G15 `git log --format=%p b769ccd7..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` and `checkout:` entries — no
    amend, rebase, reset or force-push.
G16 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` is run
    READ-ONLY at the handback and its raw output recorded, to prove this round
    opened no pull request. The reviewer measured `[]` before ordering this block;
    report what you actually see and merge nothing whatever it says.

The two pytest gates run SERIALLY, never two at once: concurrent pytest processes
here produce false reds through port-bound supervisors (R-0518 class).

Handback:
Completion report + the handoff written by C6 and completed by C7. Push with
`git push origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN8>>>
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
R8, this round: repair the ledger separation R7's G5 caught — four findings landed
as one paragraph block, so three of them were invisible to the extractor that
carries the open set forward — then record the R7 verdict and close the session.
T001 part (a) is landed and proved: the wheel now carries `apps/ui/dist`.

## Next Steps
1. R9 — T001 part (b), the packaging-time guard that refuses to produce a wheel
   whose `apps/ui/dist/index.html` is absent, plus the two-mode resolver TEST that
   DECISION F086 D3 keeps after withdrawing the two-mode resolver CODE. The guard
   is owed because the carry alone is silent: measured at 72e07381, a build with
   the carry applied and no `dist/` present exits 0 and produces a 414-member
   wheel carrying 0 UI files.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops every
  VCS exclusion when the build root is itself gitignore-matched, so any future
  packaging probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, measured against the
  same files at the base.
<<<END PLAN8>>>

<<<SLICE FINDINGS2>>>

- R-0578 — High — An authored slice that appends several findings without blank lines between them makes all but the first invisible to the extractor that carries the open set forward. R7's FINDINGS slice laid R-0574, R-0575, R-0576 and R-0577 out as four CONSECUTIVE lines. The ledger's own paragraph rule — split on runs of blank lines, then take any block whose FIRST line matches `^- R-\d+ — ` — therefore reads those four lines as ONE paragraph keyed to R-0574, and R7's G5 went red reading 157 registered where it required 160. Measured at `b769ccd7`: the paragraph extraction yields 157 registered and the line-anchored one yields 160, the block keyed R-0574 spans four lines and itself contains all four ids, and the three finding lines not preceded by a blank line are exactly R-0575, R-0576 and R-0577 — while all 156 findings present at `72e07381` are blank-line separated. Nothing was lost in BYTES; what was lost is machine visibility, and the tool that would have dropped them is the one that carries the open set into the next feature. That is the R-0572 damage shape arriving through layout rather than through truncation, one round after this same reviewer wrote the paragraph rule down to prevent it. The counter-measure is structural and belongs in the block, not in a habit: an authored slice that carries more than one finding separates them with a blank line, and the round that appends it gates BOTH extractions and requires them to AGREE — a single reading can be self-consistently wrong, and two that must match cannot.

- R-0579 — Low — A gate whose command cannot run on the host is red at the base and therefore proves nothing. R7's G8 ordered `python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"` as a validity check on the edited file, and this host's `python3` is 3.10.12 while `tomllib` entered the standard library in 3.11, so the command exits 1 with `ModuleNotFoundError: No module named 'tomllib'` against the edited file and equally against the base blob. The worker reported both readings and substituted a `tomli` parse as an ADDITIONAL reading rather than swapping the gate, which is the correct handling. No harm reached the artifact — the file is valid TOML, and both wheel builds in the same round parsed it and exited 0, which is the stronger evidence anyway. This is R-0364 once more, narrowed to the interpreter's own version: a gate is executed at its base before it is ordered, and "the standard library has this module" is exactly the kind of assumption that never announces itself.
<<<END FINDINGS2>>>

<<<SLICE RESOLUTION>>>

Done: R-0578 — Resolved at R8 C3. The three finding lines that followed their predecessor with no blank line — R-0575, R-0576 and R-0577 — each gained exactly one blank line before it, and nothing else in `.agent/live_review.md` changed: the multiset of `^- R-\d+ — ` lines is identical across that commit, the file with all blank lines removed is byte-identical across it, and the byte length grew by exactly 3. The property that matters is not the edit but its result — the paragraph extraction and the line-anchored extraction now return the SAME registered set, where at `b769ccd7` they returned 157 and 160. R8's G5 requires that agreement at HEAD and records the disagreement at `b769ccd7` as its control, so the check can fail; R8's G6 requires the four separation properties above. R-0579 is NOT resolved here: it is a defect in a gate's command rather than in an artifact, there is nothing on disk to repair, and the durable fix is the reviewer executing every gate at its base — which is R-0364, already open.
<<<END RESOLUTION>>>

<<<SLICE RECORD6>>>

Gate: R8 — the R7 entry. R7 FAILED on G5, and every other gate its block ordered was re-taken by the reviewer over `72e07381..b769ccd7` rather than read from the handback. WHAT FAILED: the FINDINGS slice appended R-0574 through R-0577 as four consecutive lines, so the ledger's paragraph extraction read 157 registered at `b769ccd7` against the required 160, and R-0575, R-0576 and R-0577 are invisible to it while remaining fully present in bytes — the reviewer confirmed all three readings independently, including that the block keyed R-0574 spans four lines and contains all four ids. The defect is the REVIEWER's slice layout, not the worker's application: the worker applied the slice byte-verbatim as ordered, reported both readings, refused to insert separators because doing so would have made the ledger diverge from the authored bytes, and named the interaction correctly. It is registered as R-0578 and repaired by this round's C3. WHAT PASSED, all re-executed: the transport held in the PRIMARY cmp-against-scratchpad form at sha256 3af052ece31a358e6caf5c21660d7e13d56c4cdfc20b15be95de7e4f048fbce0, 32245 B, 387 lines, with `.agent/authored/f086-r7.md` and `.agent/last_block.md` AS COMMITTED AT `b769ccd7` both equal to the reviewer's scratch original; `.agent/plan.md` at `b769ccd7` is byte-equal to its PLAN7 slice at 43 lines; the three ledger appends and the `.agent/decisions.md` append are all true byte-exact prefix-plus-remainder appends whose remainders equal FINDINGS, RECORD5 and DECISION3, with `## DECISION F086 D3` occurring exactly once so no landed DECISION was edited; the carried set of 152 is still byte-equal at `b769ccd7` to the `76661dc1` blob, against a negative control of 113 of 152; 0 marker lines leaked into `.agent/live_review.md` or `.agent/decisions.md` at `b769ccd7`; the suites returned `160 passed` and `42 passed` serially in the primary checkout at `b769ccd7`, each exit 0; seven paths over eight single-parent commits inserting 387, 261, 11, 5, 2, 54, 6 and 65 lines, none over 500 and no exemption needed. THE ROUND'S DELIVERABLE LANDED AND IS PROVED: `pyproject.toml` at `b769ccd7` carries `artifacts = ["apps/ui/dist/**"]`, PYFROM occurs once at the base and PYTO once at HEAD with all six TO-only lines appearing exactly once among that commit's six added lines, and a wheel built from an out-of-repo worktree at the C5 commit holds 417 members, 2155470 bytes and 3 under `apps/ui/dist/` including `index.html`, against a control at `72e07381` from the same preparation holding 414 members and 0 — a control that CAN fail, which is precisely what R6's could not. Those three subject numbers equal the reviewer's own independent measurement of the same configuration, taken before the block was written. THE SECOND RED WAS THE REVIEWER'S TOO: G8's `tomllib` sub-clause cannot run on this host's Python 3.10.12 and is red at the base as well, registered as R-0579. What the reviewer did NOT observe, and accepts on the worker's report because it is unobservable once a round has ended, is the absence of `.agent/STOP` at the points the block names, the serial ordering of the two pytest runs, and the removal of the two out-of-repo probe worktrees, whose end state — one worktree line and an empty `git status --porcelain` — the reviewer did confirm.
<<<END RECORD6>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

This section exists because finding R-0571, registered by this feature, is that a
verdict issued and never written to disk cannot be told apart from one never
issued. It is appended rather than written into the sections above so that the
next handback rewrite cannot silently destroy it.

Session of 2026-08-20, self-drive per docs/agents/self_drive_protocol.md, and the
SECOND session on this branch. The reviewer wrote nothing in the work tree; one
delegated worker per round made every commit; every verdict below rests on gates
the reviewer re-executed itself over the committed diff, never on a handback's
summary.

| Round | Range | Verdict |
|---|---|---|
| R5 | 655661b0..91459dc1 | PASS |
| R6 | 91459dc1..72e07381 | PASS |
| R7 | 72e07381..b769ccd7 | FAIL — R-0578 |

R5 was inherited unreviewed from the previous session, which ended immediately
after issuing its own verdict; reviewing it first was Phase 1 rule 4 and it
passed on every gate. R6 was ordered to choose the wheel carry mechanism by
measurement and could not: its red control was sited under `.remedy-wt/`, and
hatchling drops every VCS exclusion when the build root is itself gitignore-matched,
so the control read 3 where 0 was required. The worker obeyed the block's own halt
clause, left `pyproject.toml` untouched, found the cause in hatchling's source and
proved it — the right outcome from a broken order, and the defect is registered as
R-0574 against the reviewer. R7 then landed the carry for real, with the probe tree
moved OUTSIDE the repository: `artifacts = ["apps/ui/dist/**"]` is in
`pyproject.toml` at `b769ccd7`, a wheel built at that commit carries
`apps/ui/dist/index.html` and both asset bundles, and the control that must read 0
does read 0. R7 failed only on the layout of the reviewer's own findings slice,
which R8 repaired.

Every finding this session registered — R-0574 through R-0579 — is a defect in
the reviewer's own gates rather than in any worker's execution. That is the honest
summary of the session: the workers were not the weak link, and every round that
went wrong went wrong in the order, not in the obedience.

DECISION F086 D3 was ruled and is the session's other durable output. It withdraws
D1 part (c) — the dual-mode asset resolver — because the premise was false, and
measured false from an extracted wheel, from an independent wheel-root-shaped copy
and from the checkout: `_get_frontend_dist()`'s three `.parent` hops
land on the wheel ROOT, where `apps/` is a sibling of `packages/` exactly as in a
checkout, so the single existing expression already resolves in both modes. The
test per mode is KEPT. D1 part (b), the packaging-time guard, is still owed and no
release may be cut before it exists: with the carry applied and no `dist/` present
a build still exits 0 and ships a wheel with zero UI files.

The open set stands at 160 once this round's own C2 and C4 have landed, which is
what G5 requires and measures at HEAD, and the next free id is R-0580. By
docs/agents/planner_reviewer_prompt.md §4 item 13 the LAST round of a branch has no
on-disk gate entry, so R8's own verdict is the terminator and lives in the
reviewer's closing report rather than here. That absence is the rule, not an
omission — and it is precisely the hole R-0571 exists to close.
<<<END VERDICT>>>
