"""Erzeugt die Lernerfolgskontrolle (max. 5 Seiten, Druckfassung) und den Erwartungshorizont.

Layout nach HBG-AB-Designsystem: A4, 3 cm Lochrand links, Arial 11 pt, Farbe nur als Linie
(keine Flächenfüllung, tonersparend), Aufgabenkopf mit Punktefeld, große Ankreuzkästchen,
Eintragekästchen für Zahlen und Lückenzeilen mit Schreibhöhe.

Benötigt nur python-docx. Danach rendern, z. B.:
  soffice --headless --convert-to pdf lernerfolgskontrolle.docx erwartungshorizont.docx
und alle Seiten visuell prüfen. Anschließend pruefungspaket.zip aktualisieren.
"""
from pathlib import Path
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_TAB_ALIGNMENT, WD_LINE_SPACING, WD_ALIGN_PARAGRAPH

OUT = Path(__file__).resolve().parent

# HBG-AB-Farben (nur als Linien/Schrift)
SCHIEFER = '2C3D4C'
ROST = 'D97A4A'
GOLD = 'C17B00'
TEXT = '1E2A35'
LINIE = 'BDBDBD'
MUTED = '666666'
FONT = 'Arial'

CONTENT_MM = 165  # 210 - 30 - 15

D = None  # aktuelles Dokument


def rgb(hexs):
    return RGBColor.from_string(hexs)


# ---------------------------------------------------------------- Grundlagen

def set_fonts(style, size, bold=None, color=TEXT):
    style.font.name = FONT
    style.font.size = Pt(size)
    style.font.color.rgb = rgb(color)
    if bold is not None:
        style.font.bold = bold
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), FONT)


def para_border(p, edge, sz, color, space=4):
    ppr = p._p.get_or_add_pPr()
    bdr = ppr.find(qn('w:pBdr'))
    if bdr is None:
        bdr = OxmlElement('w:pBdr'); ppr.append(bdr)
    e = OxmlElement('w:' + edge)
    e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz))
    e.set(qn('w:space'), str(space)); e.set(qn('w:color'), color)
    bdr.append(e)


def add_field(par, instr, size=8, color=MUTED):
    for kind, text in (('begin', None), ('instr', instr), ('separate', None), ('text', '1'), ('end', None)):
        r = par.add_run()
        r.font.size = Pt(size); r.font.color.rgb = rgb(color)
        if kind == 'instr':
            it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = f' {instr} '
            r._r.append(it)
        elif kind == 'text':
            r.text = text
        else:
            fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), kind); r._r.append(fc)


def run(par, text, size=11, bold=False, italic=False, color=TEXT):
    r = par.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic; r.font.color.rgb = rgb(color)
    return r


def document(title_footer, teacher=False):
    d = Document()
    s = d.sections[0]
    s.page_width = Mm(210); s.page_height = Mm(297)
    s.top_margin = Mm(18); s.bottom_margin = Mm(16)
    s.left_margin = Mm(30); s.right_margin = Mm(15)
    s.header_distance = Mm(8); s.footer_distance = Mm(8)
    s.different_first_page_header_footer = True

    normal = d.styles['Normal']
    set_fonts(normal, 10.5 if teacher else 11)
    pf = normal.paragraph_format
    pf.space_before = Pt(0); pf.space_after = Pt(3 if teacher else 4)
    pf.line_spacing = 1.08
    for name in ('Header', 'Footer'):
        set_fonts(d.styles[name], 8, color=MUTED)

    # Kopf ab Seite 2: Titel links, Namensfeld rechts (falls Blätter getrennt werden)
    hp = s.header.paragraphs[0]
    hp.paragraph_format.tab_stops.add_tab_stop(Mm(CONTENT_MM), WD_TAB_ALIGNMENT.RIGHT)
    run(hp, 'WP Technik 7  |  Vom Baum zum Holz  |  ' + title_footer, 8, color=MUTED)
    if not teacher:
        run(hp, '\tName: ______________________', 9, color=TEXT)
    para_border(hp, 'bottom', 4, LINIE, 3)

    for footer in (s.footer, s.first_page_footer):
        fp = footer.paragraphs[0]
        fp.paragraph_format.tab_stops.add_tab_stop(Mm(CONTENT_MM), WD_TAB_ALIGNMENT.RIGHT)
        run(fp, title_footer + '  |  30 Minuten Open Book  |  HBG Dortmund', 8, color=MUTED)
        run(fp, '\tSeite ', 8, color=MUTED)
        add_field(fp, 'PAGE')
        run(fp, ' von ', 8, color=MUTED)
        add_field(fp, 'NUMPAGES')
    return d


