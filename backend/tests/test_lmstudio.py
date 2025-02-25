import requests
import os
from dotenv import load_dotenv

# โหลดตัวแปรจาก .env
load_dotenv()
api_base = os.getenv("LMSTUDIO_API_BASE")

def test_lmstudio_connection():
    """ทดสอบการเชื่อมต่อกับ LM Studio API"""
    try:
        # ทดสอบ model list endpoint
        response = requests.get(f"{api_base}/models")
        if response.status_code == 200:
            print("✅ สามารถเชื่อมต่อกับ LM Studio API ได้สำเร็จ")
            models = response.json()
            print(f"โมเดลที่มีให้ใช้งาน: {models}")
            return True
        else:
            print(f"❌ ไม่สามารถเชื่อมต่อกับ LM Studio API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อกับ LM Studio: {str(e)}")
        return False

def test_lmstudio_completion():
    """ทดสอบการส่งคำขอไปยัง LM Studio API"""
    try:
        # ทดสอบ chat completion endpoint
        payload = {
            "model": os.getenv("LLM_MODEL_NAME"),
            "messages": [
                {"role": "system", "content": "คุณเป็นผู้ช่วยที่เป็นประโยชน์"},
                {"role": "user", "content": "สวัสดี ช่วยอธิบายว่า LLM คืออะไร?"}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(f"{api_base}/chat/completions", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ สามารถเรียกใช้ LM Studio API สำหรับ chat completion ได้สำเร็จ")
            print(f"การตอบกลับ: {result['choices'][0]['message']['content'][:100]}...")
            return True
        else:
            print(f"❌ ไม่สามารถเรียกใช้ LM Studio API สำหรับ chat completion: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการเรียกใช้ LM Studio API: {str(e)}")
        return False

if __name__ == "__main__":
    print("ทดสอบการเชื่อมต่อกับ LM Studio...")
    connection_success = test_lmstudio_connection()
    
    if connection_success:
        print("\nทดสอบการส่งคำขอไปยัง LM Studio...")
        test_lmstudio_completion()