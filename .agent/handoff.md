# Handoff — F253 round 24: book round 23 and the acceptance audit, the hardening stage's first repairs

## Session

SESSION 5 of feature F253 · round 24 · rounds so far 24

Context self-assessment: the reviewer ends session 5 after six rounds and the acceptance audit; the next round designs the order key, which a fresh session reads from the start.

Fortschritt: ~95 % (S1 to S7, audit · two gaps, repeated audit, closure open) — Schätzung

## Range

Review of `c7633415bd7f37b2c8af98deacf17845f5420356`..`0de4689ce3ed9f989a9169bfd3520dfdd122ba44`
(the last commit before this handback, C3).

## Commits

### ca88c97e5 F253 R24 C1: book round 23, resolve R-1208, the acceptance audit, register R-1209 to R-1215, DECISION F253 D21, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r24.md` | 168/0 | new file, byte copy of `block.md` (168 lines, sha256 `3e0b2470c06b24e59ce7627782869f7d5fab15cff54e8e0a135796a17c578957`) |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D21 |
| `.agent/f253_acceptance_audit.md` | 208/0 | new file, byte copy of `dry-f253_acceptance_audit.md` |
| `.agent/live_review.md` | 20/0 | `append-live_review.txt`'s bytes appended: round 23's gate entry, R-1208 resolved, R-1209, the audit entry, R-1210 to R-1215 |
| `.agent/plan.md` | 13/13 | `dry-plan.md`, byte for byte |

### 7ac41bb8c F253 R24 C2: tests for a running run's answer, the 202 answers, a client token on the port, the listener and the page's test section (R-1209, R-1212 to R-1215)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_serve_runs.py` | 37/0 | R-1209: a `RunLauncher` whose stand-in prints one envelope line, flushes and waits for a release file; once the log holds the line, `run_record_payload` reads `running` and `answer` None; after the release and the recorded end it reads `ended` and that envelope |
| `tests/orchestration/test_serve_daemon.py` | 61/0 | R-1213: through a real supervisor with `api_port=0`, a client token from `api/clients.json` (mode 0o600, a project that does not exist, token of 45 characters) reads `GET /api/v1/interface` with 200 and is refused `POST .../decline` with 403 `api_client_policy_refused`, the ledger's line names the client and the status, the job is not declined; R-1214: an `ast` reader of `serve_daemon.py` that fails on any `ssl` import and on any `ThreadingHTTPServer` call whose host is not the constant `"127.0.0.1"`, and asserts it found one |
| `tests/ui_server/test_public_api.py` | 73/0 | R-1212: the 202 body of `POST /api/v1/orders` (an `OrderLauncher` stand-in, waited to its end) equals what `client order <order> --json` prints, and that of `POST /api/v1/jobs/{job}/run` (a `RunLauncher` stand-in) equals what `client run <job> --json` prints, each run as a child process from the checkout with the test's environment; R-1215: the section "A client's test" names the eight things the block lists, and the gate test file's source holds the seven quoted fragments; the import of `serve_paths` |

### 0de4689ce F253 R24 C3: the feature file states the writes' design as built (R-1211, DECISION F253 D21)

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T12_F253.md` | 9/0 | `dry-T12_F253.md`, byte for byte: the section "Amendment — DECISION F253 D21" |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |
| `.agent/operator_questions.md` | this commit | byte copy of `dry-operator_questions.md`: Q14 |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command of mine read, listed or
  wrote the repository's own `.data`. No test started a real provider: every stand-in run and
  order is a test's own.

## Verification

0. Preconditions, before any write: `block.md` read sha256
   `3e0b2470c06b24e59ce7627782869f7d5fab15cff54e8e0a135796a17c578957`; every file listed in
   `digests.txt` matched its entry (Python `hashlib`); `git rev-parse HEAD` and
   `origin/feature/f253-public-http-api` both read `c7633415bd7f37b2c8af98deacf17845f5420356`;
   `git status --porcelain` empty; `.agent/STOP` absent. `git branch --show-current` read
   `feature/f253-public-http-api` before each commit.
1. **Gate 1**: `git status --porcelain` empty after C3; the byte proofs, one script: the authored
   copy equals `block.md`, the audit copy equals `dry-f253_acceptance_audit.md`, `.agent/plan.md`
   equals `dry-plan.md`, the feature file equals `dry-T12_F253.md`, `.agent/live_review.md` and
   `.agent/decisions.md` each equal their blob at the base followed by their slice — all True.
2. **Gate 2**, the block's selection from the primary checkout, once: exit 0, tail
   `728 passed in 101.92s (0:01:41)`, no FAILED, ERROR or SKIPPED line.
3. **Gate 3**: `python3 -m ruff check` on the three test files — exit 0, `All checks passed!`.
4. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`.
5. **Gate 5**: the open-finding reader — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149',
   'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1207',
   'R-1209', 'R-1210', 'R-1211', 'R-1212', 'R-1213', 'R-1214', 'R-1215']`, as ordered.
6. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r24.md`: 168 lines, byte-equal, sha256
  `3e0b2470c06b24e59ce7627782869f7d5fab15cff54e8e0a135796a17c578957`.
