# from PyPDF2 import PdfReader
import docx
import os
import fitz

class Extractor:
    @staticmethod
    def extract_text_from_pdf(path):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text

    @staticmethod
    def extract_text_from_docx(file_path):
        text = ""
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + " "
        return text

    @staticmethod
    def extract_text_from_txt(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text

    @staticmethod
    def extract_text_from_file(file):
        filename = file.filename if hasattr(file, 'filename') else file
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            return Extractor.extract_text_from_pdf(file)
        elif ext == ".docx":
            return Extractor.extract_text_from_docx(file)
        elif ext == ".txt":
            return Extractor.extract_text_from_txt(file)
        else:
            raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    pdf_text = Extractor.extract_text_from_file("data/resumes/Achal_resume_college.pdf")
    # docx_text = extract_text_from_file("data/resumes/sample_resume.docx")
    # txt_text = extract_text_from_file("data/resumes/sample_resume.txt")

    print("PDF:", pdf_text[:1600])
    # print("DOCX:", docx_text[:200])
    # print("TXT:", txt_text[:200])
