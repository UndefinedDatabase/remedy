── STEP T003 migration-order step 4 / F105 — R20 ──────────────
Goal:        Gate R19 on disk, then migrate prompt-assembly site 4 —
             `build_orchestrator_prompt` and its system half — onto the
             prompt-segment registry, under a content-equality golden that
             pins BYTE equality with the pre-migration render.
Bundle:      C1a save block · C1b mirror to last_block · C2 live_review
             (R19 gate, R-0249, next-free-ID) · C3 production composition ·
             C4 golden test · C5 decisions.md (D6 amendment fixing R-0248,
             new DECISION D7) · C6 plan.md + handoff.md
Change:      exactly these paths, nothing else —
             `.agent/authored/f105-r20-1.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/handoff.md`,
             `packages/orchestration/orchestrator_loop.py`,
             `tests/orchestration/test_orchestrator_prompt_golden.py` (new).
Constraints: Do not touch any other production file. Do not change prompt
             CONTENT — only its composition. Do not edit
             `docs/agents/orchestrator_protocol.md`. Do not add a runtime
             writer for the protocol document (F070 Do-not-touch). Do not
             wire `on_call` / call evidence this round: that is DEFERRED by
             this block, see "Declared deferral" below. Do not touch
             `mission_compiler.py` (R-0246 belongs to a later round). No
             `tiktoken`, no new dependency.
Handback:    completion report + rewrite `.agent/handoff.md`
───────────────────────────────────────────────────────────────

## Declared deferral (not a silent scope cut)

`.agent/t003_inventory.md`'s migration order calls site 4's "real work" the
evidence gap — no production caller passes `on_call` to `run_mission`, so the
orchestrator manifest reaches no call evidence — plus the read-per-call hashing
question. This block CLOSES the hashing question as DECISION F105 D7 (C5) and
DEFERS the evidence gap to the already-planned round that wires `on_call` for
the mission and plan sites together. Reason: `apps/cli/commands/mission_cmd.py`
line 362 is the third of three call sites that need the same recorder pattern,
and doing all three in one round gives one pattern and one review instead of
three divergent ones. The deferral is recorded in `.agent/plan.md` at C6 and
must be named in the handback's item-status table.

## Commit order and content

### C1a — save the block
Write `.agent/authored/f105-r20-1.md` as instructed above. Commit it ALONE.
    git commit -m "chore(f105): save the R20 block verbatim"

### C1b — mirror the block to last_block
Copy `.agent/authored/f105-r20-1.md` over `.agent/last_block.md` (`cp`, so the
bytes are identical by construction). Commit alone.
    git commit -m "chore(f105): mirror the R20 block to last_block"

### C2 — live_review: the R19 gate, finding R-0249, next free ID
Apply PAIR_A, PAIR_B and PAIR_C to `.agent/live_review.md`. One commit.
    git commit -m "chore(f105): record the R19 gate and register R-0249"

### C3 — production: compose site 4 from registered segments
Edit `packages/orchestration/orchestrator_loop.py` ONLY. See "C3 detail".
    git commit -m "chore(f105): compose the orchestrator prompt from registered segments"

### C4 — the content-equality golden
Create `tests/orchestration/test_orchestrator_prompt_golden.py`. See "C4 detail".
    git commit -m "chore(f105): pin the orchestrator prompt with a content-equality golden"

### C5 — decisions: amend D6 (fixes R-0248), add D7
Apply PAIR_D and PAIR_E to `.agent/decisions.md`, and PAIR_F to
`.agent/live_review.md` (the authored `Done:` text for R-0248). One commit.
    git commit -m "chore(f105): amend DECISION D6 and record DECISION D7"

### C6 — plan and handoff
Apply PAIR_G to `.agent/plan.md` (full replacement). Rewrite
`.agent/handoff.md`. One commit.
    git commit -m "chore(f105): update the plan and write the R20 handoff"

Then: `git push -u origin feature/f105-cache-optimal-prompt-ordering`.

## C3 detail — the composition move

`build_orchestrator_prompt` (line ~797) currently returns, by f-string:

    build_orchestrator_system_prompt(repo_root) + "\n\n" + "# Mission state\n\n" + context.text

