// frontend/components/classroom/ClassroomCard.tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, Upload, FileText } from "lucide-react";
import Link from "next/link";

interface ClassroomCardProps {
  id: string;
  name: string;
  teacherName: string;
  studentCount: number;
  assignmentCount: number;
}

export function ClassroomCard({
  id,
  name,
  teacherName,
  studentCount,
  assignmentCount,
}: ClassroomCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>{name}</span>
          <Users className="h-5 w-5 text-gray-500" />
        </CardTitle>
        <p className="text-sm text-gray-500">Teacher: {teacherName}</p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex justify-between text-sm">
            <span>Students: {studentCount}</span>
            <span>Assignments: {assignmentCount}</span>
          </div>
          <div className="flex gap-2">
            <Link href={`/class-student/${id}/upload`} className="flex-1">
              <Button variant="outline" className="w-full">
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </Button>
            </Link>
            <Link href={`/class-student/${id}/assignments`} className="flex-1">
              <Button variant="outline" className="w-full">
                <FileText className="h-4 w-4 mr-2" />
                View
              </Button>
            </Link>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}