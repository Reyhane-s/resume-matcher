import sys
import os

# اضافه کردن مسیر پروژه به مسیرهای Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from python_codes.result_test import final_data
from flask import Flask, render_template, request
import pandas as pd
from spacy import load


# بارگذاری مدل Spacy
nlp = load("en_core_web_md")

# تعریف توابع نمره‌دهی
def calculate_skill_similarity(user_skills, resume_skills):
    if not resume_skills:
        return 0
    user_skills_doc = nlp(" ".join(user_skills))
    resume_skills_doc = nlp(" ".join(resume_skills))
    return user_skills_doc.similarity(resume_skills_doc)

def calculate_age_score(required_age_range, candidate_age):
    min_age, max_age = required_age_range
    # محدودیت سنی
    min_age = max(min_age, 15)
    max_age = min(max_age, 65)

    if candidate_age is None:
        return 0
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
    total_weight = skill_weight + age_weight + degree_weight

    if age_score == 0:
        age_weight = 0
    if degree_score == 0:
        degree_weight = 0

    remaining_weight = 1 - (age_weight + degree_weight)
    skill_weight = remaining_weight if remaining_weight > 0 else 0.6

    total_score = (skill_score * skill_weight) + (age_score * age_weight) + (degree_score * degree_weight)
    return round(total_score * 100, 2)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # دریافت داده‌های ورودی کاربر
    user_skills = request.form.get('skills').split(',')
    min_age = int(request.form.get('min_age', 15))
    max_age = int(request.form.get('max_age', 65))
    required_age_range = (min_age, max_age)
    required_degree = request.form.get('degree')

    # وزن‌های ورودی از کاربر
    skill_weight = float(request.form.get('skill_weight', 0.85))
    age_weight = float(request.form.get('age_weight', 0.05))
    degree_weight = float(request.form.get('degree_weight', 0.1))

    # بارگذاری داده‌های رزومه‌ها
    df = pd.DataFrame(final_data)

    # محاسبه نمرات
    df['skill_score'] = df['Skills'].apply(lambda x: calculate_skill_similarity(user_skills, x))
    df['age_score'] = df['Age'].apply(lambda x: calculate_age_score(required_age_range, x))
    df['degree_score'] = df['Degree'].apply(lambda x: calculate_degree_score(required_degree, x))

    # محاسبه نمره نهایی
    df['total_score'] = df.apply(lambda row: calculate_total_score(
        row['skill_score'], row['age_score'], row['degree_score'], skill_weight, age_weight, degree_weight), axis=1)

    # مرتب‌سازی بر اساس نمره نهایی
    df_sorted = df.sort_values(by='total_score', ascending=False)

    # انتخاب ۵ ردیف اول
    top_5_matches = df_sorted.head(5)

    # جایگزینی مقادیر گم‌شده با "No Information"
    top_5_matches.fillna("No Information", inplace=True)
    top_5_matches.replace(0, "No Information", inplace=True)

    return render_template('results.html', results=top_5_matches.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
