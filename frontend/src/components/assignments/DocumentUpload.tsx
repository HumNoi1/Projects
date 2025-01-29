// components/assignments/DocumentUpload.tsx
import { useRef, useState } from 'react'
import { CloudArrowUpIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { Progress } from '@/components/ui/progress'

interface DocumentUploadProps {
  onFileSelect: (file: File) => void;
  isUploading?: boolean;
  progress?: number;
  accept?: string;
  maxSize?: number;
}

export const DocumentUpload = ({
  onFileSelect,
  isUploading = false,
  progress = 0,
  accept = '.pdf,.doc,.docx,.txt',
  maxSize = 10485760 // 10MB
}: DocumentUploadProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    setError(null)

    if (file) {
      if (file.size > maxSize) {
        setError(`File size should not exceed ${maxSize / 1048576}MB`)
        return
      }

      setSelectedFile(file)
      onFileSelect(file)
    }
  }

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const file = event.dataTransfer.files?.[0]
    
    if (file) {
      if (file.size > maxSize) {
        setError(`File size should not exceed ${maxSize / 1048576}MB`)
        return
      }

      setSelectedFile(file)
      onFileSelect(file)
    }
  }

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
  }

  return (
    <div>
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {selectedFile ? (
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <CloudArrowUpIcon className="w-8 h-8 text-blue-600" />
              <div>
                <p className="font-medium">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => {
                setSelectedFile(null)
                if (fileInputRef.current) {
                  fileInputRef.current.value = ''
                }
              }}
              className="text-gray-500 hover:text-red-500"
            >
              <XMarkIcon className="w-5 h-5" />
            </button>
          </div>
        ) : (
          <div className="text-center">
            <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mx-auto" />
            <p className="mt-2 text-sm text-gray-600">
              Drag and drop your file here, or{' '}
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="text-blue-600 hover:text-blue-700"
              >
                browse
              </button>
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Supported formats: PDF, DOC, DOCX, TXT up to 10MB
            </p>
          </div>
        )}
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}

      {isUploading && (
        <div className="mt-4">
          <Progress value={progress} />
          <p className="text-sm text-gray-600 mt-2">
            Uploading... {progress}%
          </p>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept={accept}
        onChange={handleFileChange}
      />
    </div>
  )
}