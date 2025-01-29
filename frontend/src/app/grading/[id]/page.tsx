// app/grading/[id]/page.tsx
import GradingLayout from '@/components/grading/GradingLayout'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Grading Session - Auto Grading System',
  description: 'Grade student assignments with AI assistance',
}

export default function GradingSessionPage() {
  return <GradingLayout />
}