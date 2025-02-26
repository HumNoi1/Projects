// frontend/src/app/layout.tsx
import React from 'react';
import { Navbar } from '../components/layout/navbar';
import './globals.css';

export const metadata = {
  title: 'ระบบตรวงานอัตโนมัติ',
  description: 'ระบบตรวจงานอัตโนมัติโดยใช้ LLM',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        <Navbar />
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </main>
      </body>
    </html>
  );
}