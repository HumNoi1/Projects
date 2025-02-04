// frontend/hooks/useAssignment.ts
import { useState, useEffect } from 'react';
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
import type { Assignment } from '@/types/database';

export function useAssignment(assignmentId: string) {
  const [assignment, setAssignment] = useState<Assignment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  const supabase = createClientComponentClient();

  useEffect(() => {
    async function fetchAssignment() {
      try {
        const { data, error } = await supabase
          .from('assignments')
          .select('*')
          .eq('id', assignmentId)
          .single();

        if (error) throw error;
        setAssignment(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    }

    if (assignmentId) {
      fetchAssignment();
    }
  }, [assignmentId, supabase]);

  return { assignment, loading, error };
}