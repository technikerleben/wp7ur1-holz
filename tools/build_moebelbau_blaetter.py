"""Einzelblätter Möbelwerkstatt: Ideenblatt, Protokollblatt, Ergebnisbogen (je 1 Seite, DOCX + PDF).

Akzentfarben passend zum TaskCards-Farbcode, nur als Linien (tonersparend):
Idee/Skizze = Salbeigrün, Protokoll = Schieferblau, Ergebnis = Ocker.
Aufruf: python3 tools/build_moebelbau_blaetter.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx.shared import Pt, Mm, RGBColor  # noqa: E402
from build_moebelbau_druck import new_doc, Builder, to_pdf, OUT  # noqa: E402

GREEN, BLUE, OCHRE = '4D8B3F', '3E5668', 'C17B00'


def kopf(b, farbe, marke, titel, hinweis):
    z = b.p(marke, size=10)
    z.runs[0].bold = True
    z.runs[0].font.color.rgb = RGBColor.from_string(farbe)
    z.paragraph_format.space_after = Pt(0)
    h = b.D.add_paragraph(titel, 'Heading 1')
    h.paragraph_format.space_after = Pt(4)
    b._border(h, ['bottom'], farbe, '18')
    b.p('Name: ______________________________   Datum: ______________   Woche: ____', size=10.5)
    z = b.p(hinweis, size=9)
    z.runs[0].font.color.rgb = RGBColor.from_string('666666')


def phase(b, farbe, nr, wort, sub):
    z = b.p(sub, bold_lead=f'{nr}  {wort}   ', size=10)
    z.runs[0].font.size = Pt(12)
    z.runs[-1].font.color.rgb = RGBColor.from_string('666666')
    pf = z.paragraph_format
    pf.space_before = Pt(7); pf.space_after = Pt(2); pf.left_indent = Mm(3)
    b._border(z, ['left'], farbe, '24')


def feld(b, text, n=1, size=10):
    b.p(text, size=size).paragraph_format.space_after = Pt(0)
    b.lines(n)


# ------------------------------------------------------------------ Ideenblatt
def ideenblatt():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Ideenblatt')
    b = Builder(D)
    b.line_h = 21
    kopf(b, GREEN, 'IDEE · SKIZZE', 'Meine Möbelidee Nr. ____',
         'Nutze für jede Idee ein eigenes Blatt. Danach: Foto in TaskCards als grüne Karte ✏️ SKIZZE.')
    b.table(None, [
        ['Für wen?', ''],
        ['Welches Problem löst es?', ''],
    ], [1.5, 5], height=10, size=10)
    b.h('Skizze')
    b.p('Zeichne deine Idee. Trage die wichtigsten Maße in mm ein. Gern auch eine zweite Ansicht.',
        size=9.5)
    b.box(None, 225)
    b.h('Beschreibung')
    feld(b, 'Das ist meine Idee (Was ist es? Woraus besteht es?):', 2)
    feld(b, 'Anwendung – so wird es benutzt (wo, wie, wofür?):', 2)
    feld(b, 'Das ist das Besondere oder Neue daran:', 1)
    b.table(None, [
        ['Weg:', '[  ] Modell aus Eisstielen     [  ] Original aus Dachlatte'],
        ['Material (grob):', ''],
        ['Kurzcheck:', '[  ] in 6 Wochen schaffbar    [  ] sicher baubar    [  ] passt zur Teamgröße'],
    ], [1.5, 5], height=8.5, size=10)
    path = OUT / 'ideenblatt.docx'
    D.save(path)
    return path


# --------------------------------------------------------------- Protokollblatt
def protokollblatt():
    D = new_doc('HBG  |  WP Technik 7  |  Möbelwerkstatt – Protokoll einer Werkstatteinheit')
    b = Builder(D)
    b.line_h = 21
    kopf(b, BLUE, 'PROTOKOLL', 'Meine Werkstatteinheit',
         'Ein Blatt pro Einheit. Danach: Foto in TaskCards als blaue Karte 📘 PROTOKOLL.')
    b.p('Einheit:   [  ] Montag (45 Min.)     [  ] Mittwoch (90 Min.)', size=10.5)

    phase(b, BLUE, '1', 'PLANEN', 'zu Beginn der Stunde')
    feld(b, 'Das habe ich mir letztes Mal als nächsten Schritt vorgenommen:', 1)
    feld(b, 'Mein Ziel für heute – am Ende der Stunde habe ich …', 2)
    b.table(['Meine Schritte heute', 'erledigt?'],
            [[f'{i}.', '[  ] ja  [  ] teils  [  ] nein'] for i in (1, 2, 3)],
            [4, 2.5], height=7.5, size=9.5, pad=1.5)
    b.p('Das brauche ich (Material, Werkzeug, Lehrgang L__): ______________________________', size=10)
    feld(b, 'Daran erkenne ich, dass ich mein Ziel erreicht habe:', 1)

    phase(b, BLUE, '2', 'DURCHFÜHREN', 'während der Arbeit')
    feld(b, 'Das habe ich geschafft:', 2)
    feld(b, 'Problem und meine Lösung:', 2)
    b.p('Hilfe:  [  ] Hilfekarte H___  [  ] Team  [  ] Lehrkraft  [  ] keine      '
        'Foto vom Stand:  [  ] ja  [  ] nein', size=9.5)

    phase(b, BLUE, '3', 'REFLEKTIEREN', 'am Ende der Stunde')
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
    b = Builder(D)
    b.line_h = 20
    kopf(b, OCHRE, 'ERGEBNIS · SELBSTBEWERTUNG', 'Mein fertiges Projekt',
         'Ergänzt die Fotos deines fertigen Werkstücks. Danach: in TaskCards als gelbe Karte ⭐ PROJEKT.')
    b.table(None, [
        ['Mein Werkstück:', ''],
        ['Weg / Team:', '[  ] Modell   [  ] Original      [  ] allein   [  ] mit: ____________________'],
    ], [1.5, 5], height=8, size=10)
    b.p('Meine Fotos in TaskCards:   [  ] von vorn   [  ] von der Seite   [  ] Detail einer Verbindung   '
        '[  ] im Einsatz', size=9.5)

    b.h('Mein Test')
    b.table(['Mein Prüfkriterium', 'Ergebnis', 'erfüllt?'],
            [['', '', '[  ] ja  [  ] teils  [  ] nein'] for _ in range(2)],
            [2.8, 2, 2.1], height=10, size=9.5, pad=1.5)

    b.h('So schätze ich mein Werkstück ein')
    b.p('++ sehr gut gelungen · + gelungen · o teilweise · – noch nicht gelungen', size=9.5)
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
                [1.35, 2.3, 0.35, 0.35, 0.35, 0.35, 1.9], height=8.5, size=9, pad=1.2)
    b.bold_cells(t)

    b.h('Rückblick')
    feld(b, 'Das habe ich nach dem Test verbessert:', 1)
    feld(b, 'Darauf bin ich besonders stolz:', 1)
    feld(b, 'Das mache ich beim nächsten Projekt anders:', 1)
    b.table(['Rückmeldung der Lehrkraft'], [['']], [1], height=22, size=10)
    path = OUT / 'ergebnisbogen.docx'
    D.save(path)
    return path


if __name__ == '__main__':
    for path in [ideenblatt(), protokollblatt(), ergebnisbogen()]:
        to_pdf(path)
        print('erstellt:', path.name, '+ PDF')
