// frontend/app/classes/[classId]/page.tsx
import Link from 'next/link';
import { Upload, List, Users } from 'lucide-react';
import { getClassById, getAssignmentsByClassId } from '@/lib/supabase';

export default async function ClassDetailPage({ 
  params 
}: { 
  params: { classId: string } 
}) {
  const classData = await getClassById(params.classId);
  
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
      <h1 className="text-2xl font-bold mb-6">{classData.name}</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* ส่วนของครู */}
        <div className="border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">สำหรับครู</h2>
          
          <div className="space-y-4">
            <Link 
              href={`/classes/${params.classId}/teacher/upload`}
              className="block border rounded p-4 hover:border-blue-500 hover:shadow-md transition-all"
            >
              <div className="flex items-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                  <Upload size={24} className="text-blue-600" />
                </div>
                <div>
                  <h3 className="font-medium">อัปโหลดไฟล์เฉลย</h3>
                  <p className="text-sm text-gray-600">อัปโหลดไฟล์เฉลยสำหรับงานที่มอบหมาย</p>
                </div>
              </div>
            </Link>
            
            <Link 
              href={`/classes/${params.classId}/teacher/files`}
              className="block border rounded p-4 hover:border-blue-500 hover:shadow-md transition-all"
            >
              <div className="flex items-center">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4">
                  <List size={24} className="text-green-600" />
                </div>
                <div>
                  <h3 className="font-medium">รายการไฟล์</h3>
                  <p className="text-sm text-gray-600">ดูรายการไฟล์เฉลยทั้งหมด</p>
                </div>
              </div>
            </Link>
          </div>
        </div>
        
        {/* ส่วนของนักเรียน */}
        <div className="border rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">สำหรับนักเรียน</h2>
          
          <div className="space-y-4">
            <Link 
              href={`/classes/${params.classId}/student/upload`}
              className="block border rounded p-4 hover:border-blue-500 hover:shadow-md transition-all"
            >
              <div className="flex items-center">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mr-4">
                  <Upload size={24} className="text-purple-600" />
                </div>
                <div>
                  <h3 className="font-medium">ส่งงาน</h3>
                  <p className="text-sm text-gray-600">อัปโหลดงานที่ได้รับมอบหมาย</p>
                </div>
              </div>
            </Link>
            
            <Link 
              href={`/classes/${params.classId}/student/files`}
              className="block border rounded p-4 hover:border-blue-500 hover:shadow-md transition-all"
            >
              <div className="flex items-center">
                <div className="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center mr-4">
                  <List size={24} className="text-amber-600" />
                </div>
                <div>
                  <h3 className="font-medium">รายการงานที่ส่ง</h3>
                  <p className="text-sm text-gray-600">ดูรายการงานและผลการตรวจ</p>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}