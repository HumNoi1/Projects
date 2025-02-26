// frontend/app/batch-grading/page.tsx
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '../../components/ui/button';
import { Assignment } from '../../lib/types/assignment';

export default function BatchGradingPage() {
  const router = useRouter();
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAssignment, setSelectedAssignment] = useState<string>('');
  const [teacherFile, setTeacherFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const { getAssignments } = await import('../../lib/api/assignments');
        const data = await getAssignments();
        setAssignments(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAssignments();
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setTeacherFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedAssignment || !teacherFile) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const { createBatchGrading } = await import('../../lib/api/batch-grading');
      const result = await createBatchGrading(teacherFile, selectedAssignment);
      router.push(`/batch-grading/${result.batch_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="py-6 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-3 text-gray-600">กำลังโหลดข้อมูล...</p>
      </div>
    );
  }

  return (
    <div className="py-6">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">ตรวจงานแบบกลุ่ม</h1>
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      <div className="bg-white shadow rounded-lg p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="assignment" className="block text-sm font-medium text-gray-700">
              เลือกงาน
            </label>
            <select
              id="assignment"
              value={selectedAssignment}
              onChange={(e) => setSelectedAssignment(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
              required
            >
              <option value="">-- เลือกงาน --</option>
              {assignments.map((assignment) => (
                <option key={assignment.id} value={assignment.id}>
                  {assignment.title}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label htmlFor="teacher-file" className="block text-sm font-medium text-gray-700">
              อัปโหลดไฟล์เฉลย
            </label>
            <div className="mt-1">
              <input
                id="teacher-file"
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500
                       file:mr-4 file:py-2 file:px-4
                       file:rounded-md file:border-0
                       file:text-sm file:font-semibold
                       file:bg-blue-50 file:text-blue-700
                       hover:file:bg-blue-100"
                required
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">
              รองรับเฉพาะไฟล์ PDF เท่านั้น
            </p>
          </div>
          
          <div className="flex justify-end">
            <Button
              type="submit"
              isLoading={isSubmitting}
              disabled={!selectedAssignment || !teacherFile || isSubmitting}
            >
              เริ่มตรวจงานแบบกลุ่ม
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}