import pandas as pd
import spacy

# بارگذاری مدل زبان
nlp = spacy.load("en_core_web_lg")

def extract_age(resume):
    doc = nlp(resume)
    list1 = []
    list3 = []
    filtered_numbers = []

    # استخراج موجودیت‌های با برچسب DATE
    for ent in doc.ents:
        if ent.label_ == "DATE":
            list1.append(ent.text)
    print(list1)
    # پردازش مقادیر استخراج‌شده
    for item in list1:
        list2 = item.split(" ")
        list2.sort()
        list3.extend(list2)
        print(list3)
    # فیلتر کردن اعداد مورد نظر
    for string in list3:
        if string.isdigit():
            number = int(string)
            if 1970 <= number <= 2003:
                number = 2024 - number
                filtered_numbers.append(number)
                continue
            if 20 <= number <= 57:
                filtered_numbers.append(number)

    # بازگشت مقدار سن، اگر موجود بود
    if filtered_numbers:
        age = max(filtered_numbers)
        return age
    else:
        return None

# فرض می‌کنیم که دیتافریم data از قبل موجود است
data = pd.DataFrame({
    'Clean_Resume': [
        "Born in 1990, with over 10 years of experience...",
        "40 years old Experienced professional born in 1985...",
        "Recent graduate, age 39, 40 ",
        # افزودن رزومه‌های دیگر
    ]
})

# ایجاد ستون جدید برای مقادیر سن
data['Age'] = data['Clean_Resume'].apply(extract_age)

print(data['Age'])
