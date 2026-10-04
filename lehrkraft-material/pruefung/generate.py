"""Generate the four-page 30-minute open-book exam and its answer key.
Run with the bundled Python; render the DOCX files with render_docx.py afterwards.
"""
from pathlib import Path
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
import sys
sys.path.insert(0, '/root/.codex/skills/builtins/documents/scripts')
from table_geometry import apply_table_geometry
OUT=Path(__file__).resolve().parent

def document(teacher=False):
 d=Document();s=d.sections[0];s.page_width=Mm(210);s.page_height=Mm(297)
 s.top_margin=s.bottom_margin=Mm(17);s.left_margin=Mm(22);s.right_margin=Mm(18)
 for name,size in [('Normal',11),('Title',21),('Heading 1',17),('Heading 2',14)]:
  st=d.styles[name];st.font.name='DejaVu Sans';st.font.size=Pt(size);st.font.color.rgb=RGBColor(0,0,0)
  st.paragraph_format.line_spacing=1.1;st.paragraph_format.space_after=Pt(5)
  st.paragraph_format.space_before=Pt(0 if name=='Normal' else 8)
  for b in list(st.element.findall('.//'+qn('w:pBdr'))):b.getparent().remove(b)
 s.header.paragraphs[0].text='WP Technik 7  |  Vom Baum zum Holz'
 f=s.footer.paragraphs[0];f.text=('Erwartungshorizont' if teacher else 'Lernerfolgskontrolle')+'  |  30 Minuten Open Book  |  Seite '
 field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');f._p.append(field)
 for st in ['Header','Footer']:d.styles[st].font.size=Pt(8)
 return d

def p(text='',bold=False):
 x=D.add_paragraph();r=x.add_run(text);r.bold=bold;return x

def h(text):D.add_heading(text,2)
def table(head,rows,widths):
 t=D.add_table(rows=1,cols=len(head));t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for c,txt in zip(t.rows[0].cells,head):c.text=txt
 for row in rows:
  for c,txt in zip(t.add_row().cells,row):c.text=str(txt)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for c in row.cells:
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   pr=c._tc.get_or_add_tcPr();border=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'5');e.set(qn('w:color'),'D9D9D9');border.append(e)
   pr.append(border)
   if i==0:
    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EEEEEE');pr.append(shade)
   for z in c.paragraphs:
    z.paragraph_format.space_before=z.paragraph_format.space_after=Pt(3)
    for r in z.runs:r.font.size=Pt(10.5);r.bold=i==0
 apply_table_geometry(t,[round(x*56.692913) for x in widths],indent_dxa=0)
 return t

def choose(prompt,options,multi=False):
 p(prompt+(' Mehrere Antworten sind richtig.' if multi else ' Nur eine Antwort ist richtig.'),True)
 for option in options:
  z=p('☐ '+option);z.paragraph_format.space_after=Pt(2)

def page(title):D.add_page_break();D.add_heading(title,0)
D=document();D.add_heading('Lernerfolgskontrolle Holz',0)
p('Name: ________________________  Klasse: _____  Datum: __________')
p('Arbeitszeit: 30 Minuten. Du darfst das gedruckte Material deiner Mappe benutzen. Das iPad und andere digitale Geräte darfst du nicht benutzen.',True)
p('Arbeite allein. Trage Zahlen oder kurze Wörter ein. Bei Ankreuzaufgaben steht dabei, ob eine oder mehrere Antworten richtig sind. Kreuze nur die richtigen Aussagen an. Bei Mehrfachauswahl kostet jedes falsche Kreuz einen Punkt in dieser Teilaufgabe; weniger als 0 Punkte gibt es nicht. Insgesamt: 30 Punkte.')
h('1 Aufbau des Stamms   4 Punkte')
p('1a Ergänze. Nutze deine Mappe. (2 P)')
p('Das ____________________ ermöglicht das Dickenwachstum.\nDas ____________________ leitet Wasser von den Wurzeln nach oben.')
choose('1b Der Bast ist rings um den Stamm unterbrochen. Welche Folge ist möglich? (2 P)',[
 'Die Wurzeln bekommen zu wenig Zucker aus den Blättern.',
 'Das Mark bildet sofort eine neue Borke.',
 'Der Stamm kann keine Jahresringe mehr zeigen.'])
