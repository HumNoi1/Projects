// frontend/app/class-student/page.tsx
import { Metadata } from "next";
import { ClassroomCard } from "@/components/classroom/ClassroomCard";
import { CreateClassroomDialog } from "@/components/classroom/CreateClassroomDialog";

export const metadata: Metadata = {
  title: "Class Student - Grading with LLM",
  description: "Manage your classrooms and student assignments",
};

// This would typically come from an API
const mockClassrooms = [
  {
    id: "1",
    name: "Mathematics 101",
    teacherName: "John Doe",
    studentCount: 30,
    assignmentCount: 5,
  },
  {
    id: "2",
    name: "Physics Advanced",
    teacherName: "Jane Smith",
    studentCount: 25,
    assignmentCount: 3,
  },
];

export default function ClassStudentPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Class Management</h1>
        <CreateClassroomDialog />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockClassrooms.map((classroom) => (
          <ClassroomCard key={classroom.id} {...classroom} />
        ))}
      </div>
    </div>
  );
}