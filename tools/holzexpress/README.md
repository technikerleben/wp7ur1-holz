# Holzexpress
Kurzes 3D-Spiel für den offenen Anfang in WP Technik 7 (etwa 3–5 Minuten).

Spielbare Datei: `../../holzexpress.html`. Three.js und kompilierte Tailwind-Utilities sind eingebettet. Keine CDN-Abhängigkeit, kein Login, kein Tracking, keine Speicherung persönlicher Daten.

## Inhalte
- Waldexkursion: Eiche, Rotbuche, Ahorn und Birke anhand von Blatt/Rinde auswählen; Namen bei Bedarf aufdecken.
- A1: sechs Stammschichten erkunden; Kambium als Wachstumsschicht.
- A2: neun Jahresringe im Modell; Beobachtung und mögliche Ursache ausdrücklich unterscheiden.
- A3: Baum → Fällen → Transport (automatisch) → Sägewerk → Vermessen/Ablängen → Einschnitt → Schnittholz.
- A4: zwei geometrisch berechnete Schnittpläne. Brettquerschnitte liegen im Kreis; Randstücke und Sägespalte reduzieren die Ausbeute. Maße und Holzernte sind didaktisch vereinfacht.

Drei zufällig ausgewählte Bestellungen. Fehlversuche kosten nichts. Ohne Ton und ohne Transport-Minispiel. Länge (4 m) und Durchmesser (64 cm) messen, Stamm quer in 1-m- oder 2-m-Abschnitte ablängen, dann längs einschneiden. Der Sägespalt beim Ablängen ist im Längenmodell nicht berücksichtigt. Die Lieferung zählt alle Abschnitte; die Schnittplanansicht zeigt exemplarisch einen Abschnitt. Freiwillige Baumscheibe, reduzierte Bewegung gemäß Geräteinstellung. Ein Finger dreht die 3D-Ansicht, zwei Finger zoomen (OrbitControls). Kurzes Antippen wählt Bäume; Ziehen löst keine Baumwahl aus. Touch, Maus und Leertaste. Ohne WebGL bleibt der Ablauf mit gezeichneter Ersatzansicht über Schaltflächen spielbar.

## Bauen
In diesem Ordner `npm install`, dann `npm run build`. Die erzeugte HTML-Datei wird im Repository eingecheckt und direkt als statische Seite bereitgestellt. Kein Build-Schritt in Vercel nötig.

Three.js: MIT, Lizenztext in der HTML-Datei. Tailwind CSS: MIT.
