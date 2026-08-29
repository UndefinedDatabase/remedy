# STEP R6/F040 — T002 PART 1: THE CLIENT'S DIGEST SEAM

Goal: give the browser a pure module that decodes the digest envelope, builds
the card's cost line from the SAME string the metrics bar reads, and names the
endpoint's path — plus the Python guard that pins its purity. Book the round 5
verdict, resolve R-0754 and rule DECISION F040 D7.

Base: `4e5e9bf8`, the round-5 handback commit and the tip of
`feature/f040-completion-digest`. Stay on that branch. Open no pull request.

WHY THIS SHAPE, measured rather than assumed. This repository CANNOT render a
React component in a test: `apps/ui/vitest.config.ts` sets
`environment: "node"`, there is no jsdom and no testing library, and every one
of the `.test.ts` files under `apps/ui/src/api/` tests pure logic. The feature
file's T002 line asks for "component tests"; here that resolves to pure-logic
vitest over `src/api/` plus a Python guard under `tests/ui_contracts/` reading
the source as TEXT — the shape `test_cost_metric_render.py` and
`test_design_drift.py` already use. DECISION F040 D7 in slice RECORD6 rules it.
This round therefore builds the decidable half FIRST; the `.tsx` card and its
CSS conformance come later, and the trigger/dismiss/last-seen rule is its own
round after this one.

NO TYPESCRIPT COLOUR IS ORDERED THIS ROUND, and the reason is measured, not
assumed. The reviewer probed `npx vitest run --root apps/ui --config ...` at the
base and it was REFUSED before execution with `This command requires approval`,
so no exit code exists for it; the disposable-worktree red-proof route needs
that same command and `apps/ui/node_modules` is gitignored and absent in a
worktree, so a mutation there would be red for every possible module and prove
nothing. What IS available and what this block orders instead: the vitest suite
through the pytest node that spawns it, which a broken module genuinely turns
red, and a Python guard that needs no `node_modules` and IS red-proved normally.
Do not try to route around the refusal — a permission boundary is a finding, not
an obstacle.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r6.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN6
- C2  append slice RECORD6 to `.agent/live_review.md`
- C3  apply pair PAIRACTUAL to `apps/ui/src/api/costMetric.ts` AND add
      `apps/ui/src/api/jobDigest.ts` per the SPEC below
- C4  create `apps/ui/src/api/jobDigest.test.ts` per the SPEC below
- C5  create `tests/ui_contracts/test_job_digest_card_contract.py` per the SPEC
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r6.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    apps/ui/src/api/costMetric.ts
    apps/ui/src/api/jobDigest.ts
    apps/ui/src/api/jobDigest.test.ts
    tests/ui_contracts/test_job_digest_card_contract.py
    .agent/handoff.md

NO PYTHON PRODUCTION CODE CHANGES. `packages/orchestration/job_digest.py`,
`packages/orchestration/ui_server.py` and everything else under `packages/` and
`apps/cli/` are NOT edited. No `.tsx` file is created or edited this round — the
card itself is a later round, and a component with no test harness is exactly
what this round is deliberately not building.

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. If one looks wrong, apply it as
   given and DECLARE the problem in the handback's deviations.
