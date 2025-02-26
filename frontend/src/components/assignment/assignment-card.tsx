// frontend/components/assignment/assignment-card.tsx
import React from 'react';
import Link from 'next/link';
import { Assignment } from '../../lib/types/assignment';

interface AssignmentCardProps {
  assignment: Assignment;
}

export const AssignmentCard: React.FC<AssignmentCardProps> = ({ assignment }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow">
      <h3 className="text-lg font-semibold text-gray-900">{assignment.title}</h3>
      <p className="mt-2 text-gray-600 line-clamp-3">{assignment.description}</p>
      
      <div className="mt-4 flex justify-between items-center">
        <div className="text-sm text-gray-500">
          สร้างเมื่อ: {new Date(assignment.created_at).toLocaleDateString('th-TH')}
        </div>
        
        <div className="flex space-x-2">
          <Link href={`/assignments/${assignment.id}`} className="text-blue-600 hover:text-blue-800 text-sm font-medium">
            ดูรายละเอียด
          </Link>
        </div>
      </div>
    </div>
  );
};