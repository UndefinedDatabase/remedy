import { describe, it, expect } from "vitest";
import { ACTUAL_BASIS } from "./costMetric";
import {
  JOB_DIGEST_VERSION,
  decodeJobDigest,
  digestCostLine,
  jobDigestPath,
} from "./jobDigest";

// A well-formed envelope, shaped after the stored goldens under
// `tests/orchestration/fixtures/job_digest/golden/` so the fixture and the wire
// cannot drift apart in this file's imagination.
const envelope = {
  version: JOB_DIGEST_VERSION,
  job_id: "abc-123",
  state: "completed",
  headline: "The run is completed and its terminal status is all_green.",
  cost: { value: "not-measured", basis: "absent" },
  ownership: [] as string[],
  decisions: { open_count: 0, peak_urgency: 0 },
  primary_action: { label: "Review and merge the branch", rule_id: "all-green" },
};

describe("decodeJobDigest", () => {
  it("decodes every field of a well-formed envelope", () => {
    const digest = decodeJobDigest(envelope);
    expect(digest).not.toBeNull();
    expect(digest).toEqual(envelope);
  });

  it("carries the ownership sentences it is given, dropping non-strings", () => {
    const digest = decodeJobDigest({
      ...envelope,
      ownership: ["Builder owns two tasks", 7, null, "Reviewer owns one"],
    });
    expect(digest?.ownership).toEqual([
      "Builder owns two tasks",
      "Reviewer owns one",
    ]);
  });

  it("answers null for a payload that is not a plain object", () => {
    expect(decodeJobDigest(null)).toBeNull();
    expect(decodeJobDigest(undefined)).toBeNull();
    expect(decodeJobDigest("a digest")).toBeNull();
    expect(decodeJobDigest(7)).toBeNull();
    expect(decodeJobDigest([envelope])).toBeNull();
  });

  it("answers null when job_id is missing or is not a string", () => {
    const { job_id, ...withoutJobId } = envelope;
    expect(job_id).toBe("abc-123");
    expect(decodeJobDigest(withoutJobId)).toBeNull();
    expect(decodeJobDigest({ ...envelope, job_id: 42 })).toBeNull();
    expect(decodeJobDigest({ ...envelope, job_id: null })).toBeNull();
  });

  it("answers null for a version this client does not understand", () => {
    expect(decodeJobDigest({ ...envelope, version: JOB_DIGEST_VERSION + 1 })).toBeNull();
    expect(decodeJobDigest({ ...envelope, version: "1" })).toBeNull();
    const { version, ...withoutVersion } = envelope;
    expect(version).toBe(JOB_DIGEST_VERSION);
    expect(decodeJobDigest(withoutVersion)).toBeNull();
  });

  it("IGNORES an unknown extra key rather than rejecting the envelope", () => {
    // The server may add a field before this client learns it, and DECISION
    // F040 D3's own reasoning is that an additive field needs no version bump.
    const digest = decodeJobDigest({ ...envelope, deep_link: "/jobs/abc-123" });
    expect(digest).toEqual(envelope);
    expect(digest).not.toHaveProperty("deep_link");
  });

  it("reads a missing section as a complete one full of absences", () => {
    const digest = decodeJobDigest({
      version: JOB_DIGEST_VERSION,
      job_id: "abc-123",
    });
    expect(digest).toEqual({
      version: JOB_DIGEST_VERSION,
      job_id: "abc-123",
      state: "",
      headline: "",
      cost: { value: "", basis: "" },
      ownership: [],
      decisions: { open_count: 0, peak_urgency: 0 },
      primary_action: { label: "", rule_id: "" },
    });
  });

  it("never throws on a hostile payload", () => {
    const hostile: Record<string, unknown> = {
      version: JOB_DIGEST_VERSION,
      job_id: "abc-123",
      cost: "not an object",
      decisions: { open_count: Number.NaN, peak_urgency: -3 },
      primary_action: [],
      ownership: "not an array",
    };
    const digest = decodeJobDigest(hostile);
    expect(digest?.cost).toEqual({ value: "", basis: "" });
    expect(digest?.decisions).toEqual({ open_count: 0, peak_urgency: 0 });
    expect(digest?.ownership).toEqual([]);
    expect(digest?.primary_action).toEqual({ label: "", rule_id: "" });
  });
});

describe("digestCostLine", () => {
  it("treats the exactness string as exact THROUGH the imported constant", () => {
    // THE POINT OF THIS FILE. The basis is not retyped here: it is the same
    // binding `costMetric.ts` exports and the metrics bar reads, so the day the
    // server renames that value this test moves with it instead of pinning the
    // old name (DECISION F040 D2's drift, one layer up).
    const line = digestCostLine({ value: "$1.20", basis: ACTUAL_BASIS });
    expect(line).toEqual({ value: "$1.20", estimated: false });
  });

  it("marks an absent basis as an estimate", () => {
    expect(digestCostLine({ value: "not-measured", basis: "absent" }).estimated).toBe(true);
  });

  it("marks a lower_bound basis as an estimate", () => {
    expect(digestCostLine({ value: "$0.40", basis: "lower_bound" }).estimated).toBe(true);
  });

  it("marks an unknown basis as an estimate, because unknown provenance is not an actual", () => {
    expect(digestCostLine({ value: "$9.99", basis: "" }).estimated).toBe(true);
    expect(digestCostLine({ value: "$9.99", basis: "ACTUAL" }).estimated).toBe(true);
  });

  it("carries the figure's own text unchanged and composes no words", () => {
    const line = digestCostLine({ value: "1.2M tokens", basis: "absent" });
    expect(line.value).toBe("1.2M tokens");
  });
});

describe("jobDigestPath", () => {
  const request = { jobId: "abc-123", token: "t0k" };

  it("addresses the job's digest endpoint", () => {
    expect(jobDigestPath(request)).toBe("/api/jobs/abc-123/digest?token=t0k");
  });

  it("percent-encodes the token and the job id, so neither can add a parameter or a segment", () => {
    const path = jobDigestPath({ jobId: "job/7", token: "a&b=c" });
    expect(path).toBe("/api/jobs/job%2F7/digest?token=a%26b%3Dc");
    expect(path).not.toContain("job/7");
    expect(path.split("&")).toHaveLength(1);
  });

  it("prefixes an explicit baseUrl and stays relative without one", () => {
    expect(jobDigestPath({ ...request, baseUrl: "http://127.0.0.1:8123" })).toBe(
      "http://127.0.0.1:8123/api/jobs/abc-123/digest?token=t0k",
    );
    expect(jobDigestPath(request).startsWith("/api/")).toBe(true);
  });
});
