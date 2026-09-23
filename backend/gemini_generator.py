import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


class GeminiDocumentGenerator:

    def generate_document(self, document_type, parties, terms, dates):

        prompt = f"""
Create a professional legal document.

Document Type: {document_type}
Parties: {parties}
Key Terms: {terms}
Dates: {dates}

Generate a clear, structured legal document with:
1. Title
2. Parties
3. Effective Date
4. Main Terms and Conditions
5. Responsibilities
6. Signatures section

Use professional and easy-to-understand legal language.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text