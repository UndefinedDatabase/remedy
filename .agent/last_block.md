── STEP T003d/4 — F115 Prompt breakdown & cost report · Round 18 ─────────────
Goal:        Give the new user-visible behaviour its docs page. `remedy stats
             report` gets one guide that explains how to read every number it
             prints, states the two breakdowns it deliberately does NOT have,
             and is registered in the `docs/README.md` index in this same PR.

Round type:  SPLIT in shape and delegated by construction
             (docs/agents/self_drive_protocol.md): the change set is docs/ and
             .agent/ only, but the reviewer writes nothing in the work tree, so
             a worker still makes every commit and the reviewer still gates.

Findings:    There is NO findings-first commit this round, and that is not an
             omission. §4 item 4 of docs/agents/planner_reviewer_prompt.md puts
             the previous round's authored findings text in the round's FIRST
             commit; R17's gate entry `Done: R-0337` is ALREADY on disk, applied
             at commit `0fa1e40a`, and this round registers no new finding. So
             `.agent/live_review.md` is NOT a path of this round's change set,
             and gate (h) checks that it stayed out.

Bundle:      This is the ONLY ordering statement in this block. Every later
             clause defers to it and none of them restates an order.
  C1  Save this whole block verbatim to `.agent/authored/f115-r18-1.md`.
  C2  Mirror the same bytes into `.agent/last_block.md`.
  C3  NEW FILE `docs/guides/cost-report-user-guide-v0.md`, from SLICE A,
      applied verbatim.
  C4  `docs/README.md` — the two index rows of SLICE B.
  C5  Replace `.agent/plan.md` with SLICE C, then rewrite `.agent/handoff.md`.

Change:
  C3 — docs/guides/cost-report-user-guide-v0.md
    * A NEW file whose bytes are SLICE A exactly. You are not the author of
      this text: apply it, do not improve it, do not rewrap it. If any claim in
      it is FALSE against the code, do NOT silently correct it — stop, commit
      nothing further, and report the false claim with the source line that
      contradicts it. A reviewer error is cheaper than a doc that disagrees
      with itself.
    * The fenced `text` block inside SLICE A is a verbatim copy of
      `tests/orchestration/fixtures/cost_report/golden/cost_report.md`. Gate (c)
      proves that by extraction and diff, so a single changed character there
      is a red gate, not a nit.
  C4 — docs/README.md
    * Two rows, each an APPEND-shaped insertion after an existing line. Both
      pairs are in SLICE B with their FROM anchors. Nothing else in that file
      changes: no reordering, no reflow, no other row touched.
  C5 — .agent/plan.md and .agent/handoff.md
    * `.agent/plan.md` is REPLACED by SLICE C, byte for byte.
    * `.agent/handoff.md` is rewritten per the Handback clause below.

Constraints:
  * Nothing outside these five paths changes:
      .agent/authored/f115-r18-1.md
      .agent/last_block.md
      docs/guides/cost-report-user-guide-v0.md
      docs/README.md
      .agent/plan.md
      .agent/handoff.md
    (six paths across five commits; C5 touches two).
  * This round adds no code and no test. If you believe a test is needed to
    pin a doc claim, say so in the handback — do not add one.
  * Push after EVERY commit, not once at the end (finding R-0289).
  * Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string (AGENTS.md, Commit Discipline).
  * `.remedy-wt/` holds other sessions' scratch: create only your own
    directory, delete only your own, remove and prune before the handback.
  * `git status --porcelain` is empty at handback.

