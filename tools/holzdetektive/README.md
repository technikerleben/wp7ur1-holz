# Holzdetektive – die verschwundenen Etiketten

Freiwilliger offener Start nach den echten Materialprüfungen (A5/A6): drei zufällig angeordnete Holzproben und drei von fünf Brettspuren. Kein Countdown, keine Punktabzüge, beliebige Versuche, hilfreiche Rückmeldungen. Dauer ungefähr 3–5 Minuten; zusätzlich frei zugängliches Spurenbuch für alle fünf Begriffe.

## Inhalt und fachliche Grenzen

Angelehnt an `pruefstation.html`, `tools/prueflabor/film.js`, A5–A7 in `kurs-daten.js` und `holzfehler.html`. Spielarchiv und Messungen verwenden dieselben ausdrücklich illustrativen Probenwerte wie die Prüflaboranimation: Fichte 65 g, Buche 125 g, Akazie 135 g; alle 200 × 50 × 18 mm (180 cm³). Der Kursname „Akazie“ ist keine botanische Identifikation. Diese Kombinationen lösen die Fälle im Spiel, sind aber keine allgemeingültigen Bestimmungsschlüssel.

Dichte wird aus Masse/Volumen berechnet; Vergleiche setzen gleiches Volumen und ähnliche Feuchte voraus. Härte bekommt eine eigenständige Prüfung mit gleicher Münze und gleichem Druck; der vereinfachte Münztest ist kein genormtes Härteverfahren. Aus der Masse wird keine Härte abgeleitet. Quellen und Schwinden sind normale Veränderungen durch Aufnahme/Abgabe gebundenen Wassers; Ast, Riss und Verwerfen werden gesondert erklärt. Verformung und Feuchtigkeitsreaktionen sind als Zeitraffer und stark vergrößert gekennzeichnet.

## Technik und Build

Eine selbstständige Datei `holzdetektive.html`: gebündeltes Three.js 0.180.0, OrbitControls, SVGRenderer als Fallback ohne WebGL und kompiliertes Tailwind 3.4.17. Keine CDN-Aufrufe, kein Ton, keine persönlichen Daten, kein externer Spielservice. Ein Finger dreht, zwei Finger zoomen; Maus und Tastatur bedienen die Stationen. Die Kamera lässt sich zurücksetzen. Messanimationen pausieren bei ausgeblendetem Tab.

```sh
npm install --prefix tools/holzexpress
node tools/holzdetektive/build.mjs
```

Die vorhandenen, versionierten Abhängigkeiten von `tools/holzexpress/package.json` werden gemeinsam genutzt. `compiled.css` ist nur ein Build-Zwischenergebnis. Die fertige HTML wird zusammen mit den Quelldateien eingecheckt; Vercel liefert sie statisch aus. Verlinkt in Lernweg, Startseite und echter Prüfstation.
