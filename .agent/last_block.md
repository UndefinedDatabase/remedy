# STEP R3/F040 — T001 PART 1: THE DIGEST COMPOSITION MODULE

Goal: build `packages/orchestration/job_digest.py`, the pure composition the
digest endpoint and `remedy job digest` will both render from — state, headline,
cost with its exactness basis, the honest-empty ownership list, the open-decision
count with its urgency peak, and the ONE primary action taken from the report's
own rule table. No endpoint and no CLI this round; those are the next one.

Base: `8e013dc5`, the round-2 handback commit and the tip of
`feature/f040-completion-digest`. Stay on that branch. Open no pull request.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r3.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN3
- C2  append slice RECORD3 to `.agent/live_review.md`
- C3  append slice SLIP3 to `.agent/prose_slips.md`
- C4  create `packages/orchestration/job_digest.py` per the SPEC below
- C5  create `tests/orchestration/test_job_digest.py` per the SPEC below
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r3.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/job_digest.py
    tests/orchestration/test_job_digest.py
    .agent/handoff.md

NOTHING under `apps/` changes, and no existing module under `packages/` is
edited. `packages/orchestration/ui_server.py` is NOT touched this round — the
endpoint is the next round's work and wiring it early would ship a route no test
covers.

## Constraints

1. Apply every slice BYTE FOR BYTE. If one looks wrong, apply it as given and
   DECLARE the problem in the handback's deviations.
