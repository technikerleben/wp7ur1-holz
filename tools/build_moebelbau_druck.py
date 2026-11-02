"""Druckmaterial Möbelwerkstatt: Projektübersicht + Projektbogen (DOCX + PDF).

Stil wie tools/build_mappe.py: A4, Arial, monochrome Überschriften,
Schreiblinien, Zeichenwörter (MAPPE, HALTEPUNKT, HILFE, KONTROLLE).
Aufruf: python3 tools/build_moebelbau_druck.py
"""
from pathlib import Path
import subprocess
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'moebelbau' / 'druck'
OUT.mkdir(parents=True, exist_ok=True)
INK = '263844'
TEXT_W = 170  # mm


# ---------------------------------------------------------------- Grundgerüst
def new_doc(header, landscape=False):
    D = Document()
    sec = D.sections[0]
    sec.page_width, sec.page_height = (Mm(297), Mm(210)) if landscape else (Mm(210), Mm(297))
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
    sec.top_margin = sec.bottom_margin = Mm(16)
    sec.left_margin = sec.right_margin = Mm(20)
    sec.header_distance = sec.footer_distance = Mm(8)
    for name, size, before, after in [('Normal', 11, 0, 5), ('Title', 24, 0, 6),
                                      ('Subtitle', 12, 0, 6), ('Heading 1', 19, 0, 8),
                                      ('Heading 2', 12.5, 11, 5), ('Heading 3', 11, 8, 4)]:
        s = D.styles[name]
        s.font.name = 'Arial'
        rf = s.element.rPr.rFonts
        for a in ['asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme']:
            rf.attrib.pop(qn('w:' + a), None)
        for a in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
            rf.set(qn('w:' + a), 'Arial')
        s.font.size = Pt(size)
        s.font.color.rgb = RGBColor.from_string(INK)
        s.font.italic = False
        pf = s.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), 1.2
    D.styles['Normal'].font.color.rgb = RGBColor.from_string('222222')
    for sty in D.styles:  # Rahmenlinien der Standard-Titelstile entfernen
        if sty.element.pPr is not None:
            for b in list(sty.element.pPr.findall(qn('w:pBdr'))):
                sty.element.pPr.remove(b)
    for name in ['Header', 'Footer']:
        D.styles[name].font.name = 'Arial'
        D.styles[name].font.size = Pt(8.5)
    sec.header.paragraphs[0].text = header
    f = sec.footer.paragraphs[0]
    f.text = 'Möbelwerkstatt · Alles aus Dachlatte · Seite '
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    f._p.append(fld)
    return D


class Builder:
    def __init__(self, D, width=TEXT_W):
        self.D = D
        self.width = width
        self._pb = False

    def _para(self, text='', style=None):
        z = self.D.add_paragraph(text, style)
        if self._pb:
            z.paragraph_format.page_break_before = True
            self._pb = False
        return z

    def p(self, text='', style=None, bold_lead=None, size=None, align=None):
        z = self._para(style=style)
        if bold_lead:
            z.add_run(bold_lead).bold = True
        if text:
            z.add_run(text)
        if size:
            for r in z.runs:
                r.font.size = Pt(size)
        if align == 'center':
            z.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return z

    def h1(self, t):
        return self._para(t, 'Heading 1')

    def h(self, t):
        return self._para(t, 'Heading 2')

    def h3(self, t):
        return self._para(t, 'Heading 3')

    def brk(self):
        self._pb = True

    def _border(self, z, edges, color='999999', sz='4'):
        pp = z._p.get_or_add_pPr()
        b = OxmlElement('w:pBdr')
        for edge in edges:
            a = OxmlElement('w:' + edge)
            a.set(qn('w:val'), 'single'); a.set(qn('w:sz'), sz)
            a.set(qn('w:color'), color); a.set(qn('w:space'), '6')
            b.append(a)
        pp.append(b)

    def lines(self, n=2):
        for _ in range(n):
            z = self.p()
            pf = z.paragraph_format
            pf.space_after = pf.space_before = Pt(0)
            pf.line_spacing = Pt(23)
            self._border(z, ['bottom', 'between'], 'AAAAAA', '3')

    def box(self, label=None, height=50, hint=None):
        if label:
            self.h(label)
        z = self.p(hint or ' ', size=9)
        if hint:
            z.runs[0].font.color.rgb = RGBColor.from_string('777777')
        z.paragraph_format.line_spacing = Pt(height)
        z.paragraph_format.space_after = Pt(6)
        self._border(z, ['top', 'left', 'bottom', 'right'])

    def note(self, word, text):
        """Zeichenwort + Satz, mit linker Linie (tonersparend, keine Fläche)."""
        z = self.p(text, bold_lead=word + ': ')
        z.paragraph_format.left_indent = Mm(3)
        self._border(z, ['left'], INK, '18')
        return z

    def table(self, headers, rows, widths=None, height=None, size=10, header_bold=True, pad=2.5):
        D = self.D
        t = D.add_table(rows=1 if headers else 0, cols=len(widths or headers or rows[0]))
        t.style = 'Table Grid'
        if headers:
            for c, txt in zip(t.rows[0].cells, headers):
                c.text = txt
        for row in rows:
            cells = t.add_row().cells
            for c, txt in zip(cells, row):
                c.text = str(txt)
        n = len(t.columns)
        widths = widths or [1] * n
        mm = [self.width * w / sum(widths) for w in widths]
        # feste Spaltenbreiten (Word + LibreOffice)
        t.autofit = False
        tblPr = t._tbl.tblPr
        lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
        grid = t._tbl.tblGrid
        for gc, w in zip(grid.findall(qn('w:gridCol')), mm):
            gc.set(qn('w:w'), str(round(w / 25.4 * 1440)))
        for i, row in enumerate(t.rows):
            for c, w in zip(row.cells, mm):
                c.width = Mm(w)
                for q in c.paragraphs:
                    pf = q.paragraph_format
                    pf.space_after = pf.space_before = Pt(pad)
                    pf.line_spacing = 1.1
                    for r in q.runs:
                        r.font.size = Pt(size)
                        if i == 0 and headers and header_bold:
                            r.bold = True
            row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
            if height and (i > 0 or not headers):
                row.height = Mm(height)
                row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        if headers:
            t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
        sp = self.p()
        pf = sp.paragraph_format
        pf.space_after = Pt(4); pf.space_before = Pt(0); pf.line_spacing = Pt(4)
        return t

    def bold_cells(self, t, col=0, start=1):
        for row in t.rows[start:]:
            for q in row.cells[col].paragraphs:
                for r in q.runs:
                    r.bold = True


