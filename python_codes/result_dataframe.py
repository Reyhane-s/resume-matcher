import pandas as pd
import numpy as np
# ایمپورت کردن توابع از فایل‌های مختلف
from extract_skills import get_skills
from extract_skills import skills

from extract_age import extract_age
from extract_degree import get_degree
df = pd.read_csv("../resume dataset/Resume.csv")
#df = df.reindex(np.random.permutation(df.index))
data = df.copy().iloc[
    0:200,
]
# فرض می‌کنیم دیتافریم اصلی data از قبل موجود است و شامل ستون ID است
#data = pd.DataFrame({
 #   'ID': [1, 2, 3],  # نمونه آیدی‌ها
 #   'Resume_str': [
 #       "Born in 1990, with over 10 years of experience...",
 #       "Experienced professional born in 1985...",
 #       "Recent graduate, age 25 with a BSc degree...",
        # رزومه‌های دیگر
 #   ]
#})



# اجرای توابع و دریافت نتایج
skills1 = skills # فرض کنیم که این تابع یک لیست از مهارت‌ها را برمی‌گرداند
#ages = extract_age(data)  # فرض کنیم که این تابع یک لیست از سن‌ها را برمی‌گرداند
#degrees = get_degree(data)  # فرض کنیم که این تابع یک لیست از مدارک تحصیلی را برمی‌گرداند

# ساختن دیتافریم نهایی
final_data = pd.DataFrame({
    'ID-Person': data['ID'],  # استفاده از ستون ID موجود در data
    'Skills': skills1,         # نتایج استخراج شده از فایل extract_skills.py
    #'Age': ages,              # نتایج استخراج شده از فایل extract_age.py
    #'Degree': degrees         # نتایج استخراج شده از فایل extract_degree.py
})

# نمایش یا ذخیره‌سازی دیتافریم نهایی
print(final_data)
