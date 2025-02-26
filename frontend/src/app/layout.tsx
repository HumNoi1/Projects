// frontend/app/layout.tsx
import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Sidebar from '@/components/ui/sidebar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Grading LLM',
  description: 'ระบบตรวจงานอัตโนมัติด้วย LLM',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="th">
      <body className={inter.className}>
        <div className="flex">
          <Sidebar />
          <div className="ml-64 flex-1 p-6">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}