and `build_orchestrator_system_prompt` (line ~89) returns:

    "# Orchestrator protocol {PROTOCOL_VERSION}\n# Source: {PROTOCOL_DOC_RELATIVE} (versioned in the repository)\n\n" + orchestrator_protocol_text(repo_root)

Three segments fall out, and they are ALREADY in rank order, so unlike sites
1-3 this migration is byte-exact rather than equal-modulo-ordering. Preserve
that: the composed text must equal the pre-migration text byte for byte.

1. `orchestrator_system`, rank `SegmentStabilityRank.SYSTEM` — the two-line
   provenance header, WITHOUT its trailing blank line (the delimiter supplies
   it). Its bytes:
   `f"# Orchestrator protocol {PROTOCOL_VERSION}\n# Source: {PROTOCOL_DOC_RELATIVE} (versioned in the repository)"`
2. `orchestrator_protocol`, rank `SegmentStabilityRank.CONVENTIONS` —
   `orchestrator_protocol_text(repo_root)`, read per call (DECISION D7).
3. `orchestrator_mission_state`, rank `SegmentStabilityRank.JOB_CONTEXT` —
   `f"# Mission state\n\n{context.text}"`.

Add these public functions, both returning `ComposedPrompt`:

- `compose_orchestrator_system_prompt(repo_root: Path | None = None) -> ComposedPrompt`
  — registers segments 1 and 2.
- `compose_orchestrator_prompt(context: OrchestratorContext, repo_root: Path | None = None) -> ComposedPrompt`
  — registers segments 1, 2 and 3.

`compose_orchestrator_prompt` MUST build its own registry with all three
segments rather than string-concatenating the system `ComposedPrompt.text`
with a third segment: the manifest of the full prompt has to list all three
entries, which is the whole point of the manifest.

Then reduce both existing builders to `.text` of their composer, keeping their
signatures and docstrings intact (extend the docstrings, do not replace them):

    def build_orchestrator_system_prompt(repo_root: Path | None = None) -> str:
        return compose_orchestrator_system_prompt(repo_root).text

    def build_orchestrator_prompt(context, repo_root=None) -> str:
        return compose_orchestrator_prompt(context, repo_root).text

Import from `packages.orchestration.prompt_segments`: `ComposedPrompt`,
`PromptSegmentRegistry`, `SegmentStabilityRank`, `compose_prompt_segments`.
Follow the idiom already set by `packages/orchestration/flight_plan.py`
(`compose_flight_plan_prompt`) and `packages/orchestration/intake.py`
(`compose_intake_prompt`) — read both before you write, and match them.

Two placement constraints. `compose_orchestrator_prompt` takes an
`OrchestratorContext`, which is defined further down the module than line 89,
so put `compose_orchestrator_prompt` and `build_orchestrator_prompt` where
`build_orchestrator_prompt` already lives (~line 797) and keep the system pair
at ~line 89. Do not reorder the module. Second: this module is a POLICY layer
(Rule A6, stated in its own docstring) — you are moving composition into an
existing registry, not writing a new one.

Carry a one-line WHY comment directly above each new segment constant or
registration, in the shape the two reference sites use, naming the rank and
why it holds. Above `compose_orchestrator_prompt`, state the fact that makes
this site different: the pre-migration order was ALREADY rank-ordered, so the
migration is byte-exact and the golden asserts exact equality.

## C4 detail — the golden

New file `tests/orchestration/test_orchestrator_prompt_golden.py`. Module
docstring must state: this pins site 4's prompt while its composition moves to
the registry; the pre-migration forms below were sliced from
`git show 04a3396d:packages/orchestration/orchestrator_loop.py` and not one
byte was retyped; the file must NEVER be edited to make a failing test pass,
because an intentional CONTENT change is exactly the event it exists to fail on.

Obtain the pre-migration f-string bodies with that exact `git show`, sliced by
line index. Freeze them as two module constants — the system-prompt form and
the full-prompt form — as format strings whose only placeholders are the
version, the source path, the protocol text and the context text. The protocol
DOCUMENT is deliberately NOT frozen: it is large, it is expected to change, and
freezing it would turn this golden into a second copy of a document that
already has one home.

Tests to write (name them for what they assert):
1. `build_orchestrator_system_prompt()` equals the pre-migration system form
   rendered with the live `PROTOCOL_VERSION`, `PROTOCOL_DOC_RELATIVE` and
   `orchestrator_protocol_text()` — BYTE equality, `==`.
