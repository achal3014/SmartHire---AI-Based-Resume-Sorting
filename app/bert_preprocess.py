import re
from typing import List
from sentence_transformers import SentenceTransformer
from app.section_extractor import ResumeSectionExtractorFuzzy

class BertPreprocessor:
    def __init__(self, model_name="all-MiniLM-L6-v2", section_threshold=80, important_sections=None):
        self.model = SentenceTransformer(model_name)
        self.section_extractor = ResumeSectionExtractorFuzzy(threshold=section_threshold)
        self.important_sections = important_sections or ["experience", "skills", "projects"]

    # --- Text Cleaning ---
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^a-z0-9\s.,]', '', text)
        return text.strip()

    # --- Section Extraction ---
    def extract_sections_text(self, text: str) -> str:
        sections = self.section_extractor.extract_sections(text)
        # Combine only the important sections
        selected_texts = [sections[s] for s in self.important_sections if s in sections]
        return " ".join(selected_texts)

    # --- Chunking for long resumes ---
    def chunk_text(self, text: str, max_tokens: int = 512) -> List[str]:
        tokens = text.split()
        chunks = []
        for i in range(0, len(tokens), max_tokens - 50):  # leave space for special tokens
            chunk = tokens[i:i+max_tokens-50]
            chunk_text = " ".join(chunk)
            chunks.append(chunk_text)
        return chunks

    # --- Full preprocessing: clean + extract sections + chunk ---
    def preprocess_resume(self, raw_text: str) -> List[str]:
        cleaned = self.clean_text(raw_text)
        section_text = self.extract_sections_text(cleaned)
        chunks = self.chunk_text(section_text)
        return chunks

