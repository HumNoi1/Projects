// app/page.tsx
import GradingStats from '@/components/GradingStats'
import RecentAssignments from '@/components/RecentAssignments'
import PendingGrades from '@/components/PendingGrades'

export default function Home() {
  return (
    <div className="space-y-6">
      <GradingStats />
      <div className="grid grid-cols-2 gap-6">
        <RecentAssignments />
        <PendingGrades />
      </div>
    </div>
  )
}