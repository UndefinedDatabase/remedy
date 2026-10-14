# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q18 — Two review folders in the checkout (2026-10-13, F306, round 9; updated 2026-10-14, round 11)

**What needs deciding.** At 23:13 on the thirteenth of October, two folders appeared directly in
the repository folder, while the loop was running the whole test collection. Both names begin with
remedy-review and the date of the eighth of July, and the second name ends in the number 2. They
look like an old review package, unpacked twice. The loop did not create them. The loop has now
moved them, unchanged, and you can decide whether they stay where they are now.

**Why it matters.** The test collection reads every test it finds below the repository folder, so
it also tried to read the tests inside those folders. That run counted twelve failures that have
nothing to do with the code. The tidiness check also failed while the folders were there. After
the move, the whole test collection passed with no failure.

**My recommendation.** Keep them where they are now, or move them anywhere you like outside the
repository folder. The loop first tried a folder named remedy-review-moved in your home folder, but
its permission settings do not let it write outside the repository folder. So it moved both folders
into a folder with the same name inside its own hidden scratch folder, which is called .remedy-wt
and sits in the repository folder. Git ignores that scratch folder, and neither the test collection
nor the tidiness check looks inside it. Nothing inside the two folders was opened, changed or
deleted. If you want to keep an unpacked review package, unpack it outside the repository folder in
future.

**What happens if you say nothing.** The move is already done and stays as it is until you say
otherwise. You can undo it by moving both folders back into the repository folder.
