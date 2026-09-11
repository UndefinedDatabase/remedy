# F275 T003 — DECISION F275 D36's remedy is unavailable on this runtime, and the route that works

> Measured by the reviewer at `30072048`, this round's base, in the primary checkout, with
> no `git worktree` created and no suite run. THIS FILE RECORDS A MEASUREMENT; IT FLIPS
> NOTHING AND FIXES NOTHING. No line under `packages/`, `apps/`, `tests/`, `docs/` or
> `scripts/` moved in the round that wrote it. It replaces none of the earlier residue
> artefacts and corrects none of them: it corrects one paragraph of one DECISION, and it
> does that by appending a new decision rather than by editing the landed one.
>
> PROVENANCE. Every figure below is re-derived by the committed instrument
> `.agent/authored/f275-r64-route.py.md`, which is what this round's gate runs. There is
> no reviewer-only reading in this artefact.

## 1. What this round found, in one sentence

DECISION F275 D36 part three orders the descriptor probe's recorded key to gain
`col_offset`. A frame on this interpreter has no column to give, so that remedy cannot be
implemented as written — and a different recorded value, already present on every frame,
discriminates the class D36 bounded.

## 2. The runtime does not carry what D36 asks for

    python 3.10.12
    code objects carry co_positions (PEP 657, 3.11+): False
    positional attributes a frame carries: ['f_lasti', 'f_lineno']

Column information for a byte-code instruction arrived in CPython 3.11 with PEP 657, as
`code.co_positions()`. This interpreter is 3.10.12 and has no such method. The F275 R53
descriptor probe records `(owner, field, mode, path, LINE, function)` and takes its line
from `frame.f_lineno`; there is no `frame.f_col_offset` to take beside it, and there was
never going to be one. D36's part three is not wrong about the DEFECT — the key is one
discriminator short, exactly as it says — it is wrong about the discriminator that is
available.

## 3. `f_lasti` discriminates, on the real model, through the real walk

The instrument installs a descriptor of the F275 R53 probe's own shape over
`packages.core.models.Job.id`, a real pydantic field, and walks outward through frames
exactly as that probe does, keeping the CHOSEN frame's `f_lasti` beside its `f_lineno`.
Against one line holding two reads of the same attribute on two different receivers:

    Job.id read direct=True <file>:85 two_on_one_line() f_lasti=4
    Job.id read direct=True <file>:85 two_on_one_line() f_lasti=12
    reads 2   distinct (path, line, func) 1   distinct with f_lasti 2
    the offset DISCRIMINATES where the line does not: True

ONE key for two reads becomes TWO. That is the whole of the defect D36 named — "on 39
lines one proof ruled two receivers" — answered by a value the frame already carries.
The reading is taken through pydantic's own dispatch and the probe's own outward walk, not
against a toy class, because those two are precisely what made the earlier probe's frame
attribution hard.

## 4. The offset resolves back to a NAMED receiver

An offset is only useful if it can be joined to the static site set, which is keyed by
receiver. Disassembling the caller's code object and taking the last name-load instruction
at or before the recorded offset:

    f_lasti=4    -> receiver 'a'
    f_lasti=12   -> receiver 'b'
    receivers resolved in order ['a', 'b'] | source order ['a', 'b'] | MATCH True

## 5. How far that reaches over the 39 D36 bounded

    at-risk lines 39   ruled sites on them 78
    lines whose receiver-NAME set has more than one member: 39
    lines carrying the placeholder receiver '(expr)': 7

ALL 39 have receiver names that differ, which is not a lucky property but the definition
of the class: D36 built it as the line where two DIFFERENT receiver names share ONE owner
verdict. So a key carrying the receiver separates every one of the 39 by construction, and
the only question left is whether the receiver can be RECOVERED from an instruction offset.
Classifying every attribute node on those lines by the shape of its receiver expression:

| receiver expression | nodes |
|---|---:|
| a bare `Name` | 68 |
| a `Subscript` | 4 |
| a `Call` | 3 |
| an `Attribute` | 2 |

A bare name is what a single load instruction resolves. The other nine are not resolvable
that way and the route must REFUSE them rather than guess — which is the same obligation
`R-0880`'s fix clause already carries as its SECOND half, arriving from the other
direction. Named, because a refusal list that is not enumerated is not a refusal:

    tests/cli/test_self_dogfood_execution_cli.py:38 .id        Subscript
    tests/orchestration/test_loop_run.py:340 .id               Call
    tests/orchestration/test_loop_run.py:384 .id               Attribute
    tests/orchestration/test_loop_run.py:396 .id               Attribute
    tests/orchestration/test_repair_request_builder.py:69 .id  Call
    tests/orchestration/test_repair_request_builder.py:76 .id  Call
    tests/test_project_brain.py:262 .id                        Subscript
    tests/test_project_brain.py:297 .id                        Subscript
    tests/test_runner.py:133 .id                               Subscript

The instrument SORTS that list, because the ruled set it walks is a `set` and an unsorted
walk gives a different order in every process — a report a gate compares line by line has
to be the same report twice. Whether it succeeds is this round's G5(e), measured on the
committed blob rather than claimed here.

EVERY ONE OF THE NINE IS IN A TEST FILE. The four production lines D36 names are all in
the 68.

## 6. One line the site set and the source do not agree about

The table above counts 77 attribute nodes where the ruled set holds 78 sites, and the
instrument prints the one line they disagree on rather than reconciling the totals:

    packages/orchestration/long_run_executor.py:504 .id
      ruled sites 2   ast nodes 1   site cols [19, 40]   node value cols [30]

The source line is `return QueuePull(entry_id=entry.id, status=QUEUE_PULL_PLANNED,` and it
carries ONE `.id` attribute. The ruled set holds TWO sites on it. That is not the same
defect as D36's — D36's is one proof covering two real sites, and this is a site with no
attribute node under it at all — and this artefact does NOT diagnose it. It is reported
because `long_run_executor.py:504` is one of the four frames round 61's run reached and
D36 named by hand, so the line that motivated the bound is also the line where the set's
own arithmetic does not close.

## 7. What this settles, and what it does not

SETTLED: D36's part-three remedy is unimplementable on this interpreter, and the class it
was meant to resolve is resolvable by `f_lasti` plus a disassembly, on the real model,
over 68 of the 77 nodes on the 39 lines, with the remaining nine enumerated and all of
them in tests.

NOT SETTLED, and stated rather than implied. THE RE-DERIVATION IS NOT PERFORMED HERE. This
round measured the route; spending it means modifying the committed probe, running the
suite under it twice, and rebuilding the site set — which is a round of its own and is
what the plan now orders next. The nine refusals are enumerated but not decided: whether
they are struck, resolved by hand, or left to the transform's refusal is the next round's
question and not this one's. The `long_run_executor.py:504` disagreement of section 6 is
reported and NOT diagnosed. And nothing here touches `R-0880`, which stays open with both
of its obligations exactly where DECISION F275 D36 left them.
