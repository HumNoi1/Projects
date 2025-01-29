// components/grading/GradingForm.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { CloudArrowUpIcon, DocumentTextIcon } from '@heroicons/react/24/outline'
import { Card } from '@/components/ui/card'
import Link from 'next/link'

interface GradingCriteria {
  name: string;
  description: string;
  maxScore: number;
  weight: number;
}

const GradingForm = () => {
  const router = useRouter()
  const [referenceFile, setReferenceFile] = useState<File | null>(null)
  const [studentFiles, setStudentFiles] = useState<File[]>([])
  const [criteria, setCriteria] = useState<GradingCriteria[]>([
    { name: 'Content Accuracy', description: 'Correctness of the answer', maxScore: 10, weight: 1 }
  ])

  const handleReferenceUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      setReferenceFile(e.target.files[0])
    }
  }

  const handleStudentUploads = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setStudentFiles(Array.from(e.target.files))
    }
  }

  const handleAddCriteria = () => {
    setCriteria([...criteria, { 
      name: '', 
      description: '', 
      maxScore: 10, 
      weight: 1 
    }])
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement grading submission
    router.push('/grading/session/[id]')
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Reference Answer Upload */}
      <Card className="p-6 bg-white/50">
        <h2 className="text-lg font-medium mb-4">Reference Answer</h2>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          {referenceFile ? (
            <div className="flex items-center justify-center space-x-3">
              <DocumentTextIcon className="w-8 h-8 text-blue-600" />
              <div className="text-left">
                <p className="font-medium">{referenceFile.name}</p>
                <p className="text-sm text-gray-500">
                  {(referenceFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
          ) : (
            <label className="cursor-pointer">
              <div className="flex flex-col items-center">
                <CloudArrowUpIcon className="w-12 h-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-600">Upload reference answer</p>
                <p className="text-xs text-gray-500">PDF, DOC, TXT up to 10MB</p>
              </div>
              <input
                type="file"
                className="hidden"
                accept=".pdf,.doc,.docx,.txt"
                onChange={handleReferenceUpload}
              />
            </label>
          )}
        </div>
      </Card>

      {/* Student Submissions Upload */}
      <Card className="p-6 bg-white/50">
        <h2 className="text-lg font-medium mb-4">Student Submissions</h2>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <label className="cursor-pointer">
            <div className="flex flex-col items-center">
              <CloudArrowUpIcon className="w-12 h-12 text-gray-400" />
              <p className="mt-2 text-sm text-gray-600">
                {studentFiles.length > 0 
                  ? `${studentFiles.length} files selected` 
                  : 'Upload student submissions'}
              </p>
              <p className="text-xs text-gray-500">PDF, DOC, TXT up to 10MB each</p>
            </div>
            <input
              type="file"
              multiple
              className="hidden"
              accept=".pdf,.doc,.docx,.txt"
              onChange={handleStudentUploads}
            />
          </label>
        </div>
      </Card>

      {/* Grading Criteria */}
      <Card className="p-6 bg-white/50">
        <h2 className="text-lg font-medium mb-4">Grading Criteria</h2>
        <div className="space-y-4">
          {criteria.map((criterion, index) => (
            <div key={index} className="grid grid-cols-4 gap-4">
              <input
                type="text"
                placeholder="Criterion name"
                value={criterion.name}
                onChange={(e) => {
                  const newCriteria = [...criteria]
                  newCriteria[index].name = e.target.value
                  setCriteria(newCriteria)
                }}
                className="col-span-1 px-4 py-2 rounded-lg border bg-white/50"
              />
              <input
                type="text"
                placeholder="Description"
                value={criterion.description}
                onChange={(e) => {
                  const newCriteria = [...criteria]
                  newCriteria[index].description = e.target.value
                  setCriteria(newCriteria)
                }}
                className="col-span-2 px-4 py-2 rounded-lg border bg-white/50"
              />
              <div className="col-span-1 flex space-x-2">
                <input
                  type="number"
                  placeholder="Max score"
                  value={criterion.maxScore}
                  onChange={(e) => {
                    const newCriteria = [...criteria]
                    newCriteria[index].maxScore = Number(e.target.value)
                    setCriteria(newCriteria)
                  }}
                  className="w-20 px-4 py-2 rounded-lg border bg-white/50"
                />
                <input
                  type="number"
                  step="0.1"
                  placeholder="Weight"
                  value={criterion.weight}
                  onChange={(e) => {
                    const newCriteria = [...criteria]
                    newCriteria[index].weight = Number(e.target.value)
                    setCriteria(newCriteria)
                  }}
                  className="w-20 px-4 py-2 rounded-lg border bg-white/50"
                />
              </div>
            </div>
          ))}
          <button
            type="button"
            onClick={handleAddCriteria}
            className="text-blue-600 hover:text-blue-700"
          >
            + Add Criterion
          </button>
        </div>
      </Card>

      {/* Form Actions */}
      <div className="flex justify-end space-x-4">
        <Link
          href="/grading"
          className="px-6 py-2 text-gray-700 hover:text-gray-900 bg-gray-100 rounded-lg hover:bg-gray-200"
        >
          Cancel
        </Link>
        <button
          type="submit"
          className="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
        >
          Start Grading
        </button>
      </div>
    </form>
  )
}

export default GradingForm