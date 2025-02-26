// frontend/lib/api/assignments.ts
import { Assignment } from '../types/assignment';

// Define the API_URL constant at the top of your file
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getAssignments(): Promise<Assignment[]> {
  // Note: This endpoint isn't shown in the provided files, so this is an assumption
  const response = await fetch(`${API_URL}/assignments`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get assignments');
  }

  return response.json();
}

export async function getAssignment(id: string): Promise<Assignment> {
  // Note: This endpoint isn't shown in the provided files, so this is an assumption
  const response = await fetch(`${API_URL}/assignments/${id}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get assignment');
  }

  return response.json();
}

export async function createAssignment(assignment: Omit<Assignment, 'id' | 'created_at' | 'updated_at'>): Promise<Assignment> {
  // Note: This endpoint isn't shown in the provided files, so this is an assumption
  const response = await fetch(`${API_URL}/assignments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(assignment),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to create assignment');
  }

  return response.json();
}