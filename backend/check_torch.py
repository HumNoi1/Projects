from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from llama_cpp import Llama

# โหลดโมเดลและ tokenizer
model_name = "app/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf"  # หรือโมเดลอื่นที่คุณต้องการใช้
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# ย้ายโมเดลไปยัง GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# ตัวอย่างการใช้งาน
text = "Hello, how are"
inputs = tokenizer(text, return_tensors="pt").to(device)
outputs = model.generate(**inputs)
result = tokenizer.decode(outputs[0])
print(result)