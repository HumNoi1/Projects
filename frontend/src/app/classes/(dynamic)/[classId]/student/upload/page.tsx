// frontend/app/classes/[classId]/student/upload/page.tsx
import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import FileUpload from '@/components/ui/file-upload';
import { getClassById } from '@/lib/supabase';

export default async function StudentUploadPage({ 
  params 
}: { 
  params: { classId: string } 
}) {
  const { classId } = await params;
  const classData = await getClassById(classId);
  
  if (!classData) {
    return (
      <div className="text-center py-10">
        <h1 className="text-2xl font-bold text-red-500">ไม่พบข้อมูลห้องเรียน</h1>
        <Link href="/classes" className="text-blue-500 hover:underline mt-4 inline-block">
          กลับไปยังรายการห้องเรียน
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <Link 
          href={`/classes/${params.classId}`}
          className="flex items-center text-blue-500 hover:underline"
        >
          <ChevronLeft size={16} className="mr-1" />
          กลับไปยังห้องเรียน {classData.name}
        </Link>
      </div>
      
      <FileUpload 
        fileType="student"
        assignmentId={params.classId}
        title="ส่งงานสำหรับการตรวจ"
        description="อัปโหลดงานของคุณเพื่อให้ระบบตรวจอัตโนมัติ คุณจะได้รับผลคะแนนและคำแนะนำจากระบบหลังจากการตรวจ"
      />
    </div>
  );
}