# Spiel – Vom Baum zum Brett

Hybrides Würfelspiel für den Technikunterricht.

## Grundidee

Das iPad übernimmt nur die Spielleitung:
- digitales Spielfeld
- Würfel
- Spielfiguren
- automatische Bewegung und Bereichserkennung

Die eigentlichen Aufgaben, Infotexte und Lösungen bleiben gedruckt auf dem Tisch, damit die Lernenden miteinander sprechen, darstellen, zeichnen und beraten.

## Technischer Aufbau

- `index.html` – Spielfeld und Bedienoberfläche
- `spiel.css` – responsive Gestaltung für iPad-Querformat
- `spiel.js` – Feldkoordinaten und Bewegungslogik
- `assets/hintergrund.webp` – Panorama ohne Wegpunkte

Das Spielfeld ist in fünf exakt gleich breite Bereiche zu je 20 % geteilt:

1. Wald
2. Baumfällung
3. Transport
4. Sägewerk
5. Baumarkt

Der Weg wird vollständig in HTML/CSS/JavaScript über das Hintergrundbild gelegt. Dadurch sind alle Feldpositionen eindeutig bekannt und die Spielfiguren können später exakt von Feld zu Feld bewegt werden.

## Aktueller Prototyp

Der erste Prototyp legt 40 Felder an, acht pro Bereich. Ein Teststein kann mit „Feld weiter“ über den kompletten Weg bewegt werden. Damit lässt sich zuerst prüfen, ob Wegführung, Feldgrößen und Positionen auf dem Hintergrund funktionieren.

## Nächster Ausbau

Nach Freigabe des Spielfelds:
1. 2–5 Spieler einrichten
2. Würfelanimation
3. Zuordnung 1/6 = Malen, 2/5 = Quiz, 3/4 = Pantomime
4. „Geschafft“ = 3 Felder vor, „nicht geschafft“ = stehenbleiben
5. besetzte Felder automatisch überspringen
6. Bereichswechsel erkennen und gedruckte Infokarte anfordern
7. Gewinnerkennung am Ziel
