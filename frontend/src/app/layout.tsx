// src/app/layout.tsx
import { Inter } from 'next/font/google'
import './globals.css'
import Sidebar from '@/components/sidebar'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
 }: {
  children: React.ReactNode
 }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex min-h-screen bg-zinc-50">
          <Sidebar />
          <main className="flex-1">{children}</main>
        </div>
      </body>
    </html>
  )
 }