2. `build_orchestrator_prompt(context)` equals the pre-migration full form
   rendered the same way — BYTE equality. Use a small deterministic
   `OrchestratorContext`; construct it the way the existing
   `tests/orchestration/test_orchestrator_loop.py` constructs one, do not
   invent a new fixture shape.
3. The full manifest has exactly three entries, in this order, with these
   names and ranks: `orchestrator_system` 0, `orchestrator_protocol` 1,
   `orchestrator_mission_state` 3. Assert ranks are non-decreasing.
4. Each manifest entry's `sha256` equals `hashlib.sha256(<that segment's own
   text>.encode("utf-8")).hexdigest()`, and the composed text equals
   `PROMPT_SEGMENT_DELIMITER.join(<segment texts in manifest order>)` — i.e.
   composition injects no bytes of its own.
5. The cacheable-prefix payoff, MEASURED not asserted: compose two prompts from
   two contexts that differ ONLY in `context.text`; assert the two composed
   texts share a common prefix that ends exactly at the end of the protocol
   segment, that the `orchestrator_system` and `orchestrator_protocol` manifest
   hashes are equal across the two, and that ONLY the
   `orchestrator_mission_state` hash differs. Put the measured shared-prefix
   length into the assertion message so the number is visible in a failure.
6. `compose_orchestrator_system_prompt()`'s two-entry manifest is the prefix of
   the three-entry one — same names, ranks and hashes for entries 0 and 1.

## Done when (run every command; record the REAL exit code and real output)

A. Transport, disk to disk:
   `sha256sum .agent/authored/f105-r20-1.md .agent/last_block.md` — equal.
   `cmp .agent/authored/f105-r20-1.md .agent/last_block.md` — exit 0.
B. Block size: `wc -l .agent/authored/f105-r20-1.md` — must be <= 400.
C. Application, per target file:
   `grep -c '^- R-0249 ' .agent/live_review.md` -> 1
   `grep -c '^- Reviewer gate on R19 ' .agent/live_review.md` -> 1
   `grep -c '^  Done: R-0248 ' .agent/live_review.md` -> 1
   `sed -n '8p' .agent/live_review.md` -> ends `Next free ID: R-0250.`
   `grep -c '^## DECISION F105 D7 ' .agent/decisions.md` -> 1
   `grep -c 'committed BEFORE any of them at C1b' .agent/decisions.md` -> 0
   `grep -c '^===BEGIN\|^===END' .agent/live_review.md .agent/decisions.md .agent/plan.md` -> 0 for all three
   `wc -l .agent/plan.md` -> < 50
D. Round gate:
   `python3 -m pytest tests/orchestration/test_orchestrator_prompt_golden.py -q`
   `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q`
     — baseline before this round was `192 passed`; it must still pass, and
       state the new number and why it changed if it did.
   `python3 -m pytest tests/orchestration/test_prompt_segments.py -q`
   `python3 -m pytest tests/docs/ -q`  (a `.agent/`-only round still runs it;
     baseline 294 passed)
E. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` (baseline 42 passed).
F. Red-proof, in a DISPOSABLE `git worktree` at HEAD, NEVER in the primary
   checkout (AGENTS.md safety + protocol G5). Scratch goes under the gitignored
   `.remedy-wt/`. Three mutations, each reverted before the next:
   M1 — swap `orchestrator_protocol`'s rank to `STEERING`: the golden's rank
        and/or prefix test must go RED.
   M2 — drop the `# Mission state\n\n` prefix from segment 3: the byte-equality
        test must go RED.
   M3 — change the `orchestrator_system` segment to keep its trailing newline:
        byte equality must go RED.
   For each: record the command, the exit code, and the NAME of the failing
   test. Then revert and show the suite green again. Remove and prune the
   worktree afterwards; `git worktree list` must show the primary alone.
G. Hygiene, measured AFTER the C6 commit: `git status --porcelain` empty;
   `git log --numstat c65d663e..HEAD` — report the `+` column per commit and
   confirm each is under 500.

## PAIR list — shapes declared at authoring time

