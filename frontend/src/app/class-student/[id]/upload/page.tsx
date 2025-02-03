// frontend/app/class-student/[id]/upload/page.tsx
import { Metadata } from "next";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Upload } from "lucide-react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Upload Assignment - Grading with LLM",
  description: "Upload student assignments for grading",
};

export default function UploadPage({ params }: { params: { id: string } }) {
  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Upload Assignment</h1>
      <p>Class ID: {params.id}</p> {/* Use the params prop */}
      
      <Card>
        <CardHeader>
          <CardTitle>Upload Files</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <Label htmlFor="assignmentTitle">Assignment Title</Label>
              <Input id="assignmentTitle" placeholder="Enter assignment title" />
            </div>
            
            <div>
              <Label htmlFor="file">Assignment File (PDF)</Label>
              <div className="mt-2">
                <Input
                  id="file"
                  type="file"
                  accept=".pdf"
                  className="cursor-pointer"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2">
            <Button variant="outline">
                <Link href="/class-student">
                    Cancel
                </Link>
            </Button>
              <Button>
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}