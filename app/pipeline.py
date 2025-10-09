import os
from app.extract import Extractor
from app.tf_idf_preprocess import SimpleResumePreprocessor as TFIDFPreprocessor
from app.tf_idf_matcher import TFIDFMatcher
from app.bert_preprocess import BertPreprocessor
from app.bert_matcher import BertRanker as BERTMatcher
from app.section_extractor import ResumeSectionExtractorFuzzy
from app.keyword_matcher import KeywordMatcher


class ResumePipeline:
    def __init__(self):
        self.extractor = Extractor()
        self.section_extractor = ResumeSectionExtractorFuzzy(threshold=80)
        self.tfidf_preprocessor = TFIDFPreprocessor()
        self.tfidf_matcher = TFIDFMatcher()
        self.bert_preprocessor = BertPreprocessor()
        self.bert_matcher = BERTMatcher(self.bert_preprocessor)
        self.keyword_matcher = KeywordMatcher()

    # Section extraction helper
    def get_processed_resumes(self, resume_files):
        resume_texts = []
        resume_names = []

        for file in resume_files:
            sections = self.section_extractor.extract_sections_from_file(file)
            important_sections = sections["important_sections"]
            processed = " ".join(important_sections.values())
            resume_texts.append(processed)
            resume_names.append(os.path.basename(file))

        return resume_texts, resume_names

    # TF-IDF Ranking
    def rank_resumes_tfidf(self, resume_files, job_description: str):
        resume_texts, resume_names = self.get_processed_resumes(resume_files)

        jd_processed = self.tfidf_preprocessor.process_text(job_description)
        self.tfidf_matcher.fit(resume_texts, resume_names)
        ranked_results = self.tfidf_matcher.rank_resumes(jd_processed)

        # Scale to 0–1
        if ranked_results and ranked_results[0][1] > 0:
            max_score = ranked_results[0][1]
            ranked_results = [(name, score / max_score) for name, score in ranked_results]

        return ranked_results

    # BERT Ranking
    def rank_resumes_bert(self, resume_files, job_description: str):
        resume_texts, resume_names = self.get_processed_resumes(resume_files)
        bert_results = self.bert_matcher.rank_resumes(job_description, resume_texts)

        name_score_list = []
        for resume_text, score in bert_results:
            idx = resume_texts.index(resume_text)
            name_score_list.append((resume_names[idx], score))

        # Normalize 0–1
        if name_score_list and name_score_list[0][1] > 0:
            max_score = name_score_list[0][1]
            name_score_list = [(name, score / max_score) for name, score in name_score_list]

        return name_score_list

    # Keyword Ranking
    def rank_resumes_keyword(self, resume_files, job_description: str, jd_skills):
        resume_texts, resume_names = self.get_processed_resumes(resume_files)
        ranked_results = self.keyword_matcher.rank_resumes(resume_texts, resume_names, job_description, jd_skills)

        if ranked_results:
            max_score = max(score for _, score in ranked_results)
            if max_score > 0:
                ranked_results = [(name, score / max_score) for name, score in ranked_results]

        return ranked_results

    # Hybrid Ranking (TF-IDF + BERT + Keywords)
    def rank_resumes_hybrid(self, resume_files, job_description: str, jd_skills,
                            weights=(0.4, 0.4, 0.2)):
        """
        Combines TF-IDF, BERT, and Keyword scores using weighted average.
        :param weights: (tfidf_weight, bert_weight, keyword_weight)
        """
        tfidf_results = dict(self.rank_resumes_tfidf(resume_files, job_description))
        bert_results = dict(self.rank_resumes_bert(resume_files, job_description))
        keyword_results = dict(self.rank_resumes_keyword(resume_files, job_description, jd_skills))

        tfidf_w, bert_w, keyword_w = weights
        hybrid_scores = {}

        for file in resume_files:
            name = os.path.basename(file)
            tfidf_score = tfidf_results.get(name, 0)
            bert_score = bert_results.get(name, 0)
            keyword_score = keyword_results.get(name, 0)

            final_score = (
                tfidf_w * tfidf_score +
                bert_w * bert_score +
                keyword_w * keyword_score
            )

            hybrid_scores[name] = final_score

        # Sort descending
        ranked = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked


if __name__ == "__main__":
    sample_resumes = [
        "./data/resumes/A.pdf",
        "./data/resumes/B.pdf",
        "./data/resumes/C.pdf",
        "./data/resumes/D.pdf",
        "./data/resumes/Achal_resume_college.pdf",
    ]

    sample_jd = """
    Looking for a Machine Learning Engineer with strong Python skills,
    experience in NLP, and familiarity with Flask for deploying models.
    """

    jd_skills = ["Python", "Machine Learning", "Deep Learning", "Flask", "NLP"]

    pipeline = ResumePipeline()

    print("=== TF-IDF Ranking ===")
    tfidf_results = pipeline.rank_resumes_tfidf(sample_resumes, sample_jd)
    for name, score in tfidf_results:
        print(f"{name}: {score:.3f}")

    print("\n=== BERT Ranking ===")
    bert_results = pipeline.rank_resumes_bert(sample_resumes, sample_jd)
    for name, score in bert_results:
        print(f"{name}: {score:.3f}")

    print("\n=== Keyword Ranking ===")
    keyword_results = pipeline.rank_resumes_keyword(sample_resumes, sample_jd, jd_skills)
    for name, score in keyword_results:
        print(f"{name}: {score:.3f}")

    print("\n=== HYBRID Ranking (TF-IDF + BERT + Keyword) ===")
    hybrid_results = pipeline.rank_resumes_hybrid(sample_resumes, sample_jd, jd_skills)
    for name, score in hybrid_results:
        print(f"{name}: {score:.3f}")
