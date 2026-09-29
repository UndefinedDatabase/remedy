// DECISIONS F042 D3 and D4 — one project context around every face of the cockpit: the project
// list loaded once per token, the opened job's own project loaded once per job, the ACTIVE
// project resolved by DECISION F042 D1's precedence, and a switch taken through the ONE gate
// that any other address change also advances, so a switch in flight never lands on a page the
// reader left by Back. `enterProject` takes the same gated path as `switchTo`, only replacing
// the address rather than pushing it, so the home grid's single-project skip never leaves a
// grid Back would only skip forward again to reach; `goHome` advances the gate to "" before
// asking the address to move, so a switch already in flight is dropped the same way any other
// address change drops one. Its context style follows `ReducedMotionProvider.tsx`: one default
// value, no throw for a reader outside the provider, because `RemedyApp.tsx` mounts exactly one.
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import { loadJobProject, loadProjectSummary, loadProjectsView } from "../../api/remedyApi";
import { createSwitchGate, resolveActiveProject, switchProject } from "../../api/projectScope";
import type {
  JobProject,
  ProjectEntry,
  ProjectsView,
  ProjectSummary,
  ProjectSwitch,
} from "../../api/projectScope";

export interface ProjectContextValue {
  view: ProjectsView | null;
  active: ProjectEntry | null;
  switchTo(slug: string): void;
  enterProject(slug: string): void;
  goHome(): void;
  readSummary(slug: string): Promise<ProjectSummary | null>;
}

const ProjectContext = createContext<ProjectContextValue>({
  view: null,
  active: null,
  switchTo: () => {},
  enterProject: () => {},
  goHome: () => {},
  readSummary: () => Promise.resolve(null),
});

export interface ProjectProviderProps {
  token: string;
  jobId: string;
  project: string;
  onSwitched: (result: ProjectSwitch, replace: boolean) => void;
  onHome: () => void;
  children: React.ReactNode;
}

export function ProjectProvider({ token, jobId, project, onSwitched, onHome, children }: ProjectProviderProps) {
  const [view, setView] = useState<ProjectsView | null>(null);
  const [jobProjectState, setJobProjectState] = useState<{ jobId: string; jobProject: JobProject | null }>({
    jobId: "",
    jobProject: null,
  });
  const gate = useRef(createSwitchGate(project));

  useEffect(() => {
    if (token === "") return;
    let cancelled = false;
    void loadProjectsView({ token }).then((loaded) => {
      if (!cancelled) setView(loaded);
    });
    return () => { cancelled = true; };
  }, [token]);

  useEffect(() => {
    if (jobId === "" || token === "") return;
    let cancelled = false;
    void loadJobProject({ jobId, token }).then((loaded) => {
      if (!cancelled) setJobProjectState({ jobId, jobProject: loaded });
    });
    return () => { cancelled = true; };
  }, [jobId, token]);

  useEffect(() => {
    if (gate.current.current() !== project) gate.current.begin(project);
  }, [project]);

  // The job's own project counts only while it still belongs to the CURRENT job: a pairing
  // fetched for an earlier `jobId` is dropped the moment the address moves on, even before its
  // own successor answer has arrived.
  const jobProject = jobProjectState.jobId === jobId ? jobProjectState.jobProject : null;
  const active = resolveActiveProject(view, project, jobProject);

  const readSummary = useCallback((slug: string): Promise<ProjectSummary | null> => {
    return loadProjectSummary({ project: slug, token });
  }, [token]);

  const switchTo = useCallback((slug: string): void => {
    void switchProject(slug, gate.current, readSummary, (result) => onSwitched(result, false));
  }, [readSummary, onSwitched]);

  const enterProject = useCallback((slug: string): void => {
    void switchProject(slug, gate.current, readSummary, (result) => onSwitched(result, true));
  }, [readSummary, onSwitched]);

  const goHome = useCallback((): void => {
    gate.current.begin("");
    onHome();
  }, [onHome]);

  const value = useMemo<ProjectContextValue>(
    () => ({ view, active, switchTo, enterProject, goHome, readSummary }),
    [view, active, switchTo, enterProject, goHome, readSummary],
  );

  return <ProjectContext.Provider value={value}>{children}</ProjectContext.Provider>;
}

export function useProjectContext(): ProjectContextValue {
  return useContext(ProjectContext);
}
