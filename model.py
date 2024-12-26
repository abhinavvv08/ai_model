import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from bertopic import BERTopic


page_bg_img = """
<style>
body {
    background-image: url('https://e0.pxfuel.com/wallpapers/108/545/desktop-wallpaper-emoji-for-computer-simple.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


template = """
Answer the question below.

Here is the conversation history: {context}

Question : {question}

Answer:
"""

model = OllamaLLM(model = "llama3:8b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

st.title("AI Chatbot 🤖")
st.subheader("Ask me anything and watch the conversation unfold")

#initialize session state for conversation context
if 'messages' not in st.session_state:
    st.session_state.messages = [] #store chat history

#display chat history dyanmically 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#user input for the chat 
if user_input := st.chat_input("your question ...."):
    #append user input to chat history
    st.session_state.messages.append({"role": "user", "content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
#generate AI response 
with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
        try:
            #pass the conversation context and user input to the chatbot
            context = "\n".join(
                [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]
            )
            result = chain.invoke({"context": context, "question": user_input})
            response = result if isinstance(result, str) else str(result)

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content":response})
        except Exception as e:
            st.error(f"An error occured: {str(e)}")
