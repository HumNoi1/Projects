// components/grading/GradingLayout.tsx
'use client'

import { useState } from 'react'
import DocumentViewer from '@/components/grading/DocumentViewer'
import GradingProgress from '@/components/grading/GradingProgress'
import StudentList from '@/components/grading/StudentList'
import { Card } from '@/components/ui/card'

const GradingLayout = () => {
  // State for tracking selected student and grading progress
  const [selectedStudent, setSelectedStudent] = useState<string | null>(null)
  const [gradingResults, setGradingResults] = useState<Record<string, any>>({})

  // Reference document (teacher's answer)
  const referenceDoc = {
    title: "Chapter 4 - Reference Answer",
    content: "Lorem ipsum..." // จะถูกแทนที่ด้วยเนื้อหาจริง
  }

  return (
    <div className="h-[calc(100vh-4rem)] flex">
      {/* Left Panel - Reference Answer */}
      <div className="w-1/3 p-4">
        <Card className="h-full bg-white/50 backdrop-blur-xl overflow-hidden">
          <div className="p-4 border-b bg-blue-50/50">
            <h2 className="text-lg font-semibold">Reference Answer</h2>
          </div>
          <div className="p-4 h-[calc(100%-4rem)] overflow-auto">
            <DocumentViewer document={referenceDoc} />
          </div>
        </Card>
      </div>

      {/* Center Panel - Grading Progress */}
      <div className="flex-1 p-4 flex flex-col">
        <Card className="flex-1 bg-white/50 backdrop-blur-xl">
          <div className="p-4 border-b bg-purple-50/50">
            <h2 className="text-lg font-semibold">Grading Progress</h2>
          </div>
          <div className="p-4 h-[calc(100%-4rem)] overflow-auto">
            <GradingProgress
              selectedStudent={selectedStudent}
              gradingResults={gradingResults}
              onGradingUpdate={(results) => {
                setGradingResults({
                  ...gradingResults,
                  [selectedStudent!]: results
                })
              }}
            />
          </div>
        </Card>
      </div>

      {/* Right Panel - Student Submissions */}
      <div className="w-1/3 p-4">
        <Card className="h-full bg-white/50 backdrop-blur-xl">
          <div className="p-4 border-b bg-green-50/50">
            <h2 className="text-lg font-semibold">Student Submissions</h2>
          </div>
          <div className="h-[calc(100%-4rem)]">
            <StudentList
              selectedStudent={selectedStudent}
              onSelectStudent={setSelectedStudent}
              gradingResults={gradingResults}
            />
          </div>
        </Card>
      </div>
    </div>
  )
}

export default GradingLayout