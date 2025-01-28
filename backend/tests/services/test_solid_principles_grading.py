# Standard library imports
import pytest
from datetime import datetime
from typing import List, Dict

# Third-party imports
from unittest.mock import patch, AsyncMock

# Local application imports
from app.services.grading_service import GradingService
from app.services.llm_service import LLMService
from app.models.grading import (
    GradingCriteria,  # สำหรับกำหนดเกณฑ์การให้คะแนน
    GradingResult,    # สำหรับเก็บผลการตรวจ
    GradingRequest    # สำหรับสร้างคำขอการตรวจ
)

# Setup logging
import logging
logger = logging.getLogger(__name__)

@pytest.fixture
def se_reference_answer():
    """
    คำตอบมาตรฐานจากอาจารย์เกี่ยวกับหลักการ SOLID ในวิศวกรรมซอฟต์แวร์
    คำตอบนี้ครอบคลุมประเด็นสำคัญและมีการอธิบายที่ชัดเจน
    """
    return """
    SOLID Principles เป็นหลักการออกแบบซอฟต์แวร์ที่สำคัญในการพัฒนาระบบเชิงวัตถุ (OOP) ประกอบด้วย:

    1. Single Responsibility Principle (SRP)
    - หลักการความรับผิดชอบเดียว
    - แต่ละคลาสควรมีหน้าที่รับผิดชอบเพียงอย่างเดียว
    - ช่วยให้โค้ดมีความชัดเจน บำรุงรักษาง่าย และลดผลกระทบเมื่อต้องแก้ไข

    2. Open-Closed Principle (OCP)
    - หลักการเปิดปิด
    - ซอฟต์แวร์ควรเปิดรับการขยาย แต่ปิดสำหรับการแก้ไข
    - ใช้การสืบทอดและ interface แทนการแก้ไขโค้ดเดิม

    3. Liskov Substitution Principle (LSP)
    - หลักการแทนที่ของ Liskov
    - คลาสลูกต้องสามารถแทนที่คลาสแม่ได้โดยไม่ทำให้โปรแกรมผิดพลาด
    - รักษาความสอดคล้องของ behavior ระหว่างคลาสแม่และคลาสลูก

    4. Interface Segregation Principle (ISP)
    - หลักการแยก interface
    - ไม่ควรบังคับให้คลาสต้อง implement method ที่ไม่ได้ใช้
    - แยก interface ใหญ่เป็น interface เล็กๆ ที่เฉพาะเจาะจง

    5. Dependency Inversion Principle (DIP)
    - หลักการพึ่งพาแบบผกผัน
    - โมดูลระดับสูงไม่ควรพึ่งพาโมดูลระดับต่ำโดยตรง
    - ควรพึ่งพา abstraction แทนการพึ่งพา implementation

    การนำ SOLID Principles ไปใช้จะช่วยให้ซอฟต์แวร์มีความยืดหยุ่น บำรุงรักษาง่าย 
    และรองรับการเปลี่ยนแปลงในอนาคต
    """

@pytest.fixture
def student_answers():
    """
    คำตอบของนักเรียน 5 คนที่มีความเข้าใจและการอธิบายในระดับที่แตกต่างกัน
    """
    return [
        {
            "student_id": "6001",
            "answer": """
            SOLID Principles มี 5 ข้อ คือ
            1. Single Responsibility - คลาสควรมีหน้าที่เดียว
            2. Open-Closed - เปิดให้ขยาย ปิดการแก้ไข
            3. Liskov Substitution - คลาสลูกต้องแทนที่คลาสแม่ได้
            4. Interface Segregation - แยก interface ให้เล็กลง
            5. Dependency Inversion - ใช้ abstraction แทน implementation
            ทั้งหมดนี้ช่วยให้โค้ดดีขึ้น แก้ไขง่ายขึ้น
            """
        },
        {
            "student_id": "6002",
            "answer": """
            SOLID Principles เป็นหลักการสำคัญในการออกแบบซอฟต์แวร์เชิงวัตถุ
            Single Responsibility หมายถึงคลาสควรมีหน้าที่เดียว เช่น คลาส UserRepository 
            ควรจัดการเฉพาะการเก็บข้อมูล User

            Open-Closed คือการออกแบบให้ขยายฟังก์ชันได้โดยไม่ต้องแก้โค้ดเดิม 
            ใช้ inheritance หรือ interface

            Liskov Substitution ต้องให้คลาสลูกทำงานแทนคลาสแม่ได้ถูกต้อง 
            เช่น Square ต้องทำงานเหมือน Rectangle

            Interface Segregation คือการแยก interface ให้เล็กและตรงจุดประสงค์
            ไม่ควรมี interface ใหญ่ที่มี method เยอะเกินจำเป็น

            Dependency Inversion ใช้ abstraction แทนการพึ่งพา concrete class โดยตรง
            ทำให้เปลี่ยน implementation ได้ง่าย
            """
        },
        {
            "student_id": "6003",
            "answer": """
            Solid มี Single responsibility คือทำงานเดียว
            Open closed คือเปิดปิด
            Liskov คือเปลี่ยนแทนกันได้
            Interface คือแยกส่วน
            Dependency คือการพึ่งพา
            """
        },
        {
            "student_id": "6004",
            "answer": """
            SOLID Principles ประกอบด้วย:
            1. Single Responsibility Principle คือการที่คลาสควรมีหน้าที่รับผิดชอบเพียงอย่างเดียว
            เพื่อให้โค้ดมีความชัดเจนและแก้ไขง่าย

            2. Open-Closed Principle คือการออกแบบให้สามารถเพิ่มความสามารถใหม่ได้
            โดยไม่ต้องแก้ไขโค้ดเดิม ใช้การสืบทอดหรือ interface

            3. Liskov Substitution Principle กำหนดว่าคลาสลูกต้องสามารถทำงานแทนคลาสแม่ได้
            โดยไม่ทำให้โปรแกรมทำงานผิดพลาด

            4. Interface Segregation Principle คือการแยก interface ให้มีขนาดเล็ก
            และมีความเฉพาะเจาะจง ไม่ควรบังคับให้คลาสต้อง implement method ที่ไม่จำเป็น

            5. Dependency Inversion Principle คือการพึ่งพา abstraction แทน concrete class
            ทำให้โค้ดยืดหยุ่นและเปลี่ยนแปลงได้ง่าย

            การใช้ SOLID ช่วยให้โค้ดมีคุณภาพดี บำรุงรักษาง่าย และปรับเปลี่ยนได้ในอนาคต
            """
        },
        {
            "student_id": "6005",
            "answer": """
            SOLID principles คือแนวทางการเขียนโค้ดให้ดี คือ
            S - Single responsibility ทำงานแค่อย่างเดียว
            O - Open closed ขยายได้แต่แก้ไม่ได้
            L - Liskov substitution คลาสลูกแทนที่คลาสแม่
            I - Interface segregation แยก interface เล็กๆ
            D - Dependency inversion ใช้ abstract แทน concrete

            จริงๆแล้วผมไม่เข้าใจว่าทำไมต้องใช้ SOLID 
            การเขียนโค้ดธรรมดาก็ได้ไม่เห็นต้องยุ่งยาก
            """
        }
    ]

