── STEP T003 remaining deny rows — F085 — R65 ────────────────────────────────

Goal: finish the network posture's wiring. The two rows amendment F085 D1 still marks default-deny
— `dod-process` and `builder` — set `deny_network`, each pinned by a test in the file its own class
already owns, so all three bounded classes in that table now carry the posture R64 built. The R64
PASS is recorded in the same round, and the one finding that review raised is registered with its
counter-measure landing BEFORE the record that cites it.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 land checklist item 25 · C3 record the R64 PASS and register R-0560 · C4 wire the `dod-process`
row · C5 wire the `builder` row · C6 pin the `dod-process` row · C7 pin the `builder` row ·
C8 handback. That list runs past five commits, so the handback takes the ≤100-line cap AGENTS.md
allows when a per-commit table needs it.

CONVENTION, binding on every count here, carried verbatim in force from the R64 block. A line count
is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN19, CHECK25, DOD1,
DOD2, BUILD1, BUILD2 AND TESTBUILD; ITS END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE RECORD33
AND TESTDOD — listed rather than counted, per §3 checklist item 11. Each append slice CARRIES ITS OWN
LEADING BLANK LINES, so the separation its target's convention requires is a property of bytes that
were measured and never of a join shape that was reasoned about.

## Change

C1 applies PLAN19F→PLAN19T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep a stale
label. C2 applies CHECK25F→CHECK25T to `docs/agents/planner_reviewer_prompt.md`, adding item 25 to the
§3 checklist. C3 appends RECORD33 to the END of `.agent/live_review.md`. C4 applies DOD1 then DOD2, in
that order, to `packages/orchestration/exec_guard.py`. C5 applies BUILD1 then BUILD2, in that order, to
`packages/orchestration/managed_builder_execution.py`. C6 appends TESTDOD to the END of
`tests/orchestration/test_exec_guard.py`. C7 applies TESTBUILDF→TESTBUILDT to
`tests/orchestration/test_managed_builder_execution.py`, which is a REWRITE and not an append because
that file ends in `if __name__ == "__main__":` and its policy tests live in a class.

Change set, named rather than counted: `.agent/authored/f085-r65.md`, `.agent/last_block.md`,
`.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`, `.agent/live_review.md`,
`packages/orchestration/exec_guard.py`, `packages/orchestration/managed_builder_execution.py`,
`tests/orchestration/test_exec_guard.py`, `tests/orchestration/test_managed_builder_execution.py`,
`.agent/handoff.md`. Nothing else. NO `docs/roadmap/**` path is in that set, so the §3 docs tier does
NOT trigger and no `tests/docs/` gate is ordered; `docs/agents/**` is outside what `tests/docs/` reads.
FOUR `.py` paths ARE in it, so a lint gate and a red control ARE ordered. The three `runtime-server`
call sites R61 and R63 migrated — `packages/runtimes/dev_server.py`,
`packages/runtimes/runtime_supervisor.py` and `apps/cli/commands/runtime_cmd.py` — are NOT in the set
and this round must not touch them. All seven tracked paths named here were resolved on disk at
e5eecb29 with `git ls-tree`, one call per path, before emission, per checklist item 24, and all seven
exist.

The design reading a gate cannot recompute, taken from `docs/roadmap/features/T2_F085.md` at e5eecb29:
the amendment F085 D1 policy table's network column reads `default-deny` for the `builder`, `test` and
`dod-process` rows and for no other row, so C4 and C5 complete that column rather than extending it.
`dod-app` is deliberately NOT wired — its harness serves the network on its own port, which that same
file states — and the `test` row was wired at R64. DOD1T and BUILD1T carry that per-row reasoning into
the two docstrings, where a reader searching for it will land.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r65.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C8; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   e5eecb29 and prints its own output here per checklist item 15, one reading per pair:
   PLAN19F→PLAN19T `TO contains FROM: false`; CHECK25F→CHECK25T `TO contains FROM: false`;
   DOD1F→DOD1T `TO contains FROM: false`; DOD2F→DOD2T `TO contains FROM: false`;
   BUILD1F→BUILD1T `TO contains FROM: false`; BUILD2F→BUILD2T `TO contains FROM: false`;
   TESTBUILDF→TESTBUILDT `TO contains FROM: true`. The first six are therefore REWRITES and each owes
   the FROM 0x / TO 1x reading over its own post-commit file. TESTBUILD is APPEND-shaped, so the
   FROM-zero count is unattainable for it BY CONSTRUCTION and must NOT be reported: its obligation is
   FROM exactly 1x and TO exactly 1x in the post-commit blob, which is §4.9's append reading for a
   pair whose TO opens with its own FROM. Each FROM occurs EXACTLY 1x in its target at e5eecb29 — the
   reviewer measured all seven.
