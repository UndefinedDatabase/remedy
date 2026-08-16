── STEP R1 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Claim F085 in the ledger, reset the live-review record while carrying the F083
open set forward, and register the one closure candidate the reviewer's R28
closure review of F083 produced. No production code, no test content, no
inventory yet — R2 is the seam inventory.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r1.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  reset `.agent/live_review.md`: authored header + Steps + Findings, then
      R-0490, then the F083 open set carried forward verbatim
  C2  claim: `docs/roadmap/STATUS.md` pair + `.agent/context.md` +
      `.agent/plan.md` + `.agent/candidates.md`, whole-file for the three
      `.agent` files
  C3  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `a5a70621`, the tip of `origin/main` (merge of PR #203).
Every range gate below names that SHA. The branch is `feature/f085-sandbox-hardening`,
cut from `origin/main` AFTER the Open PR Gate is run and recorded.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are LIVEREVIEW-HEADER, R0490, STATUSLINE-FROM, STATUSLINE-TO,
CONTEXT, PLAN and CANDIDATES. Every slice's bytes end with a single trailing
newline, and every whole-file slice is the COMPLETE file including that newline.

──────────────────────────────────────────────────────────────

Change:

0. Open PR Gate, before any branch is created. Run
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` and
   record the raw output in the handback. The reviewer measured `[]` at
   authoring time; if it is still `[]` nothing is merged and you continue. If it
   is NOT `[]`, stop and hand off — do not merge and do not create the branch.
   Then `git checkout main`, `git pull --ff-only`, confirm `git rev-parse HEAD`
   equals `a5a70621`, and `git checkout -b feature/f085-sandbox-hardening`.
   Do NOT delete the local `feature/f083-ci-self-check` branch; it is merged and
   left alone (self-drive protocol G2).

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f085-r1.md`. The reviewer's original is on disk at
   `.remedy-wt/f085-r1.md`; copy that file rather than retyping it (`cp` may be
   denied — `shutil.copyfile` is an acceptable substitute; the gate names the
   byte property, not the tool). Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r1.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — rebuild `.agent/live_review.md` in this exact order, then commit:
   a. the LIVEREVIEW-HEADER slice, byte-verbatim;
   b. the R0490 slice, byte-verbatim;
   c. the F083 open set, carried forward VERBATIM and never retyped. Extract it
      programmatically from the PRE-RESET file — the blob at `a5a70621` —
      like this: a finding paragraph is a line matching `^- R-\d+ — `; a
      resolution is a line matching `^Done: R-\d+ — `; the open set is every
      finding paragraph whose id has no resolution line anywhere in that file.
      Append those paragraphs in the order they appear in the pre-reset file,
      each separated from the next by exactly one blank line, each byte-equal to
      its pre-reset original. The reviewer measured the pre-reset file at
      `a5a70621` as 117 registered ids, 13 resolved, 0 `Landed:` lines, 0
      duplicate ids and 0 resolutions naming an unregistered id.

4. C2 — the claim, one commit, four files:
   a. `docs/roadmap/STATUS.md`: replace the single line STATUSLINE-FROM with
      STATUSLINE-TO. This is a REWRITE pair (the TO does not contain the FROM),
      so the proof is FROM 0x and TO 1x over the whole file after the edit.
   b. `.agent/context.md`: whole file := the CONTEXT slice.
   c. `.agent/plan.md`: whole file := the PLAN slice.
   d. `.agent/candidates.md`: whole file := the CANDIDATES slice.
   README.md is NOT touched: its "Next: F085 (Sandbox hardening, stage 1)" line
   and its capability counters are already correct at the base and only move at
   closure. The reviewer verified that at `a5a70621`.

5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
   Its state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~2 % (F085 beansprucht · T001/T002/T003 offen) — Schätzung`
   Include the per-commit changed-files tables, the item-status table, every
   gate reading below with its real exit code, and any declared deviation.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   `.agent/plan.md` current before every commit; push after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass.
3. No production code, no test file, no `docs/` file other than
   `docs/roadmap/STATUS.md` is touched this round. If the work seems to require
   one, stop and hand off.
4. Destructive or red-proof verification runs only inside a disposable
   `git worktree` under `.remedy-wt/`, never in the primary checkout, which
   satisfies `git status --porcelain` == empty at the handback.
5. Never force-push, never rebase, never amend, never work on `main`, never
   delete a branch. Do not create the PR this round — the branch is pushed and
   the PR is created at closure.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand
   back. A red gate ends the round honestly.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent.
G2  TRANSPORT: `.remedy-wt/f085-r1.md`, the committed `.agent/authored/f085-r1.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/live_review.md` at HEAD: recompute the sets with the same two
    regexes named in C1. Report registered, resolved, `Landed:`, duplicate ids
    and resolutions naming an unregistered id. REQUIRED: the set of OPEN ids at
    HEAD equals the set of OPEN ids in the blob at `a5a70621` PLUS exactly
    `R-0490`, as a set comparison — report the two counts rather than predicting
    them, and report the max id and the next free id.
G4  Every carried paragraph is byte-equal to its pre-reset original: for each
    carried id, compare the paragraph at HEAD against the paragraph extracted
    from the blob at `a5a70621`. Report the number compared and the number
    equal; those two numbers must agree.
G5  `.agent/live_review.md` contains the substring `Steps`.
G6  `docs/roadmap/STATUS.md` at HEAD: STATUSLINE-FROM occurs 0x, STATUSLINE-TO
    occurs 1x, `^- \[~\]` occurs exactly 1x, `^- \[x\] F\d{3} — ` still occurs
    50x, and `<<` occurs 0x. The reviewer measured FROM 1x, `[~]` 0x and
    `[x] F` 50x at `a5a70621`.
G7  `.agent/context.md` at HEAD contains `## Active Branch`, the substring
    `feature/`, the substring `Steps`, a match of `\bF\d{3}\b`, and `resource`
    or `pytest` case-insensitively; and does NOT contain any of
    `allow repo_test_run`, `synthetic_count: 4`, `job=None source_apply bypass`,
    `steps-74_1-79`, `steps-91-100`, `Steps 91-100`, `feature/steps-74`,
    `PR #33`.
G8  `.agent/plan.md` at HEAD contains `## Goal`, `## Next Steps` and a match of
    `\bF\d{3}\b`, and is under 50 lines. Report the line count.
G9  Each of `.agent/context.md`, `.agent/plan.md`, `.agent/candidates.md` is
    byte-equal to its slice. Report each file's sha256 and line count.
G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
    → exit 0. These four files are the readers of the state files this round
    rewrites. Report the passed count and the exit code. RUN THIS IN THE PRIMARY
    CHECKOUT, not in a worktree: the reviewer measured `157 passed`, exit 0,
    in the primary checkout, and the SAME command in a fresh worktree is red on
    `TestVitestFrontendTestFoundation::test_vitest_passes`, which spawns
    `npx vitest run` and cannot resolve `apps/ui/node_modules` because that
    path is gitignored and therefore absent from every fresh worktree by
    construction. That red is the known R-0480 mechanism and not a base red.
G11 `python3 -m pytest tests/docs/ -q` → exit 0. The reviewer measured
    `295 passed` at `a5a70621`. This round changes `docs/roadmap/**`, which is
    what makes this gate mandatory.
G12 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed` at `a5a70621`.
G13 `git diff --name-only a5a70621..HEAD` lists exactly this set and nothing
    else: `.agent/authored/f085-r1.md`, `.agent/candidates.md`,
    `.agent/context.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md`.
    Report the real list and flag any difference rather than editing to match.
G14 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1 and C2 only. None may exceed 500. C3's own insertion count cannot
    exist while C3's text is being written, so it is reported in your FINAL
    MESSAGE — the round report, written after C3 exists — and not in this file.
G15 `git log --format=%p a5a70621..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` and `checkout:` entries —
    no amend, rebase, reset or force-push.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push the branch with
`git push -u origin feature/f085-sandbox-hardening`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE LIVEREVIEW-HEADER>>>
# Live Review — F085 Sandbox hardening (stage 1)

> Round-by-round review record for the F085 branch, reset at the feature claim.
> The F083 record closed with PR #202, merged 2026-08-16, and the operator
> amendment PR #203 followed it on `main`; that branch's closing verdict lives
> in its handoff and in the PR, per docs/agents/planner_reviewer_prompt.md §4
> item 13. Finding ids continue the monotonic R-XXXX series across the reset.
> Next free id: R-0491.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The findings open when
> the F083 record closed are reproduced verbatim at the end of this file,
> extracted by id out of the previous record and never retyped. The pre-reset
> record held no `Landed:` line.

## Steps
R1 claim F085, reset this record carrying the F083 open set forward, and
register R-0490 out of the reviewer's R28 closure review → R2 the subprocess
seam inventory: every `subprocess.*` call site in `packages/` and `apps/`, each
with its enclosing symbol, its command class, the source of its cwd, its
environment handling, whether it carries a timeout and whether its output is
bounded, plus the AST guards that already constrain those files and the R-0202
spawn path → R3 record R2 and rule the stage-1 command classes and their
policies as a DECISION → R4 T001 `exec_guard.run_guarded` with rlimits, a wall
timeout distinct from the provider timeouts, and output caps → R5 T001 the
runaway fixtures — cpu, memory, output and sleep — each killed and each
classified `resource_limit` with the tripped limit named → R6 record R4 and R5 →
R7 onward T002 seam migration, one order per seam with behaviour-equality
goldens for well-behaved commands, plus environment scrubbing and its allowlist
test → then T003 the network posture, the per-class policies, the honest
limitations document and its README link → then the integration gate → then
closure. The map from R7 on is planned rather than measured: the inventory R2
produces is what fixes the seam order, and a round that changes this map records
the change as a DECISION in this file. Each round marks the PREVIOUS one done
and never itself; the FULL map is stated here ONLY. Another file may name at
most the NEXT round — `.agent/plan.md` must, because AGENTS.md mandates its Next
Steps section — and naming one round is not restating the map (R-0447, R-0455).

## Findings
<<<END LIVEREVIEW-HEADER>>>

<<<SLICE R0490>>>
- R-0490 — Low, THE CLOSURE PROTOCOL'S PRODUCER-PITFALL LIST NEVER STATES THAT `output_hash` MUST BE THE SHA-256 OF `stdout_summary` EXACTLY, AND F083'S FIRST CLOSURE PACKAGE WAS BLOCKED BY THAT GAP. Raised by the reviewer during the R28 closure review of F083 and registered here as a closure candidate, per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings". The R28 worker hashed the FULL pytest stdout while recording only its last line as `stdout_summary`, and `scripts/build_review_manifest.py` requires `output_hash == sha256(stdout_summary)`, so packaging attempt 1 returned PACKAGE_STATUS=BLOCKED_EVIDENCE with the single verbatim error `verification_tests.json runs[0] output_hash does not match sha256(stdout_summary)`. The worker repaired it inside the round — the whole 181-character stdout recorded as `stdout_summary` and hashed exactly, the evidence job and the zip rebuilt from the same clean tree at the same head, nothing committed changed between the two attempts — and attempt 2 packaged READY_FOR_REVIEW. That reading of protocol step 2's "fix or go `[!]`" branch is correct and the reviewer accepts it. The reviewer re-verified the delivered package independently rather than accepting the handback: sha256 162bacf6265e79651b098c524b5060de44d58e9d89e9ec4d645c158950b78986 recomputed from disk, `zipfile.testzip()` None, 6284 members. Nothing false was closed over, which is why this is Low rather than Medium. It is registered because the pitfall list at that document's Algorithm step 1 carries (a) node ids with `len(node_ids) == selected`, (b) `test_files` entries that are files and never directories, (c) the `^vr-\d{4,}$` run_id regex and (d) never a full-suite node-id list, and says of this field only that verification_runs entries "need a sha256-hex output_hash" — which the BLOCKED package had. The exact-preimage rule is a sixth pitfall that document does not carry, the fifth being R-0448's sorted-`test_files` rule, which is still open and routed the same way. The fix is one bullet in `docs/roadmap/STATUS_closure_protocol.md`; that is a process doc F085 does not own and AGENTS.md forbids mixing an unrelated fix into a feature branch, so it routes to the same paydown branch as R-0403, R-0448, R-0482 and R-0487. OPEN.
<<<END R0490>>>

<<<SLICE STATUSLINE-FROM>>>
- [ ] F085 — Sandbox hardening (stage 1)
<<<END STATUSLINE-FROM>>>

<<<SLICE STATUSLINE-TO>>>
- [~] F085 — Sandbox hardening (stage 1)
<<<END STATUSLINE-TO>>>

<<<SLICE CONTEXT>>>
# Context — F085 Sandbox hardening (stage 1)

## Active Branch
feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after the F083
closure PR #202 and the operator amendment PR #203 were both merged. Self-drive
session per docs/agents/self_drive_protocol.md: the main session plans and
reviews and writes nothing in the work tree, one delegated worker per round
makes every commit.

## Scope
In: stage-1 containment for builder-, test- and DoD-spawned subprocesses — a
common `exec_guard` seam carrying POSIX resource limits, a wall timeout distinct
from the provider timeouts, output-size caps, a cwd pinned inside the worktree,
an environment allowlist, and a default-deny network posture for build and test
commands, plus the honest limitations document and its README link. The tripped
limit becomes an additive `resource_limit` postmortem class.

Out, per the feature file's Do-not-touch: container isolation, provider
transport timeouts, and fence semantics. Windows is explicitly out of scope for
stage 1 and is documented as such. No wording anywhere — code comments included
— may claim more containment than is enforced.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/, and a round rewriting `.agent/` state also gates the four files
  that read that state live: tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a gate (R-0364); ruff is gated scoped to the files a round touches,
  measured against the SAME files at origin/main so a pre-existing error is not
  read as a new one.
- Two AST guards already constrain this feature's target files and bind every
  seam order: `test_no_subprocess_in_discovery_module` forbids `subprocess.run`
  in packages/orchestration/command_discovery.py, and
  `test_no_shell_true_in_orchestration` forbids `shell=True` anywhere in
  packages/orchestration/*.py.
- 104 findings are open at the claim, carried forward into the reset record per
  DECISION F057 D1. R-0403, R-0448, R-0482, R-0487 and R-0490 are routed to a
  paydown branch and are deliberately not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXT>>>

<<<SLICE PLAN>>>
# Plan — F085 Sandbox hardening (stage 1)

Branch: feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after
the F083 closure PR #202 and the amendment PR #203 merged.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
Builder-spawned commands stop relying on prompted discipline: every builder,
test and DoD subprocess gets POSIX resource limits, a per-command wall timeout,
output-size caps, a cwd pinned inside the worktree, an environment allowlist and
a default-deny network posture — with a document that says EXACTLY what stage 1
does and does not prevent. DONE when the limits provably kill a runaway fixture
(cpu, memory, oversized output, endless sleep) and classify it `resource_limit`
with the tripped limit named, an off-scope write attempt fails, well-behaved
commands behave identically under the guard, a secret-like parent env var never
reaches a child, and the limitations document exists and is linked from the
README.

## Current Step
R1, this round: the Open PR Gate, the branch, the STATUS claim `[ ]` → `[~]`,
the live-review reset carrying the F083 open set forward, and the registration
of R-0490. No production code and no test content.

## Next Steps
1. R2 — the subprocess-seam inventory in `.agent/f085_inventory.md`: every
   `subprocess.*` call site in `packages/` and `apps/` with its enclosing
   symbol, command class, cwd source, environment handling, timeout and output
   bounding. The reviewer measured 73 such call sites across 33 files at
   a5a70621; the feature file's premise of "a small number of helpers" is what
   R2 tests.

## Risks
- The feature file says subprocess execution "already flows through a small
  number of helpers". At 73 call sites in 33 files that premise is unproven, and
  if R2 disproves it the seam migration T002 plans is a much larger job than the
  task slicing assumes. That is a spec finding for R3, not a reason to widen R2.
- R-0202 is carried into this feature: a spawned path once ignored
  REMEDY_UI_NO_AUTO_BUILD and the mechanism was never explained. The inventory
  must locate that path rather than assume it is gone.
<<<END PLAN>>>

<<<SLICE CANDIDATES>>>
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

The carrier is empty. The one candidate F083's closure review produced was
registered as R-0490 in `.agent/live_review.md` at F085 R1, which is what the
closure protocol asks the next feature's first reviewed round to do.
<<<END CANDIDATES>>>
