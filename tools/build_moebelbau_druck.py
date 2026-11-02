"""Druckmaterial Möbelwerkstatt: Projektübersicht, Werkstattheft, Erwartungshorizont,
Buchungsliste (DOCX + PDF).

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
        self.line_h = 23

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

    def lines(self, n=2, h=None):
        for _ in range(n):
            z = self.p()
            pf = z.paragraph_format
            pf.space_after = pf.space_before = Pt(0)
            pf.line_spacing = Pt(h or self.line_h)
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
    ('L5', 'Tellerschleifer', 'O', True,
     'nur auf der Tellerseite schleifen, die nach unten dreht; Werkstück auf dem Auflagetisch '
     'führen, Winkelanschlag nutzen, keine kleinen Teile freihändig, Absaugung, Schutzbrille',
     'Lattenende rechtwinklig bis zum Anriss geschliffen'),
    ('L6', 'Standbohrmaschine', 'O', True,
     'Werkstück im Maschinenschraubstock spannen – nie mit der Hand halten; Futterschlüssel '
     'abziehen, Drehzahl und Tiefenanschlag einstellen, keine Handschuhe, Haare zusammen. '
     'Entfällt mit Bohrmaschinen-Führerschein aus Klasse 5',
     'senkrechte Bohrung auf Anriss mit eingestellter Tiefe'),
    ('L7', 'Akkuschrauber', 'O', True,
     'Bohrer und Bit einsetzen, Drehrichtung und Drehmoment einstellen, Werkstück einspannen',
     'Loch gerade vorgebohrt, Schraube bündig eingedreht'),
    ('L8', 'Leimen', 'O', False,
     'Leim dünn auftragen, Zwingen mit Zulagen ansetzen, Winkel prüfen, Leimreste feucht abwischen',
     'rechtwinklige Leimverbindung'),
    ('L9', 'Verschrauben', 'O', False,
     'anreißen, Randabstand beachten, vorbohren, senken, passende Schraubenlänge wählen '
     '(vorher L7)',
     'Lattenecke ohne Riss verschraubt'),
    ('L10', 'Holzdübel', 'O', False,
     'Bohrstellen mit Dübelmarker übertragen, Bohrtiefe begrenzen, Dübel mit Leim einsetzen, '
     'pressen (vorher L6 oder L7, dazu L8)',
     'bündige Dübelverbindung'),
    ('L11', 'Dekupiersäge', 'M', True,
     'Niederhalter einstellen, Blatt prüfen, Finger seitlich vom Blatt, langsam vorschieben, '
     'Schutzbrille, lange Haare zusammenbinden',
     'Kurve sauber nach Anriss aus einer Platte gesägt'),
    ('L12', 'Platten durch Kreuzverleimung', 'M', False,
     'Eisstiele in Lagen quer zueinander verleimen, pressen, trocknen lassen; '
     'verstehen, warum Kreuzlagen stabiler sind',
     'ebene, zweilagige Platte; du erklärst das Prinzip'),
    ('L13', 'Furnier aufbringen', 'M', False,
     'Furnier mit Cutter am Stahllineal zuschneiden, Faserrichtung wählen, dünn leimen, pressen, '
     'Überstand bündig schleifen',
     'furniertes Probestück ohne Blasen'),
]
PFLICHT_TXT = ('Stichsäge, Handschleifgerät, Tellerschleifer, Standbohrmaschine, Akkuschrauber '
               'und Dekupiersäge')


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
    b.p('Ihr arbeitet allein, zu zweit oder zu dritt. Mehr als drei Personen hat ein Team nicht. '
        'Ausnahme: Im Großprojekt (Seite 4) arbeiten mehrere Teams zusammen. '
        'Je größer das Team, desto größer darf das Projekt sein.', size=10.5)
    t = b.table(TEAM[0], TEAM[1:], [0.9, 1.7, 1.9, 2.1], size=9.5)
    b.bold_cells(t)
    b.p('Größer heißt: mehr Bauteile, mehr Baugruppen, mehr Planung. Größer heißt nicht: höher oder '
        'stärker belastbar. Die Sicherheitsregeln gelten für alle.', size=10)

    b.brk()
    b.h1('Dein Projektweg')
    plan = [
        ['1', 'Ideen finden: Bedarf entdecken, mindestens drei eigene Ideen skizzieren, Team bilden',
         'Werkstattheft 1A–1B'],
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
    b.p('So buchst du: Im Werkstattheft (2C) planst du, welche Lehrgänge du brauchst, und kreuzt sie '
        'im Werkstattpass an. Dann trägst du dich auf der Buchungsliste ein – spätestens eine Stunde '
        'vorher. Am Ende zeigst du dein Probestück, die Lehrkraft unterschreibt. Lehrgänge des anderen '
        'Wegs darfst du auch buchen. Dir fehlt ein Arbeitsgang? Schlage einen eigenen Lehrgang vor.',
        size=9.5)
    for key, label in GRUPPEN:
        b.h3(label)
        rows = [[lehrgang_name(c, n, pf), inh, nw] for c, n, g, pf, inh, nw in LEHRGAENGE if g == key]
        t = b.table(['Lehrgang', 'Das lernst du', 'Das zeigst du am Ende'], rows,
                    [1.5, 3.6, 1.9], size=8.5, pad=1.5)
        b.bold_cells(t)

    # --- Großprojekt
    b.brk()
    b.p('GROSSPROJEKT · FÜR MEHR ALS DREI PERSONEN', 'Subtitle')
    b.h1('Ein Taschenregal für den Technikraum A3')
    b.p('Im Technikraum A3 liegen Rucksäcke auf dem Boden und im Weg. Gesucht wird ein Regal mit '
        '20 Ablagefächern für Rucksäcke. Das schafft kein Team allein – hier arbeiten mehrere '
        'Teams wie in einem echten Betrieb zusammen.', size=10.5)
    b.note('SO IST ES GEDACHT', 'Jedes Teilteam hat weiterhin höchstens drei Personen. Mehrere '
           'Teilteams bilden zusammen das Großprojekt. Die Lehrkraft ist eure Kundin bzw. euer '
           'Kunde. Das Großprojekt ist ein Vorschlag: Ihr entscheidet, ob ihr es übernehmt.')
    b.h('Das wünscht sich die Kundschaft (Lastenheft)')
    for s_ in ['20 Fächer; in jedes Fach passt ein Schulrucksack.',
               'Höchstens etwa 1,20 m hoch, damit alle gut hineinsehen und das Regal sicher steht.',
               'Standsicher: Die Module werden miteinander verbunden. Die Wandbefestigung übernimmt '
               'die Lehrkraft oder der Hausmeister.',
               'Gebaut aus Dachlatten. Platten nur nach Absprache.',
               'Glatte Kanten, keine Splitter, Oberfläche geölt oder lasiert.',
               'Etwas Abstand zum Boden, damit man darunter reinigen kann.']:
        z = b.p('• ' + s_, size=10)
        z.paragraph_format.space_after = Pt(2)
    b.h('Vorschlag für die Teilteams')
    t = b.table(['Teilteam', 'Aufgabe'], [
        ['Planung (1 Team)', 'Wand in A3 vermessen, Rucksäcke der Klasse messen und wiegen, '
                            'Maßraster festlegen, Gesamtzeichnung und Materialliste'],
        ['Modulbau (3–5 Teams)', 'je ein gleiches Modul nach Maßraster bauen, '
                                 'z. B. 5 Module mit je 2 × 2 Fächern nebeneinander'],
        ['Qualität (1 Team)', 'Schablonen und Prüflehren bauen, jedes Modul nach Maß prüfen, '
                              'Module verbinden, Abnahme vorbereiten'],
    ], [1.6, 5], size=9.5)
    b.bold_cells(t)
    b.p('Die Aufteilung ist ein Vorschlag. Ihr könnt sie ändern, wenn ihr es begründet – '
        'z. B. andere Modulgrößen, wenn die Wand es verlangt.', size=10)
    b.h('Darauf kommt es besonders an')
    for s_ in ['Ein gemeinsames Maßraster: Alle Module müssen ohne Nacharbeit zusammenpassen.',
               'Serienfertigung: gleiche Teile mit Schablone und Anschlag zuschneiden.',
               'Absprachen: Ein kurzes Teamtreffen zu Beginn jeder Mittwochsstunde. '
               'Ein Projektplan hängt im Raum.',
               'Last: Wiegt eure Rucksäcke. Plant mit dem schwersten, nicht mit dem leichtesten.']:
        z = b.p('• ' + s_, size=10)
        z.paragraph_format.space_after = Pt(2)
    b.note('HALTEPUNKT', 'Das Großprojekt braucht eine eigene Freigabe der Lehrkraft für die '
           'Gesamtplanung – vor dem ersten Zuschnitt. Jede Person führt ihr eigenes Werkstattheft.')
    path = OUT / 'projektuebersicht.docx'
    D.save(path)
    return path


# ============================================================== Werkstattheft
# Arbeitseinheiten: (Nr., Woche, Tag, Minuten, Input/Schwerpunkt, Arbeitsseiten)
EINHEITEN = [
    (1, 1, 'Montag', 45, 'Projektstart: Galerie, Sicherheit, Modell oder Original?', 'Start, 1A'),
    (2, 1, 'Mittwoch', 90, 'Bedarf entdecken, Ideen skizzieren, Team bilden, entscheiden', '1A, 1B'),
    (3, 2, 'Montag', 45, 'Maße, Maßstab und Holzquerschnitt klären', '2A, 2B'),
    (4, 2, 'Mittwoch', 90, 'Zeichnung, Stückliste, Lehrgänge buchen, Freigabe', '2B, 2C, 2D'),
    (5, 3, 'Montag', 45, 'Reihenfolge der Baugruppen, Arbeitsplatz vorbereiten', '2C, Werkstattpass'),
    (6, 3, 'Mittwoch', 90, 'Bauen I: Lehrgänge, Bauteile herstellen, erste Verbindungen', 'Werkstattpass'),
    (7, 4, 'Montag', 45, 'Zwischencheck: Liege ich im Plan?', '4A'),
    (8, 4, 'Mittwoch', 90, 'Bauen II: montieren, aussteifen, schleifen', '–'),
    (9, 5, 'Montag', 45, 'Prüfkriterien und sichere Prüfanordnung festlegen', '5A'),
    (10, 5, 'Mittwoch', 90, 'Erster Funktionstest, Schwachstelle finden', '5A'),
    (11, 6, 'Montag', 45, 'Verbessern, Oberfläche ölen oder lasieren, Bilanz', '6A'),
    (12, 6, 'Mittwoch', 90, 'Abnahme, kurze Vorstellung, Rückblick', '6B, Bewertung'),
]

# Bewertung: (Code, Kriterium, max. Punkte, Beschreibung für Lernende)
BEWERTUNG_A = [
    ('A1', 'Bedarf, Ideen und Entscheidung', 6,
     'echter Bedarf, mindestens drei Ideen, Entscheidung begründet'),
    ('A2', 'Konstruktionszeichnung', 6, 'vollständig, alle wichtigen Maße, Baugruppen erkennbar'),
    ('A3', 'Stückliste, Materialbedarf, Arbeitsplan', 4, 'passt zur Zeichnung, realistisch'),
    ('A4', 'Stundenprotokolle P1–P12', 12,
     'konkrete Ziele, Durchführung festgehalten, ehrliche Reflexion mit nächstem Schritt'),
    ('A5', 'Funktionstest und Verbesserung', 6, 'Ergebnisse, Schwachstelle, Vorher-nachher'),
    ('A6', 'Materialbilanz und Rückblick', 4, 'Verbrauch ausgewertet, eigene Entscheidungen erklärt'),
    ('A7', 'Eigenständigkeit', 2, 'eigene Idee, gewähltes Niveau, Hilfen gezielt genutzt'),
]
BEWERTUNG_B = [
    ('B1', 'Funktion', 15, 'erfüllt deine eigenen Prüfkriterien (nach der Verbesserung)'),
    ('B2', 'Maßhaltigkeit', 10, 'entspricht deiner Zeichnung'),
    ('B3', 'Verbindungen', 12, 'fest, sauber und fachgerecht ausgeführt'),
    ('B4', 'Oberfläche und Kanten', 8, 'geschliffen, Kanten gebrochen, behandelt'),
    ('B5', 'Stabilität und Sicherheit', 8, 'steht sicher, kippt und wackelt nicht'),
    ('B6', 'Arbeitsweise in der Werkstatt', 7, 'sicher, sauber, Lehrgänge und Regeln beachtet'),
]


def build_werkstattheft():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Werkstattheft')
    b = Builder(D)

    def page(code, title, goal=None):
        b.brk()
        b.h1(f'{code}  |  {title}')
        if goal:
            b.p(goal, bold_lead='Lernziel: ')

    def phase(nr, word, sub):
        z = b.p(sub, bold_lead=f'{nr}  {word}   ', size=10)
        z.runs[0].font.size = Pt(12)
        z.runs[-1].font.color.rgb = RGBColor.from_string('666666')
        pf = z.paragraph_format
        pf.space_before = Pt(6); pf.space_after = Pt(2); pf.left_indent = Mm(3)
        b._border(z, ['left'], INK, '24')
        return z

    def field(label, n=1, size=10):
        b.p(label, size=size).paragraph_format.space_after = Pt(0)
        b.lines(n)

    # ---------------------------------------------------------- Deckblatt
    b.p('MEIN WERKSTATTHEFT', 'Subtitle')
    D.add_paragraph('Möbelwerkstatt', 'Title')
    b.p('WP Technik 7 · Alles aus Dachlatte · Modell oder Original')
    b.p('Name: ___________________________________   Klasse: __________')
    b.p('Mein Team: ______________________________________________________')
    b.h('So arbeitest du in jeder Stunde')
    t = b.table(['1  PLANEN', '2  DURCHFÜHREN', '3  REFLEKTIEREN'], [[
        'Zu Beginn: Ich schreibe auf, was ich mir für heute vornehme und woran ich merke, '
        'dass ich es geschafft habe.',
        'Während der Arbeit: Ich arbeite meine Schritte ab, halte fest, was ich geschafft habe '
        'und wie ich Probleme gelöst habe.',
        'Am Ende: Ich prüfe, ob ich mein Ziel erreicht habe, und lege meinen nächsten Schritt fest.']],
        [1, 1, 1], size=10)
    b.p('Dafür gibt es für jede Stunde ein Stundenprotokoll (P1 bis P12). '
        'Dazwischen liegen die Arbeitsseiten für dein Projekt (1A bis 6B).', size=10)
    b.h('Dein Heft ist deine Lernerfolgskontrolle')
    b.note('WICHTIG', 'Dieses Werkstattheft ist zusammen mit deinem Werkstück die zweite '
           'Klassenarbeit. Das Heft zählt 40 %, das Werkstück 60 %. Die Kriterien findest du '
           'auf der letzten Seite – lies sie schon jetzt.')
    for s_ in ['Jede Person führt ein eigenes Heft – auch im Team. Teamentscheidungen schreibt ihr alle auf, '
               'Protokolle und Reflexion schreibst du allein.',
               'Schreibe ehrlich. Ein Ziel, das du nicht erreicht hast, ist kein Fehler – '
               'wenn du erklärst, was du daraus machst.',
               'Das Heft bleibt im Technikraum. Fotos vom Arbeitsstand darfst du einkleben.']:
        z = b.p('• ' + s_, size=10)
        z.paragraph_format.space_after = Pt(2)
    b.h('Hier findest du Hilfe')
    b.p('Erst selbst probieren → Hilfekarte H1–H8 im Lernnavigator → Team → Lehrkraft. '
        'Arbeitsgänge lernst du in Lehrgängen (Werkstattpass).', size=10)

    # ---------------------------------------------------------- Überblick
    page('Start', 'Mein Projekt auf einen Blick', 'Ich behalte mein ganzes Projekt im Blick.')
    b.p('Fülle den oberen Teil aus, sobald du dich entschieden hast (Woche 1).', size=10)
    b.table(None, [
        ['Ich baue:', ''], ['für (Person / Ort):', ''],
        ['Materialweg:', '[  ] Weg M – Modell aus Eisstielen     [  ] Weg O – Original aus Dachlatte'],
        ['Teamgröße:', '[  ] allein   [  ] zu zweit   [  ] zu dritt   [  ] Teilteam im Großprojekt'],
        ['Mein Startniveau:', '[  ] 1 Anwenden   [  ] 2 Konstruieren   [  ] 3 Optimieren'],
        ['Meine Baugruppe:', ''],
    ], [1.3, 5], height=9, size=10)
    b.h('Mein Zeitplan')
    b.p('Plane in Woche 1 grob, was du in jeder Woche schaffen willst. Kreuze am Ende jeder Woche an, '
        'wo du stehst. So merkst du früh, ob du deinen Plan ändern musst.', size=10)
    b.table(['Woche', 'Das will ich schaffen', 'Das habe ich geschafft', 'im Plan?'],
            [[str(w), '', '', '[  ] ja\n[  ] knapp\n[  ] nein'] for w in range(1, 7)],
            [0.6, 2.6, 2.6, 1], height=17, size=9.5, pad=1.5)
    b.h('Meilensteine')
    b.table(['Haltepunkt', 'Seite', 'Datum', 'Kürzel Lehrkraft'], [
        ['Entscheidung steht', '1B', '', ''], ['Freigabe der Planung', '2D', '', ''],
        ['Funktionstest', '5A', '', ''], ['Abnahme', '6B', '', '']],
        [2.6, 0.8, 1.3, 1.6], height=8, size=10, pad=1.5)

    # ---------------------------------------------------------- Werkstattpass
    page('Werkstattpass', 'Meine Lehrgänge', 'Ich lerne Arbeitsgänge, bevor ich sie brauche.')
    b.note('PFLICHT', f'{PFLICHT_TXT}: Du benutzt sie erst, wenn hier die Unterschrift '
                      'der Lehrkraft steht.')
    b.p('Kreuze an, was du brauchst. Buche einen Termin auf der Buchungsliste. '
        'Nach dem Lehrgang zeigst du dein Probestück, die Lehrkraft trägt Datum und Kürzel ein.',
        size=10)
    for key, label in GRUPPEN:
        b.h3(label)
        rows = [[f'{c}  {n}' + (' · PFLICHT' if pf else ''), '[  ]', '', '', '']
                for c, n, g, pf, inh, nw in LEHRGAENGE if g == key]
        t = b.table(['Lehrgang', 'brauche ich', 'gebucht für', 'bestanden am', 'Kürzel Lehrkraft'],
                    rows, [3, 0.9, 1.2, 1.2, 1.2], height=8, size=9, pad=1.5)
        b.bold_cells(t)
    b.h3('Mein eigener Lehrgangswunsch')
    b.table(['Arbeitsgang', 'Warum brauche ich ihn?', 'bestanden am', 'Kürzel Lehrkraft'],
            [['', '', '', ''] for _ in range(2)], [2, 2.9, 1.3, 1.3], height=8, size=9, pad=1.5)

    # ---------------------------------------------------------- Stundenprotokoll
    def protokoll(nr, woche, tag, minuten, inhalt, seiten):
        b.line_h = 21
        b.brk()
        b.h1(f'P{nr}  |  Stundenprotokoll')
        b.p(f'Woche {woche} · {tag} · {minuten} Minuten        Datum: ______________', size=10.5)
        z = b.p(f'Heute: {inhalt}  ·  Arbeitsseiten: {seiten}', size=10)
        z.runs[0].bold = True
        phase('1', 'PLANEN', 'zu Beginn der Stunde')
        if nr > 1:
            b.p('Das habe ich mir letzte Stunde als nächsten Schritt vorgenommen:', size=10)
            b.lines(1)
        b.p('Mein Ziel für heute – am Ende der Stunde habe ich …', size=10)
        b.lines(2)
        b.table(['Meine Schritte heute', 'erledigt?'],
                [['1.', '[  ] ja  [  ] teils  [  ] nein'], ['2.', '[  ] ja  [  ] teils  [  ] nein'],
                 ['3.', '[  ] ja  [  ] teils  [  ] nein']], [4.3, 2.2], height=7.5, size=9.5, pad=1.5)
        b.p('Das brauche ich (Material, Werkzeug, Lehrgang L__): _____________________________', size=10)
        b.p('Daran erkenne ich, dass ich mein Ziel erreicht habe:', size=10)
        b.lines(1)
        phase('2', 'DURCHFÜHREN', 'während der Arbeit')
        b.p('Das habe ich geschafft:', size=10)
        b.lines(2)
        b.p('Problem und meine Lösung – oder: Das mache ich nächstes Mal anders:', size=10)
        b.lines(2)
        b.p('Hilfe genutzt:   [  ] Hilfekarte H___   [  ] Team   [  ] Lehrkraft   [  ] keine nötig',
            size=10)
        phase('3', 'REFLEKTIEREN', 'am Ende der Stunde')
        b.table(['', 'noch nicht', 'teilweise', 'gut', 'sehr gut'], [
            ['Ich habe mein Ziel erreicht.', '[  ]', '[  ]', '[  ]', '[  ]'],
            ['Ich habe konzentriert gearbeitet.', '[  ]', '[  ]', '[  ]', '[  ]'],
            ['Ich habe sicher und ordentlich gearbeitet.', '[  ]', '[  ]', '[  ]', '[  ]'],
            ['Im Team lief es gut. (nur bei Teamarbeit)', '[  ]', '[  ]', '[  ]', '[  ]'],
        ], [3.6, 0.9, 0.9, 0.7, 0.8], size=9.5, pad=1.5)
        b.p('Mein nächster Schritt (schreibe ihn nächstes Mal oben ab):', size=10)
        b.lines(1)
        b.line_h = 23

    E = {e[0]: e for e in EINHEITEN}

    # ---------------------------------------------------------- Woche 1
    protokoll(*E[1])
    page('1A', 'Bedarf entdecken und Ideen finden', 'Ich finde eine echte Aufgabe für ein Möbelstück.')
    b.p('Schau dich um: in deinem Zimmer, im Klassenraum, im Werkraum, bei Familie oder Freunden. '
        'Was liegt herum? Was ist unpraktisch? Wem könntest du helfen?', size=10.5)
    b.table(['Ort', 'Das Problem', 'Wer hätte etwas davon?'],
            [['', '', ''] for _ in range(3)], [1.3, 3, 2], height=12)
    b.h('Meine drei Ideen')
    b.p('Skizziere mindestens drei unterschiedliche Ideen. Schnelle Skizzen reichen. '
        'Mindestens eine Idee ist ganz von dir – nicht aus dem Ideenspeicher.', size=10.5)
    b.table(['Idee 1: ____________', 'Idee 2: ____________', 'Idee 3: ____________'],
            [['', '', '']], [1, 1, 1], height=95)
    b.note('HILFE', 'Kein Einfall? Frage dich: Was nervt mich jeden Tag? '
                    'Erst dann: Ideenspeicher in der Projektübersicht.')

    page('1B', 'Entscheiden', 'Ich treffe eine begründete Entscheidung.')
    b.p('Bewerte jede Idee: ++ sehr gut · + gut · – eher nicht. Ergänze ein eigenes Kriterium.', size=10.5)
    b.table(['Kriterium', 'Idee 1', 'Idee 2', 'Idee 3'], [
        ['löst ein echtes Problem', '', '', ''], ['in 6 Wochen schaffbar', '', '', ''],
        ['passt zu unserer Teamgröße', '', '', ''], ['sicher baubar', '', '', ''],
        ['neu oder eigen', '', '', ''], ['eigenes Kriterium: ____________', '', '', ''],
    ], [3, 1, 1, 1], height=8.5)
    b.p('Wir bauen: __________________________________________________________', size=10.5)
    b.p('Darum haben wir uns so entschieden:', size=10.5)
    b.lines(3)
    b.p('Das ist an unserer Idee neu oder eigen:', size=10.5)
    b.lines(2)
    b.p('Übertrage deine Entscheidung auf die Seite „Mein Projekt auf einen Blick“.', size=10)
    b.note('HALTEPUNKT', 'Zeige deine Entscheidung der Lehrkraft. Passt der Umfang zur Teamgröße? '
                         '(Tabelle in der Projektübersicht)')
    b.p('Entscheidung besprochen am: ____________   Kürzel Lehrkraft: ____________', size=10)
    protokoll(*E[2])

    # ---------------------------------------------------------- Woche 2
    protokoll(*E[3])
    page('2A', 'Anforderungen, Prüfkriterien, Team', 'Ich lege fest, was mein Möbel können muss.')
    b.h('Was muss unser Möbel können?')
    b.table(['Muss es können', 'Wäre schön'], [['', ''] for _ in range(3)], [1, 1], height=9)
    b.h('Unsere Prüfkriterien')
    b.p('Mindestens zwei Kriterien, die man mit ja oder nein prüfen kann. '
        'Beispiel: „Der Ständer hält ein Buch mit 1 kg, ohne zu kippen.“', size=10)
    b.table(['Nr.', 'Prüfkriterium', 'So prüfen wir es'],
            [['1', '', ''], ['2', '', ''], ['3', '', '']], [0.5, 3.2, 2.8], height=11)
    b.h('Teamvertrag')
    b.p('Bei Einzelarbeit: nur deine Hauptbaugruppen eintragen. Im Großprojekt: euer Teilteam und '
        'eure Aufgabe.', size=10)
    b.table(['Name', 'Ich bin verantwortlich für (Baugruppe / Möbelteil)', 'Unterschrift'],
            [['', '', ''] for _ in range(3)], [1.6, 3.4, 1.5], height=10)
    b.p('Unsere Regeln: Wenn wir uns nicht einig sind, machen wir es so:', size=10)
    b.lines(2)

    page('2B', 'Konstruktionszeichnung', 'Ich zeichne mein Möbel maßhaltig.')
    b.p('Zeichne dein Möbel in einer Ansicht oder schräg von vorn. Trage alle wichtigen Maße in mm ein. '
        'Markiere die Baugruppen und wer sie baut.', size=10.5)
    b.box(None, 360)
    b.p('Gesamtmaße (B × T × H): ______ × ______ × ______ mm      Nur Weg M – Maßstab: 1 : ______',
        size=10.5)
    b.note('HILFE', 'H1 Von der Idee zur Zeichnung · H2 Maßstab umrechnen')

    page('2C', 'Stückliste, Arbeitsplan, Lehrgänge', 'Ich plane Material, Schritte und Lehrgänge.')
    b.h('Stückliste')
    b.table(['Nr.', 'Bauteil', 'Anzahl', 'Länge (mm)', 'Material', 'Wer?'],
            [[str(i), '', '', '', '', ''] for i in range(1, 9)],
            [0.5, 2.4, 0.8, 1.2, 1.6, 1.1], height=7, size=9.5, pad=1.5)
    b.p('Weg O: Dachlatte gesamt ______ m (+ ca. 10 % Verschnitt = ______ m)      '
        'Weg M: Eisstiele ______ Stück', size=10)
    b.p('Verbindungen (z. B. leimen, schrauben, dübeln): ____________________________________', size=10)
    b.h('Reihenfolge der Arbeitsschritte')
    b.table(['Schritt', 'Was wird gemacht?', 'Werkzeug / Maschine', 'Lehrgang', 'Wer?'],
            [[str(i), '', '', 'L___', ''] for i in range(1, 7)], [0.6, 3, 1.6, 0.9, 0.9],
            height=7.5, size=9.5, pad=1.5)
    b.p('Kreuze die nötigen Lehrgänge im Werkstattpass an und trage dich auf der Buchungsliste ein.',
        size=10)
    b.note('HILFE', 'H3 Dachlatten prüfen · H4 Verbindungen · H7 Zuschnitt und Kosten · '
                    'Lehrgänge: Projektübersicht Seite 3')

    page('2D', 'Freigabe', 'Ich prüfe meine Planung, bevor ich säge.')
    b.note('HALTEPUNKT', 'Zeige deine Planung der Lehrkraft. Erst nach der Freigabe schneidest du '
                         'Material zu.')
    b.table(['Prüfpunkt', 'Ich', 'Lehrkraft'], [
        ['Das Möbel löst ein echtes Problem (1A, 1B).', '[  ]', '[  ]'],
        ['Der Umfang passt zur Teamgröße.', '[  ]', '[  ]'],
        ['Die Zeichnung hat alle wichtigen Maße (2B).', '[  ]', '[  ]'],
        ['Stückliste und Zeichnung passen zusammen (2C).', '[  ]', '[  ]'],
        ['Es gibt mindestens zwei prüfbare Prüfkriterien (2A).', '[  ]', '[  ]'],
        ['Jede Person hat eine eigene Baugruppe.', '[  ]', '[  ]'],
        ['Nötige Lehrgänge sind angekreuzt und gebucht.', '[  ]', '[  ]'],
        ['Kein Sitzmöbel, kein hohes Regal in Originalgröße.', '[  ]', '[  ]'],
    ], [5, 0.8, 1.1], height=8)
    b.h('Rückmeldung der Lehrkraft')
    b.p('Materialrahmen: _______________________________________________________', size=10.5)
    b.p('Bitte noch ändern:', size=10.5)
    b.lines(4)
    b.p('[  ] Freigegeben      Datum: ______________      Kürzel: ______________', size=10.5)
    protokoll(*E[4])

    # ---------------------------------------------------------- Woche 3 und 4
    protokoll(*E[5])
    protokoll(*E[6])
    protokoll(*E[7])
    page('4A', 'Zwischencheck', 'Ich überprüfe meinen Plan und passe ihn an.')
    b.p('Halbzeit beim Bauen. Vergleiche mit deinem Zeitplan auf der Seite „Mein Projekt auf einen Blick“.',
        size=10.5)
    b.table(['Frage', 'Meine Antwort'], [
        ['Wo stehe ich? Was ist schon fertig?', ''],
        ['Was fehlt noch bis zum Test in Woche 5?', ''],
        ['Liege ich im Plan?', '[  ] ja     [  ] knapp     [  ] nein'],
        ['Was kann ich vereinfachen oder weglassen, ohne dass die Funktion leidet?', ''],
        ['Welche Hilfe oder welchen Lehrgang brauche ich noch?', ''],
    ], [2.4, 4], height=20, size=10)
    b.h('Mein angepasster Plan bis zum Test')
    b.table(['Stunde', 'Das erledige ich'], [['Woche 4 · Mittwoch', ''], ['Woche 5 · Montag', '']],
            [1.6, 4.8], height=14, size=10)
    b.p('Zwischencheck besprochen mit: ______________   Kürzel Lehrkraft: ______________', size=10)
    protokoll(*E[8])

    # ---------------------------------------------------------- Woche 5
    protokoll(*E[9])
    page('5A', 'Funktionstest', 'Ich prüfe mein Möbel ehrlich und finde Schwachstellen.')
    b.note('HALTEPUNKT', 'Plant den Test mit der Lehrkraft. Testet nur mit der vereinbarten Last.')
    b.p('Vereinbarte Prüflast / Prüfanordnung: ______________________________________', size=10.5)
    b.table(['Prüfkriterium (aus 2A)', 'Ergebnis', 'Erfüllt?'],
            [['', '', 'ja / teils / nein'] for _ in range(3)], [3, 2.6, 1.2], height=13)
    b.h('Schwachstelle')
    field('Diese Stelle hat nicht gut funktioniert:', 2, 10.5)
    field('Ich vermute als Ursache:', 2, 10.5)
    b.box('Meine Verbesserungsidee (Skizze)', 150)
    b.note('HILFE', 'H5 Aussteifen · H6 Kippen und Prüfen · H8 Verbessern mit Test')
    protokoll(*E[10])

    # ---------------------------------------------------------- Woche 6
    protokoll(*E[11])
    page('6A', 'Verbessern, Oberfläche, Bilanz', 'Ich zeige mit einem Test, dass es besser geworden ist.')
    b.h('Vorher – nachher')
    b.table(['', 'Vorher', 'Nachher'], [['Was habe ich verändert?', '', ''], ['Testergebnis', '', '']],
            [1.6, 2.5, 2.5], height=18)
    b.h('Oberfläche')
    b.p('[  ] geölt     [  ] lasiert     [  ] furniert     [  ] unbehandelt,  weil ____________________',
        size=10.5)
    b.h('Materialbilanz')
    b.table(['', 'Geplant (2C)', 'Verbraucht', 'Rest / Verschnitt'],
            [['Dachlatte (m) oder Eisstiele (Stück)', '', '', '']], [2.4, 1.3, 1.3, 1.5], height=11)
    field('Hier habe ich Material gespart oder verschwendet:', 2, 10.5)
    b.h('Was wäre, wenn wir es zehnmal bauen?')
    field('Wie könnte man euer Möbel zehnmal herstellen? Denkt an gleiche Längen, Schablonen, '
          'Reihenfolge und Qualitätskontrolle.', 3, 10.5)

    page('6B', 'Abnahme und Rückblick', 'Ich schätze meine Arbeit ehrlich ein.')
    b.note('HALTEPUNKT', 'Abnahme: Du stellst dein Werkstück in 2–3 Minuten vor und erklärst eine '
                         'Entscheidung, auf die du stolz bist.')
    b.table(['Ich kann …', 'noch nicht', 'teilweise', 'sicher'], [
        ['eine eigene Möbelidee aus einem Bedarf entwickeln.', '[  ]', '[  ]', '[  ]'],
        ['eine Zeichnung mit Maßen und eine Stückliste erstellen.', '[  ]', '[  ]', '[  ]'],
        ['meine Stunden planen und meinen Plan anpassen.', '[  ]', '[  ]', '[  ]'],
        ['die Arbeitsgänge aus meinen Lehrgängen sicher anwenden.', '[  ]', '[  ]', '[  ]'],
        ['maßgenau und sauber fertigen.', '[  ]', '[  ]', '[  ]'],
        ['mein Möbel prüfen und eine Schwachstelle verbessern.', '[  ]', '[  ]', '[  ]'],
        ['im Team Verantwortung übernehmen (falls Team).', '[  ]', '[  ]', '[  ]'],
    ], [4, 0.9, 0.9, 0.9], height=7.5, size=9.5, pad=1.5)
    for q, n in [('Diese Entscheidung habe ich selbst getroffen:', 2), ('Darauf bin ich stolz:', 1),
                 ('Das hat mir beim Planen meiner Stunden geholfen:', 1),
                 ('Das würde ich beim nächsten Projekt anders machen:', 2)]:
        field(q, n, 10.5)
    b.table(['Feedback von meinem Team', 'Feedback der Lehrkraft'], [['', '']], [1, 1], height=34)
    protokoll(*E[12])

    # ---------------------------------------------------------- Bewertung
    page('Bewertung', 'Meine Lernerfolgskontrolle')
    b.p('Werkstattheft (Teil A, 40 Punkte) und Werkstück (Teil B, 60 Punkte) ergeben zusammen '
        '100 Punkte. Schätze dich vor der Abgabe selbst ein: ++ sicher erfüllt · + erfüllt · '
        'o teilweise · – noch nicht.', size=10)

    def bew(titel, rows):
        b.h3(titel)
        t = b.table(['', 'Kriterium', 'Daran erkennt man es', 'max.', 'Ich', 'Punkte'],
                    [[c, k, d, str(m), '', ''] for c, k, m, d in rows] + [['', 'Summe', '', str(sum(r[2] for r in rows)), '', '']],
                    [0.45, 1.7, 3.1, 0.5, 0.5, 0.7], size=9, pad=1.5)
        b.bold_cells(t, col=1)
        for c in t.rows[-1].cells:
            for q in c.paragraphs:
                for r in q.runs:
                    r.bold = True

    bew('Teil A · Werkstattheft (40 %)', BEWERTUNG_A)
    bew('Teil B · Werkstück (60 %)', BEWERTUNG_B)
    b.p('Im Team wird beim Werkstück deine eigene Baugruppe und das gemeinsame Ergebnis bewertet. '
        'Das Werkstattheft wird für jede Person einzeln bewertet.', size=9.5)
    b.p('Gesamt: ________ / 100 Punkte        Note: ____________        Datum, Kürzel: ______________',
        size=10.5)

    path = OUT / 'werkstattheft.docx'
    D.save(path)
    return path


# ===================================================== Erwartungshorizont
STUFEN = {
    'A1': ('echter, konkret beschriebener Bedarf; mind. drei verschiedene Ideen, davon eine eigene; '
           'Entscheidung mit Kriterien begründet', 'Bedarf und drei Ideen vorhanden, Begründung knapp',
           'Bedarf unklar oder weniger als drei Ideen; keine Begründung'),
    'A2': ('vollständige, saubere Zeichnung; alle für den Bau nötigen Maße; Baugruppen und ggf. Maßstab angegeben',
           'Zeichnung verständlich, einzelne Maße fehlen', 'Skizze ohne verwertbare Maße'),
    'A3': ('Stückliste vollständig und passend zur Zeichnung; Materialbedarf mit Verschnitt; sinnvolle Reihenfolge '
           'mit Lehrgängen', 'weitgehend vollständig, kleinere Widersprüche', 'lückenhaft oder passt nicht zur Zeichnung'),
    'A4': ('nahezu alle Protokolle; Ziele konkret und überprüfbar; Durchführung nachvollziehbar; Reflexion ehrlich, '
           'nächster Schritt wird in der Folgestunde aufgegriffen', 'Protokolle überwiegend vorhanden; Ziele teils '
           'allgemein („weiterbauen“)', 'viele Protokolle fehlen oder bleiben formelhaft'),
    'A5': ('Testergebnisse zu allen Prüfkriterien; Schwachstelle mit Ursache; Verbesserung mit Vorher-nachher belegt',
           'Test dokumentiert, Verbesserung beschrieben, aber nicht erneut geprüft', 'Test oder Verbesserung fehlt'),
    'A6': ('Materialbilanz ausgewertet und bewertet; Rückblick benennt eigene Entscheidungen und Konsequenzen',
           'Bilanz ausgefüllt, Rückblick allgemein', 'fehlt weitgehend'),
    'A7': ('eigene Idee umgesetzt, Niveau passend gewählt oder gesteigert, Hilfen gezielt eingesetzt',
           'teilweise eigenständig', 'überwiegend nach Vorgabe oder mit dauerhafter Anleitung'),
    'B1': ('alle eigenen Prüfkriterien erfüllt (ggf. nach Verbesserung)', 'überwiegend erfüllt',
           'Hauptfunktion nicht erfüllt'),
    'B2': ('Abweichung zur Zeichnung höchstens ca. ±2 mm (Original) bzw. ±1 mm (Modell)',
           'einzelne größere Abweichungen ohne Funktionsverlust', 'deutliche Abweichungen, Funktion beeinträchtigt'),
    'B3': ('Verbindungen fest, rechtwinklig, sauber (keine Risse, kein Leimüberschuss, Schrauben bündig)',
           'fest, aber mit sichtbaren Mängeln', 'lose oder fehlerhaft'),
    'B4': ('Flächen sauber geschliffen, Kanten gebrochen, Oberfläche gleichmäßig behandelt',
           'überwiegend sauber, einzelne Splitter/Kratzer', 'raue Flächen, scharfe Kanten'),
    'B5': ('steht sicher, wackelt und kippt nicht bei vorgesehener Nutzung', 'leichte Mängel',
           'instabil oder nicht sicher nutzbar'),
    'B6': ('arbeitet sicher und selbstständig, hält Lehrgangs- und Werkstattregeln ein, Arbeitsplatz ordentlich',
           'meist regelgerecht, gelegentliche Erinnerung nötig', 'wiederholte Regelverstöße'),
}


def build_erwartungshorizont():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Erwartungshorizont (Lehrkraft)')
    b = Builder(D)
    b.p('LEHRKRAFT · LERNERFOLGSKONTROLLE 2', 'Subtitle')
    D.add_paragraph('Erwartungshorizont Werkstattheft und Werkstück', 'Title')
    b.p('Die zweite Klassenarbeit wird durch eine Projektleistung ersetzt: Werkstattheft (Teil A, 40 Punkte) '
        'und Werkstück (Teil B, 60 Punkte). Bewertet wird nicht Größe, Traglast oder Verzierung, sondern '
        'Planung, Fertigung, Funktion, Materialeinsatz und Reflexion.', size=10.5)
    b.h('Hinweise zur Durchführung')
    for s_ in ['Jede Person führt ein eigenes Heft. Teamentscheidungen dürfen gleich lauten; Stundenprotokolle, '
               'Reflexion und Rückblick werden individuell bewertet.',
               'Werkstück im Team: Bewertet werden die eigene Baugruppe (laut Teamvertrag 2A) und das '
               'Gesamtergebnis. B6 wird individuell über die Projektzeit beobachtet.',
               'Abnahme (Woche 6): kurzes Fachgespräch (2–3 Min.) am Werkstück; das Gespräch stützt die '
               'Bewertung von A1, A7 und B1.',
               'Das gewählte Niveau fließt in A7 ein. Eine gut umgesetzte Niveau-1-Aufgabe kann trotzdem '
               'sehr gut bewertet werden.',
               'Stichproben während der Arbeit: Heft am Ende einer Stunde einsammeln oder einsehen, '
               'kurze Rückmeldung zum Ziel geben (A4).']:
        z = b.p('• ' + s_, size=10)
        z.paragraph_format.space_after = Pt(2)

    def stufen(titel, rows):
        b.h(titel)
        t = b.table(['', 'Kriterium (max.)', 'volle Punktzahl', 'etwa die Hälfte', 'wenige / keine'],
                    [[c, f'{k} ({m})', *STUFEN[c]] for c, k, m, d in rows],
                    [0.45, 1.4, 2.6, 1.8, 1.8], size=8.5, pad=1.5)
        b.bold_cells(t, col=1)

    stufen('Teil A · Werkstattheft (40 Punkte)', BEWERTUNG_A)
    stufen('Teil B · Werkstück (60 Punkte)', BEWERTUNG_B)
    b.h('Notenschlüssel (Vorschlag – an Fachschaftsbeschluss anpassen)')
    b.table(['Punkte', '100–87', '86–73', '72–59', '58–45', '44–20', '19–0'],
            [['Note', 'sehr gut', 'gut', 'befriedigend', 'ausreichend', 'mangelhaft', 'ungenügend']],
            [1, 1, 1, 1.2, 1.2, 1.2, 1.2], size=9.5)
    path = OUT / 'werkstattheft-erwartungshorizont.docx'
    D.save(path)
    return path


# ========================================================= Buchungsliste
def build_buchungsliste():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Buchungsliste Lehrgänge', landscape=True)
    b = Builder(D, width=257)
    kurz = {'alle': 'für alle', 'O': 'Original', 'M': 'Modell'}
    seiten = [('für alle und Weg O, Teil 1', ['L1', 'L2', 'L3', 'L4', 'L5', 'L6'], 2),
              ('Weg O, Teil 2', ['L7', 'L8', 'L9', 'L10'], 3),
              ('Weg M (Modell)', ['L11', 'L12', 'L13'], 3)]
    for i, (titel, codes, termine) in enumerate(seiten):
        if i:
            b.brk()
        b.h1(f'Buchungsliste Lehrgänge · {titel}')
        z = b.p('Trage deinen Namen spätestens eine Stunde vorher ein. Höchstens 4 Personen pro Termin. '
                'PFLICHT = Maschine: erst nach dem Lehrgang benutzen.', size=10)
        rows = []
        for c, n, g, pf, inh, nw in LEHRGAENGE:
            if c not in codes:
                continue
            for k in range(termine):
                label = f'{c}  {n} · {kurz[g]}' + (' · PFLICHT' if pf else '') if k == 0 else ''
                rows.append([label, '', '', '', '', '', ''])
        t = b.table(['Lehrgang', 'Termin', 'Platz 1', 'Platz 2', 'Platz 3', 'Platz 4', 'erledigt'],
                    rows, [2.6, 1.2, 2, 2, 2, 2, 1], height=9, size=8.5, pad=1.5)
        b.bold_cells(t)
        if 'L11' in codes:
            b.h('Eigener Lehrgangswunsch')
            b.table(['Arbeitsgang', 'Wer wünscht ihn?', 'Warum?', 'Termin', 'erledigt'],
                    [['', '', '', '', ''] for _ in range(3)], [2.2, 2.4, 3.6, 1.2, 1], height=9, size=9)
    path = OUT / 'lehrgang-buchungsliste.docx'
    D.save(path)
    return path


if __name__ == '__main__':
    for path in [build_uebersicht(), build_werkstattheft(), build_erwartungshorizont(),
                 build_buchungsliste()]:
        to_pdf(path)
        print('erstellt:', path.relative_to(ROOT), '+ PDF')
