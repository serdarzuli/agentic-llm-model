import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from src.agents.query_router import route_query
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="🔍 Agentic LLM", layout="wide")

# Başlık alanı
st.markdown("""
    <h1 style='text-align: center;'>🤖 Agentic LLM Assistant</h1>
    <p style='text-align: center; font-size:18px;'>Ask questions, explore documents, and interact with your AI assistant.</p>
    <hr>
""", unsafe_allow_html=True)

add_vertical_space(1)

# Layout: Sol tarafta girişler, sağda cevap
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Configuration")

    query = st.text_area("📝 Ask a Question", height=120)

    provider = st.selectbox("📡 LLM Provider", ["openai", "openrouter"])
    model = st.text_input("📦 Model Name", value="gpt-3.5-turbo" if provider == "openai" else "deepseek/deepseek-r1-0528:free")

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