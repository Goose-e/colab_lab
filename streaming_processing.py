from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, desc
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType

KAFKA_BOOTSTRAP_SERVERS = "kafka-3b640a91-kolosovich19-3d1c.b.aivencloud.com:13375"
KAFKA_TOPIC = "students-progress-topic"

TRUSTSTORE_PATH = "/content/kafka.truststore.jks"
KEYSTORE_PATH = "/content/kafka.keystore.p12"
KEYSTORE_PASSWORD = "changeit"

spark = SparkSession.builder \
    .appName("Lab3_StreamProcessing") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("student_id", IntegerType(), True),
    StructField("course_id", IntegerType(), True),
    StructField("category", StringType(), True),
    StructField("progress_percent", DoubleType(), True),
    StructField("score", DoubleType(), True),
    StructField("country", StringType(), True),
    StructField("enrollment_date", StringType(), True),
])

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("kafka.security.protocol", "SSL") \
    .option("kafka.ssl.endpoint.identification.algorithm", "") \
    .option("kafka.ssl.truststore.location", TRUSTSTORE_PATH) \
    .option("kafka.ssl.truststore.password", KEYSTORE_PASSWORD) \
    .option("kafka.ssl.truststore.type", "JKS") \
    .option("kafka.ssl.keystore.location", KEYSTORE_PATH) \
    .option("kafka.ssl.keystore.password", KEYSTORE_PASSWORD) \
    .option("kafka.ssl.keystore.type", "PKCS12") \
    .option("kafka.ssl.key.password", KEYSTORE_PASSWORD) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

streaming_stats = parsed_df.groupBy("category").count().orderBy(desc("count"))

query = streaming_stats.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="5 seconds") \
    .start()

print("Ожидание данных из Kafka...")
query.awaitTermination(timeout=60)
query.stop()
print("Потоковая обработка завершена")
