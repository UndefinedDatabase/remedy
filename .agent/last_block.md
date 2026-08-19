── STEP T002e call sites, part 1 — F085 — R61 ────────────────────────────────

Goal: migrate the TWO app-spawning `runtime-server` call sites — `packages/runtimes/dev_server.py`
and `packages/runtimes/runtime_supervisor.py` — onto `runtime_server_exec_policy` via
`plan_child_spawn`, each keeping its own `Popen` and its own supervision, and pin the result with a
test that reads the environment the child really received. The third call site,
`apps/cli/commands/runtime_cmd.py`, is NOT in this round: it spawns the Remedy supervisor rather
than a project's app, its declared keys are a different set, and its scrub narrows what the other
two can hand on — so it is safer once these two are landed and green. This round also records the
R60 PASS, which the round after a verdict always owes.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md`
· C2 record the R60 PASS · C3 migrate both sites and adapt the one boundary test they break · C4 add
the child-environment test · C5 handback. That list runs past C0a, C0b, C1, C2, C3, C4 to C5, so it
holds more than five commits and the handback may use the ≤100-line form AGENTS.md allows.

CONVENTION, binding on every count here, carried verbatim in force from the R60 block. A line count
is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and
NO joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN15, SITE2A,
SITE2B, SITE3A, SITE3B, BOUNDA and BOUNDB; ITS END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE
TESTCODE AND RECORD29 — listed rather than counted, per §3 checklist item 11. Each append slice
CARRIES ITS OWN LEADING BLANK LINES, so the separation its target's convention requires is a
property of bytes that were measured and never of a join shape that was reasoned about.

## Change

C1 applies PLAN15F→PLAN15T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep
a stale label. C2 appends RECORD29 to the END of `.agent/live_review.md`. C3 applies SITE2A then
SITE2B to `packages/runtimes/dev_server.py`, SITE3A then SITE3B to
`packages/runtimes/runtime_supervisor.py`, and BOUNDA then BOUNDB to
`tests/runtimes/test_runtime_cli_process_boundary.py`. C4 appends TESTCODE to the END of
`tests/runtimes/test_dev_server.py`.

The three files of C3 are ONE commit on purpose, and this is the one place this block departs from
the usual one-file-per-commit habit. After the two migrations alone the boundary test
`test_the_readiness_failure_returns_the_line_the_child_really_printed` is RED — the reviewer ran it
and saw exit 3, "the CLI gave up before the child printed" — because that test hands its application
a marker path through the PARENT environment, which is exactly the channel this feature closes. Its
adaptation is therefore part of the same change and not a separate step; splitting them would put a
knowingly red commit on the branch.

Change set, named rather than counted: `.agent/authored/f085-r61.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/runtimes/dev_server.py`,
`packages/runtimes/runtime_supervisor.py`, `tests/runtimes/test_runtime_cli_process_boundary.py`,
`tests/runtimes/test_dev_server.py`, `.agent/handoff.md`. Nothing else.
`apps/cli/commands/runtime_cmd.py` is NOT in that set and is not edited this round. The reviewer ran
`git ls-tree 5b9f935b --` on it and on all four other source paths before emitting, per §3 checklist
item 24, and all five exist. No `docs/roadmap/**` path is in the set, so the §3 docs tier does NOT
trigger and no `tests/docs/` gate is ordered.

## What the scrub keeps, settled per site before editing

Both migrated sites spawn a PROJECT's application and both build its environment the same way, with
`RuntimeSpec.resolved_env(port)`, which at 5b9f935b returns `dict(os.environ)` overlaid with the
spec's own `env` mapping and then `PORT`. So for both, the keys the child needs ON TOP of
`RUNTIME_SERVER_ENV_ALLOWLIST` are exactly `PORT` plus the spec's own keys, and both are already in
that merged mapping — which is why the merged mapping is passed as the scrub SOURCE rather than
`os.environ`. `PORT` is load-bearing, not a formality: every dummy application under
`tests/runtimes/` reads `os.environ["PORT"]` and dies without it. `REMEDY_RUNTIME_PORT` and
`REMEDY_RUNTIME_LOG_MAX` are read by the supervisor PROCESS ITSELF, never by its child, so they are
not declared here; they belong to the `runtime_cmd.py` site and are the next round's business.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r61.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round orders NO destructive check and NO red proof — the reviewer ran
   the red control itself before emitting — so `git worktree list` is one line at round start,
   throughout, and at the end. Do not create a worktree.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   5b9f935b and prints its own output here per checklist item 15, one reading per pair:
   PLAN15F→PLAN15T `TO contains FROM: false`; SITE2AF→SITE2AT `TO contains FROM: true`;
   SITE2BF→SITE2BT `TO contains FROM: false`; SITE3AF→SITE3AT `TO contains FROM: true`;
   SITE3BF→SITE3BT `TO contains FROM: false`; BOUNDAF→BOUNDAT `TO contains FROM: false`;
   BOUNDBF→BOUNDBT `TO contains FROM: false`. So PLAN15, SITE2B, SITE3B, BOUNDA and BOUNDB are
   REWRITES and each owes the FROM 0x / TO 1x reading over its post-commit blob. SITE2A and SITE3A
   are APPEND-shaped: they owe FROM exactly 1x and TO exactly 1x after the commit, and NO zero count
   is owed or may be reported for them, because a TO that contains its own FROM can never drive that
   FROM to zero. Each of the seven FROMs occurs EXACTLY 1x in its target at 5b9f935b — the reviewer
   measured all seven separately.
4. TESTCODE AND RECORD29 HAVE NO FROM. Each is appended at the END of its target. Their obligation
   is ORDERED EQUALITY per §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of
   the post-commit file, the slice is an exact SUFFIX of it, and the lines that commit's diff ADDS
   are exactly the slice's lines IN ORDER. TESTCODE is CODE, so the per-line "each TO-only addition
   exactly 1x" count is NOT owed for it and must not be reported. Do not invent a FROM for either.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of both migrations. Only C0a
   and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds.
6. Every sentence in RECORD29 that states a reading of a file THIS BLOCK also edits names the SHA it
   was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first.
7. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD29 is reviewer text. Do not add a `Landed:`
   line, do not add a `Done:` paragraph of your own, and do not edit RECORD29 to reconcile it with
   anything you measure. A disagreement between RECORD29 and your own reading is a finding to REPORT
   in the handback, never to fix.
8. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. Registered stays 174, done stays 28, landed
   stays 0, open stays 146, and the next free id stays R-0560. RECORD29 is a `Gate:` paragraph and
   carries no `- R-` registration line and no `Done:` line, which is why the arithmetic must not
   move; G7 exists to prove it did not.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and reports them in G2. The worker re-measures all three from the
   committed `.agent/authored/f085-r61.md` and reports them; a mismatch is a finding against this
   block, not against the worker.
10. NEITHER MIGRATION MAY CHANGE ANYTHING ELSE ABOUT ITS `Popen`. `start_new_session=True`, the
   stream wiring and the surrounding try/except stay exactly as they are: this round changes the
   `cwd`, the `env` and the addition of `preexec_fn`, and nothing further. Both TOs keep the
   existing `# noqa: S603` comment line untouched.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, never widen the
   change set to route around a red, and never touch `apps/cli/commands/runtime_cmd.py`.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line at round start and at the end, with
NO worktree created in between.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r61.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each, measured on every copy. Also report the block's TOTAL, PROSE and
RECORD29 line counts read from that committed file, against the 490 / 400 / 140 figures in
constraint 9. The reviewer holds its own original and runs the disk-to-disk comparison against it
itself; do not name or read any path outside the repository's tracked tree.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - For PLAN15, SITE2B, SITE3B, BOUNDA and BOUNDB report FROM 0x and TO exactly 1x over the
   post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob must reproduce the
   post-commit blob BYTE-EXACTLY.
 - For SITE2A and SITE3A report FROM exactly 1x and TO exactly 1x over the post-commit blob, and the
   same byte-exact re-application. Report NO zero count for these two.
 - For TESTCODE and RECORD29 report the ordered-equality readings constraint 4 names: pre-commit
   blob is a byte-exact PREFIX, the slice is an exact SUFFIX, `pre + slice` equals the post-commit
   blob byte for byte, and the commit's ADDED lines are exactly the slice's lines IN ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 LINT, over `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`,
`tests/runtimes/test_dev_server.py` and `tests/runtimes/test_runtime_cli_process_boundary.py`, in
the PRIMARY checkout. BOTH halves are ALREADY RED at 5b9f935b, where the reviewer measured them, so
NEITHER may be ordered as exit 0 and both are compared as rule-code MULTISETS instead. Run each with
`--output-format json` and count the `code` field, so the comparison is a multiset and not a glance
at the tail of a listing.
 - `python3 -m ruff check <the four paths>` — base multiset exactly `{I001: 1}`, that one finding in
   `tests/runtimes/test_runtime_cli_process_boundary.py`, which this round does not repair because
   its imports are not what this round touches. HEAD must give the SAME multiset.
 - `python3 -m ruff check --preview <the four paths>` — base multiset exactly `{E303: 1, I001: 1}`,
   the `E303` in `packages/runtimes/dev_server.py`. HEAD must give the SAME multiset.
 - A NEW code, or a second instance of either, is a red under constraint 11.

G5 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each exit 0. The reviewer took
every base reading below itself, in the primary checkout, at 5b9f935b.
 - `python3 -m pytest tests/runtimes/ -rf -q` — base `251 passed` with NO skips. C4 adds exactly one
   test, so the expected reading is the base count plus one, `252 passed`, still with no skips. This
   is the suite that runs the real CLI, the real supervisor and real applications, so it is where
   both migrations are proven end to end rather than by inspection. It takes about 3.5 minutes; that
   is normal, not a hang.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q` — base `36 passed`, expected
   UNCHANGED: this round CONSUMES the seam and must not alter it.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — base `160 passed`, expected UNCHANGED; two
   of them assert on `.agent/plan.md`, which C1 rewrites, and that is why this set is ordered.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G6 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 44 lines mechanically by applying the pair to that file's blob at 5b9f935b.

G7 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
5b9f935b and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 174 / 28 / 0, 146 open, max registered R-0559, max resolved
R-0558. At HEAD the reading must be IDENTICAL — 174 / 28 / 0, 146 open, same two maxima — and all
three symmetric differences must be EMPTY, because constraint 8 rules this round registers and
resolves nothing. Next free id R-0560. Report all three symmetric differences, the duplicate-id
count and the count of resolutions naming an unregistered id, at both SHAs.

G8 HYGIENE. `git diff --name-only 5b9f935b..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular does NOT hold
`apps/cli/commands/runtime_cmd.py`, whose migration is the next round's. Report per-commit
insertions for every commit BEFORE C5 — C5 cannot measure itself, so its own insertions go in the
round report — and confirm none exceeds 500. This branch spent the AGENTS.md declared-oversize
allowance at d4473f85, so a second oversize commit is a STOP under constraint 11, never a
declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 5b9f935b, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3,
C4 and C5, the real G1-G8 results with exit codes, the open-findings count and the next expected
action. The Bundle above holds more than five commits, so the ≤100-line form applies; if the
mandated content still does not fit, name the DECISION D15 stated cause and the specific mandated
content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~98 % (T001 gebaut · R13-R60 PASS · T002a-T002d KOMPLETT · T002e — die
`runtime-server`-Policy gebaut, die beiden App-Call-Sites migriert und mit einem
Kind-Environment-Test gepinnt, `apps/cli/commands/runtime_cmd.py` offen · T003 offen) — Schätzung,
gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R62, which migrates the LAST `runtime-server` call site, `apps/cli/commands/runtime_cmd.py`, whose
child is the Remedy supervisor rather than a project application, and whose declared keys are
`REMEDY_DATA_DIR`, `REMEDY_RUNTIME_LOG_MAX` and `REMEDY_RUNTIME_PORT` — the first because the
supervisor resolves its own runtime directory through `projects_dir()`, the second because
`tests/runtimes/test_runtime_cli_process_boundary.py` passes it to the CLI to cap the log, the third
because the supervisor reads it with `os.environ[...]` and dies without it. TWO: R61 carries no
verdict of its own, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13); R62 carries it. THREE: a standalone closing line
stating the open findings count and the next free id as its own sentence. FOUR: `Phase 1 rule 1
first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires every handoff naming
a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN15F
## Current Step
R60, this round: a RECORD round that writes no code. It records the R59 PASS, which the round
after a verdict always owes because a round cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13). The `runtime-server` policy built at R59 is
verified and unchanged; nothing consumes it yet.

## Next Steps
1. Migrate the three `runtime-server` call sites onto the policy:
   `apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
   `packages/runtimes/runtime_supervisor.py`. Each keeps its own `Popen` and its own
   supervision; what changes is the `cwd`, `env` and `preexec_fn` it spawns with, which come
   from `plan_child_spawn`. Settle per site which keys its child needs on top of
   `RUNTIME_SERVER_ENV_ALLOWLIST` BEFORE editing: a scrub that drops one breaks a server.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN15F

BEGIN-PLAN15T
## Current Step
R61, this round: the two APP-spawning `runtime-server` call sites — `packages/runtimes/dev_server.py`
and `packages/runtimes/runtime_supervisor.py` — take `plan_child_spawn`, so a project's application
inherits the allowlist plus `PORT` and the spec's own keys and nothing else. A test reads the
environment from inside the running child. The R60 PASS is recorded in the same round.

## Next Steps
1. Migrate the LAST call site, `apps/cli/commands/runtime_cmd.py`, whose child is the Remedy
   supervisor rather than a project application. Its declared keys are `REMEDY_DATA_DIR`,
   `REMEDY_RUNTIME_LOG_MAX` and `REMEDY_RUNTIME_PORT`: the supervisor resolves its runtime
   directory through `projects_dir()`, the boundary suite passes the log cap to the CLI, and the
   supervisor reads the port with `os.environ[...]` and dies without it.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN15T

BEGIN-SITE2AF
        argv = self.spec.resolved_cmd(self.port)
        env = self.spec.resolved_env(self.port)
END-SITE2AF

BEGIN-SITE2AT
        argv = self.spec.resolved_cmd(self.port)
        env = self.spec.resolved_env(self.port)
        # F085 T002e: the CHILD half of the `runtime-server` policy. `resolved_env` has
        # already merged the spec's own keys and `PORT` over the parent's environment, so
        # those are the DECLARED keys and the merged mapping is the scrub SOURCE; the
        # allowlist keeps them plus its own members, and every other variable the parent
        # held — a provider key, an operator's shell setting — stops here.
        from packages.orchestration.exec_guard import (
            plan_child_spawn,
            runtime_server_exec_policy,
        )
        spawn_plan = plan_child_spawn(runtime_server_exec_policy(
            cwd=self.spec.cwd,
            env=env,
            declared_env_keys=("PORT", *(str(key) for key in self.spec.env)),
        ))
END-SITE2AT

BEGIN-SITE2BF
                argv,
                cwd=self.spec.cwd,
                env=env,
END-SITE2BF

BEGIN-SITE2BT
                argv,
                cwd=spawn_plan.cwd,
                env=spawn_plan.env,
                preexec_fn=spawn_plan.preexec_fn,  # rlimits between fork and exec
END-SITE2BT

BEGIN-SITE3AF
        argv = self.spec.resolved_cmd(self.port)
        env = self.spec.resolved_env(self.port)
END-SITE3AF

BEGIN-SITE3AT
        argv = self.spec.resolved_cmd(self.port)
        env = self.spec.resolved_env(self.port)
        # F085 T002e: the CHILD half of the `runtime-server` policy, exactly as
        # `dev_server.DevServer.start` takes it. The supervisor keeps the parent half —
        # the log pump, the readiness report, the stop path. Its own `REMEDY_RUNTIME_*`
        # variables are ITS environment, not the application's, so they are not declared.
        from packages.orchestration.exec_guard import (
            plan_child_spawn,
            runtime_server_exec_policy,
        )
        spawn_plan = plan_child_spawn(runtime_server_exec_policy(
            cwd=self.spec.cwd,
            env=env,
            declared_env_keys=("PORT", *(str(key) for key in self.spec.env)),
        ))
END-SITE3AT

BEGIN-SITE3BF
                argv, cwd=self.spec.cwd, env=env,
END-SITE3BF

BEGIN-SITE3BT
                argv, cwd=spawn_plan.cwd, env=spawn_plan.env,
                preexec_fn=spawn_plan.preexec_fn,  # rlimits between fork and exec
END-SITE3BT

BEGIN-BOUNDAF
def _config(root: Path, script: str, *, timeout: float = 20.0,
            port: int | None = None) -> None:
    if port is None:
        port = worker_port()
    cfg = root / ".remedy"
    cfg.mkdir(exist_ok=True)
    (cfg / "config.toml").write_text(
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "{script}"]\n'
        'cwd = "."\n'
        f"port = {port}\n"
        'health_path = "/"\n'
        f"ready_timeout_s = {timeout}\n"
    )
END-BOUNDAF

BEGIN-BOUNDAT
def _config(root: Path, script: str, *, timeout: float = 20.0,
            port: int | None = None, env: dict[str, str] | None = None) -> None:
    if port is None:
        port = worker_port()
    cfg = root / ".remedy"
    cfg.mkdir(exist_ok=True)
    body = (
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "{script}"]\n'
        'cwd = "."\n'
        f"port = {port}\n"
        'health_path = "/"\n'
        f"ready_timeout_s = {timeout}\n"
    )
    # `runtime.env` is the SUPPORTED channel for a variable the application needs.
    # Since F085 T002e the guard scrubs the parent environment, so a value smuggled
    # through `os.environ` no longer reaches the child; a DECLARED key does.
    if env:
        body += "\n[runtime.env]\n" + "".join(
            f'{key} = "{value}"\n' for key, value in env.items())
    (cfg / "config.toml").write_text(body)
END-BOUNDAT

BEGIN-BOUNDBF
        (project / "never_marker.py").write_text(NEVER_WITH_MARKER)
        _config(project, "never_marker.py", timeout=12.0)

        env = dict(os.environ)
        env["REMEDY_DATA_DIR"] = str(data_root)
        env["REMEDY_TEST_MARKER"] = str(marker)
END-BOUNDBF

BEGIN-BOUNDBT
        (project / "never_marker.py").write_text(NEVER_WITH_MARKER)
        # DECLARED, not inherited: T002e scrubs the application environment, so the
        # marker path travels through `runtime.env` — which also proves a declared
        # key survives the CLI and the supervisor end to end.
        _config(project, "never_marker.py", timeout=12.0,
                env={"REMEDY_TEST_MARKER": str(marker)})

        env = dict(os.environ)
        env["REMEDY_DATA_DIR"] = str(data_root)
END-BOUNDBT

BEGIN-TESTCODE


class TestTheChildEnvironmentIsScrubbed:
    """F085 T002e — what a launched application really inherits, measured IN the child.

    `tests/orchestration/test_exec_guard.py` pins the POLICY object. The only place
    what a real `Popen` under it hands over can be observed is the child itself, so
    this server dumps its own environment to a file before it starts serving.
    """

    ENV_DUMP_SERVER = """
import http.server, json, os, sys
port = int(os.environ["PORT"])
open(sys.argv[1], "w").write(json.dumps(dict(os.environ)))
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""

    def test_a_secret_parent_variable_never_reaches_the_app(self, project, monkeypatch):
        import json

        (project / "envdump.py").write_text(self.ENV_DUMP_SERVER)
        dump = project / "child_env.json"
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-must-not-travel")
        monkeypatch.setenv("REMEDY_UNDECLARED_MARKER", "must-not-travel")

        server = DevServer(
            RuntimeSpec(
                cmd=[sys.executable, str(project / "envdump.py"), str(dump)],
                cwd=str(project), port=worker_port(), health_path="/",
                ready_timeout_s=20.0, env={"APP_DECLARED_TOKEN": "travels"},
            ),
            project,
        )
        server.start()
        try:
            assert server.wait_ready().ok
            child_env = json.loads(dump.read_text())
        finally:
            server.stop()

        assert child_env["PORT"] == str(server.port)
        assert child_env["APP_DECLARED_TOKEN"] == "travels"    # the spec's own key
        assert "PATH" in child_env                             # the allowlist held
        assert "ANTHROPIC_API_KEY" not in child_env            # the guard's floor held
        assert "REMEDY_UNDECLARED_MARKER" not in child_env     # the allowlist bound
END-TESTCODE

BEGIN-RECORD29

Gate: R61 — the R60 entry. R60 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer over
d91d2ffa..5b9f935b, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing beyond the handback length it declared. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT
HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback: the committed
`.agent/authored/f085-r60.md` and the committed `.agent/last_block.md` at 5b9f935b, both of those
working copies as they stand at 5b9f935b, and the reviewer's own original are all five byte-EQUAL at
sha256 ec373c9c3df936db9dd595afa7799255e80649b84b0212e93ca43f0e8678aa47, 19312 B, 253 lines, 6 marker
lines, which is the digest that block carried. THE SHAPES HELD, and the two classes were measured
apart. PLAN14F→PLAN14T at ac7f5ac5 is a REWRITE: `TO contains FROM: false`, FROM 1x before and 0x
after, TO exactly 1x, numstat `6 6`, and re-applying the extracted FROM→TO to the pre-commit blob
reproduces the post-commit blob BYTE-EXACTLY. RECORD28 at a567afe3 satisfies ORDERED EQUALITY on
every clause: the pre-commit blob is a byte-exact PREFIX, the slice an exact SUFFIX, `pre + slice`
equals the post-commit blob byte for byte, and that commit's ADDED lines equal the slice's 47 lines
IN ORDER, numstat `47 0`. Marker LINES at 5b9f935b are 0 in both slice targets, `.agent/plan.md` and
`.agent/live_review.md`. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with the block's
exact command lines, each exit 0: the four state readers `160 passed`, unchanged as ordered, and the
canary `42 passed`. THE PLAN CONTRACT HELD at ac7f5ac5: 45 lines against the 50-line cap with
`## Goal`, `## Next Steps` and a roadmap F-id all present, 45 being the figure that block projected.
THE ARITHMETIC DID NOT MOVE, as constraint 8 of that block required: 174 registered / 28 done / 0
landed and 146 open at d91d2ffa, the same three numbers and the same 146 at 5b9f935b, max registered
R-0559 and max resolved R-0558 at both, all three symmetric differences EMPTY, and 0 duplicate ids
and 0 resolutions naming an unregistered id at both SHAs. HYGIENE IS CLEAN: the path set over
d91d2ffa..a567afe3 is exactly `.agent/authored/f085-r60.md`, `.agent/last_block.md`,
`.agent/live_review.md` and `.agent/plan.md`, holds no `.py` path at all and none of the three
`runtime-server` call sites; per-commit INSERTIONS are 253, 171, 6, 47 and 52 for the handback
commit, none over 500; all five commits are single-parent. THE BLOCK'S OWN SIZE re-measured from the
committed file gives TOTAL 253, PROSE 170 and RECORD28 47, agreeing with that block's own figures and
under 490 / 400 / 140. CHECKLIST ITEM 24 HELD FOR THE ROUND AFTER THE ONE THAT PROMOTED IT: all three
call sites resolve at d91d2ffa — `apps/cli/commands/runtime_cmd.py` blob 01ab65ed,
`packages/runtimes/dev_server.py` blob 7715a28e and `packages/runtimes/runtime_supervisor.py` blob
9f3749ae — so the absence clause G7 carried forbade paths that really exist, which is what R-0559
asked for. THE ONE REPORTING NOTE THE HANDBACK RAISED WAS CHECKED RATHER THAN ACCEPTED: G3's
marker-count clause and G2's are not in conflict, because G3 counts marker lines in the slice
TARGETS, where the reviewer reads 0, while G2 counts them in the two transport COPIES, where the
reviewer reads 6 by construction. NOTHING FAILED and this round registers no finding.
END-RECORD29