h('2 Jahresringe auswerten   4 Punkte')
D.add_picture(str(OUT/'ringe.png'),width=Mm(95))
p('Die Mitte ist ein Punkt. Jede Kreislinie begrenzt einen Jahresring. Die Rinde ist nicht dargestellt. Die Zeichnung ist ein Modell.')
p('2a Trage nur die Zahl ein: Alter an dieser Schnittstelle: etwa ______ Jahre. (1 P)')
choose('2b Ring 8 ist schmaler als die Nachbarringe. Was zeigt das? (1 P)',[
 'Der Stamm ist in diesem Jahr weniger in die Dicke gewachsen.',
 'Der Baum ist in diesem Jahr kleiner geworden.'])
choose('2c Sam sagt: „In Jahr 8 hat es bestimmt zu wenig geregnet.“ Prüfe die Aussage. (2 P)',[
 'Wassermangel ist eine mögliche Ursache.',
 'Die Ringbreite beweist Wassermangel.',
 'Auch Licht, Temperatur oder Konkurrenz können das Wachstum beeinflussen.',
 'Ein schmaler Ring zeigt, wie hoch der Baum war.'],True)
page('Vom Baum zum Brett und zum Holztest')
h('3 Produktionsweg und Schnittplan   6 Punkte')
p('3a Ordne die Schritte. Trage nur die Zahlen 1 bis 6 in die Kästchen ein. 1 ist der Anfang. Nutze jede Zahl einmal. (3 P)',True)
p('[____] Transport     [____] Schnittholz     [____] Baum\n[____] Einschnitt     [____] Fällen     [____] Sägewerk')
p('3b Ergänze ein passendes Wort: Beim Sägen entstehen ____________, weil das Sägeblatt eine Schnittbreite hat. (1 P)')
p('3c Du brauchst mindestens 12 cm breite Bretter. Du darfst schmale Bretter nicht zusammenleimen. Nutze die Übungsdaten.')
table(['Plan','Ausbeute','Breite jedes Bretts'],[['A','72 %','9 cm'],['B','64 %','14 cm']],[30,55,85])
choose('Wähle den passenden Plan. (1 P)',['Plan A','Plan B'])
p('Ergänze: Dieser Plan passt, weil seine Bretter ______ cm breit sind. (1 P)')
h('4 Holzproben vergleichen   4 Punkte')
p('Zwei gleich große, ähnlich trockene Proben werden mit derselben Münze bei möglichst gleichem Druck geprüft. Die Angaben sind Übungsdaten.')
table(['Probe','Masse','Druckspur'],[['P','45 g','deutliche Spur'],['Q','68 g','kaum eine Spur']],[30,45,95])
choose('4a Welche Probe ist in diesem Test härter? (1 P)',['Probe P','Probe Q'])
p('4b Ergänze ein passendes Wort: Die härtere Probe erkenne ich daran, dass die Münze ____________ eine Spur hinterlässt. (1 P)')
choose('4c Eine dritte Probe ist doppelt so groß und wiegt 80 g. Welche Aussagen stimmen? (2 P)',[
 'Ihre größere Masse kann an ihrer Größe liegen.',
 'Die Masse von 80 g beweist, dass das Holz am härtesten ist.',
 'Für einen fairen Massevergleich sollten die Proben gleich groß und ähnlich trocken sein.',
 'Beim Massevergleich spielt die Feuchtigkeit keine Rolle.'],True)
page('Holzfeuchte und Holzfehler')
h('5 Holz arbeitet   4 Punkte')
p('Dieselbe Probe wird vor und nach dem Trocknen gemessen. Die Angaben sind Übungsdaten.')
table(['Messwert','Vorher feucht','Nach dem Trocknen'],[['Masse','80 g','68 g'],['Breite','50 mm','49 mm']],[60,55,55])
p('5a Ergänze zwei passende Wörter. (2 P)')
p('Die Masse sinkt, weil das Holz ____________________ abgibt.\nDie Breite nimmt ab. Diese Verkleinerung heißt ____________________.')
p('5b Eine Holzschublade klemmt in einem feuchten Raum. Ergänze zwei passende Wörter. (2 P)')
p('Das Holz kann Wasser aufnehmen und ____________________.\nBeim Bau lässt du deshalb etwas ____________________ für die Bewegung.')
h('6 Holzfehler beurteilen   4 Punkte')
D.add_picture(str(OUT/'fehler.png'),width=Mm(164))
p('Bild C zeigt ein Brett von der Seite über einer geraden Unterlage.')
p('6a Ordne zu. Trage nur die Zahlen ein: 1 = Ast, 2 = Verwerfen, 3 = Riss. (3 P)',True)
p('Bild A: ______     Bild B: ______     Bild C: ______')
choose('6b Ein Brett hat einen kleinen, fest verwachsenen Ast. Welche Aussage stimmt? (1 P)',[
 'Das Brett muss immer weggeworfen werden.',
 'Ob der Ast stört, hängt von seiner Lage und der Nutzung des Bretts ab.',
 'Ein Ast macht jedes Brett automatisch tragfähiger.'])