def to_pdf(docx_path):
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir',
                    str(docx_path.parent), str(docx_path)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ------------------------------------------------------- gemeinsame Inhalte
WEGE = [
    ['', 'Weg M: Modell', 'Weg O: Originalgröße'],
    ['Hauptmaterial', 'Holz-Eisstiele', 'Dachlatten (Fichte/Tanne, z. B. 24 × 48 mm)'],
    ['Dazu', 'Holzleim, Klammern, Furnier; für Bewegliches kleine Achsen',
     'Leim, Schrauben, Holzdübel, kleine Scharniere; anderes Material nur, wenn du es begründest'],
    ['Arbeitsgänge', 'Dekupiersäge, Platten durch Kreuzverleimung, Furnier aufbringen',
     'Stichsäge, Handschleifgerät, Akkuschrauber, Leimen, Verschrauben, Holzdübel'],
    ['Darauf kommt es an', 'Proportionen, Maßstab (z. B. 1:5 oder 1:10), Leimen, Aussteifen',
     'Nutzmaße, Zuschnitt, Vorbohren, Schrauben, Standfestigkeit'],
    ['So wird geprüft', 'passend zum Modell, z. B. mit Modellfigur oder kleiner Prüflast',
     'mit einer vorher vereinbarten, kleinen Gebrauchslast'],
]

TEAM = [
    ['', 'Allein', 'Zu zweit', 'Zu dritt (höchstens)'],
    ['Weg M\nModell',
     'ein kleines Modell aus einem Baukörper, z. B. Hocker, Ständer oder Ablage',
     'ein größeres Modell oder zwei Möbel, die zusammengehören, z. B. Tisch mit Stuhl',
     'ein mehrteiliges Modell, z. B. eine Möbelgruppe oder eine Zimmerecke mit mehreren Möbeln'],
    ['Weg O\nOriginal',
     'ein Kleinmöbel, z. B. Beistelltisch, Buchständer oder Ablage',
     'ein größeres Möbel mit mehreren Baugruppen, z. B. niedriges Regal oder Caddy mit Fächern',
     'ein größeres Möbel oder zwei Module, die sich kombinieren lassen, z. B. Modulregal'],
    ['Jede Person …', 'plant und baut alles selbst.',
     '… verantwortet mindestens eine eigene Baugruppe.',
     '… verantwortet mindestens eine eigene Baugruppe bzw. ein eigenes Möbelteil.'],
]

