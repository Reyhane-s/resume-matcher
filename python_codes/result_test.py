import sys
import os

# اضافه کردن مسیر پروژه به مسیرهای Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_codes.extract_skills import get_skills
from python_codes.test4 import extract_numbers,extract_age
from python_codes.extract_degree import get_degree,unique_degrees,get_highest_degree
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#nltk.download(['stopwords','wordnet'])

#warning
import warnings
warnings.filterwarnings('ignore')

#data uplouded
df = pd.read_csv("../resume dataset/Resume.csv")
#df = df.reindex(np.random.permutation(df.index))
data = df.copy().iloc[
    0:200,
]
#data cleaned
clean = []
for i in range(data.shape[0]):
    review = re.sub(
        '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',
        " ",
        data["Resume_str"].iloc[i],
    )
    review = review.lower()
    review = review.split()
    lm = WordNetLemmatizer()
    review = [
        lm.lemmatize(word)
        for word in review
        if not word in set(stopwords.words("english"))
    ]
    review = " ".join(review)
    clean.append(review)

data["Clean_Resume"] = clean

skills= data["Clean_Resume"].str.lower().apply(get_skills)

data['Extracted_Numbers'] = data['Resume_str'].apply(extract_numbers)
ages =data['Extracted_Numbers'].apply(extract_age)
ages = ages.fillna(0).astype(int)

degrees = data["Clean_Resume"].str.lower().apply(get_degree)
degrees = degrees.apply(unique_degrees)
degrees = degrees.apply(get_highest_degree)

final_data = pd.DataFrame({
    'ID-Person': data['ID'],  # استفاده از ستون ID موجود در data
    'Skills': skills,         # نتایج استخراج شده از فایل extract_skills.py
    'Age': ages,              # نتایج استخراج شده از فایل extract_age.py
    'Degree': degrees         # نتایج استخراج شده از فایل extract_degree.py
})

# نمایش یا ذخیره‌سازی دیتافریم نهایی
#print(final_data['ID-Person'])
#print(final_data['Skills'])
#print(final_data['Age'])
#print(final_data['Degree'])
