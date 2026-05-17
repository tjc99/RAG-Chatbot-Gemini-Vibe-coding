
# 🌊 Vibe Coding 终极稳健版 RAG Bot

这是一个基于 **Streamlit**、**FAISS 本地向量数据库** 和 **Gemini 2.5 Flash** 大脑构建的文档白盒 RAG 问答机器人。

### ✨ 核心亮点
* **本地向量化 (0报错)**：首次运行自动下载轻量级模型，彻底告别远程 Embedding 接口不稳定的问题。
* **纯净 Python 逻辑 (0黑盒)**：没有晦涩复杂的 LangChain 封装，纯手工打造核心 Prompt，逻辑清晰可见。
* **可交互上传 PDF**：支持网页端直接拖拽/上传文档，实时消化，即刻对话。

---

## 🚀 快速开始

### 1. 克隆本仓库
打开终端或 Anaconda Prompt，运行以下命令：
```bash
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

```

### 2. 安装依赖

运行以下命令一键安装所有需要的 Python 库：

```bash
pip install -r requirements.txt

```

### 3. 启动应用

依赖安装完成后，运行以下命令启动 Streamlit 网页端：

```bash
streamlit run rag_chatbot_gemini.py

```

---

## ⚙️ 使用说明

1. **打开网页**：应用启动后，在浏览器中打开显示的本地链接（通常是 `http://localhost:8501`）。
2. **配置密钥**：在网页左侧边栏输入你的 **Google API Key**。
3. **上传文档**：在左侧边栏上传一份 **PDF 格式** 的文档。
4. **模型初始化**：
> 💡 **提示**：首次上传文件时，系统会自动在本地下载轻量级 Embedding 模型（`all-MiniLM-L6-v2`，约几十 MB），请耐心等待片刻。


5. **开始对话**：当系统提示“已准备就绪”后，即可在右侧聊天框中向文档提问！

```

```
