── STEP R24 — F031 Decision inbox ────────────────────────────
Goal:        T002b BADGE, THE HALF THAT COUNTS — server side. DECISION F031
             D2's two CONSTANT-ZERO counters in `ui_server.py` are replaced by
             one re-derivation over `decision_queue.list_decisions`, so
             `metrics.open` and `open_decision_count` finally answer with the
             number of open decisions a job really has. The R23 verdict, the
             third `R-0593` instance and one new finding are written first.

Fortschritt: ~82 % (F031 claimed; R1 through R23 landed, R23 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING and FILTERING SHIPPED and gated · T002b badge
             SERVER half here, its UI half at R25 · T003 offen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R23 gate entry, the R-0593 recurrence and the new
             finding · C3 the counter re-derivation, its tests and DECISION
             F031 D9 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r24.md                (C0a)
             .agent/last_block.md                       (C0b)
             .agent/plan.md                             (C1)
             .agent/live_review.md                      (C2)
             packages/orchestration/ui_server.py        (C3)
             tests/ui_server/test_live_state.py         (C3)
             tests/ui_server/test_dashboard_contract.py (C3)
             .agent/decisions.md                        (C3, D9)
             .agent/handoff.md                          (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).
             NOTHING under `apps/` is written this round. The badge's MARKUP
             is R25's, and so are the two comment repairs C2 records.

── Base ──────────────────────────────────────────────────────
The round base is `030a43d1597dfc3b00933dacb50e882728a434e7`, the R23
handback commit and the tip of `feature/f031-decision-inbox`, local and
remote EQUAL — the reviewer measured both with `git ls-remote` at the R23
gate. Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here resolved under `git cat-file -t` before emission;
the types are NOT all `commit`, and G8 does not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 665858 bytes; `^- R-\d+ — ` 242 all DISTINCT,
  maximum `R-0681`; `^Done: R-\d+ — ` 4, so the §3 item 10 open set is
  238; `^Recurrence: R-` 18; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and
  `^Gate: F\d+ R\d+ — ` 4, those four being `F031 R19`, `F031 R20`,
  `F031 R21` and `F031 R22`.
- `.agent/plan.md` 45 lines, 2581 bytes. `docs/roadmap/**` is UNTOUCHED,
  so the §3 docs-round gate is not earned and is not ordered. `apps/ui`
  is untouched too, so no `npm` command is ordered anywhere in G1–G9.
- The Python suites, every one exit 0: `tests/ui_server/` 474,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate`
  16, `test_autonomy` 81, `test_golden_path` 42. `python3 -m ruff check`
  over the three Python paths the change set names: "All checks passed!".
- THE TWO COUNTERS ARE CONSTANT ZERO, which is WHY this round exists.
  `_build_dashboard` computes `decision_count` by scanning events for
  `human_decision_requested`, and `_build_live_state_json` computes its
  local `open_decisions` the same way; `blocker_count`, the other addend
  of `metrics.open`, scans for `stop_reason_recorded`. The reviewer
  grepped the whole repository outside `tests/` and `.agent/` for BOTH
  event names: every occurrence is a READER, there is NO EMITTER, and the
  only writers of either string are test fixtures. So `metrics.open` and
  `open_decision_count` are BOTH constant zero in production today, which
  is one fact more than DECISION F031 D2 records.
- THE DERIVATION ALREADY EXISTS AND IS CHEAP. `decision_queue` exports
  `list_decisions(job, events)` and `open_decisions(decisions)`; measured
  on a Core `Job` of 50 tasks against 500 events at 0.309 ms per combined
  call, so calling it per dashboard build costs nothing to design around.
- THE FIXTURES ARE MEASURED, NOT ASSUMED (§3 item 8). At this base, with
  `list_decisions` called directly: a `Job` carrying NO `target_repo` in
  its metadata and one task yields exactly ONE open decision, of type
  `stop_reason` and severity `blocker` — the "No target repository
  attached to job." reason `stop_reasons.derive_stop_reasons` raises. The
  SAME job with `target_repo` set and no events yields ZERO, and with
  `target_repo` set plus three `human_decision_requested` events STILL
  yields ZERO. That third shape is the discriminator S3 needs: the old
  event scan answers 3 for it and the new derivation answers 0.
- THE SUITE GUARDS OVER `ui_server.py` were read first (§3 item 7): the
  only `.count(...) ==` assertion over that file anywhere under `tests/`
  is `source.count("exec_guard.run_guarded_runtime_build_command(") == 2`
  in `tests/ui_server/test_dashboard_contract.py`, which S1 does not
  touch, and no `== 1` assertion reads it at all. Adding a symbol is safe.
- THE EVENT-INJECTION IDIOM this repository already uses for these
  builders is `patch("packages.orchestration.ui_server._load_events",
  return_value=events)`, as `tests/test_repair_context_reviewer_memory.py`
  does: both builders take only `job` and load their own events.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission
  and stated so your re-measurement can disagree with the reviewer's, are
  490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085
  D5). G2 orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D9 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S4 fixes behaviour,
   structure and naming; YOU write that code, those tests and that
   decision entry under AGENTS.md's Mandatory Self-Review Loop and its
   File Editing Safety Rules. Where the spec is silent, prefer the idiom
   the neighbouring code already uses. Where the spec is WRONG, say so in
   the handback and do the right thing.
3. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r24.md` at C0a and mirrored byte-identically into
   `.agent/last_block.md` at C0b. Extract every slice PROGRAMMATICALLY out
   of the COMMITTED C0a blob by its marker LINES — `<<<SLICE <NAME>` opens,
   `<<<END <NAME>` closes. Marker lines never reach a target file.
4. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra commit,
   none dropped, no reordering. C1 is FIRST substantive because this round
   writes the finding ledger (§3 item 23). To correct a landed commit, do
   NOT add one outside this sequence — declare it, and give it its own
   `## Commits` and item-status rows (R-0675).
5. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
6. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present,
   finish the commit in hand, write the handback and stop. NEVER delete
   that sentinel (R-0347).
7. The slices this block carries are the whole text PLANF031R24 and the
   appended text LEDGER24. This paragraph names them and states no count;
   G2 orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention each slice already ends in a newline, so `.agent/live_review.md`
   after C2 is EXACTLY: its blob at C1, then one newline, then LEDGER24 —
   and it receives NOTHING ELSE in that commit (R-0657). LEDGER24's own
   paragraph count is yours to measure; this paragraph states no number.
   `.agent/decisions.md` also GROWS at C3, but by text YOU author under S4,
   so no equality gate is ordered over it and none may be reported.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported
   and no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER24 is an append.
10. THIS ROUND MINTS EXACTLY ONE FINDING ID AND RESOLVES NONE. LEDGER24
    carries `R-0682`, so `^- R-\d+ — ` moves 242 → 243 with the maximum
    moving `R-0681` → `R-0682`, and `^Recurrence: R-` moves 18 → 19. Both
    `^Done: R-` and `^Landed: R-` stay UNCHANGED at 4 and 0, so the §3
    item 10 open set moves 238 → 239. WRITE NO `Landed:` LINE and no
    `Done:` line: R-0593 stays OPEN and R-0682 is minted OPEN, their fixes
    routed to R25 by the plan. R-0593's landed paragraph and its earlier
    `Recurrence:` paragraph are NOT edited (§3 item 20) — LEDGER24 appends
    a SECOND recurrence paragraph beside them.
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/` or
    `apps/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `packages/` only `ui_server.py` is
    written — NOT `decision_queue.py`, NOT `decision_inbox.py`, NOT
    `stop_reasons.py`. Inside `tests/` only the two files the change set
    names. THE FEATURE FILE IS NOT EDITED: DECISION F031 D2 already
    amended it for this round and S4 adds no amendment to it.
12. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the
    G7 suites. Everything already there is pre-existing scratch belonging
    to no commit, this block's own file included: create no worktree at an
    existing path, and delete nothing you did not create.

── Specification (S1–S4) — the production change ─────────────
S1  THE ONE DERIVATION, in `packages/orchestration/ui_server.py`. Add a
    single module-level private helper — name it for what it answers, two
    to four words carrying the domain word, in the shape AGENTS.md's Code
    Discoverability Conventions fix — which takes the job and its already
    loaded events and returns the NUMBER of open decisions as an `int`.
    It imports `list_decisions` and `open_decisions` from
    `packages.orchestration.decision_queue` INSIDE the function, the idiom
    every other derivation here uses, and catches the same narrow exception
    set `_build_orchestrator_section` catches, returning 0 rather than
    propagating, because both fields it feeds are typed `int` with no
    unknown state. Say that in the one-line WHY comment above it.
    THE NAME MUST NOT COLLIDE. `ui_server.py` already imports a DIFFERENT
    `list_decisions`, from `orchestrator_brain`, inside
    `_build_orchestrator_section`; keep the two distinguishable at the
    call site rather than letting one spelling mean two functions.

S2  THE TWO CALL SITES, in the same file, each becoming one call to S1's
    helper. (a) In `_build_live_state_json`, the local `open_decisions`
    computed by scanning events for `human_decision_requested` is REPLACED
    — note that its current local NAME is the same word as the
    `decision_queue` export S1 imports, so do not leave a shadow standing.
    `open_decision_count` in the returned payload keeps its key and its
    type. (b) In `_build_dashboard`, `decision_count` is replaced the same
    way. `blocker_count` then has NO remaining reader, since `metrics.open`
    is its only use: RETIRE IT with the expression that used it, under
    DECISION F031 D9 below, rather than leaving a dead local behind.
    `metrics.open` keeps its key, its type and its position; only the
    number it carries changes.

S3  THE TESTS, in the two files the change set names, each beside the
    tests already covering that builder and following that file's existing
    fixture idiom, using the `_load_events` patch the Base section names.
    Cover, at minimum, these three properties, which the Base section
    measured at this round's base and which the OLD code fails:
    (a) the repo-less job — no `target_repo`, one task, no events — makes
    `_build_live_state_json(...)["open_decision_count"]` and
    `_build_dashboard(...)["metrics"]["open"]` BOTH answer the number
    `open_decisions(list_decisions(...))` gives for that same job, which
    is not zero;
    (b) a job with `target_repo` set and no events makes both answer zero,
    so the count is not merely "always positive";
    (c) THE DISCRIMINATOR: a job with `target_repo` set plus several
    `human_decision_requested` events makes both STILL answer zero — the
    proof that the event ledger no longer feeds either field. Derive each
    expected number from `open_decisions(list_decisions(job, events))` in
    the test itself rather than hardcoding it, so the tests pin the
    DERIVATION and not one fixture's arithmetic. Name every test for the
    property it pins, not for a step number.

S4  DECISION F031 D9, appended to `.agent/decisions.md` in the shape D1
    through D8 already use there, ruling what `metrics.open` MEANS now.
    CHOSEN: `metrics.open` is the count of OPEN DECISIONS alone, so
    `blocker_count` leaves that sum and the `stop_reason_recorded` scan
    retires with it. WHY: `decision_queue` is already the aggregation of
    everything a human must act on and its own branch 2 derives a
    `stop_reason` decision from `derive_stop_reasons`, so keeping the
    addend would double-count the same blocker the day either event name
    gains an emitter — and TODAY it adds a measured constant zero, so
    nothing observable is lost by removing it. Record the measurement the
    Base section states: neither `human_decision_requested` nor
    `stop_reason_recorded` has any emitter outside tests. ALTERNATIVE:
    keeping `blocker_count + <new count>`, rejected as a latent
    double-count that no test would catch while both addends are zero.
    REVERSE by restoring the addend and its scan.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R24
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D9.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R24 OPENS T002b's badge with its SERVER half: one re-derivation over
`decision_queue.list_decisions` replaces the two constant-zero counters DECISION
F031 D2 names in `ui_server.py`, so `metrics.open` and `open_decision_count`
answer with a real number, pinned by tests in both builder suites.

## Next Steps
1. R25 the badge's UI half — the count rendered where the operator sees it —
   plus the two comment repairs R-0682 and the R-0593 recurrence route there.
2. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE COUNT IS A NEW READ ON A HOT PATH: `_build_live_state_json` answers the
  cockpit's poll, so the derivation it now calls must stay total and cheap. It
  is measured at 0.309 ms for 50 tasks against 500 events, and every branch of
  `list_decisions` already guards itself, but a raise escaping it would break
  the dashboard rather than the badge.
- A FAILURE READS AS ZERO, because both fields are typed `int` and carry no
  unknown state. That is honest only while the WHY comment above the helper
  says so and names `_build_orchestrator_section` as the richer shape.
- NO EVENT KIND IS ADDED, per DECISION F031 D2. A round that "fixes" the badge
  by emitting `decision.requested` has left this design, not completed it.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `f548277e`, and this round's C2 raises it to 239 by minting
  R-0682, in the commit order the R24 block's constraint 4 fixes.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 and
  R-0682; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R24

<<<SLICE LEDGER24
Gate: F031 R23 — the F031 R23 entry. R23 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r23.md`, the C0a blob committed at `85bd1995`, the C0b blob committed at `15919a4d`, and `.agent/last_block.md` read off disk at `030a43d1` are ALL FOUR byte-identical at sha256 `aeae1dd3f6c7c9ee7aeb3ac059b54501d81bf827d636dc1242818a1845014623` over 37051 bytes and 443 lines, C0a and C0b resolving to the SAME git blob `e0d5e6231a89c5069f79d6e6e740e1cea8392972`. THE EXTRACTION printed 2 slices, 46 content lines and 443 total, so PROSE was 443 − 46 = 397 against the 400-line cap DECISION F085 D5 sets and TOTAL 443 against the 490 DECISION F085 D6 sets — three lines of prose margin for a second round running, which is why R24's design was measured against the caps before its spec was written. THE PLAN at `114394a0` equals PLANF031R23 exactly at 2581 bytes and 45 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 45 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `f548277e` is its C1 blob plus one newline plus LEDGER23, at 657516 + 1 + 8341 = 665858 against an actual 665858, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 305 to 306 and its last 1 unit equals LEDGER23's paragraph once trailing newlines are rstripped on BOTH sides, the handling the R21 and R22 entries already record as necessary. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on disk, flipping one byte inside the appended region: both readers REJECT the mutant and both ACCEPT the true file. THE SETS MOVED ONLY WHERE CONSTRAINT 10 ALLOWED: `^- R-\d+ — ` 242 to 242 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` unchanged, `^Done: R-` 4 to 4, `^Landed: R-` 0 to 0 and `^Recurrence: R-` 18 to 18. THE SPLIT SERIES BEHAVED AS DECISION F031 D7 RULES for a fourth round running: `^Gate: R\d+ — ` 19 to 19, frozen, and `^Gate: F\d+ R\d+ — ` 3 to 4, the added key exactly `F031 R22`, all keys DISTINCT. The §3 item 10 open set is 238 at `f548277e`, and `- R-0593 — ` occurs exactly ONCE line-anchored and `^Recurrence: R-0593` exactly ONCE, so its paragraphs were not edited. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with ZERO diagnostics on stdout and stderr; `npm run test:unit` at 23 files and 352 tests with `decisionCard.test.ts` 27, `decisionOrder.test.ts` 16 and `decisionFilter.test.ts` 20, every one UNMOVED as a round adding no test requires; and in Python `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and `test_golden_path` 42 — every count identical to the base readings. G6(b)'s GREEN IS CORRECT BY CONSTRUCTION AND THE REVIEWER CONFIRMED IT WITHOUT MUTATING ANYTHING: `apps/ui` collects 23 `.test.ts` files and not one of them imports `DecisionInboxCard`, whose only importer anywhere under `apps/ui/src` is `RightLivePanel.tsx`, so no test can reach that guard and the empty-state trap really is pinned by `tsc`, structure and review alone — the gap DECISION F031 D5 accepts, measured rather than assumed. THE ORDERING SEAM SURVIVED THE FILTER, which is the property R23 could most easily have broken: `RightLivePanel.tsx` still passes `orderDecisionInbox(dashboard.decisionInbox)` to the card, `filterDecisionsByType` returns `models.slice()` or `Array.prototype.filter`, and neither re-sorts, so DECISION F031 D6's rule reaches the rendered list unchanged. DEVIATION 2 IS A REAL SPEC CATCH BY THE WORKER, not a deviation to forgive, and the reviewer measured its ground: `--remedy-focus` is defined in `docs/ui/design_reference/tokens.css` and occurs ZERO times in `apps/ui/src/styles/tokens.css`, while every one of the eight custom properties the C3/C3b sheet does name — `--remedy-radius-pill`, `--remedy-bg-2`, `--remedy-line`, `--remedy-line-strong`, `--remedy-muted`, `--remedy-ink`, `--remedy-blue-50` and `--remedy-blue-strong` — is defined in BOTH sheets, so the shipped ring resolves and the fallback form really would have turned `TestEveryCustomPropertyResolves` red. `.emptyState` occurs exactly once in `RightLivePanel.module.css`, so deviation 4's reuse names a class that exists. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `114394a0`, `.agent/live_review.md` at `f548277e` and all four files C3 and C3b write, against a CONTROL of 2 and 2 over the C0a blob; the range `879bd137`..`44435f81` names 8 paths, none under `docs/`, `packages/` or `tests/` and none of `.agent/context.md`, either inventory, `RightLivePanel.tsx` or `decisionFilter.ts`, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the seven commits of `879bd137`..`030a43d1` are each SINGLE-PARENT with insertions 443, 251, 17, 2, 168, 26 and 70 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and the first six agree CELL FOR CELL with the `+/-` column of that handback's `## Commits` table, which is the §3 item 28 reading; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 24 SHA-shaped occurrences, 11 distinct, failing set EMPTY, 9 `commit` and 2 `blob`. THE REFLOG read by OPERATION PREFIX over this round's seven entries is `commit` seven times, with amend 0, rebase 0 and cherry 0. THE PUSH DISCHARGED, which is the outcome G9 routed to the reviewer rather than to any file R23 wrote: measured with `git ls-remote`, `refs/heads/feature/f031-decision-inbox` and the local tip are both `030a43d1597dfc3b00933dacb50e882728a434e7`, and no pull request was created, no branch deleted and nothing merged. THE HANDBACK FITS ITS TIER WITH NO OVERAGE: 93 lines against the 100 AGENTS.md allows for its 7 commits, every mandated section present, and C3b correctly carried its own `## Commits` and item-status rows as R-0675 requires. THE VERDICT IS PASS. What R23 earns is not a finding against its execution but two entries against the REVIEWER'S OWN change set, appended beside this one.

Recurrence: R-0593 — A THIRD INSTANCE IN `apps/ui`, AND IT IS THIS FINDING'S BINDING FIX CLAUSE GOING UNSERVED FOR THE SECOND TIME BY THE REVIEWER, IN A CHANGE SET, EXACTLY AS THE F008 R33 PARAGRAPH OF THE LANDED ENTRY DESCRIBES. Measured by the reviewer at `030a43d1` by reading both files. `apps/ui/src/api/decisionFilter.ts` still carries the header sentence R22 wrote: "THE SEAM IS NOT WIRED YET — `RightLivePanel.tsx` still hands `orderDecisionInbox(...)` straight to the card — and `decisionInboxView` is the shape that wiring will call, which is why it exists a round before its caller does." R23's C3, `6147efc4`, GAVE IT THAT CALLER: `DecisionInboxCard.tsx` imports `DECISION_FILTER_ALL` and `decisionInboxView` from `../../api/decisionFilter` and calls the view once per render. The middle clause stays literally TRUE — `RightLivePanel.tsx` really does still hand `orderDecisionInbox(dashboard.decisionInbox)` to the card, and R23 deliberately left it that way — and the clauses either side of it are now false: the seam IS wired, and the module no longer exists a round before its caller. THAT IS THE SAME ONE-DIRECTIONAL DISCOVERABILITY GAP the earlier recurrence records, arriving in the module the earlier recurrence's own fix created: a reader who searches `decisionFilter.ts` for its consumer is told there is none. NO NEW ID IS MINTED for it (§3 item 30): R-0593 is the record of exactly this defect and holds the fix clause this instance breaks — "a block that adds a caller for a prop, a caller for a module, or a first use of anything an existing comment calls absent names that comment's file in its own change set". The R23 block did the OPPOSITE, and did it explicitly: its constraint 11 listed `decisionFilter.ts` among the files the round must NOT write, and its G8 gated the range for that file's ABSENCE. The worker applied every slice byte for byte and was right to, so the false sentence landed under a round that earns a PASS — which is what makes this the reviewer's entry rather than the worker's. THE COUNTER-MEASURE THIS TIME IS MECHANICAL RATHER THAN REMEMBERED: before an `apps/ui` change set is fixed, grep the modules it will newly IMPORT for the words "not wired", "no caller", "before its caller" and "still absent", and name any file that matches. R-0593 stays OPEN with its instances in `packages/orchestration/release_gate.py` and `pyproject.toml` untouched; its landed paragraph and its first `Recurrence:` paragraph are not edited (§3 item 20), and the fix for this instance is routed to R25 by `.agent/plan.md` at this round's C1.

- R-0682 — Low, A CHIP ROW'S GROUP LABEL IS ANNOUNCED TO NOBODY, AND THE BLOCK THAT ORDERED IT CITED A DESIGN-REFERENCE ENTRY THAT DOES NOT ORDER IT. Raised by the reviewer at the F031 R23 gate, by reading the shipped markup against the spec it cites. MEASURED at `030a43d1`: `apps/ui/src/components/panels/DecisionInboxCard.tsx` renders the chip strip as `<div className={styles.decisionFilterRow} aria-label={FILTER_CHIPS_LABEL}>` with NO `role` attribute, and `apps/ui/src/components/graph/GraphFilterChips.tsx` has carried the same shape since before this feature, as `<div className={styles.chips} aria-label="Graph filters">`. A `div` with no role maps to the ARIA `generic` role, and `generic` prohibits an accessible name, so NEITHER label reaches the accessibility tree: both strings are computed, shipped and dropped. THE CITATION IS THE OTHER HALF. The R23 block's S1 ordered "the chip row carries an `aria-label`" and attributed that to `component_spec.md`'s FilterChips entry, and that entry — measured at the same commit — reads "A11y: aria-pressed buttons; filter changes announce via polite live region" and names no row label at all. So a requirement the design reference does not make was attributed to it, which is the R-0338 class, and the attribution is what stopped anyone asking how the label would be exposed. WHY LOW AND NOT MEDIUM: everything `component_spec.md` DOES order is shipped and works — `aria-pressed` sits on every chip and the list sits inside `aria-live="polite"` — so the control is operable, its state is announced and its changes are announced; the whole loss is the group's NAME, and a screen-reader user reaches the same chips with the same states either way. WHY IT IS A FINDING AT ALL: an inert attribute is worse than an absent one, because it reads on the page as accessibility work already done, and the next reader copies the pattern — which is precisely how it reached the second file. FIX, routed to R25 with the R-0593 recurrence because R24's change set holds no `apps/` path: add `role="group"` beside the existing `aria-label` in BOTH files, the ARIA pattern that makes a labelled group nameable, and consider pinning it in `tests/ui_contracts/`, which already reads both files. SEARCHED BEFORE MINTING per §3 item 30: at `f548277e` the strings `aria-label`, `accessib`, `aria-pressed` and `screen reader` each occur ZERO times in `.agent/live_review.md` and `role=` occurs once, inside an unrelated entry, so no open finding describes this defect and no id is being duplicated.
<<<END LEDGER24

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback, transcripts kept out of it
(R-0582). "Green" as a word is a finding. Every gate runs at a commit
STRICTLY EARLIER than C4 (§3 item 31); G9's push runs after it and names
its own carrier.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from
    disk is ABSENT before C0a and again before C4; `git status --porcelain`
    line count after each of C0a, C0b, C1, C2 and C3 is 0. Then report
    sha256, byte count and line count for FOUR readings —
    `.remedy-wt/f031-r24.md` before C0a, the committed C0a blob, the
    committed C0b blob, and `.agent/last_block.md` off disk after C0b — all
    four EQUAL, and the git blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL line count — the numbers YOUR extractor printed.
    Then report PROSE, computed as TOTAL minus CONTENT, against the two
    caps the Base section names. If either is exceeded, say so plainly and
    continue: an oversize block is the reviewer's defect to record, not
    yours to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R24 under
    your stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice with its
    trailing newline REMOVED. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l`
    STRICTLY under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER24's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because the R21, R22 and R23 entries all
    record that a naive split reports FALSE on a byte-perfect file. This
    slice carries MORE THAN ONE paragraph, so the ORDER of the last N units
    is load-bearing and a set comparison does not discharge it. NEGATIVE
    CONTROL: flip ONE byte inside the appended text; BOTH readers must
    reject the mutant and BOTH accept the true file. Do that flip in memory
    or under a disposable worktree per constraint 12, never on the tracked
    file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the
    shape constraint 10 states — report each side of every movement it
    names, plus that the ids ADDED are exactly `R-0682` and the ids REMOVED
    are the EMPTY SET, and that all `^- R-\d+ — ` ids are DISTINCT.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 4 → 5,
    the ADDED key being exactly `F031 R23`, all keys DISTINCT (§3 item 26).
    Report the §3 item 10 open set at C2 — paragraphs minus `Done:` lines.
    Report that `- R-0593 — ` still occurs exactly ONCE line-anchored, and
    report the `^Recurrence: R-0593` count, which constraint 10 moves.

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated. In `packages/orchestration/ui_server.py`
    INSIDE THAT WORKTREE, change the body of the S1 helper so it returns the
    literal `0` and nothing else, leaving every other byte of the file alone
    — which restores EXACTLY the behaviour the Base section measured at this
    round's base, where both fields are constant zero. Then run, from the
    worktree root:
      python3 -m pytest tests/ui_server/test_live_state.py -q
      python3 -m pytest tests/ui_server/test_dashboard_contract.py -q
    BOTH must go RED. Report the REAL exit code of each, the NAMES of the
    tests that failed, and the failure count YOUR run measured — this block
    states no number for it. A GREEN here means S3's tests do not reach the
    change and is reported as such rather than worked around. Restore
    nothing in the primary; remove the worktree BY ITS EXACT PATH and report
    `git worktree list` as 1 line after, naming that path.

G7  Structure, then the suites. Over `packages/orchestration/ui_server.py`
    at C3 report, as counts YOU measured: that the S1 helper's name occurs
    exactly ONCE as a `def`, that it occurs at each of the two call sites S2
    names, that `human_decision_requested` no longer occurs inside either
    `_build_dashboard` or `_build_live_state_json` — read the function
    bodies, not the whole file, since the humanize maps elsewhere in the
    module legitimately keep that string — and that `blocker_count` occurs
    ZERO times in the whole file. Then in the PRIMARY checkout at the C3
    tree, all REAL exit 0, run SERIALLY and never two alive at once, with
    `git worktree list` reported as 1 line immediately BEFORE the first of
    them, by these exact command lines with no extra flag:
      python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_live_state.py tests/ui_server/test_dashboard_contract.py
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/orchestration/test_autonomy.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus `test_autonomy.py` — which asserts `"open" in metrics` over
    the dashboard S2 changes — plus the canary. The reviewer ran all seven
    at `030a43d1` with these exact lines and measured, in that order, "All
    checks passed!" and then 474, 52, 21, 16, 81 and 42, every one exit 0.
    `tests/ui_server/` MUST EXCEED 474 by exactly the number of tests S3
    adds: report BOTH numbers and their difference, and account for any
    other difference.

G8  Markers, paths, commit shapes and object ids. Line-anchored
    `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2 and every file C3 writes, against the
    same counts over the COMMITTED C0a blob as a CONTROL, where they are
    NOT 0. ONLY the line-anchored reading is ordered — LEDGER24 quotes both
    markers inside backticks mid-line, so a raw SUBSTRING count is
    unmeetable and is NOT ordered. `git diff --name-only <base>..C3` names
    NO path under `docs/` or `apps/`, and neither `.agent/context.md` nor
    either inventory file nor `packages/orchestration/decision_queue.py`
    nor `packages/orchestration/decision_inbox.py`; the range path set
    MINUS the change set is EMPTY and the change set MINUS the range is
    exactly `.agent/handoff.md`, which C4 writes. Over C0a..C3 report per
    commit that it is single-parent and its INSERTION count — the `+`
    column only, per AGENTS.md DECISION F104 D1 — each under 500; those
    same numbers fill the `+/-` column of the `## Commits` table, derived
    from `git diff --numstat` and NOT from `git commit`'s own summary, and
    you report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only,
    by the OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry` each 0
    and how many entries you scoped to. Finally extract every SHA-shaped
    token from the COMMITTED C0a blob with the word-bounded pattern
    matching 7 to 40 hex characters — whose boundaries do NOT match the
    64-char sha256 digest this block also carries — pass each to
    `git cat-file -t`, and report the token count YOUR extractor measured,
    the type per token, and the FAILING SET, which MUST BE EMPTY. THE TYPES
    ARE NOT ALL `commit`: LEDGER24 quotes the git BLOB id
    `e0d5e6231a89c5069f79d6e6e740e1cea8392972`, resolved before emission.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY
    FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the
    next gate and records them in the R24 entry of `.agent/live_review.md`.
    In `## External actions` write the push COMMAND and that sentence. In
    the item-status table the push row is `done`, reason "ordered after C4;
    outcome carried by G9 to the reviewer". Report the real outcome in your
    final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C4, S1 through S4 and
the push, ONE LINE PER GATE with its real result, the finding counts, and
the next expected action. Carry the `Fortschritt:` block above VERBATIM —
count its lines yourself; no numeral is stated here.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED MECHANICALLY
BEFORE YOU COMMIT IT, or the list is named and NO numeral is given (R-0441).
Any finding count carries the RULE and the COMMIT it was measured at
(F009 D10); a narrower set is "the findings this feature must still act on".

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it
from AGENTS.md under `### handoff.md` against the commit count constraint 4
fixes, and report BOTH that count and the tier. If the MANDATED content
genuinely does not fit, exceed it and carry a DECISION D15 "Deviations,
declared" line naming your measured count as a NUMERAL (R-0430) and the
content behind it. Never drop a section to fit; claim no token cap.

THIS ROUND ENDS THE SESSION, so your `## Next` section is the next
session's first instruction and names, in order: that it reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule
2; that the R24 verdict is UNRECORDED and owed by the next round's ledger
commit (DECISION F085 D9); and that R25 is the badge's UI half, which also
carries the R-0682 fix and the third `R-0593` instance C2 records.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
