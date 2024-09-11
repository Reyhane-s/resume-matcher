import pandas as pd
import re
from datetime import datetime


# تابع برای تبدیل سال تولد به سن
def convert_birth_year_to_age(birth_year):
    current_year = datetime.now().year
    return current_year - birth_year


# تابع برای استخراج سن از متن رزومه
def extract_age_from_resume(resume_text):
    # جستجو برای اعداد با استفاده از Regular Expressions
    numbers = re.findall(r'\b\d{1,4}\b', resume_text)  # جستجوی اعداد 1 تا 4 رقمی

    # فیلتر کردن اعداد براساس متن اطراف آن برای شناسایی سن یا سال تولد
    for num in numbers:
        num = int(num)

        # فرض کنیم سن افراد بین 15 تا 80 سال باشد
        if 15 <= num <= 80:
            return num

        # فرض کنیم سال تولد در بازه 1940 تا سال جاری باشد
        current_year = datetime.now().year
        if 1940 <= num <= current_year:
            age = convert_birth_year_to_age(num)
            if 15 <= age <= 80:  # بررسی کنیم که سن معتبر باشد
                return age

    # اگر هیچ سن یا سال تولدی یافت نشد
    return None


# نمونه DataFrame
data = {
    'Resume_str': [
        "من محمد هستم و 30 سال دارم. من در زمینه برنامه‌نویسی تجربه دارم.",
        "من در سال 1990 به دنیا آمده‌ام و سابقه کار در حوزه مدیریت دارم.",
        "رزومه من شامل 20 سال تجربه کار در صنعت IT است. من متولد 1985 هستم.",
        "من 40 سالمه و متخصص در داده کاوی هستم."
    ]
}

df = pd.DataFrame(data)

# اعمال تابع استخراج سن بر روی هر رزومه
df['Extracted_Age'] = df['Resume_str'].apply(extract_age_from_resume)

# نمایش نتایج
print(df['Extracted_Age'])
