// components/classes/ClassForm.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { PlusIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { ClassFormData } from '@/types/class'
import { createClass } from '@/lib/api/classes'

interface Student {
  email: string;
  name: string;
}

export default function ClassForm() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [students, setStudents] = useState<Student[]>([{ email: '', name: '' }])

  const [formData, setFormData] = useState<ClassFormData>({
    name: '',
    subject: '',
    grade: '',
    academic_year: new Date().getFullYear().toString(),
    description: '',
    students: [{ email: '', name: '' }]
  })
  
  const handleAddStudent = () => {
    setStudents([...students, { email: '', name: '' }])
  }
  
  const handleRemoveStudent = (index: number) => {
    setStudents(students.filter((_, i) => i !== index))
  }
  
  const handleStudentChange = (index: number, field: keyof Student, value: string) => {
    const newStudents = [...students]
    newStudents[index][field] = value
    setStudents(newStudents)
  }
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      await createClass(formData)
      router.push('/classes')
      router.refresh()
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setError('Failed to create class')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Basic Class Information */}
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Class Name
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Subject
            </label>
            <select
              required
              className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Subject</option>
              <option value="mathematics">Mathematics</option>
              <option value="physics">Physics</option>
              <option value="english">English</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Grade Level
            </label>
            <select
              required
              className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Grade</option>
              <option value="10">Grade 10</option>
              <option value="11">Grade 11</option>
              <option value="12">Grade 12</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Academic Year
            </label>
            <input
              type="text"
              required
              className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., 2024"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            className="w-full px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Add a description for your class..."
          />
        </div>
      </div>

      {/* Students Section */}
      <div>
        <h3 className="font-medium text-gray-900 mb-4">Students</h3>
        <div className="space-y-3">
          {students.map((student, index) => (
            <div key={index} className="flex gap-4">
              <input
                type="email"
                value={student.email}
                onChange={(e) => handleStudentChange(index, 'email', e.target.value)}
                placeholder="Student email"
                className="flex-1 px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                value={student.name}
                onChange={(e) => handleStudentChange(index, 'name', e.target.value)}
                placeholder="Student name"
                className="flex-1 px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {students.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleRemoveStudent(index)}
                  className="p-2 text-gray-500 hover:text-red-500"
                >
                  <XMarkIcon className="w-5 h-5" />
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={handleAddStudent}
            className="inline-flex items-center px-4 py-2 text-sm text-blue-600 hover:text-blue-700"
          >
            <PlusIcon className="w-4 h-4 mr-2" />
            Add Student
          </button>
        </div>
      </div>

      {/* Form Actions */}
      <div className="flex justify-end space-x-4 pt-6">
        <Link
            href="/classes"
            className="px-6 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200"
        >
            Cancel
        </Link>
        <button
          type="submit"
          className="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
        >
          Create Class
        </button>
      </div>
    </form>
  )
}