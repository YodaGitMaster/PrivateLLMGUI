from typing import Dict, Optional, Union, List
import requests
import streamlit as st
import os, sys
sys.path.insert(0, os.path.abspath("../utils"))
from utils.memory import ChatMemory as mem
import json
import time 

def initialize_memory() -> mem:
    """Initialize ChatMemory."""
    return mem()


m: mem = initialize_memory()


def retrieve_clicked_button(button_states: Dict[str, bool]) -> Optional[str]:
    """Retrieve the clicked button from button_states."""
    for key, value in button_states.items():
        if value:
            return key
    return None



def api_call(text):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3", "prompt": text},
    )

    generated_text = response.text.splitlines()
    generated_text = [json.loads(line) for line in generated_text]

    full_text = ''
    for word in generated_text:
        full_text += word['response']
    
    print(f"Status Code: {response.status_code}")
    
    try:
        return full_text
    except Exception as e:
        print(f"Error: {e}")
        return None

def query():
    user_input: str = st.text_area("Question", key="user_input", height=180)
    if st.button("Generate Response") and len(user_input) >= 3:
        start_time = time.time()

        with st.spinner("Generating Response..."):
            try:
                answer = api_call(user_input)

                st.write("Generated Text:")
                st.write(answer)

                summary = 'summarize this text in one sentence of 5 words\n'
                summary_result = api_call(text=f"{summary}\n text:\n {user_input[:150]}")
                print(summary_result)
                m.write_to_file(f"Question:\n{user_input}\n\nAnswer:\n{answer}", title=summary_result)

                elapsed_time = time.time() - start_time
                st.success(f"Text generated in {elapsed_time:.2f} seconds")

            except Exception as e:
                st.error(f"Error generating text: {e}")
                

def display_chat_history(chats: List[str]):
    """Display chat history or handle new chat."""
    st.sidebar.title('Chat History')

    button_states: Dict[str, bool] = {}

    for chat in chats:
        button_states[chat] = st.sidebar.button(
            f'{chat.strip(".log")[:20]} ...', key=chat)

    clicked_button: Optional[str] = retrieve_clicked_button(button_states)

    if clicked_button:
        content: str = m.read_log_file(clicked_button)
        content: List[str] = content.split('\n')
        content: List[str] = [item for item in content if item != ""]
        st.write(content[0:])
    else:
        query()



def main():
    """Main function to execute the Streamlit app."""
    st.title("PrivateGPT")
  
    st.markdown(
        """
        <style>
            .stButton > button {
                width: 100%;
                border-radius: 50px;
                height:10%; /* Set the desired height here */
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    new_chat: bool = st.sidebar.button(f'New Chat', key='Search')
    


    chats: List[str] = m.list_log_files()
    display_chat_history(chats)


if __name__ == "__main__":
    main()
