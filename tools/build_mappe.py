from pathlib import Path
import sys,json,math
from docx import Document
from docx.shared import Mm,Pt,RGBColor
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'/root/.codex/skills/builtins/documents/scripts')
from table_geometry import apply_table_geometry
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'materialien'; OUT.mkdir(exist_ok=True)
data=json.loads((ROOT/'kurs-daten.js').read_text().split(' = ',1)[1].rstrip(';\n'))
# Preset compact_reference_guide; named overrides worksheet_A4: 20mm margins,
# Arial 12pt, monochrome headings, response lines 24pt, page-based worksheet IDs.
D=Document();sec=D.sections[0];sec.page_width=Mm(210);sec.page_height=Mm(297)
sec.top_margin=sec.bottom_margin=Mm(18);sec.left_margin=sec.right_margin=Mm(20);sec.header_distance=sec.footer_distance=Mm(9)
for name,size,before,after in [('Normal',12,0,6),('Title',25,0,10),('Subtitle',13,0,8),('Heading 1',20,0,10),('Heading 2',13,14,7),('Heading 3',12,10,5)]:
 s=D.styles[name];s.font.name='Arial';s.font.size=Pt(size);s.font.color.rgb=RGBColor.from_string('263844');s.paragraph_format.space_before=Pt(before);s.paragraph_format.space_after=Pt(after);s.paragraph_format.line_spacing=1.25
D.styles['Normal'].font.color.rgb=RGBColor.from_string('222222')
for sty in D.styles:
 if sty.element.pPr is not None:
  for border in list(sty.element.pPr.findall(qn('w:pBdr'))):sty.element.pPr.remove(border)
for name in ['Header','Footer']:
 D.styles[name].font.name='Arial';D.styles[name].font.size=Pt(9)
sec.header.paragraphs[0].text='HBG  |  WP Technik 7  |  Vom Baum zum Holz'
f=sec.footer.paragraphs[0];f.text='Deine Ergebnisse gehören in die Mappe.                                         '
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)

def p(t='',style=None):return D.add_paragraph(t,style)
def h(t):return D.add_paragraph(t,'Heading 2')
def page(id,title,goal=None):
 if len(D.paragraphs):D.add_page_break()
 D.add_heading(id+'  |  '+title,0)
 p('Name: ____________________________   Datum: ______________')
 if goal:p('Mein Ziel: '+goal)
def lines(n=2):
 for _ in range(n):
  z=p();z.paragraph_format.space_after=Pt(0);z.paragraph_format.line_spacing=1;z.paragraph_format.space_before=Pt(0)
  z.paragraph_format.line_spacing=Pt(24)
  pp=z._p.get_or_add_pPr();b=OxmlElement('w:pBdr');bot=OxmlElement('w:bottom');bot.set(qn('w:val'),'single');bot.set(qn('w:sz'),'3');bot.set(qn('w:color'),'AAAAAA');b.append(bot);between=OxmlElement('w:between');between.set(qn('w:val'),'single');between.set(qn('w:sz'),'3');between.set(qn('w:color'),'AAAAAA');b.append(between);pp.append(b)
def box(label,height=55):
 h(label);z=p(' ');z.paragraph_format.line_spacing=Pt(height);z.paragraph_format.space_after=Pt(8)
 pp=z._p.get_or_add_pPr();b=OxmlElement('w:pBdr')
 for edge in ['top','left','bottom','right']:
  a=OxmlElement('w:'+edge);a.set(qn('w:val'),'single');a.set(qn('w:sz'),'4');a.set(qn('w:color'),'999999');a.set(qn('w:space'),'6');b.append(a)
 pp.append(b)
