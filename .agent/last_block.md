STEP T002 preparation — F037 R8

Goal: correct the design authority the remaining UI rounds will build against,
book the R7 verdict, resolve `R-0715`, register `R-0719`, and establish by
MEASUREMENT whether the frontend test runner can run here at all.

Base: `996ffea9`. Branch: `feature/f037-rendered-diff-viewer`. SESSION 2 of
feature F037, round 8, rounds so far 7.

Bundle, one commit each, in this order:
C0a  save this block verbatim to `.agent/authored/f037-r8.md`
C0b  mirror the C0a blob into `.agent/last_block.md`
C1   `.agent/plan.md` from slice PLANF037R8
C2   `.agent/live_review.md` from pair DONE715PAIR, then append GATER7, then
     append R0719; `.agent/prose_slips.md` append SLIPR8
C3   `docs/roadmap/features/T5_F037.md` append AMEND4;
     `.agent/decisions.md` append DECISION3
C4   `.agent/handoff.md`, the handback

Change set — these paths and no others:
  .agent/authored/f037-r8.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/decisions.md
  docs/roadmap/features/T5_F037.md
  .agent/handoff.md
Run `git push origin feature/f037-rendered-diff-viewer` AFTER C4. Create no pull
request and merge nothing: the Open PR Gate returned `[]` when this block was
authored.

Slice convention: the authored texts in this block are PLANF037R8, DONE715PAIR,
GATER7, R0719, SLIPR8, AMEND4 and DECISION3. Each is delimited by a line
`<<<SLICE <NAME>` and a line `<<<END <NAME>`; the marker lines are never part of
the text. A pair slice carries a `<<<FROM` line and a `<<<TO` line inside it,
which are likewise never part of either text.

Constraints:
1. Apply every slice byte for byte, extracted from the COMMITTED C0a blob by its
   marker LINES in Python. Never retype a slice, never edit a slice.
2. `.agent/plan.md` is a WHOLE-FILE replacement by PLANF037R8.
3. DONE715PAIR is a FROM/TO pair against `.agent/live_review.md`. The
   containment test was run before emission: `TO contains FROM: false`. It is a
   REWRITE, so it orders its FROM at 0x and its TO at 1x in the file after C2,
   and it orders no append reading. The FROM was measured at exactly ONE
   occurrence at the base; report the count you measure before the edit.
4. GATER7 and R0719 are appends at EOF of `.agent/live_review.md`, applied in
   that order and AFTER the pair, in the same commit. SLIPR8 appends at EOF of
   `.agent/prose_slips.md`. AMEND4 appends at EOF of
   `docs/roadmap/features/T5_F037.md`. DECISION3 appends at EOF of
   `.agent/decisions.md`. Every append uses the file's existing convention: a
   single separator newline, then the slice bytes.
5. `R-0719` is the only id minted this round, and it is the next free one: the
   maximum registered id at the base is `R-0718`, measured.
6. Do NOT touch the `Landed: R-0711` line or any existing `Done:` paragraph.
7. NO TypeScript, TSX, CSS or any file under `apps/` is written this round. The
   reason is gate G7 and it is deliberate: the reviewer's three attempts to run
   the frontend test runner were all refused by this environment, and no code
   will be ordered that neither the worker nor the reviewer can execute. G7
   settles that question; the next round acts on the answer.
8. Do NOT touch `packages/`, `tests/`, `docs/roadmap/ROADMAP.md` or
   `docs/roadmap/STATUS.md`.

SPEC — there is no production code in this round. The work is the four authored
appends, the one pair and the probe.

Done when — eight gates. Run every one, record its REAL exit code and its
verbatim summary line, and put one line per gate in the handback.

G1 hygiene. Read `.agent/STOP` from disk before C0a and again before C4; report
   ABSENT or PRESENT at both points, and if PRESENT stop after the current
   commit and hand off. Report `git rev-parse HEAD` before C0a — it must equal
   the base above — and `git branch --show-current`. Report the
   `git status --porcelain` LINE COUNT after each of C0a, C0b, C1, C2 and C3;
   each must be 0.

