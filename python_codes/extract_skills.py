
import spacy
import os
nlp = spacy.load("en_core_web_lg")
# مسیر پایه پروژه
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# استفاده از مسیر مطلق برای فایل CSV
skill_pattern_path = os.path.join(BASE_DIR,'..', 'pattern dataset', 'jz_skill_patterns.jsonl')

ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(skill_pattern_path)

def get_skills(text):
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            subset.append(ent.text)
    myset.append(subset)
    return set(subset)


