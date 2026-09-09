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
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent

# Preset compact_reference_guide; named overrides worksheet_A4: 20mm margins,
# Arial 12pt, monochrome headings, response lines 24pt, page-based worksheet IDs.
D=Document();sec=D.sections[0];sec.page_width=Mm(210);sec.page_height=Mm(297)
sec.top_margin=sec.bottom_margin=Mm(18);sec.left_margin=sec.right_margin=Mm(20);sec.header_distance=sec.footer_distance=Mm(9)
for name,size,before,after in [('Normal',12,0,6),('Title',25,0,10),('Subtitle',13,0,8),('Heading 1',20,0,10),('Heading 2',13,14,7),('Heading 3',12,10,5)]:
 s=D.styles[name];s.font.name='Arial';s.font.size=Pt(size);s.font.color.rgb=RGBColor.from_string('000000');s.paragraph_format.space_before=Pt(before);s.paragraph_format.space_after=Pt(after);s.paragraph_format.line_spacing=1.25
D.styles['Normal'].font.color.rgb=RGBColor.from_string('222222')
for sty in D.styles:
 if sty.element.pPr is not None:
  for border in list(sty.element.pPr.findall(qn('w:pBdr'))):sty.element.pPr.remove(border)
for name in ['Header','Footer']:
 D.styles[name].font.name='Arial';D.styles[name].font.size=Pt(9)
sec.header.paragraphs[0].text='HBG  |  WP Technik 7  |  Vom Baum zum Holz'
f=sec.footer.paragraphs[0];f.text='WP Technik 7   Lernerfolgskontrolle                                         '
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
# Exact schematic figures, drawn locally for print.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26)
im=Image.new('RGB',(1000,420),'white');dr=ImageDraw.Draw(im);r=7
for n in range(1,13):
 prev=r;r+=7 if n==8 else 14
 dr.ellipse((230-r,205-r,230+r,205+r),outline='black',width=2)
 if n==8:
  dr.line((230+r,205,510,205),fill='black',width=2);dr.text((525,185),'Ring 8',fill='black',font=font)
