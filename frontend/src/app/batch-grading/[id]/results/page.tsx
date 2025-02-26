// frontend/app/batch-grading/[id]/results/page.tsx
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '../../../../components/ui/button';
import { GradingResponse } from '../../../../lib/types/grading';

interface ResultsPageProps {
  params: {
    id: string;
  };
}

export default function ResultsPage({ params }: ResultsPageProps) {
  const router = useRouter();
  const [results, setResults] = useState<GradingResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const { getBatchResults } = await import('../../../../lib/api/batch-grading');
        const data = await getBatchResults(params.id);
        setResults(data.results);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [params.id]);

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

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
          <Button onClick={() => router.push('/batch-grading')}>กลับไปหน้าตรวจงานแบบกลุ่ม</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="py-6">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">ผลการตรวจงานแบบกลุ่ม</h1>
      
      {results.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-gray-500">ยังไม่มีผลการตรวจงาน</p>
          <div className="mt-4">
            <Button onClick={() => router.push('/batch-grading')}>กลับไปหน้าตรวจงานแบบกลุ่ม</Button>
          </div>
        </div>
      ) : (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <div className="px-4 py-5 sm:p-6">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      รหัสนักเรียน
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      คะแนน
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      จุดเด่น
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      จุดที่ควรปรับปรุง
                    </th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      การดำเนินการ
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {results.map((result) => (
                    <tr key={result.student_id}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {result.student_id}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className={`text-sm font-bold ${getScoreColor(result.score)}`}>
                          {result.score}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <ul className="text-sm text-gray-900 list-disc list-inside">
                          {result.strengths.slice(0, 2).map((strength, index) => (
                            <li key={index} className="truncate max-w-xs">{strength}</li>
                          ))}
                          {result.strengths.length > 2 && (
                            <li className="text-gray-500">และอีก {result.strengths.length - 2} ข้อ</li>
                          )}
                        </ul>
                      </td>
                      <td className="px-6 py-4">
                        <ul className="text-sm text-gray-900 list-disc list-inside">
                          {result.areas_for_improvement.slice(0, 2).map((area, index) => (
                            <li key={index} className="truncate max-w-xs">{area}</li>
                          ))}
                          {result.areas_for_improvement.length > 2 && (
                            <li className="text-gray-500">และอีก {result.areas_for_improvement.length - 2} ข้อ</li>
                          )}
                        </ul>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => router.push(`/assignments/${result.assignment_id}/results?student_id=${result.student_id}`)}
                          className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                        >
                          ดูรายละเอียด
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="mt-6 flex justify-end">
              <Button onClick={() => router.push('/batch-grading')}>
                เสร็จสิ้น
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}