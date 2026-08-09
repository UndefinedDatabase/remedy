# Context — F105 Cache-optimal prompt ordering

## Active Branch
feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245 after
PR #188 — the F104 closure — was merged at the Open PR Gate. F105 is claimed
`[~]` under Rule A5 as the first `[ ]` entry after F104 in
docs/roadmap/STATUS.md.

## Scope
In: a registered-segment prompt registry with a documented stability rank
scale; `compose()` producing byte-stable ordering per role plus a segment
manifest (name, rank, hash) recorded into call evidence; role loaders for the
existing docs/agents/worker_conventions.md and docs/agents/reviewer_conventions.md
under a token cap that fails loudly; migration of the existing prompt builders
to compose through the registry, each with a content-equality golden; and
`remedy stats cache`, which reports cache-read share per role from actuals the
system already captures.

Out, per the feature file's Do-not-touch: model-routing policy content,
provider-side cache configuration, and prompt CONTENT beyond composition. The
two conventions files are LOADED here, never re-authored — any change to their
rules goes through a reviewed diff of those files, not through builder code.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/ and apps/, and
  production code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/ also runs tests/docs/.
  The full suite runs only at the integration gate, with `-n auto`. Destructive
  and mutation checks run only inside a disposable git worktree, so resource
  safety stays intact and no background pytest process is ever left running.
- A cache figure no provider reported prints as "not reported", never as a zero
  pretending to be a measurement (A9).

## Steps
R1 claim, candidate sweep and state reset → R2 T001 the segment registry,
compose and the manifest → R3 T002 the conventions loaders and their goldens →
R4+ T003 one builder per round, each with a content-equality golden → T004 the
cache stats view → integration gate → closure.
