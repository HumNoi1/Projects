// frontend/components/ui/sidebar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, BookOpen, Settings } from 'lucide-react';

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="h-screen bg-gray-100 w-64 fixed left-0 top-0 p-4 border-r">
      <div className="mb-6">
        <h1 className="text-xl font-bold">Grading LLM</h1>
      </div>
      
      <nav>
        <ul className="space-y-2">
          <li>
            <Link 
              href="/"
              className={`flex items-center p-2 rounded ${
                pathname === '/' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-200'
              }`}
            >
              <Home size={18} className="mr-2" />
              <span>หน้าหลัก</span>
            </Link>
          </li>
          <li>
            <Link 
              href="/classes"
              className={`flex items-center p-2 rounded ${
                pathname.startsWith('/classes') ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-200'
              }`}
            >
              <BookOpen size={18} className="mr-2" />
              <span>ห้องเรียน</span>
            </Link>
          </li>
          <li>
            <Link 
              href="/settings"
              className={`flex items-center p-2 rounded ${
                pathname.startsWith('/settings') ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-200'
              }`}
            >
              <Settings size={18} className="mr-2" />
              <span>ตั้งค่า</span>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}