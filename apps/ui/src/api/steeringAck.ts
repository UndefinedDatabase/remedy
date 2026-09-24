// THE STEERING ACKNOWLEDGEMENT, as the cockpit shows it (T5_F264 T003, DECISION F264 D7).
//
// The stream's `steering_message_consumed` frame carries a `steering` field of exactly
// three values — the message id, the round it took effect from, and the restatement the
// server wrote (`ui_server._steering_ack_summary_payload`, DECISION F264 D6). This module
// reads that field, CHECKING every value because the envelope is parsed JSON from a server
// this client does not control, and turns it into the one line the activity feed shows.
// `remedy chat show` prints the same restatement from the same run-log event, so the CLI
// and the cockpit cannot disagree about what was understood or from which round.
//
// THE DELIBERATE ABSENCES. It renders nothing and knows no component. It never shortens
// the restatement: it quotes the operator's own words, and a cut quotation has been
// rewritten. A frame whose field is missing or malformed answers `null`, so the feed falls
// back to the catalog's plain line rather than inventing a round.

/** The kind of the frame that acknowledges a steering message. */
export const STEERING_ACK_EVENT = "steering_message_consumed";

/** One acknowledgement, as the stream carries it. */
export interface SteeringAck {
  messageId: string;
  roundNumber: number;
  understood: string;
}

/** The acknowledgement a frame's envelope carries, or `null` when it carries none. */
export function readSteeringAck(envelope: Record<string, unknown>): SteeringAck | null {
  if (envelope["event"] !== STEERING_ACK_EVENT) {
    return null;
  }
  const field = envelope["steering"];
  if (typeof field !== "object" || field === null) {
    return null;
  }
  const steering = field as Record<string, unknown>;
  const messageId = steering["message_id"];
  const roundNumber = steering["round_number"];
  const understood = steering["understood"];
  if (typeof messageId !== "string" || typeof understood !== "string" || understood === ""
      || typeof roundNumber !== "number" || !Number.isInteger(roundNumber)) {
    return null;
  }
  return { messageId, roundNumber, understood };
}

/** The line the activity feed shows for one acknowledgement: the round first, because it
 *  is the half an operator scans for, then the restatement, whole. */
export function steeringAckLine(ack: SteeringAck): string {
  return `Steering taken in at round ${ack.roundNumber}: ${ack.understood}.`;
}
