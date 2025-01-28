// types/class.ts
export interface Class {
    id: number
    name: string
    students: number
    assignments: number
    averageScore: number
    teacher: string
    lastActive: string
  }

export interface ClassFormData {
  name: string;
  subject: string;
  grade: string;
  academicYear: string;
  description?: string;
  students: {
    email: string;
    name: string;
  }[];
}