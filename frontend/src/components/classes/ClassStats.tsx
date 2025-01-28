// components/classes/ClassStats.tsx
import { UserGroupIcon, DocumentTextIcon, CheckCircleIcon } from '@heroicons/react/24/outline'

const stats = [
  {
    name: 'Active Classes',
    value: '12',
    icon: UserGroupIcon,
    bgColor: 'bg-blue-100',
    textColor: 'text-blue-600'
  },
  {
    name: 'Total Students',
    value: '248',
    icon: DocumentTextIcon,
    bgColor: 'bg-green-100',
    textColor: 'text-green-600'
  },
  {
    name: 'Graded Assignments',
    value: '1,234',
    icon: CheckCircleIcon,
    bgColor: 'bg-purple-100',
    textColor: 'text-purple-600'
  }
]

const ClassStats = () => {
  return (
    <div className="grid grid-cols-3 gap-6">
      {stats.map((stat) => (
        <div key={stat.name} className="glass-card p-6 hover-card">
          <div className="flex items-center space-x-4">
            <div className={`rounded-full p-3 ${stat.bgColor}`}>
              <stat.icon className={`w-6 h-6 ${stat.textColor}`} />
            </div>
            <div>
              <p className="text-sm text-gray-600">{stat.name}</p>
              <p className="text-2xl font-semibold mt-1">{stat.value}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ClassStats