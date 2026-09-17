# F281 Round 15 — step block

## Goal

Book round 14's independently-reviewed PASS, then fix `apps/cli/help_renderer.py`'s
`_box()` so long right-column text WRAPS across continuation lines instead of being
truncated with an ellipsis (DECISION F281 D4), clearing the Acceptance line "A
200-character option help renders without `…`." Pre-verified twice in disposable
worktrees (`.remedy-wt/`, removed after use): the fix applied cleanly and
`tests/test_help_renderer.py tests/test_grouped_cli.py -q` read `296 passed`
(293 baseline + 3 new sweep tests, 1 test renamed with no count change); a
mutation red-proof reverting ONLY the `_box()` edit reddened exactly the four
ellipsis-guard tests (19 passed, 4 failed) and no other test, then re-applying
restored `23 passed` in `tests/test_help_renderer.py` alone.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r15.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD14 + DECISION F281 D4 + PLAN15 — one commit.
C2: CODE — 2 edits in `apps/cli/help_renderer.py` (the `textwrap` import and
`_box()`'s wrap logic) and 2 edits in `tests/test_help_renderer.py` (rename
+ rewrite `test_long_content_truncated`, insert `TestNoEllipsisAcrossCatalog`)
— one commit.
C3: HANDBACK.

## C1 — RECORD14 + DECISION F281 D4 + PLAN15

### RECORD14 — append to `.agent/live_review.md`, after its current last
line, separated by exactly one blank line, verbatim:

```
Gate: F281 R14 — the F281 round 14 entry. VERDICT PASS. Written by the planner and reviewer of F281's second session after reading the committed range `a8e42d10`..`eabb26f5` (commits `19d999c1`, `22412ceb`, `f3e301cc`, `eabb26f5`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r14.md` and `.agent/last_block.md` are byte-identical, sha256 `c69adf225c91896c12cc5b678b65a6e5c3c9baa27a3bba0734c6208d53383127`, reproduced directly by `cmp` and `sha256sum`. THE CODE, reproduced by `git show 22412ceb`: all 4 FROM/TO edits landed exactly as ordered — the `stats.bench` reword, the `VOCABULARY_MODE` flip with its comment, the new `SYNONYM_EXEMPTIONS` block, and `_synonym_offenders()`'s return line — and the commit's path set is exactly the two declared files. THE MEASUREMENT, reproduced directly at HEAD against the real, committed catalog: `_meaning_violations()` reads `[]`, `_synonym_offenders()` reads `[]`, `VOCABULARY_MODE` reads `"enforced"` — matching the block's own G1 prediction exactly. THE G5 CHECK, reproduced directly: the raw (pre-exemption) offender set, recomputed by re-running `_synonym_offenders()`'s own loop without the final subtraction, reads exactly `{('arg:do.run:--fixture-builder:description', 'loop'), ('command:dev.agent-loop:command_id', 'loop')}`, identical to `SYNONYM_EXEMPTIONS` — the exemption removes exactly these two and nothing else. THE GATES, reproduced directly: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` reads `74 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `python3 -m ruff check apps/cli/command_catalog.py tests/docs/test_vocabulary.py` reads `All checks passed!`. THE OPERATOR QUESTION: `.agent/operator_questions.md`'s Q1 entry lands exactly as the block's Constraints specify — heading `### Q1 — narrow vocabulary check's synonym scope (2026-09-17, F281, round 14)`, body in plain sentences with no ids, round numbers, decision ids or file paths, the standard closing sentence. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `eabb26f5` matches `origin/feature/f281-cli-help-surface`. A HARMLESS SELF-REFERENCE NOTE (not a defect): the handback's own "Final HEAD: f3e301cc" names the commit before its own C3, the same convention round 13's handback used (`90bf6f46` before its own `a8e42d10`) — the true final HEAD, `eabb26f5`, is what this entry verifies. WHY PASS: every byte independently reproduces, all 4 code edits are correct and complete, the exemption is proven non-vacuous and exactly as narrow as DECISION F281 D3 claims, and the operator-questions entry matches its spec exactly.
```

### DECISION — append to `.agent/decisions.md`, after its current last
line, separated by exactly one blank line, verbatim:

```
## DECISION F281 D4 (2026-09-17, F281 round 15) — `_box()`'s long right-column text wraps across continuation lines instead of being truncated with an ellipsis