# Lehrgänge: (Code, Name, Gruppe, Pflicht, Das lernst du, Das zeigst du am Ende)
# Pflicht = Maschine/Elektrowerkzeug: erst nach Lehrgang + Unterschrift im Werkstattpass.
GRUPPEN = [('alle', 'Für alle'), ('O', 'Weg O – Original aus Dachlatte'), ('M', 'Weg M – Modell aus Eisstielen')]
LEHRGAENGE = [
    ('L1', 'Richtig schleifen', 'alle', False,
     'von grob nach fein schleifen (z. B. Körnung 80 → 120 → 180), immer mit der Faser, '
     'mit Schleifklotz, Kanten brechen',
     'Probestück ohne Querkratzer, Kanten gebrochen'),
    ('L2', 'Oberflächen ölen oder lasieren', 'alle', False,
     'Staub entfernen, dünn auftragen, Überschuss abnehmen, trocknen lassen; '
     'Öl-Lappen richtig entsorgen',
     'gleichmäßig behandeltes Probestück; du erklärst die Lappen-Regel'),
    ('L3', 'Stichsäge', 'O', True,
     'Latte fest einspannen, Schutzbrille, Fußplatte aufsetzen, erst einschalten, dann sägen; '
     'Blatt nur ohne Akku/Stecker wechseln',
     'gerader Schnitt entlang einer Anrisslinie'),
    ('L4', 'Handschleifgerät', 'O', True,
     'Schleifpapier wechseln, Werkstück sichern, Absaugung nutzen, ohne Druck führen',
     'Fläche glatt geschliffen, Kanten nicht abgerundet'),
    ('L5', 'Akkuschrauber', 'O', True,
     'Bohrer und Bit einsetzen, Drehrichtung und Drehmoment einstellen, Werkstück einspannen',
     'Loch gerade vorgebohrt, Schraube bündig eingedreht'),
    ('L6', 'Leimen', 'O', False,
     'Leim dünn auftragen, Zwingen mit Zulagen ansetzen, Winkel prüfen, Leimreste feucht abwischen',
     'rechtwinklige Leimverbindung'),
    ('L7', 'Verschrauben', 'O', False,
     'anreißen, Randabstand beachten, vorbohren, senken, passende Schraubenlänge wählen '
     '(vorher L5)',
     'Lattenecke ohne Riss verschraubt'),
    ('L8', 'Holzdübel', 'O', False,
     'Bohrstellen mit Dübelmarker übertragen, Bohrtiefe begrenzen, Dübel mit Leim einsetzen, '
     'pressen (vorher L5 und L6)',
     'bündige Dübelverbindung'),
    ('L9', 'Dekupiersäge', 'M', True,
     'Niederhalter einstellen, Blatt prüfen, Finger seitlich vom Blatt, langsam vorschieben, '
     'Schutzbrille, lange Haare zusammenbinden',
     'Kurve sauber nach Anriss aus einer Platte gesägt'),
    ('L10', 'Platten durch Kreuzverleimung', 'M', False,
     'Eisstiele in Lagen quer zueinander verleimen, pressen, trocknen lassen; '
     'verstehen, warum Kreuzlagen stabiler sind',
     'ebene, zweilagige Platte; du erklärst das Prinzip'),
    ('L11', 'Furnier aufbringen', 'M', False,
     'Furnier mit Cutter am Stahllineal zuschneiden, Faserrichtung wählen, dünn leimen, pressen, '
     'Überstand bündig schleifen',
     'furniertes Probestück ohne Blasen'),
]
PFLICHT_TXT = 'Stichsäge, Handschleifgerät, Akkuschrauber und Dekupiersäge'


def lehrgang_name(code, name, pflicht):
    return f'{code}  {name}' + ('\nPFLICHT' if pflicht else '')


IDEEN = [
    ['Schreibtischständer', 'für Buch oder Tablet, fest oder neigbar'],
    ['Materialablage', 'offene Ablage oder Caddy mit Fächern'],
    ['Niedriges Regal', 'freistehend, mit geringer Höhe'],
    ['Beistelltisch', 'stabile Beine, Querstreben, kleine Last'],
    ['Variables Möbel', 'klappbar oder verstellbar, mit Anschlägen'],
    ['Modulsystem', 'zwei oder mehr Teile, die zusammenpassen'],
]


