# WP Technik 7 · Vom Baum zum Holz

**Die Mappe ist der Arbeitsort. Die Website ist der Lernnavigator.**

## Unterricht und Zugänge

6 Wochen, jede Woche Montag 45 Minuten und Mittwoch 90 Minuten: 18 Unterrichtsstunden / 810 Minuten.

- `index.html`: Einstieg für Lernende und Lehrkräfte.
- `lernweg.html`: A1–A10 als einzelne Schritte, gestufte Hilfen und freiwillige Vertiefungen.
- `lehrkraft.html`: Wochenabläufe, Ressourcen, Materialvorbereitung und Kurzinputs.
- `materialien/holzforscher-mappe.pdf` und `.docx`: 16-seitige Papiermappe.
- `materialien/kundenkarten.pdf` und `.docx`: acht Kundenkarten auf vier Seiten.
- Weitere PDFs im Materialordner: einzelne Aufträge zum Nachdrucken.

## Technik

Statische HTML/CSS/JS-Dateien; kein Build-Schritt nötig. Lokal mit `python -m http.server 8765` starten.

`kurs-daten.js` enthält die Aufträge und Kundenkarten. `tools/build_course.py` erzeugt diese Datei. `tools/build_mappe.py` erzeugt die DOCX-Dateien und das Beschriftungsbild; benötigt Python mit python-docx und Pillow sowie den table_geometry-Helfer des Documents-Skills. DOCX anschließend rendern und visuell prüfen; `tools/split_materials.py` übernimmt geprüfte PDFs und erzeugt Einzelblätter.

`cockpit-daten.js` enthält Wochenplanung und Ressourcenstatus. Nach Materialänderungen diese Zuordnung aktualisieren. Papier-IDs und Navigator müssen immer übereinstimmen.

## Navigation und Speicherung

Navigator: `hbg_holz_navigator_v2` speichert aktuellen Auftrag/Schritt, Pflichtabschlüsse, verwendete Hilfestufen und abgeschlossene Vertiefungen lokal. Alte Daten der früheren Lernwegversion werden nicht gelöscht oder als neue Abschlüsse übernommen.

App-Aufrufe tragen `von=A1` usw. Der Rückweg führt zum aktuellen Auftrag. Für bewusstes Wiederholen, etwa aus dem Kompetenzcheck: `lernweg.html?auftrag=A7&wiederholen=1`.

App-Modi: `baumscheibe.html?modus=entdecken|beschriften|ringe`, `pruefstation.html?station=aussehen|gewicht|haerte|wasser`, `holzfehler.html?modus=zuordnen|vertiefung`, `steckbriefe.html?auftrag=schneidebrett` (weitere IDs in kurs-daten.js).

Die Apps behalten Zuordnungs- und Simulationszustände. Schriftliche Leistungen werden nicht mehr digital eingegeben. Vorhandene ältere Daten werden nicht gelöscht. Die Lehrkraft-Vorbereitung verwendet einen separaten Speicher. Es gibt keine Synchronisierung und keine Klassenübersicht über Schülerleistungen.

## Prüfungspaket

Auf ausdrücklichen Wunsch vorläufig im öffentlichen Lehrkraftbereich: `lehrkraft-material/pruefung/`. Lernerfolgskontrolle (60 Minuten) und Erwartungshorizont mit dreistufigem Kompetenzraster, jeweils PDF und DOCX. Das ZIP enthält das komplette Paket. Vor Reihenbeginn in das geschützte Dateisystem übertragen; Anleitung im Paket beachten. Die Dokumente sind nicht im Lernnavigator oder in der Schülermappe verlinkt. Frühere Git-Versionen und Deployments können weiterhin erreichbar bleiben.

Fachliche Hintergrundquellen: [GD Holz: Quellen und Schwinden](https://holzvomfach.de/fachwissen-holz/wissenswertes/holzwissen/quellen-und-schwinden/), [GD Holz: Holzfeuchte](https://holzvomfach.de/fachwissen-holz/glossar/holzfeuchte-gl/) und [Waldwissen: Jahrringanalyse](https://www.waldwissen.net/de/waldwirtschaft/schadensmanagement/jahrringanalyse). Die Unterrichtsmodelle vereinfachen; Ringbreite allein belegt keine eindeutige Wachstumsursache.
