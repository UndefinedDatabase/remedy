── STEP T003 network posture — F085 — R64 ────────────────────────────────────

Goal: open T003 by building the network posture. `exec_guard` gains a `deny_network` policy field
and a `DENIED_NETWORK_ENV` overlay written AFTER the allowlist scrub, and the `test` class — the
largest deny row in amendment F085 D1's policy table — sets it, so a guarded test command's
toolchain can no longer reach the network through a proxy it honours. The R63 PASS is recorded in
the same round, because a round cannot record a verdict on itself (§4.13).

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record the R63 PASS · C3 build the posture in `exec_guard.py` · C4 add the
tests · C5 handback. That list runs past C0a, C0b, C1, C2, C3, C4 to C5, so it holds MORE than
five commits and the handback takes the ≤100-line cap AGENTS.md allows when a per-commit table
needs it.

CONVENTION, binding on every count here, carried verbatim in force from the R63 block. A line
count is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES
STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST
CONTENT LINE: extract it as everything after the `BEGIN-` line's own newline up to and including
the newline immediately before the `END-` line, so that `pre + slice` is already a
newline-terminated file and NO joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO
PAIRS ARE PLAN18, GUARD1, GUARD2, GUARD3, GUARD4, GUARD5 AND GUARD6; ITS END-OF-FILE APPENDS,
WHICH HAVE NO FROM AT ALL, ARE TESTNET AND RECORD32 — listed rather than counted, per §3
checklist item 11. Each append slice CARRIES ITS OWN LEADING BLANK LINES, so the separation its
target's convention requires is a property of bytes that were measured and never of a join shape
that was reasoned about.

## Change

C1 applies PLAN18F→PLAN18T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can
keep a stale label. C2 appends RECORD32 to the END of `.agent/live_review.md`. C3 applies GUARD1
through GUARD6, in that order, to `packages/orchestration/exec_guard.py`. C4 appends TESTNET to
the END of `tests/orchestration/test_exec_guard.py`.

Change set, named rather than counted: `.agent/authored/f085-r64.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/exec_guard.py`,
`tests/orchestration/test_exec_guard.py`, `.agent/handoff.md`. Nothing else. NO `docs/roadmap/**`
path is in that set, so the §3 docs tier does NOT trigger and no `tests/docs/` gate is ordered.
TWO `.py` paths ARE in it, so a lint gate and a red control ARE ordered. The three
`runtime-server` call sites R61 and R63 migrated — `packages/runtimes/dev_server.py`,
`packages/runtimes/runtime_supervisor.py` and `apps/cli/commands/runtime_cmd.py` — are NOT in the
set and this round must not touch them. All five paths named here were resolved on disk at
e26f1f3e with `git ls-tree`, one call per path, before emission, per checklist item 24, and all
five exist.

The `dod-process` and builder rows also carry default-deny in the D1 table and are NOT wired
here; PLAN18T records why and what follows. The one design reading a gate cannot recompute:
`HTTP_PROXY`, `HTTPS_PROXY` and `ALL_PROXY` are `FORBIDDEN_ENV_KEYS` members, read in
`packages/orchestration/exec_guard.py` at e26f1f3e, so the overlay cannot travel through an
allowlist — the floor would delete it. GUARD2T and GUARD5T carry that reasoning into the code
itself, where a reader searching for it will land, and TESTNET pins the ordering.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r64.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   e26f1f3e and prints its own output here per checklist item 15, one reading per pair:
   PLAN18F→PLAN18T `TO contains FROM: false`; GUARD1F→GUARD1T `TO contains FROM: false`;
   GUARD2F→GUARD2T `TO contains FROM: true`; GUARD3F→GUARD3T `TO contains FROM: true`;
   GUARD4F→GUARD4T `TO contains FROM: true`; GUARD5F→GUARD5T `TO contains FROM: true`;
   GUARD6F→GUARD6T `TO contains FROM: false`. PLAN18, GUARD1 and GUARD6 are therefore REWRITES
   and each owes the FROM 0x / TO 1x reading over its own post-commit file. GUARD2, GUARD3,
   GUARD4 and GUARD5 are APPEND-shaped, so the FROM-zero count is unattainable for them BY
   CONSTRUCTION and must NOT be reported: their obligation is FROM exactly 1x and TO exactly 1x
   in the post-commit blob, which is §4.9's append reading for a pair whose TO opens with its own
   FROM. Each FROM occurs EXACTLY 1x in its target at e26f1f3e — the reviewer measured all seven.
