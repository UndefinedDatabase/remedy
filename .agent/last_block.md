── STEP R5 — F086 Release capability (record + session close) ────

Goal:
Record the R4 verdict in the review ledger, then close this session cleanly: the
worker writes its handback, and the reviewer's own session verdict is APPENDED to
that file so it survives on disk instead of dying with the session. This is the
LAST round of the session. No code, no test, no PR.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f086-r5.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` := the PLAN5 slice, whole file
  C2  append the RECORD3 slice to `.agent/live_review.md`
  C3  rewrite `.agent/handoff.md` per docs/agents/handback_template.md
  C4  append the VERDICT slice to `.agent/handoff.md`

C1 precedes C2 because §3 pre-emission item 23 requires the plan to advance
before any commit touching the finding ledger, and RECORD3 touches it.

Why C4 exists and why it APPENDS. Finding R-0571, registered by this very
feature, is that a verdict issued and never written to disk is indistinguishable
from one never issued: a branch's last round has no on-disk gate entry by
construction (docs/agents/planner_reviewer_prompt.md §4 item 13). The
counter-measure is the record round — the reviewer authors its verdict as a named
slice and the worker applies it, exactly as every other authored text is applied.
It APPENDS rather than rewrites because a rewrite of `.agent/handoff.md` is what
destroys a verdict already written into it.

Base:
This round starts from `655661b0`, the tip of `feature/f086-release-capability`
and the R4 handback commit. Every range gate below names that SHA. Stay on the
existing branch — do NOT create one, do NOT run the Open PR Gate, do NOT open a
PR. The branch stays pushed and unmerged; its PR is created at closure, which is
a later session's work.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN5, RECORD3 and VERDICT. PLAN5 is the COMPLETE file including
its single trailing newline. RECORD3 and VERDICT are EOF-APPENDS, defined as pure
concatenation with each slice's own leading blank line INSIDE the slice, so
nothing is prepended and nothing is stripped. No FROM/TO pair exists in this
block.

──────────────────────────────────────────────────────────────

Change:

0. Confirm `git rev-parse HEAD` equals `655661b0`, `git branch --show-current` is
   `feature/f086-release-capability`, `git status --porcelain` is EMPTY and
   `.agent/STOP` is absent. If any differs, stop and hand off.

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f086-r5.md`. The reviewer's original is on disk at
   `.remedy-wt/f086-r5.md`; copy that file rather than retyping it
   (`shutil.copyfile` is fine; the gate names the byte property, not the tool).
   Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f086-r5.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` := the PLAN5 slice, byte-verbatim, whole file. Commit
   alone.

4. C2 — append the RECORD3 slice to `.agent/live_review.md` under the append
   convention. Commit alone. The paragraph begins `Gate:` and registers no
   finding id, so the ledger sets are unchanged by this commit; G4 requires it.

5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md, with
   every mandated section in the template's order: Range, Commits, External
   actions, Verification, Authored-text proofs, Deviations & assumptions, Next.
   Range is `Review of 655661b0..<HEAD>`.
   BEFORE writing it, measure the VERDICT slice's own line count from the
   COMMITTED `.agent/authored/f086-r5.md`, because C4 appends exactly those lines
   to this file. Your `Deviations & assumptions` section states the FINAL line
   count of `.agent/handoff.md` as it will stand after C4 — your own lines plus
   the slice's — and, if that total exceeds the cap, declares the overage under
   AGENTS.md DECISION D15 naming its cause: this round carries the reviewer's
   authored session verdict, which is mandated content for the round that closes
   a session, and no section is dropped to meet the cap. Do NOT trim after C4;
   a trim commit against the cap is the smell the template names.
   The `Next` section names, in this order, the next session's first two actions:
   re-read `.agent/STOP` from disk (Phase 1 rule 1), then run the Open PR Gate
   (Phase 1 rule 2).

6. C4 — append the VERDICT slice to `.agent/handoff.md` under the append
   convention. Commit alone. Nothing else in that file changes: the file as
   written by C3 must be a byte-exact PREFIX of the file at HEAD, and G7
   measures exactly that.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If one cannot be applied as-is, stop
   and declare it — never adjust the bytes to make a gate pass.
3. This round writes NO code and NO test. No path under `packages/`, `apps/`,
   `tests/`, `docs/` or `scripts/`, and not `pyproject.toml`, is touched. G10
   measures the change set exactly.
4. Never force-push, never rebase, never amend, never work on `main`, never
   delete a branch, and do not create one. Do NOT create a pull request: this
   feature is mid-flight and its PR belongs to its closure round.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
6. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, exit code and output, and hand back.
7. The VERDICT slice is the reviewer's text. Do not summarise it, do not
   reformat it, and do not write a verdict of your own anywhere: a
   worker-authored verdict is a finding however honestly it is hedged
   (docs/agents/planner_reviewer_prompt.md §4 item 4).

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent. Branch still
    `feature/f086-release-capability`.
G2  TRANSPORT: `.remedy-wt/f086-r5.md`, the committed `.agent/authored/f086-r5.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN5 slice extracted from the
    COMMITTED `.agent/authored/f086-r5.md`, contains `## Goal`, `## Next Steps`
    and a match of `\bF\d{3}\b`, and is under 50 lines. Report sha256 and lines.
