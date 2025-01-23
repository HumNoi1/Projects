import React from 'react';
import { Brain, Sparkles } from 'lucide-react';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white/10 backdrop-blur-lg rounded-2xl shadow-xl p-8 space-y-8">
        <div className="text-center space-y-2">
          <div className="flex justify-center gap-2">
            <Brain className="w-10 h-10 text-purple-400" />
            <Sparkles className="w-10 h-10 text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            AI Grading System
          </h1>
          <p className="text-gray-300">Powered by LLM Technology</p>
        </div>

        <form className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-200">Email</label>
            <input
              type="email"
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-gray-600 text-gray-100 focus:border-purple-400 focus:ring-purple-400"
              placeholder="your@email.com"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-200">Password</label>
            <input
              type="password"
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-gray-600 text-gray-100 focus:border-purple-400 focus:ring-purple-400"
              placeholder="••••••••"
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="flex items-center">
              <input type="checkbox" className="w-4 h-4 rounded border-gray-600 text-purple-500" />
              <span className="ml-2 text-sm text-gray-300">Remember me</span>
            </label>
            <a href="#" className="text-sm text-purple-400 hover:text-purple-300">
              Forgot password?
            </a>
          </div>

          <div className="space-y-4">
            <Link
                href="/dashboard"
                className="w-full py-3 px-4 bg-gradient-to-r from-purple-400 to-blue-400 text-white rounded-lg font-medium hover:from-purple-500 hover:to-blue-500 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 focus:ring-offset-gray-900 text-center"
            >
                Sign in
            </Link>
            <button
              type="button"
              className="w-full py-3 px-4 bg-transparent border-2 border-purple-400 text-purple-400 rounded-lg font-medium hover:bg-purple-400/10 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 focus:ring-offset-gray-900"
            >
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}