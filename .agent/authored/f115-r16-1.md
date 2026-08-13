── STEP T003b/4 — F115 Prompt breakdown & cost report · Round 16 ─────────────
Goal:        The report gains its second half: what the equal-length period
             immediately before this one cost, and — where that window holds
             nothing, or cannot be computed at all — a stated reason instead
             of a column of zeros.

Bundle:      This is the ONLY ordering statement in this block. Every later
             clause defers to it and none of them restates an order.
  C1  Findings first. Append the two authored paragraphs of SLICE A to
      `.agent/live_review.md`. OWN commit, and the FIRST commit of the round.
  C2  Save this whole block verbatim to `.agent/authored/f115-r16-1.md`.
  C3  Mirror the same bytes into `.agent/last_block.md`.
  C4  `packages/orchestration/token_ledger.py` — `PriorReportPeriod` and
      `prior_report_period`, plus tests.
  C5  `packages/orchestration/cost_report.py` — the comparison section in both
      renderings, the extended `_same_question` guard, the version bump, the
      two golden files moved in THIS SAME commit, plus tests.
  C6  Append the authored DECISION F115 D6 of SLICE B to `.agent/decisions.md`.
  C7  Replace `.agent/plan.md` with SLICE C, then rewrite `.agent/handoff.md`.

Change:
  C4 — packages/orchestration/token_ledger.py, beside `query_cost`
    * A frozen dataclass `PriorReportPeriod` with exactly these fields:
      `since: str | None = None`, `until: str | None = None`,
      `unavailable_reason: str | None = None`, and a property `available`
      returning True when `since` and `until` are both set. The invariant —
      either the pair is set or the reason is — is what makes "no comparison
      data" a statement rather than a silence, so give the class a docstring
      that says it and a `__post_init__` that raises if both or neither side
      is populated.
    * `prior_report_period(since: str | None, until: str | None)
      -> PriorReportPeriod`. It computes the equal-length window immediately
      before `[since, until)` and returns it, or returns the reason it cannot.
      Pure: no ledger, no clock, no I/O.
    * THE ARITHMETIC, exactly:
      - Both ends are parsed with
        `datetime.fromisoformat(text.replace("Z", "+00:00"))`.
      - `d = parsed_until - parsed_since`. The prior window is
        `[parsed_since - d, since)`.
      - The prior window's `until` is THE ORIGINAL `since` STRING, byte for
        byte — never a re-serialisation of the parsed value. The two windows
        must abut under the SAME lexicographic `ts_utc` comparison
        `_cost_filters` performs, and reformatting one side would break that
        by formatting luck alone. Write the one-line WHY above it.
      - The prior window's `since` is `(parsed_since - d).isoformat()`, which
        reproduces the awareness of the input it was derived from.
    * THE FOUR UNAVAILABLE CASES, each with its own distinct reason sentence,
      and none of them raising:
      - either `since` or `until` is absent — an open-ended period has no
        length, so no prior window can be placed;
      - either string fails `fromisoformat` — nothing is guessed;
      - one end is offset-naive and the other offset-aware, so subtracting
        them is a `TypeError` — report it, never invent an offset;
      - `until <= since`, so the period is empty or inverted and its prior
        window would be too.
    * Add the new names to the module docstring's `Public API::` list, in the
      shape the other entries already use.
    * Tests, in `tests/orchestration/test_token_ledger.py`, in their own class:
      the happy path over both a bare-date pair and an offset-aware pair;
      the byte-for-byte reuse of the original `since` string as the prior's
      `until`; each of the four unavailable cases reaching its own reason;
      and the partition property — `query_cost` over the prior window plus
      `query_cost` over the current window equals `query_cost` over
      `[prior.since, until)`, on the existing `cost_ledger` fixture.

  C5 — packages/orchestration/cost_report.py
    * Both renderers take two new keyword-only parameters, after `label`:
      `prior: CostReport | None = None` and
      `no_comparison_reason: str | None = None`.
    * `_same_question` gains a THIRD guard, for the prior report, and it only
      fires when `prior` is not None: the prior must be the prior of THIS
      period — `prior.until == cost.since` — and it must come from the same
      ledger — `(prior.ledger_path, prior.ledger_exists)` equal to the
      current report's. A mismatched prior published as a comparison is the
      same defect the first two guards already refuse, so refuse it the same
      way, with a message naming both sides. Extend the docstring by one
      short paragraph.
    * A new markdown section `## Compared to the previous period`, rendered
      after the segment section. When a `prior` is given: a four-column table
      `figure | this period | previous | change` with one row per entry of
      `COST_FIGURE_COLUMNS` plus a `calls` row, values rendered by the
      existing `_figure`. The change cell is the SIGNED difference, with an
      explicit `+` on a positive; when EITHER side is None the change cell is
      `COST_UNMEASURED_LABEL` and no arithmetic is attempted. When no `prior`
      is given: the `no_comparison_reason` sentence, or a default sentence
      when the caller named none, and NO table.
    * A prior period that exists but holds ZERO calls is not a comparison. It
      renders the "no comparison data" shape with its own sentence naming that
      the window was read and was empty — the P6 distinction between "we did
      not look" and "we looked and there was nothing".
    * Remedy deliberately does NOT print a percentage change here. Say so in
      the module docstring, in the "Remedy deliberately does not" shape it
      already uses, with the reason: a prior figure of 0 has no denominator
      and a percentage of an unmeasured figure is not a measurement.
    * `cost_report_json` gains a `"comparison"` key holding `"available"`
      (bool), `"reason"` (the sentence, or `""` when available),
      `"prior"` (null, or an object with `"since"`, `"until"` and a
      `_cost_row_payload` of the prior total) and `"deltas"` (an object keyed
      by the `COST_FIGURE_COLUMNS` names plus `"calls"`, each value the signed
      difference or null where either side is unmeasured).
    * `COST_REPORT_VERSION` becomes 3.
    * BOTH golden files move in THIS commit, hand-edited, NEVER regenerated by
      a test. The golden pair is rendered with no `since` and no `until`, so
      it exercises the FIRST unavailable case; render it with the
      `no_comparison_reason` that `prior_report_period` produces for that case
      so the golden pins the real sentence and not a hand-written paraphrase.
    * Tests, in `tests/orchestration/test_cost_report.py`: a comparison
      renders in both formats; a change cell is `unmeasured` when either side
      is None and never a number; an empty prior window renders the
      "we looked and there was nothing" shape rather than a table of zeros;
      a prior whose `until` is not this report's `since` is REFUSED by both
      renderers; a prior from a different ledger is refused too.

