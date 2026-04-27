import os
import re
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class BMSDataProcessor:
    def __init__(self, papers_dir: str):
        self.papers_dir = papers_dir
        self.papers = self._list_papers()
        
    def _list_papers(self) -> List[str]:
        return [f for f in os.listdir(self.papers_dir) if f.endswith('.pdf')]

    def clean_text(self, text: str) -> str:
        # 1. 合并被分页打断的单词
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        # 2. 统一BMS术语 (如 "SOC" 统一为 "State of Charge (SOC)")
        # 注意：这里只做简单的替换，实际可能需要更复杂的逻辑
        # text = text.replace("SOC", "State of Charge (SOC)")
        # 3. 去除页码、页眉页脚 (简单处理，复杂处理需根据PDF结构)
        text = re.sub(r'\n\d+\n', '\n', text)
        # 4. 去除多余空格
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def process_all_papers(self) -> List[Document]:
        all_docs = []
        for i, paper_name in enumerate(self.papers, 1):
            paper_path = os.path.join(self.papers_dir, paper_name)
            loader = PyPDFLoader(paper_path)
            pages = loader.load()
            
            paper_docs = []
            for page in pages:
                # 清洗文本
                cleaned_content = self.clean_text(page.page_content)
                
                # 更新元数据
                metadata = page.metadata
                metadata.update({
                    "paper_id": i,
                    "paper_title": paper_name,
                    "page_number": metadata.get("page", 0) + 1,
                    "source": paper_name
                })
                
                # 识别章节 (简单启发式：大写或带编号的行)
                # section_match = re.search(r'^[1-9]\.?\s+[A-Z].*', cleaned_content, re.MULTILINE)
                # metadata["section"] = section_match.group(0) if section_match else "Unknown"
                
                paper_docs.append(Document(page_content=cleaned_content, metadata=metadata))
            
            all_docs.extend(paper_docs)
        
        return all_docs

    def split_documents(self, documents: List[Document]) -> List[Document]:
        # 语义分块策略：800 tokens, 200 overlap
        # 使用 RecursiveCharacterTextSplitter 模拟按章节、段落分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )
        return text_splitter.split_documents(documents)

if __name__ == "__main__":
    processor = BMSDataProcessor("./papers")
    raw_docs = processor.process_all_papers()
    split_docs = processor.split_documents(raw_docs)
    print(f"Processed {len(raw_docs)} pages into {len(split_docs)} chunks.")
    if split_docs:
        print(f"Sample Metadata: {split_docs[0].metadata}")
