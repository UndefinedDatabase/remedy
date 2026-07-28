11. Authored `.agent` state texts satisfy the repo's own `.agent`
    contract tests (PH v3): every authored `.agent/live_review.md`
    reset/replacement carries a `## Steps` section (the tests assert
    the substring "Steps"), and every authored `.agent/plan.md` text
    keeps `## Goal` plus a `## Next Steps` heading — so
    reviewer-authored state never turns contract tests red as a side
    effect (F251 D4 lesson: authored texts flipped four contract
    tests in both directions across rounds). The D4 design question
    itself — fixture-based vs live-coupled — stays with F252.
