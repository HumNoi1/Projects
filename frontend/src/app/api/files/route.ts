// frontend/app/api/files/route.ts
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const supabase = createRouteHandlerClient({ cookies });
  
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    const fileType = formData.get('fileType') as 'teacher' | 'student';
    const assignmentId = formData.get('assignmentId') as string;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // อัปโหลดไฟล์ไปยัง storage bucket
    const bucketName = fileType === 'teacher' ? 'teacher_files' : 'student_files';
    const filePath = `${assignmentId}/${file.name}`;
    
    const { data: uploadData, error: uploadError } = await supabase.storage
      .from(bucketName)
      .upload(filePath, file);

    if (uploadError) throw uploadError;

    // บันทึกข้อมูลลงใน files table
    const { data: fileRecord, error: insertError } = await supabase
      .from('files')
      .insert({
        file_name: file.name,
        file_path: filePath,
        file_type: fileType,
        file_size: file.size,
        mime_type: file.type,
        assignment_id: assignmentId,
      })
      .select()
      .single();

    if (insertError) throw insertError;

    return NextResponse.json(fileRecord);
  } catch (error) {
    console.error('Error uploading file:', error);
    return NextResponse.json(
      { error: 'Failed to upload file' },
      { status: 500 }
    );
  }
}