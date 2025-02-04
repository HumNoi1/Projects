// frontend/types/database.ts
export interface Teacher {
    id: string;
    email: string;
    full_name: string;
    department?: string;
    position?: string;
    created_at: string;
    updated_at: string;
  }
  
  export interface Assignment {
    id: string;
    title: string;
    description?: string;
    course_code: string;
    semester: string;
    academic_year: string;
    due_date?: string;
    max_score: number;
    rubric?: Record<string, string>;
    teacher_id: string;
    created_at: string;
    updated_at: string;
  }
  
  export interface FileRecord {
    id: string;
    file_name: string;
    file_path: string;
    file_type: 'answer_key' | 'submission';
    file_size: number;
    mime_type: string;
    assignment_id: string;
    student_id?: string;
    student_name?: string;
    uploaded_by: string;
    created_at: string;
    updated_at: string;
  }
  
  export interface GradingResult {
    id: string;
    assignment_id: string;
    student_id: string;
    student_name: string;
    submission_id: string;
    score: number;
    feedback?: string;
    rubric_scores?: Record<string, number>;
    graded_by: string;
    graded_at: string;
    created_at: string;
    updated_at: string;
  }