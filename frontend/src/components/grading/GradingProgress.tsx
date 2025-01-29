// components/grading/GradingProgress.tsx
import { useState, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import type { GradingCriteria, GradingResult } from './types'

interface GradingProgressProps {
  selectedStudent: string | null;
  gradingResults: Record<string, GradingResult>;
  onGradingUpdate: (results: GradingResult) => void;
}

const GradingProgress = ({
  selectedStudent,
  gradingResults,
  onGradingUpdate
}: GradingProgressProps) => {
  const [isLoading, setIsLoading] = useState(false)

  const criteria: GradingCriteria[] = [
    { name: 'Content Accuracy', maxScore: 10 },
    { name: 'Understanding', maxScore: 10 },
    { name: 'Organization', maxScore: 5 }
  ]

  const currentResults = selectedStudent ? gradingResults[selectedStudent] : null

  useEffect(() => {
    if (selectedStudent && !currentResults) {
      setIsLoading(true)
      // Simulate API call to LLM for grading
      setTimeout(() => {
        const mockResults: GradingResult = {
          scores: {
            'Content Accuracy': 8.5,
            'Understanding': 7.5,
            'Organization': 4.0
          },
          feedback: "Good understanding of concepts but could improve organization.",
          confidence: 0.85
        }
        onGradingUpdate(mockResults)
        setIsLoading(false)
      }, 2000)
    }
  }, [selectedStudent])

  if (!selectedStudent) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        Select a student submission to start grading
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-full">
        <div className="w-full max-w-md space-y-4">
          <Progress value={30} className="w-full" />
          <p className="text-center text-sm text-gray-600">
            Analyzing submission...
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Scores */}
      <div className="grid gap-4">
        {criteria.map((criterion) => (
          <Card key={criterion.name} className="bg-white/70">
            <CardContent className="p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">{criterion.name}</span>
                <span className="text-lg font-semibold">
                  {currentResults?.scores[criterion.name]} / {criterion.maxScore}
                </span>
              </div>
              <Progress 
                value={(currentResults?.scores[criterion.name] / criterion.maxScore) * 100}
              />
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Feedback */}
      <Card className="bg-white/70">
        <CardContent className="p-4">
          <h3 className="font-medium mb-2">Feedback</h3>
          <p className="text-sm text-gray-600">{currentResults?.feedback}</p>
        </CardContent>
      </Card>

      {/* Confidence Score */}
      <Card className="bg-white/70">
        <CardContent className="p-4">
          <div className="flex justify-between items-center">
            <span className="font-medium">AI Confidence</span>
            <span className="text-sm text-gray-600">
              {(currentResults?.confidence * 100).toFixed(1)}%
            </span>
          </div>
          <Progress 
            value={currentResults?.confidence * 100}
            className="mt-2"
          />
        </CardContent>
      </Card>
    </div>
  )
}

export default GradingProgress