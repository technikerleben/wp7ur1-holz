from pathlib import Path
import re
from pypdf import PdfReader,PdfWriter
out=Path(__file__).resolve().parents[1]/'materialien/offener-anfang'
r=PdfReader(out/'spielkarten-offener-anfang.pdf');assert len(r.pages)==12
for w in range(6):
 a,b=r.pages[w*2:w*2+2];expected=[f'S{w*2+1:02}',f'S{w*2+2:02}']
 assert re.findall(r'S\d{2}',a.extract_text())==expected
 assert re.findall(r'S\d{2}',b.extract_text())==expected
 assert 'VORDERSEITE AUFGABEN' in a.extract_text() and 'RÜCKSEITE LÖSUNGEN' in b.extract_text()
 writer=PdfWriter();writer.add_page(a);writer.add_page(b);writer.write(out/f'woche-{w+1}.pdf')
print('6 Wochenpakete; Vorder- und Rückseiten stimmen überein.')
