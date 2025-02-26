// frontend/components/ui/forms/upload-form.tsx
import React, { useState } from 'react';
import { Button } from '../button';

interface UploadFormProps {
  fileType: 'teacher' | 'student';
  assignmentId: string;
  onUploadSuccess: (fileRecord: any) => void;
  onUploadError: (error: Error) => void;
}

export const UploadForm: React.FC<UploadFormProps> = ({
  fileType,
  assignmentId,
  onUploadSuccess,
  onUploadError,
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      return;
    }
    
    setIsUploading(true);
    
    try {
      // Import dynamically to avoid server-side issues
      const { uploadFile } = await import('../../../lib/api/files');
      const fileRecord = await uploadFile(file, fileType, assignmentId);
      onUploadSuccess(fileRecord);
    } catch (error) {
      onUploadError(error instanceof Error ? error : new Error('An unknown error occurred'));
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700">
          {fileType === 'teacher' ? 'อัปโหลดไฟล์เฉลย' : 'อัปโหลดไฟล์คำตอบ'}
        </label>
        <div className="mt-1">
          <input
            id="file-upload"
            name="file-upload"
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
      
      <Button
        type="submit"
        isLoading={isUploading}
        disabled={!file || isUploading}
      >
        อัปโหลด
      </Button>
    </form>
  );
};