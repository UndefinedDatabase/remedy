── STEP R32 — F086 Release capability ─────────────────────────
Goal:        Repair the packaging guard that refuses `pip install -e`, so this
             branch's CI can run at all, and record R31's verdict plus the new
             finding R-0598 in the ledger.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0598 and record R31 · C3 the code fix and its tests ·
             C4 the ist-doc paragraph · C5 the handback, then push.

Change:      Exactly these paths, in this order, one commit each except C3.
             C0a `.agent/authored/f086-r32.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `hatch_build.py` AND `tests/test_packaging_smoke.py` TOGETHER
             C4  `docs/system/release-capability-v1.md`
             C5  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at dcf351c6 and must stay untouched: `docs/roadmap/STATUS.md`,
             `README.md`, `.agent/candidates.md`, `.agent/context.md`, `pyproject.toml`,
             `.github/workflows/ci.yml`, `.github/workflows/release.yml`,
             `apps/cli/version_report.py`, `packages/orchestration/ui_server.py`,
             `tests/test_install_smoke.py`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f086-r32.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f086-r32.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL to
   each other; the reviewer stated their expected digest when it delegated, and
   that digest cannot appear in this file because this file is what it digests.
3. PAIR SHAPES, measured by the reviewer with a containment test before emission,
   one reading per pair, quoted here as the test printed it:
     DOCPAIR   `TO contains FROM: False` → REWRITE
     FNPAIR    `TO contains FROM: True`  → APPEND
     HOOKPAIR  `TO contains FROM: False` → REWRITE
     IMPORTPAIR `TO contains FROM: False` → REWRITE
     ISTPAIR   `TO contains FROM: True`  → APPEND
   For each REWRITE prove FROM 1x at dcf351c6 and 0x after, TO 1x after. For each
   APPEND prove FROM 1x at both ends and TO 1x after; never order a FROM-zero
   count for an APPEND. Every FROM was measured at 1x in its target at dcf351c6.
4. TESTAPPEND IS A CODE APPEND, so its obligation is ORDERED EQUALITY, not a
   per-line count (section 4.9, R-0531): the pre-C3 blob of
   `tests/test_packaging_smoke.py` is a byte-exact PREFIX of the post-C3 file,
   TESTAPPEND is an exact SUFFIX of it, and the lines C3's diff ADDS to that path
   are exactly TESTAPPEND's lines IN ORDER.
5. COMMIT ORDER IS FIXED and C4 comes AFTER C3. ISTSLICE states present-tense
   facts about `hatch_build.py` — that `build_target_ships_ui_assets` exists and
   that `initialize` returns before both rules — which are true only once C3 has
   landed. This constraint is what makes those sentences true on landing; it is
   the R-0524 carve-out and you cannot satisfy it by accident.
6. YOU NEVER WRITE A `Done:` PARAGRAPH. R-0598 is registered by C2 and fixed by
   C3, so C3's message and the handback record it as
   `Landed: R-0598 — the editable target is exempted; hatch_build.py + tests`.
   Only the reviewer's authored text sets a resolution.
7. THE PULL REQUEST IS NOT MERGED and not touched. #207 already exists for this
   branch; C5 is followed by `git push` only, which updates it. Do not run
   `gh pr merge`, `gh pr create`, `gh pr edit` or any force push.
8. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
9. Destructive checks run only in a disposable worktree under `.remedy-wt/`. The
   primary checkout satisfies `git status --porcelain` empty after every commit.
10. This block is 327 lines total, of which 160 are slice lines.

<<<SLICE PLAN32
# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. Pull request
#207 is open and NOT merged by this session; it merges at the next feature's Open
PR Gate, and only once its CI check is green.
`.agent/live_review.md` is the source of truth for the open set, for the next free
finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R32: repair R-0598 — the build hook refused the editable target, so
`pip install -e ".[dev]"`, which is CI's first step, failed on every fresh clone
and no test in this branch's only CI run executed. Register the finding, record
R31's verdict, exempt the editable target behind a named predicate, and cover it.

## Next Steps
1. THE REVIEWER GATES R32 and, if it passes, authors `Done: R-0598` for the next
   round. The branch stays open until the CI check on #207 is green.
2. THE PR IS NOT MERGED BY THIS SESSION. It merges at the next feature's start
   through the AGENTS.md Open PR Gate, which is the operator's manual-review
   window; the operator may merge it manually at any time instead.
3. F086 STAYS `[x]` IN THE LEDGER. R-0598 does not falsify the closure's own
   claim — a shipped wheel is still refused without UI assets, and the accepted
   evidence names the commit it was taken at — so the correction is a dated
   ledger entry, never a rewrite of a landed STATUS line.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- CI HAS NEVER RUN GREEN ON THIS BRANCH. R-0598 is the first failure it found;
  a second may sit behind it, because the run died before any test executed.
- The review package is 71% `.remedy-wt/` scratch by member count (R-0403, open
  and routed to a paydown branch); it inflates the package and is not a failure.
<<<END PLAN32

<<<SLICE FIND0598
- R-0598 — High — THE PACKAGING GUARD REFUSED EVERY BUILD TARGET, SO THE PROJECT'S OWN DEV INSTALL AND ITS ENTIRE CI DIED ON ANY FRESH CLONE. `hatch_build.py`'s `RemedyBuildHook.initialize` calls `assert_frontend_assets_built` for every target hatchling hands it, and the editable install is one of them: hatchling's `build_editable` invokes the hook with the target named `editable`, `apps/ui/dist` is build output that no clone carries, and the guard therefore raised `ValueError` before a single dependency was installed. Registered at R32 against the T001 packaging commit f754228e, which introduced the hook. It went unseen for the whole feature because this repository's CI triggers only on `push` to `main` and on `pull_request`, so the branch had no run at all until R31 opened the pull request — run 32402941541 against dcf351c6, conclusion `failure`, ending `error: metadata-generation-failed`, with zero tests executed. The last green run of `main` is 32344673860 at 76661dc1, this branch's own base, so the regression is the branch's and merging it would have turned `main` red. The counter-measure is a named build-target predicate rather than a wider `try`: a SHIPPED artifact must still be refused when it carries no UI, which is what DECISION F086 D1 part (b) rules, and the editable target — which copies no asset anywhere and serves the UI from the checkout it points at — was never in that rule's scope.
<<<END FIND0598

<<<SLICE RECORD31
Gate: R32 — the R31 entry. R31 PASSED with NO finding against its own work, and R-0598, which this round registers, is against the BRANCH rather than against R31 — which is exactly what R31's bundle exposed, because creating the pull request is what first ran CI on this branch at all. Every gate R31's block ordered was RE-EXECUTED by the reviewer over `d1889132..dcf351c6` rather than read from the handback. THE TRANSPORT HELD IN THE PRIMARY FORM: the reviewer's scratch original `.remedy-wt/f086-r31.md`, the committed `.agent/authored/f086-r31.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 832e466af3e5afa5a726adacfbc0cb2d2289f118329cd8072baf6bf8799663bc over 27551 B and 373 lines, and that digest is the one the reviewer stated before delegating. THE RANGE IS EXACTLY WHAT THE HANDBACK DECLARES: seven paths over five single-parent commits, with every `+/-` cell byte-identical to `git diff --numstat` at 373/0, 296/330, 22/25, 4/0 and the closure commit's 32/34, 4/3 and 1/1, and a maximum insertion column of 373 under the 500 cap. THE LEDGER APPEND HELD: the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder is a blank line, R-0597, a blank line and the R31 entry, with both blank separators present. THE CLOSURE COMMIT LANDED AS ORDERED: `docs/roadmap/STATUS.md` is 342 lines at both ends with `- [~] F086` going 1 to 0 and `- [x] F086 — Release capability (` reading 1, each of the four closure values occurring exactly once on that line, and `README.md` moving 124 to 125 lines across its three pairs. WHAT NO GATE OF THAT ROUND COULD SEE is the state of the pull request it created, because the request does not exist until after the last commit and its checks do not finish for minutes after that: run 32402941541 against dcf351c6 ended `failure`, and reading it is this session's work order under the AGENTS.md operator amendment amend0820-gate-autonomy rather than a blocker that ends the session. R31 is therefore no longer the branch terminator, and its verdict lives here in the ledger, where the section 4 item 13 carve-out never had to reach.
<<<END RECORD31

