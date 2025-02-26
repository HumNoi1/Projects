// frontend/lib/api/files.ts
import { FileRecord } from '../types/file';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

export async function uploadFile(
  file: File,
  fileType: 'teacher' | 'student',
  assignmentId: string
): Promise<FileRecord> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', fileType);
  formData.append('assignment_id', assignmentId);

  const response = await fetch(`${API_URL}/files`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to upload file');
  }

  return response.json();
}