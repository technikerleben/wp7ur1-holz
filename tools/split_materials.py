"""Split the verified 16-page mappe PDF into cockpit downloads."""
from pathlib import Path
from pypdf import PdfReader, PdfWriter
root = Path(__file__).resolve().parents[1] / 'materialien'
source = PdfReader(root / 'holzforscher-mappe.pdf')
assert len(source.pages) == 16, 'Verify pagination before splitting.'
parts = {'deckblatt':[0], 'lernweg-uebersicht':[1], **{f'a{i}':[i+1] for i in range(1,7)}, 'a7':[8,9], 'a8':[10], 'a9':[11], 'a10':[12], 'kompetenzcheck-papier':[13], 'uebung':[14], 'vertiefung':[15]}
for name, pages in parts.items():
    writer = PdfWriter()
    for page in pages: writer.add_page(source.pages[page])
    writer.write(root / f'{name}.pdf')
print(f'{len(parts)} Einzelmaterialien erstellt.')
