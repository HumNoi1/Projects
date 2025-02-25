// frontend/src/components/StatusIndicator.tsx
'use client';

import { useEffect, useState } from 'react';
import { HealthService } from '@/services/api';
import { CheckCircle, XCircle } from 'lucide-react';

export function StatusIndicator() {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);

  useEffect(() => {
    async function checkBackendStatus() {
      try {
        await HealthService.checkStatus();
        setIsOnline(true);
      } catch (error) {
        console.error('Backend health check failed:', error);
        setIsOnline(false);
      }
    }

    checkBackendStatus();
    // ตรวจสอบทุก 30 วินาที
    const interval = setInterval(checkBackendStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  if (isOnline === null) {
    return <span className="text-gray-500">Checking server status...</span>;
  }

  return (
    <div className="flex items-center">
      {isOnline ? (
        <>
          <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
          <span className="text-green-600">Server Online</span>
        </>
      ) : (
        <>
          <XCircle className="w-4 h-4 text-red-500 mr-2" />
          <span className="text-red-600">Server Offline</span>
        </>
      )}
    </div>
  );
}