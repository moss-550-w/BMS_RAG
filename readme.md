# BMS 领域专业 RAG 问答系统项目报告

## 一、 项目概述
本项目旨在基于 8 篇 BMS（电池管理系统）学术论文 PDF 构建一个专业问答系统。系统严格基于论文内容回答，确保“零幻觉”，并提供精确的论文引用溯源，适配学术研究与工程实践。

## 二、 核心功能
- **学术级精准问答**：答案 100% 来源于提供的论文，严禁引入外部先验知识。
- **精确引用溯源**：每个技术观点均标注对应的 [论文编号, 页码]。
- **BMS 专属查询重写**：将用户口语化提问重写为学术检索式，提升检索准确度。
- **多引擎支持**：支持火山引擎 (Ark) 与 阿里云 (DashScope) 双向量化引擎。
- **本地持久化**：采用 FAISS 进行向量存储，支持索引本地保存与增量更新。

## 三、 系统架构
系统采用经典的 RAG (Retrieval-Augmented Generation) 架构并进行了领域增强：
1.  **数据层**：使用 `PyPDFLoader` 解析 PDF，通过自定义清洗逻辑处理 BMS 术语与分页打断。
2.  **存储层**：利用 `FAISS` 实现本地向量库，结合 `ArkEmbeddings` 或 `DashScopeEmbeddings`。
3.  **检索层**：集成查询重写与 Rerank 排序逻辑，确保 Top-k 片段的高相关性。
4.  **生成层**：集成火山引擎 `Doubao-32K` 大模型，配合专家级 System Prompt。

## 四、 技术栈
- **框架**：LangChain, Python 3.13
- **大模型**：火山引擎 Doubao-pro-32k
- **向量化**：阿里云 DashScope (text-embedding-v3) / 火山引擎 Embedding
- **向量库**：FAISS
- **依赖管理**：`openai`, `dashscope`, `pypdf`, `python-dotenv`

## 五、 关键修复与优化记录
1.  **API 批量限制修复**：针对火山引擎 API 单次请求最大 256 片段的限制，将 `chunk_size` 优化为 250。
2.  **Token 化兼容性修复**：实现了自定义 `ArkEmbeddings` 类，绕过了 LangChain 原生类在本地自动 Token 化导致的 `BadRequestError`。
3.  **多引擎适配**：增加了环境变量 `EMBEDDING_PROVIDER`，支持在不同云服务商之间无缝切换。
4.  **BMS 术语清洗**：针对 PDF 解析中的分页、特殊符号进行了清洗，保障算法公式与术语的完整性。

## 六、 运行指南 (前后端分离架构)
1.  **环境配置**：
    在 `.env` 文件中配置 API Key 与接入点 ID。
2.  **安装依赖**：
    ```bash
    pip install -r requirements.txt
    ```
3.  **启动后端 API 服务**：
    ```bash
    # Windows PowerShell 指定端口示例
    $env:BACKEND_PORT=8001; python backend_api.py
    ```
    *后端服务将运行在 http://localhost:8001*
4.  **启动前端 Web 界面**：
    ```bash
    # 确保前端连接到正确的后端端口
    $env:BACKEND_PORT=8001; python -m streamlit run app.py
    ``` ```
    *前端会自动连接到后端 API 进行问答与管理*

## 七、 架构优势 (Separated Architecture)
- **解耦性**：前端 UI 与 RAG 核心逻辑分离，支持独立部署与扩展。
- **并发支持**：后端基于 FastAPI，可支持多个前端客户端或 API 调用。
- **异步处理**：索引重建等耗时操作在后台异步执行，不阻塞 UI 交互。
- **标准化接口**：提供标准 RESTful API，便于集成到其他业务系统。

## 七、 测试结果示例
**提问**：什么是BMS？
**系统回答**：
- **核心结论**：BMS 是管理电池安全与性能的电子控制系统。
- **详细阐述**：涵盖了定义、硬件构成（传感器、执行器）、工作逻辑（SOC 估计、故障诊断）等细节。
- **引用溯源**：准确标注了引用的论文标题与具体页码。

---
*报告生成日期：2026-04-26*