Constraints:
  * AGENTS.md is the highest authority; nothing here weakens it.
  * Every commit is pushed before the next one begins (finding R-0289).
  * Each commit stays under the 500-insertion cap (AGENTS.md counting rule:
    the `+` column only). C4 and C5 are each likely to be large — if either
    approaches the cap, split it and say so in the handback rather than
    landing an oversize commit.
  * Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string.
  * Do NOT touch: the CLI, `apps/cli/command_catalog.py`, `stats_ledger_cmd.py`,
    `docs/`, `docs/roadmap/`, pricing, calibration. Those are later rounds.
    No "while I'm here" edits.
  * The three authored slices are applied BYTE FOR BYTE. You may not reword,
    rewrap, retitle or trim them. If a slice cannot be applied as given, apply
    nothing, and report the exact obstacle in the handback.
  * SLICE A appends to the end of `.agent/live_review.md`. SLICE B appends to
    the end of `.agent/decisions.md`. SLICE C fully replaces `.agent/plan.md`.
  * Destructive verification — gate (i) — runs ONLY inside a disposable
    `git worktree` under the gitignored `.remedy-wt/`, never in the primary
    checkout. Remove and prune it before the handback.
  * `git status --porcelain` is empty at handback.

Done when: every value below is REAL and recorded in the handback with the
command that produced it. "Green" as a word is not a result.
  (a) `.agent/authored/f115-r16-1.md` and `.agent/last_block.md` are byte
      identical. Report the method used, the sha256 of BOTH, and
      `wc -lc .agent/last_block.md`.
  (b) Scoped to the ADDED lines of C1's own commit:
      `git show <C1> -- .agent/live_review.md` shows `^+Done: R-0335` exactly
      once and `^+- R-0336` exactly once, and `git show --numstat <C1>`
      reports ZERO deleted lines. Whole-file after C1: `^Done:` 9, `^- R-0`
      17, `^## Steps` 1, `^Landed:` 0.
  (c) `git log --oneline 6752841a..HEAD` lists C1 LAST, i.e. it is the oldest
      commit of the round.
  (d) THE GOLDENS MOVED ONLY WHERE THIS ROUND ADDS A SURFACE. Do NOT predict
      or target a line count — report the real `git show --numstat <C5> --`
      pair for both golden files, and separately PROVE that no DATA moved:
      load the old and new `cost_report.json` with python and assert that the
      `buckets`, `segments`, `total`, `label`, `filters` and `ledger_exists`
      values are EQUAL, so the only differences are the new `comparison` key
      and the `report_version` bump. Print the python comparison's real
      output. For the markdown, print the full `git diff` of the file and
      confirm by eye that every changed line belongs to the new section.
      If any figure, bucket or segment row moved, STOP and report it — that
      is a renderer regression, not a golden to re-bless.
  (e) `python3 -m ruff check packages/orchestration/token_ledger.py
      packages/orchestration/cost_report.py
      tests/orchestration/test_token_ledger.py
      tests/orchestration/test_cost_report.py` prints `All checks passed!`
      and exits 0.
  (f) `python3 -m pytest tests/orchestration/test_token_ledger.py
      tests/orchestration/test_cost_report.py -q` — the pre-round baseline is
      119, every one of which stays green. Report the real total.
  (g) `python3 -m pytest tests/cli/test_stats_cost.py -q` — baseline 41,
      untouched by this round. Report the real number.
  (h) Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` — baseline
      42. Report the real number.
  (i) Two probes, both inside one disposable worktree under `.remedy-wt/`:
        P1 make `prior_report_period` return the window WITHOUT subtracting —
           i.e. `[since, since)` — run the C4 and C5 test files, and report
           the NAMES of every test that fails.
        P2 restore that, then make the change cell fall back to `0` instead of
           `COST_UNMEASURED_LABEL` when a side is None, re-run, and report the
           NAMES of every test that fails.
      Report NAMES, not counts, and do not predict either. Then remove and
      prune the worktree and show that `git worktree list` is back to one line.
  (j) `wc -l .agent/plan.md` is under 50.
  (k) `git status --porcelain` is empty, and
      `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
      is `0  0` after the last push.
  (l) `git diff --name-only 0d6c97aa..HEAD` contains no path matching
      `remedy-wt`.