4. TESTNET AND RECORD32 HAVE NO FROM. Each is appended at the END of its target. Their obligation
   is ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX
   of the post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff
   ADDS are exactly the slice's lines IN ORDER. Do not invent a FROM for either and do not report
   a FROM count. TESTNET is CODE, so §4.9's per-line "each TO-ONLY addition exactly 1x" count
   does NOT bind it and must not be reported — ordered equality replaces it (R-0531).
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of both code commits. Only
   C0a and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23
   binds it.
6. Every sentence in RECORD32 that states a reading of a file names the SHA it was read at in the
   same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to
   EVERY reading in the clause, not only the first. RECORD32 states readings of R63's range only,
   all of which are prior state, so every SHA it names already exists when it is written.
7. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD32 is reviewer text. Do not add a
   `Landed:` line, do not add a `Done:` paragraph of your own, and do not edit RECORD32 to
   reconcile it with anything you measure. A disagreement between RECORD32 and your own reading
   is a finding to REPORT in the handback, never to fix.
8. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. The reviewer re-executed every R63 gate and
   found nothing to register. Registered stays 174, done stays 28, landed stays 0, open stays
   146, and the next free id stays R-0560. RECORD32 is a `Gate:` paragraph and carries no `- R-`
   registration line and no `Done:` line, which is why the arithmetic must not move; G6 proves it.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on
   the final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r64.md`; a mismatch is a finding against this block, not the worker.
10. C3 AND C4 ARE SEPARATE COMMITS and land in that order. C3 alone leaves the suite green — the
   reviewer verified that in a disposable worktree at e26f1f3e — so neither commit is knowingly
   red.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never
   widen the change set to route around a red.
12. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any
   checkout or worktree. These suites spawn real supervisors that bind a port and leave escapees
   when a readiness assertion fails, so two concurrent runs redden each other on tests neither
   touched: at e26f1f3e the R63 gate suite read `1 failed, 304 passed` concurrent and
   `305 passed` at exit 0 serial.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty
at round start and after every commit. This round DOES order a destructive check (G8), so
`git worktree list` is one line at round start, one line again at the end, and the worktree G8
creates is removed and pruned before the handback is written.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r64.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line
count and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD32 line
counts read from that committed file, against constraint 9's 490 / 400 / 140.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN18F→PLAN18T is a REWRITE over `.agent/plan.md` at C1: report its FROM 0x and its TO
   exactly 1x over the post-commit blob, and re-applying the extracted FROM→TO to the pre-commit
   blob must reproduce the post-commit blob BYTE-EXACTLY.
 - GUARD1F→GUARD1T and GUARD6F→GUARD6T are REWRITES over
   `packages/orchestration/exec_guard.py` at C3: the same three readings each, measured over that
   file's own pre- and post-commit blobs.
 - GUARD2, GUARD3, GUARD4 and GUARD5 are APPEND-shaped over that same file at C3: report FROM
   exactly 1x AND TO exactly 1x in the post-commit blob, and NO FROM-zero count for any of them.
   For all six GUARD pairs together, re-applying them IN ORDER to the pre-commit blob must
   reproduce the post-commit blob BYTE-EXACTLY — the reading that proves no pair was reflowed.
 - For RECORD32 at C2 and TESTNET at C4 report the ordered-equality readings constraint 4 names:
   pre-commit blob is a byte-exact PREFIX, the slice is an exact SUFFIX, `pre + slice` equals the
   post-commit blob byte for byte, and that commit's ADDED lines are exactly the slice's lines IN
   ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0, and serially
per constraint 12. Report each run's passed count; the counts are reported, never predicted, and
only the exit code is ordered. The reviewer took every base reading below itself, in the primary
checkout, at e26f1f3e.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py
   tests/orchestration/test_test_runner.py tests/test_test_runner.py
   tests/orchestration/test_ci_run.py tests/orchestration/test_managed_builder_execution.py
   tests/orchestration/test_dod_runners.py -q -rf` — base `324 passed`, no skips: the readers of
   the seam C3 changes, since `test_command_exec_policy` reaches every one of them.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — base `160 passed`; two of them assert on
   `.agent/plan.md`, which C1 rewrites, and that is the whole reason this set is ordered.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains
`## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the
three booleans. The reviewer projected 42 lines by applying the pair to that blob at e26f1f3e.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
e26f1f3e and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 174 / 28 / 0, 146 open, max registered R-0559, max resolved
R-0558. At HEAD the reading must be IDENTICAL — 174 / 28 / 0, 146 open, same two maxima — and all
three symmetric differences must be EMPTY, because constraint 8 rules this round registers and
resolves nothing. Next free id R-0560. Report all three symmetric differences, the duplicate-id
count and the count of resolutions naming an unregistered id, at both SHAs.

G7 LINT, over the two `.py` paths this round edits, run from the repository root with the
repository's OWN configuration — no `--isolated`, per §3 checklist item 12. BOTH halves are green
at the base, so both are ordered GREEN rather than compared as multisets; the reviewer executed
both at e26f1f3e itself, per R-0364, and both printed `All checks passed!`.
 - `python3 -m ruff check packages/orchestration/exec_guard.py
   tests/orchestration/test_exec_guard.py` — exit 0.
 - `python3 -m ruff check --preview packages/orchestration/exec_guard.py
   tests/orchestration/test_exec_guard.py` — exit 0. The preview half is ordered separately
   because ruff is preview-blind to the E301-E306 class that a code append most plausibly breaks
   (R-0500, R-0558).

G8 RED CONTROL, the ONLY destructive check this round, and ONLY inside a disposable `git
worktree` at HEAD under §4.10 — never in the primary checkout. In that worktree revert EXACTLY
ONE thing: the single line `        deny_network=True,` in `test_command_exec_policy`, deleting
that one line and changing nothing else, then re-run
`python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf`. The run must FAIL, and among
the failures must be `test_the_test_class_policy_denies_the_network_its_row_denies` on its
`assert policy.deny_network is True` line. Report every failing test's full name and that
asserted line. The reviewer ran this control itself at emission and saw exactly that, and
separately ran the un-reverted file 10 times, all 10 green, so the colour is ordered rather than
probed (the stability rule the F085 R6 lesson fixed). Then remove and prune the worktree and
confirm `git status --porcelain` empty in the primary checkout.

G9 HYGIENE. `git diff --name-only e26f1f3e..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular holds none
of `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py` and
`apps/cli/commands/runtime_cmd.py`. Those three and the two `.py` paths this round edits were
each resolved at e26f1f3e with `git ls-tree e26f1f3e -- <path>`, one call per path, and all five
exist; re-run those five calls and report each result, per §3 checklist item 24. Report
per-commit insertions for every commit BEFORE C5 — C5 cannot measure itself, so its own go in the
round report — and confirm none exceeds 500. This branch spent the AGENTS.md declared-oversize
allowance at d4473f85, so a second oversize commit is a STOP under constraint 11, never a
declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA e26f1f3e, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2,
C3, C4 and C5, the real G1-G9 results with exit codes, the open-findings count and the next
expected action. The Bundle above holds more than five commits, so the ≤100-line cap applies; if
the mandated content genuinely does not fit even there, name the DECISION D15 stated cause and
the specific mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~99 % (T001 gebaut · R13-R63 PASS · T002 KOMPLETT — alle vier Klassen migriert ·
T003 begonnen: die Netz-Policy steht im Guard und die `test`-Klasse verweigert das Netz, die
restlichen deny-Zeilen und das Limitations-Dokument sind offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R65 wires the
remaining deny rows — `dod_process_exec_policy` in `packages/orchestration/exec_guard.py` and the
builder policy in `packages/orchestration/managed_builder_execution.py` — each with the seam test
its own class already has; T003's limitations document and its README link follow. TWO: R64
carries no verdict of its own, because the round that records a verdict cannot record one on
itself (docs/agents/planner_reviewer_prompt.md §4.13); R65 carries it. THREE: a standalone
closing line stating the open findings count and the next free id. FOUR: `Phase 1 rule 1 first:
re-read `.agent/STOP` from disk`, which the self-drive protocol requires every handoff naming a
next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN18F
## Current Step
R63, this round: the LAST `runtime-server` call site, `apps/cli/commands/runtime_cmd.py`, takes
`plan_child_spawn`, so the Remedy supervisor the CLI launches inherits the allowlist plus the
three `REMEDY_*` keys it declares and nothing else. A test pins that handover at the `Popen`
seam, which is the only place it can be observed. The R62 PASS is recorded in the same round.

## Next Steps
1. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
2. Then the integration gate, then closure.
END-PLAN18F

BEGIN-PLAN18T
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
END-PLAN18T

BEGIN-GUARD1F
- No network posture and no filesystem fence; both are T003.
END-GUARD1F

BEGIN-GUARD1T
- No filesystem fence; it is T003's remaining half. The network posture EXISTS since T003 for
  the classes whose policy sets `deny_network`, and it is a PROXY posture and never a kernel
  one: it points a child's proxy variables at a closed loopback port, so a toolchain that
  HONOURS those variables cannot reach the network while a binary that ignores them still can.
  Stage 2 closes that gap; stage 1 raises the bar and declines to call it containment.
END-GUARD1T

BEGIN-GUARD2F
TEST_COMMAND_OUTPUT_CAP_BYTES: int = 16 * 1024 * 1024
END-GUARD2F

BEGIN-GUARD2T
TEST_COMMAND_OUTPUT_CAP_BYTES: int = 16 * 1024 * 1024

#: WHY the RFC 863 discard port on loopback: nothing listens there, so a connect is REFUSED at
#: once rather than hanging a build behind a routing black hole.
DENIED_NETWORK_PROXY_URL: str = "http://127.0.0.1:9"

#: WHY written AFTER the allowlist scrub and never through an allowlist: these names are
#: `FORBIDDEN_ENV_KEYS` members and the floor is not a policy's to lift. The floor denies the
#: PARENT's proxy, which may carry credentials; these values are the guard's own and are
#: inherited from nobody. Both cases are set because toolchains disagree about spelling, and
#: `NO_PROXY` is EMPTY so no host is exempt from the deny.
DENIED_NETWORK_ENV: tuple[tuple[str, str], ...] = (
    ("ALL_PROXY", DENIED_NETWORK_PROXY_URL),
    ("HTTPS_PROXY", DENIED_NETWORK_PROXY_URL),
    ("HTTP_PROXY", DENIED_NETWORK_PROXY_URL),
    ("NO_PROXY", ""),
    ("all_proxy", DENIED_NETWORK_PROXY_URL),
    ("http_proxy", DENIED_NETWORK_PROXY_URL),
    ("https_proxy", DENIED_NETWORK_PROXY_URL),
    ("no_proxy", ""),
)
END-GUARD2T

BEGIN-GUARD3F
    env_allowlist: tuple[str, ...] | None = None
END-GUARD3F

BEGIN-GUARD3T
    env_allowlist: tuple[str, ...] | None = None
    #: WHY the field lives here and not in a caller: the deny must survive the allowlist scrub,
    #: and `plan_child_spawn` is the only place that sees the environment after it. True
    #: overlays `DENIED_NETWORK_ENV`; the D1 policy table's network column decides it per class.
    deny_network: bool = False
END-GUARD3T

BEGIN-GUARD4F
    The environment follows the module's rule exactly: `policy.env` reaches the
    child UNCHANGED — including `None`, which means "inherit" — while
    `env_allowlist` is None, and is rebuilt by `scrub_child_env` when it is not.
END-GUARD4F

BEGIN-GUARD4T
    The environment follows the module's rule exactly: `policy.env` reaches the
    child UNCHANGED — including `None`, which means "inherit" — while
    `env_allowlist` is None, and is rebuilt by `scrub_child_env` when it is not.
    `deny_network` then overlays `DENIED_NETWORK_ENV` on whatever that produced,
    after the scrub and never before it, so a denied child inherits what its
    policy allows PLUS the posture.
END-GUARD4T

BEGIN-GUARD5F
    child_env = policy.env
    if policy.env_allowlist is not None:
        child_env = scrub_child_env(
            os.environ if policy.env is None else policy.env, policy.env_allowlist
        )
END-GUARD5F

BEGIN-GUARD5T
    child_env = policy.env
    if policy.env_allowlist is not None:
        child_env = scrub_child_env(
            os.environ if policy.env is None else policy.env, policy.env_allowlist
        )
    if policy.deny_network:
        # AFTER the scrub on purpose: these keys are `FORBIDDEN_ENV_KEYS` members, so a scrub
        # running later would delete the very posture this sets. `None` means "inherit", and a
        # denied child inherits the parent environment PLUS the deny.
        child_env = dict(os.environ if child_env is None else child_env)
        child_env.update(DENIED_NETWORK_ENV)
END-GUARD5T

BEGIN-GUARD6F
        env_allowlist=(
            TEST_COMMAND_ENV_ALLOWLIST + tuple(extra_env_keys) + tuple(sorted(overlay))
        ),
    )