def p(text='', bold=False, size=None, italic=False, color=TEXT, keep=False, after=None, before=None, indent=0):
    x = D.add_paragraph()
    if text:
        run(x, text, size or (D.styles['Normal'].font.size.pt), bold, italic, color)
    f = x.paragraph_format
    if keep: f.keep_with_next = True
    if after is not None: f.space_after = Pt(after)
    if before is not None: f.space_before = Pt(before)
    if indent: f.left_indent = Mm(indent)
    return x


def page_break():
    # Umbruch an den letzten Absatz hängen: kein leerer Absatz, der eine Leerseite erzeugen kann
    from docx.enum.text import WD_BREAK
    D.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)


# ---------------------------------------------------------------- Tabellen

def cell_borders(cell, **edges):
    pr = cell._tc.get_or_add_tcPr()
    old = pr.find(qn('w:tcBorders'))
    if old is not None: pr.remove(old)
    b = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement('w:' + edge)
        spec = edges.get(edge)
        if spec:
            e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(spec[0])); e.set(qn('w:color'), spec[1])
        else:
            e.set(qn('w:val'), 'nil')
        b.append(e)
    pr.append(b)


def cell_margins(cell, top=50, bottom=50, left=100, right=100):
    pr = cell._tc.get_or_add_tcPr()
    m = OxmlElement('w:tcMar')
    for k, v in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        e = OxmlElement('w:' + k); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa'); m.append(e)
    pr.append(m)


def geometry(t, widths_mm, indent_mm=0):
    dxa = [round(w * 56.6929) for w in widths_mm]
    tbl = t._tbl; tp = tbl.tblPr
    for tag in ('w:tblW', 'w:tblLayout', 'w:tblInd'):
        o = tp.find(qn(tag))
        if o is not None: tp.remove(o)
    w = OxmlElement('w:tblW'); w.set(qn('w:w'), str(sum(dxa))); w.set(qn('w:type'), 'dxa'); tp.append(w)
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tp.append(lay)
    ind = OxmlElement('w:tblInd'); ind.set(qn('w:w'), str(round(indent_mm * 56.6929))); ind.set(qn('w:type'), 'dxa'); tp.append(ind)
    grid = tbl.tblGrid
    for gc, v in zip(grid.findall(qn('w:gridCol')), dxa):
        gc.set(qn('w:w'), str(v))
    for row in t.rows:
        for c, v in zip(row.cells, dxa):
            c.width = v * 635  # EMU


def keep_rows(t, keep_last=False):
    rows = list(t.rows)
    for i, row in enumerate(rows):
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        if i < len(rows) - 1 or keep_last:
            for c in row.cells:
                for z in c.paragraphs: z.paragraph_format.keep_with_next = True


def table(head, rows, widths, indent=5, keep_last=True, size=None):
    size = size or (10 if TEACHER else 10.5)
    t = D.add_table(rows=1, cols=len(head))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for c, txt in zip(t.rows[0].cells, head): c.text = txt
    for r in rows:
        for c, txt in zip(t.add_row().cells, r): c.text = str(txt)
    strong = (10, SCHIEFER); light = (4, LINIE)
    for i, row in enumerate(t.rows):
        for c in row.cells:
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if i == 0:
                cell_borders(c, top=strong, bottom=strong)
            else:
                cell_borders(c, bottom=light)
            cell_margins(c, 60, 60, 100, 100)
            for z in c.paragraphs:
                z.paragraph_format.space_before = z.paragraph_format.space_after = Pt(0)
                for r in z.runs:
                    r.font.size = Pt(size); r.bold = (i == 0)
                    r.font.color.rgb = rgb(SCHIEFER if i == 0 else TEXT)
    geometry(t, widths, indent)
    keep_rows(t, keep_last)
    spacer()
    return t


def spacer(pt=4, keep=False):
    x = D.add_paragraph(); f = x.paragraph_format
    f.space_after = Pt(0); f.space_before = Pt(0); f.line_spacing = Pt(pt)
    if keep: f.keep_with_next = True
    return x


# ---------------------------------------------------------------- Schülerkomponenten

IND = 5  # mm Einzug für Aufgabeninhalt


def kopf(titel, fach):
    x = D.add_paragraph(); f = x.paragraph_format
    f.tab_stops.add_tab_stop(Mm(CONTENT_MM), WD_TAB_ALIGNMENT.RIGHT)
    f.space_after = Pt(1)
    run(x, titel, 19, True, color=SCHIEFER)
    run(x, '\t' + fach, 9, True, color=SCHIEFER)
    m = p('HBG Dortmund  ·  Vom Baum zum Holz  ·  A1 bis A10', size=8, color=MUTED, after=0)
    para_border(m, 'bottom', 12, SCHIEFER, 5)
    spacer(5)


