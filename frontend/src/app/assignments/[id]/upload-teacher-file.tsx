// frontend/app/assignments/[id]/upload-teacher-file.tsx
'use client';

import React, { useState } from 'react';
import { UploadForm } from '../../../components/ui/forms/upload-form';
import { FileRecord } from '../../../lib/types/file';

interface UploadTeacherFileProps {
  assignmentId: string;
}

export const UploadTeacherFile: React.FC<UploadTeacherFileProps> = ({ assignmentId }) => {
  const [fileRecord, setFileRecord] = useState<FileRecord | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUploadSuccess = (record: FileRecord) => {
    setFileRecord(record);
    setError(null);
  };

  const handleUploadError = (err: Error) => {
    setError(err.message);
  };

  return (
    <div className="bg-white shadow-sm rounded-lg p-6">
      {fileRecord ? (
        <div className="text-sm text-gray-600">
          <div className="flex items-center mb-4">
            <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <span className="font-medium">อัปโหลดไฟล์เฉลยสำเร็จ</span>
          </div>
          <p>ชื่อไฟล์: {fileRecord.file_name}</p>
          <p>ขนาดไฟล์: {(fileRecord.file_size / 1024).toFixed(2)} KB</p>
          <button
            onClick={() => setFileRecord(null)}
            className="mt-3 text-sm text-blue-600 hover:text-blue-800"
          >
            อัปโหลดไฟล์ใหม่
          </button>
        </div>
      ) : (
        <>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          <UploadForm
            fileType="teacher"
            assignmentId={assignmentId}
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />
        </>
      )}
    </div>
  );
};