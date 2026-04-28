
from docx import Document
import sys

# Set encoding for print
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dump_template_full(path):
    doc = Document(path)
    print(f"--- TEMPLATE: {path} ---")
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip():
            print(f"P{i}: {para.text[:120]}")
    print(f"--- End TEMPLATE ---")

dump_template_full(r"C:\D_Drive\regime-platform\ppt\Project Report template.docx")
