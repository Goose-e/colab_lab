import subprocess
import os

CA_PEM = "/content/ca.pem"
CERT_PEM = "/content/service.cert"
KEY_PEM = "/content/service.key"
KEYSTORE_PATH = "/content/kafka.keystore.p12"
TRUSTSTORE_PATH = "/content/kafka.truststore.jks"
KEYSTORE_PASSWORD = "changeit"

if not all([os.path.exists(CA_PEM), os.path.exists(CERT_PEM), os.path.exists(KEY_PEM)]):
    raise FileNotFoundError("Сертификаты не найдены")

subprocess.run([
    "keytool", "-importcert",
    "-file", CA_PEM,
    "-keystore", TRUSTSTORE_PATH,
    "-alias", "ca",
    "-noprompt",
    "-storepass", KEYSTORE_PASSWORD
], check=True)

subprocess.run([
    "openssl", "pkcs12", "-export",
    "-in", CERT_PEM,
    "-inkey", KEY_PEM,
    "-out", KEYSTORE_PATH,
    "-name", "client",
    "-passout", f"pass:{KEYSTORE_PASSWORD}"
], check=True)

print("Keystore и Truststore созданы")
print("Keystore:", KEYSTORE_PATH)
print("Truststore:", TRUSTSTORE_PATH)