- `append-live_review.txt` and `append-decisions.txt` each appended to their base blob at
  `c7633415b`: "post equals pre plus slice" True for both.
- `dry-f253_acceptance_audit.md` to `.agent/f253_acceptance_audit.md`, `dry-plan.md` to
  `.agent/plan.md` and `dry-T12_F253.md` to `docs/roadmap/features/T12_F253.md`: byte-equal.
- `dry-operator_questions.md` to `.agent/operator_questions.md`: copied byte for byte in this
  commit.

## Deviations & assumptions

- Two of my read-only shell calls began with `cd` into the checkout (the block forbids `cd`, even
  for a read); one ran, the other was stopped by the permission check. The working directory resets
  between calls and nothing was written by either; every later call used absolute paths.
- Diff reading: for C1, the block copy, the audit copy and the two appended slices were not read as
  diff hunks (each is proven byte-equal to a file I had read whole or to its source); the plan hunk
  was read. The diffs of C2 and C3 were read whole before their commits.
- Choices left to me in C2: the R-1209 stand-in prints its envelope, flushes and waits for a
  release file, and the test polls the log for `"ok"` before it reads the payload; the R-1212 tests
  start their record through a launcher on `serve_paths` of the scratch data root named by
  `REMEDY_DATA_DIR`, and return that ended record from a recording starter; the R-1213 test writes
  `api/clients.json` itself after the supervisor starts, which the supervisor reads again at every
  call; the R-1214 test reads the host of the first positional argument as a tuple whose first
  element is a constant; the R-1215 test joins the page section's whitespace before it looks for
  `remedy serve start --json` and `remedy serve stop --json`, because the page breaks the first
  inside its code span across two lines (the page is unchanged).
- Single test selections run while writing: the new test of each of the three files, by `-k`
  (1, 2 and 3 passed).
- The `remedy` command installed on this machine was never run; every Remedy call was
  `python3 -m apps.cli.main` from the checkout.

## Round verdicts

Round 23's PASS, with R-1208 resolved and R-1209 registered, and the acceptance audit with its six
gaps, are booked by C1 above. Round 24's verdict is the reviewer's.

## For the operator, in plain sentences

Round twenty-three's work passed review. Then a fresh checker, given only the feature's
description, tested every promise the description makes by breaking the code on purpose and
watching a test fail: 23 of 32 promises held that way, 3 belong to a later feature, and 6 had no
test that would notice them breaking. This round added tests for four of those six and for one more
the review found, wrote down in the feature's description how changes over the web are carried out,
and asks you about that in the new question below; the last open promise, refusing an order a
program sends twice, comes next.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): no pull request for this branch, none to merge.
3. Then book round 24's verdict and resolve what it repaired in the next round's first commit.
4. Then the second repair round: the order key and F304's fifth path over HTTP (R-1210, R-1207).
5. Then the audit repeated for the six statements that had gaps.

Round 25 is the soft limit of 25 rounds (operator amendment amend0827-process-diet rule 6): the next session writes the scope report and applies the split-and-close default of operator amendment amend0905-throughput, closing F253 through the closure sequence with what is repaired and carrying what is not as findings with an owner.

Operator questions open: 3.
Open findings: 20 (R-1209 to R-1215, Low, owned by F253; R-1160, Medium, and R-1138, R-1139,
R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196 and R-1207, Low, owned by
F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 23, resolve R-1208, the acceptance audit, register R-1209 to R-1215, DECISION F253 D21, the plan and the block | done | `ca88c97e5` |
| C2: tests for R-1209, R-1212, R-1213, R-1214, R-1215 | done | `7ac41bb8c` |
| C3: the feature file's amendment (R-1211) | done | `0de4689ce` |
| Gates 1 to 5 | done | all green, gate 2 once |
| C4: this handback and operator question Q14 | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
