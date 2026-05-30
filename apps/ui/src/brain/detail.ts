/**
 * Detail Card — floating compact info card for node clicks.
 *
 * No permanent rail. Opens on click, closes on X or clicking canvas.
 * Advanced metadata collapsed by default.
 */

interface NodeDetail {
  node_id: string;
  type: string;
  label: string;
  status: string | null;
  risk: string | null;
  layer: number;
  importance: number;
  cluster: string;
  meaning: string;
  why_it_exists: string;
  evidence: string[];
  next_actions: string[];
  commands: string[];
  advanced: Record<string, unknown>;
}

type FetchDetail = (nodeId: string) => Promise<NodeDetail>;

export class DetailCard {
  private el: HTMLElement;
  private fetchDetail: FetchDetail;
  private currentNodeId: string | null = null;

  constructor(el: HTMLElement, fetchDetail: FetchDetail) {
    this.el = el;
    this.fetchDetail = fetchDetail;
  }

  async show(nodeId: string) {
    if (this.currentNodeId === nodeId && this.el.classList.contains("visible")) {
      this.hide();
      return;
    }
    this.currentNodeId = nodeId;

    // Show loading state
    this.el.innerHTML = `<button class="close-btn" id="detail-close">&times;</button>
      <h3>Loading...</h3>`;
    this.el.classList.add("visible");
    this._bindClose();

    try {
      const detail = await this.fetchDetail(nodeId);
      this._render(detail);
    } catch {
      this.el.innerHTML = `<button class="close-btn" id="detail-close">&times;</button>
        <h3>Error loading detail</h3>`;
      this._bindClose();
    }
  }

  hide() {
    this.el.classList.remove("visible");
    this.currentNodeId = null;
  }

  private _bindClose() {
    const btn = document.getElementById("detail-close");
    if (btn) btn.addEventListener("click", () => this.hide());
  }

  private _render(d: NodeDetail) {
    const statusBadge = d.status ? `<span style="display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;background:${d.status === 'failed' ? '#fee' : d.status === 'active' ? '#efe' : '#f5f5f5'};color:${d.status === 'failed' ? '#c33' : '#555'}">${d.status}</span>` : "";
    const riskBadge = d.risk ? `<span style="display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;background:${d.risk === 'high' ? '#fee' : '#fff5e5'};color:${d.risk === 'high' ? '#c33' : '#b86'};margin-left:4px">${d.risk}</span>` : "";

    let html = `<button class="close-btn" id="detail-close">&times;</button>
      <h3>${esc(d.label)}</h3>
      <div class="subtitle">${esc(d.type)} &middot; ${esc(d.cluster)} ${statusBadge} ${riskBadge}</div>`;

    if (d.meaning) {
      html += `<div class="field"><div class="field-label">Meaning</div><div class="field-value">${esc(d.meaning)}</div></div>`;
    }
    if (d.why_it_exists) {
      html += `<div class="field"><div class="field-label">Why it exists</div><div class="field-value">${esc(d.why_it_exists)}</div></div>`;
    }
    if (d.evidence && d.evidence.length > 0) {
      html += `<div class="field"><div class="field-label">Evidence</div><div class="field-value">${d.evidence.map(e => esc(String(e))).join("<br>")}</div></div>`;
    }
    if (d.next_actions && d.next_actions.length > 0) {
      html += `<div class="field"><div class="field-label">Next actions</div><div class="field-value">${d.next_actions.map(a => esc(String(a))).join("<br>")}</div></div>`;
    }
    if (d.commands && d.commands.length > 0) {
      html += `<div class="field"><div class="field-label">Commands</div><div class="field-value" style="font-family:monospace;font-size:12px">${d.commands.map(c => esc(String(c))).join("<br>")}</div></div>`;
    }

    // Advanced (collapsed)
    const advKeys = Object.keys(d.advanced || {});
    if (advKeys.length > 0) {
      html += `<button class="advanced-toggle" id="adv-toggle">Advanced (${advKeys.length} fields)</button>
        <div class="advanced-content" id="adv-content">`;
      for (const k of advKeys) {
        const v = d.advanced[k];
        const display = typeof v === "object" ? JSON.stringify(v, null, 2) : String(v);
        html += `<div class="field"><div class="field-label">${esc(k)}</div><div class="field-value" style="font-size:12px;word-break:break-all">${esc(display)}</div></div>`;
      }
      html += `</div>`;
    }

    this.el.innerHTML = html;
    this._bindClose();

    // Advanced toggle
    const toggle = document.getElementById("adv-toggle");
    const content = document.getElementById("adv-content");
    if (toggle && content) {
      toggle.addEventListener("click", () => content.classList.toggle("open"));
    }
  }
}

function esc(s: string): string {
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}
