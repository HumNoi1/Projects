// frontend/components/grading/BatchGradingResults.tsx
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';

interface GradingResult {
  student_id: string;
  student_name: string;
  score: number;
  feedback: string;
  graded_at: string;
  rubric_scores?: Record<string, number>;
  similarities?: Array<{
    teacherText: string;
    studentText: string;
    similarity: number;
  }>;
}

interface BatchGradingResultsProps {
  results: GradingResult[];
}

export function BatchGradingResults({ results }: BatchGradingResultsProps) {
  const [selectedResult, setSelectedResult] = useState<GradingResult | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  // ฟังก์ชันเพื่อกำหนดสีตามคะแนน
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  // คำนวณค่าเฉลี่ยคะแนนทั้งหมด
  const averageScore = results.length > 0
    ? Math.round(results.reduce((sum, result) => sum + result.score, 0) / results.length)
    : 0;

  const showDetailDialog = (result: GradingResult) => {
    setSelectedResult(result);
    setIsDialogOpen(true);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Batch Grading Results</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-lg font-medium">Class Average Score:</span>
              <span className={`text-2xl font-bold ${getScoreColor(averageScore)}`}>
                {averageScore}/100
              </span>
            </div>
            <Progress value={averageScore} className="h-2" />
          </div>

          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Student Name</TableHead>
                  <TableHead>Score</TableHead>
                  <TableHead>Graded At</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((result) => (
                  <TableRow key={result.student_id}>
                    <TableCell>{result.student_name}</TableCell>
                    <TableCell className={getScoreColor(result.score)}>
                      {result.score}/100
                    </TableCell>
                    <TableCell>{new Date(result.graded_at).toLocaleString()}</TableCell>
                    <TableCell className="text-right">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => showDetailDialog(result)}
                      >
                        View Details
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* รายละเอียดผลการตรวจแต่ละคน */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              Grading Details for {selectedResult?.student_name || 'Student'}
            </DialogTitle>
          </DialogHeader>
          
          {selectedResult && (
            <div className="space-y-6 mt-4">
              <div className="flex items-center justify-between">
                <span className="text-lg font-medium">Score:</span>
                <span className={`text-2xl font-bold ${getScoreColor(selectedResult.score)}`}>
                  {selectedResult.score}/100
                </span>
              </div>

              {selectedResult.rubric_scores && Object.keys(selectedResult.rubric_scores).length > 0 && (
                <div>
                  <h3 className="font-medium mb-2">Rubric Breakdown:</h3>
                  <div className="space-y-3">
                    {Object.entries(selectedResult.rubric_scores).map(([criterion, score]) => (
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
                <div className="p-4 bg-muted rounded-md">
                  <p className="whitespace-pre-line">{selectedResult.feedback}</p>
                </div>
              </div>

              {selectedResult.similarities && selectedResult.similarities.length > 0 && (
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
                      {selectedResult.similarities.map((item, index) => (
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
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}