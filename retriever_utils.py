# retriever_utils.py

import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DEFAULT_MARKDOWN_FILE = "data/output.md"

def build_retriever_from_markdown(markdown_text, output_path=DEFAULT_MARKDOWN_FILE):
    print(f"📝 Building retriever from markdown: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)
    except Exception as e:
        raise ValueError(f"❌ Failed to write markdown to disk: {e}")

    if not os.path.exists(output_path):
        raise ValueError(f"❌ Expected markdown not found at: {output_path}")

    try:
        loader = TextLoader(output_path)
        documents = loader.load()
    except Exception as e:
        raise ValueError(f"❌ Failed to load markdown file: {e}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    vectordb = Chroma.from_documents(docs, embeddings)  # In-memory
    return vectordb.as_retriever()

def clear_vector_store():
    if os.path.exists("data"):
        for file in os.listdir("data"):
            if file.endswith(".md"):
                os.remove(os.path.join("data", file))