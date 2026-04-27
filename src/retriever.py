import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.documents import Document

load_dotenv()

class BMSRetriever:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.client = OpenAI(
            api_key=os.getenv("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        self.rerank_endpoint = os.getenv("RERANK_ENDPOINT_ID")
        self.doubao_endpoint = os.getenv("DOUBAO_ENDPOINT_ID")

    def rewrite_query(self, query: str) -> str:
        """将用户自然语言提问重写为学术查询式"""
        prompt = f"""
# 任务
将用户关于BMS的自然语言提问转换为更适合语义检索的学术查询式。

# 转换规则
1. 扩展相关的BMS专业术语
2. 修正可能的拼写错误和术语错误
3. 明确模糊的概念和表述
4. 保持问题的核心意图不变
5. 只输出优化后的查询式，不要添加任何其他解释

# 示例
用户提问：BMS怎么估计电池电量？
优化后：电池管理系统(BMS)中荷电状态(SOC)的估计方法

用户提问：{query}
优化后："""
        
        response = self.client.chat.completions.create(
            model=self.doubao_endpoint,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def rerank(self, query: str, documents: List[Document], top_n: int = 3) -> List[Document]:
        """使用火山引擎 Rerank API 对结果进行重排序"""
        if not documents:
            return []
            
        # 准备 Rerank 输入
        # 注意：这里假设火山引擎有 Rerank API 接口，如果暂时没有，可以使用简单的相关性过滤
        # 由于 volcengine SDK 的 Rerank 接口可能随版本变化，这里提供一个逻辑框架
        
        # 简单模拟：过滤相似度低于 0.6 的结果 (FAISS 默认是 L2 距离，需转换或使用 similarity_search_with_score)
        # 这里为了演示，我们假设只取前 top_n 个，实际中应调用 Rerank API
        
        # 如果要调用真实的 Rerank API (假设 endpoint 支持):
        # try:
        #     # 具体的 Rerank 调用逻辑
        #     pass
        # except Exception as e:
        #     print(f"Rerank failed: {e}")
        
        return documents[:top_n]

    def retrieve(self, query: str) -> List[Document]:
        # 1. 查询重写
        try:
            rewritten_query = self.rewrite_query(query)
            print(f"优化后的查询: {rewritten_query}")
        except Exception as e:
            print(f"查询重写失败，使用原查询: {e}")
            rewritten_query = query
        
        # 2. 向量检索
        docs = self.vectorstore.similarity_search(rewritten_query, k=10)
        
        # 3. 重排序
        final_docs = self.rerank(rewritten_query, docs, top_n=3)
        
        return final_docs
