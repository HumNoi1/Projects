// types/class.ts
export interface Class {
  id: string;
  name: string;
  subject: string;
  grade: string;
  description?: string;
  academic_year: string;
  teacher_id: string;
  active: boolean;
  created_at: string;
}

export interface ClassStudent {
  id: string;
  class_id: string;
  student_email: string;
  student_name: string;
  joined_at: string;
}

export interface ClassFormData {
  name: string;
  subject: string;
  grade: string;
  description?: string;
  academic_year: string;
  students: {
      email: string;
      name: string;
  }[];
}