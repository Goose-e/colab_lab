import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(123)
random.seed(123)

categories = ["Программирование", "Дизайн", "Маркетинг", "Языки", "Бизнес", "Наука о данных"]
countries = ["Беларусь", "Россия", "Казахстан", "Украина", "Польша", "Германия"]
start_date = datetime(2024, 6, 1)

rows = []
for i in range(200):
    student_id = random.randint(1, 50000)
    course_id = random.randint(1, 500)
    category = random.choice(categories)
    progress_percent = round(np.clip(np.random.normal(60, 30), 0, 100), 1)
    score = round(np.clip(np.random.normal(70, 20), 0, 100), 1)
    country = random.choice(countries)
    enrollment_date = start_date + timedelta(days=random.randint(0, 30))
    rows.append([student_id, course_id, category, progress_percent, score, country, enrollment_date])

df = pd.DataFrame(rows, columns=["student_id", "course_id", "category", "progress_percent", "score", "country", "enrollment_date"])
df.to_csv("new_data.csv", index=False)
print("Файл new_data.csv создан")
