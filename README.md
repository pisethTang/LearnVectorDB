# LearnVectorDB — RAG with MongoDB Atlas Vector Search

A learning project that implements a **Retrieval-Augmented Generation (RAG)** pipeline using MongoDB Atlas Vector Search, LangChain, and OpenAI. Users can ask natural language questions through a Gradio web UI and receive two outputs: a raw vector search result and an LLM-synthesised answer.

---

## How It Works

1. **Load** — `extract_information.py` reads all `.txt` files from `sample_files/` using LangChain's `DirectoryLoader`.
2. **Embed** — Each document is converted into a vector embedding via `OpenAIEmbeddings` (`text-embedding-ada-002`).
3. **Store** — Embeddings and document content are upserted into a MongoDB Atlas collection (`langchain_demo.collection_of_text_blobs`) and indexed with a Vector Search index named `vector_index`.
4. **Query** — At runtime, the user's question is embedded and a similarity search (`k=1`) retrieves the most relevant document chunk from Atlas.
5. **Generate** — The retrieved chunk is passed through LangChain's `RetrievalQA` chain backed by `gpt-3.5-turbo-instruct`, which synthesises a final natural-language answer.
6. **UI** — A Gradio web interface exposes both outputs (raw vector result + LLM answer) side by side.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Package manager | [uv](https://github.com/astral-sh/uv) |
| Vector database | [MongoDB Atlas Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search) |
| Orchestration | [LangChain](https://docs.langchain.com/) `< 0.1` |
| Embeddings | OpenAI `text-embedding-ada-002` via `langchain.embeddings.openai` |
| LLM | OpenAI `gpt-3.5-turbo-instruct` |
| Document parsing | LangChain `DirectoryLoader` + `unstructured` |
| Web UI | [Gradio](https://www.gradio.app/) |
| MongoDB driver | `pymongo` |

---

## Project Structure

```
LearnVectorDB/
├── extract_information.py   # Main RAG pipeline: load → embed → store → query → serve UI
├── load_data.py             # (placeholder) for data loading utilities
├── key_param.py             # API keys and connection strings (do NOT commit secrets)
├── main.py                  # Entry point stub
├── pyproject.toml           # Project metadata and dependencies
└── sample_files/            # Source documents used for vector indexing
    ├── aerodynamics.txt         # Technical text about aerodynamics and boundary layer control
    ├── chat_conversation.txt    # Conversation between Alfred and Bruce about MongoDB
    └── log_example.txt          # Sample MongoDB/MONGOT log entries
```

---

## Setup

### 1. Install dependencies
```bash
uv sync
```

### 2. Configure credentials
Edit `key_param.py` and set your own values:
```python
OPENAI_API_KEY = "sk-..."
MONGO_URI = "mongodb+srv://<user>:<password>@<cluster>.mongodb.net/..."
```
> **Warning:** Never commit real API keys to version control. Consider using a `.env` file with `python-dotenv` instead.

### 3. Create a Vector Search index in MongoDB Atlas
In your Atlas cluster, create a Vector Search index on `langchain_demo.collection_of_text_blobs` with the name `vector_index`. Use the following index definition:
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}
```

### 4. Run the app
```bash
uv run python extract_information.py
```
This loads and embeds the sample documents, then launches the Gradio interface. A public shareable link is printed to the terminal.

---

## Sample Files

The three documents in `sample_files/` are intentionally from **different domains** to demonstrate that vector search can retrieve the correct source regardless of topic:

- **aerodynamics.txt** — Scientific text about boundary layer control, laminar/turbulent flow, winglets, and lift-to-drag ratios.
- **chat_conversation.txt** — A dialogue between Alfred and Bruce covering MongoDB compression algorithms (Snappy, zlib, zstd).
- **log_example.txt** — Realistic MongoDB server log lines including MONGOT index builds, vector search queries, replication events, and WiredTiger storage messages.

---

## References
1. [LangChain Documentation](https://reference.langchain.com/python/langchain/langchain)
2. [LangChain Docs](https://docs.langchain.com/)
3. [Chat with the LangChain Docs](https://chat.langchain.com/?threadId=7bdaae88-47e1-440a-a5d0-9808c1576cd8)
4. YouTube tutorial: [Vector Search RAG Tutorial – Combine Your Data with LLMs](https://www.youtube.com/watch?v=JEBDfGqrAUA&t=471s)
