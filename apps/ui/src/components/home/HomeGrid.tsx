// T5_F042 T003, DECISION F042 D4 — the home face: a grid of project cards, twelve to a page, a
// card opening its project; the single-project skip, entered once through the provider's
// `enterProject`; and the empty state's invite to `remedy init`. Every rule the cards draw on —
// paging, tone, cost words, the card's own shape — lives in `homeGrid.ts` and is not restated
// here.
import { useEffect, useRef, useState } from "react";
import { DEGRADED_LINE, NO_PROJECTS_LINE, homePage, projectCardOf } from "../../api/homeGrid";
import type { ProjectSummary } from "../../api/projectScope";
import { useProjectContext } from "../shell/ProjectProvider";
import styles from "./HomeGrid.module.css";

export const HOME_TITLE = "Projects";
export const HOME_LOADING_LINE = "Reading your projects…";

export function HomeGrid() {
  const { view, switchTo, enterProject, readSummary } = useProjectContext();
  const [page, setPage] = useState(1);
  const [summaries, setSummaries] = useState<Record<string, ProjectSummary | null>>({});
  const enteredRef = useRef<string | null>(null);

  const isSingle = view !== null && view.single_project && view.projects.length === 1;
  const singleSlug = isSingle ? view!.projects[0].slug : null;

  // The single-project skip: enters that project ONCE per slug, guarded by a ref rather than by
  // re-running the effect, so a re-render mid-flight never asks the provider twice.
  useEffect(() => {
    if (singleSlug === null) return;
    if (enteredRef.current === singleSlug) return;
    enteredRef.current = singleSlug;
    enterProject(singleSlug);
  }, [singleSlug, enterProject]);

  const pageResult = view !== null ? homePage(view.projects, page) : null;
  const slugsKey = pageResult ? pageResult.items.map((p) => p.slug).join("|") : "";

  // The page's summaries, read together and dropped through a `cancelled` flag: a page turned
  // before they arrive must never store an answer for a slug that is no longer on screen.
  useEffect(() => {
    if (pageResult === null || pageResult.items.length === 0) return;
    let cancelled = false;
    const slugs = pageResult.items.map((p) => p.slug);
    void Promise.all(
      slugs.map((slug) => readSummary(slug).then((summary): [string, ProjectSummary | null] => [slug, summary])),
    ).then((pairs) => {
      if (cancelled) return;
      setSummaries((prev) => {
        const next = { ...prev };
        for (const [slug, summary] of pairs) next[slug] = summary;
        return next;
      });
    });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps -- keyed by the page's slugs (see above)
  }, [slugsKey, readSummary]);

  if (view === null || isSingle) {
    return <div data-ui="home-loading">{HOME_LOADING_LINE}</div>;
  }

  if (view.projects.length === 0) {
    return <div data-ui="home-empty">{NO_PROJECTS_LINE}</div>;
  }

  const result = pageResult!;

  return (
    <section data-ui="home-grid" className={styles.grid}>
      <h1 className={styles.title}>{HOME_TITLE}</h1>
      <div className={styles.cards}>
        {result.items.map((entry) => {
          const hasSummary = Object.prototype.hasOwnProperty.call(summaries, entry.slug);
          const card = projectCardOf(entry, hasSummary ? summaries[entry.slug] : null);
          return (
            <button
              type="button"
              key={entry.slug}
              className={styles.card}
              data-ui="project-card"
              data-slug={entry.slug}
              data-reachable={card.reachable ? "true" : "false"}
              onClick={() => switchTo(entry.slug)}
            >
              <div className={styles.name}>{card.name}</div>
              <div className={styles.folderHint}>{card.folderHint}</div>
              {card.fixIt && <div className={styles.fixIt} data-ui="card-fix-it">{card.fixIt}</div>}
              {hasSummary && (
                <>
                  <div
                    className={styles.resultLine}
                    data-ui="card-result"
                    data-tone={card.resultTone}
                    style={{ borderLeftColor: `var(--remedy-state-${card.resultTone})` }}
                  >
                    {card.resultLine}
                  </div>
                  <div className={styles.chip} data-ui="card-active">{card.activeChip}</div>
                  <div
                    className={styles.chip}
                    data-ui="card-decisions"
                    data-urgent={card.urgent ? "true" : "false"}
                  >
                    {card.decisionsChip}
                  </div>
                  <div className={styles.cost} data-ui="card-cost">{card.costLine}</div>
                  {card.degraded && <div className={styles.degraded}>{DEGRADED_LINE}</div>}
                </>
              )}
            </button>
          );
        })}
      </div>
      {result.pages > 1 && (
        <nav className={styles.pager} data-ui="home-pager">
          <button type="button" disabled={result.page <= 1} onClick={() => setPage((p) => p - 1)}>
            Previous
          </button>
          <span data-ui="home-page">Page {result.page} of {result.pages}</span>
          <button type="button" disabled={result.page >= result.pages} onClick={() => setPage((p) => p + 1)}>
            Next
          </button>
        </nav>
      )}
    </section>
  );
}
