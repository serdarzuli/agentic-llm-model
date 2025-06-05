# 🤖 Agentic LLM Assistant

Agentic LLM Assistant is a modular, multimodal AI-powered assistant that allows users to query over documents, transcripts, and images using large language models (LLMs). It supports file uploads, real-time responses, customizable prompts, and multiple model providers such as OpenAI and OpenRouter.

## 🚀 Features

- 🔍 Ask questions over 200+ documents (PDF, audio, images, structured data)
- 📎 Upload files and instantly summarize their content
- 🤖 RAG-based architecture with reranking and fallback search
- 📡 Support for OpenAI, Claude, Mistral, and other OpenRouter models
- 🧠 Dynamic prompt template system (frontend-controlled)
- 📄 Metadata-based filtering (e.g., type: meeting, pdf, image)
- 🧾 Built-in quick query options (Meeting Summary, Key Points, etc.)

## 📁 Project Structure

```
AGENTIC-LLM-MODEL/
│
├── .env                        # API keys and config
├── config.yaml                # Optional runtime configuration
├── main.py                    # CLI test interface
├── requirements.txt           # Python dependencies
│
├── frontend/
│   └── streamlit_app.py       # Streamlit-based web frontend
│
└── src/
    ├── agents/                # Routing and synthesis logic
    │   └── query_router.py
    │
    ├── data/                  # Raw and processed data
    │
    ├── models/                # LLM backend handler
    │   └── model_selector.py
    │
    ├── retrievers/            # Embedding + hybrid retrieval
    │   ├── embedding_generator.py
    │   └── hybrid_retriever.py
    │
    ├── tools/                 # File parsers and AI helpers
    │   ├── pdf_loader.py
    │   ├── audio_transcriber.py
    │   ├── image_captioner.py
    │   ├── image_parser.py
    │   └── metadata_enricher.py
    │
    └── utils/                 # File reading utilities
        └── file_reader.py
```

## 🧪 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables
Create a `.env` file:
```env
OPENAI_API_KEY=your-openai-key
OPENROUTER_API_KEY=your-openrouter-key
MODEL_PROVIDER=openai
MODEL_NAME=gpt-3.5-turbo
```

### 3. Launch the web app
```bash
streamlit run frontend/streamlit_app.py
```

## 📌 Future Enhancements

- LangChain agent chaining
- File vectorization upon upload
- Admin panel with history & analytics
- Voice input & output

---
