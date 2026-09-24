import os
import re
from io import BytesIO

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from fpdf import FPDF


def sanitize_text(text: str) -> str:
    """
    Removes special characters and typographic quotes to ensure clean formatting.
    """
    if not text:
        return ""
    replacements = {
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "•": "* ",
        "…": "...",
        "₹": "Rs. ",
        "\u00a0": " ",
        "™": "(TM)",
        "®": "(R)",
        "©": "(C)",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def clean_unicode_for_pdf(text: str) -> str:
    """
    Ensures text is safe for FPDF latin-1 encoding.
    """
    sanitized = sanitize_text(text)
    return sanitized.encode("latin-1", "replace").decode("latin-1")


def format_docx(text: str, doc_type: str) -> bytes:
    """
    Uses python-docx to:
    - Embed logo
    - Add titles, paragraph formatting (Times New Roman font)
    - Auto-generate a Terms table from semicolon-separated or bullet input
    - Include footer at the bottom
    """
    doc = Document()

    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # 1. Embed Logo
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "Image", "Logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(2.5))

    # 2. Document Title
    sanitized_doc_type = sanitize_text(doc_type)
    title = doc.add_heading(sanitized_doc_type, level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)

    doc.add_paragraph()

    lines = [line.strip() for line in sanitize_text(text).split("\n") if line.strip()]

    extracting_terms = False
    term_items = []

    for line in lines:
        # Check if line looks like a header (e.g. ## Header, 1. Title, ALL CAPS header)
        if line.startswith("#") or (line.isupper() and len(line) < 50) or line.endswith(":"):
            clean_line = re.sub(r"^#+\s*", "", line)
            p = doc.add_paragraph()
            run = p.add_run(clean_line)
            run.font.name = "Times New Roman"
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 51, 102)
        elif line.startswith("* ") or line.startswith("- ") or ";" in line:
            # Bullet point or semicolon-separated term
            items = [item.strip().lstrip("*- ") for item in line.split(";") if item.strip()]
            for item in items:
                p = doc.add_paragraph(style="List Bullet" if "List Bullet" in doc.styles else None)
                run = p.add_run(item)
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(line)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

    # 3. Add Terms & Conditions Table if semicolon-separated terms or clauses exist
    raw_terms_matches = [l for l in lines if ";" in l or l.startswith("Terms") or l.startswith("Key Terms")]
    if raw_terms_matches:
        doc.add_paragraph()
        table_title = doc.add_paragraph()
        run_tt = table_title.add_run("Summary of Terms & Conditions")
        run_tt.font.name = "Times New Roman"
        run_tt.font.size = Pt(13)
        run_tt.font.bold = True
        run_tt.font.color.rgb = RGBColor(0, 51, 102)

        terms_list = []
        for line in raw_terms_matches:
            parts = [p.strip().lstrip("*- ") for p in line.split(";") if p.strip()]
            terms_list.extend(parts)

        if terms_list:
            table = doc.add_table(rows=1, cols=2)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = "Clause #"
            hdr_cells[1].text = "Term / Condition Description"

            # Style header row
            shading_elm = parse_xml(r'<w:shd {} w:fill="003366"/>'.format(nsdecls('w')))
            hdr_cells[0]._tc.get_or_add_tcPr().append(shading_elm)
            shading_elm2 = parse_xml(r'<w:shd {} w:fill="003366"/>'.format(nsdecls('w')))
            hdr_cells[1]._tc.get_or_add_tcPr().append(shading_elm2)

            for cell in hdr_cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.color.rgb = RGBColor(255, 255, 255)
                        r.font.bold = True

            for idx, term in enumerate(terms_list, 1):
                row_cells = table.add_row().cells
                row_cells[0].text = f"Clause {idx}"
                row_cells[1].text = term
                for cell in row_cells:
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.name = "Times New Roman"
                            r.font.size = Pt(11)

    # 4. Footer
    footer = doc.sections[0].footer
    footer_para = footer.paragraphs[0]
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run = footer_para.add_run("LegalEase Inc. | contact@legalease.com | All Rights Reserved.")
    f_run.font.name = "Times New Roman"
    f_run.font.size = Pt(9)
    f_run.font.color.rgb = RGBColor(128, 128, 128)

    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output.getvalue()


class BrandedPDF(FPDF):
    """
    Custom FPDF class with logo header and footer on pages.
    """
    def header(self):
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "Image", "Logo.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=75, y=8, w=60)
            self.ln(22)
        else:
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, clean_unicode_for_pdf("LegalEase Inc. | contact@legalease.com | All Rights Reserved."), align="C")


def format_pdf(text: str, doc_type: str) -> bytes:
    """
    Utilizes FPDF with custom header/footer:
    - Center-aligned logo
    - Bold headings for sections
    - Bullet-style terms
    """
    pdf = BrandedPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Document Title
    pdf.set_font("Times", "B", 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, clean_unicode_for_pdf(doc_type), ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Times", size=11)
    pdf.set_text_color(30, 30, 30)

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines:
        cleaned = clean_unicode_for_pdf(line)
        if line.startswith("#") or (line.isupper() and len(line) < 50) or line.endswith(":"):
            pdf.ln(3)
            pdf.set_font("Times", "B", 12)
            pdf.set_text_color(0, 51, 102)
            header_text = re.sub(r"^#+\s*", "", cleaned)
            pdf.multi_cell(0, 7, header_text)
            pdf.set_font("Times", "", 11)
            pdf.set_text_color(30, 30, 30)
        elif line.startswith("* ") or line.startswith("- ") or ";" in line:
            items = [item.strip().lstrip("*- ") for item in line.split(";") if item.strip()]
            for item in items:
                pdf.cell(8, 6, "  *", ln=False)
                pdf.multi_cell(0, 6, clean_unicode_for_pdf(item))
        else:
            pdf.multi_cell(0, 6, cleaned)
            pdf.ln(2)

    out = pdf.output(dest="S")
    if isinstance(out, str):
        return out.encode("latin-1", "replace")
    return bytes(out)


def format_html_preview(text: str) -> str:
    """
    Converts output to stylized HTML blocks for inline display in Streamlit.
    """
    sanitized = sanitize_text(text)
    html_lines = []

    for line in sanitized.split("\n"):
        line_str = line.strip()
        if not line_str:
            continue
        if line_str.startswith("#"):
            clean_h = re.sub(r"^#+\s*", "", line_str)
            html_lines.append(f"<h3 style='color: #6366f1; margin-top: 18px; margin-bottom: 8px;'>{clean_h}</h3>")
        elif line_str.isupper() and len(line_str) < 50:
            html_lines.append(f"<h4 style='color: #818cf8; margin-top: 14px; margin-bottom: 6px;'>{line_str}</h4>")
        elif line_str.startswith("* ") or line_str.startswith("- "):
            clean_b = line_str.lstrip("*- ")
            html_lines.append(f"<li style='margin-left: 20px; margin-bottom: 4px;'>{clean_b}</li>")
        elif ";" in line_str:
            items = [i.strip() for i in line_str.split(";") if i.strip()]
            html_lines.append("<ul>")
            for item in items:
                html_lines.append(f"<li style='margin-left: 20px; margin-bottom: 4px;'>{item}</li>")
            html_lines.append("</ul>")
        else:
            html_lines.append(f"<p style='margin-bottom: 10px;'>{line_str}</p>")

    content_html = "\n".join(html_lines)

    return f"""
    <div style="
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #334155;
        background-color: #1e1e1e;
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-top: 15px;
        margin-bottom: 15px;
        max-height: 500px;
        overflow-y: auto;
    ">
        {content_html}
    </div>
    """
