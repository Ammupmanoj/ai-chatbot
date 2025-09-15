import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import base64

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Inject improved CSS and JS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #1f2937;
    font-family: 'Poppins', 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
}

.creator-banner {
    text-align: center;
    font-size: 12px;
    color: #d1d5db;
    margin-bottom: 10px;
    user-select: none;
}
.creator-banner a {
    color: #a78bfa;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s ease;
}
.creator-banner a:hover {
    color: #c4b5fd;
    text-decoration: underline;
}

.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 20px;
    border-radius: 20px;
    background: #f3f4f6cc;
    margin-bottom: 20px;
    border: 1px solid #e0e7ff;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
    scroll-behavior: smooth;
}

.user-msg, .bot-msg {
    display: flex;
    align-items: flex-end;
    margin: 12px 0;
    animation: fadeInUp 0.4s ease forwards;
}

.user-msg {
    justify-content: flex-end;
}

.user-bubble, .bot-bubble {
    padding: 14px 18px;
    border-radius: 24px;
    max-width: 70%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    font-size: 16px;
    line-height: 1.4;
    white-space: pre-wrap;
    word-wrap: break-word;
    user-select: text;
    transition: background-color 0.3s ease;
}

.user-bubble {
    background: #6366f1;
    color: white;
    border-bottom-right-radius: 4px;
}

.user-bubble:hover {
    background: #4f46e5;
}

.bot-bubble {
    background: #e0e7ff;
    color: #1e293b;
    border-bottom-left-radius: 4px;
}

.bot-bubble:hover {
    background: #c7d2fe;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 0 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    flex-shrink: 0;
}

.typing {
    font-style: italic;
    color: #6b7280;
    margin-left: 52px;
    animation: blink 1.2s infinite;
    font-size: 15px;
}

.timestamp {
    font-size: 11px;
    color: #9ca3af;
    margin: 4px 52px;
    user-select: none;
}

.stChatInput textarea {
    border-radius: 20px !important;
    padding: 14px !important;
    background: #eef2ff !important;
    color: #1e293b !important;
    font-size: 16px !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    border: none !important;
    resize: none !important;
    transition: box-shadow 0.3s ease;
}
.stChatInput textarea:focus {
    box-shadow: 0 0 0 3px #6366f1 !important;
    outline: none !important;
}

.stChatInput button {
    background-color: #6366f1 !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 10px 24px !important;
    font-weight: 700;
    font-size: 16px !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.5);
    border: none !important;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.stChatInput button:hover {
    background-color: #4f46e5 !important;
}

.footer {
    margin-top: 30px;
    text-align: center;
    font-size: 13px;
    color: #c7d2fe;
    user-select: none;
}

h1 {
    font-weight: 700;
    color: white;
    margin: 0;
    user-select: none;
}

.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 25px;
    gap: 12px;
    user-select: none;
    text-shadow: 0 2px 6px rgba(0,0,0,0.3);
}

.status {
    text-align: center;
    font-size: 14px;
    color: #a5b4fc;
    margin-bottom: 20px;
    font-weight: 600;
    user-select: none;
}

.status span {
    color: #22c55e;
    font-weight: 700;
}

.clear-btn {
    background-color: #ef4444;
    color: white;
    border-radius: 20px;
    padding: 10px 24px;
    font-weight: 700;
    font-size: 16px;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.5);
    transition: background-color 0.3s ease;
    margin-bottom: 10px;
    user-select: none;
}
.clear-btn:hover {
    background-color: #b91c1c;
}

@keyframes blink {
    0%, 100% { opacity: 0.2; }
    50% { opacity: 1; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Creator badge with GitHub link
st.markdown('''
<div class="creator-banner">
    Made with ❤️ by <a href="https://github.com/Ammupmanoj" target="_blank">Ammu P Manoj</a> | Powered by OpenAI
</div>
''', unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="header-container">
    <img src="https://i.imgur.com/rdm3W9t.png" alt="Bot" style="width:48px; height:48px;">
    <h1>AI Chatbot</h1>
</div>
<div class="status">
    Status: <span>Online</span>
</div>
""", unsafe_allow_html=True)

# Sound effect
def play_sound():
    try:
        with open("send.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# Session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    timestamp = datetime.now().strftime("%H:%M")
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-msg"><div class="user-bubble">{msg["content"]}</div>'
            f'<img src="https://i.imgur.com/7k12EPD.png" class="avatar" alt="User "></div>'
            f'<div class="timestamp" style="text-align:right;">{timestamp}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot-msg"><img src="https://i.imgur.com/rdm3W9t.png" class="avatar" alt="Bot">'
            f'<div class="bot-bubble">{msg["content"]}</div></div>'
            f'<div class="timestamp" style="text-align:left;">{timestamp}</div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# User input
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="bot-msg"><img src="https://i.imgur.com/rdm3W9t.png" class="avatar" alt="Bot">'
                    '<div class="bot-bubble typing">Typing...</div></div>', unsafe_allow_html=True)
    time.sleep(1.5)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    bot_reply = response.choices[0].message.content

    placeholder.empty()
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    play_sound()
    st.experimental_rerun()

# Clear chat button with improved style
if st.button("🗑 Clear Chat", key="clear", help="Clear the chat history", args=None):
    st.session_state.messages = []
    st.experimental_rerun()

# Optional footer
st.markdown("""
<div class="footer">
    &copy; 2024 AI Chatbot. All rights reserved.
</div>
""", unsafe_allow_html=True)