CONTEXT. `docs/roadmap/features/T2_F281.md`'s Acceptance list carries, verbatim
from F261's T004 via F280's T002: "A 200-character option help renders without
`…`." `apps/cli/help_renderer.py`'s `_box()`, the shared row-renderer behind
`render_root_help`, `render_group_help` and `render_command_help`, truncated
any row whose `"  {left}{pad}  {right}"` content exceeded `BOX_WIDTH` (78) to
`BOX_WIDTH - 1` characters plus `"…"`.

MEASURED. `apps/cli/command_catalog.py`'s real, committed catalog carries a
221-character `ArgDef.help` string (`job.show --full`) and group descriptions
up to 96 characters; before this round, `python3 -m apps.cli.grouped job show
--help` truncated `--full`'s help with an ellipsis, and even the default
`python3 -m apps.cli.grouped --help` (no option over 200 characters, only two
group descriptions over 78) printed the ellipsis twice, and
`python3 -m apps.cli.grouped --all-commands` printed it at least once. A
disposable-worktree dry run of the fix reproduces zero ellipsis in `--help`,
`--all-commands` and `job show --help`, and a mutation red-proof — reverting
only the `_box()` edit — reddens exactly the round's own four ellipsis-guard
tests (`test_long_content_wraps_without_ellipsis`,
`test_root_help_has_no_ellipsis`, `test_every_group_help_has_no_ellipsis`,
`test_every_command_help_has_no_ellipsis`, 19 passed / 4 failed) and no other
test, confirming the fix is load-bearing.

CHOSEN. `_box()` computes `prefix_width` (the fixed `"  {left}{pad}  "` gutter)
and `wrap_width = BOX_WIDTH - prefix_width`, then calls
`textwrap.wrap(right, width=wrap_width)` and emits one row per wrapped line,
continuation lines indented under the right column by `prefix_width` spaces.
No new dependency: `textwrap` is stdlib. The three render functions and every
caller are unchanged — only `_box()`'s internals move, so the fix reaches
`render_root_help`, `render_group_help` and `render_command_help` at once.

ALTERNATIVES CONSIDERED. Widening `BOX_WIDTH` — rejected: no fixed width
accommodates a 359-character command description (the longest in the
catalog), and a wider box would still truncate eventually while making every
short row wider for no reason. Wrapping only past a higher threshold and
truncating past a second, larger one — rejected: the Acceptance line requires
no truncation at all, not a longer rope. Reflowing with
`shutil.get_terminal_size()` instead of a fixed width — rejected: the module's
own docstring states "Deterministic — no terminal probing, fixed width (78
inner)" as a design constraint this round does not touch.

CONSEQUENCE. Every catalog surface's help text, however long, renders in full
across as many lines as it needs; `remedy --help`, every `remedy <group>
--help` and every `remedy <group> <command> --help` carry zero `"…"`
characters, measured directly rather than assumed. HOW TO REVERSE: revert
this round's C2 commit; delete this paragraph.
```

### PLAN15 — replace the entire content of `.agent/plan.md` with exactly:

```
# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 15. C1 books round 14's PASS. C2 fixes `apps/cli/help_renderer.py`'s
`_box()`: long right-column text now WRAPS across continuation lines instead
of being truncated with an ellipsis (DECISION F281 D4), clearing the
Acceptance line "A 200-character option help renders without `…`." Three new
tests in `tests/test_help_renderer.py` sweep the real catalog (root help,
every group, every command) for zero ellipsis.

## Next Steps

