// components/PendingGrades.tsx
import { ArrowRightIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

const pendingGrades = [
  {
    id: 1,
    student: 'John Doe',
    assignment: 'Mathematics Final',
    submittedAt: '2024-01-28 14:30',
    class: 'Grade 10-A'
  },
  {
    id: 2,
    student: 'Jane Smith',
    assignment: 'Physics Quiz',
    submittedAt: '2024-01-28 15:45',
    class: 'Grade 11-B'
  },
  {
    id: 3,
    student: 'Mike Johnson',
    assignment: 'English Essay',
    submittedAt: '2024-01-28 16:20',
    class: 'Grade 12-A'
  }
]

const PendingGrades = () => {
  return (
    <div className="glass-card p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Pending Grades</h2>
        <Link 
          href="/grading"
          className="text-sm text-blue-600 hover:text-blue-700 flex items-center"
        >
          View all
          <ArrowRightIcon className="w-4 h-4 ml-1" />
        </Link>
      </div>
      <div className="space-y-4">
        {pendingGrades.map((grade) => (
          <div key={grade.id} className="flex items-center justify-between p-4 bg-white/50 rounded-lg hover:bg-white/80 transition-colors">
            <div>
              <h3 className="font-medium">{grade.student}</h3>
              <p className="text-sm text-gray-600">{grade.assignment}</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium">{grade.class}</p>
              <p className="text-sm text-gray-600">Submitted {grade.submittedAt}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default PendingGrades