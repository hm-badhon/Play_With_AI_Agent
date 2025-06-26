import streamlit as st
import requests
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")]
)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Banking Chatbot", layout="centered")
st.title("🏦 Intelligent Banking Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

# Input box
user_input = st.chat_input("Ask about loans, accounts, or transactions...")

if user_input:
    try:
        if not user_input.strip():
            st.error("Please enter a valid query.")
            logger.warning("Empty input received")
            st.stop()
        
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Send to FastAPI backend with timeout
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/chat")
        response = requests.post(
            backend_url,
            json={"query": user_input},
            timeout=10
        )
        response.raise_for_status()

        answer = response.json().get("response", "No response received")
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        logger.info("Successfully processed query and displayed response")
    except requests.exceptions.RequestException as e:
        st.error("Failed to connect to the server. Please try again later.")
        logger.error(f"Request error: {str(e)}")
    except Exception as e:
        st.error("An unexpected error occurred.")
        logger.error(f"Unexpected error: {str(e)}")