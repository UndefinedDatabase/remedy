# Contract template — api-service

The floor of the contract for an order that builds an HTTP API service. Every criterion below is
part of such a mission's contract, and the planner adds its own criteria on top; it never drops one
of these. The format is DECISION F269 D1's, and `remedy do --contract api-service` forces this
template.

## Proposed when the order mentions

- api
- rest api
- http api
- endpoint
- web service
- microservice

## Criteria

- blocking: Every endpoint the order names exists, and a test calls each one and checks its response.
- blocking: A request with invalid input gets a client error response, never a server error, and a test proves it.
- blocking: The test suite passes.
- advisory: Every endpoint the service serves is documented.
- blocking: No file is added that nothing references.
  check: {"kind": "custom_cmd", "spec": {"argv": ["python3", "-m", "packages.orchestration.contract_hygiene", "unreferenced"]}, "description": "contract hygiene: unreferenced"}
- blocking: Code that is replaced is deleted in the same task, never left beside its replacement.
  check: {"kind": "custom_cmd", "spec": {"argv": ["python3", "-m", "packages.orchestration.contract_hygiene", "replaced"]}, "description": "contract hygiene: replaced"}
- blocking: No stub, placeholder or TODO body survives the job.
  check: {"kind": "custom_cmd", "spec": {"argv": ["python3", "-m", "packages.orchestration.contract_hygiene", "stubs"]}, "description": "contract hygiene: stubs"}

## Fixture order

Build an HTTP API service that stores notes, with endpoints to create, list and delete a note.
