# Self-Repair Proposal User Guide

## What is a self-repair proposal?

A self-repair proposal is a safe, bounded document that Remedy creates after
analyzing its own run evidence. It describes what seems broken, what evidence
supports that conclusion, and what a worker should do to fix it.

A proposal is **not** auto-repair. It is a draft for you to review.

## How it differs from auto-repair

| Aspect | Auto-repair | Self-repair proposal |
|--------|-------------|----------------------|
| Who decides? | The system | You (the operator) |
| Code changes? | Automatic | None until you approve |
| Provider calls? | Yes | Never |
| Can be denied? | No | Yes |
| Can be edited? | No | Yes |

## Workflow

### 1. Create a proposal from a run

```bash
remedy self-repair proposal-create <run_id> --json
```

Remedy analyzes the replay evidence for the given dogfood run and creates a
proposal. If no issues are found, the proposal status is `blocked`.

### 2. Review the proposal

```bash
remedy self-repair proposal-show <proposal_id> --json
```

Read the problem summary, evidence references, suspected files, and suggested
worker prompt.

### 3. Approve, deny, or edit

```bash
# Approve
remedy self-repair proposal-approve <proposal_id> --operator-id <your-id> --json

# Deny
remedy self-repair proposal-deny <proposal_id> --operator-id <your-id> --reason "not needed" --json

# Edit the worker prompt
remedy self-repair proposal-edit <proposal_id> --operator-id <your-id> --text "revised prompt" --json
```

Editing returns the proposal to `awaiting_operator` status. You must approve
it again after editing.

### 4. Convert to worker prompt

```bash
remedy self-repair worker-prompt <proposal_id> --json
```

Only approved proposals can be converted. The output is prompt text — Remedy
does not execute it automatically.

### 5. List proposals

```bash
remedy self-repair proposal-list --json
remedy self-repair proposal-list --run-id <run_id> --json
```

## How evidence references work

Proposals contain evidence references like:

- `replay:<run_id>` — points to a dogfood run replay analysis
- `integrity:<check_code>` — points to a specific integrity check result
- `review_bundle:<section_name>` — points to a degraded review bundle section
- `config:<warning>` — points to a config diagnostic warning

Follow these references to inspect the underlying evidence. Raw logs, prompts,
transcripts, and secrets are never included in the proposal.

## What is not automated yet

- No automatic code repair
- No automatic approval
- No automatic PR or commit creation
- No provider/model-assisted diagnosis
- No cross-run correlation
- No learning from past proposals
