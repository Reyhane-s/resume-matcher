import sys
import os

# اضافه کردن مسیر پروژه به مسیرهای Python
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_codes.extract_skills import get_skills
from python_codes.extract_age import extract_numbers,extract_age
from python_codes.extract_degree import get_degree,unique_degrees,get_highest_degree
import pandas as pd

import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#nltk.download(['stopwords','wordnet'])

#warning
import warnings
warnings.filterwarnings('ignore')
# مسیر پایه پروژه
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# استفاده از مسیر مطلق برای فایل CSV
csv_file_path = os.path.join(BASE_DIR,"..", 'resume dataset', 'Resume.csv')
df = pd.read_csv(csv_file_path)


data = df.copy().iloc[
    0:500,
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
    'Age': ages,              # نتایج استخراج شده از فایل extract_age1.py
    'Degree': degrees,        # نتایج استخراج شده از فایل extract_degree.py
    'Resume_str': data['Resume_str']
})
# ذخیره final_data به عنوان فایل CSV در پوشه result dataset
csv_save_path = os.path.join(BASE_DIR, '..', 'resume dataset', 'final_data.csv')
final_data.to_csv(csv_save_path, index=False)

#print(type(final_data['ID-Person']))
#print(type(final_data['Skills']))
#print(type(final_data['Age']))
#print(type(final_data['Degree']))
#print(type(final_data['Resume_str']))