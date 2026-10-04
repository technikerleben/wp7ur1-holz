# Holzexpress
Kurzes 3D-Spiel für den offenen Anfang in WP Technik 7 (etwa 3–5 Minuten).

Spielbare Datei: `../../holzexpress.html`. Three.js und kompilierte Tailwind-Utilities sind eingebettet. Keine CDN-Abhängigkeit, kein Login, kein Tracking, keine Speicherung persönlicher Daten.

## Inhalte
- Waldexkursion: Eiche, Rotbuche, Ahorn und Birke anhand von Blatt/Rinde auswählen; Namen bei Bedarf aufdecken.
- A1: sechs Stammschichten erkunden; Kambium als Wachstumsschicht.
- A2: neun Jahresringe im Modell; Beobachtung und mögliche Ursache ausdrücklich unterscheiden.
- A3: Baum → Fällen → Transport → Sägewerk → Einschnitt → Schnittholz.
- A4: zwei geometrisch berechnete Schnittpläne. Brettquerschnitte liegen im Kreis; Randstücke und Sägespalte reduzieren die Ausbeute. Maße und Holzernte sind didaktisch vereinfacht.

Drei zufällig ausgewählte Bestellungen. Fehlversuche kosten nichts. Pfützen verlangsamen den Transport. Freiwillige Baumscheibe, optionale Töne, reduzierte Bewegung gemäß Geräteinstellung. Touch, Maus und Pfeiltasten/Leertaste. Ohne WebGL bleibt der Ablauf über Schaltflächen spielbar.

## Bauen
In diesem Ordner `npm install`, dann `npm run build`. Die erzeugte HTML-Datei wird im Repository eingecheckt und direkt als statische Seite bereitgestellt. Kein Build-Schritt in Vercel nötig.

Three.js: MIT, Lizenztext in der HTML-Datei. Tailwind CSS: MIT.
