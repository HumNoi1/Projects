// components/classes/ClassFilters.tsx
import { FunnelIcon } from '@heroicons/react/24/outline'

const ClassFilters = () => {
  return (
    <div className="flex space-x-4 items-center">
      <div className="relative">
        <input
          type="text"
          placeholder="Search classes..."
          className="pl-4 pr-10 py-2 border rounded-lg bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <select className="px-4 py-2 border rounded-lg bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="">All Grades</option>
        <option value="10">Grade 10</option>
        <option value="11">Grade 11</option>
        <option value="12">Grade 12</option>
      </select>
      
      <select className="px-4 py-2 border rounded-lg bg-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="">All Subjects</option>
        <option value="math">Mathematics</option>
        <option value="physics">Physics</option>
        <option value="english">English</option>
      </select>
      
      <button className="flex items-center px-4 py-2 border rounded-lg bg-white/50 hover:bg-white/70">
        <FunnelIcon className="w-5 h-5 mr-2" />
        More Filters
      </button>
    </div>
  )
}

export default ClassFilters