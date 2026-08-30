── STEP T003 PART 1 / F040 — ROUND 15 ────────────────────────
Goal:        CLI parity: `remedy job digest <id>` prints the same composition
             the HTTP route prints — "the report's little sibling"
             (`docs/roadmap/features/T5_F040.md` line 72). Bare mode prints a
             short human block; `--json` prints `build_job_digest(job, events)`
             VERBATIM, obtained the SAME two calls `_cmd_job_summary`
             (`apps/cli/commands/job.py:1133-1178`) already makes —
             `resolve_job_id`/`load_job` then `load_run_events(resolve_data_root(),
             job.id)` — so the CLI and the route
             (`packages/orchestration/ui_server.py:2778-2782`, `_build_digest_json`)
             can never print a different envelope for the same job. This round
             does not touch `build_job_digest` itself, any `.ts`/`.tsx` file, or
             the end-to-end scenario T003 also names — those are the next round.

Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R14 verdict) · C3 the catalog entry ·
             C4 the command + its dispatch wiring · C5 its guard ·
             C6 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r15.md`               (C0a, new)
               `.agent/last_block.md`                       (C0b)
               `.agent/plan.md`                             (C1)
               `.agent/live_review.md`                      (C2)
               `apps/cli/command_catalog.py`                (C3)
               `apps/cli/commands/job.py`                   (C4)
               `tests/cli/test_job_digest_cli.py`           (C5, new)
               `.agent/handoff.md`                          (C6)
             NOTHING ELSE IS EDITED. `packages/orchestration/job_digest.py`,
             `packages/orchestration/ui_server.py`, `packages/orchestration/timeline.py`,
             `packages/orchestration/decision_inbox.py`, every file under
             `apps/ui/` and every file under `docs/roadmap/` are READ ONLY.

Constraints:
 1. APPLY EVERY AUTHORED SLICE BYTE FOR BYTE. If a slice looks wrong, apply it
    anyway and DECLARE the objection in the handback. Never repair a slice.
    `command_catalog.py`'s new entry, `job.py`'s new function and dispatch
    line, and the new guard file are a SPEC, not a slice — the code is yours
    to write — and this constraint does not bind them; constraints 5-10 below
    bind them instead.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6 and it is fixed.
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the
    finding ledger, so `.agent/plan.md` is current before the ledger is
    touched.
 4. RECORD15 IS APPENDED, never inserted. Measured directly rather than
    assumed: read `.agent/live_review.md`'s exact byte length at the branch
    tip this round opens on and confirm whether it ends with a trailing
    newline; do not trust this line's own claim about that byte. The append
    is one newline followed by the slice's bytes. READING (b) IS STATED HERE
    IN ITS FINAL, GENERALIZED FORM, learned across three rounds of the same
    template gaining and then needing a correction (R12 undeclared, R13
    declared, R14's own N=1 case still needing a fix) — G3 below states it
    directly: paragraph 1 of the slice is ALWAYS checked by SUFFIX match,
    because a single-newline join always fuses it with the base's own last
    pre-existing paragraph, WHETHER OR NOT paragraph 1 is also the slice's
    only (last) paragraph; every paragraph 2..N, if N>1, is checked by RAW
    EQUALITY against the committed file's own blank-line units in order.
    This reading needs no case split on N and is expected to survive future
    single-paragraph appends without another correction.
 5. `_cmd_job_digest`'S NEW LINES, IN THIS SHAPE (a SPEC: comment wording is
    yours, calls and order are fixed):
    (i)   `job_id = resolve_job_id(job_id_str)` then `job = load_job(job_id)`
          inside a `try`, `except JobNotFoundError:` catching it — the SAME
          shape `_cmd_job_report` uses at `apps/cli/commands/job.py:1743-1751`;
    (ii)  on that except branch, if `json_output` print
          `_json.dumps({'error': 'job_not_found', 'job_id': job_id_str})` to
          stdout, else print `f'Error: job not found: {job_id_str}'` to
          `sys.stderr` — the SAME two spellings `_cmd_job_run_report` uses at
          `apps/cli/commands/job.py:1709-1712` — then `sys.exit(1)`;
    (iii) `data_dir = resolve_data_root()` then
          `events = load_run_events(data_dir, job.id)`, importing
          `load_run_events` from `packages.orchestration.timeline` the same
          way `_cmd_job_summary` does at `apps/cli/commands/job.py:1144-1147`;
    (iv)  `digest = build_job_digest(job, events)`, importing `build_job_digest`
          from `packages.orchestration.job_digest` — the ONLY call in this
          function that builds the envelope; no field of `digest` is
          recomputed, renamed or filtered before being printed;
    (v)   if `json_output`, `print(_json.dumps(digest, indent=2))` and
          `return` — the digest dict PASSED THROUGH WHOLE, matching
          `_build_digest_json`'s own return value for the same job byte for
          byte once both are serialized;
    (vi)  else, five `print` lines reading (in this order) the job id, then
          `digest["state"]`, then `digest["headline"]` verbatim, then
          `digest["cost"]["value"]` and `digest["cost"]["basis"]` on one
          line, then `digest["decisions"]["open_count"]` and
          `digest["decisions"]["peak_urgency"]` on one line, then
          `digest["primary_action"]["label"]` on the last line. No
          `ownership` line is rendered this round: the key is always empty
          (DECISION F040 D3) and giving it a display format before F035
          ships a producer would guess at a shape nothing produces yet.
 6. `_json.dumps(` OCCURS EXACTLY TWICE in `_cmd_job_digest`'s body: once in
    (ii)'s error branch, once in (v)'s success branch. `build_job_digest(`
    occurs exactly once. `resolve_job_id(`, `load_job(`, `resolve_data_root(`
    and `load_run_events(` each occur exactly once.
 7. THE CATALOG ENTRY. In `apps/cli/command_catalog.py`, insert one
    `CommandEntry` immediately after the `job.report` entry's closing `),`
    (the entry ending at line 512 today) and before the `job.fences` entry
    (starting at line 514 today):
      `command_id="job.digest"`, `group_id="job"`, `subcommand="digest"`,
      a one-line `description` naming the completion digest,
      `action_class="read_only"`, `args=(_JOB_ID, _JSON_OPT)`,
      `supports_json=True`, `related=("job.report", "job.summary")`.
    Exactly one `CommandEntry` in the whole file has `command_id="job.digest"`.
 8. THE DISPATCH WIRING. In `apps/cli/commands/job.py`'s `COMMAND_HANDLERS`
    dict, insert `"job.digest": lambda args: _cmd_job_digest(args.job_id,
    json_output=getattr(args, "json", False))` — place it adjacent to
    `"job.report"`'s own entry (today ending at line 2440, immediately before
    `"job.fences"` at line 2441), in either order relative to `job.report`'s
    own lines as long as it is not split across a comment block that belongs
    to a different entry. Exactly one key `"job.digest"` in the dict.
 9. THE FUNCTION'S PLACEMENT in `apps/cli/commands/job.py`: define
    `_cmd_job_digest` immediately after `_cmd_job_report` ends (today the
    blank line at 1841, before `def _cmd_job_dod` at 1842) — proximity to its
    closest sibling, not a load-bearing constraint G5 checks by position, but
    do not scatter it elsewhere in the file.
10. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN BEFORE
    C6. If it appears, finish the commit in hand, write the handback and
    stop.
11. DESTRUCTIVE VERIFICATION ONLY INSIDE A DISPOSABLE `git worktree` WHERE
    ANY IS NEEDED, removed before the handback, with `git worktree list`
    showing one line after. The primary checkout satisfies `git status
    --porcelain` empty at every commit. This round's own guard (C5) is a
    plain pytest module exercising Python functions directly — no worktree
    is needed for G6's own mutations if they are made and reverted inside
    the primary checkout using a saved copy of the two edited files restored
    byte-for-byte after each; a worktree is the SAFER default and is
    preferred, but either is acceptable as long as `git status --porcelain`
    reads empty at every commit boundary.

Done when: every gate below is executed, each with its REAL exit code taken
from `subprocess.run(...).returncode`. All of them run at commits strictly
earlier than C6, and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk, against the reviewer's
    own surviving original: report the sha256 and byte length of
    `.remedy-wt/f040-r15-block.md`, of `.agent/authored/f040-r15.md` and of
    `.agent/last_block.md`, and that all three are equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN15 slice; report
    its line count and that it is under 50; report that it holds `## Goal`,
    `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2, USING THE GENERALIZED READING (b) OF
    CONSTRAINT 4. Re-measure the pre-commit length rather than taking it from
    this block. Reading (a): the base blob is a byte PREFIX of the committed
    file and base + one newline + slice reconstructs it whole. Reading (b):
    split the slice on blank lines into N paragraphs (N counted by the
    script, never asserted); paragraph 1 is checked by asking whether SOME
    blank-line unit of the committed file ENDS WITH paragraph 1; each
    paragraph 2..N, if N>1, is checked by RAW EQUALITY against the
    committed file's own blank-line units in order. Negative control: inside
    a disposable worktree, flip one byte inside paragraph 1 (the slice's
    only paragraph if N=1) and report that both readings REJECT it and both
    ACCEPT the unflipped bytes.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base and
    the committed file, never by reading the slice: the distinct ids
    matching `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching
    `^Gate: F040 R14 — `. Report ADDED and REMOVED for each set and the
    open count (registered minus resolved, both distinct) before and after;
    report that no id's status changes this round.
 G5 THE COMMAND'S SHAPE, at C3 and C4. Over `apps/cli/command_catalog.py`:
    report the count of `CommandEntry(...)` blocks whose `command_id` equals
    `"job.digest"` (must be 1), and that its tuple names
    `args=(_JOB_ID, _JSON_OPT)` and `supports_json=True`. Over
    `apps/cli/commands/job.py` with comments stripped: extract
    `_cmd_job_digest`'s own function body (from its `def` line to the next
    top-level `def`) and report, IN SOURCE-POSITION ORDER inside that span,
    the offset of `resolve_job_id(`, `load_job(`, `except JobNotFoundError`,
    `resolve_data_root(`, `load_run_events(`, `build_job_digest(`, and the
    FIRST and SECOND occurrence of `_json.dumps(` — seven markers, strictly
    increasing except the two `_json.dumps(` occurrences which straddle the
    `if json_output`/`else` branch (report both). Report that
    `build_job_digest(` occurs exactly once and `_json.dumps(` occurs exactly
    twice in that span. Separately, report the count of the key
    `"job.digest"` in the `COMMAND_HANDLERS` dict (must be 1) and that its
    value's source text contains `_cmd_job_digest(` and
    `json_output=getattr(args, "json", False)`.
 G6 THE GUARD'S OWN RUN AND ITS RED PROOF, at C5. First,
    `python3 -m pytest tests/cli/test_job_digest_cli.py -q` in the primary
    checkout, real exit code. Second, THE RED PROOF, for EACH of these four
    mutations to `apps/cli/commands/job.py` — asserting the anchor is UNIQUE
    before replacing it, reverting to the control and re-confirming green
    before the next, inside a disposable worktree or a saved-and-restored
    copy per constraint 11:
      (a) in `_cmd_job_digest`, change `if json_output:` (the branch guarding
          (v)'s JSON print) to `if True:`, so bare mode also emits JSON;
      (b) change (v)'s `print(_json.dumps(digest, indent=2))` to
          `print(_json.dumps({'digest': digest}, indent=2))`, wrapping the
          envelope in an extra key;
      (c) in (ii)'s except branch, delete the `if json_output:` / `else:`
          split so the plain-text stderr line always prints regardless of
          `--json`;
      (d) change (i)'s `job_id = resolve_job_id(job_id_str)` to
          `job_id = job_id_str`, skipping short-id-prefix resolution.
    For each, report the guard's real exit code (must be 1) and the node ids
    that FAILED. Restore and report byte equality to the committed file, and
    the guard green again, after each.
 G7 THE SUITES AND THE TREE, at C5:
      python3 -m pytest tests/cli/ -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/docs/ -q
    Report each REAL exit code. Then report `git status --porcelain`, the
    count from `git ls-files --others --exclude-standard`, `git worktree
    list`, and the `+` column of `git diff --numstat` for each commit from
    C0a through C5. C6's own insertion count is not orderable here and is not
    ordered (§3 item 14). Those insertion numbers are ALSO required in the
    handback's `## Commits` table `+/-` column (§3 item 28): take every cell
    from THIS gate's output and say in the handback that you did.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — this is SESSION 3 of F040 — the round
             (15), the range, the per-commit table with the `+/-` column from
             `git diff --numstat`, one line per gate with its REAL exit code,
             the item-status table, the deviations, and the open-findings
             count. Then `git push -u origin feature/f040-completion-digest`.
             Create no pull request, merge nothing, force-push nothing, touch
             no branch.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN15
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 15.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D10 | done | rounds 2-9 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | round 7, PASS |
| T002 the hero card stylesheet and its guard | done | round 8, PASS |
| T002 the card's copy rules and the §17 screen | done | round 9, PASS |
| T002 the card component and its guard | done | round 11, PASS |
| T002 the storage edge (dismissal + last-seen) | done | round 12, PASS |
| T002 the fetch loader `loadJobDigest` | done | round 13, PASS |
| T002 the mount into `RemedyShell.tsx` | done | round 14, PASS |
| T003 CLI parity — `remedy job digest <id>` | done | this round |
| T003 the end-to-end, integration gate, closure | open | next |

## Next Steps
1. This round adds `remedy job digest <id>` (bare text + `--json`), reusing
   `build_job_digest`/`load_run_events` the same way `_cmd_job_summary`
   already does, so the CLI and the HTTP route can never disagree.
2. The next round is the end-to-end: finish a fake job while the UI is
   "away", reopen, hero shows the right CTA, dismiss, no re-show — then the
   integration gate and closure.
3. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN15

<<<BEGIN RECORD15
Gate: F040 R14 — T002 PART 5E, THE MOUNT INTO REMEDYSHELL.TSX. VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, per docs/agents/self_drive_protocol.md Phase 2 step 3. THE MOUNT: `RemedyShell.tsx`'s diff (`24f5d155..fac40f99`) was read in full — the six new pieces constraint 5(i)-(vi) orders appear in that order (the digest load effect, `browserDigestVisibilityPort(window.localStorage)`, the last-seen lazy-read then write effect, the dismissal lazy-read, `latestActivityMs` from `newestActionRow(stream.recent ?? [])`, and `digestVisibility({...nowMs: Date.now()})`), the card renders as the first child of the viewport div immediately after `<DegradedBanner>` and before the shell's own div, is conditioned on `digest !== null`, and `onDismissed` re-reads the port rather than hard-coding an instant; `onOpenDecisions`/`onPrimaryAction` are omitted entirely, matching constraint 6. Deviation 2's claim — `DigestVisibilityPort` correctly NOT imported because TypeScript infers `digestPort`'s type from `browserDigestVisibilityPort`'s own return type — was independently confirmed against the diff's own import block, which names only the value `digestVisibility` and the type `DigestDismissal`. THE LEDGER: independently computed by script over `.agent/live_review.md`, by difference between `1c08f775^` and `1c08f775` — registered ADDED `[]` REMOVED `[]`, resolved ADDED `[]` REMOVED `[]`, `DECISION F040 D\d+` ADDED `[]` REMOVED `[]`, `^Gate: F040 R13 — ` 0 before → 1 after, open count 262 → 262, distinct registered 317 → 317, distinct resolved 55 → 55 — matching the handback exactly. THE GUARD'S OWN RED PROOF WAS INDEPENDENTLY REPRODUCED: the reviewer built its own disposable worktree (`.remedy-wt/wt-review-r14`, removed after), applied mutation (c) — deleting `window.localStorage` from the `browserDigestVisibilityPort(` call — and got the SAME two failures the handback reports, both inside `TestStorageEdgeBindsTheRealLocalStorage`; restored and reconfirmed 26/26 green, `git worktree list` back to one line. THE SIX SUITES OF G7 WERE INDEPENDENTLY RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT: `tests/ui_contracts/` 809 passed, 4 skipped; `tests/ui_server/` 515 passed; `tests/docs/` 295 passed; `tests/cli/test_golden_path.py` 42 passed; the vitest-foundation node 4 passed; the typescript node 1 passed, 73 deselected — every figure matches the handback's own claim exactly. G1, G2 and G3's own byte-script re-execution were read and cross-checked against the diff and the block's own procedure rather than independently re-executed; nothing in that reading contradicts the handback. ONE NON-BLOCKING GAP IS CARRIED FORWARD IN THE REVIEWER'S OWN GATE TEMPLATE, DECLARED BY THE WORKER RATHER THAN FOUND BY THIS REVIEW: G3 reading (b)'s wording, corrected at R14's own block relative to R13's, still assumed paragraph 1 and paragraph N were different paragraphs and so had a residual gap for N=1, which R14's own RECORD14 slice hit exactly (a single dense paragraph). The worker applied the structurally consistent generalization instead — paragraph 1 is ALWAYS checked by suffix match because it is always the one fused with the base's own last paragraph, and paragraph N gets raw equality only when N>1 — and reported PASS under that reading, which the reviewer independently confirms is the correct generalization and damages nothing on disk. Per amend0827 rule 2 this spends no id and buys no correction round; THIS ROUND'S OWN G3 ABOVE STATES THE GENERALIZED WORDING DIRECTLY FROM THE START, so a future N=1 append is not a fourth occurrence of the same undeclared-then-declared cycle. THE ROUND PASSES: every path in the change set matches the block's order, no constraint is violated, the tree is clean and pushed. No new finding is raised by this review.
<<<END RECORD15

SPEC — `apps/cli/command_catalog.py` (C3, edit)

Read the file's `job.report` and `job.fences` entries at HEAD before writing
anything. Insert one new `CommandEntry` between them, per constraint 7. Use
`_JOB_ID` and `_JSON_OPT`, already imported/defined in this module — do not
redefine either.

SPEC — `apps/cli/commands/job.py` (C4, edit)

Read `_cmd_job_summary` (1133-1178), `_cmd_job_report` (1739-1840) and
`_cmd_job_run_report`'s error branch (1703-1713) at HEAD before writing
anything — every anchor in constraints 5, 6, 8 and 9 is a real line in one of
them today. Add `_cmd_job_digest` per constraint 5, wired per constraint 8,
placed per constraint 9. `JobNotFoundError`, `resolve_job_id`, `load_job` and
`resolve_data_root` are already imported at module level (used by the
functions above) — do not re-import them; do import `load_run_events` from
`packages.orchestration.timeline` and `build_job_digest` from
`packages.orchestration.job_digest` inside the function body, matching the
local-import style `_cmd_job_summary` already uses at line 1144.

SPEC — `tests/cli/test_job_digest_cli.py` (C5, new file)

Follow the shape `tests/cli/test_job_report.py` already establishes over this
SAME command family — read it in full before writing this, it is your
closest sibling: the `isolate_data_root` autouse fixture, a `saved_job(...)`
helper building a real `Job`/`Task` via `packages.core.models` and
`packages.orchestration.storage.save_job`, and direct-function-call tests
against `capsys` (this CLI is argparse-based; no `CliRunner`, no subprocess).
Import `_cmd_job_digest` from `apps.cli.commands.job` and
`build_job_digest` from `packages.orchestration.job_digest`. Cover, each with
its own discriminator matching the four mutations G6 orders:
  - `--json` output, parsed with `json.loads`, is `==` to
    `build_job_digest(job, load_run_events(resolve_data_root(), job.id))`
    computed independently in the test (the exact-equality assertion that
    catches (a) and (b) both);
  - bare-mode output is NOT valid JSON (`pytest.raises` around `json.loads`,
    or an equivalent non-parse assertion) and contains the job id and the
    digest's own `state` string;
  - an unknown job id: bare mode exits 1 with a clean stderr message and no
    traceback and no stdout; `--json` mode exits 1 with a stdout JSON payload
    whose `error` key is `"job_not_found"` (the discriminator for (c));
  - a short (8-character) prefix of a real job's id resolves to the same
    digest `--json` would print for the full id (the discriminator for (d));
  - the catalog registers `job.digest` exactly once (`CATALOG` from
    `apps.cli.command_catalog`), and its `args` name both `job_id` and
    `--json` (`get_command("job.digest")`).
A guard file whose tests cannot fail against all four G6 mutations is not
this round's guard, it is a guess that happens to read green.
──────────────────────────────────────────────────────────────