═══ SLICE A — APPEND to .agent/live_review.md ═══════════════════════════════

Done: R-0335 — RESOLVED at the R15 gate, and resolved in the only way it could be: the R14 verdict it said was missing from disk now IS on disk, written by R15's findings-first commit `f77554bf` and re-measured rather than copied out of the handoff. The R15 round as a whole is PASS. The reviewer re-ran every gate itself: `cmp .agent/authored/f115-r15-1.md .agent/last_block.md` exit 0 — the reviewer's sandbox allows `cmp` even though the worker's refused it, so the worker's sha256-plus-byte-compare substitute was corroborated by the primary proof rather than merely accepted — with sha256 `e3a1ea5706f77fccdb2953ab1db9c35a32cf493c598a6981cb4bc02d05d5d39b` over both copies, `wc -lc` 251 18389, the live-review counts 8 / 16 / 1 / 0, `git show --numstat f77554bf` 4 insertions and ZERO deletions, C1 the oldest commit of `5c7f5159..HEAD`, ruff `All checks passed!` over all four files, 119 passed against a 119 baseline of 114 plus five new tests, 83 passed over the canary and the untouched CLI cost tests, `wc -l .agent/plan.md` 43, an empty porcelain, 0 0 against origin, and 38 changed paths with no `remedy-wt` among them. The three authored slices were compared DISK TO DISK against the committed `.agent/authored/f115-r15-1.md` rather than against a reviewer retype — 43 of 43 plan lines, 39 decision lines, 3 live-review lines, all byte-identical — which is the R-0147 class this project has paid for before. Both declared deviations are ACCEPTED: refreshing the two `Public API::` signature lines and the test-module docstring was right, because leaving them would have left a false claim on disk beside a changed signature, and the gate (d) json number was the reviewer's error and not the worker's, registered below. A THIRD probe of the reviewer's own choosing, which the block did not order, settled the question the ordered probes could not: deleting the `until` clause only proves the filter is WIRED, while flipping `ts_utc < ?` to `ts_utc <= ?` proves it is HALF-OPEN, which is the whole content of DECISION F115 D5. That mutation fails exactly `test_a_call_at_exactly_until_is_out_while_one_at_exactly_since_is_in`, `test_the_merge_carries_the_period_end_of_its_inputs` and `test_until_narrows_the_shares_exactly_as_it_narrows_the_cost` and nothing else, so the three new tests bind the boundary reading and not merely the presence of a parameter. The probe ran in a disposable worktree under `.remedy-wt/`, which was removed and pruned; `git worktree list` shows one line.

