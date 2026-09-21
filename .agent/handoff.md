# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 18 · CLOSURE

## Session

SESSION 7 of feature F277 · round 18 · rounds so far 18

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

**SCOPE REPORT (required by amend0827 rule 6 at the 7-session soft limit).** Unchanged in
substance since round 12, and this round discharges it. *Finished:* T001, the event
vocabulary, and T002, the JSON envelope with its dispatch error boundary. *Missing:* T003 is
partly applied — `fail()` exists and nine of the twenty-eight CLI modules call it. T004 is not
started. *The proposal, now executed:* DECISION F277 D10 closes F277 on T001 and T002 complete
and T003 in part; the remainder is registered as F283, directly behind F277 in the STATUS
ledger. The operator question it owes is `.agent/operator_questions.md` Q2.
**THIS ROUND IS THE CLOSURE.** Round 17's PASS is booked, R-1014 is resolved through the single
checklist consolidation pass, the ledger is rotated, and STATUS F277 is flipped to `[x]` with
the README capability sync and the SU-025 `consumed_by` edit in ONE commit, last on the branch
under Rule A4.

Context self-assessment: before any edit I read `AGENTS.md`,
`docs/agents/handback_template.md`, `.remedy-wt/f277-r18-block.md` and
`docs/roadmap/STATUS_closure_protocol.md` (Preconditions and Algorithm in full, including
Algorithm steps 4 and 5, the amend0905-throughput rotation paragraph and the amend0911-feedback
ownership paragraph), then all six payloads, then round 17's `.agent/handoff.md` in full. I
also read `scripts/rotate_live_review.py` in full before running it, so the record model and
the open-set definition this handback reports are the script's own and not a re-implementation.

## Range

Review of `365051fa`..`HEAD`.

## Commits

### 235b73fc F277 R18 C1a: copy round 18 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r18-block.md | +243/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r18-checklist.diff | +24/-0 | byte-for-byte copy of the checklist.diff payload |
| .agent/authored/f277-r18-ledger.md | +4/-0 | byte-for-byte copy of the ledger.md payload |
| .agent/authored/f277-r18-plan.md | +46/-0 | byte-for-byte copy of the plan.md payload |
| .agent/authored/f277-r18-queue.diff | +12/-0 | byte-for-byte copy of the queue.diff payload |
| .agent/authored/f277-r18-readme.diff | +35/-0 | byte-for-byte copy of the readme.diff payload |
| .agent/authored/f277-r18-status.diff | +12/-0 | byte-for-byte copy of the status.diff payload |

Measured insertions (`git show --numstat`): **376**. Expected: 133 payload lines plus the
measured block line count of 243, which is 376. They **MATCH**. I ran the ordered cap
arithmetic BEFORE committing: `500 − 133 − 243 =` **124**, non-negative, so the commit was legal
and needed no oversize declaration. This feature's one permitted declaration stays spent where
round 12 spent it.

### 0bd08e24 F277 R18 C1b: book round 17's PASS and resolve R-1014
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append the ledger.md payload: the round 17 `Gate:` entry and the `Done: R-1014` resolution |
| .agent/plan.md | +26/-24 | rewrite to the plan.md payload, byte-identical, 46 lines |

Measured insertions (`git show --numstat`): **30**. The block expected **30** — 4 plus the plan
rewrite's own diff insertions of **26**. Both the total and the per-file breakdown match.

### 475cbdc2 F277 R18 C2: merge R-1014's rule into checklist item 12
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +14/-0 | `git apply` of checklist.diff: R-1014's rule merged as a closing clause of item 12, no new item |

Measured insertions: **14**. The block expected **14**. They MATCH.

### 7ac8140a F277 R18 C3: rotate the live review ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-51 | 15 `Gate:` records of `[x]` features and 5 resolved finding pairs moved out |
| .agent/live_review_archive.md | +52/-0 | the same records appended byte-verbatim, sha256-verified by the script before any write |

Measured insertions: **52**. The script's path set is exactly the two files amend0905-throughput
names; it touched no third path.

