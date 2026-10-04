# Prüflabor als animierter Versuchsfilm

Die Visualisierung wird in `pruefstation.html` oberhalb der erhaltenen Stationsanleitungen angezeigt. Vier Kapitel zeigen Aussehen, Masse, Münztest und Wasseraufnahme. Start/Pause, Wiederholen, Zeitregler und automatische Haltepunkte führen zur echten Prüfung und zu A5.1. Der Aufrufparameter `station` wählt das passende Filmkapitel; der Rückweg bleibt im Lernnavigator.

Alle Modelle sind 200 × 50 × 18 mm. Die Holzart „Akazie“ ist die vom Kurs verwendete Probenbezeichnung. Farben, Massen, Druckspuren und Tropfenverhalten sind ausdrücklich illustrative Beispieldaten; sie sind keine Messwerte der Unterrichtsproben oder allgemeingültige Holzartkennwerte. Der Tropfenversuch zeigt 60 Sekunden im gekennzeichneten Zeitraffer. Gleich große Tropfen werden gleichzeitig aufgesetzt. Die Druckprüfung stellt gleiche Belastung dar und keinen genormten Härtemessversuch.

Der Film enthält keine Audiospur, startet nicht automatisch und pausiert beim Wechsel in einen anderen Browsertab sowie bei Berührung der 3D-Ansicht. Bei fehlendem WebGL bleiben die vollständigen Stationsanleitungen zugänglich. JavaScript ist für die bisherige Aufgabenführung erforderlich.

## Bearbeiten und bauen

`film.js` ist die Quelle. Das Build-Skript verwendet die im benachbarten Holzexpress-Build festgelegten Abhängigkeiten Three.js 0.180.0, Tailwind 3.4.17 und esbuild 0.25.12:

```sh
cd tools/holzexpress
npm install
cd ../prueflabor
node build.mjs
```

Der Build erzeugt `prueflabor-film.js` und `prueflabor-film.css` im Repo-Hauptverzeichnis. Beide werden zusammen mit der HTML-Seite veröffentlicht. Zur Laufzeit sind keine externen CDNs nötig. Farben und Beispieldaten werden in `woods` am Anfang von `film.js` angepasst. Die Maße werden in der Three.js-Geometrie festgelegt; bei einer Änderung auch die Beschriftung in `pruefstation.html` aktualisieren.