2. C0a is a COPY: the block is at `.remedy-wt/f040-r6-block.md`. Use
   `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append.
4. `.agent/live_review.md` is APPEND-ONLY.
5. `.agent/plan.md` stays under 50 lines.
6. Every exit code is REAL, from `subprocess.run(...).returncode` in a script
   under the gitignored `.remedy-wt/`. Never through a pipe.
7. Mutation and red-proof checks run ONLY in a disposable `git worktree`. The
   ONLY red proof this round is the PYTHON guard's, which needs no
   `node_modules`; see the no-colour paragraph above.
8. C3 IS ONE COMMIT holding the pair and the new module. They are not separable:
   `jobDigest.ts` imports the symbol the pair exports, so landing the import
   before the export is a module that does not resolve.
9. THE ONE STRING THAT MEANS EXACT HAS EXACTLY ONE HOME. `costMetric.ts:58`
   defines `const ACTUAL_BASIS = "actual"` and the pair exports it unchanged.
   `jobDigest.ts` IMPORTS it and NEVER writes the literal `"actual"` — a second
   copy is the drift DECISION F040 D2 already spent a round preventing for the
   urgency formula, and the digest's basis is the same class of shared value.
10. `jobDigest.ts` READS NO CLOCK, OPENS NO SOCKET AND KEEPS NO STORAGE. It
    takes what it needs as arguments, in the manner `recency.ts` documents at
    its head. Nothing in it calls `fetch`, `Date.now`, `new Date`,
    `localStorage`, `sessionStorage` or `crypto`. The trigger rule that WILL
    need a clock is a later round and takes `nowMs` as a parameter when it
    arrives.
11. The `remedy` console script is DENIED to this session; use
    `python3 -m apps.cli.main ...` if needed and say so.
12. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
13. Push after C6. No pull request, no merge, no force-push.
14. Pair shape, measured: PAIRACTUAL `TO contains FROM: false` — it is a
    REPLACEMENT, not an append, so its obligation is FROM occurring exactly 1x
    BEFORE the edit and exactly 0x AFTER, with TO occurring exactly 1x after.

## SANDBOX NOTES — read before writing a script

- Env-var assignment is DENIED in all three shell forms (`VAR=x cmd`,
  `env VAR=x cmd`, `export VAR=x; cmd`). Set it in-process with
  `os.environ[...]` or `monkeypatch.setenv`.
- `cp` is denied; copy with `shutil.copyfile`.
- `$(...)` inside a compound, `;`/`&&` chains and process substitution are
  rejected by FORM. One command per call, or a driver script run as a single
  `bash script.sh`, or `python3 - <<'PY'`.
- The Bash tool does not surface non-zero exits; capture them as
  `subprocess.run(...).returncode`.
- `npx vitest` and `npm run test:unit` are REFUSED to this session class. Reach
  vitest and tsc through the pytest nodes named in G7.

## Slices

The authored units are PLAN6, RECORD6 and the two halves of PAIRACTUAL, each
between its own BEGIN and END marker line. The markers are NOT part of the
unit; the newline ENDING the last content line IS.

<<<BEGIN PLAN6
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 6.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 claim and the seam inventory | done | round 1, PASS |
| the spec decisions D2 to D6 | done | rounds 2, 3 and 5 |
| T001 the composition module and its tests | done | round 3, PASS |
| T001 the endpoint and its route tests | done | round 4, PASS |
| T001 the envelope goldens, R-0754 closed | done | round 5, PASS |
| T002 the client digest seam and its guard | done | this round |
| T002 the trigger, dismiss and last-seen rule | open | next |
| T002 the hero card and its CSS conformance | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round gives the browser a pure `jobDigest.ts` — decode, path, cost line
   — reading the exactness string from `costMetric.ts` rather than restating it,
   plus the Python guard that pins the module's purity.
2. The next round rules where a dismissal persists and builds the show/dismiss/
   last-seen rule as a pure function over an injected seam, the shape
   `decisionNonce.ts` established.
3. Then the hero card itself with its CSS conformance guard, and T003's
   `remedy job digest` plus the end-to-end, the integration gate and closure.

## Risks
- R-0570 and R-0752 stay OPEN, routed to the paydown branch. R-0753 stays OPEN
  as this feature's documented risk: the persisted actuals record has no money
  field, so the digest's cost basis can only answer `absent` in production.
- Two homes for the urgency formula exist until the TypeScript copy is retired,
  pinned equal by `tests/ui_contracts/test_decision_urgency_parity.py`.
<<<END PLAN6

<<<BEGIN RECORD6
Gate: F040 R5 — T001'S LAST ACCEPTANCE CLAUSE, THE ENVELOPE GOLDENS. VERDICT PASS. Reviewed by re-running every gate in the reviewer's own driver; every figure the worker reported reproduced. TRANSPORT is REAL at sha256 `4e3bcefd476e46e33540e3d1216b31360cefcb84f69b7468bd3eee55cd07821c` over 27067 bytes, equal on all three copies. THE PLAN is byte-equal to PLAN5 at 1910 bytes and 40 lines. THE RECORD APPEND reconstructs whole at 1668053 + 1 + 10079 = 1678133, N counted as 3, paragraph order holding, base a prefix. THE LEDGER moved as ordered — registered 314 to 315 with ADDED `['R-0754']` and REMOVED `[]`, resolved ADDED `[]`, `DECISION F040` ADDED `['D6']`, one `^Gate: F040 R4 — ` line, open count 262. THE FOUR GOLDENS WERE READ BY THE REVIEWER AS STORED BYTES and match the envelope probe taken independently at `458e8d51` before the round was authored: eight keys each, `all-green`, `open-decision`, `blocked-failed` and `indeterminate` as the four rules, `job_id` normalized in every one, the blocked shape's `peak_urgency` the deterministic 2400 that (3+1)x600 gives under the module's frozen clock, and the em dash stored literally rather than as a `—` escape. THE REVIEWER RAN THREE MUTATIONS IN ITS OWN WORKTREE, control first in each, and all three bit exactly where they should. M1, changing the `all-green` label in PRODUCTION code at `packages/orchestration/run_report.py:411`: REAL exit 1, and the single dead test is `test_the_normalized_envelope_equals_its_stored_golden[green]` — so the goldens pin CONTENT and not merely shape. M2, the one that matters most and the one the block was written to make possible, WIDENING `_normalize` so it swallows any label containing the word `decision`: REAL exit 1 with TWO dead tests, the `blocked_with_decisions` golden AND `test_the_normalization_leaves_the_ctas_own_words` — so the narrowness guard is a real discriminator and not decoration, which is the difference between a golden that pins the CTA's words and one that has quietly normalized them away. M3, a LENGTH-PRESERVING perturbation of one stored golden's headline: REAL exit 1 on that shape alone, so the comparison is over content rather than size. Each restored run returned to 46 passed at REAL exit 0. NO SELF-BLESSING, re-measured by the reviewer over the committed bytes with `ast`: `GOLDEN_DIR` is bound exactly once, and a write-verb sweep WIDER than the block ordered — `write_text`, `write_bytes`, `dump`, `mkdir`, `touch`, `unlink`, `rmdir`, `rename`, `writelines`, `write` and `open` with a write mode — finds ZERO across the whole module, not merely across the new section. THE FEATURE FILE took an APPEND-shaped edit: FROM 1x, eleven TO-only lines each exactly 1x among eleven added lines and ZERO removed, `AMENDMENT A1`, `A2` and `A3` each exactly 1x, and T001's Task-slicing entry unchanged — the amendment records how the clause is MET and does not delete the clause, which is the distinction that keeps the acceptance list honest. DETERMINISM WAS MEASURED RATHER THAN ASSUMED, because a golden's characteristic failure is the flake: twelve consecutive runs of the module, all REAL exit 0. Six suites serially all REAL exit 0 — 46, 515, 699 with 4 skipped, `tests/docs/` 295, 16 and the canary 42 — `ruff` clean on the edited module, tree clean, zero untracked, seven commits at insertions 321, 229, 7, 6, 186, 11 and 365, every one under 500. THE WORKER'S TEN DEVIATIONS WERE ALL CORRECTLY DECLARED, and deviation 2 deserves naming because it repairs the REVIEWER's omission: the block ordered the golden section appended and said nothing about the module docstring, which until this round argued "A golden would keep passing while the digest and the report drifted apart" — a sentence that, left standing above the section it now precedes, would have been the R-0417 stale-prose class landing in the very file the round was extending. The worker rewrote it to "A golden ALONE would keep passing … so the golden section at the bottom stands BESIDE that assertion and never in place of it", declared it as unordered, and was right on both counts. The block should have ordered that pair; it did not, and the worker caught it.

Done: R-0754 — RESOLVED at `1f31b4dc` and `38dd0117`, and resolved by BUILDING the clause rather than by arguing it away. The finding was that T001 had been declared complete with its acceptance clause "Fixture goldens exact" never built and never discharged, and that the plan text had been narrowed in the same round that declared it done. BOTH HALVES ARE NOW ANSWERED. The clause is MET: four stored envelope goldens, one per state shape, live under `tests/orchestration/fixtures/job_digest/golden/` and are compared WHOLE against the envelope the same fixture builds, with exactly three identities normalized first. The narrowing is REVERSED rather than papered over: `.agent/plan.md` now carries the item "T001 the envelope goldens and R-0754" and the feature file carries AMENDMENT A3 stating how the clause is met, so a closure reading the acceptance list finds the answer beside the question instead of finding neither. VERIFIED BY THE REVIEWER, not taken from the handback: the goldens were read as stored bytes and matched an envelope probe taken independently before the round was authored, and three mutations — a production label change, an over-broad normalizer and a length-preserving byte perturbation — each reddened exactly the tests they should, with the unmutated control reported first in every case. THE COUNTER-MEASURE THE FINDING CARRIED IS IN FORCE FROM THIS BLOCK ON and is not merely promised: a block whose plan slice marks a T-slice `done` states, in the block itself, that slice's acceptance clauses and where each one is met. This block does that for T002 in the paragraph its Goal opens with, which is the first exercise of the rule. THE LESSON IS THE REVIEWER'S AND IS RECORDED HERE RATHER THAN IN A SLIP, because it is the finding's root cause: seven green gates in R4 and eight in R3 measured everything the block ordered and nothing the FEATURE FILE required, so a T-slice was declared complete against a plan row the same block had rewritten. A gate list is a claim about what was checked, never about what was owed.

DECISION F040 D7 — "COMPONENT TESTS" IN THIS REPOSITORY MEANS PURE-LOGIC VITEST PLUS A PYTHON SOURCE GUARD, BECAUSE NOTHING HERE CAN RENDER A COMPONENT. THE PROBLEM: `docs/roadmap/features/T5_F040.md:79-80` slices T002 as "hero card + CSS conformance + trigger/dismiss/last-seen mechanics + component tests", and a builder reading "component tests" will reach for a renderer. MEASURED by the reviewer at `4e5e9bf8`: `apps/ui/vitest.config.ts` sets `environment: "node"`, the repository ships NEITHER jsdom NOR a testing library, and every `.test.ts` under `apps/ui/src/api/` tests pure logic — no React component is rendered anywhere in this repository's tests. A second measurement bounds what a round may even attempt: direct `npx vitest` and `npm run test:unit` are REFUSED to this session class before execution, and because `apps/ui/node_modules` is gitignored it is absent from any disposable worktree, so the mutation red-proof guardrail G5 requires is unreachable for TypeScript — a mutation there is red for every possible module, which is the vacuous-probe shape R-0703 registered. CHOSEN, and it is a three-part reading of the clause rather than a refusal of it: (a) every DECIDABLE rule of the card goes into `apps/ui/src/api/*.ts` as a pure function and is covered by vitest, which the pytest node `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes` runs and which a broken module genuinely turns red; (b) the `.tsx` file keeps only wiring, and its structure and CSS conformance are pinned by a Python guard under `tests/ui_contracts/` reading the source as TEXT, the shape `test_cost_metric_render.py`, `test_design_drift.py` and `test_main_layout_guard.py` already establish, which needs no `node_modules` and IS red-proved normally; (c) types are checked by `tests/ui_server/test_dashboard_contract.py -k typescript`, whose result must be read as passed-or-SKIPPED because that node skips when the toolchain is absent and a skip is not a type check. ALTERNATIVES CONSIDERED: (i) add jsdom and a testing library to get real render tests — rejected on scope, that is a toolchain change affecting every UI feature and it is not F040's to make on its own authority; (ii) write render tests anyway and let them skip — rejected, a permanently skipped test is a false green and this repository's honesty rule prefers an absent test to a sleeping one; (iii) claim the clause unmeetable and drop it — rejected, the decidable half is most of the card's behaviour and it is fully testable, so dropping it would trade real coverage for a wording problem. HOW TO REVERSE: if a renderer is ever added, the `.tsx` guards become render tests and (b) retires; nothing in (a) changes, because a pure rule is worth testing purely either way. WHAT IT COSTS TO BE WRONG: the wiring inside the `.tsx` is pinned as TEXT rather than as behaviour, which is weaker, and the block that builds the card must therefore keep that file as thin as the guard can see.
<<<END RECORD6

<<<BEGIN PAIRACTUAL-FROM
/** The only basis string that means the figure is not an estimate. */
const ACTUAL_BASIS = "actual";
<<<END PAIRACTUAL-FROM