| Pair | Target | Shape |
|---|---|---|
| A | live_review | APPEND (TO contains FROM verbatim as its prefix) |
| B | live_review | REWRITE (FROM 0x after, TO 1x after) |
| C | live_review | APPEND |
| D | decisions | REWRITE |
| E | decisions | APPEND |
| F | live_review | APPEND |
| G | plan | full replacement, byte-for-byte equal to the slice |

For every APPEND pair prove: FROM occurs exactly 1x after, and each TO-ONLY
line occurs at least 1x. For every REWRITE pair prove: FROM 0x after, TO 1x
after. For every commit touching a state file, also report the count of added
lines that trace to NO authored TO slice — the stray count, which must be 0.

===BEGIN PAIR_A_FROM===
  entry in place, in the round that next touches `.agent/decisions.md`. OPEN.
===END PAIR_A_FROM===

===BEGIN PAIR_A_TO===
  entry in place, in the round that next touches `.agent/decisions.md`. OPEN.
- R-0249 (Low, F105 R19, the plan names a narrower function than the migration
  order does): `.agent/plan.md` sends R20 to "migration-order step 4,
  `orchestrator_loop.py::build_orchestrator_system_prompt`". The migration order
  in `.agent/t003_inventory.md` — which that same plan names as the authority
  over how T003 is counted — lists step 4 as `build_orchestrator_prompt`, the
  OUTER composition at line 797, and describes it as "two segments, already
  rank-ordered". `build_orchestrator_system_prompt` at line 89 is only its
  rank-0/rank-1 half. A worker reading the plan alone migrates the inner
  function and leaves the outer one an f-string that concatenates a composed
  prompt with a raw section header; the round's own acceptance — this prompt
  composes from registered segments — is then false for the prompt actually
  sent, and the manifest describes a strict prefix of it. This is not a wrong
  spec: the inventory is right and the plan abbreviated it. Fix: the plan names
  `build_orchestrator_prompt` and says its system half migrates with it. The
  fix lands in this round's plan rewrite; the next gate verifies it and
  resolves this entry. OPEN.
===END PAIR_A_TO===

===BEGIN PAIR_B_FROM===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0249.
===END PAIR_B_FROM===

===BEGIN PAIR_B_TO===
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0250.
===END PAIR_B_TO===

===BEGIN PAIR_C_FROM===
  70156f31 -> c65d663e.
===END PAIR_C_FROM===

===BEGIN PAIR_C_TO===
  70156f31 -> c65d663e.
