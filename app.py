# app.py

import gradio as gr
import os
import re
from graph import build_retriever_and_db, answer_question
from retriever_utils import clear_vector_store
from langchain.memory import ConversationBufferMemory

# Global references
retriever = None
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def is_valid_url(url):
    return re.match(r'^https?://[^\s]+$', url) is not None

def start_session(url):
    global retriever, memory
    if not is_valid_url(url):
        return gr.update(visible=False), [], "❌ Invalid URL format."
    
    status = "⏳ Crawling and indexing documents..."
    yield gr.update(visible=False), [], status  # Hide chat during crawl
    
    try:
        retriever = build_retriever_and_db(url)
        memory.clear()  # Reset memory for new session
        status = "✅ Website indexed! You can now ask questions."
        yield gr.update(visible=True), [], status
    except ValueError as e:
        yield gr.update(visible=False), [], f"❌ {e}"

def ask_question(message, chat_history):
    global retriever, memory

    if retriever is None:
        chat_history.append({"role": "assistant", "content": "❌ Please index a website first."})
        return chat_history, ""
    
    chat_history.append({"role": "user", "content": message})
    answer = answer_question(retriever, message, memory)
    chat_history.append({"role": "assistant", "content": answer})
    return chat_history, ""

def reset_session():
    global retriever, memory
    retriever = None
    memory.clear()
    clear_vector_store()
    return "", gr.update(visible=False), [], "🔁 Reset complete."

with gr.Blocks() as demo:
    gr.Markdown("# 🔎 Website QA Chatbot")

    with gr.Row():
        url_input = gr.Textbox(label="Website URL")
        start_button = gr.Button("Start")
        reset_button = gr.Button("Reset")

    status_display = gr.Markdown("ℹ️ Status messages will appear here.")

    chatbot = gr.Chatbot(label="Q&A Chat", visible=False, type='messages')
    question_input = gr.Textbox(label="Ask a question", placeholder="e.g. What services does the company offer?")

    start_button.click(
        fn=start_session,
        inputs=url_input,
        outputs=[chatbot, chatbot, status_display]
    )

    question_input.submit(
        fn=ask_question,
        inputs=[question_input, chatbot],
        outputs=[chatbot, question_input]
    )

    reset_button.click(
        fn=reset_session,
        outputs=[url_input, chatbot, chatbot, status_display]
    )

demo.launch()