### C4 — THE CLOSURE COMMIT (this commit)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | `git apply` of status.diff: F277 `[~]` → `[x]` with the full closure segment set |
| README.md | +10/-3 | `git apply` of readme.diff: 87→88 accepted, Tier 2 Done 29→30, and the F277 capability paragraph |
| scripts/self_use_queue.json | +1/-1 | `git apply` of queue.diff: SU-025 `consumed_by` "" → "F277" |
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the cap under DECISION F104 D1 |

Measured insertions across the three applied diffs: **12** — 1 for STATUS, 10 for README and 1
for the queue, which is exactly what the block expected. Self-reference exception (handback
template, R-0149 pattern): a handback cannot table the commit that writes it, so this table is
written from the staged diff. **C4 is the LAST commit on this branch under Rule A4**; no
trailing commit follows it, which is why the push and the pull request below are recorded as
PENDING here and reported with their real outcomes in the worker's session reply.

## External actions

- `git push -u origin feature/f277-machine-contracts` after C4 — **PENDING at the time this
  file is written**, because the push ships this very file. Its real transcript and exit code
  are in the worker's session reply. See deviation 2.
- `gh pr create` after that push — **PENDING at the time this file is written**. The pull
  request NUMBER and URL cannot appear here: they do not exist when C4 is written, and no
  trailing commit may add them, because DECISION amend0827 D2 permits exactly ONE successor to
  the closure commit and only when its path set is exactly `.agent/candidates.md`, which this
  is not. Both are reported in the session reply.
- **NOTHING IS MERGED.** No `gh pr merge` was run, `main` was never checked out, and no branch
  was deleted. Guardrail G1 and Algorithm step 6 defer the merge to the next feature's Open PR
  Gate, which is the operator's manual-review window.
- No worktree was added or removed. The three `remedy/job-*` worktrees and both review packages
  were left alone.

## Verification

### Pre-flight

- `ls .agent/STOP`: `No such file or directory`. There is no STOP on disk.
- `git status --porcelain`: empty (0 lines).
- `git branch --show-current`: `feature/f277-machine-contracts`.
- `git log --oneline -1`: `365051fa`, the commit the block names.
- Block self-verification (R-0954), `.remedy-wt/f277-r18-block.md`:

| reading | measured | given in the delegation message | equal |
|---|---|---|---|
| line count | 243 | 243 | True |
| sha256 | `9ae5de76f986bf227a9dd756e7e3b2b80799548ebff1afdd5070b7e074246ca1` | `9ae5de76f986bf227a9dd756e7e3b2b80799548ebff1afdd5070b7e074246ca1` | True |

Neither reading differs, so the round went ahead. The block file is 16144 bytes.

### G1(a) — PAYLOADS transport, eighteen readings

| file | lines measured / given | bytes measured / given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| checklist.diff | 24 / 24 | 1865 / 1865 | `47f97064d756f9ca79ca694d12e2cd4a31ef59960574d618f1e23b8c0502c329` | True |
| ledger.md | 4 / 4 | 5572 / 5572 | `9d0cecea7069a4c7390201d755a536d52b58fd561a074b6a1920ed3d2d201283` | True |
| plan.md | 46 / 46 | 2314 / 2314 | `7420146c3f96c4078923f574f0987796b739a345287a0824a885112d864cb41f` | True |
| queue.diff | 12 / 12 | 9431 / 9431 | `602ea535db08600bfe831123717d72f5824dcf9d50474e2380629885648c37d9` | True |
| readme.diff | 35 / 35 | 1627 / 1627 | `bf1d4d52edf45eadd8062dada116300188474e98d0392226579808e93a0af47d` | True |
| status.diff | 12 / 12 | 2398 / 2398 | `4c6be11764e32cb5ca01c4f9a61e8755dc204c94ff3a2c930f6fca0b9c8e5bc0` | True |

