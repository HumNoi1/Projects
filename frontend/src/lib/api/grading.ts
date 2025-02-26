import { GradingRequest, GradingResponse } from '../types/grading';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function gradeSubmission(
  assignmentId: string,
  gradingRequest: GradingRequest
): Promise<GradingResponse> {
  const response = await fetch(`${API_URL}/grading/${assignmentId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(gradingRequest),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to grade submission');
  }

  return response.json();
}