import streamlit as st
import markdown
from markdown_utils import save_markdown, load_markdown_files, get_markdown_file_path
from agent import run_agent
import streamlit as st
from utils import page_config, session_reset

if st.query_params.get("thread_id", None) is None and "thread_id" not in st.session_state:
    st.warning("No session provided. Please select a session from the Home page.")
    st.stop()

st.query_params["thread_id"] = st.session_state.thread_id if "thread_id" in st.session_state else st.query_params.get("thread_id", None)
st.session_state.thread_id = st.query_params.get("thread_id", None) 

if st.query_params.get("thread_id", None) is None or st.query_params.get("thread_id", None) == "None":
    st.switch_page("Home.py")
    st.stop()

page_config()
session_reset(reset_thread_id=False)

st.subheader("Session: " + st.session_state.thread_id)

# Create two columns for the layout
col1, col2 = st.columns([3, 3])

with st.sidebar:
    st.subheader("Agent Chat")
    if len(st.session_state.markdown_files) == 0:
                
            # User input
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_area("Your message:", height=100)
                submit_button = st.form_submit_button("Send")
                
                if submit_button and user_input:
                    # Run the agent to get a response
                    try:
                        with st.spinner("Agent is thinking..."):
                            # Display chat history
                            chat_container = st.container()
                            with chat_container:
                                st.write(f"**You:** {user_input}")
                                st.write_stream(run_agent(user_input, st.session_state.thread_id))
                        
                        # Save the markdown and update the file list
                        st.session_state.markdown_files = load_markdown_files(st.session_state.thread_id)
                    except Exception as e:
                        st.error(f"Error while processing your request: {str(e)}")
                
            # Reset conversation button
            if st.button("Reset Conversation", key="reset_conversation"):
                st.rerun()
    else:
        st.info("Once a session is created, you can't trigger another agent run. Please create a new session to start a new conversation.")

# File selection
if st.session_state.markdown_files:
    selected_file = st.selectbox(
        "Select a markdown file to edit:", 
        st.session_state.markdown_files,
        index=st.session_state.markdown_files.index(st.session_state.selected_file) if st.session_state.selected_file in st.session_state.markdown_files else 0
    )
    
    if selected_file != st.session_state.selected_file:
        # Load the selected file's content
        file_path = get_markdown_file_path(selected_file, st.session_state.thread_id)
        with open(file_path, 'r') as f:
            st.session_state.current_markdown = f.read()
        st.session_state.selected_file = selected_file
else:
    st.info("No markdown files available yet. Start a conversation with the agent to generate some!")


st.subheader("Markdown Editor")

# Create tabs for Edit and Preview
preview_tab, edit_tab = st.tabs(["Preview", "Edit"])

with edit_tab:
    # Markdown editor
    markdown = st.text_area(
        "Edit your markdown here:",
        value=st.session_state.current_markdown,
        height=300,
        key="markdown_editor"
    )

with preview_tab:
    # Markdown preview
    st.markdown("### Preview")
    if markdown:
        st.markdown(markdown)
    else:
        st.info("No content to preview yet.")

# Save button
if st.button("Save Changes") and st.session_state.selected_file:
    try:
        save_markdown(st.session_state.selected_file, markdown, st.session_state.thread_id)
        st.success(f"Saved changes to {st.session_state.selected_file}")
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
