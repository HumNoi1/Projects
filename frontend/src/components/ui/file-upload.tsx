// frontend/components/ui/file-upload.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Upload, Loader2 } from 'lucide-react';
import { uploadFile } from '@/lib/api';

interface FileUploadProps {
  fileType: 'teacher' | 'student';
  assignmentId: string;
  title: string;
  description: string;
}

export default function FileUpload({ 
  fileType, 
  assignmentId, 
  title, 
  description 
}: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    
    if (selectedFile) {
      // Check if file is PDF
      if (!selectedFile.name.endsWith('.pdf')) {
        setError('กรุณาอัปโหลดไฟล์ PDF เท่านั้น');
        setFile(null);
        return;
      }
      
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('กรุณาเลือกไฟล์ก่อนอัปโหลด');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      await uploadFile(file, fileType, assignmentId);
      setSuccess(true);
      setTimeout(() => {
        // Redirect to file list page
        const basePath = fileType === 'teacher' 
          ? `/classes/${assignmentId}/teacher/files`
          : `/classes/${assignmentId}/student/files`;
        router.push(basePath);
        router.refresh();
      }, 1500);
    } catch (err: any) {
      setError(err.message || 'เกิดข้อผิดพลาดในการอัปโหลดไฟล์');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">{title}</h1>
      <p className="mb-6 text-gray-600">{description}</p>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="border-2 border-dashed rounded-lg p-8 text-center">
          {file ? (
            <div className="space-y-2">
              <div className="font-medium text-green-600">{file.name}</div>
              <div className="text-sm text-gray-500">{(file.size / 1024).toFixed(2)} KB</div>
              <button
                type="button"
                onClick={() => setFile(null)}
                className="text-red-500 text-sm hover:underline"
              >
                เปลี่ยนไฟล์
              </button>
            </div>
          ) : (
            <div>
              <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <Upload size={28} className="text-gray-500" />
              </div>
              <p className="mb-2">ลากไฟล์มาวางที่นี่ หรือคลิกเพื่อเลือกไฟล์</p>
              <p className="text-sm text-gray-500">รองรับเฉพาะไฟล์ PDF เท่านั้น</p>
            </div>
          )}
          
          <input
            type="file"
            id="file-upload"
            accept=".pdf"
            onChange={handleFileChange}
            className={file ? "hidden" : "absolute inset-0 w-full h-full opacity-0 cursor-pointer"}
          />
        </div>
        
        {error && (
          <div className="bg-red-100 text-red-600 p-3 rounded-md">
            {error}
          </div>
        )}
        
        {success && (
          <div className="bg-green-100 text-green-600 p-3 rounded-md">
            อัปโหลดไฟล์สำเร็จ! กำลังนำคุณไปยังหน้ารายการไฟล์...
          </div>
        )}
        
        <button
          type="submit"
          disabled={!file || loading}
          className={`w-full py-3 rounded-md flex justify-center items-center
            ${!file || loading
              ? 'bg-gray-300 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`
          }
        >
          {loading ? (
            <>
              <Loader2 size={20} className="animate-spin mr-2" />
              กำลังอัปโหลด...
            </>
          ) : 'อัปโหลดไฟล์'}
        </button>
      </form>
    </div>
  );
}