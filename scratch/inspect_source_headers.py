
from docx import Document
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dump_source_headers(path):
    doc = Document(path)
    print(f"--- SOURCE HEADERS: {path} ---")
    for para in doc.paragraphs:
        # Most headers have bold or specific styles, but let's just check for "Chapter" or numbered headers
        if para.text.strip() and (para.style.name.startswith('Heading') or para.text.upper().startswith('CHAPTER')):
            print(f"{para.style.name}: {para.text}")
    print(f"--- End SOURCE HEADERS ---")

dump_source_headers(r"C:\D_Drive\regime-platform\ppt\Regime_Shift_Detection_Report.docx")