G2 transport, ONE digest comparison. After C0a report the sha256, byte count and
   line count of `.agent/authored/f037-r8.md`. After C0b report that
   `git rev-parse HEAD:.agent/authored/f037-r8.md` and
   `git rev-parse HEAD:.agent/last_block.md` are the SAME blob hash. State
   plainly that this chain covers the saved copy, its mirror and the working
   copy, and claims nothing about the bytes of any prompt.

G3 extraction and caps. Extract every slice from the COMMITTED C0a blob by its
   marker lines and print each slice's NAME and line count. Print TOTAL, CONTENT
   (the sum of the slice line counts) and PROSE = TOTAL − CONTENT, all as
   measured. PROSE must be at most 400 and TOTAL at most 490.

G4 the plan at C1. `.agent/plan.md` byte-equal to PLANF037R8 under the
   newline-included convention: report True or False. Report the NEGATIVE
   CONTROL against the slice minus its trailing newline; it must be False.
   Report `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` strictly under 50.

G5 the record at C2, full byte forensics — this is the append into the record.
   PAIR: report the FROM count before and after (1 then 0) and the TO count
   before and after (0 then 1).
   APPENDS: the base `.agent/live_review.md` is 1166346 bytes and
   `.agent/prose_slips.md` is 8424 bytes; report the measured values beside
   them. For EACH of the three appends — GATER7, R0719, SLIPR8 — report reader
   (a) as the BYTE IDENTITY `result == before + b"\n" + slice`, stating that
   identity explicitly rather than a length sum with a prefix check, because
   those two properties together cannot reject a byte flipped inside the
   appended region and this gate's own control requires exactly that rejection.
   Report reader (b) independently and structurally: have your script COUNT N,
   the number of blank-line units in the slice, and compare the LAST N units of
   the file against the slice's N units IN ORDER. NEGATIVE CONTROL per append:
   flip one byte inside the FIRST appended paragraph and report that reader (a)
   and reader (b) BOTH come back False.
   COUNTS after C2, line-anchored, each reported as measured:
     `^- R-\d+ — ` 280 — `R-0719` is the one id minted
     `^Done: R-\d+ — ` 28 — `R-0715` resolved
     `^Landed: R-` 1 — only the `R-0711` line survives
     `^Gate: F\d+ R\d+ — ` 78
   Report the ids ADDED (exactly `R-0719`), the ids newly RESOLVED (exactly
   `R-0715`), whether all ids are DISTINCT, the maximum id, and the size of the
   open set.

G6 the two docs appends at C3. For EACH of AMEND4 into
   `docs/roadmap/features/T5_F037.md` (base 7981 bytes) and DECISION3 into
   `.agent/decisions.md` (base 655420 bytes), report the measured base size
   beside the figure above and reader (a) as the same BYTE IDENTITY G5 defines,
   plus reader (b) over the last N blank-line units with N counted by your
   script. Report the line-anchored count of `^## DECISION ` in
   `.agent/decisions.md` before and after C3: 168 then 169, and report that
   `F037 D3` occurs exactly once in that file after C3. Report the
   line-anchored counts of `^<<<SLICE ` and `^<<<END ` in both files after C3;
   both must be 0 in both files.

G7 THE PROBE — can the frontend test runner run here at all? This gate produces
   an ANSWER, not a colour, and either answer is a pass for this round.
   Attempt each of the following THREE commands, in this order, from the
   repository root, and report for each one: the exact command, whether it RAN
   or was REFUSED by the environment, and either its real exit code with its
   summary line, or the refusal message verbatim.
     1. `npx vitest run --root apps/ui`
     2. `npm --prefix apps/ui run test:unit`
     3. `apps/ui/node_modules/.bin/vitest run --root apps/ui`
   If ANY of them RUNS, report the full result — the suite is expected green at
   the base since this round writes no frontend code, so report the real number
   of passing tests and treat a red as a finding to declare, not to fix.
   If ALL THREE are REFUSED, say so plainly and state that no vitest result
   exists for this round. Do NOT claim, estimate or infer a test outcome you did
   not observe, do NOT attempt any other route to the runner, and do NOT install
   or modify anything to make it run. A refusal is a measurement and it is the
   single most useful thing this round can produce.
   ALSO in this gate, and these two DO run: the docs gate
   `python3 -m pytest tests/docs/ -q`, required because this round's change set
   includes `docs/roadmap/**`, measured GREEN at the base at `295 passed`; and
   the canary `python3 -m pytest tests/cli/test_golden_path.py -q`, measured
   GREEN at the base at `42 passed`. Report the real exit code and verbatim
   summary of each, and if either differs from the base figure report the
   difference rather than explaining it away.

