# graph.py
import os
import re
from scraper_utils import scrape_url_with_playwright
from retriever_utils import build_retriever_from_markdown
from index_utils import index_documents
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory


# 🧱 Build retriever and index documents (called once on Start)
def build_retriever_and_db(url: str):
    try:
        print(f"🕷️ Build retriever and db: {url}")
        domain = re.sub(r'https?://|www\.', '', url).split('/')[0]
        md_path = f"scraped_data/{domain}.md"
        os.makedirs("scraped_data", exist_ok=True)

        # 📥 Scrape and save markdown
        markdown = scrape_url_with_playwright(url, output_file=md_path)
        print(f"✅ Scraped content saved to: {md_path}")

        if not markdown.strip():
            raise ValueError("Scraped content is empty. Please check the URL.")

        # 🧠 Build retriever from markdown
        retriever = build_retriever_from_markdown(markdown, output_path=md_path)

        # Optional: Only needed if you still use index_documents() on ./data/
        # index_documents()

        return retriever

    except Exception as e:
        print(f"❌ Error during crawl/index: {e}")
        raise ValueError(f"Failed to process the URL: {str(e)}")


# 🤖 Answer a user question using RAG
def answer_question(retriever, question: str, memory=None) -> str:
    llm = ChatOpenAI()

    if memory is None:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False
    )

    result = qa.invoke({"question": question})
    return result.get("answer", "❓ No answer found.")