END-GUARD6F

BEGIN-GUARD6T
        env_allowlist=(
            TEST_COMMAND_ENV_ALLOWLIST + tuple(extra_env_keys) + tuple(sorted(overlay))
        ),
        deny_network=True,
    )
END-GUARD6T

BEGIN-TESTNET


def test_a_denied_policy_points_every_proxy_spelling_at_the_closed_port():
    """The posture is proxy-shaped: both spellings set, and no host exempted."""
    child_env = exec_guard.plan_child_spawn(exec_guard.ExecGuardPolicy(
        env={"PATH": "/usr/bin"}, deny_network=True,
    )).env

    for key, value in exec_guard.DENIED_NETWORK_ENV:
        assert child_env[key] == value
    assert child_env["HTTP_PROXY"] == "http://127.0.0.1:9"   # the literal, not the constant
    assert child_env["no_proxy"] == ""
    assert child_env["PATH"] == "/usr/bin"


def test_the_deny_survives_the_scrub_that_forbids_those_very_keys():
    """The ordering property: the floor drops the PARENT's proxy, and the guard's own
    value is written after that floor has run rather than before it."""
    child_env = exec_guard.plan_child_spawn(exec_guard.ExecGuardPolicy(
        env={"PATH": "/usr/bin", "HTTP_PROXY": "http://corp.example:3128"},
        env_allowlist=("PATH", "HTTP_PROXY"),
        deny_network=True,
    )).env

    assert child_env["HTTP_PROXY"] == exec_guard.DENIED_NETWORK_PROXY_URL
    assert "corp.example" not in child_env["HTTP_PROXY"]


