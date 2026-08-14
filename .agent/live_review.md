# Live Review — F057 Rate-limit-aware scheduler

> Round-by-round review record for the F057 branch, reset at the feature claim.
> The paydown0814 record closed with PR #198, merged 2026-08-14; that branch's
> closing verdict lives in its handoff and in the PR, per
> docs/agents/planner_reviewer_prompt.md §4 item 13. Finding ids continue the
> monotonic R-XXXX series across the reset. Next free id: R-0363.
>
> This reset CARRIES the open set forward rather than dropping it. R-0361 was
> open when the previous record closed and is reproduced verbatim at the end of
> this file, byte for byte out of `21c8148e:.agent/live_review.md`. See
> DECISION F057 D1 in `.agent/decisions.md`.

## Steps
R1 claim F057, reset this record carrying R-0361 forward, register R-0362,
record DECISION F057 D1, and build T001 — one place that normalizes the
rate-limit signal shapes this repo really emits, with unit tests over samples
extracted from existing evidence → R2 T002, the governor itself: per-provider
cooldown state, `acquire()` with a budget deadline, an injected clock, and the
stop-beats-wait ordering → R3 T003, the seam integration at the provider-call
choke point, wait evidence, the report line, and the limit-emitting fixture
end-to-end → integration gate → closure.

## Findings

- R-0362 — Medium — the open-finding set is silently discarded at every branch claim, and Rule A2 forbids the claim that discards it. ROADMAP.md:27 states Rule A2 as "Every block ends with a final review: PASS or FINDINGS. No new feature is started while findings are open", and `docs/agents/reviewer_conventions.md` restates it as "No new feature starts while findings are open (A2)". At the F045 closure the reviewer's own GATE-R15 entry recorded the open set as exactly three — R-0350, R-0354 and R-0358, all Low — after RECOMPUTING it from the record per the pre-emission checklist's item 10. None of those three ids appears anywhere in the paydown0814 record that replaced it: `git show f789ebc8:.agent/live_review.md` carries only R-0359, R-0360 and R-0361. The reset therefore did not resolve them, did not defer them and did not name them; it dropped them, and the same mechanism was about to drop R-0361 at this claim. Two rules are in conflict and neither yields on its own: A2 read literally blocks every feature claim that follows a PASS_WITH_RISKS closure, which is six of the last seven closures in `docs/roadmap/STATUS.md`, while the reset as practised makes A2 unenforceable by erasing its input. No governing document authorises the erasure — `docs/agents/planner_reviewer_prompt.md` §1 says the record is reset at the claim but says nothing about what happens to findings that are open when it is, and `docs/roadmap/STATUS_closure_protocol.md` routes only CLOSURE CANDIDATES, which are explicitly not findings and spend no id. Registered here rather than acted on silently, per §2's rule that a practice invoked without a doc pointer is a finding candidate in the same brief. The structural half of the fix is applied in this round: this record carries R-0361 forward verbatim instead of dropping it, and DECISION F057 D1 states the reading under which the claim proceeds. The documentation half — an explicit carry-forward rule in `docs/agents/planner_reviewer_prompt.md` §1, and whatever becomes of R-0350, R-0354 and R-0358 — is NOT in this feature's scope: AGENTS.md forbids mixing an unrelated fix into a feature branch, so it belongs on its own paydown branch, exactly as DECISION F045 D8 routed the reviewer-conventions repair. OPEN.

- R-0361 — Low — a gate round ordered a proof command the session cannot execute, and asserted an exit code the fetch tool contradicts. The R1 gate block ordered the posted F045 verdict fetched back with `gh api --paginate ... --jq '.[-1].body'` and `cmp`-ed against the authored file, expecting exit 0. `gh api` is denied by this session's permission layer, so the ordered command never ran at all; the worker's substitute, `gh pr view 197 --json comments --jq`, exited 1 because the `--jq` writer appends a newline to a body that already ends in one, leaving the fetched file exactly one byte longer with no differing byte in the common prefix. The worker proved equality the honest way instead — extracting the raw JSON body with no jq in the path, where the sha256 of the posted bytes and of the authored file are both `b9db4e4c41cf59c0c4adcfa8368c83843e2c0ee4e29ceab0b324864ebc19f5ff` and `cmp` exits 0 — declared both deviations in its report, and proceeded rather than burning the round on a tooling artifact. The reviewer re-verified that byte equality independently at `1e7f7bca` and agrees the merge was safe; nothing landed wrong. This is the R-0252/R-0336/R-0350 family — an ordered gate whose expected value the reviewer never computed from the tool that produces it — plus a second failure the existing counter-measures do not reach: ordering a command the permission layer denies makes the gate UNREACHABLE rather than merely wrong, and an unreachable gate cannot fail honestly. Counter-measure, applied from R2 on: a block may only order a command the reviewer has itself executed in this session, and a byte-equality claim over any transport that may normalise trailing newlines is stated as a sha256 comparison over extracted bytes, never as a `cmp` exit code. OPEN.
