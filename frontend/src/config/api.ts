// frontend/src/config/api.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
export const API_V1 = `${API_BASE_URL}/api/v1`;

export const ENDPOINTS = {
  GRADING: `${API_V1}/grading/grade`,
  DOCUMENT_UPLOAD: `${API_V1}/document/upload/pdf`,
  HEALTH: `${API_V1}/health`,
};