- Reviewer gate on R19 (2026-08-09, the next session's reviewer, paying the
  gate R19 was owed as the session terminator): PASS. Range `c65d663e..HEAD`
  at 04a3396d, FIVE commits, FIVE paths, every one `.agent/` state — exactly
  the block's declared change set, no production file and no test file, so no
  mutation red-proof was owed and none is claimed. Insertions from
  `git log --numstat`: 230, 137, 17, 51 and 53, each under 500; C1b's 137/-307
  and C4's handoff rewrite are each the verbatim rewrite of one state file.
  Transport was re-proved disk to disk by the reviewer rather than read out of
  the handback: `.agent/authored/f105-r19-1.md` and `.agent/last_block.md` both
  hash to 7f8cd1eb1a388d07c74381658934d473c1afdd4447e546784e3b88bc4a3638c3,
  `cmp` exits 0, and both are 230 lines, so the handback's `7f8cd1eb…` is the
  real digest and D5's 400-line cap holds with room. Application checked per
  target: `grep -c '^- R-0248 '` is 1 and `grep -c '^- Reviewer gate on R18 '`
  is 1, so neither the finding nor the owed gate was applied twice; line 8 read
  `Next free ID: R-0249.`; marker LINES `^===BEGIN|^===END` count 0 in both
  `.agent/live_review.md` and `.agent/plan.md`.
  Gates re-run by the reviewer with real exit codes, none accepted as a word:
  canary `tests/cli/test_golden_path.py` 42 passed in 19.35s; `tests/docs/`
  294 passed; `tests/ui_server/test_dashboard_contract.py` 70 passed;
  `tests/orchestration/test_integrity_gate.py` 15 passed; the `.agent` state
  contracts 2 passed / 16360 deselected under the reviewer's own `-k` selector.
  `git status --porcelain` was empty and `git worktree list` showed the primary
  alone, so G5 holds and no destructive check leaked into the checkout.
  Honest gap, stated rather than papered over: the handback's fourth D-gate
  item, `remedy integrity check --json`, could NOT be executed — this session's
  shell layer refused the invocation — so the reviewer ran the integrity gate's
  own test file instead and does NOT restate the handback's `passed=True,
  fail_count=0` over 5 checks. That number stays the worker's claim, unverified
  here. It gates nothing this round, because R19 shipped no code for the
  integrity checker to have an opinion about; a round that ships code does not
  get the same pass.
  The declared counts check out against the commands that produced them:
  `wc -l` returns 46 for `.agent/plan.md`, under the <50 rule, and 85 for
  `.agent/handoff.md`, exactly the number the D15 overage line declares — the
  overage is stated truthfully rather than rounded, which is the whole test of
  a stated-cause deviation. All four declared deviations ACCEPTED; deviation
  2's benign 2x sentence collision was re-counted and the PAIR_C block itself
  occurs exactly 1x, which is the claim that matters. Deviation 3 is the R-0248
  gap, already registered and fixed this round. One finding is registered
  against the handback's planning record rather than against R19's work,
  R-0249. `LAST_REVIEWED_SHA` advances c65d663e -> 04a3396d.
===END PAIR_C_TO===

===BEGIN PAIR_D_FROM===
D6 — within one delegated round, `.agent/plan.md` is rewritten in the round's
LAST commit and the Commit Gate's plan check is satisfied for the round's
intermediate commits by `.agent/last_block.md`, which carries the round's plan
verbatim and is committed BEFORE any of them at C1b. The plan of record for an
in-flight round is the block; `.agent/plan.md` states where the FEATURE stands,
and mid-round it stands nowhere new yet.
===END PAIR_D_FROM===

===BEGIN PAIR_D_TO===
D6 — within one delegated round, `.agent/plan.md` is rewritten in the round's
LAST commit and the Commit Gate's plan check is satisfied for the round's
intermediate commits from C1b onward by `.agent/last_block.md`, which carries
the round's plan verbatim. C1a is the exception, and it is covered differently
rather than not at all: it precedes C1b — DECISION D5 split them in that order
so the block is counted once — and what it commits is
`.agent/authored/<round>.md`, the block's OWN verbatim copy, so for that one
commit the plan of record and the commit content are the same bytes and agree
by construction. The plan of record for an in-flight round is the block;
`.agent/plan.md` states where the FEATURE stands, and mid-round it stands
nowhere new yet.

Amended at F105 R20 to fix finding R-0248. The original text said the block is
"committed BEFORE any of them at C1b", which a reader can falsify with one
`git log`: C1a comes first. The mechanism was sound; the word "any" overclaimed
its reach.
===END PAIR_D_TO===

===BEGIN PAIR_E_FROM===
licence to leave the file stale. Blocks stop declaring the ordering as a
deviation and cite this entry instead.

Reverse this decision by deleting this entry.
===END PAIR_E_FROM===

===BEGIN PAIR_E_TO===
licence to leave the file stale. Blocks stop declaring the ordering as a
deviation and cite this entry instead.

Reverse this decision by deleting this entry.

## DECISION F105 D7 — the protocol document is hashed per call (2026-08-09)

Context: `.agent/t003_inventory.md` hands migration-order step 4 an open
question it calls the read-per-call hashing question.
`orchestrator_protocol_text` reads `docs/agents/orchestrator_protocol.md` from
disk on EVERY call to `build_orchestrator_system_prompt`, and the segment
registry hashes whatever text it is handed. Registering the document as a
segment therefore re-reads and re-hashes, once per iteration, a file that does
not change within a run. The alternative was to read and hash it once — at
import, or at first registration — and reuse the digest for the rest of the
run.

D7 — the document is read and hashed PER CALL. The manifest has exactly one
job: to record the bytes that were actually sent. A digest cached at
registration records the bytes that were sent the FIRST time, so if the
document is edited mid-run the manifest reports a hash for text that no
provider ever received. That is the overclaim class the Proof Chain exists to
prevent, and a manifest that can lie about its own subject is worth less than
no manifest, because it is believed. What the caching would buy is one read of
a small file per iteration, set against a loop that already assembles a
dossier, reads the mission record, reads the stop file and appends a ledger
entry every iteration.

Worth stating because it is the obvious objection: this costs no cache hits.
Re-reading unchanged bytes yields the same bytes, so the composed prefix stays
byte-identical across iterations and the provider cache still hits it. Only a
genuine edit produces a different hash and a miss, and that miss is CORRECT —
the prompt really did change, and F105's whole argument is that a miss should
be explainable rather than mysterious.

Scope: this site. It sets no rule for segments whose source is expensive to
read. A future segment backed by something costly may cache its digest, and
when it does it declares the staleness window it is accepting, in its own
entry.

Reverse this decision by deleting this entry.
===END PAIR_E_TO===

===BEGIN PAIR_F_FROM===
  entry in place, in the round that next touches `.agent/decisions.md`. OPEN.
===END PAIR_F_FROM===

===BEGIN PAIR_F_TO===
  entry in place, in the round that next touches `.agent/decisions.md`.
  Done: R-0248 — fixed at F105 R20, in the round that next touched
  `.agent/decisions.md`, exactly as the finding directed. DECISION D6's
  mechanism sentence now reads "from C1b onward" and states that C1a is covered
  by committing the block's own verbatim copy, so the coverage claim matches
  what `git log` shows. The amendment is marked as an amendment inside the
  entry, naming R-0248 and quoting the phrase that overclaimed, so a later
  reader can see what changed without diffing. RESOLVED.
===END PAIR_F_TO===

===BEGIN PAIR_G===
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 merged at the Open PR Gate. One-session self-drive, one delegated
worker per round. The next free finding ID lives in `.agent/live_review.md`
line 8 and is deliberately not duplicated here (R-0240's root cause).

## Goal

Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals.
Prompt CONTENT does not change; only its composition.

## Current Step

T001 and T002 are DONE and gated. T003 counts in the MIGRATION ORDER of
`.agent/t003_inventory.md`, never that file's catalogue "Site N" headings
(R-0241). Migration-order steps 1 (`intake.py`), 2 (`mission_compiler.py`),
3 (`flight_plan.py`) and 4 (`orchestrator_loop.py`) are COMPLETE, each with its
own golden; step 4 covers `build_orchestrator_prompt` AND its system half
`build_orchestrator_system_prompt`, and is the only one so far whose golden
asserts BYTE equality rather than equality modulo ordering, because its
pre-migration order was already rank-ordered (R-0249). `LAST_REVIEWED_SHA` is
04a3396d; R20 is ungated. Open findings: R-0221, R-0239, R-0246, R-0247,
R-0249. No PR; one is created at CLOSURE.

## Next Steps

- The next round gates R20 FIRST, then takes migration-order step 5,
  `pingpong_loop.py::_build_builder_prompt` — twelve conditional parts and a
  `"\n".join` whose blank-line runs must be reproduced exactly.
- Then step 6, `pingpong_loop.py::_build_reviewer_prompt`, last and highest
  content-equality risk. One builder per round, each with its own golden.
- BEFORE step 5, decide whether the schema tail from `build_schema_prompt` /
  `native_schema_prompt` becomes a registered rank-4 segment. Until that is
  settled, every manifest for sites 1-4 describes a strict prefix of the bytes
  actually sent.
- ONE later round wires `on_call` for all three sites that lack call evidence —
  `mission_cmd.py:362` (orchestrator, deferred by R20's block),
  `mission_cmd.py:187` + `gauntlet_runner.py:505` (mission), and
  `do_cmd.py:253` + `:2860` (plan) — one recorder pattern, one review.
- Fix R-0246 in the round that next touches `mission_compiler.py`.
- Register the Phase-0 gap the R17 gate records: the protocol gives no
  disposition for a tree a dead session left dirty. Not yet a DECISION.
- Then T004, `remedy stats cache` over actuals; then the integration gate
  (docs/agents/integration_gate.md); then closure
  (docs/roadmap/STATUS_closure_protocol.md), where the PR is created.

## Risks

- R-0221 stays open and will cost the integration gate phantom base-only
  failures.
- Four of the six migrated builders still reach no call evidence, so F105's
  every-role acceptance line is met for intake only until that round lands.
===END PAIR_G===
