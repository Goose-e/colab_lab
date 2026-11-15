from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, stddev, expr, count, desc

spark = SparkSession.builder \
    .appName("Lab3_BatchProcessing") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

DATA_INPUT_PATH = "/content/drive/MyDrive/lab3_data/raw_data.csv"
DATA_OUTPUT_PATH = "/content/drive/MyDrive/lab3_results/"

df = spark.read.csv(DATA_INPUT_PATH, header=True, inferSchema=True)
df = df.dropna().dropDuplicates()

print("Количество строк:", df.count())
print("Количество столбцов:", len(df.columns))

numeric_stats = df.select(
    mean("progress_percent").alias("avg_progress"),
    stddev("progress_percent").alias("std_progress"),
    expr("percentile_approx(progress_percent, 0.5)").alias("median_progress"),
    mean("score").alias("avg_score"),
    stddev("score").alias("std_score"),
    expr("percentile_approx(score, 0.5)").alias("median_score")
)
numeric_stats.show()

top_categories = df.groupBy("category").agg(count("*").alias("students_count")) \
    .orderBy(desc("students_count")).limit(5)
top_categories.show()

numeric_stats.toPandas().to_csv(DATA_OUTPUT_PATH + "numeric_stats.csv", index=False)
top_categories.toPandas().to_csv(DATA_OUTPUT_PATH + "top_categories.csv", index=False)

print("Результаты сохранены")
