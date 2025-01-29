# tests/fixtures/create_sample_pdf.py
from fpdf import FPDF

def create_sample_pdf():
    pdf = FPDF()
    
    # หน้าที่ 1
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a sample PDF document", ln=1, align='C')
    pdf.multi_cell(0, 10, txt="This is the first page with some sample content.")
    
    # หน้าที่ 2
    pdf.add_page()
    pdf.cell(200, 10, txt="Page 2", ln=1, align='C')
    pdf.multi_cell(0, 10, txt="This is the second page with different content.")
    
    # บันทึกไฟล์
    pdf.output("tests/fixtures/sample.pdf")

if __name__ == "__main__":
    create_sample_pdf()