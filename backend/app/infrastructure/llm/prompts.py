from langchain.prompts import PromptTemplate

GRADING_TEMPLATE = """
You are an expert grader for educational assignments. You will be given:
1. A teacher's answer key
2. A student's submission

Your task is to grade the student's work fairly and provide constructive feedback.

Teacher's Answer Key:
{teacher_text}

Student's Submission:
{student_text}

Please analyze the student's work and provide:
1. A numerical score out of 100
2. Detailed feedback explaining the score
3. Point out specific strengths and areas for improvement
4. Identify any key concepts the student has missed or misunderstood

Your response should be in the following JSON format:
{{
    "score": <numerical_score>,
    "feedback": "<detailed_feedback>",
    "strengths": ["<strength1>", "<strength2>", ...],
    "areas_for_improvement": ["<area1>", "<area2>", ...],
    "missed_concepts": ["<concept1>", "<concept2>", ...]
}}
"""

grading_prompt = PromptTemplate(
    input_variables=["teacher_text", "student_text"],
    template=GRADING_TEMPLATE
)