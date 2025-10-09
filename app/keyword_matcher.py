import re
from typing import List, Tuple
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('stopwords')
nltk.download('wordnet')

class KeywordMatcher:
    """
    Hybrid keyword matcher combining:
    1. Exact keyword overlap (general + skill)
    2. Semantic keyword similarity (using spaCy embeddings)
    """

    def __init__(self,
                 weight_skills: float = 0.4,
                 weight_general: float = 0.2,
                 weight_semantic: float = 0.4,
                 semantic_threshold: float = 0.7):
        """
        :param weight_skills: weight given to skill overlap
        :param weight_general: weight given to general word overlap
        :param weight_semantic: weight given to semantic similarity
        :param semantic_threshold: minimum similarity score to count as semantic match
        """
        self.weight_skills = weight_skills
        self.weight_general = weight_general
        self.weight_semantic = weight_semantic
        self.semantic_threshold = semantic_threshold

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.nlp = spacy.load("en_core_web_md")

    # TEXT PROCESSING
    def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        words = [self.lemmatizer.lemmatize(w) for w in text.split() if w not in self.stop_words]
        return " ".join(words)

    def extract_keywords(self, text: str) -> set:
        """
        Extracts keywords (alphanumeric) from text.
        """
        text = text.lower()
        keywords = re.findall(r"[a-zA-Z0-9_#+]+", text)
        return set(keywords)
    
    # EXACT MATCH SCORES
    def compute_overlap_score(self, resume_text: str, job_description: str) -> float:
        """
        Computes normalized keyword overlap score (0–1).
        """
        resume_words = self.extract_keywords(resume_text)
        jd_words = self.extract_keywords(job_description)
        if not jd_words:
            return 0.0
        intersection = resume_words.intersection(jd_words)
        return len(intersection) / len(jd_words)

    def compute_skill_overlap(self, resume_text: str, jd_skills: List[str]) -> float:
        """
        Computes overlap of known skills explicitly (0–1).
        """
        resume_words = self.extract_keywords(resume_text)
        jd_skill_set = set(skill.lower() for skill in jd_skills)
        if not jd_skill_set:
            return 0.0
        intersection = resume_words.intersection(jd_skill_set)
        return len(intersection) / len(jd_skill_set)

    # SEMANTIC MATCH SCORES
    def compute_semantic_score(self, resume_text: str, jd_skills: List[str]) -> float:
        """
        Computes semantic similarity score between resume and skill list (0–1).
        Uses spaCy's word embeddings.
        """
        if not jd_skills:
            return 0.0

        resume_doc = self.nlp(self.preprocess_text(resume_text))
        matches = 0

        for kw in jd_skills:
            kw_doc = self.nlp(kw.lower())
            similarity = resume_doc.similarity(kw_doc)
            if similarity >= self.semantic_threshold:
                matches += 1

        return matches / len(jd_skills)

    # RANKING LOGIC
    def rank_resumes(
        self, resume_texts: List[str], resume_names: List[str],
        job_description: str, jd_skills: List[str]
    ) -> List[Tuple[str, float]]:
        """
        Ranks resumes based on:
        - general overlap
        - skill overlap
        - semantic similarity
        """
        scores = []

        for text, name in zip(resume_texts, resume_names):
            general_score = self.compute_overlap_score(text, job_description)
            skill_score = self.compute_skill_overlap(text, jd_skills)
            semantic_score = self.compute_semantic_score(text, jd_skills)

            final_score = (
                self.weight_general * general_score +
                self.weight_skills * skill_score +
                self.weight_semantic * semantic_score
            )

            scores.append((name, final_score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


def main():
    matcher = KeywordMatcher()

    resumes = [
        "Experienced in Machine Learning, Deep Learning, and Python.",
        "Frontend Developer skilled in React, JavaScript, and Node.js.",
        "Data Scientist with NLP, Flask, and TensorFlow experience."
    ]
    names = ["resume1.pdf", "resume2.pdf", "resume3.pdf"]

    jd = "Looking for a Python developer with experience in machine learning, NLP, and Flask."
    skills = ["Python", "Machine Learning", "Deep Learning", "Flask", "NLP"]

    ranked = matcher.rank_resumes(resumes, names, jd, skills)

    for name, score in ranked:
        print(f"{name}: {round(score, 3)}")

if __name__ == "__main__":
    main()
