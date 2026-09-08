# WP Technik 7 · Vom Baum zum Holz

Hybride Unterrichtsreihe: **Die Mappe ist der Arbeitsort. Die Website ist der Lernnavigator.**

## Zugänge

- `index.html`: Auswahl zwischen Lernweg und Lehrkraft-Cockpit.
- `lehrkraft.html`: Wochenplanung, Ressourcenregister, Vorbereitung, druckbare Kurzinputs und Berufekarten.
- `lernweg.html`: vorhandener Lernweg; der geplante Single-Step-Umbau steht noch aus.

Das Projekt besteht aus statischen HTML-, CSS- und JavaScript-Dateien ohne Build-Schritt. Lokal zum Beispiel mit `python -m http.server 8765` starten.

## Cockpit

`cockpit-daten.js` enthält sechs Themenwochen und den Ressourcenbestand. `cockpit.js` steuert Navigation, Suche, Filter und Vorbereitungshäkchen; `cockpit.css` enthält Bildschirm- und Drucklayout.

Direkte Links sind beispielsweise `lehrkraft.html#woche-3`, `lehrkraft.html#ressourcen` oder `lehrkraft.html#vorbereitung`.

Ressourcenstatus:

- **Vorhanden**: im Cockpit nutzbarer Inhalt.
- **Umbau offen**: funktionierende Bestandsseite, die noch an das hybride Konzept angepasst werden muss.
- **Fehlt**: noch keine Datei. Deshalb kein Downloadlink.

Wenn ein Papiermaterial erstellt wird, im Ressourcenregister den tatsächlichen Pfad hinterlegen und den Status aktualisieren. Die geplanten Unteraufgaben-IDs in den Wochenansichten und auf dem Papier müssen übereinstimmen. Die Bestands-Apps unterstützen die geplanten URL-Modi noch nicht; deshalb nutzt das Cockpit deren Grundadressen.

Die Lehrkraft-Vorbereitung liegt ausschließlich im lokalen Browser-Speicher unter `hbg_holz7_lehrkraft_v1`. Es gibt keine Klassenübersicht über Schülerfortschritte und keine Synchronisierung zwischen Geräten. Das Cockpit verwendet keine Daten der bestehenden Lernseiten.

## Zeitraster

Die Angabe „montags Einzelstunde, mittwochs Doppelstunde im Wechsel“ lässt zwei Planungsvarianten zu. Das Cockpit startet deshalb ohne festgelegten Rhythmus:

- Wochenweise wechselnd: 9 Unterrichtsstunden / 405 Minuten über sechs Wochen. Für den gesamten geplanten Umfang muss Zeit oder Pflichtumfang angepasst werden.
- Beide Termine jede Woche: 18 Unterrichtsstunden / 810 Minuten über sechs Wochen.

## Noch offene Arbeiten

Papiermappe und Vorlagen A1–A10 einschließlich Kundenkarten, Papier-Kompetenzcheck, Lernnachweis und Erwartungshorizont fehlen. Anschließend bzw. abgestimmt darauf: Single-Step-Lernweg, gestufte Hilfen, freiwillige Vertiefungen, Rückwege und Parameter für die Apps sowie Verlagerung schriftlicher Leistungen aufs Papier.

Die vollständigen didaktischen Leitlinien stehen in `UNTERRICHTSKONZEPT.md`.
