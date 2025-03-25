import os
import glob
from typing import List

def get_markdown_directory(session_id: str) -> str:
    """
    Get the directory path for storing markdown files.
    Creates the directory if it doesn't exist.
    
    Returns:
        str: Path to the markdown directory
    """
    markdown_dir = os.path.join(os.getcwd(), "my-docs", session_id)
    os.makedirs(markdown_dir, exist_ok=True)
    return markdown_dir

def get_markdown_file_path(filename: str, session_id: str) -> str:
    """
    Get the full path for a markdown file.
    
    Args:
        filename: The name of the markdown file
        
    Returns:
        str: Full path to the markdown file
    """
    return os.path.join(get_markdown_directory(session_id), filename)

def save_markdown(filename: str, content: str, session_id: str) -> None:
    """
    Save markdown content to a file.
    
    Args:
        filename: The name of the markdown file
        content: The markdown content to save
    """
    file_path = get_markdown_file_path(filename, session_id)
    with open(file_path, 'w') as f:
        f.write(content)

def load_markdown_files(session_id: str) -> List[str]:
    """
    Load a list of all available markdown files.
    
    Returns:
        List[str]: List of markdown filenames
    """
    markdown_dir = get_markdown_directory(session_id)
    files = glob.glob(os.path.join(markdown_dir, "*.md"))
    return [os.path.basename(f) for f in sorted(files)]

def load_markdown_content(filename: str, session_id: str) -> str:
    """
    Load the content of a markdown file.
    
    Args:
        filename: The name of the markdown file
        
    Returns:
        str: The content of the markdown file
    """
    file_path = get_markdown_file_path(filename, session_id)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read()
    return ""


def list_available_sessions():
    """List all available session directories in my-docs"""
    my_docs_path = "my-docs"  # adjust path as needed
    if not os.path.exists(my_docs_path):
        return []
    return [d for d in os.listdir(my_docs_path) 
            if os.path.isdir(os.path.join(my_docs_path, d))]
