// The decision inbox's CLIENT NONCE, minted here and nowhere else (T5_F031
// T003). Every other module in this chain CONSUMES a nonce the caller already
// holds — `decisionAnswer.ts` refuses one outside the server's class,
// `decisionSend.ts` carries it into the body, `decisionSubmit.ts` moves it —
// so until this file existed nothing in this browser could produce one, and an
// answer could be composed but never actually sent. This module is that one
// missing value and nothing besides.
//
// IT ANSWERS `null` RATHER THAN THROWING, because `null` is this feature's word
// for unsendable: `buildDecisionResolveCommand` and `buildDecisionSendRequest`
// already answer it for an empty job id, an empty token, a blank answer, a
// nonce outside the class and a decision that is not open. A caller that
// already branches on `null` gains no new shape from a minter that cannot mint,
// and a throw inside a click handler is an unhandled rejection. DECISION F031
// D17 rules that, and rules the two choices below.
//
// THE CLASS IS THE SERVER'S AND IT KEEPS EXACTLY ONE MIRROR IN THIS BROWSER.
// `decisionAnswer.ts` holds that mirror as `COMMAND_NONCE_PATTERN` — itself a
// copy of `safe_points._ID_RE`, reached through `nonce_is_valid` — and exports
// the predicate `isUsableCommandNonce` over it. This module imports that
// predicate and never restates the pattern: a second literal would be a second
// thing to keep in step with the server, and the value it guards becomes a
// FILENAME in the job's control directory, so a value outside the class is a
// path rather than an id.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// IT READS NO CLOCK. No timestamp in the value, no expiry, no elapsed time. A
// clock would make this module untestable without freezing one, and a nonce a
// reader can date is a nonce a reader will be tempted to order.
// IT KEEPS NO COUNTER AND NO STORAGE. Nothing is remembered between calls, so
// there is no `localStorage` key, no module-level mutable and nothing to clear
// when a tab is closed.
// IT CLAIMS NO UNIQUENESS OF ITS OWN. Two calls collide exactly when the
// injected source collides; this module adds a prefix, drops what the class
// forbids and cuts to length, and none of those three make a value more unique
// than it arrived. The default source is the browser's own
// `crypto.randomUUID`, and the uniqueness claim is that function's alone.
// IT KNOWS NOTHING ABOUT WHAT A DECISION OR A COMMAND IS. No card, no answer
// text, no job, no token, no request. It is handed no model and reaches for
// none, which is why it can be minted before the operator has chosen anything.
// IT OPENS NO SOCKET and sends nothing; `decisionSubmit.ts` is still the only
// module in this feature that touches the wire.
import { isUsableCommandNonce } from "./decisionAnswer";

/** THE TESTING SEAM: the one function that reaches for randomness, passed IN
 *  rather than reached for, the same shape DECISION F031 D16 fixed for the send.
 *  A test supplies its own source and never patches a global — no test under
 *  `apps/ui/src` patches one today, and a leaked global is a failure that
 *  surfaces in an unrelated file. */
export type NonceRandomSource = () => string;

/** What marks a nonce as MINTED BY THIS BROWSER rather than by the CLI or by a
 *  test fixture. It is deliberately short: the value it prefixes is a filename
 *  in the job's control directory and the class allows 64 characters in total,
 *  so every character spent here is one the source does not get. Its first
 *  character is a letter because the class requires the first character of the
 *  whole nonce to be alphanumeric. */
const BROWSER_NONCE_PREFIX = "ui-";

/** The longest nonce the server's class permits, counted in characters: one
 *  leading character and up to 63 more, so 64 is its ceiling. This is a LENGTH
 *  and nothing else — the character class itself is never restated in this
 *  file, and the final guard below is what actually decides. */
const MAX_COMMAND_NONCE_LENGTH = 64;

/** Whether ONE character is one the server's class would carry. Asked of the
 *  exported predicate rather than of a second regex, by probing the character
 *  inside the shortest nonce that could hold it: one leading letter, then the
 *  character. The leading letter is there only because the class constrains the
 *  FIRST position more tightly than the rest, and it is discarded — nothing but
 *  the predicate's verdict on `character` leaves this function. */
function isCommandNonceCharacter(character: string): boolean {
  return isUsableCommandNonce(`a${character}`);
}

/** THE MINTER: one call to the injected source becomes a nonce the commands
 *  endpoint accepts, or `null` when no such nonce can be built from what the
 *  source answered. The source is called EXACTLY ONCE, so a caller that needs
 *  two nonces calls this twice and neither call can be surprised by a retry.
 *
 *  It composes in three steps and then submits to the guard: the source's answer
 *  loses every character the class forbids; a source that sanitises away to
 *  nothing is unsendable and answers `null`; what is left is prefixed and cut to
 *  the class's length. `isUsableCommandNonce` has the LAST WORD on the composed
 *  value, so nothing this function builds can escape the rule the server
 *  enforces, however the steps above are later changed. */
export function mintDecisionClientNonce(
  randomSource: NonceRandomSource = () => crypto.randomUUID(),
): string | null {
  const sanitisedSource = Array.from(randomSource())
    .filter(isCommandNonceCharacter)
    .join("");
  if (sanitisedSource === "") {
    return null;
  }
  const nonce = `${BROWSER_NONCE_PREFIX}${sanitisedSource}`.slice(
    0,
    MAX_COMMAND_NONCE_LENGTH,
  );
  return isUsableCommandNonce(nonce) ? nonce : null;
}
