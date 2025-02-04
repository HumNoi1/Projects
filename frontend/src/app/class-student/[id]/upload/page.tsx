// frontend/app/grading/page.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { PDFViewer } from '@/components/grading/PDFViewer';
import { GradingResult } from '@/components/grading/GradingResult';
import { Loader2 } from 'lucide-react';

export default function GradingPage() {
  const [teacherFile, setTeacherFile] = useState<File | null>(null);
  const [studentFile, setStudentFile] = useState<File | null>(null);
  const [isGrading, setIsGrading] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [gradingResult, setGradingResult] = useState<any>(null);

  const handleStartGrading = async () => {
    if (!teacherFile || !studentFile) return;

    setIsGrading(true);
    try {
      // สร้าง FormData สำหรับส่งไฟล์
      const formData = new FormData();
      formData.append('teacher_file', teacherFile);
      formData.append('student_file', studentFile);

      // ส่งไฟล์ไปยัง API
      const response = await fetch('/api/v1/document', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setGradingResult(result);
    } catch (error) {
      console.error('Error grading files:', error);
      // TODO: แสดง error message
    } finally {
      setIsGrading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Grade Assignment</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PDFViewer
          title="Teacher's Answer Key"
          onFileSelect={(file) => setTeacherFile(file)} fileType={'teacher'} assignmentId={''} onFileUpload={function (): void {
            throw new Error('Function not implemented.');
          } }        />
        <PDFViewer
          title="Student's Submission"
          onFileSelect={(file) => setStudentFile(file)} fileType={'teacher'} assignmentId={''} onFileUpload={function (): void {
            throw new Error('Function not implemented.');
          } }        />
      </div>

      <div className="flex justify-center">
        <Button
          size="lg"
          disabled={!teacherFile || !studentFile || isGrading}
          onClick={handleStartGrading}
        >
          {isGrading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Start Grading
        </Button>
      </div>

      {gradingResult && (
        <GradingResult
          score={gradingResult.score}
          feedback={gradingResult.feedback}
          similarities={gradingResult.similarities}
        />
      )}
    </div>
  );
}