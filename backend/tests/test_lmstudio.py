import asyncio
import os
import httpx
import json
import os
from dotenv import load_dotenv

# load enviroment variables
load_dotenv()

API_BASE = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234")
API_KEY = os.getenv("LLM_MODEL_NAME", "bartowski/Llama-3.2-3B-Instruct-GGUF")

async def test_lmstudio_connection():
    print(f"Testing connection to LMStudio API at {API_BASE}...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # ทดสอบเชื่อมต่อกับ LMStudio API
            response = await client.get(f"{API_BASE}/v1/models")
            response.raise_for_status()
            models = response.json()
            print(f"✅ Connected to LMStudio API at {API_BASE}")
            
            # ทดสอบ chat completion API
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is 2+2?"}
            ]
            
            response = await client.post(
                f"{API_BASE}/v1/chat/completions",
                json={
                    "model": "bartowski/Llama-3.2-3B-Instruct-GGUF",
                    "messages": messages,
                    "max_tokens": 100,
                    "temperature": 0.7,
                }
            )
            response.raise_for_status()
            result = response.json()
            
            print("\nChat completion test result:")
            print(f"Response: {result['choices'][0]['message']['content']}")
            print("\n✅ LM-Studio connection successful!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error connecting to LM-Studio: {str(e)}")
        print("\nPlease check that:")
        print("1. LM-Studio is running")
        print("2. API Server is enabled in LM-Studio settings")
        print("3. The API URL in .env file is correct")
        print("4. The model is loaded in LM-Studio")
        return False

if __name__ == "__main__":
    asyncio.run(test_lmstudio_connection())