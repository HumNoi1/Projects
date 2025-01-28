// components/Header.tsx
import { BellIcon } from '@heroicons/react/24/outline'
import Image from 'next/image'

const Header = () => {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-semibold text-gray-800">Welcome back!</h1>
        <p className="text-gray-600">Let&apos;s grade some assignments</p>
      </div>
      
      <div className="flex items-center space-x-4">
        <button className="p-2 text-gray-600 hover:bg-gray-100 rounded-full">
          <BellIcon className="w-6 h-6" />
        </button>
        <div className="flex items-center space-x-3">
          <span className="text-gray-700">Teacher Name</span>
          <div className="w-10 h-10 rounded-full overflow-hidden">
            <Image
              src="/avatar-placeholder.jpg"
              alt="Profile"
              width={40}
              height={40}
              className="object-cover"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Header