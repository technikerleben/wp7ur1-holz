"""Sprachlich entlastete, zieldifferente Fassung der Lernerfolgskontrolle Holz
(Bildungsgang Lernen, NRW) plus Lösungsblatt für die Lehrkraft.

Nutzt die Layout-Bausteine aus generate.py (alles oberhalb des Schülerblatt-Markers).
Danach rendern:
  soffice --headless --convert-to pdf lernerfolgskontrolle-lernen.docx loesung-lernen.docx
und alle Seiten visuell prüfen.

Sprachregeln dieser Fassung: ein Gedanke pro Satz, keine Nebensätze, Aktiv, Du-Ansprache,
konkrete Verben (Kreuze an, Trage ein, Zähle), Fachwörter mit Artikel im Wortspeicher,
nur Einfachauswahl mit zwei Antworten, keine Minuspunkte, kein Bonus.
"""
from pathlib import Path

_here = Path(__file__).resolve().parent
_src = (_here / 'generate.py').read_text(encoding='utf-8')
exec(_src.split('# =================================================================== Schülerblatt')[0])

FS = 12.5     # Grundschrift
GAPL = '____________________'

# ---------------------------------------------------------------- Bausteine (größer, luftiger)


def kopf_l(titel, fach, meta):
    x = D.add_paragraph(); f = x.paragraph_format
    f.tab_stops.add_tab_stop(Mm(CONTENT_MM), WD_TAB_ALIGNMENT.RIGHT)
    f.space_after = Pt(1)
    run(x, titel, 19, True, color=SCHIEFER)
    run(x, '\t' + fach, 9, True, color=SCHIEFER)
    m = p(meta, size=8, color=MUTED, after=0)
    para_border(m, 'bottom', 12, SCHIEFER, 5)
    spacer(5)


def box(lines, color=SCHIEFER, size=FS, after=8):
    t = D.add_table(rows=1, cols=1)
    c = t.rows[0].cells[0]
    cell_borders(c, left=(24, color), top=(4, LINIE), bottom=(4, LINIE), right=(4, LINIE))
    cell_margins(c, 90, 90, 160, 140)
    for i, segs in enumerate(lines):
        z = c.paragraphs[0] if i == 0 else c.add_paragraph()
        z.paragraph_format.space_after = Pt(4); z.paragraph_format.line_spacing = 1.15
        if isinstance(segs, str): segs = [(segs, False)]
        for seg, b in segs: run(z, seg, size, b)
    c.paragraphs[-1].paragraph_format.space_after = Pt(0)
    geometry(t, [CONTENT_MM])
    keep_rows(t)
    spacer(after)


def aufgabe_l(nr, titel, mappe, punkte, before=14):
    x = D.add_paragraph(); f = x.paragraph_format
    f.keep_with_next = True; f.space_before = Pt(before); f.space_after = Pt(6)
    f.left_indent = Mm(2.5)
    f.tab_stops.add_tab_stop(Mm(CONTENT_MM - 2.5), WD_TAB_ALIGNMENT.RIGHT)
    para_border(x, 'left', 24, ROST, 6)
    run(x, f'Aufgabe {nr}', 13.5, True, color=SCHIEFER)
    run(x, f'   {titel}', 13.5, True)
    run(x, f'\t____ / {punkte} Punkte', 9.5, color=MUTED)
    h = p('', keep=True, after=4, indent=IND + 8)
    run(h, 'Hilfe: ', 10, True, color=MUTED); run(h, f'Schau in deiner Mappe bei {mappe}.', 10, color=MUTED)


def satz(t, bold=False, keep=True, after=3, size=FS, italic=False, before=0):
    x = D.add_paragraph(); f = x.paragraph_format
    f.left_indent = Mm(IND + 8); f.space_after = Pt(after); f.space_before = Pt(before)
    f.keep_with_next = keep; f.line_spacing = 1.15
    if isinstance(t, str): t = [(t, bold)]
    for seg, b in t: run(x, seg, size, b, italic)
    return x


def auftrag(label, t, punkte=None, before=8):
    """Arbeitsauftrag: fett, mit Teilnummer, Punkte klein dahinter."""
    x = D.add_paragraph(); f = x.paragraph_format
    f.left_indent = Mm(IND + 9); f.first_line_indent = Mm(-9)
    f.tab_stops.add_tab_stop(Mm(IND + 9))
    f.space_before = Pt(before); f.space_after = Pt(4); f.keep_with_next = True
    run(x, label, FS, True, color=SCHIEFER)
    run(x, '\t' + t, FS, True)
    if punkte: run(x, f'  ({punkte} P)', 9.5, color=MUTED)


