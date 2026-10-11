# Handback — F297 round 1: claim, book F205 R10/S4, slice list, T002 to T004 landed

## Session

SESSION 1 of feature F297 · round 1 · rounds so far 1

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~12 % (T001 to T004 landed · T005 to T025 open) — Schätzung

## Range

Review of `9dab4d7f0`..`HEAD`.

## Commits

### 75b45c750 F297 R1 C1: claim F297, book F205 R10 and S4, re-head the ledger, DECISION F297 D1 and the slice list

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r1.md` | +178/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r1/prep/block.md` |
| `docs/roadmap/STATUS.md` | +1/-1 | F297's STATUS line claimed, `[ ]` to `[~]` |
| `.agent/live_review.md` | +32/-26 | re-headed to F297, Owner line moves R-1248 to F305, and the appended `Gate: F205 R10` and `Gate: F205 S4` paragraphs (VERDICT PASS each) |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D1: the slice list, the two findings carried at the claim, R-1248 moved to F305, R-1241 as the closing structural step |
| `.agent/prose_slips.md` | +4/-0 | four dated lines carried from F205's handbacks (round 10 ×2, session 2 ×1, session 4 ×1) |
| `.agent/plan.md` | +19/-17 | rewritten in full for F297 round 1 |
| `.agent/context.md` | +10/-15 | rewritten in full for F297 round 1 |
| `docs/roadmap/features/T2_F297.md` | +79/-0 | `## Task slicing` section (T001 to T025) and the Acceptance lines for the ids F297 takes |
| `docs/roadmap/features/T13_F305.md` | +3/-0 | R-1248's Acceptance line (moved here by DECISION F297 D1) |

### e05e9d396 F297 R1 C2: seven tripwire tests import study before patching intake, and the orphan guard reads the git hooks (R-1172, R-1243)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_decision_cmd.py` | +4/-0 | imports `packages.orchestration.study` directly above the first `monkeypatch.setattr` of `intake.make_provider_call_fn` (R-1172) |
| `tests/cli/test_do_flags.py` | +4/-0 | same repair |
| `tests/cli/test_do_order_file.py` | +4/-0 | same repair |
| `tests/cli/test_do_project_repo.py` | +4/-0 | same repair |
| `tests/cli/test_quick_start.py` | +4/-0 | same repair |
| `tests/cli/test_status_cmd.py` | +4/-0 | same repair |
| `tests/orchestration/test_resume_cli.py` | +4/-0 | same repair |
| `tests/test_no_orphan_modules.py` | +7/-4 | entry-point rule now reads every file under `.githooks/`; the hand-written `scripts/check_commit_subject.py` `ALLOWED_UNWIRED` row deleted; `_entry_point_files` reads `(".githooks", ("*",))`; the planted-orphan test gains `.githooks/commit-msg` and `scripts/from_hook.py` (R-1243) |

