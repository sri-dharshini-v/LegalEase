import streamlit as st
import requests
from io import BytesIO
from docx import Document
from fpdf import FPDF

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

document_type = st.selectbox(
    "Document Type",
    ["Agreement", "Contract", "NDA", "Lease", "Employment Offer Letter"]
)

parties = st.text_area(
    "Parties",
    placeholder="Example: ABC Pvt Ltd and John Doe"
)

terms = st.text_area(
    "Key Terms",
    placeholder="Example: Salary: ₹30,000; Duration: 1 year; Notice Period: 30 days"
)

dates = st.text_input(
    "Effective Date",
    placeholder="Example: 01-10-2026"
)

if st.button("Generate Document"):

    data = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/generate",
            json=data
        )

        if response.status_code == 200:
            st.session_state["document"] = response.json()["document"]
            st.success("Document generated successfully!")
        else:
            st.error(f"Backend error: {response.status_code}")

    except Exception as e:
        st.error(f"Could not connect to backend: {e}")


if "document" in st.session_state:

    st.subheader("Document Preview")

    edited_document = st.text_area(
        "Edit Document",
        value=st.session_state["document"],
        height=500
    )

    st.session_state["document"] = edited_document

    st.subheader("Preview")

    st.markdown(
        edited_document.replace("\n", "<br>"),
        unsafe_allow_html=True
    )

    st.subheader("Download")

    document_text = edited_document

    st.download_button(
        "Download TXT",
        data=document_text,
        file_name="legalease_document.txt",
        mime="text/plain"
    )

    docx_buffer = BytesIO()
    doc = Document()