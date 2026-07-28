12. Before diagnosing a relay gap ("the block never reached the
    worker"), read .agent/last_block.md and its git history. A
    recorded refusal means delivered-and-refused: re-emit CORRECTED
    bytes, never the same bytes, and never conclude "never delivered"
    while a refusal record exists (PH v3 lesson: three refused
    emissions left zero disk trace and the gap was misdiagnosed for
    three turns).
