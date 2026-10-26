**Kurz:** Das entscheidet nicht eine einzelne Datei, sondern zwei zusammen. `packages/orchestration/do_lane.py` steuert die Entscheidung und trifft das letzte Wort. `packages/orchestration/scope_decision.py` stellt dem Planner die eigentliche Frage „ein Job oder mehrere?“.

## Ablauf: `settle_do_lane` in `packages/orchestration/do_lane.py:398-420`

1. **Regex-Routing zuerst.** `select_do_lane` (`do_lane.py:209-244`) wählt eine Lane:
   - `bounded`: ein Job mit wenigen, ausdrücklich genannten Dateien.
   - `full`: der Planner plant Milestones.
   - `hold`: eine Rückfrage statt einer Vermutung.

   Ein Auftrag mit mehreren Projekten oder mit `--force-mission` geht immer auf `full`. Mit `--force-job` wird er `bounded`, außer bei einem `hold`.

2. **„Ein Job“ ohne Nachfrage.** `order_single_job_reason` (`do_lane.py:188-206`) prüft zwei Fälle:
   - Der Kopf der Auftragsdatei sagt `shape: single-job`. Die Konstante `ORDER_SHAPE_SINGLE_JOB` steht in `packages/orchestration/order_file.py:44`.
   - Der Text nennt genau eine Datei.

   Trifft einer davon zu, wird der Auftrag ein Job ohne Milestones, und der Planner wird nicht gefragt.

3. **Wann der Planner gefragt wird.** `asks_scope_decision` (`do_lane.py:357-368`) entscheidet das. Nicht gefragt wird:
   - bei `--no-llm`, `--force-job`, `--force-mission` oder mehreren Projekten,
   - bei einem `hold`,
   - bei einem Auftrag, der keine Änderung verlangt,
   - wenn Schritt 2 schon „ein Job“ ergeben hat,
   - bei einem `bounded`-Auftrag, dessen Text seine Dateien selbst nennt.

4. **Die Frage an den Planner.** `decide_order_scope` (`scope_decision.py:70-115`) schickt dem Planner (Standard `claude-cli`) den Auftrag, höchstens 2000 getrackte Pfade (`SCOPE_DECISION_MAX_PATHS`) und eine feste Frage, die einen Job bevorzugt. Die Antwort ist genau ein JSON-Objekt:
   - `single_job`
   - `files`
   - `reason` (ein deutscher Satz)

   Daraus wird das Ergebnis `decided`:
   - **`several_jobs`** nur, wenn `single_job: false` **und** ein nicht leerer `reason` vorliegt (`scope_decision.py:110-113`).
   - **`one_job`** sonst, also der Standard. Das gilt auch bei `false` ohne Begründung.
   - **`regex_fallback`**, wenn der Planner nicht erreichbar ist, der Aufruf fehlschlägt oder die Antwort auch nach einem erneuten Parse-Versuch ungültig bleibt. Aus einer unbrauchbaren Antwort wird keine Größe geraten (`scope_decision.py:11-13`).

5. **Das Ergebnis anwenden.** `lane_after_scope_decision` (`do_lane.py:371-395`) setzt das Ergebnis um:
   - `several_jobs`: die `full`-Lane mit Milestones, also mehrere Jobs.
   - `one_job`: Eine `bounded`-Lane bleibt `bounded`, wenn die Dateien des Planners darin enthalten sind. Sonst wird der Auftrag `full`, aber als **ein** Job ohne Milestones, dessen Tasks der Planner plant.
   - `regex_fallback`: Die Lane aus Schritt 1 bleibt unverändert.

Die Entscheidung wird als Beleg in `scope_decision.json` im Evidence-Ordner jedes Jobs gespeichert (`record_scope_decision`, `scope_decision.py:118-127`).

## Dateien, auf denen die Antwort beruht
- `packages/orchestration/scope_decision.py`
- `packages/orchestration/do_lane.py`
- `packages/orchestration/order_file.py` (nur die Konstante `shape: single-job`)
