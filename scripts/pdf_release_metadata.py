"""Apply author/title/language metadata without editing PDF page content."""
from pathlib import Path
import fitz

def set_pdf_info(pdf_path, title, subject='', keywords=''):
    p=Path(pdf_path)
    temp=p.with_suffix('.release-info.pdf')
    with fitz.open(p) as pdf:
        metadata=pdf.metadata.copy()
        metadata.update({'title':title,'author':'H','subject':subject,
                         'creator':'The Book of Chance publishing system',
                         'keywords':keywords or 'Confluent Humanism, Fellowship of Chance'})
        pdf.set_metadata(metadata)
        pdf.xref_set_key(pdf.pdf_catalog(),'Lang','(en-NZ)')
        pdf.save(temp,garbage=4,deflate=True)
    temp.replace(p)
