# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q18 — Two review folders in the checkout (2026-10-13, F306, round 9)

**What needs deciding.** At 23:13 on the thirteenth of October, two folders appeared directly in
the repository folder, while the loop was running the whole test collection. Both names begin with
remedy-review and the date of the eighth of July, and the second name ends in the number 2. They
look like an old review package, unpacked twice. The loop did not create them. Please decide whether they may be moved out of the repository folder.

**Why it matters.** The test collection reads every test it finds below the repository folder, so
it also tried to read the tests inside those folders. That run counted twelve failures that have
nothing to do with the code, so the loop has to run the whole collection again before this
clean-up can be accepted. The tidiness check also fails as long as the folders are there.

**My recommendation.** Move both folders, unchanged, to a folder outside the repository, for
example a folder named remedy-review-moved in your home folder. If you want to keep an unpacked
review package, unpack it outside the repository folder in future.

**What happens if you say nothing.** The next loop session moves both folders, unchanged, to the
folder remedy-review-moved in your home folder, writes that move down as a decision you can
reverse by moving them back, and then runs the whole test collection again.