# ============================================================ Projektübersicht
def build_uebersicht():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Projektübersicht')
    b = Builder(D)
    b.p('ANSCHLUSSPROJEKT · MÖBELBAU', 'Subtitle')
    D.add_paragraph('Alles aus Dachlatte – Möbelwerkstatt', 'Title')
    b.p('6 Wochen · montags 45 Minuten · mittwochs 90 Minuten')

    b.h('Dein Auftrag')
    b.p('Entwickle und baue ein Möbelstück, das eine echte Aufgabe erfüllt. '
        'Wer braucht es? Was muss es können? Das findest du selbst heraus.')
    b.note('DU ENTSCHEIDEST',
           'Du wählst dein Möbelstück, deinen Materialweg, dein Team und dein Niveau. '
           'Die Ideen auf Seite 2 sind nur Anregungen. Eigene Ideen sind ausdrücklich erwünscht. '
           'Die Lehrkraft prüft bei der Freigabe nur: Ist es sicher? Ist es in 6 Wochen schaffbar?')

    b.h('Zwei Wege – gleich viel wert')
    t = b.table(WEGE[0], WEGE[1:], [1.1, 2, 2.4], size=9.5)
    b.bold_cells(t)
    b.p('Für alle: richtig schleifen und die Oberfläche ölen oder lasieren. '
        'Alle Arbeitsgänge lernst du in kurzen Lehrgängen (Seite 3).', size=10)
    b.p('Ein Modell ist keine leichte Ersatzaufgabe. Ein großes Möbel ist nicht automatisch besser. '
        'Gute Planung, saubere Arbeit und ein ehrlicher Test zählen.', size=10)

    b.h('Teamgröße bestimmt den Umfang')
    b.p('Ihr arbeitet allein, zu zweit oder zu dritt. Mehr als drei Personen sind nicht möglich. '
        'Je größer das Team, desto größer darf das Projekt sein.', size=10.5)
    t = b.table(TEAM[0], TEAM[1:], [0.9, 1.7, 1.9, 2.1], size=9.5)
    b.bold_cells(t)
    b.p('Größer heißt: mehr Bauteile, mehr Baugruppen, mehr Planung. Größer heißt nicht: höher oder '
        'stärker belastbar. Die Sicherheitsregeln gelten für alle.', size=10)

    b.brk()
    b.h1('Dein Projektweg')
    plan = [
        ['1', 'Ideen finden: Bedarf entdecken, mindestens drei eigene Ideen skizzieren, Team bilden',
         'Projektbogen Teil 1–2'],
        ['2', 'Planen: Zeichnung mit Maßen, Stückliste, Aufgaben im Team verteilen, '
              'nötige Lehrgänge buchen',
         'HALTEPUNKT Freigabe'],
        ['3', 'Bauen I: Lehrgänge besuchen, Bauteile herstellen, erste Verbindungen',
         'Werkstattpass, Bautagebuch'],
        ['4', 'Bauen II: montieren, aussteifen, schleifen', 'Bautagebuch'],
        ['5', 'Testen: eigene Prüfkriterien prüfen, Schwachstelle finden', 'HALTEPUNKT Test'],
        ['6', 'Verbessern, erneut testen, Oberfläche ölen oder lasieren, vorstellen',
         'HALTEPUNKT Abnahme'],
    ]
    b.table(['Woche', 'Das machst du', 'Meilenstein'], plan, [0.7, 4.2, 1.6], size=10)
    b.p('Vor der Freigabe wird nichts endgültig zugeschnitten. Wer früher fertig ist, '
        'stellt sich selbst eine technische Zusatzanforderung, z. B. verstellbar, '
        'kombinierbar oder materialsparend – nicht nur mehr Deko.', size=10)

    b.h('Ideenspeicher – nur falls du nicht weiterkommst')
    rows = [[f'{a} – {x}', f'{c} – {y}'] for (a, x), (c, y) in zip(IDEEN[::2], IDEEN[1::2])]
    b.table(None, rows, [1, 1], size=9.5)
    b.p('Jede Idee geht als Modell oder im Original. Ein Stuhl oder eine Bank ist nur als '
        'Modell möglich. Noch besser: eine Idee, die es hier nicht gibt.', size=10)

    b.h('Sicher arbeiten')
    for s in [f'{PFLICHT_TXT} benutzt du erst nach dem Lehrgang und mit Unterschrift '
              'im Werkstattpass. Keine Kreissägen.',
              'Einzelne Eisstiele kürzt du von Hand. An die Dekupiersäge kommen nur verleimte Platten '
              'und sicher geführte Teile. Kurze Lattenstücke spannst du fest ein.',
              'Dachlatten vorher prüfen: Äste, Risse, Splitter, Verzug. Kanten sorgfältig schleifen.',
              'Öl-Lappen können sich selbst entzünden: ausgebreitet trocknen lassen oder in den '
              'geschlossenen Metallbehälter.',
              'Keine Sitzmöbel, Kletterteile oder hohen Regale in Originalgröße. '
              'Modelle werden nicht wie echte Möbel belastet.']:
        z = b.p('• ' + s, size=10)
        z.paragraph_format.space_after = Pt(2)

    b.h('Daran erkennst du ein gutes Projekt')
    krit = [
        ['Eigene Idee', 'Ich habe einen echten Bedarf gefunden und selbst entschieden.'],
        ['Planung', 'Zeichnung, Maße und Stückliste passen zusammen.'],
        ['Fertigung', 'Ich arbeite maßgenau, sauber und sicher.'],
        ['Funktion', 'Mein Möbel besteht meine eigenen Prüfkriterien – oder ich habe es verbessert.'],
        ['Material', 'Ich gehe sparsam mit Material um und kenne meinen Verbrauch.'],
        ['Reflexion', 'Ich kann erklären, was ich warum verändert habe.'],
    ]
    t = b.table(None, krit, [1.2, 5], size=10)
    b.bold_cells(t, start=0)
    b.p('Nicht bewertet werden Größe, absolute Traglast, Verzierung oder die Anzahl verbrauchter Stiele.',
        size=9.5)

    # --- Seite 3: Lehrgänge
    b.brk()
    b.h1('Lehrgänge – kurz lernen, sicher bauen')
    b.p('Ein Lehrgang ist eine kurze Einführung bei der Lehrkraft: etwa 10 bis 15 Minuten, '
        'höchstens 4 Personen, während der Arbeitsphase. Du buchst ihn selbst – dann, '
        'wenn dein Projekt ihn braucht.', size=10.5)
    b.note('PFLICHT', f'{PFLICHT_TXT} benutzt du erst, wenn du den Lehrgang gemacht hast und '
                      'die Lehrkraft im Werkstattpass unterschrieben hat.')
    b.h('So buchst du einen Lehrgang')
    for i, s in enumerate([
            'Plane im Projektbogen (Teil 5): Welche Arbeitsgänge brauche ich? Kreuze sie im Werkstattpass an.',
            'Trage dich auf der Buchungsliste ein – spätestens eine Stunde vorher.',
            'Mach beim Lehrgang mit und zeige am Ende dein Probestück.',
            'Die Lehrkraft unterschreibt im Werkstattpass. Jetzt darfst du den Arbeitsgang selbst nutzen.'], 1):
        z = b.p(f'{i}.  {s}', size=10)
        z.paragraph_format.space_after = Pt(2)
    b.p('Lehrgänge des anderen Wegs darfst du auch buchen, wenn dein Entwurf sie braucht. '
        'Dir fehlt ein Arbeitsgang? Schlage einen eigenen Lehrgang vor.', size=10)
    for key, label in GRUPPEN:
        b.h3(label)
        rows = [[lehrgang_name(c, n, pf), inh, nw] for c, n, g, pf, inh, nw in LEHRGAENGE if g == key]
        t = b.table(['Lehrgang', 'Das lernst du', 'Das zeigst du am Ende'], rows,
                    [1.5, 3.6, 1.9], size=8.5, pad=1.5)
        b.bold_cells(t)
    path = OUT / 'projektuebersicht.docx'
    D.save(path)
    return path


