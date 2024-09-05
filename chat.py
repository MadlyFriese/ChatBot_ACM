from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st

st.title('Chatbot with Multiple LLMs')

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "previous_model" not in st.session_state:
    st.session_state.previous_model = None

option = st.selectbox(
    "Choose the model",
    ("llama2", "llama3.1:8b", "stable-code"),
    index=0,
    placeholder="Model",
)

if st.session_state.previous_model != option:
    st.session_state.chat_log = []
    st.session_state.previous_model = option

llm = None
if option == "llama2":
    llm = Ollama(model="llama2")
elif option == "llama3.1:8b":
    llm = Ollama(model="llama3.1:8b")
elif option == "stable-code":
    llm = Ollama(model="stable-code")

for message in st.session_state.chat_log:
    role, content = message.split(": ", 1)
    with st.chat_message(role.lower()):
        st.write(f"{role}: {content}")

if llm:
    input_text = st.chat_input("Input your query")

    output_parser = StrOutputParser()

    if input_text:
        st.session_state.chat_log.append(f"User: {input_text}")

        conversation_history_str = "\n".join(st.session_state.chat_log)
        formatted_prompt = (
            f"You are a chatbot. Please reply to the input given by the user accordingly. "
            f"Remember what you were asked previously for context on future prompts.\n\n{conversation_history_str}"
        )

        with st.chat_message("user"):
            st.write("User:", input_text)
       
        response = llm(formatted_prompt)  
        parsed_response = output_parser.parse(response)

        with st.chat_message("assistant"):
            st.write("Bot:", parsed_response)
     
        st.session_state.chat_log.append(f"Bot: {parsed_response}")

