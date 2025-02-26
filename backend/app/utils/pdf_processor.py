from pypdf import PdfReader
import os

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        reader = PdfReader(file_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""