<<<BEGIN PAIRACTUAL-TO
/** The only basis string that means the figure is not an estimate.
 *  EXPORTED because the completion digest's cost line reads the same string
 *  (DECISION F040 D7): the bar and the hero card must agree about what
 *  "exact" is, and a second copy of this literal is the drift DECISION F040 D2
 *  already spent a round preventing for the urgency formula. */
export const ACTUAL_BASIS = "actual";
<<<END PAIRACTUAL-TO

## SPEC for C3 — `apps/ui/src/api/jobDigest.ts`

Read `apps/ui/src/api/recency.ts` for the house voice of a pure rule module,
`apps/ui/src/api/costMetric.ts` for the cost vocabulary, and
`apps/ui/src/api/remedyApi.ts:702-760` for `diffEnvelopePath` / `loadDiffEnvelope`
— the path-builder-plus-loader pattern F037 established for a per-job endpoint.
Follow them; invent no new pattern.

Open the module with a comment block in the house style: what it is, and the
DELIBERATE ABSENCES written where a reader will search for them (no clock, no
storage, no socket — per constraint 10), the way `decisionNonce.ts` does.

Export, with a one-line WHY comment above each definition:

- `JobDigestCost`, `JobDigestDecisions`, `JobDigestPrimaryAction` and
  `JobDigest` — the envelope's shape as TypeScript types, the eight top-level
  keys the goldens under `tests/orchestration/fixtures/job_digest/golden/` pin.
  Read one of those files for the exact shape rather than inferring it.
