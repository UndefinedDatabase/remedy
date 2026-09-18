
## DECISION F269 D1 (2026-09-18, reviewer, round 3) — the contract template format, its proposal and `--contract`
CONTEXT: T2_F269.md reserves this number for the template format ("`docs/contracts/<name>.md`,
human-readable, compiled to criteria") and names four templates, one fixture order each, a planner
proposal and `--contract <name>`. Measured at `b487e3f7`: `docs/contracts/` does not exist;
`remedy do --contract` exits 2 through `_DO_FLAGS_NOT_YET_AVAILABLE` in `apps/cli/commands/do_cmd.py`;
`do_sequence._step_plan` creates the mission and sets its order before `plan_mission`, and
`write_planner_criteria` keeps every non-planner criterion; the wheel ships `packages` and `apps`
only, so no file under `docs/` reaches an installed wheel; no `do` job stores a DoD or runs a gate.
CHOSEN: (1) FORMAT. A template is `docs/contracts/<name>.md`, and its first line is exactly
`# Contract template — <name>`, where `<name>` is the file stem. It has three `## ` sections, which
the loader reads by their exact headings: `## Proposed when the order mentions` — one bullet per
phrase, lowercase; `## Criteria` — one bullet per criterion, `- blocking: <text>` or
`- advisory: <text>`, optionally followed by one line indented two spaces, `check: <JSON object>`,
which must validate as an F061 `DraftCheck` apart from its id and is used as that criterion's
check instead of the compiled one; `## Fixture order` — one paragraph, the order the template's
tests plan. Any other non-blank line under those sections is refused with the file and line named.
Prose before the first section is free. (2) COMPILE. A template compiles to criteria with origin `template`, whole-mission
scope, ids `C001` upward in file order, and each check either from its `check:` line (id
`ctr-<criterion id>`, refs [`<criterion id>:0`], the criterion's `blocking`) or from DECISION F269
D4 (1)'s compiler. (3) PROPOSAL. The proposal is deterministic: each template scores the number of its
phrases that occur in the order, case-insensitive, where an occurrence counts only when the
characters on either side of it are neither word characters nor hyphens; the single top scorer
is proposed, and a top score of zero, or a tie at the top, proposes nothing. (4) `do`. `remedy do --contract <name>`
forces a template, and a name that is not a template exits 2 naming the templates before any step
runs; without the flag the proposal applies when there is one. The chosen template is written onto
the new mission before `plan_mission`, so the planner's criteria are added after it and none of its
criteria are dropped (DECISION amend0911-feedback D5), and the plan step's detail says whether it
was forced or proposed. (5) The templates are read from the source tree. The hygiene criteria
T2_F269.md puts in every template land in the next round, with a check that measures them. Until
then no template carries them, because F061's compiler would judge them by the test suite alone,
and that is a live indicator that does not measure the claim.
ALTERNATIVES: a YAML or JSON template, rejected because the feature file asks for human-readable
Markdown; a proposal by a model call, rejected because it changes the mission-plan draft schema or
adds a structured call for one word, and the deterministic match is testable; shipping the
templates in the wheel, rejected here because distribution is F215's and nothing installs Remedy
from a wheel today. REVERSE: delete `docs/contracts/`, the loader and its tests, restore the
`--contract` refusal row, and delete this paragraph.
