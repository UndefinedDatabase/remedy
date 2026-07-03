# REMEDY MASTERPLAN — Kernprodukt bis zur 20M-Reife (150 Features, nach Wichtigkeit)

> **Version 3.0 (FINAL) · 2026-07-02 · Ersetzt REMEDY_ROADMAP_100.md**
> **Ablage im Repo:** `docs/roadmap/ROADMAP.md` — damit Remedy es ab F080 selbst liest.
> **Adressat:** Der Orchestrator (GPT, Web-Oberfläche). Dieses Dokument wird als Anhang
> übergeben und ist die verbindliche Quelle für JEDE Planung. Bei Konflikt zwischen
> Tagesidee und diesem Dokument gewinnt dieses Dokument. Änderungen daran macht nur
> der Operator (decodeux).

---

## TEIL A — PROTOKOLL FÜR DEN ORCHESTRATOR (GPT im Web, arbeitet über Review-Zips)

Der Orchestrator sieht das Repository nicht direkt. Der Arbeitszyklus ist:
Operator lädt das aktuelle Review-Zip hoch → Orchestrator reviewt final → entscheidet
„weiter" oder „Review-Punkte beheben" → gibt den nächsten Block als Self-Run-Goal aus.

**A1 — Positionsbestimmung aus dem Zip.** Jede Sitzung beginnt mit dem hochgeladenen
Review-Zip. Der Orchestrator liest daraus: `.review_zip_manifest.json` (Status, Gates,
dirty files), `.agent/MASTERPLAN_LEDGER.md` (Fortschritt lt. Teil G — die Datei liegt
im Repo und ist damit automatisch im Zip), `.agent/live_review.md` und
`evidence/current/`. Ohne Zip wird nicht geplant — der Orchestrator fordert es an.

**A2 — Der Orchestrator ist der Final-Reviewer.** Er prüft das Zip gegen die
Done-Kriterien der aktiven F-Nummern und fällt ein Verdict: **PASS** (Block
abgeschlossen, Ledger-Update vorschlagen, nächsten Block planen) oder **FINDINGS**
(konkrete, nummerierte Review-Punkte; der nächste Block ist dann ein Fix-Block, kein
neues Feature). Es wird kein neues Feature geplant, solange FINDINGS offen sind.

**A3 — Blockgröße: bewusste Mischung aus mittelgroß und GROSS.** Blöcke umfassen
1–3 F-Nummern und mischen absichtlich mittelgroße mit großen Tasks (viele Dateien,
lange Läufe): Große Tasks sind zugleich der Belastungstest, ob Remedy große Aufgaben
beherrscht — genau das soll das Produkt können. Regeln:
- Mindestens jeder zweite Block enthält einen bewusst großen Task.
- Scheitert ein großer Task, bestimmt das Postmortem (F010) zuerst die Fehlerklasse;
  zerlegt wird erst NACH der Analyse — nicht präventiv alles klein schneiden.
- Ergebnisse großer Tasks fließen in die Kapazitäts-Leiter (F144) ein.

**A4 — DONE hat vier Bedingungen.** Ein Feature ist erst DONE, wenn:
(1) Tests grün, (2) Remedy-Reviewer-Verdict PASS, (3) der Orchestrator es im
Zip-Review nach A2 freigegeben hat, (4) es per CLI/UI real benutzbar und auf main
committet ist. Tests allein reichen NICHT. „Implementiert aber blockiert" = NICHT DONE.

**A5 — Priorität = Dokumentreihenfolge.** Geplant wird immer die niedrigste unfertige
F-Nummer, deren Abhängigkeiten (Teil F) erfüllt sind. Ausnahmen: expliziter
Operator-Auftrag sowie ausgewiesene Prioritäts-Ausnahmen in Teil D (derzeit: F146–F148 werden unmittelbar nach Tier 0, vor F013, eingeplant;
F149–F150 gehören prioritär zu Tier 6 und werden mit F117–F128 eingeplant).

**A6 — Meta-Arbeits-Sperre.** Es werden KEINE neuen Evidence-Gates, Manifeste,
Taxonomien, Proof-Chains oder Hygiene-Schichten geplant, außer eine F-Nummer verlangt
es wörtlich. Das bestehende Evidence-System ist eingefroren (Bugfixes erlaubt).
Grund: Das Projekt hat bereits ~84k Zeilen Prozess-Maschinerie bei <1,5k Zeilen
nutzersichtbarer Fähigkeit. Jede weitere Meta-Schicht senkt den Produktwert.

**A7 — Selbstauflösungs-Klausel.** Tier 3 dieses Plans baut den Orchestrator in Remedy
selbst ein. Der GPT-Orchestrator plant damit aktiv an seiner eigenen Ablösung. Das ist
gewollt und wird nicht umgangen, verzögert oder wegdiskutiert.

**A8 — UI-Tasks brauchen Sichtmaterial.** Für das Cockpit existiert ein verbindliches
Referenzdesign (Teil H, `docs/ui/design_reference/ux_design.png`). Solange
F087–F089 nicht DONE sind, übersetzt der Orchestrator dieses Design selbst und
liefert fertiges CSS/TSX inline in den UI-Task-Prompts (Agenten sehen keine Bilder);
Layout, Glyphen und Farben folgen dabei strikt Teil H. Ab F089 DONE entfällt das:
dann wird die `design_reference` direkt übergeben.

**A9 — Keine Rückfragen zur Laufzeit.** Self-Run-Goals werden so formuliert, dass der
Builder NIE eine Design- oder Produktfrage stellen muss: Alle Vorgaben (Farben, Namen,
Verhalten) stehen explizit im Goal bzw. in der design_reference. Fehlt eine Vorgabe,
gilt die Referenz wörtlich (der Screenshot ist Gesetz) oder ein dokumentierter
Default — niemals eine Frage mitten im Lauf.

---

## TEIL B — PRODUKTVISION: DIE SIEBEN SÄULEN

Remedy ist ein Orchestrierungs-Cockpit, das aus einem Auftrag ein fertiges,
bewiesenes Softwareprodukt macht — und dem Menschen dabei nie das Steuer nimmt.

1. **Sichtbarkeit & Eigentümerschaft.** Der User sieht live, wie sein Job zu Tasks
   wird (der Growing-Brain-Graph, Teil H: Tasks, Runs und Artefakte materialisieren
   sich als wachsendes Nervennetz), kann jederzeit stoppen, eingreifen,
   Tasks verbieten oder ändern. Seine Vorgaben (Prompt, Screenshot, Spec) sind Gesetz
   und werden nie durch Rückfragen mitten im Lauf ersetzt. Das Produkt fühlt sich an
   wie SEIN Produkt, weil er es sichtbar steuert und jede Abweichung dokumentiert ist.
