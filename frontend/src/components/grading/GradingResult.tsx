// frontend/src/components/grading/GradingResult.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table';
import { Progress } from '@/components/ui/progress';

interface GradingResultProps {
  score: number;
  feedback: string;
  similarities: Array<{
    teacherText: string;
    studentText: string;
    similarity: number;
  }>;
  rubricScores?: Record<string, number>;
}

export function GradingResult({ 
  score, 
  feedback, 
  similarities, 
  rubricScores = {} 
}: GradingResultProps) {
  // ฟังก์ชันเพื่อกำหนดสีตามคะแนน
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Grading Result</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-lg font-medium">Overall Score:</span>
            <span className={`text-2xl font-bold ${getScoreColor(score)}`}>
              {score}/100
            </span>
          </div>

          {Object.keys(rubricScores).length > 0 && (
            <div>
              <h3 className="font-medium mb-2">Rubric Breakdown:</h3>
              <div className="space-y-3">
                {Object.entries(rubricScores).map(([criterion, score]) => (
                  <div key={criterion}>
                    <div className="flex justify-between mb-1">
                      <span>{criterion}</span>
                      <span className={getScoreColor(score)}>{score}%</span>
                    </div>
                    <Progress value={score} className="h-2" />
                  </div>
                ))}
              </div>
            </div>
          )}

          <div>
            <h3 className="font-medium mb-2">Feedback:</h3>
            <p className="text-gray-600 whitespace-pre-line">{feedback}</p>
          </div>

          {similarities.length > 0 && (
            <div>
              <h3 className="font-medium mb-2">Text Similarity Analysis:</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Teacher&apos;s Text</TableHead>
                    <TableHead>Student&apos;s Text</TableHead>
                    <TableHead className="w-[100px]">Similarity</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {similarities.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell className="align-top">{item.teacherText}</TableCell>
                      <TableCell className="align-top">{item.studentText}</TableCell>
                      <TableCell className="text-right">
                        {(item.similarity * 100).toFixed(1)}%
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}