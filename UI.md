# BMS领域专业RAG问答系统 UI设计方案
结合项目**学术专业性、BMS行业属性、RAG溯源引用核心需求**，设计一套简洁专业、轻量化Web端界面，适配PC端开发/办公使用，风格偏工业科技风+学术极简风，完整贴合项目功能。

## 一、整体设计定位
1. **风格基调**：低饱和工业蓝+浅灰极简风，契合新能源、电池管理（BMS）工业属性，兼顾学术严谨感；
2. **适配终端**：优先PC端（开发、科研人员使用场景），自适应平板；
3. **核心设计重点**：问答区为主、文献溯源面板独立展示、引擎切换可视化、操作极简；
4. **色彩规范**
   - 主色：`#165DFF`（科技蓝，按钮、选中态、重点标识）
   - 辅助色：`#0FC6C2`（引用标签、溯源高亮）
   - 中性色：`#F5F7FA`（背景）、`#333333`（正文）、`#86909C`（辅助文字）
   - 警示色：`#F53F3F`（异常提示）

## 二、页面整体布局（三栏经典布局）
```
顶部导航栏（全局配置+系统信息）
——————————————————————————————
左侧：系统配置侧边栏 ｜ 中间：核心问答区 ｜ 右侧：文献溯源引用面板
——————————————————————————————
底部：版权&项目信息栏
```

### 1. 顶部导航栏（Header）
- 左侧：**项目标题**「BMS 领域专业RAG智能问答系统」+ 电池简约图标
- 中间：系统状态提示
  - 向量库状态：`索引已加载 / 未加载`
  - 模型状态：`Doubao-32K 运行中`
- 右侧：全局功能按钮
  1. 清空对话
  2. 重建向量索引（对应命令行 `--rebuild`）
  3. 暗色/亮色模式切换

### 2. 左侧配置侧边栏（Aside-左）
固定宽度，折叠/展开切换，承载项目核心配置能力，对应后端多引擎、参数配置：
#### 模块1：嵌入模型引擎配置
- 标题：向量引擎切换
- 单选选择框：
  - ✅ 火山引擎 Ark Embedding
  - ☐ 阿里云 DashScope Embedding
- 同步联动环境变量 `EMBEDDING_PROVIDER`

#### 模块2：检索参数配置
- Top-K 检索片段：数值输入框（默认5）
- Rerank 重排序：开关（默认开启）
- 文本分片大小：展示固定250（标注：已适配API限制）

#### 模块3：文献资源管理
- 已载入论文库：展示8篇BMS论文列表（缩略标题）
- 本地FAISS索引：`已持久化存储` 状态标识
- 增量更新按钮：支持新增PDF论文导入

#### 模块4：系统说明
- 简短提示：**严格基于论文内容，零幻觉输出**

### 3. 中间核心问答区（Main-主区域）
页面核心交互区，仿ChatGPT对话流式布局，适配大篇幅学术回答：
#### 上方：对话展示区
- 气泡式对话设计
  - 用户提问：浅灰色右对齐气泡
  - AI回答：白色卡片式左对齐，**流式逐字输出**
- 回答内容结构化排版（完美匹配项目输出格式）：
  1. 核心结论（加粗高亮）
  2. 详细阐述（常规正文）
  3. 关键公式/专业术语：等宽字体高亮
- 特殊标识：所有技术观点自动附带 `[论文编号, 页码]` 角标引用

#### 下方：提问输入区
- 大尺寸多行输入框：支持换行、长文本输入，适配学术长问句
- 功能按钮：
  - ✨ 问题重写：一键将口语化提问转为BMS学术检索式
  - 发送提问（主按钮，主色高亮）
  - 清空输入

### 4. 右侧溯源引用面板（Aside-右）
项目**差异化核心UI**，解决论文溯源需求，默认展开：
#### 模块1：本次问答引用来源
- 标题：当前回答·文献溯源
- 卡片列表展示：
  - 引用论文编号、论文名称、引用页码
  - 来源片段预览：截取论文原文关键内容
  - 复制引用、查看原文按钮

#### 模块2：全局文献库目录
- 全部8篇BMS论文索引目录
- 点击快速查看论文基础信息
- 区分已引用/未引用文献灰色置灰

### 5. 底部栏（Footer）
- 文字信息：基于LangChain+FAISS ｜ BMS专业领域定制RAG系统
- 版本标注：V1.0 | 报告生成：2026-04-26

## 三、核心特色交互设计
1. **零幻觉标识**
AI回答顶部固定标签：`🔒 内容全部来源于本地BMS论文库，无外部知识拓展`，强化项目核心卖点。

2. **引用联动交互**
点击回答内的 `[论文编号, 页码]` 引用角标，右侧溯源面板自动定位并高亮对应原文片段。

3. **索引加载状态动画**
点击「重建向量索引」后，展示加载动画+文字提示：PDF解析→文本清洗→向量化→FAISS存储 流程提示。

4. **BMS术语特殊渲染**
对SOC、SOH、电池均衡、故障诊断、电池热管理等专业术语自动标蓝高亮，提升阅读性。

5. **响应式适配**
- 电脑端：三栏完整展示
- 小屏设备：左侧配置栏、右侧溯源栏可折叠，保留全屏问答区

## 四、配色&组件规范（可直接落地开发）
### 1. 按钮组件
- 主按钮（发送、重建索引）：主色填充，圆角6px
- 次按钮（重写问题、复制）：白色边框+文字主色
- 开关组件：引擎、重排序功能统一风格切换按钮

### 2. 卡片样式
- 圆角：8px
- 阴影：轻微悬浮阴影，简约高级
- 分割线：浅灰细分割线，区分不同模块

### 3. 字体规范
- 中文：微软雅黑 / 苹方
- 英文/代码/公式：Consolas 等宽字体
- 标题：16px 加粗
- 正文：14px
- 引用标注：12px 辅助色

