#spacy
import spacy
#Data loading/ Data manipulation
import pandas as pd
import numpy as np

#nltk
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download(['stopwords','wordnet'])

#warning
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv("../resume dataset/Resume.csv")
#df = df.reindex(np.random.permutation(df.index))
data = df.copy().iloc[
    200:400,
]
print(data.head())
nlp = spacy.load("en_core_web_lg")
#age_pattern_path = "../pattern dataset/age.jsonl"
#ruler = nlp.add_pipe("entity_ruler")
#ruler.from_disk(age_pattern_path)
print(nlp.pipe_names)


clean = []
for i in range(data.shape[0]):
    review = re.sub(
        '(@[A-Za-z]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',  # اصلاح الگو برای حفظ اعداد
        "  ",
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


# Debugging: Check loaded patterns
#print(ruler.patterns)  # Ensure patterns are loaded correctly

# Debugging: Test simple text directly
#test_text = "I was born in 1990 and I'm 30 years old."
#doc = nlp(test_text)
#for ent in doc.ents:
 #   print(ent.text, ent.label_)



def extract_age(resume):
    doc = nlp(resume)
    list1 = []
    list3 = []
    filtered_numbers = []

    # استخراج موجودیت‌های با برچسب DATE
    for ent in doc.ents:
        if ent.label_ == "DATE":
            list1.append(ent.text)

    # پردازش مقادیر استخراج‌شده
    for item in list1:
        list2 = item.split(" ")
        list2.sort()
        list3.extend(list2)

    # فیلتر کردن اعداد مورد نظر
    for string in list3:
        if string.isdigit():
            number = int(string)
            if 1970 <= number <= 2003:
                number = 2024 - number
                filtered_numbers.append(number)
                continue
            if 20 <= number <= 35:
                filtered_numbers.append(number)

    # بازگشت مقدار سن، اگر موجود بود
    if filtered_numbers:
        age = int(max(filtered_numbers))
        return age
    else:
        return None


data['Age'] = data["Clean_Resume"].apply(extract_age)
data['Age'] = data['Age'].fillna(0).astype(int)
print(data['Age'])
count_zero_ages = (data['Age'] == 0).sum()

print(f"تعداد مقادیر 0 در ستون Age: {count_zero_ages}")