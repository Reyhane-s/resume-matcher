import streamlit as st
import pandas as pd
from spacy import load
from result_test import final_data  # فرض می‌کنیم این فایل حاوی داده‌های رزومه‌ها است

# بارگذاری مدل SpaCy
nlp = load("en_core_web_md")

# تعریف توابع نمره‌دهی
def calculate_skill_similarity(user_skills, resume_skills):
    if not resume_skills:  # اگر لیست مهارت‌ها خالی است
        return 0
    user_skills_doc = nlp(" ".join(user_skills))
    resume_skills_doc = nlp(" ".join(resume_skills))
    return user_skills_doc.similarity(resume_skills_doc)

def calculate_age_score(required_age_range, candidate_age):
    if candidate_age is None:  # اگر سن موجود نیست
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
    candidate_level = degree_levels.get(candidate_degree, 0) if candidate_degree else 0  # مقدار 0 برای مدرک ناشناخته
    return min(1, max(0, candidate_level / required_level))

def calculate_total_score(skill_score, age_score, degree_score, skill_weight=0.85, age_weight=0.05, degree_weight=0.1):
    if age_score == 0:  # اگر سن موجود نیست
        age_weight = 0
    if degree_score == 0:  # اگر مدرک تحصیلی موجود نیست
        degree_weight = 0

    # تنظیم وزن مهارت‌ها باقیمانده وزن‌ها
    remaining_weight = 1 - (age_weight + degree_weight)
    skill_weight = remaining_weight if remaining_weight > 0 else 0.6

    # محاسبه نمره نهایی با وزن‌های تنظیم شده
    return (skill_score * skill_weight) + (age_score * age_weight) + (degree_score * degree_weight)

# بارگذاری داده‌های رزومه
df = pd.DataFrame(final_data)

# اینترفیس Streamlit
st.title("Resume Matcher")

# دریافت ورودی از کاربر
user_skills = st.text_input("Enter required skills (comma separated):", "python, data science").split(",")
user_skills = [skill.strip().lower() for skill in user_skills]  # حذف فضای خالی و تبدیل به حروف کوچک

required_age_range = st.slider("Select required age range:", 18, 65, (25, 45))

required_degree = st.selectbox("Select required degree:", ["high school", "associate", "bachelor", "master", "phd", "postdoc"])

# محاسبه نمرات برای هر سطر
df['skill_score'] = df['Skills'].apply(lambda x: calculate_skill_similarity(user_skills, x))
df['age_score'] = df['Age'].apply(lambda x: calculate_age_score(required_age_range, x))
df['degree_score'] = df['Degree'].apply(lambda x: calculate_degree_score(required_degree, x))

# محاسبه نمره نهایی
df['total_score'] = df.apply(lambda row: calculate_total_score(row['skill_score'], row['age_score'], row['degree_score']), axis=1)

# مرتب‌سازی DataFrame بر اساس ستون 'total_score' به صورت نزولی و انتخاب ۵ ردیف اول
top_5_matches = df.sort_values(by='total_score', ascending=False).head(5)

# نمایش نتایج
st.header("Top 5 Matches")
st.write(top_5_matches[['Skills', 'Age', 'Degree', 'total_score']])
