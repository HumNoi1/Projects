# tests/test_integration.py
import pytest
from app.services.llm_client import LMStudioLLMClient
from app.services.embedding_service import EmbeddingService
from app.services.grading_service import GradingService, GradingServiceError
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

class TestIntegration:
    """ทดสอบการทำงานร่วมกันของทุกส่วนในระบบ"""

    @pytest.fixture
    def grading_service(self):
        return GradingService()

    @pytest.fixture
    def embedding_service(self):
        return EmbeddingService()

    @pytest.fixture
    def llm_client(self):
        return LMStudioLLMClient()

    @pytest.fixture
    def sample_math_question(self):
        """ตัวอย่างโจทย์คณิตศาสตร์"""
        return {
            "question": "Solve the equation: 2x + 5 = 13",
            "student_answer": "First I subtract 5 from both sides: 2x = 8\nThen divide both sides by 2: x = 4",
            "reference_answer": "2x + 5 = 13\nSubtract 5 from both sides: 2x = 8\nDivide both sides by 2: x = 4\nCheck: 2(4) + 5 = 13 ✓",
            "rubric": {
                "problem_solving": {
                    "weight": 40,
                    "criteria": "Shows clear step-by-step solution"
                },
                "accuracy": {
                    "weight": 40,
                    "criteria": "Arrives at correct answer"
                },
                "verification": {
                    "weight": 20,
                    "criteria": "Verifies the answer"
                }
            }
        }

    @pytest.fixture
    def sample_essay_question(self):
        """ตัวอย่างคำถามเรียงความ"""
        return {
            "question": "Explain the causes of climate change.",
            "student_answer": """Climate change is primarily caused by human activities. The main cause is the burning of fossil fuels like coal and oil, which releases greenhouse gases into the atmosphere. These gases trap heat and cause the Earth's temperature to rise. Deforestation also contributes by reducing the Earth's ability to absorb CO2.""",
            "reference_answer": """Climate change is predominantly driven by human activities. The primary contributor is the emission of greenhouse gases, particularly CO2, through the burning of fossil fuels in industry, transportation, and energy production. These gases create a 'greenhouse effect' by trapping heat in the atmosphere. Additionally, deforestation significantly reduces the Earth's natural carbon sinks, as trees absorb CO2 during photosynthesis. Other factors include industrial processes, agricultural practices, and changes in land use patterns.""",
            "rubric": {
                "content": {
                    "weight": 40,
                    "criteria": "Covers key causes of climate change"
                },
                "understanding": {
                    "weight": 30,
                    "criteria": "Shows clear understanding of mechanisms"
                },
                "completeness": {
                    "weight": 30,
                    "criteria": "Includes both human and environmental factors"
                }
            }
        }

    @pytest.mark.asyncio
    async def test_complete_grading_flow(
        self,
        grading_service,
        embedding_service,
        llm_client,
        sample_math_question,
        sample_essay_question
    ):
        """ทดสอบกระบวนการตรวจงานทั้งหมด"""
        try:
            # ทดสอบการเชื่อมต่อกับ LM-Studio ก่อน
            logger.info("\n=== Testing LM-Studio Connection ===")
            test_response = await llm_client.generate("test")
            if "Error" in test_response:
                pytest.skip(f"LM-Studio is not accessible: {test_response}")

            # 1. ทดสอบการตรวจข้อสอบคณิตศาสตร์
            logger.info("\n=== Math Question Grading Test ===")
            logger.info(f"Question: {sample_math_question['question']}")
            logger.info(f"Student Answer:\n{sample_math_question['student_answer']}")
            logger.info(f"Reference Answer:\n{sample_math_question['reference_answer']}")
            
            math_result = await grading_service.grade_assignment(
                student_answer=sample_math_question['student_answer'],
                reference_answer=sample_math_question['reference_answer'],
                rubric=sample_math_question['rubric']
            )
            
            logger.info("\nMath Grading Result:")
            logger.info(json.dumps(math_result['grading_result'], indent=2))

            # 2. ทดสอบการตรวจเรียงความ
            logger.info("\n=== Essay Grading Test ===")
            logger.info(f"Question: {sample_essay_question['question']}")
            logger.info(f"Student Answer:\n{sample_essay_question['student_answer']}")
            logger.info(f"Reference Answer:\n{sample_essay_question['reference_answer']}")
            
            essay_result = await grading_service.grade_assignment(
                student_answer=sample_essay_question['student_answer'],
                reference_answer=sample_essay_question['reference_answer'],
                rubric=sample_essay_question['rubric']
            )
            
            logger.info("\nEssay Grading Result:")
            logger.info(json.dumps(essay_result['grading_result'], indent=2))

            # 3. ทดสอบการค้นหาความคล้ายคลึง
            logger.info("\n=== Similarity Search Test ===")
            embeddings = await embedding_service.create_embeddings([
                sample_math_question['student_answer'],
                sample_math_question['reference_answer']
            ])
            assert len(embeddings) == 2
            logger.info("Successfully created embeddings for similarity comparison")

            # 4. ทดสอบการให้ข้อเสนอแนะโดยตรงจาก LLM
            logger.info("\n=== Detailed Feedback Generation Test ===")
            feedback = await llm_client.generate(
                prompt=f"""
                Question: {sample_essay_question['question']}
                Student's answer: {sample_essay_question['student_answer']}
                
                Please provide:
                1. Three specific strengths
                2. Three areas for improvement
                3. Suggestions for better understanding of the topic
                """
            )
            logger.info("\nDetailed Feedback:")
            logger.info(feedback)

            # ตรวจสอบผลลัพธ์
            assert math_result['success']
            assert essay_result['success']
            assert 'grading_result' in math_result
            assert 'grading_result' in essay_result
            assert feedback is not None

            logger.info("\n=== All Tests Completed Successfully ===")

        except Exception as e:
            logger.error(f"Integration test failed: {str(e)}")
            raise

    @pytest.mark.asyncio
    async def test_grading_error_handling(self, grading_service):
        """ทดสอบการจัดการข้อผิดพลาดในการตรวจงาน"""
        try:
            # ทดสอบกรณี input ว่าง
            with pytest.raises(GradingServiceError) as exc_info:
                await grading_service.grade_assignment(
                    student_answer="",
                    reference_answer="",
                    rubric={}
                )
            assert "Missing required input" in str(exc_info.value)
            logger.info("Empty input test passed")

            # ทดสอบกรณี rubric ไม่ถูกต้อง
            invalid_rubrics = [
                # rubric ที่ไม่มี weight
                {
                    "content": {
                        "criteria": "Test criteria"
                    }
                },
                # rubric ที่ไม่มี criteria
                {
                    "content": {
                        "weight": 100
                    }
                },
                # rubric ที่มี weight ไม่ใช่ตัวเลข
                {
                    "content": {
                        "weight": "100",
                        "criteria": "Test criteria"
                    }
                }
            ]

            for i, invalid_rubric in enumerate(invalid_rubrics):
                with pytest.raises(GradingServiceError) as exc_info:
                    await grading_service.grade_assignment(
                        student_answer="Test answer",
                        reference_answer="Reference answer",
                        rubric=invalid_rubric
                    )
                logger.info(f"Invalid rubric test {i+1} passed: {str(exc_info.value)}")

        except Exception as e:
            logger.error(f"Error handling test failed: {str(e)}")
            raise