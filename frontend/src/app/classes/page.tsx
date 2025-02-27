// app/classes/page.tsx
import Link from 'next/link';
import { Plus } from 'lucide-react';
import { getAllClasses } from '@/lib/supabase';
import { Suspense } from 'react';

// คอมโพเนนต์สำหรับแสดงรายการห้องเรียน
async function ClassList() {
  // ดึงข้อมูลห้องเรียนทั้งหมด
  const classes = await getAllClasses();
  
  if (classes.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-500">ยังไม่มีห้องเรียน กรุณาสร้างห้องเรียนใหม่</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {classes.map((classItem) => (
        <Link 
          key={classItem.id} 
          href={`/classes/${classItem.id}`}
          className="block border rounded-lg p-4 hover:border-blue-500 hover:shadow-md transition-all"
        >
          <h2 className="text-lg font-semibold">{classItem.name}</h2>
          <p className="text-gray-600 text-sm mt-1">
            {classItem.description || 'ไม่มีคำอธิบาย'}
          </p>
          <div className="mt-2 text-sm text-gray-500">
            งาน: {classItem.assignment_count || 0} รายการ
          </div>
        </Link>
      ))}
    </div>
  );
}

export default function ClassesPage() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">ห้องเรียนทั้งหมด</h1>
        <Link 
          href="/classes/create" 
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded flex items-center"
        >
          <Plus size={18} className="mr-1" />
          สร้างห้องเรียนใหม่
        </Link>
      </div>

      {/* แสดงรายการห้องเรียนด้วย Suspense สำหรับ Loading State */}
      <Suspense fallback={<p className="text-center py-4">กำลังโหลดข้อมูล...</p>}>
        <ClassList />
      </Suspense>

      {/* Card สร้างห้องเรียนใหม่ */}
      <div className="mt-8">
        <Link 
          href="/classes/create"
          className="border border-dashed rounded-lg p-4 hover:border-blue-500 hover:shadow-md transition-all flex items-center justify-center h-32"
        >
          <div className="text-center">
            <span className="mx-auto w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-2">
              <Plus size={24} className="text-gray-600" />
            </span>
            <span className="text-gray-600 font-medium">สร้างห้องเรียนใหม่</span>
          </div>
        </Link>
      </div>
    </div>
  );
}