Done when: every value below is REAL and recorded in the handback with the
command that produced it. Do NOT predict or target any count — where a baseline
is named, MEASURE it before your first commit, report it, then report the value
after.
  (a) `.agent/authored/f115-r18-1.md` and `.agent/last_block.md` are byte
      identical. Report the method (`cmp`, or sha256 over both plus a byte
      compare if `cmp` is refused), the sha256 of BOTH, and
      `wc -lc .agent/last_block.md`.
  (b) `test -f docs/guides/cost-report-user-guide-v0.md` succeeds, and
      `wc -l docs/guides/cost-report-user-guide-v0.md` — report the value. No
      value is predicted for it.
  (c) THE EXAMPLE IS THE GOLDEN, not a retype. Run exactly:
        diff <(awk '/^```text$/{f=1;next} /^```$/{f=0} f' docs/guides/cost-report-user-guide-v0.md) tests/orchestration/fixtures/cost_report/golden/cost_report.md
      Report the exit code and any output. Exit 0 with no output is the only
      passing result.
  (d) THE FLAGS THE GUIDE NAMES ARE THE FLAGS THE CATALOG HAS. Run:
        python3 -c "from apps.cli.command_catalog import COMMAND_CATALOG as C; e=[x for x in C if x.command_id=='stats.report'][0]; print([a.name for a in e.args])"
      If the catalog's export is named differently, find the real name with
      `grep -n "^COMMAND\|^_COMMAND\|def .*catalog" apps/cli/command_catalog.py`
      and say which name you used. Report the printed list verbatim. Then
      confirm, by reading SLICE A against that list, that the guide names no
      flag absent from it and that `--all-projects` is absent from both.
  (e) THE JSON KEYS THE GUIDE LISTS ARE THE REAL ONES. Run:
        python3 -c "import json;d=json.load(open('tests/orchestration/fixtures/cost_report/golden/cost_report.json'));print(sorted(d));print(d['report_version'], repr(d['unmeasured_notation']))"
      Report both lines verbatim, then confirm the guide's key list is that
      same set in that same spelling, and that the version and the notation
      word the guide states are the printed ones.
  (f) THE NO-LEDGER SENTENCE IS THE CODE'S OWN. Run:
        grep -c "No ledger on disk for this scope" packages/orchestration/cost_report.py docs/guides/cost-report-user-guide-v0.md
        grep -c "COST_DEFAULT_LABEL = " packages/orchestration/cost_report.py
        grep -n "COST_DEFAULT_LABEL = " packages/orchestration/cost_report.py
      Report the real counts and the default-label value, and confirm the guide
      states that same value.
  (g) REGISTRATION, scoped to C4's own commit. Report:
        git show --numstat <C4> -- docs/README.md
        grep -c "cost-report-user-guide-v0.md" docs/README.md
      The grep counts LINES: two rows, so 2. Both pairs in SLICE B are
      APPEND-shaped (each TO contains its FROM verbatim), so the obligation is
      NOT a whole-file "FROM 0x": among the lines THAT COMMIT'S DIFF ADDS, each
      TO-only line appears exactly once, and each FROM anchor still appears
      exactly once in the whole file. Report both readings
      (`git show <C4> -- docs/README.md | grep -c '^+|'` for the added rows).
  (h) THIS ROUND'S CHANGE SET. Report `git diff --name-only aff20fa3..HEAD`.
      It must list exactly the six paths of the Constraints clause and nothing
      else — in particular NOT `.agent/live_review.md`, for the reason the
      Findings clause gives.
  (i) `python3 -m pytest tests/docs/ -q` — baseline `294 passed`, measured by
      the reviewer at `aff20fa3`. This round changes `docs/README.md`, which
      those tests read. Report the real number.
  (j) Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` — baseline
      `42 passed`. Report the real number.
  (k) `wc -l .agent/plan.md` under 50; `git status --porcelain` empty;
      `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
      is `0  0`; `git diff --name-only 0d6c97aa..HEAD` contains no path
      matching `remedy-wt`.
  (l) `remedy stats report --help` is probably REFUSED by this sandbox. Try it
      once. If it runs, paste the real output and say whether it contradicts
      any line of the guide. If it is refused, report the refusal text and say
      that the guide's flag list rests on gate (d) instead. Do not fabricate
      the binary's output under any circumstances.

═══ SLICE A — NEW FILE .agent -> docs/guides/cost-report-user-guide-v0.md ════

# Cost report — user guide (v0)

`remedy stats report` answers one question about a project: where did the tokens
go, and what did they cost. It reads that project's token ledger and writes
nothing. Every number it prints comes from a ledger row — nothing is
interpolated, and nothing is priced that a provider did not price.

For the estimates Remedy makes BEFORE a task runs, see
[token-economy-user-guide-v0.md](token-economy-user-guide-v0.md). This guide is
about actuals, after the fact.

