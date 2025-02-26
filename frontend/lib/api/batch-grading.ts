// frontend/lib/api/batch-grading.ts
import { BatchGradingResponse } from '../types/grading';

export async function createBatchGrading(
  teacherFile: File,
  assignmentId: string
): Promise<{ batch_id: string; success: boolean; message: string }> {
  const formData = new FormData();
  formData.append('teacher_file', teacherFile);
  formData.append('assignment_id', assignmentId);

  const response = await fetch(`${API_URL}/batch-grading`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create batch grading');
  }

  return response.json();
}

export async function addStudentsToBatch(
  batchId: string,
  studentFileIds: string[]
): Promise<{ success: boolean; message: string; batch_id: string }> {
  const response = await fetch(`${API_URL}/batch-grading/${batchId}/students`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ student_file_ids: studentFileIds }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to add students to batch');
  }

  return response.json();
}

export async function getBatchResults(
  batchId: string
): Promise<BatchGradingResponse> {
  const response = await fetch(`${API_URL}/batch-grading/${batchId}/results`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get batch results');
  }

  return response.json();
}