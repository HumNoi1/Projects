// components/Sidebar.tsx
import { HomeIcon, BookOpenIcon, ClipboardIcon, UserGroupIcon, ChartBarIcon, CogIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

const Sidebar = () => {
  const menuItems = [
    { name: 'Dashboard', icon: HomeIcon, href: '/' },
    { name: 'Assignments', icon: ClipboardIcon, href: '/assignments' },
    { name: 'Grading', icon: BookOpenIcon, href: '/grading' },
    { name: 'Classes', icon: UserGroupIcon, href: '/classes' },
    { name: 'Analytics', icon: ChartBarIcon, href: '/analytics' },
    { name: 'Settings', icon: CogIcon, href: '/settings' },
  ]

  return (
    <div className="w-64 bg-white/60 backdrop-blur-xl border-r border-gray-200">
      <div className="h-16 flex items-center px-6">
        <h1 className="text-2xl font-bold text-blue-600">AutoGrade</h1>
      </div>
      <nav className="mt-4">
        {menuItems.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className="flex items-center px-6 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600"
          >
            <item.icon className="w-5 h-5 mr-3" />
            {item.name}
          </Link>
        ))}
      </nav>
    </div>
  )
}

export default Sidebar