def identzeile():
    t = D.add_table(rows=2, cols=3)
    for i, label in enumerate(('NAME', 'KLASSE', 'DATUM')):
        c = t.rows[0].cells[i]; c.text = ''
        run(c.paragraphs[0], label, 7.5, color=MUTED)
        cell_borders(c); cell_margins(c, 0, 0, 0, 200)
        c2 = t.rows[1].cells[i]; c2.text = ''
        run(c2.paragraphs[0], ' ', 13)
        cell_borders(c2, bottom=(6, '333333')); cell_margins(c2, 0, 20, 0, 200)
        for cc in (c, c2):
            cc.paragraphs[0].paragraph_format.space_after = Pt(0)
    geometry(t, [85, 35, 45])
    spacer(6)


def infobox(lines, color=SCHIEFER):
    """Kasten mit farbiger linker Linie, ohne Füllung."""
    t = D.add_table(rows=1, cols=1)
    c = t.rows[0].cells[0]
    cell_borders(c, left=(24, color), top=(4, LINIE), bottom=(4, LINIE), right=(4, LINIE))
    cell_margins(c, 80, 80, 160, 140)
    first = True
    for text, bold in lines:
        z = c.paragraphs[0] if first else c.add_paragraph()
        first = False
        z.paragraph_format.space_after = Pt(3)
        if isinstance(text, list):
            for seg, b in text: run(z, seg, 10, b)
        else:
            run(z, text, 10, bold)
    c.paragraphs[-1].paragraph_format.space_after = Pt(0)
    geometry(t, [CONTENT_MM])
    keep_rows(t)
    spacer(8)


def aufgabe(nr, titel, tag, punkte, bonus=False, before=12):
    x = D.add_paragraph(); f = x.paragraph_format
    f.keep_with_next = True; f.space_before = Pt(before); f.space_after = Pt(5)
    f.left_indent = Mm(2.5)
    f.tab_stops.add_tab_stop(Mm(CONTENT_MM - 2.5), WD_TAB_ALIGNMENT.RIGHT)
    para_border(x, 'left', 24, GOLD if bonus else ROST, 6)
    run(x, f'Aufgabe {nr}', 12, True, color=SCHIEFER)
    run(x, f'   {titel}', 12, True)
    run(x, f'   {tag}', 8.5, color=MUTED)
    einheit = 'Bonuspunkte' if bonus else 'Punkte'
    run(x, f'\t____ / {punkte} {einheit}', 9.5, color=MUTED)
    return x


def teil(label, text, punkte=None, hint=None, keep=True, bold=True, before=6):
    x = D.add_paragraph(); f = x.paragraph_format
    f.left_indent = Mm(IND + 8); f.first_line_indent = Mm(-8)
    f.space_before = Pt(before); f.space_after = Pt(3); f.keep_with_next = keep
    run(x, label, 11, True, color=SCHIEFER)
    run(x, '\t' + text, 11, bold)
    f.tab_stops.add_tab_stop(Mm(IND + 8))
    if punkte:
        run(x, f'  ({punkte} P)', 9.5, color=MUTED)
    if hint:
        run(x, '  ' + hint, 10, italic=True, color=TEXT)
    return x


def text(t, keep=True, size=None, italic=False, after=3):
    x = p(t, size=size, italic=italic, keep=keep, after=after, indent=IND + 8)
    return x


def luecke(zeilen, keep_last=False):
    """Lückensätze mit Schreibhöhe (exakt 26 pt)."""
    out = []
    for i, z in enumerate(zeilen):
        x = D.add_paragraph(); f = x.paragraph_format
        f.left_indent = Mm(IND + 8); f.space_after = Pt(2)
        f.line_spacing_rule = WD_LINE_SPACING.EXACTLY; f.line_spacing = Pt(25)
        f.keep_with_next = keep_last or i < len(zeilen) - 1
        run(x, z, 11)
        out.append(x)
    return out


GAP = '______________________'
GAP_S = '____________'


def ankreuzen(optionen, keep_last=False):
    for i, o in enumerate(optionen):
        x = D.add_paragraph(); f = x.paragraph_format
        f.left_indent = Mm(IND + 16); f.first_line_indent = Mm(-8)
        f.tab_stops.add_tab_stop(Mm(IND + 16))
        f.space_before = Pt(1); f.space_after = Pt(2.5)
        f.keep_with_next = keep_last or i < len(optionen) - 1
        run(x, '□', 16)
        run(x, '\t' + o, 11)