dr.ellipse((227,202,233,208),fill='black');dr.text((520,245),'Modell einer Baumscheibe',fill='black',font=font)
im.save(OUT/'ringe.png')
im=Image.new('RGB',(1350,340),'white');dr=ImageDraw.Draw(im)
for x,label in [(15,'Bild A'),(460,'Bild B'),(905,'Bild C')]:dr.text((x+130,285),label,fill='black',font=font)
dr.rectangle((20,40,420,240),outline='black',width=3)
for y in [85,125,165,205]:dr.line((25,y,410,y+5),fill='#999',width=2)
dr.line([(205,40),(180,85),(210,120),(175,165),(190,205)],fill='black',width=7)
dr.rectangle((465,40,865,240),outline='black',width=3)
for ry in [22,38,55]:dr.ellipse((665-ry,140-ry,665+ry,140+ry),outline='black',width=3)
for y in [70,210]:dr.line((475,y,855,y),fill='#999',width=2)
# Bowed board in side view, next to a straight reference surface.
dr.arc((915,-30,1325,210),0,180,fill='black',width=4);dr.arc((915,5,1325,245),0,180,fill='black',width=4)
dr.line((915,90,915,125),fill='black',width=4);dr.line((1325,90,1325,125),fill='black',width=4);dr.line((915,255,1325,255),fill='#999',width=2)
im.save(OUT/'fehler.png')
# Seven task pages with space for handwriting.
D.add_heading('Lernerfolgskontrolle Holz',0);p('Name: _________________________  Klasse: ______  Datum: __________')
p('Du hast 60 Minuten. Arbeite allein auf diesen sieben Seiten. Mappe und iPad bleiben geschlossen. Nutze die Materialien auf dem Blatt. Kurze Sätze reichen. Prüfe deine Antworten am Ende.')
p('Bearbeite in jedem Block zuerst a, dann b und c. Wenn du festhängst, beginne den nächsten Block. Zeige bei c, wie du dein Wissen weiterdenken kannst.')
h('1  Was steckt im Stamm');p('1a Erkennen: Beschrifte die sechs Bereiche mit den Wörtern aus dem Kasten.')
D.add_picture(str(OUT/'stamm.png'),width=Mm(155))
p('Borke · Bast · Kambium · Splintholz · Kernholz · Mark')
p('1b Erklären: Welche Aufgabe haben Kambium und Splintholz?');lines(3)
p('1c Weiterdenken: Der Bast ist rings um einen Stamm stark beschädigt. Warum ist das für den Baum gefährlich?');lines(3)
page('2','Was verraten Jahresringe');D.add_picture(str(OUT/'ringe.png'),width=Mm(150))
p('Die Mitte ist als Punkt markiert. Jede geschlossene Kreislinie begrenzt einen Jahresring. Die Rinde ist nicht dargestellt.')
h('2a Erkennen');p('Zähle die Jahresringe. Notiere das ungefähre Alter an dieser Schnittstelle.');lines(2)
h('2b Erklären');p('Ring 8 ist schmaler als seine Nachbarringe. Was sagt das über das Wachstum?');lines(3)
h('2c Weiterdenken');p('Sam sagt: „In diesem Jahr hat es bestimmt zu wenig geregnet.“ Beurteile Sams Aussage.');lines(4)
page('3','Vom Baum zum Brett');h('3a Erkennen');p('Ordne die sechs Begriffe. Schreibe die richtige Reihenfolge auf.')
p('Transport · Schnittholz · Baum · Einschnitt · Fällen · Sägewerk');lines(3)
h('3b Erklären');p('Was passiert beim Einschnitt? Warum entsteht dabei Verschnitt?');lines(4)
h('3c Weiterdenken');p('Du brauchst mindestens 12 cm breite Bretter. Die Bretter werden nicht zusammengeleimt. Welchen Schnittplan wählst du? Begründe mit der Tabelle.')
table(['Plan','Ausbeute','Brettbreite'],[['A','72 %','9 cm'],['B','64 %','14 cm']],[1,2,2]);lines(4)
page('4','Was zeigt der Holztest');p('Zwei gleich große, ähnlich trockene Proben werden mit derselben Münze bei möglichst gleichem Druck geprüft.')
table(['Probe','Masse','Sichtbare Spur'],[['P','45 g','deutliche Druckspur'],['Q','68 g','kaum eine Druckspur']],[1,1,3])
h('4a Erkennen');p('Welche Probe hat die größere Masse? Bei welcher Probe siehst du die deutlichere Druckspur?');lines(2)
h('4b Erklären');p('Welche Probe ist bei dieser Prüfung härter? Begründe mit einer Beobachtung.');lines(3)
h('4c Weiterdenken');p('Eine dritte Probe ist doppelt so groß und wiegt 80 g. Alex sagt: „Diese Holzart ist am schwersten.“ Warum reicht dieser Vergleich nicht aus? Wie könntest du besser vergleichen?');lines(4)
page('5','Warum arbeitet Holz');table(['Messung derselben Probe','Vorher feucht','Nach Trocknung'],[['Masse','80 g','68 g'],['Breite','50 mm','49 mm']],[2,1,1])
h('5a Erkennen');p('Ergänze die Fachbegriffe.')
p('Holz nimmt Wasser in seine Zellwände auf und wird größer: ______________')
p('Holz wird beim Trocknen kleiner: __________________________')
h('5b Erklären');p('Beschreibe die beiden Veränderungen in der Tabelle. Erkläre, warum sie entstehen.');lines(4)
h('5c Weiterdenken');p('Eine Schublade lässt sich in einem feuchten Raum plötzlich schwer öffnen. Erkläre eine mögliche Ursache. Wie kannst du beim Bau vorsorgen?');lines(5)
page('6','Muss dieses Holz weg');D.add_picture(str(OUT/'fehler.png'),width=Mm(170))
p('Vereinfachte Zeichnungen. Bild C zeigt ein Brett von der Seite über einer geraden Unterlage.')
h('6a Erkennen');p('Ordne zu: Riss · Ast · Verwerfen')
p('Bild A: ______________  Bild B: ______________  Bild C: ______________')
h('6b Erklären');p('Wähle einen Fehler. Beschreibe ein Problem, das dadurch bei einem Möbelstück entstehen kann.');lines(4)
h('6c Weiterdenken');p('Ein Brett hat einen kleinen, fest verwachsenen Ast. Muss es aussortiert werden? Begründe an einem Beispiel.');lines(4)
page('7','Berate eine Kundin');p('Eine Kundin braucht ein Schneidebrett. Sie benutzt es täglich. Es soll eine harte, glatte Oberfläche haben. Nach dem Abwaschen trocknet sie es sorgfältig.')
table(['Holzart','Eigenschaften und Grenzen'],[['Fichte','Weich, leicht, preiswert. Gut bearbeitbar. Druckstellen entstehen leicht.'],['Buche','Hart, fein und gleichmäßig strukturiert. Lässt sich glatt bearbeiten. Arbeitet stark bei wechselnder Feuchte.'],['Eiche','Hart, deutlich gemasert. Lässt sich glatt bearbeiten. Meist teurer; kann bei Kontakt mit Eisen und Feuchte dunkel verfärben.']],[1,4])
h('7a Erkennen');p('Nenne zwei wichtige Anforderungen aus dem Kundenauftrag.');lines(1)
h('7b Erklären');p('Wähle eine Holzart. Begründe mit drei passenden Eigenschaften. Nenne einen Nachteil.');lines(4)
h('7c Weiterdenken');p('Vergleiche deine Wahl mit einer anderen Holzart. Warum bleibst du bei deiner Wahl oder änderst sie?');lines(3)
D.save(OUT/'lernerfolgskontrolle.docx')
# Teacher edition, criteria and printable individual feedback.
D=Document();s=D.sections[0];s.page_width=Mm(210);s.page_height=Mm(297);s.top_margin=s.bottom_margin=Mm(18);s.left_margin=s.right_margin=Mm(20)
for name,size in [('Normal',11),('Title',23),('Heading 1',18),('Heading 2',13)]:
 st=D.styles[name];st.font.name='Arial';st.font.size=Pt(size);st.font.color.rgb=RGBColor(0,0,0);st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.15
 for b in list(st.element.findall('.//'+qn('w:pBdr'))):b.getparent().remove(b)
