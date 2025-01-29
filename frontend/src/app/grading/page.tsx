// app/grading/page.tsx
import GradingQueue from '@/components/grading/GradingQueue'
import { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Auto Grading System - Grading',
  description: 'Grade student assignments using AI assistance',
}

export default function GradingPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-800">Grading Dashboard</h1>
        <Link
          href="/grading/new"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Start New Grading
        </Link>
      </div>
      <GradingQueue />
    </div>
  )
}