**All eighteen readings equal: True.** Total payload lines **133**. Each of the four `.diff`
payloads dry-ran with `git apply --check` at real exit code **0** before it was applied:
checklist.diff 0, status.diff 0, readme.diff 0, queue.diff 0. Nothing was written into
`.remedy-wt/f277-r18-payloads/`.

### G1(b) — the seven `.agent/authored/f277-r18-*` copies against their sources

Copied with `shutil.copyfile`, then compared byte-for-byte against the originals:

| copy | source | sha256 | identical |
|---|---|---|---|
| f277-r18-block.md | `.remedy-wt/f277-r18-block.md` | `9ae5de76f986bf22…` | True |
| f277-r18-checklist.diff | `.remedy-wt/f277-r18-payloads/checklist.diff` | `47f97064d756f9ca…` | True |
| f277-r18-ledger.md | `.remedy-wt/f277-r18-payloads/ledger.md` | `9d0cecea7069a4c7…` | True |
| f277-r18-plan.md | `.remedy-wt/f277-r18-payloads/plan.md` | `7420146c3f96c407…` | True |
| f277-r18-queue.diff | `.remedy-wt/f277-r18-payloads/queue.diff` | `602ea535db08600b…` | True |
| f277-r18-readme.diff | `.remedy-wt/f277-r18-payloads/readme.diff` | `bf1d4d52edf45ead…` | True |
| f277-r18-status.diff | `.remedy-wt/f277-r18-payloads/status.diff` | `4c6be11764e32cb5…` | True |

**Copies compared: 7. All True.** The chain makes no claim about the bytes emitted into the
worker's prompt, which this workflow cannot measure.

### G1(c) — the append at C1b

Byte arithmetic by strict CONCATENATION, not by length:

| file | pre measured | pre, reviewer's | payload | post measured | post, reviewer's | pre+payload == post |
|---|---|---|---|---|---|---|
| .agent/live_review.md | 487135 | 487135 | 5572 | 492707 | 492707 | True |

All three of my numbers equal the reviewer's three.

**Reading (b), the independent structural reader (§3 item 36).** My script COUNTED the
blank-line-separated paragraphs in `ledger.md` rather than taking the number from the block:
**N = 2**. It then compared the LAST 2 such units of the whole file against those 2 payload
paragraphs IN ORDER: **True**. Unit 1 is the round 17 `Gate:` record, unit 2 the
`Done: R-1014` resolution, in the payload's own order.

**Negative control.** I flipped one bit at byte offset 487146, INSIDE the FIRST appended
paragraph, on an in-memory copy; the committed file was never mutated. **BOTH readings return
False:**

```
READING 1 strict concatenation pre+payload == mutated: False
READING 2 structural last-N comparison:                False
```

So neither reader is a length comparison and neither can be satisfied by a payload that differs
by a single bit.

### G1(d) — the plan rewrite at C1b

| reading | value |
|---|---|
| payload sha256 | `7420146c3f96c4078923f574f0987796b739a345287a0824a885112d864cb41f` |
| committed `.agent/plan.md` sha256 | `7420146c3f96c4078923f574f0987796b739a345287a0824a885112d864cb41f` |
| byte equal | True |
| line count | 46 (under the AGENTS.md 50-line rule: True) |

### G1(e) — open set by distinct id in `.agent/live_review.md`

Computed with the repository's OWN canonical reader — `open_finding_ids` from
`scripts/rotate_live_review.py`, the same function `remedy integrity check` reads the ledger
through — rather than a hand-rolled regex:

| rev | OPEN by distinct id | reviewer's |
|---|---|---|
| 365051fa | **23** | 23 |
| C1b `0bd08e24` | **22** | 22 |
| C3 `7ac8140a` | **22** | 22 |

The fall from 23 to 22 is `R-1014` resolving, and the rotation changes NO count — it moves
records only, which is the property amend0905-throughput requires of it. All three numbers
equal the reviewer's three.

### G2 — THE CONSOLIDATION DID NOT GROW THE LIST

The pre-emission checklist's items counted mechanically as the lines matching `^  \d{1,2}\. \*\*`,
taking the first 34 (a later numbered list in the same file reuses small numbers; the raw match
count over the whole file is 38 at both ends):