<<<SLICE DOCFROM
ships zero UI files, which DECISION F086 D1 part (b) forbids.
<<<END DOCFROM

<<<SLICE DOCTO
ships zero UI files, which DECISION F086 D1 part (b) forbids. It binds the
targets that SHIP those files and never the editable one, which ships nothing of
its own and serves the UI from the checkout it points at.
<<<END DOCTO

<<<SLICE FNFROM
FRONTEND_DIST_INDEX = "apps/ui/dist/index.html"
REVISION_WHEEL_NAME = "REVISION"
<<<END FNFROM

<<<SLICE FNTO
FRONTEND_DIST_INDEX = "apps/ui/dist/index.html"
REVISION_WHEEL_NAME = "REVISION"
EDITABLE_BUILD_TARGET = "editable"


def build_target_ships_ui_assets(version: str) -> bool:
    """Return whether build target `version` produces an artifact that SHIPS the UI.

    Only the editable target does not. `pip install -e` writes a path hook pointing
    at the checkout, so the UI serves from `apps/ui/dist` in the source tree once it
    is built and nothing is ever copied out; guarding that target refuses the dev
    install on every fresh clone instead. Measured on CI run 32402941541 at
    dcf351c6, where the workflow's own `pip install -e ".[dev]"` step exited 1 and
    no test ran at all. DECISION F086 D1 part (b) governs the SHIPPED artifact,
    which every other target still is.
    """
    return version != EDITABLE_BUILD_TARGET