1. Remaining Acceptance items, freshly re-measured this round: the D4 visible
   group order test does not exist yet; `doctor core`'s dead-commands section
   does not exist (design item (c) of DECISION amend0905-vocab D11,
   `T2_F271.md` T002 — check the scope-overlap risk below before authoring);
   R-0805, R-0809, R-0895 and R-0934 are all still OPEN; the README quickstart
   is unchanged. Re-measure fresh at round 16's claim rather than trusting
   this line.
2. Session 2 of F281 is 7 delegated rounds in (rounds 9-15), at the top of
   the 6-to-8 target (amend0905-throughput). End this session after round 15
   on demonstrably sufficient progress, or continue if context comfortably
   suffices.

## Risks

- The `doctor core` dead-commands section appears in BOTH this feature's own
  Acceptance list and F271's (`T2_F271.md` T002, design item (c)) — F271 runs
  AFTER F281 in STATUS order. Read both files fresh before claiming that item;
  do not implement the same mechanism twice.
```

## C2 — CODE (4 edits: 2 in `apps/cli/help_renderer.py`, 2 in
`tests/test_help_renderer.py`)

Apply each FROM → TO pair below EXACTLY. Every FROM string must appear
verbatim EXACTLY ONCE (edits 3 and 4 are APPEND pairs — TO contains FROM
verbatim, checked by containment, not by occurrence count); if a
single-occurrence FROM does not match exactly once, STOP and report the
exact mismatch rather than guessing or forcing it.

1. Add the `textwrap` import, in `apps/cli/help_renderer.py`. FROM (whole
   3-line block):
```
from __future__ import annotations

BOX_WIDTH = 78  # inner width (between vertical bars)
```
TO:
```
from __future__ import annotations

import textwrap

BOX_WIDTH = 78  # inner width (between vertical bars)
```

2. `_box()`'s row-rendering loop, in `apps/cli/help_renderer.py`. FROM (whole
   9-line block, 4-space indent for `else:`):
```
    else:
        max_left = max(len(r[0]) for r in rows)
        for left, right in rows:
            pad = " " * (max_left - len(left))
            content = f"  {left}{pad}  {right}"
            # Truncate if too long, pad if too short
            if len(content) > BOX_WIDTH:
                content = content[: BOX_WIDTH - 1] + "…"
            content = content.ljust(BOX_WIDTH)
            lines.append(f"│{content}│")
```
TO:
```
    else:
        max_left = max(len(r[0]) for r in rows)
        prefix_width = 2 + max_left + 2
        wrap_width = max(BOX_WIDTH - prefix_width, 1)
        for left, right in rows:
            pad = " " * (max_left - len(left))
            prefix = f"  {left}{pad}  "
            wrapped = textwrap.wrap(right, width=wrap_width) or [""]
            lines.append(f"│{(prefix + wrapped[0]).ljust(BOX_WIDTH)}│")
            for cont in wrapped[1:]:
                lines.append(f"│{(' ' * prefix_width + cont).ljust(BOX_WIDTH)}│")
```

3. Rename and rewrite `test_long_content_truncated`, in
   `tests/test_help_renderer.py`. FROM (whole 4-line block):
```
    def test_long_content_truncated(self) -> None:
        text = _box("Test", [("x" * 40, "y" * 50)])
        for line in text.splitlines():
            assert len(line) == BOX_WIDTH + 2, f"Line too long: {len(line)}"
```
TO:
```
    def test_long_content_wraps_without_ellipsis(self) -> None:
        text = _box("Test", [("x" * 40, "y" * 50)])
        assert "…" not in text
        for line in text.splitlines():
            assert len(line) == BOX_WIDTH + 2, f"Line too long: {len(line)}"
