# BMS RAG 问答系统 - 微信小程序前端

本项目是基于微信原生框架开发的 BMS 领域专业 RAG 问答系统移动端。

## 核心功能
- **智能问答**：支持文字/语音输入，流式显示回答内容。
- **精确溯源**：回答中包含引用角标，点击可查看原文片段与页码。
- **文献库**：查看已加载的 BMS 专业文献列表与详情。
- **系统配置**：动态切换向量引擎（火山/阿里）、调整检索 Top-K 参数。

## 快速开始

1.  **安装微信开发者工具**：[下载地址](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2.  **导入项目**：
    - 打开微信开发者工具，选择“导入项目”。
    - 目录选择当前 `mp_frontend` 文件夹。
    - AppID 使用：`wxe3a7e66516ef7f1f`。
3.  **配置后端地址**：
    - 修改 `app.js` 中的 `baseUrl`。
    - 如果是本地调试，请在开发者工具“详情” -> “本地设置”中勾选“不校验合法域名”。
4.  **添加图标资源**：
    - 由于本代码包不含二进制图片，请在 `assets/` 目录下添加以下图标（建议使用 48x48 或 64x64 的 PNG/SVG）：
        - `chat.png`, `chat_active.png` (问答 Tab)
        - `book.png`, `book_active.png` (文献 Tab)
        - `user.png`, `user_active.png` (我的 Tab)
        - `ai_avatar.png`, `user_avatar.png` (头像)
        - `mic.png` (语音图标)
        - `pdf_icon.png` (文献图标)
        - `sort.png` (排序图标)
        - `arrow_right.png` (箭头图标)
        - `empty.png` (空状态图标)

## 技术架构
- **前端**：微信小程序原生框架 (WXML/WXSS/JS)
- **后端**：FastAPI (已集成 CORS 与标准化 API 接口)
- **通信**：HTTPS / WebSocket

## 密钥管理
- 你的小程序上传私钥已保存为：`private.wxe3a7e66516ef7f1f.key`。请妥善保管，用于代码上传。
