# import os
# import time
# import tempfile
# from pathlib import Path

# import streamlit as st
# from dotenv import load_dotenv
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()
# API_KEY = os.getenv("GOOGLE_API_KEY")

# # Configure Gemini if API key is available
# if API_KEY:
#     genai.configure(api_key=API_KEY)
# else:
#     st.error("Missing Google API Key. Please set it in your .env file.")

# # Streamlit Page Configuration
# st.set_page_config(
#     page_title="Multimodal AI Agent - Video Summarizer",
#     page_icon="🤖",
#     layout='wide'
# )

# st.title("🎥 Phidata Video AI Summarizer Agent")
# st.header("Powered by Gemini 2.0 Flash Exp 🚀")

# # Initialize AI Agent
# @st.cache_resource
# def initialize_agent():
#     return Agent(
#         name="Video AI Summarizer",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],
#         markdown=True
#     )

# # Instantiate the agent
# multimodal_agent = initialize_agent()

# # Upload Video
# video_file = st.file_uploader(
#     "📤 Upload a video file", 
#     type=['mp4', 'avi', 'mov'], 
#     help="Upload a video for AI analysis"
# )

# if video_file:
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
#         temp_video.write(video_file.read())
#         video_path = temp_video.name

#     st.video(video_path, format='video/mp4', start_time=0)

#     user_query = st.text_area(
#         "🧠 What insights are you seeking from the video?",
#         placeholder="Ask anything about the video content. The AI agent will analyze and gather relevant information."
#     )

#     if user_query:
#         with st.spinner("Analyzing video content and gathering insights..."):
#             # You can pass the video path or metadata to the agent if supported
#             response = multimodal_agent.run(user_query)
#             st.markdown("### 💡 AI Response:")
#             st.markdown(response.content if hasattr(response, "content") else response)

import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai

# Load environment
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("🚨 Google API Key not found in environment!")

# Page Config
st.set_page_config(
    page_title="🎬 Video AI Agent Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("🎥 Video AI Agent Chat Interface")
st.caption("Ask questions and get summarized insights from your video")

# Initialize Agent
@st.cache_resource
def initialize_agent():
    return Agent(
        name="VideoSummarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True
    )

agent = initialize_agent()

# Initialize session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Video uploader
video_file = st.file_uploader("📤 Upload a video", type=['mp4', 'avi', 'mov'])

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_vid:
        temp_vid.write(video_file.read())
        video_path = temp_vid.name

    st.video(video_path)

    st.markdown("---")

    # Chat section
    with st.container():
        st.subheader("💬 Chat with AI about your video")

        # Show chat history
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.chat_message("🧑‍💻 You").markdown(msg)
            else:
                st.chat_message("🤖 AI").markdown(msg)

        user_input = st.chat_input("Ask something about the video...")

        if user_input:
            st.session_state.chat_history.append(("user", user_input))
            with st.chat_message("🤖 AI"):
                with st.spinner("Analyzing..."):
                    response = agent.run(user_input)
                    ai_response = response.content if hasattr(response, "content") else str(response)
                    st.markdown(ai_response)
                    st.session_state.chat_history.append(("ai", ai_response))
