# Verbindliche Leitlinien · WP Technik 7

Gesamtschule NRW, sechs Wochen, iPads und persönliche Papiermappe. Jede Woche Montag 45 Minuten und Mittwoch 90 Minuten, insgesamt 18 Unterrichtsstunden (810 Minuten).

**Digital macht sichtbar, führt und unterstützt. Papier dokumentiert das Lernen.**

## Arbeitsweise bei Änderungen

1. Vorhandene Dateien prüfen und funktionierende Visualisierungen erhalten.
2. Arbeitsergebnisse auf Papier verlagern; keine vollständigen schriftlichen Schülerleistungen ausschließlich digital speichern.
3. Die gleichzeitig sichtbare Information reduzieren. Immer die Frage beantworten: „Was soll ich jetzt tun?“
4. Eindeutige Blatt- und Unteraufgaben-IDs verwenden. Dateinamen möglichst beibehalten.
5. Hilfen auf Nachfrage stufenweise öffnen; freiwillige Vertiefung vom Pflichtteil trennen.
6. Rückkehr zum aktuellen Schritt im Lernweg sicherstellen.
7. Auf iPad, bei Vergrößerung und mit Tastatur prüfen. Bestehende Funktionen auf Regressionen prüfen.

## Single-Step-Lernweg

Anzeige: Auftrag, aktueller Schritt, Medium, eine konkrete Handlungsanweisung, höchstens ein Hauptbutton und ggf. ein Hilfebutton. Fortschritt bleibt sichtbar. Wochen- und Gesamtübersicht nur über „Lernweg ansehen“ öffnen.

Beispiel: „A4 · Schritt 2 von 5. 📱 Öffne den Schnittplan und probiere zwei Pläne aus.“ Danach: „📁 Öffne deine Mappe bei A4.1. Trage die Ergebnisse ein.“

Nach dem Pflichtabschluss: „Deine Pflichtaufgabe ist geschafft. Möchtest du das Thema noch vertiefen?“ Auswahl zwischen nächstem Auftrag und Vertiefung. Eine Videovertiefung ersetzt niemals die Produktkarte auf Papier.

Hilfekaskade: kleiner Denkanstoß → Wortspeicher → Satzanfang/Struktur → stärkere Lösungshilfe. Jeweils nur die nächste Hilfe auf Nachfrage zeigen.

## Gemeinsame Symbole

- 📁 MAPPE: Papierarbeit.
- 📱 iPAD: digitales Material.
- 📖 LESEN: Information.
- 🔬 ERKUNDEN: ausprobieren und beobachten.
- 💡 HILFE: freiwillige Unterstützung.
- 🔍 VERTIEFUNG: freiwillige Zusatzaufgabe.
- 🛑 HALTEPUNKT: Lehrkraft oder Partner einbeziehen.
- ✓ KONTROLLE: Pflichtteil überprüfen.

## Lernweg und Papier-IDs

Die Unteraufgaben-IDs sind in der 16-seitigen Holzforscher-Mappe und im Navigator umgesetzt.

| Woche | Auftrag | Papier |
|---|---|---|
| 1 | A1 Baumscheibe | A1.1: Borke, Bast, Kambium, Splintholz, Kernholz, Mark |
| 1 | A2 Jahresringe | A2.1: Alter; A2.2: Ring untersuchen und Vermutung begründen |
| 2 | A3 Produktionskette | A3.1: Baum, Fällen, Transport, Sägewerk, Einschnitt, Schnittholz mit je einem Satz |
| 2 | A4 Schnittplan | A4.1: zwei Pläne, Bretter und Ausbeute; A4.2: Verschnitt und Vergleich |
| 3 | A5 Prüflabor | A5.1: Aussehen, Masse, Härte, Wasseraufnahme |
| 3 | A6 Prüfbericht | A6.1: Beobachtung, Eigenschaft, Verwendung für zwei Holzarten |
| 3/4 | A7 Trockenversuch | A7.1: vorher/nachher mit Datum, Masse, Breite, ggf. Dicke; A7.2: Auswertung |
| 4 | A8 Holzfehler | A8.1: Riss, Ast, Verwerfen; A8.2: Erklärung und technische Folge |
| 5 | A9 Beratung | A9.1: Anforderungen; A9.2: Holzart, drei Eigenschaften, Nachteil, Begründung |
| 5 | A10 Produktkarte | A10.1: Produkt, Holzart, Begründung, Nachteil |
| 6 | Kompetenzcheck | konkrete Papierübungen; anschließend Lernnachweis |

Die feuchten Proben für A7 müssen in Woche 3 vorbereitet und gemessen werden. Mehr Masse bei gleichem Volumen und vergleichbarer Feuchte belegt höhere Dichte, nicht automatisch größere Härte. Keine eindeutige Wetterursache aus einem Jahresring ableiten.

## Bestands-Apps weiterentwickeln

- `baumscheibe.html`: Erkunden, Beschriften und Ringe erhalten; schriftliche Vermutungen/Expertenantworten auf Papier. Zielparameter `modus=entdecken` und `modus=ringe`.
- `produktionskette.html`: Sortieren und Kontrolle erhalten; Satzfelder entfernen.
- `schnittplan.html`: Simulation, Schnittlinien, Ausbeute und zwei Pläne erhalten; schriftliche Auswertung auf Papier.
- `pruefstation.html`: Stationsanleitung, Messhinweise und Wortspeicher; keine digitale Ergebnistabelle oder Berichte. Zielparameter z. B. `station=gewicht`.
- `holzfehler.html`: Zuordnung und Visualisierung erhalten; Pflicht Riss/Ast/Verwerfen, Vertiefung z. B. Schüsseln/Verdrehen/Harzgalle. Schriftliche Erklärung auf Papier. Zielparameter `modus=zuordnen`.
- `steckbriefe.html`: fünf Holzarten Fichte/Kiefer/Buche/Eiche/Birke und Vergleich erhalten. Kundenberatung und Begründung auf Papier. Zielparameter z. B. `auftrag=schneidebrett`.
- `kompetenzcheck.html`: Selbsteinschätzung darf digital bleiben. Konkrete Übung mit Papier-ID und Rückweg empfehlen.

Die genannten Parameter sind implementiert; zusätzlich gibt es in der Baumscheibe den Modus beschriften und bei Holzfehlern den Modus vertiefung.

## Papiermaterialien und Lehrkraftbereich

Vorhanden: Deckblatt, Lernwegübersicht, A1–A8, acht A9-Kundenkarten, A9-Beratungsbogen, A10-Produktkarte, Kompetenzcheck-Papieroption sowie Übungs- und Vertiefungsblatt. Offen: Lernnachweis und Erwartungshorizont. Schüleraufträge in einfacher Sprache und Du-Form.

Lehrkraft-Cockpit: vollständiger Ressourcenüberblick mit ehrlichem Verfügbarkeitsstatus, Vorbereitung, Themenwochen, kurzen Inputs, Haltepunkten und Berufeporträts. Keine offenen Aufgaben als vorhandene Dateien verlinken.

Kurzinputs: Phänomen → Beobachtung → Leitfrage → kurze Klärung → Lernweg. Berufe: Forstwirt/in, Holzbearbeitungsmechaniker/in, Holztechniker/in und Tischler/in bzw. Schreiner/in. Keine langen Berufsorientierungsblöcke.

Das Cockpit ist eine Material- und Planungsansicht, kein Zugangsschutz. Vor einer späteren Bereitstellung von Prüfungslösungen prüfen, wie diese für Lernende unzugänglich bleiben.