def luecke_l(zeilen, keep_last=False):
    for i, z in enumerate(zeilen):
        x = D.add_paragraph(); f = x.paragraph_format
        f.left_indent = Mm(IND + 9); f.space_after = Pt(3)
        f.line_spacing_rule = WD_LINE_SPACING.EXACTLY; f.line_spacing = Pt(30)
        f.keep_with_next = keep_last or i < len(zeilen) - 1
        run(x, z, FS)


def ankreuzen_l(optionen, keep_last=False):
    for i, o in enumerate(optionen):
        x = D.add_paragraph(); f = x.paragraph_format
        f.left_indent = Mm(IND + 19); f.first_line_indent = Mm(-10)
        f.tab_stops.add_tab_stop(Mm(IND + 19))
        f.space_before = Pt(2); f.space_after = Pt(5)
        f.keep_with_next = keep_last or i < len(optionen) - 1
        run(x, '□', 20)
        run(x, '\t' + o, FS)


def wortspeicher(woerter):
    t = D.add_table(rows=1, cols=len(woerter) + 1)
    cells = t.rows[0].cells
    run(cells[0].paragraphs[0], 'Wortspeicher', 10, True, color=SCHIEFER)
    for c, w in zip(cells[1:], woerter):
        run(c.paragraphs[0], w, FS, True)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for c in cells:
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        c.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell_borders(c, top=(8, SCHIEFER), bottom=(8, SCHIEFER), left=(4, LINIE), right=(4, LINIE))
        cell_margins(c, 90, 90, 100, 100)
    rest = (CONTENT_MM - IND - 9 - 30) / len(woerter)
    geometry(t, [30] + [rest] * len(woerter), IND + 9)
    keep_rows(t, keep_last=True)
    spacer(6, keep=True)


def reihenfolge(schritte, box_mm=12):
    """schritte = [(wort, vorgabe)] in gemischter Reihenfolge, untereinander mit Abstand."""
    n = len(schritte)
    t = D.add_table(rows=n * 2 - 1, cols=2)
    for i, (wort, vorgabe) in enumerate(schritte):
        row = t.rows[i * 2]
        row.height = Mm(box_mm); row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        b, l = row.cells
        cell_borders(b, top=(12, '333333'), bottom=(12, '333333'), left=(12, '333333'), right=(12, '333333'))
        cell_borders(l); cell_margins(l, 0, 0, 200, 0)
        if vorgabe:
            run(b.paragraphs[0], vorgabe, 15, True, color=MUTED)
            b.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(l.paragraphs[0], wort, FS)
        for c in (b, l):
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
        if i < n - 1:
            g = t.rows[i * 2 + 1]; g.height = Mm(2.5); g.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
            for c in g.cells:
                cell_borders(c)
                c.paragraphs[0].paragraph_format.space_after = Pt(0)
                c.paragraphs[0].paragraph_format.line_spacing = Pt(2)
    geometry(t, [box_mm, 60], IND + 9)
    keep_rows(t)
    spacer(6)


def kaestchen_l(labels, box_mm=13, label_mm=26):
    t = D.add_table(rows=1, cols=len(labels) * 2)
    row = t.rows[0]; row.height = Mm(box_mm); row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    for k, lab in enumerate(labels):
        l, b = row.cells[k * 2], row.cells[k * 2 + 1]
        cell_borders(b, top=(12, '333333'), bottom=(12, '333333'), left=(12, '333333'), right=(12, '333333'))
        cell_borders(l); cell_margins(l, 0, 0, 0, 120)
        run(l.paragraphs[0], lab, FS, True); l.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for c in (b, l):
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
    geometry(t, [label_mm, box_mm] * len(labels), IND + 9)
    keep_rows(t)
    spacer(6)


def tabelle_l(head, rows, widths):
    t = table(head, rows, widths, indent=IND + 9, size=FS - 0.5)
    return t