def test_a_policy_that_does_not_deny_carries_no_proxy_variable_at_all():
    """The default is off, and off means ABSENT rather than empty."""
    child_env = exec_guard.plan_child_spawn(exec_guard.ExecGuardPolicy(
        env={"PATH": "/usr/bin"}, env_allowlist=("PATH",),
    )).env

    assert child_env == {"PATH": "/usr/bin"}
    assert not set(dict(exec_guard.DENIED_NETWORK_ENV)) & set(child_env)


def test_the_test_class_policy_denies_the_network_its_row_denies():
    """Amendment F085 D1's network column for the `test` row, in code."""
    policy = exec_guard.test_command_exec_policy(60, "/tmp")

    assert policy.deny_network is True


@pytest.mark.subprocess
def test_a_denied_child_really_receives_the_closed_port(monkeypatch):
    """A real child, through the seam, dumps the posture it actually inherited."""
    monkeypatch.setenv("HTTP_PROXY", "http://corp.example:3128")

    result = run_guarded_test_command(_child(_ENV_DUMP), timeout_sec=30, cwd=None)
    dumped = _dumped(result)

    assert result.returncode == 0
    assert dumped["HTTP_PROXY"] == exec_guard.DENIED_NETWORK_PROXY_URL
    assert dumped["no_proxy"] == ""
    assert b"corp.example" not in result.stdout
END-TESTNET

BEGIN-RECORD32

