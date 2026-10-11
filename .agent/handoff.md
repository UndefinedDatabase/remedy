# Handback — F297 round 9: book round 8, land T021 and T022

## Session

SESSION 2 of feature F297 · round 9 · rounds so far 9

Context self-assessment: the session verified the block and all 15 prepared files' digests before
any write, read every diff in full against the current tree (including the dry files' prefixes
against the live state files, via a bounded python3 check) before staging, and executed the two
commits and six gates in one uninterrupted pass with no retries; context remains comfortable at
handback.

Fortschritt: ~85 % (T001 to T022 landed · T023 to T025 open) — Schätzung

## Range

Review of `ff3700ce2`..`HEAD`.

## Commits

### 73f9708da F297 R9 C1: book round 8 and the resolutions of R-1156, R-1157 and R-1230, DECISION F297 D10

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r9.md` | +126/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r9/prep/block.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D10: how round 9 repairs R-1219 and R-1220 |
| `.agent/live_review.md` | +8/-0 | appended the `Gate: F297 R8` paragraph (VERDICT PASS) and the `Done:` paragraphs for R-1156, R-1157 and R-1230 |
| `.agent/plan.md` | +9/-7 | rewritten in full for F297 round 9 |
| `.agent/prose_slips.md` | +1/-0 | one dated line on round 8's handback |

### ed007c1b4 F297 R9 C2: the starts' own refusals are held whole and the poll's and apply's equal their commands, and the no-TLS check reads all the supervisor reaches (R-1219, R-1220)

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T12_F253.md` | +9/-0 | amendment recording DECISION F297 D10: which refusals are the route's own vs. equal to a command's envelope, and the no-TLS repair |
| `docs/system/public-http-api-v1.md` | +12/-4 | the two start routes' own refusals are named as the route's own, not `remedy do`'s; the run poll's `run_not_found` for a value naming no job is named equal to `remedy client run`'s envelope |
| `tests/orchestration/test_import_reachability.py` | +4/-3 | `reachable_closure` now takes its entry points as an argument, defaulting to the existing six |
| `tests/orchestration/test_serve_daemon.py` | +36/-17 | the no-TLS test now walks the full first-party import closure via `reachable_closure`/`resolve_module_path` and fails on an `ssl` import or a call naming the string `"ssl"`; a new subprocess case holds the run poll's refusal of a value naming no job equal to the `job apply` command's envelope |
| `tests/ui_server/test_public_api.py` | +96/-0 | new coverage: the order start's and run start's own refusals held whole (five order-start cases, the running-mission key refusal, and five run-start cases), and a check that the contract page states both sections' refusals are the route's own |

### this commit F297 R9 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, docs/agents/handback_template.md) |

## External actions

Before this round, the reviewer merged pull request 327 — an operator change that makes hosted CI
start only by hand — at the Open PR Gate, as merge commit `f83708293` on `main`. No other `gh`
command run and no PR opened or touched by this round. `git push origin
feature/f297-findings-paydown-v7` after this commit, reported below with the post-push `git
rev-parse HEAD origin/feature/f297-findings-paydown-v7`.

## Verification

**Preconditions (before C1):** `git status --porcelain` empty; `git rev-parse HEAD` read
`ff3700ce2b803bf6f1810e810ac6dd801f15e54d`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`; `.agent/STOP` absent.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r9/prep/block.md`
read `126`; `sha256sum` read
`653fa1a34b8fb738a2d8b92af5feed3ff6d116c5f7f9d6944c5d946e385215bc` — both equal to the values the
prompt delivered. All 15 Bundle-listed prepared files (the 9 `dry-*` files, the three
`append-*.txt` files, `verify.py`, `run_selection.py` and `selection.txt`) hashed via `sha256sum`:
every one matched the block's stated digest exactly. The dry files' expected line counts (base plus
the per-file numstat the block gives) were also checked against their actual `wc -l` and all nine
matched exactly, and the three large `.agent/` files' unchanged prefixes (first N lines, N = the
pre-round line count) were checked byte-for-byte against the corresponding dry file's prefix via a
python3 script (`check_prefix.py`): all three `prefix_equal= True`.