G4  LEDGER UNCHANGED BY THIS ROUND. Using a PARAGRAPH extraction — split on runs
    of blank lines into blocks; a finding paragraph is any block whose FIRST
    line matches `^- R-\d+ — `, the whole block and never its first line —
    report at HEAD and at `655661b0`: registered, resolved, `Landed:`, duplicate
    ids, resolutions naming an unregistered id, and the OPEN set. REQUIRED as
    set comparisons, reporting both sides: the registered, resolved and OPEN
    sets are IDENTICAL at the two SHAs. The reviewer measured 156 registered, 1
    resolved and 155 open at `655661b0`.
G5  CARRY STILL INTACT — the R2 repair must not regress. The carried set is the
    ids present BOTH in the HEAD ledger and in the blob at `76661dc1`; the
    reviewer measured that set as 152 and verified it equals the set of ids
    registered-and-unresolved in that blob. For every such id, its paragraph at
    HEAD is byte-equal to its paragraph in the `76661dc1` blob. Report compared
    and equal; they must agree at 152. NEGATIVE CONTROL, read-only, no checkout:
    the SAME comparison against the blob at `25f7a5af` MUST report strictly
    fewer equal than compared — the reviewer measured 113 of 152. If both halves
    agree the check cannot fail; report that and hand back.
G6  The RECORD3 paragraph is present verbatim at HEAD, begins `Gate:`, and does
    NOT match `^- R-\d+ — `. `.agent/live_review.md` contains `Steps`, and NO
    LINE of it begins `<<<SLICE ` or `<<<END ` — that is, no marker line leaked.
    The count is of marker LINES and not of the substring `<<<`, because prose
    in these files legitimately quotes the marker syntax when describing this
    very gate, and a whole-file substring count is therefore unmeetable by
    construction (§3 pre-emission items 2 and 6). Report the marker-line count.
G7  `.agent/handoff.md`: the file as committed by C3 is a byte-exact PREFIX of
    the file at HEAD, and the appended remainder is exactly the VERDICT slice,
    byte for byte. Report the prefix check as True or False and the slice's
    sha256. Report the file's final line count, and that NO LINE of it begins
    `<<<SLICE ` or `<<<END `. The reviewer measured that the file at `655661b0`
    already holds the substring `<<<` three times, all inline in prose quoting
    this very gate's wording, so a whole-file substring count is unmeetable here
    and the marker-LINE count is the property that means anything.
    Report also that the seven mandated section headings of
    docs/agents/handback_template.md are present.
G8  `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
    → exit 0. RUN IN THE PRIMARY CHECKOUT, not a worktree: the reviewer measured
    `160 passed`, exit 0, at `655661b0`, and the same command in a fresh
    worktree is red on `TestVitestFrontendTestFoundation::test_vitest_passes`,
    which spawns `npx vitest run` and cannot resolve `apps/ui/node_modules`,
    absent from every fresh worktree because it is gitignored. That red is the
    known R-0480 mechanism, not a base red.
G9  `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at `655661b0`. `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` are NOT gated this round: no
    path under `docs/` changes.
