// components/grading/StudentList.tsx
import { CheckCircleIcon, ClockIcon } from '@heroicons/react/24/outline'

interface Student {
  id: string
  name: string
  content: string
}

interface GradingResult {
  score: number
  feedback: string
  gradedAt: string
}

interface StudentListProps {
  selectedStudent: string | null
  onSelectStudent: (id: string) => void
  gradingResults: Record<string, GradingResult>
}

const StudentList = ({
  selectedStudent,
  onSelectStudent,
  gradingResults
}: StudentListProps) => {
  const students: Student[] = [
    { id: '1', name: 'John Doe', content: 'Lorem ipsum...' },
    { id: '2', name: 'Jane Smith', content: 'Lorem ipsum...' },
    // Add more students
  ]

  return (
    <div className="divide-y">
      {students.map((student) => {
        const isGraded = gradingResults[student.id]
        const isSelected = selectedStudent === student.id

        return (
          <button
            key={student.id}
            onClick={() => onSelectStudent(student.id)}
            className={`w-full p-4 flex items-center justify-between hover:bg-gray-50/50 transition-colors ${
              isSelected ? 'bg-blue-50/50' : ''
            }`}
          >
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                {student.name.charAt(0)}
              </div>
              <div className="text-left">
                <p className="font-medium">{student.name}</p>
                <p className="text-sm text-gray-500">
                  {isGraded ? 'Graded' : 'Pending'}
                </p>
              </div>
            </div>
            {isGraded ? (
              <CheckCircleIcon className="w-5 h-5 text-green-500" />
            ) : (
              <ClockIcon className="w-5 h-5 text-gray-400" />
            )}
          </button>
        )
      })}
    </div>
  )
}

export default StudentList