# =================================================================== Schülerblatt (Fassung 2)
TEACHER = False
D = document('Lernerfolgskontrolle Holz  ·  Fassung 2')
D.styles['Normal'].font.size = Pt(FS)
kopf_l('Lernerfolgskontrolle Holz', 'WP TECHNIK 7', 'HBG Dortmund  ·  Vom Baum zum Holz  ·  A1 bis A8')
identzeile()
box([
    [('Du hast ', False), ('30 Minuten', True), (' Zeit.', False)],
    [('Du darfst deine ', False), ('Mappe', True), (' benutzen.', False)],
    [('Das ', False), ('iPad', True), (' bleibt in der Tasche.', False)],
    'Lies jede Aufgabe genau. Arbeite allein.',
    [('Bei jeder Ankreuzaufgabe ist ', False), ('nur 1 Antwort', True), (' richtig.', False)],
    [('So kreuzt du an:  ', False), ('☒', False), ('  richtig      ', False), ('□', False), ('  falsch', False)],
])

# ---- Aufgabe 1
aufgabe_l(1, 'Der Stamm', 'A1', 3, before=2)
auftrag('1', 'Setze die Wörter ein. Jedes Wort passt einmal.', 3, before=2)
wortspeicher(['die Borke', 'das Kambium', 'das Splintholz'])
luecke_l([f'{GAPL} schützt den Baum außen.',
          f'{GAPL} lässt den Stamm dicker werden.',
          f'{GAPL} leitet Wasser nach oben.'])

# ---- Aufgabe 2
aufgabe_l(2, 'Jahresringe', 'A2', 2)
t = D.add_table(rows=1, cols=2)
lc, rc = t.rows[0].cells
for c in (lc, rc):
    cell_borders(c); cell_margins(c, 0, 0, 0, 120)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
lc.paragraphs[0].add_run().add_picture(str(OUT / 'ringe.png'), width=Mm(66))
for i, (seg, b) in enumerate([('Jeder Kreis ist ein Jahresring.', False),
                              ('Zähle die Ringe.', True),
                              ('Tipp: Mache bei jedem Ring einen kleinen Strich.', False)]):
    z = rc.paragraphs[0] if i == 0 else rc.add_paragraph()
    z.paragraph_format.space_after = Pt(5)
    run(z, seg, FS if i < 2 else 10.5, b, italic=(i == 2))
z = rc.add_paragraph(); z.paragraph_format.space_before = Pt(4)
run(z, '2a  ', FS, True, color=SCHIEFER); run(z, 'Trage die Zahl ein.', FS, True); run(z, '  (1 P)', 9.5, color=MUTED)
z = rc.add_paragraph(); z.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
z.paragraph_format.line_spacing = Pt(30)
run(z, 'Der Baum ist etwa ______ Jahre alt.', FS)
geometry(t, [72, 80], IND + 8)
keep_rows(t, keep_last=True)
spacer(4, keep=True)
auftrag('2b', 'Ring 8 ist schmal. Was bedeutet das? Kreuze an.', 1)
ankreuzen_l(['In diesem Jahr ist der Stamm nur wenig dicker geworden.',
             'In diesem Jahr ist der Baum kleiner geworden.'])

# ---- Aufgabe 3
page_break()
aufgabe_l(3, 'Vom Baum zum Brett', 'A3 und A4', 4, before=0)
auftrag('3a', 'Was passiert zuerst? Was passiert danach? Trage die Zahlen 2 bis 5 ein. Die 1 ist schon da.', 2, before=2)
reihenfolge([('Transport', None), ('Baum', '1'), ('Brett', None), ('Fällen', None), ('Sägewerk', None)])
auftrag('3b', 'Du brauchst ein Brett. Es soll mindestens 12 cm breit sein.', before=6)
tabelle_l(['Plan', 'So breit ist jedes Brett'], [['Plan A', '9 cm'], ['Plan B', '14 cm']], [30, 60])
x = satz('Welcher Plan passt? Kreuze an.', bold=True, after=3); run(x, '  (1 P)', 9.5, color=MUTED)
ankreuzen_l(['Plan A', 'Plan B'])
x = satz('Trage die Zahl ein.', bold=True, after=0, before=4); run(x, '  (1 P)', 9.5, color=MUTED)
luecke_l(['Die Bretter von diesem Plan sind ______ cm breit.'])

