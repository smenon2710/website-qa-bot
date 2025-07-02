# index_utils.py

import os
import dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
dotenv.load_dotenv()

def index_documents(directory="./data"):
    """Load markdown files, split into chunks, embed, and store in *in-memory* Chroma."""
    loader = DirectoryLoader(directory, glob="**/*.md")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

    # ❗In-memory Chroma: no persist_directory
    db = Chroma.from_documents(documents=chunks, embedding=embeddings)

    print(f"✅ Indexed {len(chunks)} chunks into Chroma (in-memory).")
    return db

def load_vector_store():
    raise NotImplementedError("In-memory vector store does not support loading from disk.")