### 2da913d13 F297 R1 C3: the F298 spec states its version rule, and the contract page names the table of every exit code (R-1242)

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T12_F298.md` | +2/-2 | the spec states the interface-version rule ("rises with every addition") instead of a literal number, with the R-1242 reference |
| `docs/system/machine-client-contract-v1.md` | +3/-0 | the "Exit codes" section intro names the generated "Exit codes of every command" table at the page's end |
| `tests/cli/test_client_interface.py` | +11/-0 | new test `test_the_paths_exit_code_table_points_at_the_generated_table_of_every_code` holding the pointer against the generated section (R-1242) |

### this commit F297 R1 C4: handback, and two operator questions

| Path | +/- | Reason |
|---|---|---|
| `.agent/operator_questions.md` | +40/-1 | Q11 (four real order texts the session may not read) and Q12 (mission card moved to F305, DECISION F297 D1), replacing the `EMPTY` line |
| `.agent/handoff.md` | this commit | this file (self-reference rule, docs/agents/handback_template.md) |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. The block states the Open PR Gate already ran and found none open; re-checked before C0 and again found none.
- `ListAgents` (read-only, before C4) — this session's own running subagent (research only, no repo writes), one busy peer session "Universe nächste 10 Features" and one idle peer session "Universe-Plan WEITER Version 3"; neither peer is named as touching F297 or `feature/f297-findings-paydown-v7`.
- `git push -u origin feature/f297-findings-paydown-v7` — plain push, no force; reported in the worker's final reply, along with the post-push `git rev-parse HEAD origin/feature/f297-findings-paydown-v7`.

## Verification

**Preconditions (before C0):** `git status --porcelain` empty; `git rev-parse HEAD` read `9dab4d7f01f9574f23cf637861f74222107fcb21`, the required base.

**Block and prepared-file digests (before any write):** `wc -l` on `block.md` read `178`; `sha256sum` read
`d02430ed49ad19318b9ef1fcd1f8ea725d4b6e37613db87cf2529acfdcecea4a` — both equal to the values the
prompt delivered. All 27 Bundle-listed prepared files (`block.md`, the 20 `dry-*` files, the 3
`append-*.txt` files, `verify.py`, `run_selection.py`, `selection.txt`) hashed via a python3 script
under `.remedy-wt/f297-r1-worker/check_digests.py`: every one read `OK`, final line `ALL_OK`.

**C1:** `python3 -I c1_copy.py` copied the block and the eight `dry-*` files; each printed
`cmp_equal=True` and the recomputed sha256 of each `dry-*` source matched the Bundle's stated
digest. Before commit, `git diff --cached --numstat` read exactly: `178 0 .agent/authored/f297-r1.md`,
`1 1 docs/roadmap/STATUS.md`, `32 26 .agent/live_review.md`, `12 0 .agent/decisions.md`,
`4 0 .agent/prose_slips.md`, `19 17 .agent/plan.md`, `10 15 .agent/context.md`,
`79 0 docs/roadmap/features/T2_F297.md`, `3 0 docs/roadmap/features/T13_F305.md` — all matching the
block's required readings. `git branch --show-current` read `feature/f297-findings-paydown-v7`
before the commit.

**C2:** `python3 -I c2_copy.py` copied the eight test/guard files; each printed `cmp_equal=True`.
Before commit, `git diff --cached --numstat` read `4 0` for each of the seven tripwire files and
`7 4` for `tests/test_no_orphan_modules.py`, matching the block exactly. `git diff --cached` was
read in full: every tripwire file gained the same three comment lines plus
`import packages.orchestration.study  # noqa: F401` directly above its first
`monkeypatch.setattr("packages.orchestration.intake.make_provider_call_fn", tripwire)`; the guard
gained the `.githooks/` docstring sentence, lost the `scripts/check_commit_subject.py`
`ALLOWED_UNWIRED` row, gained `(".githooks", ("*",))` in `_entry_point_files`, and the planted-tree
fixture gained `.githooks/commit-msg` and `scripts/from_hook.py` — matching the block's description
exactly. `git branch --show-current` read `feature/f297-findings-paydown-v7` before the commit.

