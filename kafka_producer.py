from kafka import KafkaProducer
import pandas as pd
import json
import time


KAFKA_BOOTSTRAP_SERVERS = "kafka-3b640a91-kolosovich19-3d1c.b.aivencloud.com:13375"
KAFKA_TOPIC = "students-progress-topic"

SSL_CA_LOCATION = "/content/ca.pem"
SSL_CERT_LOCATION = "/content/service.cert"
SSL_KEY_LOCATION = "/content/service.key"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    security_protocol="SSL",
    ssl_cafile=SSL_CA_LOCATION,
    ssl_certfile=SSL_CERT_LOCATION,
    ssl_keyfile=SSL_KEY_LOCATION,
    value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
    acks="all"
)

new_data = pd.read_csv("new_data.csv")

for _, row in new_data.iterrows():
    message = row.to_dict()
    producer.send(KAFKA_TOPIC, value=message)
    print("Отправлено:", message)
    time.sleep(0.2)

producer.flush()
producer.close()
print("Отправка завершена")