| | count | numbers |
|---|---|---|
| BEFORE the edit | **34** | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37 |
| AFTER the edit | **34** | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37 |

Both are 34 and both run 1 to 16, 18, 20 to 31 and 33 to 37 — the SAME SET at both ends, which
is the "same length or shorter" amend0827 rule 4 requires and the figure its own paragraph names.
The clause landed as the closing sentences of item 12, directly before item 13, so R-1014's fix
clause is MERGED and no item was appended. No number is retired, because nothing was merged away.

`git diff --name-only 0bd08e24 475cbdc2` names exactly one path, and its length is **1**:

```
docs/agents/planner_reviewer_prompt.md
```

### G3 — THE ROTATION PRESERVED THE RECORD

`python3 scripts/rotate_live_review.py`, real exit code **0**. Full output:

```
gate records moved: 15
finding pairs moved: 5 (10 records)
old ledger size: 492707 bytes
new ledger size: 421313 bytes
old archive size: 4361155 bytes
new archive size: 4432550 bytes
open findings before: 22
open findings after: 22
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```

I ran `--dry-run` first and it printed the identical eight numbers, writing nothing.

| reading | before | after | reviewer's before/after |
|---|---|---|---|
| ledger bytes | 492707 | **421313** | 492707 / 421313 |
| archive bytes | 4361155 | **4432550** | 4361155 / 4432550 |
| open findings | 22 | **22** | 22 / 22 |

Every one of the six numbers equals the reviewer's. `git diff --name-only 475cbdc2 7ac8140a`
names exactly the two paths amend0905-throughput allows, and its length is **2**:

```
.agent/live_review.md
.agent/live_review_archive.md
```

**THE R-1014 PAIR MOVED WHOLE**, counted by line-anchored search rather than asserted:

| location | `^- R-1014 — ` registrations | `^Done: R-1014 — ` lines |
|---|---|---|
| `.agent/live_review_archive.md` | **1** | **1** |
| `.agent/live_review.md` | **0** | **0** |

The archive holds both halves and the live ledger holds neither, which is what "a pair moves
whole" means. Three prose MENTIONS of the string `R-1014` remain in the live ledger; all three
sit inside OTHER records that did not move (earlier `Gate:` entries that narrate the finding),
and none of them is a registration or a `Done:` record. The rotation ran AFTER C1b on purpose:
before it, the registration would have stayed behind while its resolution moved ahead.

### G4 — THE CLOSURE COMMIT IS EXACTLY WHAT THE PROTOCOL FIXES

`git diff --name-only 7ac8140a <C4>` names exactly four paths, and its length is **4**:

```
.agent/handoff.md
README.md
docs/roadmap/STATUS.md
scripts/self_use_queue.json
```

That is precisely the path set Algorithm step 5 fixes. R-0154 is satisfied: the README sync is
in the SAME commit as the STATUS `[x]` edit, so README and STATUS never disagree in any
committed state.

**F277's STATUS line, read back in full:**

```
- [x] F277 — Machine contracts: event vocabulary, JSON envelope, exit codes (T001-T002 complete and T003 in part: the shared `fail()` helper and nine of twenty-eight CLI modules migrated onto it; the rest of T003 and all of T004 moved to F283; accepted 2026-09-21 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f2771701c0de5a17 · package remedy-review-20260921-032054-READY_FOR_REVIEW.zip · SHA-256 cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD deeac639488b1cb1be930a550b2295509652051f)
```

**The other three read-backs:**

| reading | value |
|---|---|
| README accepted line | `88 of 283 registered items accepted. Next: the first unchecked item in docs/roadmap/STATUS.md.` |
| README Tier 2 row | `| 2 | Minimal Self-Build Runtime | 30 | 36 |` |
| `SU-025` `consumed_by` | `F277` |

SU-025 is the queue's ONLY pending item and its title is `Address ledger finding R-0820`, so
precondition 6's "exactly one self-use item is consumed by this close" holds by count as well
as by edit.

