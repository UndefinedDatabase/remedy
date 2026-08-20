# Handback — F085 · session of 2026-08-19 (Open PR Gate, BLOCKED)

Branch `feature/f085-sandbox-hardening`, HEAD at the R75 record round. This session planned and
reviewed only: no feature code, no new branch, no merge, no verdict. F085 stays CLOSED and
ACCEPTED — the R74 PASS verdict landed at 4c2d707b and is also the single comment on PR #204
(2026-08-19T19:19:16Z), so it is not stranded.

Fortschritt: F085 ist gebaut und abgenommen; offen ist nur der Merge. Der Open PR Gate wurde in
dieser Sitzung erreicht und hat GESPERRT — der CI-Check auf PR #204 ist rot. Lokal ist dieselbe
Commit-Spitze grün, die Ursache liegt also in der CI-Umgebung und nicht im Testcode. WELCHE Stage
rot ist, konnte diese Sitzung nicht feststellen: `gh run` und `gh api` sind hier gesperrt.

## Phase 0 — probe, run this session

- `git status --porcelain` EMPTY; branch `feature/f085-sandbox-hardening`; `.agent/STOP` absent.
- `gh pr list --state open`: exactly ONE — #204, `feature/f085-sandbox-hardening` → `main`,
  `isDraft: false`. Phase 1 rule 2 fired.
- `remedy plan status` / `remedy plan next` NOT run — the `remedy` entry point is denied
  session-wide here. Disk fallback used: `.agent/handoff.md`, `.agent/plan.md`,
  `.agent/candidates.md`.

## The blocker

`gh pr checks 204` → one check, `ci` (workflow CI), state FAILURE, 43m26s, run 32292354363,
job 96196033505. `gh pr view 204` → `state OPEN`, `mergeable MERGEABLE`,
`mergeStateStatus UNSTABLE`, `isDraft false`, 0 reviews, 1 comment.

AGENTS.md Open PR Gate: failing checks mean stop, report the blocker, do not proceed with new
work. No `gh pr merge` was run and no branch was created.

The run tested the CURRENT head: `4c2d707b` was committed 19:16:44Z, the check started 19:19:55Z
and completed 20:03:21Z.

## Verification — re-run, not read

- FULL SUITE at `4c2d707b`, primary checkout, `python3 -m pytest -n auto -q`: EXIT 0,
  `17132 passed, 19 skipped in 144.77s (0:02:24)`. The red is NOT a local test failure.
- `git diff --numstat e950e8af..4c2d707b`: the four ungated R75 commits touch `.agent/` ONLY —
  `authored/f085-r75.md` 299/0, `candidates.md` 18/0, `handoff.md` 109/0, `last_block.md` 272/356.
  No source, doc or test file in that range.

## Not known — do not guess

Which CI stage went red. The job log was never read: `gh run` and `gh api` are DENIED here.

Hypothesis, NOT a finding: CI runs its stages SERIALLY — `pytest_argv_for_stage` builds
`["-m", expr, "-q", *paths]` with no `-n auto`, and `pyproject.toml` sets no `addopts` — where the
green run above used `-n auto`. Stage budgets sum to 3900s (`fast` 900, `standard` 2100, and `ui`,
`smoke`, `budgets` 300 each) and a budget kill returns exit 124 with note `timed out`
(`packages/orchestration/ci_run.py`). A 43m26s wall is CONSISTENT with a `standard` budget kill on
a 2-core hosted runner. Consistent is not measured — read the log before acting on this.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Phase 0 probe | done | |
| Phase 1 decide | done | rule 2 fired |
| Open PR Gate #204 | blocked | check `ci` FAILURE — AGENTS.md orders stop and report |
| New feature work | skipped | the Gate forbids new work while the PR is blocked |

Open findings: 152, next free id R-0570 — carried from the R74 record, NOT re-measured here.
`.agent/candidates.md` holds TWO entries and stays non-empty.

## Deviations, declared

Handback line count <<LINES>>, over the 60-line cap. Mandated content only — the Phase 0 readings,
the blocker's real command outputs, the verification results, the item-status table and the
next-action list. No section dropped; verbosity is not the cause.

## Next

1. Phase 1 rule 1 FIRST: re-read `.agent/STOP` from disk.
2. Then the Open PR Gate on #204 — it stays blocked while `ci` is FAILURE. Read the log of run
   32292354363: a session where `gh run view --log-failed` is permitted, or the operator supplies
   it. Do NOT merge, do NOT create a branch, do NOT start a feature until that check is green.
3. Only after the merge: the next feature by Rule A5, whose FIRST reviewed round registers or
   resolves BOTH `.agent/candidates.md` entries and empties that file.