**C3:** `python3 -I c3_copy.py` copied the three files; each printed `cmp_equal=True`. Before
commit, `git diff --cached --numstat` read `2 2 docs/roadmap/features/T12_F298.md`,
`3 0 docs/system/machine-client-contract-v1.md`, `11 0 tests/cli/test_client_interface.py`, in that
order — matching the block exactly. `git status --porcelain -- tests/cli/test_machine_client_contract.py`
read empty: that file was not touched. `grep -n "Exit codes of every command" docs/system/machine-client-contract-v1.md`
read two lines (the new intro sentence and the generated heading), confirming the pointer resolves.
`git branch --show-current` read `feature/f297-findings-paydown-v7` before the commit.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f297-r1/prep/verify.py /home/decodeux/Repos/remedy` →
every line `True` (file-equality checks for all 20 touched paths, the decisions/prose_slips
base-plus-slice checks, and the ledger-tail checks), last line `ALL True`, exit 0.

**Gate 2:** `python3 -m ruff check tests/test_no_orphan_modules.py tests/cli/test_client_interface.py
tests/cli/test_decision_cmd.py tests/cli/test_quick_start.py tests/cli/test_do_order_file.py
tests/cli/test_do_flags.py tests/cli/test_do_project_repo.py tests/cli/test_status_cmd.py
tests/orchestration/test_resume_cli.py` → `All checks passed!`, exit 0.

**Gate 3:** `python3 /home/decodeux/Repos/remedy/.remedy-wt/f297-r1/prep/run_selection.py /home/decodeux/Repos/remedy`
(one `pytest -q -n auto -rfEs -p no:cacheprovider` invocation over `selection.txt`'s 19 entries plus
every `tests/test_*.py`) → three SKIPPED lines (`tests/test_agent_tooling.py:43` D12 quarantine,
`tests/test_install_smoke.py:175` opt-in install smoke, `tests/test_repair_context_reviewer_memory.py:257`
UI source not found), no FAILED or ERROR line, no `process(es) behind` line, summary
`3872 passed, 3 skipped in 40.72s`, `exit 0`. The reviewer's dry tree (no `apps/ui/node_modules`)
read `3870 passed, 5 skipped`; the primary checkout ran the two UI-toolchain tests that dry tree
skipped, so `+2 passed, -2 skipped` — consistent with the block's stated variance.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` → `{"check_count": 6, "fail_count": 0,
"ok": true, "passed": true, ...}`, all six checks `pass` (`handler_import` 184 handlers,
`live_review_verdict` last Gate PASS, `plan_consistency` unchecked=0, `relevant_untracked`
untracked=0 relevant=0, `repo_root_hygiene` clean, `high_blockers_open` none open), exit 0.

**Gate 5:** `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172',
'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235', 'R-1236', 'R-1237', 'R-1238',
'R-1239', 'R-1240', 'R-1241', 'R-1242', 'R-1243', 'R-1246', 'R-1247', 'R-1248', 'R-1249', 'R-1250']`
— the 29 ids in the required order, exit 0.

**Gate 6:** `python3 -c "print(open('docs/roadmap/STATUS.md', encoding='utf-8').read().count('- [~] F297 — Findings paydown v7'))"`
→ `1`, exit 0.

No mutation red-proof was run (the reviewer ran them in its dry tree per amend0930-test-load rule
4). No full suite was run. No two test commands ran at once; each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by `filecmp.cmp`
(disk-to-disk, not shallow), all read `True`; the 27-file digest pre-check (above) additionally
confirmed every prepared source's sha256 against the Bundle's stated values before any copy:

1. `.remedy-wt/f297-r1/prep/block.md` → `.agent/authored/f297-r1.md`: 178 lines both, sha256
   `d02430ed49ad19318b9ef1fcd1f8ea725d4b6e37613db87cf2529acfdcecea4a` both.
2. `dry-STATUS.md` → `docs/roadmap/STATUS.md`: cmp equal, sha256
   `31a121ba8fecf1eb35c0b1abf015e332371d0763fbb0f7887593d844f7ccf645` both.
3. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, sha256
   `335a2427035fb78cc3360f9445b1fd114538d2f4a14739b79f172d65752e197f` both.
4. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, sha256
   `7922436cece7606291b45243d12863544d0c700b546e5fc42c69d30fd660f26d` both.
5. `dry-prose_slips.md` → `.agent/prose_slips.md`: cmp equal, sha256
   `44adfeb79fb405019dbe2e75c3332933e607add1b2545f51945e45687b654fbc` both.
6. `dry-plan.md` → `.agent/plan.md`: cmp equal, sha256
   `43db6bf38fb95296c97f5558d75059b9925bfb3991d7685b00a828d57a4cdde8` both.
7. `dry-context.md` → `.agent/context.md`: cmp equal, sha256
   `5790b569bec4217ed99b65e885bcc65e5164f9410937c99bb55096a7fdfdc500` both.
