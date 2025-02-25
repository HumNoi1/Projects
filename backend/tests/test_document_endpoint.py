# backend/tests/test_document_endpoint.py
import pytest
import os
from fastapi.testclient import TestClient
from main import app
from pathlib import Path
import tempfile
from unittest.mock import patch, AsyncMock, MagicMock

client = TestClient(app)

def test_upload_pdf_endpoint():
    # Create a simple test PDF
    pdf_content = b"%PDF-1.0\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n149\n%%EOF"

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_file.write(pdf_content)
        temp_path = Path(temp_file.name)

    try:
        # Mock the document processor and Path.unlink
        with patch('app.api.v1.endpoints.document.DocumentProcessor') as MockProcessor, \
             patch('pathlib.Path.unlink', return_value=None):
            processor_instance = MockProcessor.return_value
            processor_instance.process_pdf = AsyncMock(return_value={
                'success': True,
                'total_pages': 1,
                'embedding_ids': [1],
                'file_path': str(temp_path)
            })

            # Read file content
            with open(temp_path, 'rb') as f:
                file_content = f.read()

            # Make request
            response = client.post(
                "/api/v1/document/upload/pdf/",
                files={"file": ("test.pdf", file_content, "application/pdf")},
                params={"class_id": 1, "assignment_id": 2}
            )

            # Verify response
            assert response.status_code == 200
            # Add assertions for response content
    finally:
        # Try to clean up after test
        try:
            if temp_path.exists():
                os.chmod(temp_path, 0o666)
                temp_path.unlink()
        except:
            pass