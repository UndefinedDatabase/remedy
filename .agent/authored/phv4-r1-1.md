**Paste-block format (PH v4, operator ruling 2026-07-28):** the paste
block is ALWAYS the LAST content of the reply — nothing after it,
ever; recaps and notes go before it. The ENTIRE block is emitted
inside a fenced code block so no markdown renderer on the relay path
can mutate its bytes (PH v3 lesson: an unfenced emission had heading
markers, blockquote markers and leading indentation stripped in
transit — every authored hash in it broke). The FIRST line inside the
fence is the single top separator, exactly:
━━━━━━━━━━━━━━━━━━━━ ✂ PROMPT — copy everything below ━━━━━━━━━━━━━━━━━━━━
Copy starts on the NEXT line; the separator's glyphs never touch the
copied bytes. There is NO bottom delimiter — the block ends at the
closing fence, which is unambiguous because nothing may follow the
block. SEPARATOR LINE ONLY — never side borders or per-line
prefixes: any character added to a content line becomes part of the
copied bytes and breaks every sha256 in the block. Authored texts
appear ONLY inside that single block, exactly once per reply;
rendering an authored text or the block region twice in one reply is
a defect of the reply, treated like a transport fault (F251-R3
lesson: a duplicated, truncated render broke an authored hash
unrecoverably).