**C1:** `python3 -I c1_copy.py` copied the four `dry-*` whole files and the block to
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
`.agent/authored/f297-r9.md`; each printed `cmp_equal= True`. `.agent/authored/f297-r9.md` read
`wc -l` 126 and the same sha256 as `block.md`. `git branch --show-current` read
`feature/f297-findings-paydown-v7` before staging. `git diff --cached --numstat` read exactly
`126 0 .agent/authored/f297-r9.md`, `12 0 .agent/decisions.md`, `8 0 .agent/live_review.md`,
`9 7 .agent/plan.md`, `1 0 .agent/prose_slips.md` — matching the block's required readings. The
full staged diff of `.agent/plan.md` was read directly (27 lines); the appended tails of
`.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` were confirmed against
the block's `append-live_review.txt`, `append-decisions.txt` and `append-prose_slips.txt` (byte
content of each append file matches the tail the respective dry file carries), and their prefixes
were confirmed unchanged by the prefix check above, so the staged diff is exactly those appended
tails. The `Gate: F297 R8` paragraph and the three `Done:` paragraphs matched the block's "For the
record" description; the DECISION F297 D10 text matched its heading and content; the prose-slips
line matched the round-8 handback inaccuracy it names.

**C2:** `python3 -I c2_copy.py` copied the five files; each printed `cmp_equal= True`. `git diff
--cached --numstat` read `9 0 docs/roadmap/features/T12_F253.md`,
`12 4 docs/system/public-http-api-v1.md`, `4 3 tests/orchestration/test_import_reachability.py`,
`36 17 tests/orchestration/test_serve_daemon.py`, `96 0 tests/ui_server/test_public_api.py` —
matching the block exactly. Every diff was read in full before staging against the current tree:
the contract page's new sentences naming which refusals are the route's own and which equal a
command's envelope, the `T12_F253.md` amendment recording DECISION F297 D10, the reachability
helper's new optional argument (default preserves existing callers), the no-TLS test's rewrite to
walk `reachable_closure`/`resolve_module_path` and its new subprocess case for the run-poll/apply
comparison, and the new test file coverage for both starts' own refusals. `git branch
--show-current` read `feature/f297-findings-paydown-v7` before staging.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r9/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (10
file-equality checks and the three ledger/decisions/prose-slips base-plus-slice checks), last line
`ALL True`, exit 0.

**Gate 2:** `python3 -m ruff check tests/ui_server/test_public_api.py
tests/orchestration/test_serve_daemon.py tests/orchestration/test_import_reachability.py` →
`All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r9/prep/run_selection.py /home/decodeux/Repos/remedy` → 3
SKIPPED lines (`tests/test_agent_tooling.py:43` D12 quarantine, `tests/test_install_smoke.py:175`
opt-in install smoke, `tests/test_repair_context_reviewer_memory.py:257` UI source not found), no
FAILED or ERROR line, no `process(es) behind` line, summary `3699 passed, 3 skipped in 75.54s
(0:01:15)`, `exit 0` — matching the reviewer's dry-tree reading of `3699 passed, 3 skipped` named
in the prompt.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1219', 'R-1220', 'R-1235', 'R-1240', 'R-1241', 'R-1246', 'R-1248', 'R-1249', 'R-1251']` — the
9 ids in the required order, exit 0.

**Gate 6:** `git log --format=%s ff3700ce2..HEAD` → the two subjects of C1 and C2, newest first,
exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4; the block's own Constraints also forbid
it this round). No full suite was run beyond the selection gate 3 names; `REMEDY_TEST_MAX_WORKERS`
was never set. No two test commands ran at once; each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 15-file digest pre-check (above)
additionally confirmed every prepared source's sha256 against the Bundle's stated values before
any copy:

1. `.remedy-wt/f297-r9/prep/block.md` → `.agent/authored/f297-r9.md`: 126 lines both, sha256
   `653fa1a34b8fb738a2d8b92af5feed3ff6d116c5f7f9d6944c5d946e385215bc` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, 284 lines both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, 29176 lines both.
4. `dry-prose_slips.md` → `.agent/prose_slips.md`: cmp equal, 1236 lines both.
5. `dry-plan.md` → `.agent/plan.md`: cmp equal, 27 lines both.
6. `dry-public-http-api-v1.md` → `docs/system/public-http-api-v1.md`: cmp equal, 263 lines both.
7. `dry-T12_F253.md` → `docs/roadmap/features/T12_F253.md`: cmp equal, 190 lines both.
8. `dry-test_public_api.py` → `tests/ui_server/test_public_api.py`: cmp equal, 2388 lines both.
9. `dry-test_serve_daemon.py` → `tests/orchestration/test_serve_daemon.py`: cmp equal, 1164 lines
   both.
