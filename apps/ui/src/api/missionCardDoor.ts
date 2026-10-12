// The mission card's two doors (F305 T002, DECISION F305 D2), shaped like the project doors of
// `remedyApi.ts`: one injected fetcher, one decoder from `missionCard.ts`, and no throw. They live
// here rather than in `remedyApi.ts`, which is a row of `docs/system/structure-ledger-v1.md` and
// may not grow.
import { decodeMissionOrders, decodeProjectMissions, missionOrdersPath, projectMissionsPath } from "./missionCard";
import type { MissionOrders, ProjectMissions } from "./missionCard";

/** How a mission door reaches the network; a test hands each loader below a fake. */
export type MissionCardFetcher = (path: string) => Promise<unknown>;

/** The one network read of this module: a GET on the page's own origin, refused unless the
 *  server answered 2xx. */
async function fetchMissionCardJson(path: string): Promise<unknown> {
  const response = await fetch(path, { method: "GET", credentials: "same-origin" });
  if (!response.ok) throw new Error(`Request failed ${response.status}: ${path}`);
  return response.json();
}

/** Read a project's missions through the single door. NEVER THROWS: a failed read and an
 *  envelope the decoder refuses both answer `null`. */
export async function loadProjectMissions(
  request: { project: string; token: string; baseUrl?: string },
  fetchPayload: MissionCardFetcher = fetchMissionCardJson,
): Promise<ProjectMissions | null> {
  try {
    return decodeProjectMissions(await fetchPayload(projectMissionsPath(request)));
  } catch {
    return null;
  }
}

/** Read one mission's orders through the single door. NEVER THROWS: a failed read and an
 *  envelope the decoder refuses both answer `null`. */
export async function loadMissionOrders(
  request: { project: string; missionId: string; token: string; baseUrl?: string },
  fetchPayload: MissionCardFetcher = fetchMissionCardJson,
): Promise<MissionOrders | null> {
  try {
    return decodeMissionOrders(await fetchPayload(missionOrdersPath(request)));
  } catch {
    return null;
  }
}
