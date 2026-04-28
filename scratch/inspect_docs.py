
from docx import Document
import sys

def dump_docx(path, label):
    try:
        doc = Document(path)
        print(f"--- {label}: {path} ---")
        for i, para in enumerate(doc.paragraphs[:50]): # First 50 paragraphs
            if para.text.strip():
                print(f"P{i}: {para.text}")
        print(f"--- End {label} ---")
    except Exception as e:
        print(f"Error reading {path}: {e}")

dump_docx(r"C:\D_Drive\regime-platform\ppt\Regime_Shift_Detection_Report.docx", "SOURCE")
dump_docx(r"C:\D_Drive\regime-platform\ppt\Project Report template.docx", "TEMPLATE")
