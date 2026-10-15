// amend1015 P4.1: what each rail button opens. Before this, six of the seven icons had no
// action at all. Each now opens a panel that already exists and works, and a button whose
// panel the mount does not hand over is not rendered — no inert control is left on screen.

/** DECISION F042 D5 (3): Overview's tooltip, as the dock has always said it. */
export const OVERVIEW_TITLE = "All projects";

/** The rail's buttons, top to bottom. */
export const RAIL_KEYS = ["Overview", "Checks", "Activity", "Files", "History", "Docs", "Settings"] as const;
export type RailKey = (typeof RAIL_KEYS)[number];

/** The panels the shell can open from the rail, and which one is open now. */
export interface RailActions {
  onChecks?: () => void;
  onActivity?: () => void;
  onFiles?: () => void;
  onHistory?: () => void;
  onDocs?: () => void;
  onSettings?: () => void;
  active?: RailKey | null;
}

export interface RailItem {
  key: RailKey;
  title: string;
  onClick: () => void;
  active: boolean;
}

// Each button's tooltip names the panel it opens, so the icon is never the only clue.
const TITLES: Record<RailKey, string> = {
  Overview: OVERVIEW_TITLE,
  Checks: "Plan: the job's tasks and their checks",
  Activity: "Activity: what the agents did",
  Files: "Results: the changed files and the diff",
  History: "Story: how this job unfolded",
  Docs: "Terms: what every word on this page means",
  Settings: "System details",
};

/** The rendered buttons: Overview always (it goes home), every other key only with its action. */
export function railItemsOf(goHome: () => void, actions: RailActions = {}): RailItem[] {
  const handlers: Record<RailKey, (() => void) | undefined> = {
    Overview: goHome,
    Checks: actions.onChecks,
    Activity: actions.onActivity,
    Files: actions.onFiles,
    History: actions.onHistory,
    Docs: actions.onDocs,
    Settings: actions.onSettings,
  };
  const active = actions.active ?? "Overview";
  return RAIL_KEYS.flatMap((key) => {
    const onClick = handlers[key];
    return onClick === undefined ? [] : [{ key, title: TITLES[key], onClick, active: key === active }];
  });
}