**The package segments re-read off the package FILE itself, not off the block:**

| reading | measured off the file | the block's |
|---|---|---|
| package filename | `remedy-review-20260921-032054-READY_FOR_REVIEW.zip` | identical |
| SHA-256, recomputed over the 28355558 bytes on disk | `cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723` | identical |
| `.review_zip_manifest.json` `committed_review_subject.head_commit` | `deeac639488b1cb1be930a550b2295509652051f` | identical |
| `package_status` | `READY_FOR_REVIEW` | — |
| `blocking_reasons` | absent/None | — |

The STATUS line's `accepted HEAD` equals that manifest head_commit, so the line names the head
the verdict and the zip actually cover.

### G5 — THE CLOSURE GATES

```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ \
    tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py \
    tests/regression/test_resource_safety.py
451 passed in 104.92s (0:01:44)
```

Real exit code **0**. The reviewer's dry run, taken in a DISPOSABLE WORKTREE at `365051fa`,
read `449 passed, 2 skipped`. Mine reads `451 passed` with **0 skipped**: the same 451 tests
selected, with two that skip in a cold worktree passing here in the primary checkout, where
`apps/ui`'s `dist` and `node_modules` are already built. I report the difference rather than
calling it a match; the failure count is 0 in both. The gate CAN fail and its pass means
something — the reviewer reproduced `1 failed, 448 passed, 2 skipped` at exit 1 with the README
accepted count left at 87, and the same with the Tier 2 Done cell left at 29.

`remedy integrity check --json`, closure precondition 3, real exit code **0** — all five checks
`pass`, `passed: true`, `fail_count: 0`, `check_count: 5`:

```json
{"handler_import": "pass (handlers=145)",
 "live_review_verdict": "pass",
 "plan_consistency": "pass (unchecked=0)",
 "relevant_untracked": "pass (untracked=0, relevant=0)",
 "high_blockers_open": "pass (no open blocker/high findings)"}
```

The full suite was NOT re-run: it ran once at round 15 and
`.agent/authored/f277-closure-suite.txt` is what this closure reads back, exactly as
precondition 2 directs.

### G6 — PUSH, PULL REQUEST AND TREE

**PENDING at the time this file is written.** The push carries this file and the pull request
does not exist until after it, so neither outcome is obtainable from inside C4 and no trailing
commit may add them (DECISION amend0827 D2). Both are reported in the worker's session reply
with their real exit codes, and the pull request with its number and URL. **Nothing is merged
in this session.**

### The round's whole tracked path set

`git diff --name-only 365051fa <C4>` — I report the LENGTH I MEASURED rather than checking it
against a number the block states: **15** paths, listed in the order the command printed them.

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f277-r18-block.md | C1a `235b73fc` |
| 2 | .agent/authored/f277-r18-checklist.diff | C1a `235b73fc` |
| 3 | .agent/authored/f277-r18-ledger.md | C1a `235b73fc` |
| 4 | .agent/authored/f277-r18-plan.md | C1a `235b73fc` |
| 5 | .agent/authored/f277-r18-queue.diff | C1a `235b73fc` |
| 6 | .agent/authored/f277-r18-readme.diff | C1a `235b73fc` |
| 7 | .agent/authored/f277-r18-status.diff | C1a `235b73fc` |
| 8 | .agent/handoff.md | C4, this commit |
| 9 | .agent/live_review.md | C1b `0bd08e24`, then C3 `7ac8140a` |
| 10 | .agent/live_review_archive.md | C3 `7ac8140a` |
| 11 | .agent/plan.md | C1b `0bd08e24` |
| 12 | README.md | C4, this commit |
| 13 | docs/agents/planner_reviewer_prompt.md | C2 `475cbdc2` |
| 14 | docs/roadmap/STATUS.md | C4, this commit |
| 15 | scripts/self_use_queue.json | C4, this commit |

