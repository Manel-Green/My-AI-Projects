import streamlit as st
import os
from dotenv import load_dotenv
from dotenv import find_dotenv
load_dotenv(find_dotenv())
from agent import graph
from langchain_core.messages import AIMessage
import asyncio

st.set_page_config(page_title="Sprinter Warranty Checker")

st.title ("Sprinter Warranty Agent")
st.markdown ("Enter a vehicle part e.g., Alternator or brakes to check coverage ")

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#user input
if user_input := st.chat_input("Ask about a part..."):
    #add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    #invoke langgraph agent
    with st.chat_message("assistant"):
        #we pass the full history to the graoh
        #inputs = {"messages": [("user", user_input)]}
        placeholder = st.empty()
        

        async def run_agent():
            current_text = ""
            async for event in graph.astream_events(
                {"messages": [("user", user_input)]}, version="v2"
            ):
                if event["event"] == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        current_text += content
                        placeholder.markdown(current_text + "|")
            return current_text

        final_response = asyncio.run(run_agent())

        placeholder.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})