page('Eine Holzart für einen Auftrag auswählen')
h('7 Eine Kundin beraten   4 Punkte')
p('Eine Kundin braucht ein Regal für einen trockenen Innenraum. Die Oberfläche soll hart und glatt sein. Von den passenden Holzarten möchte sie die preiswertere. Vergleiche nur die Angaben in der Tabelle.',True)
p('Die Tabelle enthält vereinfachte Übungsangaben. Alle angebotenen Bretter haben passende Maße.')
table(['Holzart','Oberfläche und Bearbeitung','Preis','Grenze'],[
 ['Fichte','weich; lässt sich glatt bearbeiten','niedrig','Druckstellen entstehen leicht'],
 ['Buche','hart; lässt sich glatt bearbeiten','mittel','arbeitet stark bei wechselnder Feuchte'],
 ['Eiche','hart; lässt sich glatt bearbeiten','hoch','teurer als Buche']], [25,64,25,56])
choose('7a Welche Holzart erfüllt den Auftrag am besten? (1 P)',['Fichte','Buche','Eiche'])
p('7b Ergänze deine Begründung mit zwei passenden Wörtern. (2 P)')
p('Die gewählte Holzart eignet sich, weil ihre Oberfläche\n____________________ ist und sich ____________________ bearbeiten lässt.')
p('7c Ergänze einen passenden Nachteil. (1 P)')
p('Bei wechselnder Feuchtigkeit arbeitet dieses Holz ____________________.')
h('Prüfe deine Arbeit')
p('Lies deine Antworten noch einmal. Sind alle Zahlen und Lücken ausgefüllt? Hast du bei jeder Ankreuzaufgabe auf den Hinweis geachtet?')
p('Punkte: ______ / 30    Rückmeldung: __________________________')
D.save(OUT/'lernerfolgskontrolle.docx')

D=document(True);D.add_heading('Erwartungshorizont Holz',0)
p('Zur vierseitigen Lernerfolgskontrolle mit 30 Minuten Arbeitszeit und 30 Punkten. Erlaubt ist das gedruckte Material der Mappe. iPad und andere digitale Geräte sind ausgeschlossen.')
h('Durchführung und Zeitplanung')
p('Die vier Seiten gemeinsam ausgeben. Orientierung: Aufgaben 1 und 2 etwa 7 Minuten, 3 und 4 etwa 8 Minuten, 5 und 6 etwa 7 Minuten, Aufgabe 7 etwa 5 Minuten, abschließende Kontrolle etwa 3 Minuten. Das Nachschlagen ist in diesen Planwerten enthalten; nach dem ersten Einsatz prüfen. Vereinbarte Nachteilsausgleiche beachten.')
h('Bewertung')
p('Sinngemäße Lückenfüllungen anerkennen. Rechtschreibfehler nicht abziehen, sofern der Fachbegriff eindeutig ist. Jeder Teil wird getrennt bewertet. Ein falsches Kreuz in 4a verhindert nicht den Punkt für eine fachlich passende Begründung in 4b. Kein automatisch abgeleiteter Notenschlüssel.')
p('Einfachauswahl: Nur das richtige und kein weiteres Feld angekreuzt ergibt die genannten Punkte. Mehrfachauswahl 2c und 4c: je richtig gesetztem Kreuz 1 Punkt, je falsch gesetztem Kreuz 1 Punkt Abzug innerhalb der Teilaufgabe; mindestens 0, höchstens 2 Punkte. Nicht gesetzte Kreuze geben keine Punkte. Ein vollständig leeres Feld ergibt 0 Punkte. So wird nicht wahlloses Ankreuzen belohnt.')
h('Lösungen zu Aufgaben 1 bis 4')
for title,text in [
('1 Aufbau des Stamms   4 Punkte','1a Kambium; Splintholz: je 1 P. 1b Erste Aussage: Die Wurzeln bekommen zu wenig Zucker aus den Blättern; 2 P bei eindeutiger Auswahl. Die Störung des Zuckertransports wird aus der Funktion des Basts abgeleitet.'),
('2 Jahresringe   4 Punkte','2a 12 Jahre: 1 P. 2b Erste Aussage (geringerer Dickenzuwachs): 1 P. 2c Erste und dritte Aussage: Wassermangel ist möglich, andere Ursachen kommen ebenfalls infrage; bis 2 P nach Mehrfachregel.'),
('3 Produktionsweg und Schnittplan   6 Punkte','3a In der gedruckten Reihenfolge: 3, 6, 1, 5, 2, 4. Je korrekt eingetragener Zahl 0,5 P, insgesamt 3 P. 3b Späne / Sägespäne: 1 P. 3c Plan B: 1 P; 14 cm: 1 P. Die höhere Ausbeute von A genügt bei einer Mindestbreite von 12 cm nicht.'),
('4 Holzproben   4 Punkte','4a Probe Q: 1 P. 4b kaum: 1 P. 4c Erste und dritte Aussage: Größere Masse kann durch größeres Volumen entstehen; gleiche Größe und ähnliche Trockenheit erlauben einen fairen Vergleich; bis 2 P nach Mehrfachregel.')]:
 h(title);p(text)