def kaestchen(paare, label_mm, box_mm=11, pro_zeile=3, keep_last=False):
    """Eintragekästchen für Zahlen: paare = [(Beschriftung vor oder nach Kästchen)]."""
    zeilen = [paare[i:i + pro_zeile] for i in range(0, len(paare), pro_zeile)]
    t = D.add_table(rows=len(zeilen) * 2 - 1, cols=pro_zeile * 2)
    for zi, zeile in enumerate(zeilen):
        row = t.rows[zi * 2]
        row.height = Mm(box_mm); row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        for k, (lab, vor) in enumerate(zeile):
            box = row.cells[k * 2 + (1 if vor else 0)]
            labc = row.cells[k * 2 + (0 if vor else 1)]
            cell_borders(box, top=(12, '333333'), bottom=(12, '333333'), left=(12, '333333'), right=(12, '333333'))
            cell_borders(labc)
            cell_margins(labc, 0, 0, 120 if not vor else 0, 120)
            labc.text = ''; run(labc.paragraphs[0], lab, 11)
            if vor:
                labc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            for c in (box, labc):
                c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                c.paragraphs[0].paragraph_format.space_after = Pt(0)
        if zi < len(zeilen) - 1:
            gap = t.rows[zi * 2 + 1]
            gap.height = Mm(3); gap.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
            for c in gap.cells: cell_borders(c)
    widths = []
    for k in range(pro_zeile):
        widths += [label_mm, box_mm] if paare[0][1] else [box_mm, label_mm]
    geometry(t, widths, IND + 8)
    keep_rows(t, keep_last)
    spacer(6, keep_last)


def bild(path, width_mm, keep=True):
    D.add_picture(str(path), width=Mm(width_mm))
    x = D.paragraphs[-1]
    x.paragraph_format.left_indent = Mm(IND + 8)
    x.paragraph_format.keep_with_next = keep
    x.paragraph_format.space_after = Pt(2)


EINE = 'Nur eine Antwort ist richtig.'
MEHR = 'Mehrere Antworten sind richtig.'

# =================================================================== Schülerblatt
TEACHER = False
D = document('Lernerfolgskontrolle Holz')
kopf('Lernerfolgskontrolle Holz', 'WP TECHNIK 7')
identzeile()
infobox([
    ('Arbeitszeit: 30 Minuten. Du darfst das gedruckte Material deiner Mappe benutzen. '
     'Das iPad und andere digitale Geräte darfst du nicht benutzen.', True),
    ('Arbeite allein. Trage Zahlen oder kurze Wörter ein. Bei Ankreuzaufgaben steht dabei, ob eine oder '
     'mehrere Antworten richtig sind. Kreuze nur die richtigen Aussagen an.', False),
    ('Bei Mehrfachauswahl kostet jedes falsche Kreuz einen Punkt in dieser Teilaufgabe; '
     'weniger als 0 Punkte gibt es nicht.', False),
    ([('Pflicht: ', True), ('Aufgaben 1 bis 6 zu A1 bis A8, 28 Punkte.  ', False),
      ('Bonus: ', True), ('Aufgabe 7 zu A9/A10 ist freiwillig (4 Punkte).', False)], False),
])

# ---- Seite 1
aufgabe(1, 'Aufbau des Stamms', 'A1', 4, before=4)
teil('1a', 'Ergänze. Nutze deine Mappe.', 2)
luecke([f'Das {GAP} ermöglicht das Dickenwachstum.',
        f'Das {GAP} leitet Wasser von den Wurzeln nach oben.'], keep_last=False)
teil('1b', 'Der Bast ist rings um den Stamm unterbrochen. Welche Folge ist möglich?', 2, EINE)
ankreuzen(['Die Wurzeln bekommen zu wenig Zucker aus den Blättern.',
           'Das Mark bildet sofort eine neue Borke.',
           'Der Stamm kann keine Jahresringe mehr zeigen.'])

aufgabe(2, 'Jahresringe auswerten', 'A2', 4)
# Bild links, Hinweis und 2a rechts (spart Höhe, Bild bleibt neben der Frage)
t = D.add_table(rows=1, cols=2)
lc, rc = t.rows[0].cells
for c in (lc, rc):
    cell_borders(c); cell_margins(c, 0, 0, 0, 120)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
lc.paragraphs[0].add_run().add_picture(str(OUT / 'ringe.png'), width=Mm(70))
z = rc.paragraphs[0]; z.paragraph_format.space_after = Pt(8)
run(z, 'Die Mitte ist ein Punkt. Jede Kreislinie begrenzt einen Jahresring. Die Rinde ist nicht '
    'dargestellt. Die Zeichnung ist ein Modell.', 10, italic=True)
z = rc.add_paragraph(); z.paragraph_format.space_after = Pt(4)
run(z, '2a  ', 11, True, color=SCHIEFER); run(z, 'Trage nur die Zahl ein.', 11, True); run(z, '  (1 P)', 9.5, color=MUTED)
z = rc.add_paragraph(); z.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
z.paragraph_format.line_spacing = Pt(26); z.paragraph_format.space_after = Pt(0)
run(z, 'Alter: etwa ________ Jahre', 11)
geometry(t, [82, 70], IND + 8)
keep_rows(t, keep_last=True)
spacer(4, keep=True)

