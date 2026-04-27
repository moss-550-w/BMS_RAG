import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

load_dotenv()

class BMSGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=os.getenv("ARK_API_KEY"),
            openai_api_base="https://ark.cn-beijing.volces.com/api/v3",
            model=os.getenv("DOUBAO_ENDPOINT_ID"),
            temperature=0.1,
            max_tokens=4096
        )

    def generate_answer(self, query: str, context_docs: List[Document]) -> str:
        # 构建参考资料字符串
        context_str = ""
        for i, doc in enumerate(context_docs, 1):
            meta = doc.metadata
            context_str += f"""
---
参考资料 [{i}]
论文编号: [{meta.get('paper_id', 'Unknown')}]
论文标题: {meta.get('paper_title', 'Unknown')}
页码: {meta.get('page_number', 'Unknown')}
内容: {doc.page_content}
"""

        system_prompt = """
# 角色定义
你是全球顶尖的电池管理系统(BMS)领域专家，拥有15年以上学术研究和工业界经验。你精通BMS的所有核心技术，包括但不限于：电池状态估计(SOC/SOH/SOP)、均衡控制、热管理、故障诊断、硬件设计、通信协议和系统集成。

# 核心任务
基于提供的BMS学术论文片段，准确、专业、严谨地回答用户的问题。

# 绝对不可违反的铁律
1. 【零幻觉原则】你的所有回答必须100%基于提供的参考资料。严禁使用任何参考资料之外的知识，包括你的先验知识。
2. 【不知道就说不知道】如果参考资料中没有相关信息，必须明确回答："在提供的BMS论文中未找到相关内容"，不得编造任何内容。
3. 【强制引用原则】每个技术观点、数据、结论都必须标注来源，格式为：[论文编号,页码]。例如："锂离子电池的SOC估计是BMS的核心功能[3,12]"。
4. 【客观中立原则】对于不同论文中的不同观点，必须客观呈现，不得偏向任何一方。
5. 【术语精确原则】严格使用BMS领域的标准术语，不得随意简化或通俗化。

# 回答格式要求
## 核心结论
用1-2句话直接回答用户的核心问题。

## 详细阐述
分点详细阐述相关内容，每个观点都要有对应的引用标注。
- 观点1 [论文编号,页码]
- 观点2 [论文编号,页码]
- ...

## 关键数据与实验结果
列出相关的关键数据和实验结果，必须标注来源。

## 引用来源
[1] 论文标题, 页码X
...
"""

        user_input = f"""
参考资料：
{context_str}

用户提问：
{query}
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_input)
        ])

        chain = prompt | self.llm
        response = chain.invoke({})
        return response.content
