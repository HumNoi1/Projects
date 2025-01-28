// components/classes/ClassGrid.tsx
import { UserGroupIcon, BookOpenIcon, ChartBarIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

const classes = [
  {
    id: 1,
    name: 'Mathematics 10-A',
    students: 32,
    assignments: 15,
    averageScore: 85,
    teacher: 'Mr. John Smith',
    lastActive: '2 hours ago'
  },
  // ... other classes
]

const ClassGrid = () => {
  return (
    <div className="grid grid-cols-3 gap-6">
      {classes.map((classItem) => (
        <Link 
          key={classItem.id}
          href={`/classes/${classItem.id}`}
          className="block glass-card p-6 hover-card transition-all duration-200"
        >
          <div className="flex justify-between items-start">
            <div>
              <h3 className="font-semibold text-lg">{classItem.name}</h3>
              <p className="text-sm text-gray-600">{classItem.teacher}</p>
            </div>
            <span className="text-xs text-gray-500">{classItem.lastActive}</span>
          </div>
          
          <div className="mt-6 grid grid-cols-3 gap-4">
            <div className="text-center">
              <UserGroupIcon className="w-5 h-5 mx-auto text-blue-600" />
              <p className="mt-1 text-sm font-medium">{classItem.students}</p>
              <p className="text-xs text-gray-600">Students</p>
            </div>
            <div className="text-center">
              <BookOpenIcon className="w-5 h-5 mx-auto text-green-600" />
              <p className="mt-1 text-sm font-medium">{classItem.assignments}</p>
              <p className="text-xs text-gray-600">Assignments</p>
            </div>
            <div className="text-center">
              <ChartBarIcon className="w-5 h-5 mx-auto text-purple-600" />
              <p className="mt-1 text-sm font-medium">{classItem.averageScore}%</p>
              <p className="text-xs text-gray-600">Average</p>
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}

export default ClassGrid