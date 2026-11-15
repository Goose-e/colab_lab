import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(9)
random.seed(9)

N = 500000

categories = ["Программирование", "Дизайн", "Маркетинг", "Языки", "Бизнес", "Наука о данных"]
countries = ["Беларусь", "Россия", "Казахстан", "Украина", "Польша", "Германия"]

start_date = datetime(2023, 1, 1)
rows = []
for i in range(N):
    student_id = random.randint(1, 50000)
    course_id = random.randint(1, 500)
    category = random.choice(categories)
    progress_percent = round(np.clip(np.random.normal(60, 30), 0, 100), 1)
    score = round(np.clip(np.random.normal(70, 20), 0, 100), 1)
    country = random.choice(countries)
    enrollment_date = start_date + timedelta(days=random.randint(0, 700))
    rows.append([student_id, course_id, category, progress_percent, score, country, enrollment_date])

df = pd.DataFrame(rows, columns=["student_id", "course_id", "category", "progress_percent", "score", "country", "enrollment_date"])

nan_idx = df.sample(frac=0.03, random_state=9).index
df.loc[nan_idx, "score"] = np.nan

dup_rows = df.sample(frac=0.01, random_state=9)
df = pd.concat([df, dup_rows], ignore_index=True)

df.to_csv("raw_data.csv", index=False)
print("Файл raw_data.csv создан, строк:", len(df))