def table(headers,rows,widths=None,height=None):
 t=D.add_table(rows=1,cols=len(headers));t.style='Table Grid'
 for c,txt in zip(t.rows[0].cells,headers):c.text=txt
 for row in rows:
  cells=t.add_row().cells
  for c,txt in zip(cells,row):c.text=str(txt)
 for i,row in enumerate(t.rows):
  for c in row.cells:
   for q in c.paragraphs:
    q.paragraph_format.space_after=Pt(4);q.paragraph_format.space_before=Pt(4);q.paragraph_format.line_spacing=1.15
    for r in q.runs:r.font.size=Pt(11);r.bold=(i==0)
  if height and i>0:row.height=Mm(height);row.height_rule=WD_ROW_HEIGHT_RULE.AT_LEAST
  pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
 t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 total=round(170/25.4*1440)
 if not widths:widths=[total//len(headers)]*len(headers);widths[-1]+=total-sum(widths)
 else:
  widths=[round(total*x/sum(widths)) for x in widths];widths[-1]+=total-sum(widths)
 apply_table_geometry(t,widths,indent_dxa=120)
 if height:
  for row in t.rows[1:]:row.height=Mm(height);row.height_rule=WD_ROW_HEIGHT_RULE.AT_LEAST
 return t

def check(text):p('KONTROLLE: '+text)
# Accurate schematic independent of app's shuffled numbers: six radial layers, callouts.
img=Image.new('RGB',(1400,700),'white');dr=ImageDraw.Draw(img);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',30)
cx,cy=350,340
rads=[290,262,238,218,130,24]
for r,fill in zip(rads,['#ddd','#fff','#ddd','#fff','#eee','#ccc']):dr.ellipse((cx-r,cy-r,cx+r,cy+r),fill=fill,outline='#333',width=3)
for i,(r,a) in enumerate(zip([278,250,228,175,80,0],[-55,-32,-7,20,49,0])):
 x=cx+r*math.cos(math.radians(a));y=cy+r*math.sin(math.radians(a));yy=90+i*98
 dr.ellipse((x-5,y-5,x+5,y+5),fill='#111');dr.line([(x,y),(720,yy),(790,yy)],fill='#222',width=2)
 dr.text((810,yy-20),f'{i+1}. ____________________',font=font,fill='#111')
img.save(OUT/'baumscheibe-schema.png')
# cover
p('MEINE HOLZFORSCHER-MAPPE','Subtitle');D.add_heading('Vom Baum zum Holz',0)
p('WP Technik 7  |  6 Wochen');p('Name: ___________________________________');p('Klasse: ___________')
h('So arbeitest du');p('Die Mappe ist dein Arbeitsort. Die Website zeigt dir den nächsten Schritt. Schreibe und zeichne deine Ergebnisse auf diese Blätter.')
p('Öffne auf deinem iPad:');p('https://wp7ur1-holz.vercel.app/lernweg.html')
h('Unsere Zeichen');table(['Zeichenwort','Das tust du'],[['MAPPE','Du schreibst oder zeichnest auf Papier.'],['iPAD','Du nutzt digitales Material.'],['LESEN','Du liest eine Information.'],['ERKUNDEN','Du probierst aus oder beobachtest.'],['HILFE','Du öffnest freiwillig einen Tipp.'],['VERTIEFUNG','Du wählst eine freiwillige Zusatzaufgabe.'],['HALTEPUNKT','Du sprichst mit Lehrkraft oder Partner.'],['KONTROLLE','Du prüfst deinen Pflichtteil.']],[1,3])
p('Auf Papier steht zusätzlich immer das Zeichenwort. So bleibt die Orientierung auch im Schwarz-Weiß-Druck klar.')
page('WEG','Dein Lernweg');p('Hake den Auftrag ab, wenn dein Ergebnis in der Mappe liegt und du es geprüft hast.')
table(['Woche','Auftrag','Fertig'],[[str(t['week']),t['id']+' '+t['title'],'[  ]'] for t in data['tasks']]+[['6','Kompetenzcheck, Übung und Lernnachweis','[  ]']],[1,6,1])
h('Dein Unterricht');p('Montag: 45 Minuten. Mittwoch: 90 Minuten. Jede Woche beginnt mit einem kurzen Input. Danach arbeitest du an deinem nächsten Schritt.')
h('Deine Lernroutine');p('Start: Welches Blatt brauche ich?');p('Arbeit: Lies nur den aktuellen Schritt. Nutze bei Bedarf eine Hilfe.');p('Abschluss: Prüfe dein Ergebnis. Merke dir deinen nächsten Schritt.')
p('Wichtig: In Woche 3 beginnt bereits die erste Messung für A7.')
page('A1','Die Baumscheibe','Ich kann sechs Teile des Stamms benennen.')
h('A1.1 | MAPPE');p('Erkunde zuerst die Baumscheibe am iPad. Beschrifte dann die sechs Bereiche im Bild. Die Zahlen in der App können anders angeordnet sein.')
D.add_picture(str(OUT/'baumscheibe-schema.png'),width=Mm(170))
p('Wortspeicher: Kernholz · Bast · Mark · Borke · Splintholz · Kambium')
p('Das Bild ist ein vereinfachtes Modell. Die dünnen Schichten sind vergrößert. Nicht jeder Baum hat einen deutlich dunkleren Kern.')
h('Erkläre kurz');p('Wo wird der Stamm dicker?');lines(2);check('Alle sechs Begriffe sind zugeordnet. Ich habe meine Beschriftung geprüft.')
page('A2','Jahresringe lesen','Ich kann Beobachtung und Vermutung unterscheiden.')
h('A2.1 | MAPPE');p('Untersuche die Modell-Scheibe in der App. Zähle die Jahresringe und prüfe deine Zahl.');p('Zahl der Jahresringe: ___________');p('Ungefähres Alter an dieser Schnittstelle: ___________ Jahre')
h('A2.2 | MAPPE');p('Wähle einen auffälligen Ring. Zähle seine Nummer von innen.');p('Ich untersuche Ring Nummer: ___________');p('Das sehe ich (zum Beispiel: breiter oder schmaler als die Nachbarringe):');lines(2);p('Das vermute ich als mögliche Ursache:');lines(2);p('Das könnte das Wachstum beeinflusst haben, weil …');lines(2)
p('Merke: Ein Jahresring zeigt Wachstum. Die genaue Ursache ist am Ring allein nicht sicher erkennbar.');check('Meine Beobachtung und meine Vermutung stehen getrennt da.')
page('A3','Vom Baum zum Brett','Ich kann die Produktionskette erklären.')
h('A3.1 | MAPPE');p('Ordne zuerst die Karten am iPad. Schreibe dann die sechs Schritte in die Tabelle. Erkläre jeden Schritt in einem kurzen Satz.')
table(['Nr.','Produktionsschritt','Was passiert?'],[[str(i),'',''] for i in range(1,7)],[.5,2,4],height=22)
p('Satzanfänge: Zuerst … Danach … Anschließend … Am Ende …');check('Die Reihenfolge stimmt. Zu jedem Schritt steht ein Satz.')
page('A4','Der Schnittplan','Ich kann Schnittpläne vergleichen.')
h('A4.1 | MAPPE');p('Erstelle zwei unterschiedliche Pläne in der Simulation. Notiere die angezeigten Werte.')
table(['Plan','Nutzbare Bretter','Ausbeute in %'],[['A','',''],['B','','']],[1,2,2],height=15)
h('A4.2 | MAPPE');p('Wo entsteht Verschnitt? Erkläre mit deinen Plänen.');lines(2);p('Warum kann nicht der ganze Stamm zu Brettern werden?');lines(2);p('Welchen Plan wählst du? Begründe. Beachte Ausbeute und brauchbare Brettmaße.');lines(3);check('Ich habe beide Pläne dokumentiert und meine Wahl begründet.')
page('A5','Die Prüftabelle','Ich kann Holzproben vergleichbar untersuchen.')
h('A5.1 | MAPPE');p('Untersuche drei gleich große Proben. Trage Messwerte und Beobachtungen direkt ein. Die Stationsanleitung steht auf dem iPad.')
table(['Prüfung','Probe ___','Probe ___','Probe ___'],[['Holzart','','',''],['Farbe und Maserung','','',''],['Masse in g','','',''],['Härte: sichtbare Spur','','',''],['Wasser nach ___ s','','','']],[1.4,1,1,1],height=20)
p('Bedingungen: gleiche Probengröße, vergleichbare Feuchte, gleiche Tropfenzahl und Wartezeit. Prüfe Wasser auf derselben Oberflächenrichtung.')
p('Wortspeicher: hell · dunkel · fein · deutlich · keine Spur · leichte Spur · deutliche Spur · Tropfen steht · zieht ein')
p('HALTEPUNKT: Bereite mit deiner Lehrkraft die feuchte Probe für A7 vor. Notiere die Startwerte auf A7.1.');check('Alle vier Prüfungen sind dokumentiert. Ich habe aufgeräumt.')
page('A6','Der Prüfbericht','Ich kann aus Beobachtungen Eigenschaften ableiten.')
h('A6.1 | MAPPE');p('Wähle zwei Holzarten aus A5.1. Verbinde jeweils eine Beobachtung mit einer Eigenschaft und einer passenden Verwendung.')
for i in [1,2]:
 h(f'Holzart {i}: ______________________________');p('Ich beobachte …');lines(1);p('Also ist dieses Holz im Vergleich …');lines(1);p('Gut ist das für …, weil …');lines(1)
p('Wichtig: Eine höhere Masse allein belegt keine größere Härte. Dafür brauchst du den Härteversuch.');check('Mein Partner hat geprüft: Die Eigenschaft passt zur Beobachtung.')
page('A7.1','Trockenversuch: Messen','Ich kann Veränderungen dokumentieren.')
p('HALTEPUNKT: Beginne diese Seite in Woche 3 mit deiner Lehrkraft.');p('Proben-ID: ___________  Holzart: __________________________')
p('Markiere die Messstellen an der Probe. Miss in Woche 4 dieselbe Probe an denselben Stellen mit denselben Geräten.')
table(['Messung','Woche 3: feucht','Woche 4: nach Trocknung','Neu minus alt'],[['Datum','','','-'],['Masse in g','','',''],['Breite in mm','','',''],['Dicke in mm (optional)','','','']],[1.3,1.2,1.4,1.1],height=19)
p('Ein Minuszeichen bedeutet: Der neue Wert ist kleiner. Wenn du keine Veränderung messen kannst, trage 0 ein.')
box('Skizziere deine Probe. Markiere Breite und Messstelle.',60)
p('Trocknungsort: __________________________________________')
page('A7.2','Trockenversuch: Auswerten','Ich kann Trocknen, Schwinden und Quellen erklären.')
h('A7.2 | MAPPE');p('Beschreibe zuerst deine Messwerte. Was hat sich verändert? Was blieb gleich?');lines(3)
p('Erkläre, warum sich die Masse beim Trocknen verändern kann.');lines(2)
p('Ergänze die Begriffe mit einer eigenen Erklärung.');table(['Begriff','Deine Erklärung'],[['Holzfeuchte',''],['Schwinden',''],['Quellen','']],[1,4],height=16)
p('Warum sollte Holz vor dem Möbelbau passend getrocknet werden? Nenne ein mögliches Problem.');lines(2)
p('Merke: Eine kleine Maßänderung ist manchmal nicht messbar. Du brauchst keine Werte zu erfinden.');check('Ich habe Messwerte und Erklärung unterschieden.')
page('A8','Holzfehler finden','Ich kann Fehler erkennen und Folgen beschreiben.')
h('A8.1 | MAPPE');p('Ordne die drei Begriffe am iPad zu. Zeichne danach zu jedem Begriff eine einfache Skizze.')
table(['Riss','Ast','Verwerfen'],[['','','']],[1,1,1],height=40)
h('A8.2 | MAPPE');p('Wähle einen Fehler. Nenne ein Produkt und erkläre eine mögliche technische Folge.');p('Mein Fehler: ______________  Mein Produkt: ______________');lines(4)
p('Ein Ast ist ein natürlicher Teil des Holzes. Ob er stört, hängt von seiner Beschaffenheit und vom Produkt ab.');check('Die drei Skizzen sind erkennbar. Meine Erklärung nennt eine Folge.')
page('A9','Die Holzberatung','Ich kann eine begründete Materialentscheidung treffen.')
h('A9.1 | MAPPE');p('Lies deine Kundenkarte. Notiere den Auftrag und wichtige Anforderungen.');p('Mein Kundenauftrag: __________________________________');lines(2)
h('A9.2 | MAPPE');p('Vergleiche Holzarten am iPad. Entscheide dich.');p('Ich empfehle: __________________________________________');table(['Passende Eigenschaft','Das hilft beim Auftrag, weil …'],[['',''],['',''],['','']],[1,2],height=15)
p('Ein Nachteil meiner Wahl:');lines(1);p('Meine Empfehlung in einem zusammenhängenden Satz:');lines(2);check('Drei Eigenschaften, ein Nachteil und eine Begründung sind vorhanden.')
page('A10','Meine Produktkarte','Ich kann meine Empfehlung verständlich darstellen.')
p('A10.1 | MAPPE: Nutze A9. Gestalte die vier Bereiche. Lass einen Partner prüfen, ob deine Empfehlung verständlich ist.')
box('Feld 1 | Produktname und Skizze',70)
h('Feld 2 | Gewählte Holzart');lines(1)
h('Feld 3 | Drei passende Eigenschaften mit Begründung');lines(4)
h('Feld 4 | Ein Nachteil');lines(2)
p('Partnerprüfung: ___________________  Datum: _____________')
page('K','Mein Kompetenzcheck','Ich weiß, was ich als Nächstes übe.')
p('Schätze dich ehrlich ein. Der Check steuert dein Lernen. Er ist keine Klassenarbeit.')
competencies=[('Produktionskette ordnen','A3'),('Stammteile benennen','A1'),('Beobachtung und Eigenschaft unterscheiden','A6'),('erklären, warum Holz getrocknet wird','A7'),('Quellen und Schwinden erklären','A7'),('eine Holzart passend auswählen','A9'),('eine Materialentscheidung begründen','A9/A10')]
table(['Ich kann …','Unsicher','Teilweise','Sicher'],[[a,'[  ]','[  ]','[  ]'] for a,b in competencies],[4,1,1,1],height=13)
p('Wähle zuerst einen unsicheren Punkt. Öffne den genannten Auftrag im Lernweg und bearbeite eine Übung auf U.1.')
p('Punkt 1: A3 | Punkt 2: A1 | Punkt 3: A6 | Punkte 4 und 5: A7 | Punkt 6: A9 | Punkt 7: A9/A10')
p('Ich übe: ____________________  Auftrag: __________________')
page('U.1','Meine gezielte Übung');p('Wähle genau eine Übung passend zu deinem Kompetenzcheck. Nutze zuerst bei Bedarf dein Material. Prüfe danach ohne Hilfe.')
for title,txt in [('A1','Skizziere einen Stammquerschnitt und beschrifte seine sechs Bereiche.'),('A3','Schreibe die Produktionskette auf. Erkläre zwei Schritte.'),('A6','Nenne eine Beobachtung aus A5. Leite eine passende Eigenschaft und Verwendung ab.'),('A7','Erkläre an einem Beispiel Quellen oder Schwinden und eine mögliche Folge.'),('A9/A10','Wähle einen anderen Kundenauftrag. Begründe eine Holzart mit drei Eigenschaften und einem Nachteil.')]:p(title+': '+txt)
p('Meine Übung / Auftrags-ID: ______________________________')
lines(9);p('Kontrolle mit: ______________  Mein nächster Schritt: __________')
page('V.1','Meine freiwillige Vertiefung');p('Diese Seite ist freiwillig. Wähle eine Vertiefung erst, wenn dein Pflichtauftrag geprüft ist. Die Aufgabe öffnest du im Lernweg.')
p('Auftrag: ___________  Meine Frage: ________________________');lines(12)
p('Das habe ich neu verstanden:');lines(2)
D.save(OUT/'holzforscher-mappe.docx')
# Separate customer cards, two per page. Reuse same styles and geometry.
for child in list(D._element.body):
 if child.tag!=qn('w:sectPr'):D._element.body.remove(child)
for i,c in enumerate(data['customers']):
 if i%2==0 and i:D.add_page_break()
 D.add_heading('A9-K'+str(i+1)+' | '+c['title'],1);p('KUNDENKARTE');p(c['text'])
 h('Dein Auftrag');p('Notiere die Anforderungen auf A9.1. Vergleiche Holzarten. Begründe auf A9.2 deine Wahl mit drei Eigenschaften und einem Nachteil.')
 p('HILFE bei Bedarf: '+c['hint'])
 if i%2==0:p().paragraph_format.space_after=Pt(28)
D.save(OUT/'kundenkarten.docx')
print('Mappe und acht Kundenkarten erstellt.')
