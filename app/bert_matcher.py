from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from app.bert_preprocess import BertPreprocessor

class BertRanker:
    def __init__(self, preprocessor: BertPreprocessor, model_name="multi-qa-mpnet-base-dot-v1"):
        self.preprocessor = preprocessor
        self.model = SentenceTransformer(model_name)

    def get_jd_embedding(self, text: str):
        return self.model.encode(text, convert_to_tensor=True)

    def get_resume_embedding(self, resume: str):
        chunks = self.preprocessor.chunk_text(resume)
        embeddings = [self.get_jd_embedding(chunk) for chunk in chunks]
        return sum(embeddings) / len(embeddings)

    def rank_resumes(self, job_desc: str, resumes: list):
        job_desc_clean = self.preprocessor.clean_text(job_desc)
        resumes_clean = [self.preprocessor.clean_text(r) for r in resumes]

        jd_embedding = self.get_jd_embedding(job_desc_clean)
        resume_embeddings = [self.get_resume_embedding(r) for r in resumes_clean]

        cosine_scores = [util.pytorch_cos_sim(jd_embedding, emb).item() for emb in resume_embeddings]
        ranked = sorted(zip(resumes, cosine_scores), key=lambda x: x[1], reverse=True)
        return ranked   

if __name__ == "__main__":
    # Initialize preprocessor and BertRanker
    preprocessor = BertPreprocessor()
    bert_ranker = BertRanker(preprocessor)

    # Sample job description
    job_desc = """
    Looking for a Machine Learning Engineer with strong Python skills,
    experience in NLP, and familiarity with Flask for deploying models.
    """

    # Sample resumes (replace with real text or extracted text from files)
    resumes = [
        """Experienced Java developer with 3 years in Spring Boot and Hibernate.
           Worked on microservices and cloud deployment.""",

        """Python developer skilled in Flask, Pandas, Scikit-learn, and TensorFlow.
           2 years experience building ML pipelines and deploying APIs.""",

        """Data scientist with expertise in NLP, BERT, HuggingFace Transformers,
           and model deployment. Strong experience in Python and Flask."""
    ]

    # Rank resumes
    ranked_resumes = bert_ranker.rank_resumes(job_desc, resumes)

    # Print results
    print("=== BERT Ranking ===")
    for i, (resume_text, score) in enumerate(ranked_resumes, start=1):
        print(f"Rank {i}: Score = {score:.4f}\nResume: {resume_text}\n")
