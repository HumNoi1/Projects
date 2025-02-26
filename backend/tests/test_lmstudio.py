import requests
import os

# ค่าการตั้งค่าที่ใช้สำหรับการทดสอบเท่านั้น
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "llama3")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embedding-model")

def test_lmstudio_connection():
    """
    ทดสอบการเชื่อมต่อกับ LMStudio
    """
    print(f"Testing connection to LMStudio at {LMSTUDIO_URL}...")
    
    # ทดสอบ Completion API
    try:
        completion_url = f"{LMSTUDIO_URL}/completions"
        payload = {
            "model": LMSTUDIO_MODEL,
            "prompt": "Hello, my name is",
            "max_tokens": 50,
            "temperature": 0.7
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        response = requests.post(completion_url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LMStudio Completion API test successful!")
            print(f"Response: {result['choices'][0]['text']}")
        else:
            print(f"❌ LMStudio Completion API test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing LMStudio Completion API: {e}")
    
    # ทดสอบ Embeddings API
    try:
        embeddings_url = f"{LMSTUDIO_URL}/embeddings"
        payload = {
            "model": EMBEDDING_MODEL,
            "input": "This is a test sentence for embeddings."
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        response = requests.post(embeddings_url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LMStudio Embeddings API test successful!")
            print(f"Embedding dimension: {len(result['data'][0]['embedding'])}")
        else:
            print(f"❌ LMStudio Embeddings API test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing LMStudio Embeddings API: {e}")
        print("Note: If this fails, check if your LMStudio supports embeddings API.")
        print("The backup embedding service will be used if this API is not available.")

if __name__ == "__main__":
    test_lmstudio_connection()