G8 structure, artifacts and the Open PR Gate, measured at C3.
   Report `git diff --name-only <base>..<C3>` against the change set above minus
   `.agent/handoff.md`, and report BOTH residues — actual minus expected and
   expected minus actual — each of which must be empty.
   Report a restricted `git diff --stat` showing that `apps/`, `packages/` and
   `tests/` are ALL EMPTY for this round, and that `docs/` holds only
   `docs/roadmap/features/T5_F037.md`.
   Report the per-commit INSERTION count from `git diff --numstat` for C0a, C0b,
   C1, C2 and C3 — not for C4, whose own count cannot exist while its text is
   being written — and confirm each commit is single-parent and each insertion
   count is under 500.
   Run the `^<<<SLICE ` / `^<<<END ` counter over the C0a blob and report the
   number it measures, which must be greater than zero, so the sweeps in G5 and
   G6 are shown not to be blind.
   Report `git ls-files .remedy-wt` line count, which must be 0, and
   `git worktree list` line count, which must be 1 — this round opens no
   worktree, because it runs no destructive verification.
   Report the Open PR Gate verbatim:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
   The PUSH is ordered after C4 and is deliberately NOT part of any gate: C4
   writes the handback, so the handback cannot report a value that does not
   exist when it is written. Run the push, and do not name its result in
   `.agent/handoff.md`; the reviewer reads the remote tip itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the Session block naming SESSION 2 of feature F037 and round 8, the
range and base SHA, a per-commit changed-files table with a `+/-` column taken
from `git diff --numstat` itself and agreeing cell for cell with the per-commit
reading G8 orders, the external actions, one line per gate G1 through G8 with
its real result, the item-status table covering every C-item and every gate with
`done`, `skipped` or `deviated` plus a reason, the Deviations, and the Next
section. It has NO length cap. In the Next section state the G7 answer FIRST and
in one unmissable sentence — whether the frontend test runner can be executed
here — because the next round's whole shape depends on it, then that the first
action of the next round is to re-read `.agent/STOP` from disk, then the Open PR
Gate.

<<<SLICE PLANF037R8
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1, D2 and D3.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
T001 is COMPLETE: the parser, the resolver and the two GET routes all landed and
were proved by mutation. R8 prepares T002 rather than starting it. It corrects
the feature file's design authority for the diff surface, which named a section
that does not exist, and it MEASURES whether the frontend test runner can be
executed in this environment at all — the reviewer's three attempts were
refused, and no UI code is ordered until that has an answer, because code that
neither role can execute cannot be verified and must not be certified.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R7 gate, `R-0715`, `R-0719`, the slip | ordered | record first |
| C3 the feature-file amendment and the decision | ordered | authority before builders |
| C4 the handback | ordered | carries the probe's answer first |

## Next Steps
1. Act on the G7 answer. If the runner executes, T002's rendering core lands as
   a pure `.ts` view-model beside its `.test.ts`, which is the only shape this
   package tests: `apps/ui/vitest.config.ts` sets `environment: "node"` and the
   repository has neither jsdom nor a testing library, so no React component is
   rendered in any of its 31 test files. If the runner cannot execute, the
   session hands off asking the operator to grant it, and orders no UI code.
2. T002 the rendering core, then the React components and their CSS module
   against the binding CSS and amendment A4.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- The frontend runner is unproven here. That is what G7 measures, and it is the
  single largest risk to the rest of this feature.
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- No bundle-size budget exists anywhere in `tests/` or `apps/ui/vite.config.ts`,
  so T003 would be creating that ceiling rather than satisfying one.
