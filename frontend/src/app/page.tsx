// app/page.tsx
import Dashboard from '@/components/dashboard/Dashboard'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Classroom Dashboard',
  description: 'View and manage your classroom activities'
}

export default function Home() {
  return (
    <div className="flex h-screen bg-gray-900">
      <Dashboard />
    </div>
  )
}