- `decodeJobDigest(raw: unknown): JobDigest | null` — the defensive decode, in
  the manner `normalizePipeline` and `normalizePromptTrace` answer `null` for a
  payload they cannot use. It answers `null` for a non-object, for a missing or
  non-string `job_id`, and for a `version` that is not the number the module
  expects; it never throws. Unknown EXTRA keys are ignored rather than rejected
  — the server may add a field before this client learns it, and D5's own
  reasoning is that an additive field needs no version bump.
- `JOB_DIGEST_VERSION` — the version this client understands, as a number.
- `digestCostLine(cost: JobDigestCost): { value: string; estimated: boolean }` —
  the card's cost line as a RULE, not as copy. `estimated` is
  `cost.basis !== ACTUAL_BASIS`, with `ACTUAL_BASIS` IMPORTED from
  `./costMetric` per constraint 9; `value` is the figure's own text.
  THIS MODULE WRITES NO PRESENTATION COPY. It does NOT contain the `~` marker
  and does NOT contain the words `, estimated`: `costMetric.ts` returns an
  `estimated` BOOLEAN and `apps/ui/src/components/metrics/TopMetricsBar.tsx`
  owns the strings as `ESTIMATE_MARK` and `ESTIMATE_PHRASE`, so the card renders
  them from there and the phrase keeps the one home it already has. Putting the
  copy here would be a second home for it — the same defect constraint 9 forbids
  for the basis string, one layer up.
