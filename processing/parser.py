import PyPDF2
from docx import Document
import re

class FileParser:
    @staticmethod
    def parse_pdf(file):
        text = ""
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    @staticmethod
    def parse_docx(file):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def anonymize_text(text):
        # Remove personal information to mitigate bias
        text = re.sub(r'(?i)\b(name|gender|dob|address)\b:.*?\n', '', text)
        return text