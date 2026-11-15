import subprocess
import os

CA_PEM = "/content/colab_lab/ca.pem"
CERT_PEM = "/content/colab_lab/service.cert"
KEY_PEM = "/content/colab_lab/service.key"
KEYSTORE_PATH = "/content/colab_lab/kafka.keystore.p12"
TRUSTSTORE_PATH = "/content/colab_lab/kafka.truststore.jks"
KEYSTORE_PASSWORD = "passw12"

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
