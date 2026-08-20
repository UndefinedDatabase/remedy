── STEP T002d environment question — F085 — R56 ──────────────────────────────

Goal: settle the npm environment question `.agent/plan.md` carries as a risk, which the R55 PASS
ordered R56 to answer BEFORE any call site migrates. The `runtime-build` allowlist row is widened
from the bare `test` set to the npm and node CONFIGURATION keys a build actually reads, each key
named IN FULL so that no credential spelled `NPM_CONFIG_*` passes with them, and two tests pin
both halves. NO call site migrates in this round. The R55 PASS is recorded in the same round.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R55 · C3 widen the row and ship its two tests · C4 handback. That is
SIX ordered commits, which is more than five, so the handback carries the ≤100-line allowance
rather than the ≤60-line cap.

CONVENTION, binding on every count here, carried verbatim in force from the R55 block because it is
the R-0556 counter-measure. A line count is the `splitlines` reading — a trailing newline is NOT an
extra line. A SLICE IS THE BYTES STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE
NEWLINE THAT TERMINATES ITS LAST CONTENT LINE: extract it as everything after the `BEGIN-` line's
own newline up to and including the newline immediately before the `END-` line, so that
`pre + slice` is already a newline-terminated file and NO joiner and NO terminator byte is ever
added. RECORD24 is PROSE joined to its target by exactly one blank line. TESTSNPM is CODE joined to
its target by exactly one blank line, so the file keeps the two-blank-line separation PEP 8 puts
between top-level definitions and `pre + "\n" + slice` is the whole post-commit file.

## Change

C1 applies PLAN10F→PLAN10T to `.agent/plan.md`, rewriting the `## Current Step` section, the WHOLE
`## Next Steps` list and the WHOLE `## Risks` list — the last two because this round answers the
npm risk and removing an entry changes that list's arity, so the FROM spans the whole structure.
C2 appends RECORD24 to `.agent/live_review.md`. C3 applies ALLOWF→ALLOWT to
`packages/orchestration/exec_guard.py` and appends TESTSNPM to
`tests/orchestration/test_exec_guard.py` — one commit, because a policy row and the test that pins
its members are one logical step and splitting them would land a widened row with no pin for the
length of a commit.

Change set, named rather than counted: `.agent/authored/f085-r56.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/exec_guard.py`,
`tests/orchestration/test_exec_guard.py`, `.agent/handoff.md`. Nothing else. No `docs/roadmap/**`
path is in that set, so the §3 docs tier does NOT trigger and no `tests/docs/` gate is ordered.
`packages/orchestration/ui_server.py` is deliberately NOT in it: the migration is R57's, and this
round exists so that R57 migrates onto a row that already answers the question.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r56.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round orders no destructive check, so it creates no worktree and
   `git worktree list` stays one line throughout.
3. PAIR SHAPES. The reviewer ran the containment test on each pair at emission against that file's
   blob at 49a3fdcb and prints its own output here per checklist item 15, one reading per pair:
   PLAN10F→PLAN10T `TO contains FROM: false`; ALLOWF→ALLOWT `TO contains FROM: false`. Both are
   therefore REWRITES and each owes the FROM 0x / TO 1x reading over its own post-commit file. Each
   FROM occurs EXACTLY 1x in its target at 49a3fdcb — the reviewer measured both. RECORD24 and
   TESTSNPM are APPENDS carrying no FROM, so no containment reading is owed for either.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the code. Only C0a and C0b
   may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
5. Every sentence in RECORD24 that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. C0b overwrites the
   working `.agent/last_block.md` before RECORD24 lands, which is why a SHA carries those readings.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested PLAN10F and ALLOWF against every
   later-applied text at emission and got NO hits, so both G3 FROM-0x readings stay attainable
   (checklist item 2).
7. Nothing outside the declared change set is touched. This round REGISTERS NOTHING and RESOLVES
   NOTHING: R55 passed with no finding, so the registered, done and landed counts are all
   UNCHANGED, the open count stays 145 and the next free id stays R-0558.