G10 `git diff --name-only 655661b0..HEAD` lists exactly:
    `.agent/authored/f086-r5.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`. Report the real list and flag any
    difference rather than editing to match. `pyproject.toml` and every path
    under `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` must be ABSENT.
G11 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2 and C3. None may exceed 500 unless it is the verbatim rewrite of
    a SINGLE `.agent/**` state file, exempt under AGENTS.md DECISION F104 D1; if
    you invoke that exemption, name it and the file. C4's own count cannot exist
    while C3's text is being written, so report it in your FINAL MESSAGE.
G12 `git log --format=%p 655661b0..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` and `checkout:` entries —
    no amend, rebase, reset or force-push.
G13 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` is
    run READ-ONLY at the handback and its raw output recorded, to prove this
    round opened no pull request. The reviewer measured `[]` before ordering
    this block; report what you actually see and merge nothing whatever it says.

The two pytest gates run SERIALLY, never two at once: concurrent pytest
processes here produce false reds through port-bound supervisors (R-0518 class).

Handback:
Completion report + the handoff written by C3 and completed by C4. Push with
`git push origin feature/f086-release-capability`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN5>>>
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
R5, this round: record the R4 verdict and close the session. The claim, the
repair of the R1 carry, the measured packaging inventory and the two packaging
DECISIONs are all landed and gated. No code has been written yet — T001 has not
started.

## Next Steps
1. R6 — T001 begins, ruled by DECISION F086 D1 in `.agent/decisions.md`: the
   explicit wheel carry for `apps/ui/dist`, chosen by MEASUREMENT of what the
   installed hatchling honours; the packaging-time guard that refuses a wheel
   whose `apps/ui/dist/index.html` is absent; the dual-mode resolver in
   `_get_frontend_dist()` with a test per mode; and the installed-mode path that
   never spawns npm. The measured baseline it must move is a wheel of 414
   members and 2038283 bytes carrying 0 members under `apps/ui/dist/`.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the
  wheel's console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- Building a releasable wheel will require the UI to be built first, by DECISION
  F086 D1's own consequence. CI and any human cutting a release inherit that
  constraint, and a round that adds the npm build step routes it through the
  F085 `exec_guard` seam rather than a bare subprocess.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, measured against
  the same files at the base.
<<<END PLAN5>>>

<<<SLICE RECORD3>>>

Gate: R5 — the R4 entry. R4 PASSED. Every gate its block ordered was re-taken by the reviewer over `0cabd17e..655661b0` rather than read from the handback. THE TRANSPORT HELD in the PRIMARY cmp-against-scratchpad form: the reviewer's scratch original, the committed `.agent/authored/f086-r4.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 84485aac89d300e388c7a432af78dca51f6da510784d67de60a653cbcdf53b20, 21879 B, 302 lines, and `.agent/plan.md` is byte-equal to its PLAN4 slice at 43 lines. THE LEDGER WAS UNCHANGED, which is what a record round owes: registered, resolved and OPEN are IDENTICAL sets at `0cabd17e` and `655661b0` — 156 registered, 1 resolved, 155 open, 0 duplicate ids, 0 resolutions naming an unregistered id, 0 `Landed:` lines — because the appended paragraph begins `Gate:` and matches no finding pattern. THE APPEND WAS AN APPEND: `.agent/decisions.md` at `0cabd17e` is a byte-exact PREFIX of the file at `655661b0`, and the remainder is exactly DECISION1 then DECISION2, at sha256 998c729d1e488ad15e614b91a5e479b1380781d8af9a1258c8cbf3da58657dfd (3251 B) and ead658cf7756e29c89ede8f2a72eb47005b40ab1f2c424cbfc842b09f26e9d4a (2059 B), each heading occurring exactly once, so no landed DECISION was edited. THE R2 REPAIR HAS NOT REGRESSED and its check still cannot pass vacuously: all 152 carried paragraphs at `655661b0` are byte-equal to their originals in the blob at `76661dc1`, while the same comparison against `25f7a5af` reports 113 of 152. THE TWO CARRY-SET DEFINITIONS WERE PROVED TO COINCIDE rather than assumed to: the worker declared that it first read the carried set as all 184 finding paragraphs of the pre-reset blob and corrected it to the ids present in BOTH the HEAD ledger and that blob, and the reviewer verified that this set and the reviewer's own — registered-and-unresolved in the pre-reset blob — are the SAME 152 ids, so the two routes to 152/152 and 113/152 agree by construction and not by luck. THE SUITES WERE RE-RUN, NOT READ, serially in the primary checkout at `655661b0`: `160 passed` for the four state readers and `42 passed` for the canary, each exit 0. THE HYGIENE HELD: six paths, all under `.agent/`, over six single-parent commits inserting 302, 193, 23, 2, 78 and 44 lines, none over 500 and no exemption needed; `pyproject.toml`, `packages/orchestration/ui_server.py` and every path under `apps/`, `tests/` and `docs/` are absent from the range, which is what a round that RULES a code change without making one must show. The handback measured 100 lines against its 100-line cap with no overage declaration needed, written once with no trim commit. THE ROUND DECLARED NO DEPARTURE from its ordered commit sequence and the reviewer found none. What the reviewer did NOT observe, and accepts on the worker's report because it is unobservable once a round has ended, is the absence of `.agent/STOP` at the points the block names and the serial ordering of the two pytest runs.
<<<END RECORD3>>>

