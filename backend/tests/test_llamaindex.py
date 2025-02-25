import os
import sys
from dotenv import load_dotenv
import traceback

print("กำลังเริ่มการทดสอบ...")
print(f"Python version: {sys.version}")

try:
    print("กำลังโหลดโมดูล LlamaIndex...")
    from llama_index.core import Document, VectorStoreIndex
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.core.settings import Settings
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.vector_stores.milvus import MilvusVectorStore
    from pymilvus import connections, utility
    print("โหลดโมดูลเรียบร้อย")
except ImportError as e:
    print(f"❌ เกิดข้อผิดพลาดในการโหลดโมดูล: {e}")
    print("โปรดตรวจสอบว่าได้ติดตั้ง LlamaIndex และ dependencies ครบถ้วนแล้ว")
    traceback.print_exc()
    sys.exit(1)

# โหลดตัวแปรจาก .env
print("กำลังโหลดตัวแปรจาก .env...")
load_dotenv()
lmstudio_api_base = os.getenv("LMSTUDIO_API_BASE")
embedding_model = os.getenv("EMBEDDING_MODEL_NAME")
llm_model = os.getenv("LLM_MODEL_NAME")

print(f"LM Studio API Base: {lmstudio_api_base}")
print(f"Embedding Model: {embedding_model}")
print(f"LLM Model: {llm_model}")

# ตั้งค่าสำหรับ LM Studio OpenAI compatible API
os.environ["OPENAI_API_BASE"] = lmstudio_api_base
os.environ["OPENAI_API_KEY"] = "not-needed"

def test_llamaindex_basic():
    print("\n----- ทดสอบการทำงานพื้นฐานของ LlamaIndex -----")
    try:
        print("1. กำลังสร้างเอกสารทดสอบ...")
        documents = [
            Document(text="LlamaIndex คือเฟรมเวิร์กที่ช่วยในการสร้างแอปพลิเคชันที่ใช้ LLM"),
            Document(text="RAG คือเทคนิคในการเพิ่มข้อมูลให้กับ LLM โดยการดึงข้อมูลที่เกี่ยวข้อง")
        ]
        print("สร้างเอกสารทดสอบเรียบร้อย")
        
        print("2. กำลังตั้งค่า LLM...")
        llm = OpenAI(
            model=llm_model,
            temperature=0.7
        )
        print("ตั้งค่า LLM เรียบร้อย")
        
        print("3. กำลังตั้งค่า Embedding model...")
        embed_model = OpenAIEmbedding(
            model_name=embedding_model,
            embed_batch_size=10
        )
        print("ตั้งค่า Embedding model เรียบร้อย")
        
        print("4. กำลังตั้งค่า node parser...")
        node_parser = SentenceSplitter(
            chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200"))
        )
        print("ตั้งค่า node parser เรียบร้อย")
        
        print("5. กำลังตั้งค่า Settings...")
        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.node_parser = node_parser
        print("ตั้งค่า Settings เรียบร้อย")
        
        print("6. กำลังสร้าง index...")
        index = VectorStoreIndex.from_documents(documents)
        print("✅ สร้าง VectorStoreIndex สำเร็จ")
        
        print("7. กำลังทดสอบการค้นหา...")
        query_engine = index.as_query_engine()
        response = query_engine.query("LlamaIndex คืออะไร?")
        print("✅ การสืบค้นสำเร็จ")
        print(f"การตอบกลับ: {response}")
        
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทดสอบ LlamaIndex: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_llamaindex_basic()