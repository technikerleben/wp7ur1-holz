# Spiel – Vom Baum zum Brett

Hybrides Würfelspiel für den Technikunterricht in Klasse 7.

## Grundidee

Das iPad übernimmt bewusst nur die Spielleitung:

- Spielfeld und Figuren
- Würfel
- Zuordnung der Würfelzahl zur Kartenart
- Bewegung der Figuren
- Bereichserkennung
- Regel „besetztes Feld überspringen“
- Spielerwechsel und Zielerkennung

Die eigentlichen Aufgaben, Lösungen und Sachtexte bleiben gedruckt auf dem Tisch. Dadurch schauen die Lernenden nicht dauerhaft auf den Bildschirm, sondern müssen miteinander lesen, zeichnen, darstellen, beraten und entscheiden.

## Spielregel in der Webapp

- **1 oder 6:** rote Karte – Malaufgabe
- **2 oder 5:** gelbe Karte – Quizfrage
- **3 oder 4:** blaue Karte – Pantomime
- **Aufgabe geschafft:** 3 Felder vor
- **Aufgabe nicht geschafft:** stehenbleiben
- **Zielfeld besetzt:** automatisch bis zum nächsten freien Feld weiterrücken
- **Neuer Bereich:** passende gedruckte Infokarte einmal gemeinsam laut lesen
- **Ziel:** Wer zuerst das letzte Feld erreicht, gewinnt

Ein Zug, der über das letzte Feld hinausführen würde, endet direkt auf dem Zielfeld.

## Spielfeld

Das Panorama ist in fünf exakt gleich breite HTML-Bereiche zu je 20 % geteilt:

1. Wald
2. Baumfällung
3. Transport
4. Sägewerk
5. Baumarkt

Der Weg liegt vollständig als HTML/SVG-Ebene über dem Hintergrundbild. Dadurch kennt die Anwendung jede Feldposition exakt und kann Figuren zuverlässig bewegen.

Aktuell gibt es **40 Felder**, also **8 Felder je Bereich**.

## Dateien

- `index.html` – Oberfläche, Spielaufbau und Dialoge
- `spiel.css` – iPad-optimierte Gestaltung
- `spiel.js` – Spielzustand, Würfel, Figuren, Bewegung und Regeln
- `assets/hintergrund.webp` – Hintergrundpanorama ohne Wegpunkte

## Spielablauf

1. 2–5 Personen auswählen und optional Namen eintragen.
2. Zu Beginn wird die Infokarte **„Der Wald“** vorgelesen.
3. Die aktuelle Person würfelt auf dem iPad.
4. Das iPad zeigt nur die Kartenart an.
5. Die Gruppe führt die Aufgabe mit der gedruckten Karte durch.
6. Die Gruppe tippt **„Geschafft“** oder **„Nicht geschafft“**.
7. Bei Erfolg bewegt die Webapp die Figur automatisch.
8. Beim ersten Erreichen eines neuen Bereichs fordert die Webapp die passende Infokarte an.
9. Danach wechselt der Zug automatisch zur nächsten Person.
