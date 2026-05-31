/**
 * Detail Card v2 — compact floating info card for node clicks.
 *
 * No permanent rail. No scroll-heavy panel.
 * Shows: title, status, why this matters, evidence, next action, copy command.
 * Advanced metadata collapsed and visually secondary.
 */

interface NodeDetail {
  version: number;
  node_id: string;
  title: string;
  status_text: string;
  why_this_matters: string;
  evidence_summary: string[];
  next_safe_action: string;
  copy_command: string;
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
    let html = `<button class="close-btn" id="detail-close">&times;</button>
      <h3>${esc(d.title)}</h3>`;

    if (d.status_text) {
      html += `<div class="subtitle">${esc(d.status_text)}</div>`;
    }

    if (d.why_this_matters) {
      html += `<div class="field"><div class="field-label">Why this matters</div><div class="field-value">${esc(d.why_this_matters)}</div></div>`;
    }

    if (d.evidence_summary && d.evidence_summary.length > 0) {
      html += `<div class="field"><div class="field-label">Evidence</div><div class="field-value">${d.evidence_summary.map(e => esc(String(e))).join("<br>")}</div></div>`;
    }

    if (d.next_safe_action) {
      html += `<div class="field"><div class="field-label">Next safe action</div><div class="field-value">${esc(d.next_safe_action)}</div></div>`;
    }

    if (d.copy_command) {
      html += `<div class="field"><div class="field-label">Command</div><div class="field-value copy-command" title="Click to copy" style="font-family:monospace;font-size:12px;cursor:pointer;padding:4px 8px;background:#f5f7fa;border-radius:4px" id="copy-cmd">${esc(d.copy_command)}</div></div>`;
    }

    // Advanced (collapsed, visually secondary)
    const advKeys = Object.keys(d.advanced || {});
    if (advKeys.length > 0) {
      html += `<button class="advanced-toggle" id="adv-toggle">Advanced</button>
        <div class="advanced-content" id="adv-content">`;
      for (const k of advKeys) {
        const v = d.advanced[k];
        const display = typeof v === "object" ? JSON.stringify(v) : String(v);
        html += `<div class="field"><div class="field-label">${esc(k)}</div><div class="field-value" style="font-size:11px;color:#8899aa">${esc(display)}</div></div>`;
      }
      html += `</div>`;
    }

    this.el.innerHTML = html;
    this._bindClose();

    // Copy command click
    const copyEl = document.getElementById("copy-cmd");
    if (copyEl) {
      copyEl.addEventListener("click", () => {
        navigator.clipboard.writeText(d.copy_command).catch(() => {});
        copyEl.style.background = "#e8f5e9";
        setTimeout(() => { copyEl.style.background = "#f5f7fa"; }, 600);
      });
    }

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
