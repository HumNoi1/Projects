// frontend/components/grading/PDFViewer.tsx
import { useState } from 'react';
import * as React from 'react';
import { Upload } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import '@/types/database';

interface PDFViewerProps {
  title: string;
  fileType: 'teacher' | 'student';
  assignmentId: string;
  onFileUpload: (file: File) => void;
  onFileSelect?: (file: File) => void;
}

export const PDFViewer: React.FC<PDFViewerProps> = ({ title, fileType, assignmentId, onFileUpload }) => {
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('fileType', fileType);
      formData.append('assignmentId', assignmentId);

      const response = await fetch('/api/files', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const fileRecord = await response.json();
      onFileUpload(fileRecord);
    } catch (error) {
      console.error('Error uploading file:', error);
      // TODO: แสดง error message
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
      </CardContent>
    </Card>
  );
};