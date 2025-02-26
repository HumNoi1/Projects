from langchain.chains import LLMChain
from app.infrastructure.llm.lmstudio import LMStudioClient
from app.infrastructure.llm.prompts import grading_prompt
import json

class GradingChain:
    def __init__(self):
        lmstudio_client = LMStudioClient()
        self.llm = lmstudio_client.get_chat_model()
        self.chain = LLMChain(llm=self.llm, prompt=grading_prompt)
    
    async def grade_submission(self, teacher_text: str, student_text: str):
        """
        Grade a student submission using the LLM chain.
        """
        try:
            result = await self.chain.arun(
                teacher_text=teacher_text,
                student_text=student_text
            )
            
            # Parse the JSON response
            grading_result = json.loads(result)
            
            return grading_result
        except Exception as e:
            print(f"Error in grading chain: {str(e)}")
            # Return a fallback result in case of error
            return {
                "score": 0,
                "feedback": f"Error processing submission: {str(e)}",
                "strengths": [],
                "areas_for_improvement": ["Unable to process submission"],
                "missed_concepts": []
            }