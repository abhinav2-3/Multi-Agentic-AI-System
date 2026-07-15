import streamlit as st
from langchain_core.messages import HumanMessage
from main import workflow  # import your compiled graph

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 AI Assistant")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "user-1"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# Render past messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = workflow.invoke(
                {
                    "input": user_input,
                    "messages": [HumanMessage(content=user_input)],
                },
                config=config,
            )
            response = result["final_response"]
            st.markdown(response)

    st.session_state.chat_history.append({"role": "assistant", "content": response})
