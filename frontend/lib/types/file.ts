  // frontend/lib/types/file.ts
  export interface FileRecord {
    id: string;
    file_name: string;
    file_path: string;
    file_type: 'teacher' | 'student';
    file_size: number;
    mime_type: string;
    assignment_id: string;
    text_content: string;
    created_at: string;
  }