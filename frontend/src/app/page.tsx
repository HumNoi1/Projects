// frontend/app/page.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold">Welcome to Grading with LLM</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Quick Grade</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="mb-4">Start grading student assignments instantly with our LLM-powered system.</p>
            <Link href="/grading">
              <Button>Start Grading</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Batch Grading</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="mb-4">Grade multiple students at once with our batch grading feature.</p>
            <Link href="/batch">
              <Button>Batch Grading</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Class Management</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="mb-4">Manage your classes and student information efficiently.</p>
            <Link href="/class-student">
              <Button variant="outline">View Classes</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Your recent grading activities will appear here.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}