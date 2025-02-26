// frontend/app/assignments/[id]/submit/page.tsx
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { UploadForm } from '../../../../components/ui/forms/upload-form';
import { FileRecord } from '../../../../lib/types/file';
import { Button } from '../../../../components/ui/button';

interface SubmitPageProps {
  params: {
    id: string;
  };
}

export default function SubmitPage({ params }: SubmitPageProps) {
  const router = useRouter();
  const [studentId, setStudentId] = useState('');
  const [fileRecord, setFileRecord] = useState<FileRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleUploadSuccess = (record: FileRecord) => {
    setFileRecord(record);
    setError(null);
  };

  const handleUploadError = (err: Error) => {
    setError(err.message);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!fileRecord) {
      setError('กรุณาอัปโหลดไฟล์งานก่อน');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const { gradeSubmission } = await import('../../../../lib/api/grading');
      // Simply await the function call without storing the unused result
      await gradeSubmission(params.id, { student_id: studentId });
      router.push(`/assignments/${params.id}/results?student_id=${studentId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="py-6">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">ส่งงาน</h1>
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      <div className="bg-white shadow rounded-lg p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
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
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              ไฟล์งาน
            </label>
            
            {fileRecord ? (
              <div className="bg-gray-50 p-4 rounded-md">
                <div className="flex items-center mb-2">
                  <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span className="font-medium">อัปโหลดไฟล์สำเร็จ</span>
                </div>
                <p className="text-sm text-gray-600">ชื่อไฟล์: {fileRecord.file_name}</p>
                <p className="text-sm text-gray-600">ขนาดไฟล์: {(fileRecord.file_size / 1024).toFixed(2)} KB</p>
                <button
                  type="button"
                  onClick={() => setFileRecord(null)}
                  className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                  อัปโหลดไฟล์ใหม่
                </button>
              </div>
            ) : (
              <UploadForm
                fileType="student"
                assignmentId={params.id}
                onUploadSuccess={handleUploadSuccess}
                onUploadError={handleUploadError}
              />
            )}
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
              isLoading={isSubmitting}
              disabled={!fileRecord || !studentId || isSubmitting}
            >
              ส่งงานและตรวจอัตโนมัติ
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}