<<<END FNTO

<<<SLICE HOOKFROM
    def initialize(self, version, build_data):
        assert_frontend_assets_built(self.root)
<<<END HOOKFROM

<<<SLICE HOOKTO
    def initialize(self, version, build_data):
        if not build_target_ships_ui_assets(version):
            return
        assert_frontend_assets_built(self.root)
<<<END HOOKTO

<<<SLICE IMPORTFROM
from hatch_build import FRONTEND_DIST_INDEX, assert_frontend_assets_built
<<<END IMPORTFROM

<<<SLICE IMPORTTO
from hatch_build import (
    FRONTEND_DIST_INDEX,
    BuildHookInterface,
    RemedyBuildHook,
    assert_frontend_assets_built,
    build_target_ships_ui_assets,
)
<<<END IMPORTTO

<<<SLICE TESTAPPEND


@pytest.mark.unit
class TestEditableBuildsAreNotGuarded:
    """`pip install -e` must survive a checkout whose UI was never built.

    The guard as first written refused EVERY build target, so the editable install
    that is CI's first step died on any fresh clone and no test ran at all (R-0598).
    """

    def test_the_dev_environment_exercises_the_plain_hook_class(self):
        # The dev extra never installs hatchling, so the module's documented
        # `object` fallback is what the two hook tests below construct. If that
        # ever changes this fails first and explains them.
        assert BuildHookInterface is object

    def test_the_editable_target_does_not_ship_ui_assets(self):
        assert build_target_ships_ui_assets("editable") is False

    def test_every_other_target_ships_ui_assets(self):
        assert build_target_ships_ui_assets("standard") is True
        assert build_target_ships_ui_assets("sdist") is True

    def test_an_editable_build_is_allowed_without_built_assets(self, tmp_path):
        hook = RemedyBuildHook.__new__(RemedyBuildHook)
        hook.root = str(tmp_path)
        build_data = dict(extra_metadata=dict())
        hook.initialize("editable", build_data)
        assert build_data["extra_metadata"] == dict()

    def test_a_shipped_build_is_still_refused_without_built_assets(self, tmp_path):
        hook = RemedyBuildHook.__new__(RemedyBuildHook)
        hook.root = str(tmp_path)
        with pytest.raises(ValueError) as excinfo:
            hook.initialize("standard", dict(extra_metadata=dict()))
        assert FRONTEND_DIST_INDEX in str(excinfo.value)
<<<END TESTAPPEND

<<<SLICE ISTFROM
Both rules live in plain module-level functions, so the test suite exercises them
without the build backend installed. The revision is written to a temporary
staging directory and never into the source tree: a generated file there would
survive the build and report a revision nobody built.
<<<END ISTFROM

<<<SLICE ISTTO
Both rules live in plain module-level functions, so the test suite exercises them
without the build backend installed. The revision is written to a temporary
staging directory and never into the source tree: a generated file there would
survive the build and report a revision nobody built.

Neither rule binds the EDITABLE target. `build_target_ships_ui_assets` answers
that question and `initialize` returns before both rules when the answer is no.
`pip install -e` writes a path hook into the checkout and copies no asset
anywhere, so refusing it protects nothing while breaking the dev install every
fresh clone starts with — including this repository's own first CI step, which is
how R-0598 was found, on run 32402941541.
<<<END ISTTO

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f086-release-capability; `git status --porcelain`
   EMPTY after every commit and at the handback; `git worktree list` back to one
   line. No reading is taken by overwriting a file in the primary checkout — use
   `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and byte and line counts of `.remedy-wt/f086-r32.md`,
   of `.agent/authored/f086-r32.md` at C0a and of `.agent/last_block.md` at C0b,
   and state whether all three are EQUAL. Constraint 2 names the expected digest.
G3 PLAN. `.agent/plan.md` at C1 byte-equals PLAN32; report its sha256 and line
   count, that the count is under 50, and that `## Goal`, `## Next Steps` and
   `F086` all occur.