8. `dry-T2_F297.md` → `docs/roadmap/features/T2_F297.md`: cmp equal, sha256
   `4e4b48315f3a2971f252433bc67e1f0c6cc8fcb53be37d58f8fad70e5283beb5` both.
9. `dry-T13_F305.md` → `docs/roadmap/features/T13_F305.md`: cmp equal, sha256
   `c08a7f5c6642284c8756492600382858175da43c08e818f96339fa2de7a1a0b8` both.
10. `dry-test_decision_cmd.py` → `tests/cli/test_decision_cmd.py`: cmp equal, sha256
    `4b7e5feac806a8eebee911d306da5827392ab2730c09381d2fe830ee7bdb65de` both.
11. `dry-test_quick_start.py` → `tests/cli/test_quick_start.py`: cmp equal, sha256
    `4015a95ea6946eb984b68be116dee921355a144e6207a02e1c911eb307debd07` both.
12. `dry-test_do_order_file.py` → `tests/cli/test_do_order_file.py`: cmp equal, sha256
    `f3de0c7d94f4a96feaa6fc55e0870a28942dbb27aa6e1e966fff5a842c75e758` both.
13. `dry-test_do_flags.py` → `tests/cli/test_do_flags.py`: cmp equal, sha256
    `f2c861615a4b02b426a20ac960ff4e987838ab06c92ab132cb40bb37681268bd` both.
14. `dry-test_do_project_repo.py` → `tests/cli/test_do_project_repo.py`: cmp equal, sha256
    `46d9f9fc242bd498d2c9e932e12b3117b2e2e6ea4179a0089c2197d2bbf3f84c` both.
15. `dry-test_status_cmd.py` → `tests/cli/test_status_cmd.py`: cmp equal, sha256
    `771af5a1004a7ce00517c4b2a2541ab9fd8a6290f51c62d1bccbfc260210598f` both.
16. `dry-test_resume_cli.py` → `tests/orchestration/test_resume_cli.py`: cmp equal, sha256
    `4169c3da16cbdf719dc41a7f66614ad1b1f02b1c81d35554dc74ab0f337cf0cb` both.
17. `dry-test_no_orphan_modules.py` → `tests/test_no_orphan_modules.py`: cmp equal, sha256
    `a18dbf60f28c88a16caee55401effdddd7c0654157779609a92e2eaad0218dc7` both.
18. `dry-T12_F298.md` → `docs/roadmap/features/T12_F298.md`: cmp equal, sha256
    `2b0f8bcf99839b5c3d751e030ba343b0a3b786badc45bc80832c6ab033a5d1c1` both.
19. `dry-machine-client-contract-v1.md` → `docs/system/machine-client-contract-v1.md`: cmp equal,
    sha256 `ddfa7eff182d2b6370e3390fa9a0502a985fda5bf6a7d9a1cd761eccadf2d7db` both.
20. `dry-test_client_interface.py` → `tests/cli/test_client_interface.py`: cmp equal, sha256
    `b4f6ecb41554791d99cde0205374f3af63256ddd71f51842bf734120bc333237` both.
21. `dry-operator_questions.md` → `.agent/operator_questions.md`: cmp equal, sha256
    `81995b5756d273d42450ec2e8dc941bdd410ff4651588aabf28d9b1798916794` both.

The three `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`,
`append-prose_slips.txt`) were listed in the Bundle and digest-checked (all `OK`), but C1 orders
copying the eight whole `dry-*.md` files, which already carry that content baked in; the
`append-*.txt` files were not applied separately, and nothing in the block calls for that.

## Deviations & assumptions

