// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Auto Grading System',
  description: 'Automated grading system powered by LLM',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gradient-to-br from-blue-50/30 to-purple-50/30`}>
        <div className="min-h-screen flex">
          <Sidebar />
          <main className="flex-1 p-8">
            <Header />
            <div className="mt-6">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  )
}