// app/classes/page.tsx
import Link from 'next/link'
import ClassGrid from '@/components/classes/ClassGrid'
import ClassFilters from '@/components/classes/ClassFilters'
import ClassStats from '@/components/classes/ClassStats'

export default function ClassesPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-800">Classes</h1>
        <Link 
          href="/classes/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Create New Class
        </Link>
      </div>
      
      <ClassStats />
      <ClassFilters />
      <ClassGrid />
    </div>
  )
}