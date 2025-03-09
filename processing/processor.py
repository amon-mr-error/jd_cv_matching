import spacy
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import re

nlp = spacy.load("en_core_web_lg")
kw_model = KeyBERT()
sbert_model = SentenceTransformer('all-mpnet-base-v2')

class TextProcessor:
    def __init__(self):
        pass

    def extract_keywords(self, text, top_n=10):
        """Extract top keywords using KeyBERT."""
        keywords = kw_model.extract_keywords(
            text, 
            keyphrase_ngram_range=(1, 2),  # Unigrams and bigrams
            stop_words='english', 
            top_n=top_n
        )
        return [kw[0] for kw in keywords]  # Return just the keywords

    def extract_entities(self, text):
        """Extract entities and keywords dynamically."""
        doc = nlp(text)
        
        # Extract entities using spaCy
        entities = {
            "ORG": [],  # Organizations
            "TECH": [],  # Technologies/Tools
            "ROLE": []   # Job roles
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        # Extract keywords
        keywords = self.extract_keywords(text)
        
        return {
            "skills": list(set(entities["TECH"] + keywords)),  # Combine tech and keywords
            "experience": re.findall(r'(\d+\+? years?.*?)(?=\s\w+|\n)', text),
            "text": text
        }

    def get_embeddings(self, text):
        """Generate embeddings using Sentence Transformers."""
        return sbert_model.encode(text)