- `jobDigestPath(request: { jobId: string; token: string; baseUrl?: string }): string`
  — the endpoint's path, built exactly the way `diffEnvelopePath` builds the
  diff's, INCLUDING its encoding of the token and its handling of `baseUrl`.
  The route the server serves is `GET /api/jobs/<job_id>/digest`; that is
  measured at `packages/orchestration/ui_server.py`, where `"digest"` is
  registered in the per-job handlers dict.

Do NOT add a loader that calls `fetch` this round — constraint 10 forbids the
socket, and the path builder is the half that is decidable and worth pinning.

## SPEC for C4 — `apps/ui/src/api/jobDigest.test.ts`

Read `apps/ui/src/api/recency.test.ts` and the `diffEnvelopePath` cases in
`apps/ui/src/api/remedyApi.test.ts:585-610` first, and follow their conventions.

Cover, at least: a well-formed envelope decoding to every field; `null` for a
non-object, for a missing `job_id` and for a wrong `version`; an unknown extra
key IGNORED rather than rejected; `digestCostLine` marking `absent` and
`lower_bound` as estimated and `actual` as not; and `jobDigestPath` over a plain
case, a token needing encoding and an explicit `baseUrl`.

ONE OF THESE IS THE POINT AND MUST BE WRITTEN AS SUCH: a test asserting
`digestCostLine` treats the string `"actual"` as exact THROUGH THE IMPORTED
`ACTUAL_BASIS`, not through a literal retyped in the test — so the day the
server renames that value, this test moves with it instead of pinning the old
name.