# ============================================================== Projektbogen
def build_bogen():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Projektbogen')
    b = Builder(D)

    def page(code, title, goal=None, first=False):
        if not first:
            b.brk()
        b.h1(f'{code}  |  {title}')
        if goal:
            b.p(goal, bold_lead='Lernziel: ')

    # --- Deckblatt
    b.p('MEIN PROJEKTBOGEN', 'Subtitle')
    D.add_paragraph('Möbelwerkstatt', 'Title')
    b.p('Alles aus Dachlatte · Modell oder Original')
    b.p('Name: ___________________________________   Klasse: __________')
    b.p('Mein Team: ______________________________________________________')
    b.h('So arbeitest du')
    b.p('Jede Person führt einen eigenen Projektbogen. Entscheidungen im Team schreibt ihr alle auf. '
        'Der Bogen ist deine Planung, dein Bautagebuch und dein Nachweis. Er gehört in die Mappe.')
    b.note('DU ENTSCHEIDEST',
           'Was du baust, entscheidest du. Auf diesen Seiten findest du Fragen, die dir beim '
           'Entscheiden helfen. Es gibt keine fertige Bauanleitung.')
    b.h('Meine Meilensteine')
    ms = [
        ['1', 'Idee und Entscheidung', 'Teil 1–2', '', ''],
        ['2', 'Freigabe der Planung', 'Teil 3–5', '', ''],
        ['3', 'Erster Funktionstest', 'Teil 7', '', ''],
        ['4', 'Verbesserung und Abnahme', 'Teil 8–9', '', ''],
    ]
    b.table(['Nr.', 'Meilenstein', 'Seiten', 'Datum', 'Kürzel Lehrkraft'], ms,
            [0.5, 2.6, 1.1, 1.2, 1.5], height=11)
    b.h('Hier findest du Hilfe')
    b.p('Hilfekarten im Lernnavigator: H1 Von der Idee zur Zeichnung · H2 Maßstab · '
        'H3 Dachlatten prüfen · H4 Verbindungen · H5 Aussteifen · H6 Kippen und Prüfen · '
        'H7 Zuschnitt und Kosten · H8 Verbessern mit Test', size=10)
    b.p('Erst selbst probieren, dann die Hilfekarte, dann das Team, dann die Lehrkraft.', size=10)
    b.p('Arbeitsgänge lernst du in Lehrgängen. Du buchst sie auf der Buchungsliste. '
        'Was du schon darfst, steht in deinem Werkstattpass auf der nächsten Seite.', size=10)

    # --- Werkstattpass
    page('Werkstattpass', 'Meine Lehrgänge', 'Ich lerne Arbeitsgänge, bevor ich sie brauche.')
    b.note('PFLICHT', f'{PFLICHT_TXT}: Du benutzt sie erst, wenn hier die Unterschrift '
                      'der Lehrkraft steht.')
    b.p('Kreuze an, was du für dein Projekt brauchst. Buche dann einen Termin. '
        'Nach dem Lehrgang zeigst du dein Probestück. Die Lehrkraft trägt Datum und Kürzel ein.',
        size=10)
    for key, label in GRUPPEN:
        b.h3(label)
        rows = [[lehrgang_name(c, n, pf), '[  ]', '', '', '']
                for c, n, g, pf, inh, nw in LEHRGAENGE if g == key]
        t = b.table(['Lehrgang', 'brauche ich', 'gebucht für', 'bestanden am', 'Kürzel Lehrkraft'],
                    rows, [2.6, 1, 1.3, 1.3, 1.3], height=9, size=9.5)
        b.bold_cells(t)
    b.h3('Mein eigener Lehrgangswunsch')
    b.table(['Arbeitsgang', 'Warum brauche ich ihn?', 'bestanden am', 'Kürzel Lehrkraft'],
            [['', '', '', ''] for _ in range(2)], [2, 2.9, 1.3, 1.3], height=9, size=9.5)

    # --- Teil 1
    page('Teil 1', 'Bedarf entdecken', 'Ich finde eine echte Aufgabe für ein Möbelstück.')
    b.h('1.1 | MAPPE  Wo fehlt etwas?')
    b.p('Schau dich um: in deinem Zimmer, im Klassenraum, im Werkraum, bei Familie oder Freunden. '
        'Was liegt herum? Was ist unpraktisch? Wem könntest du helfen?')
    b.table(['Ort', 'Das Problem', 'Wer hätte etwas davon?'],
            [['', '', ''] for _ in range(3)], [1.3, 3, 2], height=13)
    b.h('1.2 | MAPPE  Meine drei Ideen')
    b.p('Skizziere mindestens drei unterschiedliche Ideen. Schnelle Skizzen reichen. '
        'Mindestens eine Idee soll ganz von dir sein – nicht aus dem Ideenspeicher.')
    t = b.table(['Idee 1', 'Idee 2', 'Idee 3'], [['', '', '']], [1, 1, 1], height=62)
    b.p('Name: ____________________    Name: ____________________    Name: ____________________',
        size=9.5)
    b.note('HILFE', 'Kein Einfall? Frage: Was nervt mich jeden Tag? '
                    'Oder öffne den Ideenspeicher auf der Projektübersicht.')

    # --- Teil 2
    page('Teil 2', 'Entscheiden', 'Ich treffe eine begründete Entscheidung.')
    b.h('2.1 | MAPPE  Ideen vergleichen')
    b.p('Bewerte jede Idee: ++ sehr gut · + gut · – eher nicht. Ergänze ein eigenes Kriterium.')
    b.table(['Kriterium', 'Idee 1', 'Idee 2', 'Idee 3'], [
        ['Löst ein echtes Problem', '', '', ''],
        ['Ist in 6 Wochen schaffbar', '', '', ''],
        ['Passt zu unserer Teamgröße', '', '', ''],
        ['Ist sicher baubar', '', '', ''],
        ['Ist neu oder eigen', '', '', ''],
        ['Eigenes Kriterium: ____________', '', '', ''],
    ], [3, 1, 1, 1], height=9)
    b.h('2.2 | MAPPE  Unsere Entscheidung')
    b.p('Wir bauen: ____________________________________________________________')
    b.p('für (Person/Ort): _____________________________________________________')
    b.p('Materialweg:   [  ] Weg M – Modell aus Eisstielen     [  ] Weg O – Original aus Dachlatte')
    b.p('Teamgröße:   [  ] allein     [  ] zu zweit     [  ] zu dritt')
    b.p('Ich starte auf:   [  ] Niveau 1 Anwenden   [  ] Niveau 2 Konstruieren   '
        '[  ] Niveau 3 Optimieren')
    b.p('Darum haben wir uns so entschieden:')
    b.lines(3)
    b.p('Das ist an unserer Idee neu oder eigen:')
    b.lines(2)
    b.note('KONTROLLE', 'Passt der Umfang zur Teamgröße? Schau in die Tabelle auf der Projektübersicht.')

    # --- Teil 3
    page('Teil 3', 'Anforderungen und Team', 'Ich lege fest, was mein Möbel können muss.')
    b.h('3.1 | MAPPE  Was muss unser Möbel können?')
    b.table(['Muss es können', 'Wäre schön'], [['', ''] for _ in range(3)], [1, 1], height=10)
    b.h('3.2 | MAPPE  Unsere Prüfkriterien')
    b.p('Schreibe mindestens zwei Kriterien, die man prüfen kann. '
        'Beispiel: „Der Ständer hält ein Buch mit 1 kg, ohne zu kippen.“')
    b.table(['Nr.', 'Prüfkriterium', 'So prüfen wir es'],
            [['1', '', ''], ['2', '', ''], ['3', '', '']], [0.5, 3.2, 2.8], height=12)
    b.h('3.3 | MAPPE  Teamvertrag')
    b.p('Bei Einzelarbeit: Notiere nur deine Hauptbaugruppen und lass die Regeln weg.', size=10)
    b.table(['Name', 'Ich bin verantwortlich für (Baugruppe / Möbelteil)', 'Unterschrift'],
            [['', '', ''] for _ in range(3)], [1.6, 3.4, 1.5], height=12)
    b.p('Unsere Regeln für die Zusammenarbeit:')
    b.lines(2)
    b.p('Wenn wir uns nicht einig sind, machen wir es so:')
    b.lines(1)

    # --- Teil 4
    page('Teil 4', 'Konstruktionszeichnung', 'Ich zeichne mein Möbel maßhaltig.')
    b.h('4.1 | MAPPE  Zeichnung mit Maßen')
    b.p('Zeichne dein Möbel in einer Ansicht oder als Skizze von schräg. Trage alle wichtigen Maße '
        'in mm ein. Markiere die Baugruppen und wer sie baut.')
    b.box(None, 330)
    b.p('Gesamtmaße (B × T × H): ______ × ______ × ______ mm      '
        'Nur Weg M – Maßstab: 1 : ______', size=10.5)
    b.note('HILFE', 'H1 Von der Idee zur Zeichnung · H2 Maßstab umrechnen')

    # --- Teil 5
    page('Teil 5', 'Stückliste und Arbeitsplan', 'Ich plane Material und Arbeitsschritte.')
    b.h('5.1 | MAPPE  Stückliste')
    b.table(['Nr.', 'Bauteil', 'Anzahl', 'Länge (mm)', 'Material', 'Wer?'],
            [[str(i), '', '', '', '', ''] for i in range(1, 9)],
            [0.5, 2.4, 0.8, 1.2, 1.6, 1.1], height=7.5, size=9.5)
    b.h('5.2 | MAPPE  Materialbedarf')
    b.p('Weg O: Dachlatte gesamt ______ m (plus ca. 10 % Verschnitt = ______ m)')
    b.p('Weg M: Eisstiele gesamt ______ Stück      Sonstiges: _______________________________')
    b.p('Verbindungen (z. B. leimen, schrauben, Scharnier): ______________________________')
    b.h('5.3 | MAPPE  Reihenfolge der Arbeitsschritte')
    b.table(['Schritt', 'Was wird gemacht?', 'Werkzeug', 'Wer?'],
            [[str(i), '', '', ''] for i in range(1, 7)], [0.6, 3.4, 1.6, 1], height=8, size=9.5)
    b.h('5.4 | MAPPE  Meine Lehrgänge')
    b.p('Für meine Arbeitsschritte brauche ich diese Lehrgänge (z. B. L3, L7):  '
        '__________________________')
    b.p('Kreuze sie im Werkstattpass an und trage dich auf der Buchungsliste ein.', size=10)
    b.note('HILFE', 'H3 Dachlatten prüfen · H4 Verbindungen · H7 Zuschnitt und Kosten · '
                    'Lehrgangsübersicht: Projektübersicht Seite 3')

    # --- Teil 6 Freigabe
    page('Teil 6', 'Freigabe', 'Ich prüfe meine Planung, bevor ich säge.')
    b.note('HALTEPUNKT', 'Zeige deine Planung der Lehrkraft. Erst nach der Freigabe '
                         'schneidest du Material zu.')
    b.h('6.1 | KONTROLLE  Unsere Planung ist vollständig')
    b.table(['Prüfpunkt', 'Wir', 'Lehrkraft'], [
        ['Das Möbel löst ein echtes Problem (Teil 1–2).', '[  ]', '[  ]'],
        ['Der Umfang passt zur Teamgröße.', '[  ]', '[  ]'],
        ['Die Zeichnung hat alle wichtigen Maße.', '[  ]', '[  ]'],
        ['Stückliste und Zeichnung passen zusammen.', '[  ]', '[  ]'],
        ['Es gibt mindestens zwei prüfbare Prüfkriterien.', '[  ]', '[  ]'],
        ['Jede Person hat eine eigene Baugruppe.', '[  ]', '[  ]'],
        ['Nötige Lehrgänge sind im Werkstattpass angekreuzt und gebucht.', '[  ]', '[  ]'],
        ['Wer eine Maschine nutzt, macht vorher den Pflicht-Lehrgang.', '[  ]', '[  ]'],
        ['Kein Sitzmöbel, kein hohes Regal in Originalgröße.', '[  ]', '[  ]'],
    ], [5, 0.8, 1.1], height=8.5)
    b.h('6.2 | Rückmeldung der Lehrkraft')
    b.p('Materialrahmen: _________________________________________________________')
    b.p('Bitte noch ändern:')
    b.lines(4)
    b.p('[  ] Freigegeben      Datum: ______________      Kürzel: ______________')

    # --- Bautagebuch
    page('Bautagebuch', 'Was habe ich geschafft?', 'Ich plane meine nächsten Schritte selbst.')
    b.p('Fülle am Ende jeder Bauphase eine Zeile aus. So weißt du beim nächsten Mal sofort weiter.')
    b.table(['Datum', 'Das habe ich geschafft', 'Problem und meine Lösung', 'Nächster Schritt'],
            [['', '', '', ''] for _ in range(7)], [0.9, 2.1, 2.1, 1.6], height=31, size=9.5)

    # --- Teil 7 Test
    page('Teil 7', 'Funktionstest', 'Ich prüfe mein Möbel ehrlich und finde Schwachstellen.')
    b.note('HALTEPUNKT', 'Plant den Test mit der Lehrkraft. Testet nur mit der vereinbarten Last.')
    b.h('7.1 | MAPPE  Erster Test')
    b.table(['Prüfkriterium (aus 3.2)', 'Ergebnis', 'Erfüllt?'],
            [['', '', 'ja / teils / nein'] for _ in range(3)], [3, 2.6, 1.2], height=15)
    b.h('7.2 | MAPPE  Schwachstelle')
    b.p('Diese Stelle hat nicht gut funktioniert:')
    b.lines(2)
    b.p('Ich vermute als Ursache:')
    b.lines(2)
    b.box('7.3 | MAPPE  Meine Verbesserungsidee (Skizze)', 190)
    b.note('HILFE', 'H5 Aussteifen · H6 Kippen und Prüfen · H8 Verbessern mit Test')

    # --- Teil 8 Verbesserung
    page('Teil 8', 'Verbessern und erneut testen', 'Ich zeige mit einem Test, dass es besser geworden ist.')
    b.h('8.1 | MAPPE  Vorher – nachher')
    b.table(['', 'Vorher', 'Nachher'], [
        ['Was habe ich verändert?', '', ''],
        ['Testergebnis', '', ''],
    ], [1.6, 2.5, 2.5], height=20)
    b.h('8.2 | MAPPE  Materialbilanz')
    b.table(['', 'Geplant (5.2)', 'Verbraucht', 'Verschnitt / Rest'],
            [['Dachlatte (m) oder Eisstiele (Stück)', '', '', '']], [2.4, 1.3, 1.3, 1.5], height=12)
    b.p('Hier haben wir Material gespart oder verschwendet:')
    b.lines(2)
    b.h('8.3 | MAPPE  Oberfläche')
    b.p('Unsere Oberfläche:   [  ] geölt     [  ] lasiert     [  ] furniert     [  ] unbehandelt')
    b.p('Darum haben wir uns so entschieden:')
    b.lines(2)
    b.h('8.4 | MAPPE  Was wäre, wenn wir es zehnmal bauen?')
    b.p('Wie könnte man euer Möbel zehnmal herstellen? Denkt an gleiche Längen, '
        'Schablonen, Reihenfolge und Qualitätskontrolle.')
    b.lines(3)

    # --- Teil 9 Reflexion
    page('Teil 9', 'Abnahme und Rückblick', 'Ich schätze meine Arbeit ehrlich ein.')
    b.h('9.1 | MAPPE  Meine Selbsteinschätzung')
    b.table(['Ich kann …', 'noch nicht', 'teilweise', 'sicher'], [
        ['eine eigene Möbelidee aus einem Bedarf entwickeln.', '[  ]', '[  ]', '[  ]'],
        ['eine Zeichnung mit Maßen und eine Stückliste erstellen.', '[  ]', '[  ]', '[  ]'],
        ['maßgenau und sicher fertigen.', '[  ]', '[  ]', '[  ]'],
        ['die Arbeitsgänge aus meinen Lehrgängen sicher anwenden.', '[  ]', '[  ]', '[  ]'],
        ['mein Möbel mit eigenen Kriterien prüfen.', '[  ]', '[  ]', '[  ]'],
        ['eine Schwachstelle verbessern und das begründen.', '[  ]', '[  ]', '[  ]'],
        ['sparsam mit Material umgehen.', '[  ]', '[  ]', '[  ]'],
        ['im Team Verantwortung übernehmen (falls Team).', '[  ]', '[  ]', '[  ]'],
    ], [4, 0.9, 0.9, 0.9], height=8)
    b.h('9.2 | MAPPE  Rückblick')
    for q, n in [('Diese Entscheidung habe ich selbst getroffen:', 2),
                 ('Darauf bin ich stolz:', 1),
                 ('Das würde ich beim nächsten Mal anders machen:', 2)]:
        b.p(q)
        b.lines(n)
    b.h('9.3 | Feedback')
    b.table(['Von meinem Team', 'Von der Lehrkraft'], [['', '']], [1, 1], height=48)

    path = OUT / 'projektbogen.docx'
    D.save(path)
    return path