<<<END PLANF037R8

<<<SLICE DONE715PAIR
<<<FROM
Landed: R-0715 — the docstring of `_do_get_route_facts` in `tests/ui_server/test_command_channel.py` no longer counts the job endpoints: "The thirteen job endpoints live in a dict literal inside `do_GET`" is now "The job endpoints live in a dict literal inside `do_GET`", which is the delete-the-numeral counter-measure the finding names rather than an update to fifteen, and the clause that carries the real property — that adding one puts it in the walk for free — is unchanged. The same commit adds the task-run diff route to `_walkable_paths`, so the route this round introduces is walked by the 405 discipline. In commit C4 of F037 R7.
<<<TO
Done: R-0715 — RESOLVED at F037 R7, commit `23b9ab39`, and verified by the reviewer at `996ffea9`. The docstring of `_do_get_route_facts` in `tests/ui_server/test_command_channel.py` no longer counts the job endpoints at all: "The thirteen job endpoints live in a dict literal inside `do_GET`" is now "The job endpoints live in a dict literal inside `do_GET`". THAT IS THE COUNTER-MEASURE THE FINDING NAMED — delete the numeral rather than update it — and it is the right one for a reason this round demonstrated rather than argued: the same round added a FIFTEENTH endpoint key, so a numeral updated to fourteen at R7 would have been stale inside its own commit. The clause carrying the real property, that adding one puts it in the walk for free, is unchanged and still true. THE REPAIR IS MEASURED, NOT READ: the reviewer counted `thirteen` at 0 in that file at `996ffea9`, and the worker additionally counted `twelve`, `fourteen`, `fifteen` and `sixteen` at 0, so no substitute numeral was quietly put in its place — which is the failure mode this class of repair invites. The guard the docstring belongs to is unharmed: `tests/ui_server/test_command_channel.py` is exit 0 at `106 passed` both at the base and at `996ffea9`, measured by the reviewer in the primary checkout and again inside a disposable worktree, and the same commit registered the round's new structural route in `_walkable_paths` so the 405 discipline really walks it.
<<<END DONE715PAIR

<<<SLICE GATER7
Gate: F037 R7 — the routing round, and the round that COMPLETES T001. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran the load-bearing ones itself at `996ffea9`. THE FEATURE'S SERVER HALF IS NOW WHOLE: a job-scope route as a key in the `do_GET` handlers dict, and a task-run-scope route spelled out structurally because it needs a second path segment, both calling `build_diff_view` through thin builders that hold no filesystem logic of their own. THE SUITE AND THE GUARD ARE GREEN AT REAL EXIT CODES: `python3 -m pytest tests/ui_server/test_diff_endpoint.py tests/ui_server/test_command_channel.py tests/orchestration/test_diff_view_source.py -q` is exit 0 at `121 passed`, `python3 -m ruff check` over the three touched paths under the repository's own configuration is exit 0 at `All checks passed!`, and the canary is exit 0 at `42 passed`. ALL THREE ROUTE MUTATIONS REPRODUCE EXACTLY AS REPORTED, run by the reviewer in a disposable worktree with `__pycache__` purged before every run and the module restored between them, each mutated string counted at exactly one occurrence before its edit: unmutated control exit 0 at `6 passed`; removing the `"diff"` handlers key is exit 1 at `2 failed, 4 passed`; making the structural route pass `task_id=None` is exit 1 at `2 failed, 4 passed`, and it fails on the assertion that the task run's files are its OWN, which is the discriminator that fixture pair exists for; and answering 404 instead of 200 for an unknown run is exit 1 at `1 failed, 5 passed`. THE ROUTE-WALK GUARD WAS MEASURED IN BOTH PLACES AND IS UNMOVED AT `106 passed`, in the primary checkout and inside the worktree, which matters because C4 edited that very file. THE DESIGN DECISION THE ROUND CARRIES IS RIGHT AND IS PINNED: an unknown task run answers 200 with `available` False and `reason` `unknown_task_run` rather than 404, because absence is DATA in this envelope and a 404 would make a job with no diff indistinguishable from a bad URL — and the test asserts the status explicitly so a later change to 404 is a red rather than a silent drift. THE ROUND ADDED NO NEW LITERAL GET ROUTE, so the `LITERAL_GET_ROUTES` exact-set guard was never at risk, and the job scope was deliberately made a dict key so the AST walk acquires it for free while the structural route was registered in `_walkable_paths` by hand. `R-0715` IS RESOLVED ABOVE. THE RECORD MOVED AS ORDERED: `^- R-\d+ — ` unmoved at 279, `^Done: R-\d+ — ` unmoved at 27, `^Landed: R-` 1 to 2, `^Gate: F\d+ R\d+ — ` 76 to 77, and the open set 252 at both points. ONE DEVIATION IS DECLARED AND IT IS A REPAIR OF THE REVIEWER'S OWN GATE: G5 worded append reader (a) as a length sum plus a byte-prefix check, and those two properties together cannot reject a byte flipped INSIDE the appended region, which is precisely what the same gate's negative control ordered them to reject; the worker implemented the stronger byte IDENTITY instead and said so. The reviewer accepts the stronger reading, has adopted it in this round's own gates, and records the authoring failure in `.agent/prose_slips.md` with no id, because nothing landed wrong on disk. NO BLOCK CONDITION AROSE: nothing fabricated, no false live indicator, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER7

