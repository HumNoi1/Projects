import os
from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file.
    """
    try:
        if not os.path.exists(file_path):
            return "File not found"
            
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return f"Error extracting text: {str(e)}"