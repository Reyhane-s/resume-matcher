def get_highest_degree(degrees):
    # دیکشنری برای نگاشت اشکال مختلف مدارک به یک مقدار ثابت
    degree_aliases = {
        "high school": ["high school", "hs", "secondary school"],
        "associate": ["associate", "as", "aa", "aas"],
        "bachelor": ["bachelor", "bs", "ba", "bsc", "b.a.", "b.s."],
        "master": ["master", "ms", "ma", "msc", "m.a.", "m.s.", "mba", "m.eng", "m.e."],
        "phd": ["phd", "doctorate", "ph.d.", "dphil"],
        "postdoc": ["postdoc", "postdoctoral", "post-doc"]
    }

    # دیکشنری برای سطح‌بندی مدارک تحصیلی
    degree_levels = {
        "high school": 1,
        "associate": 2,
        "bachelor": 3,
        "master": 4,
        "phd": 5,
        "postdoc": 6
    }

    # ایجاد نگاشت معکوس برای تمام معادل‌ها به مقدار ثابت
    degree_map = {}
    for key, aliases in degree_aliases.items():
        for alias in aliases:
            degree_map[alias] = key

    # مقدار اولیه برای بالاترین سطح
    highest_level = 0
    highest_degree = None

    # بررسی مدارک در لیست
    for degree in degrees:
        degree_lower = degree.lower()  # تبدیل به حروف کوچک برای مطابقت
        standardized_degree = degree_map.get(degree_lower)  # معادل‌سازی

        if standardized_degree:
            level = degree_levels[standardized_degree]
            # اگر سطح مدرک از سطح قبلی بیشتر باشد، آن را به عنوان بالاترین سطح ذخیره کن
            if level > highest_level:
                highest_level = level
                highest_degree = standardized_degree

    return highest_degree

# مثال
#degrees_list = ["b.s.", "ms", "high school", "ph.d.", "associate", "m.eng"]
#highest_degree = get_highest_degree(degrees_list)
#print("Highest Degree:", highest_degree)  # خروجی: postdoc
