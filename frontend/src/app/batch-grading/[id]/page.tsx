// frontend/app/batch-grading/[id]/page.tsx
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '../../../components/ui/button';
import { FileRecord } from '../../../lib/types/file';

interface BatchGradingDetailPageProps {
  params: {
    id: string;
  };
}

export default function BatchGradingDetailPage({ params }: BatchGradingDetailPageProps) {
  const router = useRouter();
  const [files, setFiles] = useState<FileRecord[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isPolling, setIsPolling] = useState(false);
  const [batchCompleted, setBatchCompleted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // This is a mock function, as we don't have an actual endpoint for this in the provided backend files
  const fetchStudentFiles = async () => {
    // In a real implementation, you would call the appropriate API endpoint
    return new Promise<FileRecord[]>((resolve) => {
      // Simulating API response
      setTimeout(() => {
        resolve([
          {
            id: 'file1',
            file_name: 'student1_submission.pdf',
            file_path: '/path/to/file1',
            file_type: 'student',
            file_size: 1024,
            mime_type: 'application/pdf',
            assignment_id: 'assignment1',
            text_content: 'Sample content',
            created_at: new Date().toISOString(),
          },
          {
            id: 'file2',
            file_name: 'student2_submission.pdf',
            file_path: '/path/to/file2',
            file_type: 'student',
            file_size: 2048,
            mime_type: 'application/pdf',
            assignment_id: 'assignment1',
            text_content: 'Sample content',
            created_at: new Date().toISOString(),
          },
        ]);
      }, 1000);
    });
  };

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const data = await fetchStudentFiles();
        setFiles(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
      } finally {
        setIsLoading(false);
      }
    };

    fetchFiles();
  }, [params.id]);

  const handleCheckboxChange = (fileId: string) => {
    setSelectedFiles((prev) => {
      if (prev.includes(fileId)) {
        return prev.filter((id) => id !== fileId);
      } else {
        return [...prev, fileId];
      }
    });
  };

  const handleSelectAll = () => {
    if (selectedFiles.length === files.length) {
      setSelectedFiles([]);
    } else {
      setSelectedFiles(files.map((file) => file.id));
    }
  };

  const handleSubmit = async () => {
    if (selectedFiles.length === 0) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const { addStudentsToBatch } = await import('../../../lib/api/batch-grading');
      await addStudentsToBatch(params.id, selectedFiles);
      
      // Start polling for results
      setIsPolling(true);
      pollForResults();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
      setIsSubmitting(false);
    }
  };

  const pollForResults = async () => {
    try {
      const { getBatchResults } = await import('../../../lib/api/batch-grading');
      const result = await getBatchResults(params.id);
      
      if (result.completed) {
        setBatchCompleted(true);
        setIsPolling(false);
      } else {
        // Poll again after 3 seconds
        setTimeout(pollForResults, 3000);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'เกิดข้อผิดพลาดในการตรวจสอบสถานะ');
      setIsPolling(false);
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

  if (isPolling || batchCompleted) {
    return (
      <div className="py-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">สถานะการตรวจงานแบบกลุ่ม</h1>
        
        <div className="bg-white shadow rounded-lg p-6 text-center">
          {isPolling ? (
            <>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-lg font-medium text-gray-900">กำลังตรวจงาน...</p>
              <p className="mt-2 text-gray-600">ระบบกำลังตรวจงานทั้งหมด {selectedFiles.length} ชิ้น</p>
            </>
          ) : (
            <>
              <div className="text-green-500 mx-auto mb-4">
                <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <p className="mt-2 text-lg font-medium text-gray-900">การตรวจงานเสร็จสิ้น</p>
              <p className="mt-2 text-gray-600">ตรวจงานทั้งหมด {selectedFiles.length} ชิ้นเรียบร้อยแล้ว</p>
              <div className="mt-6">
                <Button onClick={() => router.push(`/batch-grading/${params.id}/results`)}>
                  ดูผลการตรวจ
                </Button>
              </div>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="py-6">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">เลือกงานนักเรียนที่ต้องการตรวจ</h1>
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}
      
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex justify-between items-center mb-4">
            <button
              type="button"
              onClick={handleSelectAll}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              {selectedFiles.length === files.length ? 'ยกเลิกทั้งหมด' : 'เลือกทั้งหมด'}
            </button>
            <span className="text-sm text-gray-500">
              เลือก {selectedFiles.length} จาก {files.length} ไฟล์
            </span>
          </div>
          
          <div className="border rounded-md overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    <input
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      checked={selectedFiles.length === files.length && files.length > 0}
                      onChange={handleSelectAll}
                    />
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ชื่อไฟล์
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ขนาด
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    วันที่อัปโหลด
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {files.map((file) => (
                  <tr key={file.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="checkbox"
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        checked={selectedFiles.includes(file.id)}
                        onChange={() => handleCheckboxChange(file.id)}
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {file.file_name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">
                        {(file.file_size / 1024).toFixed(2)} KB
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">
                        {new Date(file.created_at).toLocaleDateString('th-TH')}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="mt-6 flex justify-end">
            <Button
              variant="secondary"
              onClick={() => router.back()}
              className="mr-3"
            >
              ยกเลิก
            </Button>
            <Button
              onClick={handleSubmit}
              isLoading={isSubmitting}
              disabled={selectedFiles.length === 0 || isSubmitting}
            >
              เริ่มตรวจงาน ({selectedFiles.length} ชิ้น)
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}