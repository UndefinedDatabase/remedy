# REMEDY MASTERPLAN — Feature-Detailpläne (150 Files)

Jedes Feature des Masterplans (docs/roadmap/ROADMAP.md, v3.0) hat hier ein eigenes
Detail-File: `features/T{tier}_F{nnn}.md`. Diese Files sind die Arbeitsgrundlage für
den Orchestrator (GPT im Web ODER später Remedy selbst): Sie enthalten IST-Bezug,
konkrete Namen (Module, CLI, API), Task-Schnitt, Akzeptanz-Checks, Tests und Risiken.

**Nutzung:** Dem Orchestrator werden pro Block nur der Masterplan + die 1–3 gerade
aktiven Feature-Files übergeben. Der Orchestrator formt daraus die finalen
self_run_goal-Prompts — die Files sind die Spezifikation, nicht der Prompt selbst.

**Verbindlichkeit der Namen:** Alle Namen (CLI-Befehle, Endpoints, Modulpfade,
Event-Typen, CSS-Variablen) sind in `CONVENTIONS.md` registriert und werden von
allen Features geteilt. Abweichungen nur mit Update von CONVENTIONS.md.

## Ausführungsreihenfolge (lt. Masterplan A5 inkl. Ausnahmen)
1. Tier 0: F001–F012 (Fundament)
2. Tier 9: F146–F148 (Projektbindung & CLI — A5-Ausnahme, vor F013)
3. Tier 1: F013–F044 (Cockpit) — parallelisierbar mit Tier 5 (F103–F116)
4. Tier 2: F045–F068 (Langläufer & Idea Engine)
5. Tier 3: F069–F086 (eigener Orchestrator)
6. Tier 4: F087–F102 (Design-to-Code)
7. Tier 6: F117–F128 + F149–F150 (Memory-Karten)
8. Tier 7: F129–F142 (Qualität & Vertrauen)
9. Tier 8: F143–F145 (Flaggschiffe)

## Datei-Liste
T0: F001–F012 · T9: F146–F148 · T1: F013–F044 · T2: F045–F068 · T3: F069–F086
T4: F087–F102 · T5: F103–F116 · T6: F117–F128, F149, F150 · T7: F129–F142 · T8: F143–F145
