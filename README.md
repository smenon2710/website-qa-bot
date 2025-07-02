# 🔎 Website QA Chatbot (RAG)

This project lets you crawl a website, extract its content, and chat with it using RAG (Retrieval-Augmented Generation) via OpenAI and LangChain.

---

## 🚀 Features

- 🔍 Crawls websites using Playwright
- 📄 Converts HTML to Markdown
- 📚 Splits, embeds, and stores documents
- 💬 Gradio chatbot interface to ask questions
- 🧠 Maintains conversation history with memory
- 🧹 Reset and re-crawl support

---

## 🛠️ Requirements

- Python 3.9+
- Node.js 18+
- OpenAI API key (`.env`)

---

## 📦 Install

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js packages
npm install playwright turndown

# (Optional) Install Playwright browser binaries
npx playwright install
```

---

## 🔑 Environment

Create a `.env` file with:

```bash
OPENAI_API_KEY=your_openai_key
```

---

## 🧪 Run

```bash
python app.py
```

Access it at [http://127.0.0.1:7877](http://127.0.0.1:7877)

---

## 📁 Files

| File                 | Purpose                               |
|----------------------|----------------------------------------|
| `app.py`             | Gradio chatbot interface               |
| `graph.py`           | Orchestrates crawling and RAG          |
| `scraper_utils.py`   | Shells out to Playwright to scrape     |
| `run_playwright.js`  | JS crawler using Playwright + Turndown |
| `retriever_utils.py` | Builds vectorstore from markdown       |
| `index_utils.py`     | Optional in-memory vector embedding    |

---

## ⚠️ Notes

- All scraped `.md` files are saved in `scraped_data/` for inspection.
- Vector store is in-memory (no persistent DB).
- Reset button clears previous session and allows new website indexing.

---

## 📄 License

MIT
