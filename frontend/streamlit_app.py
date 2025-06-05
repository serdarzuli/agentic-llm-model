import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from src.agents.query_router import route_query
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="🔍 Agentic LLM", layout="wide")

# CSS for full-width layout and white background
st.markdown("""
    <style>
        body, .stApp {
            background-color: white;
            color: #000;
        }
        .centered-title {
            text-align: center;
            font-size: 36px;
            margin-bottom: 0px;
        }
        .subtext {
            text-align: center;
            font-size: 18px;
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# Başlık alanı
st.markdown("""
    <h1 class='centered-title'>🤖 Agentic LLM Assistant</h1>
    <p class='subtext'>Ask questions, upload files, and interact with your AI assistant in real time.</p>
    <hr>
""", unsafe_allow_html=True)

add_vertical_space(1)

# Upload section
uploaded_file = st.file_uploader("📎 Upload a file (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])

# Layout: Ortada başlıklar, soldan sağa kayan içerik
with st.container():
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("📘 Quick Options")
        st.button("🔍 Summarize Uploaded File")
        st.button("💼 Meeting Summary")
        st.button("📄 Report Overview")
        st.button("🧾 Extract Key Points")

        st.subheader("📝 Ask a Question")
        query = st.text_area("Your Question", height=100)

        provider = st.selectbox("📡 LLM Provider", ["openai", "openrouter"])
        model = st.text_input("📦 Model Name", value="gpt-3.5-turbo" if provider == "openai" else "mistralai/mistral-7b-instruct")

        with st.expander("🧠 Prompt Template (Optional)"):
            prompt_template = st.text_area("Prompt format (use {query} and {context})", height=160, value="""
You are a helpful assistant.

Based on the following documents, answer the question:

QUESTION:
{query}

CONTEXT:
{context}

ANSWER:
""")

        run = st.button("🚀 Run Query")

    with col2:
        st.subheader("💬 Response")
        if run:
            if not query.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Processing..."):
                    response = route_query(
                        query=query,
                        prompt_template=prompt_template,
                        provider=provider,
                        model=model
                    )
                st.success("✅ Response Ready!")
                st.markdown(response)

st.markdown("""<hr><p style='text-align:center;font-size:14px;'>Built with 🧠 by Agentic LLM Project</p>""", unsafe_allow_html=True)