<<<SLICE R0719
- R-0719 — Medium, THE FEATURE FILE SENDS EVERY UI BUILDER OF THIS FEATURE TO A DESIGN-REFERENCE SECTION THAT DOES NOT EXIST. Raised by the reviewer at the F037 R7 gate, while scoping T002; no round was ordered to look for it. `docs/roadmap/features/T5_F037.md:14` closes its CANONICAL DESIGN REFERENCE banner with "Feature-specific: diff surface tokens per `ux_spec.md`; the viewer's entry-point contract per `component_spec.md`." THE SECOND HALF RESOLVES AND THE FIRST DOES NOT. MEASURED BY THE REVIEWER AT `996ffea9`, case-insensitively over the whole of `docs/ui/design_reference/ux_spec.md`: the string `diff` occurs ZERO times, so there are no diff surface tokens there to follow, and a grep of the whole design-reference folder returns the viewer's material in two OTHER files entirely — `component_spec.md:113-116`, which names the entry point `onOpenDiff(taskId)` from `DetailPopover` and states that the design-reference package deliberately does not build the viewer, and `assets_spec.md:92-95`, which puts the mono family on diff surfaces and requires ligatures OFF via `font-feature-settings:"liga" 0`. THE EFFECT IS ON THE FEATURE'S WHOLE REMAINING SCOPE, which is why this is not cosmetic: the same banner binds builders to the design reference and forbids inventing a visual language, with any deviation requiring an assumption_log entry, so a T002 builder told to take diff tokens from `ux_spec.md` finds nothing, and the two honest routes left to it are to stall or to invent — and the banner forbids the second. MEDIUM AND NOT HIGH because nothing is unbuildable and no suite is red: the Design section of the feature file itself carries the binding CSS, and the reviewer confirmed at `996ffea9` that the two custom properties that CSS names, `--remedy-ink-soft` and `--remedy-bg-2`, are both really defined in the shipped sheet `apps/ui/src/styles/tokens.css`, so the visual authority does exist — it is only pointed at the wrong file. NOT LOW because T002 and T003 are the entire remaining scope of this feature and both are UI rounds that read this banner first. THIS IS NOT `R-0715`, which was a stale numeral in a test docstring, and not `R-0427`, which is a stale claim in a module docstring under `packages/`: this is a pointer to a section that never existed rather than a sentence that went stale. COUNTER-MEASURE: amend the feature file rather than the design reference, because the design reference is the operator's artifact and its silence on the viewer is deliberate — `component_spec.md:115-116` says so in as many words. The amendment names the three real authorities, and the reviewer authors it into this same round as A4 with DECISION F037 D3 recording the choice and how to reverse it. OPEN.
<<<END R0719

