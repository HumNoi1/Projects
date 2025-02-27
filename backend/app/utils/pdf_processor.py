# backend/app/utils/pdf_processor.py
from pypdf import PdfReader
import logging

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file.
    """
    try:
        logging.info(f"Extracting text from PDF: {file_path}")
        text = ""
        reader = PdfReader(file_path)
        
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text
            
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
        # ส่งคืนข้อความว่างแทนที่จะทำให้เกิดข้อผิดพลาด
        return "Error extracting text from PDF"