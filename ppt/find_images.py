import sys
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document

doc = Document(r'C:\D_Drive\regime-platform\ppt\ExpenseIQ A Smart Expense Management System.docx')
for i, p in enumerate(doc.paragraphs):
    images = sum(1 for r in p.runs if 'graphic' in r._element.xml)
    if images > 0:
        print(f'Paragraph {i}: {len(p.runs)} runs, {images} images. Text: {p.text[:50]}')
