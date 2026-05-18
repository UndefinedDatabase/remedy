"""
apps.api — Reserved namespace for Remedy HTTP API server.

Planned purpose:
    REST/WebSocket API exposing Remedy orchestration over HTTP.  Will wrap
    the CLI command layer with a FastAPI or similar framework, enabling
    external tooling, dashboards, and multi-user access.

Current status:
    Reserved namespace — no implementation in this step.
    All access is via the CLI (apps.cli.main).

Future layer:
    HTTP API server (planned Step 38+).
"""
