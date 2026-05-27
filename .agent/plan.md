# Plan

## Goal
Step 38.1: Grouped CLI Entry-Point Hardening

## Current Step
Complete — committing

## Tasks
- [x] Add compatibility bridge in apps/cli/main.py (group name detection, subcommand disambiguation)
- [x] Handle conflict: "brain" and "project" are both old flat commands and group names
- [x] Add 12 behavioral tests for bridge delegation (group help, dispatch, flat compat)
- [x] Verify full test suite: 2236 passed, 0 failed
- [x] Verify `remedy job` exits 0 with grouped help via installed command
- [ ] Commit and push