teil('2b', 'Ring 8 ist schmaler als die Nachbarringe. Was zeigt das?', 1, EINE)
ankreuzen(['Der Stamm ist in diesem Jahr weniger in die Dicke gewachsen.',
           'Der Baum ist in diesem Jahr kleiner geworden.'])
teil('2c', 'Sam sagt: „In Jahr 8 hat es bestimmt zu wenig geregnet.“ Prüfe die Aussage.', 2, MEHR)
ankreuzen(['Wassermangel ist eine mögliche Ursache.',
           'Die Ringbreite beweist Wassermangel.',
           'Auch Licht, Temperatur oder Konkurrenz können das Wachstum beeinflussen.',
           'Ein schmaler Ring zeigt, wie hoch der Baum war.'])

# ---- Seite 2
page_break()
aufgabe(3, 'Produktionsweg und Schnittplan', 'A3  A4', 6, before=0)
teil('3a', 'Ordne die Schritte. Trage nur die Zahlen 1 bis 6 in die Kästchen ein. '
     '1 ist der Anfang. Nutze jede Zahl einmal.', 3)
kaestchen([('Transport', False), ('Schnittholz', False), ('Baum', False),
           ('Einschnitt', False), ('Fällen', False), ('Sägewerk', False)], label_mm=36)
teil('3b', 'Ergänze ein passendes Wort.', 1)
luecke([f'Beim Sägen entstehen {GAP}, weil das Sägeblatt eine Schnittbreite hat.'])
teil('3c', 'Du brauchst mindestens 12 cm breite Bretter. Du darfst schmale Bretter nicht '
     'zusammenleimen. Nutze die Übungsdaten.', bold=True)
table(['Plan', 'Ausbeute', 'Breite jedes Bretts'], [['A', '72 %', '9 cm'], ['B', '64 %', '14 cm']],
      [25, 40, 60], indent=IND + 8)
x = text('Wähle den passenden Plan.', after=2)
run(x, '  (1 P)  ', 9.5, color=MUTED); run(x, EINE, 10, italic=True)
ankreuzen(['Plan A', 'Plan B'])
x = text('Ergänze:  ', after=2); run(x, '(1 P)', 9.5, color=MUTED)
luecke(['Dieser Plan passt, weil seine Bretter ________ cm breit sind.'])

# ---- Seite 3
page_break()
aufgabe(4, 'Holzproben vergleichen', 'A5  A6', 6, before=0)
text('Zwei gleich große, ähnlich trockene Proben werden mit derselben Münze bei möglichst gleichem '
     'Druck geprüft. Die Angaben sind Übungsdaten.')
table(['Probe', 'Masse', 'Druckspur'], [['P', '45 g', 'deutliche Spur'], ['Q', '68 g', 'kaum eine Spur']],
      [25, 35, 65], indent=IND + 8)
teil('4a', 'Welche Probe ist in diesem Test härter?', 1, EINE)
ankreuzen(['Probe P', 'Probe Q'])
teil('4b', 'Ergänze ein passendes Wort.', 1)
luecke([f'Die härtere Probe erkenne ich daran, dass die Münze {GAP_S} eine Spur hinterlässt.'])
teil('4c', 'Eine dritte Probe ist doppelt so groß und wiegt 80 g. Welche Aussagen stimmen?', 2, MEHR)
ankreuzen(['Ihre größere Masse kann an ihrer Größe liegen.',
           'Die Masse von 80 g beweist, dass das Holz am härtesten ist.',
           'Für einen fairen Massevergleich sollten die Proben gleich groß und ähnlich trocken sein.',
           'Beim Massevergleich spielt die Feuchtigkeit keine Rolle.'])
teil('4d', 'Verbinde Beobachtung, Eigenschaft und Verwendung. Welche Aussagen passen?', 2, MEHR)
ankreuzen(['Eine glatte Oberfläche ohne Splitter eignet sich für ein häufig angefasstes Brett.',
           'Geringe Wasseraufnahme ist bei wechselnder Feuchtigkeit eine günstige Eigenschaft.',
           'Eine deutliche Druckspur beweist, dass das Holz für stark belastete Oberflächen besonders hart ist.'])

# ---- Seite 4
page_break()
aufgabe(5, 'Holz arbeitet', 'A7', 4, before=0)
text('Dieselbe Probe wird vor und nach dem Trocknen gemessen. Die Angaben sind Übungsdaten.')
table(['Messwert', 'Vorher feucht', 'Nach dem Trocknen'], [['Masse', '80 g', '68 g'], ['Breite', '50 mm', '49 mm']],
      [40, 42, 45], indent=IND + 8)
