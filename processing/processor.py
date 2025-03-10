import spacy
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import re
import json
import os

# Load spaCy model and other models
nlp = spacy.load("en_core_web_lg")
kw_model = KeyBERT()
sbert_model = SentenceTransformer('all-mpnet-base-v2')

class TextProcessor:
    def __init__(self):
        # Load the skills list from skills.json (should be a JSON array of skill strings)
        skills_file = os.path.join(os.path.dirname(__file__), "skills.json")
        try:
            with open(skills_file, "r", encoding="utf-8") as f:
                self.skill_list = json.load(f)
            # Removed print debug from UI
        except Exception as e:
            self.skill_list = []
            print("Error loading skills.json:", e)

    def extract_keywords(self, text, top_n=10):
        """Extract top keywords using KeyBERT."""
        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=top_n
        )
        return [kw[0] for kw in keywords]

    def extract_entities(self, text):
        """
        Extract skills and experience details from text.
        For skills, we match only those present in the skills.json list using regex with word boundaries.
        """
        normalized_text = text.lower()
        matched_skills = []
        for skill in self.skill_list:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, normalized_text):
                matched_skills.append(skill)
        # Remove duplicates
        matched_skills = list(set(matched_skills))
        
        # Filter out matches that look like numeric ranges (if any)
        matched_skills = [s for s in matched_skills if not re.fullmatch(r'\[\d+\s*-\s*\d+\]', s)]
        
        # Regex to capture experience details (e.g., "3 years", "5+ years in ...", etc.)
        experience = re.findall(r'(\d+\+?\s*years?[^\n,;.]*)', text, re.IGNORECASE)
        
        return {
            "skills": matched_skills,
            "experience": experience,
            "text": text
        }

    def get_embeddings(self, text):
        """Generate embeddings using Sentence Transformers."""
        return sbert_model.encode(text)
