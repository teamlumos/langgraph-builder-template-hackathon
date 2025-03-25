from markdown_utils import list_available_sessions, load_markdown_files
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

def page_config():
    # Page configuration
    st.set_page_config(
        page_title="Integration Research Agent",
        page_icon="💬",
        layout="wide"
    )
    
    # Title and introduction
    st.title("Integration Research Agent")
    st.markdown("NYC Integration Hackathon March, 2025")

def session_reset(reset_thread_id=True):
    if reset_thread_id:
        if "thread_id" in st.session_state:
            st.session_state.thread_id = None

    st.session_state.thread_id = None if "thread_id" not in st.session_state else st.session_state.thread_id

    st.session_state.markdown_files = load_markdown_files(st.session_state.thread_id) if "thread_id" in st.session_state and st.session_state.thread_id is not None else []

    st.session_state.chat_history = []
    st.session_state.current_markdown = ""
    
    st.session_state.selected_file = None
    st.session_state.available_sessions = list_available_sessions()
