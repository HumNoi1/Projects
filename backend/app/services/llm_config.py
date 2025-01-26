from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMConfig:
    _instance = None
    _model = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.model_file = settings.MODEL_FILE  # ชื่อไฟล์ .gguf
        self.n_gpu_layers = settings.N_GPU_LAYERS  # จำนวน layers ที่จะโหลดบน GPU
        
    def load_model(self):
        """โหลดโมเดล GGUF จาก HuggingFace"""
        if self._model is None:
            try:
                logger.info(f"Downloading model {self.model_name}")
                # ดาวน์โหลดไฟล์โมเดลจาก HuggingFace
                model_path = hf_hub_download(
                    repo_id=self.model_name,
                    filename=self.model_file,
                    token=settings.HUGGINGFACE_TOKEN
                )
                
                logger.info(f"Loading model from {model_path}")
                # โหลดโมเดลด้วย llama-cpp-python
                self._model = Llama(
                    model_path=model_path,
                    n_gpu_layers=self.n_gpu_layers,  # -1 คือใช้ทุก layers
                    n_ctx=2048,  # context window size
                    n_batch=512   # batch size
                )
                
                logger.info("Model loaded successfully!")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise
                
        return self._model
    
    def get_model(self):
        """ส่งคืนโมเดล"""
        return self.load_model()