teil('5a', 'Ergänze zwei passende Wörter.', 2)
luecke([f'Die Masse sinkt, weil das Holz {GAP} abgibt.',
        f'Die Breite nimmt ab. Diese Verkleinerung heißt {GAP}.'])
teil('5b', 'Eine Holzschublade klemmt in einem feuchten Raum. Ergänze zwei passende Wörter.', 2)
luecke([f'Das Holz kann Wasser aufnehmen und {GAP}.',
        f'Beim Bau lässt du deshalb etwas {GAP} für die Bewegung.'])

aufgabe(6, 'Holzfehler finden', 'A8', 4)
bild(OUT / 'fehler.png', 148)
text('Bild C zeigt ein Brett von der Seite über einer geraden Unterlage.', size=10, italic=True)
teil('6a', 'Ordne zu. Trage nur die Zahlen ein: 1 = Ast, 2 = Verwerfen, 3 = Riss.', 3)
kaestchen([('Bild A', True), ('Bild B', True), ('Bild C', True)], label_mm=26)
teil('6b', 'Ein Brett hat einen kleinen, fest verwachsenen Ast. Welche Aussage stimmt?', 1, EINE)
ankreuzen(['Das Brett muss immer weggeworfen werden.',
           'Ob der Ast stört, hängt von seiner Lage und der Nutzung des Bretts ab.',
           'Ein Ast macht jedes Brett automatisch tragfähiger.'])

# ---- Seite 5
page_break()
infobox([('Freiwillige Bonusaufgabe zu A9 und A10', True),
         ('Aufgabe 7 gehört nicht zum Pflichtteil. Wenn du sie auslässt, verlierst du keine Pflichtpunkte. '
          'Es gibt keine zusätzliche Arbeitszeit. Prüfe zuerst deine Pflichtaufgaben.', False)], color=GOLD)
aufgabe(7, 'Eine Produktkarte ausfüllen', 'A9  A10', 4, bonus=True, before=0)
text('Eine Kundin braucht ein Regal für einen trockenen Innenraum. Die Oberfläche soll hart und glatt sein. '
     'Von den passenden Holzarten möchte sie die preiswertere. Wähle für ihre Produktkarte eine Holzart, '
     'passende Eigenschaften und einen Nachteil. Vergleiche nur die Angaben in der Tabelle.').runs[0].bold = True
text('Die Tabelle enthält vereinfachte Übungsangaben. Alle angebotenen Bretter haben passende Maße.',
     size=10, italic=True)
table(['Holzart', 'Oberfläche und Bearbeitung', 'Preis', 'Grenze'], [
    ['Fichte', 'weich; lässt sich glatt bearbeiten', 'niedrig', 'Druckstellen entstehen leicht'],
    ['Buche', 'hart; lässt sich glatt bearbeiten', 'mittel', 'arbeitet stark bei wechselnder Feuchte'],
    ['Eiche', 'hart; lässt sich glatt bearbeiten', 'hoch', 'teurer als Buche']],
    [22, 50, 20, 60], indent=IND + 8)
teil('7a', 'Welche Holzart erfüllt den Auftrag am besten?', 1, EINE)
ankreuzen(['Fichte', 'Buche', 'Eiche'])
teil('7b', 'Ergänze deine Begründung mit zwei passenden Wörtern.', 2)
luecke(['Die gewählte Holzart eignet sich, weil ihre Oberfläche',
        f'{GAP} ist und sich {GAP} bearbeiten lässt.'])
teil('7c', 'Ergänze einen passenden Nachteil.', 1)
luecke([f'Bei wechselnder Feuchtigkeit arbeitet dieses Holz {GAP}.'])

spacer(14)
infobox([('Prüfe deine Arbeit', True),
         ('Lies deine Antworten noch einmal. Sind alle Zahlen und Lücken ausgefüllt? '
          'Hast du bei jeder Ankreuzaufgabe auf den Hinweis geachtet?', False)], color=SCHIEFER)

# Auswertungsfeld für die Lehrkraft
t = D.add_table(rows=2, cols=2)
for c, lab in zip(t.rows[0].cells, ('Pflichtpunkte:   ______ / 28', 'Bonus:   ______ / 4')):
    c.text = ''; run(c.paragraphs[0], lab, 11, True)
m = t.rows[1].cells[0].merge(t.rows[1].cells[1])
m.text = ''; run(m.paragraphs[0], 'Feedback:', 11, True)
for _ in range(2):
    z = m.add_paragraph(); z.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    z.paragraph_format.line_spacing = Pt(24)
for row in t.rows:
    for c in row.cells:
        cell_borders(c, top=(8, SCHIEFER), bottom=(8, SCHIEFER), left=(8, SCHIEFER), right=(8, SCHIEFER))
        cell_margins(c, 80, 80, 140, 140)
