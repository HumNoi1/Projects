"use client";

import React from 'react';
import Navbar from '@/app/components/Navbar';
import { BarChart, Users, BookOpen, CheckSquare } from 'lucide-react';

const DashboardPage = () => {
  const stats = [
    {
      title: 'ชั้นเรียนทั้งหมด',
      value: '12',
      icon: BookOpen,
      trend: '+2 จากเดือนที่แล้ว'
    },
    {
      title: 'นักเรียนทั้งหมด',
      value: '486',
      icon: Users,
      trend: '+18 จากเดือนที่แล้ว'
    },
    {
      title: 'งานที่ต้องตรวจ',
      value: '34',
      icon: CheckSquare,
      trend: '12 งานใหม่วันนี้'
    },
    {
      title: 'คะแนนเฉลี่ย',
      value: '78.5',
      icon: BarChart,
      trend: '+2.1% จากเดือนที่แล้ว'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto py-6 px-4">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">แดชบอร์ด</h1>
        
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex items-center justify-between pb-2">
                <h3 className="text-sm font-medium text-gray-500">{stat.title}</h3>
                <stat.icon className="h-5 w-5 text-gray-400" />
              </div>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-gray-500 mt-1">{stat.trend}</p>
            </div>
          ))}
        </div>

        <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-4">งานที่ต้องตรวจล่าสุด</h2>
            <div className="space-y-4">
              <table className="min-w-full">
                <thead className="border-b">
                  <tr role="row">
                    <th className="text-left text-sm text-gray-500 pb-3">ชั้นเรียน</th>
                    <th className="text-left text-sm text-gray-500 pb-3">งาน</th>
                    <th className="text-left text-sm text-gray-500 pb-3">กำหนดส่ง</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  <tr role="row">
                    <td className="py-3">ม.6/1</td>
                    <td className="py-3">แบบฝึกหัด บทที่ 4</td>
                    <td className="py-3">วันนี้</td>
                  </tr>
                  <tr role="row">
                    <td className="py-3">ม.5/2</td>
                    <td className="py-3">รายงานการทดลอง</td>
                    <td className="py-3">พรุ่งนี้</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-4">ชั้นเรียนที่กำลังสอน</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b">
                <div>
                  <h3 className="font-medium">ม.6/1 วิทยาศาสตร์</h3>
                  <p className="text-sm text-gray-500">นักเรียน 42 คน</p>
                </div>
                <button className="text-blue-600 hover:text-blue-800">
                  ดูรายละเอียด
                </button>
              </div>
              <div className="flex items-center justify-between py-3 border-b">
                <div>
                  <h3 className="font-medium">ม.5/2 ฟิสิกส์</h3>
                  <p className="text-sm text-gray-500">นักเรียน 38 คน</p>
                </div>
                <button className="text-blue-600 hover:text-blue-800">
                  ดูรายละเอียด
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;