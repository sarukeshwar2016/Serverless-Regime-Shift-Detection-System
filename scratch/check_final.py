
from docx import Document
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#checking the cicd
def check_final(path):
    doc = Document(path)
    print(f"--- FINAL REPORT CHECK: {path} ---")
    for i, para in enumerate(doc.paragraphs[:40]): # Check front matter
        if para.text.strip():
            print(f"P{i}: {para.text}")
    print(f"--- End CHECK ---")

check_final(r"C:\D_Drive\regime-platform\ppt\Final_Regime_Shift_Detection_Report.docx")
