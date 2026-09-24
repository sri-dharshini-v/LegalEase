import os
import sys
import requests
import streamlit as st

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.document_formatter import format_docx, format_pdf, format_html_preview, sanitize_text
import config

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered"
)

# Header & Logo Display
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    logo_path = config.LOGO_PATH
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center;'>⚖️ LegalEase</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# User Input Interface
document_type = st.text_input(
    "Document Type (Ex: Agreement, Contract, NDA)",
    placeholder="Freelance Work Contract"
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)"
)

terms = st.text_area(
    "Terms & Conditions (Use semicolons for bullet points)",
    placeholder="Work must be delivered by May 15, 2025; Payment will be made within 7 days of invoice; The client retains intellectual property rights; Confidentiality must be maintained at all times"
)

dates = st.text_input(
    "Effective Date",
    placeholder="April 15, 2025"
)

st.markdown("<br>", unsafe_allow_html=True)

# Document Generation
if st.button("Generate Document", type="primary", use_container_width=True):
    if not document_type.strip():
        st.warning("Please enter a document type.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates
        }

        with st.spinner("Generating legal document with Gemini AI..."):
            try:
                backend_url = f"{config.BACKEND_URL}/generate"
                response = requests.post(backend_url, json=payload, timeout=60)

                if response.status_code == 200:
                    raw_text = response.json().get("document", "")
                    clean_doc = sanitize_text(raw_text)
                    st.session_state["generated_text"] = clean_doc
                    st.session_state["doc_type"] = document_type
                    st.session_state["show_edit"] = False
                    st.success("✔ Document Generated Successfully!")
                else:
                    st.error(f"Backend Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend server at {config.BACKEND_URL}. Ensure FastAPI backend is running! Error: {e}")

if "generated_text" not in st.session_state:
    st.info("ℹ️ Click 'Generate Document' to start")

# Render Generated Document & Options
if "generated_text" in st.session_state and st.session_state["generated_text"]:
    doc_text = st.session_state["generated_text"]
    current_doc_type = st.session_state.get("doc_type", "Legal_Document")
    file_stub = current_doc_type.replace(" ", "_").lower()

    st.subheader("Document Preview")
    html_preview = format_html_preview(doc_text)
    st.markdown(html_preview, unsafe_allow_html=True)

    # Edit Document Option
    col_e1, col_e2 = st.columns([1, 3])
    with col_e1:
        if st.button("✏️ Edit Document", use_container_width=True):
            st.session_state["show_edit"] = not st.session_state.get("show_edit", False)

    if st.session_state.get("show_edit", False):
        st.subheader("Edit Document Below:")
        edited_text = st.text_area(
            "Document Content",
            value=doc_text,
            height=350
        )
        st.session_state["generated_text"] = edited_text
        doc_text = edited_text

    st.markdown("---")
    st.subheader("Download Options")

    d_col1, d_col2, d_col3 = st.columns(3)

    with d_col1:
        st.download_button(
            "📄 Download as .TXT",
            data=doc_text,
            file_name=f"{file_stub}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with d_col2:
        try:
            docx_data = format_docx(doc_text, current_doc_type)
            st.download_button(
                "📝 Download as .DOCX",
                data=docx_data,
                file_name=f"{file_stub}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as err:
            st.error(f"DOCX Generation Error: {err}")

    with d_col3:
        try:
            pdf_data = format_pdf(doc_text, current_doc_type)
            st.download_button(
                "📕 Download as .PDF",
                data=pdf_data,
                file_name=f"{file_stub}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as err:
            st.error(f"PDF Generation Error: {err}")