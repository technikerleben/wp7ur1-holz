# Möbelwerkstatt in TaskCards – Einrichtung

Eine Pinnwand für die ganze Lerngruppe. Jedes Kind hat **eine eigene Spalte, die nur es selbst sieht**. Die Lehrkraft sieht als Besitzerin/Besitzer alles.
Die Dokumentation in TaskCards ersetzt das gedruckte Werkstattheft.

---

## 1. Farbcode

Jede Karte bekommt eine Farbe **und** ein Zeichen am Anfang des Titels, damit sie auch ohne Farbe (Graustufen, Farbsehschwäche) erkennbar bleibt.

| Farbe | Titel beginnt mit | Was? | Wer legt an? |
|---|---|---|---|
| **Lila** `#8C3CDD` | 💡 IDEE | „Mein Projekt“ und Ideen/Skizzen (Ideenblatt), neue Version = neue Karte | Kind (Startkarte legt die Lehrkraft an) |
| **Blau** `#3C3CDD` | 📘 PROTOKOLL | ein Protokollblatt pro Werkstatteinheit: Planen, Durchführen, Reflektieren | Kind, jede Stunde |
| **Grün** `#3CDD3C` | ✅ ERGEBNIS | Fotos des fertigen Werkstücks und Ergebnisbogen (Selbstbewertung), Rückblick | Kind, am Ende |
| **Orange** | 🔶 LEHRGANG | gebuchter oder gemachter Lehrgang, Foto vom Probestück | Kind |
| **Gelb** | 🏁 MEILENSTEIN | eine geschaffte Station mit Foto (Fortschritt) | Kind |
| **Rot** (optional) | ❓ HILFE | „Ich komme nicht weiter bei …“ | Kind |

Die Farben von Lila, Blau und Grün entsprechen den Kopfbalken der drei Arbeitsblätter. Wählt in TaskCards jeweils die ähnlichste Kartenfarbe.

In der Spalte eines Kindes sieht man so auf einen Blick: Gibt es zu jeder Stunde einen blauen Eintrag? Wie viele gelbe Meilensteine sind schon da? Welche Lehrgänge (orange) wurden gemacht? Steckt irgendwo eine rote Karte?

> Bitte vor dem Start prüfen, welche Kartenfarben die eigene TaskCards-Version anbietet, und die Legende ggf. anpassen.

---

### Arbeitsblätter dazu (je 1 Seite, digital in GoodNotes ausfüllen, dann als PDF oder Bild in TaskCards hochladen)
- [Ideenblatt](druck/ideenblatt.pdf) → lila Karte 💡 IDEE
- [Protokollblatt](druck/protokollblatt.pdf): eine Seite pro Werkstatteinheit (Planen, Durchführen, Reflektieren) → blaue Karte 📘 PROTOKOLL
- [Ergebnisbogen](druck/ergebnisbogen.pdf): Selbstbewertung zu den Fotos des fertigen Werkstücks → grüne Karte ✅ ERGEBNIS

Quelle: `tools/build_moebelbau_blaetter.py`

---

## 2. Aufbau der Pinnwand

Darstellung: **Pinnwand** (Spalten). In den Sicherheitseinstellungen **„Private Pinnwand“** aktivieren.

| Spalte | Kinder | Inhalt |
|---|---|---|
| ℹ️ Start & Infos | Lesen | Farbcode-Legende (oben anheften), Kartenvorlagen, Links |
| 🔒 Werkstattpass & Freigaben | Verweigert | nur für die Lehrkraft: verbindliche Bestätigungen |
| Mia K. | nur Mia: Schreiben | Mias Projekt |
| Ben S. | nur Ben: Schreiben | Bens Projekt |
| … | … | eine Spalte pro Kind |

Spaltennamen: Vorname und Anfangsbuchstabe oder ein Kürzel – keine vollen Namen.

