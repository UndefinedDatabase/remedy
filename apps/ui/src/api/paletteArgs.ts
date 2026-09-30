// T5_F044 T001, DECISION F044 D3 — the palette's argument flow: a command's own `args`, in
// `paletteCommands.ts`'s order, asked one at a time. A value is trimmed on the way in, since the
// record this flow builds is durable and edge space is noise no later reader asked for — the same
// rule `rerunSend.ts`'s own model trims by. A required argument answered blank refuses the answer
// outright; an optional one answered blank is recorded as no answer at all, since `paletteSend.ts`
// omits an absent key exactly as `buildRerunSubtreeRequest`'s own optional fields do. EVERY
// FUNCTION HERE IS PURE: `answerArg` never changes the flow it was given, and a fresh flow is
// handed back instead.
import type { PaletteArg, PaletteCommand } from "./paletteCommands";

/** One command's own walk through its arguments: which entry started it, what has been answered
 *  so far, and which argument comes next. */
export interface PaletteArgFlow {
  readonly entry: PaletteCommand;
  readonly values: Readonly<Record<string, string>>;
  readonly index: number;
}

/** A fresh flow over one command, its walk not yet begun. */
export function startArgFlow(entry: PaletteCommand): PaletteArgFlow {
  return { entry, values: {}, index: 0 };
}

/** The argument still to ask, or `null` once every one of the entry's arguments has an answer. */
export function currentArg(flow: PaletteArgFlow): PaletteArg | null {
  return flow.entry.args[flow.index] ?? null;
}

/** One answer, trimmed, becoming a FRESH flow one step further along — or `null` when there is no
 *  current argument to answer, or the current one is required and the trimmed answer is blank. An
 *  optional argument answered blank advances the flow without adding a key. */
export function answerArg(flow: PaletteArgFlow, value: string): PaletteArgFlow | null {
  const arg = currentArg(flow);
  if (arg === null) return null;
  const trimmed = value.trim();
  if (arg.required && trimmed === "") return null;
  const values = trimmed === "" ? { ...flow.values } : { ...flow.values, [arg.name]: trimmed };
  return { entry: flow.entry, values, index: flow.index + 1 };
}

/** Every one of the entry's arguments has an answer (or the entry asks none at all). */
export function argFlowComplete(flow: PaletteArgFlow): boolean {
  return flow.index >= flow.entry.args.length;
}
