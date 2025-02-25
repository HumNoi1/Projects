// frontend/src/services/api.ts
import { ENDPOINTS } from '@/config/api';

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse(response: Response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(
      response.status,
      errorData.detail || `Error: ${response.status} ${response.statusText}`
    );
  }
  return response.json();
}

export const GradingService = {
  async gradeAssignment(studentAnswer: string, referenceAnswer: string, rubric: any) {
    const response = await fetch(ENDPOINTS.GRADING, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        student_answer: studentAnswer,
        reference_answer: referenceAnswer,
        rubric: rubric,
      }),
    });
    
    return handleResponse(response);
  },
  
  async uploadDocument(file: File, fileType: 'teacher' | 'student', assignmentId: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', fileType);
    formData.append('assignment_id', assignmentId);
    
    const response = await fetch(ENDPOINTS.DOCUMENT_UPLOAD, {
      method: 'POST',
      body: formData,
    });
    
    return handleResponse(response);
  },

  async gradeFromPDF(teacherFile: File, studentFile: File, rubric: any) {
    const formData = new FormData();
    formData.append('teacher_file', teacherFile);
    formData.append('student_file', studentFile);
    formData.append('rubric', JSON.stringify(rubric));

    const response = await fetch(`${ENDPOINTS.GRADING}/grade-pdf`, {
      method: 'POST',
      body: formData,
    });

    return handleResponse(response);
  }
};

export const HealthService = {
  async checkStatus() {
    const response = await fetch(ENDPOINTS.HEALTH);
    return handleResponse(response);
  }
};