2. C0a is a COPY: the block is at `.remedy-wt/f040-r3-block.md`. Use
   `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append.
4. `.agent/live_review.md` and `.agent/prose_slips.md` are APPEND-ONLY.
5. `.agent/plan.md` stays under 50 lines.
6. Every exit code is REAL, from `subprocess.run(...).returncode` in a script
   under the gitignored `.remedy-wt/`. Never through a pipe.
7. The mutation red-proof runs ONLY in a disposable `git worktree`; purge
   `__pycache__` and use `python3 -B` there. The primary checkout is
   `git status --porcelain` empty at every reading.
8. `job_digest.py` is a NEW module under `packages/orchestration/`, which is
   swept by repo-wide guards that name no path: the `REMEDY_DATA_DIR`
   single-reader invariant, the path-utils single-implementation invariant, the
   bare-`except: pass` ban, and the development-artifact boundary. Read a
   sibling module's header before writing and satisfy those guards by
   construction rather than by repair.
9. THE MODULE IS PURE COMPOSITION. It owns NO storage, writes NO file, starts NO
   subprocess and opens NO socket. It reads only through the seams named in the
   SPEC. A digest that persisted anything would be a second source of truth for
   state that already has one.
10. The `remedy` console script is DENIED; use `python3 -m apps.cli.grouped ...`
    if needed and say so.
11. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
12. Push after C6. No pull request, no merge, no force-push.

## Slices

The authored units are PLAN3, RECORD3 and SLIP3, each between its own BEGIN and
END marker line. The markers are NOT part of the unit; the unit starts on the
line after BEGIN and ends with the newline before END.

<<<BEGIN PLAN3
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 1, round 3.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2, D3 and D4 | done | round 2, PASS |
| the one-source urgency and R-0751 | done | round 2, PASS |
| T001 the composition module and its tests | done | this round |
| T001 the endpoint, its route tests and goldens | open | next round |
| T002 the hero card, triggers, the TS retirement | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round builds `packages/orchestration/job_digest.py` as a pure
   composition over the report sources, the inbox read path and the budget
   counters, with the four state-shape fixtures its tests are named for.
2. The round after it wires the endpoint into the server's handlers dict, adds
   its route tests and the goldens.
3. T002 then builds the hero card and retires the TypeScript urgency copy per
   DECISION F040 D2; T003 adds CLI parity and the end-to-end.

## Risks
- R-0570 and R-0752 (both Low) stay OPEN and are routed to the paydown branch:
  their fixes edit `README.md`, `tests/docs/test_docs_consistency.py` and
  thirteen feature files, none of which F040 owns.
- Two homes for the urgency formula exist until T002. They are pinned equal by
  `tests/ui_contracts/test_decision_urgency_parity.py` rather than trusted.
<<<END PLAN3

<<<BEGIN RECORD3
Gate: F040 R2 — THE SPEC-SETTLEMENT ROUND. VERDICT PASS. Reviewed by re-running every gate against the reviewer's own scratch original. TRANSPORT is REAL rather than self-consistent: the reviewer wrote the block to `.remedy-wt/f040-r2-block.md` before delegation and both committed copies equal it at sha256 `d05f9c085aa6227ae2de7a8dc666901900e2404b3aa657a480711ccf4ad39e1c` over 29954 bytes. THE PLAN is byte-equal to PLAN2 at 38 lines. THE RECORD APPEND reconstructs at 1643633 + 1 + 12099 = 1655733 with N counted as 5 and the paragraph order holding. THE LEDGER moved exactly as ordered: registered 311 to 312 with ADDED `['R-0751']`, resolved ADDED `[]`, `DECISION F040` ADDED `['D2','D3','D4']`, one `^Gate: F040 R1 — ` line, and `^Done: R-0570` still 0. THE SLIPS FILE gained exactly one line and its earlier bytes are a byte-exact prefix. THE TWO EDITED SOURCE FILES WERE PROVED WHOLE, which is the reading that matters most this round: the base blob of `docs/roadmap/features/T5_F040.md` with EXACTLY the two authored pairs substituted is BYTE-EQUAL to the committed blob, and the same holds for `packages/orchestration/run_report.py` with PAIRCOMMENT — so no other line of either file moved, which no FROM/TO count alone can establish. The singular test-directory spelling now reads 0 in the feature file. THE NEW BEHAVIOUR WAS RE-PROVED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, control first: unmutated 58 passed at REAL exit 0, then the single mutation of `decision_urgency`'s returned expression to `blocked * age` gave REAL exit 1 at 9 failed and 49 passed, then the restored bytes gave 58 passed again — so the tests genuinely bite on the `+ 1` that DECISION F031 D6 exists to protect. The worktree was removed and `git worktree list` holds the primary checkout alone. TEN SUITES were re-run serially in the primary checkout, every one REAL exit 0: `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 508, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_run_report.py` 81, `test_decision_inbox.py` 43, `tests/ui_contracts/` 699 passed with 4 skipped, and the canary 42. ELEVEN COMMITS, one path each, insertions 349, 299, 19, 10, 1, 16, 1, 51, 72, 185 and — the reading the handback cannot take of itself, supplied here per §3 item 31 — 281 for the handback commit, every one under 500. THE WORKER'S SIX DEVIATIONS WERE ALL CORRECTLY DECLARED AND NONE IS A FINDING. Three of them are defects in the reviewer's own block text and are recorded as prose slips rather than ids, per amend0827 rule 2: a false numeral inside RECORD2, the "new test class" instruction contradicting the same SPEC's "follow its conventions" over a file holding only module-level functions, and a G4 clause that required the slips file to grow by exactly one line and thereby FORBADE the blank separator every other entry in that file carries. The worker's judgement on the remaining three was right in each case — adding the new function to the module's `Public API::` docstring list was outside a strict reading of constraint 8 and is exactly the stale-list defect R-0746 records, so leaving it out to obey the letter would have shipped the very defect the round was fixing next door.

- R-0752 — Low, THIRTEEN FEATURE FILES SEND THEIR BUILDERS TO A TEST DIRECTORY THAT HAS NEVER EXISTED. Raised by the reviewer at the F040 R2 gate, from the worker's own G5 sweep: the round corrected the spelling in `docs/roadmap/features/T5_F040.md` and the sweep measured how far the same typo reaches. THE MEASUREMENT, taken at `8e013dc5` with `git grep -ln "tests/ui_contract/" -- docs/roadmap/features/`: thirteen files — T4_F119, T4_F126, T5_F008, T5_F009, T5_F019, T5_F022, T5_F023, T5_F024, T5_F031, T5_F038, T5_F041, T5_F042 and T7_F142 — name the SINGULAR `tests/ui_contract/` while the directory that exists is the PLURAL `tests/ui_contracts/`. Low, because nothing executes a feature file, and the cost is bounded and repeatable rather than hypothetical: F009 hit it at R2 and spent a DECISION on it, F031 hit it again at R7, and F040 hit it a third time at R1 — three features have each paid a fraction of a round rediscovering the same typo, and eleven more files are still armed. The open set was searched for the DEFECT before this id was minted, per §3 item 30: `R-0719` is the nearest shape — a feature file routing builders to a design-reference section that does not exist — but it names F037's file and that section, not this path, so the evidence does not join it. NOT F040's TO FIX: the repair edits thirteen files this feature does not own, and AGENTS.md's Scope Control forbids mixing it into a feature branch. It routes to the same paydown branch as `R-0570`, and it is cheap there — one mechanical substitution plus a pin asserting the singular spelling appears in no file under `docs/roadmap/features/`, which is the half that stops it recurring a fourth time.

DECISION F040 D5 — THE PRIMARY ACTION NAMES ITS RULE AND CARRIES NO DEEP LINK, BECAUSE THERE IS NOTHING TO LINK INTO. THE PROBLEM: `docs/roadmap/features/T5_F040.md:42` specifies `primary_action {label, deep link}`. MEASURED by the reviewer at `8e013dc5`: `grep -rn "deep_link\|deepLink" packages/ apps/ui/src` returns NOTHING, and neither does a search for `location.hash`, a router or a route table under `apps/ui/src` — the cockpit is a single page with no routing layer, so there is no address a deep link could hold and no consumer that could follow one. CHOSEN: `primary_action` carries `label` and `rule_id`, and the envelope carries NO `deep_link` key at all. The SERVER names the RULE; the CLIENT decides the affordance. That is the same one-source discipline the CTA itself follows — the label already comes verbatim from `recommended_next_action`, so the digest and the report cannot disagree — and it extends it to the navigation: T002 maps `rule_id` to an in-page action using the focus mechanism F021 already shipped for feed rows, rather than inventing a URL scheme that nothing parses. ALTERNATIVES CONSIDERED: (a) emit a `deep_link` string against a route scheme invented now — rejected, it would be a published field with no reader and no parser, and the first real router would have to honour or break it; (b) emit `deep_link: null` for shape fidelity — rejected because a key that is always null is indistinguishable on the wire from one whose producer is broken, and this repository's own honesty rule prefers an absent key to a null one. HOW TO REVERSE: add the key when a routing layer exists; adding a field is additive and needs no version bump. NOTE THE ASYMMETRY WITH DECISION F040 D3, which is deliberate: `ownership` KEEPS its key as an empty list because its producer F035 is a scheduled feature that will fill it, while `deep_link` has no scheduled producer at all, so one absence is a waiting field and the other is not a field.
<<<END RECORD3

<<<BEGIN SLIP3

2026-08-29 · F040 R2 · The reviewer's DECISION F040 D3 paragraph states "THIS IS THE THIRD FEATURE FILE CARRYING THAT TYPO" from two precedent mentions it had grepped rather than from a count of the files; the round's own G5 sweep measured thirteen others still carrying it, so F040 was the fourteenth, and the numeral is the recollection §3 item 16 forbids standing beside a measurement.

2026-08-29 · F040 R2 · The reviewer's SPEC for C7 ordered "APPEND a new test class" and in the same paragraph "follow its fixture and naming conventions" over `tests/orchestration/test_decision_inbox.py`, which holds twenty module-level functions and no class at all, so the two halves of one instruction could not both be obeyed and the worker had to choose and declare.

2026-08-29 · F040 R2 · The reviewer's G4 required `.agent/prose_slips.md` to grow by exactly one line, which FORBADE the blank separator every other entry in that file carries, so the F040 R1 entry landed without one; the landed line is not rewritten and this round's append restores the convention going forward.
<<<END SLIP3

## SPEC for C4 — `packages/orchestration/job_digest.py`

WRITE THIS from the specification. Read `packages/orchestration/decision_inbox.py`
first: it is the closest sibling in size, purpose and style — a pure composition
with a version constant, a `Public API::` docstring block and WHY comments — and
this module should read like it.

**The public surface.** A version constant `JOB_DIGEST_VERSION = 1` and one
function:

    def build_job_digest(job: Any, events: list[dict[str, Any]] | None = None) -> dict[str, Any]:

`events` defaults to None and is passed through to the inbox read path; a caller
that already loaded them does not load them twice.

**The envelope**, exactly these top-level keys and no others:

    {
      "version": JOB_DIGEST_VERSION,
      "job_id": <str>,
      "state": <str>,
      "headline": <str>,
      "cost": {"value": <str>, "basis": <str>},
      "ownership": [],
      "decisions": {"open_count": <int>, "peak_urgency": <int>},
      "primary_action": {"label": <str>, "rule_id": <str>},
    }

**Where each value comes from — these are the one-source obligations.**

- `job_id`, `state`: from `build_report_sources(job)`
  (`packages/orchestration/run_report.py:967`). Use `build_report_sources`, NOT
  `collect_report_sources` — only the former merges `_evidence_sources`, and
  only it fills `open_decision_count` and `blocked`, which are the fields rules
  1 and 3 of the next-action table branch on. A digest built on
  `collect_report_sources` could never recommend answering a decision.
- `primary_action`: `recommended_next_action(sources)`
  (`packages/orchestration/run_report.py:383`) called on that SAME sources
  object. `label` is its `.action` and `rule_id` is its `.rule_id`, both taken
  from the returned `NextAction` and NEITHER re-derived. THIS IS THE FEATURE'S
  CENTRAL ONE-SOURCE PROPERTY: the digest's CTA and the report's recommendation
  must be incapable of disagreeing, and they are only incapable of it if this
  module never decides anything itself. Do not add a rule, do not reorder, do
  not special-case a state.
- `headline`: ONE plain sentence naming the job's state and its terminal status
  when it has one. Compose it here from the sources; it is the digest's own
  prose, not the report's. Absent values render honestly — the report's own
  convention is `not recorded`, never a zero and never a guess.
- `cost.value`: the rendered figure. `cost.basis`: the EXACTNESS vocabulary per
  DECISION F040 D4 — `actual`, `lower_bound` or `absent`, and NEVER a member of
  `BudgetCounters.actual_sources`, which is provenance. Derive BOTH from a
  `BudgetCounters` object obtained the same way `_evidence_sources` obtains it,
  at `packages/orchestration/run_report.py:829-845`: `load_job_plan`, then
  `counters_from_persisted(decode_persisted_budget_actuals(...))`. Take the
  value from `counters.cost_description()` so the digest never re-derives a
  number, and map the basis by the rule D4 fixes: `measured_cost_usd is None`
  gives `absent`, `unpriced_call_count > 0` gives `lower_bound`, otherwise
  `actual`. When there are no actuals at all the value is the report's own
  `not-measured` spelling and the basis is `absent`. YES, this reads the
  persisted actuals a second time, after `build_report_sources` already read
  them; that is deliberate and a WHY comment says so, because `ReportSources`
  carries only the RENDERED `token_description` and the PROVENANCE tuple and
  keeps no `measured_cost_usd`, so the exactness basis is not recoverable from
  it without parsing a rendered string.
- `ownership`: the empty list, always, per DECISION F040 D3 — F035 is unbuilt
  and there is no source. A WHY comment names D3 and F035 so the next reader
  does not read the empty list as a bug.
- `decisions.open_count`: `sources.open_decision_count`, or 0 when it is None.
- `decisions.peak_urgency`: the MAXIMUM of `decision_urgency(card)`
  (`packages/orchestration/decision_inbox.py`) over the OPEN cards of
  `build_decision_inbox(job, events)`, and 0 when there are none. Import the
  function; do not restate the arithmetic — DECISION F040 D2 made that module
  its single home for exactly this call site.

**Totality.** No input makes `build_job_digest` raise. Every seam it reads is
already guarded or is wrapped here with a narrow, documented `except` in the
style of `_evidence_sources` — never a bare `except: pass`, which a repo-wide
guard forbids. A job with no plan, no actuals, no tasks and no decisions
produces a complete envelope whose values say so.

## SPEC for C5 — `tests/orchestration/test_job_digest.py`

Read `tests/orchestration/test_run_report.py` first for the fixture conventions
this package uses for a fake job.

The feature file names FOUR state shapes and each gets its own fixture and its
own assertions: **green** (every task completed, nothing open), **blocked with
decisions** (at least two open decisions with different ages and blocked sizes),
**budget-stopped** (a terminal status in the budget family) and **mid-run**.

Cover, at least:

- the envelope's key set is exactly the eight specified keys, for every one of
  the four shapes — a test that reads the key set rather than individual keys,
  so a field added without a version bump reddens here;
- `version` is `JOB_DIGEST_VERSION`;
- THE ONE-SOURCE PROPERTY, asserted directly and for every shape: the digest's
  `primary_action.label` and `.rule_id` equal
  `recommended_next_action(build_report_sources(job))`'s `.action` and
  `.rule_id` for the SAME job. Assert it against the function's real return
  value, never against a hard-coded string — a golden would pass while the two
  drifted, which is the whole failure this feature exists to prevent;
- the blocked-with-decisions shape recommends the `open-decision` rule, which is
  the branch `collect_report_sources` alone could not reach;
- `peak_urgency` is the maximum over the open cards and agrees with
  `decision_urgency` applied to the peak card by hand;
- `peak_urgency` is 0 and `open_count` is 0 for the green shape;
- `ownership` is `[]` for all four, with the test naming DECISION F040 D3 so a
  later reader knows it is a decision and not an oversight;
- `cost.basis` is `absent` when no actuals are persisted, `lower_bound` when
  unpriced calls exist, and `actual` otherwise — three tests, and the value
  string is the one `cost_description()` produced, not a re-rendered figure;
- TOTALITY: a job object missing plan, actuals, tasks and decisions still
  returns the full envelope and does not raise.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C6, which writes the handback.

G1 TRANSPORT, at C0b. One sha256 over three files — `.remedy-wt/f040-r3-block.md`,
   the committed `.agent/authored/f040-r3.md` and `.agent/last_block.md` —
   reported with the byte length, all three EQUAL. This block states no expected
   digest; the reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN3 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length yourself; the
   reviewer read 1655733 at `8e013dc5`. Base + one separator newline + RECORD3
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION against
   the entire committed file; (b) PARAGRAPH ORDER — the last N blank-line units
   equal RECORD3's N paragraphs IN ORDER, N COUNTED by your script. NEGATIVE
   CONTROL in a disposable worktree: flip one byte inside the FIRST appended
   paragraph and report that BOTH readings reject it and accept the unflipped
   bytes.

G4 THE LEDGER AND THE SLIPS, at C2 and C3. Distinct `^- R-\d+ — ` ids before and
   after with ADDED exactly `['R-0752']`; ADDED resolved `[]`; distinct
   `^DECISION F040 D\d+ — ` with ADDED exactly `['D5']`; exactly one
   `^Gate: F040 R2 — ` line; `^Done: R-0570` and `^Done: R-0752` both 0. For
   `.agent/prose_slips.md`: SLIP3 is appended with NO separator newline of its
   own — it opens with a blank line by construction — so assert the committed
   file equals the pre-commit bytes followed EXACTLY by SLIP3, and report the
   line count before and after.

G5 THE MODULE, at C4. `ruff check packages/orchestration/job_digest.py`;
   `python3 -m compileall -q packages/orchestration/job_digest.py`; and a script
   that imports the module and reports: `JOB_DIGEST_VERSION`, the envelope's
   top-level key set for a minimal fake job, and that the key set is exactly the
   eight the SPEC names. PURITY, measured rather than asserted: report the
   result of `grep -n "open(\|Path(\|subprocess\|socket\|requests\|urllib"` over
   the new module, and justify in the handback any hit that is not an import of
   a named seam. Report that `packages/orchestration/ui_server.py` is NOT in
   this round's path set.

G6 THE TESTS AND THE RED PROOF, at C5. First
   `python3 -m pytest tests/orchestration/test_job_digest.py -q` — REAL exit 0
   with the passed count. Then, INSIDE A DISPOSABLE WORKTREE at C5: report the
   UNMUTATED control's exit code over that file FIRST — it must be 0 — then make
   ONE mutation, replacing the call to `recommended_next_action` in
   `<worktree>/packages/orchestration/job_digest.py` with a hard-coded
   `NextAction(rule_id="all-green", action="Nothing to do.")`, and report the
   exit code and failing count. That mutation breaks the one-source property and
   NOTHING ELSE, so it is the proof that the property is actually pinned rather
   than merely described. Name the worktree path, remove it, and report that
   `git worktree list` no longer holds it.

G7 THE SUITES AND THE TREE, at C5. Each its own REAL exit code:
   `python3 -m pytest tests/orchestration/test_run_report.py -q`,
   `python3 -m pytest tests/orchestration/test_decision_inbox.py -q`,
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured 81, 43, 508, 16, 21 and 42 at the base. Then
   `git status --porcelain` EMPTY, `git ls-files --others --exclude-standard`
   count 0, and the per-commit insertion counts for C0a through C5, every one
   under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state
block, the `## Commits` table with a `+/-` column taken from
`git diff --numstat` and never from file line counts, the deviations, the
item-status table with every bundle item and every gate appearing exactly once,
and the next steps. State `SESSION 1` of F040 and round 3. No length cap. Name
R-0570 and R-0752 as OPEN and routed off this branch, and R-0751 as fixed at
round 2.