- R-0336 — Low — reviewer gate arithmetic, tenth of its class, self-registered. R15's gate (d) predicted that the golden `cost_report.json` would move by `2 1`: one changed `report_version` line plus one added `"until"` line. The real diff is `3 2`. The prediction is not merely off, it is arithmetically unreachable, and the reason is a fact about the format rather than about the change: `json.dumps(sort_keys=True)` placed the new `"until"` key AFTER `"timezone"`, which is the last key of the `filters` object, so the `"timezone": "UTC"` line had to gain a trailing comma. Git counts that as one deletion plus one addition on top of the added line. The worker was right, did not stop the round on it, said plainly that the prediction forgot the comma, and proved by reading the diff that no figure, bucket or segment row had moved — which is exactly the judgement gate (d)'s STOP clause exists to invite rather than to suppress. What makes this its own id rather than a tally mark under R-0327 is that it is a NEW subclass. The standing pre-emission checklist's item 8 sends the reviewer to the code that PRODUCES a gated value, and the reviewer did go there: `sort_keys=True` was read, and the alphabetical position of `until` after `timezone` was derived correctly. What went unread is the SERIALISER'S PUNCTUATION — that a key appended after the last one perturbs the line before it. Item 8 covers the value; nothing covers the FORMAT the value is embedded in. The counter-measure is already applied in the next block rather than deferred: R16's gate (d) orders NO line-count prediction at all and replaces it with a structural proof — load both goldens and assert that every DATA key is equal, so the gate constrains what actually matters (that no figure moved) instead of a line count the reviewer keeps mis-deriving. That is the general repair for this family: when a gate's value depends on a formatter, gate the SEMANTICS and report the arithmetic, never predict the arithmetic. Tenth of the reviewer-arithmetic and self-contradiction family after R-0282, R-0321, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333, R-0334 and R-0335. No source fix. OPEN.

═══ SLICE B — APPEND to .agent/decisions.md ═════════════════════════════════

## DECISION F115 D6 — the prior period reuses the current period's `since` STRING (2026-08-13)

The prior-period comparison needs the equal-length window immediately before
`[since, until)`. The arithmetic is obvious; the SERIALISATION is not, and it
is where this would have gone wrong.

The prior window is `[parsed_since - d, since)` where `d = until - since`. Its
opening bound is computed and must be serialised. Its CLOSING bound is not
computed at all: it is the ORIGINAL `since` string, byte for byte, passed
through untouched.

