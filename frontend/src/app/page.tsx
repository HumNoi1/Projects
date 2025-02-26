// frontend/app/page.tsx
import React from 'react';
import Link from 'next/link';
import { Button } from '../components/ui/button';

export default function Home() {
  return (
    <div className="py-10">
      <header>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold leading-tight text-gray-900">
            ยินดีต้อนรับสู่ระบบตรวจงานอัตโนมัติด้วย AI
          </h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <div className="px-4 py-8 sm:px-0">
            <div className="border-4 border-dashed border-gray-200 rounded-lg p-10">
              <div className="text-center">
                <h2 className="text-2xl font-semibold text-gray-900">
                  เริ่มต้นใช้งานระบบตรวจงานอัตโนมัติ
                </h2>
                <p className="mt-4 text-gray-600">
                  ระบบนี้ช่วยให้คุณสามารถตรวจงานนักเรียนได้อย่างรวดเร็วและแม่นยำโดยใช้ AI
                </p>
                
                <div className="mt-8 flex justify-center space-x-4">
                  <Link href="/assignments">
                    <Button size="lg">
                      ดูงานทั้งหมด
                    </Button>
                  </Link>
                  <Link href="/assignments/create">
                    <Button variant="secondary" size="lg">
                      สร้างงานใหม่
                    </Button>
                  </Link>
                </div>
                
                <div className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-3">
                  <div className="bg-white shadow rounded-lg p-6">
                    <h3 className="text-lg font-semibold">อัปโหลดเฉลย</h3>
                    <p className="mt-2 text-gray-600">
                      อัปโหลดเฉลยของคุณในรูปแบบไฟล์ PDF
                    </p>
                  </div>
                  
                  <div className="bg-white shadow rounded-lg p-6">
                    <h3 className="text-lg font-semibold">รับงานนักเรียน</h3>
                    <p className="mt-2 text-gray-600">
                      รับงานนักเรียนในรูปแบบไฟล์ PDF
                    </p>
                  </div>
                  
                  <div className="bg-white shadow rounded-lg p-6">
                    <h3 className="text-lg font-semibold">ตรวจงานอัตโนมัติ</h3>
                    <p className="mt-2 text-gray-600">
                      ระบบจะใช้ AI เพื่อตรวจงานและให้ข้อเสนอแนะโดยอัตโนมัติ
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}