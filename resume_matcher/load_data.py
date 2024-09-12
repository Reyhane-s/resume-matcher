import pandas as pd
import sys
import os

# اضافه کردن مسیر پروژه به مسیرهای Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from backend.database import SessionLocal, Resume, init_db
from python_codes.result_test import final_data  # این خط ممکن است نیاز به تنظیم داشته باشد

# تابع برای بارگذاری داده‌ها به پایگاه داده
def load_data_to_db(data):
    # ایجاد یک جلسه برای پایگاه داده
    db: Session = SessionLocal()

    try:
        # پیمایش روی داده‌ها و اضافه کردن به پایگاه داده
        for item in data:
            resume = Resume(
                skills=", ".join(item.get("Skills", [])),  # تبدیل لیست مهارت‌ها به رشته
                age=item.get("Age"),
                degree=item.get("Degree")
            )
            db.add(resume)

        # ذخیره تغییرات
        db.commit()
    except Exception as e:
        print("Error loading data to the database:", e)
        db.rollback()
    finally:
        # بستن جلسه پایگاه داده
        db.close()

# فراخوانی تابع برای بارگذاری داده‌ها
if __name__ == "__main__":
    # اطمینان از این که جداول پایگاه داده ایجاد شده‌اند
    init_db()
    # بارگذاری داده‌ها از دیتاست
    load_data_to_db(final_data)
    print("Data loaded successfully.")
