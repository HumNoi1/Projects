// components/assignments/AssignmentList.tsx
"use client";

import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { 
  UserGroupIcon, 
  ClockIcon,
  CheckCircleIcon,
  CloudArrowDownIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'
import { Progress } from '@/components/ui/progress'

// กำหนด interface สำหรับข้อมูล Assignment
interface Assignment {
  id: string;
  title: string;
  className: string;
  dueDate: string;
  submissionCount: number;
  totalStudents: number;
  referenceFile: string;
  status: 'active' | 'closed';
  gradingProgress: number;
}

// กำหนด Props ที่จะส่งเข้ามาใน Component
interface AssignmentListProps {
  onDownloadReference?: (assignmentId: string) => void;
  onViewSubmissions?: (assignmentId: string) => void;
}

const AssignmentList = ({
  onDownloadReference,
}: AssignmentListProps) => {
  // State สำหรับการกรองและค้นหา
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'closed'>('all')

  // ข้อมูลตัวอย่าง (ในการใช้งานจริงจะดึงจาก API)
  const assignments: Assignment[] = [
    {
      id: '1',
      title: 'Chapter 4 Quiz - Thermodynamics',
      className: 'Physics 11-A',
      dueDate: '2024-02-15',
      submissionCount: 28,
      totalStudents: 35,
      referenceFile: 'thermodynamics_reference.pdf',
      status: 'active',
      gradingProgress: 65
    },
    {
      id: '2',
      title: 'Literature Essay - Shakespeare',
      className: 'English 10-B',
      dueDate: '2024-02-20',
      submissionCount: 42,
      totalStudents: 45,
      referenceFile: 'shakespeare_rubric.pdf',
      status: 'active',
      gradingProgress: 30
    }
  ]

  // กรองรายการตามการค้นหาและสถานะ
  const filteredAssignments = assignments.filter(assignment => {
    const matchesSearch = assignment.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         assignment.className.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === 'all' || assignment.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // ฟังก์ชันแปลงวันที่เป็นรูปแบบที่อ่านง่าย
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('th-TH', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  return (
    <div className="space-y-6">
      {/* ส่วนค้นหาและกรอง */}
      <div className="flex space-x-4">
        <input
          type="text"
          placeholder="Search assignments..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as 'all' | 'active' | 'closed')}
          className="px-4 py-2 rounded-lg border bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Status</option>
          <option value="active">Active</option>
          <option value="closed">Closed</option>
        </select>
      </div>

      {/* รายการ Assignments */}
      <div className="grid gap-4">
        {filteredAssignments.map((assignment) => (
          <Card 
            key={assignment.id}
            className="p-6 hover:shadow-md transition-shadow bg-white/50 backdrop-blur-sm"
          >
            <div className="flex justify-between items-start">
              {/* ข้อมูลพื้นฐานของ Assignment */}
              <div className="space-y-3">
                <div>
                  <h3 className="text-lg font-medium">{assignment.title}</h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                    <span className="flex items-center">
                      <UserGroupIcon className="w-4 h-4 mr-1" />
                      {assignment.className}
                    </span>
                    <span className="flex items-center">
                      <ClockIcon className="w-4 h-4 mr-1" />
                      Due: {formatDate(assignment.dueDate)}
                    </span>
                  </div>
                </div>

                {/* แสดงความคืบหน้าการส่งงาน */}
                <div className="max-w-md">
                  <div className="flex justify-between text-sm mb-1">
                    <span>Submissions</span>
                    <span>{assignment.submissionCount}/{assignment.totalStudents}</span>
                  </div>
                  <Progress 
                    value={(assignment.submissionCount / assignment.totalStudents) * 100} 
                    className="h-2"
                  />
                </div>

                {/* แสดงความคืบหน้าการตรวจ */}
                <div className="max-w-md">
                  <div className="flex justify-between text-sm mb-1">
                    <span>Grading Progress</span>
                    <span>{assignment.gradingProgress}%</span>
                  </div>
                  <Progress 
                    value={assignment.gradingProgress}
                    className="h-2 [&>div]:bg-green-600"
                  />
                </div>
              </div>

              {/* ปุ่มดำเนินการ */}
              <div className="flex flex-col space-y-2">
                <button
                  onClick={() => onDownloadReference?.(assignment.id)}
                  className="flex items-center px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  <CloudArrowDownIcon className="w-4 h-4 mr-2" />
                  Reference File
                </button>
                <Link
                  href={`/assignments/${assignment.id}/submissions`}
                  className="flex items-center px-3 py-2 text-sm text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                >
                  <CheckCircleIcon className="w-4 h-4 mr-2" />
                  View Submissions
                </Link>
                <Link
                  href={`/assignments/${assignment.id}/grade`}
                  className="flex items-center px-3 py-2 text-sm text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                >
                  <ArrowPathIcon className="w-4 h-4 mr-2" />
                  Continue Grading
                </Link>
              </div>
            </div>
          </Card>
        ))}

        {/* แสดงข้อความเมื่อไม่พบรายการ */}
        {filteredAssignments.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No assignments found matching your criteria
          </div>
        )}
      </div>
    </div>
  )
}

export default AssignmentList