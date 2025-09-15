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

# Inject CSS
st.markdown("""
<style>
body {
    background: white;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.creator-banner {
    text-align: center;
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 5px;
}
.chat-container {
    max-height: 550px;
    overflow-y: auto;
    padding: 20px;
    border-radius: 16px;
    background: #ffffff;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border: 1px solid #e5e7eb;
}
.user-msg, .bot-msg {
    display: flex;
    align-items: flex-end;
    margin: 10px 0;
}
.user-bubble, .bot-bubble {
    padding: 12px;
    border-radius: 12px;
    max-width: 70%;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    animation: fadeIn 0.3s ease-in-out;
    font-size: 15px;
}
.user-bubble {
    background: #3b82f6;
    color: white;
    margin-left: auto;
}
.bot-bubble {
    background: #e5e7eb;
    color: black;
    margin-right: auto;
}
.avatar {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    margin: 0 8px;
}
.typing {
    font-style: italic;
    color: #6b7280;
    margin-left: 45px;
    animation: blink 1s infinite;
}
@keyframes blink {
    0% { opacity: 0.2; }
    50% { opacity: 1; }
    100% { opacity: 0.2; }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.timestamp {
    font-size: 10px;
    color: #9ca3af;
    margin: 2px 45px;
}
.footer {
    margin-top: 20px;
    text-align: center;
    font-size: 12px;
    color: #6b7280;
}
.stTextInput > div > input {
    border-radius: 12px !important;
    padding: 14px !important;
    background: #f3f4f6 !important;
    color: black !important;
    font-size: 16px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.stButton > button {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Creator badge
st.markdown('''
<div class="creator-banner">
    Made with ❤️ by <a href="https://github.com/Ammupmanoj" target="_blank" style="color:#3b82f6; text-decoration:none;">Ammu P Manoj</a> | Powered by OpenAI
</div>
''', unsafe_allow_html=True)

# Header
st.markdown(f"""
<div style="display:flex; align-items:center; justify-content:center; margin-bottom:20px;">
    <img src="https://i.imgur.com/rdm3W9t.png" style="width:40px; height:40px; margin-right:10px;">
    <h1 style="font-size:28px; margin:0;">AI Chatbot</h1>
</div>
<div style="text-align:center; font-size:13px; color:#6b7280; margin-bottom:10px;">
    Status: <span style="color:limegreen;">Online</span>
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
            f'<img src="https://i.imgur.com/7k12EPD.png" class="avatar"></div>'
            f'<div class="timestamp">{timestamp}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot-msg"><img src="https://i.imgur.com/rdm3W9t.png" class="avatar">'
            f'<div class="bot-bubble">{msg["content"]}</div></div>'
            f'<div class="timestamp">{timestamp}</div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Input box
user_input = st.text_input("Ask anything...", key="input")
if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div class="bot-msg"><img src="https://i.imgur.com/rdm3W9t.png" class="avatar">'
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
    st.rerun()

# Clear chat
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    AI can make mistakes. Please double-check responses.
</div>
""", unsafe_allow_html=True)
