# Handoff — operator amendment amend1024-one-real-order (session 1, closing)

Branch `feature/amend1024-one-real-order`, merged into `main`. Feature F317 accepted; next line under
Rule A5: F316. The handback below is the one written to
`~/.remedy-loop/amend1024-one-real-order.handback.md`, copied unchanged.

# Übergabe — Operator-Amendment amend1024-one-real-order

Stand: 25. Oktober 2026. Zweig `feature/amend1024-one-real-order`, nach `main` gemergt und gepusht.
Zu Beginn der Sitzung war ein Pull Request offen (#390, F158). Das Open-PR-Gate hat ihn gemergt,
bevor die Arbeit begann.

## Was ist jetzt Standard?

Der Standard für Planer, Bauer, Prüfer und Reparatur ist jetzt das Claude-Code-Programm `claude-cli`.
Pi mit dem lokalen Modell `muse-glimmer:latest` über Ollama bleibt wählbar. Man wählt es mit
`--builder-provider pi` oder mit `builder = "pi"` in der Tabelle `[roles]` der Datei `.remedy/config.toml`.
Alle anderen Rollen wie `study`, `summary` und `teacher` behalten ihr lokales Modell.

Der Planer liest jetzt die Tabelle `[roles]` genauso wie Bauer und Prüfer. Damit ist der Befund
R-1448 geschlossen. Die Reihenfolge ist: Kommandozeilen-Flag, gespeicherter Job, Tabelle `[roles]`,
dann `planner.provider` aus `remedy.toml`, dann der Produktstandard.

Über die öffentliche HTTP-API gilt dasselbe für einen Client mit `host_tools`. Für jeden anderen
Aufrufer, auch für das eigene Token des Servers, bleibt alles wie bisher. Die Route gibt ihm `pi`, `pi`
und `ollama` mit, solange weder der Auftrag noch die Tabelle `[roles]` des Projekts etwas anderes
nennt.

Die Größe eines Auftrags entscheidet jetzt der Planer und nicht mehr ein regulärer Ausdruck. Vor jeder
Meilensteinplanung fragt Remedy den Planer, ob der Auftrag ein Job ist oder wirklich mehrere braucht.
Die Antwort hat genau drei Felder: `single_job`, `files` und `reason`. Sie liegt in jedem Job als
`scope_decision.json` unter `evidence`. Ein Job ist der Standard. Mehrere Jobs gibt es nur, wenn der
Planer `single_job: false` mit einer Begründung liefert. Ein Auftrag mit der Kopfzeile
`shape: single-job` wird nicht gefragt. Die alten Lanes aus `do_lane.py` entscheiden nur noch, wenn
der Planer nicht erreichbar ist oder keine brauchbare Antwort gibt.

Der claude-cli-Bauer darf jetzt Bash benutzen, aber nur für eine feste Liste:
- den Testbefehl des Projekts,
- `python -m pytest`, `python3 -m pytest` und `pnpm test`,
- `git status`, `git diff` und `git log`,
- `ls`, `cat`, `head`, `tail`, `wc`, `grep` und `rg`,
- `py_compile`, `pnpm build` und `pnpm lint`.

Jeder abgelehnte Befehl wird als Nachweis protokolliert. Der Modus `dangerous-skip` ist unverändert.

Ein claude-cli-Bauer zeichnet seinen Aufruf jetzt standardmäßig als Stream auf. So ist jeder Befehl,
den er ausgeführt hat, im Nachweis sichtbar.

Dollarbeträge erscheinen nur noch, wenn `cost.show_usd = true` in `remedy.toml` steht. Das gilt für
`remedy stats`, `remedy job show`, `remedy do` und die öffentliche API. Standardmäßig zeigen sie Tokens
und Aufrufe. Die Befehle `remedy stats valuations`, `remedy stats recompute-costs` und
`remedy worker pricing-update` sind als fortgeschritten markiert und fehlen in der Standardhilfe. Sie
laufen aber weiter.

## Hat der echte Lauf geklappt, und wie viele Tokens hat er gebraucht?

Ja. Das Testprojekt lag unter `/tmp/amend1024-g/greet-project`: ein Paket mit zwei Modulen, einer
README und drei Tests. Ein Client mit `host_tools` hat den Auftrag über die öffentliche API
eingereicht, ohne Dateipfad und ohne Formkopfzeile. Der Auftrag lautete: „Die Funktion, die den Gruß
baut, soll den Namen auch dann groß schreiben, wenn er klein getippt wurde. Die README bekommt einen
Satz dazu.“ Der Kopf enthielt nur, was die API verlangt: das Projekt sowie `max-total-tokens: 300000`
und `max-provider-calls: 40`.

Der zweite Lauf (Auftrag `e4eaaaa9cebd3304`, Job `24270f620da248bc`) ist so gelaufen:
- claude-cli hat entschieden, dass es ein Job ist, und hat einen deutschen Satz als Begründung
  geschrieben.
- Genau ein Job wurde gebaut.
- Der Bauer hat `python3 -m pytest -q` selbst ausgeführt. Er sah „5 passed“ und später „9 passed“.
- Der Prüfer hat alle drei Aufgaben mit `pass` angenommen.
- `remedy job apply` hat die Änderung ins Testprojekt gebracht. `greet/core.py` schreibt den Namen
  jetzt groß, die README hat einen Satz dazu, und es gibt sechs neue Tests. Danach liefen dort 9 Tests
  grün.

Der Lauf hat 9 Aufrufe gebraucht, in gut 2 Minuten:
- Die 6 Aufrufe von Bauer und Prüfer brauchten 36 Eingabe-Tokens und 5.193 Ausgabe-Tokens. Dazu kamen
  135.803 Tokens aus dem Cache und 22.317 Tokens, die in den Cache geschrieben wurden.
- Die 3 Planeraufrufe brauchten geschätzt etwa 3.500 Tokens.
- Das Auftragsbuch zählt 8.711 Tokens.

Ein erster Lauf (Auftrag `3a45850644d6d551`) hat ebenfalls eine richtige Änderung geliefert. Er
brauchte 11 Aufrufe und 11.820 Tokens. Damals fehlte aber der Stream des Bauers, also war nicht zu
sehen, dass er die Tests selbst ausgeführt hatte. Ich habe dieses Ergebnis absichtlich abgelehnt und
den Stream zum Standard gemacht. Dann habe ich den Auftrag erneut geschickt.

Der vollständige Nachweis liegt unter `evidence/current/f317_real_order/` mit einer README. Es gibt
keinen `manual_operator_repair`. F317 ist in `docs/roadmap/STATUS.md` angenommen.

## Welche Umgebungsvariable hat beim echten claude-Aufruf gefehlt?

Für einen funktionierenden Aufruf hat auf dieser Maschine keine Variable gefehlt.

Ich habe zwei echte Aufrufe gemacht:
- Mit der neuen Liste hat der Aufruf in 6,8 Sekunden die verlangte Datei angelegt.
- Mit der alten Liste aus F152 als Gegenprobe hat der Aufruf ebenfalls funktioniert, in 11,4 Sekunden.

Der Grund für das zweite Ergebnis: Der `claude`-Wrapper aus `~/Repos/system/bin` steht als erster auf
dem Pfad. Wenn `CLAUDE_CONFIG_DIR` fehlt, wählt er selbst ein aktives Profil. Ohne diese Variable
könnte ein Bauer deshalb auf einem anderen Ihrer Konten laufen als die Sitzung, die ihn gestartet hat.
Deshalb wird `CLAUDE_CONFIG_DIR` jetzt durchgereicht, zusammen mit den anderen elf Namen aus D1.

Beide Ergebnisse stehen unter `evidence/current/claude_cli_real_binary_check*.json` und in
`docs/adr/0002-claude-cli-worker-isolation.md`.

## Welche Features wurden geparkt?

22 Features stehen jetzt in Package 2 mit dem Vermerk „geparkt bis F317 dreimal in Folge auf Luna
geklappt hat“:
- F153, F155, F154 und F161,
- F067 und F065,
- F130, F132, F136, F137, F142 und F143,
- F088, F091, F092, F093, F095, F097, F099, F100, F101 und F102.

33 Features habe ich nicht geparkt. Sonst wäre eine Abhängigkeit zerrissen, denn Features, die aktiv
bleiben, nennen sie in ihrer Zeile „Depends on“. Betroffen sind:
- der ganze Tier 4,
- F073, F063, F064 und F066,
- F129, F131, F134, F135, F138, F139 und F140,
- F087, F089, F090, F094, F096 und F098.

Das steht als Frage Q28 in `.agent/operator_questions.md`. Meine Empfehlung dort ist, die abhängigen
Features ebenfalls zu parken.

F316 bleibt offen, aber ohne R-1448. Die übrigen Befunde schließt keiner der Teile A bis E.

## Was muss der Operator auf seiner Maschine noch tun?

Remedy muss nicht neu installiert werden. Die Installation ist editierbar und zeigt auf
`~/Repos/remedy`. Jeder neue Aufruf von `remedy` läuft also schon mit dem neuen Code, sobald `main`
ausgecheckt ist.

Den langlaufenden Supervisor (Prozess 740108, seit dem 20. Oktober auf Port 8450) müssen Sie neu
starten. Sein HTTP-Teil läuft noch mit altem Code im Speicher und gibt Clients ohne `host_tools` die
lokalen Standards nicht mit. Die Läufe, die er startet, nutzen aber schon den neuen Standard
claude-cli. Neu starten Sie ihn mit:

    remedy serve stop
    REMEDY_SERVE_API_PORT=8450 remedy serve start

Erst nach dem Neustart gewähren Sie dem Universe-Client `host_tools`. Dann laufen seine Aufträge mit
claude-cli. Für das Orb des Universums ist das dieser Befehl:

    remedy client grant-host-tools orb-universe

Für die anderen beiden Clients geht es genauso:

    remedy client grant-host-tools orb-remedy
    remedy client grant-host-tools luna

Prüfen können Sie das Ergebnis mit `remedy client show`.

Es gibt keinen Befehl, der einen neuen Client anlegt. Einen Client trägt man von Hand in
`.data/api/clients.json` ein, mit Dateirechten 0600, so wie es `docs/system/public-http-api-v1.md`
beschreibt. Ich habe das im echten Lauf genau so gemacht.

Beantworten Sie bitte Q28.

Nach Belieben können Sie die Reste des gelöschten Cockpits entfernen: `apps/ui/dist`,
`apps/ui/node_modules`, `apps/ui/legacy` und `apps/ui/.data`. Sie sind nicht versioniert, und ich
habe sie nicht angefasst.

Der Supervisor des Testlaufs ist beendet. Das Testprojekt und seine Daten liegen noch unter
`/tmp/amend1024-g`. Den Ordner können Sie löschen.

## Abweichungen vom Auftrag

- Den Schlüssel `dod.test_command` gibt es in Remedy nicht. Der Testbefehl eines Projekts steht in
  `[tests] command` der Datei `.remedy/config.toml`. Die Erlaubnisliste liest ihn von dort, mit den
  bekannten Rückfällen.
- Die Erlaubnisliste enthält zusätzlich `python3` und erlaubt `pytest` mit beliebigen Argumenten statt
  nur `-q`. Auf dieser Maschine gibt es kein `python`, und ein Bauer muss auch einzelne Testdateien
  laufen lassen dürfen.
- Ein Auftrag im begrenzten Lane, der seine Dateien selbst ausdrücklich nennt, wird nicht nach seiner
  Größe gefragt. Er sagt schon selbst, was er ist, und bleibt ohne Planeraufruf.
- Der Kopf des API-Auftrags enthält das Projekt und die Kappen, weil die API ohne beides ablehnt. Eine
  Formkopfzeile enthält er nicht.
- `apps/ui` habe ich in den Plantexten umgeschrieben. Die 43 Dateien abgeschlossener Features haben je
  einen datierten Hinweissatz bekommen, statt ihre Geschichte umzuschreiben.
- Die Struktur-Ratsche ist für `_cmd_do` (+1 Zeile), `pingpong_provider.py` (+3) und
  `apps/cli/commands/job.py` (+1) angehoben. Für jede steht ein Satz im Struktur-Hauptbuch. Nichts
  wurde künstlich abgespalten.
- Die Teile E und F2/F5 haben zwei Hilfsagenten in eigenen Arbeitsbäumen gebaut. Ich habe ihre Commits
  übernommen, ihre Arbeitsbäume entfernt und alles im gemeinsamen Testlauf geprüft.

## Tests

Der erste vollständige Lauf hatte 67 Fehler. Die Ursachen:
- Tests schrieben den alten Standard fest.
- Gefälschte Planer kannten die neue Größenfrage nicht.
- Durch den Stream-Standard fehlte JSON.
- Mehrere Wächter waren betroffen: die Zahl der breiten `except`, ein verwaister Script-Eintrag, die
  Erreichbarkeitsliste, ein Wort in einer Hilfe und der fehlende Abschnitt in `context.md`.
- Einige Fehler kamen nur aus den Arbeitsbäumen der Hilfsagenten.

Kein Test wurde gelöscht oder abgeschwächt. Tests, die den alten Standard prüfen, wählen ihn jetzt
ausdrücklich.

Neu ist ein Schutz in `tests/conftest.py`: Kein Test erreicht mehr das echte `claude` dieser Maschine.

Der zweite Lauf hatte noch 4 Fehler. Die Interface-Route darf ihre Dollar-Schlüssel nicht verstecken,
weil sie Schlüssel nur beschreibt. Danach war alles grün.

Der letzte vollständige Lauf: `python3 -m pytest -n auto -q --maxfail=400` mit Python 3.10.12,
24.290 Tests bestanden und 11 übersprungen. Er lief vor dem Commit dieser Übergabe auf Commit
`8f4de35b3`. Danach habe ich ihn auf dem endgültigen Baum wiederholt, das Ergebnis steht im Merge-Commit.
`ruff check .` ist grün.

## Stand der Teile

| Teil | Status | Grund |
|------|--------|-------|
| A1 | done | |
| A2 | done | R-1448 geschlossen |
| A3 | done | |
| B1–B4 | done | |
| C1–C3 | done | `dod.test_command` gibt es nicht, siehe Abweichungen |
| D1–D2 | done | keine Variable fehlte, siehe oben |
| E1–E2 | done | |
| F1 | done | F317 registriert und angenommen |
| F2 | deviated | 22 geparkt, 33 bleiben wegen Abhängigkeiten, Frage Q28 |
| F3 | done | |
| F4 | done | |
| F5 | done | |
| G1–G4 | done | zweiter Lauf, der erste wurde absichtlich abgelehnt |
