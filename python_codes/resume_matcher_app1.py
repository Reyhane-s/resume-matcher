import streamlit as st
import pandas as pd
from spacy import load
from result_test import final_data

# بارگذاری مدل SpaCy
nlp = load("en_core_web_md")


# تعریف توابع نمره‌دهی
def calculate_skill_similarity(user_skills, resume_skills):
    if not resume_skills:
        return 0
    user_skills_doc = nlp(" ".join(user_skills))
    resume_skills_doc = nlp(" ".join(resume_skills))
    return user_skills_doc.similarity(resume_skills_doc)


def calculate_age_score(required_age_range, candidate_age):
    if candidate_age is None:
        return 0
    min_age, max_age = required_age_range
    if min_age <= candidate_age <= max_age:
        return 1
    elif candidate_age < min_age:
        return max(0, 1 - (min_age - candidate_age) / 10)
    else:
        return max(0, 1 - (candidate_age - max_age) / 10)


def calculate_degree_score(required_degree, candidate_degree):
    degree_levels = {"high school": 1, "associate": 2, "bachelor": 3, "master": 4, "phd": 5, "postdoc": 6}
    required_level = degree_levels.get(required_degree, 0)
    candidate_level = degree_levels.get(candidate_degree, 0) if candidate_degree else 0
    return min(1, max(0, candidate_level / required_level))


def calculate_total_score(skill_score, age_score, degree_score, skill_weight=0.85, age_weight=0.05, degree_weight=0.1):
    if age_score == 0:
        age_weight = 0
    if degree_score == 0:
        degree_weight = 0

    remaining_weight = 1 - (age_weight + degree_weight)
    skill_weight = remaining_weight if remaining_weight > 0 else 0.6

    return (skill_score * skill_weight) + (age_score * age_weight) + (degree_score * degree_weight)


# اینترفیس Streamlit
st.set_page_config(page_title="Resume Matcher", page_icon=":briefcase:", layout="centered")

st.title("🔍 Resume Matcher")
st.markdown("Find the best matches for your job requirements with ease!")

# استفاده از ستون‌ها برای مرتب‌سازی ورودی‌ها
col1, col2 = st.columns(2)

with col1:
    user_skills = st.text_area("🛠️ Enter required skills (comma separated):", "python, data science").split(",")
    user_skills = [skill.strip().lower() for skill in user_skills]

with col2:
    required_age_range = st.slider("🎯 Select required age range:", 18, 65, (25, 45))
    required_degree = st.selectbox("🎓 Select required degree:",
                                   ["high school", "associate", "bachelor", "master", "phd", "postdoc"])

if st.button("🚀 Find Matches"):
    with st.spinner('Matching resumes... Please wait...'):
        df = pd.DataFrame(final_data)
        df['skill_score'] = df['Skills'].apply(lambda x: calculate_skill_similarity(user_skills, x))
        df['age_score'] = df['Age'].apply(lambda x: calculate_age_score(required_age_range, x))
        df['degree_score'] = df['Degree'].apply(lambda x: calculate_degree_score(required_degree, x))
        df['total_score'] = df.apply(
            lambda row: calculate_total_score(row['skill_score'], row['age_score'], row['degree_score']), axis=1)

        top_5_matches = df.sort_values(by='total_score', ascending=False).head(5)

    st.success("✅ Top 5 matches found!")
    st.header("📋 Top 5 Matches")
    st.write(top_5_matches[['Skills', 'Age', 'Degree', 'total_score']])

    # افزودن جزئیات بیشتر
    for index, row in top_5_matches.iterrows():
        st.subheader(f"📝 Resume {index + 1}")
        st.write(f"**Skills:** {', '.join(row['Skills'])}")
        st.write(f"**Age:** {row['Age']}")
        st.write(f"**Degree:** {row['Degree']}")
        st.write(f"**Total Score:** {row['total_score']:.2f}")
        st.markdown("---")
