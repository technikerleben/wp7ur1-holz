# Spielkarten für den offenen Anfang

Zwölf Karten, zwei je Themenwoche. Jede Karte hat drei wählbare Stufen: 1 Superleicht, 2 Weiterdenken, 3 Knobeln. Die Rückseite enthält drei zugehörige Lösungen oder Musterantworten. Keine feste Einteilung der Kinder in Leistungsgruppen. Eine gewählte Stufe genügt; alle Stufen sind zugänglich.

## Drucken

Die PDF ist die verbindliche Druckvorlage: A4 Hochformat, tatsächliche Größe 100 %, eine PDF-Seite pro Blattseite, doppelseitig mit Wenden an der langen Kante. Keine Broschürenfunktion oder Mehrfachseiten verwenden. Alle zwölf Seiten in ihrer Reihenfolge drucken: sechs Blätter ergeben zwölf doppelseitige Karten. Seiten 1/2 gehören zusammen, dann 3/4 usw. Oben liegt auf beiden Seiten dieselbe Karte, unten ebenfalls. An der waagerechten Trennlinie schneiden; Außenränder bei Bedarf beschneiden. Zuerst ein Blatt als Duplexprobe drucken, da Druckertreiber abweichen können. Die Wochen-PDFs enthalten jeweils genau ein solches Vorder-Rückseiten-Paar.

Die Word-Datei ist bearbeitbar. Nach Änderungen Seitenumbrüche und Duplexzuordnung neu prüfen. Die Rückseiten gehören zu diesen Spielkarten und bleiben als Selbstkontrolle für Kinder zugänglich; sie sind keine Prüfungslösungen.

## So beginnt die Stunde

Vorher zwei aktuelle Karten und gegebenenfalls bekannte Karten auslegen. Pro Tischgruppe mindestens einen Satz, bei großen Gruppen doppelt. Ein Schmierzettel und ein Stift reichen für die einzige optionale Schreibvariante auf S11; sonst sind keine Zusatzmaterialien nötig. Ruhige Partnerstimme und Gesten am Platz.

1. Minute: Wähle eine Karte, eine Stufe und allein oder zu zweit.
2.–4. Minute: Löse zunächst selbst. Zu zweit Rollen wechseln.
5. Minute: Drehe um und vergleiche. Entscheide: noch einmal versuchen oder beim nächsten Mal eine höhere Stufe.

Ein gemeinsames Signal beendet die Phase. Karte zurücklegen, dann dem nächsten Unterrichtsschritt folgen. Keine Pflicht, alle drei Stufen zu schaffen; kein Wettrennen und keine Bewertung. Die Karte darf wiederholt werden. Mündliche Spielantworten sind keine verbindlichen Mappenergebnisse. Wenn daraus eine eigene Vertiefung entsteht, dokumentiere sie auf V.1.

Für schwache Leser: mit Stufe 1 beginnen, Partner liest bei Bedarf vor. Die erste Stufe enthält Hinweise und meist nur zwei Auswahlmöglichkeiten. Für stärkere Kinder: eine andere Erklärung oder ein Gegenbeispiel suchen und mit der Musterlösung vergleichen.

## Wochenzuordnung

- Woche 1: S01 Stammgeflüster, S02 Ringrennen
- Woche 2: S03 Sägewerk auf Reisen, S04 Brett oder Pech
- Woche 3: S05 Laborlüge, S06 Fair oder faul
- Woche 4: S07 Holz in Bewegung, S08 Fehlerdetektive
- Woche 5: S09 Kundenpantomime, S10 Wer bin ich aus Holz
- Woche 6: S11 Wahrheitswächter, S12 Knack den Holzcode

Die Wochenplanung berücksichtigt fünf Minuten offenen Anfang in jedem Termin. Der Montag bleibt 45 Minuten, der Mittwoch 90 Minuten. Mittwoch in Woche 6: anschließend fünf Minuten Prüfungsorganisation, 60 Minuten Kontrolle, zehn Minuten Reflexion und zehn Minuten Abschluss.

## Dateien weiterentwickeln

`tools/build_spielkarten.py` erzeugt DOCX und Kartendaten. DOCX rendern, alle Seiten visuell prüfen, die geprüfte PDF ablegen und `tools/split_spielkarten.py` ausführen. Dieses Skript prüft Reihenfolge und Karten-IDs der Duplexpaare und erstellt die Wochenpakete.
