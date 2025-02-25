// frontend/src/components/grading/PDFViewer.tsx
import { useState } from 'react';
import * as React from 'react';
import { Upload } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { GradingService } from '@/services/api';

interface PDFViewerProps {
  title: string;
  fileType: 'teacher' | 'student';
  assignmentId: string;
  onFileUpload: (file: File) => void;
}

export const PDFViewer: React.FC<PDFViewerProps> = ({ title, fileType, assignmentId, onFileUpload }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // สร้าง URL สำหรับแสดงตัวอย่างไฟล์ PDF
    const fileUrl = URL.createObjectURL(file);
    setPreviewUrl(fileUrl);

    setIsUploading(true);
    try {
      // อัปโหลดไฟล์ไปยัง API
      await GradingService.uploadDocument(file, fileType, assignmentId);
      
      // แจ้งคอมโพเนนต์ parent
      onFileUpload(file);
    } catch (error) {
      console.error('Error uploading file:', error);
      // แสดง error message (ใช้ toast หรือ alert component)
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {!previewUrl ? (
          // ส่วนอัปโหลดไฟล์
          <div className="flex items-center justify-center w-full">
            <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <Upload className="w-8 h-8 mb-4 text-gray-500" />
                <p className="mb-2 text-sm text-gray-500">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500">PDF (MAX. 10MB)</p>
              </div>
              <input
                type="file"
                className="hidden"
                accept="application/pdf"
                onChange={handleFileChange}
                disabled={isUploading}
              />
            </label>
          </div>
        ) : (
          // แสดงตัวอย่าง PDF
          <div className="w-full h-64">
            <iframe
              src={previewUrl}
              className="w-full h-full"
              title={title}
            />
          </div>
        )}
      </CardContent>
    </Card>
  );
};