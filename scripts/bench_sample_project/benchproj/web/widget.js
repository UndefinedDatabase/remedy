// The items widget: fetches /items and renders one <li> per item.
// renderItems is pure (items in, markup out); load() alone touches the page.
function escapeHtml(text) {
  return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderItems(items) {
  return items.map((item) => `<li data-id="${item.id}">${escapeHtml(item.name)}</li>`).join("");
}

async function load() {
  const response = await fetch("/items");
  document.getElementById("items").innerHTML = renderItems(await response.json());
}

if (typeof document !== "undefined") { load(); }
if (typeof module !== "undefined") { module.exports = { escapeHtml, renderItems }; }
