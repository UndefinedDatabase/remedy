// F044 T001 — the bar's routing rule (DECISION F044 D1). The fixtures live in
// `paletteRouting.goldens.json`, which `tests/ui_contracts/test_palette_contract.py` also reads and
// runs through the chat's own parse, so the two languages are held to the same lines.
import { describe, expect, it } from "vitest";
import { PALETTE_COMMANDS } from "./paletteCommands";
import {
  BAR_LEADING_VERBS,
  BAR_NOTE_OPENERS,
  BAR_QUESTION_WORDS,
  routeBarText,
} from "./paletteRouting";

// There is no `@types/node` in this workspace, so the node built-ins arrive through a dynamic
// import whose specifier is a variable, as `costMetric.test.ts` reads its source.
const FS_MODULE = "node:fs";
const URL_MODULE = "node:url";
type FsModule = { readFileSync: (path: string, encoding: string) => string };
type UrlModule = { fileURLToPath: (url: URL) => string };

interface RoutingGolden {
  text: string;
  focused: string;
  route: "none" | "chat" | "command" | "palette";
  command: string;
}

async function goldens(): Promise<RoutingGolden[]> {
  const fs = (await import(FS_MODULE)) as FsModule;
  const url = (await import(URL_MODULE)) as UrlModule;
  const path = url.fileURLToPath(new URL("./paletteRouting.goldens.json", import.meta.url));
  return JSON.parse(fs.readFileSync(path, "utf8")) as RoutingGolden[];
}

describe("routeBarText over the goldens", () => {
  it("routes every golden line to its golden route", async () => {
    const rows = await goldens();
    expect(rows.length).toBeGreaterThan(0);
    for (const row of rows) {
      const want = row.route === "command" ? { kind: "command", command: row.command } : { kind: row.route };
      expect(routeBarText(row.text, row.focused), JSON.stringify(row.text)).toEqual(want);
    }
  });

  it("holds a command golden for every leading verb, every note opener and 'run again'", async () => {
    const lines = (await goldens())
      .filter((row) => row.route === "command")
      .map((row) => row.text.replace(/\s+/g, " ").trim().toLowerCase());
    for (const opener of [...Object.keys(BAR_LEADING_VERBS), ...BAR_NOTE_OPENERS, "run again"]) {
      expect(lines.some((line) => line === opener || line.startsWith(`${opener} `) || line.startsWith(`${opener}:`)), opener).toBe(true);
    }
  });

  it("holds a golden for each tie-break: a question over a verb, and a verb only as a whole word", async () => {
    const byText = new Map((await goldens()).map((row) => [`${row.text}|${row.focused}`, row.route]));
    expect(byText.get("stop?|")).toBe("chat");
    expect(byText.get("can you stop the job|")).toBe("chat");
    expect(byText.get("stopwatch|")).toBe("palette");
    expect(byText.get("island map|")).toBe("palette");
  });
});

describe("the routing tables", () => {
  it("are the chat's words, in the chat's order", () => {
    expect(BAR_QUESTION_WORDS).toEqual([
      "what", "why", "how", "when", "where", "which", "who", "did", "does", "do",
      "is", "are", "was", "were", "can", "could", "has", "have",
    ]);
    expect(BAR_NOTE_OPENERS).toEqual(["tell the builder", "tell it", "note", "steer"]);
    expect(BAR_LEADING_VERBS).toEqual({
      stop: "job.stop", cancel: "job.stop", abort: "job.stop",
      pause: "job.pause",
      resume: "job.unpause", unpause: "job.unpause", continue: "job.unpause",
      veto: "job.veto-task", skip: "job.veto-task", drop: "job.veto-task",
      rerun: "job.rerun-subtree", retry: "job.rerun-subtree",
    });
  });

  it("never route to a command the palette cannot send itself", () => {
    const sendable = new Set(PALETTE_COMMANDS.filter((entry) => entry.flow === "send").map((entry) => entry.command));
    for (const command of [...Object.values(BAR_LEADING_VERBS), "job.steer", "chat.send"]) {
      expect(sendable.has(command), command).toBe(true);
    }
  });
});

describe("routeBarText on its own", () => {
  it("reads only the table's own words, never a prototype member", () => {
    expect(routeBarText("toString", "")).toEqual({ kind: "palette" });
    expect(routeBarText("constructor now", "")).toEqual({ kind: "palette" });
  });

  it("reads a question mark at the end after trimming", () => {
    expect(routeBarText("pause ?  ", "")).toEqual({ kind: "chat" });
  });
});
