// frontend/components/grading/GradingResult.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface GradingResultProps {
  score: number;
  feedback: string;
  similarities: Array<{
    teacherText: string;
    studentText: string;
    similarity: number;
  }>;
}

export function GradingResult({ score, feedback, similarities }: GradingResultProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Grading Result</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-lg font-medium">Score:</span>
            <span className="text-2xl font-bold">{score}/100</span>
          </div>

          <div>
            <h3 className="font-medium mb-2">Feedback:</h3>
            <p className="text-gray-600">{feedback}</p>
          </div>

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
        </div>
      </CardContent>
    </Card>
  );
}