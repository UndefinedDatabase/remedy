import { describe, it, expect } from "vitest";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { NonceRandomSource } from "./decisionNonce";
import { isUsableCommandNonce } from "./decisionAnswer";

/** The prefix every nonce this browser mints carries. It is spelled out here
 *  rather than imported because the module keeps it private on purpose: a test
 *  that reads the constant would pass whatever the constant became, and this
 *  literal is what pins the value an operator's control directory will show. */
const BROWSER_PREFIX = "ui-";

/** The longest nonce the server's class permits. Stated here as a NUMBER the
 *  test owns, so a change to the module's own ceiling has to be argued for
 *  rather than silently agreed with. */
const CLASS_LENGTH_CEILING = 64;

/** A source that RECORDS how often it was asked. The recorded count IS the
 *  "exactly once" assertion, and no global is touched to obtain it. */
function countingSource(answer: string) {
  const calls: number[] = [];
  const source: NonceRandomSource = () => {
    calls.push(calls.length);
    return answer;
  };
  return { calls, source };
}

/** A source that answers one fixed string, for the tests that care about the
 *  value rather than the call. */
function fixedSource(answer: string): NonceRandomSource {
  return () => answer;
}

describe("mintDecisionClientNonce", () => {
  it("mints a nonce the server's own predicate accepts, from a well-formed source", () => {
    const nonce = mintDecisionClientNonce(fixedSource("3f2b1c4d5e6f"));
    expect(nonce).not.toBeNull();
    expect(isUsableCommandNonce(nonce)).toBe(true);
  });

  it("marks the nonce as this browser's by carrying the prefix", () => {
    const nonce = mintDecisionClientNonce(fixedSource("3f2b1c4d5e6f"));
    expect(nonce).toBe(`${BROWSER_PREFIX}3f2b1c4d5e6f`);
  });

  it("asks the random source EXACTLY ONCE, so one call is one nonce", () => {
    const { calls, source } = countingSource("3f2b1c4d5e6f");
    mintDecisionClientNonce(source);
    expect(calls).toHaveLength(1);
  });

  it("keeps every character the server's class permits, letters, digits, underscore and dash alike", () => {
    expect(mintDecisionClientNonce(fixedSource("a1_B-9"))).toBe(
      `${BROWSER_PREFIX}a1_B-9`,
    );
  });

  it("drops every character outside the server's class and mints from what is left", () => {
    expect(mintDecisionClientNonce(fixedSource("a b/c!d"))).toBe(
      `${BROWSER_PREFIX}abcd`,
    );
  });

  it("answers null when the source's answer is entirely outside the class, because nothing is left to mint from", () => {
    expect(mintDecisionClientNonce(fixedSource("!!! /// ???"))).toBeNull();
  });

  it("answers null for an empty source, because an empty answer sanitises to nothing", () => {
    expect(mintDecisionClientNonce(fixedSource(""))).toBeNull();
  });

  it("cuts a very long source to a nonce the class still accepts", () => {
    const nonce = mintDecisionClientNonce(fixedSource("a".repeat(200)));
    expect(nonce).not.toBeNull();
    expect(isUsableCommandNonce(nonce)).toBe(true);
    expect((nonce as string).length).toBeLessThanOrEqual(CLASS_LENGTH_CEILING);
  });

  it("answers two DIFFERENT nonces for two DIFFERENT sources, which forbids a hidden constant", () => {
    const first = mintDecisionClientNonce(fixedSource("alpha1"));
    const second = mintDecisionClientNonce(fixedSource("bravo2"));
    expect(first).not.toBeNull();
    expect(second).not.toBeNull();
    expect(first).not.toBe(second);
  });
});
