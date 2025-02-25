import os
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex, ServiceContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.milvus import MilvusVectorStore
from pymilvus import connections, utility

# โหลดตัวแปรจาก .env
load_dotenv()

# ตั้งค่าสำหรับ LM Studio OpenAI compatible API
os.environ["OPENAI_API_BASE"] = os.getenv("LMSTUDIO_API_BASE")
os.environ["OPENAI_API_KEY"] = "not-needed"

def test_llamaindex_basic():
    """ทดสอบการทำงานพื้นฐานของ LlamaIndex"""
    try:
        # สร้างเอกสารทดสอบ
        documents = [
            Document(text="LlamaIndex คือเฟรมเวิร์กที่ช่วยในการสร้างแอปพลิเคชันที่ใช้ LLM โดยมี RAG พื้นฐานรองรับ"),
            Document(text="RAG (Retrieval Augmented Generation) คือเทคนิคในการเพิ่มข้อมูลให้กับ LLM โดยการดึงข้อมูลที่เกี่ยวข้องก่อนการสร้างคำตอบ")
        ]
        
        # ตั้งค่า LLM และ Embedding model
        llm = OpenAI(
            model=os.getenv("LLM_MODEL_NAME"),
            temperature=0.7
        )
        
        embed_model = OpenAIEmbedding(
            model_name=os.getenv("EMBEDDING_MODEL_NAME"),
            embed_batch_size=10
        )
        
        # ตั้งค่า node parser
        node_parser = SentenceSplitter(
            chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200"))
        )
        
        # ตั้งค่า service context
        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            node_parser=node_parser
        )
        
        # สร้าง index จากเอกสาร
        index = VectorStoreIndex.from_documents(
            documents,
            service_context=service_context
        )
        
        print("✅ สร้าง VectorStoreIndex สำเร็จ")
        
        # ทดสอบการค้นหา
        query_engine = index.as_query_engine()
        response = query_engine.query("LlamaIndex คืออะไร?")
        
        print("✅ การสืบค้นสำเร็จ")
        print(f"การตอบกลับ: {response}")
        
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทดสอบ LlamaIndex: {str(e)}")
        return False

def test_llamaindex_milvus():
    """ทดสอบการใช้ LlamaIndex กับ Milvus"""
    try:
        # เชื่อมต่อกับ Milvus
        connections.connect(
            alias="default",
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530")
        )
        
        # กำหนดชื่อ collection
        collection_name = "llamaindex_test"
        
        # ลบ collection เดิมถ้ามี
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f"ลบ collection {collection_name} เดิม")
        
        # สร้าง vector store
        vector_store = MilvusVectorStore(
            collection_name=collection_name,
            dim=int(os.getenv("EMBEDDING_DIMENSION", "384")),
            overwrite=True
        )
        
        # สร้างเอกสารทดสอบ
        documents = [
            Document(text="LlamaIndex คือเฟรมเวิร์กที่ช่วยในการสร้างแอปพลิเคชันที่ใช้ LLM โดยมี RAG พื้นฐานรองรับ"),
            Document(text="RAG (Retrieval Augmented Generation) คือเทคนิคในการเพิ่มข้อมูลให้กับ LLM โดยการดึงข้อมูลที่เกี่ยวข้องก่อนการสร้างคำตอบ")
        ]
        
        # ตั้งค่า LLM และ Embedding model
        llm = OpenAI(
            model=os.getenv("LLM_MODEL_NAME"),
            temperature=0.7
        )
        
        embed_model = OpenAIEmbedding(
            model_name=os.getenv("EMBEDDING_MODEL_NAME"),
            embed_batch_size=10
        )
        
        # ตั้งค่า node parser
        node_parser = SentenceSplitter(
            chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200"))
        )
        
        # ตั้งค่า service context
        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            node_parser=node_parser
        )
        
        # สร้าง index และบันทึกใน Milvus
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=vector_store.get_storage_context(),
            service_context=service_context
        )
        
        print("✅ สร้าง VectorStoreIndex และบันทึกใน Milvus สำเร็จ")
        
        # ทดสอบการค้นหา
        query_engine = index.as_query_engine()
        response = query_engine.query("RAG คืออะไร?")
        
        print("✅ การสืบค้นจาก Milvus สำเร็จ")
        print(f"การตอบกลับ: {response}")
        
        # ลบ collection เพื่อทำความสะอาด
        utility.drop_collection(collection_name)
        print(f"ลบ collection {collection_name} สำเร็จ")
        
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทดสอบ LlamaIndex กับ Milvus: {str(e)}")
        return False

if __name__ == "__main__":
    print("ทดสอบการทำงานพื้นฐานของ LlamaIndex...")
    basic_success = test_llamaindex_basic()
    
    if basic_success:
        print("\nทดสอบการใช้ LlamaIndex กับ Milvus...")
        test_llamaindex_milvus()