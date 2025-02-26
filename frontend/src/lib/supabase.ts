// frontend/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

// ตรวจสอบว่ามีการกำหนดค่า environment variables
if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
  throw new Error('Missing Supabase environment variables')
}

// สร้าง Supabase client
export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

// เพิ่มประเภทข้อมูลสำหรับห้องเรียน
export interface ClassData {
  id?: string;
  name: string;
  description?: string;
  created_by?: string;
}

// ฟังก์ชันสำหรับดึงข้อมูลคลาสทั้งหมด
export async function getAllClasses() {
  const { data, error } = await supabase
    .from('classes')
    .select('*')
    .order('created_at', { ascending: false })

  if (error) {
    console.error('Error fetching classes:', error)
    return []
  }

  return data || []
}

// ฟังก์ชันสำหรับดึงข้อมูลคลาสเดียว
export async function getClassById(classId: string) {
  const { data, error } = await supabase
    .from('classes')
    .select('*')
    .eq('id', classId)
    .single()

  if (error) {
    console.error('Error fetching class:', error)
    return null
  }

  return data
}

// ฟังก์ชันสำหรับดึงข้อมูลงานในคลาส
export async function getAssignmentsByClassId(classId: string) {
  const { data, error } = await supabase
    .from('assignments')
    .select('*')
    .eq('class_id', classId)
    .order('created_at', { ascending: false })

  if (error) {
    console.error('Error fetching assignments:', error)
    return []
  }

  return data || []
}

// เพิ่มฟังก์ชันสำหรับสร้างห้องเรียนใหม่
export async function createClass(classData: ClassData) {
  // เพิ่ม timestamp ให้กับข้อมูล
  const newClass = {
    ...classData,
    created_at: new Date().toISOString(),
    assignment_count: 0, // เริ่มต้นที่ 0 เนื่องจากเป็นห้องเรียนใหม่
  };

  const { data, error } = await supabase
    .from('classes')
    .insert([newClass])
    .select('*')
    .single();

  if (error) {
    console.error('Error creating class:', error);
    throw new Error(`ไม่สามารถสร้างห้องเรียนได้: ${error.message}`);
  }

  return data;
}

// ฟังก์ชันสำหรับดึงข้อมูลผู้ใช้ที่กำลังล็อกอินอยู่
export async function getCurrentUser() {
  const { data: { user }, error } = await supabase.auth.getUser();
  
  if (error) {
    console.error('Error fetching current user:', error);
    return null;
  }
  
  return user;
}