@pytest.fixture
def grading_criteria():
    """
    เกณฑ์การให้คะแนนที่ครอบคลุมทั้งความเข้าใจและการอธิบาย
    """
    return [
        GradingCriteria(
            name="ความครบถ้วนของเนื้อหา",
            description="อธิบายครบทุกหลักการและใจความสำคัญ",
            max_score=10.0,
            weight=0.4
        ),
        GradingCriteria(
            name="ความถูกต้องของการอธิบาย",
            description="อธิบายแต่ละหลักการได้ถูกต้อง ชัดเจน",
            max_score=10.0,
            weight=0.3
        ),
        GradingCriteria(
            name="การยกตัวอย่างและการประยุกต์ใช้",
            description="มีการยกตัวอย่างและอธิบายการนำไปใช้",
            max_score=10.0,
            weight=0.3
        )
    ]

@pytest.mark.asyncio
async def test_batch_grading_solid_principles(
    se_reference_answer,
    student_answers,
    grading_criteria
):
    """
    ทดสอบการตรวจให้คะแนนคำตอบเกี่ยวกับ SOLID Principles ของนักเรียน 5 คน
    พร้อมแสดงผลการให้คะแนนโดยละเอียด
    """
    grading_service = GradingService()
    results = []

    print("\nผลการตรวจข้อสอบ SOLID Principles:")
    print("=" * 80)

    for student in student_answers:
        result = await grading_service.grade_answer(
            reference_answer=se_reference_answer,
            student_answer=student["answer"],
            criteria=grading_criteria,
            language="th"
        )
        results.append({
            "student_id": student["student_id"],
            "result": result
        })

        # แสดงผลการตรวจของแต่ละคน
        print(f"\nนักเรียนรหัส: {student['student_id']}")
        print("-" * 40)
        print(f"คะแนนรวม: {result.total_score:.2f}/10")
        print("\nคะแนนแยกตามเกณฑ์:")
        for criterion_name, score in result.criteria_scores.items():
            print(f"- {criterion_name}: {score:.2f}/10")
        print("\nความคิดเห็นจากผู้ตรวจ:")
        print(result.feedback)
        print("\nความมั่นใจในการตรวจ: {:.1%}".format(result.confidence_score))
        print("-" * 80)

    # ตรวจสอบความถูกต้องของการให้คะแนน
    assert len(results) == 5, "ควรมีผลการตรวจครบทั้ง 5 คน"
    
    for result in results:
        assert isinstance(result["result"], GradingResult), (
            "ผลการตรวจต้องเป็น GradingResult"
        )
        assert 0 <= result["result"].total_score <= 10, (
            "คะแนนรวมต้องอยู่ในช่วง 0-10"
        )
        assert len(result["result"].criteria_scores) == len(grading_criteria), (
            "ต้องมีคะแนนครบทุกเกณฑ์"
        )
        assert 0.5 <= result["result"].confidence_score <= 1.0, (
            "ความมั่นใจในการตรวจต้องอยู่ในระดับที่ยอมรับได้"
        )

    # คำนวณและแสดงสถิติของคะแนน
    total_scores = [r["result"].total_score for r in results]
    avg_score = sum(total_scores) / len(total_scores)
    max_score = max(total_scores)
    min_score = min(total_scores)

    print("\nสรุปผลการตรวจ:")
    print(f"คะแนนเฉลี่ย: {avg_score:.2f}")
    print(f"คะแนนสูงสุด: {max_score:.2f}")
    print(f"คะแนนต่ำสุด: {min_score:.2f}")