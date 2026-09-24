# Task Plan

Schema: task_plan_v1
Tasks: 4

## Tasks

### 1. T1 — Build T1

**Goal:** goal of T1
**Band:** S | **Depends on:** none

**Acceptance:**
- the parser reads a file

**Files hint:**
- `docs/README.md`

### 2. T3 — Build T3

**Goal:** goal of T3
**Band:** S | **Depends on:** T1

**Acceptance:**
- the summary names the file

**Files hint:**
- `docs/README.md`

### 3. T2a — Build T2 (1/2)

**Goal:** goal of T2
**Band:** M | **Depends on:** T1

**Acceptance:**
- the report lists every row

**Files hint:**
- `docs/README.md`

### 4. T2b — Build T2 (2/2)

**Goal:** goal of T2
**Band:** M | **Depends on:** T2a

**Acceptance:**
- the report totals each column

**Files hint:**
- `docs/README.md`

## Normalization

Normalization changed nothing.

## Edits

This plan was edited 2 time(s) before approval; the log is `user_edited_plan.json`.

- version 2: `plan_split_task` by `cli`
- version 3: `plan_reorder` by `cli`
