export interface GradingRequest {
    student_id: string;
}

export interface GradingResponse {
    assignment_id: string;
    student_id: string;
    score: number;
    feedback: string;
    strengths: string[];
    areas_for_improvement: string[];
    missed_concepts: string[];
}

export interface BatchGradingRequest {
    assignment_id: string;
}

export interface BatchGradingResponse {
    batch_id: string;
    results: GradingResponse[];
    completed: boolean;
}