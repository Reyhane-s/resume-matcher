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
df = df.reindex(np.random.permutation(df.index))
data = df.copy().iloc[
    0:200,
]
print(data.head())
nlp = spacy.load("en_core_web_lg")
age_pattern_path = "../pattern dataset/age.jsonl"
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(age_pattern_path)
print(nlp.pipe_names)
def get_age(text):
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "AGE":
            subset.append(ent.text)
    myset.append(subset)
    return subset

clean = []
for i in range(data.shape[0]):
    review = re.sub(
        '(@[A-Za-z]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',  # اصلاح الگو برای حفظ اعداد
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
data["age"] = data["Clean_Resume"].str.lower().apply(get_age)
print(data["age"].iloc[1:20])

# Debugging: Check loaded patterns
print(ruler.patterns)  # Ensure patterns are loaded correctly

# Debugging: Test simple text directly
test_text = "I was born in 1990 and I'm 30 years old."
doc = nlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.label_)

for i, resume in enumerate(data["Clean_Resume"].iloc[:20]):  # تست با داده‌های تمیز شده
    print(f"Cleaned Resume {i+1}: {resume}")
    doc = nlp(resume)
    list1 = []
    list3=[]
    filtered_numbers = []
    for ent in doc.ents:

        #print(ent.text, ent.label_)
        if ent.label_ =="DATE":
            list1.append(ent.text)
    print(list1)
    for item in list1:
       list2= item.split(" ")
       list2.sort()
       list3.extend(list2)

       #print(list2)
       #print("#######")
    print(list3)
    for string in list3:
        if string.isdigit():

            number = int(string)
            # بررسی اینکه آیا عدد در محدوده مورد نظر است
            if 1970 <= number <= 2003:
                filtered_numbers.append(number)
    if filtered_numbers:
        min_number = min(filtered_numbers)
        age=2024 - min_number
        print(f"Age is:  {age}")
    else:
        print("NO INFORMATION FOUND IN")

    #print(filtered_numbers)
    print("------")