# ---- Aufgabe 4
page_break()
aufgabe_l(4, 'Holz testen', 'A5 und A6', 2, before=0)
satz('Du drückst eine Münze fest auf zwei Holzproben.')
satz('Das siehst du danach:', after=4)
tabelle_l(['Probe', 'Spur von der Münze'], [['Probe P', 'tiefe Spur'], ['Probe Q', 'kaum eine Spur']], [30, 60])
auftrag('4a', 'Welche Probe ist härter? Kreuze an.', 1, before=2)
ankreuzen_l(['Probe P', 'Probe Q'])
auftrag('4b', 'Ein Brett wird oft angefasst. Welche Oberfläche ist gut? Kreuze an.', 1)
ankreuzen_l(['glatt und ohne Splitter', 'rau und mit Splittern'])

# ---- Aufgabe 5
aufgabe_l(5, 'Holz arbeitet', 'A7', 3)
satz('Ein Stück Holz wird getrocknet.')
tabelle_l(['', 'vorher', 'nachher'], [['Gewicht', '80 g', '68 g']], [30, 30, 30])
auftrag('5a', 'Das Holz ist jetzt leichter. Warum? Kreuze an.', 1, before=2)
ankreuzen_l(['Das Holz hat Wasser abgegeben.', 'Das Holz hat Wasser aufgenommen.'])
auftrag('5b', 'Setze die Wörter ein.', 2)
wortspeicher(['Quellen', 'Schwinden'])
luecke_l(['Holz nimmt Wasser auf. Es wird größer.',
          f'Das heißt: {GAPL}',
          'Holz gibt Wasser ab. Es wird kleiner.',
          f'Das heißt: {GAPL}'])

# ---- Aufgabe 6
page_break()
aufgabe_l(6, 'Holzfehler', 'A8', 4, before=0)
D.add_picture(str(OUT / 'fehler.png'), width=Mm(140))
pic = D.paragraphs[-1].paragraph_format
pic.left_indent = Mm(IND + 8); pic.keep_with_next = True; pic.space_after = Pt(4)
auftrag('6a', 'Welcher Fehler ist auf dem Bild? Trage die Zahl ein.', 3, before=2)
tabelle_l(['Zahl', 'Fehler', 'So sieht er aus'], [
    ['1', 'Ast', 'ein runder Fleck im Holz'],
    ['2', 'Riss', 'das Holz ist aufgerissen'],
    ['3', 'Verwerfen', 'das Brett ist krumm']], [18, 30, 80])
kaestchen_l(['Bild A', 'Bild B', 'Bild C'])
auftrag('6b', 'Ein Brett hat einen kleinen Ast. Der Ast sitzt fest. Was stimmt? Kreuze an.', 1)
ankreuzen_l(['Das Brett muss in den Müll.', 'Man kann das Brett oft noch benutzen.'])

# ---- Abschluss
spacer(10)
box([[('Fertig? Prüfe deine Arbeit.', True)],
     'Hast du in jede Lücke etwas geschrieben?',
     'Hast du bei jeder Ankreuzaufgabe 1 Kreuz gemacht?',
     [('So ging es mir:     □  gut      □  mittel      □  schwer', False)]], color=SCHIEFER, after=6)
t = D.add_table(rows=1, cols=2)
c0, c1 = t.rows[0].cells
run(c0.paragraphs[0], 'Punkte:   ______ / 18', FS, True)
run(c1.paragraphs[0], 'Feedback:', FS, True)
for _ in range(2):
    z = c1.add_paragraph(); z.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    z.paragraph_format.line_spacing = Pt(22)
for c in (c0, c1):
    cell_borders(c, top=(8, SCHIEFER), bottom=(8, SCHIEFER), left=(8, SCHIEFER), right=(8, SCHIEFER))
    cell_margins(c, 80, 80, 140, 140)
geometry(t, [55, 110])
keep_rows(t)
D.save(OUT / 'lernerfolgskontrolle-lernen.docx')

# =================================================================== Lösungsblatt Fassung 2
TEACHER = True
D = document('Lösungsblatt Holz  ·  Fassung 2', teacher=True)
D.styles['Normal'].font.size = Pt(10)
kopf_l('Lösung Holz · Fassung 2', 'LEHRKRAFT', 'Zieldifferente Fassung, Bildungsgang Lernen  ·  A1 bis A8  ·  18 Punkte')


def h(t):
    x = p(t, bold=True, size=11.5, color=SCHIEFER, keep=True, before=7, after=3)
    para_border(x, 'bottom', 4, LINIE, 2)