# ========================================================= Buchungsliste
def build_buchungsliste():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Buchungsliste Lehrgänge', landscape=True)
    b = Builder(D, width=257)
    kurz = {'alle': 'für alle', 'O': 'Original', 'M': 'Modell'}
    seiten = [('Lehrgänge für alle und Weg O (Original)', ('alle', 'O'), 2),
              ('Lehrgänge Weg M (Modell)', ('M',), 3)]
    for i, (titel, gruppen, termine) in enumerate(seiten):
        if i:
            b.brk()
        b.h1(f'Buchungsliste · {titel}')
        z = b.p('Trage deinen Namen spätestens eine Stunde vorher ein. Höchstens 4 Personen pro Termin. '
                'PFLICHT = Maschine: erst nach dem Lehrgang benutzen.', size=10)
        rows = []
        for c, n, g, pf, inh, nw in LEHRGAENGE:
            if g not in gruppen:
                continue
            for k in range(termine):
                label = f'{c}  {n} · {kurz[g]}' + (' · PFLICHT' if pf else '') if k == 0 else ''
                rows.append([label, '', '', '', '', '', ''])
        t = b.table(['Lehrgang', 'Termin', 'Platz 1', 'Platz 2', 'Platz 3', 'Platz 4', 'erledigt'],
                    rows, [2.6, 1.2, 2, 2, 2, 2, 1], height=9 if termine == 2 else 10, size=8.5, pad=1.5)
        b.bold_cells(t)
        if 'M' in gruppen:
            b.h('Eigener Lehrgangswunsch')
            b.table(['Arbeitsgang', 'Wer wünscht ihn?', 'Warum?', 'Termin', 'erledigt'],
                    [['', '', '', '', ''] for _ in range(3)], [2.2, 2.4, 3.6, 1.2, 1], height=9, size=9)
    path = OUT / 'lehrgang-buchungsliste.docx'
    D.save(path)
    return path


if __name__ == '__main__':
    for path in [build_uebersicht(), build_bogen(), build_buchungsliste()]:
        to_pdf(path)
        print('erstellt:', path.relative_to(ROOT), '+ PDF')
