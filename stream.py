import streamlit as st
from llama_index.core.llms import ChatMessage, MessageRole
import logging
import time
from llama_index.llms.ollama import Ollama
import os
import numpy as np
ollama_directory = os.getenv("OLLAMA_DIRECTORY")
logging.basicConfig(level = logging.INFO)

#we use this to store chat history, using if statement to check if messages are already there or not o/w initialize an empty array
if 'messages' not in st.session_state:
    st.session_state.messages=[]
#handles interaction with llama model
def stream_chat(model, messages):
    try:
        llm = Ollama(model=model, request_timeout=120) #initializes llama model with a specific timeout thing of 120 secs
        resp = llm.stream_chat(messages) #streams chat responses from the llama model
        response = ""
        response_placeholder = st.empty() #creates an entire section in the streamlit app for dynamically update the response
        for r in resp:
            response += r.delta
            response_placeholder.write(response)
            logging.info(f"Model:{model}, Messages:{messages}, Response:{response}") #logs all the models messages and responses 
            return response
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}") #catches any errors and logs them 
        raise e
def main():
    st.title("Chat with LLMs Models")
    logging.info("App Started")

    model = st.sidebar.selectbox("Choose a model", ["mymodel", "llama3.1 8b", "phi3", "mistral"])
    logging.info(f"Model Selected : {model}")

    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info(f"User Input: {prompt}")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if st.session_state.messages[0]["role"] != "assistant" :
        with st.chat_message("assistant"):
            start_time = time.time()
            logging.info("Generating info...")
    
    with st.spinner("Writing..."):
        try:
            messages = [ChatMessage(role = msg["role"], content = msg["content"]) for message in st.session_state.messages]
            response_message = stream_chat(model, messages)
            duration = time.time() - start_time
            response_message_with_duration = f"{response_message}\n\nDuration: {duration:.2f} seconds"
            st.session_state.messages.append({"role" : "assistant", "content" : response_message_with_duration})
            st.write(f"Duration: {duration:.2f} seconds")
            logging.info(f"Response: {response_message}, Duration : {duration:.2f} s")
        
        except Exception as e :
            st.session_state.messages.append({"role" : "assistant", "content" : stre(e)})
            st.error("An error has occured while generating the information")
            logging.error(f"Error : {str(e)}")

if __name__ == "__main__" :
    main()
