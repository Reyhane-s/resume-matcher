import sys
import os

# اضافه کردن مسیر پروژه به مسیرهای Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
import pandas as pd
from spacy import load
from python_codes.result_test import final_data

# بارگذاری مدل Spacy
nlp = load("en_core_web_md")

app = Flask(__name__)

# تعریف توابع نمره‌دهی (همون‌هایی که نوشتی)
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
    total_weight = skill_weight + age_weight + degree_weight
    if age_score == 0:
        age_weight = 0
    if degree_score == 0:
        degree_weight = 0
    remaining_weight = 1 - (age_weight + degree_weight)
    skill_weight = remaining_weight if remaining_weight > 0 else 0.6
    return (skill_score * skill_weight) + (age_score * age_weight) + (degree_score * degree_weight)

# مسیر اصلی برای نمایش فرم و پردازش نتایج
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # گرفتن ورودی‌ها از فرم
        user_skills = request.form['skills'].split(',')
        min_age = int(request.form['min_age'])
        max_age = int(request.form['max_age'])
        required_degree = request.form['degree']
        required_age_range = (min_age, max_age)

        # محاسبه نمرات برای هر سطر
        df = pd.DataFrame(final_data)
        df['skill_score'] = df['Skills'].apply(lambda x: calculate_skill_similarity(user_skills, x))
        df['age_score'] = df['Age'].apply(lambda x: calculate_age_score(required_age_range, x))
        df['degree_score'] = df['Degree'].apply(lambda x: calculate_degree_score(required_degree, x))

        # محاسبه نمره نهایی
        df['total_score'] = df.apply(lambda row: calculate_total_score(row['skill_score'], row['age_score'], row['degree_score']), axis=1)

        # مرتب‌سازی و انتخاب ۵ مورد برتر
        df_sorted = df.sort_values(by='total_score', ascending=False)
        top_5_matches = df_sorted.head(5)

        # ارسال نتایج به صفحه HTML
        return render_template('results.html', results=top_5_matches.to_dict(orient='records'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
