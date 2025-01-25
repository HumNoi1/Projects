from llama_cpp import Llama
import os
import torch

# ทดสอบการโหลดโมเดลด้วย GPU
llm = Llama(
    model_path="models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    n_gpu_layers=-1,  # ใช้ทุก layer บน GPU
    verbose=True
)

# ควรเห็น log การทำงานที่แสดงการใช้ CUDA/cuBLAS