## SPEC for C5 — `tests/ui_contracts/test_job_digest_card_contract.py`

Read `tests/ui_contracts/test_cost_metric_render.py` for the convention: a
Python test that reads TypeScript source as TEXT and pins properties no
type-checker can see. Follow it.

STRIP COMMENTS AND STRING LITERALS BEFORE ASSERTING AN ABSENCE. A guard that
greps raw source reports its own prose: this module's header will NAME the
absences it promises, so a naive search for `localStorage` finds the comment
that says there is none. State in the module docstring that the stripping is
why the guard is honest.

Pin, over `apps/ui/src/api/jobDigest.ts`:

- THE PURITY, per constraint 10: over comment- and string-stripped source,
  `fetch`, `Date.now`, `new Date`, `localStorage`, `sessionStorage`, `crypto`
  and `XMLHttpRequest` each occur ZERO times.
- THE ONE-SOURCE COST STRING: the literal `"actual"` occurs ZERO times in
  `jobDigest.ts`, and `ACTUAL_BASIS` is IMPORTED there from `./costMetric`.
  Pair that zero with a POSITIVE CONTROL proving the search reaches the file at
  all — assert some string the module certainly contains — so a zero is
  distinguishable from a blind search.
- THE SINGLE HOME, measured across the directory: over comment-stripped,
  NON-TEST `.ts` sources under `apps/ui/src/api/`, the literal `"actual"`
  occurs exactly ONCE, and that occurrence is in `costMetric.ts`. The reviewer
  measured exactly this at the base and it held.
- NO PRESENTATION COPY: over comment-stripped source, `jobDigest.ts` contains
  neither the phrase `, estimated` nor a `~` marker, because
  `TopMetricsBar.tsx` owns both as `ESTIMATE_PHRASE` and `ESTIMATE_MARK` and a
  second copy is the drift this feature keeps paying to avoid. Assert against
  THAT component that the two constants still live there, so the guard fails if
  the copy moves rather than silently passing once it is gone.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C6, which writes the handback.

