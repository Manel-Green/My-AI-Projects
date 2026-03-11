from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from src.tools import get_retriever_tool

# 1- define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2- Setup tool & model
tool = get_retriever_tool()
tools = [tool]
llm = ChatOpenAI(model="gpt-4o", temperature=0 )

# 3- define the system prompt

system_prompt = (
    """
    you are a mercedes benz sprinter warranty assistant.
    your goal is to determine if a vehicle is covered under warranty based only on the provided pdf
    always search the documents before answering
    if the part is mentioned, state if it is "covered" or "not covered" and cite the section
    if you can't find the information, say you dont know, do not make up policies

"""
)

#the chatbot node
def chatbot(state: State):
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.bind_tools(tools).invoke(messages)
    return {"messages": [response]}

#build graph
workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

graph = workflow.compile()
