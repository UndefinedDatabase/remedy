── STEP R11 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Build the FIRST half of T002a: environment scrubbing in `exec_guard.py` behind an
opt-in `env_allowlist`, with a `FORBIDDEN_ENV_KEYS` floor a wrong allowlist cannot
lower. It comes before the migration because amendment F085 D1 gives the builder
class an env allowlist, so migrating a site first would either skip that allowlist
or invent it at the site. NO call site is migrated here and the module still has no
callers, so nothing in the running system becomes safer — gate 11 proves that.

Base: `2587780d9aa0d67d710e63193b3186ea3fc56a1d`, the R10 handback commit and the
tip of `feature/f085-sandbox-hardening`. Stay on this branch; create no other.

Bundle (ordered, one commit each; none added, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r11.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `packages/orchestration/exec_guard.py` and its test file := the GUARD pairs,
      the TEST pairs and NEWTESTS — ONE commit, code and its tests together
  C2  `.agent/plan.md` := the PLAN pair applied
  C3  rewrite `.agent/handoff.md` (the handback)

Slice convention:
Each authored unit sits between a `<<<SLICE NAME>>>` and a `<<<END NAME>>>` marker,
each occupying a line whose ENTIRE content is that marker. Extract slices by those
marker LINES programmatically and apply byte-verbatim; a `<<<` mid-line inside a
slice is prose, and no marker line reaches a target file. The slices are NEWTESTS
and the FROM/TO halves of PLAN, GUARD1..GUARD7, TEST1 and TEST2, each ending with a
single trailing newline.

Round type: SPLIT — the change set reaches `packages/`, so production code never
merges self-certified: the reviewer gates, you execute.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block byte for byte to `.agent/authored/f085-r11.md`.
   The reviewer's original is at `.remedy-wt/f085-r11.md` and its sha256 is in the
   delegation; COPY that file rather than retyping it (`shutil.copyfile` is fine —
   the gate names a byte property, not a tool). Verify the digest, then commit alone.
2. C0b — copy the COMMITTED `.agent/authored/f085-r11.md` over
   `.agent/last_block.md`, whole file. Commit alone.
3. C1 — ONE commit over exactly two files.
   a. In `packages/orchestration/exec_guard.py` apply GUARD1..GUARD7 in order.
      Shapes, declared per pair and to be proved as declared: REWRITE for GUARD1,
      GUARD2, GUARD4 and GUARD6; APPEND for GUARD3, GUARD5 and GUARD7. Each FROM
      occurs exactly once immediately before its own replacement.
   b. In `tests/orchestration/test_exec_guard.py` apply TEST1 (REWRITE) and TEST2
      (APPEND), then append NEWTESTS at the very END of the file preceded by exactly
      TWO blank lines — the separator PYTHON requires between top-level definitions,
      NOT the one-blank-line convention of `.agent/live_review.md`, whose reuse for a
      source file was finding R-0500. NEWTESTS already carries two blank lines
      internally. Gate 8 measures it, since stable ruff never evaluates E301-E306.
   c. Touch NO other file and migrate NO call site: the five builder sites of
      amendment F085 D1 stay exactly as they are. Gate 11 proves it.
4. C2 — apply the PLAN pair to `.agent/plan.md`, a REWRITE spanning `## Current
   Step` and `## Next Steps`; `## Goal` and `## Risks` are NOT touched and must come
   through byte-identical. Commit alone.
5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its state
   block repeats the delegation's Fortschritt line verbatim. A DECISION D15
   stated-cause overage is allowed with its cause named; sections are never dropped
   to meet the cap. Its "Next" section names, in order, Phase 1 rule 1 of
   self_drive_protocol.md — re-read `.agent/STOP` — and only THEN the Open PR Gate.

Constraints:

1. The guardrails G1-G8 of docs/agents/self_drive_protocol.md bind unchanged and
   this block restates none of them — read that file before you start. Beyond them:
   no PR is created and none is merged this round; `.agent/STOP` is re-read from
   disk before the FIRST and again before the LAST commit; and all gate scratch,
   including any disposable worktree, lives under the gitignored `.remedy-wt/` and
   never enters the change set.
2. Apply every slice byte-verbatim. If a slice looks wrong, STOP and say so in the
   handback rather than correcting it — a corrected slice makes the reviewer's proof
   measure text the reviewer never wrote.
3. The change set is exactly `.agent/authored/f085-r11.md`, `.agent/last_block.md`,
   `packages/orchestration/exec_guard.py`, `tests/orchestration/test_exec_guard.py`,
   `.agent/plan.md` and `.agent/handoff.md`. Nothing under `docs/`, `apps/`,
   `scripts/` or `docs/roadmap/`. `.agent/context.md` and `.agent/decisions.md` are
   deliberately NOT updated: scope and constraints are unchanged.

Done when — run each gate from the repository root and report its exact output:

G1  `git status --porcelain` EMPTY before each commit; `.agent/STOP` absent per
    constraint 1; `git worktree list` exactly one line at the handback.
G2  TRANSPORT: sha256 of `.remedy-wt/f085-r11.md`, the committed
    `.agent/authored/f085-r11.md` and the committed `.agent/last_block.md` — all three
    EQUAL. Report the one digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD: report sha256, bytes and lines; confirm `## Goal`,
    `## Next Steps`, a `\bF\d{3}\b` match, under 50 lines, and that `## Goal` and
    `## Risks` are byte-identical to their text at 2587780d.
G4  PAIR SHAPES over the WHOLE of each target file at HEAD. REWRITES PLAN, GUARD1,
    GUARD2, GUARD4, GUARD6, TEST1: FROM 0 times, TO exactly 1 time. APPENDS GUARD3,
    GUARD5, GUARD7, TEST2: FROM exactly 1 time (the TO contains it verbatim, which is
    what makes it an append) and each TO-ONLY added line exactly once AMONG THE LINES
    THAT COMMIT ADDS (§4 item 9). NEWTESTS occurs once and the test file ENDS with
    it. Report `git show --numstat` for C1 and C2 as a READING, not an assertion.
G5  `git diff --name-only 2587780d..HEAD` equals the constraint-3 set minus
    `.agent/handoff.md`, measured before C3 (R-0149, R-0494). Report every path.
G6  IMPORT PATH, so the suite below cannot be measuring another checkout, run from
    the repository root and reporting both values:
    `python3 -c "import packages.orchestration.exec_guard as m; print(m.__file__, hasattr(m, 'scrub_child_env'))"`
G7  DETERMINISM: run `python3 -m pytest tests/orchestration/test_exec_guard.py -q`
    TEN consecutive times at HEAD; report all ten exit codes and summary lines, and
    the test count you OBSERVE rather than one you expect.
G8  SEPARATOR MEASUREMENT over the whole of `tests/orchestration/test_exec_guard.py`,
    as two lists at base AND at HEAD, compared and not asserted:
    `[len(m.group(0)) for m in re.finditer(r"\n+(?=@pytest\.mark\.subprocess)", text)]`
    and the same for `r"\n+(?=def test_)"`.
G9  `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`
    → report the exit code, under the repository's OWN configuration and NOT
    `--isolated` (R-0463). It was exit 0 for both files at base, so a red here is new;
    it says nothing about blank lines, which G8 measures.
G10 `python3 -m pytest tests/cli/test_golden_path.py -q` → the canary; the reviewer
    measured `42 passed` at 2587780d. Then, this round rewriting `.agent/` state:
    `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q`
    → the reviewer measured `157 passed` at 2587780d.
G11 NO CALLER, the honesty gate: `grep -rln "exec_guard" packages apps scripts tests`
    names exactly `packages/orchestration/exec_guard.py` and
    `tests/orchestration/test_exec_guard.py`. Report every path; a third means a call
    site was migrated and constraint 3c was broken.
G12 INSERTIONS (the `+` column) per commit for C0a, C0b, C1 and C2 — not C3, whose
    own count cannot exist while its text is written (R-0489). None may exceed 500.
G13 HISTORY: `git log --format=%p 2587780d..HEAD` shows one parent per commit; report
    the reflog and confirm no amend, rebase, reset, branch switch or force-push.

Handback: completion report + rewrite `.agent/handoff.md`. Push after C2 and again
after C3, then run
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`, report its
output and create no PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLANF>>>
## Current Step
R10, this round: record the R9 PASS, resolve R-0500 and register R-0501. Pure
record round — no code, no tests, no behaviour, `.agent/` state only.

## Next Steps
1. R11 builds the FIRST half of T002a: environment scrubbing in `exec_guard.py`
   behind an opt-in `env_allowlist`, with a `FORBIDDEN_ENV_KEYS` floor a wrong
   allowlist cannot lower, plus tests for the secret-like variable, the R-0202
   variable and the untouched no-allowlist path.
2. T002a's migration half: the five builder sites of amendment F085 D1 —
   `managed_builder_execution.py`:1160, `pingpong_provider.py`:952, 1075, 1208
   and `stream_evidence.py`:595 — move to `run_guarded` with a builder policy
   and behaviour-equality goldens.
3. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
4. T002b-d, then T003 — network posture, limitations document, README link.
<<<END PLANF>>>

<<<SLICE PLANT>>>
## Current Step
R11, this round: the FIRST half of T002a — environment scrubbing in
`exec_guard.py` behind an opt-in `env_allowlist`, with a `FORBIDDEN_ENV_KEYS`
floor a wrong allowlist cannot lower. No call site is migrated, so the running
system gains nothing yet and no containment claim follows from this round.

## Next Steps
1. T002a's migration half: the five builder sites of amendment F085 D1 —
   `managed_builder_execution.py`:1160, `pingpong_provider.py`:952, 1075, 1208
   and `stream_evidence.py`:595 — move to `run_guarded` with a builder policy
   and behaviour-equality goldens.
2. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
3. T002b-d, then T003 — network posture, limitations document, README link.
<<<END PLANT>>>

<<<SLICE GUARD1F>>>
- No environment scrubbing and no allowlist. `ExecGuardPolicy.env` is handed to
  the child UNCHANGED; scrubbing is T002.
<<<END GUARD1F>>>

<<<SLICE GUARD1T>>>
- No environment scrubbing UNLESS the policy asks for it: with
  `env_allowlist=None` the policy's `env` reaches the child UNCHANGED, which every
  T001 test relies on. CHOOSING an allowlist per command class is T002a's
  migration half and is not done here.
<<<END GUARD1T>>>

<<<SLICE GUARD2F>>>
from collections.abc import Sequence
<<<END GUARD2F>>>

<<<SLICE GUARD2T>>>
from collections.abc import Mapping, Sequence
<<<END GUARD2T>>>

<<<SLICE GUARD3F>>>
    "core_file_bytes": "RLIMIT_CORE",
}
<<<END GUARD3F>>>

<<<SLICE GUARD3T>>>
    "core_file_bytes": "RLIMIT_CORE",
}

#: Never inherited by a guarded child, whatever an allowlist says. Same spelling and
#: members as `managed_builder_execution._FORBIDDEN_ENV_KEYS`, kept here so the guard
#: denies them even when a caller's allowlist is wrong.
FORBIDDEN_ENV_KEYS = frozenset({
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "CLAUDE_API_KEY",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
    "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
    "GITHUB_TOKEN", "GH_TOKEN", "GITLAB_TOKEN",
    "DATABASE_URL", "REDIS_URL",
})


def scrub_child_env(source: Mapping[str, str], allowlist: Sequence[str]) -> dict[str, str]:
    """Build a child environment from `source`, keeping ONLY allowlisted keys.

    A `FORBIDDEN_ENV_KEYS` member is dropped even when the allowlist names it: the
    allowlist is a caller's policy, this set is the guard's floor. An undefined key
    is ABSENT, not empty — a build tool reads empty as "set to nothing".
    """
    keep = set(allowlist) - FORBIDDEN_ENV_KEYS
    return {key: source[key] for key in sorted(keep) if key in source}
<<<END GUARD3T>>>

<<<SLICE GUARD4F>>>
    `env` is passed through unchanged: scrubbing is T002, not stage 1.
<<<END GUARD4F>>>

<<<SLICE GUARD4T>>>
    `env` reaches the child unchanged while `env_allowlist` is None. When
    `env_allowlist` names keys, the child's environment is built by
    `scrub_child_env` from `env` — or from `os.environ` when `env` is None —
    keeping only those keys and never one in `FORBIDDEN_ENV_KEYS`.
<<<END GUARD4T>>>

<<<SLICE GUARD5F>>>
    env: dict[str, str] | None = None
<<<END GUARD5F>>>

<<<SLICE GUARD5T>>>
    env: dict[str, str] | None = None
    env_allowlist: tuple[str, ...] | None = None
<<<END GUARD5T>>>

<<<SLICE GUARD6F>>>
    started = time.monotonic()
    proc = subprocess.Popen(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=policy.cwd,
        env=policy.env,
<<<END GUARD6F>>>

<<<SLICE GUARD6T>>>
    child_env = policy.env
    if policy.env_allowlist is not None:
        child_env = scrub_child_env(
            os.environ if policy.env is None else policy.env, policy.env_allowlist
        )

    started = time.monotonic()
    proc = subprocess.Popen(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=policy.cwd,
        env=child_env,
<<<END GUARD6T>>>

<<<SLICE GUARD7F>>>
Why the wall timeout is supervised here rather than forwarded as a `timeout=`
<<<END GUARD7F>>>

<<<SLICE GUARD7T>>>
What an allowlist does NOT bound, stated where a reader will look for it: it
bounds what the PARENT hands over, never what the child's own runtime then adds
to itself. A CPython child spawned with a restricted environment sets `LC_CTYPE`
during PEP 538 locale coercion, so the child's environment is a SUPERSET of the
scrubbed one. Nothing here can prevent that, and stage 1 does not pretend to.

Why the wall timeout is supervised here rather than forwarded as a `timeout=`
<<<END GUARD7T>>>

<<<SLICE TEST1F>>>
from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded
<<<END TEST1F>>>

<<<SLICE TEST1T>>>
from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded, scrub_child_env
<<<END TEST1T>>>

<<<SLICE TEST2F>>>
    found = subprocess.run(["pgrep", "-af", MARKER], capture_output=True, text=True)
    return [line for line in found.stdout.splitlines() if "pgrep" not in line]
<<<END TEST2F>>>

<<<SLICE TEST2T>>>
    found = subprocess.run(["pgrep", "-af", MARKER], capture_output=True, text=True)
    return [line for line in found.stdout.splitlines() if "pgrep" not in line]


#: A child that prints its whole environment, one KEY=VALUE per line.
_ENV_DUMP = (
    "import os, sys\n"
    "sys.stdout.write(''.join(f'{k}={v}\\n' for k, v in sorted(os.environ.items())))\n"
)

#: CPython adds this to any child spawned with a restricted environment (PEP 538
#: locale coercion). It is the interpreter's, not the guard's, so assertions below
#: subtract it rather than crediting the guard with producing it.
_INTERPRETER_ADDED_ENV_KEYS = frozenset({"LC_CTYPE"})


def _dumped(result) -> dict[str, str]:
    """The child's environment from its stdout, minus what the interpreter added.

    Subtract-if-present, never assert-present: a build that does not coerce the
    locale has nothing to subtract and the assertions still hold.
    """
    lines = result.stdout.decode().splitlines()
    parsed = dict(line.split("=", 1) for line in lines if "=" in line)
    return {k: v for k, v in parsed.items() if k not in _INTERPRETER_ADDED_ENV_KEYS}
<<<END TEST2T>>>

<<<SLICE NEWTESTS>>>
@pytest.mark.subprocess
def test_no_allowlist_hands_the_environment_to_the_child_unchanged():
    """The T001 contract, pinned: without an allowlist NOTHING is scrubbed.

    A forbidden key sits in `env` on purpose and arrives, so a migration that
    forgets its allowlist is visibly unprotected, not quietly half-protected.
    """
    passed = {"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "sk-unscrubbed-by-design"}

    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(wall_timeout_seconds=10.0, env=passed),
    )

    assert result.returncode == 0
    assert _dumped(result) == passed


@pytest.mark.subprocess
def test_the_allowlist_keeps_only_the_variables_it_names():
    """An allowlisted key survives; an unlisted key never reaches the child."""
    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(
            wall_timeout_seconds=10.0,
            env={"PATH": "/usr/bin", "REMEDY_KEPT": "yes", "REMEDY_DROPPED": "no"},
            env_allowlist=("PATH", "REMEDY_KEPT"),
        ),
    )

    assert result.returncode == 0
    assert _dumped(result) == {"PATH": "/usr/bin", "REMEDY_KEPT": "yes"}


@pytest.mark.subprocess
def test_a_secret_like_variable_never_reaches_the_child_even_when_allowlisted():
    """`FORBIDDEN_ENV_KEYS` is the guard's floor: a wrong allowlist cannot lower it."""
    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(
            wall_timeout_seconds=10.0,
            env={"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "sk-should-never-appear"},
            env_allowlist=("PATH", "ANTHROPIC_API_KEY"),
        ),
    )

    assert result.returncode == 0
    assert "ANTHROPIC_API_KEY" not in _dumped(result)
    assert b"sk-should-never-appear" not in result.stdout
    assert _dumped(result) == {"PATH": "/usr/bin"}


@pytest.mark.subprocess
def test_the_ui_no_auto_build_variable_survives_an_allowlist_that_names_it():
    """R-0202: the variable a spawn path once dropped is allowlistable and arrives."""
    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(
            wall_timeout_seconds=10.0,
            env={"PATH": "/usr/bin", "REMEDY_UI_NO_AUTO_BUILD": "1"},
            env_allowlist=("PATH", "REMEDY_UI_NO_AUTO_BUILD"),
        ),
    )

    assert result.returncode == 0
    assert _dumped(result)["REMEDY_UI_NO_AUTO_BUILD"] == "1"


def test_scrub_child_env_drops_a_key_the_source_never_defined():
    """An allowlisted but undefined key is ABSENT, never present and empty."""
    scrubbed = scrub_child_env({"PATH": "/usr/bin"}, ("PATH", "NEVER_SET_ANYWHERE"))

    assert scrubbed == {"PATH": "/usr/bin"}
    assert "NEVER_SET_ANYWHERE" not in scrubbed
<<<END NEWTESTS>>>
