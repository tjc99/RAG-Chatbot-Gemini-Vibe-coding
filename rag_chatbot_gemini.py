import streamlit as st
import os
import tempfile
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
# 
# # === 核心配置 ===
FAISS_DIR = "faiss_local_index"
# 
st.set_page_config(page_title="Vibe RAG Bot", page_icon="🌊", layout="wide")
st.title("🌊 Vibe Coding 终极稳健版 RAG")
st.caption("本地向量化 (0报错) + 纯净 Python 逻辑 (0黑盒) + Gemini 大脑")
# 
# # === 侧边栏：获取必要信息 ===
with st.sidebar:
     st.header("⚙️ 准备工作")
     api_key = st.text_input("🔑 填入 Google API Key", type="password", help="仅用于最终聊天对话")
     uploaded_file = st.file_uploader("📄 上传你的 PDF 文档", type=["pdf"])
 
# # === 核心处理函数 (带缓存防重复运行) ===
@st.cache_resource(show_spinner=False)
def build_vector_store(file_bytes):
     # 1. 每次上传新文件，清理旧战场
     if os.path.exists(FAISS_DIR):
         shutil.rmtree(FAISS_DIR)
# 
#     # 2. 安全写入临时文件
     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
         tmp.write(file_bytes)
         tmp_path = tmp.name
# 
     try:
#         # 3. 加载与切割
         loader = PyPDFLoader(tmp_path)
         docs = loader.load()
         splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
         chunks = splitter.split_documents(docs)
# 
#         # 4. 【核心稳健点】使用本地 HuggingFace 模型进行向量化！
#         # 首次运行会自动下载模型权重，彻底告别 Google API 404 错误
         embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
 
#         # 5. 存入 FAISS 数据库
         vector_store = FAISS.from_documents(chunks, embeddings)
         vector_store.save_local(FAISS_DIR)
         return vector_store
     finally:
         os.remove(tmp_path)
# 
# # === 聊天交互主逻辑 ===
if uploaded_file and api_key:
#     # 显示处理进度
     with st.spinner("⏳ 正在用本地模型消化文档 (首次需下载几十MB模型，请稍候)..."):
         vs = build_vector_store(uploaded_file.read())
     st.success(f"🎉 **{uploaded_file.name}** 已准备就绪！")
# 
#     # 初始化大模型与聊天历史
     llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
# 
     if "messages" not in st.session_state:
         st.session_state.messages = []
# 
#     # 渲染历史对话
     for msg in st.session_state.messages:
         with st.chat_message(msg["role"]):
             st.markdown(msg["content"])
# 
#     # 处理用户提问
     if user_input := st.chat_input("向文档提问吧..."):
#         # 显示用户问题
         st.session_state.messages.append({"role": "user", "content": user_input})
         with st.chat_message("user"):
             st.markdown(user_input)
# 
         with st.chat_message("assistant"):
             with st.spinner("思考中..."):
#                 # 【白盒 RAG 逻辑】没有任何晦涩的 Chain！
# 
#                 # 第 1 步：检索
                 retrieved_docs = vs.similarity_search(user_input, k=4)
                 context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
# 
#                 # 第 2 步：纯手工打造 Prompt
                 prompt = f"""你是一个精准的文档阅读助手。请严格根据下面的<参考文档>来回答用户的<问题>。
# 如果你不知道，或者文档里没有写，请直接回复“抱歉，文档中并未提及相关信息。”，不要自行编造。
# 
# <参考文档>
# {context_text}
# </参考文档>
# 
# <问题>
# {user_input}
# </问题>
# """
#                 # 第 3 步：调用模型并展示
                 try:
                     response = llm.invoke(prompt)
                     answer = response.content
                     st.markdown(answer)
# 
#                     # 极客专属功能：查看原文片段
                     with st.expander("👀 查看底层检索到的原文片段"):
                         st.info(context_text)
# 
#                     # 保存历史
                     st.session_state.messages.append({"role": "assistant", "content": answer})
                 except Exception as e:
                     st.error(f"❌ 调用 Gemini API 时发生错误：{e}")
# 
elif not api_key:
     st.info("👈 请先在左侧输入你的 Google API Key。")
elif not uploaded_file:
     st.info("👈 请在左侧上传一份 PDF 文档开始。")