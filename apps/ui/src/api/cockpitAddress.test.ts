// F042 T002, DECISION F042 D3 — the reviewer's acceptance of the cockpit's address: what the
// page's own query string names, which face it opens, and the key a new project or a new job
// remounts the shell under. DECISION F042 D4 gave an address with only a token the home grid
// and added the address the way home writes.
import { describe, expect, it } from "vitest";
import {
  EMPTY_PROJECT_LINE,
  MISSING_ADDRESS_LINE,
  addressFromSearch,
  cockpitFaceOf,
  homeSearch,
  shellKeyOf,
} from "./cockpitAddress";

describe("addressFromSearch", () => {
  it("reads the job, the trimmed project and the token", () => {
    expect(addressFromSearch("?job=j1&project=%20alpha%20&token=t")).toEqual({ jobId: "j1", project: "alpha", token: "t" });
  });

  it("still reads the older job_id, and job before it", () => {
    expect(addressFromSearch("?job_id=old&token=t").jobId).toBe("old");
    expect(addressFromSearch("?job_id=old&job=new&token=t").jobId).toBe("new");
  });

  it("reads every absent part as the empty string", () => {
    expect(addressFromSearch("")).toEqual({ jobId: "", project: "", token: "" });
  });
});

describe("cockpitFaceOf", () => {
  it("opens a job's cockpit whenever the address names a job and a token", () => {
    expect(cockpitFaceOf({ jobId: "j1", project: "", token: "t" })).toBe("job");
    expect(cockpitFaceOf({ jobId: "j1", project: "alpha", token: "t" })).toBe("job");
  });

  it("opens the empty project for a project with no job", () => {
    expect(cockpitFaceOf({ jobId: "", project: "alpha", token: "t" })).toBe("empty_project");
  });

  it("says the address is missing without a token, whatever else it names", () => {
    expect(cockpitFaceOf({ jobId: "j1", project: "alpha", token: "" })).toBe("missing");
    expect(cockpitFaceOf({ jobId: "", project: "", token: "" })).toBe("missing");
  });

  it("opens the home grid for a token with neither a job nor a project", () => {
    expect(cockpitFaceOf({ jobId: "", project: "", token: "t" })).toBe("home");
  });

  it("words both faces that have no job", () => {
    expect(MISSING_ADDRESS_LINE).toBe("Missing job or token in the URL.");
    expect(EMPTY_PROJECT_LINE).toBe("This project has no jobs yet.");
  });
});

describe("shellKeyOf", () => {
  it("changes with the project and with the job, and with nothing else", () => {
    const base = { jobId: "j1", project: "alpha", token: "t" };
    expect(shellKeyOf(base)).toBe(shellKeyOf({ ...base, token: "other" }));
    expect(shellKeyOf(base)).not.toBe(shellKeyOf({ ...base, project: "beta" }));
    expect(shellKeyOf(base)).not.toBe(shellKeyOf({ ...base, jobId: "j2" }));
  });

  it("never lets one project and job pair collide with another", () => {
    expect(shellKeyOf({ jobId: "b", project: "a|", token: "" })).not.toBe(shellKeyOf({ jobId: "|b", project: "a", token: "" }));
    expect(shellKeyOf({ jobId: "", project: "ab", token: "" })).not.toBe(shellKeyOf({ jobId: "b", project: "a", token: "" }));
  });
});

describe("homeSearch", () => {
  it("drops the project and every job-scoped parameter and keeps the rest in place", () => {
    expect(homeSearch("?token=t&project=beta&job=b1&theme=x&focus=n1&level=2&tab=diff&job_id=b1"))
      .toBe("?token=t&theme=x");
  });

  it("answers the empty string for an address left with nothing", () => {
    expect(homeSearch("?project=beta&job=b1")).toBe("");
  });

  it("opens the home face from the address it writes", () => {
    expect(cockpitFaceOf(addressFromSearch(homeSearch("?token=t&project=beta&job=b1")))).toBe("home");
  });
});
