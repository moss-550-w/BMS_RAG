import os
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from src.data_processor import BMSDataProcessor
from src.vector_store import BMSVectorStore
from src.retriever import BMSRetriever
from src.generator import BMSGenerator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="BMS RAG API Server",
    description="电池管理系统 (BMS) 专业领域 RAG 问答系统后端 API",
    version="1.0.0"
)

# 全局组件初始化 (懒加载)
class RAGComponents:
    def __init__(self):
        self.processor = BMSDataProcessor("./papers")
        self.vector_store_manager = BMSVectorStore("faiss_index")
        self.vectorstore = self.vector_store_manager.load_index()
        self.generator = None
        self.is_indexing = False

    def reload_index(self):
        self.vectorstore = self.vector_store_manager.load_index()
        return self.vectorstore

    def get_generator(self):
        if self.generator is None:
            self.generator = BMSGenerator()
        return self.generator

rag = RAGComponents()

# --- Pydantic 模型 ---
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    rerank: bool = True
    embedding_provider: Optional[str] = None

class Citation(BaseModel):
    content: str
    metadata: dict

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]

class StatusResponse(BaseModel):
    papers_count: int
    index_loaded: bool
    is_indexing: bool
    papers_list: List[str]

# --- API 路由 ---

@app.get("/api/v1/status", response_model=StatusResponse)
async def get_status():
    """获取系统状态和论文库信息"""
    return {
        "papers_count": len(rag.processor.papers),
        "index_loaded": rag.vectorstore is not None,
        "is_indexing": rag.is_indexing,
        "papers_list": rag.processor.papers
    }

@app.post("/api/v1/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """执行 RAG 检索与生成"""
    if rag.vectorstore is None:
        rag.reload_index()
        if rag.vectorstore is None:
            raise HTTPException(status_code=400, detail="向量索引未加载，请先重建索引。")

    # 动态切换引擎逻辑 (简单实现)
    if request.embedding_provider:
        os.environ["EMBEDDING_PROVIDER"] = request.embedding_provider
        # 注意：这里会影响全局状态，演示环境下暂且如此
        rag.vector_store_manager = BMSVectorStore("faiss_index")
        rag.reload_index()

    try:
        retriever = BMSRetriever(rag.vectorstore)
        generator = rag.get_generator()
        
        # 检索
        relevant_docs = retriever.retrieve(request.query)
        # 生成
        answer = generator.generate_answer(request.query, relevant_docs)
        
        citations = [
            Citation(content=doc.page_content, metadata=doc.metadata) 
            for doc in relevant_docs
        ]
            
        return QueryResponse(answer=answer, citations=citations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检索生成失败: {str(e)}")

@app.post("/api/v1/rewrite")
async def rewrite_query(request: QueryRequest):
    """问题重写接口"""
    if rag.vectorstore is None:
        rag.reload_index()
        
    try:
        retriever = BMSRetriever(rag.vectorstore)
        rewritten = retriever.rewrite_query(request.query)
        return {"rewritten_query": rewritten}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"问题重写失败: {str(e)}")

def background_rebuild_task():
    """后台索引重建任务"""
    rag.is_indexing = True
    try:
        print("开始后台重建索引...")
        raw_docs = rag.processor.process_all_papers()
        split_docs = rag.processor.split_documents(raw_docs)
        rag.vectorstore = rag.vector_store_manager.build_index(split_docs)
        print("索引重建完成。")
    except Exception as e:
        print(f"索引重建失败: {e}")
    finally:
        rag.is_indexing = False

@app.post("/api/v1/index/rebuild")
async def rebuild_index(background_tasks: BackgroundTasks):
    """触发向量索引重建"""
    if rag.is_indexing:
        return {"message": "索引正在重建中，请勿重复操作"}
    
    background_tasks.add_task(background_rebuild_task)
    return {"message": "索引重建任务已启动"}

if __name__ == "__main__":
    import uvicorn
    # 支持从环境变量获取端口，默认 8000
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
