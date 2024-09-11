import pandas as pd
import spacy
import re

# خواندن فایل xlsx که شامل اسامی فیلدهای آکادمیک است
academic_fields = pd.read_excel('../pattern dataset/academic_fields.xlsx')

# تبدیل فیلدهای آکادمیک به یک لیست
# تبدیل فیلدهای آکادمیک به یک set برای جستجوی سریع‌تر
field_names = set(academic_fields['Field Name'].str.lower().tolist())# ستون باید بر اساس نام ستون در فایل xlsx تغییر کند

# خواندن فایل رزومه‌ها (csv)
resumes = pd.read_csv('../resume dataset/Resume.csv')

# ستون مربوط به متن رزومه‌ها (بر اساس نام ستون در فایل csv)
resume_texts = resumes['Resume_str']  # تغییر بر اساس نام ستون در فایل csv

# ایجاد یک مدل nlp از SpaCy
#nlp = spacy.load("en_core_web_lg")

# تابع برای جستجوی فیلدهای آکادمیک در هر رزومه
def find_academic_fields(text):
    text = text.lower()
    found_fields = {field for field in field_names if re.search(r'\b' + re.escape(field) + r'\b', text)}
    return list(found_fields)

# اعمال تابع بر روی هر رزومه و ایجاد یک ستون جدید با فیلدهای آکادمیک پیدا شده
resumes['Academic Fields Found'] = resume_texts.apply(find_academic_fields)

# نمایش نتایج
print(resumes[['Resume_str', 'Academic Fields Found']])

# ذخیره نتایج در یک فایل جدید CSV
resumes.to_csv('resumes_with_academic_fields.csv', index=False)
