"use client";

import { Brain, Sparkles, Mail } from 'lucide-react';

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md text-center space-y-6">
        <div className="flex justify-center space-x-2">
          <Brain className="w-8 h-8 text-blue-600" />
          <Sparkles className="w-8 h-8 text-blue-600" />
        </div>

        <Mail className="w-16 h-16 text-blue-600 mx-auto" />
        
        <h2 className="text-2xl font-bold text-gray-900">Check your email</h2>
        <p className="text-gray-500">
          We sent you a verification link. Please check your email to verify your account.
        </p>

        <a 
          href="/auth/login" 
          className="block w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          Return to login
        </a>
      </div>
    </div>
  );
}