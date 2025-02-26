// app/classes/create/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ChevronLeft, Loader2 } from 'lucide-react';
import { createClass, getCurrentUser } from '@/lib/supabase';

// Add this interface at the top of your file or in a separate types file
interface User {
  id: string;
  email?: string;
  // Add other user properties as needed
}

export default function CreateClassPage() {
  const [className, setClassName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const router = useRouter();

  // ดึงข้อมูลผู้ใช้ปัจจุบัน
  useEffect(() => {
    async function fetchCurrentUser() {
      const user = await getCurrentUser();
      setCurrentUser(user);
    }
    fetchCurrentUser();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!className.trim()) {
      setError('กรุณากรอกชื่อห้องเรียน');
      return;
    }
    
    setLoading(true);
    setError(null);

    try {
      // สร้างห้องเรียนใหม่ใน Supabase
      await createClass({
        name: className.trim(),
        description: description.trim(),
        created_by: currentUser?.id,
      });
      
      // แสดงข้อความหรือทำการรีไดเร็กไปยังหน้ารายการห้องเรียน
      router.push('/classes');
      router.refresh(); // เพื่อรีโหลดข้อมูลใหม่ในหน้ารายการห้องเรียน
    } catch (err: unknown) {
      // Type-safe error handling
      setError(
        err instanceof Error ? err.message : 'เกิดข้อผิดพลาดในการสร้างห้องเรียน'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <Link 
          href="/classes"
          className="flex items-center text-blue-500 hover:underline"
        >
          <ChevronLeft size={16} className="mr-1" />
          กลับไปยังรายการห้องเรียน
        </Link>
      </div>

      <h1 className="text-2xl font-bold mb-6">สร้างห้องเรียนใหม่</h1>

      <form onSubmit={handleSubmit} className="max-w-xl space-y-4">
        <div>
          <label htmlFor="class-name" className="block text-sm font-medium mb-1">ชื่อห้องเรียน <span className="text-red-500">*</span></label>
          <input
            id="class-name"
            type="text"
            value={className}
            onChange={(e) => setClassName(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
            placeholder="กรอกชื่อห้องเรียน"
          />
        </div>

        <div>
          <label htmlFor="class-description" className="block text-sm font-medium mb-1">คำอธิบาย</label>
          <textarea
            id="class-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            rows={4}
            placeholder="อธิบายเกี่ยวกับห้องเรียนนี้"
          />
        </div>

        {error && (
          <div className="bg-red-100 text-red-600 p-3 rounded-md">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 rounded-md flex items-center justify-center ${
            loading ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600 text-white'
          }`}
        >
          {loading ? (
            <>
              <Loader2 size={20} className="animate-spin mr-2" />
              กำลังสร้างห้องเรียน...
            </>
          ) : 'สร้างห้องเรียน'}
        </button>
      </form>
    </div>
  );
}