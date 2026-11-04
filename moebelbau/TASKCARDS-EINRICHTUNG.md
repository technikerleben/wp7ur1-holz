# Möbelwerkstatt in TaskCards – Einrichtung

Eine Pinnwand für die ganze Lerngruppe. Jedes Kind hat **eine eigene Spalte, die nur es selbst sieht**. Die Lehrkraft sieht als Besitzerin/Besitzer alles.
Die Dokumentation in TaskCards ersetzt das gedruckte Werkstattheft.

---

## 1. Farbcode

Jede Karte bekommt eine Farbe **und** ein Zeichen am Anfang des Titels, damit sie auch ohne Farbe (Graustufen, Farbsehschwäche) erkennbar bleibt.

| Farbe | Titel beginnt mit | Was? | Wer legt an? |
|---|---|---|---|
| **Blau** | 📘 PROTOKOLL | Ein Eintrag pro Stunde: Datum, Plan, Einschätzung am Ende | Kind, jede Stunde |
| **Grün** | ✏️ SKIZZE | Foto der Skizze mit Maßen, Materialliste; neue Version = neue Karte | Kind |
| **Orange** | 🔶 LEHRGANG | gebuchter oder gemachter Lehrgang, Foto vom Probestück | Kind |
| **Lila** | 🏁 MEILENSTEIN | eine geschaffte Station mit Foto (Fortschritt) | Kind |
| **Gelb** | ⭐ PROJEKT | „Mein Projekt“ am Anfang, „Rückblick“ am Ende | Lehrkraft legt an, Kind füllt aus |
| **Rot** (optional) | ❓ HILFE | „Ich komme nicht weiter bei …“ | Kind |

In der Spalte eines Kindes sieht man so auf einen Blick: Gibt es zu jeder Stunde einen blauen Eintrag? Wie viele lila Meilensteine sind schon da? Welche Lehrgänge (orange) wurden gemacht? Steckt irgendwo eine rote Karte?

> Bitte vor dem Start prüfen, welche Kartenfarben die eigene TaskCards-Version anbietet, und die Legende ggf. anpassen.

---

### Arbeitsblätter dazu (je 1 Seite, auf Papier oder am iPad ausfüllen, dann fotografieren)
- [Ideenblatt](druck/ideenblatt.pdf) → grüne Karte ✏️ SKIZZE
- [Protokollblatt](druck/protokollblatt.pdf): eine Seite pro Werkstatteinheit (Planen, Durchführen, Reflektieren) → blaue Karte 📘 PROTOKOLL
- [Ergebnisbogen](druck/ergebnisbogen.pdf): Selbstbewertung zu den Fotos des fertigen Werkstücks → gelbe Karte ⭐ PROJEKT

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
4. **Startkarte pro Kind**: In jede Kinderspalte eine gelbe Karte **„⭐ PROJEKT – Mein Projekt“** (Vorlage unten).
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

### ⭐ PROJEKT – Mein Projekt (gelb, Lehrkraft legt an)
```
Ich baue: …
Für (Person/Ort): …
Weg:  Modell aus Eisstielen  /  Original aus Dachlatte
Team: allein / mit …
Mein Startniveau: 1 / 2 / 3
Mein Prüfkriterium: Mein Möbel ist gut, wenn …
```

### 📘 PROTOKOLL – [Datum] (blau, jede Stunde)
```
Mein Plan für heute:
– …
– …

Am Ende:  ✅ geschafft   🟡 teilweise   ❌ nicht geschafft
Warum / nächster Schritt: …
```
Zu Beginn der Stunde anlegen (Plan), am Ende ergänzen (Einschätzung). Foto vom Arbeitsstand ist erwünscht, aber freiwillig.

### ✏️ SKIZZE – [Was?] Version [1] (grün)
```
Foto der Skizze anhängen – Maße in mm müssen lesbar sein.
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

### 🏁 MEILENSTEIN – [Station] (lila)
```
Station:  Idee · Skizze · Freigabe · Zuschnitt · Montage · Schliff · Oberfläche · Test · Fertig
Foto anhängen.
Das war schwierig / darauf bin ich stolz: …
```

### ⭐ PROJEKT – Rückblick (gelb, am Ende)
```
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
Station geschafft → lila Karte mit Foto
Neue Skizze → grüne Karte · Lehrgang → orange Karte
Nicht weiter? → rote Karte (und Lehrkraft fragen)
```

---

## 5. Bewertung (Vorschlag)

Lernerfolgskontrolle wie bisher: **Dokumentation 40 % · Werkstück 60 %**. Die Dokumentation wird für jedes Kind einzeln bewertet.

| | Dokumentation in TaskCards | Punkte |
|---|---|---|
| D1 | ⭐ Mein Projekt und ✏️ Skizze mit Maßen und Materialliste | 10 |
| D2 | 📘 Protokoll: zu (fast) jeder Stunde Plan und ehrliche Einschätzung | 12 |
| D3 | 🏁 Meilensteine mit Fotos: Fortschritt nachvollziehbar | 8 |
| D4 | 🔶 Lehrgänge dokumentiert | 4 |
| D5 | ⭐ Rückblick: Test, Verbesserung, eigene Einschätzung | 6 |
| | **Summe** | **40** |

Werkstück (60 Punkte): Kriterien B1–B6 wie im Erwartungshorizont (`druck/werkstattheft-erwartungshorizont.pdf`).

Rückmeldung während des Projekts: Kommentare an den Karten. Zur Archivierung als Klassenarbeit vor der Bewertung jede Kinderspalte sichern, z. B. über die Ansicht der Berechtigung als PDF drucken oder über die Export-Funktion der Pinnwand. Das Format vorher einmal testen.

---

## 6. Datenschutz

- In Spaltennamen und Berechtigungen nur Vornamen mit Anfangsbuchstaben oder Kürzel verwenden.
- Fotos nur vom Werkstück, nicht von Personen.
- Links mit Passwort verteilen. Bei Verlust die Berechtigung löschen und neu anlegen.
