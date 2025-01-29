// app/assignments/page.tsx
import AssignmentList from '@/components/assignments/AssignmentList'
import { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Assignments - Auto Grading System',
  description: 'Manage and grade student assignments',
}

export default function AssignmentsPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-800">Assignments</h1>
        <Link
          href="/assignments/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Create Assignment
        </Link>
      </div>
      <AssignmentList />
    </div>
  )
}