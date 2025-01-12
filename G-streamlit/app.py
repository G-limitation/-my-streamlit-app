import streamlit as st
import os
from volcenginesdkarkruntime import Ark

# Streamlit 应用标题
st.title("威少AI助手5")

# 从环境变量中获取API密钥
api_key = os.environ.get("ARK_API_KEY")

# 如果环境变量中没有API密钥，则提示用户输入
if not api_key:
    api_key = st.text_input("请输入您的Volcengine API密钥：", type="password")

# 初始化Ark客户端
client = Ark(api_key=api_key)

# 用于存储对话历史的列表
conversation_history = []

# 读取 prompts.txt 文件中的内容作为 system content
def read_prompts_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"文件 {file_path} 未找到。请检查文件路径。")
        return ""
    except Exception as e:
        st.error(f"读取文件时发生错误：{e}")
        return ""

system_content = read_prompts_file("c:/Users/Administrator/Desktop/G工作/prompts.txt")

# 将 system content 添加到对话历史中
conversation_history.append({"role": "system", "content": system_content})

# 用户输入问题的文本框
user_input = st.text_input("请输入你的问题：")

# 检查是否存在会话状态，如果不存在，则初始化
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# 当用户输入问题后，调用模型并显示响应
if user_input:
    st.write("正在思考中...")
    # 将当前问题添加到对话历史中
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    # 在将用户的问题添加到对话历史之后，添加一条分割线
    st.markdown("---")
    # 创建带有对话历史的Completion请求
    try:
        completion = client.chat.completions.create(
            model="ep-20250107204359-j7dsw",
            messages=st.session_state.conversation_history,
        )
        response = completion.choices[0].message.content
        # 将模型的回答添加到对话历史中
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        # 分栏显示对话记录
        col1, col2 = st.columns(2)
        with col1:
            for message in st.session_state.conversation_history:
                if message["role"] == "user":
                    st.markdown(f"<div style='text-align: left;'>你：{message['content']}</div>", unsafe_allow_html=True)
        with col2:
            for message in st.session_state.conversation_history:
                if message["role"] == "assistant":
                    st.markdown(f"<div style='text-align: left;'>AI：{message['content']}</div>", unsafe_allow_html=True)
        # 在将用户的问题添加到对话历史之后，添加一条分割线
        st.markdown("---")
    except Exception as e:
        st.error(f"调用API时发生错误：{e}")
