# Execution Guard — what stage 1 does NOT prevent

## Overview

F085 stage 1 gives builder-spawned commands POSIX resource limits, a wall timeout, output
caps, a pinned cwd, an environment allowlist over a forbidden-key floor, and a default-deny
network posture. This document states the non-guarantees, because a guard trusted past its
evidence is worse than no guard: the code deliberately declines to call any of this
containment.

## The network posture is a PROXY posture, never a kernel one

`deny_network` points a child's proxy variables — both spellings, plus an empty `NO_PROXY` so
no host is exempt — at `http://127.0.0.1:9`, the RFC 863 discard port, where nothing listens
and a connect is refused at once.

- A toolchain that HONOURS proxy variables cannot reach the network. Measured: a guarded child
  is refused against a loopback server that is really listening, while the same child without
  the posture is served.
- A binary that IGNORES them reaches the network anyway. Static Go binaries, anything using
  raw sockets, and most things speaking a non-HTTP protocol are in that set.
- Nothing here blocks DNS, raw sockets, or a unix socket to a local daemon.

Kernel-level isolation is stage 2. Stage 1 raises the bar and reports honestly.

## Six classes run under the guard, and only three of them deny the network

Amendment F085 D1's table marks SIX classes stage-1 guarded: `builder`, `test`, `dod-process`,
`dod-app`, `runtime-server` and `runtime-build`. Being guarded and denying the network are
SEPARATE columns of that table. Only `builder`, `test` and `dod-process` default-deny. The
other three are guarded but keep network access, because the server classes are judged by an
HTTP readiness probe and `runtime-build` fetches from a package registry — so a guarded
command is not necessarily a command that cannot reach the network.

The `git` (24 sites), `packaging` (11) and `other` (8) classes are NOT stage-1 classes and
still spawn unsupervised, so a limit proved for a test command says nothing about a `git`
invocation. Their exclusion is a SCOPE ruling and NOT a safety claim: their argv is authored by
Remedy itself rather than supplied by a project, which is the problem this feature names. It
follows that several of those sites pass no timeout at all and can hang, and stage 1 does not
fix that.

## An allowlist bounds the PARENT, not the child's own runtime

Scrubbing decides what the parent hands over. It cannot decide what the child then adds to
itself: a CPython child sets `LC_CTYPE` during PEP 538 locale coercion, so a child's
environment is a SUPERSET of the scrubbed one. Tests subtract that key rather than crediting
the guard with producing it.

## Output caps bound what the guard READS

The cap applies to the child's stdout and stderr while the guard is reading them. An
application that writes its own log to a FILE takes no guard cap at all, and neither does
anything a child writes through a descriptor the guard never owned. Past the cap the guard
stops STORING and keeps COUNTING, so the reported byte totals stay honest while the stored
output is truncated.

## Limits that are enforced but not classified

`address_space_bytes` is enforced through RLIMIT_AS. A child that exceeds it has its mapping
refused, raises `MemoryError` and exits 1 with no signal, and its `ru_maxrss` stays below the
limit because the refused mapping never became resident. Nothing `wait4` reports distinguishes
that death from any other exit-1 failure, so the guard enforces the limit and declines to name
it in `tripped_limit`. Naming it would be an overclaim.

## There is no filesystem fence

The cwd is PINNED, which decides where a relative path lands. It does not stop a child writing
to an absolute path outside the worktree. A filesystem fence is stage 2.

## A stream still blocked at the grace deadline leaks

If a stream is still blocked when the grace deadline passes, one pipe read end and one daemon
thread survive the run. Closing that descriptor under a blocked reader risks the thread reading
a recycled descriptor after a later `open()`, so the leak is the deliberately chosen cheaper
wrong.

## Where the rules live

Policy per command class: `packages/orchestration/exec_guard.py`. The class table and the
staging plan: `docs/roadmap/features/T2_F085.md`.
