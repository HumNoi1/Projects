// frontend/app/classes/[classId]/student/files/page.tsx
import Link from 'next/link';
import { ChevronLeft, Upload } from 'lucide-react';
import FileList from '@/components/ui/file-list';
import { getClassById } from '@/lib/supabase';
import { supabase } from '@/lib/supabase';

async function getStudentFiles(classId: string) {
  const { data, error } = await supabase
    .from('files')
    .select('*, grades(score)')
    .eq('assignment_id', classId)
    .eq('file_type', 'student')
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching student files:', error);
    return [];
  }

  // Transform data to include graded status and score
  return (data || []).map(file => ({
    ...file,
    graded: file.grades !== null,
    score: file.grades ? file.grades.score : null
  }));
}

export default async function StudentFilesPage({ 
  params 
}: { 
  params: { classId: string } 
}) {
  const classData = await getClassById(params.classId);
  const files = await getStudentFiles(params.classId);
  
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
      
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">รายการงานที่ส่ง</h1>
        <Link 
          href={`/classes/${params.classId}/student/upload`}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded flex items-center"
        >
          <Upload size={16} className="mr-2" />
          ส่งงานใหม่
        </Link>
      </div>
      
      <FileList 
        files={files}
        fileType="student"
        assignmentId={params.classId}
      />
    </div>
  );
}