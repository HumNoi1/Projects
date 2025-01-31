// lib/api/classes.ts
import { supabase } from '@/lib/supabase'
import { Class, ClassFormData } from '@/types/class'

export async function createClass(data: ClassFormData) {
    try {
        // 1. สร้างชั้นเรียนใหม่
        const { data: classData, error: classError } = await supabase
            .from('classes')
            .insert({
                name: data.name,
                subject: data.subject,
                grade: data.grade,
                description: data.description,
                academic_year: data.academic_year,
                teacher_id: supabase.auth.getUser().then(res => res.data.user?.id)
            })
            .select()
            .single()

        if (classError) throw classError

        // 2. เพิ่มนักเรียนเข้าชั้นเรียน
        if (data.students.length > 0) {
            const { error: studentError } = await supabase
                .from('class_students')
                .insert(
                    data.students.map(student => ({
                        class_id: classData.id,
                        student_email: student.email,
                        student_name: student.name
                    }))
                )

            if (studentError) throw studentError
        }

        return classData
    } catch (error) {
        console.error('Error creating class:', error)
        throw error
    }
}