h('Einsatz')
p('Für Schülerinnen und Schüler mit zieldifferentem Lernen im Förderschwerpunkt Lernen. Gleicher Termin, gleiche Optik wie die Regelfassung; das Schülerblatt nennt den Förderschwerpunkt nicht (nur „Fassung 2“ in der Fußzeile).')
p('30 Minuten Open Book mit der gedruckten Mappe, kein iPad. Abweichungen (mehr Zeit, Vorlesen, Einzelplatz) nach Förderplan. Die Aufgaben dürfen vorgelesen werden; Fachwörter dürfen nicht erklärt werden, die Wortspeicher reichen.')
h('Was gegenüber der Regelfassung geändert ist')
table(['Bereich', 'Änderung'], [
    ['Sprache', 'Ein Gedanke pro Satz, keine Nebensätze, Du-Ansprache, konkrete Verben (Kreuze an, Trage ein, Zähle). 12,5 pt, größere Ankreuz- und Eintragefelder.'],
    ['Stützen', 'Wortspeicher mit Artikel (1, 5b), Bildlegende mit Kurzerklärung (6a), Zähltipp (2a), vorgegebener Startschritt (3a), Mappenverweis bei jeder Aufgabe.'],
    ['Inhalt', 'Mindeststandard A1 bis A8 mit wenigen leichten Regelstandard-Anteilen. Entfallen: Bast/Zuckertransport (1b), Prüfung von Sams Aussage (2c), Schnittbreite (3b), Ausbeute, Vergleichsbedingungen (4c), Schublade/Bewegungsreserve (5b), Bonus A9/A10.'],
    ['Antwortformat', 'Nur Einfachauswahl mit je zwei Antworten, keine Mehrfachauswahl, keine Minuspunkte. Reihenfolge mit 5 statt 6 Schritten.']],
    [32, 133], indent=0, keep_last=False, size=9)
h('Lösungen')
table(['Aufgabe', 'Lösung', 'Punkte'], [
    ['1', 'die Borke schützt; das Kambium lässt dicker werden; das Splintholz leitet Wasser. Artikel nicht bewerten.', 'je 1 P = 3'],
    ['2a', '12 (11 bis 13 bei erkennbar sorgfältigem Zählen anerkennen)', '1'],
    ['2b', 'Erste Antwort: nur wenig dicker geworden', '1'],
    ['3a', 'Baum 1, Fällen 2, Transport 3, Sägewerk 4, Brett 5. In gedruckter Reihenfolge: 3, 1, 5, 2, 4', 'je 0,5 P = 2'],
    ['3b', 'Plan B; 14 cm', 'je 1 P = 2'],
    ['4a', 'Probe Q', '1'],
    ['4b', 'glatt und ohne Splitter', '1'],
    ['5a', 'Das Holz hat Wasser abgegeben.', '1'],
    ['5b', 'größer: Quellen; kleiner: Schwinden', 'je 1 P = 2'],
    ['6a', 'Bild A = 2 (Riss), Bild B = 1 (Ast), Bild C = 3 (Verwerfen)', 'je 1 P = 3'],
    ['6b', 'Zweite Antwort: oft noch benutzen', '1'],
    ['', 'Gesamt', '18']], [20, 117, 28], indent=0, keep_last=False, size=9)
p('Rechtschreibung nicht bewerten, wenn das Wort erkennbar ist. Bei Ankreuzaufgaben zählt nur ein eindeutiges Kreuz; zwei Kreuze ergeben 0 Punkte.', before=4)
h('Bewertung')
p('Die Leistung wird an den individuellen Lernzielen gemessen (Förderplan, Vorgaben der AO-SF für den Bildungsgang Lernen), nicht am Maßstab der Regelfassung. Die 18 Punkte sind deshalb nicht mit den 28 Pflichtpunkten der Regelfassung vergleichbar. Ein Notenschlüssel wird hier bewusst nicht vorgegeben.')
p('Rückmeldebogen: „Individuelle Rückmeldung“ im Erwartungshorizont; Höchstpunkte hier 3, 2, 4, 2, 3, 4.')
D.save(OUT / 'loesung-lernen.docx')
print('Fassung 2: Schülerblatt und Lösungsblatt erzeugt. 18 Punkte.')
