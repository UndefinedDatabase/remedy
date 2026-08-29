// The completion digest's HERO CARD (T5_F040 T002). `jobDigest.ts` decodes the
// envelope, `digestVisibility.ts` decides WHEN to show it and `digestCardCopy.ts`
// decides what its words say; this component is the fourth and last piece — the
// EDGE that binds those three pure modules to a render and to the one storage
// port DECISION F040 D8 declares. Every decidable rule already lives in one of
// those three files and none of it is restated here: this file renders the
// answers it is handed and binds the one side effect that has to live at an
// edge somewhere.
//
// THE DISMISSAL PORT IS BOUND HERE, DECISION F040 D8. `digestVisibility.ts`
// DECLARES `DigestVisibilityPort` and implements nothing, exactly as
// `AgentNowCard.tsx` binds the clock `recency.ts` refuses to read. The concrete
// port — wherever a dismissal actually persists — is the mount's to construct
// and hand down as a prop; this component only calls the two methods the port
// promises.
//
// `tests/ui_contracts/test_digest_hero_card.py` pins the properties below that
// no type-checker can see: the edge stays the edge, and no rule gets a second
// home.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// IT READS NO CLOCK EXCEPT AT THE DISMISSAL. `Date.now()` is called in exactly
// one place — the dismiss handler — because that is the one edge DECISION F040
// D8 names; everything else about WHEN the card shows was already decided by
// `digestVisibility.ts` before this component ever ran, and it re-derives none
// of that rule.
// IT KEEPS NO STORAGE OF ITS OWN. No localStorage key, no sessionStorage key: a
// dismissal is written through `port.writeDismissal`, and only the concrete
// port the mount constructs decides where that write lands.
// IT OPENS NO SOCKET. No fetch, no XMLHttpRequest, no loader: the digest has
// already arrived as a prop by the time this component runs.
// IT ADDS NO CSS OF ITS OWN. `DigestHeroCard.module.css` (round 8) supplies the
// three classes this component uses and nothing more is declared here; the
// state-coloured headline and the layout rules belong with the mount, where the
// card is first seen in context.
// IT RESTATES NO RULE. The state phrase comes from `digestStateLabel`, the call
// to action from `digestCtaText`, the exactness flag from `digestCostLine`, and
// the estimate mark and phrase from `TopMetricsBar.tsx` — none of them
// reimplemented, none of them retyped as a literal.
import type { JobDigest } from "../../api/jobDigest";
import { digestCostLine } from "../../api/jobDigest";
import type { DigestVisibility, DigestVisibilityPort } from "../../api/digestVisibility";
import { digestStateLabel, digestCtaText } from "../../api/digestCardCopy";
import { ESTIMATE_MARK, ESTIMATE_PHRASE } from "../metrics/TopMetricsBar";
import styles from "./DigestHeroCard.module.css";

export interface DigestHeroCardProps {
  digest: JobDigest;
  visibility: DigestVisibility;
  port: DigestVisibilityPort;
  onDismissed?: () => void;
  onOpenDecisions?: () => void;
  onPrimaryAction?: (ruleId: string) => void;
}

export function DigestHeroCard({
  digest,
  visibility,
  port,
  onDismissed,
  onOpenDecisions,
  onPrimaryAction,
}: DigestHeroCardProps) {
  // The RULE is `digestVisibility`'s and this component re-derives none of it:
  // it is handed the answer and branches on it.
  if (!visibility.show) {
    return null;
  }

  const stateLabel = digestStateLabel(digest.state);
  const cost = digestCostLine(digest.cost);
  const ctaText = digestCtaText(digest.primary_action.label);
  const hasOwnership = digest.ownership.length > 0;
  const hasOpenDecisions = digest.decisions.open_count > 0;

  const handleDismiss = () => {
    // The ONE clock read in this file, because this is the edge — the same
    // split `AgentNowCard.tsx` makes for `recency.ts`.
    port.writeDismissal(digest.job_id, Date.now());
    onDismissed?.();
  };

  const handlePrimaryAction = () => {
    onPrimaryAction?.(digest.primary_action.rule_id);
  };

  return (
    <section className={styles.heroCard} data-state={digest.state}>
      {/* Rendered as the server wrote it, with no §17 screen: `_headline` in
          `packages/orchestration/job_digest.py` composes the digest's OWN
          prose as one plain sentence and never borrows the report's Markdown,
          so unlike `primary_action.label` it carries no markup and no
          identifier to remove. Reading taken at `5778fccb`. */}
      <h2 className={styles.heroHeadline}>{digest.headline}</h2>
      <p>{stateLabel}</p>
      <p>
        {cost.estimated && <span>{ESTIMATE_MARK}</span>}
        {cost.value}
        {cost.estimated && <span>{ESTIMATE_PHRASE}</span>}
      </p>
      {/* DECISION F040 D3: an empty ownership list is OMITTED, never rendered
          empty. */}
      {hasOwnership && (
        <ul>
          {digest.ownership.map((sentence, i) => (
            <li key={i}>{sentence}</li>
          ))}
        </ul>
      )}
      {hasOpenDecisions && (
        <button type="button" onClick={onOpenDecisions}>
          {digest.decisions.open_count} open decision
          {digest.decisions.open_count === 1 ? "" : "s"}, peak urgency {digest.decisions.peak_urgency}
        </button>
      )}
      <button type="button" onClick={handleDismiss}>
        Dismiss
      </button>
      <button type="button" className={styles.heroCta} onClick={handlePrimaryAction}>
        {ctaText}
      </button>
    </section>
  );
}