G4 LEDGER APPEND. The pre-C2 blob of `.agent/live_review.md` is a byte-exact
   PREFIX of the post-C2 blob, and the remainder is a blank line, FIND0598, a
   blank line and RECORD31 — report the remainder's line count, its sha256, and
   that BOTH blank separators are present.
G5 LEDGER SETS. With `^- R-\d+ — ` as registered and `^Done: R-\d+ — ` as
   resolved, report both counts plus open and `Landed:` at dcf351c6 and at C2.
   The reviewer measured 180 / 6 / 174 / 0 at dcf351c6. The registered set must
   gain EXACTLY `R-0598` and lose none; the resolved set must be UNCHANGED.
G6 ITEM-20 SCAN. Over C2's ADDED lines only, delete backtick-quoted spans first,
   then report the count of `\bHEAD\b` — it must be 0. Run the SAME extractor
   over `fd166295`'s added lines to that file as a RED CONTROL and report that
   count too; a control that does not read above 0 makes the gate worthless.
G7 ITEM-26 HEADER. Report how many lines begin `Gate: R` at dcf351c6 and at C2,
   which header keys occur more than once at each end, that
   `Gate: R32 — the R31 entry.` occurs 1x, that it is the LAST such header, and
   that the text following it begins `R31 ` once its leading space is stripped.
   The reviewer measured 29 headers at dcf351c6 with exactly
   `Gate: R19 — the R18 entry` duplicated.
G8 THE PAIRS. For each of DOCPAIR, FNPAIR, HOOKPAIR, IMPORTPAIR and ISTPAIR
   report the counts constraint 3 assigns to its shape, and for each edited file
   report that the post-commit file equals the pre-commit blob with that single
   occurrence replaced and NOTHING else changed, with the file's sha256 and its
   line count before and after.
G9 THE CODE APPEND. Report constraint 4's ordered equality for
   `tests/test_packaging_smoke.py` at C3: prefix preserved, TESTAPPEND an exact
   suffix, and the lines C3's diff adds to that path equal TESTAPPEND's lines in
   order. Report the file's sha256.
G10 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/test_packaging_smoke.py tests/test_build_revision.py -q -rf`
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/docs/ -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q`
   The reviewer measured, at dcf351c6, 9 passed for the first selection, 295 for
   tests/docs/ and 42 for the canary; the first selection MUST rise, because C3
   adds tests to it.
G11 THE PROOF THAT THE NEW TESTS GUARD THE FIX. In a disposable worktree at C3,
   delete the two lines `        if not build_target_ships_ui_assets(version):`
   and `            return` from `hatch_build.py` — counted 1x each in THAT file
   first — and run
   `python3 -m pytest tests/test_packaging_smoke.py -q -rf`. Report the exit code
   and the failing node ids. Then remove and prune the worktree and report
   `git worktree list`. The reviewer measured this same revert going RED naming
   only `TestEditableBuildsAreNotGuarded::test_an_editable_build_is_allowed_without_built_assets`.
G12 LINT. `python3 -m ruff check hatch_build.py tests/test_packaging_smoke.py`
   with the repository's own configuration and no `--isolated`. Report the exact
   command and its output. The reviewer measured `All checks passed!` for these
   two paths at dcf351c6, so exit 0 is the honest reading here.
G13 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only dcf351c6..HEAD`
   and state that it equals the Change list with no path on either side alone;
   that each of the ten paths the Change section names as untouched is PRESENT at
   dcf351c6 and absent from that range; that every commit in the range has one
   parent; that every `git reflog` entry of this round is `commit:`; and each
   commit's insertion column from `git diff --numstat`, every one under 500. Per
   checklist item 28 the same `+/-` cells appear in the handback's `## Commits`
   table and must be byte-identical to the tool's output there.
G14 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
   `hatch_build.py` and `tests/test_packaging_smoke.py` at C3 and
   `docs/system/release-capability-v1.md` at C4. Every count must be 0.
G15 THE PUSH. After C5, `git push` and report its real output, then re-read
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
   report it verbatim. Do NOT merge and do NOT wait on the CI run; the reviewer
   watches it. C5's own insertion count and the push cannot appear inside C5, so
   they belong in the round report, not in `.agent/handoff.md`.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, at most 60
             lines or a DECISION D15 stated-cause line naming the real count and
             the mandated content that caused it. It carries the item-status
             table for the C0a..C5 bundle, the `## Commits` table G13 pins, one
             LINE per gate rather than its transcript (R-0582), and the
             `Landed: R-0598` line constraint 6 fixes. The full transcripts go in
             the round report you return, never in the file.
──────────────────────────────────────────────────────────────
