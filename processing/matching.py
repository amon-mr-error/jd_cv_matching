from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Matcher:
    @staticmethod
    def calculate_similarity(jd_embedding, cv_embedding):
        # Normalize embeddings to unit length
        jd_embedding = jd_embedding / np.linalg.norm(jd_embedding)
        cv_embedding = cv_embedding / np.linalg.norm(cv_embedding)
        
        # Calculate cosine similarity and scale it to 0-100
        similarity = cosine_similarity([jd_embedding], [cv_embedding])[0][0]
        return max(0, similarity) * 100

    @staticmethod
    def rank_candidates(jd_data, cvs_data):
        # Use the skills extracted from the JD as the reference set.
        jd_skills = set(jd_data['skills'])
        
        # Calculate importance for JD skills: frequency counts in JD text.
        jd_text_lower = jd_data['text'].lower()
        jd_skill_importance = {}
        for skill in jd_skills:
            count = jd_text_lower.count(skill.lower())
            jd_skill_importance[skill] = count
        
        # Maximum possible importance is the sum of frequencies for all JD skills.
        total_jd_importance = sum(jd_skill_importance.values())
        
        # Set weighting factors: alpha for similarity and (1 - alpha) for skill importance.
        # alpha can be tuned based on your desired influence.
        alpha = 0.85
        
        scores = []
        for cv in cvs_data:
            cv_skills = set(cv['skills'])
            # Only include skills that are present in both JD and CV.
            skill_overlap = jd_skills.intersection(cv_skills)
            
            # Sum the importance (frequency) for the overlapping skills.
            importance_sum = sum(jd_skill_importance.get(skill, 0) for skill in skill_overlap)
            
            # Normalize the importance: if total_jd_importance is 0, use 0; else convert to a percentage.
            if total_jd_importance > 0:
                importance_percentage = (importance_sum / total_jd_importance) * 100
            else:
                importance_percentage = 0
            
            similarity = Matcher.calculate_similarity(jd_data['embedding'], cv['embedding'])
            # Compute final score as a weighted average.
            final_score = alpha * similarity + (1 - alpha) * importance_percentage
            
            score = {
                'name': cv['name'],
                'score': similarity,  # raw similarity score (for debugging if needed)
                'skills_matched': list(skill_overlap),
                'match_count': len(skill_overlap),
                'experience': cv['experience'],
                'final_score': final_score
            }
            scores.append(score)
        
        # Sort candidates based on final score (higher is better)
        return sorted(scores, key=lambda x: x['final_score'], reverse=True)
    
def adjust_score(score: float) -> float:
    """
    Placeholder for bias mitigation logic.
    """
    return score
