'use client'

import React from 'react'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card } from '@/components/ui/card'
import { DocumentUpload } from '@/components/assignments/DocumentUpload'
import { ClassSelect } from '@/components/assignments/ClassSelect'

interface ClassSelectProps {
  classes: string[];
  value: string;
  onChange: (selectedClass: string) => void;
}

// คำอธิบาย: Interface นี้กำหนดโครงสร้างข้อมูลของ Assignment
interface AssignmentFormData {
  title: string;
  description: string;
  dueDate: string;
  classId: string;
  maxScore: number;
  referenceFile?: File;
}

const AssignmentForm = () => {
  const router = useRouter()
  const [formData, setFormData] = useState<AssignmentFormData>({
    title: '',
    description: '',
    dueDate: '',
    classId: '',
    maxScore: 100
  })
  
  // คำอธิบาย: State สำหรับจัดการสถานะการอัพโหลดไฟล์
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const classes = ['Class 1', 'Class 2', 'Class 3'] // Example class list

  const handleClassChange = (selectedClass: string) => {
    setFormData({ ...formData, classId: selectedClass })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsUploading(true)

    try {
      // จำลองการอัพโหลดไฟล์แบบ Progressive
      for (let i = 0; i <= 100; i += 10) {
        await new Promise(resolve => setTimeout(resolve, 200))
        setUploadProgress(i)
      }

      // TODO: Implement actual file upload and form submission
      router.push('/assignments')
    } catch (error) {
      console.error('Error creating assignment:', error)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* ส่วนข้อมูลพื้นฐานของ Assignment */}
      <Card className="p-6 bg-white/50">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Assignment Title
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Chapter 4 Quiz - Thermodynamics"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Enter assignment description"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Due Date
              </label>
              <input
                type="datetime-local"
                required
                value={formData.dueDate}
                onChange={(e) => setFormData({...formData, dueDate: e.target.value})}
                className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Score
              </label>
              <input
                type="number"
                required
                value={formData.maxScore}
                onChange={(e) => setFormData({...formData, maxScore: Number(e.target.value)})}
                className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                min="0"
                step="1"
              />
            </div>
          </div>
        </div>
      </Card>

      {/* ส่วนเลือกชั้นเรียน */}
      <Card className="p-6 bg-white/50">
        <h3 className="text-lg font-medium mb-4">Select Class</h3>
        <ClassSelect
          classes={classes}
          value={formData.classId}
          onChange={handleClassChange}
        />
      </Card>

      {/* ส่วนอัพโหลดเอกสารเฉลย */}
      <Card className="p-6 bg-white/50">
        <h3 className="text-lg font-medium mb-4">Reference Document</h3>
        <DocumentUpload
          onFileSelect={(file) => setFormData({...formData, referenceFile: file})}
          isUploading={isUploading}
          progress={uploadProgress}
          accept=".pdf,.doc,.docx,.txt"
          maxSize={10485760} // 10MB
        />
      </Card>

      {/* ปุ่มดำเนินการ */}
      <div className="flex justify-end space-x-4">
        <button
          type="button"
          onClick={() => router.push('/assignments')}
          className="px-6 py-2 text-gray-700 hover:text-gray-900 bg-gray-100 rounded-lg hover:bg-gray-200"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isUploading}
          className="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isUploading ? 'Creating...' : 'Create Assignment'}
        </button>
      </div>
    </form>
  )
}

export default AssignmentForm