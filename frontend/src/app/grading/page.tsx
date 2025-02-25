// frontend/src/app/grading/page.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { PDFViewer } from '@/components/grading/PDFViewer';
import { Loader2 } from 'lucide-react';
import { GradingResult } from '@/components/grading/GradingResult';
import { GradingService } from '@/services/api';

export default function GradingPage() {
  const [teacherFile, setTeacherFile] = useState<File | null>(null);
  const [studentFile, setStudentFile] = useState<File | null>(null);
  const [isGrading, setIsGrading] = useState(false);
  const [gradingResult, setGradingResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // สร้าง ID สำหรับการทดสอบ (ในระบบจริงอาจดึงจาก URL params)
  const assignmentId = "test-assignment-1";

  const handleStartGrading = async () => {
    if (!teacherFile || !studentFile) return;

    setIsGrading(true);
    setError(null);
    
    try {
      // เรียกใช้ API เพื่อให้คะแนน
      const result = await GradingService.gradeAssignment(
        "Student answer extracted from PDF", // ในระบบจริงควรดึงข้อมูลจากไฟล์ที่อัปโหลดไว้
        "Reference answer extracted from PDF", // ในระบบจริงควรดึงข้อมูลจากไฟล์ที่อัปโหลดไว้
        {
          "Content": {
            "weight": 40,
            "criteria": "Evaluates understanding of concepts"
          },
          "Clarity": {
            "weight": 30,
            "criteria": "Clear expression of ideas"
          }
        }
      );
      
      setGradingResult(result.grading_result);
    } catch (error) {
      console.error('Error grading assignments:', error);
      setError(error instanceof Error ? error.message : 'An unknown error occurred');
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
          fileType="teacher"
          assignmentId={assignmentId}
          onFileUpload={(file) => setTeacherFile(file)}
        />
        <PDFViewer
          title="Student's Submission"
          fileType="student"
          assignmentId={assignmentId}
          onFileUpload={(file) => setStudentFile(file)}
        />
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>{error}</p>
        </div>
      )}

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
          similarities={gradingResult.similarities || []}
        />
      )}
    </div>
  );
}