<<<SLICE VERDICT>>>

## Reviewer's session verdict — authored by the reviewer, applied by the worker

This section exists because finding R-0571, registered by this feature, is that a
verdict issued and never written to disk cannot be told apart from one never
issued. It is appended rather than written into the sections above so that the
next handback rewrite cannot silently destroy it.

Session of 2026-08-20, self-drive per docs/agents/self_drive_protocol.md. The
reviewer wrote nothing in the work tree; one delegated worker made every commit of
every round; every verdict below rests on gates the reviewer re-executed itself
over the committed diff, never on a handback's summary.

| Round | Range | Verdict |
|---|---|---|
| R1 | 76661dc1..25f7a5af | FAIL — R-0572, R-0573 |
| R2 | 25f7a5af..9e855296 | PASS |
| R3 | 9e855296..0cabd17e | PASS |
| R4 | 0cabd17e..655661b0 | PASS |

R1 claimed F086, reset the review record carrying the F085 open set forward and
registered the two closure candidates as R-0570 and R-0571, emptying
`.agent/candidates.md`. It FAILED on the carry: 39 multi-line finding paragraphs
were truncated to their headlines, 52917 characters of the permanent record lost.
The cause was the reviewer's own block wording — "a finding paragraph is a line
matching `^- R-\d+ — `" defines the paragraph as the line — and the worker applied
it literally and reported honestly. No gate caught it because R1's own transport
gate compared both sides with that same broken extractor; R-0572 carries the loss
and R-0573 the gate defect. R2 restored all 39 paragraphs verbatim from the
pre-reset blob and resolved R-0572, under a check whose negative control is
required to reject the corrupt state. R3 measured the packaging shape by building
a real wheel and established that a wheel built from a pristine checkout carries
ZERO members under `apps/ui/dist/` — Remedy currently packages a CLI whose UI
cannot serve. R4 ruled DECISION F086 D1 and D2 on that measurement.

The open set stands at 155, next free id R-0574. R-0573 remains OPEN: its durable
fix promotes a rule into the pre-emission checklist at
docs/agents/planner_reviewer_prompt.md §3, a file F086 does not own, so it routes
to a paydown branch with R-0403, R-0448, R-0482, R-0487 and R-0490.

By docs/agents/planner_reviewer_prompt.md §4 item 13 the LAST round of a branch
has no on-disk gate entry, so R5's own verdict is the terminator and lives in the
reviewer's closing report rather than here. That absence is the rule, not an
omission — and it is precisely the hole R-0571 exists to close.
<<<END VERDICT>>>