<<<SLICE SLIPR8
- 2026-08-28 · F037 R7 · G5 worded append reader (a) as a length sum plus a
  byte-PREFIX check, and those two properties together cannot reject a byte
  flipped INSIDE the appended region — which is exactly the rejection the same
  gate's negative control ordered them to produce, so the control could have
  passed a corrupted append. The worker implemented the stronger byte IDENTITY
  `result == before + b"\n" + slice` and declared the substitution. An append
  reader is stated as the IDENTITY it must prove, never as an arithmetic a
  control can satisfy.
<<<END SLIPR8

<<<SLICE AMEND4
**A4 — the diff surface's design authority is this file's binding CSS together
with `component_spec.md` and `assets_spec.md`; `ux_spec.md` carries nothing
about diffs (finding `R-0719`, DECISION F037 D3).** The CANONICAL DESIGN
REFERENCE banner at the top of this file ends with "Feature-specific: diff
surface tokens per `ux_spec.md`". Measured at `996ffea9`, case-insensitively
over the whole of `docs/ui/design_reference/ux_spec.md`, the string `diff`
occurs ZERO times: there are no diff surface tokens in that file to follow. The
three authorities that DO exist, and which builders of T002 and T003 follow
instead:

1. The binding CSS block in the Design section of this file. Its two custom
   properties resolve in the shipped sheet: `--remedy-ink-soft` and
   `--remedy-bg-2` are both defined in `apps/ui/src/styles/tokens.css`.
2. `docs/ui/design_reference/component_spec.md:113-116` — the entry point is a
   button in `DetailPopover` emitting `onOpenDiff(taskId)`. That section also
   states that the design-reference package deliberately does NOT build the
   viewer, which is why F037 owns it and why the silence elsewhere is not an
   oversight to be filled by invention.
3. `docs/ui/design_reference/assets_spec.md:92-95` — the mono family applies to
   diff surfaces, and ligatures are OFF there:
   `font-feature-settings:"liga" 0`.

The banner's `ux_spec.md` pointer is SUPERSEDED for the diff surface and for
nothing else; every other clause of that banner, including the prohibition on
inventing a visual language and the assumption_log requirement for any
deviation, stands unchanged.
<<<END AMEND4

<<<SLICE DECISION3
## DECISION F037 D3 — the diff surface's design authority is named in the feature file, and `ux_spec.md` is not one of the three (2026-08-28, F037 R8)

CONTEXT. `docs/roadmap/features/T5_F037.md:14` directs builders to "diff surface
tokens per `ux_spec.md`". Measured at `996ffea9`, `docs/ui/design_reference/ux_spec.md`
contains no occurrence of `diff` at all, case-insensitively, so that pointer
resolves to nothing. T002 and T003 are the entire remaining scope of this
feature and both are UI rounds whose builders read that banner first. Registered
as finding `R-0719`.

CHOSEN. Amend the FEATURE FILE with amendment A4, naming the three authorities
that do exist: this file's own binding CSS, whose `--remedy-ink-soft` and
`--remedy-bg-2` were confirmed present in `apps/ui/src/styles/tokens.css`;
`component_spec.md:113-116` for the entry-point contract; and
`assets_spec.md:92-95` for the mono family and the ligatures-off rule on diff
surfaces. The banner's other clauses are untouched.

ALTERNATIVES CONSIDERED. (a) Add a diff-surface section to `ux_spec.md`. Rejected:
the design reference is the operator's artifact, AGENTS.md's documentation
boundary keeps `docs/` describing what IS, and `component_spec.md:115-116`
states that the design-reference package deliberately does not build the viewer
— so its silence is a decision, not a gap for a feature branch to fill.
(b) Delete the clause and leave the diff surface unattributed. Rejected: it would
leave a builder with a banner that forbids inventing a visual language and no
authority to follow, which is the same defect wearing a shorter sentence.
(c) Leave it and rely on reviewers to catch it each round. Rejected: it had
already survived seven rounds unread.

REVERSE by deleting amendment A4 from `docs/roadmap/features/T5_F037.md` and
this decision, restoring the banner's `ux_spec.md` pointer as the sole
feature-specific authority for the diff surface.
<<<END DECISION3
