// components/grading/GradingQueue.tsx
import { CalendarIcon, CheckCircleIcon, ClockIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

const GradingQueue = () => {
  const assignments = [
    {
      id: 1,
      title: 'Physics Quiz Chapter 4',
      class: 'Grade 11-B',
      pendingCount: 28,
      gradedCount: 12,
      dueDate: '2024-02-03'
    },
    // Add more assignments
  ]

  return (
    <div className="grid gap-6">
      {assignments.map((assignment) => (
        <Link
          key={assignment.id}
          href={`/grading/${assignment.id}`}
          className="glass-card p-6 hover-card"
        >
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-medium text-lg">{assignment.title}</h3>
              <p className="text-sm text-gray-600">{assignment.class}</p>
            </div>
            <div className="flex space-x-6">
              <div className="flex items-center space-x-2">
                <ClockIcon className="w-5 h-5 text-orange-500" />
                <span className="text-sm">{assignment.pendingCount} pending</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircleIcon className="w-5 h-5 text-green-500" />
                <span className="text-sm">{assignment.gradedCount} graded</span>
              </div>
              <div className="flex items-center space-x-2">
                <CalendarIcon className="w-5 h-5 text-gray-500" />
                <span className="text-sm">Due {assignment.dueDate}</span>
              </div>
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}

export default GradingQueue