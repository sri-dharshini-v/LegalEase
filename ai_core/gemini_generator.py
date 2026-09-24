import os
import time
import warnings
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")


class GeminiDocumentGenerator:
    """
    Handles legal document generation using Google Gemini API.
    Uses google.genai Client as primary, falling back to legacy google-generativeai.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables or .env file.")

        self.genai_client = None
        self.genai_legacy = None

        # Try initializing google-genai Client SDK (New recommended SDK)
        try:
            from google import genai as new_genai
            self.genai_client = new_genai.Client(api_key=self.api_key)
        except Exception:
            pass

        # Fallback to legacy google-generativeai SDK if needed
        if not self.genai_client:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.genai_legacy = genai.GenerativeModel(self.model_name)
            except Exception:
                pass

        if not self.genai_client and not self.genai_legacy:
            raise RuntimeError("Failed to initialize Google Gemini SDK.")

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n"
            f"Ensure formal legal structure with multiple sections and legal clauses."
        )

        max_retries = 3
        last_error = None

        models_to_try = [self.model_name]
        if self.model_name != "gemini-1.5-pro":
            models_to_try.append("gemini-1.5-pro")
        if "gemini-3.6-flash" not in models_to_try:
            models_to_try.append("gemini-3.6-flash")

        for model in models_to_try:
            for attempt in range(max_retries):
                try:
                    # Strategy 1: google.genai Client SDK
                    if self.genai_client:
                        response = self.genai_client.models.generate_content(
                            model=model,
                            contents=prompt
                        )
                        if response and hasattr(response, "text") and response.text:
                            return response.text.strip()

                    # Strategy 2: google-generativeai SDK
                    if self.genai_legacy:
                        import google.generativeai as genai
                        model_obj = genai.GenerativeModel(model)
                        response = model_obj.generate_content(prompt)
                        if response and hasattr(response, "text") and response.text:
                            return response.text.strip()

                except Exception as e:
                    last_error = e
                    time.sleep(1)

        if last_error:
            raise RuntimeError(f"Failed to generate document with Gemini API: {str(last_error)}")
        raise RuntimeError("Empty response received from Gemini API.")
