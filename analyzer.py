from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer().fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return round(similarity[0][0] * 100, 2)  # percentage
