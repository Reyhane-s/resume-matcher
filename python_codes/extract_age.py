import pandas as pd
import re

def extract_numbers(text):
    # استفاده از regex برای استخراج تمام اعداد
    numbers = re.findall(r'\d+', text)
    # تبدیل اعداد استخراج شده به عدد صحیح (int)
    numbers = [int(num) for num in numbers]
    return numbers

def extract_age(resume):
    filtered_numbers=[]
    # فیلتر کردن اعداد مورد نظر
    for string in resume:


        if 1970 <= string <= 2003:
             string = 2024 - string
             filtered_numbers.append(string)
             continue
        if 20 <= string <= 35:
             filtered_numbers.append(string)

    # بازگشت مقدار سن، اگر موجود بود
    if filtered_numbers:
        age = int(max(filtered_numbers))
        return age
    else:
        return None


# فرض می‌کنیم که دیتافریم data از قبل موجود است
#df = pd.read_csv("../resume dataset/Resume.csv")
#df = df.reindex(np.random.permutation(df.index))
#data = df.copy().iloc[
#    200:400,
#]

# استخراج تمام اعداد از رزومه‌ها و ذخیره در ستون جدید
#data['Extracted_Numbers'] = data['Resume_str'].apply(extract_numbers)
#data['Age'] =data['Extracted_Numbers'].apply(extract_age)
#data['Age'] = data['Age'].fillna(0).astype(int)
#print(data['Age'])
#count_zero_ages = (data['Age'] == 0).sum()

#print(f"تعداد مقادیر 0 در ستون Age: {count_zero_ages}")
#print(data['Extracted_Numbers'])