## The command

```
remedy stats report [--since <ts>] [--until <ts>] [--job <id>]
                    [--by role|model|day] [--label <name>]
                    [--project <id>] [--json]
```

- `--since` / `--until` bound the period as ISO-8601 timestamps (`2026-08-01`,
  or `2026-08-01T12:00:00+00:00`; a trailing `Z` is read as `+00:00`). The
  period is HALF-OPEN: a call at exactly `--since` is IN, a call at exactly
  `--until` is OUT. Two adjacent periods therefore never double-count a call.
- `--job` narrows to one job — in this period AND in the period it is compared
  against, so the comparison stays one question rather than two.
- `--by` groups the cost table by `role`, `model` or `day`. Without it you get
  the grand total only.
- `--label` names the scope in the report's header. The default is
  `(unlabelled)`.
- `--project` picks the project whose ledger is read. Exactly one, and there is
  deliberately NO `--all-projects`: cost folds across projects but the segment
  breakdown does not, so an all-projects report would publish one project's
  breakdown under a multi-project total.
- `--json` prints the same facts as a machine-readable payload.

All timestamps are UTC, and the report says so in its own header.

## What it looks like

This is the report the suite pins against a fixture ledger, copied verbatim
from `tests/orchestration/fixtures/cost_report/golden/cost_report.md`:

```text
# Cost report — f115-golden

Filters: since=-  until=-  job=-  by=day · all timestamps UTC

## Cost

| bucket | calls | tokens in | tokens out | cache read | cache write | cost usd | basis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-08-01 | 1 | 1000 | 200 | unmeasured | unmeasured | unmeasured | 0/1 measured |
| 2026-08-05 | 1 | 1000 | 200 | unmeasured | unmeasured | unmeasured | 0/1 measured |
| 2026-08-09 | 2 | 2000 | 400 | 64 | 32 | 0.2500 | 1/2 measured |
| TOTAL | 4 | 4000 | 800 | 64 | 32 | 0.2500 | 1/4 measured |

PARTLY UNMEASURED: these figures cover only the 1 call(s) whose provider reported them; the 3 unmeasured call(s) contribute nothing to any figure above.
No price is computed: a cost appears only where a provider reported one.

## Where the tokens went

| segment | calls | segments | chars | tokens est. | share |
| --- | --- | --- | --- | --- | --- |
| diff | 1 | 1 | 400 | 100 | 43.5% |
| schema_tail | 1 | 1 | 60 | 100 | 43.5% |
| task_brief | 1 | 1 | 120 | 30 | 13.0% |
| TOTAL | - | 3 | 580 | 230 | 100.0% |

Attribution: 2 call(s) carry a segment manifest, 2 do not. An unattributed call is one whose prompt was never traced; it is counted here and given no share of any segment kind.

## Compared to the previous period

No previous period: this report has no start or no end, and an open-ended period has no length to mirror.
```

## Reading the numbers

Three sections, always in this order.

**`## Cost`** — one row per bucket plus a `TOTAL` row: calls, tokens in and
out, cache read and write, cost in USD, and the row's basis as `N/M measured`.
A figure no provider reported prints the word `unmeasured`, never `0`: a reader
has to be able to tell "nobody reported this" from "it was zero", and in a
column of numbers only a word does that. A total that is only partly measured
says so in its own sentence. No price is ever computed — there is no price
table, so an unpriced call stays unpriced instead of being multiplied into a
plausible figure.

**`## Where the tokens went`** — the input share per prompt-segment kind, taken
from the segment manifest each traced call records. The `Attribution:` line
names how many calls carry a manifest and how many do not. An unattributed call
is one whose prompt was never traced: it is counted, and given no share of any
segment kind, rather than being guessed into a bucket.

**`## Compared to the previous period`** — the equal-length window immediately
before this one, queried under the same `--job` filter. It needs BOTH bounds:
an open-ended period has no length to mirror, and the report prints that reason
instead of a table. A previous window that exists but held no calls gets a
different sentence, because "there was no window to look at" and "we looked and
found nothing" are two different facts about the same empty space. Where there
IS a table, the line under it names the window that was compared against, so
the baseline is never anonymous.

