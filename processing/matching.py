from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Matcher:
    @staticmethod
    def calculate_similarity(jd_embedding, cv_embedding):
        # Normalize embeddings to unit length
        jd_embedding = jd_embedding / np.linalg.norm(jd_embedding)
        cv_embedding = cv_embedding / np.linalg.norm(cv_embedding)
        
        # Calculate cosine similarity
        similarity = cosine_similarity([jd_embedding], [cv_embedding])[0][0]
        
        # Scale to 0-100 range
        return max(0, similarity) * 100  # Ensure score is between 0 and 100

    @staticmethod
    def rank_candidates(jd_data, cvs_data):
        jd_skills = set(jd_data['skills'])
        
        scores = []
        for cv in cvs_data:
            # Calculate skill overlap
            cv_skills = set(cv['skills'])
            skill_overlap = jd_skills.intersection(cv_skills)
            
            # Calculate similarity scores
            similarity = Matcher.calculate_similarity(jd_data['embedding'], cv['embedding'])
            
            score = {
                'name': cv['name'],
                'score': similarity,  # Already scaled to 0-100
                'skills_matched': list(skill_overlap),
                'match_count': len(skill_overlap),
                'experience': cv['experience']
            }
            scores.append(score)
        
        # Sort by both similarity and skill count
        return sorted(scores, 
                     key=lambda x: (x['score'], x['match_count']), 
                     reverse=True)