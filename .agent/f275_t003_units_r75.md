# F275 T003 — a SITE and a LINE are different units, and DECISION F275 D48 is corrected

> Measured by the reviewer at `dac50bcd`, this round's base. The coverage reading runs in the
> PRIMARY CHECKOUT and writes no tracked file; the mutations run in a disposable `git worktree`
> under the gitignored `.remedy-wt/` that the instrument itself creates and removes.
> THIS FILE RECORDS A MEASUREMENT; IT FLIPS NOTHING. No line under `packages/`, `apps/`,
> `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
>
> PROVENANCE, STATED AS A SHAPE. EVERY INDENTED LINE IN THIS FILE is a verbatim excerpt of the
> output of the committed instrument `.agent/authored/f275-r75-witness.py.md`, which is what
> this round's gate runs. Every figure in the PROSE that the instrument does not print is a
> CITATION of a named decision, finding, round or section, and names its source in the sentence
> that uses it — including the three numerals this file QUOTES from DECISION F275 D48 in order
> to correct them, which it USES nowhere. No line carrying a wall-clock duration is quoted
> anywhere in this file.

## 1. The defect, which the round 74 worker found and this round measures

COVERAGE RESOLVES A CONTEXT PER LINE. The ruled set is keyed per SITE — path, line, column and
attribute — and several ruled sites can share one line. Round 74's instrument printed a SITE
count in its first section and a LINE distribution in its third, named neither, and DECISION
F275 D48 then restated the two as though they were one number: it says the distribution runs
"over all 176 at once", gives "98 by ten or more", and totals "7065 site-and-test pairs".

THE WORKER CAUGHT IT BY ARITHMETIC, not by reading the prose: round 74's buckets summed to
fewer than its own site total, which is the kind of check a document cannot pass by accident.
D48's two LOAD-BEARING readings — the risk set and the thin set — were unaffected, and section
3 below shows why. The three numerals were not.

## 2. Both units, printed, with the arithmetic visible

          production SITES refused                         :   175
          distinct LINES they sit on                       :   166
          SITES sharing a line with another site           :     9
          A witness count is a property of a LINE, so the buckets below count LINES.
          witnessed by zero         :     0 lines, carrying     0 sites
          witnessed by one          :    11 lines, carrying    11 sites
          witnessed by two to nine  :    58 lines, carrying    60 sites
          witnessed by ten or more  :    97 lines, carrying   104 sites
          the bucket LINE counts sum to                    :   166
          the bucket SITE counts sum to                    :   175
          median witnesses per LINE                        :    17
          total (line, test) witness pairs                 :  6966

EVERY COUNT NOW SAYS WHICH UNIT IT IS IN, and both sums are printed so the arithmetic is
visible rather than assumed. The corrected figures are 175 sites on 166 lines; 97 lines
carrying 104 sites witnessed by ten or more tests; and 6966 LINE-and-test pairs, which is what
the instrument has always computed and D48 called site-and-test pairs.

## 3. Why the ruling survives its own wrong numerals

          the risk set holds                               : 0 lines, carrying 0 sites
          the thin set holds                               : 11 lines, carrying 11 sites
          thin sites whose single witness really catches the rename: 11 of 11

THE TWO READINGS D48 TURNS ON ARE THE SAME IN BOTH UNITS, and that is not luck — it is the
reason the correction is a correction rather than a retraction. A line with no witness would
carry sites with no witness, and there are none; the eleven thin LINES happen to carry exactly
eleven SITES, so "the eleven thin sites" was right as written. Every one of the eleven is still
red-proved against its own single witness. D48's discharge of DECISION F275 D45's precondition
therefore stands on the readings it actually rests on.

## 4. What DECISION F275 D49 records

D48 IS NOT REWRITTEN. The record is append-only and item 20 of
`docs/agents/planner_reviewer_prompt.md` §3 forbids repairing a landed sentence; a dated
correction beside a wrong paragraph is worth more to a later reader than a clean paragraph
with no history. D49 states the three corrected numerals, states that the unit distinction is
now printed by the instrument, and states that the ruling is unchanged.

`R-0880` STAYS OPEN. The guard is still silent on 277 ruled sites, and nothing here narrows
that. The id-SHAPE seam DECISION F275 D37 routed into T003's resolver collapse is still
production work no round has started.
