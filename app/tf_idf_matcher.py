from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from app.tf_idf_preprocess import SimpleResumePreprocessor as TFIDFPreprocessor

class TFIDFMatcher:
    def __init__(self):
        # TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        self.tfidf_matrix = None
        self.resume_texts = []
        self.resume_names = []
        self.preprocessor = TFIDFPreprocessor()

    def fit(self, raw_resume_texts: List[str], resume_names: List[str] = None):
        """
        Preprocess raw resume texts, fit TF-IDF, and store names.
        :param raw_resume_texts: list of raw resume texts (extracted by pipeline)
        :param resume_names: optional list of resume filenames
        """
        self.resume_texts = [self.preprocessor.process_text(text) for text in raw_resume_texts]
        self.resume_names = resume_names if resume_names else [f"Resume {i}" for i in range(len(raw_resume_texts))]
        self.tfidf_matrix = self.vectorizer.fit_transform(self.resume_texts)

    def rank_resumes(self, raw_job_description: str, normalize: bool = True):
        """
        Rank resumes based on TF-IDF similarity to job description.
        :param raw_job_description: raw job description text
        :param normalize: whether to scale scores 0-100
        :return: list of tuples [(resume_name, score), ...] sorted descending
        """
        if self.tfidf_matrix is None:
            raise ValueError("You must call fit() with resumes before ranking.")

        jd_processed = self.preprocessor.process_text(raw_job_description)
        jd_vector = self.vectorizer.transform([jd_processed])

        similarities = cosine_similarity(jd_vector, self.tfidf_matrix).flatten()
        ranked_resumes = list(zip(self.resume_names, similarities))
        ranked_resumes.sort(key=lambda x: x[1], reverse=True)

        return ranked_resumes



# if __name__ == "__main__":
#     # Sample resumes (already preprocessed)
#     resumes = [
#         "python django flask aws",
#         "java spring sql aws",
#         "react javascript nodejs"
#     ]
#     resume_names = ["Alice.pdf", "Bob.pdf", "Charlie.pdf"]

#     jd = "Looking for a backend developer with python and aws experience"

#     matcher = TFIDFMatcher()
#     matcher.fit(resumes, resume_names)
#     ranked = matcher.rank_resumes(jd)

#     print("Ranked Resumes:")
#     for name, score in ranked:
#         print(f"{name}: {score:.4f}")
