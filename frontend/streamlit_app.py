import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

st.set_page_config(page_title="🔍 Agentic LLM", layout="wide")

from src.agents.query_router import route_query
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
from PIL import Image
from src.tools.image_parser import parse_image_structure
from src.tools.pdf_loader import load_pdf_with_metada #nksiyon adı varsayılmıştır
from src.tools.metadata_enricher import enrich_metadata

upload_file = st.file_uploader("📂 Upload a file", type=["csv", "xlsx", "pdf", "jpg", "jpeg", "png", "bmp"], help="Upload a file to use as a knowledge base.")

extracted_data = None
meta_data = None

if upload_file is not None:
    file_type = upload_file.type
    file_name = upload_file.name
    if file_type == "text/csv":
        df = pd.read_csv(upload_file)
        st.write("CSV Data:")
        st.dataframe(df)
        extracted_data = {"text": df.to_string(), "source_id": file_name, "type": "csv"}
    elif file_type == "application/pdf":
        # PDF dosyası
        pdf_text = load_pdf_with_metada(upload_file)
        st.write("Extracted PDF Text:")
        st.text_area("PDF Content", pdf_text, height=200)
        extracted_data = {"text": pdf_text, "source_id": file_name, "type": "pdf"}
    elif file_type in ["image/jpeg", "image/png", "image/bmp"]:
        # Görsel dosyası
        image = Image.open(upload_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)
        image_result = parse_image_structure(image)
        st.write("Extracted Image Data:")
        st.json(image_result)
        extracted_data = image_result
    else:
        st.write("Unsupported file type. Please upload a CSV, PDF, or image file.")

    # Metadata enrichment
    if extracted_data:
        meta_data = enrich_metadata(extracted_data)
        st.write("Enriched Metadata:")
        st.json(meta_data)

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


    run = st.button("🚀 Run Query")

with col2:
    st.subheader("💬 Response")

    if run:
        if not query.strip():
            st.warning("Please enter a question.")
        elif not meta_data:
            st.warning("Please upload and process a file first.")
        else:
            # Promptu oluştur: metadata ve kullanıcı sorusu ile
                        # ...existing code...
            prompt = f"""
                        Below is the extracted and enriched data from the uploaded file. Use this as context to answer the user's question.
            
            --- CONTEXT ---
            {meta_data['text']}
            
            --- QUESTION ---
            {query}
            
            Answer:
            """  # <-- Closing triple quotes added here
            with st.spinner("Processing..."):
                response = route_query(
                    query=prompt,
                    provider=provider,
                    model=model
                )
            st.success("✅ Response Ready!")
            st.markdown(response)
