# Plan — operator order beweis (2026-10-29): Remedy proves it runs alone

## Goal
decodeux's order beweis: the reruns of 2026-10-29 must run without a question to him. Five
causes become F326 to F330 (Package 3, Tier 2), built on branch feature/beweis.

## Current Step
F326 to F331 built; F331 is the gap F330's time-cap check found.

## Next Steps
1. F326 the builder may run what the reviewer asks for.
2. F327 no order budget for narration; three rounds kept free.
3. F328 an unattended job raises its budget once (interface 1.34, body `auto_extend`).
4. F329 Remedy's own test run narrows to the changed parts.
5. F330 a task outside this repository ends an unattended job; time cap across a restart.

## Risks
- The orchestrator merges feature/beweis, pushes and restarts the service, not this session.
