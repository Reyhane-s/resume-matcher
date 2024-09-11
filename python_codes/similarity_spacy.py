import extract_skills as ex


# تابع برای محاسبه شباهت دو لیست از کلمات
def calculate_similarity(skills1, skills2,threshold=0.7):
    doc1 = ex.nlp(" ".join(skills1))
    doc2 = ex.nlp(" ".join(skills2))
    similarity=doc1.similarity(doc2)
    common_skills = []
    for token1 in doc1:
        for token2 in doc2:
            if token1.similarity(token2) > threshold:
                common_skills.append(token1.text)
                break

    return similarity, common_skills


# گرفتن ورودی از کاربر
user_input = input("Enter a list of skills (comma separated): ")
user_skills = [skill.strip().lower() for skill in user_input.split(',')]

# محاسبه شباهت و یافتن 5 سطر برتر
similarities = []

for idx, row in ex.data.iterrows():
    similarity,common_skills = calculate_similarity(user_skills, row['skills'])
    similarities.append((row.name, similarity,common_skills))  # ذخیره ایندکس اصلی و شباهت

# مرتب‌سازی براساس درصد شباهت
similarities.sort(key=lambda x: x[1], reverse=True)

# گرفتن 5 سطر برتر
top_5 = similarities[:5]

# نمایش نتایج
print("\nTop 5 matching rows:")
for idx, similarity, common_skills in top_5:
    print(f"Row index: {idx}, Similarity: {similarity:.2f}%")
    print(f"Common skills: {list(common_skills)}")
    print(ex.data.loc[idx].to_dict())
    print()