// frontend/app/assignments/page.tsx
import React from 'react';
import Link from 'next/link';
import { getAssignments } from '../../lib/api/assignments';
import { AssignmentCard } from '../../components/assignment/assignment-card';
import { Button } from '../../components/ui/button';

export default async function AssignmentsPage() {
  // This is a server component, so we can fetch data directly
  const assignments = await getAssignments();
  
  return (
    <div className="py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">งานทั้งหมด</h1>
        <Link href="/assignments/create">
          <Button>สร้างงานใหม่</Button>
        </Link>
      </div>
      
      {assignments.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-gray-500">ยังไม่มีงาน</p>
          <div className="mt-4">
            <Link href="/assignments/create">
              <Button>สร้างงานใหม่</Button>
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {assignments.map((assignment) => (
            <AssignmentCard key={assignment.id} assignment={assignment} />
          ))}
        </div>
      )}
    </div>
  );
}