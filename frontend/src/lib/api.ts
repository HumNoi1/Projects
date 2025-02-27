// frontend/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

// สร้าง Error Class สำหรับ API
export class ApiError extends Error {
  status: number;
  
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

// ฟังก์ชันสำหรับเรียก API
async function fetchApi<T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new ApiError(
      error.detail || `API Error: ${res.status} ${res.statusText}`,
      res.status
    );
  }

  return res.json();
}

// ฟังก์ชันสำหรับอัปโหลดไฟล์
export async function uploadFile(
  file: File,
  fileType: 'teacher' | 'student',
  assignmentId: string
) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', fileType);
  formData.append('assignment_id', assignmentId);

  const res = await fetch(`${API_BASE_URL}/files`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new ApiError(
      error.detail || `Upload failed: ${res.status} ${res.statusText}`,
      res.status
    );
  }

  return res.json();
}

// ฟังก์ชันสำหรับตรวจงานนักเรียน
export async function gradeSubmission(
  assignmentId: string,
  studentId: string
) {
  return fetchApi(`/grading/${assignmentId}`, {
    method: 'POST',
    body: JSON.stringify({
      student_id: studentId,
    }),
  });
}

// ฟังก์ชันสำหรับเริ่มการตรวจงานแบบกลุ่ม
export async function startBatchGrading(
  teacherFile: File,
  assignmentId: string
) {
  const formData = new FormData();
  formData.append('teacher_file', teacherFile);
  formData.append('assignment_id', assignmentId);

  const res = await fetch(`${API_BASE_URL}batch-grading`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new ApiError(
      error.detail || `Batch grading failed: ${res.status} ${res.statusText}`,
      res.status
    );
  }

  return res.json();
}

// ฟังก์ชันสำหรับเพิ่มนักเรียนในการตรวจงานแบบกลุ่ม
export async function addStudentsToBatch(
  batchId: string,
  studentFileIds: string[]
) {
  return fetchApi(`/batch-grading/${batchId}/students`, {
    method: 'POST',
    body: JSON.stringify({
      student_file_ids: studentFileIds,
    }),
  });
}

// ฟังก์ชันสำหรับดึงผลการตรวจงานแบบกลุ่ม
export async function getBatchResults(batchId: string) {
  return fetchApi(`/batch-grading/${batchId}/results`);
}