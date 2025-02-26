// frontend/components/layout/navbar.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export const Navbar: React.FC = () => {
  const pathname = usePathname();
  
  const isActive = (path: string) => {
    return pathname?.startsWith(path) ? 'bg-blue-900 text-white' : 'text-gray-300 hover:bg-blue-800 hover:text-white';
  };
  
  return (
    <nav className="bg-blue-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Link href="/" className="text-white font-bold text-xl">
                ระบบตรวจงานอัตโนมัติ
              </Link>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link href="/assignments" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/assignments')}`}>
                  งานทั้งหมด
                </Link>
                <Link href="/batch-grading" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/batch-grading')}`}>
                  ตรวจงานแบบกลุ่ม
                </Link>
                <Link href="/results" className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/results')}`}>
                  ผลคะแนน
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}