Gate: R64 — the R63 entry. R63 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over cbe1b3e5..e26f1f3e, not read, and each reproduces the handback's reading exactly; the worker
deviated in nothing and declared nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD,
disk-to-disk with no digest fallback, though NOT against a reviewer scratchpad original: R63 was
authored by an earlier session and this one holds no original of it, so the comparison ran across
the six copies that do exist — the committed `.agent/authored/f085-r63.md` at 28dd3923 and at
e26f1f3e, the committed `.agent/last_block.md` at 9a8e3161 and at e26f1f3e, and both working
copies as they stand at e26f1f3e — all six byte-EQUAL at sha256
b9230558fafe431bc69a62dadd059d93c1977510d53baceb817e7ef0a71c1d29, 26177 B, 373 lines, 12 marker
lines. What binds that block's CONTENT is the shape proof rather than the digest, and it held.
THE SHAPES HELD, and the two classes were measured apart, one reading per pair. PLAN17F→PLAN17T
over `.agent/plan.md` at 87c467db and SITE4F→SITE4T over `apps/cli/commands/runtime_cmd.py` at
a045970b are both REWRITES — each containment test reads `TO contains FROM: false` — and each
ends FROM 0x with TO exactly 1x, each FROM having occurred exactly 1x in its own target at
9a8e3161 and at 1d1c6abc respectively, with re-application of the extracted pair to the
pre-commit blob reproducing the post-commit blob BYTE-EXACTLY in both cases.
RECORD31 and TESTCLI, neither of which has a FROM, satisfy ORDERED EQUALITY on every clause:
RECORD31 over `.agent/live_review.md` at 1d1c6abc and TESTCLI over
`tests/cli/test_runtime_cmd.py` at 394c45af each have the pre-commit blob as a byte-exact PREFIX,
the slice as an exact SUFFIX, `pre + slice` equal to the post-commit blob byte for byte, and that
commit's ADDED lines equal to the slice's lines IN ORDER — 39 and 39, 42 and 42, numstat `39 0`
and `42 0`. Marker LINES at e26f1f3e are 0 in each of the four edited files. THE SUITES WERE
RE-RUN, NOT READ, in the primary checkout with that block's exact command lines, each exit 0:
`305 passed` against a base of `304 passed` for the migration set, C4's one new test being the
difference; `160 passed` against a base of `160 passed` for the four state readers; and the
canary `42 passed` against a base of `42 passed`. ONE READING HAD TO BE TAKEN TWICE, recorded
because it will recur: run concurrently with a second pytest process over the same file, the
migration set read `1 failed, 304 passed` and blamed
`test_an_instance_id_that_changes_during_the_request_is_never_healthy`, while serially and alone
it read `305 passed` at exit 0. These suites spawn real supervisors that bind a port and leave
escapees when a readiness assertion fails, so concurrency alone reddens tests neither run
touched; the serial reading is the honest one. THE PLAN CONTRACT HELD at e26f1f3e: 39 lines
against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all present, 39 being
that block's own projection. THE ARITHMETIC DID NOT MOVE, as constraint 8 required: 174
registered / 28 done / 0 landed and 146 open at cbe1b3e5, the same three numbers and the same 146
at e26f1f3e, max registered R-0559 and max resolved R-0558 at both, all three symmetric
differences EMPTY, and 0 duplicate ids and 0 orphan resolutions at both SHAs. LINT WAS RE-RUN over
both `.py` paths from the repository root with the repository's own configuration, plain and
`--preview`, each exit 0 with `All checks passed!`. THE RED CONTROL REPRODUCED EXACTLY inside a
disposable worktree at e26f1f3e: reverting only `cwd=spawn_plan.cwd, env=spawn_plan.env,` to
`cwd=str(source_root), env=env,` — a one-line worktree diff and nothing else — turned
`python3 -m pytest tests/cli/test_runtime_cmd.py -q -rf` from `17 passed` at exit 0 into
`1 failed, 16 passed` at exit 1, failing
`TestTheSupervisorEnvironmentIsScrubbed::test_a_secret_parent_variable_never_reaches_the_supervisor`
on its `assert "ANTHROPIC_API_KEY" not in env` line with the secret present in the reported
environment; that un-reverted baseline of `17 passed` also confirms C4 added exactly one test to
a file whose base was 16. HYGIENE IS CLEAN: the path set over cbe1b3e5..e26f1f3e is exactly the
seven the change set named; all four paths G9 orders resolved at cbe1b3e5 under `git ls-tree`;
per-commit INSERTIONS are 373, 287, 6, 39, 18, 42 and 46 for the handback commit, none over 500;
all seven commits are single-parent; and `.agent/handoff.md` at e26f1f3e is 75 lines, within the
≤100-line cap its seven-commit table allows, with the ordered Fortschritt line present verbatim.
THE BLOCK'S OWN SIZE re-measured from the committed file at e26f1f3e gives TOTAL 373, PROSE 226
counting its 12 marker lines and RECORD31 39, agreeing with that block's own figures and under
490 / 400 / 140. ONE CLAIM NO GATE COVERED WAS CHECKED RATHER
THAN ACCEPTED: RECORD31's assertion that `PYTHONPATH` and `VIRTUAL_ENV` need no declaration holds
at e26f1f3e, where `packages/orchestration/exec_guard.py` assigns
`RUNTIME_SERVER_ENV_ALLOWLIST` from `TEST_COMMAND_ENV_ALLOWLIST` and that tuple lists both keys.
ONE STATE OBSERVATION IS RECORDED AND IS NOT A WORKER DEVIATION: a disposable worktree
`.remedy-wt/rv63` existed at review time, created after the handback commit e26f1f3e by a
reviewer session that did not survive to remove it and holding a clean tree at that commit; the
reviewer used it for the red control above, then removed and pruned it, leaving `git worktree
list` at one line and `git status --porcelain` empty in the primary checkout. NOTHING FAILED and
this round registers no finding.
END-RECORD32
