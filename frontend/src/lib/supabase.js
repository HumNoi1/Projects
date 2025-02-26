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
export async function getClassById(classId) {
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
export async function getAssignmentsByClassId(classId) {
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