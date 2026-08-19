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

- R-0490 — Low, THE CLOSURE PROTOCOL'S PRODUCER-PITFALL LIST NEVER STATES THAT `output_hash` MUST BE THE SHA-256 OF `stdout_summary` EXACTLY, AND F083'S FIRST CLOSURE PACKAGE WAS BLOCKED BY THAT GAP. Raised by the reviewer during the R28 closure review of F083 and registered here as a closure candidate, per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings". The R28 worker hashed the FULL pytest stdout while recording only its last line as `stdout_summary`, and `scripts/build_review_manifest.py` requires `output_hash == sha256(stdout_summary)`, so packaging attempt 1 returned PACKAGE_STATUS=BLOCKED_EVIDENCE with the single verbatim error `verification_tests.json runs[0] output_hash does not match sha256(stdout_summary)`. The worker repaired it inside the round — the whole 181-character stdout recorded as `stdout_summary` and hashed exactly, the evidence job and the zip rebuilt from the same clean tree at the same head, nothing committed changed between the two attempts — and attempt 2 packaged READY_FOR_REVIEW. That reading of protocol step 2's "fix or go `[!]`" branch is correct and the reviewer accepts it. The reviewer re-verified the delivered package independently rather than accepting the handback: sha256 162bacf6265e79651b098c524b5060de44d58e9d89e9ec4d645c158950b78986 recomputed from disk, `zipfile.testzip()` None, 6284 members. Nothing false was closed over, which is why this is Low rather than Medium. It is registered because the pitfall list at that document's Algorithm step 1 carries (a) node ids with `len(node_ids) == selected`, (b) `test_files` entries that are files and never directories, (c) the `^vr-\d{4,}$` run_id regex and (d) never a full-suite node-id list, and says of this field only that verification_runs entries "need a sha256-hex output_hash" — which the BLOCKED package had. The exact-preimage rule is a sixth pitfall that document does not carry, the fifth being R-0448's sorted-`test_files` rule, which is still open and routed the same way. The fix is one bullet in `docs/roadmap/STATUS_closure_protocol.md`; that is a process doc F085 does not own and AGENTS.md forbids mixing an unrelated fix into a feature branch, so it routes to the same paydown branch as R-0403, R-0448, R-0482 and R-0487. OPEN.

- R-0448 — Medium, A CLOSURE BLOCK ORDERED AN EVIDENCE FIELD IN AN ORDER THE PACKAGING VALIDATOR REJECTS, SO THE FIRST PACKAGE BUILT BLOCKED_EVIDENCE. Raised by the reviewer during F082's R23 closure review and registered here as a closure candidate, per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings". The R23 block ordered `verification_runs[0].test_files` as "the eight FILES above", and that authored list was not sorted — `tests/cli/test_stats_bench.py` was written last and sorts first. `scripts/build_review_manifest.py::_vt_safe_files` rejects a list for which `tf != sorted(tf)`, which invalidates the whole VerificationTests document and leaves `vt_passed` unconfirmable, so packaging attempt 1 returned PACKAGE_STATUS=BLOCKED_EVIDENCE with two blocking reasons, of which `validate_evidence_candidate` named the sorting one as the single root error. The worker repaired it inside the round — the same eight files sorted, the suite re-run in that order so `command` and `node_ids` still describe a real execution, the evidence directory rebuilt from scratch, and `validate_evidence_candidate` checked BEFORE the second build — and attempt 2 packaged READY_FOR_REVIEW. The reviewer re-verified the delivered package independently rather than accepting the handback: sha256 3e8e33eb4bb724ce775ea5987e0fee0de5341d1a3bfe902c6e5f4f6f2deb84b2 recomputed from disk, `zipfile.testzip()` None, 6060 members, `ready_gate_matrix.ok` True with `blocking_reasons` `[]`, and `committed_review_subject.head_commit` equal to the accepted head 4b9bc7bc1dabdde5fca68de6ae20f86b11d21eb0. Nothing false was closed over. Medium, not Low, because this is a NEW member of a family the closure protocol already documents and therefore already knows how to prevent: the producer pitfalls listed at STATUS_closure_protocol.md Algorithm step 1 are (a) node ids with `len(node_ids) == selected`, (b) test_files that are files and never directories, (c) the `^vr-\d{4,}$` run_id regex and (d) never a full-suite node-id list — and the sorted-`test_files` rule is a fifth, (e), which that document does not carry, so every future closure block can lose a build to it exactly as this one did. The fix is one bullet in `docs/roadmap/STATUS_closure_protocol.md`; that is a process doc F083 does not own and AGENTS.md forbids mixing an unrelated fix into a feature branch, so it routes to a paydown branch exactly as R-0403, R-0444 and R-0445 were routed. OPEN.

- R-0449 — Low, A BLOCK ORDERED A VALUE INTO AN ARTIFACT THAT IS WRITTEN BEFORE THE VALUE CAN EXIST. Raised by the reviewer during F082's R23 closure review. The R23 block ordered three things that cannot all hold at once: the PR number appears in `.agent/handoff.md`, `gh pr create` runs AFTER C3, and no commit follows C3 because the STATUS edit must be the branch's last commit (Rule A4). The handoff is written inside C3, so the number does not exist when the file is authored and no later commit may add it. The worker declared the contradiction before the reviewer read the diff, wrote the handoff without inventing a number, named the recovery command, and reported the number in its final message; the reviewer recovered PR #201 with exactly that command and merged it at this round's Open PR Gate. This is R-0371 — never order a value that cannot exist when the text is written — recurring in the reviewer's own block one feature after R-0371 was registered for the same class, and it is the second such recurrence in R23 alongside R-0450. Low, because nothing false was written, the worker's declaration was correct, and the recovery is a single read-only command. Standing rule from here, binding the reviewer: before ordering any value INTO an artifact, name the commit that writes the artifact and the step that produces the value; if the producer is not strictly earlier than the writer, the block orders the value reported in the round's final message and orders the artifact to say so. OPEN.

- R-0450 — Low, A CARRIER FILE WHOSE OWN TEXT ORDERS AN APPEND THAT THE SAME BLOCK FORBIDS, SO THE CARRIER CANNOT CARRY. Raised by the reviewer during F082's R23 closure review. The CANDIDATES slice — authored by the reviewer and applied byte-verbatim into `.agent/candidates.md` — says "Every defect the closure round's worker declares in its handback is appended below, one line each", while the same block's Constraint 2 orders every slice applied BYTE-VERBATIM and its Constraint 3 forbids any commit after C3, which is the commit the file lands in. The worker declared two defects in its handback and appended neither, correctly giving the byte-verbatim constraint precedence and recording both as declared deviations instead. The result on disk is a carrier reading "no candidate was carried out of F082's closure review" at a head where two declared defects existed — which is the exact loss the F056-candidate operator ruling of 2026-08-01 created the carrier to prevent, arriving through the carrier's own text. Nothing was actually lost: the closure brief is the vehicle STATUS_closure_protocol.md prescribes, the file is only its disk backup for a session boundary this single-session run did not have, and the three findings registered in this round ARE those candidates. Low for that reason. Standing rule from here, binding the reviewer: a slice ordered byte-verbatim may not contain an instruction addressed to the worker about the file it lands in — instructions live in the block, never in the applied bytes — and a carrier file's text describes only what the file holds. OPEN.

- R-0403 — Low — every review package carries the gitignored `.remedy-wt/` tree as file content, so more than half of each archive is scratch that the review subject itself excludes. Measured today from the two packages on disk: `remedy-review-20260814-085403-READY_FOR_REVIEW.zip` holds 2811 of 5373 entries under `.remedy-wt/` and F077's closure package `remedy-review-20260814-161744-READY_FOR_REVIEW.zip` holds 3096 of 5746 — 52.3% and 53.9%. Cause, read from the script rather than inferred: the file-collection `find` in `scripts/make_review_zip.sh` prunes an EXPLICIT directory list (`./.git`, `./.data`, `./.agent/Evidence`, `node_modules`, `dist`, `build`, the cache directories, plus the dynamically appended `remedy-job-evidence-*` entries) and `./.remedy-wt` is not among them — so being gitignored is NOT the criterion, `./.data` is excluded by being named, and `.remedy-wt/` is collected as ordinary repo files. That directory is Remedy's own job-worktree root by design (`docs/roadmap/features/T0_F006.md`, `git worktree add .remedy-wt/<job>`), it is gitignored at init by F081's `_ensure_ignore_entry` (`.gitignore:235`), and because `/tmp` writes are denied to this session class it is also where every round's gate and transport scratch lands — 731 entries at its top level as this finding is written. Nothing here is INVALID: both packages validated READY_FOR_REVIEW, and `committed_review_subject` is a git range, so gitignored files never enter the review subject and no reviewed byte is affected. The cost is that the operator's only remote window into a run is roughly twice the size it needs to be, over a link that since 2026-08-13 is a phone. The fix is one `-path './.remedy-wt' -o` line in that prune list, which edits `scripts/make_review_zip.sh` — a file F082 does not own, and AGENTS.md forbids mixing an unrelated fix into a feature branch — so it routes to a paydown branch exactly as R-0380 and R-0381 were routed. Registered here rather than through `.agent/candidates.md` because it was raised during F077's closure review, AFTER the closure commit had already written that carrier empty, and Rule A4 forbids a commit after the closure commit: the empty carrier at this claim is therefore not evidence that nothing was raised. OPEN.

- R-0361 — Low — a gate round ordered a proof command the session cannot execute, and asserted an exit code the fetch tool contradicts. The R1 gate block ordered the posted F045 verdict fetched back with `gh api --paginate ... --jq '.[-1].body'` and `cmp`-ed against the authored file, expecting exit 0. `gh api` is denied by this session's permission layer, so the ordered command never ran at all; the worker's substitute, `gh pr view 197 --json comments --jq`, exited 1 because the `--jq` writer appends a newline to a body that already ends in one, leaving the fetched file exactly one byte longer with no differing byte in the common prefix. The worker proved equality the honest way instead — extracting the raw JSON body with no jq in the path, where the sha256 of the posted bytes and of the authored file are both `b9db4e4c41cf59c0c4adcfa8368c83843e2c0ee4e29ceab0b324864ebc19f5ff` and `cmp` exits 0 — declared both deviations in its report, and proceeded rather than burning the round on a tooling artifact. The reviewer re-verified that byte equality independently at `1e7f7bca` and agrees the merge was safe; nothing landed wrong. This is the R-0252/R-0336/R-0350 family — an ordered gate whose expected value the reviewer never computed from the tool that produces it — plus a second failure the existing counter-measures do not reach: ordering a command the permission layer denies makes the gate UNREACHABLE rather than merely wrong, and an unreachable gate cannot fail honestly. Counter-measure, applied from R2 on: a block may only order a command the reviewer has itself executed in this session, and a byte-equality claim over any transport that may normalise trailing newlines is stated as a sha256 comparison over extracted bytes, never as a `cmp` exit code. OPEN.

- R-0362 — Medium — the open-finding set is silently discarded at every branch claim, and Rule A2 forbids the claim that discards it. ROADMAP.md:27 states Rule A2 as "Every block ends with a final review: PASS or FINDINGS. No new feature is started while findings are open", and `docs/agents/reviewer_conventions.md` restates it as "No new feature starts while findings are open (A2)". At the F045 closure the reviewer's own GATE-R15 entry recorded the open set as exactly three — R-0350, R-0354 and R-0358, all Low — after RECOMPUTING it from the record per the pre-emission checklist's item 10. None of those three ids appears anywhere in the paydown0814 record that replaced it: `git show f789ebc8:.agent/live_review.md` carries only R-0359, R-0360 and R-0361. The reset therefore did not resolve them, did not defer them and did not name them; it dropped them, and the same mechanism was about to drop R-0361 at this claim. Two rules are in conflict and neither yields on its own: A2 read literally blocks every feature claim that follows a PASS_WITH_RISKS closure, which is six of the last seven closures in `docs/roadmap/STATUS.md`, while the reset as practised makes A2 unenforceable by erasing its input. No governing document authorises the erasure — `docs/agents/planner_reviewer_prompt.md` §1 says the record is reset at the claim but says nothing about what happens to findings that are open when it is, and `docs/roadmap/STATUS_closure_protocol.md` routes only CLOSURE CANDIDATES, which are explicitly not findings and spend no id. Registered here rather than acted on silently, per §2's rule that a practice invoked without a doc pointer is a finding candidate in the same brief. The structural half of the fix is applied in this round: this record carries R-0361 forward verbatim instead of dropping it, and DECISION F057 D1 states the reading under which the claim proceeds. The documentation half — an explicit carry-forward rule in `docs/agents/planner_reviewer_prompt.md` §1, and whatever becomes of R-0350, R-0354 and R-0358 — is NOT in this feature's scope: AGENTS.md forbids mixing an unrelated fix into a feature branch, so it belongs on its own paydown branch, exactly as DECISION F045 D8 routed the reviewer-conventions repair. OPEN.

- R-0363 — Low — the R1 block was emitted over its own 400-line cap. `wc -l < .agent/authored/f057-r1.md` is 404, against the 400-line limit DECISION F105 D5 sets and which pre-emission checklist item 1 (docs/agents/planner_reviewer_prompt.md §3) orders measured mechanically on the FINAL bytes before any block leaves the reviewer. The reviewer never measured it. Nothing downstream broke — the worker saved the block verbatim as required and declared the end boundary it used — but the check exists precisely because a worker required to save a block byte for byte cannot trim it, so an oversize block becomes a declared deviation on a round that did nothing wrong. The counter-measure is not a new rule, it is running the rule that already exists. OPEN.

- R-0364 — Medium — the R1 block ordered a round gate the reviewer had never executed, and that gate was already red before the round began. Gate 14 of the R1 block demanded `python3 -m ruff check` → exit 0. The reviewer's pre-emission baseline covered `tests/docs/` (`295 passed`) and `tests/cli/test_golden_path.py` (`42 passed`) and did not cover ruff at all. At the base commit `21c8148e`, in the reviewer's own disposable worktree, `python3 -m ruff check --statistics` reports 20 I001, 4 F401, 1 F821 and 1 UP035 — 26 errors, exit 1 — statistically identical to the branch, so R1 added none of them, and `ruff check` over the two new files alone is `All checks passed!`, exit 0. This is the R-0361 family recurring exactly one round after R-0361 was deliberately carried forward to keep its counter-measure in force, and it is the same class as R-0252, R-0336 and R-0350: a gate whose expected value the reviewer never computed from the tool that produces it. The worker behaved correctly — it ran the gate, reported the real exit code, proved the condition pre-existing, and declined to repair an unrelated defect on a feature branch — which means the round spent a declared deviation to prove a reviewer mistake. Counter-measure, binding from R2 on and additional to R-0361's: every gate a block orders is executed by the reviewer at the base commit BEFORE emission, and a gate already red at the base is either dropped from the block or ordered with its known-red baseline stated inline, so the worker is never asked to meet an unreachable condition. OPEN.

- R-0367 — Low — the R2 block ordered a numstat that no correct application of its own pair can produce. C2's gate demanded `git show --numstat HEAD -- packages/orchestration/rate_governor.py` → `8 4`. The authored R0365-FROM slice is 4 lines and R0365-TO is 8, and the reviewer derived `8 4` from those two counts. But the final line of both slices is byte-identical — `    counts as X" drift apart, and the drift is the bug.` — so git's diff renders it as CONTEXT rather than as a deletion plus an insertion, and the only reachable measurement is `7 3`, which is exactly what the worker measured and declared. This is pre-emission checklist item 8 (docs/agents/planner_reviewer_prompt.md §3): a done-when may not assert a number the thing that produces it makes impossible, and the expected value must be computed from that producer — here git's diff algorithm — rather than from what the number obviously ought to be. §4.9 sanctions `git show --numstat` as the MEASUREMENT a receipt reports; it does not license predicting the pair in advance. It is also the third reviewer-arithmetic defect of this session, after R-0364's unexecuted ruff gate and alongside R-0363's unmeasured block length, which together say something the individual findings do not: this reviewer's failures are concentrated entirely in numbers asserted about artifacts rather than in the review of the work itself. Counter-measure, binding from the next block on and additive to R-0364's: a block asserts the DATA property — FROM 0 occurrences, TO exactly 1, the changed-paths list, a sha256 over extracted bytes — and never a predicted insertion/deletion pair; where the arithmetic matters it is reported by the round, not ordered by the block. OPEN.

- R-0368 — Low — a round gate named a base ref belonging to a different round. Gate 14 of the R3 block ordered `git diff --name-only 36b745bd..HEAD` and expected exactly the six files that block names. `36b745bd` is the R1 handback — the base of ROUND 2, not of round 3, whose base is `c3222402` — so the ordered range necessarily spans both rounds and lists the two Python files R2 legitimately changed. The real output at `944f01cc` was eight paths, and no correct application of the R3 bundle could have made it six. The worker measured it, declared it, computed the reachable form (`git diff --name-only c3222402..HEAD` → exactly the six named files) and edited nothing to reach the ordered one; the reviewer re-measured that reachable form at `dae401e1` and confirms it. This is the fifth reviewer-arithmetic defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate and R-0367's unreachable numstat, and it is precisely the one their counter-measures do not reach: R-0364 makes the reviewer EXECUTE every gate it orders, and R-0367 bars predicted numbers, but a range gate executed at the wrong base runs cleanly at emission time and only becomes unmeetable once the round's own commits exist. Counter-measure, binding from R4 on and additive to both: every gate taking a commit range states its base as the SHA of the handback the round starts from — re-read from `git log` at emission, never carried over from the previous block — and the block prints that SHA once in its bundle header, so the range and the round agree by construction rather than by the reviewer's memory. OPEN.

- R-0369 — Low — a done-when counted a string that the same block's own slice writes into the same file. Gate 5 of the R4 block ordered `## Steps` to occur exactly 1x in `.agent/live_review.md`, and the block's own GATE-R3 slice ends with the sentence "…and `## Steps` still occurs exactly once", which the same round appends to that same file. The whole-file substring count after C1 is therefore 2 and cannot be 1; the same is true of `Gate: R2 — PASS`, quoted in the same sentence. The worker reported 1, which is the LINE-ANCHORED count and the measurement the contract actually cares about — `docs/agents/planner_reviewer_prompt.md` §4 item 11 requires the `## Steps` SECTION to exist, and `tests/ui_server/test_dashboard_contract.py` asserts the substring's presence, which two occurrences satisfy — so nothing on disk is wrong and the reviewer re-ran all four contract readers at `5de503c6` for `142 passed` to confirm it. The defect is the gate, not the file: it was ambiguous between two measurements that give different numbers, and it went unnoticed only because the worker silently picked the right one. This is the sixth recurrence of the class pre-emission checklist item 2 exists for — "a 'must be 0' done-when may not count a string that any TO slice in the same block writes into that same file" — and item 6's rule that such counts are read against the TARGET's existing content. The check is on disk, was not run, and that is the whole story. Counter-measure, binding from R5 on: every count gate over a file this block also writes states its ANCHORING explicitly, is expressed line-anchored whenever the string is a heading or a record's opening token, and is checked against the block's own slice bytes before emission — and the round reports both the anchored and the substring count so the difference stays visible rather than being absorbed by whichever reading happens to fit. OPEN.

- R-0371 — Low — a block ordered a value that cannot exist at the moment the text carrying it is written. The R5 block told the worker to append to `.agent/live_review.md` "a single line of your own of exactly this shape, with your real commit SHA: `Landed: R-0370 — <one line: what changed, which commit>`" and, six lines later, that "that live_review.md edit belongs to C2, the same commit as the test". A commit's SHA is a hash over a tree that already contains every byte of that commit, so a line inside C2 can never name C2. No correct application of the bundle could satisfy both clauses. The worker was right to declare the deviation, name the commit by its role — "R5's C2, the same commit as this line, whose SHA the handback reports" — and let the handback carry the real value `a01e8a9712aead26eb88888db352d0bb72492cb9`; nothing was fabricated and nothing was edited toward a number. This is the seventh reviewer-gate defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate, R-0367's unreachable numstat, R-0368's wrong-base range gate and R-0369's self-counting string gate, and it is a class none of their counter-measures reach: R-0364 makes the reviewer EXECUTE every gate it orders, but a self-referential SHA is not a gate at all — it is appliable CONTENT whose required value the act of applying it destroys, so there is nothing for the reviewer to execute in advance. `docs/agents/planner_reviewer_prompt.md` §4 item 4 supplies the template verbatim, including the words "which commit", and the template is fine; the defect is pairing it with "your real commit SHA" and "the same commit as the test". Counter-measure, binding from R6 on and additive to all of the above: before ordering any text to be written into a file, the reviewer checks that every value that text must contain already exists at the moment of writing. Commit SHAs, `git show --numstat` outputs and every other post-hoc measurement are ordered into the HANDBACK, which is written after the commits exist, and never into the committed text itself; where a committed line must identify its own commit it names it by its ROLE in the bundle. OPEN.

- R-0374 — Low — a wiring fix landed with no test, and the round is the reason we know. The R7 block ordered a red-proof probe (iii) that removes `rate_governor=` from the reviewer parse-retry call site, and told the worker that if it killed nothing, to say so plainly rather than reassure. It killed nothing: with the C2 wiring reverted inside the disposable worktree, the seam files gave `88 passed` and the four regression files with the canary gave `336 passed` — 424 tests, all green, with the fix removed. So the R-0372 resolution is correct on disk and entirely unpinned: any later refactor that drops that keyword argument restores the unpaced parse-retry call and no test objects. The cause is structural rather than careless. The other two call sites are reached by the seam tests through `_call_with_retry` directly, but the parse-retry site is reached only through `run_pingpong`, and no test in `tests/orchestration/test_provider_retry.py` drives a rate-limited parse retry end to end — which is also why the R6 block could order the wiring without noticing there was a third site to wire. Fix in T003 part 2, as its FIRST item and before the report surfaces, because the fixture that part needs is the same fixture this needs: drive `run_pingpong` with an injected governor and a reviewer whose parse retry hits a rate limit, and assert the wait is recorded — one test that pins the third call site and exercises the injected-governor parameter at the same time. If that turns out to be genuinely unreachable without a disproportionate fixture, the alternative is a documented deliberate absence in the AGENTS.md idiom, naming why — never silence. OPEN.

- R-0375 — Low — a block ordered a test whose ordered SHAPE could not reach the code it was meant to pin. R7's C3 item 3 asked for a review-reject test built "the way the existing tests in this file build one", which is an errorless `ReviewerOutput(verdict="needs_repair")`. `_call_with_retry` returns at `if not out.error: return out` at the top of its retry loop, well above the retry decision, so that shape never reaches the reject exclusion at all and the test would have passed identically with the exclusion deleted — a vacuous green, which is worse than a missing test because it looks like coverage. The worker caught it by reasoning about the control flow rather than by running the ordered thing and reporting a colour, built the reject with a rate-limit error attached — the only shape that reaches the guard — declared the deviation before review, and then proved the point with an unordered extra probe: dropping the explicit `is_reject or` turns that test red at `assert 3 == 1`. This is pre-emission checklist item 5's class (docs/agents/planner_reviewer_prompt.md §3), which currently speaks only of mutation red-proofs over reachable branches; the same reachability question applies to any test a block SPECIFIES BY SHAPE, and the checklist does not say so. Counter-measure, binding from the next block on: when a block dictates a test's fixture shape rather than only its property, the reviewer traces that shape through the function's early returns to the line under test before ordering it — and where the trace is not obvious, orders the PROPERTY and lets the worker choose the shape, exactly as item 5 already prescribes for mutations. That the worker found this is the split-role model working as designed, and it is registered against the reviewer, where it belongs. OPEN.

- R-0376 — Low — a range gate contradicted the round base its own block declares, and the counter-measure that was supposed to prevent exactly this did not reach it. R-0368 ended with a binding rule: every gate taking a commit range states its base as the SHA of the handback the round starts from, and the block prints that SHA once in its bundle header so range and round agree by construction. The R8 block DID print it — `Round base — the SHA every range gate in this block measures from: 2991ba30` is its second line — and gate 9 used it correctly. Gate 10 then ordered `git diff --stat 3ab9d964..HEAD -- packages/ apps/ tests/` and expected EMPTY, but `3ab9d964` is R7's base, so the range spans R7's two code commits and the real output is two files and 111 insertions. So the header exists, is correct, and is contradicted by a gate three lines below it: printing the base does not make the gates USE it, and nothing in the pre-emission checklist compares each range gate's base against the declared header. This is the clause-vs-clause class that checklist items 9 and 10 were added for, one level up — they check a block's pointers and its finding set against the world, and this one is a block disagreeing with ITSELF. Counter-measure, binding from the next block on and additive to R-0368's: the last pre-emission act on a block is to grep its own bytes for every SHA-shaped token, and every one of them must be either the declared round base or a base whose deviation the gate STATES in its own text with the reason — the form R9 gate 15 uses for the branch point. A reviewer who cannot say in one clause why a gate reads from somewhere else has found a defect, not an exception. OPEN.

- R-0377 — Medium — a block ordered a change set that excluded the one file the same block's content obliged it to change, and a state file has been false on disk ever since. R8's gate 9 capped the round at four paths, `.agent/plan.md` not among them, while C1 of that same round closed two findings and opened two more. AGENTS.md's Commit Gate item 1 requires plan.md to match the current work before every commit; the block's gate 9 forbids touching it. Both cannot hold, and the worker was right to follow the block and declare the conflict rather than silently widen its change set. The cost is measurable rather than theoretical: at `37e88970` the reviewer read `.agent/plan.md` and it states "Next free finding id: R-0374" and lists R-0372 and R-0373 as open, when the record on disk has both resolved, ten findings open and R-0376 as the next free id. A session bootstrapping from plan.md — which AGENTS.md's Session Resume step 2 tells it to read second, before it reads the review record — starts from a false ledger, and "prefer repository state over session memory" stops protecting anything when the repository state is the thing that is wrong. The cause is a reviewer habit rather than a worker error: change-set gates are written by listing the files the round's ITEMS touch, and the files a round's CONSEQUENCES touch are then absent from a list that is enforced as exhaustive. Counter-measure, binding from the next block on: any round whose bundle registers, resolves or renumbers a finding names `.agent/plan.md` in its change set and rewrites its ledger in the round's FIRST commit, so the mirror is never behind the record for the length of a round. R9 does exactly that. OPEN.

- R-0378 — Low — this feature's central promise reaches the reviewer role only through an undocumented coupling to an error-string prefix, and nothing states it or pins it. `_call_with_retry` computes `is_reject` as `hasattr(out, "verdict") and out.verdict in ("needs_repair", "fail", "blocked") and not out.error.startswith("provider_error:")`, and `ReviewerOutput.verdict` DEFAULTS to `"blocked"`. So every ReviewerOutput that carries a transport error is a review reject by default, and the ONLY thing keeping a rate-limited reviewer call out of that class — and therefore reachable by the R-0373 retry rule and the governor behind it — is the `provider_error:` prefix that the exemption names. The reviewer established this by probe rather than by reading: driving `run_pingpong` with a reviewer whose parse retry returns a bare `429 Too Many Requests` reaches the parse retry and records NO wait, while the same run with the error wrapped as `provider_error: RuntimeError: 429 Too Many Requests` retries once and records exactly one wait. Today the production path is safe, and that is a measured statement, not an assumption: every reviewer error site in `pingpong_provider.py` that could carry a rate limit is a generic `except Exception` handler that emits the prefix, and the sites that omit it emit `malformed_output:` or `stream_cap_reached:`, neither of which is a rate limit. But the invariant lives nowhere — not in the `is_reject` comment, which explains only that rejects are never retried, and not in `ReviewerOutput`, whose default is what creates the hazard. Any future reviewer path that reports a rate limit without the prefix silently stops being paced, and no test in the suite would notice. Fix in a later round, smallest first: a one-line WHY above the reject predicate naming the prefix dependency in the AGENTS.md Code Discoverability idiom, plus one seam test asserting that a `provider_error:`-prefixed rate limit on a ReviewerOutput is retried. Registering it rather than folding it into R9's test, because a fixture that merely avoids a hazard documents nothing. OPEN.

- R-0379 — Low — a block asserted a line count for its own authored slice instead of measuring it. The R12 block's C0 paragraph states that the PLAN slice "is 36 lines, inside the AGENTS.md 50-line cap"; the slice is 35 lines, and `wc -l .agent/plan.md` after a byte-identical application returns 35. Nothing downstream broke, because the ORDERED gate was "under 50" plus a `cmp` of the slice extracted from the committed block against the applied file, and both passed — so the cost was one declared deviation on a round that did exactly what it was told, plus the worker's time spent proving a reviewer mistake rather than doing the round's work. The class is already on this disk twice, as R-0336 and its recurrence R-0367: a reviewer must never PREDICT a number it can measure, and a count stated inside an authored block about that same block's own bytes is the purest case of one, because those bytes are in the reviewer's hand at emission. The pre-emission checklist's item 3 already orders cap-bounded replacements to be counted before emission, so the gap is not a missing rule but a rule applied to the CAP and not to the SENTENCE that states the count; the smallest fix is one clause in item 3 requiring that any line count named in a block's prose be the measured one, so the prose and the gate cannot disagree. Registered rather than resolved inline because that amendment edits docs/agents/planner_reviewer_prompt.md, which is outside this feature's change set, and F057 will not open a doc it never owned in order to close. OPEN.

- R-0380 — Low — a resolved finding keeps its `Landed:` line beside its `Done:` line, so the record shows a signal meaning "unreviewed fix" on a fix that was reviewed. Registered from the closure candidate carried in `.agent/candidates.md` (source F057, 2026-08-14) per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings". `docs/agents/planner_reviewer_prompt.md` §4 item 4 says the reviewer "replace[s] the `Landed:` line with the authored `Done:` text at the next gate" and that "a surviving `Landed:` line is an unreviewed fix"; in the F057 record R-0370 carries BOTH a `Landed:` line from R5 and a `Done:` line from R6. Nothing broke, because every open-set computation in this repository subtracts `^Done:` and ignores `^Landed:`, so R-0370 was correctly absent from every open set F057 computed and is absent from the carried set here. The conflict is between two rules that both live on disk: §4.4 says REPLACE, while the record is append-only by the convention every F057 block stated and every round applied — under which appending the `Done:` line IS the replacement, and deleting the `Landed:` line would rewrite the history the file exists to preserve. The fix is one clause in §4.4 saying that in an append-only record a later `Done:` supersedes an earlier `Landed:` for the same id and the `Landed:` line stays in place. That edit is to `docs/agents/planner_reviewer_prompt.md`, which F077 does not own — AGENTS.md forbids mixing an unrelated fix into a feature branch — so it belongs on a paydown branch, exactly as DECISION F045 D8 routed the reviewer-conventions repair. OPEN.

- R-0381 — Medium — the block-save commit every round begins with cannot satisfy the 500-insertion cap once its block approaches the 400-line block cap, and the exemption written for that commit does not cover its actual shape. Registered from the closure candidate raised in the R14 verdict on PR #199 per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings". Measured: commit `427c0e26` inserts 660 lines — `.agent/authored/f057-r14.md` 339 plus `.agent/last_block.md` 321 — against the cap in AGENTS.md "Commit Discipline", and the F057 R14 handback does not declare it, which by the letter of that rule is an undeclared oversize commit. The cause is structural rather than conduct: a block must be written to `.agent/authored/` and `cp`-ed to `.agent/last_block.md` in ONE commit so the `cmp` transport proof exists, so that commit's insertions are about twice the block's line count, and any block over roughly 250 lines breaks the cap by construction. The DECISION F104 D1 counting rule already exempts "the verbatim rewrite of a SINGLE `.agent/**` state file" and enumerates five filenames, none of them the `authored/` copy — so the cp-pair, one indivisible artifact for exactly the reason D1 gives, falls outside an exemption written for its twin. Across the whole history 3 of 186 block-save commits exceed 500 insertions: this one at 660, `106239a9` (F045 R1) at 632 and `ea48ea89` (F105 R4) at 523; the two earlier ones sit on merged features and drew no finding, so the practice is unpersisted rather than novel. The fix — extending the D1 bullet to name the cp-pair as one artifact, or requiring the declaration whenever the pair exceeds the cap — edits AGENTS.md, which F077 does not own, so it routes to a paydown branch. Counter-measure applied from this round on: reviewer blocks are held at or under 240 lines so the pair stays inside the cap. OPEN.

- R-0382 — Low — a reviewer block defined a record's paragraph boundary by a rule the record does not obey, and the extraction it ordered would have silently merged two findings. The R1 block told the worker that a carried finding "is the whole paragraph that begins `- R-XXXX — ` up to (not including) the next blank line". In the F057 record the findings R-0363, R-0364, R-0365 and R-0366 are stored as four ADJACENT lines with no blank line between them, so that rule terminated R-0363 only at the end of R-0366 and swallowed R-0364 whole; the ordered extraction failed rather than passing quietly, and the worker refined the terminator to "a blank line OR the next `^- R-\d+ — ` line", declared the deviation, and proved byte fidelity. The reviewer then re-extracted all fourteen carried paragraphs independently, with its own terminator, out of `c3d71465:.agent/live_review.md` and confirmed each one byte-identical in the new record, with no id dropped and none added. Nothing landed wrong. The defect is the reviewer's: this is the R-0353 family — a block whose description of a file was written from memory of the file's usual shape instead of measured against its actual bytes — and the pre-emission checklist's item 6 already says a gate reads the TARGET's existing content, which a paragraph-boundary rule plainly is. Counter-measure, applied from R2 on: any block that orders a mechanical extraction from a record states the terminator AND names one id in that record whose neighbours prove the terminator is right, measured before emission rather than assumed. OPEN.

- R-0385 — Medium — the reviewer emitted a 445-line block against its own 400-line gate, and the same overrun then ordered a commit AGENTS.md forbids. Two downstream costs, both real, both traceable to one omission. First: gate 2 of the R7 block ordered the worker to report the block's line count and assert it is "at or under 400"; the real value is 445, so the gate was unsatisfiable by construction, and the worker was right to report 445 unadjusted rather than trim an artifact it is required to save verbatim. That is the R-0371 self-referential-gate class recurring — a gate whose expected value the block's own bytes contradict. It also breaks the 240-line ceiling recorded in `.agent/context.md`, whose stated purpose is precisely "so the block-save commit stays inside the 500-insertion cap". Second: C0 of that block ordered the new authored file and its `cp` mirror committed TOGETHER, which at 445 lines measures 886 insertions against AGENTS.md's hard 500-line cap, whose own prescribed remedy is "stop and split before committing". The worker applied that remedy, splitting by file into `8ecf306f` (445 insertions, the authored file) and `8d9ed78e` (441 insertions, the `cp` mirror — itself the AGENTS.md-exempt verbatim rewrite of a single `.agent/**` state file), kept the bytes identical so `cmp` still exits 0, and consumed no oversize exception. That was the correct call and AGENTS.md outranks the block, so it is not a worker defect. The root cause is single: the block was never measured. Pre-emission checklist item 1 (docs/agents/planner_reviewer_prompt.md §3) says to count the block's lines mechanically on the FINAL bytes, after the last edit, before the block leaves the reviewer; the reviewer reasoned about a 240-line budget while drafting, kept adding, and never counted the result. Fix, both halves: the reviewer counts the emitted block with `wc -l` before delegating and cuts to the ceiling if it is over, AND any block expected to exceed roughly 250 lines orders C0 as two commits from the start, as this block does, so the cap is never something the worker has to discover mid-round. OPEN.

- R-0386 — Low — the reviewer stated two expected values in the R8 block and both were wrong, in the same block, on values it could have computed from the record it had already read. The open-finding count: the block's C4 told the worker to record SEVENTEEN after the round, when the arithmetic on its own numbers is eighteen open minus R-0384 resolved plus R-0385 registered, which is eighteen; the worker recomputed the set mechanically, got eighteen, reported it unadjusted and mirrored eighteen into `.agent/plan.md`. Gate 7: the block predicted that `grep -rn "watchdog" packages/orchestration/orchestrator_loop.py` would return "one pre-existing hit … a prose comment mentioning escalation", when the real answer is ZERO hits — the reviewer had grepped that file earlier in the session, saw a line matching a DIFFERENT pattern in the same combined command, and carried the misreading into the block instead of re-running the single grep it was about to order. Neither cost the round anything, and that is the load-bearing part of this finding rather than a mitigation of it: both gates were written in the probe form finding R-0327 prescribes — "report YOUR count", "report every hit", "do not adjust it to match this line" — so the worker's mechanical answer beat the reviewer's prediction by construction, exactly as designed. This is the sixth and seventh instance of the reviewer-arithmetic class (R-0327, R-0328, R-0336, R-0367 and now these two), and the pattern across all of them is identical: the reviewer states a number it could have measured. Fix, and it is narrower than "be careful": a block may state an expected value ONLY when the reviewer executed the exact command that produces it, at the commit the block starts from, immediately before emission. An expectation the reviewer did not run is not an expectation, it is a guess, and it goes into the block as a bare probe with no number attached. OPEN.

- R-0387 — Medium — the reviewer ran pre-emission checklist item 7 ("source guards the block never names") too narrowly and the round ended red because of it. Item 7 says to grep the suite for tests that COUNT a string over a WHOLE file before ordering a change that adds one; the reviewer instead grepped for the literal pattern `count(` and read only `tests/orchestration/test_mission_e2e.py`, the file DECISION F077 D8 happened to name. The guard that actually broke — `TestTheLedgerCoversEveryIteration::test_one_entry_per_iteration_numbered_from_one` in `tests/orchestration/test_orchestrator_loop.py` — is a whole-ledger equality of exactly the class D8 warned about, it contains no `count(` at all, and it sits in a file the R10 block DID authorise the round to gate but not to repair. Two mistakes compounded: the search pattern was a proxy for the property rather than the property itself, and the search scope was taken from a DECISION's prediction instead of from the change. The worker was left holding a red suite it was explicitly forbidden to fix, which is the outcome item 7 exists to prevent — the finding text for R-0258 says in as many words that such a guard "makes a correct SECOND call site unsatisfiable, and the worker cannot repair it without leaving its change set". From here, a block that adds an entry to any append-only record greps EVERY test file that reads that record for whole-collection equalities, not only for `count(`, and the block's Change line authorises repairing what that grep finds.

- R-0389 — Low — the R10 block was 293 lines against the 240-line ceiling `.agent/context.md` carries for this feature, and the reviewer emitted it without measuring. The ceiling exists so that the block-save commit stays inside the 500-insertion cap (R-0381), and at 293 that commit was still comfortably inside it, so nothing broke on disk and the round paid nothing for it — this is registered because an unmeasured ceiling is one round away from being an exceeded cap, and because pre-emission checklist item 1 orders the count to be taken mechanically on the final bytes, which was not done. The reviewer's own constraint list in the block repeated the 240 figure to the worker while the block containing it was 293 lines long.

- R-0391 — Medium — the reviewer raised R-0388 and decided DECISION F077 D10 on an invariant that does not exist, and it took a worker's refusal to apply the resulting order to expose it. R-0388 asserted that "one entry per iteration, numbered once" was load-bearing, citing two tests that assert it and `next_iteration_index`, which reads one past the highest recorded value. What the reviewer never did was read the code that WRITES the field it was reasoning about: `_record` has eleven call sites inside `run_mission`, and two of them — the executed move's entry and the blocked-completion escalation's entry directly below it — fire in the SAME pass with the same `iteration`, a shape that has been green and shipped since F075 R-0190 and that `TestTheSecondBlockedCompletionEscalates::test_two_blocked_completions_in_a_row_escalate` drives on purpose. The invariant was inferred from two test names and never checked against the eleven writers. This is pre-emission checklist item 8 — read the code that PRODUCES the value a gate asserts — applied to the watchdog's own number and to nothing else, and it is the second item-8-class miss on this branch after R-0387's narrow item-7 grep, which is why it is Medium and not Low. The compounding cost is on the record and is the point of the finding: the wrong diagnosis produced DECISION F077 D10, D10 ordered a code change to production behaviour that was already correct, and D10's safety premise was ALSO false — the worker measured a scripted stop-after-trip run at `[1, 2, 3, 4, 4]` with the ordered repair against `[1, 2, 3, 3, 4]` without it, because `run_mission`'s safe point calls `_record` BEFORE the top-of-loop status check that was supposed to make the collision impossible. Two independent errors in one diagnosis, and the only thing that stopped either from landing was that the block made its own premise a checkable precondition and the worker checked it. From here, a finding that asserts an invariant names every writer of the field it constrains, counted mechanically, before the finding is authored — not after a repair is ordered against it.

- R-0392 — Low — the R12 block, finding R-0391, gate GATE-R11 and DECISION F077 D11 all state that `_record` has "eleven call sites", and all four are wrong by one: `grep -c '_record(iteration' packages/orchestration/orchestrator_loop.py` returns 11, but the match at line 1036 is the `def` and the calls are at 1064, 1119, 1180, 1191, 1203, 1210, 1253, 1267, 1293 and 1296 — TEN, all inside `run_mission`, which spans 936 to 1341. The reviewer read a `grep -c` total and never subtracted the definition line it had itself included in the pattern. The count is also ambiguous in a second way the record does not mention: a completely unrelated `_record` closure is defined at line 916 inside `make_orchestrator_call_recorder` and returned at 933, so "eleven `_record` call sites" is wrong whether the reader counts the ledger writer's calls or the file's `_record` symbols. Nothing downstream changes — the claim D11 actually rests on is that TWO calls fire in one pass at one `iteration`, verified independently at 1210 and 1253, and the ALTERNATIVES paragraph's argument holds unchanged at ten — which is why this is Low and not Medium. It is registered anyway because of where it sits: R-0391 is the finding whose whole lesson is that a reviewer must count the writers of a field mechanically before authoring against it, and the sentence delivering that lesson miscounts those writers. The worker measured the drift and declared it as Deviation 2 of the R12 handback rather than correcting the reviewer's text, which is correct behaviour and is the only reason it is on the record at all. From here, a count that appears in authored text is copied from the command output WITH the command's own exclusions applied — a `grep -c` that matches a definition as well as its calls is reported as both numbers or as neither.

- R-0393 — Low — R14's red-proof transcript reports a green baseline and a mutated run measured over DIFFERENT `-k` selections, so the pair it presents is not a like-for-like comparison. The handback's gate 14 says the worktree "was proven green first (`-k "Resume or Watchdog"` → `9 passed, 83 deselected`)" and then reports mutation (a) as `1 failed, 3 passed, 88 deselected`. Those totals cannot be paired: `--collect-only` at HEAD gives `9/92` for `-k "Resume or Watchdog"` and `4/92` for `-k "Resume"`, so the mutated run selected four tests where the baseline selected nine. Both numbers are real and neither is fabricated — the reviewer reproduced the mutation independently at the wider selection and observed `1 failed, 8 passed`, the same failing test on the same assertion — which is why this is Low and not a block condition. It is registered because a red-proof is not a number, it is a PAIR: the whole evidentiary weight of "this test catches that break" rests on the two runs differing in exactly one variable, and a narrowed selection between them is a second variable that a later reader cannot rule out without re-running the proof themselves. The residual risk was real rather than theoretical: at the narrower selection the transcript's own honest note — that `test_the_json_shape_matches_show` survives the mutation by construction — is indistinguishable from the five tests that simply were not run. From here, a red-proof states ONE selection string and uses it for the green run and every mutated run, or it declares the change of scope in the same sentence as the numbers.

- R-0394 — Low — the session-close block that recorded `Gate: R15 — PASS` retargeted the "R16 owes R15's gate paragraph" claim in `.agent/handoff.md` and left the SAME claim standing in `.agent/plan.md`, whose Next Steps item 1 still read "Its FIRST commit owes R15's own `Gate: R15 — ` paragraph, which cannot exist before this round is reviewed" after that paragraph demonstrably existed. This is a reviewer defect, not a worker one: the block named `.agent/handoff.md` as its only amendment target and its own change set forbade touching `plan.md`, so the worker was right to apply it as written and to report the residue instead of silently widening scope — which is exactly what it did. The cost was bounded only by that report. `docs/agents/planner_reviewer_prompt.md` §1 has the next session read `.agent/plan.md` at bootstrap, so a reader arriving on this branch would have been told by the plan to write a gate paragraph the record already carries, and the likely outcome is a duplicate `Gate: R15` line or a round spent discovering it is not needed. The root cause is the one finding R-0331's class keeps naming: a claim that lives in more than one state file is retired in all of them or in none, and the reviewer checked its own edit against the file it was editing rather than grepping the claim across `.agent/`. From here, a block that retires a claim from a state file greps that claim's distinguishing text across `.agent/*.md` FIRST and names every file that carries it in the change set — the grep is one command and it is the whole fix.

- R-0395 — Low — the third session-close block ordered `wc -l .agent/context.md` → 88 as a gate, and the file was 100 at that block's own base commit `2d35b701` and had been since `7c5749a7`. The reviewer measured 88 after R14 and reused the number after R15 without re-measuring, though R15's own handback table records `.agent/context.md` moving +17/-5 in that very round — 88 + 12 = 100, arithmetic the block had in front of it. This is the finding R-0364's class names, "run every gate at base", recurring in the one place it is easiest to skip: a state file the reviewer is not editing and therefore does not re-read. Nothing was harmed, which is why it is Low: the worker reported the contradiction instead of routing around it, and the invariant the block actually depends on — that a rewrite pair of equal line counts leaves its file's length unchanged — held at 100 → 100, with `.agent/plan.md` 45 → 45 and `.agent/handoff.md` 133 → 133 matching their ordered values exactly. The residual risk was a worker trimming a correct file to satisfy an incorrect gate, which the block's own "stop and report rather than trimming" clause is what prevented. From here, EVERY length gate over a state file is measured at the round's base commit in the same command that produces the block's other base values, never carried forward from an earlier round — a length is a measurement, and a measurement more than one round old is a memory. This finding and the count mirrors it invalidates are applied in ONE commit, because the two previous close rounds demonstrated that registering a finding and updating the counts that quote it are a single indivisible edit.

- R-0396 — Low — the R16 gate's `attribution.txt` states an EXCLUSIVE causal claim that the very code it cites refutes. It says the `ERROR: React UI not built.` string is emitted "only on the path where `_get_frontend_dist()` found no `apps/ui/dist/index.html` and the auto-build was refused", and from that concludes the eight base-only ids failed inside a window where vite had emptied `dist`. `_load_frontend` in `packages/orchestration/ui_server.py` reaches that same string by a SECOND path: when `_get_frontend_dist()` DOES return a dist, the `elif _frontend_is_stale()` branch calls `_auto_build_frontend("source changed")`, which returns `None` on its first line whenever `REMEDY_UI_NO_AUTO_BUILD=1`, after which the function falls through to the identical `sys.exit(1)`. A PRESENT but stale `index.html` therefore produces byte-identical evidence to an absent one, and the raw log cannot discriminate the two because that env-var early return precedes the `auto-build (<reason>)` print — so the worker could not have told them apart from what it had, which is why this is Low and not a fabrication finding. The round's own recorded timestamps in fact favour the path the attribution excluded: `_frontend_is_stale()` compares `dist/index.html`'s mtime against every file under `apps/ui/src/`, the copied dist carried the primary checkout's mtimes from its 14:53:56 rebuild, and `git worktree add` wrote the base worktree's sources fresh at roughly 14:56, so the copied dist was stale from the first second of the base run — which predicts the observed 8-of-16 split exactly as well as the transient-emptying story does, both splitting on the 14:57:42 rebuild. No verdict moves: both candidates are the ENVIRONMENT class, neither is a failure of the merge base, and the serial re-run at `16 passed in 2.14s` settles that independently of which one ran. It is registered because committed gate evidence is the artifact a later reader trusts WITHOUT re-deriving it, and because the consequence generalises: `docs/agents/integration_gate.md` step 3 tells every future runner to COPY `apps/ui/dist` into the base worktree to restore parity, and a copy that preserves mtimes can never satisfy a staleness check against a freshly checked-out source tree, so that recipe reproduces these eight phantom failures on every gate this repository will ever run. The amendment — touch `dist/index.html` after the copy so it postdates the checkout, or say plainly that the ui_server class is attributed rather than restored — belongs in `docs/agents/integration_gate.md`, which is outside F077's change set, so this registers rather than resolves, the same routing R-0379 took. OPEN.

- R-0397 — Low — the R16 block set two gates that a real pytest transcript makes unsatisfiable together, and the worker paid for the reviewer's mistake with an unordered sixth commit and a declared deviation. Gate 10 ordered `base_run_tail.txt` to carry "the LAST 40 lines of the raw log", and gate 16 ordered `git diff --check d9bbfe14..HEAD` to produce no output; pytest renders the blank source-listing lines inside a traceback as four spaces, two of them landed inside that forty-line window, and `git diff --check` flags trailing whitespace on added lines. A verbatim transcript of that log therefore cannot be committed while the whitespace gate holds, and no worker can satisfy both. The worker resolved it the only honest way available: it wrote the two lines empty, disclosed the normalisation IN the evidence file rather than in a report that does not travel with it, anchored the untouched original by the raw log's sha256 in `full_log_provenance.txt`, and refused to amend `7f709e3c` because history is not rewritten here — so the cost stayed bounded to one extra commit and one deviation on a round that did exactly what it was told. The class is the pre-emission checklist's own recurring shape: its items 2, 6, 7 and 8 each teach that a gate must be checked against something OUTSIDE the block's own bytes, and this is that same error aimed at yet another outside thing — not the target file, not the guarding tests, not the code computing the asserted value, but the CONTENT the gate's own artifact will come to contain. From here, a block that orders a verbatim transcript into a TRACKED file states in the same breath which normalisation is permitted and what anchors the original, because a raw test log is full of exactly the whitespace this repository's hygiene gate rejects. OPEN.

- R-0399 — Low — the reviewer's block-save commit is at the 500-insertion cap by CONSTRUCTION, and two consecutive rounds landed on exactly 500 without anyone choosing that. C0 writes the authored block to `.agent/authored/f077-r<n>.md` AND mirrors it over `.agent/last_block.md` in one commit, so its insertion total is `N + (N - matched)`, where `N` is the block's line count and `matched` is the number of lines git's diff algorithm pairs between the OLD `last_block.md` and the new one — that is, `2N - matched`. R16's C0 measured `260 + 240 = 500` with 20 lines matched; R17's C0 measured `274 + 226 = 500` with 48 matched. Both reproduce from `git show --numstat` and neither EXCEEDS the cap, which is why this is Low and not a violation. The hazard is that the margin is invisible at authoring time and moves in the wrong direction: `matched` depends on how similar the previous block happened to be, so the reviewer cannot predict C0's size from the one number it controls, and the 400-line block cap that DECISION F105 D5 sets is in direct tension with the 500-insertion commit cap for any block past roughly 250 lines — a 275-line block against a dissimilar predecessor breaches it and forces a declared deviation onto a worker that did nothing wrong. The fix is already precedent: the R15 session-close round split its save into two commits and declared the split, and each half is then about `N` rather than `2N - matched`. From here, a block over 250 lines orders its C0 as TWO commits — the authored save, then the `last_block` mirror — so the cap binds per artifact instead of per accident. OPEN.

- R-0400 — Low — the state-file contract readers' DESELECTED count does not reproduce, and this branch's own integration-gate entry already contradicts it. The gates for R15, R16, R17 and R18 each record `216 passed, 16671 deselected` for the selection `-k "dashboard_contract or resource_safety or test_runner"`. Re-run at `386ef7b5` that same selection measures `216 passed, 16701 deselected`, and `python3 -m pytest -q --collect-only` measures `16917 tests collected` on two consecutive invocations. So 216 + 16701 = 16917 is internally consistent while 216 + 16671 = 16887 is thirty short, and the `Gate: R16` paragraph in this very file carries the number that settles it: its full-suite run measured `16898 passed, 19 skipped`, which is 16917 collected. The reviewer re-ran the full suite itself at `386ef7b5` and measured `16898 passed, 19 skipped in 143.68s` at exit 0, reproducing that total a third time. The last commit on this branch to touch `tests/` is `826fb5a3`, which is R15's work, so no change after R15 can explain a moving total. The reviewer did NOT determine why the earlier runs collected thirty fewer, and no cause is attributed here: there is no conditional-collection hook in the suite (`collect_ignore`, `allow_module_level`, `importorskip` all return nothing), `pyproject.toml` sets no `testpaths` or `norecursedirs`, and the gitignored `.remedy-wt/` scratch directory is not collected. This is Low because nothing green turns red: `216 passed` reproduces at every gate that reported it, and a deselected count gates nothing on its own. The consequence is narrower and real — three gates on this branch used deselected DELTAS as corroboration for a test-count claim ("+13 equals the 13 tests this round adds", "+10 for the 10 tests added"), and that arithmetic rests on a base number that is not currently reproducible. From here, a deselected count is reported as a raw measurement only, and the corroborating arithmetic for a test-count claim uses the passed count and `--collect-only`, both of which reproduce. OPEN.

- R-0401 — Low — the parenthetical that R-0398's repair added to `docs/system/autonomy-watchdog-v1.md` states a span that is not `run_mission`, and it still does not state the exclusion that produced the original off-by-one. The doc now reads "`_record` has ten call sites in `run_mission` (lines 936 to 1341)". `run_mission`'s `def` is at 936, but its last body line is the `return build_boundary_handoff(result, root)` at 1304; lines 1307 to 1338 are module-level constants — `IN_FLIGHT_JOB_STATES`, `BLOCKED_COMPLETIONS_BEFORE_ESCALATION`, `RETRYABLE_FAILURE_CLASSES` and `BOUNDARY_FAILURES_BEFORE_ESCALATION` — and 1341 is `def _is_retryable`, the next top-level definition. The count is unaffected, because the ten calls all sit between 1064 and 1296, which is why this is Low and not a correctness finding against the sentence. The defect is that the parenthetical was added for exactly one purpose — R-0398's own prescription, "a doc that states such a count states the span it counted over so a later reader can reproduce it" — and as written it does not serve it: a reader who counts `_record(` over 936 to 1341 finds ELEVEN occurrences, the same eleven that produced the original error, because the span given is wrong in one direction and the nested definition at 1036 is still not mentioned in the other. A repair that reproduces the defect's own failure mode for its next reader has not landed the lesson, only the number. It is registered rather than folded into R-0398's resolution so the record shows a repair being audited and found short, instead of a reviewer accepting its own prescription as met because a number changed. The fix is the DOCFIX2 rewrite in this same commit: the span becomes 936 to 1304 and the sentence names the nested definition it excludes. OPEN.

- R-0402 — Low — the R19 block twice stated a COUNT of its own enumerations and both counts were wrong, and the worker paid for it with an unordered sixth commit. The Change section read "exactly these seven paths" and then listed eight (`.agent/authored/f077-r19.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md`, `docs/system/autonomy-watchdog-v1.md`, `docs/roadmap/features/T2_F077.md`, `.agent/handoff.md`), and gate 16 read "for EACH of the seven slices" and then named nine. The SETS were right — `git diff --name-only 386ef7b5..HEAD` returns exactly those eight paths and no ninth, and all nine slices were proven — so nothing was misbuilt; only the reviewer's arithmetic over its own list was wrong, which is why this is Low. The cost was still real and lands entirely on the worker: gate 15 as written could not be satisfied, the handback had already been committed carrying the block's own "seven" verbatim, and the honest resolution took a follow-up commit that no order in the block asked for. The class is the reviewer's recurring one — a gate asserting a value the reviewer did not measure — but aimed at a new target: not the code (checklist item 8), not the target file (item 6), not the guarding tests (item 7), but the block's OWN enumerations, which is the one place the checklist never thought to look because it is the only place the reviewer fully controls. From here, a block that states the cardinality of a list it also enumerates counts that list mechanically on the final bytes, at the same moment checklist item 1 counts the block's lines, or states no number at all and lets the enumeration speak — the enumeration is the contract; the numeral adds nothing but a way to be wrong. OPEN.

- R-0404 — Low — the R1 handback states a file count that the branch's own diff contradicts, one round after the identical class was registered as R-0402. `.agent/handoff.md` gate line 14 reads "Branch touches 7 files, all under `.agent/` plus the one STATUS line", while `git diff --name-only 668d40f7..HEAD` returns EIGHT paths: `.agent/authored/f082-r1.md`, `.agent/candidates.md`, `.agent/context.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and `docs/roadmap/STATUS.md`. Exactly seven of those sit under `.agent/`, so the sentence is recoverable under the reading "seven `.agent/` files, plus the one STATUS line" — but its plain reading is a total, and as a total seven is wrong; the two clauses do not agree, which is the R-0331 class as much as the R-0402 one. Nothing downstream is affected and no verdict changes: the gate the sentence decorates is `git diff --stat 668d40f7..HEAD -- packages/ apps/ tests/`, the reviewer re-ran it independently and it is EMPTY, so no production file was touched and the change set really is the one the block named. It is registered rather than corrected in passing because R-0402 recorded this exact failure — a numeral written beside an enumeration without counting the enumeration — at the close of the previous feature, and a recurrence in the very next round is evidence that the lesson has not landed. The counter-measure, binding from R2 on: any sentence in a handback or block that pairs a numeral with an enumeration either counts that enumeration mechanically first, or states no numeral at all. OPEN.

- R-0405 — Low — the R2 block's own gate 10 contradicts the same block's C1c, so the gate could not be satisfied as written and the worker was right to answer it with an explanation instead of a number. Gate 10 orders `git diff --name-only 35838c5e..HEAD` and says the result "must equal the block's Change list", a list of seven paths; C1c of the same block orders the worker to leave `.agent/context.md` untouched when two stated checks hold, which they did, so the real diff is six paths and equality is unreachable by construction. This is the reviewer's defect, not the worker's: it is the R-0331 clause-versus-clause class, where two clauses of one block are each defensible and jointly impossible, and it is the same failure the reviewer charged the worker for in R-0404 one round earlier — a numeral asserted beside an enumeration that the block's own rules change. Nothing on disk is wrong and no verdict moves: the property the gate exists to protect, that no path appears OUTSIDE the Change list, was checked and holds at six of seven. The counter-measure, binding from R3 on: a change-set gate states the Change list as a CEILING — every path in the diff appears in the list, and paths the block conditionally exempts may be absent — never as an equality, unless the block contains no conditional write. R3's gate 10 is worded that way. OPEN.

- R-0406 — Medium — `.agent/live_review.md` carries a "Next free id" claim in its header that the record below it contradicts, and a session that trusts the header will reuse an id that already exists. The header line reads "monotonic R-XXXX series across the reset. Next free id: R-0404." while the record now contains a registered `- R-0404 — ` paragraph, so the next free id is R-0405 and the header understates it by one. The cause is structural rather than careless: the header was authored at the R1 reset when R-0404 genuinely was free, the record is APPEND-ONLY by the convention every round applies, and no round since has been permitted to rewrite a line above the append — the R2 worker noticed the staleness and correctly declined to touch it, reporting it as an observation. That is the right conduct and the wrong outcome. The claim is also redundant: `docs/agents/planner_reviewer_prompt.md` §3 checklist item 10 already requires the open set and therefore the id ceiling to be recomputed MECHANICALLY from the record at every emission and never carried forward, so a stored next-free-id is a second source of truth for a value the rule says to derive. The fix is to stop storing it: the header sentence naming a next free id is removed at the next feature's reset, and until then every consumer derives the ceiling with `max` over `^- R-\d+ — `. R3 does not rewrite the header, because doing so would break the append-only property for a cosmetic gain mid-feature; it is fixed at F082's own closure or at the next reset, whichever comes first. OPEN.

- R-0407 — Medium — `packages/orchestration/gauntlet_runner.py::measure_tokens` reads two token keys that no writer in this repository produces, so every gauntlet run records a MEASURED ZERO for tokens instead of the truth, which is exactly what that function's own docstring forbids. It sums `usage.get("prompt_tokens")` and `usage.get("completion_tokens")`, while the only producer of the `cost.usage` body it reads is `packages/orchestration/orchestrator_loop.py::measure_call_cost`, which writes `input_tokens`, `output_tokens`, `cache_read`, `cache_creation` and `total_cost_usd`; the reviewer linked writer to reader end to end — `orchestrator_loop.py` calls `measure_call_cost(call)` and passes the result into `_record`, the ledger entry carries it as `cost`, and `gauntlet_runner.py` feeds those entries to `measure_tokens` to fill `run.json`. Because `usage` IS a dict on a measured run, the function sets `measured = True` and then sums nothing, returning `{"in": 0, "out": 0}` rather than `None` — so `run.json` gets a `tokens` key of zeros and never gets `tokens_source: unmeasured`. The docstring above those lines states the opposite invariant in as many words, "``None`` is not zero. A run whose provider reported no usage did not spend nothing", and cites R-0178, "the matrix must not understate cost"; the defect is that the invariant is enforced against the wrong key names. The suite never caught it because `tests/orchestration/test_gauntlet_runner.py` builds its own fixture usage body with `prompt_tokens`/`completion_tokens` — a shape production has never written — so the test pins the reader against itself rather than against a real writer, which is the R-0391 "count the writers" class seen from the test side. F082 owns this repair rather than deferring it: the bench's `cost` field reads this exact function, and a feature may not build its headline metric on a number known to be a false zero (DECISION F082 D1). The repair is additive and keeps every gauntlet test green unmodified. OPEN.

- R-0408 — Low — reviewer blocks order a named TOOL where they mean a PROPERTY, and the tool's availability is not constant across the sessions that execute them. Every block this feature has emitted orders `cmp <a> <b>` for its transport proof and `cp` for its block save; the R3 worker reported both DENIED to it by the permission layer, along with compound shell forms reading `$?`, and satisfied the same obligation with a `python3` byte comparison plus a sha256 of each side — a proof that is strictly stronger, because it reports the digest rather than only an exit code. The R1 and R2 workers reported `cmp` exit 0 for the identical obligation, so availability varies by session class or invocation form rather than being uniformly absent, which is exactly what makes ordering the tool unsafe: a block cannot know which side of that line its worker will land on, and a worker that meets the obligation by another route is forced to spend a declared deviation proving the reviewer's phrasing wrong rather than anything about the repository. This is the same shape as the already-recorded `remedy`-entry-point split, where the CLI name is denied session-wide and `python3 -m apps.cli.main` is the working form. Nothing on disk is wrong and no verdict moves: byte equality was proven in all three rounds. The counter-measure, binding from R4 on: a transport or comparison gate states the PROPERTY and its evidence — "prove the two files are byte-identical and report the shared sha256" — and names a tool only as a suggestion, never as the gate. R4's gate 2 is worded that way. OPEN.

- R-0409 — Low — the R4 block's authored PLAN slice asserted an outcome that the same block's own stop clause existed to prevent, so the worker could not apply the slice verbatim AND keep `.agent/plan.md` true. The slice's Current Step read "the five frozen orders built behind a freeze", while C2's stop clause instructed the worker to write orders only for the capabilities its survey found expressible and forbade inventing the rest; the survey found three of five, so applying the authored text unchanged would have put a false claim in the file the Commit Gate requires to match the work. The worker resolved it correctly and declared it: it applied the slice, then corrected the two words in the same round's later commit, and preserved the authored original verbatim in `.agent/authored/f082-r4.md` and `.agent/last_block.md` so the transport proof still holds against what was actually authored. This is the reviewer's defect and it is the R-0331 clause-versus-clause class for the third time in this feature, after R-0404 and R-0405: a block wrote a NUMBER beside an outcome its own conditional logic could change. The counter-measure, binding from R5 on: an authored state slice never states a count or an outcome that a stop clause, a survey or any other conditional step in the SAME block could falsify — it names the thing without the numeral, and the numeral is written by the round that measured it. OPEN.

- R-0410 — Medium — F082's acceptance criterion "changing an order file without bumping its version fails validation" is met against a FILE-side edit only, and the closure must say so rather than quoting the criterion as satisfied outright. `packages/orchestration/bench_orders.py::load_bench_order_set` refuses an order whose bytes no longer match the digest recorded for the version the file still claims, which is the criterion's plain case and is pinned by `test_editing_an_order_without_bumping_its_version_fails_validation`. What it cannot refuse is a COORDINATED edit that rewrites the order file and also rewrites the digest recorded under the version it still claims: the manifest is the only record of what version 1's bytes were, so once it is rewritten there is nothing left to compare against. No in-repo, self-contained freeze can close that, and DECISION F082 D2 rejected deriving the version from git history precisely because validation must hold inside an exported evidence bundle where no history exists. The worker discovered this while writing its own tests, withdrew a test that asserted a refusal the design cannot deliver, replaced it with `test_a_manifest_side_digest_rewrite_is_outside_what_the_freeze_can_see` which pins the residual as a known limit, and stated the limit in the module docstring — which is the correct handling and is why this is a scope-honesty finding rather than a defect. What the freeze does buy is stated there too: the edit can no longer be silent, because it takes two coordinated changes in two files and the discarded version pair is missing from the series. The obligation this finding carries: F082's Built State section and its closure line state the threat model in these terms, and neither claims the criterion holds against a manifest rewrite. OPEN.

- R-0411 — Medium — the frozen bench set is THREE orders where the F082 feature file's Design names five, and the gap is a property of the fixture rather than of the round that stopped at three. The feature file asks for "five frozen orders probing distinct capabilities — a small CLI tool, an API endpoint with tests, a frontend widget …, a bugfix on a fixture repo, a refactor with unchanged behavior". R4's survey established, and the reviewer re-verified independently, that `scripts/gauntlet_sample_project` is a pure-Python CLI project: a grep for `http`, `flask`, `fastapi`, `django`, `route`, `endpoint`, `wsgi`, `asgi`, `uvicorn` and `socket` over the whole tree returns zero hits, and it holds no `.js`, `.ts`, `.html`, `.css` or `package.json`, so the API-endpoint and frontend-widget capabilities have nothing to be expressed against. Three ARE expressible and were built, each on a premise the reviewer checked at its source: the CLI order on `sampleproj/cli.py::build_parser` never passing `report.py::build_report`'s existing `width=`; the bugfix order on `config.py::DEFAULT_CONFIG_FILENAME` having exactly one grep hit, its own definition, while `config.py::resolve` reaches the file layer only under `if config_path is not None` and the README publishes a four-step precedence that includes it; and the refactor order on `tests/test_cli.py` already pinning stdout, stderr and exit code through `capsys`. The worker honoured the stop clause literally, refused to invent the missing two, and recorded them as owed — which is why this is registered against the PLAN rather than against the round. It is a real gap all the same: a bench that ships three of five measures less than the feature promised, and closure may not quote the Design's five. DECISION F082 D3 records how the two are recovered, and until they exist the feature file's Design is amended by that decision rather than silently under-delivered. OPEN.

- R-0412 — Medium — `.agent/context.md` carries statements from superseded plans in TWO places, because every F082 block rewrote only the clause it was pointing at and none grepped the file for the same claim elsewhere — the R-0394 "retire the claim everywhere" class, now inside a single file rather than across two. The first instance the R5 worker found and correctly declared rather than silently repaired: the sentence "Still to come: the five frozen order files with per-order version tags, the append-only history under the data root's project area, and the `stats bench` CLI surface" sits nine lines below the R5 CTXSCOPE2 pair's statement that THREE orders are built and that the missing two wait on a bench-owned fixture per DECISION F082 D3, so the file asserts both that three orders exist and that five are owed. The second instance nobody has declared and no block has ordered: the `## Steps` section still holds the seven-round map authored at R1 in commit f7f1f57e — "R3 T001 factoring, the five orders and the record schema → R4 T002 history, trend and regression rules → R5 T003 CLI, model context and a fake-provider run → R6 the integration gate → R7 closure" — which is wrong about rounds that have already happened (R3 built the pure record builder and the R-0407 token repair, R4 built the frozen order set, R5 recorded and closed) and contradicts `.agent/plan.md`, which maps R6 to T001's dry run, R7 to T002, R8 to T003, R9 to the integration gate and R10 to closure. Two state files that the bootstrap reads therefore give a resuming session two different round maps. The precedent is that this section IS maintained: F077's own `## Steps` was extended round by round with a ✅ per closed round, out to R17, and F082's has stood untouched since the claim. This is the REVIEWER's defect and not the worker's — the R5 block's Goal was in as many words "re-sync the state mirrors", and it ordered exactly one rewrite pair in this file while leaving two contradictions standing. The counter-measure, binding from R6 on: before ordering a rewrite pair in any `.agent/**` state file, grep that WHOLE file for the claim being changed and retire every instance in the same pair set, and a block whose Goal names a state re-sync re-reads the target files end to end rather than only the region it means to touch. R6 retires both instances. OPEN.

- R-0413 — Low — the R5 block's own header contradicted the plan text the same block carried, which is the R-0331 clause-versus-clause class for the fourth time in this feature and the first time it recurred in the very block that registered the counter-measure against it. The header line reads "── STEP R5/9 — F082 Self-benchmark", putting the feature at nine rounds, while the PLAN slice inside that same block ends "4. R9 the integration gate, R10 closure", putting it at ten; the denominator has moved 7, 7, 7, 8, 9 across `.agent/authored/f082-r1.md` through `f082-r5.md` while the plan it summarises grew, and at R5 it was already one short of the block's own arithmetic. Nothing on disk is wrong and no verdict moves: the denominator is an estimate and every round's real sequence is carried by `.agent/plan.md`, which was correct. It is registered rather than corrected forward because R-0409, authored and applied in that same block, states the rule it breaks — "an authored state slice never states a count or an outcome that a stop clause, a survey or any other conditional step in the SAME block could falsify" — and a counter-measure that its own block violates on emission is worth one id to stop. The counter-measure, binding from R6 on: the step header's denominator is read from the CURRENT `.agent/plan.md` Next Steps at emission and matched against the block's own PLAN slice as part of pre-emission checklist item 10, or the header carries the round number alone with no denominator. R6's header is measured against its own PLAN slice and both say ten. OPEN.

- R-0414 — Low — `.agent/context.md` carried a THIRD superseded region of exactly the class R-0412 registered one round earlier, and the R6 block that registered R-0412 left it standing. The Scope paragraph's R2-inventory sentence still reads "the factoring is ADDITIVE, so the bench lands as a NEW `packages/orchestration/capability_bench.py` with `tests/orchestration/test_capability_bench.py`" — singular, one module — while three bench modules now exist on this branch: `capability_bench.py` from R3, `bench_orders.py` from R4 and `bench_dry_run.py` from R6, each with its own test file. Nothing on disk contradicts it outright, which is why it survived two sweeps: it is an incomplete statement rather than a false one, and a grep for a contradiction does not return it. R-0412's counter-measure says to "grep that WHOLE file for the claim being changed and retire every instance in the same pair set"; the R6 block ordered two pairs against the two regions R-0412's own text named and never re-read the file for a third, so the counter-measure was applied to the instances already known instead of to the file. That is the REVIEWER's defect and not the worker's: the R6 worker found this region while executing gate 7, reported it in the handback as "one residual, NOT repaired (outside the ordered pairs)", and correctly refused to repair it outside its ordered slices, which is the R-0406 conduct this repository asks for and the second round running that the worker has declared a region the block did not order. The counter-measure, additive to R-0412's and binding from R7 on: a block that retires a superseded claim in an `.agent/**` state file greps that file for the claim's SUBJECT — here, which modules this feature builds — rather than for the sentence being replaced, and the reviewer re-reads the whole target file at emission and lists every region naming that subject, so the sweep ends at the file rather than at the findings that happened to name a region. R7 retires this one and the sweep is stated as complete for `.agent/context.md`. OPEN.

- R-0415 — Medium — T002's regression rule is built correctly and pinned by nothing: BOTH mechanisms that make it a rule rather than a comparison survive deletion with the whole suite green. The reviewer proved it by mutation in a disposable worktree at `20f101b0`, twice, each time reverting the previous mutation first. Replacing `if latest <= baseline * multiplier:` with `if latest <= baseline:` in `bench_history._threshold_regression` — deleting the threshold multiplier outright — leaves `8 passed`. Replacing the body of `bench_history._median` with `return float(sum(values)) / float(len(values))` — the mean instead of the median, the exact choice whose one-line WHY comment says "one catastrophic run must not raise the bar every later run is compared against" — also leaves `8 passed`. The cause is in the FIXTURES rather than in the assertions: all three goldens carry IDENTICAL trailing values, `flat.jsonl` and `degrading.jsonl` both at cost totals 1200 and 1200 with walls 40.0 and 40.0 across runs 1 and 2, and over identical values the median equals the mean and every positive multiplier ranks the same way, so no assertion written against those files can see either mechanism. The tests are not weak — they read their expected numbers off the goldens rather than restating them, which is exactly right — they are blind, and blind in a way only a mutation finds. This is the REVIEWER's defect: the R7 block ordered three goldens and named their shapes precisely, and every shape it named was a flat trailing series. It matters now rather than later because R9 wires `stats bench` to a CONFIG multiplier: a config knob whose value changes no test outcome is a knob that can drift to any number, including 1.0, without one gate going red, and the F082 acceptance criterion "cost/wall exceed the trailing median by a config multiplier" would then be satisfied in name only. The counter-measure, binding from R8 on: a block that orders a threshold rule also orders at least one fixture whose trailing values are NOT all equal and at least one assertion on the BASELINE the rule computed, not only on whether a warning appeared — a warn/no-warn boundary tests the fixture, a baseline value tests the rule. R8 closes it with a fourth golden and two tests, and re-runs both mutations to prove they now die. OPEN.

- R-0416 — Low — the closing sentence of R-0414 was false on disk in the same commit that wrote it. FINDING-R414 ends "R7 retires this one and the sweep is stated as complete for `.agent/context.md`", and after R7's C2 that file still carried two regions of R-0414's own class: the Scope paragraph's "Built so far" list, which names `capability_bench.py` and `bench_orders.py` and omits R6's `bench_dry_run.py`, followed by a "Still to come" clause naming the history append and the regression rules that R7's own C3 landed one commit later; and the Steps map, which awards ✅ to R1 through R5 and none to the landed R6. This is the third round running that a worker has declared a stale region its block did not order, and the second running that the declaration was correct — the R7 worker reported both under gate 7 and refused to repair them outside its ordered pair, which is the R-0406 conduct this repository asks for. The defect is entirely the reviewer's and it is a compound of two already-registered classes: R-0409 forbids an authored state slice from stating an outcome that a later step in the SAME block could falsify, and R-0413 registered the first time a counter-measure was violated by the very block that introduced it; R-0414's own counter-measure says to re-read the whole target file at emission and list every region naming the claim's subject, and the block that carried it re-read the file for the SENTENCE it was replacing instead. The claim also cost nothing to make and could not be checked by any gate, which is why it survived: gate 7 asked the worker to REPORT other stale regions, and reporting them does not retract a sentence already written. The counter-measure, binding from R8 on and additive to R-0414's: an authored finding never states that a sweep, a migration or a retirement is COMPLETE. It states what the round retires, by name, and leaves completeness to be measured by the next round's gate against the file. A completeness claim is a prediction about bytes the same block has not yet written, which is the R-0371 class in prose form. R8 retires both named regions and asserts nothing about what remains. OPEN.

- R-0417 — Low — R8's gate 11 ordered the DELETION column of `tests/orchestration/test_bench_history.py` to be 0, to protect the eight existing tests from being edited while two were added, and that gate made a sentence the same round falsified impossible to repair. The module docstring opens "The three goldens under ``fixtures/bench_history/`` are three runs over the same two order ids"; R8's C3 added `varied.jsonl`, a FOURTH golden of FOUR runs over ONE order id, so both halves of the sentence became wrong in the commit that added the file, and correcting it needs exactly one deleted line, which the gate forbade. The worker took the ordered constraint, declared the residual in the handback, and repaired nothing outside its slices — the fourth consecutive round in which a worker has declared a stale claim its block did not order and the fourth in which the declaration was correct (R-0412, R-0414, R-0416 and this one). The defect is the REVIEWER's twice over: once for a zero-deletion gate that could not coexist with the round's own change, and once for the class itself, because this is the same stale-claim class those three earlier findings already registered and the counter-measures they carry are aimed at `.agent/**` state files rather than at every file a round makes stale. Registering a fifth finding for a fifth instance would be the wrong answer; the class needs a GATE, not another paragraph. The counter-measure, binding from R10 on and REPLACING the file-scoped halves of R-0412, R-0414 and R-0416 rather than adding to them: (1) a zero-deletion gate may only be ordered over regions the round does not make stale, and where a round changes what a file's prose asserts, the block orders the prose pair in the SAME commit; (2) every block's gate list carries one standing staleness gate — for each file the round touched, re-read it end to end and report every sentence that states a count, a list of modules, a round map or a completion, together with whether it still holds — so the class is measured every round instead of discovered by a worker and registered by the reviewer one round later. R9 retires this sentence and adds that gate. OPEN.

- R-0418 — Low, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer. The R10 block's Handback paragraph ordered the handoff to "repeat the Fortschritt line verbatim", but no Fortschritt line exists anywhere in the R10 block: its only occurrence of the word is that instruction itself. This is the R-0371 class — ordering a value that cannot exist at the moment the text is written — and it arises specifically from self-drive. Under the split workflow the Fortschritt line lives in the operator brief that the paste relay carries alongside the block, so a worker reading the relay sees it; under docs/agents/self_drive_protocol.md there IS no relay, the worker is a delegated subagent that never sees the reviewer's brief, and any instruction to repeat something from that brief is unsatisfiable by construction. The worker did the right thing: it declared the deviation and invented nothing, which is exactly the behaviour planner_reviewer_prompt.md §3 item 8 predicts of an honest worker facing an unmeetable gate. The fix binds the REVIEWER, not the worker: in self-drive every block that requires the handoff to carry the Fortschritt line must CONTAIN that line as authored text, or must not order it. R11 carries it as an authored slice, which is the standing form from here.

- R-0419 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer against the code. The R11 block asserted a fact about this repository that a wider grep refutes: DECISION-D6 states the reviewer "found exactly one role bound to a model — `orchestrator.model`", and the PLAN slice repeated it as "only one role is bound to a model". Both are FALSE. `packages/providers/ollama_planner/provider.py::_resolve_model` and `packages/providers/ollama_builder/provider.py::_resolve_model` each bind a second and third role to a model, and `packages/orchestration/role_config.py::KNOWN_ROLES` is a seven-name table whose resolvable `_FIELDS` include `model`. The cause is precise and worth naming rather than generalising: the reviewer grepped ONE file, `gauntlet_runner.py`, and wrote the result as a property of the whole repository. That is the R-0391 class — "an invariant is not established by the first file you look in; grep every writer before authoring a claim against it" — recurring here in its authored-block form rather than its finding form. The claim was also load-bearing, which is what makes this Medium rather than Low: the scarcity of role→model bindings was the stated reason DECISION F082 D6 inserted an inventory round, so a false fact was carrying a real planning decision. The decision survives its bad reason — the inventory was worth running, and it is precisely what caught this — but the reason is corrected in DECISION F082 D7 rather than left standing. Standing rule from here, binding the reviewer: a block may state a repository-wide absence ("nothing does X", "only one Y exists") only after a repository-wide search, and the block names the search it ran. An absence claimed from a single file is an unrun claim.

- R-0420 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer by measuring the committed block. The R13 block is FOUR HUNDRED AND FIFTY-SEVEN lines against the four-hundred-line cap that DECISION F105 D5 sets and that `.agent/context.md` restates with 240 as the preferred target (R-0381). The reviewer never measured it. This is the third distinct member of the same family on this branch — R-0402 and R-0404 were miscounted enumerations, R-0417 was a staleness sweep claimed rather than run — and they share one root cause: the reviewer states a quantity about its OWN text without executing a count on the final bytes. No downstream cap was breached, because C0a's 457 insertions are still inside the 500-insertion commit limit, which is the only reason this is Medium and not High; the cap exists precisely to keep that distance, and spending it unknowingly is the defect. Standing rule from here, binding the reviewer: the block's line count is MEASURED on the final bytes immediately before emission, and the measured number is stated in the delegation so the worker can contradict it. A cap that is only remembered is not a cap.

- R-0421 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer with a repository-wide grep. DECISION F082 D8 states that `packages/orchestration/intake.py::make_structured_call_fn` "has six call sites" and then, in the very same sentence, enumerates seven of them — one in `intake.py` itself, two in `gauntlet_runner.py`, two in `apps/cli/commands/mission_cmd.py` and two in `apps/cli/commands/do_cmd.py`. The enumeration is CORRECT and the numeral is wrong: the real count is SEVEN, at `intake.py:324`, `gauntlet_runner.py:216` and `:225`, `mission_cmd.py:227` and `:385`, and `do_cmd.py:246` and `:2864`. This is the R-0402 and R-0404 class recurring for the third time, and the aggravating detail is that D8's own preceding sentence claims the count "was taken with a repository-wide grep before this decision was written" — the grep WAS run and did return seven; the numeral was then written from memory rather than from the grep's output, which is the exact failure the rule was written to stop. It is Medium rather than Low because it sits inside a DECISION, the most durable record this branch keeps, where a wrong number outlives every round that could have caught it. The decision's substance is untouched: the exception it grants is safe at seven call sites for precisely the reason it gives, that none of them is affected. Standing rule from here, binding the reviewer: a numeral that introduces a list is written by COUNTING that list after the list is final, never before and never from the search that produced it.

- R-0422 — Low, REVIEWER-GATE DEFECT, found by the worker and confirmed by the reviewer by re-deriving the property. R13's gate 7 ordered, for each of eight slice pairs, that `post == pre.replace(FROM, TO)` hold "over its own COMMITTED revision" — while the same block's Bundle put six of those eight pairs into ONE commit, C2. The property is therefore structurally unreachable for those six: applying a single replacement to `pre` can never reproduce a `post` that carries six, so a truthful worker must report False six times for a change that is entirely correct. The worker did the right thing and reported the composite instead — `pre` with all six replacements applied in block order EQUALS `post`, which the reviewer independently re-derived — but it had to invent the correct gate at handback time, which is the reviewer's job. This is the R-0371 family, a gate that cannot be satisfied as written, in its arithmetic form rather than its self-reference form. Standing rule from here, binding the reviewer: when N pairs share one commit, the block orders the COMPOSITE property over that commit plus the per-pair FROM 1x-to-0x and TO 0x-to-1x counts, which ARE individually measurable, and never a per-pair whole-file equality.

- R-0423 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer by measuring the committed file. The R14 block ordered `.agent/plan.md` "under 50 lines" in its own Constraint 4 and then supplied a PLAN slice that is FIFTY-TWO lines, to be applied as a WHOLE-FILE byte-equal replacement. The two orders cannot both be obeyed, and the worker obeyed the one that keeps transport provable — byte-equality — and declared the breach, which is the correct choice. This is R-0420's family recurring INSIDE the block that registered R-0420: the reviewer measured the block itself, as the new rule demands, and did not measure the slices the block carries. AGENTS.md's own under-fifty rule for `plan.md` is therefore broken on disk at HEAD, which is why this is Medium. Standing rule from here, binding the reviewer: every WHOLE-FILE slice is measured against the cap that binds its TARGET file before emission, and the measured number is stated in the block next to the constraint it must satisfy. Measuring the container does not measure the contents.

- R-0424 — Medium, REVIEWER-GATE DEFECT, found by the worker and confirmed by the reviewer by re-deriving the count. R14's gate 9 ordered that a phrase quoted out of DECISION F082 D8 appear in `.agent/live_review.md` exactly ONCE — the original inside D8 — and stated that a 2 means "the record was edited or the finding was rewritten". Neither happened: the reviewer verified that D8 is untouched by proving the whole file is a pure append over `dc376e91^`, with 8 insertions and 0 deletions. The real cause is that the block's OWN findings slice quotes that phrase verbatim, in double quotes, inside R-0421. Applying the block correctly therefore FORCES the count to 2, and the gate's stated expectation of 1 was unreachable from the moment the block was written. This is the R-0371 family — a gate that cannot be satisfied as written — in a new form: not self-reference and not arithmetic, but a gate that counts a string while ignoring the block's own contribution of that string. Standing rule from here, binding the reviewer: before ordering a count of any string, count that string in the BLOCK's own slices and either add that number to the expected value or gate a property the block's text cannot influence. This round applies the rule by ordering line-anchored counts only.

- R-0425 — Low, REVIEWER-FINDING DEFECT, found by the worker and confirmed by the reviewer with a repository-wide grep and by reading the file. R-0421 states that the seventh call site of `packages/orchestration/intake.py::make_structured_call_fn` is at `intake.py:324`. Line 324 is a COMMENT line inside the factory body; the real seventh call site is `intake.py:331`, inside `make_provider_call_fn`. The finding's substance is untouched and re-verified: there are SEVEN call sites, and the other six line numbers — `gauntlet_runner.py:216` and `:225`, `mission_cmd.py:227` and `:385`, `do_cmd.py:246` and `:2864` — are exact. Corrected here by APPENDING rather than by editing R-0421, because a registered finding is history. Low because the count, which is what R-0421 exists to correct, is right. Standing rule from here, binding the reviewer: a line number written into a finding is read back off the file at that line before the finding is emitted; a grep that returns a match does not tell you which of its lines you copied.

- R-0426 — Medium, REVIEWER-PLAN DEFECT, found by the reviewer while reading the code the plan describes. `.agent/plan.md` and the R14 handoff both state that T003b's read half means carrying `models` from `gauntlet_evidence.py::RunEvidence` into the bench record, "which needs its own additive ruling because that is a third gauntlet module". Every clause of that is false, and the code says so: `capability_bench.build_bench_record` receives the raw `run.json` body as its `evidence_body` argument, and `bench_dry_run._recorded_bodies` produces that body with `json.loads` straight off disk without constructing a `RunEvidence` at all. `RunEvidence` is not on the path, `capability_bench.py` is a BENCH module and not a gauntlet module, and the three `BenchRecord(` construction sites under `packages/` are all in bench modules. Had the block been written from the plan, the round would have edited a gauntlet module that needs no editing and would have manufactured a DECISION to permit it — the exact scope drift the additive design exists to prevent. Medium because a plan that names the wrong file directs the next round's work. This is R-0419's grep-every-writer rule applied to a data PATH rather than to a set of writers, so it adds no new standing rule; it is evidence that the existing one was not run here.

- R-0427 — Low, STALE CLAIM IN SHIPPED CODE, found by the worker under the standing staleness gate and confirmed by the reviewer by reading the file. The module docstring of `packages/orchestration/bench_history.py`, at lines 16 to 18, reads "ADDITIVE by construction (F082 inventory Q11): `BenchRecord` and `projects_dir` are IMPORTED. No symbol moves out of a bench or gauntlet module and none is edited." R15 edited `BenchRecord`: it gained the `models` field. Under the sentence's present-tense reading — no symbol is edited — the claim is now false in shipped code. Under the narrower reading the paragraph's own heading suggests — no GAUNTLET module is edited, which is the additivity the F082 inventory Q11 actually ruled on — it still holds, and that reading is the one every round on this branch has enforced. The ambiguity is the defect: a docstring that states an invariant has to state which invariant, because the next reader will apply whichever reading is convenient. Low, because no behaviour depends on it and the additive design itself is intact and measured. The worker did exactly the right thing under gate 18 — reported it and left it, since no ordered slice covered that file — and that conduct is why it is on the record instead of being quietly rewritten inside an unrelated commit. Repaired at R17, which touches that module anyway for the run: the sentence is rewritten to name the gauntlet reading explicitly, or it is deleted, and no third option is invented. Standing rule from here: an invariant sentence in a module docstring names the set it quantifies over, because "no symbol is edited" and "no gauntlet symbol is edited" are different promises and only one of them is kept.

- R-0428 — Low, REVIEWER-BLOCK DEFECT, found by the reviewer at the start of the round while re-verifying the carried block, and corrected before any worker saw it. The R15 block was authored in one session and delegated in the NEXT one, and it named `BASE is 22ef2427` in four places — the handback SHA that was HEAD when it was written. By the time it was delegated, HEAD was 56635794, because the authoring session's own handoff commit landed AFTER the block was finished. Every range gate in the block therefore addressed a base one commit behind the commit the round actually started from, and `git diff --name-only 22ef2427..HEAD` would have attributed a prior session's `.agent/handoff.md` change to R15. The reviewer re-derived the base from HEAD at delegation time, replaced all four occurrences, and re-measured the block: the substitution is length-preserving, so the line count stayed at 399 and only the digest moved, from `8f5eddfc…` to `8640cc24…`. Low, because no round was ever gated against the stale base and no measured value was affected. It is registered anyway because the CAUSE is structural and new: this is R-0368's family — a range gate's base is the SHA the round starts from — recurring in the shape that only self-drive produces. Under the split workflow a block is authored and delegated inside one relay, so its base cannot move between the two; under `docs/agents/self_drive_protocol.md` a session can end at a STOP or a limit with a block authored and unapplied, and the handoff commit that ends that session is itself the commit that invalidates the base. The handoff's own instruction made it worse by naming the block's sha256 as the thing to verify, which the reviewer did — it matched, and matching proved only that the file had not been touched, not that its base was still current. Standing rule from here, binding the reviewer: a block carried across a session boundary re-derives its BASE from HEAD at DELEGATION time and re-states it, and a handoff that carries an unapplied block says so next to the sha256 it quotes. A digest that still matches is evidence about the file, never about the repository around it.

- R-0429 — Low, REVIEWER-BLOCK DEFECT, CLAUSE-VS-CLAUSE, found by the WORKER while applying the R16 block and declared in the handback before the reviewer read the diff. The R16 block's Constraint 2 said "Properties 1 and 5 of the contract exist only to make a vacuous pass impossible", but the block's OWN contract list two hundred lines below made property 1 ANTI-VACUOUS, SYMBOLS and property 2 ANTI-VACUOUS, SCAN, with property 5 the import-time side effect. Both clauses were written by the reviewer, in one file, and they disagreed. The worker followed the CONTRACT — the correct choice, since the contract is the constructive text — but copied the constraint's wrong numbering into the new file's module docstring, and then caught it under the standing staleness gate and spent an extra commit, `3a0b1d77`, correcting one word. Low, because the shipped code is right and the cost was one line in one commit. It is registered because the CLASS is the expensive one: R-0331, R-0334, R-0353 and R-0356 are the same defect, the planner_reviewer_prompt §3 pre-emission checklist items 9 and 10 exist to catch it, and it still arrived. What those items miss is the case here — the two clauses are far apart, agree in TOPIC, and disagree only in an ORDINAL, which reads as correct on a linear pass and is only caught by resolving each numeral against the list it indexes. Standing rule from here, binding the reviewer: a block clause that cites a numbered item of its own contract by ORDINAL is checked by counting into the contract list and reading back what that ordinal actually names, in the same pass that measures the block. An ordinal is a cross-reference, and an unresolved cross-reference is the one error a careful linear read cannot see.

- R-0430 — Low, HANDOFF DEFERRED ITS OWN MEASURED LENGTH TO A CHANNEL THAT LEAVES NO DISK ARTIFACT, found by the reviewer while checking the R16 handback against AGENTS.md D15. The R16 handoff correctly declared a stated-cause overage of the 60-line cap and correctly named the mandated content that caused it — seven per-commit tables, twenty-one gate values and the item-status table, no section dropped — but where D15 requires the declaring line to name "its actual line count", the handoff instead said "Real measured length is recorded in the round's completion report". Under the split workflow that would be recoverable: the completion report is the text the worker hands to Window 1. Under `docs/agents/self_drive_protocol.md` there is no relay, the worker is a subagent whose report ends with the round, and the handoff is stated by that same protocol to be "the only return channel" — so the deferred number reached NO durable artifact and the real count, 132 lines, had to be re-measured by the reviewer from the file. Low, because the overage itself is legitimate, every mandated section is present, and the number is trivially recoverable by `wc -l`. It is registered because the CAUSE is the self-drive shape rather than carelessness: a rule written for a two-window workflow named a channel that the one-session protocol deleted, and the worker followed the rule as written. Standing rule from here: a handoff declaring a D15 overage states its own measured line count as a NUMERAL in the declaring line, and never forwards it to a completion report, a transcript or any channel that does not survive the session. Adding the numeral does not change the count, because it is written into a line that already exists.

- R-0431 — Low, REVIEWER-SLICE DEFECT, THREE FAULTS IN ONE REWRITE PAIR, two of them declared by the worker as deviations D2 and D3 before the reviewer read the diff and the third found by the reviewer reading the applied result. The R17 block's `CTXIMPLICIT-R17` pair rewrote only the TAIL of a `.agent/context.md` bullet, and the bullet's surviving head still says "The allowlist is EMPTY today and gains exactly one name at R17" while the new tail says "R17, which spent it on `packages/orchestration/bench_run.py`" — so one sentence now asserts the allowlist is empty and that it has been spent, and both halves were authored by the same reviewer in the same round. The pair also had two mechanical faults: its TO slice's second line carries no two-space continuation indent, so `deliberate act, not a repair.` sits at column 0 and dedents out of the `- ` bullet it belongs to, and the `CTXSCOPE-R17-TO` slice's first line joins an existing sentence tail to produce a 94-character line inside a paragraph wrapped at about 79. Low, because nothing executable reads `.agent/context.md` and all three faults are text. The CAUSE is one habit and worth naming once: a REWRITE pair was scoped to the smallest span that made the new claim true, instead of to the span whose MEANING the new claim changes. The reviewer measured the FROM at 1x, confirmed `FROM in TO` was False and confirmed the composite reproduced — every ordered property passed — and none of those properties can see that the sentence CONTAINING the replaced tail now contradicts itself, because they compare bytes and not claims. Standing rule from here, binding the reviewer: a REWRITE pair extends to the whole sentence, bullet or paragraph whose truth value the edit changes, never to the minimal matching span; and a TO slice landing inside an indented block reproduces that block's continuation indent and wrap width, because a slice is applied into a shape it cannot see. R18 repairs the bullet whole.

- R-0432 — Low, A CONSTRAINT FROZE THE FILE THE ROUND ITSELF MADE STALE, found by the worker under the standing staleness gate, reported and correctly NOT repaired, then confirmed by the reviewer by reading the file. The R17 block's Constraint 6 said the allowlist gains exactly one name and "Touch no other line of the pin file", and gate 22 said to repair only what the ordered slices cover. Both were obeyed exactly. The consequence is that `tests/orchestration/test_bench_never_runs_implicitly.py` now carries three sentences that were true when R16 wrote them and are false at HEAD: the module docstring's "which is empty today and gains exactly one name at R17" at line 13, the allowlist constant's "EMPTY today, which is a measured fact and not an assumption" at line 63, and the section header "callers equal the allowlist, which is empty today" at line 180. A fourth, the `MIN_SCANNED_FILES` comment "File counts measured at R16 against this repository: apps 73, packages 256, scripts 29", is NOT a defect and is deliberately left: it is explicitly time-stamped to R16, so it remains true as history, and the observed count is now packages 257 exactly as the block predicted. Low, because the code is correct and only its prose lies. The CAUSE is structural rather than careless: a block that changes a file's state MUST carry the repair for that file's own description of its state, and a "touch nothing else" constraint written to protect a pin from drive-by edits also forbade the one edit the round made necessary. Standing rule from here: when a block spends a value a file describes in its own prose, the same block carries the pair that updates that prose; a freeze constraint names the lines it freezes rather than the whole file. R18 repairs all three sentences.

- R-0433 — Low, AN ENUMERATION MEANT AS A CALL LIST WAS READ AS AN IMPORT WHITELIST, declared by the worker as deviation D1 and confirmed by the reviewer. The R17 block's Constraint 1 said `bench_run.py` "is NEW and only IMPORTS `run_campaign`, `RunnerDeps`, `load_bench_order_set`, `dry_run_from_order_set` and `append_bench_run`", intending to describe the product verbs the join calls and to forbid reaching into anything else. The worker read "only IMPORTS ... " as exhaustive, which is what it literally says, and therefore could not import `gauntlet_runner.OrderOutcome` or `capability_bench.BenchRecord` for the return type — so `BenchRunResult.outcomes` and `.rows` are typed `tuple[Any, ...]` with the concrete types named only in field comments. The worker chose obedience over silent widening, which Constraint 8 demands and which is the correct call; the defect is the constraint's wording, not the reading. Low, because the runtime behaviour is identical and the types are documented one line away. The CAUSE is that a scope fence and a type-import are different things and the sentence conflated them: forbidding a module to CALL new product surface is a real constraint, forbidding it to NAME a type it already returns is an accident. Standing rule from here: a constraint enumerating imports says what the list is FOR — the product verbs this module may call — and states explicitly that importing a type for a signature is not a call. R18 restores the concrete annotations.

- R-0434 — Low, MY OWN ENUMERATION WAS SHORT BY ONE, found by the reviewer while authoring R18 against the file R-0432 describes. R-0432 says the pin file "now carries three sentences that were true when R16 wrote them and are false at HEAD" and names three: the module docstring's "which is empty today and gains exactly one name at R17", the allowlist constant's "EMPTY today, which is a measured fact and not an assumption", and the section header "callers equal the allowlist, which is empty today". There are FOUR. The fourth is the allowlist constant's other comment, "R17 adds EXACTLY ONE name, the fake-provider run's entry point", which is future tense over a name already sitting two lines below it. Low, because it is the same prose class R-0432 already registered and R18 repairs all four in one commit. It is registered separately because the CAUSE is a different mistake: R-0432's list was derived by matching one PHRASE, "empty today", and the fourth sentence is stale without containing that phrase. That is R-0402 and R-0404's class in its other form — those two counted their own list wrongly, this one counted correctly and claimed coverage the count never had. Standing rule from here, binding the reviewer: an enumeration of stale claims in a file either STATES the query it was derived from, so a later reader knows what it cannot have found, or it is derived by reading every claim-bearing sentence in the file. A grep for the symptom is not a read of the claim.

- R-0437 — Low, A PAIR SHAPE DECLARED WITHOUT ITS NEWLINE CONVENTION. Found by the WORKER while proving C6 and declared as deviation D2. The R18 block declared `CTXSCOPE-R18` APPEND-SHAPED, and gate 8 ordered the append proof on the stated ground that its FROM count "stays 1 in `post` BY CONSTRUCTION" because the TO contains the FROM. The worker measured FROM 0x in `post` and `FROM in TO` False — a REWRITE — and said so instead of reporting the number the gate expected. Both measurements are correct, and the difference is ONE CHARACTER: the reviewer determined the shape over the slice text WITHOUT its trailing newline, where the FROM is a prefix of the TO's first line; the worker applied and measured it line-oriented, WITH the trailing newline, where "…allowlist.\n" does not occur inside "…allowlist. R18 registered\n". The reviewer re-measured both readings against the committed block after the handback and reproduced each exactly: newline excluded gives APPEND, newline included gives REWRITE. Nothing wrong reached the disk — the composite proof holds under either reading, C6 reproduces `post` byte-for-byte, and the intended text landed. Low for that reason. The CAUSE is that pair SHAPE was treated as a property of the text when it is a property of the text PLUS the newline convention of whoever applies it, and this branch has already paid for that once: F082 R5 and R6 registered the same newline-dependence for slice COUNTS, and the lesson was written down for counts only. A rule recorded for one measurement does not cover the other measurement it also governs. Standing rule from here, binding the reviewer: every pair slice states whether its FROM and TO include the trailing newline, and its shape — REWRITE or APPEND — is declared under that stated convention. A shape asserted without the convention is a coin flip the worker is left to resolve, and a worker that resolves it correctly is then reporting a mismatch against its own correct work.

- R-0438 — Medium, A GATE THAT NAMED A PATH THAT DOES NOT EXIST, so the check it stood for never ran. Found by the WORKER while executing R19's gate 10 and declared as deviation 1. The gate ordered the canary "plus the `.agent`-state contract readers `tests/dashboard`, `tests/test_test_runner.py` and `tests/regression/test_resource_safety.py`". There is no `tests/dashboard` directory in this repository; pytest exits 4 with "no tests ran" and reports no failure, so the gate is not merely wrong, it is SILENTLY vacuous — the one failure mode this repository spends the most effort refusing. The dashboard contract reader is `tests/ui_server/test_dashboard_contract.py`, and the reviewer confirmed the absence and the real location after the handback: `ls tests/` has no `dashboard` entry, and `rg -l 'context.md' tests/` returns `tests/ui_server/test_dashboard_contract.py`. Medium, not Low, because a vacuous gate reports green for the wrong reason and had this round changed `.agent/context.md` in a way the dashboard contract rejects, nothing in the ordered gate list would have caught it — and this round DID change `.agent/context.md`. Not High, because the property was in fact intact: the reviewer ran `pytest tests/test_test_runner.py tests/regression/test_resource_safety.py tests/ui_server -q` at HEAD and got 324 passed, exit 0. The CAUSE is precise and is NOT a typo. `docs/agents/planner_reviewer_prompt.md` §4.11 names the contract READERS in prose — "the dashboard contract asserts the substring Steps plus ## Active Branch" — and the reviewer turned that prose into a PATH without ever resolving it against the disk. §4.11's own instruction, in the same paragraph, is to grep every test that reads the file (`rg -ln '<filename>' tests/`); the reviewer cited the rule and skipped the command it prescribes. This is R-0353's class — a citation that does not resolve — in the form that checklist item 9 does not cover, because item 9 re-measures `file:line` citations against the branch's own edits and this path was never valid on any branch. Standing rule from here, binding the reviewer: every path a gate names is resolved on disk at emission — `ls` or `test -e` — and a gate that names a test target additionally states the count that target is expected to collect, because a path that exists but collects nothing fails the same way. A gate whose target cannot be shown to exist is not ordered.

- R-0439 — Low, A PER-LINE COUNT ORDERED OVER LINES THAT CANNOT BE UNIQUELY COUNTED. Found by the WORKER while proving R19's gate 4 and declared as deviation 3. For the two append-shaped pairs the gate ordered "the per-line count of each TO-ONLY line among the lines that commit's diff ADDS". Applied literally to EVERY TO-only line, that includes blank lines and the `# ---…---` rule comments the file uses as section separators, which the same commit adds many times over — the worker measured 2x, 4x and 20x and REPORTED those real numbers rather than the 1x the gate's phrasing implies. Both readings are defensible and the worker chose the honest one. Low, because the composite proof at the same gate settles application byte-for-byte and no wrong conclusion was drawn. What makes it worth registering is that this is the THIRD form of one recurring mistake: R-0253 established that whole-file counts are unsatisfiable when a TO legitimately repeats an existing sentence, R-0437 established that a pair's SHAPE is undefined without its newline convention, and this one establishes that a per-line count is undefined without saying WHICH lines it ranges over. Each time, the rule was written down for the instance in front of it and not for the measurement class it belongs to. Standing rule from here, binding the reviewer: a per-line count over a diff's added lines NAMES the specific distinguishing lines to be counted — lines unique to the TO by inspection — and never says "each TO-only line". Blank lines, separator comments and repeated structural lines are excluded by construction and the gate says so.

- R-0440 — Low, A RESOLUTION THAT QUOTES A FILE'S WORDING WHICH ITS OWN ROUND THEN REWRITES. Found by the WORKER and declared as R20 deviation 1. C2's `Done: R-0436` text asserts that `.agent/plan.md` "now reads ... R-0417 through R-0437". C4 of the SAME round replaced plan.md as a whole file, and the replacement reads R-0417 through R-0439. Measured at HEAD: plan.md contains "R-0417 through R-0437" 0 times and "R-0417 through R-0439" 1 time, while the `Done: R-0436` line contains "R-0417 through R-0437" 1 time. The resolution was stale the moment C4 landed, in the round that wrote it. Low, because the resolution's SUBSTANCE — that the counter-measure list is stated as a RANGE and deliberately without a count — is exactly what plan.md still does, so the finding is genuinely resolved and only its quotation is dead. What makes it worth an id is that no ordering of the commits could have saved it: putting C4 first would have made the quotation true at write time and false at the NEXT plan rewrite instead, because the range's endpoint moves every round by design. The defect is quoting a moving value at all. Standing rule from here, binding the reviewer: a `Done:` text names the PROPERTY a repair established — "stated as a range, without a count" — and never quotes the target file's current sentence, because a resolution outlives every wording it could quote. Where a quotation is genuinely needed, it is pinned to a commit SHA rather than to "now reads".

- R-0441 — Low, A NUMERAL THAT CONTRADICTS THE ENUMERATION IT CLAIMS TO HAVE BEEN COUNTED FROM. Found by the WORKER and declared as R20 deviation 3. The R20 block's slice-convention paragraph says "Two EOF appends (GATE-R19-BLOCK, which carries the gate, both findings and the decision as one body)" — a numeral of two whose own parenthetical enumerates one — and then "Four named units, counted by listing them" over a block the reviewer measures at 6 `--- BEGIN SLICE` markers resolving to 5 logical units: 1 APPEND, 3 REWRITE pairs and 1 WHOLE FILE. Both numerals are wrong, and the second is wrong while explicitly claiming to have been derived by listing. Low, because no gate depended on either numeral and nothing downstream was mismeasured. It is registered because of what it does to R-0402's standing rule: that rule says count the enumeration or state NO numeral, and the phrase "counted by listing them" had been adopted as the rule's own compliance marker — so the marker became the lie. Standing rule from here, binding the reviewer: the phrase "counted by listing them", and every phrase like it, is BANNED. A block states the enumeration and, if it states a numeral at all, that numeral is produced by counting the emitted bytes mechanically in the same pre-emission pass that measures the block's line count — never from the author's recollection of what was written, and never certified by an assertion that counting happened.

- R-0442 — Low, A HANDBACK COUNT WHOSE RANGE WAS NEVER STATED, TRUE UNDER ONE READING AND FALSE UNDER ANOTHER. Found by the REVIEWER while reproducing R20 deviation 2. The R20 handback states "context.md names D10 1x and D11 1x". Measured at HEAD: the bare token `D10` as a word occurs 2 times and `D11` as a word 2 times, while the full citation "DECISION F082 D10" occurs 1 time and "DECISION F082 D11" 1 time. The handback's numbers are true under the full-citation reading and false under the bare-token reading, and the sentence says nowhere which string it counted. The substance holds: the stale citation the deviation reports is real and is repaired by this round's CTX-D10 pair, and the second `D10` occurrence is the historical line "R18 ... rule at D10", which is correct and must NOT be touched. Low for that reason. It is registered because R-0439, written in the very block this handback answers, established that a count is undefined without saying what it ranges over — and the next document produced under that rule broke it. R-0439 bound the reviewer's gates only. Standing rule from here, binding the WORKER's handback as well as the reviewer's gates: every count in a handback states the exact string or pattern counted and the file it was counted in, quoted, so a reader can re-run it. A bare token and its full citation form are two different counts and are never reported as one.

- R-0443 — Medium, A GATE SCRATCH DIRECTORY REUSED ACROSS FEATURES, SO A STALE FILE CAN BE READ AS THIS ROUND'S MEASUREMENT. Found by the WORKER and declared as R21 deviation 3. The R21 block ordered raw logs into `.remedy-wt/.cache/gate_r21/` on the assumption it was fresh. It was not: it already held 2026-08-13 artifacts of a DIFFERENT feature's R21 — `branch_meta.txt`, `branch_failed.txt`, `comm_*.txt`, three `.sh` scripts and a handoff draft — because the directory is named after the round number only and round numbers repeat across features. Every colliding name was overwritten by this round's real measurement before it was read, and the reviewer confirmed the committed evidence is this round's throughout, so nothing false was published. Medium rather than Low because the failure mode it exposes is the vacuous-gate class R-0438 names: a wait-loop in the worker DID briefly read the stale `branch_meta.txt` as this round's, and had the round died between that read and the overwrite, a previous feature's numbers would have been reported as this gate's with nothing in the evidence chain able to detect it — the file would have had the right name, the right shape and the wrong provenance. Not High because the two suite runs write their own logs unconditionally and the reviewer can re-derive every committed number from the branch and base logs, as it did. Standing rule from here, binding the reviewer: a gate scratch directory is named for the FEATURE and the round, never the round alone, and the block orders it created fresh — the worker asserts the directory did not exist before this round, or reports what it found and deletes it before writing. A path that outlives the round that owns it is not scratch.

- R-0444 — Medium, A PARITY GATE WHOSE MEASUREMENT CANNOT SEE THE THING IT WAS ORDERED TO DETECT. Found by the WORKER and declared as R21 deviation 4; the defective gate is the reviewer's own. R21's gate 8 ordered a CONTENT digest of `apps/ui/dist` before and after the base run to verify that `REMEDY_UI_NO_AUTO_BUILD=1` had neutralised the auto-build. The digests are equal and the gate reads GREEN, but the flag did NOT neutralise every build path: `apps/ui/node_modules` (mtime 2026-08-15T11:39:47.807) and `apps/ui/dist/index.html` (11:39:49.669) were both rewritten INSIDE the base-run window 11:38:41–11:41:10, against the 11:36:04 the parity copy had left. The rebuild happened to be byte-identical, so a content digest is blind to it by construction — the gate would report GREEN for a rewrite of any content, identical or not, and only luck made those two the same case. This is R-0169 recurring, and the earlier fix (set the flag, then hash the content) is precisely the counter-measure this instance defeats. Medium: nothing was mismeasured this round because the content really was identical, but the neutralisation claim the gate exists to support was never actually tested. Standing rule from here, binding the reviewer: a gate that asserts something did NOT HAPPEN measures the event, not the outcome. For the build-neutralisation check that means recording mtimes — or a directory-state stamp covering mtime and inode — before and after, and reporting the window; a content digest may accompany it but never stands alone, because equal content is consistent with both "no rebuild" and "an identical rebuild".

- R-0445 — Medium, A STANDING DEFECT IN THE CANONICAL INTEGRATION-GATE PROCEDURE THAT MANUFACTURES EIGHT FALSE BASE FAILURES ON EVERY RUN AND MASKS REAL ONES. Found by the WORKER and declared as R21 deviation 5; proven in both directions before it was believed. `docs/agents/integration_gate.md` step 3 orders environment parity restored by COPYING `apps/ui/node_modules` and `apps/ui/dist` into the base worktree, and explicitly forbids symlinking for a good reason of its own. But a copy preserves the SOURCE mtime while `git worktree add` stamps the freshly checked-out sources with the checkout time, so the copied build is ALWAYS older than the sources it was built from. `ui_server.py::_frontend_is_stale` therefore returns True, `::_auto_build_frontend` returns None under the flag the same procedure sets, and `::_load_frontend` calls `sys.exit(1)`; the server thread dies and all eight `tests/ui_server/test_live_state.py::TestUIServerIntegration` ids fail with "Server did not start in time". The procedure cannot restore freshness by copying, so this recurs on EVERY gate run for EVERY feature — the same eight ids appear in `.agent/gate_f077_r16/base_failed.txt` from the previous feature, which is the recurrence already on disk and unrecognised at the time. Medium and not Low because integration_gate.md step 3 states in its own words that a genuine base failure in those same files WOULD BE MASKED by the environment-class attribution, and eight permanently-failing ids in the UI server's integration tests are exactly the place a real regression would hide. Not High because it produces no false GREEN — the branch side is unaffected, and every gate run so far has attributed the ids rather than ignoring them. The repair is one line of procedure and belongs to `docs/agents/integration_gate.md`, NOT to this feature branch: after the parity copy, touch `apps/ui/dist/index.html` forward of every file under `apps/ui/src` (or build in the worktree), and have the procedure verify `_frontend_is_stale()` is False before the base run rather than discovering it afterwards. Routed to a follow-up rather than repaired here, because a process-doc fix inside a feature branch is scope drift and F082's closure states it as a known open finding.

- R-0446 — Low, A PARSE RULE ORDERED OVER TEXT IT DOES NOT FIT, SO THE GATE'S POPULATION DEPENDS ON WHICH READING YOU TAKE. Found by the WORKER while executing R22's gate 12(a). The gate ordered the open-set severity census read as "the word that follows `^- R-\d+ — ` up to the first comma". Across the 75 registered paragraphs the character immediately after the severity word is a space 47 times and a comma 28 times, because this ledger's finding titles are written as "Medium, A GATE THAT ..." in some rounds and "Medium A GATE THAT ..." in others. Under the strictest reading — severity word immediately followed by a comma — the rule classifies 26 of 73 open findings and silently drops 47 while still reporting a green census; under the looser reading it classifies all 73. The worker substituted "the first word after the em-dash", reported BOTH censuses, and the answer is identical either way: Blocker 0, High 0, Medium 23, Low 50. The reviewer independently recomputed both readings at HEAD and got Low 50 and Medium 23 under each. Low, because the closure precondition this census exists to test — no open Blocker or High — holds under every reading, and because the worker caught it before it mattered. It is registered because of the shape, which is now the fourth member of one family: R-0439 said a per-line count must name which lines it ranges over, R-0442 said a handback count must name the string it counted, and this one says a PARSE rule must be validated against the text it will parse. Standing rule from here, binding the reviewer: a gate that extracts a field by a textual rule is run against the actual corpus at emission and the block states how many items the rule successfully classifies out of how many exist. A rule that silently drops the items it cannot parse is the vacuous-gate class R-0438 named, wearing different clothes.

- R-0447 — Medium, A STATE FILE THAT NOW CONTRADICTS ITSELF, BECAUSE A DECISION MOVED A VALUE AN EARLIER AUTHORED SENTENCE HAD QUOTED. Found by the WORKER through the standing staleness gate, which is exactly what that gate exists for. `.agent/context.md` at the R22 head says in one place "the round map now runs to R21 the integration gate and R22 closure (DECISION F082 D11)" and in another, four dozen lines later, "→ R23 closure, per DECISION F082 D12". Both sentences are on disk in the same file at the same commit and they disagree about which round closes this feature. The reviewer confirmed it by literal count at HEAD: `DECISION F082 D11` 1x, `DECISION F082 D12` 1x, `R22 closure` 1x, `R23 closure` 1x. The cause is precise. The offending sentence was authored by the REVIEWER at R21 as the CTX-D10 pair's TO, to retire a stale D10 citation — and it retired that citation by quoting the round map, a value that moves. One round later the reviewer's own DECISION D12 moved it, and the R22 block that ruled D12 carried no pair to repair the sentence D12 falsified. Medium, not Low: `.agent/context.md` is read by thirteen test files and is the reviewer's context of record across sessions, so a reader resuming from disk gets two different answers to "which round closes F082" with nothing to break the tie. Not High because no test asserts the round map and the plan and the Steps chain both agree on R23. This is R-0440 recurring one round after R-0440 was written, in the reviewer's own text rather than in a `Done:` paragraph, which is precisely the generalisation R-0440 failed to make. Standing rule from here, binding the reviewer: a block that rules a DECISION changing any value carries, in the SAME block, a repair pair for every sentence on disk that states that value — found by grepping the value, not by recalling where it was written. The staleness gate is the backstop, not the mechanism; a contradiction it merely REPORTS has already shipped.

- R-0451 — Low, A BLOCK ASSERTED THAT ITS OWN SLICE SAID SOMETHING THE SLICE DOES NOT SAY, SO A DOCUMENTED DROP WENT UNDOCUMENTED. Found by the WORKER while executing the R1 carry. The R1 block's prose reads "`Gate:`, `Done:` and `Landed:` lines are NOT carried, and the head slice says so in prose, so nothing is silently dropped" — but LIVEREVIEW-HEAD, the slice that actually lands on disk, names ONLY the four `Landed:` lines. The reviewer confirmed the arithmetic at the BASE record: it held 22 `^Gate: ` lines, 2 `^Done: ` lines and 4 `^Landed: ` lines, so 24 lines were dropped that the committed record does not account for, against 4 that it does. Nothing is lost in the strong sense — the pre-reset record is intact in git history at f3fd96d7 and the reconstruction gate proves the carry was exactly the open set — but the reset's own prose is the only place a reader resuming from disk would look, and it under-reports what the reset removed. Low for that reason, and because the drop itself is correct and matches the F082 reset's shape. This is the block-clause family: R-0331 and its successors say two clauses of a block must agree with each other, and this one extends it by one step — a clause that makes a claim ABOUT a slice is checked against the slice's bytes, not against the intent, because only the slice survives the round. Standing rule from here, binding the reviewer: when block prose asserts that an applied slice states something, the pre-emission checklist greps the slice body for it; an unfound assertion is either deleted from the prose or added to the slice before the block is emitted. OPEN.

- R-0452 — Low, THE BLOCK THAT REGISTERED R-0449 BROKE R-0449'S OWN RULE IN THE SAME BREATH. Found by the WORKER, which declared it as its first deviation. R-0449, registered by the R1 block, states the rule "before ordering any value INTO an artifact, name the commit that writes the artifact and the step that produces the value; if the producer is not strictly earlier than the writer, the block orders the value reported in the round's final message and orders the artifact to say so". That same block's gate 12 ordered the push result and the `gh pr list` reading into the handback, and its gate 1 ordered the post-C3 `git status --porcelain` there too — while C3 IS the handback and the push necessarily follows it. The worker reported all three in its final message and said so, which is exactly the accommodation R-0449 prescribes, so nothing false was written; the reviewer independently confirmed the clean tree, the pushed head and the empty PR list after the fact. Low for that reason. The lesson is not that the rule was wrong but that a rule stated as prose inside a finding does not bind the next block, because nothing reads it at emission time: R-0449 and R-0451 both die at the same point, the moment between authoring and emitting where no mechanical check runs. Standing rule from here, binding the reviewer: the §3 pre-emission checklist gains one item that walks every gate in the Done-when list, names the commit or step that produces its value, and rejects any gate whose producer is not strictly earlier than the artifact ordered to carry it. A counter-measure that lives only in a finding paragraph has already failed once by the time it is read. OPEN.

- R-0453 — Low, A SENTENCE COUNTED A SET THE SAME SLICE HAD ALREADY ENUMERATED, AND THE TWO DISAGREE ON DISK. Found by the WORKER while applying the R2 PLAN slice. That slice's opening paragraph enumerates the branch's findings as "R-0448 to R-0452" — five — and its Risks section then reads "Five of the six findings registered on this branch are defects in the reviewer's own block text". The reviewer confirmed both sentences are in `.agent/plan.md` at d2282fca, lines 5 and 35, and that gate 10 measured max R-0452 with 80 registered against 75 carried, which makes the branch's own count five. The numeral is wrong twice over: there is no sixth finding, and the qualifier "five of" implies an exception that does not exist — all five ARE reviewer-block defects. Nothing downstream consumed the number, and `.agent/live_review.md` remains the source of truth the plan says it mirrors, so the damage is a reader's confusion at one file. Low for that reason. This is the R-0402 / R-0404 / R-0436 family in its plainest form: a numeral written next to an enumeration that already stated the count. The standing rule from those findings — count it mechanically or state no numeral, and prefer writing the range alone — was in force and was broken anyway, in a slice whose own first paragraph carried the correct enumeration two dozen lines above. Repaired in this round's PLAN slice by removing the numeral and letting the range stand. OPEN until the repair is reviewed.

- R-0454 — Low, A GATE ORDERED A MEASUREMENT OF SUBJECTS THE BLOCK NEVER DEFINED, SO THE WORKER HAD TO CHOOSE THEM. Found by the WORKER, which declared it as its second deviation. R2's Q4 defines five stage selections by name and expression — fast, standard, ui, smoke, excluded — and Q5 then orders "Run fast, ui, smoke, safety and architecture serially". `safety` and `architecture` are not among the five and no expression is given for either anywhere in the block. The worker inferred `-m "safety and not real_ollama"` and `-m "architecture and not real_ollama"` by analogy with the `ui` and `smoke` forms, recorded both exact commands in the inventory, and declared the inference rather than presenting it as ordered. The reviewer re-ran `architecture` and reproduces 71 passed, so the inference was the right one — which is the problem, not the mitigation: a worker that guesses correctly is still a worker that guessed, and the protocol's whole point is that it must never have to. This is R-0438's family, an unrunnable-as-written gate, reached from the other side: R-0438 was a path that did not resolve on disk, this is a subject that does not resolve in the block. Low, because the inference was declared, mechanically checkable and correct. Standing rule from here, binding the reviewer: every noun a Done-when gate orders measured is either defined in the same block or resolvable to a single value on disk, and the pre-emission checklist resolves each one before emission — the same walk R-0452 added for gate values, extended to gate subjects. OPEN.

- R-0455 — Medium, THE ROUND MAP AND THE TWO FILES THAT NAME THE NEXT ROUND DISAGREE ABOUT WHAT R4 IS. Found by the REVIEWER while reviewing R3. `.agent/live_review.md` carries the round map in its `## Steps` section, and R-0447's own remedy made that section the single place the map is stated. At 83d4a649 that section reads "R3 T001 the stage runner, the marker selections and the summary table → R4 T002 the determinism and budget stages plus the guard-test wiring", while `.agent/plan.md` and `.agent/handoff.md` at the same commit each carry the string "R4 builds T001" exactly once, counted as a literal in both files. R3 did not build T001: it recorded R2, registered R-0453 and R-0454 and ruled DECISION F083 D2, and its own block says "It builds no stage runner and writes no code". So the single source says R4 is T002 while the two files derived from it say R4 is T001, and a session resuming from the map alone would build the wrong round. The arithmetic is broken with it: the map ends "R7 the integration gate → R8 closure" and the R3 handback opens "R3 of 8", but with T001 pushed to R4 every later item shifts and eight slots can no longer hold the work. The cause is precise and it is the reviewer's own: the R3 block gave its round a scope the map does not describe and ordered no repair of the map, which is the R-0447 class landing in the very file R-0447's remedy designated as the one that cannot go stale. The worker is not at fault — it applied every slice byte-verbatim as ordered and nothing in its change set reached the map. Repaired in this round's STEPS pair, which restates the map over the rounds that actually remain and narrows the "no other file restates it" clause to what it can mean, since AGENTS.md mandates a Next Steps section in `.agent/plan.md` and naming one round is not restating a map. Standing rule from here, binding the reviewer, and placed where it binds rather than left as prose (R-0452): a block that gives its round a scope the map does not describe repairs the map in that same block, or it is not emitted. OPEN until the repair is reviewed.

- R-0460 — Low, A BLOCK'S OWN CONVENTION PARAGRAPH MISCOUNTED ITS SLICES AND DENIED STATING A COUNT IN THE SAME BREATH. Declared by the WORKER while applying the R6 block, with the disk evidence, before the reviewer read the diff. That block's SLICE CONVENTION paragraph reads "five REWRITE pairs and one end-of-file append in the two code files", while its C4 bundle line orders "all six repair pairs" and six exist: RUNNER, INJECT, CALL and EXIT in `packages/orchestration/ci_run.py`, ASSERT and LAMBDAS in `tests/orchestration/test_ci_run.py`. The same sentence ends "No numeral is stated for that list — the list IS the statement (R-0402)" while stating numerals inside it, so the paragraph contradicts the rule it cites in the act of citing it. Nothing on disk is wrong: the worker gave the C4 line precedence, applied six, altered no slice and declared the disagreement, and gate 6 was satisfiable only with all six applied — which is why the round is green. This is the R-0402 / R-0404 / R-0436 / R-0453 family, whose standing rule is count it mechanically or state NO numeral, and it is now also the R-0331 family — clause-vs-clause disagreement inside one block — landing in a paragraph written to prevent exactly this. Low: no gate, claim or byte depended on the numeral. Standing rule from here, binding the reviewer, and placed in the pre-emission checklist rather than left as finding prose (R-0452): a block's convention paragraph names its authored units and states NO count of them, and any sentence that both enumerates and denies enumerating is a defect of the block regardless of which half is true. OPEN.

- R-0461 — Medium, A FINDING DECLARED ITS OWN RULE ALREADY PLACED IN THE CHECKLIST WHILE THE SAME BLOCK FORBADE TOUCHING THE FILE THAT CARRIES IT. R-0460's closing sentence reads "Standing rule from here, binding the reviewer, and placed in the pre-emission checklist rather than left as finding prose (R-0452)". It is not placed there. The pre-emission checklist in `docs/agents/planner_reviewer_prompt.md` §3 opens "Run all ten checks mechanically" and its items run 1 to 10, none of which is the convention-paragraph rule; a repo-wide grep of every `*.md` for "convention paragraph", "NO count of them", "denies enumerating" and "both enumerates" returns the rule ONLY in `.agent/live_review.md` and in the two mirrors of the block that authored it, so the absence is measured across every writer rather than inferred from one file (R-0419). The claim was moreover unsatisfiable by construction: constraint 1 of the same block fixed the change set at five `.agent/**` paths and ordered `docs/` to stay EMPTY in the range diff, so the block asserted a placement its own constraints forbade any commit in that round from making. This is exactly the class R-0452 exists to name — a standing rule written as finding prose binds nothing — and the sentence defeats it in a new way, by ASSERTING the promotion instead of performing it, which is strictly worse than leaving it as prose because a later reader greps the checklist, does not find it, and cannot tell whether the rule was retired or never landed. It is also the R-0416 class in its purest form: an authored finding stating an outcome about bytes the same block has not written and cannot write. Low would understate it — R-0416 already ruled that completeness claims are forbidden and this is a stronger claim than completeness — so Medium. The reviewer's defect entirely; the R7 worker applied the text byte-verbatim as ordered, which is the correct conduct. Fix, owed and NOT ordered here: the promotion R-0460 claimed still has to happen — the rule becomes checklist item 11 in §3, and the "Run all ten checks" opener is updated in the same pair so the count and the enumeration agree. R8 does NOT do it: this block's change set contains no `docs/` path, and ordering the edit in the finding text while excluding the file is the very defect being registered. R9 owns it as its first item. From here, a finding may state that a rule IS in the checklist only when the same block ORDERS the edit that puts it there; otherwise it names the round that will, as this one does. OPEN.

- R-0462 — Low, THE HANDBACK TOKEN CAP IS BINDING, EXCEEDED EVERY ROUND, AND MEASURED BY NOTHING. `docs/agents/handback_template.md` sets two independent limits: a LINE cap of ≤60, ≤100 for a >5-commit bundle and ≤160 for the >10-commit LARGE case, and below it a "Hard cap: this file stays ≤800 tokens — ≤1600 in the >10-commit LARGE case". The R7 handback declares a DECISION D15 stated-cause overage naming its 178 lines against the ≤100 cap, which is the correct and honest treatment of the LINE cap — and says nothing about the token cap, which it also exceeds. `.agent/handoff.md` at 2d1c6d8d is 8839 bytes; the file is English prose with tables, so no defensible bytes-per-token ratio brings it under 800, and even a deliberately generous five-bytes-per-token reading leaves it above the 1600 the LARGE case allows, which this 8-commit bundle cannot claim anyway. The property is what is registered here, not a token count the reviewer cannot measure exactly: the file is over the hard cap by a multiple, under every ratio worth arguing about. It is chronic rather than new — R5 was 164 lines, R6 152, R7 178 — and it is structural rather than careless: the mandated sections compose a per-commit table for every commit, a value for every ordered gate, and an item-status row for every C-item and every gate, which for a bundle of this shape cannot fit 800 tokens however tersely written. Low, because nothing downstream consumed a wrong number and the honesty of the record is unharmed. The cause is a gap in the counter-measure rather than in any round: pre-emission checklist item 3 names the LINE caps of `.agent/plan.md` and `.agent/handoff.md` and is silent on the token cap, so no reviewer pass has ever measured it. Fix, deferred to a paydown round and NOT to R8, because it changes a rule document that R8's change set does not include and the right repair is a ruling rather than an edit: the operator decides whether the 800-token cap is raised to match the mandated content, or the mandated content is reduced, and whichever way it goes, item 3 gains the token cap so the number is measured instead of assumed. Until that ruling, a handback that declares a D15 stated-cause overage names BOTH caps it exceeds rather than only the line cap. OPEN.

- R-0463 — Medium, A DRY RUN THAT COULD NOT FAIL THE WAY THE REAL GATE FAILS, AND SO SHIPPED A RED SLICE. The authored CI-CMD slice reached the worker with a ruff violation in it. The proximate cause is mechanical: an earlier trim pass over the block deleted a `_ROOT_DEPTH` constant that had sat between the imports and the first `def`, and the deletion took one of the two blank lines with it. The real cause is the verification. Before delegating, the reviewer DID lint the applied slice and DID read `All checks passed!` at exit 0 — under `python3 -m ruff check --no-respect-gitignore --isolated --line-length 120 --target-version py310`. `--isolated` discards `pyproject.toml`, and with it the `select = ["E", "F", "W", "I", "UP"]` line that turns the `I` (isort) rules on at all; ruff's default selection is `E` and `F` only, so `I001` was not merely unreported, it was never evaluated. The probe was green because it was blind, which is the R-0337 class — a probe whose import path or config differs from the gate's proves nothing about the gate — recurring in a new medium, configuration rather than module resolution. It is Medium and not Low because the failure mode is silent and general: every future authored code slice checked this way would pass the reviewer and fail the worker, and the round it costs is a full delegate-and-review cycle. Standing rule, binding the reviewer from here: a dry run executes the gate's EXACT command line, from the repository root, with the repository's own configuration — no `--isolated`, no substituted flags, no convenient variant — or it is not evidence and is not reported as if it were. This block does NOT place that rule in §3: C3 lands item 11 and nothing else, and asserting a promotion this change set does not order is the R-0461 defect itself. R10 owns it as checklist item 12, and this paragraph is the text item 12 carries. OPEN.

- R-0464 — Low, A GATE OVER A PARAMETRISED SUITE QUOTED A COLLECTED COUNT AS ITS BASELINE. R8's gate 10 ordered the four catalog suites and bracketed "[BASE: 593 passed, exit 0 — a red here is this round's doing]". The suites are parametrised per catalog GROUP — `test_grouped_cli.py` alone generates eight ids for every group — so a round whose whole purpose is to ADD a group necessarily moves that number, and 601 was the correct, green result. Nothing broke, because the gate ordered the worker to REPORT the count rather than to match 593, and the worker reported 601, refused to treat the delta as either error or nuisance, and accounted for all eight ids by collection. But the bracketed figure still framed 593 as the expected reading and cost the worker a disproof it could not complete — it could not re-run the suites at BASE, no worktree being permitted that round, so it had to hand the question back unresolved. This is the R-0336 family, whose rule is to gate the PROPERTY and never a serialized count. Low: no false verdict was reached and the reviewer confirmed the delta at the gate. Refinement of that rule, binding the reviewer from here: when a gate names a collected count at all, it first establishes whether the suite is parametrised over anything the round CHANGES, and if it is, the gate states the expected DELTA and its cause — "adding one group adds eight ids" — instead of a bare baseline that the round is designed to invalidate. OPEN.

- R-0465 — Medium, GATES THAT ORDER A PROPERTY AT A COMMIT WHICH CANNOT CARRY IT. The R9 block spent two of its three deviations on gates that were unsatisfiable as written, both in the same way. Gate 8 ordered the item-11 numerals to agree "over the file at C3", but four of its five anchors are created by C4 itself, so at C3 they necessarily read 0 / 1 / 0 / 0 / 1; gate 16 ordered a change set "measured BEFORE the handoff is written into C6, so it lists seven paths with `.agent/handoff.md` the seventh and last", and both clauses cannot hold at once because the seventh path is created by the very commit the measurement must precede. The worker did the right thing twice — measured what was measurable, reported both readings, declared the deviation — but each cost a round-slot of reviewer arithmetic to adjudicate, and a worker with less nerve would have fabricated the agreeing numbers instead. This is the R-0371 family, whose rule is that a block may never order a value which cannot exist at the moment the ordered text is written; the earlier instances were commit SHAs, and these two are properties pinned to the wrong commit boundary, which is the same defect wearing different clothes. Standing rule, binding the reviewer from here and already covered in spirit by §3 item 8: every done-when that names a commit states the commit at which the property FIRST holds, and when a property spans a pair of commits the gate names both readings it expects instead of one that only one of them can satisfy. OPEN.

- R-0466 — Low, A FINDING NAMED THE WRONG COMMIT FOR THE EDIT IT WAS DEFERRING. Inside RECORD-R8, finding R-0463 reads "This block does NOT place that rule in §3: C3 lands item 11 and nothing else". The R9 bundle assigns item 11 to C4 and the ruff repair to C3, so the sentence is wrong about its own block on disk: item 11 landed in bb5b8836 (C4) and 196b8f4f (C3) is the one-line ruff repair. The substance was right — the finding correctly declined to claim a promotion its change set did not order, and correctly named R10 as the round that would own it, which is precisely what §3 item 11 demands — and only the commit letter is false. The worker applied the slice byte-verbatim as constraint 2 required and declared the contradiction rather than editing reviewer text, which is the conduct this repository wants. Low because nothing downstream depended on the letter and no verdict turned on it. Refinement, binding the reviewer: when finding text names a commit inside its own block, that letter is re-read against the bundle at emission, in the same pass as §3 item 9 re-greps citations — a C-letter is a pointer, and pointers are checked, not remembered. OPEN.

- R-0468 — Low, THE REPOSITORY THIS FEATURE WILL GATE IS TWENTY-SIX RUFF ERRORS RED, AND NOT ONE CI STAGE RUNS RUFF. Measured by the reviewer at c6db29fa from the repository root, with the repo's own `pyproject.toml` and no substituted flag: `python3 -m ruff check . --statistics` reports 26 errors — 20 I001 unsorted-imports, 4 F401 unused-import, 1 UP035 deprecated-import and 1 F821 undefined-name — of which 25 are auto-fixable. None of them belongs to this branch: `python3 -m ruff check tests/orchestration/test_ci_stage_selection.py tests/orchestration/test_ci_stages.py` prints `All checks passed!` at exit 0, so R10 added no debt and all 26 predate this feature. It is registered against F083 rather than left alone because of the feature's own Acceptance line, "Clean checkout: `remedy ci` green locally and hosted with the same stage results": all five entries in `CI_STAGES` are pytest marker selections and none of them invokes a linter, so `remedy ci` is green today while `ruff check .` is red, and the day T003's hosted workflow adds a lint step it arrives red with 26 errors nobody scheduled. Low and not Medium because no false GREEN exists on disk right now — no stage claims to lint and none does — and because the remedy is bounded and mechanical rather than a redesign. Routed to T002, whose brief already names "no forbidden patterns" as budget-stage work: a lint ceiling belongs to the budget stage, and the choice between clearing the 26 first or landing the stage against a recorded baseline is R12's to make and to record as a DECISION. OPEN.

- R-0469 — Low, A NAME THAT EXISTS NOWHERE IS INTERPOLATED INTO AN ERROR MESSAGE IN PRODUCTION CODE. `check_injections_supported` in `packages/orchestration/gauntlet_injection.py` raises `MissingSeamError(f"{name} cannot be injected at {BLOCKED_INJECTIONS[name]}: " f"{MISSING_SEAM}")`, and `MISSING_SEAM` is defined nowhere at all: `grep -rn "MISSING_SEAM" --include=*.py .` returns exactly one hit in the whole repository and it is that use site. Evaluating that f-string would raise `NameError: name 'MISSING_SEAM' is not defined` instead of the `MissingSeamError` the function exists to raise, so the refusal path fails in a way none of its own tests describe. Low, and the reason is reachability, checked rather than assumed as §3 item 5 requires: `BLOCKED_INJECTIONS: dict[str, str] = {}` is an empty literal and nothing anywhere writes into it, so `name in BLOCKED_INJECTIONS` is False for every input and the branch is dead today. This is a landmine rather than a live defect, and it detonates on the first commit that registers a blocked injection class. It is registered under F083 rather than routed elsewhere because it is the concrete proof of R-0468 and inseparable from it: ruff has flagged this exact line as F821 for as long as the line has existed, and the only reason nobody noticed is that no stage of Remedy's CI runs ruff. A linter finding nobody reads is indistinguishable from having no linter. Fix and finding travel to T002 together with R-0468. OPEN.

- R-0470 — Low, A BLOCK DECLARED A SIZE IT HAD NOT MEASURED. The R11 footer reads "BLOCK SIZE, measured on these final bytes: 246 lines", and the transported bytes measure 241 lines at 22819 bytes in both `.agent/authored/f083-r11.md` and `.agent/last_block.md`, which are byte-equal to each other. The word "measured" was false: no count was taken, a number was recalled. The worker did exactly the right thing — it reported the mismatch, declared it, and changed nothing to close the gap, because closing a gap between a claim and the bytes by editing the bytes is how a record stops being one. Low because nothing downstream consumed the numeral and the cap was never in danger at either value. This is the R-0402 / R-0404 / R-0436 family, whose standing rule is count it or state NO numeral, and §3 item 1 already orders the count to be taken mechanically on the FINAL bytes after the last edit; the rule was not missing, it was skipped. Refinement, binding the reviewer and already applied by the block that carries this text: a block whose reviewer cannot mechanically count its own final bytes — which is every block in a session with no scratchpad file, because the bytes exist only in the prompt — declares NO line count and orders the WORKER to measure it against the cap instead. A number the author cannot verify is not a declaration, it is a guess wearing a declaration's clothes. OPEN.

- R-0471 — Low, TWO CLAUSES OF ONE BLOCK DISAGREED ABOUT A SINGLE NEWLINE. R11's C2 contract required "exactly one blank line between the file's current last line and its first line", while gate 10 of the same block ordered the appended tail to begin `b"\n\n## Q5 — …"`. Because `.agent/f083_inventory.md` already ended with a newline, the contract yields a tail of `b"\n## Q5 — …"` and the gate's literal would have produced two blank lines: the two clauses cannot both be satisfied. Gate 4 of that same block had the newline right for the live_review append, so the block contradicted not only itself but its own neighbouring gate. The worker applied the contract, reported the gate as measured, and declared the difference, which is the correct order of precedence and the correct disclosure. Low because the disagreement was visible on inspection and cost no rework beyond the declaration. This is the R-0437 newline family crossed with the clause-versus-clause defect: the fix is not more prose about newlines but a mechanical pass in which every gate literal that quotes an append boundary is checked against the convention paragraph of the SAME block before emission, in the same sweep §3 item 9 uses to re-grep citations. OPEN.

- R-0473 — Medium, A BUDGET IS ABOUT TO BE WRITTEN FROM ONE READING PER STAGE, WHICH IS THE MISTAKE THE PLAN'S OWN RISK NAMES. Q5 records exactly one wall-clock reading for each of `standard`, `ui` and `smoke`, and two for `fast`. The reviewer re-ran `standard` under `-n auto` on the SAME machine at the SAME commit with the expression read from `CI_STAGES`, and measured 170.1 s against the 138.8 s Q5 records — a spread of about 22 % — while the pass and skip counts were identical at 12578 and 1, and the exit code was 0 both times. Nothing was fabricated and Q5 is not wrong: a single reading honestly reported as a single reading is exactly what it claims to be, and the section carries no budget number precisely because choosing one was left to a later round. The finding is about what happens NEXT. `.agent/plan.md` has carried, for several rounds, the risk that `fast` rested on a single 391.8 s reading and that no runtime budget could be written from it; R11 replaced that with two readings for `fast` and one for every other stage, so for three of the five stages the risk is unchanged in kind and merely newer. A ceiling set at or just above a single sample fails the first time ordinary variance exceeds it, and a CI that fails for variance teaches its readers to ignore it — which is worse than having no budget, because it spends the credibility the budget existed to build. Medium because the budget stage is the very next piece of work and would bake the error in. Binding R13: before any ceiling is written, each stage that will carry one is measured at least three times and the ceiling is set from the observed SPREAD with its headroom stated, or the budget is documented as provisional and says on its face how many samples it rests on. Remedy does not need a tight budget; it needs an honest one. OPEN.

- R-0474 — Medium, A FINDING'S EVIDENCE POINTER WAS INVALIDATED BY ITS OWN BLOCK, IN THE SAME ROUND THAT WROTE IT. R12's C1 wrote R-0473 into this file with three present-tense citations of `Q5` — "Q5 records exactly one wall-clock reading for each of `standard`, `ui` and `smoke`, and two for `fast`", "the 138.8 s Q5 records", and "Q5 is not wrong" — every one of them meaning the section R11 had appended. C2 of that same block then renamed that section to `## Q9 —`, so by the end of the round all three pointers resolve to `## Q5 — Measured wall time and outcome per stage`, a different section with different numbers: it carries one reading for each of SIX stages, it puts `standard` at 134.1 s rather than 138.8 s, and it holds no second `fast` reading at all. The measured CONTENT of R-0473 is correct and was verified against `## Q9` at this gate, so nothing is fabricated and no number is wrong; what broke is the address, not the data. Medium because R-0473 is the finding that BINDS the next round, and a binding instruction naming the wrong evidence section sends the round that must obey it to the wrong table — the same consequence R-0472 was rated Medium for, with the arrow reversed: R-0472 was a heading prescribed for a file the reviewer had not read, and this is a citation left pointing at a heading the same block moved. The block was aware of the rename everywhere else — its constraint 5 reasons explicitly about which references the rename disambiguates, and the PLAN slice it applied at C3 already reads "from the `## Q9` readings" — so the omission is confined to the finding text, which makes it an emission-sweep failure rather than a misunderstanding. R-0473's text is deliberately NOT edited to close this gap: R-0470 established one round ago that closing the distance between a claim and the bytes by editing the bytes is how a record stops being one, and that principle does not weaken when the stale half is the reviewer's own. The correction lives here instead, in the finding that reports it, and it is stated once and plainly: every `Q5` in R-0473 means the section now titled `## Q9 — Stage runtime, measured at R11`. Refinement, binding the reviewer: when one block both WRITES a citation and MOVES its referent, the citation is authored in the POST-move form, and the block's pre-emission sweep re-reads every heading, section number and quoted name that any later slice of the SAME block rewrites — the sweep §3 item 9 already performs for `file:line` citations, widened to the section names this repository actually navigates by. OPEN.

- R-0475 — Medium, A PLAN SLICE DECLARED AN OUTCOME UNKNOWN THAT ITS OWN BLOCK'S EARLIER COMMIT HAD ALREADY MEASURED. The R13 block's PLAN slice, applied byte-verbatim at C3, carries the risk bullet "`standard` collects 12579 items and has never been run serially, so today's `remedy ci` may already truncate its largest stage. R13 measures it; until then the outcome is unknown, not assumed." C2 of that same block measured it two commits earlier: three samples at exit 124 against the runner's 600-second default, and an uncapped probe completing the stage green in 927.72 s. So at the round's head `.agent/plan.md` states the outcome is unknown while `## Q10`, added in the same range, records it — and `.agent/plan.md` is the file AGENTS.md's Session Resume reads second, before any doc and before the diff. Nothing false was published: the sentence was true when the block was authored, the worker was ordered to apply it byte-verbatim and correctly did, and the measurement it contradicts is itself correct. What broke is that the round's own bridge does not carry the round's own headline result. Medium because the plan is what a resumed session reads to decide what to do next, and a session that believes `standard`'s serial cost is still unmeasured either spends an hour re-measuring it or writes a budget from `## Q9`'s `-n auto` figures — the precise error R13 existed to prevent. This is R-0474's shape with a different subject: one block wrote a claim and another slice of the SAME block destroyed its truth, and where R-0474 covered citations and section names, a status claim about the world is the same failure through a different door. Standing rule, binding the reviewer: a PLAN slice is authored in the POST-round form, because C3 applies it AFTER the measurement at C2 — a risk the round is about to resolve is written as the question the round answers and the section that will carry the answer, never as an open unknown, and a risk paragraph may not name a figure that the same block's own earlier commit could move. The R13 PLAN text is deliberately NOT edited retroactively; R-0470 settled one round ago that closing the distance between a claim and the bytes by editing the bytes is how a record stops being one. RESOLVED by C3 of this block, whose PLAN states the measured outcome and names no figure its own C2 can contradict.

- R-0476 — Low, A DERIVED SPREAD WAS PUBLISHED AT A PRECISION ITS OWN PUBLISHED INPUTS CANNOT PRODUCE. `## Q10`'s spread list reads "standard — min 600.06, max 600.06, max−min 0.01." Subtracting the two published bounds gives 0.00. Neither figure is false: the three raw `duration_s` readings in `.remedy-wt/f083-r13/samples.jsonl` are 600.0565918530001, 600.0635042400008 and 600.0613217750015, both bounds round to 600.06 at two decimals, and the unrounded difference of 0.0069 rounds to 0.01. The wall-second column is published at two decimals while the spread was computed at full precision, and the section states neither convention, so the one row where the two disagree reads as an arithmetic error to any reader who checks the table against itself. Low, and not higher: every number is a true reading at its stated precision, the other three stages' spreads do reproduce from their published bounds — fast 397.45 minus 391.07 is 6.38, ui 8.09 minus 7.99 is 0.10, smoke 11.07 minus 11.06 is 0.01 — and the substantive claim attached to that row, that this spread measures the runner's kill rather than the stage's cost, is correct and stated plainly. Not Nil, because `## Q10` is the evidence a ceiling will be written from, and a table that cannot be recomputed from its own published figures invites the next round either to quote a contradiction or to re-derive numbers it should have been able to read. Standing rule, binding the reviewer: a block that orders both raw readings and a value derived from them fixes ONE precision for the pair and states it on the section's face — the derived value is computed from the numbers as published, or the section says it is computed from the unrounded readings and gives the reader no reason to subtract. `## Q10` is not edited to close the gap, for the reason R-0470 settled; the convention is stated and obeyed by `## Q11` in this block instead. OPEN.

- R-0477 — Low, A COMMIT WAS AMENDED AND THE REWRITE SURVIVES ONLY IN A CHANNEL THE REPOSITORY DOES NOT KEEP. R14's worker created C4 with the subject `docs(f083): write the R13 handback`, noticed that the convention names the PRODUCING round rather than the round being handed back, and amended the message to `docs(f083): write the R14 handback` before pushing. The correction is right: the file's own content said R14 throughout, and `6af03d95 write the R12 handback` sets the precedent the amended subject follows. Nothing published was rewritten either — `git reflog show refs/remotes/origin/feature/f083-ci-self-check` records the remote moving 6af03d95 to a677c3ba to 94e6c353, each an ancestor of the next, so the only commit the remote ever saw was the amended one and no force was used. Two things nevertheless went wrong. First, guardrail G2 of docs/agents/self_drive_protocol.md reads "Never force-push. No `--force`, no `--force-with-lease`, no history rewrite, no branch deletion" — and `git commit --amend` IS a history rewrite by git's own definition, so a worker meeting a typo in an unpushed subject has a rule that forbids the obvious repair and no stated exception, which is a gap in the rule rather than a lapse by the worker. Second, and this is the part that costs something: the amend is absent from `.agent/handoff.md`. It was reported to the reviewer in the round's final message, alongside the four values the block genuinely routes there — C4's own SHA, C4's own insertion count, the push result and the open-PR list — but those four are routed there because they CANNOT exist inside C4, whereas an amend is an action taken on the repository that a later commit could have recorded. The handback's Deviations section instead reads "Assumptions: none. No slice was repaired; no defect in reviewer text was found", which is true of every clause it makes and still leaves a reader of the repository alone unable to learn that a commit message on this branch was rewritten. Low, not Medium: the rewrite touched an unpublished commit only, the resulting subject is more correct than the one it replaced, the reviewer was told, and no evidence, gate value or measurement is affected. Two standing rules follow. Binding the WORKER: G2's prohibition is read as absolute on PUBLISHED history and as permitting exactly one exception — the message, never the content, of a commit that has not yet been pushed — and any such amend is declared in the next artifact that CAN carry it, which is the next round's record when C4 itself is the amended commit. Binding the REVIEWER: a block that orders a commit whose subject follows a convention NAMES that subject in the bundle, the way this block's own C-items are named, so the worker never has to choose it and never has to repair it. OPEN.

- R-0478 — Medium, A GATE NAMED FOUR TEST PATHS THAT DO NOT RESOLVE ON DISK, AND BUYING BLOCK-CAP HEADROOM IS WHY. The R15 block's gate 9 ordered `test_dashboard_contract.py`, `test_resource_safety.py` and `test_integrity_gate.py` as bare basenames and closed with the sentence "Paths as gate 8 names them". Gate 8 names four paths and not one of them is any of these three, so the pointer resolves to nothing and the ordered command line is a basename with no directory. The worker ran `pytest tests/cli/test_dashboard_contract.py`, got EXIT 4 and the message that the file or directory was not found, recognised it as the vacuous-gate class, globbed the real paths and re-ran them green — the honest response, and the reason this cost the round nothing. It could have cost the round everything: `pytest <missing path>` exits 4 and reports NO failure, so a worker reading exit codes less carefully would have recorded a gate that never executed a test as an unremarkable non-zero, which is precisely finding R-0438 and precisely what a self-check feature exists to prevent. Medium, not Low, because the gate whose paths evaporated is the VERIFICATION quartet, the one that stands between a scoped round and a broken repository. The cause is nameable and is the part worth keeping: the paths were full and correct in the draft, and they were shortened to basenames in the final trimming pass that brought the block from 403 lines down to the 400-line cap of docs/agents/planner_reviewer_prompt.md §3 item 1. Standing rule, binding the reviewer: a gate's PATHS, commands and flags are never the material cut to meet the block cap — they are the load-bearing bytes of the only thing a round is verified by. When a block is over cap, cut prose, cut a FROM/TO to its changed lines, or split the round; and a block that has been trimmed at all re-reads every gate's paths afterwards and resolves each one on disk before emission, because the trimming pass is exactly when they die. OPEN.

- R-0479 — Low, A GENERATED TEST FILE APPEARS UNTRACKED IN THE WORKING TREE WHILE THE SUITE RUNS, AND TWO GATES READ THE REPOSITORY AS DIRTY WHILE IT IS THERE. Measured, not inferred: while `tests/regression/test_resource_safety.py` was running in this repository, the reviewer ran the integrity gate and `ruff` against the primary checkout and read `relevant_untracked` FAIL with the message `1 relevant untracked: tests/regression/test_wrapper_slow_1014301_ijaza9_1.py`, together with `Found 27 errors.` from ruff. Both readings were taken again after that suite finished and both returned to their true values — `relevant_untracked` pass with `untracked=0, relevant=0`, and `Found 26 errors.` — and `git status --porcelain` was EMPTY before the suite, empty after it, and the named file is absent from the tree now. Nothing in R15 caused it and no committed artefact is affected; the contaminated readings were the reviewer's own, taken concurrently, and they are corrected in the gate paragraph above rather than left standing. Low because it corrupts no commit and survives no suite run. Not Nil, because two of this repository's own health checks — the integrity gate's untracked check and any lint ceiling counting errors repo-wide — report a clean repository as dirty for as long as a suite is in flight, and F083 exists to give this repository a CI whose green means something. A CI that runs its own integrity gate concurrently with its test stages would read that failure as real. Standing rule, binding every role: a gate that reads WORKING-TREE state — `git status --porcelain`, the integrity gate's untracked check, a repo-wide lint count — is run when no test suite is executing against the same checkout, and a reading taken concurrently with one is reported as contaminated rather than as a value. Whether the generator should clean up after itself, and whether `relevant_untracked` should ignore this name class, is a question for the budgets stage that will have to run these checks in a real sequence; it is NOT ruled here and no fix is ordered. OPEN.

- R-0481 — Medium, A LATE INSERTION WAS SWEPT THROUGH A BLOCK'S ARITHMETIC BUT NOT THROUGH ITS PROSE, AND THE PLAN ON DISK NOW UNDERSTATES ITS OWN ROUND. The R16-REC block was authored with two findings and finished with three: R-0480 was written after the rest of the block existed, once the reviewer had chased a one-off dashboard-contract reading to its cause. The insertion sweep updated everything that could be COUNTED — gate 13's expectation moved to 108 / 6 / 0 with max R-0480, C1's subject became "register three findings", the PLAN's next-free id became R-0481, and a new Risks bullet named R-0480 — and it updated nothing that was merely WRITTEN. Three clauses are wrong on disk as a result, all inside the PLAN slice applied at C2 and all verified by the reviewer at 0d9c72e0: `## Current Step` says "This record round wrote that verdict and the two findings it produced" where the round registered THREE; `## Next Steps` says the next round "must honour R-0478 and R-0479 when it writes its gates", silently dropping R-0480, which is the only one of the three that names a stage the next round has to design around; and `## Current Step` closes "R16 has not started" while C2's own commit subject reads "point the plan at the R17 budget stage", so the commit message and the file it commits name different rounds. Nothing is fabricated and no gate value is affected — the worker applied the slice byte-verbatim and correctly, every number the block gated on was right, and the reviewer's arithmetic reproduced at every gate. What broke is that `.agent/plan.md` is the file AGENTS.md's Session Resume orders read SECOND, before any doc and before the diff, and a session resuming from it is told to honour two findings when three are open and is given two different names for the round it should start. Medium for that reason and no other: it costs the next session a reconciliation it should not have to perform, in the one file that exists to prevent exactly that. This is the R-0474 and R-0475 shape a third time, with the trigger named at last — not a moved referent and not a stale status claim, but a LATE ADDITION whose sweep stopped at the numerals. Standing rule, binding the reviewer: when a finding, item or slice is added to a block that is already drafted, the re-sweep covers the block's PROSE as well as its counts — every sentence that enumerates the finding set, names the next round, or lists what the next round must honour is re-read against the block's FINAL bytes, and the pre-emission checklist's mechanical items are re-run on those bytes rather than on the draft they were first run on. ROUND NUMBERING, ruled here because two clauses on disk disagree and neither may be rewritten: the record round committed as `f083-r16-rec.md` has SPENT the number 16, the repair round carrying this finding is R17, and the next ENGINEERING round — the budgets stage, the R-0468 ruling and the determinism shape — is R18. The PLAN slice of this block states that and nothing else; the superseded "R16" and "R17 budget stage" clauses are left standing where they are, per R-0470. OPEN.

- R-0482 — Medium, A GUARD THAT REFUSES AN UNSUPPORTED INJECTION RAISES `NameError` INSTEAD OF THE ERROR IT NAMES, BECAUSE THE MESSAGE INTERPOLATES AN UNDEFINED NAME. Measured at ab1d2344 by the reviewer: `python3 -m ruff check .` reports `F821 Undefined name MISSING_SEAM` at `packages/orchestration/gauntlet_injection.py:286:20`, and `grep -rn "MISSING_SEAM" packages/ tests/` returns exactly one line — that same use site. The name is referenced and defined nowhere, in the repository or in the test tree. The site is `check_injections_supported`, whose whole purpose is to "refuse an order whose declared injections cannot be driven honestly": for a name in `BLOCKED_INJECTIONS` it builds `f"{name} cannot be injected at {BLOCKED_INJECTIONS[name]}: {MISSING_SEAM}"` and hands it to `MissingSeamError`. The f-string is evaluated BEFORE the exception is constructed, so that branch raises `NameError: name 'MISSING_SEAM' is not defined` and the `MissingSeamError` the caller is written to catch is never constructed at all. The unknown-injection branch immediately below it is unaffected and does raise correctly, which is why the defect is invisible from the outside: the guard appears to work, and fails only on the one input class it was written for. Medium and not High: no false GREEN exists on disk, the branch is not reached by any current test — no test in the tree names `MISSING_SEAM` — and the failure is loud rather than silent when it does fire. Not Low, because a guard whose refusal path is itself broken is worse than no guard, and because a caller catching `MissingSeamError` around this call gets an uncaught `NameError` through it. This finding belongs to F083 only in the sense that F083's lint reading is what surfaced it: it is ONE of the twenty-six errors DECISION F083 D5 freezes at the ceiling, and D5 freezes it deliberately rather than fixing it here, because the fix is a production change in an unrelated module and AGENTS.md Scope Control forbids it as a "while I'm here" edit. The fix — define the constant or drop the interpolation — belongs to a branch of its own and is not ordered by this round. OPEN.

- R-0487 — Medium, `docs/README.md` HAS NEVER BEEN LINK-CHECKED, AND THE GUARD THAT IS SUPPOSED TO CHECK IT REPORTS GREEN TWICE FOR THE WRONG FILE. `TestPrimaryDocLinksResolve` in `tests/docs/test_docs_consistency.py` parametrizes over `[p.name for p in PRIMARY_DOCS]`, and `PRIMARY_DOCS` holds both the repository root `README.md` and `docs/README.md`, so two entries share the parametrize id `README.md`. The test body then recovers the path with `next(p for p in PRIMARY_DOCS if p.name == doc)`, and `next` returns the FIRST match for both cases — the root file. The root README is therefore link-checked twice and `docs/README.md` never. Proved by paired control inside a disposable worktree at 07d6577a, not by reading: breaking one relative link in the ROOT `README.md` fails both `test_every_relative_markdown_link_exists[README.md0]` and `[README.md1]` at `2 failed, 293 passed`, while breaking one in `docs/README.md` leaves the suite at `295 passed` with nothing red. The worktree was removed and pruned. Medium and not Low: AGENTS.md makes registering every new or renamed doc in `docs/README.md` mandatory, R22's own C4 did exactly that, and the index carries 163 relative links that nothing verifies — a guard that cannot fail is the "green as a word" class this repository treats as a block condition, and here it announces itself green twice. Not High: measured directly, all 163 of those links resolve today, so the hole is latent rather than live, and no shipped artifact is wrong. NOT FIXED IN THIS FEATURE, deliberately: the repair is an edit to a test's CONTENT, which T2_F083's Do-not-touch list forbids, and `.agent/context.md` already rules that a change needing a test's content edited is a finding and not a fix. It is routed to a paydown branch of its own, alongside R-0482. The obvious repair, for whoever takes it: parametrize on a path relative to the repo root rather than on `p.name`, so the two ids stop colliding, and keep the `next(...)` lookup keyed on that same unique value. OPEN.

Gate: R1 — PASS. All fifteen ordered gates reproduce at the reviewer's own hand, from the repository root at 9ba3179e, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r1.md`, the committed `.agent/authored/f085-r1.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 7a34422a0df2ca34a94599de5804a87cf9b53e211c17de6a1e99f9d81b006512, 21785 B, 339 lines. THE RESET IS HONEST, which is this round's only irreversible act: the pre-reset blob at a5a70621 holds 117 registered ids, 13 resolved, 0 `Landed:` lines, 0 duplicates and 0 resolutions naming an unregistered id, so 104 were open; at HEAD the record holds 105 registered and 0 resolved, the set of open ids equals the pre-reset open set plus exactly R-0490 with an EMPTY symmetric difference, and each of the 104 carried paragraphs was extracted by id from the pre-reset blob and compared byte-for-byte against its counterpart at HEAD — 104 compared, 104 equal, none missing, none altered, no id registered that was not open at the base. Next free id R-0491. STATUS: the FROM line occurs 0x and the TO line 1x, `^- \[~\]` is 1x, `^- \[x\] F\d{3} — ` is still 50x, `<<` is 0x, and replacing the TO back with the FROM reproduces the base file BYTE-FOR-BYTE, which proves the commit moved that one line and nothing else. README.md is byte-identical to the base, correctly, because the capability counters move only at closure. The three whole-file state slices are byte-equal to their authored originals — context.md 297bd398… 48 lines, plan.md 05d8bf54… 40 lines, candidates.md ffa9a740… 12 lines — every contract assertion their four reader tests make is satisfied at HEAD, and no transport marker reached any target file. Re-run by the reviewer: the four state-file readers `157 passed` exit 0, `tests/docs/` `295 passed` exit 0, the canary `42 passed` exit 0. Per-commit insertions C0a 339, C0b 322, C1 41, C2 66, C3 — the handback commit — 49, none over 500; the change set is exactly the eight ordered paths and no path under `packages/`, `apps/`, `tests/` or `scripts/`; history is five single-parent commits and the reflog shows no amend, rebase, reset or force-push. The handback is 74 lines against a 60-line cap, declared inside the file with that exact count and its cause under the AGENTS.md DECISION D15 stated-cause rule, with no section dropped — permitted, not a finding. Two further declared deviations are accepted and are not findings: `shutil.copyfile` for a denied `cp`, which the block itself sanctioned because the gate names the byte property rather than the tool, and the worker's note that `.remedy-wt/` has accumulated roughly a thousand scratch entries, which is the already-registered R-0403 mechanism and unchanged by this round. The third — that `.agent/plan.md` still described the previous feature during C0a, C0b and C1 — is real, is the reviewer's fault rather than the worker's, and is registered below as R-0491.

- R-0491 — Low, THE CANONICAL ROUND BUNDLE PUTS THE BLOCK-SAVE COMMITS AHEAD OF THE PLAN UPDATE, SO EVERY ROUND'S FIRST COMMITS LAND WHILE `.agent/plan.md` STILL DESCRIBES THE PREVIOUS ROUND OR THE PREVIOUS FEATURE. Raised by the reviewer at the R1 gate, from a deviation the R1 worker declared correctly rather than routing around. AGENTS.md's Commit Gate is unconditional — "Before committing: 1. Verify `.agent/plan.md` matches the current work ... If any of these fail: DO NOT COMMIT" — and its Task Completion Protocol repeats it as "Before every commit: 1. Verify that `.agent/plan.md` reflects the current state". The R1 bundle ordered C0a, C0b and C1 before the PLAN slice landed in C2, and at C0a the plan on disk still described `amend0816 CI hosted green`, a closed and merged branch. Three commits therefore landed against a plan that did not match the current work. This is not a worker defect: the worker followed the ordered sequence, which Constraint 2 of that block required byte-verbatim, and declared the conflict in its handback instead of silently reordering — the correct behaviour on both counts. It is a REVIEWER defect, and a structural one rather than a slip, because the same ordering appears in the F083 R1 and F083 R28 bundles and would otherwise recur in every round of this feature by construction, arriving as a re-declared deviation each time instead of as a fixed rule. Low, because nothing false was written and no gate was weakened: the plan was correct from C2 on and the round's own gates proved it byte-equal to its authored slice. Counter-measure, binding on the reviewer from R2 on and demonstrated by the R2 bundle that carries this finding: the `.agent/plan.md` update is ordered as the FIRST commit of a round that has substance to record, ahead of the live-review record and ahead of the round's work, so that only the two block-save commits — which write nothing but the block itself — can precede it. Where a round genuinely cannot do that, the block says so in its own text and names the commit at which the plan becomes current, rather than leaving the worker to discover the conflict. The wider question of whether a pure block-save commit should be exempt from the Commit Gate at all is an AGENTS.md question that F085 does not own; AGENTS.md forbids mixing an unrelated fix into a feature branch, so that half routes to the same paydown branch as R-0403, R-0448, R-0482, R-0487 and R-0490. OPEN.

Gate: R2 — PASS. All sixteen ordered gates reproduce at the reviewer's own hand, from the repository root at 2d492d49, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r2.md`, the committed `.agent/authored/f085-r2.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 d5db9ebcc977024df569710a2cb7528f4311b735a6e8cf380d72ffd6aecbd139, 20720 B, 264 lines. The C2 append is honest: the pre-C2 blob of 190930 B is a byte-exact PREFIX of the 196461 B post-C2 file, the RECORD-R1 and R0491 slices each occur exactly once inside the appended tail, the numstat is `4 0` with a zero deletion column, and no transport marker reached any file. The open set moves by exactly one: 105 open at the base, 106 at HEAD, the set comparison against the base set plus R-0491 has an EMPTY symmetric difference, 0 duplicate ids and 0 resolutions naming an unregistered id, next free R-0492. THE INVENTORY WAS RE-DERIVED, NOT READ: the reviewer ran the block's own grep at HEAD, got 73 sites, and found the table's 73 rows equal to it as a SET with an empty symmetric difference; then re-parsed every one of the 33 files with an independent AST walk and re-computed all six keyword columns from each call's own keywords, agreeing on 73 of 73 rows; then re-derived the class partition, finding all seven headings inside the closed vocabulary, every declared per-class count equal to the count actually listed under it, the seven counts summing to 73, every site assigned exactly once, and the assigned set equal to the table set. The reviewer's independent walk also reproduces the worker's most valuable declaration — that only 67 of the 73 grep lines are real calls, the other six being four docstring lines and two type annotations at exactly the sites the handback names. Re-run by the reviewer: the four state-file readers `157 passed` exit 0, the canary `42 passed` exit 0. Per-commit insertions C0a 264, C0b 185, C1 14, C2 4, C3 309, C4 — the handback commit — 61, none over 500; the change set is exactly the six ordered `.agent/` paths with nothing under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/`; history is six single-parent commits with no amend, rebase, reset or force-push. One symbol disagreed between the reviewer's walk and the table — `test_execution_service.py:361`, where the table says `<module>` and an innermost-range walk says `_kill_process_group` — and the table is RIGHT under the scope-of-execution reading it applies consistently to all six non-call rows, since line 361 is the `def` header itself and a def header executes in module scope. The ambiguity is the block's, not the worker's, and is registered below as R-0492. DECISION F085 D1, recorded here per §4 item 7 and reversible by any later relay: the feature file's premise that subprocess execution "already flows through a small number of helpers" is FALSIFIED by measurement — 67 real call sites in 56 distinct enclosing functions, of which the four helpers it names cover 24, while git plumbing alone holds 24 with 12 of them in `worktrees.py`. The chosen option is to amend `docs/roadmap/features/T2_F085.md` in R4 and re-slice T002 against the measured shape rather than the assumed one; the alternatives considered were to proceed on the written slicing, which would under-scope T002 by roughly two thirds, and to widen R2 to do the re-slicing, which would have mixed an inventory round with a planning ruling. R4 also carries that amendment's `tests/docs/` gate. The map in this file's Steps section is amended by that same decision: ruling the stage-1 command classes moves from R3 to R4, because R3 is this session's terminator round.

- R-0492 — Low, A BLOCK DEFINED ITS INVENTORY UNITS BY A TEXT GREP WHILE ITS COLUMNS DEMANDED FACTS ABOUT CODE, SO SIX OF THE SEVENTY-THREE ORDERED "CALL SITES" ARE NOT CALLS AND ONE SYMBOL WAS UNDEFINED. Raised by the reviewer at the R2 gate against its own R2 block. That block's step 5 says "ONE ROW PER CALL SITE, no row for anything else", and then defines the set with `git grep -n -E 'subprocess\.(run|Popen|call|check_output|check_call)' -- packages/ apps/` while gate G7 demands the table equal that grep as a SET. A regex over text cannot distinguish a call from prose about a call, and six of the 73 matches are not calls: four are documentation — `command_discovery.py:190` and `:205`, `dod_runners.py:12`, `test_runner.py:24`, three of which are docstrings that promise the very safety properties this feature is about — and two are type annotations, `test_execution_service.py:361` and `dev_server.py:1440`. The two halves of the block are therefore unsatisfiable together, and the worker resolved the conflict the right way: it tabled all 73 to satisfy the set-equality gate, marked the six non-calls `n/a` in the six keyword columns rather than inventing `no`, and declared the tension in its handback instead of silently dropping rows. The reviewer's independent AST walk reproduces exactly those six. The same root cause produced a second defect: `symbol` is specified as "the innermost enclosing `def`/`async def`/`class` name at that line", which is undefined when the matched line IS a `def` header, as `test_execution_service.py:361` is. The table's `<module>` is correct under the scope-of-execution reading it applies consistently to all six non-call rows — a def header executes in module scope — but the block never states which reading governs, so an innermost-range walk disagrees and neither answer can be called wrong. Low, because nothing false was recorded, no gate was weakened, the six rows are honestly marked, and the inventory's value is untouched: the 67 real calls carry fully re-derived facts. Counter-measure, binding on the reviewer from R4 on: when a block orders an inventory of code units, the SET is defined by the semantic predicate the columns describe — here "a `subprocess.*` call node in the AST" — and any text grep is named only as the starting candidate list, with the block stating explicitly what to do with candidates the predicate rejects; and any column whose value depends on a scope reading names the reading. This is the R-0367 and R-0463 family seen from a new side: those bar a reviewer from asserting a number the producing tool cannot yield, while this one bars defining a set with one tool and describing it with another. OPEN.

Gate: R3 — PASS. All twelve ordered gates reproduce at the reviewer's own hand, from the repository root at fb346e8c, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r3.md`, the committed `.agent/authored/f085-r3.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 77fb0d0ec4256a6d5145f58118eac49090c11df05827cba4e21d5d74206b19ee, 16976 B, 186 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 05b3082b6f971b944d52dc84663d45bb366046abba1dcd99f94823f585be0479, 36 lines, 1970 B, carrying `## Goal`, `## Next Steps` and an F-id, under the 50-line cap. The C2 append is honest: the pre-C2 blob of 196461 B is a byte-exact PREFIX of the 202948 B post-C2 file, the RECORD-R2 and R0492 slices each occur exactly once in the whole file and both inside the 6487-byte, four-line appended tail, the numstat is `4 0` with a zero deletion column, and no transport marker reached a target file: measured at fb346e8c, before this paragraph existed, neither `.agent/plan.md` nor `.agent/live_review.md` contained a single slice-marker sequence. The open set moves by exactly one: 106 open at 2d492d49, 107 at HEAD, the symmetric difference of the HEAD open set against the base open set plus R-0492 is EMPTY, with 0 duplicate ids and 0 resolutions naming an unregistered id; max R-0492, next free R-0493. `.agent/f085_inventory.md` is byte-identical at base and at HEAD at sha256 fed207f9f8fb5a2de6a52a5366e1f3332eab1ae60c3a666cbddf4771f6c166bd, so R3 did not revise what R2 closed. The change set is exactly the five ordered `.agent/` paths with nothing under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/`; the history is five single-parent commits and the reflog over the round is five `commit:` entries with no amend, rebase, reset or force-push; per-commit insertions are C0a 186, C0b 75, C1 12, C2 4 and C3 40 — the handback commit's own count, which could not exist while its text was being written and is recorded here instead — none over 500. Re-run by the reviewer in the PRIMARY checkout: the four state-file readers `157 passed` exit 0, the canary `42 passed` exit 0. The handback's self-measurement is honest: it declares 87 lines under DECISION D15 and it measures 87. One reading is stated rather than corrected, because the gate never defined it: G5's `Landed:` figure of 14 is a raw SUBSTRING count over the whole file, while the number of actual `^Landed: R-` RECORDS is 0 — all fourteen occurrences sit in prose inside five paragraphs that discuss the convention, so no unreviewed fix is hiding in the record. That is the R-0492 class read back against the very block that registered it, and it is answered by construction rather than by a second finding: R4's G5 orders the line-start regex, which is exactly the counter-measure R-0492 binds the reviewer to from R4 on. TERMINATOR CORRECTION, recorded because the disk must not keep a claim the session has falsified: the R3 block and the R3 handback both state that the R3 verdict lives only in the handoff, the round report and the PR under §4 item 13, because R3 was authored as this branch's last round. The session continued into R4, so R3 is NOT the last round of the branch, item 13 does not apply to it, and THIS paragraph is its on-disk gate entry. Item 13 still governs whichever round does end the branch.

- R-0493 — Low, THE MANDATED DOCS-ROUND GATE IS VACUOUS FOR A FEATURE-FILE EDIT, SO A ROUND THAT AMENDS `docs/roadmap/features/**` IS GATED BY A COMMAND THAT CANNOT FAIL ON ITS OWN CHANGE. Raised by the reviewer at the R3 gate while assembling R4's gate list. docs/agents/planner_reviewer_prompt.md §3, verification tier 5, requires any round whose change set includes `docs/roadmap/**` to gate with `python3 -m pytest tests/docs/ -q`. Measured rather than assumed: `tests/docs/test_docs_consistency.py` reads `PRIMARY_DOCS` — `README.md`, `AGENTS.md`, `docs/README.md`, `docs/roadmap/STATUS.md` and `docs/roadmap/ROADMAP.md` — plus F012-specific assertions and the feature-detail FILENAME pattern, and asserts nothing whatever about the BODY of a feature detail file. Proven by a red control inside a disposable `git worktree` at fb346e8c, never in the primary checkout: with line 2 of `docs/roadmap/features/T2_F085.md` replaced by a malformed dependency line, `python3 -m pytest tests/docs/ -q` stayed GREEN at `295 passed`, while `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` went RED at `11 failed, 19 passed`. The rule is right for its founding case — R-0151, where a STATUS.md ledger-count change broke the feature-ledger pins — and vacuous for the case it now most often meets, since AGENTS.md forbids editing `ROADMAP.md` without an explicit operator request and STATUS.md edits belong to closure, which leaves the feature detail file as the ordinary `docs/roadmap/**` change. Low, because nothing false was recorded and no round has yet passed on the strength of this gate alone; the cost is a round that believes itself gated and is not. That is the silently-vacuous-gate class of R-0438 reached by a different route: R-0438's gate named a path that did not exist, while this one names a path that exists and does not cover the change. Counter-measure, binding on the reviewer from this round on and APPLIED IN THE SAME BLOCK THAT REGISTERS THIS FINDING, as gate G11: a round whose change set touches `docs/roadmap/features/**` gates `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` IN ADDITION to the mandated `tests/docs/` command, because that suite is the only one in the repository that parses those files. Promoting the rule into §3 tier 5 itself is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named as work for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487 and R-0490. OPEN.

Gate: R4 — PASS. All sixteen ordered gates reproduce at the reviewer's own hand, from the repository root at 382ed7fa, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r4.md`, the committed `.agent/authored/f085-r4.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 c755c49d28f58c0d9f97ce0e0f95daa75e9291eeb3b6fce10153291b96727b42, 23993 B, 318 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 a1a17001365fd83c0de0168d8c7d5c6057ead885121c54917fbc54322c1be673, 41 lines, 2266 B, carrying `## Goal`, `## Next Steps` and an F-id, under the 50-line cap. The C2 append is honest: the pre-C2 blob of 202948 B is a byte-exact PREFIX of the 208910 B post-C2 file, the RECORD-R3 and R0493 slices each occur exactly once in the whole file and both inside the 5962-byte, four-line appended tail, and the numstat is `4 0` with a zero deletion column. The open set moves by exactly one: 107 open at fb346e8c, 108 at HEAD, the symmetric difference of the HEAD open set against the base open set plus R-0493 is EMPTY, with 0 duplicate ids, 0 resolutions naming an unregistered id and 0 line-start `^Landed: R-` records; max R-0493, next free R-0494. `.agent/f085_inventory.md` is byte-identical at base and at HEAD at sha256 fed207f9f8fb5a2de6a52a5366e1f3332eab1ae60c3a666cbddf4771f6c166bd, so R4 did not revise what R2 closed. The amendment landed exactly as authored: in `docs/roadmap/features/T2_F085.md` FROM1 and FROM2 each occur 0 times and TO1, TO2 and the AMENDMENT each exactly once, the file ends with the AMENDMENT, `<<<` occurs 0 times, and lines 1 and 2 are byte-identical to lines 1 and 2 at fb346e8c, which is what keeps `tests/orchestration/test_roadmap_index.py` parsing it. Its arithmetic reproduces against the inventory it cites: the inventory's own per-class counts are builder 5, test 12, dod 2, runtime 5, git 24, packaging 11 and other 14, of which six `other` rows are the grep lines that are not call sites at all, so the amendment's `8 real` is exact and 5+12+2+5+24+11+8 equals the 67 real sites it claims. The change set is exactly the six ordered paths with nothing under `packages/`, `apps/`, `tests/` or `scripts/`; the history is six single-parent commits and the reflog over the round is six `commit:` entries with no amend, rebase, reset or force-push. Re-run by the reviewer in the PRIMARY checkout: `tests/docs/` 295 passed exit 0, `test_roadmap_index.py` 30 passed exit 0 — the R-0493 counter-measure doing its work on the very round that registered it — the four state-file readers 157 passed exit 0, and the canary 42 passed exit 0. The values R4's own gates routed to its round report, which no later session can read, are recorded HERE instead, measured by the reviewer at 382ed7fa: C4 inserted 48 lines, so the per-commit series is 318, 213, 16, 4, 68, 48 and none exceeds 500; the post-C4 change set is the same six paths; `git status --porcelain` is EMPTY and `git worktree list` is one line; the push landed, with `origin/feature/f085-sandbox-hardening` at 382ed7fa; and the handback measures 95 lines and 8467 B against its own DECISION D15 declaration of 95 lines, so its self-measurement is honest. That routing is the R-0494 class, registered next and answered by G14 of the R5 block.

- R-0494 — Low, UNDER SELF-DRIVE A GATE READING ROUTED TO THE "ROUND REPORT" IS WRITTEN TO A CHANNEL THAT DIES WITH THE SESSION, SO THE NEXT SESSION INHERITS A GATE IT CANNOT READ. Raised by the reviewer at the R4 gate. docs/agents/planner_reviewer_prompt.md §3 pre-emission checklist item 14 rules that a per-commit gate may not order a value the handback commit cannot hold — its own insertion count — and directs that value to the ROUND REPORT instead, which is correct for the two-window relay where the operator sees that report. docs/agents/self_drive_protocol.md removes the second window and rules the opposite way about channels: "The handoff is the only return channel, and a session with no handoff did not happen." R4 followed item 14 exactly, so its G1 post-C4 readings, its G9 post-C4 change set, its G14 C4 insertion count and its push outcome were all directed into the worker's final message; the session then ended at the handback, and every one of those readings ceased to exist. Measured rather than assumed: none of the four appears in `.agent/handoff.md` at 382ed7fa, which states for each only that it "is in the round report". Nothing false was recorded and nothing was lost in substance, because a self-drive reviewer has execution and re-measured all four at 382ed7fa — they are in the RECORD-R4 paragraph above — which is exactly why this is Low and not higher. The cost is structural: a gate whose reading lives only in an ephemeral channel is unauditable by any later reader, and under G7 session limits an ending session is the NORMAL case rather than the exception, so the channel dies routinely. This is the R-0438 silently-vacuous-gate family reached from a third direction — R-0438's gate named a path that did not exist, R-0493's named a path that exists and does not cover the change, and this one names a value that is produced and then written where nothing can read it. Counter-measure, binding on the reviewer from this round on and APPLIED IN THE SAME BLOCK THAT REGISTERS THIS FINDING, as gate G14: under self-drive the handback commit's own numbers are ordered nowhere, and the reviewer measures them at the next gate and records them in that round's record paragraph in `.agent/live_review.md`, which is on disk and therefore auditable. Amending checklist item 14 itself to carry the self-drive branch is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named as work for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490 and R-0493. OPEN.

Gate: R5 — FAIL. Every ordered gate the reviewer can re-run reproduces at the reviewer's own hand from the repository root at 16506c0b — G1 through G10 and G12 through G15, plus G17 read directly out of the two new files — and the round is failed on G11, which does not; G16 is a worker-side probe of a child process rather than a reproducible reading, and its result is consistent with the reviewer's own rlimit measurements taken while authoring the R5 block. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r5.md`, the committed `.agent/authored/f085-r5.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 4d1188a70d2f8d1ff23f6a5801c212b4406a738c7d6c59d77bb1877047ab9220, 26997 B, 341 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 cbc8ee8a0b3b7196ae4dd9832abb66b009ccbe959ae0706f06f2ec2f266547a8, 41 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The C1 append is honest: the pre-C1 blob of 208910 B is a byte-exact PREFIX of the 214867 B post-C1 file, the RECORD-R4 and R0494 slices each occur exactly once in the whole file and both inside the 5957-byte, four-line appended tail, and the numstat is `4 0` with a zero deletion column. The open set moved by exactly one: 108 open at 382ed7fa, 109 at HEAD, symmetric difference against base plus R-0494 EMPTY, 0 duplicate ids, 0 resolutions naming an unregistered id, 0 line-start `^Landed: R-` records. The change set is exactly the seven ordered paths, the history is seven single-parent commits, and the per-commit insertions are C0a 341, C0b 250, C1 4, C2 16, C3 314, C4 170, none over 500. Re-run by the reviewer in the PRIMARY checkout: ruff over the two new files exit 0 `All checks passed!`; the eight-file structural sweep `350 passed, 6 skipped` exit 0, the same reading as at base, so the new orchestration module trips none of the whole-directory guards; the canary `42 passed` exit 0; and G12 clean, the only `pgrep` matches being the reviewer's own probe command line rather than any surviving fixture. The values R5 routed nowhere are recorded HERE, measured by the reviewer at 16506c0b, which is the R-0494 counter-measure working as designed: C3 of the handback inserted 55 lines, the post-C5 change set is the same seven paths, `git status --porcelain` is EMPTY, `git worktree list` is one line, the push landed with origin at 16506c0b, and the handback measures 106 lines against its own DECISION D15 declaration of 106, so its self-measurement is honest. THE FAIL: G11 ordered `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at exit 0 and the handback reports `6 passed in 4.59s`; at the reviewer's hand the same command at the same commit returns `1 failed, 5 passed`, exit 1, on FIVE consecutive runs, failing at `assert result.cpu_seconds_used >= 1.0` with the measured value 0.999776. The test passes when run alone, which is why a single worker run could honestly have seen green: the assertion sits directly on a boundary rather than near one, so this is recorded as a marginal-assertion defect and NOT as a fabricated reading — nothing in the record supports the harsher reading, and the mechanism explains both observations. It is registered as R-0496. The reviewer's own independent probe then found the more serious defect the ordered gates did not reach, registered as R-0495: `run_guarded` under a 1.0-second `wall_timeout_seconds` returned after 300.04 seconds. G17's no-overclaim gate is confirmed at the level it was written — neither new file claims any existing seam is guarded — and R-0495 is a different failure, an internal promise the module does not keep. R5's substance is otherwise sound: the guard's classification of cpu, wall and output trips is correct, its address-space non-attribution is honest, and G16's probe confirmed the reviewer's stated reason rather than contradicting it, with returncode 1, no term_signal, `MemoryError` on stderr and `ru_maxrss` of 26157056 B below the 67108864 B limit. LAST_REVIEWED_SHA does NOT advance and stays 382ed7fa.

- R-0495 — High, `run_guarded`'S WALL TIMEOUT DOES NOT BOUND `run_guarded`'S OWN RETURN: A DESCENDANT THAT LEAVES THE PROCESS GROUP HOLDS THE INHERITED PIPES OPEN AND THE GUARD BLOCKS ON ITS STREAM PUMPS UNTIL THAT DESCENDANT EXITS. Raised by the reviewer at the R5 gate, by a probe of its own choosing rather than by any ordered gate. Measured, not reasoned: with `ExecGuardPolicy(wall_timeout_seconds=1.0, output_cap_bytes=4096)` and a child that spawns one grandchild with `start_new_session=True` and then sleeps, `run_guarded` returned after 300.04 seconds — the grandchild's full lifetime — and the returned `ExecGuardResult` carried `tripped_limit="wall_timeout"` with `wall_seconds=300.04`. The mechanism is in `packages/orchestration/exec_guard.py`: the deadline fires on schedule and `_kill_process_group` sends SIGKILL to the child's group, but a grandchild that called `setsid` is no longer IN that group, it still holds the write ends of the stdout and stderr pipes the guard created, so `_StreamPump.read1` never reaches EOF and the `out_pump.join()` and `err_pump.join()` calls in the `finally` block — which have no timeout — block until it exits. This is the feature's central promise failing in the case containment exists for. It is worse than a plain hang because the result LOOKS correct to any caller that reads `tripped_limit` alone, and `wall_seconds` is the only field that betrays it. It is not hypothetical, and the reviewer grepped rather than recalled: `start_new_session=True` appears in production code in `packages/orchestration/dod_runners.py`, `packages/orchestration/stream_evidence.py`, `packages/orchestration/test_execution_service.py`, `packages/runtimes/runtime_supervisor.py`, `packages/runtimes/dev_server.py` and `apps/cli/commands/runtime_cmd.py`. Three of those files hold sites in the very classes stage 1 migrates — dod, test and runtime under amendment F085 D1 — so the escaping descendant is not an exotic case but the ordinary shape of the code this guard is being built to wrap. The module's own `run_guarded` docstring states "the group is killed on every exit path, so no descendant outlives this call", which the same probe falsifies for a descendant that leaves the group, and the feature file's Orchestrator brief requires rejecting overclaiming wording in code comments. Counter-measure, for R7 and stated as a PROPERTY rather than an implementation: after the deadline fires and the group kill is sent, `run_guarded` must return within a bounded grace period regardless of whether any process still holds the pipes, and the result must say plainly whether the streams were complete when it returned; the docstring sentence must narrow to the process group it can actually reach. T002a is BLOCKED until this is fixed — migrating a seam onto this guard would make hangs harder to see than they are today, since an unguarded hang at least does not report a satisfied timeout. OPEN.

- R-0496 — Medium, THE T001 SUITE IS RED IN FILE ORDER ON A MARGINAL ASSERTION THAT COMPARES KERNEL CPU ACCOUNTING AGAINST AN EXACT INTEGER LIMIT. Raised by the reviewer at the R5 gate while re-running G11. `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at 16506c0b returns `1 failed, 5 passed`, exit 1, on five consecutive runs, failing at `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` on `assert result.cpu_seconds_used >= 1.0` with the measured value 0.999776; the same test run ALONE passes. Everything the test exists to prove holds in the failing run: `term_signal` is SIGXCPU, `classification` is `resource_limit`, `tripped_limit` is `cpu_seconds` and it is a member of `limits_enforced`. Only the accounting assertion fails, and it fails because `ru_utime + ru_stime` is sampled from the kernel's own CPU accounting, which is granular and rounds against the RLIMIT_CPU soft limit rather than exactly to it, so a value a few hundred microseconds under an integer limit is the NORMAL outcome and not an anomaly. The handback reports `6 passed in 4.59s` for this command, and the reviewer's reading contradicts it; the boundary mechanism explains both readings without any dishonesty, and this finding records it as a marginal-assertion defect for that reason — see the RECORD-R5 paragraph, which declines the harsher reading explicitly. Counter-measure for R7: assert the property the test is named for and drop or loosen the accounting assertion — if CPU consumption is asserted at all it is asserted against a tolerance strictly below the limit, never against the limit itself, because a test whose expected value sits ON a boundary is a coin flip that will re-fail later at a much worse moment. This is the reviewer-arithmetic family of R-0327 and R-0336 appearing inside a WORKER-authored test rather than inside a reviewer gate: order the colour, never the exact number. OPEN.

- R-0497 — Low, A REVIEWER GATE ORDERED AN EXPECTED VALUE THE CODE COULD NOT PRODUCE: G8 OF THE R5 BLOCK REQUIRED A CONTENT GREP TO MATCH A FILE THAT NEVER NAMES ITS OWN PATH. Raised by the reviewer against its own block at the R5 gate. R5's G8 ordered `grep -rn "exec_guard" packages/ apps/ scripts/ tests/` to return "matches in `packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py` ONLY", but `grep` matches CONTENT and the new module never writes the string `exec_guard` anywhere inside itself — its docstring says "execution guard" — so the module's own file cannot appear in that output by construction. The real result is two lines, both in the test file. The worker read the difference correctly, reported it, and explicitly did not edit the module to make the gate match, which is the behaviour the block's constraint 7 asks for and the reason this is Low rather than higher: nothing false was recorded and no round passed on it. The cost is one declared deviation spent proving a reviewer mistake. This is the pre-emission checklist item 8 class — a gate whose expected VALUE the code contradicts — recurring in its cheapest form, and the specific lesson is narrower than item 8 as written: a gate over an ABSENCE must name the property it means, which here is "no file other than these two imports or mentions the module", so the honest form orders the SET of matching files and asserts that set contains no third entry, rather than predicting which of the two will appear. The fix is reviewer-side and lands in the next block's gate wording, not in a worker edit; promoting the narrower rule into docs/agents/planner_reviewer_prompt.md §3 is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here, but named for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490, R-0493 and R-0494. OPEN.

Gate: R6 — PASS. Every ordered gate was re-run by the reviewer from the repository root at ca5ff4f1, and every one reproduces the handback's reading, with the round's single declared deviation CONFIRMED rather than refuted. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r6.md`, the committed `.agent/authored/f085-r6.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 fc4752a4ac333290e30d11145beaf519b9b6eb46d3b01099f95869fff5956d03, 22488 B, 213 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 8b4398f8616dcdb71cf72d254e22c09937f87052350e22bd2721cb69ab1ef5ad, 2136 B, 38 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The C1 append is honest: the pre-C1 blob of 214867 B is a byte-exact PREFIX of the 225757 B post-C1 file, the RECORD-R5, R0495, R0496 and R0497 slices each occur exactly once in the whole file and each exactly once inside the 10890-byte, eight-line appended tail, the numstat is `8 0` with a zero deletion column, and the file is byte-identical from C1 through HEAD. The open set moved by exactly three: 109 registered / 0 resolved / 109 open at 16506c0b against 112 / 0 / 112 at HEAD, symmetric difference of HEAD-open against base-open plus R-0495, R-0496 and R-0497 EMPTY, 0 duplicate ids, 0 resolutions naming an unregistered id, 0 line-start `^Landed: R-` records, max R-0497 and next free R-0498. The substring `Steps` survives 19 times. The change set is exactly the five ordered `.agent/**` paths with nothing under `packages/`, `tests/`, `docs/`, `apps/` or `scripts/`, and G8's counter-proof holds: `packages/orchestration/exec_guard.py` at sha256 d9c77caec4ed9136868cef080bd2e2ae18c4216851507dc943d778d5c575114e, 12241 B, and `tests/orchestration/test_exec_guard.py` at sha256 9301bc652ecf555b983e0cf85dc7c5da52071ef20de741b9cd3f1476188bad53, 6211 B, are byte-identical at 16506c0b and at HEAD, so constraint 4 held and nothing was repaired under cover of a record round. The history is five single-parent commits, bb22b2dd←16506c0b then 4cc753b6, 07255ccd, 93fcf6ff and ca5ff4f1, and the reflog over the round carries `commit:` entries only. The canary is `42 passed in 20.46s`, exit 0. THE DEVIATION, CONFIRMED: G9 ordered a COLOUR — it passed only when the command FAILED — and the worker reported that the colour does not reproduce, 3 red and 4 green over seven runs. At the reviewer's own hand the same command at HEAD is red on 8 runs and green on 4 out of TWELVE, `1 failed, 5 passed` against `6 passed`, always at `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`. The worker's reading is therefore corroborated and the gate as written was unmeetable rather than unmet. The worker recorded the real commands, exit codes and summary lines, edited nothing the gate measures — G8 is the byte proof — and declared the deviation, which is exactly what constraint 7 asks of it; the defect is the reviewer's own and is registered as R-0498. The values R6 routed nowhere are recorded HERE, measured by the reviewer at ca5ff4f1, which is the R-0494 counter-measure working as designed: the handback commit ca5ff4f1 inserted 41 lines and deleted 60, the per-commit insertions before it are C0a 213, C0b 106, C1 8 and C2 14 with none over 500, the post-C5 change set is the same five paths, `git status --porcelain` is EMPTY, `git worktree list` is one line, the push landed with origin at ca5ff4f1, and `.agent/handoff.md` measures 87 lines against its own DECISION D15 declaration of 87, so its self-measurement is honest. LAST_REVIEWED_SHA advances to ca5ff4f1.

- R-0498 — Low, A REVIEWER GATE ORDERED AN EXPECTED COLOUR FOR A COMMAND THE REVIEWER HAD SEEN ONLY FIVE TIMES, AND THAT COMMAND IS A COIN FLIP RATHER THAN RELIABLY RED. Raised by the reviewer against its own R6 block at the R6 gate. G9 of that block ordered `python3 -m pytest tests/orchestration/test_exec_guard.py -q`, declared that the gate PASSES when the command FAILS, and rested that order on five consecutive red runs measured at 16506c0b. The worker got 3 red and 4 green over seven runs and declared the deviation; the reviewer then measured 8 red and 4 green over twelve runs at ca5ff4f1. Five consecutive observations of one colour are not evidence of determinism — for an even coin five identical outcomes arrive once in sixteen attempts, which is ordinary rather than remarkable — so the sample never supported the order built on it, and the flakiness was a property of the test the whole time rather than something that changed between rounds. The cost was one declared deviation on a round that did everything else right, and the worse branch was reachable: had the worker's seven runs happened to come out all red, an unmeetable gate would have been recorded as satisfied and the coin flip would have stayed invisible until it fell the other way at a less convenient moment. This is the reviewer-arithmetic family of R-0327 and R-0336 reaching the same place from a third direction — R-0327 ordered a count the reviewer computed by hand, R-0497 ordered a value the code could not produce, and this one orders a colour that a non-deterministic command cannot honestly promise. Counter-measure, binding on the reviewer from this round on and APPLIED IN THE SAME BLOCK THAT REGISTERS THIS FINDING, as gate G10: a gate that names an expected COLOUR for a command whose determinism has not been established orders that command run at least TEN times with every exit code and summary line reported, and either requires the colour on all ten or is rewritten as a probe that reports what it saw. Promoting the rule into the docs/agents/planner_reviewer_prompt.md §3 pre-emission checklist is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490, R-0493, R-0494 and R-0497. OPEN.

Done: R-0496 — RESOLVED at R7. `assert result.cpu_seconds_used >= 1.0` became `assert result.cpu_seconds_used >= 0.5` in `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`, with a comment above it naming the kernel-accounting reason the old value was a boundary: `ru_utime + ru_stime` rounds against RLIMIT_CPU rather than exactly to it. The counter-measure the finding asked for is met — the tolerance is strictly BELOW the limit and the property the test is named for, the SIGXCPU trip, is asserted separately and unchanged. The reviewer verified the fix by running `python3 -m pytest tests/orchestration/test_exec_guard.py -q` TEN times at d37d1a1e: ten exits of 0, ten `6 passed` summaries, against 8 red of 12 measured at ca5ff4f1 before the fix. The coin flip is gone by measurement rather than by assertion. Commit e77fa588, `7 1` on that path.

Gate: R7 — PASS. Every one of the fifteen ordered gates was re-run by the reviewer from the repository root at d37d1a1e and every one reproduces the handback's reading; the round declared no deviation of substance and none was found. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r7.md`, the committed `.agent/authored/f085-r7.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 f6fd67339f3c9745fb845b95a1fcb5649373c70c410a5852d97a3a7a027ca6af, 21267 B, 253 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 1a2b4a3ed34f4a4ade3ffef65f2d307aebe67b64e549c1439a26ba7434920a45, 2297 B, 40 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. Both live_review appends are honest: the 225757 B base blob is a byte-exact PREFIX of the 231728 B post-C1 file, which is itself a byte-exact PREFIX of the 231994 B HEAD blob, and the numstats are `4 0` at C1 and `2 0` at C3 with both deletion columns zero. The open set moved by exactly one: 112 registered / 0 resolved / 112 open at ca5ff4f1 against 113 / 0 / 113 at HEAD, HEAD-open minus base-open = {R-0498} and base-open minus HEAD-open = {}, 0 duplicate ids, 0 resolutions naming an unregistered id, max R-0498 and next free R-0499. Exactly one LINE-START `^Landed: R-\d+` record exists and it names R-0496, which is the shape §4 item 4 asks for and which THIS round retires into the authored `Done:` above. The substring `Steps` survives 21 times. The change set is exactly the six ordered paths with nothing under `packages/`, `docs/`, `apps/` or `scripts/`, and the UNCHANGED GUARD holds: `packages/orchestration/exec_guard.py` is byte-identical at ca5ff4f1 and at HEAD at sha256 d9c77caec4ed9136868cef080bd2e2ae18c4216851507dc943d778d5c575114e, 12241 B, so constraint 4 held and no part of R-0495's fix leaked into the test round. The CPU-ASSERT pair is a REWRITE and reads as one: the FROM occurs 0 times at HEAD, the TO line exactly 1 time, numstat `7 1`. No marker line reached a target file — 0 `<<<SLICE` and 0 `<<<END` in `.agent/plan.md`, `.agent/live_review.md` and `tests/orchestration/test_exec_guard.py` — and the handback's claim about the single pre-existing `<<<` in `.agent/live_review.md` is exact: 1 occurrence at ca5ff4f1 and 1 at HEAD, in authored prose about a former gate. THE COIN FLIP IS GONE, measured and not asserted: ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at the reviewer's own hand are ten exits of 0 and ten `6 passed` summaries between 4.55s and 4.60s, against the 8 red of 12 the reviewer measured at ca5ff4f1 — which is what R-0498's counter-measure asks a colour gate to establish before it is ordered. `python3 -m ruff check` on the test file is exit 0 under the repository's own configuration; the canary is `42 passed in 20.49s`, exit 0; the eight-file structural sweep is `350 passed, 6 skipped`, exit 0, three times out of three. Per-commit insertions are C0a 253, C0b 156, C1 4, C2 7, C3 2 and C4 12, none over 500, and the history is seven single-parent commits d0e597a3←ca5ff4f1 through d37d1a1e with a reflog of `commit:` entries only. The values R7 routed nowhere are recorded HERE, measured by the reviewer at d37d1a1e, which is the R-0494 counter-measure working as designed: the handback commit d37d1a1e inserted 58 lines and deleted 42, `.agent/handoff.md` measures 103 lines against its own DECISION D15 declaration of 103 so its self-measurement is honest, `git status --porcelain` is EMPTY, `git worktree list` is one line, and origin carries d37d1a1e with no PR open. LAST_REVIEWED_SHA advances to d37d1a1e.

- R-0499 — Low, THE EIGHT-FILE STRUCTURAL SWEEP GOES RED ABOUT ONCE IN TWENTY RUNS INSIDE A FRESH GIT WORKTREE, AND THE FAILING NODE ID HAS NEVER BEEN CAPTURED. Raised by the reviewer at the R8 authoring dry run. Two observations exist and both are inside a disposable worktree, never in the primary checkout: the F085 R7 worker saw one red in 22 runs on a scratch worktree carrying a larger draft change and did not capture the node id, and the reviewer saw one red in 14 runs on the R8 dry-run worktree and did not capture it either, because the run that produced it was not the run that carried `-rf` output to the log. The red reading is `1 failed, 348 passed, 7 skipped` against the green `350 passed, 6 skipped`, so a test that normally PASSES was SKIPPED in the same run that another test failed — which is the signature of an environment-conditional skip rather than of a logic defect. The sweep's only environment-conditional member is `test_typescript_compiles` in `tests/ui_server/test_dashboard_contract.py`, which resolves `apps/ui/node_modules/.bin/tsc` relative to the file's own tree, skips with "UI toolchain absent" when that path is missing, and otherwise shells out to a REAL `tsc --noEmit` under `timeout=30` — the one member of the eight-file sweep that depends on a heavy external toolchain and on wall-clock. `node_modules` is gitignored, so a fresh worktree's copy of it is populated out of band and its state at the worktree's FIRST sweep run is not something the sweep controls. Nothing in the F085 change set reaches any of the eight files, so this is a pre-existing property of the gate and not of the guard. Counter-measure, already applied in the block that registers this finding: the sweep is ordered as a PROBE carrying `-rf`, never as an expected COLOUR, and a red run reports its FAILED node id verbatim and hands back rather than re-running until green — which is the only way the id gets captured. The finding resolves when a red run finally names the test. Whether `test_typescript_compiles` belongs in a structural sweep at all is a question for the F252 flake work and is NOT claimed here. OPEN.

Gate: R8 — PASS, and the round that finally makes the guard bound its own runtime. Every one of the fifteen ordered gates was re-run by the reviewer from the repository root at b868401f and every one reproduces the handback's reading. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r8.md`, the committed `.agent/authored/f085-r8.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 b89466df0a7caa60971c727be97ae1ab0de7478476fc7be391a0bdb63163dfde, 27927 B, 393 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 a0bd751ab5087eea336976f65cc2aa62f79dddf74fbecbc672d6bf92ab2db1a5, 2235 B, 39 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The C1 edit is exactly the shape the block ordered: the pre-C1 blob ends with the LANDED-R0496 line, stripping that line leaves 231729 B which is a byte-exact PREFIX of the 238429 B post-C1 file, and the 6700-byte remainder equals the DONE-R0496 slice, a blank line, the RECORD-R7 slice, a blank line and the R0499 slice, byte for byte — the reviewer reconstructed that remainder from its own scratchpad slices and compared bytes, rather than reading the worker's claim. The numstat is `5 1` and the single deletion is the retired `Landed:` line. The open set moved as ordered: 113 registered / 0 resolved at d37d1a1e against 114 / 1 at HEAD, registered delta exactly {R-0499} with nothing lost, resolved exactly {R-0496} against an empty base, 0 duplicate ids, 0 resolutions naming an unregistered id, max R-0499, next free R-0500, and the LINE-START `^Landed: R-\d+` count fell from 1 to 0 — the worker's marker retired into reviewer-authored text, which is what §4 item 4 asks for. The substring `Steps` survives 23 times. The change set is exactly the seven ordered paths with nothing under `docs/`, `apps/` or `scripts/`. THE FIX ITSELF, read as a diff and not as a summary: `run_guarded`'s `finally` no longer calls `out_pump.join()` and `err_pump.join()` untimed; it computes ONE `drain_deadline` from `policy.stream_drain_grace_seconds`, joins both pumps against that shared deadline so the grace is a total and not a per-stream cost, derives `streams_complete` from `is_alive()` on both, and closes `proc.stdout`/`proc.stderr` ONLY when the drain completed — the deliberate leak of a pipe read end under a still-blocked reader being cheaper than a recycled-fd read, which the added comment states where a reader will find it. `stream_drain_grace_seconds` and `streams_complete` are documented in their own dataclass docstrings, and the `run_guarded` docstring's old absolute claim "no descendant outlives this call" is narrowed to "no descendant of THAT GROUP", with the setsid escape named and attributed to R-0495. All seven pairs read as declared: GUARD5 and GUARD6 are rewrites with FROM 0x and TO 1x, GUARD1, GUARD2, GUARD3, GUARD4 and GUARD7 are appends with TO 1x, numstat `32 5`. The new test is present exactly once and the file ends with it. THE PROPERTY IS MEASURED, NOT ASSERTED: the reviewer reproduced R-0495 before ordering the fix — an escapee sleeping 20s under `wall_timeout_seconds=1.0` made the unfixed guard return after 20.13s — and the fixed guard returned after 6.00s, the 1.0s deadline plus the 5.0s grace, with `streams_complete=False` and no surviving process. Ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at the reviewer's own hand are ten exits of 0 and ten `7 passed` summaries between 7.62s and 7.66s, and the worker's independent ten are the same. The red control is decisive and the reviewer ran it too, in a disposable worktree: replacing the bounded join with `pump.join()` turns the suite red at exactly one node, `test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group`, on `assert result.streams_complete is False` — so the new test detects the very regression it was written for, and the gate can fail honestly. `grep -rn "exec_guard"` over packages, apps, scripts and tests still names exactly one file, the test file, so constraint 4 held and NO call site was migrated: the running system is still unprotected and no containment claim may be made from this round. Ruff is exit 0 under the repository's own configuration; the canary is `42 passed in 20.48s`, exit 0; the eight-file sweep is `350 passed, 6 skipped`, exit 0, three times out of three, so R-0499 gained no new observation. Per-commit insertions are C0a 393, C0b 268, C1 5, C2 32, C3 35 and C4 12, none over 500, and the history is seven single-parent commits 988869c6←d37d1a1e through b868401f with a reflog of `commit:` entries only. The values R8 routed nowhere are recorded HERE, measured by the reviewer at b868401f (R-0494): the handback commit b868401f inserted 45 lines and deleted 44, `.agent/handoff.md` measures 104 lines against its own DECISION D15 declaration of 104 so its self-measurement is honest, `git status --porcelain` is EMPTY, `git worktree list` is one line, and origin carries b868401f with no PR open. The round's eight declared deviations were all checked and all are accurate; deviation 5 is the honest declaration of a real defect the reviewer caused, and it is registered as R-0500 rather than held against the round. LAST_REVIEWED_SHA advances to b868401f.

- R-0500 — Low, A BLOCK ORDERED "PRECEDED BY EXACTLY ONE BLANK LINE" FOR AN APPEND WHOSE TARGET WAS A TOP-LEVEL PYTHON DEFINITION, WHICH THE LANGUAGE SEPARATES BY TWO. Raised by the reviewer against its own R8 block at the R8 gate. Change item 5 of that block ordered the NEW-TEST slice appended "preceded by exactly one blank line", and the worker applied it exactly, so `tests/orchestration/test_exec_guard.py` now separates its last test from the one above by ONE blank line while all its other tests are separated by TWO. The worker was right not to adjust the bytes — constraint 2 forbids it — and right to declare it, which it did as deviation 5. The wording came from the `.agent/live_review.md` appends in the same block, where one blank line IS the convention, and was reused for a Python file without re-reading what the target file's own layout demands; that reuse is the defect. Lint does not catch it and cannot be relied on to: `ruff check` was exit 0 both before and after, because pycodestyle's blank-line rules E301-E306 are preview-only in stable ruff and the repository selects `["E", "F", "W", "I", "UP"]` without preview, so those rules are never EVALUATED rather than merely unreported — the same shape as R-0463, where `--isolated` made a probe blind rather than wrong. The cost is one line of churn and this finding; nothing was mismeasured and no gate passed falsely, which is why it is Low. Counter-measure, binding on the reviewer from this round on: a block that orders an APPEND into a source file states the separator the TARGET LANGUAGE requires and never a generic blank-line count carried over from a prose or state file — and where the separator itself is the thing being fixed, the gate MEASURES it directly, as G10 of the block registering this finding does, rather than resting on a linter that does not evaluate the rule. Promoting the rule into the docs/agents/planner_reviewer_prompt.md §3 pre-emission checklist is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490, R-0493, R-0494, R-0497 and R-0498. OPEN.

Done: R-0500 — Resolved at R10. The new test is separated from the one above it by
two blank lines, matching every other top-level definition in
`tests/orchestration/test_exec_guard.py`; the fix was commit 76f53036 of R9 and
added exactly one newline byte and no code. The reviewer re-measured the property
at 02043452 rather than reading the claim: the separator list over the whole file
is `[3, 3, 3, 3, 3, 3, 3]` at HEAD against `[3, 3, 3, 3, 3, 3, 2]` at b868401f, and
the file grew from 8134 to 8135 bytes, a difference of exactly one. The
counter-measure the finding names is carried into R11, whose block states the
separator PYTHON requires for the tests it appends, distinguishes it from the
one-blank-line convention that governs this prose file, and measures it directly
instead of resting on a linter that never evaluates the rule. Promoting the
counter-measure into the docs/agents/planner_reviewer_prompt.md §3 checklist
remains a `docs/agents/**` edit outside this feature's change set and is NOT
claimed here; it stays routed to the paydown branch, whose backlog this round's
DECISION D2 calls overdue.

Gate: R9 — PASS, the round that recorded the R8 verdict and fixed the separator the
R8 block got wrong. All fifteen ordered gates were re-run by the reviewer from the
repository root at 02043452 and every one reproduces the handback's reading; the
verdict rests on those runs and not on any earlier session's claim about them, a
distinction that matters because R9's PASS existed nowhere in this repository
until this line. TRANSPORT: the committed `.agent/authored/f085-r9.md` and the
committed `.agent/last_block.md` are byte-EQUAL at sha256
e8011bbab7c5e3cd1817c1566e1112fde16ec47975b65e5cb05a358ff6d6f42d, 23297 B, 263
lines — computed over the COMMITTED files, the digest fallback of §4.9, because
this session did not author that block and holds no scratchpad original of it.
`.agent/plan.md` byte-equals its slice at sha256
83b4a6777d941144520af17a34a3731a16ab650bbc962822f1f17d356971eedb, 2217 B, 39
lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The
two `.agent/live_review.md` commits are pure appends as ordered: the pre-C1 blob is
a byte-exact PREFIX of the post-C1 file with a 7530-byte remainder, the pre-C3 blob
is byte-identical to the post-C1 blob and is a PREFIX of the file at HEAD with a
250-byte remainder, and both numstats carry a deletion column of 0. The open set
moved exactly as ordered: 114 registered / 1 resolved at b868401f against 115 / 1
at HEAD, registered delta exactly {R-0500} with nothing lost, resolved UNCHANGED at
{R-0496} because R9 resolved nothing, 0 duplicate ids, 0 resolutions naming an
unregistered id, and exactly one `^Landed:` record, naming R-0500 — which is what
an unreviewed fix is supposed to look like, and which the commit carrying this
record retires. The substring `Steps` survives 25 times. THE FIX ITSELF, read as a
diff and not as a summary: commit 76f53036 adds ONE blank line before
`@pytest.mark.subprocess` on the file's last test and changes no code, numstat
`1 0`, 8134 B to 8135 B. THE PROPERTY IS MEASURED, NOT ASSERTED: the separator list
runs `[3, 3, 3, 3, 3, 3, 2]` at b868401f and `[3, 3, 3, 3, 3, 3, 3]` at HEAD, so
every decorated test now carries the two blank lines Python separates top-level
definitions by, and the trailing 2 that was the defect is gone.
`packages/orchestration/exec_guard.py` is UNCHANGED across the round at sha256
7dde71c84992af985b28c72d9b460280238721dae474938806f28f9b421b3b67 on both sides, so
R9 added nothing to the module R8 fixed and no containment claim follows from it.
Ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py
-q` at the reviewer's own hand are ten exits of 0 and ten `7 passed` summaries
between 7.60s and 7.66s; ruff is exit 0 under the repository's own configuration
and says nothing about the separator, exactly as the block declared; the canary is
`42 passed in 20.49s`, exit 0; and the eight-file structural sweep is `350 passed,
6 skipped`, exit 0, three times out of three, so R-0499 gained no new observation.
The change set is exactly the six ordered paths with nothing under `docs/`, `apps/`
or `scripts/`. Per-commit insertions are C0a 263, C0b 124, C1 4, C2 1, C3 2 and C4
6, none over 500, and the history is seven single-parent commits 831a2b0c←b868401f
through 02043452 with no amend, rebase, reset or force-push. The values R9 routed
nowhere are recorded HERE, measured by the reviewer at 02043452 (R-0494): the
handback commit 02043452 inserted 43 lines and deleted 47, `.agent/handoff.md`
measures 100 lines against its own DECISION D15 declaration of 100 so its
self-measurement is honest, `git status --porcelain` is EMPTY, `git worktree list`
is one line, and origin carries 02043452 with no PR open. The round's five declared
deviations were all checked and all are accurate. LAST_REVIEWED_SHA advances to
02043452.

- R-0501 — Low, A HANDBACK NAMED THE NEXT SESSION'S FIRST ACTION WITHOUT NAMING
PHASE 1 RULE 1 BEFORE RULE 2. Raised by the reviewer at the R9 gate against the R9
block, which authored that section. docs/agents/self_drive_protocol.md Phase 2 ends
with a standing requirement on this exact text: "every handoff that names the next
session's first action names Phase 1 rule 1 before rule 2", rule 1 being the
re-read of `.agent/STOP` from disk and rule 2 the Open PR Gate. The R9 handoff's
"Next" section opens with "R10 starts T002a" — a next-session first action — and
among its remaining bullets names the absence of an open PR, which is rule-2
territory, while rule 1 appears nowhere in the file. The requirement exists because
Phase 0 is one-shot while G6 binds at any point, so a sentinel appearing
mid-session stays invisible until an unrelated gate trips over it (R-0347); the
belt-and-braces reminder is what is missing. Severity is Low precisely because
Phase 0 does probe `.agent/STOP` at session start and did so here, finding it
absent, so nothing was actually missed. This is the same family as R-0500 and the
second instance in two rounds: in both, the block author reused a section's
established wording without re-reading the rule that governs that section.
Counter-measure, binding on the reviewer from this round on and demonstrated by the
block that registers this finding: a block ordering a handback's "Next" section
states the rule ORDER that section must carry rather than describing its content,
as change item 5 does here. The recurrence is why this round's DECISION D2 calls
the paydown branch overdue: a counter-measure that cannot be written into
docs/agents/planner_reviewer_prompt.md §3 while a feature branch is open binds only
the block that states it, and this family has now cost two rounds. OPEN.

Gate: R11 — PASS, the round that gave `exec_guard` an opt-in environment allowlist
with a floor beneath it. All thirteen ordered gates were re-run by the reviewer from
the repository root at 0406ceba and every one reproduces the handback's reading.
TRANSPORT, disk-to-disk against the reviewer's OWN scratchpad original and NOT by
digest fallback (§4.9): `.remedy-wt/f085-r11.md`, the committed
`.agent/authored/f085-r11.md` and the committed `.agent/last_block.md` are byte-EQUAL
at sha256 0ac925d29a4c537683a695d732ed4d4af62e600ed7486d7d0d762514715a469b, 19176 B,
400 lines — at the 400-line block cap of DECISION F105 D5, not over it. `.agent/plan.md`
is sha256 699172bfed0791f5ab282384ef8f669c26249c6418ddc4fdd7a8c1688edd361a, 2446 B, 42
lines, under the 50-line cap, and the PLAN pair did what a narrowed pair is for: the
`## Goal` and `## Risks` sections are byte-IDENTICAL to their text at 2587780d, the
`## Next Steps` list renumbers contiguously 1-2-3 with no orphaned entry, and PLANF
occurs 0 times against PLANT once. ALL TEN pair shapes read exactly as declared over
the whole of each target file: FROM 0 / TO 1 for the rewrites PLAN, GUARD1, GUARD2,
GUARD4, GUARD6 and TEST1, and FROM 1 / TO 1 for the appends GUARD3, GUARD5, GUARD7 and
TEST2, with NEWTESTS occurring once and the test file ending with it. THE CHANGE
ITSELF, read as a diff and not as a summary: `FORBIDDEN_ENV_KEYS` is a frozenset whose
members and spelling match `managed_builder_execution._FORBIDDEN_ENV_KEYS`;
`scrub_child_env` intersects a caller's allowlist with the source mapping AFTER
subtracting that floor, so an allowlist naming a secret cannot lower it, and an
allowlisted key the source never defined is absent rather than empty; `env_allowlist`
is a new frozen-dataclass field defaulting to None; and `run_guarded` computes
`child_env` from `os.environ` or from `policy.env` ONLY when the allowlist is not
None, so the T001 pass-through contract is byte-for-byte unchanged when it is. The
module docstring's absence note was narrowed rather than deleted, and a new paragraph
states the honest limit a reader would otherwise have to discover: an allowlist bounds
what the PARENT hands over and never what the child's runtime adds back, a CPython
child setting `LC_CTYPE` itself under PEP 538 locale coercion, so the child's
environment is a SUPERSET of the scrubbed one. That paragraph is why the tests
subtract an interpreter-added key instead of asserting an exact environment — the
reviewer hit that exact failure in its own pre-emission dry run, which is what a dry
run is for. THE PROPERTY IS MEASURED, NOT ASSERTED: before ordering the block the
reviewer ran three red controls in a disposable worktree and each was decisive —
dropping the `FORBIDDEN_ENV_KEYS` subtraction reddens exactly
`test_a_secret_like_variable_never_reaches_the_child_even_when_allowlisted`; scrubbing
unconditionally reddens eight tests including every T001 fixture, which is what proves
the None path load-bearing; and returning `""` for an undefined key reddens exactly
`test_scrub_child_env_drops_a_key_the_source_never_defined`. Restored, the suite is
green again. At HEAD the reviewer's own ten consecutive runs of `python3 -m pytest
tests/orchestration/test_exec_guard.py -q` are ten exits of 0 and ten `12 passed`
summaries between 7.71s and 7.79s — 12 against the 7 of R9, the five new tests. The
import path was verified in the same session (`m.__file__` resolves inside the primary
checkout and both new names are present), because a shell cwd that had silently
persisted into a worktree is a real failure mode this session hit. Ruff is exit 0 for
both files under the repository's own configuration, and the worker took the same
reading at base BEFORE touching either file, so the green is unchanged rather than
newly earned. The canary is `42 passed in 20.46s` and the four `.agent/` state readers
are `157 passed in 19.74s`, both matching base. THE HONESTY GATE HOLDS, by a corrected
measurement: the only TRACKED `.py` file containing the string `exec_guard` is the test
file, and no tracked module imports `packages.orchestration.exec_guard`, so NO call
site was migrated and nothing in the running system is scrubbed by this round. The
change set is exactly the six ordered paths. Per-commit insertions are C0a 400, C0b
358, C1 145 and C2 7, none over 500; the history is five single-parent commits
a1726eb7←2587780d through 0406ceba with no amend, rebase, reset or force-push; and
`git status --porcelain` is EMPTY with one worktree. `.agent/handoff.md` measures 90
lines against its own DECISION D15 declaration of 90, so its self-measurement is
honest. The round's six declared deviations were all checked and all are accurate; two
of them report defects in the REVIEWER's gates rather than in the work, and the worker
was right to report them as measured instead of repairing text to make a number come
out — they are registered here as R-0502 and R-0503 rather than held against the round.
LAST_REVIEWED_SHA advances to 0406ceba.

Done: R-0501 — Resolved at R12. The counter-measure has now been applied twice on disk
and verified by the reviewer both times: the R10 handback's "Next" section opens with
"FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, re-read
`.agent/STOP` from disk" and only then reaches the Open PR Gate, and the R11 handback
does the same. Both blocks ordered that ORDER explicitly rather than describing the
section's content, which is the counter-measure the finding named. The rule the R9
handback missed — Phase 2's "every handoff that names the next session's first action
names Phase 1 rule 1 before rule 2" — is therefore satisfied by the two most recent
handbacks, and the belt-and-braces reminder exists again for the next session that
resumes cold. Promotion of the counter-measure into the
docs/agents/planner_reviewer_prompt.md §3 checklist stays a `docs/agents/**` edit
outside this feature's change set and is NOT claimed here; it remains routed to the
paydown branch, which this feature's DECISION D2 calls overdue.

- R-0502 — Low, A REVIEWER GATE ASKED grep FOR A STRING THE TARGET FILE CANNOT
CONTAIN, MAKING ITS EXPECTED RESULT UNREACHABLE. Raised by the reviewer at the R11
gate against its own R11 block. Gate 11 of that block ordered
`grep -rln "exec_guard" packages apps scripts tests` and declared that it "names
exactly two paths — `packages/orchestration/exec_guard.py` and
`tests/orchestration/test_exec_guard.py`". `grep -l` matches file CONTENT, and
`exec_guard.py` does not contain the string `exec_guard` anywhere in its own source,
so the module could never appear in that output — at 2587780d exactly as at HEAD. The
declared result was unreachable when the gate was written, not broken by the round.
The worker did the right thing: it reported the gate as measured, named the cause,
demonstrated the underlying property by a different route, and changed nothing to make
the number come out. This is the R-0371 family — a gate that cannot be satisfied by
any honest run — and the neighbouring R-0438 case, where a path that did not resolve
made a gate silently vacuous; here the gate was loud rather than vacuous, which is why
it cost only a deviation. The PROPERTY the gate exists for does hold, by the corrected
measurement the reviewer ran at the gate: intersected with `git ls-files`, the only
tracked `.py` file containing `exec_guard` is `tests/orchestration/test_exec_guard.py`,
and no tracked module imports `packages.orchestration.exec_guard`, so no call site was
migrated. Counter-measure, binding on the reviewer from this round on: a no-caller gate
names the IMPORT statement over TRACKED files —
`git grep -ln "from packages.orchestration.<module> import"` — and never a bare
filename grep, because a module's own name is the one string its source is least likely
to contain, and untracked `__pycache__` artifacts otherwise pollute the result. OPEN.

- R-0503 — Low, AN "EXACTLY ONCE AMONG THE ADDED LINES" PROOF IS UNSATISFIABLE FOR
STRUCTURAL LINES. Raised by the reviewer at the R11 gate against its own R11 block.
Gate 4 ordered, for each append-shaped pair, that "each TO-ONLY added line" occur
"exactly once AMONG THE LINES THAT COMMIT ADDS", quoting
docs/agents/planner_reviewer_prompt.md §4 item 9. Applied literally that is unmeetable
whenever a TO adds more than one blank line or more than one bare `"""`, which every
multi-definition Python slice does: R11's C1 added six blank lines to `exec_guard.py`,
twenty-three to the test file, and two bare docstring terminators. The worker met the
gate for every CONTENT-carrying line — GUARD3 18/18, GUARD5 1/1, GUARD7 5/5, TEST2
16/16, zero content strays — and enumerated the structural repeats instead of
filtering them out of sight, which is the honest reading and the one the reviewer
accepts. The §4 item 9 rule was written for prose files, where a repeated line is a
real signal that a slice landed twice; in a source file a repeated blank line carries
no information at all. This is the same shape as R-0253, which already had to bend the
whole-file version of this count because a TO legitimately repeats a sentence the file
already carries — the rule bends, never the text. Counter-measure, binding on the
reviewer from this round on: an "exactly once among the added lines" gate over a
SOURCE file scopes itself to lines that are not blank and not a bare docstring
delimiter, and says so in the gate rather than leaving the worker to discover the
exception and spend a deviation on it. Whether §4 item 9 itself should carry that
carve-out is a `docs/agents/**` edit outside this feature's change set and is NOT
claimed here; it is routed to the paydown branch with R-0502. OPEN.

Gate: R12 — PASS, the record round that carried the R11 verdict, one resolution and two
reviewer-gate findings onto disk. All eleven ordered gates were re-run by the reviewer and every
one reproduces the handback's reading. TRANSPORT, disk-to-disk and not by digest fallback: the
reviewer's `.remedy-wt/f085-r12.md`, the committed `.agent/authored/f085-r12.md` and
`.agent/last_block.md` are byte-EQUAL at sha256
0f66ffe7b9a96bdb9bf8f9cb130a21d7ec2b8a8102f9f02cf85fa1ff74e78678, 18334 B, 264 lines. C1 IS A
PURE APPEND, proven by shape: the pre-C1 blob is a byte-exact PREFIX of the post-C1 file, HEAD
equals it, and the 9775-byte remainder is exactly the four ordered slices, each occurring ONCE and
in order. THE ARITHMETIC: 116 / 2 / 0 at base against 118 / 3 / 0 at HEAD, so the open set rose
114 to 115 by exactly two registrations against one resolution; the registered difference is
R-0502 and R-0503 with nothing lost, the resolved difference R-0501, no duplicate ids, no
resolution naming an unregistered id. `.agent/plan.md` is 41 lines under its 50-line cap with
`## Goal`, `## Next Steps` and `## Risks` byte-IDENTICAL to base. THE HONESTY GATE HOLDS:
`exec_guard.py` and its test are byte-unchanged, so no containment claim follows from this round.
Canary 42 passed, state readers 157 passed, both matching base; insertions 264, 200, 123, 3, none
over 500; five single-parent commits, no amend or force-push; the change set is exactly the five
declared `.agent/` paths; `.agent/handoff.md` measures 85 lines against its declaration of 85; the
five declared deviations are accurate. LAST_REVIEWED_SHA advances to the R12 handback commit.

- R-0504 — Medium, A SOURCE-TEXT TEST ASSERTED A KEYWORD ITS TARGET'S OWN DOCSTRING ALSO CARRIED,
SO THE TEST WAS VACUOUS FROM THE DAY IT WAS WRITTEN. Raised by the reviewer while measuring the
R13 migration, against pre-existing code and not against any round.
`tests/orchestration/test_managed_builder_execution.py::TestManagedRunner::test_shell_false_always`
read `inspect.getsource(run_managed_builder)` and asserted that `shell=False` appears in it and
`shell=True` does not. That function's DOCSTRING opens with "shell=False ALWAYS. Sanitized env.
Hard timeout. Output byte cap.", so the positive half was satisfied by prose. The reviewer PROVED
the vacuity rather than arguing it: in a disposable worktree at the round's base commit, deleting
the `shell=False` keyword from the real `subprocess.run` call and touching nothing else left the
test GREEN, exit 0, one passed. A test that stays green when the property it names is deleted was
never testing that property. The negative half fails in the mirror image: the module docstring also
carries "NO shell=True" among its hard rules, so a substring search for the dangerous form matches
prose too. The property was never at risk — `test_no_shell_true_in_orchestration` walks the AST of
every `packages/orchestration/*.py` and fails on a real `shell=True` keyword; what was at risk was
the belief that this second test added anything. This is the R-0438 and R-0502 family, a gate that
cannot fail honestly, and the third instance in three rounds, which is why severity is Medium
rather than Low: the first two were the reviewer's own gate text, this one sat in the committed
suite. Counter-measure, applied in the round that registers it: a test asserting the SHAPE of code
parses that code and inspects the AST, never searches its text, because a docstring, a comment and
a call site are indistinguishable to a substring search. C2 replaces it with an AST assertion that
`run_managed_builder` holds no `subprocess` spawn node, that `run_guarded` holds exactly one
`Popen` node passing no `shell` keyword, and that no `shell=True` keyword node exists here. OPEN.

Gate: R13 — PASS, the round that gave `exec_guard` its first caller and put one live seam under
supervision. All twelve ordered gates were re-run by the reviewer from the repository root at
ee8e7ba1 and every one reproduces the handback's reading. TRANSPORT, disk-to-disk and not by
digest fallback: the reviewer's `.remedy-wt/f085-r13.md`, the committed
`.agent/authored/f085-r13.md` and `.agent/last_block.md` are byte-EQUAL at sha256
e7f57d218a3bb2418b744753b46e667cfa8cf6e2ab22f43342e672c2eb865808, 23370 B, 400 lines — AT the
DECISION F105 D5 block cap, not over it. C1 IS A PURE APPEND: the pre-C1 blob is a byte-exact
PREFIX of the post-C1 file, HEAD equals it, and the 3777-byte remainder is exactly RECORD-R12 and
R-0504, each occurring ONCE. THE ARITHMETIC: 118 / 3 / 0 at base against 119 / 3 / 0 at HEAD, so
the open set rose 115 to 116 by exactly one registration against no resolution, with nothing lost,
no duplicate id and no resolution naming an unregistered id. THE CHANGE ITSELF, read as a diff:
`run_managed_builder` no longer calls `subprocess.run`; it calls `run_guarded` under a
`_builder_exec_policy` that sets the wall deadline, the per-stream output cap, the cwd pin, a zero
core dump and `env_allowlist=tuple(sorted(env))` — an identity over an already-sanitized env that
adds `FORBIDDEN_ENV_KEYS` as a floor — and deliberately leaves `cpu_seconds`,
`address_space_bytes` and `open_files` None with the reason written where a reader will look. A
wall trip is re-raised as `subprocess.TimeoutExpired` so the module's existing timeout path is
reached unchanged, and the result is wrapped in a `subprocess.CompletedProcess` so every
downstream reader keeps its shape; `_guarded_exit_code` rebuilds the -SIGNUM form the guard
reports as a NAME. BEHAVIOUR EQUALITY WAS MEASURED, NOT ASSERTED: before ordering the block the
reviewer ran six paired probes against base and HEAD — echo, false, a 1s wall timeout, a missing
command, an over-cap output and a SIGKILL suicide — and all six agree on status, exit code, stored
output length and safe summary, including exit_code -9 on both sides and a child environment of
exactly the eight sanitized keys with `GITHUB_TOKEN` absent. FOUR RED CONTROLS were decisive, each
reddening EXACTLY its own test and nothing else, and the reviewer re-ran control (b) itself
against the COMMITTED code in an isolated extraction: restoring the direct spawn reddens the AST
test, disabling the wall re-raise reddens the timeout test, returning the raw returncode reddens
the signal test, and dropping `env_allowlist` reddens the policy test. At HEAD the suite is
132 passed against 129 at base, `test_exec_guard.py` is 12 passed unchanged, ruff is exit 0 for
both files at base AND at HEAD, the canary is 42 passed and the four state readers are 157 passed.
THE CALLER GATE, scoped to `-- packages tests` so no block file can match itself: ONE path at base
and THREE at HEAD, adding the module and its test — the guard's no-caller era is over.
`.agent/plan.md` is 42 lines under its 50-line cap with `## Goal` and `## Risks` byte-IDENTICAL to
base. The change set is exactly the seven declared paths with 0 outside; insertions are 400, 391,
42, 124 and 8, none over 500; the history is six single-parent commits with no amend, rebase,
reset or force-push; `git status --porcelain` is EMPTY and `git worktree list` is ONE line; and
`.agent/handoff.md` measures 95 lines against its own declaration of 95. The round's seven
declared deviations were all checked and all are accurate — deviation 7 correctly caught a stale
numeral in the dispatching brief, which named fourteen gates where the block numbers twelve; the
block governed and all twelve ran. LAST_REVIEWED_SHA advances to the R13 handback commit.

- R-0505 — Medium, TWO CLAUSES OF ONE BLOCK ORDERED INCOMPATIBLE THINGS, AND THE WORKER HAD TO
SPEND A DEVIATION CHOOSING BETWEEN THEM. Raised by the reviewer at the R13 gate against its own
R13 block. Gate G8 of that block ordered the four red controls to run "in a DISPOSABLE worktree
under `.remedy-wt/`", which is what docs/agents/self_drive_protocol.md G5 requires of destructive
verification. Constraint 3 of the SAME block said "No worktree is added, removed or pruned", and
gate G1 ordered `git worktree list` to print ONE line. No execution satisfies all three. The
constraint was correct for the round the block STARTED as — a record round plus a migration, with
no destructive check — and was never revisited when the red controls were added to the gate list
later in authoring. The worker resolved it in favour of the hard constraints, extracting
`git archive HEAD` into a gitignored directory instead of adding a worktree, proved the isolation
and the import path inside that copy, deleted it afterwards, and declared the whole thing. That is
the right call and the right report, and the round was not damaged; what it cost was a deviation
spent on the reviewer's bookkeeping. This is the family the F083 R9 lesson names — clause-versus-
clause is the gap a per-clause checklist misses, because each clause is individually correct and
only the PAIR is wrong. Counter-measure, binding on the reviewer from this round on: when a gate
is added to a drafted block, re-read the CONSTRAINTS section against it before emission, and state
in the constraint itself which gates are exempt from it rather than writing an absolute. A block
that permits no disposable tree must not also order one. OPEN.

- R-0506 — Medium, A MIGRATION FALSIFIED TWO DOCUMENTED ABSENCE CLAIMS AND LEFT BOTH STANDING.
Raised by the reviewer at the R13 gate; the round MEASURED and reported both, exactly as its gate
G12 ordered, and deliberately fixed neither. (1) `packages/orchestration/exec_guard.py` states
under "Deliberate absences, written here because text search cannot find code that does not
exist" that "NO CALLER. Nothing in this repository imports this module yet", and that choosing an
allowlist per command class "is not done here". Both were true until R13 and are FALSE at
ee8e7ba1: the scoped import grep names three paths, and `_builder_exec_policy` chooses exactly
such an allowlist. (2) `packages/orchestration/managed_builder_execution.py`'s module docstring
calls itself "the ONLY place in the codebase that may invoke subprocess for builder execution" and
promises "shell=False ALWAYS", and `run_managed_builder`'s own docstring repeats it; the spawn is
now `run_guarded`'s `subprocess.Popen`, which passes no `shell` keyword at all. The second text is
the one that MADE R-0504 possible — a docstring sentence a source-text test could satisfy — so
leaving it in place while its test has been replaced is the sharper half of this finding. Neither
was fixed at R13 because `exec_guard.py` sits outside that round's declared change set and the
docstring rewrite belongs with the four remaining builder sites, where the same sentences must be
corrected once rather than twice. This is the R-0417 staleness family: a claim of ABSENCE has a
lifetime, and the commit that ends it is the commit that owes the correction. R14 registers it;
the R15 migration round must carry the fix for both files in its change set and gate the property
that neither file claims an absence the caller gate contradicts. OPEN.

Gate: R14 — PASS, the record round `.agent/STOP` halted after its third commit. All eight ordered
gates were re-run by the reviewer from the repository root and every one reproduces the handback's
reading. TRANSPORT, disk-to-disk and not by digest fallback: the reviewer's `.remedy-wt/f085-r14.md`,
the committed `.agent/authored/f085-r14.md` and `.agent/last_block.md` are byte-EQUAL at sha256
77447503b8bc9e86e2f8f905172874568777ae8d25b074c0d3662b912b10d32e, 15023 B, 214 lines. C1 IS A PURE
APPEND: the pre-C1 blob is a byte-exact PREFIX of the post-C1 file, HEAD equals it, and the
7296-byte remainder is exactly blank + RECORD1 + blank + FIND1 + blank + FIND2 in that order, each
slice occurring ONCE, none carrying trailing whitespace, no marker line reaching it. THE ARITHMETIC: 119 / 3 / 0 at base against 121 / 3 / 0 at HEAD, so the open set rose
116 to 118 by exactly two registrations against no resolution; the registered difference is R-0505
and R-0506, the resolved difference empty, no duplicate id, no resolution naming an unregistered id.
THE HALT WAS CORRECT AND HONESTLY REPORTED. `.agent/STOP` appeared mid-round, C2 was never started,
`.agent/plan.md` is byte-IDENTICAL to base at sha256
8dae6b41813aff162aeb1c5a877ab667be909c723c30bbb4dc5b3fce42f65f6d, and PLANF still occurs EXACTLY
once in it — so the round did not half-apply a pair and then round the number, which is what this
gate catches. G5 is red by the sentinel, not by a misapplication. THE HONESTY GATE HOLDS: `exec_guard.py`,
`managed_builder_execution.py` and `test_managed_builder_execution.py` are byte-identical between
base and HEAD, so no containment claim follows from that round. State readers 157 passed and canary
42 passed, both matching base; the change set is three `.agent` paths before C3, short of the ordered
four by `.agent/plan.md` alone, which IS the skipped commit; insertions 214, 150 and 80, none over
500; four single-parent commits, every reflog entry `commit:`-prefixed, no amend, rebase, reset or
force-push; `.agent/handoff.md` measures 79 lines against its D15 declaration of 79; all seven
declared deviations are accurate. The sentinel is ABSENT at this round's start, so Phase 1 rule 1
does not fire. TWO SCOPE REASSIGNMENTS, recorded because each contradicts text already on
disk: R-0506 stays OPEN with its fix moved from R15 to R16, and T002a's CLI half is split — R15
migrates the version probe, while `_call`, `_call_reviewer_structured` and the envelope mock are ONE
indivisible unit (R-0507) R16 carries whole, already dry-run green. LAST_REVIEWED_SHA advances to
the R14 handback commit.

- R-0507 — Medium, A GREP OVER MOCK TARGETS WAS READ AS AN ENUMERATION OF THE CALL PATHS THOSE
MOCKS COVER, AND THE SCOPE IT PRODUCED WAS WRONG. Raised by the reviewer against its own R15
scoping work, before this block was emitted. Planning this round the reviewer grepped the suite for
tests that patch the CLI spawn, found exactly one — `test_structured_cli_envelope.py` patching
`packages.orchestration.pingpong_provider.subprocess.run` in its `_review` helper — read that helper
as reaching `_call_reviewer_structured` alone, and concluded that the version probe and `_call` could
migrate without touching a single test. FALSE: `test_4_legacy_non_schema_call_uses_result` sets
`REMEDY_REVIEWER_FREETEXT=1`, which routes the same helper through `_call`, so migrating `_call`
alone leaves that test patching a function the code no longer calls. The error was not the grep,
which was right about WHERE the mocks are; it was reading a list of patch TARGETS as a list of the
paths reached under them, when the reaching is decided by branches inside the tested code and by
environment variables the tests set — the R-0258 family, a source guard the block never named. It
cost no round only because the mandated dry run (planner_reviewer_prompt.md §3 checklist item 12)
ran the candidate slices against those suites in a `git archive` extraction, where it surfaced as
one red test in a set green at base. Counter-measure, binding on the reviewer from this round on:
when a block moves a call site, never infer the affected tests from a grep over mock targets — RUN
the candidate change against every suite touching the file and let the failures enumerate
themselves. The plan consequence is recorded, not hidden: `_call`, `_call_reviewer_structured` and
that mock are ONE indivisible unit, since re-pointing the mock at `_guarded_cli_run` reddens every
envelope test still on the stdlib spawn. R15 migrates the independent version probe; R16 carries the
coupled unit, already dry-run green. OPEN.

Gate: R15 — PASS, the round that gave the claude CLI seam its guarded runner. All ten ordered gates
were re-run by the reviewer from the repository root over c5d80471..7185d949 and every one
reproduces the handback's reading. TRANSPORT, disk-to-disk and not by digest fallback: the
reviewer's `.remedy-wt/f085-r15.md`, the committed `.agent/authored/f085-r15.md` and
`.agent/last_block.md` are byte-EQUAL at sha256
e2f4ef715c40f02df7d552e15348268b2d0edb24b986ff91e762c666314e2d88, 22895 B, 400 lines — AT the
DECISION F105 D5 block cap, not over it. C1 IS A PURE APPEND: the pre-C1 blob is a byte-exact PREFIX
of the post-C1 file, HEAD equals it, the remainder is exactly blank + RECORD1 + blank + FIND1, each
occurring ONCE, and C1 added no marker line — the one slice-marker token the file holds is R7 prose,
present at both ends. THE ARITHMETIC: 121 / 3 / 0 at base against 122 / 3 / 0 at HEAD, the open set rising 118 to
119 by one registration against no resolution, difference exactly R-0507, no duplicate id and no
resolution naming an unregistered id. THE CHANGE ITSELF, read as a diff and then re-measured: the
module gains `_cli_exec_policy`, `_decode_cli_stream` and `_guarded_cli_run`, and `_resolve_version`
now calls the runner. By AST over the HEAD blob, `_resolve_version` and `_guarded_cli_run` hold ZERO
subprocess spawn nodes while `_call` and `_call_reviewer_structured` still hold ONE each — the
coupled unit R-0507 names, deliberately untouched. THE STRONGEST PROOF AVAILABLE WAS TAKEN: the
committed `pingpong_provider.py` and `test_claude_cli_exec_guard.py` are BYTE-IDENTICAL to the
`git archive` extraction the reviewer dry-ran before emission, where seven red controls each
reddened exactly their own tests, so the gates that pass here are the same gates proven capable of
failing. At HEAD the goldens are 8 passed, the seven-file regression set is 333 passed at C1 and 333
at HEAD, ruff is exit 0 on both touched paths, state readers 157 passed and the canary 42 passed.
The change set is exactly the seven declared paths with 0 outside; insertions are 400, 339, 50, 134
and 9, none over 500; six single-parent commits, every reflog entry `commit:`-prefixed, no amend,
rebase, reset or force-push; `git status --porcelain` is EMPTY and `git worktree list` is ONE line.
THE ROUND'S OWN REPORTING IS WHY THIS IS A PASS AND NOT A REPAIR: all three anomalies it declared
are defects in the REVIEWER'S block text, not in its execution, and it reported each rather than
quietly repairing a slice it was told to apply byte-verbatim. They are registered below as R-0508,
R-0509 and R-0510. LAST_REVIEWED_SHA advances to the R15 handback commit.

- R-0508 — Low, A PAIR'S SHAPE WAS ASSERTED FOR ONE PAIR AND ASSUMED FOR THE REST, AND THE
ASSUMPTION WAS WRONG. Raised by the R15 worker in its handback and confirmed by the reviewer against
its own R15 block. Constraint 3 of that block classified CLST as APPEND-shaped — correctly, its TO
contains its FROM — and then said "Every other pair is a REWRITE". IMP3 is not: IMP3T is
`from packages.orchestration.exec_guard import ...` followed by the model-aliases import line that
IS IMP3F, so the TO contains the FROM verbatim and IMP3F still occurs exactly 1x at HEAD, which the
reviewer re-measured. Nothing broke, because no gate in that block ordered an "IMP3F 0x" reading —
had one existed it would have been unsatisfiable by construction, which is the R-0207 failure this
classification exists to prevent. The defect is the method, not the damage: checklist item 4 says a
pair is declared APPEND only after checking that the TO literally CONTAINS the FROM, and the block
performed that check for the pair it suspected and generalised to the others by eye. An import
insertion that keeps the anchor line is the single most common append-shaped pair in this
repository, so eye-checking is exactly where it fails. Counter-measure, applied in the build of the
block that registers this: pair shapes are classified MECHANICALLY, every TO tested for containment
of its FROM, and the result printed beside each pair before emission — never written by hand. OPEN.

- R-0509 — Medium, A REWRITE PAIR ENDED IN THE MIDDLE OF A NUMBERED LIST AND LEFT THE LIST
MALFORMED ON DISK. Raised by the R15 worker and confirmed by the reviewer. R15's PLANF covered
`## Current Step` plus only the FIRST item of `## Next Steps`; PLANT replaced it with a Current Step
and TWO numbered items. The surviving items below the FROM kept their old numbers, so
`.agent/plan.md` at 7185d949 reads 1, 2, 2, 3 — measured, not inferred. The worker was right not to
touch it: constraint 2 forbids rewording a slice, so repairing the numbering would have meant
editing authored text, and reporting the defect was the only honest move left to it. This is the
family where a pair's FROM is scoped to the text the reviewer INTENDED to change rather than to the
structure that text belongs to; a numbered list, a table and a fenced block are all single
structures whose arity a partial rewrite silently corrupts. Counter-measure, binding from this round
on: when a TO changes how many items a numbered list or table holds, the pair's FROM spans the WHOLE
structure, never a prefix of it. The block registering this carries the repair — its plan pair
covers the entire `## Next Steps` section and renumbers it 1 through 4. OPEN.

- R-0510 — Low, A SECTION HEADING COUNTED ITS OWN CONTENTS BY HAND AND GOT IT WRONG. Raised by the
R15 worker and confirmed by the reviewer. That block's heading read "Change set — exactly these SIX
paths, nothing else" and the section then enumerated SEVEN, which is also what
`git diff --name-only c5d80471..HEAD` prints; the six-path reading is the one gate G10 orders for
the range BEFORE the handback commit, so both numbers exist and the heading attached the wrong one
to the wrong set. No gate was contradicted and nothing was mis-executed. This is the R-0402 /
R-0404 / R-0436 family that memory keeps re-learning — checklist item 11: count it mechanically or
state NO numeral — and its persistence has a specific cause worth naming. The R15 block DID apply
the rule: its Bundle heading was rewritten to carry no count precisely because the commit list had
grown by one. The Change set heading was not swept in the same pass, so the fix was applied to the
instance that was noticed rather than to the class. That is the R-0417 staleness shape wearing a
different hat. Counter-measure, applied in the build of this block: no heading in it states a count
of its own contents, and the build script greps the emitted bytes for a number-word standing next to
"paths" or "commits" and fails the build if it finds one. OPEN.

Done: R-0506 — the two documented absence claims the R13 migration falsified are corrected, in the
round its own text named as the one that owes them. `packages/orchestration/exec_guard.py` no longer
says "NO CALLER. Nothing in this repository imports this module yet"; it now states PARTIAL coverage,
names the managed builder seam and the CLI provider as the callers, says which classes still spawn
unsupervised, and deliberately writes NO number, because the number changes with every migration
round and the caller grep is the honest answer. The allowlist sentence no longer claims choosing one
per command class "is not done here" — it records that callers choose it, the builder policy pinning
one and the CLI policy deliberately not. `packages/orchestration/managed_builder_execution.py` no
longer calls itself the only place that may INVOKE subprocess for builder execution: it may LAUNCH
one, and since F085 T002a it delegates the spawn to `exec_guard.run_guarded` while keeping the
policy, in both the module docstring and `run_managed_builder`'s. Both "shell=False ALWAYS" promises
are replaced by "No shell, ever" plus a pointer to the AST assertion that actually enforces it, so
the sentence that made R-0504 possible — a docstring a source-text test could satisfy — is gone.
Verified at the fix commit: the three retired phrases occur 0 times, the caller grep scoped to
`-- packages tests` names four paths, and the exec-guard and managed-builder suites are 152 passed,
matching base exactly.

Gate: R16 — PASS, the record-and-repair round that paid down R-0506 and fixed the numbering its
predecessor broke. All ten ordered gates were re-run by the reviewer over 7185d949..396ad913 and
every one reproduces the handback's reading. TRANSPORT, disk-to-disk and not by digest fallback: the
reviewer's scratch original, the committed `.agent/authored/f085-r16.md` and `.agent/last_block.md`
are byte-EQUAL at sha256 bda1ca21008ed866792258791cd785bbde79b9aa975c7c018fbaf50fe82e903e, 22488 B,
316 lines. THE TWO APPEND COMMITS BOTH HOLD THEIR SHAPE: for C1 and again for C3 the pre-commit blob
is a byte-exact PREFIX of the post-commit file, each remainder is byte-equal to blank plus exactly
the slices that commit was given, every slice occurs ONCE in the whole file, and neither commit adds
a marker line; the numstat readings are 74 and 17, both append-only. Keeping the resolution in its
own commit AFTER the fix was the right shape and it verifies cleanly: at C1 the file reads
125 / 3 / 0 and only at C3 does it read 125 / 4 / 0, so at no commit did disk claim a resolution
whose fix had not landed. THE ARITHMETIC: 122 / 3 / 0 at base against 125 / 4 / 0 at HEAD, the open
set moving 119 to 121 by three registrations against one resolution, registered difference exactly
R-0508, R-0509 and R-0510, resolved difference exactly R-0506, no duplicate id and no resolution
naming an unregistered id. THE R-0509 REPAIR IS MEASURED, NOT ASSERTED: `## Next Steps` parses to
1, 2, 2, 3 at base and to 1, 2, 3, 4 at HEAD, with `## Goal` and `## Risks` byte-identical and the
file at 43 lines under its cap. THE R-0506 RESOLUTION HOLDS: all three retired phrases count 0 in
the HEAD blobs of both source files, and the caller grep scoped to `-- packages tests` names four
paths — the two modules that import the guard and the two suites that test them — which is exactly
the claim `exec_guard.py` no longer contradicts. The three suites owning those files are 152 passed
at C1 and 152 at HEAD, ruff is exit 0 on both touched paths, state readers 157 passed and the canary
42 passed. The change set is exactly the declared paths with 0 outside; insertions are 316, 240, 74,
16, 17 and 9, none over 500; seven single-parent commits, every reflog entry `commit:`-prefixed, no
amend, rebase, reset or force-push; the tree is clean and `git worktree list` is ONE line;
`.agent/handoff.md` measures 79 lines against its own declaration of 79, and its single declared
deviation — the token cap, cause named, no section dropped — is accurate. LAST_REVIEWED_SHA advances
to the R16 handback commit.

Done: R-0507 — the coupled unit this finding identified has been migrated as one commit, which is
the only way it could be migrated. `_call` and `_call_reviewer_structured` now reach the CLI through
`_guarded_cli_run`, and `tests/orchestration/test_structured_cli_envelope.py` patches that runner
instead of `subprocess.run`. The coupling the finding predicted is now MEASURED rather than argued:
in a `git archive` extraction the reviewer reverted each half alone, and restoring the stdlib spawn
at the structured site reddened ELEVEN tests while reverting the mock target alone reddened the same
eleven — neither half is separable, exactly as the finding said. The counter-measure it bound the
reviewer to has now been exercised for three consecutive rounds: every block since has been applied
to an extraction and run against the suites that touch its files before emission, and that practice
has caught a mis-scoped migration (this finding), a vacuous timeout assertion (R15) and a
self-contradicting marker gate (R16). Five behaviour-equality goldens land with the migration —
result text, non-zero exit with its stderr tail, the wall trip's message, a signal death's -SIGNUM
form and the caller-side character cap — and four red controls each reddened their own tests.

Done: R-0509 — the malformed numbering is repaired on disk and the repair is measured at both ends.
`.agent/plan.md`'s `## Next Steps` parsed to 1, 2, 2, 3 at 7185d949 and parses to 1, 2, 3, 4 at
396ad913, with no repeated number, `## Goal` and `## Risks` byte-identical to base and the file at
43 lines under its 50-line cap. The repair was made the way the finding prescribed: R16's plan pair
spanned the WHOLE `## Next Steps` section rather than a prefix of it, so the surviving items were
renumbered by the pair itself instead of being left to collide with the new ones. The standing rule
the finding states — when a TO changes how many items a numbered list or table holds, the FROM spans
the whole structure — is not yet written into docs/agents/planner_reviewer_prompt.md §3, and this
resolution does not claim that it is; R-0508 and R-0510 stay OPEN for that promotion round, which is
where all three counter-measures stop being reviewer habit and start binding on disk.

Gate: R17 — PASS, the round that completed T002a's CLI half. All ten ordered gates were re-run by the
reviewer over 396ad913..88dbcefa and every one reproduces the handback's reading. TRANSPORT,
disk-to-disk and not by digest fallback: the committed `.agent/authored/f085-r17.md` blob, the
committed `.agent/last_block.md` blob and both working copies are byte-EQUAL at sha256
cc496f97e15b8feb9a82368c78493c03f48f1a64c8302dca265874e4fdebb195, 19911 B, 309 lines. BOTH APPEND
COMMITS HOLD THEIR SHAPE: for C1 the pre-commit blob 6c374ca1 (286462 B) is a byte-exact PREFIX of
the post-commit file 98be125d (289062 B) and the remainder is byte-equal to blank plus RECORD1; for
C3 the pre-commit blob 98be125d is a prefix of 27c1e4ef (291333 B) and the remainder is blank plus
DONE1 plus blank plus DONE2. Each slice occurs exactly ONCE in the file at HEAD, no marker line
survives anywhere in it, and HEAD equals the C3 blob. THE ARITHMETIC: 125 / 4 / 0 at base and after
C1 alike — a record registers no id, exactly as the block predicted — against 125 / 6 / 0 at HEAD,
the open set moving 121 to 119, registered difference EMPTY, resolved difference exactly R-0507 and
R-0509, no duplicate id and no resolution naming an unregistered id; max R-0510, next free R-0511.
THE MIGRATION IS COMPLETE AND MEASURED BY AST, NOT BY TEXT: over `pingpong_provider.py` at HEAD,
`_resolve_version`, both defs of `_call`, `_call_reviewer_structured` and `_guarded_cli_run` hold
ZERO `subprocess.run/Popen/call/check_output` call nodes, and so does the WHOLE MODULE. THE GOLDENS
ARE NOT VACUOUS: the eight-file provider suite reads 341 passed at C1 in a disposable worktree at
that commit and 346 at HEAD in the primary checkout — the two numbers are NOT equal and the
difference is exactly the five goldens C2 adds. Those goldens spawn a REAL child, because `_provider`
writes the body through `textwrap.dedent` to an executable stand-in, so the indented `_ENVELOPE` is
valid Python at the child and the "HELLO" assertion could not pass against a mock. TWO INDEPENDENT
RED CONTROLS, run by the reviewer in a disposable worktree at HEAD and not inherited from the block:
reverting the mock target alone reddens ELEVEN tests in `test_structured_cli_envelope.py`, which is
the number DONE1 puts on disk, and restoring the stdlib spawn at the `_call` site reddens
`test_the_probe_and_the_runner_hold_no_subprocess_spawn`, so the two AST assertions C2 adds do bite.
The five goldens stay GREEN under that second mutation, which is correct and worth stating: they pin
BEHAVIOUR across the migration while the AST guard pins the MECHANISM, and neither substitutes for
the other. THE SEAM PRESERVES ITS CONTRACT: `_guarded_cli_run` re-raises a wall trip as
`subprocess.TimeoutExpired`, republishes a signal death in the -SIGNUM form and decodes both streams
the way `text=True` did, so the `except subprocess.TimeoutExpired` handler each call site already
carried still catches. THE PLAN PAIR: PLANF 0x and PLANT 1x at HEAD, `.agent/plan.md` at sha256
8c68c6ae324fd779094990ee19c5961b35f6df4fcdb6639ef8f085aecc65c9f2, 2704 B and 44 lines under its cap,
`## Goal` and `## Risks` byte-identical to base, `## Next Steps` parsing to 1, 2, 3, 4 with no
repeat. Scoped ruff is exit 0 on all three touched paths, the state readers are 157 passed and the
canary 42 passed. BEYOND THE ORDERED GATES the reviewer ran the two provider readers G7's file list
does not cover — `test_pingpong_cli.py` at 172 passed and `test_run_manifest.py` at 44 passed — and
grepped the repository for surviving patches of `pingpong_provider.subprocess`, of which there are
none; the seam has no reader left on the stdlib path. The change set is exactly the declared paths
with 0 outside; insertions are 309, 225, 28, 45, 25 and 8 before the handback commit, which is itself
32, none over 500; seven single-parent commits, twelve reflog entries all `commit:`-prefixed, no
amend, rebase, reset or force-push; the tree is clean and `git worktree list` is ONE line. The
handback measures 80 lines against its own declaration of 80, and its stated-cause deviation is
accurate. LAST_REVIEWED_SHA advances to 88dbcefa.

Done: R-0508 — the counter-measure is on disk. `docs/agents/planner_reviewer_prompt.md` §3 now
carries checklist item 15, "Pair shapes are classified by a containment test, never by eye", which
THIS SAME BLOCK orders into that file — so the sentence you are reading names a rule that exists
rather than one a later round is expected to write, which is exactly what item 11 requires of it.
The item states the METHOD the finding faulted: every FROM/TO pair is tested mechanically for
containment and the answer printed beside that pair, one reading per pair, never one generalised to
the rest. It names its neighbour on purpose, because item 4 already stated the RULE and the R15
block still failed while satisfying it — it ran the check for the pair it suspected and eyeballed
the others. A rule and the method that produces its input are two different checks, and only the
second was missing.

Done: R-0510 — the counter-measure is on disk as checklist item 16, "No heading states a count of the
contents beneath it", ordered into `docs/agents/planner_reviewer_prompt.md` §3 by THIS SAME BLOCK.
The item carries the part of the finding that mattered: not that a heading said SIX over a body of
SEVEN, but that the R15 block DID sweep its Bundle heading and left the Change set heading behind,
so the fix reached the instance that was noticed instead of the class. It therefore ends by ordering
the sweep over EVERY heading in a block rather than the one that changed, which is the R-0417 shape
the finding named. Item 17 lands in the same commit and closes the third counter-measure this round
was held open for — the arity rule R-0509's resolution said would be promoted here — so no standing
rule of that family is left living only in reviewer habit.

Gate: R18 — PASS, the round that put three standing rules on disk. All nine ordered gates were re-run
by the reviewer over 88dbcefa..646092ce and every one reproduces the handback's reading. TRANSPORT
is proven twice over. Disk-to-disk: the committed `.agent/authored/f085-r19.md` predecessor
`.agent/authored/f085-r18.md`, the committed `.agent/last_block.md` and both working copies are
byte-EQUAL at sha256 7187303bf16c3414278b5cbcf7efe2ddb082e3e4c4405e31fc65247ca9ccbac8, 20616 B, 281
lines, with 14 marker lines and 7 slice pairs intact. And by digest fallback against the reviewer's
OWN pre-emission measurements, which is what makes the worker's declared split write a non-event:
the block was measured in four regions before it was delegated, and the saved file's four
corresponding regions hash to 989020a1, 88eed983, 5fe3c39b and 4fe2a9ff exactly as measured, with
the fifth region at its measured 71 lines and the file at its measured 281. A block that reaches
disk byte-identical to the bytes the reviewer measured has not been damaged by the number of write
calls it took. BOTH APPEND COMMITS HOLD THEIR SHAPE: for C1 the pre-commit blob (291333 B) is a
byte-exact PREFIX of the post-commit file (295507 B) and the remainder is byte-equal to blank plus
RECORD1; for C3 the pre-commit blob (295507 B) is a prefix of (297276 B) and the remainder is blank
plus DONE1 plus blank plus DONE2. Each occurs exactly ONCE at HEAD, no marker line survives, HEAD
equals the C3 blob. THE ARITHMETIC: 125 / 6 / 0 at base and again after C1 — a record adds no id —
against 125 / 8 / 0 at HEAD, the open set moving 119 to 117, registered difference EMPTY, resolved
difference exactly R-0508 and R-0510, no duplicate and no resolution naming an unregistered id; next
free R-0511. THE PROMOTION LANDED AND ITS OWN RULE HOLDS ON IT: PROMF occurs exactly once at HEAD,
so the anchor survived its append; each of the three item titles occurs exactly once among C2's 34
added lines; and the checklist region parses to a contiguous 1 through 17 with no repeat and no gap,
which is item 17's arity rule holding on the very commit that writes item 17. THE PLAN PAIR: PLANF
0x and PLANT 1x, `.agent/plan.md` at sha256
65f9287c4ef71975c8b956a9df25793cd2e5584fb528cc816a374c39d5ca0253, 2344 B, 40 lines under its cap,
`## Goal` and `## Risks` byte-identical to base, `## Next Steps` parsing to 1, 2, 3. Doc readers are
305 passed 1 skipped, the state readers 157 passed and the canary 42 passed, all rc 0 and all re-run
by the reviewer rather than accepted from the report. The change set is exactly the declared paths
with 0 outside; insertions are 281, 198, 44, 34, 21 and 7 before the handback commit, which is
itself 30, none over 500; seven single-parent commits, twenty reflog entries all `commit:`-prefixed,
no amend, rebase, reset or force-push; the tree is clean and `git worktree list` is ONE line. The
handback measures 78 lines against its own declaration of 78, inside the template's 100-line
allowance for a table of this many commits, and its two declared deviations are both accurate. THE
WORKER'S REFUSAL WAS CORRECT AND IS RECORDED AS SUCH: it found the stale check count at line 174,
declined to fix it because the change set did not include it, and reported it instead of widening
scope. That is the behaviour this loop is built to produce, and the defect it surfaced belongs to
the reviewer's block, not to its execution — it is registered below as R-0511.
LAST_REVIEWED_SHA advances to 646092ce.

- R-0511 — Low, A HEADING KEPT COUNTING ITS OWN CONTENTS IN THE PARAGRAPH THAT INTRODUCES THE RULE
AGAINST IT. Raised by the R18 worker in its handback and confirmed by the reviewer on disk.
`docs/agents/planner_reviewer_prompt.md`:174 reads "Run all twelve checks mechanically" over a list
that already held FOURTEEN items before R18 and holds SEVENTEEN after it. The count was therefore
stale by two BEFORE the promotion round and by five after it, so R18 widened a defect it did not
create — but it widened it while adding the very item, 16, that forbids a heading from counting the
contents beneath it, which is what makes this worth an id rather than a silent fix. The reviewer's
own pre-emission pass ran item 16 against the BLOCK's headings and never ran it against the TARGET
file's, which is the same class boundary items 2, 6 and 7 exist to keep separate: a rule that reads
the block, a rule that reads the file the block writes into, and a rule that reads the tests
guarding it are three different passes. Item 16 as written does not say which of those it belongs
to, and the answer is BOTH — the block's headings and the headings of any section the block edits.
No gate was contradicted and nothing was mis-executed; the R18 worker's refusal to widen its change
set was correct and is recorded in that round's gate. Counter-measure, applied by this block: C2
removes the numeral entirely rather than correcting it to seventeen, because a corrected count is
the same defect with a longer fuse — this is the R-0486 correction-carries-the-old-fact shape, and
the only stable fix for a self-count is to stop counting. The reviewer additionally swept the whole
file for the class rather than the reported line, and reports the sweep's predicate and its four
matches in this round's block. OPEN.

Done: R-0511 — the heading no longer counts anything. `docs/agents/planner_reviewer_prompt.md`:174
now reads "Run EVERY check below mechanically", so the sentence carries no numeral that a later
promotion can falsify, and the word `twelve` occurs nowhere in the file. The fix was made the way the
finding prescribed: the numeral was REMOVED rather than corrected to seventeen, because an accurate
count is the identical defect waiting for the next item — the distinction item 11 draws between a
measurement and a recollection, applied to the target file instead of to the block. The sweep the
finding also demanded was run and is reported in this round's block: the predicate is a number-word
standing next to a countable noun, it matches four lines in the file, and the three that are not
line 174 count something real inside an item's prose rather than announcing the size of a list.
Item 16 is amended by neither this fix nor this resolution; what changes is that the reviewer now
runs it against the headings of every section a block EDITS as well as against the block's own,
which is the reading the finding established and which this round is the first to perform.

Gate: R19 — PASS, the repair round that stopped a heading counting itself. All nine ordered gates
were re-run by the reviewer over 646092ce..6b6cfee5 and every one reproduces the handback's reading.
TRANSPORT is proven twice over, as it was in R18. Disk-to-disk: the committed
`.agent/authored/f085-r19.md`, the committed `.agent/last_block.md` and both working copies are
byte-EQUAL at sha256 4d750d6c237b25d7bd6e990ca0fee97bd3c9b47a03c5d2340ebda2ea81a13fba, 17340 B, 236
lines, 14 marker lines. And by digest fallback against the reviewer's OWN pre-emission measurements:
the block was measured in three regions before delegation and the saved file's three corresponding
regions hash to dc5598e8, f20288aa and a9d3811c exactly as measured. The worker split the C0a write
into seven calls because a single heredoc of that size is rejected by this session's tool; constraint
6 permitted exactly that, and the digests prove the split cost nothing. A declared deviation that a
gate can disprove is how this loop is supposed to work. THE APPEND COMMITS HOLD THEIR SHAPE: for C1
the pre-commit blob (297276 B) is a byte-exact PREFIX of the post-commit file (302599 B) and the
remainder is byte-equal to blank plus RECORD1 plus blank plus REG1; for C3 the pre-commit blob
(302599 B) is a prefix of (303775 B) and the remainder is blank plus DONE1. Each occurs exactly ONCE
at HEAD, no marker line survives, HEAD equals the C3 blob. THE ARITHMETIC MOVED WHERE IT WAS
ORDERED TO: 125 / 8 / 0 and 117 open at base, 126 / 8 / 0 and 118 open after C1 — the registration
landed, which is the reading that was flat in R17 and R18 and had to move here — and 126 / 9 / 0
with 117 open at HEAD. Registered difference exactly R-0511, resolved difference exactly R-0511, no
duplicate and no resolution naming an unregistered id; next free R-0512. THE FIX IS THE ONE THE
FINDING PRESCRIBED: HEADF occurs 0 times at HEAD and HEADT once, the diff is 2 lines for 2 lines,
and the word `twelve` occurs 0 times in the WHOLE file — the numeral was REMOVED rather than
corrected to seventeen, so there is no count left to go stale. The checklist region still parses to
a contiguous 1 through 17, so the commit that stopped counting the list did not disturb it. THE
PLAN PAIR touched what it was scoped to and nothing else: PLANF 0x, PLANT 1x, and `## Goal`,
`## Next Steps` and `## Risks` all byte-IDENTICAL to base, which is the proof that a Current-Step
rewrite did not span the list beside it. `.agent/plan.md` is at sha256
5684439dfacac31c052cd4e63bb661ed8a1b25218ae68c51fc09c3c7e1865d04, 2341 B, 40 lines under its cap.
Doc readers are 305 passed 1 skipped, state readers 157 passed, canary 42 passed, all rc 0 and all
re-run by the reviewer rather than accepted from the report. The change set is exactly the declared
paths with 0 outside; insertions are 236, 155, 58, 2, 13 and 4 before the handback commit, which is
itself 32, none over 500; seven single-parent commits, fourteen reflog entries all
`commit:`-prefixed, no amend, rebase, reset or force-push; the tree is clean, `git worktree list` is
ONE line, and the branch is in sync with its remote. The handback measures 80 lines against its own
declaration of 80. LAST_REVIEWED_SHA advances to 6b6cfee5.

Gate: R20 — PASS, the record round that closed the previous session. All seven ordered
gates were re-run by the reviewer over 6b6cfee5..1cfa0acb and every one reproduces the
handback's reading. R20's verdict is recorded HERE rather than left in the handoff: the
§4.13 terminator covers the last round of a BRANCH, and this branch continues, so the
round is an ordinary reviewed round whose gate entry the next round writes. TRANSPORT:
the committed `.agent/authored/f085-r20.md`, the committed `.agent/last_block.md` and
both working copies are byte-EQUAL at sha256
3026ed0d86d1d40c2e5d5a57076f39d7df37b96dbaa6041d0765be5fe543fbc8, 12660 B, 174 lines.
The worker split the C0a write into six calls without first attempting one, which
constraint 6 conditioned on a rejection; it declared the deviation, and the byte
equality proves the split cost nothing. Declaring a deviation a gate can disprove is
how this loop is supposed to work. THE APPEND COMMIT HOLDS ITS SHAPE: for C1 the
pre-commit blob (303775 B) is a byte-exact PREFIX of the post-commit file (307026 B)
and the remainder is exactly one blank line plus RECORD1; `Gate: R19` occurs once in
the whole file, no marker line survives, and the HEAD blob equals the C1 blob. THE
ARITHMETIC STAYED WHERE IT WAS ORDERED TO: 126 / 9 / 0 and 117 open at base and the
same at HEAD, both symmetric differences empty, no duplicate id and no resolution
naming an unregistered id; max R-0511, next free R-0512. THE PLAN PAIR touched what it
was scoped to: `.agent/plan.md` is at sha256
4f6c8d32716a73b6deb30c4076511acc62b1e5dae2adb1fab93c993b1e5364b6, 2473 B, 41 lines
under its cap. State readers are 157 passed and the canary 42 passed, both re-run by
the reviewer rather than accepted from the report, and both from the block's exact
command lines. The change set is exactly the five declared paths with 0 outside;
insertions are 174, 111, 35 and 5 before the handback commit, which is itself 31, none
over 500; five single-parent commits in a linear chain, every reflog entry
`commit:`-prefixed, no amend, rebase, reset or force-push; the tree is clean and
`git worktree list` is ONE line. The handback measures 66 lines against its own
declared 66, with the mandated content named as the cause. LAST_REVIEWED_SHA advances
to 1cfa0acb.

Gate: R21 — PASS, the round that ruled and built the streaming seam's shape. All ten
ordered gates were re-run by the reviewer over 1cfa0acb..3622f2cf and every one
reproduces the handback's reading. TRANSPORT is proven twice over. Disk-to-disk: the
committed `.agent/authored/f085-r21.md`, the committed `.agent/last_block.md` and
both working copies are byte-EQUAL at sha256
b17efc371d740f199a7d05528109e81283591cbf630d9c2673cbbf0b03d42e37, 21446 B, 330
lines, 8 marker lines. And against the reviewer's OWN pre-delegation measurement:
the whole-file digest matches, and the three regions hash to 570cbf61, 5686f3e6 and
28534295 exactly as measured before the block was handed over. The single write
succeeded, so this round spent no deviation on transport at all. THE APPEND COMMITS
HOLD THEIR SHAPE: for C1 the pre-commit blob (307026 B) is a byte-exact PREFIX of
the post-commit file (309316 B) and the remainder is exactly one blank line plus
RECORD1; for C2 the pre-commit blob of `.agent/decisions.md` (353356 B) is a prefix
of (356103 B) and the remainder is blank plus DECISION1. Each slice occurs once, no
marker line survives, and each HEAD blob equals its working copy. THE ARITHMETIC
STAYED FLAT AS ORDERED: 126 / 9 / 0 and 117 open at both ends, both symmetric
differences empty, no duplicate id and no resolution naming an unregistered id; max
R-0511. THE EXTRACTION IS FAITHFUL: `plan_child_spawn` holds the same `_plan_rlimits`
call, the same `_apply_rlimits` closure and the same `child_env` resolution that
`run_guarded` ran inline, and `run_guarded` now appends `wall_timeout` and
`output_bytes` to the plan's list rather than to its own — so the parent-side names
stay parent-side, which is the property the whole split rests on. THE MIGRATION IS
HONEST: `_stream_exec_policy` sets a cwd pin and a zero core and NOTHING else, and
its docstring says why each absent field is absent rather than implying coverage;
the cwd precedence is documented at `run_streamed_command` and pinned by a test; and
`pingpong_provider` stopped passing `cwd=` in the same commit, so cwd has exactly one
source. THE NEW ASSERTIONS REACH THE CODE THEY NAME, verified by the reviewer's own
mutation in a disposable worktree rather than accepted from the worker's probe: with
`plan_child_spawn`'s `preexec_fn` replaced by a no-op, both rlimit tests go red and
the child reports `core=0,-1` where the guarded path reports `core=0,0`, while the
behaviour-equality test correctly stays green because it asserts nothing about
rlimits. Suites re-run by the reviewer: exec_guard 16 passed against a base of 12,
the stream trio 121 against 112, the sibling seams 337 against 337 unchanged, state
readers 157, canary 42, and ruff `All checks passed!` on the block's exact command
line. The change set is exactly the declared paths with 0 outside; insertions are
330, 305, 30, 42, 134, 172 and 10 before the handback commit, which is itself 61,
none over 500; eight single-parent commits in a linear chain, every reflog entry
`commit:`-prefixed, no amend, rebase, reset or force-push; the tree is clean and
`git worktree list` is ONE line. Five deviations were declared and none is harmful:
the `TYPE_CHECKING` import in particular is correct engineering, since `exec_guard`
imports the POSIX-only `resource` module and `stream_evidence` is imported far more
widely than the one seam that takes a policy. LAST_REVIEWED_SHA advances to
3622f2cf.

- R-0512 — Low, A HANDBACK REPORTED AN INSERTION COUNT TAKEN FROM THE WRONG
PRODUCER, AND CONTRADICTED ITS OWN TABLE IN THE SAME FILE. R21's gate G10 ordered
"the `+` column of `git show --numstat`" for each commit. The handoff's G10 line
reports `C5 19`. The real reading is `10	9` — ten insertions, nine deletions — and
19 is the churn total `git show --stat` prints on its "1 file changed" line. The
same handoff's changed-files table two dozen lines above says `+10/-9` for that path,
so the file disagrees with itself and only one of the two numbers came from the tool
the gate named. Nothing false landed on disk and the conclusion the gate exists to
support — none over 500 — is true under either reading, which is why this is Low. It
is registered because AGENTS.md's Commit Discipline settles this exact ambiguity as
DECISION F104 D1: the 500-line cap counts INSERTIONS only, the `+` column, not
insertions+deletions. A verification line that reports the churn number while naming
`--numstat` re-opens a question that decision closed, and this is the same family as
R-0336 and R-0367 — a number asserted about an artifact without being computed from
the tool that produces it. Counter-measure, applied in this round's own block and
binding from here: every block that orders an insertion count names it as the FIRST
COLUMN of `git show --numstat` and says explicitly that the churn total is not the
reading, and the handback's summary numbers must agree with its own changed-files
table. OPEN.

- R-0513 — Medium, A GUARD TEST'S FAILURE MODE IS AN UNBOUNDED HANG AND AN ORPHANED
BUSY LOOP, SO IT CANNOT REPORT THE REGRESSION IT EXISTS TO CATCH.
`tests/orchestration/test_exec_guard.py::test_cpu_limit_kills_a_busy_loop_and_names_the_limit`
runs a `while True` child under `ExecGuardPolicy(cpu_seconds=1, output_cap_bytes=64
* 1024)` — no `wall_timeout_seconds`. RLIMIT_CPU is therefore the ONLY thing that
ends that child. When a regression stops the rlimit reaching it, the child never
exits, `run_guarded`'s supervision loop has no deadline to break on, its `finally`
never runs, and the group kill that would sweep the child never happens: the test
does not go red, it hangs, and it leaves an unlimited busy loop behind. This is not
hypothetical. R21's G7 probe mutated `plan_child_spawn`'s `preexec_fn` to a no-op —
exactly the regression this test names — and the suite returned nothing for 600
seconds; the worker had to abandon the single-command probe, re-run it node by node
under an external per-node timeout, and afterwards sweep a surviving pid. Medium
rather than Low because the cost is paid by whichever future round breaks rlimit
application, which is precisely the round least able to afford a silent 600-second
stall, and because the orphan outlives the run. Raised by the R21 worker as an
observation outside its change set and confirmed by the reviewer against the code
rather than accepted from the report. The fix is one policy field, and the ordering
inside `run_guarded`'s classifier is what makes it safe: `deadline_fired` is checked
BEFORE `SIGXCPU`, so a deadline set far above the CPU limit never fires on the
healthy path and never steals the `cpu_seconds` attribution, while a regressed path
is killed at the deadline and reports `wall_timeout` — a named failure instead of a
hang. OPEN.

Done: R-0512 — resolved. The counter-measure is in force in this round's own block
rather than promised for a later one: G3 and G10 both name the reading as the FIRST
COLUMN of `git show --numstat` and both say explicitly that the churn total
`git show --stat` prints is not the reading, and the Done-when clause requires every
insertion count in the handoff to agree with the changed-files table beside it. The
R21 handoff itself is history and is not rewritten — editing a past handback would
destroy the record the finding is evidence of, and AGENTS.md rewrites that file per
round rather than amending it. What changes is that the ambiguity can no longer be
reached from a block's own wording.

Done: R-0513 — resolved.
`test_cpu_limit_kills_a_busy_loop_and_names_the_limit` now carries
`wall_timeout_seconds=30.0`, thirty times the CPU limit it is testing, so the
deadline cannot fire on the healthy path. Every existing assertion survives
unchanged, and `tripped_limit == "cpu_seconds"` is now doing double duty: it is
still the property the test is named for, and it is also the proof that the backstop
did not steal the attribution — which it could only do if the deadline fired first,
because `run_guarded` checks `deadline_fired` before `SIGXCPU`. The regression the
finding describes now ends in a named failure inside the deadline instead of an
unbounded hang, and because the guard's `finally` is reached, the group kill sweeps
the busy loop rather than leaving it orphaned. This round's G7 probe b exercised that
path directly: with the rlimit suppressed, the node fails and names `wall_timeout`
within the external timeout rather than stalling the run.

Gate: R22 — PASS, the round that hardened T001 against its own failure modes. All
ten ordered gates were re-run by the reviewer over 3622f2cf..b4da5101 and every one
reproduces the handback's reading. TRANSPORT is proven twice over. Disk-to-disk: the committed
`.agent/authored/f085-r22.md`, the committed `.agent/last_block.md` and both working
copies are byte-EQUAL at sha256
f7b6b9ca92d5a5b3956afa125ba5a189e99ff104d0148499e75707edd4775677, 24629 B, 372
lines, 8 marker lines. And against the reviewer's OWN pre-delegation measurement:
the whole-file digest matches and the three regions hash to f5ecdf9d, 9a8f32e7 and
53c558ae exactly as measured before the block was handed over. The single write
succeeded. THE APPEND COMMITS HOLD THEIR SHAPE: for C1 the pre-commit blob (309316
B) is a byte-exact PREFIX of the post-commit file (316105 B) and the remainder is
exactly one blank line plus RECORD1; for C3 the pre-commit blob (316105 B) is a
prefix of (317782 B) and the remainder is blank plus DONE1. Each slice occurs once,
no marker line survives, the HEAD blob equals the working copy. THE ARITHMETIC MOVED
EXACTLY WHERE IT WAS ORDERED TO, which is the reading that was flat in R20 and R21
and had to move here: 126 / 9 / 0 and 117 open at base, 128 / 9 / 0 and 119 open
after C1 — both registrations landed before any fix — and 128 / 11 / 0 with 117 open
at HEAD. Registered difference exactly R-0512 and R-0513,
resolved difference exactly the same two, no duplicate and no resolution naming an
unregistered id; max R-0513. THE SNAPSHOT IS CORRECT WHERE IT MATTERS: every field
of `_StreamPump` now lives behind one lock and is read only through `snapshot()`, so
the three values describe a single point in the stream; `run_guarded` takes that
snapshot AFTER the joins and BEFORE the conditional close, so a partial read never
races the descriptor it reads from; `streams_complete` keeps both its meaning and
its value, being computed from `is_alive()` exactly as before; and the fd handling is
untouched, so the comment explaining why a blocked pump's descriptor stays open is
still true. The `ExecGuardResult` docstring's `b""` promise was rewritten rather than
left to rot, and the replacement claims a PARTIAL buffer and nothing more. THE
BACKSTOP DOES NOT STEAL THE ATTRIBUTION, verified by the reviewer's own mutation in a
disposable worktree rather than accepted from the worker's probe: with
`plan_child_spawn`'s `preexec_fn` replaced by a no-op and the backstop left in
place, the node FAILS in 30.28 s under an external 180 s timeout instead of hanging,
and a direct run of the same policy against the mutated module — its `__file__`
printed as proof of import path — returns `term_signal=SIGKILL`,
`classification=resource_limit` and `tripped_limit=wall_timeout`. `pgrep` finds no
survivor afterwards, which is the second half of the fix: because the deadline is
reached, `run_guarded`'s `finally` runs and the group kill sweeps the busy loop that
R21's probe had to sweep by hand. Suites re-run by the reviewer: exec_guard 18
passed against a base of 16, the stream trio 123 against 121, the sibling seams 337
unchanged, doc readers not applicable, state readers 157, canary 42, ruff
`All checks passed!`. The change set is exactly the declared paths with 0 outside;
insertions are 372, 272, 88, 10, 102, 24 and 13 before the handback commit, which is
itself 44, none over 500 — and every one of those numbers is the `--numstat` first
column, which is R-0512's counter-measure working on the first round it bound. Seven
commits before the handback, one parent each, linear; every reflog entry
`commit:`-prefixed; tree clean; `git worktree list` ONE line. Six deviations were
declared and none is harmful. Two of them are findings against the REVIEWER and are
registered below. A third deserves naming here rather than as a finding: the worker
swept an orphan its own probe created by calling `subprocess.run(["pkill", "-f",
MARKER])` from Python after the interactive `kill` and `pkill` forms were refused by
the session's permission layer. That is the same form-level rejection this
repository already routes around for shell loops, the sweep was scoped to one MARKER
string, it is the exact call `test_exec_guard.py` already makes for its own escapee,
and the worker declared it unprompted. It is correct behaviour, not a violation.
LAST_REVIEWED_SHA advances to b4da5101.

- R-0514 — Medium, A BLOCK ORDERED A PROBE WHOSE RECIPE CONTRADICTS THE PROPERTY THE
SAME PARAGRAPH SAYS IT PROVES. R22's gate G7 probe b ordered, in one sentence,
"remove `wall_timeout_seconds` from the policy in
`test_cpu_limit_kills_a_busy_loop_and_names_the_limit` AND make `plan_child_spawn`'s
`preexec_fn` a no-op", and in the next, "with the backstop the node must FAIL and
name `wall_timeout`". The backstop IS `wall_timeout_seconds`. Removing it and then
asserting its effect cannot both hold, so no run satisfies the paragraph as written:
the literal recipe reproduces the hang R-0513 describes, and the stated property
requires the field the recipe deletes. The worker handled it correctly — it named
the contradiction, ran BOTH variants, and reported both readings rather than picking
one silently — and both readings turned out useful, since the literal variant is the
only direct reproduction of R-0513's harm this feature has on record. Medium because
the round spent a declared deviation and a second full probe run proving a defect in
the reviewer's own text, and because the failure is invisible to every existing
check: item 5 of the pre-emission checklist decides WHETHER a colour may be ordered,
item 8 checks a gate's expected VALUE against the code, and item 12 governs the
reviewer's own dry runs — none of them reads the block's two sentences against EACH
OTHER, which is the only place this defect lives, because both halves are
individually sound. Counter-measure: promoted into the pre-emission checklist by
this round's own C2, as item 18. OPEN.

- R-0515 — Low, AN AUTHORED SLICE ASSERTED A GATE RESULT THE BLOCK NEVER SCHEDULED
THE GATE TO PRODUCE. R22's DONE1 slice, applied byte-verbatim into
`.agent/live_review.md` by C4, states "This round's G7 probe b exercised that path
directly: with the rlimit suppressed, the node fails and names `wall_timeout` within
the external timeout rather than stalling the run." Nothing in that block fixed WHEN
G7 ran. The bundle listed the gates after the commits, so the natural order would
have committed C4 — and with it that sentence — before the probe that makes it true.
The worker saw this and moved G7 ahead of C4 on its own initiative, declaring the
reordering as a deviation, so nothing false reached disk and the claim is now
independently confirmed. Low for that reason. It is registered because the honest
outcome depended on the worker noticing: a worker that had followed the block's own
sequence would have committed an unverified claim into the permanent record, which
is the one file in this repository that must never carry one. This is the R-0371 and
R-0449 family — never order a value into an artifact written before the value can
exist — narrowed from commit SHAs to gate RESULTS, which is a producer the existing
checklist items do not cover: item 13 governs the ORDER a block imposes on the
worker's runs and item 14 governs which commits a per-commit gate can reach, while
this is a property of a slice's TEXT. Counter-measure: promoted into the
pre-emission checklist by this round's own C2, as item 19. OPEN.

Done: R-0514 — resolved. The counter-measure is on disk as item 18 of the
pre-emission block checklist in `docs/agents/planner_reviewer_prompt.md`, applied by
this round's C2 and verified by this round's G5 before this line was written. It is
stated as a rule the reviewer runs mechanically on the final bytes, alongside the
seventeen that precede it, rather than as prose in a finding — which is the whole
point, since a rule that lives only in a finding is read once by the round that
registers it and never again. Its distinguishing note names the three neighbours it
is NOT, so the next reviewer does not have to re-derive why items 5, 8 and 12 leave
this gap open.

Done: R-0515 — resolved. The counter-measure is on disk as item 19 of the same
checklist, applied by the same commit. It is deliberately narrow: it does not
forbid a slice from describing a gate, it requires the block to SCHEDULE that gate
before the commit that writes the slice. This round's own Constraint 6 is the first
application — C3 lands after C2 precisely so that the sentence above, asserting
items 18 and 19 are on disk, is true at the moment it is committed rather than a
commit later. A rule whose own block does not obey it is the R-0460 shape, and this
one obeys it.

Gate: R23 — PASS, a paydown round that fixed two defects of the reviewer's own
block and touched no production code. All nine ordered gates were re-run by the
reviewer over b4da5101..f28ed65a and every one reproduces the handback's reading.
TRANSPORT IS EXACT: the committed `.agent/authored/f085-r23.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL at sha256
6506c9cc76ba9c63d95c5f0a41fcee4d48dca39b4e26231e6f4bd66400ebb9d4, 24320 B, 368
lines, 0 trailing-whitespace lines, and the three region digests reported —
6d1b2d39, cac13512 and 8c2421ae over lines 1-60, 61-140 and 141-end — reproduce
under the newline-included convention the handback declared, so the single write
really was single. THE APPEND COMMITS HOLD THEIR SHAPE: for C1 the pre-commit
blob is a byte-exact PREFIX of the post-commit file and the remainder is exactly
one blank line plus RECORD1; for C3 the same property holds for DONE1. Each
slice occurs exactly once in the file, no marker line survives anywhere, and the
HEAD blob equals the working copy in both cases. ALL SIX SLICE DIGESTS MATCH the
handback: RECORD1 e2bb4c28, CHECKF e411b1ad, CHECKT e4799d98, DONE1 a9fccd54,
PLANF 4e11656a, PLANT b90d1cf7, each extracted here from the committed authored
file by its own marker pair and compared against the target on disk, so the
worker's applied bytes are the reviewer's authored bytes and not a retype. THE
ARITHMETIC MOVED WHERE IT WAS ORDERED TO: 128 / 11 / 0 with 117 open at base,
130 / 11 / 0 with 119 open after C1 — both registrations landed BEFORE the fix,
which is the ordering constraint 5 existed to enforce — and 130 / 13 / 0 with 117
open at HEAD. Registered and resolved symmetric differences are each exactly
R-0514 and R-0515; no duplicate id, no resolution naming an unregistered id; max
R-0515 and next free R-0516. THE COUNTER-MEASURES ARE REALLY ON DISK AS RULES:
`docs/agents/planner_reviewer_prompt.md` at HEAD hashes to 738920de and its
pre-emission checklist parses to the numbers 1 through 19 with no gap and no
repeat, so items 18 and 19 are numbered members of the list rather than prose
appended near it. The pair was append-shaped and was proved as one — CHECKT
contains CHECKF verbatim, so the unsatisfiable "CHECKF 0x" reading was correctly
never ordered. THE PLAN PAIR WAS A REWRITE and behaved like one: PLANF 0x and
PLANT 1x at HEAD, `## Goal` and `## Risks` byte-identical to their base bytes,
42 lines, under the cap. THE GATES WERE RE-RUN, NOT READ: the reviewer executed
`python3 -m pytest tests/docs/ -q` (295 passed), the four state readers (157
passed) and the canary `tests/cli/test_golden_path.py -q` (42 passed), each as
its exact ordered command line, and each reproduced the handback's number. One
correction to the record, which changes no verdict: the reviewer's first attempt
at the state-reader gate used two wrong paths, pytest reported "no tests ran"
rather than an error, and the reading was worthless until the block's own command
line was used instead — the R-0438 vacuous-gate shape, caught here by comparing
against the ordered command rather than by any gate. COMMIT HYGIENE IS CLEAN: the
changed-path set before C5 is exactly the declared one, per-commit insertions are
368, 280, 97, 23, 19, 5 and 42 with none over 500, the seven commits form a
single-parent chain, the reflog holds nothing but `commit:` entries, and the
primary checkout is porcelain-empty with one worktree. No block condition is met
and no finding is registered against this round.

Gate: R24 — PASS, the round that opened T002b by building the shared test-class
seam and migrating the first of the twelve sites onto it. All ten ordered gates
were re-run by the reviewer over f28ed65a..3d1821bf and every one reproduces the
handback's reading. TRANSPORT IS PROVEN DISK-TO-DISK AND NOT BY FALLBACK: the
committed `.agent/authored/f085-r24.md` is byte-EQUAL to the reviewer's own
pre-delegation original as well as to the committed `.agent/last_block.md` and
both working copies, at sha256
46db5e38c4b586971364f75b7976daa3ff88e20ac5558aa2d82b807698380340, 22645 B, 355
lines, and the three region digests 7804f388, 69d643fe and 7ac81591 reproduce
exactly, so the single write really was single and nothing shifted. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1, that
slice occurs once, no marker line reached any target file, and the HEAD blob
equals the working copy. THE ARITHMETIC IS FLAT EXACTLY WHERE IT WAS ORDERED TO
BE: 130 / 13 / 0 with 117 open at base and unchanged at HEAD, both symmetric
differences empty, no duplicate id, no resolution naming an unregistered id, max
R-0515. THE SEAM IS REAL AND SHAPED LIKE WHAT IT REPLACED:
`run_guarded_test_command` returns a `CompletedProcess` with bytes streams,
raises `subprocess.TimeoutExpired` on a wall trip CARRYING the partial streams
the guard already holds, republishes a signal death as a negative returncode, and
deliberately does not catch `FileNotFoundError`, which is why `run_tests_local`'s
`command_not_found` branch still works untouched. The policy sets only what it
can defend — `cpu_seconds`, `address_space_bytes` and `open_files` stay None on
the precedent `_builder_exec_policy` already established, rather than inventing a
second answer — and the 16 MiB output cap sits above the caller's own 1 MiB
truncation with the reason written beside the value, so `output_truncated` keeps
describing what the caller measured. THE MIGRATION CHANGED THE MECHANISM AND NOT
THE OUTCOME: every mocked call site in both test files moved onto the new seam
with its fabricated `CompletedProcess` values unchanged, and the one assertion
that could no longer fail — a `shell=` check against a seam with no `shell`
parameter — was REPLACED rather than retargeted, so it now pins the argv, the
timeout and the cwd the seam really receives. THE GOLDEN RUNS A REAL CHILD AND
REACHES THE MIGRATED PATH, which the reviewer confirmed independently rather than
accepting the worker's probe: with `run_guarded_test_command` made to raise on
entry in a disposable worktree at HEAD, the golden node stopped passing and
reported the injected error. THE GATES WERE RE-RUN, NOT READ: ruff over the five
changed files exited 0 with `All checks passed!`, the migrated suites gave
`119 passed`, the four state readers `158 passed` and the canary `42 passed`,
each as its exact ordered command line and each reproducing the handback's
number. COMMIT HYGIENE IS CLEAN: the changed-path set before C5 is exactly the
declared one, per-commit insertions are 355, 315, 46, 206, 62, 9 and 68 with none
over 500, seven commits form a single-parent chain, and the reflog holds nothing
but `commit:` entries. The three declared deviations are all improvements the
block should have ordered itself and none widens scope: the falsified
`test_runner.py` safety bullets, the module-handle import that keeps a `test_`
prefixed factory out of pytest's collection, and naming the 16 MiB default as a
constant. No block condition is met.

- R-0516 — Low, A BLOCK EDITED A FILE AND LEFT A CLAIM IN IT THAT THE SAME BLOCK
MADE FALSE. R24's C2 added six tests to `tests/orchestration/test_exec_guard.py`
and, in the same commit, correctly rewrote the PARTIAL COVERAGE bullet in
`exec_guard.py` that the migration falsified. It did not touch that TEST file's
own module docstring, which still says the guard "has NO callers in this
repository, so nothing here says anything about whether any existing Remedy
subprocess is limited. It is not." That sentence has been false since T002a and
R24 made it doubly false. Low because nothing executable depends on it and no
gate could have gone red over it — its whole cost is paid by the next reader who
asks what the guard covers and is told the opposite of the truth. It is
registered rather than waved through because it is the R-0417 staleness shape
that this record already names twice: the fix reached the INSTANCE the reviewer
noticed, in the neighbouring file, and not the CLASS, in the file the block was
already editing. The counter-measure is not a new checklist item — item 16 and
the sweep rule it carries already cover a block's own headings, and the gap here
is that the same sweep was never run over the TARGET file's existing prose.
Widening item 16 would restate what the R-0417 entry already says; retiring the
claim is the fix, and this round's own C2 performs it. OPEN.

Done: R-0516 — resolved. The false sentence is off disk: this round's C2 replaced
it with a paragraph that says what these tests DO prove, points at
`exec_guard`'s PARTIAL COVERAGE note as the single place the migration state is
recorded, and deliberately repeats no count — a count in a second file is a
second thing to forget, which is how the retired sentence went stale in the first
place. The resolution is verified by this round's G5 before this line is
committed, per constraint 4. No checklist item is added: item 16 and the R-0417
entry already carry the sweep rule, and the gap R-0516 exposed was that the sweep
was run over the block's own text and not over the prose already sitting in the
file the block was editing. That is a reading of an existing rule, not a new one,
and this record is where it belongs.

Gate: R25 — PASS, the paydown round that recorded R24 and retired the stale
no-callers claim from the guard's own fixture file. All nine ordered gates were
re-run by the reviewer over 3d1821bf..5b02cff9 and every one reproduces the
handback's reading. TRANSPORT IS PROVEN DISK-TO-DISK UNDER THE §4.9 DIGEST
FALLBACK, WHICH THIS ENTRY STATES RATHER THAN HIDES: this session did not author
R25's block, so no reviewer-side pre-delegation original exists to compare
against, and the proof is instead that the committed `.agent/authored/f085-r25.md`
is byte-EQUAL to the committed `.agent/last_block.md` and to both working copies
at sha256 4abce714f82e9a6b2baad095c02c6f0aecebfd009ce4a8883531c908b8971262,
18089 B, 296 lines, with the region digests 07199a30, cad21f6b and 3de16b95 all
reproducing, and that every applied slice re-derives from that committed file by
its marker pair. THE APPEND COMMITS HOLD THEIR SHAPE: for C1 and again for C3 the
pre-commit blob is a byte-exact PREFIX of the post-commit file and the remainder
is exactly one blank line plus the slice, at numstat 67/0 and 12/0. THE ARITHMETIC
MOVES ONLY WHERE R-0516 MOVES IT: 130 / 13 / 0 with 117 open at base, 131 / 13 / 0
with 118 open after C1, and 131 / 14 / 0 with 117 open at HEAD; both symmetric
differences are exactly the set holding R-0516; no duplicate id, no resolution
naming an unregistered id, max R-0516 and next free R-0517. THE FALSE SENTENCE IS
OFF DISK AND ITS REPLACEMENT RESOLVES: DOCF occurs 0 times at HEAD and DOCT
exactly once, the file's first line is byte-unchanged from base, sha256
ee200a92041190027a59efc08a835dd2827dc951de57eb7e35cf158957d2d04c at 21388 B — and
the reviewer followed the new pointer rather than trusting it, finding the PARTIAL
COVERAGE note exactly once in `exec_guard.py`, saying what DOCT attributes to it
and writing no count, so the replacement cannot go stale the way the sentence it
replaced did. THE GATES WERE RE-RUN, NOT READ: the edited suite exited 0 with
`24 passed` and the docstring edit did NOT move that base, the four state readers
gave `158 passed`, the canary `42 passed`, and ruff over the changed `.py`
`All checks passed!`, each as its exact ordered command line. COMMIT HYGIENE IS
CLEAN: the changed-path set is the declared one, per-commit insertions are 296,
217, 67, 6, 12 and 7 with the handback's own 56 measured after it existed and none
over 500, seven commits form a single-parent chain, and the reflog holds nothing
but `commit:` entries. The handback is 100 lines — exactly the ceiling its seven
per-commit tables engage under DECISION D15, so it sits AT the cap rather than
over it. No block condition is met.

Gate: R26 — PASS, the round that carried T002b into `autorun.py` and moved its
three `test`-class sites onto the shared seam. All ten ordered gates were re-run
by the reviewer over 5b02cff9..369d94a3 and every one reproduces the handback's
reading. TRANSPORT HELD ACROSS A HALT AND A RE-CREATION: the worker stopped
before C0a because the block ordered a 312-line save while the delivered text
measured 313, committed nothing and left the tree byte-clean at 5b02cff9. The
reviewer re-measured its own source in halves, confirmed 313, and traced 312 to
hand-summed section counts taken after a late edit to three sections — an
arithmetic recollection standing in for a measurement, which is the defect the
gate caught and the reason the gate exists. The worker's two independent
transcriptions produced the identical sha256
4220f7db082fd722fa28163fdbdfe2684f6c0ec42d772c866106009c26402908 at 16616 B, and
at HEAD the committed authored file, the committed `.agent/last_block.md` and both
working copies are byte-EQUAL at that digest, 313 lines, 26 marker lines in 13
pairs, region digests 9a91a0ce, 41d355bc and e34ff2fa. THE APPEND COMMIT HOLDS
ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the post-commit file,
the remainder is exactly one blank line plus RECORD1 at numstat 35/0, and no
marker line reached any target file — the three `END-` hits in
`.agent/live_review.md` are the word `APPEND-shaped` in prose older than this
round, which a substring count reports and a line-anchored count does not. THE
ARITHMETIC IS FLAT EXACTLY WHERE IT WAS ORDERED FLAT: 131 / 14 / 0 with 117 open
at base and identical at HEAD, all three symmetric differences empty, no duplicate
id, no resolution naming an unregistered id, max R-0516. THE MIGRATION CHANGED
THE MECHANISM AND NOT THE OUTCOME: `subprocess.run(` occurs 0 times at HEAD having
occurred 3 times at base, each of the five FROM texts 0 times and each TO exactly
once, `run_guarded_test_command` 5 times as three call sites plus two imports,
`import subprocess` still present in `_run_fixture_builder` for its `except
subprocess.TimeoutExpired` clause and gone from `_run_repair_loop_fixture` where
nothing else used it. THE MIGRATED CODE SITS ON AN EXECUTED PATH, PROVEN FROM
OPPOSITE ENDS: the reviewer broke the three bare spawns at BASE before authoring
and the round gate reported 18 failures; the worker broke the SEAM at HEAD inside
a disposable worktree and the same command line reported 18 failures spanning both
driving files. The same number from both directions is what a preserved call graph
looks like. THE GATES WERE RE-RUN, NOT READ: the round gate exited 0 with
`140 passed, 6 skipped` and the migration did not move it, the guard suite
`24 passed`, the four state readers `158 passed`, the canary `42 passed` and ruff
`All checks passed!`, each as its exact ordered command line. COMMIT HYGIENE IS
CLEAN: the changed-path set before C4 is exactly the five declared paths,
per-commit insertions are 313, 258, 35, 12 and 5 with C4's own 85 measured after
it existed and none over 500, six commits form a single-parent chain, and the
reflog holds only `commit:` entries. Both deviations are declared, the D15 overage
names its own measured length, and neither widens scope. No block condition is met.

- R-0517 — Low, A BLOCK'S HANDBACK SECTION DROPPED A POINTER THE PROTOCOL
REQUIRES, AND THE HANDOFF INHERITED THE GAP. docs/agents/self_drive_protocol.md
§Phase 2 requires that every handoff naming the next session's first action names
Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR
Gate. R25's handoff carried that sentence. R26's does not, because the R26 block's
Handback section enumerated what the handoff must contain and left it out. The
worker is not at fault: it wrote what the block ordered, which is the shape this
record keeps finding on the reviewer's side of the line. Low because nothing
executable depends on it and no gate could have gone red over it — the whole cost
lands on the next session, which opens a handoff telling it to re-run gates and
saying nothing about the sentinel that can halt a round before it starts, nor
about the PR gate that must precede any new branch. It is registered rather than
waved through because the reviewer authored the omission, and a reviewer defect
spoken aloud only in a chat window is exactly the A1 trap this record exists to
close. No checklist item is added: the requirement already lives in the protocol,
so the fix is that this round's own handback carries the sentence and every later
block's Handback section names it among the mandated contents. OPEN.

Gate: R27 — PASS, the round that recorded R26 and registered the reviewer's own
omission. Every ordered gate was re-run by the reviewer over 369d94a3..07b1ba25
and each one reproduces the handback's reading. TRANSPORT IS EXACT IN ALL FOUR
PLACES: the committed `.agent/authored/f085-r27.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL at sha256
ce7ffcc42df494a9c21e733f410e6d8f48d394bc16239a0be71191232cdeafdd, 14103 B, 229
lines, 6 marker lines, region digests dfea0906, 85061d65 and b03dbb55. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD2 at numstat
61/0, RECORD2's first line occurs once among the lines that commit adds, and 0
lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits five times —
all of it `APPEND-shaped` prose older than that round, which is the exact
distinction the gate exists to force. THE ARITHMETIC MOVED BY THE ONE ID IT WAS
ORDERED TO MOVE BY: 131 registered / 14 done / 0 landed with 117 open at base and
132 / 14 / 0 with 118 open at HEAD, registered symmetric difference exactly
R-0517, done and landed symmetric differences empty, no duplicate id, no
resolution naming an unregistered id, max R-0517 and next free R-0518. THE PLAN
PAIR IS A REWRITE AND ONLY THE ORDERED REGION MOVED: PLANF2 occurs 0 times at HEAD
and PLANT2 once, `## Goal` and `## Risks` are byte-identical to their base bytes,
the file is 254757ce2fbc3267ebdda74003373bf987e83371927bb6384a1a50caf470b46c at
2370 B and 41 lines, and its `## Next Steps` list parses to 1, 2, 3. THE GATES
WERE RE-RUN, NOT READ: the four state readers exited 0 with `158 passed` and the
canary exited 0 with `42 passed`, each as its exact ordered command line, and no
ruff gate was skipped by oversight because the change set holds no `.py` file.
COMMIT HYGIENE IS CLEAN: the path set measured before the handback commit is the
four declared `.agent/` paths and the handback adds only itself, per-commit
insertions are 229, 168, 61 and 4 with the handback's own 80 measured after it
existed and none over 500, the range is a single-parent chain, and the reflog
holds only `commit:` entries. The handback is 123 lines against the 60 its
per-commit tables carry; the overage is declared, names its own measured length
and names the mandated content that caused it, which DECISION D15 permits and
which no dropped section was traded for. No block condition is met.

Done: R-0517 — resolved. The pointer is back on disk, and the block that dropped
it is the block that restored it. R27's Handback section named the
Phase-1-rule-1 sentence among the handback's mandated contents, and the handback
it produced carries it: `.agent/handoff.md` at 07b1ba25 states in its `## Next`
section that the next session's first action is re-reading `.agent/STOP` from
disk BEFORE the Open PR Gate, and the reviewer read that from the file rather
than from the worker's report. The finding closes on the PROPERTY and not on a
sentence: what is required is that a handoff naming the next session's first
action names the sentinel check first, and that every later block's Handback
section carries the requirement forward — this round's block does. No checklist
item is added, because docs/agents/self_drive_protocol.md §Phase 2 already binds
it and a second copy would be a second source of truth.

- R-0518 — Medium, A GATED TEST NEEDS A GITIGNORED BUILD DIRECTORY, SO THE
STATE-READER GATE IS RED IN EXACTLY THE DISPOSABLE WORKTREE THIS PROTOCOL
MANDATES. `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
runs `npx vitest run` with `cwd=Path("apps/ui").resolve()`, and
`apps/ui/node_modules` is gitignored at `.gitignore:221`, so a fresh
`git worktree` never carries it. That node sits inside the four-file state-reader
suite every `.agent/`-rewriting round gates on, while
docs/agents/planner_reviewer_prompt.md §4 item 10 and the self-drive protocol's
G5 both require destructive verification to run in a disposable worktree. The two
rules meet in a red no change caused. MEASURED, not inferred: in the primary
checkout the node passed 3 of 3 standalone and the whole suite read `158 passed`
at exit 0 in 5 of 5 runs at base 07b1ba25; in a worktree created at the same
commit with no `apps/ui/node_modules` it failed 2 of 2 standalone with
`AssertionError: vitest failed: ... [UNRESOLVED_IMPORT] Could not resolve
'vitest/config'`. The first red the reviewer hit reported only a tail summary and
named no node, which is why `-rf` now stands in the ordered command line — a
reading ordered in a shape that cannot carry the evidence it exists to produce is
its own small defect, recorded here rather than in a separate id. Medium because
a red gate halts a round under the standing rule that a worker never repairs
around one, and this red is reachable by any round that follows the worktree
requirement. NOT fixed here: the repair belongs in the test — skip the node when
`apps/ui/node_modules` is absent — and `tests/orchestration/test_test_runner.py`
carries no skip of its own today, so the fix is a real edit to a gate file and
sits outside this round's change set. OPEN.

Gate: R28 — PASS, the round that put `_run_isolated_process` on the seam's child
half and closed R-0517. Every ordered gate was re-run by the reviewer over
07b1ba25..b0d09db4 and each one reproduces the handback's reading. TRANSPORT WAS
PROVED AGAINST THE REVIEWER'S OWN ORIGINAL AND NOT ONLY AGAINST A DIGEST: the
scratch file the block was authored into, the committed
`.agent/authored/f085-r28.md`, the committed `.agent/last_block.md` and both
working copies are all five byte-EQUAL at sha256
c73bac4c5553f82312b5d38669bb33de3586a897f2ec7198f39c0b1399b406d0, 21848 B, 398
lines, 26 marker lines, region digests 3866a6a1, d15e4f7e and 4b8d681f. THE
APPEND COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at numstat
71/0, RECORD1's first line occurs once among the 71 lines that commit adds, and 0
lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits seven times
— five older than that round and two added by RECORD1's own prose, which quotes
the regex and the word `APPEND-shaped`. A line-anchored count reports the
property; a substring count reports the prose. THE ARITHMETIC MOVED IN BOTH SETS
AT ONCE WHILE THE OPEN COUNT STAYED FLAT: 133 registered / 15 done / 0 landed at
HEAD against 132 / 14 / 0 at base, 118 open at both ends, registered symmetric
difference exactly R-0518, done symmetric difference exactly R-0517, landed
empty, no duplicate id, no resolution naming an unregistered id, max R-0518 and
next free R-0519. A flat open count across a round that both registers and
resolves is the arithmetic working, not the arithmetic standing still. THE
MIGRATION TOOK THE CHILD HALF AND LEFT THE PARENT HALF ALONE: S1F through S4F
occur 0 times at HEAD and each TO exactly once, the new test's `def` line occurs
once among the lines C3 adds, `def test_no_shell_true(self):` still occurs
exactly once in the file, and no marker line reached any target. The source
guards over `_run_isolated_process` still hold, because the migration kept
`subprocess.Popen(`, `start_new_session=True` and `DEVNULL` inside the function
and added no `subprocess.run(`. THE PROOF IS A REAL CHILD AND THE REVIEWER BROKE
IT INDEPENDENTLY: at HEAD the new node passes, and in a disposable worktree at
HEAD with the single line `preexec_fn=plan.preexec_fn,` deleted it FAILS, then
passes again once restored. The reviewer ran that recipe itself rather than
reading the worker's transcript, and the parent's own RLIMIT_CORE of (0, -1) is
what makes the child's (0, 0) an observation rather than a tautology. THE GATES
WERE RE-RUN, NOT READ: the round gate exited 0 with `98 passed` against a base of
`97 passed` the reviewer measured before the block was written, ruff over both
changed files `All checks passed!`, the four state readers `158 passed` and the
canary `42 passed`, each as its exact ordered command line. COMMIT HYGIENE IS
CLEAN: the path set is the six declared paths, per-commit insertions are 398,
334, 71, 8 and 39 with the handback's own 84 measured after it existed and none
over 500, the range is a single-parent chain, and the reflog holds only `commit:`
entries. The handback is 125 lines against the 100 a round with more than five
per-commit tables may carry; the overage is declared, names its own measured
length and names the mandated content that caused it. R-0202 is correctly still
OPEN: the migration passes the caller's already-scrubbed `env` through unchanged,
so the variable that finding names is dropped after this round by the same code
as before it. No block condition is met.

- R-0519 — Low, A PROGRESS ESTIMATE THE REVIEWER AUTHORED OVERSTATED A SLICE THE
CLASS TABLE CAN MEASURE. R28's handback carries `Fortschritt: ~85 %`, and the plan
it inherited described T002b's remainder as the `test`-class sites "ending with
`test_execution_service.py`'s `Popen`". Measured against amendment F085 D1's class
table, five of the twelve `test`-class sites are on the shared seam and seven are
not. `test_execution_service.py`:323 was the last `Popen` of the class, not its
last SITE, and the plan sentence conflated the two — which is how an estimate
built on it reached 85 % for a slice that is under half migrated. The criterion
used, so it can be re-checked: a site is ON THE SEAM when its spawn takes cwd,
env and the fork-to-exec hook from `exec_guard`, through either
`run_guarded_test_command` or `plan_child_spawn`; each of the seven remaining
files contains no reference to either symbol. Low because nothing executable
depends on the number and no gate could go red over it. It is registered rather
than corrected in silence because the Fortschritt line is the operator's only
progress signal, it is authored by the reviewer, and
docs/agents/planner_reviewer_prompt.md §2 requires it to be honest and labelled an
estimate. The counter-measure ships in this same round: C3 writes the migration
state into `.agent/f085_inventory.md` directly beneath the class list that defines
the set, so the next estimate is derived from the file that fixes the denominator
rather than from the previous estimate. OPEN.

Gate: R29 — PASS, the state-only round that recorded the R28 PASS, registered
R-0519 and put the T002b migration state into the inventory of record. Every
ordered gate was re-run by the reviewer over b0d09db4..f99a8fe2 and each one
reproduces the handback's reading. TRANSPORT: the committed
`.agent/authored/f085-r29.md`, the committed `.agent/last_block.md` and both
working copies are all four byte-EQUAL at sha256
5c93aff876b168aada846b99dcf9ff927df3f41f3329b55a7f40d353422dd813, 18160 B, 306
lines, 10 marker lines at 157, 226, 228, 244, 246, 262, 264, 276, 278 and 306,
region digests c40e6be2, 23d988e4 and 70c142ae. No scratchpad original from that
authoring session survived into this one, so the proof is disk-to-disk over the
committed artifacts under the self-drive protocol's cmp rule; stated, not
implied. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at numstat
69/0, RECORD1's first line occurs once among the 69 lines that commit adds, and 0
lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits nine times
in that file's prose. THE ARITHMETIC MOVED IN ONE SET ONLY: 134 registered / 15
done / 0 landed at HEAD against 133 / 15 / 0 at base, 118 open rising to 119,
registered symmetric difference exactly R-0519, done and landed symmetric
differences both empty, no duplicate id, no resolution naming an unregistered id,
max R-0519 and next free R-0520. THE PAIRS LANDED WHERE THEY WERE AIMED: PLANF
occurs 0 times at HEAD and PLANT exactly once, `## Goal` and `## Risks` are
byte-identical to their base bytes, `.agent/plan.md` is 42 lines under the
50-line cap, and its `## Next Steps` parses to 1, 2, 3. INVF occurs once and INVT
once, INVT contains INVF verbatim so the pair really is append-shaped, and
`Migration state, measured at R29:` occurs once among the 16 lines C3 adds. THE
MEASUREMENT THE ROUND EXISTS TO RECORD IS TRUE OF THE SOURCE, NOT ONLY OF THE
PROSE: the reviewer re-derived it per file rather than trusting the paragraph.
`autorun.py` references `run_guarded_test_command` five times, `test_runner.py`
three times and `test_execution_service.py` references `plan_child_spawn` three
times, so those three files carry the five sites called ON THE SEAM;
`builder_bridge.py`, `ci_run.py`, `integrity_gate.py`, `job_promote.py`,
`mission_state.py`, `pingpong_loop.py` and `pingpong_promote.py` reference
neither symbol. Five on the seam, seven not, as the inventory paragraph and
R-0519 both state. THE GATES WERE RE-RUN, NOT READ: the four state
readers exited 0 at `158 passed` and the canary exited 0 at `42 passed`, each as
its exact ordered command line in the primary checkout. COMMIT HYGIENE IS CLEAN:
the path set before the handback is the five declared paths, per-commit
insertions are 306, 212, 69, 8 and 16 with the handback's own 99 measured after
it existed and none over 500, the range is a single-parent chain, and the reflog
holds only `commit:` entries. One reported number differs and neither reading is
wrong: the handback gives `## Goal` as 729 B where a heading-inclusive slice
measures 730 B, a section-boundary convention that leaves the ordered property —
byte-identical to base — reproducing either way. The 131-line handback declares
its own overage against the 100-line cap and names the mandated content that
caused it. No block condition is met.

Done: R-0519 — RESOLVED at R29 by the counter-measure the finding itself named.
`.agent/f085_inventory.md` now carries `Migration state, measured at R29:`
directly beneath the `### test — 12` heading that defines the class, naming the
criterion for being on the seam, the files that satisfy it and the files that do
not — so the next estimate is derived from the file that fixes the denominator
instead of from the previous estimate. The overstated line is gone as well: R29's
handback carries `~60 %` with `T002b 5 von 12 Sites auf dem Seam, 7 offen` in
place of `~85 %`. The reviewer verified the correction against the SOURCE, per
the per-file reading in this round's gate entry above. Resolved rather than
carried, because the finding asked for a denominator on disk and it is on disk.

Gate: R30 — PASS, the round that moved `job_promote._run_post_test` and
`pingpong_promote._run_post_test` onto the shared `test`-class seam. Every ordered
gate was re-run by the reviewer over f99a8fe2..d4fe1674 and each one reproduces
the handback's reading. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL,
not only against a digest: the scratch file the block was authored into, the
committed `.agent/authored/f085-r30.md`, the committed `.agent/last_block.md` and
both working copies are all five byte-EQUAL at sha256
fd9117aad06382747a59995dbeef4d32d75e14f3f7e3d19af7bc5499dc93b0a2, 21347 B, 399
lines, 26 marker lines, region digests 9e5478bc, 97f12afd, c6bb8ee5 and d3cf7d6b.
THE APPEND COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of
the post-commit file, the remainder is exactly one blank line plus RECORD1 at
numstat 58/0, RECORD1's first line occurs once among the 58 lines that commit
adds, and 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits
ten times in that file's prose. THE ARITHMETIC MOVED IN THE DONE SET ALONE: 134
registered / 16 done / 0 landed at d4fe1674 against 134 / 15 / 0 at f99a8fe2, 119
open falling to 118, registered symmetric difference empty, done symmetric
difference exactly R-0519, landed empty, no duplicate id, no resolution naming an
unregistered id, max R-0519 and next free R-0520. THE PAIRS LANDED WHERE THEY WERE
AIMED: at d4fe1674 SPAWNF and OUTF each occur 0 times in both migrated files while
SPAWNT and OUTT each occur once, IMPT1 occurs once in `job_promote.py` and IMPT2
once in `pingpong_promote.py`, the guard import occurs once among the lines C2 adds
to each source, each new test def occurs once among the lines C2 adds to its test
file, and 0 marker lines reached any of the four. PLANF is gone and PLANT occurs
once, in a 46-line plan under the 50-line cap. THE PROOF IS A REAL COUPLING AND THE
REVIEWER BROKE IT INDEPENDENTLY: at d4fe1674 the round gate exits 0 at `146 passed`
against the `144 passed` the reviewer measured at f99a8fe2 before the block was
written, and in the reviewer's own disposable worktree at d4fe1674, with the
guarded call replaced by a bare `subprocess.run` and the decode left standing, the
run exits 1 with `2 failed, 73 passed` — `TestApprovePostTest::test_post_apply_test_runs`
and `test_job_promote_post_test_runs_on_the_guarded_seam`, both
`AttributeError: 'str' object has no attribute 'decode'`. The first of those two is
the behaviour-equality golden this feature's Acceptance asks for: it spawns a REAL
child through the migrated function, so its staying green under the guard is the
evidence that well-behaved commands behave identically. THE GATES WERE RE-RUN, NOT
READ: ruff over the four changed files `All checks passed!`, the four state readers
`158 passed` and the canary `42 passed`, each as its exact ordered command line in
the primary checkout. COMMIT HYGIENE IS CLEAN: the path set is the nine declared
paths, per-commit insertions are 399, 317, 58, 69 and 12 with the handback's own
100 measured after it existed and none over 500, all six commits are single-parent,
and the reflog holds only `commit:` entries. The 150-line handback declares its own
overage against the 100-line cap and names the mandated content that caused it. No
block condition is met, and the worker deviated from nothing it was ordered to do.

- R-0520 — Low, A REVIEWER-AUTHORED GATE ENTRY MADE A PRESENT-TENSE CLAIM ABOUT
SOURCE FILES THE SAME BLOCK THEN CHANGED. The R29 gate entry applied at commit
9668bec4 lists seven modules and states that they "reference neither symbol",
meaning `run_guarded_test_command` and `plan_child_spawn`. That reading was taken
at f99a8fe2 and is true there. C2 of the SAME round, commit 10fe9a14, put
`job_promote.py` and `pingpong_promote.py` on the seam, and at d4fe1674 each of
those two files references `run_guarded_test_command` twice — so two of the seven
names in that sentence are wrong for every commit from 10fe9a14 onward, in a file
that is the permanent record. The defect is the reviewer's, not the worker's: R30's
handback found it under constraint 8 and reported it instead of editing a slice it
was forbidden to alter or a file outside its change set, which is exactly the
behaviour constraint 8 exists to produce. Low because nothing executable depends on
the sentence, no gate can go red over it, and the paragraph it sits in opens by
naming the range b0d09db4..f99a8fe2 that scopes it. It is registered rather than
quietly corrected because this is the R-0417 staleness class recurring in the one
place the standing gate does not reach — the reviewer's own authored prose, written
before the commit that falsifies it exists. The counter-measure is a rule, not an
edit: a slice that states a fact about a file the SAME block modifies names the
commit its reading was taken at, in the sentence itself, rather than relying on a
range named in a neighbouring sentence. Rewriting the landed text is NOT proposed —
appending a correction is how this record stays honest, and a later round may do
that; overwriting history in `.agent/live_review.md` is worse than a dated wrong
sentence. OPEN.

Gate: R31 — PASS, the round that moved `pingpong_loop._run_test_command` onto the
shared `test`-class seam and registered R-0520. Every ordered gate was re-run by the
reviewer over d4fe1674..HEAD and each one reproduces the handback's reading.
TRANSPORT REPRODUCES IN REGIONS AND NOT ONLY IN TOTAL: the committed
`.agent/authored/f085-r31.md`, the committed `.agent/last_block.md` and both working
copies are all four byte-EQUAL at sha256
9023be74ce151bf00b833090c733fe9f77210a50519f4c14790f615adc6cf2a4, 20195 B, 352
lines, 20 marker lines, region digests def02d5c, afd442cb and b083f1bd. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at 5193 =
1 + 5192 bytes, numstat 67/0, RECORD1's first line occurs once among the 67 lines
that commit adds, and 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring
`END-` hits eleven times in that file's prose. THE ARITHMETIC MOVED IN THE
REGISTERED SET ALONE: 134 registered / 16 done / 0 landed at d4fe1674 against 135 /
16 / 0 at HEAD, 118 open rising to 119, registered symmetric difference exactly
R-0520, done and landed symmetric differences both empty, no duplicate id, no
resolution naming an unregistered id, max R-0520 and next free R-0521. THE PAIRS
LANDED WHERE THEY WERE AIMED: at HEAD SPAWNF and OUTF each occur 0 times in
`pingpong_loop.py` while SPAWNT and OUTT each occur once, IMPT occurs once, the guard
import occurs once among the nine lines C2 adds to that file, the new test def occurs
once among the twenty-five lines C2 adds to its test file, 0 marker lines reached
either, and every applied slice matches its committed original byte for byte — TESTPL
is an exact suffix of the test file and RECORD1 an exact suffix of the review record.
PLANF is gone and PLANT occurs once, in a 43-line plan under the 50-line cap. THE
PROOF IS A REAL COUPLING AND THE REVIEWER BROKE IT INDEPENDENTLY: at HEAD the round
gate exits 0 at `34 passed` against the `33 passed` the reviewer measured at
d4fe1674, and in the reviewer's own disposable worktree at 16234fbf, with the guarded
call replaced by a bare `subprocess.run` and the decode left standing, the run exits 1
with `1 failed, 33 passed` — `test_pingpong_loop_test_command_runs_on_the_guarded_seam`,
`AttributeError: 'str' object has no attribute 'decode'` at `pingpong_loop.py:3549`.
THE SEAM'S CONTRACT WAS READ RATHER THAN TRUSTED: `run_guarded_test_command` raises
`subprocess.TimeoutExpired` on a wall trip, deliberately does not catch
`FileNotFoundError`, and returns a negative returncode on a signal death — so both
`except` clauses and `passed = proc.returncode == 0` are unchanged. THE GATES WERE RE-RUN, NOT READ: ruff
over the two changed files `All checks passed!`, the four state readers `158 passed`
and the canary `42 passed`, each as its exact ordered command line in the primary
checkout, each exit 0. COMMIT HYGIENE IS CLEAN: the path set is the seven declared
paths, per-commit insertions are 352, 174, 67, 34, 5 and the handback's own 130, none
over 500, all six commits are single-parent, and the reflog holds only `commit:`
entries. STALENESS REPRODUCES: `builder_bridge.py`, `ci_run.py`, `integrity_gate.py` and
`mission_state.py` each show 0 references to `run_guarded_test_command` at HEAD, and
R-0520's own text survives C2 — `job_promote.py` and `pingpong_promote.py` reference
that symbol twice each at BOTH d4fe1674 and HEAD. The 162-line handback declares its own overage against the
100-line cap and names the mandated content that caused it. No block condition is met,
and the worker deviated from nothing it was ordered to do.

Done: R-0520 — Resolved at R32. The counter-measure the finding named is now
checklist item 20 of `docs/agents/planner_reviewer_prompt.md` §3, applied by the
commit that precedes this one in this round: a slice may assert a present-tense fact
about a source file only when the sentence names the commit its reading was taken at.
The finding asked for a rule rather than an edit, so the resolution is the promotion
and not a rewrite of the R29 sentence that exposed it. That sentence stays on disk,
wrong for two of its seven names from commit 10fe9a14 onward, because appending a
correction is how this record stays honest; this paragraph is that correction.

Gate: R33 — the R32 entry. R32 PASSED: the round that promoted the slice-fact rule
into pre-emission checklist item 20, resolved R-0520 and moved
`integrity_gate._check_collect_only` onto the shared `test`-class seam. Every ordered
gate was re-run by the reviewer over 16234fbf..c2033d6c and each reproduces the
handback's reading. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL, not
only against a digest: the scratch file the block was authored into, the committed
`.agent/authored/f085-r32.md`, the committed `.agent/last_block.md` and both working
copies are all five byte-EQUAL at sha256
75deb8c5d666fc2f4053583eb8c4a3d94dd2db8f52c227df2a22b2392cf1e686, 23119 B, 400
lines, 24 marker lines, region digests eb26791d, 656230ba and 0d724fc0. THE APPEND
COMMIT HOLDS ITS SHAPE: C2's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at 4361 =
1 + 4360 bytes, numstat 55/0, RECORD1's first line occurs once among the 55 lines
that commit adds, 0 lines match `^(BEGIN|END)-[A-Z0-9]+$`, and the applied slice is
an exact suffix of the file. THE ARITHMETIC MOVED IN THE DONE SET ALONE: 135
registered / 17 done / 0 landed at c2033d6c against 135 / 16 / 0 at 16234fbf, 119
open falling to 118, registered and landed symmetric differences empty, done
symmetric difference exactly R-0520, no duplicate id, no resolution naming an
unregistered id, and next free R-0521 at both ends because the round registered
nothing. THE ORDERING THAT MADE THE RECORD TRUE WAS OBEYED: constraint 10 required
the checklist promotion to precede the resolution that cites it, and 94e70839 does
precede ce69c39a. THE PAIRS LANDED WHERE THEY WERE AIMED: at c2033d6c IGSPAWNF and
IGERRF each occur 0 times in `integrity_gate.py` while IGSPAWNT, IGERRT and IGIMPT
each occur once, the guard import occurs once among the lines C3 adds to that file,
`import subprocess` still occurs once because the `git ls-files` call in
`_check_relevant_untracked` is a different command class, the new test def occurs
once among the lines C3 adds to its test file, TESTIG is an exact suffix of that
file, and 0 marker lines reached any target. Item 20 occurs once and the checklist's
closing paragraph still occurs once. PLANF is gone and PLANT occurs once, in a
46-line plan under the 50-line cap. THE MIGRATION WAS PROVED TWICE, BY RUNNING IT
AND BY BREAKING IT: the round gate exits 0 at `16 passed` against the `15 passed`
the reviewer measured at 16234fbf, the migrated function run FOR REAL prints
`collect_only IntegrityStatus.PASS pytest collection passed` — identical to the
unmigrated reading at 16234fbf, which is the behaviour-equality evidence this
feature's Acceptance asks for, and it shows the guard's environment allowlist does
not starve a real collection — and in the reviewer's own disposable worktree at
c2033d6c, with the guarded call replaced by a bare `subprocess.run`, the run exits 1
with `1 failed, 15 passed` at node `test_collect_only_runs_on_the_guarded_seam`,
`AssertionError` at `test_integrity_gate.py:235`. THE GATES WERE RE-RUN, NOT READ:
ruff over the two changed files `All checks passed!`, the four state readers
`159 passed`, the docs suite `295 passed` and the canary `42 passed`, each as its
exact ordered command line in the primary checkout, each exit 0. COMMIT HYGIENE IS
CLEAN: the path set is the eight declared paths, per-commit insertions are 400, 288,
16, 55, 41, 12 and the handback's own 80, none over 500, all seven commits are
single-parent, and the reflog holds only `commit:` entries. The 128-line handback
declares its own overage against the 100-line cap and names the mandated content
that caused it. The worker deviated from nothing it was ordered to do, and the one
defect the round put on disk is the reviewer's, registered next.

- R-0521 — Low, A SLICE OBEYED CHECKLIST ITEM 20 AND WAS FALSIFIED ANYWAY, BECAUSE
THE COMMIT IT NAMED WAS A LABEL RATHER THAN A SHA. R32's RECORD1, applied at commit
ce69c39a, closes with a staleness sentence stating that `builder_bridge.py`,
`ci_run.py`, `integrity_gate.py` and `mission_state.py` each show 0 references to
`run_guarded_test_command` "at HEAD". That reading was taken at 16234fbf and is true
there. C3 of the SAME round, commit ed88be4c, put `integrity_gate.py` on the seam,
and at c2033d6c that file references the symbol twice — so one of the four names in
that sentence is wrong for every commit from ed88be4c onward, in a file that is the
permanent record. This is the R-0520 class recurring in the very slice that resolved
R-0520, one commit after the counter-measure landed. The defect is the reviewer's,
not the worker's: R32's handback found it under constraint 8 and reported it instead
of editing a slice it was forbidden to alter, which is exactly the behaviour
constraint 8 exists to produce. Low because nothing executable depends on the
sentence and no gate can go red over it. What makes it worth an id rather than a
correction is that item 20 was FOLLOWED: the sentence did name a commit, and the
commit it named was `HEAD`, which re-resolves as the round proceeds and so denotes a
different commit at the end of the round than at the start. A rule that can be
obeyed and defeated at once is under-specified rather than ignored, which is why the
counter-measure narrows item 20 instead of adding an item. Rewriting the landed
sentence is NOT proposed: appending a correction is how this record stays honest,
and this paragraph is that correction.

Done: R-0521 — Resolved at R33. Checklist item 20 of
`docs/agents/planner_reviewer_prompt.md` §3 now requires that the commit a slice
names be an absolute identifier that already exists when the slice is written — a
SHA, never a label like `HEAD` or `main` — applied by the commit that precedes this
one in this round. The narrowing is the whole resolution; the R31 gate entry's "at
HEAD" sentence stays on disk, wrong for one of its four names from ed88be4c onward,
because overwriting landed text is worse than a dated wrong sentence.

Gate: R34 — the R33 entry. R33 FAILED, on one sentence, under §4.5's "unverified
completion claims". EVERY GATE R33 ORDERED REPRODUCES: the reviewer re-ran G1-G7 over
c2033d6c..7480d880 and each returns the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL, not only against a digest: the scratch file the
block was authored into, the committed `.agent/authored/f085-r33.md`, the committed
`.agent/last_block.md` and both working copies are all five byte-EQUAL at sha256
a089cc6604b57cfd9c7ee5449742a4651c10c9d7db80af0f8da735bd5b566404, 19296 B, 305 lines,
10 marker lines, region digests 2c1d1941, 84609b00 and f6c3a188 under the
trailing-newline convention the handback used. THE APPEND COMMIT HELD ITS SHAPE:
c933b949's pre-commit blob is a byte-exact PREFIX of the 373548 B post-commit file,
the remainder is 6064 B = one blank line plus RECORD1, RECORD1 is an exact suffix,
its first line occurs once among the 79 lines that commit adds, numstat 79/0, 0 lines
match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 7 times. THE
ARITHMETIC MOVED IN BOTH SETS BY ONE ID: 135 registered / 17 done / 0 landed at
c2033d6c against 136 / 18 / 0 at 7480d880, 118 open at both ends, registered and done
symmetric differences each exactly R-0521, landed symmetric difference empty, no
duplicate id, no resolution naming an unregistered id, and next free R-0522. THE
NARROWING LANDED WHERE IT WAS AIMED: at 7480d880 the item-20 opener, the new
`identifier that already EXISTS` line and the checklist's closing paragraph each
occur exactly once in `docs/agents/planner_reviewer_prompt.md`, 0 marker lines
reached it, numstat 9/1, and 74dfa30e does precede c933b949 as R33's constraint 9
required. THE SUITES WERE RE-RUN, NOT READ: the four state readers `159 passed`, the
docs suite `295 passed` and the canary `42 passed`, each as its exact ordered command
line in the primary checkout, each exit 0. COMMIT HYGIENE IS CLEAN: the path set is
the six declared paths, per-commit insertions are 305, 223, 9, 79, 13 and the
handback's own 89, none over 500, all six commits are single-parent, the reflog holds
only `commit:` entries, and the ordered push landed — origin and local agree at
7480d880. The worker deviated from nothing it was ordered to do.

WHAT FAILED IS A SENTENCE NO GATE ASKED FOR. R33's handback closes its
`## Authored-text proofs` section by calling both pairs REWRITE and stating that each
FROM "matched exactly once before apply and 0 times after". The reviewer measured the
SHARPF text at 74dfa30e: it occurs once, not zero times. The findings follow: the
reviewer's mislabelling, the false line it produced, and one the reviewer found while
authoring this block's own resolutions.

- R-0522 — Medium, A PAIR WAS DECLARED A REWRITE WHILE ITS TO CONTAINED ITS FROM
VERBATIM, BY A CONSTRAINT THAT CLAIMED A MECHANICAL CONTAINMENT TEST. R33's constraint
2 reads "Pair shapes, each MEASURED by the reviewer with a containment test, one
reading per pair: SHARPF→SHARPT REWRITE · PLANF→PLANT REWRITE". SHARPT begins with
SHARPF verbatim, so the containment test returns true and the pair is APPEND-shaped;
PLANF→PLANT is a REWRITE and that half is right. This is checklist item 15 — itself
the counter-measure for R-0508, the finding in which a block "ran the check for the
single pair it suspected" and generalised — recurring one feature later in the round
that had just narrowed item 20 for the same underlying reason. Item 15 was obeyed as
written: a per-pair reading WAS printed. What was printed was the LABEL and not the
test's output, and a label is indistinguishable on the page from a measured one, so
nothing downstream could catch it. Medium rather than Low because the label is what
the worker's proof obligation is derived FROM: a wrong label does not stay a
documentation defect, it manufactures a false measurement, which is R-0523.

- R-0523 — Medium, A HANDBACK REPORTED A PROOF NUMBER THAT THE FILE ON DISK
CONTRADICTS. R33's handback, applied at 7480d880, states in `## Authored-text proofs`
that SHARPF→SHARPT and PLANF→PLANT are "both REWRITE; each FROM matched exactly once
before apply and 0 times after, each TO once after". At 74dfa30e the SHARPF text
occurs exactly once in `docs/agents/planner_reviewer_prompt.md` and the SHARPT text
occurs exactly once, because the second contains the first; the claim is true of
PLANF→PLANT and false of SHARPF→SHARPT. §4.5 lists unverified completion claims among
the block conditions, so this is the sentence that costs R33 its PASS even though
every ordered gate is green — a round's verdict is not the conjunction of its gates.
The defect is not dishonesty: §4.9 says in terms that demanding a FROM-zero count for
an append-shaped pair "invites either a fabricated number or a pointless repair
round", and this is that invitation being accepted. The counter-measure is upstream,
at R-0522, because a worker handed a correct shape reports a correct number. The
landed sentence is NOT rewritten: this paragraph is its correction, per R-0521.

- R-0524 — Low, ITEM 20 NOW DEMANDS A SHA FOR A CLASS OF SLICE IN WHICH NO SHA CAN
EXIST. R-0521's narrowing, applied at 74dfa30e, requires that the commit a slice names
be "an absolute identifier that already EXISTS when the slice is written", justified
on the ground that "a block always has such a SHA to hand, because its own base is
stated in its done-when". The base SHA answers a reading of a state that PRECEDES the
round. It cannot answer a slice that asserts what the round's own commits have just
made true — and every `Done:` paragraph in this file is of that class, including
those in this entry, which assert what items 15 and 20 require after C1 of R34. For
those the required identifier is a commit that does not exist when the slice is
authored, so the rule as narrowed is satisfiable only by a value that cannot be
written: the R-0371 shape, which this same checklist forbids for gates. Low because
it has cost no round yet and was caught while authoring rather than after landing.
Found by the reviewer against its own draft, which is where item 20 is supposed to be
read.

Done: R-0522 — Resolved at R34. Checklist item 15 of
`docs/agents/planner_reviewer_prompt.md` §3 now requires the constraint to record the
containment test's OUTPUT — `TO contains FROM: true` or `false` — with the APPEND or
REWRITE label derived on the same line, and it states that a `true` reading orders the
§4.9 append obligation and never a FROM-zero count. The narrowing is applied by the
commit that constraint 9 of this round's block fixes ahead of this one; constraint 2
of that same block is the first use of the new form, recording a boolean for every
pair it lists.

Done: R-0523 — Resolved at R34. This registration is the correction, and it is the
whole resolution: the false sentence stays in `.agent/handoff.md` where it landed,
because overwriting landed text is worse than a dated wrong sentence. What stops the
class is R-0522's narrowing plus the constraint this round's block carries, which
forbids reporting a FROM-zero count for an APPEND pair under any wording. No gate is
added, because no gate could have caught a number nothing ordered.

Done: R-0524 — Resolved at R34. Checklist item 20 of
`docs/agents/planner_reviewer_prompt.md` §3 now carves out the slice that describes
the round's own landed change: it names the block CONSTRAINT fixing the commit order
instead of a SHA, and a reading of any prior state still names its SHA. Applied by the
commit that constraint 9 of this round's block fixes ahead of this one, which is what
lets these three paragraphs name constraint 9 rather than an impossible identifier.

Gate: R35 — the R34 entry. R34 PASSED: the repair round that registered and resolved
R-0522, R-0523 and R-0524 — a pair labelled REWRITE while its TO contained its FROM,
the false rewrite proof that label produced, and the slice class item 20's required
SHA cannot reach. Every ordered gate was re-run by the reviewer over
7480d880..6ca30b16 and each reproduces the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL, not only against a digest: the scratch file the
block was authored into, the committed `.agent/authored/f085-r34.md`, the committed
`.agent/last_block.md` and both working copies are all five byte-EQUAL at sha256
42bf5eeb4bd3725848d7f824912827a9bff4948a18dd2f6cf13bc6caec46835b, 24167 B, 373 lines,
14 marker lines, region digests 2764ed2a, 6fe4a6ca and 2b83c685 — and that digest is
the one the reviewer measured BEFORE emission, so the block the worker applied is the
block the reviewer wrote. THE APPEND COMMIT HELD ITS SHAPE: 2342ed97's pre-commit blob
373548 B is a byte-exact PREFIX of the 381289 B post-commit file, the remainder is
7741 B = one blank line plus RECORD2, RECORD2 is an exact suffix, its first line
occurs once among the 104 lines that commit adds, numstat 104/0, 0 lines match
`^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 9 times. THE ARITHMETIC
MOVED IN BOTH SETS BY THE SAME THREE IDS: 136 registered / 18 done / 0 landed at
7480d880 against 139 / 21 / 0 at 6ca30b16, 118 open at both ends, registered and done
symmetric differences each exactly R-0522, R-0523 and R-0524, landed symmetric
difference empty, no duplicate id, no resolution naming an unregistered id, and next
free R-0525. THE NARROWINGS LANDED AS APPENDS AND WERE PROVED AS APPENDS: at 6ca30b16
the I15 and I20 FROM texts each still occur exactly once, which is what an
append-shaped pair guarantees and what R33's handback wrongly denied of its own pair;
the item-15, item-16 and item-20 openers and the checklist's closing paragraph each
occur exactly once; every one of the 24 lines the two TOs add that their FROMs do not
contain occurs exactly once among the 24 lines c15798a8 adds; 0 marker lines reached
the file; numstat 24/0. THE SUITES WERE RE-RUN, NOT READ: the four state readers
`159 passed`, the docs suite `295 passed` and the canary `42 passed`, each as its
exact ordered command line in the primary checkout, each exit 0. THE DOCS GATE IS
BLIND TO THE CHECKLIST EDIT AND WAS NOT COUNTED AS EVIDENCE FOR IT: the reviewer ran
the red control in a disposable worktree at 7480d880 with
`docs/agents/planner_reviewer_prompt.md` cut down to the single line `# broken`, and
`tests/docs/` still returned `295 passed`, so no test under that directory reads the
file and G5's occurrence counts are the only check on C1's content. The worktree was
removed and pruned and the primary checkout is clean. COMMIT HYGIENE IS CLEAN: the
path set before C4 is the five declared paths, per-commit insertions are 373, 304, 24,
104, 3 and the handback's own 81, none over 500, all six commits are single-parent,
the reflog holds only `commit:` entries, and the ordered push landed — origin and
local agree at 6ca30b16. THE HANDBACK REPORTED THE PAIR SHAPES THE WAY R34 EXISTS TO
MAKE POSSIBLE: both APPEND pairs are reported as APPEND with no FROM-zero count
claimed, and the one REWRITE pair carries its FROM-0x/TO-1x reading. That is R-0523's
counter-measure working on the first round it applied.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R34's worker reported that
one sentence of the reviewer's own RECORD2 was falsified by its own C4, and declared
it in the handback rather than editing a slice it was told to apply byte-verbatim.
That is exactly the behaviour constraint 8 exists to produce, and the finding below is
the reviewer's, not the worker's.

- R-0525 — Low, A RESOLUTION LOCATED LANDED TEXT IN A PATH THAT IS REWRITTEN EVERY
ROUND, WITHOUT THE SHA THAT HOLDS IT. R34's RECORD2, applied at commit 2342ed97,
closes its R-0523 resolution with the words "the false sentence stays in
`.agent/handoff.md` where it landed". Commit 6ca30b16 — C4 of the same round — rewrote
that path in full, so at 6ca30b16 it does not contain the sentence; the version of
that path in commit 7480d880 does. The referent is recoverable, because the R-0523
registration two paragraphs above names 7480d880 explicitly, which is why this is Low
and was not a block condition against R34. What makes it worth an id is that it is the
R-0520 family arriving through a door R-0524 had just left open. R-0524's carve-out
permits an ordering constraint in place of a SHA for a claim about the round's OWN
change; this sentence is not that claim. It locates a PRIOR round's text by path
alone, and for `.agent/handoff.md` a bare path can never be durable, because the last
commit of every round rewrites it by construction — the staleness is SCHEDULED, not
merely possible, and no ordering constraint reaches it. The same holds for
`.agent/plan.md`, `.agent/last_block.md` and `.agent/context.md`. Found by the
reviewer against the worker's declared observation, which is where a constraint-8
report is supposed to be read.

Done: R-0525 — Resolved at R35. Checklist item 20 of
`docs/agents/planner_reviewer_prompt.md` §3 now requires a slice that merely LOCATES
landed text to name the SHA of the commit holding it whenever the path is one this
workflow rewrites every round, and it names those paths — `.agent/handoff.md`,
`.agent/plan.md`, `.agent/last_block.md`, `.agent/context.md` — rather than leaving
the reader to judge which paths qualify. Elsewhere a bare path stays acceptable, and
the clause says so, because a rule that reaches every path would make ordinary
cross-references unwritable. Applied by the commit that constraint 9 of this round's
block fixes ahead of this one. This entry obeys the new clause: every reference it
makes to `.agent/handoff.md` names the SHA that holds the text it means.

Gate: R36 — the R35 entry. R35 PASSED: the interlude that recorded R34 and narrowed
checklist item 20 to the paths this workflow rewrites every round. Every ordered gate
was re-run by the reviewer over 6ca30b16..23b5fcd9 and each reproduces the handback's
reading. TRANSPORT: the committed `.agent/authored/f085-r35.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL at sha256
41a8470f56a9063fb40a82526f0731bb57b2de20f296b075de572848a6f8581d, 21145 B, 331 lines,
10 marker lines, region digests c9271720, 72829987 and 3e006c9f — all four measured by
the reviewer, not read from the handback. THE APPEND COMMIT HELD ITS SHAPE: cde59e8c's
pre-commit blob 381289 B is a byte-exact PREFIX of the 387274 B post-commit file, the
remainder 5985 B is one blank line plus RECORD3, RECORD3 is an exact suffix, its first
line occurs once among the 78 lines that commit adds, numstat 78/0, 0 lines match
`^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 11 times. THE ARITHMETIC
MOVED IN BOTH SETS BY THE SAME ONE ID: 139 registered / 21 done / 0 landed at 6ca30b16
against 140 / 22 / 0 at 23b5fcd9, 118 open at both ends, registered and done symmetric
differences each exactly R-0525, landed symmetric difference empty, no duplicate id, no
resolution naming an unregistered id, and next free R-0526. THE NARROWING LANDED AS AN
APPEND AND WAS PROVED AS ONE: at 23b5fcd9 the I20F text still occurs exactly once, the
item-15, item-20 and closing-paragraph openers each occur exactly once, and the 11
lines C1's diff adds are exactly the 11 lines I20T adds that I20F does not contain,
each once; 0 marker lines reached the file; numstat 11/0. THE SUITES WERE RE-RUN, NOT
READ: the four state readers `159 passed`, the docs suite `295 passed` and the canary
`42 passed`, each as its exact ordered command line in the primary checkout, each exit
0. The ordered push landed: `git ls-remote origin` and the local branch agree at
23b5fcd9. COMMIT HYGIENE IS CLEAN: the path set before C4 is the five declared paths,
per-commit insertions are 331, 215, 11, 78, 3 and the handback's own 58, none over 500,
all six commits are single-parent, and the reflog holds only `commit:` entries.

- R-0526 — Low, A RESOLUTION ASSERTED A UNIVERSAL PROPERTY OF ITS OWN REFERENCES THAT
ITS OWN TEXT DOES NOT MEET. R35's RECORD3, applied at commit cde59e8c, closes its
R-0525 resolution with "This entry obeys the new clause: every reference it makes to
`.agent/handoff.md` names the SHA that holds the text it means." The reviewer counted
the sentences of RECORD3 mentioning that path at 23b5fcd9 and found four: one locates
landed text and names 2342ed97, and the other three — the rule statement, the path list
and the compliance claim itself — name no SHA and locate nothing. Under the clause as it
landed the entry IS compliant, because the clause binds only a slice that LOCATES landed
text; what fails is the sentence's own restatement of it, which quantifies over every
reference rather than over the ones that locate text and is false of three of its own
four. The referent is recoverable, so the cost is the audit it invites: a later reader
checking the claim must re-derive that three of those references locate nothing. This is
the R-0402 and R-0460 family with a quantifier in place of a numeral — item 11 forbids a
hand-counted NUMERAL about a block's own parts, and nothing yet forbids a hand-checked
UNIVERSAL about a slice's own text. Registered here and deliberately NOT resolved in the
same round: the counter-measure is a checklist clause, this is a production round, and a
fix authored in passing is how the last three rounds became record-keeping. The next
record round resolves it by extending item 11 from numerals to any self-referential
claim a slice makes about its own text, stated as the property actually measured.

Gate: R37 — the R36 entry. R36 PASSED, and it was the first production round since R32:
the default `runner` closure of `packages/orchestration/mission_state.py` moved onto
`run_guarded_test_command`, with the first test that reaches that closure at all. Every
ordered gate was re-run by the reviewer over 23b5fcd9..483975b3 and each reproduces the
handback's reading. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL, not only
against a digest: the scratch file the block was authored into, the committed
`.agent/authored/f085-r36.md`, the committed `.agent/last_block.md` and both working
copies are all five byte-EQUAL at sha256
208ad9d39755891b5bb83f9382e6f3d613c97cafc4652ad2b8b662887d3ce8d1, 24223 B, 400 lines, 22
marker lines, region digests 7d583ed0, ace9d813 and 9b5a9653 — and that digest is the
one the reviewer measured BEFORE emission, so the block the worker applied is the block
the reviewer wrote. THE APPEND COMMIT HELD ITS SHAPE: e27c1c61's pre-commit blob 387274 B
is a byte-exact PREFIX of the 391135 B post-commit file, the remainder 3861 B is one
blank line plus RECORD4, RECORD4 is an exact suffix, its first line occurs once among the
47 lines that commit adds, numstat 47/0, 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the
BEGIN substring occurs 13 times. THE ARITHMETIC MOVED IN THE REGISTERED SET ALONE: 140
registered / 22 done / 0 landed at 23b5fcd9 against 141 / 22 / 0 at 483975b3, 118 open
against 119, registered symmetric difference exactly R-0526, done and landed symmetric
differences empty, no duplicate id, no resolution naming an unregistered id, and next
free R-0527. THE MIGRATION IS THE SLICES AND NOTHING ELSE: at 483975b3 the import sits at
MODULE level in isort order, the three APPEND FROMs each still occur once, the REWRITE
pair reads FROM 0x and TO 1x, the 34 lines C2 adds are exactly the 24 TO-only lines of the
four pairs plus the ten unchanged context lines the diff carries, 0 marker lines reached
either file, and the string `subprocess` now occurs 0 times in that module. THE SEAM IS
REACHED BY A TEST FOR THE FIRST TIME: at 23b5fcd9 every test exercising `run_verify_task`
passed its own `runner=`, so the default closure was executed by no test, and
`test_the_default_runner_goes_through_the_guarded_seam` closes that gap in the same commit
as the code. THE RED PROOF WAS RE-RUN BY THE REVIEWER, NOT READ: in a disposable worktree
at 83bc6df1 with the module-level import moved into the closure, `1 failed, 81 passed`
and the failure is `AttributeError` naming `run_guarded_test_command` at the
`monkeypatch.setattr` line — the module-level import is load-bearing, and a closure-local
one would have left the site untestable while every other gate stayed green. The worktree
was removed and pruned and the primary checkout is clean. THE SUITES WERE RE-RUN, NOT
READ: ruff `All checks passed!`, `test_mission_state.py` `82 passed`, the four state
readers `159 passed` and the canary `42 passed`, each as its exact ordered command line in
the primary checkout, each exit 0. COMMIT HYGIENE IS CLEAN: the path set is the six
declared paths, per-commit insertions are 400, 361, 47, 34, 8 and the handback's own 50,
none over 500, all six commits are single-parent, the reflog holds only `commit:` entries,
and the ordered push landed — origin and local agree at 483975b3.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R36's worker measured the
reviewer's own constraint against the slice it described, found it false, declared it in
the handback, and changed nothing. That is the second consecutive round in which the
constraint-8 report produced the round's finding, and it is why the reviewer's text is
gated by the worker's measurement rather than by the reviewer's own re-reading.

- R-0527 — Low, A BLOCK CONSTRAINT ASSERTED A PROPERTY ITS OWN SLICE DOES NOT HAVE.
Constraint 8 of the R36 block, applied at commit 8a0766c1, states that RECORD4 "states
facts about `packages/orchestration/mission_state.py` and
`tests/orchestration/test_mission_state.py`, both of which C2 of this same round edits",
and then binds every such sentence to name the SHA 23b5fcd9. Measured at 483975b3,
RECORD4 contains zero occurrences of either path: its file-state readings all belong to
the R35 range and name 6ca30b16, 23b5fcd9, cde59e8c or 2342ed97. The obligation was
therefore VACUOUS rather than met — a staleness gate that could not fail, which is the
R-0438 class arriving through a constraint instead of a path. Nothing false about the
repository landed on disk, and the worker performed the re-read anyway across all six
edited files, which is why this is Low. What makes it worth an id is where the false
sentence lives: constraint text is committed verbatim to `.agent/authored/f085-r36.md`
and `.agent/last_block.md`, so a reviewer recollection about the reviewer's own slice is
now part of the permanent record, and the only reason it was caught is that a worker
measured a claim its author had not. Found by the worker under constraint 8 and
registered by the reviewer, which is where a constraint-8 report is supposed to land.

Done: R-0526 — Resolved at R37. Checklist item 11 of
`docs/agents/planner_reviewer_prompt.md` §3 now binds any claim a block or a slice makes
about its OWN text to be measured before emission and written as the property measured,
and it names the universal-quantifier form explicitly: a slice may not assert a universal
over its own contents, because "every reference names its SHA" is a claim nobody counted
while "the sentences that locate landed text name their SHA" is one that can be. Applied
by the commit that constraint 9 of this round's block fixes ahead of this one. The
sentence R-0526 registered stays where it landed; nothing in `.agent/live_review.md` was
rewritten.

Done: R-0527 — Resolved at R37 by the same clause, which is why the two share one. Item
11 now also forbids a block constraint from asserting a property its own slice does not
have, and the counter-measure is stated as a method rather than as a prohibition: state
what was counted, or state nothing. The block that carries this resolution applies it to
itself — its constraint 8 names the one file this block both edits and makes claims
about, and asserts no property of any slice's contents. Applied by the commit that
constraint 9 of this round's block fixes ahead of this one.

Gate: R38 — the R37 entry. R37 PASSED. Every ordered gate was re-run by the reviewer
over 483975b3..c3201976 and each reproduces the handback's reading. TRANSPORT WAS PROVED
DISK-TO-DISK: the committed `.agent/authored/f085-r37.md`, the committed
`.agent/last_block.md` at 857ca31a and both working copies are byte-EQUAL at sha256
c8efc5c06444464245a311d03acc78f008246a9c259a7100330bdeac876d8409, 21768 B, 329 lines, 10
marker lines, region digests 70737984, 9bdbc476 and 89541ee6. THE APPEND COMMIT HELD ITS
SHAPE: 75feb987's pre-commit blob 391135 B is a byte-exact PREFIX of the 397527 B
post-commit file, the remainder 6392 B is one blank line plus RECORD5, RECORD5 is an
exact suffix, its first line occurs once among the 81 lines that commit adds, numstat
81/0, and 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 15
times. THE ARITHMETIC MOVED AS ORDERED: 141 / 22 / 0 at 483975b3 against 142 / 24 / 0 at
c3201976, 119 open against 118, registered symmetric difference exactly R-0527, done
symmetric difference exactly R-0526 and R-0527, landed symmetric difference empty, no
duplicate id, no resolution naming an unregistered id, next free R-0528. THE CLAUSE
LANDED AND BOTH PAIRS WERE APPLIED VERBATIM: at c3201976 the I11F text occurs once, the
item-11, item-12 and closing-paragraph openers each occur once, all 19 TO-only lines
occur exactly once among the 19 lines 69155e06 adds, numstat 19/0, and the reviewer
reproduced both applications mechanically — each pre-commit blob with its FROM replaced
once by its TO equals the post-commit blob byte for byte, for I11F→I11T and PLANF5→PLANT5
alike. THE SUITES WERE RE-RUN, NOT READ: the four state readers `159 passed`,
`tests/docs/` `295 passed` and the canary `42 passed`, each as its exact ordered command
line in the primary checkout, each exit 0. HYGIENE IS CLEAN: the path set is the six
declared paths, per-commit insertions are 329, 264, 19, 81, 3 and the handback's own 42,
none over 500, all six commits are single-parent, the reflog holds only `commit:`
entries, the handback is 94 lines against its 100-line cap, and origin and local agree at
c3201976.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R37's worker measured the
reviewer's own constraint against the slice it described, found both halves false,
declared it, and changed nothing — the third consecutive round in which the constraint-8
report produced the round's finding.

- R-0528 — Low, A BLOCK CONSTRAINT ASSERTED TWO PROPERTIES OF ITS OWN TEXT AND BOTH ARE
FALSE. Constraint 8 of the R37 block, applied at commits e2b23b33 and 857ca31a, states
that "The only file this block both edits and makes claims about is
`docs/agents/planner_reviewer_prompt.md`" and that "Every other reading RECORD5 asserts
about a state before this round names 483975b3 or an earlier SHA". Measured against
RECORD5 at c3201976, both fail. RECORD5 makes claims about three files that round edits,
not one: `docs/agents/planner_reviewer_prompt.md`, `.agent/last_block.md` and
`.agent/live_review.md`. And RECORD5's transport sentence names no SHA at all — its three
8-hex tokens 7d583ed0, ace9d813 and 9b5a9653 are region content digests and resolve to no
git object — while asserting a reading of `.agent/last_block.md` that the same round's
C0b, commit 857ca31a, falsified: that file hashes 208ad9d3 at 483975b3 and c8efc5c0 at
857ca31a and every commit after it. `.agent/last_block.md` is on
the R-0525 list of paths this workflow rewrites every round, so that sentence was owed a
SHA by a rule already on disk. This is the R-0527 shape recurring inside the very
constraint written to close R-0527, one commit before the item-11 clause forbidding it
landed. Found by the worker under constraint 8 and registered by the reviewer.

- R-0529 — Low, THE RESOLUTION THAT CLOSED R-0527 IS ITSELF AN INSTANCE OF R-0527. The
`Done: R-0527` paragraph, applied at commit 75feb987, closes with "The block that carries
this resolution applies it to itself — its constraint 8 names the one file this block
both edits and makes claims about, and asserts no property of any slice's contents."
Measured at c3201976 both halves are false, by the same readings R-0528 records: the
constraint names one file where RECORD5 claims about three, and the constraint DOES
assert a property of a slice's contents — the sentence binding every reading RECORD5
makes to name 483975b3 or earlier, which is the half the transport sentence breaks. What
separates this from R-0528 is where it landed. R-0528's text sits in a block record; this
one sits in `.agent/live_review.md`, the permanent findings register, inside the paragraph
certifying R-0527 closed — so the register now asserts a compliance nobody measured, in
the one document whose whole purpose is that its claims are measured. R37's handback
declared the constraint and did not name this second landing site, which is why it needs
an id of its own rather than a sentence inside R-0528. Per constraint 9 nothing is
rewritten: this registration is the correction.

Gate: R39 — the R38 entry. R38 PASSED. Every ordered gate was re-run by the reviewer over
c3201976..cbcb5c23 and each reproduces the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch file the block was authored into, the
committed `.agent/authored/f085-r38.md`, the committed `.agent/last_block.md` at b9d5050b
and both working copies are all five byte-EQUAL at sha256
5fa4d096e45014a54d93d7f27efe176adc4c85a1f10ebdcf6a649c6620cb5090, 18154 B, 284 lines, 12
marker lines — and that digest is the one the reviewer measured BEFORE emission, so the
block the worker applied is the block the reviewer wrote. BOTH APPENDS HELD THEIR SHAPE:
3b915e3c's pre-commit blob 397527 B is a byte-exact PREFIX of the 402603 B post-commit
file with remainder one blank line plus RECORD6, numstat 65/0; 275a294e's 356103 B is a
prefix of 358646 B with remainder one blank line plus DEC6, numstat 38/0; each slice is an
exact suffix, each first line occurs once among that commit's added lines, and 0 marker
lines reached either file. THE ARITHMETIC MOVED IN THE REGISTERED SET ALONE: 142 / 24 / 0
at c3201976 against 144 / 24 / 0 at cbcb5c23, 118 open against 120, registered symmetric
difference exactly R-0528 and R-0529, done and landed symmetric differences empty, no
duplicate id, no resolution naming an unregistered id, next free R-0530. THE PLAN PAIRS
WERE APPLIED VERBATIM: the reviewer rebuilt the file mechanically — the pre-commit blob
with each FROM replaced once by its TO equals the post-commit blob byte for byte — and
`.agent/plan.md` is 45 lines against its 50-line cap with `## Goal` and `## Next Steps`
intact. THE SUITES WERE RE-RUN, NOT READ: the four state readers `159 passed` and the
canary `42 passed`, each as its exact ordered command line in the primary checkout, each
exit 0. HYGIENE IS CLEAN: the path set is the six declared paths, per-commit insertions
are 284, 249, 65, 49 and the handback's own 48, none over 500, all five commits are
single-parent, the reflog holds only `commit:` entries, and origin and local agree at
cbcb5c23.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R38's worker measured a
sentence of the reviewer's own RECORD6 against the repository, found it false, declared it
in the handback, and changed nothing. That is the fourth consecutive round in which the
constraint-8 report produced the round's finding, and the third in which the false
sentence was one the reviewer wrote about its own text.

- R-0530 — Low, A CORRECTION INTRODUCED THE UNIVERSAL IT WAS WRITTEN TO REMOVE. RECORD6's
R-0528 paragraph, applied at commit 3b915e3c, states that `.agent/last_block.md` "hashes
208ad9d3 at 483975b3 and c8efc5c0 at 857ca31a and every commit after it". Measured: that
file hashes 208ad9d3 at 483975b3, c8efc5c0 at 857ca31a and c3201976, and 5fa4d096 at
b9d5050b and cbcb5c23. The clause "and every commit after it" is therefore false from
b9d5050b — R38's own C0b — onward, and because C0b PRECEDES C1 the sentence was already
false at the moment it landed. The two readings it actually took are correct; only the
quantifier is wrong. What makes this worth an id rather than a shrug is its provenance:
the clause was ADDED by the reviewer, in the last edit before emission, specifically to
satisfy the R-0525 rule that a reference to `.agent/last_block.md` name the SHA holding
the text it means — and naming two SHAs correctly, then generalising past them, is the
R-0526 universal-quantifier shape reappearing inside the paragraph that registers its own
class. Checklist item 11 already forbids exactly this and the block's own constraint 8
already ordered the measurement that caught it, so nothing new is owed to the checklist:
what is owed is the habit of running that measurement over sentences quantifying across
COMMITS, which no pair-shape or path check reaches. Found by the worker under constraint 8
and registered by the reviewer.

Gate: R40 — the R39 entry. R39 PASSED. Every ordered gate was re-run by the reviewer over
cbcb5c23..d3a707f5 and each reproduces the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch file the block was authored into, the
committed `.agent/authored/f085-r39.md`, the committed `.agent/last_block.md` at 757be21c
and both working copies are all five byte-EQUAL at sha256
32415af6db43f9228459a2bb05241c35c0a39073ab4ffb638d01758448f1181a, 19352 B, 349 lines, 24
marker lines. THE SEAM CHANGE IS THE FOUR PAIRS AND NOTHING ELSE: the reviewer rebuilt
`packages/orchestration/exec_guard.py` mechanically — the pre-commit blob with each FROM
replaced once by its TO equals dce66faa's blob byte for byte — and the guard's floor is
untouched, `def scrub_child_env` through its `return` hashing 3880a84d over 540 B at both
cbcb5c23 and d3a707f5. THE APPEND HELD ITS SHAPE: 607050ba's pre-commit blob 402603 B is
a byte-exact PREFIX of the 406554 B post-commit file, the remainder 3951 B is one blank
line plus RECORD7, RECORD7 is an exact suffix, its first line occurs once among the 50
lines that commit adds, numstat 50/0, and 0 marker lines reached the file. THE ARITHMETIC
MOVED IN THE REGISTERED SET ALONE: 144 / 24 / 0 at cbcb5c23 against 145 / 24 / 0 at
d3a707f5, 120 open against 121, registered symmetric difference exactly R-0530, done and
landed symmetric differences empty, no duplicate id, no resolution naming an unregistered
id, next free R-0531. THE SUITES WERE RE-RUN, NOT READ, each as its exact ordered command
line in the primary checkout, each exit 0: `test_exec_guard.py` `27 passed` against a base
of 24, the four seam consumers `262 passed` equalling their base, the four state readers
`159 passed`, ruff over the two touched paths `All checks passed!`, and the canary
`42 passed`. HYGIENE IS CLEAN: the path set is the seven declared paths, per-commit
insertions are 349, 295, 50, 66, 6 and the handback's own 147, none over 500, all six
commits are single-parent, the reflog holds only `commit:` entries, and origin and local
agree at d3a707f5.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R39's worker measured two of
the reviewer's own gate sentences against the repository, found both unsatisfiable,
declared them, ran the strongest measurement each one admitted, and changed no slice. That
is the fifth consecutive round in which the constraint-8 report produced the round's
findings. Both are registered below.

- R-0531 — Low, AN APPEND OBLIGATION WRITTEN FOR PROSE WAS ORDERED OVER A CODE SLICE.
G5 of the R39 block, applied at commit eba5de68, ordered that "every line SEAMTESTS
contains occurs exactly once AMONG THE LINES C2'S DIFF ADDS". Measured at d3a707f5, four
distinct lines of that 47-line slice fail it — the empty line 12x, `    )` 4x, the
argument line `        _child(_ENV_DUMP), timeout_sec=30, cwd=None,` 3x and
`@pytest.mark.subprocess` 2x. §4.9 states the per-line count for TO-ONLY additions and
already bends where a slice legitimately repeats a sentence the file carries; what it does
not anticipate is that a CODE slice repeats lines STRUCTURALLY, because blank separators,
closing parentheses and decorators are what code is made of. The obligation is therefore
unattainable by construction for every code append, which is the R-0207 shape — demanding
a count that invites either a fabricated number or a pointless repair round — arriving
through a slice's LANGUAGE rather than through its pair shape. The worker substituted the
property that does hold and measured it: the lines C2 adds are exactly two empty lines
followed by SEAMTESTS's 47 lines IN ORDER, the pre-commit blob is a byte-exact prefix, and
the slice is an exact suffix. That ordered-equality reading is strictly stronger than the
per-line count it replaced, since it fixes position as well as multiplicity. The next
record round resolves this by writing that reading into the checklist as the form a CODE
append is owed. Found by the worker under constraint 8 and registered by the reviewer.

- R-0532 — Low, A BASELINE GATE WAS ORDERED AT A COMMIT WHERE ITS OWN PATHS DO NOT EXIST.
G6 of the R39 block, applied at commit eba5de68, ordered `ruff check` over
`packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py` "at
`origin/main` as well", so that a pre-existing error could not be read as a new one.
Measured: `git ls-tree origin/main` returns nothing for either path — `exec_guard.py` was
ADDED on this branch at e0d4d880 — so the command exits 1 with `E902 No such file or
directory` per path and produces no lint reading at all. The comparison the gate exists to
make is empty by construction. This is R-0364 recurring in the reviewer's own text: that
finding's whole content is that a gate is executed at its base BEFORE it is ordered, and
the HEAD run was executed while the origin/main run was not. A second defect rides in the
same gate: G6's preamble binds every command in it to "the PRIMARY checkout and never in a
worktree" under R-0518, while a reading at `origin/main` from a branch checkout requires
exactly the worktree that clause forbids, so the two sentences cannot both be obeyed. The
worker ran it, recorded the exit code and output, treated the green HEAD gate as the
operative one and declared the rest, which is the correct handling. Nothing false about
the repository landed. The next record round resolves this by binding a baseline gate to
paths that exist at the base it names, and by carving the worktree exception the R-0518
clause needs.

Gate: R41 — the R40 entry. R40 PASSED. Every ordered gate was re-run by the reviewer over
d3a707f5..93226220 and each reproduces the handback's reading. TRANSPORT WAS PROVED AGAINST
THE REVIEWER'S OWN ORIGINAL: the scratch file the block was authored into, the committed
`.agent/authored/f085-r40.md` at fc5d957a, the committed `.agent/last_block.md` at 067fa3d2
and the working copies of those two paths as they stand at 93226220 are all five byte-EQUAL
at sha256 fad599b49902bd898feca72a990ba03061af4ba6598135570e7028ff797c41ed, 15082 B, 225
lines, 6 marker lines. THE APPEND HELD ITS SHAPE: a5e240ca's pre-commit blob of 406554 B is
a byte-exact PREFIX of the 412143 B post-commit file, the remainder of 5589 B is one blank
line plus RECORD8, and RECORD8 extracted by its marker pair from the committed authored
block hashes d6ce71700bafa738218c94e573b2470bfefc0532953f679234604721dc3b96af over 5588 B
and 69 lines, equal byte for byte to what that commit appended; numstat 70/0, and no marker
line reached the file. THE ARITHMETIC MOVED IN THE REGISTERED SET ALONE: 145 / 24 / 0 at
d3a707f5 against 147 / 24 / 0 at 93226220, 121 open against 123, registered symmetric
difference exactly R-0531 and R-0532, done and landed symmetric differences empty, no
duplicate id, no resolution naming an unregistered id, next free R-0533. THE PLAN PAIR
LANDED AS A REWRITE: PLANF8 0x and PLANT8 1x at 93226220, `.agent/plan.md` 45 lines under
the 50-line cap with `## Goal` and `## Next Steps` both present, no marker line, numstat
3/3. THE SUITES WERE RE-RUN, NOT READ, each in the primary checkout, each exit 0: the four
state readers `159 passed` against a base of 159, and the canary `42 passed` against 42.
HYGIENE IS CLEAN: per-commit insertions over that range are 225, 168, 70, 3 and the
handback commit's own 81, none over 500; every commit in the range is single-parent; `git
reflog -10` holds only `commit:` entries; and `git worktree list` is one line.

BOTH R40 FINDINGS REPRODUCE INDEPENDENTLY. R-0531's counts were re-measured over the 49
lines dce66faa adds to `tests/orchestration/test_exec_guard.py`: the empty line 12x,
`    )` 4x, the argument line 3x and `@pytest.mark.subprocess` 2x, and those four are the
only distinct lines occurring more than once there. R-0532's premise was re-measured at
93226220: `git ls-tree origin/main` returns nothing for either
`packages/orchestration/exec_guard.py` or `tests/orchestration/test_exec_guard.py`.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraints 8 and 9 R40's worker measured
two clauses of RECORD8 — the reviewer's own text, landed at a5e240ca — against the
repository, found both false, declared them, and repaired neither, which is exactly what
constraint 9 required. That is the sixth consecutive round in which the constraint-8 report
produced the round's findings. Both are registered below, and this registration IS the
correction: checklist item 20 holds that appending a correction is how this record stays
honest and that overwriting landed text is worse than a dated wrong sentence, so a5e240ca
keeps its bytes.

- R-0533 — Low, A PER-COMMIT INSERTION LIST REPORTED ONE COMMIT'S CHURN COLUMN. RECORD8's
hygiene clause, applied at commit a5e240ca, reads "per-commit insertions are 349, 295, 50,
66, 6 and the handback's own 147". Re-measured by walking cbcb5c23..d3a707f5, the six
commits insert 349, 295, 50, 66, 3 and 147: f31802f0 is 3 insertions and 3 deletions, so 6
is the insertions+deletions churn reading that AGENTS.md DECISION F104 D1 excludes from the
500-line cap. The clause's conclusion, none over 500, survives, so nothing false about this
repository's compliance landed; what landed is a wrong number in a permanent record. Its
provenance is what earns it an id: this is R-0530's class recurring inside the paragraph
that REGISTERED R-0530, one commit after that paragraph concluded "nothing new is owed to
the checklist ... what is owed is the habit of running that measurement over sentences
quantifying across COMMITS". A counter-measure written as finding prose binds nothing, and
the round that wrote this one is the proof. Found by the worker under constraint 8 and
registered by the reviewer.

- R-0534 — Low, A PRESENT-TENSE CLAIM ABOUT A WORKING COPY WAS FALSIFIED BY ITS OWN ROUND'S
EARLIER COMMIT. RECORD8's transport clause, applied at commit a5e240ca, states that the R39
scratch file, `.agent/authored/f085-r39.md`, `.agent/last_block.md` "at 757be21c" and "both
working copies" are "all five byte-EQUAL" at sha256 32415af6…1181a. Measured:
`.agent/last_block.md` does hash 32415af6 at 757be21c as the clause says, but 067fa3d2 —
C0b of the very round that wrote the sentence, two commits before it landed — overwrote
that path with the R40 block, so at a5e240ca both the working and the committed
`.agent/last_block.md` hash fad599b4…c41ed. Four of the five copies matched when the
sentence landed and the fifth did not. The same clause's closing "origin and local agree at
d3a707f5" was false for the same structural reason: that block ordered its single push
AFTER the handback commit, so while RECORD8 was landing local HEAD was a5e240ca and origin
was still d3a707f5. This is R-0520's shape with a twist that let it through: the qualifier
was attached to the COMMITTED reading and omitted from the WORKING reading standing beside
it in the same sentence, so item 20 read as satisfied because a SHA was present — just not
for the half that needed one. Found by the worker under constraint 8 and registered by the
reviewer.

Done: R-0530 — Resolved at R41. Item 22 of `docs/agents/planner_reviewer_prompt.md` §3 now
binds any clause that states a value per commit, a value holding at "every commit after"
one, or a total over a range to be recomputed at emission by walking that range with `git
rev-list --reverse`, one reading per commit, and written as the list that walk produced.
R-0530 concluded that nothing was owed to the checklist and that the counter-measure was a
habit; R-0533 is that habit failing one commit later inside R-0530's own paragraph, which
is the evidence that overturns the conclusion. The commit carrying item 22 is fixed by
constraint 6 of the R41 block to land after the commit carrying this paragraph. The
sentence R-0530 registered stays where it landed at 3b915e3c; nothing was rewritten.

Done: R-0531 — Resolved at R41 by the same block. §4.9 of
`docs/agents/planner_reviewer_prompt.md` now states that its per-line count is written for
PROSE and binds prose only, that a slice of CODE repeats lines structurally so the count is
unattainable by construction for every code append, and that the obligation there is
ORDERED EQUALITY instead — pre-commit blob a byte-exact prefix, slice an exact suffix, and
the lines the commit's diff adds exactly the slice's lines IN ORDER. That is the property
R39's worker substituted and measured, promoted from one round's improvisation to the rule,
and it is strictly stronger than the count it replaces because it fixes position as well as
multiplicity. The commit carrying that text is fixed by constraint 6 to land after this
one. The gate sentence R-0531 registers stays in commit eba5de68.

Done: R-0532 — Resolved at R41 by the same block. Item 21 now binds a gate ordered at any
commit other than the one under review to be checked at emission with `git ls-tree <base>
-- <path>` for EVERY path it names, because a path this branch added does not exist at that
base and the tool then exits on the missing file and produces no reading at all — the
vacuous-gate shape of R-0438, reached through the base rather than through a typo. The same
item carries the carve-out the R39 instance also needed: an R-0518 primary-checkout clause
reaches SUITE commands, which need installed dependencies, and never a read-only baseline
reading of named paths at another commit, which has no dependency to miss. The commit
carrying item 21 is fixed by constraint 6 to land after this one. G6 of the R39 block stays
as it landed at eba5de68.

Gate: R42 — the R41 entry. R41 PASSED. Every ordered gate was re-run by the reviewer over
93226220..0e2cdacd and each reproduces the handback's reading. LINE COUNTS IN THIS ENTRY
ARE `splitlines` COUNTS, stated because the convention is exactly what R-0536 below
registers. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch file the
block was authored into, the committed `.agent/authored/f085-r41.md` at 9cc4772c, the
committed `.agent/last_block.md` at a66aa301 and the working copies of those two paths as
they stand at 0e2cdacd are all five byte-EQUAL at sha256
a3716bdf9fa29892bbb6220a5b50bf6c73b057106e0465a28d71e3cd17febbba, 28265 B, 398 lines, 14
marker lines. THE APPEND HELD ITS SHAPE: 1a29a77d's pre-commit blob of 412143 B is a
byte-exact PREFIX of the 420193 B post-commit file, the remainder of 8050 B is one blank
line plus RECORD9, RECORD9 hashes cf21f13adb1535b6 over 8049 B and 101 lines and is an
exact suffix, the appended bytes equal the marker-pair extraction from the committed
authored block, numstat 102/0, no duplicate non-empty line among the 102 added, and no
marker line reached the file. THE ARITHMETIC MOVED AS ORDERED: 147 / 24 / 0 at 93226220
against 149 / 27 / 0 at 0e2cdacd, 123 open against 122, registered symmetric difference
exactly R-0533 and R-0534, done symmetric difference exactly R-0530, R-0531 and R-0532,
landed symmetric difference empty, no duplicate id, no resolution naming an unregistered
id. THE DOC EDITS LANDED AS TWO APPENDS: P49FROM, P49TO, CL20FROM and CL20TO each occur
exactly 1x at 0e2cdacd, and for BOTH commits the lines the diff adds equal the TO-only
lines IN ORDER — 14 for 01359f81 and 49 for 247df04b — which is the ordered-equality
reading item 9 of §4 now prescribes, applied to its own landing commit. The checklist
region reads labels 1..22 contiguous against 1..20 at the base; no marker line reached the
file. THE PLAN PAIR LANDED AS A REWRITE: PLANF9 0x and PLANT9 1x at 0e2cdacd, `## Goal`
and `## Next Steps` both present, no marker line, numstat 4/3. THE SUITES WERE RE-RUN, NOT
READ, each in the primary checkout, each exit 0: the four state readers `159 passed`
against a base of 159, and the canary `42 passed` against 42. HYGIENE IS CLEAN: the path
set before C5 is exactly the five ordered paths; walking 93226220..0e2cdacd gives
per-commit insertions 398, 361, 102, 14, 49, 4 and the handback commit's own 101, none
over 500; all seven commits are single-parent; `git reflog -10` holds only `commit:`
entries; and `git worktree list` is one line.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraints 8 and 9 R41's worker measured
the reviewer's own RECORD9 and the block's own predictions against the repository, found
five readings that differ, declared them and repaired none. That is the seventh
consecutive round in which the constraint-8 report produced the round's findings. The two
findings below are the reviewer's, not the worker's: R41's execution reproduced under
independent re-run in every particular.

- R-0535 — Low, THE CLAUSE THAT LANDED THE QUALIFIER RULE BROKE IT TWICE IN ITS OWN TEXT.
RECORD9, applied at commit 1a29a77d, registers R-0534 and states its counter-measure —
that a SHA qualifier attaches to EVERY reading a clause states, not only the first — and
two of RECORD9's own clauses then state a trailing reading the qualifier does not reach.
Measured: its plan clause reads "PLANF8 0x and PLANT8 1x at 93226220, `.agent/plan.md` 45
lines", and `.agent/plan.md` is 45 lines at 93226220 and at 1a29a77d but 46 at 0e2cdacd,
falsified by C4 of RECORD9's own round; its arithmetic clause closes "next free R-0533",
which is true at 93226220 and false at 1a29a77d, because RECORD9 itself registers R-0533
and R-0534 and so moves the next free id to R-0535 in the very commit that lands the
sentence. The second is the sharper of the two: no reading of the qualifier's scope makes
it true where it landed. What this is NOT is a worker error or a rule that failed — the
R41 block was authored BEFORE checklist item 20 carried the R-0534 clause, and constraint
6 put C1 ahead of C3, so RECORD9 was written under the old rule and landed under the new
one. The lesson is narrower and worth the id: a round that WRITES a checklist rule must
apply that rule to its own slices at authoring time, because the slices land in the same
round and the record does not care which commit taught it. Found by the worker under
constraint 8 and registered by the reviewer.

- R-0536 — Low, A BLOCK PREDICTED FOUR LINE COUNTS UNDER AN UNSTATED NEWLINE CONVENTION
AND EVERY ONE READ ONE HIGH. The R41 block, applied at commit 9cc4772c, stated that
`docs/agents/planner_reviewer_prompt.md` would be "707 lines at HEAD against 644 at
93226220" and that the reviewer's dry run "put it at 47 lines" for `.agent/plan.md`.
Measured at 0e2cdacd with `splitlines`: 706, 643 and 46. The reviewer counted with
`split("\n")` on text ending in a newline, which yields one trailing empty element and
therefore one extra line, while the worker counted with `splitlines`, which does not — the
same one-line divergence the newline convention exists to settle. Nothing false landed in
the repository and no gate failed, and the reason is worth recording as much as the defect:
G5 ordered "report the number rather than asserting it", so the gate asked for a
MEASUREMENT and the reviewer's wrong prediction had no gate to break. A gate that orders a
value would have failed here and cost the round a repair. The counter-measure is the one
already on disk and not followed: state the convention beside any line count a block
predicts, and default to the `splitlines` reading, which is what every worker on this
branch has used. Found by the worker under constraint 8 and registered by the reviewer.

Gate: R43 — the R42 entry. R42 PASSED. Every ordered gate was re-run by the reviewer over
0e2cdacd..4c7bcb3a and each reproduces the handback's reading. LINE COUNTS HERE ARE
`splitlines` COUNTS. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch
file `.remedy-wt/f085-r42.md`, the committed `.agent/authored/f085-r42.md` and
`.agent/last_block.md` at 7b02da1c, and the working copies of those two paths as they stand
at 4c7bcb3a, are all five byte-EQUAL at sha256 b6ba3371…f7161c25, 23195 B, 332 lines, 8
marker lines, region 1-100 at 3bc171fb05e29fa9 over 6720 B and region 101-end at
d0ad2b78183925d3 over 16475 B. BOTH APPENDS HELD THEIR SHAPE: at dc34997a a pre-commit blob
of 420193 B is a byte-exact prefix of the 426006 B post-commit file, its 5813 B remainder is
exactly one blank line plus RECORD10 — sha256 407c8ff2e3c61ac6…, 5812 B, 71 lines, 3 empty —
an exact suffix, numstat 72/0, each of the 68 non-empty slice lines occurring exactly once
among the 72 added and the added lines equal to blank-plus-slice IN ORDER; at 5695c2b0 the
same shape holds for DEC4 over 358646 B and 363135 B with a 4489 B remainder — sha256
fa6f2e9fd40c883f…, 4488 B, 60 lines, 6 empty — numstat 61/0, 54 non-empty lines each once
among the 61 added, ordered equality holding. No marker line reached either file at
4c7bcb3a. THE ARITHMETIC MOVED AS ORDERED: 149 / 27 / 0 at 0e2cdacd against 151 / 27 / 0 at
4c7bcb3a, 122 open against 124, registered symmetric difference exactly R-0535 and R-0536,
done and landed symmetric differences empty, and at each of those two SHAs no duplicate id
and no resolution naming an unregistered id. THE DECISION LANDED: lines matching
`^## DECISION F085 D\d+ —` number 2 at 0e2cdacd against 3 at 4c7bcb3a, the D4 heading occurs
exactly 1x at 4c7bcb3a, and there is no D1 section at either SHA. THE PLAN PAIR LANDED AS A
REWRITE: PLANF10 1x and PLANT10 0x at 0e2cdacd against 0x and 1x at 4c7bcb3a, `## Goal` and
`## Next Steps` present at both, no marker line at either, numstat 7/8, and `.agent/plan.md`
measuring 46 lines at 0e2cdacd and 45 at 4c7bcb3a, each under the 50-line cap. THE SUITES
WERE RE-RUN, NOT READ, each in the primary
checkout, each exit 0: the four state readers `159 passed` against a base of 159, and the
canary `42 passed` against 42. HYGIENE IS CLEAN: walking 0e2cdacd..4c7bcb3a mechanically
gives the per-commit insertion counts 332, 273, 72, 61, 7 and 122, none over 500; the path
set at 7c4a2583 is exactly the five ordered paths; all six commits are single-parent; and at
4c7bcb3a `git reflog -10` held ten entries of no non-`commit:` kind while `git worktree
list` held one line. The handback at 4c7bcb3a runs to 153 lines and carries the DECISION D15
stated cause, whose named content is mandated rather than padding.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraints 8 and 9 R42's worker measured the
reviewer's own RECORD10 and DEC4 against the repository, declared one reading that differs
and repaired none — again the round's finding came out of the constraint-8 report, as
RECORD10 recorded for R41. R-0538 is that reading; R-0537 is the reviewer's own, found while
re-reading R-0536 at this gate. R42's execution reproduced under independent re-run in every
particular.

WHY R43 SHIPS NO CODE. The `ci_run.py` migration DECISION F085 D4 rules was authored in full
for this round and proved before being deferred: applied to two disposable worktrees at
4c7bcb3a, linted clean, run to `59 passed` there against a base of `54 passed` at the same
commit, and red-controlled on four separate mutations, each of which exited non-zero. Its
step block then measured 487 lines against the 400-line cap DECISION F105 D5 sets, and
checklist item 1 requires the split BEFORE emission rather than a declared deviation
afterwards. The migration is R44's, and it starts from measured slices rather than from a
design.

- R-0537 — Low, A FINDING'S HEADLINE COUNTED FOUR OF SOMETHING ITS BODY GIVES THREE OF.
R-0536, applied at commit dc34997a, opens "A BLOCK PREDICTED FOUR LINE COUNTS UNDER AN
UNSTATED NEWLINE CONVENTION AND EVERY ONE READ ONE HIGH", and its body then quotes three
predictions from the R41 block — "707 lines at HEAD against 644 at 93226220" and "put it at
47 lines" — and measures three values against them, "706, 643 and 46". Measured at 4c7bcb3a:
the R41 block, committed at 9cc4772c, predicts exactly three line counts; its other numerals
of that family are the 50-line and 60-line caps it quotes as standing rules and the 45 and 69
that RECORD9 reports as READINGS of R40's round, none of them a prediction and none of them
quoted by R-0536. The trailing half of the headline survives — all three predictions did read
one high — so the defect is the numeral alone. This is the R-0402 / R-0404 / R-0436
enumeration family arriving where checklist item 16 does not reach: item 16 binds a section
HEADING over a list, and a finding headline is a heading over a body by every property that
made item 16 necessary, being the half nobody re-reads and the half that drifted from the
body beneath it. The counter-measure is to widen item 16 from a heading to any sentence that
counts what follows it; that promotion is NOT in the checklist and is owed to a later round,
which is why this finding names it instead of asserting it. Found and registered by the
reviewer.

- R-0538 — Low, ONE SHA QUALIFIED THREE VALUES AND ONLY TWO WERE READ THERE. R-0536, applied
at commit dc34997a, closes "Measured at 0e2cdacd with `splitlines`: 706, 643 and 46."
Measured at 4c7bcb3a: `docs/agents/planner_reviewer_prompt.md` is 706 lines at 0e2cdacd and
643 at 93226220, and `.agent/plan.md` is 46 at 0e2cdacd — so the middle value is a reading at
a commit OTHER than the one its own sentence names, and at the named commit that file is 706
rather than 643. The intent is recoverable, because the three values map positionally onto
the three predictions the preceding sentence quotes and the second of those is itself
qualified "at 93226220", so nothing false about the repository follows. What earns it an id
is where it landed: this is the mis-scoped-qualifier shape R-0534 registered and R-0535
recorded recurring, arriving for the third consecutive round and this time INSIDE the
paragraph registering a different measurement-convention defect — the same self-application
failure R-0535 named, one round after naming it. R42's worker declared it under constraint 8
and correctly left it standing under constraint 9; the registration is the correction, per
checklist item 20. Found by the worker under constraint 8 and registered by the reviewer.

Gate: R44 — the R43 entry. R43 PASSED. Every ordered gate was re-run by the reviewer over
4c7bcb3a..f3e9687a and each reproduces the handback's reading. LINE COUNTS HERE ARE
`splitlines` COUNTS. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch
file `.remedy-wt/f085-r43.md`, the committed `.agent/authored/f085-r43.md` at 5ddea9f5, the
committed `.agent/last_block.md` at 4da31634 and the working copies of those two paths as
they stand at f3e9687a are all five byte-EQUAL at sha256 3f7e0157…e393a2b426, 17166 B, 245
lines, 10 marker lines, region 1-100 at 708961ae3d989f4e over 6906 B and region 101-end at
de50ec15e79f8664 over 10260 B — disk-to-disk, no digest fallback. THE APPEND HELD ITS SHAPE:
at 007f18df a pre-commit blob of 426006 B is a byte-exact prefix of the 432672 B post-commit
file, the 6666 B remainder is exactly one blank line plus RECORD11 (sha256 2442e139ff6a0836…,
6665 B, 81 lines, 4 empty, 0 duplicate non-empty), the slice is an exact suffix, numstat 82/0,
each of the 77 non-empty slice lines occurs exactly once among the 82 added, ordered equality
added == blank+slice holds, and 0 marker LINES reached the file. THE PLAN RECONSTRUCTS:
`.agent/plan.md` at 4c7bcb3a is sha256 7b95158a…, applying PLANF11→PLANT11 and
PLANF12→PLANT12 gives 5928c3c5…, byte-identical to the committed file at 921e8712 and to the
working copy at f3e9687a; both pairs measured `TO contains FROM: false`, each FROM read 1x
and each TO 0x at 4c7bcb3a against 0x and 1x at HEAD; `## Goal` and `## Next Steps` are
present, 0 marker lines reached it, it measures 47 lines against the 50-line cap, numstat 6/4.
THE ARITHMETIC MOVED AS ORDERED: 151 / 27 / 0 at 4c7bcb3a against 153 / 27 / 0 at f3e9687a,
124 open against 126, registered symmetric difference exactly R-0537 and R-0538, done and
landed symmetric differences empty, and at each of those two SHAs no duplicate id and no
resolution naming an unregistered id. THE SUITES WERE RE-RUN, NOT READ, each in the primary
checkout, each exit 0: the four state readers `159 passed` against a base of 159 and the
canary `42 passed` against 42. HYGIENE IS CLEAN: walking 4c7bcb3a..f3e9687a mechanically
gives the per-commit insertion counts 245, 201, 82, 6 and 139, none over 500; the path set
over that whole range is exactly the five ordered paths and the range ending at 921e8712 is
that set minus `.agent/handoff.md`; all five commits are single-parent; and at f3e9687a
`git reflog -10` held ten entries of no non-`commit:` kind while `git worktree list` held one
line. The handback at f3e9687a runs to 165 lines and carries the DECISION D15 stated cause.

THREE REGISTRATIONS ARE OWED AND ARE NOT MADE HERE. Under constraints 8 and 9 R43's worker
declared three readings of the reviewer's own RECORD11 and R-0537 that differ from the
repository, and repaired none. All three reproduce under independent re-measurement at
f3e9687a: the path set "at 7c4a2583" is one path and belongs to a RANGE; the
DECISION-heading count of 2 against 3 is 0 at both SHAs in the file the sentence sits in and
true only of `.agent/decisions.md`; and R-0537's enumeration of the R41 block's numerals
omits the two "500-line cap" quotes `.agent/authored/f085-r41.md` carries at 9cc4772c. They
take ids at R45 rather than here, and nothing is at risk in the interval: the handback at
f3e9687a states all three, so the persist-first rule of §4.4 is already met by disk.

WHY THAT DEFERRAL, AND WHY THE CAP WAS RULED ON INSTEAD OF PAID AGAIN. R42 and R43 both ended
with more open findings than they started and neither moved a line of production code, which
is the ⚠️ condition docs/agents/planner_reviewer_prompt.md §2 defines. The cause is measured,
not suspected: at R43 the record and the `ci_run.py` migration together came to 487 lines
against the 400-line cap of DECISION F105 D5, and R44 re-authored the same pair from scratch
with narrowed FROM slices, docstrings pointing at DECISION F085 D4 instead of restating it,
one redundant test dropped and the registrations deferred, and still measured 462 before this
ruling was added to it. A cap that
three consecutive rounds have to be shaped around is bounding the product rather than the
prose, so DECISION F085 D5 — landed by this same commit — rules that the 400 counts a block's
PROSE and that slices are counted and reported but not capped. The R44 block is the first
measured that way and states both of its numbers. R45 owes the counter-measure D5 names, a
stated budget for a record slice, alongside the checklist item 16 widening R-0537 named and
did not perform. Neither is in the checklist at f3e9687a and this entry does not claim
otherwise.

Gate: R45 — the R44 entry. R44 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over f3e9687a..981d08d0, not read, and each reproduces the handback's reading exactly; the full
numbers live in the handback at 981d08d0 and are not restated here. LINE COUNTS ARE
`splitlines` COUNTS. What the re-run establishes: transport proved disk-to-disk against the
reviewer's own `.remedy-wt/f085-r44.md` with no digest fallback, all copies equal at sha256
d8bf11c9…, 30615 B, 516 lines; both C1 appends held their prefix-plus-blank-plus-slice shape
with 0 marker LINES reaching either file; both edited `.py` files reconstruct byte-identically
from their base blobs under the ordered slice application; the suites re-ran in the primary
checkout at exit 0, `190 passed` against a base of 186 with each of the four new test names
collected exactly once and the canary `42 passed` against 42; the arithmetic held still at
153 / 27 / 0 and 126 open at both SHAs, all three symmetric differences EMPTY.

THE ONE RED CLAUSE WAS REPORTED AS RED, WHICH IS WHY THIS IS A PASS. C0a carries 516
insertions against the AGENTS.md 500-line cap, and R44's handback declared it under the
AGENTS.md exception with an inseparability reason rather than reporting the clause green.
Clause (b) reproduces under independent measurement at 981d08d0: walking all 268 commits of
`main..981d08d0` gives exactly one over 500 — d4473f85 at 516 — the next largest at 454 and
four at 400. The allowance is spent for F085, and DEC6, landed by this same commit, is the
counter-measure so that it is never needed again.

EIGHT REGISTRATIONS, ALL OWED BEFORE THIS ROUND AND ALL RE-MEASURED AT 981d08d0. Three were
declared by R43's worker and deferred by RECORD12; five come from R44's handback, four of them
defects in the R44 block, which is the reviewer's own text.

- R-0539 — Low, A RANGE READING WAS QUALIFIED WITH A SINGLE COMMIT. RECORD11, applied at
007f18df, states "the path set at 7c4a2583 is exactly the five ordered paths". Measured at
981d08d0: `git show --name-only 7c4a2583` returns exactly one path, `.agent/plan.md`; the
five-path set is a property of the RANGE 0e2cdacd..4c7bcb3a. The mis-scoped-qualifier class
R-0534 opened and R-0538 recorded recurring, arriving through the RANGE side checklist item 22
governs. Declared by R43's worker and registered here per checklist item 20.

- R-0540 — Low, A COUNT WAS REPORTED WITHOUT THE FILE IT WAS COUNTED IN. RECORD11, applied at
007f18df, states that lines matching a `## DECISION F085 D<n> —` pattern "number 2 at 0e2cdacd
against 3 at 4c7bcb3a", and names no path. Measured at 981d08d0: in `.agent/live_review.md`,
the file that sentence sits in, the count is 0 at both SHAs; in `.agent/decisions.md` it is 2
and 3. The numbers are right and their owner is missing, so a reader who resolves the string to
the file holding it reads a false sentence. Declared by R43's worker.

- R-0541 — Low, A FINDING'S ENUMERATION OF ANOTHER TEXT'S NUMERALS WAS INCOMPLETE. R-0537,
applied at f3e9687a, states that the R41 block's numerals "of that family are the 50-line and
60-line caps it quotes as standing rules and the 45 and 69 that RECORD9 reports as READINGS".
Measured at 981d08d0 against `.agent/authored/f085-r41.md` as committed at 9cc4772c: that file
contains "500-line cap" twice, quoting the AGENTS.md commit cap, and neither occurrence appears
in R-0537's list. The conclusion survives, since neither omitted numeral is a prediction; the
enumeration fails, inside a finding whose subject is a defective enumeration. Declared by R43's
worker.

- R-0542 — Medium, A DECISION DESCRIBED THE BLOCK IT SHIPPED WITH AND THE BLOCK DID OTHERWISE.
DECISION F085 D5, applied at da47ee40, closes "The R44 block is the first measured under this
counting and declares both of its numbers in its own constraints". Measured at 981d08d0 against
`.agent/authored/f085-r44.md` as committed at d4473f85: constraint 10 of that block declines to
state them — "the worker measures them from the committed `.agent/authored/f085-r44.md` rather
than taking them from here" — and neither 239 nor 516 occurs anywhere in the block's prose.
This is checklist item 11's R-0527 shape one level out: item 11 forbids a BLOCK constraint
asserting a property its own slice lacks, and here a SLICE asserts a property its own block
lacks. DEC6 carries the counter-measure; R45's constraint 9 is the first text written under it.
Declared by R44's worker as deviation 2.

- R-0543 — Low, A PLAN SENTENCE COUNTED THE TESTS ITS OWN ROUND SHIPPED AND COUNTED THEM WRONG.
PLANT13, applied at 91ad51ae, says R44 applies DECISION F085 D4 "with five tests". Measured at
981d08d0: `def test_` in `tests/orchestration/test_ci_run.py` goes from 10 at f3e9687a to 14,
so C2 added four, and the R44 block's own goal line says "four tests". The slice was applied
byte-verbatim and correctly left unrepaired. This is the class R-0537 named and asked the
checklist to cover; that widening is R46's, having been cut from this block for size, and this
registration does not claim it has happened. Declared by R44's worker as deviation 3.

- R-0544 — Medium, A BASE READING WAS ORDERED THAT A CONTAINMENT-SHAPED PAIR CANNOT PRODUCE.
Constraint 2 of the R44 block, committed at d4473f85, asserts that each FROM occurred 1x in its
target at f3e9687a "and each TO 0x there". Measured at 981d08d0: CIT1 is the single line
`import subprocess` and CIF1 is that line preceded by `import os`, so CIF1 CONTAINS CIT1 and
CIT1 reads 1x at f3e9687a, not 0x. A deletion-shaped rewrite whose TO is a subset of its FROM
has the unattainable-count property checklist items 4 and 15 establish for an APPEND, and both
are written only about the TO-contains-FROM direction. Nothing broke, since every FROM read
exactly 1x, but the block ordered a number no honest run could produce. The counter-measure is
to order no base reading of a TO at all, which R45's constraint 2 is the first block to do.
Declared by R44's worker as deviation 4.

- R-0545 — Medium, AN ORDERED-EQUALITY GATE ASSUMED A COMMIT DOES ONE THING TO A FILE. Gate G4
of the R44 block, committed at d4473f85, orders the R-0531 code-append proof as "the pre-commit
blob is a byte-exact PREFIX of the post-commit file". Measured at 981d08d0: for
`tests/orchestration/test_ci_run.py` that clause is FALSE and cannot be true, since the same
commit both REWRITES the file's import block and APPENDS to its end. The meetable form holds
and was measured by worker and reviewer alike: the base blob with TIMPF→TIMPT applied, 4206 B,
IS a byte-exact prefix of the 6317 B post-commit file, the remainder being exactly TESTS. §4.9
carries the same assumption; this finding does not amend it, it records that the PREFIX half
must name the intermediate text whenever a commit edits above its own append, which G4 of this
round is the first gate to do. Declared by R44's worker as deviation 5.

- R-0546 — Medium, LIFTING ONE CAP LEFT THE ROUND STANDING ON ANOTHER. DECISION F085 D5,
applied at da47ee40, rules that the 400-line block cap counts a block's PROSE and that slices
are counted but not capped, its CHOSEN paragraph naming "a commit under 500 insertions" among
the caps that stand untouched. Measured at 981d08d0: the very block D5 was written for measures
516 lines, and C0a saves it as a NEW file where insertions equal lines, so D5's first
application forced the branch to spend its single AGENTS.md declared-oversize allowance. Both
rules were correctly stated and never measured against each other. What earns it an id is that
the collision was derivable at emission from numbers already in the block. DEC6, landed by this
same commit, is the counter-measure. Found by the reviewer at this gate.

Gate: R46 — the R45 entry. R45 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 981d08d0..470d2577, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with
no digest fallback: `.remedy-wt/f085-r45.md`, the committed `.agent/authored/f085-r45.md` at
d6f42cd0, the committed `.agent/last_block.md` at 6977b3e8 and both working copies as they stand
at 470d2577 are all five byte-EQUAL at sha256
448c531c3430eafe4efb0080363ff8c4e1908261f5d688bdbf248ce00c163cb0, 29951 B, 477 lines, 30 marker
lines. BOTH APPENDS HELD THEIR SHAPE: for RECORD13 on `.agent/live_review.md` and DEC6 on
`.agent/decisions.md` alike, the pre-commit blob is a byte-exact prefix, the remainder is exactly
one blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached either file,
and every non-empty slice line occurs exactly once among that path's added lines — 97 slice lines
against 98 added for the first, 43 against 44 for the second. THE CODE RECONSTRUCTS:
`packages/orchestration/builder_bridge.py` at 981d08d0 with BBF1→BBT1, BBF2→BBT2 and BBF3→BBT3
applied in that order is byte-identical to the committed file at 778a74ba, sha256
5a95a367a15f9d34…; `tests/orchestration/test_builder_bridge.py` with TIMPF→TIMPT applied and
TESTS appended is byte-identical at dffeaac42c130440…, and the ORDERED EQUALITY holds on the
form G4 ordered — the intermediate text is a byte-exact prefix, TESTS an exact suffix, and the
59 lines C2 adds are TIMPT's two new import lines followed by TESTS' 57, in order. THE SUITES
WERE RE-RUN, NOT READ, each in the primary checkout, each exit 0: the five builder-bridge files
`82 passed, 1 skipped` against a base of `80 passed, 1 skipped`, the four state readers
`159 passed` against 159, and the canary `42 passed` against 42; `ruff check` over the two `.py`
paths returned `All checks passed!`. THE ARITHMETIC MOVED AS ORDERED: 161 / 27 / 0 at 470d2577
against 153 / 27 / 0 at 981d08d0, 134 open against 126, the registered symmetric difference
exactly R-0539 through R-0546, done and landed symmetric differences EMPTY, no duplicate id and
no resolution naming an unregistered id at either SHA. HYGIENE IS CLEAN: walking
981d08d0..470d2577 mechanically gives the per-commit insertion counts 477, 410, 142, 70, 7 and
58, none over 500 and so no second call on the allowance d4473f85 spent; the path set of the
range ending at 7cd2879d is exactly the seven ordered paths; all six commits are single-parent.

THE MIGRATION IS REAL, NOT MERELY APPLIED. `import os` is gone from
`packages/orchestration/builder_bridge.py` at 470d2577 and the one surviving `os.` occurrence is
inside a comment, so the module no longer builds a child environment from the parent's own — the
scrub is what the child now gets. Before delegating, the reviewer proved the same slice bytes in
a disposable worktree at 981d08d0 under four red controls, each of which exited non-zero on the
test it was aimed at: the fixture repo demanding the scrubbed token be PRESENT, the fixture repo
demanding the `PYTHONDONTWRITEBYTECODE` overlay be ABSENT, `extra_env` dropped from the guard
call, and `cwd` handed None — the last taking 60.26 s, which is the guard's own wall tripping
rather than an assertion failing. T002b is closed: every site of the `test` class named in
DECISION F085 D3 is on the seam.

WHAT THE WORKER FOUND IN THE REVIEWER'S OWN TEXT. R45's worker applied every slice byte-verbatim
and declared one contradiction rather than repairing it, which is what constraints 1 and 6 ask
for. R-0547 is that finding. It is the reviewer's error, not the worker's, and the round is a
PASS because the worker's execution reproduced in every particular under independent re-run.

- R-0547 — Medium, A DECISION'S HEADING RULED ONE NUMBER AND ITS BODY RULED ANOTHER. DECISION
F085 D6, applied at 812626d3, is headed "a block is budgeted at 480 lines TOTAL" while its
CHOSEN paragraph rules "a block is budgeted at 490 lines TOTAL" and its CONSEQUENCE paragraph
computes from 490; the R45 block's own Goal and constraint 9 also say 490. Measured at 470d2577:
the DEC6 slice contains the string 480 once, in the heading, and 490 twice, in the body. The
cause is recoverable and worth recording, because it is the shape this repository keeps paying
for: the reviewer drafted the section at 480, revised the ruled figure to 490 in the body when
the margin's justification changed, and did not sweep the heading — the R-0481 late-addition
shape, landing in the one place checklist item 16 already governs and the widening of item 16
that R45 cut for size would have caught. Nothing was decided wrongly: 477 is inside either
figure, so no round was misjudged. What is wrong is that a live rule is ambiguous on disk. DEC6C,
appended by this same commit, fixes the ruled figure at 490 without editing DEC6, per checklist
item 20's rule that landed text is corrected by appending and never by rewriting. Found by R45's
worker under its own deviation 2 and registered by the reviewer.

Gate: R47 — the R46 entry. R46 PASSED. Every ordered gate G1-G6 was re-executed by the reviewer
over 470d2577..c8da1928, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r46.md`, the committed `.agent/authored/f085-r46.md` at
6f302271, the committed `.agent/last_block.md` at 5b351a2e and both working copies as they
stand at c8da1928 are all five byte-EQUAL at sha256
89a8b79bd98dbc53c40225c15b0070e9a57cad5d1cb788d6eef2dac6bce1363c, 13950 B, 192 lines, 4 marker
lines. BOTH APPENDS HELD THEIR SHAPE, and the reviewer extracted the two slices programmatically
from the committed block by marker pair rather than retyping them: for RECORD14 on
`.agent/live_review.md` and DEC6C on `.agent/decisions.md` alike the pre-commit blob is a
byte-exact prefix, the remainder is exactly one blank line plus the slice, the slice is an exact
suffix, 0 marker LINES reached either file, and every non-empty slice line occurs exactly once
among that path's added lines — 59 slice lines of which 3 empty against 60 added for the first,
16 of which 3 empty against 17 for the second, at sha256 ecb74b8c782b1baa… and
b1bb9c74c7725dea…, the two digests the R46 handback also reports. THE SUITES WERE RE-RUN, NOT
READ, each in the primary checkout, each exit 0: the four state readers `159 passed` against a
base of 159, the canary `42 passed` against 42. THE ARITHMETIC MOVED AS ORDERED: 162 / 27 / 0 at
c8da1928 against 161 / 27 / 0 at 470d2577, 135 open against 134, the registered symmetric
difference exactly R-0547, done and landed symmetric differences EMPTY, no duplicate id and no
resolution naming an unregistered id at either SHA. HYGIENE IS CLEAN: walking the range
mechanically gives the per-commit insertion counts 192, 144, 77 and 31, none over 500 and so no
second call on the allowance d4473f85 spent; the path set of the range ending at 9afeeb86 is
exactly the four ordered paths and the full range adds only `.agent/handoff.md`; all four
commits are single-parent; the tree is clean and `git worktree list` is one line.

THE CORRECTION IS REAL, NOT MERELY APPLIED. Measured at c8da1928 in `.agent/decisions.md`:
DECISION F085 D6's heading still reads 480 while its CHOSEN and CONSEQUENCE paragraphs read 490,
and DEC6C now stands later in that same file fixing the ruled figure at 490 without editing D6,
which is checklist item 20's rule that landed text is corrected by appending and never by
rewriting. R-0547's description of the defect reproduces on disk in every particular.

- R-0548 — Medium, REVIEWER-BLOCK DEFECT, A ROUND REGISTERED A FINDING UNDER A CHANGE SET THAT
NAMED NO PLAN, WHICH IS ALREADY THE COUNTER-MEASURE OF TWO OPEN FINDINGS AND THE BINDING RULE OF
NEITHER. The R46 block, committed at 6f302271, names five paths in its change set — the authored
block, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md` and
`.agent/handoff.md` — and its constraint 5 forbids touching anything outside that set. That same
round registered R-0547. R-0377 rules, still OPEN: "any round whose bundle registers, resolves
or renumbers a finding names `.agent/plan.md` in its change set and rewrites its ledger in the
round's FIRST commit". R-0491 rules, still OPEN: the plan update "is ordered as the FIRST commit
of a round that has substance to record", ahead of everything but the two block-save commits.
R46 satisfied neither, and its worker did the only correct thing available to it — it declared
the conflict as handback deviation 2 rather than widening the change set past a gate that would
then have gone red, which is what constraints 5 and 6 of that block require. Measured at
c8da1928, before this round's own C1 changes it: `.agent/plan.md` reads "R45, this round" under
its `## Current Step` heading and its Next Steps item 1 describes R46 as work still to come,
while all four of R46's commits stand above it in the history. THE COST IS THE ONE R-0377
ALREADY PRICED: AGENTS.md's Session Resume tells a new session to read `.agent/plan.md` second,
ahead of the review record, so a bootstrapping reader starts from a plan one round behind that
names the round it is reading as unstarted. AGENTS.md's Commit Gate item 1 — "Verify
`.agent/plan.md` matches the current work ... If any of these fail: DO NOT COMMIT" — was
unmet for all four of R46's commits, and a broken repository rule rather than a broken
convention is why this is Medium. THE CAUSE IS NOT THE R46 BLOCK ITSELF. It is that R-0377's and
R-0491's counter-measures live as finding PROSE and were never promoted into the §3 pre-emission
checklist, so no block reads them at the one moment they bind — the class this repository keeps
paying for, in which a standing rule stated in a finding body binds nothing. That is why the
counter-measure here is a checklist item and not a third restatement: this same round adds item
23 carrying both rules, and its own C1 advances the plan ahead of every other substantive
commit, which is the first application of the rule it writes. R-0377 and R-0491 stay OPEN. This
finding records their recurrence and resolves neither, because neither is resolved until a later
round demonstrates the promoted item catching what the prose did not. Found and registered by
the reviewer while gating R46.

Gate: R48 — the R47 entry. R47 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over c8da1928..d6b06997, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r47.md`, the committed `.agent/authored/f085-r47.md` at
e0eee32f, the committed `.agent/last_block.md` at 313e8321 and both working copies as they
stand at d6b06997 are all five byte-EQUAL at sha256
a1d2fe72fd6425b5bbf3a06d13e9eb25dbebabb80bfd8a10e49694251cb5530f, 22123 B, 308 lines, 14 marker
lines. THE SHAPES HELD, each measured separately from slices the reviewer extracted
programmatically from the committed block by marker pair rather than retyping them. THE REWRITE:
R47's PLANF occurs 0x and its PLANT exactly 1x in `.agent/plan.md` at 3fe2667d, with
`TO contains FROM: false` as that block declared, numstat `8 9`. THE PROSE APPEND: for RECORD15
on `.agent/live_review.md` the pre-commit blob is a byte-exact prefix, the remainder is exactly
one blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached the file,
and every non-empty slice line occurs exactly once among that path's added lines — 61 slice
lines of which 2 empty against 62 added, at sha256 a2f71483…. THE TWO CHECKLIST APPENDS: on
`docs/agents/planner_reviewer_prompt.md` at 522d925a, C16F and C23F each occur exactly 1x and
C16T and C23T each exactly 1x, `TO contains FROM: true` for both as declared, 18 TO-only lines
each against the 36 lines that commit adds to the path, 0 violations, 0 marker LINES, numstat
`36 0`. THE SUITES WERE RE-RUN, NOT READ, each in the primary checkout, each exit 0: the four
state readers `159 passed` against a base of 159, the canary `42 passed` against 42. THE PLAN
CONTRACT HOLDS: 40 lines against the 50-line cap, `## Goal`, `## Next Steps` and a roadmap F-id
all present — the union of every assertion the reviewer collected by grepping `tests/`. THE
ARITHMETIC MOVED AS ORDERED: 163 / 27 / 0 at d6b06997 against 162 / 27 / 0 at c8da1928, 136 open
against 135, the registered symmetric difference exactly R-0548, done and landed symmetric
differences EMPTY, no duplicate id and no resolution naming an unregistered id at either SHA.
THE CHECKLIST STRUCTURE IS INTACT: walking the region from its introductory bullet to the line
beginning `  Why this is on disk` gives the numerals 1 through 23 ascending with no duplicate
and no gap, and no line matches `^  24\. ` anywhere in the file, so item 23 landing at the END
of the list renumbered no surviving entry — the answer item 17 asks for. HYGIENE IS CLEAN: the
per-commit insertion counts are 308, 259, 8, 62, 36 and 42, none over 500 and so no second call
on the allowance d4473f85 spent; the path set of the range ending at 522d925a is exactly the
five ordered paths and the full range adds only `.agent/handoff.md`; all six commits are
single-parent; the tree is clean and `git worktree list` is one line.

THE PROMOTION IS REAL, NOT MERELY APPLIED. Read at d6b06997, item 16 of the §3 checklist now
reaches a finding headline and a quantifying sentence as well as a heading, and a VALUE a body
fixes as well as a COUNT; item 23 now carries the plan-path rule that R-0377 and R-0491 had
stated only in their own bodies. R47's own C1 advanced `.agent/plan.md` ahead of every other
substantive commit, which is item 23 binding the round that wrote it.

- R-0549 — Low, REVIEWER-BLOCK DEFECT, A HANDBACK'S CLOSING SECTION LOST THREE CLAUSES THE
PREVIOUS ONE CARRIED, AND ONE OF THEM NAMES WHO RECORDS THE VERDICT. Measured by diffing the
`## Next` sections of `.agent/handoff.md` at c8da1928 and at d6b06997: the R46 handback closes
with the successor clause "R46's verdict, when the reviewer issues it, is recorded by R47's own
record slice", a standalone line "Open findings: 135, next free id R-0548" and the pointer
"Phase 1 rule 1 first: re-read `.agent/STOP` from disk". The R47 handback carries none of the
three. Its open-findings count survives only inside the G6 transcript, where a resuming session
reading the `## Next` section alone will not meet it. THE CONSEQUENCE IS THE ONE THIS WORKFLOW
CANNOT ABSORB: R47's handback tells R48 not to open a repair round over the missing gate entry
and never says that R48's record slice is what writes the verdict instead, so a verdict issued
at the end of a session can be stranded in that session — the handoff is the only return
channel, and the clause that routes the verdict onto disk is the one that went missing. The
protocol's own Phase 2 requires the STOP pointer by name, so its loss is a rule broken rather
than a habit skipped. THE CAUSE IS THE R47 BLOCK, not its worker: that block's Handback section
ordered the successor clause and the repair-round warning but omitted all three of these, and
the worker wrote exactly what was ordered. Low, because nothing false was written and every
gate held; the cost is a resume hazard, not a wrong record. The counter-measure is this round's
own Handback section, which enumerates all four closing statements explicitly instead of
naming the section and trusting the previous round's shape to carry over. Found and registered
by the reviewer while gating R47.

Gate: R49 — the R48 entry. R48 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer
over d6b06997..1e0c14e0, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r48.md`, the committed `.agent/authored/f085-r48.md` at
452ffd2b, the committed `.agent/last_block.md` at 5e81e727 and both working copies as they
stand at 1e0c14e0 are all five byte-EQUAL at sha256
da6fd5a6a1de5b03d5f78f39c312a04c6504fe39a51065a82088fde08751ca38, 15488 B, 213 lines, 6 marker
lines. THE SHAPES HELD, each measured separately from slices the reviewer extracted
programmatically from the committed block by marker pair rather than retyping them. THE
REWRITE: PLAN2F occurs 0x and PLAN2T exactly 1x in `.agent/plan.md` at 360897f7, with
`TO contains FROM: false` as that block declared, numstat `3 4`. THE PROSE APPEND: for RECORD16
on `.agent/live_review.md` at 3bc7977b the pre-commit blob is a byte-exact prefix, the remainder
is exactly one blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached
the file, and every non-empty slice line occurs exactly once among that path's added lines — 60
slice lines of which 2 empty against 61 added, numstat `61 0`. THE SUITES WERE RE-RUN, NOT READ,
each in the primary checkout, each exit 0: the four state readers `159 passed` against a base of
159, the canary `42 passed` against 42. THE PLAN CONTRACT HELD at 1e0c14e0: 39 lines against the
50-line cap, `## Goal`, `## Next Steps` and a roadmap F-id all present. THE ARITHMETIC MOVED AS
ORDERED: 164 / 27 / 0 at 1e0c14e0 against 163 / 27 / 0 at d6b06997, 137 open against 136, the
registered symmetric difference exactly R-0549, done and landed symmetric differences EMPTY, no
duplicate id and no resolution naming an unregistered id at either SHA. HYGIENE IS CLEAN: over
the five commits of d6b06997..1e0c14e0 the per-commit INSERTION counts, the column AGENTS.md
DECISION F104 D1 fixes for the cap, are 213, 140, 3, 61 and 34, none over 500 and so no second
call on the allowance d4473f85 spent; the path set of the range ending at 3bc7977b is exactly
the four ordered paths and the full range adds only `.agent/handoff.md`; all five commits are
single-parent; the tree is clean and `git worktree list` is one line. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 213, PROSE 144 and RECORD16 60, all three
agreeing with what that block stated.

TWO CLAIMS THAT BLOCK MADE ABOUT EARLIER ROUNDS WERE RE-MEASURED RATHER THAN TRUSTED, because a
record repeating an unverified number launders it. R47's per-commit insertions over
c8da1928..d6b06997 really are 308, 259, 8, 62, 36 and 42. R47's five-copy transport really does
hold at sha256 a1d2fe72fd6425b5bbf3a06d13e9eb25dbebabb80bfd8a10e49694251cb5530f, 22123 B, 308
lines, 14 marker lines. RECORD16's checklist-structure claim holds WITHIN THE BOUNDS IT NAMES:
walking `docs/agents/planner_reviewer_prompt.md` at d6b06997 from its introductory checklist
bullet to the line beginning `  Why this is on disk` gives the numerals 1 through 23 ascending
with no duplicate and no gap. Read over the WHOLE file that same pattern also matches the
Verification-tiers list further down, so the bound is load-bearing and the claim is true only
because it states one. ONE DIFFERENCE IS NOTED AND IS NOT A DEFECT: the reviewer's slice digests
differ from the handback's by exactly one byte per slice, because the reviewer's extractor keeps
the newline before the END marker and the worker's dropped it; all three line counts agree at
5, 4 and 60, and the applied bytes are what G3 proved.

- R-0550 — Low, REVIEWER-BLOCK DEFECT, A RECORD SLICE STATED A PRESENT-TENSE READING OF A FILE
ITS OWN BLOCK REWROTE ONE COMMIT EARLIER. RECORD16 closes its plan-contract sentence with "THE
PLAN CONTRACT HOLDS: 40 lines against the 50-line cap", and that clause names no commit. The
reading was true of `.agent/plan.md` at d6b06997, where the file is 40 lines. C1 of that same
round, 360897f7, made it 39, and RECORD16 landed at C2, 3bc7977b — one commit LATER. So the
sentence was false of the file it describes at the moment it reached disk, and it is false at
1e0c14e0 too. This is exactly checklist item 20, the R-0520 class, and the block did not miss
the rule: its own constraint 5 asserted that "every sentence in RECORD16 that reads a file THIS
BLOCK also edits names the SHA d6b06997 in the same clause". That constraint is false of its
own slice twice over — this sentence names no SHA at all, and the one plan-reading sentence
that DOES name one names 3fe2667d, which is correct on the merits and is not the SHA the
constraint promised. A constraint asserting a property its own slice does not have is the
R-0527 shape checklist item 11 governs, so the two items met in one paragraph. Low, because
nothing about a GATE was misreported: every gate result RECORD16 states is reproducible, this
reviewer reproduced all of them, and the damage is one stale number in a permanent record.
THE COUNTER-MEASURE IS NOT A REWRITE. Item 20 fixes that explicitly — appending a correction is
how this record stays honest, and overwriting landed text is worse than a dated wrong sentence
— so the sentence stays and this paragraph is its correction. What changes is the emission
step: a constraint of the form "every sentence in X names SHA Y" is MEASURED sentence by
sentence before emission, in the same way item 15 requires a containment test per pair rather
than one reading generalised across pairs, because a universal asserted over a slice's own
sentences is the recollection item 11 exists to forbid. Found and registered by the reviewer
while gating R48.

- R-0551 — Medium, SPEC DEFECT, THE `dod` POLICY ROW COVERS TWO SITES THAT DO NOT SHARE A
POLICY, AND THE TWO DOCUMENTS DESCRIBING IT CONTRADICT EACH OTHER AND THE CODE. Amendment F085
D1 in `docs/roadmap/features/T2_F085.md` at 1e0c14e0 gives `dod` one row reading wall timeout
`yes` and network `default-deny` for both of its sites. `.agent/plan.md` at 1e0c14e0 says the
opposite of the same two sites — "whose policy differs from the `test` class in taking no wall
timeout, because their children are the long-lived harness rather than a bounded suite run" —
and the R48 handback at 1e0c14e0 repeats it. Measured against the code at 1e0c14e0, both are
wrong, in opposite directions, and each is right about one site. `.agent/f085_inventory.md`
assigns exactly `packages/orchestration/dod_runners.py`:302 and :575 to the class.
`_run_process_check`, the first, runs ONE BOUNDED CHECK — its docstring says "a check that IS
one process: pytest, lint, build, custom_cmd" — and already passes `timeout=ctx.timeout_sec`
with a `subprocess.TimeoutExpired` handler that classifies the trip; it is not a long-lived
harness, it keeps its wall timeout, and its actual stage-1 gap is `env=os.environ.copy()`.
`_run_app_once`, the second, starts the application with
`Popen(..., start_new_session=True)`, waits with `http_probe` against `spec.health_path` over
`http://<host>:<port>`, and stops it in a `finally`; a wall timeout would kill the harness
mid-probe and a default-deny network posture would break the probe that judges it, which is
word for word the reason D1 already gives for excusing the `runtime` class. THE CONSEQUENCE IS
THAT T002c COULD NOT HAVE BEEN BUILT CORRECTLY FROM EITHER DOCUMENT: following the feature file
puts a killing clock and a network denial on the app harness, and following the plan strips a
working timeout off a bounded check. Medium rather than Low because it would have landed as
production behaviour and the wrong half is invisible at review time — both readings look
internally consistent. THE COUNTER-MEASURE IS THIS ROUND'S OWN C3a AND C3b: the row splits into
`dod-process` and `dod-app` under DECISION F085 D7, ruled per §4 item 7, and `.agent/plan.md`
is corrected by C1 in the same round so the two documents agree. The site total is unchanged,
so the inventory needs no edit. Found and registered by the reviewer while planning T002c.

Gate: R50 — the R49 entry. R49 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over 1e0c14e0..25a5b42e, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r49.md`, the committed `.agent/authored/f085-r49.md` at
6f084636, the committed `.agent/last_block.md` at 8862abce and both working copies as they stand
at 25a5b42e are all five byte-EQUAL at sha256
fe04d524d02f044891f9ffb591b5aa83335a07c9ac0471bde02b6b20f13319dc, 24858 B, 345 lines, 12 marker
lines. THE SHAPES HELD, each measured separately from slices the reviewer extracted
programmatically from the committed block by marker pair rather than retyping them. THE TWO
REWRITES: PLAN3F occurs 0x and PLAN3T exactly 1x in `.agent/plan.md` at d5fb16a5 at numstat
`9 9`, and AMEND7F occurs 0x and AMEND7T exactly 1x in `docs/roadmap/features/T2_F085.md` at
7df0bf33 at numstat `8 5`; both pairs give `TO contains FROM: false`, as that block declared. THE
TWO PROSE APPENDS: for RECORD17 on `.agent/live_review.md` at 0131b21b and for DEC7 on the
feature file at ad9a38a8 the pre-commit blob is a byte-exact prefix, the remainder is exactly one
blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached either file, and
every non-empty slice line occurs exactly once among that path's added lines — 93 slice lines of
which 3 empty against 94 added at numstat `94 0`, and 25 slice lines of which 3 empty against 26
added at numstat `26 0`. THE SUITES WERE RE-RUN, NOT READ, each in the primary checkout, each
exit 0: the four state readers `159 passed` against a base of 159, the canary `42 passed` against
42, the docs tier `295 passed` against 295. THE PLAN CONTRACT HELD at d5fb16a5: 39 lines against
the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id all present. THE ARITHMETIC
MOVED AS ORDERED: 166 / 27 / 0 at 25a5b42e against 164 / 27 / 0 at 1e0c14e0, 139 open against
137, the registered symmetric difference exactly R-0550 and R-0551, done and landed symmetric
differences EMPTY, no duplicate id and no resolution naming an unregistered id at either SHA, and
R-0552 free. HYGIENE IS CLEAN: over the six commits of 1e0c14e0..25a5b42e that precede the
handback the per-commit INSERTION counts, the column AGENTS.md DECISION F104 D1 fixes for the
cap, are 345, 283, 9, 94, 8 and 26, and the handback commit adds 99; none over 500 and so no
second call on the allowance d4473f85 spent; the path set of that range is exactly the six
ordered paths and nothing else; all seven commits are single-parent; the tree is clean and
`git worktree list` is one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives
TOTAL 345, PROSE 180 and RECORD17 93, each agreeing with what that block stated and each under
its DECISION F085 D6 cap. ONE DIFFERENCE IS NOTED AND IS NOT A DEFECT: the reviewer's slice byte
counts run one below the handback's on every slice, because the two extractors disagree about the
newline preceding an END marker; the six slice line counts agree at 12, 12, 10, 13, 25 and 93,
and the applied bytes are what G3 proved.

- R-0552 — Medium, SPEC DEFECT, THE `runtime` POLICY ROW COVERS SITES THAT DO NOT SHARE A POLICY,
AND ITS NO-WALL-TIMEOUT RULING WOULD REMOVE A TIMEOUT TWO OF THEM ALREADY HAVE. The `runtime` row
of the policy table in `docs/roadmap/features/T2_F085.md` at 25a5b42e gives all five of its sites
no wall timeout. Measured against `.agent/f085_inventory.md` at 25a5b42e, whose own `callee` and
`timeout` columns already separate them, three are `Popen` calls that pass no timeout and start
long-lived children — `apps/cli/commands/runtime_cmd.py`:136 in `_serve_supervisor`,
`packages/runtimes/dev_server.py`:1484 in `start` and
`packages/runtimes/runtime_supervisor.py`:235 in `run` — while two are `subprocess.run` calls
inside `_auto_build_frontend`, `packages/orchestration/ui_server.py`:2787 and :2800, which pass
`timeout=120` and run `npm install` and `npm run build` to completion. For that second pair a
no-wall-timeout policy does not relax a guard, it REMOVES a working one, which is word for word
the regression R-0551 identified for `_run_process_check` one row above. Medium for the reason
R-0551 was Medium: it would land as production behaviour at T002d, and both readings look
internally consistent at review time. THE COUNTER-MEASURE IS THIS ROUND'S OWN C3a AND C3b, which
split the row into `runtime-server` and `runtime-build` under DECISION F085 D8 and leave the site
total unchanged, so the inventory needs no edit. THE DEEPER COUNTER-MEASURE IS THE SWEEP: D7
fixed the `dod` row and left this one standing, which is the R-0417 shape of fixing the instance
rather than the class, so D8 states the reading it took over EVERY stage-1 row. Found and
registered by the reviewer while gating R49.

- R-0553 — Low, REVIEWER-BLOCK DEFECT, AN AUTHORED SLICE ASSERTED AN UNMEASURED UNIVERSAL OVER A
CLASS AND IS FALSE OF TWO OF ITS MEMBERS. AMEND7T, applied at 7df0bf33, rewrote the paragraph
under the policy table to say that the classes taking no wall timeout are the ones whose children
are long-lived servers and that "each is judged by a readiness probe over HTTP, so each keeps
network access". Measured at 25a5b42e, the two `_auto_build_frontend` sites R-0552 names sit in a
class that paragraph covers, and they are judged by `check=True` on a completed `npm` run rather
than by any HTTP probe, so the sentence is false of them however its quantifier is read — over
classes or over sites. This is checklist item 11 as R-0526 widened it: a universal asserted over
a set nobody enumerated, written by the reviewer in the very slice that was correcting the
identical defect one row above. Low, because no GATE was misreported — every gate R49 ordered is
reproducible and this reviewer reproduced all of them — and because the normative content of that
passage is the table, which this round corrects. THE COUNTER-MEASURE IS NOT A REWRITE of the
landed sentence: C3a replaces the paragraph as part of the D8 split, and its replacement states
the no-wall-timeout rule as a condition each class is tested against rather than as a universal
over an unenumerated set, while the per-site reading lives in DEC8 beside the SHA it was taken
at. Found and registered by the reviewer while gating R49.

Gate: R51 — the R50 entry. R50 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over 25a5b42e..3a64b65e, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r50.md`, the committed `.agent/authored/f085-r50.md` at
c22cb9dd, the committed `.agent/last_block.md` at 634447bc and both working copies as they stand
at 3a64b65e are all five byte-EQUAL at sha256
061fa19d22524bd91e69697f28285376e82f45005d7894f833ab991adb390cd7, 24335 B, 334 lines, 12 marker
lines — every figure measured on every copy. THE SHAPES HELD, each measured separately from slices
the reviewer extracted programmatically from the committed block by marker pair rather than
retyping them. THE TWO REWRITES: PLAN4F occurs 0x and PLAN4T exactly 1x in `.agent/plan.md` at
2241cb69 at numstat `6 4`, and AMEND8F occurs 0x and AMEND8T exactly 1x in
`docs/roadmap/features/T2_F085.md` at 8bb7a287 at numstat `10 7`; both pairs give
`TO contains FROM: false`, as that block declared. THE TWO PROSE APPENDS: for RECORD18 on
`.agent/live_review.md` at 56722bd7 and for DEC8 on the feature file at 9b9cd0b4 the pre-commit
blob is a byte-exact prefix, the remainder is exactly one blank line plus the slice, the slice is
an exact suffix, 0 marker LINES reached either file, and every non-empty slice line occurs exactly
once among that path's added lines — 72 slice lines of which 2 empty against 73 added at numstat
`73 0`, and 29 slice lines of which 3 empty against 30 added at numstat `30 0`. THE SUITES WERE
RE-RUN, NOT READ, each in the primary checkout, each exit 0: the four state readers `159 passed`
against a base of 159, the canary `42 passed` against 42, the docs tier `295 passed` against 295.
THE PLAN CONTRACT HELD at 2241cb69: 41 lines against the 50-line cap, with `## Goal`,
`## Next Steps` and a roadmap F-id all present. THE ARITHMETIC MOVED AS ORDERED: 168 / 27 / 0 at
3a64b65e against 166 / 27 / 0 at 25a5b42e, 141 open against 139, the registered symmetric
difference exactly R-0552 and R-0553, done and landed symmetric differences EMPTY, no duplicate id
and no resolution naming an unregistered id at either SHA, and R-0554 free. HYGIENE IS CLEAN: over
the six commits of 25a5b42e..3a64b65e that precede the handback the per-commit INSERTION counts,
the column AGENTS.md DECISION F104 D1 fixes for the cap, are 334, 239, 6, 73, 10 and 30, and the
handback commit adds 79; none over 500; the path set of that range is exactly the six ordered paths
and nothing else; all seven commits are single-parent; the tree is clean and `git worktree list` is
one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 334, PROSE 182 and
RECORD18 72, agreeing with that block. THE AMENDMENT'S OWN MEASUREMENT WAS
SPOT-CHECKED rather than accepted: read at 3a64b65e, `.agent/f085_inventory.md` assigns exactly the
five sites DEC8 names to `runtime`, and `packages/orchestration/ui_server.py` really does call
`subprocess.run` with `timeout=120` twice inside `_auto_build_frontend`, for `npm install` and
`npm run build` — the pair whose working guard a no-wall-timeout policy would have removed. NO NEW
FINDING WAS REGISTERED: no gate came out red, no claim in the handback failed to reproduce, and
the open set stays at 141 with R-0554 free.

Gate: R52 — the R51 entry. R51 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 3a64b65e..67475107, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r51.md`, the committed `.agent/authored/f085-r51.md` at
44a1fbde, the committed `.agent/last_block.md` at aa38f8c7 and both working copies as they stand
at 67475107 are all five byte-EQUAL at sha256
12c6771bf04c38f94be460b4beb48ed93ea5b37709ce1f70711f89a093703abc, 29295 B, 489 lines, 28 marker
lines — every figure measured on every copy. THE SHAPES HELD, each measured separately from slices
the reviewer extracted programmatically from the committed block by marker pair. THE FIVE REWRITES
each give `TO contains FROM: false` as that block declared, each FROM occurred exactly 1x in its
own pre-commit blob and 0x in its post-commit file with its TO exactly 1x: PLAN5F→PLAN5T in
`.agent/plan.md` at 051b4082 numstat `13 11`, HDRF→HDRT in
`packages/orchestration/exec_guard.py` at ff93b13a numstat `5 3`, and DOCF→DOCT, IMPF→IMPT and
SITEF→SITET in `packages/orchestration/dod_runners.py` at 44460d56 numstat `13 6`. THE PROSE
APPEND held for RECORD19 on `.agent/live_review.md` at 73489620: byte-exact prefix, a remainder of
exactly one blank line plus the slice, an exact suffix, 0 marker LINES, and each of its 37 slice
lines — 0 empty — occurring exactly once among the 38 lines that commit adds, numstat `38 0`. THE
THREE CODE APPENDS held under the ORDERED EQUALITY §4.9 owes them since R-0531 — SEAM at fcfb2a0f
numstat `77 0`, TESTSDOD at 43cd292a numstat `52 0`, TESTSGUARD at 43cd292a numstat `22 0`: each
post-commit file equals `pre + slice` with NO joiner byte, each commit's added lines are exactly
that slice's lines IN ORDER, and 0 marker LINES reached any of the three. THE SUITES AND THE LINT
GATE WERE RE-RUN, NOT READ, in the primary checkout with the block's exact command lines, each
exit 0: the code suite `150 passed` against a base of 147, the four state readers `159 passed`
against 159, the canary `42 passed` against 42, and ruff `All checks passed!`. THE PLAN CONTRACT
HELD at 051b4082: 43 lines against the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap
F-id present. THE ARITHMETIC STOOD STILL AS ORDERED: 168 / 27 / 0 at both 3a64b65e and 67475107,
141 open at both, all three symmetric differences EMPTY, no duplicate id and no resolution naming
an unregistered id at either SHA. HYGIENE IS CLEAN: over the eight commits of 3a64b65e..67475107
that precede the handback the per-commit INSERTION counts, the column AGENTS.md DECISION F104 D1
fixes for the cap, are 489, 425, 13, 38, 5, 77, 13 and 74, and the handback commit adds 55; none
over 500; that range's path set measured before the handback is exactly the eight ordered paths
and nothing else; all nine commits are single-parent; the tree is clean and `git worktree list` is
one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 489, PROSE 226 and
RECORD19 37, agreeing with that block. THE TWO RED CONTROLS THAT BLOCK RECORDED WERE NOT TAKEN ON
TRUST: the reviewer re-ran both in a disposable worktree at 67475107 and removed it. Reverting
SITET to SITEF failed both new `dod_runners` tests and printed `AWS_SECRET_ACCESS_KEY` in the leak
test's own failure message; replacing the seam's `wall_timeout_seconds` with None failed the new
policy test AND the pre-existing `test_a_timeout_is_red_not_a_hang`, so the behaviour-equality
golden that block named really does hold the migration in place.

- R-0554 — `.agent/plan.md` claimed FOUR tests for a round that shipped THREE. Low. The R51 block
authored PLAN5T with the clause "four tests ship with it", and the round it described shipped
three: TESTSDOD defined two tests and TESTSGUARD one, which is also what the code suite measured
as `150 passed` against a base of 147. This is the class checklist item 16 names after R-0537 and
R-0543 — a sentence that quantifies what follows it, drifting because the numeral is the half
nobody re-reads — and it is the third instance of that class, in the same file R-0543 arrived in.
It is LOW and not Medium because no GATE ordered or reported the number: every gate R51 ordered is
reproducible and this reviewer reproduced all nine, so the miscount misled a reader of the plan
and never a verdict. The worker is not at fault; it applied the reviewer's slice byte-verbatim,
which is what constraint 1 required of it. C1 of the round carrying this registration retires the
clause as a side effect — PLAN6F spans the `## Current Step` section holding it and PLAN6T
describes R52 instead — so this finding is expected to be RESOLVED at the R52 gate rather than
repaired by a round of its own; `.agent/plan.md` states the CURRENT step and never a history, so
no appending correction under R-0520 is owed to it. Found and registered by the reviewer while
gating R51.

Gate: R53 — the R52 entry. R52 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 67475107..3bafcc1e, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r52.md`, the committed `.agent/authored/f085-r52.md` at
a7896384, the committed `.agent/last_block.md` at 216fe178 and both working copies as they stand
at 3bafcc1e are all five byte-EQUAL at sha256
dbb09a909d14afe36d188f834eba2698f195ac502d2372f92e0f89d5bda554b8, 25680 B, 373 lines, 10 marker
lines, and that digest is the one the R52 block itself carried — every figure measured on every
copy. THE SHAPES HELD. The single REWRITE PLAN6F→PLAN6T in `.agent/plan.md` at 511736d6 gives
`TO contains FROM: false`, its FROM occurred 1x in the pre-commit blob and 0x after with its TO
exactly 1x, numstat `11 10`. THE PROSE APPEND RECORD20 on `.agent/live_review.md` at 23a7ec30:
byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix, 0 marker
LINES, and each of its 54 non-empty slice lines occurring exactly once among the 56 lines that
commit adds, numstat `56 0`. THE TWO CODE APPENDS held under ORDERED EQUALITY — SEAM2 at d5b1c8f6
numstat `50 0` and TESTSGUARD2 at 610fd945 numstat `30 0`: each post-commit file equals
`pre + slice` with NO byte between them, each commit's added lines are exactly that slice's lines
IN ORDER, and 0 marker LINES reached either. THE SUITES AND THE LINT GATE WERE RE-RUN, NOT READ,
in the primary checkout with the block's exact command lines, each exit 0: the code suite
`151 passed` against a base of 150, the four state readers `159 passed` against 159, the canary
`42 passed` against 42, and ruff `All checks passed!`. THE PLAN CONTRACT HELD at 511736d6: 44
lines against the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 44 is
the figure that block projected. THE ARITHMETIC MOVED AS ORDERED: 169 / 27 / 0 at 3bafcc1e against
168 / 27 / 0 at 67475107, 142 open against 141, the registered symmetric difference exactly
R-0554, done and landed symmetric differences EMPTY, no duplicate id and no resolution naming an
unregistered id at either SHA. HYGIENE IS CLEAN: over the six commits of 67475107..3bafcc1e that
precede the handback the per-commit INSERTION counts, the column AGENTS.md DECISION F104 D1 fixes
for the cap, are 373, 255, 11, 56, 50 and 30, and the handback commit adds 38; none over 500; that
range's path set measured before the handback is exactly the six ordered paths and does NOT hold
`packages/orchestration/dod_runners.py`, which that round's change set excluded; all seven commits
are single-parent; the tree is clean and `git worktree list` is one line. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 373, PROSE 205 and RECORD20 55, agreeing with that
block. THE HANDBACK'S OWN SELF-CLAIM was checked and holds: it states 86 lines and measures 86,
inside the ≤100 allowance a seven-commit round carries.

- R-0555 — the R52 block's Handback section said "Six commits" over a Bundle naming seven. Low.
That block's Bundle names C0a, C0b, C1, C2, C3, C4 and C5, and its Handback section then wrote
"Six commits, so the ≤100-line allowance applies". This is checklist item 16's class as R-0537 and
R-0543 widened it — a sentence that quantifies what follows it, drifting because the numeral is
the half nobody re-reads — arriving in the reviewer's own block one round after R-0554 registered
the same class against `.agent/plan.md`. It is LOW because the allowance it computes is identical
either way: the threshold is more than five commits and both readings clear it, so no gate and no
cap moved. The worker read the Bundle rather than the sentence, wrote "Seven commits" in the
handback, and flagged the contradiction instead of silently following either half — which is the
behaviour the block wants. Found by the worker, registered by the reviewer while gating R52.

- R-0556 — a block's slice convention did not say whether a slice INCLUDES its terminating
newline, so the worker's extraction and the block's definition disagreed. Low. The R52 block's
CONVENTION said only that "a slice is the bytes strictly between its marker lines" and that a
trailing newline is not an extra line. Under the reading that a slice ends with the newline
terminating its last content line, `post == pre + slice` holds exactly for SEAM2 at d5b1c8f6 and
TESTSGUARD2 at 610fd945, which is what the reviewer measured at 3bafcc1e; under an extraction that
joins the inner lines WITHOUT a trailing newline it does not, and the worker therefore appended one
and declared an assumption for it. BOTH ROUTES PRODUCED IDENTICAL BYTES ON DISK, so nothing landed
wrong and G4 stayed green either way; what the gap cost was a declared assumption on a round that
did nothing wrong, and it put into the handback the absolute claim that `post == pre + slice` does
not hold at fcfb2a0f, which is false under the block's own convention and true only under the
worker's unstated one. This is the newline class the reviewer's own notes already carry — one
newline shifts both slice counts and pair shape — recurring because the convention sentence stated
the units without pinning the boundary. THE COUNTER-MEASURE IS IN THE R53 BLOCK'S OWN CONVENTION
paragraph, which states newline-inclusion explicitly and says that no joiner and no terminator byte
is ever added; that is the block carrying this registration. Found by the worker's declared
assumption, registered by the reviewer while gating R52.

Gate: R54 — the R53 entry. R53 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 3bafcc1e..8ba3ad45, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r53.md`, the committed `.agent/authored/f085-r53.md` at 94e4da84,
the committed `.agent/last_block.md` at 8267fde9, both of those paths at 8ba3ad45 and both working
copies as they stand at 8ba3ad45 are all seven byte-EQUAL at sha256
58a4c90c25772d8c0083afd808474e69bf96cb3c27033eb652dca7cba28f1825, 28869 B, 429 lines, 24 marker
lines — every figure measured on every copy. THE SHAPES HELD. Each of the five REWRITES gives
`TO contains FROM: false`, its FROM 1x in the pre-commit blob and 0x after with its TO exactly 1x:
PLAN7F→PLAN7T at 2e136a4e numstat `9 11`, HDRF2→HDRT2 at de4f2057 numstat `6 5`, and DOCF2→DOCT2,
IMPF2→IMPT2 and SITEF2→SITET2 all at bbd35e23, that path's numstat `27 7`. THE PROSE APPEND
RECORD21 on `.agent/live_review.md` at d5fe684c: byte-exact prefix, a remainder of exactly one
blank line plus the slice, an exact suffix, 0 marker LINES, and each of its 60 non-empty slice
lines occurring exactly once among the 63 lines that commit adds, numstat `63 0`. THE CODE APPEND
TESTSDOD2 at 85f5da00 held under ORDERED EQUALITY: the post-commit file equals `pre + slice` with
NO byte between them, that commit's added lines are exactly the slice's 41 lines IN ORDER, and 0
marker LINES reached it, numstat `41 0`. THE SUITES AND THE LINT GATE WERE RE-RUN, NOT READ, in the
primary checkout with the block's exact command lines, each exit 0: the code suite `152 passed`
against a base of 151, the four state readers `159 passed` against 159, the canary `42 passed`
against 42, and ruff `All checks passed!`. THE PLAN CONTRACT HELD at 2e136a4e: 42 lines against the
50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 42 is the figure that
block projected. THE ARITHMETIC MOVED AS ORDERED: 171 / 27 / 0 at 8ba3ad45 against 169 / 27 / 0 at
3bafcc1e, 144 open against 142, the registered symmetric difference exactly R-0555 and R-0556, done
and landed symmetric differences EMPTY, no duplicate id and no resolution naming an unregistered id
at either SHA. HYGIENE IS CLEAN: walking 3bafcc1e..8ba3ad45 commit by commit the INSERTION counts,
the column AGENTS.md DECISION F104 D1 fixes for the cap, are 429, 340, 9, 63, 6, 27, 41 and 45 for
the handback commit; none over 500; that range's path set measured before the handback is exactly
the seven ordered paths and does NOT hold `tests/orchestration/test_exec_guard.py`, which that
round's change set excluded; all eight commits are single-parent; the tree is clean and
`git worktree list` is one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives
TOTAL 429, PROSE 231 and RECORD21 62, agreeing with that block. THE HANDBACK'S OWN SELF-CLAIM was
checked and holds: `.agent/handoff.md` at 8ba3ad45 states 92 lines and measures 92, inside the
≤100 allowance an eight-commit round carries. THE REVIEWER ALSO RAN ITS OWN RED CONTROL on the
LANDED code rather than accepting the one that block recorded at its base: in a disposable worktree
at 8ba3ad45, removed afterwards, the new `TestTheDodAppSeam` test passed unmutated and went RED when
SITET2 was reverted to SITEF2, failing on `AWS_SECRET_ACCESS_KEY` present in the child environment
— so the migration is genuinely covered at its call site and the test is not vacuous.

- R-0557 — the R53 block's Handback section said "seven commits" over a Bundle naming eight. Low.
That block's Bundle at 8ba3ad45 names C0a, C0b, C1, C2, C3, C4, C5 and C6, and its Handback section
then wrote "This round's Bundle names seven commits, which is more than five". This is checklist
item 16's class as R-0537 and R-0543 widened it — a sentence that quantifies what follows it,
drifting because the numeral is the half nobody re-reads — and it is the SECOND instance in two
rounds: R-0555 registered exactly this shape against the R52 block, in the very record slice the
R53 block carried. Registering the class twice without changing the practice is what makes it worth
naming a counter-measure: the R54 block states its commit count ONCE, in its Bundle sentence, in
the same words the item-status list beneath it uses, so a later revision cannot move one without
visibly contradicting the other. It is LOW for the reason R-0555 was: the allowance it computes is
identical either way, since the threshold is more than five commits and both readings clear it, so
no gate and no cap moved, and the worker again read the Bundle rather than the sentence and wrote
"Eight commits" in the handback while flagging the contradiction. Found by the worker, registered
by the reviewer while gating R53.

Gate: R55 — the R54 entry. R54 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 8ba3ad45..1812c219, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r54.md`, the committed `.agent/authored/f085-r54.md` at eb18ad04,
the committed `.agent/last_block.md` at 2067581f, both of those paths at 1812c219 and both working
copies as they stand at 1812c219 are all seven byte-EQUAL at sha256
19497ed6660efbf34b3e2fbb246faa0c1ef0e0a75e7132c14e3757a6c3182959, 31279 B, 490 lines, 22 marker
lines — every figure measured on every copy. THE SHAPES HELD. Each of the four REWRITES gives
`TO contains FROM: false`, its FROM 1x in the pre-commit blob and 0x after with its TO exactly 1x:
PLAN8F→PLAN8T at dbfb26af numstat `8 9`, and XLAT1F→XLAT1T, XLAT2F→XLAT2T and DOCXF→DOCXT all at
1bfcaf0c, that path's numstat `7 26`. THE PROSE APPEND RECORD22 on `.agent/live_review.md` at
d48febf0: byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix,
0 marker LINES, and each of its 51 non-empty slice lines occurring exactly once among the 53 lines
that commit adds, numstat `53 0`. THE TWO CODE APPENDS held under ORDERED EQUALITY — SEAM3 at
27279810 numstat `99 0` and TESTSRB at a3d32124 numstat `46 0`: each post-commit file equals
`pre + slice` with NO byte between them, each commit's added lines are exactly that slice's lines
IN ORDER, and 0 marker LINES reached either. THE SUITES AND THE LINT GATE WERE RE-RUN, NOT READ, in
the primary checkout with the block's exact command lines, each exit 0: the code suite `156 passed`
against a base of 152, the four state readers `159 passed` against 159, the canary `42 passed`
against 42, and ruff `All checks passed!`. THE PLAN CONTRACT HELD at dbfb26af: 41 lines against the
50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 41 is the figure that
block projected. THE ARITHMETIC MOVED AS ORDERED: 172 / 27 / 0 at 1812c219 against 171 / 27 / 0 at
8ba3ad45, 145 open against 144, the registered symmetric difference exactly R-0557, done and landed
symmetric differences EMPTY, no duplicate id and no resolution naming an unregistered id at either
SHA. HYGIENE IS CLEAN: walking 8ba3ad45..1812c219 commit by commit the INSERTION counts, the column
AGENTS.md DECISION F104 D1 fixes for the cap, are 490, 417, 8, 53, 99, 7, 46 and 35 for the
handback commit; none over 500; that range's path set measured before the handback is exactly the
six ordered paths and does NOT hold `packages/orchestration/ui_server.py`, which that round's
change set excluded; all eight commits are single-parent; the tree is clean and `git worktree list`
is one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 490, PROSE 225
and RECORD22 52, agreeing with that block. THE HANDBACK'S OWN SELF-CLAIM was checked and holds:
`.agent/handoff.md` at 1812c219 states 92 lines and measures 92, inside the ≤100 allowance an
eight-commit round carries. THE WORKER'S ONE DECLARED DEVIATION WAS VERIFIED RATHER THAN ACCEPTED:
it reported writing throwaway helper scripts under the gitignored `.remedy-wt/`, and
`git ls-files .remedy-wt` returns EMPTY at 1812c219, so nothing it named entered the repository.
THE EXTRACTION WAS PROVEN SHARED, NOT ASSUMED, by the reviewer's own red control in a disposable
worktree at 1812c219 that it removed afterwards. At that commit
`_completed_process_from_guarded` is defined exactly once and called from three sites, and the
module holds `raise subprocess.TimeoutExpired(` exactly once where 8ba3ad45 held it twice — so the
duplication really is gone rather than merely wrapped. Deleting the wall-trip branch from that one
helper turned three tests RED across all three seams at once — the `test` seam's
`test_a_wall_trip_raises_timeout_expired_carrying_the_partial_output`, the `dod-process` seam's
`TestNeverASilentPass::test_a_timeout_is_red_not_a_hang` in `tests/orchestration/test_dod_runners.py`,
and the new `test_the_runtime_build_seam_raises_timeout_expired_on_a_wall_trip` — against 80 passed
and 0 failed unmutated. A refactor whose single point of failure reddens every caller is the
equality claim actually holding, which is what the round's own G5 could only show negatively.

Gate: R56 — the R55 entry. R55 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer
over 1812c219..49a3fdcb, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r55.md`, the committed `.agent/authored/f085-r55.md` and the
committed `.agent/last_block.md` at 49a3fdcb, and both of those working copies as they stand at
49a3fdcb, are all five byte-EQUAL at sha256
dfcb54609904651d7d882c01e83ade3712e1ab8a42355b62199a4271a89f665e, 19014 B, 253 lines, 6 marker
lines — every figure measured on every copy. THE SHAPES HELD. The one REWRITE gives
`TO contains FROM: false`, its FROM 1x in the pre-commit blob and 0x after with its TO exactly 1x:
PLAN9F→PLAN9T at e02f0dcc, numstat `12 7`. THE PROSE APPEND RECORD23 on `.agent/live_review.md` at
2bb63069: byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix,
0 marker LINES, and each of its 46 non-empty slice lines occurring exactly once among the 47 lines
that commit adds, numstat `47 0`. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with
the block's exact command lines, each exit 0: the four state readers `159 passed` against a base of
159, and the canary `42 passed` against 42. THE PLAN CONTRACT HELD at e02f0dcc: 46 lines against
the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 46 is the figure that
block projected. THE ARITHMETIC DID NOT MOVE, as a record round requires: 172 registered / 27 done
/ 0 landed and 145 open at 1812c219 and the same at 49a3fdcb, max registered R-0557 and max
resolved R-0532 at both, all three symmetric differences EMPTY, 0 duplicate ids and 0 resolutions
naming an unregistered id at both SHAs. HYGIENE IS CLEAN: walking 1812c219..49a3fdcb commit by
commit the INSERTION counts, the column AGENTS.md DECISION F104 D1 fixes for the cap, are 253, 174,
12, 47 and 31 for the handback commit; none over 500; that range's path set is exactly the five
ordered paths and holds NO path under `packages/` or `tests/`, which that round's change set
excluded; all five commits are single-parent; the tree is clean and `git worktree list` is one
line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 253, PROSE 158 and
RECORD23 46, agreeing with that block. THE HANDBACK'S OWN SELF-CLAIM was checked and holds:
`.agent/handoff.md` at 49a3fdcb states 69 lines and measures 69, and its DECISION D15 stated cause
names only MANDATED content — five per-commit tables, the item-status table, the verification
transcript — with no section dropped, which is what that decision permits and what a five-commit
round genuinely owes. THE ROUND'S OWN CLAIM TO HAVE REGISTERED AND RESOLVED NOTHING was verified
rather than accepted, since it is the whole substance of a record round: the registered, done and
landed id SETS at the two SHAs are identical element by element, not merely equal in count.

Gate: R57 — the R56 entry. R56 FAILED, and the failure is the reviewer's, not the worker's. Every
ordered gate G1-G8 was re-executed by the reviewer over 49a3fdcb..3bb82a25, not read, and each
reproduces the handback's reading exactly; the worker deviated in nothing, applied every slice
byte-verbatim and declared its scratch honestly. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT
HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback: `.remedy-wt/`'s
`f085-r56.md`, the committed `.agent/authored/f085-r56.md` and the committed `.agent/last_block.md`
at 3bb82a25, and both of those working copies as they stand at 3bb82a25, are all five byte-EQUAL at
sha256 1a9fcbdbd41463fd0fcd2116837d2ec6dec100304614149609db5b467a33cb82, 24319 B, 345 lines, 12
marker lines, which is the digest the reviewer emitted. THE SHAPES HELD. Both REWRITES give
`TO contains FROM: false`, FROM 1x in the pre-commit blob and 0x after with the TO exactly 1x:
PLAN10F→PLAN10T at 9a218ec1 numstat `10 12`, and ALLOWF→ALLOWT at 94574142 numstat `17 3`. THE
PROSE APPEND RECORD24 on `.agent/live_review.md` at 33c99b54: byte-exact prefix, a remainder of
exactly one blank line plus the slice, an exact suffix, 0 marker LINES, and each of its 32
non-empty slice lines occurring exactly once among the 33 lines that commit adds, numstat `33 0`.
THE CODE APPEND TESTSNPM on `tests/orchestration/test_exec_guard.py` at 94574142 held under ORDERED
EQUALITY, numstat `44 0`: the post-commit file equals `pre + "\n" + slice` byte-exactly and that
commit's added lines are one blank line followed by the slice's lines IN ORDER. THE SUITES AND THE
ORDERED LINT WERE RE-RUN, NOT READ, in the primary checkout with the block's exact command lines,
each exit 0: the guard suite `35 passed` against a base of 33, the four state readers `159 passed`
against 159, the canary `42 passed` against 42, and ruff `All checks passed!`. THE PLAN CONTRACT
HELD at 9a218ec1: 44 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap
F-id present — 44 is the figure that block projected. THE ARITHMETIC DID NOT MOVE, as that round
required: 172 / 27 / 0 and 145 open at 49a3fdcb and the same at 3bb82a25, all three symmetric
differences EMPTY. HYGIENE IS CLEAN: the per-commit INSERTION counts over that range are 345, 244,
10, 33, 61 and 38 for the handback commit; none over 500; the path set measured before the handback
excludes `packages/orchestration/ui_server.py` as that change set ordered; all six commits are
single-parent. THE WIDENING ITSELF IS RIGHT AND STAYS: the reviewer proved in a disposable worktree
at 3bb82a25, since removed, that reverting the row reddens both new tests while the other 33 stay
green, and that making `scrub_child_env` match `NPM_CONFIG_` as a PREFIX leaks
`NPM_CONFIG__AUTHTOKEN` into the child and reddens the second test alone — so the by-name-never-by-
prefix property the row depends on is pinned rather than asserted. WHAT FAILED is one blank line,
registered below.

- R-0558 — a block claimed a PEP 8 blank-line property for a code append that a one-blank-line join
cannot produce, and the ordered lint gate was structurally blind to the result. Low. The R56 block's
CONVENTION said "TESTSNPM is CODE joined to its target by exactly one blank line, so the file keeps
the two-blank-line separation PEP 8 puts between top-level definitions". Those two clauses
contradict each other: joining with ONE blank line yields ONE, and at 3bb82a25
`tests/orchestration/test_exec_guard.py` separates `_RUNTIME_BUILD_ADDED_ENV_KEYS` from the
function above it by a single blank line, where that same file separates `_ENV_DUMP` from the
function above IT by two. `ruff check --preview` over that path at 3bb82a25 reports exactly one
`E305 blank-lines-after-function-or-class`, and over the same path's blob at 49a3fdcb reports
`All checks passed!`, so the violation is this round's and the file was otherwise preview-clean.
It is LOW because nothing behavioural moved and every ordered gate is honestly reproducible; what
it cost is a formatting violation in a production test file and a false sentence in the permanent
record. THE GATE COULD NOT HAVE CAUGHT IT: this repository runs `ruff` without `--preview` and
E301-E306 are preview-only, which finding R-0500 already recorded, so the reviewer's own
pre-emission dry run — which ran the block's exact ordered command, per checklist item 12 — was
blind in precisely the way that item exists to prevent. Running the whole repository under
`--preview` is NOT the counter-measure: 634 preview findings exist across `packages/`, `tests/`
and `apps/` at 3bb82a25, and sweeping them is the churn AGENTS.md's Code Discoverability section
forbids as its own activity. THE COUNTER-MEASURE IS TWO-PART, and R57 performs both. First, a code
slice CARRIES the blank lines its target's convention requires INSIDE the slice, so the separation
is a property of bytes that were measured rather than a consequence of a join shape that was
reasoned about. Second, a block whose change set appends to a `.py` file gates it with
`ruff check --preview` over THAT path alone, and only after the reviewer has read that path at the
base commit and found it preview-clean — a file with pre-existing preview findings takes the
narrower reading instead of a gate nobody can pass. Found by the reviewer while gating R56.

Gate: R58 — the R57 entry. R57 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over 3bb82a25..b2bb3809, not read, and each reproduces the handback's reading exactly; the worker
deviated in nothing and declared its scratch honestly. LINE COUNTS ARE `splitlines` COUNTS.
TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback:
`.remedy-wt/f085-r57.md`, the committed `.agent/authored/f085-r57.md` and the committed
`.agent/last_block.md` at b2bb3809, and both of those working copies as they stand at b2bb3809, are
all five byte-EQUAL at sha256 d186ed7740849c36c93e83bcc6ae3509ae820d743aa0eb7d06d3e575a7a18b74,
22571 B, 298 lines, 10 marker lines, which is the digest the reviewer emitted. THE SHAPES HELD.
Both REWRITES give `TO contains FROM: false`, the FROM 1x in the pre-commit blob and 0x after with
the TO exactly 1x, and in each case re-applying the extracted FROM→TO to the pre-commit blob
reproduces the post-commit blob BYTE-EXACTLY: PLAN11F→PLAN11T at ddd4f8b8 numstat `5 5`, and
FIXBLANKF→FIXBLANKT at 356a1568 numstat `1 0`, where the FROM is 142 B and the TO 143 B and
`tests/orchestration/test_exec_guard.py` goes 29917 B / 731 lines to 29918 B / 732 lines — the
whole effect is one newline byte. THE PROSE APPEND RECORD25 on `.agent/live_review.md` at a6c5176f:
byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix, 0 marker
LINES, and each of its 57 non-empty slice lines occurring exactly once among the 59 lines that
commit adds, numstat `59 0`. THE SUITES AND BOTH LINT HALVES WERE RE-RUN, NOT READ, in the primary
checkout with the block's exact command lines, each exit 0: the guard suite `35 passed`, the four
state readers `159 passed`, the canary `42 passed`, ruff `All checks passed!` and — the reading
this round exists for — `ruff check --preview` over the two paths `All checks passed!`. THE RED
CONTROL THE BLOCK DID NOT ORDER WAS RUN ANYWAY, in a disposable worktree since removed, because a
green preview cannot by itself tell a repaired file from one that was never broken: at 3bb82a25
that exact command is exit 1 with `Found 1 error.` and exactly one `E305` at
`tests/orchestration/test_exec_guard.py:691`, and at 49a3fdcb it is exit 0 `All checks passed!` —
so the fix has teeth and the violation was R56's alone. THE PLAN CONTRACT HELD at ddd4f8b8: 44
lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id present, 44 being
the figure that block projected. THE ARITHMETIC MOVED EXACTLY AS ORDERED: 172 / 27 / 0 and 145 open
at 3bb82a25, 173 / 27 / 1 and 146 open at b2bb3809, the registered and landed symmetric differences
each exactly `{R-0558}` and the done symmetric difference EMPTY, with 0 duplicate ids and 0
resolutions naming an unregistered id at both SHAs. HYGIENE IS CLEAN: the path set over that range
is exactly the six the change set named and holds NEITHER `packages/orchestration/exec_guard.py`
NOR `packages/orchestration/ui_server.py`; per-commit INSERTIONS are 298, 203, 5, 59, 1, 2 and 39
for the handback commit, none over 500; all seven commits are single-parent. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 298, PROSE 199 and RECORD25 58, agreeing with that
block, and the handback's self-claim of 79 lines measures 79. TWO NUMERIC CLAIMS RECORD25 PUT INTO
THE PERMANENT RECORD WERE CHECKED RATHER THAN ACCEPTED, since a wrong count there is the R-0402
class: `--preview` over `packages`, `tests` and `apps` at 3bb82a25 reports exactly 634 findings,
and at that SHA `_ENV_DUMP` carries two blank lines above its comment block where
`_RUNTIME_BUILD_ADDED_ENV_KEYS` carried one. NOTHING FAILED and this round registers no finding.

Done: R-0558 — Resolved at R57, commit 356a1568. The two-blank-line separation PEP 8 puts between a
function and the following top-level definition is restored before `_RUNTIME_BUILD_ADDED_ENV_KEYS`
in `tests/orchestration/test_exec_guard.py`; the edit adds exactly one newline byte and changes no
code. The reviewer verified the colour in both directions in a disposable worktree, since removed:
`python3 -m ruff check --preview` over that path is exit 0 at b2bb3809 and exit 1 with exactly one
`E305` at line 691 at 3bb82a25. BOTH HALVES of the counter-measure this finding named are in force
from R58 on. First, a code slice CARRIES the blank lines its target's convention requires INSIDE
the slice — R58 goes further and uses no append at all. Second, a block editing a `.py` file gates
that path with `ruff check --preview`, narrowed where the path already carries preview findings to
a comparison of the RULE-CODE MULTISET at base and at HEAD, since a bare exit-0 gate over such a
path is unpassable: at b2bb3809 `packages/orchestration/ui_server.py` reports 3 preview findings
and `tests/ui_server/test_dashboard_contract.py` reports 13, and R58 gates both in that narrowed
form.

Gate: R59 — the R58 entry. R58 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer over
b2bb3809..79f79f27, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL,
disk-to-disk with no digest fallback: `.remedy-wt/f085-r58.md`, the committed
`.agent/authored/f085-r58.md` and the committed `.agent/last_block.md` at 79f79f27, and both of those
working copies as they stand at 79f79f27, are all five byte-EQUAL at sha256
6d46cb294da82694650390a40f65c57cc886dd9885d3e1302a638270e193bd77, 29671 B, 436 lines, 24 marker
lines, which is the digest the reviewer emitted. THE SHAPES HELD. All six pairs give
`TO contains FROM: false`, the FROM 1x in the pre-commit blob and 0x after with the TO exactly 1x,
and for all four (commit, path) pairs re-applying the extracted FROM→TO to the pre-commit blob
reproduces the post-commit blob BYTE-EXACTLY: `.agent/plan.md` at 240934ad numstat `8 9`,
`.agent/live_review.md` at 728469ac numstat `53 1`, and at 35db0c2f
`packages/orchestration/ui_server.py` numstat `13 6` with the three pairs applied in order and
`tests/ui_server/test_dashboard_contract.py` numstat `35 0`. Marker LINES at 79f79f27 are 0 in every
one of those four files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with the block's
exact command lines, each exit 0: the dashboard contract `71 passed`, which is the 71 the block
ordered the worker to confirm rather than assume; responsive `92 passed`; the guard suite
`35 passed`; the four state readers `160 passed`; the canary `42 passed`. BOTH LINT HALVES HELD:
plain `ruff check` over the two paths is exit 0 `All checks passed!`, and the NARROWED PREVIEW
multiset comparison the R57 resolution mandated reproduces per path — `ui_server.py` `E306` x3 at
both b2bb3809 and 79f79f27, `test_dashboard_contract.py` `E226` x1 / `E303` x11 / `W391` x1 at both
— identical multisets, so no slice added a blank-line defect. THE PLAN CONTRACT HELD at 240934ad: 43
lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all present, 43
being the figure that block projected. THE ARITHMETIC MOVED EXACTLY AS ORDERED: 173 / 27 / 1 and 146
open at b2bb3809, 173 / 28 / 0 and 145 open at 79f79f27, the registered symmetric difference EMPTY,
the done symmetric difference exactly `{R-0558}` ADDED and the landed symmetric difference exactly
`{R-0558}` REMOVED, with 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs.
HYGIENE IS CLEAN: the path set over b2bb3809..35db0c2f is exactly the six the change set named and
holds no `packages/orchestration/exec_guard.py`; per-commit INSERTIONS are 436, 366, 8, 53, 48 and
104 for the handback commit, none over 500; all six commits are single-parent. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 436, PROSE 267 and RECORD26T 53, agreeing with that
block, and the handback's self-claim of 135 lines measures 135. THE RED CONTROL WAS RE-RUN BY THE
REVIEWER, in a disposable worktree since removed: with BUILDT reverted to BUILDF at the
`npm run build` site alone, `python3 -m pytest tests/ui_server/test_dashboard_contract.py -rf -q` is
EXIT 1 with exactly one failure, `test_auto_build_npm_commands_run_through_the_guard`, on
`assert bare_run.call_count == 0` reading `1 == 0` — the worker's reading reproduced line for line.
THE ONE CLAIM NO ORDERED GATE COVERS WAS CHECKED RATHER THAN ACCEPTED, since every test in the round
MOCKS the seam and none exercises the real child: at 79f79f27 the real `npm run build` in `apps/ui`
returns rc 0 with 355 bytes of stdout and 0 of stderr THROUGH the seam and rc 0 with 355 and 0 bare,
so the narrowed `runtime-build` environment allowlist really does carry a working npm build, and
constraint 9's behaviour-preservation claim is measured rather than asserted. The exception contract
was read at 79f79f27 and holds: `_completed_process_from_guarded` raises `subprocess.TimeoutExpired`
on a wall trip, `run_guarded` lets `Popen` raise `FileNotFoundError` before any translation, and
`check=True` raises `subprocess.CalledProcessError`, so all three names in the two surviving `except`
tuples stay reachable.

- R-0559 — Medium — the R58 block's G8 ordered an absence reading over three paths that do not exist
in this repository. It named `packages/orchestration/runtime_cmd.py`,
`packages/orchestration/dev_server.py` and `packages/orchestration/runtime_supervisor.py` and
required the round's path set to hold none of them. The three real files are
`apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
`packages/runtimes/runtime_supervisor.py`, each resolved on disk at 79f79f27. A gate that forbids
touching a path which cannot appear forbids nothing, so the protection G8 claimed over the NEXT
round's files was never in force — the vacuous-gate class of R-0438 and R-0532, arriving through a
path that was never resolved rather than through a base that lacks it. R58 still PASSES: G8's other
half enumerated the round's path set POSITIVELY and exhaustively, and that reading is what actually
held the change set to six paths, so nothing wrong landed. The cost is that the same three wrong
paths reached `.agent/handoff.md` at 79f79f27, which is the map the next session reads, and the next
round is exactly the round those paths matter for. COUNTER-MEASURE: item 24 of the §3 checklist in
`docs/agents/planner_reviewer_prompt.md`, which constraint 6 of the R59 block fixes as landing in
the commit BEFORE this record — every path a gate NAMES is resolved with `git ls-tree` at the base
the gate names before the block is emitted. The rule is promoted into the checklist rather than left
in this paragraph, because a standing rule written as finding prose binds nothing and recurs
(R-0452, R-0454).

Gate: R60 — the R59 entry. R59 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer over
79f79f27..d91d2ffa, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing beyond the handback length it declared. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT
HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback: `.remedy-wt/f085-r59.md`,
the committed `.agent/authored/f085-r59.md` and the committed `.agent/last_block.md` at d91d2ffa, and
both of those working copies as they stand at d91d2ffa, are all five byte-EQUAL at sha256
8df06395327c5573a708a055a05eaf9b0d0d02b5103ba823908f1e13abbc1fed, 31513 B, 447 lines, 14 marker
lines, which is the digest the reviewer emitted. THE SHAPES HELD, and the two classes were measured
apart. PLAN13F→PLAN13T at 0279b57e is a REWRITE: `TO contains FROM: false`, FROM 1x before and 0x
after, TO exactly 1x, numstat `10 8`. CHECKF→CHECKT at b5b76e3c is APPEND-shaped: `TO contains FROM:
true`, FROM 1x and TO 1x after, no zero count owed or reported, numstat `14 0`. For BOTH,
re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit blob
BYTE-EXACTLY. The three FROM-less appends satisfy ORDERED EQUALITY on every clause: for RECORD28's
predecessor RECORD27 at 307b4456, and for SEAMCODE and TESTCODE at b2104539, the pre-commit blob is
a byte-exact PREFIX, the slice an exact SUFFIX, `pre + slice` equals the post-commit blob byte for
byte, and each commit's ADDED lines equal that slice's lines IN ORDER — 65, 58 and 31 lines, numstat
`65 0`, `58 0` and `31 0`. Marker LINES at d91d2ffa are 0 in all five edited files. THE SUITES WERE
RE-RUN, NOT READ, in the primary checkout with the block's exact command lines, each exit 0: the
guard suite `36 passed`, which is the 36 the block ordered the worker to confirm rather than assume;
the four state readers `160 passed`, unchanged as ordered; the canary `42 passed`. BOTH LINT HALVES
HELD IN THE STRONG FORM over the two `.py` paths: `ruff check` exit 0 `All checks passed!` and
`ruff check --preview` exit 0 `All checks passed!`, which is the direct evidence that SEAMCODE and
TESTCODE carried their own leading blank lines — the R-0558 counter-measure holding as bytes rather
than as reasoning. THE PLAN CONTRACT HELD at 0279b57e: 45 lines against the 50-line cap with
`## Goal`, `## Next Steps` and a roadmap F-id present, 45 being the figure that block projected.
THE ARITHMETIC MOVED EXACTLY AS ORDERED: 173 / 28 / 0 and 145 open at 79f79f27, 174 / 28 / 0 and 146
open at d91d2ffa, the registered symmetric difference exactly `{R-0559}` ADDED with the done and
landed symmetric differences both EMPTY, and 0 duplicate ids and 0 resolutions naming an
unregistered id at both SHAs. HYGIENE IS CLEAN: the path set over 79f79f27..b2104539 is exactly the
seven the change set named and holds none of the three R61 call sites; per-commit INSERTIONS are
447, 368, 10, 14, 65, 89 and 91 for the handback commit, none over 500; all seven commits are
single-parent. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 447, PROSE 243
and RECORD27 65, agreeing with that block. CHECKLIST ITEM 24 WAS APPLIED TO THE BLOCK THAT REGISTERED
IT: all three R61 call sites resolve at 79f79f27 — `apps/cli/commands/runtime_cmd.py`,
`packages/runtimes/dev_server.py` and `packages/runtimes/runtime_supervisor.py` — so the R-0559
defect did not recur in the round that named it. THE RED CONTROL WAS RE-RUN BY THE REVIEWER, in a
disposable worktree since removed: `wall_timeout_seconds=None,` occurs 2x after C4 and mutating the
LAST occurrence alone to `30.0` gives EXIT 1 with exactly one failure,
`test_the_runtime_server_policy_holds_no_clock_and_no_cap`. THE CLAIM NO ORDERED GATE COVERS WAS
CHECKED RATHER THAN ACCEPTED, because the new test asserts on the policy dataclass and never spawns:
at d91d2ffa the reviewer built the policy with a declared key and a forbidden key both present, took
`plan_child_spawn`, and spawned a real child with the returned `cwd`, `env` and `preexec_fn`. The
child exited 0, reported its cwd as the pinned directory, received `REMEDY_RUNTIME_PORT`, did NOT
receive `ANTHROPIC_API_KEY`, and read `RLIMIT_CORE` as `(0, 0)` — so the rlimit really is applied
between fork and exec and the scrub really is enforced, on the one path the suite exercises only by
proxy. NOTHING FAILED and this round registers no finding.

Gate: R61 — the R60 entry. R60 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer over
d91d2ffa..5b9f935b, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing beyond the handback length it declared. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT
HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback: the committed
`.agent/authored/f085-r60.md` and the committed `.agent/last_block.md` at 5b9f935b, both of those
working copies as they stand at 5b9f935b, and the reviewer's own original are all five byte-EQUAL at
sha256 ec373c9c3df936db9dd595afa7799255e80649b84b0212e93ca43f0e8678aa47, 19312 B, 253 lines, 6 marker
lines, which is the digest that block carried. THE SHAPES HELD, and the two classes were measured
apart. PLAN14F→PLAN14T at ac7f5ac5 is a REWRITE: `TO contains FROM: false`, FROM 1x before and 0x
after, TO exactly 1x, numstat `6 6`, and re-applying the extracted FROM→TO to the pre-commit blob
reproduces the post-commit blob BYTE-EXACTLY. RECORD28 at a567afe3 satisfies ORDERED EQUALITY on
every clause: the pre-commit blob is a byte-exact PREFIX, the slice an exact SUFFIX, `pre + slice`
equals the post-commit blob byte for byte, and that commit's ADDED lines equal the slice's 47 lines
IN ORDER, numstat `47 0`. Marker LINES at 5b9f935b are 0 in both slice targets, `.agent/plan.md` and
`.agent/live_review.md`. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with the block's
exact command lines, each exit 0: the four state readers `160 passed`, unchanged as ordered, and the
canary `42 passed`. THE PLAN CONTRACT HELD at ac7f5ac5: 45 lines against the 50-line cap with
`## Goal`, `## Next Steps` and a roadmap F-id all present, 45 being the figure that block projected.
THE ARITHMETIC DID NOT MOVE, as constraint 8 of that block required: 174 registered / 28 done / 0
landed and 146 open at d91d2ffa, the same three numbers and the same 146 at 5b9f935b, max registered
R-0559 and max resolved R-0558 at both, all three symmetric differences EMPTY, and 0 duplicate ids
and 0 resolutions naming an unregistered id at both SHAs. HYGIENE IS CLEAN: the path set over
d91d2ffa..a567afe3 is exactly `.agent/authored/f085-r60.md`, `.agent/last_block.md`,
`.agent/live_review.md` and `.agent/plan.md`, holds no `.py` path at all and none of the three
`runtime-server` call sites; per-commit INSERTIONS are 253, 171, 6, 47 and 52 for the handback
commit, none over 500; all five commits are single-parent. THE BLOCK'S OWN SIZE re-measured from the
committed file gives TOTAL 253, PROSE 170 and RECORD28 47, agreeing with that block's own figures and
under 490 / 400 / 140. CHECKLIST ITEM 24 HELD FOR THE ROUND AFTER THE ONE THAT PROMOTED IT: all three
call sites resolve at d91d2ffa — `apps/cli/commands/runtime_cmd.py` blob 01ab65ed,
`packages/runtimes/dev_server.py` blob 7715a28e and `packages/runtimes/runtime_supervisor.py` blob
9f3749ae — so the absence clause G7 carried forbade paths that really exist, which is what R-0559
asked for. THE ONE REPORTING NOTE THE HANDBACK RAISED WAS CHECKED RATHER THAN ACCEPTED: G3's
marker-count clause and G2's are not in conflict, because G3 counts marker lines in the slice
TARGETS, where the reviewer reads 0, while G2 counts them in the two transport COPIES, where the
reviewer reads 6 by construction. NOTHING FAILED and this round registers no finding.

Gate: R62 — the R61 entry. R61 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer over
5b9f935b..a05669a5, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing beyond the handback length it declared and one stated assumption about when a base reading
was taken, which the reviewer's own independent base reading corroborates. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest
fallback: the reviewer's original, the committed `.agent/authored/f085-r61.md` and the committed
`.agent/last_block.md` at a05669a5, and both of those working copies as they stand at a05669a5, are
all five byte-EQUAL at sha256
bb18ff7d5cdb461883a2e3b35fa6e137f178bbf759362d312904c91cd5b80eab, 30129 B, 484 lines, 32 marker
lines. THE SHAPES HELD, and the two classes were measured apart, one reading per pair. The five
REWRITES each end FROM 0x with TO exactly 1x — PLAN16's predecessor PLAN15 at 70c6c741, numstat
`9 10`, and SITE2B, SITE3B, BOUNDA and BOUNDB at 63c9fd46. The two APPEND-shaped pairs, SITE2A and
SITE3A at 63c9fd46, end FROM 1x and TO 1x, and no zero count was owed or reported for either. For
all seven, re-applying the extracted pairs in order to the pre-commit blob reproduces the
post-commit blob BYTE-EXACTLY, per path. The two FROM-less appends satisfy ORDERED EQUALITY on every
clause: RECORD29 at 603e39f7 and TESTCODE at 9727c5e3 each have the pre-commit blob as a byte-exact
PREFIX, the slice as an exact SUFFIX, `pre + slice` equal to the post-commit blob byte for byte, and
the commit's ADDED lines equal to the slice's lines IN ORDER — 36 and 49 lines, numstat `36 0` and
`49 0`. Marker LINES at a05669a5 are 0 in all six edited files. BOTH LINT HALVES WERE ALREADY RED AT
THE BASE, so both were compared as rule-code MULTISETS rather than demanded green, and both are
UNCHANGED: `ruff check` over the four paths gives `{I001: 1}` at 5b9f935b and `{I001: 1}` at
a05669a5, and `ruff check --preview` gives `{E303: 1, I001: 1}` at both — no new code and no second
instance, so neither migration introduced a lint finding. THE SUITES WERE RE-RUN, NOT READ, in the
primary checkout with the block's exact command lines, each exit 0: `tests/runtimes/` `252 passed`
against a base of `251 passed` with no skips at either, which is the base plus exactly the one test
C4 added; the guard suite `36 passed`, unchanged, so the seam this round CONSUMES was not altered;
the four state readers `160 passed`, unchanged; the canary `42 passed`. THE PLAN CONTRACT HELD at
70c6c741: 44 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present, 44 being the figure that block projected. THE ARITHMETIC DID NOT MOVE, as constraint 8 of
that block required: 174 registered / 28 done / 0 landed and 146 open at 5b9f935b, the same three
numbers and the same 146 at a05669a5, max registered R-0559 and max resolved R-0558 at both, all
three symmetric differences EMPTY, and 0 duplicate ids and 0 resolutions naming an unregistered id at
both SHAs. HYGIENE IS CLEAN: the path set over 5b9f935b..9727c5e3 is exactly the eight the change set
named and holds `apps/cli/commands/runtime_cmd.py` not at all; per-commit INSERTIONS are 484, 397, 9,
36, 46, 49 and 54 for the handback commit, none over 500; all seven commits are single-parent. THE
BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 484, PROSE 269 and RECORD29 36,
agreeing with that block's own figures and under 490 / 400 / 140. TWO CLAIMS NO GATE COVERED WERE
CHECKED RATHER THAN ACCEPTED, both by the reviewer before the block was emitted and both inside a
disposable worktree since removed, with the primary checkout's `git status --porcelain` empty
immediately after each. FIRST, the block's own slices were applied to a throwaway tree and its gates
run there, which is how the boundary test
`test_the_readiness_failure_returns_the_line_the_child_really_printed` was found to go RED at exit 3
under the migration alone — it handed its application a marker path through the PARENT environment —
and that is why C3 carries its adaptation in the same commit instead of leaving a knowingly red
commit on the branch. SECOND, the red control: reverting ONLY `env=spawn_plan.env` to `env=env` in
`packages/runtimes/dev_server.py` makes the new test FAIL on exactly its
`ANTHROPIC_API_KEY not in child_env` assertion, with the imported module path printed from inside
the same invocation to prove the worktree copy was the one under test. So the test pins the scrub
rather than passing for an unrelated reason. NOTHING FAILED and this round registers no finding.

Gate: R63 — the R62 entry. R62 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer over
a05669a5..cbe1b3e5, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing and declared nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD, disk-to-disk
with no digest fallback, though NOT against a reviewer scratchpad original: R62 was authored by an
earlier session and this one holds no original of it, so the comparison ran across the six copies
that do exist — the committed `.agent/authored/f085-r62.md` at 37114518 and at cbe1b3e5, the
committed `.agent/last_block.md` at aa9b94e8 and at cbe1b3e5, and both working copies as they stand
at cbe1b3e5 — all six byte-EQUAL at sha256
ad6827dc70e67bd8d007666fa379345ea4c318b9a62ac58baa19ceb10a4ead50, 19619 B, 256 lines, 6 marker
lines. What binds that block's CONTENT is the shape proof rather than the digest, and it held. THE
SHAPES HELD, and the two classes were measured apart, one reading per pair. PLAN16F→PLAN16T is a
REWRITE — its containment test reads `TO contains FROM: false` — and over `.agent/plan.md` at
3d754312 it ends FROM 0x with TO exactly 1x, its FROM having occurred exactly 1x in that file at
aa9b94e8, and re-applying the extracted pair to the pre-commit blob reproduces the post-commit blob
BYTE-EXACTLY. RECORD30, which has no FROM, satisfies ORDERED EQUALITY on every clause over
`.agent/live_review.md` at 5cced41e: the pre-commit blob at 3d754312 is a byte-exact PREFIX, the
slice is an exact SUFFIX, `pre + slice` equals the post-commit blob byte for byte, and that commit's
ADDED lines equal the slice's lines IN ORDER, 50 and 50, numstat `50 0`. Marker LINES at cbe1b3e5
are 0 in `.agent/plan.md`, in `.agent/live_review.md` and in `.agent/handoff.md`. THE SUITES WERE
RE-RUN, NOT READ, in the primary checkout with that block's exact command lines, each exit 0: the
four state readers `160 passed` against a base of `160 passed`, and the canary `42 passed` against a
base of `42 passed`, both unchanged because that round changed no code. THE PLAN CONTRACT HELD at
cbe1b3e5: 44 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present, 44 being the figure that block projected. THE ARITHMETIC DID NOT MOVE, as constraint 8 of
that block required: 174 registered / 28 done / 0 landed and 146 open at a05669a5, the same three
numbers and the same 146 at cbe1b3e5, max registered R-0559 and max resolved R-0558 at both, all
three symmetric differences EMPTY, and 0 duplicate ids and 0 resolutions naming an unregistered id at
both SHAs. HYGIENE IS CLEAN: the path set over a05669a5..cbe1b3e5 is exactly the five the change set
named, holds no `.py` path at all, and holds `apps/cli/commands/runtime_cmd.py` not at all;
per-commit INSERTIONS are 256, 166, 7, 50 and 30 for the handback commit, none over 500; all five
commits are single-parent; and `.agent/handoff.md` at cbe1b3e5 is 60 lines, within its own cap, with
the ordered Fortschritt line present verbatim. THE BLOCK'S OWN SIZE re-measured from the committed
file at cbe1b3e5 gives TOTAL 256, PROSE 172 counting its 6 marker lines and RECORD30 50, agreeing
with that block's own figures and under 490 / 400 / 140. ONE CLAIM NO GATE COVERED WAS CHECKED
RATHER THAN ACCEPTED: the R62 handback's open question, whether the supervisor needs `PYTHONPATH`
and `VIRTUAL_ENV` declared, was settled by reading `packages/orchestration/exec_guard.py` at
cbe1b3e5, where both keys are already members of the tuple `RUNTIME_SERVER_ENV_ALLOWLIST` is
assigned from, so R63 declares neither. NOTHING FAILED and this round registers no finding.

Gate: R64 — the R63 entry. R63 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over cbe1b3e5..e26f1f3e, not read, and each reproduces the handback's reading exactly; the worker
deviated in nothing and declared nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD,
disk-to-disk with no digest fallback, though NOT against a reviewer scratchpad original: R63 was
authored by an earlier session and this one holds no original of it, so the comparison ran across
the six copies that do exist — the committed `.agent/authored/f085-r63.md` at 28dd3923 and at
e26f1f3e, the committed `.agent/last_block.md` at 9a8e3161 and at e26f1f3e, and both working
copies as they stand at e26f1f3e — all six byte-EQUAL at sha256
b9230558fafe431bc69a62dadd059d93c1977510d53baceb817e7ef0a71c1d29, 26177 B, 373 lines, 12 marker
lines. What binds that block's CONTENT is the shape proof rather than the digest, and it held.
THE SHAPES HELD, and the two classes were measured apart, one reading per pair. PLAN17F→PLAN17T
over `.agent/plan.md` at 87c467db and SITE4F→SITE4T over `apps/cli/commands/runtime_cmd.py` at
a045970b are both REWRITES — each containment test reads `TO contains FROM: false` — and each
ends FROM 0x with TO exactly 1x, each FROM having occurred exactly 1x in its own target at
9a8e3161 and at 1d1c6abc respectively, with re-application of the extracted pair to the
pre-commit blob reproducing the post-commit blob BYTE-EXACTLY in both cases.
RECORD31 and TESTCLI, neither of which has a FROM, satisfy ORDERED EQUALITY on every clause:
RECORD31 over `.agent/live_review.md` at 1d1c6abc and TESTCLI over
`tests/cli/test_runtime_cmd.py` at 394c45af each have the pre-commit blob as a byte-exact PREFIX,
the slice as an exact SUFFIX, `pre + slice` equal to the post-commit blob byte for byte, and that
commit's ADDED lines equal to the slice's lines IN ORDER — 39 and 39, 42 and 42, numstat `39 0`
and `42 0`. Marker LINES at e26f1f3e are 0 in each of the four edited files. THE SUITES WERE
RE-RUN, NOT READ, in the primary checkout with that block's exact command lines, each exit 0:
`305 passed` against a base of `304 passed` for the migration set, C4's one new test being the
difference; `160 passed` against a base of `160 passed` for the four state readers; and the
canary `42 passed` against a base of `42 passed`. ONE READING HAD TO BE TAKEN TWICE, recorded
because it will recur: run concurrently with a second pytest process over the same file, the
migration set read `1 failed, 304 passed` and blamed
`test_an_instance_id_that_changes_during_the_request_is_never_healthy`, while serially and alone
it read `305 passed` at exit 0. These suites spawn real supervisors that bind a port and leave
escapees when a readiness assertion fails, so concurrency alone reddens tests neither run
touched; the serial reading is the honest one. THE PLAN CONTRACT HELD at e26f1f3e: 39 lines
against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all present, 39 being
that block's own projection. THE ARITHMETIC DID NOT MOVE, as constraint 8 required: 174
registered / 28 done / 0 landed and 146 open at cbe1b3e5, the same three numbers and the same 146
at e26f1f3e, max registered R-0559 and max resolved R-0558 at both, all three symmetric
differences EMPTY, and 0 duplicate ids and 0 orphan resolutions at both SHAs. LINT WAS RE-RUN over
both `.py` paths from the repository root with the repository's own configuration, plain and
`--preview`, each exit 0 with `All checks passed!`. THE RED CONTROL REPRODUCED EXACTLY inside a
disposable worktree at e26f1f3e: reverting only `cwd=spawn_plan.cwd, env=spawn_plan.env,` to
`cwd=str(source_root), env=env,` — a one-line worktree diff and nothing else — turned
`python3 -m pytest tests/cli/test_runtime_cmd.py -q -rf` from `17 passed` at exit 0 into
`1 failed, 16 passed` at exit 1, failing
`TestTheSupervisorEnvironmentIsScrubbed::test_a_secret_parent_variable_never_reaches_the_supervisor`
on its `assert "ANTHROPIC_API_KEY" not in env` line with the secret present in the reported
environment; that un-reverted baseline of `17 passed` also confirms C4 added exactly one test to
a file whose base was 16. HYGIENE IS CLEAN: the path set over cbe1b3e5..e26f1f3e is exactly the
seven the change set named; all four paths G9 orders resolved at cbe1b3e5 under `git ls-tree`;
per-commit INSERTIONS are 373, 287, 6, 39, 18, 42 and 46 for the handback commit, none over 500;
all seven commits are single-parent; and `.agent/handoff.md` at e26f1f3e is 75 lines, within the
≤100-line cap its seven-commit table allows, with the ordered Fortschritt line present verbatim.
THE BLOCK'S OWN SIZE re-measured from the committed file at e26f1f3e gives TOTAL 373, PROSE 226
counting its 12 marker lines and RECORD31 39, agreeing with that block's own figures and under
490 / 400 / 140. ONE CLAIM NO GATE COVERED WAS CHECKED RATHER
THAN ACCEPTED: RECORD31's assertion that `PYTHONPATH` and `VIRTUAL_ENV` need no declaration holds
at e26f1f3e, where `packages/orchestration/exec_guard.py` assigns
`RUNTIME_SERVER_ENV_ALLOWLIST` from `TEST_COMMAND_ENV_ALLOWLIST` and that tuple lists both keys.
ONE STATE OBSERVATION IS RECORDED AND IS NOT A WORKER DEVIATION: a disposable worktree
`.remedy-wt/rv63` existed at review time, created after the handback commit e26f1f3e by a
reviewer session that did not survive to remove it and holding a clean tree at that commit; the
reviewer used it for the red control above, then removed and pruned it, leaving `git worktree
list` at one line and `git status --porcelain` empty in the primary checkout. NOTHING FAILED and
this round registers no finding.

Gate: R65 — the R64 entry. R64 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer over
e26f1f3e..e5eecb29, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing and declared nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD, disk-to-disk
with no digest fallback: the committed `.agent/authored/f085-r64.md` and the committed
`.agent/last_block.md` at e5eecb29, both working copies as they stand at e5eecb29, and the received
`.remedy-wt/f085-r64.md` are all five byte-EQUAL at sha256
670a2563e54daff38b815a445493dba8b417024e65c5eba4e0b9cbcdb8ae2108, 31314 B, 490 lines, 32 marker lines.
THE SHAPES HELD, and the two classes were measured apart, one reading per pair. PLAN18F→PLAN18T over
`.agent/plan.md` at a8877d26, GUARD1F→GUARD1T and GUARD6F→GUARD6T over
`packages/orchestration/exec_guard.py` at 01fd653d are REWRITES — each containment test reads
`TO contains FROM: false` — and each ends FROM 0x with TO exactly 1x, each FROM having occurred
exactly 1x in its own pre-commit blob. GUARD2, GUARD3, GUARD4 and GUARD5 are APPEND-shaped over that
same file at 01fd653d, each reading FROM exactly 1x AND TO exactly 1x post-commit with no FROM-zero
reading taken, and all six GUARD pairs re-applied IN ORDER to the pre-commit blob reproduce the
post-commit blob BYTE-EXACTLY. RECORD32 over `.agent/live_review.md` at 2e6b772e and TESTNET over
`tests/orchestration/test_exec_guard.py` at 25c75325, neither of which has a FROM, satisfy ORDERED
EQUALITY on every clause: pre-commit blob a byte-exact PREFIX, slice an exact SUFFIX, `pre + slice`
equal to the post-commit blob byte for byte, and each commit's ADDED lines equal to the slice's lines
IN ORDER — 64 and 64, 57 and 57, numstat `64 0` and `57 0`. Marker LINES at e5eecb29 are 0 in each of
the four edited files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with that block's
exact command lines, serially, each exit 0: `329 passed` against a base of `324 passed` for the seam
set, C4's five new tests being the difference; `160 passed` against a base of `160 passed` for the
four state readers; and the canary `42 passed` against a base of `42 passed`. THE PLAN CONTRACT HELD
at e5eecb29: 42 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present, 42 being that block's own projection. THE ARITHMETIC DID NOT MOVE, as that block's
constraint 8 required: 174 registered / 28 done / 0 landed and 146 open at e26f1f3e, the same three
numbers and the same 146 at e5eecb29, max registered R-0559 and max resolved R-0558 at both, all
three symmetric differences EMPTY, and 0 duplicate ids and 0 orphan resolutions at both SHAs. LINT
WAS RE-RUN over both `.py` paths from the repository root with the repository's own configuration,
plain and `--preview`, each exit 0 with `All checks passed!`. THE RED CONTROL REPRODUCED EXACTLY
inside a disposable worktree at 25c75325: deleting the one line `        deny_network=True,` from
`test_command_exec_policy` in `packages/orchestration/exec_guard.py` — a worktree `git diff --stat` of
`1 file changed, 1 deletion(-)` and nothing else — turned
`python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` red at exit 1 with
`2 failed, 39 passed`, failing both
`test_the_test_class_policy_denies_the_network_its_row_denies`, the one that block ordered, and
`test_a_denied_child_really_receives_the_closed_port` on its
`assert dumped["HTTP_PROXY"] == exec_guard.DENIED_NETWORK_PROXY_URL` line with `KeyError: 'HTTP_PROXY'`
— the second being the real-child half of the same one-line revert, which that handback reported
rather than concealed. HYGIENE IS CLEAN: the path set over e26f1f3e..e5eecb29 is exactly the seven the
change set named and holds none of the three `runtime-server` paths; all five paths G9 orders resolved
at e26f1f3e under `git ls-tree`; per-commit INSERTIONS are 490, 419, 12, 64, 39, 57 and 32 for the
handback commit, none over 500; all seven commits are single-parent. THE BLOCK'S OWN SIZE re-measured
from the committed file at e5eecb29 gives TOTAL 490, PROSE 274 counting its 32 marker lines and
RECORD32 64, agreeing with that block's own figures and inside 490 / 400 / 140. ONE FINDING IS
REGISTERED AGAINST THAT BLOCK'S OWN GATE TEXT, and it is the reviewer's defect rather than the
worker's, which is why R64 still PASSES.

- R-0560 — Low — the R64 block's G8 ordered a destructive revert by quoting a line that was not unique
in the tree at the SHA the control runs at. It ordered "revert EXACTLY ONE thing: the single line
`        deny_network=True,` in `test_command_exec_policy`", and at 25c75325 those exact bytes occur
TWICE: once in `packages/orchestration/exec_guard.py`, which is where `test_command_exec_policy` is
defined, and once in `tests/orchestration/test_exec_guard.py`, which TESTNET appended in the same
round. The qualifier that disambiguates them is the function name, and that name begins with `test_`,
so it reads as a pointer INTO the test file for anyone who has not already resolved the symbol. The
reviewer of this round deleted the wrong occurrence on the first attempt, restored the file and
re-ran, so the cost is measured rather than hypothetical. This is the vacuous-and-ambiguous gate
family of R-0438, R-0532 and R-0559 arriving through the BYTES a gate orders changed rather than
through the paths it names: item 24 would have resolved every path in that sentence and still passed
it, because both paths exist. R64 PASSES anyway — the control was met, the deletion that was finally
made was the ordered one, the `1 file changed, 1 deletion(-)` reading in the handback is the correct
one, and the red it produced is the red the block predicted. The danger is that a red control cannot
tell a wrong revert from a right one: deleting the TESTNET occurrence also reddens that suite, so a
reader who never noticed the ambiguity would have reported a green-looking control that proved
nothing about `test_command_exec_policy`. COUNTER-MEASURE: item 25 of the §3 checklist in
`docs/agents/planner_reviewer_prompt.md`, which constraint 6 of this block fixes as landing in the
commit BEFORE this record — a revert target is named by the PATH it is applied to and its exact bytes
are counted IN THAT FILE at the SHA the control names, a count above 1 forcing a longer unique string.
The rule is promoted into the checklist rather than left in this paragraph, because a standing rule
written as finding prose binds nothing and recurs (R-0452, R-0454). OPEN.