### Spalte „ℹ️ Start & Infos“ (Vorschlag)
1. **Farbcode** – die Tabelle aus Abschnitt 1
2. **So dokumentierst du** – Kurzanleitung (siehe Vorlage unten)
3. **Präsentation Möbelwerkstatt** – Link auf `moebelbau/input-moebelwerkstatt.html`
4. **Lehrgänge** – Link oder PDF: Projektübersicht, Seite 3
5. **Sicherheit** – die Regeln aus der Projektübersicht, Seite 2
6. **Ideenspeicher** und **Großprojekt Taschenregal**
7. **So wird bewertet** – Abschnitt 5 dieser Datei
8. **Kartenvorlagen** – je eine Musterkarte pro Farbe (Texte unten)

### Spalte „🔒 Werkstattpass & Freigaben“ (nur Lehrkraft)
Eine Karte pro Pflicht-Lehrgang, in die du die Namen einträgst, z. B.:

> **L3 Stichsäge** – Mia K. 12.11. · Ben S. 12.11. · …

Dazu eine Karte **„Freigaben“** mit den Namen und Daten der Planungsfreigabe. Diese Spalte ist der **verbindliche Nachweis**. Orange Karten der Kinder sind deren Dokumentation, aber keine Freigabe, denn Kinder können in ihrer Spalte selbst schreiben. Im Werkraum genügt ein Blick auf diese Spalte: Darf Ben an die Stichsäge?

---

## 3. Einrichtung Schritt für Schritt

1. **Pinnwand anlegen**: neue Pinnwand, Darstellung „Pinnwand“, Titel z. B. „Möbelwerkstatt 7x“. Unter „Sicherheit“ → „Private Pinnwand“.
2. **Spalten anlegen**: „ℹ️ Start & Infos“, „🔒 Werkstattpass & Freigaben“, dann eine Spalte pro Kind.
3. **Infos füllen**: Legende, Anleitung, Links und Musterkarten in die Infospalte.
4. **Startkarte pro Kind**: In jede Kinderspalte eine lila Karte **„💡 IDEE – Mein Projekt“** (Vorlage unten).
5. **Berechtigung pro Kind** (Teilen bzw. Berechtigungen → Plus):
   - *Allgemein*: Name des Kindes, **Passwort** vergeben (z. B. ein einfacher Code; Liste nur bei dir)
   - *Inhalte erlauben*: **„Anhänge erlauben“** einschalten (für Fotos)
   - *Rechte*: „ℹ️ Start & Infos“ → **Lesen** · eigene Spalte → **Schreiben** · alle anderen Spalten → **Verweigert**
   - Speichern
6. **Testen**: Mit dem **Auge-Symbol** die Ansicht einer Berechtigung prüfen. Das Kind darf nur Infos und die eigene Spalte sehen.
7. **Verteilen**: Link oder **QR-Code** pro Kind, z. B. ausgedruckt mit dem Passwort, in die Mappe kleben oder als Lesezeichen auf dem iPad.

Wichtig:
- Wird später eine neue Spalte angelegt (z. B. ein Kind kommt dazu), mit dem Auge-Symbol prüfen, dass sie für die anderen Berechtigungen auf „Verweigert“ steht.
- Teams (bis 3 Personen): Jedes Kind behält die eigene Spalte, denn bewertet wird einzeln. Gemeinsame Skizzen lädt jedes Teammitglied in die eigene Spalte hoch.
- Aufwand für 25 Kinder: etwa 30–45 Minuten für die Berechtigungen.

---

## 4. Kartenvorlagen (zum Kopieren)

### 💡 IDEE – Mein Projekt (lila, Lehrkraft legt an)
```
Ich baue: …
Für (Person/Ort): …
Weg:  Modell aus Eisstielen  /  Original aus Dachlatte
Team: allein / mit …
Mein Startniveau: 1 / 2 / 3
Mein Prüfkriterium: Mein Möbel ist gut, wenn …
```

