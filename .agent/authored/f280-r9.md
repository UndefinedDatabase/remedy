── STEP R9/n — F280 ────────────────────────────────────────
Goal: book round 8's independently-reviewed PASS, register R-0940 (round 8's handback falsely
claimed a disposable worktree was cleaned up), and add `worker doctor`
(DECISION amend0905-vocab D4).

Bundle:
  1. Copy this block to `.agent/authored/f280-r9.md` and mirror to `.agent/last_block.md`.
  2. Append the Gate:F280 R8 + R-0940 register text to `.agent/live_review.md`, and replace
     `.agent/plan.md` with the new full content — both pre-built and pre-verified by the
     reviewer in a disposable worktree.
  3. Apply the pre-built `worker doctor` patch.
  4. Run the done-when gates, run the canary, write the handoff, commit, push.

Change — exact files, exact source:
  All four source files below live under `/home/decodeux/Repos/remedy/.remedy-wt/` (repo-root
  scratch, NOT a git ref — plain files on disk in the primary checkout's own working tree).
  Copy each BYTE-FOR-BYTE with `shutil.copyfile` or equivalent; do not retype.

  (a) `.agent/live_review.md` — append, IN THIS ORDER, to the end of the current file (which
      currently ends in exactly one `\n`):
        1. one `\n` byte (blank-line paragraph separator)
        2. the exact bytes of `.remedy-wt/gate_r8_entry.txt` (sha256
           `0826f00d14145887b03a8f57038cebc8cfa02fde545eedd6dbf621b358c45f59`, 4256 bytes,
           already ends in its own single `\n`)
        3. one `\n` byte (blank-line separator)
        4. the exact bytes of `.remedy-wt/reg_r0940.txt` (sha256
           `13b59a16b966a74be251781b7a37500eba1d5dc968a523a36ab8e60759c3ac23`, 1885 bytes,
           already ends in its own single `\n`)
      i.e. `new_bytes = old_bytes + b"\n" + gate_r8_entry + b"\n" + reg_r0940`. Do NOT restore
      any further newline byte this round — round 8 already fixed R-0939 and the file already
      ends in `\n`.
  (b) `.agent/plan.md` — REPLACE THE WHOLE FILE with the exact bytes of
      `.remedy-wt/f280-r9-plan.md` (sha256 `6a6aa759c706c8b9907a7725ce4c165bfb2e7b5fcdb4640d352f7a3fdcd0d1f4`,
      2743 bytes, 46 lines). This is a rewrite per AGENTS.md `.agent/plan.md` convention, not
      an append.
  (c) Apply `.remedy-wt/f280-r9-doctor.patch` (sha256
      `19cc5623f0b44334193a5c558c8dbc446ec2837477c4ca176aac5678efbc7d50`, 8689 bytes, 199
      lines) with `git apply --check` then `git apply` from the repo root. It touches exactly:
      `apps/cli/command_catalog.py` (adds one `CommandEntry` for `worker.doctor`, right after
      `worker.status`, matching D4's stated subcommand order `list | show | resources | unload
      | status | doctor`), `apps/cli/commands/worker.py` (adds `_cmd_worker_doctor` and its
      `COMMAND_HANDLERS["worker.doctor"]` entry), and a new file `tests/cli/test_worker.py`
      (11 tests: catalog wiring, ready/not-ready on ollama's presence, that a `future`-status
      spec is never probed, text output, and that an `available` spec with no defined probe
      FAILS rather than silently passing).

Constraints:
  - Do not touch any file this block does not name.
  - `worker doctor` probes ONLY the `ollama` provider (the one spec currently `status=
    "available"` in `packages/orchestration/worker_adapters.py`); every other spec is
    `status="future"` and this round adds no probe for any of them — a doctor that claims a
    future provider is ready would be worse than one that says nothing.
  - `worker doctor` makes NO network call and writes NO file; its one side effect is
    `shutil.which("ollama")`, the same read-only PATH lookup `worker resources` already does.
  - Commit order: C0a (authored carrier) → C0b (last_block mirror) → C1 (the two `.agent/`
    fixes, ONE commit) → C2 (the patch application, ONE commit) → C3 (handoff). Do not split
    C1 or C2 further; both are far under the 500-line insertion cap.
  - `git status --porcelain` empty before your first commit and after your last.
  - Any disposable worktree you create for verification (including the G8 mutation below)
    goes under `.remedy-wt/`, inside this checkout — NOT `/tmp` — and you remove it yourself
    as the LAST action of the step that created it, verified by `git worktree list` showing
    only the primary checkout before your handback commit.

Done when (run every command from the repo root, primary checkout):
  G1 TRANSPORT — one digest comparison: `sha256sum .agent/authored/f280-r9.md` equals
     `sha256sum .agent/last_block.md`, and `cmp` each of the four source files under
     `.remedy-wt/` against the corresponding section it produced in the committed target —
     report PASS/FAIL, not a re-typed diff.
  G2 THE RECORD — after C1, over `.agent/live_review.md`:
     `python3 -c "import re; d=open('.agent/live_review.md').read(); print(len(re.findall(r'^Gate: F\d+ R\d+ — ', d, re.M)), len(set(re.findall(r'^- (R-\d{4}) — ', d, re.M))), len(set(re.findall(r'^Done: (R-\d{4}) — ', d, re.M))))"`
     must read exactly `35 136 7`. `.agent/plan.md` must be exactly 46 lines with exactly one
     `## Goal`, one `## Current Step`, one `## Next Steps`, one `## Risks`.
  G3 THE PATCH — after C2, `git diff --numstat 146ca89f..HEAD -- apps/ tests/` reads exactly
     three paths: `apps/cli/command_catalog.py` 10/0, `apps/cli/commands/worker.py` 57/0,
     `tests/cli/test_worker.py` 99/0 (a new file).
  G4 THE CATALOG — after C2, `worker.doctor` is in `apps.cli.command_catalog.CATALOG`
     (`command_id`), it is the LAST entry with `group_id == "worker"` (D4's own subcommand
     order places `doctor` after `status`), `action_class == "read_only"`, and
     `apps.cli.commands.worker.COMMAND_HANDLERS["worker.doctor"]` is callable.
  G5 TARGETED TESTS — after C2:
     `python3 -m pytest tests/cli/test_worker.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py tests/test_command_discovery.py tests/cli/test_worker_facade_cmd.py tests/cli/test_golden_path.py -q`
     reads `237 passed` plus the 11 new `tests/cli/test_worker.py` nodes (so `248 passed` in
     total over that exact command line).
  G6 RUFF — after C2, `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/worker.py tests/cli/test_worker.py`
     reads `All checks passed!`.
  G7 MUTATION RED-PROOF (reachability of the new tests) — in a DISPOSABLE git worktree under
     `.remedy-wt/` only (never the primary checkout, never `/tmp`), at your own C2 commit:
     change `ready = len(blockers) == 0` to `ready = True` in
     `apps/cli/commands/worker.py::_cmd_worker_doctor`, then run
     `python3 -m pytest tests/cli/test_worker.py -q`. Report the exact count and the failing
     node ids (expect 5 of the 11 nodes red: `test_ollama_missing_from_path_is_a_blocker` and
     the four parametrized `test_an_available_spec_with_no_probe_fails_rather_than_passing_silently`
     cases). Revert your mutation, re-run the same command, report the second (green, `11
     passed`) result. Remove the disposable worktree yourself before your handback commit and
     confirm with `git worktree list`.
  G8 DOCS — `python3 -m pytest tests/docs/ -q` reads `310 passed` (unchanged from base — this
     round adds no new command to any doc's prose and no group).

Handback: completion report (state block, deviations, next steps) + rewrite
`.agent/handoff.md`. Attribute commits `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
Session number: this is SESSION 4 of F280, round 9.
──────────────────────────────────────────────────────────────