G1 TRANSPORT, at C0b. One sha256 over three files — `.remedy-wt/f040-r6-block.md`,
   the committed `.agent/authored/f040-r6.md` and `.agent/last_block.md` — with
   the byte length, all three EQUAL. This block states no expected digest.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN6 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length yourself; the
   reviewer read 1678133 at `4e5e9bf8`. Base + one separator newline + RECORD6
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION against
   the entire committed file; (b) PARAGRAPH ORDER — the last N blank-line units
   equal RECORD6's N paragraphs IN ORDER, N COUNTED by your script. Report that
   the base bytes are a PREFIX of the committed file. NEGATIVE CONTROL in a
   disposable worktree: flip one byte inside the FIRST appended paragraph and
   report that BOTH readings reject it and accept the unflipped bytes.

G4 THE LEDGER, at C2. Distinct `^- R-\d+ — ` ids before and after with ADDED
   `[]` and REMOVED `[]` — this round registers NO new finding. Distinct
   `^Done: R-\d+` ids with ADDED exactly `['R-0754']`. Distinct
   `DECISION F040 D\d+` with ADDED exactly `['D7']`. Exactly one
   `^Gate: F040 R5 — ` line. Report the open count and the fall from 262.

G5 THE PAIR AND THE SINGLE HOME, at C3. PAIRACTUAL is a REPLACEMENT, not an
   append: report FROM occurring exactly 1x in `costMetric.ts` BEFORE the edit
   and exactly 0x AFTER, and TO exactly 1x after. Then, over comment-stripped
   NON-TEST `.ts` sources under `apps/ui/src/api/`: the literal `"actual"`
   occurs exactly ONCE and it is in `costMetric.ts`; `jobDigest.ts` contains the
   string `ACTUAL_BASIS` and imports it from `./costMetric`. Name the files the
   sweep actually read and their count, so the absence is as wide as the search.

G6 THE GUARD AND ITS RED PROOF, at C5. First
   `python3 -m pytest tests/ui_contracts/test_job_digest_card_contract.py -q` —
   REAL exit 0 with the passed count. Then, INSIDE A DISPOSABLE WORKTREE, the
   UNMUTATED control FIRST, then TWO mutations of `jobDigest.ts`, each reverted
   before the next: (a) insert a real `Date.now()` call into a function body —
   the purity assertion must die; (b) replace the imported `ACTUAL_BASIS`
   comparison with the literal `"actual"` — the one-source assertion must die.
   Report each REAL exit code and WHICH tests died, never only a count. Restore,
   re-run, report the restored exit code and that the bytes equal the original.
   Name the worktree, remove it, report `git worktree list` no longer holds it.

G7 VITEST AND THE TYPECHECK, at C5, through the pytest nodes and NOT through a
   direct `npx` call, which is refused to this session:
   `python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs`
   and `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`.
   For EACH, report the REAL exit code AND whether the node PASSED or SKIPPED —
   a skip is not a type check and must not be reported as one. The reviewer
   measured 4 passed and 1 passed at the base, neither skipped. NO TypeScript
   mutation colour is ordered; say in the handback that none was run and why.

G8 THE SUITES AND THE TREE, at C5. Each its own REAL exit code:
   `python3 -m pytest tests/ui_contracts/ -q`,
   `python3 -m pytest tests/orchestration/test_job_digest.py -q`,
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/docs/ -q`, and the canary
   `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer measured
   699 passed with 4 skipped, 46, 515, 295 and 42 at the base; `tests/ui_contracts/`
   MUST rise by the number of tests C5 adds, so report both numbers and the
   difference. Then `git status --porcelain` EMPTY, `git ls-files --others
   --exclude-standard` count 0, and the per-commit insertion counts for C0a
   through C5, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state
block, the `## Commits` table with a `+/-` column taken from
`git diff --numstat`, the deviations, the item-status table with every bundle
item and every gate appearing exactly once, and the next steps. State
`SESSION 2` of F040 and round 6. No length cap. Record that T002's DECIDABLE
half is built and that no `.tsx` and no CSS landed this round, name R-0570,
R-0752 and R-0753 as OPEN and R-0754 as RESOLVED by C2, and name the next
action as T002 part 2 — the trigger, dismiss and last-seen rule as a pure
function over an injected seam, with the DECISION that rules where a dismissal
persists.