Fifteen distinct paths, set-equal to constraint 3's enumeration — the seven authored copies
plus the eight the constraint names one by one. `.agent/candidates.md`, `.agent/decisions.md`,
`.agent/operator_questions.md` and `docs/roadmap/features/T2_F277.md` appear **0** times each.
Nothing under `packages/`, `apps/` or `tests/` was touched.

## Authored-text proofs

- The seven copies at C1a, compared with the reviewer's originals under
  `.remedy-wt/f277-r18-payloads/` and `.remedy-wt/f277-r18-block.md`: **seven readings, all
  True** (G1(b)).
- The REWRITE payload against the committed file: `.agent/plan.md` is sha256-equal to `plan.md`
  at 46 lines (G1(d)).
- The APPEND payload against the committed file: strict byte concatenation True, with all three
  byte numbers equal to the reviewer's, plus the independent structural reader at a COUNTED N
  of 2, plus a one-bit negative control inside the first appended paragraph driving BOTH readers
  to False (G1(c)).
- The four DIFF payloads: each applied with `git apply`, never retyped; each dry-ran with
  `git apply --check` at exit 0 first. The STATUS line and the README paragraph therefore reach
  disk as the reviewer's own bytes — no closure text was transcribed by hand.
- No payload was edited or retyped. All seven copies were made with `shutil.copyfile`, the
  append by reading the payload's bytes and concatenating them.

## Deviations & assumptions

1. **The bundle ran C1a, C1b, C2, C3, C4 — five commits, exactly as ordered. Nothing was added,
   dropped or reordered, and C4 is the last commit on the branch.** Recorded here because the
   template asks the question directly.
2. **No trailing commit for the C4 push or the pull request; both go in the session reply.**
   Rule A4 makes C4 last and DECISION amend0827 D2 permits only a `.agent/candidates.md`
   successor, which this is not. The handoff therefore states both as PENDING, which is what
   the block ordered, and the real outcomes — including the PR number and URL — are reported in
   the worker's reply.
3. **C1b's commit message was corrected by `git commit --amend` before any push.** My first
   write of the subject read `book round 17 PASS` instead of the block's
   `book round 17's PASS`. I amended the message only; the tree was untouched, the commit was
   local and unpushed and had never left this machine, so no published history was rewritten
   and no force-push was involved. The committed subject now matches the block verbatim. The
   pre-amend SHA was `4cbaeaf5`; the committed one is `0bd08e24`.
4. **G5's pytest reading differs from the reviewer's dry run in its SKIP count, not its result:**
   `451 passed, 0 skipped` here against `449 passed, 2 skipped` there. Same 451 selected, zero
   failures in both. The cause is the environment, not the change: the reviewer measured in a
   disposable worktree with a cold `apps/ui` `dist`, and this is the primary checkout where it
   is built. Reported rather than smoothed over.
5. **amend0911-feedback (i), the owner re-assignment, had nothing to re-assign — MEASURED, not
   assumed, and flagged for the reviewer.** The paragraph orders every open finding this feature
   owned and did not resolve to be re-assigned to the next findings-paydown feature in the same
   commit as the verdict bookings. I read all 22 open registrations with the canonical
   `split_records` reader: **0** of them carry an `Owner: F277` line. Thirteen carry
   `Owner: F282 — Findings paydown v2` and nine carry no `Owner:` line in the registration
   record at all. Round 17's handoff listed this step as owed, and the round 18 block did not
   order it, so I performed no ledger edit of my own — authoring ledger text is the reviewer's
   role and the ledger payload was fixed. **The nine registrations without an `Owner:` line are
   the reviewer's to judge**: if that absence is the thing amend0911 (i) means to repair, it
   needs a round, and F277 is closed. Listed so the decision is made rather than inherited.
6. **I read the built package's manifest out of the zip to obtain `head_commit`.** That is a
   read of the artefact round 17's one permitted build produced, not a rebuild; the block asked
   for both package segments to be re-read off the package file rather than off its own page.
