
from docx import Document

def inspect_source(path):
    doc = Document(path)
    print(f"--- SOURCE: {path} ---")
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip():
            print(f"P{i}: {para.text[:100]}...") # Print first 100 chars
    print(f"--- End SOURCE ---")

inspect_source(r"C:\D_Drive\regime-platform\ppt\Regime_Shift_Detection_Report.docx")