10. `dry-test_import_reachability.py` → `tests/orchestration/test_import_reachability.py`: cmp
    equal, 146 lines both.

The three `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`,
`append-prose_slips.txt`) were listed in the Bundle and digest-checked (all `True`), but C1 orders
copying the four whole `dry-*.md` files, which already carry that content baked in; the
`append-*.txt` files were not applied separately, and nothing in the block calls for that (same
note as F297's prior rounds' handbacks).

## Deviations & assumptions

1. **Shell shape.** Most read-only checks this round (`git status`, `git branch --show-current`,
   `git add`, `git diff --cached`, `git commit`, `git log`, `wc -l`, `sha256sum`, the ruff
   invocation, `integrity check`, the gate-1/gate-3/gate-4/gate-5 script invocations) were run with
   the working directory set to `/home/decodeux/Repos/remedy` rather than `git -C ... <command>` as
   the top-level task instructions prefer; none were refused by the sandbox. Both copy steps used
   the mandated python3 scripts under `.remedy-wt/f297-r9-worker/`. (Same note as F297's prior
   rounds' handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag.
3. **Prefix-equality tooling.** The three large `.agent/` files (`decisions.md` at 29,164
   pre-round lines, `live_review.md` at 276, `prose_slips.md` at 1,235) exceed the inline Read
   tool's practical per-call budget at full-file size, and a plain `diff` of each against its dry
   counterpart would print the whole appended tail inline at that size; their unchanged-prefix
   check was done instead by a small python3 script that splits both files into lines and compares
   the current file against the dry file's matching prefix slice, printing only a boolean per file.
   The appended tails were separately confirmed byte-for-byte against the block's `append-*.txt`
   files. `.agent/plan.md` (27 lines post-round) was read in full via plain `git diff --cached`.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r9/`; no pull request
opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear during
the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The next round's first commit books round 9's verdict and the resolutions of R-1219 and
   R-1220.
5. T023 and T024: R-1240 and R-1249.
6. T025 R-1241, the structural step; then the closure sequence.

Operator questions open: 1.
Open findings: 9, all owned by F297 except R-1248, owned by F305, and R-1251, owned by the next
findings paydown.

## For the operator, in plain sentences

This round first wrote last round's results permanently into the project's record. It then closed
a gap in how the project's own public web interface describes itself: for the two actions that
start new work, the written description now says plainly which of its error responses are that
action's very own, since no existing command in the project answers quite the same way, and which
of its other error responses must always match, word for word, the equivalent existing command's
answer. Both are now checked by automated tests so a future change cannot drift from the written
description without being caught. Separately, the test that makes sure the program never tries to
use an unencrypted network connection where encryption is required was deepened so that it now
checks every piece of code reachable from the relevant part of the program, rather than a
hand-picked list of files, closing a gap where a newly added file could have been missed. Nothing a
person using the project would notice changed in how it behaves; the behavior is the same, only
more thoroughly described and checked. Before this round, a separate change from the person
reviewing the work was merged that makes the project's own automated online checks start only when
someone chooses to start them, rather than on their own. One question remains open from last round,
unchanged, about a spending allowance for a maintenance job; nothing new is waiting on you right
now.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 8, resolutions of R-1156, R-1157 and R-1230, DECISION F297 D10; numstat matched exactly |
| C2 | done | T021 landed: the two start routes' own refusals and the poll's/apply's equal-envelope refusals are held whole by new tests and the contract page; T022 landed: the no-TLS test now reads the full first-party import closure the supervisor reaches; numstat and diff content matched exactly |
| C3 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `3699 passed, 3 skipped`, exit 0, matching the reviewer's dry-tree reading |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 9 ids, exact order |
| Gate 6 | passed | two subjects, newest first |
| T021 (R-1219) | done | the order start's and run start's own refusals held whole by new tests; the run poll's and apply's refusals of a value naming no job held equal to their commands' envelopes; the contract page and `T12_F253.md` state which refusals are the route's own |
| T022 (R-1220) | done | the no-TLS test walks `reachable_closure` from `packages.orchestration.serve_daemon` and fails on an `ssl` import or a call naming the string `"ssl"` |