8. THE WIDENING IS BY NAME AND NEVER BY PREFIX. `scrub_child_env` matches an allowlist entry as a
   whole key, so naming `NPM_CONFIG_CACHE`, `NPM_CONFIG_PREFIX`, `NPM_CONFIG_REGISTRY` and
   `NPM_CONFIG_USERCONFIG` individually is what keeps `NPM_CONFIG__AUTHTOKEN` and every other
   credential in that namespace out of the child. Do not replace those entries with a prefix test,
   a glob or a loop over `os.environ`, and do not add a proxy variable: `HTTP_PROXY`, `HTTPS_PROXY`
   and `ALL_PROXY` are `FORBIDDEN_ENV_KEYS` members and that floor is not a row's to lift.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 345, PROSE 194, RECORD24 32. The worker
   re-measures all three from the committed `.agent/authored/f085-r56.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
10. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.
11. THIS ROUND ORDERS NO RED CONTROL. The reviewer proved TWICE in its own disposable worktree at
   49a3fdcb, before emitting this block, that these tests have teeth: reverting ALLOWT to ALLOWF
   turns both new tests RED with the other 33 green, and making `scrub_child_env` match
   `NPM_CONFIG_` as a PREFIX reddens the second one alone. It removed that worktree. Repeating
   either here would put a destructive check in the primary checkout for no new information.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r56.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r56.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - The TWO REWRITES of constraint 3: in each post-commit file its FROM occurs 0x and its TO exactly
   1x. Report both counts per pair and `git show --numstat` for each path and commit.
 - C2 / RECORD24 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's prose.
   §4.9's per-line PROSE obligation also applies: every non-empty line the slice contains occurs
   exactly once among the lines C2's diff adds TO THAT PATH.
 - C3 / TESTSNPM / `tests/orchestration/test_exec_guard.py`, a CODE APPEND: §4.9 as R-0531 narrows
   it binds ORDERED EQUALITY and NOT a per-line count, because code repeats lines structurally. The
   pre-commit blob is a byte-exact PREFIX of the post-commit file, the remainder is exactly one
   blank line plus the slice, the slice is an exact SUFFIX, the lines C3's diff adds to that path
   are exactly the slice's lines IN ORDER, and 0 marker LINES land in it.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each exit 0. The reviewer took
every base reading below itself, in the primary checkout, at 49a3fdcb.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q` — base `33 passed`, and this
   round ships two tests, so the expected reading is `35 passed`. REPORT the number.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — ordered because C1 rewrites
   `.agent/plan.md`, which two of them assert on. Base `159 passed`.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 LINT. `python3 -m ruff check packages/orchestration/exec_guard.py
tests/orchestration/test_exec_guard.py`, exit 0, with the repository's own `pyproject.toml` and NO
`--isolated` flag, because that flag would discard the `select` line that enables the rules
(R-0463). The reviewer ran this exact command line at 49a3fdcb and got `All checks passed!`.

G6 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 44 lines mechanically by applying the pair to that file's blob at 49a3fdcb.

G7 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
49a3fdcb and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 172 / 27 / 0, 145 open, max registered R-0557, max resolved
R-0532. At HEAD ALL THREE COUNTS MUST BE UNCHANGED and ALL THREE SYMMETRIC DIFFERENCES MUST BE
EMPTY, because this round records a verdict and registers nothing; 145 open, next free id R-0558.
Report the three symmetric differences, the duplicate-id count and the count of resolutions naming
an unregistered id, at both SHAs.