geometry(t, [82.5, 82.5])
keep_rows(t)
D.save(OUT / 'lernerfolgskontrolle.docx')

# =================================================================== Erwartungshorizont
TEACHER = True
D = document('Erwartungshorizont Holz', teacher=True)
kopf('Erwartungshorizont Holz', 'LEHRKRAFT')


def h(t):
    x = p(t, bold=True, size=12, color=SCHIEFER, keep=True, before=9, after=3)
    para_border(x, 'bottom', 4, LINIE, 2)


p('Zur fünfseitigen Lernerfolgskontrolle mit 30 Minuten Arbeitszeit, 28 Pflichtpunkten (A1 bis A8) und 4 freiwilligen Bonuspunkten (A9/A10). Erlaubt ist das gedruckte Material der Mappe. iPad und andere digitale Geräte sind ausgeschlossen.')
h('Durchführung und Zeitplanung')
p('Die fünf Seiten gemeinsam ausgeben (einseitig drucken und heften oder beidseitig; Seite 5 enthält nur die Bonusaufgabe und das Auswertungsfeld). Orientierung: Aufgaben 1 und 2 etwa 7 Minuten, 3 und 4a bis 4c etwa 8 Minuten, 4d bis 6 etwa 7 Minuten, abschließende Pflichtkontrolle etwa 3 Minuten; verbleibende 5 Minuten optional für Bonusaufgabe 7. Das Nachschlagen ist in diesen Planwerten enthalten; nach dem ersten Einsatz prüfen. Vereinbarte Nachteilsausgleiche beachten.')
h('Bewertung')
p('Pflichtteil und Bonus getrennt dokumentieren: Pflicht maximal 28 Punkte, Bonus maximal 4 Punkte. Auslassen der Bonusaufgabe mindert das Pflichtergebnis nicht. 32 Punkte sind kein Pflichtnenner. Die Bonusanrechnung bei einer Note wird vorab durch die Lehrkraft festgelegt; hier wird kein Notenschlüssel vorgegeben.')
p('Sinngemäße Lückenfüllungen anerkennen. Rechtschreibfehler nicht abziehen, sofern der Fachbegriff eindeutig ist. Jeder Teil wird getrennt bewertet. Ein falsches Kreuz in 4a verhindert nicht den Punkt für eine fachlich passende Begründung in 4b. Kein automatisch abgeleiteter Notenschlüssel.')
p('Einfachauswahl: Nur das richtige und kein weiteres Feld angekreuzt ergibt die genannten Punkte. Mehrfachauswahl 2c, 4c und 4d: je richtig gesetztem Kreuz 1 Punkt, je falsch gesetztem Kreuz 1 Punkt Abzug innerhalb der Teilaufgabe; mindestens 0, höchstens 2 Punkte. Nicht gesetzte Kreuze geben keine Punkte. Ein vollständig leeres Feld ergibt 0 Punkte. So wird nicht wahlloses Ankreuzen belohnt.')
h('Lösungen zu Aufgaben 1 bis 4')
for title, body in [
    ('1 Aufbau des Stamms A1   4 Punkte', '1a Kambium; Splintholz: je 1 P. 1b Erste Aussage: Die Wurzeln bekommen zu wenig Zucker aus den Blättern; 2 P bei eindeutiger Auswahl. Die Störung des Zuckertransports wird aus der Funktion des Basts abgeleitet.'),
    ('2 Jahresringe   4 Punkte', '2a 12 Jahre: 1 P. 2b Erste Aussage (geringerer Dickenzuwachs): 1 P. 2c Erste und dritte Aussage: Wassermangel ist möglich, andere Ursachen kommen ebenfalls infrage; bis 2 P nach Mehrfachregel.'),
    ('3 Produktionsweg und Schnittplan A3 A4   6 Punkte', '3a In der gedruckten Reihenfolge: 3, 6, 1, 5, 2, 4. Je korrekt eingetragener Zahl 0,5 P, insgesamt 3 P. 3b Späne / Sägespäne: 1 P. 3c Plan B: 1 P; 14 cm: 1 P. Die höhere Ausbeute von A genügt bei einer Mindestbreite von 12 cm nicht.'),
    ('4 Holzproben   6 Punkte', '4a Probe Q: 1 P. 4b kaum: 1 P. 4c Erste und dritte Aussage: Größere Masse kann durch größeres Volumen entstehen; gleiche Größe und ähnliche Trockenheit erlauben einen fairen Vergleich; bis 2 P nach Mehrfachregel. 4d Erste und zweite Aussage: Glätte ohne Splitter ist für häufiges Anfassen günstig; geringe Wasseraufnahme ist bei wechselnder Feuchte günstig. Eine tiefe Druckspur spricht für geringere Härte. Bis 2 P nach Mehrfachregel.')]:
    p(title, bold=True, keep=True, before=4, after=1); p(body)