7. **Scratch hygiene.** Every log and exit-code capture is under the gitignored
   `.remedy-wt/f277-r18-scratch/`. I wrote nothing into `.remedy-wt/f277-r18-payloads/`.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy block + 6 payloads | done | 376 insertions, matching 133 + 243; cap headroom 124, computed before committing |
| C1b book round 17's PASS and resolve R-1014 | done | 30 insertions by `git show --numstat`, matching the block's 30 (4 + 26) |
| C2 merge R-1014's rule into checklist item 12 | done | 14 insertions, matching the block's 14; exactly one path; list 34 before and 34 after |
| C3 rotate the ledger into its archive | done | script exit 0; two paths only; 492707→421313 and 4361155→4432550; open 22 before and 22 after |
| C4 close F277 — STATUS x, README sync, SU-025 consumed | done | exactly four paths; 12 insertions (1+10+1); last commit on the branch |
| G1(a) payload transport, eighteen readings | done | 18/18 equal to the table; all four diffs dry-ran at exit 0 |
| G1(b) seven authored copies | done | 7/7 byte-identical to their sources |
| G1(c) the append, concatenation + structural reader + control | done | both True; 487135 + 5572 = 492707, equal to the reviewer's three numbers; N counted as 2; one-bit control returns False on BOTH readers |
| G1(d) plan rewrite | done | sha256-equal, 46 lines, under the 50-line rule |
| G1(e) open set at three revisions | done | 23 at `365051fa`, 22 at C1b, 22 at C3, by the canonical `open_finding_ids` reader; equal to the reviewer's three |
| G2 the list did not grow | done | 34 before, 34 after, same number set; one path |
| G3 the rotation preserved the record | done | six byte/count readings all equal the reviewer's; two paths; R-1014's pair in the archive and neither half in the ledger |
| G4 the closure commit's path set | done | four paths exactly; STATUS line, both README readings and `SU-025` read back; package name, SHA-256 and manifest head_commit re-read off the package file |
| G5 the closure gates | done | pytest `451 passed` at exit 0 (see deviation 4); `integrity check` all five `pass` at exit 0 |
| G6 push, pull request and tree | **pending at write time** | C4 is last on the branch; both outcomes reported in the session reply, neither can be written into the commit that precedes them |
| Constraint 1 no payload edited or retyped | done | `shutil.copyfile`, byte concatenation and `git apply` only; every diff dry-ran first |
| Constraint 2 every commit under 500 insertions | done | 376, 30, 14, 52 and 12; this handoff is a single `.agent/**` state file and exempt |
| Constraint 3 no unnamed file touched | done | 15 paths, set-equal to the enumeration; candidates, decisions, operator_questions and the F277 feature file 0 times each |
| Constraint 4 stop on red | done | no gate went red, so nothing was stopped; the closure landed whole |
| Constraint 5 nothing is merged | done | no `gh pr merge`, no checkout of `main`, no branch deletion |
| Constraint 6 leave the worktrees and both packages alone | done | no worktree added or removed; both review zips untouched where they stand |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 18 — C1a, C1b, C2, C3 and C4, with all six gates.
3. **The Open PR Gate, which merges THIS pull request before any new branch is cut.** It was
   deliberately not merged in this session (guardrail G1, Algorithm step 6); the gap is the
   operator's manual-review window, and the package under review is
   `remedy-review-20260921-032054-READY_FOR_REVIEW.zip` at
   `cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723`, archived at
   `/home/decodeux/Repos/remedy-history/zips`.
4. Then Rule A5, which proposes **F283**, standing directly behind F277 in the STATUS ledger:
   the refusal sweep over the nineteen unmigrated CLI modules, the
   read-only-without-`supports_json` set, and the exit-code taxonomy.

**ONE CARRIED ITEM, NAMED EXPLICITLY:** `.agent/candidates.md` still holds **three** entries,
each recording the finding id it was registered as. The disk-vehicle rule makes a non-empty
candidates file a BLOCK CONDITION at feature-claim time, so **F283's FIRST reviewed round
resolves and empties it**. It was deliberately not touched this round; the block forbade it.

Open findings count: **22**. Operator-questions count: **2**.
