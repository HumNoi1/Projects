// frontend/app/assignments/[id]/grade/page.tsx
'use client';

import { useAssignment } from '@/hooks/useAssignment';
import { PDFViewer } from '@/components/grading/PDFViewer';
// ... imports อื่นๆ

export default function GradingPage({ params }: { params: { id: string } }) {
  const { assignment, loading: assignmentLoading } = useAssignment(params.id);
  
  // ... code อื่นๆ เหมือนเดิม แต่ส่ง assignmentId ไปให้ PDFViewer
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        {assignmentLoading ? 'Loading...' : assignment?.title}
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PDFViewer
          title="Teacher's Answer Key"
          fileType="teacher"
          assignmentId={params.id}
          onFileUpload={(file) => setTeacherFile(file)}
        />
        {/* ... */}
      </div>
      {/* ... */}
    </div>
  );
}