import os
import streamlit as st
import time
import requests
import re
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 后端 API 配置
# 使用 127.0.0.1 替代 localhost 以避免 Windows DNS 解析可能的延迟
API_BASE_URL = os.getenv("API_BASE_URL", f"http://127.0.0.1:{os.getenv('BACKEND_PORT', '8001')}/api/v1")

# 页面配置
st.set_page_config(
    page_title="BMS 领域专业 RAG 智能问答系统",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式 (保留原有设计)
st.markdown("""
<style>
    .main { background-color: #F5F7FA; }
    .header-container {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 20px; background-color: white; border-bottom: 1px solid #E5E8EB; margin-bottom: 20px;
    }
    .header-title { font-size: 24px; font-weight: bold; color: #165DFF; display: flex; align-items: center; }
    .status-tag { padding: 2px 10px; border-radius: 12px; font-size: 12px; margin-left: 10px; }
    .status-online { background-color: #E8FFEA; color: #00B42A; }
    .status-offline { background-color: #FFE8E8; color: #F53F3F; }
    .stChatMessage { background-color: white !important; border-radius: 8px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important; margin-bottom: 15px !important; }
    .citation-tag { color: #0FC6C2; font-weight: 500; cursor: pointer; background-color: rgba(15, 198, 194, 0.1); padding: 0 4px; border-radius: 3px; font-size: 0.9em; }
    .term-highlight { color: #165DFF; font-weight: 500; background-color: rgba(22, 93, 255, 0.08); padding: 0 2px; border-radius: 3px; }
    .reference-card { background-color: white; border: 1px solid #E5E8EB; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
    .reference-title { font-weight: bold; font-size: 14px; color: #333; }
    .reference-meta { font-size: 12px; color: #86909C; margin-top: 4px; }
    .reference-content { font-size: 13px; background-color: #F7F8FA; padding: 8px; border-radius: 4px; margin-top: 8px; color: #4E5969; }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 辅助函数 ---
def highlight_terms(text):
    terms = ['SOC', 'SOH', 'BMS', '电池均衡', '故障诊断', '电池热管理', '卡尔曼滤波', '神经网络', '锂离子电池', '动力电池']
    # 按照长度降序排序，确保优先匹配长词
    terms.sort(key=len, reverse=True)
    
    # 构造正则表达式：匹配 HTML 标签或目标术语
    # 分组 1: HTML 标签 (保持不变)
    # 分组 2: 目标术语 (进行包装)
    pattern = re.compile(r'(<[^>]+>)|(' + '|'.join(map(re.escape, terms)) + r')')
    
    def replace(match):
        if match.group(1):
            return match.group(1)  # 返回原始标签
        else:
            term = match.group(2)
            return f'<span class="term-highlight">{term}</span>'
            
    return pattern.sub(replace, text)

def process_citations(text):
    return re.sub(r'\[(\d+),\s*(\d+)\]', r'<span class="citation-tag">[\1, \2]</span>', text)

# --- API 调用 ---
def get_api_status():
    try:
        resp = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        return None
    return None

def query_backend(query, top_k, provider):
    payload = {"query": query, "top_k": top_k, "embedding_provider": provider}
    try:
        # 增加超时时间到 120s，以应对复杂问题的 LLM 生成耗时
        resp = requests.post(f"{API_BASE_URL}/query", json=payload, timeout=120)
        if resp.status_code == 200:
            return resp.json()
        else:
            st.error(f"后端错误: {resp.json().get('detail', '未知错误')}")
    except Exception as e:
        st.error(f"无法连接后端: {e}")
    return None

def rewrite_query_api(query):
    try:
        resp = requests.post(f"{API_BASE_URL}/rewrite", json={"query": query}, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("rewritten_query")
    except:
        pass
    return query

def trigger_rebuild():
    try:
        resp = requests.post(f"{API_BASE_URL}/index/rebuild")
        return resp.status_code == 200
    except:
        return False

# --- UI 逻辑 ---
status_data = get_api_status()
is_online = status_data is not None

# 会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_citations" not in st.session_state:
    st.session_state.current_citations = []

# 顶部导航
st.markdown(f"""
<div class="header-container">
    <div class="header-title">
        🔋 BMS 领域专业 RAG 智能问答系统
        <span class="status-tag {'status-online' if is_online else 'status-offline'}">
            后端状态: {'在线' if is_online else '离线'}
        </span>
        <span class="status-tag status-online">模型: Doubao-32K</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 左右侧边栏布局
left_col, main_col, right_col = st.columns([1, 2.5, 1.2])

# --- 左侧配置 ---
with left_col:
    st.subheader("⚙️ 系统配置")
    
    with st.expander("🛠️ 向量引擎切换", expanded=True):
        provider_map = {
            "火山引擎 Ark Embedding": "volcengine",
            "阿里云 DashScope Embedding": "alibabacloud"
        }
        selected_label = st.radio(
            "选择嵌入模型",
            list(provider_map.keys()),
            index=0 if os.getenv("EMBEDDING_PROVIDER") != "alibabacloud" else 1
        )
        selected_provider = provider_map[selected_label]
            
    with st.expander("🔍 检索参数配置", expanded=True):
        top_k = st.slider("Top-K 检索片段", 1, 20, 5)
        rerank_enabled = st.toggle("Rerank 重排序", value=True)
        
    with st.expander("📚 文献资源管理", expanded=True):
        if is_online:
            st.write(f"已载入论文: {status_data['papers_count']} 篇")
            for paper in status_data['papers_list']:
                st.caption(f"• {paper[:30]}...")
            
            if status_data.get('is_indexing'):
                st.warning("🔄 索引正在后台重建中...")
                if st.button("刷新状态"): st.rerun()
            else:
                if st.button("🔄 重建向量索引", use_container_width=True):
                    if trigger_rebuild():
                        st.success("重建任务已启动")
                        st.rerun()
        else:
            st.error("后端离线，无法获取文献信息")

    st.success("🔒 内容全部来源于本地 BMS 论文库")

# --- 中间问答区 ---
with main_col:
    chat_placeholder = st.container(height=600)
    
    with chat_placeholder:
        if not st.session_state.messages:
            st.chat_message("assistant").markdown("""
            👋 欢迎使用 BMS 领域专业 RAG 问答系统！
            所有回答都严格基于后端载入的 BMS 专业论文。
            """)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(highlight_terms(process_citations(message["content"])), unsafe_allow_html=True)

    # 输入区
    col1, col2 = st.columns([4, 1])
    with col2:
        rewrite_clicked = st.button("✨ 问题重写", use_container_width=True)
    
    if query := st.chat_input("请输入您关于 BMS 领域的问题...", disabled=not is_online):
        if rewrite_clicked:
            with st.spinner("重写中..."):
                query = rewrite_query_api(query)
                st.toast(f"优化为: {query}")
        
        st.session_state.messages.append({"role": "user", "content": query})
        with chat_placeholder:
            with st.chat_message("user"): st.markdown(query)

        with chat_placeholder:
            with st.chat_message("assistant"):
                msg_box = st.empty()
                with st.spinner("生成回答中..."):
                    result = query_backend(query, top_k, selected_provider)
                    if result:
                        answer = result['answer']
                        st.session_state.current_citations = result['citations']
                        # 模拟流式渲染
                        full_txt = ""
                        for chunk in re.split(r'(\s+)', answer):
                            full_txt += chunk
                            time.sleep(0.01)
                            msg_box.markdown(full_txt + "▌")
                        msg_box.markdown(full_txt)
                        st.session_state.messages.append({"role": "assistant", "content": full_txt})
                        st.rerun()

# --- 右侧溯源面板 ---
with right_col:
    st.subheader("📑 文献溯源")
    if st.session_state.current_citations:
        for i, cit in enumerate(st.session_state.current_citations, 1):
            meta = cit['metadata']
            st.markdown(f"""
            <div class="reference-card">
                <div class="reference-title">[{meta.get('paper_id', i)}] {meta.get('paper_title', 'Unknown')}</div>
                <div class="reference-meta">页码: {meta.get('page_number', 'N/A')}</div>
                <div class="reference-content">{cit['content'][:200]}...</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("提问后将在此展示引用文献来源")
        
    st.divider()
    st.subheader("📂 全局文献库")
    if is_online:
        for i, paper in enumerate(status_data['papers_list'], 1):
            st.markdown(f"<div style='font-size: 12px;'>{i}. {paper}</div>", unsafe_allow_html=True)

# 底部
st.markdown("<div style='text-align: center; color: #86909C; font-size: 12px; margin-top: 50px;'>基于 FastAPI + Streamlit | BMS RAG V1.1</div>", unsafe_allow_html=True)
