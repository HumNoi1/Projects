// components/RecentAssignments.tsx
import { ClockIcon, CheckCircleIcon } from '@heroicons/react/24/outline'

const assignments = [
  {
    id: 1,
    title: 'Final Exam - Mathematics',
    class: 'Grade 10-A',
    submissions: 35,
    deadline: '2024-02-01',
    status: 'in_progress'
  },
  {
    id: 2,
    title: 'Physics Quiz Chapter 4',
    class: 'Grade 11-B',
    submissions: 28,
    deadline: '2024-02-03',
    status: 'pending'
  },
  {
    id: 3,
    title: 'English Essay - Literature',
    class: 'Grade 12-A',
    submissions: 42,
    deadline: '2024-02-05',
    status: 'completed'
  }
]

const RecentAssignments = () => {
  return (
    <div className="glass-card p-6">
      <h2 className="text-lg font-semibold mb-4">Recent Assignments</h2>
      <div className="space-y-4">
        {assignments.map((assignment) => (
          <div key={assignment.id} className="flex items-center justify-between p-4 bg-white/50 rounded-lg hover:bg-white/80 transition-colors">
            <div>
              <h3 className="font-medium">{assignment.title}</h3>
              <p className="text-sm text-gray-600">{assignment.class}</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium">{assignment.submissions} submissions</p>
                <p className="text-sm text-gray-600">Due {assignment.deadline}</p>
              </div>
              {assignment.status === 'completed' ? (
                <CheckCircleIcon className="w-6 h-6 text-green-500" />
              ) : (
                <ClockIcon className="w-6 h-6 text-orange-500" />
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RecentAssignments