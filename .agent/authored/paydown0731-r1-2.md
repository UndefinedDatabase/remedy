   Digest fallback (operator ruling 2026-07-31, F052-R3 precedent):
   when the reviewer's scratchpad originals are unavailable at
   review time (session tmp death, window restart), the transport
   proof falls back to recomputing sha256 over the COMMITTED
   .agent/authored/ files and comparing against the BEGIN-marker
   digests recorded in the reviewer's own emitted block; the verdict
   text states that the fallback was used, so the evidence chain
   stays honest. cmp-against-scratchpad remains the primary proof
   whenever the originals exist.