2. **Langläufer-Autonomie („Overnight").** „Overnight" ist ein Bild, kein
   Zeitfenster: Ein Job läuft unbeaufsichtigt SO LANGE WIE NÖTIG — Minuten, Stunden
   oder Tage, gern während man schläft — nach dem Schema TRIGGER → SCOPE → ACTION →
   BUDGET → STOP → REPORT, bis „feature-complete nach prüfbaren Kriterien", nicht
   bis „der Agent findet es fertig". Es gibt keine Nacht-Mechanik im System, nur
   Läufe ohne anwesenden Menschen.
3. **Tokenwahrheit & Tokensparsamkeit.** Jede Zahl ist gemessen (nie geschätzt als
   echt ausgegeben), und die Architektur (Caching, Routing, Kontextdisziplin) senkt
   die Kosten systematisch.
4. **Beweisbare Qualität.** Generierung und Bewertung sind getrennt; Ergebnisse werden
   am laufenden Produkt verifiziert (Tests, Playwright, Pixel-Fidelity, Security-Scan).
   Remedys Evidence-System wird vom Ballast zum Alleinstellungsmerkmal: beweisbare
   Autonomie.
5. **Design-to-Code.** Screenshot rein → feature-complete UI raus, mit messbarer
   Design-Treue, egal wie lange der Lauf dafür braucht.
6. **Eigener Orchestrator.** Remedy plant selbst von der Mission bis zum Task — das
   Copy-Paste zu einem externen GPT entfällt vollständig.
7. **Gedächtnis & Projektbindung.** Jeder Job gehört zu einem Projekt/Repo
   (Autodetektion aus dem Arbeitsverzeichnis); Ziele, Konventionen, Lektionen und
   Entscheidungen persistieren als projektgebundene Memory-Cards — Remedy wird pro
   Projekt messbar schlauer. Bedienung im Golden Path: `cd repo && remedy do "…"`.

---

## TEIL C — DESIGN-PRINZIPIEN (Stand der Technik, in jede Umsetzung einzubauen)

**P1 — Monitoring + Interrupt schlägt Einzel-Approval.** Erfahrene Nutzer wollen nicht
jede Aktion freigeben, sondern zuverlässig SEHEN was passiert und einfach eingreifen
können. Alle Cockpit-Features folgen diesem Muster: maximale Transparenz, minimale
Pflicht-Klicks, jederzeit unterbrechbar. (Anthropic-Forschung zu Agent-Autonomie 2026.)

**P2 — Governed Autonomy.** Autonomie ist gestuft: Lesen frei, risikoarme Schreibaktionen
bedingt frei, riskante Aktionen (destruktiv, extern, teuer) immer mit menschlichem Gate.
Jede Freigabe-Anfrage zeigt drei Dinge: Beleg, erwartetes Ergebnis, Schaden im Fehlerfall.

**P3 — Loops statt Prompts.** Die Arbeitseinheit ist die deklarierte Schleife mit
Stop-Bedingung, nicht der Einzelprompt. Fortschritt lebt auf der Festplatte (Repo,
Checkpoints), nie nur im Gesprächsverlauf.

**P4 — Generierung ≠ Bewertung.** Builder bewerten nie eigene Arbeit. Bewertung erfolgt
am laufenden Produkt, nicht nur am Diff. Für Kritisches: zweiter, adversarialer Blick.

**P5 — Ein Task = eine Session.** Kontextfenster sind die harte Grenze; Handoffs
zwischen Sessions laufen über strukturierte Artefakte im Repo.

**P6 — Ehrlichkeit vor Schönheit.** unknown ≠ cheap, estimated ≠ actual, geskippt ≠
erledigt. Kein Feature darf diese Prinzipien aufweichen — sie sind der spätere
Verkaufskern („beweisbare Autonomie").

**P7 — Vorgaben vorne, keine Fragen mittendrin.** Alle Produkt- und
Designentscheidungen stehen VOR dem Lauf fest: im Prompt, in der Spec, im Screenshot.
Die Referenz ist Gesetz — zeigt der Screen Blau, wird es Blau, Punkt. Das System
stellt während eines Laufs NIE Geschmacksfragen; echte Unklarheiten werden einmalig
und gebündelt im Flight Plan geklärt (F034) oder per dokumentiertem Default
entschieden (assumption_log). Eigentümerschaft entsteht durch sichtbare Steuerung
und Eingriffsmacht — nicht durch Dauerbefragung.

---

## TEIL D — DIE 150 FEATURES (Reihenfolge = Wichtigkeit)

Format: **Fxxx Titel** — Beschreibung. → Done-Kriterium (messbar).

---

### TIER 0 — SYSTEMRELEVANTES FUNDAMENT (F001–F012)
*Ohne diese 12 trägt nichts anderes. Sie sind klein, aber jede spätere Säule steht darauf.*

**F001 Adaptive Provider-Timeouts + Retry** — Timeout pro Rolle/Taskgröße berechnet
(Basis 600s Builder / 300s Reviewer, +60s je erlaubter Datei, Cap 2400s); vor final
`provider_unavailable` bis zu 2 automatische Retries mit Backoff (30s/120s), Zähler in
der Evidence. Ersetzt die hart kodierten 120–300s, die aktuell die Hauptfehlerquelle
der Self-Runs sind. → 10 Self-Runs ohne Timeout-Block.

**F002 Operator-Eingriff als gültiger Evidence-Pfad** — `remedy do repair-attest
<job> <task>` erzeugt bei manueller Reparatur alle Pflicht-Artefakte
(execution_mode=manual_operator_repair, review mit verdict=operator_attested,
token_accounting actual_available=false/reason=manual, Diff-Hashes). Menschliches
Eingreifen darf das System nie wieder in BLOCKED_EVIDENCE zwingen. → Ein manuell
reparierter Task passiert final_verifier.

**F003 Echte Token-/Kostenmessung** — Builder/Reviewer-Aufrufe nutzen
`claude -p --output-format json`; usage (input/output/cache_read/cache_creation),
total_cost_usd, num_turns, duration_ms, session_id landen in token_accounting →
token_truth `actual_available: true`, confidence=high. → Jobsumme stimmt mit
CLI-Reports überein.

**F004 Roh-Stream-Archiv** — Optional `--stream-evidence`: stream-json (--verbose)
wird per tee als Roh-JSONL gesichert UND geparst (Tool-Calls, api_retry-Events).
Grundlage für Live-Feed, Audit, Replay. → agent_run_trace zeigt echte
Tool-Call-Sequenz statt „reconstructed".

**F005 Strukturierte Outputs erzwingen** — Planner-/Reviewer-Antworten per
`--json-schema` (Claude CLI) gegen Pydantic-Schemata; Format-Parse-Fehler und deren
Repair-Runden verschwinden. → 0 Parse-Fehler in 10 Runs.

**F006 Worktree-Isolation pro Lauf** — Jeder Run arbeitet in eigenem `git worktree`,
nie im Haupt-Checkout; Ergebnis = Branch + PR-fertiger Diff. Voraussetzung für
Parallelität und sichere unbeaufsichtigte Läufe. → Zwei parallele Läufe kollidieren nicht.

**F007 Runtime-Harness** — Remedy startet/stoppt den Dev-Server des Zielprojekts
kontrolliert (Port, Health-Check, Timeout, Log-Capture). Das 17-Zeilen-Paket
`runtimes/` wird hier real. → `remedy runtime serve --probe` bringt apps/ui hoch
und meldet ready.

**F008 SSE-Eventstream** — `/api/jobs/<id>/events/stream` auf Basis des vorhandenen
events-since-Cursors; Frontend abonniert statt 5s-Polling. → Statuswechsel sichtbar
<1s nach Backend-Event.

**F009 Der eine Schreibkanal** — Genau EIN POST-Endpoint
`/api/jobs/<id>/commands` (Token, CSRF-Header, Rate-Limit), der ausschließlich in
die bestehende approval_/decision_queue schreibt. Read-only-Philosophie bleibt,
aber die UI kann handeln. → Entscheidung aus der UI wird vom Backend ausgeführt.

**F010 Automatisches Fehlerklassen-Postmortem** — Jeder gescheiterte Run schreibt
failure_postmortem.json (timeout / parse / review_reject / infra / budget) und
aggregiert in `remedy stats failures`. → Retry-Kaskaden werden als Klassen zählbar.

**F011 Kill-Switch** — `.remedy/STOP`-Datei + Command via F009 beenden jeden Lauf
am nächsten sicheren Punkt; UI-Stop-Button. → Stop wirkt ≤1 Zyklus.

**F012 Deterministische Läufe** — `--bare`-Modus (ignoriert lokale Hooks/MCP),
gepinnte Env, dokumentierte Seeds wo möglich; Grundlage für Replay und Audit.
→ Zwei Läufe desselben Fake-Provider-Jobs sind bit-identisch.

---

### TIER 1 — DER KERN-RUN: LIVE-COCKPIT & EIGENTÜMERSCHAFT (F013–F044)
*Das Herzstück deiner Vision: Job rein, Nodes materialisieren sich live, jederzeit
stoppen/eingreifen/verbieten/ändern — der User weiß immer, was passiert, und trifft
die Entscheidungen, die das Produkt zu SEINEM machen.*

**F013 Job-Intake** — Auftrag in natürlicher Sprache + Anhänge (Dateien, später
Screenshots) → strukturierter Job (Ziel, Kontext, Vorgaben, Anti-Ziele). Intake
stellt fehlende Pflichtangaben als kompakte Rückfragen. → Ein Prosa-Auftrag wird
ohne Handarbeit zum validen Job-Objekt.

**F014 Flight Plan (Plan-Vorschau vor Start)** — Vor Ausführung zeigt Remedy: Task-DAG,
geschätzte Kosten/Dauer je Task (Bänder, ehrlich als Schätzung markiert), Risiken,
berührte Pfade, benötigte Entscheidungen. Nichts läuft ohne Plan-Ansicht. → Flight
Plan erscheint für jeden Job; Start erst nach Bestätigung (überspringbar per Flag).

**F015 Interaktives Plan-Editing** — Im Flight Plan: Tasks löschen, umformulieren,
umsortieren, mergen, splitten; Akzeptanzkriterien editieren. Änderungen fließen als
Evidence-Vermerk (user_edited_plan) ein. → Editierter Plan wird exakt so ausgeführt.

**F016 Skalierende Task-Granularität** — Die Node-Anzahl skaliert mit der Jobgröße
nach expliziten Regeln (min 1, max konfigurierbar; Ziel-Tokenbudget pro Task steuert
den Schnitt). Kleiner Job = 2 Nodes, großer Job = 30. → Testfälle für 3 Jobgrößen
erzeugen erwartete Node-Zahlen.

**F017 Scope-Fences** — Pro Job: geschützte Pfade (nie anfassen), verbotene Aktionen
(z. B. keine Dependency-Änderungen), Muss-Pfade. In UI und Goal-File editierbar;
Verstoß = harter Task-Fail. → Fence-Verstoß-Test schlägt korrekt fehl.

**F018 Budget & Stop-Bedingungen im Flight Plan** — Jeder Job deklariert BUDGET
(€/Tokens), STOP (Bedingungen: alles grün / N Zyklen / Deadline) und REPORT (Ziel)
nach dem Loop-Schema. → Erstes erreichtes Limit stoppt sauber am Checkpoint.

**F019 Live-Node-Materialisierung (Growing Brain)** — Das Netz wächst live gemäß
Ontologie H2: Planner-Arbeit lässt Task-Nodes am Ast sprießen; jeder Builder-/
Review-/Repair-/Test-Run sprießt als Kind-Node aus seinem Task; jeder Provider-Call
setzt einen Synapsen-Punkt, jedes Artefakt einen Dokument-Punkt (Events via SSE F008,
Quelle F004). Der User sieht seinen Job buchstäblich zu einem Organismus wachsen —
der emotionale Kernmoment des Produkts. → Bei einem echten Lauf entstehen Task- UND
Run-Nodes einzeln animiert, exakt in Ereignis-Reihenfolge, rückführbar auf Events.

**F020 Node-Lebenszyklus & Glyphen-Sprache** — Zustände und Glyphen exakt nach
Design-Legende (H2): Open violett, Planned blass, In Progress pulsierend mit
Kantenpartikeln, Done grün, Failed/Blocked als einzige Warnfarbe; Glyphen `</>` /
Person / Kolben / Wiederhol-Ring je Node-Typ. Respektiert Reduced-Motion (H4).
→ Alle 8 Node-Typen aus H2 im Livelauf visuell unterscheidbar; Motion-Off-Test.

**F021 Live-Aktivitätsfeed + „Agent is doing now"** — Rechte Leiste nach H1:
oben die Live-Karte mit der aktuellen Aktion („Builder is implementing
collect_file_metadata()"), darunter der Feed aus echten Tool-Events (F004):
„Builder liest src/auth.py", „Reviewer: 2 Findings". Keine Platzhalter. → Karte
und Feed sind 1:1 auf Roh-Events rückführbar; Karte wechselt <1s nach Event.

**F022 Live-Kosten-Ticker** — Metrik-Leiste (H1) erhält neben OPEN/PLANNED/DONE/
PROGRESS die laufenden Kosten/Tokens des Jobs in Echtzeit (F003 via SSE) mit
Budget-Fortschrittsbalken und Restschätzung. → Ticker bewegt sich im Livelauf;
Endstand = Ledger-Stand.

**F023 Semantischer Zoom L0–L3** — Die vier Stufen aus H3 vollständig: L0
Organismus (Runs aggregiert zu Ast-Aktivität), L1 Task-Expansion (nur einer,
Geschwister dimmen), L2 Run-Detail-Popover (Verdict, Tokens, Dauer, Diff-Link,
Synapsen sichtbar), L3 Evidenz-Seitenpanel. Zoom und Klick führen zur selben
Stufe; Brotkrumen, Esc, Doppelklick-Reset, Cluster-Aggregation >8 Kinder (H4).
→ Alle Stufen per Zoom UND Klick erreichbar; Cluster-Test mit 20 Runs; 60fps bei
500 Gesamt-Nodes in L0.

**F024 Phasen-Zeitleiste mit Scrubber** — Fußzeile nach H1: Job → Planning →
Build → Test → Review → Finalized mit Unter-Glyphen (`</>`/Kolben/Person) je
Phase; verschmolzen mit dem Event-Replay: Ziehen am Scrubber spult den gesamten
Graph-Zustand vor/zurück. → Scrubbing durch abgeschlossenen Job flüssig; Phasen-
Marker springen korrekt.

**F025 Pause/Resume** — Global und pro Node: Pause stoppt vor dem nächsten
Provider-Call; Resume setzt exakt fort (kein Kontextverlust dank Session-IDs).
→ Pause→Resume-Lauf endet identisch zu ununterbrochenem Lauf.

**F026 Task-Edit zur Laufzeit** — Wartende oder pausierte Nodes können umformuliert
werden (Prompt, Scope, Akzeptanzkriterien); Node startet mit Vermerk
user_modified_at_runtime neu. → Editierter Node baut nachweislich nach neuer Vorgabe.

**F027 Task-Veto** — Jeder noch nicht appliedte Node kann verboten werden; abhängige
Nodes werden automatisch neu geplant oder als unerreichbar markiert — transparent im
Graph. → Veto auf Mittel-Node erzeugt korrekten Folgezustand.

**F028 Task-Injektion** — Neuen Node zur Laufzeit hinzufügen (mit Abhängigkeiten);
Scheduler ordnet ihn ein. → Injizierter Node läuft im selben Job durch.

**F029 Subtree-Rerun** — Node + Nachfolger ab Checkpoint neu ausführen (z. B. nach
Edit oder mit anderem Modell). → Rerun produziert konsistenten Workspace ohne
Reste des alten Zweigs.

**F030 Steering-Nachrichten** — Freitext-Hinweis an einen laufenden/nächsten Task
(„nutze die bestehende Button-Komponente"), wird in die nächste Builder-Runde
injiziert und in der Evidence vermerkt. → Hinweis nachweislich im Prompt-Trace.

**F031 Entscheidungs-Postfach** — Entscheidungen blockieren nur ihren Zweig; alles
Unabhängige läuft weiter. Postfach bündelt offene Entscheidungen mit Kontext.
→ Job mit 1 Entscheidung + 2 freien Tasks liefert 2 Ergebnisse + 1 saubere Anfrage.

**F032 Approval mit Dreiklang** — Jede Freigabe-Anfrage zeigt: Beleg (Evidenz),
erwartetes Ergebnis, Downside im Fehlerfall (P2). Einheitliche Karte in UI und
Abschlussreport. → Kein Approval ohne die drei Felder.

**F033 Hunk-genaue Diff-Freigabe** — Bei Approval-pflichtigen Änderungen: pro
Änderungsblock annehmen/ablehnen; abgelehnte Hunks gehen als präzises Repair-Feedback
zurück. → Teilfreigabe erzeugt korrekten Patch + Repair-Runde für den Rest.

**F034 Gebündelte Klärung im Flight Plan (nie im Lauf)** — Erkennt der Planner echte
Unklarheiten (fehlende Pflicht-Vorgabe, Widerspruch zwischen Prompt und Referenz),
sammelt er sie zu EINEM konsolidierten Klärblock im Flight Plan — beantwortbar in
einer Minute, vor dem Start. Während des Laufs gilt: Referenz ist Gesetz, sonst
dokumentierter Default im assumption_log der Evidence. Null Fragen zur Laufzeit.
→ Job mit 3 eingebauten Unklarheiten erzeugt genau 1 Klärblock vorab und 0
Laufzeit-Fragen; Defaults stehen im assumption_log.

**F035 Ownership-Ledger** — Chronik aller User-Eingriffe und -Vorgaben des Jobs
(„Du hast T004 verboten", „Deine Vorgabe: Farbschema aus ref.png", „Flight-Plan-
Klärung: X entschieden") im Report und in der UI — sichtbare Urheberschaft ohne
Dauerbefragung. → Ledger vollständig gegen decision_queue- und Eingriffs-Historie.

**F036 Guided Tour des Ergebnisses** — Nach Jobabschluss generiert Remedy eine
Führung durch das Gebaute (Struktur, Kernentscheidungen, wo was liegt, wie man es
startet) — der User versteht sein Produkt, statt es nur zu besitzen. → Tour für
einen Demo-Job; Externer findet damit den Einstiegspunkt.

**F037 Gerenderter Diff-Viewer** — Node-Detail zeigt syntax-gehighlightete Diffs
(safe.diff existiert) statt Rohtext; Datei-Navigation, Kollaps. → Contract-Test.

**F038 Node-Chat (read-only fundiert)** — „Warum hast du das so gelöst?" an einen
Node: Antwort wird ausschließlich aus dessen Evidence (Prompt-Trace, Review,
Diff) generiert, mit Quellenangabe auf die Artefakte. Kein freies Fabulieren.
→ Antworten zitieren Evidence-Abschnitte.

**F039 Story-/Replay-Modus** — Der ganze Job als geführte Erzählung auf der
Zeitleiste (F024) — auch als Übergabe an Dritte. → Story für abgeschlossenen Job.

**F040 Abschluss-/Rückkehr-Digest** — Nach Jobende bzw. beim ersten UI-Öffnen nach
Abwesenheit (laufender oder beendeter Langlauf): Hero-Karte mit Stand/Ergebnis,
Kosten, Entscheidungen, nächster Aktion.
→ Contract-Test.

**F041 Artefakt-Vorschau** — Gerenderte README, erzeugte Screenshots, laufende
Preview-URL (F007) direkt im Cockpit. → Preview-Link öffnet die gebaute App.

**F042 Mehrprojekt-Cockpit** — Startseite über Projekte: letzte Läufe, Kostenwoche,
offene Entscheidungen, Ideen-Queue-Zähler. → Zwei Demo-Projekte korrekt.

**F043 Erklärschicht** — Jede Metrik/Status hat 1-Satz-Tooltip; Onboarding-Tour
(6 Schritte) beim ersten Start. → Copy-Audit: kein Begriff ohne Tooltip.

**F044 Bedien-Qualität** — Cmd+K-Palette (nutzt F009-Kommandos), Keyboard-Navigation
im Graph; Performance-Budget First Paint <1,5s, 60fps bei 200 Nodes, in CI geprüft.
→ Budget-Tests grün.

---

### TIER 2 — OVERNIGHT-AUTONOMIE & IDEA ENGINE (F045–F068)
*Die zweite Kernsäule. Klarstellung: „Overnight" heißt nur, dass ein Lauf
unbeaufsichtigt so lange arbeitet, wie der Auftrag braucht (auch während man
schläft) — es gibt KEINE Nacht-Mechanik, keine Tageszeit-Logik. Ein Lauf endet,
wenn die Done-Kriterien grün sind oder ein Limit greift; sonst arbeitet er weiter.
Plus dein Ideen-Prozess: Remedy erfindet Vorschläge, du approvst/deniest/priorisierst.*

**F045 Loop-Definitionen** — Deklaratives Format für autonome Läufe:
TRIGGER (manuell/Zeit/Event) · SCOPE (Repo, Pfade, Queue) · ACTION · BUDGET
(€/Tokens/Zyklen) · STOP (Bedingungen) · REPORT (Ziel). Jede Langlauf-Fähigkeit
baut auf diesem Schema auf. → Ein Loop-File startet einen definierten Lauf.

**F046 Mehrzyklen-Schleife** — Der bewusst auf max_cycles=1 begrenzte Executor wird
zur budgetierten Schleife (F018-Limits); erstes erreichtes Limit stoppt am Checkpoint.
→ 5-Zyklen-Lauf endet exakt am Limit, Zustand konsistent.

**F047 Checkpoint & Resume (kill-sicher)** — Nach jedem Zyklus vollständiger
Checkpoint; `--resume <run>` setzt exakt fort. → kill -9 mitten im Zyklus, Resume,
Ergebnis identisch zu ununterbrochenem Lauf.

**F048 Auftrags-Queue** — Aufträge sammeln (`remedy queue add`), atomares Claiming
(kein Task doppelt), Prioritäten; abgearbeitet wird, sobald Kapazität frei ist —
sofort oder eben während man schläft. → 3 Einträge, ein Lauf, 3 Ergebnisse.

**F049 Parallelität** — Bis zu N unabhängige Tasks parallel in eigenen Worktrees
(F006), gemeinsames Budget, Concurrency-Cap wegen Rate-Limits. → Messbar kürzere
Wandzeit, keine Kollisionen.

**F050 DAG-Scheduling** — Tasks deklarieren depends_on; parallelisiert wird nur
Unabhängiges; ein blockierter Zweig legt nie den ganzen Lauf lahm. → Diamant-
Abhängigkeit korrekt ausgeführt.

**F051 Eskalation statt Block (unbeaufsichtigt)** — Entscheidungs-pflichtige Tasks landen
im Postfach (F031), der Lauf macht mit Unabhängigem weiter. → Unbeaufsichtigter
Lauf mit 1 Approval-Task + 2 freien liefert 2 Ergebnisse + 1 wartende Entscheidung.

**F052 Selbstheilende Testrunden** — Scheitern Tests nach einem Zyklus: begrenzte
Auto-Repair-Runde (max 2, Session-Resume F106) bevor der Zyklus als failed gilt.
→ Injizierter trivialer Testbruch wird unbeaufsichtigt selbst repariert.

**F053 Abschluss- & Zwischenreport** — EIN Markdown pro Lauf (bei Ende oder auf
Abruf als Zwischenstand, wenn der Lauf noch arbeitet): gebaut / blockiert / Kosten /
Entscheidungen / Diff-Links / empfohlene nächste Aktion. → Golden-Test + realer
Langlauf; Zwischenreport eines laufenden Jobs korrekt.

**F054 Auto-Revert-Vorschlag** — Verschlechtert der Endstand die Testsuite
gegenüber dem Startstand des Laufs, liegt ein Revert-Patch + Analyse bei (wird NIE selbst
ausgeführt). → Simulierte Regression erzeugt Vorschlag.

**F055 Rehearsal (Dry-Run)** — `--rehearse`: kompletter Plan + Kostenschätzung +
Risikoliste ohne Ausführung — der Check vor dem echten Lauf. → Rehearse-Output
strukturgleich zum echten Lauf.

**F056 Missionen: persistentes Ziel, Jobs als Ausführungseinheiten** — Credo:
Ein Auftrag ist IMMER zuerst ein Job. Er wird erst zur Mission, wenn Remedy nach
dem ersten Job selbstständig Folge-Jobs planen und steuern soll. Definition:
Mission = persistentes Ziel, Job = Ausführungseinheit. Kein zweiter UI-Begriff im
Golden Path — der Einstieg bleibt `remedy do "…"`, Remedy entscheidet intern
(klar abgrenzbarer Auftrag → Job; Langziel mit Folge-Läufen → Mission) und macht
die Entscheidung im Flight Plan transparent. Missionszustand persistiert; jeder
Folge-Job beginnt mit Verify des Vorstands („verify before building"). Im Cockpit
sind die Jobs einer Mission sichtbar VERKETTET (Lineage-Faden bis zum
Ursprungs-Job). → Ein Langziel erzeugt eine Mission mit 3 verketteten Jobs;
Cockpit zeigt den Faden bis zum Ursprung; ein einfacher Auftrag bleibt ein
einzelner Job ohne Missions-Overhead.

**F057 Rate-Limit-bewusster Scheduler** — Läufe kennen Provider-Limits/Zeitfenster;
bei Limit-Treffern wird gewartet statt gescheitert (api_retry-Events aus F004).
→ Simuliertes Rate-Limit verzögert statt blockiert.

**F058 Modell-Failover-Kette** — Bei Nichtverfügbarkeit: definierte Kette
(z. B. Opus→Sonnet), Wechsel ehrlich in Evidence (configured vs actual model).
→ Failover-Test dokumentiert den Wechsel korrekt.

**F059 Benachrichtigungen** — Push bei „Entscheidung nötig" und „Lauf fertig"
(Webhook/ntfy/Mail, konfigurierbar). → Testlauf löst Notification aus.

**F060 Langlauf-Zertifikat** — Kompaktes, teilbares Evidence-Bundle pro Lauf
(Hashes, Kosten, Verdicts, Entscheidungen) — „beweisbare Autonomie" als Artefakt.
Nutzt review_bundle, baut NICHTS Neues (A6). → ZIP <5 MB pro Lauf.

**F061 Definition-of-Done-Compiler** — Aus den Nutzer-Vorgaben werden PRÜFBARE
Acceptance-Checks generiert (Tests, Playwright-Flows, Lint, Build); „feature-complete"
heißt: alle Checks grün, nicht „der Agent meint fertig". Der wichtigste Baustein
gegen Vibe-Code. → Job endet erst bei 100% grünen kompilierten Checks.

**F062 Produkt-Smoke als Abschlussgate** — Vor Jobende: App startet (F007),
Kernflows sind per Playwright klickbar, keine Konsolen-Fehler. → Absichtlich
kaputter Startpfad lässt den Job nicht enden.

**F063 Idea Engine v1** — Nach (und optional während) Jobs erzeugt ein Ideen-Prozess
Feature-Vorschläge: je Idee Begründung, geschätzter Aufwand (Band), geschätzter
Nutzen, betroffene Bereiche — in eine persistente Ideen-Queue. → Nach Demo-Job
liegen ≥3 begründete Ideen in der Queue.

**F064 Ideen-Queue-UI** — Karten mit approve / deny / Priorität ziehen; approved →
automatischer Flight-Plan-Entwurf (F014) zur Bestätigung. Denied wird erinnert
(nie wieder identisch vorschlagen). → Approve-Flow erzeugt startbaren Plan.

**F065 Ideen-Herkunfts-Beleg** — Jede Idee referenziert die konkrete Beobachtung
(Testlücke X, TODO Y, UX-Reibung Z, Nutzerentscheidung W) — keine freien
Halluzinationen. Ideen ohne Beleg werden verworfen. → Jede Queue-Idee hat
mind. 1 prüfbare Referenz.

**F066 Idea Engine v2 (kontinuierlich, opt-in)** — Beobachtet TODO-Kommentare,
Coverage-Lücken, wiederkehrende Fehlerklassen, Ownership-Ledger-Muster und legt
periodisch Ideen nach — als konfigurierter Loop (F045), nie ungefragt ausführend.
→ Periodischer Lauf erzeugt Ideen ausschließlich in die Queue.

**F067 Routine-Missionen** — Vordefinierte Loops: Dependency-Updates, Lint-Schulden,
Doku-Sync, Testlücken schließen, Karten-Aufräumen (F124) — als Bibliothek
startklarer Loop-Files.
→ Dependency-Loop läuft einmal erfolgreich durch.

**F068 Autonomie-Bilanz (auf Abruf)** — `remedy stats autonomy --since <Zeitraum>`:
was lief autonom, wo war Mensch nötig, Interrupt-Quote, Erfolgsrate — die
Steuerungszahlen für „wie viel darf Remedy schon allein". Kein fester
Berichtsrhythmus; die Bilanz wird gezogen, wann immer man sie braucht.
→ Bilanz über einen frei gewählten Zeitraum korrekt gegen Ledger/Evidence.

---

### TIER 3 — REMEDY ALS EIGENER ORCHESTRATOR: GPT-ABLÖSUNG (F069–F086)
*Dritte Kernsäule: das Copy-Paste zum Web-GPT verschwindet. Remedy plant selbst —
von der Mission bis zum Task — mit dem „Gesamtbild", das heute der externe GPT hält.*

**F069 Mission-Compiler** — Langziel in Prosa → Epics → Jobs → Tasks, mehrstufig,
mit Begründungskette; jede Ebene menschlich editierbar (F015-Muster). → Eine
Beispiel-Mission wird zu 3 Epics mit startbaren Jobs kompiliert.

**F070 Orchestrator-Loop** — Eine Remedy-eigene Orchestrator-Rolle (Provider-Call
mit Missions-Dossier) entscheidet nach jedem Job: nächster Job / Replan / Eskalation.
„Loops statt Prompts" — der User schreibt Missionen, nicht mehr Prompts.
→ 3 aufeinanderfolgende Jobs laufen ohne menschliches Prompting.

**F071 Missions-Dossier** — Komprimiertes Gesamtbild (Ziele, Architektur-Snapshot,
Entscheidungen, offene Fronten) als stabiler, gecachter Prompt-Präfix des
Orchestrators; wird nach jedem Job aktualisiert (aus Memory-Cards, Tier 6).
→ Dossier ≤3k Tokens, nachweislich im Cache (cache_read>0).

**F072 Spec-First** — Pro Feature eine lebende Spezifikation als Vertrag; Builder
bauen gegen die Spec, ein Sync-Check meldet Drift zwischen Spec und Code.
→ Absichtliche Code-Abweichung wird als Spec-Drift gemeldet.

**F073 Eval-Suiten als Brücke** — Wiederkehrende Probleme (3× gleiche Fehlerklasse)
erzeugen automatisch eine kleine Eval (Testfall + erwartetes Verhalten), die künftige
Pläne mitprüfen. → Wiederholtes Problem erscheint als Eval und schlägt vor dem
Merge an.

**F074 Planner-Kalibrierung** — Schätzung vs. Realität (Kosten, Dauer, Repair-Runden)
wird pro Taskklasse gespeichert und fließt in künftige Flight-Plan-Schätzungen.
→ Schätzfehler sinkt über 10 Jobs messbar.

**F075 Zuverlässigkeits-Meilenstein** — 10 Self-Runs in Folge ohne Operator-Eingriff,
jede Abweichung per F010 klassifiziert und behoben. Gate für alles Weitere in Tier 3.
→ 10/10 dokumentiert.

**F076 Vision-Planner (Design-Übersetzung in-house)** — Der Orchestrator dekomponiert
Screenshots selbst (nutzt Tier-4-Bausteine F087–F089) — die letzte Fähigkeit, für die
heute der Web-GPT gebraucht wird. → Screenshot→Flight-Plan ohne externes Tool.

**F077 Orchestrator-Wachhund** — Eine zweite, günstige Instanz prüft jeden
Orchestrator-Plan gegen Masterplan + Spec + Fences und meldet Drift/Scope-Creep,
bevor ausgeführt wird. → Absichtlicher Drift-Plan wird abgefangen.

**F078 Konfigurierbare Autonomie-Level** — Pro Projekt L2 (jede Aktion bestätigen)
bis L5 (nur Missionsgrenzen); Risikoklassen (read/write/destructive/expensive)
mappen auf Gates (P2). → Levelwechsel ändert Gate-Verhalten nachweislich.

**F079 Session-Handoffs** — Strukturierte Übergabe-Artefakte zwischen Orchestrator-
Sessions (Stand, offene Fronten, nächste Absicht) im Repo — nie im Chatverlauf.
→ Neustart mitten in einer Mission setzt korrekt fort.

**F080 Maschinenlesbarer Masterplan** — Dieses Dokument erhält einen YAML-Spiegel
(F-Nummern, Status, Abhängigkeiten); der interne Orchestrator liest seine Position
selbst — das Ledger-Protokoll (Teil A/G) wird obsolet. → `remedy plan status` zeigt
nächste offene F-Nummer.

**F081 remedy init** — Ein Befehl macht jedes fremde Repo Remedy-fähig: registriert
es in der Projekt-Registry (F146), erkennt Sprache/Testbefehl, legt `.remedy/` mit
Memory-Skelett + Config + CLAUDE.md an, verifiziert per Smoke-Task. → Frisches
Fremd-Repo in <2 Min einsatzbereit; danach genügt `remedy do` (F147).

**F082 Fremdprojekt-Benchmark** — 5 reale Klein-Aufträge (CLI-Tool, REST-API,
React-Widget, Bugfix, Screenshot-UI) laufen regelmäßig; Ergebnisse im Zeitverlauf.
Der ehrliche Realitätscheck des Gesamtsystems. → Benchmark-Report v1 mit Baseline.

**F083 CI-Release-Gate** — main immer releasebar: volle Suite + Benchmark-Smoke in
CI; Merge nur grün. → Absichtlicher Bruch wird geblockt.

**F084 Demo-Modus** — `remedy demo`: vollständiger Fake-Provider-Durchlauf mit
realistischer Live-UI-Show, offline, <60s — für Erstnutzer und Vorführungen.
→ Läuft offline durch.

**F085 Sicherheits-Härtung** — Least-Privilege-Toolflächen pro Rolle,
Sandbox-Grenzen dokumentiert+getestet, Redaction gegen echte Leak-Corpora geprüft,
Threat-Model-Dokument. → Audit-Checkliste grün.

**F086 Installierbare Releases** — Semver-Tags, generiertes Changelog, Installation
auf frischer Maschine (pip/pipx), Quickstart ≤10 Min bis zum ersten Lauf.
→ Externer Tester schafft Quickstart ohne Hilfe.

---

### TIER 4 — DESIGN-TO-CODE (F087–F102)
*Screenshot rein, feature-complete UI raus — mit messbarer Treue. Ersetzt das
manuelle CSS-in-Prompts-Kodieren vollständig.*

**F087 design_reference-Artefakt** — Jobs/Tasks akzeptieren PNG/JPG
(`--design ref.png`), versioniert per Hash in der Evidence. → Bild hängt beweisbar
am Task.

**F088 Bild an den Builder** — Builder-Prompt referenziert die Bilddatei; Claude
Code liest sie nativ aus dem Worktree („Lies zuerst design/ref.png, beschreibe
Layout, Farben, Typo, Abstände"). → Stream-Evidence zeigt den Read auf die Bilddatei.

**F089 Design-Dekomposition** — Vision-Schritt erzeugt strukturierte Spec:
Komponentenbaum, Farbtokens, Typo-Skala, Spacing, Interaktionsvermutungen (JSON,
F005-Schema). → Farbstichprobe der Spec stimmt mit Pixelwerten überein.

**F090 Screenshot-Verifikation** — Playwright rendert die gebaute Route
deterministisch (fixe Viewport-Größe, Animationen aus, Fonts geladen) →
actual.png neben ref.png in der Evidence. → Beide Bilder je Task vorhanden.

**F091 Pixel-Diff-Check** — pixelmatch ref vs actual, maxDiffPixelRatio
konfigurierbar; Score + diff.png als normaler AcceptanceCheck. → Falsche Farbe
macht den Check rot.

**F092 Visueller Reviewer** — Reviewer erhält ref/actual/diff und bewertet nach
Design-Qualität, Originalität, Handwerk, Funktionalität mit ortsbezogenen Findings
(„Header-Padding 8px zu klein"). → Findings referenzieren Bildregionen; Repair
behebt sie nachweislich.

**F093 Fidelity-Schleife** — Build → Screenshot → Diff → visuelles Review → Repair
bis Score ≥ Schwelle oder Rundenbudget aus; eingehängt in die BESTEHENDE
pingpong/repair-Maschinerie (A6: keine neue Loop-Klasse). → Demo-Screenshot in
≤3 Runden auf ≥90%.

**F094 Interaktions-Verifikation** — Evaluator bedient die UI (klicken, tippen,
hovern) und prüft die aus F089 vermuteten Interaktionen — Funktion, nicht nur Pixel.
→ interactions_verified[] in der Evidence.

**F095 Multi-Screen-Flows** — Mehrere Screenshots = ein Flow (Login→Liste→Detail);
Routen/Navigation geplant, jeder Screen + Übergänge verifiziert. → 3-Screen-Flow
feature-complete.

**F096 Responsive-Verifikation** — Fidelity bei 3 Viewports; Referenz pro
Breakpoint möglich, sonst heuristische Umbruchprüfung. → Evidence mit 3
Screenshot-Sätzen.

**F097 Design-Tokens ins Zielprojekt** — Aus F089 werden echte Token-Dateien
(CSS-Vars/Tailwind) statt hartkodierter Werte. → Zweiter Screen desselben Systems
nutzt vorhandene Tokens (Diff-Beweis).

**F098 Komponenten-Katalog** — Gebaute Komponenten mit Thumbnail, Props, Pfad im
Projektgedächtnis; neue Screens referenzieren Bestehendes. → „Button primary" wird
beim zweiten Screen wiederverwendet, nicht dupliziert.

**F099 Fidelity-Baseline-Guard** — Erreichte Baselines werden
toHaveScreenshot-Snapshots im Zielprojekt; spätere Tasks dürfen sie nicht
verschlechtern. → Absichtliche Regression wird gefangen.

**F100 Fidelity im Cockpit** — Score (0–100) + Vorher/Nachher-Slider + Runden-Kino
pro Design-Task — sichtbare Konvergenz, Spaß beim Zusehen. → UI-Contract-Test.

**F101 Referenz-Treue-Regel bei Ambiguität** — Ist ein Screenshot mehrdeutig
(verdeckte Bereiche, nicht ablesbare Zustände), gilt strikt: sichtbare Pixel sind
Gesetz; Unsichtbares wird nach dokumentiertem Default ergänzt (Designsystem-Tokens
F097, nächstliegende Konvention) und im assumption_log ausgewiesen. Echte
Blocker-Ambiguität landet im Flight-Plan-Klärblock (F034), nie als Laufzeit-Frage.
→ Test mit teilverdecktem Referenzbild erzeugt korrekte Defaults + assumption_log,
0 Laufzeit-Fragen.

**F102 Langlauf × Design** — F087–F095 unbeaufsichtigt im Langlauf: PNG rein,
feature-complete UI raus (z. B. während man schläft), mit Fidelity-Report und
Vorher/Nachher-Bildern im Abschlussreport (F053). → Realer unbeaufsichtigter
Beweislauf.

---

### TIER 5 — TOKEN-ÖKONOMIE (F103–F116)
*Messen, dann senken. Ziel: −50 % Kosten pro Task bei gleicher Qualität, alles belegt.*

**F103 Kosten-Ledger** — Persistente Aggregation €/Tokens je Task/Job/Projekt/Tag;
`remedy stats cost --since 7d`. → Summe stimmt mit F003-Rohdaten überein.

**F104 Hartes Budget-Enforcement** — `--budget-usd/--budget-tokens` je Job;
Überschreitung → sauberer Checkpoint-Stop, Status budget_exhausted. → Mini-Budget
stoppt nach Task 1 ohne Datenverlust.

**F105 Cache-optimierte Promptordnung** — Stabiler Präfix zuerst (Regeln,
Konventionen, Memory-Cards, Missions-Dossier), Volatiles ans Ende — maximiert
Prompt-Caching. → cache_read_tokens>0 ab dem zweiten Task jedes Jobs.

**F106 Session-Resume für Repair** — Repair-Runden via `--resume <session_id>`
statt Voll-Prompt-Neuaufbau. → Input-Tokens der Repair-Runde −40 % gemessen.

**F107 Kontextpaket v2** — Repo-Map (Symbole) + nur berührte Dateiabschnitte +
Signaturen der Nachbarn statt N Volldateien. → Kontextpakete −30 % bei stabiler
Reviewer-Passrate.

**F108 Komprimierte Summaries** — Vorgänger-Task-Summaries als strukturierte
5-Zeilen-Stichpunkte (Dateien, Symbole, offene Punkte), erzeugt von Haiku/Ollama.
→ Summary-Größe −60 %, Passrate stabil.

**F109 Modell-Routing nach Klasse** — trivial→Haiku, standard→Sonnet,
komplex/Architektur→Opus; Override per Flag; Klassifikation im Flight Plan sichtbar.
→ Messbarer Kostenunterschied im Ledger bei gemischtem Job.

**F110 Reviewer-Downgrade-Politik** — Reviewer standardmäßig eine Klasse unter dem
Builder, außer Task ist kritisch markiert. → Konfig + Evidence-Feld.

**F111 Diff-basierte Repair-Prompts** — Repair erhält nur Findings + betroffene
Hunks + Minimal-Umgebung, nie den Voll-Task erneut. → Repair-Prompt ≤25 % des
Originals.

**F112 Klassen-Kontextbudget + Ehrlichkeit** — Hartes Input-Budget je Taskklasse;
bei Beschnitt listet die Evidence omitted_context[] (Pfad+Grund), damit Fails auf
fehlenden Kontext rückführbar sind. → Kein Task über Budget; Liste vorhanden.

**F113 Ollama-Offload** — Summaries, Commit-Messages, Fehlerklassifikation, Ideen-
Vorfilter laufen lokal (kostenfrei), Fallback Haiku. → Ledger zeigt 0-Kosten-Zeilen
für diese Rollen.

**F114 Anfrage-Dedupe** — Hash über (Task-Body+Kontext): identische Anfrage im
selben Job wird nicht erneut gesendet (cache_hit=true in Evidence). → Test mit
dupliziertem Task.

**F115 Prompt-Breakdown & Kosten-Auswertung** — Zusammensetzung jedes Prompts nach
Segmenten (Tokens); `remedy stats report --since <Zeitraum>`: Kostenkurve, teuerste
Klassen, Cache-Quote, Einsparung vs. Vorzeitraum — auf Abruf, kein fester Rhythmus.
→ Breakdown je Task abrufbar; Report für freien Zeitraum korrekt.

**F116 Kosten-Anomalie-Alarm** — Task >3× Klassenmedian → Warnung in UI und Report;
bei unbeaufsichtigten Läufen zusätzlich Drossel-Option. → Simulierter Ausreißer erzeugt Warnung.

---

### TIER 6 — MEMORY: KARTEN ZUERST, RETRIEVAL SPÄTER (F117–F128)
*Deine Memory-Card-Intuition ist richtig: deterministisch, auditierbar, cache-freundlich,
im Repo versioniert. Vektor-DB wird ein OPTIONALER späterer Baustein, kein Fundament.*

**F117 Memory-Cards v1** — Typisierte Karten als Markdown+Frontmatter im Zielrepo
(`.remedy/memory/cards/`): Typen goal / convention / lesson / decision / component;
Felder: id, typ, tags, scope, gültig-für-Taskklassen, Budgetgewicht, Quelle.
→ `remedy memory list` zeigt Karten strukturiert.

**F118 Karten-Anheftung** — Deterministische Regeln, welche Karten in welchen Prompt
kommen (nach Typ, Tags, Taskklasse), mit hartem Token-Budget (~2k) und stabiler
Sortierung (Cache-Synergie F105). Kein Retrieval-Zufall. → Prompt-Breakdown zeigt
Karten-Segment; identischer Task → identisches Segment.

**F119 Karten-UI: die Sammlung** — Karten als professionelle Sammlung präsentiert
(Sammelkarten-Optik ohne Kitsch: Typ-Farbe, Titel, Wert-Rang aus F150, Herkunft,
Nutzungshistorie). Ansehen, editieren, an/aus, löschen, pinnen (immer anheften),
manuell an einzelne Tasks/Jobs anheften oder davon entfernen, pro Job temporär
überschreiben. → Edit/Anheften aus der UI landet in der Datei bzw. im Job (F009);
Detailansicht zeigt Herkunft + Einsatz-Historie.

**F120 Harvesting mit Freigabe** — Fehler (F010), Review-Findings (3× gleiche
Klasse) und Jobabschlüsse erzeugen Karten-KANDIDATEN; der User approved/verwirft —
niemals Auto-Persistenz. → Echter Timeout-Fall erzeugt Lesson-Kandidat
„Builder-Timeouts ≥600s".

**F121 Entscheidungs-Karten automatisch** — Jede F031-Entscheidung, jeder
Flight-Plan-Klärpunkt (F034) und jeder dokumentierte Default (assumption_log) wird
als decision-Karten-KANDIDAT angelegt („REST statt GraphQL, weil …") — das
Produktgedächtnis der Eigentümerschaft. → Klärpunkt erzeugt Kandidat mit Begründung.

**F122 Karten im Missions-Dossier** — Das Orchestrator-Dossier (F071) wird aus
goal-/decision-Karten generiert — Gesamtbild aus dem Gedächtnis, nicht aus
Chatverläufen. → Dossier-Diff nach neuem decision-Karten-Approve.

**F123 Wirksamkeits-KPI** — A/B über Zeit: Passrate/Kosten/Repair-Runden mit vs.
ohne Karten-Anheftung, in der Kosten-Auswertung (F115). → KPI nach einer A/B-Phase vorhanden.

**F124 Karten-Hygiene (manuell + periodisch)** — `remedy memory compact`: Duplikate
mergen, Veraltetes archivieren (nie still löschen), Budgetgrenzen halten;
Konflikt-Erkennung (zwei Karten widersprechen sich → User entscheidet). Zusätzlich
als Routine-Mission (F067) ein periodischer, LLM-gestützter Aufräum-Lauf: prüft
Karten gegen den aktuellen Code-/Systemstand auf Obsoleszenz (referenzierte Datei
weg, Konvention überholt, Lesson durch Fix gegenstandslos) und legt Archivierungs-/
Update-VORSCHLÄGE in die Queue — Entscheidung immer beim User. → Aufgeblähtes Set
wird messbar kompakter; simulierte obsolete Karte wird vorgeschlagen, nie
automatisch entfernt.

**F125 Globale Karten (opt-in)** — Projektübergreifende Lessons via explizites
`remedy memory promote`; niemals automatisch. → Promote-Flow-Test.

**F126 „Was weiß Remedy?"-Ansicht** — Vollständige, exportierbare Transparenz über
das Projektgedächtnis in der UI — Vertrauensgrundlage. → Ansicht = Dateistand.

**F127 Komponenten-Karten** — F098-Katalog als component-Karten (Thumbnail, Props,
Pfad, Verwendungen) — Design-Gedächtnis im selben System. → Zweiter Screen
referenziert die Karte nachweislich.

**F128 Retrieval-Baustein v2 (optional, zuschaltbar)** — Erst ab >200 aktiven Karten
oder großen Repos: Embedding-Suche über Karten+Code als eigenständiges Modul hinter
dem MemoryGateway-Interface; Ergebnisse werden Karten-Vorschläge zur Anheftung,
nie stiller Kontext. → Baustein an/aus ohne Verhaltensänderung des Kerns.

**F149 remedy study (Nachtrag, gehört prioritär zu Tier 6)** — Remedy auf ein
BESTEHENDES Projekt loslassen: `remedy study` analysiert das Repo initial
(Architektur, Konventionen, Testlage, Risiken, zentrale Komponenten, offene TODOs)
und erzeugt daraus Karten-KANDIDATEN aller Typen — präsentiert als „Kartenzug" in
der Sammlung (F119): der User sieht, was Remedy über sein Projekt gelernt hat,
approved/verwirft/editiert jede Karte. Jede Karte trägt den Beleg (Dateipfad,
Codeausschnitt-Referenz). Nur approvte Karten werden aktiv. → `remedy study` auf
einem Fremd-Repo liefert ≥10 belegte Kandidaten; UI zeigt sie als Sammlung; keine
Karte wird ohne Approve angeheftet.

**F150 Karten-Wert & Explorations-Chance (Nachtrag, gehört prioritär zu Tier 6)** —
Jede Karte hat einen Wert, der AUSSCHLIESSLICH durch messbare Signale steigt oder
fällt: Karte war angeheftet + Task PASS ohne Repair → Wert steigt leicht; Karte
angeheftet + wiederholte Fails/Findings in ihrem Themenfeld → Wert sinkt; A/B-Daten
aus F123 kalibrieren. Keine LLM-Bauchgefühl-Bewertung. Die Anheftungs-Auswahl
(F118) gewichtet nach Wert, reserviert aber eine feste Explorations-Quote
(z. B. 20 % des Karten-Budgets) für neue/niedrig bewertete Karten, damit Neues
eine faire Chance bekommt. Der Wert ist in der Sammlung sichtbar (Rang-Stufen,
professionell). → Auswahlverteilung folgt nachweislich Gewicht+Exploration; Wert
ändert sich nur durch validierte Nutzung (Test mit synthetischer Historie).


---

### TIER 7 — QUALITÄT & VERTRAUEN: DIE 20M-DIFFERENZIERER (F129–F142)
*Features, die du noch nicht auf dem Radar hattest — sie machen aus „Agent baut Code"
das Produkt „beweisbar gute Software entsteht autonom". Der Branchen-Schmerzpunkt 2026
ist Code-Churn: ~50 % KI-Code, aber 41 % mehr davon wird binnen 30 Tagen wieder
gelöscht. Wer Überlebensqualität BEWEISEN kann, gewinnt.*

**F129 Test-First-Gate** — Konfigurierbar pro Projekt: Builder muss zuerst den
scheiternden Test liefern (Evidence: rot), dann die Implementierung (Evidence: grün).
TDD als erzwungener Ablauf, nicht als Bitte. → Task ohne roten Vorab-Test wird
zurückgewiesen.

**F130 Mutations-Stichprobe** — Nach relevanten Tasks: Mutationstest-Stichprobe
(z. B. mutmut) auf den geänderten Bereich — beweist, dass die Tests wirklich prüfen.
→ Ein „Test ohne Assertions"-Fall wird entlarvt.

**F131 Adversarialer Zweit-Review** — Für kritisch markierte Tasks: zusätzlicher
Red-Team-Pass (Sicherheit, Edge-Cases, Missbrauch) durch separaten Provider-Call
mit Angreifer-Rolle. → Eingebaute Schwachstelle im Testfall wird gefunden.

**F132 Provider-Tournament** — Für kritische Tasks: gleicher Task an 2 Builder
(z. B. Opus vs Sonnet, oder 2 Provider), Reviewer kürt den Gewinner; Kosten bewusst
verdoppelt, nur auf Anforderung. Macht `model_route_tournament` real. → Tournament-
Lauf liefert Gewinner + Begründung + beide Diffs.

**F133 Provider-Trust-Score** — Passrate/Repair-Quote je Modell×Taskklasse über
Zeit; fließt in Routing (F109) und Flight-Plan-Empfehlungen. Macht `provider_trust`
real. → Score ändert Routing nachweislich nach genug Datenpunkten.

**F134 Security-Gate** — SAST (semgrep/bandit) als Standard-AcceptanceCheck jedes
Jobs; Findings blocken oder eskalieren je Schwere (P2-Risikoklassen). → Eingebaute
Schwachstelle blockt den Task.

**F135 Flaky-Test-Detektor** — Wiederholte Läufe erkennen instabile Tests;
Quarantäne-Liste + Report statt falscher Fails, die Repair-Runden verbrennen.
→ Simulierter Flaky-Test landet in Quarantäne, nicht im Repair.

**F136 Time-Travel** — Jeder Node-Zustand (Workspace-Snapshot) ist wiederherstellbar;
„Zurück zu vor T004" als ein Klick — Sicherheit macht Mut zur Autonomie.
→ Restore stellt Workspace bit-genau her.

**F137 Shadow-Mode** — Kompletter Job als Was-wäre-wenn: alles läuft, nichts wird
applied; Ergebnis ist ein Diff-Paket + Report zum Ansehen. Ideal für Vertrauensaufbau
und riskante Missionen. → Shadow-Lauf hinterlässt 0 Änderungen im Zielrepo.

**F138 Automatische ADRs** — Signifikante Architekturänderungen erzeugen ein
Architecture-Decision-Record (Kontext, Optionen, Wahl, Konsequenzen) als
decision-Karte + Doku-Datei. → Demo-Refactor erzeugt korrektes ADR.

**F139 Churn-Metrik** — Misst, wie viel von Remedys Code nach 7/30 Tagen noch lebt
(git-Analyse) — die ehrliche Qualitätszahl, die die Branche meist versteckt.
→ `remedy stats churn` liefert die Kurve.

**F140 Bit-genauer Run-Replay** — Ein Lauf ist aus seiner Evidence vollständig
reproduzierbar (F012 + Roh-Streams F004): gleicher Input → gleiche Artefakte.
Das Enterprise-Audit-Feature schlechthin. → Replay eines Fake-Provider-Runs ist
bit-identisch.

**F141 Berechtigungs-Matrix** — Jede Aktion hat eine Risikoklasse
(read/write/destructive/expensive/external); Klassen mappen pro Autonomie-Level
(F078) auf frei/bedingt/Gate. Least Privilege als Systemeigenschaft. → Matrix-Test:
destructive ohne Gate ist unmöglich.

**F142 Vertrauens-Dashboard** — Die Zahlen, die den Produktwert BEWEISEN, an einem
Ort: Erfolgsrate, Interrupt-Quote, Churn, Kosten/Task, Fidelity-Schnitt,
Autonomie-Level-Verlauf. Das ist später die Investoren-/Kunden-Ansicht — aber
zuerst deine eigene Steuerzentrale. → Dashboard speist sich vollständig aus echten
Ledger-/Evidence-Daten.

---

---

### TIER 8 — FLAGGSCHIFF-FEATURES (F143–F145)
*Drei Killer, die aus allem darunter das Produkt machen, das man nicht vergisst.*

**F143 Genesis-Run: Ein Prompt → ein Produkt** — Der Flaggschiff-Modus: aus einem
leeren Ordner entsteht in einem unbeaufsichtigten Langlauf ein komplettes, lauffähiges Produkt — Repo-Init,
Architektur, Implementierung, Tests, CI-Konfiguration, README, laufende Preview
(F007/F041) — gesteuert durch einen einzigen Auftrag (Prosa und/oder Screenshots),
abgesichert durch DoD-Compiler (F061), Produkt-Smoke (F062) und Langlauf-Zertifikat
(F060). Das ist der Moment, den man in 60 Sekunden vorführen kann und der das
Produkt verkauft. → Realer Beweislauf: ein Absatz + 1 Screenshot vor dem
Schlafengehen — beim Aufwachen ein startbares, grünes, klickbares Produkt mit
Zertifikat (oder ein ehrlicher Zwischenreport, wenn es noch arbeitet).

**F144 Kapazitäts-Leiter (Self-Benchmark der Taskgröße)** — Remedy vermisst
kontinuierlich seine eigene Belastbarkeit: eine definierte Leiter von Task-Größen
(S: 2 Dateien/1 Modul → M: 8 Dateien → L: 25 Dateien/Cross-Cutting → XL:
Genesis-Klasse), je Stufe Erfolgsrate, Kosten, Repair-Quote über Zeit. Große
Self-Run-Tasks (A3) speisen die Leiter automatisch. Die Leiter steuert, welche
Taskgrößen der Planner sich autonom zutraut — und ist zugleich der öffentliche
Fähigkeitsbeweis des Produkts. → `remedy stats ladder` zeigt Stufen-Erfolgsraten;
Planner-Schnitt (F016) nutzt die Leiter nachweislich.

**F145 Playbook-Destillation** — Erfolgreiche Jobs werden zu wiederverwendbaren
Playbooks destilliert: parametrisierte Loop-Vorlagen (F045) mit erprobter
Task-Struktur, DoD-Checks und Memory-Karten-Verweisen („React-Dashboard aus
Screenshot", „REST-API mit Auth", „Migrations-Mission"). Neue Jobs, die einem
Playbook ähneln, starten mit dessen Gerüst statt bei null — schneller, billiger,
verlässlicher, und mit jedem Erfolg wächst die Bibliothek. Kandidaten werden
vorgeschlagen (Ideen-Queue-Muster F064), nie automatisch angelegt. → Zweiter
ähnlicher Job startet nachweislich aus dem Playbook und ist im Ledger messbar
günstiger als der erste.

---

### TIER 9 — PROJEKTBINDUNG & CLI-ERGONOMIE (F146–F148)
*⚠️ PRIORITÄTS-AUSNAHME zu A5: Diese drei Features werden UNMITTELBAR NACH TIER 0
eingeplant (vor F013), denn Cockpit, Memory, Ledger und Queue hängen an der
Projekt-Dimension. Das Zielbild: Remedy lokal installieren, ins Repo wechseln,
`remedy do "Task..."` — fertig.*

**F146 Projekt-Identität & Repo-Autodetektion** — `remedy` erkennt aus dem
Arbeitsverzeichnis das Projekt (Aufwärtssuche nach `.git`/`.remedy`), bindet es an
eine stabile Projekt-ID in einer globalen Registry (`~/.remedy/projects.json` —
macht `project_registry.py` real). Datenmodell: Projektnahes lebt IM Repo
(`.remedy/` mit Memory-Karten, Config, Ledger — versionierbar), Maschinennahes
global (`~/.remedy/projects/<id>/` für Job-Daten, Caches, Kosten-Ledger). Jeder
Job, Run und jedes Evidence-Bundle trägt die project_id. Außerhalb eines Repos:
klare Meldung + Hinweis auf `remedy init` (F081). → In zwei verschiedenen Repos
erzeugt `remedy do` nachweislich getrennte Jobs, Memory und Ledger; Evidence
enthält die korrekte project_id.

**F147 Golden-Path-CLI** — Das Drei-Befehle-Mentalmodell: (1) `remedy do "Task…"`
startet ohne weitere Flags — Autodetektion (F146), Defaults aus globaler + Projekt-
Config (Provider, Modelle, Budgets), Flight Plan (F014), los. (2) `remedy` allein
zeigt den Projektstatus (aktive Jobs, letzte Läufe, offene Entscheidungen, Kosten
der Woche). (3) `remedy ui` öffnet das Cockpit, gefiltert auf das aktuelle Projekt.
Alles Weitere bleibt erreichbar, aber der Golden Path braucht null Konfiguration
nach `remedy init`. Hilfe passt auf einen Bildschirm. → Frisches geklontes Repo:
`remedy init` + `remedy do "…"` = laufender Job in <2 Minuten; `remedy` zeigt
danach korrekten Status.

**F148 Projekt-Scoping durchgängig** — Die project_id-Dimension zieht sich durch
ALLES: Cockpit-Startseite gruppiert nach Projekten (F042), Memory-Karten sind
projektgebunden mit explizitem promote für Globales (F117/F125), Kosten-Ledger und
Kosten-Auswertungen pro Projekt filterbar (F103/F115), Auftrags-Queue mischt Projekte nur mit
Kennzeichnung (F048), Ideen-Queue pro Projekt (F064), Kapazitäts-Leiter global UND
pro Projekt (F144). Kein stilles Vermischen von Projektdaten, nirgends. → Zwei
Projekte parallel: Ledger, Memory, Ideen und Reports bleiben nachweislich getrennt;
ein Cross-Projekt-Leak-Test schlägt fehl, wenn Daten vermischt würden.


## TEIL E — MEILENSTEINE (woran „fertig" gemessen wird)

| Meilenstein | Enthält | Beweis |
|---|---|---|
| M1 „Es hält" | Tier 0 komplett | 10 Self-Runs ohne Block, echte Tokenzahlen |
| M2 „Mein Produkt" | F013–F035 | Livejob mit Materialisierung, Eingriff, Veto, Steering — auf Video |
| M3 „Langläufer" | F045–F062 | Großer Auftrag vor dem Schlafengehen — beim Aufwachen fertig oder ehrlich weiterarbeitend |
| M4 „Es denkt mit" | F063–F066 | Ideen-Queue mit belegten Ideen, Approve→Plan-Flow |
| M5 „GPT abgelöst" | F069–F080 | Eine Mission läuft 3 Jobs weit ohne externes Prompting |
| M6 „Es sieht" | F087–F102 | Screenshot rein → UI ≥90 % Fidelity, unbeaufsichtigt |
| M7 „Es spart" | Tier 5 | −50 % Kosten/Task vs. M1-Baseline, im Ledger belegt |
| M8 „Es erinnert" | Tier 6 | Karten-KPI zeigt bessere Passrate/Kosten mit Memory |
| M9 „Es beweist" | Tier 7 | Vertrauens-Dashboard live; Churn-, Replay-, Security-Beweise |
| M10 „Genesis" | F143–F145 | Ein Prompt → lauffähiges Produkt, komplett unbeaufsichtigt, mit Zertifikat |

Wenn M1–M10 erreicht sind, ist das KERNPRODUKT auf 20M-Reife: beweisbar autonome,
tokeneffiziente, design-treue Softwareerstellung unter voller menschlicher
Eigentümerschaft. (Die Bewertung selbst entsteht dann aus Nutzern/Umsatz — das ist
bewusst nicht Teil dieses Plans.)

## TEIL F — ABHÄNGIGKEITS-SCHNELLREFERENZ

- Tier 0 (F001–F012) blockiert ALLES. Zuerst. Vollständig.
- F146 ← blockiert F147–F148 und die Projekt-Dimension von F042, F048, F064, F081,
  F103, F115, F117, F144; wird direkt nach Tier 0 eingeplant (A5-Ausnahme)
- F008+F009 ← blockieren F019–F044 (Cockpit); alle Cockpit-Features bauen gegen Teil H
- F003 ← blockiert F022, F103–F116, F142
- F004 ← blockiert F021, F023, F140
- F006+F047 ← blockieren F049, F056, F136, F137
- F007 ← blockiert F041, F062, F090–F102
- F014/F015 ← blockieren F034, F064, F069
- F045–F047 ← blockieren F048–F068, F102
- F087–F089 ← blockieren F076, F090–F102 und heben A8 auf
- F117–F118 ← blockieren F071, F121–F128
- F061 ist Voraussetzung für jeden „feature-complete"-Anspruch (M3, M6)
- F149 ← setzt F117+F146 voraus; F150 ← setzt F118+F103+F123 voraus
- F143 ← setzt F045–F062 + F061/F062 + F087–F093 voraus (Genesis = Krönung, nicht Anfang)
- F144 ← speist sich aus A3-Großtasks; braucht nur F010 + F103
- F145 ← setzt F045 + F117 voraus
- Parallel-Spuren möglich: (Cockpit F019–F044) ∥ (Langläufer F045–F062) ∥ (Tokens F103–F116) nach Tier 0

## TEIL G — FORTSCHRITTS-LEDGER (Vorlage; liegt als .agent/MASTERPLAN_LEDGER.md im Repo)

```
# MASTERPLAN LEDGER — zuletzt aktualisiert: <Datum>
DONE:    F001, F002, ...
ACTIVE:  F00x (Job-ID, Stand)
FAILED:  F00y (Fehlerklasse, Kurzgrund)
SKIPPED: F00z (Operator-Entscheidung, Grund)
NÄCHSTER BLOCK LT. A5: F0..
```

Die Datei liegt im Repo unter `.agent/MASTERPLAN_LEDGER.md` und ist damit automatisch
in jedem Review-Zip enthalten — der Orchestrator liest sie dort (A1) und schlägt nach
jedem Zip-Review die Aktualisierung vor (A2/A4). Ab F080 übernimmt Remedy diese
Buchführung selbst.

---

## TEIL H — COCKPIT-REFERENZDESIGN & NODE-ONTOLOGIE („Growing Brain")

Es existiert ein verbindliches Referenzdesign für das Cockpit (Datei:
`docs/ui/design_reference/ux_design.png` — der Operator legt den Screenshot dort
ab und committet ihn). Alle Tier-1-Features werden GEGEN dieses Design gebaut; ab
F090 wird die Treue dazu per Screenshot-Verifikation gemessen. Das Design definiert:

**H1 — Layout (aus dem Referenzbild):**
- Kopfzeile: Metrik-Leiste (OPEN / PLANNED / DONE / PROGRESS %) + LIVE-Badge.
- Zentrum: der Growing-Brain-Graph — ein organisch wachsendes Nervennetz mit dem
  Job-Kern in der Mitte (Code-Glyphe), Äste = Arbeitsstränge, Leuchtintensität =
  Aktivität.
- Darüber: Kommandoleiste „Ask your agent or jump to anything" (= F065).
- Rechte Leiste: „AGENT IS DOING NOW" (Live-Karte, = F021-Kopf), CHAT/ACTIVITY
  (Aktivitätsfeed + Steering-Eingabe, = F021/F030), TASKS-Liste mit Status
  (Done / In Progress / Planned) und „+ Add Task" (= F028).
- Fußzeile: Phasen-Zeitleiste Job → Planning → Build → Test → Review → Finalized
  mit Unter-Glyphen pro Phase (= F024); Legende: `</>` LLM-Action, Kolben = Test,
  Person = Review.
- Filter-Chips (All / Open / Planned / Done) unten links im Graph.

**H2 — Node-Ontologie.** Nodes sind NICHT nur Tasks. Jede Erzeugung — jeder Prompt,
jeder Run, jedes Artefakt — wird ein Knoten im Netz:

| Node-Typ | Entsteht wenn | Glyphe (lt. Design) | Eltern |
|---|---|---|---|
| Job-Kern | Job startet | großes `</>` im Zentrum | — |
| Task | Planner erzeugt Task | Kreis-Node am Ast | Job-Kern |
| Builder-Run | Builder-Prompt startet | `</>` klein | Task |
| Review-Run | Reviewer-Prompt startet | Person | Task |
| Repair-Run | Repair-Runde startet | `</>` mit Wiederhol-Ring | Builder-Run |
| Test-Run | Testausführung | Kolben | Task |
| Prompt-Ereignis | jeder einzelne Provider-Call | Synapsen-Punkt auf der Kante | jeweiliger Run |
| Artefakt | Diff/Datei/Report erzeugt | Dokument-Punkt | erzeugender Run |

Statusfarben aus der Design-Legende: Open = violett, Planned = klein/blass,
In Progress = pulsierend blau mit Kantenpartikeln, Done = grün, Failed/Blocked = warm
(einzige Warnfarbe im sonst kühlen Schema).

**H3 — Semantische Zoomstufen (menschenfreundliche Festlegung).** Tiefe entsteht
durch Zoom ODER Klick — beides führt zur selben Stufe:

- **L0 Organismus:** Nur Job-Kern + Task-Nodes + Ast-Struktur. Runs sind zu
  Leucht-Aktivität ihrer Task-Äste aggregiert. Das ist die Standard- und
  Beruhigungsansicht: ein Blick genügt für „wie geht es meinem Projekt".
- **L1 Task aufgeklappt:** Klick/Zoom auf einen Task expandiert NUR diesen: seine
  Builder-/Review-/Repair-/Test-Run-Kinder sprießen sichtbar; Geschwister-Tasks
  dimmen (Fokus+Kontext). Immer nur EIN Task gleichzeitig expandiert.
- **L2 Run:** Klick auf einen Run-Node öffnet das Detail-Popover (existiert):
  Verdict, Tokens/Kosten, Dauer, Prompt-Zusammensetzung, Diff-Link. Prompt-
  Ereignisse des Runs werden als Synapsen-Punkte auf seiner Kante sichtbar.
- **L3 Evidenz:** Klick auf Artefakt/Prompt-Punkt öffnet das Seitenpanel
  (Diff-Viewer F037, Prompt-Trace, Node-Chat F038). Textinhalte werden NIE im
  Graph gerendert — der Graph bleibt Organismus, das Panel ist die Lupe.

**H4 — Menschlichkeits-Regeln:**
- Progressive Enthüllung: pro Stufe kommt genau EINE neue Informationsschicht dazu.
- Aggregation statt Überwältigung: >8 Kind-Nodes eines Typs kollabieren zu einem
  Cluster-Node („+12 Runs"), Klick expandiert.
- Orientierung: Brotkrumen-Anzeige (Job › Task › Run), Esc = eine Stufe zurück,
  Doppelklick auf Leere = L0.
- Live-Wachstum: neue Nodes sprießen animiert aus ihrem Eltern-Node (F019) — bei
  Reduced-Motion: sanftes Einblenden statt Wachstumsanimation.
- Performance: L0 rendert auch bei 500 Gesamt-Nodes flüssig, weil Runs aggregiert
  sind (Budget aus F044).