1. **Commit trailer.** The block (C4's constraints section) orders the trailer
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` on every commit. This session's own
   system instructions (not a `CLAUDE.md` or memory rule, so the block does not out-rank them) order
   `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` for every commit made from here on,
   which this session is. All four commits (C1 to C4) carry the Sonnet 5 trailer, not the block's
   literal text.
2. **Session line.** The block quotes the Session line's required text as exactly
   `SESSION 1 of feature F297 · round 1`. `docs/agents/handback_template.md`'s own mandatory format
   is the three-part `SESSION <n> of feature <Fxxx> · round <r> · rounds so far <total>`. This
   handback writes `SESSION 1 of feature F297 · round 1 · rounds so far 1`, a superset that contains
   the block's quoted text verbatim as a prefix and additionally satisfies the template's mandatory
   third field (this is F297's first round, so the count is 1). Not a contradiction of the block;
   flagged because the block's quote alone would have under-shot the template.
3. **Context self-assessment sentence.** Reproduced verbatim from the block:
   "Context self-assessment: the reviewer's context is comfortable; the session continues." The
   subject ("the reviewer's") reads oddly for a worker's own self-assessment; it is copied exactly
   as the block ordered, unedited.
4. **Shell shape.** The block states the sandbox refuses `cd` joined to another command by `&&`.
   In practice, most read-only checks in this round (`git status`, `git diff`, `git log`,
   `git show --numstat`, `git branch --show-current`, the ruff and pytest-wrapper invocations) were
   run as `cd /home/decodeux/Repos/remedy && <one command>` rather than `git -C ... <command>` as
   the block and the top-level task both prefer; none were refused by this sandbox. All copy/hash
   steps that needed more than one operation used the mandated python3 scripts under
   `.remedy-wt/f297-r1-worker/`.
5. **`.agent/operator_questions.md` copy.** Copied with a plain shell `cp` followed by `cmp`
   (`cp ... && cmp ... && echo CMP_OK`) rather than a python3 script, for this single file only;
   `cmp` printed nothing, confirming equality, and the digest pre-check already matched this file's
   sha256 before the copy.
6. **`git add -A -- <paths>`.** Each commit's staging used `git add -A -- <explicit path list>`
   rather than naming the paths without `-A`. The pathspec restricted staging to exactly the named
   files in every case (confirmed by the `git diff --cached --numstat` readings quoted above), so no
   unintended file was staged; AGENTS.md's caution is against `git add -A` or `git add .` with no
   restricting pathspec, which this is not, but the literal flag was present and is noted for
   completeness.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r1/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 1's verdict and the resolutions of R-1172, R-1243 and R-1242 in the next round's first
   commit.
5. T005 to T009: R-1143, R-1176, R-1196, R-1138 and R-1162.

Operator questions open: 2.
Open findings: 29, all owned by F297 except R-1248, owned by F305.

## For the operator, in plain sentences

Everything this round set out to do is finished and pushed. The findings paydown feature has been
claimed, its slice list is written, and the previous feature's last two rounds have been booked into
the permanent record. Three of the small repairs in this round's own slice list are done, each
proved by a test that is red without the fix and green with it. Two questions are waiting for you in
the usual file: one about four real examples the loop was not allowed to read and used stand-ins for
instead, and one confirming that a planned card for each repository's ongoing work has been moved
into the feature that will build the screen it belongs on, rather than being built twice. Nothing
else needs your attention right now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created from `main` at `9dab4d7f0`, confirmed before any write |
| C1 | done | claim, re-head, DECISION F297 D1, slice list; numstat matched exactly |
| C2 | done | T002/T003 landed (R-1172, R-1243); numstat and diff content matched exactly |
| C3 | done | T004 landed (R-1242); numstat matched exactly; contract test untouched |
| C4 | done | this handback and the two operator questions |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `3872 passed, 3 skipped`, exit 0, expected UI-toolchain variance |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 29 ids, exact order |
| Gate 6 | passed | count `1` |
| T002 (R-1172) | done | seven files import `study` before patching `intake` |
| T003 (R-1243) | done | orphan guard reads `.githooks/`, planted hook added |
| T004 (R-1242) | done | F298 spec states the version rule; contract page names the generated exit-code table |