s.header.paragraphs[0].text='HBG  |  WP Technik 7  |  Lehrkraftmaterial'
f=s.footer.paragraphs[0];f.text='Erwartungshorizont Holz                                              ';fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
D.add_heading('Erwartungshorizont Holz',0)
p('Zur Lernerfolgskontrolle mit sieben Aufgabenblöcken und 60 Minuten Bearbeitungszeit. Teilaufgabe a erfasst den Mindeststandard, b den Regelstandard und c den Expertenstandard.')
p('Die Standards bauen fachlich aufeinander auf. Sie beschreiben einzelne Kompetenzen, keine festen Schülergruppen. Alle Kinder dürfen alle Teilaufgaben bearbeiten. Expertenaufgaben zählen hier zur Kontrolle; sie sind nicht die freiwilligen Vertiefungen des Lernwegs.')
h('Durchführung');p('Sieben Aufgabenblätter ausgeben. Etwa 50 Minuten für Aufgaben und 10 Minuten zum Lesen und Prüfen vorsehen. Mappe und Apps bleiben geschlossen. Die Materialauszüge auf dem Blatt sind erlaubt. Nachteilsausgleiche wie vereinbart berücksichtigen. Zeiten sind Planwerte und nach dem ersten Einsatz zu prüfen.')
h('Auswertung');p('Pro Teilaufgabe E = erreicht, T = teilweise erreicht, N = noch nicht erreicht eintragen. E bedeutet: Alle im Lösungsteil genannten Kernmerkmale sind enthalten. T bedeutet: Mindestens ein tragfähiger Bestandteil stimmt, aber die Antwort bleibt wesentlich unvollständig. N bedeutet: Kein tragfähiger Bestandteil, ein grundlegender Widerspruch oder keine Antwort. Bei Aufzählungen gelten die angegebenen Schwellen.')
p('Sinngemäße Antworten und fachlich passende Alternativen anerkennen. Rechtschreibung verändert den fachlichen Kompetenzstatus nicht, solange die Aussage verständlich bleibt. Folgefehler nicht mehrfach bewerten: Entscheidend ist auch die nachvollziehbare Begründung.')
p('Die Standards nicht zu einer pauschalen Niveaustufe verrechnen. Höhere Leistungen bleiben sichtbar, auch wenn Grundlagen lückenhaft sind. Dieses Raster enthält bewusst keinen Notenschlüssel; eine gegebenenfalls erforderliche Benotung ist vor dem Einsatz gesondert festzulegen.')
h('Ablage vor Reihenbeginn');p('Prüfung und Lösungen liegen vorläufig im öffentlichen Lehrkraft-Cockpit. Vor Reihenbeginn in das vorgesehene geschützte Dateisystem übertragen und die öffentlichen Dateien sowie Links entfernen. Auch Generator, ZIP-Paket und Abbildungen gehören zum Prüfungspaket. Bereits veröffentlichte Git-Versionen und frühere Deployments bleiben möglicherweise erreichbar. Für eine vertrauliche Prüfung daher vor dem Einsatz eine neue Aufgabenvariante ausschließlich im geschützten System erstellen.')
D.add_page_break();D.add_heading('Kompetenzraster',0)
rows=[['1 Stamm','Sechs Bereiche zuordnen','Kambium und Splintholz erklären','Folge einer Bastschädigung erklären'],['2 Jahresringe','Ringe zählen und Alter angeben','Ringbreite mit Wachstum verbinden','Ursache und sichere Aussage unterscheiden'],['3 Produktionsweg','Sechs Schritte ordnen','Einschnitt und Verschnitt erklären','Ausbeute und Brettmaß abwägen'],['4 Prüfen','Beobachtungen entnehmen','Härte aus Beobachtung ableiten','Vergleichsbedingungen beurteilen'],['5 Holz arbeitet','Quellen und Schwinden benennen','Trocknungsdaten erklären','Problem und Vorsorge übertragen'],['6 Holzfehler','Drei Fehler zuordnen','Technische Folge erklären','Verwendbarkeit abhängig vom Zweck beurteilen'],['7 Beratung','Anforderungen erkennen','Materialwahl begründen','Alternativen anhand gleicher Kriterien abwägen']]
table(['Kompetenz','Mindeststandard a','Regelstandard b','Expertenstandard c'],rows,[1.1,1.4,1.6,1.7],height=21)
p('Beleggrundlage: die jeweilige Teilaufgabe 1a bis 7c. Rückmeldung mit E, T oder N je Feld; keine automatische Gesamtstufe.')
solutions=[
('1 Aufbau des Stamms','a Mindeststandard: 1 Borke, 2 Bast, 3 Kambium, 4 Splintholz, 5 Kernholz, 6 Mark. E: sechs richtig; T: zwei bis fünf richtig; N: höchstens eine richtige Zuordnung.', 'b Regelstandard: Kambium bildet neue Zellen und ermöglicht Dickenwachstum. Splintholz transportiert Wasser und Mineralstoffe von den Wurzeln nach oben. E: beide Funktionen im Kern korrekt; T: nur eine Funktion korrekt oder beide erkennbar unvollständig.', 'c Expertenstandard: Der Bast transportiert Zucker aus den Blättern zu anderen Baumteilen. Eine ringförmige Unterbrechung beeinträchtigt die Versorgung, insbesondere der Wurzeln. E: Transportfunktion und Folge verbunden; T: Versorgungsschaden erkannt, aber Transport oder Zusammenhang unklar.'),
('2 Jahresringe lesen','a Mindeststandard: zwölf Jahresringe; ungefähr zwölf Jahre an dieser Schnittstelle. E: beides stimmt; T: Ringzählung mit einem Zählfehler und dazu passender Altersangabe oder nur eine der beiden Angaben.', 'b Regelstandard: Ring 8 zeigt geringeren Dickenzuwachs als die Nachbarringe. E: Dickenzuwachs und Vergleich genannt; T: nur allgemein „weniger gewachsen“. Keine Aussage über die Baumhöhe ableiten.', 'c Expertenstandard: Wassermangel ist möglich, aber nicht sicher aus der Ringbreite abzulesen. Auch Licht, Temperatur oder Konkurrenz kommen infrage. E: Unsicherheit begründet, etwa mit einer anderen Ursache; T: „nicht sicher“ oder mögliche andere Ursache ohne Erklärung.'),
('3 Vom Baum zum Brett','a Mindeststandard: Baum → Fällen → Transport → Sägewerk → Einschnitt → Schnittholz. E: vollständig richtig; T: überwiegend sinnvolle Abfolge mit mindestens drei richtigen direkten Nachbarschaften; N: weniger.', 'b Regelstandard: Beim Einschnitt wird der Stamm aufgesägt. Runde Randbereiche und die Schnittbreite des Sägeblatts führen zu Material, das nicht zu den vorgesehenen Brettern wird. E: Vorgang und mindestens eine schlüssige Verschnittursache; T: nur eines davon.', 'c Expertenstandard: Plan B; 14 cm erfüllen die Mindestbreite von 12 cm, 9 cm bei A nicht. Die höhere Ausbeute von A hilft bei diesem Auftrag nicht. E: Wahl mit Maßvergleich und Abwägung; T: B mit nur einer passenden Begründung.'),
('4 Holz prüfen','a Mindeststandard: Q hat die größere Masse. P hat die deutlichere Druckspur. E: beides korrekt; T: eine Angabe korrekt.', 'b Regelstandard: Q ist im Versuch härter, weil die Münze kaum eine Spur hinterlässt. E: Eigenschaft und passende Beobachtung verbunden; T: Q ohne Begründung. Eine größere Masse allein begründet keine Härte.', 'c Expertenstandard: Die größere Probe kann allein wegen ihres Volumens mehr wiegen. Gleich große und ähnlich trockene Proben vergleichen; alternativ Dichte bei vergleichbarer Feuchte bestimmen. E: Problem und passende Verbesserung; T: nur Problem oder Verbesserung.'),
('5 Quellen und Schwinden','a Mindeststandard: Quellen; Schwinden. E: beide Begriffe richtig; T: einer richtig.', 'b Regelstandard: Masse sinkt um 12 g, Breite um 1 mm. Wasserabgabe senkt die Masse; Wasserabgabe aus den Zellwänden kann Schwinden bewirken. E: beide Veränderungen mit zutreffender Erklärung; T: korrekte Veränderungen ohne Erklärung oder nur ein erklärter Zusammenhang. Die Zahlen der Differenzen sind nicht zwingend, wenn die Veränderungen eindeutig beschrieben sind.', 'c Expertenstandard: Aufnahme von Feuchtigkeit kann das Holz quellen lassen; dadurch kann die Schublade klemmen. Vorsorge: ausreichend Spiel für Bewegung oder passend getrocknetes Holz. E: Ursache, Klemmen und passende Vorsorge; T: nur Erklärung oder passende Vorsorge.'),
('6 Holzfehler beurteilen','a Mindeststandard: A Riss, B Ast, C Verwerfen. E: alle drei richtig; T: eine oder zwei richtige Zuordnungen.', 'b Regelstandard: Zum Beispiel Riss schwächt eine belastete Verbindung; verworfenes Brett liegt nicht plan auf; loser Ast kann herausfallen. E: Fehler, Produktbezug und konkrete technische Folge; T: plausible Folge ohne klaren Produktbezug. „Sieht schlecht aus“ allein genügt nicht.', 'c Expertenstandard: Nicht automatisch aussortieren. Ein fester Ast kann bei einer dekorativen Fläche akzeptabel sein; an einer belasteten Verbindung hängt die Eignung von Lage und Zustand ab. E: zweckbezogene Entscheidung mit Beispiel; T: bedingte Entscheidung ohne ausgeführtes Beispiel.'),
('7 Holzberatung','a Mindeststandard: Zwei Anforderungen aus dem Auftrag, etwa harte und glatte Oberfläche oder Eignung für tägliche Nutzung. E: zwei passende Anforderungen; T: eine.', 'b Regelstandard: Beispiel Buche: hart gegen Druckspuren, feine gleichmäßige Struktur, gut glatt bearbeitbar. Nachteil: arbeitet bei wechselnder Feuchte. E: begründete Wahl mit drei passenden Eigenschaften und einem Nachteil; T: grundsätzlich passende Wahl, aber unvollständige Begründung. Eiche ist bei schlüssiger Begründung ebenfalls möglich; Fichte erfüllt die geforderte Härte nicht.', 'c Expertenstandard: Beispiel Buche und Fichte: Beide bearbeitbar; Buche ist härter, Fichte preiswerter. Für den häufigen Gebrauch ist hier die Härte wichtiger. E: zwei Holzarten anhand mindestens eines gemeinsamen Kriteriums verglichen und Entscheidung abgewogen; T: Unterschied genannt, aber nicht für den Auftrag abgewogen.')]
for i,(title,a,b,c) in enumerate(solutions):
 if i%2==0:D.add_page_break()
 h(title)
 for txt in [a,b,c]:p(txt)
D.add_page_break();D.add_heading('Deine Rückmeldung',0);p('Name: ____________________________  Datum: ______________')
p('E = erreicht   T = teilweise erreicht   N = noch nicht erreicht')
table(['Kompetenz','Mindeststandard','Regelstandard','Expertenstandard'],[[r[0],'','',''] for r in rows],[1.3,1,1,1],height=12)
h('Das kannst du schon sicher');lines(3)
h('Dein nächster Lernschritt');p('Übe zuerst: _________________________  Auftrag: __________');p('Nutze U.1 für dein Ergebnis. Prüfe es danach mit einem Partner oder deiner Lehrkraft.');lines(2)
p('Passendes Material: 1 → A1 | 2 → A2 | 3 → A3/A4 | 4 → A5/A6 | 5 → A7 | 6 → A8 | 7 → A9/A10')
p('Rückblick: Das kann ich nach der Übung besser:');lines(2)
D.save(OUT/'erwartungshorizont.docx')
print('Zwei Dokumente erstellt.')