page('Lösungen und Kompetenzbelege')
for title,text in [
('5 Holz arbeitet   4 Punkte','5a Wasser; Schwinden: je 1 P. Auch „Feuchtigkeit“ bzw. „schwinden“ sinngemäß akzeptieren. 5b quellen / größer werden; Spiel / Platz / Abstand: je 1 P. Das Quellen kann zum Klemmen führen; die Bewegungsreserve ist eine passende Vorsorge.'),
('6 Holzfehler   4 Punkte','6a A = 3, B = 1, C = 2: je 1 P. 6b Zweite Aussage: Lage und Nutzung entscheiden; 1 P bei eindeutiger Auswahl. Ein fest verwachsener Ast ist kein pauschaler Ausschussgrund.'),
('7 Materialentscheidung   4 Punkte','7a Buche: 1 P. Nach Tabelle erfüllen Buche und Eiche Härte und glatte Bearbeitbarkeit; Buche ist von beiden preiswerter. 7b hart; glatt: je 1 P. 7c stark / deutlich: 1 P. Die Lückensätze werden unabhängig von 7a bewertet; kein mehrfacher Abzug eines Auswahlfehlers.')]:
 h(title);p(text)
h('Was die kurze Arbeit nachweisen kann')
p('Die geschlossene oder stark gestützte Antwortform prüft Verstehen und Anwenden mit wenig Schreibaufwand. Sie belegt keine frei formulierte ausführliche Erklärung. Die früheren 21 Teilaufgaben a bis c und deren Raster gelten für diese Fassung nicht mehr. Eine Gesamtpunktzahl wird deshalb nicht automatisch in einen Kompetenzstandard übersetzt.')
table(['Anforderung','Belege in dieser Arbeit'],[
 ['Mindeststandard','Funktionen ergänzen (1a), Ringe zählen (2a), Schritte ordnen (3a), Begriffe und Bilder zuordnen (6a)'],
 ['Regelstandard','Ringbreite deuten (2b), Schnittbreite erklären (3b), Härte aus Druckspur ableiten (4a/b), Trocknungsdaten erklären (5a), Eigenschaften mit Auftrag verbinden (7b/c)'],
 ['Expertenstandard','Folge einer Bastschädigung ableiten (1b), Grenze einer Aussage prüfen (2c), Mindestbreite gegen Ausbeute abwägen (3c), Vergleichsbedingungen prüfen (4c), Vorsorge übertragen (5b), Verwendbarkeit beurteilen (6b), mehrere Anforderungen abwägen (7a)']], [43,127])
p('Die Expertenbelege sind hier kurze, gestützte Entscheidungen. Für Aussagen über selbstständiges Argumentieren zusätzlich die Mappe oder ein Gespräch heranziehen.')
page('Individuelle Rückmeldung')
p('Name: ____________________________  Datum: ______________')
p('Punkte: ______ / 30')
table(['Bereich','Punkte','Dein nächster Übungsauftrag'],[
 ['Stamm','____ / 4','A1'],['Jahresringe','____ / 4','A2'],['Produktionsweg und Schnittplan','____ / 6','A3 und A4'],['Holzproben','____ / 4','A5 und A6'],['Holzfeuchte','____ / 4','A7'],['Holzfehler','____ / 4','A8'],['Materialentscheidung','____ / 4','A9 und A10']], [75,25,70])
h('Das gelingt dir schon')
p('________________________________________________________________\n________________________________________________________________')
h('Deine nächsten Schritte')
p('Übe zuerst: _____________________________________________________\nPassender Auftrag: ______________________________________________')
p('Wenn nötig, übe danach: __________________________________________')
p('Erkläre einen dieser Zusammenhänge in zwei eigenen Sätzen auf U.1. Besprich deine Erklärung mit einem Partner oder deiner Lehrkraft.')
D.save(OUT/'erwartungshorizont.docx')
print('Exam: 4 planned pages. Answer key: 3 planned pages. Total: 30 points.')
