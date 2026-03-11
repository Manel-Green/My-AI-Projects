# Mercedes Warranty Agent

This is an Agent, that will tell if the part of the vehicle entered by the user is covered by the warranty or not. It is based on the Service and Warranty Information 2025, published by Mercedes Benz. It is just a simple case, where one agent is using RAG to answer the user's request.  
I used semantic chunks, and LangGraph to have a cyclical agent: it can loop back, correct its own mistakes and gives me a final answer when it thinks it is right.


I executed the following steps:

1. Ingestion phase: here we created the chunks and the vector store
2. Then we turn it into a retriever tool, that allows the agent to reach into the vector store folder and pull out the relevant warranty information
3. Then I build the agent logic in agent.py, using LangGraph
4. in Main we put the streamlit code and connect everything


