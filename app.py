import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Set page settings
st.set_page_config(page_title="Helpy ChatBot", layout="wide")

# Sidebar
with st.sidebar:
    #st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/368px-Google_2015_logo.svg.png", width=100)
    st.markdown("## 🤖 Helpy ChatBot")
    st.caption("Powered by **Gemini 2.5 Flash**")
    st.markdown("---")
    if st.button("🔄 Reset Chat"):
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.messages = []
        st.rerun()  # Fixed here

# Initialize memory
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("""
    <style>
        .big-title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 16px;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">💬 Helpy ChatBot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask me anything — I’m here to help!</div>', unsafe_allow_html=True)
st.markdown("---")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Type your message...")  # Now text will be visible normally

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Gemini response
    response = st.session_state.chat.send_message(user_input)
    ai_message = response.text

    st.chat_message("assistant").markdown(ai_message)
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
