import os
from typing import List
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from openai import OpenAI

load_dotenv()

class ArkEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        batch_size = 250
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = self.client.embeddings.create(
                input=batch,
                model=self.model
            )
            results.extend([data.embedding for data in response.data])
        return results

    def embed_query(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=[text],
            model=self.model
        )
        return response.data[0].embedding

class BMSVectorStore:
    def __init__(self, index_path: str = "faiss_index"):
        self.index_path = index_path
        provider = os.getenv("EMBEDDING_PROVIDER", "volcengine").lower()
        
        if provider == "alibabacloud":
            from langchain_community.embeddings import DashScopeEmbeddings
            self.embeddings = DashScopeEmbeddings(
                model=os.getenv("EMBEDDING_ENDPOINT_ID", "text-embedding-v3"),
                dashscope_api_key=os.getenv("EMBEDDING_API_KEY")
            )
            print(f"Using Alibaba Cloud Embeddings: {os.getenv('EMBEDDING_ENDPOINT_ID')}")
        else:
            # 默认使用火山引擎
            self.embeddings = ArkEmbeddings(
                api_key=os.getenv("ARK_API_KEY"),
                model=os.getenv("EMBEDDING_ENDPOINT_ID")
            )
            print(f"Using Volcengine Embeddings: {os.getenv('EMBEDDING_ENDPOINT_ID')}")

    def build_index(self, documents: List[Document]):
        print(f"Building index with {len(documents)} chunks...")
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        vectorstore.save_local(self.index_path)
        print(f"Index saved to {self.index_path}")
        return vectorstore

    def load_index(self):
        if os.path.exists(self.index_path):
            return FAISS.load_local(
                self.index_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        return None

    def search(self, query: str, k: int = 10):
        vectorstore = self.load_index()
        if vectorstore:
            return vectorstore.similarity_search(query, k=k)
        return []