4. RECORD33 AND TESTDOD HAVE NO FROM. Each is appended at the END of its target. Their obligation is
   ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of the
   post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are
   exactly the slice's lines IN ORDER. Do not invent a FROM for either and do not report a FROM count.
   TESTDOD is CODE, so §4.9's per-line "each TO-ONLY addition exactly 1x" count does NOT bind it and
   must not be reported — ordered equality replaces it (R-0531).
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of every code commit. Only C0a
   and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. C2 LANDS BEFORE C3 ON PURPOSE. RECORD33 names item 25 of the §3 checklist as R-0560's
   counter-measure, so the item must already be on disk when the record that cites it is written —
   the ordering the R59 block used for item 24, and the reason a standing rule left in finding prose
   binds nothing (R-0452, R-0454).
7. Every sentence in RECORD33 that states a reading of a file names the SHA it was read at in the same
   clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to EVERY
   reading in the clause, not only the first. RECORD33 states readings of R64's range and of this
   round's base only, all of which are prior state, so every SHA it names already exists when it is
   written.
8. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD33 is reviewer text and carries the R-0560
   registration inside it. Do not add a `Landed:` line, do not add a `Done:` paragraph of your own,
   and do not edit RECORD33 to reconcile it with anything you measure. A disagreement between RECORD33
   and your own reading is a finding to REPORT in the handback, never to fix.
9. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES NOTHING. Registered moves 174 → 175, done
   stays 28, landed stays 0, open moves 146 → 147, and the next free id moves R-0560 → R-0561.
   RECORD33 carries exactly one `- R-` registration line and no `Done:` line, which is why the
   arithmetic moves in exactly that one place; G6 proves it.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r65.md`; a mismatch is a finding against this block, not the worker.
11. C4, C5, C6 AND C7 ARE SEPARATE COMMITS and land in that order. C4 and C5 each leave the suite
   green on their own — the reviewer verified both in a disposable worktree at e5eecb29 — so no
   commit in this round is knowingly red.
12. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, and never widen the
   change set to route around a red.
13. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. These suites spawn real supervisors that bind a port and leave escapees when a readiness
   assertion fails, so two concurrent runs redden each other on tests neither touched: at e26f1f3e the
   R63 gate suite read `1 failed, 304 passed` concurrent and `305 passed` at exit 0 serial.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. This round DOES order a destructive check (G8), so
`git worktree list` is one line at round start, one line again at the end, and the worktree G8 creates
is removed and pruned before the handback is written.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r65.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD33 line counts read
from that committed file, against constraint 10's 490 / 400 / 140.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN19F→PLAN19T is a REWRITE over `.agent/plan.md` at C1, CHECK25F→CHECK25T a REWRITE over
   `docs/agents/planner_reviewer_prompt.md` at C2: for each report its FROM 0x and its TO exactly 1x
   over the post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob must
   reproduce the post-commit blob BYTE-EXACTLY.
 - DOD1F→DOD1T and DOD2F→DOD2T are REWRITES over `packages/orchestration/exec_guard.py` at C4, and
   BUILD1F→BUILD1T and BUILD2F→BUILD2T are REWRITES over
   `packages/orchestration/managed_builder_execution.py` at C5: the same three readings each,
   measured over each file's own pre- and post-commit blobs, and for each file both of its pairs
   re-applied IN ORDER must reproduce the post-commit blob BYTE-EXACTLY.
 - TESTBUILDF→TESTBUILDT is APPEND-shaped over `tests/orchestration/test_managed_builder_execution.py`
   at C7: report FROM exactly 1x AND TO exactly 1x in the post-commit blob, NO FROM-zero count, and
   re-application reproducing the post-commit blob BYTE-EXACTLY.
 - For RECORD33 at C3 and TESTDOD at C6 report the ordered-equality readings constraint 4 names:
   pre-commit blob is a byte-exact PREFIX, the slice is an exact SUFFIX, `pre + slice` equals the
   post-commit blob byte for byte, and that commit's ADDED lines are exactly the slice's lines IN
   ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0, and serially per
constraint 13. Report each run's passed count; the counts are reported, never predicted, and only the
exit code is ordered. The reviewer took every base reading below itself, in the primary checkout, at
e5eecb29.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py tests/orchestration/test_test_runner.py
   tests/test_test_runner.py tests/orchestration/test_ci_run.py
   tests/orchestration/test_managed_builder_execution.py tests/orchestration/test_dod_runners.py
   -q -rf` — base `329 passed`, no skips: the readers of both seams C4 and C5 change.
 - `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
   tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
   base `160 passed`; two of them assert on `.agent/plan.md`, which C1 rewrites, and that is the whole
   reason this set is ordered.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected by
grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 40 lines by applying the pair to that blob at e5eecb29.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
e5eecb29 and at HEAD, from the line-start patterns for a registration, a resolution and a landed line.
The reviewer's base reading is 174 / 28 / 0, 146 open, max registered R-0559, max resolved R-0558. At
HEAD the reading must be 175 / 28 / 0, 147 open, max registered R-0560 and max resolved still R-0558,
because constraint 9 rules this round registers exactly one finding and resolves nothing. The
symmetric difference of the registered sets must be EXACTLY `{R-0560}` and the done and landed
symmetric differences must both be EMPTY. Next free id R-0561. Report all three symmetric differences,
the duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs.

G7 LINT, over the four `.py` paths this round edits, run from the repository root with the
repository's OWN configuration — no `--isolated`, per §3 checklist item 12. BOTH halves are green at
the base, so both are ordered GREEN rather than compared as multisets; the reviewer executed both at
e5eecb29 itself, per R-0364, and both printed `All checks passed!` over all four paths.
 - `python3 -m ruff check packages/orchestration/exec_guard.py
   packages/orchestration/managed_builder_execution.py tests/orchestration/test_exec_guard.py
   tests/orchestration/test_managed_builder_execution.py` — exit 0.
 - The same four paths again with `--preview` — exit 0. The preview half is ordered separately because
   ruff is preview-blind to the E301-E306 class that a code append most plausibly breaks (R-0500,
   R-0558).

G8 RED CONTROL, the ONLY destructive check this round, and ONLY inside a disposable `git worktree` at
HEAD under §4.10 — never in the primary checkout. In that worktree revert EXACTLY ONE thing: replace
the DOD2T bytes with the DOD2F bytes in `packages/orchestration/exec_guard.py`, which deletes the one
line `        deny_network=True,` from `dod_process_exec_policy` and changes nothing else, then re-run
`python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf`. The revert is ordered as a BYTE
PAIR over a NAMED path and not as a bare line because that bare line occurs FOUR times among the
`.py` files this round leaves behind — twice in `packages/orchestration/exec_guard.py`, once in
`packages/orchestration/managed_builder_execution.py` and once in
`tests/orchestration/test_exec_guard.py` — and twice more in each block mirror under `.agent/`, while
the DOD2T bytes occur exactly ONCE in `packages/orchestration/exec_guard.py`, which is item 25 of the
§3 checklist applied to this block's own control. Report the worktree's `git diff --stat`,
which must read `1 file changed, 1 deletion(-)`. The run must FAIL, and among the failures must be
`test_the_dod_process_policy_denies_the_network_its_row_denies` on its
`assert policy.deny_network is True` line. Report every failing test's full name and that asserted
line. Then remove and prune the worktree and confirm `git status --porcelain` empty in the primary
checkout.

G9 HYGIENE. `git diff --name-only e5eecb29..HEAD` measured BEFORE C8 holds exactly the change set
above minus `.agent/handoff.md`, which C8 writes, and nothing else — and in particular holds none of
`packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py` and
`apps/cli/commands/runtime_cmd.py`. Those three and the four `.py` paths this round edits were each
resolved at e5eecb29 with `git ls-tree e5eecb29 -- <path>`, one call per path, and all seven exist;
re-run those seven calls and report each result, per §3 checklist item 24. Report per-commit
insertions for every commit BEFORE C8 — C8 cannot measure itself, so its own go in the round report —
and confirm none exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at
d4473f85, so a second oversize commit is a STOP under constraint 12, never a declaration. Confirm
every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
e5eecb29, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3, C4,
C5, C6, C7 and C8, the real G1-G9 results with exit codes, the open-findings count and the next
expected action. The Bundle above holds more than five commits, so the ≤100-line cap applies; if the
mandated content genuinely does not fit even there, name the DECISION D15 stated cause and the
specific mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~99 % (T001 gebaut · R13-R64 PASS · T002 KOMPLETT — alle vier Klassen migriert ·
T003 fast fertig: alle drei default-deny-Zeilen der D1-Tabelle sind verdrahtet und gepinnt, offen
bleibt allein das Limitations-Dokument mit seinem README-Link) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R66 writes T003's
limitations document and its README link, stating what stage 1 does NOT prevent — a binary that
ignores proxy variables reaches the network anyway, an app log written to a file takes no guard output
cap, and the git, packaging and other classes never ran under the guard at all — after which the
integration gate and closure follow. TWO: R65 carries no verdict of its own, because the round that
records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R66
carries it. THREE: a standalone closing line stating the open findings count and the next free id.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires
every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN19F
## Current Step
R64, this round: T003 opens with the network posture itself. `exec_guard` gains a `deny_network`
policy field and a `DENIED_NETWORK_ENV` overlay written AFTER the allowlist scrub — the proxy
names are `FORBIDDEN_ENV_KEYS` members, so the floor would otherwise delete the posture — and the
`test` class, the largest deny row in amendment F085 D1's table, sets it. The R63 PASS is
recorded in the same round.

## Next Steps
1. Wire the remaining deny rows: `dod_process_exec_policy` in the same module and the builder
   policy in `managed_builder_execution`, each with the seam test its class already has.
2. T003's limitations document and its README link, stating what stage 1 does NOT prevent: a
   binary that ignores proxy variables reaches the network anyway, an app log written to a file
   takes no guard output cap, and the git, packaging and other classes never ran under the guard
   at all.
3. Then the integration gate, then closure.
END-PLAN19F

BEGIN-PLAN19T
## Current Step
R65, this round: the two deny rows amendment F085 D1 still leaves unwired take the posture R64
built. `dod_process_exec_policy` and `managed_builder_execution._builder_exec_policy` set
`deny_network=True`, each pinned by a test in the file its own class already owns, so all three
bounded rows of that table now deny. The R64 PASS is recorded and its one finding registered in
the same round, with the counter-measure landing ahead of the record.

## Next Steps
1. T003's limitations document and its README link, stating what stage 1 does NOT prevent: a
   binary that ignores proxy variables reaches the network anyway, an app log written to a file
   takes no guard output cap, and the git, packaging and other classes never ran under the guard
   at all.
2. Then the integration gate, then closure.
END-PLAN19T

BEGIN-CHECK25F
      Session Resume tells the next session to read.
  Why this is on disk and not a habit: item 2 has recurred six times across
END-CHECK25F

BEGIN-CHECK25T
      Session Resume tells the next session to read.
  25. **A destructive gate's revert target is named by PATH and is unique inside it.** Finding
      R-0560. A red control that orders a revert by quoting a LINE — "delete the single line `X`
      in `Y`" — names the FILE the revert is applied to, and the exact bytes it orders removed are
      counted IN THAT FILE at the SHA the control runs at, where the count must be 1. Naming only
      the enclosing function is not a measurement: the same line commonly occurs in a second
      source file and in the block mirrors under `.agent/`, and a reader who resolves that name to
      the wrong file reverts the wrong line while the run still goes red — which is exactly what
      the control cannot distinguish from its own success. Where the bytes recur inside the named
      file, the control orders a longer UNIQUE byte string instead. Item 24 resolves the paths a
      gate NAMES; this one resolves the BYTES a gate orders CHANGED.
  Why this is on disk and not a habit: item 2 has recurred six times across
END-CHECK25T

BEGIN-DOD1F
    allowlisted keys, and `FORBIDDEN_ENV_KEYS` remains the floor beneath it.
    """
END-DOD1F

BEGIN-DOD1T
    allowlisted keys, and `FORBIDDEN_ENV_KEYS` remains the floor beneath it.

    `deny_network=True` is amendment F085 D1's network column for this row: a DoD
    check is a bounded, project-authored command, so it takes the same proxy
    posture the `test` class takes, written after the scrub that would delete it.
    """
END-DOD1T

BEGIN-DOD2F
        env_allowlist=DOD_PROCESS_ENV_ALLOWLIST,
    )
END-DOD2F

BEGIN-DOD2T
        env_allowlist=DOD_PROCESS_ENV_ALLOWLIST,
        deny_network=True,
    )
END-DOD2T

BEGIN-BUILD1F
    the product of `_build_sanitized_env`, so allowlisting its keys reproduces it.
    """
END-BUILD1F

BEGIN-BUILD1T
    the product of `_build_sanitized_env`, so allowlisting its keys reproduces it.

    `deny_network=True` is amendment F085 D1's network column for the `builder` row.
    It is a PROXY posture and not a kernel one, so a build tool that honours proxy
    variables cannot reach the network while one that ignores them still can.
    """
END-BUILD1T

BEGIN-BUILD2F
        env_allowlist=tuple(sorted(env)),
        core_file_bytes=0,
    )
END-BUILD2F

BEGIN-BUILD2T
        env_allowlist=tuple(sorted(env)),
        core_file_bytes=0,
        deny_network=True,
    )
END-BUILD2T

BEGIN-TESTDOD


def test_the_dod_process_policy_denies_the_network_its_row_denies():
    """Amendment F085 D1's network column for the `dod-process` row, in code."""
    policy = exec_guard.dod_process_exec_policy(45, "/tmp/dod-cwd")

    assert policy.deny_network is True
    child_env = exec_guard.plan_child_spawn(policy).env
    assert dict(exec_guard.DENIED_NETWORK_ENV).items() <= child_env.items()
END-TESTDOD

BEGIN-TESTBUILDF
        smuggled = dict(env, GITHUB_TOKEN="ghp_never")
        floored = _builder_exec_policy(30, 4096, None, smuggled)
        assert "GITHUB_TOKEN" not in scrub_child_env(smuggled, floored.env_allowlist)
END-TESTBUILDF

BEGIN-TESTBUILDT
        smuggled = dict(env, GITHUB_TOKEN="ghp_never")
        floored = _builder_exec_policy(30, 4096, None, smuggled)
        assert "GITHUB_TOKEN" not in scrub_child_env(smuggled, floored.env_allowlist)

    def test_the_builder_policy_denies_the_network_its_row_denies(self):
        """Amendment F085 D1's network column for the `builder` row, in code."""
        from packages.orchestration.exec_guard import (
            DENIED_NETWORK_ENV,
            plan_child_spawn,
        )
        from packages.orchestration.managed_builder_execution import _builder_exec_policy
        env = _build_sanitized_env({})
        policy = _builder_exec_policy(30, 4096, None, env)
        assert policy.deny_network is True
        child_env = plan_child_spawn(policy).env
        assert dict(DENIED_NETWORK_ENV).items() <= child_env.items()
        assert all(child_env[key] == value for key, value in env.items())
END-TESTBUILDT

BEGIN-RECORD33

Gate: R65 — the R64 entry. R64 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer over
e26f1f3e..e5eecb29, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing and declared nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD, disk-to-disk
with no digest fallback: the committed `.agent/authored/f085-r64.md` and the committed
`.agent/last_block.md` at e5eecb29, both working copies as they stand at e5eecb29, and the received
`.remedy-wt/f085-r64.md` are all five byte-EQUAL at sha256
670a2563e54daff38b815a445493dba8b417024e65c5eba4e0b9cbcdb8ae2108, 31314 B, 490 lines, 32 marker lines.
THE SHAPES HELD, and the two classes were measured apart, one reading per pair. PLAN18F→PLAN18T over
`.agent/plan.md` at a8877d26, GUARD1F→GUARD1T and GUARD6F→GUARD6T over
`packages/orchestration/exec_guard.py` at 01fd653d are REWRITES — each containment test reads
`TO contains FROM: false` — and each ends FROM 0x with TO exactly 1x, each FROM having occurred
exactly 1x in its own pre-commit blob. GUARD2, GUARD3, GUARD4 and GUARD5 are APPEND-shaped over that
same file at 01fd653d, each reading FROM exactly 1x AND TO exactly 1x post-commit with no FROM-zero
reading taken, and all six GUARD pairs re-applied IN ORDER to the pre-commit blob reproduce the
post-commit blob BYTE-EXACTLY. RECORD32 over `.agent/live_review.md` at 2e6b772e and TESTNET over
`tests/orchestration/test_exec_guard.py` at 25c75325, neither of which has a FROM, satisfy ORDERED
EQUALITY on every clause: pre-commit blob a byte-exact PREFIX, slice an exact SUFFIX, `pre + slice`
equal to the post-commit blob byte for byte, and each commit's ADDED lines equal to the slice's lines
IN ORDER — 64 and 64, 57 and 57, numstat `64 0` and `57 0`. Marker LINES at e5eecb29 are 0 in each of
the four edited files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with that block's
exact command lines, serially, each exit 0: `329 passed` against a base of `324 passed` for the seam
set, C4's five new tests being the difference; `160 passed` against a base of `160 passed` for the
four state readers; and the canary `42 passed` against a base of `42 passed`. THE PLAN CONTRACT HELD
at e5eecb29: 42 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present, 42 being that block's own projection. THE ARITHMETIC DID NOT MOVE, as that block's
constraint 8 required: 174 registered / 28 done / 0 landed and 146 open at e26f1f3e, the same three
numbers and the same 146 at e5eecb29, max registered R-0559 and max resolved R-0558 at both, all
three symmetric differences EMPTY, and 0 duplicate ids and 0 orphan resolutions at both SHAs. LINT
WAS RE-RUN over both `.py` paths from the repository root with the repository's own configuration,
plain and `--preview`, each exit 0 with `All checks passed!`. THE RED CONTROL REPRODUCED EXACTLY
inside a disposable worktree at 25c75325: deleting the one line `        deny_network=True,` from
`test_command_exec_policy` in `packages/orchestration/exec_guard.py` — a worktree `git diff --stat` of
`1 file changed, 1 deletion(-)` and nothing else — turned
`python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` red at exit 1 with
`2 failed, 39 passed`, failing both
`test_the_test_class_policy_denies_the_network_its_row_denies`, the one that block ordered, and
`test_a_denied_child_really_receives_the_closed_port` on its
`assert dumped["HTTP_PROXY"] == exec_guard.DENIED_NETWORK_PROXY_URL` line with `KeyError: 'HTTP_PROXY'`
— the second being the real-child half of the same one-line revert, which that handback reported
rather than concealed. HYGIENE IS CLEAN: the path set over e26f1f3e..e5eecb29 is exactly the seven the
change set named and holds none of the three `runtime-server` paths; all five paths G9 orders resolved
at e26f1f3e under `git ls-tree`; per-commit INSERTIONS are 490, 419, 12, 64, 39, 57 and 32 for the
handback commit, none over 500; all seven commits are single-parent. THE BLOCK'S OWN SIZE re-measured
from the committed file at e5eecb29 gives TOTAL 490, PROSE 274 counting its 32 marker lines and
RECORD32 64, agreeing with that block's own figures and inside 490 / 400 / 140. ONE FINDING IS
REGISTERED AGAINST THAT BLOCK'S OWN GATE TEXT, and it is the reviewer's defect rather than the
worker's, which is why R64 still PASSES.

- R-0560 — Low — the R64 block's G8 ordered a destructive revert by quoting a line that was not unique
in the tree at the SHA the control runs at. It ordered "revert EXACTLY ONE thing: the single line
`        deny_network=True,` in `test_command_exec_policy`", and at 25c75325 those exact bytes occur
TWICE: once in `packages/orchestration/exec_guard.py`, which is where `test_command_exec_policy` is
defined, and once in `tests/orchestration/test_exec_guard.py`, which TESTNET appended in the same
round. The qualifier that disambiguates them is the function name, and that name begins with `test_`,
so it reads as a pointer INTO the test file for anyone who has not already resolved the symbol. The
reviewer of this round deleted the wrong occurrence on the first attempt, restored the file and
re-ran, so the cost is measured rather than hypothetical. This is the vacuous-and-ambiguous gate
family of R-0438, R-0532 and R-0559 arriving through the BYTES a gate orders changed rather than
through the paths it names: item 24 would have resolved every path in that sentence and still passed
it, because both paths exist. R64 PASSES anyway — the control was met, the deletion that was finally
made was the ordered one, the `1 file changed, 1 deletion(-)` reading in the handback is the correct
one, and the red it produced is the red the block predicted. The danger is that a red control cannot
tell a wrong revert from a right one: deleting the TESTNET occurrence also reddens that suite, so a
reader who never noticed the ambiguity would have reported a green-looking control that proved
nothing about `test_command_exec_policy`. COUNTER-MEASURE: item 25 of the §3 checklist in
`docs/agents/planner_reviewer_prompt.md`, which constraint 6 of this block fixes as landing in the
commit BEFORE this record — a revert target is named by the PATH it is applied to and its exact bytes
are counted IN THAT FILE at the SHA the control names, a count above 1 forcing a longer unique string.
The rule is promoted into the checklist rather than left in this paragraph, because a standing rule
written as finding prose binds nothing and recurs (R-0452, R-0454). OPEN.
END-RECORD33
