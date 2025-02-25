from unittest.mock import MagicMock, patch
import pytest
import asyncio
from pathlib import Path
from app.services.pdf_service import PDFService
import tempfile

@pytest.mark.asyncio
async def test_extract_text():
    # Create a simple test PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_path = Path(temp_file.name)
    
    try:
        # This test needs a real PDF file to work
        # For a real test, you would create a PDF file with known content
        # For this example, we'll mock the fitz functionality
        
        with patch('fitz.open') as mock_fitz:
            mock_doc = MagicMock()
            mock_page = MagicMock()
            mock_page.get_text.return_value = "Test PDF content"
            mock_doc.__len__.return_value = 1
            mock_doc.__getitem__.return_value = mock_page
            mock_fitz.return_value = mock_doc
            
            service = PDFService()
            result = await service.extract_text(temp_path)
            
            assert len(result) == 1
            assert result[0]['content'] == "Test PDF content"
            assert result[0]['metadata']['page_number'] == 1
            assert result[0]['metadata']['total_pages'] == 1
    finally:
        # Clean up
        temp_path.unlink(missing_ok=True)