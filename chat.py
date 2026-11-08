import os
import streamlit as st
from openai import OpenAI
from datetime import datetime
import json


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

# 设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

st.title("AI智能伴侣")

# 保存会话信息
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "messages": st.session_state.messages,
            "current_session": st.session_state.current_session
        }

        #创建会话管理文件夹
        if not os.path.exists("sessions"): # 如果不存在文件夹则创建
            os.mkdir("sessions")

        # 保存会话信息到文件中
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

# 生成会话标识
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 加载所有历史会话
def load_all_sessions():
    session_list = []
    if os.path.exists("sessions"):
        for file_name in os.listdir("sessions"):
            if file_name.endswith(".json"):
                session_list.append(file_name[:-5])
    # 返回会话列表
    session_list.sort(reverse=True)  # 按时间倒序排列
    return session_list

# 加载指定会话
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.messages = session_data["messages"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话失败")

# 删除指定会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            # 如果删除的是当前会话，则清空聊天记录并生成新的会话标识
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败")


#系统提示词
system_prompt = """
    你叫 %s，现在是用户的真实伴侣，请完全带入伴侣角色。
    规则：
        1.每次只回复1条消息
        2.禁止任何场景或状态描述文字
        3.匹配用户的语言
        4.回复简单，像微信聊天一样
        5.有需要的话可以使用❤️💋等emoji表情
        6.用符合伴侣性格的方式对话
        7.回复的内容，要充分体现伴侣的性格特征
    伴侣性格：
        - %s
    你必须严格遵守上述规则来回复用户
"""

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示侧边栏中的伴侣昵称和性格
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"

if "nature" not in st.session_state:
    st.session_state.nature = "活波开朗的东北姑娘"

# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

# 左侧侧边栏：with：streamlit中的上下文管理器
with st.sidebar:
    # 会话管理
    st.subheader('AI控制面板')
    if st.button('新建会话',width="stretch",icon="🖍️"):
        # 保存当前会话信息
        save_session()

        # 新建对话
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun() # 重新运行页面

    # 历史会话
    st.text('历史会话')
    session_list = load_all_sessions()
    for session in session_list:
        col1, col2 = st.columns([4,1])
        with col1:
            if st.button(session, icon="📜", width="stretch", key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", icon="❌", width="stretch", key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    # 添加分割线
    st.divider()

    # 伴侣信息设置
    st.subheader('伴侣信息')

    # 用户输入伴侣昵称和性格
    nick_name = st.text_input('昵称',placeholder='请输入昵称',value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area('性格',placeholder='请输入性格描述',value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

# 显示当前会话名称
st.text(f"会话名称: {st.session_state.current_session}")

# 显示聊天记录
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入您要问的问题...")
if prompt:
    st.chat_message("user").write(prompt)

    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用 DeepSeek 获取 AI 回答
    response = client.chat.completions.create(
        model=os.getenv("DEEPSEEK_MODEL"),
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True  # 设置为 True 以启用流式输出
    )

    # 显示 AI 回答（非流式输出）
    # print('-------->大模型返回的结果',response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #创建一个空容器用于显示 AI 回答（流式输出）
    response_container = st.empty()

    # 显示 AI 回答（流式输出）
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_container.chat_message("assistant").write(full_response)


    # 保存 AI 回答
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 保存会话信息
    save_session()
