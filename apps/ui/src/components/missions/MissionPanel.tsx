import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import type { MissionOrders, ProjectMissions } from "../../api/missionCard";
import {
  MISSIONS_LOADING_LINE,
  MISSIONS_UNREADABLE_LINE,
  NO_MISSIONS_LINE,
  NO_ORDERS_LINE,
  NO_PROJECT_LINE,
  ORDERS_LOADING_LINE,
  ORDERS_UNREADABLE_LINE,
  UNTITLED_ORDER_LINE,
  chainReachLine,
  chipLabel,
  chipOpenable,
  earlierOrdersLine,
  missionCardLine,
  orderUsageLine,
} from "../../api/missionCard";
import { loadMissionOrders, loadProjectMissions } from "../../api/missionCardDoor";
import styles from "./MissionPanel.module.css";

/**
 * The project's missions (F305 T002, DECISIONS F305 D1 and D2; R-1248): one card per mission of
 * the project the cockpit shows. Opening a card loads that mission's newest orders, each with the
 * model calls and tokens of its jobs and its chain band: one chip per job of the order, in every
 * repository the order reached. A chip opens that job in its own project's cockpit through
 * `onOpenJob`, the project context's own address change. Opened from `RightLivePanel.tsx`'s
 * "Missions" button and mounted by `RemedyShell.tsx` as a sibling outside `<main>`, the same
 * place the results panel mounts.
 *
 * PORTALED TO `document.body`, for the reason `TourOverlay.tsx`'s own comment records.
 */
export function MissionPanel({ project, jobId, serverToken, onOpenJob, onClose }: {
  project: string;
  jobId: string;
  serverToken: string;
  onOpenJob: (slug: string, jobId: string) => void;
  onClose: () => void;
}) {
  const [missions, setMissions] = useState<{ project: string; view: ProjectMissions | null } | null>(null);
  const [openMissionId, setOpenMissionId] = useState<string | null>(null);
  const [orders, setOrders] = useState<{ missionId: string; view: MissionOrders | null } | null>(null);

  useEffect(() => {
    if (project === "") return;
    let cancelled = false;
    void loadProjectMissions({ project, token: serverToken }).then((view) => {
      if (!cancelled) setMissions({ project, view });
    });
    return () => { cancelled = true; };
  }, [project, serverToken]);

  // A mission's orders are read only when its card is opened, and again each time it is.
  useEffect(() => {
    if (project === "" || openMissionId === null) return;
    let cancelled = false;
    const missionId = openMissionId;
    void loadMissionOrders({ project, missionId, token: serverToken }).then((view) => {
      if (!cancelled) setOrders({ missionId, view });
    });
    return () => { cancelled = true; };
  }, [project, serverToken, openMissionId]);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose]);

  const shown = missions !== null && missions.project === project ? missions : null;
  const openOrders = orders !== null && orders.missionId === openMissionId ? orders : null;

  return createPortal(
    <section role="region" aria-label="Missions" data-ui="mission-panel" className={styles.panel}>
      <header className={styles.header}>
        <h2>Missions</h2>
        <button type="button" onClick={onClose}>Close missions</button>
      </header>
      {project === "" && <p className={styles.quiet}>{NO_PROJECT_LINE}</p>}
      {project !== "" && shown === null && <p className={styles.quiet}>{MISSIONS_LOADING_LINE}</p>}
      {shown !== null && shown.view === null && <p className={styles.quiet}>{MISSIONS_UNREADABLE_LINE}</p>}
      {shown?.view && shown.view.missions.length === 0 && <p className={styles.quiet}>{NO_MISSIONS_LINE}</p>}
      {shown?.view && shown.view.missions.length > 0 && (
        <ul className={styles.missions}>
          {shown.view.missions.map((card) => {
            const open = card.mission_id === openMissionId;
            return (
              <li key={card.mission_id} className={styles.card} data-ui="mission-card">
                <button
                  type="button"
                  className={styles.cardToggle}
                  aria-expanded={open}
                  onClick={() => setOpenMissionId(open ? null : card.mission_id)}
                >
                  <span className={styles.goal}>{card.goal}</span>
                  <span className={styles.cardLine}>{missionCardLine(card)}</span>
                </button>
                {open && openOrders === null && <p className={styles.quiet}>{ORDERS_LOADING_LINE}</p>}
                {open && openOrders !== null && openOrders.view === null && (
                  <p className={styles.quiet}>{ORDERS_UNREADABLE_LINE}</p>
                )}
                {open && openOrders?.view && openOrders.view.orders.length === 0 && (
                  <p className={styles.quiet}>{NO_ORDERS_LINE}</p>
                )}
                {open && openOrders?.view && openOrders.view.orders.length > 0 && (
                  <ol className={styles.orders} data-ui="mission-orders">
                    {openOrders.view.orders.map((order) => (
                      <li key={order.order_id || "before-orders"} className={styles.order} data-ui="mission-order">
                        <p className={styles.orderTitle}>{order.title || UNTITLED_ORDER_LINE}</p>
                        <p className={styles.orderLine} data-ui="mission-order-usage">{orderUsageLine(order.usage)}</p>
                        <p className={styles.quiet}>{chainReachLine(order.chain)}</p>
                        <div className={styles.chain} data-ui="mission-chain">
                          {order.chain.map((chip) => (
                            <button
                              key={chip.job_id}
                              type="button"
                              className={styles.chip}
                              data-ui="mission-chip"
                              data-project={chip.slug}
                              data-job={chip.job_id}
                              aria-current={chip.job_id === jobId ? "true" : undefined}
                              disabled={!chipOpenable(chip)}
                              onClick={() => onOpenJob(chip.slug, chip.job_id)}
                            >
                              <span className={styles.chipProject}>{chipLabel(chip)}</span>
                              <span className={styles.chipTitle}>{chip.title || chip.job_id}</span>
                              <span className={styles.chipState}>{chip.state}</span>
                            </button>
                          ))}
                        </div>
                      </li>
                    ))}
                  </ol>
                )}
                {open && openOrders?.view && earlierOrdersLine(openOrders.view.earlier_orders) !== "" && (
                  <p className={styles.quiet}>{earlierOrdersLine(openOrders.view.earlier_orders)}</p>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </section>,
    document.body,
  );
}
