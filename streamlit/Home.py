import streamlit as st
from utils import page_config, session_reset
import uuid
from markdown_utils import load_markdown_files

page_config()
session_reset()

# Session selector
selected_session = st.selectbox(
    "Select Session:",
    options=["", "New Session"] + st.session_state.available_sessions,
    index=0 if st.session_state.thread_id not in st.session_state.available_sessions else 
          st.session_state.available_sessions.index(st.session_state.thread_id) + 1
)

if selected_session != "" and selected_session != st.session_state.thread_id:
    if selected_session == "New Session":
        selected_session = str(uuid.uuid4())
    st.session_state.thread_id = selected_session
    st.session_state.chat_history = []
    st.session_state.current_markdown = ""
    st.session_state.markdown_files = load_markdown_files(st.session_state.thread_id)
    st.session_state.selected_file = None

    st.switch_page("pages/Research.py")

