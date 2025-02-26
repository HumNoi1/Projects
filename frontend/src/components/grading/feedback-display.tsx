// frontend/components/grading/feedback-display.tsx
import React from 'react';
import { GradingResponse } from '../../lib/types/grading';

interface FeedbackDisplayProps {
  gradingResult: GradingResponse;
}

export const FeedbackDisplay: React.FC<FeedbackDisplayProps> = ({ gradingResult }) => {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900">ผลการตรวจงาน</h3>
        <p className="mt-1 text-sm text-gray-500">
          รหัสงาน: {gradingResult.assignment_id}
        </p>
        <p className="mt-1 text-sm text-gray-500">
          รหัสนักเรียน: {gradingResult.student_id}
        </p>
      </div>
      
      <div>
        <h4 className="text-md font-medium text-gray-900">คะแนน</h4>
        <div className="mt-2">
          <div className="flex items-center">
            <div className="text-3xl font-bold text-blue-600">{gradingResult.score}</div>
            <span className="ml-2 text-gray-500">คะแนน</span>
          </div>
        </div>
      </div>
      
      <div>
        <h4 className="text-md font-medium text-gray-900">ข้อเสนอแนะ</h4>
        <p className="mt-2 text-gray-700">{gradingResult.feedback}</p>
      </div>
      
      <div>
        <h4 className="text-md font-medium text-green-700">จุดเด่น</h4>
        <ul className="mt-2 space-y-1 list-disc list-inside">
          {gradingResult.strengths.map((strength, index) => (
            <li key={index} className="text-gray-700">{strength}</li>
          ))}
        </ul>
      </div>
      
      <div>
        <h4 className="text-md font-medium text-amber-700">จุดที่ควรปรับปรุง</h4>
        <ul className="mt-2 space-y-1 list-disc list-inside">
          {gradingResult.areas_for_improvement.map((area, index) => (
            <li key={index} className="text-gray-700">{area}</li>
          ))}
        </ul>
      </div>
      
      {gradingResult.missed_concepts.length > 0 && (
        <div>
          <h4 className="text-md font-medium text-red-700">แนวคิดที่ยังไม่เข้าใจ</h4>
          <ul className="mt-2 space-y-1 list-disc list-inside">
            {gradingResult.missed_concepts.map((concept, index) => (
              <li key={index} className="text-gray-700">{concept}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};