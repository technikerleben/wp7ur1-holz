# Prüfungspaket Holz

5 Seiten Lernerfolgskontrolle (Druckfassung im HBG-AB-Layout: 3 cm Lochrand, Arial, tonersparend ohne Flächen, große Ankreuz- und Eintragekästchen, Punktefeld je Aufgabe, Namensfeld auf jeder Folgeseite; Bonusaufgabe allein auf Seite 5), 30 Minuten, 28 Pflichtpunkte zu A1 bis A8 und 4 freiwillige Bonuspunkte zu A9/A10. Open Book: Das gedruckte Material der Mappe darf genutzt werden; iPad und andere digitale Geräte sind nicht erlaubt. 3 Seiten Erwartungshorizont einschließlich Kompetenzbelegen und individueller Rückmeldung. PDF zum Drucken; DOCX zum Bearbeiten.

Reihenfolgeaufgaben werden nur nummeriert. Kurze Erklärungen und Begründungen erfolgen in Lückensätzen. Jede Auswahlaufgabe nennt ausdrücklich Einfach- oder Mehrfachauswahl. Die Bewertung der Mehrfachauswahl ist im Schülerblatt und Erwartungshorizont beschrieben. Keine freie Langantwort. Nachschlagen, Bearbeiten und Prüfen sind in den 30 Minuten enthalten.

Die frühere a/b/c-Struktur wurde durch eine kürzere Aufgabenfolge ersetzt. Belege für Mindest-, Regel- und Expertenstandard stehen im Erwartungshorizont; die geschlossenen Antwortformate belegen kein selbstständiges ausführliches Argumentieren.

## Bewertung (Regelfassung)

Drei Schritte, Kompetenz vor Note (Erwartungshorizont S. 3, Rückmeldebogen S. 4):
1. Kompetenzstand je Bereich: sicher ab 75 %, teilweise ab 45 %, darunter „noch nicht“.
2. Bestehen nur über die Pflichtpunkte: ab 45 % = 13 von 28. Darunter gezielt üben (Bereiche „noch nicht“), dann Wiederholung der Lernerfolgskontrolle.
3. Note aus Pflicht + Bonus (höchstens 28): sehr gut ab 87 % (24,5), gut ab 73 % (20,5), befriedigend ab 59 % (17), ausreichend ab 45 % (13), mangelhaft ab 18 % (5,5), darunter ungenügend. Grenzen auf halbe Punkte aufgerundet; Schlüssel zentral in `generate.py` (`SCHLUESSEL`).

## Auswertungs-App

`auswertung.html` (eine Datei, offline): Punkte je Teilaufgabe antippen, persönliche Rückmeldung und interne Notiz eintragen. Die App zeigt Kompetenzstand je Bereich, Bestehen und Note und gibt eine zweiseitige Rückmeldung über den Druckdialog als PDF aus (einzeln oder für alle vollständig bewerteten Personen). Daten liegen nur im Browserspeicher (localStorage) des Geräts; Sicherung als JSON und CSV-Export sind eingebaut. Aufbau nach `apps/auswertung-lek1` aus d5ur1-wunschbriefe. Unter 13 Pflichtpunkten ist die Note höchstens mangelhaft.

## Musterlösung (Regelfassung)

`musterloesung.pdf/.docx` (5 Seiten): identisch mit der Arbeit, alle Lösungen rot eingetragen (Lücken, Kreuze, Kästchen, volle Punktzahl). Entsteht im selben Lauf wie die Arbeit (`generate.py`, `schuelerblatt(muster=True)`), bleibt also bei Änderungen automatisch deckungsgleich. Sinngemäße Alternativen und Punkteregeln stehen im Erwartungshorizont.

## Fassung 2: zieldifferent, Bildungsgang Lernen

`lernerfolgskontrolle-lernen.pdf/.docx` (4 Seiten, 18 Punkte) und `loesung-lernen.pdf/.docx` (1 Seite). Gleiche Optik und gleicher Termin wie die Regelfassung; das Schülerblatt nennt den Förderschwerpunkt nicht, nur „Fassung 2“ in der Fußzeile. Ein Gedanke pro Satz, Wortspeicher mit Artikel, Mappenverweis bei jeder Aufgabe, nur Einfachauswahl mit zwei Antworten, keine Minuspunkte, kein Bonus. Inhalt: Mindeststandard A1 bis A8. Quelle: `generate_lernen.py` (nutzt die Layout-Bausteine aus `generate.py`). Bewertung nach Förderplan, nicht nach dem Maßstab der Regelfassung.

## Vor Reihenbeginn übertragen

1. Das gesamte Paket in das vorgesehene geschützte Dateisystem kopieren und dort die Berechtigungen prüfen.
2. Für die tatsächlich eingesetzte vertrauliche Kontrolle dort eine neue Aufgabenvariante erstellen. Diese Ausgangsfassung wurde auf ausdrücklichen Wunsch zunächst öffentlich bereitgestellt; Git-Historie, frühere Deployments und heruntergeladene Kopien können fortbestehen.
3. Den Ordner lehrkraft-material/pruefung einschließlich ZIP, Generator und Bildern aus der öffentlichen aktuellen Bereitstellung entfernen. Die Einträge LN, EH, LN-DOCX, EH-DOCX, ML, AUSWERTUNG, LN-L, LN-L-DOCX, LOES-L und PRUEFUNG-PAKET in cockpit-daten.js entfernen oder auf einen geschützten Einstieg umstellen. Hinweise in cockpit.js und der Wochenplanung aktualisieren.
4. Neu veröffentlichen und prüfen, dass die bisherigen direkten Dateiadressen nicht mehr aus der aktuellen Bereitstellung ausliefern. Bloßes Entfernen der Links genügt nicht.

Der aktuelle Lehrkraftbereich ist nicht zugriffsgeschützt. Die Dateien sind ausschließlich dort verlinkt und nicht Bestandteil der Schülermappe oder des Lernnavigators.

## Bearbeiten

Die DOCX-Dateien können direkt bearbeitet werden. generate.py ist die reproduzierbare Quelle und enthält auch Lösungen; benötigt nur python-docx. Rendern z. B. mit `soffice --headless --convert-to pdf *.docx`. Nach Änderungen DOCX rendern und alle Seiten visuell prüfen; PDF und ZIP anschließend aktualisieren.

Die Probearbeit für HolzBot steht in `../../materialien/holzbot-probearbeit.md`: eigenständige Übungsvariante mit Aufgaben, Lösungen, Bewertung und verbindlichem Ablauf für den Chatbot.
Das ZIP enthält zusätzlich die Datei `holzbot-probearbeit.md` zum Hochladen als Wissensbasis.
