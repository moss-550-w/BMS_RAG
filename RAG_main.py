import os
import argparse
from dotenv import load_dotenv
from src.data_processor import BMSDataProcessor
from src.vector_store import BMSVectorStore
from src.retriever import BMSRetriever
from src.generator import BMSGenerator

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="BMS RAG System")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the vector database")
    args = parser.parse_args()

    # 1. 初始化组件
    processor = BMSDataProcessor("./papers")
    vector_store_manager = BMSVectorStore("faiss_index")
    
    # 2. 检查或构建向量库
    vectorstore = vector_store_manager.load_index()
    if args.rebuild or vectorstore is None:
        print("Indexing papers... this may take a while.")
        raw_docs = processor.process_all_papers()
        split_docs = processor.split_documents(raw_docs)
        vectorstore = vector_store_manager.build_index(split_docs)
    
    # 3. 初始化检索器和生成器
    retriever = BMSRetriever(vectorstore)
    generator = BMSGenerator()

    print("\n" + "="*50)
    print("欢迎使用 BMS 领域专业 RAG 问答系统")
    print("系统已加载 8 篇 BMS 学术论文")
    print("输入 'exit' 或 'quit' 退出系统")
    print("="*50 + "\n")

    while True:
        query = input("\n请输入您的 BMS 相关问题: ").strip()
        if query.lower() in ['exit', 'quit']:
            break
        if not query:
            continue

        try:
            print(f"正在检索相关资料...")
            relevant_docs = retriever.retrieve(query)
            
            if not relevant_docs:
                print("未找到相关参考资料。")
                continue

            print(f"正在生成专业回答...")
            answer = generator.generate_answer(query, relevant_docs)
            
            print("\n" + "-"*30 + " 系统回答 " + "-"*30)
            print(answer)
            print("-" * 70)
            
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
