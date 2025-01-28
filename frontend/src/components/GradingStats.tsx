// components/GradingStats.tsx
import { ClipboardDocumentCheckIcon, ClockIcon, DocumentCheckIcon, UserGroupIcon } from '@heroicons/react/24/outline'

const stats = [
  {
    name: 'Total Assignments',
    value: '156',
    icon: ClipboardDocumentCheckIcon,
    change: '+12%',
    changeType: 'positive'
  },
  {
    name: 'Pending Grades',
    value: '23',
    icon: ClockIcon,
    change: '-5%',
    changeType: 'negative'
  },
  {
    name: 'Graded Today',
    value: '48',
    icon: DocumentCheckIcon,
    change: '+18%',
    changeType: 'positive'
  },
  {
    name: 'Active Classes',
    value: '12',
    icon: UserGroupIcon,
    change: '0%',
    changeType: 'neutral'
  }
]

const GradingStats = () => {
  return (
    <div className="grid grid-cols-4 gap-6">
      {stats.map((stat) => (
        <div key={stat.name} className="glass-card p-6 hover-card">
          <div className="flex justify-between">
            <div>
              <p className="text-sm text-gray-600">{stat.name}</p>
              <p className="text-2xl font-semibold mt-2">{stat.value}</p>
            </div>
            <div className="rounded-full p-2 bg-blue-100">
              <stat.icon className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-4">
            <span className={`text-sm ${
              stat.changeType === 'positive' ? 'text-green-600' :
              stat.changeType === 'negative' ? 'text-red-600' :
              'text-gray-600'
            }`}>
              {stat.change} from last week
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default GradingStats