page_break()
h('Lösungen und Kompetenzbelege')
for title, body in [
    ('5 Holz arbeitet A7   4 Punkte', '5a Wasser; Schwinden: je 1 P. Auch „Feuchtigkeit“ bzw. „schwinden“ sinngemäß akzeptieren. 5b quellen / größer werden; Spiel / Platz / Abstand: je 1 P. Das Quellen kann zum Klemmen führen; die Bewegungsreserve ist eine passende Vorsorge.'),
    ('6 Holzfehler   4 Punkte', '6a A = 3, B = 1, C = 2: je 1 P. 6b Zweite Aussage: Lage und Nutzung entscheiden; 1 P bei eindeutiger Auswahl. Ein fest verwachsener Ast ist kein pauschaler Ausschussgrund.'),
    ('7 Freiwilliger Bonus A9 A10   4 Bonuspunkte', '7a Buche: 1 P. Nach Tabelle erfüllen Buche und Eiche Härte und glatte Bearbeitbarkeit; Buche ist von beiden preiswerter. 7b hart; glatt: je 1 P. 7c stark / deutlich: 1 P. Die Lückensätze werden unabhängig von 7a bewertet; kein mehrfacher Abzug eines Auswahlfehlers.')]:
    p(title, bold=True, keep=True, before=4, after=1); p(body)
h('Was die kurze Arbeit nachweisen kann')
p('Die geschlossene oder stark gestützte Antwortform prüft Verstehen und Anwenden mit wenig Schreibaufwand. Sie belegt keine frei formulierte ausführliche Erklärung. Die früheren 21 Teilaufgaben a bis c und deren Raster gelten für diese Fassung nicht mehr. Eine Gesamtpunktzahl wird deshalb nicht automatisch in einen Kompetenzstandard übersetzt.')
table(['Anforderung', 'Belege in dieser Arbeit'], [
    ['Mindeststandard', 'Funktionen ergänzen (1a), Ringe zählen (2a), Schritte ordnen (3a), Begriffe und Bilder zuordnen (6a)'],
    ['Regelstandard', 'Ringbreite deuten (2b), Schnittbreite erklären (3b), Härte aus Druckspur ableiten (4a/b), Trocknungsdaten erklären (5a), Beobachtung mit Verwendung verbinden (4d); optional: Eigenschaften mit Auftrag verbinden (7b/c)'],
    ['Expertenstandard', 'Folge einer Bastschädigung ableiten (1b), Grenze einer Aussage prüfen (2c), Mindestbreite gegen Ausbeute abwägen (3c), Vergleichsbedingungen prüfen (4c), Vorsorge übertragen (5b), Verwendbarkeit beurteilen (6b), optional: mehrere Anforderungen abwägen (7a)']],
    [38, 127], indent=0, keep_last=False)
p('Die Expertenbelege sind hier kurze, gestützte Entscheidungen. Für Aussagen über selbstständiges Argumentieren zusätzlich die Mappe oder ein Gespräch heranziehen.')
page_break()
h('Individuelle Rückmeldung')
p('Name: ____________________________  Datum: ______________')
p('Pflichtpunkte: ______ / 28    Freiwilliger Bonus: ______ / 4', after=6)
table(['Bereich', 'Punkte', 'Dein nächster Übungsauftrag'], [
    ['Stamm', '____ / 4', 'A1'], ['Jahresringe', '____ / 4', 'A2'], ['Produktionsweg und Schnittplan', '____ / 6', 'A3 und A4'],
    ['Holzproben', '____ / 6', 'A5 und A6'], ['Holzfeuchte', '____ / 4', 'A7'], ['Holzfehler', '____ / 4', 'A8'],
    ['Freiwilliger Bonus', '____ / 4', 'A9 und A10 (optional)']], [72, 28, 65], indent=0, keep_last=False)
h('Das gelingt dir schon')
for _ in range(2): luecke(['________________________________________________________________'])
h('Deine nächsten Schritte')
luecke(['Übe zuerst: ______________________________________________________',
        'Passender Auftrag: ________________________________________________',
        'Wenn nötig, übe danach: ___________________________________________'])
p('Erkläre einen dieser Zusammenhänge in zwei eigenen Sätzen auf U.1. Besprich deine Erklärung mit einem Partner oder deiner Lehrkraft.', before=6)
D.save(OUT / 'erwartungshorizont.docx')
print('Lernerfolgskontrolle: 5 geplante Seiten. Erwartungshorizont: 3 geplante Seiten. Pflicht 28 P, Bonus 4 P.')
