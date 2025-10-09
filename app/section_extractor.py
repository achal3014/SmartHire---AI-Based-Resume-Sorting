from typing import Dict
from rapidfuzz import fuzz, process
from app.extract import Extractor
import re

class ResumeSectionExtractorFuzzy:
    SECTION_HEADERS_MAPPING = {
        # Projects / Achievements
        "projects": "projects",
        "personal projects": "projects",
        "academic projects": "projects",
        "major projects": "projects",
        "notable projects": "projects",
        "achievements": "projects",
        "awards & achievements": "projects",
        "recognitions": "projects",

        # Certifications / Training
        "certifications": "certifications",
        "professional certifications": "certifications",
        "courses & certifications": "certifications",
        "training": "certifications",

        # Publications
        "publications": "publications",
        "research publications": "publications",
        "papers": "publications",
        "articles": "publications",

        # Hobbies / Interests
        "hobbies": "hobbies",
        "interests": "hobbies",
        "personal interests": "hobbies",
        "extracurricular activities": "hobbies",
        "extracurriculars": "hobbies",

        # References
        "references": "references",
        "professional references": "references",

        # Summary / Objective
        "summary": "summary",
        "professional summary": "summary",
        "career summary": "summary",
        "objective": "summary",
        "career objective": "summary",
        "profile": "summary",

        # Experience / Work
        "experience": "experience",
        "work experience": "experience",
        "professional experience": "experience",
        "employment history": "experience",
        "relevant experience": "experience",
        "internships": "experience",
        "industry experience": "experience",
        "work history": "experience",
        "research experience": "experience",

        # Education
        "education": "education",
        "academic background": "education",
        "qualifications": "education",
        "educational qualifications": "education",
        "degrees": "education",

        # Skills
        "skills": "skills",
        "technical skills": "skills",
        "key skills": "skills",
        "core competencies": "skills",
        "programming skills": "skills",
    }

    def __init__(self, threshold: int = 80, important_sections=None):
        """
        :param threshold: Minimum fuzzy match score to consider a line as a section header
        :param important_sections: List of canonical section names considered important
        """
        self.threshold = threshold
        self.extractor = Extractor()
        # Default important sections
        self.important_sections = important_sections or ["projects", "certifications", "publications", "skills", "experience"]

    def preprocess_text(self, text: str) -> str:
        """
        Clean text to remove page breaks, multiple newlines, and normalize hyphens.
        """
        text = text.replace("\f", " ")           # remove form feeds (page breaks)
        text = text.replace("\r", " ")           # remove carriage returns
        text = re.sub(r"-\n", "", text)          # join hyphenated words across lines
        text = re.sub(r"\n+", "\n", text)        # normalize multiple newlines
        return text

    def extract_sections_from_file(self, resume_file: str) -> Dict[str, Dict[str, str]]:
        """
        Extract all sections and important sections separately.
        Returns a dict:
        {
            "all_sections": {...},
            "important_sections": {...}
        }
        """
        raw_text = self.extractor.extract_text_from_file(resume_file)
        all_sections = self.extract_sections(raw_text)

        important_sections = {k: v for k, v in all_sections.items() if k in self.important_sections}

        return {
            "all_sections": all_sections,
            "important_sections": important_sections
        }

    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Divide resume text into sections based on fuzzy-matched headers.
        Returns a dictionary: {canonical_section_name: section_text}
        """
        text = self.preprocess_text(text)
        lines = text.splitlines()
        sections = {}
        current_section = "other"
        buffer = []

        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue

            # Fuzzy match against headers
            best_match = process.extractOne(
                line_clean.lower(),
                [h.lower() for h in self.SECTION_HEADERS_MAPPING.keys()],
                scorer=fuzz.ratio
            )

            if best_match and best_match[1] >= self.threshold:
                matched_header = self.SECTION_HEADERS_MAPPING[best_match[0].lower()]

                if buffer:
                    sections[current_section] = " ".join(buffer)
                    buffer = []

                current_section = matched_header
            else:
                buffer.append(line_clean)

        if buffer:
            sections[current_section] = " ".join(buffer)

        return sections


# if __name__ == "__main__":
#     # Path to a resume file
#     resume_file = "./data/resumes/Achal_resume_college.pdf"

#     # Initialize section extractor
#     extractor = ResumeSectionExtractorFuzzy(threshold=80)

#     # Extract sections
#     sections_dict = extractor.extract_sections_from_file(resume_file)

#     # Print all sections
#     print("=== ALL SECTIONS ===\n")
#     for section, content in sections_dict["all_sections"].items():
#         print(f"--- {section.upper()} ---")
#         snippet = content[:300] if len(content) > 300 else content
#         print(snippet + ("..." if len(content) > 300 else ""))
#         print("\n")

#     # Print important sections
#     print("=== IMPORTANT SECTIONS ===\n")
#     for section, content in sections_dict["important_sections"].items():
#         print(f"--- {section.upper()} ---")
#         snippet = content[:300] if len(content) > 300 else content
#         print(snippet + ("..." if len(content) > 300 else ""))
#         print("\n")
