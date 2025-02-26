// frontend/app/assignments/[id]/page.tsx
import React from 'react';
import Link from 'next/link';
import { getAssignment } from '../../../lib/api/assignments';
import { Button } from '../../../components/ui/button';
import { UploadTeacherFile } from './upload-teacher-file';

interface AssignmentPageProps {
  params: {
    id: string;
  };
}

export default async function AssignmentPage({ params }: AssignmentPageProps) {
  const assignment = await getAssignment(params.id);
  
  return (
    <div className="py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">{assignment.title}</h1>
        <div className="flex space-x-3">
          <Link href={`/assignments/${params.id}/submit`}>
            <Button>ส่งงาน</Button>
          </Link>
          <Link href={`/assignments/${params.id}/grade`}>
            <Button variant="secondary">ตรวจงาน</Button>
          </Link>
        </div>
      </div>
      
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">รายละเอียดงาน</h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">สร้างเมื่อ {new Date(assignment.created_at).toLocaleDateString('th-TH')}</p>
        </div>
        <div className="border-t border-gray-200">
          <dl>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">คำอธิบาย</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{assignment.description}</dd>
            </div>
          </dl>
        </div>
      </div>
      
      {/* Teacher file upload component */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">เฉลยของครู</h2>
        <UploadTeacherFile assignmentId={params.id} />
      </div>
    </div>
  );
}