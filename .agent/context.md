# Context

## Active Branch
feature/steps-850-864-tooling-provenance

## Scope
Steps 850-864: Proof Chain file-provenance hotfix plus Pi/Claude/VS Code tooling modernization.

## Prior Step Status
Steps 840-849: BLOCKED BY REVIEW until file provenance stops showing unrelated/global tests as causal proof. Timestamp ordering and change_set association are otherwise fixed.

## Current Work
Part A: make `file why` use the same linked-test truth as `change proof --path` and omit unlinked/global tests from proof chain steps.
Part B: inspect actual on-disk `.pi`, `.claude`, MCP, and package setup; document/configure safe local agent tooling without inventing schemas.

## Detected Setup So Far
- `.pi/`: absent in actual working repo.
- `.claude/`: present with `.claude/settings.local.json` only.
- `.mcp.json`: absent.
- `.vscode/mcp.json`: absent.
- Root `package.json`: absent.
- `apps/ui/package.json` and lockfile: present.

## Constraints
Use `scripts/remedy_pytest.sh`; no direct pytest, no background pytest, no `shell=True`.
No secrets, `.env`, `.data`, raw artifacts/stdout/diffs/source content in summaries.
Reviewer findings beat worker self-report.
