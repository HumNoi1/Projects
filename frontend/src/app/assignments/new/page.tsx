// app/assignments/new/page.tsx
import AssignmentForm from '@/components/assignments/AssignmentForm'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

export default function NewAssignmentPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <Link 
        href="/assignments" 
        className="inline-flex items-center text-gray-600 hover:text-gray-800 mb-6"
      >
        <ArrowLeftIcon className="w-4 h-4 mr-2" />
        Back to Assignments
      </Link>
      
      <div className="glass-card p-8">
        <h1 className="text-2xl font-semibold text-gray-800 mb-6">Create New Assignment</h1>
        <AssignmentForm />
      </div>
    </div>
  )
}