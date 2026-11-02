# Vorbereitung auf die Open-Book-Klassenarbeit

Termin: Mittwoch, 4. November 2026, 30 Minuten. Alle gedruckten Unterlagen und schriftlichen Notizen sind erlaubt; das iPad ist in der Klassenarbeit nicht erlaubt. Pflicht: A1–A8; eine freiwillige Bonusaufgabe zu A9/A10.

## Einstieg und Führung

In `lernweg.html` stehen der Einstieg „Bereit für die Klassenarbeit?“ und ein Eintrag in „Alle Aufträge“. `vorbereitung.js` führt durch fünf Schritte (5 + 8 + 15 + 10 + 7 Minuten). Zeitangaben sind Orientierung, keine Sperren. Der normale A1–A10-Fortschritt bleibt unverändert. Vorbereitungs-Schritt, Abschluss-Checkliste und offene Frage werden separat lokal gespeichert; einzelne Quizantworten nur während des aktuellen Seitenbesuchs.

`vorbereitung-daten.js` enthält vier Themenbereiche mit je drei Aufgaben sowie je einer ähnlichen zweiten Aufgabe für jeden Fehler. Jede Auswahl nennt ausdrücklich Einfach- oder Mehrfachauswahl. Rückmeldungen erklären die Antwortteile und verweisen auf die Mappe. Die Vorbereitung erteilt keine Note und setzt keine neue Prüfungshürde.

Die Übungsphase nutzt `materialien/mini-probe-vorbereitung.pdf`: eine zweiseitige A4-PDF mit eigenen Übungsaufgaben A1–A8, die in Goodnotes importiert und dort bearbeitet wird. Erst danach öffnen die Lernenden in Schritt 5 die Lösungen und verbessern ihre Antworten direkt in der PDF. Es werden keine Aufgaben oder Lösungen der tatsächlichen Klassenarbeit eingebunden.

## Rätselhinweis

Der modale Hinweis erscheint ausschließlich am **1. und 2. November 2026**, jeweils nach dem Kalenderdatum in Europe/Berlin. Das Lösungswort ist **MAPPE**; Groß-/Kleinschreibung und äußere Leerzeichen sind gleichgültig. Escape und Antippen des Hintergrunds schließen den Hinweis nicht. Eine falsche Antwort speichert keine Bestätigung. Erst die richtige Eingabe speichert eine Bestätigung pro Tag und öffnet die Vorbereitung. Ohne verfügbaren Browser-Speicher gilt die Bestätigung nur im laufenden Seitenbesuch. Bei Rückkehr zur Seite oder Wechsel zurück zum Tab wird das Datum erneut geprüft. Es gibt keine serverseitige Lesebestätigung.

## Prüfung

JavaScript: `node --check vorbereitung.js`

Bestehende Regression: `node tests/zwischencheck.test.cjs`

DOM-Integrationstests benötigen jsdom; isoliert ohne Änderungen an Projekt-Abhängigkeiten:

```sh
npm install --prefix /tmp/holz-vorbereitung-test jsdom --no-audit --no-fund
NODE_PATH=/tmp/holz-vorbereitung-test/node_modules node tests/vorbereitung.test.cjs
```

Abgedeckt: Datumsgrenzen einschließlich Berliner Mitternacht, tägliche Bestätigung, falsche/richtige Eingabe, Escape, alle 24 Aufgabenlösungen, Mehrfachauswahl, unvollständige Antworten, zweite Aufgaben, alle fünf Schritte, Papierlink, Lösungen, Abschluss, unveränderter Kursfortschritt und verweigerter Browser-Speicher.
