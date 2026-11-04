"""Einzelblätter Möbelwerkstatt: Ideenblatt, Protokollblatt, Ergebnisbogen (je 1 Seite, DOCX + PDF).

Digital gedacht: Bearbeitung in GoodNotes, Upload in TaskCards. Darum farbige Flächen erlaubt.
Farben = TaskCards-Farbcode: Ideen lila #8C3CDD · Protokoll blau #3C3CDD · Ergebnis grün #3CDD3C
Aufruf: python3 tools/build_moebelbau_blaetter.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx.shared import Pt, Mm, RGBColor  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from build_moebelbau_druck import new_doc, Builder, to_pdf, OUT  # noqa: E402

LILA, BLAU, GRUEN = '8C3CDD', '3C3CDD', '3CDD3C'


def mix(hexcol, f):
    """Farbe mit Weiß mischen (f = Anteil der Farbe)."""
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    return ''.join(f'{round(255 - (255 - c) * f):02X}' for c in (r, g, b))


def dark(hexcol, f=0.62):
    """Abgedunkelte Variante für gut lesbare Schrift (v. a. beim hellen Grün)."""
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    return ''.join(f'{round(c * f):02X}' for c in (r, g, b))


def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def shade_par(par, fill):
    pPr = par._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    pPr.append(shd)


def table_borders(t, color, sz='6'):
    tblPr = t._tbl.tblPr
    for old in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(old)
    bd = OxmlElement('w:tblBorders')
    for edge in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        e = OxmlElement('w:' + edge)
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), sz); e.set(qn('w:color'), color)
        bd.append(e)
    tblPr.append(bd)


class FarbBuilder(Builder):
    def __init__(self, D, farbe):
        super().__init__(D)
        self.farbe = farbe
        self.hell = mix(farbe, 0.16)
        self.linie = mix(farbe, 0.45)
        self.text = dark(farbe) if farbe == GRUEN else farbe

    def table(self, headers, rows, *a, first_col=False, **k):
        t = super().table(headers, rows, *a, **k)
        table_borders(t, self.linie)
        if headers:
            for c in t.rows[0].cells:
                shade_cell(c, self.hell)
                for q in c.paragraphs:
                    for r in q.runs:
                        r.font.color.rgb = RGBColor.from_string(self.text)
        if first_col:
            for row in t.rows[(1 if headers else 0):]:
                shade_cell(row.cells[0], self.hell)
        return t

    def lines(self, n=2, h=None):
        for _ in range(n):
            z = self.p()
            pf = z.paragraph_format
            pf.space_after = pf.space_before = Pt(0)
            pf.line_spacing = Pt(h or self.line_h)
            self._border(z, ['bottom', 'between'], self.linie, '4')

    def box(self, label=None, height=50, hint=None):
        z = self.p(' ', size=9)
        z.paragraph_format.line_spacing = Pt(height)
        z.paragraph_format.space_after = Pt(6)
        self._border(z, ['top', 'left', 'bottom', 'right'], self.farbe, '12')


def kopf(b, marke, titel, hinweis):
    t = b.D.add_table(rows=1, cols=1)
    c = t.rows[0].cells[0]
    shade_cell(c, b.farbe)
    q = c.paragraphs[0]
    weiss = 'FFFFFF' if b.farbe != GRUEN else '143D14'  # helles Grün: dunkle Schrift für Kontrast
    r = q.add_run(marke + '\n'); r.bold = True; r.font.size = Pt(10)
    r.font.color.rgb = RGBColor.from_string(weiss)
    r = q.add_run(titel); r.bold = True; r.font.size = Pt(22)
    r.font.color.rgb = RGBColor.from_string(weiss)
    q.paragraph_format.space_before = Pt(6); q.paragraph_format.space_after = Pt(6)
    q.paragraph_format.left_indent = Mm(2)
    table_borders(t, b.farbe)
    sp = b.p(); sp.paragraph_format.line_spacing = Pt(4); sp.paragraph_format.space_after = Pt(4)
    b.p('Name: ______________________________   Datum: ______________   Woche: ____', size=10.5)
    z = b.p(hinweis, size=9.5)
    z.runs[0].font.color.rgb = RGBColor.from_string(b.text)


def abschnitt(b, wort, sub=None, nr=None):
    """Abschnittskopf als farbig hinterlegter Balken."""
    lead = f'{nr}  {wort}' if nr else wort
    z = b.p(('   ' + sub) if sub else '', bold_lead=lead, size=10)
    z.runs[0].font.size = Pt(12.5)
    z.runs[0].font.color.rgb = RGBColor.from_string(b.text)
    if sub:
        z.runs[-1].font.color.rgb = RGBColor.from_string('555555')
    pf = z.paragraph_format
    pf.space_before = Pt(6); pf.space_after = Pt(3)
    shade_par(z, b.hell)
    b._border(z, ['left'], b.farbe, '36')


def feld(b, text, n=1, size=10):
    b.p(text, size=size).paragraph_format.space_after = Pt(0)
    b.lines(n)


# ------------------------------------------------------------------ Ideenblatt
def ideenblatt():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Ideenblatt')
    b = FarbBuilder(D, LILA)
    b.line_h = 21
    kopf(b, 'IDEE', 'Meine Möbelidee Nr. ____',
         'Für jede Idee ein eigenes Blatt. In GoodNotes ausfüllen, dann in TaskCards als lila Karte hochladen.')
    b.table(None, [['Für wen?', ''], ['Welches Problem löst es?', '']],
            [1.5, 5], height=10, size=10, first_col=True)
    abschnitt(b, 'Skizze', 'Zeichne deine Idee mit den wichtigsten Maßen in mm. Gern auch eine zweite Ansicht.')
    b.box(None, 218)
    abschnitt(b, 'Beschreibung')
    feld(b, 'Das ist meine Idee (Was ist es? Woraus besteht es?):', 2)
    feld(b, 'Anwendung – so wird es benutzt (wo, wie, wofür?):', 2)
    feld(b, 'Das ist das Besondere oder Neue daran:', 1)
    b.table(None, [
        ['Weg:', '[  ] Modell aus Eisstielen     [  ] Original aus Dachlatte'],
        ['Material (grob):', ''],
        ['Kurzcheck:', '[  ] in 6 Wochen schaffbar    [  ] sicher baubar    [  ] passt zur Teamgröße'],
    ], [1.5, 5], height=8.5, size=10, first_col=True)
    path = OUT / 'ideenblatt.docx'
    D.save(path)
    return path


# --------------------------------------------------------------- Protokollblatt
def protokollblatt():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Protokoll einer Werkstatteinheit')
    b = FarbBuilder(D, BLAU)
    b.line_h = 20
    kopf(b, 'PROTOKOLL', 'Meine Werkstatteinheit',
         'Ein Blatt pro Einheit. In GoodNotes ausfüllen, dann in TaskCards als blaue Karte hochladen.')
    b.p('Einheit:   [  ] Montag (45 Min.)     [  ] Mittwoch (90 Min.)', size=10.5)

    abschnitt(b, 'PLANEN', 'zu Beginn der Stunde', nr='1')
    feld(b, 'Das habe ich mir letztes Mal als nächsten Schritt vorgenommen:', 1)
    feld(b, 'Mein Ziel für heute – am Ende der Stunde habe ich …', 2)
    b.table(['Meine Schritte heute', 'erledigt?'],
            [[f'{i}.', '[  ] ja  [  ] teils  [  ] nein'] for i in (1, 2, 3)],
            [4, 2.5], height=7.5, size=9.5, pad=1.5)
    b.p('Das brauche ich (Material, Werkzeug, Lehrgang L__): ______________________________', size=10)
    feld(b, 'Daran erkenne ich, dass ich mein Ziel erreicht habe:', 1)

    abschnitt(b, 'DURCHFÜHREN', 'während der Arbeit', nr='2')
    feld(b, 'Das habe ich geschafft:', 2)
    feld(b, 'Problem und meine Lösung:', 2)
    b.p('Hilfe:  [  ] Hilfekarte H___  [  ] Team  [  ] Lehrkraft  [  ] keine      '
        'Foto vom Stand:  [  ] ja  [  ] nein', size=9.5)

    abschnitt(b, 'REFLEKTIEREN', 'am Ende der Stunde', nr='3')
    b.table(['', 'noch nicht', 'teilweise', 'gut', 'sehr gut'], [
        ['Ich habe mein Ziel erreicht.', '[  ]', '[  ]', '[  ]', '[  ]'],
        ['Ich habe konzentriert gearbeitet.', '[  ]', '[  ]', '[  ]', '[  ]'],
        ['Ich habe sicher und ordentlich gearbeitet.', '[  ]', '[  ]', '[  ]', '[  ]'],
        ['Im Team lief es gut. (nur bei Teamarbeit)', '[  ]', '[  ]', '[  ]', '[  ]'],
    ], [3.6, 0.9, 0.9, 0.7, 0.8], size=9.5, pad=1.5)
    feld(b, 'Mein nächster Schritt:', 1)
    path = OUT / 'protokollblatt.docx'
    D.save(path)
    return path


# ---------------------------------------------------------------- Ergebnisbogen
def ergebnisbogen():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Ergebnis und Selbstbewertung')
    b = FarbBuilder(D, GRUEN)
    b.line_h = 20
    kopf(b, 'ERGEBNIS · SELBSTBEWERTUNG', 'Mein fertiges Projekt',
         'Ergänzt die Fotos deines fertigen Werkstücks. In GoodNotes ausfüllen, dann in TaskCards '
         'als grüne Karte hochladen.')
    b.table(None, [
        ['Mein Werkstück:', ''],
        ['Weg / Team:', '[  ] Modell   [  ] Original      [  ] allein   [  ] mit: ____________________'],
    ], [1.5, 5], height=8, size=10, first_col=True)
    b.p('Meine Fotos in TaskCards:   [  ] von vorn   [  ] von der Seite   [  ] Detail einer Verbindung   '
        '[  ] im Einsatz', size=9.5)

    abschnitt(b, 'Mein Test')
    b.table(['Mein Prüfkriterium', 'Ergebnis', 'erfüllt?'],
            [['', '', '[  ] ja  [  ] teils  [  ] nein'] for _ in range(2)],
            [2.8, 2, 2.1], height=10, size=9.5, pad=1.5)

    abschnitt(b, 'So schätze ich mein Werkstück ein',
              '++ sehr gut · + gelungen · o teilweise · – noch nicht')
    rows = [
        ['Funktion', 'Es erfüllt seine Aufgabe und meine Prüfkriterien.'],
        ['Maße', 'Es passt zu meiner Skizze.'],
        ['Verbindungen', 'Sie sind fest und sauber.'],
        ['Oberfläche und Kanten', 'geschliffen, keine Splitter, behandelt'],
        ['Stabilität', 'Es steht sicher, wackelt und kippt nicht.'],
        ['Arbeitsweise', 'Ich habe sicher, sauber und selbstständig gearbeitet.'],
    ]
    t = b.table(['', 'Daran erkennt man es', '++', '+', 'o', '–', 'Begründung (Stichwort)'],
                [[k, d, '', '', '', '', ''] for k, d in rows],
                [1.35, 2.3, 0.35, 0.35, 0.35, 0.35, 1.9], height=8.5, size=9, pad=1.2,
                first_col=True)
    b.bold_cells(t)

    abschnitt(b, 'Rückblick')
    feld(b, 'Das habe ich nach dem Test verbessert:', 1)
    feld(b, 'Darauf bin ich besonders stolz:', 1)
    feld(b, 'Das mache ich beim nächsten Projekt anders:', 1)
    b.table(['Rückmeldung der Lehrkraft'], [['']], [1], height=20, size=10)
    path = OUT / 'ergebnisbogen.docx'
    D.save(path)
    return path


if __name__ == '__main__':
    for path in [ideenblatt(), protokollblatt(), ergebnisbogen()]:
        to_pdf(path)
        print('erstellt:', path.name, '+ PDF')
