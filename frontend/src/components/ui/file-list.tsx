// frontend/components/ui/file-list.tsx
'use client';

import { useState } from 'react';
import { FileText, Check, X, Loader2 } from 'lucide-react';
import { gradeSubmission } from '@/lib/api';

interface FileListProps {
  files: Array<{
    id: string;
    file_name: string;
    created_at: string;
    student_id?: string;
    graded?: boolean;
    score?: number;
  }>;
  fileType: 'teacher' | 'student';
  assignmentId: string;
}

export default function FileList({ files, fileType, assignmentId }: FileListProps) {
  const [gradingFile, setGradingFile] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [gradedResults, setGradedResults] = useState<Record<string, any>>({});

  const handleGradeSubmission = async (fileId: string, studentId: string) => {
    setGradingFile(fileId);
    setError(null);
    
    try {
      const result = await gradeSubmission(assignmentId, studentId);
      setGradedResults((prev) => ({
        ...prev,
        [fileId]: result
      }));
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(`การตรวจงานล้มเหลว: ${errorMessage}`);
    } finally {
      setGradingFile(null);
    }
  };

  if (files.length === 0) {
    return (
      <div className="text-center py-10 border rounded-lg">
        <FileText size={48} className="mx-auto text-gray-300 mb-3" />
        <p className="text-gray-500">
          {fileType === 'teacher' 
            ? 'ยังไม่มีไฟล์เฉลยถูกอัปโหลด' 
            : 'ยังไม่มีงานที่ถูกส่ง'}
        </p>
      </div>
    );
  }

  return (
    <div>
      {error && (
        <div className="bg-red-100 text-red-600 p-3 rounded-md mb-4">
          {error}
        </div>
      )}
      
      <div className="border rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ชื่อไฟล์
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                วันที่อัปโหลด
              </th>
              {fileType === 'student' && (
                <>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    สถานะ
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    คะแนน
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    การดำเนินการ
                  </th>
                </>
              )}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {files.map((file) => (
              <tr key={file.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <FileText size={18} className="text-gray-400 mr-2" />
                    <span>{file.file_name}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(file.created_at).toLocaleString('th-TH')}
                </td>
                
                {fileType === 'student' && (
                  <>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {file.graded || gradedResults[file.id] ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          <Check size={12} className="mr-1" />
                          ตรวจแล้ว
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                          <X size={12} className="mr-1" />
                          ยังไม่ได้ตรวจ
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {file.graded || gradedResults[file.id] ? (
                        <span className="font-medium">
                          {gradedResults[file.id]?.score || file.score || 0}/100
                        </span>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {gradingFile === file.id ? (
                        <button 
                          className="text-gray-400 cursor-not-allowed flex items-center"
                          disabled
                        >
                          <Loader2 size={16} className="mr-1 animate-spin" />
                          กำลังตรวจ...
                        </button>
                      ) : (
                        <button 
                          onClick={() => file.student_id && handleGradeSubmission(file.id, file.student_id)}
                          className={`text-blue-600 hover:text-blue-800 
                            ${!file.student_id || file.graded || gradedResults[file.id] ? 'opacity-50 cursor-not-allowed' : ''}`}
                          disabled={!file.student_id || file.graded || !!gradedResults[file.id]}
                        >
                          {file.graded || gradedResults[file.id] ? 'ตรวจแล้ว' : 'ตรวจงาน'}
                        </button>
                      )}
                    </td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}