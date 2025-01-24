import torch
from llama_cpp import Llama
import os

def check_available_gpus():
    print("Checking available GPUs...")
    
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        print(f"Found {gpu_count} CUDA GPU(s):")
        
        for i in range(gpu_count):
            # ดึงข้อมูลพื้นฐานของ GPU
            gpu_name = torch.cuda.get_device_name(i)
            props = torch.cuda.get_device_properties(i)
            gpu_memory = props.total_memory / 1024**3  # แปลงเป็น GB
            
            print(f"GPU {i}: {gpu_name} (Memory: {gpu_memory:.2f} GB)")
            print(f"   - Compute Capability: {props.major}.{props.minor}")
            print(f"   - Multi Processors: {props.multi_processor_count}")
    else:
        print("No CUDA GPUs found")
        gpu_count = 0
    
    return gpu_count

def initialize_llama(model_path):
    gpu_count = check_available_gpus()
    
    print(f"\nInitializing Llama model...")
    try:
        if gpu_count > 0:
            print("Configuring model for GPU usage...")
            # สำหรับ RTX 3050 4GB เราจะใช้การตั้งค่าที่ประหยัด memory
            llm = Llama(
                model_path=model_path,
                n_ctx=1024,
                n_batch=256,
                n_threads=6,
                n_gpu_layers=32,        # เพิ่มจำนวน layers ที่จะรันบน GPU
                main_gpu=0,
                offload_kv=True,        # เพิ่มตัวเลือกนี้เพื่อ offload KV cache ไปยัง GPU
                gpu_layers=[0,1],       # ระบุ layers ที่จะรันบน GPU
                seed=42,
                numa=True              # เปิดใช้ NUMA optimization
            )
            print("Model loaded successfully on GPU")
        else:
            print("Configuring model for CPU usage...")
            llm = Llama(
                model_path=model_path,
                n_ctx=1024,
                n_batch=256,
                n_threads=6,
                n_gpu_layers=0
            )
            print("Model loaded successfully on CPU")
            
        return llm
        
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        raise

def test_model(llm):
    print("\nTesting model with a simple prompt...")
    test_prompt = "What is artificial intelligence?"
    try:
        response = llm(
            test_prompt, 
            max_tokens=128,        # ลดจำนวน tokens เพื่อการทดสอบ
            temperature=0.7,
            top_p=0.95,
            echo=False
        )
        print(f"\nPrompt: {test_prompt}")
        print(f"Response: {response['choices'][0]['text'].strip()}")
    except Exception as e:
        print(f"Error during inference: {str(e)}")

if __name__ == "__main__":
    # ตรวจสอบและโหลดโมเดล
    model_path = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    
    # เริ่มต้นโมเดลและทดสอบ
    llm = initialize_llama(model_path)
    test_model(llm)