G8 HYGIENE. `git diff --name-only 49a3fdcb..HEAD` measured BEFORE C4 holds exactly the change set
above minus `.agent/handoff.md`, which C4 writes, and nothing else — and in particular does NOT
hold `packages/orchestration/ui_server.py`, which this round's change set excludes. Report
per-commit insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own insertions
go in the round report — and confirm none exceeds 500. This branch spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint 10,
never a declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 49a3fdcb, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3
and C4, the real G1-G8 results with exit codes, the open-findings count and the next expected
action. The Bundle above names six commits, which is more than five, so the ≤100-line allowance
applies; if the mandated content genuinely does not fit even that, name the DECISION D15 stated
cause and the specific mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~94 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R55 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht, Extraktion und die
Umgebungszeile gebaut, die fünf Call-Sites offen · T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R57, which migrates the two `runtime-build` call sites in `_auto_build_frontend`
(`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`,
now that the row those sites will run under answers the environment question. Then the three
`runtime-server` sites, then T003, the integration gate and closure. TWO: R56's own verdict is NOT
on disk as a gate entry, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, and R57 must not
open a repair round to close it. THREE: a standalone closing line stating the open findings count
and the next free id as its own sentence. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from
disk`, which the self-drive protocol requires every handoff naming a next action to put ahead of
the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN10F
## Current Step
R55, this round: a RECORD round only. It persists the R54 PASS to `.agent/live_review.md` and
advances this file; it writes no production code and ships no test. It exists because the
reviewer's session ended at its declared round cap, and a verdict that lives only in a chat reply
is one the next session would have to re-derive from the diff.

## Next Steps
1. T002d's second half — migrate the two `runtime-build` sites in `_auto_build_frontend`
   (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with
   `check=True`, settling the npm environment risk below FIRST. Then the three `runtime-server`
   sites, which take no wall timeout because a clock would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.

## Risks
- `RUNTIME_BUILD_ENV_ALLOWLIST` is `TEST_COMMAND_ENV_ALLOWLIST`, read at 1812c219: it carries
  `HOME` and `PATH`, so a public-registry `npm install` survives the scrub, but it names no
  `NPM_CONFIG_*`, no `NODE_*` and no proxy variable. A project on a private registry or behind a
  proxy would break at the migration, not at the seam. R56 settles this BEFORE it migrates —
  widen that row, or take the `extra_env_keys` knob the `test` row already carries.
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
END-PLAN10F

BEGIN-PLAN10T
## Current Step
R56, this round: settle the npm environment question T002d's second half depends on. The
`runtime-build` allowlist row is widened from the bare `test` set to the npm and node
CONFIGURATION keys a build reads, each key named in full so no credential spelled `NPM_CONFIG_*`
passes with them, and two tests pin both halves. No call site migrates here. The R55 PASS is
recorded in the same round.

## Next Steps
1. T002d's second half — migrate the two `runtime-build` sites in `_auto_build_frontend`
   (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with
   `check=True`. Then the three `runtime-server` sites, which take no wall timeout because a
   clock would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
END-PLAN10T

BEGIN-ALLOWF
#: WHY: the environment a `runtime-build` command may inherit, and its per-stream cap.
#: The MEMBERS are the `test`-class values and the NAMES are deliberately separate, for
#: the reason `DOD_PROCESS_ENV_ALLOWLIST` states: T2_F085's policy table rules
#: `runtime-build` as its own row, so widening one row stays a one-line edit here.
RUNTIME_BUILD_ENV_ALLOWLIST: tuple[str, ...] = TEST_COMMAND_ENV_ALLOWLIST
END-ALLOWF

BEGIN-ALLOWT
#: WHY: the environment a `runtime-build` command may inherit, and its per-stream cap.
#: The `test`-class values are the BASE and the NAMES stay deliberately separate, for
#: the reason `DOD_PROCESS_ENV_ALLOWLIST` states: T2_F085's policy table rules
#: `runtime-build` as its own row, so widening one row is an edit here alone.
#: The ADDED keys are the npm and node CONFIGURATION a build legitimately reads: `HOME`
#: and `PATH` alone reach a public registry with default settings only, so a project on
#: a private registry, a custom cache or a corporate TLS root would have broken at the
#: call site rather than at the seam. Each key is named IN FULL and never by a prefix,
#: which is what keeps `NPM_CONFIG__AUTHTOKEN` — and every other credential spelled
#: into that namespace — out of the child, since `scrub_child_env` matches whole keys.
#: Remedy deliberately does not pass a proxy variable here: `HTTP_PROXY`, `HTTPS_PROXY`
#: and `ALL_PROXY` are `FORBIDDEN_ENV_KEYS` members, which is the guard's floor and not
#: a row's to lift, so a build behind a proxy is a STATED stage-1 limitation for T003's
#: document rather than something this row reaches.
RUNTIME_BUILD_ENV_ALLOWLIST: tuple[str, ...] = TEST_COMMAND_ENV_ALLOWLIST + (
    "NODE_ENV", "NODE_EXTRA_CA_CERTS", "NODE_OPTIONS", "NODE_PATH",
    "NPM_CONFIG_CACHE", "NPM_CONFIG_PREFIX", "NPM_CONFIG_REGISTRY",
    "NPM_CONFIG_USERCONFIG",
)
END-ALLOWT

BEGIN-TESTSNPM
#: The npm and node CONFIGURATION keys the `runtime-build` row adds to the `test` base.
#: Listed here so the two tests below read the same set and a widening edits one place.
_RUNTIME_BUILD_ADDED_ENV_KEYS = frozenset({
    "NODE_ENV", "NODE_EXTRA_CA_CERTS", "NODE_OPTIONS", "NODE_PATH",
    "NPM_CONFIG_CACHE", "NPM_CONFIG_PREFIX", "NPM_CONFIG_REGISTRY",
    "NPM_CONFIG_USERCONFIG",
})


def test_the_runtime_build_row_adds_the_npm_configuration_to_the_test_base():
    """The widened row, asserted as base-plus-additions rather than as a re-listing.

    The `test` set is asserted to SURVIVE as a subset, so a later widening of the
    shared base cannot silently drop out of this class, and `FORBIDDEN_ENV_KEYS` is
    asserted disjoint so the floor holds however the row grows.
    """
    allowlist = set(exec_guard.RUNTIME_BUILD_ENV_ALLOWLIST)
    assert set(TEST_COMMAND_ENV_ALLOWLIST) <= allowlist
    assert _RUNTIME_BUILD_ADDED_ENV_KEYS <= allowlist
    assert not exec_guard.FORBIDDEN_ENV_KEYS & allowlist


@pytest.mark.subprocess
def test_the_runtime_build_row_passes_npm_config_by_name_and_never_by_prefix(monkeypatch):
    """A named `NPM_CONFIG_*` key reaches the child; a credential in that namespace does not.

    This is the property that makes the widening safe to ship: `scrub_child_env` matches
    a whole key, so `NPM_CONFIG__AUTHTOKEN` is unlisted rather than merely unmentioned.
    `HTTPS_PROXY` is asserted absent for the other reason — it is a `FORBIDDEN_ENV_KEYS`
    member, so the floor drops it even though a build behind a proxy would want it.
    """
    monkeypatch.setenv("NPM_CONFIG_REGISTRY", "https://registry.example.invalid")
    monkeypatch.setenv("NPM_CONFIG__AUTHTOKEN", "npm-token-should-never-appear")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example.invalid:8080")

    completed = exec_guard.run_guarded_runtime_build_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None)

    dumped = _dumped(completed)
    assert completed.returncode == 0
    assert dumped["NPM_CONFIG_REGISTRY"] == "https://registry.example.invalid"
    assert "NPM_CONFIG__AUTHTOKEN" not in dumped
    assert "HTTPS_PROXY" not in dumped
END-TESTSNPM

BEGIN-RECORD24
Gate: R56 — the R55 entry. R55 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer
over 1812c219..49a3fdcb, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r55.md`, the committed `.agent/authored/f085-r55.md` and the
committed `.agent/last_block.md` at 49a3fdcb, and both of those working copies as they stand at
49a3fdcb, are all five byte-EQUAL at sha256
dfcb54609904651d7d882c01e83ade3712e1ab8a42355b62199a4271a89f665e, 19014 B, 253 lines, 6 marker
lines — every figure measured on every copy. THE SHAPES HELD. The one REWRITE gives
`TO contains FROM: false`, its FROM 1x in the pre-commit blob and 0x after with its TO exactly 1x:
PLAN9F→PLAN9T at e02f0dcc, numstat `12 7`. THE PROSE APPEND RECORD23 on `.agent/live_review.md` at
2bb63069: byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix,
0 marker LINES, and each of its 46 non-empty slice lines occurring exactly once among the 47 lines
that commit adds, numstat `47 0`. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with
the block's exact command lines, each exit 0: the four state readers `159 passed` against a base of
159, and the canary `42 passed` against 42. THE PLAN CONTRACT HELD at e02f0dcc: 46 lines against
the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 46 is the figure that
block projected. THE ARITHMETIC DID NOT MOVE, as a record round requires: 172 registered / 27 done
/ 0 landed and 145 open at 1812c219 and the same at 49a3fdcb, max registered R-0557 and max
resolved R-0532 at both, all three symmetric differences EMPTY, 0 duplicate ids and 0 resolutions
naming an unregistered id at both SHAs. HYGIENE IS CLEAN: walking 1812c219..49a3fdcb commit by
commit the INSERTION counts, the column AGENTS.md DECISION F104 D1 fixes for the cap, are 253, 174,
12, 47 and 31 for the handback commit; none over 500; that range's path set is exactly the five
ordered paths and holds NO path under `packages/` or `tests/`, which that round's change set
excluded; all five commits are single-parent; the tree is clean and `git worktree list` is one
line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 253, PROSE 158 and
RECORD23 46, agreeing with that block. THE HANDBACK'S OWN SELF-CLAIM was checked and holds:
`.agent/handoff.md` at 49a3fdcb states 69 lines and measures 69, and its DECISION D15 stated cause
names only MANDATED content — five per-commit tables, the item-status table, the verification
transcript — with no section dropped, which is what that decision permits and what a five-commit
round genuinely owes. THE ROUND'S OWN CLAIM TO HAVE REGISTERED AND RESOLVED NOTHING was verified
rather than accepted, since it is the whole substance of a record round: the registered, done and
landed id SETS at the two SHAs are identical element by element, not merely equal in count.
END-RECORD24
