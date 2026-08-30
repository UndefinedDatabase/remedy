import { describe, it, expect } from "vitest";
import { browserDigestVisibilityPort } from "./browserDigestPort";

/** A small fake satisfying the `Storage` slice `browserDigestPort.ts` actually
 *  requires — `getItem`/`setItem` backed by a `Map`. This package ships no DOM
 *  testing library, so this is the smallest fake that lets the module's real
 *  code run rather than a mock of its behaviour. */
function fakeStorage(seed: Record<string, string> = {}): Pick<Storage, "getItem" | "setItem"> {
  const map = new Map<string, string>(Object.entries(seed));
  return {
    getItem(key: string): string | null {
      return map.has(key) ? (map.get(key) as string) : null;
    },
    setItem(key: string, value: string): void {
      map.set(key, value);
    },
  };
}

describe("browserDigestVisibilityPort and dismissal", () => {
  it("a written dismissal reads back exactly, for one job", () => {
    const port = browserDigestVisibilityPort(fakeStorage());
    port.writeDismissal("job-1", 1_700_000_000_000);
    expect(port.readDismissal("job-1")).toBe(1_700_000_000_000);
  });
});

describe("browserDigestVisibilityPort and last-seen", () => {
  it("a written last-seen reads back exactly, for one job", () => {
    const port = browserDigestVisibilityPort(fakeStorage());
    port.writeLastSeen("job-1", 1_700_000_001_000);
    expect(port.readLastSeen("job-1")).toBe(1_700_000_001_000);
  });
});

describe("browserDigestVisibilityPort and job isolation", () => {
  it("two different job ids' dismissals do not collide", () => {
    const port = browserDigestVisibilityPort(fakeStorage());
    port.writeDismissal("job-1", 1_700_000_000_000);
    expect(port.readDismissal("job-2")).toBeNull();
    port.writeDismissal("job-2", 1_700_000_002_000);
    expect(port.readDismissal("job-1")).toBe(1_700_000_000_000);
    expect(port.readDismissal("job-2")).toBe(1_700_000_002_000);
  });

  it("two different job ids' last-seen instants do not collide", () => {
    const port = browserDigestVisibilityPort(fakeStorage());
    port.writeLastSeen("job-1", 1_700_000_000_000);
    expect(port.readLastSeen("job-2")).toBeNull();
    port.writeLastSeen("job-2", 1_700_000_002_000);
    expect(port.readLastSeen("job-1")).toBe(1_700_000_000_000);
    expect(port.readLastSeen("job-2")).toBe(1_700_000_002_000);
  });
});

describe("browserDigestVisibilityPort and concern isolation", () => {
  it("a job's own dismissal and its own last-seen do not collide", () => {
    const port = browserDigestVisibilityPort(fakeStorage());
    port.writeDismissal("job-1", 1_700_000_000_000);
    expect(port.readLastSeen("job-1")).toBeNull();
    port.writeLastSeen("job-1", 1_700_000_003_000);
    expect(port.readDismissal("job-1")).toBe(1_700_000_000_000);
    expect(port.readLastSeen("job-1")).toBe(1_700_000_003_000);
  });
});

describe("browserDigestVisibilityPort and absence", () => {
  it("reading a key that was never written answers null", () => {
    const port = browserDigestVisibilityPort(fakeStorage());
    expect(port.readDismissal("job-never")).toBeNull();
    expect(port.readLastSeen("job-never")).toBeNull();
  });

  it("reading a key whose stored value does not parse to a finite number answers null", () => {
    const port = browserDigestVisibilityPort(
      fakeStorage({ "remedy:digest:dismissal:job-1": "not-a-number" }),
    );
    expect(port.readDismissal("job-1")).toBeNull();
  });

  it("a numeric string round-trips through the same read path exactly (positive control)", () => {
    const port = browserDigestVisibilityPort(
      fakeStorage({ "remedy:digest:dismissal:job-1": "1700000000000" }),
    );
    expect(port.readDismissal("job-1")).toBe(1_700_000_000_000);
  });
});
