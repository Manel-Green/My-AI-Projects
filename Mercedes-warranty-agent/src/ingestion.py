from dotenv import load_dotenv
import os 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def ingest_docs():
    #configuration
    PDF_NAME = "sprinter_warranty.pdf"
    RAW_DATA_PATH = os.path.join("data", PDF_NAME)
    STORE_PATH = "vector_store"

    #load the pdf
    print(f"---Loading{PDF_NAME}---")
    loader = PyPDFLoader(RAW_DATA_PATH)
    raw_documents = loader.load()

    #split text into chunks
    print("--Splitting documents into chunks--")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100,
        separators = ["\n\n", "\n", "", " "],
        keep_separator= True
    )
    texts = text_splitter.split_documents(raw_documents)
    print(f"Created {len(texts)} chunks. ")

    #create embeddings and Vector store
    embeddings = OpenAIEmbeddings()

    vector_store = FAISS.from_documents(texts, embeddings)

    #save locally 
    print(f"--Saving database to {STORE_PATH}---")
    vector_store.save_local(STORE_PATH)

    print(" :) Ingestion complete! you can run the streamlit app")

if __name__ == "__main__":
    ingest_docs()
    



