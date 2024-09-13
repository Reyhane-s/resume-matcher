#spacy
import spacy
from spacy.pipeline import EntityRuler
from spacy.lang.en import English
from spacy.tokens import Doc

#gensim
import gensim
from gensim import corpora

#Visualization
from spacy import displacy
import pyLDAvis.gensim_models
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt

#Data loading/ Data manipulation
import pandas as pd
import numpy as np
import jsonlines

#nltk
import re
#import nltk
#from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer
#nltk.download(['stopwords','wordnet'])
import os
#warning
#import warnings
#warnings.filterwarnings('ignore')



#df = pd.read_csv("../resume dataset/Resume.csv")
#df = df.reindex(np.random.permutation(df.index))
#data = df.copy().iloc[
 #   0:200,
#]
#print(data.head())
nlp = spacy.load("en_core_web_lg")
# مسیر پایه پروژه
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# استفاده از مسیر مطلق برای فایل CSV
skill_pattern_path = os.path.join(BASE_DIR,'..', 'pattern dataset', 'jz_skill_patterns.jsonl')
#df = pd.read_csv(csv_file_path)

#skill_pattern_path = "../pattern dataset/jz_skill_patterns.jsonl"
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(skill_pattern_path)
#print(nlp.pipe_names)
def get_skills(text):
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            subset.append(ent.text)
    myset.append(subset)
    return set(subset)


#def unique_skills(x):
  #  return list(set(x))

#clean = []
#for i in range(data.shape[0]):
#    review = re.sub(
#        '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',
 #       " ",
 #       data["Resume_str"].iloc[i],
 #   )
#    review = review.lower()
#    review = review.split()
#    lm = WordNetLemmatizer()
 #   review = [
#        lm.lemmatize(word)
#        for word in review
 #       if not word in set(stopwords.words("english"))
#    ]
#    review = " ".join(review)
 #   clean.append(review)

#data["Clean_Resume"] = clean
#data["skills"] = data["Clean_Resume"].str.lower().apply(get_skills)
#skills= data["Clean_Resume"].str.lower().apply(get_skills)
#data["skills"] = data["skills"].apply(unique_skills)
#print(data.iloc[0])
#print(data["skills"].iloc[0])
#print(data["skills"])