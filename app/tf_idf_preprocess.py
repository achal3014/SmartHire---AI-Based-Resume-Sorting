import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from typing import List, Optional

required_corpora = ['stopwords', 'wordnet', 'omw-1.4']
for corpus in required_corpora:
    try:
        nltk.data.find(f'corpora/{corpus}')
    except LookupError:
        nltk.download(corpus)
        print(f"Downloaded NLTK corpus: {corpus}")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

class SimpleResumePreprocessor:  
    def __init__(self):
        self.resume_stopwords = stop_words.union({
            'resume', 'cv', 'curriculum', 'vitae', 'profile', 'summary',
            'objective', 'references', 'available', 'upon', 'request'
        })

    def clean_text(self, text: str) -> str:
        """Perform basic text cleaning"""
        if not isinstance(text, str):
            return ""

        text = text.lower()
        # text = re.sub(r'\S+@\S+', '', text)            # Remove emails
        # text = re.sub(r'[\d\-\(\)\s]{8,}', '', text)  # Remove phone numbers
        text = re.sub(r'https?://\S+', '', text)      # Remove URLs
        text = re.sub(r'[^a-z\s]', '', text)          # Remove special characters
        text = re.sub(r'\s+', ' ', text).strip()      # Remove extra spaces

        return text

    def tokenize_and_lemmatize(self, text: str) -> List[str]:
        tokens = text.split()
        processed_tokens = [
            lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.resume_stopwords and len(token) > 2
        ]
        return processed_tokens

    def process_text(self, text: str) -> Optional[str]:
        try:
            cleaned_text = self.clean_text(text)
            processed_tokens = self.tokenize_and_lemmatize(cleaned_text)
            return ' '.join(processed_tokens)
        except Exception as e:
            print(f"An error occurred during processing: {e}")
            return None

# # Example usage
# if __name__ == "__main__":
#     preprocessor = SimpleResumePreprocessor()
    
#     sample_resume = """
#     John Doe
#     Software Developer
#     Email: john.doe@email.com | Phone: (555) 123-4567 | Portfolio: https://johndoe.com

#     Objective
#     A highly motivated professional with a proven track record of success.

#     Experience
#     Senior Developer | ABC Tech | 2020 - Present
#     - Developed and maintained web applications.

#     Education
#     BS in Computer Science | State University | 2018
#     """
    
#     cleaned_resume = preprocessor.process_text(sample_resume)
    
#     if cleaned_resume:
#         print("Original Text:\n", sample_resume)
#         print("\nProcessed Text (Simplified):\n", cleaned_resume)