Why that matters. `_cost_filters` compares `ts_utc` LEXICOGRAPHICALLY — that is
the whole reason `ts_utc` is TEXT rather than an epoch number, and `query_cost`
says so in its own docstring. Two windows abut correctly only if the boundary
they share is the SAME STRING on both sides. Round-tripping it through
`fromisoformat` and `.isoformat()` does not guarantee that: `"2026-08-01"`
comes back as `"2026-08-01T00:00:00"`, and `"...+00:00"` and `"...Z"` are the
same instant in two spellings. Every one of those round-trips still happens to
order correctly against a well-formed `ts_utc`, which is precisely the danger —
it would work by formatting luck, and the first ledger written in a different
ISO-8601 shape would silently double-count or drop the boundary call. Passing
the original bytes through makes the partition property of DECISION F115 D5
hold by construction instead.

Four cases yield no prior window at all, and each states its own reason rather
than returning a bare None: an open-ended period has no length to mirror; an
unparseable end is never guessed at; a naive end paired with an aware one is a
`TypeError` from `datetime`, and inventing an offset to avoid it would be
fabricating the user's timezone; and a period whose end is at or before its
start has an empty or inverted prior window. A fifth case is not an error but
still not a comparison: a prior window that EXISTS and holds zero calls. It is
reported as "read, and empty", which is the P6 distinction between not having
looked and having looked and found nothing.

Alternatives considered. (a) Return `None` for every unavailable case —
rejected because the report must print WHY there is no comparison, and a bare
None cannot say. (b) Normalise both ends to a canonical UTC spelling before
comparing — rejected as a larger change with a wider blast radius: it would
alter how `since` itself filters, which is pinned by existing tests and by both
goldens, for a benefit this feature does not need.

Reverse by deleting `PriorReportPeriod` and `prior_report_period` and dropping
the two comparison parameters from the renderers. Nothing else reads them: the
CLI that will call them is a later round.

═══ SLICE C — FULL REPLACEMENT of .agent/plan.md ════════════════════════════

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 6752841a (R15 PASS). Next free finding
ID: R-0337. Open findings: 10 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0331, R-0333, R-0334, R-0336. R-0335 was RESOLVED at the R15
gate. No PR exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003 is half built. The period has two ends and the comparison now has
its arithmetic: `prior_report_period` places the equal-length window
before `[since, until)`, reusing the current `since` STRING as the prior's
exclusive end so the two windows abut under the same lexicographic
compare (DECISION F115 D6). Four cases yield no window and each states
its reason; a window that exists but is empty says so rather than
rendering zeros. Both renderers print the comparison, `_same_question`
refuses a prior that is not this period's prior, and
`COST_REPORT_VERSION` is 3. No CLI is wired.

## Next Steps
1. T003c — the `remedy stats report` CLI, markdown and `--json`, with its
   catalog entry, `--since`/`--until` validation and the second query the
   comparison needs; `stats_ledger_cmd.UNMEASURED` becomes an import of
   `COST_UNMEASURED_LABEL` so the concept keeps one spelling.
2. T003d — the docs page the new user-visible behaviour needs.
3. Integration gate (docs/agents/integration_gate.md).
4. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit.

Fortschritt: 88 % (T001 ✅ · T002 ✅ · T003 halb) — Schätzung

═════════════════════════════════════════════════════════════════════════════

Handback:    A completion report plus a rewritten `.agent/handoff.md`. The
             handoff carries: feature and round, branch, the per-commit table,
             the changed-files table, the item-status table covering C1..C7
             with `done`/`skipped`/`deviated` and a reason for anything not
             `done`, every gate value (a)..(l) as a real measured value, the
             open-findings count, and the next expected action. It repeats the
             Fortschritt line of SLICE C verbatim. Cap is 60 lines; exceed it
             only with a DECISION D15 "Deviations, declared" line naming the
             real line count and the mandated content that caused the overage.
             Never drop a section to meet the cap.
─────────────────────────────────────────────────────────────────────────────
