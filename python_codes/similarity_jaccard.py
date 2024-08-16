import extract_resume as ex

def jaccard_similarity(list1, list2):
    intersection = len(set(list1).intersection(set(list2)))
    union = len(set(list1).union(set(list2)))
    return intersection / union

# گرفتن ورودی از کاربر
user_input = input("Enter a list of skills (comma separated): ")
user_skills = [skill.strip().lower() for skill in user_input.split(',')]

# محاسبه شباهت و یافتن 5 سطر برتر
similarities = []

for idx, row in ex.data.iterrows():
    similarity = jaccard_similarity(user_skills, row['skills'])
    similarities.append((row.name, similarity))  # ذخیره ایندکس اصلی و شباهت

# مرتب‌سازی براساس درصد شباهت
similarities.sort(key=lambda x: x[1], reverse=True)

# گرفتن 5 سطر برتر
top_5 = similarities[:5]

# نمایش نتایج
print("\nTop 5 matching rows:")
for idx, similarity in top_5:
    common_skills = set(user_skills).intersection(set(ex.data.loc[idx]['skills']))
    print(f"Row index: {idx}, Similarity: {similarity*100:.2f}%")
    print(f"Common skills: {list(common_skills)}")
    print(ex.data.loc[idx].to_dict())
    print()