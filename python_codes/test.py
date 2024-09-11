import pandas as pd
import re
import multiprocessing as mp
import numpy as np
# خواندن فایل xlsx که شامل اسامی فیلدهای آکادمیک است
academic_fields = pd.read_excel('../pattern dataset/academic_fields.xlsx', engine='openpyxl')

# تبدیل فیلدهای آکادمیک به یک set برای جستجوی سریع‌تر
field_names = set(academic_fields['Field Name'].str.lower().tolist())

# خواندن فایل رزومه‌ها (csv)
resumes = pd.read_csv('../resume dataset/Resume.csv')

# ستون مربوط به متن رزومه‌ها
resume_texts = resumes['Resume_str']  # تغییر بر اساس نام ستون در فایل csv

# تابع برای جستجوی فیلدهای آکادمیک در هر رزومه با استفاده از Regular Expressions
def find_academic_fields(text):
    text = text.lower()
    found_fields = {field for field in field_names if re.search(r'\b' + re.escape(field) + r'\b', text)}
    return list(found_fields)

# تابع برای پردازش یک بخش از داده‌ها
def process_chunk(chunk):
    return chunk.apply(find_academic_fields)

# تقسیم داده‌ها به بخش‌های کوچکتر برای پردازش موازی
num_chunks = mp.cpu_count()  # تعداد بخش‌ها بر اساس تعداد هسته‌های پردازنده
chunks = np.array_split(resume_texts, num_chunks)

# پردازش موازی با استفاده از Pool
with mp.Pool(processes=num_chunks) as pool:
    results = pool.map(process_chunk, chunks)

# ترکیب نتایج
flat_results = [item for sublist in results for item in sublist]
resumes['Academic Fields Found'] = pd.Series(flat_results)

# نمایش نتایج
print(resumes[['Resume_str', 'Academic Fields Found']])

# ذخیره نتایج در یک فایل جدید CSV
resumes.to_csv('resumes_with_academic_fields.csv', index=False)