## 五、技术落地选型（适配后端Python项目）
结合你的Python+LangChain后端，推荐低成本快速开发方案：
1. **前端框架**：Streamlit（最优解）
   - 优势：Python直接编写UI，无需前后端分离、快速对接RAG后端代码、开发效率极高，适合项目demo/毕设/科研项目
2. **备选方案**：
   - Flask + Vue3：适合后期迭代完整版系统
   - Gradio：极简快速搭建，适合快速演示

---

我可以直接给你生成 **可直接运行的 Streamlit 完整前端代码**，无缝对接你现有RAG_main.py、FAISS向量库、双嵌入引擎，需要我直接写代码吗？

代码如下：<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>BMS领域专业RAG问答系统</title>
    <script src="https://res.gemcoder.com/js/reload.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css"
      rel="stylesheet"
    />
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              primary: '#165DFF',
              secondary: '#0FC6C2',
              neutral: '#F5F7FA',
              'text-main': '#333333',
              'text-secondary': '#86909C',
              danger: '#F53F3F'
            },
            fontFamily: {
              sans: ['Microsoft YaHei', 'PingFang SC', 'sans-serif'],
              mono: ['Consolas', 'monospace']
            }
          }
        }
      };
    </script>
    <style type="text/tailwindcss">
      @layer utilities {
          .content-auto {
              content-visibility: auto;
          }
          .bubble-user {
              background-color: #f0f2f5;
              border-radius: 12px 12px 4px 12px;
          }
          .bubble-ai {
              background-color: #ffffff;
              border-radius: 12px 12px 12px 4px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          }
          .citation-tag {
              font-size: 12px;
              color: #0FC6C2;
              cursor: pointer;
              transition: all 0.2s;
          }
          .citation-tag:hover {
              text-decoration: underline;
              background-color: rgba(15, 198, 194, 0.1);
          }
          .term-highlight {
              color: #165DFF;
              font-weight: 500;
              background-color: rgba(22, 93, 255, 0.08);
              padding: 0 2px;
              border-radius: 3px;
          }
          .reference-card {
              transition: all 0.3s;
          }
          .reference-card.highlight {
              background-color: rgba(15, 198, 194, 0.1);
              border-color: #0FC6C2;
              transform: scale(1.02);
          }
      }
    </style>
  </head>
  <body class="bg-neutral font-sans text-text-main min-h-screen flex flex-col">
    <!-- [MODULE] 123_顶部导航栏 -->
    <header class="bg-white shadow-sm py-3 px-4">
      <div
        class="container mx-auto flex flex-wrap items-center justify-between"
      >
        <!-- [MODULE] 45a_导航栏左侧项目标题 -->
        <div class="flex items-center space-x-3">
          <i class="fas fa-battery-full text-primary text-2xl"> </i>
          <h1 class="text-xl font-bold hidden md:block">
            BMS 领域专业RAG智能问答系统
          </h1>
          <h1 class="text-xl font-bold md:hidden">BMS RAG问答</h1>
        </div>
        <!-- [/MODULE] 45a_导航栏左侧项目标题 -- 项目名称与图标展示 -->
        <!-- [MODULE] 7b2_导航栏中间系统状态 -->
        <div class="flex items-center space-x-6 my-2 md:my-0">
          <div class="flex items-center space-x-2">
            <span class="text-text-secondary text-sm"> 向量库: </span>
            <span
              class="text-sm px-2 py-1 bg-green-100 text-green-700 rounded-full"
            >
              索引已加载
            </span>
          </div>
          <div class="flex items-center space-x-2">
            <span class="text-text-secondary text-sm"> 模型: </span>
            <span
              class="text-sm px-2 py-1 bg-blue-100 text-blue-700 rounded-full"
            >
              Doubao-32K 运行中
            </span>
          </div>
        </div>
        <!-- [/MODULE] 7b2_导航栏中间系统状态 -- 显示向量库和模型运行状态 -->
        <!-- [MODULE] 8c3_导航栏右侧功能按钮 -->
        <div class="flex items-center space-x-3">
          <button
            id="clear-chat"
            class="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            <i class="fas fa-trash-alt mr-1"> </i>
            清空对话
          </button>
          <button
            id="rebuild-index"
            class="px-3 py-1.5 text-sm border border-primary text-primary bg-white rounded-md hover:bg-primary/5 transition-colors"
          >
            <i class="fas fa-sync-alt mr-1"> </i>
            重建索引
          </button>
          <button
            id="theme-toggle"
            class="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            <i class="fas fa-moon mr-1"> </i>
          </button>
        </div>
        <!-- [/MODULE] 8c3_导航栏右侧功能按钮 -- 清空对话、重建索引、主题切换功能按钮 -->
      </div>
    </header>
    <!-- [/MODULE] 123_顶部导航栏 -- 包含项目标题、系统状态提示和全局功能按钮 -->
    <!-- [MODULE] d45_主内容区域 -->
    <div class="flex flex-1 overflow-hidden">
      <!-- [MODULE] 2e6_左侧系统配置侧边栏 -->
      <aside
        id="left-sidebar"
        class="w-64 bg-white shadow-sm flex-shrink-0 overflow-y-auto transition-all duration-300"
      >
        <div class="p-4 space-y-6">
          <!-- [MODULE] f37_嵌入模型引擎配置 -->
          <div class="border-b pb-4">
            <h3 class="text-lg font-semibold mb-3 flex items-center">
              <i class="fas fa-microchip text-primary mr-2"> </i>
              向量引擎切换
            </h3>
            <div class="space-y-3">
              <label class="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="embedding"
                  value="ark"
                  checked
                  class="w-4 h-4 text-primary"
                />
                <span class="ml-2 text-sm"> 火山引擎 Ark Embedding </span>
              </label>
              <label class="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="embedding"
                  value="dashscope"
                  class="w-4 h-4 text-primary"
                />
                <span class="ml-2 text-sm"> 阿里云 DashScope Embedding </span>
              </label>
            </div>
          </div>
          <!-- [/MODULE] f37_嵌入模型引擎配置 -- 选择不同的向量嵌入引擎 -->
          <!-- [MODULE] 5g8_检索参数配置 -->
          <div class="border-b pb-4">
            <h3 class="text-lg font-semibold mb-3 flex items-center">
              <i class="fas fa-sliders-h text-primary mr-2"> </i>
              检索参数配置
            </h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm mb-1"> Top-K 检索片段 </label>
                <input
                  type="number"
                  value="5"
                  min="1"
                  max="20"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                />
              </div>
              <div class="flex items-center justify-between">
                <label class="text-sm"> Rerank 重排序 </label>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" checked class="sr-only peer" />
                  <div
                    class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[&quot;&quot;] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"
                  ></div>
                </label>
              </div>
              <div>
                <label class="block text-sm mb-1"> 文本分片大小 </label>
                <div
                  class="flex items-center px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                >
                  <span class="text-sm text-text-secondary">
                    250
                    <span class="text-xs ml-2 text-text-secondary">
                      (已适配API限制)
                    </span>
                  </span>
                </div>
              </div>
            </div>
          </div>
          <!-- [/MODULE] 5g8_检索参数配置 -- 配置检索Top-K和重排序开关等参数 -->
          <!-- [MODULE] 9h1_文献资源管理 -->
          <div class="border-b pb-4">
            <h3 class="text-lg font-semibold mb-3 flex items-center">
              <i class="fas fa-book text-primary mr-2"> </i>
              文献资源管理
            </h3>
            <div class="space-y-3">
              <div>
                <p class="text-sm mb-2">已载入论文库</p>
                <div class="max-h-32 overflow-y-auto space-y-2 pr-1">
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    1. 锂离子电池SOC估计方法综述
                  </div>
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    2. 基于机器学习的电池SOH预测研究
                  </div>
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    3. 电池管理系统热安全策略分析
                  </div>
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    4. 电动汽车BMS故障诊断技术进展
                  </div>
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    5. 锂离子电池均衡控制方法研究
                  </div>
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    6. 基于深度学习的电池健康状态估计
                  </div>
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    7. 动力电池系统热管理技术研究
                  </div>
                  <div class="text-sm p-2 bg-gray-50 rounded">
                    8. 电池模型参数辨识方法对比研究
                  </div>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm"> 本地FAISS索引 </span>
                <span
                  class="text-sm px-2 py-1 bg-green-100 text-green-700 rounded-full"
                >
                  已持久化存储
                </span>
              </div>
              <button
                class="w-full py-2 text-sm border border-dashed border-gray-300 rounded-md hover:border-primary hover:text-primary transition-colors"
              >
                <i class="fas fa-plus mr-1"> </i>
                增量更新论文库
              </button>
            </div>
          </div>
          <!-- [/MODULE] 9h1_文献资源管理 -- 展示已载入论文，支持增量更新 -->
          <!-- [MODULE] k29_系统说明 -->
          <div>
            <div class="bg-primary/5 p-3 rounded-md">
              <p class="text-sm text-primary font-medium">
                <i class="fas fa-info-circle mr-1"> </i>
                严格基于论文内容，零幻觉输出
              </p>
            </div>
          </div>
          <!-- [/MODULE] k29_系统说明 -- 展示系统核心特性提示 -->
        </div>
        <button
          id="toggle-left"
          class="hidden md:block absolute left-[15.5rem] top-20 bg-white shadow-md rounded-full w-6 h-6 flex items-center justify-center z-10"
        >
          <i
            class="fas fa-chevron-left text-text-secondary text-xs toggle-left-icon"
          >
          </i>
        </button>
      </aside>
      <!-- [/MODULE] 2e6_左侧系统配置侧边栏 -- 系统配置和文献管理功能 -->
      <!-- [MODULE] 3m4_中间核心问答区 -->
      <main class="flex-1 overflow-y-auto p-4 flex flex-col">
        <!-- [MODULE] 6n7_对话展示区 -->
        <div id="chat-container" class="flex-1 mb-4 space-y-6">
          <!-- 欢迎消息 -->
          <div class="bubble-ai p-4 max-w-[85%]">
            <div class="mb-2">
              <span
                class="inline-block px-2 py-1 bg-secondary/10 text-secondary text-xs rounded mb-3"
              >
                🔒 内容全部来源于本地BMS论文库，无外部知识拓展
              </span>
            </div>
            <p class="mb-2">
              👋
              欢迎使用BMS领域专业RAG问答系统！我可以帮您解答关于电池管理系统相关的学术问题，所有回答都基于本地载入的BMS专业论文，并会标注引用来源。
            </p>
            <p class="mb-2">您可以尝试提问例如：</p>
            <ul class="list-disc ml-5 mb-2">
              <li class="mb-1">
                当前
                <span class="term-highlight"> SOC </span>
                估计主要有哪些方法？
              </li>
              <li class="mb-1">
                <span class="term-highlight"> SOH </span>
                预测常用的机器学习算法是什么？
              </li>
              <li>电池热管理的最新研究进展有哪些？</li>
            </ul>
          </div>
        </div>
        <!-- [/MODULE] 6n7_对话展示区 -- 展示所有历史对话消息 -->
        <!-- [MODULE] 8p2_提问输入区 -->
        <div class="bg-white p-4 rounded-lg shadow-sm">
          <textarea
            id="question-input"
            placeholder="请输入您关于BMS领域的问题..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary resize-none"
            rows="3"
          >
          </textarea>
          <div class="flex items-center justify-between mt-3">
            <div class="flex space-x-3">
              <button
                id="rewrite-question"
                class="px-4 py-2 text-sm border border-primary text-primary bg-white rounded-md hover:bg-primary/5 transition-colors"
              >
                <i class="fas fa-magic mr-1"> </i>
                ✨ 问题重写
              </button>
              <button
                id="clear-input"
                class="px-4 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              >
                <i class="fas fa-eraser mr-1"> </i>
                清空输入
              </button>
            </div>
            <button
              id="send-question"
              class="px-6 py-2 text-sm bg-primary text-white rounded-md hover:bg-primary/90 transition-colors"
            >
              <i class="fas fa-paper-plane mr-1"> </i>
              发送提问
            </button>
          </div>
        </div>
        <!-- [/MODULE] 8p2_提问输入区 -- 问题输入与功能按钮 -->
      </main>
      <!-- [/MODULE] 3m4_中间核心问答区 -- 对话展示和用户提问交互核心区域 -->
      <!-- [MODULE] q56_右侧文献溯源引用面板 -->
      <aside
        id="right-sidebar"
        class="w-80 bg-white shadow-sm flex-shrink-0 overflow-y-auto transition-all duration-300 border-l border-gray-200"
      >
        <div class="p-4 space-y-6">
          <!-- [MODULE] s78_本次问答引用来源 -->
          <div>
            <h3 class="text-lg font-semibold mb-3 flex items-center">
              <i class="fas fa-quote-left text-secondary mr-2"> </i>
              当前回答·文献溯源
            </h3>
            <div id="citation-container" class="space-y-4">
              <div class="text-center py-8 text-text-secondary text-sm">
                <i class="fas fa-file-alt text-3xl mb-3 block opacity-40"> </i>
                提问后将在此展示引用文献来源
              </div>
            </div>
          </div>
          <!-- [/MODULE] s78_本次问答引用来源 -- 展示当前回答引用的文献片段 -->
          <!-- [MODULE] t90_全局文献库目录 -->
          <div class="border-t pt-4">
            <h3 class="text-lg font-semibold mb-3 flex items-center">
              <i class="fas fa-book-list text-primary mr-2"> </i>
              全局文献库目录
            </h3>
            <div class="space-y-2 max-h-64 overflow-y-auto">
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors"
              >
                <div class="font-medium">1. 锂离子电池SOC估计方法综述</div>
                <div class="text-xs text-text-secondary mt-1">
                  82页 · 储能科学与技术
                </div>
              </div>
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors"
              >
                <div class="font-medium">2. 基于机器学习的电池SOH预测研究</div>
                <div class="text-xs text-text-secondary mt-1">
                  64页 · 中国电机工程学报
                </div>
              </div>
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors"
              >
                <div class="font-medium">3. 电池管理系统热安全策略分析</div>
                <div class="text-xs text-text-secondary mt-1">
                  48页 · 汽车工程
                </div>
              </div>
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors"
              >
                <div class="font-medium">4. 电动汽车BMS故障诊断技术进展</div>
                <div class="text-xs text-text-secondary mt-1">
                  75页 · 电工技术学报
                </div>
              </div>
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors"
              >
                <div class="font-medium">5. 锂离子电池均衡控制方法研究</div>
                <div class="text-xs text-text-secondary mt-1">
                  56页 · 电源学报
                </div>
              </div>
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors opacity-50"
              >
                <div class="font-medium">6. 基于深度学习的电池健康状态估计</div>
                <div class="text-xs text-text-secondary mt-1">
                  68页 · 控制与决策
                </div>
              </div>
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors opacity-50"
              >
                <div class="font-medium">7. 动力电池系统热管理技术研究</div>
                <div class="text-xs text-text-secondary mt-1">
                  92页 · 汽车工程学报
                </div>
              </div>
              <div
                class="text-sm p-2 border rounded-md cursor-pointer hover:border-primary transition-colors opacity-50"
              >
                <div class="font-medium">8. 电池模型参数辨识方法对比研究</div>
                <div class="text-xs text-text-secondary mt-1">
                  53页 · 电池学报
                </div>
              </div>
            </div>
          </div>
          <!-- [/MODULE] t90_全局文献库目录 -- 展示所有载入的论文，区分已引用未引用 -->
        </div>
        <button
          id="toggle-right"
          class="hidden md:block absolute right-[19.5rem] top-20 bg-white shadow-md rounded-full w-6 h-6 flex items-center justify-center z-10"
        >
          <i
            class="fas fa-chevron-right text-text-secondary text-xs toggle-right-icon"
          >
          </i>
        </button>
      </aside>
      <!-- [/MODULE] q56_右侧文献溯源引用面板 -- 展示文献溯源和全局文献目录 -->
    </div>
    <!-- [/MODULE] d45_主内容区域 -- 包含左右侧边栏和中间核心区 -->
    <!-- [MODULE] w45_底部信息栏 -->
    <footer class="bg-white py-3 border-t border-gray-200">
      <div class="container mx-auto px-4 text-center">
        <p class="text-sm text-text-secondary">
          基于LangChain+FAISS ｜ BMS专业领域定制RAG系统 ｜
          <span class="ml-2"> V1.0 | 报告生成：2026-04-26 </span>
        </p>
      </div>
    </footer>
    <!-- [/MODULE] w45_底部信息栏 -- 版本和项目信息 -->
    <!-- 重建索引进度模态框 -->
    <div
      id="rebuild-modal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 hidden"
    >
      <div class="bg-white rounded-lg p-6 w-[500px] max-w-[90%]">
        <h3 class="text-lg font-semibold mb-4">重建向量索引</h3>
        <div class="space-y-4">
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div
              id="rebuild-progress"
              class="bg-primary h-2.5 rounded-full transition-all duration-500"
              style="width: 10%"
            ></div>
          </div>
          <div id="rebuild-status" class="text-sm text-text-secondary">
            <p class="mb-1">
              <i class="fas fa-spinner fa-spin mr-2 text-primary"> </i>
              正在解析PDF文档...
            </p>
          </div>
          <button
            id="close-rebuild-modal"
            class="mt-4 w-full py-2 bg-primary text-white rounded-md hidden"
          >
            完成
          </button>
        </div>
      </div>
    </div>
    <!-- [/MODULE] -->
  </body>
  <!-- [JSMOD] j1_侧边栏折叠展开功能 -->
  <script id="sidebar-toggle">
    document.addEventListener('DOMContentLoaded', function () {
      var leftSidebar = document.getElementById('left-sidebar');
      var rightSidebar = document.getElementById('right-sidebar');
      var toggleLeftBtn = document.getElementById('toggle-left');
      var toggleRightBtn = document.getElementById('toggle-right');
      var leftIcon = document.querySelector('.toggle-left-icon');
      var rightIcon = document.querySelector('.toggle-right-icon');
      var leftCollapsed = false;
      var rightCollapsed = false;
      toggleLeftBtn.addEventListener('click', function () {
        if (!leftCollapsed) {
          leftSidebar.classList.add('w-0');
          leftSidebar.classList.remove('w-64');
          leftIcon.classList.remove('fa-chevron-left');
          leftIcon.classList.add('fa-chevron-right');
          toggleLeftBtn.style.left = '0';
        } else {
          leftSidebar.classList.remove('w-0');
          leftSidebar.classList.add('w-64');
          leftIcon.classList.add('fa-chevron-left');
          leftIcon.classList.remove('fa-chevron-right');
          toggleLeftBtn.style.left = '15.5rem';
        }
        leftCollapsed = !leftCollapsed;
        setTimeout(function () {
          return window.dispatchEvent(new Event('resize'));
        }, 300);
      });
      toggleRightBtn.addEventListener('click', function () {
        if (!rightCollapsed) {
          rightSidebar.classList.add('w-0');
          rightSidebar.classList.remove('w-80');
          rightIcon.classList.remove('fa-chevron-right');
          rightIcon.classList.add('fa-chevron-left');
          toggleRightBtn.style.right = '0';
        } else {
          rightSidebar.classList.remove('w-0');
          rightSidebar.classList.add('w-80');
          rightIcon.classList.add('fa-chevron-right');
          rightIcon.classList.remove('fa-chevron-left');
          toggleRightBtn.style.right = '19.5rem';
        }
        rightCollapsed = !rightCollapsed;
        setTimeout(function () {
          return window.dispatchEvent(new Event('resize'));
        }, 300);
      });
    });
  </script>
  <!-- [/JSMOD] j1_侧边栏折叠展开功能 -- 实现左右侧边栏折叠和展开交互 -->
  <!-- [JSMOD] j2_核心问答功能 -->
  <script id="chat-function">
    document.addEventListener('DOMContentLoaded', function () {
      var chatContainer = document.getElementById('chat-container');
      var questionInput = document.getElementById('question-input');
      var sendBtn = document.getElementById('send-question');
      var clearInputBtn = document.getElementById('clear-input');
      var clearChatBtn = document.getElementById('clear-chat');
      var rewriteBtn = document.getElementById('rewrite-question');
      var citationContainer = document.getElementById('citation-container');

      // 示例引用数据
      var sampleCitations = [{
        id: 1,
        paperId: 1,
        title: "锂离子电池SOC估计方法综述",
        page: 14,
        content: "目前锂离子电池SOC估计方法主要分为四类：安时积分法、开路电压法、基于模型的方法和数据驱动方法。其中，基于模型的方法包括卡尔曼滤波系列方法，而数据驱动方法则包含神经网络、支持向量机等机器学习算法<span class='citation-tag' data-paper-id='1' data-page='14'>[1, 14]</span>。"
      }, {
        id: 2,
        paperId: 6,
        title: "基于深度学习的电池健康状态估计",
        page: 37,
        content: "近年来深度学习方法在<span class='term-highlight'>SOH</span>预测领域得到了广泛应用，卷积神经网络(CNN)能够自动提取电池特征，循环神经网络(RNN)擅长处理时序数据，长短期记忆网络(LSTM)进一步解决了梯度消失问题，在实际应用中取得了较高预测精度<span class='citation-tag' data-paper-id='6' data-page='37'>[6, 37]</span>。"
      }];

      // BMS专业术语列表
      var bmsTerms = ['SOC', 'SOH', 'BMS', '电池均衡', '故障诊断', '电池热管理', '卡尔曼滤波', '神经网络', '锂离子电池', '动力电池', 'FAISS', '向量化', 'RAG', '重排序'];

      // 高亮BMS术语
      function highlightBmsTerms(text) {
        var result = text;
        bmsTerms.forEach(function (term) {
          var regex = new RegExp("(".concat(term, ")"), 'g');
          result = result.replace(regex, "<span class=\"term-highlight\">$1</span>");
        });
        return result;
      }

      // 添加用户消息
      function addUserMessage(content) {
        var div = document.createElement('div');
        div.className = 'flex justify-end';
        div.innerHTML = "<div class=\"bubble-user p-4 max-w-[85%]\">\n                <p>".concat(highlightBmsTerms(escapeHtml(content)), "</p>\n            </div>");
        chatContainer.appendChild(div);
        scrollToBottom();
      }

      // 开始添加AI消息
      function startAiMessage() {
        var div = document.createElement('div');
        div.className = 'flex justify-start';
        div.innerHTML = "<div class=\"bubble-ai p-4 max-w-[85%]\" id=\"current-ai-message\">\n                <div class=\"mb-2\">\n                    <span class=\"inline-block px-2 py-1 bg-secondary/10 text-secondary text-xs rounded mb-3\">\n                        \uD83D\uDD12 \u5185\u5BB9\u5168\u90E8\u6765\u6E90\u4E8E\u672C\u5730BMS\u8BBA\u6587\u5E93\uFF0C\u65E0\u5916\u90E8\u77E5\u8BC6\u62D3\u5C55\n                    </span>\n                </div>\n                <div id=\"ai-response-content\"></div>\n            </div>";
        chatContainer.appendChild(div);
        return document.getElementById('ai-response-content');
      }

      // 流式输出文本
      function typeText(element, text) {
        var index = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 0;
        if (index < text.length) {
          var currentText = element.innerHTML + text.charAt(index);
          element.innerHTML = highlightBmsTerms(processCitations(currentText));
          setTimeout(function () {
            return typeText(element, text, index + 1);
          }, 30);
        } else {
          // 完成后加载引用
          loadCitations(sampleCitations);
        }
        scrollToBottom();
      }

      // 处理引用标签
      function processCitations(text) {
        return text.replace(/\[(\d+),\s*(\d+)\]/g, '<span class="citation-tag" data-paper-id="$1" data-page="$2">[$1, $2]</span>');
      }

      // HTML转义
      function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
      }

      // 滚动到底部
      function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
        window.scrollTo(0, document.body.scrollHeight);
      }

      // 加载引用面板
      function loadCitations(citations) {
        citationContainer.innerHTML = '';
        if (citations.length === 0) {
          citationContainer.innerHTML = "<div class=\"text-center py-8 text-text-secondary text-sm\">\n                    <i class=\"fas fa-file-alt text-3xl mb-3 block opacity-40\"></i>\n                    \u6682\u65E0\u5F15\u7528\u6587\u732E\n                </div>";
          return;
        }
        citations.forEach(function (citation) {
          var card = document.createElement('div');
          card.className = 'reference-card border rounded-md p-3';
          card.dataset.paperId = citation.paperId;
          card.dataset.page = citation.page;
          card.innerHTML = "<div class=\"flex justify-between items-start mb-2\">\n                    <div>\n                        <span class=\"text-xs bg-secondary text-white px-2 py-0.5 rounded\">".concat(citation.paperId, "</span>\n                        <span class=\"text-sm font-medium ml-1\">").concat(citation.title, "</span>\n                    </div>\n                    <span class=\"text-xs text-text-secondary\">\u9875\u7801:").concat(citation.page, "</span>\n                </div>\n                <p class=\"text-sm bg-gray-50 p-2 rounded my-2\">").concat(citation.content, "</p>\n                <div class=\"flex items-center justify-end space-x-2 mt-2\">\n                    <button class=\"copy-citation px-2 py-1 text-xs border border-secondary text-secondary rounded hover:bg-secondary/5 transition-colors\">\n                        <i class=\"fas fa-copy mr-1\"></i>\u590D\u5236\u5F15\u7528\n                    </button>\n                    <button class=\"view-full px-2 py-1 text-xs border border-primary text-primary rounded hover:bg-primary/5 transition-colors\">\n                        <i class=\"fas fa-eye mr-1\"></i>\u67E5\u770B\u539F\u6587\n                    </button>\n                </div>");
          citationContainer.appendChild(card);
        });

        // 添加点击事件
        document.querySelectorAll('.copy-citation').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var _this = this;
            var card = this.closest('.reference-card');
            var paperId = card.dataset.paperId;
            var page = card.dataset.page;
            var text = "[".concat(paperId, ",").concat(page, "]").concat(sampleCitations.find(function (c) {
              return c.paperId == paperId;
            }).title);
            navigator.clipboard.writeText(text).then(function () {
              _this.innerHTML = '<i class="fas fa-check mr-1"></i>已复制';
              setTimeout(function () {
                _this.innerHTML = '<i class="fas fa-copy mr-1"></i>复制引用';
              }, 1500);
            });
          });
        });
      }

      // 点击引用角标高亮对应面板
      document.addEventListener('click', function (e) {
        if (e.target.classList.contains('citation-tag')) {
          var paperId = e.target.dataset.paperId;
          var page = e.target.dataset.page;

          // 移除之前的高亮
          document.querySelectorAll('.reference-card.highlight').forEach(function (card) {
            card.classList.remove('highlight');
          });

          // 添加当前高亮
          var targetCard = document.querySelector(".reference-card[data-paper-id=\"".concat(paperId, "\"][data-page=\"").concat(page, "\"]"));
          if (targetCard) {
            targetCard.classList.add('highlight');
            targetCard.scrollIntoView({
              behavior: 'smooth',
              block: 'center'
            });
          }
        }
      });

      // 发送问题
      sendBtn.addEventListener('click', function () {
        var question = questionInput.value.trim();
        if (!question) return;
        addUserMessage(question);
        questionInput.value = '';

        // 模拟AI回复
        var aiResponse = "**\u6838\u5FC3\u7ED3\u8BBA**\uFF1A\u5F53\u524D\u9488\u5BF9<span class=\"term-highlight\">SOC</span>\u4F30\u8BA1\u7684\u7814\u7A76\u5DF2\u7ECF\u5F62\u6210\u4E86\u8F83\u4E3A\u5B8C\u6574\u7684\u65B9\u6CD5\u4F53\u7CFB\uFF0C\u878D\u5408\u591A\u79CD\u65B9\u6CD5\u7684\u590D\u5408\u4F30\u8BA1\u65B9\u6848\u662F\u5F53\u524D\u7814\u7A76\u70ED\u70B9<span class=\"citation-tag\" data-paper-id=\"1\" data-page=\"14\">[1, 14]</span>\u3002\n**\u8BE6\u7EC6\u9610\u8FF0**\uFF1A\n\u73B0\u6709\u7814\u7A76\u4E2D\uFF0C<span class=\"term-highlight\">SOC</span>\uFF08State of Charge\uFF09\u4F30\u8BA1\u8868\u793A\u7535\u6C60\u5269\u4F59\u7535\u91CF\u7684\u4F30\u8BA1\uFF0C\u662F\u7535\u6C60\u7BA1\u7406\u7CFB\u7EDF(BMS)\u7684\u6838\u5FC3\u529F\u80FD\u4E4B\u4E00\u3002\u76EE\u524D\u4E3B\u6D41\u65B9\u6CD5\u5206\u4E3A\u56DB\u7C7B\uFF1A\n1. \u5B89\u65F6\u79EF\u5206\u6CD5\uFF1A\u5B9E\u73B0\u7B80\u5355\uFF0C\u4F46\u5B58\u5728\u7D2F\u8BA1\u8BEF\u5DEE\uFF0C\u9700\u8981\u5B9A\u671F\u6821\u51C6\n2. \u5F00\u8DEF\u7535\u538B\u6CD5\uFF1A\u7CBE\u5EA6\u8F83\u9AD8\uFF0C\u4F46\u9700\u8981\u957F\u65F6\u95F4\u9759\u7F6E\uFF0C\u65E0\u6CD5\u5728\u7EBF\u5E94\u7528\n3. \u57FA\u4E8E\u6A21\u578B\u7684\u65B9\u6CD5\uFF1A\u5982\u6269\u5C55\u5361\u5C14\u66FC\u6EE4\u6CE2(EKF)\u3001\u65E0\u5473\u5361\u5C14\u66FC\u6EE4\u6CE2(UKF)\uFF0C\u7CBE\u5EA6\u8F83\u9AD8\uFF0C\u80FD\u5B9E\u73B0\u5728\u7EBF\u4F30\u8BA1\uFF0C\u662F\u5F53\u524D\u5DE5\u4E1A\u754C\u5E94\u7528\u4E3B\u6D41\n4. \u6570\u636E\u9A71\u52A8\u65B9\u6CD5\uFF1A\u57FA\u4E8E\u673A\u5668\u5B66\u4E60\u3001\u6DF1\u5EA6\u5B66\u4E60\uFF0C\u4E0D\u4F9D\u8D56\u7CBE\u786E\u7535\u6C60\u6A21\u578B\uFF0C\u5728\u590D\u6742\u5DE5\u51B5\u4E0B\u8868\u73B0\u4F18\u5F02\uFF0C\u662F\u5F53\u524D\u5B66\u672F\u7814\u7A76\u70ED\u70B9<span class=\"citation-tag\" data-paper-id=\"1\" data-page=\"22\">[1, 22]</span>\n**\u5173\u952E\u516C\u5F0F**\uFF1A\n```\nSOC(k) = SOC(k-1) + (I(k) * \u0394t) / Cn\n```\n\u5176\u4E2D\uFF0CI(k)\u662Fk\u65F6\u523B\u7535\u6D41\uFF0C\u0394t\u662F\u65F6\u95F4\u6B65\u957F\uFF0CCn\u662F\u989D\u5B9A\u5BB9\u91CF\u3002\n\u7814\u7A76\u8868\u660E\uFF0C\u878D\u5408\u591A\u79CD\u65B9\u6CD5\u7684\u590D\u5408\u65B9\u6848\u80FD\u591F\u517C\u987E\u7CBE\u5EA6\u548C\u9C81\u68D2\u6027\uFF0C\u662F\u672A\u6765\u53D1\u5C55\u8D8B\u52BF\u3002\u57FA\u4E8E\u6DF1\u5EA6\u5B66\u4E60\u7684\u65B9\u6CD5\u968F\u7740\u6570\u636E\u91CF\u7684\u589E\u52A0\u6027\u80FD\u4E0D\u65AD\u63D0\u5347\uFF0C\u6709\u671B\u5728\u5B9E\u9645\u5E94\u7528\u4E2D\u83B7\u5F97\u66F4\u5E7F\u6CDB\u5E94\u7528<span class=\"citation-tag\" data-paper-id=\"1\" data-page=\"31\">[1, 31]</span>\u3002";
        var responseElement = startAiMessage();
        typeText(responseElement, aiResponse);
      });

      // 回车发送
      questionInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && e.shiftKey === false) {
          e.preventDefault();
          sendBtn.click();
        }
      });

      // 清空输入
      clearInputBtn.addEventListener('click', function () {
        questionInput.value = '';
      });

      // 清空对话
      clearChatBtn.addEventListener('click', function () {
        chatContainer.innerHTML = "<div class=\"bubble-ai p-4 max-w-[85%]\">\n                <div class=\"mb-2\">\n                    <span class=\"inline-block px-2 py-1 bg-secondary/10 text-secondary text-xs rounded mb-3\">\n                        \uD83D\uDD12 \u5185\u5BB9\u5168\u90E8\u6765\u6E90\u4E8E\u672C\u5730BMS\u8BBA\u6587\u5E93\uFF0C\u65E0\u5916\u90E8\u77E5\u8BC6\u62D3\u5C55\n                    </span>\n                </div>\n                <p class=\"mb-2\">\uD83D\uDC4B \u6B22\u8FCE\u4F7F\u7528BMS\u9886\u57DF\u4E13\u4E1ARAG\u95EE\u7B54\u7CFB\u7EDF\uFF01\u6211\u53EF\u4EE5\u5E2E\u60A8\u89E3\u7B54\u5173\u4E8E\u7535\u6C60\u7BA1\u7406\u7CFB\u7EDF\u76F8\u5173\u7684\u5B66\u672F\u95EE\u9898\uFF0C\u6240\u6709\u56DE\u7B54\u90FD\u57FA\u4E8E\u672C\u5730\u8F7D\u5165\u7684BMS\u4E13\u4E1A\u8BBA\u6587\uFF0C\u5E76\u4F1A\u6807\u6CE8\u5F15\u7528\u6765\u6E90\u3002</p>\n                <p class=\"mb-2\">\u60A8\u53EF\u4EE5\u5C1D\u8BD5\u63D0\u95EE\u4F8B\u5982\uFF1A</p>\n                <ul class=\"list-disc ml-5 mb-2\">\n                    <li class=\"mb-1\">\u5F53\u524D <span class=\"term-highlight\">SOC</span> \u4F30\u8BA1\u4E3B\u8981\u6709\u54EA\u4E9B\u65B9\u6CD5\uFF1F</li>\n                    <li class=\"mb-1\"><span class=\"term-highlight\">SOH</span> \u9884\u6D4B\u5E38\u7528\u7684\u673A\u5668\u5B66\u4E60\u7B97\u6CD5\u662F\u4EC0\u4E48\uFF1F</li>\n                    <li>\u7535\u6C60\u70ED\u7BA1\u7406\u7684\u6700\u65B0\u7814\u7A76\u8FDB\u5C55\u6709\u54EA\u4E9B\uFF1F</li>\n                </ul>\n            </div>";
        citationContainer.innerHTML = "<div class=\"text-center py-8 text-text-secondary text-sm\">\n                <i class=\"fas fa-file-alt text-3xl mb-3 block opacity-40\"></i>\n                \u63D0\u95EE\u540E\u5C06\u5728\u6B64\u5C55\u793A\u5F15\u7528\u6587\u732E\u6765\u6E90\n            </div>";
      });

      // 问题重写示例
      rewriteBtn.addEventListener('click', function () {
        var currentQuestion = questionInput.value.trim();
        if (!currentQuestion) {
          alert('请先输入问题内容');
          return;
        }

        // 示例重写结果
        var rewritten = currentQuestion + "\uFF08\u5B66\u672F\u91CD\u5199\uFF1A\u9488\u5BF9\u9502\u79BB\u5B50\u7535\u6C60\u7BA1\u7406\u7CFB\u7EDF\u4E2D\uFF0C\u8BF7\u7CFB\u7EDF\u68B3\u7406\u5F53\u524DSOC\u4F30\u8BA1\u65B9\u6CD5\u7684\u7814\u7A76\u8FDB\u5C55\u4E0E\u4F18\u7F3A\u70B9\u5BF9\u6BD4\uFF09";
        questionInput.value = rewritten;
      });
    });
  </script>
  <!-- [/JSMOD] j2_核心问答功能 -- 实现问答交互、流式输出、引用高亮等功能 -->
  <!-- [JSMOD] j3_重建索引功能 -->
  <script id="rebuild-index">
    document.addEventListener('DOMContentLoaded', function () {
      var rebuildBtn = document.getElementById('rebuild-index');
      var modal = document.getElementById('rebuild-modal');
      var progressBar = document.getElementById('rebuild-progress');
      var statusEl = document.getElementById('rebuild-status');
      var closeBtn = document.getElementById('close-rebuild-modal');
      var steps = [{
        percent: 25,
        text: '正在解析PDF文档...'
      }, {
        percent: 45,
        text: '正在进行文本清洗与分片...'
      }, {
        percent: 70,
        text: '正在进行文本向量化计算...'
      }, {
        percent: 90,
        text: '正在构建FAISS索引...'
      }, {
        percent: 100,
        text: '索引存储完成！'
      }];
      rebuildBtn.addEventListener('click', function () {
        modal.classList.remove('hidden');
        progressBar.style.width = '10%';
        statusEl.innerHTML = "<p class=\"mb-1\"><i class=\"fas fa-spinner fa-spin mr-2 text-primary\"></i>\u6B63\u5728\u89E3\u6790PDF\u6587\u6863...</p>";
        closeBtn.classList.add('hidden');
        var stepIndex = 0;
        var interval = setInterval(function () {
          stepIndex++;
          if (stepIndex < steps.length) {
            var step = steps[stepIndex];
            progressBar.style.width = step.percent + '%';
            statusEl.innerHTML += "<p class=\"mb-1\"><i class=\"fas fa-spinner fa-spin mr-2 text-primary\"></i>".concat(step.text, "</p>");
          } else {
            clearInterval(interval);
            statusEl.innerHTML = steps.map(function (step) {
              return "<p class=\"mb-1\"><i class=\"fas fa-check-circle mr-2 text-green-500\"></i>".concat(step.text.replace('正在', '已完成'), "</p>");
            }).join('');
            closeBtn.classList.remove('hidden');

            // 更新向量库状态
            var vectorStatus = document.querySelector('.bg-green-100');
            vectorStatus.textContent = '索引已加载';
          }
        }, 1200);
      });
      closeBtn.addEventListener('click', function () {
        modal.classList.add('hidden');
      });

      // 点击外部关闭模态框
      modal.addEventListener('click', function (e) {
        if (e.target === modal) {
          modal.classList.add('hidden');
        }
      });
    });
  </script>
  <!-- [/JSMOD] j3_重建索引功能 -- 实现重建索引进度展示动画 -->
  <!-- [JSMOD] j4_主题切换功能 -->
  <script id="theme-toggle">
    document.addEventListener('DOMContentLoaded', function () {
      var themeToggle = document.getElementById('theme-toggle');
      var icon = themeToggle.querySelector('i');
      var isDark = false;
      themeToggle.addEventListener('click', function () {
        isDark = !isDark;
        if (isDark) {
          document.body.classList.remove('bg-neutral');
          document.body.classList.add('bg-gray-900');
          document.body.classList.add('text-white');
          icon.classList.remove('fa-moon');
          icon.classList.add('fa-sun');
        } else {
          document.body.classList.add('bg-neutral');
          document.body.classList.remove('bg-gray-900');
          document.body.classList.remove('text-white');
          icon.classList.add('fa-moon');
          icon.classList.remove('fa-sun');
        }
      });
    });
  </script>
  <!-- [/JSMOD] j4_主题切换功能 -- 实现亮色/暗色主题切换 -->
</html>
