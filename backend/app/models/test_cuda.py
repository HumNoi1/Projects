from pyexpat import model
import torch

# ตรวจสอบว่า GPU พร้อมใช้งานหรือไม่
if torch.cuda.is_available():
    print("GPU is available")
    # ตรวจสอบว่าโมเดลถูกโหลดบน GPU หรือไม่
    device = torch.device("cuda")
    print(f"Using device: {device}")
else:
    print("GPU is not available, using CPU instead")
    device = torch.device("cpu")
    print(f"Using device: {device}")

# ตรวจสอบว่าโมเดลถูกโหลดบน GPU หรือไม่
model.to(device)