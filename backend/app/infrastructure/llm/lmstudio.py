from langchain_community.llms import LlamaCpp
from langchain_community.chat_models import ChatOpenAI
from app.core.config import settings
import os

class LMStudioClient:
    def __init__(self):
        self.api_base = settings.LMSTUDIO_URL
        self.model_name = settings.LMSTUDIO_MODEL
    
    def get_chat_model(self):
        """
        Get a Langchain chat model that connects to LMStudio.
        """
        # Using OpenAI compatible API offered by LMStudio
        return ChatOpenAI(
            model=self.model_name,
            temperature=0.2,
            api_key="not-needed", # LMStudio typically doesn't need an API key
            base_url=self.api_base
        )
    
    def get_local_model(self, model_path):
        """
        Load a local model using LlamaCpp for direct inference.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        return LlamaCpp(
            model_path=model_path,
            temperature=0.2,
            max_tokens=2000,
            top_p=0.95,
            verbose=True
        )