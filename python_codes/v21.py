import spacy
from spacy.pipeline import EntityRuler
from spacy.lang.en import English
from spacy.tokens import Doc

# Gensim
import gensim
from gensim import corpora

# Visualization
from spacy import displacy
import pyLDAvis.gensim_models
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt

# Data loading/ Data manipulation
import pandas as pd
import numpy as np
import jsonlines

# NLTK
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download(['stopwords', 'wordnet'])

# Warning
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv("../resume dataset/Resume.csv")
df = df.reindex(np.random.permutation(df.index))
data = df.copy().iloc[0:200]
print(data.head())

# Load the spaCy model
nlp = spacy.load("en_core_web_lg")

# Define and add EntityRuler for skills
skill_pattern_path = "../pattern dataset/jz_skill_patterns.jsonl"
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(skill_pattern_path)

# Define and add EntityRuler for education and age
education_and_age_pattern_path = "../pattern dataset/education_and_age_patterns.jsonl"
ruler = nlp.add_pipe("entity_ruler", after="ner")
ruler.from_disk(education_and_age_pattern_path)

print(nlp.pipe_names)

def get_skills(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return list(set(skills))

def get_education(text):
    doc = nlp(text)
    education = [ent.text for ent in doc.ents if ent.label_ == "EDUCATION"]
    return list(set(education))

def get_age(text):
    doc = nlp(text)
    age = [ent.text for ent in doc.ents if ent.label_ == "AGE"]
    return list(set(age))

def preprocess_text(text):
    review = re.sub(
        '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',
        " ",
        text
    )
    review = review.lower()
    review = review.split()
    lm = WordNetLemmatizer()
    review = [
        lm.lemmatize(word)
        for word in review
        if not word in set(stopwords.words("english"))
    ]
    return " ".join(review)

# Apply text preprocessing
data["Clean_Resume"] = data["Resume_str"].apply(preprocess_text)

# Extract skills, education, and age
data["skills"] = data["Clean_Resume"].apply(get_skills)
data["education"] = data["Clean_Resume"].apply(get_education)
data["age"] = data["Clean_Resume"].apply(get_age)

# Print results for verification
print(data[['skills', 'education', 'age']].head())

# Save to a new CSV file
data.to_csv("../resume dataset/Resume_with_Extraction.csv", index=False)
