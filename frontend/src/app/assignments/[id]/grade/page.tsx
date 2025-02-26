// frontend/app/assignments/[id]/grade/page.tsx
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '../../../../components/ui/button';
import { FeedbackDisplay } from '../../../../components/grading/feedback-display';
import { GradingResponse } from '../../../../lib/types/grading';

interface GradePageProps {
  params: {
    id: string;
  };
}

export default function GradePage({ params }: GradePageProps) {
  const router = useRouter();
  const [studentId, setStudentId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [gradingResult, setGradingResult] = useState<GradingResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      const { gradeSubmission } = await import('../../../../lib/api/grading');
      const result = await gradeSubmission(params.id, { student_id: studentId });
      setGradingResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="py-6">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">ตรวจงาน</h1>
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      {!gradingResult ? (
        <div className="bg-white shadow rounded-lg p-6">
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="studentId" className="block text-sm font-medium text-gray-700">
                รหัสนักเรียน
              </label>
              <input
                type="text"
                id="studentId"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            
            <div className="flex justify-end">
              <Button
                type="button"
                variant="secondary"
                onClick={() => router.back()}
                className="mr-3"
              >
                ยกเลิก
              </Button>
              <Button
                type="submit"
                isLoading={isLoading}
                disabled={!studentId || isLoading}
              >
                ตรวจงาน
              </Button>
            </div>
          </form>
        </div>
      ) : (
        <div className="bg-white shadow rounded-lg p-6">
          <FeedbackDisplay gradingResult={gradingResult} />
          
          <div className="mt-6 flex justify-end">
            <Button
              variant="secondary"
              onClick={() => setGradingResult(null)}
              className="mr-3"
            >
              ตรวจงานชิ้นอื่น
            </Button>
            <Button onClick={() => router.back()}>
              เสร็จสิ้น
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}