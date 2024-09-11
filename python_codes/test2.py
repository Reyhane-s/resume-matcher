import pandas as pd
from spacy import load

# بارگذاری مدل Spacy
nlp = load("en_core_web_md")

# تعریف توابع محاسبه نمره
def calculate_skill_similarity(user_skills, resume_skills):
    user_skills_doc = nlp(" ".join(user_skills))
    resume_skills_doc = nlp(" ".join(resume_skills))
    return user_skills_doc.similarity(resume_skills_doc)

def calculate_age_score(required_age_range, candidate_age):
    min_age, max_age = required_age_range
    if min_age <= candidate_age <= max_age:
        return 1
    elif candidate_age < min_age:
        return max(0, 1 - (min_age - candidate_age) / 10)
    else:
        return max(0, 1 - (candidate_age - max_age) / 10)

def calculate_degree_score(required_degree, candidate_degree):
    degree_levels = {"دیپلم": 1, "کاردانی": 2, "کارشناسی": 3, "کارشناسی ارشد": 4, "دکتری": 5}
    required_level = degree_levels.get(required_degree, 0)
    candidate_level = degree_levels.get(candidate_degree, 0)
    return min(1, max(0, candidate_level / required_level))

# تابع محاسبه نمره نهایی
def calculate_total_score(skill_score, age_score, degree_score, skill_weight=0.6, age_weight=0.2, degree_weight=0.2):
    return (skill_score * skill_weight) + (age_score * age_weight) + (degree_score * degree_weight)

# نمونه DataFrame
data = {
    'skills': [['python', 'machine learning'], ['excel', 'management'], ['python', 'data analysis']],
    'age': [30, 40, 25],
    'degree': ['کارشناسی', 'کارشناسی ارشد', 'کارشناسی']
}

df = pd.DataFrame(data)

# ورودی‌های کاربر برای پوزیشن
user_skills = ['python', 'data science']
required_age_range = (25, 35)
required_degree = 'کارشناسی'

# محاسبه نمرات برای هر سطر
df['skill_score'] = df['skills'].apply(lambda x: calculate_skill_similarity(user_skills, x))
df['age_score'] = df['age'].apply(lambda x: calculate_age_score(required_age_range, x))
df['degree_score'] = df['degree'].apply(lambda x: calculate_degree_score(required_degree, x))

# محاسبه نمره نهایی
df['total_score'] = df.apply(lambda row: calculate_total_score(row['skill_score'], row['age_score'], row['degree_score']), axis=1)

# نمایش نتایج
print(df)
