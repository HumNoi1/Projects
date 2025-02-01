export default function Home() {
  return (
    <div className="h-screen flex items-center justify-center">
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold text-zinc-800">AutoGrader</h1>
        <p className="text-xl text-zinc-600">AI-Powered Assignment Grading System</p>
        <div className="flex gap-4 justify-center mt-8">
          <a href="/classes" className="px-8 py-3 bg-zinc-800 text-white rounded-lg hover:bg-zinc-700">
            Get Started
          </a>
          <a href="/about" className="px-8 py-3 bg-white text-zinc-800 rounded-lg hover:bg-zinc-100">
            Learn More
          </a>
        </div>
      </div>
    </div>
  )
 }