### 📘 PROTOKOLL – [Datum] (blau, jede Stunde)
Protokollblatt aus GoodNotes anhängen, oder kurz direkt in die Karte:
```
Mein Plan für heute:
– …
– …

Am Ende:  ✅ geschafft   🟡 teilweise   ❌ nicht geschafft
Warum / nächster Schritt: …
```
Zu Beginn der Stunde anlegen (Plan), am Ende ergänzen (Einschätzung). Foto vom Arbeitsstand ist erwünscht, aber freiwillig.

### 💡 IDEE – [Was?] Version [1] (lila)
```
Ideenblatt aus GoodNotes anhängen – Maße in mm müssen lesbar sein.
Materialliste:
– … Stück … (Länge … mm)
– …
Was ist neu gegenüber der letzten Version? …
```

### 🔶 LEHRGANG – [L3 Stichsäge] (orange)
```
Gebucht für: …
Gemacht am: …
Das habe ich gelernt (1 Satz): …
Foto vom Probestück anhängen.
```
Nur der Eintrag der Lehrkraft im Werkstattpass gilt als Freigabe.

### 🏁 MEILENSTEIN – [Station] (gelb)
```
Station:  Idee · Skizze · Freigabe · Zuschnitt · Montage · Schliff · Oberfläche · Test · Fertig
Foto anhängen.
Das war schwierig / darauf bin ich stolz: …
```

### ✅ ERGEBNIS – Mein fertiges Projekt (grün, am Ende)
```
Fotos anhängen: von vorn · von der Seite · Detail einer Verbindung · im Einsatz
Ergebnisbogen aus GoodNotes anhängen.

1. Mein Test: Hat mein Möbel mein Prüfkriterium erfüllt?  ja / teilweise / nein
2. Das habe ich verbessert: …
3. Darauf bin ich stolz / das mache ich nächstes Mal anders: …
```

### ❓ HILFE – [Thema] (rot, optional)
```
Ich komme nicht weiter bei: …
Das habe ich schon versucht: …
```

### Infokarte „So dokumentierst du“
```
Jede Stunde:
1. Zu Beginn: blaue Karte – Datum und dein Plan
2. Arbeiten! Fotos machen, wenn etwas fertig ist
3. Am Ende: blaue Karte ergänzen – geschafft? nächster Schritt?
Station geschafft → gelbe Karte mit Foto
Neue Idee/Skizze → lila Karte · Lehrgang → orange Karte
Fertig → grüne Karte mit Fotos und Ergebnisbogen
Nicht weiter? → rote Karte (und Lehrkraft fragen)
```

---

## 5. Bewertung (Vorschlag)

Lernerfolgskontrolle wie bisher: **Dokumentation 40 % · Werkstück 60 %**. Die Dokumentation wird für jedes Kind einzeln bewertet.

| | Dokumentation in TaskCards | Punkte |
|---|---|---|
| D1 | 💡 Mein Projekt und Ideen/Skizze mit Maßen | 10 |
| D2 | 📘 Protokoll: zu (fast) jeder Stunde Plan und ehrliche Einschätzung | 12 |
| D3 | 🏁 Meilensteine mit Fotos: Fortschritt nachvollziehbar | 8 |
| D4 | 🔶 Lehrgänge dokumentiert | 4 |
| D5 | ✅ Ergebnis: Fotos, Test, Selbstbewertung, Rückblick | 6 |
| | **Summe** | **40** |

Werkstück (60 Punkte): Kriterien B1–B6 wie im Erwartungshorizont (`druck/werkstattheft-erwartungshorizont.pdf`).

Rückmeldung während des Projekts: Kommentare an den Karten. Zur Archivierung als Klassenarbeit vor der Bewertung jede Kinderspalte sichern, z. B. über die Ansicht der Berechtigung als PDF drucken oder über die Export-Funktion der Pinnwand. Das Format vorher einmal testen.

---

## 6. Datenschutz

- In Spaltennamen und Berechtigungen nur Vornamen mit Anfangsbuchstaben oder Kürzel verwenden.
- Fotos nur vom Werkstück, nicht von Personen.
- Links mit Passwort verteilen. Bei Verlust die Berechtigung löschen und neu anlegen.
