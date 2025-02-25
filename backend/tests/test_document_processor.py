# backend/tests/test_document_processor.py
import pytest
from app.services.document_processor import DocumentProcessor
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_process_pdf():
    # Mock data
    mock_pages = [
        {
            'content': 'Page 1 content',
            'metadata': {'page_number': 1, 'total_pages': 2}
        },
        {
            'content': 'Page 2 content',
            'metadata': {'page_number': 2, 'total_pages': 2}
        }
    ]
    
    mock_embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    mock_ids = [1, 2]
    
    # Create mocks
    with patch('app.services.document_processor.PDFService') as MockPDFService, \
         patch('app.services.document_processor.EmbeddingService') as MockEmbeddingService:
        
        # Setup PDF service mock
        pdf_instance = MockPDFService.return_value
        pdf_instance.extract_text = AsyncMock(return_value=mock_pages)
        
        # Setup embedding service mock
        embedding_instance = MockEmbeddingService.return_value
        embedding_instance.create_embeddings = AsyncMock(return_value=mock_embeddings)
        embedding_instance.store_embeddings = AsyncMock(return_value=mock_ids)
        
        # Test
        processor = DocumentProcessor()
        result = await processor.process_pdf(
            Path('test.pdf'),
            {'assignment_id': '123'}
        )
        
        # Verify
        assert result['success'] == True
        assert result['total_pages'] == 2
        assert result['embedding_ids'] == mock_ids
        pdf_instance.extract_text.assert_called_once()
        embedding_instance.create_embeddings.assert_called_once()
        embedding_instance.store_embeddings.assert_called_once()