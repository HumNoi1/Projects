// frontend/app/components/Navbar.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Bell, User } from 'lucide-react';

const Navbar = () => {
  const pathname = usePathname();
  
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/dashboard" className="text-xl font-bold text-gray-800">
              Auto Grading
            </Link>
            <div className="ml-10 flex space-x-4">
              <Link href="/classes" 
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname?.includes('/classes') 
                    ? 'bg-gray-100 text-gray-900' 
                    : 'text-gray-500 hover:text-gray-900'
                }`}>
                ชั้นเรียน
              </Link>
              <Link href="/dashboard/assignments"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname?.includes('/assignments')
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-500 hover:text-gray-900'
                }`}>
                งานที่มอบหมาย
              </Link>
              <Link href="/dashboard/students"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname?.includes('/students')
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-500 hover:text-gray-900'
                }`}>
                นักเรียน
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button
              aria-label="notification"
              className="p-2 rounded-full text-gray-500 hover:text-gray-900">
              <Bell className="h-5 w-5" />
            </button>
            <button
              aria-label="profile"
              className="p-2 rounded-full text-gray-500 hover:text-gray-900">
              <User className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;