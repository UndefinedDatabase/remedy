import { describe, expect, it } from "vitest";
import { STEERING_ACK_EVENT, readSteeringAck, steeringAckLine } from "./steeringAck";

const UNDERSTOOD = "the builder follows “Use pnpm.” from round 2 of task task-1 on";

function envelope(steering: unknown, event: string = STEERING_ACK_EVENT) {
  return { event, seq: 3, steering };
}

describe("readSteeringAck", () => {
  it("reads the three fields the stream carries", () => {
    expect(readSteeringAck(envelope({
      message_id: "sm-0001", round_number: 2, understood: UNDERSTOOD,
    }))).toEqual({ messageId: "sm-0001", roundNumber: 2, understood: UNDERSTOOD });
  });

  it("answers null for any other kind, even one carrying the field", () => {
    expect(readSteeringAck(envelope({
      message_id: "sm-0001", round_number: 2, understood: UNDERSTOOD,
    }, "steering_message_received"))).toBeNull();
  });

  it("answers null for a missing or malformed field rather than inventing a round", () => {
    expect(readSteeringAck(envelope(undefined))).toBeNull();
    expect(readSteeringAck(envelope("sm-0001"))).toBeNull();
    expect(readSteeringAck(envelope({ message_id: "sm-0001", round_number: "2",
      understood: UNDERSTOOD }))).toBeNull();
    expect(readSteeringAck(envelope({ message_id: "sm-0001", round_number: 2.5,
      understood: UNDERSTOOD }))).toBeNull();
    expect(readSteeringAck(envelope({ message_id: "sm-0001", round_number: 2,
      understood: "" }))).toBeNull();
    expect(readSteeringAck(envelope({ round_number: 2, understood: UNDERSTOOD }))).toBeNull();
  });
});

describe("steeringAckLine", () => {
  it("names the round and quotes the restatement whole", () => {
    expect(steeringAckLine({ messageId: "sm-0001", roundNumber: 2, understood: UNDERSTOOD }))
      .toBe(`Steering taken in at round 2: ${UNDERSTOOD}.`);
  });
});
