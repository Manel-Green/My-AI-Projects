import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools.retriever import create_retriever_tool

def get_retriever_tool():
    """ loads the local FAISS vector database and wraps it into a Langchain tool that the agent can use to search the pdf"""

    #define the directory where the database is stored
    DB_PATH = "vector_store"

    #setup embeddings
    embeddings = OpenAIEmbeddings()

    #load the FAISS index from the local folder
    # we set allow_dangerous_deserialization = TRUE because we created this fileourselves
    vector_store = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization= True
    )

    #create the retriever object
    # k=3 tells the agent to grab the 3 most relevant snippets from the pdf
    retriever = vector_store.as_retriever(search_kwargs= {"k": 3})

    # wrap the retriever in a tool
    # The description is very important: it tells the LLM when to use this tool

    tool = create_retriever_tool(
        retriever,
        "search_sprinter_warranty",
        "searches the sprinter warranty manual. Use this for any question regarding vehicle parts, coverage or warranty terms"
    )

    return tool

