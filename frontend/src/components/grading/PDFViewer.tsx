// frontend/components/grading/PDFViewer.tsx
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileUp, Eye, Trash } from 'lucide-react';

interface PDFViewerProps {
  title: string;
  onFileSelect: (file: File) => void;
}

export function PDFViewer({ title, onFileSelect }: PDFViewerProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      // สร้าง URL สำหรับแสดงตัวอย่าง PDF
      const fileUrl = URL.createObjectURL(file);
      setPreviewUrl(fileUrl);
      onFileSelect(file);
    }
  };

  const handleRemoveFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedFile(null);
    setPreviewUrl(null);
  };

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {!selectedFile ? (
            <div className="flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-6 min-h-[400px]">
              <FileUp className="h-12 w-12 text-gray-400 mb-4" />
              <label className="cursor-pointer">
                <Button variant="outline">Choose PDF File</Button>
                <input
                  type="file"
                  className="hidden"
                  accept=".pdf"
                  onChange={handleFileChange}
                />
              </label>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-medium">{selectedFile.name}</span>
                <div className="flex gap-2">
                  <Button variant="outline" size="icon">
                    <Eye className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={handleRemoveFile}
                  >
                    <Trash className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              {previewUrl && (
                <iframe
                  src={previewUrl}
                  className="w-full h-[500px] border rounded-lg"
                />
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}