```

4. Insert `TestNoEllipsisAcrossCatalog`, in `tests/test_help_renderer.py`,
   immediately before `class TestRenderError:` (this pair is an APPEND: TO
   contains FROM verbatim, confirmed by direct containment check). FROM:
```
class TestRenderError:
```
TO:
```
class TestNoEllipsisAcrossCatalog:
    """Acceptance (T2_F281.md): a 200-character option help renders without an
    ellipsis — long text wraps instead of being truncated."""

    def test_root_help_has_no_ellipsis(self) -> None:
        from apps.cli.command_catalog import GROUPS
        groups = [(g.id, g.description) for g in GROUPS.values()]
        text = render_root_help("remedy", "Remedy.", groups)
        assert "…" not in text

    def test_every_group_help_has_no_ellipsis(self) -> None:
        from apps.cli.command_catalog import GROUPS, get_commands_for_group
        for group_id, group_def in GROUPS.items():
            commands = [(c.subcommand, c.description) for c in get_commands_for_group(group_id)]
            text = render_group_help("remedy", group_id, group_def.description, commands)
            assert "…" not in text, f"group {group_id} help was truncated"

    def test_every_command_help_has_no_ellipsis(self) -> None:
        from apps.cli.command_catalog import CATALOG
        for cmd in CATALOG:
            positionals = [(a.name, a.help) for a in cmd.args if not a.is_option]
            options = [(a.name, a.help) for a in cmd.args if a.is_option]
            text = render_command_help(
                "remedy", cmd.group_id, cmd.subcommand, cmd.description, positionals, options
            )
            assert "…" not in text, f"{cmd.command_id} help was truncated"


class TestRenderError:
```

## Constraints

- The C2 commit's path set is exactly two files: `apps/cli/help_renderer.py`
  and `tests/test_help_renderer.py`. `tests/test_grouped_cli.py` is read by
  G1 but not touched.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.
- No `.agent/operator_questions.md` entry this round: this fix directly
  implements an explicit Acceptance line with no policy tradeoff, so there is
  nothing for the operator to rule on.
- Do not touch `docs/roadmap/features/T2_F281.md` or `T2_F271.md`; the scope
  question PLAN15 names is read-only research for round 16, not this round's
  work.

## Gates (at most six; run and record real exit codes)

- G1 TARGETED: `python3 -m pytest tests/test_help_renderer.py
  tests/test_grouped_cli.py -q` — expect `296 passed` (293 baseline + 3 new
  sweep tests; the renamed test does not change the count).
- G2 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect
  `42 passed`, unchanged.
- G3 RUFF: `python3 -m ruff check apps/cli/help_renderer.py
  tests/test_help_renderer.py` reads `All checks passed!`.
- G4 DIRECT MEASUREMENT: count occurrences of `"…"` in the real output
  of `python3 -m apps.cli.grouped --help`, `python3 -m apps.cli.grouped
  --all-commands` and `python3 -m apps.cli.grouped job show --help` — expect
  `0`, `0`, `0` for all three (down from 2, a nonzero count, and 1
  respectively before this round's fix).
- G5 MUTATION RED-PROOF, in a disposable git worktree (`git worktree add
  --detach`, removed after use): with this round's edits applied,
  `python3 -m pytest tests/test_help_renderer.py -q` reads `23 passed`; then
  revert ONLY edit 2 (the `_box()` FROM/TO pair) back to its FROM text,
  leaving the import and both test edits applied, and re-run the same
  command — expect exactly `test_long_content_wraps_without_ellipsis`,
  `test_root_help_has_no_ellipsis`, `test_every_group_help_has_no_ellipsis`
  and `test_every_command_help_has_no_ellipsis` to FAIL (`19 passed, 4
  failed`) and no other test to change; then re-apply edit 2 and confirm
  `23 passed` again before deleting the worktree.
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only
  the primary checkout, HEAD matches `origin/feature/f281-cli-help-surface`
  after push. Re-run this LITERALLY as the LAST action before writing the
  handback.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output; the branch is pushed; `.agent/handoff.md` is
rewritten as C3 naming this round, its commits, its verification results,
and the next expected action (round 16 re-reads `T2_F281.md`'s Acceptance
list fresh, resolves the F271 dead-commands scope question PLAN15 names
before touching that item, and claims the next unverified Acceptance line).
If the worker corrects anything in this block, the correction is stated
explicitly under "Deviations & assumptions" — never left silent.
