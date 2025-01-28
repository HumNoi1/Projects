// app/classes/new/page.tsx
import ClassForm from '@/components/classes/ClassForm'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

export default function CreateClassPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <Link 
        href="/classes" 
        className="inline-flex items-center text-gray-600 hover:text-gray-800 mb-6"
      >
        <ArrowLeftIcon className="w-4 h-4 mr-2" />
        Back to Classes
      </Link>
      
      <div className="glass-card p-8">
        <h1 className="text-2xl font-semibold text-gray-800 mb-6">Create New Class</h1>
        <ClassForm />
      </div>
    </div>
  )
}