## Two breakdowns this report does not have yet

The roadmap asks for a per-role and a per-task-class breakdown. Remedy
deliberately does not fake either one:

- `--by role` has ONE bucket today, because a task run's `role` is recorded as
  `"builder"` for the whole run. The existing `remedy stats cost` view already
  prints that limit in its own output.
- There is no per-task-class breakdown at all: no ledger row carries a task
  class, so there is nothing to aggregate. The report stays silent rather than
  inventing a bucket.

Both limits belong to their own features. This report shows what exists and
says nothing about what does not.

## When there is no ledger

A project whose ledger was never written is not a project that cost nothing, so
the report refuses to print a table of zeros and says this instead:

```
No ledger on disk for this scope — nothing has been recorded yet. Run 'remedy stats backfill-ledger <evidence-dir>' to mirror existing evidence.
```

`remedy stats backfill-ledger <evidence-dir>` mirrors finalized task runs from
an evidence directory into the ledger. It writes the ledger and never the
evidence, and it is idempotent: the same evidence always yields the same rows.
Run it, then run the report again.

## The json payload

`--json` prints `report_version: 3` and these top-level keys:

`buckets`, `comparison`, `filters`, `label`, `ledger_exists`, `note`,
`report_version`, `segments`, `total`, `unmeasured_notation`

In json an unmeasured figure is `null`, not the word — and
`unmeasured_notation` states that convention inside the payload itself, so a
consumer cannot read a missing measurement as a zero.

═══ SLICE B — TWO APPEND-SHAPED PAIRS in docs/README.md ═════════════════════

PAIR 1 — the Quick-Find table. FROM (exactly one line, appears once):

| context | [context-inspector.md](system/context-inspector.md) | system |

TO (that same line, unchanged, plus one new line after it):

| context | [context-inspector.md](system/context-inspector.md) | system |
| cost report | [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | guide |

PAIR 2 — the Guides table. FROM (exactly one line, appears once):

| [autocoder-usage.md](guides/autocoder-usage.md) | How to use the autocoder |

TO (that same line, unchanged, plus one new line after it):

| [autocoder-usage.md](guides/autocoder-usage.md) | How to use the autocoder |
| [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | Reading `remedy stats report` |

═══ SLICE C — FULL REPLACEMENT of .agent/plan.md ════════════════════════════

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: aff20fa3 (R17 PASS, plus the state-only
close-out commits). Next free finding ID: R-0338. Open findings: 11 —
R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333, R-0334,
R-0336, R-0337. No PR exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003d gave the command its docs page:
`docs/guides/cost-report-user-guide-v0.md` explains the half-open period,
the `unmeasured` word, the attribution line, the prior-period sentence and
the json keys, states that per-role has one bucket and per-task-class has
no source, and is registered in the `docs/README.md` index in this same
PR. Its example report is the T002 golden byte for byte, so the guide
cannot drift from the renderer without a red gate.

## Next Steps
1. Integration gate (docs/agents/integration_gate.md) — the full suite
   with `-n auto`, R-0322's five pre-existing reds expected.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the authored STATUS line committed last, then the PR.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit —
  and now the guide's example too.
- The `remedy` binary is refused in this session's sandbox, so CLI wiring
  is proven through the suite and never through a pasted `--help`.

Fortschritt: 96 % (T001 ✅ · T002 ✅ · T003 ✅ — Integration-Gate + Closure
offen) — Schätzung

═════════════════════════════════════════════════════════════════════════════

Handback:    A completion report plus a rewritten `.agent/handoff.md`, carrying
             feature and round, branch, the per-commit table, the changed-files
             table, the item-status table over C1..C5 with `done`/`skipped`/
             `deviated` and a reason for anything not `done`, every gate value
             (a)..(l) as a real measured value with its baseline where one was
             named, the open-findings count, and the next expected action. It
             repeats the Fortschritt line of SLICE C verbatim. Cap is 60 lines;
             exceed it only with a DECISION D15 "Deviations, declared" line
             naming the real line count and the mandated content that caused
             the overage. Never drop a section to meet the cap.
─────────────────────────────────────────────────────────────────────────────
