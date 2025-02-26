// frontend/app/assignments/[id]/results/page.tsx
'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '../../../../components/ui/button';
import { FeedbackDisplay } from '../../../../components/grading/feedback-display';
import { GradingResponse } from '../../../../lib/types/grading';

interface ResultsPageProps {
  params: {
    id: string;
  };
}

export default function ResultsPage({ params }: ResultsPageProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const studentId = searchParams.get('student_id');
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [gradingResult, setGradingResult] = useState<GradingResponse | null>(null);

  useEffect(() => {
    if (!studentId) {
      setError('ไม่พบรหัสนักเรียน');
      setIsLoading(false);
      return;
    }

    const fetchResults = async () => {
      try {
        // This is a mock function, as we don't have an actual endpoint for this in the provided backend files
        // In a real implementation, you would call the appropriate API endpoint
        const { gradeSubmission } = await import('../../../../lib/api/grading');
        const result = await gradeSubmission(params.id, { student_id: studentId });
        setGradingResult(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [params.id, studentId]);

  if (isLoading) {
    return (
      <div className="py-6 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-3 text-gray-600">กำลังโหลดผลการตรวจ...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-6">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
        <div className="mt-4 text-center">
          <Button onClick={() => router.back()}>กลับ</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="py-6">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">ผลการตรวจงาน</h1>
      
      {gradingResult ? (
        <div className="bg-white shadow rounded-lg p-6">
          <FeedbackDisplay gradingResult={gradingResult} />
          
          <div className="mt-6 flex justify-end">
            <Button onClick={() => router.back()}>
              กลับ
            </Button>
          </div>
        </div>
      ) : (
        <div className="text-center py-10">
          <p className="text-gray-500">ไม่พบผลการตรวจงาน</p>
          <div className="mt-4">
            <Button onClick={() => router.back()}>
              กลับ
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}